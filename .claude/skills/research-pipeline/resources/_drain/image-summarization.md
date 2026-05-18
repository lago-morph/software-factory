# Image summarization

When an image file is added to a record (via `reconcile-source-dir.py` or as part of the drain), its file entry gets `comment: "(image — pending summary)"`. This doc covers how to replace that marker with an actual summary.

## Why summarize?

The catalog's `files[].comment` field is searchable. A descriptive image summary lets jq queries like "do we have a diagram of X?" actually work:

```bash
jq 'to_entries | map(select((.value.files // [])[] | (.comment // "") | test("pipeline"; "i")))' \
  reference-only/sources.json
```

Without summaries, images are opaque blobs the catalog can't reason about.

## Procedure

For each file entry marked `(image — pending summary)`:

1. **Read the image** using vision capability:
   ```python
   # Conceptually:
   # The Read tool with image_path returns visual content the agent can describe
   ```

2. **Describe what it shows** in 2–3 sentences. Focus on:
   - The structural element (diagram, screenshot, chart, photo)
   - The key labels / arrows / text visible
   - The concept the image illustrates (in the context of the source's title)

3. **Update the file entry's comment**:
   ```bash
   F=reference-only/sources.json
   ID="0a7f3b8e00"
   FNAME="figure-1.png"
   SUMMARY="Diagram showing 4-stage pipeline: spec → plan → build → review. Yellow boxes are human checkpoints; blue is agent steps. Arrows indicate handoffs with explicit gating."

   jq --arg id "$ID" --arg fname "$FNAME" --arg s "$SUMMARY" \
      '.[$id].files |= map(if .filename == $fname then .comment = $s else . end)' "$F" \
      > /tmp/new.json && \
   mv /tmp/new.json "$F"
bash .claude/skills/research-pipeline/scripts/normalize-sources-json.sh "$F"
   ```

4. **Decide if the diagrams add information** — if yes and the record's `has_useful_diagrams` is `"unknown"` or `"no"`, update it:
   ```bash
   jq --arg id "$ID" '.[$id].has_useful_diagrams = "yes"' "$F" \
      > /tmp/new.json && \
   mv /tmp/new.json "$F"
bash .claude/skills/research-pipeline/scripts/normalize-sources-json.sh "$F"
   ```

   "Useful" = informationally distinct from the text. A header banner is not useful. An architecture diagram is.

## Batch summarization

If many records have pending image summaries:

```bash
jq -r 'to_entries[] | .key as $id | .value.files[] | select((.comment // "") | test("pending summary")) | "\($id)/\(.filename)"' \
  reference-only/sources.json
```

Process each one. Don't try to summarize all in one agent call — vision per-image is the unit.

## Summary style

| Good | Bad |
|---|---|
| "4-quadrant matrix mapping autonomy (low→high) against tooling sophistication (basic→advanced); positions Cursor, Claude Code, Codex, Devin." | "An image with some text and arrows" |
| "Sankey diagram of the 90-minute multi-agent run: 65% of tokens in LeadResearcher, 30% in subagents, 5% in CitationAgent. Total: 1.2M tokens." | "A diagram showing tokens" |
| "Screenshot of a GitHub PR review comment with three resolved threads and the merge button green." | "A screenshot" |

Be specific. Mention numbers, labels, axes, named entities. The summary is the search key.

## When NOT to summarize

- The image is purely decorative (logo, header banner, stock photo)
- The image content is already captured in the source's text (e.g., an OCR of a quote)
- The image is broken / a 404 placeholder

In these cases, set the comment to a short note explaining why no summary:

```
comment: "(decorative — site logo)"
comment: "(image rendering of a quote already captured in main.txt)"
comment: "(broken image placeholder)"
```

Don't leave the `(image — pending summary)` marker in place if you've reviewed the image and decided no real summary is warranted.

## Future automation

A future PR (not in scope for #79) could automate image summarization via a dedicated subagent. For now, summaries are an agent-side task done during drain stage 5 or as a separate manual pass.
