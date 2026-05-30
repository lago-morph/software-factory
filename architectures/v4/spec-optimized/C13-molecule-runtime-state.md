# C13 — Molecule (instantiated workflow) / runtime state  (Spec, Track B)

> Source: AI-CONTEXT §3.2 concept-7 ("Formula = TOML DAG template; **Molecule = instantiated bead-tree**", l.91; P1/P3/P4/P12), §3.3 vocabulary ("molecule | instantiated workflow / bead-tree", l.102; "wisp | unit of dispatchable work", l.108; "convoy | batched workflow", l.104), §16 cold-agent recovery (`gc bd find`, `gc converge resume <bead_id>`, l.694–699); README Part 4 P10 ("dependency-aware persistent task graph… survives across agent sessions", l.233–244), Part 6 Phase-0/1 ("3-step minimum" formula design→implement→review, README:383); _meta inventory C13 row (maps A22b workflow-instance, B32; depends C12, C18 — see note below; foundational=N); _meta review-log **D-4** (C19↔C20 direction; edge-direction discipline) ; _meta gaps G06 (formula/molecule undefined-term pair — co-owned with C12/C07), G17 (no store schema — the bead-tree envelope is C19/C20's, C13 owns the *tree-shape* invariants), G18 (loop termination — molecule is where a run's bound is realized); F-MODE-COVERAGE P1/P3/P4/P12, F52/F47 (loop/Goodhart at run scope).
> Inventory ID: C13   Kind: artifact (runtime-state instance)   Status: sweep-1
> Deltas: DELTA-01 (molecule = a *named, addressable runtime object* with its own identity + lifecycle state machine, not merely "the set of beads that happen to exist for a run"); DELTA-02 (instantiation is a typed, transactional **bind→materialize→seal** transform from `ParsedFormula`(C12)+`FormulaParameters` to a rooted bead-tree, all-or-nothing); DELTA-03 (the **molecule root bead** — a first-class `molecule` bead carrying `{molecule_id, formula_identity, params, lifecycle_state, bound}` — is the single resume/query anchor for `gc converge resume`, closing the §16 cold-start gap at the run level); DELTA-04 (tree-shape invariants owned *here*: every run bead is `child_of`-reachable from the root, node→bead mapping is total and injective, the molecule's `blocks` sub-graph is the formula's edge-set projected onto beads); DELTA-05 (**run-scope loop bound** — the formula's gate `bound` (C12) is realized as a per-molecule budget the molecule enforces/escalates, giving G18 a concrete owner at the workflow-instance layer; policy numerics still C18/C39); DELTA-06 (dependency on **C19 directly**, not (only) C18 — see "ID-mapping / dependency note"); DELTA-07 (**re-instantiation / branch-from-midpoint** as a first-class operation — a molecule can be re-materialized from a checkpoint for C49 counterfactual replay + C55 methodology A/B, instead of only ever growing forward).

## 1. Purpose & responsibility

C13 is **the runtime state of one in-flight workflow**: the live object you get when a C12 *formula* (an inert TOML DAG template) is **instantiated** for a specific run. Per AI-CONTEXT §3.2 concept-7 the realization is a **bead-tree** — a rooted tree/graph of C19 beads — so a molecule is *not a new store*; it is a **shape and a lifecycle imposed on the existing work-graph** (C19/C20) plus a small amount of own identity/state.

The load-bearing transform: **"a formula (class) + parameters → a molecule (instance): a rooted, attributed bead-tree whose nodes are this run's units of work, whose edges are the formula's dependencies, and whose lifecycle is independently resumable."** Formula : Molecule :: class : object :: AST : process.

C13 owns:
- **Molecule identity + lifecycle** (DELTA-01/03) — a `molecule_id`, a pointer to the originating `FormulaIdentity` (C12) and the bound `params`, and a run-scope lifecycle state machine (`instantiating → running → {converged | failed | escalated | abandoned}` with `paused/resuming`). Materialized as a first-class **`molecule` root bead** so the whole run is one queryable, resumable anchor (the thing `gc converge resume <bead_id>` resolves, §16).
- **The instantiation transform** (DELTA-02) — the typed `instantiate(ParsedFormula, FormulaParameters) → Molecule` operation: map each formula node to a freshly-created C19 bead (`child_of` the root), project each formula edge to a `blocks` edge between the corresponding beads, stamp `created_by`/provenance, and **seal** transactionally (all-or-nothing; a half-built tree never becomes a runnable molecule).
- **The run-shape invariants** (DELTA-04) — the rules that make "this set of beads" a *well-formed molecule*: total+injective node→bead mapping, root-reachability via `child_of`, the `blocks` sub-graph being exactly the formula's projected DAG, and no run bead orphaned from its molecule. These are the *instance-level* analogue of C12's *template-level* well-formedness.
- **Run progression / frontier exposure** (the "live" part) — the molecule answers "what is dispatchable now?" (its ready-frontier, delegated to C19's `ready_frontier` scoped to this molecule) and "where does this run stand?" (per-node completion state), the substrate C05 dispatch and C18 reconciler drive against. C13 does **not** execute nodes; it tracks and exposes their run state.
- **Run-scope loop bound** (DELTA-05) — the molecule carries and enforces the workflow-instance budget (max iterations / wall-budget) derived from the formula's gate `bound` (C12 §4), escalating to C18/C39 policy when exceeded. This is the run-level realization of G18 termination.
- **Checkpoint / re-instantiation** (DELTA-07) — the ability to capture a molecule's run-state and re-materialize a *sibling* molecule branched from a chosen node, the substrate C49 (counterfactual replay) and C55 (methodology A/B) need.

What it is **NOT**:
- **Not the formula.** C12 is the inert template/class; C13 is the live instance. (This is the exact pair G06 flags as load-bearing-but-underdefined; C12 §1 + C13 §1 jointly pin it, C07 links here.)
- **Not a new store.** The durable nodes/edges/persistence are **C19**'s; the per-type payload schemas (incl. whether a `molecule` bead type exists and its fields) are **C20**'s. C13 owns the *tree-shape contract and run lifecycle*, layered over C19/C20 — it persists nothing C19 doesn't.
- **Not the dispatcher.** C05 routes a ready bead/wisp to an agent; C13 only computes/exposes the ready set. "wisp = unit of dispatchable work" (AI-CONTEXT §3.3) ≈ a molecule's leaf-most ready bead handed to C05.
- **Not the reconciler.** C18 runs the per-tick desired-state convergence and evaluates `gate` nodes; C13 supplies the run-state C18 converges *toward* and records C18's gate verdicts as bead transitions. (Loop *policy* — N attempts → escalate, oscillation — is C18/C39, per XC-3; C13 only owns the *bound slot* and the escalation *signal*.)
- **Not the executor of nodes.** `agent` nodes run on C28 via C05; `tool` nodes on C17; `gate` nodes are evaluated by C18. C13 maps formula-node→bead and tracks each bead's state; it never invokes a node.
- **Not the trajectory.** A molecule is the *work*-tree (C19); the *conversation*-DAG of each agent node's turns is CXDB (C21). They join only via attribution/ids, never by a bead being a turn (README l.241–244).

## 2. Context & dependencies

### ID-mapping / dependency note (DELTA-06)
The inventory lists C13 `Depends on: C12, C18`. **C18 is the wrong primary edge.** A molecule is "an instantiated **bead-tree**" (AI-CONTEXT §3.2 concept-7) — its durable substrate is **C19** (the bead work-graph), which C13's builder for C19 already names as a consumer ("a molecule *is* an instantiated bead-tree… C13 builds on C19's graph", C19 §1/§2). C18 *drives* a molecule's convergence but a molecule exists, persists, and is resumable **without** the reconciler running. We therefore record **C13 → {C12 (template source), C19 (durable bead-tree substrate)} as primary; C18 as a *runtime collaborator*, not a build-time dependency.** Same C-ID retained for diffability; this is a dependency-direction correction, not a split. (Co-owns the edge-direction discipline D-4 applies to C19↔C20.)

- **Depends on:**
  - **C12** (formula) — supplies `ParsedFormula` + `FormulaIdentity` + the `NodeBinding`/`CanonicalForm`/gate-`bound` contracts. C13's `instantiate` consumes C12's *validated, fully-bound* graph; C13 assumes well-formedness was already proven by C12 and does **not** re-lint the template (it validates only the *instance* shape).
  - **C19** (bead store / typed work-graph) — the durable substrate. Molecule beads are C19 beads; `child_of` (tree) and `blocks` (dependency) are C19's named edge taxonomy; resume is C19's `find`/`walk`; the ready-frontier is C19's `ready_frontier()` scoped to a molecule. C13 is a *shape + lifecycle* over C19, not a parallel store.
  - **C20** (bead schema) — governs the `molecule` (root) bead type's payload schema + lifecycle states, registered via the C20↔C22 seam (D-3). C13 *specifies* the run-state fields; C20 *owns* their schema. Soft/co-foundational, like C19↔C20.
  - **C03** (config) — `[formulas]` flag gates whether molecules exist at all (Phase 0 off → implicit single-step "molecule of one"; Phase 1 on → real bead-trees, README:369/383).
  - **C41** (identity) — every run bead's `created_by` (the molecule's instantiator/owner actor) is a non-null C41 reference (inherited from C19's DELTA-02 invariant).
- **Runtime collaborators (not build-time deps):**
  - **C18** (reconciler) — ticks the molecule toward convergence; evaluates `gate` beads; signals when a node's bound is hit. **C05** (sling) — consumes the molecule's ready-frontier to dispatch. **C28/C17** — execute `agent`/`tool` node beads.
- **Consumed by (fan-out):**
  - **C18** (run state to converge), **C05** (ready-frontier), **C39** (fix-task beads attach *into* a molecule's tree as `child_of`/`caused_by`), **C33** (satisfaction reads the molecule's terminal/judge beads per run), **C49** (counterfactual replay branches a molecule from a midpoint, DELTA-07), **C55** (runs the *same* spec under different formulas → comparable molecules, the methodology-experiment unit), **C52** (self-bootstrap is itself a molecule; resume of an in-progress build = resume of a molecule, §16 `factory_build_in_progress`), **AI-CONTEXT §16** cold-start (`gc converge resume <molecule_root_bead_id>`).
- **Sits at:** the **Workflow Engine** runtime layer — one level above C12 (template) and directly on C19 (graph). Batch 2 (per inventory: instantiable once C12 + C19 shapes are fixed). Not foundational (it's an instance pattern over foundational stores), but on the critical run-path: nothing executes a workflow without a molecule.

## 3. Interfaces / contracts

Named-and-described (sweep 1; concrete signatures, bead-payload JSON, and Mermaid lifecycle/sequence diagrams in sweep 2).

**Inbound — the molecule lifecycle API (what callers invoke):**
- **`instantiate(parsed_formula, params, owner_actor) → Molecule`** — the DELTA-02 bind→materialize→seal transform. Pre: `parsed_formula` is C12-validated and fully bound; all required `params` present (C12 enforced totality, C13 asserts it). Post: a sealed molecule with a `running` root bead, a total node→bead mapping, projected `blocks` edges, and the formula's gate-`bound` recorded. **All-or-nothing**: on any per-node create failure the partial tree is rolled back (or marked `instantiation_failed` and never `running`); no half-built molecule is dispatchable.
- **`resume(molecule_id) → Molecule`** — reconstruct the live molecule from C19 (root bead + `child_of` tree + per-node state). The substrate of `gc converge resume` (§16). Pure read over C19; no new beads. Returns the molecule in whatever lifecycle state it was last persisted at.
- **`branch(molecule_id, from_node, overrides?) → Molecule`** (DELTA-07) — materialize a *sibling* molecule sharing history up to `from_node`, then diverging (new params/formula-variant). The C49/C55 hook. Records lineage (`branched_from`) on the new root.
- **`record_node_outcome(molecule_id, node_bead_id, outcome) → ()`** — the seam C18/C05/C28/C17 call to advance a node's bead lifecycle (e.g. `done`/`failed`/gate-verdict). Bumps the molecule's progress; may trigger frontier recomputation or bound-escalation. (C13 *records*; it does not decide policy.)
- **`abandon(molecule_id, reason) → ()`** — terminal transition to `abandoned`, attributed; leaves the tree intact for audit.

**Inbound — run-state query contract (frozen early for C05/C18/C33/C49):**
- **`ready_frontier(molecule_id) → [Bead]`** — molecule-scoped dispatchable set (delegates to C19 `ready_frontier`, filtered to this molecule's subtree). What C05 pulls from.
- **`state(molecule_id) → MoleculeState`** — `{lifecycle_state, nodes: per-node status, completed/total, bound_remaining, root_bead_id}`.
- **`node_for(molecule_id, formula_node_id) → BeadId`** / **`formula_node_for(bead_id) → NodeId`** — the bidirectional node↔bead mapping (DELTA-04 total+injective).

**Outbound (what C13 calls):**
- → **C19**: `create`/`update`/`add_edge`/`walk`/`find`/`ready_frontier` — all durable graph operations.
- → **C20**: `validate(molecule_root_bead)` at root create (the run-state payload schema check).
- → **C12**: reads `ParsedFormula`/`NodeBinding`/`bound` (no mutation of the template).
- → **C41**: stamps `created_by` (inherited C19 invariant).

**Invariants** (DELTA-04 — C13 owns the *instance* shape; C19 owns *graph* acyclicity/durability):
- **Rooted:** exactly one `molecule` root bead per molecule; every run bead is `child_of`-reachable from it (no orphan run beads). The root is the resume anchor.
- **Total + injective node→bead mapping:** every formula node maps to exactly one run bead and vice-versa; no formula node is unmaterialized, no run bead is unmapped (excepting *later-injected* fix-task beads, which attach via `caused_by` and are marked non-template).
- **Edge-projection fidelity:** the molecule's `blocks` sub-graph is exactly the formula's edge-set projected onto beads — neither edges added nor dropped at instantiation. (Acyclicity follows from C12's DAG guarantee + C19's `add_edge` cycle-rejection; C13 asserts equality, not just acyclicity.)
- **Sealed-before-runnable:** a molecule transitions to `running` only after the full tree is materialized + sealed; `instantiating`/`instantiation_failed` molecules are never in any `ready_frontier`.
- **Bound monotonicity (DELTA-05):** the run-scope budget only decreases; reaching zero forces a transition out of `running` (→ `escalated`), never silent looping (G18/F52).
- **Resume fidelity:** `resume(id)` reconstructs a molecule byte-equivalent in run-state to the last persisted state — the molecule is *entirely* recoverable from C19 (no C13-private durable state).
- **Identity stability:** `molecule_id` and its `formula_identity` are immutable post-seal; a methodology change = a new/`branch`ed molecule, never an in-place rewrite (so C55/C33 joins stay sound).

## 4. Data model / state

C13's durable state lives **entirely in C19** (DELTA-03: "no C13-private store"). What C13 *defines* is the shape and the run-state fields carried on beads.

**The `molecule` root bead** (payload schema owned by C20, fields specified by C13):

| Field | Meaning | Notes |
|---|---|---|
| `molecule_id` | stable run identity | the `gc converge resume` anchor (§16) |
| `formula_identity` | `{name, version, methodology_id}` from C12 | the C55/C33/C50 join key; immutable post-seal |
| `params` | the bound `FormulaParameters` (C12) | snapshot of what this run was instantiated with |
| `lifecycle_state` | `instantiating \| running \| paused \| converged \| failed \| escalated \| abandoned` | the run-scope state machine (§5) |
| `bound` | run budget (max-iterations / wall-budget) from formula gate `bound` (C12) | DELTA-05; decremented as the run progresses |
| `bound_remaining` | live budget | hits 0 → `escalated` |
| `branched_from` | optional `{molecule_id, node}` lineage | DELTA-07 (C49/C55) |
| `created_by`, `seq`, `bead_format_version` | inherited C19 envelope | attribution + ordering + evolution |

**Run (node) beads** — one per formula node, `child_of` the root:
- type/payload per node kind: an `agent` node-bead references its `template_ref` (C09) + dispatch state; a `tool` node-bead its `tool_node_id` (C17); a `gate` node-bead its predicate + C18 verdict; a `sub_formula` node-bead points at a *nested molecule's* root (composition = a child molecule).
- per-node run status (`pending → ready → dispatched → done | failed | gated`) — the projection C05/C18 drive.
- `blocks` edges among run beads = the formula's edges; `caused_by` edges attach later fix-task beads (C39) into the live tree.

**Lifecycle ownership split (the load-bearing clarity for G06/G17):**
- **C12** owns the *template* schema (inert TOML, well-formedness invariants).
- **C19** owns the *bead envelope*, the *edge taxonomy*, *durability*, and *graph acyclicity*.
- **C20** owns the *per-type payload schema + lifecycle states* (incl. the `molecule` type).
- **C13** owns the *instantiation transform*, the *tree-shape invariants*, the *run lifecycle state machine*, the *bound enforcement*, and *resume/branch* — i.e. everything that makes the bead-tree a *molecule* rather than just a pile of beads.

**Persistence/consistency:** none beyond C19's (append+fsync+atomic-rename, DELTA-04 of C19). Instantiation is **transactional at the C13 layer** (DELTA-02): it either seals a complete molecule or leaves no `running` molecule. Resume is a pure read; there is no C13 cache that can diverge from C19.

## 5. Behavior

Four flows (sweep-2 adds Mermaid lifecycle + instantiation sequence diagrams):

1. **Instantiate (formula → molecule).** Caller hands a C12 `ParsedFormula` + `params` + `owner_actor`. C13: (a) creates the `molecule` root bead (`instantiating`), (b) for each formula node creates a `child_of` run bead with its `NodeBinding`, (c) projects each formula edge to a `blocks` edge (C19 `add_edge`, which rejects cycles — a redundant safety net over C12's DAG guarantee), (d) asserts the tree-shape invariants (§3), (e) **seals**: root → `running`. Any failure before seal → rollback / `instantiation_failed`; never a half-runnable molecule.
2. **Run / progress.** C18 ticks; C05 pulls `ready_frontier(molecule_id)` and dispatches leaf-ready beads to C28/C17. As nodes complete, `record_node_outcome` advances bead state, recomputes the frontier, and decrements `bound`. `gate` beads carry C18's convergence verdict. When the last node converges → root `converged`; on unrecoverable node failure → `failed`; on bound exhaustion → `escalated` (hand to C18/C39 policy). The molecule is the *run-state ledger* C18 converges and C33 later scores.
3. **Resume (cold-start / crash recovery).** A restarted agent runs `gc converge resume <molecule_root_bead_id>` (§16). C13 `resume` reads the root + `child_of` subtree + per-node state from C19 and reconstructs the live molecule exactly — because *all* run-state is durable in C19, resume is lossless and needs no C13-private journal. (This is the §16 "find its bead → resume the workflow" path; `factory_build_in_progress` molecules (C52) resume identically.)
4. **Branch / re-instantiate (DELTA-07).** For C49 counterfactual replay or C55 methodology A/B: `branch(molecule_id, from_node, overrides)` materializes a sibling molecule sharing history up to `from_node`, then diverging with new params or a variant formula. Lineage recorded; the two molecules are independently runnable + comparable (same `formula_identity.methodology_id`, different `version`/params → exactly the C50/C55 comparison unit).

The *methodology* is never expressed in C13 — it lives wholly in the C12 formula. C13 is the **mechanism that turns one chosen methodology into one running, resumable, attributable, bounded instance**.

## 6. Failure modes & handling

- **G06 (formula/molecule undefined-term pair)** — *primary clarity gap, co-owned with C12/C07.* **Mitigation:** C13 §1 is the authoritative definition of "molecule" (instance) against C12's "formula" (template): class↔object, with the bead-tree realization pinned. C07 glossary links here for "molecule/bead-tree/wisp"; the template-vs-instance line that confuses readers is now testable as the C12/C13 boundary.
- **G18 / F52 (no run-level termination → infinite loop / "more controller patches")** — *the run is where an unbounded loop actually burns tokens.* **Mitigation (DELTA-05):** every molecule carries a `bound` (from the formula's gate `bound`, C12) and enforces `bound_remaining` monotonic decrease; exhaustion forces `escalated`, never silent re-iteration. C13 owns the *slot + signal*; the numeric *policy* (N attempts, oscillation detection, L5 ship authorization) stays C18/C39 (XC-3). This gives G18 a concrete owner at the workflow-instance layer that the docs lacked.
- **Half-built / torn molecule** — a crash mid-instantiation leaving a partial tree that looks runnable. **Mitigation:** sealed-before-runnable invariant + transactional instantiate (DELTA-02). A molecule is `running` only after a complete sealed tree; `instantiating`/`instantiation_failed` roots are excluded from every frontier, so a torn tree can never dispatch work. Resume of an `instantiating` molecule re-drives to seal-or-fail, not to a partial run.
- **Orphaned run beads (G17-adjacent shape bug)** — a run bead not reachable from any molecule root, so it can't be resumed/audited as part of a run. **Mitigation:** rooted + total-mapping invariants (DELTA-04); every run bead is `child_of`-reachable from exactly one root. Fix-task beads (C39) injected later attach via `caused_by` into the live tree, keeping them in-molecule.
- **Edge-projection drift** — instantiation silently adds/drops a dependency vs the formula (run diverges from declared methodology). **Mitigation:** edge-projection fidelity invariant — the molecule's `blocks` sub-graph must *equal* the formula's projected edge-set; asserted at seal. This keeps C55/C33's "this run = this methodology" claim honest.
- **Resume divergence** — a resumed molecule differs from its pre-crash state. **Mitigation:** resume-fidelity invariant + no-C13-private-durable-state (all run-state in C19, recovered by `child_of` walk). The molecule is a *pure projection* of C19, so resume is deterministic.
- **Methodology drift mid-run (corrupts C55/C50)** — `formula_identity` changed in place. **Mitigation:** identity-stability invariant — `molecule_id`/`formula_identity` immutable post-seal; a methodology change is a `branch`, producing a new comparable molecule, never an in-place edit.

## 7. Cross-cutting (security / cost / scale / observability / ops)

- **Security:** a molecule is an *attributed* run — `created_by` on the root + every run bead (C41) means "which actor instantiated/owns this workflow" is always answerable (P9). A `sub_formula`/`branch` cannot escape the originating actor's capability set (inherited from C12's pack/capability constraint + C19 attribution). When C52 self-bootstrap *generates* molecules, the molecule root is the audit anchor for "the factory built this".
- **Cost:** the molecule is the natural **cost-accounting unit** — cost-per-run = tokens/tool-cost summed over a molecule's node beads, the granularity C46 keys cost-per-satisfaction against (joined via `formula_identity`). The `bound` (DELTA-05) is the per-run cost circuit-breaker (G32/G13 single-Max-seat budget pressure: a runaway molecule is capped, not unbounded).
- **Scale:** molecules are graph-shaped and cheap; the only scale concern is many concurrent molecules sharing one C19 store — bounded by C19's concurrency contract, not C13. A `convoy` (AI-CONTEXT §3.3, "batched workflow") is *N molecules dispatched together*, a C05-layer batching concept over C13 instances (named here for vocabulary completeness; convoy mechanics are out of C13 scope).
- **Observability:** the molecule root `molecule_id` + `formula_identity` is the **join key** between the work-graph (C19), the trajectory store (C21, each node's turns), and satisfaction (C33). "Which methodology/version/params produced this run, and where did it stand?" is one root-bead lookup. Every lifecycle transition is a C19 mutation → C23 event (the trajectory-shaped feed).
- **Ops:** resume-from-bead (§16) means an in-flight workflow survives crash/restart as a first-class operation, not a best-effort recovery; `gc converge resume <molecule_root>` is the single operator verb. A stuck molecule is `escalated`, surfacing in `gc bd find --type molecule --state escalated`.

## 8. Acceptance criteria & test strategy

1. **Instantiation transform (DELTA-02):** a C12-validated `ParsedFormula` + complete `params` instantiates to a sealed `running` molecule with a `molecule` root and one `child_of` run bead per formula node; the README "3-step minimum" formula (design→implement→review, README:383) instantiates to a 3-node + root molecule. (Shared fixture with C12 AC#7.)
2. **All-or-nothing seal (DELTA-02 / sealed-before-runnable):** an injected per-node create failure mid-instantiation yields **no** `running` molecule (rollback or `instantiation_failed`); a torn molecule never appears in any `ready_frontier`.
3. **Tree-shape invariants (DELTA-04):** rooted (single root, no orphan run beads), total+injective node↔bead mapping, and edge-projection fidelity (molecule `blocks` sub-graph == formula edge-set projected) all hold post-seal; a fixture that drops/adds an edge fails the seal assertion.
4. **Resume fidelity:** instantiate → run partway → simulate crash → `resume(molecule_id)` reconstructs an identical run-state (lifecycle, per-node status, `bound_remaining`) purely from C19; no C13-private state needed. (Drives `gc converge resume`, §16.)
5. **Run-scope bound (DELTA-05 / G18):** a molecule whose run exceeds its `bound` transitions to `escalated` (not silent looping) and signals C18/C39; `bound_remaining` is monotonic non-increasing. (F52 fixture.)
6. **Branch / re-instantiate (DELTA-07):** `branch(molecule_id, from_node)` produces a sibling molecule sharing history up to `from_node`, with `branched_from` lineage and the same `methodology_id`; the two are independently runnable + identity-comparable. (C49/C55 fixture.)
7. **Identity stability:** `molecule_id`/`formula_identity` are immutable post-seal; an attempt to rewrite the methodology in place fails — only `branch` produces a new methodology run. (C55/C33 join-soundness fixture.)
8. **Vocabulary authority (G06):** C07 glossary entries for molecule / bead-tree / wisp link to C13 as the definition source; the formula(template) vs molecule(instance) distinction is testable as the C12↔C13 boundary contract.
9. **Dependency-direction correction (DELTA-06):** a molecule can be instantiated, persisted, and resumed with C18 (reconciler) **absent** — proving C19, not C18, is the build-time substrate dependency.

## 9. Open questions

- **OQ1 (→ review-log) — Does Gas City natively model a "molecule" as a first-class object, or is "molecule" purely v4's name for "the bead-tree under a run-root"?** If `gc` has a native molecule/convergence object with its own state, C13's root-bead + lifecycle (DELTA-01/03) must conform-or-wrap it; if not, C13's root-bead *is* the molecule. Gated on the same unverified-Gas-City risk as C12 OQ1 / G11. **Top open question** — the whole instance model is downstream of confirming `gc converge`'s real object model.
- **OQ2 — Confirm the C13→C19 (not C13→C18) dependency-direction correction (DELTA-06) at the integrator pass.** The inventory says `Depends on: C12, C18`; this spec argues C18 is a runtime collaborator and C19 is the true substrate dep. Mirror of the D-4 edge-direction discipline; needs a canonical ruling. (→ review-log, XC-style.)
- **OQ3 — Where exactly does the run-scope `bound` policy numerics live (C13 slot vs C18/C39 policy vs C12 declaration)?** C13 owns the slot+signal (DELTA-05); XC-3 assigns the numeric policy to C39 (and maybe C18). Confirm the three-way split so a runaway run has exactly one escalation owner.
- **OQ4 — Is `sub_formula` composition realized as a *nested child molecule* (this spec's reading) or flattened into the parent tree at instantiation?** Determines whether C13 resume/branch operate on a molecule *forest* (nested roots) or a single flat tree — and whether C55 can compose methodologies (ties to C12 OQ3). Co-specify with C12.
- **OQ5 — Branch/checkpoint granularity for C49 (DELTA-07): can a molecule branch from *any* node, or only at gate/checkpoint boundaries?** Arbitrary-midpoint branching is the C49 "largely unsolved" ask (G19); restricting to gate boundaries is cheaper and may suffice for C55. Co-specify with C49.
