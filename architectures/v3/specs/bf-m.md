---
candidate: bf-m
candidate-name: Brownfield, Methodology-First
mandate-scope: brownfield
based-on-commit: c54daf1
based-on-date: 2026-05-26
mandate-fit:
  initial-spec: n/a
  refactor: brownfield
  mvp: n/a
  post-mvp-evolution: brownfield
  regression-fix: brownfield
---

# Architecture spec — BF-M (Brownfield, Methodology-First)

## §0 ADR-citation index

| ADR ID | Title | Layer | Variant of | Citing § |
|---|---|---|---|---|
| 0010 | P-01 Sandbox runtime | common-substrate | — | §2, §3 |
| 0011 | P-02 Cost ceilings | common-substrate | — | §2, §4 |
| 0012 | P-05 Trajectory capture | common-substrate | — | §2, §3, §4 |
| 0013 | P-06 Watchdog tiers | common-substrate | — | §2, §3, §4 |
| 0014 | P-07 Telemetry ingestor | common-substrate | — | §2, §3 |
| 0015 | P-08 Scenario storage with runner contract | designed-system-substrate | — | §2, §3, §4 |
| 0016 | P-14 Judge router | common-substrate | — | §2, §3 |
| 0017 | P-22 Polyglot codebase index | common-substrate | — | §2, §3 |
| 0018 | Discipline — bias guard | discipline | — | §4 |
| 0019 | Discipline — cognitive escrow | discipline | — | §4 |
| 0020 | Discipline — cost ceiling | discipline | — | §4 |
| 0021 | Discipline — holdout | discipline | — | §4 |
| 0022 | Discipline — honesty | discipline | — | §4 |
| 0023 | Discipline — knowledge promotion | discipline | — | §4 |
| 0024 | Discipline — regime classification | discipline | — | §4 |
| 0025 | Discipline — scoping | discipline | — | §4 |
| 0026 | Discipline — three-loop | discipline | — | §4 |
| 0027 | Discipline — trifecta closure | discipline | — | §4 |
| 0031 | P-23 Dependency-impact graph | common-substrate | — | §2, §3 |
| 0032 | P-12 Deterministic linter framework | common-substrate | — | §2, §3 |
| 0033 | P-25 CaMeL perimeter | 2-candidate-fold-substrate | — | §2, §3, §6 |
| 0034 | P-27 Archaeological-brief tooling | 2-candidate-fold-substrate | — | §2, §3, §6 |
| 0045 | P-03 Worktree isolation (BF-M orphan) | orphan-substrate | — | §2, §3 |
| 0046 | P-04 PR creator (BF-M orphan) | orphan-substrate | — | §2, §3 |

**Framework-ADR pairing annotation.** BF-M **does not claim** any of the four framework ADRs (0028 P-19, 0029 P-28, 0030 P-29, 0036 P-30) as substrate. Per [BF-M substrate-requirements §3](../substrate-requirements/bf-m.md): "**BF-M does not name any of P-28, P-29, P-30, or P-19** (the contested-primitive set whose fixed sub-section headers were required by [auto-004 Round 2 §3](../decisions/auto-004-phase-4-dispatch-shape.md))." Consequently no framework + per-variant ADR pair appears in §0, and the [AGENTS-MD-a9fb7b42f8 framework-scope discipline](../../../AGENTS.md#framework-adr-scope-boundary-discipline) does not bind. P-19 regime classification at the methodology layer (stage-1 work-unit-class typing) is **operator-authored decision-table content**, not a substrate primitive — see §3.

**2-candidate fold annotation.** ADR 0033 (P-25 CaMeL perimeter) is shared with BF-S; ADR 0034 (P-27 archaeological-brief tooling) is shared with BF-L. Per the [Phase-4.2 overlap.md verdict on P-27](../primitives/overlap.md#2-primitive-overlap-counts-by-candidate-coverage): same primitive, shared envelope, work-unit-class-parameterised per-section compression rule. Per ADR 0033: same `CaMeL.execute(plan_ast, capability_profile, policy)` contract across BF-S and BF-M.

## §1 Overview

**Mandate.** Brownfield-only by deliberate construction (per [§6 of the track file](../tracks/brownfield-methodology-first.md#6-what-this-track-is-not-trying-to-be) — "Not a unified architecture"). BF-M makes no greenfield claim; stages 2 (Comprehension) and 3 (change-intent rather than system-intent) are brownfield-defining by construction.

**Axis.** Methodology — specifically, **the per-cycle process is the architecture**. The 8-stage cycle (Trigger → Comprehension → Intent capture → Plan → Build → Cross-model review → Acceptance → Ship-or-escalate) is the load-bearing artifact; substrate primitives are **stage-attached capabilities** at boundaries, not a pre-decided platform.

**Entry-mode.** Brownfield only. Day-0 input is the pre-existing codebase + issue queue + runtime telemetry + production traces. Cold-start is N/A — stage 2 (Comprehension) is the brownfield analog of cold-start: the first cycle's archaeological brief covers more of the codebase than subsequent briefs because the knowledge store is empty.

**Methodology summary.** Substrate-light, methodology-heavy. Each cycle traverses the 8 named stages; stage-compression rules per work-unit-class (regression-fix may skip stage 4; codebase-evolution-proposal may loop stages 2-4) are operator-authored. Substrate vendors (Gas City / OpenHands / Codex / custom) are interchangeable at the boundaries the cycle declares. The architecture is *the cycle and its variations by work-unit-class*.

**Load-bearing claim.** **Archaeological brief tooling + worktree isolation + per-issue PR-creator coordination, composed as methodology-first brownfield.** The combination of [P-27 archaeological brief (ADR 0034)](../../../docs/adr/0034-p-27-archaeological-brief-tooling.md) at stage 2, [P-03 isolated worktree (ADR 0045)](../../../docs/adr/0045-p-03-worktree-isolation.md) at stage 5, and [P-04 structured-metadata PR creator (ADR 0046)](../../../docs/adr/0046-p-04-pr-creator.md) at stage 8 is the per-cycle methodological closure: comprehension is substrate-traceable, build is concurrency-safe, and re-entry is machine-readable. The cycle refuses to advance unless each stage's substrate capability is satisfied.

## §2 Substrate composition

BF-M is a high-primitive-count candidate (~13 substrate references per the [Phase-4.1 coverage row](../primitives/index.md#per-candidate-primitive-coverage-round-trip-check)) — mostly commodity, with designed-system anchors at P-25 and P-27. Per the [Phase-4.1 BF-M substrate-requirements summary](../substrate-requirements/bf-m.md): the high primitive-count is a *feature* of methodology-first under brownfield (each stage names what it needs at its boundary), not a substrate-bloat signal.

**Common substrate (commodity).** [P-01 sandbox runtime (ADR 0010)](../../../docs/adr/0010-p-01-sandbox-runtime.md) wraps stage 5 (Build) per-cycle. [P-02 cost ceilings (ADR 0011)](../../../docs/adr/0011-p-02-cost-ceilings.md) enforce per-cycle / per-work-unit-class budget caps per [D-5](../decisions-captured.md). [P-05 trajectory capture (ADR 0012)](../../../docs/adr/0012-p-05-trajectory-capture.md) records each cycle event; stage-8 PR body carries a trajectory pointer (the F42 cognitive-escrow re-entry surface). [P-06 watchdog tiers (ADR 0013)](../../../docs/adr/0013-p-06-watchdog-tiers.md) attach Daemon to every stage, Triage at stages 4/5/6, Patrol across cycles for F34/F54/F55/F57 drift. [P-22 polyglot codebase index (ADR 0017)](../../../docs/adr/0017-p-22-polyglot-codebase-index.md) is the stage-2 code-traversal substrate (single-tenant tree-sitter + per-language LSP federation + SQLite-FTS/DuckDB tier).

**Common substrate (designed-system).** [P-07 telemetry ingestor (ADR 0014)](../../../docs/adr/0014-p-07-telemetry-ingestor.md) provides stage-2 runtime-telemetry read with per-role ABAC filter (the load-bearing CTR-B5 / CTR-G2 inversion — telemetry-derived assertions feed stage-7 scenarios via P-27). [P-08 scenario storage with runner contract (ADR 0015)](../../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md) is consumed at stage 7 (Acceptance); per [Phase-4.2 verdict](../primitives/overlap.md#p-08--p-09--held-out-runner--scenario-storage-collapse), P-09 (held-out runner) absorbs into P-08's runner-API contract — BF-M's substrate-requirements §5 deferral is resolved by the absorption. [P-14 judge router (ADR 0016)](../../../docs/adr/0016-p-14-judge-router.md) provides stage-6 cross-family reviewer routing (F46 mitigation per CJ Hess `kevin/carl`). [P-23 dependency-impact graph (ADR 0031)](../../../docs/adr/0031-p-23-dependency-impact-graph.md) is consumed at stage 2 (blast-radius compute for the archaeological brief's `enforced_constraints` field). [P-12 deterministic linter framework (ADR 0032)](../../../docs/adr/0032-p-12-deterministic-linter-framework.md) runs at stage 6 (F38 mitigation) and stage 3 (GtWR R7/R8/R9 on the change-intent block).

**2-candidate-fold substrate (designed-system).** [P-25 CaMeL perimeter (ADR 0033)](../../../docs/adr/0033-p-25-camel-perimeter.md) wraps the stage-5 Build phase when the work-unit-class is in a `production-adjacent` regime. Per [overlap.md P-25 row](../primitives/overlap.md#2-primitive-overlap-counts-by-candidate-coverage): shared-by-2 (BF-S, BF-M), same `CaMeL.execute(plan_ast, capability_profile, policy)` contract. BF-M binds NORMAL vs STRICT mode as a per-work-unit-class config; bypass is substrate-logged and cannot be set by the agent under review (F53-resistant). Utility-tax calibration is partial-RG (see §6).

[P-27 archaeological-brief tooling (ADR 0034)](../../../docs/adr/0034-p-27-archaeological-brief-tooling.md) is **dual-use** at BF-M — stage-2 archaeological-brief generator AND stage-7 codebase-derived scenario extractor (the [Phase-4.1 coverage row](../primitives/index.md#per-candidate-primitive-coverage-round-trip-check) names P-27 twice against BF-M). Per [ADR 0034 verdict on the BF-M variant](../../../docs/adr/0034-p-27-archaeological-brief-tooling.md): tool-using LLM-judge synthesis loop over Git-blame + Glean-equivalent fact-store (for BF-M without P-26: the loop runs over P-22 + P-07 + P-24-equivalent attribution directly). The envelope carries three load-bearing sections: `introduction-cycle`, `intent-decay-log`, `contemporary-references`. The **per-section compression rule** is BF-M's work-unit-class parameterisation: `regression-fix` cycles get narrow + deep; `codebase-evolution-proposal` cycles get broad + shallow. Brief-quality calibration is partial-RG (see §6).

**Orphan substrate (BF-M-only).** [P-03 worktree isolation (ADR 0045)](../../../docs/adr/0045-p-03-worktree-isolation.md) provides stage-5 per-cycle isolation: ephemeral `git worktree add` checkouts rooted on a tmpfs-mounted directory, one worktree per cycle-id, torn down by a hook-driven cleanup on cycle end. F17 (parallel agents on shared dirs lose data) is substrate-enforced at stage 5. Per-cycle ref namespace (`refs/cycle/<id>/...`) prevents sibling-cycle branch collision; the P-04 PR creator promotes from this namespace at push time.

[P-04 PR creator (ADR 0046)](../../../docs/adr/0046-p-04-pr-creator.md) is the stage-8 authenticated egress: thin `gh` CLI wrapper invoked from the BF-M cycle harness, authenticated by a per-cycle GitHub App installation token issued at cycle boot, emitting a typed Pydantic PR-body block. Required fields: `cycle_id`, `agent_id`, `model_snapshot`, `trajectory_pointer`, `change_intent_block`, `archaeological_brief_pointer`, `acceptance_verdict`. Commit messages carry F14 attribution trailers. Credentials never enter the cycle's P-01 closure (token held harness-side, outside the closure). Non-GitHub forges (`glab` / `tea`) follow the same shape.

**X_UNM_B articulation.** **N/A (mandate-specific candidate; X_UNM_B does not apply).** BF-M is brownfield-only by construction per the [track file §6](../tracks/brownfield-methodology-first.md#6-what-this-track-is-not-trying-to-be); its stage-2 Comprehension is the brownfield-defining stage and presumes the existing codebase + runtime as primary inputs. There is no greenfield-codebase-model-acquisition gap to articulate.

## §3 Methodology shape

**Per-cycle loop.** Eight named methodology obligations, executed sequentially with declared stage-compression rules per work-unit-class. Per the [BF-M track §1.1](../tracks/brownfield-methodology-first.md#11-the-brownfield-cycle-the-architectural-primary-unit):

1. **Trigger.** External signal (issue / change-request / regression alert / dependency bump / scheduled patrol finding / operator-initiated proposal) converted into a typed **work-unit-class** declaration (`regression-fix` / `refactor` / `post-mvp-evolution` / `codebase-evolution-proposal` / `mvp-extension` per [DEC-2](../decisions-captured.md)). The cycle refuses to start if classification fails. Substrate: trigger inbox + classifier prompt + classification audit log. **P-19 framework is not claimed** — the classifier is operator-authored decision-table content at the methodology layer, not a substrate primitive. Per the [BF-M substrate-requirements summary §3](../substrate-requirements/bf-m.md): BF-M's `regime` is a stage-7-attached attribute (acceptance gate strictness scales with stakes), not a separate top-level concept.

2. **Comprehension.** Read the relevant codebase slice + tests + recent commits + production traces + runtime telemetry. Produce the **archaeological brief** ([P-27 (ADR 0034)](../../../docs/adr/0034-p-27-archaeological-brief-tooling.md)) consumed by downstream stages. Substrate: [P-22 codebase index (ADR 0017)](../../../docs/adr/0017-p-22-polyglot-codebase-index.md), [P-23 dependency graph (ADR 0031)](../../../docs/adr/0031-p-23-dependency-impact-graph.md), [P-07 telemetry ingestor (ADR 0014)](../../../docs/adr/0014-p-07-telemetry-ingestor.md), [P-05 trajectory capture (ADR 0012)](../../../docs/adr/0012-p-05-trajectory-capture.md) for the read itself.

3. **Intent capture.** Author the **change-intent block** (a contraction of El Kaim's 9-field intent to fit a per-PR change rather than a whole-system spec). Fields: rationale, invariants-to-preserve, observable acceptance, regression surface, blast radius, rollback plan. **Spec the change, not the system.** [P-12 deterministic linter (ADR 0032)](../../../docs/adr/0032-p-12-deterministic-linter-framework.md) runs GtWR R7/R8/R9 vocab lint + complexity-diagnosis check (F38, F39 mitigation). The cycle refuses to advance without a passing change-intent block.

4. **Plan.** N≥3 candidate plans with explicit trade-offs (Klaassen four-clause plan-prompt). Per-plan adversarial critic. Decompose only to the point intent-stability permits — F59 (premature decomposition) is the named hazard. The cycle MAY loop stages 2-4 before committing to a plan when the work-unit-class is `codebase-evolution-proposal`.

5. **Build.** Execute the selected plan against an isolated worktree via [P-03 (ADR 0045)](../../../docs/adr/0045-p-03-worktree-isolation.md). Builder agent has **no access to acceptance criteria withheld at stage 7** (D-4 holdout discipline, substrate-enforced). Sandbox: [P-01 (ADR 0010)](../../../docs/adr/0010-p-01-sandbox-runtime.md). Cost ceiling: [P-02 (ADR 0011)](../../../docs/adr/0011-p-02-cost-ceilings.md). Watchdog: [P-06 (ADR 0013)](../../../docs/adr/0013-p-06-watchdog-tiers.md). **CaMeL boundary**: when the work-unit-class is in a `production-adjacent` regime, [P-25 (ADR 0033)](../../../docs/adr/0033-p-25-camel-perimeter.md) wraps the build with capability-typed dataflow per the `CaMeL.execute(plan_ast, capability_profile, policy)` contract (F12 → F33 → F44 lethal-trifecta closure).

6. **Cross-model review.** Distinct-model reviewer (F46 mitigation per CJ Hess `kevin/carl`) checks the diff against the change-intent. Specialized critics for code-quality, security, conformance to existing-codebase conventions (Anthropic Auto-Review pattern). Substrate: [P-14 cross-family routing (ADR 0016)](../../../docs/adr/0016-p-14-judge-router.md), [P-12 deterministic linters (ADR 0032)](../../../docs/adr/0032-p-12-deterministic-linter-framework.md).

7. **Acceptance.** Held-out scenario set + existing test suite + deterministic linter pass + Ashby-aware deterministic perimeter check (F51 mitigation). **Brownfield-specifically:** scenarios MAY be drawn *from the codebase* per the D-2 challenge (CTR-B5 inversion) — production traces, existing integration tests, telemetry-derived assertions via [P-07 (ADR 0014)](../../../docs/adr/0014-p-07-telemetry-ingestor.md) + [P-27 (ADR 0034)](../../../docs/adr/0034-p-27-archaeological-brief-tooling.md)'s stage-7 codebase-derived scenario extractor. The holdout is the **unseen subset, not the out-of-tree subset**. Substrate: [P-08 scenario storage with runner contract (ADR 0015)](../../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md) — the runner-API is the absorbed-P-09 contract per [Phase-4.2 overlap.md](../primitives/overlap.md#p-08--p-09--held-out-runner--scenario-storage-collapse).

8. **Ship-or-escalate.** Either: open PR via [P-04 (ADR 0046)](../../../docs/adr/0046-p-04-pr-creator.md) with structured commit metadata (F14 attribution), with the change-intent + archaeological brief + trajectory pointer attached as PR body; or escalate to human under a declared trigger condition (regression severity > threshold; blast radius > policy; novel risk pattern; F56 stress-bypass detection). The PR body IS BF-M's F42 cognitive-escrow re-entry surface — machine-readable typed block, not operator-formatted convention.

**Vocabulary mapping (per [track §2.1](../tracks/brownfield-methodology-first.md#21-lights-out--l5-tension-brief-21-oq-b1)).** "Lights-out" maps to *per-stage human-out-of-loop*, not to L5. Stages 1-7 run lights-out for automation-eligible work-unit-classes; stage 8 may escalate. The mapping is **per-stage**, not whole-system — which dissolves CTR-A1 / CTR-H10 for BF-M.

**Work-unit polymorphism.** The cycle is work-unit-class-polymorphic per [DEC-2](../decisions-captured.md). Atelier-style triggers `regression-fix` + `post-mvp-evolution`; Refinery-style triggers `refactor` + `mvp-extension`; `codebase-evolution-proposal` is the third shape the v2 set lacked (the agent itself proposes the change after stage-2 comprehension surfaces an issue not in any queue). The cycle hosts all three; the variation is which stages compress and which expand. Stage-compression specification per work-unit-class is BF-M's own OQ-T1, carried to Phase 5/6 methodology spec (see §6).

**Distinctive methodology decisions.** Three:

- **Methodology cycle IS the architecture; substrate is downstream.** Substrate primitives are *stage-attached capabilities at boundaries* (vendor-deferred). Per [track §6](../tracks/brownfield-methodology-first.md#6-what-this-track-is-not-trying-to-be): "Not a substrate selection."
- **Tempting-wrong-hybrid (F52) explicitly forbidden architecturally.** Per [track §2.5](../tracks/brownfield-methodology-first.md#25-failure-mode-coverage-severity-by-stage): the cycle does NOT accrete deterministic wrappers around LLM stages; **deterministic checks live ONLY at stage 7 perimeter** where they belong. The architectural rejection of mid-pipe deterministic wrappers is load-bearing — it is what distinguishes BF-M from substrate-first brownfield candidates.
- **Stage obligations are substrate-enforced, not operator-voluntary.** Per [track §2.5 F53 row](../tracks/brownfield-methodology-first.md#25-failure-mode-coverage-severity-by-stage): *the cycle refuses to advance, not the operator refusing-to-skip*. Substrate enforces the air-gap (D-4 holdout); substrate emits the PR-body typed block (F14 / F42); substrate runs the perimeter check (F51).

## §4 Discipline binding

BF-M binds all 10 discipline ADRs (0018-0027). Per-discipline binding:

- **Bias guard ([ADR 0018](../../../docs/adr/0018-discipline-bias-guard.md)).** Bound at stage 6 cross-model review: [P-14 (ADR 0016)](../../../docs/adr/0016-p-14-judge-router.md) enforces cross-family routing for reviewer (F46). OQ-T2 (cross-model necessity under Anthropic same-model-fine finding) is methodology-layer, not substrate-contract — carried to §6.

- **Cognitive escrow ([ADR 0019](../../../docs/adr/0019-discipline-cognitive-escrow.md)).** Bound at stage 8: the PR body bundles change-intent + archaeological brief + trajectory pointer + failed-acceptance line as the typed re-entry surface ([P-04 (ADR 0046)](../../../docs/adr/0046-p-04-pr-creator.md)). Kahana's "fragile dependency" framing addressed structurally — re-entry is substrate-emitted typed block, not operator-formatted prose.

- **Cost ceiling ([ADR 0020](../../../docs/adr/0020-discipline-cost-ceiling.md)).** Bound at [P-02 (ADR 0011)](../../../docs/adr/0011-p-02-cost-ceilings.md) with per-work-unit-class parameterisation. CTR-E1 10× cost variance + CTR-E6 CaMeL ~7-point utility tax accepted as inputs to ceiling calibration; the ceiling itself is non-optional. Per-stage budgets enforced individually (e.g., P-27 brief-generation LLM-judge cost capped per-brief).

- **Holdout ([ADR 0021](../../../docs/adr/0021-discipline-holdout.md)).** Bound at stage 5 / stage 7 air-gap: builder agent at stage 5 has no access to acceptance set at stage 7. **Brownfield-redefined**: per the D-2 challenge, the holdout is the *unseen subset* of codebase-derived scenarios, not the out-of-tree subset. [P-08 (ADR 0015)](../../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md)'s partition-discipline + role-keyed access boundary enforces the unseen-subset air-gap substrate-side. Scenarios-from-codebase governance (own OQ-T4) is carried to §6.

- **Honesty ([ADR 0022](../../../docs/adr/0022-discipline-honesty.md)).** Bound at the PR-body schema ([ADR 0046](../../../docs/adr/0046-p-04-pr-creator.md)) — required fields (agent_id, model_snapshot, acceptance_verdict) cannot be omitted; F14 attribution is mechanical. The change-intent block's `rollback plan` field is the per-cycle honest-prospect declaration.

- **Knowledge promotion ([ADR 0023](../../../docs/adr/0023-discipline-knowledge-promotion.md)).** Bound at the [followup/11 four-way classification](../tracks/brownfield-methodology-first.md#12-what-sits-across-the-cycle-cross-cutting-not-pre-decided-substrate) + `kw:confidence` tagging. Stale-knowledge inversion (F8) is the *next reader's* per-write check, not a curator daemon's batch refresh — BF-M's deliberate choice per [track §7 OQ-9](../tracks/brownfield-methodology-first.md#7-open-questions-surfaced-by-this-track). Knowledge-curator placement is contested (CTR-H2 / CTR-H3) and carried to §6.

- **Regime classification ([ADR 0024](../../../docs/adr/0024-discipline-regime-classification.md)).** Bound at stage 1 (work-unit-class typing) + stage 7 (acceptance gate strictness). **BF-M does not claim the P-19 framework** — regime classification is operator-authored decision-table content at the methodology layer (the discipline contract requires a per-variant declaration only when a candidate claims the P-19 framework, which BF-M does not).

- **Scoping ([ADR 0025](../../../docs/adr/0025-discipline-scoping.md)).** Bound at stage 3 (change-intent block scopes the per-cycle work). Work-unit-class taxonomy governs stage compression. Premature decomposition (F59) is the named hazard at stage 4.

- **Three-loop ([ADR 0026](../../../docs/adr/0026-discipline-three-loop.md)).** Bound at the cycle's plan → work → review → compound loop. The "compound" step is materialised as Patrol-tier monitoring of cross-cycle drift (F34/F54/F55/F57) — meta-loop closure is substrate-enforced via [P-06 (ADR 0013)](../../../docs/adr/0013-p-06-watchdog-tiers.md), not operator-voluntary.

- **Trifecta closure ([ADR 0027](../../../docs/adr/0027-discipline-trifecta-closure.md)).** Bound at stage 5 [P-25 CaMeL boundary (ADR 0033)](../../../docs/adr/0033-p-25-camel-perimeter.md) when production-adjacent + stage 7 deterministic perimeter via [P-12 (ADR 0032)](../../../docs/adr/0032-p-12-deterministic-linter-framework.md). F12 → F33 → F44 cascade closed at the substrate by capability-typed dataflow; the model cannot bypass a capability check by being persuaded.

**Disciplines BF-M is silent on.** None — BF-M carries all 10. The four open methodology questions (OQ-T1 stage-compression, OQ-T2 cross-model review necessity, OQ-T3 CaMeL utility-tax acceptance, OQ-T4 scenarios-from-codebase governance) are methodology-layer carries to Phase 5/6/8, not discipline rejections.

## §5 Mandate fit

BF-M's mandate-fit YAML block (in frontmatter) restated per work-unit-class:

- **initial-spec: n/a.** BF-M is brownfield-only by construction (per [track §6](../tracks/brownfield-methodology-first.md#6-what-this-track-is-not-trying-to-be)). Initial-spec authoring presupposes greenfield (no prior codebase to read); BF-M's stage 2 (Comprehension) is the brownfield analog and presumes the codebase exists. **N/a, not silent** — the cycle's shape rejects this work-unit-class. Falsifying scenario: if an operator successfully ran BF-M's stages 2-3 (Comprehension → change-intent) against an empty repository, the brownfield-defining claim of stage 2 is wrong.

- **refactor: brownfield.** Refactoring is a canonical BF-M work-unit-class (Refinery-style trigger shape per [track §2.3](../tracks/brownfield-methodology-first.md#23-oq-b4-unit-of-work)). The change-intent block at stage 3 specs the refactor as a typed change against existing invariants; stage 7 acceptance uses codebase-derived scenarios (existing integration tests + telemetry assertions). Supporting substrate evidence: ADRs 0017 (P-22), 0031 (P-23), 0033 (P-25), 0034 (P-27), 0045 (P-03), 0046 (P-04). Falsifying scenario: if refactor cycles routinely fail at stage 2 because the archaeological brief misses load-bearing invariants (P-27 brief-quality calibration failure), BF-M's brownfield-refactor claim degrades.

- **mvp: n/a.** MVP authoring presupposes greenfield (cold-start; intent-block + accumulated tests). BF-M's stages 2-3 are brownfield-defining; greenfield analogs would require substituting them with a different shape (which is a different methodology). **N/a, not silent** — explicit out-of-scope per [track §6](../tracks/brownfield-methodology-first.md#6-what-this-track-is-not-trying-to-be) "Not a greenfield architecture." Falsifying scenario: if BF-M's 8-stage cycle successfully completed an end-to-end MVP authoring run with no pre-existing codebase, the stage-2-brownfield-defining claim is wrong.

- **post-mvp-evolution: brownfield.** Post-MVP cycles against an existing codebase are the BF-M canonical case. The codebase is the durable artifact (D-1 challenged-partial per [track §4](../tracks/brownfield-methodology-first.md#4-defaults-accepted-vs-challenged)); the change-intent block + archaeological brief + PR body are per-cycle artifacts. Supporting substrate evidence: full BF-M ADR set. Falsifying scenario: if post-MVP cycles on a thickened codebase trend toward stage-2 comprehension cost exceeding stage-5 build cost by >10× consistently, the methodology-first thesis (substrate is downstream) inverts and BF-M is structurally substrate-first.

- **regression-fix: brownfield.** Regression fixes are the BF-M-easiest cell to clear Jaymin's Automation Mode bars per [track §2.1](../tracks/brownfield-methodology-first.md#21-lights-out--l5-tension-brief-21-oq-b1) — the failing test IS the held-out acceptance. Stage-4 compression: `regression-fix` may skip stage 4's multi-plan generation or collapse it to N=1 (OQ-T1 specification carry). Supporting substrate evidence: ADRs 0015 (P-08), 0045 (P-03), 0046 (P-04). Falsifying scenario: if regression-fix cycles on BF-M routinely require human escalation at stage 8 (not the L4-by-design rate), the per-(work-unit-class × stage) Automation-Mode bar-clearance claim against Jaymin's ~L3 ceiling (CTR-A5) is wrong.

**DEC-1.a falsifier-discipline observation.** BF-M claims `brownfield` (not `both`) on all 3 non-n/a cells. Per [DEC-1.a](../decisions-captured.md), this is *consistent* with the no-methodology-serves-both-mandates working hypothesis — BF-M's affirmative brownfield-shape is the deliberate construction. Two `n/a` cells (initial-spec, mvp) are not silence but explicit out-of-scope rejections with stated rationale.

## §6 Open carries

Surfaced into Phase 7 (back-fill) / Phase 8 (lean-eval) / future ADRs:

- **OQ-T1: Stage-compression rules per work-unit-class (Phase-5/6 methodology spec).** The cycle declares stages compress/expand by class, but the rules are sketched not specified. Does `regression-fix` truly skip stage 4, or merely collapse it to N=1? Is `codebase-evolution-proposal`'s stage-2-3-4 loop bounded? Carried per [track §7 OQ-1](../tracks/brownfield-methodology-first.md#7-open-questions-surfaced-by-this-track).

- **OQ-T2: Cross-model review necessity under CTR-D7/CTR-D8 (Phase-5 ADR / Phase-8 lean-eval).** Husain/Shankar's "same-model judging is fine when task differs" empirically contradicts stage-6 cross-family insistence. BF-M took the F46 side; necessity-vs-contingent unresolved. Status: Phase-8 pressure-test of cross-family routing policy.

- **OQ-T3: CaMeL utility-tax acceptance criterion (Phase-5 ADR + Phase-8 lean-eval).** [ADR 0033](../../../docs/adr/0033-p-25-camel-perimeter.md) accepts the ~7-point utility tax as structurally non-zero; per-deployment acceptance criterion is required. Per [BF-M substrate-requirements §2](../substrate-requirements/bf-m.md#2-rg-primitives) **partial-RG accepted-as-RG choice (b)**: the substrate exposes per-class bypass with audit-log; the acceptance criterion is per-deployment measurement (Phase-5 production-adjacency-policy ADR + Phase-8 realized-tax measurement).

- **OQ-T4: Scenarios-from-codebase governance (Phase-3 / Phase-5).** D-2 challenge inverts holdout-location (unseen subset, not out-of-tree) but does not specify how the unseen subset is selected from a codebase-derived pool without leaking. Status: Phase-5 carry.

- **P-27 brief-quality calibration (Phase-5/8 RG carry).** Per [ADR 0034](../../../docs/adr/0034-p-27-archaeological-brief-tooling.md) and [BF-M substrate-requirements §2](../substrate-requirements/bf-m.md#2-rg-primitives): three plausible calibration approaches in the sketch, none empirically validated. **Partial-RG accepted-as-RG choice (b)**: substrate exposes brief-quality metrics + gating thresholds as first-class parameters so Phase-8 sweeps are tractable. Status: Phase-8 lean-eval candidate.

- **OQ-T6 brownfield regime ceiling measurability (Phase-8 lean-eval).** Per [track §2.1 / §7 OQ-6](../tracks/brownfield-methodology-first.md#21-lights-out--l5-tension-brief-21-oq-b1): does per-(work-unit-class × stage) Automation-Mode bar clearance contest Jaymin's brownfield ~L3 ceiling? Measurement protocol not specified.

- **OQ-T10 / F36 instruction-following ceiling vs change-intent block size (Phase-8 lean-eval).** Stage 3 caps simultaneous requirements per change, but refusal criterion when change-intent grows past 10-20 specified requirements is unspecified. Per [track §7 OQ-10](../tracks/brownfield-methodology-first.md#7-open-questions-surfaced-by-this-track).

- **OQ-8 Anthropic Skills network-closure vs Patrol "dreaming" (Phase-5 ADR).** Stage 2 and Patrol arguably need overnight-research style "dreaming"; if substrate vendor closes network at Skill layer, Comprehension and Patrol need different mechanism. Status: Phase-5 carry.

## §7 References

**ADR set (this spec's binding inputs).** Per the §0 ADR-citation index above; relative paths under `../../../docs/adr/`:

- Common substrate: [ADR 0010](../../../docs/adr/0010-p-01-sandbox-runtime.md), [ADR 0011](../../../docs/adr/0011-p-02-cost-ceilings.md), [ADR 0012](../../../docs/adr/0012-p-05-trajectory-capture.md), [ADR 0013](../../../docs/adr/0013-p-06-watchdog-tiers.md), [ADR 0014](../../../docs/adr/0014-p-07-telemetry-ingestor.md), [ADR 0015](../../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md), [ADR 0016](../../../docs/adr/0016-p-14-judge-router.md), [ADR 0017](../../../docs/adr/0017-p-22-polyglot-codebase-index.md).
- Designed-system common substrate: [ADR 0031 (P-23)](../../../docs/adr/0031-p-23-dependency-impact-graph.md), [ADR 0032 (P-12)](../../../docs/adr/0032-p-12-deterministic-linter-framework.md).
- 2-candidate-fold substrate: [ADR 0033 (P-25 CaMeL, BF-S+BF-M)](../../../docs/adr/0033-p-25-camel-perimeter.md), [ADR 0034 (P-27 archaeological-brief, BF-M+BF-L)](../../../docs/adr/0034-p-27-archaeological-brief-tooling.md).
- Orphan substrate (BF-M-only): [ADR 0045 (P-03 worktree isolation)](../../../docs/adr/0045-p-03-worktree-isolation.md), [ADR 0046 (P-04 PR creator)](../../../docs/adr/0046-p-04-pr-creator.md).
- Discipline: [ADR 0018](../../../docs/adr/0018-discipline-bias-guard.md), [ADR 0019](../../../docs/adr/0019-discipline-cognitive-escrow.md), [ADR 0020](../../../docs/adr/0020-discipline-cost-ceiling.md), [ADR 0021](../../../docs/adr/0021-discipline-holdout.md), [ADR 0022](../../../docs/adr/0022-discipline-honesty.md), [ADR 0023](../../../docs/adr/0023-discipline-knowledge-promotion.md), [ADR 0024](../../../docs/adr/0024-discipline-regime-classification.md), [ADR 0025](../../../docs/adr/0025-discipline-scoping.md), [ADR 0026](../../../docs/adr/0026-discipline-three-loop.md), [ADR 0027](../../../docs/adr/0027-discipline-trifecta-closure.md).

**Supporting docs:**

- [BF-M candidate-registry entry](../candidate-registry.md#bf-m--brownfield-methodology-first-1)
- [BF-M substrate-requirements summary](../substrate-requirements/bf-m.md)
- [Brownfield-methodology-first track sketch](../tracks/brownfield-methodology-first.md)
- [Phase-4.2 overlap.md — P-08↔P-09 collapse + P-25/P-27 shared-by-2 rows](../primitives/overlap.md)
- [DEC-1.a unification-verdict working hypothesis](../decisions-captured.md)
- [DEC-2 mandate-fit-per-(architecture × work-unit-class)](../decisions-captured.md)
- [auto-006 Phase-6 dispatch-shape brief](../decisions/auto-006-phase-6-dispatch-shape.md) — this spec authored under the Round-2 rubric.
