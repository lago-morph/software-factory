# Querying the catalog

Read-only operations. For editing patterns see `edit.md`. For comprehensive jq snippets see `jq-recipes.md`.

## Quick lookups

```bash
F=reference-only/sources.json
```

### "What's record X?"
```bash
jq '.["0a7f3b8e00"]' "$F"
```

### "What's record X's title and URL?"
```bash
jq '.["0a7f3b8e00"] | {title, canonical_url}' "$F"
```

### "Find the record for URL X"
```bash
URL="https://example.com/article"
ID=$(python .claude/skills/research-pipeline/scripts/url_canonicalize.py "$URL" \
     | awk '/^id:/{print $2}')
jq --arg id "$ID" '.[$id]' "$F"
```

### "Find any record citing 'simonwillison' in its URL"
```bash
jq 'to_entries | map(select(.value.canonical_url? | test("simonwillison")))' "$F"
```

### "What records are tagged 'evals'?"
```bash
jq 'to_entries | map(select(.value.tags? | any(. == "evals"))) | map(.value.title)' "$F"
```

### "What reports cite record X?"
```bash
jq '.["0a7f3b8e00"].references_from' "$F"
```

### "What records does report Y cite?"
```bash
REPORT="research/29-prompt-engineering-survey.md"
jq --arg r "$REPORT" \
   'to_entries | map(select(.value.references_from? | any(. == $r))) | map({(.key): .value.title}) | add' "$F"
```

## Discovery / browsing

### "Show me the markdown browse view"
The MD is at `reference-only/sources.md`. It's auto-regenerated when sources.json changes on main. Read it directly:

```bash
cat reference-only/sources.md | less
```

Or grep for an id / topic / tag and jump to the record in the JSON.

### "Show me records with no files yet (wishlist)"
```bash
jq 'to_entries | map(select((.value.files // []) | length == 0)) | map({(.key): .value.title}) | add' "$F"
```

### "Show me records where some files are wanted"
```bash
jq 'to_entries | map(select((.value.files // [])[] | .ingestion_status == "want")) | map({(.key): .value.title}) | add' "$F"
```

### "Which records have problems (partial/error files)?"
```bash
jq 'to_entries | map(select((.value.files // [])[] | .completeness == "partial" or .completeness == "error"))' "$F"
```

### "Count things"
```bash
jq 'length' "$F"                                                            # total records
jq '[.[] | select(.pointer_to == null)] | length' "$F"                     # non-superseded
jq '[.[] | (.files // []) | length] | add' "$F"                            # total file entries
jq '[.[] | (.files // [])[] | select(.ingestion_status == "have")] | length' "$F"  # files we have
```

## Cross-record analyses

### "Group records by tag"
```bash
jq '[.[] | {title, tags: (.tags // [])}] | reduce .[] as $r ({}; . as $acc | $r.tags | reduce .[] as $t ($acc; .[$t] = ((.[$t] // []) + [$r.title])))' "$F"
```

### "Find records with similar canonical_url hosts (potential dupes)"
```bash
jq '[.[] | select(.canonical_url) | .canonical_url | capture("https?://(?<host>[^/]+)").host] | group_by(.) | map({host: .[0], count: length}) | sort_by(-.count)' "$F"
```

### "List all reports referenced by any record"
```bash
jq '[.[] | (.references_from // [])[]] | unique | sort' "$F"
```

## Working from a record id

When the user gives you an id, the first thing to do is fetch and print the record:

```bash
ID="0a7f3b8e00"
jq --arg id "$ID" '.[$id]' "$F"
```

If you only need the location of the files on disk:
```bash
jq --arg id "$ID" '.[$id].files[] | {format, filename, location, ingestion_status, completeness}' "$F"
```

To actually read a file:
```bash
ls reference-only/$ID/
cat reference-only/$ID/main.txt
```

## What NOT to do

- Do not Read the entire `sources.json` into your context window. Use jq.
- Do not parse the markdown view to find data — go to the JSON.
- Do not assume id values are sequential — they're sha256 prefixes (effectively random).
- Do not assume a file path until you've looked at `files[].location` (it may override the default).
