# Drain stage 5 — content processing

The catalog is valid. Now extract content from registered sources into research reports.

This is the stage that used to be the entire "drain" workflow in pre-catalog versions of this skill. It still does roughly the same thing — reads source content, summarizes/extracts, folds into reports — but operates on **record IDs**, not file paths.

## Per-record workflow

For each record that has new content to process (i.e., files added in this drain run):

1. **Read the record's metadata**:
   ```bash
   jq --arg id "$ID" '.[$id]' reference-only/sources.json
   ```

2. **Read the primary file**:
   ```bash
   PRIMARY=$(jq -r --arg id "$ID" \
     '.[$id].files[] | select(.format != "image/png" and .format != "image/jpeg") | .filename' \
     reference-only/sources.json | head -1)
   cat "reference-only/$ID/$PRIMARY"
   ```

3. **Extract content** — summarize, pull key claims, identify quotes worth anchoring.

4. **Identify or create the target report** — based on the source's theme/tags, find the right `research/NN-<slug>.md` or `research/followup/NN-<topic>.md`.

5. **Add content to the report** — extend an existing section or add a new one. Cite the source by its `canonical_url` (the linter uses URL matching, not id matching, for `references_from`).

6. **Update the record's `references_from`** — after the report is written, add the report path:
   ```bash
   F=reference-only/sources.json
   ID="0a7f3b8e00"
   REPORT="research/29-prompt-engineering-survey.md"

   jq --arg id "$ID" --arg r "$REPORT" \
      '.[$id].references_from = ((.[$id].references_from // []) + [$r] | unique)' "$F" \
      > /tmp/new.json && \
   mv /tmp/new.json "$F"
bash .claude/skills/research-pipeline/scripts/normalize-sources-json.sh "$F"
   ```

7. **If the source's content is now fully captured** (the report covers what's worth quoting), update the file's `completeness`:
   ```bash
   jq --arg id "$ID" --arg fname "$PRIMARY" \
      '.[$id].files |= map(if .filename == $fname then .completeness = "complete" else . end)' \
      "$F" > /tmp/new.json && \
   mv /tmp/new.json "$F"
bash .claude/skills/research-pipeline/scripts/normalize-sources-json.sh "$F"
   ```

## Image content

If the record has image files marked with `comment: "(image — pending summary)"`, generate summaries:

See `image-summarization.md` for the full procedure. In short:
1. Read the image (vision-capable)
2. Write a 2–3 sentence summary describing what it shows
3. Replace the pending-summary marker with the real comment
4. Set `has_useful_diagrams` on the record if the diagrams add information

## YouTube embed candidates

If the drain run summary lists any YouTube URLs under "YouTube embed candidates", read the surrounding-text snippet and decide whether the video is worth a transcript. For each useful one, add a `youtube-transcript` file entry with `ingestion_status: want` to the embedding record. The user then fetches the transcript and drops a `.txt` file (first line = video URL) for drain/reconcile to promote.

Full procedure: `youtube-transcripts.md`.

## Failure-mode discovery and registration

> **Cross-reference:** [`architecture-failure-mode-gate`](../../../architecture-failure-mode-gate/SKILL.md) skill owns `architectures/failure-modes.md`, its schema, and the CI gate that enforces column-correspondence with the architecture alternatives. Load it whenever you touch the file. The procedure below covers the *discovery* side (proposing a new F-mode from a research source); the gate skill covers the *table edit* side (the row/column mechanics). Adding a new F-mode row is a row-level event — the gate explicitly does NOT require column-spillover correspondence for row additions.

When a source proposes, names, or surfaces a new failure mode, the canonical project-wide index is [`architectures/failure-modes.md`](../../../../../architectures/failure-modes.md). This is the index of record — every newly-promoted failure mode MUST be registered there in the same commit that lands the report proposing it. Failure-mode *definitions* may continue to live in their proposing report or synthesis doc (that is where the verbatim provenance sits); [`architectures/failure-modes.md`](../../../../../architectures/failure-modes.md) is the index — short row per F-mode pointing to the canonical definition — plus the per-architecture coverage matrix seeded from [`architectures/00-comparison.md`](../../../../../architectures/00-comparison.md) §2.4.

### Procedure when a report proposes a new failure mode

1. **Pick a candidate number.** Read [`architectures/failure-modes.md`](../../../../../architectures/failure-modes.md) AND [`research/INDEX.md`](../../../../../research/INDEX.md) ("Looking for a failure mode" entry) to find the current high-water mark. Allocate the next free integer.

2. **Detect collisions.** Search the repo for the candidate number BEFORE writing the report:

   ```bash
   # Replace 47 with the candidate number
   grep -rn "F47\b" --include="*.md" .
   ```

   If the number is already used by a *different* proposed failure mode (this happened with F36/F37 — see [`research/PLAN.md` §3.6 at commit `58216ff`](https://github.com/lago-morph/software-factory/blob/58216ffdf8b0e2a86ec0fd536eed57c6d6fbc713/research/PLAN.md#L83-L97) for the worked example; the live file is [`research/PLAN.md`](../../../../../research/PLAN.md) but its section numbers drift), you have a collision.

3. **Resolve collisions by renumbering, not by ignoring.** When two proposals collide:
   - The earlier-merged proposal keeps the number (de-facto incumbent).
   - The new proposal takes the next free integer.
   - If both are landing in the same session, the report that registers first in [`architectures/failure-modes.md`](../../../../../architectures/failure-modes.md) keeps the number; the other re-numbers.

4. **Propagate the renumbered identifier.** A renumber is not done until every reference is updated. After the table in [`architectures/failure-modes.md`](../../../../../architectures/failure-modes.md) settles, search carefully and fix EVERY occurrence:

   ```bash
   # Use word-boundary matching to avoid matching F45 when searching for F4
   grep -rn "F<OLD>\b" --include="*.md" .
   # Also check non-markdown formats — JSON, YAML, scripts
   grep -rn "F<OLD>\b" .
   ```

   Common reference sites:
   - The proposing report itself (the §N.N title; in-line citations like "F<OLD> proposed")
   - [`research/INDEX.md`](../../../../../research/INDEX.md) (the per-report row + the "Looking for a failure mode" entry)
   - [`research/PLAN.md`](../../../../../research/PLAN.md) (collision notes; round-summary bullets)
   - [`research/synthesis/`](../../../../../research/synthesis/) `*.md` (cross-references)
   - Other reports that already cite the colliding number
   - [`architectures/`](../../../../../architectures/) `*.md` (rarely; the comparison doc's matrix is in [`architectures/failure-modes.md`](../../../../../architectures/failure-modes.md) itself)
   - [Retrospectives](../../../../../retrospective/) and [ADRs](../../../../../docs/adr/)

   A renumber missed in any of these silently corrupts cross-references — the diff must show every old number replaced.

5. **Register in [`architectures/failure-modes.md`](../../../../../architectures/failure-modes.md).** Add a row to the index naming the F-mode and its canonical definition site. If the report adds per-architecture coverage data, extend the coverage matrix too. Commit [`architectures/failure-modes.md`](../../../../../architectures/failure-modes.md) in the same commit as the proposing report.

6. **Update [`research/INDEX.md`](../../../../../research/INDEX.md).** The "Looking for a failure mode" entry at the bottom of the index is the lookup table from F-mode number to definition site; keep it in sync.

### When NOT to propose a new F-mode

Before allocating a new number, check whether the phenomenon is already covered by an existing F-mode. The corpus has caught false novelty several times (e.g., F24 *trust creep* is adjacent to F7 *normalization of deviance* but distinguishable; promoted as separate after vetting). When in doubt, frame as a sharpening of the existing F-mode rather than a new one — the catalog's value is in distinct mitigations, not in count.

---

## Multi-source synthesis

When multiple records contribute to the same section of a report, the drain agent's job is to synthesize — not just append. Read all relevant sources, identify overlapping claims, surface contradictions, note where one source is the primary anchor and others are corroborating.

The output is a cohesive report section, with footnote-style citations to each source's URL.

## Synthesis docs — where they live and how they're versioned

Cross-report synthesis documents live in `research/synthesis/` (not at the top of `research/`). Both the existing syntheses (`00-synthesis.md`, `13-round-2-synthesis.md`) and any new ones go there.

Every synthesis doc carries a YAML frontmatter header identifying the corpus state it was authored against:

```yaml
---
based-on-commit: <short-sha>
based-on-date: YYYY-MM-DD
---
```

The same header convention applies to architecture docs under `architectures/`. This skill does not own that directory, but the rule is shared so future readers can always tell what evidence base a synthesis or architecture decision sits on.

## Report structure conventions

(Inherited from the legacy SKILL.old.md; preserved here for continuity)

Each report follows:
```markdown
# NN — <Topic>

**Date:** YYYY-MM-DD
**Branch:** claude/<short-slug>
**Status:** Active / Partial / Superseded
**Plan reference:** research/PLAN.md §X

## TL;DR
1-paragraph synthesis

## Sources status
| URL | Status | Notes |
|---|---|---|
| https://... | ✅ Primary anchor | |
| https://... | ✅ Corroborates | |

## §1, §2, ...
Substantive sections, with inline citations.

## Open questions
What's missing or needs more sources.
```

## Phase 0 reminder

Don't start stage 5 unless stages 1–4 are complete and lint passes. Stale catalog state + new report content is a recipe for drift.

## After stage 5

Commit the report + catalog changes:

```bash
git add research/ reference-only/sources.json
git commit -m "drain: report NN updated with N new sources"
```

The auto-workflow regenerates `sources.md` on the next push to main.
