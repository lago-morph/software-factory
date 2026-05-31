# C17 — Tool-Node Abstraction  (Spec, Track A)

> Source: README §"Principle 4 — Deterministic-first" (lines 152–162; the "Tool node abstraction" row line 158 "Gas City native — tool beads … Native", and line 154 "Tool nodes are cheap and reproducible. Most steps don't need a model. Use models only where reasoning is required."), README §Part 3.1 "P4 (deterministic-first): reconciler + tool-node primitives available" (line 370), README §13.3-equivalent tool sketches (Inspect AI subprocess line 599, bridge line 389, satisfaction aggregator line 426). AI-CONTEXT §3.2 "nine concepts" concept 7 Formulas+Molecules / concept 9 Health Patrol (lines 91, 93), §3.5 P4 strength row "Strong (reconciler + tool nodes)" (line 69), §13.3 `[[tool]]` subprocess sketch (lines 599–608). F-MODE-COVERAGE F51 (Ashby-deficient probabilistic guard; line 76) and F52 (tempting-wrong-hybrid / deterministic-without-purpose; line 100). component-inventory C17 row (deps C02; gap G29; foundational yes); component-inventory-A A35 (Tool node abstraction; RM P4, AC §3.2), A17 (P4 deterministic-first cross-cutting). C02 spec `spec/C02-pack-extension-abi.md` (the ABI C17 is realized over).
> Inventory ID: C17   Kind: component   Status: sweep-1
> Track: A (faithful)

## 1. Purpose & responsibility

C17 is the **unified workflow-engine view of a deterministic step**: the single abstraction the v4
Workflow Engine uses for "a step that doesn't need a model." In Gas City terms this is a **tool bead /
tool node** (README:158 "Tool node abstraction — Unified interface for deterministic steps — Gas City
native — tool beads — Native"). It is the realization, inside formulas and molecules, of **Principle 4
(deterministic-first)**: "Tool nodes are cheap and reproducible. Most steps don't need a model. Use models
only where reasoning is required." (README:154; AI-CONTEXT §3.5 P4 = "Strong (reconciler + tool nodes)").

Where **C02** owns the *wire protocol + bundle format* for a subprocess tool node (the `[[tool]]`
declaration and the input/output/status ABI — the G29 seam), **C17 owns the workflow-engine abstraction
over that protocol**: how a deterministic step is named, placed in a formula/molecule (C12/C13), bound to
a concrete tool-node implementation, invoked by the reconciler/dispatch path, and how its result advances
the work graph. C17 is the contract that lets a formula author write "this node is deterministic" without
caring whether the binary is Go, Python, or a CLI, and without re-implementing the C02 ABI per node.

**Responsibilities**
- Define the **tool-node abstraction**: the logical shape of a deterministic workflow step — its identity
  (`name`), its bound implementation (a C02 `[[tool]]` subprocess), its declared inputs/outputs (the
  placeholder context it consumes and the partition/result it produces), and its **determinism contract**
  (same inputs → same outputs; no model call; reproducible).
- Provide the **uniform interface** that formulas (C12) and molecules (C13) use to reference a deterministic
  step, so a node can be placed in a DAG identically regardless of the tool's implementation language
  (README:253–255 Python tool nodes; README:426 Go tool node; README:170 Inspect-AI CLI as tool node).
- Establish the **node-kind boundary**: a *tool node* is the deterministic kind; an *LLM/agent node* (a
  step that calls a model) is a **different node kind** and is out of C17's scope. C17 is the surface P4's
  discipline tooling (C16 / A36b) checks against — "is this LLM node really necessary, or would a tool node
  suffice?" (README:160 "Discipline tooling — Catches LLM-where-tool-suffices"; F-MODE F52).
- Carry the **determinism / reproducibility invariant** that makes a tool node the *primary* guard in the
  deterministic-first posture (A17; F-MODE F51 "deterministic boundary typing is the primary guard;
  LLM-judge is secondary").

**Explicitly NOT**
- NOT the **subprocess ABI / pack bundle** (C02). C02 defines *how* a tool-node binary is declared and
  exchanges bytes; C17 defines the *workflow abstraction* that binds a deterministic step to such a binary.
  C17 **depends on** C02; it does not redefine the wire protocol.
- NOT the **Gas City substrate / executor** (C01). C01's reconciler + tool-bead executor *run* a tool node;
  C17 is the abstraction they execute, not the engine.
- NOT the **formula format** (C12) or the **molecule** runtime (C13). C17 is referenced *by* a formula node;
  it does not own the DAG template or the instantiated bead-tree.
- NOT an **LLM / agent node**. Model-calling steps are a different node kind (owned by the session/provider
  + model-floor side, C04/C28/C29). C17's whole point is to be the *non-model* alternative.
- NOT the **reconciler / Health Patrol** (C18). C18 decides *when* to (re)run a node and handles
  convergence/retry; C17 defines *what a node is*.
- NOT the individual deterministic tools themselves (the EARS spec linter C10, the workflow/discipline
  linters C15/C16, the CXDB bridge C24, the satisfaction aggregator, the anomaly/embedding/clustering
  Python nodes). Each of those is *a* tool node — an instance built against C17's abstraction and C02's ABI.

## 2. Context & dependencies

| Direction | Component | Relationship |
|---|---|---|
| Upstream (depends on) | **C02** pack/tool-node ABI | C17's abstraction is realized over C02's `[[tool]] type="subprocess"` declaration + input/output/status ABI (the G29 seam). C17 = workflow view; C02 = wire protocol. |
| Upstream (runtime) | **C01** Gas City substrate | C01's reconciler + tool-bead executor spawn and run the subprocess a C17 node binds to. |
| Upstream (terms) | **C07** vocabulary-glossary | Canonical meaning of `tool bead`/`tool node`, `formula`, `molecule`, `bead` (G06). |
| Downstream (places nodes) | **C12** formula format, **C13** molecule | A formula DAG references a C17 deterministic node; a molecule instantiates it as a bead. |
| Downstream (disciplines on it) | **C16** discipline linter (A36b), **C15** workflow linter | C16 flags LLM nodes that should be C17 tool nodes (F52); C15 lints the formula structure that places them. |
| Downstream (instances — "a tool node") | **C24** CXDB bridge, **C30/C31** scenario store/runner, **C10** EARS spec linter, **C33** satisfaction aggregator, **C44** digital twin, and every component the inventory marks "tool node" / "Python tool node" | Each is built *as* a C17 deterministic node over the C02 ABI. The inventory routes C30, C31, C44 explicitly through C17 as a dependency. (C32 the LLM-judge is *not* a C17 tool node — it is a model-calling step, the node kind C17 explicitly excludes.) |

C17 is **foundational** (inventory: yes) and lives in **Batch 1**, authored in parallel with C02/C01
because nearly every deterministic step in the factory is "a C17 tool node."

## 3. Interfaces / contracts

Sweep 1 — interfaces **named and described**; concrete signatures/schemas deferred to sweep 2.

### 3.1 The tool-node abstraction (the unified interface)

A **tool node** is a workflow step described by these named elements (sweep-1 descriptions; the wire-level
realization of inputs/outputs/status is C02's, referenced, not redefined):

| Element | Description | Source / fill |
|---|---|---|
| `name` (node identity) | The logical identity a formula/molecule references when placing the step. Resolves to a C02 `[[tool]]` of the same `name`. | README:158; C02 §3.2 `name` |
| `kind = deterministic` | Declares this is a tool node, not a model/agent node. The node-kind tag the discipline linter (C16/F52) keys on. | > [FAITHFUL-FILL] |
| Bound implementation | The C02 `[[tool]] type="subprocess"` (command/args/work_partition) the node executes. | C02 §3.2 |
| Declared inputs | The placeholder context the node consumes (e.g. `{scenario_path}`, `{task}`), drawn from the molecule/bead context and substituted into C02 `args` (+ optional stdin in C02's JSON profile). | AI-CONTEXT §13.3; C02 §3.2 |
| Declared outputs | What the node produces back to the work graph: files in its `work_partition` and/or a structured result, surfaced to the molecule as the step's product. | C02 §3.2; C02 §3.3 |
| Status | Success/failure of the step = the C02 exit-code status; the workflow engine reads it to advance or block the DAG. | C02 §3.2 (exit code) |
| **Determinism contract** | Same declared inputs ⇒ same declared outputs; no model call; reproducible. The invariant that makes the node a valid P4 deterministic guard. | README:154; A17; F51 |

> [FAITHFUL-FILL] **`kind = deterministic` tag.** v4 names "tool node" and "LLM node" as distinct (README
> contrasts deterministic tool nodes vs. model steps, and C16/A36b's whole job is "catches
> LLM-where-tool-suffices"), but the four docs never give the explicit node-kind field. The minimal
> faithful fill is a single node-kind tag distinguishing `deterministic` (tool node) from the model/agent
> kind, because the discipline linter (F52) cannot fire without a machine-readable distinction. C17 only
> *names* the tag; the enforcement policy is C16's.
> *Consistency note:* C02-faithful §3.2 already states a "deterministic-first" tool-node invariant for the
> same concept at the ABI layer. The two fills are the same distinction at different layers; the tag's
> *home* (the C12 formula-node entry vs. the C02 `[[tool]]` block — **not** a C17-owned new file) is the
> open reconciliation, tracked as OQ-2 with C12/C16.

### 3.2 Inbound: how a formula/molecule references a C17 node

A formula DAG node (C12) that is deterministic references a tool node **by `name`**; instantiation (C13)
binds that name to the C02 `[[tool]]` and supplies the molecule context that feeds the declared inputs.
The contract C17 freezes for C12/C13 is: *a deterministic node is referenced uniformly by name + declared
inputs/outputs, independent of the bound binary's language*. This is the "unified interface" of README:158.

> [AMBIGUITY: G29] **Where the input/output/status realization lives.** Two faithful readings of the C17↔C02
> split: **Reading A** — C17 is a *thin naming/abstraction layer* and the entire I/O channel (args/files/
> exit-code, optional stdin/stdout-JSON) is C02's; C17 adds only node-kind + determinism semantics.
> **Reading B** — C17 *owns a workflow-facing input/output declaration* distinct from the ABI (which context
> keys a node consumes and which outputs it surfaces) while C02 owns only the byte-level wire format.
> **Pick Reading A.** The *bytes and the I/O contract itself* are C02's (G29 is resolved there, in
> `spec/C02-pack-extension-abi.md` §3.2, which already enumerates the input/output/status channels
> as ABI elements). C17 adds only: the **node-kind** tag, the **determinism** semantics, and the **uniform
> by-name reference** a formula uses to place the step. C17 does **not** introduce a third "workflow-level
> I/O declaration" ownership band — *which placeholder keys a node fills* is the **C12** formula-node entry
> (the node's args/context binding), and *which bytes those become* is C02's ABI. Rationale: this is the
> only split that keeps C17 thin (consistent with §4/§8 "no new on-disk artifact / view-only"), avoids
> duplicating C02's already-resolved seam, and matches C02 scoping itself "NOT the tool-node abstraction as a
> workflow concept (C17)" while owning the wire contract. C17 therefore does **not** re-specify the wire
> bytes or a parallel I/O declaration; it cites C02 (bytes) and C12 (which placeholders a node fills).

### 3.3 Outbound: what C17 guarantees to dependents

- To **C12/C13** (formula/molecule): a stable "reference a deterministic step by name + declared inputs;
  get a status + declared outputs back" contract, identical across tool-node implementation languages.
- To **C16** (discipline linter): a machine-readable node-kind tag so "LLM node where a tool node would
  suffice" can be detected (F52).
- To **C18** (reconciler): a step whose success/failure is a clean status signal and whose re-execution is
  *intended* to be safe because the node declares the determinism contract. (Note: v4 specifies no runtime
  determinism check; safe re-run is the declared P4 payoff, enforced by the contract + C16/test — not a
  C17 runtime-checked guarantee. See §6 and OQ-3.)
- To **every "tool node" component** (C24, C30–C33, C44, …): one abstraction to build against, so a new
  deterministic tool is "declare a `[[tool]]` (C02) + reference it as a deterministic node (C17)," nothing
  more.

## 4. Data model / state

C17 is a **component/abstraction**, not a data store; it owns *the node definition shape*, not live state.

- **Node definition** (named, sweep-1): the logical record binding `name` → C02 `[[tool]]` + `kind=deterministic`
  + declared inputs/outputs. Where this record physically lives is C12's formula TOML (the node entry in a
  DAG) plus the C02 `[[tool]]` block it resolves to — C17 does not introduce a third file.
  > [FAITHFUL-FILL] C17 adds no new on-disk artifact; it is a *view* over C12 nodes + C02 tools. Minimal-
  > consistent because v4 calls it "native — tool beads" with no separate store, and introducing one would
  > be an architectural addition the faithful track forbids.
- **Per-execution state** (a tool node's invocation) belongs to **C13** (the molecule/bead the run produces)
  and **C19/C20** (the bead and its schema), carrying `created_by` (C41) and landing on the event bus (C23).
  C17 owns no runtime state of its own.
- **Determinism property** is a *declared invariant*, not stored data: C17 asserts it; C16's discipline
  linter and C18's safe-re-run rely on it.

## 5. Behavior

Key flow (sweep-1 narrative; sequence diagram deferred to sweep-2):

1. A formula author places a **deterministic node** in a DAG (C12), referencing a tool node by `name` and
   declaring its inputs/outputs.
2. At run time the molecule (C13) **instantiates** the node as a bead and binds it to the C02 `[[tool]]` of
   the same `name`, supplying the declared inputs from molecule/bead context.
3. The reconciler/dispatch path (C18/C01) reaches the node; Gas City **substitutes `{placeholders}` and
   spawns** the subprocess per the C02 ABI in the declared `work_partition`.
4. The subprocess runs deterministically (no model call), produces its **declared outputs** (partition
   files / structured result) and a **status** (exit code) per C02.
5. C17's abstraction surfaces that status + outputs to the molecule as the step's product; on success the
   work graph advances; on failure the status blocks the DAG and C18/C40 own retry/escalation.
6. Because the node *declares* determinism, **re-running it on the same inputs is intended to be safe** —
   the declared property C18's convergence loop and C40's crash-survival lean on (the P4 payoff). v4
   specifies no runtime enforcement; the property is contract-declared and C16/test-enforced, not
   C17-guaranteed at runtime (see §6, OQ-3).

The discipline behavior P4 asserts: deterministic nodes are the *default*; a model/agent node must be
*justified* (README:154, :160). C17 is the surface that makes "is this step deterministic?" a first-class,
checkable question (F52).

## 6. Failure modes & handling

| F-mode | Relevance to C17 | Handling (faithful) |
|---|---|---|
| **F51** Ashby-deficient probabilistic guard | C17 tool nodes are the **primary** (deterministic) guard; LLM-judge is secondary (F-MODE §76). | The deterministic-first abstraction *is* the mitigation: C17 gives the engine a non-probabilistic node kind so boundary-typing/validation steps are deterministic, not model calls. (Addressed.) |
| **F52** Tempting-wrong-hybrid / deterministic-without-purpose | Risk that P4 becomes "discipline without purpose" — tool nodes (or LLM nodes) added with no falsifying scenario (F-MODE §100). | C17 exposes the machine-readable node-kind tag (3.1 fill) so C16/A36b can enforce "every guard points at a scenario it catches; no LLM node where a tool node suffices." C17 *enables* the check; the policy + monthly catch-count review is C16's. |
| **Tool-node nonzero exit / crash** | A deterministic step fails. | Status = C02 exit code (3.1); C17 surfaces it; the reconciler/Health-Patrol (C18) and Orders (C40) own retry/escalation. Deterministic re-run is safe (5.6). > [FAITHFUL-FILL]: v4 gives no C17-level retry contract; minimal-consistent placement is "C17 surfaces status; convergence loop decides," since C18/C40 own retries/crash-survival. |
| **Non-deterministic "tool" node** (determinism contract violated) | A node declared deterministic that actually varies output (hidden clock/network/randomness). | The determinism contract (3.1) is the invariant; detection is acceptance-test + C16 discipline territory. > [FAITHFUL-FILL]: v4 asserts reproducibility (README:154) but specifies no runtime determinism check; faithful floor is "contract is declared and tested," enforcement deferred to C16/test strategy. |

> [FAITHFUL-FILL] **G29** is a **minor** gap *owned and resolved by C02* (the wire ABI). C17 addresses G29
> only by *consuming* C02's resolution and adding node-kind + determinism + the uniform by-name reference
> (3.2); it does not re-resolve the bytes and does not introduce a separate workflow-level I/O declaration.
> No other C17-assigned failure mode is deferred.

## 7. Cross-cutting (security / cost / scale / observability / ops)

- **Security.** A C17 tool node inherits C02's subprocess + `work_partition` confinement: deterministic
  steps run as isolated child processes, not in-process plugins, so a misbehaving node cannot corrupt the
  engine. Determinism also means a tool node carries no hidden model-prompt-injection surface (the F51/F33
  reason deterministic boundary typing is the *primary* guard).
- **Cost / scale.** Tool nodes are "cheap and reproducible" (README:154) — **no token cost** (no model
  call). The cost is process-startup overhead (C02's spawn-per-step), accepted because deterministic steps
  are the cheap default. The *economic* argument for C17 is exactly P4: use models only where reasoning is
  required, everything else is a tool node. > [FAITHFUL-FILL] no perf budget stated; not invented here.
- **Observability.** Every tool-node execution is an actor action: it carries `created_by` (C41) and lands
  on the event bus (C23) as a bead (C19/C20). C17 ensures the abstraction surfaces node `name` + status so
  that record is complete — consistent with P9 attribution being native (README:371).
- **Ops / discipline.** C17 is the surface the P4 discipline operates on: the monthly "catches per guard"
  review (F-MODE §100) reads C17 node-kinds. The "unified interface" claim (README:158) is what keeps a
  Python tool node (PyOD/HDBSCAN) and a Go tool node (CXDB bridge) and a CLI tool node (Inspect AI)
  operationally identical from the workflow engine's view.

## 8. Acceptance criteria & test strategy

Sweep-1 high-level criteria (concrete tests at sweep-2):

1. **Uniform placement across languages** — a Go tool node, a Python tool node, and a CLI tool node
   (README:426 / :253–255 / :170) are each placed in a formula by `name` + declared inputs/outputs using
   the *same* node abstraction, with no per-language workflow code.
2. **Deterministic node runs end-to-end via C02** — a deterministic node references a C02 `[[tool]]`,
   receives substituted inputs, executes in its `work_partition`, and its exit code is surfaced as the
   step's status (C02 Reading A floor).
3. **Node-kind distinction is machine-readable** — a deterministic node and a model/agent node are
   distinguishable by the node-kind tag, such that the discipline linter (C16/A36b) can flag an LLM node
   where a tool node would suffice (F52).
4. **Determinism / safe re-run** — re-executing a deterministic node on identical inputs yields identical
   declared outputs and is safe to repeat (the property C18 convergence relies on).
5. **Failure surfaces cleanly** — a tool node that exits nonzero blocks the DAG with a status the
   reconciler can act on, rather than silently advancing.
6. **No new on-disk artifact** — C17 is realized as a view over C12 formula nodes + C02 `[[tool]]` blocks;
   no third file format is introduced (faithful "native" constraint).

## 9. Open questions

(Mirrored into `_meta/review-log.md`.)

1. **[top open question] C17↔C02 ownership of the input/output *declaration*** (3.2 [AMBIGUITY: G29]):
   sweep-1 places wire-bytes in C02 and workflow-level declared-inputs/outputs in C17. Sweep-2 must confirm
   this split against C02's frozen ABI so a node's declared inputs map cleanly onto C02 `args`/stdin and its
   declared outputs onto partition files / stdout — every downstream tool node (C24, C31, C33) depends on it.
2. **Node-kind tag name/shape** — the `kind=deterministic` vs model/agent tag (3.1 fill) must be reconciled
   with C16 (discipline linter) and C12 (formula node schema) so the linter and the formula agree on one
   field.
3. **Runtime determinism enforcement** — v4 asserts reproducibility but specifies no runtime check; is a
   determinism guard (e.g. re-run-and-compare in test, or a sandbox that denies clock/network) in scope for
   v4, or purely a declared-and-reviewed discipline (C16)?
4. **Tool-node retry contract placement** — confirm C17 only surfaces status and C18/C40 own retry, with no
   per-node retry policy at the C17 abstraction (consistent with C02's same fill).
5. **Gas City "tool bead" reality** — like all "Native" cells, the claim that Gas City exposes a unified
   tool-bead interface is unverified (G11 — Gas City unverified); sweep-2 should confirm the native shape
   before freezing C17's mapping onto it.
