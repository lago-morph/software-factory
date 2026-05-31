# C14 — Formula↔DOT Translator + Visualizer  (Spec, canonical track)

> Source: README §"Principle 3 — Pipeline-file as process" (lines 126–150; row 133 "Workflow visualizer — Render the DAG for review — Custom: formula → DOT exporter + graphviz — n/a (your work; small) — Gas City pack"; row 135 "Workflow translator (bidirectional) — DOT ↔ formula for interop with DOT-based tools — Custom (~few hundred LOC Go)"; line 150 "the translator gives you visualization + lint compatibility with the DOT-graph ecosystem"; the Mermaid `F<-->T<-->D-->{L,G}` diagram lines 137–148). README §Part 6 Phase 1 (line 384 "Build the formula↔DOT bidirectional translator as a small Go tool … few hundred lines"; line 385 "Add `gc formula export <name> --format dot` for graphviz rendering"; line 392 "P3 … full, including visualization and (optionally) Mammoth-derived 21-rule linter"). README §Part 8 (line 538 "Start the formula↔DOT translator as a small Go side project … the bidirectional capability is what enables Mammoth-compatible linting"). README §Part 5 (line 301 "Mammoth … DOT linter is the strongest transfusion target"). AI-CONTEXT §10.1 decision table (line 469 "Formula↔DOT bidirectional translator | Yes, Phase 1 | Resolves Gas City vs Attractor-shape impedance; enables Mammoth-style linting"), §12 (line 509 "Mammoth's exact 21 DOT linter rules: should be documented and ported to formulas"). F-MODE-COVERAGE F26 (line 72 "chain length is a formula property, visible and lintable"), F53 (line 77 "Substrate-triggered structural controls … formula checks"). component-inventory C14 row (Maps from A37/A34/A37b/B29; Depends on C12; gap G24; Subsystem Workflow Engine; Kind interface; foundational no). review-log C12:OQ-2 ("loop primitive vs pure DAG … drives C15/C14"), D-7 (node-kind taxonomy home = C12). Related specs: `spec/C12-formula-pipeline-file.md` (the formula artifact + node-kind set this translates), `spec/C15-workflow-linter.md` (downstream consumer of the DOT side), `spec/C02-pack-extension-abi.md` (the pack/tool-node surface C14 ships over).
> Inventory ID: C14   Kind: interface   Status: sweep-1
> Track: canonical (faithful posture)

## 1. Purpose & responsibility

C14 is the **interop seam between the Gas City formula format (C12, TOML DAG) and the DOT-graph ecosystem**.
It exists for two reasons the corpus states plainly: (a) to **render a formula for human review**
(README:133 "Render the DAG for review") — the half README:392 marks P3-delivered "full, including
visualization" (the *export/visualize* direction is the delivered, near-native one); and
(b) to give the factory **bidirectional DOT↔formula interop** so DOT-ecosystem tooling — chiefly the
Mammoth-derived 21-rule linter (C15) — can be brought to bear on v4's workflows (README:135, :538;
AI-CONTEXT:469). The bidirectional/import half is the "small Go side project" that "doesn't have to be
perfect" (README:538); its guarantee is not Phase-1 "delivered-full" but the **G24 round-trip proof** below. v4 frames it as a *small* artifact: "~few hundred LOC Go" (README:135), "a small Go side
project" that "doesn't have to be perfect" (README:538).

The load-bearing obligation — and C14's whole reason to be a *spec'd component* rather than a throwaway
script — is **round-trip fidelity (G24)**: the corpus asserts lossless bidirectionality between two formats
of *unequal expressive power* (TOML's sections-as-flags vs DOT's arbitrary edge/node attributes) but never
shows it holds. C14 owns that proof. Its deliverable is not "a DOT writer" (DOT writers/parsers are
off-the-shelf, README:384 "transfusion source: any DOT writer/parser library") — it is the **translation
contract plus the round-trip property that makes the contract trustworthy**.

**Responsibilities**
- Define the **formula→DOT export** mapping: how a C12 formula (nodes with a kind from `{agent, tool, gate,
  sub_formula}`, edges/dependencies, gates, parameters) is rendered as a DOT `digraph` suitable for
  graphviz rendering and for DOT linters (C15).
- Define the **DOT→formula import** mapping: how a DOT graph (within an agreed **profile** — see §3) is
  parsed back into a valid C12 formula.
- **Prove and bound round-trip fidelity (G24):** specify `formula → DOT → formula` as the canonical
  lossless direction, define the **canonical-form / normalization** that makes equality decidable, and
  **enumerate the DOT constructs that fall outside the formula's expressive power** (so the reverse
  direction either rejects them loudly or maps them by an explicit, documented rule — never silently
  drops them).
- Ship as a **Gas City pack** (README:133/135 "Gas City pack"): a tool-node binary over the C02 ABI plus,
  where it exists, a thin seam to the native `gc formula export … --format dot` path (README:385).

**Explicitly NOT**
- **NOT the formula format itself (C12).** C14 *reads and writes* the C12 artifact; it does not own the
  formula schema or the node-kind set. The set `{agent, tool, gate, sub_formula}` is **named by C12
  (taxonomy home, D-7)** — C14 *references* it to map node kinds onto DOT, and must **never redefine it**.
- **NOT the DOT-ecosystem linter.** Structural rules over the DAG are **C15** (Mammoth 21-rule transfusion;
  inventory C15, depends on C14). C14's job is to *produce the DOT C15 lints* and to keep that DOT faithful;
  the rules themselves, and porting them, live in C15 (README:134; AI-CONTEXT:509).
- **NOT graphviz / the renderer.** Turning DOT into a picture is **graphviz** (off-the-shelf, README:143).
  C14 emits DOT; it does not draw pixels. The `--format dot` rendering path is `gc` + graphviz, not custom
  C14 code (see the DROP note in §3.1 and OQ-1).
- **NOT a DOT writer/parser library.** The byte-level DOT syntax is handled by an existing DOT library
  (README:384). C14 is the *semantic mapping* layered on top, plus the fidelity proof — not a re-implemented
  grammar.
- **NOT the runtime.** C14 never executes a workflow; it only translates its description. Execution is Gas
  City (C01) over the C12 formula. The DOT form is for **review, interop, and linting only** — it is not an
  alternate execution input (the formula remains the source of truth; the round trip must return *to* the
  formula).

## 2. Context & dependencies

| Direction | Component | Relationship |
|---|---|---|
| Upstream (depends on) | **C12** formula / pipeline-file format | C14 reads/writes the C12 TOML formula and references C12's node-kind set `{agent, tool, gate, sub_formula}` (D-7). C12 is C14's sole hard dependency (inventory). |
| Upstream (host surface) | **C02** pack & tool-node ABI | C14 ships as a pack: its translator runs as a `[[tool]]` subprocess tool node over the C02 ABI (README:133/135 "Gas City pack"). |
| Upstream (optional seam) | **C01** Gas City substrate | The native `gc formula export <name> --format dot` command (README:385) — if `gc` provides it — is C14's preferred export front door; C14 wraps/extends it rather than reinventing it (G11 caution, see §3.1). |
| Downstream (primary consumer) | **C15** workflow linter (Mammoth 21-rule) | C15 lints the **DOT** C14 emits; the bidirectional capability is "what enables Mammoth-compatible linting" (README:538). C15 depends on C14 (inventory). |
| Downstream (consumer) | **Human reviewer / graphviz** | The export feeds graphviz for "render the DAG for review" (README:133, :392). |
| Peer / terms | **C07** vocabulary-glossary | C14 uses C07's canonical meanings of `formula`, `tool node`, `gate`, `sub_formula` (G06). |

C14 is **not foundational** (inventory: no) and lands in **Batch 3** (Workflow tooling), after C12 (Batch 1)
and alongside C15 (which consumes it). It is a leaf on the dependency graph: nothing the critical-path spine
needs blocks on C14, but C15's lint value blocks on C14's DOT fidelity.

## 3. Interfaces / contracts

Sweep 1 — interfaces **named and described**; concrete DOT attribute names, the formal canonical form, and
the exact DOT profile grammar are deferred to sweep 2.

### 3.1 Outbound: `export` — formula → DOT (the visualization + lint feed)

A named operation **`export(formula) → dot`**: given a C12 formula, emit a DOT `digraph` whose nodes are the
formula's steps and whose edges are its dependencies. Sweep-1 mapping (named, not yet attribute-typed):

| Formula concept (C12) | DOT rendering (described) | Note |
|---|---|---|
| Node identity | DOT node id | 1:1; ids must survive the round trip (canonical-form key). |
| Node **kind** `{agent, tool, gate, sub_formula}` | DOT node attribute (e.g. a `kind=` attr) **+** a visual style (shape/color) for graphviz | Kind values are **C12's** (D-7); C14 only chooses the attribute encoding. |
| Node binding (C17 tool name / C09 template name) | DOT node attribute | Preserved verbatim for round-trip. |
| Edge / dependency | DOT directed edge | Edge direction = dependency direction. |
| **Loop / back-edge marker** (bounded-iteration construct) | DOT **marked back-edge** (a back-edge carrying an attribute that flags it as a *sanctioned bounded loop*, distinct from a raw cycle) | **The C14→C15 seam element.** C15 must distinguish a sanctioned bounded loop from a raw back-edge in the DOT it lints (C15 §3.3 rule 1; C15 §9 OQ-2 names "loop-construct markers" as part of the surface it needs). The **concrete encoding is deferred to C12:OQ-2** (the loop primitive is unfrozen — §3.4); this row freezes the *obligation* (export must emit a marked, lintable loop) so C15's loop-lint capability is not silently dropped. |
| Gate / `wait` semantics | DOT node (kind=`gate`) + attribute | The gate is a node-kind, so it rides the kind mapping. |
| Formula parameters / metadata | DOT graph-level attributes | Graph attrs carry formula-scope data that has no node home. |

> [FAITHFUL-FILL] **Export may be partly native — flag a custom translator.** The corpus carries **two
> signals here, not one.** README:385 ("Add `gc formula export <name> --format dot` for graphviz rendering")
> implies the **export direction is, or will be, a `gc`-native subcommand**; but README:133 labels the
> visualizer "**Custom: formula → DOT exporter + graphviz**" and README:384 says "**Build** the formula↔DOT
> bidirectional translator as a small Go tool." So whether export is native `gc` or factory-custom is
> genuinely open (OQ-1), not merely "unverified that :385 is native." The capability-for-principle bar
> resolves the default regardless: if Gas City provides export natively, C14 must **not** reimplement it. The minimal-consistent reading: C14's export interface is the
> **named contract**, and its *implementation* is "shell out to / wrap `gc formula export --format dot`
> where it exists; supply the thin mapping only for whatever `gc` does not emit." The genuinely-custom,
> principle-bound code is the **import** direction and the **fidelity proof** (3.2/3.3), not a second DOT
> exporter. (G11 caution: README:385 is framed under "Add", so whether `--format dot` is native `gc` or a
> v4-supplied subcommand is unverified — OQ-1. C14 must not bind to invented `gc` export internals; it binds
> to the *observable* `--format dot` output if present, else emits DOT itself via an off-the-shelf writer.)

### 3.2 Inbound: `import` — DOT → formula (the interop direction)

A named operation **`import(dot) → formula`**: parse a DOT graph (within the **C14 DOT profile**, below) into
a valid C12 formula. This is the direction with **no native `gc` support named anywhere** in the corpus and
is therefore C14's irreducible custom surface.

- **The C14 DOT profile.** Because DOT is strictly more expressive than a C12 formula (G24's core point),
  `import` is defined over a **named, restricted DOT profile**, not arbitrary DOT: the subset of DOT that has
  a well-defined formula meaning (the constructs `export` produces, plus the Attractor/Mammoth-shaped DOT the
  corpus points at — README:301; one-shot `*.dot` exemplars). DOT outside the profile is handled by §3.3's
  rejection/mapping rule, never silently coerced.
- **Validity postcondition.** `import` must yield a formula that **C12 accepts and C15 would not flag as
  malformed**; an import that cannot produce a valid formula fails loudly (it does not emit a broken
  formula).

### 3.3 The round-trip / fidelity contract (G24 — the core deliverable)

This is the contract C14 exists to guarantee. Three named properties:

1. **Canonical lossless direction — `formula → DOT → formula` = identity (mod canonical form).** For any
   valid C12 formula `f`, `import(export(f))` must equal `f` after both are reduced to a defined
   **canonical form** (stable node/edge ordering, normalized attribute set, no presentation-only noise).
   Equality is asserted on the canonical form, not on raw bytes, because attribute/line ordering is not
   semantically meaningful. **This is the property G24 says is asserted-but-unshown; C14 makes it testable
   (see §8 AC-1) and CI-enforced.**
2. **Reverse direction is fidelity-bounded, not assumed-lossless — `DOT → formula → DOT`.** For DOT *inside
   the C14 profile*, the reverse round trip is also identity-mod-canonical-form. For DOT *outside* the
   profile, C14 owes an **explicit, enumerated** outcome per construct: either (a) a documented lowering rule
   into the formula, or (b) a **loud rejection** naming the unsupported construct. Silent loss is forbidden —
   that is the exact failure G24 warns of (lossiness "asserted, not shown").
3. **The expressive-power gap is enumerated, not hand-waved.** C14 ships (sweep-2) a **catalog of DOT
   constructs with no formula equivalent** — arbitrary edge attributes, multi-edges, ports/record shapes,
   subgraph/cluster semantics beyond `sub_formula`, undirected edges, cycles where the formula is acyclic,
   etc. — each marked *lowered-by-rule* or *rejected*. This catalog **is** the G24 resolution: fidelity is
   *proven within a stated profile* and *bounded with a named exclusion list* outside it.
   > [AMBIGUITY: G24] **Is the asserted "lossless bidirectionality" (README:135) a property of *all* DOT, or
   > of the formula-shaped subset?** *Reading A:* lossless for arbitrary DOT↔formula (the literal reading of
   > "bidirectional translator"). *Reading B:* lossless for the **formula↔DOT round trip and the DOT-profile
   > subset**, with a bounded, declared exclusion list for richer DOT. **Pick Reading B.** Two unequal
   > formats cannot be mutually lossless in general (this is G24's own argument), and the corpus's *purpose*
   > for the reverse direction is interop with formula-shaped DOT linters (C15) — not ingesting hostile
   > arbitrary DOT. Reading B is the only internally-consistent reading and is what "round-trip fidelity must
   > be proven" (inventory) actually demands: prove it where it can hold, bound it where it cannot.

### 3.4 The loop-primitive caveat (cross-component, drives fidelity)

> [AMBIGUITY: C12:OQ-2] The corpus has not settled **how Gas City expresses bounded iteration in a "DAG
> file"** (review-log C12:OQ-2, explicitly "drives C15/C14"). If formulas encode loops (a back-edge, a
> bounded-repeat node), that construct must have a **defined DOT encoding and a defined inverse**, or the
> round trip breaks on every iterative formula. C14 cannot resolve C12:OQ-2 (it is C12's), but it **must
> treat the loop primitive as a first-class entry in the §3.3 exclusion/mapping catalog** and freeze its DOT
> encoding the moment C12 freezes the primitive.
>
> **Two states must not be conflated (C14↔C15 seam).** C14's *end-state* is **not** to reject loops — it is
> to **export them as a marked back-edge** (the §3.1 loop/back-edge marker row) so that **C15 can lint the
> loop**: C15 §3.3 rule 1 must tell a sanctioned bounded loop apart from a raw cycle, and C15 §9 OQ-2 names
> "loop-construct markers" as exactly the surface it needs C14 to freeze. Distinguish:
> - **(interim, until C12:OQ-2 lands)** — the loop primitive is unfrozen, so C14 has no encoding to emit;
>   an as-yet-unencodable loop is a **rejected** catalog entry that **fails loud** rather than emitting
>   *lossy/ambiguous* DOT (better to refuse than to emit a raw back-edge C15 would mis-flag as a cycle).
> - **(end-state, once C12 freezes the primitive)** — C14 emits the **marked** loop construct and ships a
>   defined inverse; the catalog entry flips from *rejected* to *lowered-by-rule*, restoring C15's
>   loop-lint capability. Fail-loud is the temporary blocker, **not** a permanent capability removal.
>
> Flagged as OQ-2; gates C15's ability to lint loops, which is why the §3.1 marker row freezes the
> *obligation* now even though the concrete encoding waits on C12.

## 4. Data model / state

C14 is an **interface/translator**, not a data store; it owns *mapping definitions*, not live state.

- **Owned: the formula↔DOT mapping table** and the **C14 DOT profile grammar** (the named subset of DOT with
  formula meaning). These are format definitions, version-locked to the C12 schema version they target.
- **Owned: the canonical-form definition** used to decide round-trip equality (§3.3.1).
- **Owned: the DOT-construct exclusion catalog** (§3.3.3).
- **No persistent runtime state.** Each `export`/`import` is a pure function of its input artifact (a
  stateless tool-node invocation over the C02 ABI). > [FAITHFUL-FILL] statelessness is the minimal-consistent
  shape: README frames C14 as a "small Go tool"/"side project" with no store, and the C02 tool-node ABI is
  spawn-per-step.
- **Versioning.** Because the mapping is pinned to C12's formula schema and AI-CONTEXT §3.5 predicts breaking
  formula-format changes, C14's mapping table carries the **C12 schema version it round-trips against**, so a
  formula it cannot faithfully translate is rejected rather than silently mistranslated.

## 5. Behavior

Key flows (sweep-1 narrative; sequence diagram deferred to sweep-2):

- **Visualization flow.** Reviewer asks to see a formula → C14 `export`s it to DOT (wrapping `gc formula
  export --format dot` where native) → graphviz renders the DOT → human reviews the DAG (README:133, :392).
- **Lint flow.** C14 `export`s the formula to DOT → **C15** runs the Mammoth-derived 21 rules over that DOT →
  findings route back (this is the "bidirectional capability … enables Mammoth-compatible linting" path,
  README:538). C14's only job here is that the DOT it emits is a faithful image of the formula, so C15's
  findings are about the *real* workflow.
- **Interop / import flow.** A DOT graph from a DOT-ecosystem tool (within the profile) → C14 `import`s it to
  a C12 formula → C12/C15 validate it → it becomes a runnable formula.
- **Fidelity gate (the load-bearing flow).** In CI, for every formula in the corpus and a property-based
  generator of formulas, run `import(export(f)) ≟ f` under canonical form; any mismatch is a **build
  failure** with a diff. This is what converts G24 from an assertion into a guarantee.

## 6. Failure modes & handling

| F-mode / failure | Relevance to C14 | Handling (faithful) |
|---|---|---|
| **F26** Telephone / sustained chain | "chain length is a formula property, visible and **lintable**" (F-MODE:72). C14 is what makes a formula *visible* (export→graphviz) and *lintable-via-DOT* (export→C15). | C14 enables the visibility/lint that addresses F26; the rule that flags over-long chains is C15's. C14's duty is fidelity so the chain C15 sees is the real one. |
| **F53** Voluntary-discipline fragility | "formula checks replace operator-voluntary discipline" (F-MODE:77). DOT-ecosystem linting is one such substrate check. | C14 supplies the DOT that makes the check possible; the check is C15. |
| **Round-trip loss (G24 core)** | A formula that translates to DOT and back to a *different* formula would make visualization and linting lie. | The §3.3 fidelity contract + the §8 CI gate: mismatch = loud failure, never silent. Out-of-profile DOT on `import` is **rejected by name**, never coerced. |
| **Expressive-power overflow on import** | DOT carrying constructs with no formula meaning (arbitrary edge attrs, ports, clusters, cycles). | `import` rejects out-of-profile constructs with a message naming the construct (§3.3.2); it never emits a malformed formula. |
| **Loop-primitive mismatch** | If C12's iteration primitive has no DOT inverse, iterative formulas break the round trip. | Treated as a first-class catalog entry (§3.4). **Interim** (C12:OQ-2 unfrozen): export of an as-yet-unencodable loop **fails loud** rather than emitting lossy/ambiguous DOT. **End-state** (C12 freezes the primitive): export emits a **marked back-edge** (§3.1 loop-marker row) with a defined inverse so C15 can lint the loop — the entry flips *rejected* → *lowered-by-rule*. Fail-loud is the temporary blocker, not C14's end-state. |
| **C12 schema drift** | A new formula-format version C14 hasn't mapped. | Version-locked mapping (§4) rejects unknown schema versions rather than mistranslating. |
| **Drift from `gc` export output** | If C14 wraps native `gc formula export` and that output changes. | C14 binds to the *observable* `--format dot` output, not `gc` internals (G11); a contract test (§8 AC-5) catches output drift. |

## 7. Cross-cutting (security / cost / scale / observability / ops)

- **Security.** C14 handles only workflow *descriptions* (formulas/DOT), not credentials or live data; no
  lethal-trifecta surface of its own. The one caution: `import` parses untrusted DOT, so it must use a
  hardened off-the-shelf DOT parser and the restricted profile (§3.2) — it must not `eval` or execute graph
  content. (DOT is data, never code, to C14.)
- **Cost.** Zero token cost — C14 is **deterministic** (it is itself a `tool` node, the P4 deterministic-first
  case): pure format translation, no model in the loop. Process-spawn cost only (C02 spawn-per-step). v4
  states no perf budget (it's "small"/"few hundred LOC"); none invented here.
- **Scale.** Translation is O(nodes+edges) per formula; formulas are human-authored DAGs (tens of nodes), so
  scale is a non-issue. Not on any throughput-ceiling path (cf. G34).
- **Observability.** Each translation is a tool-node invocation and carries `created_by` (C41) on the event
  bus (C23) like any tool node — useful for "who re-rendered/translated which formula when".
- **Ops / licensing.** C14 is "your work" (README:133/135, n/a license) built on an off-the-shelf DOT
  writer/parser (README:384) and graphviz — both standard-permissive; no `internal/` Gas City import (C14 is
  a pack over C02, not a Go import of `gc`). The Mammoth transfusion that *uses* C14's DOT is C15's license
  concern, not C14's (README:301 "MIT; verify").

## 8. Acceptance criteria & test strategy

Sweep-1 high-level criteria (concrete tests at sweep-2):

1. **Round-trip identity holds (G24).** For every formula in the corpus **and** a property-based generator of
   valid C12 formulas, `import(export(f))` equals `f` under the defined canonical form. CI-enforced; any
   mismatch fails the build with a diff. *(This AC is the G24 resolution made testable.)*
2. **Profile round-trip holds in reverse.** For DOT inside the C14 profile, `export(import(d))` equals `d`
   under canonical form.
3. **Out-of-profile DOT is rejected, not coerced.** A DOT graph carrying an enumerated unsupported construct
   (arbitrary edge attr, port, cluster, cycle, undirected edge) causes `import` to fail with a message naming
   the construct — and **never** yields a malformed or silently-lossy formula.
4. **Exclusion catalog is complete & honest.** Every DOT construct the parser can encounter is classified
   *lowered-by-rule* or *rejected* in the §3.3.3 catalog; no "undefined behavior" gaps. (Sweep-2 deliverable;
   sweep-1 names the obligation.)
5. **Export matches the native path (if any).** Where `gc formula export --format dot` exists, C14's export
   is semantically equal to it (same nodes/edges/kinds), so C14 wraps rather than diverges (OQ-1); a contract
   test detects drift in `gc`'s output.
6. **DOT is lint-ready for C15.** The DOT C14 emits parses cleanly in the Mammoth-derived linter (C15) and
   the linter's findings correspond to real formula properties (validated against a known-malformed formula).
7. **Node-kind fidelity.** Every node-kind value `{agent, tool, gate, sub_formula}` survives
   formula→DOT→formula unchanged, and C14 never introduces a kind value outside C12's set (D-7 conformance).

## 9. Open questions

(Mirrored into `_meta/review-log.md`.)

1. **[OQ-1 — top open question] Is `gc formula export <name> --format dot` native `gc` or a v4-supplied
   subcommand?** The corpus is genuinely two-sided: README:385 frames it under "Add" (suggesting a `gc`
   subcommand), while README:133 ("**Custom**: formula → DOT exporter") and README:384 ("**Build** … a small
   Go tool") suggest factory-custom — and all are unverified (G11). This decides whether C14's export
   direction is a thin *wrapper* over native output (preferred under the bar — don't reinvent) or a *custom*
   DOT emitter (over an off-the-shelf writer, README:384). Resolve by running `gc` (the same G11 spike
   C01/C02 need); until then C14 binds to observable `--format dot` output if present, else emits DOT via an
   off-the-shelf writer. Either way C14 never reinvents a *native* exporter and never binds to `gc` internals.
2. **[OQ-2] Loop / bounded-iteration primitive (C12:OQ-2).** C12 has not frozen how a formula expresses
   iteration in a DAG file; this "drives C15/C14" (review-log). C14 cannot round-trip a loop construct it
   cannot encode in DOT. **This is the load-bearing C14→C15 seam contract:** C15 §9 OQ-2 needs C14's DOT to
   carry **loop-construct markers** so C15 §3.3 rule 1 can distinguish a sanctioned bounded loop from a raw
   cycle. C14's §3.1 export surface therefore freezes the *obligation* (export a **marked** loop) now; the
   *concrete encoding + inverse* freeze the moment C12 freezes the primitive. Until then, an unencodable loop
   is a *rejected* catalog entry (fail loud, not lossy) — the **interim** state, **not** C14's end-state
   (end-state = marked back-edge, *lowered-by-rule*, so C15 can lint loops; see §3.4).
3. **Exact canonical form for equality.** The precise normalization (node/edge ordering, attribute
   canonicalization, which presentation attrs are "noise") that makes `import(export(f)) = f` decidable is a
   sweep-2 deliverable; sweep-1 only asserts it must exist and be the basis of the CI gate.
4. **The C14 DOT profile grammar.** The exact restricted DOT subset `import` accepts (and the full exclusion
   list) must be pinned against the Attractor/Mammoth-shaped DOT the corpus targets (README:301; one-shot
   `*.dot` exemplars) — sweep-2.
5. **DOT encoding of node bindings & parameters.** Whether tool/template bindings and formula parameters ride
   as node attributes vs graph attributes (§3.1) must be fixed so both directions agree — sweep-2, jointly
   with C12's on-disk field decisions (C12:OQ-4).
