# ADR 0014: P-07 telemetry ingestor

- **Status**: Accepted
- **Date**: 2026-05-25
- **Deciders**: lead agent (Phase 5 Wave 5.1a parallel fanout)

## Context

Three brownfield candidates claim P-07 telemetry ingestor as a substrate primitive: [BF-S](../../architectures/v3/substrate-requirements/bf-s.md), [BF-M](../../architectures/v3/substrate-requirements/bf-m.md), and [BF-L](../../architectures/v3/substrate-requirements/bf-l.md) (via its [P-26 Codebase Model](../../architectures/v3/primitives/index.md) runtime view). The [Phase-3.5 buildability sketch](../../architectures/v3/primitives/cluster-C2.md#p-07-telemetry-ingestor-per-role-read-filters) verdicts P-07 `designed-system`: the telemetry-ingestion half is commodity (an OpenTelemetry Collector pipeline plus a backend), but two pieces of design content are load-bearing: (a) a high-cardinality, time-series backend that can serve in-cycle feature retrieval at low query latency, and (b) the **per-role read filter** discipline that enforces holdout partitioning at the read API. Per the [Phase-4.2 overlap analysis](../../architectures/v3/primitives/overlap.md#p-07-telemetry-ingestor), P-07 is shared across the three brownfield candidates with distinct downstream consumers but a uniform substrate.

Two forcing failure modes shape the decision. [F28 (holdout leakage)](../../architectures/v3/failure-modes-v3.md#f28--holdout-leakage--acceptance-criteria-seen-by-builders) — brownfield's "scenarios live in the running system" inversion makes filesystem-partition holdout impossible; the substrate must enforce partitioning at the read API. [F55 (behavioural drift)](../../architectures/v3/failure-modes-v3.md#f55--behavioural-drift-self-reference-loop) — production telemetry is the out-of-distribution ground truth that breaks self-reference loops, but only if it is queryable in-cycle.

Per-cycle telemetry events must carry two substrate-issued tags written at ingest time: a **codebase-region** tag (BF-L's P-26 runtime view joins on this) and a **methodology-cycle-id** tag (BF-M's stage-7 scenario evaluation joins on this). Both are dimensions on which the eligibility classifier ([P-19 per-region variant](../../architectures/v3/primitives/P-19-eligibility-regime-classifier.md)) reads features.

## Decision

**Build P-07 as an OpenTelemetry Collector ingest pipeline writing into ClickHouse as the backend, with an OPA-Rego per-role read-filter proxy in front of every query.** The Collector's `attributes` processor stamps `codebase.region`, `methodology.cycle_id`, and `holdout.bucket = hash(trace_id) % 100 < 20 ? "holdout" : "training"` onto every incoming span / metric / log at ingest time; assignments are durable from write-time and the `holdout.bucket` field is non-rewritable post-ingest. ClickHouse is the OLAP store — its high-cardinality MergeTree indexing and sub-second range-query latency on time-series workloads meet both BF-L's in-cycle feature retrieval requirement (P-19 reads on the agent's hot path) and BF-M's per-cycle methodology aggregations.

A thin FastAPI query proxy fronts ClickHouse; every query is rewritten by an OPA-Rego policy bundle that filters rows by the caller's role token (builder / V&V / comprehension), denying builder-role reads on `holdout.bucket = "holdout"`. Each allow/deny verdict is logged to [P-05 trajectory capture](../../architectures/v3/primitives/cluster-C2.md#p-05-trajectory-capture) with cycle ID. The role token is a substrate-issued JWT scoped per cycle; the partition policy itself is declared in a `holdout-policy.yaml` signed at deploy time and immutable for the cycle's lifetime.

## Alternatives considered

**B. Prometheus + Grafana Loki as the backend.** *Why rejected:* Prometheus's label-cardinality model breaks down at the cardinality this workload requires — `codebase.region × methodology.cycle_id × trace_id` is an unbounded product on long-lived deployments, and Prometheus's documented cardinality guidance caps active series in the low millions. BF-L's P-26 runtime view joins on per-region telemetry across the full repo history, which exceeds that envelope by one to two orders of magnitude. ClickHouse's columnar storage has no equivalent ceiling.

**C. Datadog (or equivalent managed observability SaaS).** *Why rejected:* per-event ingest pricing on a workload that runs 24/7 across every brownfield cycle is a hard cost-ceiling violation under [ADR 0020 (discipline cost ceiling)](./0020-discipline-cost-ceiling.md), and the vendor lock-in is structurally incompatible with the substrate's audit / replay discipline (we cannot guarantee that a vendor-side data lifecycle policy preserves held-out partitions across export/import). The per-role filter would also have to be re-implemented on top of the vendor's RBAC primitives, which do not generalize to ABAC over event attributes.

**D. Raw S3 + Athena (object-store + on-demand SQL).** *Why rejected:* Athena query latency (seconds to tens of seconds for cold partitions) is unsuitable for in-cycle feature retrieval — [P-19's per-region eligibility classifier](../../architectures/v3/primitives/P-19-eligibility-regime-classifier.md) runs on the agent's hot path before each cycle's region-eligibility decision. The throughput is fine; the latency profile is not. S3 + Athena remains the right archival tier downstream of ClickHouse, not the live query tier.

**E. VictoriaMetrics as the backend.** Considered as a near-substitute for ClickHouse. *Why not selected:* VictoriaMetrics is a strong fit for the metrics half of the workload, but trace and log signals require a separate backend (its trace support is immature relative to ClickHouse-native pipelines like ClickStack / SigNoz). ClickHouse unifies metrics + traces + logs in one store and is the documented backend of multiple production OpenTelemetry deployments. Carried as a fallback if ClickHouse operational cost lands worse than expected at Phase 8.

## Consequences

**Easier:** F28 mitigation is substrate-enforced at the read API rather than agent-discipline-dependent. BF-L's [P-26 runtime view](../../architectures/v3/primitives/index.md), BF-M's stage-7 cycle-keyed scenario evaluation, and BF-S's S-3 telemetry-as-OOD-ground-truth all consume the same backend with role-filtered queries. In-cycle feature retrieval for [P-19](../../architectures/v3/primitives/P-19-eligibility-regime-classifier.md) lands at ClickHouse's sub-second range-query latency. F58 (runtime/design-time compliance split) gets the audited query log as evidence stream for RSI-board visibility.

**Harder:** ClickHouse operational footprint (cluster sizing, MergeTree partition tuning, replica topology) is a real ops burden — heavier than Prometheus-class deployments. OPA-Rego policy authoring becomes a per-deployment task, and JWT issuance / rotation is a separate identity discipline (resolved at architecture-spec time per Phase 6). Schema evolution on the ingest-time tag set (`codebase.region`, `methodology.cycle_id`) is a coordination point between BF-L and BF-M deployments.

**Explicitly NOT promising:** uniform tag semantics across candidates. BF-L's `codebase.region` is derived from the structural view of P-26; BF-M's `methodology.cycle_id` is the stage-7 cycle identifier; the substrate tags both at ingest but does not collapse their semantics. Per-candidate ADRs in Wave 5.3 will record the tag-derivation contract for each consumer.

## References

- [P-07 buildability sketch — C2 cluster, per-role read filters](../../architectures/v3/primitives/cluster-C2.md#p-07-telemetry-ingestor-per-role-read-filters)
- [Phase-4.2 overlap verdict — P-07 shared by BF-S / BF-M / BF-L](../../architectures/v3/primitives/overlap.md#p-07-telemetry-ingestor)
- [BF-L substrate-requirements summary — P-26 runtime view consumes P-07](../../architectures/v3/substrate-requirements/bf-l.md)
- [BF-S substrate-requirements summary — S-3 telemetry-as-OOD-ground-truth](../../architectures/v3/substrate-requirements/bf-s.md)
- [BF-M substrate-requirements summary — stage-7 cycle-keyed evaluation](../../architectures/v3/substrate-requirements/bf-m.md)
- [F28 holdout leakage failure mode](../../architectures/v3/failure-modes-v3.md#f28--holdout-leakage--acceptance-criteria-seen-by-builders)
- [F55 behavioural drift failure mode](../../architectures/v3/failure-modes-v3.md#f55--behavioural-drift-self-reference-loop)
- [F58 runtime/design-time compliance split](../../architectures/v3/failure-modes-v3.md#f58--runtimedesign-time-compliance-split)
- [ADR 0015: P-08 scenario storage with runner contract](./0015-p-08-scenario-storage-with-runner-contract.md) — sibling per-role-filter ADR using the same OPA-Rego ABAC pattern
- [ADR 0020: discipline cost ceiling](./0020-discipline-cost-ceiling.md) — forcing constraint on vendor-SaaS alternatives
