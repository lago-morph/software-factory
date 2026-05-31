# C16 — Discipline linter (LLM-where-tool) (`discipline-linter`)  (Build Plan, canonical track)

> Source / Spec ref: spec/C16-discipline-linter.md
> Track: canonical. Sweep: 1 (architecture altitude — plan names the workstreams and the contracts to freeze; per-heuristic detectors + false-positive measurement land at sweep 2/3).

## 1. Work breakdown

Ordered tasks. Size S/M/L. Prerequisites by task id / component id.

| id | Task | Size | Prereqs |
|---|---|---|---|
| T1 | **Freeze C16 I/O contract** as a C17 deterministic tool node over the C02 ABI: declared inputs (`formula_path`, rule config) → status (exit code) + declared output (findings report + per-guard catch counts). | S | C17, C02 ABI frozen; C12 §3.1 node-kind data |
| T2 | **Define the findings-report schema** with the **mandatory `falsifying_scenario`** field (`node_id`, `rule_id`, `severity`, `message`, `falsifying_scenario`); pick serialization (defer JSON/SARIF to sweep 2 per OQ-4); stub so dependents can read it. The schema MUST make a finding without a falsifying scenario unrepresentable (INV-2). | S | T1 |
| T3 | **Author the heuristic-set definition** (the in-pack rule table): enumerate the "a tool would suffice" heuristics (pure transform / lookup / deterministic validation / no-reasoning-verb), each as `rule_id` + default severity + mechanically-checkable flag. (Sweep-2 deepens to per-heuristic detectors + false-positive rate.) | M | spec §3.3 |
| T4 | **Implement the LLM-where-tool detectors** over `agent` nodes: read each node's kind (C12 set, **D-7**) + task/prompt, run the heuristics, emit a finding *with its falsifying scenario* when one fires. | L | T2, T3 |
| T5 | **Implement the justification-rebuttal path**: read the author "why a model is required here" annotation on `agent` nodes; suppress/downgrade a flag when a non-empty justification is present (§3.3). Coordinate the annotation field home with C12 (OQ-3). | M | T4; C12 (annotation field) |
| T6 | **Implement per-guard catch-count emission** as a C46 meta-metric input (the monthly F52 review, F-MODE:100); emit as part of the run record (bead), no separate store. | S | T2; C46 metric-input shape |
| T7 | **Parse front-end / node-walk** over the C12 TOML DAG (enumerate nodes + kinds + annotations); on a parse failure, defer structural errors to C15 and emit a low-severity "could not analyse" note (spec §6). | M | T1; C12 format; C15 boundary |
| T8 | **Blocking/advisory disposition** wiring to C03 config (INV-3): default advisory (zero exit + report + counts); per-heuristic-class opt-in to blocking (nonzero exit). | S | T1, C03 |
| T9 | **Package as a Gas City pack** with a `[[tool]] type="subprocess"` declaration (C02) so it places as a C17 deterministic node. (No OSS transfusion source expected — README:160 "n/a (your work)"; confirm at sweep 2.) | M | T1, T4–T6 |
| T10 | **Test corpora + acceptance suite** (AC-1…AC-9): positive (LLM-where-tool → finding+scenario), justified (no error), clean (zero), determinism (run-twice diff), blocking-config matrix, and the **reflexive-discipline test** (no finding may lack a falsifying scenario, AC-2). | M | T4–T8 |

## 2. Dependency graph

**Must precede C16 (external):**
- **C12** formula format **incl. its node-kind set `{agent, tool, gate, sub_formula}`** (the input surface +
  the `agent`/`tool` distinction C16 keys on; **D-7**) — must be frozen. (Batch 2.)
- **C17 / C02** tool-node abstraction + ABI (declared inputs → status + outputs) — frozen.
- **C03** config layering (the enable + blocking disposition) — shape known.
- **C46** meta-metric input shape (for the catch-count emission) — shape known.
- **C12** annotation field home for the justification marker (OQ-3) — needed for T5; can stub against an
  agreed field until C12 standardizes it.

**Critical path:** C12 (+ node-kind set) + C17/C02 frozen → **T1** (I/O contract) → **T2** (report schema
with `falsifying_scenario`) → **T3** (heuristic table) → **T4** (detectors) → **T9** (pack) → **T10**
(acceptance). T1→T2→T3→T4 is the serial spine; T5/T6/T7/T8 fan out.

**Can run concurrently with C16:** **C15** (workflow linter) and **C14** (Formula↔DOT translator) — sibling
Workflow-Engine components that share the C12 formula input but do not depend on C16. C16 and C15 are
co-deployable over the same formula (different questions).

## 3. Parallelization

Once **T1–T3 (contracts + heuristic table)** are frozen, the work fans out because each heuristic is an
independent, stateless function over the same parsed formula:

- **Workstream A:** T4 LLM-where-tool detectors (further splittable **one detector per `rule_id`** — each
  heuristic is an independent function against the frozen report schema).
- **Workstream B:** T5 justification-rebuttal path (only this stream touches the C12 annotation field;
  isolatable; coordinate field home with C12).
- **Workstream C:** T6 catch-count meta-metric emission (only this stream touches the C46 metric-input
  shape; isolatable).
- **Workstream D:** T7 parse front-end / node-walk (the shared parser all detectors consume — freeze its
  output shape early so A/B build against a stub; it also owns the C15-boundary degrade path).

T8 (config), T9 (packaging), T10 (tests) gather the streams. The natural fan-out unit is **one detector per
`rule_id`** — the heuristic table (T3) is the contract that lets N detectors be authored in parallel.

## 4. Interfaces-first / contract milestones

Freeze these first so dependents and parallel streams build against stubs:
1. **C16 tool-node I/O contract (T1):** declared inputs (`formula_path`, config) → exit-code status +
   findings-report + catch-counts output, in the C17/C02 vocabulary. Lets C16 be *placed in a formula*
   (authoring/CI) before any detector exists.
2. **Findings-report schema *with* `falsifying_scenario` (T2):** the **load-bearing** contract — the schema
   makes "no guard without a falsifying scenario" (INV-2; F-MODE:100) structurally true, not advisory. Freeze
   before T4; every consumer (author loop, C39 fix-task, C46 review) reads it.
3. **Heuristic-table definition (T3):** the enumerated `rule_id`s + default severities the parallel detector
   streams divide along.
4. **Parsed-formula / node-walk shape (T7 output):** the front-end shape detectors consume — stub early so
   A/B don't block on D.
5. **Justification-annotation field (with C12, OQ-3):** agree the per-node marker home with C12 so T5 and the
   formula authors share one field.

## 5. Risks & de-risking order

Spike in this order to retire the most uncertainty:
1. **OQ-G18 / C39 boundary (highest leverage — fidelity risk):** confirm with **C39** (and possibly C18)
   that the self-healing-loop **numeric** termination/oscillation/L5-ship policy (**G18**, ledger **XC-3**)
   lives in C39, **not** C16. C16 builds *only* the static LLM-vs-tool linter. Settle before sizing anything,
   so C16 does not accidentally absorb runtime-loop policy (the over-build the bar forbids).
2. **OQ-2 / heuristic false-positive rate:** prototype the 4 seed heuristics against real formulas to measure
   the **"measurable false-positive rate"** F-MODE:100 mandates — this sizes T3/T4 and validates that the
   heuristics are useful, not noise. Biggest substance unknown. If a heuristic is too noisy to carry a
   *crisp* falsifying scenario, it is a candidate to DROP (it would be discipline-without-purpose — the F52
   trap C16 exists to prevent, applied to itself).
3. **OQ-3 justification-annotation home (with C12):** spike the per-node marker with C12 so the rebuttal path
   (T5) and authors agree on one field; de-risks re-flagging justified nodes every run.
4. **OQ-1 blocking-vs-advisory:** confirm with C03/integrator whether the linter ever hard-gates or is always
   advisory; drives T8 and AC-6. Spec picks advisory-by-default (discipline, not a gate).

## 6. Definition of done

**Per-component (sweep-1 exit):**
- C16 places as a C17 deterministic tool node via the C02 ABI, no model call (AC-9, AC-4).
- LLM-where-tool heuristics run over `agent` nodes of a C12 formula and emit the structured findings report,
  **every finding carrying a falsifying scenario** (AC-1, AC-2 — the load-bearing criterion).
- Justification annotation rebuts a flag (AC-3); per-guard catch counts emitted for the C46 monthly F52
  review (AC-7).
- Deterministic and read-only (AC-4, AC-5).
- Advisory-by-default with config-gated blocking wired to C03 (AC-6).
- Keys on C12's node-kind set without redefining it, and carries **no** heal-loop termination policy — G18 is
  routed to C39 (AC-8; XC-3).
- Test corpora (positive / justified / clean / determinism / blocking-matrix / reflexive-discipline) pass
  (AC-1…9).

**Per-task:** each Txx exits when its acceptance slice passes — e.g. each detector (T4) ships with a
positive fixture *and a falsifying-scenario assertion*; T5 with a justified-node fixture; T7 with the
unparseable-formula degrade case.

**Carried to sweep 2:** per-heuristic detector + severity + **false-positive-rate** table (OQ-2), findings
serialization choice (OQ-4), the C12 justification-field home (OQ-3), sequence diagram, and concrete
per-heuristic fixtures.
