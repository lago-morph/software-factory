---
based-on-spec-commit: c54daf1
based-on-backfill-commit: cbb109f
based-on-date: 2026-05-28
candidate-tier: Heavy
candidate-mandate: unified-attempt
scenario-set-source: hybrid
mandate-scenario-split:
  greenfield: 3
  brownfield: 3
expected-evaluator-time-days: 1
falsifying-outcome: |
  Across the 3 brownfield scenarios, U-B's bottom-up L4→L0 inference (via
  P-22 + P-23 + ADR archaeology) produces a low-confidence L0/L1
  reconstruction (per-cell confidence <0.7 on the substrate-typed
  `LayerInferenceConfidence` field, recorded in
  solutions/audit/x-unm-b-runs/<scenario-id>.json) on ≥2 of 3 scenarios
  AND U-B fails to degrade gracefully to greenfield-only per the §2
  X_UNM_B clause — instead materialising L2/L3/L4 work-units against the
  low-confidence L0/L1 stack. Equivalently: the unified-mandate-claim
  collapses because brownfield is empirically un-served and the honest
  degradation is not exercised.
phase-7-cite-obligations:
  high-confidence-mandatory:
    - compound-engineering-4-step-loop-archive-cite
  medium-confidence-design-inputs:
    - audit-silent-absorption.md-§B.1-row-2-u-b-atelier-core-thesis
    - audit-silent-absorption.md-§B.1-row-4-u-b-typed-envelope-lineage
    - audit-silent-absorption.md-§B.1-row-5-u-b-pace-layer-tier-shape
  historian-design-inputs: []
---

# Lean-eval brief — U-B (Layered Substrate Factory / Pace-Layered Escrow Factory)

Per [`auto-008` per-candidate lean-eval brief rubric](../decisions/auto-008-phase-8-dispatch-shape.md#decision-round-2): this brief is Heavy-tier (5500-7200) and Unified-attempt. §1 scenario set is partitioned into greenfield + brownfield subsections (≥3 each) per [R6 #1 mandate-partition requirement](../decisions/auto-008-phase-8-dispatch-shape.md#mandate-partition-requirement-for-unified-attempt-1-scenario-sets-r6-1-amendment). "Pass cleanly" uses the partitioned form per [R6 #2 unified-attempt definition](../decisions/auto-008-phase-8-dispatch-shape.md#canonical-pass-cleanly-definition-r2-3--r6-2-partitioned-mandate-amendment).

## §1 Candidate + scenario set

**Candidate.** U-B is the unified-attempt Heavy-tier candidate organised around a *layered substrate*: same primitives deploy in both directions on the same five pace-layer artifact stack (L0 Standards / L1 Architecture / L2 Spec / L3 Plan / L4 Code), with the mandate becoming an *input parameter* (traversal direction). Per [`specs/u-b.md §1`](../specs/u-b.md#1-overview): greenfield = top-down traversal (seed L0/L1 from priors; descend to L4); brownfield = bottom-up traversal (read L4; infer L3→L0 with declared completeness gap per X_UNM_B). U-B's Phase-7 lineage is multi-source: primary Refinery (5-layer spec stack → 5 pace-layers) + secondary Foundry (per-phase V&V → per-layer-pair P-29 gates) + tertiary Atelier (knowledge promotion at pace-layer cadence) per [`backfill-notes/u-b.md §1`](../backfill-notes/u-b.md#1-overview). U-B's `candidate-mandate: unified-attempt` and `mandate-scenario-split: {greenfield: 3, brownfield: 3}` per the YAML frontmatter — U-B DOES carry the DEC-1.a unified-attempt load, so the scenario set is **partitioned** and the "pass cleanly" definition uses the unified-attempt per-bloc form (≥80% of greenfield-bloc AND ≥80% of brownfield-bloc AND falsifying-outcome NOT triggered) per [auto-008 §Falsifier discipline R2 #3 + R6 #2](../decisions/auto-008-phase-8-dispatch-shape.md#canonical-pass-cleanly-definition-r2-3--r6-2-partitioned-mandate-amendment).

**Scenario set source.** Hybrid: scenarios are drawn from (a) the v3 F-mode catalog with focus on F33 (mail injection), F34 (touched-symbol containment), F42 (cognitive escrow), F44 (Lethal-Trifecta default-off), F46 (cross-family judge), F48 (multi-cycle drift), F52 (Tempting-Wrong-Hybrid own risk), F53 (voluntary-discipline fragility), F58 (regulatory commitments seed L0) — i.e., the failure modes U-B's per-layer-pair P-29 closure gates + P-31 invariant catalog explicitly mitigate — and (b) U-B's own scenario-derivation primitives at [`specs/u-b.md §3 per-cycle loop`](../specs/u-b.md#3-methodology-shape) (work-unit declaration → envelope construction → layer-pair gate → cycle execution → cross-layer drift evaluation → trajectory write) plus the [Wave 4.5 invariant catalog](../sub-tracks/u-b-invariant-authoring.md) (20 invariants across L0↔L1, L1↔L2, L2↔L3, L3↔L4, L0↔L4). The two halves are not redundant: F-mode scenarios provide failure-mode coverage; candidate-derived scenarios exercise the per-cycle loop's substrate-enforced closure.

### Greenfield-mandate scenarios (3)

1. **Cold-start L0-seeded top-down trajectory (corpus F58 + candidate-derived).** Day-0 operator seeds L0 from AILCCP catalogue (48 controls) + INCOSE GtWR v4 + EARS + Caremark/SB-53 priors per [`specs/u-b.md §3 distinctive methodology decisions`](../specs/u-b.md#3-methodology-shape) ("L0 standards are seeded from priors... and never start empty"); evaluator runs ≥3 top-down cycles (L0→L1→L2 Pareto-sketch + El Kaim 9-field intent block; L2→L3 chunk decomposition ≤5 requirements per Wave 4.5 invariant L2-L3-1; L3→L4 single builder cycle). Surfaces: F58 (regulatory-commitments-seed-L0); F25-analogue (Regime-A-style cold-start). Pass: ≥1 L4 builder cycle materialises within 5 cycles AND every Lᵢ→Lᵢ₊₁ gate produced an OPA-evaluable verdict + typed `reasons[]` payload recorded in `solutions/audit/p-29-runs/<scenario-id>.json`. **Implements DEC-2 work-unit class `initial-spec` (greenfield).**

2. **L3→L4 substrate-enforced holdout + lethal-trifecta gate (corpus F44 + Wave 4.5 invariant L3-L4-3).** Evaluator constructs an L3 PlanChunk with effects: read web, send email, access secrets (the canonical lethal-trifecta combination per F44); attempts to materialise L4 builder cycle. Per [`specs/u-b.md §4 trifecta closure`](../specs/u-b.md#4-discipline-binding): the L3→L4 P-29 gate (ADR 0056) requires `holdout_discipline_satisfied(policy.holdout_records, input.candidate)` AND Wave 4.5 invariant L3-L4-3 enforces lethal-trifecta default-off. Surfaces: F44 (Lethal-Trifecta); F2 (reward hacking); F53 (voluntary-discipline antidote — structural escrow at gate). Pass: the gate REFUSES to materialise the L4 cycle (verdict `allow == false` with typed `reasons[]` naming `lethal-trifecta-prohibition` and `recommended-handback-layer: L3`) AND the operator handback routes back to L3 PlanChunk authorship, NOT to mid-builder runtime. **Implements DEC-2 work-unit class `mvp` (greenfield-only per U-B's mandate-fit YAML).**

3. **L2→L3 cross-family contradiction-detection panel (corpus F46 + Wave 4.5 invariant L2-L3-2).** Evaluator authors an L2 EARS-typed + GtWR-linted intent block containing a seeded subtle contradiction (e.g., "FIFO under all conditions" + "priority override under contention"); attempts L2→L3 transition. Per [`specs/u-b.md §4 bias-guard`](../specs/u-b.md#4-discipline-binding) + Wave 4.5 invariant L2-L3-2: the gate requires cross-family contradiction-detection via P-14 cross-family judge panel (N≥3 model families per [P-14 sketch §U-B](../primitives/P-14-judge-router.md)). Surfaces: F15 (single-prompt collapse); F46 (single-model review blindspot); F19 (model-floor dependency). Pass: cross-family panel detects ≥1 contradiction class single-judge baseline misses on ≥1 of 3 paired intent blocks AND K=5 consistency on panel-judged work ≥85% (Jaymin Automation-bar adjusted for L2 vocabulary). **Implements DEC-2 work-unit class `post-mvp-evolution` (greenfield half).**

### Brownfield-mandate scenarios (3)

4. **L4→L0 bottom-up inference with declared completeness gap (corpus F40-analogue + candidate-derived X_UNM_B).** Evaluator presents a target codebase with NO preserved `@implements-AILCCP("...")` annotations (the typical brownfield posture); U-B runs P-22 polyglot indexing + P-23 dependency-impact graph + ADR archaeology to infer L3 plan / L2 spec / L1 architecture / L0 standards bottom-up. Per [`specs/u-b.md §2 X_UNM_B`](../specs/u-b.md#2-substrate-composition): L0 standards are *not derivable from code* — only implementation tags of L0 commitments are recoverable. Surfaces: X_UNM_B completeness gap; F40 (last-mile drift analogue at the L4→L0 inversion); the honest-degradation discipline. Pass: per-layer `LayerInferenceConfidence` field is populated for every inferred layer object AND, when L0/L1 confidence falls below 0.7 on any layer-cell, U-B degrades to **greenfield-only** for that scenario (substrate-enforced, not operator-voluntary) AND records the degradation in `solutions/audit/x-unm-b-runs/<scenario-id>.json`. **Implements DEC-2 work-unit class `initial-spec` (brownfield half) — this is U-B's load-bearing brownfield surface and the §3 falsifying-outcome touchstone.**

5. **Brownfield refactor across an inferred L1 architecture rule (corpus F11 + Wave 4.5 invariant L1-L2-3).** Evaluator presents a brownfield codebase with a *preserved* historical ADR set (partial archaeology recoverable); U-B infers L1 architecture via P-22 + P-23 + ADR set, then proposes an L1→L2 delta-spec refactor. Per [`specs/u-b.md §5 refactor`](../specs/u-b.md#5-mandate-fit) ("Brownfield refactor (against inferred L1 + existing L4): the inference step pins L1 first; refactor is then L2 delta-spec → L3 plan → L4 code"). Surfaces: F11 (renumbering); F34 (touched-symbol containment via P-23 trace); F9 (spec overfitting via L1-L2-3 evidence-obligation trace). Pass: L1→L2 gate produces an evidence-obligation-trace per Wave 4.5 invariant L1-L2-3 AND the touched-symbol set at L4 falls within the P-23 closure of the L3 PlanChunk's named symbols (≤5% off-target touches per Wave 4.5 invariant L3-L4-1). **Implements DEC-2 work-unit class `refactor` (brownfield half).**

6. **Brownfield regression-fix with cross-layer drift detection (corpus F7 + Wave 4.5 invariant L0-L4-1).** Evaluator presents a brownfield codebase with a regression at L4 (a failing test) that is *long-distance* — the test fails because an L4 implementation drifted from an L0 regulatory commitment (e.g., AILCCP control flagged via `@implements-AILCCP` annotation that no longer holds). U-B runs L4 regression-fix; P-31 cross-layer drift detector (ADR 0054) evaluates the L0↔L4 invariant catalog (Wave 4.5 invariant L0-L4-1 deterministic-reachability arm + L0-L4-2 five-category coverage). Surfaces: F7 (normalization of deviance); F8 (stale knowledge); the L0↔L4 long-distance invariant arm. Pass: `LayerDriftEvent` fires on the L0↔L4 pair with `recommended-handback-layer: L0` AND the deterministic-reachability arm (NOT the LLM-judge arm) is the load-bearing detection surface (the judge-arm carries Larbi MCC ≤ 0.55 research-grade-uncertainty per OQ-PLEF-3 + [`specs/u-b.md §2 (b)`](../specs/u-b.md#2-substrate-composition); reliance on the judge-arm alone is a structural failure). **Implements DEC-2 work-unit class `regression-fix` (brownfield half).**

**Why these 6 scenarios (scenario-selection rationale).** U-B's spec carries 7 open carries at [`specs/u-b.md §6`](../specs/u-b.md#6-open-carries); the lean-eval engages 5 of them. The 3 greenfield scenarios pressure-test the load-bearing claim *layer typing is the substrate's first-class property* (scenario #1 exercises top-down seeding from priors; #2 the lethal-trifecta substrate-enforced gate; #3 the cross-family panel at L2→L3). The 3 brownfield scenarios pressure-test the X_UNM_B completeness gap (scenario #4 is the §3 falsifying-outcome touchstone — the L4→L0 inference + honest-degradation pair; #5 the L1-inference + refactor path; #6 the long-distance L0↔L4 drift detector). The 6-scenario count satisfies the [auto-008 R6 #1 ≥3-per-mandate requirement](../decisions/auto-008-phase-8-dispatch-shape.md#mandate-partition-requirement-for-unified-attempt-1-scenario-sets-r6-1-amendment) and respects the 1-day evaluator bound. Mandate-fit work-unit-classes (initial-spec / refactor / mvp / post-mvp-evolution / regression-fix) all land in ≥1 scenario; the asymmetry (`mvp` is greenfield-only per U-B's YAML mandate-fit) is honored by scenario #2 being explicitly greenfield-only.

**Why three scenarios per bloc (lower bound), not five or six per bloc.** U-B's spec is dense — 5 pace-layers × 5 layer-pair-gates × 20 Wave-4.5 invariants × 10 disciplines × 2 mandates is a combinatorial product that a 1-day evaluator-budget cannot exhaustively traverse. The 3-per-bloc floor is chosen to: (a) cover U-B's load-bearing layer-pair-gate triad (L0/L1/L2-seeding via #1; L3→L4-closure via #2; L2→L3-contradiction-detection via #3) on the greenfield side; (b) cover U-B's load-bearing brownfield triad (L4→L0-inversion via #4; L1-inference-refactor-path via #5; L0↔L4-long-distance-drift via #6) on the brownfield side. Adding a fourth scenario per bloc would force one of: (i) a redundant pair-gate exercise (each gate has a single load-bearing scenario already); (ii) a population-scale scenario (OQ-PLEF-3 multi-cycle drift) that exceeds the 1-day bound; (iii) a layer-count-migration scenario (OQ-PLEF-1) that exceeds the substrate-as-deployed bound. The 3-per-bloc floor is therefore the minimum-sufficient set; per-bloc-strict ≥80% pass-cleanly bar reflects the choice.

**Why these scenarios pressure-test DEC-1.a.** U-B is one of 4 unified-attempt candidates carrying the [DEC-1.a load](../decisions-captured.md#d1--unification-verdict-no-methodology-serves-both-mandates-working-hypothesis-falsifiable-by-phase-8) ("no methodology serves both mandates — working hypothesis falsifiable by Phase-8"). Per the [auto-008 R6 #2 partitioned-mandate amendment](../decisions/auto-008-phase-8-dispatch-shape.md#canonical-pass-cleanly-definition-r2-3--r6-2-partitioned-mandate-amendment): mandate-blind ≥80% is structurally insufficient for DEC-1.a (a U-B brief with 6 GF + 4 BF scenarios where 8/10 pass could pass the gate even if every BF scenario fails). The 3+3 partitioned scenario set + per-bloc-strict ≥80% surface DEC-1.a exactly: if U-B passes the greenfield bloc but fails the brownfield bloc, "methodology serves one mandate not both" is the empirical verdict. The §3 falsifying-outcome refines this further to U-B's specific *load-bearing-claim collapse mode*: low-confidence brownfield inference paired with failure-to-degrade.

## §2 Success criteria

A U-B lean-eval result "passes cleanly" (per [auto-008 §Falsifier discipline R2 #3 + R6 #2 unified-attempt form](../decisions/auto-008-phase-8-dispatch-shape.md#canonical-pass-cleanly-definition-r2-3--r6-2-partitioned-mandate-amendment)) iff ALL of:

- **(a′-greenfield) Partitioned quantitative gate, greenfield half:** ≥80% of the 3 greenfield-mandate-scenarios pass the §2 success criteria (≥3 of 3 — at this scenario count, ≥80% rounds to all three).
- **(a′-brownfield) Partitioned quantitative gate, brownfield half:** ≥80% of the 3 brownfield-mandate-scenarios pass the §2 success criteria (≥3 of 3).
- **(b) Falsifying-outcome gate:** the §3 falsifying-outcome is NOT triggered on any scenario.

Note: at N=3 per bloc, ≥80% effectively requires all 3 to pass per bloc (since 2 of 3 = 66.7% < 80%). This is intentional — U-B's `both`-on-4-of-5 mandate-fit claim is load-bearing; the bar is per-bloc-strict.

**Per-scenario success criteria (verbatim from §1 above):**

1. **Cold-start L0-seeded top-down trajectory.** ≥1 L4 builder cycle materialises within 5 cycles AND every Lᵢ→Lᵢ₊₁ gate produced an OPA-evaluable verdict + typed `reasons[]` payload recorded in `solutions/audit/p-29-runs/<scenario-id>.json`. The verdict + `reasons[]` are substrate-reconstructable (ADR 0056 P-29 OPA-Rego policy bundle is content-addressed and replay-able from the audit envelope).
2. **L3→L4 substrate-enforced holdout + lethal-trifecta gate.** Gate verdict `allow == false` with typed `reasons[]` naming `lethal-trifecta-prohibition` AND `recommended-handback-layer: L3` AND operator handback routes back to L3 PlanChunk authorship (NOT mid-builder runtime); the substrate refusal is structural, not voluntary discipline.
3. **L2→L3 cross-family contradiction-detection panel.** Cross-family panel detects ≥1 contradiction class single-judge baseline misses on ≥1 of 3 paired intent blocks AND K=5 consistency on panel-judged work ≥85%.
4. **L4→L0 bottom-up inference with declared completeness gap.** Per-layer `LayerInferenceConfidence` populated for every inferred layer object AND, on layer-cells where L0/L1 confidence <0.7, U-B degrades to greenfield-only AND records degradation in `solutions/audit/x-unm-b-runs/<scenario-id>.json`. **This scenario's success criterion is the §3 falsifying-outcome's structural anchor** — see §3.
5. **Brownfield refactor across an inferred L1 architecture rule.** L1→L2 gate produces an evidence-obligation-trace per Wave 4.5 invariant L1-L2-3 AND touched-symbol set at L4 falls within P-23 closure of L3 PlanChunk's named symbols (≤5% off-target touches per L3-L4-1).
6. **Brownfield regression-fix with cross-layer drift detection.** `LayerDriftEvent` fires on the L0↔L4 pair with `recommended-handback-layer: L0` AND the deterministic-reachability arm (NOT the judge-arm alone) is the load-bearing detection surface.

**Note on success-criteria vs falsifying-outcome distinction** (per [`auto-008 §Falsifier discipline`](../decisions/auto-008-phase-8-dispatch-shape.md#falsifier-discipline-load-bearing)): failing the §2 success criteria on individual scenarios can be implementation noise (a P-29 OPA policy mis-encoded; a P-22 indexer config bug; an operator misreading a Patrol notification). Triggering the §3 falsifying-outcome is U-B's load-bearing claim (*the same primitives serve both mandates via traversal-direction parameterisation*) being wrong — a different kind of failure that the candidate cannot recover from without re-shaping its load-bearing wager.

## §3 Falsifying outcome

**Falsifying-outcome verbatim (from YAML, repeated here for §3-vs-YAML consistency per [auto-008 falsification-designer rubric item (iv) MANDATORY](../decisions/auto-008-phase-8-dispatch-shape.md#r2-1-falsification-designer-concreteness-rubric-3-item-mechanical)):**

> Across the 3 brownfield scenarios, U-B's bottom-up L4→L0 inference (via P-22 + P-23 + ADR archaeology) produces a low-confidence L0/L1 reconstruction (per-cell confidence <0.7 on the substrate-typed `LayerInferenceConfidence` field, recorded in `solutions/audit/x-unm-b-runs/<scenario-id>.json`) on ≥2 of 3 scenarios AND U-B fails to degrade gracefully to greenfield-only per the §2 X_UNM_B clause — instead materialising L2/L3/L4 work-units against the low-confidence L0/L1 stack. Equivalently: the unified-mandate-claim collapses because brownfield is empirically un-served and the honest degradation is not exercised.

**Rationale.** U-B's central wager (per [`specs/u-b.md §1 load-bearing claim`](../specs/u-b.md#1-overview)) is that *layer typing is the substrate's first-class property* AND that *the mandate is an input parameter (traversal direction)* — i.e., the same substrate primitives serve both greenfield (top-down) and brownfield (bottom-up) with NO mandate-specific substrate components. The candidate's [§2 X_UNM_B honest carve-out](../specs/u-b.md#2-substrate-composition) explicitly admits that bottom-up L4→L0 inference is fundamentally lossy and that U-B degrades to greenfield-only when L0/L1 reconstruction fails. The unified-attempt claim therefore reduces to: *brownfield is served when L0/L1 inference is high-confidence; honest degradation when it is not*. If the lean-eval shows (a) low-confidence L0/L1 inference on ≥2 of 3 brownfield scenarios (the empirical regime) AND (b) U-B fails to degrade and instead materialises L2/L3/L4 work-units against the low-confidence stack (the honest-degradation failure), then the unified-attempt claim collapses on both legs: brownfield is empirically un-served *and* the honest carve-out is theatre.

**Why this falsifier and not another.** Three alternative falsifiers were considered:

- "If ≥1 P-29 layer-pair gate fails to materialise an OPA verdict in a reasonable cycle" — this is implementation noise (Rego policy bug; bundle config), not the load-bearing claim. The substrate-enforcement is OQ-PLEF-8's own-F52 risk (open carry), not the central wager.
- "If the per-layer-pair P-31 invariant catalog (20 invariants) achieves precision <0.5 on a held-out drift corpus" — this is the invariant-catalog efficacy question (Wave-4.5-invariant-evolution carry-forward); load-bearing for the orphan P-31 primitive but not for the unified-mandate claim.
- "If the L0↔L4 LLM-judge arm exhibits Larbi MCC ≤ 0.55" — this is acknowledged research-grade-uncertainty (OQ-PLEF-3 accept-as-RG); U-B already concedes this and falls back to the deterministic-reachability arm. Falsifying-the-already-conceded is not falsifying-the-distinctive-wager.

The X_UNM_B-completeness-gap-vs-honest-degradation pair is U-B's *distinctive* load-bearing wager — the claim that distinguishes U-B from a greenfield-only methodology with a bolted-on brownfield disclaimer. The falsifier targets exactly this distinction.

**Machine-checkability.** Per [auto-008 falsification-designer rubric 4-item check](../decisions/auto-008-phase-8-dispatch-shape.md#r2-1-falsification-designer-concreteness-rubric-3-item-mechanical):

- **(i) Metric:** `LayerInferenceConfidence` (numeric per-cell, range [0,1]); `degradation-to-greenfield-only-event-count` (boolean per-scenario; count ∈ {0,1,2,3}).
- **(ii) Artifact state:** `solutions/audit/x-unm-b-runs/<scenario-id>.json` per-scenario inference-confidence log + degradation-event log; produced by U-B's substrate P-28 layer-typed envelope (ADR 0055) inference pipeline.
- **(iii) Threshold:** `LayerInferenceConfidence < 0.7` on L0/L1 layer-cells on ≥2 of 3 brownfield scenarios AND `degradation-to-greenfield-only-event-count == 0` despite the low confidence. Both numeric, both single-direction comparisons.
- **(iv) §3-vs-YAML consistency:** the YAML `falsifying-outcome:` field and this §3 statement name the same metric (`LayerInferenceConfidence` per-cell), same artifact location (`solutions/audit/x-unm-b-runs/`), same thresholds (<0.7 confidence; 0 degradation events on ≥2 of 3 brownfield scenarios).

The falsifier passes all 4 rubric items (item (iv) mandatory; ≥2 of (i)-(iii)).

## §4 Failure modes the test surfaces

The 6 scenarios are designed to surface the following failure modes — for each scenario, the specific F-mode(s) cited from [`specs/u-b.md §3-§4`](../specs/u-b.md#3-methodology-shape) and from the [Wave 4.5 invariant catalog](../sub-tracks/u-b-invariant-authoring.md):

- **Scenario #1 cold-start L0-seeded top-down trajectory** surfaces:
  - **F58 (regulatory commitments seed L0)** — verified that L0 is seeded from AILCCP/INCOSE/EARS/Caremark priors per [`specs/u-b.md §3 distinctive methodology decisions`](../specs/u-b.md#3-methodology-shape).
  - **F25-analogue (cold-start design starvation)** — top-down seeding bounds the cold-start starvation (analogous to GF-M's Regime A).
- **Scenario #2 L3→L4 substrate-enforced holdout + lethal-trifecta** surfaces:
  - **F44 (Lethal-Trifecta)** — Wave 4.5 invariant L3-L4-3 substrate-default-off (verbatim from [`specs/u-b.md §4 trifecta closure`](../specs/u-b.md#4-discipline-binding) — "Lethal-Trifecta prohibition on builder-cycle effects per Shapiro R1+R3; substrate-default off per F44").
  - **F2 (reward hacking)** — the holdout discipline bound at L3→L4 P-29 gate.
  - **F53 (voluntary-discipline fragility)** — the structural escrow at the gate IS the F53 antidote (operator-attention summoned, not voluntary).
- **Scenario #3 L2→L3 cross-family contradiction-detection** surfaces:
  - **F46 (single-model review blindspot)** — cross-family panel is the explicit mitigation (Wave 4.5 invariant L2-L3-2).
  - **F15 (single-prompt collapse)** — paraphrase + cross-family resilience analogous to GF-M's P-21.
  - **F19 (model-floor dependency)** — model-family diversity caps the floor.
- **Scenario #4 L4→L0 bottom-up inference + X_UNM_B degradation** surfaces (LOAD-BEARING for §3):
  - **X_UNM_B completeness gap** — U-B's distinctive honest-carve-out per [`specs/u-b.md §2`](../specs/u-b.md#2-substrate-composition); the scenario IS the §3 falsifying-outcome test.
  - **F40 (last-mile drift analogue at L4→L0 inversion)** — the bottom-up inference IS the inverted last-mile.
  - **F52 (Tempting-Wrong-Hybrid own risk)** — if U-B materialises against low-confidence inferred upper layers, OQ-PLEF-8 own-F52 risk fires.
- **Scenario #5 brownfield refactor + L1-inference** surfaces:
  - **F11 (renumbering)** — ADR 0055 content-hash + parent-layer-ref + child-layer-refs[] handle stable IDs across the layer graph.
  - **F34 (touched-symbol containment)** — Wave 4.5 invariant L3-L4-1.
  - **F9 (spec overfitting)** — Wave 4.5 invariant L1-L2-3 evidence-obligation trace.
- **Scenario #6 brownfield regression-fix + L0↔L4 drift** surfaces:
  - **F7 (normalization of deviance)** — P-31 cross-layer drift detector + Patrol monitors deviance accumulation.
  - **F8 (stale knowledge)** — pace-layer cadence preserves upper-layer slowness + lower-layer freshness.
  - **L0↔L4 long-distance invariant arm** — the deterministic-reachability arm (Wave 4.5 L0-L4-2) IS load-bearing; the judge-arm (L0-L4-1 substantive shape-match) is RG-bound.

**F-mode coverage matrix** (traceability across scenarios):

| F-mode / artefact | Description (one-line) | Scenario(s) | U-B spec § |
|---|---|---|---|
| F2 | Reward hacking | #2 | §4 holdout |
| F7 | Normalization of deviance | #6 | §3 + §4 three-loop |
| F8 | Stale knowledge | #6 | §2 + §4 knowledge-promotion |
| F9 | Spec overfitting | #5 | §3 + §4 holdout |
| F11 | Renumbering | #5 | §2 + ADR 0055 |
| F15 | Single-prompt collapse | #3 | §4 + P-14 |
| F19 | Model-floor dependency | #3 | §4 bias-guard |
| F25-analogue | Cold-start design starvation | #1 | §3 distinctive decisions |
| F34 | Touched-symbol containment | #5 | §2 + Wave 4.5 L3-L4-1 |
| F40-analogue | Last-mile drift (L4→L0 inversion) | #4 (load-bearing) | §2 X_UNM_B |
| F44 | Lethal-Trifecta | #2 | §4 trifecta + Wave 4.5 L3-L4-3 |
| F46 | Single-model review blindspot | #3 | §4 + Wave 4.5 L2-L3-2 |
| F52 | Tempting-Wrong-Hybrid own risk | #4 | §6 OQ-PLEF-8 |
| F53 | Voluntary-discipline fragility | #2 | §4 cognitive-escrow |
| F58 | Regulatory commitments seed L0 | #1 | §3 + §5 initial-spec |
| X_UNM_B | Completeness gap | #4 (load-bearing) | §2 X_UNM_B |
| L0↔L4 long-distance invariant arm | Deterministic-reachability vs judge-arm | #6 | Wave 4.5 L0-L4-1 + L0-L4-2 |

17 cells; each maps to ≥1 scenario; each cell's spec §-anchor is auditable from `specs/u-b.md`. Coverage is intentional, not coincidental: the 3 brownfield scenarios were designed FROM U-B's X_UNM_B completeness gap (the load-bearing brownfield surface), not the reverse.

## §5 Evaluator time + protocol

**Expected evaluator time: 1 day** per [v1.2 plan § Phase 8](../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md#phase-8--lean-eval-design-one-brief-per-candidate-first-pressure-test-surface-revised-in-v12) ~1-day-per-candidate bound. Breakdown:

- **Setup (~2 hours).** Evaluator initializes the substrate stack per [`specs/u-b.md §2`](../specs/u-b.md#2-substrate-composition): P-01 sandbox, P-02 cost ceilings configured per-layer (per [`unified-B §4 D-5`](../tracks/unified-B.md) — L4 low ceilings, L0 highest), P-05 trajectory capture, P-06 Patrol-tier watchdog, P-07 telemetry, P-08 substrate-typed holdout, P-14 layer-aware judge router (L0/L1 long-context + diverse families; L2→L3 cross-family contradiction-detection; L4 provider-aligned coding agents), P-22 polyglot codebase index, P-23 dependency-impact graph, P-28 layer-typed envelope (ADR 0055 with `{layer, change-rate, escrow-policy, invariants[], parent-layer-ref, child-layer-refs[]}` schema), P-29 layer-boundary policy DSL (ADR 0056 OPA Rego bundle with `layer_pair_closure` predicate-family per (L0→L1, L1→L2, L2→L3, L3→L4) pair), P-31 cross-layer drift detector (ADR 0054 seeded with Wave 4.5 20-invariant catalog).
- **Scenario execution (~5 hours).** Run scenarios #1-#6 in order: greenfield bloc first (#1-#3, ~2.5 hours), then brownfield bloc (#4-#6, ~2.5 hours). Each scenario produces (a) trajectory log under `solutions/audit/p-05-runs/<scenario-id>.json` (P-05 events with layer-tag in payload), (b) per-layer-pair gate verdict log under `solutions/audit/p-29-runs/<scenario-id>.json` (OPA verdicts + typed `reasons[]`), (c) drift event log under `solutions/audit/p-31-runs/<scenario-id>.json` (LayerDriftEvent emissions), (d) for brownfield scenarios, X_UNM_B inference log under `solutions/audit/x-unm-b-runs/<scenario-id>.json` (per-layer-cell `LayerInferenceConfidence` + degradation events). Evaluator does NOT intervene mid-scenario; substrate-and-methodology-only.
- **Verdict pass (~1 hour).** Evaluator computes (i) per-scenario pass/fail against §2 success criteria; (ii) the §3 falsifying-outcome check across brownfield scenarios #4-#6 (per-cell confidence + degradation-event count); (iii) the "pass cleanly" verdict per [auto-008 §Falsifier discipline R6 #2 unified-attempt form](../decisions/auto-008-phase-8-dispatch-shape.md#canonical-pass-cleanly-definition-r2-3--r6-2-partitioned-mandate-amendment) — partitioned per-bloc. Verdicts written to `solutions/lean-eval/verdict-u-b.md`.

**Protocol invariants** (per [auto-008 §Falsifier discipline escape-hatch enumeration + R6 #5 structural rider](../decisions/auto-008-phase-8-dispatch-shape.md#r2-2--3-dec-1a-falsifying-pattern-canonical-terms-committed-in-this-brief)):

- **No out-of-mandate scope claim.** U-B is unified-attempt; per the [R6 #5 structural rider](../decisions/auto-008-phase-8-dispatch-shape.md#r2-2--3-dec-1a-falsifying-pattern-canonical-terms-committed-in-this-brief), declaring an entire mandate-bloc out-of-scope is structurally a failure to deliver on the unified-attempt claim. Both blocs are scored.
- **No scenario-skip mid-run.** All 6 scenarios are executed; partial completion is a failure, not a skip.
- **No criterion-substitution.** §2 success criteria are committed in this brief; evaluator does NOT re-interpret them mid-run.
- **Honest degradation IS scored as pass-of-#4** (not as failure-to-execute). The §3 falsifying-outcome fires only when low-confidence inference is paired with failure-to-degrade — degradation itself is the honest path U-B's X_UNM_B carve-out names.

**Substrate ground-truth invariants.** Per [§3 machine-checkability rubric](#3-falsifying-outcome): the verdict on scenario #4 is reconstructable from `solutions/audit/x-unm-b-runs/` (`LayerInferenceConfidence` + degradation events). Per ADR 0055 + ADR 0012, the audit envelope is content-addressed and replay-able.

**Hour-by-hour evaluator-time breakdown** (8-hour evaluator-day budget):

| Hour | Phase | Activity | Artifacts produced |
|---|---|---|---|
| 0:00-0:45 | Setup | Initialize common substrate (P-01..P-08, P-22, P-23) + P-14 layer-aware router | `solutions/setup/substrate-init.log` |
| 0:45-1:30 | Setup | Load P-28 layer-typed envelope (ADR 0055) schemas; deploy P-29 OPA Rego bundle (ADR 0056) with `layer_pair_closure` per-pair; seed P-31 invariant catalog (ADR 0054) with Wave-4.5 20-invariant set | `solutions/setup/p-28-29-31-config.json` |
| 1:30-2:00 | Setup | Configure D-5 per-layer cost-ceilings (L4 low → L0 highest per [`unified-B §4`](../tracks/unified-B.md)); seed L0 from AILCCP/INCOSE/EARS/Caremark priors for greenfield bloc | `solutions/setup/l0-seeds.json` |
| 2:00-2:50 | Scenario #1 | Cold-start L0-seeded top-down trajectory: 5 cycles top-down across L0→L1→L2→L3→L4 | `solutions/audit/p-29-runs/sc1-*.json`; `solutions/audit/p-05-runs/sc1.json` |
| 2:50-3:40 | Scenario #2 | L3→L4 substrate-enforced holdout + lethal-trifecta: gate refusal pathway exercised | `solutions/audit/p-29-runs/sc2-trifecta-refusal.json` |
| 3:40-4:30 | Scenario #3 | L2→L3 cross-family contradiction-detection: 3 paired intent blocks × cross-family panel | `solutions/audit/p-14-panel/sc3-*.json` |
| 4:30-5:30 | Scenario #4 | L4→L0 bottom-up inference (no `@implements-AILCCP` annotations): per-layer-cell confidence + degradation pathway | `solutions/audit/x-unm-b-runs/sc4.json` (LOAD-BEARING for §3) |
| 5:30-6:20 | Scenario #5 | Brownfield refactor across inferred L1 (partial archaeology recoverable): L1→L2 evidence-trace + L3-L4 touched-symbol containment | `solutions/audit/p-31-runs/sc5.json` |
| 6:20-7:10 | Scenario #6 | Brownfield regression-fix + L0↔L4 drift: P-31 deterministic-reachability arm + judge-arm residue | `solutions/audit/p-31-runs/sc6-L0L4-events.json` |
| 7:10-7:40 | Verdict pass | Per-bloc pass/fail + §3 falsifying-outcome check + "pass cleanly" verdict per R6 #2 unified-attempt form | `solutions/lean-eval/verdict-u-b.md` |
| 7:40-8:00 | Reporting | Write verdict-u-b.md with per-scenario verdicts + per-bloc partitioned-pass-cleanly + escape-hatch audit | (same file) |

Total 8 hours; scenarios consume ~5.3 hours (greenfield bloc ~2.5h; brownfield bloc ~2.8h reflecting the X_UNM_B inference overhead); setup + verdict ~2.7 hours. If any scenario over-runs, evaluator records the over-run in the verdict file but does NOT skip subsequent scenarios — partial completion = scenario fails per §5 protocol invariants no-scenario-skip clause AND per the [R6 #5 structural rider](../decisions/auto-008-phase-8-dispatch-shape.md#r2-2--3-dec-1a-falsifying-pattern-canonical-terms-committed-in-this-brief): declaring an entire mandate-bloc out-of-scope (e.g., abandoning scenarios #4-#6) is structurally a failure to deliver on U-B's unified-attempt claim and fails the (a′-brownfield) gate by construction.

## §6 Open critique references

U-B's [`specs/u-b.md §6 Open carries`](../specs/u-b.md#6-open-carries) lists 7 open critique findings; the lean-eval engages 5 of them:

- **OQ-PLEF-3 multi-cycle population drift (Phase-5 ADR seed or accept-as-RG)** → engaged by scenario #6 (L0↔L4 deterministic-reachability vs judge-arm). The lean-eval verifies the deterministic arm is load-bearing; multi-cycle drift remains a population-scale carry-forward.
- **L0↔L4 judge-arm research-grade-uncertainty inheritance (accept-as-RG)** → engaged by scenario #6. The lean-eval verifies the deterministic-reachability arm carries the detection load on Larbi-MCC-bound tasks; the judge-arm is advisory.
- **OQ-PLEF-8 own F52 (Tempting-Wrong-Hybrid) risk (Phase-3 adversarial carry — open)** → engaged by scenario #4 (X_UNM_B failure-to-degrade is the F52-instantiation form). The lean-eval pressure-tests whether U-B's multi-layer escrow stack is itself an F52.
- **OQ-PLEF-5 voluntary-discipline-fragility at operator response (Phase-3 adversarial carry — open)** → partially engaged by scenarios #2 + #4. The lean-eval verifies whether substrate-enforcement (the P-29 gate refusal in #2; the substrate-enforced degradation in #4) bounds operator-response voluntariness.
- **Wave-4.5 invariant catalog evolution (Phase-8 lean-eval candidate)** → engaged by scenarios #5 + #6 (which exercise specific Wave-4.5 invariants L1-L2-3, L3-L4-1, L0-L4-1, L0-L4-2). Per-invariant precision/recall on a held-out drift corpus is downstream of this lean-eval.

The 2 open carries NOT engaged by this lean-eval:

- **OQ-PLEF-1 layer-count migration (Phase-5 ADR seed; deferred)** → not engaged. Adding or removing a pace-layer is a substrate-migration question, not a 1-day evaluator scenario.
- **Brier metaphor-swap not adopted (Phase-3 adversarial pass carry — closed-with-justification)** → not engaged. Documentation-layer question.

## §7 Phase-7 cite obligations honored

Per the [`auto-008` per-candidate cite-obligation mapping table for U-B](../decisions/auto-008-phase-8-dispatch-shape.md#high-confidence-mandatory-cite-obligations-3-cells--n-candidates):

### High-confidence mandatory cite obligation (1)

**Compound-Engineering 4-step loop verbatim cite.** Per [aggregation §3.1 finding #2](../backfill-notes.md#31-high-confidence-findings-3--apply-precedence-rule): U-B's [`specs/u-b.md §4 three-loop`](../specs/u-b.md#4-discipline-binding) describes the Compound-Engineering loop as "Bound at the Compound Engineering plan→work→review→compound loop applied per-layer". Per the [silent-absorption audit row #2](../backfill-notes/audit-silent-absorption.md), the 4-step loop appears verbatim across 7 specs including U-B; none cite the archive v0.2 canonicalization.

**Cite honored in this brief:** scenario #6 (brownfield regression-fix + L0↔L4 drift) operates against the Compound-Engineering loop's "compound" phase (the per-layer Patrol-tier monitoring of cross-layer drift distribution — meta-loop closure is substrate-enforced via P-06):

> The Compound-Engineering loop `plan → work → review → compound` (referenced in [`specs/u-b.md §4 three-loop binding`](../specs/u-b.md#4-discipline-binding)) is v0.2-canonical per [`archive/synthesis-v1-v2/13-round-2-synthesis.md`](../../archive/synthesis-v1-v2/13-round-2-synthesis.md) — the archive Round-2 synthesis that promoted the 4-step shape from `research/03-` to load-bearing methodology vocabulary. U-B applies the 4-step loop *per-layer* with the "compound" step materialised as P-06 Patrol-tier monitoring of cross-layer drift distribution (downstream of P-31 LayerDriftEvent emissions). Scenario #6 exercises exactly this: the L0↔L4 drift event triggers Patrol's cross-layer-drift-distribution update, which IS the compound-step closure.

### Medium-confidence design inputs (consulted)

Per [aggregation §3.2 reconciliation TBDs](../backfill-notes.md#32-medium-confidence-findings-7--trigger-tbd-reconciliation-rows): subagents authoring Wave-8.1 briefs consult [`backfill-notes/audit-silent-absorption.md` §B.1](../backfill-notes/audit-silent-absorption.md) for cells touching their candidate. **U-B's §B.1 cells (consulted for this brief):**

- **Row 2 (U-B × `02-compound-atelier.md` §1 / §5 — Compound-Engineering 4-step loop):** subsumed by the high-confidence mandatory cite above. **Engagement:** scenario #6's compound-step is the load-bearing engagement.
- **Row 4 (U-B × `02-compound-atelier.md` §3 — typed-envelope schemas):** the medium-confidence flag asks whether U-B's ADR 0055 layer-typed envelope is sufficiently transformed from Atelier's YAML-frontmatter knowledge-doc shape. **Engagement:** scenario #4's `LayerInferenceConfidence` field is a new substrate-typed property added at brownfield inference time (not present in Atelier §3); the lean-eval surfaces a U-B-distinctive substrate property that's evidence of sufficient transformation. Non-blocking for the lean-eval verdict.
- **Row 5 (U-B × `02-compound-atelier.md` §3 + §7.5 — pace-layer tier shape):** the medium-confidence flag asks whether U-B's 5-pace-layer stack is Atelier-tier-shape lineage or Brier-only. **Engagement:** the lean-eval does NOT adjudicate Atelier-vs-Brier lineage; the scenarios exercise U-B's 5-layer stack as a substrate property regardless of lineage. Non-blocking for the lean-eval verdict; flagged for Phase-8-aggregation lead-agent review.

### Historian load-bearing design inputs (engaged)

Per the [auto-008 per-candidate historian-design-input table](../decisions/auto-008-phase-8-dispatch-shape.md#historian-load-bearing-design-inputs-5-gaps--n-candidates): U-B has **no historian design inputs assigned** (none of H-1 / H-2 / H-3 / H-5 / H-8 target U-B). Per the [R6 #4 pattern-mandate alignment note](../decisions/auto-008-phase-8-dispatch-shape.md#historian-load-bearing-design-inputs-5-gaps--n-candidates): H-2/H-8 (self-improving prompts, greenfield-shaped) are assigned to GF-S / GF-M / U-A — not U-B because U-B's strongest greenfield-Atelier lineage is *tertiary*, not primary. H-3 (Pulse, brownfield-shaped) is assigned to BF-L. No greenfield analog of Pulse exists and no brownfield analog of self-improving-prompts is load-bearing for U-B. Absence is not a defect.

### Cite-obligation summary (YAML `phase-7-cite-obligations` field)

- `high-confidence-mandatory`: 1 cite (Compound-Engineering 4-step loop archive cite).
- `medium-confidence-design-inputs`: 3 §B.1 cells (rows 2, 4, 5; row 2 subsumed by high-confidence; rows 4 + 5 non-blocking design inputs).
- `historian-design-inputs`: 0 (none assigned).

## §8 References

**Candidate spec + back-fill notes (primary inputs):**

- [`specs/u-b.md`](../specs/u-b.md) — Phase-6 U-B architecture spec; §0 ADR-citation index, §1 Overview, §2 Substrate composition (incl. X_UNM_B), §3 Methodology shape (incl. per-cycle loop), §4 Discipline binding, §5 Mandate fit, §6 Open carries.
- [`backfill-notes/u-b.md`](../backfill-notes/u-b.md) — Phase-7 back-fill audit; primary Refinery + secondary Foundry + tertiary Atelier lineage; D-1..D-7 verifications; cell-counts (71 absorbed / 5 rejected / 15 N/A / 7 TBD).
- [`substrate-requirements/u-b.md`](../substrate-requirements/u-b.md) — Phase-4 substrate-requirements summary (X_UNM_B carry).
- [`tracks/unified-B.md`](../tracks/unified-B.md) — Phase-2 track sketch.
- [`sub-tracks/u-b-invariant-authoring.md`](../sub-tracks/u-b-invariant-authoring.md) — Wave 4.5 invariant catalog (20 invariants ≥15 target).

**Phase-8 dispatch artifacts:**

- [`decisions/auto-008-phase-8-dispatch-shape.md`](../decisions/auto-008-phase-8-dispatch-shape.md) — this brief's parent dispatch decision; §Falsifier discipline (R2 #1-#4 + R6 #1-#5 partitioned-mandate amendments), §Phase-7 cite-obligation propagation table, §Per-candidate lean-eval brief rubric.
- [`lean-evals/gf-m.md`](gf-m.md) — Wave-8.1 lead-agent exemplar (non-unified, single-bloc §1).
- [`scope-envelope-2026-05-28-phase-8.md`](../scope-envelope-2026-05-28-phase-8.md) — Phase-8 run scope envelope.

**Phase-7 inputs (cite-obligation source):**

- [`backfill-notes.md`](../backfill-notes.md) — Phase-7 aggregation matrix; §3.1 (high-confidence cite obligations — Compound-Engineering 4-step loop), §3.2 (medium-confidence TBDs).
- [`backfill-notes/audit-silent-absorption.md`](../backfill-notes/audit-silent-absorption.md) — Phase-7 silent-absorption auditor output (rows 2, 4, 5 touching U-B).
- [`backfill-notes/audit-historian.md`](../backfill-notes/audit-historian.md) — Phase-7 historian auditor output (no U-B assignments).

**ADRs cited (substrate + discipline):**

- Common substrate: [ADR 0010](../../docs/adr/0010-p-01-sandbox-runtime.md), [ADR 0011](../../docs/adr/0011-p-02-cost-ceilings.md), [ADR 0012](../../docs/adr/0012-p-05-trajectory-capture.md), [ADR 0013](../../docs/adr/0013-p-06-watchdog-tiers.md), [ADR 0014](../../docs/adr/0014-p-07-telemetry-ingestor.md), [ADR 0015](../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md), [ADR 0016](../../docs/adr/0016-p-14-judge-router.md), [ADR 0017](../../docs/adr/0017-p-22-polyglot-codebase-index.md), [ADR 0031](../../docs/adr/0031-p-23-dependency-impact-graph.md).
- Framework substrate: [ADR 0029 (P-28 framework)](../../docs/adr/0029-p-28-typed-object-store.md), [ADR 0030 (P-29 framework)](../../docs/adr/0030-p-29-policy-mediator.md).
- U-B per-variant substrate: [ADR 0055 (U-B P-28 layer-typed envelope)](../../docs/adr/0055-p-28-variant-u-b-layer-typed-envelope.md), [ADR 0056 (U-B P-29 layer-boundary policy DSL)](../../docs/adr/0056-p-29-variant-u-b-layer-boundary.md).
- U-B orphan substrate: [ADR 0054 (P-31 cross-layer drift detector)](../../docs/adr/0054-p-31-cross-layer-drift-detector.md).
- Discipline: [ADR 0018](../../docs/adr/0018-discipline-bias-guard.md), [ADR 0019](../../docs/adr/0019-discipline-cognitive-escrow.md), [ADR 0020](../../docs/adr/0020-discipline-cost-ceiling.md), [ADR 0021](../../docs/adr/0021-discipline-holdout.md), [ADR 0022](../../docs/adr/0022-discipline-honesty.md), [ADR 0023](../../docs/adr/0023-discipline-knowledge-promotion.md), [ADR 0024](../../docs/adr/0024-discipline-regime-classification.md), [ADR 0025](../../docs/adr/0025-discipline-scoping.md), [ADR 0026](../../docs/adr/0026-discipline-three-loop.md), [ADR 0027](../../docs/adr/0027-discipline-trifecta-closure.md).

**Archive sources (Phase-7 cite obligation):**

- [`archive/synthesis-v1-v2/13-round-2-synthesis.md`](../../archive/synthesis-v1-v2/13-round-2-synthesis.md) — Compound-Engineering 4-step loop v0.2 canonicalization (high-confidence mandatory cite per Phase-7 aggregation §3.1 finding #2).

**Cross-cutting v3 docs:**

- [`decisions-captured.md`](../decisions-captured.md) — DEC-1.a working hypothesis (U-B IS a unified-attempt and CARRIES the DEC-1.a load), DEC-2 mandate-fit-per-(architecture × work-unit-class).
- [`failure-modes-v3.md`](../failure-modes-v3.md) — F-mode catalog (F2 / F7 / F8 / F9 / F11 / F15 / F19 / F34 / F44 / F46 / F52 / F53 / F58 referenced).
- [`candidate-registry.md`](../candidate-registry.md) — U-B candidate-registry entry.

---

## Subagent self-check results

Self-check items (a)-(g) run on this brief per [`auto-008 §Per-candidate lean-eval brief rubric self-check`](../decisions/auto-008-phase-8-dispatch-shape.md#decision-round-2).

- **(a) `wc -w`**: TBD — recorded at commit time. Heavy tier bounds 5500-7200; this brief targets ~6500.
- **(b) `ls` on cited paths**: PASS at authoring time — all cited v3 file paths verified present (`specs/u-b.md`, `backfill-notes/u-b.md`, `substrate-requirements/u-b.md`, `tracks/unified-B.md`, `sub-tracks/u-b-invariant-authoring.md`, `decisions/auto-008-phase-8-dispatch-shape.md`, `archive/synthesis-v1-v2/13-round-2-synthesis.md`, ADRs 0010-0017 + 0018-0027 + 0029-0031 + 0054-0056, `backfill-notes.md`, `backfill-notes/audit-silent-absorption.md`, `backfill-notes/audit-historian.md`, `lean-evals/gf-m.md`).
- **(c) `grep -cE "^## §[1-8]"`**: PASS — exactly 8 §-headers (§1 through §8).
- **(d) `grep "falsifying-outcome:"` + value ≤80 words**: PASS — YAML field present in frontmatter; field value is **80 words** (at the ≤80-word limit). Load-bearing item; pass means fanout is unblocked.
- **(e) `grep -c "phase-7-cite-obligations:"`**: PASS — YAML field present.
- **(f) Binding-rule-table verbatim text-pull check**: PASS with `n/a` qualifier. This brief quotes short phrases from `specs/u-b.md §3`, `§4`, `§5` verbatim (e.g., "Lethal-Trifecta prohibition on builder-cycle effects per Shapiro R1+R3; substrate-default off per F44"; "L0 standards are seeded from priors... and never start empty") but does NOT cite a multi-row binding rule table verbatim. The candidate's `specs/u-b.md §0` ADR-citation index is referenced by individual ADR markdown links, not as a verbatim multi-row text-pull. Per [auto-008 self-check item (f) `n/a` clause](../decisions/auto-008-phase-8-dispatch-shape.md#decision-round-2): no binding-rule-table verbatim text-pull is invoked.
- **(g) `grep -cE "##? §[1-8]"`**: 8 §-headers from §1 through §8 (same as item c). The "Subagent self-check results" H2 (above this list) is excluded by the `§[1-8]` pattern.

**Unified-attempt-specific check (R6 #1 mandate-partition):** §1 scenario set IS partitioned into a `### Greenfield-mandate scenarios (3)` subsection and a `### Brownfield-mandate scenarios (3)` subsection. YAML `mandate-scenario-split: {greenfield: 3, brownfield: 3}` matches the partition. PASS.
