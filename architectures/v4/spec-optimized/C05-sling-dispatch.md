# C05 — Sling / dispatch (`sling-dispatch`)  (Spec, Track B)

> Source: AI-CONTEXT §3.2 concept-8 (l.92 "Dispatch (Sling) | Routes bead/wisp to agent or pool | P2, P3"), §3.3 vocabulary (l.105 "sling | dispatch / route"; l.100 "rig | agent worker role"; l.104 "convoy | batched workflow"; l.108 "wisp | unit of dispatchable work"; l.110 "Mayor | senior coordinator role"); README §"Principle 1" (l.109 "sling routes work to agents with specific templates"; l.111 binding summary), README §"Principle 2" three-layer table (l.117–124 agent loop / dispatch), README §3.4/Phase-0 (l.364 "no multi-rig **pool**" at smallest install; pool is a Phase-1 capability gated by `[rigs]`), AI-CONTEXT §3.4 (l.122 `[rigs]` "explicitly off" at Phase 0). Companion faithful spec [`spec-faithful/C05-sling-dispatch.md`](../spec-faithful/C05-sling-dispatch.md). **Routing-key authority split (load-bearing):** optimized [`spec-optimized/C09-prompt-template-binding.md`](./C09-prompt-template-binding.md) — C09 *resolves* `template_ref → template + spec bundle` and renders; **C05 *routes*** the work item to an agent/pool. The two never overlap (DELTA-04). Collaborators: [`spec-optimized/C13-molecule-runtime-state.md`](./C13-molecule-runtime-state.md) (`ready_frontier(molecule_id) → [Bead]` is "what C05 pulls from", §3 l.58); [`spec-optimized/C28-claude-code-agent-loop.md`](./C28-claude-code-agent-loop.md) (`acquire(estimated_tokens, model_family) → grant | back-pressure`, the admission seam, C28 §3 l.78; "what C05 dispatches *to*", C28 l.17); [`spec-optimized/C29-model-floor-stylesheet.md`](./C29-model-floor-stylesheet.md) (returns `ModelSelection` to dispatch C05, C29 §5 l.107; consumed-by row l.34); [`spec-optimized/C41-identity-attribution.md`](./C41-identity-attribution.md) (`created_by`/`on_behalf_of` on every dispatched action). Inventory C05 row (maps A09b/A22h/A22f/A22g/B25; depends C01, C18; **no assigned Gxx**; foundational=N). Review-log [D-1](../_meta/review-log.md) (same-family judge — affects which `model_family` C05 admission-tags judge dispatch with).
> Inventory ID: C05   Kind: component   Status: sweep-1
> Deltas: DELTA-01 (**dispatch is a typed `RoutingDecision` over an explicit `RoutingKey`, not an opaque "sling routes it" verb** — the routing inputs `{role/rig, model_family-via-C29, capability/egress profile-via-C42/C43, admission-via-C28}` are a named, attributable record so "why did this work item land on this agent" is a queryable fact, not folklore); DELTA-02 (**admission-controlled, back-pressure-aware dispatch** — C05 calls C28's seat governor *before* committing a placement and queues/sheds on back-pressure, so the single-Max-seat ceiling G34 names is honoured at the router instead of thrashed; routing is *resource-aware*, not fire-and-forget); DELTA-03 (**pool routing is a declared, bounded strategy with a fairness + starvation guard**, not "route to a pool" hand-wave — `least-loaded | round-robin | affinity` over a `[rigs]`-declared pool, with per-rig concurrency caps and an anti-starvation aging rule); DELTA-04 (**routing-key authority is split from binding authority** — C05 *routes*, C09 *resolves* the template/spec; C05 treats the binding as an opaque input it never re-derives, closing the C05/C09 double-ownership ambiguity the inventory's `Depends on` graph leaves open); DELTA-05 (**convoy = explicit batched-dispatch primitive with an atomicity policy**, not just a vocabulary word — N wisps dispatched as one admission/attribution unit with all-or-nothing-or-best-effort declared, so batch placement has defined partial-failure semantics); DELTA-06 (**every placement is an idempotent, attributable, replayable `dispatch` record** keyed by `{wisp_id, attempt_no}` — a redelivered or retried dispatch can never double-place a wisp, and the record is the join key for attribution C41 / meta-metrics C46).

## 1. Purpose & responsibility

C05 is the **router**: it takes a *dispatchable work item* (a **wisp** — "unit of dispatchable work", AI-CONTEXT:108; concretely a ready bead from a molecule's frontier) and **places it on the right executor** — a single agent, a tool-node, or a **pool** of agent rigs — by **role/template**, honouring resource admission, capability profile, and model-family policy. It is the substrate seam between *"what is ready to run"* (C13/C19) and *"the thing that runs it"* (C28/C17). In Gas City vocabulary it is **sling** (AI-CONTEXT:105); its batched form is a **convoy** (AI-CONTEXT:104, DELTA-05).

C05 owns:
- **The routing decision** (DELTA-01): given a wisp + its binding (from C09) + a target descriptor (role/rig, from the formula node / C12 `NodeBinding` and C42), select one executor (or pool member), producing a typed `RoutingDecision`.
- **Admission + back-pressure** (DELTA-02): before committing a placement, acquire capacity from C28's seat governor (`acquire`) and from the target rig's concurrency budget; on refusal, queue/age/shed rather than over-commit.
- **Pool routing** (DELTA-03): when the target is a `[rigs]`-declared pool, choose a member by a declared strategy with fairness + anti-starvation guarantees.
- **The dispatch record** (DELTA-06): an idempotent, attributable placement fact keyed by `{wisp_id, attempt_no}`, stamped with `created_by` (C41), persisted on the event-bus (C23) / work-graph (C19) — the audit + replay anchor.
- **Convoy batching** (DELTA-05): grouping N wisps into one dispatch unit with a declared atomicity policy.

**What C05 is NOT:**
- **Not the binding resolver.** C09 resolves `template_ref → template body + spec bundle` and renders the instruction (C09 DELTA-01). C05 *routes* the work to an agent that will run that instruction; it treats the binding as an opaque input and **never re-derives spec/template** (DELTA-04; README:109 "sling routes work to agents with *specific* templates" — the template selection is C09's, the *placement* is C05's).
- **Not the ready-set computer.** C13 exposes `ready_frontier(molecule_id) → [Bead]`; C05 *consumes* it (C13 §3 l.58 "what C05 pulls from"). C05 does not decide *which* beads are ready — it decides *where each ready one goes*.
- **Not the executor.** `agent` nodes execute on **C28**, `tool` nodes on **C17**. C05 hands the work over and records the placement; it does not run the agent loop or the tool (C12:21, C13:26).
- **Not the model selector.** **C29** resolves `{adapter, model, family, cost_class}` (`ModelSelection`); C05 *consumes* that selection as a routing input and an admission tag, it does not pick the model (C29:107).
- **Not the reconciler.** **C18** (Health Patrol) drives the per-tick convergence loop and decides *when* to (re)dispatch a node and how many attempts remain; C05 is the *mechanism* C18 invokes to place a wisp, not the convergence policy (AI-CONTEXT:93; see §2 dependency-direction note + OQ1).
- **Not the partition/identity authority.** **C42** declares rig read/write partitions and **C41** stamps attribution; C05 *enforces the placement matches* the declared partition (a wisp can't be routed to a rig outside its allowed partition) and *attaches* `created_by`, but it does not author the partition policy or the identity (C42, C41).
- **Not messaging.** Inter-agent coordination (Mail/Nudge) is **C06**; C05 is one-directional work *placement*, not the duplex coordination bus.

## 2. Context & dependencies

| Direction | Component | Relationship |
|---|---|---|
| Upstream (ready set) | **C13** molecule / **C19** work-graph | C05 pulls `ready_frontier(molecule_id) → [Bead]` (C13 §3) — the dispatchable wisps. Soft-runtime: C13 computes readiness, C05 places. |
| Upstream (binding) | **C09** prompt-template binding | The wisp arrives with a resolved binding (`{template_id, spec_id, agent_role}` + rendered instruction / `prompt.id`). C05 routes to an agent *for that role*; it never re-resolves the binding (DELTA-04). C09 §2 lists C05 as the router it supplies bindings to. |
| Upstream (target descriptor) | **C12** formula `NodeBinding` / **C42** rig | An `agent` node carries `{template_ref (C09), role/rig hint (C05/C42)}` (C12 §3 l.55). C05 reads the role/rig hint to pick the target (or pool). |
| Lateral (model selection) | **C29** model floor/stylesheet | C05 obtains `ModelSelection` (`{adapter, model, family, cost_class}`) for the node and uses `family` as the admission tag + a routing constraint (judge ≠ coder family per policy). C29 §5 returns the selection "to dispatch (C05)". |
| Lateral (admission) | **C28** agent loop governor | C05 calls `acquire(estimated_tokens, model_family) → grant | back-pressure(retry-after)` before committing a placement; on back-pressure it queues/ages/sheds (DELTA-02; C28 §3 l.78, §5 l.93/l.100). |
| Downstream (executor) | **C28** (agent) / **C17** (tool) | The placement target. C05 hands the wisp + binding + `ModelSelection` + capability profile to the executor and records the dispatch. |
| Cross-cutting | **C41** identity / **C23** event-bus / **C19** work-graph | Every dispatch record carries `created_by`/`on_behalf_of` (C41) and is appended to C23/C19 as an attributable edge (DELTA-06). |
| Substrate / control | **C01** Gas City / **C18** reconciler | C01 provides the native `sling` mechanism C05 specializes. C18 is the **caller** that drives (re)dispatch per tick (dependency-direction nuance — see note). |

> [DELTA-04] **What v4 said:** README:109 ("sling routes work to agents with *specific* templates") and the inventory (`C09 Depends on: C05`; `C05 Depends on: C01, C18`) leave *who owns the routing key* ambiguous — the same sentence couples template selection and placement. **Change:** a hard authority split — **C09 resolves** the template/spec binding; **C05 routes** the (already-bound) wisp to an executor. The `RoutingKey` C05 consumes is `{agent_role, rig/pool target, model_family, capability_profile}`; the *binding* (`{template_id, spec_id, prompt.id}`) is an opaque pass-through C05 attaches to the placement but never computes. **Rationale (force: simplicity + parallelizability):** two components co-owning "which template + which agent" is a double-write hazard and blocks parallel build. Splitting on the verb (`resolve` vs `route`) gives each a single responsibility and a clean freeze-able seam (M1). **Tradeoff:** C05 depends on C09 having already run (the binding must exist before placement); accepted — the formula-node order already guarantees bind-then-dispatch, and C09 §2 already names C05 as its downstream router.

**Dependency-direction note (→ OQ1).** The inventory lists `C05 Depends on: C01, C18`. The **C01** leg is correct (C05 specializes Gas City's native sling). The **C18** leg is a *caller*, not a build-time dependency: **C18 (reconciler) calls C05** to place a ready wisp each tick; C05 must build and test against C13/C19 + stubs with **C18 absent** (this mirrors the C13-B DELTA-06 / OQ2 correction, where the same `Depends on: …, C18` was found to be the reverse of the runtime call direction). C05's real build-time deps are **C13/C19** (ready set), **C09** (binding), **C29** (model selection), **C28** (admission), **C42/C41** (partition/attribution). Flagged for integrator ratification (OQ1).

C05 sits in **Runtime Substrate**, is **non-foundational**, and is **Batch 2** (parallel with C04/C09/C28/C29/C42 per the inventory build batches). It is the connective tissue between the ready-set (C13), the binding (C09), the model floor (C29), and the worker (C28).

## 3. Interfaces / contracts

Sweep-1: interfaces **named + described**; concrete signatures, the `RoutingDecision`/`DispatchRecord` schemas, and the pool-strategy state → sweep 2.

### 3.1 Inbound

- **`dispatch(wisp, binding, target_descriptor, ctx) → DispatchOutcome`** — the core entry C18/C13 invoke to place one ready wisp. `wisp` = a ready bead (id, type, params) from `ready_frontier`. `binding` = the opaque C09 result (`{template_id, spec_id, agent_role, prompt.id}`) — pass-through (DELTA-04). `target_descriptor` = `{rig/pool ref, role}` from the formula `NodeBinding` (C12) / C42. `ctx` = `{molecule_id, run_id, attempt_no, owner_actor}`. **Pre:** the binding is resolved (C09 done) and the wisp is genuinely in the molecule's ready frontier (C13). **Post:** exactly one executor is selected and a `DispatchRecord` is minted (or the call returns `back_pressured`/`unroutable` — never a silent drop). Idempotent on `{wisp_id, attempt_no}` (DELTA-06).
- **`dispatch_convoy(wisps[], binding_map, target_descriptor, ctx, atomicity) → ConvoyOutcome`** — batched placement (DELTA-05). `atomicity ∈ {all_or_nothing | best_effort}`. **Post:** for `all_or_nothing`, either all N place or none do (failed admissions roll back the batch); for `best_effort`, each wisp's outcome is independent and reported per-wisp.
- **`cancel(wisp_id, attempt_no, reason) → ()`** — withdraw a queued/placed-but-not-started wisp (e.g. C18 supersedes a node, or a bound is exhausted). Idempotent.

### 3.2 Outbound

- **Executor hand-off (C05 → C28 / C17).** C05 invokes the executor with `{wisp, binding, model_selection (C29), capability_profile (C42/C43)}`. For `agent` nodes this is the C28 entry that begins a turn loop; for `tool` nodes the C17 tool-node invocation. C05 receives an accept/started ack (the executor owns the outcome thereafter; C05 records *placement*, not completion).
- **Admission request (C05 → C28 governor).** `acquire(estimated_tokens, model_family) → grant | back_pressure(retry_after)` (DELTA-02). On `grant`, C05 commits the placement and holds the lease reference in the dispatch record; on `back_pressure`, C05 queues the wisp with an aging timestamp.
- **Model-selection request (C05 → C29).** For the node's role, obtain `ModelSelection`; `family` becomes the admission tag and a routing constraint. If C29 fails closed (no compliant judge family, C29 DELTA-06), C05 surfaces `unroutable` upward rather than placing an out-of-policy executor.
- **Dispatch record (C05 → C23 / C19 / C41).** A content-addressed/idempotent `DispatchRecord` (DELTA-06): `{dispatch_id = hash({wisp_id, attempt_no}), wisp_id, attempt_no, molecule_id, run_id, agent_role, rig/pool_member, model_family, binding_ref (template_id/spec_id), capability_profile_ref, created_by, on_behalf_of, ts, outcome ∈ {placed|back_pressured|unroutable|cancelled}}`, appended to C23/C19 as an attributable edge.

### 3.3 Pool-routing contract (DELTA-03)

- A `target_descriptor` naming a **pool** (a `[rigs]`-declared multi-rig set, README:364 "multi-rig pool") resolves through a declared **placement strategy**: `least_loaded` (default; by live-lease count per rig) | `round_robin` | `affinity` (sticky by `{spec_id|molecule_id}` for cache/context reuse). Each rig carries a **concurrency cap** (max live leases). An **anti-starvation aging rule** guarantees a queued wisp's effective priority rises with wait time so no wisp is indefinitely passed over under sustained load.

### 3.4 Invariants

- **INV-1 (single-placement).** Each `(wisp_id, attempt_no)` is placed on **exactly one** executor, or not placed (queued/unroutable). Never zero-on-success, never two. The dispatch record is the witness.
- **INV-2 (idempotent dispatch).** Re-invoking `dispatch` for the same `{wisp_id, attempt_no}` returns the existing `DispatchRecord` and does **not** double-place (DELTA-06) — safe under C18 tick redelivery / crash-replay.
- **INV-3 (admission-before-commit).** No placement is committed without a governor `grant` (DELTA-02). A capped Max seat is never over-granted by the router (C28 §4 "admission is the enforcement point").
- **INV-4 (binding pass-through).** C05 never re-derives `template`/`spec`; the binding is consumed opaquely (DELTA-04). Same wisp+binding always routes against the same `RoutingKey` inputs (determinism modulo pool-load).
- **INV-5 (partition-honouring).** A wisp is only placed on a rig whose C42 partition permits the work's read/write scope; a placement that would violate a partition is `unroutable`, never silently downgraded (holdout-isolation relevance, C42/C34).
- **INV-6 (attribution-complete).** Every placement carries `created_by` and (for delegated work) `on_behalf_of` (C41); no anonymous dispatch.
- **INV-7 (fairness/no-starvation).** Under sustained load, pool routing (DELTA-03) places every queued wisp in bounded time via the aging rule; no wisp waits unboundedly while others are placed.

## 4. Data model / state

C05 is mostly a **transform + a small amount of live scheduling state**; durable facts ride C23/C19.

| Aspect | Optimized spec |
|---|---|
| Owned (live, transient) | The **dispatch queue + per-rig lease counters** (DELTA-02/03): queued wisps awaiting admission, each with an aging timestamp; per-rig live-lease counts for `least_loaded`/cap enforcement. Reconstructable from open dispatch records + governor state on restart. |
| Minted (durable) | The **`DispatchRecord`** (DELTA-06), append-only on C23/C19, keyed `{wisp_id, attempt_no}`. The authoritative placement fact. |
| Referenced (not owned) | `ready_frontier` (C13/C19), the binding (C09), `ModelSelection` (C29), seat leases (C28 governor), rig partitions (C42), identity (C41). C05 reads/uses, never authors. |
| Identity | `dispatch_id = hash({wisp_id, attempt_no})` — deterministic, idempotency key (INV-2). |
| Persistence | Dispatch records: event-bus (C23) / work-graph (C19). Queue + lease counters: in-memory scheduling state, rebuildable; no separate durable store needed (the *commitment* — the placement — is the durable record). |
| Consistency | Admission grant + dispatch-record append must be **atomic enough** that a granted seat always has a matching `placed` record (no leaked leases); the queue is best-effort and self-healing from records on restart. |

## 5. Behavior

Core flow: **pull ready → resolve target & model → admit → place → record** (driven per-tick by C18).

```mermaid
flowchart LR
    C18[C18 reconciler tick] -->|drive (re)dispatch| C05
    C13[C13 ready_frontier(molecule_id)] -->|ready wisps| C05
    C09[C09 binding: template_id/spec_id/prompt.id] -->|opaque binding| C05
    C12[C12 NodeBinding: role/rig hint] -->|target descriptor| C05
    C05 -->|select model| C29[C29 ModelSelection]
    C29 -->|adapter/model/family/cost| C05
    C05 -->|acquire(tokens, family)| GOV[C28 seat governor]
    GOV -->|grant / back-pressure| C05
    C05 -->|pool strategy + cap + aging| PICK[pick executor / rig member]
    C05 -->|enforce C42 partition| PART{partition ok?}
    PART -->|no| UNR[unroutable]
    PART -->|yes + grant| PLACE[hand off + mint DispatchRecord]
    PLACE -->|agent| C28[C28 agent loop]
    PLACE -->|tool| C17[C17 tool node]
    PLACE -->|created_by / append| REC[C41 / C23 / C19]
    GOV -->|back-pressure| Q[queue + age, retry next tick]
```

Key flow notes:
- **Pull.** C18 ticks the molecule; C05 takes the ready wisp(s) from C13's `ready_frontier` (C05 does not compute readiness, INV against C13).
- **Resolve target & model.** Read the formula node's role/rig hint (C12/C42) → a single rig or a pool. Ask C29 for `ModelSelection`; carry `family` forward. If C29 fails closed (no compliant judge family) → `unroutable` (don't place out-of-policy).
- **Admit.** `acquire(estimated_tokens, family)` from C28 (DELTA-02). `back_pressure` → queue the wisp with an aging timestamp; retried next tick (no thrash against a capped seat, G34).
- **Place.** For a pool, apply the strategy + cap + aging (DELTA-03) to pick a member that honours its C42 partition (INV-5). Commit *exactly one* placement (INV-1), mint the idempotent `DispatchRecord` (DELTA-06), stamp `created_by`/`on_behalf_of` (C41), hand `{wisp, binding, model_selection, capability_profile}` to C28/C17.
- **Record.** Append to C23/C19; the record is the join key for attribution audits (C34/C35) and meta-metrics (C46 cost-per-dispatch, queueing time).
- **Convoy.** `dispatch_convoy` (DELTA-05) admits/places N wisps as one unit; `all_or_nothing` rolls back partial admissions, `best_effort` reports per-wisp. A convoy shares one batch attribution envelope.
- **Retry/replay.** On a C18-driven retry (new `attempt_no`) the prior record is preserved and a new idempotent record is minted; redelivery of the *same* `{wisp_id, attempt_no}` is a no-op return of the existing record (INV-2) — crash-safe.

## 6. Failure modes & handling

C05 has **no assigned Gxx** in the inventory. The F-modes it touches are operational dispatch/scale modes; the gaps it *interacts with* (G34 throughput, G31 capability exposure, G36 attribution) are owned elsewhere and addressed here only at the routing seam.

| Failure | Applies to C05 how | Optimized handling |
|---|---|---|
| **Seat/quota saturation (G34 surface)** | A capped Max seat would be over-committed if C05 fired placements blind. | **DELTA-02 admission-before-commit (INV-3):** `acquire` gates every placement; on back-pressure the wisp queues + ages and retries next tick. The single-seat ceiling is honoured *at the router*; back-pressure propagates to C18's tick rather than thrashing. |
| **Pool starvation / unfairness** | Under load a naïve strategy can indefinitely pass over some wisps or hammer one rig. | **DELTA-03 aging + per-rig cap (INV-7):** effective priority rises with wait; caps bound per-rig load; `least_loaded` default spreads work. |
| **Double-dispatch on retry/crash-replay** | C18 tick redelivery or a crash mid-place could place the same wisp twice. | **DELTA-06 idempotent record (INV-2):** `dispatch_id = hash({wisp_id, attempt_no})`; re-invocation returns the existing record, never double-places. |
| **Out-of-policy placement (judge family / model floor)** | Routing a judge to the coder family, or a coder below floor, violates C29 policy. | C05 carries C29's `family` as a routing constraint and **fails to `unroutable`** when C29 fails closed (C29 DELTA-06) rather than placing a non-compliant executor. Composes with review-log D-1 (same-family judge → constraint is advisory now, but the *seam* stays). |
| **Partition violation (holdout-isolation surface, G21/G28)** | A wisp routed to a rig outside its declared read/write partition leaks scope. | **INV-5:** placement is refused (`unroutable`) when it would breach a C42 partition; C05 enforces the partition at placement, not after the fact. |
| **Capability/egress over-grant (G31 surface)** | The executor could get ambient Bash/net/fs beyond the node's need. | C05 binds the **C42/C43 capability profile** into the hand-off (C28 DELTA-04 consumes it per-invocation); C05 carries the profile, C43 defines it. Narrows the pre-twin blast-radius window at the dispatch seam. |
| **Unroutable wisp (no target / no capacity / failed policy)** | No rig matches, pool exhausted, or C29/governor refuses. | Returned as an explicit `unroutable`/`back_pressured` outcome to C18 (never a silent drop, INV-1); C18 owns the retry/escalation policy (bound decrement, fix-task, OQ2). |
| **Convoy partial failure** | Some wisps in a batch admit, others back-pressure. | **DELTA-05 atomicity policy:** `all_or_nothing` rolls back the partial batch; `best_effort` reports per-wisp and lets C18 re-drive the unplaced ones. |

## 7. Cross-cutting (security / cost / scale / observability / ops)

- **Security.** Two postures. (1) **Partition enforcement (INV-5):** C05 is a chokepoint that refuses a placement violating a C42 read/write partition — load-bearing for holdout isolation (C34/G21) because *the router decides which rig touches which work*. (2) **Capability binding:** C05 carries the C42/C43 capability/egress profile into every hand-off so the executor never gets ambient access (G31 surface, narrowed at dispatch). Every placement is attributable (`created_by`/`on_behalf_of`, C41/INV-6) — no anonymous dispatch (G36 surface).
- **Cost.** The dispatch record (DELTA-06) carries `model_family`/`cost_class` and queueing time → C46 meta-metrics can attribute **cost-per-dispatch** and **time-to-placement** to routing decisions. Admission control (DELTA-02) is the point where a budget-aware C29 cost-tier (C29 DELTA-05) translates into *not* placing when budget is exhausted.
- **Scale.** C05 is the router that makes the single-Max-seat ceiling (G34) *governed* rather than *hit blindly*: admission + back-pressure + queue/age. Throughput is bounded by C28's seat pool (C28 DELTA-03), not by C05 — C05's job is to *honour* the bound and spread load across the pool fairly (DELTA-03). C05 itself is cheap (a scheduler over a queue + counters).
- **Observability.** `DispatchRecord` is a first-class join: `dispatch_id → {wisp, binding, model_family, rig, outcome, queue_time}`. Holdout audit (C34), override audit (C35), and meta-metrics (C46) key off it to answer "what was placed where, why, and at what cost" without log reconstruction.
- **Ops.** Pool size + strategy + per-rig caps are C03 config (`[rigs]`); enabling pool routing is the Phase-0→Phase-1 step (README:364 "no multi-rig pool" at smallest install → `[rigs]` on in Phase 1). At Phase 0 (single agent, `[rigs]` off) C05 degrades to **direct single-agent placement** — the same `dispatch` path with a trivial one-member pool (no strategy needed), so the Phase-0 install needs no pool machinery.

## 8. Acceptance criteria & test strategy

1. **AC-1 (single-placement, INV-1).** A ready wisp + binding + target → exactly one executor hand-off + one `DispatchRecord`; never zero-on-success, never two. *Placement assertion against C28/C17 stubs.*
2. **AC-2 (binding pass-through, DELTA-04).** C05 routes using only the `RoutingKey`; it never re-derives `template`/`spec` (the binding is opaque). *Cross-check: a wisp with a pre-resolved binding routes without any C09 call from C05.*
3. **AC-3 (admission-before-commit, DELTA-02/INV-3).** Under a governor returning `back_pressure`, the wisp is **queued + aged**, not placed; under `grant`, placed. A capped seat is never over-granted. *Governor stub fixtures (grant / back-pressure).*
4. **AC-4 (idempotent dispatch, DELTA-06/INV-2).** Re-invoking `dispatch` for the same `{wisp_id, attempt_no}` returns the existing record and does not double-place; a new `attempt_no` mints a new record. *Replay/redelivery fixture.*
5. **AC-5 (pool fairness + no-starvation, DELTA-03/INV-7).** Over a multi-rig pool under sustained load, `least_loaded` spreads work within caps and the aging rule places every queued wisp in bounded time. *Load-simulation fixture asserting no wisp waits past the aging bound.*
6. **AC-6 (partition enforcement, INV-5).** A wisp targeting a rig outside its C42 partition returns `unroutable`, never a silent downgrade. *Partition-violation negative fixture.*
7. **AC-7 (model-policy honour).** When C29 fails closed (no compliant judge family), C05 returns `unroutable` rather than placing a non-compliant executor; the `model_family` rides the record. *C29-fail-closed stub.*
8. **AC-8 (attribution-complete, INV-6).** Every dispatch record carries `created_by` and (delegated) `on_behalf_of`. *Record assertion against a C41 stub.*
9. **AC-9 (convoy atomicity, DELTA-05).** An `all_or_nothing` convoy with one back-pressured member rolls back the whole batch; `best_effort` places the admittable ones and reports the rest. *Batch fixtures, both modes.*
10. **AC-10 (Phase-0 degrade).** With `[rigs]` off (single agent), `dispatch` places via the trivial one-member path with no pool machinery — the smallest install dispatches without a pool. *Phase-0 config fixture.*
11. **AC-11 (C18-absent build proof, OQ1).** `dispatch` + the queue/admission path build and test against C13/C19 + C28/C29 stubs with **C18 absent** — proving C18 is a caller, not a build-time dep. *Stub-driven test with no C18 present (mirrors C13 AC9).*

Sweep-1 strategy: stub C13 (`ready_frontier`), C09 (opaque binding), C29 (`ModelSelection`/fail-closed), C28 (governor grant/back-pressure), C42 (partition), C41 (actor); drive `dispatch`/`dispatch_convoy` against them and assert AC1–AC11. Concrete `RoutingDecision`/`DispatchRecord` schemas, the pool-strategy state machine + aging algorithm, and the convoy rollback protocol → sweep 2 (co-frozen with C28 governor + C29 selection + C13 frontier).

## 9. Open questions

- **OQ1 (→ [review-log](../_meta/review-log.md), top open question).** *C05 build-time dependency direction (the `Depends on: C01, C18` C18 leg).* The inventory lists C05 depending on C18, but **C18 calls C05** (reconciler drives dispatch per tick); C18 is a runtime caller, not a build-time dependency. C05's real build-time deps are C13/C19 + C09 + C29 + C28 + C42/C41. **Recommendation:** treat C01 as the only substrate dep and C18 as a caller; build/test C05 with C18 absent (AC-11). This is the exact pattern the integrator already accepted for C13-B (DELTA-06/OQ2 — same `…, C18` reversal). Needs a one-line integrator ratification.
- **OQ2.** *Who owns retry/escalation policy when C05 returns `unroutable`/`back_pressured`?* C05 reports the outcome; the *decision* to retry (decrement a molecule's `bound`, raise a `fix_task`, escalate) is C18/C39 policy (C13 §5 bound-escalation; C13 XC-3 "numerics deferred to C18/C39"). Recommend: C05 is mechanism-only (returns the outcome + retry-after); C18 owns the loop bound. Confirm the seam shape with C18/C39.
- **OQ3.** *Convoy semantics vs Gas City native `convoy`.* DELTA-05 specifies an atomicity policy, but whether Gas City exposes a native `convoy` object (with its own batching/state) or "convoy" is purely v4's name for batched sling needs the same Gas-City-reality spike as C12/C13 OQ1 (G11). Pick "v4 batches over sling" provisionally; confirm against `gc`.
- **OQ4.** *Pool placement-strategy default + affinity key.* `least_loaded` is the proposed default; `affinity` (sticky by `spec_id`/`molecule_id` for context reuse) trades load-spread for cache locality. The default strategy, the affinity key, and whether affinity is opt-in per formula node → sweep 2 (ties to C28 seat-pool locality and C29 cost-tier).
