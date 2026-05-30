# C07 — Vocabulary & Glossary  (Build Plan, Track A)

> Source / Spec ref: spec-faithful/C07-vocabulary-glossary.md
> Track: A (faithful)   Sweep: 1

## 1. Work breakdown

| ID | Task | Size | Prereqs |
|---|---|---|---|
| T1 | **Seed the canonical term set.** Extract every term from AI-CONTEXT §3.2 (nine concepts) + §3.3 (translation table) + the G06 list (README Part 4 load-bearing terms). Produce the master list. | S | spec §4.1 |
| T2 | **Define each term.** For every seeded term: canonical one-line definition, generic equivalent, provenance (Gas City runtime / corpus author / v4 convention), and pointer to the owning component spec where the deep definition lives. | M | T1 |
| T3 | **Resolve / flag collisions.** Walk the cross-term defects (G01 "layer", G02 "phase", and any same-word-two-meanings). For each: record both readings, pick the v4-consistent one *or* flag + defer to the owning doc per Track-A discipline. | M | T2 |
| T4 | **Choose registry shape + author it.** Ratify the TOML term-registry format (the [FAITHFUL-FILL]); write one entry per term with fields `term, definition, generic_equivalent, provenance, principles[], aliases[], status`. | M | T2, (coordinate C03) |
| T5 | **Generate the human-facing glossary doc** from the registry; make it the single artifact README links to (the G06 one-hop fix). | S | T4 |
| T6 | **Wire historical aliases.** Carry the v3 translation-table mappings (v3-pipeline jargon → plain name) and any deprecated terms as `aliases`/`status=deprecated` so older artifacts still resolve. | S | T4 |
| T7 | **Acceptance check.** Diff the C07 term set against (a) G06 list, (b) AI-CONTEXT §3.2/§3.3, (c) grep of README Part 4; close any gaps. Verify one-meaning-per-term and provenance-recorded invariants. | S | T4, T5 |

## 2. Dependency graph

- **Upstream (must precede C07 freeze):** C01 (`gas-city-substrate`) supplies the runtime vocabulary
  C07 catalogs. C07 only needs C01's *term inventory* to be stable, not its implementation — so C07 can
  start as soon as the nine-concepts list is fixed (it already is, AI-CONTEXT §3.2).
- **Soft coordination:** C03 (`config-feature-flags`) for registry file conventions (T4); C18/C19/C20/
  C29/C40 own deep definitions C07 points to (T2) — C07 needs only their *names* settled, not their
  specs finished.
- **Downstream (build against C07):** C08, C09, C10, C12/C13, C15, C16, and all human docs.
- **Critical path:** T1 → T2 → T4 → T7. T3 (collision resolution) is the riskiest link and gates the
  "one meaning per term" invariant.

C07 is in **Batch 1 (foundational)** (component-inventory line 107): author in parallel with
C01/C02/C03 so the vocabulary is frozen before dependents build.

## 3. Parallelization

Within C07 the fan-out is small but real:
- **Stream A (definitions):** T1 → T2 — pure authoring against fixed v4 sources; no external blockers.
- **Stream B (registry mechanics):** T4 registry-format decision + skeleton can be drafted concurrently
  with Stream A using a stub term list, then filled once T2 lands.
- **Stream C (collision analysis):** T3 is independent research over G01/G02 and can run alongside A/B;
  it only merges into the registry at T4.

T5 (human doc generation) and T6 (alias wiring) are mechanical once T4 exists and can run together.

## 4. Interfaces-first / contract milestones

Freeze early so dependents can build against stubs:
1. **The canonical term list (T1 output)** — freeze first; C08/C09/C10 author against the term *names*
   immediately even before definitions are final.
2. **The registry schema (T4 fields)** — freeze second; linters (C10/C15/C16) code their vocab-check
   loader against the schema while entries are still being filled.
3. **The owning-component pointer convention (T2)** — agree that C07 holds the one-liner + a pointer,
   and the deep definition lives in the owning spec; prevents duplication and double-source drift.

## 5. Risks & de-risking order

| Risk | De-risk action (order) |
|---|---|
| **Term collisions (G01 layer / G02 phase) leave the glossary ambiguous** — highest uncertainty. | Spike T3 *first*, in parallel: produce the both-readings write-up and the recommended Track-A disposition (resolve vs defer) before the registry is filled. |
| **Registry format churn** with C03 (AI-CONTEXT §3.5 warns of breaking config/schema changes). | Ratify T4 format with C03 early; keep entries format-portable (flat fields) so a migration is mechanical. |
| **Definitions duplicate / drift from owning component specs** (C19 beads, C40 Orders, C29 stylesheet, C18 convergence). | Lock the "one-liner + pointer" convention (milestone 3) so C07 never becomes a second copy of the substrate. |
| **Incomplete G06 coverage** (a Part-4 term silently missing). | T7 grep-based diff against README Part 4 as a hard gate. |

## 6. Definition of done

**Per-component (ties to spec §8 acceptance):**
- DoD-1: Every G06 term + every AI-CONTEXT §3.2/§3.3 term present in C07 with definition + generic
  equivalent (spec AC-1, AC-2).
- DoD-2: One meaning per term; all collisions either resolved with a v4-consistent rationale or flagged
  + deferred to the owning doc (spec AC-3).
- DoD-3: Provenance recorded for every term (spec AC-4).
- DoD-4: Human glossary generated from the registry and linked from README such that a README-only
  reader resolves any Part-4 term in one hop (spec AC-5).
- DoD-5: Acceptance checklist (T7) passes: term-set diff against G06 list, §3.2/§3.3, and README Part 4
  grep shows no gaps.

**Per-task:** each T-task is done when its output artifact exists and passes the relevant invariant
check above; T7 is the integrating gate for the whole component.
