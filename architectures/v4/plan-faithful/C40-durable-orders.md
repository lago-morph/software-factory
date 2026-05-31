# C40 — Durable Workflow Engine (Orders)  (Build Plan, canonical track)

> Source / Spec ref: spec/C40-durable-orders.md
> Sources cited in spec: README §"Principle 11" (line 246, durable-workflow row line 258, summary line 261),
> §Part 6 Phase 3b (lines 459–466); AI-CONTEXT §3.1 (line 76 "Orders subscribing to crashes/gates"), §3.3
> (line 109 "order | event-triggered workflow"), §3.4 (Phase-0 "Explicitly off … orders"), §3.5 (migration
> tail), §10 (line 333), §11.1 (line 486 Temporal-deferral), §9.1 (line 408 transfusion); spec/C23 §1/§2/§5
> (event bus = trigger substrate); component-inventory C40 row (line 52) + Batch-3 (line 111); gap G33;
> review-log D-6 (canonical track), D-8 (Order owned by C40).

## 1. Work breakdown

C40 is **seam-spec + conformance + ceiling-disclosure** over an **adopted, native** Gas City primitive
(README line 258 "Orders native") — **not** authorship of a durable-workflow engine. The work is: confirm
the Order primitive exists in the pinned substrate and turns on via the `orders` block (off at minimum,
AI-CONTEXT §3.4); **prove the crash-resume + retry + event-trigger invariants** against the *real* Orders;
**document the G33 durability ceiling honestly** (what survives, what does not) without hardening it; freeze
the trigger/launch/durability contract C39 builds against; and define the falsifiable "Orders insufficient →
Temporal" threshold (OQ-1). **No Temporal integration and no custom engine/saga framework is built** (the bar).

| Task | Description | Size | Prereqs |
|---|---|---|---|
| **T1** Confirm Orders in pinned substrate | Confirm the Gas City Order primitive (event-triggered + durable) exists in the pinned C01 substrate and is **enabled by the `orders` config block** (off at minimum, AI-CONTEXT §3.4). Record what backing store it uses. No new engine. | S | C01 + C23 standing |
| **T2** Conformance: event-trigger | Conformance pack asserting **AC-1** (an Order with a trigger predicate over C23 events fires iff a matching event appears; AI-CONTEXT §3.1 line 76) and **AC-5** (no `orders` block ⇒ no Orders instantiated). | M | T1, C23 conformance (event stream) |
| **T3** Conformance: crash-resume + retry (the core claim) | Assert **AC-2** (in-flight Order survives a runtime crash/restart and **resumes** from persisted progress) and **AC-3** (failed step retried, bounded) against the *real* bus. This is the G33 claim "for Gas City only" — exercised here to find the **actual ceiling depth**. | L | T1 |
| **T4** Conformance: trigger crash-safety | Assert **AC-4** (a waiting Order does not miss a trigger event around a crash — resumes reading C23 from its checkpointed `seq`, inherited from C23 I3). | M | T2, T3 |
| **T5** Document the G33 durability ceiling | Author the **honest ceiling disclosure** (spec §6 / **AC-7**): Gas-City-internal crash/retry = survives; non-Gas-City OSS-component fault-tolerance (CXDB/LangFuse/Python-node) = NOT covered (owned at C21/C24/C17 seams); exactly-once / HA / cross-process saga = NOT built → Temporal-deferral trigger. **Document, do not harden.** | M | T3, T4 |
| **T6** Freeze Order-definition + trigger-predicate contract | Freeze the §4 [FAITHFUL-FILL] record `{trigger, launches, retry}` + how a trigger matches a C23 `action_type`/`target_ref` (OQ-2) — bound to the **pinned `gc` `orders` syntax**, NOT invented internals (G11). The contract C39 parses. | M | T2, T3 |
| **T7** Define the "Orders insufficient → Temporal" threshold | Using T3/T4's measured ceiling, write the **falsifiable trigger** (OQ-1): which concrete durability shortfall flips the deferred Temporal decision. Surfaces as the top OQ → review-log. **No Temporal code.** | S | T3, T4, T5 |
| **T8** Freeze C40↔C39 launch seam | Freeze how an Order **drives a C39 fix-task chain** (AC-8 / I3): who owns termination/escalation when the durable workflow loops (C39 per G35), and whether an Order ever launches a plain C12 formula directly (OQ-4). | S | T6, C39 spec |

## 2. Dependency graph

- **Upstream of C40:** **C23** (event bus) must be standing and conformance-passed — it is the **trigger
  substrate** (spec §2; C40's sole declared dependency, component-inventory line 52) and supplies the
  ordered-read/checkpoint surface that makes triggering crash-safe (C23 I2/I3, INV-4). **C01** hosts the
  Order primitive; **C03** supplies the `orders` enable-flag. C40 is **off at minimum** (AI-CONTEXT §3.4) and
  **built in inventory Batch 3** so the Order seam stands before the README **Phase-3b** Healer pieces
  (C36–C39, inventory Batch 4) consume it — "Batch *n*" and "Phase *n*" are distinct, non-aligned schemes (spec §1).
- **Critical path:** **T1 → T3 → T5 → T7** is the gating chain. **T3** (crash-resume conformance) is the
  single most load-bearing task — it measures the *actual* durability ceiling, and **everything honest about
  C40 depends on knowing what Orders really survive**: the G33 disclosure (T5), the Temporal threshold (T7),
  and the contract C39 relies on (T6) are all unsound until T3 reports the real ceiling. T6 (frozen Order +
  trigger contract) gates the downstream consumer.
- **Downstream of C40 (blocked until T6/T8):** **C39** (fix-task loop-closure) — the *inferred* canonical
  workflow an Order drives (coupling not v4-stated; confirmed jointly at OQ-4/T8 — spec §2); it cannot rely
  on Orders for durable re-entry until the trigger/launch contract is frozen and
  the ceiling is known (so C39 knows what it must *itself* handle for termination/escalation, G35).

## 3. Parallelization

- **Independent once T1 confirms Orders exist + enable:** **T2** (event-trigger) and **T3** (crash-resume +
  retry) target **different invariants** against the same enabled Order primitive and can be authored
  concurrently; **T4** (trigger crash-safety) couples to both (needs a waiting Order from T2 and a crash from
  T3), so it joins after.
- **Serialize:** the **disclosure/contract** tasks come after their proving conformance: **T5** (ceiling) and
  **T6** (contract) consume T3/T4; **T7** (Temporal threshold) consumes the measured ceiling (T3/T4/T5); **T8**
  (C39 seam) consumes T6. T3 is the join point the honest-output work feeds into.
- **Cross-component concurrency:** C40's conformance (T2–T4) can be authored in parallel with **C39**'s spec
  (they meet at T8); both wait on C23 conformance for a real event stream to trigger from.

## 4. Interfaces-first / contract milestones

Freeze early so the downstream consumer (C39) builds against a stub in parallel:
1. **The Order-definition + trigger-predicate contract** (§4 [FAITHFUL-FILL] `{trigger, launches, retry}` +
   C23-event match) — **T6**. The contract C39 parses; **highest-leverage freeze**. Bound to pinned `gc`
   syntax (G11), not invented internals.
2. **The durability contract + its ceiling** (I4/I5 + §6 disclosure: "progress survives a Gas-City-internal
   crash; non-Gas-City components are not made fault-tolerant; no exactly-once/HA/saga") — **T5**. C39 needs
   the ceiling to know what *it* must handle (termination/escalation, G35).
3. **The event-trigger subscription seam** (I2: consume C23 ordered-read/checkpoint, resume-from-`seq`) —
   frozen with T2/T4; the guarantee that triggering is crash-safe.
4. **The C40↔C39 launch seam** (I3) — **T8**, with C39: how an Order drives a fix-task chain.

## 5. Risks & de-risking order

1. **G33 durability-ceiling honesty (spec §6 / OQ-3) — de-risk FIRST.** The single most important thing C40
   gets right is an **accurate, un-hardened** statement of what Orders survive. The risk is *over-claiming*
   ("Orders make the whole stack crash-proof" — the exact G33 mistake) or *over-building* (a custom
   circuit-breaker/saga framework — the exact bar violation). Retire by running **T3/T4 against the pinned
   binary first** and reporting the measured ceiling, then writing T5 to that measurement.
2. **Upstream-claim verification (mirrors the C21/C23 G11 thread).** "Survives crashes / retries" is an
   **unverified Gas City assumption** until exercised — resume granularity (mid-step vs step-boundary), retry
   defaults, re-launch idempotency (OQ-3). T3 against the *real* enabled Orders is the de-risking gate; do
   **not** bind to invented `gc` Order internals (G11 caution).
3. **The "Orders insufficient → Temporal" trigger is undefined (OQ-1).** v4 defers Temporal with no
   threshold (AI-CONTEXT §11.1 line 486). Risk: the deferral stays an un-actionable hand-wave. Retire by
   T7 converting the measured ceiling (T3/T4) into a falsifiable trigger — **without** building Temporal.
4. **Contract churn at the C39 seam.** If T6 freezes the wrong Order/trigger shape, C39 reworks. De-risk by
   freezing the minimal [FAITHFUL-FILL] record + pinned-`gc` trigger grammar before C39 contracts against it.
5. **Scope creep against the bar.** The standing temptation is to build durability machinery (saga,
   exactly-once, store-replication) the principle already gets natively. **Guard:** AC-6 (no custom engine)
   is itself a review gate; every proposed line of C40 code must point at a principle Orders *fail* to meet —
   and at sweep 1 there is none.

## 6. Definition of done

- **Per-component:** the pinned Gas City Order primitive is confirmed present + `orders`-enabled (T1); the
  **Gas-City-Orders conformance pack** passes **AC-1…AC-8** against the real primitive (event-trigger,
  crash-resume, retry, trigger crash-safety, off-by-default, no-custom-engine, ceiling-honesty, drives-P11-
  workflow) — the gate that **must pass before C39 relies on Orders**. AC-2 + AC-4 (the crash paths) are the
  load-bearing assertions.
- **Per-task:** each Tn's named ACs/freezes are demonstrated; **T5** publishes the **honest G33 durability-
  ceiling disclosure** (survives / does-not-survive); **T6** publishes the frozen Order-definition + trigger
  contract (pinned `gc`); **T7** records the falsifiable "Orders insufficient → Temporal" threshold (→
  review-log OQ-1); **T8** records the C40↔C39 launch seam.
- **Bar check:** **no** factory-authored durable-workflow engine, saga/compensation framework, state-machine
  runtime, **or Temporal integration** appears in the deliverable (Temporal stays the documented, deferred
  upgrade path only).
- **Exit:** all four §9 OQs are resolved or explicitly carried to sweep 2 with an owner (Temporal-threshold →
  sweep-2 once ceiling measured; Order/trigger syntax → pinned-`gc` verification; ceiling-depth → pinned-
  binary; C39 launch seam → C39).
