# ADR 0012: P-05 trajectory capture

- **Status**: Accepted
- **Date**: 2026-05-25
- **Deciders**: lead agent (Phase 5 Wave 5.1a)

## Context

Seven or more candidates depend on P-05 trajectory capture for evidence
([overlap.md §2 coverage tier ≥7](../../architectures/v3/primitives/overlap.md#2-primitive-overlap-counts-by-candidate-coverage)):
GF-S, BF-M, and U-C name it directly; "implicit-most" claims it as the
substrate-of-record that downstream observation and attribution primitives
read. The contract is **per-event append-only persistence** of the full cycle
trace — every LLM input/output, every tool call invocation and result, every
judge/guard verdict, every operator action — written before control returns
to the caller, so crash-resume is replay from the last persisted event and
post-hoc forensic reconstruction across cycle boundaries is possible
([cluster-C2 § P-05](../../architectures/v3/primitives/cluster-C2.md#p-05-trajectory-capture)).

Downstream consumers fix the contract shape: P-06 Patrol tier reads the
trajectory store at hours cadence for cross-cycle drift detection; P-08
holdout-replay (per [ADR 0015](./0015-p-08-scenario-storage-with-runner-contract.md))
emits a `ScenarioResult` whose verdict is grounded in trajectory evidence;
P-24 attribution joins trajectory events to PR-body pointers (BF-M D-7); the
Phase-8 lean-evals consume trajectory replays as their primary signal. All
four consumers require **queryability by cycle-ID, event-ID, time-window,
and (U-C variant) distance tuple**, not just sequential read.

The forcing failure modes are
[F14 attribution collapse](../../architectures/v3/failure-modes-v3.md#f14--attribution-collapse)
(widened in Phase 1 to cover forensic-reconstruction debt) and
[F55 behavioural drift](../../architectures/v3/failure-modes-v3.md#f55--behavioural-drift-self-reference-loop)
(rated `critical` for greenfield). Both demand a query surface, not just an
append log: F14 reconstruction crosses N worktrees and K timelines, and
F55 detection requires statistical distribution checks over many cycles.

## Decision

**Build P-05 as OpenTelemetry traces with a custom `llm.invocation` span
type, written to an append-only content-addressed object store (S3-compatible
with object-versioning, or local content-addressed filesystem for dev), and
indexed by a co-located embedded analytical database (DuckDB primary; SQLite
WAL acceptable for smaller deployments) for cycle-ID / event-ID / time-window
/ distance-tuple queries.**

Concretely: the writer wraps every LLM call, tool invocation, judge call,
and guard decision; it builds an OTel span whose attributes carry the typed
payload (model snapshot, prompt hash, response hash, tool name, tool args,
tool result, verdict, latency, cost) and whose `event_id` is the SHA-256 of
the canonicalized payload. The full payload (prompt body, response body,
tool-result body) is written to the blob store under its content hash; the
OTel span carries the hash, not the body. fsync (blob) and OTel-batch-flush
(span) both complete before the wrapper returns. The DuckDB index is rebuilt
from the OTel trace stream by an ingest sidecar that runs at trace-export
cadence; queries hit DuckDB, then dereference blobs by hash on demand.

The U-C distance-keyed variant adds the
[P-32 distance tuple](../../architectures/v3/primitives/overlap.md#2-primitive-overlap-counts-by-candidate-coverage)
as a span attribute at write time, indexable in DuckDB without schema change.
The BF-M D-7 PR-body pointer is the trace-ID + cycle-ID — both first-class
OTel fields.

## Alternatives considered

**B. Bespoke JSONL log file per cycle.** Initially the simplest fit — fsync
per line, append-only, content-addressed via per-line SHA. *Why rejected:*
non-queryable beyond `grep`. P-06 Patrol's hours-cadence distribution checks,
P-08's holdout-replay verdict joins, and P-24's cross-cycle attribution
walks all require structured query (`WHERE cycle_id = X AND kind = 'llm.call'
AND ts BETWEEN ...`). Building a query layer over JSONL ends up
reimplementing what DuckDB+OTel already provides. Also single-machine
(no S3 archival path), which breaks the U-C cross-cycle reference requirement
([cluster-C2 § P-05 reads](../../architectures/v3/primitives/cluster-C2.md#p-05-trajectory-capture)).

**C. LangSmith or commercial APM (Datadog APM, Honeycomb).** Drop-in trace
ingestion + a query UI + retention SLA. *Why rejected:* vendor lock-in on the
substrate-of-record is structurally incompatible with the brownfield
on-premises mandate ([BF-S substrate-requirements](../../architectures/v3/substrate-requirements/bf-s.md))
and with the GF-S "everything is content-addressed" discipline. Per-cycle
trace cost at commercial APM pricing also dominates the
[P-02 cost-ceiling envelope](./0020-discipline-cost-ceiling.md) at scale. The
OTel API surface is the standardized half of what these vendors offer;
self-hosting the storage half preserves the option of swapping in any
OTel-compatible UI later (Jaeger, Tempo, Grafana) without rewriting the
writers.

**D. LMDB or SQLite WAL as the primary store (the cluster-C2 sketch's
alternate path).** *Why rejected for the primary path:* both are excellent
for per-cycle single-machine writes but neither is the right substrate for
cross-cycle archival and cross-machine read access. SQLite WAL remains an
acceptable fallback for the index half in single-node deployments; LMDB is
preserved as the writer-side staging buffer when blob-store latency spikes.

## Consequences

**Easier:** F14 forensic reconstruction becomes a DuckDB query rather than a
multi-file `grep` exercise. F55 cross-cycle drift detection (P-06 Patrol's
statistical pass) reads from the same store the writers fill, with no ETL
step. P-08 holdout-replay verdicts can cite specific event hashes as
evidence. Standard OTel tooling (Jaeger, Tempo, Grafana) works out of the
box for human inspection.

**Harder:** Operating an S3-compatible blob store + a DuckDB index sidecar +
an OTel collector is a three-component substrate, not a single file. The
`llm.invocation` custom span type is a project-specific extension to the
OTel semantic conventions; downstream tools that assume vanilla OTel will
ignore the typed attributes. Trace-export latency (OTel's batch-flush
interval) bounds how recent the index can be — sub-second writes appear in
the index within seconds, not microseconds.

**Explicitly NOT promising:** the same-vs-distinct verdict on per-candidate
trajectory variants. GF-S/BF-M's plain trajectory, U-C's distance-keyed
trajectory, and any candidate-specific event-kind extensions are deferred to
Phase-5 Wave-5.3 candidate-specific ADRs (per
[auto-005 Round 2](../../architectures/v3/decisions/auto-005-phase-5-dispatch-shape.md)).
The common substrate (OTel + blob + DuckDB index + content-addressed event
IDs) is what this ADR fixes; the per-candidate span-attribute schemas are
Wave-5.3 content.

## References

- [P-05 buildability sketch in cluster-C2](../../architectures/v3/primitives/cluster-C2.md#p-05-trajectory-capture)
- [Phase-4.2 overlap analysis (P-05 ≥7-candidate coverage)](../../architectures/v3/primitives/overlap.md#2-primitive-overlap-counts-by-candidate-coverage)
- [F14 attribution collapse](../../architectures/v3/failure-modes-v3.md#f14--attribution-collapse) and [F55 behavioural drift](../../architectures/v3/failure-modes-v3.md#f55--behavioural-drift-self-reference-loop) — forcing failure modes
- [ADR 0015: P-08 scenario storage with runner contract](./0015-p-08-scenario-storage-with-runner-contract.md) — downstream consumer (holdout-replay verdicts cite trajectory evidence)
- [auto-005 Round 2 Phase-5 dispatch shape](../../architectures/v3/decisions/auto-005-phase-5-dispatch-shape.md) — Wave-5.1a common-ADR scope
- Substrate-requirements summaries claiming P-05: [GF-S](../../architectures/v3/substrate-requirements/gf-s.md), [BF-M](../../architectures/v3/substrate-requirements/bf-m.md), [U-C](../../architectures/v3/substrate-requirements/u-c.md)
