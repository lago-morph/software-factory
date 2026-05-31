# C31 — Scenario Runner  (Spec, canonical track)

> Source: README §"Principle 5 — Scenarios as held-out test set" (line 172 "Scenario runner | Executes
> scenarios against the system | Inspect AI runner | MIT | Gas City pack"; line 177 "Install Inspect AI,
> write a small pack that exposes it as a tool node"), §Part 6 Phase 2 (line 423 "Install Inspect AI (MIT)";
> line 424 "Build Gas City pack wrapping Inspect AI as a scenario provider (the `[[service]] type =
> "inspect_ai"` block)"; line 439 "**P5** … Inspect AI handles storage + execution; scenario-to-bead binding
> via pack"; line 442 "The harder parts are the Inspect AI wrap and the scenario isolation policy"); AI-CONTEXT
> §7 "Layer 2" (line 300 "Scenario runner | Inspect AI runner | MIT | Recommended"), §4.3 (line 176 raw-API-bodies
> escape hatch, line 178 correlation attributes incl. `session.id`), §11.1 (line 467 "Inspect AI for Layer 2 —
> Yes — Most mature general-purpose; agent-trajectory model fits"), §12 (line 512 "**Inspect AI's session-id
> model vs Gas City's**: likely needs adapter layer; impedance unknown" — **G25**), §13.3 (lines 599–608 Inspect
> AI invocation as a Gas City `[[tool]] type="subprocess"` running `inspect eval {scenario_path} --task {task}`
> with `work_partition = "scenarios"`; lines 587–596 the `scenario_authoring` vs `implementer` rig partitions);
> component-inventory C31 row (line 43 "Executes scenarios against the system (Inspect AI runner wrapped as
> pack); needs session-id adapter", maps A47/A28i/A28j/B42/B49, depends C30+C17, gap G25, foundational no) +
> Batch-3 note (line 111); component-inventory-A A47 (line 151 "Inspect AI runner; Gas City pack"), A28i (line
> 229 "Inspect AI subprocess tool node — Gas City `[[tool]] type="subprocess"` invoking `inspect eval`"), A28j
> (line 230 "Inspect AI `[[service]]` provider block — `type = "inspect_ai"`"); component-inventory-B B42 (line
> 54), B49 (line 61 "Inspect AI … multi-slot (authoring+runner+judge+aggregation)"); spec/C17 §3 (tool-node
> abstraction; C17 lists C31 as an instance, line 64), spec/C02 (subprocess ABI); ambiguities-and-gaps G25;
> review-log D-6 (canonical track), D-13 (C34 owns read-isolation enforcement; C42 provides the partition).
> Inventory ID: C31   Kind: component   Status: sweep-1
> Track: A (faithful)

## 1. Purpose & responsibility

C31 is the factory's **scenario runner**: the **Inspect AI runner wrapped as a Gas City pack** that
**executes held-out scenarios against the system** and emits each run's **agent trajectory** for the judge
(C32) to score. v4 is explicit that the runner itself is **off-the-shelf** — "Scenario runner | Executes
scenarios against the system | **Inspect AI runner** | MIT | Gas City pack" (README:172), "Inspect AI handles
storage + execution" (README:439). C31 therefore does **not** build a runner, a scheduler, or an eval loop;
those are Inspect AI's `inspect eval`. C31 is the **two pieces of glue v4 actually asks the factory to
build**:

1. **The wrap** — expose Inspect AI to the workflow engine as a Gas City **`[[service]] type="inspect_ai"`
   provider block** (A28j; README:424) invoked through a **`[[tool]] type="subprocess"`** tool node that runs
   `inspect eval {scenario_path} --task {task}` in the scenario rig (A28i; AI-CONTEXT §13.3 lines 599–608),
   bound to the engine via the **C17 tool-node abstraction** over the **C02 subprocess ABI**.
2. **The session-id adapter** (G25) — the genuine custom code that **threads Claude Code's `session.id` into
   scenario execution so trajectories thread**: it reconciles Inspect AI's own session/sample identity model
   with the Gas City + Claude Code `session.id` (AI-CONTEXT §4.3 line 178) so that the turns a scenario run
   provokes are attributable to *that run* and chain into one coherent trajectory downstream (CXDB via C24,
   judge via C32).

C31 is **half of the P5 mechanism** (the *execution* half). P5's other halves are owned elsewhere: scenario
**authoring + storage with read-isolation** is **C30**, and **holdout-integrity enforcement/audit** is **C34**
(D-13). C31 only **runs** the scenarios C30 stores; it is a leaf component delivered in **Batch 3 / Phase 2**
(component-inventory line 111; README Phase 2).

**Responsibilities (what C31 is the spec-of-record for):**
- **Wrap Inspect AI as a scenario provider** — the `[[service]] type="inspect_ai"` block (A28j) and the
  `[[tool]] type="subprocess"` node that shells `inspect eval` (A28i), packaged as a Gas City pack (A47;
  README:172/424).
- **Execute a scenario against the system on demand** — given a scenario reference (from C30) and a task,
  invoke `inspect eval {scenario_path} --task {task}` and run it to completion, in the **scenario rig**
  (`work_partition = "scenarios"`, AI-CONTEXT §13.3 line 607).
- **Own the session-id adapter (G25)** — map/inject `session.id` across the Inspect-AI ↔ Gas-City/Claude-Code
  boundary so the run's emitted turns thread into one trajectory; surface the run's `session.id` so C24
  (telemetry→CXDB) and C32 (judge) can find the right trajectory.
- **Surface the run's trajectory + result as the step product** — make Inspect AI's trajectory/sample output
  and exit status available to the workflow engine (C17) and to the judge (C32) as the tool node's declared
  output (README:439 "scenario-to-bead binding via pack").
- **Be a C17 tool node over the C02 ABI** — packaged + invoked per the tool-node/pack contract, not a Python
  or Go import of the engine (C17 §1; README:177).

**Explicitly NOT (boundaries):**
- **NOT the runner engine.** Inspect AI's `inspect eval` *is* the runner/scheduler/eval-loop (README:172;
  AI-CONTEXT §7 line 300; §11.1 line 467). C31 **wraps and invokes** it; it does **not** implement a custom
  runner, scheduler, retry loop, or parallel-eval engine. *(Building one would be the over-build the bar
  forbids — see §6.)*
- **NOT scenario authoring or storage.** The Inspect AI **Task DSL** and the **read-isolated scenario store**
  (separate git repo + rig partition) are **C30** (README:170–171; A45). C31 receives a scenario *reference*
  and a task; it does not define the scenario format or own the store.
- **NOT holdout-integrity enforcement or audit.** Whether the implementer agent could read scenarios, the
  `scenarios ∉ read_partition(worker)` policy, and the after-the-fact leakage audit are **C34** (D-13;
  F-MODE F28); the rig partition C34 enforces is **provided by C42** (D-13). C31 simply *runs inside* the
  scenario rig; it does not police access. *(C31's read-isolation contribution is purely positional — it
  executes in `work_partition="scenarios"`, the partition C34/C42 govern.)*
- **NOT the judge / scorer.** Scoring a trajectory against a scenario (LLM-as-judge) is **C32**; satisfaction
  aggregation (Inspect AI score reduction) is **C33** (README:185/188). Inspect AI is *multi-slot*
  (authoring+runner+judge+aggregation, B49) but C31 occupies **only the runner slot** — it executes and emits
  the trajectory; C32 consumes it. C31 does not compute satisfaction or a pass/fail verdict.
- **NOT the telemetry→CXDB bridge.** Persisting the run's trajectory turns into CXDB is **C24** (raw-API-bodies
  → CXDB). C31 *makes the run happen and tags it with `session.id`*; C24 *delivers the resulting turns*. C31
  does not post to CXDB. *(The adapter's job is to make the `session.id` correct so C24's parent-chain lands
  the turns under the right trajectory — AI-CONTEXT §5.4.)*
- **NOT the digital twins.** Scenarios run against **twins** rather than production for critical external deps
  (F-MODE F12/F54; README:195); the twins are **C44**. C31 executes whatever target the scenario/task
  configures; it does not provide or select the twin.
- **NOT cross-family enforcement.** "Judge ≠ coder model family" is a C29/model-stylesheet rule (README:189);
  irrelevant to the runner. (And per review-log D-1, the cross-family rule is relaxed to same-provider for now.)

## 2. Context & dependencies

| Direction | Component | Relationship |
|---|---|---|
| Upstream (depends on) | **C30** Scenario store w/ isolation | Authors + stores scenarios (Inspect AI Task DSL) in the **read-isolated** `scenario_authoring` rig; hands C31 a **scenario reference** (`{scenario_path}`) + task to execute. Inventory C31 "Depends on: C30". C31 *executes* what C30 *stores* (keeps the author/execute split; D-13 read-isolation). |
| Upstream (depends on) | **C17** Tool-node abstraction | C31 is placed in a formula/molecule as a **deterministic-shaped tool node** (`inspect eval` subprocess) referenced by name; C17 gives the uniform by-name placement over the C02 ABI (C17 §3, lists C31 as an instance, line 64). Inventory C31 "Depends on: C17". |
| Underlying ABI | **C02** Pack/tool-node ABI | The `[[tool]] type="subprocess"` wire contract (command/args/work_partition/exit-status) C31's `inspect eval` node is realized over (AI-CONTEXT §13.3; C17 §3 Reading A). |
| The wrapped OSS | **Inspect AI** (B49; `github.com/UKGovernmentBEIS/inspect_ai`) | The MIT runner C31 wraps — provides `inspect eval`, the trajectory/sample model, and the session/sample identity C31's adapter reconciles. C31 supplies *no* runner of its own. |
| Identity source | **Claude Code `session.id`** (AI-CONTEXT §4.3 line 178) | The correlation attribute the adapter threads into the run so emitted turns chain into one trajectory; also "Gas City session resume + Claude Code session-id" for cross-session continuity (README:240). |
| Downstream (consumer) | **C32** Judge harness | Scores the trajectory C31 emits against the scenario. C31 produces the trajectory + run identity; C32 consumes it. |
| Downstream (consumer) | **C24** Telemetry→CXDB bridge | Delivers the run's emitted turns into CXDB, parent-chained via `session.id` (AI-CONTEXT §5.4); the adapter's correct `session.id` is what makes that landing coherent. |
| Governed-by (positional) | **C34** Holdout enforcement, **C42** Role/rig partition | C34 enforces `scenarios ∉ read_partition(worker)` + audits leakage (D-13); C42 provides the partition. C31 *runs inside* the `scenarios` work-partition they govern; it does not enforce. |
| Packaging host | **C02/C17** pack + tool-node ABI | C31 ships as a Gas City pack (the `[[service]] type="inspect_ai"` + `[[tool]]` blocks), not a Go/Python import (README:177; C17 §1). |

**Position in the system.** C31 is **Batch 3 / Phase 2** (component-inventory line 111; README:417): it stands
up once Inspect AI is installed and C30's scenario store + C17/C02 tool-node ABI exist. It is **not
foundational** (inventory C31): it is a leaf of the evaluation tier that the bootstrap-validation milestone
exercises (README:429 "Run the factory on the spec"). v4 flags that "the harder parts are the **Inspect AI
wrap** and the scenario isolation policy" (README:442) — the wrap is C31's; the isolation policy is C30/C34's.
C31 builds in parallel with its Evaluation-&-Judge siblings (C30/C32/C33/C34; inventory line 111).

## 3. Interfaces / contracts

Sweep-1: interfaces **named and described**; concrete CLI flags / trajectory schema / adapter field-mapping
defer to sweep 2 (and the scenario format to C30, the trajectory/score model to Inspect AI + C32).

| # | Interface | Direction | Description | Owning/detailing component |
|---|---|---|---|---|
| I1 | **`[[service]] type="inspect_ai"` provider block** | declarative (config) | The Gas City service block that registers Inspect AI as the scenario provider (A28j; README:424). The pack-level declaration that makes the runner available to the engine. | C31 (this); C02/C03 (service-block model) |
| I2 | **`inspect eval` subprocess tool node** | inbound (invoke) | The `[[tool]] type="subprocess"` node — `command="inspect"`, `args=["eval","{scenario_path}","--task","{task}"]`, `work_partition="scenarios"` (A28i; AI-CONTEXT §13.3). The engine invokes this node to *run a scenario*; placement is by C17 (by-name); bytes/exit-status are C02's. | C31 (this); C17 (placement), C02 (ABI) |
| I3 | **Scenario-reference + task input** | inbound (data) | The `{scenario_path}` (a C30 store reference) + `{task}` the node consumes, substituted into `args` from molecule/bead context. C31 does not define the scenario format (C30) — it consumes a reference to it. | C30 (format/store), C31 (consumes) |
| I4 | **Session-id adapter (G25)** | internal/glue | The custom glue that maps Claude Code/Gas City **`session.id`** ↔ Inspect AI's run/sample identity, **injecting** it into the eval so the run's emitted turns thread into one trajectory, and **surfacing** the run's `session.id` as part of the node's output. **This is C31's core custom deliverable.** | C31 (this) |
| I5 | **Run trajectory + result output** | outbound (data) | The node's declared output: Inspect AI's emitted **trajectory/sample log** + run identity (`session.id`) + exit status, surfaced to the workflow engine (C17) and bound to a bead so C32 (judge) can score it ("scenario-to-bead binding via pack", README:439). *[FAITHFUL-FILL]: README:439 states the **binding-via-pack** concept; the exact **bead-binding shape** (which fields land on the bead so C32 locates the right trajectory) is inferred from the bead model (C19/C20) + the judge-consumes-trajectory flow and is deferred to sweep 2 (OQ-4), not a v4-stated contract.* | C31 (this); C32 (consumer), C17 (surfacing) |
| I6 | **Pack/tool-node lifecycle** | inbound (ops) | C31 packaged + configured as a Gas City pack (Inspect AI install + the I1/I2 blocks); operated in Phase 2 alongside C30/C32 (README:423–424). | C02/C17 (ABI), C31 (config) |

**Invariants C31 must uphold:**
- **INV-1 (runner is Inspect AI, not custom):** scenario execution is performed by `inspect eval`; C31 adds
  **no** runner/scheduler/eval-loop of its own. The only custom code is the **wrap (I1/I2)** and the
  **session-id adapter (I4)**. (Bar discipline — README:172/439; see §6.)
- **INV-2 (trajectory threads by `session.id`):** every scenario run is associated with exactly one
  `session.id`, and all turns the run provokes carry that id so they chain into one trajectory (so C24's
  parent-chain lands them coherently and C32 scores the right trajectory). This is the property the adapter
  (I4) exists to guarantee (AI-CONTEXT §4.3 line 178, §5.4; G25). *C31's guarantee is the **coherent
  `session.id`**; the **parent-chain landing itself** is C24's mechanism over the raw-bodies→CXDB seam, whose
  `session.id`→CXDB-parent-pointer mapping rule is the **G26** seam C24 owns — C31 supplies the correct id, it
  does not perform the parent-chaining.*
  > [AMBIGUITY: G25] v4 states only that Inspect AI's session-id model **vs** Gas City's "likely needs adapter
  > layer; impedance unknown" (AI-CONTEXT §12 line 512) and does not give the mapping. Two readings of the
  > adapter's depth: **(a) thin** — a 1:1 id translation (carry/rename the existing `session.id` into the
  > Inspect-AI run's metadata and back out) when the two identity models are reconcilable; **(b) thick** — a
  > stateful correlation layer that *generates/assigns* a run id and maintains a map (Inspect AI sample/eval id
  > ⇄ Claude Code `session.id`) when Inspect AI owns its own session identity that cannot be overridden.
  > **Chosen: (a) as the faithful baseline — thinnest adapter that threads the existing `session.id`** — with
  > (b) named as the fallback. Rationale: v4 calls this a single "**adapter layer**" (singular, lightweight),
  > consistently treats `session.id` as *the* correlation key the whole telemetry/CXDB chain already uses
  > (AI-CONTEXT §4.3/§5.4), and the "impedance unknown" caveat is explicitly a *spike*, not a directive to
  > build a heavy broker. The actual depth is **OQ-1**: it is empirically determined by whether Inspect AI
  > lets the caller set/propagate the session identity (thin) or mints its own (thick map). C31 owns whichever
  > the spike resolves to; both are "the adapter layer" v4 scopes.
- **INV-3 (runs in the scenario rig, does not police it):** the `inspect eval` node executes with
  `work_partition = "scenarios"` (AI-CONTEXT §13.3 line 607). C31 **inherits** the read-isolation that C34
  enforces / C42 provides (D-13); it does **not** itself check holdout integrity. C31's only obligation is to
  *run in the right partition*, not to enforce it.
- **INV-4 (no scoring / no verdict):** C31 emits the trajectory + status; it computes **no** satisfaction
  score and renders **no** pass/fail verdict — that is C32/C33 (README:185/188). The runner is verdict-blind.
- **INV-5 (wrap is a pack, not an import):** C31 is delivered as a Gas City pack invoking the `inspect` CLI
  via the C02 subprocess ABI; it does **not** import Inspect AI's Python (or the engine's Go) in-process
  (README:177; C17 §1). The Python lives behind the subprocess boundary (F-MODE F45 bounding, §7).

## 4. Data model / state

C31 is **largely stateless** — it shells out to `inspect eval` per run and surfaces the result. The only
state directly forced by a v4 requirement is the **adapter's `session.id` association** (and, under the thick
reading, its id map). State C31 is the spec-of-record for at sweep 1:

| State | Description | Persistence | Detailed by |
|---|---|---|---|
| **Pack / service + tool config** | The `[[service]] type="inspect_ai"` block + the `[[tool]]` subprocess node (command/args/`work_partition="scenarios"`), plus Inspect AI install/version pin. | Pack TOML (C02/C03 model). | C02/C03 (model), C31 (binding) |
| **Per-run `session.id` association** *(adapter, I4/INV-2)* | The `session.id` threaded into a given scenario run, and (thick reading only) the Inspect-AI-run-id ⇄ `session.id` map. **The one piece of state forced by G25.** | Thin reading: transient per-invocation (carried in the run's env/metadata, not a store). Thick reading: a small per-run correlation map — **OQ-1**. | C31 (adapter) |
| **Run trajectory + result** | Inspect AI's emitted trajectory/sample log + exit status, surfaced as the node's output. **Stored/owned by Inspect AI's log dir + the bead it binds to (C19/C20)**; the trajectory's durable home is **CXDB via C24**. | Inspect AI log output (transient) → bead (C19/C20) → CXDB (C24). | **Inspect AI** (log), **C24** (CXDB), C32 (consumer) |
| **Scenario reference + task** | The `{scenario_path}` (C30 store reference) + `{task}` the run consumes. | Owned by **C30** (the scenario store); C31 holds only the reference for the duration of a run. | **C30** |

> [FAITHFUL-FILL] v4 specifies the runner's *behavior* (invoke `inspect eval` on a scenario) and *names* the
> needed adapter, but not C31's persisted state. The minimal faithful set is **the adapter's per-run
> `session.id` association** — the *only* state a v4-named requirement forces ("needs session-id adapter",
> inventory C31; "Inspect AI's session-id model vs Gas City's … adapter layer", §12 G25). Everything else is
> owned upstream/downstream: the scenario is **C30**'s, the trajectory's durable store is **CXDB/C24**'s, the
> score is **C32**'s, the config is the **pack TOML**'s. Whether the adapter state is transient (thin) or a
> small map (thick) is OQ-1; either way C31 introduces **no** general-purpose store — consistent with "write a
> *small* pack that exposes it as a tool node" (README:177).

**Consistency / lifecycle.** C31 stands up in **Phase 2** with the Inspect AI install + the scenario store
(README:423–424). Each run is **ephemeral**: invoke → emit trajectory → surface output; the durable artifacts
are the **trajectory in CXDB** (C24) and the **bead** (C19/C20). C31 holds no long-lived source of truth; a
restart loses at most an in-flight `inspect eval` (which the workflow engine / Orders re-drive — C40), and the
already-emitted trajectory survives in its log dir + CXDB.

## 5. Behavior

**Stand up (Phase 2).** Install Inspect AI (README:423). The pack declares the `[[service]] type="inspect_ai"`
provider (I1) and the `[[tool]] type="subprocess"` `inspect eval` node (I2) with `work_partition="scenarios"`
(AI-CONTEXT §13.3). The session-id adapter (I4) is wired into the invocation.

**Execute a scenario (steady state).**
1. **Receive** (I3): the engine reaches the scenario-run node in a formula/molecule with a `{scenario_path}`
   (C30 reference) + `{task}` from bead context.
2. **Thread session-id** (I4): the adapter establishes the run's `session.id` — carrying the existing Claude
   Code/Gas City `session.id` into the Inspect AI run's metadata/env (thin), or assigning + mapping a run id
   (thick) — so emitted turns will chain into one trajectory (INV-2; G25).
3. **Invoke** (I2): run `inspect eval {scenario_path} --task {task}` as a C02 subprocess in the `scenarios`
   partition (INV-3). Inspect AI *is* the runner — it drives the system through the scenario and produces a
   trajectory/sample log (INV-1).
4. **Surface** (I5): on completion, surface Inspect AI's trajectory/log + the run's `session.id` + exit status
   as the node's declared output, bound to a bead (README:439). C32 (judge) consumes the trajectory; C24
   delivers the emitted turns to CXDB under the threaded `session.id`.
5. **On failure**: a nonzero `inspect eval` exit surfaces as the node's status (C02 exit-code); the workflow
   engine / Orders (C18/C40) own retry/escalation — C31 adds no custom retry loop (INV-1).

> The exact `inspect eval` CLI surface (flags beyond `--task`), the trajectory/sample-log schema, the precise
> `session.id` ⇄ Inspect-AI-id field mapping and injection mechanism (env var? `--metadata`? sample tag?),
> and the bead-binding shape are **sweep-2+**. The scenario format is **C30**; the score model is **C32**; the
> trajectory store is **CXDB/C24**.

## 6. Failure modes & handling

C31 owns the one gap assigned at this seam (G25).

**G25 (minor) — Inspect AI session-id model vs Gas City's; adapter layer; impedance unknown. ADDRESSED HERE
(C31's core custom deliverable).** v4 flags the need for an adapter but leaves the mapping + depth open
(AI-CONTEXT §12 line 512). Faithful resolution: **C31 owns a session-id adapter (I4) that threads the
existing Claude Code/Gas City `session.id` into each scenario run** so the run's turns chain into one
trajectory (INV-2), surfacing that id for C24 (CXDB parent-chain) and C32 (judge). The **thin** 1:1 id
translation is the faithful baseline; a **thick** stateful id-map is the fallback if Inspect AI mints its own
unalterable session identity (the [AMBIGUITY: G25] reading; depth = OQ-1, a sweep-1/2 spike). This is exactly
the "low-effort custom code where a principle could not be met without it" the bar **KEEPS**: P5's trajectory
attribution (and therefore P6 scoring, P10/P11's trajectory memory) **cannot** be met if scenario-run turns
do not thread under a coherent id, and the OSS stack does not provide that reconciliation off-the-shelf
("impedance unknown").

**Over-build the bar makes C31 DROP (flagged per the brief):**
- **A custom runner / scheduler / eval-loop** — DROPPED. Inspect AI's `inspect eval` is the runner
  (README:172/439; INV-1). Building one is the canonical over-build; C31 wraps, it does not re-implement.
- **A custom parallel-run / fan-out engine, retry policy, or rate-limiter** — DROPPED. Parallelism + retry
  are Inspect AI's (eval-set) and the workflow engine's (C18/C40 own re-drive); C31 adds neither.
- **Holdout-enforcement / leakage-audit logic** — DROPPED here (it is **C34**'s, D-13). C31 only runs in the
  `scenarios` partition (INV-3); it does not police reads.
- **Scoring / satisfaction / verdict** — DROPPED here (**C32/C33**, INV-4). The runner is verdict-blind.
- **A scenario format/store** — DROPPED here (**C30**). C31 consumes a reference.
- **CXDB trajectory delivery** — DROPPED here (**C24**). C31 tags the run; C24 delivers turns.

**Other failure cases.**
- **`inspect eval` nonzero exit / Inspect AI internal error** → surfaces as the C02 tool-node status; C18/C40
  own retry/escalation. *[FAITHFUL-FILL]: v4 gives no C31-level retry contract; minimal-consistent placement
  is "surface status, engine decides" — same posture as C17 §6.]*
- **Adapter cannot thread `session.id`** (Inspect AI rejects/overrides the injected id) → the trajectory may
  not chain coherently; this is the **G25 impedance risk** the spike (OQ-1) retires before C32/C24 rely on it.
  Mitigation: detect at the bridge (C24 sees an unparented/mis-parented turn) — but the *fix* is the adapter
  depth (thin→thick). Until the spike resolves, this is the component's top risk (OQ-1).
- **Scenario runs against production instead of a twin** → out of C31's scope; the run target is configured by
  the scenario/task (C30) and the twin is C44; C31 executes what it is given (F-MODE F12/F54 context).
- **Python-harness fault** (F45) → bounded by the subprocess boundary (INV-5): a fault in Inspect AI's Python
  is a nonzero exit at the C02 ABI, not an in-process crash of the (Go) engine.

> F-mode applicability is owned by C57 (coverage map). C31 underwrites the **execution** side of the P5
> F-modes: **F39** (point-spec / region-mismatch — Inspect AI region scoring over multiple acceptable
> trajectories, F-MODE:90) and **F9** (spec overfitting — signed scenarios run as held-out, F-MODE:19) operate
> on the *runs C31 produces*; **F28** (holdout leakage, F-MODE:22) is **C30/C34**'s, with C31 contributing only
> the `scenarios`-partition execution. C31 inherits the **F45** (language-as-harness, Python) residual
> (F-MODE:92), whose blast radius is **bounded** to the subprocess (INV-5) — note F45 is **"Partial — Python
> sections inherit risk"** in F-MODE-COVERAGE, i.e. the subprocess boundary *bounds* the residual, it does
> not *close* it. C31 defers the canonical F-mode mapping to C57.

## 7. Cross-cutting (security / cost / scale / observability / ops)

- **Security.** C31 executes scenarios in the **`scenarios` work-partition** (AI-CONTEXT §13.3) under the
  read-isolation **C34 enforces / C42 provides** (D-13) — C31 *honors* the partition, it does not own the
  policy. The Inspect AI Python runs **behind the C02 subprocess boundary** (INV-5), bounding the Python
  blast radius (F45). The adapter carries `session.id` (a correlation attribute, not a secret) into the run.
  Scenarios that target external deps should use **twins** (C44), not production, to bound exposure (F-MODE
  F12/F54) — selected by the scenario, not C31.
- **Cost.** A run is an `inspect eval` subprocess; the **token cost is the scenario's** (it drives the system
  through real model calls), not C31's wrapper. C31's own overhead is process-startup + the adapter (cheap).
  v4 gives no separate runner cost model.
- **Scale.** Throughput = how fast scenarios can be run; **parallelism/fan-out is Inspect AI's** (eval-set) +
  the workflow engine's (formula/molecule concurrency), **not** a C31-owned scheduler (INV-1). The P7 twins
  exist precisely so scenarios can "run thousands per hour without rate limits" (README:195) — a property of
  the *target*, not the runner wrapper.
- **Observability.** The run's **trajectory** is the primary artifact — it lands in CXDB via C24 (parent-chain
  by the adapter's `session.id`) and is what C32 scores. C31's own health (eval exit status, run latency,
  adapter id-threading success rate) is the operational signal that tells ops whether scenarios are
  executing + threading correctly. Emitting these on the event bus (C23) keeps runs auditable.
- **Ops.** Pack-delivered tool node operated alongside C30/C32 in Phase 2 (README:423–424). **Pin the Inspect
  AI version** so the `inspect eval` CLI surface + trajectory schema the adapter and C32 depend on are
  reproducible (parallels C24's CXDB-version-pin posture). v4 flags "the **Inspect AI wrap** … harder part"
  (README:442) — that wrap + the adapter spike *are* C31's work.

## 8. Acceptance criteria & test strategy

Sweep-1 = high-level criteria (concrete tests at sweep 2).

1. **AC-1 (runner wrap — I1/I2/INV-1):** the pack registers Inspect AI via `[[service]] type="inspect_ai"`
   and a `[[tool]] type="subprocess"` node runs `inspect eval {scenario_path} --task {task}`; a scenario
   executes end-to-end **without any custom runner code** (Inspect AI is the runner; README:172/439).
2. **AC-2 (executes a scenario against the system — I3):** given a C30 scenario reference + task, C31 runs it
   and produces an Inspect AI trajectory/sample log + exit status as the node's output.
3. **AC-3 (session-id threads — I4/INV-2, addresses G25):** a scenario run is associated with exactly one
   `session.id`, and the turns the run provokes chain into **one** trajectory under that id — verifiable by
   C24 landing them as a single parent-chained trajectory in CXDB (AI-CONTEXT §4.3/§5.4) and by C32 scoring
   that trajectory.
4. **AC-4 (adapter depth resolved — OQ-1/G25):** the spike confirms whether Inspect AI accepts an injected
   `session.id` (thin) or requires a maintained id-map (thick); the implemented adapter matches reality and
   AC-3 passes under it.
5. **AC-5 (runs in the scenario rig, does not enforce — INV-3):** the `inspect eval` node executes with
   `work_partition="scenarios"`; C31 contains **no** holdout-enforcement/audit logic (that is C34; D-13).
6. **AC-6 (verdict-blind — INV-4):** C31 emits a trajectory + status only; it computes **no** satisfaction
   score and renders **no** pass/fail verdict (C32/C33 do).
7. **AC-7 (pack, not import — INV-5):** C31 is a Gas City pack invoking the `inspect` CLI over the C02
   subprocess ABI; no in-process import of Inspect AI Python (or engine Go). A Python fault surfaces as a
   nonzero exit, not an engine crash (F45 bounding).
8. **AC-8 (trajectory → judge handoff — I5):** the emitted trajectory + run identity are bound to a bead such
   that C32 can locate and score the **right** trajectory ("scenario-to-bead binding via pack", README:439).
9. **AC-9 (no over-build):** review confirms C31 contains no custom runner/scheduler/eval-loop, no parallel-run
   engine, no retry policy, no scoring, no scenario store, no CXDB delivery — only the **wrap** + the
   **session-id adapter** (the bar; INV-1).

**Test strategy.** A **scenario-runner integration pack** that: installs the pinned Inspect AI, points the
`inspect eval` node at a synthetic C30 scenario in the `scenarios` partition, and drives AC-1…AC-9 — in
particular the **session-id threading (AC-3/AC-4)**: run a multi-turn scenario and assert its turns land in
CXDB (C24) as **one** parent-chained trajectory under the run's `session.id`, and that C32 scores that
trajectory. The **adapter spike** (thin vs thick, OQ-1) is the first de-risker and gates AC-3. This suite must
pass before **C32 (judge)** and **C33 (satisfaction)** rely on C31's trajectories — it is the *execution* half
of the P5 mechanism the **bootstrap-validation milestone** (README:429) exercises.

## 9. Open questions

- **OQ-1 (→ review-log, top): session-id adapter depth (G25).** Does Inspect AI let the caller set/propagate
  the run's session identity (→ **thin** 1:1 translation of the existing `session.id`), or does it mint its
  own unalterable session/sample id (→ **thick** maintained `session.id` ⇄ Inspect-AI-id map)? This is the
  "impedance unknown" v4 flags (AI-CONTEXT §12 line 512); resolve by a **direct Inspect AI spike** before
  sweep 2, since C24's parent-chain (AI-CONTEXT §5.4) and C32's scoring both depend on the threaded id. (The
  single load-bearing uncertainty for C31.)
- **OQ-2 (→ review-log): exact `session.id` injection mechanism.** Given OQ-1's answer, *how* is the id
  carried into `inspect eval` — env var, `--metadata`/`-T` task arg, sample tag, or Inspect AI hook? Freeze at
  sweep 2 against the real CLI; it is the concrete field-mapping behind I4.
- **OQ-3 (→ review-log): one scenario → one `session.id` granularity.** Does a single `inspect eval` (which
  may run many samples/epochs) map to **one** `session.id` for the whole eval, or **one per sample**? This
  sets the trajectory granularity C24/C32 see (a scenario "run" vs a per-sample trajectory). Confirm with
  C32/C24 at sweep 2 (interacts with Inspect AI's sample model, B49).
- **OQ-4 (→ review-log): `inspect eval` CLI surface + trajectory-log schema.** The exact flags (beyond
  `--task`), the trajectory/sample-log format C32 must parse, and how it is surfaced/bound to a bead
  (README:439). Pin to the chosen Inspect AI version; freeze with C32 at sweep 2.
- **OQ-5 (→ review-log): run target / twin selection.** Confirm the scenario/task (C30) — not C31 — selects
  whether a run hits a **twin** (C44) vs the real system (F-MODE F12/F54; README:195), so C31 stays target-
  agnostic. (Boundary check, not a C31 mechanism.)
