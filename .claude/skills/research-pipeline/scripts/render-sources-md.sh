#!/usr/bin/env bash
# Render reference-only/sources.md from reference-only/sources.json.
# Delegates to render-sources-md.py for the actual rendering (jq+bash got too
# complex once we added category grouping and the manual-fetch header table).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
exec python3 "$HERE/render-sources-md.py" "$@"
