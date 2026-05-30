# C23 — Event bus  (Build Plan, Track B)

> Source / Spec ref: [spec-optimized/C23-event-bus.md](../spec-optimized/C23-event-bus.md)

## 1. Work breakdown

| Task | Description | Size | Prereqs |
|---|---|---|---|
| T1 | **Freeze the record envelope + `event_id`** (DELTA-06/03): `{event_id=(stream,seq), seq, ts, stream, type, actor, payload}` JSONL line schema + versioning; non-null `created_by`. The contract C19/C20/C24/C40/C41 build against. | S | C41 actor stamp shape; C20 envelope alignment (`bead_format_version` precedent) |
| T2 | **Define the `EventBus` port** (DELTA): `Append`, `Read`, `Tail`, `Cursor`/`Commit`. Pre/post + invariants from spec §3. Stub + Gas City native both target it. | S | T1 |
| T3 | **Durable append + monotonic gap-free `seq`** (DELTA-01): per-stream appender, fsync barrier, head-`seq` recovery, torn-trailing-line truncation on restart. | M | T2 |
| T4 | **Stream partitioning + segmentation** (DELTA-04/05): per-`run_id`/actor streams; size/time-rolled segment files `<stream>/<from_seq>.jsonl`; single-writer-per-segment. | M | T3 |
| T5 | **Durable consumer cursors + at-least-once read/tail** (DELTA-02/03): `Read(from_seq)`, `Tail`, per-consumer `Commit`; resume-from-committed on restart. | M | T3 |
| T6 | **Bounded back-pressure + low-water-mark** (DELTA-02): producer/consumer decoupling guarantee; `min(committed_seq)` over registered consumers; `consumer-lag` health signal to C01. | M | T5 |
| T7 | **Retention / segment prune** (DELTA-05): prune whole segments below low-water-mark by age/reachability; durability floor protects un-ingested data; max-age escalation hook. | M | T4, T6 |
| T8 | **Gas City native binding**: wire the Gas City event-bus primitive (AI-CONTEXT §3.2 #3) behind the `EventBus` port; verify it satisfies T3–T7 contracts or document the gap. | M | T2–T7 |
| T9 | **Health + ops surface**: per-stream head `seq`, consumer lag, segment count, prune low-water-mark → C01 `Health()`; backup-as-plain-JSONL ops contract. | S | T6 |
| T10 | **Conformance suite** (spec §8 acceptance #1–#9): durability, crash-torn recovery, back-pressure, at-least-once replay, retention floor, per-stream isolation, attribution, port swap, CXDB-fallback interplay. | M | T3–T8 |

## 2. Dependency graph

- **Upstream (must precede C23 ship):** **C01** (mount/lifecycle/supervised restart, `created_by` plumbing via C41), **C41** (actor value shape). C23 is a Batch-1 foundational + Gas City "always-on" primitive (no Phase gate).
- **Critical path inside C23:** T1 envelope → T2 port → T3 durable append → (T4 partitioning ∥ T5 cursors) → T6 back-pressure → T7 retention → T10 conformance. T3 (durable append + recovery) is the load-bearing core; everything else hangs off it.
- **Downstream blocked on C23 contracts (not on C23 being complete):** **C19** (`BeadMutationEvent` emit, resolves C19-OQ1), **C20** (`SchemaChangeEvent`), **C21** (DELTA-04 durable-spool fallback + replay — C21's *whole* G33 story depends on C23 T1/T3), **C24** (reads C23 as lowest-impedance CXDB source), **C40** (Orders subscribe), **C41** (attribution ledger). These can build against stubs once T1+T2 land.

```
C01 ─┐
C41 ─┴─► T1(envelope) ─► T2(port) ─► T3(durable append) ─┬─► T4(partition) ─┐
                                                          └─► T5(cursors) ──┴─► T6(back-pressure) ─► T7(retention) ─► T10(conformance)
                                       T2 ──(contract freeze)──► C19, C20, C21, C24, C40, C41 build in parallel against stubs
```

## 3. Parallelization

- **After T2 (port freeze), fan out three independent workstreams:** (a) durability core T3→T4 (segment/fsync/recovery), (b) consumer plane T5→T6 (cursors, back-pressure, low-water-mark), (c) the **stub `EventBus`** for downstream unblocking. (a) and (b) converge at T6.
- **T8 (Gas City native) runs concurrently** with (a)/(b) as a separate binding that must pass the same T10 suite — verifies the native primitive meets the augmented contract rather than re-implementing it.
- **Downstream parallelism is the point:** freezing T1+T2 early lets C19/C20/C21/C24/C40/C41 (six consumers) build simultaneously against the stub. This is the highest-leverage early freeze in Batch 1 — three sibling specs already wrote contracts against C23.

## 4. Interfaces-first / contract milestones

1. **M1 — Envelope + `event_id` frozen (T1):** the JSONL line shape + idempotency key. Unblocks every producer's emit code and every consumer's parse code. *Highest priority* — C21-OQ2 and C19-OQ1 resolve here.
2. **M2 — `EventBus` port frozen (T2):** `Append`/`Read`/`Tail`/`Cursor`/`Commit` signatures + invariants. Unblocks stub-based downstream builds (six consumers).
3. **M3 — Delivery semantics frozen (T5):** at-least-once + per-consumer cursor + dedup-on-`event_id`. The C23↔C24↔C40 seam contract; co-freeze with C24 (G26/G27) and C21 (OQ2).
4. **M4 — Durability + ordering contract proven (T3):** fsync barrier + gap-free `seq` + torn-line recovery demonstrated — the evidence C21's DELTA-04 fallback stands on.

## 5. Risks & de-risking order

1. **Spike T3 first (durability/recovery):** prove append-then-fsync + torn-trailing-line truncation + gap-free `seq` recovery under `kill -9`. This is the load-bearing claim three sibling specs lean on; if Gas City's native bus doesn't actually fsync-before-return, C21's whole G33 fallback is unsound. *Retire this uncertainty before anything else.*
2. **Spike T8 (Gas City native fidelity):** does the inherited event-bus primitive give gap-free `seq`, per-stream partitioning, and durable cursors — or do we need to wrap/augment it? Determines whether C23 is "configure the native" vs "implement the port over the native's append." (→ OQ1, OQ5.)
3. **Validate the back-pressure + low-water-mark interplay (T6/T7):** the G33 answer is only real if a dead consumer can't both (a) block producers and (b) force unbounded disk OR data loss. Prototype the max-age escalation decision early (→ OQ4) with C56/C57.
4. **Confirm the CXDB-feed split (OQ2):** C23-path vs raw-API-bodies-path for CXDB ingest — co-design with C24 before C24's bridge solidifies, else two ingest paths double-write to C21.

## 6. Definition of done

- **Per-task:** each task's acceptance maps to a spec §8 case (T3→#1/#2, T6→#3, T5→#4, T7→#5, T4→#6, T1→#7, T2/T8→#8, T3+T5↔C21→#9).
- **Per-component (C23 ships when):**
  1. Envelope + port frozen and consumed by ≥1 producer (C19) and ≥1 consumer (C24) stub (M1/M2).
  2. Durable append with gap-free monotonic `seq` survives `kill -9` + restart with torn-line truncation (acceptance #1/#2).
  3. Back-pressure decoupling proven: frozen consumer → producers unaffected, zero loss; unfreeze → full ordered drain (#3).
  4. At-least-once + `event_id` dedup proven against forced re-delivery (#4); retention low-water-mark protects un-ingested data (#5).
  5. Per-stream isolation under concurrent multi-stream load; no global lock (#6).
  6. Non-null `created_by` enforced; `factory.audit` reconstructs ordered who-did-what (#7).
  7. File-only impl and Gas City native both pass the conformance suite (#8).
  8. Joint CXDB-fallback test with C21 DELTA-04: kill C21 → events stay durable on C23 → restart → zero-loss zero-dup replay (#9).
  9. Health surface (lag, low-water-mark, segment count) visible to C01 `Health()`.
  10. Open questions OQ1–OQ5 recorded in [_meta/review-log.md](../_meta/review-log.md).
