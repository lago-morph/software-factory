# Drain stage 3 — catalog update

For each (file, URL, id) tuple from stage 2, create or update the catalog and physically move the file.

## Three sub-flows

### A. New record (id not in catalog)

```bash
ID="9f8e7d6c5b"
CANONICAL="https://newsite.org/post"
SRC="research/manual/new-thing.html"

# Create the target directory
mkdir -p reference-only/$ID

# Move the file
git mv "$SRC" "reference-only/$ID/$(basename $SRC)"

# Compute sha256
SHA=$(sha256sum "reference-only/$ID/$(basename $SRC)" | awk '{print $1}')
FNAME=$(basename "$SRC")

# Extract title (best-effort)
TITLE=$(python -c "
from extract_url import extract_url
from pathlib import Path
import re

p = Path('reference-only/$ID/$FNAME')
content = p.read_text(encoding='utf-8', errors='replace')[:5000]
m = re.search(r'<title[^>]*>([^<]+)</title>', content, re.IGNORECASE)
print((m.group(1) if m else '(unknown)').strip())
")

# Determine format
EXT="${SRC##*.}"
case "$EXT" in
  html|htm) FMT="html" ;;
  mhtml) FMT="mhtml" ;;
  md) FMT="md" ;;
  txt) FMT="txt" ;;
  pdf) FMT="pdf" ;;
  ipynb) FMT="ipynb" ;;
  *) FMT="other" ;;
esac

# Add to catalog
F=reference-only/sources.json
jq --arg id "$ID" --arg url "$CANONICAL" --arg title "$TITLE" \
   --arg fname "$FNAME" --arg sha "$SHA" --arg fmt "$FMT" '
  . + {($id): {
    id: $id,
    canonical_url: $url,
    title: $title,
    files: [{
      format: $fmt,
      filename: $fname,
      sha256: $sha,
      ingestion_status: "have",
      completeness: "unknown"
    }]
  }}
' "$F" > /tmp/new.json && \
jq -S 'to_entries | sort_by(.key) | from_entries' /tmp/new.json > "$F"
```

### B. Existing record (id already in catalog)

Same logic, but append to `files[]` instead of creating the record:

```bash
ID="0a7f3b8e00"
SRC="research/manual/page1.mhtml"

# Move into existing dir
git mv "$SRC" "reference-only/$ID/$(basename $SRC)"

SHA=$(sha256sum "reference-only/$ID/$(basename $SRC)" | awk '{print $1}')
FNAME=$(basename "$SRC")
FMT="mhtml"

# Append to files[]
jq --arg id "$ID" --argjson f "{
  \"format\": \"$FMT\",
  \"filename\": \"$FNAME\",
  \"sha256\": \"$SHA\",
  \"ingestion_status\": \"have\",
  \"completeness\": \"unknown\"
}" '.[$id].files += [$f]' "$F" > /tmp/new.json && \
jq -S 'to_entries | sort_by(.key) | from_entries' /tmp/new.json > "$F"
```

### C. Reconciliation (orphan files in existing `<id>/` dirs)

For each `<id>/` directory with unregistered files:

```bash
python scripts/reconcile-source-dir.py <id>
```

The script handles everything: format detection, sha256, comment markers for images, etc.

To reconcile every record at once:

```bash
python scripts/reconcile-source-dir.py --all
```

## Batch processing pattern

For a typical drain run with many files, batch the jq updates:

```bash
# Build a single jq filter that processes all files in one go
jq_filter='.'
# For each (id, url, file) — extend the filter
# ...

# Apply once
jq "$jq_filter" "$F" > /tmp/new.json
jq -S 'to_entries | sort_by(.key) | from_entries' /tmp/new.json > "$F"
```

Reduces the number of normalize passes and keeps the git diff coherent.

## Pointer handling

If the new URL extracted from a file points to an id that has a `pointer_to`:

```bash
ID="0a7f3b8e00"
POINTER=$(jq -r --arg id "$ID" '.[$id].pointer_to // empty' "$F")
if [ -n "$POINTER" ]; then
  echo "Record $ID is superseded → following pointer to $POINTER"
  ID="$POINTER"
  # Use $POINTER as the target for the file
fi
```

The file goes into the canonical (pointed-to) record's directory, not the superseded one.

## URL mismatch handling

If the file is being added to record X but its extracted URL doesn't quite match X's `canonical_url` (e.g., different tracking params that survived canonicalization, or the file is genuinely a different page):

1. Log a warning
2. Add the file anyway with a comment: `"URL extracted as Y, record canonical is Z — verify"`
3. Surface in drain summary for human review

The user decides whether to keep both, retire one with `pointer_to`, or split.

## After stage 3

Run stage 4 (validation). Don't skip.
