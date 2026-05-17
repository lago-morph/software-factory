"""Cross-check filesystem against catalog.

Two-way diff between `reference-only/<id>/<files>` on disk and `record.files[]` in
the catalog:

    - Files on disk under reference-only/<id>/ NOT in record's files[] → "not registered"
    - record.files[] entries with ingestion_status=have but no file on disk → "missing on disk"
    - Top-level files/dirs under reference-only/ that aren't valid 10-hex-char ids
      (and aren't recognized catalog control files) → "stray"

Legacy directories under reference-only/ that aren't id-shaped (e.g., the
existing `anthropic-agent-skills/`, `lenny-podcast-transcripts/`, `el-kaim-book/`
sub-trees) are tolerated — they were established before the per-id convention.
A `file.location` override on a record file entry will silence the orphan check
for that file even if it lives in a legacy path.

Exit:
    0 = clean
    1 = errors
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _config import data_path, library_path, repo_root, ConfigError  # noqa: E402

ID_RE = re.compile(r"^[0-9a-f]{10}$")
CONTROL_FILES = {
    "sources.json",
    "sources.schema.json",
    "sources.md",
    ".regen-trigger",
    "README.md",      # convention; may exist
}


def main() -> int:
    try:
        data_p = data_path()
        lib = library_path()
    except ConfigError as e:
        print(f"✗ Config error: {e}", file=sys.stderr)
        return 1

    if not data_p.exists():
        print(f"✗ {data_p} does not exist", file=sys.stderr)
        return 1
    if not lib.exists():
        print(f"✗ {lib} does not exist", file=sys.stderr)
        return 1

    try:
        data = json.loads(data_p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"✗ JSON parse error: {e}", file=sys.stderr)
        return 1

    errors = []
    warnings = []
    root = repo_root()

    # Build the expected file map from the catalog: {id: set(filenames_or_paths)}
    expected: dict[str, set[Path]] = {}
    # Also track explicit location overrides — these may point anywhere
    override_paths: set[Path] = set()

    for record_id, record in data.items():
        if not isinstance(record, dict) or not ID_RE.match(record_id):
            continue
        files = record.get("files", []) or []
        for f in files:
            if not isinstance(f, dict):
                continue
            if f.get("ingestion_status") != "have":
                continue
            filename = f.get("filename")
            location = f.get("location")
            if location:
                p = (root / location).resolve()
                override_paths.add(p)
            elif filename:
                p = (lib / record_id / filename).resolve()
                expected.setdefault(record_id, set()).add(p)
                if not p.exists():
                    rel = p.relative_to(root) if str(p).startswith(str(root)) else p
                    errors.append(
                        f"{record_id}: file {filename!r} marked have but missing on disk at {rel}"
                    )

    # Walk reference-only top-level
    for entry in sorted(lib.iterdir()):
        name = entry.name
        if entry.is_file():
            if name in CONTROL_FILES or name.startswith("."):
                continue
            warnings.append(f"stray file at top of library: {entry.relative_to(root)}")
            continue
        # entry is a directory
        if not ID_RE.match(name):
            # Legacy directory — tolerated. Check that all its files are referenced by SOME record's
            # location override; otherwise just warn.
            referenced = 0
            unreferenced = 0
            for f in entry.rglob("*"):
                if not f.is_file():
                    continue
                if f.resolve() not in override_paths:
                    unreferenced += 1
                else:
                    referenced += 1
            if unreferenced:
                warnings.append(
                    f"legacy dir {entry.relative_to(root)}: "
                    f"{referenced} referenced, {unreferenced} unreferenced files"
                )
            continue
        # entry is a per-id directory
        record_id = name
        if record_id not in data:
            warnings.append(
                f"directory reference-only/{record_id}/ exists but no record with that id"
            )
            continue
        # Check every file in the dir is in the record's files[]
        record_expected = expected.get(record_id, set())
        for f in sorted(entry.iterdir()):
            if not f.is_file():
                continue
            if f.resolve() not in record_expected and f.resolve() not in override_paths:
                rel = f.relative_to(root)
                errors.append(
                    f"{record_id}: file on disk not in record's files[]: {rel}"
                )

    # Report
    for e in errors:
        print(f"✗ {e}", file=sys.stderr)
    for w in warnings:
        print(f"⚠ {w}", file=sys.stderr)

    if errors:
        print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)", file=sys.stderr)
        return 1
    if warnings:
        print(f"\n✓ filesystem matches catalog ({len(warnings)} warning(s))")
        return 0
    print("✓ filesystem matches catalog")
    return 0


if __name__ == "__main__":
    sys.exit(main())
