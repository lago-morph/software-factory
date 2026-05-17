#!/usr/bin/env bash
# Render reference-only/sources.md from reference-only/sources.json using jq.
#
# Sections (auto-derived from each record's state):
#   §1 Complete            — every file have+complete
#   §2 Partial             — has some have files, some want/partial/error
#   §3a Wanted (URL known) — no have files; canonical_url is set
#   §3b Wanted (title only) — no have files; no canonical_url (search hints only)
#   §4 Superseded          — pointer_to is non-null
#
# Within each section, records are sorted by lowercase title.
#
# Per-record output (the "less detail" view):
#   ### <id> — <title> <a id="<id>"></a>
#   <canonical_url>
#   *<short_summary>*
#   - **Files:** <comma-separated format ✓ / format (want) list>
#   - **Tags:** <tags>
#   - **Cited in:** <reports count>
#   - **Diagrams:** yes/no/unknown
#
# Stdout is the rendered markdown.

set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../../../.." && pwd)"
DATA="$ROOT/reference-only/sources.json"

if [ ! -f "$DATA" ]; then
    echo "ERROR: $DATA not found" >&2
    exit 1
fi

# Categorize each record into a section
JQ_CATEGORIZE='
def status(r):
  if (r.pointer_to // null) != null then "superseded"
  else
    (r.files // []) as $files
    | ([$files[] | select(.ingestion_status == "have")] | length) as $n_have
    | ([$files[] | select(.ingestion_status == "want")] | length) as $n_want
    | ([$files[] | select(.completeness == "partial" or .completeness == "error")] | length) as $n_problem
    | if $n_have == 0 then
        if (r.canonical_url // null) != null then "wanted_url" else "wanted_title" end
      elif $n_want > 0 or $n_problem > 0 then
        "partial"
      else "complete"
      end
  end;

to_entries
| map(.value.id = .key | .value._section = status(.value) | .value)
'

# Render one record as markdown
JQ_RENDER_RECORD='
def section_anchor: "<a id=\"\(.id)\"></a>";
def header: "### \(.id) — \(.title) " + section_anchor;
def url_line: if .canonical_url then "<\(.canonical_url)>" else "*(no URL set)*" end;
def short: if .short_summary then "*\(.short_summary)*" else "" end;
def file_chip(f):
  (f.format // "?") as $fmt
  | if f.ingestion_status == "have" then "\($fmt) ✓"
    elif f.ingestion_status == "want" then "\($fmt) (want)"
    elif f.ingestion_status == "skip-not-necessary" then "\($fmt) (skip)"
    else "\($fmt) (?)" end;
def files_line:
  if (.files // [] | length) > 0 then
    "- **Files:** " + ([.files[] | file_chip(.)] | join(" · "))
  else
    "- **Files:** *(none registered)*"
  end;
def tags_line:
  if (.tags // [] | length) > 0 then
    "- **Tags:** " + ([.tags[] | "`\(.)`"] | join(" · "))
  else "" end;
def refs_line:
  if (.references_from // [] | length) > 0 then
    "- **Cited in:** " + ([.references_from[] | "`\(.)`"] | join(" · ")) + " *(\(.references_from | length))*"
  else "" end;
def diag_line:
  if .has_useful_diagrams then "- **Diagrams:** \(.has_useful_diagrams)" else "" end;
def superseded_stub:
  "### \(.id) ~~\(.title)~~ → see [\(.pointer_to)](#\(.pointer_to))";

if .pointer_to then
  superseded_stub
else
  [
    header,
    "",
    url_line,
    "",
    short,
    "",
    files_line,
    tags_line,
    refs_line,
    diag_line
  ] | map(select(. != "")) | join("\n")
end
'

# Build the full document
{
    cat <<'HEADER'
# Source catalog — browse view

Auto-generated from `reference-only/sources.json` by `scripts/render-sources-md.sh`.
Do not edit by hand — your changes will be overwritten on next push to `main`.

To edit a source, use `jq` on `sources.json` and let the GitHub Action regenerate this file.
To find the full record for any source, search this file for the 10-char id, then
`jq '.["<id>"]' reference-only/sources.json`.

HEADER

    for section in complete partial wanted_url wanted_title superseded; do
        case "$section" in
            complete)      title="§ 1 — Complete";  blurb="Every registered file is present and complete." ;;
            partial)       title="§ 2 — Partial";   blurb="Has some content, but also files that are wanted, partial, or had fetch errors." ;;
            wanted_url)    title="§ 3a — Wanted (URL known)"; blurb="URL is known but no content acquired yet." ;;
            wanted_title)  title="§ 3b — Wanted (title only)"; blurb="Title + search hints only; no URL yet." ;;
            superseded)    title="§ 4 — Superseded"; blurb="Records replaced by another; pointer_to is set." ;;
        esac

        # Extract records for this section
        records=$(jq -r --arg section "$section" "
            $JQ_CATEGORIZE
            | map(select(._section == \$section))
            | sort_by(.title | ascii_downcase)
            | .[] | (. | del(._section)) | (
                $JQ_RENDER_RECORD
              )
            | . + \"\n\"
        " "$DATA" 2>/dev/null || echo "")

        count=$(jq -r --arg section "$section" "
            $JQ_CATEGORIZE
            | map(select(._section == \$section))
            | length
        " "$DATA")

        printf "## %s *(%s records)*\n\n" "$title" "$count"
        printf "*%s*\n\n" "$blurb"

        if [ -n "$records" ]; then
            printf "%s\n" "$records"
        else
            printf "*(none)*\n\n"
        fi
    done

    # Footer
    printf -- "---\n\n"
    printf "*Generated %s*\n" "$(date -u +'%Y-%m-%d %H:%M:%S UTC')"
}
