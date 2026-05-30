# C24 — Telemetry → CXDB ingestion bridge  (Build Plan, Track B)

> Source / Spec ref: [spec-optimized/C24-telemetry-cxdb-bridge.md](../spec-optimized/C24-telemetry-cxdb-bridge.md)

C24 is **not foundational** and builds *against frozen contracts* (C21 ingest §3, C23 read cursor §3, C28 telemetry emission §3). The whole plan is "build against stubs of those three; the seam decision (OQ1 partition) is the only thing that must be resolved before the dual-path core hardens."

## 1. Work breakdown

| Task | Description | Size | Prereqs |
|---|---|---|---|
| **T1 — IngestRecord + type-map** | Define the internal `IngestRecord` (normalized from both sources) and the static `kind → {bundle_id,type,version}` map pinned to D-2 `softwarefactory.v4.trajectory` (DELTA-06). | S | C21 §3 triple format frozen; C22 D-2 namespace (review-log D-2) |
| **T2 — C21 ingest client** | Idempotent post client over C21 `AppendTurn` (:9010 HTTP/JSON; :9009 binary optional later); honor `BUSY`/`UNAVAILABLE`; retry+backoff; supply `parent_ref`/`typed_payload`/`attribution` (DELTA-02). | M | T1; C21 ingest stub |
| **T3 — Durable spool + cursor** | On-disk `inbox/archive/quarantine/cursor` state machine; ack-before-release (DELTA-03); crash-safe reload. | M | C01 mount/lifecycle stub |
| **T4 — BodyWatcher source** | Watch `OTEL_LOG_RAW_API_BODIES` dir; readiness protocol (atomic-rename / `.done` / size-stable, DELTA-05); parse raw body (transfuse `internal/sessionlog` pattern); quarantine on failure. | M | T1, T3; C25 inbox-dir contract |
| **T5 — Session head table + parent rule** | `session.id → head TurnRef` durable table; genesis-on-new-session; advance-on-ack; re-root-on-resume; export-order ordinal ordering (DELTA-04). | M | T2, T3 |
| **T6 — BusTailer source** | `Tail` C23 from durable cursor; map bus record → IngestRecord; `Commit` on ack (DELTA-01 second adapter). | M | T1, T2; C23 read-cursor stub |
| **T7 — Canonical-path partition enforcement** | Implement the OQ1 per-class routing rule so the two adapters never double-ingest; reject misrouted records (DELTA-01, G27). | S | T4, T6; **OQ1 resolved** |
| **T8 — Health/control + supervision** | `Health()` (inbox_depth, spool_depth, bus_lag, post_error_rate, quarantine_count, last_ack_ts); `Start/Stop/Drain` under C01 (DELTA-06); `bridge-lag` alarm + retention ceiling. | M | T3, T2; C01 supervision |
| **T9 — Conformance + chaos suite** | The 9 acceptance tests (§8): idempotent at-least-once, ack-before-release, CXDB-down back-pressure, parent-chain correctness, dual-path no-double-ingest, partial-file safety, type-map, lifecycle, off-hot-path proof. | L | T2–T8 |
| **T10 — Pack packaging** | Package as a pack-declared supervised service (standalone binary, no Go import of Gas City), version-pinned; `city.toml` wiring of the inbox path (AI-CONTEXT §579). | S | T8 |

## 2. Dependency graph

- **Upstream contracts that must be frozen first (external):** C21 ingest contract + triple format (C21 plan §4 M1), C23 read-cursor + `event_id` semantics, C28 correlation-key guarantee, C25 inbox-dir/filename contract, the D-2 bundle-id ruling. All are *Batch 1/foundational* and freeze before C24 (Batch 2) starts — C24 is a downstream integrator, never on the foundational critical path.
- **Internal critical path:** T1 → T2 → (T3 ∥ T5) → T4 → T9. The raw-bodies path (T2→T3→T4→T5) is the path v4 actually builds and the one carrying the hard G26 sub-problems, so it is the critical path; the bus path (T6) is additive.
- **OQ1 gate:** T7 (and the *hardening* of T9's dual-path test #5) is blocked on the OQ1 canonical-path partition decision. Everything else can proceed against either adapter independently.

## 3. Parallelization

Once T1 (IngestRecord + type-map) freezes, three workstreams run concurrently:
- **WS-A (raw-bodies):** T2 → T3 → T4 → T5 (the critical path; one owner end-to-end since these share the spool state machine).
- **WS-B (bus path):** T6 against a C23 stub — fully independent of WS-A until the T7 merge point.
- **WS-C (ops/supervision):** T8 health + packaging T10 against the spool interface T3 exposes — independent of the source adapters.

T9's per-feature acceptance tests can be authored in parallel with their target tasks (test-first). The single serialization point is **T7**, which both WS-A and WS-B feed and which is OQ1-gated.

## 4. Interfaces-first / contract milestones

- **M1 (freeze first):** `IngestRecord` shape + the `kind → {bundle_id,type,version}` D-2 type-map (T1). Lets WS-A and WS-B build against a common normalized record.
- **M2:** the C21-ingest-client interface (T2) — the single point all sources post through; stub it so T3/T4/T5/T6 build against the idempotent-post contract without a live CXDB.
- **M3:** the spool/cursor interface (T3) — `submit(record) / ack(turn_ref) / reload()` — so WS-C (health) and both source adapters share one durability seam.
- **M4 (decision milestone, not code):** OQ1 canonical-path partition frozen → unblocks T7. Co-decided with C21-OQ2 + C23-OQ2 (one integrator ruling across the three seam specs).

## 5. Risks & de-risking order

1. **OQ5 — exporter file-write semantics (spike first).** Does `OTEL_LOG_RAW_API_BODIES` write atomically (rename) or stream-append? The readiness protocol (DELTA-05) and therefore T4 hinge on this. Cheapest, highest-leverage spike: configure Claude Code with the env var and observe the inbox dir under load. Retire before committing T4's protocol.
2. **OQ1 — canonical-path partition.** The only decision that blocks the dual-path merge (T7). Resolve early via the integrator ruling; until then build T4/T6 independently against the single-adapter contract.
3. **C21 perf/availability (inherited C21-OQ4).** C24's sizing depends on C21's unverified :9010 ingest ceiling. De-risk by running T9's off-hot-path proof (#9) + CXDB-down back-pressure (#3) early — they prove C24 is *safe regardless* of C21's perf, decoupling C24's correctness from the unverified store.
4. **Parent-chain correctness (DELTA-04).** Wrong `parent_ref` silently corrupts downstream replay/clustering. De-risk with T9 #4 (out-of-order arrival → correct export-order DAG) authored test-first against T5.
5. **Disk-fill when permanently backed up (OQ2).** The inbox is written by an exporter C24 doesn't control, so back-pressure can't stop the disk filling. Prototype the retention-ceiling + escalation against T8's `Health()` before declaring the G33 story complete.

## 6. Definition of done

**Per-component (ties to spec §8 acceptance):**
- All 9 acceptance tests pass against a C21 stub *and* a live CXDB (T9), including the two joint tests with C21 (idempotency #1↔C21 #2, CXDB-down #3↔C21 #4).
- Off-hot-path proof (#9) demonstrates agent-run latency is independent of C24 state — the load-bearing G33 guarantee.
- OQ1 partition decision is recorded (review-log) and T7 enforces it; no event class is double-ingested.
- C24 runs as a supervised pack service (T10) with `Health()` surfacing the bounded-degradation signals to C01.

**Per-task DoD:**
- T1–T6: unit-tested against frozen contract stubs; idempotency + ack-before-release invariants asserted.
- T7: rejects misrouted records (no silent double-post); partition rule matches the recorded OQ1 ruling verbatim.
- T8: `bridge-lag` alarm fires on stalled `last_ack_ts`; retention ceiling bounds disk.
- T10: standalone binary, no Go import of Gas City (AI-CONTEXT §5.4); version-pinned; `city.toml` inbox wiring present.

**Seam-closure DoD (the reason C24 exists):** G26's five sub-points each have a passing test (delivery semantics #1, back-pressure #3, parent mapping #4, partition #5, partial files #6); G27 is resolved by the recorded partition (T7); G33's raw-bodies-class durability is proven by #2/#3/#9. Residuals (OQ1–OQ5) are logged to review-log, not silently carried.
