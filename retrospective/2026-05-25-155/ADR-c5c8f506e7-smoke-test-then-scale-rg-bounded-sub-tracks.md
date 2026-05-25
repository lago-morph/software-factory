# ADR: Smoke-test then scale pattern for RG-primitive bounded sub-tracks

- **ID**: ADR-c5c8f506e7
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-25
- **Source retrospective**: ../2026-05-25-155.md
- **PRs covered**: #146, #152

## Context

The [Phase-3.5.5 RG-primitive rule](../../architectures/v3/candidate-registry.md#phase-355-rule-on-load-bearing-rg-primitives-binding-user-approved-2026-05-25) gives candidates with research-grade-uncertainty load-bearing primitives a choice: (a) commit to a bounded authoring sub-track at Phase 4, or (b) downgrade the dependent contract to accept-as-RG. The rule says nothing about *how* the bounded sub-track should be structured. Two independent design events converged on the same answer:

- **U-B P-31** (auto-002 R2, overnight 2026-05-25): the initial proposal was a full sub-track delivering ≥15 invariants. Adversarial review rejected it on cost grounds (≥30× understated cost) and substance grounds (count-gate without substance discipline). Round 2 substituted a smoke-test (1 invariant per layer-pair, 5 total, with non-trivial definition + corpus citation + positive/negative examples) that gated a full sub-track. Result: smoke-test passed 5/5; full sub-track scaled to 20 invariants in this session's Wave 4.5.

- **BF-L conventional + invariant views** (auto-003 R2, this session): the initial proposal was bounded sub-tracks with count-gates (≥20 patterns per language × 3 languages = 60; ≥5 invariants per language × 3 = 15). Adversarial review rejected it identically: count-gate without substance discipline; calibrated-precision gate against a non-existent measurement instrument. Round 2 adopted the U-B smoke-test pattern: 3 non-trivial artifacts per language × 3 languages = 9 per view, with binary multi-cell verdict logic. Both BF-L smoke-tests PASSED 3/3 in this session's Wave 4.5.

The shape is consistent enough across two independent applications to deserve codification.

## Decision

When a candidate methodology carries a research-grade-uncertainty load-bearing primitive and elects the Phase-3.5.5 option (a) bounded sub-track, the sub-track structure is smoke-test (3 non-trivial artifacts per cell with multi-cell binary verdict) followed by conditional scale-up (≥10 per cell) only if smoke-test passes, with accept-as-RG plus methodology-degradation clause as the failure fallback.

## Alternatives considered

- **Direct full sub-track (no smoke-test).** Cheaper *if* it succeeds, but the auto-002 R1 evidence showed ≥30× cost-understatement risk; the failure mode is silent count-inflation that masks the substance question.
- **Smoke-test only, no scale-up.** Sufficient as a feasibility demonstration but not as Phase-5-ADR-grade content. The scale-up converts smoke-test feasibility into design-system content that Phase 6 architecture specs can cite.
- **Calibrated-precision gate (e.g., precision ≥0.7 against a golden corpus).** Rejected because the measurement instrument typically does not exist for RG primitives (that's why they're RG); the gate becomes functional pre-elimination via measurement absence.
- **Per-candidate ad-hoc gate shapes.** Rejected because the cross-candidate consistency (U-B + BF-L conventional + BF-L invariant) is itself evidence of robustness; codifying the pattern lets future candidates adopt it without rediscovering the substance-discipline failure mode.

## Consequences

- Future RG-primitive bounded sub-tracks have a known shape; subagent briefs are templatable.
- The non-trivial-definition clause and the honesty-discipline clause become mandatory components of the sub-track brief (currently they are P-31-smoke-test conventions that propagated by precedent; this ADR makes them binding).
- Cost: 1 smoke-test subagent per cell × multi-cell verdict + conditional 1-2 scale-up subagents. Total Wave-4.5-style cost per candidate: 1-3 subagents (smoke-test typically batches multiple cells into one subagent; scale-up is conditional).
- Trade-off accepted: the smoke-test's binary multi-cell verdict can produce a "1 of 3 passes" outcome that triggers partial sub-track + partial fallback. Methodology-degradation clauses then activate per-cell; the candidate's Phase-6 spec must articulate per-cell degradation. This is more complex than a single-bit pass/fail but more honest.

## References

- [`../2026-05-25-155.md`](../2026-05-25-155.md) — the source retrospective.
- [`./SKILL-SPEC-c62b95ee1c-bounded-sub-track-smoke-test-scaling.md`](./SKILL-SPEC-c62b95ee1c-bounded-sub-track-smoke-test-scaling.md) — the skill spec.
- [`../../architectures/v3/decisions/auto-002-ub-path.md`](../../architectures/v3/decisions/auto-002-ub-path.md) — first application (U-B P-31).
- [`../../architectures/v3/decisions/auto-003-bfl-rg-view-choice.md`](../../architectures/v3/decisions/auto-003-bfl-rg-view-choice.md) — second application (BF-L conventional + invariant).
- [`../../architectures/v3/primitives/P-31-smoke-test-invariants.md`](../../architectures/v3/primitives/P-31-smoke-test-invariants.md) — the smoke-test artifact that established the non-trivial-definition + honesty-discipline clauses.
- PRs the decision was made / applied in: #146 (auto-003 R2), #152 (Wave 4.5 outputs).
