# C07 — Vocabulary & glossary  (Build Plan, Track B)

> Source / Spec ref: [spec-optimized/C07-vocabulary-glossary.md](../spec-optimized/C07-vocabulary-glossary.md)
> Track B, sweep 1. Foundational. Deltas referenced: DELTA-01…06 (see spec header).

## 1. Work breakdown

Ordered tasks. Size S/M/L. Prereqs by task id (and external C-IDs).

| id | Task | Size | Prereqs |
|---|---|---|---|
| T1 | **`GlossaryEntry` schema** — `{term, canonical_definition, owning_components (C-ID[]), corpus_equivalent, provenance, aliases, deprecated_by, lock_in_cost, extraction_safe_synonym}`. Freeze the per-term record shape. DELTA-01/03/06. | S | — |
| T2 | **`CanonicalReading` schema + overloaded-term ledger** — `{term, pinned_sense, disambiguation_rule, rejected_senses[], rename_recommendation}`; seed the two known offenders ("layer" G01, "phase" G02). DELTA-02. | S | T1 |
| T3 | **`CanonicalTermSet` export shape** — flat machine-readable set (term + accepted aliases + deprecated forms), content-hashed + versioned; the artifact C10/C15 load. DELTA-04. | S | T1 |
| T4 | **Registry seed — Gas City term family** — author the ~13 Gas City / Gas Town terms (`city`, `rig`, `formula`, `molecule`, `pack`, `convoy`, `sling`, `wisp`, `order`, `wait`, `polecat`, `Mayor`, `Health Patrol`) with owner-pointer C-IDs + corpus equivalents (AI-CONTEXT §3.3, v3 [`01-vocabulary.md`](../../v3/build-guide/01-vocabulary.md)). DELTA-03/06. | M | T1 |
| T5 | **Registry seed — paradigm term family** — author the ~10 paradigm terms (`spec`, `scenario`, `holdout`, `judge`, `satisfaction`, `digital twin`, `gene transfusion`, `bead`, `CXDB turn`, `model stylesheet`) with owner-pointers. | M | T1 |
| T6 | **`CorpusTranslationTable` generator** — Gas-City-term → plain-corpus-name surface for human readers (cognitive-load mitigation). Derived from the registry, not a separate source. | S | T4, T5 |
| T7 | **Validation gate** — enforce the four invariants: term uniqueness; single canonical reading (overloaded term ⇒ `CanonicalReading` present); owner-pointer integrity (every C-ID resolves against [component-inventory](../_meta/component-inventory.md)); lint-set completeness (every term ∈ `CanonicalTermSet`); alias monotonicity. DELTA-04/05. | M | T2, T3, T4, T5 |
| T8 | **Render generator** — byte-deterministic Markdown glossary regenerated from the registry source (single-source-of-truth golden). | S | T4, T5, T6 |
| T9 | **Alias / deprecation lifecycle** — `DeprecateTerm` moves a term to an alias with `deprecated_by` + named removal version; downstream refs keep resolving. DELTA-05. | S | T1, T7 |
| T10 | **Lint-wiring handshake (C10/C15)** — publish the `CanonicalTermSet` consumption contract: how C10 (spec linter) and C15 (workflow linter) load + pin the content-hashed version; the off-canon / undefined / deprecated-past-removal checks they run. DELTA-04. | M | T3, T7, **C10**, **C15** |
| T11 | **Doc-term coverage check (G06)** — tooling that enumerates load-bearing terms in README/AI-CONTEXT and diffs against the registry; an undefined doc term is a build failure. | M | T4, T5, T7 |

## 2. Dependency graph

- **Upstream (must precede C07 being *useful*):** C01 (source of the Gas City term family — C07 records, does not invent, those names; soft/authoring-time dependency, no runtime call). The [component-inventory](../_meta/component-inventory.md) C-ID set must be stable enough for owner-pointer integrity (T7) to validate.
- **Downstream (consume C07):** **mechanical** consumers C10 (spec linter) + C15 (workflow linter) load `CanonicalTermSet` (T10); **reference** consumers are the broad fan-out of every component owning a v4 term (C01, C02, C05, C06, C12, C13, C18, C19/C20, C21/C22, C29, C40, C42, C44, C51, C54) — they cross-reference C07 instead of re-defining.
- **Critical path inside C07:** T1 → (T2 ∥ T3 ∥ T4 ∥ T5) → T7 → T10. T6/T8/T9/T11 hang off the registry + gate and are not on the longest path.
- **System note:** C07 is Batch-1 foundational. Its load-bearing output is *not* code completeness but the **frozen `GlossaryEntry` + `CanonicalReading` + `CanonicalTermSet` schemas** (§4) plus the seeded overloaded-term ledger — that is what lets every other spec reference one canonical meaning and structurally kills the two-readings-of-"layer" bug class (G01/G02).

## 3. Parallelization

Explicit fan-out after the schema freeze (T1, then T2/T3):

- **Stream A (overload authority):** T2 — author the `CanonicalReading` ledger; the load-bearing Track-B mandate (pin "layer"/"phase"). Independent once T1 lands.
- **Stream B (registry content):** T4 ∥ T5 — the two term families are disjoint and authored in parallel by separate workstreams against the T1 schema.
- **Stream C (export + lint):** T3 → T10 — the `CanonicalTermSet` shape and the C10/C15 consumption handshake. T10 backgrounds on C10/C15 availability; stub the linter sink to unblock.
- **Stream D (human surface):** T6 → T8 — translation table + render; pure derivation from the registry, runs after content lands.

T4 and T5 are the natural parallel pair (two authors, disjoint term sets). T10 and T11 are the streams that depend on *other* components (C10/C15 for T10; the README/AI-CONTEXT corpus for T11) and are the natural background/last-to-land work.

## 4. Interfaces-first / contract milestones

Freeze these early so dependents build against stubs:

1. **`GlossaryEntry` schema (T1)** — the per-term record; every term author + every reference consumer codes against it first.
2. **`CanonicalReading` schema (T2)** — the overload-resolution record; freeze before any doc author needs to disambiguate "layer"/"phase". This is the artifact downstream specs cite to know which sense is canonical.
3. **`CanonicalTermSet` export contract (T3)** — content-hashed, versioned; the single surface C10/C15 vendor. Freeze so the linters can pin "validated against glossary vN".
4. **Owner-pointer convention** — the rule that a `GlossaryEntry` carries a *one-paragraph meaning + owning C-ID*, never authoritative depth — so owning specs (C12, C20, …) stay the single source for behavior and C07 never becomes a dual source of truth.

Stub strategy: ship the three schemas + the seeded overloaded-term ledger (the "layer"/"phase" `CanonicalReading`s) first; downstream specs reference the canonical senses while Streams B/C/D fill in the long tail of terms.

## 5. Risks & de-risking order

Spike highest-uncertainty first:

1. **OQ1 — authority scope of DELTA-02 (rename vs flag-only).** Does C07 get to mandate the corpus-wide rename ("Layer N" → "principle tier N", touching C54/C57/AI-CONTEXT §6/§7), or only to *flag* off-canon usage? This is a cross-component-edit decision; settle it before T2's `rename_recommendation` field is treated as binding. Pinning-only is the safe default; rename is the stronger fix. *Top open question — retire first.*
2. **OQ2 — `CanonicalTermSet` ownership seam.** Standalone canonical JSON (single-source-of-truth-data pattern) that C10/C15 vendor, vs generated into each linter's pack. Decide before T10 to fix the C07↔C10/C15 build dependency direction.
3. **Inventory-churn fragility (owner-pointer integrity, T7).** Owner-pointer integrity validates against [component-inventory](../_meta/component-inventory.md) C-IDs; if IDs split/merge (allowed in Track B), pointers dangle. De-risk by treating the C-ID set as a frozen contract input and failing the build loudly on a dangling pointer rather than silently dropping it.
4. **OQ3 — term authorship under self-bootstrap (C52).** Once the factory authors its own components, new vocabulary can enter un-canonicalized. De-risk by deciding whether `RegisterTerm` is a mandatory bootstrap doc-step gate — relevant only at Batch-4 (C52), so noted-and-deferred, not on the sweep-1 critical path.

## 6. Definition of done

Per-component (ties to spec §8 acceptance):

- **DoD-1 Coverage (G06):** every load-bearing term in README/AI-CONTEXT (the ~13 Gas City + ~10 paradigm terms of spec §1) has exactly one `GlossaryEntry` with a non-empty definition and ≥1 valid `owning_components` C-ID; doc-term diff is empty (tooling-verified). [T4, T5, T11]
- **DoD-2 Overload resolution (G01/G02):** `CanonicalReading` entries exist for "layer" and "phase", each naming a pinned sense, ≥1 rejected sense, and a disambiguation rule; a doc using a rejected sense bare is flagged. [T2, T10]
- **DoD-3 Owner-pointer integrity:** every `owning_components` C-ID resolves against the component inventory; no dangling pointers (tooling-verified). [T7]
- **DoD-4 Single canonical reading:** registering a term with two live definitions and no `CanonicalReading` fails the build (negative test). [T7]
- **DoD-5 Lint-set wiring (F38/DELTA-04):** C10/C15 loading the exported `CanonicalTermSet` flag (a) an invented undefined term, (b) a deprecated alias past removal, (c) a bare rejected-sense use of an overloaded term. [T3, T10]
- **DoD-6 Alias monotonicity (DELTA-05):** deprecating a term keeps it resolving via `deprecated_by` until its named removal version (positive + boundary test). [T9]
- **DoD-7 Render fidelity:** the human Markdown glossary regenerates byte-deterministically from the registry source (single-source-of-truth golden test). [T8]

Per-task DoD: each task lands with the unit test for its acceptance bullet above and codes against the frozen §4 interfaces; no task is "done" until the contract it implements is unchanged from its freeze (or the change is propagated to all stub consumers).

Component is **done** when DoD-1…7 pass, the §4 schemas are frozen, the overloaded-term ledger pins "layer"/"phase", and at least one real downstream linter (C10 via `CanonicalTermSet`) consumes the export (the canonical integration check).
