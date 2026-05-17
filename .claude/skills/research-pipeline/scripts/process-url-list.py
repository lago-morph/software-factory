"""Process a URL-list text file into the catalog as wanted records.

Reads a .txt or .md file whose content is just URLs (one per line, blank lines
and # comments allowed). For each URL not already in the catalog, creates a
minimal record with canonical_url + computed id + title='(unknown)' and no files.

Usage:
    python process-url-list.py <path> [--delete-after]
        Reads the file, updates sources.json, optionally deletes the input file.

The catalog update is atomic: full jq transform piped to a temp file, then mv.
Re-runnable: existing IDs are no-ops.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _config import data_path, ConfigError  # noqa: E402
from classify_text import classify  # noqa: E402
from url_canonicalize import canonicalize_and_id  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("path", help="text file containing URL list (one per line)")
    ap.add_argument("--delete-after", action="store_true",
                    help="delete the input file after successful processing")
    ap.add_argument("--dry-run", action="store_true",
                    help="print what would be added without modifying sources.json")
    args = ap.parse_args()

    input_path = Path(args.path)
    if not input_path.exists():
        print(f"✗ {input_path} does not exist", file=sys.stderr)
        return 1

    try:
        data_p = data_path()
    except ConfigError as e:
        print(f"✗ Config error: {e}", file=sys.stderr)
        return 1

    text = input_path.read_text(encoding="utf-8", errors="replace")
    classification = classify(text)
    if classification["kind"] != "url_list":
        print(
            f"✗ {input_path} is not a pure URL list (kind={classification['kind']}).",
            file=sys.stderr,
        )
        if classification["kind"] in {"source_with_first_url", "source_with_header_url"}:
            print(
                f"  This looks like a content file with an embedded URL ({classification['extracted_url']}).\n"
                "  Use the drain pipeline (stage 1) to ingest it instead.",
                file=sys.stderr,
            )
        elif classification["kind"] == "mixed_error":
            print(
                "  Mixed content (some URLs, some not). Disambiguate before processing.",
                file=sys.stderr,
            )
        return 1

    if not data_p.exists():
        print(f"✗ {data_p} does not exist", file=sys.stderr)
        return 1
    try:
        data = json.loads(data_p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"✗ JSON parse error: {e}", file=sys.stderr)
        return 1

    added = []
    already_present = []
    failed = []
    for raw_url in classification["urls"]:
        try:
            canon, rid = canonicalize_and_id(raw_url)
        except ValueError as e:
            failed.append((raw_url, str(e)))
            continue
        if rid in data:
            already_present.append((raw_url, rid))
            continue
        new_record = {
            "id": rid,
            "canonical_url": canon,
            "title": "(unknown)",
            "files": [],
        }
        if canon != raw_url.strip():
            new_record["original_url"] = raw_url.strip()
        data[rid] = new_record
        added.append((raw_url, rid))

    # Sort + write
    sorted_data = {k: data[k] for k in sorted(data.keys())}

    if args.dry_run:
        print(f"Would add {len(added)} record(s):")
        for u, rid in added:
            print(f"  {rid}  {u}")
        if already_present:
            print(f"Already present: {len(already_present)}")
        if failed:
            print(f"Failed to parse: {len(failed)}")
            for u, err in failed:
                print(f"  {u}: {err}")
        return 0

    if added:
        tmp = data_p.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(sorted_data, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
        tmp.replace(data_p)

    # Report
    print(f"✓ Added {len(added)} new record(s)")
    for u, rid in added:
        print(f"  + {rid}  {u}")
    if already_present:
        print(f"  ({len(already_present)} already in catalog)")
    if failed:
        print(f"  ✗ {len(failed)} URL(s) failed to parse:", file=sys.stderr)
        for u, err in failed:
            print(f"    {u}: {err}", file=sys.stderr)

    if args.delete_after and not failed:
        input_path.unlink()
        print(f"  deleted: {input_path}")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
