# P-27 — Archaeological-brief generation tooling

**Claimed by.** [BF-M §1.1 stage 2 (Comprehension)](../tracks/brownfield-methodology-first.md) — produces an "archaeological brief: what is here, how it works, what constraints it enforces, what the trigger touches" from code, tests, commits, traces, telemetry. Also BF-M §2.5's F21/F61 mitigation surface. **Related-to** [BF-L's scenario-derivation primitive](../tracks/brownfield-legacy-ingestion-first.md) — same construction shape, different output schema; same-vs-distinct deferred to Phase 4.2.

**Dispatch tier.** per-primitive (designed-system).

## Contract restatement

A tool that, given (a) a trigger and (b) read-access to the Codebase Model (P-26's six views), produces a typed **Brief** object consumed by BF-M Intent-capture (stage 3) and Plan (stage 4). Schema fields (minimal): `trigger_summary`; `touched_surfaces` (from P-22 + P-23); `blast_radius` (P-23 reverse-dependency closure scored by P-07 call-frequency); `enforced_constraints` (invariants / types / tests / lint in scope); `recent_history` (commits / authors / PRs over touched surfaces, from P-24); `runtime_observations` (P-07 traces / error rates where available); `open_questions`; `confidence_per_field`. The Brief is append-only-versioned; the PR body (BF-M stage 8) carries a pointer to the specific Brief version, satisfying F40 attribution.

## Construction path

Build with **Pydantic v2** for the Brief schema and **Anthropic structured outputs** (`tool_use` with strict JSON-schema-validated tool definitions) or **OpenAI structured outputs** (`response_format={'type':'json_schema', 'strict': true}`) as the generation surface. **Integration sentence:** the Brief root model's `model_json_schema()` export is passed verbatim as the `json_schema` argument to the model call, so the provider mechanically prevents emission of a Brief that fails Pydantic structural validation — collapsing the parse-retry loop ad-hoc prompt-extraction methods carry. The agent runs as a **tool-using loop** whose tools are read-only Codebase Model queries (`query_symbol`, `find_callers`, `recent_commits_touching`, `runtime_trace_for_endpoint`, `lint_rules_matching`) exposed via the [P-26 model-query interface](P-26-codebase-model.md); each tool returns typed substructures the model composes into the Brief. **LangExtract** (Google's structured-extraction toolkit) is a viable alternative over unstructured corpus text (commit messages, doc comments) — it specialises in source-grounded extraction with citation pointers, matching the brief's "every claim cites a Codebase Model query result" discipline. Per-section budgets are enforced via P-02; the loop is trajectory-captured via P-05.

## Per-candidate notes

Only **BF-M directly claims P-27**. BF-L names a *scenario-derivation* primitive with the same construction shape but different output schema (test scenarios for stage-7 acceptance, not a comprehension brief). Whether scenario-derivation and archaeological-brief collapse to one primitive with two schemas, or stay distinct, is a Phase-4.2 question — not rendered here.

## Corpus-why citation

**BF-M §1.1 stage 2** — Comprehension is a *named methodology obligation*; the cycle cannot advance without a brief. **F21 / F61** ([failure-modes-v3.md §2 / §5a](../failure-modes-v3.md)) — context-window exhaustion and multi-agent context fragmentation are the brownfield-critical failure modes the brief mitigates by *compressing* the codebase into a typed artifact downstream stages read instead of raw code. **F40 (last-mile drift)** — the brief-pointer in the PR body is part of the per-cycle attribution chain. **Own open question:** BF-M §7 names *stage-2 compression rules per work-unit-class* as unresolved — the brief schema must host `regression-fix` (narrow, deep) and `codebase-evolution-proposal` (broad, shallow) shapes without two schemas. **Prior-art:** [research/14 (El Kaim)](../../../research/14-el-kaim-book-intent-and-spec-authorship.md) §3 ships a 9-field intent block as a structured-authoring template; the Brief generalises that pattern from human-authored intent to LLM-authored, human-reviewable archaeology.

## Research-grade-uncertainty flag

`partial` — the **construction surface** is well-understood; the **brief-quality calibration problem** is open. No current substrate-resident technique deterministically distinguishes a "form-correct + substance-thin" brief (every field populated, but `enforced_constraints` missed the load-bearing invariant, or `blast_radius` under-counted by a hop) from a "form-correct + substance-rich" one. Plausible (unproven) calibration surfaces: (a) **hold-out-brief evaluation** — correlate stage-7 acceptance failures with brief omissions over N cycles; (b) **cross-family second-pass diff** — two distinct-family models each generate, structural diff surfaces blind spots; (c) **adversarial reviewer agent** with "find a load-bearing fact this brief missed" prompt. None is empirically validated in the corpus. The primitive ships without a quality-gate beyond structural validation; calibration is a Phase-5/8 problem.

## Buildability verdict

**`designed-system`** — LLM-with-structured-output is a well-understood construction shape (Pydantic + Anthropic/OpenAI structured-outputs APIs + tool-using loop). The design content is (a) the Brief schema's field decomposition + per-work-unit-class compression rules, (b) the Codebase Model query surface the brief-generation tools wrap, and (c) the brief-versioning + PR-attribution integration with BF-M stage 8. Brief-quality calibration is an open research problem flagged in the uncertainty section, not a buildability blocker — the *structural* contract is fully buildable today, mirroring P-17's structural-vs-substance split.
