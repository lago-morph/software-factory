"""Drain pipeline orchestrator — runs stages 1-4 automatically.

Stage 5 (content extraction into reports) is agent-side and remains manual.
This script does all the mechanical work and produces a summary the agent
uses to drive stage 5.

Pipeline:
  Stage 1 — Inventory uningested files in ingestion_paths.
  Stage 2 — Try to extract a URL from each file.
            Files in `reference-only/<id>/` get reconciled (no URL needed).
            Files in ingestion drop dirs without URL → flagged as error.
  Stage 3 — For each (file, URL) tuple:
              - Create new record OR add file to existing record
              - git mv the file into reference-only/<id>/<filename>
              - For URL-list .txt files: create wanted records, delete the list
  Stage 4 — Run lint-sources.sh. Halt if it fails.

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
    data_path, library_path, ingestion_paths, repo_root, ConfigError,
)
from url_canonicalize import canonicalize_and_id, canonicalize_url  # noqa: E402
from extract_url import extract_url  # noqa: E402
from classify_text import classify  # noqa: E402

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
        self.errors_no_url: list[Path] = []
        self.errors_classification: list[tuple[Path, str]] = []
        self.errors_image_in_drop: list[Path] = []
        self.records_with_image_summaries_pending: set[str] = set()
        self.lint_exit_code: int | None = None
        self.lint_output: str = ""

    def to_markdown(self) -> str:
        lines = [
            "# Drain run summary",
            "",
            f"- URL lists processed: **{len(self.url_lists_processed)}** "
            f"({sum(n for _, n in self.url_lists_processed)} new wanted records)",
            f"- Files attached to existing records: **{len(self.files_added_to_existing)}**",
            f"- Files added as new records: **{len(self.files_added_as_new_records)}**",
            f"- Orphan files reconciled in `reference-only/<id>/`: **{len(self.reconciled_orphans)}**",
            f"- Files flagged (no extractable URL in drop dir): **{len(self.errors_no_url)}**",
            f"- Files flagged (mixed/unrecognized content): **{len(self.errors_classification)}**",
            f"- Images in drop dirs without `<id>/` placement: **{len(self.errors_image_in_drop)}**",
            f"- Records with images pending summary: **{len(self.records_with_image_summaries_pending)}**",
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
        if self.errors_no_url or self.errors_classification or self.errors_image_in_drop:
            lines.append("## Flagged files (NOT ingested)")
            lines.append("")
            for f in self.errors_no_url:
                lines.append(f"- ❌ `{f}` — no extractable URL")
            for f, reason in self.errors_classification:
                lines.append(f"- ❌ `{f}` — {reason}")
            for f in self.errors_image_in_drop:
                lines.append(f"- ⚠ `{f}` — image in drop dir; move to `reference-only/<id>/` manually")
            lines.append("")

        return "\n".join(lines)


def stage_1_inventory(roots: list[Path]) -> list[Path]:
    """Find every file in ingestion paths that's a candidate for ingestion."""
    candidates = []
    suffixes = set(EXT_TO_FORMAT.keys())
    for root in roots:
        if not root.exists():
            continue
        for p in sorted(root.rglob("*")):
            if p.is_file() and p.suffix.lower() in suffixes:
                candidates.append(p)
    return candidates


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


def stage_2_3_per_file(candidates: list[Path], result: DrainResult, data: dict,
                       dry_run: bool):
    """For each file: extract URL, create/update record, move file."""
    lib = library_path()
    root = repo_root()

    for f in candidates:
        # Images in drop dirs without <id>/ → flag
        fmt = detect_format(f.name)
        if fmt in IMAGE_FORMATS:
            result.errors_image_in_drop.append(f.relative_to(root))
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
            continue

        # Plan the move
        dst = lib / rid / f.name

        if dry_run:
            if rid in data:
                result.files_added_to_existing.append((f.relative_to(root), rid))
            else:
                result.files_added_as_new_records.append((f.relative_to(root), rid))
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

        if rid in data:
            # Append to existing record
            files = data[rid].get("files", [])
            # Skip if filename already registered
            if any(isinstance(x, dict) and x.get("filename") == f.name for x in files):
                continue
            files.append(file_entry)
            data[rid]["files"] = files
            result.files_added_to_existing.append((f.relative_to(root), rid))
        else:
            # Create new record
            data[rid] = {
                "id": rid,
                "canonical_url": canon,
                "title": "(unknown)",
                "files": [file_entry],
            }
            result.files_added_as_new_records.append((f.relative_to(root), rid))


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


def stage_4_validate(result: DrainResult) -> None:
    """Run lint-sources.sh and capture its result."""
    script = Path(__file__).resolve().parent / "lint-sources.sh"
    proc = subprocess.run(
        ["bash", str(script)],
        capture_output=True, text=True,
    )
    result.lint_exit_code = proc.returncode
    result.lint_output = proc.stdout + proc.stderr


def normalize_and_write(data: dict, data_p: Path):
    """Sort keys + sort records + pretty print + write atomically."""
    sorted_data = {k: data[k] for k in sorted(data.keys())}
    tmp = data_p.with_suffix(".json.tmp")
    tmp.write_text(
        json.dumps(sorted_data, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    tmp.replace(data_p)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="don't modify anything")
    ap.add_argument("--no-lint", action="store_true", help="skip stage 4 validation")
    ap.add_argument("--target", help="only scan this dir (instead of all ingestion_paths)")
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

    roots = [Path(args.target)] if args.target else ingestion_paths()
    result = DrainResult()

    # Stage 1
    candidates = stage_1_inventory(roots)
    print(f"Stage 1: {len(candidates)} candidate file(s) inventoried", file=sys.stderr)

    # Stage 1b: handle URL lists
    candidates = stage_1b_url_lists(candidates, result, data, args.dry_run)
    if result.url_lists_processed:
        print(f"Stage 1b: processed {len(result.url_lists_processed)} URL list(s)", file=sys.stderr)

    # Stages 2 + 3 combined
    stage_2_3_per_file(candidates, result, data, args.dry_run)
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

    # Print summary to stdout (this is the agent's input to stage 5)
    print(result.to_markdown())

    # Exit code reflects lint result
    if result.lint_exit_code and result.lint_exit_code != 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
