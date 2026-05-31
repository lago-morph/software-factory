# C40 — Durable Workflow Engine (Orders)  (Spec, canonical track)

> Source: README §"Principle 11 — Self-healing loop" (line 246 "Observability → anomaly → diagnosis → fix →
> ship", durable-workflow row line 258 "Durable workflow / Survives crashes / retries / **Gas City Orders** +
> Temporal (Go SDK), Inngest, Trigger.dev / MIT / Apache 2.0 / **Orders native; Temporal optional**", summary
> line 261 "P11 is the largest custom engineering effort"); README §Part 6 Phase 3b (lines 459–466 "P11
> components (Healer in pieces) … Each piece is a separate factory build … Build the simplest first"); README
> Phase-0 install (the `orders` block is **explicitly off** at minimum, AI-CONTEXT §3.4 line "Explicitly off:
> `[daemon]`, `[mail]`, `[formulas]`, `[rigs]`, Dolt server, `[[service]]` blocks, **orders**"). AI-CONTEXT
> §3.1 P11 row (line 76 "Mechanism present (**Orders subscribing to crashes/gates**); no Healer agent
> shipped"); §3.2 concept 3 (line 87 Event Bus → P9/P10/P11); §3.3 vocab (line 109 "order | event-triggered
> workflow"); §10 layer-4 table (line 333 "Durable workflow / Temporal, Inngest, Trigger.dev, Restate,
> Hatchet / … / Very mature (generic)"); §11.1 deferral row (line 486 "Whether to add **Temporal** for
> durable workflow / **When Gas City Orders prove insufficient** / Gas City Orders may be enough; Temporal is
> fallback"); §9.1 transfusion (line 408 "Durable workflow: Temporal SDK examples …, Inngest patterns, AWS
> Step Functions"); §3.5 migration-tail risk (lines 124–129). spec/C23 §1/§5 (event bus is the trigger
> substrate; "Orders are event-triggered workflows that subscribe to events", C23 §2 + §5). component-
> inventory C40 row (line 52 "Event-triggered workflows surviving crashes/retries (Gas City Orders; Temporal
> optional)", maps A59/A22c/B38/B39, depends C23, gap G33, foundational no) + Batch-3 note (line 111);
> ambiguities-and-gaps G33; review-log D-6 (canonical track), D-8 (Order owned by C40; C07 glossary entry,
> C12 references but does not define).
> Inventory ID: C40   Kind: component   Status: sweep-1
> Track: canonical (per D-6 — no Track-A/B framing)

## 1. Purpose & responsibility

C40 is the factory's **durable-workflow seam — "Orders"**: the spec-of-record for **event-triggered
workflows that survive crashes and retries** (component-inventory C40; AI-CONTEXT §3.3 line 109 "order |
event-triggered workflow"). An Order is a workflow that is **started by an event** rather than by a direct
dispatch, and that **persists its progress** so a crash/restart of the runtime resumes it rather than losing
it (README line 258 "Survives crashes / retries"). In the P11 self-healing loop, Orders are the
**always-running glue** that watches the event bus for trigger conditions (a crash, a failed gate) and
launches the response workflow — "Mechanism present (**Orders subscribing to crashes/gates**)" (AI-CONTEXT
§3.1 line 76).

Like C23 (event bus) and C01 (substrate), C40 is **owned by the adopted Gas City substrate (MIT)**, not
factory-authored: **Gas City Orders are NATIVE** (durable, event-triggered, crash-surviving) (README line 258
"Orders native"). C40's deliverable is therefore **the seam spec of-record for the Order primitive** — what
an Order *is*, how it is triggered off C23 events, what state survives a crash, and the contract handed to
its P11 consumer (C39 fix-task loop-closure — *inferred* as the workflow an Order most naturally drives:
v4 states only "Orders subscribing to crashes/gates" (AI-CONTEXT §3.1 line 76), and C39's own declared
deps are C38/C20/C08, so this launch coupling is C40's faithful inference, not a v4-stated wiring — see
§2 and OQ-4). Per
**D-8**, "Order" (durable event-triggered workflow) is **owned by C40** (this component is its home); C12
formula files *reference* Orders but do not define them; **C07 carries the glossary entry** (C07 line 125).

C40 is **NOT foundational** (component-inventory line 52, "foundational? no") and is **off at minimum
install** — the `orders` block is in Phase-0's "Explicitly off" list (AI-CONTEXT §3.4). It is **built in
inventory Batch 3** (component-inventory line 111, the workflow-tooling batch — "…durable Orders") so the
Order seam is *standing before* the **README Phase-3b** P11 Healer pieces (anomaly/clustering/diagnosis/
fix-task/loop-closure = C36–C39, inventory Batch 4) turn on and consume it. NB: inventory "Batch *n*" and
README "Phase *n*" are **distinct, non-aligned** decompositions — C40 is *not* itself one of the README
Phase-3b build bullets (which are the Healer pieces, README lines 459–466); Orders appear only as the P11
*capability* row, README line 258. The Order capability is enabled when the self-healing loop is built.

**Responsibilities (what C40 is the spec-of-record for):**
- **Event-trigger binding** — an Order declares a *trigger condition over C23 events* (e.g. an event of a
  given `action_type` such as a crash or a failed gate); when a matching event appears on the bus, the Order
  fires (AI-CONTEXT §3.1 line 76 "Orders subscribing to crashes/gates"; trigger substrate = C23).
- **Durable execution** — the Order's in-flight progress is **persisted** so a runtime crash/restart
  **resumes** it from where it was rather than re-running from scratch or dropping it (README line 258
  "Survives crashes / retries").
- **Retry on failure** — a failed step is retried (README line 258 "retries"); the retry policy is a
  property of the Order, supplied by Gas City.
- **Glue, not logic** — an Order *triggers and drives* a workflow (typically a formula/molecule or a
  fix-task chain); the workflow's own steps are owned elsewhere (C12 formula, C39 fix-task). C40 owns *that
  the trigger-and-survive mechanism exists*, not the response content.
- **Durability-ceiling disclosure (G33)** — C40 documents **honestly** what Gas City Orders' crash/retry
  survival does and does not cover (§6), rather than hardening it.

**Explicitly NOT (boundaries):**
- **NOT factory-authored, and NOT a new durable-workflow engine.** Gas City Orders are **native** (README
  line 258). C40 is the *seam spec over the adopted Order primitive*, not a Go engine. **No custom
  durable-workflow engine, no saga/compensation framework, no state-machine runtime is built** — the bar
  drops any such custom capability because the principle (P11 durability) is *already met natively* by Orders.
  (Mirrors C23/C01's adoption boundary.)
- **NOT Temporal.** Temporal is the **explicitly optional / deferred fallback** — "Orders native; **Temporal
  optional**" (README line 258), added only "**When Gas City Orders prove insufficient**" (AI-CONTEXT §11.1
  line 486). C40 does **not** build a Temporal integration at sweep 1; Temporal is named as the documented
  upgrade path (and transfusion exemplar, §9.1 line 408) and nothing more. See §6 (durability ceiling) and
  §9 (the "Orders insufficient?" trigger is the open question).
- **NOT the event bus.** C23 owns the append-only JSONL action log, the monotonic `seq`, and the
  ordered-read/checkpoint surface Orders *consume* to detect their triggers (spec/C23 §1, §3 I2). C40 is the
  *subscriber/workflow* layer over that stream; it does not own the log, its ordering, or `created_by`.
- **NOT the formula/molecule.** A **formula** (C12) is the TOML DAG *template* for a workflow and a
  **molecule** (C13) is an instantiated bead-tree run of one. An **Order** is the *event-trigger + durability
  wrapper* that may *launch* such a workflow. v4 names these as **distinct** (AI-CONTEXT §3.2 concept 7 vs
  §3.3 "order"); C12 §1 explicitly defers the Order definition here (C12 line 59, D-8). C40 does not own DAG
  structure, node kinds, or linting.
- **NOT a convoy.** A **convoy** (atomic multi-bead dispatch) is a *sling/dispatch* concept owned by **C05**
  (D-8). C40 ≠ C05. An Order is event-*triggered*; a convoy is a *batched dispatch* unit.
- **NOT the Healer / diagnosis logic.** "Orders subscribing to crashes/gates" is the *mechanism*; "**no
  Healer agent shipped**" (AI-CONTEXT §3.1 line 76) — the anomaly→diagnosis→fix *content* is C36/C37/C38/C39.
  C40 provides the durable event-triggered *carrier*; what the triggered workflow *does* is the Self-Healing
  Loop's job. In particular **loop-closure / fix-task re-entry is C39** — C40 may be the Order that *drives*
  a fix-task workflow, but the termination/escalation contract and the bead chain are C39's.
- **NOT the reconciler / Health Patrol.** C18 is the *per-tick desired-state convergence* control loop
  (AI-CONTEXT §3.2 concept 9). An Order is *event-triggered and durable across crashes*, a different
  primitive from the polling reconciler; C40 does not own convergence gates.
- **NOT a message broker / queue.** Like C23, "Orders" are a Gas City primitive, not Kafka/NATS; durable
  inter-agent messaging is **Mail+Nudge (C06)**. C40 introduces no external queue (consistent with the
  "no Postgres/Redis/Kafka" stance, AI-CONTEXT §5.3).

## 2. Context & dependencies

| Direction | Component | Relationship |
|---|---|---|
| Upstream (depends on) | **C23** Event Bus | The **trigger substrate**. Orders *subscribe to* C23 events and fire on a matching `action_type` (AI-CONTEXT §3.1 line 76; spec/C23 §2 lists C40 as a downstream consumer, §5 "Orders are *triggered* by matching events"). C40 reads via C23's ordered-read/checkpoint surface (C23 I2/I3). **Sole declared dependency** (component-inventory line 52). |
| Upstream (host) | **C01** Gas City substrate | Orders are a Gas City primitive hosted by the substrate; gated on by the `orders`/daemon config (off at minimum, AI-CONTEXT §3.4). C40 inherits Gas City's migration-tail risk (§3.5) like C01/C23. |
| Upstream (config) | **C03** Config / feature-flags | Section-presence enables Orders (the `orders` block); off in Phase 0, enabled when the self-healing loop is built (AI-CONTEXT §3.4; C03 model). |
| Tightly-coupled consumer (inferred) | **C39** Fix-task generation & loop-closure | **Inferred** canonical workflow an Order drives in P11: a crash/anomaly event triggers an Order that drives the fix-task → resolution chain. *This launch coupling is C40's faithful inference, not a v4-stated fact* — v4 states only "Orders subscribing to crashes/gates" (AI-CONTEXT §3.1 line 76), describes the fix-task→resolution chain as a "Custom bead chain" (README lines 257–259) without naming Orders as its carrier, and C39's declared deps are C38/C20/C08 (inventory line 51), not C40. C40 supplies the *durable event-triggered carrier*; C39 owns the fix-task bead chain + termination/escalation (G35). Confirm the seam at OQ-4. |
| Peer (vocabulary) | **C07** glossary; **C12** formula | C07 carries the *Order* glossary entry (D-8; C07 line 125). C12 *references* Orders but defines them here (D-8; C12 §1 line 59). The workflow an Order launches is typically a C12 formula / C13 molecule. |
| Upgrade path (deferred) | **Temporal** (MIT) | The optional fallback if Orders prove insufficient (AI-CONTEXT §11.1 line 486); **not built** at sweep 1. Also the transfusion exemplar for durable-workflow patterns (§9.1 line 408). |

**Position in the system.** C40 sits in the **Self-Healing Loop** subsystem and is built in **Batch 3 /
Phase 3b** (component-inventory line 111; README line 459 "Each piece is a separate factory build"). It is a
**thin seam over a native Gas City primitive** — its job is to specify *how* the self-healing workflows are
triggered-and-survived, not to add an engine. It is **off until P11 is built** (Phase-0 "Explicitly off"
list, AI-CONTEXT §3.4); the minimal factory never instantiates an Order.

## 3. Interfaces / contracts

Sweep-1: interfaces **named and described**; concrete Order-definition syntax, trigger-predicate grammar, and
state/retry wire contracts defer to sweep 2 (and to the pinned Gas City `orders` semantics — **G11 caution:
do not bind to invented `gc` Order internals**; names below are *roles*, not asserted `gc` API).

| # | Interface | Direction | Description | Owning/detailing component |
|---|---|---|---|---|
| I1 | **Order definition / registration** | inbound (config) | Declare an Order: a **trigger predicate over C23 events** + the **workflow it launches** + a **retry policy**. Enabled by the `orders` config block (off at minimum). Concrete TOML shape = sweep-2 / pinned `gc`. | C40 (seam); C03 (flag); C01 (host) |
| I2 | **Event-trigger subscription** | inbound (read) | C40 consumes C23's **ordered-read / tail / checkpoint** surface (C23 I2/I3) to watch for events matching an Order's trigger predicate; fires the Order on a match. Resumes from its last-processed `seq` after a restart (the property that makes triggering crash-safe). | **C23** (provides stream + checkpoint), C40 (subscriber) |
| I3 | **Order execution / launch** | outbound | On trigger, the Order **launches its workflow** — typically a C12 formula instantiated as a C13 molecule, or a C39 fix-task chain. C40 owns *that the launch happens durably*; the launched workflow's steps are owned downstream. | C40 (launch), C12/C13/C39 (workflow content) |
| I4 | **Durable state / resume** | internal (state) | The Order's **in-flight progress** is persisted by Gas City so a crash/restart **resumes** it (what survived is the durability ceiling, §4/§6). C40 specs the *contract* ("progress survives crash"); the backing store is Gas City's. | **Gas City** (mechanism), C40 (contract) |
| I5 | **Retry policy** | internal (config) | A failed step is retried per the Order's policy (README line 258 "retries"). The policy is an Order property; defaults + bounds are Gas City's. | **Gas City** (mechanism), C40 (contract) |
| I6 | **Temporal upgrade seam (latent)** | outbound (deferred) | The named, **unbuilt** fallback: if Orders prove insufficient, the durable-workflow role is satisfied by Temporal behind this same triggering/durability contract (AI-CONTEXT §11.1 line 486). Documented, not wired. | (deferred) |

**Invariants C40 must uphold (Order-level):**
- **INV-1 (event-triggered):** an Order is **started by a matching C23 event**, not by direct dispatch
  (AI-CONTEXT §3.3 line 109 "event-triggered workflow"; §3.1 line 76). The trigger source is the event bus.
- **INV-2 (durable progress / crash-resume):** an Order's in-flight progress **survives a runtime
  crash/restart** and **resumes** rather than being lost or silently restarted (README line 258). This is the
  native Gas City guarantee C40 is the spec-of-record for — and an **adopted** property *verified* by the
  conformance pack (AC-2), not one C40 independently enforces over Gas City's internals (same G11-class
  "exercise the upstream claim" posture as C23/C01).
- **INV-3 (retried on failure):** a failed step is retried per the Order's policy (README line 258); retries
  are bounded (the bound is a Gas City property, surfaced at I5).
- **INV-4 (trigger crash-safety via C23 checkpoint):** because triggering rides C23's ordered/checkpointed
  stream (I2; C23 INV-2), an Order that was waiting for a trigger **does not miss the event** across a
  restart — it resumes reading from its last-processed `seq` (inherited from C23, not independently built).
- **INV-5 (no custom engine):** C40 adds **no factory-authored durable-workflow machinery** — the durability
  comes from Gas City Orders (or, deferred, Temporal). This is a *boundary* invariant the bar enforces.

## 4. Data model / state

C40 *owns the Order seam + the trigger/durability contract*; the **backing persistence is Gas City's** and
the **event stream it reads is C23's**. State C40 is the spec-of-record for at sweep 1:

| State | Description | Persistence | Detailed by |
|---|---|---|---|
| **Order definition** | The declared trigger predicate (over C23 `action_type`/event shape) + launched workflow + retry policy. | Version-controlled config (the `orders` block; C03 model). | C40 (seam); C03 (config) |
| **In-flight Order progress** | The durable execution state of a *running* Order — which step it reached — so a crash resumes it (INV-2). | **Gas City Order backing store** (substrate-owned; exact store = pinned `gc`). | **Gas City** (store), C40 (contract) |
| **Trigger checkpoint** | The Order subscriber's last-processed C23 `seq` (so it resumes triggering after restart, INV-4). | C23's checkpoint surface (C23 I3), not a C40-owned store. | **C23** |
| **Retry counter / bound** | Per-step attempt count against the policy bound (INV-3). | With the in-flight Order state (Gas City). | **Gas City**, C40 (contract) |

> [FAITHFUL-FILL] v4 specifies the Order *primitive* ("event-triggered workflow, survives crashes/retries",
> README line 258; AI-CONTEXT §3.3 line 109; §3.1 line 76) but not the concrete Order-definition record. The
> minimal faithful elaboration of one Order is: **`{trigger: <predicate over C23 events>, launches: <formula|
> fix_task workflow ref>, retry: <policy>}`** — the smallest set implied by "event-triggered" (needs a
> trigger predicate over the bus) + "drives a workflow" (needs a launch target) + "survives retries" (needs a
> retry policy). Field-level names/types and the trigger-predicate grammar (how an Order matches a C23
> `action_type`/`target_ref`) are **sweep-2** and must bind to the **pinned `gc` Order syntax**, not invented
> internals (G11). The in-flight progress record is **Gas City's**, not C40's to define.

**Consistency / lifecycle.** An Order is **declared once** (config), then **dormant** until its trigger
fires; on a matching C23 event it **launches** its workflow and **persists progress** until completion;
across a crash it **resumes**. The Order primitive is **additive and off by default** (Phase-0 "Explicitly
off", AI-CONTEXT §3.4) — nothing in the minimal factory creates an Order; the capability is *enabled* in
Phase 3b when the self-healing loop is built. The durability is **as deep as Gas City Orders go and no
deeper** — see §6 (G33 ceiling): C40 does not add replication, exactly-once, or cross-process saga semantics.

## 5. Behavior

**Enable (Phase 3b).** Orders are turned on via the `orders` config block (off at minimum, AI-CONTEXT §3.4);
this is part of building the self-healing loop (README line 459 "Each piece is a separate factory build").

**Declare an Order (config path).** An operator/pack declares an Order via I1: a trigger predicate over C23
events (e.g. `action_type = crash` / a failed-gate event), the workflow it launches (a C12 formula or C39
fix-task chain), and a retry policy.

**Trigger + launch (run path).**
1. C40's subscriber tails C23's ordered event stream (I2; C23 I2/I3), checkpointing its position by `seq`.
2. When an event **matches** an Order's trigger predicate (INV-1), the Order **fires**.
3. The Order **launches** its workflow (I3) — instantiating a C12 formula as a C13 molecule, or driving a
   C39 fix-task chain.
4. Gas City **persists the Order's progress** (I4, INV-2); failed steps are **retried** per policy (I5,
   INV-3).

**Crash + resume (durability path).**
- If the runtime crashes mid-Order, on restart Gas City **resumes** the in-flight Order from its persisted
  progress (INV-2) rather than dropping or blindly re-running it.
- A waiting (not-yet-triggered) Order resumes reading C23 from its checkpointed `seq` (INV-4) so it **does
  not miss** a trigger event that landed around the crash — this crash-safety is *inherited from C23's
  ordered/checkpointed log*, the reason C23 is the trigger substrate.

> Sequence/state diagrams (Mermaid), the exact Order-definition TOML, the trigger-predicate grammar, the
> retry-policy schema, and the resume semantics are **sweep-2+**, and must be pinned against the real `gc`
> Order behaviour (G11). The workflow an Order launches is owned by C12/C13 (formula/molecule) or C39
> (fix-task); its termination/escalation is C39's.

## 6. Failure modes & handling

C40's failure story is **the honest durability ceiling of Gas City Orders (G33)** — the one gap assigned to
it — plus the boundary discipline of not over-building.

**G33 (major) — no story for partial/cascading failure of the OSS stack; "Gas City Orders survive crashes"
is claimed for Gas City only (the durability ceiling).** This is C40's assigned gap and it is a **document-
the-ceiling-honestly, do-not-harden** obligation (per the dispatch + the G33 finding text: *"'Gas City Orders
survive crashes' is claimed for Gas City only"*).

> [AMBIGUITY: G33] Two readings of C40's obligation. **(a)** *C40 must build the missing degradation/retry/
> circuit-breaker design for the whole OSS stack* (CXDB down, LangFuse losing traces, a Python tool node
> OOMing) **so that Orders paper over partial stack failure**. **(b)** *C40 owns only the Order primitive's
> own durability and must document its ceiling honestly* — Orders survive **Gas-City-internal** crashes/
> retries, and **do not** by themselves make the *non-Gas-City* OSS components (CXDB, LangFuse, Python tool
> nodes) fault-tolerant. **Chosen: (b).** This is most consistent with the rest of v4 and with the bar: the
> G33 finding itself says the crash-survival claim is *"for Gas City only"*; v4 locates the *store/bridge*
> partial-failure obligation at **C21/C24** (C21 §6 fail-open; C24 retain-in-inbox + bounded retry —
> *already discharged there*), not at the Order layer; and building a stack-wide circuit-breaker/degradation
> framework here is exactly the **custom non-principle hardening the bar drops** ("MORE capability tied to a
> specific 12-principle? … non-principle → DROP"). C40's faithful contribution is therefore to **state the
> ceiling**, not raise it.
>
> **The durability ceiling — what survives, what does not (honest disclosure):**
> - **Survives (native Orders, INV-2/INV-3):** a **Gas-City-internal crash/restart** of an in-flight Order
>   (progress is persisted and resumed) and a **failed step** (retried per policy). This is the P11 guarantee
>   v4 actually claims (README line 258).
> - **Does NOT survive / is NOT covered by Orders alone (the ceiling):**
>   - **Non-Gas-City OSS-component failure** — an Order driving a workflow that calls **CXDB** (down),
>     **LangFuse** (losing traces), or a **Python tool node** (OOM) does not make those components
>     fault-tolerant; the Order will retry the *step*, but the *dependency's* availability is owned at its own
>     seam (CXDB outage → C21 §6 fail-open + C24 buffer; tool-node OOM → C17/C36 Python-node concern). G33's
>     *cross-component cascade* design is explicitly **not** C40's to invent.
>   - **Anything Gas City Orders themselves do not persist** — exactly-once side effects, distributed/
>     cross-process saga rollback, and HA/replication of the Order backing store are **not** asserted by v4
>     and **not** built here. If a use case needs them, that is the documented "**Orders prove insufficient**"
>     trigger to consider **Temporal** (AI-CONTEXT §11.1 line 486) — a *deferred* decision, not sweep-1 work.
>   - **Unverified upstream specifics** — *how deep* Orders' crash-resume goes (mid-step vs step-boundary
>     resume, retry-bound defaults, idempotency of a re-launched workflow) is an **unverified Gas City
>     assumption** (G11) until exercised against the pinned binary (AC-2/OQ-1). The ceiling is documented as
>     "as deep as the pinned `gc` proves, and no deeper".

**F-modes.** C40 has **no F-mode uniquely assigned** to it in F-MODE-COVERAGE (the Layer-4/P11 modes F4/F7/
F22/F23/F24/F40/F57 are owned by the **Healer/anomaly/diagnosis** content — C36/C38 — not by the durable-
trigger carrier). C40's contribution is *enabling*: it is the **durable event-triggered carrier** that lets
the P11 mechanism *run at all* and *survive a crash mid-heal*, so the self-healing loop it carries (and the
F-modes that loop addresses) are not lost to a restart. The canonical F-mode mapping is **owned by C57**;
C40 surfaces only its own failure class (the G33 durability ceiling) and defers the mapping there.

**Degraded behaviour.** If the trigger substrate (**C23**) is unavailable, no Orders fire — but C23 is the
always-on substrate log and is the *last* thing to fail (spec/C23 §6); when it returns, Orders resume from
their checkpoints (INV-4). If a launched **workflow's dependency** is down, the Order **retries the step**
(INV-3, fail-open to the run) and the dependency's own seam owns recovery (C21/C24). If the **Order backing
store** itself is lost, that is a substrate-level (C01) failure — faithful handling is to surface it, not to
build store-replication here (the ceiling, above).

## 7. Cross-cutting (security / cost / scale / observability / ops)

- **Security.** Orders fire from C23 events, which carry universal `created_by` (C23 INV-3) — so a
  triggered/durable workflow is **attributed** like any other action (P9). C40 adds no new actor surface; it
  inherits C41's attribution and C23's trigger provenance. A malicious/unsigned event triggering an Order is
  the same **F32 (mail-injection / unsigned coordination)** class C23 carries (deferred optional HMAC, C41) —
  C40 does **not** add a separate signing layer (bar: non-principle hardening → DROP).
- **Cost.** Orders are local Gas City mechanism (no managed-workflow fees, consistent with "no Postgres/
  Redis/Kafka", AI-CONTEXT §5.3). v4 gives no per-Order cost model; a misconfigured trigger that fires too
  often is a known operational concern (OQ).
- **Scale.** Orders subscribe to the C23 stream; they scale by **resuming from a checkpoint**, not
  re-reading (inherited from C23 I3). v4 names no bound on concurrent in-flight Orders → a known limitation
  (OQ). The single-Max-seat agent-throughput ceiling (G34) sits on the *workflow* the Order launches, not on
  the trigger mechanism — out of C40 scope.
- **Observability.** An Order's own lifecycle (triggered / running / resumed-after-crash / failed-retry) is
  itself recorded on the C23 event bus (every action emits an event, C23 INV-4) — so Orders are observable
  through the same audit trail, and their progress is visible to the P11 loop they serve.
- **Ops.** **Off at minimum** (`orders` in the Phase-0 "Explicitly off" list, AI-CONTEXT §3.4); enabling it
  is a Phase-3b step. Inherits Gas City's **migration-tail risk** (AI-CONTEXT §3.5): an Order-semantics or
  config-format change upstream would ripple here — **pin the Gas City version** (mirrors spec/C01 INV-1,
  spec/C23 §7). The "Orders insufficient → Temporal" upgrade is an ops/architecture decision, deferred
  (AI-CONTEXT §11.1 line 486).

## 8. Acceptance criteria & test strategy

Sweep-1 = high-level criteria (concrete tests at sweep 2, against the **pinned** Gas City binary).

1. **AC-1 (event-triggered — INV-1/I1/I2):** an Order declared with a trigger predicate over C23 events
   **fires** when (and only when) a matching event appears on the bus (AI-CONTEXT §3.1 line 76).
2. **AC-2 (crash-resume — INV-2/I4, the core durability claim):** an in-flight Order **survives a runtime
   crash/restart** and **resumes** from its persisted progress (does not drop, does not blindly re-run from
   scratch) (README line 258). *This is the claim G33 says is asserted "for Gas City only" — AC-2 exercises
   it against the real bus to establish the actual ceiling depth.*
3. **AC-3 (retry on failure — INV-3/I5):** a failed step is **retried** per the Order's policy, within a
   bounded number of attempts (README line 258).
4. **AC-4 (trigger crash-safety — INV-4):** an Order waiting for a trigger **does not miss** a trigger event
   that lands around a crash — on restart it resumes reading C23 from its checkpointed `seq` (inherited from
   C23 I3).
5. **AC-5 (off-by-default — Phase-0 boundary):** the minimal Phase-0 install (no `orders` block) instantiates
   **no** Orders; the capability is inert until enabled (AI-CONTEXT §3.4).
6. **AC-6 (no custom engine — INV-5, the bar):** the durability/triggering is provided by the **adopted Gas
   City Order primitive** — there is no factory-authored durable-workflow engine, saga framework, or
   state-machine runtime in C40's deliverable.
7. **AC-7 (durability-ceiling honesty — G33):** the spec **states explicitly** what Orders do and do not
   cover (Gas-City-internal crash/retry yes; non-Gas-City OSS-component fault-tolerance no; exactly-once /
   HA / cross-process saga no → that is the Temporal-deferral trigger). Verified as a **documentation/review
   gate**, not by hardening.
8. **AC-8 (drives the P11 workflow — I3):** an Order can launch its workflow (a C12 formula/C13 molecule or a
   C39 fix-task chain) on trigger, so the self-healing loop's response runs durably (README §3b).

**Test strategy.** A **Gas-City-Orders conformance pack** (mirroring the C01/C21/C23 conformance shape) that
boots the **pinned** Gas City substrate with the `orders` block enabled and asserts AC-1…AC-8 against the
*real* Order primitive — in particular **AC-2 (crash-resume) and AC-4 (trigger crash-safety)**, which
establish the *actual* durability ceiling the G33 disclosure (§6) must report. This conformance is the
de-risking gate that must pass before **C39** (fix-task loop-closure) relies on Orders to drive its workflow.

## 9. Open questions

- **OQ-1 (→ review-log, top): the "Orders prove insufficient → Temporal" trigger is undefined.** v4 defers
  Temporal "**When Gas City Orders prove insufficient**" (AI-CONTEXT §11.1 line 486) but **never states the
  threshold** — what concrete durability shortfall (missing exactly-once? no cross-process saga? resume
  granularity too coarse? backing-store HA?) flips the decision. Until AC-2/AC-4 exercise the *real* Order
  ceiling, "sufficient" is unmeasurable. Freeze the threshold at sweep 2 once the conformance pack reports
  what Orders actually guarantee. *(This is the load-bearing open question: it converts the deferred
  Temporal bet into a falsifiable trigger.)*
- **OQ-2 (→ review-log): Order-definition syntax + trigger-predicate grammar must bind to pinned `gc`.** The
  §4 [FAITHFUL-FILL] record (`{trigger, launches, retry}`) and *how* a trigger matches a C23 event
  (`action_type`/`target_ref` predicate) are sweep-2 and must use the **real Gas City `orders` syntax**, not
  invented internals (G11 caution). Frozen before C39 contracts against it.
- **OQ-3: durability-ceiling depth (G33) is unverified.** Does crash-resume restart mid-step or only at step
  boundaries? Are re-launched workflows idempotent? What is the default retry bound? These set the *exact*
  ceiling the §6 disclosure reports and must be confirmed against the pinned binary (mirrors the C21/C23
  "exercise the upstream claims" thread).
- **OQ-4: C40↔C39 launch seam.** Confirm the contract by which an Order *drives* a C39 fix-task chain (who
  owns termination/escalation when the durable workflow itself loops — C39 per G35) and whether an Order ever
  launches a plain C12 formula directly vs always via a fix-task bead.
