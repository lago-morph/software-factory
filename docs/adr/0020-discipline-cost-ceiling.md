# ADR 0020: Discipline — cost ceiling

- **Status**: Accepted
- **Date**: 2026-05-25
- **Deciders**: lead agent (Phase 5 Wave 5.2 exemplar)

## Context

Cost ceilings appear across most candidates' substrate-requirements summaries as a **discipline** binding the methodology layer to substrate enforcement. The [disciplines index](../../architectures/v3/disciplines/index.md) names cost-ceiling as one of 21 canonical disciplines; the per-discipline write-up at [`disciplines/cost-ceiling.md`](../../architectures/v3/disciplines/cost-ceiling.md) describes the contract surface.

The forcing concern is unbounded token / call / dollar spend during long-running agentic cycles — particularly under [GF-M's paraphrase fan-out × cost-ceiling interaction](../../architectures/v3/tracks/greenfield-methodology-first.md) where Regime-A paraphrase divergence is a known multiplier. Without a multi-axis hard cap enforced at the substrate layer, methodology drift accumulates silently; the absence is `voluntary-discipline-fragile` per [F53](../../architectures/v3/failure-modes-v3.md).

Cost-ceilings sits *between* substrate primitive [P-02 (cost ceilings, hard, multi-axis)](../../architectures/v3/primitives/cluster-C1.md) and the methodology layer: P-02 is the **enforcement mechanism**; this discipline is the **methodology contract** that names which axes are bound, under which regime classes, with which escalation behavior.

## Decision

**The cost-ceiling discipline binds every methodology to declare, per [eligibility regime class](../../architectures/v3/disciplines/regime-classification.md), a multi-axis hard cap (tokens, calls, dollar, wall-clock) and an escalation behavior on cap breach (halt / escalate-to-operator / fallback-to-cheaper-policy).** Caps are enforced by [P-02](../../architectures/v3/primitives/cluster-C1.md) at the substrate layer; the methodology authors the per-regime cap-table and the breach-handling contract. Methodology shapes that fan out (e.g., GF-M Regime-A paraphrase divergence) MUST account for fan-out cost as a known multiplier in the cap-table, not as an exceptional case.

Architecture-spec authors (Phase 6) write the per-regime cap-table for each candidate. Phase-8 lean-evals MUST include a cap-breach pressure-test for each candidate at least once.

## Alternatives considered

**B. Discipline lives entirely at substrate (P-02 alone, no methodology contract).** *Why rejected:* substrate enforces the cap value but does not know which axis matters per regime — a methodology that values latency would set wall-clock tight and tokens loose; a methodology that values cost would invert. The per-regime cap-table is a methodology decision that the substrate can only enforce, not author. Without the methodology contract, regimes default to substrate's vendor-friendly defaults and the discipline degenerates to F53-fragile per-deployment ops. See [P-02 sketch](../../architectures/v3/primitives/cluster-C1.md).

**C. Soft caps with operator escalation only.** *Why rejected:* soft caps invite F40 (last-mile drift) where a methodology hovers near cap without breaching, accumulating cost over many cycles. Hard caps with explicit fallback-to-cheaper-policy keep methodology behavior bounded. See [cost-ceiling discipline write-up](../../architectures/v3/disciplines/cost-ceiling.md).

## Consequences

**Easier:** Cost-bounded execution across all candidates; uniform breach-handling contract for ops; Phase-8 lean-evals have a defined pressure-test surface. Candidates that pre-declare fan-out multipliers (GF-M Regime-A) catch cost-stacking math at architecture-spec time rather than at first cap-breach.

**Harder:** Each candidate's architecture spec carries an explicit per-regime cap-table — non-trivial authoring work in Phase 6. Methodology shapes that resist quantification (operator-judgment-heavy cycles) need to either name a wall-clock cap as a proxy or explicitly accept the F53 risk in their architecture spec.

**Explicitly NOT promising:** specific cap *values*. This discipline is a contract shape, not a numerical recommendation; values are per-deployment and live in the architecture spec.

## References

- [Cost-ceiling discipline write-up](../../architectures/v3/disciplines/cost-ceiling.md)
- [Disciplines index](../../architectures/v3/disciplines/index.md)
- [P-02 cost-ceilings substrate primitive sketch](../../architectures/v3/primitives/cluster-C1.md)
- [Regime classification discipline](../../architectures/v3/disciplines/regime-classification.md)
- [GF-M cost-ceiling × paraphrase-fan-out interaction](../../architectures/v3/tracks/greenfield-methodology-first.md)
- [auto-005 Round 2 Phase-5 dispatch shape](../../architectures/v3/decisions/auto-005-phase-5-dispatch-shape.md) — this ADR is the Wave-5.2 exemplar.
