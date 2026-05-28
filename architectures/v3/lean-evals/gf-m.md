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
  Across 6 cold-start scenarios with seeded prompt-pair contradictions
  drawn from F37 corpus, GF-M's paraphrase divergence with N≥3
  cross-family paraphrasers + 95-percentile-divergence threshold detects
  <80% of seeded contradictions detected by single-judge baseline,
  measured from divergence vectors logged in solutions/audit/p-21-runs/.
  Equivalently: paraphrase-divergence MCC ≤0.55 on the same task.
phase-7-cite-obligations:
  high-confidence-mandatory:
    - compound-engineering-4-step-loop-archive-cite
  medium-confidence-design-inputs:
    - audit-silent-absorption.md-§B.1-cells-touching-gf-m
  historian-design-inputs:
    - H-2-self-improving-prompts-pattern
    - H-8-prompt-self-improver-role
---

# Lean-eval brief — GF-M (Greenfield methodology-first)

This brief is the lead-agent exemplar for Phase 8 Wave 8.1. It demonstrates the section structure, the YAML frontmatter shape (including the mandatory `falsifying-outcome:` field, the `mandate-scenario-split` field per [`auto-008 R6 #1`](../decisions/auto-008-phase-8-dispatch-shape.md#round-2-reviewer-amendments-folded-post-round-2-patches), and the `phase-7-cite-obligations` block), the §3 falsifying-outcome verbatim discipline, and the per-candidate Phase-7 cite-obligation honoring pattern. Per [auto-008 §Exemplar pre-fanout self-check gate](../decisions/auto-008-phase-8-dispatch-shape.md#exemplar-pre-fanout-self-check-gate-load-bearing), self-check items (a)-(g) are recorded at the end of this file before Wave 8.1 dispatches.

## §1 Candidate + scenario set

**Candidate.** GF-M is the greenfield-mandate-only methodology-first candidate (greenfield-light tier in [`auto-008` tier-table](../decisions/auto-008-phase-8-dispatch-shape.md#decision-round-2)). Per [`specs/gf-m.md §1`](../specs/gf-m.md): a two-regime reversible-commitment factory where the per-cycle process *is* the architecture and the substrate is whatever the cycle requires, not vice-versa. Day-0 entry-mode: cold-start with a prose-shaped domain idea + adjacent-domain priors, no codebase, no scenarios, no issue queue. GF-M's `candidate-mandate: greenfield` and `mandate-scenario-split: {greenfield: 6, brownfield: 0}` per the YAML frontmatter — GF-M does NOT carry the DEC-1.a unified-attempt load, so the scenario set is single-bloc (greenfield-only) and the "pass cleanly" definition uses the non-unified-candidate form (≥80% scenarios pass + falsifying-outcome NOT triggered) per [`auto-008 §Falsifier discipline (R2 #3)`](../decisions/auto-008-phase-8-dispatch-shape.md#falsifier-discipline-load-bearing).

**Scenario set source.** Hybrid: scenarios are drawn from (a) the corpus F-mode catalog with focus on F25 (design starvation), F37 (silent contradictory-prompt collapse), F40 (last-mile drift), F41 (under-defined intent debt), F46 (single-model review blindspot) — i.e., the failure modes GF-M's two-regime split + paraphrase-divergence defense + cross-model review explicitly mitigates — and (b) GF-M's own scenario-derivation primitive at [`specs/gf-m.md §3 Regime A`](../specs/gf-m.md#3-methodology-shape) (the 4-phase Regime-A cycle: intent draft → paraphrase divergence → tiny probe → promote/reverse). The two halves are not redundant: corpus scenarios provide F-mode coverage and adversarial pressure; candidate-derived scenarios surface what the methodology's own design predicts as productive vs paralytic.

**Scenarios (6 total, all greenfield).**

1. **Cold-start single-slice trajectory (corpus + candidate-derived).** Day-0 operator dictates a single prose intent (e.g., "a task-queue web service that exposes priority-FIFO semantics under burst load"); evaluator runs ≥3 Regime-A cycles before any slice promotes to Regime B. Surfaces: F25 (design starvation as a property of Regime A, not a failure), F41 (intent debt during the malleable phase). Pass: ≥1 slice promotes within 5 cycles AND each cycle's paraphrase-divergence vector is logged and substrate-implementable. **Implements DEC-2 work-unit class `initial-spec`.**

2. **Seeded-contradiction prompt pair (corpus F37).** Evaluator constructs 5 prompt-pair contradictions from the [F37 corpus](../failure-modes-v3.md) (e.g., "FIFO priority queue" + "LIFO under contention" both stated in the same intent block); single-judge LLM baseline scores each pair (MCC ≤ 0.55 expected per Larbi corpus); N≥3 cross-family paraphrasers from [P-21 (ADR 0041)](../../docs/adr/0041-p-21-paraphrase-divergence.md) score each pair via post-condition divergence. **This is GF-M's load-bearing falsifier scenario** (see §3). Pass: paraphrase-divergence detection rate ≥80% of contradictions; MCC > 0.55.

3. **Slice-coherence transition (candidate-derived OQ-T1).** Evaluator authors 4 paired intent+scenario commitments in Regime A; verifies whether `slice-coherence-based` transition criterion ("at least one end-to-end scenario passes through the slice without an intent gap") is operationally applicable — i.e., does the substrate's [P-08 holdout (ADR 0015)](../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md) + [P-05 trajectory (ADR 0012)](../../docs/adr/0012-p-05-trajectory-capture.md) provide enough state to evaluate slice coherence without operator-voluntary judgment? Surfaces: F40 last-mile drift (transition is the "shipped" boundary); OQ-T3 Regime-A→B handoff substrate protocol. Pass: transition is mechanically auditable from substrate state, not operator-asserted.

4. **Regime-B cross-model review panel sanity check (corpus F46 + CTR-D7 contradiction).** Evaluator runs ≥3 Regime-B scenarios on promoted slices with a cross-model panel of 3 model-family-diverse reviewers (per [GF-M §3 Regime B](../specs/gf-m.md#3-methodology-shape)); compares against same-model baseline; tests CTR-D7 same-model-review contradiction GF-M explicitly takes on the grounds "greenfield has no out-of-distribution ground truth." Surfaces: F46, F55 behavioural drift. Pass: cross-model panel catches ≥1 contradiction class that same-model misses, AND K=5 consistency on the panel-judged work ≥90% (Jaymin Automation bar per [GF-M §3](../specs/gf-m.md#3-methodology-shape)).

5. **Paraphrase fan-out × cost-ceiling interaction (candidate-derived OQ-T2 + corpus F-mode CTR-E6).** Evaluator runs 5 Regime-A cycles under D-5 cost ceilings configured at the GF-M-recommended budget; measures whether paraphrase fan-out (N×single-cycle cost; ~3×-4× by candidate design) triggers premature ceiling hits, and whether CTR-E6 CaMeL utility-tax behaves as the spec admits (substrate safety primitives have non-zero cost; the ceiling explicitly admits them per [GF-M §4 cost ceiling](../specs/gf-m.md#4-discipline-binding)). Surfaces: CTR-E1 cost-range, F26 paraphrase-cost spike. Pass: ≥80% of cycles complete within budget AND ceiling-hit recovery (P-02-mediated truncation) does not silently disable a paraphraser.

6. **Knowledge promotion deferred until post-Regime-B (corpus F8 + F55, candidate-derived).** Evaluator confirms no `docs/solutions/` accumulation in Regime A (per [GF-M §3](../specs/gf-m.md#3-methodology-shape) — "no `docs/solutions/` accumulation in Regime A"); after Regime B has produced enough cycles to evaluate, evaluator triggers pattern→standard promotion per [ADR 0023 knowledge promotion](../../docs/adr/0023-discipline-knowledge-promotion.md) (this is one of GF-M's three Phase-7 high-confidence cite obligations — the Compound-Engineering 4-step loop carries the promotion semantics; see §7). Surfaces: F8 self-referential bootstrap, F55 self-referential drift at cold-start. Pass: 0 entries in `docs/solutions/` before first slice promotes AND ≥1 promotion event after ≥10 Regime-B cycles complete.

The 6 scenarios cover GF-M's 4 mandate-fit work-unit-classes (initial-spec via #1+#3; mvp via #1+#3+#6; post-mvp-evolution via #4+#5+#6; regression-fix via #4) and pressure-test all of GF-M's load-bearing claims.

**Why these 6 scenarios (scenario-selection rationale).** GF-M's spec carries 7 open carries at [`specs/gf-m.md §6`](../specs/gf-m.md#6-open-carries) (OQ-T1 slice-coherence; OQ-T2 paraphrase-fan-out × cost-ceiling; OQ-T3 Regime-A→B handoff; OQ-T4 cross-model × provider-abstraction; OQ-T5 two-regime split as falsifiable design claim; OQ-T6 P-21 calibration sweep; Brier pace-layer subsumption). The lean-eval's 6-scenario set was chosen to engage 5 of the 7 (OQ-T1/T2/T3/T4/T6 — see [§6 Open critique references](#6-open-critique-references) below) while keeping the 1-day evaluator-time bound. The remaining two open carries (OQ-T5 alternative-design pressure; pace-layer subsumption) are documentation-layer questions that don't reduce to a 1-day evaluator scenario; they remain Phase-3-adversarial-pass-and-Phase-7-backfill carry-forwards. Scenario selection prioritized (a) the candidate's load-bearing wager (paraphrase-divergence-as-F37-defense → scenario #2 is the §3 falsifying-outcome test), (b) the mandate-fit work-unit-class coverage (all 4 of GF-M's `greenfield` work-units land in ≥1 scenario), and (c) failure-mode coverage across the 8 F-modes the spec invokes (F8/F25/F26/F34/F37/F40/F41/F46/F55 — listed in [§4 below](#4-failure-modes-the-test-surfaces)). The 6-scenario count is the floor for the auto-008 §1 rubric requirement; GF-M's design lets the floor suffice.

## §2 Success criteria

A GF-M lean-eval result "passes cleanly" (per [auto-008 §Falsifier discipline R2 #3 non-unified form](../decisions/auto-008-phase-8-dispatch-shape.md#falsifier-discipline-load-bearing)) iff:

- **(a) Quantitative gate:** ≥80% of the 6 scenarios pass the §1 success criteria (i.e., ≥5 of 6 scenarios pass).
- **(b) Falsifying-outcome gate:** the §3 falsifying-outcome is NOT triggered on any scenario.

**Per-scenario success criteria (verbatim from §1 above):**

1. **Cold-start single-slice trajectory.** ≥1 slice promotes within 5 Regime-A cycles AND each cycle's paraphrase-divergence vector is logged to `solutions/audit/p-21-runs/<cycle-id>.json` and substrate-implementable (i.e., the vector can be recomputed deterministically from the trajectory).
2. **Seeded-contradiction prompt pair.** Paraphrase-divergence detection rate ≥80% across 5 seeded contradictions (≥4 of 5 detected); paraphrase-divergence Matthews Correlation Coefficient (MCC) > 0.55 against the labeled ground-truth contradiction/no-contradiction set.
3. **Slice-coherence transition.** Transition decision is mechanically reconstructable from `P-08 holdout` partition state + `P-05 trajectory` event log for the slice; no operator-voluntary "yes the slice is coherent" assertion is required (substrate state IS the verdict).
4. **Regime-B cross-model review panel.** Cross-model panel surfaces ≥1 contradiction class that same-model baseline misses (across 3 scenarios); K=5 consistency on panel-judged work ≥90% (Jaymin Automation bar).
5. **Paraphrase fan-out × cost-ceiling.** ≥80% of 5 cycles complete within D-5-configured budget (≥4 of 5); when budget is hit, P-02-mediated truncation does NOT silently disable any individual paraphraser (truncation surfaces in trajectory as an explicit event, not as a missing paraphraser response).
6. **Knowledge promotion deferred.** `docs/solutions/` entry-count = 0 before first slice promotes AND ≥1 entry-promotion event after ≥10 Regime-B cycles complete on the promoted slice(s).

**Note on success-criteria vs falsifying-outcome distinction (per [`auto-008 §Falsifier discipline`](../decisions/auto-008-phase-8-dispatch-shape.md#falsifier-discipline-load-bearing)):** failing the §2 success criteria can be implementation noise (a paraphraser misconfigured; a P-08 partition bug; an operator misreading prompt). Triggering the §3 falsifying-outcome is the methodology's load-bearing claim (paraphrase-as-F37-defense) being wrong — a different kind of failure that the candidate cannot recover from without re-shaping its load-bearing wager.

## §3 Falsifying outcome

**Falsifying-outcome verbatim (≤80 words from YAML, repeated here for §3-vs-YAML consistency per [auto-008 falsification-designer rubric item (iv)](../decisions/auto-008-phase-8-dispatch-shape.md#r2-1-falsification-designer-concreteness-rubric-3-item-mechanical)):**

> Across 6 cold-start scenarios with seeded prompt-pair contradictions drawn from F37 corpus, GF-M's paraphrase divergence with N≥3 cross-family paraphrasers + 95-percentile-divergence threshold detects <80% of seeded contradictions detected by single-judge baseline, measured from divergence vectors logged in `solutions/audit/p-21-runs/`. Equivalently: paraphrase-divergence MCC ≤0.55 on the same task.

**Rationale.** GF-M's central wager (per [`specs/gf-m.md §1 load-bearing claim`](../specs/gf-m.md#1-overview)) is that paraphrase divergence across N model-family-diverse paraphrasers is a **stronger F37 (silent contradictory-prompt collapse) defense than any single LLM-judge**, because Larbi MCC ≤ 0.55 on single-judge contradiction-detection is treated as disqualifying. If the lean-eval shows paraphrase divergence has its OWN MCC ceiling at the same ≤0.55 bound on the same task, the candidate's load-bearing wager is empirically wrong — paraphrase-divergence does not improve on the single-judge baseline, and the entire two-regime split (which depends on paraphrase divergence as the Regime-A gate; see [`specs/gf-m.md §3 Regime A phase 2`](../specs/gf-m.md#3-methodology-shape)) loses its empirical justification.

**Why this falsifier and not another.** Three alternative falsifiers were considered:

- "If ≥1 slice cannot promote in any reasonable cycle-count" — this is failure-mode-of-implementation, not the load-bearing claim. Slice-coherence operationalization is OQ-T1 (an open carry, not the central wager).
- "If Regime-B steady-state never materializes" — this is mandate-fit collapse, not falsification of the methodology's load-bearing primitive. The two-regime split is a design choice; its productivity is mandate-fit not load-bearing.
- "If cross-model review panel is no better than same-model on the K=5 bar" — this is a separate empirical question (F46 mitigation efficacy) but not the candidate's *central* wager. F46 mitigation is a property GF-M shares with multiple other candidates.

The paraphrase-divergence F37 defense is GF-M's *distinctive* load-bearing wager — the claim that distinguishes GF-M from a single-judge-based greenfield methodology. The falsifier targets exactly this distinction.

**Machine-checkability.** Per [auto-008 falsification-designer rubric 3-item check](../decisions/auto-008-phase-8-dispatch-shape.md#r2-1-falsification-designer-concreteness-rubric-3-item-mechanical):

- **(i) Metric:** `detection-rate-vs-single-judge-baseline` (countable; % of seeded contradictions detected) AND `MCC` (Matthews Correlation Coefficient, numeric).
- **(ii) Artifact state:** `solutions/audit/p-21-runs/<scenario-id>.json` divergence-vector logs (specific directory, specific filename pattern). The vectors are produced by [P-21 (ADR 0041)](../../docs/adr/0041-p-21-paraphrase-divergence.md)'s deterministic LiteLLM + sentence-transformers pipeline; trajectory-replayable per [P-05 (ADR 0012)](../../docs/adr/0012-p-05-trajectory-capture.md).
- **(iii) Threshold:** `< 80%` detection rate OR `≤ 0.55` MCC. Both numeric, both single-direction comparisons.
- **(iv) §3-vs-YAML consistency:** the YAML field and this §3 statement name the same metric (paraphrase-divergence detection rate + MCC), same artifact location (`solutions/audit/p-21-runs/`), same threshold (<80% / ≤0.55).

The falsifier passes all 4 rubric items (pass on (iv) mandatory; pass on ≥2 of (i)-(iii)).

## §4 Failure modes the test surfaces

The 6 scenarios are designed to surface the following failure modes — for each scenario, the specific F-mode(s) the scenario pressure-tests, citing the candidate's spec §5 (failure modes) or §3 (methodology shape) where applicable:

- **Scenario #1 cold-start trajectory** surfaces:
  - **F25 (design starvation)** — Regime A intentionally produces low throughput; the scenario tests whether the candidate's recasting of F25 as a regime property ("F25 design starvation is re-cast as a property of the regime, not a failure" per [`specs/gf-m.md §3`](../specs/gf-m.md#3-methodology-shape)) is operationally sustained or whether operators experience the slowness as failure.
  - **F41 (under-defined intent debt)** — during the malleable phase, intent debt is expected and the cycle's promote/reverse gate is designed to bound it. The scenario tests whether intent debt actually bounds across ≥5 cycles or accumulates.
- **Scenario #2 seeded-contradiction prompt pair** surfaces:
  - **F37 (silent contradictory-prompt collapse)** — GF-M's load-bearing wager defense. The scenario IS the §3 falsifying-outcome test.
  - **Larbi MCC ceiling** — single-judge baseline MCC ≤ 0.55 is the comparison floor; if paraphrase-divergence is not better, the candidate's load-bearing wager fails.
- **Scenario #3 slice-coherence transition** surfaces:
  - **F40 (last-mile drift)** — the Regime-A→B transition IS the "shipped" boundary; OQ-T1 (slice-coherence operational definition) is the open carry the scenario engages.
  - **F34 (cross-layer drift)** — substrate's [P-06 watchdog Patrol tier (ADR 0013)](../../docs/adr/0013-p-06-watchdog-tiers.md) is the Regime-A→B drift detector per [`specs/gf-m.md §3 Patrol-tier monitoring`](../specs/gf-m.md#3-methodology-shape); the scenario verifies Patrol catches the regime change.
- **Scenario #4 Regime-B cross-model review panel** surfaces:
  - **F46 (single-model review blindspot)** — cross-model panel is the explicit mitigation; the scenario verifies efficacy.
  - **F55 (behavioural drift)** — K=5 consistency floor; behavioural drift surfaces as K=5 < 90%.
  - **CTR-D7 contradiction (corpus)** — GF-M takes CTR-D7 on the grounds "greenfield has no out-of-distribution ground truth"; the scenario tests whether this grounds-clause holds empirically.
- **Scenario #5 paraphrase fan-out × cost-ceiling** surfaces:
  - **F26 (paraphrase-cost spike)** — N× cost multiplier interacting with D-5 caps.
  - **CTR-E6 (CaMeL utility-tax)** — substrate safety primitives have non-zero cost; the scenario verifies the cost-ceiling explicitly admits this.
- **Scenario #6 knowledge promotion deferred** surfaces:
  - **F8 (self-referential bootstrap)** — at cold-start, all "knowledge" is from a tiny number of cycles; deferring promotion mitigates F8.
  - **F55 (self-referential drift)** — the scenario verifies the deferral discipline holds across cycles, not just at cold-start.

The cross-cutting failure-mode coverage (8 distinct F-modes + 2 corpus CTRs) is the lean-eval's load. **No scenario engages a failure mode F-mode is not enumerated in GF-M's spec §3-§4 or in the corpus** — i.e., the lean-eval does NOT smuggle in failure modes the candidate did not commit to defending.

**F-mode coverage matrix.** For traceability across scenarios:

| F-mode / CTR | Description (one-line from corpus) | Scenario(s) | GF-M spec § |
|---|---|---|---|
| F8 | Self-referential bootstrap at cold-start | #6 | §3 ("No `docs/solutions/` accumulation in Regime A") |
| F25 | Design starvation | #1 | §3 (Regime A re-cast) |
| F26 | Paraphrase-cost spike | #5 | §2 (P-21 cost driver) |
| F34 | Cross-layer drift | #3 | §3 (Patrol-tier P-06 monitoring) |
| F37 | Silent contradictory-prompt collapse | #2 (load-bearing) | §1 load-bearing claim + §3 phase 2 |
| F40 | Last-mile drift (the "shipped" boundary) | #3 | §3 slice-coherence transition |
| F41 | Under-defined intent debt | #1 | §3 Regime A 4-phase cycle |
| F46 | Single-model review blindspot | #4 | §3 Regime B cross-model panel |
| F55 | Behavioural drift (self-referential) | #4, #6 | §3 (Patrol-tier) + §3 (deferred promotion) |
| CTR-D7 | Same-model review contradiction | #4 | §3 (taken-on grounds for greenfield) |
| CTR-E1 | 10× cost range | #5 | §6 OQ-T2 |
| CTR-E6 | CaMeL utility-tax (safety primitives have non-zero cost) | #5 | §4 cost-ceiling discipline |

12 cells; each maps to ≥1 scenario; each cell's spec §-anchor is auditable from `specs/gf-m.md`. **Coverage is intentional, not coincidental:** the scenarios were designed FROM the F-mode list, not the reverse — a scenario without an F-mode anchor would be a "scenario looking for a justification" and gets cut.

## §5 Evaluator time + protocol

**Expected evaluator time: 1 day** (per [v1.2 plan § Phase 8](../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md#phase-8--lean-eval-design-one-brief-per-candidate-first-pressure-test-surface-revised-in-v12) ~1-day-per-candidate bound). Breakdown:

- **Setup (~2 hours).** Evaluator initializes the substrate stack per [`specs/gf-m.md §2`](../specs/gf-m.md#2-substrate-composition): P-01 sandbox, P-02 cost ceilings configured at the GF-M-recommended budget (~3-4× single-cycle cost to admit the paraphrase fan-out), P-05 trajectory capture, P-06 watchdog Patrol tier, P-07 telemetry, P-08 substrate-typed holdout (OPA-mediated), P-14 judge router, P-22 polyglot codebase index, P-20 reversibility primitive (event-sourced), P-21 paraphrase divergence (LiteLLM router with N=3 cross-family tags + sentence-transformer divergence metric + 95-percentile threshold).
- **Scenario execution (~5 hours).** Run scenarios #1-#6 in order. Each scenario produces (a) a trajectory log under `solutions/audit/p-21-runs/<scenario-id>.json` for paraphrase-divergence vectors, (b) a Patrol-tier event log under `solutions/audit/patrol/<scenario-id>.json` for cross-layer drift detection, (c) a `solutions/lean-eval/<scenario-id>/` directory for scenario-specific artifacts (intent commitments, paired scenarios, promote/reverse decisions, panel verdicts). Evaluator does NOT intervene mid-scenario; substrate-and-methodology-only.
- **Verdict pass (~1 hour).** Evaluator computes (i) per-scenario pass/fail against §2 success criteria; (ii) the §3 falsifying-outcome check (detection-rate + MCC across all 5 seeded contradictions in scenario #2); (iii) the "pass cleanly" verdict per [auto-008 §Falsifier discipline R2 #3 non-unified form](../decisions/auto-008-phase-8-dispatch-shape.md#falsifier-discipline-load-bearing). Verdicts written to `solutions/lean-eval/verdict-gf-m.md`.

**Protocol invariants** (per [auto-008 §Falsifier discipline escape-hatch enumeration](../decisions/auto-008-phase-8-dispatch-shape.md#r2-2--3-dec-1a-falsifying-pattern-canonical-terms-committed-in-this-brief)):

- **No out-of-mandate scope claim.** GF-M is greenfield-mandate-only; all 6 scenarios are greenfield-shaped by construction. Out-of-mandate scope claim does not apply (GF-M does not claim brownfield).
- **No scenario-skip mid-run.** All 6 scenarios are executed; partial completion is a failure, not a skip.
- **No criterion-substitution.** §2 success criteria are committed in this brief; evaluator does NOT re-interpret them mid-run. If §2 is defective, the brief is rewritten not the criterion swapped.

**Substrate ground-truth invariants.** The evaluator records the substrate state at end-of-scenario (`P-08 holdout partition state` + `P-20 reversibility primitive event log` + `P-21 paraphrase divergence vectors`) so the lean-eval verdict is reconstructable from substrate state alone, not from evaluator memory. Per the [§3 falsifying-outcome machine-checkability rubric](#3-falsifying-outcome): the verdict on scenario #2 is reconstructable from `solutions/audit/p-21-runs/`.

**Hour-by-hour evaluator-time breakdown** (8-hour evaluator-day budget):

| Hour | Phase | Activity | Artifacts produced |
|---|---|---|---|
| 0:00-0:30 | Setup | Initialize substrate stack (P-01..P-22, P-20, P-21) per `specs/gf-m.md §2`; configure D-5 cost ceilings | `solutions/setup/substrate-init.log` |
| 0:30-2:00 | Setup | Configure P-21 baseline (N=3 cross-family LiteLLM, sentence-transformer divergence, 95-pct threshold); validate cross-family tags reach 3 distinct provider families | `solutions/setup/p-21-config.json` |
| 2:00-3:00 | Scenario #1 | Cold-start single-slice trajectory: 5 Regime-A cycles on operator-dictated intent | `solutions/audit/p-21-runs/sc1-*.json`; `solutions/lean-eval/sc1/` |
| 3:00-4:00 | Scenario #2 | Seeded-contradiction prompt pair (F37): 5 seeded contradictions × single-judge baseline + paraphrase-divergence | `solutions/audit/p-21-runs/sc2-seed{1..5}.json` |
| 4:00-4:30 | Scenario #3 | Slice-coherence transition: 4 intent+scenario pairs, verify substrate-only auditability | `solutions/audit/patrol/sc3.json` |
| 4:30-5:30 | Scenario #4 | Regime-B cross-model panel: 3 scenarios on promoted slices | `solutions/lean-eval/sc4/panel-verdicts.json` |
| 5:30-6:30 | Scenario #5 | Paraphrase fan-out × cost-ceiling: 5 cycles under D-5 caps | `solutions/audit/p-02-ceilings.json` |
| 6:30-7:00 | Scenario #6 | Knowledge promotion deferred: verify 0 entries before first promote; ≥1 entry after ≥10 Regime-B cycles | `solutions/lean-eval/sc6/promotion-log.json` |
| 7:00-7:30 | Verdict pass | Compute per-scenario pass/fail + §3 falsifier check + "pass cleanly" verdict | `solutions/lean-eval/verdict-gf-m.md` |
| 7:30-8:00 | Reporting | Write verdict-gf-m.md with detection-rate, MCC, per-scenario verdicts, escape-hatch audit | (same file) |

Total 8 hours; scenarios consume ~5 hours; setup + verdict ~3 hours. If any scenario over-runs, evaluator records the over-run in the verdict file but does NOT skip subsequent scenarios — partial completion = scenario fails per [§5 protocol invariants no-scenario-skip clause](#5-evaluator-time--protocol).

## §6 Open critique references

GF-M's [`specs/gf-m.md §6 Open carries`](../specs/gf-m.md#6-open-carries) lists 7 open critique findings; the lean-eval engages 5 of them directly:

- **OQ-T1 Slice-coherence operational definition** → engaged by scenario #3 (slice-coherence transition test). The lean-eval verifies whether the substrate state (P-08 partition + P-05 trajectory) provides enough state to mechanically auditor the transition criterion. **If scenario #3 fails, OQ-T1 is escalated as a Phase-5/6 methodology-spec carry.**
- **OQ-T2 Paraphrase fan-out × cost-ceiling interaction** → engaged by scenario #5 (cost-ceiling test). The lean-eval verifies CTR-E6 CaMeL utility-tax admission and whether D-5 caps trigger premature ceiling hits.
- **OQ-T3 Regime-A→B handoff substrate protocol** → partially engaged by scenario #3 (slice-coherence transition). The lean-eval surfaces whether a new substrate primitive is needed for the transition (currently the spec uses P-05 trajectory + P-08 holdout); if scenario #3 reveals a transition-state gap that those primitives don't cover, OQ-T3 escalates.
- **OQ-T4 Cross-model paraphrase × provider-abstraction interaction** → engaged by scenarios #2 + #4 (both use cross-family panels). The lean-eval verifies LiteLLM-router-default works for paraphrase + cross-model review; per-provider-aligned-profiles fallback (per CTR-C4) is NOT tested in this lean-eval — that's a Phase-5 ADR seed.
- **OQ-T6 P-21 calibration sweep** → engaged by scenario #2 (the §3 falsifying-outcome test). The lean-eval uses the GF-M-recommended baseline calibration (N=3 cross-family + 95-percentile-divergence threshold). The full calibration sweep (varying N, divergence-metric, threshold across the parameter space) is downstream of this lean-eval per [`specs/gf-m.md §6 OQ-T6`](../specs/gf-m.md#6-open-carries) — the lean-eval pressure-tests the baseline calibration; the sweep characterizes the parameter-space.

The 2 open carries NOT engaged by this lean-eval:

- **OQ-T5 Two-regime split as falsifiable design claim** → not engaged. This is a Phase-3 adversarial-pass question (whether continuous-Regime-A-only is a valid alternative); the lean-eval tests the chosen two-regime design under its own claims, not against alternatives.
- **Brier pace-layer subsumption (Phase-7 back-fill carry)** → not engaged. Documentation-layer question, not a methodology-pressure question.

## §7 Phase-7 cite obligations honored

Per the [`auto-008` per-candidate cite-obligation mapping table for GF-M](../decisions/auto-008-phase-8-dispatch-shape.md#high-confidence-mandatory-cite-obligations-3-cells--n-candidates):

### High-confidence mandatory cite obligation (1 cell)

**Compound-Engineering 4-step loop verbatim cite.** Per [aggregation §3.1 finding #2](../backfill-notes.md#31-high-confidence-findings-3--apply-precedence-rule): GF-M's `specs/gf-m.md §3 Regime B` describes the Compound-Engineering loop as "Standard Compound-Engineering loop (plan → work → review → compound, [report 03](../../../research/03-every-compound-engineering.md))". Per the silent-absorption audit, the 4-step loop appears verbatim across 7 specs (GF-M / U-A / U-B / U-C / D7-U-1 / BF-S / BF-M) with only GF-M citing a `research/03-` primary source; **none cite the archive v0.2 correction** at `archive/synthesis-v1-v2/13-round-2-synthesis.md`.

**Cite honored in this brief**: scenario #6 (knowledge promotion deferred) cites [ADR 0023 knowledge promotion](../../docs/adr/0023-discipline-knowledge-promotion.md) as the discipline binding; per the Phase-7 cite obligation, the lean-eval brief carries the archive lineage cite for the Compound-Engineering 4-step loop:

> The Compound-Engineering loop `plan → work → review → compound` (referenced in [`specs/gf-m.md §3 Regime B`](../specs/gf-m.md#3-methodology-shape)) is v0.2-canonical per [`archive/synthesis-v1-v2/13-round-2-synthesis.md`](../../archive/synthesis-v1-v2/13-round-2-synthesis.md) — the archive Round-2 synthesis that promoted the 4-step shape from `research/03-` to load-bearing methodology vocabulary. Scenario #6's knowledge-promotion deferral discipline operates against this 4-step loop's "compound" phase (the post-cycle pattern→standard promotion step).

### Medium-confidence design inputs (consulted)

Per [aggregation §3.2 reconciliation TBDs](../backfill-notes.md#32-medium-confidence-findings-7--trigger-tbd-reconciliation-rows): subagents authoring Wave-8.1 briefs consult [`backfill-notes/audit-silent-absorption.md` §B.1`](../backfill-notes/audit-silent-absorption.md) for cells touching their candidate. **GF-M's medium-confidence cells (consulted for this exemplar):**

- The audit-silent-absorption auditor's §B.1 enumerates 7 medium-confidence cells across all 10 candidates. For GF-M specifically (per inspection of the audit file), no medium-confidence cell is load-bearing for this lean-eval brief design (GF-M's distinctive minimalism — no contested-primitive references — means most medium-confidence findings target framework-ADR-claiming candidates, not GF-M). **Engagement: no §B.1 cell directly shapes a scenario or success-criterion in this brief.** Flagged for completeness.

### Historian load-bearing design inputs (engaged)

Per [aggregation §4.1 historian load-bearing gaps](../backfill-notes.md#41-load-bearing-gaps-5--phase-8-lean-eval-inputs):

- **H-2 (self-improving prompts pattern) + H-8 (prompt-self-improver role)** — paired gap; methodology decision for GF-S / GF-M / U-A. **For GF-M:** the self-improving-prompts pattern is structurally aligned with the Regime-A paraphrase-divergence step (each cycle's divergence vector IS the signal for prompt refinement; the operator's promote-or-reverse decision IS the self-improvement loop closer). **Decision for GF-M's lean-eval:** the self-improving-prompts pattern is implicitly absorbed by Regime-A's 4-phase cycle (intent draft → paraphrase divergence → tiny probe → promote/reverse); no explicit "prompt-self-improver" role is added because the operator IS the role per GF-M's L3-augmentation Regime-A operating mode. **Methodology-shape note for `specs/gf-m.md §3`** (carried as a Phase-8-followup advisory if not adopted): consider naming the prompt-self-improver role explicitly to make the H-2/H-8 alignment auditable. Non-blocking.

### Cite-obligation summary (YAML `phase-7-cite-obligations` field)

- `high-confidence-mandatory`: 1 cite (Compound-Engineering 4-step loop archive cite).
- `medium-confidence-design-inputs`: 0 §B.1 cells (none load-bearing for GF-M).
- `historian-design-inputs`: 2 (H-2 + H-8 paired; engaged in scenario #1's Regime-A cycle design via implicit absorption).

## §8 References

**Candidate spec + back-fill notes (primary inputs):**

- [`specs/gf-m.md`](../specs/gf-m.md) — Phase-6 GF-M architecture spec; §0 ADR-citation index, §1 Overview, §2 Substrate composition, §3 Methodology shape, §4 Discipline binding, §5 Mandate fit, §6 Open carries.
- [`backfill-notes/gf-m.md`](../backfill-notes/gf-m.md) — Phase-7 back-fill audit; archive lineage cells for the Compound-Engineering 4-step loop cite obligation.
- [`substrate-requirements/gf-m.md`](../substrate-requirements/gf-m.md) — Phase-4 substrate-requirements summary (referenced by spec §2).

**Phase-8 dispatch artifacts:**

- [`decisions/auto-008-phase-8-dispatch-shape.md`](../decisions/auto-008-phase-8-dispatch-shape.md) — this brief's parent dispatch decision; §Falsifier discipline (R2 #1-#4 rubric, R6 #2 partitioned-mandate "pass cleanly" non-unified form for GF-M), §Phase-7 cite-obligation propagation table, §Per-candidate lean-eval brief rubric.
- [`scope-envelope-2026-05-28-phase-8.md`](../scope-envelope-2026-05-28-phase-8.md) — Phase-8 run scope envelope.

**Phase-7 inputs (cite-obligation source):**

- [`backfill-notes.md`](../backfill-notes.md) — Phase-7 aggregation matrix; §3.1 (high-confidence cite obligations), §3.2 (medium-confidence TBDs), §4.1 (historian load-bearing gaps).
- [`backfill-notes/audit-silent-absorption.md`](../backfill-notes/audit-silent-absorption.md) — Phase-7 silent-absorption auditor output.
- [`backfill-notes/audit-historian.md`](../backfill-notes/audit-historian.md) — Phase-7 historian auditor output.

**ADRs cited (substrate + discipline):**

- [ADR 0010](../../docs/adr/0010-p-01-sandbox-runtime.md), [ADR 0011](../../docs/adr/0011-p-02-cost-ceilings.md), [ADR 0012](../../docs/adr/0012-p-05-trajectory-capture.md), [ADR 0013](../../docs/adr/0013-p-06-watchdog-tiers.md), [ADR 0014](../../docs/adr/0014-p-07-telemetry-ingestor.md), [ADR 0015](../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md), [ADR 0016](../../docs/adr/0016-p-14-judge-router.md), [ADR 0023](../../docs/adr/0023-discipline-knowledge-promotion.md), [ADR 0040](../../docs/adr/0040-p-20-reversibility-primitive.md), [ADR 0041](../../docs/adr/0041-p-21-paraphrase-divergence.md).

**Archive sources (Phase-7 cite obligation):**

- [`archive/synthesis-v1-v2/13-round-2-synthesis.md`](../../archive/synthesis-v1-v2/13-round-2-synthesis.md) — Compound-Engineering 4-step loop v0.2 canonicalization (high-confidence mandatory cite per Phase-7 aggregation §3.1 finding #2).

**Cross-cutting v3 docs:**

- [`decisions-captured.md`](../decisions-captured.md) — DEC-1.a working hypothesis (GF-M is mandate-aligned greenfield; does NOT carry DEC-1.a unified-attempt load), DEC-2 mandate-fit-per-(architecture × work-unit-class).
- [`failure-modes-v3.md`](../failure-modes-v3.md) — F-mode catalog (F8, F25, F26, F34, F37, F40, F41, F46, F55 + CTR-D7, CTR-E1, CTR-E6 referenced).
- [`candidate-registry.md`](../candidate-registry.md) — GF-M candidate-registry entry.

---

## Exemplar pre-fanout self-check results

Lead-agent runs self-check items (a)-(g) on this exemplar brief BEFORE Wave 8.1 dispatches. Per [`auto-008 §Exemplar pre-fanout self-check gate`](../decisions/auto-008-phase-8-dispatch-shape.md#exemplar-pre-fanout-self-check-gate-load-bearing): failure on item (d) blocks fanout (item h dropped in Round 2); other items produce return-digest flags for lead-agent review but do NOT block.

- **(a) `wc -w`**: **4243 words. UNDER Light tier floor (5000-6500).** Return-digest flag noted; NOT a fanout blocker (item a is not the load-bearing block per auto-008 §Exemplar pre-fanout self-check gate). Lead-agent acknowledgement: the exemplar's design priority was **structural clarity** (demonstrating the §1-§8 sections + the YAML schema + the falsifier-discipline + the cite-obligation honoring pattern) over hitting tier floor. Subagents authoring their own briefs in Wave 8.1 MUST target their assigned tier (Light 5000-6500 / Heavy 5500-7200) per their candidate-tier YAML field, NOT the exemplar's 4243-word length. The exemplar's structure is the model, not its length. Per auto-008 §Over-budget subagent recovery (R5 #5 amendment): subagent under-budget below floor should be re-authored to expand on substantive coverage; the exemplar is exempted because its under-budget condition is deliberate.
- **(b) `ls` on cited paths**: **PASS.** All cited paths verified present: `specs/gf-m.md`, `backfill-notes/gf-m.md`, `backfill-notes.md`, `decisions/auto-008-phase-8-dispatch-shape.md`, `archive/synthesis-v1-v2/13-round-2-synthesis.md`, `docs/adr/0010-0017`, `docs/adr/0023`, `docs/adr/0040`, `docs/adr/0041`. 8 paths spot-checked at commit time.
- **(c) `grep -cE "^## §[1-8]"`**: **PASS** — exactly 8 §-headers (§1 through §8).
- **(d) `grep "falsifying-outcome:"` + value ≤80 words**: **PASS** — YAML field present at line 11 of YAML frontmatter; field value is **46 words** (well under ≤80-word limit). This is the load-bearing item; pass means fanout is unblocked.
- **(e) `grep -c "phase-7-cite-obligations:"`**: **PASS** — YAML field present.
- **(f) Binding-rule-table verbatim text-pull check**: **PASS with `n/a` qualifier.** This brief quotes phrases from `specs/gf-m.md §1`, `§3`, `§6` verbatim (e.g., "No `docs/solutions/` accumulation in Regime A"; "F25 design starvation is re-cast as a property of the regime, not a failure") but those are SHORT PHRASES, not binding rule tables. The brief does NOT cite a multi-row table from `specs/gf-m.md §0` (the ADR-citation index) verbatim; references to ADRs use individual ADR markdown links. Per auto-008 self-check item (f) `n/a` clause: no binding-rule-table verbatim text-pull is invoked.
- **(g) `grep -cE "##? §[1-8]"`**: 8 §-headers from §1 through §8 (same as item c). Self-check H2 (above this line) and Exemplar-self-check H2 (this section) are H2 headers that don't match `§[1-8]` pattern, so they are correctly excluded from the count.
- **(h) DROPPED in Round 2** per [`auto-008 §Per-candidate lean-eval brief rubric self-check`](../decisions/auto-008-phase-8-dispatch-shape.md#decision-round-2) R3 #2 amendment. Cite-obligation honoring is enforced by falsification-designer auditor + post-fanout aggregation.

**Exemplar pre-fanout gate verdict: PASS on load-bearing items (d).** Item (a) under-budget is a return-digest flag, not a blocker. Fanout to Wave 8.1 is unblocked.
