# C05 — Sling / dispatch (`sling-dispatch`)  (Build Plan, Track B)

> Source / Spec ref: [`spec-optimized/C05-sling-dispatch.md`](../spec-optimized/C05-sling-dispatch.md)

## 1. Work breakdown

| Task | Description | Size | Prerequisites |
|---|---|---|---|
| **T1** | Define the **`RoutingKey` + `RoutingDecision` types** (spec §3.1/DELTA-01): `RoutingKey = {agent_role, rig/pool target, model_family, capability_profile_ref}`; `RoutingDecision = {executor, rig_member, model_selection, admission_lease}`. The opaque `binding` (C09) is a pass-through field, never re-derived (DELTA-04). | S | C09 binding shape (`{template_id, spec_id, agent_role, prompt.id}`); C12 `NodeBinding` role/rig hint |
| **T2** | Define + register the **`DispatchRecord` schema** (DELTA-06): `{dispatch_id = hash({wisp_id, attempt_no}), wisp_id, attempt_no, molecule_id, run_id, agent_role, rig/pool_member, model_family, binding_ref, capability_profile_ref, created_by, on_behalf_of, ts, outcome}`. Submit to C20 for registration via the C20↔C22 seam (review-log D-3); append-path on C23/C19. | M | C20 register mechanism; C41 actor fields; C23/C19 append contract |
| **T3** | Implement **`dispatch(wisp, binding, target_descriptor, ctx) → DispatchOutcome`** — the core single-placement transform: resolve target+model (call C29) → admit (call C28 governor) → enforce C42 partition → commit exactly-one placement → mint idempotent `DispatchRecord` → hand off to C28/C17. Enforce INV-1/2/3/5/6. | L | T1, T2, C29 `ModelSelection`, C28 `acquire`, C42 partition, C41 actor |
| **T4** | Implement the **admission + back-pressure queue** (DELTA-02): on governor `back_pressure`, enqueue the wisp with an aging timestamp; surface `back_pressured` to the caller; re-attempt on next drive. The resource-aware half of dispatch (INV-3). Freeze the `acquire` call shape jointly with C28 (M1). | M | T3 skeleton; C28 governor `acquire(estimated_tokens, model_family)` |
| **T5** | Implement **pool routing** (DELTA-03/INV-7): `least_loaded | round_robin | affinity` strategy over a `[rigs]`-declared pool, per-rig concurrency caps, and the anti-starvation **aging rule**. Phase-0 degrades to a trivial one-member pool (AC-10). | M | T3, T4; C03 `[rigs]` pool config shape; C42 rig set |
| **T6** | Implement **idempotency + replay safety** (DELTA-06/INV-2): `dispatch_id` keying so a redelivered `{wisp_id, attempt_no}` returns the existing record (no double-place); a new `attempt_no` mints a new record. Crash-safe under C18 tick redelivery. | M | T2, T3 |
| **T7** | Implement **`dispatch_convoy(wisps[], …, atomicity) → ConvoyOutcome`** (DELTA-05): batched admission/placement with `all_or_nothing` (rollback partial admissions) vs `best_effort` (per-wisp report); one batch attribution envelope. | M | T3, T4 |
| **T8** | Implement **`cancel(wisp_id, attempt_no, reason)`** — withdraw a queued / placed-but-not-started wisp (C18 supersede / bound-exhaust). Idempotent. | S | T3, T4 |
| **T9** | **Vocabulary wiring** (sling/wisp/convoy/pool, G06): author C05's canonical text for *sling = route/place*, *wisp = unit of dispatchable work*, *convoy = batched dispatch*, *pool = multi-rig target*; link C07 glossary here. Pin the **C05(route) ↔ C09(resolve) authority split** (DELTA-04) as a testable boundary. | S | spec §1 frozen |
| **T10** | Acceptance test suite (spec §8 AC1–AC11) incl. governor grant/back-pressure, idempotent replay, pool fairness/aging under load, partition-violation negative, C29-fail-closed, convoy both modes, Phase-0 degrade, and the **C18-absent build proof** (AC-11). | M | T3–T8 |

## 2. Dependency graph

```
C13/C19 (ready_frontier → wisps)  ─┐
C09 (opaque binding)              ─┤
C12 (NodeBinding role/rig hint)   ─┼─► C05.T3 dispatch ─► T4 admission ─► T5 pool ─► T7 convoy
C29 (ModelSelection / fail-closed)─┤        │              │
C28 (acquire governor)            ─┘        │              └─► T6 idempotency/replay
C42 (rig partition + pool set) ─────────────┘
C41 (created_by / on_behalf_of) ──► (stamped on every DispatchRecord, T2/T3)
C20 (DispatchRecord registration) ◄── T2
C03 ([rigs] pool flag gates pool routing; off at Phase 0)
```

- **Critical path:** C29 + C28 + C09 interface freezes → **T1/T2 (types+record)** → **T3 (dispatch)** → T4/T6 → T5 → T7 → T10. **T3 is the long pole** — the resolve→admit→partition→commit→record sequence is where every invariant lands.
- **C05 is NOT on C18's build path.** Per spec DELTA-04/OQ1, **C18 (reconciler) *calls* C05** to place a ready wisp each tick; C05 builds and tests against C13/C19 + C29/C28/C42 stubs with **C18 absent** (AC-11). This is the dependency-direction correction the integrator must confirm — the inventory's `Depends on: C01, C18` is wrong on the **C18 leg** (a caller, not a build-time dep). **Exact precedent:** C13-B made the identical correction (its `Depends on: C12, C18` C18-leg was the reverse of the call direction; integrator already accepted it).
- **Upstream blockers / freezes (already in flight, Batch 2):** C28 must expose `acquire(estimated_tokens, model_family) → grant | back_pressure` (C28 DELTA-02); C29 must expose `ModelSelection` + fail-closed (C29 DELTA-06); C09 must freeze the opaque binding shape; C13 must freeze `ready_frontier`; C42 must expose the rig partition + pool set; C20 must accept the `DispatchRecord` type registration.

## 3. Parallelization

Independent workstreams after the C28/C29/C09/C13/C42 interface freezes (M1):
- **WS-A (types/record):** T1, T2, T9 — pure data/definition + vocabulary; no runtime code; lands first and unblocks everyone (mirrors C13-B WS-A).
- **WS-B (dispatch core):** T3, T6 — the resolve→admit→partition→commit→record transform + idempotency; the long pole.
- **WS-C (resource control):** T4, T5 — admission/back-pressure queue + pool strategy/aging; depends on the frozen `acquire` shape and the `[rigs]` config shape, *not* on T3's internals, so it develops against a hand-built fixture placement in parallel with WS-B.
- **WS-D (batch + lifecycle):** T7, T8 — convoy + cancel; depends on T3's commit path + T4's queue shape (start once those are frozen, not fully impl'd).
- **WS-E (tests):** T10 — fixtures authored in parallel; executed as WS-B/C/D land. The stub harness (C13/C09/C29/C28/C42/C41 stubs) is itself a parallelizable artifact authored up-front.

Fan-out: WS-A ∥ WS-C-design ∥ (WS-E stub+fixture authoring) immediately after M1; WS-B leads the runtime; WS-D follows WS-B's commit-path freeze.

## 4. Interfaces-first / contract milestones

- **M1 (freeze first):** three seams, co-frozen with their owners so C05 builds against stubs before any owner is complete —
  1. the **C28 admission seam** `acquire(estimated_tokens, model_family) → grant | back_pressure(retry_after)` (DELTA-02);
  2. the **C29 selection seam** `→ ModelSelection {adapter, model, family, cost_class}` + fail-closed (DELTA-06);
  3. the **C09 opaque-binding shape** `{template_id, spec_id, agent_role, prompt.id}` (DELTA-04, pass-through).
  Plus C13's `ready_frontier` (already a C13 M1) and C42's rig/partition shape. These let C18/C13/C39 build against C05 stubs and let C05 build against owner stubs simultaneously.
- **M2:** the **`dispatch` signature + single-placement/idempotency semantics** (INV-1/INV-2) + the **`DispatchRecord` schema** (T2) — so C18 (tick driver), C46 (cost/queue metrics), and C34/C35 (audits) bind to a stable placement fact.
- **M3:** the **pool-strategy + aging contract** (DELTA-03) + the **`[rigs]` config shape** — co-frozen with C03 (`[rigs]`) and C42 (rig set), the Phase-0→Phase-1 enablement boundary.
- **M4:** the **convoy atomicity contract** (DELTA-05) — co-frozen with any consumer that batches (C55 methodology runs; C18 multi-node ticks).

## 5. Risks & de-risking order

1. **Dependency-direction correction (spec OQ1 / DELTA-04) — do first, cheap, high-clarity.** Confirm at the integrator pass that C05's build-time deps are C13/C19+C09+C29+C28+C42/C41 and that **C18 is a caller**, not a build dep. Falsifiable proof: AC-11 (`dispatch` builds+tests with C18 absent). Same correction C13-B already landed — low effort, retire before committing the build order.
2. **Admission-seam shape with C28 (spec §3.2 / M1) — highest cross-component uncertainty.** The `acquire`/back-pressure contract is co-owned with C28's governor (C28 DELTA-02). Spike the exact grant/lease/release lifecycle (does C05 hold the lease, or does the executor? when is it released?) *before* finalizing T3/T4 — a wrong lease-ownership model leaks seats (spec §4 "no leaked leases"). Retire with a grant→place→release fixture against a C28 governor stub (AC-3).
3. **Idempotency under crash/redelivery (spec INV-2 / DELTA-06).** A crash between governor `grant` and `DispatchRecord` append could leave a granted-but-unrecorded lease (double-place on replay). Spike the commit ordering (grant → tentative record → place → finalize, or compensating release on restart) so the `dispatch_id` dedup is airtight. Retire with a crash-injection replay fixture (AC-4) — mirrors C13-B's transactional-seal spike.
4. **Pool fairness/starvation under sustained load (spec INV-7 / DELTA-03).** The aging rule must provably bound wait time; a naïve `least_loaded` can starve a wisp whose only eligible rig is saturated. De-risk with a load-simulation fixture asserting a max-wait bound (AC-5) before declaring DELTA-03 done.
5. **Gas City native `convoy`/`sling` reality (spec OQ3 / G11).** Whether `gc` exposes a native `convoy`/pool object or these are purely v4 names over sling needs the same Gas-City-reality spike as C12/C13 OQ1. Pick "v4 batches over native sling" provisionally; keep T7 agnostic to native-vs-synthetic until confirmed. Do **not** block T3–T6 on this.

## 6. Definition of done

- **Per-task:** each Tn meets its spec §8 acceptance criterion (T3→AC1/AC6/AC8; T1→AC2; T4→AC3; T6→AC4; T5→AC5/AC10; T3-model-policy→AC7; T7→AC9; dependency-direction→AC11).
- **Per-component:**
  - A ready wisp + opaque binding + target is placed on **exactly one** executor with **exactly one** `DispatchRecord` (AC1), routing only on the `RoutingKey` without re-deriving the binding (AC2).
  - Under a back-pressuring governor the wisp **queues + ages** and never over-commits a capped seat; under `grant` it places (AC3); re-invoking the same `{wisp_id, attempt_no}` never double-places (AC4).
  - Over a multi-rig pool under sustained load, work spreads within caps and every queued wisp places within the aging bound (AC5); a partition-violating target is `unroutable` (AC6); a C29 fail-closed yields `unroutable`, not a non-compliant placement (AC7).
  - Every dispatch carries `created_by`/`on_behalf_of` (AC8); a convoy honours its declared atomicity (AC9); the Phase-0 `[rigs]`-off install dispatches via the trivial one-member path with no pool machinery (AC10).
  - **`dispatch` demonstrably builds + tests with C18 (reconciler) absent (AC11)**, proving C18 is a caller, not a build-time dep (the OQ1 dependency-direction correction).
  - C07 glossary links to C05 for sling/wisp/convoy/pool; the **C05(route) ↔ C09(resolve)** authority split is a documented, testable boundary (T9).
  - The four open questions (OQ1 dep-direction, OQ2 retry/escalation owner, OQ3 native-convoy, OQ4 pool-strategy default) are mirrored to [`_meta/review-log.md`](../_meta/review-log.md) with owners.
