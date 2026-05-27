---
candidate: gf-m
candidate-name: Greenfield methodology-first (two-regime reversible-commitment factory)
mandate-scope: greenfield
based-on-commit: c54daf1
based-on-date: 2026-05-26
mandate-fit:
  initial-spec: greenfield
  refactor: silent
  mvp: greenfield
  post-mvp-evolution: greenfield
  regression-fix: greenfield
---

# Architecture spec — GF-M (Greenfield methodology-first)

## §0 ADR-citation index

| ADR ID | Title | Layer | Variant of | Citing § |
|---|---|---|---|---|
| 0010 | P-01 Sandbox runtime | common-substrate | — | §2, §4 |
| 0011 | P-02 Cost ceilings | common-substrate | — | §2, §3, §4 |
| 0012 | P-05 Trajectory capture | common-substrate | — | §2, §3, §4 |
| 0013 | P-06 Watchdog tiers | common-substrate | — | §2, §3, §4 |
| 0014 | P-07 Telemetry ingestor | common-substrate | — | §2, §4 |
| 0015 | P-08 Scenario storage with runner contract | designed-system-substrate | — | §2, §3, §4 |
| 0016 | P-14 Judge router | common-substrate | — | §2, §3, §4 |
| 0017 | P-22 Polyglot codebase index | common-substrate | — | §2 |
| 0018 | Discipline — bias guard | discipline | — | §4 |
| 0019 | Discipline — cognitive escrow | discipline | — | §4 |
| 0020 | Discipline — cost ceiling | discipline | — | §4 |
| 0021 | Discipline — holdout | discipline | — | §4 |
| 0022 | Discipline — honesty | discipline | — | §4 |
| 0023 | Discipline — knowledge promotion | discipline | — | §4 |
| 0024 | Discipline — regime classification | discipline | — | §4 |
| 0025 | Discipline — scoping | discipline | — | §4 |
| 0026 | Discipline — three-loop | discipline | — | §4 |
| 0027 | Discipline — trifecta closure | discipline | — | §4 |
| 0040 | GF-M P-20 reversibility primitive | orphan-substrate | — | §2, §3 |
| 0041 | GF-M P-21 paraphrase divergence primitive | orphan-substrate | — | §2, §3, §6 |

**No framework-ADR claims.** GF-M does not claim any of P-19 (ADR 0028), P-28 (ADR 0029), P-29 (ADR 0030), or P-30 (ADR 0036) frameworks — substrate-requirements §3 explicitly establishes this ("GF-M does not name any of P-28, P-29, P-30, or P-19"). The Variant-of column is empty for every row by design. GF-M's distinctive minimalism is the *absence* of contested-primitive references: the cycle's gates are encoded directly in P-08 holdout policy, P-21 paraphrase divergence, and P-20 reversible commit/reverse semantics — no decision-table classifier framework and no typed-envelope store are required. The framework-ADR scope-boundary discipline ([AGENTS-MD-a9fb7b42f8](../../../AGENTS.md#framework-adr-scope-boundary-discipline)) therefore imposes no pairing obligation on this spec.

## §1 Overview

**Mandate.** Greenfield-only. The candidate's organising claim is that the per-cycle process *is* the architecture; the substrate is whatever the chosen cycle shape *requires*, not vice-versa (per [greenfield-methodology-first §0](../tracks/greenfield-methodology-first.md)).

**Axis.** Methodology-first. The cycle shape is the load-bearing decision layer. Two regimes — *Regime A* (spec-discovery, L3 augmentation) and *Regime B* (spec-anchored execution, L4 lights-out on promoted slices) — are run as distinct work-unit classes with different gates, different judges, and different exit criteria. The split is itself the architecture.

**Entry-mode.** Greenfield-only cold-start. Day-0 state: an operator with a prose-shaped domain idea + adjacent-domain priors, no codebase, no scenarios, no issue queue. The factory begins in Regime A only; Regime B starts running once the first slice promotes. Per substrate-requirements §4, GF-M does not acquire a Codebase Model from legacy artifacts — `X_UNM_B` is N/A by mandate.

**Methodology summary.** Thin-substrate, methodology-dominates. Each Regime-A cycle is a four-phase commitment loop: (1) operator dictates intent + EARS-linted acceptance-criteria block; (2) N model-family-diverse paraphrasers restate the intent and disagreement is the contradiction signal; (3) a fidelity-1 tiny probe surfaces what paraphrase missed; (4) operator promote-or-reverse. Reversal is cheap by design — the substrate's P-20 reversibility primitive (sub-ms event-sourced persist) makes the malleable phase *productive* rather than paralytic. Regime B inherits the Compound-Engineering loop with a mandatory cross-model review panel.

**Load-bearing claim.** GF-M's central wager is that *paraphrase divergence across N model-family-diverse paraphrasers is a stronger F37 (silent contradictory-prompt collapse) defense than any single LLM-judge*, because Larbi MCC ≤ 0.55 on single-judge contradiction-detection is treated as disqualifying (per [track §2.9](../tracks/greenfield-methodology-first.md)). The cycle's central gate is *behavioural disagreement across paraphrasers*, not judge confidence. This claim is empirically untested — Phase-8 lean-eval (per [§6](#6-open-carries)) is the falsification surface.

## §2 Substrate composition

GF-M's substrate is small by candidate design — 5 buildability-confirmed primitives plus the discipline ADRs. Per substrate-requirements §1, "GF-M requires 5 substrate primitives (cognitive-escrow primitive demoted to methodology-layer per [DEC-2](../phase-3.4-decisions-resolved.md#dec-2--cognitive-escrow-placement-methodology); not listed here)."

**Orphan substrate (single-candidate primitives).** Two ADRs carry the load-bearing primitives that no sibling candidate needs:

- **P-20 reversibility primitive** ([ADR 0040](../../../docs/adr/0040-p-20-reversibility-primitive.md)). Event-sourced storage of intent + scenario artifacts with sub-ms per-event persist. The substrate's job is *cheap commit-and-reverse* on the intent/scenario object pair so that Regime-A reversal is methodology-affordable. Per [P-20 sketch](../primitives/P-20-reversibility-primitive.md) and OpenHands V1 prior art, sub-ms persist is the warrant that reversible-commitment cycles are not cost-bound on the persistence layer; the cycle cost is dominated by paraphrase fan-out (see P-21), not reversibility. GF-M takes the default contract: ADR 0040 records the storage choice (EventStoreDB vs Postgres event_log alternate path, both append-only, content-addressed) as a deferred Phase-5 ADR seed per substrate-requirements §5.
- **P-21 paraphrase divergence primitive** ([ADR 0041](../../../docs/adr/0041-p-21-paraphrase-divergence.md)). N model-family-diverse paraphrasers callable in parallel via LiteLLM Router with cross-family tags + deterministic prompt-paraphrase generators via Jinja2 seeded macros + sentence-transformer divergence metric. GF-M's contract: N ≥ 3 (cross-family per [F46](../failure-modes-v3.md)); N, divergence-metric, and threshold are exposed as first-class first-class parameters per substrate-requirements §3 so the Phase-8 lean-eval calibration sweep is tractable. ADR 0041's calibration partial-RG flag is carried explicitly: the *construction* is `designed-system` (LiteLLM + asyncio.gather + sentence-transformers per [P-21 sketch](../primitives/P-21-paraphrase-divergence.md)); the *calibration* — choosing N, divergence-metric, and threshold against Larbi MCC ≤ 0.55 — is GF-M's own OQ-T6 and the load-bearing Phase-8 lean-eval candidate (see §6).

**Designed-system substrate (commodity-baseline candidate).** GF-M takes the default contract on the sole designed-system primitive shared with the common substrate baseline:

- **P-08 scenario storage with substrate-typed holdout** ([ADR 0015](../../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md)). Per substrate-requirements §3: "GF-M's contract: holdout enforcement is *substrate-typed*, not agent-policy. The sketch's default contract is OPA-mediated ABAC over `partition=train|holdout` with builder/judge role tokens (per [cluster-C3 § P-08](../primitives/cluster-C3.md)). GF-M takes this default as-is — the sketch's design content already meets GF-M's CTR-G2 mitigation requirement." Phase-5 ADR-seed carry: OPA-vs-Cedar policy-engine choice per substrate-requirements §5.

**Commodity substrate baseline.** Three commodity primitives consumed without candidate-specific contract delta beyond their sketch defaults — [P-01 sandbox runtime (ADR 0010)](../../../docs/adr/0010-p-01-sandbox-runtime.md), [P-02 cost ceilings (ADR 0011)](../../../docs/adr/0011-p-02-cost-ceilings.md), [P-06 watchdog tiers (ADR 0013)](../../../docs/adr/0013-p-06-watchdog-tiers.md). P-02 carries the candidate's known cost-multiplier (the per-Regime-A-cycle paraphrase fan-out is the dominant cost driver, ~N× single-cycle cost per [track §2.6](../tracks/greenfield-methodology-first.md), which is the methodology's explicit cost-vs-correctness trade per UC5). P-06's Patrol tier is load-bearing for the Regime-A→Regime-B transition (F34 cross-layer drift, F55 behavioural drift). Additional commodity primitives consumed: [P-05 trajectory capture (ADR 0012)](../../../docs/adr/0012-p-05-trajectory-capture.md) for cycle-event persistence, [P-07 telemetry (ADR 0014)](../../../docs/adr/0014-p-07-telemetry-ingestor.md) for Patrol-tier inputs, [P-14 judge router (ADR 0016)](../../../docs/adr/0016-p-14-judge-router.md) for the Regime-B cross-model review panel, and [P-22 polyglot codebase index (ADR 0017)](../../../docs/adr/0017-p-22-polyglot-codebase-index.md) for the Regime-B builder's tool surface once an artifact exists.

**No contested-primitive references.** GF-M's distinctive shape: the cycle does not require P-19 classifier dispatch (the Regime-A→B transition is *slice-coherence-based*, not feature-vector-classified), does not require a P-28 typed-envelope store (intent + scenario versions are event-sourced via P-20, not envelope-stored), does not require a P-29 policy mediator (holdout is OPA-on-P-08, not a separate policy primitive), and does not require a P-30 event registrar (Patrol-tier P-06 watches the trajectory stream directly). Per substrate-requirements §3: "No contested-primitive references. GF-M does not name any of P-28, P-29, P-30, or P-19 (the Phase-4.2 same-vs-distinct candidates). No fixed sub-section headers needed."

**X_UNM_B not applicable.** Per substrate-requirements §4: "`N/A (mandate-specific candidate; X_UNM_B does not apply)`. GF-M is greenfield-only (per [working definitions](../phase-3.4-decisions-resolved.md#working-definitions-greenfield-brownfield-entry-mode-framing)); it does not need to acquire a Codebase Model from legacy artifacts because its system originates inside the methodology."

## §3 Methodology shape

**Two regimes.** Per [track §1](../tracks/greenfield-methodology-first.md), the greenfield mandate is split into two regimes the cycle treats differently — the split is the architecture, not a stylistic preference.

**Regime A — Spec-discovery (the malleable phase).**

- *Operating mode.* L3 augmentation by default. Lights-out is explicitly *not* claimed in Regime A because the dominant failure modes (F36 instruction-following ceiling, F37 silent contradictory-prompt collapse, F41 under-defined intent debt, F39 point-spec/region-mismatch) are model-capability limits with empirically inadequate LLM-judge mitigation. The cycle's contract is to *make the spec converge fast enough that Regime B can run lights-out*, not to itself run lights-out.
- *Unit of work.* A *reversible commitment* — a hypothesis-shaped artifact pair: (a) an El Kaim 9-field intent block with `invariants` populated, (b) a paired Kaner out-of-tree scenario operationalising the intent. Both versioned. Both explicitly labelled `reversible` until promoted.
- *Cycle shape (4 phases).* (1) **Intent draft** — operator dictates prose; substrate produces an EARS-constrained acceptance-criteria block; deterministic GtWR R7/R8/R9 lint runs at this gate (failures returned to operator, not silently rewritten). (2) **Paraphrase divergence** — N independent model-family agents restate the intent ([P-21 (ADR 0041)](../../../docs/adr/0041-p-21-paraphrase-divergence.md)); behavioural disagreement at the post-condition level flags `underspecified` and returns to the operator. **This is the F37 defense.** Larbi MCC ≤ 0.55 single-judge contradiction-detection is treated as disqualifying. K=5 prompt-paraphrase robustness 3-of-5 (Jaymin Augmentation bar) is the empirical floor. (3) **Tiny probe** — one candidate scenario realised in the smallest possible working artifact (Schillace fidelity-1). The probe's job is to surface what paraphrase missed. (4) **Promote or reverse** — operator-judged thick signal; on reverse, the intent + scenario pair is *deleted* via [P-20 (ADR 0040)](../../../docs/adr/0040-p-20-reversibility-primitive.md), not amended. Reversal is cheap; that is what makes spec-malleable productive rather than paralytic.
- *Exit condition.* When the cumulative durable-intent set covers a coherent slice (criterion: at least one end-to-end scenario passes through the slice without an intent gap), the slice transitions to Regime B. Different slices transition at different times; Regimes A and B run concurrently after the first promotion. *Slice-coherence is an operationally-underdefined criterion* (OQ-T1; see §6) — a substrate-implementable check is owed at Phase-5/6 methodology spec, not at this substrate-composition layer.

**Regime B — Spec-anchored execution (the steady-state phase).**

- *Operating mode.* L4 lights-out on `regression-fix` and `post-mvp-evolution` work units operating on *promoted* slices. L3 augmentation on any work unit touching a still-`reversible` intent (the per-cycle mandate-fit declaration DEC-2 asks for).
- *Unit of work.* A scenario from the durable scenario set ([P-08 (ADR 0015)](../../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md); Kaner-shaped, out-of-tree, holdout-partitioned).
- *Cycle shape.* Standard Compound-Engineering loop (plan → work → review → compound, [report 03](../../../research/03-every-compound-engineering.md)) with one explicit modification: the review panel is **cross-model** (per F46 single-model review blindspot; CJ Hess `kevin/carl` pattern), *not* same-model — this contradicts CTR-D7 on the specific grounds that greenfield has no out-of-distribution ground truth. Routed via [P-14 (ADR 0016)](../../../docs/adr/0016-p-14-judge-router.md).
- *Empirical bar.* K=5 consistency ≥90% (Jaymin Automation bar); the cross-model review panel produces the K-sample continuously, so violations are caught in-cycle, not at audit time.

**Reversal as substrate primitive, not methodology promise.** The cycle's productivity in the malleable phase is purchased by sub-ms reversibility ([P-20](../../../docs/adr/0040-p-20-reversibility-primitive.md)), not by operator discipline. Reversal *is* the cycle's exit signal on probe-dissatisfaction — operator decisions are escrow-interval-shaped, not free-form.

**Patrol-tier monitoring as Regime-A→B drift detector.** [P-06 (ADR 0013)](../../../docs/adr/0013-p-06-watchdog-tiers.md) Patrol tier runs from day 0, watching for F55 behavioural drift and F34 cross-layer drift. The Regime-A→B regime change is exactly the kind of drift Patrol catches; substrate-enforced, not operator-voluntary.

**Day-0 to day-N trajectory.** Day-0 starts in Regime A only. Day 0 → T₁ (first slice promotion): Regime A only; cycle time dominated by operator reflection and paraphrase fan-out; throughput low *by design* (F25 design starvation is re-cast as a property of the regime, not a failure). Day T₁ → T₂: Regimes A and B run concurrently on different slices. Day T₂ onward: steady-state; Regime A continues for new slices (`post-mvp-evolution` work unit class). The transition is *slice-coherence-based*, not time-based — the methodology's answer to "when is the spec ready" is "not when complete, but when a slice is end-to-end coherent."

**No `docs/solutions/` accumulation in Regime A.** Self-referential drift (F55) is most acute at cold-start because all "knowledge" is from a tiny number of cycles. Knowledge promotion (ADR 0023 binding; see §4) begins only after Regime B has produced enough cycles to be evaluable.

## §4 Discipline binding

GF-M binds 9 of the 10 discipline ADRs (0018–0027); cognitive escrow is bound *at the methodology layer* per DEC-2 rather than as a substrate primitive. Per-discipline:

- **Bias guard ([ADR 0018](../../../docs/adr/0018-discipline-bias-guard.md)).** Bound at Regime-B's cross-model review panel and Regime-A's paraphrase step. Both enforce model-family diversity by construction (F46 mitigation). The cycle has *only one* deterministic wrapper (the GtWR linter at Phase 1) and one cross-model check (paraphrase divergence) — a deliberate guard against control-layer accretion per [track §2.9 F52](../tracks/greenfield-methodology-first.md).
- **Cognitive escrow ([ADR 0019](../../../docs/adr/0019-discipline-cognitive-escrow.md)).** Bound at the *methodology* layer (DEC-2 demotion), specifically at the Regime-A operator touchpoints (intent dictation, promote/reverse decision). Substrate surfaces reflection prompts in the interval; the prompt→response interval is designed substrate surface, not operator-voluntary discipline. F42, F53 mitigation.
- **Cost ceiling ([ADR 0020](../../../docs/adr/0020-discipline-cost-ceiling.md)).** Bound at [P-02 (ADR 0011)](../../../docs/adr/0011-p-02-cost-ceilings.md) with the Regime-A paraphrase fan-out (~N× single-cycle cost) admitted as the dominant cost-driver. CTR-E6 CaMeL utility-tax is acknowledged: substrate safety primitives have non-zero cost, and the ceiling must explicitly admit them. Phase-8 lean-eval candidate: paraphrase-fan-out × cost-ceiling interaction (OQ-T2).
- **Holdout ([ADR 0021](../../../docs/adr/0021-discipline-holdout.md)).** Bound at [P-08 (ADR 0015)](../../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md) substrate-typed holdout — *not* agent-policy. F28 mitigation. Greenfield specifically: scenarios are authored out-of-tree from day 0 (CTR-B5/CTR-G2 fragility flag does not bite greenfield).
- **Honesty ([ADR 0022](../../../docs/adr/0022-discipline-honesty.md)).** Bound at the Regime-A→B promotion gate (operator must *see* the paraphrase divergence vector; cannot promote on faith). The promote-or-reverse decision is the moment honesty becomes substrate-enforced rather than operator-voluntary.
- **Knowledge promotion ([ADR 0023](../../../docs/adr/0023-discipline-knowledge-promotion.md)).** Bound at the Regime-A→B slice transition. Pattern→standard promotion happens only after Regime B has produced enough cycles to evaluate. The deliberately *delayed* accumulation (no `docs/solutions/` in Regime A) is the candidate's distinctive F8/F55 mitigation.
- **Regime classification ([ADR 0024](../../../docs/adr/0024-discipline-regime-classification.md)).** Bound at the two-regime split itself. Regime A vs Regime B is the candidate's per-cycle declaration per DEC-2; no P-19 classifier framework is required because the regime label is determined by the work-unit's *target* (still-reversible intent → Regime A, promoted slice scenario → Regime B), not by a learned feature-vector.
- **Scoping ([ADR 0025](../../../docs/adr/0025-discipline-scoping.md)).** Bound at the slice-coherence transition criterion. Work-unit scope is bounded by the slice; cross-slice work is itself a Regime-A authoring concern, not a Regime-B execution concern.
- **Three-loop ([ADR 0026](../../../docs/adr/0026-discipline-three-loop.md)).** Bound at the Regime-B Compound-Engineering loop (plan → work → review → compound). The "compound" step is materialised as Patrol-tier monitoring of the slice-coherence and paraphrase-divergence distributions — meta-loop closure is substrate-enforced via [P-06 (ADR 0013)](../../../docs/adr/0013-p-06-watchdog-tiers.md) + [P-07 (ADR 0014)](../../../docs/adr/0014-p-07-telemetry-ingestor.md), not operator-voluntary.
- **Trifecta closure ([ADR 0027](../../../docs/adr/0027-discipline-trifecta-closure.md)).** Bound at [P-08 (ADR 0015)](../../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md) holdout + the GtWR linter at Phase 1. Both substrate-enforced. F44 lethal-trifecta production-scissors is substrate-default-off per [track §1.4](../tracks/greenfield-methodology-first.md); methodology does not relax it.

**Disciplines GF-M is NOT silent on but does not own.** None — GF-M carries all 10 disciplines, with cognitive escrow at the methodology layer rather than the substrate layer per DEC-2. No discipline is rejected.

## §5 Mandate fit

GF-M's mandate-fit YAML block (in this spec's frontmatter) restated per work-unit-class:

- **initial-spec: greenfield.** Initial-spec authoring is exactly what Regime A is shaped for. Day-0 cold-start operates against the operator-authored intent block (the day-0 frozen anchor); paraphrase divergence + tiny-probe + promote-or-reverse is the cycle. Substrate evidence: [ADR 0040](../../../docs/adr/0040-p-20-reversibility-primitive.md) (cheap reversal), [ADR 0041](../../../docs/adr/0041-p-21-paraphrase-divergence.md) (F37 defense), [ADR 0015](../../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md) (out-of-tree scenarios from day 0). Falsifying scenario: if Regime-A cycles cannot promote *any* slice across a multi-month run, the cold-start trajectory is broken and the two-regime split is unproductive on greenfield.

- **refactor: silent.** GF-M takes no position on `refactor` work units. Refactor presupposes an existing codebase against which the proposed change is sized — GF-M's day-0 entry-mode is greenfield-only, and `refactor` becomes a `post-mvp-evolution` sub-case once an artifact exists. The candidate's track explicitly names brownfield as out-of-scope per [track §6](../tracks/greenfield-methodology-first.md). Silence (not n/a) per the dispatch brief's token semantics: GF-M has no claim, not a deliberate rejection.

- **mvp: greenfield.** MVP authoring is the canonical Regime-A→Regime-B trajectory. Day 0 = first Regime-A intent dictation; T₁ = first slice promotes (the MVP's first end-to-end-coherent surface); T₂ = MVP shipping when enough slices have promoted to cover the operator's MVP envelope. Substrate evidence: same as initial-spec. Falsifying scenario: if Regime-A cycles accumulate intents indefinitely without slice-coherence, the MVP is never shippable and the candidate's earned-lights-out claim collapses.

- **post-mvp-evolution: greenfield.** Post-MVP cycles operate against a thickened durable-intent set + a populated durable-scenario set. Regime A continues to expand the durable spec for new slices while Regime B handles steady-state execution on already-promoted slices. Substrate evidence: [ADR 0040](../../../docs/adr/0040-p-20-reversibility-primitive.md) + [ADR 0015](../../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md) + [ADR 0016 P-14](../../../docs/adr/0016-p-14-judge-router.md) (cross-model review). Falsifying scenario: if post-MVP work units re-enter Regime A at a rate indistinguishable from cold-start, Regime B has not in fact become steady-state and the two-regime claim is wrong.

- **regression-fix: greenfield.** Regression fixes operate against the durable scenario set (the failing scenario *is* the anchor; the fix is a Regime-B work unit). L4 lights-out by construction because the scenario is promoted. Substrate evidence: [ADR 0015 P-08 (ADR 0015)](../../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md) holdout + [ADR 0021 holdout discipline](../../../docs/adr/0021-discipline-holdout.md). Falsifying scenario: if regression-fix cycles routinely surface intent ambiguities (returning to Regime A), the durable-intent boundary was drawn too tight and slice-coherence was insufficient at promotion.

**DEC-1.a falsifier-discipline observation.** GF-M claims `greenfield` on 4 of 5 work-unit classes (initial-spec, mvp, post-mvp-evolution, regression-fix) and `silent` on refactor. No `both` claims — this is evidence *for* the no-methodology-serves-both-mandates working hypothesis per [DEC-1.a](../decisions-captured.md#d1--unification-verdict-no-methodology-serves-both-mandates-working-hypothesis-falsifiable-by-phase-8). The Phase-8 lean-eval will pressure-test these claims by attempting brownfield deployment and observing whether the slice-coherence transition criterion can be applied retroactively to an existing codebase (per [§6](#6-open-carries)).

## §6 Open carries

Surfaced into Phase 7 (back-fill audit) / Phase 8 (lean-eval) / future Phase-5 ADRs:

- **P-21 calibration sweep — biggest single OQ (Phase-8 lean-eval; GF-M's own OQ-T6).** Per substrate-requirements §2 partial-RG flag and §5: choose `N × divergence-metric × threshold` against Larbi MCC ≤ 0.55 such that paraphrase divergence is empirically adequate as the F37 contradiction-detection defense. The substrate exposes these three parameters as first-class per [ADR 0041](../../../docs/adr/0041-p-21-paraphrase-divergence.md). The empirical question — whether paraphrase divergence has its own MCC ceiling for contradiction detection that the corpus does not yet measure — is the candidate's load-bearing falsification surface. **Status: accepted-as-RG-calibration; Phase 8 pressure-tests degradation.**

- **Slice-coherence operational definition (Phase-5/6 methodology-spec carry; OQ-T1).** "End-to-end scenario passes through the slice without intent gap" is a verbal criterion. A substrate-implementable check is owed at the methodology-spec layer — candidate: re-run paraphrase divergence at slice scope. Empirical calibration needed.

- **Paraphrase fan-out × cost-ceiling interaction (Phase-8 lean-eval candidate; OQ-T2).** Regime-A's ~N× single-cycle cost multiplied by D-5 caps yields a sharply-bounded throughput. CTR-E1's 10× cost-range with no methodology-side resolution exacerbates this. **Status: Phase-8 carry.**

- **Regime-A→B handoff substrate protocol (Phase-5 ADR seed; OQ-T3).** Closest corpus analog is C16 trajectory replay, but slice-promotion is a spec-layer transition, not a runtime replay. ADR question: is a new primitive needed, or can the transition be expressed on top of [P-05 trajectory (ADR 0012)](../../../docs/adr/0012-p-05-trajectory-capture.md) + [P-08 holdout (ADR 0015)](../../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md)?

- **Cross-model paraphrase × provider-abstraction interaction (Phase-5 ADR seed; OQ-T4).** GF-M requires multi-provider *capability* (model-family diversity) but is agnostic on RouterLLM-vs-provider-aligned-profiles. If CTR-C4 resolves toward per-provider profiles, paraphrase cost rises (separate harnesses per provider). The [P-21 sketch](../primitives/P-21-paraphrase-divergence.md)'s LiteLLM-router default is GF-M's working assumption; ADR formalisation owed.

- **Two-regime split as falsifiable design claim (OQ-T5).** A single-regime greenfield architecture might exist that carries spec-malleability through the whole cycle without the promote/reverse distinction. The split is GF-M's *answer* to F40 last-mile drift (the slice promotion is the "shipped" transition); Phase-3 adversarial pass on continuous-Regime-A-only is the falsification surface.

- **Brier pace-layer subsumption (Phase-7 back-fill carry).** GF-M does not claim Brier pace-layers as substrate — slice-coherence is the only spec-layer transition concept. Phase-7 back-fill audit: does GF-M's slice-coherence subsume Brier's pace-layers, or is it a strictly weaker re-encoding?

## §7 References

**ADR set (this spec's binding inputs).** Per the §0 ADR-citation index above; relative paths under `../../../docs/adr/`:

- Common substrate: [ADR 0010](../../../docs/adr/0010-p-01-sandbox-runtime.md), [ADR 0011](../../../docs/adr/0011-p-02-cost-ceilings.md), [ADR 0012](../../../docs/adr/0012-p-05-trajectory-capture.md), [ADR 0013](../../../docs/adr/0013-p-06-watchdog-tiers.md), [ADR 0014](../../../docs/adr/0014-p-07-telemetry-ingestor.md), [ADR 0016](../../../docs/adr/0016-p-14-judge-router.md), [ADR 0017](../../../docs/adr/0017-p-22-polyglot-codebase-index.md).
- Designed-system substrate: [ADR 0015 (P-08)](../../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md).
- Orphan substrate (GF-M-specific): [ADR 0040 (P-20 reversibility primitive)](../../../docs/adr/0040-p-20-reversibility-primitive.md), [ADR 0041 (P-21 paraphrase divergence)](../../../docs/adr/0041-p-21-paraphrase-divergence.md).
- Discipline: [ADR 0018](../../../docs/adr/0018-discipline-bias-guard.md), [ADR 0019](../../../docs/adr/0019-discipline-cognitive-escrow.md), [ADR 0020](../../../docs/adr/0020-discipline-cost-ceiling.md), [ADR 0021](../../../docs/adr/0021-discipline-holdout.md), [ADR 0022](../../../docs/adr/0022-discipline-honesty.md), [ADR 0023](../../../docs/adr/0023-discipline-knowledge-promotion.md), [ADR 0024](../../../docs/adr/0024-discipline-regime-classification.md), [ADR 0025](../../../docs/adr/0025-discipline-scoping.md), [ADR 0026](../../../docs/adr/0026-discipline-three-loop.md), [ADR 0027](../../../docs/adr/0027-discipline-trifecta-closure.md).

**Supporting docs:**

- [GF-M candidate-registry entry](../candidate-registry.md#gf-m--greenfield-methodology-first)
- [GF-M substrate-requirements summary](../substrate-requirements/gf-m.md)
- [Greenfield-methodology-first track sketch](../tracks/greenfield-methodology-first.md)
- [P-20 reversibility primitive sketch](../primitives/P-20-reversibility-primitive.md)
- [P-21 paraphrase divergence primitive sketch](../primitives/P-21-paraphrase-divergence.md)
- [DEC-1.a unification-verdict working hypothesis](../decisions-captured.md#d1--unification-verdict-no-methodology-serves-both-mandates-working-hypothesis-falsifiable-by-phase-8)
- [DEC-2 mandate-fit-per-(architecture × work-unit-class)](../decisions-captured.md#d2--mandate-fit-is-per-architecture--work-unit-class-not-per-architecture)
- [auto-006 Phase-6 dispatch-shape brief](../decisions/auto-006-phase-6-dispatch-shape.md) — this spec is authored under its Round-2 rubric.
- [U-C exemplar spec](./u-c.md) — Phase-6 format model.
