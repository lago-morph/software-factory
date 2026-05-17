# Reference audit

`check-source-refs.py` cross-checks URLs cited in research reports against the catalog.

## What it checks

For every URL cited in any `.md` file under the configured `report_paths`:
1. Does the catalog have a record for that URL (matching on canonical form)?
2. Does that record's `references_from` list the citing report?

For every record in the catalog with a `canonical_url`:
1. Does at least one report cite that URL? (warning only — wanted records legitimately have no citations yet)

## Running it

```bash
python .claude/skills/research-pipeline/scripts/check-source-refs.py
```

Exit codes:
- `0` — catalog covers every cited URL
- `1` — at least one URL is cited but missing from catalog (or `references_from` is stale)

## Output format

```
✗ URL cited in research/29-prompt-engineering-survey.md (and 2 other report(s)) but no record in catalog: https://hamel.dev/blog/posts/llm-judge/

⚠ 0a7f3b8e00: references_from lists 'research/05-simon-willison.md' but URL not found in that file

⚠ 1b2c3d4e00: research/00-synthesis.md cites this URL but it's not in references_from
```

Errors (✗) are mismatches that need fixing. Warnings (⚠) are inconsistencies that should be cleaned up but don't block.

## Common scenarios

### "URL cited in X but no record in catalog"

A report cites a URL the catalog doesn't know about. Fix:
1. Create a record for it (see `edit.md` Case 1)
2. Either run the drain to fetch it, OR mark it as `want` and move on

Bulk-fix every uncatalogued URL via:
```bash
# Collect every URL cited but not in catalog
python .claude/skills/research-pipeline/scripts/check-source-refs.py 2>&1 \
  | grep -oE 'https?://\S+' \
  > /tmp/missing-urls.txt

# Add them as wanted records
python .claude/skills/research-pipeline/scripts/process-url-list.py /tmp/missing-urls.txt
```

### "references_from lists X but URL not found in that file"

The record claims it's cited in a report, but the report doesn't actually have the URL. Either:
1. The citation was removed from the report — drop the stale entry from `references_from`
2. The URL changed (e.g., the report uses a tracking-param variant the canonicalizer strips differently) — verify both sides canonicalize the same way

To fix the stale entry:
```bash
F=reference-only/sources.json
ID="0a7f3b8e00"
STALE_REPORT="research/05-simon-willison.md"

jq --arg id "$ID" --arg r "$STALE_REPORT" \
   '.[$id].references_from |= map(select(. != $r))' "$F" > /tmp/new.json && \
jq -S 'to_entries | sort_by(.key) | from_entries' /tmp/new.json > "$F"
```

### "report cites this URL but it's not in references_from"

The catalog's `references_from` is out of date — the report cites a URL but the record doesn't record that. Add the missing entry:

```bash
F=reference-only/sources.json
ID="0a7f3b8e00"
NEW_REPORT="research/29-prompt-engineering-survey.md"

jq --arg id "$ID" --arg r "$NEW_REPORT" \
   '.[$id].references_from = ((.[$id].references_from // []) + [$r] | unique)' "$F" \
   > /tmp/new.json && \
jq -S 'to_entries | sort_by(.key) | from_entries' /tmp/new.json > "$F"
```

The drain pipeline (PR #81) will auto-populate `references_from` for every record after each report is written. Until then, hand-update.

## URL matching rules

URLs are matched by canonical form (see `url_canonicalize.py`). This means:

- `https://example.com/page` and `https://example.com/page?utm_source=x` are equivalent — both match the same record.
- `https://EXAMPLE.com/Page/` and `https://example.com/Page` are equivalent (host lowercased, trailing slash stripped).
- `https://example.com/page#section` and `https://example.com/page` are equivalent (fragment dropped).

If a report's URL with tracking params doesn't match a record, verify the canonicalizer is stripping the same params on both sides.

## Punctuation handling

The check-source-refs script strips trailing `.,;:!?)]}>"'` from URLs found in reports — so `See https://example.com/page.` matches `https://example.com/page`. If you're seeing weird matches/mismatches, look at the actual URL extraction:

```bash
grep -oE 'https?://[^[:space:]<>")]+' research/29-*.md | sort -u | head -10
```

## Limits

- Only checks `.md` files in `report_paths`. Doesn't check code comments, README content elsewhere, etc.
- URL extraction is regex-based; obscure markdown autolinks like `<https://example.com/page>` work, but URL-shaped strings embedded in code blocks are also matched (might generate false positives if a report has example URLs in fence blocks). If this becomes a problem, add `--exclude-code-blocks` (not yet implemented; future work).
