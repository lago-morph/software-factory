#!/usr/bin/env bash
# Run all source-catalog linters in order. Exit non-zero if any fail.
# Always run this before staging changes to sources.json.

set -uo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"

fail=0

run() {
    local label="$1"; shift
    echo "=== $label ==="
    if ! "$@"; then
        echo "FAIL: $label" >&2
        fail=1
    fi
    echo ""
}

run "config validation"     python3 "$HERE/validate-config.py"
run "schema + structural"   python3 "$HERE/validate-sources.py"
run "filesystem ↔ catalog"  python3 "$HERE/check-source-dirs.py"
run "URL ↔ reports"         python3 "$HERE/check-source-refs.py"
run "fetch_provenance"      python3 "$HERE/check-fetch-provenance.py"
run "sanity (warnings)"     python3 "$HERE/sanity-check-record.py"

if [ $fail -ne 0 ]; then
    echo "✗ lint failed"
    exit 1
fi
echo "✓ all checks passed"
exit 0
