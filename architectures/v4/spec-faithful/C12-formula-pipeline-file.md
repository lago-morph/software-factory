# C12 — Formula / Pipeline-File Format  (Spec, Track A)

> Source: README §"Principle 3 — Pipeline-file as process" (lines 126–150; row 132 "Workflow format — The DAG specification — Gas City formulas (TOML) — MIT — Native", line 128 "The workflow is a DAG file, version-controlled, runner-agnostic. The methodology lives in the file, not in agent prompts."), README §Part 1 (lines 29–33, 50–55 "wrong methodology means a new pipeline file"), README Phase 0 (line 369 "P3 … basic via implicit single-step pipeline; full when formulas turn on in Phase 1"), README Phase 1 (lines 382–385 "Turn on `[formulas]`… Define one initial formula (3-step minimum)… `gc formula export <name> --format dot`"), README §509 ("TOML formulas"). AI-CONTEXT §3.1 P3 row (line 68 "Strong when `[formulas]` enabled (TOML DAGs)"), §3.2 concept 7 (line 91 "Formulas + Molecules — Formula = TOML DAG template; Molecule = instantiated bead-tree — P1, P3, P4, P12"), §3.3 vocab (line 101 "formula | pipeline file / workflow DAG template"; line 104 "convoy | batched workflow"; line 109 "order | event-triggered workflow"), §13.2 (lines 548–550 `[formulas]` enables formula DAG composition). one-shot-specs §"Gas Town/Gas City" (line 81 "work primitives are *formulas* and *protomolecules/molecules* — reusable workflow templates (design → plan → implement → review → test chains)"). F-MODE-COVERAGE F26 (line 72 "chain length is a formula property, visible and lintable"), F53 (line 77 "formula checks replace operator-voluntary discipline"). component-inventory C12 row (Maps from A33/A16/A96/B28; Depends on C01, C03; gap G06; foundational yes). component-inventory §3.2 batch placement (C12 foundational, starts Batch 1 once C01/C03 fixed; Batch 2 core build flow). Related specs: `spec-faithful/C01-gas-city-substrate.md` (substrate that runs formulas), `spec-faithful/C03-config-feature-flags.md` (`[formulas]` section-presence flag), `spec-faithful/C17-tool-node-abstraction.md` (deterministic node kind placed in a formula), `spec-faithful/C07-vocabulary-glossary.md` (G06 term ownership).
> Inventory ID: C12   Kind: artifact   Status: sweep-1
> Track: A (faithful)

## 1. Purpose & responsibility

C12 is the **formula** — the v4 **pipeline-file format**: a version-controlled **TOML file describing a
workflow as a DAG** of steps (README:128, :132; AI-CONTEXT §3.2 concept 7 "Formula = TOML DAG template").
It is the artifact that carries **Principle 3 (pipeline-file as process)**: *"The workflow is a DAG file,
version-controlled, runner-agnostic. The methodology lives in the file, not in agent prompts."* (README:128).

C12 is the load-bearing realization of v4's central inversion: **methodology is the variable, substrate is
convergent** (README:29–33). Because the methodology lives in the formula and not in agent prompts, the ten
v3 candidate methodologies "collapse from ten architectural decisions to ten pipeline configurations to run
on the same platform" (README:31), and "wrong methodology means a new pipeline file" rather than a substrate
rewrite (README:51). The formula is therefore the **unit of methodology** — the place a design choice
(design→plan→implement→review→test chain; loop topology; which step is deterministic vs. model-driven;
where the human gates) is expressed declaratively so it can be diffed, linted, visualized, and swapped.

**Responsibilities**
- Define the **formula artifact**: a TOML file declaring a workflow as a **directed acyclic graph** of
  **nodes** (steps) and **edges** (dependencies/ordering), version-controlled and runner-agnostic
  (README:128, :132).
- Be the **single home of methodology**: the chain shape (e.g. design→plan→implement→review→test, the
  Gas City protomolecule pattern, one-shot-specs:81), the loop/branch topology, the human-gate placement,
  and the per-step node kind (deterministic tool node C17 vs. model/agent node) all live *in the formula*,
  not in prompt templates (C09) or agent prompts (README:128; F-MODE F26 "chain length is a formula
  property, visible and lintable").
- Provide the **named-reference surface** other components key on: a node references a prompt template (C09)
  or a tool node (C17) **by name**; a formula is referenced **by name** at dispatch and at instantiation
  (`gc formula export <name>`, README:385; the molecule C13 instantiates "a formula by name").
- Be the **input artifact** to the Workflow Engine tooling that surrounds it: it is what the formula↔DOT
  translator (C14) converts, what the workflow linter (C15) and discipline linter (C16) check, what the
  molecule (C13) instantiates into a live bead-tree, and what the methodology-experiment loop (C55) swaps.
- Be **gated by config**: formulas are **off** until `[formulas]` is present in `city.toml` (C03 section-
  presence flag; README:382, AI-CONTEXT §13.2). At smallest install (Phase 0) there are no formulas — P3 is
  "basic via implicit single-step pipeline" and becomes full when formulas turn on in Phase 1 (README:369).

**Explicitly NOT**
- NOT the **runtime/executor**. The Gas City substrate (C01) and reconciler (C18) *run* a formula; C12 is the
  *file format* they read, not the engine. C12 owns the static artifact; C13 owns the running instance.
- NOT the **molecule** (C13). A formula is the **template**; a molecule is "a formula instantiated into a live
  bead-tree for a specific run" (inventory C13; AI-CONTEXT §3.2 "Molecule = instantiated bead-tree"). C12 has
  no per-run state.
- NOT a **prompt template** (C09). A model/agent node *references* a prompt template by name; the prompt text
  lives in C09's Go `text/template` markdown (AI-CONTEXT §3.2 concept 5). The methodology (which steps, in
  what order, with what gates) is C12's; the per-step instruction text is C09's.
- NOT the **tool-node abstraction** (C17) or the **tool ABI** (C02). A deterministic node *references* a C17
  tool node by name; C12 places it in the DAG but does not define the tool's wire protocol.
- NOT the **DOT format / visualizer / linters** (C14/C15/C16). Those *operate on* a formula; C12 is the
  source artifact, not the translator or the rule sets.
- NOT the **dispatch** mechanism (C05/sling). Sling routes a node's work to an agent/pool; C12 declares *what*
  the node is, not *which* worker executes it at runtime.
- NOT a **convoy** (batched workflow) or **order** (event-triggered workflow) as distinct artifacts. v4 names
  these as Gas City vocabulary (AI-CONTEXT §3.3); a convoy is a batching of formulas and an order is an
  event-trigger over workflows (C40). C12 owns the single-formula DAG format; batching/eventing are separate
  concerns. > [FAITHFUL-FILL] — see §3.

## 2. Context & dependencies

| Direction | Component | Relationship |
|---|---|---|
| Upstream (runtime) | **C01** Gas City substrate | C01 is the DOT-shaped TOML workflow runner that *reads and executes* formulas (README:121 "Pipeline engine — DOT-shaped workflow runner — Gas City"; inventory C01 "DOT-shaped TOML workflow runner"). C12 is the format C01 natively consumes. |
| Upstream (gating) | **C03** layered config / feature-flags | `[formulas]` section presence in `city.toml` enables formula DAG composition (README:382; AI-CONTEXT §13.2; C03 §"section presence = capability"). Below that flag, no formula is active. |
| Upstream (terms) | **C07** vocabulary-glossary | Canonical meaning of *formula*, *molecule*, *node*, *DAG*, *convoy*, *order*, *wisp* (G06 — see §3 ambiguity). |
| Downstream (instantiates) | **C13** molecule | A molecule is this formula instantiated into a live bead-tree for one run (inventory C13 depends on C12). |
| Downstream (converts) | **C14** formula↔DOT translator + visualizer | Bidirectional TOML-formula ↔ DOT conversion for graphviz render + DOT-ecosystem lint (README:133–135, :384–385; inventory C14 depends on C12). |
| Downstream (lints structure) | **C15** workflow linter (Mammoth 21-rule) | Structural rules over the DAG, run against the formula (via DOT, README:134; inventory C15 depends on C14). |
| Downstream (lints discipline) | **C16** discipline linter | Flags LLM nodes where a deterministic tool node would suffice — keys on the per-node *kind* C12 records (README:160; inventory C16 depends on C12). |
| Downstream (places nodes) | **C17** tool-node abstraction, **C09** prompt template | A formula node references a C17 deterministic tool node **or** a C09 prompt template by name. |
| Downstream (swaps) | **C55** methodology-as-config experiment loop | v3's candidate methodologies run "as swappable pipeline files"; empirical results select methodology per work type (inventory C55 depends on C12). |
| Downstream (gate) | **C50** promotion gate | A promotion gate is itself "a Gas City formula with a statistical gate" (README:276; inventory C50 depends on C12). |

C12 is **foundational** (inventory: yes). It can start authoring in **Batch 1** "once C01/C03 shape is
fixed" and lands fully in **Batch 2** as part of the core build flow (inventory §"Suggested build/spec
batches"). Its single hardest external unknown is that the formula *schema is Gas City's*, not invented by
v4 (G11 — Gas City unverified; see §9).

## 3. Interfaces / contracts

Sweep 1 — interfaces **named and described**; concrete TOML schema / field signatures deferred to sweep 2.

### 3.1 The formula artifact (named structure)

A formula is a TOML file whose named elements are (sweep-1 descriptions; exact key names are Gas City's and
are confirmed at sweep 2 against the real `gc` formula schema — see §9 / G11):

| Element | Description | Source / fill |
|---|---|---|
| Formula identity (`name`) | The name a formula is referenced by — at `gc formula export <name>`, at dispatch, and at molecule instantiation. | README:385 |
| Node set | The DAG's steps. Each node has an identity, a **kind** (deterministic tool node C17 vs. model/agent node), and a binding (a C17 tool-node name or a C09 prompt-template name). | README:128, :132; AI-CONTEXT §3.2 concept 7; C17 §3.1 |
| Edge set / ordering | The directed dependencies between nodes that make the workflow a **DAG** (acyclicity is the defining property; cycles are expressed as bounded loop constructs, not raw back-edges — see invariants). | README:128 ("DAG file"); F26 |
| Node kind tag | Per-node marker distinguishing a deterministic tool node from a model/agent node; the field C16's discipline linter (F52) and the C17 abstraction key on. | C17 §3.1 [FAITHFUL-FILL]; README:160 |
| Gate / wait nodes | Synchronization / human-approval gates expressed as nodes (Gas City `wait` = "gating / synchronization primitive", AI-CONTEXT §3.3). The human-gate placement is a methodology property living in the formula. | AI-CONTEXT §3.3; one-shot-specs:65 (human-gate pipeline) |
| Parameters / placeholders | Run-time inputs a formula declares (e.g. `$epic_id`, `$rfc_path` in the exemplar pipelines, one-shot-specs:62–63) that a molecule binds at instantiation. | one-shot-specs:62–63 > [FAITHFUL-FILL] |

> [FAITHFUL-FILL] **Parameters/placeholders as a formula element.** v4 does not enumerate formula fields, but
> the exemplar pipeline files it cites (`"Implement epic $epic_id"`, `"Break $rfc_path into an epic"`,
> one-shot-specs:62–63) are parameterized templates, and a molecule must bind *something* per run. The
> minimal faithful fill is "a formula declares named parameters that the molecule binds at instantiation,"
> because instantiation (C13) is meaningless if a template carries no slots. The concrete binding syntax is
> deferred to C13 + sweep 2 (it is Gas City's, not invented here).

> [FAITHFUL-FILL] **Loop topology under acyclicity.** v4 names the artifact a **DAG** (README:128) yet the
> exemplar formulas it cites include Ralph-loop "one issue at a time" pipelines (one-shot-specs:62) and v4
> leans on closed-loop self-healing. The minimal faithful reconciliation is: a formula is a DAG of *step
> types*, and iteration is a **bounded loop construct** (a node that re-enters under a gate/condition), not a
> raw graph cycle — preserving the "DAG file" claim while admitting the loop methodologies v4 explicitly
> runs. The exact loop primitive is Gas City's; C12 only requires that iteration be a declared, bounded,
> lintable construct (so F26 "chain length is a formula property, visible and lintable" holds).

### 3.2 Inbound: who produces / authors a formula

- **A human/methodology author** writes a formula directly (Phase 1 "Define one initial formula", README:383),
  or transfuses one from an exemplar protomolecule (one-shot-specs:81 "design → plan → implement → review →
  test chains").
- **C55** (methodology-experiment loop) supplies *alternative* formulas — the v3 candidates as swappable
  pipeline files — selected empirically per work type.
- **The factory itself** (C52 self-bootstrap) may author a formula for its own next component; C12 is just the
  format such authored workflows take.

### 3.3 Outbound: what C12 guarantees to consumers

- To **C01/C18** (runtime): a TOML DAG that the DOT-shaped workflow runner can read and execute node-by-node,
  with acyclicity guaranteeing a topological execution order.
- To **C13** (molecule): a named, parameterized template that can be instantiated into a bead-tree, with every
  node resolvable to a concrete binding (C17 tool node or C09 template) and every parameter declared.
- To **C14** (translator): a structure with a well-defined node/edge model so a *lossless* round-trip to DOT
  is at least *possible* in principle (round-trip fidelity is C14's burden — G24 — not C12's, but C12 must
  expose a node/edge model clean enough to make it tractable).
- To **C15/C16** (linters): a machine-readable structure whose nodes carry a **kind** and whose edges/loops
  carry a visible topology, so structural rules (F26 chain length, cycle bounds) and discipline rules
  (LLM-where-tool, F52) are checkable on the file alone.

> [AMBIGUITY: G06] **Are "formula", "convoy", and "order" three artifacts C12 must define, or one?**
> **Reading A** — C12 owns *only* the single-formula DAG; convoy (batched workflow) and order (event-triggered
> workflow) are separate artifacts/components (order → C40 durable Orders; convoy → an unassigned batching
> concept). **Reading B** — C12 is the umbrella "pipeline-file format" and must define all three TOML shapes.
> **Pick Reading A.** The inventory gives C12 the one-line "TOML DAG describing the workflow" and assigns
> **orders** to a distinct component (C40 "Durable workflow engine (Orders)"); the vocabulary table
> (AI-CONTEXT §3.3) lists *convoy*, *order*, and *formula* as **distinct** terms with distinct generic
> equivalents. The faithful, minimal-scope reading is therefore: C12 = the single formula DAG format; a
> convoy is a *batching of* formulas and an order is an *event-trigger over* a formula, both layered on C12
> but owned elsewhere. C12's job under G06 is to pin the meaning of **formula / node / edge / DAG** (deferring
> the full glossary to C07); it explicitly does *not* expand to own convoy/order artifacts.

## 4. Data model / state

C12 is an **artifact** (a file format), not a data store; it owns the *static template shape*, not live state.

- **Owned artifact:** the formula TOML file, version-controlled in the workspace/pack (README:128
  "version-controlled"; methodologies are distributed *in packs*, AI-CONTEXT §3.3 "pack = distributable
  methodology bundle", so formulas ship inside packs C02 and/or live in the city repo).
- **No per-run state.** All instance state — which nodes have run, their bead status, retries, the bead-tree —
  belongs to **C13** (molecule) and the bead store **C19/C20**. C12 is immutable input to a run.
- **Lifecycle:** authored → (linted C15/C16, visualized C14) → enabled by `[formulas]` (C03) → instantiated
  into a molecule (C13) per run → swapped/promoted as methodology evidence accrues (C55/C50). The formula
  file itself changes only by version-controlled edit (a new pipeline file, README:51), never by a run.
- **Identity & attribution:** a formula is referenced by `name`; authorship of a formula edit is an actor
  action carried via C41 (`created_by`) like any other artifact change. > [FAITHFUL-FILL] (consistency with
  P9 native attribution; C12 introduces no new identity concept).
- **Consistency requirement:** the **acyclicity invariant** (DAG) and **node-binding resolvability** (every
  node resolves to a C17 tool node or C09 template; every parameter is declared) are the static invariants a
  formula must satisfy before it is runnable — enforced by C15 (structure) and the linters, not by C12 at
  runtime.

## 5. Behavior

C12 is a passive artifact; "behavior" is the lifecycle in which it participates (sweep-1 narrative; sequence
diagram deferred to sweep 2):

1. **Author / transfuse** a formula TOML (a DAG of nodes + edges; nodes bound to C17 tool nodes or C09
   templates; parameters declared) — Phase 1 "define one initial formula, 3-step minimum to validate"
   (README:383).
2. **Lint & visualize**: C14 exports the formula to DOT (`gc formula export <name> --format dot`, README:385)
   for graphviz; C15 runs Mammoth-style structural rules; C16 flags LLM-where-tool nodes. All operate on the
   file before it ever runs.
3. **Enable**: `[formulas]` present in `city.toml` (C03) turns formula DAG composition on (Phase 1).
4. **Instantiate**: at dispatch, the formula is referenced by name and **C13** instantiates it into a live
   bead-tree (molecule) for a specific run, binding declared parameters.
5. **Execute**: C01's DOT-shaped runner + the reconciler (C18) walk the DAG in topological order; each node's
   work is dispatched (C05) to an agent (model node) or executed as a tool node (C17); bounded loop nodes
   re-enter under their gate.
6. **Evolve**: methodology evidence (C55/C46) drives swapping one formula for another (a new pipeline file,
   README:51) or promoting a variant (C50); the change is a version-controlled file edit, not a runtime
   mutation.

The defining behavioral property: **methodology change = formula edit**. Because the chain, gates, loop
bounds, and node kinds are all *in the file*, changing how work is done is a diffable file change that the
linters and visualizer can review before it runs (README:51; F26; F53 "formula checks replace operator-
voluntary discipline").

## 6. Failure modes & handling

| F-mode | Relevance to C12 | Handling (faithful) |
|---|---|---|
| **F26** Telephone / sustained inter-agent chain | An over-long agent→agent handoff chain degrades like a game of telephone. | v4's answer is *exactly* C12: "Pipeline-file (P3) controls handoff patterns; chain length is a **formula property, visible and lintable**" (F-MODE:72). C12 makes chain length a structural property of the file so C15 can lint it. (Addressed by being the formula.) |
| **F53** Voluntary-discipline fragility | Methodology enforced by operator goodwill erodes. | "Substrate-triggered structural controls (… formula checks) replace operator-voluntary discipline" (F-MODE:77). Because methodology lives in the formula (not prompts), it is structurally checkable, not voluntary. |
| **F52** Tempting-wrong-hybrid (deterministic-without-purpose) | Nodes/guards added with no falsifying scenario. | C12 records the per-node **kind** (3.1) so C16's discipline linter can enforce "no LLM node where a tool node suffices; every guard points at a scenario" (F-MODE:100). C12 *exposes* the kind; the policy is C16's. |
| **Malformed / cyclic formula** | A formula with a raw cycle, unresolved node binding, or undeclared parameter. | Detection is C15 (structure) + C16 (discipline) + instantiation-time binding-resolution (C13), not a C12 runtime check. C12's contribution is to define the **acyclicity + binding-resolvability invariants** (4) the linters check against. > [FAITHFUL-FILL]: v4 names a linter (C15) but no in-format validator; the faithful floor is "C12 defines the invariants; C15/C16/C13 enforce them." |
| **Methodology-in-prompt leakage** | Author puts workflow logic in agent prompts (C09) instead of the formula. | The P3 invariant — "methodology lives in the file, not in agent prompts" (README:128) — is the guard; it is a *discipline* surfaced by review/lint, not a mechanical C12 check. > [FAITHFUL-FILL]: no automated detector specified in v4; deferred to C16/C10 review discipline. |

> [FAITHFUL-FILL] **G06 (undefined terms)** is C12's only assigned gap; it is addressed in §3.3 [AMBIGUITY:
> G06] by pinning *formula / node / edge / DAG* and scoping out convoy/order, and by deferring the broader
> glossary to **C07** (which owns G06 system-wide). No C12-assigned failure mode is deferred unaddressed.

## 7. Cross-cutting (security / cost / scale / observability / ops)

- **Security.** A formula is declarative data, not code; it carries no execution privilege of its own. Its node
  *bindings* inherit the security posture of what they bind to (C17 tool-node subprocess confinement; C09
  prompt + model node). The risk a formula introduces is *topological* (an unbounded loop, an over-long chain)
  — bounded by the DAG/loop-bound invariants (4) and the linters (C15). C12 adds no new trust surface.
- **Cost / scale.** The formula is the *lever* on cost: by placing deterministic tool nodes (C17, no token
  cost) where models aren't needed, the formula directly governs token spend (P4 economics). Chain length and
  loop bounds — formula properties — set the per-run cost ceiling. v4 gives no per-formula budget field;
  > [FAITHFUL-FILL] none invented here (cost modeling is C46/G32 territory).
- **Observability.** A formula is the *template* whose every instantiated node becomes an attributed bead
  (C19/C20) on the event bus (C23) carrying `created_by` (C41). The formula→molecule→bead-tree mapping is what
  lets a run be replayed and judged against the formula it came from.
- **Ops / version control.** Formulas are version-controlled (README:128) and ship in packs (C02) as the
  "distributable methodology bundle" (AI-CONTEXT §3.3). A methodology change is a reviewed, diffable,
  lintable, visualizable file edit — the operational property that makes "methodology is the variable"
  practical (README:51).

## 8. Acceptance criteria & test strategy

Sweep-1 high-level criteria (concrete tests at sweep 2):

1. **A formula is a valid TOML DAG** — a 3-step formula (README:383 "3-step minimum to validate") parses,
   declares nodes + edges, and is acyclic; the runner (C01) executes its nodes in a topological order.
2. **Methodology lives in the file** — the chain shape, gate placement, and per-node kind are read from the
   formula, with no workflow logic required in agent prompts (README:128); swapping methodology is a formula
   edit, not a prompt or substrate change (README:51).
3. **Nodes resolve by name** — every node binds to a C17 tool node or a C09 prompt template by name, and every
   declared parameter is bindable by a molecule (C13) at instantiation.
4. **Node kind is machine-readable** — deterministic vs. model/agent nodes are distinguishable so C16 can flag
   LLM-where-tool (F52) and C15 can count chain length (F26) from the file alone.
5. **Round-trippable to DOT (tractably)** — the node/edge model is clean enough that `gc formula export <name>
   --format dot` (README:385) and C14's reverse path are possible; *fidelity proof* is C14's acceptance
   criterion (G24), but C12 must not introduce constructs that have no DOT representation.
6. **Gated by config** — with `[formulas]` absent (Phase 0), no formula is active (implicit single-step
   pipeline, README:369); with it present (Phase 1), formulas compose (AI-CONTEXT §13.2).
7. **Loop bounded & lintable** — an iterative formula (Ralph-loop, one-shot-specs:62) expresses iteration as a
   bounded, declared loop construct, not a raw cycle, so chain/loop bounds are lintable (F26).

## 9. Open questions

(Mirrored into `_meta/review-log.md`.)

1. **[top open question] Real Gas City formula schema (G11).** C12's entire field model (node/edge/kind/loop/
   parameter key names, the exact TOML shape) is **Gas City's**, asserted "Native" but unverified — no author
   has run `gc` (G11). Sweep 2 must freeze the concrete schema against the actual `gc formula` format before
   any dependent (C13 instantiation, C14 translation, C15 rules) can bind to it. This is the single gating
   uncertainty for the whole Workflow Engine subsystem.
2. **Loop primitive vs. pure DAG** (3.1 [FAITHFUL-FILL]) — confirm how Gas City expresses bounded iteration
   within a "DAG file" so the acyclicity claim and the loop methodologies (Ralph, self-healing re-entry)
   coexist; this drives C15's cycle/loop rules and C14's DOT mapping.
3. **Convoy/order boundary** (3.3 [AMBIGUITY: G06]) — confirm with C40 (Orders) and C07 that C12 owns only the
   single-formula DAG and that batching (convoy) / event-triggering (order) are layered elsewhere.
4. **Node-kind field reconciliation** — the per-node `kind` tag must be the *same* field C17 (§3.1 fill) and
   C16 key on; sweep 2 must reconcile its name/shape across C12/C16/C17 so there is one field, not three.
5. **Parameter-binding syntax** (3.1 [FAITHFUL-FILL]) — the formula↔molecule parameter contract (`$epic_id`-
   style slots) must be pinned jointly with C13 so instantiation has a defined binding rule.
