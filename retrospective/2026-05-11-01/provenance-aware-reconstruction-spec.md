# Spec: `provenance-aware-reconstruction`

## Intent

When primary sources are unavailable (sandbox 403s, paywalls, offline) and a research subagent must reconstruct content from secondary coverage, every claim must carry a provenance tag. Without this discipline, reconstructed claims propagate downstream as if they were verified facts, and synthesis layers cannot tell the difference between a verbatim quote and an LLM hallucination.

In this session, the v1 research pass (sandbox blocked the canonical sources) produced **five distinct fabrications** that propagated into all four architecture specs before the v2 pass caught them: a non-existent HN comment id (46955602), Willison's "4 agents → exhausted by 11 AM" specific number (only "11 AM" is verbatim; "4 agents" was invented), the "6,000–7,000 lines" StrongDM spec count (third-party speculation), the "DTU = Digital Twin Users" expansion (correct: "Universe"), and a Cal Newport attribution that didn't exist. Each propagated through synthesis into multiple downstream documents.

This skill prevents that by requiring provenance tags on every claim and preserving them through synthesis.

## Trigger

**Direct user requests:**
- "Set up a reconstruction-aware research run"
- "Make sure we tag provenance"
- `/provenance-aware`

**Proactive triggers (offer the skill):**
- A research subagent is about to operate on secondary sources because primary access is blocked.
- A subagent brief involves "extract verbatim quotes" or "list per-URL claims".
- Synthesizing material across multiple reconstructed sources.
- Reviewing a research report from a previous reconstruction pass.

**Negative triggers (do NOT activate):**
- The subagent has direct primary-source access (no reconstruction needed).
- The work is creative writing or design (no factual claims to attribute).

## Inputs

- A subagent brief (or a research report draft).
- The list of sources to be cited.
- Knowledge of which sources are primary (reachable) vs. secondary (reconstructed).

## Outputs

- A provenance-tagged subagent brief (or report) where every claim carries one of: `[verbatim]`, `[paraphrase, source confirmed]`, `[reconstructed from secondary]`, `[inference]`.
- A top-of-document "Reachability caveat" section listing which sources were reached vs. reconstructed.
- A revision pass checklist for upgrading reconstructed claims to verbatim when primary access becomes available.

## Workflow

1. **Audit reachability.** Before dispatching subagents, identify which sources are primary-reachable from the sandbox. Mark the rest as reconstruction candidates.
2. **Brief tagging.** In every reconstruction subagent's brief, mandate the provenance vocabulary and require tags on every claim. Example brief snippet: *"Every quoted claim must carry a provenance tag: `[verbatim]` (direct from a primary source), `[paraphrase, source confirmed]` (your wording, but the source supports it), `[reconstructed from secondary]` (you saw the claim only in a third-party source quoting the primary), `[inference]` (you derived this from context)."*
3. **Cross-check rule.** For every `[reconstructed]` quote, require at least TWO independent secondary sources that agree on the wording before promoting to `[paraphrase, source confirmed]`. One secondary source = stays `[reconstructed]`.
4. **ID verification.** Every numeric ID in a citation (HN comment id, PR number, page number) must be reachable in the actual fetched source, or labeled `[reconstructed id — verify before use]`.
5. **Synthesis preservation.** When a tagged claim feeds into a synthesis document, the tag travels with it. Stripping tags during synthesis is the worst failure mode — once stripped, downstream consumers treat the claim as fact.
6. **Revision-pass scheduling.** As part of the initial plan, schedule a revision pass against primary sources (not as an "if we have time" extra). The cost of fabrications propagating is higher than the cost of the revision pass.
7. **Caveat documentation.** Every reconstructed report has a top-of-document "Reachability caveat" section. Maintain it through revisions; never delete (only update when sources later become available).

## Concrete examples

### Example 1 — provenance tags in a sentence

Original v1 reconstruction:

> "Cherny reported 10–30 PRs/day across 10–15 parallel sessions."

With provenance tags:

> "Cherny is reported to ship 10–30 PRs/day [paraphrase from secondary, Lenny editorial summary] across 10–15 parallel sessions [reconstructed from third-party recap, not yet verified against primary]."

The second form makes the synthesis layer responsible for treating the "10–15" claim with appropriate suspicion. The v2 pass would have flagged it as needing verification.

### Example 2 — catching the Willison "4 agents" fabrication

A reconstruction subagent saw "mentally exhausted by 11 AM" in the Lenny editorial summary and inferred a specific count of parallel agents based on patterns in other sources. The brief should have required:

> *"For every numeric claim, cite the exact phrase from the source. If the number is not in the source verbatim, do not include it; flag the underlying claim as `[reconstructed — number not in primary]`."*

With this rule, the brief would have produced "Willison reports being mentally exhausted by 11 a.m. when running parallel agents [verbatim from Lenny summary]" with no specific count. The fabrication would not have happened.

### Example 3 — synthesis layer preserving tags

A bad synthesis update:

> "Cherny runs 10–15 parallel sessions and produces 10–30 PRs per day."

A good synthesis update:

> "Cherny is reported to run 10–15 parallel sessions [reconstructed] and ship 10–30 PRs/day [paraphrase, Lenny summary]. The session-count claim is not yet verified against primary."

The good version makes the editorial decision visible. The reader can decide to trust the claim, or to chase it down. The bad version pretends both numbers have equal evidentiary weight.

## Anti-patterns

- **Treating secondary summaries as primary.** A blog post quoting StrongDM's homepage is not StrongDM's homepage.
- **Dropping provenance tags during synthesis.** Once `[reconstructed]` becomes a plain quote, downstream consumers treat it as verified.
- **"Looks plausible" as a verification standard.** "Programming as a professional discipline will be over in a year or two" sounded plausible enough to pass v1 review — but no such comment exists. Plausibility is not verification.
- **Trusting URL slugs as label expansions.** `/dtu` does not mean "Digital Twin Users". The expansion lives in the body. (DTU = Digital Twin Universe.)
- **Verifying once and forgetting.** Provenance is metadata that travels with the claim. Verification of a paragraph is not verification of a sentence within it.

## Acceptance criteria

1. Every claim in a reconstructed report carries a provenance tag.
2. The report header has a "Reachability caveat" section listing primary-reached vs. reconstructed sources.
3. Synthesis documents that consume the report preserve tags on quoted claims.
4. A revision pass is scheduled (or completed) before claims are promoted into architecture / decision documents.
5. Cross-checking is enforced: any `[paraphrase, source confirmed]` quote has at least two independent secondary sources or one primary source backing it.

## Files this skill creates / modifies

- The subagent brief template (modify with provenance-tag requirement).
- The report template (add "Reachability caveat" section + provenance-tag vocabulary).
- An optional repo file `research/provenance-vocabulary.md` defining the tag set canonically.
- Synthesis-document headers / footers note which sources are reconstructed vs. primary.
