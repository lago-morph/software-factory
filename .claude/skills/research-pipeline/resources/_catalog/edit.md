# Editing the catalog

This document covers every common edit operation. Read `schema-reference.md` first if you need to know what a field means; read `jq-recipes.md` if you need more jq examples.

## Cardinal rule

**Never edit `reference-only/sources.json` with `Edit` or `Write` directly.** Hand-editing JSON leads to:
- Trailing-comma errors
- Inconsistent indentation that pollutes diffs
- Key-ordering drift
- Accidental field misspellings the schema would catch later

Always go through jq + temp file + mv. After any change, normalize and run the linter.

## The standard edit cycle

```bash
F=reference-only/sources.json

# 1. Make the change to a temp file
jq '<your transform>' "$F" > /tmp/new.json

# 2. Normalize keys + ordering
mv /tmp/new.json /tmp/normalized.json
bash .claude/skills/research-pipeline/scripts/normalize-sources-json.sh /tmp/normalized.json

# 3. Atomic replace
mv /tmp/normalized.json "$F"

# 4. Lint
bash .claude/skills/research-pipeline/scripts/lint-sources.sh

# 5. If lint passes, commit
git add "$F"
git commit -m "..."
```

If lint fails, look at the error message — it always identifies the offending record id and field. Fix and re-lint.

## Adding a new source

### Case 1: You have a URL and want to register intent (no files yet)

Use `process-url-list.py` if you have multiple URLs, or do it manually:

```bash
URL="https://example.com/article"

# Compute id and canonical form
read CANON ID <<< $(python .claude/skills/research-pipeline/scripts/url_canonicalize.py "$URL" \
  | awk '/canonical_url:/{u=$2} /^id:/{print u, $2}')

# Add to catalog
jq --arg id "$ID" --arg url "$CANON" \
   '. + {($id): {id: $id, canonical_url: $url, title: "(unknown)", files: []}}' \
   "$F" > /tmp/new.json && \
mv /tmp/new.json "$F"
bash .claude/skills/research-pipeline/scripts/normalize-sources-json.sh "$F"
```

### Case 2: You have a URL and a downloaded file

```bash
URL="https://example.com/article"
LOCAL_FILE="/some/path/to/downloaded.html"

# Compute id
read CANON ID <<< $(python .claude/skills/research-pipeline/scripts/url_canonicalize.py "$URL" \
  | awk '/canonical_url:/{u=$2} /^id:/{print u, $2}')

# Move the file into the per-id directory
mkdir -p reference-only/$ID
cp "$LOCAL_FILE" reference-only/$ID/

# Compute sha256
SHA=$(sha256sum "reference-only/$ID/$(basename $LOCAL_FILE)" | awk '{print $1}')
FNAME=$(basename "$LOCAL_FILE")

# Add the record with the file entry
jq --arg id "$ID" --arg url "$CANON" --arg fname "$FNAME" --arg sha "$SHA" '
  . + {($id): {
    id: $id,
    canonical_url: $url,
    title: "(unknown)",
    files: [{
      format: "html",
      filename: $fname,
      ingestion_status: "have",
      completeness: "unknown",
      sha256: $sha
    }]
  }}
' "$F" > /tmp/new.json && \
mv /tmp/new.json "$F"
bash .claude/skills/research-pipeline/scripts/normalize-sources-json.sh "$F"
```

Then run `python scripts/sanity-check-record.py $ID` to verify content consistency.

### Case 3: You know a source exists by title but have no URL

```bash
# Use a deterministic placeholder id — just pick the first 10 hex chars of
# sha256 of the title. Mark canonical_url null. Add search_hints.

TITLE="A Field Guide to Rapidly Improving AI Products"
PLACEHOLDER_ID=$(echo -n "$TITLE" | sha256sum | head -c 10)

jq --arg id "$PLACEHOLDER_ID" --arg title "$TITLE" '
  . + {($id): {
    id: $id,
    title: $title,
    files: [],
    search_hints: [
      {hint: "Google: \"\($title)\"", tried: false, found: false}
    ]
  }}
' "$F" > /tmp/new.json && \
mv /tmp/new.json "$F"
bash .claude/skills/research-pipeline/scripts/normalize-sources-json.sh "$F"
```

When you eventually find a URL, **create a new record with the real id** (sha256 of URL) and set the placeholder's `pointer_to` to point at the new record. Don't try to mutate the id of the placeholder.

## Editing an existing record

### Update a scalar field
```bash
jq --arg id "0a7f3b8e00" --arg val "New summary text" \
   '.[$id].short_summary = $val' "$F" > /tmp/new.json && \
mv /tmp/new.json "$F"
bash .claude/skills/research-pipeline/scripts/normalize-sources-json.sh "$F"
```

### Add a tag (idempotent)
```bash
jq --arg id "0a7f3b8e00" --arg tag "evals" \
   '.[$id].tags = ((.[$id].tags // []) + [$tag] | unique)' \
   "$F" > /tmp/new.json && \
mv /tmp/new.json "$F"
bash .claude/skills/research-pipeline/scripts/normalize-sources-json.sh "$F"
```

### Add a file entry to an existing record
```bash
jq --arg id "0a7f3b8e00" --argjson f '{
  "format": "pdf",
  "filename": "extra.pdf",
  "ingestion_status": "have",
  "completeness": "complete",
  "sha256": "abcd..."
}' '.[$id].files += [$f]' "$F" > /tmp/new.json && \
mv /tmp/new.json "$F"
bash .claude/skills/research-pipeline/scripts/normalize-sources-json.sh "$F"
```

**Easier alternative**: drop the file into `reference-only/<id>/` directly and run:
```bash
python .claude/skills/research-pipeline/scripts/reconcile-source-dir.py <id>
```
The reconciler computes sha256, detects format, and adds the entry for you.

### Mark a file as superseded by a better version
```bash
# Update completeness of the inferior file
jq --arg id "0a7f3b8e00" --arg fname "partial.html" \
   '.[$id].files |= map(if .filename == $fname then .completeness = "partial" else . end)' \
   "$F" > /tmp/new.json && \
mv /tmp/new.json "$F"
bash .claude/skills/research-pipeline/scripts/normalize-sources-json.sh "$F"
```

If the file is genuinely useless, change `ingestion_status` to `skip-not-necessary` and consider whether to delete the file from disk (do so via `git rm reference-only/<id>/<fname>` so it's recorded in history).

## Retiring (not deleting) a record

Use `pointer_to` to redirect to a replacement:

```bash
OLD="0a7f3b8e00"
NEW="1b2c3d4e00"

jq --arg old "$OLD" --arg new "$NEW" \
   '.[$old].pointer_to = $new' "$F" > /tmp/new.json && \
mv /tmp/new.json "$F"
bash .claude/skills/research-pipeline/scripts/normalize-sources-json.sh "$F"
```

Optionally move the old record's files into the new one's directory:
```bash
git mv reference-only/$OLD/* reference-only/$NEW/  # if applicable
rmdir reference-only/$OLD                          # only if empty
```

The retired record's `files[]` should be cleared (or files moved to the new record and re-added there). The linter will warn about orphaned files in `reference-only/<OLD>/` if you leave them.

## Common mistakes to avoid

| Don't | Do |
|---|---|
| `Edit` or `Write` on `sources.json` | jq transform → temp → mv |
| Skip the normalize step | Always `bash .claude/skills/research-pipeline/scripts/normalize-sources-json.sh reference-only/sources.json` |
| Skip the linter | Always `bash scripts/lint-sources.sh` before staging |
| Hand-invent an id | Always `python scripts/url_canonicalize.py <url>` |
| Delete a record | Set `pointer_to`; record stays in the catalog |
| Put a path in `filename` | Use `location` override or rename to basename |
| Edit `references_from` by hand | Let `check-source-refs.py --fix` populate it (run as part of drain) |

## When the linter rejects your edit

See `validation.md` for the playbook on every error message.
