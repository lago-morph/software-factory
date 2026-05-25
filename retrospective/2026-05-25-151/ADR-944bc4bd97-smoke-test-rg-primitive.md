# ADR: Smoke-test pattern for candidate sub-tracks with research-grade primitives

- **ID**: ADR-944bc4bd97
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-25
- **Source retrospective**: ../2026-05-25-151.md
- **PRs covered**: #142, #143

## Context

In the 2026-05-25 session, the v3 synthesis Phase-3.5.5 candidate re-check identified U-B (Pace-Layered Escrow Factory) as conditional survival because its load-bearing substrate primitive P-31 (cross-layer drift detector) had landed research-grade-uncertainty. Per the Phase-3.5.5 RG-primitive rule established later in the session, U-B had the option of a bounded Phase-4 invariant-authoring sub-track to convert the RG portion into designed-system content. Decision brief `auto-002` Round 1 proposed exactly that: a full Phase-4 sub-track delivering ≥15 cross-layer invariants (5 layer-pairs × ≥3 per pair).

Two real adversarial reviewers (scoping-principle skeptic + cost/scope hawk) caught two problems with Round 1: the brief misread the P-31 sketch on whether corpus fragments pointed at cross-layer invariants (they didn't — see [AGENTS-MD-d6fb69a1c8](AGENTS-MD-d6fb69a1c8-verify-cross-artifact-citations.md)), and the cost was understated by ~30× because it ignored the downstream Phase-5/6/7/8 tail U-B would absorb before any failure verdict. Both reviewers independently proposed a **smoke-test variant**: dispatch one subagent to attempt 1 non-trivial machine-checkable invariant per layer-pair (5 total) with explicit verdict logic. Cost: ~50K tokens (1 dispatch). 30× cheaper than full sub-track failure.

Round 2 adopted the smoke-test variant. The smoke-test (`P-31-smoke-test-invariants.md`) returned 5/5 non-trivial invariants with verbatim corpus citations — U-B survived with full sub-track authorized. If the smoke-test had returned ≤1/5, U-B would have self-eliminated at a small fraction of the original proposal's cost. Either verdict was acceptable; the smoke-test made the verdict cheap to obtain.

## Decision

**When a candidate methodology has a load-bearing primitive that lands research-grade-uncertainty at Phase-N close and a bounded authoring sub-track is being considered to convert it into designed-system content, dispatch a single Phase-N follow-up smoke-test subagent first to attempt one instance of the work per applicable unit, and adjudicate the full-commitment decision based on the smoke-test result rather than on a-priori plausibility.** The smoke-test verdict logic is declared in the decision brief before dispatch (e.g., "≥4 of 5 → full sub-track; 2-3 → contract restate; ≤1 → self-eliminate"). The pattern applies to any candidate / sub-system whose RG portion is feasibility-grade (not just calibration-grade) and whose proposed full sub-track is substantive (≥5 worker-units; rejection-cost ≥10× smoke-test-cost).

## Alternatives considered

- **Commit to the full sub-track on a-priori plausibility.** Rejected because the lead agent's plausibility judgment is exactly what an RG flag exists to caution against — by definition, the construction path is uncertain. The 2026-05-25 evidence is that `auto-002` Round-1 plausibility argument turned out to be misreading the source sketch; the smoke-test would have caught this even without the citation rule.
- **Self-eliminate on Phase-N close without giving the candidate a chance.** Rejected as too aggressive. The scoping principle is to carry every defensible candidate; an RG flag doesn't make a candidate undefendable — it makes the path to defense uncertain. The smoke-test is the cheap version of "let them attempt."
- **Run the full sub-track in parallel with all candidates' Phase-N+1 work, then adjudicate.** Rejected because failure of the sub-track at the end of Phase-N+1 has already incurred all the in-flight work. The smoke-test is at the boundary; failure-cost is bounded to the smoke-test itself.
- **Use one round of adversarial review instead of the smoke-test.** Rejected because reviewers can only attack the *arguments* in the brief; they can't run the work. The smoke-test produces actual evidence of feasibility. Reviewers can challenge the smoke-test's verdict-logic before dispatch and its results after — but the smoke-test produces what no number of reviewers can: actual execution.

## Consequences

**Easier.** Candidates with RG primitives can be carried through Phase-N close honestly without forcing premature self-elimination or premature commitment. The smoke-test result file is a durable evidence artifact that downstream phases reference; later Phase-4 / Phase-8 work has a concrete starting point rather than a hypothetical. Failures are cheap and provide negative evidence the user can review without losing all the downstream investment.

**Harder.** Each RG-primitive sub-track adjudication now requires a smoke-test before commitment — one extra subagent dispatch per affected candidate / primitive. The smoke-test verdict-logic must be declared in advance, which forces the lead agent (or reviewers) to articulate what "good enough" looks like before seeing the result. Smoke-tests that span heterogeneous units (e.g., per-language patterns) must sample structurally, not uniformly.

**Accepted trade-off.** The smoke-test pays for itself in expected value the moment one smoke-test prevents one full-sub-track failure. The 2026-05-25 evidence is that `auto-002`'s smoke-test was 30× cheaper than the full sub-track; even at a 50% baseline failure rate, the expected savings dominate.

## References

- [`../2026-05-25-151.md`](../2026-05-25-151.md) — the source retrospective.
- [`./SKILL-SPEC-6a405bb67c-smoke-test-before-commitment.md`](./SKILL-SPEC-6a405bb67c-smoke-test-before-commitment.md) — the operationalizing skill spec.
- [`./ADR-46130f96d5-v3-phase-3.5.5-rg-rule.md`](./ADR-46130f96d5-v3-phase-3.5.5-rg-rule.md) — the v3-specific RG-primitive rule this pattern instances.
- [`../../architectures/v3/primitives/P-31-smoke-test-invariants.md`](../../architectures/v3/primitives/P-31-smoke-test-invariants.md) — the canonical example of a smoke-test result file.
- [`../../architectures/v3/decisions/auto-002-ub-path.md`](../../architectures/v3/decisions/auto-002-ub-path.md) — the decision brief that adopted the pattern in Round 2.
- PRs the decision was made in: #142 (`auto-002` Round 2 adopting smoke-test variant), #143 (smoke-test result + cascade).
