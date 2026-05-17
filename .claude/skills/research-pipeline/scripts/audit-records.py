"""Record-scoped mechanical audit.

Unlike `lint-sources.sh` (which validates the entire catalog and is run pre-commit),
this script audits a specific set of records — typically the ones drain.py just
touched — and reports issues that *should have been caught at ingestion time*.

The point of failures here is **forward-thinking**: every issue surfaced is a hint
that drain.py is missing a step. When you add a new check, also update drain.py
to produce records that satisfy it. The audit grows over time as we discover edge
cases; drain.py grows in lockstep so the audit always passes on fresh ingestions.

Checks (per record):
  1. title-not-placeholder      — title is set and != "(unknown)".
  2. has-canonical-url          — canonical_url is non-null and well-formed.
  3. url-is-canonical           — canonicalize(canonical_url) == canonical_url.
  4. id-derivation              — record.id == sha256(canonical_url)[:10].
  5. has-files                  — files[] has at least one entry (have OR want OR skip).
  6. file-on-disk               — every have-file exists at expected path.
  7. file-sha256-matches        — every have-file's recorded sha256 matches disk.
  8. format-matches-extension   — files[].format matches filename's extension.
  9. has-category-tag           — at least one tag from the 15 canonical categories.
 10. pointer-chain-ok           — pointer_to (if set) points to a non-pointer record.
 11. fetch-provenance-ok        — if fetch_provenance is set, status is non-null.
 12. image-has-summary          — image files have a non-empty comment field.

Usage:
    python audit-records.py <id> [<id>...]   # audit specific record IDs
    python audit-records.py --all            # audit every record
    python audit-records.py --json           # emit JSON instead of text

Exit codes:
    0 = all audited records clean
    1 = one or more findings
    2 = could not load catalog
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _config import (  # noqa: E402
    data_path, library_path, repo_root, skill_md_path, ConfigError,
)
from url_canonicalize import canonicalize_url, compute_id  # noqa: E402


# Keep in sync with render-sources-md.py CATEGORY_ORDER. When categories.json
# gets built as a single source of truth (deferred follow-up), this list is
# replaced by `from _categories import category_tags`.
CANONICAL_CATEGORY_TAGS = frozenset({
    "dark-factory",
    "intent-driven-architecture",
    "spec-authorship",
    "willison-canon",
    "compound-engineering",
    "anthropic-substrate",
    "openai-substrate",
    "other-vendor-substrate",
    "skills-composition",
    "evals-and-benchmarks",
    "academic-foundations",
    "security-primitives",
    "governance-and-legal",
    "ai-engineering-culture",
    "meta-synthesis",
})

# Map record file.format → expected extensions (lowercase, leading dot).
FORMAT_EXT = {
    "html": {".html", ".htm"},
    "mhtml": {".mhtml"},
    "md": {".md"},
    "txt": {".txt"},
    "pdf": {".pdf"},
    "ipynb": {".ipynb"},
    "image/png": {".png"},
    "image/jpeg": {".jpg", ".jpeg"},
    "image/svg+xml": {".svg"},
    "image/gif": {".gif"},
    "image/webp": {".webp"},
    "json": {".json"},
    "yaml": {".yaml", ".yml"},
    "csv": {".csv"},
    "zip": {".zip"},
    "bibtex": {".bib"},
}

IMAGE_FORMATS = {
    "image/png", "image/jpeg", "image/svg+xml", "image/gif", "image/webp",
}


class Finding:
    __slots__ = ("record_id", "check", "message")

    def __init__(self, record_id: str, check: str, message: str):
        self.record_id = record_id
        self.check = check
        self.message = message

    def to_dict(self) -> dict:
        return {"record_id": self.record_id, "check": self.check, "message": self.message}

    def __str__(self) -> str:
        return f"✗ {self.record_id} [{self.check}] {self.message}"


def _record_path(record_id: str, f: dict, lib: Path, root: Path) -> Path | None:
    """Resolve the disk path for a file entry, or None if it has neither
    filename nor location."""
    location = f.get("location")
    if location:
        return root / location
    filename = f.get("filename")
    if filename:
        return lib / record_id / filename
    return None


def audit_record(record_id: str, record: dict, data: dict, lib: Path,
                 root: Path) -> list[Finding]:
    """Run all checks for one record and return any findings."""
    findings: list[Finding] = []

    # A superseded record gets a narrower audit — its pointer_to says
    # "real data lives elsewhere", so we don't insist on title etc.
    is_pointer = bool(record.get("pointer_to"))

    # 10. pointer-chain-ok (also applies to non-pointer records implicitly: no chain)
    if is_pointer:
        target_id = record["pointer_to"]
        target = data.get(target_id)
        if not isinstance(target, dict):
            findings.append(Finding(record_id, "pointer-chain-ok",
                f"pointer_to={target_id!r} does not exist"))
        elif target.get("pointer_to"):
            findings.append(Finding(record_id, "pointer-chain-ok",
                f"pointer_to={target_id!r} is itself a pointer (chain > 1 hop)"))
        # For pointer records, skip the rest — they're stubs by design.
        return findings

    # 1. title-not-placeholder
    title = (record.get("title") or "").strip()
    if not title or title == "(unknown)":
        findings.append(Finding(record_id, "title-not-placeholder",
            f"title is {title!r}; extract from file content or set manually"))

    # 2. has-canonical-url
    canonical_url = record.get("canonical_url")
    if not canonical_url:
        # Records can legitimately exist with only search_hints (title-only
        # discovery). Don't flag if search_hints is populated.
        if not record.get("search_hints"):
            findings.append(Finding(record_id, "has-canonical-url",
                "canonical_url is null and no search_hints set"))
    else:
        # 3. url-is-canonical
        try:
            canon = canonicalize_url(canonical_url)
        except ValueError as e:
            findings.append(Finding(record_id, "url-is-canonical",
                f"canonicalize raised: {e}"))
        else:
            if canon != canonical_url:
                findings.append(Finding(record_id, "url-is-canonical",
                    f"not in canonical form; got {canonical_url!r}, expected {canon!r}"))
            # 4. id-derivation
            try:
                expected_id = compute_id(canonical_url)
            except ValueError:
                pass
            else:
                if expected_id != record_id:
                    findings.append(Finding(record_id, "id-derivation",
                        f"id should be {expected_id} (sha256(canonical_url)[:10])"))

    # 9. has-category-tag
    tags = record.get("tags") or []
    if not any(t in CANONICAL_CATEGORY_TAGS for t in tags):
        findings.append(Finding(record_id, "has-category-tag",
            "no tag from the 15 canonical categories "
            "(see resources/_catalog/category-taxonomy.md)"))

    # 5. has-files
    files = record.get("files") or []
    if not files:
        findings.append(Finding(record_id, "has-files",
            "files[] is empty; add 'want' or 'have' entries"))

    # 6 + 7 + 8 + 12: per-file checks
    for i, f in enumerate(files):
        if not isinstance(f, dict):
            continue
        status = f.get("ingestion_status")
        fmt = f.get("format")
        filename = f.get("filename")

        # 8. format-matches-extension
        if fmt in FORMAT_EXT and filename:
            ext = Path(filename).suffix.lower()
            if ext and ext not in FORMAT_EXT[fmt]:
                findings.append(Finding(record_id, "format-matches-extension",
                    f"files[{i}] format={fmt!r} but filename={filename!r} "
                    f"(expected extension in {sorted(FORMAT_EXT[fmt])})"))

        if status != "have":
            continue

        # 6. file-on-disk
        abs_path = _record_path(record_id, f, lib, root)
        if abs_path is None:
            findings.append(Finding(record_id, "file-on-disk",
                f"files[{i}] status=have but no filename/location set"))
            continue
        if not abs_path.exists():
            try:
                rel = abs_path.relative_to(root)
            except ValueError:
                rel = abs_path
            findings.append(Finding(record_id, "file-on-disk",
                f"files[{i}] status=have but missing on disk at {rel}"))
            continue

        # 7. file-sha256-matches
        recorded_sha = f.get("sha256")
        if recorded_sha:
            try:
                actual = hashlib.sha256(abs_path.read_bytes()).hexdigest()
            except OSError as e:
                findings.append(Finding(record_id, "file-sha256-matches",
                    f"files[{i}] could not read {abs_path.name}: {e}"))
            else:
                if actual != recorded_sha:
                    findings.append(Finding(record_id, "file-sha256-matches",
                        f"files[{i}] {abs_path.name}: recorded={recorded_sha[:12]}…, "
                        f"actual={actual[:12]}… — re-compute and update"))

        # 12. image-has-summary
        if fmt in IMAGE_FORMATS:
            if not (f.get("comment") or "").strip():
                findings.append(Finding(record_id, "image-has-summary",
                    f"files[{i}] {filename or '<no-name>'} is an image but "
                    "comment is empty; populate with auto-summary"))

        # 11. fetch-provenance-ok
        fp = f.get("fetch_provenance")
        if isinstance(fp, dict):
            if fp.get("status") is None:
                findings.append(Finding(record_id, "fetch-provenance-ok",
                    f"files[{i}] fetch_provenance set but status is null"))

    return findings


def emit_text(findings: list[Finding], target_ids: list[str], always_mode: bool,
              skill_md: Path) -> None:
    """Human-readable report. Prints to stdout."""
    for f in findings:
        print(str(f))

    n = len(findings)
    n_records = len(target_ids)
    if n == 0:
        print(f"✓ audit clean — {n_records} record(s) checked, no findings")
    else:
        # Group by check for the user
        by_check: dict[str, int] = {}
        for f in findings:
            by_check[f.check] = by_check.get(f.check, 0) + 1
        print(f"\n{n} finding(s) across {n_records} record(s):")
        for check, count in sorted(by_check.items(), key=lambda kv: -kv[1]):
            print(f"  - {check}: {count}")
        print(
            "\nNext step: for each finding, either fix the record OR — if the "
            "issue points to a gap in the drain pipeline — extend drain.py to "
            "produce records that satisfy the check."
        )

    if always_mode:
        try:
            rel = skill_md.relative_to(Path.cwd())
        except ValueError:
            rel = skill_md
        print(
            f"\nℹ audit ran because `audit_after_ingestion: always` is set. "
            f"Configure in {rel} (search for `audit_after_ingestion`)."
        )


def emit_json(findings: list[Finding]) -> None:
    print(json.dumps([f.to_dict() for f in findings], indent=2, sort_keys=True))


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("ids", nargs="*", help="record IDs to audit")
    ap.add_argument("--all", action="store_true", help="audit every record")
    ap.add_argument("--json", action="store_true", help="emit JSON output")
    ap.add_argument("--always-mode-footer", action="store_true",
                    help="append the user-facing 'configured in …' footer "
                         "(drain.py sets this when audit_after_ingestion=always)")
    args = ap.parse_args(argv[1:])

    try:
        data_p = data_path()
        lib = library_path()
        skill_md = skill_md_path()
    except ConfigError as e:
        print(f"✗ config error: {e}", file=sys.stderr)
        return 2

    if not data_p.exists():
        print(f"✗ {data_p} does not exist", file=sys.stderr)
        return 2

    try:
        data = json.loads(data_p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"✗ JSON parse error: {e}", file=sys.stderr)
        return 2

    if args.all:
        target_ids = sorted(data.keys())
    else:
        target_ids = args.ids
        if not target_ids:
            print("usage: audit-records.py <id>... | --all", file=sys.stderr)
            return 2

    root = repo_root()
    id_re = re.compile(r"^[0-9a-f]{10}$")
    findings: list[Finding] = []
    for rid in target_ids:
        if not id_re.match(rid):
            print(f"✗ {rid}: not a valid 10-hex id", file=sys.stderr)
            return 2
        record = data.get(rid)
        if not isinstance(record, dict):
            print(f"✗ {rid}: no such record", file=sys.stderr)
            return 2
        findings.extend(audit_record(rid, record, data, lib, root))

    if args.json:
        emit_json(findings)
    else:
        emit_text(findings, target_ids, args.always_mode_footer, skill_md)

    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
