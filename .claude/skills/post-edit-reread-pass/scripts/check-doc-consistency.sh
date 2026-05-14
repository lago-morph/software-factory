#!/usr/bin/env bash
# check-doc-consistency.sh — drift candidate finder for long markdown docs.
#
# Runs a battery of greps for the common drift shapes documented in
# .claude/skills/post-edit-reread-pass/SKILL.md. Findings are ADVISORY:
# each candidate may or may not be actual drift. Review in context.
#
# The script never modifies the doc.
#
# Usage:
#   check-doc-consistency.sh <path-to-doc>
#   check-doc-consistency.sh <path-to-doc> --quiet      # suppress per-shape headers
#   check-doc-consistency.sh <path-to-doc> --shape=N    # run only shape N (1..7)
#
# Exit codes:
#   0  — completed (candidates may or may not have been found; the script
#        does not opine on whether a candidate is actual drift).
#   2  — usage error (missing file, file unreadable).

set -u

usage() {
    cat >&2 <<EOF
Usage: $0 <path-to-doc> [--quiet] [--shape=N]

Runs targeted greps to surface candidate drift in a long markdown doc.
Findings are advisory — each candidate should be reviewed in context.

Drift shapes (per SKILL.md):
  1  Count drift            — numeric framing that may have stale duplicates
  2  Status / state drift   — open/closed/pending qualifiers across sections
  3  Cross-section ref drift — "see §N" pointers that may have gone stale
  4  Stale qualifier drift  — "still pending", "TODO", aged in place
  5  Contradicted-by-newer  — claims that may conflict with newer artifacts
  6  Version-bump drift     — version refs that may be out of sync
  7  Aged-inventory drift   — file/issue/PR refs that may be stale
EOF
    exit 2
}

QUIET=0
ONLY_SHAPE=""
FILE=""

for arg in "$@"; do
    case "$arg" in
        --quiet) QUIET=1 ;;
        --shape=*) ONLY_SHAPE="${arg#--shape=}" ;;
        -h|--help) usage ;;
        -*) echo "unknown flag: $arg" >&2; usage ;;
        *) FILE="$arg" ;;
    esac
done

if [ -z "$FILE" ]; then
    usage
fi
if [ ! -r "$FILE" ]; then
    echo "cannot read: $FILE" >&2
    exit 2
fi

header() {
    if [ "$QUIET" -eq 0 ]; then
        echo
        echo "=== Shape $1: $2 ==="
    fi
}

run_shape() {
    local n="$1"
    shift
    if [ -n "$ONLY_SHAPE" ] && [ "$ONLY_SHAPE" != "$n" ]; then
        return
    fi
    "$@"
}

# Shape 1 — count drift
shape1() {
    header 1 "Count drift candidates (numeric framing)"
    # Spelled-out small numbers in prose. Common drift surface.
    grep -nE "\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\b" "$FILE" \
        | grep -viE "^\s*[0-9]+:.*\b(one|two|three|four|five|six|seven|eight|nine|ten)-(line|page|day|hour|week|column|row|step)\b" \
        || true
    echo
    # Digit-form counts with units. Each "N <item>" line is a candidate.
    grep -nE "\b[0-9]+ (item|items|rows?|entries|records?|files?|sources?|sections?|chapters?|reports?|tasks?|issues?|PRs?|skills?|suggestions?|comments?|days?|hours?|tests?|cases?|examples?|fields?|columns?|members?|users?|services?|hosts?|URLs?|links?)\b" "$FILE" \
        || true
}

# Shape 2 — status / state drift
shape2() {
    header 2 "Status / state markers (verify §1 snapshot agrees with detail)"
    grep -nE "✅|🟡|❌|⏳|🔴|🟢|🟠|🔵|⚪|⚫" "$FILE" || true
    echo
    grep -nE "\b(RESOLVED|PENDING|DONE|OPEN|CLOSED|BLOCKED|IN PROGRESS|TODO|WONT FIX|WON'T FIX|FIXED|DEFERRED)\b" "$FILE" || true
}

# Shape 3 — cross-section ref drift
shape3() {
    header 3 "Cross-section references (verify each target exists)"
    grep -nE "(see |See |refer to |Refer to |per |Per |in |In )?§[0-9A-Z]+(\.[0-9A-Z]+)*" "$FILE" || true
    echo
    grep -niE "section [0-9A-Z]+(\.[0-9A-Z]+)*" "$FILE" || true
}

# Shape 4 — stale qualifier drift
shape4() {
    header 4 "Stale qualifiers (verify the underlying state is still as described)"
    grep -nE "\b(still |currently |as of [0-9]{4}-[0-9]{2}-[0-9]{2}|pending|outstanding|in.flight|in-flight|to be |awaiting|queued|deferred)\b" "$FILE" || true
    echo
    # TBD / TODO / FIXME / NOTE markers
    grep -nE "\b(TBD|TODO|FIXME|XXX|HACK|NOTE:|N\.B\.)\b" "$FILE" || true
}

# Shape 5 — contradicted-by-newer-artifact drift
shape5() {
    header 5 "Out-of-scope / will-not / decided-against statements (verify no newer artifact reverses these)"
    grep -niE "(out of scope|not in scope|will not|won.t|deliberately not|explicitly not|deferred|skipped|decided against|rejected)" "$FILE" || true
}

# Shape 6 — version-bump bookkeeping drift
shape6() {
    header 6 "Version references (verify top-of-doc and history table agree)"
    grep -nE "\bv[0-9]+(\.[0-9]+)+(-[a-zA-Z0-9]+)?\b" "$FILE" || true
    echo
    grep -niE "(version[:\s]+[0-9]+(\.[0-9]+)+|version history|earlier versions?|previous versions?)" "$FILE" || true
}

# Shape 7 — aged-inventory drift
shape7() {
    header 7 "Inventory references (verify file/issue/PR refs are current)"
    # Issue / PR refs
    grep -nE "#[0-9]+" "$FILE" || true
    echo
    # File paths that may or may not still exist
    grep -nE "\`[a-zA-Z0-9._/-]+\.(md|py|js|ts|tsx|jsx|sh|yaml|yml|json|toml)\`" "$FILE" | head -50 || true
    echo
    # Commit-hash candidates
    grep -nE "\b[0-9a-f]{7,40}\b" "$FILE" | head -20 || true
}

run_shape "1" shape1
run_shape "2" shape2
run_shape "3" shape3
run_shape "4" shape4
run_shape "5" shape5
run_shape "6" shape6
run_shape "7" shape7

if [ "$QUIET" -eq 0 ]; then
    cat <<EOF

=== done ===
Findings are advisory. Each candidate is a place to verify against current
state — not necessarily a bug. Apply judgement.
EOF
fi
