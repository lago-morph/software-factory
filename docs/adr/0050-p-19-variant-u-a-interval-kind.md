# ADR 0050: U-A P-19 variant — interval-kind feature source

- **Status**: Accepted
- **Date**: 2026-05-25
- **Deciders**: Wave 5.3c1 subagent

## Context

[ADR 0028](0028-p-19-eligibility-regime-classifier.md) records the **common P-19 framework** — decision-table engine (Drools or OPA Rego) + LLM-judge fallback via [P-14](0016-p-14-judge-router.md) + OPA hard-floor post-check — shared across four contested variants (GF-S work-unit-class, BF-L per-region, U-C distance-gated, U-A interval-kind). It explicitly defers per-variant feature-source and output-regime decisions to four Wave-5.3 ADRs; this ADR is the U-A one. Sibling deliverable [ADR 0051](0051-p-28-variant-u-a-interval-envelope.md) records U-A's P-28 interval-typed envelope schema, which this classifier reads features from.

The [Phase-4.2 overlap.md verdict on P-19](../../architectures/v3/primitives/overlap.md#p-19-eligibility--regime-classifier--four-contested-variants) is verbatim: **"SAME primitive (P-19 classifier framework), DISTINCT feature sources + distinct output regime sets. All four share the construction recipe (Drools/OPA Rego decision tables + LLM-judge fallback via P-14 + OPA hard-floor post-check per [P-19 sketch](../../architectures/v3/primitives/P-19-eligibility-regime-classifier.md)). The differences are at the *feature engineering* layer and the *output enum* layer, not the *decision-engine* layer."** The overlap.md table row for U-A specifies the feature source as **"`EscrowInterval.kind`, `pace-layer`, `priors` fields at interval-open time + substrate-current judge agreement + cost-ceiling state"** and the output as **"`automation-eligibility` consumed by P-29 and P-30."**

[U-A's substrate-requirements summary §3 P-19 contract](../../architectures/v3/substrate-requirements/u-a.md) locks the day-0 default: **`escalate` for every interval-kind until declared threshold-bars are measured**, enforced as an OPA-post-check substrate floor rather than a methodology choice (per [unified-A §5.4](../../architectures/v3/tracks/unified-A.md#54-day-0--day-n-trajectory)). Distinct from GF-S/S9 (work-unit-class features inferred from intent-block diff), BF-L (code-region features from [P-26](0047-p-26-codebase-model.md)), and U-C (distance tuple from P-32) — those classify by what a cycle *does* in the codebase or graph; U-A classifies by what the envelope *declares the interval to be*.

Decision-engine, fallback, and hard-floor disciplines are inherited unchanged from [ADR 0028](0028-p-19-eligibility-regime-classifier.md); this ADR specifies what plugs into them.

## Decision

**Build U-A's P-19 instantiation as an interval-kind feature-engineering layer that reads the EscrowInterval envelope at interval-open time and emits an `automation-eligibility` regime into the [ADR 0028](0028-p-19-eligibility-regime-classifier.md) decision engine, with output consumed by [P-29 policy mediator](0030-p-29-policy-mediator.md) and [P-30 event registrar](0036-p-30-event-registrar-substrate.md).**

Three components:

1. **Envelope-typed feature extractor.** Reads at interval-open time from the [U-A interval envelope (ADR 0051)](0051-p-28-variant-u-a-interval-envelope.md) into a feature vector: `{interval_kind, pace_layer, priors_out_of_tree_count, priors_out_of_tree_signatures, priors_in_tree_count, priors_in_tree_signatures, substrate_judge_agreement_recent, cost_ceiling_state}`. The first three groups come straight off the envelope's `kind`, `pace-layer`, and `priors.{out-of-tree, in-tree}` fields. The judge-agreement feature is a substrate-computed rolling statistic — the cross-family agreement rate from [P-14](0016-p-14-judge-router.md) on recently closed intervals sharing the same `kind`. The cost-ceiling feature is the current [P-02](../../architectures/v3/primitives/index.md) headroom against per-interval and per-cycle budgets.

2. **Decision-table classification.** The feature vector is evaluated by the ADR 0028 decision-table engine (OPA Rego preferred so the cut-points live next to the [U-A P-29 policy mediator](0030-p-29-policy-mediator.md) Rego rules) and emits an `automation-eligibility` label ∈ {`lights-out`, `sample-audit`, `escalate`, `human-required`} per interval. Hard floors (OPA post-check, per ADR 0028 F57 discipline): `kind = bootstrap → automation-eligibility = escalate, full stop` (per [unified-A §5.3](../../architectures/v3/tracks/unified-A.md#53-bootstrap-interval-policies-strictest-defaults)); `kind ∈ {archaeology, methodology-delta}` AND not yet audited at a re-entry interval → at-most `sample-audit`; cost-ceiling breach → never `lights-out`; substrate-judge-agreement-recent < threshold → never `lights-out`.

3. **Day-0 → day-N trajectory.** Day 0 the OPA rule pack is configured so every interval-kind defaults to `escalate`; graduation to `sample-audit` or `lights-out` per kind requires (a) operator confirmation at a re-entry interval and (b) measured threshold-bars on that kind's recent history (per [unified-A §5.4](../../architectures/v3/tracks/unified-A.md#54-day-0--day-n-trajectory)). The graduation event is itself a typed event on the envelope graph — auditable, reversible, watchdog-monitored by Patrol for F57 drift.

The output `automation-eligibility` is written back to the envelope's `classifier.automation-eligibility` slot and consumed downstream: [P-29](0030-p-29-policy-mediator.md) uses it to select the `policies.gate / sandbox / approval-gate / judge-diversity` rule pack; [P-30](0036-p-30-event-registrar-substrate.md) uses it to decide re-entry transitions.

## Alternatives considered

**B. Per-region feature source (BF-L's variant).** *Why rejected:* per the [overlap.md verdict](../../architectures/v3/primitives/overlap.md#p-19-eligibility--regime-classifier--four-contested-variants), per-region is BF-L's distinct shape, grounded in [P-26 Codebase Model](0047-p-26-codebase-model.md) code-region indexing. U-A does not stand up P-26 as a substrate primitive — [U-A §4 X_UNM_B articulation](../../architectures/v3/substrate-requirements/u-a.md) explicitly notes the typed-node-graph envelope lacks first-class code-region typing, so per-region features are unconstructable from U-A's substrate. Importing per-region would also erase U-A's load-bearing claim that the envelope's `kind` field is the authoritative regime axis.

**C. Work-unit-class feature source (GF-S's variant).** *Why rejected:* per the [overlap.md table](../../architectures/v3/primitives/overlap.md#p-19-eligibility--regime-classifier--four-contested-variants), work-unit-class is GF-S/S9's distinct shape — features derived from intent-block-fields-touched, declared stakes, and scenario-set saturation. It presupposes intent-block typing that U-A does not carry; U-A's envelope-typed substrate sees only the interval-kind enum, not GF-S's work-unit taxonomy. Per [U-A §3](../../architectures/v3/substrate-requirements/u-a.md), U-A's typed-filter primary axis is `kind × pace-layer × classifier.work-unit-class`, where `work-unit-class` is itself a *downstream* envelope field set *by* the classifier — making intent-block features a layering inversion.

## Consequences

**Easier:** U-A's classifier discipline lands on the same envelope every other U-A substrate primitive reads, so cross-primitive consistency is a typing property of the envelope rather than a coordination promise. The day-0 `escalate` default is an OPA floor (substrate-enforced, not methodology-enforced) — the cold-start posture cannot drift by accident. F57 drift is monitorable at the envelope-typed level: Patrol can diff regime distributions per `kind × pace-layer` slice.

**Harder:** Substrate-judge-agreement-recent and cost-ceiling-state must be exposed as substrate-readable features (not only logged), which adds a substrate-query contract on top of [P-14](0016-p-14-judge-router.md) and [P-02](../../architectures/v3/primitives/index.md). The interval-kind enum becomes load-bearing for classifier behavior — adding a new `kind` value requires an OPA rule-pack update and a graduation policy per [unified-A §5.4](../../architectures/v3/tracks/unified-A.md#54-day-0--day-n-trajectory). The graduation-event audit trail per kind expands the trajectory-store volume.

## References

- [ADR 0028: P-19 eligibility/regime classifier framework](0028-p-19-eligibility-regime-classifier.md) — parent common ADR (decision-table engine, P-14 fallback, OPA hard-floor pattern)
- [ADR 0051: U-A P-28 variant — interval-typed envelope](0051-p-28-variant-u-a-interval-envelope.md) — sibling Wave-5.3c1 deliverable defining the EscrowInterval envelope this classifier reads features from
- [Phase-4.2 overlap.md P-19 verdict — four contested variants](../../architectures/v3/primitives/overlap.md#p-19-eligibility--regime-classifier--four-contested-variants) — SAME-with-DISTINCT-feature-sources verdict and the interval-kind row this ADR instantiates
- [U-A substrate-requirements summary §3 P-19 contract](../../architectures/v3/substrate-requirements/u-a.md) — feature source, output consumers (P-29, P-30), day-0 `escalate` floor
- [Unified-A §5.4 Day-0 → day-N trajectory](../../architectures/v3/tracks/unified-A.md#54-day-0--day-n-trajectory) — graduation discipline per interval-kind
- [ADR 0030: P-29 policy mediator](0030-p-29-policy-mediator.md) — downstream consumer of `automation-eligibility`
- [ADR 0036: P-30 event registrar substrate](0036-p-30-event-registrar-substrate.md) — downstream consumer of `automation-eligibility` for re-entry transitions
- [ADR 0016: P-14 judge router](0016-p-14-judge-router.md) — source of the substrate-current judge-agreement feature
- [ADR 0024: Discipline — regime classification](0024-discipline-regime-classification.md) — methodology contract requiring per-variant declaration of feature source + regime set + hard-floor table
