# Drain stage 2 — URL reverse-engineering

For each file from stage 1 that needs URL extraction, derive the canonical URL.

## The tool

```bash
python scripts/extract_url.py <path>
```

Returns the extracted URL or `(none)`.

Format-specific strategies built in:

| Format | Strategy |
|---|---|
| `.mhtml` | `Snapshot-Content-Location:` or `Content-Location:` MIME header |
| `.html` | `<link rel="canonical">`, then `<meta property="og:url">`, then `<meta name="twitter:url">` |
| `.pdf` | `/URL`, `/Source`, or `/URI` in PDF object metadata (best-effort, no PDF lib needed) |
| `.txt` | `URL: <url>` / `Source: <url>` / `Link: <url>` header, then first-line URL |
| `.md` | YAML frontmatter `url:` / `source:` / `canonical_url:`, then text strategies |
| `.ipynb` | First markdown cell scanned for URL |
| `.json` | Top-level `canonical_url` or `url` field |
| image/* | Always returns None (use directory placement instead) |

## Hard rule

**If URL extraction fails for a file in an ingestion drop directory:** the file is flagged as an error and **stays where it is**. The drain does not invent a URL or guess. The file does NOT enter the catalog.

The operator's job is then to either:
1. Add a URL header to the file (`URL: https://...` at the top) and re-run
2. Move the file into the right `reference-only/<id>/` directory manually (which makes it a stage-3 reconciliation case instead)
3. Decide the file isn't worth ingesting and delete it from the drop dir

**Exception:** if URL extraction fails for a file already in `reference-only/<id>/`, that's fine — directory placement IS the identity. No error.

## Canonicalization

The extracted URL is run through `url_canonicalize.py` before any lookup:

```bash
python scripts/url_canonicalize.py "$EXTRACTED_URL"
```

This produces `(canonical_url, id)`. The id is what we use to find/create the record.

## Handling redirects upstream

If a URL extraction yields a URL that you suspect is a redirect of an older URL we have in the catalog, search for the older URL:

```bash
jq --arg url "$EXTRACTED" \
   'to_entries | map(select(.value.canonical_url == $url or .value.original_url == $url))' \
   reference-only/sources.json
```

If you find a record, decide:
- Same content, new URL → update the record's `original_url` to preserve the back-reference
- Different content (the redirect target is a different thing) → create a new record

## Output of stage 2

For each file from stage 1:

```
file: research/manual/page1.mhtml
extracted URL: https://example.com/article
canonical: https://example.com/article
id: 0a7f3b8e00
status: existing record (will update)

file: research/manual/new-thing.html
extracted URL: https://newsite.org/post
canonical: https://newsite.org/post
id: 9f8e7d6c5b
status: new record (will create)

file: research/manual/mystery.html
extracted URL: (none)
status: ERROR — flagged, will not be processed
```

Pass this categorized list to stage 3.
