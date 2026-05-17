# Manual additions

Three workflows for getting content into the catalog without writing JSON by hand. The filesystem is the UI; the catalog catches up.

## Workflow A: Track a URL without fetching (URL list)

You have one or more URLs you want to track but don't need to fetch yet. Drop a `.txt` (or `.md`) file containing just URLs into an ingestion drop directory:

```bash
cat > research/manual/urls-to-track.txt <<'EOF'
# Sources I want eventually
https://hamel.dev/blog/posts/llm-judge/
https://www.anthropic.com/news/multi-agent-research
https://eugeneyan.com/writing/llm-evaluator/
EOF
```

Then run:
```bash
python .claude/skills/research-pipeline/scripts/process-url-list.py research/manual/urls-to-track.txt --delete-after
```

For each URL:
- Compute the canonical form and id
- Create a record with `canonical_url` + `title: "(unknown)"` and no files
- If the id already exists, no-op

After processing, the `.txt` file is deleted. Re-running on the same file (recreated) is a no-op.

These records show up in § 3a (Wanted, URL known) of the markdown view. The drain pipeline knows to look for content for these URLs.

### What counts as a URL list?

Per `classify_text.py` rules:
- Every non-blank, non-`#`-comment line is a URL → **url_list**
- One URL on the first line + content below → **source_with_first_url** (treated as the source itself, not a URL list)
- A `URL: <url>` header line + content → **source_with_header_url** (same)
- Mixed URL and non-URL lines → **mixed_error** (flagged, not processed)
- No structure → **unrecognized** (flagged, not processed)

If your file gets rejected, the error message tells you why. Most often it's because you accidentally included a stray non-URL line.

## Workflow B: Drop content files into the right `<id>/` directory

When you've manually downloaded a file (PDF you saved from your browser, HTML you saved with "Save Page As", an extra screenshot, etc.) and you know which source it belongs to:

```bash
# Move it into the source's directory
mv ~/Downloads/extra-paper.pdf reference-only/0a7f3b8e00/

# Tell the catalog to catch up
python .claude/skills/research-pipeline/scripts/reconcile-source-dir.py 0a7f3b8e00
```

The reconciler:
1. Computes sha256 of the new file
2. Detects format from extension
3. Tries URL extraction (just for warning purposes — directory placement is the identity)
4. Adds a file entry with `ingestion_status=have`, `completeness=unknown`
5. For images, adds `comment: "(image — pending summary)"` so the drain knows to generate a visual summary

**You don't need to provide a URL.** The directory IS the identity. If the file's content has a URL that mismatches the record's `canonical_url`, you'll get a warning (not an error) — possibly worth investigating but doesn't block.

### Reconcile every record at once

```bash
python .claude/skills/research-pipeline/scripts/reconcile-source-dir.py --all
```

Useful after a bulk drop into multiple `<id>/` directories.

### Dry-run first

```bash
python .claude/skills/research-pipeline/scripts/reconcile-source-dir.py 0a7f3b8e00 --dry-run
```

Prints what would be added without modifying anything.

## Workflow C: Drop a content file in an ingestion directory

When you have a content file (HTML, MHTML, PDF, etc.) but it's NOT yet associated with a record — e.g., you found a new source and saved it from your browser:

```bash
# Drop it into research/manual/
cp ~/Downloads/saved-page.mhtml research/manual/

# Run the drain pipeline (which will process all uningested files)
```

See `_drain/workflow-overview.md` for the full drain procedure. In short:
1. Drain inventories the new file
2. Tries to extract its URL (per format rules)
3. If URL extraction succeeds → creates/updates the record + moves the file into `reference-only/<id>/`
4. If URL extraction fails → the file STAYS in `research/manual/` and is flagged as an error (you'll need to either fix the file or provide URL hints)

Unlike Workflow B, Workflow C requires a URL to be extractable from the file. If the file is an image with no extractable URL, drop it directly into the right `<id>/` directory (Workflow B).

## Quick decision tree

| Situation | Workflow |
|---|---|
| I have URLs I want to track later | A: URL list |
| I have a file and know which existing source it's for | B: drop into `<id>/` + reconcile |
| I have a file for a brand-new source | C: drop into `research/manual/` + drain |
| I have an image for an existing source | B: drop into `<id>/` (no URL needed) |
| I have a file and I'm not sure which source it's for | C: drop into `research/manual/` and let drain identify it |

## What happens to manually-dropped images

When you drop an image into `reference-only/<id>/` and reconcile, the file gets registered with `comment: "(image — pending summary)"`. The next drain run picks up that marker and generates an actual summary using vision capability:

```
comment: "Diagram showing 4-stage software factory pipeline: spec → plan → build → review.
Yellow boxes indicate human checkpoints; blue indicates agent steps."
```

The summary is searchable — `jq` for records with diagrams matching a topic:
```bash
jq 'to_entries | map(select((.value.files // [])[] | (.comment // "") | test("pipeline"; "i")))' \
  reference-only/sources.json
```

## Sanity check after manual additions

After any reconcile or drain that added files:
```bash
python .claude/skills/research-pipeline/scripts/sanity-check-record.py <id>
```

Flags warnings if the new file's content doesn't seem to match the record's existing files or the canonical URL — useful for catching "I dropped this into the wrong directory" mistakes.
