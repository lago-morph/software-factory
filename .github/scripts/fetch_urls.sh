#!/usr/bin/env bash
# Fetch each URL in .fetch-work/urls.txt and save under
# research/fetched/issue-<N>/. Produces both:
#   - <slug>.html : raw response body
#   - <slug>.md   : html2text conversion (best-effort)
# Plus a summary.md written to .fetch-work/summary.md for the issue comment.
#
# Failures are tolerated per-URL; the script exits 0 unless something
# pathological happens (e.g. urls.txt missing).
set -euo pipefail

ISSUE_NUMBER="${ISSUE_NUMBER:?ISSUE_NUMBER not set}"
OUT_DIR="research/fetched/issue-${ISSUE_NUMBER}"
WORK_DIR=".fetch-work"
URLS_FILE="${WORK_DIR}/urls.txt"
SUMMARY="${WORK_DIR}/summary.md"

if [ ! -s "$URLS_FILE" ]; then
  echo "No URLs file or empty; nothing to do." >&2
  exit 0
fi

mkdir -p "$OUT_DIR"
: > "$SUMMARY"

ua="Mozilla/5.0 (compatible; software-factory-fetch/1.0; +https://github.com/lago-morph/software-factory)"

# Generate a short, filesystem-safe slug from a URL. We do not use the URL's
# path directly because Windows-unsafe characters and length limits make that
# fragile. Slug = sha1(url)[:10] + "_" + sanitized-host-and-tail.
slug_for() {
  local url="$1"
  local sha
  sha=$(printf "%s" "$url" | sha1sum | cut -c1-10)
  local tail
  tail=$(printf "%s" "$url" \
    | sed -E 's|^https?://||; s|[^A-Za-z0-9._/-]|_|g; s|/+|__|g' \
    | cut -c1-80)
  printf "%s_%s" "$sha" "$tail"
}

i=0
while IFS= read -r url; do
  [ -z "$url" ] && continue
  i=$((i+1))
  slug=$(slug_for "$url")
  html_path="${OUT_DIR}/${slug}.html"
  md_path="${OUT_DIR}/${slug}.md"

  echo "[$i] Fetching: $url" >&2

  # Capture HTTP status + final URL for the summary. --max-time bounds the
  # whole exchange. -L follows redirects. -k tolerates broken TLS chains we
  # don't care about for research material. -A sets a user agent so domains
  # that 403 the default curl UA may relent.
  http_code=$(
    curl --silent --show-error --location --insecure \
      --max-time 30 \
      --user-agent "$ua" \
      --output "$html_path" \
      --write-out "%{http_code}" \
      "$url" 2> "${WORK_DIR}/${slug}.err" || true
  )

  bytes=0
  if [ -f "$html_path" ]; then
    bytes=$(wc -c < "$html_path" | tr -d ' ')
  fi

  if [ "${http_code:-000}" = "200" ] && [ "$bytes" -gt 0 ]; then
    if python3 -c "import html2text" 2>/dev/null; then
      python3 - <<PY > "$md_path" 2> "${WORK_DIR}/${slug}.h2t.err" || true
import html2text, sys
with open("$html_path", "r", encoding="utf-8", errors="replace") as f:
    html = f.read()
h = html2text.HTML2Text()
h.body_width = 0
h.ignore_images = True
sys.stdout.write(h.handle(html))
PY
    fi
    printf -- "- [%d] \`%s\` → \`%s\` (HTTP %s, %s bytes)\n" \
      "$i" "$url" "$html_path" "$http_code" "$bytes" >> "$SUMMARY"
  else
    err_short=""
    if [ -f "${WORK_DIR}/${slug}.err" ]; then
      err_short=$(head -c 200 "${WORK_DIR}/${slug}.err" | tr '\n' ' ')
    fi
    printf -- "- [%d] \`%s\` → FAILED (HTTP %s, %s bytes) %s\n" \
      "$i" "$url" "${http_code:-000}" "$bytes" "$err_short" >> "$SUMMARY"
    # Keep the partial response for debugging; don't delete html_path.
  fi
done < "$URLS_FILE"

echo "Done. Wrote $i URLs to $OUT_DIR." >&2
exit 0
