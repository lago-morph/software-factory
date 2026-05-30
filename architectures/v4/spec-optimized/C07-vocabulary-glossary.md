# C07 — Vocabulary & glossary  (Spec, Track B)

> Source: AI-CONTEXT §3.2 (nine concepts), §3.3 (vocabulary translation table), §9 (gene-transfusion def by analogy), §3.4 (smallest-install term set); README Part 4 (Gas City terms used as load-bearing), Part 6 ("Layer"/"Phase" usage), Part 3 (three-layer architecture); F-MODE-COVERAGE F38 (vocabulary lint debt); v3 build guide [`01-vocabulary.md`](../../v3/build-guide/01-vocabulary.md) (corpus-name canon + v3-jargon translation table); _meta gaps [G06](../_meta/ambiguities-and-gaps.md) (primary), [G01](../_meta/ambiguities-and-gaps.md) ("layer" overload), [G02](../_meta/ambiguities-and-gaps.md) ("phase" overload).
> Inventory ID: C07   Kind: cross-cutting   Status: sweep-1
> Deltas: DELTA-01 (glossary is an *authoritative machine-readable registry*, not a prose table), DELTA-02 (glossary granted authority to pin canonical readings of overloaded terms — resolves G01 "layer", G02 "phase"), DELTA-03 (every term carries a provenance/origin field + corpus-name mapping), DELTA-04 (vocabulary-lint hook feeds F38 / C10 / C15 with the canonical term set), DELTA-05 (deprecation/alias lifecycle for migration tail-risk), DELTA-06 (per-term "lock-in cost" + extraction-safe synonym so terms are recoverable, not a trap).

## 1. Purpose & responsibility

C07 is the **single source of truth for what every load-bearing term in Software Factory v4 means**. The v4 corpus uses ~13 Gas City / Gas Town terms (`city`, `rig`, `formula`, `molecule`, `pack`, `convoy`, `sling`, `wisp`, `order`, `wait`, `polecat`, `Mayor`, `Health Patrol`) plus ~10 paradigm terms (`spec`, `scenario`, `holdout`, `judge`, `satisfaction`, `digital twin`, `gene transfusion`, `bead`, `CXDB turn`, `model stylesheet`) as if defined, while the actual definitions are scattered, partial, or analogy-only (G06). C07 owns:

- a **canonical term registry**: one entry per term with a pinned definition, the v4 component(s) that own/realize it (by C-ID), its corpus/plain-name equivalent, and its provenance;
- **authority to pin a single canonical reading of overloaded terms** (DELTA-02) — most importantly the two conflicting senses of **"layer"** (G01) and **"phase"** (G02) — so downstream specs reference *one* meaning;
- a **canonical term list export** that the deterministic linters (C10 spec-linter, C15 workflow-linter) consume to detect undefined / off-canon / drifted vocabulary (F38, DELTA-04);
- the **alias / deprecation lifecycle** that absorbs Gas City's expected pack-schema and formula-format churn (AI-CONTEXT §3.5, DELTA-05) without breaking downstream references.

What it is **NOT**:
- **Not a definition author for the things themselves.** C07 does not define *how* a formula executes (C12) or *what* a bead schema contains (C20); it records the canonical *name and one-paragraph meaning* and **points at** the owning component as the authoritative depth source. C07 is the index and the term-arbiter, not the implementation spec.
- **Not a runtime component.** It produces a static, version-controlled data artifact + a lint-time check. It is not on any request path and holds no live state.
- **Not a translation/i18n layer.** "Translation" here means Gas-City-term → corpus-plain-name mapping (a cognitive-load mitigation), not human-language localization.
- **Not the linter.** C07 *supplies the canonical term set* to C10/C15; it does not itself implement EARS/Mammoth rules.

## 2. Context & dependencies

- **Depends on:** C01 (Gas City substrate — the source of the Gas City term family; C07 records, does not invent, those names). Soft dependency only: C07 is authored as a data artifact and does not call C01 at runtime.
- **Consumed by (broad fan-out — every component that uses a v4 term):** directly cross-referenced by the components that *own* each term — C01 (`city`), C02 (`pack`), C05 (`sling`, `wisp`), C06 (mail/nudge), C12 (`formula`), C13 (`molecule`), C18 (`Health Patrol`, `convergence gate`), C19/C20 (`bead`), C21/C22 (`CXDB turn`), C29 (`model stylesheet`), C40 (`order`/`convoy`), C42 (`rig`), C44 (`digital twin`), C51 (`gene transfusion`), C54 (`phase` — see DELTA-02/G02). Mechanically consumed by **C10** (spec linter) and **C15** (workflow linter) which import the canonical term set (DELTA-04).
- **Sits at:** a cross-cutting position in the Runtime Substrate. Foundational: every other spec should reference C07 for any term in its registry rather than re-defining it, so that the two-readings-of-"layer" class of bug (G01/G02) is structurally impossible.

## 3. Interfaces / contracts

Named-and-described (sweep 1; concrete schema + signatures in sweep 2).

**Outbound (the registry is read, never written at runtime)**
- `GlossaryEntry` — the canonical record per term: `{ term, canonical_definition, owning_components (C-ID[]), corpus_equivalent, provenance (DELTA-03), aliases, deprecated_by, lock_in_cost, extraction_safe_synonym (DELTA-06) }`.
- `CanonicalReading` (DELTA-02) — for an **overloaded** term, the pinned sense plus the *rejected* sense(s): `{ term, pinned_sense, disambiguation_rule, rejected_senses[], rename_recommendation }`. This is the authority artifact that resolves G01/G02. **Authority scope:** C07's binding authority is *pinning a canonical sense + flagging off-canon usage* (lintable). `rename_recommendation` is **advisory only** — an actual corpus-wide rename ("Layer N" → "principle tier N") touches C54/C57 and the AI-CONTEXT source docs, which C07 may not edit; that is an integrator/human cross-component decision (OQ1).
- `CanonicalTermSet` (DELTA-04) — the flat machine-readable export (term + accepted aliases + deprecated forms) that C10/C15 load to drive vocabulary-lint (F38). Stable, content-hashed, versioned.
- `CorpusTranslationTable` — the Gas-City-term → plain-corpus-name table (AI-CONTEXT §3.3 + v3 [`01-vocabulary.md`](../../v3/build-guide/01-vocabulary.md)), surfaced for human readers to mitigate the front-loaded lock-in cost (AI-CONTEXT §3.3 closing note).

**Inbound (authoring / maintenance, not runtime)**
- `RegisterTerm` / `DeprecateTerm` — the lifecycle operations a maintainer (or a future factory-built doc step) performs to add a term, retire one to an alias, or pin a reading. Validated against the uniqueness + single-owner invariants below.

**Invariants**
- **Term uniqueness:** each `term` appears exactly once in the registry; collisions are a build error.
- **Single canonical reading:** every term resolves to exactly one `canonical_definition`; an overloaded term MUST have a `CanonicalReading` pinning one sense and naming the rejected sense(s) (DELTA-02). A term with two live senses and no `CanonicalReading` fails the build.
- **Owner-pointer integrity:** every `owning_components` C-ID exists in the [component inventory](../_meta/component-inventory.md); C07 never *defines depth* for a term whose owner exists — it points there (no duplicated source of truth).
- **Alias monotonicity (DELTA-05):** a deprecated term keeps resolving (via `deprecated_by`) until a named removal version; aliases never silently disappear mid-cycle.
- **Lint-set completeness (DELTA-04):** every term in the registry appears in `CanonicalTermSet`; the linters can never be asked to accept a term the glossary doesn't carry.

## 4. Data model / state

C07's state is a **single version-controlled data artifact** (canonical machine-readable form + rendered human view), not a live store.

- **Registry file** — one `GlossaryEntry` per term. Canonical serialization is structured (TOML/JSON, sweep-2 picks); a rendered Markdown glossary is *generated* from it (single-source-of-truth: humans read the render, machines read the source).
- **Overloaded-term ledger** — the set of `CanonicalReading`s. Seeded at sweep-1 with the two known offenders:

  | Overloaded term | Pinned canonical sense (v4) | Rejected sense | Disambiguation rule |
  |---|---|---|---|
  | **"layer"** (G01) | The **convergent three-layer architecture**: (1) LLM client, (2) agent loop, (3) pipeline engine — *plus persistence* (README Part 3; v3 [`01-vocabulary.md`](../../v3/build-guide/01-vocabulary.md) "three-layer architecture"). | The "**Layer 0–6**" *principle-grouping* numbering (AI-CONTEXT §6/§7 "Layer 2–6 coverage", README Part 6 "Layer 2/5/6"). | When a doc means the principle-grouping, it MUST write **"Layer N"** (capital-L, numbered) and link C57's principle map; bare "layer" always means the three-layer architecture. Recommend renaming the numbered scheme to **"principle tier N"** (DELTA-02 rename_recommendation) to retire the overload. |
  | **"phase"** (G02) | The **four-phase delivery plan** P0→P1→P2→P3+ (README Part 6; owned by C54). There is **no enumerated Phase 4/5/6**. | **Pinned reading** (a decision, not a discovered fact): stray "Phase 6" (README:342) is a typo for the numbered "Layer 6" principle tier — the most v4-consistent reading of G02, which itself states the reference is genuinely ambiguous. | "Phase N" with N∈{0,1,2,3} = delivery plan (C54). Any "Phase ≥4" reference is off-canon and MUST be rewritten to "Layer N" (principle tier) **or flagged for human confirmation** — never silently rewritten, since G02 leaves a real ambiguity. |

- **No runtime mutable state.** Generations are git commits; the content hash of `CanonicalTermSet` is the version the linters pin against.

## 5. Behavior

Two flows; neither is a live control loop.

**Authoring / maintenance (human or factory doc-step):**
1. `RegisterTerm` adds/updates a `GlossaryEntry`; build validates uniqueness, owner-pointer integrity, and single-reading.
2. For an overloaded term, a `CanonicalReading` MUST accompany it or the build fails.
3. On Gas City churn (AI-CONTEXT §3.5), `DeprecateTerm` moves the old form to an alias with a `deprecated_by` pointer and a removal version (DELTA-05) — downstream refs keep resolving.
4. Build regenerates the human Markdown render and re-hashes `CanonicalTermSet`.

**Consumption (lint-time, mechanical):**
1. C10 (spec linter) / C15 (workflow linter) load the pinned `CanonicalTermSet` version.
2. They flag tokens that are undefined, off-canon (a rejected sense of an overloaded term used bare), or use a deprecated alias past its removal version — feeding F38 (DELTA-04).
3. Humans consume `CorpusTranslationTable` + the rendered glossary to pay down the front-loaded vocabulary cost.

(Sweep-2 will add a Mermaid showing registry → `CanonicalTermSet` → C10/C15 and the authoring-validation gate.)

## 6. Failure modes & handling

- **F38 (Vocabulary lint debt)** — *primary.* v4 marks F38 "Addressed" via "EARS-style spec linter… deterministically detectable" (F-MODE-COVERAGE), but a linter with no canonical term list can only check *form*, not *vocabulary correctness*. C07 supplies the missing input: the `CanonicalTermSet` (DELTA-04) is what makes "deterministically detectable" actually true. Without C07, F38's "Addressed" is hollow.
- **G06 (undefined load-bearing terms)** — *the gap this component exists for.* Mitigation: the registry forces a definition + owner-pointer for every term README/AI-CONTEXT uses; a term used in any v4 doc but absent from the registry is a lint failure (DELTA-04).
- **G01 / G02 (overloaded "layer"/"phase")** — Mitigation: the `CanonicalReading` ledger (DELTA-02) pins one sense and names the rejected sense; off-canon bare usage is lintable. This is the "Track B may give the glossary authority to pin canonical readings" mandate, exercised.
- **Lock-in / undefined-term debt (inventory one-liner)** — Mitigation (DELTA-06): every Gas City term carries an `extraction_safe_synonym` and a `lock_in_cost` note, so the vocabulary is *recoverable* (the runtime substrate stays swappable) rather than a one-way trap. Aligns with AI-CONTEXT §3.6's "tmux runtime is deliberately vocabulary-free" finding.
- **Definition drift / dual source of truth** — risk that C07 re-defines a term and drifts from its owning component. Mitigation: owner-pointer-integrity invariant — C07 stores a *one-paragraph canonical meaning + pointer*, never the authoritative depth, so the owner spec stays the single source for behavior.
- **Migration tail-risk churn (AI-CONTEXT §3.5)** — Gas City may rename terms 1–2×/quarter. Mitigation: alias/deprecation lifecycle (DELTA-05) absorbs renames without breaking the ~25 downstream cross-references at once.

## 7. Cross-cutting

- **Security:** none on the request path (no runtime surface). Indirect: pins the meaning of security-bearing terms (`rig`, `holdout`, `digital twin`, `isolation`) so C30/C34/C42/C43 don't drift on what they're enforcing.
- **Cost / cognitive load:** the dominant cost is *human* — vocabulary is "real cognitive cost but front-loaded and recoverable" (AI-CONTEXT §3.3). The `CorpusTranslationTable` + render is the explicit mitigation; per-term `lock_in_cost` (DELTA-06) makes the cost legible rather than hidden.
- **Scale:** O(terms) static artifact; no scaling concern. Lint cost is O(tokens) and already borne by C10/C15.
- **Observability / ops:** the registry is version-controlled; `CanonicalTermSet` is content-hashed so a spec can pin "validated against glossary vN". Glossary changes are diffable in git history.

## 8. Acceptance criteria & test strategy

1. **Coverage (G06):** every load-bearing term appearing in README/AI-CONTEXT (the ~13 Gas City + ~10 paradigm terms enumerated in §1) has exactly one `GlossaryEntry` with a non-empty definition and ≥1 valid `owning_components` C-ID. (Tooling-verified: enumerate doc terms, diff against registry, empty diff.)
2. **Overload resolution (G01/G02):** `CanonicalReading` entries exist for "layer" and "phase"; each names a pinned sense, ≥1 rejected sense, and a disambiguation rule. A doc using a rejected sense bare is flagged.
3. **Owner-pointer integrity:** every `owning_components` C-ID resolves against the [component inventory](../_meta/component-inventory.md); no dangling pointers (tooling-verified).
4. **Single canonical reading:** an attempt to register a term with two live definitions and no `CanonicalReading` fails the build (negative test).
5. **Lint-set wiring (F38/DELTA-04):** C10/C15 loading the exported `CanonicalTermSet` flag (a) an invented undefined term, (b) a deprecated alias past removal, (c) a bare rejected-sense use of an overloaded term.
6. **Alias monotonicity (DELTA-05):** deprecating a term keeps it resolving via `deprecated_by` until its named removal version (positive + boundary test).
7. **Render fidelity:** the human Markdown glossary regenerates byte-deterministically from the registry source (single-source-of-truth golden test).

## 9. Open questions

- **OQ1 (→ [review-log](../_meta/review-log.md)):** *Authority scope of DELTA-02.* The brief grants C07 authority to *pin* canonical readings — but does it have authority to mandate the **rename** ("Layer N" → "principle tier N") across the corpus, or only to flag off-canon usage? A rename touches C54, C57, AI-CONTEXT §6/§7 and is a cross-component edit; pinning-only is safer but leaves the ugly overload in place. *Top open question.*
- **OQ2:** Serialization + ownership seam — does the `CanonicalTermSet` export live as a standalone canonical JSON (single-source-of-truth-data pattern) that C10/C15 vendor, or is it generated into each linter's pack? Affects the C07↔C10/C15 build dependency.
- **OQ3:** Who authors new terms once the factory is self-bootstrapping (C52)? If factory-built components introduce vocabulary, the `RegisterTerm` gate must be part of the bootstrap doc-step or new terms enter un-canonicalized.
