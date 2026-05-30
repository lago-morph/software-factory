# C21 — CXDB trajectory store  (Build Plan, Track B)

> Source / Spec ref: [spec-optimized/C21-cxdb-trajectory-store.md](../spec-optimized/C21-cxdb-trajectory-store.md)

## 1. Work breakdown

| Task | Description | Size | Prereqs |
|---|---|---|---|
| T1 | **CXDB repo-inspection spike (G11/OQ1).** Clone `github.com/strongdm/cxdb`, run it, confirm the turn/Blob-CAS/branch model, measure ingest p50 + retrieval, map its Go client surface to the proposed `TrajectoryStore` port. Output: a go/no-go on DELTA-01 thinness + a verified perf baseline. | M | none (de-risk first) |
| T2 | **Freeze the `{bundle_id,type,version}` triple format** (DELTA-03) jointly with C22. The on-turn wire shape of the type triple + the v4 trajectory bundle ID `softwarefactory.v4.trajectory` (canonical per D-2) + the initial turn-type names. | S | none (contract) |
| T3 | **Define the `TrajectoryStore` port** (DELTA-01): `AppendTurn`, `PutBlob`, `GetTurn`, `GetBlob`, `WalkTrajectory`, `EnumerateBranches`, `Branch`, `Query`, back-pressure signal. Language-neutral contract + Go binding (CXDB client is Go). | M | T2 |
| T4 | **In-memory stub implementation** of the port (for conformance suite + downstream parallel build). | M | T3 |
| T5 | **CXDB-backed adapter**: wire the port to the real CXDB server (:9009 binary + :9010 HTTP), parent-chain via `session.id`. | L | T1, T3 |
| T6 | **Idempotency layer** (DELTA-02): deterministic `TurnRef` from `(parent, blob_hash, type_triple, attribution)`; dedup-on-append. | M | T5 |
| T7 | **Branch API** (DELTA-05): `Branch` + `BranchRef` + provenance turn + `EnumerateBranches`; prove O(1) + source-immutability. | M | T6 |
| T8 | **Degraded-mode + C23 spool-replay** (DELTA-04, G33): back-pressure response, non-blocking ingest, drain-from-C23 on recovery (co-built at the C24/C23 seam). | L | T6, (C23, C24 contracts) |
| T9 | **Integrity + retention/GC** (DELTA-06): self-verifying reads; mark-and-sweep compaction; retention policy hooks. | M | T6 |
| T10 | **Typed query/projection API** (DELTA-07): `Query(typed_filter)`, typed `WalkTrajectory` stream for C36/C37/C38. | M | T5, T2 (via C22 resolution) |
| T11 | **Conformance suite** covering all spec §8 acceptance criteria; runs against both stub (T4) and CXDB adapter (T5). | M | T4, T5 |
| T12 | **Ops: version pin + health surface** (`UNAVAILABLE`/`BUSY`/spool-depth/compaction-lag → C01 `Health()`); plain-file backup of `turns.log`/`blobs.pack`/`registry/`. | S | T5, T8 |

## 2. Dependency graph

- **Upstream (must precede C21 work):** C01 storage-lifecycle + `created_by` stamp contract; C22 type-triple resolution (co-frozen at T2); C23 event-bus record shape + C24 bridge contract (needed for T8 degraded-mode).
- **Critical path:** **T1 → T3 → T5 → T6 → {T7, T8, T9, T10} → T11**. T1 (the repo-inspection spike) gates the whole DELTA-01 bet and the perf-contract claim; do it *first*. T6 (idempotency) is the hinge — branch, degraded-mode, and query all assume it.
- **Cross-component critical path:** C21 is the root for the whole observability/loop chain — C24, C36, C37, C38, C49 all block on C21's port (T3) and read API (T10). Freezing T3 early unblocks four downstream teams.

## 3. Parallelization

- **After T3 (port frozen):** stub (T4) and CXDB adapter (T5) proceed on independent workstreams; downstream consumers (C24 ingest, C49 branch, C37/C38 read) build against the stub immediately.
- **After T6:** T7 (branch), T9 (integrity/GC), T10 (query) are mutually independent — three parallel workstreams. T8 (degraded-mode) runs in parallel but is gated on the C23/C24 seam being co-available.
- **T2** (triple format) and **T1** (spike) have no prereqs and run concurrently from day 0.
- **T11** (conformance) is authored in parallel with implementation (test-first against the port), then run against both implementations.

## 4. Interfaces-first / contract milestones

Freeze early, in this order, to unblock the most dependents:
1. **The `{bundle_id,type,version}` triple format + `softwarefactory.v4.trajectory` bundle ID** (T2) — co-owned with C22; *everything* typed depends on it.
2. **The `TrajectoryStore` port signatures** (T3) — C24/C49/C36/C37/C38 all code against this; freezing it lets four downstream teams build on the stub before the CXDB adapter exists.
3. **The ingest idempotency contract** (DELTA-02, defined in T3, realized in T6) — C24 must know retries are safe before it builds delivery.
4. **The back-pressure / degraded-mode signal** (DELTA-04, in T3) — the C23/C24 seam needs the `BUSY`/`UNAVAILABLE` contract to build the spool path.

## 5. Risks & de-risking order

1. **DELTA-01 port thinness + G11 perf (highest):** spike T1 first. If CXDB's surface is too idiosyncratic to wrap thinly, or perf misses p50<1 ms, the optimization degrades to "document lock-in + keep fork option" — surface to review-log before committing downstream teams to the port.
2. **G33 degraded-mode at the seam (T8):** the C21↔C23↔C24 spool contract is the load-bearing reliability story; spike a kill-CXDB-mid-run test early (acceptance §8.4) against the stub + a fault-injecting adapter.
3. **Idempotency correctness (T6):** a wrong `TurnRef` derivation silently duplicates or drops turns under retry; property-test it (acceptance §8.2) before T7/T8 build on it.
4. **Triple-format churn (T2):** if C21 and C22 drift on the triple, every typed turn rots — freeze jointly, CI-pin (G17).

## 6. Definition of done

- All spec §8 acceptance criteria pass against **both** the stub and the CXDB adapter via the T11 conformance suite.
- Dedup, idempotency (DELTA-02), O(1) branch isolation (DELTA-05), degraded-mode replay (DELTA-04/G33), integrity rejection (DELTA-06), and type-triple pinning (DELTA-03/G17) each have a passing, named test.
- Measured perf evidence recorded (p50 append <1 ms @10 KB, sub-ms retrieval @≥100 GB) — or a logged deviation against the §5.5 claim with the DELTA-01 fork/swap fallback invoked (G11).
- The `TrajectoryStore` port is published and at least one downstream consumer (C24 or C49) is building against it.
- Health signals wired to C01 `Health()`; CXDB binary version pinned; file-layout backup documented.
- Open questions OQ1–OQ5 either resolved or mirrored to [_meta/review-log.md](../_meta/review-log.md) with owners (OQ1, OQ2 co-spec C24, OQ3 co-spec C22).
