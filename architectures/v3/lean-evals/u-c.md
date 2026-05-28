---
based-on-spec-commit: c54daf1
based-on-backfill-commit: e66f099
based-on-date: 2026-05-28
candidate-tier: Heavy
candidate-mandate: unified-attempt
scenario-set-source: hybrid
mandate-scenario-split:
  greenfield: 3
  brownfield: 3
expected-evaluator-time-days: 1
falsifying-outcome: |
  Across 3 greenfield + 3 brownfield scenarios run on the same U-C
  substrate stack with identical work-unit-class coverage, the
  dispatcher's regime distribution (counts of {lights-out,
  cross-model-judging, human-required} over cycles logged in
  `solutions/audit/p-19-dispatch/`) diverges between mandate-blocs
  by >40 percentage-points OR the brownfield bloc fails to reach
  ≥80% scenario pass while greenfield does. Mandate is not a
  parameter; it is the organising distinction.
phase-7-cite-obligations:
  high-confidence-mandatory:
    - compound-engineering-4-step-loop-archive-cite
  medium-confidence-design-inputs:
    - audit-silent-absorption.md-§B.1-finding-2-compound-engineering-cells-touching-u-c
    - audit-silent-absorption.md-§B.1-finding-4-typed-envelope-atelier-lineage-tbd
  historian-design-inputs:
    - H-1-stable-ID-lettering-convention-adopted-by-u-c
---

# Lean-eval brief — U-C (Anchor-Distance Factory; Unified-attempt Foundry-primary)

Per [auto-008 §Per-candidate lean-eval brief rubric](../decisions/auto-008-phase-8-dispatch-shape.md#decision-round-2) + R6 partitioned-mandate amendments. U-C is a unified-attempt Heavy-tier candidate (per the [auto-008 tier table](../decisions/auto-008-phase-8-dispatch-shape.md#decision-round-2)). This brief partitions §1 scenarios into a greenfield-mandate bloc (≥3 scenarios) and a brownfield-mandate bloc (≥3 scenarios) per [auto-008 §1 R6 #1 amendment](../decisions/auto-008-phase-8-dispatch-shape.md#round-2-reviewer-amendments-folded-post-round-2-patches); the §3 falsifying-outcome is designed to surface U-C failing to deliver on ONE of its two claimed mandates (not implementation noise on either side).

**U-C adopts the stable-ID lettering convention (H-1) as a Phase-8 design input.** Per the [aggregation §4.1 H-1 finding](../backfill-notes.md#41-load-bearing-gaps-5--phase-8-lean-eval-inputs): the historian flagged H-1 (R/A/F/AE/U/S/K stable-ID lettering per Refinery `00-synthesis.md` §5.5 + `02-compound-atelier.md` §6.1) as the highest-priority load-bearing gap, methodology-layer absorbed only via P-22 + P-24 substrate substitution; one of {U-C, D7-U-1} was invited to adopt explicitly. U-C volunteers: ADR 0059 P-28 anchor envelope already enforces stable-ID discipline at content-hash preimage (immutability-metadata-first contract per [u-c spec §2 P-28 anchor envelope](../specs/u-c.md#2-substrate-composition)); aligning the methodology-layer lettering onto U-C's anchor.kind enum is mechanical. The §1/§6 surface below names how H-1 lands; the lean-eval pressure-tests it via scenarios #2 and #3 (anchor-edit traceability under multi-cycle accumulation).

## §1 Candidate + scenario set

**Candidate.** U-C is the unified-attempt Foundry-primary candidate (Heavy-tier per [auto-008 tier table](../decisions/auto-008-phase-8-dispatch-shape.md#decision-round-2)). Per [`specs/u-c.md §1`](../specs/u-c.md#1-overview): an Anchor-Distance Factory whose load-bearing primitive is distance-from-frozen-anchor — every work unit is parameterised by a single scalar (graph-distance between the proposed change and the nearest frozen anchor). Mandate is a *parameter* (anchor's `kind` field) rather than an organising distinction; greenfield and brownfield work units traverse the **same** dispatcher with the **same** regimes (`near-anchor` / `mid-distance` / `far-anchor`) parameterised by the anchor set's content. Phase-6 exemplar candidate; Phase-7 backfill audit pattern: Foundry > Refinery > Atelier > Tournament in lineage depth.

**Day-0 entry-modes.** Both supported. Greenfield (cold-start, intent-block-only anchor set, L4-by-construction first cycles, lights-out *earned* via anchor accumulation); brownfield (anchor set drawn from existing codebase + observable behaviour + slow-layer invariants — Brier "Architecture" and "Standards" pace-layers + live test suite + runtime telemetry; X_UNM_B Codebase-Model acquisition inherits BF-L's structural P-26 view via P-22 + P-23 per [u-c spec §2 final paragraph](../specs/u-c.md#2-substrate-composition)).

**Mandate-scenario partition (R6 #1).** Unified-attempt obligation: ≥3 greenfield + ≥3 brownfield scenarios. The §3 falsifying-outcome compares the SAME dispatcher's regime distribution across the two blocs — if mandate is genuinely a parameter, the regime-distribution shapes should be reconstructible from anchor-set content (not from mandate label).

**Scenario set source.** Hybrid: scenarios are drawn from (a) the corpus F-mode catalog focused on F37 (silent contradictory-prompt collapse), F47 (Goodhart-on-tokens, U-C's P-32 vulnerability), F8 (multi-month cold-start staleness, U-C §6 carry), F11 (renumbering / stable-ID resilience, the H-1 adoption surface), F13 (missing-config, U-C §11 TBD), F46 (single-model review blindspot), F33/F51 (intent_field_touches LLM-judged residual); and (b) U-C's own scenario-derivation primitives from [`specs/u-c.md §3 step 1-2`](../specs/u-c.md#3-methodology-shape) (work-unit declaration + DistanceTuple computation pipeline). Hybrid because U-C's substrate-heavy thesis means corpus F-modes engage the substrate directly and U-C's distance-derivation primitives engage the dispatcher's regime semantics.

### Greenfield-mandate scenarios (3, ≥3 floor satisfied per R6 #1)

1. **Cold-start trajectory shift across 30 cycles (corpus F8 + candidate-derived §3 decision 2).** Operator authors a single prose intent block (Day-0 frozen anchor); evaluator runs 30 cycles under U-C's L4-by-construction cold-start. Tracks: (i) per-cycle DistanceTuple distribution; (ii) anchor-accumulation rate (live-tests + architecture-rules promoted via pattern→standard); (iii) transition cycle index where ≥X% of work-unit distribution sits at `d ≤ τ_low` for K consecutive cycles (the substrate-mechanical lights-out-trigger). Surfaces: F25 (design starvation framed as L4-cold-start property), F8 (staleness over multi-cycle horizon), F47 (Goodhart drift in distance estimator under accumulating anchors). **Implements DEC-2 work-unit classes `initial-spec` + `mvp`.** Pass: (a) ≥1 work-unit promotes to lights-out by cycle 30 (earned-lights-out claim); (b) Patrol-tier P-06 monitor logs distance-distribution drift events at expected anchor-acquisition boundaries (per [u-c spec §3 step 5](../specs/u-c.md#3-methodology-shape)); (c) DistanceTuple is operator-legible at dispatch (the OQ-5 honesty-discipline gate; see [u-c spec §6 honesty open-carry](../specs/u-c.md#6-open-carries)).

2. **Seeded-contradiction prompt + anchor-edit traceability (corpus F37 + H-1 stable-ID surface).** Evaluator authors 5 seeded contradictions in the intent block (e.g., paired contradictory architecture-rule candidates); P-07 telemetry sets `contradiction_flag = true` per [ADR 0058 decision 3 hard floor](../../docs/adr/0058-p-19-variant-u-c-distance-tuple.md). Each contradiction triggers an `anchor-edit` work unit (always human-required per [u-c spec §3 step 4](../specs/u-c.md#3-methodology-shape)); evaluator validates the AILCCP immutable log + the H-1 stable-ID convention (R/A/F/AE/U/S/K) carries through anchor envelope content-hash preimage. Surfaces: F37 (contradiction catch via hard floor), F11 (renumbering / stable-ID resilience, H-1 adoption surface). Pass: (a) all 5 contradictions catch `contradiction_flag = true` ⇒ `human-required`; (b) AILCCP log entries are content-hash-pinned and reconstruct the full anchor lineage; (c) stable-ID lettering survives 5 anchor-edits without silent renumbering (P-28 ADR 0059's `frozen-since` + `mutation-protocol` participation in content-hash preimage is the substrate-enforcement mechanism).

3. **Goodhart adversarial gaming on `intent_field_touches` leg (corpus F47 + U-C §6 OQ).** Adversarial subagent attempts to author work units that land under `τ_low` while smuggling far-anchor changes — the explicit Phase-8 carry per [u-c spec §6 Goodhart-resistance OQ-1](../specs/u-c.md#6-open-carries). The `intent_field_touches` leg (P-14-routed LLM judge against `symbol → intent-field` map) is the load-bearing F33/F51-vulnerable surface per [ADR 0057 Goodhart resistance](../../docs/adr/0057-p-32-distance-estimator.md). Patrol-tier residual-detector spec (the Phase-5 ADR carry per [u-c spec §6](../specs/u-c.md#6-open-carries)) is the downstream mitigation. **Implements DEC-2 work-unit class `post-mvp-evolution`.** Pass: Patrol-tier P-06 logs ≥4 of 5 adversarial work units as distance-distribution-drift events; the residual-detector flags `intent_field_touches` divergence from `graph_distance` × `pace_layer_crossings` composite (the F47 signal that LLM-judge has drifted from the structural ground truth).

### Brownfield-mandate scenarios (3, ≥3 floor satisfied per R6 #1)

4. **X_UNM_B Codebase-Model acquisition on a real legacy codebase (corpus F40 + candidate-derived §2 final paragraph).** Evaluator provisions a brownfield deployment with a real existing codebase (≥10K LoC polyglot per [P-22 (ADR 0017)](../../docs/adr/0017-p-22-polyglot-codebase-index.md) baseline); operator authors anchor set drawn from observable behaviour + slow-layer invariants per [u-c spec §2 X_UNM_B](../specs/u-c.md#2-substrate-composition). Tests whether: (a) the dependency graph + pace-layer mapping (P-22 + P-23) supports `graph_distance` computation on legacy code; (b) the `intent_field_touches` leg degrades gracefully to operator-attested + L3 dispatch fallback when no synthesised intent block exists (the documented mitigation); (c) the resulting regime distribution is comparable in shape to the greenfield scenario #1 trajectory at equivalent anchor-accumulation depth. Surfaces: F40 (last-mile drift on brownfield), F13 (missing-config — U-C §11 TBD). **Implements DEC-2 work-unit class `initial-spec` (brownfield variant).** Pass: (a) DistanceTuple computes for ≥80% of work units (i.e., the structural + pace-layer legs cover the dependency graph); (b) `intent_field_touches` graceful-degradation surfaces explicitly as an L3 dispatch event in P-05 trajectory (not silent failure); (c) regime distribution shape is within ±40 percentage-points of the greenfield equivalent — the §3 falsifying-outcome's load-bearing threshold.

5. **Regression-fix as near-anchor by construction (corpus F4 + candidate-derived §5 falsifier).** Evaluator authors 5 brownfield regression-fix scenarios where the failing live-test IS the anchor; work units propose minimal-distance fixes (per [u-c spec §5 regression-fix](../specs/u-c.md#5-mandate-fit) — "regression fixes are by construction near-anchor (the failing test IS the anchor; the fix's distance to the test is small)"). Tests: (a) DistanceTuple consistently lands at `d ≤ τ_low` for the 5 fixes; (b) dispatcher routes ≥4 of 5 to lights-out (the regression-fix-as-near-anchor falsifier per [u-c spec §5](../specs/u-c.md#5-mandate-fit)); (c) holdout discipline (ADR 0021) substrate-enforced via P-08 partition. Surfaces: F4 (code quality on regression boundary), F46 (single-model review blindspot — explicitly admissible at near-anchor per Anthropic followup/07 single-family clause). **Implements DEC-2 work-unit class `regression-fix`.** Pass: per criteria (a)-(c); regime distribution skewed strongly to lights-out (the substrate-mechanical regression-fix shape).

6. **Brownfield refactor + Brier pace-layer subsumption pressure-test (corpus F20 + U-C §6 OQ-4).** Evaluator authors 5 brownfield refactor work units targeting architecture-rules (Brier "Architecture" pace-layer) vs standards-rules (Brier "Standards" pace-layer); tests whether anchor-distance correctly subsumes Brier's pace-layers OR is a strictly weaker re-encoding (the explicit Phase-3 adversarial-pass carry per [u-c spec §6 OQ-4](../specs/u-c.md#6-open-carries)). Surfaces: F20 (maintenance asymmetry on brownfield), F46 (cross-model review at mid-distance), brier pace-layer subsumption claim. **Implements DEC-2 work-unit classes `refactor` + `post-mvp-evolution` (brownfield variants).** Pass: (a) `pace_layer_crossings` leg correctly discriminates architecture-rule vs standards-rule mutations (≥4 of 5 correctly classified); (b) regime distribution differs in expected direction between pace-layers (architecture-rule edits route to far-anchor; standards-rule edits route to mid-distance); (c) no work unit routes to lights-out without crossing a pace-layer threshold (the pace-layer-as-substrate-enforced-anchor claim).

**Mandate-scenario partition rationale.** The 6 scenarios cover 4 of 5 U-C work-unit-classes across both mandates (initial-spec greenfield+brownfield via #1+#4; mvp greenfield via #1; regression-fix brownfield via #5; post-mvp-evolution greenfield+brownfield via #3+#6; refactor brownfield via #6). Scenarios are partitioned so that the §3 falsifying-outcome's comparison (regime distribution across mandate-blocs at equivalent anchor-accumulation depth) is mechanical: scenarios #1 vs #4 are matched on work-unit-class (initial-spec). The remaining U-C work-unit-class (refactor greenfield against intent-invariants) is not engaged within the 6-scenario floor; flagged as Phase-8-followup if scenario #6 surfaces a pace-layer-subsumption gap that demands a paired greenfield refactor probe.

**Matched-pair design (load-bearing for §3).** Scenarios #1 (greenfield initial-spec, 30-cycle cold-start) and #4 (brownfield initial-spec, X_UNM_B Codebase-Model acquisition) are deliberately work-unit-class-matched — both target `initial-spec` per U-C's [§5 mandate-fit](../specs/u-c.md#5-mandate-fit) (`initial-spec: brownfield` in YAML, BUT the greenfield form is L4-by-construction per spec §5). U-C's mandate-as-parameter claim predicts: at equivalent anchor-accumulation depth (cycle index N where anchor count is comparable across both blocs), the dispatcher's regime distribution should be reconstructible from anchor-set content alone — i.e., the {lights-out, cross-model-judging, human-required} counts should be within ±40 percentage-points across the two blocs. If mandate is the organising distinction (rather than a parameter), the distribution shapes diverge structurally regardless of anchor-accumulation depth. The §3 falsifier targets exactly this matched-pair divergence.

**Why these 6 and not others (scenario-selection rationale).** U-C's [`specs/u-c.md §6 open-carries`](../specs/u-c.md#6-open-carries) lists 7 open carries: P-32 calibration recipe; F33/F51 Patrol-detector spec; operator-legibility (OQ-5); F8 staleness; Brier pace-layer subsumption (OQ-4); Goodhart adversarial gaming (OQ-1); D-3 challenge. The 6-scenario set engages 5 of the 7 (P-32 calibration via #1's distance distribution; F33/F51 via #3's adversarial probe; operator-legibility via #1's DistanceTuple-at-dispatch test; F8 via #1's 30-cycle horizon; Goodhart via #3; pace-layer subsumption via #6). OQ-2 D-3 challenge is a Phase-3 design-decision question (not a 1-day evaluator-time-bound scenario); not engaged. Scenario selection prioritised: (a) U-C's load-bearing wager (mandate-as-parameter; scenarios #1 vs #4 are the matched-pair test that the §3 falsifier consumes), (b) work-unit-class coverage across both mandates (DEC-2 alignment), and (c) F-mode coverage on U-C's 8-F-mode-invocation surface (F8/F25/F33/F37/F40/F46/F47/F51 — listed in [§4 below](#4-failure-modes-the-test-surfaces)).

## §2 Success criteria

A U-C lean-eval result "passes cleanly" (per [auto-008 §Falsifier discipline R6 #2 partitioned-mandate amendment](../decisions/auto-008-phase-8-dispatch-shape.md#falsifier-discipline-load-bearing) unified-attempt form) iff ALL of:

- **(a′) Partitioned quantitative gate:** ≥80% of greenfield-mandate scenarios pass §1 per-scenario success criteria (i.e., ≥3 of 3 greenfield scenarios pass) AND ≥80% of brownfield-mandate scenarios pass §1 per-scenario success criteria (i.e., ≥3 of 3 brownfield scenarios pass). Mandate-blind ≥80% (≥5 of 6 either-bloc) does NOT suffice for unified-attempts; R6 #2 forbids mandate-bloc masking.
- **(b) Falsifying-outcome gate:** the §3 falsifying-outcome is NOT triggered. This is the load-bearing claim test (mandate-as-parameter; see §3 below).
- **(c) Structural rider (R6 #5):** ≥3 scenarios scored in each mandate-bloc; declaring a mandate-bloc out-of-scope for a unified-attempt is structurally a failure to deliver on the unified-attempt claim per the [auto-008 §canonical escape-hatch enumeration](../decisions/auto-008-phase-8-dispatch-shape.md#r2-2--3-dec-1a-falsifying-pattern-canonical-terms-committed-in-this-brief).

**Per-scenario success criteria (verbatim from §1 above).** Restated for §2-vs-§1 consistency:

1. **Cold-start 30-cycle trajectory.** (a) ≥1 work-unit promotes to lights-out by cycle 30; (b) Patrol-tier P-06 logs distance-distribution drift events at expected anchor-acquisition boundaries; (c) DistanceTuple is operator-legible at dispatch (the OQ-5 honesty test).
2. **Seeded-contradiction + H-1 anchor-edit traceability.** (a) all 5 contradictions catch `contradiction_flag = true` ⇒ `human-required`; (b) AILCCP log entries are content-hash-pinned with reconstructable lineage; (c) stable-ID lettering survives 5 anchor-edits without silent renumbering (H-1 adoption test).
3. **Goodhart adversarial gaming on intent_field_touches.** Patrol-tier P-06 logs ≥4 of 5 adversarial work units as distance-distribution-drift events; residual-detector flags `intent_field_touches` divergence from `graph_distance × pace_layer_crossings` composite.
4. **X_UNM_B Codebase-Model acquisition.** (a) DistanceTuple computes for ≥80% of work units; (b) `intent_field_touches` graceful-degradation surfaces explicitly as L3 dispatch event in P-05 trajectory (not silent failure); (c) regime distribution within ±40 percentage-points of greenfield equivalent.
5. **Regression-fix as near-anchor.** (a) DistanceTuple consistently lands at `d ≤ τ_low` for ≥4 of 5 fixes; (b) dispatcher routes ≥4 of 5 to lights-out; (c) holdout discipline substrate-enforced via P-08 partition (no operator-voluntary holdout).
6. **Brownfield refactor + pace-layer subsumption.** (a) `pace_layer_crossings` correctly discriminates architecture-rule vs standards-rule mutations (≥4 of 5); (b) regime distribution differs in expected direction between pace-layers; (c) no work unit routes to lights-out without crossing a pace-layer threshold.

**Note on success-criteria vs falsifying-outcome distinction (per [auto-008 §Falsifier discipline](../decisions/auto-008-phase-8-dispatch-shape.md#falsifier-discipline-load-bearing)).** Failing any individual per-scenario success criterion can be implementation noise (a P-32 weight miscalibration; a P-22 index inconsistency; an operator misreading DistanceTuple display). Triggering the §3 falsifying-outcome means U-C's **load-bearing unified-attempt wager** — mandate-as-parameter — is empirically wrong: mandate is the organising distinction, not anchor.kind. The unified-attempt claim collapses and U-C reverts to (at best) two parallel mandate-aligned methodologies sharing a substrate, not one methodology.

## §3 Falsifying outcome

**Falsifying-outcome verbatim (≤80 words from YAML, repeated here for §3-vs-YAML consistency per [auto-008 falsification-designer rubric item (iv)](../decisions/auto-008-phase-8-dispatch-shape.md#r2-1-falsification-designer-concreteness-rubric-3-item-mechanical)):**

> Across 3 greenfield + 3 brownfield scenarios run on the same U-C substrate stack with identical work-unit-class coverage, the dispatcher's regime distribution (counts of {lights-out, cross-model-judging, human-required} over cycles logged in `solutions/audit/p-19-dispatch/`) diverges between mandate-blocs by >40 percentage-points OR the brownfield bloc fails to reach ≥80% scenario pass while greenfield does. Mandate is not a parameter; it is the organising distinction.

**Rationale.** U-C's central wager (per [`specs/u-c.md §1 load-bearing claim`](../specs/u-c.md#1-overview) + [u-c track §0](../tracks/unified-C.md)) is that anchor-distance is the substrate's first-class scalar and mandate becomes a *parameter* (the anchor's `kind` field) rather than the organising distinction. The dispatcher routes work units by distance regime; the same dispatcher serves both mandates. If the lean-eval shows the dispatcher's regime distribution diverges fundamentally between greenfield and brownfield blocs at equivalent anchor-accumulation depth (matched-pair scenarios #1 vs #4 are the load-bearing comparison), the unified-attempt claim is empirically wrong: mandate-as-parameter does not hold because the dispatcher's routing depends materially on which mandate the anchor set came from, not on the anchor set's content alone.

**Why this falsifier and not another.** Four alternative falsifiers were considered:

- "If P-32 calibration sweep fails to produce operator-meaningful risk mapping" — this is OQ-1 (an open carry, accepted as RG flag) about a calibration problem downstream of the load-bearing claim. Not the central wager.
- "If F47 Goodhart residual detector cannot be specified" — this is F33/F51-vulnerability of the `intent_field_touches` leg (one of three estimator legs), which U-C explicitly acknowledges as a Phase-5 ADR carry. Not the central wager.
- "If operator-legibility of DistanceTuple at dispatch is opaque" — this is OQ-5 honesty-discipline carve-out. Important but a property of the dispatch-UI surface, not the load-bearing dispatcher claim itself.
- "If anchor-edit traceability under H-1 stable-IDs fails" — this is scenario #2's success-criteria test (H-1 adoption surface). Important but a property of the typed-envelope substrate, not the load-bearing mandate-as-parameter claim.

The mandate-as-parameter claim is U-C's *distinctive* unified-attempt wager — the claim that distinguishes U-C from a hypothetical two-parallel-mandate-methodologies-sharing-a-substrate architecture. The falsifier targets exactly this distinction, and it is structurally tied to the R6 #2 partitioned "pass cleanly" definition: a unified-attempt that fails the partitioned-bloc gate by mandate-bloc asymmetry IS evidence that mandate is the organising distinction. Per [auto-008 §canonical escape-hatch structural rider](../decisions/auto-008-phase-8-dispatch-shape.md#r2-2--3-dec-1a-falsifying-pattern-canonical-terms-committed-in-this-brief): a unified-attempt declaring a mandate-bloc out-of-scope structurally fails the unified-attempt claim — the falsifier's second clause ("brownfield bloc fails to reach ≥80% while greenfield does") catches the silent-out-of-scope-by-failure variant.

**Machine-checkability.** Per [auto-008 falsification-designer rubric 3-item check + R5 #2 item (iv)](../decisions/auto-008-phase-8-dispatch-shape.md#r2-1-falsification-designer-concreteness-rubric-3-item-mechanical):

- **(i) Metric:** dispatcher-regime-distribution counts per mandate-bloc (countable; integer counts of {lights-out, cross-model-judging, human-required} over cycles); divergence as percentage-points between matched-mandate-blocs. AND scenario-pass-rate per mandate-bloc (≥80% gate).
- **(ii) Artifact state:** `solutions/audit/p-19-dispatch/<scenario-id>/<cycle-id>.json` dispatch-decision logs (specific directory, specific filename pattern). Logs are produced by P-19 dispatcher (ADR 0058)'s deterministic decision-table + LLM-judge fallback pipeline + OPA hard-floor post-check; trajectory-replayable per P-05 (ADR 0012).
- **(iii) Threshold:** `>40 percentage-points` regime-distribution divergence OR `brownfield <80%` while `greenfield ≥80%`. Both numeric, both single-direction comparisons.
- **(iv) §3-vs-YAML consistency:** the YAML field and this §3 statement name the same metric (dispatcher-regime-distribution divergence + scenario-pass-rate per mandate-bloc), same artifact location (`solutions/audit/p-19-dispatch/`), same thresholds (>40 percentage-points / brownfield-<80%-while-greenfield-≥80%).

The falsifier passes all 4 rubric items (pass on (iv) mandatory; pass on items (i)-(iii)).

## §4 Failure modes the test surfaces

The 6 scenarios are designed to surface the following failure modes; per [auto-008 §Per-candidate brief §4 rubric](../decisions/auto-008-phase-8-dispatch-shape.md#decision-round-2), each scenario maps to ≥1 F-mode in U-C's spec invocations (per [`u-c spec §3-§4 + §6`](../specs/u-c.md#3-methodology-shape) F-mode references):

- **Scenario #1 cold-start 30-cycle trajectory** surfaces:
  - **F25 (design starvation)** — L4-by-construction cold-start; tests whether earned-lights-out trajectory materializes per [u-c spec §3 distinctive decision 2](../specs/u-c.md#3-methodology-shape).
  - **F8 (multi-month cold-start staleness)** — U-C §6 explicit Phase-8 carry; 30-cycle horizon is the lean-eval-tractable proxy for multi-month.
  - **F47 (Goodhart on tokens)** — Patrol-tier monitor for distance-distribution drift per [u-c spec §3 step 5 + §6](../specs/u-c.md#6-open-carries).
- **Scenario #2 seeded-contradiction + H-1 anchor-edit traceability** surfaces:
  - **F37 (silent contradictory-prompt collapse)** — U-C's hard-floor catch (`contradiction_flag = true ⇒ human-required` per [ADR 0058 decision 3](../../docs/adr/0058-p-19-variant-u-c-distance-tuple.md)).
  - **F11 (renumbering / stable-ID resilience)** — H-1 adoption surface; ADR 0059 `frozen-since` + `mutation-protocol` in content-hash preimage.
- **Scenario #3 Goodhart adversarial gaming on intent_field_touches** surfaces:
  - **F47 (Goodhart on distance estimator)** — U-C's load-bearing P-32 vulnerability per [u-c spec §6 Goodhart-resistance OQ-1](../specs/u-c.md#6-open-carries).
  - **F33/F51 (intent_field_touches residual)** — explicit RG-flag carry per [ADR 0057 Goodhart resistance](../../docs/adr/0057-p-32-distance-estimator.md).
- **Scenario #4 X_UNM_B Codebase-Model acquisition** surfaces:
  - **F40 (last-mile drift on brownfield)** — anchor-set acquisition from legacy code; X_UNM_B cross-mandate inheritance.
  - **F13 (missing-config)** — U-C backfill-notes §11 surfaced-TBD #7; coverage-completeness gap.
- **Scenario #5 regression-fix as near-anchor** surfaces:
  - **F4 (code quality on regression boundary)** — substrate-enforced via P-08 holdout discipline.
  - **F46 (single-model review blindspot)** — near-anchor admits single-family per Anthropic followup/07; the controlled-blindspot test.
- **Scenario #6 brownfield refactor + Brier pace-layer subsumption** surfaces:
  - **F20 (maintenance asymmetry on brownfield)** — pace_layer_crossings as substrate-typed-asymmetry.
  - **F46 (single-model review blindspot)** — cross-model judge at mid-distance via P-14 per [u-c spec §4 bias-guard](../specs/u-c.md#4-discipline-binding).

**F-mode coverage matrix.** For traceability across scenarios:

| F-mode | One-line description | Scenario(s) | U-C spec § |
|---|---|---|---|
| F4 | Code quality on regression boundary | #5 | §4 holdout binding |
| F8 | Multi-month cold-start staleness | #1 | §6 open-carry |
| F11 | Renumbering / stable-ID resilience | #2 | §2 P-28 + ADR 0059 (H-1 adoption surface) |
| F13 | Missing-config | #4 | backfill-notes §11 TBD #7 |
| F20 | Maintenance asymmetry brownfield | #6 | §1 axis (mandate-as-parameter) |
| F25 | Design starvation | #1 | §3 distinctive decision 2 |
| F33/F51 | intent_field_touches LLM-judge residual | #3 | §6 open-carry (Phase-5 ADR seed) |
| F37 | Silent contradictory-prompt collapse | #2 | §3 step 4 hard floors (ADR 0058 decision 3) |
| F40 | Last-mile drift brownfield | #4 | §2 X_UNM_B |
| F46 | Single-model review blindspot | #5 + #6 | §4 bias-guard binding |
| F47 | Goodhart on distance estimator | #1 + #3 | §6 open-carry |

11 F-mode rows; each maps to ≥1 scenario; each cell's spec §-anchor is auditable from `specs/u-c.md`. **Coverage is intentional, not coincidental:** scenarios were designed from U-C's F-mode invocations + open carries, not the reverse. No scenario engages an F-mode U-C's spec does not commit to defending.

**Per-bloc F-mode-coverage symmetry note.** Both mandate-blocs engage substantively distinct F-modes (greenfield bloc: F8, F11, F25, F33/F51, F37, F47; brownfield bloc: F4, F13, F20, F40, F46, F47). The F47 (Goodhart) overlap across blocs is intentional — U-C's P-32 distance estimator is the substrate primitive that serves both mandates, so its Goodhart-vulnerability surfaces on both sides. The §3 falsifying-outcome does NOT predict identical F-mode coverage per bloc; it predicts identical *dispatcher regime distribution* per matched-work-unit-class. The F-mode coverage list above is the per-scenario-design-input enumeration, not the §3 falsification surface.

## §5 Evaluator time + protocol

**Expected evaluator time: 1 day** (per [v1.2 plan § Phase 8 ~1-day-per-candidate bound](../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md#phase-8--lean-eval-design-one-brief-per-candidate-first-pressure-test-surface-revised-in-v12)). U-C as Heavy-tier unified-attempt carries more substrate-stack initialization than Light-tier mandate-aligned candidates; the hour-by-hour breakdown front-loads X_UNM_B setup.

**Hour-by-hour breakdown** (8-hour evaluator-day budget):

| Hour | Phase | Activity | Artifacts produced |
|---|---|---|---|
| 0:00-0:45 | Setup | Initialize substrate stack per [`specs/u-c.md §2`](../specs/u-c.md#2-substrate-composition): P-01 sandbox, P-02 cost ceilings (per-distance parameterised), P-05 trajectory, P-06 Patrol-tier, P-07 telemetry, P-08 substrate-typed holdout, P-12 linter, P-14 judge router, P-22 polyglot index, P-23 dependency-impact graph, P-28 typed-object store (anchor envelope per ADR 0059), P-32 distance estimator (per ADR 0057). | `solutions/setup/substrate-init.log` |
| 0:45-1:30 | Setup | Configure P-32 baseline weights `(w_g, w_p, w_i)` + thresholds `(τ_low, τ_high)` per Phase-5 calibration carry; validate cross-family judge routing reaches ≥3 model families via P-14. | `solutions/setup/p-32-config.json` |
| 1:30-2:30 | Scenario #1 | Cold-start 30-cycle greenfield trajectory: operator-authored intent block; substrate-only execution; Patrol-tier distance-distribution monitoring. | `solutions/audit/p-19-dispatch/sc1-c{01..30}.json`; `solutions/audit/patrol/sc1.json` |
| 2:30-3:00 | Scenario #2 | Greenfield seeded-contradiction + H-1 anchor-edit traceability: 5 paired contradictions; AILCCP immutable log validation. | `solutions/audit/p-19-dispatch/sc2-edit{1..5}.json`; `solutions/audit/ailccp/sc2.json` |
| 3:00-3:45 | Scenario #3 | Greenfield Goodhart adversarial gaming: 5 adversarial work units; Patrol-tier residual-detector logs. | `solutions/audit/p-19-dispatch/sc3-adv{1..5}.json`; `solutions/audit/patrol/sc3-residual.json` |
| 3:45-5:00 | Scenario #4 | Brownfield X_UNM_B Codebase-Model acquisition: ≥10K-LoC polyglot codebase + operator-authored anchor set; P-22 + P-23 acquisition; intent_field_touches graceful-degradation test. | `solutions/audit/p-19-dispatch/sc4-c{01..N}.json`; `solutions/setup/p-22-index.log` |
| 5:00-5:45 | Scenario #5 | Brownfield regression-fix as near-anchor: 5 failing-live-test scenarios; lights-out routing test. | `solutions/audit/p-19-dispatch/sc5-fix{1..5}.json` |
| 5:45-6:45 | Scenario #6 | Brownfield refactor + pace-layer subsumption: 5 architecture-rule + standards-rule refactor work units. | `solutions/audit/p-19-dispatch/sc6-refactor{1..5}.json` |
| 6:45-7:30 | Verdict pass | Compute per-scenario pass/fail against §2; compute §3 falsifying-outcome (regime-distribution divergence between sc1↔sc4 matched pair; scenario-pass-rate per mandate-bloc). | `solutions/lean-eval/verdict-u-c.md` |
| 7:30-8:00 | Reporting | Write verdict-u-c.md with regime-distribution comparison plot, mandate-bloc pass rates, escape-hatch audit, H-1 adoption verdict. | (same file) |

**Protocol invariants** (per [auto-008 §Falsifier discipline escape-hatch enumeration](../decisions/auto-008-phase-8-dispatch-shape.md#r2-2--3-dec-1a-falsifying-pattern-canonical-terms-committed-in-this-brief)):

- **No out-of-mandate scope claim.** U-C is unified-attempt; both mandate-blocs are in-scope by construction. Per the R6 #5 structural rider, declaring a mandate-bloc out-of-scope structurally fails the unified-attempt claim — evaluator may NOT skip the brownfield bloc to preserve the unified-attempt verdict.
- **No scenario-skip mid-run.** All 6 scenarios are executed; partial completion on any scenario is a failure on that scenario, not a skip. Per the R6 #5 structural rider: ≥3 scenarios scored in each mandate-bloc is required; skipping reduces the count and structurally fails the partitioned-bloc gate.
- **No criterion-substitution.** §2 success criteria are committed in this brief; evaluator does NOT re-interpret them mid-run. If §2 is defective, the brief is rewritten not the criterion swapped.

**Substrate ground-truth invariants.** The evaluator records substrate state at end-of-scenario (P-19 dispatch logs + P-05 trajectory + P-28 anchor envelope content-hashes + AILCCP immutable log) so the lean-eval verdict is reconstructable from substrate state alone, not from evaluator memory. The §3 falsifying-outcome's verdict (regime-distribution divergence between matched-mandate-blocs) is reconstructable from `solutions/audit/p-19-dispatch/` alone.

**Anchor-accumulation depth measurement.** The §3 matched-pair comparison requires "equivalent anchor-accumulation depth" — operationally defined as: cycle index N where the brownfield anchor-set size (drawn from existing codebase + observable behaviour + slow-layer invariants at deployment time, then incrementally accumulated) is within ±20% of the greenfield anchor-set size at the same cycle index N. Per [u-c spec §1 entry-mode](../specs/u-c.md#1-overview), brownfield anchor sets begin non-empty (operator-authored at deployment + automated extraction from codebase via P-22 + P-23), while greenfield anchor sets begin minimal (operator-authored intent block only). The matched-pair test therefore measures regime-distribution at the cycle where both blocs have comparable anchor-set sizes — typically cycle 5-10 for the brownfield bloc (anchor set thick at Day-0) vs cycle 20-30 for the greenfield bloc (anchor set accumulates through pattern→standard promotion). The evaluator reports the cycle-index pairs used in the matched-pair comparison; deviation from ±20% size-match triggers a §3 verdict caveat rather than an unconditional falsifier.

**Cost-ceiling considerations.** U-C's per-distance cost ceilings (per [u-c spec §4 cost-ceiling binding](../specs/u-c.md#4-discipline-binding)) parameterise P-02 caps by regime (near-anchor lower; anchor-edit highest). For the lean-eval, evaluator configures ceilings per the [P-32 ADR 0057 calibration baseline](../../docs/adr/0057-p-32-distance-estimator.md) recommendations: near-anchor budget ~$0.20/cycle; mid-distance ~$0.80/cycle; far-anchor + anchor-edit ~$2.50/cycle. Total 8-hour evaluator budget bounded at ~$80 across all 6 scenarios; if ceilings trigger early on scenario #4 (X_UNM_B P-22 index acquisition is the highest-cost scenario at substrate-setup time), evaluator may extend the scenario-#4 ceiling by 1.5× without affecting the §3 verdict (ceilings are implementation-noise, not load-bearing claim).

## §6 Open critique references

U-C's [`specs/u-c.md §6 open carries`](../specs/u-c.md#6-open-carries) lists 7 open critique findings; the lean-eval engages 5 of them directly:

- **P-32 calibration recipe (Phase-5 ADR seed, accepted-with-RG-flag)** → engaged by scenario #1 (30-cycle distance-distribution trajectory) + scenario #4 (X_UNM_B regime-distribution shape). The lean-eval uses Phase-5-calibrated baseline weights `(w_g, w_p, w_i)` + thresholds `(τ_low, τ_high)`; the calibration sweep itself (varying weights + thresholds across the parameter space) is downstream of this lean-eval per [u-c spec §6](../specs/u-c.md#6-open-carries) — the lean-eval pressure-tests the baseline calibration; the sweep characterizes the parameter-space.
- **F33/F51 residual Patrol-detector spec (Phase-5 ADR seed, accepted-with-RG-flag)** → engaged by scenario #3 (Goodhart adversarial gaming on `intent_field_touches`). The lean-eval validates the Patrol-tier residual-detector spec can be operationalized; if scenario #3 fails, the F33/F51 carry escalates as a Phase-5 ADR blocker.
- **Operator-legibility of DistanceTuple at dispatch (Phase-8 lean-eval candidate, biggest single OQ)** → engaged by scenario #1 success-criterion (c). The lean-eval pressure-tests the honesty discipline carve-out per [u-c spec §4 honesty carve-out](../specs/u-c.md#4-discipline-binding); if scenario #1 (c) fails, the OQ-5 carry escalates.
- **F8 staleness over multi-month cold-start (Phase-8 lean-eval candidate)** → engaged by scenario #1 (30-cycle horizon as lean-eval-tractable proxy for multi-month). Full multi-month horizon is downstream of the 1-day lean-eval; flagged as Phase-8-followup if cycle-30 trajectory surfaces stale-anchor signals.
- **Goodhart-resistance under adversarial gaming (Phase-8 lean-eval candidate)** → engaged by scenario #3 (load-bearing adversarial probe). Composite with F33/F51 carry.

The 2 open carries NOT engaged by this lean-eval:

- **Brier pace-layer subsumption (Phase-3 adversarial pass carry — open)** → engaged at the *operational* layer by scenario #6 (pace_layer_crossings discrimination) but NOT at the conceptual layer (does anchor-distance correctly subsume Brier's pace-layers vs strictly weaker re-encoding). The conceptual question is a Phase-3 adversarial-pass back-fill carry per [u-c spec §6 OQ-4](../specs/u-c.md#6-open-carries); the lean-eval's operational probe is sufficient.
- **D-3 challenge (`Agent = Model + Harness + Anchor-Context`)** → not engaged. Phase-3 design-decision question; not a 1-day evaluator-time-bound scenario. Remains a Phase-3 cross-mandate-review carry-forward per [u-c spec §6 D-3 challenge](../specs/u-c.md#6-open-carries).

**Backfill-notes surfaced TBDs.** Per [`backfill-notes/u-c.md §11`](../backfill-notes/u-c.md): 9 surfaced TBDs. Of these, 4 are engaged by the lean-eval: #5 (Tournament scaling — F8 multi-month, engaged via scenario #1), #6 (F8 staleness, scenario #1), #7 (F13 Missing-config, scenario #4), #8 (F14 Attribution collapse — partial via P-05 cycle_id traceability in scenario #2's AILCCP log). The remaining 5 TBDs (#1-#4, #9) are coordination-medium / falsified-consensus / Refinery-5-mode / Foundry-defect-of-origin / parallel-agents-shared-dirs — not 1-day-evaluator-tractable; flagged as Phase-8-followup if scenario #2 (AILCCP log) surfaces an attribution-completeness gap.

## §7 Phase-7 cite obligations honored

Per the [`auto-008` per-candidate cite-obligation mapping table for U-C](../decisions/auto-008-phase-8-dispatch-shape.md#high-confidence-mandatory-cite-obligations-3-cells--n-candidates):

### High-confidence mandatory cite obligation (1 cell)

**Compound-Engineering 4-step loop verbatim cite.** Per [aggregation §3.1 finding #2](../backfill-notes.md#31-high-confidence-findings-3--apply-precedence-rule) + [audit-silent-absorption §B.1 finding #2](../backfill-notes/audit-silent-absorption.md): U-C's `specs/u-c.md §3` describes the Compound Engineering loop as "the default per-cycle methodology" — the phrase "plan → work → review → compound" appears verbatim across 7 specs (U-C among them); only GF-M cites `research/03-every-compound-engineering.md`; **none** cite the archive `02-compound-atelier.md` §1 or `00-synthesis.md` §0 where the 4-step phrasing is canonicalized, and none cite the `13-round-2-synthesis.md` Round-2 archive promotion to load-bearing vocabulary.

**Cite honored in this brief:** U-C's scenario #1 (cold-start trajectory) operates the Compound Engineering 4-step loop per cycle (plan → work → review → compound); per the Phase-7 cite obligation, this brief carries the archive lineage cite verbatim:

> The Compound-Engineering loop `plan → work → review → compound` (referenced in [`specs/u-c.md §3`](../specs/u-c.md#3-methodology-shape)) is v0.2-canonical per [`archive/synthesis-v1-v2/13-round-2-synthesis.md`](../../archive/synthesis-v1-v2/13-round-2-synthesis.md) — the Round-2 archive synthesis that promoted the 4-step shape from `research/03-` (every.to compound engineering) to load-bearing methodology vocabulary. U-C's scenario #1 + scenario #6 cycles iterate the 4-step loop; U-C's [§4 three-loop binding (ADR 0026)](../specs/u-c.md#4-discipline-binding) materialises the "compound" step as Patrol-tier P-06 distance-distribution monitoring (substrate-enforced meta-loop closure, not operator-voluntary).

### Medium-confidence design inputs (consulted)

Per [aggregation §3.2 reconciliation TBDs](../backfill-notes.md#32-medium-confidence-findings-7--trigger-tbd-reconciliation-rows): subagents authoring Wave-8.1 briefs consult [`backfill-notes/audit-silent-absorption.md §B.1`](../backfill-notes/audit-silent-absorption.md) for cells touching their candidate. **U-C's medium-confidence cells (consulted for this lean-eval brief):**

- **§B.1 finding #2** (Compound-Engineering 4-step loop, U-C in the 7-spec set). Covered by the high-confidence cite above. **Engagement:** explicit archive cite in this §7.
- **§B.1 finding #4** (Typed-envelope schemas; U-A / U-B / U-C / D7-U-1 × `02-compound-atelier.md` §3). U-C's ADR 0059 anchor envelope is structurally the Atelier §3.2 YAML-frontmatter knowledge-doc shape lifted to substrate (`kind, content, frozen-since, owning-mandate, mutation-protocol`). Per the medium-confidence `tbd` row, lead-agent adjudicates Atelier-derived vs sufficiently-transformed. **Engagement for this lean-eval:** scenario #2's H-1 stable-ID traceability test exercises the typed-envelope substrate explicitly; if the H-1 adoption succeeds (success-criterion (c) of scenario #2), the Atelier-derived-shape claim is operationally validated independent of the cite-question. The cite-question itself is documentation-layer (whether the Atelier §3 lineage should appear in the U-C spec §2 P-28 cite block); the lean-eval does not require it to land.

### Historian load-bearing design inputs (engaged)

Per [aggregation §4.1 historian load-bearing gaps](../backfill-notes.md#41-load-bearing-gaps-5--phase-8-lean-eval-inputs):

- **H-1 stable-ID lettering convention (R/A/F/AE/U/S/K) — U-C adopts.** Per the [auto-008 cite-obligation propagation table](../decisions/auto-008-phase-8-dispatch-shape.md#historian-load-bearing-design-inputs-5-gaps--n-candidates): one of {U-C, D7-U-1} was invited to adopt H-1 in their lean-eval methodology. **U-C adopts H-1 as a Phase-8 design input** (does not defer to D7-U-1). Rationale: U-C's ADR 0059 P-28 anchor envelope already enforces stable-ID discipline at the substrate level (content-hash preimage including `frozen-since` + `mutation-protocol` makes silent re-dating structurally impossible); aligning the methodology-layer lettering convention (R/A/F/AE/U/S/K) onto U-C's anchor.kind enum (`{intent-invariant, architecture-rule, standards-rule, live-test, runtime-trace, anchor-edit, plus the upstream operator-authored Knowledge-doc kind}`) is mechanical. **Lean-eval surface:** scenario #2 (H-1 anchor-edit traceability) pressure-tests whether the lettering survives 5 anchor-edits without silent renumbering — the Refinery `00-synthesis.md` §5.5 + `02-compound-atelier.md` §6.1 stable-identifier discipline operationalized in U-C's substrate. **Anchor.kind ↔ H-1 mapping:** `architecture-rule ↔ A` (architecture rules); `standards-rule ↔ S` (standards rules); `live-test ↔ F` (frozen / executable fixture); `runtime-trace ↔ U` (runtime-observable / unstructured trace); `anchor-edit ↔ AE` (the AE letter from R/A/F/AE/U/S/K, U-C's structural rider for the anchor-mutation queue); `intent-invariant ↔ R` (root intent, the operator-authored Day-0 anchor); knowledge-doc-style anchor-companion ↔ K. The R/A/F/AE/U/S/K convention maps cleanly onto U-C's anchor.kind enum + the anchor mutation queue's `anchor-edit` envelope; ADR 0059's content-hash preimage IS the substrate-enforcement layer that the methodology-layer lettering relies on. **Adoption rationale (audit-historian §C top recommendation):** the historian's [audit §C `Highest-priority gap`](../backfill-notes/audit-historian.md) names H-1 as "methodologically load-bearing, named in two archive files, only partially absorbed by P-22 + P-24 substrate substitution"; U-C's adoption closes the methodology-layer gap by binding the lettering onto an existing typed-envelope substrate that already enforces the immutability property H-1 depends on. **Phase-8-followup note:** if D7-U-1's lean-eval brief also engages H-1 adoption as a parallel design input (the two candidates were named as alternates per [auto-008 cite-obligation table](../decisions/auto-008-phase-8-dispatch-shape.md#historian-load-bearing-design-inputs-5-gaps--n-candidates)), no conflict — U-C's adoption is via ADR 0059 envelope structure; D7-U-1's would be via its own typed-envelope substrate (ADR 0062 FC envelope). Both adoptions are independent operationalizations of the same methodology-layer convention.

### Cite-obligation summary (YAML `phase-7-cite-obligations` field)

- `high-confidence-mandatory`: 1 cite (Compound-Engineering 4-step loop archive cite).
- `medium-confidence-design-inputs`: 2 §B.1 cells (finding #2 covered by the high-confidence cite; finding #4 typed-envelope Atelier lineage operationally engaged via scenario #2).
- `historian-design-inputs`: 1 (H-1 stable-ID lettering convention; U-C adopts).

## §8 References

**Candidate spec + back-fill notes (primary inputs):**

- [`specs/u-c.md`](../specs/u-c.md) — Phase-6 U-C architecture spec; §0 ADR-citation index, §1 Overview, §2 Substrate composition, §3 Methodology shape, §4 Discipline binding, §5 Mandate fit, §6 Open carries. Phase-6 exemplar.
- [`backfill-notes/u-c.md`](../backfill-notes/u-c.md) — Phase-7 back-fill audit; archive lineage cells for the Compound-Engineering 4-step loop cite obligation; 9 surfaced TBDs + 3 Phase-7 spec-patch candidates.
- [`substrate-requirements/u-c.md`](../substrate-requirements/u-c.md) — Phase-4 substrate-requirements summary; X_UNM_B Codebase-Model acquisition specified.

**Phase-8 dispatch artifacts:**

- [`decisions/auto-008-phase-8-dispatch-shape.md`](../decisions/auto-008-phase-8-dispatch-shape.md) — this brief's parent dispatch decision; §Falsifier discipline (R2 #1-#4 rubric + R6 #1-#5 partitioned-mandate amendments for unified-attempts), §Phase-7 cite-obligation propagation table, §Per-candidate lean-eval brief rubric.
- [`scope-envelope-2026-05-28-phase-8.md`](../scope-envelope-2026-05-28-phase-8.md) — Phase-8 run scope envelope.
- [`lean-evals/gf-m.md`](./gf-m.md) — Phase-8 Wave-8.1 exemplar (lead-agent-authored); section structure + YAML schema + falsifier-discipline pattern.

**Phase-7 inputs (cite-obligation source):**

- [`backfill-notes.md`](../backfill-notes.md) — Phase-7 aggregation matrix; §3.1 (high-confidence cite obligations), §3.2 (medium-confidence TBDs), §4.1 (historian load-bearing gaps).
- [`backfill-notes/audit-silent-absorption.md`](../backfill-notes/audit-silent-absorption.md) — Phase-7 silent-absorption auditor output; §B.1 finding #2 (Compound-Engineering 4-step loop; U-C among 7 specs), finding #4 (typed-envelope Atelier lineage; U-C among 4 specs).
- [`backfill-notes/audit-historian.md`](../backfill-notes/audit-historian.md) — Phase-7 historian auditor output; H-1 stable-ID lettering convention (U-C adopts).

**ADRs cited (substrate + discipline):**

- Common substrate: [ADR 0010](../../docs/adr/0010-p-01-sandbox-runtime.md), [ADR 0011](../../docs/adr/0011-p-02-cost-ceilings.md), [ADR 0012](../../docs/adr/0012-p-05-trajectory-capture.md), [ADR 0013](../../docs/adr/0013-p-06-watchdog-tiers.md), [ADR 0014](../../docs/adr/0014-p-07-telemetry-ingestor.md), [ADR 0015](../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md), [ADR 0016](../../docs/adr/0016-p-14-judge-router.md), [ADR 0017](../../docs/adr/0017-p-22-polyglot-codebase-index.md).
- Framework + per-variant: [ADR 0028 (P-19 framework)](../../docs/adr/0028-p-19-eligibility-regime-classifier.md) + [ADR 0058 (U-C P-19 distance-tuple variant)](../../docs/adr/0058-p-19-variant-u-c-distance-tuple.md); [ADR 0029 (P-28 framework)](../../docs/adr/0029-p-28-typed-object-store.md) + [ADR 0059 (U-C P-28 anchor envelope variant)](../../docs/adr/0059-p-28-variant-u-c-anchor-envelope.md).
- Orphan substrate: [ADR 0057 (P-32 distance estimator)](../../docs/adr/0057-p-32-distance-estimator.md).
- Designed-system: [ADR 0031 (P-23 dependency-impact graph)](../../docs/adr/0031-p-23-dependency-impact-graph.md), [ADR 0032 (P-12 deterministic linter)](../../docs/adr/0032-p-12-deterministic-linter-framework.md).
- Discipline: [ADR 0018](../../docs/adr/0018-discipline-bias-guard.md), [ADR 0019](../../docs/adr/0019-discipline-cognitive-escrow.md), [ADR 0020](../../docs/adr/0020-discipline-cost-ceiling.md), [ADR 0021](../../docs/adr/0021-discipline-holdout.md), [ADR 0022](../../docs/adr/0022-discipline-honesty.md), [ADR 0023](../../docs/adr/0023-discipline-knowledge-promotion.md), [ADR 0024](../../docs/adr/0024-discipline-regime-classification.md), [ADR 0025](../../docs/adr/0025-discipline-scoping.md), [ADR 0026](../../docs/adr/0026-discipline-three-loop.md), [ADR 0027](../../docs/adr/0027-discipline-trifecta-closure.md).

**Archive sources (Phase-7 cite obligation):**

- [`archive/synthesis-v1-v2/13-round-2-synthesis.md`](../../archive/synthesis-v1-v2/13-round-2-synthesis.md) — Compound-Engineering 4-step loop v0.2 canonicalization (high-confidence mandatory cite per Phase-7 aggregation §3.1 finding #2).
- [`archive/synthesis-v1-v2/00-synthesis.md`](../../archive/synthesis-v1-v2/00-synthesis.md) §5.5 — stable-identifier discipline (H-1 source, adopted by U-C).
- [`archive/architectures-v2/01-specification-refinery.md`](../../archive/architectures-v2/01-specification-refinery.md) §6.1 — stable-identifier discipline (H-1 source, paired with `00-synthesis.md` §5.5).
- [`archive/architectures-v2/02-compound-atelier.md`](../../archive/architectures-v2/02-compound-atelier.md) §3 — typed-envelope artifact stack (silent-absorption finding #4; operationally engaged via scenario #2).

**Cross-cutting v3 docs:**

- [`decisions-captured.md`](../decisions-captured.md) — DEC-1.a unified-attempt working hypothesis (U-C carries the DEC-1.a load); DEC-2 mandate-fit-per-(architecture × work-unit-class).
- [`failure-modes-v3.md`](../failure-modes-v3.md) — F-mode catalog (F4, F8, F11, F13, F20, F25, F33, F37, F40, F46, F47, F51 referenced).
- [`candidate-registry.md`](../candidate-registry.md#u-c--anchor-distance-factory) — U-C candidate-registry entry.
- [`tracks/unified-C.md`](../tracks/unified-C.md) — original Phase-3 track sketch; OQ-1 / OQ-4 / OQ-5 source.
