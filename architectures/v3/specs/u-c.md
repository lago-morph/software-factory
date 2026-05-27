---
candidate: u-c
candidate-name: Anchor-Distance Factory
mandate-scope: unified-attempt
based-on-commit: aa9d372
based-on-date: 2026-05-26
exemplar: true
exemplar-for: Phase-6 per-candidate spec authoring (auto-006 Round 2)
mandate-fit:
  initial-spec: brownfield
  refactor: both
  mvp: greenfield
  post-mvp-evolution: both
  regression-fix: both
---

# Architecture spec — U-C (Anchor-Distance Factory)

## §0 ADR-citation index

| ADR ID | Title | Layer | Variant of | Citing § |
|---|---|---|---|---|
| 0010 | P-01 Sandbox runtime | common-substrate | — | §2, §4 |
| 0011 | P-02 Cost ceilings | common-substrate | — | §2, §4 |
| 0012 | P-05 Trajectory capture | common-substrate | — | §2, §3, §4 |
| 0013 | P-06 Watchdog tiers | common-substrate | — | §2, §4 |
| 0014 | P-07 Telemetry ingestor | common-substrate | — | §2, §3 |
| 0015 | P-08 Scenario storage with runner contract | designed-system-substrate | — | §2, §4 |
| 0016 | P-14 Judge router | common-substrate | — | §2, §3 |
| 0017 | P-22 Polyglot codebase index | common-substrate | — | §2, §3 |
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
| 0028 | P-19 Eligibility / regime classifier framework | common-substrate | — | §2, §3 |
| 0029 | P-28 Typed-object store framework | common-substrate | — | §2, §3 |
| 0031 | P-23 Dependency-impact graph | common-substrate | — | §2, §3 |
| 0032 | P-12 Deterministic linter framework | common-substrate | — | §2, §4 |
| 0057 | P-32 Distance estimator | orphan-substrate | — | §2, §3 |
| 0058 | U-C P-19 variant — distance-tuple feature source | per-variant-substrate | 0028 | §2, §3 |
| 0059 | U-C P-28 variant — anchor envelope schema | per-variant-substrate | 0029 | §2, §3 |

**Framework + per-variant pairing check.** U-C claims frameworks 0028 (P-19) and 0029 (P-28); per [AGENTS-MD-a9fb7b42f8](../../../AGENTS.md#framework-adr-scope-boundary-discipline), each framework reference is paired with U-C's per-variant ADR — 0028 with 0058, 0029 with 0059. U-C does not claim frameworks 0030 (P-29 policy mediator) or 0036 (P-30 event registrar) as substrate primitives: U-C's anchor mutation queue is a typed-filter view over the P-28 substrate (per [u-c.md §3](../substrate-requirements/u-c.md)), not a separate P-29/P-30 binding. Mutation-protocol policy is encoded in the P-28 anchor envelope's `mutation-protocol` field (ADR 0059), enforced at write time by ADR 0029's envelope-registration contract.

## §1 Overview

**Mandate.** Unified-attempt. U-C carries both greenfield and brownfield mandates parameterised by the anchor's `kind` (intent-invariant vs architecture-rule / live-test / runtime-trace) rather than by the architecture's shape (per [unified-C §0](../tracks/unified-C.md)).

**Axis.** Distance-from-frozen-anchor — every work unit is parameterised by a single scalar: the graph distance between the change the work unit proposes and the nearest frozen anchor the architecture recognises. The axis is unified-defensible because the mandate becomes a *parameter* (the anchor's content) rather than the organising distinction.

**Entry-mode.** Either greenfield (cold-start: operator authors the intent block; first cycles are L4-by-construction; lights-out is *earned* by anchor accumulation) or brownfield (anchor set initially drawn from existing codebase + observable behaviour + slow-layer invariants — Brier "Architecture" and "Standards" pace-layers plus live test suite and runtime telemetry). Distance estimator works on either; X_UNM_B brownfield acquisition specified in §2.

**Methodology summary.** Substrate-heavy, thin-methodology. Per-cycle process is generic — agent receives a work unit + anchor set + computed DistanceTuple + dispatched regime. The Compound Engineering loop (plan → work → review → compound) is the default per-cycle methodology; Atelier-style queues and Attractor-style DOT pipelines are plug-in alternatives. The substrate's distance-gated dispatcher is the load-bearing decision layer; methodology decisions are downstream of distance.

**Load-bearing claim.** Anchor-distance is the substrate's first-class scalar. The dispatcher routes work units by distance regime. Mandate is parameterised by anchor `kind`. CTR-C2 ("substrate-heavy + thin-methodology") is the shape U-C defends, not avoids.

## §2 Substrate composition

U-C carries six substrate-layer ADRs beyond the common substrate baseline (0010-0017) and discipline ADRs (0018-0027):

**Framework substrate (with per-variant pairing per [AGENTS-MD-a9fb7b42f8](../../../AGENTS.md#framework-adr-scope-boundary-discipline)).** The Phase-4.2 [`overlap.md` verdict on P-19](../primitives/overlap.md#p-19-eligibility--regime-classifier--four-contested-variants) is verbatim:

> **"SAME primitive (P-19 classifier framework), DISTINCT feature sources + distinct output regime sets. All four share the construction recipe (Drools/OPA Rego decision tables + LLM-judge fallback via P-14 + OPA hard-floor post-check per [P-19 sketch](../../architectures/v3/primitives/P-19-eligibility-regime-classifier.md)). The differences are at the *feature engineering* layer and the *output enum* layer, not the *decision-engine* layer."**

The corresponding [`overlap.md` verdict on P-28](../primitives/overlap.md#p-28-typed-object-store--four-contested-variants) is verbatim:

> **"Verdict: SAME primitive (P-28 typed-object store framework), DISTINCT envelopes. All four share the construction recipe (libgit2 `git_odb_write` + `refs/notes/<envelope-kind>`; Postgres `bytea`+`jsonb`+GIN alternate path; content-addressed append-only with typed envelope per P-28 sketch). The envelope schemas are non-overlapping but the underlying primitive (typed envelope + content-hash + append-only + Glean/Postgres-compatible storage) is identical."**

Both verdicts bind U-C's spec to pair every framework ADR with its U-C per-variant ADR (per [AGENTS-MD-a9fb7b42f8](../../../AGENTS.md#framework-adr-scope-boundary-discipline) framework-ADR scope boundary). Concretely:

- **P-19 distance-gated dispatcher.** Framework: [ADR 0028](../../../docs/adr/0028-p-19-eligibility-regime-classifier.md) records the common decision-table engine (Drools / OPA Rego) + LLM-judge fallback via [P-14](../../../docs/adr/0016-p-14-judge-router.md) + OPA hard-floor post-check shared across four contested variants. U-C variant: [ADR 0058](../../../docs/adr/0058-p-19-variant-u-c-distance-tuple.md) records U-C's feature source as the [P-32](../../../docs/adr/0057-p-32-distance-estimator.md) DistanceTuple + `contradiction_flag` lifted from [P-07 telemetry](../../../docs/adr/0014-p-07-telemetry-ingestor.md), and output regime as `{lights-out, cross-model-judging, human-required}`. U-C names this primitive a *dispatcher* rather than *classifier* because P-32 has already done the feature engineering (the dispatcher's job is threshold logic on `w_g · graph_distance + w_p · pace_layer_crossings + w_i · intent_field_touches` plus the contradiction-flag hard floor — the F37 catch). Per [u-c.md §3 P-19 contract](../substrate-requirements/u-c.md), the dispatcher reads the DistanceTuple from P-32, computes the composite, applies thresholds `(τ_low, τ_high)`, and emits regime ∈ {lights-out, cross-model-judging, human-required} — but `contradiction_flag = true ⇒ human-required` regardless of composite.

- **P-28 anchor envelope.** Framework: [ADR 0029](../../../docs/adr/0029-p-28-typed-object-store.md) records the substrate decision (libgit2 `git_odb_write` + `refs/notes/<envelope-kind>` namespaces, or Postgres `bytea`+`jsonb`+GIN alternate path; content-addressed append-only) shared across four contested variants. U-C variant: [ADR 0059](../../../docs/adr/0059-p-28-variant-u-c-anchor-envelope.md) registers the `anchor` envelope-kind with schema `{kind, content, frozen-since, owning-mandate, mutation-protocol}` and typed-filter axis `kind × owning-mandate`. U-C's contract is **immutability-metadata-first** — `frozen-since` and `mutation-protocol` are first-class envelope fields participating in the content-hash preimage (silent re-dating is structurally impossible). Per [u-c.md §3 P-28 contract](../substrate-requirements/u-c.md), the typed filter is keyed on `kind × owning-mandate` and the anchor mutation queue is a typed-filter view over the same substrate (`kind=anchor-edit` envelopes with `proposed-content` + `target-anchor-hash`) — not a separate primitive.

**Orphan substrate (single-candidate primitive):**

- **P-32 distance estimator.** [ADR 0057](../../../docs/adr/0057-p-32-distance-estimator.md) records U-C's orphan: a multi-component typed estimator `distance(work-unit, anchor-set) → DistanceTuple{graph_distance, pace_layer_crossings, intent_field_touches, contradiction_flag}`. Three legs:
  - Structural leg (`graph_distance`): composes [P-22 polyglot codebase index](../../../docs/adr/0017-p-22-polyglot-codebase-index.md) + [P-23 dependency-impact graph](../../../docs/adr/0031-p-23-dependency-impact-graph.md) to compute symbol-reach × test-coverage.
  - Pace-layer leg (`pace_layer_crossings`): deterministic decision table mapping file globs to Brier pace-layers (per [unified-C §3](../tracks/unified-C.md)).
  - Semantic-touch leg (`intent_field_touches`): P-14-routed LLM judge against a stored `symbol → intent-field` map (this leg is F33/F51-vulnerable; see §6 open carries).
  - Contradiction flag (Boolean): set by the [P-07 telemetry ingestor](../../../docs/adr/0014-p-07-telemetry-ingestor.md) when the work unit's proposed change implies anchor mutation (the F37 catch).

**Distance-keyed P-05 (commodity primitive with U-C-specific contract on output schema):**

- [P-05 trajectory capture](../../../docs/adr/0012-p-05-trajectory-capture.md) is consumed unchanged at the substrate decision layer, but U-C extends the per-event payload with the DistanceTuple at write time. This is methodology-layer enrichment over a commodity substrate primitive — sub-ms persist cost per [P-05 ADR](../../../docs/adr/0012-p-05-trajectory-capture.md) is preserved.

**Commodity substrate baseline.** [P-01 sandbox](../../../docs/adr/0010-p-01-sandbox-runtime.md), [P-02 cost ceilings](../../../docs/adr/0011-p-02-cost-ceilings.md), [P-06 watchdog tiers](../../../docs/adr/0013-p-06-watchdog-tiers.md), [P-07 telemetry](../../../docs/adr/0014-p-07-telemetry-ingestor.md), [P-08 scenario storage](../../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md), [P-14 judge router](../../../docs/adr/0016-p-14-judge-router.md), [P-22 polyglot index](../../../docs/adr/0017-p-22-polyglot-codebase-index.md). P-06 is the Patrol-tier monitoring substrate for distance-distribution drift (F47 Goodhart-on-Tokens residual detector). P-12 [deterministic linter framework](../../../docs/adr/0032-p-12-deterministic-linter-framework.md) is consumed for anchor-content syntactic validation but not customised.

**X_UNM_B brownfield Codebase-Model acquisition** (per [u-c.md §4](../substrate-requirements/u-c.md)). For brownfield deployments, U-C needs the dependency graph + a pace-layer mapping. Both come from the **structural view portion** of BF-L's P-26 (covered by [P-22](../../../docs/adr/0017-p-22-polyglot-codebase-index.md) + [P-23](../../../docs/adr/0031-p-23-dependency-impact-graph.md), both designed-system, no RG flag inherited because U-C only depends on P-26's non-RG views). The anchor set is operator-authored at deployment time. The `intent_field_touches` leg is the load-bearing brownfield acquisition gap; if `intent_field_touches` cannot be computed (no synthesised intent block from legacy spec artifacts), the leg degrades to operator-attested with L3 dispatch fallback — graceful degradation, not silent failure.

## §3 Methodology shape

**Per-cycle loop.** Generic and thin. Each cycle:

1. **Work-unit declaration.** Agent (or operator) declares a typed work unit naming its target anchor set.
2. **Distance computation.** [P-32 distance estimator (ADR 0057)](../../../docs/adr/0057-p-32-distance-estimator.md) computes the DistanceTuple. Cost: substrate-driven, fanout into [P-22](../../../docs/adr/0017-p-22-polyglot-codebase-index.md) + [P-23](../../../docs/adr/0031-p-23-dependency-impact-graph.md) for the structural leg; [P-14 judge router](../../../docs/adr/0016-p-14-judge-router.md) for the semantic-touch leg.
3. **Regime dispatch.** [P-19 distance-gated dispatcher (ADR 0058)](../../../docs/adr/0058-p-19-variant-u-c-distance-tuple.md) evaluates composite + hard floors against the [P-19 framework (ADR 0028)](../../../docs/adr/0028-p-19-eligibility-regime-classifier.md) decision-table engine, emits regime label.
4. **Cycle execution.** Per the dispatched regime:
   - **Near-anchor (lights-out)**: substrate-enforced gates only — acceptance criteria (P-08 scenarios), holdout discipline (ADR 0021), bias guard (ADR 0018). Single-family model permitted per [Anthropic followup/07](../tracks/unified-C.md) where its conditions are met.
   - **Mid-distance (cross-model-judging)**: K=5 ≥70% Augmentation bar; paraphrase ≥3/5; cross-family judge required (F46 mitigation) via [P-14](../../../docs/adr/0016-p-14-judge-router.md).
   - **Far-anchor or anchor-edit (human-required)**: named-human L4 review; mandatory cooling-off windows on anchor-edit; Caremark-style immutable AILCCP logging.
5. **Trajectory write.** [P-05 (ADR 0012)](../../../docs/adr/0012-p-05-trajectory-capture.md) appends the cycle event with the DistanceTuple in the payload — Patrol-tier ([P-06 (ADR 0013)](../../../docs/adr/0013-p-06-watchdog-tiers.md)) monitors the empirical distance distribution.

**Regime structure** (per [unified-C §1](../tracks/unified-C.md)). Three regimes — near-anchor, mid-distance, far-anchor — separated by versioned thresholds `(τ_low, τ_high)` and weighted by `(w_g, w_p, w_i)`. Hard floors (per [ADR 0058](../../../docs/adr/0058-p-19-variant-u-c-distance-tuple.md) decision 3):
- `contradiction_flag = true ⇒ human-required` regardless of composite (F37 catch, supersedes rule-engine + LLM-judge).
- Cold-start cycle count `< N ⇒ augmentation-required` (F25 design-starvation mitigation).
- `kind = anchor-edit` target ⇒ `human-required` (the explicit re-entry mechanism per OQ-B3).

**Work-unit definition.** A *distance-typed proposed change* whose anchor set is named explicitly. Both Atelier-style issue work units and Refinery-style change-request work units are representable; dispatcher is front-end-agnostic. The unit-of-work cost ceiling is per-distance: near-anchor work has lower [P-02 (ADR 0011)](../../../docs/adr/0011-p-02-cost-ceilings.md) caps; anchor-edit work has the highest.

**Distinctive methodology decisions.** Three:

- **Anchor mutation is a substrate primitive, not a methodology promise.** Anchor edits are typed envelopes (`kind=anchor-edit` per [ADR 0059](../../../docs/adr/0059-p-28-variant-u-c-anchor-envelope.md)) routed through the dispatcher with mandatory L4 human review. Caremark/RSI exposure (F43) is structurally addressed by the AILCCP immutable log on the anchor mutation queue.

- **Day-0 → day-N trajectory is a distance-distribution shift, not a calendar date.** Cold-start cycles are L4-by-construction because no near-anchor anchors exist beyond the operator-authored intent block. Anchors accumulate via pattern → standard promotion (Brier pace-layers), first-passing tests becoming live-tests, ADRs becoming architecture-rules. Transition to steady-state is mechanical: when ≥X% of work-unit distance distribution sits at `d ≤ τ_low` for K consecutive cycles, the dispatcher begins to route those work units lights-out.

- **Methodology layer takes no opinion on coordination medium.** Mail-bus vs GitHub-issues vs commit-message is a methodology-layer detail orthogonal to substrate. U-C is agnostic; deployment chooses.

## §4 Discipline binding

U-C binds 9 of the 10 discipline ADRs (0018-0027); honesty is bound but with a candidate-specific carve-out (operator-legibility OQ-5). Per-discipline binding:

- **Bias guard ([ADR 0018](../../../docs/adr/0018-discipline-bias-guard.md)).** Bound at the dispatcher: cross-model judging at mid-distance enforces model-family diversity (F46 mitigation). Near-anchor work permits single-family per Anthropic followup/07.

- **Cognitive escrow ([ADR 0019](../../../docs/adr/0019-discipline-cognitive-escrow.md)).** Bound at the [P-05 (ADR 0012)](../../../docs/adr/0012-p-05-trajectory-capture.md) trajectory + Patrol-tier ([P-06 (ADR 0013)](../../../docs/adr/0013-p-06-watchdog-tiers.md)) tier. Kahana's "fragile dependency" framing is addressed structurally: the prompt→response interval is a designed substrate surface, not operator-voluntary discipline.

- **Cost ceiling ([ADR 0020](../../../docs/adr/0020-discipline-cost-ceiling.md)).** Bound at [P-02 (ADR 0011)](../../../docs/adr/0011-p-02-cost-ceilings.md) with per-distance parameterisation: near-anchor work has lower ceilings, anchor-edit work has the highest. CTR-E1 cost-variance is addressed by per-distance ceilings rather than a single global ceiling.

- **Holdout ([ADR 0021](../../../docs/adr/0021-discipline-holdout.md)).** Bound at [P-08 scenario storage (ADR 0015)](../../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md) — distance-gated dispatcher is the substrate-enforced holdout boundary; near-anchor work has acceptance criteria withheld by the dispatcher itself (D-4 substrate enforcement).

- **Honesty ([ADR 0022](../../../docs/adr/0022-discipline-honesty.md)).** Bound but with a candidate-specific carve-out: operator-legibility of the DistanceTuple at dispatch ([unified-C §7 OQ-5](../tracks/unified-C.md)) is the biggest single open question. If operators cannot see why a work unit was routed to lights-out vs Augmentation vs human-required, the substrate is opaque in exactly the way F42 (cognitive-escrow negligence) names. Carried as Phase-8 lean-eval candidate (§6).

- **Knowledge promotion ([ADR 0023](../../../docs/adr/0023-discipline-knowledge-promotion.md)).** Bound at the anchor mutation queue: pattern → standard promotion is the canonical knowledge-promotion path (Brier pace-layers). Each cycle's repeatable pattern is candidate for promotion to `anchor.kind=standards-rule`. Promotion is an `anchor-edit` work unit (always L4).

- **Regime classification ([ADR 0024](../../../docs/adr/0024-discipline-regime-classification.md)).** Bound at [P-19 (ADR 0058)](../../../docs/adr/0058-p-19-variant-u-c-distance-tuple.md) per the framework decision. U-C names the per-variant declaration of feature source (DistanceTuple) + regime set (`{lights-out, cross-model-judging, human-required}`) + hard-floor table per the discipline contract.

- **Scoping ([ADR 0025](../../../docs/adr/0025-discipline-scoping.md)).** Bound at the [P-19 dispatcher (ADR 0058)](../../../docs/adr/0058-p-19-variant-u-c-distance-tuple.md): work-unit scope is bounded by the dispatched regime. No mandate-specific scoping; anchor's `kind` field parameterises mandate.

- **Three-loop ([ADR 0026](../../../docs/adr/0026-discipline-three-loop.md)).** Bound at the Compound Engineering plan→work→review→compound loop. The "compound" step is materialised as Patrol-tier monitoring of the distance distribution (F47 detection) — meta-loop closure is substrate-enforced, not operator-voluntary.

- **Trifecta closure ([ADR 0027](../../../docs/adr/0027-discipline-trifecta-closure.md)).** Bound at the [P-08 (ADR 0015)](../../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md) holdout + the [P-12 deterministic linter (ADR 0032)](../../../docs/adr/0032-p-12-deterministic-linter-framework.md) — both substrate-enforced.

**Disciplines U-C is NOT silent on but does not own.** None — U-C carries all 10 disciplines. The carve-out on honesty (operator-legibility) is a carry to Phase 8, not a rejection.

## §5 Mandate fit

U-C's mandate-fit YAML block (in this spec's frontmatter) restated per work-unit-class:

- **initial-spec: brownfield.** For brownfield, U-C's anchor set is drawn from the existing codebase + observable behaviour + slow-layer invariants (Brier pace-layers + live tests + runtime traces). For greenfield, initial-spec authoring is by construction L4 (cold-start, no near-anchor anchors exist); U-C does not pretend to lights-out initial-spec on greenfield. Falsifying scenario: if an operator on greenfield achieves lights-out initial-spec authoring, the distance estimator's cold-start invariant is wrong.

- **refactor: both.** Refactoring is naturally distance-typed — the proposed change's distance to the nearest architecture-rule or live-test anchor determines the regime. Greenfield refactor (against intent-invariants): the architecture-rule anchor set is built incrementally per the cold-start trajectory. Brownfield refactor (against live-test anchors + Brier pace-layers): the structural view of the codebase (P-22 + P-23) drives `graph_distance` directly. Supporting substrate evidence: ADR 0057 P-32, ADR 0058 P-19 dispatcher, ADR 0059 P-28 anchor envelope. Falsifying scenario: if refactor work units land at indistinguishable distances on greenfield vs brownfield with identical regime distributions, the mandate-as-parameter claim is wrong.

- **mvp: greenfield.** MVP authoring (greenfield-typical) operates against the operator-authored intent block — the day-0 frozen anchor. Anchor set thickens as MVP cycles deposit live-tests and architecture-rules. Falsifying scenario: if MVP work units never accumulate enough anchors to leave the L4 cold-start regime, U-C's earned-lights-out claim is wrong. Brownfield MVP work is not a canonical U-C work-unit-class (MVP presupposes greenfield-leaning evolution); U-C does not claim it but does not n/a it either — silent rather than reject.

- **post-mvp-evolution: both.** Post-MVP cycles operate against a thickened anchor set on either mandate. Greenfield: intent-block + accumulated architecture-rules + accumulated live-tests. Brownfield: existing codebase + accumulated standards-rules from operator deployment. Distance estimator is uniform across mandates. Supporting substrate evidence: ADR 0057 P-32, ADR 0058 P-19 dispatcher. Falsifying scenario: if post-MVP cycles on brownfield require fundamentally different primitives than on greenfield, the unified claim collapses.

- **regression-fix: both.** Regression fixes are by construction near-anchor (the failing test IS the anchor; the fix's distance to the test is small). Substrate evidence: ADR 0058 contradiction-flag hard floor + ADR 0021 holdout discipline. Falsifying scenario: if regression-fix cycles routinely route to mid-distance or far-anchor regimes, regression-as-near-anchor is wrong.

**DEC-1.a falsifier-discipline observation.** U-C explicitly claims `both` on 3 of 5 work-unit-classes (refactor, post-mvp-evolution, regression-fix). Per [DEC-1.a](../decisions-captured.md#d1--unification-verdict-no-methodology-serves-both-mandates-working-hypothesis-falsifiable-by-phase-8), this is evidence weighing against the no-methodology-serves-both-mandates working hypothesis. The Phase-8 lean-eval will pressure-test these `both` claims (per [§6](#6-open-carries)).

## §6 Open carries

Surfaced into Phase 7 (back-fill) / Phase 8 (lean-eval) / future ADRs:

- **P-32 calibration recipe (Phase-5 ADR seed, accepted-with-RG-flag).** Per [u-c.md §2 RG flag (a)](../substrate-requirements/u-c.md), no corpus recipe maps weights `(w_g, w_p, w_i)` and thresholds `(τ_low, τ_high)` to operator-meaningful risk. Phase-8 lean-eval: calibration sweep against operator-rated risk + historical-incident regression. The substrate exposes the parameters as versioned config so the sweep is tractable. **Status: accepted-as-RG; Phase 8 pressure-tests degradation.**

- **F33/F51 residual Patrol-detector spec (Phase-5 ADR seed, accepted-with-RG-flag).** Per [ADR 0057 § Goodhart resistance](../../../docs/adr/0057-p-32-distance-estimator.md), the `intent_field_touches` LLM-judged leg is structurally F33/F51-vulnerable. Patrol-tier residual detector spec ([P-06 (ADR 0013)](../../../docs/adr/0013-p-06-watchdog-tiers.md)) closes the F47 Goodhart concern downstream of dispatch, but the detector itself is owed. **Status: Phase-5 follow-up ADR carry.**

- **Operator-legibility of the DistanceTuple at dispatch (Phase-8 lean-eval candidate, biggest single OQ).** Per [unified-C §7 OQ-5](../tracks/unified-C.md): if operators cannot see why a work unit was routed lights-out vs Augmentation vs human-required, the substrate is opaque. Phase-8 lean-eval: expose DistanceTuple at dispatch and have operators rate legibility. **Status: Phase-8 carry; pressure-tests the honesty discipline.**

- **F8 staleness over multi-month cold-start (Phase-8 lean-eval candidate).** Per [u-c.md §5](../substrate-requirements/u-c.md): the `anchor-edit` queue's cooling-off windows could be vulnerable to F53 (voluntary discipline fragility). Phase-8: test stale-anchor detection at multi-month time horizons.

- **Brier pace-layer subsumption (Phase-3 adversarial pass carry — open).** Per [unified-C §7 OQ-4](../tracks/unified-C.md): does anchor-distance correctly subsume Brier's pace-layers, or is it a strictly weaker re-encoding? Phase-7 back-fill audit: read Brier's framing and check what anchor-distance loses.

- **Goodhart-resistance under adversarial gaming (Phase-8 lean-eval candidate).** Per [unified-C §7 OQ-1](../tracks/unified-C.md): an adversarial subagent attempts to author work units that land under `τ_low` while smuggling far-anchor changes. **Status: Phase-8 pressure-test.**

- **`Agent = Model + Harness + Anchor-Context` (D-3 challenge).** Per [unified-C §4](../tracks/unified-C.md), U-C challenges D-3 ("Agent = Model + Harness") and proposes the extension. Resolution deferred to Phase-3 cross-mandate review of the D-3 default — not load-bearing for the spec itself.

## §7 References

**ADR set (this spec's binding inputs).** Per the §0 ADR-citation index above; relative paths under `../../../docs/adr/`:

- Common substrate: [ADR 0010](../../../docs/adr/0010-p-01-sandbox-runtime.md), [ADR 0011](../../../docs/adr/0011-p-02-cost-ceilings.md), [ADR 0012](../../../docs/adr/0012-p-05-trajectory-capture.md), [ADR 0013](../../../docs/adr/0013-p-06-watchdog-tiers.md), [ADR 0014](../../../docs/adr/0014-p-07-telemetry-ingestor.md), [ADR 0015](../../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md), [ADR 0016](../../../docs/adr/0016-p-14-judge-router.md), [ADR 0017](../../../docs/adr/0017-p-22-polyglot-codebase-index.md).
- Designed-system / framework substrate: [ADR 0028 (P-19 framework)](../../../docs/adr/0028-p-19-eligibility-regime-classifier.md), [ADR 0029 (P-28 framework)](../../../docs/adr/0029-p-28-typed-object-store.md), [ADR 0031 (P-23)](../../../docs/adr/0031-p-23-dependency-impact-graph.md), [ADR 0032 (P-12)](../../../docs/adr/0032-p-12-deterministic-linter-framework.md).
- Per-variant substrate (U-C-specific): [ADR 0058 (U-C P-19 distance-tuple)](../../../docs/adr/0058-p-19-variant-u-c-distance-tuple.md), [ADR 0059 (U-C P-28 anchor envelope)](../../../docs/adr/0059-p-28-variant-u-c-anchor-envelope.md).
- Orphan substrate: [ADR 0057 (P-32 distance estimator)](../../../docs/adr/0057-p-32-distance-estimator.md).
- Discipline: [ADR 0018](../../../docs/adr/0018-discipline-bias-guard.md), [ADR 0019](../../../docs/adr/0019-discipline-cognitive-escrow.md), [ADR 0020](../../../docs/adr/0020-discipline-cost-ceiling.md), [ADR 0021](../../../docs/adr/0021-discipline-holdout.md), [ADR 0022](../../../docs/adr/0022-discipline-honesty.md), [ADR 0023](../../../docs/adr/0023-discipline-knowledge-promotion.md), [ADR 0024](../../../docs/adr/0024-discipline-regime-classification.md), [ADR 0025](../../../docs/adr/0025-discipline-scoping.md), [ADR 0026](../../../docs/adr/0026-discipline-three-loop.md), [ADR 0027](../../../docs/adr/0027-discipline-trifecta-closure.md).

**Supporting docs:**

- [U-C candidate-registry entry](../candidate-registry.md#u-c--anchor-distance-factory)
- [U-C substrate-requirements summary](../substrate-requirements/u-c.md)
- [Unified-C track sketch](../tracks/unified-C.md)
- [Phase-4.2 overlap.md P-28 verdict](../primitives/overlap.md#p-28-typed-object-store--four-contested-variants)
- [Phase-4.2 overlap.md P-19 verdict](../primitives/overlap.md#p-19-eligibility--regime-classifier--four-contested-variants)
- [DEC-1.a unification-verdict working hypothesis](../decisions-captured.md#d1--unification-verdict-no-methodology-serves-both-mandates-working-hypothesis-falsifiable-by-phase-8)
- [DEC-2 mandate-fit-per-(architecture × work-unit-class)](../decisions-captured.md#d2--mandate-fit-is-per-architecture--work-unit-class-not-per-architecture)
- [auto-006 Phase-6 dispatch-shape brief](../decisions/auto-006-phase-6-dispatch-shape.md) — this spec is the exemplar authored under its Round-2 rubric.
