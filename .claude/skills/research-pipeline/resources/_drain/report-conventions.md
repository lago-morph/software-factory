# Report writing conventions

(Preserved from the pre-catalog version of this skill. Still applies — these are the conventions every research report in `research/` follows.)

## File naming

| Item | Default path |
|---|---|
| Research reports | `research/NN-<slug>.md` (NN = next zero-padded sequence integer; slug = short kebab-case noun phrase) |
| Partial reports | `research/NN-<slug>-partial.md` (when intentionally covering part of an originally larger scope) |
| Followup reports | `research/followup/NN-<slug>.md` |
| Research index | `research/INDEX.md` (one-line summary per report) |
| Resumable plan | `research/PLAN.md` (next-session handoff + §10 progress log) |
| Browser-fetch script | `research/fetch-from-browser.sh` |

## Report structure (every report)

```markdown
# NN — <Title>

**Date:** YYYY-MM-DD
**Branch:** claude/<short-slug>
**Status:** Active / Partial / Superseded
**Plan reference:** research/PLAN.md §X
**One-line:** <single sentence headline>

## TL;DR
1-paragraph synthesis

## <Substantive sections — H2 each>
Body content with inline citations linking to source URLs.
Each section addresses one sub-question from the report's lead question.

## Sources reviewed

| URL | Status | Notes |
|---|---|---|
| https://... | ✅ Primary anchor | Section §2; verbatim quote on X |
| https://... | ✅ Corroborates | Section §3 |
| https://... | ⚠ Paywall — summary only | |
| https://... | ❌ 404 — see Wayback | |

## Open questions
What's missing or needs more sources. These often become followup reports.
```

### Sources-Reviewed table legend

- **✅ Primary anchor** — load-bearing source for at least one substantive claim; quoted or paraphrased with specific attribution
- **✅ Corroborates** — supports a claim made primarily elsewhere; cited for triangulation
- **⚠ Partial** — fetched but truncated (paywall, JS shell, error, etc.); summarized only
- **❌ Sunset / 404** — URL no longer resolves; content lost or moved
- **❌ Blocked** — sandbox couldn't fetch; tracked in `research/unfetched-sources.md`

### Index entry format (in `research/INDEX.md`)

```markdown
| NN | <slug> | <status> | <one-line description of what the report covers> |
```

## Future-research clusters

When writing a report, you'll frequently spot cited sources that deserve their own focused investigation. Capture these at the end of the report:

```markdown
### Future research: <single-phrase cluster name>

3-5 cited URLs from this report's bibliography that share a tight theme
worth a dedicated drain. Include a 1-2 sentence justification per cluster.
```

These clusters seed future drain runs.

## Cross-references with other skills

- For fetching blocked URLs, use [fetch-blocked-urls](../../../../fetch-blocked-urls/SKILL.md).
- For in-flight workflow tracking (issues filed but not yet drained), use [in-flight-workflow-tracking](../../../../in-flight-workflow-tracking/SKILL.md).
- For per-source-cluster preliminary indexing (before a heavy drain), use [preliminary-index-pass](../../../../preliminary-index-pass/SKILL.md).
