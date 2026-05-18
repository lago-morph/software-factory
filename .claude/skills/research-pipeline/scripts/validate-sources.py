"""Validate reference-only/sources.json — schema + structural invariants.

Schema validation uses the JSON Schema at reference-only/sources.schema.json.
Structural invariants (not expressible in JSON Schema):
    - Each record's id matches sha256(canonical_url)[:10] when canonical_url is set
    - Each record's id matches its parent map key
    - pointer_to references point to existing records
    - No circular pointer_to chains
    - No record points to itself
    - file.filename basename pattern (no path components)
    - file.location override paths (if set) are repo-relative and the file exists
    - file.sha256 matches actual file content when file is on disk and status=have
    - Top-level JSON is sorted by id (deterministic ordering for clean diffs)

Errors print with record id and field name (never line numbers — the AI works by id).

Exit:
    0 = OK
    1 = errors
    2 = warnings only

Requirements:
    pip install jsonschema pyyaml
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _config import (  # noqa: E402
    data_path, schema_path, repo_root, library_path, ConfigError,
)
from url_canonicalize import compute_id, canonicalize_url  # noqa: E402

try:
    from jsonschema import Draft202012Validator
except ImportError as e:
    raise SystemExit("jsonschema not installed: pip install jsonschema") from e


def main() -> int:
    try:
        data_p = data_path()
        schema_p = schema_path()
    except ConfigError as e:
        print(f"✗ Config error: {e}", file=sys.stderr)
        return 1

    if not data_p.exists():
        print(f"✗ {data_p} does not exist", file=sys.stderr)
        return 1
    if not schema_p.exists():
        print(f"✗ {schema_p} does not exist", file=sys.stderr)
        return 1

    try:
        data = json.loads(data_p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"✗ JSON parse error in {data_p}: {e}", file=sys.stderr)
        return 1

    try:
        schema = json.loads(schema_p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"✗ JSON parse error in {schema_p}: {e}", file=sys.stderr)
        return 1

    errors: list[str] = []
    warnings: list[str] = []

    # 1. JSON Schema validation
    validator = Draft202012Validator(schema)
    for err in validator.iter_errors(data):
        path = "/".join(str(p) for p in err.absolute_path)
        errors.append(f"schema: {path or '<root>'}: {err.message}")

    if not isinstance(data, dict):
        print(f"✗ Top-level must be an object (map of id -> record), got {type(data).__name__}", file=sys.stderr)
        return 1

    # 2. Top-level key ordering check (for clean diffs)
    keys = list(data.keys())
    if keys != sorted(keys):
        warnings.append(
            "Top-level keys are not sorted alphabetically. "
            "Run: bash .claude/skills/research-pipeline/scripts/normalize-sources-json.sh "
            "reference-only/sources.json to fix."
        )

    # 3. Per-record structural checks
    seen_ids: set[str] = set()
    for record_id, record in data.items():
        if not isinstance(record, dict):
            errors.append(f"{record_id}: record must be an object")
            continue

        # id matches map key
        rec_id_field = record.get("id")
        if rec_id_field != record_id:
            errors.append(
                f"{record_id}: record.id={rec_id_field!r} doesn't match map key {record_id!r}"
            )

        # id matches sha256(canonical_url)[:10] when canonical_url is set
        canonical_url = record.get("canonical_url")
        if canonical_url:
            try:
                expected_id = compute_id(canonical_url)
            except ValueError as e:
                errors.append(f"{record_id}: canonical_url invalid: {e}")
            else:
                if expected_id != record_id:
                    errors.append(
                        f"{record_id}: id doesn't match sha256(canonical_url)[:10]={expected_id}; "
                        f"either correct the id or correct the canonical_url"
                    )
                # canonical_url must also be in canonical form
                try:
                    canon = canonicalize_url(canonical_url)
                    if canon != canonical_url:
                        warnings.append(
                            f"{record_id}: canonical_url is not in canonical form; "
                            f"got {canonical_url!r}, expected {canon!r}"
                        )
                except ValueError:
                    pass

        # Title required and not empty
        if not record.get("title"):
            errors.append(f"{record_id}: title is required and must be non-empty")

        # pointer_to checks (done in a second pass once seen_ids is built)
        seen_ids.add(record_id)

    # 4. Pointer integrity (second pass)
    for record_id, record in data.items():
        if not isinstance(record, dict):
            continue
        pointer = record.get("pointer_to")
        if pointer is None:
            continue
        if pointer == record_id:
            errors.append(f"{record_id}: pointer_to points to itself")
            continue
        if pointer not in seen_ids:
            errors.append(f"{record_id}: pointer_to={pointer!r} doesn't exist as a record")
            continue
        # Detect circular chains
        visited = {record_id}
        current = pointer
        while current and current in data:
            if current in visited:
                errors.append(
                    f"{record_id}: pointer_to chain is circular (involves {current!r})"
                )
                break
            visited.add(current)
            current = data[current].get("pointer_to")

    # 5. File entry checks
    root = repo_root()
    lib = library_path()
    for record_id, record in data.items():
        if not isinstance(record, dict):
            continue
        files = record.get("files", [])
        if not isinstance(files, list):
            continue
        for i, f in enumerate(files):
            if not isinstance(f, dict):
                continue
            status = f.get("ingestion_status")
            filename = f.get("filename")
            location = f.get("location")

            # filename should be basename only
            if filename and ("/" in filename or "\\" in filename):
                errors.append(
                    f"{record_id} files[{i}]: filename {filename!r} contains path separator; use basename only "
                    f"(or use 'location' override for paths outside reference-only/<id>/)"
                )

            # Resolve actual disk path
            if location:
                abs_path = root / location
            elif filename:
                abs_path = lib / record_id / filename
            else:
                abs_path = None

            if status == "have":
                if abs_path is None:
                    errors.append(
                        f"{record_id} files[{i}]: ingestion_status=have but no filename or location set"
                    )
                elif not abs_path.exists():
                    rel = abs_path.relative_to(root) if abs_path.is_absolute() and str(abs_path).startswith(str(root)) else abs_path
                    errors.append(
                        f"{record_id} files[{i}]: ingestion_status=have but file not on disk at {rel}"
                    )
                elif f.get("sha256"):
                    actual = hashlib.sha256(abs_path.read_bytes()).hexdigest()
                    if actual != f["sha256"]:
                        errors.append(
                            f"{record_id} files[{i}]: sha256 mismatch (recorded={f['sha256'][:12]}..., actual={actual[:12]}...)"
                        )

    # Report
    for e in errors:
        print(f"✗ {e}", file=sys.stderr)
    for w in warnings:
        print(f"⚠ {w}", file=sys.stderr)

    n_records = sum(1 for v in data.values() if isinstance(v, dict))
    if errors:
        print(f"\n{n_records} record(s) checked; {len(errors)} error(s), {len(warnings)} warning(s)", file=sys.stderr)
        return 1
    if warnings:
        print(f"\n✓ {n_records} record(s) valid ({len(warnings)} warning(s))")
        return 2
    print(f"✓ {n_records} record(s) valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
