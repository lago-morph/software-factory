# ADR 0032: P-12 deterministic linter framework (with EARS+GtWR rule pack)

- **Status**: Accepted
- **Date**: 2026-05-25
- **Deciders**: lead agent (Phase 5 Wave 5.1b parallel fanout)

## Context

Three candidates claim P-12 as a load-bearing substrate primitive: [GF-S/S8](../../architectures/v3/tracks/greenfield-substrate-first.md) (linter framework as the deterministic substrate of the four-guard mediator P-15), [GF-C §1.1.2](../../architectures/v3/tracks/greenfield-cold-start-first.md) (EARS-mandated Acceptance Criteria with deterministic GtWR linting at the authoring boundary), and [BF-M stage 6](../../architectures/v3/tracks/brownfield-methodology-first.md) (F38 vocabulary-lint mitigation). The [P-12 buildability sketch](../../architectures/v3/primitives/cluster-C3.md#p-12--deterministic-linter-framework) verdicts the engine `commodity`; the [P-16 EARS+GtWR sketch](../../architectures/v3/primitives/P-16-ears-gtwr-linter.md) verdicts the rule library `designed-system`.

Per the [Phase-4.2 overlap analysis](../../architectures/v3/primitives/overlap.md#p-12--p-16--deterministic-linter-framework--earsgtwr-rule-library-absorption), **P-16 absorbs into P-12**: P-12 is the rule-engine framework (deterministic per-cycle checks); P-16 is a specific rule library (INCOSE R7–R35 + EARS pattern conformance) running on it. They are distinct artifacts at the engineering layer but not separable as substrate primitives — an engine without rule packs is non-functional; a rule pack without an engine is non-executable. This ADR covers the combined surface.

The forcing failure modes are [F38 (vocabulary lint debt)](../../architectures/v3/failure-modes-v3.md#f38--vocabulary-lint-debt) — greenfield `high`, "authoring-side and *deterministically detectable*" — and [F51 (Ashby-deficient probabilistic guard)](../../architectures/v3/failure-modes-v3.md), which motivates a *deterministic* perimeter rather than an LLM-as-judge over the same surface. F38 mitigation cannot be agent-discipline-dependent ([F53-fragile](../../architectures/v3/failure-modes-v3.md)) and must reject [F51](../../architectures/v3/failure-modes-v3.md) sycophancy by construction.

## Decision

**Build P-12 as a Tree-sitter-based deterministic rule-engine with a pluggable rule-pack loader supporting multiple rule packs per cycle.** The engine API surface is: (a) `register_pack(pack-id, rules[])` where each rule is a pure function `(ast-node, context) → violations[]`; (b) `lint(artifact, pack-ids[]) → {rule-id, severity, span, message}[]` running a single AST walk that dispatches to all registered rules across the named packs; (c) a severity-and-threshold layer that gates the cycle on configured violation counts and emits the typed violation envelope to [P-05 trajectory capture](../../architectures/v3/primitives/cluster-C2.md). The engine is rule-set-agnostic — same input + same rule-pack version yields the same output (closes [F51](../../architectures/v3/failure-modes-v3.md)).

**The default rule pack shipped with P-12 is the INCOSE GtWR R7–R35 + EARS-five-pattern subset** specified in the [P-16 sketch](../../architectures/v3/primitives/P-16-ears-gtwr-linter.md) (R7 vague-term lexicon, R8 escape-clause, R9 open-ended-clause, R26 universal-quantifier, R35 absolute-statement; plus five EARS-template dependency-parse matchers — Ubiquitous / State-driven / Event-driven / Optional-feature / Unwanted-behaviour). spaCy provides the linguistic structure (POS tags, dependency arcs) for the lexicon and pattern rules; Tree-sitter provides parsing for the surrounding structured artifact (intent blocks, EARS-formed acceptance criteria, change-intent prose, scenario manifests). Rule-packs are versioned alongside the engine so rule-edits are auditable.

**Which rule packs each candidate activates is methodology-layer content, not substrate.** This ADR fixes only the *framework* contract. Per [overlap.md §P-12↔P-16](../../architectures/v3/primitives/overlap.md#p-12--p-16--deterministic-linter-framework--earsgtwr-rule-library-absorption): GF-C names the full INCOSE R7–R35 + EARS subset; GF-S/S8 names the four-guard subset (GtWR lint + contradiction-detector + req-count budgeter + perimeter typing). Those candidate-specific selections are deferred to Wave-5.3 per-candidate ADRs.

## Alternatives considered

**B. Two distinct primitives — P-12 (engine) and P-16 (rule library) — with separate ADRs.** Initially carried this way through Phase 3.5. *Why rejected:* the [Phase-4.2 overlap verdict](../../architectures/v3/primitives/overlap.md#p-12--p-16--deterministic-linter-framework--earsgtwr-rule-library-absorption) found the engine and rule-pack non-separable as substrate primitives. The P-16 sketch's own §"Relationship to P-12" concedes "P-12 can host P-16, high confidence" and "the construction path … is engine-shape-identical to any deterministic linter P-12 would host." Separate ADRs invited drift on the loader-API contract and version-pinning discipline.

**C. PMD / SpotBugs / ESLint as the engine (compiled-language linters as substrate).** *Why rejected:* PMD/SpotBugs target Java/JVM bytecode; ESLint is JavaScript-specific. The artifacts P-12 lints (intent blocks, EARS-formed acceptance criteria, change-intent prose, scenario manifests) are *spec-level* and *polyglot*, not source code in a single language. Tree-sitter supplies polyglot parsing without per-language framework switching and is the prior art the [P-12 sketch](../../architectures/v3/primitives/cluster-C3.md#p-12--deterministic-linter-framework) explicitly cites.

**D. LLM-as-linter (judge model evaluates each requirement against R7–R35).** *Why rejected:* non-deterministic; rerun-flakes contradict [F38](../../architectures/v3/failure-modes-v3.md#f38--vocabulary-lint-debt)'s "deterministically detectable" property, and the LLM-judge surface is exactly what [F51 (Ashby-deficient probabilistic guard)](../../architectures/v3/failure-modes-v3.md) identifies as failure-prone for this class of check. GF-C §1.1.2 explicitly frames the linter as "deterministic perimeter, not LLM-judge."

## Consequences

**Easier:** F38 mitigation becomes substrate-enforced and uniform across all three claiming candidates. The rule-pack-loader interface means new rule packs (contradiction-detection, req-count budgeter, perimeter typing per GF-S/S8; future BF-M lints; per-candidate custom packs) compose without engine changes. Determinism closes the F51 sycophancy surface at the authoring boundary by construction.

**Harder:** Tree-sitter grammars for spec-level artifacts (EARS-formed acceptance criteria, change-intent prose) must be authored and maintained — Tree-sitter ships parsers for programming languages, not for these DSLs. Rule-pack versioning and the gate-threshold layer are an additional configuration surface methodology layers must specify.

**Explicitly NOT promising:** which rule packs activate per candidate, the rule-set selection within each pack, or threshold tuning. Those are methodology-layer decisions resolved in Wave-5.3 per-candidate ADRs (GF-C, GF-S, BF-M) deferred to next run per [auto-005 Round 2](../../architectures/v3/decisions/auto-005-phase-5-dispatch-shape.md).

## References

- [P-12 buildability sketch](../../architectures/v3/primitives/cluster-C3.md#p-12--deterministic-linter-framework) and [P-16 EARS+GtWR sketch](../../architectures/v3/primitives/P-16-ears-gtwr-linter.md)
- [Phase-4.2 overlap verdict on P-12 ↔ P-16 absorption](../../architectures/v3/primitives/overlap.md#p-12--p-16--deterministic-linter-framework--earsgtwr-rule-library-absorption)
- [F38 vocabulary lint debt](../../architectures/v3/failure-modes-v3.md#f38--vocabulary-lint-debt) and [F51 Ashby-deficient probabilistic guard](../../architectures/v3/failure-modes-v3.md)
- Substrate-requirements summaries citing P-12: [GF-S](../../architectures/v3/substrate-requirements/gf-s.md), [GF-C](../../architectures/v3/substrate-requirements/gf-c.md), [BF-M](../../architectures/v3/substrate-requirements/bf-m.md)
- [auto-005 Round 2 Phase-5 dispatch shape](../../architectures/v3/decisions/auto-005-phase-5-dispatch-shape.md) — Wave 5.1b common-ADR scope
