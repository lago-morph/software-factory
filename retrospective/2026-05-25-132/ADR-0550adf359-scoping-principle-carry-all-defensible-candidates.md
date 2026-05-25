# ADR: Scoping principle for research-synthesis methodology: carry all defensible candidates

- **ID**: ADR-0550adf359
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-25
- **Source retrospective**: ../2026-05-25-132.md
- **PRs covered**: #132

## Context

The v3 architecture-synthesis methodology was originally framed (in the Phase-3.4 integration brief) as a winner-picking exercise: at the Phase-3.4 checkpoint, the user would pick one of: 1 unified architecture / 2 separate architectures / 2 unified candidates / defer. The session surfaced a fundamental problem with this framing.

The corpus that feeds factory-architecture synthesis contains no validated working software factory. Authors of source documents — company blogs, white papers, books — have incentives to convince audiences that their approach works; what they describe is not the same as a deployed factory that produces working software at industrial scale. Under those conditions, eliminating promising candidates at the end of Phase 3 forecloses *crossover opportunities*: cases where a piece of one candidate's architecture turns out to be exactly the missing piece that another candidate proposed in a more awkward way. The information value of preserving multiple candidates through pressure-testing (Phase 8 lean-evaluation, downstream simulation, mock-up evaluation) is higher than the cost of carrying them.

The user declared this an immutable scoping principle during the session and noted: "Trying at this point to eliminate promising candidates is exactly the opposite of what we are trying to do."

## Decision

**Research-synthesis pipelines that evaluate multiple candidate architectures will not eliminate candidates at intermediate phases; each candidate that successfully defends itself against critique carries forward through later phases, with elimination deferred to the empirical evaluation stage.**

A candidate is "carried forward" when (i) each adversarial-critique finding against it is either addressed in the candidate's own material or explicitly accepted as an open concern; (ii) the candidate has produced buildability sketches for its substrate-primitive requirements (or those sketches are queued as Phase-3.5 work); (iii) its load-bearing claims are corpus-grounded.

## Alternatives considered

- **Pick a small set (1-3 candidates) at end of Phase 3.** Rejected because the corpus does not provide evidence sufficient to declare a winner; choosing too early loses optionality without earning information.
- **Carry all candidates regardless of defense status.** Rejected because un-defended candidates pollute the downstream comparison surface — they take up evaluation budget without earning their place.
- **Run only a single Phase-2 fanout track per mandate (no 9-track parallelism).** Rejected at the methodology-design stage; the deliberate divergence in Phase 2 is what produces the candidate diversity to evaluate downstream.

## Consequences

**Easier.** Crossover insights become possible — pieces of one candidate can be lifted into another at Phase 5+ if the buildability sketches show synergy. The Phase-8 lean-evaluation surface becomes the primary differentiation point, which is the right place for empirical claims to land. UC4 (the user's hypothesis that no single architecture serves both mandates) becomes empirically testable rather than logically forced.

**Harder.** Phase 4 substrate/divergence extraction operates over potentially 10+ candidates instead of 3. Phase 5 ADR count grows (some ADRs apply per-candidate). Phase 6 architecture specs are authored per surviving candidate. Phase 7 back-fill audit runs per candidate. Phase 8 lean-eval briefs are per candidate. The maintenance burden of the catalog rises.

**Accepted trade-off.** Higher Phase-4-onward authoring cost in exchange for preserving optionality. The user explicitly accepted this: the cost of carrying candidates through lean-evaluation is "tokens"; the cost of eliminating prematurely is potentially the wrong architecture for thousands of hours of downstream work.

## References

- [`../2026-05-25-132.md`](../2026-05-25-132.md) — source retrospective.
- [`./SKILL-SPEC-1232311024-candidate-registry.md`](./SKILL-SPEC-1232311024-candidate-registry.md) — the candidate-registry skill captures the operational consequence: state-of-all-candidates lookup so downstream sessions can pick up cold.
- PRs the decision was made in: #132.

<!--
PROMOTION NOTE: this decision applies at the methodology level (governs research-synthesis pipelines), not at the v3-instance level. If adopted, the ADR lives in `docs/adr/` as a binding choice that future synthesis runs inherit.
-->
