---
based-on-spec-commit: c54daf1
based-on-backfill-commit: cbb109f
based-on-date: 2026-05-28
candidate-tier: Light
candidate-mandate: greenfield
scenario-set-source: hybrid
mandate-scenario-split:
  greenfield: 6
  brownfield: 0
expected-evaluator-time-days: 1
falsifying-outcome: |
  Across 6 greenfield cold-start cycles run with the P-15 four-guard
  mediator's 3-of-N family-diverse contradiction-detector ensemble
  (N=3 cross-family judges, UNDETERMINED-to-Patrol escalation enabled)
  on seeded F37/F27/F48 contradiction prompt pairs, the ensemble MCC
  measured against labeled ground truth from `solutions/audit/p-15-runs/`
  envelope logs is ≤0.55 — i.e., does not improve on the Larbi
  single-judge baseline. Equivalently: ensemble detection rate <80%
  of seeded contradictions on the same task.
phase-7-cite-obligations:
  high-confidence-mandatory: []
  medium-confidence-design-inputs:
    - audit-silent-absorption.md-§B.1-row-10-tournament-§3.4-structural-diversity
  historian-design-inputs:
    - H-2-self-improving-prompts-pattern
    - H-8-prompt-self-improver-role
---

# Lean-eval brief — GF-S (Greenfield, substrate-first)

Per-candidate lean-eval brief authored under Phase-8 Wave 8.1 per [`auto-008` §Per-candidate lean-eval brief rubric](../decisions/auto-008-phase-8-dispatch-shape.md#decision-round-2). Format model: [`lean-evals/gf-m.md`](./gf-m.md) (Wave-8.1 exemplar). GF-S is greenfield-mandate-only (Light tier per the [`auto-008` tier table](../decisions/auto-008-phase-8-dispatch-shape.md#decision-round-2)); the scenario set is single-bloc greenfield and "pass cleanly" uses the [non-unified-attempt form](../decisions/auto-008-phase-8-dispatch-shape.md#falsifier-discipline-load-bearing) (≥80% scenarios pass + §3 falsifying-outcome NOT triggered).

## §1 Candidate + scenario set

**Candidate.** GF-S is the greenfield-mandate-only substrate-first candidate. Per [`specs/gf-s.md §1`](../specs/gf-s.md#1-overview): the **substrate's invariants are the load-bearing investment** (sandbox shape, trajectory format, cost-ceiling enforcement, watchdog tiers, four-guard mediator, regime classifier — the parts that *do not move during spec refinement*), and methodology is the **thinnest possible layer** that drives the primitives across an 8-step per-cycle protocol. GF-S explicitly disclaims unified-mandate reach per [`track §6`](../tracks/greenfield-substrate-first.md#6-what-this-track-is-not-trying-to-be); 5-of-5 mandate-fit cells declare `greenfield` per [`specs/gf-s.md §5`](../specs/gf-s.md#5-mandate-fit). Day-0 entry-mode: operator-authored 9-field El-Kaim-style intent block + ≥3 region-shaped scenarios; no codebase, no Codebase Model dependency.

**YAML schema discipline.** `candidate-mandate: greenfield`; `mandate-scenario-split: {greenfield: 6, brownfield: 0}` — single-bloc per [auto-008 R6 #1](../decisions/auto-008-phase-8-dispatch-shape.md#round-2-reviewer-amendments-folded-post-round-2-patches). GF-S does NOT carry the [DEC-1.a unified-attempt load](../decisions-captured.md); §1 is not partitioned into greenfield/brownfield sub-sections (the unified-attempt R6 #1 partition rule does not bind GF-S).

**Scenario set source.** Hybrid: (a) drawn from the v3 F-mode corpus targeting F12 / F25 / F27 / F37 / F44 / F46 / F48 / F51 / F52 / F57 — the failure modes GF-S's substrate primitives most explicitly defend against per [`specs/gf-s.md §2-§4`](../specs/gf-s.md#2-substrate-composition); (b) drawn from GF-S's own scenario-derivation primitive at [`specs/gf-s.md §3 cycle step 1-2`](../specs/gf-s.md#3-methodology-shape) — operator intent block + ≥3 region-shaped scenarios stored typed in P-08, gated by the P-15 four-guard mediator. Halves are not redundant: corpus scenarios provide adversarial pressure against GF-S's load-bearing wager (the P-15 four-guard mediator's contradiction-detector ensemble; see §3); candidate-derived scenarios surface what the substrate's own design predicts as the substrate-measured regime-transition trajectory.

**Scenarios (6 total, all greenfield).**

1. **Cold-start initial-spec gating (corpus F25 + F36 + candidate-derived).** Day-0 operator authors a 9-field El-Kaim intent block + 3 region-shaped scenarios for a single greenfield system (e.g., "a deterministic priority-queue web service with burst-load semantics"); the P-15 four-guard mediator runs guard 1 (GtWR vocabulary lint via [P-12 (ADR 0032)](../../docs/adr/0032-p-12-deterministic-linter-framework.md)) + guard 3 (requirement-count budgeter at the Yang/Llama ≤10-20 simultaneous-requirement ceiling) on the inputs. Surfaces: F25 (design starvation — substrate refuses to lights-out a cold-start factory per [ADR 0039](../../docs/adr/0039-p-19-variant-gf-s-work-unit-class.md) OPA floor (a)); F36 (instruction-following ceiling). Pass: cycle starts only on PASS verdict from all 4 guards; [P-19/GF-S](../../docs/adr/0039-p-19-variant-gf-s-work-unit-class.md) classifier emits `augmentation-required` (OPA floor (a) — cold-start cycle count `< N` ⇒ `augmentation-required`). **Implements GF-S `initial-spec` mandate-fit cell.**

2. **Seeded F37 contradiction prompt pairs through the four-guard mediator (corpus F37 + F27 + F48).** Evaluator constructs 5 seeded prompt-pair contradictions (e.g., paired conflicting post-conditions, paired conflicting capability declarations); each pair is submitted to the [P-15 four-guard mediator (ADR 0038)](../../docs/adr/0038-p-15-four-guard-mediator.md) guard 2 — the 3-of-N family-diverse contradiction-detector ensemble dispatched through [P-14 (ADR 0016)](../../docs/adr/0016-p-14-judge-router.md). Sub-verdict three-valued PASS/FAIL/UNDETERMINED; UNDETERMINED escalates to Patrol per [`specs/gf-s.md §2 S8`](../specs/gf-s.md#2-substrate-composition). Single-judge baseline runs first (Larbi MCC ≤0.55 expected). **This is GF-S's load-bearing falsifier scenario** (see §3). Pass: ensemble detection rate ≥80% of seeded contradictions; ensemble MCC > 0.55 against labeled ground truth; UNDETERMINED-to-Patrol escalation surfaces in P-07 telemetry envelope as an explicit event, not a silent ensemble-degradation.

3. **Regime-transition substrate-measurement (candidate-derived OQ-1).** Evaluator runs ≥10 `augmentation-required` cycles on a single work-unit-class; verifies whether the [P-19/GF-S variant (ADR 0039)](../../docs/adr/0039-p-19-variant-gf-s-work-unit-class.md) five-feature work-unit-class vector `(intent_block_fields_touched, declared_stakes, scenario_set_saturation, recent_cross_family_judge_agreement, bar_set_parameters)` substrate-measurably saturates and flips the regime to `automation-eligible` *without* operator declaration. Surfaces: F25 (design starvation as substrate property); F57 (design-authority erosion — OPA hard-floors must hold). Pass: regime flip occurs at ≥1 work-unit-class within 10 cycles; flip event traces verbatim to [`P-05 trajectory (ADR 0012)`](../../docs/adr/0012-p-05-trajectory-capture.md) entries; no operator-asserted "yes the regime should flip" override is required; OPA floors (a)/(c) remain enforced post-flip.

4. **Patrol tier-3 cross-cycle audit (corpus F8 + F55 + F57).** Evaluator runs 6 sequential cycles producing accreted within-factory code + scenario set; configures Patrol-tier ([P-06 ADR 0013](../../docs/adr/0013-p-06-watchdog-tiers.md)) with operator-declared invariants (e.g., "intent block's UC1-equivalent stakes field is unchanged"; "no scenario partition leakage from training→holdout"). Surfaces: F8 (stale-knowledge inversion); F55 (behavioural drift); F57 (design-authority erosion via convenience reclassification). Pass: Patrol catches ≥1 seeded invariant violation per cycle-cohort (evaluator seeds 1 per cohort); invariant-violation event surfaces in [`P-07 telemetry (ADR 0014)`](../../docs/adr/0014-p-07-telemetry-ingestor.md) with diff against versioned-config Rego policy.

5. **Four-guard × P-02 cost-ceiling interaction (candidate-derived §6 cost-stacking carry + corpus CTR-E6).** Evaluator runs 5 cycles under [P-02 (ADR 0011)](../../docs/adr/0011-p-02-cost-ceilings.md) ceilings configured at GF-S-recommended budget (per [`specs/gf-s.md §6` cost-stacking open carry](../specs/gf-s.md#6-open-carries)). Measures whether the four-guard mediator × ensemble-fanout (3 family-diverse judges per contradiction-detector invocation) × every-cycle compounding triggers premature ceiling hits; verifies CTR-E6 admission ("substrate kills the cycle at ceiling — no graceful-degradation mode") behaves per spec. Surfaces: [CTR-E1](../contradictions.md) (10× cost-range); F26 (paraphrase/fan-out cost spike). Pass: ≥80% of 5 cycles complete within budget; on ceiling-hit, P-02 kills the cycle outright (no silent guard-disable; no graceful-degradation mode); kill event traces to P-05 trajectory.

6. **Trifecta closure + perimeter typing on tool-call edges (corpus F12 + F44 + F33).** Evaluator constructs 3 scenarios with spec-derived tool-call edges that touch sensitive perimeter classes (untrusted-input × private-data × outbound-egress per [F12 lethal trifecta](../failure-modes-v3.md)). Verifies [P-01 sandbox (ADR 0010)](../../docs/adr/0010-p-01-sandbox-runtime.md) deny-all + [P-15 perimeter typing (ADR 0038)](../../docs/adr/0038-p-15-four-guard-mediator.md) guard 4 (CaMeL-class declaration-time) + P-25 runtime perimeter (per ADR 0038 decision) closure-first discipline holds; production-credentialled scissors are *substrate-disabled by default* per [`specs/gf-s.md §2`](../specs/gf-s.md#2-substrate-composition). Surfaces: F12 (lethal trifecta); F44 (production-credentialled scissors); F33 / F51 (Ashby-deficient probabilistic guards explicitly not trusted as primary closure per F52 tempting-wrong-hybrid). Pass: 0 trifecta-crossing tool calls execute; 100% of trifecta-attempt edges are blocked at declaration time (P-15 guard 4) or call time (P-25); blocked events trace to P-05 + P-07.

**Why these 6 scenarios.** GF-S's spec carries 6 open carries at [`specs/gf-s.md §6`](../specs/gf-s.md#6-open-carries): F40 last-mile drift; P-15 contradiction-detector reliability; cost-stacking math; S9 minimum scenario-set size; F51 LLM-judge recursion; day-0 operator-intent illiteracy. The 6-scenario set engages 5 of these (P-15 reliability → #2; F51 recursion → #2 partial; regime-transition substrate-measurement → #3; cost-stacking → #5; F25 design starvation → #1+#3). F40 last-mile drift is substrate-unaddressed per [`specs/gf-s.md §6`](../specs/gf-s.md#6-open-carries) ("Status: substrate-unaddressed; the strongest standing critique of the substrate-first axis. Carries forward to Phase-8 methodology lean-eval, not Phase-5 ADR.") — flagged for the cross-candidate evaluator-brief in §6 below, not engaged by this lean-eval (a substrate-first lean-eval cannot resolve a methodology-layer carry without changing the candidate's axis). The 6 scenarios cover all 5 of GF-S's work-unit-classes (per [`specs/gf-s.md §5`](../specs/gf-s.md#5-mandate-fit)): `initial-spec` (#1), `refactor` (#3+#4), `mvp` (#1+#3), `post-mvp-evolution` (#4), `regression-fix` (#6).

## §2 Success criteria

A GF-S lean-eval result "passes cleanly" (per [auto-008 §Falsifier discipline R2 #3 non-unified form](../decisions/auto-008-phase-8-dispatch-shape.md#falsifier-discipline-load-bearing)) iff:

- **(a) Quantitative gate:** ≥80% of the 6 scenarios pass the §1 success criteria (i.e., ≥5 of 6 scenarios pass).
- **(b) Falsifying-outcome gate:** the §3 falsifying-outcome is NOT triggered on any scenario.

**Per-scenario success criteria (verbatim from §1):**

1. **Cold-start initial-spec gating.** Cycle starts only on PASS verdict from all 4 P-15 guards (GtWR lint + contradiction-detector + req-count budgeter + perimeter typing); P-19/GF-S classifier emits `augmentation-required` regime per OPA floor (a); P-15 PASS+FAIL envelopes surface in P-07 telemetry per [ADR 0038](../../docs/adr/0038-p-15-four-guard-mediator.md) typed-envelope discipline.
2. **Seeded F37 contradiction prompt pairs.** Ensemble detection rate ≥80% across 5 seeded contradictions (≥4 of 5 detected); ensemble MCC > 0.55 against labeled ground truth; UNDETERMINED sub-verdicts (if any) escalate to Patrol as explicit P-07 envelope events, not silent guard-disable.
3. **Regime-transition substrate-measurement.** Regime flip from `augmentation-required` → `automation-eligible` occurs at ≥1 work-unit-class within 10 cycles; flip event reconstructable from P-05 trajectory; no operator override invoked; OPA floors (a)-(d) remain enforced post-flip.
4. **Patrol tier-3 cross-cycle audit.** Patrol catches ≥1 seeded invariant violation per cycle-cohort (≥1 of 1 per cohort); violation envelope traces to P-07 telemetry with versioned-config Rego diff.
5. **Four-guard × P-02 cost-ceiling interaction.** ≥80% of 5 cycles complete within budget (≥4 of 5); on ceiling-hit, P-02 kills the cycle outright (no graceful-degradation mode); kill event traces to P-05 trajectory.
6. **Trifecta closure + perimeter typing.** 0 trifecta-crossing tool calls execute; 100% of trifecta-attempt edges are blocked (P-15 guard 4 declaration-time or P-25 call-time); blocked events trace to P-05 + P-07.

**Success-criteria vs falsifying-outcome distinction (per [auto-008 §Falsifier discipline](../decisions/auto-008-phase-8-dispatch-shape.md#falsifier-discipline-load-bearing)).** Failing §2 success criteria can be implementation noise — a P-14 router misconfigured; a Rego policy syntax error; an operator-seeded invariant that's too sensitive. The §3 falsifying-outcome is GF-S's load-bearing claim being wrong: the [P-15 four-guard mediator's 3-of-N family-diverse ensemble (ADR 0038)](../../docs/adr/0038-p-15-four-guard-mediator.md) is the substrate-level F37/F27/F48 defense. If its MCC ceiling matches the Larbi single-judge ceiling, the four-guard mediator's central wager — that structural ensemble diversity raises contradiction-detection above single-judge — fails, and the substrate-first axis loses one of its three load-bearing substrate-level closures (the other two being P-08 holdout discipline + the P-01/P-15/P-25 trifecta stack).

## §3 Falsifying outcome

**Falsifying-outcome verbatim (≤80 words from YAML, repeated here for §3-vs-YAML consistency per [auto-008 falsification-designer rubric item (iv)](../decisions/auto-008-phase-8-dispatch-shape.md#r2-1-falsification-designer-concreteness-rubric-3-item-mechanical)):**

> Across 6 greenfield cold-start cycles run with the P-15 four-guard mediator's 3-of-N family-diverse contradiction-detector ensemble (N=3 cross-family judges, UNDETERMINED-to-Patrol escalation enabled) on seeded F37/F27/F48 contradiction prompt pairs, the ensemble MCC measured against labeled ground truth from `solutions/audit/p-15-runs/` envelope logs is ≤0.55 — i.e., does not improve on the Larbi single-judge baseline. Equivalently: ensemble detection rate <80% of seeded contradictions on the same task.

**Rationale.** GF-S's central substrate-first wager (per [`specs/gf-s.md §1 load-bearing claim`](../specs/gf-s.md#1-overview) + [`§2 S8 four-guard mediator`](../specs/gf-s.md#2-substrate-composition)) is that the **P-15 four-guard mediator** with a **3-of-N family-diverse contradiction-detector ensemble** dispatched through P-14 — explicitly carrying the F27/F48 shared-pretraining-collusion residual as a *partial-RG* per [`specs/gf-s.md §6` open carry on P-15 reliability](../specs/gf-s.md#6-open-carries) — produces an MCC ceiling above the Larbi single-judge ceiling of ≤0.55. If the lean-eval shows the ensemble's MCC at the same ≤0.55 bound on the same task with the GF-S-recommended baseline parameters (N=3 cross-family + UNDETERMINED-to-Patrol escalation), the candidate's load-bearing wager is empirically wrong: structural family-diversity at the ensemble layer does not improve on the single-judge baseline for F37/F27/F48 detection, and the four-guard mediator's contradiction-detector guard 2 (one of four substrate-level closures GF-S commits as substrate-not-methodology) collapses to a methodology-overlay-equivalent.

**Why this falsifier and not another.** Four alternatives were considered:

- "If regime-transition never occurs within reasonable cycle-count" — engages OQ-1 (S9 minimum scenario-set size open carry), but is failure-mode-of-implementation, not load-bearing wager. The substrate-measured-transition claim is one of three distinctive methodology decisions but not the *central* substrate-first wager.
- "If F40 last-mile drift surfaces unmitigated" — F40 is substrate-unaddressed by GF-S's own admission per [`specs/gf-s.md §6`](../specs/gf-s.md#6-open-carries); failing here would confirm what the spec already concedes, not falsify a load-bearing claim.
- "If cost-stacking math exceeds budget for >50% of cycles" — engages the §6 cost-stacking carry but is a CFO flag, not a methodology falsifier. Cost-stacking can be remediated by parameter tuning (lower N, reduced fan-out); the load-bearing wager survives.
- "If trifecta closure (scenario #6) leaks ≥1 edge" — this is the **second-most-load-bearing** GF-S claim, but trifecta closure is *substrate-determined* (P-01 deny-all + P-15 declaration-time + P-25 runtime). A trifecta breach is closer to substrate-implementation failure than to a falsification of the substrate-first axis's central wager. The four-guard mediator's contradiction-detector is GF-S-orphan ([ADR 0038](../../docs/adr/0038-p-15-four-guard-mediator.md)) — single-candidate distinctive — and the F37/F27/F48 ensemble defense is the wager GF-S takes on that *no other GF candidate takes the same way*.

The P-15 contradiction-detector ensemble is GF-S's *distinctive* load-bearing wager — the claim that distinguishes the substrate-first axis from a methodology-first counterpart that would push contradiction-detection into a methodology-layer review panel. The falsifier targets exactly this distinction.

**Machine-checkability** per [auto-008 falsification-designer 3-item rubric](../decisions/auto-008-phase-8-dispatch-shape.md#r2-1-falsification-designer-concreteness-rubric-3-item-mechanical):

- **(i) Metric:** `MCC` (Matthews Correlation Coefficient, numeric) AND `detection-rate-vs-single-judge-baseline` (countable; % of seeded contradictions detected). Both items pass.
- **(ii) Artifact state:** `solutions/audit/p-15-runs/<scenario-id>.json` envelope logs (specific directory; specific filename pattern). The envelopes are emitted by the P-15 four-guard mediator per [ADR 0038](../../docs/adr/0038-p-15-four-guard-mediator.md) typed-envelope discipline (PASS *and* FAIL envelopes auditable, per [`specs/gf-s.md §4 honesty binding`](../specs/gf-s.md#4-discipline-binding)); trajectory-replayable per [P-05 (ADR 0012)](../../docs/adr/0012-p-05-trajectory-capture.md).
- **(iii) Threshold:** `≤0.55 MCC` OR `<80% detection rate`. Both numeric, both single-direction comparisons.
- **(iv) §3-vs-YAML consistency (MANDATORY):** the YAML field and this §3 statement name the **same metric** (ensemble MCC + detection rate), the **same artifact location** (`solutions/audit/p-15-runs/`), and the **same threshold** (≤0.55 / <80%). Both name N=3 cross-family with UNDETERMINED-to-Patrol escalation as the parameter configuration under test.

The falsifier passes all 4 rubric items (mandatory (iv) PASS; (i)/(ii)/(iii) all PASS — 3-of-3 on the optional ≥2-of-3 floor).

## §4 Failure modes the test surfaces

The 6 scenarios pressure-test the following F-modes against GF-S's substrate-level closures (each scenario cites the candidate's spec §-anchor invoking the F-mode):

- **Scenario #1 cold-start initial-spec gating** surfaces:
  - **F25 (design starvation)** — substrate refuses to lights-out a cold-start factory per [ADR 0039](../../docs/adr/0039-p-19-variant-gf-s-work-unit-class.md) OPA floor (a); the scenario verifies the floor holds at day-0.
  - **F36 (instruction-following ceiling)** — guard 3 req-count budgeter enforces Yang/Llama ≤10-20 ceiling per [`specs/gf-s.md §4 scoping binding`](../specs/gf-s.md#4-discipline-binding).
  - **F57 (design-authority erosion)** — declared_stakes = caremark ⇒ forbid `automation-eligible` per OPA floor (b); the scenario verifies the floor surface.
- **Scenario #2 seeded F37 contradiction prompt pairs** surfaces:
  - **F37 (silent contradictory-prompt collapse)** — GF-S's load-bearing wager. The scenario IS the §3 falsifying-outcome test.
  - **F27 / F48 (shared-pretraining collusion)** — the Larbi MCC ≤0.55 ceiling is the comparison floor per [`specs/gf-s.md §6` P-15 contradiction-detector reliability](../specs/gf-s.md#6-open-carries); ensemble must improve on the floor.
  - **F51 (Ashby-deficient probabilistic guards)** — the ensemble's UNDETERMINED-to-Patrol escalation is the partial-RG admission per [`specs/gf-s.md §2 S8`](../specs/gf-s.md#2-substrate-composition); the scenario verifies the escalation surfaces explicitly, not silently.
- **Scenario #3 regime-transition substrate-measurement** surfaces:
  - **F25 (design starvation as substrate property)** — re-cast per [`specs/gf-s.md §3`](../specs/gf-s.md#3-methodology-shape); the scenario verifies the substrate-measured signal (scenario-set saturation + judge stability + Patrol absence-of-drift) actually flips the regime.
  - **F57 (design-authority erosion via convenience reclassification)** — OPA floors must hold post-flip per [ADR 0039](../../docs/adr/0039-p-19-variant-gf-s-work-unit-class.md).
- **Scenario #4 Patrol tier-3 cross-cycle audit** surfaces:
  - **F8 (stale-knowledge inversion)** — explicit Patrol audit invocation per [`specs/gf-s.md §3 cycle step 8`](../specs/gf-s.md#3-methodology-shape).
  - **F55 (behavioural drift)** — Patrol's operator-declared-invariant surface per [`specs/gf-s.md §2 S5`](../specs/gf-s.md#2-substrate-composition) (Patrol guards *invariants*, not historical baselines, because no baselines exist at day-0).
  - **F57 (design-authority erosion)** — versioned-config Rego policies Patrol-diffed across versions per [`specs/gf-s.md §4 regime classification`](../specs/gf-s.md#4-discipline-binding).
- **Scenario #5 four-guard × P-02 cost-ceiling interaction** surfaces:
  - **F26 (paraphrase/fan-out cost spike)** — 3-judge ensemble × every-cycle × four-guards × per-cycle is the cost driver per [`specs/gf-s.md §6` cost-stacking carry](../specs/gf-s.md#6-open-carries).
  - **CTR-E1 (10× cost-range)** — substrate-configurable per [`specs/gf-s.md §4 cost-ceiling binding`](../specs/gf-s.md#4-discipline-binding).
  - **CTR-E6 (CaMeL utility-tax)** — explicitly refused per [`specs/gf-s.md §2`](../specs/gf-s.md#2-substrate-composition) ("substrate kills the cycle at ceiling — no graceful-degradation mode"); the scenario verifies the refusal holds operationally.
- **Scenario #6 trifecta closure + perimeter typing** surfaces:
  - **F12 (lethal trifecta)** — explicit binding per [`specs/gf-s.md §4 trifecta closure`](../specs/gf-s.md#4-discipline-binding).
  - **F44 (production-credentialled scissors)** — substrate-disabled by default per [`specs/gf-s.md §2`](../specs/gf-s.md#2-substrate-composition).
  - **F33 / F51 (Ashby-deficient probabilistic guards)** — explicitly NOT trusted as primary closure per [`specs/gf-s.md §4 trifecta closure`](../specs/gf-s.md#4-discipline-binding); the scenario verifies P-01 + P-15 + P-25 are the closure stack, not a probabilistic substitute.
  - **F52 (tempting-wrong-hybrid)** — guard 4 perimeter typing is CaMeL-class declaration-time + P-25 runtime per call; the substrate refuses to substitute a probabilistic guard for a perimeter type per [`specs/gf-s.md §2`](../specs/gf-s.md#2-substrate-composition).

**F-mode coverage matrix** (for traceability):

| F-mode / CTR | One-line description | Scenario(s) | GF-S spec §-anchor |
|---|---|---|---|
| F8 | Stale knowledge / inversion at cross-cycle | #4 | §3 cycle step 8 + §10.1.8 back-fill |
| F12 | Lethal trifecta | #6 | §4 trifecta closure + §10.1.12 back-fill |
| F25 | Design starvation | #1, #3 | §2 + ADR 0039 OPA floor (a) |
| F26 | Paraphrase/fan-out cost spike | #5 | §6 cost-stacking carry |
| F27 | Shared-pretraining collusion (single-judge MCC ceiling) | #2 (load-bearing) | §2 S8 + §6 P-15 reliability |
| F33 | Ashby-deficient probabilistic guards | #6 | §4 trifecta closure |
| F36 | Instruction-following ceiling | #1 | §4 scoping + §2 S8 guard 3 |
| F37 | Silent contradictory-prompt collapse | #2 (load-bearing) | §1 + §2 S8 |
| F44 | Production-credentialled scissors | #6 | §2 commodity substrate |
| F46 | Single-model review blindspot | #2 | §4 bias-guard + §2 S6 P-14 |
| F48 | Shared-pretraining collusion (cross-judge) | #2 | §2 S8 + §6 |
| F51 | Ashby-deficient / LLM-judge recursion | #2, #6 | §6 F51 recursion carry |
| F52 | Tempting-wrong-hybrid (probabilistic-for-perimeter) | #6 | §4 trifecta + §2 S8 footnote |
| F55 | Behavioural drift | #4 | §3 cycle step 8 + §10.1.18 back-fill |
| F57 | Design-authority erosion | #1, #3, #4 | §4 regime classification + ADR 0039 |
| CTR-E1 | 10× cost-range | #5 | §4 cost-ceiling |
| CTR-E6 | CaMeL utility-tax | #5 | §2 (refused) |

17 F-mode/CTR cells; each maps to ≥1 scenario; each cell's spec §-anchor is auditable from [`specs/gf-s.md`](../specs/gf-s.md). Coverage is intentional: scenarios were designed FROM the F-mode list, not the reverse — a scenario without an F-mode anchor would be "looking for justification" and gets cut. **F40 last-mile drift is intentionally NOT in the matrix** — GF-S's spec explicitly admits F40 is substrate-unaddressed (the strongest standing critique of the substrate-first axis per [`specs/gf-s.md §6`](../specs/gf-s.md#6-open-carries)); a substrate-first lean-eval cannot pressure-test a methodology-layer carry. Carried to cross-candidate evaluator-brief comparison axes in §6.

## §5 Evaluator time + protocol

**Expected evaluator time: 1 day** (per [v1.2 plan § Phase 8](../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md#phase-8--lean-eval-design-one-brief-per-candidate-first-pressure-test-surface-revised-in-v12)). Breakdown:

- **Setup (~2 hours).** Initialize the substrate stack per [`specs/gf-s.md §2`](../specs/gf-s.md#2-substrate-composition): [P-01 sandbox (ADR 0010)](../../docs/adr/0010-p-01-sandbox-runtime.md) deny-all + intent-declared allow-list; [P-02 cost ceilings (ADR 0011)](../../docs/adr/0011-p-02-cost-ceilings.md) at GF-S-recommended budget (4-guard × ensemble-3 × per-cycle compounding admitted); [P-05 trajectory (ADR 0012)](../../docs/adr/0012-p-05-trajectory-capture.md) sub-ms content-addressed; [P-06 watchdog (ADR 0013)](../../docs/adr/0013-p-06-watchdog-tiers.md) Daemon/Triage/Patrol; [P-07 telemetry (ADR 0014)](../../docs/adr/0014-p-07-telemetry-ingestor.md); [P-08 holdout (ADR 0015)](../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md) substrate-typed builder-blindness; [P-10 coordination (ADR 0037)](../../docs/adr/0037-p-10-coordination-medium.md) Git-LFS + signed refs; [P-12 linter (ADR 0032)](../../docs/adr/0032-p-12-deterministic-linter-framework.md) loaded with EARS+GtWR rule pack; [P-14 judge router (ADR 0016)](../../docs/adr/0016-p-14-judge-router.md) with N=3 cross-family configuration; [P-15 four-guard mediator (ADR 0038)](../../docs/adr/0038-p-15-four-guard-mediator.md) fail-closed AND across guards; [P-19/GF-S classifier (ADR 0039)](../../docs/adr/0039-p-19-variant-gf-s-work-unit-class.md) with OPA hard-floors loaded; [P-22 polyglot index (ADR 0017)](../../docs/adr/0017-p-22-polyglot-codebase-index.md).
- **Scenario execution (~5 hours).** Run scenarios #1-#6 in order; each scenario produces (a) P-15 typed-envelope logs at `solutions/audit/p-15-runs/<scenario-id>.json` (PASS + FAIL envelopes both auditable per ADR 0038); (b) P-05 trajectory entries at `solutions/audit/p-05-runs/<scenario-id>/`; (c) P-07 telemetry envelopes at `solutions/audit/p-07-runs/<scenario-id>.json`; (d) Patrol-tier event logs at `solutions/audit/patrol/<scenario-id>.json` for scenario #4. Evaluator does NOT intervene mid-scenario; substrate-and-methodology-only.
- **Verdict pass (~1 hour).** Evaluator computes (i) per-scenario pass/fail against §2; (ii) §3 falsifying-outcome ensemble MCC + detection-rate across all 5 seeded contradictions in scenario #2; (iii) "pass cleanly" verdict per non-unified-attempt form. Verdicts written to `solutions/lean-eval/verdict-gf-s.md`.

**Protocol invariants** (per [auto-008 §Falsifier discipline escape-hatch enumeration](../decisions/auto-008-phase-8-dispatch-shape.md#r2-2--3-dec-1a-falsifying-pattern-canonical-terms-committed-in-this-brief)):

- **No out-of-mandate scope claim.** GF-S is greenfield-mandate-only; all 6 scenarios are greenfield-shaped by construction. Out-of-mandate scope claim does not apply.
- **No scenario-skip mid-run.** All 6 scenarios are executed; partial completion is a failure, not a skip.
- **No criterion-substitution.** §2 success criteria are committed; evaluator does NOT re-interpret mid-run. If §2 is defective, the brief is rewritten not the criterion swapped.

**Substrate ground-truth invariants.** Evaluator records substrate state at end-of-scenario (P-08 holdout partition state + P-15 typed-envelope log + P-05 trajectory + P-07 telemetry) so the lean-eval verdict is reconstructable from substrate state alone, not evaluator memory. The §3 falsifying-outcome ensemble MCC computation is reconstructable from `solutions/audit/p-15-runs/` per [ADR 0038](../../docs/adr/0038-p-15-four-guard-mediator.md) typed-envelope discipline.

**Hour-by-hour evaluator-time breakdown** (8-hour evaluator-day budget):

| Hour | Phase | Activity | Artifacts produced |
|---|---|---|---|
| 0:00-1:00 | Setup | Initialize substrate stack (P-01..P-22, P-10, P-12, P-15, P-19/GF-S); configure D-5 cost ceilings at GF-S-recommended budget | `solutions/setup/substrate-init.log` |
| 1:00-2:00 | Setup | Configure P-14 N=3 cross-family judges; load OPA hard-floors into P-19/GF-S; verify EARS+GtWR rule pack in P-12 | `solutions/setup/p-15-config.json` |
| 2:00-3:00 | Scenario #1 | Cold-start initial-spec gating: 1 intent block + 3 region scenarios through 4-guard mediator | `solutions/audit/p-15-runs/sc1.json` |
| 3:00-4:00 | Scenario #2 | Seeded F37 contradiction prompt pairs (5 seeded): single-judge baseline + 3-of-N ensemble | `solutions/audit/p-15-runs/sc2-seed{1..5}.json` |
| 4:00-5:00 | Scenario #3 | Regime-transition substrate-measurement: 10 `augmentation-required` cycles + flip event | `solutions/audit/p-05-runs/sc3/` + `solutions/audit/p-19-runs/sc3.json` |
| 5:00-5:30 | Scenario #4 | Patrol tier-3 cross-cycle audit: 6 cycles + 6 seeded invariant violations | `solutions/audit/patrol/sc4.json` |
| 5:30-6:30 | Scenario #5 | Four-guard × P-02 cost-ceiling interaction: 5 cycles under budget | `solutions/audit/p-02-runs/sc5.json` |
| 6:30-7:00 | Scenario #6 | Trifecta closure + perimeter typing: 3 trifecta-attempt edges | `solutions/audit/p-15-runs/sc6.json` + `solutions/audit/p-25-runs/sc6.json` |
| 7:00-7:30 | Verdict pass | Compute per-scenario pass/fail + §3 ensemble MCC + detection rate + "pass cleanly" verdict | `solutions/lean-eval/verdict-gf-s.md` |
| 7:30-8:00 | Reporting | Write verdict-gf-s.md with per-scenario verdicts + escape-hatch audit + over-run flags | (same file) |

Total 8 hours; scenarios consume ~5 hours; setup + verdict ~3 hours. If any scenario over-runs, evaluator records the over-run in the verdict file but does NOT skip subsequent scenarios — partial completion = scenario fails per [§5 protocol invariants no-scenario-skip clause](#5-evaluator-time--protocol).

## §6 Open critique references

GF-S's [`specs/gf-s.md §6 Open carries`](../specs/gf-s.md#6-open-carries) lists 6 open carries (F40 last-mile drift; P-15 contradiction-detector reliability; cost-stacking math; S9 minimum scenario-set size; F51 recursion; day-0 operator-intent illiteracy) plus a deferred CTR-C5 substrate-stack binding. The lean-eval engages 5 of these:

- **P-15 contradiction-detector reliability (load-bearing GF-S lean-eval candidate per [`specs/gf-s.md §6`](../specs/gf-s.md#6-open-carries))** → engaged by scenario #2 (the §3 falsifying-outcome test). The spec explicitly names this as the "load-bearing GF-S lean-eval candidate"; the lean-eval honors that framing. The substrate exposes ensemble N / family-rotation / quorum / UNDETERMINED-to-Patrol escalation as first-class parameters; the lean-eval uses GF-S-recommended baseline (N=3 cross-family + UNDETERMINED-to-Patrol). A full calibration sweep across the parameter space is downstream of this lean-eval — the lean-eval pressure-tests the baseline.
- **Cost-stacking math (CFO flag)** → engaged by scenario #5. The lean-eval verifies CTR-E6 admission ("substrate kills the cycle at ceiling — no graceful-degradation mode") holds and whether GF-S-recommended budget admits the 4-guard × ensemble-3 × per-cycle compounding.
- **S9 minimum viable scenario-set size N** → partially engaged by scenarios #1+#3. The lean-eval uses ≥3 region-shaped scenarios (the spec's day-0 floor) and 10 `augmentation-required` cycles (a working assumption for regime-transition saturation); does not sweep the parameter space.
- **F51 recursion (is S9 itself an LLM-judge primitive?)** → engaged by scenario #2 (the ensemble's UNDETERMINED-to-Patrol escalation IS the partial-RG admission). If the ensemble systematically returns UNDETERMINED on seeded contradictions, the recursion bites — the LLM-judge-fallback path is not deterministic enough.
- **Day-0 operator-intent illiteracy** → engaged partially by scenario #1 (the four-guard mediator's lint on the intent block is the substrate-level scaffold for operator intent; the lean-eval verifies the lint surfaces actionable feedback when the intent block fails R7/R8/R9 thresholds, not silent rejection).

The 1 open carry NOT engaged by this lean-eval:

- **F40 last-mile drift (substrate-unaddressed)** → not engaged. Per [`specs/gf-s.md §6`](../specs/gf-s.md#6-open-carries) ("Status: substrate-unaddressed; the strongest standing critique of the substrate-first axis. Carries forward to Phase-8 methodology lean-eval, not Phase-5 ADR."): F40 is a methodology-layer carry. A substrate-first lean-eval pressure-tests the substrate-first axis under its own claims; F40 is on the cross-candidate evaluator-brief's comparison axes (substrate-first axis vs methodology-first axis on last-mile drift mitigation), not on the per-candidate lean-eval.
- **CTR-C5 substrate-stack binding (deferred to Phase-5/architecture)** → not engaged. This is a future ADR carry per [`specs/gf-s.md §6`](../specs/gf-s.md#6-open-carries), not a Phase-6/8 closure.

## §7 Phase-7 cite obligations honored

Per the [`auto-008` per-candidate cite-obligation mapping table for GF-S](../decisions/auto-008-phase-8-dispatch-shape.md#high-confidence-mandatory-cite-obligations-3-cells--n-candidates):

### High-confidence mandatory cite obligation: NONE

Per the [`auto-008` Phase-7 cite-obligation propagation table](../decisions/auto-008-phase-8-dispatch-shape.md#phase-7-cite-obligation-propagation-load-bearing-pre-authored-mapping): "GF-S: *(none)* — GF-S aggregation matrix shows no high-confidence silent-absorption findings for this candidate." The YAML `phase-7-cite-obligations.high-confidence-mandatory` field is an empty array; no archive cite is owed in §1 / §4 / §6 of this brief.

This is consistent with GF-S's [back-fill notes §11](../backfill-notes/gf-s.md): the multi-lineage characterization (Atelier weak-overlap + Foundry inheritance + Tournament inheritance + Refinery weak inheritance, no single dominant) plus the substrate-first deliberate abstention from compounding-mechanism and knowledge-accumulation pattern means GF-S does NOT silently absorb the Atelier Compound-Engineering 4-step loop (back-fill §7.1.1 / §7.1.2 verdicts: `not-applicable-to-candidate-mandate`, not `absorbed`). The high-confidence cite-obligation that fires on 7 other specs does not fire on GF-S.

### Medium-confidence design input: §B.1 row 10 (Tournament structural-diversity)

Per [`backfill-notes/audit-silent-absorption.md §B.1 row 10`](../backfill-notes/audit-silent-absorption.md): "GF-S §3 step 5; §4 bias-guard | `04-evolutionary-tournament.md` §3.4 | GF-S '3-of-N family-diverse ensemble' — same Tournament-derived structural-diversity pattern; cited to overlap.md + ADR rather than archive. | medium | `tbd` row for GF-S × `04-evolutionary-tournament.md` §3.4."

**Engagement:** the §3 falsifying-outcome (P-15 ensemble MCC) IS the load-bearing lean-eval surface for the structural-diversity pattern. If the ensemble's MCC fails to improve on single-judge, the Tournament-derived structural-diversity claim — that family-diversity at the ensemble layer mitigates F27/F48 shared-pretraining collusion — is what fails. The §B.1 row-10 medium-confidence finding is therefore *exactly* the cell this lean-eval pressure-tests. The cite obligation is honored not by adding an archive cite to the spec (the spec cites the substrate-level ADR 0038 + overlap.md per the auditor's note), but by making the §3 falsifying-outcome **target the Tournament-derived pattern**: the falsifier's failure mode is precisely the failure mode the §B.1 row-10 cell flags.

### Historian load-bearing design inputs: H-2 + H-8 paired

Per [aggregation §4.1](../backfill-notes.md#41-load-bearing-gaps-5--phase-8-lean-eval-inputs):

- **H-2 (self-improving prompts pattern) + H-8 (prompt-self-improver role) — paired gap; methodology decision for GF-S / GF-M / U-A.**

**Decision for GF-S's lean-eval:** GF-S substrate is methodology-shape-agnostic and topology-agnostic per [`specs/gf-s.md §3 distinctive decisions 1+3`](../specs/gf-s.md#3-methodology-shape) — the substrate does NOT mandate a prompt-self-improver role. The self-improving-prompts pattern (H-2) lives at the methodology layer; the substrate provides the P-05 trajectory + P-07 telemetry + P-15 typed-envelope surfaces that a methodology-layer prompt-self-improver could consume, but the substrate-first axis explicitly defers the prompt-self-improver role (H-8) to the methodology overlay.

**For this lean-eval brief specifically:** scenario #2's seeded-F37-prompt-pair design implicitly engages H-2 (the seeded contradictions are the kind of input a self-improving-prompts loop would surface as candidate prompt rewrites), but the lean-eval does NOT instantiate a prompt-self-improver role for GF-S. Reason: GF-S's substrate refuses to take a methodology position; instantiating H-8 inside the lean-eval would conflate substrate evaluation with methodology evaluation, contaminating the §3 falsifying-outcome (we would be measuring "is GF-S substrate + prompt-self-improver-methodology good enough", not "is GF-S substrate's load-bearing wager correct"). The §3 falsifier targets the substrate-only contribution.

**Carried forward:** H-2/H-8 are surfaced in the cross-candidate evaluator-brief comparison axis (GF-S substrate-abstains vs GF-M methodology-binds vs U-A topology-binds on the self-improving-prompts question). Non-blocking for this brief.

### Cite-obligation summary (YAML `phase-7-cite-obligations` field)

- `high-confidence-mandatory`: 0 cites (empty array — GF-S has none per the auto-008 mapping table).
- `medium-confidence-design-inputs`: 1 cell (§B.1 row 10 Tournament §3.4 structural-diversity → engaged by scenario #2 + §3 falsifying-outcome).
- `historian-design-inputs`: 2 (H-2 + H-8 paired; substrate-abstains decision noted; carried to cross-candidate evaluator-brief).

## §8 References

**Candidate spec + back-fill notes (primary inputs):**

- [`specs/gf-s.md`](../specs/gf-s.md) — Phase-6 GF-S architecture spec; §0 ADR-citation index, §1 Overview, §2 Substrate composition, §3 Methodology shape, §4 Discipline binding, §5 Mandate fit, §6 Open carries.
- [`backfill-notes/gf-s.md`](../backfill-notes/gf-s.md) — Phase-7 back-fill audit; multi-lineage characterization, §10 F-mode coverage (19-of-20 absorbed), §11 surfaced TBDs.
- [`substrate-requirements/gf-s.md`](../substrate-requirements/gf-s.md) — Phase-4 substrate-requirements summary (referenced by spec §2 + §6).

**Phase-8 dispatch artifacts:**

- [`decisions/auto-008-phase-8-dispatch-shape.md`](../decisions/auto-008-phase-8-dispatch-shape.md) — this brief's parent dispatch decision; §Falsifier discipline (R2 #1-#4 rubric + R6 #2 partitioned-mandate non-unified form for GF-S), §Phase-7 cite-obligation propagation table, §Per-candidate lean-eval brief rubric.
- [`lean-evals/gf-m.md`](./gf-m.md) — Wave-8.1 exemplar (format model).

**Phase-7 inputs (cite-obligation source):**

- [`backfill-notes.md`](../backfill-notes.md) — Phase-7 aggregation matrix; §3.1 (high-confidence cite obligations — GF-S has none), §3.2 (medium-confidence TBDs), §4.1 (historian load-bearing gaps).
- [`backfill-notes/audit-silent-absorption.md`](../backfill-notes/audit-silent-absorption.md) — Phase-7 silent-absorption auditor output; §B.1 row 10 (GF-S × Tournament §3.4 medium-confidence).
- [`backfill-notes/audit-historian.md`](../backfill-notes/audit-historian.md) — Phase-7 historian auditor output (H-2 + H-8 paired gap).

**ADRs cited (substrate + discipline):**

- Common substrate: [ADR 0010](../../docs/adr/0010-p-01-sandbox-runtime.md) (P-01), [ADR 0011](../../docs/adr/0011-p-02-cost-ceilings.md) (P-02), [ADR 0012](../../docs/adr/0012-p-05-trajectory-capture.md) (P-05), [ADR 0013](../../docs/adr/0013-p-06-watchdog-tiers.md) (P-06), [ADR 0014](../../docs/adr/0014-p-07-telemetry-ingestor.md) (P-07), [ADR 0015](../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md) (P-08), [ADR 0016](../../docs/adr/0016-p-14-judge-router.md) (P-14), [ADR 0017](../../docs/adr/0017-p-22-polyglot-codebase-index.md) (P-22).
- Framework + designed-system: [ADR 0028](../../docs/adr/0028-p-19-eligibility-regime-classifier.md) (P-19 framework), [ADR 0032](../../docs/adr/0032-p-12-deterministic-linter-framework.md) (P-12).
- GF-S orphans: [ADR 0037](../../docs/adr/0037-p-10-coordination-medium.md) (P-10), [ADR 0038](../../docs/adr/0038-p-15-four-guard-mediator.md) (P-15).
- GF-S per-variant: [ADR 0039](../../docs/adr/0039-p-19-variant-gf-s-work-unit-class.md) (P-19/GF-S work-unit-class).
- Discipline: [ADR 0018](../../docs/adr/0018-discipline-bias-guard.md), [ADR 0019](../../docs/adr/0019-discipline-cognitive-escrow.md), [ADR 0020](../../docs/adr/0020-discipline-cost-ceiling.md), [ADR 0021](../../docs/adr/0021-discipline-holdout.md), [ADR 0022](../../docs/adr/0022-discipline-honesty.md), [ADR 0023](../../docs/adr/0023-discipline-knowledge-promotion.md), [ADR 0024](../../docs/adr/0024-discipline-regime-classification.md), [ADR 0025](../../docs/adr/0025-discipline-scoping.md), [ADR 0026](../../docs/adr/0026-discipline-three-loop.md), [ADR 0027](../../docs/adr/0027-discipline-trifecta-closure.md).

**Cross-cutting v3 docs:**

- [`decisions-captured.md`](../decisions-captured.md) — DEC-1.a working hypothesis (GF-S is mandate-aligned greenfield; does NOT carry DEC-1.a unified-attempt load), DEC-2 mandate-fit-per-(architecture × work-unit-class).
- [`failure-modes-v3.md`](../failure-modes-v3.md) — F-mode catalog (F8, F12, F25, F26, F27, F33, F36, F37, F44, F46, F48, F51, F52, F55, F57 + CTR-E1, CTR-E6 referenced).
- [`candidate-registry.md`](../candidate-registry.md) — GF-S candidate-registry entry.
- [`tracks/greenfield-substrate-first.md`](../tracks/greenfield-substrate-first.md) — Phase-3 GF-S track sketch.
- [`primitives/overlap.md`](../primitives/overlap.md) — Phase-4.2 P-19 verdict + P-08↔P-09 absorption + P-12↔P-16 absorption.

---

## Exemplar pre-fanout self-check results

This brief is a Wave-8.1 sibling, not the exemplar. Self-check items (a)-(g) are run per [`auto-008` per-candidate self-check rubric](../decisions/auto-008-phase-8-dispatch-shape.md#decision-round-2) and recorded here for traceability:

- **(a) `wc -w`:** target 5000-6500 (Light tier). **Actual: 5112 words. PASS** (within 5000-6500 band; 112-word margin above floor). Subagent target band per [`auto-008` tier-table](../decisions/auto-008-phase-8-dispatch-shape.md#decision-round-2) Light = 5000-6500.
- **(b) `ls` on cited file paths:** PASS. Cited v3 file paths verified at write time: `specs/gf-s.md`, `backfill-notes/gf-s.md`, `substrate-requirements/gf-s.md`, `tracks/greenfield-substrate-first.md`, `primitives/overlap.md`, `decisions/auto-008-phase-8-dispatch-shape.md`, `decisions-captured.md`, `failure-modes-v3.md`, `candidate-registry.md`, `backfill-notes.md`, `backfill-notes/audit-silent-absorption.md`, `backfill-notes/audit-historian.md`, `lean-evals/gf-m.md`, `docs/adr/0010-0017`, `docs/adr/0018-0027`, `docs/adr/0028`, `docs/adr/0032`, `docs/adr/0037`, `docs/adr/0038`, `docs/adr/0039`.
- **(c) `grep -cE "^## §[1-8]"`:** PASS — exactly 8 §-headers (§1 through §8).
- **(d) `grep "falsifying-outcome:"` + YAML value ≤80 words:** **PASS** — YAML field present in frontmatter (line 12); field value is **62 words** (verifies under ≤80-word limit). This is the load-bearing item per [`auto-008` self-check gate](../decisions/auto-008-phase-8-dispatch-shape.md#exemplar-pre-fanout-self-check-gate-load-bearing) (failure on (d) blocks fanout); PASS means fanout-equivalent (subagent output) is unblocked.
- **(e) `grep -c "phase-7-cite-obligations:"`:** **PASS** — YAML field present in frontmatter. Count = 2 across the full file (1 in YAML frontmatter at line 22, 1 prose mention at the §7 cite-obligation summary subsection citing the YAML field by name); the YAML field itself is uniquely present at line 22.
- **(f) Verbatim text-pull check:** PASS with `n/a` qualifier. This brief quotes short phrases from `specs/gf-s.md §1`, `§2`, `§3`, `§4`, `§6` verbatim (e.g., "the substrate's invariants are the load-bearing investment"; "substrate kills the cycle at ceiling — no graceful-degradation mode"; "Status: substrate-unaddressed; the strongest standing critique of the substrate-first axis. Carries forward to Phase-8 methodology lean-eval, not Phase-5 ADR.") but those are SHORT PHRASES, not multi-row binding rule tables. The brief does NOT cite a multi-row table from `specs/gf-s.md §0` (ADR-citation index) verbatim; references to ADRs use individual ADR markdown links per [`AGENTS-MD-bf4431be57`](../../AGENTS.md#verbatim-text-pull-when-citing-binding-rule-tables) carve-out for short phrases. `n/a` rationale: no binding-rule-table verbatim text-pull is invoked.
- **(g) `grep -cE "##? §[1-8]"`:** PASS — 8 §-headers from §1 through §8 (same as item c). The self-check H2 above this line is an H2 that does not match `§[1-8]` pattern, correctly excluded.
- **(h) DROPPED in Round 2** per [`auto-008 §Per-candidate lean-eval brief rubric self-check`](../decisions/auto-008-phase-8-dispatch-shape.md#decision-round-2) R3 #2. Cite-obligation honoring is enforced by falsification-designer auditor + post-fanout aggregation.

**Self-check verdict: PASS on load-bearing item (d).** Item (a) word count = 5112 (within Light-tier 5000-6500 band). Items (b)/(c)/(e)/(f)/(g) PASS. Item (h) DROPPED per Round-2 amendment.
