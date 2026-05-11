#!/usr/bin/env bash
# fetch-from-browser.sh — pull URLs that automated fetchers can't reach
#
# Use this when sources are behind:
#   - a paywall (Lenny, Every.to, Substack-paid posts)
#   - a Cloudflare interactive challenge that GitHub Actions runners can't solve (el-kaim)
#   - any login-required page
#
# It uses your browser's cookies (you provide a Netscape-format cookies.txt)
# plus a recent realistic User-Agent. Output goes to research/manual/, where
# the next research-pipeline-skill activation will pick it up.
#
# Usage:
#   bash research/fetch-from-browser.sh <path-to-cookies.txt> [url-list-file]
#
# Default url-list-file is research/unfetched-sources.md (the script extracts
# URLs from the markdown table). Pass any file with one URL per line to
# override.
#
# Notes:
#   - For Cloudflare interactive challenges (e.g. el-kaim), even cookies+UA
#     won't help — JavaScript challenge can't be solved by curl. For those,
#     use the browser's File → Save Page As → Web Page Complete and drop
#     the resulting .html into research/manual/ directly.
#   - For SPA / heavily JS-rendered pages, the saved HTML may be skeletal.
#     Reader View → copy text → paste into research/manual/<slug>.txt is a
#     reliable fallback.
#
# After files land in research/manual/, commit and push them. A subsequent
# research-pipeline activation will scan for new content and dispatch
# subagents to incorporate them, then delete the raw files.

set -euo pipefail

COOKIES="${1:?Usage: $0 <cookies.txt> [url-list-file]}"
URL_LIST="${2:-research/unfetched-sources.md}"
OUT_DIR="research/manual"
UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'

if [ ! -f "$COOKIES" ]; then
  echo "ERROR: cookies file not found: $COOKIES" >&2
  echo "Export from your browser via a 'Get cookies.txt' extension first." >&2
  exit 1
fi

mkdir -p "$OUT_DIR"

# Extract https://... URLs from the source file (works for plain lists or
# markdown tables — we just grep for URLs and dedupe).
mapfile -t URLS < <(grep -oE 'https?://[^[:space:]<>")|]+' "$URL_LIST" \
  | sed 's/[[:punct:]]*$//' \
  | sort -u)

if [ "${#URLS[@]}" -eq 0 ]; then
  echo "No URLs found in $URL_LIST" >&2
  exit 0
fi

slug_for() {
  local url="$1"
  local sha tail
  sha=$(printf '%s' "$url" | sha1sum | cut -c1-10)
  tail=$(printf '%s' "$url" \
    | sed -E 's|^https?://||; s|[^A-Za-z0-9._/-]|_|g; s|/+|__|g' \
    | cut -c1-80)
  printf '%s_%s' "$sha" "$tail"
}

echo "Fetching ${#URLS[@]} URL(s) into $OUT_DIR using cookies from $COOKIES"
echo

i=0
for url in "${URLS[@]}"; do
  i=$((i + 1))
  slug=$(slug_for "$url")
  out="$OUT_DIR/${slug}.html"

  echo "[$i/${#URLS[@]}] $url"
  http_code=$(curl --silent --show-error --location \
    --max-time 30 \
    --user-agent "$UA" \
    --cookie "$COOKIES" \
    --output "$out" \
    --write-out '%{http_code}' \
    "$url" || true)

  bytes=0
  [ -f "$out" ] && bytes=$(wc -c < "$out" | tr -d ' ')

  if [ "${http_code:-000}" = "200" ] && [ "$bytes" -gt 5000 ]; then
    # Quick sanity check — Cloudflare stubs are tiny and contain "Just a moment"
    if grep -q "Just a moment\|Attention Required\|cf-mitigated" "$out" 2>/dev/null; then
      echo "  -> got Cloudflare challenge ($bytes bytes); curl can't solve it. Use browser Save Page As." >&2
      mv "$out" "$out.cloudflare-stub"
    else
      echo "  -> saved $out ($bytes bytes)"
    fi
  else
    echo "  -> FAILED (HTTP ${http_code:-000}, $bytes bytes)" >&2
  fi
done

echo
echo "Done. Files in $OUT_DIR — commit, push, then ask Claude to drain new content."
