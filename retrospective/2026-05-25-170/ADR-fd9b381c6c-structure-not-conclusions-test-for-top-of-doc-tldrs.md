# ADR: Structure-not-conclusions test for top-of-doc TL;DRs

- **ID**: ADR-fd9b381c6c
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-25
- **Source retrospective**: ../2026-05-25-170.md
- **PRs covered**: #161, #164

## Context

The [context-slimming plan](../../CONTEXT-SLIMMING-PLAN.md) introduces a TL;DR-first discipline: the two heaviest foundational docs carry a `## TL;DR (≤200 words)` section at the top, regenerated end-of-run by a subagent reading the body. The discipline works only if the TL;DR captures **structure** (what topics live where, how the doc is organized) rather than **conclusions** (what the body argues for). A TL;DR that restates conclusions silently drifts when the body's conclusions change, because the regen subagent does not know which TL;DR lines were structural vs. conclusion-restating; it just rewrites the whole TL;DR from the body.

In PR A2 of the 2026-05-25 run, the lead-agent-inline TL;DR on `architectures/v3/candidate-registry.md` (99 words) included the sentence "The previously-proposed GF → BF continuity matrix is **withdrawn** per DEC-1.b." The fresh-context verification subagent in PR A5 flagged this as a concern: would the line need updating if the policy flipped (i.e., a future Phase 5 re-evaluates and re-proposes the matrix)? Yes ⇒ restates content. PR A5 rephrased to name a structural element instead (presence of a strikethrough section in the registry).

## Decision

**Every line of a top-of-doc `## TL;DR (≤200 words)` section MUST pass the heuristic "would this line need updating if the doc's conclusions changed?" — if yes, rewrite to name a structural element rather than a conclusion.** The test is applied as a self-review pass before commit by the TL;DR author, and is mechanically verified by the fresh-context-verification subagent pattern (see [SKILL-SPEC-ad9a173772](./SKILL-SPEC-ad9a173772-phase-A-fresh-context-verification.md)).

## Alternatives considered

- **No rule; rely on TL;DR authors to use good judgment.** Rejected because the failure mode is silent: a conclusion-restating TL;DR looks well-written until the body's conclusion changes, at which point the regen subagent cannot distinguish "preserve this structural line" from "regenerate this conclusion line." The 2026-05-25 PR A2 demonstrated that even a careful lead-agent author missed the failure mode.
- **Forbid TL;DRs entirely.** Rejected because the TL;DR-first discipline is load-bearing for the context-slimming plan; the 2-large-doc TL;DR contract saves ~30-35% of session-start context per the plan's expected savings.
- **Require TL;DRs but disable regeneration.** Rejected because manual TL;DR maintenance is the failure mode this discipline was designed to avoid (TL;DRs drift behind their bodies).

## Consequences

**Easier:** TL;DR regeneration becomes mechanically safe — the regen subagent rewrites the TL;DR from the body without risking a structural-line erase, because every line is structural by rule. The discipline is self-checking via the verification-subagent pattern.

**Harder:** TL;DR authors must apply one extra heuristic check per line at authoring time. Some lines that read more naturally as conclusion-restatement (e.g., "the registry withdraws the X matrix") need to be rephrased to structural form ("the registry contains a strikethrough-marked X section"), which can read awkwardly.

**Trade-off accepted:** A slight authorial-effort tax at TL;DR write-time in exchange for mechanical safety of the regeneration loop.

**Explicitly NOT promising:** the rule does not apply to TL;DRs in non-regenerating contexts (e.g., a one-off summary in a PR description). It applies only to top-of-doc `## TL;DR (≤200 words)` sections that the autonomous-run skill's end-of-run regeneration sub-step targets.

## References

- [`../2026-05-25-170.md`](../2026-05-25-170.md) — source retrospective.
- [`./AGENTS-MD-a1ca4ac935-tldr-structure-not-conclusions-test.md`](./AGENTS-MD-a1ca4ac935-tldr-structure-not-conclusions-test.md) — per-rule agents-file addition for this ADR.
- [`./SKILL-SPEC-ad9a173772-phase-A-fresh-context-verification.md`](./SKILL-SPEC-ad9a173772-phase-A-fresh-context-verification.md) — the verification skill that mechanically catches violations.
- [`../../CONTEXT-SLIMMING-PLAN.md`](../../CONTEXT-SLIMMING-PLAN.md) § Part 3 — TL;DR-first discipline.
- [`../../.claude/skills/autonomous-run/SKILL.md`](../../.claude/skills/autonomous-run/SKILL.md) § End-of-run protocol step 3 — TL;DR regeneration sub-step.
- PRs: #161 (PR A2, original TL;DR with the failure mode), #164 (PR A5, the fix).
