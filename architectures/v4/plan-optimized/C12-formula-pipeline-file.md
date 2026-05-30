# C12 — Formula / pipeline-file format  (Build Plan, Track B)

> Source / Spec ref: [C12 spec (Track B)](../spec-optimized/C12-formula-pipeline-file.md)

## 1. Work breakdown

| Task | Description | Size | Prereqs |
|---|---|---|---|
| T1 | **Probe Gas City's native formula schema** (OQ1/OQ2/OQ3): read `gc` formula docs + a real formula file; record the native node model, branching/gate support, and `sub_formula` composition support. | M | C01 shape fixed |
| T2 | **Freeze the formula schema (DELTA-01)**: identity / parameters / nodes / edges / gates blocks as versioned TOML grammar; write the schema-version doc. | M | T1 |
| T3 | **Define the node taxonomy (DELTA-02)**: closed `{agent, tool, gate, sub_formula}` set; per-kind `ref` namespace mapping to C09/C17/C18/C12. | S | T2 |
| T4 | **Specify the binding contract (DELTA-03)**: `FormulaParameters` declaration + resolution to C08 spec_ref and C09 template_ref; parameter totality fail-closed rule. | M | T3, C08/C09 contracts |
| T5 | **Define `ParsedFormula` + well-formedness invariants (DELTA-05)**: acyclicity, reachability, no-dangling-ref, sub_formula acyclicity; typed diagnostics (`FormulaCycle`, etc.). | M | T2 |
| T6 | **Define `CanonicalForm` + identity hash (DELTA-07/04)**: deterministic node/edge/key ordering; `{name, version, methodology_id, transfused_from}` identity + hash. | M | T5 |
| T7 | **Define the formula↔DOT vocabulary intersection (DELTA-07, OQ4)**, co-specified with C14: which constructs round-trip losslessly; out-of-vocabulary rejection rule. | M | T6, C14 contract |
| T8 | **Author the golden formula corpus**: the Phase-1 3-step minimum (README:383) + malformed fixtures (cycle/orphan/dangling) shared with C15. | S | T5 |
| T9 | **Wire provenance/attribution (DELTA-06)**: formula authoring/promotion emits attributed event (C41); `transfused_from` lineage for C51. | S | T6 |

## 2. Dependency graph

- **Upstream (must precede C12 usefully):** C01 (runner + native schema — gates T1), C03 (`[formulas]` flag). C08/C09 contracts needed for T4; C17/C18 ref-namespaces for T3; C14 vocabulary for T7.
- **Critical path inside C12:** **T1 → T2 → T3 → T5 → T6 → T7**. Everything is downstream of T1 (the Gas City schema probe): the spec's top open question (OQ1) is "how much are we *describing* vs *constraining*?" — T1 collapses that uncertainty and unblocks the rest.
- **Downstream blocked on C12 contracts:** C13 (needs T4 binding + T5 ParsedFormula), C14 (needs T6 canonical + T7 vocabulary), C15 (needs T5 invariants + T8 fixtures), C16 (needs T3 taxonomy), C18 (needs T3 gate kind), C55/C50 (need T6 identity).

```
T1 ── T2 ── T3 ──┬── T4 ── (C13)
                 ├── T5 ──┬── T6 ──┬── T7 ── (C14)
                 │        │        └── T9
                 │        └── T8 ── (C15)
                 └────────────────── (C16 needs T3)
```

## 3. Parallelization

After T1 + T2 (serial, blocking — the schema must exist first), three workstreams run concurrently:

- **WS-A (executor semantics):** T3 → T4 — node taxonomy + binding contract (interfaces C09/C13/C17/C18 build against).
- **WS-B (structural truth):** T5 → T8 — invariants + golden/malformed fixtures (C15 builds against).
- **WS-C (interop/identity):** T6 → T7 → T9 — canonical form, DOT vocabulary, provenance (C14/C50/C55/C51 build against).

WS-A/B/C share only the frozen T2 schema, so they fan out cleanly. T7 has a cross-dependency on C14's spec and should be co-owned.

## 4. Interfaces-first / contract milestones

Freeze these early so dependents stub against them:

1. **The formula TOML schema (T2)** — the artifact contract; freeze first, everything keys off it.
2. **Node taxonomy + per-kind `ref` namespaces (T3)** — lets C09/C17/C18 know their identifier space and C16 know what's lintable.
3. **`ParsedFormula` + well-formedness invariants (T5)** — the object C13/C14/C15 consume; freeze before linter work starts.
4. **`FormulaIdentity` `{name, version, methodology_id}` (T6)** — the swappability handle C55/C50 depend on.
5. **DOT round-trip vocabulary intersection (T7)** — the contract C14 implements; co-frozen with C14.

## 5. Risks & de-risking order

1. **OQ1 — Gas City's actual formula schema is unverified (G11).** Highest risk: if the native grammar contradicts the node taxonomy, T2/T3 are a conform-or-fork decision touching C01. **De-risk first (T1)** with a real `gc` formula before freezing anything.
2. **OQ2/OQ3 — branching + sub_formula composition may not be native.** Several v3 candidate methodologies need conditional branching / composition; if not in-format, methodology expressiveness moves to C18 + a pack. Spike a branching + sub_formula formula early (within T1).
3. **G24 / DOT round-trip (T7).** Two formats of unequal power; de-risk by defining the *intersection* (DELTA-07) rather than promising losslessness across the union — prototype one formula→DOT→formula cycle against a Kilroy/Attractor `.dot` exemplar.
4. **Binding contract coupling (T4).** Depends on C08/C09 maturity; stub their refs to avoid a serial stall.

## 6. Definition of done

- **Per-task:** each DELTA's acceptance criterion in [spec §8](../spec-optimized/C12-formula-pipeline-file.md#8-acceptance-criteria--test-strategy) passes (schema stability, taxonomy closure, well-formedness fail-closed, binding totality, methodology identity, DOT round-trip, 3-step minimum, vocabulary authority).
- **Per-component:**
  - A versioned formula schema doc exists; the golden corpus (incl. the 3-step minimum) parses, binds, and hands a well-formed bound graph to C13.
  - Malformed fixtures (cycle/orphan/dangling/self-include) all fail closed with typed diagnostics, sharing fixtures with C15.
  - `CanonicalForm` round-trips losslessly with C14 across the agreed vocabulary intersection; out-of-vocabulary DOT is rejected, never silently dropped.
  - C07 glossary links "formula"/"molecule"/"node"/"gate" to this spec as the definition source (G06 closed for C12's vocabulary).
  - OQ1 resolved (Gas City schema confirmed) and recorded in the review-log; OQ2–OQ4 either resolved or explicitly carried to C14/C18/C55 specs.
