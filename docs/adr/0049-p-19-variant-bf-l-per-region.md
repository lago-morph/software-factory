# ADR 0049: BF-L P-19 variant — per-region feature source

- **Status**: Accepted
- **Date**: 2026-05-25
- **Deciders**: Wave 5.3b subagent

## Context

[ADR 0028](0028-p-19-eligibility-regime-classifier.md) records the **common P-19 framework** — decision-table engine (Drools or OPA Rego) + LLM-judge fallback via [P-14](0016-p-14-judge-router.md) + OPA hard-floor post-check — shared across four contested variants (GF-S work-unit-class, BF-L per-region, U-C distance-gated, U-A interval-kind). It explicitly defers per-variant feature-source and output-regime decisions to four Wave-5.3 ADRs (this ADR is the BF-L one).

The [Phase-4.2 overlap analysis verdict on P-19](../../architectures/v3/primitives/overlap.md#p-19-eligibility--regime-classifier--four-contested-variants) is verbatim: **"SAME primitive (P-19 classifier framework), DISTINCT feature sources + distinct output regime sets. All four share the construction recipe (Drools/OPA Rego decision tables + LLM-judge fallback via P-14 + OPA hard-floor post-check per [P-19 sketch](../../architectures/v3/primitives/P-19-eligibility-regime-classifier.md)). The differences are at the *feature engineering* layer and the *output enum* layer, not the *decision-engine* layer."** The overlap.md table row for BF-L specifies the feature source as "Code-region features from Codebase Model (P-26): test-coverage, runtime telemetry, churn cadence, Caremark/RSI tag, debt-cluster, idiom-conformance (conditional), invariant-density (conditional)" and the output regime as **"Per-region regime (output regime is per region, not per cycle)."** This per-region shape is unique to BF-L among the four variants — GF-S classifies per work-unit, U-C and U-A classify per cycle/interval.

[BF-L's substrate-requirements summary §3 P-19 contract](../../architectures/v3/substrate-requirements/bf-l.md) names the same feature schema and adds: "a cycle touching multiple regions inherits the strictest classification." It further notes the per-region variant is the load-bearing answer to BF-L's CTR-A4 lights-out / L5 mapping question — without per-region granularity, BF-L cannot honor the discipline that *different regions of the same codebase carry different stakes* (a legacy untested debt-cluster vs. a green-field idiom-conformant module). It also gates the `idiom-conformance` and `invariant-density` features as **conditional**: when the conventional or invariant view falls back to (b) per the Wave-4.5 smoke-test verdict, the corresponding feature drops and the methodology-degradation clause activates.

The decision-engine, fallback, and hard-floor disciplines are inherited unchanged from [ADR 0028](0028-p-19-eligibility-regime-classifier.md); this ADR specifies only what plugs into them.

## Decision

**Build BF-L's P-19 instantiation as a per-region feature-engineering layer that reads the Codebase Model ([ADR 0047 P-26](0047-p-26-codebase-model.md)) and emits per-region regime classifications into the [ADR 0028](0028-p-19-eligibility-regime-classifier.md) decision engine.**

Three components:

1. **Per-region feature extractor.** Joins on the Codebase Model's structural symbol ID space at a fixed snapshot version (per ADR 0047 Merkle-DAG versioning) to produce a feature vector per region: `{test_coverage_density, runtime_telemetry_density, churn_cadence_90d, caremark_rsi_tag, debt_cluster_id, idiom_conformance_score?, invariant_density_score?}`. The `?`-suffixed fields are conditional — present only when the conventional / invariant Wave-4.5 sub-tracks return (a). Region granularity is the Codebase Model's structural-view region (function / class / module — the same granularity P-26 indexes).

2. **Per-region classification.** The feature vector is evaluated by the ADR 0028 decision-table engine (OPA Rego preferred, Drools acceptable) emitting a regime label *per region*. Hard floors: `caremark_rsi_tag = true → never automation-eligible` (per ADR 0028 F57 discipline); region in a flagged debt-cluster → at-most `augmentation-required`; coverage-density < threshold AND telemetry-density < threshold → `human-required`.

3. **Cycle-level rollup.** A cycle touching multiple regions inherits the **strictest** per-region classification (max over the regime lattice). The rollup is deterministic substrate logic, not a separate classifier; auditability is per-region-then-aggregated.

The conditional-feature pattern: when Wave-4.5 returns (b) for the conventional view, the OPA rule pack drops `idiom_conformance_score` from the active feature set and the methodology-degradation clause logs the regime as `degraded-convention`; same for invariant.

## Alternatives considered

**B. Per-cycle classification (GF-S's variant).** *Why rejected:* this is GF-S's work-unit-class shape, which classifies the *whole cycle* by intent-block-fields-touched + declared stakes. It collapses regional heterogeneity (a cycle touching a Caremark-tagged region and a green-field region would receive one label) and forfeits BF-L's load-bearing claim that legacy code regions carry intrinsic regime constraints independent of what a cycle declares about itself. Per the [overlap.md table](../../architectures/v3/primitives/overlap.md#p-19-eligibility--regime-classifier--four-contested-variants), per-cycle is GF-S's distinct output regime; importing it into BF-L would erase the substantive difference Phase-4.2 deliberately preserved.

**C. Distance-tuple features (U-C's variant).** *Why rejected:* U-C's `P-32 DistanceTuple (graph_distance, pace_layer_crossings, intent_field_touches)` measures *relational* distance from a cycle's target to the rest of the substrate. BF-L's thesis is that classification follows from **intrinsic region properties** indexed by the Codebase Model (coverage, telemetry, churn, debt, Caremark exposure), not from cycle-to-target topology. Distance-tuple features also presuppose a P-32 distance estimator BF-L does not stand up; the Codebase Model is BF-L's load-bearing substrate (per its [§4 X_UNM_B articulation](../../architectures/v3/substrate-requirements/bf-l.md#4-x_unm_b-articulation)) and the feature source must be P-26.

## Consequences

**Easier:** BF-L's CTR-A4 / L5 mapping question lands on substrate: regime stratification reflects code-region reality rather than cycle-declared intent. Caremark/RSI exposure becomes an OPA hard floor at the region level, not an after-the-fact discipline check. The conditional-feature pattern lets Wave-4.5 verdicts on conventional / invariant views flow into classification gracefully without re-architecting the feature schema.

**Harder:** The per-region rollup discipline must be tested explicitly (cycle touching N regions → max-strictness label); operator UI must surface *which* region drove a classification. The Codebase Model snapshot-consistency contract (ADR 0047) is now load-bearing for classifier reproducibility — feature extraction must pin to a version. Methodology-degradation logging adds a `degraded-convention` / `degraded-invariant` regime variant the Patrol drift-monitor must distinguish from regular F57 drift.

## References

- [ADR 0028: P-19 eligibility/regime classifier framework](0028-p-19-eligibility-regime-classifier.md) — parent common ADR (decision-table engine, P-14 fallback, OPA hard-floor pattern)
- [Phase-4.2 overlap.md P-19 verdict — four contested variants](../../architectures/v3/primitives/overlap.md#p-19-eligibility--regime-classifier--four-contested-variants) — SAME-with-DISTINCT-feature-sources verdict and the per-region row this ADR instantiates
- [BF-L substrate-requirements summary §3 P-19 contract](../../architectures/v3/substrate-requirements/bf-l.md) — per-region feature schema, conditional features, strictest-regime rollup
- [ADR 0047: P-26 Codebase Model](0047-p-26-codebase-model.md) — integrated six-view substrate this variant reads features from
- [P-19 buildability sketch](../../architectures/v3/primitives/P-19-eligibility-regime-classifier.md) — BF-L bullet naming the per-region variant as the load-bearing answer to CTR-A4
- [ADR 0024: Discipline — regime classification](0024-discipline-regime-classification.md) — methodology contract requiring per-variant declaration of feature source + regime set + hard-floor table
