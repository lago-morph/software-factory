"""Reconcile a reference-only/<id>/ directory against its catalog record.

For a given record id (or all records if --all), scan the corresponding
reference-only/<id>/ directory and add any files on disk that aren't already
in record.files[].

For each new file:
    - Compute sha256
    - Detect format from extension
    - Try URL extraction (best-effort; not required since directory placement
      already proves the file belongs to this source)
    - If URL extracted, check that it matches the record's canonical_url; if
      not, add the file but include a comment noting the mismatch (warning only)
    - Add file entry with ingestion_status=have, completeness=unknown
    - For images, set comment="(image — pending summary)" so the drain knows
      to generate a summary in the next pass

Usage:
    python reconcile-source-dir.py <id>           # reconcile one record
    python reconcile-source-dir.py --all          # reconcile every record
    python reconcile-source-dir.py <id> --dry-run # preview without changes
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _config import data_path, library_path, ConfigError  # noqa: E402
from extract_url import extract_url  # noqa: E402
from url_canonicalize import canonicalize_url  # noqa: E402

ID_RE = re.compile(r"^[0-9a-f]{10}$")

FORMAT_BY_EXT = {
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
    ".yaml": "yaml", ".yml": "yaml",
    ".csv": "csv",
    ".zip": "zip",
}

IMAGE_FORMATS = {"image/png", "image/jpeg", "image/svg+xml", "image/gif", "image/webp"}


def reconcile_one(record_id: str, data: dict, lib: Path, dry_run: bool) -> tuple[int, list[str]]:
    """Returns (n_added, warnings)."""
    if record_id not in data:
        return 0, [f"{record_id}: no such record"]
    record = data[record_id]
    if not isinstance(record, dict):
        return 0, [f"{record_id}: record is not an object"]

    dir_path = lib / record_id
    if not dir_path.exists():
        return 0, []  # no directory to reconcile

    existing_files = record.get("files", [])
    if not isinstance(existing_files, list):
        existing_files = []
    existing_filenames = {
        f.get("filename") for f in existing_files
        if isinstance(f, dict) and f.get("filename") and not f.get("location")
    }

    record_url = record.get("canonical_url")
    record_url_canon = None
    if record_url:
        try:
            record_url_canon = canonicalize_url(record_url)
        except ValueError:
            pass
    record_host = _host(record_url_canon) if record_url_canon else None

    warnings: list[str] = []
    n_added = 0

    for f in sorted(dir_path.iterdir()):
        if not f.is_file():
            continue
        if f.name in existing_filenames:
            continue
        if f.name.startswith(".") or f.name in {"README.md"}:
            continue

        fmt = FORMAT_BY_EXT.get(f.suffix.lower(), "other")
        sha = hashlib.sha256(f.read_bytes()).hexdigest()

        # Best-effort URL extraction. Not required to succeed for files in known dir.
        extracted = extract_url(f)
        comment_parts = []
        if extracted and record_host:
            try:
                extracted_canon = canonicalize_url(extracted)
                extracted_host = _host(extracted_canon)
                if extracted_host and extracted_host != record_host:
                    msg = (
                        f"URL mismatch: file extracts as {extracted_host}, "
                        f"record canonical is {record_host}"
                    )
                    comment_parts.append(msg)
                    warnings.append(f"{record_id}/{f.name}: {msg}")
            except ValueError:
                pass

        if fmt in IMAGE_FORMATS:
            comment_parts.append("(image — pending summary)")

        entry = {
            "format": fmt,
            "filename": f.name,
            "sha256": sha,
            "ingestion_status": "have",
            "completeness": "unknown",
        }
        if comment_parts:
            entry["comment"] = " ".join(comment_parts)

        existing_files.append(entry)
        n_added += 1
        if dry_run:
            print(f"  + would add: {record_id}/{f.name}  [{fmt}]")
        else:
            print(f"  + added:     {record_id}/{f.name}  [{fmt}]")

    record["files"] = existing_files
    return n_added, warnings


def _host(url: str | None) -> str | None:
    if not url:
        return None
    m = re.match(r"https?://([^/]+)", url)
    return m.group(1).lower() if m else None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*", help="record IDs to reconcile (default: see --all)")
    ap.add_argument("--all", action="store_true", help="reconcile every record")
    ap.add_argument("--dry-run", action="store_true", help="preview without changes")
    args = ap.parse_args()

    if not args.ids and not args.all:
        ap.error("specify record id(s) or --all")

    try:
        data_p = data_path()
        lib = library_path()
    except ConfigError as e:
        print(f"✗ Config error: {e}", file=sys.stderr)
        return 1

    if not data_p.exists():
        print(f"✗ {data_p} does not exist", file=sys.stderr)
        return 1
    try:
        data = json.loads(data_p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"✗ JSON parse error: {e}", file=sys.stderr)
        return 1

    if args.all:
        target_ids = [k for k in data.keys() if ID_RE.match(k)]
    else:
        target_ids = args.ids

    total_added = 0
    all_warnings: list[str] = []
    for rid in target_ids:
        n, ws = reconcile_one(rid, data, lib, args.dry_run)
        total_added += n
        all_warnings.extend(ws)

    if not args.dry_run and total_added > 0:
        sorted_data = {k: data[k] for k in sorted(data.keys())}
        tmp = data_p.with_suffix(".json.tmp")
        tmp.write_text(
            json.dumps(sorted_data, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        tmp.replace(data_p)

    for w in all_warnings:
        print(f"⚠ {w}")

    print(f"\n{'(dry run) ' if args.dry_run else ''}{total_added} file(s) added across {len(target_ids)} record(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
