# C12 — Formula / Pipeline-File Format  (Build Plan, Track A)

> Source / Spec ref: spec-faithful/C12-formula-pipeline-file.md

## 1. Work breakdown

| ID | Task | Size | Prerequisites |
|---|---|---|---|
| T1 | **Verify the real Gas City formula schema** — run `gc`, read the actual `gc formula` TOML format; record the concrete node/edge/kind/loop/parameter key names. Retires G11 for C12. | M | C01 shape fixed; a runnable `gc` |
| T2 | **Freeze the formula field model** (sweep 2): node identity, node kind tag, edge/ordering, gate/wait nodes, bounded-loop construct, parameters/placeholders — as a concrete TOML schema citing T1. | M | T1 |
| T3 | **Pin the node-kind field** jointly with C16 + C17 so one field serves discipline-lint, tool-node abstraction, and formula. | S | T2; C17 §3.1, C16 |
| T4 | **Pin the parameter-binding contract** jointly with C13 (`$slot`-style declaration → molecule binding). | S | T2; C13 |
| T5 | **Pin the bounded-loop / acyclicity construct** so DAG claim and Ralph-loop / self-heal re-entry coexist; feeds C15 cycle rules + C14 DOT mapping. | M | T2; C15, C14 |
| T6 | **Author the canonical 3-step reference formula** (README:383 "3-step minimum to validate") as the conformance fixture every dependent builds against. | S | T2 |
| T7 | **Scope-confirm convoy/order out** with C40 + C07 (C12 owns single-formula DAG only). | S | C40, C07 |
| T8 | **Write acceptance fixtures** (spec §8): valid DAG, malformed/cyclic reject, by-name resolution, kind-readable, DOT-tractable, config-gated, bounded-loop. | M | T2–T6 |

## 2. Dependency graph

- **Upstream that must precede C12 field-freeze:** **C01** (runtime/format owner — formulas are Gas City's
  native shape) and **C03** (`[formulas]` flag). The inventory states C12 "can start once C01/C03 shape is
  fixed."
- **Critical path:** **T1 (verify Gas City schema) → T2 (freeze field model) → T3/T4/T5 (cross-component field
  pins) → T6/T8 (fixture + acceptance).** T1 is the gating uncertainty (G11): until the real `gc` formula
  format is known, every field is provisional and no dependent can bind.
- **Downstream blocked on C12's frozen schema:** **C13** (instantiation), **C14** (DOT translation), **C15**
  (structural rules), **C16** (discipline rules), **C55** (methodology swap), **C50** (gate-as-formula). These
  cannot freeze their own contracts until T2/T3/T4/T5 land.

## 3. Parallelization

C12 is a small artifact-spec; internal fan-out is limited, but the cross-component *pins* parallelize:
- **Stream A (schema):** T1 → T2 — the spine; must go first.
- **Stream B (field reconciliations), all forkable once T2 drafts:** T3 (kind ↔ C16/C17), T4 (params ↔ C13),
  T5 (loop ↔ C14/C15), T7 (convoy/order ↔ C40/C07). These are independent conversations with different
  components and run concurrently.
- **Stream C (fixtures):** T6 + T8 follow the field model and can be written in parallel with the Stream B
  pins (they validate the same shape).

## 4. Interfaces-first / contract milestones

Freeze early so dependents build against stubs in parallel:
1. **The formula field model (T2)** — node/edge/kind/loop/parameter shape. The contract C13/C14/C15/C16/C55
   all bind to. Highest-leverage freeze in the Workflow Engine subsystem.
2. **The node-kind field (T3)** — one shared field across C12/C16/C17 (avoids three divergent tags).
3. **The parameter-binding contract (T4)** — formula↔molecule slot binding, frozen with C13.
4. **The bounded-loop/acyclicity construct (T5)** — frozen so C14's DOT round-trip and C15's cycle rules have a
   fixed target.
5. **The 3-step reference formula (T6)** — the executable conformance fixture dependents test against.

Publish T2's draft schema (even stubbed against unverified Gas City keys) before T1 fully completes, so
C13/C14/C15 can start against a provisional contract and re-bind when T1 lands.

## 5. Risks & de-risking order

1. **G11 — Gas City formula schema unverified (highest).** The entire field model is asserted "Native" but no
   author has run `gc`. **De-risk first (T1):** obtain/run Gas City, read the real `gc formula` format. If it
   diverges from the inferred model, every downstream binding shifts. This is the top open question.
2. **DAG-vs-loop tension (T5).** v4 says "DAG file" yet runs Ralph-loop and self-heal re-entry. If Gas City has
   no bounded-loop primitive within its DAG, the faithful reconciliation (loop = bounded re-entry construct)
   may need revisiting. Spike a Ralph-loop formula early.
3. **Node-kind field divergence (T3).** Three components (C12/C16/C17) independently fill a node-kind tag; if
   not reconciled they drift into three fields. Reconcile in one pass.
4. **DOT round-trip tractability (feeds C14/G24).** C12 must not introduce constructs with no DOT
   representation; validate the node/edge model against C14's translator design before freezing T2.

## 6. Definition of done

**Per-component DoD** (ties to spec §8 acceptance criteria):
- A concrete formula TOML schema is frozen against the **verified** Gas City format (T1/T2), or the residual
  G11 risk is explicitly flagged where verification was impossible.
- The 3-step reference formula parses, is acyclic, and executes node-by-node on C01 in topological order (§8.1).
- Methodology (chain/gate/kind) is read from the file, not prompts; a methodology change is a formula edit
  (§8.2).
- Every node resolves by name to a C17 tool node or C09 template; every parameter is molecule-bindable (§8.3).
- Node kind is machine-readable for C16/C15 (§8.4); one shared field reconciled across C12/C16/C17 (T3).
- The node/edge model is DOT-tractable (no construct without a DOT image) so C14 can attempt round-trip (§8.5).
- `[formulas]`-gating verified: absent → implicit single-step (Phase 0); present → composition (§8.6).
- An iterative formula expresses iteration as a bounded, lintable loop, not a raw cycle (§8.7).
- Convoy/order confirmed out of C12 scope with C40/C07 (T7).

**Per-task DoD:** each task closes its named cross-component pin (T3/T4/T5/T7) or fixture (T6/T8) with the
counterpart component's sign-off recorded, and every spec [FAITHFUL-FILL] / [AMBIGUITY: G06] either resolved
against verified Gas City behavior or carried forward as an explicit open question in `_meta/review-log.md`.
