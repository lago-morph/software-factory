# ADR: Greenfield-to-brownfield continuity as primary Phase-4 design concern

- **ID**: ADR-ff2a376c34
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-25
- **Source retrospective**: ../2026-05-25-132.md
- **PRs covered**: #132

## Context

The original v3 synthesis plan structured Phase 4 ("Shared/divergent extraction") around two outputs: a shared-substrate document (what greenfield and brownfield architectures genuinely share) and a divergence document (where they genuinely diverge). The plan's framing was static — extract structural overlap, then proceed to ADRs.

The user reframed DEC-1 (the unification verdict) at session end. Their hypothesis: no methodology serves both greenfield and brownfield together; substrates and disciplines/philosophy *do* fit both mandates; the differentiator is the methodology layer. Crucially: **greenfield efforts eventually turn into maintaining an active codebase.** A factory that ran greenfield will, when the codebase matures, transition to brownfield work without changing architecture — same substrate, same disciplines, switch the methodology layer. The transition is structural, not optional.

This reframe surfaces a Phase-4 output the original plan did not name: an explicit **continuity matrix** — which greenfield-methodology outputs become brownfield-methodology inputs. Without this, the substrate / discipline / methodology split doesn't tell the operator "if my greenfield methodology produces artifacts X, Y, Z, my brownfield methodology can immediately consume them; if it produces only A, B, the brownfield methodology has to re-derive C from archaeology." The continuity story is the load-bearing operational concern for factories that are expected to outlive their initial greenfield phase.

## Decision

**Phase 4 of a factory-architecture synthesis must explicitly extract, as a first-class output alongside the shared-substrate and divergence documents, a continuity matrix specifying which greenfield-methodology outputs become brownfield-methodology inputs.** Phase 4 produces four documents (not the original two): (a) shared-substrate inventory with buildability per primitive; (b) shared-discipline inventory; (c) divergence document; (d) **greenfield → brownfield continuity matrix**.

A continuity-compatible greenfield methodology is one whose typed, versioned, queryable outputs (intent blocks, evaluation suites, RSI declarations, trajectory histories, scenario stores, classifier baselines) align with the input contracts of one or more brownfield methodologies. Continuity becomes a Phase-4 evaluation criterion: greenfield candidates that produce continuity-compatible artifacts are stronger; those that do not lose the continuity benefit and the factory's lifecycle cost rises (because brownfield work must re-derive what greenfield could have produced as a side effect).

## Alternatives considered

- **Treat continuity as a Phase-6 architecture-spec concern (per-spec).** Rejected because by Phase 6, the substrate and methodology choices are locked; if a methodology was chosen without continuity in mind, retrofitting at the spec layer is much more expensive than designing it in at Phase 4.
- **Treat continuity as an implicit consequence of the substrate/methodology split.** Rejected because the substrate/methodology split alone is silent on artifact contracts between mandates; without an explicit matrix, there's no mechanism to surface continuity gaps.
- **Defer continuity to a post-synthesis lifecycle ADR.** Rejected for the same reason as the Phase-6 option — too late to influence methodology design.

## Consequences

**Easier.** Phase 6 architecture specs can name their continuity profile explicitly: "this greenfield architecture produces these artifacts that satisfy these brownfield-methodology input contracts." Phase 8 lean-evaluation can include a "now operate this as if the codebase is mature" exercise to test continuity empirically. Operators choosing between candidate factories have continuity as a comparison axis.

**Harder.** Phase 4 grows by one substantial document. Some greenfield candidates may turn out to be continuity-incompatible and lose evaluation points — which is information value, but also a constraint on the methodology proposer's design freedom. The substrate/discipline/methodology split becomes more intricate (the continuity matrix references all three layers).

**Accepted trade-off.** One additional Phase-4 document in exchange for surfacing the most important operational concern factory operators will face: how the factory's lifecycle handles the greenfield-to-brownfield transition.

## References

- [`../2026-05-25-132.md`](../2026-05-25-132.md) — source retrospective.
- [`../../architectures/v3/candidate-registry.md`](../../architectures/v3/candidate-registry.md) — the greenfield-to-brownfield continuity table at the end of the candidate registry; concrete worked example of the matrix this ADR formalizes.
- [`../../architectures/v3/SESSION-HANDOFF-2026-05-25-phase-3.4-close.md`](../../architectures/v3/SESSION-HANDOFF-2026-05-25-phase-3.4-close.md) — handoff doc captures the DEC-1 reframe that motivates this ADR. (Renamed from `SESSION-HANDOFF-2026-05-25.md` at Phase-3.5 close.)
- [`./ADR-0550adf359-scoping-principle-carry-all-defensible-candidates.md`](./ADR-0550adf359-scoping-principle-carry-all-defensible-candidates.md) — the scoping principle that keeps multiple greenfield + brownfield candidates alive; continuity matrix is a comparison across them.
- PRs the decision was made in: #132.
