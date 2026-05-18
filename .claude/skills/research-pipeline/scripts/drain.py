"""Drain pipeline orchestrator — runs stages 1-4 automatically.

Stage 5 (content extraction into reports) is agent-side and remains manual.
This script does all the mechanical work and produces a summary the agent
uses to drive stage 5.

Pipeline:
  Stage 1  — Inventory uningested files in ingestion_paths.
  Stage 2  — Try to extract a URL from each file.
             Files in `reference-only/<id>/` get reconciled (no URL needed).
             Files in ingestion drop dirs without URL → flagged as error.
  Stage 3  — For each (file, URL) tuple:
               - Create new record OR add file to existing record
               - Extract a title from the file content (HTML/MHTML/MD/TXT)
                 and store it on the record so the audit passes
               - git mv the file into reference-only/<id>/<filename>
               - For URL-list .txt files: create wanted records, delete the list
  Stage 4  — Run lint-sources.sh. Halt if it fails.
  Stage 4b — Audit each touched record via audit-records.py per the
             `audit_after_ingestion` config knob (always|sometimes|never).
             Findings are surfaced to the agent/user but do NOT fail the run —
             they're a forward-thinking signal: if drain produces an issue
             flagged by the audit, drain.py is missing a step.

Output: a drain-summary report on stdout (markdown) telling the agent what
was processed, what failed, and what records are ready for stage 5.

Usage:
    python drain.py                 # process all ingestion paths
    python drain.py --dry-run       # show what would happen
    python drain.py --no-lint       # skip stage 4 (don't recommend in production)
    python drain.py --target <dir>  # only scan one specific dir
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _config import (  # noqa: E402
    data_path, library_path, ingestion_paths, load_config, repo_root,
    resolve, skill_md_path, ConfigError,
)
from url_canonicalize import canonicalize_and_id, canonicalize_url  # noqa: E402
from extract_url import extract_url, companion_path  # noqa: E402
from update_plan import update_plan_after_drain  # noqa: E402
from extract_title import extract_title  # noqa: E402
from classify_text import classify  # noqa: E402
from youtube_urls import (  # noqa: E402
    canonicalize_youtube_url, extract_youtube_urls_from_file,
    first_line_youtube_url, is_youtube_url,
)

AUDIT_SCRIPT = Path(__file__).resolve().parent / "audit-records.py"

# Format detection
EXT_TO_FORMAT = {
    ".html": "html", ".htm": "html",
    ".mhtml": "mhtml",
    ".md": "md",
    ".txt": "txt",
    ".pdf": "pdf",
    ".ipynb": "ipynb",
    ".png": "image/png",
    ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".svg": "image/svg+xml",
    ".gif": "image/gif",
    ".webp": "image/webp",
    ".json": "json",
}

IMAGE_FORMATS = {
    "image/png", "image/jpeg", "image/svg+xml", "image/gif", "image/webp",
}


def detect_format(filename: str) -> str:
    return EXT_TO_FORMAT.get(Path(filename).suffix.lower(), "other")


class DrainResult:
    """Accumulator for drain run; emits a markdown summary."""

    def __init__(self):
        self.url_lists_processed: list[tuple[Path, int]] = []  # (file, n_urls_added)
        self.files_added_to_existing: list[tuple[Path, str]] = []  # (file, record_id)
        self.files_added_as_new_records: list[tuple[Path, str]] = []
        self.reconciled_orphans: list[tuple[Path, str]] = []
        self.transcripts_delivered: list[tuple[Path, str, str]] = []  # (file, record_id, video_url)
        self.companions_consumed: list[tuple[Path, Path]] = []  # (companion, target)
        self.companions_orphaned: list[Path] = []  # companion with no resolved target
        self.wants_purged: list[tuple[str, int]] = []  # (record_id, count)
        self.errors_no_url: list[Path] = []
        self.errors_classification: list[tuple[Path, str]] = []
        self.errors_image_in_drop: list[Path] = []
        self.errors_unmatched_transcript: list[tuple[Path, str]] = []  # (file, video_url)
        self.records_with_image_summaries_pending: set[str] = set()
        # (referrer_record_id, source_file, video_url, snippet)
        self.youtube_embed_candidates: list[tuple[str, Path, str, str]] = []
        self.touched_record_ids: set[str] = set()
        self.lint_exit_code: int | None = None
        self.lint_output: str = ""
        self.audit_mode: str = "always"
        self.audit_ran: bool = False
        self.audit_exit_code: int | None = None
        self.audit_output: str = ""

    def to_markdown(self) -> str:
        lines = [
            "# Drain run summary",
            "",
            f"- URL lists processed: **{len(self.url_lists_processed)}** "
            f"({sum(n for _, n in self.url_lists_processed)} new wanted records)",
            f"- Files attached to existing records: **{len(self.files_added_to_existing)}**",
            f"- Files added as new records: **{len(self.files_added_as_new_records)}**",
            f"- Orphan files reconciled in `reference-only/<id>/`: **{len(self.reconciled_orphans)}**",
            f"- YouTube transcripts delivered (want → have): **{len(self.transcripts_delivered)}**",
            f"- Companion URL files consumed: **{len(self.companions_consumed)}**",
            f"- Companion URL files left orphaned (target not ingested): **{len(self.companions_orphaned)}**",
            f"- Stale `want` entries cleared by format-final attachments: **{sum(n for _, n in self.wants_purged)}** "
            f"(across {len(self.wants_purged)} record(s))",
            f"- Files flagged (no extractable URL in drop dir): **{len(self.errors_no_url)}**",
            f"- Files flagged (mixed/unrecognized content): **{len(self.errors_classification)}**",
            f"- Images in drop dirs without `<id>/` placement: **{len(self.errors_image_in_drop)}**",
            f"- Transcript files with no matching wanted entry: **{len(self.errors_unmatched_transcript)}**",
            f"- Records with images pending summary: **{len(self.records_with_image_summaries_pending)}**",
            f"- YouTube embed candidates (awaiting agent judgement): **{len(self.youtube_embed_candidates)}**",
            "",
            f"**Lint exit code:** {self.lint_exit_code}",
            "",
        ]
        if self.lint_exit_code and self.lint_exit_code != 0:
            lines.append("**Lint failed — halt before stage 5 (content processing).**\n")
            lines.append("```")
            lines.append(self.lint_output[-2000:])
            lines.append("```")
            lines.append("")
            return "\n".join(lines)

        if self.files_added_as_new_records:
            lines.append("## Stage 5 candidates — new records")
            lines.append("")
            for f, rid in self.files_added_as_new_records:
                lines.append(f"- `{rid}` — {f.name}")
            lines.append("")
        if self.files_added_to_existing:
            lines.append("## Stage 5 candidates — files added to existing records")
            lines.append("")
            for f, rid in self.files_added_to_existing:
                lines.append(f"- `{rid}` — {f.name}")
            lines.append("")
        if self.reconciled_orphans:
            lines.append("## Reconciled orphan files (already in <id>/ dirs)")
            lines.append("")
            for f, rid in self.reconciled_orphans:
                lines.append(f"- `{rid}` — {f.name}")
            lines.append("")
        if self.records_with_image_summaries_pending:
            lines.append("## Records with pending image summaries (Stage 3b)")
            lines.append("")
            for rid in sorted(self.records_with_image_summaries_pending):
                lines.append(f"- `{rid}`")
            lines.append("")
        if self.transcripts_delivered:
            lines.append("## YouTube transcripts delivered")
            lines.append("")
            for f, rid, video in self.transcripts_delivered:
                lines.append(f"- `{rid}` — {f.name} (video {video})")
            lines.append("")
        if self.youtube_embed_candidates:
            lines.append("## YouTube embed candidates (agent: evaluate, then add wanted entries)")
            lines.append("")
            lines.append("Each link below was found in an ingested document. If the "
                         "surrounding text suggests the video would be a useful source, "
                         "add a `want` file entry of format `youtube-transcript` on the "
                         "embedding record with `youtube_url` set. See "
                         "`resources/_drain/youtube-transcripts.md`.")
            lines.append("")
            for rid, src, url, snippet in self.youtube_embed_candidates:
                lines.append(f"- `{rid}` ← `{src.name}`: {url}")
                if snippet:
                    lines.append(f"  > {snippet[:240]}")
            lines.append("")
        if (self.errors_no_url or self.errors_classification
                or self.errors_image_in_drop or self.errors_unmatched_transcript
                or self.companions_orphaned):
            lines.append("## Flagged files (NOT ingested)")
            lines.append("")
            for f in self.errors_no_url:
                lines.append(f"- ❌ `{f}` — no extractable URL")
            for f, reason in self.errors_classification:
                lines.append(f"- ❌ `{f}` — {reason}")
            for f in self.errors_image_in_drop:
                lines.append(f"- ⚠ `{f}` — image in drop dir; move to `reference-only/<id>/` manually")
            for f, video_url in self.errors_unmatched_transcript:
                lines.append(
                    f"- ⚠ `{f}` — transcript for {video_url} but no wanted "
                    f"`youtube-transcript` entry references that video. Move to "
                    f"`reference-only/<id>/` of the embedding record manually, or "
                    f"add the wanted entry first."
                )
            for f in self.companions_orphaned:
                lines.append(
                    f"- ⚠ `{f}` — companion URL file whose target was not ingested "
                    f"(target missing or itself failed to ingest); left in place."
                )
            lines.append("")

        if self.audit_ran:
            lines.append(f"## Audit (mode: `{self.audit_mode}`)")
            lines.append("")
            if self.audit_exit_code == 0:
                lines.append(
                    f"✓ audit clean across {len(self.touched_record_ids)} touched record(s)."
                )
            else:
                lines.append(
                    f"⚠ audit flagged issues on touched record(s) "
                    f"(exit code {self.audit_exit_code}). Findings:"
                )
                lines.append("")
                lines.append("```")
                lines.append(self.audit_output.strip()[-2000:])
                lines.append("```")
                lines.append("")
                lines.append(
                    "For each finding: either fix the record, or — if the issue "
                    "points to a gap in the drain pipeline — extend `drain.py` so "
                    "future ingestions satisfy the check."
                )
            lines.append("")
        elif self.audit_mode == "never":
            lines.append("_Audit skipped (`audit_after_ingestion: never`)._")
            lines.append("")

        return "\n".join(lines)


COMPANION_NAME_RE = re.compile(r"^URL of (.+)\.txt$")

# Files in ingestion drop directories whose filename is one of these are
# documentation about the directory itself, not content to ingest. They're
# silently skipped by stage 1 inventory. Case-insensitive match.
INVENTORY_SKIP_FILENAMES = {
    "readme.md", "readme.txt", "readme",
    "notes.md", "notes.txt",
    "agents.md", "claude.md",
    ".gitignore", ".gitkeep",
}


# "Format-final" rule. A file is format-final for a record if its format is
# the best we can capture for the record's canonical URL — in which case any
# generic `want` placeholder on the same record can be safely cleared, since
# no later ingestion will improve on it.
#
#   - MHTML for any URL: always format-final (highest-fidelity HTML save;
#     embeds CSS + images; nothing strictly better exists).
#   - PDF / TXT / MD / CSV / JSON / IPYNB for a URL whose path ends with the
#     matching extension: format-final (the file IS the URL's payload).
#   - HTML / HTM: format-final only if the URL ends with `.html` / `.htm`
#     (MHTML is generally better for arbitrary article URLs).
#   - Anything else: not format-final.
#
# Paywall / JS-block evidence overrides this rule — but that's caller-side
# (the audit can mark a file `completeness: error`, which signals re-fetch).

FORMAT_FINAL_EXTENSIONS = {
    "pdf": ".pdf",
    "txt": ".txt",
    "md": ".md",
    "csv": ".csv",
    "json": ".json",
    "ipynb": ".ipynb",
}


def _url_path_extension(url: str) -> str:
    """Return the lowercased extension of the URL's path (incl. leading dot),
    or '' if there's no extension. Strips query string + fragment.
    """
    if not url:
        return ""
    # Cut off query and fragment.
    for sep in ("?", "#"):
        i = url.find(sep)
        if i != -1:
            url = url[:i]
    # Find the last path segment.
    last = url.rsplit("/", 1)[-1]
    if "." not in last:
        return ""
    return "." + last.rsplit(".", 1)[-1].lower()


def is_format_final(file_format: str, canonical_url: str) -> bool:
    """Return True iff a `have` file in this format is the best capture
    we can hope to get for canonical_url — meaning any matching generic
    `want` entries on the same record can be cleared.
    """
    if file_format == "mhtml":
        return True
    ext = _url_path_extension(canonical_url)
    if file_format in ("html", "htm"):
        return ext in (".html", ".htm")
    expected = FORMAT_FINAL_EXTENSIONS.get(file_format)
    if expected is None:
        return False
    return ext == expected


def _purge_satisfied_wants(files: list, canonical_url: str) -> int:
    """Remove generic `want` entries on a record that have now been
    satisfied. A generic want is one without a `youtube_url` field;
    transcript wants are tied to a specific video and are NEVER touched
    by this function.

    A generic want is "satisfied" iff EITHER:
      (a) some `have` file on the record is format-final for canonical_url
          (mhtml always; matching-extension otherwise — see is_format_final), OR
      (b) some `have` file on the record has the same `format` as the want.

    Returns the count of `want` entries removed.
    """
    haves = [
        f for f in files
        if isinstance(f, dict) and f.get("ingestion_status") == "have"
    ]
    has_format_final = any(
        is_format_final(h.get("format", ""), canonical_url) for h in haves
    )
    have_formats = {h.get("format", "") for h in haves}
    keep: list = []
    removed = 0
    for f in files:
        if (isinstance(f, dict)
                and f.get("ingestion_status") == "want"
                and not f.get("youtube_url")):
            want_fmt = f.get("format", "")
            satisfied = has_format_final or (want_fmt in have_formats)
            if satisfied:
                removed += 1
                continue
        keep.append(f)
    files[:] = keep
    return removed


# Back-compat alias for external imports during the refactor.
_purge_generic_wants = _purge_satisfied_wants


def stage_1_inventory(roots: list[Path]) -> tuple[list[Path], dict[Path, Path]]:
    """Find every file in ingestion paths that's a candidate for ingestion.

    Returns (candidates, companions) where companions maps a target path
    to its `URL of <target.name>.txt` sibling. Companions are NOT in the
    candidates list — they're consumed when their target is ingested.

    A companion file whose target is missing from the ingestion paths is
    NOT a candidate either; it's surfaced as an orphan in the summary.
    """
    candidates: list[Path] = []
    companions: dict[Path, Path] = {}
    suffixes = set(EXT_TO_FORMAT.keys())
    for root in roots:
        if not root.exists():
            continue
        for p in sorted(root.rglob("*")):
            if not (p.is_file() and p.suffix.lower() in suffixes):
                continue
            if p.name.lower() in INVENTORY_SKIP_FILENAMES:
                # Directory README / NOTES / AGENTS / etc. — not ingestable
                # content; silently skipped.
                continue
            m = COMPANION_NAME_RE.match(p.name)
            if m:
                target = p.parent / m.group(1)
                companions[target] = p
                continue
            candidates.append(p)
    return candidates, companions


def stage_1b_url_lists(candidates: list[Path], result: DrainResult, data: dict,
                       dry_run: bool) -> list[Path]:
    """Process URL-list files. Returns the candidates list with them removed."""
    remaining = []
    for f in candidates:
        if f.suffix.lower() not in {".txt", ".md"}:
            remaining.append(f)
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            remaining.append(f)
            continue
        cls = classify(text)
        if cls["kind"] == "url_list":
            n_added = 0
            for raw_url in cls["urls"]:
                try:
                    canon, rid = canonicalize_and_id(raw_url)
                except ValueError:
                    continue
                if rid not in data:
                    data[rid] = {
                        "id": rid,
                        "canonical_url": canon,
                        "title": "(unknown)",
                        "files": [],
                    }
                    n_added += 1
                # Every URL in the list — new or not — counts as touched, so
                # audit can flag it if the record is still incomplete.
                result.touched_record_ids.add(rid)
            result.url_lists_processed.append((f, n_added))
            if not dry_run:
                f.unlink()
            continue
        if cls["kind"] == "mixed_error":
            result.errors_classification.append((f, "mixed_error: URLs mixed with non-URL content"))
            remaining.append(f)  # don't process further
            continue
        if cls["kind"] == "unrecognized":
            result.errors_classification.append((f, "unrecognized: no clear URL structure"))
            remaining.append(f)
            continue
        # source_with_first_url / source_with_header_url → stage 2
        remaining.append(f)
    return remaining


def _find_wanted_transcript(data: dict, video_url: str) -> tuple[str, int] | None:
    """Return (record_id, file_index) of the first wanted youtube-transcript
    file entry whose youtube_url matches video_url, or None."""
    for rid, record in data.items():
        if not isinstance(record, dict):
            continue
        for i, fe in enumerate(record.get("files") or []):
            if not isinstance(fe, dict):
                continue
            if fe.get("format") != "youtube-transcript":
                continue
            if fe.get("ingestion_status") != "want":
                continue
            if fe.get("youtube_url") == video_url:
                return rid, i
    return None


def _try_deliver_transcript(f: Path, result: DrainResult, data: dict,
                            dry_run: bool) -> bool:
    """If `f` is a .txt whose first line is a YouTube URL, attempt to
    promote a matching wanted entry from want → have. Returns True if the
    file was handled (either delivered or flagged unmatched); False if
    it's not a transcript file and the caller should fall through to
    normal URL extraction.
    """
    if f.suffix.lower() != ".txt":
        return False
    video = first_line_youtube_url(f)
    if not video:
        return False

    root = repo_root()
    lib = library_path()
    match = _find_wanted_transcript(data, video)
    if match is None:
        result.errors_unmatched_transcript.append((f.relative_to(root), video))
        return True

    rid, idx = match
    try:
        sha = hashlib.sha256(f.read_bytes()).hexdigest()
    except OSError:
        result.errors_classification.append(
            (f.relative_to(root), "could not read transcript file")
        )
        return True

    dst = lib / rid / f.name
    if dry_run:
        result.transcripts_delivered.append((f.relative_to(root), rid, video))
        result.touched_record_ids.add(rid)
        return True

    dst.parent.mkdir(parents=True, exist_ok=True)
    # Avoid clobbering an existing file at dst
    if dst.exists() and dst.resolve() != f.resolve():
        result.errors_classification.append(
            (f.relative_to(root),
             f"transcript collision: {dst.relative_to(root)} already exists")
        )
        return True
    try:
        subprocess.run(
            ["git", "mv", str(f.relative_to(root)), str(dst.relative_to(root))],
            cwd=root, check=True, capture_output=True, text=True,
        )
    except subprocess.CalledProcessError:
        if not dst.exists():
            shutil.move(str(f), str(dst))

    entry = data[rid]["files"][idx]
    entry["filename"] = f.name
    entry["sha256"] = sha
    entry["ingestion_status"] = "have"
    entry.setdefault("completeness", "unknown")
    # youtube_url stays as-is (already set on the wanted entry).
    result.transcripts_delivered.append((f.relative_to(root), rid, video))
    result.touched_record_ids.add(rid)
    return True


def _scan_for_youtube_embeds(record_id: str, file_path: Path,
                             record: dict, result: DrainResult) -> None:
    """Surface YouTube URLs found in an ingested document as candidates
    for the agent to (manually) add wanted transcript entries for.

    Skips URLs already covered by an existing youtube-transcript file
    entry on the same record (any status).
    """
    mentions = extract_youtube_urls_from_file(file_path)
    if not mentions:
        return
    already: set[str] = set()
    for fe in record.get("files") or []:
        if isinstance(fe, dict) and fe.get("format") == "youtube-transcript":
            yu = fe.get("youtube_url")
            if yu:
                already.add(yu)
    for m in mentions:
        if m.url in already:
            continue
        result.youtube_embed_candidates.append(
            (record_id, file_path, m.url, m.snippet)
        )


def _consume_companion(target: Path, companions: dict[Path, Path],
                       result: DrainResult, root: Path, dry_run: bool) -> None:
    """If `target` has a registered companion file, git-rm it. Called
    after the target has been successfully ingested."""
    comp = companions.pop(target, None)
    if comp is None or not comp.exists():
        return
    if dry_run:
        result.companions_consumed.append((comp.relative_to(root), target.relative_to(root) if target.exists() else target))
        return
    try:
        subprocess.run(
            ["git", "rm", str(comp.relative_to(root))],
            cwd=root, check=True, capture_output=True, text=True,
        )
    except subprocess.CalledProcessError:
        comp.unlink(missing_ok=True)
    result.companions_consumed.append((comp.relative_to(root), target))


def stage_2_3_per_file(candidates: list[Path], result: DrainResult, data: dict,
                       dry_run: bool, companions: dict[Path, Path] | None = None):
    """For each file: extract URL, create/update record, move file."""
    lib = library_path()
    root = repo_root()
    companions = companions if companions is not None else {}

    for f in candidates:
        # Images in drop dirs without <id>/ → flag
        fmt = detect_format(f.name)
        if fmt in IMAGE_FORMATS:
            result.errors_image_in_drop.append(f.relative_to(root))
            continue

        # YouTube transcript delivery (.txt with first-line video URL) —
        # handled separately because the file's URL is *not* the parent
        # record's canonical URL.
        if _try_deliver_transcript(f, result, data, dry_run):
            continue

        # Try URL extraction
        url = extract_url(f)
        if url is None:
            result.errors_no_url.append(f.relative_to(root))
            continue

        try:
            canon, rid = canonicalize_and_id(url)
        except ValueError:
            result.errors_classification.append(
                (f.relative_to(root), f"URL extraction yielded invalid URL: {url}")
            )
            continue

        # Follow pointer_to if applicable
        if rid in data:
            ptr = data[rid].get("pointer_to")
            if ptr and ptr in data:
                rid = ptr  # resolve to canonical record

        # Compute sha256 of the file
        try:
            sha = hashlib.sha256(f.read_bytes()).hexdigest()
        except OSError:
            result.errors_classification.append(
                (f.relative_to(root), "could not read file")
            )
            continue

        # Skip if a file with this sha is already registered anywhere in the catalog
        # (this happens when research/manual/ still has legacy copies of files we've
        # already moved into reference-only/<id>/).
        already_registered = False
        if rid in data:
            for x in data[rid].get("files", []):
                if isinstance(x, dict) and x.get("sha256") == sha:
                    already_registered = True
                    break
        if already_registered:
            if not dry_run:
                # Just delete the duplicate from the drop dir
                try:
                    subprocess.run(
                        ["git", "rm", str(f.relative_to(root))],
                        cwd=root, check=True, capture_output=True, text=True,
                    )
                except subprocess.CalledProcessError:
                    f.unlink(missing_ok=True)
            _consume_companion(f, companions, result, root, dry_run)
            continue

        # Plan the move
        dst = lib / rid / f.name

        if dry_run:
            if rid in data:
                result.files_added_to_existing.append((f.relative_to(root), rid))
            else:
                result.files_added_as_new_records.append((f.relative_to(root), rid))
            _consume_companion(f, companions, result, root, dry_run)
            continue

        # Execute the move
        dst.parent.mkdir(parents=True, exist_ok=True)
        try:
            subprocess.run(
                ["git", "mv", str(f.relative_to(root)), str(dst.relative_to(root))],
                cwd=root, check=True, capture_output=True, text=True,
            )
        except subprocess.CalledProcessError:
            # Fall back to plain move
            if not dst.exists():
                shutil.move(str(f), str(dst))

        # Build the file entry
        file_entry = {
            "format": fmt,
            "filename": f.name,
            "sha256": sha,
            "ingestion_status": "have",
            "completeness": "unknown",
        }

        # Best-effort title extraction from the now-moved file. We read from
        # the destination because the source was just git-mv'd. Falling back
        # to "(unknown)" only if extraction yields nothing — the audit will
        # then flag the record so the user knows to fill it in.
        extracted_title = extract_title(dst) if dst.exists() else None

        if rid in data:
            # Append to existing record
            files = data[rid].get("files", [])
            # Skip if filename already registered
            if any(isinstance(x, dict) and x.get("filename") == f.name for x in files):
                continue
            files.append(file_entry)
            # Clear any generic `want` placeholders that are now satisfied
            # (format-final attach, OR same-format have already on record).
            # Transcript-format wants (those carrying youtube_url) are
            # preserved — different ingestion track.
            purged = _purge_satisfied_wants(files, data[rid].get("canonical_url", ""))
            if purged:
                result.wants_purged.append((rid, purged))
            data[rid]["files"] = files
            # If the existing title is the placeholder and we extracted a real
            # one from this newly-attached file, upgrade it.
            if (data[rid].get("title") in (None, "", "(unknown)")) and extracted_title:
                data[rid]["title"] = extracted_title
            result.files_added_to_existing.append((f.relative_to(root), rid))
        else:
            # Create new record
            data[rid] = {
                "id": rid,
                "canonical_url": canon,
                "title": extracted_title or "(unknown)",
                "files": [file_entry],
            }
            result.files_added_as_new_records.append((f.relative_to(root), rid))
        result.touched_record_ids.add(rid)

        # Surface any YouTube URLs found in this newly-ingested document
        # so the agent can decide whether to add wanted transcript entries.
        scan_target = dst if dst.exists() else f
        _scan_for_youtube_embeds(rid, scan_target, data[rid], result)

        # The target made it into the catalog; the companion URL file (if
        # any) has done its job and can be removed.
        _consume_companion(f, companions, result, root, dry_run)


def stage_3c_reconcile(result: DrainResult, data: dict, dry_run: bool):
    """For each per-id directory with orphan files, add them to the record."""
    lib = library_path()
    root = repo_root()
    id_re = re.compile(r"^[0-9a-f]{10}$")

    if not lib.exists():
        return

    for entry in sorted(lib.iterdir()):
        if not entry.is_dir() or not id_re.match(entry.name):
            continue
        rid = entry.name
        if rid not in data:
            continue
        record = data[rid]
        existing_filenames = {
            x.get("filename") for x in record.get("files", [])
            if isinstance(x, dict) and x.get("filename") and not x.get("location")
        }
        for f in sorted(entry.iterdir()):
            if not f.is_file() or f.name in existing_filenames or f.name.startswith("."):
                continue
            fmt = detect_format(f.name)
            try:
                sha = hashlib.sha256(f.read_bytes()).hexdigest()
            except OSError:
                continue

            # YouTube-transcript detection: a .txt whose first line is a
            # YouTube URL is a transcript file, not a plain txt source.
            yt_url = first_line_youtube_url(f) if fmt == "txt" else None
            if yt_url:
                # If a wanted entry on this record matches, promote it
                # in place rather than appending a new entry.
                promoted = False
                for fe in record.get("files") or []:
                    if (isinstance(fe, dict)
                            and fe.get("format") == "youtube-transcript"
                            and fe.get("ingestion_status") == "want"
                            and fe.get("youtube_url") == yt_url):
                        if not dry_run:
                            fe["filename"] = f.name
                            fe["sha256"] = sha
                            fe["ingestion_status"] = "have"
                            fe.setdefault("completeness", "unknown")
                        result.transcripts_delivered.append(
                            (f.relative_to(root), rid, yt_url)
                        )
                        result.touched_record_ids.add(rid)
                        promoted = True
                        break
                if promoted:
                    continue
                # No wanted entry — add a new have entry directly.
                file_entry = {
                    "format": "youtube-transcript",
                    "filename": f.name,
                    "sha256": sha,
                    "ingestion_status": "have",
                    "completeness": "unknown",
                    "youtube_url": yt_url,
                }
                if not dry_run:
                    record.setdefault("files", []).append(file_entry)
                result.reconciled_orphans.append((f.relative_to(root), rid))
                result.touched_record_ids.add(rid)
                continue

            file_entry = {
                "format": fmt,
                "filename": f.name,
                "sha256": sha,
                "ingestion_status": "have",
                "completeness": "unknown",
            }
            if fmt in IMAGE_FORMATS:
                file_entry["comment"] = "(image — pending summary)"
                result.records_with_image_summaries_pending.add(rid)
            if not dry_run:
                record.setdefault("files", []).append(file_entry)
            result.reconciled_orphans.append((f.relative_to(root), rid))
            result.touched_record_ids.add(rid)


def stage_4_validate(result: DrainResult) -> None:
    """Run lint-sources.sh and capture its result."""
    script = Path(__file__).resolve().parent / "lint-sources.sh"
    proc = subprocess.run(
        ["bash", str(script)],
        capture_output=True, text=True,
    )
    result.lint_exit_code = proc.returncode
    result.lint_output = proc.stdout + proc.stderr


def stage_4b_audit(result: DrainResult, mode: str) -> None:
    """Run audit-records.py against touched IDs based on `audit_after_ingestion`.

    `mode` values:
        always    — always audit when there are touched records.
        sometimes — audit only when any record had a status change worth
                    re-checking (new have-files attached or records created).
        never     — skip entirely.
    """
    result.audit_mode = mode
    if mode == "never":
        return
    if not result.touched_record_ids:
        return
    if mode == "sometimes":
        # "sometimes" means: only worth running when something materially
        # changed on disk. New records or new have-files qualify; pure
        # wanted-record creation from URL lists does not.
        has_material = bool(result.files_added_as_new_records
                            or result.files_added_to_existing
                            or result.reconciled_orphans)
        if not has_material:
            return

    cmd = [sys.executable, str(AUDIT_SCRIPT), *sorted(result.touched_record_ids)]
    if mode == "always":
        cmd.append("--always-mode-footer")
    proc = subprocess.run(cmd, capture_output=True, text=True)
    result.audit_ran = True
    result.audit_exit_code = proc.returncode
    result.audit_output = proc.stdout + proc.stderr


def normalize_and_write(data: dict, data_p: Path):
    """Write `data` to `data_p` in the canonical normalized shape.

    This output MUST be byte-identical to what
    ``scripts/normalize-sources-json.sh`` produces on the same data
    (which runs ``jq -S '.'`` on the file). Both forms are the single
    source of truth for "normalized sources.json" — the workflow,
    drain.py, and any hand-jq edits all converge on the same bytes.

    Canonical shape:
      - All object keys sorted alphabetically at every level
        (``sort_keys=True`` matches jq's ``-S``).
      - 2-space indent (matches jq default).
      - UTF-8 preserved (``ensure_ascii=False`` matches jq default).
      - Arrays preserve their existing element order.
      - Trailing newline.

    Verified by ``tests/unit/test_normalize_sources.py``.
    """
    tmp = data_p.with_suffix(".json.tmp")
    tmp.write_text(
        json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    tmp.replace(data_p)


def _run_tidy_wants(data: dict, data_p: Path, dry_run: bool) -> int:
    """Catalog-wide want-sweep. For each record, apply `_purge_satisfied_wants`
    to drop any generic `want` entries already satisfied by an existing
    `have` file. Idempotent; safe to re-run.

    Returns 0 always (informational sweep). Prints a per-record summary to
    stdout and writes the catalog atomically (unless --dry-run).
    """
    touched = 0
    purged_total = 0
    lines = ["# Tidy-wants sweep", ""]
    for rid in sorted(data.keys()):
        rec = data[rid]
        if not isinstance(rec, dict):
            continue
        files = list(rec.get("files") or [])
        url = rec.get("canonical_url") or ""
        purged = _purge_satisfied_wants(files, url)
        if not purged:
            continue
        touched += 1
        purged_total += purged
        lines.append(f"- `{rid}` — clearing {purged} stale `want` entr"
                     f"{'y' if purged == 1 else 'ies'}  ({url})")
        if not dry_run:
            rec["files"] = files

    lines.append("")
    lines.append(f"**Records touched:** {touched}  |  "
                 f"**Total `want` entries cleared:** {purged_total}")
    if dry_run:
        lines.append("")
        lines.append("_(dry-run — no changes written)_")
    elif touched:
        normalize_and_write(data, data_p)
        lines.append("")
        lines.append(f"_Catalog rewritten at {data_p.relative_to(repo_root())}._")
    print("\n".join(lines))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="don't modify anything")
    ap.add_argument("--no-lint", action="store_true", help="skip stage 4 validation")
    ap.add_argument("--no-audit", action="store_true",
                    help="skip the post-ingestion audit regardless of config")
    ap.add_argument("--audit-mode", choices=["always", "sometimes", "never"],
                    help="override audit_after_ingestion from config")
    ap.add_argument("--target", help="only scan this dir (instead of all ingestion_paths)")
    ap.add_argument("--tidy-wants", action="store_true",
                    help="catalog-wide sweep: clear stale `want` entries on "
                         "records that already have a format-final `have` file "
                         "for the same URL. Skips the regular drain pipeline.")
    ap.add_argument("--no-plan-update", action="store_true",
                    help="skip the automatic Session-bullet + §10-row insertion "
                         "into research/PLAN.md. Use only if you intend to write "
                         "the entry by hand in the same commit.")
    args = ap.parse_args()

    try:
        data_p = data_path()
    except ConfigError as e:
        print(f"✗ Config error: {e}", file=sys.stderr)
        return 1

    if not data_p.exists():
        print(f"✗ {data_p} does not exist — bootstrap first", file=sys.stderr)
        return 1

    data = json.loads(data_p.read_text(encoding="utf-8"))

    if args.tidy_wants:
        return _run_tidy_wants(data, data_p, args.dry_run)

    roots = [Path(args.target)] if args.target else ingestion_paths()
    result = DrainResult()

    # Stage 1
    candidates, companions = stage_1_inventory(roots)
    print(f"Stage 1: {len(candidates)} candidate file(s) inventoried"
          f" ({len(companions)} companion URL file(s) paired)", file=sys.stderr)

    # Stage 1b: handle URL lists
    candidates = stage_1b_url_lists(candidates, result, data, args.dry_run)
    if result.url_lists_processed:
        print(f"Stage 1b: processed {len(result.url_lists_processed)} URL list(s)", file=sys.stderr)

    # Stages 2 + 3 combined
    stage_2_3_per_file(candidates, result, data, args.dry_run, companions)

    # Any companion file whose target wasn't ingested stays put — flag it.
    root = repo_root()
    for target, comp in companions.items():
        if comp.exists():
            result.companions_orphaned.append(comp.relative_to(root))
    print(f"Stage 2-3: {len(result.files_added_to_existing) + len(result.files_added_as_new_records)} "
          f"file(s) ingested, {len(result.errors_no_url) + len(result.errors_classification)} flagged",
          file=sys.stderr)

    # Stage 3c: reconcile orphans in <id>/ dirs
    stage_3c_reconcile(result, data, args.dry_run)
    if result.reconciled_orphans:
        print(f"Stage 3c: reconciled {len(result.reconciled_orphans)} orphan file(s)", file=sys.stderr)

    # Write back the catalog
    if not args.dry_run:
        normalize_and_write(data, data_p)

    # Stage 4: validate
    if not args.no_lint and not args.dry_run:
        stage_4_validate(result)
        print(f"Stage 4: lint exit code {result.lint_exit_code}", file=sys.stderr)

    # Stage 4b: per-record audit on touched IDs
    if not args.no_audit and not args.dry_run:
        if args.audit_mode:
            mode = args.audit_mode
        else:
            try:
                mode = load_config().get("audit_after_ingestion", "always")
            except ConfigError:
                mode = "always"
        if mode not in {"always", "sometimes", "never"}:
            print(f"⚠ audit_after_ingestion={mode!r} invalid; defaulting to 'always'",
                  file=sys.stderr)
            mode = "always"
        stage_4b_audit(result, mode)
        if result.audit_ran:
            print(f"Stage 4b: audit exit code {result.audit_exit_code} "
                  f"on {len(result.touched_record_ids)} touched record(s)",
                  file=sys.stderr)
        else:
            print(f"Stage 4b: audit skipped (mode={result.audit_mode}, "
                  f"touched={len(result.touched_record_ids)})", file=sys.stderr)

    # Stage 4c: auto-record this drain in research/PLAN.md so the corpus
    # narrative stays in step with the catalog. Skipped on --dry-run,
    # --no-plan-update, or if the drain made no material changes.
    plan_update_status: dict | None = None
    if not args.dry_run and not args.no_plan_update:
        try:
            cfg_plan_path = resolve(load_config().get("plan_path", "research/PLAN.md"))
        except ConfigError:
            cfg_plan_path = resolve("research/PLAN.md")
        plan_update_status = update_plan_after_drain(result, cfg_plan_path)
        if plan_update_status.get("skipped"):
            print(f"Stage 4c: PLAN.md update skipped — "
                  f"{plan_update_status.get('skipped_reason')}", file=sys.stderr)
        else:
            print(f"Stage 4c: PLAN.md updated — Round-{plan_update_status.get('round_number')} "
                  f"bullet={plan_update_status.get('bullet_inserted')} "
                  f"row={plan_update_status.get('row_inserted')} "
                  f"version={plan_update_status.get('version_after')}", file=sys.stderr)

    # Print summary to stdout (this is the agent's input to stage 5)
    print(result.to_markdown())
    if plan_update_status and not plan_update_status.get("skipped"):
        print()
        print(f"## PLAN.md auto-update")
        print()
        print(f"- Round number assigned: **{plan_update_status.get('round_number')}**")
        print(f"- Session bullet inserted under §1: **{plan_update_status.get('bullet_inserted')}**")
        print(f"- §10 lookup-table row inserted: **{plan_update_status.get('row_inserted')}**")
        print(f"- Version line bumped to: **{plan_update_status.get('version_after')}**")
        print()
        print(f"Both the bullet and the row are placeholder text. **Edit them to be hand-written** "
              f"before the commit lands; see "
              f"`.claude/skills/research-pipeline/resources/_plan/update-discipline.md`.")

    # Exit code reflects lint result (audit findings are informational, not fatal —
    # they're hints for what to fix or what to add to drain).
    if result.lint_exit_code and result.lint_exit_code != 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
