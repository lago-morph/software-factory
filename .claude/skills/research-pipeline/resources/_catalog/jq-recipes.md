# jq recipes

Copy-pasteable jq one-liners for working with `reference-only/sources.json`. All examples assume:

```bash
F=reference-only/sources.json
```

## Read-only queries

### Count records
```bash
jq 'length' "$F"
```

### List all record ids
```bash
jq -r 'keys[]' "$F"
```

### Get one record by id
```bash
jq '.["0a7f3b8e00"]' "$F"
```

### Get just the title and URL for one record
```bash
jq '.["0a7f3b8e00"] | {title, canonical_url}' "$F"
```

### Find a record by URL substring
```bash
jq 'to_entries | map(select(.value.canonical_url? | tostring | test("simonwillison")))' "$F"
```

### List records by tag
```bash
jq 'to_entries | map(select(.value.tags? | type == "array" and any(. == "evals")))' "$F"
```

### Find records with no files
```bash
jq 'to_entries | map(select((.value.files // []) | length == 0)) | map(.key)' "$F"
```

### Find records pointing to a specific record
```bash
jq --arg target "0a7f3b8e00" \
   'to_entries | map(select(.value.pointer_to == $target)) | map(.key)' "$F"
```

### Show records cited in a specific report
```bash
jq --arg report "research/29-prompt-engineering-survey.md" \
   'to_entries | map(select(.value.references_from? | any(. == $report))) | map(.value.title)' "$F"
```

### Count files of each format across the whole catalog
```bash
jq '[.[] | (.files // [])[] | .format] | group_by(.) | map({format: .[0], count: length})' "$F"
```

### Find records with images marked useful
```bash
jq 'to_entries | map(select(.value.has_useful_diagrams == "yes")) | map(.value.title)' "$F"
```

## Editing patterns

**Cardinal rule:** never edit `sources.json` with `Edit` or `Write` directly. Use jq + temp file + mv. Always re-sort keys.

### Update a single field on one record
```bash
jq --arg id "0a7f3b8e00" --arg new "New short summary text" \
   '.[$id].short_summary = $new' "$F" > /tmp/new.json && \
jq -S 'to_entries | sort_by(.key) | from_entries' /tmp/new.json > "$F"
```

### Add a tag to a record (idempotent)
```bash
jq --arg id "0a7f3b8e00" --arg tag "evals" \
   '.[$id].tags = ((.[$id].tags // []) + [$tag] | unique)' "$F" > /tmp/new.json && \
jq -S 'to_entries | sort_by(.key) | from_entries' /tmp/new.json > "$F"
```

### Remove a tag
```bash
jq --arg id "0a7f3b8e00" --arg tag "old-tag" \
   '.[$id].tags |= map(select(. != $tag))' "$F" > /tmp/new.json && \
jq -S 'to_entries | sort_by(.key) | from_entries' /tmp/new.json > "$F"
```

### Add a new file entry to an existing record
```bash
jq --arg id "0a7f3b8e00" --argjson f '{
  "format": "pdf",
  "filename": "paper.pdf",
  "ingestion_status": "have",
  "completeness": "complete",
  "sha256": "abcdef..."
}' '.[$id].files += [$f]' "$F" > /tmp/new.json && \
jq -S 'to_entries | sort_by(.key) | from_entries' /tmp/new.json > "$F"
```

### Mark a file's status (e.g. flip want → have)
```bash
jq --arg id "0a7f3b8e00" --arg fname "main.pdf" \
   '.[$id].files |= map(if .filename == $fname then .ingestion_status = "have" | .completeness = "complete" else . end)' \
   "$F" > /tmp/new.json && \
jq -S 'to_entries | sort_by(.key) | from_entries' /tmp/new.json > "$F"
```

### Create a new record from scratch
```bash
# First compute the id
URL="https://example.com/new-source"
ID=$(python .claude/skills/research-pipeline/scripts/url_canonicalize.py "$URL" | awk '/^id:/{print $2}')
CANONICAL=$(python .claude/skills/research-pipeline/scripts/url_canonicalize.py "$URL" | awk '/^canonical_url:/{print $2}')

# Then add the record
jq --arg id "$ID" --arg url "$CANONICAL" --arg title "Title Of Source" \
   '. + {($id): {id: $id, canonical_url: $url, title: $title, files: []}}' "$F" > /tmp/new.json && \
jq -S 'to_entries | sort_by(.key) | from_entries' /tmp/new.json > "$F"
```

### Mark a record as superseded (pointer_to another)
```bash
jq --arg old "0a7f3b8e00" --arg new "1b2c3d4e00" \
   '.[$old].pointer_to = $new' "$F" > /tmp/new.json && \
jq -S 'to_entries | sort_by(.key) | from_entries' /tmp/new.json > "$F"
```

### Bulk: add `references_from` entries derived from a grep
```bash
# Find every record whose URL appears in a given report and append that report
REPORT="research/00-synthesis.md"
URLS=$(grep -oE 'https?://[^[:space:]<>")]+' "$REPORT" | sort -u)
for URL in $URLS; do
  ID=$(python .claude/skills/research-pipeline/scripts/url_canonicalize.py "$URL" 2>/dev/null | awk '/^id:/{print $2}')
  if jq -e --arg id "$ID" 'has($id)' "$F" >/dev/null; then
    jq --arg id "$ID" --arg ref "$REPORT" \
       '.[$id].references_from = ((.[$id].references_from // []) + [$ref] | unique)' \
       "$F" > /tmp/new.json && mv /tmp/new.json "$F"
  fi
done
# Final sort:
jq -S 'to_entries | sort_by(.key) | from_entries' "$F" > /tmp/new.json && mv /tmp/new.json "$F"
```

## Normalization & sort discipline

After ANY edit:

```bash
jq -S 'to_entries | sort_by(.key) | from_entries' "$F" > /tmp/normalized.json && \
mv /tmp/normalized.json "$F"
```

This:
1. Sorts object keys within each record (`-S`)
2. Sorts records by id
3. Pretty-prints with default indentation

After re-normalizing, run the linter:
```bash
bash .claude/skills/research-pipeline/scripts/lint-sources.sh
```

## Output formats

### Compact one-line summaries
```bash
jq -r 'to_entries[] | "\(.key)  \(.value.title)  \(.value.canonical_url // "(no url)")"' "$F"
```

### CSV for import into a spreadsheet
```bash
jq -r 'to_entries[] | [.key, .value.title, .value.canonical_url] | @csv' "$F"
```

### Just records with broken pointer_to (for debug)
```bash
jq 'to_entries | map(select(.value.pointer_to and (.value.pointer_to as $p | $p | in($parent // {})) == false))' "$F"
```
(That last one is awkward — easier to just run `validate-sources.py`.)

## Diff-friendly editing in practice

The pattern that minimizes commit diffs:

```bash
F=reference-only/sources.json

# 1. Make the change to a tmp file
jq '...your transform...' "$F" > /tmp/new.json

# 2. Normalize
jq -S 'to_entries | sort_by(.key) | from_entries' /tmp/new.json > /tmp/normalized.json

# 3. Replace atomically
mv /tmp/normalized.json "$F"

# 4. Lint
bash .claude/skills/research-pipeline/scripts/lint-sources.sh

# 5. Commit
git add "$F"
git commit -m "..."
```

The git diff for a single-field edit will be 3 lines: the field's old and new value. No reordering noise.
