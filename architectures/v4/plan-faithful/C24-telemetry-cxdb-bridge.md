# C24 — Telemetry → CXDB Ingestion Bridge  (Build Plan, Track A)

> Source / Spec ref: spec-faithful/C24-telemetry-cxdb-bridge.md

## 1. Work breakdown

| Task | Description | Size | Prerequisites |
|---|---|---|---|
| T1 | **Freeze the bridge seam contract (M1)** — the input contract (raw-body file shape + completeness signal from C25/C28), the output contract (CXDB :9010 turn POST, C21 I2), and the type triple (`softwarefactory.v4.trajectory`, C22/D-2). This is the interface that unblocks parallel build. | S | C21 I2 frozen, C22 triple, C25/C28 raw-body format |
| T2 | **Pack/tool-node skeleton** — package C24 as a Gas City tool node per C02/C17 ABI; config surface (inbox dir, CXDB endpoint, bundle id, retry params) per C03 model. No Go import of Gas City (README:389). | S | C02/C17 ABI, T1 |
| T3 | **Inbox watcher + completeness gate (I1/INV-4)** — watch `OTEL_LOG_RAW_API_BODIES` dir; detect a body file is fully written before ingest (resolves G26 partial-file via OQ-2 mechanism). | M | T2, OQ-2 (file-completeness mechanism) |
| T4 | **Body → turn parser/shaper (I2)** — transfuse the `internal/sessionlog` + Kilroy parse pattern (C51): untruncated request/response JSON → CXDB turn payload + triple + `session.id`. | M | T1, T3, C22 triple |
| T5 | **`session.id` → parent-turn mapper (I3/INV-2)** — per-session head map; resolve parent pointer; first-body→root vs subsequent→prior-head rule (resolves G26 mapping via OQ-3). | M | T4 |
| T6 | **CXDB HTTP poster (I4)** — POST turn to :9010 (C21 I2); handle ack/error; rely on BLAKE3 idempotency for safe re-post (INV-1). | S | T4, C21 I2 |
| T7 | **Durable buffer + retry/back-pressure (I5/INV-3, addresses G33)** — persist un-acked complete bodies; bounded retry/back-off when CXDB down; fail-open to the run; bounded-buffer limit (OQ-4). | M | T6 |
| T8 | **Checkpoint/cursor + restart-resume (INV-5)** — persist inbox cursor + session-head map; resume without re-scan-from-zero or drop on restart. | M | T5, T7 |
| T9 | **Quarantine + bridge-health events** — quarantine unparseable bodies; emit inbox-lag / buffer-depth / CXDB-up-down / error-rate events to C23 for observability. | S | T6, C23 I1 |
| T10 | **Integration pack (AC-1…AC-9)** — synthetic-inbox harness + pinned CXDB; drive all acceptance tests, especially the CXDB-down fail-open/recover cycle. | L | T3–T8, C21 conformance pack |

## 2. Dependency graph

**Must precede C24:**
- **C21** (CXDB :9010 ingest seam + conformance pack passing — the sink must exist and be proven).
- **C22** (the `softwarefactory.v4.trajectory` type triple C24 stamps — D-2 binding).
- **C25/C28** (the raw-body producer side: `OTEL_LOG_RAW_API_BODIES` emission + the file format/completeness signal).
- **C02/C17** (pack + tool-node ABI to package + invoke C24).

**C24 must precede (its consumers assume trajectories land in CXDB):**
- **C36/C37/C38** P11 self-healing readers; **C49** counterfactual replay; **C46** meta-metrics.

**Critical path inside C24:** T1 → T4 → T5 → T6 → T7 → T8 → T10. The **buffer/retry (T7)** + **restart-resume
(T8)** are the load-bearing, hardest tasks (this is "the first non-trivial integration; budget a week",
README:541) and gate the G33 acceptance (AC-6/AC-7).

## 3. Parallelization

Once **T1 (seam freeze)** and **T2 (skeleton)** land, three workstreams fan out concurrently:
- **WS-A (ingest):** T3 (watcher/completeness) → T4 (parser) → T5 (parent mapper). The data-shaping spine.
- **WS-B (delivery):** T6 (HTTP poster) → T7 (buffer/retry) → T8 (checkpoint). The durability spine — can
  build against a stub CXDB while WS-A builds against synthetic bodies.
- **WS-C (ops):** T9 (quarantine + health events) — independent of A/B internals, only needs the C23 emit
  seam.
T10 (integration pack) joins all three. WS-A and WS-B meet at the T4→T6 handoff (the shaped turn).

## 4. Interfaces-first / contract milestones

- **M1 — seam contract freeze (T1):** the three contracts dependents/sub-streams build against:
  (a) **input** = raw-body file shape + completeness signal (with C25/C28),
  (b) **output** = CXDB :9010 turn POST shape (C21 I2),
  (c) **type triple** = `softwarefactory.v4.trajectory` (C22/D-2).
  Freezing M1 lets WS-A build against synthetic bodies and WS-B against a stub CXDB in parallel.
- **M2 — parent-chain rule frozen (T5/OQ-3):** the `session.id`→parent-turn mapping, before C49/self-healing
  reason over trajectory shape.
- **M3 — durability contract frozen (T7/T8):** at-least-once + bounded-buffer + restart-resume semantics,
  before C36/C46 depend on completeness guarantees.

## 5. Risks & de-risking order

1. **Spike first — G33 fail-open/buffer/recover (T6+T7+T8 thin slice).** Prove a body survives a CXDB outage
   and lands idempotently on recovery, with the run never blocking. This retires the single highest-value/
   highest-risk uncertainty and *is* the README:541 "budget a week" work. Validates AC-6/AC-7 early.
2. **Spike — file-completeness detection (T3/OQ-2)** against the *real* Claude Code raw-body emitter: confirm
   how a body file signals "fully written" (rename/close/size-stable). A wrong guess → torn turns (AC-4).
3. **Confirm — `session.id`→parent rule (T5/OQ-3)** against real multi-turn sessions, incl. bridge restart
   mid-session (does a session resume its existing trajectory?).
4. **Measure — throughput + buffer bound (OQ-4/OQ-5):** HTTP :9010 keep-up vs body emission volume; the
   outage window the bounded buffer survives before oldest-trajectory loss.
5. **Confirm — G27 path binding (AC-9):** verify the event-bus path is latent (not wired) and raw-bodies is
   the sole wired source, matching the spec's reading (b).

## 6. Definition of done

**Per-component DoD:** the integration pack (T10) passes **AC-1…AC-9** against a pinned CXDB —
watch→post happy path, per-session parent-chain + cross-session independence, complete-file-only ingest,
at-least-once + idempotent delivery, **CXDB-down fail-open/buffer/recover**, restart-resumability, no-OTLP,
and confirmed raw-bodies path binding. The bridge is a pack-delivered tool node (no Gas City Go import),
configured via the §13.2 inbox/endpoint binding.

**Per-task DoD:**
- T1: M1 contracts written + agreed with C21/C22/C25 owners; sub-streams can build against stubs.
- T3: complete-file gate proven against the real emitter (AC-4); no torn turn posted.
- T4/T5: a multi-body session reconstructs in conversation order from CXDB (AC-2/AC-3).
- T6: a complete body posts and is resolvable on read (AC-1).
- T7/T8: AC-6 (down→buffer→recover) and AC-7 (restart, no loss/no dup) pass; buffer bound documented (OQ-4).
- T9: bridge-health events visible on C23; unparseable body quarantined without blocking the inbox.
- T10: full AC suite green; **must pass before C36/C37/C38/C46/C49 build on landed trajectories**.

**Open questions to resolve before sweep 2** (mirrored to review-log): OQ-1 (G27 residual / event-bus
latency), OQ-2 (file-completeness mechanism), OQ-3 (exact `session.id`→parent rule), OQ-4 (buffer bound /
durability ceiling), OQ-5 (HTTP :9010 vs binary :9009 under load).
