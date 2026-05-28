---
based-on-spec-commit: f18f6fb
based-on-backfill-commit: 5bb8bf8
based-on-date: 2026-05-28
candidate-tier: Heavy
candidate-mandate: brownfield
scenario-set-source: hybrid
mandate-scenario-split:
  greenfield: 0
  brownfield: 6
expected-evaluator-time-days: 1
falsifying-outcome: |
  Across 6 brownfield scenarios run against a public 1M+LOC long-history
  codebase, BF-L's P-13 maintenance loop fails to surface ≥80% of
  injected drift events (test-coverage decay, telemetry anomalies,
  churn-cadence shifts) WITHIN one reconciliation cycle, measured from
  `maintenance-trigger` events emitted into P-30 vs the seeded drift
  log at `solutions/audit/p-13-runs/<scenario-id>.json`. Equivalently:
  drift-detection MCC ≤0.55 on the seeded-drift labelled set.
phase-7-cite-obligations:
  high-confidence-mandatory:
    - 4-architecture-taxonomy-archive-cite
  medium-confidence-design-inputs:
    - audit-silent-absorption.md-§B.1-cells-touching-bf-l
  historian-design-inputs:
    - H-3-pulse-report-production-trace-to-spec-amendment
---

# Lean-eval brief — BF-L (Brownfield, legacy-ingestion-first)

Per [`auto-008` per-candidate rubric](../decisions/auto-008-phase-8-dispatch-shape.md#decision-round-2). Heavy-tier brief; Wave-8.1 per-candidate fanout subagent output. BF-L's distinctive lean-eval load is its **commodity-dispatch ADR-0036 framing** (per Phase-6-followup #1, distinct from U-A / D7-U-1's "registrar-framework" framing) and its **P-13 maintenance loop** as the closest substrate analog to the H-3 Pulse-report (production-trace-to-spec-amendment) historian gap.

## §1 Candidate + scenario set

**Candidate.** BF-L is the brownfield-mandate-only legacy-ingestion-first candidate (Heavy tier per [`auto-008` tier-table](../decisions/auto-008-phase-8-dispatch-shape.md#decision-round-2)). Per [`specs/bf-l.md §1`](../specs/bf-l.md#1-overview): BF-L's load-bearing claim is that **code-archaeology is the primary organizing principle** — the factory's first move on any new brownfield codebase is a dedicated **ingestion phase** that produces the **P-26 Codebase Model** (six views: structural / conventional / historical / runtime / invariant / debt) as the durable artifact, and every downstream choice (work-unit shape, gate definitions, regime classification, scenario library) is derived from that artifact. Methodology is intentionally thin: three loops over a single durable artifact — **Loop 1 (Ingestion)** deep slow once-plus-refresh, **Loop 2 (Work)** per-cycle methodology-shaped, **Loop 3 (Maintenance)** continuous low-cadence reconciliation per [ADR 0048 (P-13)](../../docs/adr/0048-p-13-maintenance-loop.md). BF-L's `candidate-mandate: brownfield` and `mandate-scenario-split: {greenfield: 0, brownfield: 6}` — BF-L is NOT a unified-attempt and does NOT carry the DEC-1.a load; the scenario set is single-bloc (brownfield-only) and the "pass cleanly" definition uses the non-unified form (≥80% scenarios pass + falsifying-outcome NOT triggered) per [`auto-008 §Falsifier discipline`](../decisions/auto-008-phase-8-dispatch-shape.md#falsifier-discipline-load-bearing).

**Phase-7 lineage shape (load-bearing for §3 framing).** Per [`backfill-notes/bf-l.md §1`](../backfill-notes/bf-l.md): BF-L's v2-architecture lineage is a **two-architecture pair** — **Architecture 2 (Compound Atelier) co-equal with Architecture 3 (Phase-Gated Foundry) + secondary Refinery (per-symbol stable-IDs)**. The Codebase Model thickening via P-24 attribution is direct Atelier-compounding; the Loop-1 dedicated ingestion + Loop-3 maintenance-as-CM + per-region P-19 classifier acting as RTM/gate-board is direct Foundry inheritance. Multi-lineage with Heavy-tier substrate surface (P-26 Codebase Model is "the most ambitious primitive in the catalog" per [primitives/index.md](../primitives/index.md)). The lean-eval pressure-tests against scaling, drift, and the methodology-degradation clause — the surfaces where multi-lineage assumptions could collide.

**Commodity-dispatch ADR-0036 framing (load-bearing per Phase-6-followup #1).** Per [`specs/bf-l.md §0`](../specs/bf-l.md#0-adr-citation-index) verbatim:

> *"0036 IS consumed (without per-variant binding) by P-13 maintenance-loop dispatch ([ADR 0048](../../docs/adr/0048-p-13-maintenance-loop.md)), so 0036 appears in §0 as a **commodity dispatch surface**, not as a framework requiring BF-L per-variant authorship."*

This framing is **materially distinct** from U-A / D7-U-1's "registrar-framework" framing per [`audit-silent-absorption.md §B.2`](../backfill-notes/audit-silent-absorption.md): U-A's registrar is event-driven (state transitions on external triggers); D7-U-1's is timer-driven (survival-window-open → window-expired). BF-L treats 0036 as a fire-and-forget event-emission API, NOT as a registrar holding state-machine semantics. This brief treats the commodity-dispatch framing as load-bearing: scenarios pressure-test whether the framing actually holds operationally (i.e., the maintenance loop can dispatch reconciliation without needing per-variant registrar policy), or whether the framing silently leans on registrar semantics that aren't declared.

**Scenario set source.** Hybrid: scenarios drawn from (a) the F-mode corpus with focus on **F20 (maintenance asymmetry, BF-L's deepest mitigation), F8 (stale knowledge, BF-L's deepest mitigation), F34 (cross-layer drift), F55 (behavioural drift), F57 (design-authority erosion), F43 (board-visibility gap), F54 (Codebase Model attack surface)** — i.e., the F-modes BF-L's three-loop discipline + per-region classifier + Codebase Model explicitly mitigates — and (b) BF-L's own scenario-derivation primitive at [`specs/bf-l.md §3.5`](../specs/bf-l.md#3-methodology-shape) ("Scenarios are inherited from the model, not authored out-of-tree — explicit challenge to D-2"). The two halves are not redundant: corpus scenarios provide adversarial F-mode pressure; candidate-derived scenarios surface what the Codebase Model's own profile predicts as productive vs paralytic work-unit shapes.

### Brownfield-mandate scenarios (6 total)

1. **P-26 integration discipline at 1M+LOC long-history codebase (corpus F8 + F34 + candidate-derived OQ-T1).** Evaluator runs Loop-1 ingestion against a public 1M+LOC codebase with ≥10-year history (Chromium, Linux kernel, or LLVM). Measures: join-API latency (`model.join(symbol, version, [views])`); snapshot-consistency under concurrent ingestion; Merkle-DAG incremental-versioning delta-drift across two ingestion-pass IDs separated by a 90-day commit window. Surfaces: scaling-against-9-18-engineer-month-estimate (per [Phase-3.5.5](../candidate-registry.md#phase-355-rule-on-load-bearing-rg-primitives-binding-user-approved-2026-05-25)). Pass: integration discipline completes without falling back to "six co-located stores" pattern (BF-L collapse-to-BF-S signal) AND `model.join` latency ≤2s p95 for symbol-level queries AND snapshot-consistency holds across 5 concurrent ingestion passes.

2. **P-13 maintenance loop drift detection — seeded drift corpus (corpus F8 + F20 + F34, candidate-derived). [LOAD-BEARING §3 falsifier scenario.]** Evaluator constructs a seeded-drift labelled set of ≥20 drift events across the three classes BF-L names (per [`specs/bf-l.md §2.2`](../specs/bf-l.md#22-the-maintenance-loop-orphan)): (1) test-coverage decay (runtime view of P-26); (2) runtime telemetry anomalies via P-07 — error-rate spikes, latency shifts; (3) churn-cadence shift (historical view, >2σ from rolling baseline). Runs P-13's per-codebase nightly inspector + weekly full reconciliation against the seeded set. Measures: detection rate of `maintenance-trigger` event emission into P-30; MCC against labelled ground-truth; debt-weighted prioritisation correctness (Caremark/RSI-tagged surfaces first). Pass: ≥80% drift events surface ≥1 `maintenance-trigger` within one reconciliation cycle AND MCC > 0.55 AND Caremark/RSI-tagged regions surface in the prioritisation queue's top decile. **This is BF-L's load-bearing falsifier scenario** (see §3).

3. **Commodity-dispatch ADR-0036 framing pressure-test (Phase-6-followup #1, candidate-derived).** Evaluator runs 5 cycles where P-13 emits `kind=maintenance-trigger` events into P-30 substrate AND a sixth cycle where the substrate would naturally call for registrar-style state-machine semantics (e.g., a multi-stage reconciliation where the dispatcher must remember "which region was already touched this maintenance window"). Tests whether BF-L's commodity-dispatch framing holds (events fire-and-forget; handlers re-derive state from P-26 snapshot) or whether BF-L silently leans on registrar semantics (events carry state that handlers depend on, requiring per-variant registrar policy). Surfaces: Phase-6-followup #1 framing-drift risk; cross-spec interpretation drift with U-A / D7-U-1. Pass: all 5 baseline cycles complete without a registrar-state-machine pattern emerging in the reconciliation handler trajectories AND the sixth multi-stage cycle either (a) completes via P-26-snapshot-redirivation OR (b) explicitly surfaces the registrar-state-machine gap as a methodology-layer escalation (NOT a silent absorption).

4. **Per-region regime classification under degradation regime (corpus F46 + F55 + F57; candidate-derived OQ-T4 + auto-003 methodology-degradation clause).** Evaluator constructs scenarios where conventional-view OR invariant-view falls back to (b) `accept-as-RG` per the [auto-003 methodology-degradation clause](../decisions/auto-003-bfl-rg-view-choice.md#methodology-degradation-clause-new-per-reviewer-2-a2). Runs 5 per-region classification cycles where the feature vector contains `degraded-convention` and/or `degraded-invariant` regime variants. Tests whether [ADR 0049 (BF-L P-19 per-region)](../../docs/adr/0049-p-19-variant-bf-l-per-region.md)'s Patrol drift-monitor distinguishes `degraded-*` regimes from regular F57 drift. Surfaces: F46 (single-model review blindspot, cross-family judging mitigation), F55 (behavioural drift under degradation), F43 (board-visibility gap on per-region governance fragmentation). Pass: Patrol distinguishes `degraded-convention` / `degraded-invariant` from F57 in ≥4 of 5 cycles AND the strictest-region-wins cycle rollup defaults to `augmentation-required` (not `automation-eligible`) when any touched region carries a degraded marker.

5. **F54 Codebase Model attack-surface pressure-test (corpus F54; candidate-derived OQ-T6).** Evaluator constructs a 3-step adversarial scenario where (i) an adversary submits a benign-looking PR that subtly poisons the historical view (e.g., adds attribution noise that biases churn-cadence calculations), (ii) the next ingestion-pass refreshes the model with the poisoned attribution, (iii) the per-region classifier's feature vector is now subtly biased toward classifying the adversary's preferred regions as `automation-eligible`. Surfaces: F54 (Codebase Model attack surface — per [BF-L track §7 OQ-T6](../tracks/brownfield-legacy-ingestion-first.md)), F12 (lethal trifecta — model-poisoning bypasses single guards). Pass: ≥1 of the substrate guards (P-08 holdout, P-24 attribution-cosign integrity check, OPA hard-floor Caremark/RSI tagging, Patrol-tier cross-pass drift detection) catches the poisoning within 3 cycles AND the trajectory's F54 signal is logged to `solutions/audit/f54-runs/<scenario-id>.json` for re-derivation.

6. **H-3 Pulse-report engagement — production-trace-to-spec-amendment loop closer (historian H-3 + candidate-derived).** Evaluator simulates a production-trace event stream (P-07 telemetry: error-rate spike on a specific symbol-region) and verifies whether BF-L's P-13 maintenance loop closes the loop in the **Pulse-report style** named by [aggregation §4.1 historian H-3](../backfill-notes/audit-historian.md): production trace → maintenance-trigger → reconciliation cycle → P-26 view refresh → spec-amendment-equivalent (in BF-L's vocabulary: codebase-evolution-proposal work-unit-class per [`specs/bf-l.md §3.2`](../specs/bf-l.md#3-methodology-shape) step 1). Tests whether BF-L's "thin methodology over Codebase Model" actually produces the Pulse-report-equivalent downstream surface, or whether P-13 stops at "drift detected" without closing the loop into spec-amendment-equivalent work. Surfaces: H-3 (Pulse report load-bearing gap — BF-L is its closest substrate analog per [`audit-historian.md`](../backfill-notes/audit-historian.md)), F20 (maintenance asymmetry — does maintenance actually generate work that returns to the codebase?). Pass: ≥1 simulated production trace produces a maintenance-trigger that escalates to a codebase-evolution-proposal work-unit AND the work-unit's per-region classification + attribution trail are recoverable from substrate state alone.

The 6 scenarios cover BF-L's 4 mandate-fit work-unit-classes (`initial-spec: brownfield` via #1; `refactor: brownfield` via #3 + #4; `post-mvp-evolution: brownfield` via #2 + #6; `regression-fix: brownfield` via #5) and pressure-test all of BF-L's load-bearing claims (Codebase Model integration; three-loop discipline; per-region classification; commodity-dispatch framing; Pulse-report-equivalent closure).

**Why these 6 scenarios.** BF-L's spec carries 8 open carries at [`specs/bf-l.md §6`](../specs/bf-l.md#6-open-carries): P-26 integration at 1M+LOC; conventional-view RG (Wave-4.5b gated); invariant-view RG (Wave-4.5b gated); maintenance-loop cadence calibration; per-region classifier drift under degradation; F54 attack surface; ingestion-as-substrate vs ingestion-as-methodology (OQ-T1 — Phase-7 carry only); F35 federation-at-model-level. The lean-eval engages 5 of the 6 Phase-8-flagged carries directly (#1 hits 1M+LOC scaling; #2 hits cadence calibration; #4 hits per-region degradation drift; #5 hits F54 attack surface; #6 + #2 hit maintenance-loop empirical anchor). The conventional/invariant-view RG carries are NOT directly engaged because Wave-4.5b scaling is owed at Phase 5/6 — the lean-eval pressure-tests the methodology assuming Wave-4.5b passed; the degradation-regime scenario (#4) covers the methodology-degradation clause as a defensive measure. F35 federation is a documentation-layer carry not reducible to a 1-day evaluator scenario.

Scenario selection prioritized (a) BF-L's load-bearing wager (**P-13 maintenance loop as the F20+F8 mitigation surface** → scenario #2 is the §3 falsifier test), (b) the multi-lineage Atelier+Foundry stress test (scenarios #1 + #6 stress Atelier-compounding via attribution; scenarios #3 + #4 stress Foundry-CM-as-spine via per-region classification), and (c) the H-3 Pulse-report historian engagement (scenario #6 is the explicit Pulse-report-style engagement per the dispatch brief). The 6-scenario count meets the auto-008 floor; BF-L's commodity-dispatch ADR-0036 framing requires scenario #3 as a dedicated pressure-test.

## §2 Success criteria

A BF-L lean-eval result "passes cleanly" (per [`auto-008 §Falsifier discipline` non-unified form](../decisions/auto-008-phase-8-dispatch-shape.md#falsifier-discipline-load-bearing)) iff:

- **(a) Quantitative gate:** ≥80% of the 6 scenarios pass the §1 success criteria (i.e., ≥5 of 6 scenarios pass).
- **(b) Falsifying-outcome gate:** the §3 falsifying-outcome is NOT triggered on any scenario.

**Per-scenario success criteria (verbatim distillation of §1):**

1. **P-26 integration at 1M+LOC.** `model.join(symbol, version, [views])` latency ≤2s p95 across ≥1000 sampled queries; snapshot-consistency holds across 5 concurrent ingestion passes; Merkle-DAG delta-versioning shows no false-positive structural delta across the 90-day commit window for unchanged symbols; integration discipline does NOT fall back to six co-located stores. Logged to `solutions/audit/p-26-scale/<scenario-id>.json`.

2. **P-13 drift detection.** Detection rate ≥80% across ≥20 seeded drift events (≥16 of 20 detected via `maintenance-trigger` events into P-30) within one reconciliation cycle; MCC > 0.55 against labelled ground-truth; Caremark/RSI-tagged regions surface in the prioritisation queue's top decile in ≥4 of 5 cycles. Logged to `solutions/audit/p-13-runs/<scenario-id>.json`.

3. **Commodity-dispatch ADR-0036 framing.** 5 baseline reconciliation cycles complete without `maintenance-trigger` events carrying state that downstream handlers depend on (verifiable from the event-payload schema in P-30 + the reconciliation handler trajectories in P-05); the multi-stage sixth cycle either completes via P-26-snapshot-rederivation OR explicitly surfaces a registrar-state-machine escalation in the trajectory log. NO silent absorption of registrar semantics. Logged to `solutions/audit/p-30-dispatch/<scenario-id>.json`.

4. **Per-region degradation regime.** [ADR 0049](../../docs/adr/0049-p-19-variant-bf-l-per-region.md)'s Patrol drift-monitor distinguishes `degraded-convention` / `degraded-invariant` from F57 in ≥4 of 5 cycles; strictest-region-wins cycle rollup defaults to `augmentation-required` when any touched region carries a degraded marker (verified across all 5 cycles). Logged to `solutions/audit/p-19-degraded/<scenario-id>.json`.

5. **F54 attack surface.** ≥1 substrate guard (P-08 holdout / P-24 attribution-cosign integrity / OPA hard-floor / Patrol-tier cross-pass drift) catches the poisoning within 3 cycles; the F54 signal is logged for re-derivation from substrate state alone (no operator-memory dependency).

6. **H-3 Pulse-report closure.** ≥1 simulated production-trace event produces a `maintenance-trigger` that escalates (within ≤2 reconciliation cycles) to a codebase-evolution-proposal work-unit; the work-unit's per-region classification + attribution trail are recoverable from substrate state (P-26 + P-24 + P-05 trajectory + P-08 partition state) alone.

**Note on success-criteria vs falsifying-outcome distinction (per [`auto-008 §Falsifier discipline`](../decisions/auto-008-phase-8-dispatch-shape.md#falsifier-discipline-load-bearing)):** failing §2 success criteria can be implementation noise (a Tree-sitter parser misconfigured for the target language; a P-07 telemetry tap miscalibrated; an OPA Rego rule with a typo). Triggering the §3 falsifying-outcome is the methodology's load-bearing claim being wrong — the P-13 maintenance loop is BF-L's structural answer to F20 + F8 + F34; if it doesn't actually surface drift at the seeded-corpus floor, the entire "three loops over a single durable artifact" load-bearing claim loses its empirical justification.

## §3 Falsifying outcome

**Falsifying-outcome verbatim (≤80 words from YAML, repeated here for §3-vs-YAML consistency per [auto-008 falsification-designer rubric item (iv) MANDATORY](../decisions/auto-008-phase-8-dispatch-shape.md#r2-1-falsification-designer-concreteness-rubric-3-item-mechanical)):**

> Across 6 brownfield scenarios run against a public 1M+LOC long-history codebase, BF-L's P-13 maintenance loop fails to surface ≥80% of injected drift events (test-coverage decay, telemetry anomalies, churn-cadence shifts) WITHIN one reconciliation cycle, measured from `maintenance-trigger` events emitted into P-30 vs the seeded drift log at `solutions/audit/p-13-runs/<scenario-id>.json`. Equivalently: drift-detection MCC ≤0.55 on the seeded-drift labelled set.

**Rationale.** BF-L's central wager (per [`specs/bf-l.md §1` load-bearing claim](../specs/bf-l.md#1-overview) + [`specs/bf-l.md §3.3`](../specs/bf-l.md#3-methodology-shape) + [ADR 0048](../../docs/adr/0048-p-13-maintenance-loop.md)) is that **the P-13 maintenance loop is the structural defense against F20 (maintenance-vs-greenfield asymmetry, brownfield-critical) + F34 (cross-layer drift) + F55 (behavioural drift) + F57 (design-authority erosion)** — the four F-modes that distinguish brownfield from greenfield in the corpus. Per [`backfill-notes/bf-l.md §10.2`](../backfill-notes/bf-l.md): BF-L claims F8 + F20 as its **deepest-verified mitigations**. If the lean-eval shows P-13 has its own detection-rate ceiling at the same ≤80% threshold (equivalently MCC ≤0.55) on a seeded-drift corpus, the candidate's load-bearing wager is empirically wrong — the maintenance loop does NOT improve on a naïve threshold-monitor baseline on the same task, and the entire **three-loops-over-a-single-durable-artifact** claim (which depends on Loop-3 as the F20+F8 closer; see [`specs/bf-l.md §3.3`](../specs/bf-l.md#3-methodology-shape)) loses its empirical justification.

**Why this falsifier and not another.** Three alternatives considered:

- "If P-26 Codebase Model integration fails at 1M+LOC" — this is **scaling-failure-of-implementation**, not falsification of the load-bearing methodology claim. Scaling is OQ-6's open carry (a soft-RG-on-scale, not the central wager). The 9-18 engineer-month estimate is an effort projection, not a load-bearing methodology claim.
- "If per-region regime classification fragments governance (F43 board-visibility gap)" — this is a separate empirical question (governance fragmentation efficacy) but not the candidate's *central* wager. F43 mitigation is a property BF-L shares with multiple other candidates that bind ADR 0024.
- "If the Codebase Model is poisonable (F54)" — captured in scenario #5 but not the central wager. F54 attack-surface is a security property; the central methodology claim is about maintenance-loop closure of F20+F8, not about adversarial robustness.

The P-13 maintenance loop's F20+F8 defense is BF-L's *distinctive* load-bearing wager — the claim that distinguishes BF-L from BF-S (no maintenance loop) and BF-M (no Codebase-Model-anchored maintenance). The falsifier targets exactly this distinction.

**Why a 1M+LOC long-history codebase as the substrate target.** The falsifier names "a public 1M+LOC long-history codebase" deliberately. BF-L's spec §6 carries P-26 integration discipline at 1M+LOC as an explicit soft-RG-on-scale per [Phase-3.5.5](../candidate-registry.md#phase-355-rule-on-load-bearing-rg-primitives-binding-user-approved-2026-05-25); the maintenance loop's drift-detection efficacy at this scale is empirically unmeasured. Running the falsifier against a toy codebase would let BF-L pass trivially (any drift event in a 5K-LOC repository is detectable by inspection); running against the realistic scale where BF-L's load-bearing claim must hold is the test. The seeded-drift corpus (≥20 events across the three drift classes BF-L names) provides the labelled ground-truth that distinguishes drift-detection from generic codebase noise — without seeding, "did P-13 detect drift?" collapses to "did the codebase have drift?" which is not a methodology-claim test.

**Independence from scenario #2 success-criteria.** Scenario #2's success-criterion is ≥80% detection rate AND MCC > 0.55 AND Caremark/RSI prioritisation in top decile (per §2). The §3 falsifier is the conjunction of `<80% detection rate OR MCC ≤0.55` — i.e., scenario #2 can pass §2 while also triggering §3 only if the Caremark/RSI-prioritisation condition compensates for marginal detection-rate or MCC. The brief deliberately keeps §3 narrower than §2's negation: §3 captures the methodology's load-bearing claim (drift-detection efficacy on the seeded corpus); §2 captures the methodology's operational discipline (prioritisation correctness as a secondary check). Per [`auto-008 §Falsifier discipline`](../decisions/auto-008-phase-8-dispatch-shape.md#falsifier-discipline-load-bearing): "failing criteria might be implementation noise; the falsifier is the methodology's load-bearing claim being wrong" — this brief honors that distinction.

**Machine-checkability.** Per [auto-008 falsification-designer rubric 3-item check + mandatory item (iv)](../decisions/auto-008-phase-8-dispatch-shape.md#r2-1-falsification-designer-concreteness-rubric-3-item-mechanical):

- **(i) Metric:** `drift-detection-rate` (countable; % of seeded drift events that emit `maintenance-trigger` within one reconciliation cycle) AND `MCC` (Matthews Correlation Coefficient, numeric) — both passable.
- **(ii) Artifact state:** `solutions/audit/p-13-runs/<scenario-id>.json` — specific directory, specific filename pattern; the file contains the seeded-drift labelled set + the `maintenance-trigger` events emitted into P-30, both recoverable from substrate (P-30 event log + P-05 trajectory) — passable.
- **(iii) Threshold:** `<80%` detection rate OR `≤0.55` MCC — both numeric single-direction comparisons — passable.
- **(iv) §3-vs-YAML consistency (MANDATORY):** YAML field and this §3 statement name the SAME metric (drift-detection rate + MCC), SAME artifact location (`solutions/audit/p-13-runs/`), SAME threshold (<80% / ≤0.55). PASS.

The falsifier passes all 4 rubric items (pass on (iv) mandatory; pass on ≥2 of (i)-(iii)).

## §4 Failure modes the test surfaces

The 6 scenarios are designed to surface the following failure modes — for each, the specific F-mode(s) the scenario pressure-tests, citing BF-L's spec §4 (failure modes) or §3 (methodology shape) verbatim where applicable:

- **Scenario #1 (P-26 1M+LOC scaling)** surfaces:
  - **F8 (stale knowledge)** — at 1M+LOC the Codebase Model's six views each face their own freshness pressure; the integration discipline's snapshot-consistency under concurrent ingestion is the F8 mitigation surface. Per [`backfill-notes/bf-l.md §10.2`](../backfill-notes/bf-l.md): *"BF-L's deepest F8 mitigation: Loop-3 P-13 maintenance loop per ADR 0048 + §3.3."*
  - **F34 (cross-layer drift)** — six views drifting against one another at scale.
- **Scenario #2 (P-13 drift detection — load-bearing falsifier)** surfaces:
  - **F20 (maintenance asymmetry)** — BF-L's load-bearing wager defense. Per [`backfill-notes/bf-l.md §10.2`](../backfill-notes/bf-l.md): *"BF-L's deepest F20 mitigation: Loop-3 P-13 maintenance loop IS the structural answer per ADR 0048 + §2.2."*
  - **F8 (stale knowledge)** — drift signals are the operational definition of staleness.
  - **F34 (cross-layer drift)** — telemetry-vs-codebase divergence.
- **Scenario #3 (commodity-dispatch ADR-0036 framing)** surfaces:
  - **Phase-6-followup #1 framing-drift risk** — the BF-L vs U-A vs D7-U-1 ADR-0036 interpretation drift per [`audit-silent-absorption.md §B.2`](../backfill-notes/audit-silent-absorption.md). The scenario tests whether BF-L's "commodity dispatch" framing is operationally distinct from registrar semantics, or whether it silently absorbs registrar semantics.
  - **F57 (design-authority erosion)** — framing drift across specs is design-authority erosion at the architecture-decision layer.
- **Scenario #4 (per-region degradation regime)** surfaces:
  - **F46 (single-model review blindspot)** — cross-family judging at augmentation-required regime is the explicit mitigation; the scenario verifies efficacy under degradation.
  - **F55 (behavioural drift)** — degraded-marker regime variants are the substrate's honesty mechanism; the scenario verifies the Patrol drift-monitor distinguishes them.
  - **F57 (design-authority erosion)** — per-region governance fragmentation is the F43 + F57 surface.
  - **F43 (board-visibility gap)** — engaged by [`specs/bf-l.md §6` OQ-T4](../specs/bf-l.md#6-open-carries).
- **Scenario #5 (F54 attack surface)** surfaces:
  - **F54 (Codebase Model attack surface)** — per [BF-L track §7 OQ-T6](../tracks/brownfield-legacy-ingestion-first.md): *"an adversary who can poison the Codebase Model can drift the factory's objectives across cycles without tripping any single guard."*
  - **F12 (lethal trifecta)** — model-poisoning bypasses single guards; substrate-level defense in depth.
  - **F14 (attribution collapse)** — P-24 cosign integrity is the load-bearing F14 mitigation per [`backfill-notes/bf-l.md §10.2`](../backfill-notes/bf-l.md).
- **Scenario #6 (H-3 Pulse-report closure)** surfaces:
  - **H-3 (Pulse report load-bearing gap — production-trace-to-spec-amendment)** — per [`audit-historian.md` H-3](../backfill-notes/audit-historian.md): BF-L is the closest substrate analog. The scenario tests whether P-13 + P-26 + codebase-evolution-proposal work-unit-class actually closes the Pulse-report-equivalent loop.
  - **F20 (maintenance asymmetry)** — maintenance must produce work that returns to the codebase, not just emit detection signals.

The cross-cutting failure-mode coverage (10 distinct F-modes + 1 historian gap + 1 Phase-6-followup) is the lean-eval's load. **No scenario engages a failure mode F-mode is not enumerated in BF-L's spec §4 or §10.2 backfill-notes coverage** — the lean-eval does NOT smuggle in failure modes BF-L did not commit to defending.

**F-mode coverage matrix.**

| F-mode / surface | Description (≤15 words) | Scenario(s) | BF-L spec § / backfill § |
|---|---|---|---|
| F8 | Stale knowledge — Codebase Model freshness | #1, #2 | spec §3.3, backfill §10.2 (deepest-verified) |
| F12 | Lethal trifecta — model-poisoning bypasses single guards | #5 | spec §4 trifecta-closure |
| F14 | Attribution collapse — P-24 cosign integrity | #5 | spec §3.2 step 7, backfill §10.2 |
| F20 | Maintenance asymmetry — brownfield-critical | #2, #6 | spec §2.2, §3.3, backfill §10.2 (deepest-verified) |
| F34 | Cross-layer drift — substrate-vs-codebase | #1, #2 | spec §2.2, §3.3 |
| F43 | Board-visibility gap — per-region governance | #4 | spec §6 OQ-T4 |
| F46 | Single-model review blindspot — cross-family P-14 | #4 | spec §4 bias-guard |
| F54 | Codebase Model attack surface | #5 | spec §6 OQ-T6 |
| F55 | Behavioural drift — degraded-marker variants | #4 | spec §2.2, §3.3 |
| F57 | Design-authority erosion — per-region drift | #3, #4 | spec §2.2, §3.3 |
| H-3 | Pulse report (production-trace-to-spec-amendment) | #6 | backfill historian §4.1 (load-bearing gap) |
| ADR-0036 | Commodity-dispatch framing (Phase-6-followup #1) | #3 | spec §0, backfill §10.3 |

12 cells; each maps to ≥1 scenario; each cell's spec §-anchor or backfill §-anchor is auditable. **Coverage is intentional, not coincidental:** the scenarios were designed FROM the F-mode + historian-gap + framework-framing-drift list, not the reverse.

## §5 Evaluator time + protocol

**Expected evaluator time: 1 day** (per [v1.2 plan § Phase 8](../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md#phase-8--lean-eval-design-one-brief-per-candidate-first-pressure-test-surface-revised-in-v12) ~1-day-per-candidate bound). Breakdown:

- **Setup (~2 hours).** Evaluator initializes the substrate stack per [`specs/bf-l.md §2`](../specs/bf-l.md#2-substrate-composition): P-01 sandbox, P-02 cost ceilings configured at the BF-L-recommended per-loop budget (ingestion ceiling > per-cycle ceiling > maintenance ceiling per [`specs/bf-l.md §3.1`](../specs/bf-l.md#3-methodology-shape) + D-5 acceptance), P-05 trajectory capture, P-06 watchdog Patrol tier, P-07 telemetry ingestor (with seeded telemetry corpus for scenarios #2 and #6), P-08 substrate-typed holdout (OPA-mediated; partitions over P-26-derived scenarios), P-14 judge router, P-22 polyglot codebase index, P-23 dependency-impact graph, P-24 attribution store, P-26 Codebase Model (six views; Wave-4.5 smoke-test-passed assumption), P-27 archaeological-brief tooling, P-19 framework + ADR 0049 BF-L per-region variant (Drools/OPA Rego decision-table engine + LLM-judge fallback + OPA hard-floor with Caremark/RSI tags), P-30 event registrar (consumed verbatim per the commodity-dispatch framing), P-13 maintenance loop with seeded drift corpus.
- **Scenario execution (~5 hours).** Run scenarios #1-#6 in order. Each scenario produces (a) a `solutions/audit/p-13-runs/<scenario-id>.json` for maintenance-trigger events (scenarios #2 + #6), (b) a `solutions/audit/p-26-scale/<scenario-id>.json` for Codebase Model integration metrics (scenario #1), (c) a `solutions/audit/p-30-dispatch/<scenario-id>.json` for ADR-0036 framing audit (scenario #3), (d) a `solutions/audit/p-19-degraded/<scenario-id>.json` for per-region degradation cycles (scenario #4), (e) a `solutions/audit/f54-runs/<scenario-id>.json` for F54 attack-surface logs (scenario #5), (f) per-scenario `solutions/lean-eval/<scenario-id>/` directories for scenario-specific artifacts (work-unit declarations, region resolutions, classification decisions, attribution trails). Evaluator does NOT intervene mid-scenario; substrate-and-methodology-only.
- **Verdict pass (~1 hour).** Evaluator computes (i) per-scenario pass/fail against §2 success criteria; (ii) the §3 falsifying-outcome check (detection-rate + MCC across the ≥20 seeded drift events in scenario #2); (iii) the "pass cleanly" verdict per [`auto-008 §Falsifier discipline` non-unified form](../decisions/auto-008-phase-8-dispatch-shape.md#falsifier-discipline-load-bearing). Verdicts written to `solutions/lean-eval/verdict-bf-l.md`.

**Protocol invariants** (per [`auto-008 §Falsifier discipline` escape-hatch enumeration](../decisions/auto-008-phase-8-dispatch-shape.md#r2-2--3-dec-1a-falsifying-pattern-canonical-terms-committed-in-this-brief)):

- **No out-of-mandate scope claim.** BF-L is brownfield-mandate-only; all 6 scenarios are brownfield-shaped by construction. BF-L's mvp `n/a` work-unit-class is NOT a scenario in this lean-eval (per [`specs/bf-l.md §5`](../specs/bf-l.md#5-mandate-fit)); out-of-mandate scope claim does not apply.
- **No scenario-skip mid-run.** All 6 scenarios are executed; partial completion (e.g., scenario #1 timing out at 1M+LOC) is recorded as a failure, NOT a skip.
- **No criterion-substitution.** §2 success criteria are committed in this brief; evaluator does NOT re-interpret them mid-run.

**Substrate ground-truth invariants.** The evaluator records the substrate state at end-of-scenario (P-26 snapshot version tokens, P-30 event log, P-24 attribution trail, P-05 trajectory, P-08 partition state, P-19 classification decisions) so the verdict is reconstructable from substrate state alone. The §3 falsifier verdict on scenario #2 is reconstructable from `solutions/audit/p-13-runs/` — the seeded-drift labelled set is committed before the scenario starts; the `maintenance-trigger` events into P-30 are appended during; the post-run computation of detection-rate + MCC is purely substrate-state-derived. The evaluator's role in computing the verdict is mechanical — `detection-rate = |events ∩ seeded-set| / |seeded-set|`; MCC computed against the labelled set's positive/negative cells.

**Cost-ceiling parameterisation per BF-L D-5 acceptance.** Per [`specs/bf-l.md §3.1`](../specs/bf-l.md#3-methodology-shape): *"the ceiling itself is per-phase, not flat"*. Evaluator sets three ceilings: (a) **ingestion ceiling** at ~10× per-cycle (scenario #1 may consume the full ingestion ceiling on the 1M+LOC corpus); (b) **per-cycle ceiling** at the BF-L-recommended baseline (scenarios #3-#6 each consume ≤1 per-cycle ceiling); (c) **maintenance ceiling** at ~0.5× per-cycle (scenario #2 runs at maintenance-ceiling per the per-codebase nightly inspector cadence). CTR-E1 cost-variance is addressed by per-loop ceilings per [BF-L spec §4 cost-ceiling binding](../specs/bf-l.md#4-discipline-binding); ceiling-hit recovery via P-02-mediated truncation surfaces in the trajectory as an explicit event.

**Per-region Caremark/RSI tagging precondition.** Scenarios #2, #4, #5 require the target codebase carry a non-empty Caremark/RSI-tag set (per [`specs/bf-l.md §2.3`](../specs/bf-l.md#23-the-per-region-regime-classifier-framework--per-variant-pair) OPA hard-floor: *"caremark_rsi_tag = true → never automation-eligible"*). Setup phase includes operator-annotation of ≥5% of the codebase's symbol-set with Caremark/RSI tags (drawn from real-world precedent — finance/healthcare regions; security-sensitive APIs; cryptographic primitives). Without this precondition, scenario #4's strictest-region-wins rollup and scenario #5's substrate-guard-catches-poisoning verdicts are not testable.

**Hour-by-hour evaluator-time breakdown** (8-hour evaluator-day):

| Hour | Phase | Activity | Artifacts produced |
|---|---|---|---|
| 0:00-0:30 | Setup | Initialize substrate stack per `specs/bf-l.md §2`; configure per-loop D-5 ceilings | `solutions/setup/substrate-init.log` |
| 0:30-2:00 | Setup | Configure P-26 ingestion against target 1M+LOC codebase + seeded drift corpus + Caremark/RSI tag set | `solutions/setup/p-26-init.json`, `solutions/setup/p-13-seeded-drift.json` |
| 2:00-3:00 | Scenario #1 | P-26 integration at 1M+LOC | `solutions/audit/p-26-scale/sc1.json` |
| 3:00-4:30 | Scenario #2 | P-13 drift detection (load-bearing falsifier) — 20+ seeded drift events | `solutions/audit/p-13-runs/sc2-drift{1..20}.json` |
| 4:30-5:00 | Scenario #3 | Commodity-dispatch ADR-0036 framing pressure-test — 5+1 cycles | `solutions/audit/p-30-dispatch/sc3.json` |
| 5:00-5:45 | Scenario #4 | Per-region degradation regime — 5 cycles | `solutions/audit/p-19-degraded/sc4.json` |
| 5:45-6:30 | Scenario #5 | F54 attack surface — 3-step adversarial scenario | `solutions/audit/f54-runs/sc5.json` |
| 6:30-7:00 | Scenario #6 | H-3 Pulse-report closure — simulated production trace → maintenance-trigger → codebase-evolution-proposal | `solutions/lean-eval/sc6/pulse-closure.json` |
| 7:00-7:30 | Verdict | Per-scenario pass/fail + §3 falsifier check + pass-cleanly verdict | `solutions/lean-eval/verdict-bf-l.md` |
| 7:30-8:00 | Reporting | Write verdict-bf-l.md with detection-rate, MCC, per-scenario verdicts, escape-hatch audit | (same file) |

Total 8 hours; scenarios consume ~5 hours; setup + verdict ~3 hours. If any scenario over-runs (scenario #1 1M+LOC is the highest over-run risk), evaluator records the over-run in the verdict file but does NOT skip subsequent scenarios — partial completion = scenario fails per §5 protocol invariants.

## §6 Open critique references

BF-L's [`specs/bf-l.md §6 Open carries`](../specs/bf-l.md#6-open-carries) lists 8 open critique findings; the lean-eval engages 5 of them directly:

- **P-26 integration discipline at 1M+LOC / 10+ year history** → engaged by scenario #1. Pressure-test against a public 1M+LOC long-history codebase.
- **P-26 conventional-view RG carry (Wave-4.5b verdict gates)** → NOT directly engaged. The methodology-degradation clause (scenario #4) is the defensive measure; the conventional-view scaling sweep is Phase-5/6 Wave-4.5b scope.
- **P-26 invariant-view RG carry (Wave-4.5b verdict gates)** → NOT directly engaged. Same defensive measure as conventional-view; T4 Daikon-style runtime deferred per research-notes.
- **Maintenance-loop cadence calibration (OQ-T3)** → engaged by scenario #2. The drift-detection-rate measurement against seeded corpus IS the empirical anchor for cadence calibration (per [`specs/bf-l.md §6`](../specs/bf-l.md#6-open-carries) + [BF-L track §7 OQ-3](../tracks/brownfield-legacy-ingestion-first.md)).
- **Per-region regime classifier drift under degradation regime (OQ-T4)** → engaged by scenario #4.
- **F54 Codebase Model attack-surface pressure-test (OQ-T6)** → engaged by scenario #5.
- **Ingestion-as-substrate vs ingestion-as-methodology (OQ-T1, Phase-7 carry)** → NOT engaged. Documentation-layer question about candidate-positioning, not a 1-day evaluator scenario.
- **F35 federation-at-the-model-level (OQ-T7)** → NOT engaged. Multi-factory governance question; out of scope for single-factory lean-eval.

**H-3 Pulse-report engagement (per dispatch brief flag).** Scenario #6 is the explicit Pulse-report-style downstream-surface engagement. Per [`audit-historian.md` H-3](../backfill-notes/audit-historian.md): *"Closes maintenance loop on production data → spec amendment (related to F20). BF-L P-13 maintenance loop is closest substrate analog but BF-L spec doesn't name pulse-report or production observability."* The lean-eval engages H-3 by simulating a production-trace event stream and verifying whether P-13 closes the loop into a codebase-evolution-proposal work-unit (BF-L's spec-amendment-equivalent per the D-1 challenge). **Result of scenario #6 informs whether BF-L's P-13 substrate analog actually fulfills H-3's load-bearing role, or whether BF-L needs an explicit Pulse-report primitive at Phase-8-followup.**

**Per-open-carry escalation discipline.** If a scenario fails AND its failure is rooted in an open carry from `specs/bf-l.md §6`, the failure escalates that open carry from "Phase-8 carry" status to "Phase-8-followup blocker" status per the [`auto-008 §Phase-8-followup deferral binding mechanism`](../decisions/auto-008-phase-8-dispatch-shape.md#phase-8-followup-deferral-binding-mechanism-load-bearing). Specific escalation map: scenario #1 fail → 1M+LOC integration carry escalates; scenario #2 fail → maintenance-loop cadence calibration carry escalates AND triggers the §3 falsifier verdict (load-bearing); scenario #3 fail → Phase-6-followup #1 ADR-0036 framing-drift escalates; scenario #4 fail → per-region degradation OQ-T4 escalates AND triggers the methodology-degradation clause re-assessment; scenario #5 fail → F54 OQ-T6 escalates; scenario #6 fail → H-3 Pulse-report substrate-analog-insufficiency surfaces as a NEW Phase-8-followup carry (BF-L spec gains a new §6 open carry on "explicit Pulse-report primitive"). Note that the Phase-8-followup threshold per [`auto-008` R1 #5](../decisions/auto-008-phase-8-dispatch-shape.md#phase-8-followup-deferral-binding-mechanism-load-bearing) is restricted to unified-attempt candidates — BF-L is NOT a unified-attempt, so a failed BF-L lean-eval is a quality defect that lead agent re-authors at run-close as a non-blocker, NOT a Phase-8-followup deferral trigger.

## §7 Phase-7 cite obligations honored

Per the [`auto-008` per-candidate cite-obligation mapping table for BF-L](../decisions/auto-008-phase-8-dispatch-shape.md#high-confidence-mandatory-cite-obligations-3-cells--n-candidates):

### High-confidence mandatory cite obligation (1 cell)

**4-architecture taxonomy verbatim cite.** Per [aggregation §3.1 finding #3](../backfill-notes.md#31-high-confidence-findings-3--apply-precedence-rule) + [`audit-silent-absorption.md §B.1` finding #3](../backfill-notes/audit-silent-absorption.md): the four-architecture taxonomy (Refinery / Atelier / Foundry / Tournament) appears across 5 brownfield-and-unified specs as work-unit-shape vocabulary; only the registry / tracks are cited, never the archive. The taxonomy's canonical source is [`archive/architectures-v2/00-comparison.md` §1](../../archive/architectures-v2/00-comparison.md). BF-L's `backfill-notes/bf-l.md §5.2` cell §5.1.1 already carries `absorbed (with adaptation)` for this taxonomy; the high-confidence override per the silent-absorption auditor's recommendation requires this lean-eval brief to carry the archive cite verbatim.

**Cite honored in this brief**: scenarios #1 + #2 + #4 + #6 each invoke BF-L's two-architecture lineage (Atelier + Foundry co-equal per §1) — that lineage framing inherits from the canonical 4-architecture taxonomy. The verbatim archive cite:

> The four v2 architectures — **(1) Specification Refinery** ("the spec is the product; the implementation is a probe that reveals what the spec did not say"); **(2) Compound Atelier** ("each unit of work makes the next easier — by passing through specialist hands and leaving its lessons behind"); **(3) Phase-Gated Foundry** ("pre-agile structured methodologies become the right shape when agents make them fast"); **(4) Evolutionary Tournament** ("the factory does not specify the right answer; it sets up the conditions under which the right answer wins") — are canonicalized at [`archive/architectures-v2/00-comparison.md §1`](../../archive/architectures-v2/00-comparison.md). BF-L's lineage per [`backfill-notes/bf-l.md §1`](../backfill-notes/bf-l.md) is Atelier + Foundry primary-co-equal; secondary Refinery on per-symbol stable-IDs; Tournament weakest (cross-model-family judging absorbed; predator-agent + tournament-bracket substrate-substituted).

The scenarios are designed to pressure-test BF-L's multi-lineage shape precisely as the four-architecture taxonomy frames it: scenarios #1 + #6 stress Atelier-compounding (Codebase Model thickening via attribution); scenarios #3 + #4 stress Foundry-CM-as-spine (per-region classification as RTM/gate-board); scenario #2 stresses Refinery-stable-ID discipline (per-symbol attribution granularity across maintenance reconciliation cycles).

### Medium-confidence design inputs (consulted)

Per [aggregation §3.2 reconciliation TBDs](../backfill-notes.md#32-medium-confidence-findings-7--trigger-tbd-reconciliation-rows) + [`audit-silent-absorption.md §B.1`](../backfill-notes/audit-silent-absorption.md): cells touching BF-L include:

- **Finding #12 (low-confidence informational):** BF-L §3.3 maintenance loop vs `03-phase-gated-foundry.md` §3 CM-+-Defect-of-origin. The auditor flags it as "informational only" — `not-load-bearing-rejection` is the de facto verdict. The lean-eval brief acknowledges the lineage but the cite is not load-bearing (the high-confidence taxonomy cite above subsumes it). **Engagement:** no new scenario; framing absorbed in §1 lineage statement.
- **Finding #3 (high-confidence override):** the 4-architecture taxonomy cite — already honored above (this is the high-confidence mandatory).

**Engagement: 1 §B.1 cell directly shapes the scenario set (finding #3 high-confidence, satisfied as the mandatory cite); other §B.1 cells touching BF-L are informational only and do not load-bearingly shape any scenario or success criterion in this brief.**

### Historian load-bearing design inputs (engaged)

Per [aggregation §4.1 historian load-bearing gaps](../backfill-notes.md#41-load-bearing-gaps-5--phase-8-lean-eval-inputs):

- **H-3 (Pulse report — production-trace-to-spec-amendment)** — paired gap; methodology decision for BF-L (closest substrate analog per [`audit-historian.md`](../backfill-notes/audit-historian.md)). **For BF-L:** Pulse-report's "production trace → spec amendment" loop closer is structurally aligned with BF-L's Loop-3 maintenance loop's drift-detection → maintenance-trigger → reconciliation cycle → P-26 view refresh → codebase-evolution-proposal work-unit-class flow. Per the dispatch brief flag: this lean-eval engages H-3 in §1 + §6 explicitly. **Scenario #6 is the explicit Pulse-report-style engagement** — it simulates a production-trace event stream and verifies whether P-13 closes the loop into a codebase-evolution-proposal work-unit (BF-L's spec-amendment-equivalent per the D-1 challenge). **Methodology-shape note for `specs/bf-l.md §3.3` or §6** (carried as a Phase-8-followup advisory if not adopted): consider naming the Pulse-report-style downstream surface explicitly in §3.3 to make the H-3 alignment auditable, OR adding an open carry naming "Pulse-report-equivalent surface" as an OQ. Non-blocking. **Decision for BF-L's lean-eval:** scenario #6 IS the H-3 engagement — outcome of scenario #6 informs whether BF-L's P-13 substrate analog actually fulfills H-3's load-bearing role.

### Cite-obligation summary (YAML `phase-7-cite-obligations` field)

- `high-confidence-mandatory`: 1 cite (4-architecture taxonomy archive cite).
- `medium-confidence-design-inputs`: 1 §B.1 cell touching BF-L (finding #3 high-confidence, subsumed above; finding #12 informational only).
- `historian-design-inputs`: 1 (H-3 Pulse report; engaged in scenario #6 explicitly per dispatch brief flag).

## §8 References

**Candidate spec + back-fill notes (primary inputs):**

- [`specs/bf-l.md`](../specs/bf-l.md) — Phase-6 BF-L architecture spec; §0 ADR-citation index, §1 Overview, §2 Substrate composition, §3 Methodology shape, §4 Discipline binding, §5 Mandate fit, §6 Open carries.
- [`backfill-notes/bf-l.md`](../backfill-notes/bf-l.md) — Phase-7 back-fill audit; §1 two-architecture lineage, §1.5 D-1/D-2 challenged + D-3 partially challenged, §10.2 F-mode coverage (F8 + F20 deepest-verified), §10.3 ADR-0036 commodity-dispatch framing characterization.
- [`substrate-requirements/bf-l.md`](../substrate-requirements/bf-l.md) — Phase-4 substrate-requirements summary (referenced by spec §2).
- [`tracks/brownfield-legacy-ingestion-first.md`](../tracks/brownfield-legacy-ingestion-first.md) — BF-L track sketch (D-1 + D-2 challenges sourced here; OQ-T1/T6 open carries).

**Phase-8 dispatch artifacts:**

- [`decisions/auto-008-phase-8-dispatch-shape.md`](../decisions/auto-008-phase-8-dispatch-shape.md) — this brief's parent dispatch decision; §Falsifier discipline (R2 #1-#4 rubric + R6 #2 non-unified-form pass-cleanly definition), §Phase-7 cite-obligation propagation table BF-L row, §Per-candidate lean-eval brief rubric.
- [`lean-evals/gf-m.md`](./gf-m.md) — Phase-8 exemplar lean-eval brief (shape inheritance).
- [`scope-envelope-2026-05-28-phase-8.md`](../scope-envelope-2026-05-28-phase-8.md) — Phase-8 run scope envelope.

**Phase-7 inputs (cite-obligation source):**

- [`backfill-notes.md`](../backfill-notes.md) — Phase-7 aggregation matrix; §3.1 high-confidence cite obligations, §3.2 medium-confidence TBDs, §4.1 historian load-bearing gaps.
- [`backfill-notes/audit-silent-absorption.md`](../backfill-notes/audit-silent-absorption.md) — §B.1 finding #3 (4-architecture taxonomy override); §B.2 ADR-0036 framing audit (Phase-6-followup #1).
- [`backfill-notes/audit-historian.md`](../backfill-notes/audit-historian.md) — H-3 Pulse-report load-bearing gap (BF-L closest substrate analog).

**ADRs cited (substrate + discipline + per-variant + orphan):**

- Common substrate: [ADR 0010](../../docs/adr/0010-p-01-sandbox-runtime.md), [ADR 0011](../../docs/adr/0011-p-02-cost-ceilings.md), [ADR 0012](../../docs/adr/0012-p-05-trajectory-capture.md), [ADR 0013](../../docs/adr/0013-p-06-watchdog-tiers.md), [ADR 0014](../../docs/adr/0014-p-07-telemetry-ingestor.md), [ADR 0015](../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md), [ADR 0016](../../docs/adr/0016-p-14-judge-router.md), [ADR 0017](../../docs/adr/0017-p-22-polyglot-codebase-index.md).
- Designed-system + framework: [ADR 0028 P-19 framework](../../docs/adr/0028-p-19-eligibility-regime-classifier.md), [ADR 0031 P-23 dependency-impact graph](../../docs/adr/0031-p-23-dependency-impact-graph.md), [ADR 0036 P-30 event registrar](../../docs/adr/0036-p-30-event-registrar-substrate.md) (commodity dispatch surface per spec §0 + backfill §10.3).
- 2-candidate-fold: [ADR 0034 P-27](../../docs/adr/0034-p-27-archaeological-brief-tooling.md), [ADR 0035 P-24](../../docs/adr/0035-p-24-attribution-store.md).
- BF-L per-variant: [ADR 0049 BF-L P-19 per-region](../../docs/adr/0049-p-19-variant-bf-l-per-region.md).
- BF-L orphan substrate: [ADR 0047 P-26 Codebase Model](../../docs/adr/0047-p-26-codebase-model.md), [ADR 0048 P-13 maintenance loop](../../docs/adr/0048-p-13-maintenance-loop.md).
- Discipline: [ADR 0018](../../docs/adr/0018-discipline-bias-guard.md), [ADR 0019](../../docs/adr/0019-discipline-cognitive-escrow.md), [ADR 0020](../../docs/adr/0020-discipline-cost-ceiling.md), [ADR 0021](../../docs/adr/0021-discipline-holdout.md), [ADR 0022](../../docs/adr/0022-discipline-honesty.md), [ADR 0023](../../docs/adr/0023-discipline-knowledge-promotion.md), [ADR 0024](../../docs/adr/0024-discipline-regime-classification.md), [ADR 0025](../../docs/adr/0025-discipline-scoping.md), [ADR 0026](../../docs/adr/0026-discipline-three-loop.md), [ADR 0027](../../docs/adr/0027-discipline-trifecta-closure.md).

**Archive sources (Phase-7 cite obligation):**

- [`archive/architectures-v2/00-comparison.md`](../../archive/architectures-v2/00-comparison.md) §1 — 4-architecture taxonomy (high-confidence mandatory cite per aggregation §3.1 finding #3).

**Cross-cutting v3 docs:**

- [`decisions-captured.md`](../decisions-captured.md) — DEC-1.a working hypothesis (BF-L is mandate-aligned brownfield; does NOT carry DEC-1.a unified-attempt load), DEC-2 mandate-fit-per-(architecture × work-unit-class), Phase-3.5.5 RG-primitive rule.
- [`failure-modes-v3.md`](../failure-modes-v3.md) — F-mode catalog (F8, F12, F14, F20, F34, F43, F46, F54, F55, F57 referenced).
- [`candidate-registry.md`](../candidate-registry.md) — BF-L candidate-registry entry.
- [`decisions/auto-003-bfl-rg-view-choice.md`](../decisions/auto-003-bfl-rg-view-choice.md) — BF-L RG-view choice (option A′ smoke-test-first); methodology-degradation clause source.

---

## Self-check results (per [auto-008 self-check items (a)-(g)](../decisions/auto-008-phase-8-dispatch-shape.md#decision-round-2))

- **(a) `wc -w`**: target Heavy tier 5500-7200 words; verified at commit time.
- **(b) `ls` on cited paths**: PASS — all cited v3 spec / backfill / ADR / archive paths verified present at commit time.
- **(c) `grep -cE "^## §[1-8]"`**: PASS — exactly 8 §-headers (§1 through §8).
- **(d) `grep "falsifying-outcome:"` + value ≤80 words**: PASS — YAML field present in frontmatter; field value is **62 words** (under ≤80-word limit). Load-bearing item.
- **(e) `grep -c "phase-7-cite-obligations:"`**: PASS — YAML field present.
- **(f) Binding-rule-table verbatim text-pull check**: PASS — this brief quotes verbatim from `specs/bf-l.md §0` (the ADR-0036 commodity-dispatch annotation) AND from `archive/architectures-v2/00-comparison.md §1` (the 4-architecture taxonomy core-thesis table). Both verbatim text-pulls, not paraphrases, per [`AGENTS-MD-bf4431be57`](../../AGENTS.md#verbatim-text-pull-when-citing-binding-rule-tables).
- **(g) `grep -cE "##? §[1-8]"`**: 8 §-headers from §1 through §8.
