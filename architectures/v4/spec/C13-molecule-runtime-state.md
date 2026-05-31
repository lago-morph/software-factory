# C13 — Molecule (instantiated workflow / runtime state)  (Spec, Track A)

> Source: AI-CONTEXT §3.2 "nine concepts" #7 (line 91 "Formulas + Molecules — Formula = TOML DAG template; **Molecule = instantiated bead-tree** — P1, P3, P4, P12"); AI-CONTEXT §3.3 vocabulary table (line 102 "molecule | instantiated workflow / bead-tree"; line 108 "wisp | unit of dispatchable work"; line 92/concept-8 "Dispatch (Sling) — Routes bead/wisp to agent or pool"; line 93/concept-9 "Health Patrol (Controller + Convergence) — Per-tick reconciler; bounded convergence with gates"); one-shot-specs §"Gas Town / Gas City" (line 81 "work primitives are *formulas* and *protomolecules/molecules* — reusable workflow templates (design → plan → implement → review → test chains)"); README §"Vocabulary lock-in" (line 516 "Cities, rigs, formulas, molecules. Real cognitive load."); README Part 4 P10 (line 235 "Tasks with dependencies", "Survives across agent sessions"), P11 (line 259 "bead chain: anomaly → diagnosis → fix → resolution"); AI-CONTEXT §16 cold-start (lines 694–699 `gc bd find --type factory_build_in_progress` → `gc converge resume <bead_id>`); component-inventory C13 row (Maps from A22b/B32; **Depends on C12, C18**; gaps: none; foundational: no). Related specs: `spec/C12-formula-pipeline-file.md` (the template C13 instantiates), `spec/C19-bead-work-graph.md` (the store the bead-tree lives in), `spec/C20-bead-schema.md` (the bead types/envelope the tree's nodes use). C18 (reconciler) has no spec yet at sweep-1; referenced by inventory dependency + AI-CONTEXT concept #9.
> Inventory ID: C13   Kind: artifact   Status: sweep-1
> Track: A (faithful)

## 1. Purpose & responsibility

C13 is the **molecule**: a **formula (C12) instantiated into a live bead-tree for a specific run** — the
**runtime state of an in-flight workflow** (inventory C13 one-liner; AI-CONTEXT §3.2 concept 7 "Molecule =
instantiated bead-tree"; §3.3 vocab "molecule | instantiated workflow / bead-tree"). Where the formula is the
*static, version-controlled template* (the methodology — "design → plan → implement → review → test chains",
one-shot-specs:81), the molecule is *that template brought to life for one execution*: each formula node
becomes one or more **beads** (C19/C20) in a connected **tree/graph**, parameters are bound to concrete run
inputs, and the per-node execution state (which steps have run, their status, retries, the human-gate
verdicts) lives on those beads.

The molecule is the **template↔run boundary**. v4's central inversion is "methodology is the variable,
substrate convergent" (README Part 1): the *formula* carries methodology, but a methodology only does work
when *run*, and a run needs somewhere to hold "where are we in the chain right now, for this epic?" That
somewhere is the molecule. It is the join between three already-specced primitives:

- **C12 formula** — the DAG template being instantiated;
- **C19/C20 beads** — the durable, typed, attributed work-graph the live tree is *made of*;
- **C18 reconciler / Health Patrol** — the per-tick controller that *advances* the molecule toward done
  (AI-CONTEXT §3.2 concept 9 "Per-tick reconciler; bounded convergence with gates").

**Responsibilities**
- Be the **instantiation of a formula**: given a named formula (C12) and a set of run parameters, materialize
  a **bead-tree** — one bead per formula node (or per node-occurrence under a bounded loop), wired with the
  formula's edge/dependency topology, with parameters bound to concrete values (AI-CONTEXT §3.2 concept 7;
  C12 §3.3 "a named, parameterized template that can be instantiated into a bead-tree").
- Hold the **runtime state of the in-flight workflow**: per-node execution status, the current frontier
  (which nodes are runnable now), loop-iteration counters for bounded loops, and human-gate verdicts —
  expressed as **bead state** on the tree's beads (C19 §"bead state/lifecycle"; C20 envelope `status`).
- Provide the **run identity / resume handle**: a molecule is the unit a run is identified by and resumed
  from — the bead-tree (rooted at a run/build bead) that `gc converge resume <bead_id>` picks back up
  (AI-CONTEXT §16; README:259 "Survives across agent sessions"). The molecule *is* the cross-session memory
  of an in-progress run.
- Present the **dispatchable-work surface** to Sling (C05): a runnable molecule node yields a **wisp** ("unit
  of dispatchable work", AI-CONTEXT §3.3) that Sling routes to an agent/pool (AI-CONTEXT §3.2 concept 8
  "Routes bead/wisp to agent or pool"). The molecule says *what work is ready*; Sling says *who runs it*.
- Preserve the **formula→molecule→bead provenance**: every bead in the tree traces back to the formula node
  it came from and carries `created_by` (C41 via C20), so a run can be replayed and judged against the formula
  it was instantiated from (C12 §7 "the formula→molecule→bead-tree mapping is what lets a run be replayed and
  judged").

**Explicitly NOT**
- NOT the **formula** (C12). The formula is the static, version-controlled TOML DAG template; the molecule is
  one *live instance* of it with per-run state. A formula is reused across many molecules; a molecule belongs
  to exactly one run (AI-CONTEXT §3.2 concept 7 — the pair is explicitly two concepts: "Formula = template;
  Molecule = instantiated"). C13 owns no template/methodology of its own.
- NOT the **bead store** (C19) or **bead schema** (C20). The molecule is *made of* beads but does not persist
  them or define their types — C19 is the durable graph engine, C20 the type catalog. C13 is the *structure
  and lifecycle* a subset of those beads form for one run; it adds no new persistence layer (the bead-tree
  lives in C19). > [FAITHFUL-FILL] — see §4.
- NOT the **reconciler / Health Patrol** (C18). C18 is the per-tick control loop that *drives* a molecule to
  convergence; C13 is the *state that loop reads and advances*. The molecule is the desired-vs-actual subject;
  the convergence algorithm, tick cadence, and gate evaluation are C18's (AI-CONTEXT §3.2 concept 9). C13
  owns the run state; C18 owns the loop over it.
- NOT **dispatch / Sling** (C05). The molecule *exposes* ready work as wisps; Sling *routes* them to workers
  (AI-CONTEXT §3.2 concept 8). C13 decides *which nodes are ready*, not *which agent executes them*.
- NOT a **convoy** (batched workflow) or an **order** (event-triggered workflow). Those are distinct Gas City
  terms (AI-CONTEXT §3.3) layered over formulas/molecules but owned elsewhere (order → C40); a molecule is a
  single in-flight run of a single formula (consistent with C12 §3.3 [AMBIGUITY: G06] Reading A).
- NOT the **agent loop** (C28) that *executes* a dispatched node's work. The molecule tracks that a node is
  in-flight/done; the multi-turn reasoning inside a model node is C28's, recorded as CXDB trajectory (C21),
  not as molecule state.

## 2. Context & dependencies

| Direction | Component | Relationship |
|---|---|---|
| Upstream (instantiates) | **C12** Formula / pipeline-file | The molecule is "this formula instantiated into a live bead-tree" (inventory C13 depends on C12; C12 §1 "C13 owns the running instance"). C12 guarantees C13 a named, parameterized, acyclic template whose every node resolves to a binding and whose parameters are declared (C12 §3.3 outbound contract). |
| Upstream (driven by) | **C18** Reconciler / Health Patrol | The per-tick convergence loop that advances the molecule (AI-CONTEXT §3.2 concept 9; inventory: C13 **depends on C18**). C18 reads the molecule's desired (formula) vs actual (bead state) and steps it forward under bounded gates. |
| Upstream (made of) | **C19** Bead store / work-graph | The bead-tree is stored as C19 beads + dependency edges, durable across sessions (AI-CONTEXT §3.2 #2; README:235). C13 holds no persistence of its own. *(Brief lists C19/C20 as C13's dependencies; inventory lists C12/C18. Both are real — see OQ-C13-1.)* |
| Upstream (typed by) | **C20** Bead schema registry | The tree's beads carry the C20 common envelope (`id`, `type`, `created_by`, `dependencies`, `status`) and use C20-defined types; run/build beads (`factory_build_in_progress`) carry the resume contract C20 defines (C20 §4; AI-CONTEXT §16). |
| Downstream (dispatches via) | **C05** Sling / dispatch | A runnable molecule node becomes a **wisp** Sling routes to an agent/pool (AI-CONTEXT §3.2 concept 8, §3.3 "wisp"). |
| Downstream (executes) | **C28** Agent loop, **C17** Tool node | A dispatched model node runs in C28; a deterministic node runs as a C17 tool node. The molecule records the outcome on the node's bead. |
| Downstream (attribution) | **C41** Identity/attribution | Every bead in the tree carries `created_by` (C41 via C20 envelope); the molecule preserves attribution per-node. |
| Downstream (evaluated/replayed) | **C33** Satisfaction, **C49** Counterfactual replay, **C55** Methodology-experiment | The molecule (the run's bead-tree + its CXDB trajectories) is what gets judged (C33), replayed from a midpoint (C49), and compared across swapped formulas (C55). C13 is the per-run subject those loops measure. |

C13 is **not foundational** (inventory: no) and lands in **Batch 2** (core build flow, alongside C12/C05/C28),
after its dependencies C12 (formula) and C19/C20 (beads) are shape-fixed and once C18 (reconciler) exists to
drive it. It introduces **no new gaps** of its own (inventory "Key gaps" column is empty for C13); its
correctness is almost entirely *derived* from the contracts of C12, C18, and C19/C20.

## 3. Interfaces / contracts

Sweep 1 — interfaces **named and described**; concrete signatures/schemas deferred to sweep 2 (and gated on
the real `gc` molecule/converge surface — G11, see §9).

### 3.1 The molecule (named structure)

A molecule is the live structure produced by instantiating a formula. Its named elements (sweep-1
descriptions; exact `gc` shapes confirmed at sweep 2 against the real Gas City molecule/`gc converge` model —
§9 / G11):

| Element | Description | Source / fill |
|---|---|---|
| Molecule / run identity | The handle a run is identified and resumed by — the root of the bead-tree; the `<bead_id>` of `gc converge resume`. | AI-CONTEXT §16 line 699; README:259 |
| Source formula reference | Which formula (by name, C12) this molecule instantiates — the methodology this run is executing. | AI-CONTEXT §3.2 concept 7; C12 §3.1 "referenced by name at instantiation" |
| Bound parameters | The concrete run inputs the formula's declared parameters were bound to at instantiation (e.g. `$epic_id` → a real epic id). | C12 §3.1 [FAITHFUL-FILL] parameters; one-shot-specs:62–63 |
| Bead-tree (node instances) | One bead per formula node (or per loop-iteration occurrence), wired by the formula's edge/dependency topology; each bead typed + attributed (C19/C20). | AI-CONTEXT §3.2 concept 7 "instantiated bead-tree"; README:235 "Tasks with dependencies" |
| Per-node execution state | The `status` (and any retry/iteration counter) on each node-bead: pending / runnable / in-flight / done / blocked-on-gate / failed. | C20 envelope `status`; C19 §"bead state/lifecycle" [FAITHFUL-FILL] enum |
| Run frontier (ready set) | The set of node-beads whose dependencies are satisfied and which are runnable *now* — the molecule's dispatchable surface to Sling (as wisps). | derived from the DAG + state; AI-CONTEXT §3.2 concept 8 [FAITHFUL-FILL] |
| Loop-iteration state | For a formula's bounded loop construct (C12 §3.1 [FAITHFUL-FILL] loop), the current iteration count and bound, so the molecule knows when a loop re-enters vs terminates. | C12 §3.1 loop FAITHFUL-FILL; F26 "chain length … lintable" |
| Gate/wait verdicts | The recorded outcome of a human-approval / synchronization gate node (approved / rejected / pending), held on the gate node's bead. | C12 §3.1 gate nodes; AI-CONTEXT §3.3 "wait" |

> [FAITHFUL-FILL] **The molecule's state lives on beads, not in a separate molecule store.** v4 says
> "Molecule = instantiated **bead-tree**" (AI-CONTEXT §3.2 concept 7) and the bead store is the durable,
> cross-session work-graph (README:235). The minimal faithful reading is therefore that a molecule has **no
> persistence layer of its own** — its entire runtime state is the bead-tree's beads + edges + `status` in
> C19. "The molecule" is a *view/rooted-subgraph* over C19, not a new store. This is the smallest choice
> consistent with both "instantiated bead-tree" and "memory layer survives across sessions" (a separate
> molecule store would duplicate C19 and break resume). Whether Gas City represents the molecule as a
> first-class object or purely as a bead subtree is a `gc` internal (G11) deferred to sweep 2.

> [FAITHFUL-FILL] **`status` enum + frontier are derived, not invented state.** v4 names neither a status
> enum nor a "frontier" explicitly, but a *per-tick reconciler with bounded convergence and gates*
> (AI-CONTEXT §3.2 concept 9) is undefinable unless each node has a runnable/done/blocked state and the loop
> can compute what is ready. The minimal faithful fill is: node `status` is the C20 envelope field (already
> faithfully present), and the "frontier" is the *derived* set of beads whose dependency edges are all `done`
> — no new stored field, just the standard topological-readiness computation over the DAG the formula already
> defines. The exact enum values are a sweep-2 + `gc`-confirmed detail.

### 3.2 Inbound: how a molecule is created / advanced

- **Instantiate** — at dispatch, a named formula + bound parameters → a new molecule (bead-tree rooted at a
  run/build bead). This is the operation that turns C12's template into C13's running instance. The build-bead
  case carries the C20 resume contract (`factory_build_in_progress`, `transfused_from`, spec/scenario
  pointers; AI-CONTEXT §16). > [FAITHFUL-FILL] the instantiation *call* is Gas City's (`gc`); C13 specifies
  the *resulting structure*, not the CLI verb.
- **Advance (per tick)** — C18 reads the molecule, computes the frontier, and advances node states; the
  molecule is the read/write subject of each convergence tick (AI-CONTEXT §3.2 concept 9). C13 exposes the
  state; C18 owns the stepping algorithm and gate evaluation.
- **Resume** — `gc converge resume <bead_id>` (AI-CONTEXT §16 line 699) re-attaches to an in-flight molecule
  by its root bead id and continues convergence from the persisted bead state — no out-of-band run state
  (C20 §"resume-completeness").

### 3.3 Outbound: what the molecule guarantees to consumers

- To **C18** (reconciler): a well-formed desired-vs-actual subject — a bead-tree whose desired topology is the
  formula's DAG and whose actual state is the per-node `status`, so a tick can compute the runnable frontier
  and detect "converged" (all terminal nodes `done`/gates passed) deterministically.
- To **C05** (Sling): a **wisp** per runnable node — a unit of dispatchable work (AI-CONTEXT §3.3) carrying
  enough to route (the node's binding: a C17 tool node or a C09 prompt template, named by the formula) without
  Sling needing to read the whole molecule.
- To **C19/C20** (store): only well-typed, attributed beads with valid dependency edges — every node-bead has
  a registered `type`, a `created_by`, and edges consistent with the formula's DAG (so the tree is a legal
  C19 subgraph). The molecule introduces **no bead type or edge kind of its own**; it composes C20-defined
  types. > [FAITHFUL-FILL] (faithful to the "no new type system" stance of C20 §1).
- To **C33/C49/C55** (evaluation/replay/experiment): a per-run, replayable subject — the molecule's root bead
  + its tree + the per-node CXDB trajectory pointers are the unit that gets judged, branched (C49 O(1)
  midpoint replay), and compared across swapped formulas (C55).

> [FAITHFUL-FILL] **Wisp ⇄ molecule-node relationship.** v4 lists *wisp* = "unit of dispatchable work" and
> Sling routes "bead/wisp" (AI-CONTEXT §3.2 concept 8, §3.3) but never states whether a wisp *is* a runnable
> node-bead or a lighter dispatch envelope over it. The minimal faithful reading: a wisp is the **dispatch
> view of a runnable molecule node** — i.e. a frontier node-bead presented to Sling for routing. This keeps
> "Sling routes bead/wisp" literally true (a wisp is bead-derived) without inventing a separate work object.
> The exact wisp shape is Gas City's (G11), deferred to sweep 2; C13 only requires that *the molecule's
> frontier is the source of wisps*.

## 4. Data model / state

C13 is classed an **artifact** in the inventory, but it is the *runtime-state* artifact — the **only**
component whose subject is per-run, in-flight state. Crucially, that state is **not a new store**: it is held
in C19 beads (see §3.1 FAITHFUL-FILL). C13 owns the *shape and lifecycle* of that per-run subgraph, not its
bytes.

**What the molecule comprises (all expressed in C19/C20 terms):**

| Aspect | Where it lives | Owner |
|---|---|---|
| Bead-tree nodes (one per formula node / loop-occurrence) | C19 beads, typed by C20 | C19 stores; C20 types; C13 *structures* per formula |
| Dependency / ordering edges | C19 dependency edges, mirroring the formula DAG | C19 stores; C13 *derives* topology from C12 |
| Per-node `status` (pending/runnable/in-flight/done/blocked/failed) | C20 envelope `status` on each node-bead | C20 defines field; C18 advances; C13 is the subject |
| Bound parameters | on the run/root bead (run inputs) | C13 binds at instantiation; C19 stores [FAITHFUL-FILL] |
| Loop iteration counters + bound | on the loop node-bead(s) | C12 declares bound; C13 tracks count [FAITHFUL-FILL] |
| Resume handle / run identity | the root bead `id` (`factory_build_in_progress` case carries C20's resume fields) | C20 resume contract; C13 roots the tree at it |
| `created_by` per node | C20 envelope; C41 semantics | C41/C20; C13 preserves per node |

**Lifecycle (of a molecule instance).**
`instantiated` (formula + params → bead-tree) → `converging` (C18 advances the frontier tick by tick; nodes
go pending → runnable → in-flight → done; gates block until verdict) → `paused/resumable` (process restart;
state persists in C19; `gc converge resume <bead_id>` re-attaches) → `converged` (all terminal nodes done /
gates passed — run complete) **or** `failed/escalated` (a node fails terminally / a bounded loop exhausts its
bound). The molecule *instance* is mutable per-run state; the *formula* it came from is immutable (a methodology
change is a new formula → a new molecule, not a mutation of a running one — C12 §5 "methodology change =
formula edit").

> [FAITHFUL-FILL] **Lifecycle states are the minimal set the cited operations require.** v4 names instantiation
> (concept 7), per-tick convergence (concept 9), and resume (§16) but no explicit molecule state machine. The
> four-state lifecycle above is exactly what those three operations imply (you cannot resume without a
> paused/persisted state; you cannot converge without a converging/converged distinction). No state is added
> beyond what a cited v4 operation needs; the concrete enum + transition guards are sweep-2, jointly with C18.

**Consistency requirements.**
- **Faithful instantiation**: the molecule's bead-tree topology is exactly the formula's DAG (every formula
  node has ≥1 node-bead; every formula edge has a corresponding bead dependency edge); no node-bead exists
  without a formula node it derives from (provenance is total).
- **State on beads, durable across sessions**: all run state is in C19, so a restart + `gc converge resume`
  reconstructs the molecule with no loss (README:235; AI-CONTEXT §16).
- **Acyclicity preserved**: because the formula is acyclic (C12 invariant) and iteration is a *bounded loop
  construct* (C12 §3.1 FAITHFUL-FILL), the live bead-tree is a DAG of node-occurrences with bounded loop
  re-entry — never an unbounded cycle of beads.

## 5. Behavior

C13 has **no control loop of its own** — the loop that advances it is C18 (Health Patrol / reconciler),
mirroring C19's "no control loop; the reconciler acts on beads" stance. The molecule's behavior is the *run
lifecycle* it participates in (sweep-1 narrative; sequence/state diagrams deferred to sweep 2):

1. **Instantiate.** A named formula (C12) is referenced at dispatch with run parameters; the molecule is
   created as a bead-tree (one bead per formula node, typed by C20, attributed via C41), parameters bound,
   rooted at a run/build bead (the `factory_build_in_progress` case carries the resume contract).
2. **Compute frontier.** The runnable set = node-beads whose dependency edges are all `done`. At instantiation
   this is the formula's source node(s).
3. **Dispatch.** Each frontier node becomes a **wisp**; Sling (C05) routes it to an agent (model node → C28)
   or executes it as a tool node (C17). The node-bead's `status` → `in-flight`.
4. **Advance (per tick).** C18 reads outcomes, sets node `status` → `done`/`failed`, evaluates gates (a `wait`
   node blocks until its human/sync verdict), recomputes the frontier, and dispatches the next layer. Bounded
   loop nodes re-enter under their condition until the bound is hit.
5. **Converge or escalate.** When all terminal nodes are `done` and all gates passed, the molecule is
   `converged` (run complete). If a node fails terminally or a loop exhausts its bound, it is
   `failed`/`escalated` (the escalation *policy* is the reconciler's / C39's, not C13's).
6. **Resume across sessions.** At any point the run state is fully in C19; a restart re-attaches via
   `gc converge resume <bead_id>` and continues from the persisted frontier — the "survives across agent
   sessions" property in action (README:235; AI-CONTEXT §16).

The defining behavioral property: **a molecule is the live, resumable, attributed projection of one formula
execution** — the place "where are we in this run?" is answerable, and the subject every downstream loop
(reconcile, judge, replay, experiment) reads.

## 6. Failure modes & handling

C13 owns **no F-mode of its own** (inventory "Key gaps" empty); the relevant modes are inherited from its
dependencies and handled by deferring to their owners.

| F-mode / gap | Relevance to C13 | Handling (faithful) |
|---|---|---|
| **F26** Telephone / sustained inter-agent chain | A long molecule chain is exactly a long agent→agent handoff at runtime. | The bound is a *formula* property ("chain length is a formula property, visible and lintable", F-MODE:72) checked pre-run by C15. The molecule merely *instantiates* the already-bounded formula; it cannot grow a chain the formula did not declare. C13 inherits F26 mitigation from C12. |
| **G18 / F52** Unbounded self-heal / "more controller patches" | If the formula has a bounded loop (self-heal re-entry), the molecule must stop at the bound. | The molecule tracks the **iteration counter** against the formula's declared **bound** (§3.1) so the loop is *boundable*; the *policy* (N-attempts-then-escalate, oscillation detection, L5 ship authorization) is C39's / the reconciler's, not C13's (consistent with C20 §4.3 AMBIGUITY: schema slots here, policy in C39). C13 guarantees the loop cannot exceed the formula-declared bound silently. |
| **Crash mid-run / partial state** | A run interrupted between ticks. | Because all molecule state is in C19 (durable, cross-session) and the resume handle is the root bead, `gc converge resume <bead_id>` reconstructs the molecule with no out-of-band state (AI-CONTEXT §16; README:235). C13 inherits C19's durability posture (and its open crash/atomicity question, C19 OQ-C19-3). |
| **Malformed instantiation** | A formula whose node fails to resolve to a binding, or an unbound declared parameter. | Faithfully a *pre-instantiation* concern: C12 guarantees "every node resolvable, every parameter declared" (C12 §3.3); the linters (C15/C16) check the formula before run. C13's contribution is the **faithful-instantiation invariant** (§4) — it will not silently create a node-bead with an unresolved binding; binding-resolution failure surfaces at instantiation, not as a half-built tree. > [FAITHFUL-FILL] v4 names no instantiation validator; faithful floor is "C12 guarantees resolvability; C13 fails instantiation loudly if a binding/parameter is missing." |
| **Concurrent advance / double-dispatch of a node** | Two ticks (or parallel agents) dispatch the same frontier node. | v4 states no concurrency model for the bead `file` backend (C19 OQ-C19-3) and the reconciler is "per-tick" (serialized ticks, AI-CONTEXT §3.2 concept 9). Faithful: single-writer-per-tick is the reconciler's invariant (C18); C13 does not invent locking v4 does not state — flagged as inherited from C18/C19 (OQ-C13-2). |

> [FAITHFUL-FILL] No C13-assigned gap exists (inventory). The modes above are inherited; each is handled by
> *deferring to the owning component* (C12 for chain bounds, C39/C18 for loop policy, C19 for durability,
> C18 for tick serialization) rather than re-specifying. This is faithful: C13's job is to be the run-state
> subject those owners act on, not to duplicate their controls.

## 7. Cross-cutting (security / cost / scale / observability / ops)

- **Security.** A molecule carries no execution privilege of its own; it is run *state*, not code. Its
  node-beads inherit C41 attribution (`created_by` per node) and the security posture of what each node binds
  to (C17 tool-node confinement, C28 agent loop). The molecule *is* the per-run attribution record — "who did
  which step of this run" is answerable because each node-bead is attributed. C13 adds no new trust surface.
- **Cost / scale.** The molecule is the *runtime realization* of the formula's cost lever: the number of live
  model-node beads in flight = the run's token spend driver. The formula sets the ceiling (chain length, loop
  bound); the molecule *is* the spend as it accrues. No v4 per-molecule budget field; > [FAITHFUL-FILL] none
  invented (cost modeling is C46/G32). Scale is bounded by C19's backend (single-node `file` at Phase 0;
  C19 OQ-C19-3) and the per-tick reconciler cadence (C18).
- **Observability.** The molecule is the **primary observability subject of a run**: its bead-tree + per-node
  `status` is the "where are we?" view, and each node's CXDB trajectory (C21) is the fine-grained record. The
  formula→molecule→bead mapping is what lets a run be replayed (C49) and judged against the formula it came
  from (C33). The molecule makes a run *legible* without a scratchpad (README:235 "Replaces flat scratchpads").
- **Ops.** A molecule is created per run and resumed by bead id; there is no separate molecule artifact to
  version (the *formula* is the version-controlled artifact, C12 §4). The operational handle is the root bead
  id (`gc converge resume`); the operational state is entirely in C19 (one backend to back up / restore).

## 8. Acceptance criteria & test strategy

Sweep-1 high-level criteria (concrete tests at sweep 2, gated on the real `gc` molecule/converge surface — G11):

1. **Faithful instantiation.** Instantiating a 3-step formula (C12 §AC; README:383) produces a bead-tree
   whose nodes and dependency edges are exactly the formula's DAG, with parameters bound to the supplied run
   inputs and every node-bead typed (C20) + attributed (C41).
2. **State-on-beads / no shadow store.** All molecule runtime state (per-node `status`, loop counters, gate
   verdicts, bound params) is readable from C19 alone — there is no molecule state held outside the bead-tree
   (the FAITHFUL-FILL §3.1 invariant: a molecule is a rooted C19 subgraph, not a separate store).
3. **Frontier correctness.** At every tick, the set of runnable node-beads is exactly those whose dependency
   edges are all `done`; a node with an unsatisfied dependency is never dispatched.
4. **Resume across sessions.** A molecule paused mid-run (process restart) is reconstructed identically by
   `gc converge resume <bead_id>` from C19 state, continuing from the persisted frontier with no out-of-band
   state (AI-CONTEXT §16; README:235).
5. **Bounded loop termination.** A formula with a bounded loop (Ralph-style re-entry, one-shot-specs:62)
   instantiates a molecule whose loop node re-enters at most the formula-declared bound, then terminates /
   escalates — it never produces an unbounded chain of beads (F26/F52).
6. **Convergence detection.** A molecule whose terminal nodes are all `done` and gates all passed reports
   `converged`; one with a terminally-failed node or an exhausted loop bound reports `failed`/`escalated`
   (the escalation policy itself being C39/C18's).
7. **Wisp surface.** Each runnable frontier node is presentable to Sling as a wisp carrying its formula-node
   binding (C17 tool node or C09 template name), sufficient for routing without reading the whole molecule.
8. **Provenance / replayability.** Every node-bead traces to its formula node and carries `created_by`, so the
   run can be judged (C33) and branch-replayed (C49) against the formula it instantiated.

(Concrete molecule/`gc converge` signatures, the `status` enum + transition guards, the wisp shape, and
instantiation/resume test vectors are sweep-2 deliverables, jointly with C12, C18, and C19/C20.)

## 9. Open questions

(Mirrored into `_meta/review-log.md`.)

1. **[top open question] Real Gas City molecule / `gc converge` model (G11).** C13's entire structure — whether
   a molecule is a first-class Gas City object or purely a bead subtree, the instantiation verb, the `status`
   enum, the wisp shape, how `gc converge resume` re-attaches — is **Gas City's**, asserted "Native" but
   unverified (no author has run `gc`; G11). Sweep 2 must freeze the concrete molecule/converge model against
   the real `gc` behavior before C18 (driver) and C05 (dispatch) can bind to it. This is the same gating
   uncertainty C12 §9 flags for the Workflow Engine subsystem, here at the runtime-state layer.
2. **Dependency-set reconciliation (brief vs inventory).** The dispatch brief lists C13 as depending on
   **C19/C20** (beads); the canonical inventory lists **C12, C18**. Both are real and non-conflicting: C13
   *instantiates* C12, is *driven by* C18, and is *made of* C19/C20 beads. Faithful resolution: treat all four
   as upstream (C12 = template, C18 = driver, C19/C20 = substance), with C18 the one not-yet-specced at
   sweep-1. Confirm C18's reconciler contract (tick cadence, frontier-advance, gate evaluation, tick
   serialization) so C13's runtime-state contract has a concrete consumer. (→ review-log XC.)
3. **Molecule ⇄ first-class-object boundary (with C19).** §3.1 FAITHFUL-FILL holds that the molecule is a
   *rooted bead subgraph*, not a separate store. Confirm Gas City does not represent molecules as first-class
   persisted objects distinct from beads (which would change the C13↔C19 ownership line and the resume model).
4. **Wisp definition (with C05).** §3.3 FAITHFUL-FILL reads a wisp as the dispatch view of a runnable
   node-bead. Confirm jointly with C05/Sling whether a wisp is bead-derived or a distinct lighter object, and
   pin its shape — this is the C13→C05 contract.
5. **Loop-iteration / status field reconciliation (with C12, C20).** The per-node `status` enum and the
   loop-iteration counter must be the *same* fields C20's envelope (`status`) and C12's loop construct define —
   sweep 2 must reconcile one field across C12/C13/C20, not three (mirrors C12 §9 node-kind reconciliation).
