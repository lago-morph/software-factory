# C23 — Event Bus  (Build Plan, canonical track)

> Source / Spec ref: spec/C23-event-bus.md
> Sources cited in spec: AI-CONTEXT §3.2 (concept 3, line 87), §5.4 (impedance table line 228, bridge line 232), §5.5 (lines 234–239); README §Part 4 (lines 222, 227–228, 231, 252); spec/C01 §3 I7 (line 87) + §4 (line 111) + INV-3; component-inventory C23 row (line 35) + Batch-1 (line 107); F-MODE-COVERAGE F10/F14/F11/F32/F43; gap G27.

## 1. Work breakdown

C23 is *seam-spec + verification + contract-freeze* over an **adopted** Gas City primitive (README line 252
"Native") — not authorship of a new event bus. The work is: confirm the always-on JSONL+seq bus exists in
the pinned substrate, **prove the append-only / monotonic-seq / universal-attribution invariants**, freeze
the event-record shape and ordering contract the three dependents (C24 bridge, C41 identity, C40 Orders)
build against, and surface the G27 CXDB-path contradiction to the bridge seam.

| Task | Description | Size | Prereqs |
|---|---|---|---|
| **T1** Confirm bus in pinned substrate | Confirm the Gas City event bus (append-only JSONL + monotonic seq) is present and always-on in the pinned C01 substrate (AI-CONTEXT §3.2 concept 3); record its backing-store location/format. No separate install (README line 252 "always"). | S | C01 standing |
| **T2** Conformance: append-only + seq | Conformance pack asserting AC-1 (always-on emit, no config), AC-2 (append-only — records never mutated/reordered/deleted), AC-3 (strictly-increasing monotonic `seq`, total order). | M | T1 |
| **T3** Conformance: universal attribution | Assert AC-4 (every event carries a **resolvable `created_by`**; no anonymous events) against the real bus — the F14 guarantee (README line 231). Joint check with C41. | M | T1, C41 actor-schema available |
| **T4** Conformance: ordered read + checkpoint | Assert AC-5 (read from a checkpointed `seq` to head in order; resume from last-processed `seq` after restart) and AC-7 (audit completeness — every action emits, no silent gaps). | M | T1 |
| **T5** CXDB-independence proof | Assert AC-8: with CXDB down, the event bus keeps appending and is the surviving source-of-truth trail (supports C21 G33 fail-open, spec/C21 §6). | S | T1, C19/C21 standing |
| **T6** Freeze event-record schema | Freeze the §4 [FAITHFUL-FILL] record `{seq, ts, created_by, action_type, target_ref?, payload}` + the `action_type` enumeration (OQ-2) so C24/C41/C40 contract against a stable shape. | M | T2, T3 |
| **T7** Resolve G27 bridge-source seam with C24 | With C24, decide whether the event-bus path is *wired* or *latent* (spec §6 reading (b)); freeze I5 (the bridgeable-source guarantee) regardless. Surface as OQ-1 → review-log. | M | T6, C24 spec |
| **T8** Freeze attribution carrier seam with C41 | Freeze the carrier-vs-resolver split (I4): C23 owns the field, C41 owns the actor schema + resolution ("rides events", OQ-3). | S | T3, C41 spec |

## 2. Dependency graph

- **Upstream of C23:** **C01** (the substrate that *contains* the bus) must be standing; C23 is *intrinsic
  to* the Phase-0 substrate, not additive (spec §4 "always-on from Phase 0"). T3 needs **C41** (actor
  schema) to verify `created_by` resolvability end-to-end; T5 needs **C19/C21** so the CXDB-independence
  path has a real source-of-truth fallback.
- **Critical path:** **T1 → T2 → T6** is the gating chain. T6 (the frozen event-record schema) is the single
  most load-bearing artifact — **C24** (bridge source seam), **C41** (`created_by` carrier), and **C40**
  (event-triggered Orders) are all unbuildable against a stub until the record shape + ordering contract are
  frozen. T2's append-only + monotonic-seq proof gates T6 (the schema is only trustworthy if the invariants
  hold on the real bus).
- **Downstream of C23 (blocked until T6/T7/T8):** C24 (lowest-impedance source), C41 (rides events), C40
  (subscribes to events), and the P11 self-healing/audit consumers.

## 3. Parallelization

- **Independent once T1 confirms the bus exists:** T2 (append-only/seq), T4 (read/checkpoint), and T5
  (CXDB-independence) are **independent conformance assertions** and can be authored concurrently — each
  targets a different invariant against the same booted bus.
- **T3 (attribution)** can run in parallel with T2/T4 but couples to C41 (needs the actor schema to assert
  *resolvability*) — start the carrier-side assertion immediately, join the resolver-side when C41 lands.
- **Serialize:** the freeze tasks (T6 schema → T7 G27 seam, T8 attribution seam) come after their proving
  conformance tasks; T6 is the join point the parallel conformance work feeds into.

## 4. Interfaces-first / contract milestones

Freeze early so the three dependents build against stubs in parallel:
1. **The event-record schema** (§4 [FAITHFUL-FILL] + `action_type` enum) — **T6**. The contract C24/C41/C40
   all parse. *Highest-leverage freeze.*
2. **The ordering + checkpoint contract** (I2/I3: monotonic `seq`, read-from-seq, resume-from-seq) — the
   guarantee C24's bridge ordering (G27) and C40's Order-triggering depend on. Frozen with T2/T4.
3. **The `created_by` carrier seam** (I4) — **T8**, with C41: C23 carries the field, C41 resolves the actor.
4. **The CXDB-bridge source seam** (I5) — **T7**, with C24: the "attributed + trajectory-shaped" guarantee,
   independent of *which* path C24 wires (G27 lives at the bridge).

## 5. Risks & de-risking order

1. **G27 — event-bus-vs-raw-bodies CXDB path contradiction (spec §6 / OQ-1).** Spike **first** with C24:
   the spec picks reading (b) (raw bodies wired, event bus latent-but-available), but if the event-bus path
   *is* the intended source, C23's stream shape (I5) becomes load-bearing for the bridge. Retire by freezing
   the bridge source with C24 before C24 builds.
2. **Upstream-claim verification (mirrors the C21 G11 thread).** "Monotonic seq", "records every action",
   and append-only durability are *unverified Gas City assumptions* until exercised — especially `seq`
   semantics under concurrency / crash and torn-final-line recovery (OQ-4). T2/T3 against the *real pinned*
   bus is the de-risking gate.
3. **Record-schema churn.** If T6 freezes the wrong field set, C24/C41/C40 rework. De-risk by freezing the
   minimal [FAITHFUL-FILL] record and the `action_type` enum *before* dependents contract against it.
4. **Attribution-completeness (F14).** A single anonymous action path would break the P9 guarantee (INV-4) —
   T3/AC-7 must prove *no* action bypasses the log.

## 6. Definition of done

- **Per-component:** the pinned Gas City event bus is confirmed always-on (T1); the
  **event-bus conformance pack** passes **AC-1…AC-8** against the real bus (append-only, monotonic-seq,
  universal `created_by`, ordered replay/checkpoint, audit completeness, CXDB-independence) — the gate that
  **must pass before C24, C41, and C40 build on C23**.
- **Per-task:** each Tn's named ACs/freezes are demonstrated; T6 publishes the frozen event-record schema +
  `action_type` enum; T7 records the G27 bridge-source decision (→ review-log OQ-1); T8 records the C41
  carrier/resolver seam.
- **Exit:** all four §4 OQs are either resolved or explicitly carried to sweep 2 with an owner (G27→C24 seam,
  schema→sweep-2, attribution seam→C41, seq-under-concurrency→pinned-binary verification).
