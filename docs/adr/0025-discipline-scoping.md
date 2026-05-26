# ADR 0025: Discipline — scoping

- **Status**: Accepted
- **Date**: 2026-05-25
- **Deciders**: lead agent (Phase 5 Wave 5.2)

## Context

Scoping appears in every surviving candidate's substrate-requirements summary as a **process discipline** binding how the synthesis pipeline treats candidates across Phases 4–8. The [disciplines index](../../architectures/v3/disciplines/index.md) names scoping as one of 21 canonical disciplines (entry `D-Scoping`); the per-discipline write-up at [`disciplines/scoping.md`](../../architectures/v3/disciplines/scoping.md) describes it as "the most process-shaped of the inventory."

Unlike the other Wave-5.2 disciplines (cost-ceiling, bias-guard, cognitive-escrow), scoping does not bind a substrate primitive. It binds the **lead agent's authorship behavior** across phases. The forcing concern: no public source has detailed a working software-factory architecture, so narrowing to a small candidate set at end-of-Phase-3 forecloses crossover opportunities where pieces of one candidate turn out to be the missing piece for another. Pressure-testing must happen on empirical surfaces (Phase-8 lean-evals, downstream simulation), not on the lead agent's pre-empirical preference.

The principle was declared by the user 2026-05-25 in [phase-3.4-decisions-resolved.md](../../architectures/v3/phase-3.4-decisions-resolved.md#scoping-principle-immutable-overrides-any-conflicting-framing-in-the-integration-brief) and marked immutable. This ADR records the operational contract that downstream phases inherit.

## Decision

**The scoping discipline binds the synthesis pipeline to carry every defensible candidate forward; elimination decisions are deferred until empirical pressure-testing produces evidence.** Per the binding rule table ([AGENTS-MD-bf4431be57](../../architectures/v3/phase-3.4-decisions-resolved.md#scoping-principle-immutable-overrides-any-conflicting-framing-in-the-integration-brief)), the user-declared principle reads verbatim:

> **Carry forward every candidate methodology / architecture that has defensible supporting arguments and that successfully addressed Phase-3.2 / Phase-3.3 criticism. Do not eliminate at end-of-Phase-3.**

Operationalized across downstream phases:

- **Phase 4** — substrate-requirements summaries are authored *per surviving candidate*. "Shared substrate" extraction is reframed as primitive-overlap analysis for tooling-decision support, not as a winner-picking exercise. Summaries MUST NOT pre-eliminate candidates by collapsing variation into a single recommended shape.
- **Phase 5** — ADRs preserve per-candidate variation. Where candidates agree, the ADR is shared and cross-referenced; where they diverge, separate ADRs (or an explicit per-candidate section) record the variation rather than picking a winner.
- **Phase 6** — one architecture spec per surviving candidate; the mandate-fit matrix has a row per candidate. No down-selection.
- **Phase 8** — lean-eval briefs are per-candidate and constitute the empirical pressure-test surface where elimination decisions become evidence-grounded.

Critiques (Phase-3.2 persona-adversarial, Phase-3.3 D7 blind-axis) are reframed: each critique is material for *"what must this candidate address before it carries forward?"*, not *"should this candidate demote?"*. A candidate whose critique findings have been addressed (or whose authors have given substantive defense) carries forward.

## Alternatives considered

**B. End-of-Phase-3 elimination (narrow to 1–3 candidates before Phase 4).** *Why rejected:* premature and pre-empirical. The user's rationale, recorded in [phase-3.4-decisions-resolved.md](../../architectures/v3/phase-3.4-decisions-resolved.md#scoping-principle-immutable-overrides-any-conflicting-framing-in-the-integration-brief): no public source has given details of a software-factory architecture/methodology that actually works; company blogs, white papers, and books are written by authors with incentives to convince. Narrowing on lead-agent judgment alone forecloses crossover (pieces of one candidate becoming the missing piece for another) and bakes in the lead agent's anchoring biases at the moment they have the least counter-pressure. The empirical pressure-test surface (Phase-8 lean-evals + downstream simulation) is where elimination belongs.

**C. Evidence-gated elimination at every phase (allow demotion as soon as any phase produces a negative signal).** *Why rejected:* the same problem at smaller scale. Each phase's outputs are still authored under lead-agent framing pressure; "evidence" produced inside the pipeline before Phase 8 is structurally the lead agent's own pattern-matching, not empirical pressure-testing. Allowing demotion at any phase reintroduces the elimination dynamic the scoping principle forbids, just spread thinner. See [`disciplines/scoping.md`](../../architectures/v3/disciplines/scoping.md) "Phase-3 does not eliminate candidates… pressure-testing happens at Phase-8 lean-eval and downstream simulation."

## Consequences

**Easier:** Phase-8 lean-evals have a richer candidate set to pressure-test (10 candidates per [DEC-1.c](../../architectures/v3/phase-3.4-decisions-resolved.md)); crossover opportunities remain visible because no candidate is removed before its parts can be recombined; lead-agent anchoring on a favorite candidate is structurally defused. D7-style "carry both" verdicts ([`d7-u-1-prohibit-interval-escrow.md`](../../architectures/v3/bias-guards/phase-3/d7-blind-axis/d7-u-1-prohibit-interval-escrow.md)) become routine rather than exceptional.

**Harder:** Phase-4 / Phase-5 / Phase-6 authoring volume scales linearly with surviving-candidate count. The lead agent must resist a strong gravitational pull toward shared "executive-summary" framings that implicitly down-select. Phase-5 ADR authors must check, per ADR, that per-candidate variation is preserved where real.

**Explicitly NOT promising:** numerical cap on candidate count. The principle is "however many can pass review and pressure-testing make a strong case for being evaluated," not "narrow to 1–3." If a future Phase-8 lean-eval falsifies a candidate empirically, that candidate exits; the discipline does not protect candidates from evidence, only from premature lead-agent judgment.

## References

- [Scoping-principle discipline write-up](../../architectures/v3/disciplines/scoping.md)
- [Phase-3.4 scoping principle (binding, immutable)](../../architectures/v3/phase-3.4-decisions-resolved.md#scoping-principle-immutable-overrides-any-conflicting-framing-in-the-integration-brief)
- [Disciplines index — D-Scoping entry](../../architectures/v3/disciplines/index.md)
- [DEC-3 greenfield candidate set decision](../../architectures/v3/decisions/dec-3-greenfield-methodology.md)
- [DEC-4 brownfield candidate set decision](../../architectures/v3/decisions/dec-4-brownfield-methodology.md)
- [D7-U-1 "carry both" recommendation as scoping-principle application](../../architectures/v3/bias-guards/phase-3/d7-blind-axis/d7-u-1-prohibit-interval-escrow.md)
- [auto-005 Round 2 Phase-5 dispatch shape](../../architectures/v3/decisions/auto-005-phase-5-dispatch-shape.md)
