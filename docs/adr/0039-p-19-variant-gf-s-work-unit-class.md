# ADR 0039: GF-S P-19 variant — work-unit-class feature source

- **Status**: Accepted
- **Date**: 2026-05-25
- **Deciders**: lead agent (Phase 5 Wave 5.3a subagent)

## Context

This is a **variant ADR** of the [P-19 common framework (ADR 0028)](0028-p-19-eligibility-regime-classifier.md). ADR 0028 ships the shared decision-engine substrate (Drools / OPA Rego decision tables + LLM-judge fallback via [P-14 (ADR 0016)](0016-p-14-judge-router.md) + OPA hard-floor post-check); this ADR specifies the **feature engineering layer** GF-S plugs into that engine, plus the **output regime enum** GF-S declares — both deferred from Wave 5.1b to Wave 5.3 per [auto-005 Round 2](../../architectures/v3/decisions/auto-005-phase-5-dispatch-shape.md#decision-round-2).

The [Phase-4.2 overlap verdict on P-19's four contested variants](../../architectures/v3/primitives/overlap.md#p-19-eligibility--regime-classifier--four-contested-variants) is verbatim:

> **Verdict: SAME primitive (P-19 classifier framework), DISTINCT feature sources + distinct output regime sets.** All four share the construction recipe (Drools/OPA Rego decision tables + LLM-judge fallback via P-14 + OPA hard-floor post-check per [P-19 sketch](../../architectures/v3/primitives/P-19-eligibility-regime-classifier.md)). The differences are at the *feature engineering* layer and the *output enum* layer, not the *decision-engine* layer.

GF-S's claim per [substrate-requirements §3 P-19 entry](../../architectures/v3/substrate-requirements/gf-s.md): feature source is **work-unit-class features** — *intent-block-fields-touched, declared stakes, scenario-set saturation per work-unit-class, recent cross-family judge agreement on the class, configured bar-set parameters* — and the output regime set is `automation-eligible / augmentation-required / escalate`. Greenfield-only framing means no Codebase Model to pull region features from (BF-L's variant) and no graph distance to anchor against (U-C's variant); the only stable identifier at substrate-call time is the **work-unit class**, the spec-shape-agnostic equivalence class assigned by GF-S's intent-block typing.

Forcing failure modes: [F25 design starvation](../../architectures/v3/failure-modes-v3.md#f25--design-starvation) (cold-start factory must default `augmentation-required`; day-0 feature vector is intentionally information-poor) and [F57 design-authority erosion](../../architectures/v3/failure-modes-v3.md#f57--design-authority-erosion-convenience-reclassifies-stakes) (each named feature is auditable and Patrol-diffable across versions).

## Decision

**Adopt the five-feature work-unit-class vector as GF-S's input to the [ADR 0028](0028-p-19-eligibility-regime-classifier.md) decision-table engine, with `automation-eligible / augmentation-required / escalate` as the declared output regime enum.** Feature schema, typed and frozen at the deployment-config layer:

1. `intent_block_fields_touched: set[str]` — named intent-block fields the work unit modifies, extracted from the cycle manifest at intent-typed-event time.
2. `declared_stakes: enum{low, medium, high, caremark}` — operator-declared stakes per [GF-S §1.S9](../../architectures/v3/tracks/greenfield-substrate-first.md#1s9--eligibility-classifier-regime-naming-substrate-primitive); `caremark` is the OPA hard-floor sentinel.
3. `scenario_set_saturation: float ∈ [0, 1]` — the ratio of work-unit-class-tagged scenarios in [P-08 (ADR 0015)](0015-p-08-scenario-storage-with-runner-contract.md) that have been runner-evaluated within the saturation window; the F25 cold-start floor reads this feature.
4. `recent_cross_family_judge_agreement: float ∈ [0, 1]` — rolling-window cross-family judge agreement on the work-unit class via [P-14](0016-p-14-judge-router.md)'s `cross-family` policy.
5. `bar_set_parameters: BarSet` — the deployment's configured bar-set (Jaymin's K=5 ≥90% / paraphrase 5/5 thresholds per the [P-19 sketch corpus citation](../../architectures/v3/primitives/P-19-eligibility-regime-classifier.md#corpus-why-citation)) as a typed record.

The feature extractor runs at cycle-open time, writes the vector as a typed event to the trajectory store ([P-05 (ADR 0012)](0012-p-05-trajectory-capture.md)), and hands it to the ADR 0028 decision-table engine. **GF-S-specific OPA hard floors** (Rego policies in the deployment config): (a) cold-start cycle count < N → force `augmentation-required` (F25); (b) `declared_stakes = caremark` → forbid `automation-eligible` (F57); (c) `scenario_set_saturation < S_min` → force `augmentation-required` (F25); (d) RSI-flagged work-unit classes → forbid `automation-eligible` ([F43](../../architectures/v3/failure-modes-v3.md#f43--rsi-board-visibility-gap)). The output regime drives sandbox capability-profile selection ([P-01 (ADR 0010)](0010-p-01-sandbox-runtime.md)) and the four-guard mediator's gate-set choice.

## Alternatives considered

**B. Per-region features (BF-L's variant).** Pull features from the Codebase Model (P-26) — test coverage, runtime-telemetry density, churn cadence, idiom-conformance. *Why rejected:* GF-S is greenfield-only per [§6 "what this track is not"](../../architectures/v3/tracks/greenfield-substrate-first.md#6-what-this-track-is-not-trying-to-be); no legacy codebase exists at day 0, so P-26 inputs are structurally unavailable. This is exactly the feature source BF-L's variant ADR owns; importing it would violate the [overlap.md "DISTINCT feature sources" clause](../../architectures/v3/primitives/overlap.md#p-19-eligibility--regime-classifier--four-contested-variants) and erase GF-S's methodology bet (work-unit-class typing as the substrate-relevant equivalence class, not code-region geography).

**C. Distance-tuple features (U-C's variant).** Use the P-32 distance tuple `(graph_distance, pace_layer_crossings, intent_field_touches)` plus a `contradiction_flag` hard-floor. *Why rejected:* (1) GF-S declines to bind P-32 at all — graph-distance presupposes a target invariant graph, which GF-S's spec-shape-agnostic substrate refuses to assume; (2) U-C's regime enum (`lights-out / cross-model-judging / human-required`) names different decision handles than GF-S's, and downstream gate-set selectors differ structurally; (3) this is U-C's variant by overlap-verdict assignment — re-using its feature source here would collapse two of the four variants Phase-8 is meant to pressure-test.

## Consequences

**Easier.** GF-S inherits ADR 0028's three-layer engine without re-implementation. The five-feature schema is trivially auditable — each feature is a named OPA input and each cut-point is a Rego file Patrol diffs for F57 drift. The cold-start `augmentation-required` default falls out of feature (3) plus OPA floor (c), not from agent discipline. Day-0 deployments can run rules-only (LLM fallback degrades gracefully per ADR 0028) because the five features are deterministic at intent-typed-event time.

**Harder.** Feature (4) requires sufficient P-14 judge traffic on the work-unit class for the rolling window to populate; bootstrapping deployments read it as `unknown` and the OPA floor takes over. Feature (5) couples the classifier to the deployment's bar-set configuration; bar-set changes invalidate cached classifications and trigger a Patrol re-baseline event. The intent-block-typing layer (feature 1) must be live at substrate-day-1, adding ordering pressure on [GF-S §5.2 bootstrap protocol](../../architectures/v3/tracks/greenfield-substrate-first.md#52-the-bootstrap-protocol).

**Phase-8 lean-eval candidate (in scope).** The [overlap.md four-variant correlation pressure-test](../../architectures/v3/primitives/overlap.md#p-19-eligibility--regime-classifier--four-contested-variants) — run a shared scenario set through all four feature sources (this ADR's work-unit-class vector; BF-L's per-region; U-C's distance tuple; U-A's interval-kind) and measure regime-output correlation. High correlation suggests the candidates are making different methodology bets on the same substrate signal; low correlation confirms genuinely distinct cognitive frames. GF-S owes this evaluation a typed feature-vector export. S9 own-OQ #1 (minimal viable scenario-set N for `automation-eligible` flip) and OQ #3 (F51 LLM-judge-as-classifier recursion) per [GF-S §5](../../architectures/v3/substrate-requirements/gf-s.md) ride along.

**Explicitly NOT promising.** This ADR does not specify decision-table cut-points (deployment-config per ADR 0028), the OPA Rego policy text for GF-S-specific floors (Phase-6 architecture spec), or the BarSet schema's internal structure (P-14 / bar-set ADR scope).

## References

- [ADR 0028: P-19 eligibility / regime classifier framework](0028-p-19-eligibility-regime-classifier.md) — PARENT common ADR; decision-engine substrate this variant plugs into
- [Phase-4.2 overlap verdict on P-19 four contested variants](../../architectures/v3/primitives/overlap.md#p-19-eligibility--regime-classifier--four-contested-variants) — `SAME primitive, DISTINCT feature sources + distinct output regime sets`
- [GF-S substrate-requirements §3 P-19 entry](../../architectures/v3/substrate-requirements/gf-s.md) — work-unit-class feature naming and S9 regime-set declaration
- [P-19 buildability sketch](../../architectures/v3/primitives/P-19-eligibility-regime-classifier.md) [§Per-candidate notes](../../architectures/v3/primitives/P-19-eligibility-regime-classifier.md#per-candidate-notes-no-same-vs-distinct-verdicts), [§Corpus-why citation](../../architectures/v3/primitives/P-19-eligibility-regime-classifier.md#corpus-why-citation) — corpus citation for the feature source and the F25 cold-start default
- [GF-S §1.S9 eligibility classifier substrate slot](../../architectures/v3/tracks/greenfield-substrate-first.md#1s9--eligibility-classifier-regime-naming-substrate-primitive)
- [ADR 0024: Discipline — regime classification](0024-discipline-regime-classification.md) — methodology-layer counterpart binding GF-S to declare this feature source + hard-floor table
- [auto-005 Round 2 Phase-5 dispatch shape](../../architectures/v3/decisions/auto-005-phase-5-dispatch-shape.md#decision-round-2) — Wave-5.3 per-variant ADR scope
