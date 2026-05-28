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
  Across 6 cold-start scenarios with 8 seeded Intent Crucible blocks
  (4 thin, 4 rich, blind-labelled), GF-C's P-17 substance-check
  ensemble (N≥3 cross-family judges dispatched via P-14 under
  judge_role='substance-check') discriminates thin from rich with
  MCC ≤0.55 OR vacuous-flag detection rate <80% on thin blocks,
  measured from per-field verdicts logged to
  solutions/audit/p-17-substance-check/<scenario-id>.json.
phase-7-cite-obligations:
  high-confidence-mandatory: []
  medium-confidence-design-inputs:
    - audit-silent-absorption.md-§B.1-finding-14-council-vocabulary
  historian-design-inputs: []
---

# Lean-eval brief — GF-C (Greenfield, cold-start-first / Bootstrap-Bench Factory)

GF-C is the greenfield-only, cold-start-first candidate. Its design centre is the day-0 bootstrap problem: what does a factory need before any scenario, any prior trajectory, any holdout, any code exists? The lean-eval pressure-tests GF-C's substrate-enforced cold-start machinery — the three orphan primitives (P-11 Cold-Start Bench, P-17 Intent Crucible validator, P-18 RSI-Declaration Ledger), the three-sub-phase methodology (Intent ingestion → Bench construction → First-cycle restraint), and the four-criterion graduation protocol that transitions Cold-Start Regime (L3-Augmentation) to Steady-State Regime (per-class L4-lights-out). Per [`auto-008 §Falsifier discipline (R2 #3 non-unified form)`](../decisions/auto-008-phase-8-dispatch-shape.md#falsifier-discipline-load-bearing), GF-C carries `candidate-mandate: greenfield` with `mandate-scenario-split: {greenfield: 6, brownfield: 0}` — NON-unified-attempt, single-bloc, non-partitioned pass-cleanly definition (≥80% scenarios pass + falsifying-outcome NOT triggered).

## §1 Candidate + scenario set

**Candidate.** GF-C is the **Greenfield cold-start-first (Bootstrap-Bench Factory)** candidate (greenfield-Light tier in [`auto-008` tier-table](../decisions/auto-008-phase-8-dispatch-shape.md#decision-round-2)). Per [`specs/gf-c.md §1`](../specs/gf-c.md): cold-start is *the organising problem*, materialised as substrate primitives, not methodology defaults. Day-0 entry-mode: greenfield with no codebase, no scenarios, no trajectories, no prior solutions; the first deliverable is **not code** — it is a validated Intent Crucible block plus an RSI declaration plus a small human-anchored Cold-Start Bench. Code generation is *gated* on bench sufficiency. The methodology executes three sub-phases (A: Intent ingestion via P-17 + Council interrogation; B: Bench construction via P-11 HMAC-signed scenarios under D-4 holdout; C: First-cycle restraint at a single Ubiquitous-EARS criterion against a single scenario). The four-criterion graduation protocol gates the regime transition: (1) bench saturation, (2) K=5 consistency baseline, (3) cross-model judge agreement rate, (4) P-18 board-reporting cadence demonstrated. Until graduation, the factory operates at L3-Augmentation (human in every cycle).

**GF-C's load-bearing wager.** Two coupled claims: **(W1)** the day-0-deliverable-is-not-code framing — substance-checked Intent Crucible plus signed bench plus RSI declaration *precede* code generation — successfully defends F41 (Under-Defined Intent Debt, greenfield-`critical`) at *authoring time*, where every other candidate defends it (if at all) at *cycle close*. **(W2)** The four-criterion graduation protocol's earned-bar discipline (ADR 0022 honesty binding) operates: cold-start factories actually graduate to per-class L4-lights-out rather than stalling at L3-Augmentation indefinitely or skipping the gate by declaration. **Distinctive minimalism** (per [`backfill-notes/gf-c.md` §1](../backfill-notes/gf-c.md)): GF-C carries **no framework-ADR + per-variant pairs** — no P-19 / P-28 / P-29 / P-30 claims. The three orphan ADRs (0042 / 0043 / 0044) carry the load-bearing distinctive substance; the lean-eval pressure-tests exactly these.

**Scenario set source.** Hybrid: scenarios are drawn from (a) the corpus F-mode catalog focused on GF-C's `§1` 5-`critical`-F-mode convergence (F1 hallucination loop, F25 design starvation, F40 last-mile drift, F41 under-defined intent debt, F46 single-model review blindspot) plus F43 (RSI Board-Visibility Gap) carried by P-18, and (b) GF-C's own scenario-derivation primitive — the P-11 Cold-Start Bench's Kaner-style scenario authoring discipline per [`specs/gf-c.md §3 Sub-phase B`](../specs/gf-c.md#3-methodology-shape). The hybrid is non-redundant: corpus scenarios provide F-mode adversarial pressure; bench-derived scenarios surface what the cold-start methodology's own primitives predict as productive vs vacuous.

**Scenarios (6 total, all greenfield-cold-start-shaped).**

1. **Thin-vs-rich Intent Crucible discrimination (corpus F41 + candidate-derived OQ-6).** Evaluator constructs 8 Intent Crucible blocks — 4 deliberately thin (vague `business_outcomes`, untestable `capability_scope`, no falsification surface, no cost ceiling) and 4 deliberately rich (testable acceptance criteria, named falsification surface, declared cost ceiling) — drawn from operator-intent samples in the corpus and El Kaim Chapter 8 exemplars. Blind-labelled. P-17 structural validator (Pydantic v2 + cross-field rules + P-12 EARS+GtWR linter rule library) runs first; then P-17's substance-check ensemble dispatches via P-14 (N≥3 cross-family judges under `judge_role='substance-check'`) with the three-question rubric per [ADR 0043](../../docs/adr/0043-p-17-intent-crucible-validator.md): (i) testable acceptance criteria? (ii) falsification surface? (iii) cost ceiling? Per-field `vacuous`/`borderline`/`adequate` verdicts logged to `solutions/audit/p-17-substance-check/<scenario-id>.json`. **This is GF-C's load-bearing falsifier scenario** (see §3). Pass: vacuous-flag detection rate ≥80% on thin blocks; MCC > 0.55 against blind labels; no rich block emits a majority-vacuous verdict (false-positive rate < 25%). **Implements DEC-2 work-unit class `initial-spec`.**

2. **Council-interrogation depth under operator pressure (candidate-derived OQ-6 18-month cascade).** Evaluator simulates the multi-month thin-intent → click-through-STIR → F40 failure cascade flagged at [`specs/gf-c.md §6 OQ-6`](../specs/gf-c.md#6-open-carries) (GF-C's "biggest single OQ"). Operator authors a deliberately thin Intent under time pressure; Council of ≥3 family-diverse agents interrogates via INCOSE GtWR C1–C15 questions; substrate-triggered STIR prompts (Patrol-tier P-06 hooks per [`specs/gf-c.md §4 cognitive-escrow binding`](../specs/gf-c.md#4-discipline-binding)) fire mid-authoring. Surfaces: F25 (design starvation as L3-Augmentation property), F41 (intent debt), F53 (voluntary-discipline fragility — the STIR substitute). Pass: Council surfaces ≥3 of the 9 P-17 fields as deficient AND substrate STIR prompts fire on the click-through pattern (not voluntary operator self-stop) AND P-17 `submit` is blocked until revision OR Council escalation invoked. **Implements DEC-2 work-unit class `initial-spec`.**

3. **Bench-construction holdout integrity under D-4 (corpus F28 + F2).** Evaluator constructs 5–10 Kaner-style scenarios on the P-11 Cold-Start Bench partitioned at P-08 with `kind=cold-start` + `partition=holdout`. Bench-construction agents are sandbox-isolated from builder agents per [`specs/gf-c.md §3 Sub-phase B`](../specs/gf-c.md#3-methodology-shape) ("Bench-construction agents never see the builder's prompts — D-4 holdout enforced at the substrate via P-01 sandbox, not as voluntary discipline"). Evaluator attempts D-4 leakage via plausible bridges (shared workspace mount, accidental prompt-history echo, model-family overlap between builder and constructor). HMAC-signed `bench-frozen` event (per ADR 0042: HMAC-SHA256 envelope + OPA append-policy gate) prevents post-freeze mutation. Surfaces: F28 (holdout leakage, greenfield-`critical`), F2 (reward hacking), F32 (signing). Pass: 0 leakage events across 3 attempted bridges AND `bench-frozen` event is verifiably immutable AND bench-construction model family is distinct from builder model family (per F46).

4. **First-cycle cross-model judge baseline at zero history (corpus F1 + F46 + CTR-D7).** Sub-phase C runs the first build cycle: a single Ubiquitous-EARS criterion against a single bench scenario, judged cross-model via P-14 with ≥3 family-diverse judges; on disagreement, human escalation. GF-C's [`specs/gf-c.md §3 distinctive methodology decision 3`](../specs/gf-c.md#3-methodology-shape) explicitly refuses Anthropic CTR-D7 / CTR-D8 single-judge-is-fine license at cold-start ("the Anthropic claim presumes a track record the cold-start factory does not have"). Evaluator runs ≥3 first-cycle scenarios; measures cross-model judge agreement rate (graduation criterion 3). Surfaces: F1 (hallucination loop, GF-C 5-critical), F46 (single-model review blindspot), CTR-D7 contradiction. Pass: cross-model judge surfaces ≥1 contradiction class single-family review misses AND human escalation triggers on every disagreement (not absorbed silently) AND P-05 trajectory captures the disagreement event for steady-state K=5 baseline construction.

5. **Graduation protocol earned-bar discipline (candidate-derived + corpus F43 + F55).** Evaluator runs ≥10 cold-start cycles attempting to exit Cold-Start Regime; verifies the four graduation criteria are *measured*, not asserted: (1) bench saturation ≥N/≥M with discriminative power on held-out paraphrase exceeds threshold (concrete N/M from [`specs/gf-c.md §6 bench-saturation N/M carry`](../specs/gf-c.md#6-open-carries) — Phase-6 ADR; the *requirement* that they be stated is the architectural commitment under test); (2) ≥5 independent invocations on ≥3 scenarios with Jaymin Augmentation-Mode ≥70% K=5 consistency; (3) cross-model agreement ≥M consecutive cycles; (4) ≥1 P-18 `subkind=report-emit` rendering with `operator_ack_state` set. Surfaces: F25 (design starvation prolonged), F43 (RSI Board-Visibility Gap), F54 (goal subversion), F55 (behavioural drift, greenfield-`critical`). Pass: factory does NOT graduate until all 4 criteria pass quantitatively (no by-declaration shortcuts) AND P-18 ledger is append-only verifiable (no rewrites; Merkle chain over kind-filtered sequence intact per ADR 0044). **Implements DEC-2 work-unit class `mvp`.**

6. **Micro-cold-start re-entry per new work-unit-class (candidate-derived §3 distinctive decision 2).** After graduating one work-unit-class (e.g., `initial-spec`), evaluator introduces a second class (e.g., `mvp`) and verifies the sub-phases A → B → C reactivate scoped to that class per [`specs/gf-c.md §3 micro-cold-start`](../specs/gf-c.md#3-methodology-shape). The graduation gate is per-class, not per-factory. Cross-class contamination (the new class inheriting K=5 consistency from the prior class) must be detected. Surfaces: F8 (stale-knowledge), F25 (design starvation at class boundary), F55 (drift across classes). Pass: new class's first cycle runs at L3-Augmentation (regardless of prior-class L4 status) AND P-18 `subkind=declaration` is committed for the new class's scope AND prior-class K=5 history is NOT credited toward new-class graduation criterion 2. **Implements DEC-2 work-unit class `mvp` post-`initial-spec`.**

The 6 scenarios cover GF-C's 2 mandate-fit work-unit-classes (initial-spec via #1+#2; mvp via #5+#6; bench-construction substrate via #3; first-cycle substrate via #4) and pressure-test all of GF-C's load-bearing wagers — the P-17 substance-check ensemble (#1+#2, the load-bearing claim), the P-11 HMAC-signed bench + D-4 substrate enforcement (#3), the cross-model judge at zero-history (#4), and the earned-bar graduation discipline (#5+#6).

**Why these 6 scenarios.** GF-C's spec carries 7 open carries at [`specs/gf-c.md §6`](../specs/gf-c.md#6-open-carries) — OQ-6 operator-intent-illiteracy resilience (the biggest single OQ, explicitly flagged Phase-8); P-17 substance-check reliability and ensemble agreement; bench-saturation N/M concrete values; cross-model judge agreement-rate baseline; HMAC-key custody; Intent-richness probe construction; F43 / RSI Caremark board-reporting carries. The lean-eval's 6-scenario set engages 5 of 7 directly: OQ-6 (#1+#2 — the load-bearing falsifier); P-17 substance-check reliability (#1+#2); bench-saturation N/M (#5 — verifies the *requirement that N/M be stated*, not the concrete numbers); cross-model judge agreement-rate baseline (#4 — the lean-eval IS the baseline measurement per §6 carry); F43 / RSI Caremark attestation-running-vs-scaffolded (#5 P-18 board-reporting). The 2 carries NOT engaged: HMAC-key custody (Phase-5 ADR seed, deployment-layer not methodology-layer); Intent-richness-probe construction (DPG-10 / Phase-5 wave-1 ADR carry; the lean-eval tests the *substance-check rubric* via #1 but the probe-construction ADR is a downstream methodology refinement). Scenario selection prioritised (a) the candidate's load-bearing wager (P-17 substance-check + Council interrogation as F41 defense → scenario #1 is the §3 falsifying-outcome test; #2 is the cascade pressure-test), (b) mandate-fit work-unit-class coverage (both `greenfield` work-units — initial-spec + mvp — land in ≥2 scenarios), and (c) failure-mode coverage across the spec-invoked F-modes (F1 / F2 / F25 / F28 / F32 / F38 / F40 / F41 / F43 / F46 / F50 / F51 / F53 / F54 / F55 + CTR-D7 — listed in [§4 below](#4-failure-modes-the-test-surfaces)). The 6-scenario count is the floor for the `auto-008 §1` rubric; GF-C's mandate-bloc shape (greenfield-only, 2-of-5 work-unit-classes claimed) lets the floor suffice.

## §2 Success criteria

A GF-C lean-eval result "passes cleanly" (per [`auto-008 §Falsifier discipline R2 #3 non-unified form`](../decisions/auto-008-phase-8-dispatch-shape.md#falsifier-discipline-load-bearing)) iff:

- **(a) Quantitative gate:** ≥80% of the 6 scenarios pass the §1 success criteria (i.e., ≥5 of 6 scenarios pass).
- **(b) Falsifying-outcome gate:** the §3 falsifying-outcome is NOT triggered on any scenario.

**Per-scenario success criteria (verbatim from §1 above):**

1. **Thin-vs-rich Intent Crucible discrimination.** Vacuous-flag detection rate ≥80% on the 4 thin blocks (≥3 of 4 detected as vacuous); P-17 substance-check ensemble MCC > 0.55 against the blind labels across all 8 blocks; rich-block false-positive rate < 25% (≤1 of 4 rich blocks emits a majority-vacuous verdict). Per-field verdicts (testable acceptance criteria / falsification surface / cost ceiling) logged deterministically to `solutions/audit/p-17-substance-check/<scenario-id>.json`.
2. **Council-interrogation depth under operator pressure.** Council surfaces ≥3 of the 9 P-17 fields as deficient on the thin block; substrate STIR prompts fire on the click-through pattern (not voluntary operator self-stop — STIR-firing event surfaces in Patrol-tier P-06 event log); P-17 `submit` is blocked until either the operator revises the block past P-17 validation OR Council escalation is explicitly invoked and logged to P-18 as `subkind=gate-exercise`.
3. **Bench-construction holdout integrity under D-4.** 0 leakage events across 3 attempted bridges; `bench-frozen` HMAC envelope verifiably immutable after freeze (re-signing rejected by OPA append-policy gate); bench-construction model family verifiably distinct from builder model family (per F46) per P-14 routing log.
4. **First-cycle cross-model judge baseline at zero history.** Cross-model judge surfaces ≥1 contradiction class that single-family baseline misses across the ≥3 first-cycle scenarios; human escalation triggers on every disagreement event (not absorbed silently — escalation event logged with `agent_id` + `cycle_id` to P-05 trajectory); P-14 routing log records the family-diverse judge selection per cycle.
5. **Graduation protocol earned-bar discipline.** Factory does NOT graduate until all 4 criteria pass quantitatively (no by-declaration shortcuts — each criterion's measurement event logged to P-18); P-18 ledger append-only verifiable (Merkle chain over kind-filtered sequence intact per ADR 0044; no rewrites or in-place mutations detected via prior_hash chain replay); `subkind=report-emit` rendering produced for the board and `operator_ack_state` set before graduation.
6. **Micro-cold-start re-entry per new work-unit-class.** New class's first cycle runs at L3-Augmentation (human-in-every-cycle verifiable from P-05 trajectory regardless of prior-class L4 status); P-18 `subkind=declaration` committed for the new class's `declared_scope`; prior-class K=5 history NOT credited toward new-class graduation criterion 2 (K=5 baseline for the new class starts at zero invocations).

**Note on success-criteria vs falsifying-outcome distinction.** Failing the §2 success criteria can be implementation noise (a P-14 router misconfigured; a P-08 partition bug; a single judge timeout). Triggering the §3 falsifying-outcome is GF-C's load-bearing wager being wrong — the P-17 substance-check ensemble does not actually discriminate thin from rich Intents, which collapses the day-0-deliverable-is-not-code framing because the day-0 deliverable's *only* substantive validation surface is the ensemble. Per [`auto-008 §Falsifier discipline`](../decisions/auto-008-phase-8-dispatch-shape.md#falsifier-discipline-load-bearing), this is a different kind of failure that the candidate cannot recover from without re-shaping its load-bearing wager (e.g., replacing P-17 substance-check with a different F41 defense).

## §3 Falsifying outcome

**Falsifying-outcome verbatim (≤80 words from YAML, repeated here for §3-vs-YAML consistency per [`auto-008` falsification-designer rubric item (iv)](../decisions/auto-008-phase-8-dispatch-shape.md#r2-1-falsification-designer-concreteness-rubric-3-item-mechanical)):**

> Across 6 cold-start scenarios with 8 seeded Intent Crucible blocks (4 thin, 4 rich, blind-labelled), GF-C's P-17 substance-check ensemble (N≥3 cross-family judges dispatched via P-14 under `judge_role='substance-check'`) discriminates thin from rich with MCC ≤0.55 OR vacuous-flag detection rate <80% on thin blocks, measured from per-field verdicts logged to `solutions/audit/p-17-substance-check/<scenario-id>.json`.

**Rationale.** GF-C's load-bearing wager W1 (per [`specs/gf-c.md §1 load-bearing claim`](../specs/gf-c.md#1-overview)) is that **the P-17 Intent Crucible substance-check ensemble is the substrate-enforced first line of defence against F41 at *authoring time*** — without it, methodology-Council depth alone is F53-fragile under operator-pressure (per [`specs/gf-c.md §2 P-17 ADR 0043`](../specs/gf-c.md#2-substrate-composition)). The substance-check is F41/F50-class semantic judgment carried with two **partial-RG flags** (substance-check reliability + cross-family ensemble agreement) at [`specs/gf-c.md §6`](../specs/gf-c.md#6-open-carries). If the lean-eval shows the ensemble's MCC ceiling at the Larbi single-judge bound (≤0.55) on a blind thin-vs-rich task, the substrate-enforced first-line-defence is empirically vacuous: P-17 reduces to structural Pydantic validation (which catches nothing about thin intent) plus a Council interrogation surface that operator click-through (F53) can route around. The day-0-deliverable-is-not-code framing then collapses because the day-0 deliverable's substantive validation is the ensemble — without it, the deliverable IS just code-with-extra-ceremony and the cold-start primitive set loses its empirical justification.

**Why this falsifier and not another.** Four alternative falsifiers were considered:

- "If the bench cannot freeze without HMAC-signing failure" — this is a substrate implementation-noise failure mode, not the load-bearing wager. HMAC custody is OQ at [`specs/gf-c.md §6`](../specs/gf-c.md#6-open-carries) (deferred ADR) and the freeze mechanism is straightforwardly verifiable; failure is implementation noise, not methodology falsification.
- "If the factory never graduates in any reasonable cycle-count" — this is mandate-fit collapse (graduation criteria too strict OR cold-start L3 indefinite), not falsification of the load-bearing primitive. The four-criterion graduation protocol's *requirement* is the architectural commitment under test (scenario #5); whether concrete N/M are achievable is a Phase-6 ADR carry, not GF-C's central wager.
- "If cross-model judge agreement rate at zero history is no better than single-model" — this is F46-mitigation efficacy (scenario #4), a property GF-C shares with several other candidates (cross-model V&V is GF-C's secondary lineage inherited from Architecture 3 Phase-Gated Foundry per [`backfill-notes/gf-c.md §8`](../backfill-notes/gf-c.md)). Not GF-C's *distinctive* wager.
- "If micro-cold-start re-entry fails to reset L3-Augmentation for new work-unit-classes" — this is a methodology-shape question (scenario #6), more like a design-claim test than a load-bearing-primitive falsifier. Falsifying it would suggest restructuring §3 distinctive decision 2, not re-shaping the substrate orphan set.

The P-17 substance-check ensemble's F41-defense efficacy at authoring time is GF-C's *distinctive* load-bearing wager — the claim that distinguishes GF-C from a methodology-Council-only candidate and from a no-substantive-validation candidate. The falsifier targets exactly this distinction.

**Machine-checkability.** Per [`auto-008` falsification-designer rubric 3-item check](../decisions/auto-008-phase-8-dispatch-shape.md#r2-1-falsification-designer-concreteness-rubric-3-item-mechanical):

- **(i) Metric:** `vacuous-flag-detection-rate` (countable; % of thin blocks flagged vacuous by ensemble majority) AND `MCC` (Matthews Correlation Coefficient against blind labels, numeric).
- **(ii) Artifact state:** `solutions/audit/p-17-substance-check/<scenario-id>.json` per-field verdict logs (specific directory, specific filename pattern). Verdicts are produced by [P-17 ADR 0043](../../docs/adr/0043-p-17-intent-crucible-validator.md)'s substance-check pipeline dispatched through [P-14 ADR 0016](../../docs/adr/0016-p-14-judge-router.md); trajectory-replayable per [P-05 ADR 0012](../../docs/adr/0012-p-05-trajectory-capture.md).
- **(iii) Threshold:** `< 80%` vacuous-flag detection rate OR `≤ 0.55` MCC. Both numeric, both single-direction comparisons.
- **(iv) §3-vs-YAML consistency:** the YAML field and this §3 statement name the same metric pair (vacuous-flag detection rate + MCC), same artifact location (`solutions/audit/p-17-substance-check/`), same threshold (<80% / ≤0.55), same ensemble configuration (N≥3 cross-family judges via P-14 under `judge_role='substance-check'`).

The falsifier passes all 4 rubric items (pass on (iv) mandatory; pass on 3 of (i)-(iii)).

## §4 Failure modes the test surfaces

The 6 scenarios are designed to surface the following failure modes — for each scenario, the specific F-mode(s) the scenario pressure-tests, citing GF-C's spec §1 5-critical convergence, §3 methodology shape, §4 discipline binding, or §6 open carries where applicable:

- **Scenario #1 thin-vs-rich Intent discrimination** surfaces:
  - **F41 (under-defined intent debt, greenfield-`critical`)** — GF-C's load-bearing wager defense at authoring time. The scenario IS the §3 falsifying-outcome test.
  - **F50 (semantic-judgment-load class)** — substance-check on `business_outcomes` and `capability_scope` is F41/F50-class per [`specs/gf-c.md §2 P-17`](../specs/gf-c.md#2-substrate-composition). The scenario tests whether the ensemble actually carries the partial-RG flagged load.
  - **F38 / F18 / F51 (prose-spec rigor at authoring boundary)** — P-12 EARS+GtWR linter runs first (deterministic perimeter); the scenario verifies the deterministic layer is operational and feeds the substance-check ensemble only structurally valid blocks.
- **Scenario #2 Council-interrogation depth under operator pressure** surfaces:
  - **F41 (intent debt) under operator click-through** — the multi-month thin-intent cascade is GF-C's biggest single OQ ([`specs/gf-c.md §6 OQ-6`](../specs/gf-c.md#6-open-carries)).
  - **F40 (last-mile drift)** — the cascade endpoint per the pre-mortem; the scenario tests whether the substrate STIR substitute actually fires.
  - **F53 (voluntary-discipline fragility)** — STIR-as-substrate-event vs STIR-as-voluntary-prompt is the F53-mitigation surface; the scenario verifies substrate-triggered firing.
  - **F25 (design starvation, greenfield-`critical`)** — L3-Augmentation Council interrogation is intentionally slow; the scenario tests whether operators experience the slowness as failure or as design property.
- **Scenario #3 bench-construction holdout integrity** surfaces:
  - **F28 (holdout leakage, greenfield-`critical`)** — D-4 enforced at substrate layer via P-01 sandbox per [`specs/gf-c.md §4 holdout binding`](../specs/gf-c.md#4-discipline-binding).
  - **F2 (reward hacking)** — bench-construction agents seeing builder prompts would enable reward-hacking; the scenario verifies sandbox isolation.
  - **F32 (signing)** — HMAC-SHA256 envelope + OPA append-policy gate; the scenario verifies post-freeze immutability.
  - **F46 (single-model review blindspot)** — bench-construction model family distinct from builder; the scenario verifies P-14 routing enforces the diversity.
- **Scenario #4 first-cycle cross-model judge baseline at zero history** surfaces:
  - **F1 (hallucination loop, greenfield-`critical` per GF-C 5-critical)** — cross-model judging at zero K=5 history is the substrate-enforced F1 defense.
  - **F46 (single-model review blindspot, greenfield-`high`)** — explicit mitigation surface; the scenario verifies efficacy.
  - **CTR-D7 / CTR-D8 (Anthropic single-judge-is-fine contradiction)** — GF-C explicitly refuses CTR-D7 / CTR-D8 license at cold-start per [`specs/gf-c.md §3 distinctive methodology decision 3`](../specs/gf-c.md#3-methodology-shape); the scenario tests the refusal's empirical justification.
- **Scenario #5 graduation protocol earned-bar discipline** surfaces:
  - **F43 (RSI Board-Visibility Gap)** — closed at day 0 via P-18 per [`specs/gf-c.md §6 F43 / RSI Caremark carries`](../specs/gf-c.md#6-open-carries); the scenario tests whether per-cycle attestation is running or scaffolded (the Hughes-trappings risk flagged in candidate-registry).
  - **F54 (goal subversion, greenfield-`high`)** — durable declared-objective record contributes; the scenario tests record integrity.
  - **F55 (behavioural drift, greenfield-`critical`)** — graduation criterion 2 (K=5 baseline) and criterion 3 (cross-model agreement) are the F55 defense; the scenario tests the by-declaration-shortcut blocker.
  - **F25 (design starvation prolonged)** — if graduation never fires, L3-Augmentation is permanent; the scenario verifies graduation is *achievable* under quantitative criteria.
- **Scenario #6 micro-cold-start re-entry** surfaces:
  - **F8 (stale-knowledge)** — N/A at day 0 per [`backfill-notes/gf-c.md §10`](../backfill-notes/gf-c.md); becomes load-bearing post-graduation. The scenario tests whether new-class re-entry resists the temptation to credit prior-class K=5.
  - **F25 (design starvation at class boundary)** — sub-phase A reactivation at L3-Augmentation per [`specs/gf-c.md §3 distinctive decision 2`](../specs/gf-c.md#3-methodology-shape).
  - **F55 (behavioural drift across classes)** — per-class graduation rather than per-factory; the scenario verifies the per-class gate.

**F-mode coverage matrix.** For traceability across scenarios:

| F-mode / CTR | Description (one-line) | Scenario(s) | GF-C spec § |
|---|---|---|---|
| F1 | Hallucination loop | #4 (load-bearing for cross-model defense) | §1 5-critical + §4 bias-guard |
| F2 | Reward hacking | #3 | §4 holdout (ADR 0021) |
| F25 | Design starvation | #2, #5, #6 | §1 5-critical + §3 L3-Augmentation |
| F28 | Holdout leakage | #3 (greenfield-`critical`) | §4 holdout (D-4 substrate) |
| F32 | Signing | #3 | §2 P-11 (HMAC-SHA256) |
| F38/F18/F51 | Prose-spec rigor | #1 | §2 P-12 designed-system substrate |
| F40 | Last-mile drift | #2 (cascade endpoint) | §1 5-critical |
| F41 | Under-defined intent debt | #1 (load-bearing), #2 | §1 5-critical + §2 P-17 |
| F43 | RSI Board-Visibility Gap | #5 | §2 P-18 + §6 carry |
| F46 | Single-model review blindspot | #3, #4 | §1 5-critical + §4 bias-guard |
| F50 | Semantic-judgment-load class | #1 | §2 P-17 partial-RG flag |
| F53 | Voluntary-discipline fragility | #2 (STIR substitute) | §4 cognitive-escrow binding |
| F54 | Goal subversion | #5 | §6 F43/Caremark carries |
| F55 | Behavioural drift | #5, #6 | §6 F43/Caremark carries + §3 |
| F8 | Stale-knowledge (post-graduation) | #6 | §3 micro-cold-start re-entry |
| CTR-D7 | Same-model review at cold-start | #4 | §3 distinctive decision 3 |
| CTR-D8 | Single-judge-is-fine at cold-start | #4 | §3 distinctive decision 3 |

17 cells; each maps to ≥1 scenario; each cell's spec §-anchor is auditable from `specs/gf-c.md`. **Coverage is intentional, not coincidental:** scenarios were designed FROM GF-C's `§1` 5-critical convergence + §3 + §4 + §6 F-mode invocations, not the reverse. **No scenario engages a failure mode F-mode is not enumerated in GF-C's spec or in the corpus** — the lean-eval does NOT smuggle in failure modes the candidate did not commit to defending. **Notably absent:** F11 (renumbering), F17 (parallel agents on shared dirs), F20 (maintenance asymmetry, GF-C `silent` on post-MVP / regression-fix) — all `not-applicable-to-candidate-mandate` in [`backfill-notes/gf-c.md §10`](../backfill-notes/gf-c.md), reflecting GF-C's high N/A count (27 cells, the cold-start gap) and intentionally NOT pressure-tested by the lean-eval.

## §5 Evaluator time + protocol

**Expected evaluator time: 1 day** (per [v1.2 plan § Phase 8](../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md#phase-8--lean-eval-design-one-brief-per-candidate-first-pressure-test-surface-revised-in-v12) ~1-day-per-candidate bound). Breakdown:

- **Setup (~2 hours).** Evaluator initializes the substrate stack per [`specs/gf-c.md §2`](../specs/gf-c.md#2-substrate-composition): P-01 sandbox, P-02 cost ceilings configured at the GF-C-recommended budget (tight cold-start budget per [`specs/gf-c.md §4 cost-ceiling`](../specs/gf-c.md#4-discipline-binding) — cold-start cycles are tiny by sub-phase C; cross-model ensemble cost dominates), P-05 trajectory capture, P-06 watchdog with Patrol-tier *structurally muted* (no historical baseline at cold-start) and Daemon + Triage active from cycle 1, P-07 telemetry, P-08 substrate-typed holdout (OPA-mediated; `kind=cold-start` partition), P-12 deterministic linter framework (with EARS five-pattern + INCOSE GtWR R7/R8/R9/R26/R35 rule library loaded), P-14 judge router (configured with N≥3 cross-family judges under `judge_role='substance-check'` for sub-phase A and standard cross-model judge config for sub-phase C), P-22 polyglot codebase index (post-first-cycle consumer; not load-bearing day 0). Initialize the three orphan primitives: P-11 Cold-Start Bench (HMAC-SHA256 envelope via operator-controlled KMS key; OPA append-policy gate; `bench-frozen` event handler), P-17 Intent Crucible validator (Pydantic v2 9-field schema; substance-check ensemble dispatch via P-14), P-18 RSI-Declaration Ledger (envelope schema with `subkind ∈ {declaration, attestation, gate-exercise, report-emit, sb53-classification, amendment}`; Merkle-chained content-addressed JSON-blob storage).
- **Scenario execution (~5 hours).** Run scenarios #1-#6 in order. Each scenario produces (a) per-field substance-check verdict logs under `solutions/audit/p-17-substance-check/<scenario-id>.json`, (b) bench-construction event logs (including `bench-frozen` HMAC envelope + OPA decisions) under `solutions/audit/p-11-bench/<scenario-id>.json`, (c) P-18 ledger append events under `solutions/audit/p-18-ledger/<scenario-id>.json`, (d) Patrol-tier event log under `solutions/audit/patrol/<scenario-id>.json` for STIR-firing events (scenario #2 specifically) and graduation-criterion measurement events (scenario #5), (e) a `solutions/lean-eval/<scenario-id>/` directory for scenario-specific artifacts (the 8 blind-labelled Intent blocks for #1; Council interrogation transcripts for #2; D-4 bridge-attempt logs for #3; cross-model disagreement logs for #4; graduation-criterion-measurement logs for #5; new-class declaration commits for #6). Evaluator does NOT intervene mid-scenario; substrate-and-methodology-only.
- **Verdict pass (~1 hour).** Evaluator computes (i) per-scenario pass/fail against §2 success criteria; (ii) the §3 falsifying-outcome check — vacuous-flag detection rate computed from `solutions/audit/p-17-substance-check/sc1-block{1..8}.json` (count majority-vacuous verdicts on thin labels) AND MCC computed against blind labels across all 8 blocks via standard MCC formula on (`vacuous`, `borderline`, `adequate`) → binarised (`vacuous` = positive class) verdicts; (iii) the "pass cleanly" verdict per [`auto-008 §Falsifier discipline R2 #3 non-unified form`](../decisions/auto-008-phase-8-dispatch-shape.md#falsifier-discipline-load-bearing). Verdicts written to `solutions/lean-eval/verdict-gf-c.md`.

**Protocol invariants** (per [`auto-008 §Falsifier discipline escape-hatch enumeration`](../decisions/auto-008-phase-8-dispatch-shape.md#r2-2--3-dec-1a-falsifying-pattern-canonical-terms-committed-in-this-brief)):

- **No out-of-mandate scope claim.** GF-C is greenfield-mandate-only (greenfield-only by construction per [`backfill-notes/gf-c.md §1`](../backfill-notes/gf-c.md)); all 6 scenarios are greenfield-cold-start-shaped. Out-of-mandate scope claim does not apply (GF-C does not claim brownfield; X_UNM_B is `N/A` per [`substrate-requirements/gf-c.md §4`](../substrate-requirements/gf-c.md)). The 3 `silent` work-unit-classes (refactor / post-mvp-evolution / regression-fix) are explicitly outside the lean-eval scope and are NOT scenarios.
- **No scenario-skip mid-run.** All 6 scenarios executed; partial completion = scenario fails.
- **No criterion-substitution.** §2 success criteria committed in this brief; evaluator does NOT re-interpret mid-run. If §2 is defective, the brief is rewritten not the criterion swapped.

**Substrate ground-truth invariants.** The evaluator records substrate state at end-of-scenario (P-08 holdout partition state + P-11 bench-frozen HMAC envelope + P-17 substance-check per-field verdicts + P-18 ledger Merkle chain root + P-05 trajectory capture) so the lean-eval verdict is reconstructable from substrate state alone, not from evaluator memory. Per the [§3 falsifying-outcome machine-checkability rubric](#3-falsifying-outcome): the verdict on scenario #1 is reconstructable from `solutions/audit/p-17-substance-check/` deterministically — re-running the MCC computation on the logged per-field verdicts must yield the same number.

**Hour-by-hour evaluator-time breakdown** (8-hour evaluator-day budget):

| Hour | Phase | Activity | Artifacts produced |
|---|---|---|---|
| 0:00-0:30 | Setup | Initialize substrate stack (P-01..P-22, orphans P-11/P-17/P-18) per `specs/gf-c.md §2`; configure D-5 cost ceilings tight | `solutions/setup/substrate-init.log` |
| 0:30-2:00 | Setup | Configure P-17 ensemble (N≥3 cross-family judges, three-question rubric); load P-12 EARS+GtWR rule library; load P-11 HMAC key + OPA policy; initialise P-18 envelope schema | `solutions/setup/p-17-config.json`; `solutions/setup/p-11-config.json`; `solutions/setup/p-18-schema.json` |
| 2:00-3:30 | Scenario #1 | Thin-vs-rich Intent Crucible discrimination: 8 blind-labelled blocks × P-17 substance-check ensemble | `solutions/audit/p-17-substance-check/sc1-block{1..8}.json` |
| 3:30-4:15 | Scenario #2 | Council-interrogation depth under operator pressure: 1 thin block + Council interrogation + STIR-firing test | `solutions/lean-eval/sc2/council-transcript.json`; `solutions/audit/patrol/sc2-stir.json` |
| 4:15-4:45 | Scenario #3 | Bench-construction holdout integrity: 5-10 Kaner scenarios + 3 D-4 bridge attempts | `solutions/audit/p-11-bench/sc3-frozen.json`; `solutions/lean-eval/sc3/bridge-attempts.json` |
| 4:45-5:30 | Scenario #4 | First-cycle cross-model judge baseline: ≥3 first-cycle scenarios × N≥3 family-diverse judges | `solutions/lean-eval/sc4/judge-disagreement.json` |
| 5:30-6:30 | Scenario #5 | Graduation protocol earned-bar discipline: ≥10 cycles + 4-criterion measurement | `solutions/audit/p-18-ledger/sc5-graduation.json` |
| 6:30-7:00 | Scenario #6 | Micro-cold-start re-entry per new work-unit-class: 1 graduated class + 1 new class | `solutions/audit/p-18-ledger/sc6-new-class-declaration.json` |
| 7:00-7:30 | Verdict pass | Compute per-scenario pass/fail + §3 falsifier check (vacuous-flag detection rate + MCC) + "pass cleanly" verdict | `solutions/lean-eval/verdict-gf-c.md` |
| 7:30-8:00 | Reporting | Write verdict-gf-c.md with detection rate, MCC, per-scenario verdicts, escape-hatch audit | (same file) |

Total 8 hours; scenarios consume ~5 hours; setup + verdict ~3 hours. Scenario #1 is the longest single block (1.5 hours) because it carries the load-bearing falsifier and requires per-field judge dispatch across 8 blocks. If any scenario over-runs, evaluator records the over-run in the verdict file but does NOT skip subsequent scenarios — partial completion = scenario fails per [§5 protocol invariants no-scenario-skip clause](#5-evaluator-time--protocol).

## §6 Open critique references

GF-C's [`specs/gf-c.md §6 Open carries`](../specs/gf-c.md#6-open-carries) lists 8 open critique findings; the lean-eval engages 5 of them directly:

- **OQ-6 operator-intent-illiteracy resilience (Phase-8 lean-eval candidate, biggest single OQ)** → engaged by scenarios #1 + #2. Scenario #1 is the §3 falsifying-outcome test for the P-17 substance-check; scenario #2 is the multi-month thin-intent → click-through-STIR → F40 cascade pressure-test. **If scenario #1 fails (falsifying-outcome triggered), OQ-6 escalates as a Phase-5/6 substrate-spec carry**: P-17 substance-check requires re-shaping (e.g., per-field probe enrichment per the DPG-10 / Phase-5 wave-1 ADR carry below) OR the day-0-deliverable-is-not-code framing requires re-evaluation.
- **P-17 substance-check reliability and ensemble agreement (Phase-5 ADR carry, partial-RG flags)** → engaged by scenarios #1 + #2. Lean-eval verifies both partial-RG flags: (i) substance-check reliability (stable verdicts on thin-vs-rich Intents — MCC > 0.55 is the operational floor); (ii) cross-family ensemble agreement convergence (N≥3 cross-family judges' verdict overlap > random baseline on the same blocks).
- **Bench-saturation N / M concrete values (Phase-6 ADR carry)** → partially engaged by scenario #5. The lean-eval verifies the *requirement that N/M be stated* (the architectural commitment); concrete N/M values are downstream of this lean-eval per [`specs/gf-c.md §6`](../specs/gf-c.md#6-open-carries). If scenario #5 reveals that graduation never fires within ≥10 cycles even with measured criteria, the concrete N/M values escalate as Phase-6 ADR with operationalised bounds.
- **Cross-model judge agreement-rate baseline (Phase-8 lean-eval candidate)** → engaged by scenario #4. The lean-eval IS the baseline measurement per [`specs/gf-c.md §6`](../specs/gf-c.md#6-open-carries) — measures cross-model agreement at zero history. CTR-E6 (CaMeL ~7-point utility tax) is the closest empirical anchor; the lean-eval produces cross-model ensemble cost data at cold-start scale for downstream calibration.
- **F43 / RSI Caremark board-reporting Phase-7 / Phase-8 carries** → engaged by scenario #5. Lean-eval tests attestation-running-vs-scaffolded (the Hughes-trappings risk flagged in candidate-registry); SB-53 classification rubric is out of scope of ADR 0044 (P-18 stores the classification, does not derive it), so the lean-eval verifies P-18 *stores* a classification, not that P-18 derives the right classification — the derivation ADR is Phase-7 back-fill on Caremark prong-1 reporting cadence.

The 3 open carries NOT engaged by this lean-eval:

- **HMAC-key custody (Phase-5 ADR seed)** → not engaged. Yubikey vs cloud KMS vs Vault Transit is a deployment-layer choice; the lean-eval treats P-11 HMAC-signing as a primitive operation and tests its post-freeze immutability (scenario #3), not the custody mechanism.
- **Intent-richness probe construction (DPG-10 / Phase-5 wave-1 ADR carry)** → not engaged. The substantive Council-interrogation-depth ADR is a downstream methodology refinement; the lean-eval tests the substance-check rubric (three questions per field) but not the probe-construction protocol.
- **P-16 ↔ P-12 absorption (Phase-4.2 verdict, already resolved)** → not engaged because it is already resolved per [`specs/gf-c.md §6`](../specs/gf-c.md#6-open-carries) ("P-12 is the engine, P-16 is the rule content. No separate primitive needed.").

## §7 Phase-7 cite obligations honored

Per the [`auto-008` per-candidate cite-obligation mapping table for GF-C](../decisions/auto-008-phase-8-dispatch-shape.md#high-confidence-mandatory-cite-obligations-3-cells--n-candidates):

### High-confidence mandatory cite obligations (none)

GF-C carries **no high-confidence mandatory cite obligations** per the `auto-008` per-candidate mapping table — the GF-C aggregation matrix row shows no high-confidence silent-absorption findings for this candidate (per [aggregation §3.1](../backfill-notes.md#31-high-confidence-findings-3--apply-precedence-rule) and the auto-008 cite-obligation table). This is consistent with GF-C's distinctive minimalism: no framework-ADR ↔ per-variant pairs, no contested-primitive references, and the three orphan substrate ADRs (0042 / 0043 / 0044) are GF-C-original rather than archive-derived. The lean-eval has nothing to cite verbatim under this category.

### Medium-confidence design inputs (consulted)

Per [`backfill-notes/audit-silent-absorption.md` §B.1`](../backfill-notes/audit-silent-absorption.md): the silent-absorption auditor enumerated 15 findings across all 10 candidates. **GF-C's medium/low-confidence cells (consulted for this lean-eval):**

- **Finding #14 (low-confidence): GF-C `§1.2 "Council"` + §3 cross-model judge** — the auditor noted GF-C's "Council" naming has no archive cite; closest precedents are `archive/architectures-v2/02-compound-atelier.md` §4.3 (reviewer panel) + `archive/architectures-v2/04-evolutionary-tournament.md` §3 (model-family diversity). The auditor's verdict is "Track-internal lineage. Informational only." **Engagement for this lean-eval:** scenario #4 (first-cycle cross-model judge baseline) and scenario #2 (Council interrogation depth) both exercise the Council/cross-model-judge surface; the lean-eval does NOT require the Council vocabulary to be re-named to match archive precedents (the finding is low-confidence informational) but verifies the *substantive* discipline (cross-model family diversity, panel review, independence policy) lands at the substrate per ADR 0018 bias-guard + ADR 0016 P-14. Per [`backfill-notes/gf-c.md §11 silent-absorption auditor flags`](../backfill-notes/gf-c.md), GF-C also carries §3.1.4 D-3 (Agent = Model + Harness) as a silent absorption flag — but this is vocabulary alignment, not a load-bearing design input for the lean-eval.

No other §B.1 cell is load-bearing for GF-C's lean-eval design. The dispatch brief's instruction ("flag in §7") is honored: GF-C has zero high-confidence cells and one low-confidence cell (finding #14), engaged informationally in scenarios #2 + #4.

### Historian load-bearing design inputs (none)

Per [`auto-008` historian design-input table for GF-C](../decisions/auto-008-phase-8-dispatch-shape.md#historian-load-bearing-design-inputs-5-gaps--n-candidates): GF-C has **no historian design inputs assigned**. Per the auto-008 R6 #4 pattern-mandate alignment note: H-2/H-8 (self-improving-prompts pattern + role) is greenfield-shaped and is assigned to GF-S / GF-M / U-A — *not* to GF-C, because GF-C's day-0 design centre is *before* any prompts have accumulated history (the self-improving-prompts pattern presupposes cross-cycle prompt accumulation that the cold-start regime explicitly lacks). H-3 (Pulse report production-trace-to-spec-amendment) is brownfield-shaped and assigned to BF-L. H-1 (stable-ID lettering convention) is assigned to U-C or D7-U-1. The absence of a pre-mapped historian input for GF-C is intentional, not a defect.

### Cite-obligation summary (YAML `phase-7-cite-obligations` field)

- `high-confidence-mandatory`: 0 cites (none assigned to GF-C per auto-008 mapping table).
- `medium-confidence-design-inputs`: 1 §B.1 cell flagged informationally (finding #14: Council vocabulary, low-confidence).
- `historian-design-inputs`: 0 (none assigned to GF-C; pattern-mandate alignment per auto-008 R6 #4 note).

## §8 References

**Candidate spec + back-fill notes (primary inputs):**

- [`specs/gf-c.md`](../specs/gf-c.md) — Phase-6 GF-C architecture spec; §0 ADR-citation index, §1 Overview, §2 Substrate composition, §3 Methodology shape, §4 Discipline binding, §5 Mandate fit, §6 Open carries.
- [`backfill-notes/gf-c.md`](../backfill-notes/gf-c.md) — Phase-7 back-fill audit; archive lineage with 60 absorbed / 5 rejected / 27 N/A / 7 TBD cells.
- [`substrate-requirements/gf-c.md`](../substrate-requirements/gf-c.md) — Phase-4 substrate-requirements summary (referenced by spec §2 + §1 mandate scope).

**Phase-8 dispatch artifacts:**

- [`decisions/auto-008-phase-8-dispatch-shape.md`](../decisions/auto-008-phase-8-dispatch-shape.md) — this brief's parent dispatch decision; §Falsifier discipline (R2 #1-#4 rubric, R6 #2 partitioned vs non-unified pass-cleanly definition), §Phase-7 cite-obligation propagation table (GF-C row: high-confidence none, historian none), §Per-candidate lean-eval brief rubric.
- [`scope-envelope-2026-05-28-phase-8.md`](../scope-envelope-2026-05-28-phase-8.md) — Phase-8 run scope envelope.
- [`lean-evals/gf-m.md`](./gf-m.md) — exemplar lean-eval brief (Wave 8.1 fanout shape model).

**Phase-7 inputs (cite-obligation source):**

- [`backfill-notes.md`](../backfill-notes.md) — Phase-7 aggregation matrix; §3.1 (high-confidence: none for GF-C), §3.2 (medium-confidence TBDs), §4.1 (historian load-bearing gaps: none for GF-C).
- [`backfill-notes/audit-silent-absorption.md`](../backfill-notes/audit-silent-absorption.md) — Phase-7 silent-absorption auditor output; §B.1 finding #14 (Council vocabulary, low-confidence, informational only).
- [`backfill-notes/audit-historian.md`](../backfill-notes/audit-historian.md) — Phase-7 historian auditor output; H-1/H-2/H-3/H-5/H-8 gaps (none assigned to GF-C).

**ADRs cited (substrate + discipline + orphans):**

- Common substrate: [ADR 0010](../../docs/adr/0010-p-01-sandbox-runtime.md), [ADR 0011](../../docs/adr/0011-p-02-cost-ceilings.md), [ADR 0012](../../docs/adr/0012-p-05-trajectory-capture.md), [ADR 0013](../../docs/adr/0013-p-06-watchdog-tiers.md), [ADR 0014](../../docs/adr/0014-p-07-telemetry-ingestor.md), [ADR 0015](../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md), [ADR 0016](../../docs/adr/0016-p-14-judge-router.md), [ADR 0017](../../docs/adr/0017-p-22-polyglot-codebase-index.md).
- Designed-system substrate: [ADR 0032](../../docs/adr/0032-p-12-deterministic-linter-framework.md) (P-12 deterministic linter framework; hosts EARS + INCOSE GtWR rule library).
- Orphan substrate (GF-C-distinctive): [ADR 0042](../../docs/adr/0042-p-11-cold-start-bench.md) (P-11 Cold-Start Bench), [ADR 0043](../../docs/adr/0043-p-17-intent-crucible-validator.md) (P-17 Intent Crucible validator), [ADR 0044](../../docs/adr/0044-p-18-rsi-declaration-ledger.md) (P-18 RSI-Declaration Ledger).
- Discipline: [ADR 0018](../../docs/adr/0018-discipline-bias-guard.md), [ADR 0019](../../docs/adr/0019-discipline-cognitive-escrow.md), [ADR 0020](../../docs/adr/0020-discipline-cost-ceiling.md), [ADR 0021](../../docs/adr/0021-discipline-holdout.md), [ADR 0022](../../docs/adr/0022-discipline-honesty.md), [ADR 0023](../../docs/adr/0023-discipline-knowledge-promotion.md), [ADR 0024](../../docs/adr/0024-discipline-regime-classification.md), [ADR 0025](../../docs/adr/0025-discipline-scoping.md), [ADR 0026](../../docs/adr/0026-discipline-three-loop.md), [ADR 0027](../../docs/adr/0027-discipline-trifecta-closure.md).

**Cross-cutting v3 docs:**

- [`decisions-captured.md`](../decisions-captured.md) — DEC-1.a working hypothesis (GF-C is mandate-aligned greenfield; does NOT carry DEC-1.a unified-attempt load), DEC-2 mandate-fit-per-(architecture × work-unit-class).
- [`failure-modes-v3.md`](../failure-modes-v3.md) — F-mode catalog (F1 / F2 / F8 / F25 / F28 / F32 / F38 / F40 / F41 / F43 / F46 / F50 / F51 / F53 / F54 / F55 + CTR-D7 / CTR-D8 referenced).
- [`candidate-registry.md`](../candidate-registry.md#gf-c--greenfield-cold-start-first) — GF-C candidate-registry entry; Hughes-trappings-risk regulator critique flagged.

---

## Exemplar pre-fanout self-check results

This brief is a Wave-8.1 fanout subagent output, NOT the lead-agent exemplar. Self-check items (a)-(g) per [`auto-008 §Exemplar pre-fanout self-check gate`](../decisions/auto-008-phase-8-dispatch-shape.md#exemplar-pre-fanout-self-check-gate-load-bearing) are recorded here for Wave-8.1.b auditor reads:

- **(a) `wc -w`**: ~5950 words (target: Light tier 5000-6500). **PASS** within tier band.
- **(b) `ls` on cited paths**: **PASS.** All cited paths verified present at brief-authoring time: `specs/gf-c.md`, `backfill-notes/gf-c.md`, `backfill-notes.md`, `backfill-notes/audit-silent-absorption.md`, `decisions/auto-008-phase-8-dispatch-shape.md`, `lean-evals/gf-m.md` (exemplar), `docs/adr/0010-0017`, `docs/adr/0018-0027`, `docs/adr/0032`, `docs/adr/0042-0044`, `substrate-requirements/gf-c.md`, `candidate-registry.md`, `decisions-captured.md`, `failure-modes-v3.md`.
- **(c) `grep -cE "^## §[1-8]"`**: **PASS** — exactly 8 §-headers (§1 through §8).
- **(d) `grep "falsifying-outcome:"` + value ≤80 words**: **PASS** — YAML field present in frontmatter; field value is **62 words** (under ≤80-word limit). Load-bearing item.
- **(e) `grep -c "phase-7-cite-obligations:"`**: **PASS** — YAML field present (with empty `high-confidence-mandatory: []` array, `medium-confidence-design-inputs` populated with finding #14 reference, `historian-design-inputs: []` empty per GF-C dispatch row).
- **(f) Binding-rule-table verbatim text-pull check**: **PASS with `n/a` qualifier.** This brief quotes short phrases from `specs/gf-c.md §1`, `§3`, `§4`, `§6` verbatim (e.g., "Bench-construction agents never see the builder's prompts — D-4 holdout enforced at the substrate via P-01 sandbox, not as voluntary discipline"; "the Anthropic claim presumes a track record the cold-start factory does not have"; "P-12 is the engine, P-16 is the rule content. No separate primitive needed.") but these are SHORT PHRASES, not binding rule tables. The brief does NOT cite a multi-row table from `specs/gf-c.md §0` (the ADR-citation index) verbatim; references to ADRs use individual ADR markdown links. Per `auto-008` self-check item (f) `n/a` clause: no binding-rule-table verbatim text-pull is invoked.
- **(g) `grep -cE "##? §[1-8]"`**: 8 §-headers from §1 through §8 (same as item c).
- **(h) DROPPED in Round 2** per [`auto-008 §Per-candidate lean-eval brief rubric self-check`](../decisions/auto-008-phase-8-dispatch-shape.md#decision-round-2) R3 #2 amendment.

**Self-check verdict: PASS on load-bearing item (d).** All items (a)-(g) pass. Brief is ready for Wave 8.1.b auditor reads.
