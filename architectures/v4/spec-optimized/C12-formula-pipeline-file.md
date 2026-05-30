# C12 — Formula / pipeline-file format  (Spec, Track B)

> Source: README Part 4 "Principle 3 — Pipeline-file as process" (:126–151), README Phase 0/1 (:364, :369, :382–385); AI-CONTEXT §2 (table: pipeline-file-as-process), §3.1 (P3 "Strong when `[formulas]` enabled (TOML DAGs)"), §3.2 concept 7 ("Formula = TOML DAG template; Molecule = instantiated bead-tree"), §3.3 (vocabulary table), §3.4/§13.2 (`[formulas]` flag), §11.2 (GF-M first); _meta inventory C12 row; _meta gaps G06 (undefined terms — primary), G24, G05; F-MODE-COVERAGE references to P3.
> Inventory ID: C12   Kind: artifact   Status: sweep-1
> Deltas: DELTA-01 (formula = versioned schema, not folklore TOML), DELTA-02 (explicit node taxonomy: agent / tool / gate / sub-formula), DELTA-03 (parameter + binding contract for spec→formula→template), DELTA-04 (methodology-as-data: named, versioned, swappable formula identity for C55), DELTA-05 (DAG well-formedness invariants owned here, surfaced to C15/C16), DELTA-06 (formula provenance + transfusion lineage fields), DELTA-07 (DOT round-trip canonical-form requirement pushed into the format itself, de-risking G24/C14).

## 1. Purpose & responsibility

C12 is **the workflow definition format**: a version-controlled TOML file (a Gas City *formula*) that describes a build/eval/heal workflow as a **directed acyclic graph of typed nodes**. It is the load-bearing realization of Principle 3 ("the methodology lives in the file, not in agent prompts," README:128). C12 owns:

- The **formula schema** (DELTA-01): the typed grammar of a formula file — its header/identity block, node table, edge/dependency declarations, parameters, and gates — as a stable, versioned artifact rather than whatever TOML Gas City happens to parse.
- The **node taxonomy** (DELTA-02): the closed set of node kinds a formula may contain — `agent` (an LLM step bound to a prompt template, C09), `tool` (a deterministic tool-node, C17), `gate` (a convergence/approval/wait condition, feeding C18), and `sub_formula` (composition of another formula). Each kind names which other component executes it.
- The **parameter + binding contract** (DELTA-03): how a formula declares inputs (e.g. `spec_ref`, `epic_id`, `rfc_path`) and binds them to the spec artifact (C08) and to prompt templates (C09) at instantiation time, so the *same* formula runs against different specs.
- The **methodology identity** (DELTA-04): a formula carries `{name, version, methodology_id}` so that v3's ten candidate methodologies are *named, versioned, swappable data* — the substrate of C55's methodology-as-config experiment loop.
- The **DAG well-formedness invariants** (DELTA-05): acyclicity, single-entry reachability, typed-edge legality, no dangling node refs — defined *here* as the canonical structural truth, then enforced by the linters (C15 structural, C16 discipline) and surfaced by C14's translator.

This component is the **place methodology is written down**. Everything downstream that "runs a workflow" (C13 molecule, C18 reconciler, C55 experiment loop, C50 promotion gate) consumes a C12 formula.

What it is **NOT**:
- **Not the runtime state.** A formula is a *template/class*; the live instantiated bead-tree for one run is C13 (molecule). C12 is inert data; C13 is the running instance. (AI-CONTEXT §3.2 concept 7.)
- **Not the executor.** C12 does not run nodes. `agent` nodes are executed by C28 via C05 dispatch; `tool` nodes by C17; `gate` nodes evaluated by C18. C12 only *declares* what runs and in what dependency order.
- **Not the prompt.** The methodology (sequence, gates, branching) lives in C12; the per-step *instruction text* lives in C09 templates that C12 nodes reference by name. This split is the whole point of P3 — keep the process out of the prompt.
- **Not the linter.** Structural rules (C15) and LLM-where-tool discipline (C16) are separate components; C12 owns the *invariants*, not the rule engines that check them.
- **Not the DOT format.** DOT is C14's interop concern. C12 defines a canonical form that makes round-tripping *possible* (DELTA-07), but the bidirectional translator and graphviz export are C14.
- **Not the feature flag.** `[formulas]` in `city.toml` (C03) *turns this capability on*; the flag is C03, the files it enables are C12.

## 2. Context & dependencies

- **Depends on:**
  - **C01** (Gas City substrate) — provides the formula runner and the TOML reader; C12 specifies the schema that runner must honor. Per AI-CONTEXT §3.2 concept 7, formulas are a native Gas City primitive.
  - **C03** (config/feature-flags) — `[formulas]` section presence gates C12 (README:382, AI-CONTEXT §13.2). Without the flag, the smallest install runs an implicit single-step pipeline only (README:369).
- **Consumed by (fan-out):**
  - **C13** (molecule) — instantiates a formula into a live bead-tree.
  - **C14** (formula↔DOT translator) — reads formulas to emit DOT for visualization/lint; round-trips DOT back to formula.
  - **C15** (workflow linter) — structural rules over the DAG.
  - **C16** (discipline linter) — flags `agent` nodes that should be `tool` nodes.
  - **C18** (reconciler) — evaluates `gate` nodes for convergence.
  - **C09** (prompt-template binding) — `agent` nodes reference templates by name; C12 defines the reference contract.
  - **C17** (tool-node abstraction) — `tool` nodes reference tool-node identifiers; C12 defines the reference contract.
  - **C50** (promotion gate), **C55** (methodology-experiment loop) — treat formulas as swappable, versioned, comparable units.
- **Sits at:** the head of the Workflow Engine subsystem; foundational (Batch 1/2 — can start once C01/C03 shape is fixed, per inventory build-batch notes).

## 3. Interfaces / contracts

Named-and-described (sweep 1; concrete TOML schema + signatures in sweep 2).

**Inbound (what the format must accept / what produces formulas)**
- **`FormulaFile`** — the on-disk TOML artifact. Authored by humans (Phase 1+), by the spec→beads breakdown (one-shot-specs `spec-to-beads` pattern), or by C52 self-bootstrap. Carries: identity header, parameter declarations, node table, edge declarations, gate declarations.
- **`FormulaParameters`** — the named inputs a caller supplies at instantiation (`spec_ref`, `epic_id`, `rfc_path`, etc.), satisfying the formula's declared parameter contract (DELTA-03).
- **`DOTGraph` (via C14)** — a DOT graph round-tripped *back* into formula form; must land in C12's canonical form (DELTA-07).

**Outbound (what C12 exposes to consumers)**
- **`ParsedFormula`** — the validated, in-memory graph object: typed nodes, edges, parameters, gates, identity. The single representation every consumer (C13/C14/C15/C16/C18) reads; nobody re-parses raw TOML. Carries the well-formedness guarantees of §3-invariants.
- **`FormulaIdentity`** — `{name, version, methodology_id, transfused_from?}` (DELTA-04/06): the stable handle by which C55 selects a methodology, C50 promotes a variant, and C51 records gene-transfusion lineage.
- **`NodeBinding` contract** — per node, the resolved reference to its executor: an `agent` node → `{template_ref (C09), role/rig hint (C05/C42)}`; a `tool` node → `{tool_node_id (C17), io schema ref}`; a `gate` node → `{gate_kind, predicate, bound (C18)}`; a `sub_formula` node → `{formula_ref, param mapping}`.
- **`CanonicalForm`** — a deterministic serialization (node ordering, edge ordering, key ordering) that makes formula→DOT→formula and formula→formula identity-comparison stable (DELTA-07, de-risks G24).

**Invariants** (DELTA-05 — C12 is the canonical owner; C15/C16 enforce):
- **Acyclic:** the node/edge set forms a DAG. A cycle is a malformed formula (typed `FormulaCycle` error), never accepted.
- **Single logical entry, reachable:** every node is reachable from the entry set; no orphan nodes.
- **No dangling refs:** every edge endpoint, every `template_ref`, `tool_node_id`, and `sub_formula` ref resolves; `sub_formula` composition is itself acyclic (no formula includes itself transitively).
- **Closed node taxonomy:** every node has exactly one kind from `{agent, tool, gate, sub_formula}` (DELTA-02); an unknown kind is a parse error.
- **Determinism:** the same `FormulaFile` parses to a byte-stable `CanonicalForm` (precondition for DELTA-07 round-trip and for C50/C55 identity comparison).
- **Parameter totality:** instantiation fails closed if a declared required parameter is unbound (DELTA-03) — no formula runs half-bound.

## 4. Data model / state

C12 is **stateless at runtime** — a formula is inert, version-controlled data. The owned "state" is the *schema definition* and the parsed in-memory object; live run-state belongs to C13.

A formula file's logical structure (sweep-2 pins exact TOML keys):

| Block | Contents | Notes |
|---|---|---|
| **Identity** | `name`, `version`, `methodology_id`, optional `transfused_from`, `description` | DELTA-04/06. Drives C55 selection, C50 promotion, C51 lineage. |
| **Parameters** | declared inputs: `{name, type, required, default?}` | DELTA-03. Bound at instantiation by C13. |
| **Nodes** | array-of-tables; each `{id, kind, ref, ...kind-specific}` | DELTA-02 taxonomy. `ref` resolves to C09/C17/C18 target. |
| **Edges** | dependency declarations `{from, to, condition?}` | The DAG. `condition` enables branching gates. |
| **Gates** | `{node_id, gate_kind, predicate, bound}` | Convergence/approval/wait; consumed by C18. `bound` is the loop-bound (ties to G18 termination at the workflow level). |

- **Versioning:** formulas are version-controlled files (git) and carry an internal `version`. A methodology is the `{name, methodology_id}` pair; its `version`s are an evolution lineage (DELTA-04). This is what lets C55 run "the same methodology, two variants" and C50 promote one.
- **Canonical form:** derived, deterministic serialization used for diffing, DOT round-trip, and identity hashing. Not separately persisted; recomputed.
- **Provenance:** `transfused_from` (DELTA-06) records the external exemplar a formula was derived from (Kilroy/Attractor `.dot` pipelines per one-shot-specs §research), feeding C51's gene-transfusion discipline.

## 5. Behavior

Three flows (sweep-2 adds Mermaid):

1. **Author/load:** a `FormulaFile` is read by the Gas City runner (C01) under the `[formulas]` flag (C03). C12 parses → validates well-formedness invariants (§3) → produces `ParsedFormula`. Malformed formulas fail closed at load with typed diagnostics; they are never instantiated.
2. **Bind/instantiate (hand-off to C13):** a caller supplies `FormulaParameters`; C12's binding contract resolves each node's executor reference (`NodeBinding`) and checks parameter totality. The bound, parameterized graph is handed to C13, which instantiates it into a live bead-tree (molecule). C12's responsibility ends at "validated, fully-bound graph"; C13 owns the running instance.
3. **Round-trip (with C14):** C12 emits `CanonicalForm`; C14 maps it to DOT for graphviz (C-visualizer) and Mammoth-style linting (C15). DOT edited externally round-trips back through C14 into C12's canonical form — DELTA-07 requires the format expose enough structure (and accept enough) that this is lossless for the supported node/edge/gate vocabulary.

The methodology *itself* is expressed entirely in flows 1–2: the choice of nodes, their order, the gates, the branching. Swapping methodology = swapping the formula file (AI-CONTEXT §2 "rewrites pipeline file" risk-on-misfit = Low).

## 6. Failure modes & handling

- **G06 (undefined load-bearing vocabulary)** — *primary gap for C12.* "Formula", "molecule", "pipeline file", "DAG", "node", "gate", "sub-formula" are used load-bearing across the corpus with the definition split between README and AI-CONTEXT (G06). **Mitigation:** C12 *is* the authoritative definition of "formula" and its sub-vocabulary (node taxonomy DELTA-02, identity DELTA-04, the formula/molecule split). C12's §1/§3 are the canonical text the glossary (C07) links to; the formula↔molecule distinction (template vs instance) is pinned here, resolving the most-confused pair. Residual: the *rest* of the Gas City vocabulary (rig/sling/convoy/wisp) is owned by C07, not C12.
- **Malformed-DAG acceptance (structural)** — a cyclic or orphan-node formula reaching execution would hang or silently drop work. **Mitigation:** acyclicity + reachability + no-dangling-ref invariants are owned here (DELTA-05), enforced by C15, and fail-closed at load. A formula that fails well-formedness is never handed to C13.
- **LLM-where-tool-suffices (discipline)** — an `agent` node doing deterministic work that a `tool` node should (a P3/cost failure). **Mitigation:** the closed node taxonomy (DELTA-02) makes "is this node an LLM or a tool?" a *typed, machine-checkable* property, which is precisely what gives C16 a falsifiable surface to flag against. C12 doesn't decide policy; it makes the policy checkable.
- **DOT round-trip loss (G24)** — README asserts a "few hundred LOC" bidirectional translator across two formats of unequal expressive power; round-trip fidelity unaddressed. **Mitigation (DELTA-07):** C12 defines a `CanonicalForm` and constrains the formula vocabulary so the *supported subset* round-trips losslessly; anything DOT can express that C12 cannot is explicitly out-of-format (rejected on import) rather than silently dropped. This converts G24 from "prove lossless across unequal formats" to "prove lossless across a defined, intersected vocabulary." Hard residual stays in C14's spec.
- **Half-bound instantiation** — a formula run with a missing required parameter. **Mitigation:** parameter totality invariant (DELTA-03) — fail closed at bind time.
- **Methodology drift / unattributed swap** — a methodology silently changed mid-experiment would corrupt C55/C50 comparisons. **Mitigation:** `{name, version, methodology_id}` identity (DELTA-04) + git versioning make every methodology change an attributable, diffable event.

## 7. Cross-cutting (security / cost / scale / observability / ops)

- **Security:** formulas are *code-shaped config* that drive agent action; a malicious `sub_formula` ref or `tool_node_id` is a supply-chain surface. C12 requires every ref resolve within the declared pack/capability set (C02/C03); cross-formula composition is acyclic and explicit. Authoring/promoting a formula is an attributed action (C41) — relevant when C52 self-bootstrap *generates* formulas.
- **Cost:** the node taxonomy is the lever for P3's cost story — making `tool` vs `agent` a first-class, lintable distinction (DELTA-02/C16) is what lets the factory push deterministic work off the (token-metered, rate-limited) agent path. The methodology-as-data identity (DELTA-04) is the unit C46 keys cost-per-satisfaction against.
- **Scale:** formulas are small static files; no scale concern in C12 itself. The `bound` field on gates (DELTA-05) is where workflow-level loop bounds live, feeding the G18 termination story at C18/C39.
- **Observability:** `FormulaIdentity` + `CanonicalForm` hash make "which methodology, which version produced this trajectory" answerable — the join key between the workflow definition and the CXDB trajectories (C21) / satisfaction metric (C33).
- **Ops:** version-controlled, diffable, lintable-before-run. A bad methodology is a reverted commit, not a substrate rebuild (the core v4 thesis).

## 8. Acceptance criteria & test strategy

1. **Schema stability (DELTA-01):** a corpus of valid formulas parses to `ParsedFormula`; a versioned schema doc exists and a schema-version bump is a deliberate, documented event (golden formulas).
2. **Node taxonomy closure (DELTA-02):** every node resolves to exactly one of `{agent, tool, gate, sub_formula}`; an unknown kind fails parse; each kind's `ref` resolves to the correct component's identifier space (C09/C17/C18/C12).
3. **Well-formedness (DELTA-05):** cyclic, orphan-node, dangling-ref, and self-including-`sub_formula` formulas each fail closed at load with the typed diagnostic; valid DAGs pass. (Shared fixtures with C15.)
4. **Binding totality (DELTA-03):** instantiation with all required params succeeds; a missing required param fails closed before any node executes; defaults apply when declared.
5. **Methodology identity (DELTA-04):** two formulas sharing `methodology_id` but differing `version` are recognized as variants of one methodology (C55/C50 fixture); identity is stable across reformatting (canonical-form hash).
6. **DOT round-trip (DELTA-07, with C14):** for the supported vocabulary, formula→DOT→formula yields byte-identical `CanonicalForm`; a DOT construct outside the vocabulary is rejected on import, never silently dropped.
7. **3-step minimum validates (README:383):** the Phase-1 "3-step minimum" formula (e.g. design→implement→review) parses, binds, and hands a well-formed bound graph to C13.
8. **Vocabulary authority (G06):** C07 glossary entries for formula/molecule/node link to C12 as the definition source; the template-vs-instance distinction is testable as a documented contract.

## 9. Open questions

- **OQ1 (→ review-log):** **What exactly is Gas City's native formula TOML schema, and how much of DELTA-01/02 is *describing* it vs *constraining* it?** G11 flags that no author has verified Gas City's behavior. If Gas City's formula grammar already fixes a node model, C12's taxonomy must conform-or-fork (touches C01). *Top open question* — the whole format spec is downstream of confirming the real Gas City formula schema.
- **OQ2:** Is `gate`/branching expressive power (conditional edges, loops-with-bound) within native Gas City formulas, or does it require the C18 reconciler + a pack extension? Affects whether methodology branching (needed by several v3 candidates) is in-format or in-runtime.
- **OQ3:** Does `sub_formula` composition exist natively, or is methodology composition flattened at author time? Determines whether C55 can compose methodologies or only swap whole files.
- **OQ4:** Where is the formula↔DOT vocabulary intersection drawn (DELTA-07) — i.e., which DOT/Attractor constructs (from the Kilroy/Attractor `.dot` exemplars) are *in* the supported round-trip set? This is the concrete contract C14 builds against and should be co-specified with C14.
