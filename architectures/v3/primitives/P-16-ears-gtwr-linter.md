# P-16 — EARS + GtWR linter

**Claimed by.** [GF-C](../tracks/greenfield-cold-start-first.md) §1.1.2 (EARS-mandated Acceptance Criteria + deterministic GtWR R7/R8/R9 linter at the authoring boundary); [GF-S §1.S8 component](../tracks/greenfield-substrate-first.md) (guard #1 of the four-guard mediator runs the GtWR vocabulary lint set R7/R8/R9/R26/R35).

**Dispatch tier.** per-primitive (designed-system).

## Contract restatement

A deterministic rule engine that consumes a requirement statement (or small block) and emits a structured verdict: (a) which of the five EARS patterns ([`research/25`](../../../research/25-requirements-engineering-foundations.md) §2 — Ubiquitous / State-driven / Event-driven / Optional-feature / Unwanted-behaviour) the statement matches, with an explicit "no-pattern-match" verdict for prose that escapes the grammar; (b) per-rule pass/fail across the INCOSE GtWR R7–R35 rule set with citation to the violated rule ID, the offending span, and the rule's textual basis. The verdict is **deterministic** — same input + same rule-library version yields same output — distinguishing this primitive from any LLM-as-judge over the same surface (per F51) and per GF-C §1.1.2's explicit "deterministic perimeter, not LLM-judge" framing. The primitive blocks at the authoring boundary: a statement that fails the configured rule subset cannot enter the Cold-Start Bench or the downstream cycle input.

## Construction path

Build a **custom Python rule engine** layered on **spaCy** for tokenization / POS-tagging / dependency-parsing, with the rule library implemented as a registry of pure-function checkers — one function per GtWR rule, each returning `(rule_id, passed, span, message)`. **Integration sentence:** spaCy's `Doc`/`Span` objects and dependency-parse arcs (via `token.dep_` / `token.head`) supply exactly the linguistic structure the R7 vague-term check ("approximate," "as needed"), R8 escape-clause check ("if possible"), R9 open-ended-clause check ("etc."), R26 universal-quantifier check ("all"/"every"), and R35 absolute-statement check ("always"/"never") each need — lexicon lookup over lemmatized tokens for R7, constituent-pattern matches over dependency arcs for R8, POS-conditioned token matches for R26/R35. EARS pattern matching is **five regex/dependency templates** ("When `<trigger>`, the `<system>` shall `<response>`" → Event-driven; etc.) over the spaCy parse — readily pattern-matchable since EARS is literally a five-template grammar. Prior art for the construction shape: open-source requirements tooling such as **rmtoo** and **Doorstop** demonstrates that rule-engine + lexicon + dependency-parse is the standard build for requirements lint.

## Corpus-why citation

The load-bearing F-ids: **F38** ([`failure-modes-v3`](../failure-modes-v3.md) §4 — "AI-authored specs accumulate INCOSE GtWR R7/R8/R9 violations at rates well above human-authored specs because LLMs default to hedging language," greenfield severity `high`); **F18** (§1 — prose specs lack rigor, greenfield `high`); **F41** (§5a — under-defined-intent debt, greenfield `critical`); supports mitigation of **F36** (instruction-following ceiling, greenfield `critical`) and **F37** (silent contradictory-prompt collapse, greenfield `critical`) by ensuring the simultaneous-requirements input to the builder is well-formed before counting against the Yang ceiling. **Named section in GF-C:** [§1.1.2](../tracks/greenfield-cold-start-first.md) "EARS-mandated Acceptance Criteria" — explicitly identifies the GtWR linter as the F38 mitigation at the *authoring boundary* and as the F51 mitigation that avoids the LLM-judge-sycophancy trap at the same surface. GF-C §5 ("Bootstrap protection") names "deterministic perimeter at the authoring layer (against F38, F18, F51-greenfield-`high`)" as the **first of five** silent-failure protections — a cold-start architecture without this primitive cannot meet the GF-C threat model.

## Relationship to P-12 and P-15

**Can P-12 host P-16? Yes, with high confidence.** P-12 is defined as "rule-engine for deterministic per-cycle checks (separate primitive from the rule set itself)" ([index.md](index.md) row P-12); P-16 is precisely a specific rule library running on exactly that shape of engine. The construction path above (Python rule-function registry + spaCy parse + per-rule deterministic verdict) is engine-shape-identical to any deterministic linter P-12 would host. **Evidence:** GF-S §1.S8 already treats them as composed — the four-guard mediator (P-15) includes "GtWR vocabulary lint" (P-16's content) as guard #1, listed alongside contradiction-detector, requirement-count budgeter, and perimeter typing, all running on the same deterministic-check substrate (P-12's role). P-12 is the engine, P-16 is the rule library; the [index.md "Notes on numbering"](index.md#notes-on-numbering) collapse question is well-posed and construction-path evidence points toward **P-16-absorbs-into-P-12-as-rule-content**. **Relationship to P-15:** P-15 *consumes* P-16 as its first guard; P-16 is a *component* of P-15, not a sibling. Same-vs-distinct verdict deferred to Phase 4.2 per the scoping principle.

## Research-grade-uncertainty flag

`none` — EARS (Mavin) and INCOSE GtWR R7–R35 are publicly specified; spaCy + rule-function registry is a commodity construction shape.

## Buildability verdict

**`designed-system`** — engine is commodity; the **specific rule library** (which R7-R35 rules to implement, curated vague-term / escape-clause lexicons, EARS template patterns, threshold tuning) is the design content. Matches index.md's pre-tag.
