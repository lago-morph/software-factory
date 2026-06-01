# C23 — Event Bus  (Build Plan, canonical track)

> Source / Spec ref: [spec/C23-event-bus.md](../spec/C23-event-bus.md)
> Sources cited in spec: AI-CONTEXT §3.2 (concept 3, line 87), §5.4 (impedance table line 228, bridge line 232), §5.5 (lines 234–239); README §Part 4 (lines 222, 227–228, 231, 252); spec/C01 §3 I7 (line 87) + §4 (line 111) + INV-3; component-inventory C23 row (line 35) + Batch-1 (line 107); F-MODE-COVERAGE F10/F14/F11/F32/F43; gap G27; binding decision D-5.

## 1. Work breakdown

C23 is *seam-spec + verification + contract-freeze* over an **adopted** Gas City primitive (README line 252
"Native") — not authorship of a new event bus. The work is: confirm the always-on JSONL+seq bus exists in
the pinned substrate, **prove the append-only / gap-free-seq / universal-attribution invariants**, freeze
the event-record shape (§4.2) + `EventId` type (§4.1) + `action_type` enum (§4.3), and freeze the C41
seam (the gap-free `event_id` stream, D-5) **first** — before any of the three dependents (C24, C41, C40)
build against C23.

> [FAITHFUL-FILL] **Sweep-2 adds T9 (the C41 `event_id`-stream seam freeze, D-5).** The D-5 ruling
> requires C23 to freeze the gap-free `event_id` stream contract as a *separate, named seam* that C41
> can build its hash-chain against. This task is new at sweep-2; it is the critical C41-gating deliverable.

| Task | Description | Size | Prereqs |
|---|---|---|---|
| **T1** Confirm bus in pinned substrate | Confirm the Gas City event bus (append-only JSONL + monotonic seq) is present and always-on in the pinned C01 substrate (AI-CONTEXT §3.2 concept 3); record its backing-store location, format, and gap-free-vs-merely-monotonic seq semantics. No separate install (README line 252 "always"). | S | C01 standing |
| **T2** Conformance: append-only + seq | Conformance pack asserting AC-S2-1 (always-on emit, no config), AC-S2-2 (append-only — records never mutated/reordered/deleted), AC-S2-3 (closed `action_type`), plus AC-S2-5 (durability fail-loud, E5). | M | T1 |
| **T3** Conformance: universal attribution | Assert AC-S2-4 (no anonymous events — E1/INV-3/F14) against the real bus. Joint check with C41: C23 carries the field; C41 asserts resolvability end-to-end. | M | T1, C41 actor-schema available |
| **T4** Conformance: ordered read + checkpoint | Assert AC-S2-R1 (read from checkpoint), AC-S2-R2 (resume after crash), AC-S2-8 (audit completeness — every action emits, no silent gaps), AC-S2-7 (torn-line recovery, E8). | M | T1 |
| **T5** CXDB-independence proof | Assert AC-S2-9: with CXDB down, the event bus keeps appending and is the surviving source-of-truth trail (supports C21 G33 fail-open, spec/C21 §6). | S | T1, C19/C21 standing |
| **T6** Freeze event-record schema | Freeze the §4.2 `EventRecord` wire schema (`event_id`, `seq`, `ts`, `created_by`, `action_type`, `target_ref?`, `payload`) + the §4.3 `action_type` enumeration (OQ-2) so C24/C41/C40 contract against a stable shape. Verify AC-S2-6 (`seq`/`event_id.seq` consistency). | M | T2, T3 |
| **T7** Resolve G27 bridge-source seam with C24 | With C24, decide whether the event-bus path is *wired* or *latent* (spec §6 reading (b)); freeze I5 (the bridgeable-source guarantee) regardless. Record decision → review-log OQ-1. | M | T6, C24 spec |
| **T8** Freeze attribution carrier seam with C41 | Freeze the carrier-vs-resolver split (I4): C23 carries `created_by`, C41 owns the actor schema + resolution ("rides events", OQ-3). Documented as a bilateral interface contract. | S | T3, C41 spec |
| **T9** Freeze C41 `event_id`-stream seam (D-5) | **NEW at sweep-2. The C41-gating deliverable.** Freeze the §3.1 / §4.1 `EventId = {stream, seq}` contract as the D-5 seam: C23 guarantees gap-free, strictly-increasing `seq` within a named stream; C41 may read this stream via I2 to compute its hash-chain. Assert AC-S2-O (gap-free total order — 100-record sequence with no gaps). This is the seam to freeze first before C41 can build. Document that C23 provides **ordered `event_id`s ONLY** — it does NOT provide the chain. | M | T1, T2 |

## 2. Dependency graph

- **Upstream of C23:** **C01** (the substrate that *contains* the bus) must be standing; C23 is *intrinsic
  to* the Phase-0 substrate, not additive (spec §4 "always-on from Phase 0"). T3 needs **C41** (actor
  schema) to verify `created_by` resolvability end-to-end; T5 needs **C19/C21** so the CXDB-independence
  path has a real source-of-truth fallback.
- **Critical path (sweep-2 update):** **T1 → T2 → T9** is now the *primary* gating chain for C41. T9 (the
  `event_id`-stream seam freeze, D-5) is the single first artifact C41 needs to start building its
  hash-chain. Run T9 as early as T2 permits — do not wait for T6 (full schema freeze) to unblock C41.
  **T1 → T2 → T6** remains the gating chain for C24 and C40. T6 is still the highest-leverage single
  freeze (C24/C40 need the full record shape).
- **Downstream of C23 (dependency matrix):**
  - **C41** — blocked on **T9** (gap-free `event_id` stream contract). Once T9 is frozen, C41 can build
    its hash-chain against C23 stubs.
  - **C24** — blocked on **T6** (full record schema) and **T7** (bridge-source decision).
  - **C40** — blocked on **T6** (record schema, especially `action_type` for trigger predicates) and
    **T8** (attribution carrier for C40's Order triggers).

## 3. Parallelization

- **Independent once T1 confirms the bus exists:** T2 (append-only/seq), T4 (read/checkpoint), and T5
  (CXDB-independence) are **independent conformance assertions** and can be authored concurrently — each
  targets a different invariant against the same booted bus.
- **T3 (attribution)** can run in parallel with T2/T4 but couples to C41 (needs the actor schema to assert
  *resolvability*) — start the carrier-side assertion immediately, join the resolver-side when C41 lands.
- **T9 (C41 seam freeze)** can start concurrently with T2 once T1 is confirmed — T9 only needs the
  gap-free-seq property (a subset of T2's verification work) and the `EventId` type definition (§4.1), not
  the full T6 record schema. **Run T9 in parallel with T2 to maximize C41 unblocking speed.**
- **Serialize:** the freeze tasks (T6 schema → T7 G27 seam, T8 attribution seam) come after their proving
  conformance tasks; T6 is the join point the parallel conformance work feeds into. T9 is the earlier
  join point for C41 specifically.

## 4. Interfaces-first / contract milestones

Freeze in this priority order to maximize downstream parallelism:

1. **[FIRST] The `event_id`-stream seam** (`EventId = {stream, seq}`, gap-free INV-6) — **T9**. This is
   the C41-gating freeze (D-5). C41 cannot start building its hash-chain until this seam is frozen.
   *Freeze T9 before anything else that C41 depends on.*
2. **The event-record schema** (§4.2 `EventRecord` + §4.3 `action_type` enum) — **T6**. The contract
   C24/C41/C40 all parse. *Highest-leverage freeze for C24 and C40.*
3. **The ordering + checkpoint contract** (I2/I3: gap-free `seq`, read-from-seq, resume-from-seq) — the
   guarantee C24's bridge ordering (G27) and C40's Order-triggering depend on. Frozen with T2/T4.
4. **The `created_by` carrier seam** (I4) — **T8**, with C41: C23 carries the field, C41 resolves the
   actor.
5. **The CXDB-bridge source seam** (I5) — **T7**, with C24: the "attributed + trajectory-shaped"
   guarantee, independent of *which* path C24 wires (G27 lives at the bridge).

## 5. Risks & de-risking order

1. **D-5 / OQ-4 — gap-free vs. merely-monotonic seq (top risk, new at sweep-2).** D-5 requires C23 to
   provide *gap-free* `event_id`s (spec §3.1). But v4 says only "monotonic seq" (AI-CONTEXT §3.2);
   gap-free is a stronger property the D-5 integrator ruling *adds*. **Risk: the pinned Gas City binary
   may not guarantee gap-free seq under concurrent producers or crash/restart.** Spike T1 and T9 against
   the *real* pinned binary first; confirm gap-free behavior before C41 builds its chain on this property.
   If the binary is only monotonic-but-gapped, the D-5 seam needs a shim (a single-writer wrapper that
   serializes all appends and maintains the gap-free invariant). This is the single most important
   de-risking action in sweep-2.
2. **G27 — event-bus-vs-raw-bodies CXDB path contradiction (spec §6 / OQ-1).** Spike **first** with C24:
   the spec picks reading (b) (raw bodies wired, event bus latent-but-available), but if the event-bus path
   *is* the intended source, C23's stream shape (I5) becomes load-bearing for the bridge. Retire by freezing
   the bridge source with C24 before C24 builds.
3. **Upstream-claim verification (mirrors the C21 G11 thread).** "Monotonic seq", "records every action",
   and append-only durability are *unverified Gas City assumptions* until exercised — especially `seq`
   semantics under concurrency / crash and torn-final-line recovery (OQ-4). T2/T9 against the *real pinned*
   bus is the de-risking gate.
4. **Record-schema churn.** If T6 freezes the wrong field set, C24/C41/C40 rework. De-risk by freezing the
   minimal `EventRecord` (§4.2) and `action_type` enum (§4.3) *before* dependents contract against them.
5. **Attribution-completeness (F14).** A single anonymous action path would break the P9 guarantee (INV-4) —
   T3/AC-S2-4 must prove *no* action bypasses the log.

## 6. Definition of done

- **Per-component:** the pinned Gas City event bus is confirmed always-on (T1); the
  **event-bus conformance pack** passes **AC-S2-1…AC-S2-9 + AC-S2-O + AC-S2-R1/R2** against the real
  bus (append-only, gap-free monotonic seq, universal `created_by`, ordered replay/checkpoint, audit
  completeness, CXDB-independence, gap-free `event_id` stream) — the gate that **must pass before
  C24, C41, and C40 build on C23**.
- **Per-task:** each Tn's named ACs/freezes are demonstrated:
  - T2: AC-S2-1, AC-S2-2, AC-S2-3, AC-S2-5 pass.
  - T3: AC-S2-4 passes (jointly with C41).
  - T4: AC-S2-R1, AC-S2-R2, AC-S2-7, AC-S2-8 pass.
  - T5: AC-S2-9 passes.
  - T6: frozen `EventRecord` schema + `action_type` enum; AC-S2-6 passes.
  - T7: G27 bridge-source decision recorded (→ review-log OQ-1).
  - T8: C41 carrier/resolver seam documented bilaterally.
  - **T9: gap-free `event_id` stream verified (AC-S2-O passes); `EventId = {stream, seq}` seam frozen;
    D-5 boundary documented ("C23 provides gap-free ordered `event_id`s ONLY; it does NOT provide the
    chain"). This is the C41 seam to freeze first.**
- **Exit:** all OQs are either resolved (OQ-3 → T8, OQ-2 → T6) or explicitly carried with an owner:
  - OQ-1 (G27 bridge contradiction) → C24 seam, T7.
  - OQ-4 (gap-free vs. merely-monotonic under concurrency) → pinned-binary verification at T1/T9;
    shim path documented if binary is only monotonic.
