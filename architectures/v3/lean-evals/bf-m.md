---
based-on-spec-commit: c54daf1
based-on-backfill-commit: cbb109f
based-on-date: 2026-05-28
candidate-tier: Heavy
candidate-mandate: brownfield
scenario-set-source: hybrid
mandate-scenario-split:
  greenfield: 0
  brownfield: 6
expected-evaluator-time-days: 1
falsifying-outcome: |
  Across 6 medium-codebase brownfield scenarios (50k-250k LOC, ≥3 languages,
  ≥18 months commit history), BF-M's P-27 archaeological brief misses ≥1
  load-bearing invariant per scenario in ≥4 of 6 scenarios, measured as
  stage-6/7 review-or-acceptance failures attributable to brief omission
  via the `archaeological_brief_pointer` trace in
  `solutions/audit/p-27-briefs/<cycle-id>.json`. Equivalently: brief-recall
  MCC ≤0.55 against the labeled invariant ground-truth set.
phase-7-cite-obligations:
  high-confidence-mandatory:
    - compound-engineering-4-step-loop-archive-cite
    - 4-architecture-taxonomy-archive-cite
  medium-confidence-design-inputs:
    - audit-silent-absorption.md-§B.1-row-6-bf-m-stage-6-reviewer-panel
    - audit-silent-absorption.md-§B.1-row-11-bf-m-klaassen-four-clause
  historian-design-inputs: []
---

# Lean-eval brief — BF-M (Brownfield, Methodology-First)

This brief is the Wave-8.1 per-candidate lean-eval for BF-M, the brownfield-mandate methodology-first candidate at the **medium-codebase** tier (between BF-S small and BF-L large). Per [`auto-008 §Decision (Round 2)`](../decisions/auto-008-phase-8-dispatch-shape.md#decision-round-2), the brief follows the §1-§8 rubric with the mandatory `falsifying-outcome:` YAML field + §3 falsifying-outcome verbatim discipline + Phase-7 cite-obligation honoring. BF-M is Heavy tier (word budget 5500-7200) per its multi-lineage profile (Atelier + Foundry hybrid + Refinery secondary on the change-intent surface) and its 2 high-confidence cite-obligation surface (Compound-Engineering 4-step loop + 4-architecture taxonomy).

## §1 Candidate + scenario set

**Candidate.** BF-M is the brownfield-mandate-only methodology-first candidate (brownfield-heavy tier in [`auto-008` tier-table](../decisions/auto-008-phase-8-dispatch-shape.md#decision-round-2)) targeting the **medium-codebase** complexity wager. Per [`specs/bf-m.md §1`](../specs/bf-m.md#1-overview): the per-cycle 8-stage methodology (Trigger → Comprehension → Intent capture → Plan → Build → Cross-model review → Acceptance → Ship-or-escalate) *is* the architecture; substrate primitives are stage-attached capabilities at boundaries (vendor-deferred). Day-0 entry-mode: brownfield only — a pre-existing codebase + issue queue + runtime telemetry + production traces. Stage 2 (Comprehension) is the brownfield-defining stage; cold-start is N/A. Per [`specs/bf-m.md §5`](../specs/bf-m.md#5-mandate-fit): `initial-spec: n/a`, `mvp: n/a`, `refactor: brownfield`, `post-mvp-evolution: brownfield`, `regression-fix: brownfield`. BF-M's `candidate-mandate: brownfield` and `mandate-scenario-split: {greenfield: 0, brownfield: 6}` per the YAML frontmatter — BF-M does NOT carry the DEC-1.a unified-attempt load, so the scenario set is single-bloc (brownfield-only) and the "pass cleanly" definition uses the non-unified-candidate form (≥80% scenarios pass + falsifying-outcome NOT triggered) per [`auto-008 §Falsifier discipline (R2 #3)`](../decisions/auto-008-phase-8-dispatch-shape.md#falsifier-discipline-load-bearing).

**Medium-codebase distinctive wager.** Between BF-S (small) and BF-L (large), BF-M's medium-codebase positioning is the load-bearing tier: a codebase large enough that **archaeological-brief quality** (P-27 [ADR 0034](../../docs/adr/0034-p-27-archaeological-brief-tooling.md)) becomes the bottleneck (BF-S's small codebase can be read directly; BF-L's large codebase requires Pulse-style production-trace-to-spec-amendment per [aggregation §4.1 H-3](../backfill-notes.md#41-load-bearing-gaps-5--phase-8-lean-eval-inputs)). BF-M's wager: the per-section compression rule (`introduction-cycle` + `intent-decay-log` + `contemporary-references` per work-unit-class) + the LLM-judge synthesis loop over P-22 + P-07 + P-24-equivalent attribution suffices to surface load-bearing invariants at medium-codebase scale without the Pulse-style infrastructure BF-L requires.

**Fixture-scale rationale.** The 50k-250k LOC bound is chosen at the lower-bound where direct codebase read (BF-S's assumed entry-mode) becomes infeasible — ~50k LOC is roughly the threshold where a human engineer or a single-context LLM cannot hold the codebase coherently without summarization — and at the upper-bound where Pulse-style production-trace ingestion is not yet structurally required for routine cycles (~250k LOC is roughly the threshold where production-trace-derived spec amendments become the dominant signal source, per [aggregation §4.1 H-3](../backfill-notes.md#41-load-bearing-gaps-5--phase-8-lean-eval-inputs)). The ≥3 languages constraint matches P-22's polyglot framing (tree-sitter + per-language LSP federation per [ADR 0017](../../docs/adr/0017-p-22-polyglot-codebase-index.md)); a single-language fixture would let a less-sophisticated codebase index pass, masking P-22's structural value. The ≥18 months commit history is the floor at which the `intent-decay-log` section of the P-27 brief has enough material to be meaningful (a fresh codebase has no decay to log).

**Scenario set source.** Hybrid: scenarios drawn from (a) the corpus F-mode catalog focused on F8 (stale knowledge), F14 (attribution collapse), F17 (parallel-agents-shared-dirs), F33-F44 (lethal trifecta cascade), F38 (deterministic-linter coverage), F46 (single-model review blindspot), F52 (tempting-wrong-hybrid), F53 (substrate-enforced stage refusal), F59 (premature decomposition) — i.e., the failure modes BF-M's 8-stage cycle + P-27 brief + P-03 worktree + P-04 PR-creator + P-25 CaMeL boundary explicitly mitigate — and (b) BF-M's own scenario-derivation primitive at [`specs/bf-m.md §3 stage 7`](../specs/bf-m.md#3-methodology-shape) (codebase-derived scenarios via [P-07 telemetry (ADR 0014)](../../docs/adr/0014-p-07-telemetry-ingestor.md) + [P-27 archaeological-brief tooling (ADR 0034)](../../docs/adr/0034-p-27-archaeological-brief-tooling.md)'s stage-7 codebase-derived scenario extractor — the CTR-B5/CTR-G2 inversion). The two halves are not redundant: corpus scenarios provide F-mode coverage and adversarial pressure; codebase-derived scenarios surface what the methodology's own design predicts for medium-codebase brownfield.

**Scenarios (6 total, all brownfield, all medium-codebase: 50k-250k LOC, ≥3 languages, ≥18 months commit history).**

1. **Regression-fix on a medium-codebase familiar-module (corpus F38 + candidate-derived).** Operator queues a regression bug in a frequently-touched module (≥10 prior commits in last 18 months). Evaluator runs the BF-M cycle stages 1-8; verifies stage-2 archaeological brief surfaces load-bearing invariants from the failing test + recent commits; stage-3 change-intent block captures rationale/invariants/acceptance/regression/blast/rollback; stage-4 may collapse N=1 candidate plan (regression-fix compression per [`specs/bf-m.md §5 regression-fix`](../specs/bf-m.md#5-mandate-fit)); stage-5 builds in P-03 worktree; stage-6 cross-model reviewer (P-14 cross-family); stage-7 acceptance against unseen subset of codebase-derived scenarios + failing test. Surfaces: F38 (deterministic-linter coverage), F46 (cross-model review). Pass: cycle reaches stage-8 PR open with typed body in ≤cost-ceiling; ≥1 codebase-derived scenario from `intent-decay-log` passes the unseen-subset gate. **Implements DEC-2 work-unit class `regression-fix`.**

2. **P-27 archaeological-brief invariant recall (corpus F8 + candidate-derived; load-bearing).** Evaluator constructs 5 seeded "load-bearing-invariant" scenarios on a medium-codebase fixture (each invariant a property the codebase enforces silently — e.g., a serialization ordering, an idempotency guarantee, a rate-limit floor). For each scenario, BF-M's stage-2 P-27 brief is generated and scored: did the brief's `enforced_constraints` field include the load-bearing invariant? **This is BF-M's load-bearing falsifier scenario** (see §3). Pass: brief-recall ≥80% across 5 invariants (≥4 of 5 surfaced); brief-recall MCC > 0.55 against the labeled ground-truth invariant set.

3. **Codebase-evolution-proposal stages 2-4 loop (candidate-derived OQ-T1).** Evaluator runs a `codebase-evolution-proposal` work-unit-class cycle where the agent itself proposes a refactor after stage-2 surfaces an issue not in any queue. Verifies stages 2-4 loop is bounded (does the loop terminate within ≤3 iterations?) + stage-compression rules per [`specs/bf-m.md §3 work-unit polymorphism`](../specs/bf-m.md#3-methodology-shape) are operationally applicable. Surfaces: F59 (premature decomposition), F25 (design starvation as a regime property). Pass: loop terminates ≤3 iterations; stage-compression decisions are mechanically reconstructable from cycle harness state, not operator-asserted.

4. **Stage-6 cross-model review panel (corpus F46 + CTR-D7 contradiction; OQ-T2).** Evaluator runs ≥3 cycles where the stage-6 cross-model reviewer panel (P-14 cross-family + specialized critics for code-quality, security, conformance to existing-codebase conventions per [`specs/bf-m.md §3 stage 6`](../specs/bf-m.md#3-methodology-shape) — the Anthropic Auto-Review pattern absorbed silently from `02-compound-atelier.md §4.3` per [`audit-silent-absorption.md §B.1 row 6`](../backfill-notes/audit-silent-absorption.md)) is compared against a same-model baseline; tests the CTR-D7 same-model-review contradiction BF-M takes on the F46-defensible grounds. Surfaces: F46, F55 (behavioural drift). Pass: cross-model panel catches ≥1 contradiction class same-model misses across 3 cycles; reviewer panel does not silently collapse to a single voice (verified via P-14 routing trace).

5. **Stage-5 CaMeL boundary + cost-ceiling interaction (corpus F12/F33/F44 + CTR-E6 + OQ-T3).** Evaluator runs ≥3 cycles where the work-unit-class is `production-adjacent` (triggering [P-25 CaMeL perimeter (ADR 0033)](../../docs/adr/0033-p-25-camel-perimeter.md) wrap at stage 5); measures whether the ~7-point CaMeL utility tax + D-5 cost ceilings interact catastrophically (premature ceiling hits) or admit-as-non-zero per BF-M's [`specs/bf-m.md §4 cost-ceiling binding`](../specs/bf-m.md#4-discipline-binding) ("CTR-E6 ~7-point utility tax accepted as inputs to ceiling calibration; the ceiling itself is non-optional"). Surfaces: F12 → F33 → F44 lethal-trifecta cascade closure (per `specs/bf-m.md §4 trifecta-closure` binding); CTR-E1 10× cost-range; F53 (substrate-enforced stage refusal). Pass: ≥80% of cycles complete within budget; F12/F33/F44 cascade is substrate-closed (no model-persuadable capability bypass observed in P-25 audit logs); bypass-attempt events surface in trajectory as explicit `capability-bypass-rejected` events.

6. **Parallel-cycle worktree isolation + PR-creator coordination (corpus F17 + F14 + candidate-derived).** Evaluator runs ≥3 cycles concurrently on the same medium-codebase fixture, each on a different work-unit. Verifies [P-03 worktree isolation (ADR 0045 orphan)](../../docs/adr/0045-p-03-worktree-isolation.md) substrate-closes F17 (no cross-cycle data loss; per-cycle ref namespace `refs/cycle/<id>/...` prevents branch collision); verifies [P-04 PR creator (ADR 0046 orphan)](../../docs/adr/0046-p-04-pr-creator.md) emits required-fields-complete typed Pydantic PR bodies for all 3 concurrent cycles (F14 attribution mechanical); verifies stage-8 trajectory pointers are machine-readable per [`specs/bf-m.md §3 stage 8`](../specs/bf-m.md#3-methodology-shape) F42 cognitive-escrow re-entry surface. Surfaces: F17, F14, F42, F53. Pass: 3 concurrent cycles complete with 0 cross-cycle data corruption; 3 PR bodies validate against the Pydantic schema (required `cycle_id` + `agent_id` + `model_snapshot` + `trajectory_pointer` + `change_intent_block` + `archaeological_brief_pointer` + `acceptance_verdict` fields all populated); P-04 token never enters P-01 closure (verified via P-01 audit log).

The 6 scenarios cover BF-M's 3 mandate-fit work-unit-classes (refactor via #3+#6; post-mvp-evolution via #3+#5; regression-fix via #1+#2) and pressure-test BF-M's load-bearing claims (P-27 brief quality at #2 — the load-bearing falsifier; P-03 worktree isolation at #6; P-04 PR-creator at #6; P-25 CaMeL boundary at #5; cross-model review at #4; stage-compression at #3).

**Why these 6 scenarios (scenario-selection rationale).** BF-M's spec carries 8 open carries at [`specs/bf-m.md §6`](../specs/bf-m.md#6-open-carries) (OQ-T1 stage-compression rules per work-unit-class; OQ-T2 cross-model review necessity under CTR-D7/D8; OQ-T3 CaMeL utility-tax acceptance criterion; OQ-T4 scenarios-from-codebase governance; P-27 brief-quality calibration; OQ-T6 brownfield regime ceiling measurability; OQ-T10/F36 instruction-following ceiling vs change-intent block size; OQ-8 Anthropic Skills network-closure vs Patrol dreaming). The lean-eval's 6-scenario set engages 6 of the 8 (OQ-T1/T2/T3/T4 + P-27 brief-quality + OQ-T10 — see [§6 Open critique references](#6-open-critique-references)) while keeping the 1-day evaluator-time bound. Scenario selection prioritized (a) BF-M's load-bearing wager (P-27 archaeological-brief invariant recall at medium-codebase scale → scenario #2 is the §3 falsifying-outcome test), (b) the mandate-fit work-unit-class coverage (all 3 of BF-M's brownfield work-units land in ≥1 scenario; the 2 `n/a` work-units explicitly excluded by construction), and (c) failure-mode coverage across the F-modes the spec invokes (F8/F14/F17/F38/F46/F52/F53/F59 + F12/F33/F44 cascade — see §4). The 6-scenario count is the floor for the auto-008 §1 rubric requirement; BF-M's design admits 6 cleanly given the mandate-bloc is single (brownfield-only, no greenfield partition required).

## §2 Success criteria

A BF-M lean-eval result "passes cleanly" (per [auto-008 §Falsifier discipline R2 #3 non-unified form](../decisions/auto-008-phase-8-dispatch-shape.md#falsifier-discipline-load-bearing)) iff:

- **(a) Quantitative gate:** ≥80% of the 6 scenarios pass the §1 success criteria (i.e., ≥5 of 6 scenarios pass).
- **(b) Falsifying-outcome gate:** the §3 falsifying-outcome is NOT triggered on any scenario.

**Per-scenario success criteria (verbatim from §1 above):**

1. **Regression-fix familiar-module.** Cycle reaches stage-8 PR open with typed body in ≤D-5-configured cost-ceiling; ≥1 codebase-derived scenario from `intent-decay-log` passes the unseen-subset gate at stage-7 acceptance; PR body's `archaeological_brief_pointer` resolves to a P-27 brief artifact with non-empty `enforced_constraints` field.
2. **P-27 brief invariant recall.** Brief-recall rate ≥80% across 5 seeded load-bearing invariants (≥4 of 5 surfaced in the brief's `enforced_constraints` field); brief-recall Matthews Correlation Coefficient (MCC) > 0.55 against the labeled ground-truth invariant set.
3. **Codebase-evolution-proposal stages 2-4 loop.** Loop terminates within ≤3 iterations (per the BF-M spec sketch of bounded iteration); stage-compression decisions per work-unit-class are mechanically reconstructable from `solutions/audit/cycle-harness/<cycle-id>.json` event log (which stages compressed, which expanded, why); no operator-voluntary "the proposal is mature enough" assertion required.
4. **Stage-6 cross-model review panel.** Cross-model panel surfaces ≥1 contradiction class that same-model baseline misses across 3 cycles; P-14 cross-family routing trace verifies ≥3 distinct provider families consulted per cycle; specialized critics (code-quality + security + conformance) each contribute ≥1 finding in ≥2 of 3 cycles.
5. **Stage-5 CaMeL boundary + cost-ceiling.** ≥80% of 3 cycles complete within D-5-configured budget (≥3 of 3 if all three are intended; or ≥3 of 4 if a fourth is added for fault-tolerance); F12/F33/F44 cascade is substrate-closed (no model-persuadable capability bypass observed in P-25 audit logs); CaMeL utility-tax measured ≤9 percentage points (~7-point baseline + 2-point slack admitted per [`specs/bf-m.md §6 OQ-T3`](../specs/bf-m.md#6-open-carries)).
6. **Parallel-cycle worktree + PR-creator.** 3 concurrent cycles complete with 0 cross-cycle data corruption (verified via diff against expected per-cycle state); 3 PR bodies validate against the Pydantic schema (all required fields populated); P-04 token never observed in any P-01 closure (verified via P-01 audit log + token-presence grep).

**Note on success-criteria vs falsifying-outcome distinction (per [`auto-008 §Falsifier discipline`](../decisions/auto-008-phase-8-dispatch-shape.md#falsifier-discipline-load-bearing)):** failing §2 success criteria can be implementation noise (a P-14 router misconfiguration; a P-03 hook failure; an evaluator misreading a brief field). Triggering the §3 falsifying-outcome is the methodology's load-bearing claim (P-27 brief quality at medium-codebase scale) being wrong — a different kind of failure that the candidate cannot recover from without re-shaping its archaeological-brief tooling thesis.

**Cost-ceiling configuration note (per [`specs/bf-m.md §4 cost-ceiling binding`](../specs/bf-m.md#4-discipline-binding)).** D-5 cost ceilings are per-work-unit-class parameterised for this lean-eval: regression-fix cycles (scenario #1) budgeted narrower (single-plan stage 4 compression); codebase-evolution-proposal (scenario #3) budgeted wider (stages 2-4 loop may iterate up to 3 times). The CaMeL utility-tax (scenario #5) admits the ~7-point ceiling-overhead per [CTR-E6 acceptance](../specs/bf-m.md#6-open-carries); ceiling-hits that occur strictly within the admitted overhead range do NOT count as scenario-failures, but ceiling-hits that occur outside the admitted range (e.g., a 15-point realized utility-tax) DO count as scenario-#5 failures.

## §3 Falsifying outcome

**Falsifying-outcome verbatim (≤80 words from YAML, repeated here for §3-vs-YAML consistency per [auto-008 falsification-designer rubric item (iv)](../decisions/auto-008-phase-8-dispatch-shape.md#r2-1-falsification-designer-concreteness-rubric-3-item-mechanical)):**

> Across 6 medium-codebase brownfield scenarios (50k-250k LOC, ≥3 languages, ≥18 months commit history), BF-M's P-27 archaeological brief misses ≥1 load-bearing invariant per scenario in ≥4 of 6 scenarios, measured as stage-6/7 review-or-acceptance failures attributable to brief omission via the `archaeological_brief_pointer` trace in `solutions/audit/p-27-briefs/<cycle-id>.json`. Equivalently: brief-recall MCC ≤0.55 against the labeled invariant ground-truth set.

**Rationale.** BF-M's central wager (per [`specs/bf-m.md §1 load-bearing claim`](../specs/bf-m.md#1-overview)) is that *Archaeological brief tooling + worktree isolation + per-issue PR-creator coordination, composed as methodology-first brownfield* is the per-cycle methodological closure for brownfield. At the medium-codebase tier — the BF-M-distinctive complexity wager (more complex than BF-S, where small codebase can be read directly; less than BF-L, where Pulse-style production-trace-to-spec-amendment infrastructure is required) — the **load-bearing component is P-27 brief quality**: the LLM-judge synthesis loop over P-22 (codebase index) + P-07 (telemetry) + P-24-equivalent (attribution) must surface load-bearing invariants in the brief's `enforced_constraints` field, or every downstream stage (intent-capture at 3, build at 5, review at 6, acceptance at 7) operates on incomplete information. If the brief systematically misses load-bearing invariants at medium-codebase scale, BF-M's brownfield-methodology-first thesis inverts to substrate-first (because the brief is the substrate that didn't deliver) and the entire 8-stage cycle's downstream guarantees lose their grounding.

The MCC ≤0.55 threshold mirrors the Larbi single-judge ceiling for contradiction-detection — if BF-M's P-27 brief synthesis loop is no better than a naive single-judge inspection at recall-of-load-bearing-invariants, the brief tool is not the methodological closure BF-M claims it to be; it is single-judge wearing a more expensive interface.

**Brief-recall ground-truth labeling protocol.** The 5 seeded load-bearing invariants for scenario #2 are constructed BEFORE the brief is generated, drawn from the medium-codebase fixture using one of three labeling channels: (a) explicitly documented invariants in existing test cases (e.g., property-based test predicates; assertions in integration tests); (b) implicit invariants surfaced by P-23 dependency-impact graph analysis (e.g., a serialization contract that ≥3 modules depend on, observable via P-23 blast-radius compute); (c) operator-attested invariants gathered from the fixture's commit history (commit messages explicitly stating "preserves invariant X" or "must not violate Y"). The labeling channels are recorded in `solutions/setup/invariant-labels.json` BEFORE scenario #2 runs, so the brief-recall scoring is not post-hoc tunable.

**Why this falsifier and not another.** Three alternative falsifiers were considered:

- "If P-03 worktree isolation fails F17 closure" — this is substrate-implementation-failure, not the load-bearing methodology claim. P-03 is an orphan ADR with well-defined contract; failure here is a P-03 bug, not a BF-M architectural-thesis failure.
- "If the stage-6 cross-model panel cannot catch a single contradiction class" — this is OQ-T2 territory (cross-model review necessity), but per BF-M [`§6 OQ-T2`](../specs/bf-m.md#6-open-carries), this is an open carry not a load-bearing claim; BF-M took the F46 side as a methodological default, not as the central wager.
- "If parallel cycles deadlock at the harness layer" — this is a concurrency-correctness question, not a methodology-first vs substrate-first question.

The P-27 brief-quality MCC ceiling is BF-M's *distinctive* load-bearing wager at the medium-codebase tier — the claim that distinguishes BF-M from a substrate-first brownfield methodology and from BF-S (small-codebase, where the brief is less load-bearing because the codebase can be read directly) and from BF-L (large-codebase, where Pulse-style production-trace infrastructure is the load-bearing substrate, not the brief alone). The falsifier targets exactly this distinction.

**Machine-checkability.** Per [auto-008 falsification-designer rubric 4-item check](../decisions/auto-008-phase-8-dispatch-shape.md#r2-1-falsification-designer-concreteness-rubric-3-item-mechanical):

- **(i) Metric:** `brief-recall-rate` (countable; % of seeded load-bearing invariants surfaced in `enforced_constraints` field) AND `MCC` (Matthews Correlation Coefficient, numeric).
- **(ii) Artifact state:** `solutions/audit/p-27-briefs/<cycle-id>.json` (specific directory, specific filename pattern). The briefs are produced by [P-27 (ADR 0034)](../../docs/adr/0034-p-27-archaeological-brief-tooling.md)'s tool-using LLM-judge synthesis loop; trajectory-replayable per [P-05 (ADR 0012)](../../docs/adr/0012-p-05-trajectory-capture.md).
- **(iii) Threshold:** `<80%` recall rate OR `≤0.55` MCC. Both numeric, both single-direction comparisons.
- **(iv) §3-vs-YAML consistency:** the YAML field and this §3 statement name the same metric (brief-recall + MCC), same artifact location (`solutions/audit/p-27-briefs/`), same threshold (<80% / ≤0.55).

The falsifier passes all 4 rubric items (pass on (iv) mandatory; pass on ≥2 of (i)-(iii)).

## §4 Failure modes the test surfaces

For each scenario, the specific F-mode(s) the scenario pressure-tests, citing the candidate's spec §3 (methodology shape) or §4 (discipline binding) where applicable:

- **Scenario #1 regression-fix familiar-module** surfaces:
  - **F38 (deterministic-linter coverage)** — stage 3 P-12 GtWR R7/R8/R9 vocab lint + stage 7 P-12 perimeter (per [`specs/bf-m.md §3 stage 3/7`](../specs/bf-m.md#3-methodology-shape)). Scenario verifies the linter ladder catches regression-fix patterns.
  - **F46 (cross-model review)** — stage 6 cross-model reviewer (P-14) on the diff against change-intent.
  - **F42 (cognitive-escrow re-entry)** — PR body is the F42 re-entry surface per BF-M §3 stage 8.
- **Scenario #2 P-27 brief invariant recall** surfaces:
  - **F8 (stale knowledge)** — the brief's `intent-decay-log` is the load-bearing recall surface; F8 mitigation via next-reader-check (per BF-M §4 knowledge-promotion binding). The scenario IS the §3 falsifying-outcome test.
  - **Larbi MCC ceiling** — single-judge baseline MCC ≤0.55 is the comparison floor; if brief synthesis is not better, BF-M's load-bearing wager fails at medium-codebase scale.
- **Scenario #3 codebase-evolution-proposal loop** surfaces:
  - **F59 (premature decomposition)** — stage 4 is the named hazard per [`specs/bf-m.md §3 stage 4`](../specs/bf-m.md#3-methodology-shape); the loop's bounded-iteration discipline is tested.
  - **F25 (design starvation)** — `codebase-evolution-proposal` is the third work-unit-shape the v2 set lacked; design starvation surfaces as failure-to-converge in the stages 2-4 loop.
- **Scenario #4 stage-6 cross-model review panel** surfaces:
  - **F46 (single-model review blindspot)** — cross-model panel via P-14 is the explicit mitigation; the scenario verifies efficacy.
  - **F55 (behavioural drift)** — Patrol-tier across cycles (per [`specs/bf-m.md §4 three-loop`](../specs/bf-m.md#4-discipline-binding)).
  - **CTR-D7 contradiction (corpus)** — BF-M takes the F46 side; the scenario tests whether the grounds-clause holds empirically.
- **Scenario #5 stage-5 CaMeL boundary + cost-ceiling** surfaces:
  - **F12 → F33 → F44 lethal-trifecta cascade** — per [`specs/bf-m.md §4 trifecta-closure`](../specs/bf-m.md#4-discipline-binding): "F12 → F33 → F44 cascade closed at the substrate by capability-typed dataflow"; P-25 CaMeL boundary is the substrate-side closure.
  - **F53 (substrate-enforced stage refusal)** — per BF-M §3 distinctive decision 3 + §4 honesty binding; CaMeL bypass cannot be set by the agent under review (F53-resistant).
  - **CTR-E1 + CTR-E6 (cost-range + CaMeL utility-tax)** — both accepted as inputs to ceiling calibration per BF-M §4 cost-ceiling binding.
- **Scenario #6 parallel-cycle worktree + PR-creator** surfaces:
  - **F17 (parallel-agents-shared-dirs)** — P-03 worktree isolation (ADR 0045 orphan) is the substrate-side closure; per-cycle ref namespace + tmpfs ephemeral checkouts.
  - **F14 (attribution collapse)** — P-04 PR creator (ADR 0046 orphan) emits typed Pydantic PR body with required `agent_id` + `model_snapshot` + `trajectory_pointer` per BF-M §4 honesty binding.
  - **F42 (cognitive-escrow re-entry)** — PR body IS the F42 re-entry surface per BF-M §3 stage 8 "machine-readable typed block, not operator-formatted convention".

The cross-cutting failure-mode coverage (10 distinct F-modes + 3 corpus CTRs) is the lean-eval's load. **No scenario engages a failure mode F-mode is not enumerated in BF-M's spec §2-§4 or in the corpus** — the lean-eval does NOT smuggle in failure modes the candidate did not commit to defending.

**F-mode coverage matrix.** For traceability across scenarios:

| F-mode / CTR | Description (one-line from corpus) | Scenario(s) | BF-M spec § |
|---|---|---|---|
| F8 | Stale knowledge (next-reader-check inversion) | #2 (load-bearing) | §4 knowledge-promotion |
| F12 | Lethal trifecta | #5 | §4 trifecta-closure + ADR 0033 |
| F14 | Attribution collapse | #6 | §4 honesty + §3 stage 8 + ADR 0046 |
| F17 | Parallel agents on shared dirs | #6 | §2 P-03 + §3 stage 5 + ADR 0045 |
| F25 | Design starvation | #3 | §3 work-unit polymorphism |
| F33 | Lethal-trifecta cascade step | #5 | §4 trifecta-closure |
| F38 | Deterministic-linter coverage | #1 | §3 stage 3/7 + ADR 0032 |
| F42 | Cognitive-escrow re-entry surface | #1, #6 | §3 stage 8 + §4 cognitive-escrow |
| F44 | Lethal-trifecta cascade step | #5 | §4 trifecta-closure |
| F46 | Single-model review blindspot | #1, #4 | §3 stage 6 + §4 bias-guard |
| F53 | Substrate-enforced stage refusal | #5, #6 | §3 distinctive decision 3 |
| F55 | Behavioural drift (self-referential) | #4 | §4 three-loop + Patrol-tier |
| F59 | Premature decomposition | #3 | §3 stage 4 |
| CTR-D7 | Same-model review contradiction | #4 | §6 OQ-T2 |
| CTR-E1 | 10× cost range | #5 | §4 cost-ceiling |
| CTR-E6 | CaMeL utility-tax | #5 | §4 cost-ceiling + §6 OQ-T3 |

16 cells; each maps to ≥1 scenario; each cell's spec §-anchor is auditable from `specs/bf-m.md`. **Coverage is intentional, not coincidental:** scenarios were designed FROM the F-mode list, not the reverse.

## §5 Evaluator time + protocol

**Expected evaluator time: 1 day** (per [v1.2 plan § Phase 8](../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md#phase-8--lean-eval-design-one-brief-per-candidate-first-pressure-test-surface-revised-in-v12) ~1-day-per-candidate bound). Breakdown:

- **Setup (~2 hours).** Evaluator initializes BF-M's substrate stack per [`specs/bf-m.md §2`](../specs/bf-m.md#2-substrate-composition): P-01 sandbox at stage-5 wrap; P-02 cost ceilings per-work-unit-class budget caps (regression-fix narrower than codebase-evolution-proposal per [`§3 work-unit polymorphism`](../specs/bf-m.md#3-methodology-shape)); P-05 trajectory; P-06 watchdog Daemon-everywhere + Triage-at-stages-4/5/6 + Patrol-cross-cycle; P-07 telemetry ingestor (the load-bearing CTR-B5/G2 inversion surface); P-08 scenario storage with absorbed-P-09 runner contract; P-12 deterministic linter framework; P-14 judge router (cross-family routing); P-22 polyglot codebase index (tree-sitter + per-language LSP + SQLite-FTS/DuckDB); P-23 dependency-impact graph; P-25 CaMeL perimeter (NORMAL/STRICT per-work-unit-class config); P-27 archaeological-brief tooling (tool-using LLM-judge synthesis loop over P-22 + P-07 + P-24-equivalent); P-03 worktree isolation (BF-M-only orphan; tmpfs-mounted ephemeral checkouts); P-04 PR creator (BF-M-only orphan; per-cycle GitHub App installation token outside P-01 closure). Configure the medium-codebase fixture (50k-250k LOC, ≥3 languages, ≥18 months commit history).

- **Scenario execution (~5 hours).** Run scenarios #1-#6 in order. Each scenario produces (a) per-cycle archaeological brief at `solutions/audit/p-27-briefs/<cycle-id>.json`, (b) per-cycle trajectory log via P-05, (c) per-cycle PR body via P-04 (validated against the Pydantic schema), (d) Patrol-tier event log under `solutions/audit/patrol/<cycle-id>.json` for cross-cycle drift detection, (e) P-25 capability audit log under `solutions/audit/camel/<cycle-id>.json` (scenario #5), (f) parallel-cycle reference-namespace audit (scenario #6). Evaluator does NOT intervene mid-scenario; substrate-and-methodology-only.

- **Verdict pass (~1 hour).** Evaluator computes (i) per-scenario pass/fail against §2 success criteria; (ii) the §3 falsifying-outcome check (brief-recall rate + MCC across 5 seeded load-bearing invariants in scenario #2); (iii) the "pass cleanly" verdict per [auto-008 §Falsifier discipline R2 #3 non-unified form](../decisions/auto-008-phase-8-dispatch-shape.md#falsifier-discipline-load-bearing). Verdicts written to `solutions/lean-eval/verdict-bf-m.md`.

**Protocol invariants** (per [auto-008 §Falsifier discipline escape-hatch enumeration](../decisions/auto-008-phase-8-dispatch-shape.md#r2-2--3-dec-1a-falsifying-pattern-canonical-terms-committed-in-this-brief)):

- **No out-of-mandate scope claim.** BF-M is brownfield-mandate-only; all 6 scenarios are brownfield-shaped by construction. BF-M's `initial-spec: n/a` and `mvp: n/a` mandate-fit cells are explicit out-of-scope rejections, not silence; the lean-eval respects this by NOT including any greenfield-shaped scenario. Out-of-mandate scope claim does not apply (BF-M does not claim greenfield).
- **No scenario-skip mid-run.** All 6 scenarios are executed; partial completion is a failure, not a skip.
- **No criterion-substitution.** §2 success criteria are committed in this brief; evaluator does NOT re-interpret them mid-run. If §2 is defective, the brief is rewritten not the criterion swapped.

**Substrate ground-truth invariants.** The evaluator records the substrate state at end-of-scenario (P-05 trajectory + P-25 audit logs + P-27 brief artifacts + P-04 PR body Pydantic-validated state) so the lean-eval verdict is reconstructable from substrate state alone, not from evaluator memory. Per the [§3 falsifying-outcome machine-checkability rubric](#3-falsifying-outcome): the verdict on scenario #2 is reconstructable from `solutions/audit/p-27-briefs/`.

**Hour-by-hour evaluator-time breakdown** (8-hour evaluator-day budget):

| Hour | Phase | Activity | Artifacts produced |
|---|---|---|---|
| 0:00-1:00 | Setup | Initialize BF-M substrate stack per `specs/bf-m.md §2` (P-01..P-27 + P-03 + P-04 orphans); configure D-5 cost ceilings per-work-unit-class | `solutions/setup/substrate-init.log` |
| 1:00-2:00 | Setup | Stand up the medium-codebase fixture (50k-250k LOC, ≥3 languages, ≥18 months history); generate seeded load-bearing-invariant labels for scenario #2 | `solutions/setup/fixture-{loc,lang,history}.json`; `solutions/setup/invariant-labels.json` |
| 2:00-3:00 | Scenario #1 | Regression-fix on familiar-module: 1 BF-M cycle through stages 1-8 | `solutions/audit/p-27-briefs/sc1.json`; `solutions/lean-eval/sc1/pr-body.json` |
| 3:00-4:00 | Scenario #2 | P-27 brief invariant-recall: 5 seeded scenarios × brief generation + recall scoring | `solutions/audit/p-27-briefs/sc2-seed{1..5}.json` |
| 4:00-4:30 | Scenario #3 | Codebase-evolution-proposal stages 2-4 loop | `solutions/audit/cycle-harness/sc3.json` |
| 4:30-5:30 | Scenario #4 | Stage-6 cross-model panel: 3 cycles | `solutions/lean-eval/sc4/panel-verdicts.json` |
| 5:30-6:30 | Scenario #5 | CaMeL boundary + cost-ceiling: 3 production-adjacent cycles | `solutions/audit/camel/sc5-*.json`; `solutions/audit/p-02-ceilings.json` |
| 6:30-7:00 | Scenario #6 | Parallel-cycle worktree + PR-creator: 3 concurrent cycles | `solutions/audit/p-03-worktrees/sc6.json`; `solutions/lean-eval/sc6/pr-bodies.json` |
| 7:00-7:30 | Verdict pass | Compute per-scenario pass/fail + §3 falsifier check + "pass cleanly" verdict | `solutions/lean-eval/verdict-bf-m.md` |
| 7:30-8:00 | Reporting | Write verdict-bf-m.md with brief-recall, MCC, per-scenario verdicts, escape-hatch audit | (same file) |

Total 8 hours; scenarios consume ~5 hours; setup + verdict ~3 hours. If any scenario over-runs, evaluator records the over-run in the verdict file but does NOT skip subsequent scenarios — partial completion = scenario fails per [§5 protocol invariants no-scenario-skip clause](#5-evaluator-time--protocol).

## §6 Open critique references

BF-M's [`specs/bf-m.md §6 Open carries`](../specs/bf-m.md#6-open-carries) lists 8 open critique findings; the lean-eval engages 6 of them directly:

- **OQ-T1 Stage-compression rules per work-unit-class** → engaged by scenario #3 (codebase-evolution-proposal stages 2-4 loop). The lean-eval verifies whether the stages 2-4 loop is bounded and whether stage-compression decisions are mechanically reconstructable from cycle harness state. **If scenario #3 fails, OQ-T1 is escalated as a Phase-5/6 methodology-spec carry.**
- **OQ-T2 Cross-model review necessity under CTR-D7/D8** → engaged by scenario #4 (stage-6 cross-model panel). The lean-eval verifies whether cross-model panel catches contradictions same-model misses, testing BF-M's F46-side commitment.
- **OQ-T3 CaMeL utility-tax acceptance criterion** → engaged by scenario #5 (CaMeL boundary + cost-ceiling). The lean-eval measures realized utility-tax against the ~7-point baseline + 2-point slack admitted.
- **OQ-T4 Scenarios-from-codebase governance** → engaged by scenarios #1 + #2 (both rely on codebase-derived scenarios). The lean-eval verifies the unseen-subset-not-out-of-tree holdout discipline (D-2 challenge per BF-M's challenged-defaults — see backfill-notes §1.5).
- **P-27 brief-quality calibration (Phase-5/8 RG carry)** → engaged by scenario #2 (the §3 falsifying-outcome test). The lean-eval uses BF-M's per-section compression rule baseline (`introduction-cycle` + `intent-decay-log` + `contemporary-references`); a full calibration sweep across compression parameters is downstream per [`specs/bf-m.md §6`](../specs/bf-m.md#6-open-carries).
- **OQ-T10/F36 Instruction-following ceiling vs change-intent block size** → engaged by scenario #1 + #3 (both produce change-intent blocks). The lean-eval verifies whether stage-3 caps simultaneous requirements per change without triggering F36 refusal at the BF-M cap of 10-20 specified requirements.

The 2 open carries NOT engaged by this lean-eval:

- **OQ-T6 Brownfield regime ceiling measurability** → not engaged. This is a measurement-protocol question across multiple work-unit-classes that exceeds the 1-day evaluator budget; would require a multi-day fixture run + per-(work-unit-class × stage) Automation-Mode bar-clearance measurement against Jaymin's ~L3 brownfield ceiling per [`specs/bf-m.md §5 regression-fix falsifying scenario`](../specs/bf-m.md#5-mandate-fit). Carried as Phase-8-followup advisory.
- **OQ-8 Anthropic Skills network-closure vs Patrol "dreaming"** → not engaged. Substrate-vendor question (per BF-M §1 axis "vendor-deferred at boundaries"); the lean-eval substrate stack assumes network-open for stage-2 P-27 brief generation and Patrol-tier monitoring. If a future deployment closes network at the Skill layer, OQ-8 fires; not in this lean-eval's scope.

**Open-carries-to-falsifier traceability.** None of the 6 engaged open carries collapse into the §3 falsifying-outcome surface (which is specifically P-27 brief invariant-recall at medium-codebase scale, an item NOT enumerated in BF-M's §6 open carries as a separate OQ — though "P-27 brief-quality calibration" is the closest match, surfaced in §6 as a partial-RG carry per [BF-M substrate-requirements §2](../substrate-requirements/bf-m.md#2-rg-primitives) "**Partial-RG accepted-as-RG choice (b)**: substrate exposes brief-quality metrics + gating thresholds as first-class parameters so Phase-8 sweeps are tractable"). The lean-eval's §3 falsifying-outcome is therefore not a re-statement of an open carry but a load-bearing wager the spec implicitly carries — making the falsifier the genuine pressure-test surface, not an open-question-rehearsal.

## §7 Phase-7 cite obligations honored

Per the [`auto-008` per-candidate cite-obligation mapping table for BF-M](../decisions/auto-008-phase-8-dispatch-shape.md#high-confidence-mandatory-cite-obligations-3-cells--n-candidates):

### High-confidence mandatory cite obligations (2 cells)

**(1) Compound-Engineering 4-step loop verbatim cite.** Per [aggregation §3.1 finding #2](../backfill-notes.md#31-high-confidence-findings-3--apply-precedence-rule) + [`audit-silent-absorption.md §B.1 row 2`](../backfill-notes/audit-silent-absorption.md): BF-M's `specs/bf-m.md §4 three-loop binding` invokes "plan → work → review → compound" loop with Patrol-tier closure but does NOT cite `archive/synthesis-v1-v2/13-round-2-synthesis.md` where the 4-step phrasing is v0.2-canonicalized. **Cite honored in this brief**: scenario #3 (codebase-evolution-proposal stages 2-4 loop) operates against the 4-step loop's "plan" phase + scenario #4 (stage-6 cross-model review) operates against the "review" phase; per the Phase-7 cite obligation:

> The Compound-Engineering loop `plan → work → review → compound` (referenced in [`specs/bf-m.md §4 three-loop binding`](../specs/bf-m.md#4-discipline-binding)) is v0.2-canonical per [`archive/synthesis-v1-v2/13-round-2-synthesis.md`](../../archive/synthesis-v1-v2/13-round-2-synthesis.md) — the archive Round-2 synthesis that promoted the 4-step shape from `research/03-` to load-bearing methodology vocabulary. BF-M's 8-stage cycle materializes the 4-step loop at per-cycle granularity (stages 4-5 = plan + work; stage 6 = review; stage 8 PR-body + cross-cycle Patrol-tier = compound).

**(2) 4-architecture taxonomy cite.** Per [aggregation §3.1 finding #3](../backfill-notes.md#31-high-confidence-findings-3--apply-precedence-rule) + [`audit-silent-absorption.md §B.1 row 3`](../backfill-notes/audit-silent-absorption.md): BF-M's lineage statement at backfill-notes §1 ("hybrid of Architecture 2 Compound Atelier and Architecture 3 Phase-Gated Foundry, with secondary inheritance from Architecture 1 Specification Refinery") invokes the 4-architecture taxonomy but does NOT cite `archive/architectures-v2/00-comparison.md §1` where the taxonomy is canonical. **Cite honored in this brief**:

> The 4-architecture taxonomy (Atelier-style / Refinery-style / Foundry-style / Tournament-style work-unit-shape taxonomy) referenced as BF-M's lineage (per [`backfill-notes/bf-m.md §1`](../backfill-notes/bf-m.md#1-overview)) is v2-canonical per [`archive/architectures-v2/00-comparison.md §1`](../../archive/architectures-v2/00-comparison.md). BF-M's hybrid Atelier+Foundry lineage at the medium-codebase tier inherits the workshop-chain shape from Atelier §4.1 (BF-M's 8 stages are the workshop chain at per-cycle granularity) and the phase-bound-V&V-pairing shape from Foundry §2 (BF-M's stages 5-6-7 are the Build/Review/Acceptance V&V triad).

### Medium-confidence design inputs (consulted)

Per [aggregation §3.2 reconciliation TBDs](../backfill-notes.md#32-medium-confidence-findings-7--trigger-tbd-reconciliation-rows) + [`audit-silent-absorption.md §B.1`](../backfill-notes/audit-silent-absorption.md): subagents consult §B.1 for cells touching their candidate. **BF-M's medium-confidence cells (consulted for this brief):**

- **§B.1 row 6 (BF-M × `02-compound-atelier.md §4.3` reviewer panel)** — BF-M's stage-6 cross-model reviewer with specialized critics (code-quality / security / conformance) is structurally the Atelier §4.3 reviewer panel + "Anthropic Auto-Review pattern". **Engagement:** scenario #4's design explicitly tests the specialized-critics-each-contribute-finding success criterion — directly probing whether BF-M's silently-absorbed Atelier-§4.3 reviewer-panel structure operates at medium-codebase scale. Flagged in §1 scenario #4.
- **§B.1 row 11 (BF-M × `02-compound-atelier.md §0.0 + §6` Klaassen four-clause plan-prompt)** — BF-M stage 4 invokes "Klaassen four-clause plan-prompt" without archive cite to the Klaassen examples canonicalized in Atelier §6. **Engagement:** scenario #3 (codebase-evolution-proposal stages 2-4 loop) exercises stage 4's N≥3 candidate-plan generation — i.e., the four-clause prompt is on the hot path. Non-load-bearing for this lean-eval's falsifier; flagged for completeness.

### Historian load-bearing design inputs (engaged)

Per [aggregation §4.1 historian load-bearing gaps](../backfill-notes.md#41-load-bearing-gaps-5--phase-8-lean-eval-inputs) + [`auto-008` historian-design-inputs mapping table](../decisions/auto-008-phase-8-dispatch-shape.md#historian-load-bearing-design-inputs-5-gaps--n-candidates): **BF-M is mapped to (none)**. H-2/H-8 (self-improving-prompts pattern + role) is greenfield-shaped → assigned to GF-S / GF-M / U-A. H-3 (Pulse report production-trace-to-spec-amendment) is brownfield-shaped but BF-L-scale → assigned to BF-L (large codebase; P-13 maintenance loop is the closest analog). H-1 (stable-ID lettering convention) → U-C or D7-U-1. H-5 → glossary non-blocking. **Per the pattern-mandate alignment note (R6 #4 amendment):** the absence of a pre-mapped historian design input for BF-M is intentional, not a candidate-quality signal — H-3 Pulse is a large-codebase pattern that does not apply at BF-M's medium-codebase tier (the brief-as-substrate suffices without Pulse-style production-trace infrastructure). No historian input engaged for this brief.

### Cite-obligation summary (YAML `phase-7-cite-obligations` field)

- `high-confidence-mandatory`: 2 cites (Compound-Engineering 4-step loop archive cite + 4-architecture taxonomy archive cite).
- `medium-confidence-design-inputs`: 2 §B.1 cells (row 6 reviewer panel; row 11 Klaassen four-clause) — both engaged at scenario-design level.
- `historian-design-inputs`: 0 (per pattern-mandate alignment note R6 #4).

**Audit-trail discipline (per [`AGENTS.md § Internal document references`](../../AGENTS.md)).** Every cite in this §7 (and across §1-§6 above) uses a relative path with a §-anchor where the source has one; archive cites for the 2 high-confidence mandatory obligations resolve to the v0.2-canonical and v2-canonical source files (not paraphrases or summaries thereof). The medium-confidence design inputs at §B.1 rows 6 + 11 are flagged in scenario #4's design (Anthropic Auto-Review pattern absorbed silently) and scenario #3's design (Klaassen four-clause prompt invoked at stage 4) — both surfacings are auditable from the §1 scenario text via the relevant `audit-silent-absorption.md` row references. The falsification-designer auditor in Wave 8.1.b will verify these cite-obligations are honored via `grep` against the obligation set named in this §7's YAML summary.

## §8 References

**Candidate spec + back-fill notes (primary inputs):**

- [`specs/bf-m.md`](../specs/bf-m.md) — Phase-6 BF-M architecture spec; §0 ADR-citation index, §1 Overview, §2 Substrate composition, §3 Methodology shape, §4 Discipline binding, §5 Mandate fit, §6 Open carries.
- [`backfill-notes/bf-m.md`](../backfill-notes/bf-m.md) — Phase-7 back-fill audit; §1.5 D-1..D-7 verification (D-1 + D-2 challenged), per-archive-file classification, §11 summary.
- [`substrate-requirements/bf-m.md`](../substrate-requirements/bf-m.md) — Phase-4 substrate-requirements summary (high-primitive-count rationale).
- [`tracks/brownfield-methodology-first.md`](../tracks/brownfield-methodology-first.md) — Phase-3.5 BF-M track sketch.

**Phase-8 dispatch artifacts:**

- [`decisions/auto-008-phase-8-dispatch-shape.md`](../decisions/auto-008-phase-8-dispatch-shape.md) — this brief's parent dispatch decision; §Falsifier discipline (R2 #1-#4 rubric, R6 #2 partitioned-mandate "pass cleanly" non-unified form for BF-M), §Phase-7 cite-obligation propagation table (BF-M row), §Per-candidate lean-eval brief rubric.
- [`lean-evals/gf-m.md`](./gf-m.md) — Wave-8.1 exemplar; structural template followed in this brief.

**Phase-7 inputs (cite-obligation source):**

- [`backfill-notes.md`](../backfill-notes.md) — Phase-7 aggregation matrix; §3.1 (high-confidence cite obligations), §3.2 (medium-confidence TBDs), §4.1 (historian load-bearing gaps).
- [`backfill-notes/audit-silent-absorption.md`](../backfill-notes/audit-silent-absorption.md) — Phase-7 silent-absorption auditor output; §B.1 rows 2, 3, 6, 11 touching BF-M.

**ADRs cited (substrate + discipline):**

- Common substrate: [ADR 0010](../../docs/adr/0010-p-01-sandbox-runtime.md), [ADR 0011](../../docs/adr/0011-p-02-cost-ceilings.md), [ADR 0012](../../docs/adr/0012-p-05-trajectory-capture.md), [ADR 0013](../../docs/adr/0013-p-06-watchdog-tiers.md), [ADR 0014](../../docs/adr/0014-p-07-telemetry-ingestor.md), [ADR 0015](../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md), [ADR 0016](../../docs/adr/0016-p-14-judge-router.md), [ADR 0017](../../docs/adr/0017-p-22-polyglot-codebase-index.md).
- Designed-system common: [ADR 0031 (P-23)](../../docs/adr/0031-p-23-dependency-impact-graph.md), [ADR 0032 (P-12)](../../docs/adr/0032-p-12-deterministic-linter-framework.md).
- 2-candidate-fold: [ADR 0033 (P-25 CaMeL, BF-S+BF-M)](../../docs/adr/0033-p-25-camel-perimeter.md), [ADR 0034 (P-27 archaeological-brief, BF-M+BF-L)](../../docs/adr/0034-p-27-archaeological-brief-tooling.md).
- Orphan (BF-M-only): [ADR 0045 (P-03 worktree isolation)](../../docs/adr/0045-p-03-worktree-isolation.md), [ADR 0046 (P-04 PR creator)](../../docs/adr/0046-p-04-pr-creator.md).
- Discipline: [ADR 0018](../../docs/adr/0018-discipline-bias-guard.md), [ADR 0019](../../docs/adr/0019-discipline-cognitive-escrow.md), [ADR 0020](../../docs/adr/0020-discipline-cost-ceiling.md), [ADR 0021](../../docs/adr/0021-discipline-holdout.md), [ADR 0022](../../docs/adr/0022-discipline-honesty.md), [ADR 0023](../../docs/adr/0023-discipline-knowledge-promotion.md), [ADR 0024](../../docs/adr/0024-discipline-regime-classification.md), [ADR 0025](../../docs/adr/0025-discipline-scoping.md), [ADR 0026](../../docs/adr/0026-discipline-three-loop.md), [ADR 0027](../../docs/adr/0027-discipline-trifecta-closure.md).

**Archive sources (Phase-7 cite obligations):**

- [`archive/synthesis-v1-v2/13-round-2-synthesis.md`](../../archive/synthesis-v1-v2/13-round-2-synthesis.md) — Compound-Engineering 4-step loop v0.2 canonicalization (high-confidence mandatory cite per Phase-7 aggregation §3.1 finding #2).
- [`archive/architectures-v2/00-comparison.md`](../../archive/architectures-v2/00-comparison.md) — 4-architecture taxonomy §1 canonicalization (high-confidence mandatory cite per Phase-7 aggregation §3.1 finding #3).
- [`archive/architectures-v2/02-compound-atelier.md`](../../archive/architectures-v2/02-compound-atelier.md) — Atelier §4.3 reviewer panel + §0.0/§6 Klaassen four-clause (medium-confidence design inputs per §B.1 rows 6, 11).
- [`archive/architectures-v2/03-phase-gated-foundry.md`](../../archive/architectures-v2/03-phase-gated-foundry.md) — Foundry §2 phase-bound V&V pairing (BF-M's secondary lineage anchor).

**Cross-cutting v3 docs:**

- [`decisions-captured.md`](../decisions-captured.md) — DEC-1.a working hypothesis (BF-M is mandate-aligned brownfield; does NOT carry DEC-1.a unified-attempt load), DEC-2 mandate-fit-per-(architecture × work-unit-class).
- [`failure-modes-v3.md`](../failure-modes-v3.md) — F-mode catalog (F8, F12, F14, F17, F25, F33, F38, F42, F44, F46, F53, F55, F59 + CTR-D7, CTR-E1, CTR-E6 referenced).
- [`candidate-registry.md`](../candidate-registry.md) — BF-M candidate-registry entry.
