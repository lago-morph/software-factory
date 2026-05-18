#!/usr/bin/env bash
# Canonical normalizer for reference-only/sources.json.
#
# This is the SINGLE SOURCE OF TRUTH for what a normalized sources.json
# looks like on disk. Every catalog mutator — drain.py, the auto-regen
# workflow, hand-jq edits — must end by calling this script (or producing
# byte-identical output) so the file's shape never depends on which tool
# wrote it last.
#
# Output shape:
#   - All object keys sorted alphabetically at every level (jq -S).
#   - 2-space indent (jq default).
#   - UTF-8 preserved as-is (no \uXXXX escapes — jq's default for printable
#     non-ASCII; matches Python's `json.dumps(..., ensure_ascii=False)`).
#   - Arrays preserve their existing element order (jq does not reorder
#     arrays under -S).
#   - Trailing newline (jq appends one).
#
# Usage:
#   normalize-sources-json.sh [<path>]
#       Default <path>: reference-only/sources.json.
#       Edits the file in place atomically (jq output → temp → mv).
#       Exits 0 on success, non-zero if jq fails or the file is unparseable.
#
# Python equivalent (must produce byte-identical output):
#   json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
#
# Verification:
#   python -m pytest tests/unit/test_normalize_sources.py
set -euo pipefail

PATH_IN="${1:-reference-only/sources.json}"
if [ ! -f "$PATH_IN" ]; then
    echo "error: $PATH_IN does not exist" >&2
    exit 1
fi

TMP="${PATH_IN}.normalize.tmp"
trap 'rm -f "$TMP"' EXIT

jq -S '.' "$PATH_IN" > "$TMP"
mv "$TMP" "$PATH_IN"
