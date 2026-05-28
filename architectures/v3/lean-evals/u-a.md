---
based-on-spec-commit: 00ae134
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
  Across 6 partitioned scenarios (3 greenfield bootstrap + 3 brownfield
  archaeology), U-A's Compound-Knowledge Atelier promotes zero
  methodology-delta intervals to typed `solutions/` envelopes
  (`docs/solutions/` directory state at scenario close, counted via the
  ADR-0051 envelope's `kind: methodology-delta` content-hash records)
  on EITHER the greenfield bloc OR the brownfield bloc. Equivalently:
  promotion-rate per bloc ≤0 entries per ≥3 cycles.
phase-7-cite-obligations:
  high-confidence-mandatory:
    - knowledge-promotion-4-token-enum-archive-cite
    - compound-engineering-4-step-loop-archive-cite
    - 4-architecture-taxonomy-archive-cite
  medium-confidence-design-inputs:
    - audit-silent-absorption.md-§B.1-finding-4-typed-envelope-Atelier-lineage
  historian-design-inputs:
    - H-2-self-improving-prompts-pattern
    - H-8-prompt-self-improver-role
---

# Lean-eval brief — U-A (Escrow-Graph Factory)

This brief is the Phase-8 Wave-8.1 per-candidate lean-eval for U-A — one of the 4 unified-attempt candidates carrying the DEC-1.a falsification load per [auto-008 §Falsifier discipline R6 #2](../decisions/auto-008-phase-8-dispatch-shape.md#r2-2--3-dec-1a-falsifying-pattern-canonical-terms-committed-in-this-brief). U-A claims BOTH greenfield and brownfield mandates by parameterising the typed-node-graph substrate via `kind` distribution and `policies` slot contents on the `EscrowInterval` envelope; the brief's §1 scenario set is partitioned per [auto-008 R6 #1](../decisions/auto-008-phase-8-dispatch-shape.md#round-2-reviewer-amendments-folded-post-round-2-patches) into a `### Greenfield-mandate scenarios` subsection (≥3) and a `### Brownfield-mandate scenarios` subsection (≥3); the "pass cleanly" verdict uses the unified-attempt partitioned form (per [auto-008 R6 #2](../decisions/auto-008-phase-8-dispatch-shape.md#r2-2--3-dec-1a-falsifying-pattern-canonical-terms-committed-in-this-brief): ≥80% greenfield-bloc pass AND ≥80% brownfield-bloc pass AND falsifying-outcome NOT triggered on any scenario).

## §1 Candidate + scenario set

**Candidate.** U-A is the unified-attempt Compound-Knowledge Atelier candidate (Heavy tier in [`auto-008` tier-table](../decisions/auto-008-phase-8-dispatch-shape.md#decision-round-2)). Per [`specs/u-a.md §1`](../specs/u-a.md#1-overview): U-A's load-bearing axis is the typed-node-graph over `EscrowInterval` envelopes — every cycle is a directed graph of typed interval nodes; the substrate enforces *what happens inside each interval* (gates, judges, immutable logs, sandbox attestations, reflection-trigger firings, AILCCP three-controls coverage); methodology layer composes *which intervals exist*. Entry-mode is mandate-parameterised: greenfield enters with `kind: bootstrap` (priors.in-tree=[]); brownfield enters with `kind: archaeology` (priors.in-tree=[codebase, history, traces, tests]). Steady-state on both mandates is the same interval graph — `kind` and `pace-layer` drive policy lookup; the substrate sees only the typed envelope.

**Mandate.** Unified-attempt. U-A's spec frontmatter carries `both` on 4-of-5 work-unit-classes (initial-spec, refactor, post-mvp-evolution, regression-fix) and `greenfield` on mvp. Per [auto-008 §Falsifier discipline R6 #1 + #2](../decisions/auto-008-phase-8-dispatch-shape.md#round-2-reviewer-amendments-folded-post-round-2-patches), U-A's `mandate-scenario-split: {greenfield: 3, brownfield: 3}` is mandatory; the §1 partition below honors it.

**Scenario set source.** Hybrid: scenarios draw from (a) the corpus F-mode catalog — F1 (hallucination loop), F8 (stale knowledge / self-referential bootstrap), F27 (bootstrap-can't-self-judge), F33 (lethal trifecta), F37 (silent contradictory-prompt collapse), F46 (single-model review blindspot), F47 (convenience-reclassifies-stakes), F48 (cross-interval tacit collusion), F53 (voluntary-discipline fragility), F55 (self-referential drift), F57 (regime-distribution drift) — and (b) U-A's own scenario-derivation primitives at [`specs/u-a.md §3 cycle steps 1-5`](../specs/u-a.md#3-methodology-shape) (interval-open → classifier-dispatch → execution → closure attempt → escalation/re-entry) and [`specs/u-a.md §5 mandate-fit cells`](../specs/u-a.md#5-mandate-fit) which name per-cell falsifying scenarios. The hybrid is non-redundant: corpus F-modes load the substrate's structural-discipline claim (F53 closure); candidate-derived scenarios surface the typed-graph's mandate-parameterisation claim.

### Greenfield-mandate scenarios

**Scenario count: 3 (≥3 mandatory per auto-008 R6 #1).** Each scenario is `kind: bootstrap` or downstream of a bootstrap interval; priors.in-tree=[]; priors.out-of-tree=[operator-curated adjacent-domain priors].

1. **Greenfield cold-start bootstrap with hard-floor verification (corpus F1 + F27 + candidate-derived ADR 0050 hard floor 1).** Day-0 operator authors a single `kind: bootstrap` interval on a prose-shaped greenfield intent (e.g., "a content-addressed event-bus exposing at-least-once delivery with idempotency-key dedup under multi-writer load"); evaluator confirms the ADR 0050 classifier dispatches `automation-eligibility = escalate` (substrate floor, NOT `lights-out`) AND `policies.judge-diversity: different-family` is mandatorily required by the ADR 0052 Rego bundle. **Engages [specs/u-a.md §3 distinctive decision #2](../specs/u-a.md#3-methodology-shape) ("Bootstrap interval cannot self-judge")** and [u-a §6 X_UNM_B carry-forward](../specs/u-a.md#6-open-carries) (greenfield bootstrap has no X_UNM_B gap, so this scenario is clean of that gap). Pass: classifier emits `escalate` (NOT `lights-out` / `sample-audit`); P-14 routes to a cross-family judge per the Rego rule; the bootstrap interval cannot close without `policies.judge-diversity` slot satisfaction; trajectory log under `solutions/audit/u-a-bootstrap/<interval-id>.json` shows the cross-family routing event. **Implements DEC-2 work-unit class `initial-spec` (greenfield-leaning).**

2. **Greenfield knowledge-promotion deferred until methodology-delta interval (corpus F8 + candidate-derived §4 knowledge-promotion).** Evaluator runs ≥5 cold-start `kind: bootstrap` → `kind: spec-author` → `kind: refactor` interval cycles WITHOUT any explicit `kind: methodology-delta` interval being authored; verifies `docs/solutions/` directory state remains empty (0 entries) — U-A's `kind: methodology-delta` IS the substrate's promotion gate per [specs/u-a.md §4 knowledge-promotion binding](../specs/u-a.md#4-discipline-binding). Then operator authors a `kind: methodology-delta` interval consuming the prior cycles' content-addressed envelope records; the ADR 0050 classifier dispatches with `judge-diversity: different-family` MANDATORY default per [ADR 0053 alternative B rejection](../../docs/adr/0053-p-30-variant-u-a-re-entry.md). Pass: 0 `docs/solutions/` entries before the methodology-delta interval; ≥1 entry promoted post-methodology-delta (typed envelope with `kind: methodology-delta` content-hash record); promotion event is cross-family-judged per ADR 0052 Rego slot rule. **The promotion envelope's category field is one of the 4-token enum `insight / playbook / correction / pattern` per [archive/architectures-v2/02-compound-atelier.md §3.2](../../archive/architectures-v2/02-compound-atelier.md) — see §7 cite obligation #1.**

3. **Greenfield self-improving-prompts pattern engaged via methodology-delta (H-2 / H-8 historian gap, candidate-derived).** Evaluator triggers a sequence in which an ADR 0050 classifier feature (e.g., `substrate_judge_agreement_recent < threshold`) recurs across 3 cycles, exposing a prompt-failure pattern. Per H-2 (self-improving prompts pattern) + H-8 (prompt-self-improver role) — both engaged in §7 below — the operator authors a `kind: methodology-delta` interval that rewrites the agent prompt class causing the divergence, gated by `policies.judge-diversity: different-family` per ADR 0052 + held against a P-08 holdout test set per [ADR 0021 holdout discipline](../../docs/adr/0021-discipline-holdout.md). Pass: rewritten-prompt-class succeeds against P-08 holdout at ≥80% (Klaassen-pattern bar from [archive/architectures-v2/02-compound-atelier.md line 173](../../archive/architectures-v2/02-compound-atelier.md)); the rewrite event is captured as a content-addressed `kind: methodology-delta` envelope; the ADR 0053 re-entry registrar emits no `severity_class_trigger` for the prompt class on subsequent cycles. **Surfaces F55 self-referential drift via the self-improvement loop closure.**

### Brownfield-mandate scenarios

**Scenario count: 3 (≥3 mandatory per auto-008 R6 #1).** Each scenario is `kind: archaeology` or downstream of an archaeology interval; priors.in-tree=[codebase, history, traces, tests]; priors.out-of-tree=[].

4. **Brownfield archaeology with X_UNM_B substrate-floor verification (corpus F37 + candidate-derived [specs/u-a.md §2 X_UNM_B](../specs/u-a.md#2-substrate-composition)).** Operator authors a `kind: archaeology` interval against an existing codebase (≥10K LOC across ≥3 languages so [P-22 polyglot codebase index (ADR 0017)](../../docs/adr/0017-p-22-polyglot-codebase-index.md) is exercised); evaluator confirms the ADR 0050 classifier hard floor 2 fires (`kind ∈ {archaeology, methodology-delta}` AND not yet audited at a re-entry interval → at-most `sample-audit`); the X_UNM_B substrate floor (post-archaeology interval defaults `classifier.automation-eligibility = escalate` per [specs/u-a.md §2 X_UNM_B paragraph](../specs/u-a.md#2-substrate-composition)) holds and `policies.judge-diversity: different-family` is mandatory on every downstream interval until the archaeology interval has been audited at a re-entry interval. Pass: classifier emits `sample-audit` at most (NOT `lights-out`); X_UNM_B floor holds; ≥1 archaeology-derived envelope produced as a typed P-28 record; no silent code-region-grain Codebase Model claim escapes the substrate. **Implements DEC-2 work-unit class `initial-spec` (brownfield-leaning via archaeology→spec-author chain) per [specs/u-a.md §5 initial-spec cell](../specs/u-a.md#5-mandate-fit).**

5. **Brownfield regression-fix via failing-test as priors.in-tree first element (corpus F33 + candidate-derived [specs/u-a.md §5 regression-fix cell](../specs/u-a.md#5-mandate-fit)).** Evaluator seeds a brownfield regression — a failing test that the existing codebase passed in a prior commit — and runs a `kind: regression-fix` interval. Per [specs/u-a.md §5 regression-fix](../specs/u-a.md#5-mandate-fit): "the failing test IS the substrate's near-anchor (in U-C terms) and U-A treats it as the `priors.in-tree` first element". The ADR 0050 classifier typically dispatches `sample-audit` after threshold measurement; ADR 0052 enforces the `gate` slot against the failing-test acceptance record (F33 lethal-trifecta closure via [ADR 0027 trifecta-closure](../../docs/adr/0027-discipline-trifecta-closure.md) = gate + holdout + sandbox all substrate-enforced). Pass: regression-fix interval closes with the failing test now passing; the close event satisfies all three trifecta slots (`gate` per ADR 0052; `holdout` per ADR 0021 with leak detection; `sandbox` per P-01); `audit_envelope` bundle hash captured per ADR 0052. **Falsifier-adjacent: if regression-fix routinely escalates to `human-required` because the substrate cannot distinguish it from broader refactor, the per-`kind` regime structure is wrong per [specs/u-a.md §5 regression-fix falsifying scenario](../specs/u-a.md#5-mandate-fit).**

6. **Brownfield post-MVP evolution + re-entry registrar with operator acknowledgement (corpus F47 + F48, candidate-derived [specs/u-a.md §3 step 5 + §6 F48 carry](../specs/u-a.md#3-methodology-shape)).** Evaluator runs ≥3 `kind: refactor` intervals against the existing brownfield codebase WHILE intentionally inducing a cost-ceiling breach on the 2nd interval (configured per [ADR 0011 P-02 cost ceilings](../../docs/adr/0011-p-02-cost-ceilings.md)) AND a Patrol-tier escalation on the 3rd (regime-distribution drift across `kind × pace-layer` slice per [ADR 0013 P-06 watchdog](../../docs/adr/0013-p-06-watchdog-tiers.md)). The ADR 0053 re-entry registrar MUST transition `in-flight → frozen → re-entry-open` on the cost-ceiling breach (via `cost_ceiling_breach(ledger_ref)` signal) AND on the Patrol escalation (via `watchdog_escalate(tier, evidence)` signal); operator's `operator_acknowledge(decision ∈ {resume, redirect, close}, payload)` is the atomic step to terminal state. Pass: both re-entry intervals fire; operator acknowledgement is captured as a content-addressed event-log envelope; the timer half of the Temporal triad fires ONLY to log `awaiting-operator-acknowledgement` per [ADR 0053 explicit asymmetry against D7-U-1](../../docs/adr/0053-p-30-variant-u-a-re-entry.md) — never drives a state transition. **Engages [specs/u-a.md §6 F48 carry](../specs/u-a.md#6-open-carries) (cross-interval tacit collusion via shared trajectory store) by verifying re-entry isolates the in-flight graph position without leaking subsequent-interval state.**

The 6 partitioned scenarios cover U-A's 4 unified-attempt-relevant work-unit-classes (initial-spec via #1+#4; refactor via #5+#6; post-mvp-evolution via #6; regression-fix via #5; mvp via #2 greenfield-only per spec §5 mvp cell) and pressure-test U-A's load-bearing wager: **the typed-node-graph substrate parameterises mandate via `kind` distribution while preserving the same structural-discipline closure on both blocs.** The 3+3 partition is the floor per auto-008 R6 #1; U-A's design lets the floor suffice for a 1-day evaluator-time bound.

**Why these 6 scenarios.** U-A's spec carries 6 open carries at [`specs/u-a.md §6`](../specs/u-a.md#6-open-carries); the lean-eval engages 4 of them directly (DPU-1 interval-granularity cost via #6's re-entry firing pattern under cost-ceiling pressure; classifier audit discipline via #1+#2's classifier dispatch verification; F48 cross-interval correlation via #6's re-entry isolation check; X_UNM_B articulation depth via #4's substrate-floor verification). Scenario selection prioritized (a) the candidate's distinctive load-bearing wager (typed-graph mandate-parameterisation → #2 + #4 are the mandate-symmetry tests), (b) F-mode coverage across 11 F-modes the spec invokes (F1/F8/F27/F33/F37/F46/F47/F48/F53/F55/F57), and (c) the 3+3 mandate-bloc floor per auto-008 R6 #1.

## §2 Success criteria

A U-A lean-eval result "passes cleanly" (per [auto-008 §Falsifier discipline R6 #2 unified-attempt partitioned form](../decisions/auto-008-phase-8-dispatch-shape.md#r2-2--3-dec-1a-falsifying-pattern-canonical-terms-committed-in-this-brief)) iff ALL of:

- **(a′) Partitioned quantitative gate (greenfield bloc):** ≥80% of the 3 `greenfield-mandate-scenarios` pass the §1 success criteria (i.e., ≥3 of 3 scenarios pass — at this scenario count, 80% rounds up to 3).
- **(a′) Partitioned quantitative gate (brownfield bloc):** ≥80% of the 3 `brownfield-mandate-scenarios` pass the §1 success criteria (i.e., ≥3 of 3 scenarios pass).
- **(b) Falsifying-outcome gate:** the §3 falsifying-outcome is NOT triggered on EITHER bloc.

**Per-scenario success criteria (verbatim from §1 above):**

1. **Greenfield cold-start bootstrap with hard-floor verification.** Classifier emits `escalate` (NOT `lights-out` / `sample-audit`); P-14 routes to a cross-family judge per the ADR 0052 Rego rule; the bootstrap interval cannot close without `policies.judge-diversity` slot satisfaction; trajectory log under `solutions/audit/u-a-bootstrap/<interval-id>.json` shows the cross-family routing event.

2. **Greenfield knowledge-promotion deferred until methodology-delta interval.** 0 `docs/solutions/` entries before the first `kind: methodology-delta` interval is authored AND ≥1 entry promoted post-methodology-delta (typed envelope with `kind: methodology-delta` content-hash record under the `refs/notes/escrow-interval` namespace per [ADR 0051](../../docs/adr/0051-p-28-variant-u-a-interval-envelope.md)); promotion event is cross-family-judged per ADR 0052 Rego slot rule; the envelope's category field is one of the 4-token enum `insight / playbook / correction / pattern`.

3. **Greenfield self-improving-prompts pattern engaged.** Rewritten-prompt-class succeeds against the P-08 holdout test set at ≥80% (Klaassen-pattern bar); the rewrite event is captured as a content-addressed `kind: methodology-delta` envelope; the ADR 0053 re-entry registrar emits no `severity_class_trigger` for the prompt class on subsequent cycles (≥3 cycles).

4. **Brownfield archaeology with X_UNM_B substrate-floor verification.** Classifier emits `sample-audit` at most (NOT `lights-out`); X_UNM_B floor (`escalate` post-archaeology until audited at re-entry) holds and is mechanically recoverable from substrate state (ADR 0050 classifier verdict + envelope's `classifier.automation-eligibility` field); ≥1 archaeology-derived envelope produced as a typed P-28 record under `refs/notes/escrow-interval` with `kind: archaeology`; no silent code-region-grain Codebase Model claim escapes the substrate (only interval-grain).

5. **Brownfield regression-fix.** Regression-fix interval closes with the failing test now passing; the close event satisfies all three trifecta slots (`gate` per ADR 0052 with leak-detection on the failing-test acceptance record; `holdout` per ADR 0021; `sandbox` per P-01); `audit_envelope` bundle hash captured per ADR 0052; ADR 0050 classifier dispatches `sample-audit` (NOT `human-required` — escalation to `human-required` flags this scenario fails per the spec §5 regression-fix falsifying scenario).

6. **Brownfield post-MVP evolution + re-entry registrar.** Both re-entry intervals fire on the seeded triggers (`cost_ceiling_breach` on interval-2; `watchdog_escalate` on interval-3); operator acknowledgement is captured as a content-addressed event-log envelope; the timer handler fires ONLY to log `awaiting-operator-acknowledgement` and re-arm — never drives a state transition (the explicit asymmetry against D7-U-1 per [ADR 0053 line on registrar-framework characterization](../../docs/adr/0053-p-30-variant-u-a-re-entry.md) and per [backfill-notes/u-a.md §4.3](../backfill-notes/u-a.md)).

**Note on success-criteria vs falsifying-outcome distinction (per [auto-008 §Falsifier discipline](../decisions/auto-008-phase-8-dispatch-shape.md#falsifier-discipline-load-bearing)):** failing the §2 success criteria can be implementation noise (a Rego bundle misconfigured; an OPA hard-floor mis-applied; a Temporal signal lost). Triggering the §3 falsifying-outcome is U-A's load-bearing claim — that the typed-node-graph substrate's `kind: methodology-delta` knowledge-promotion pathway serves BOTH mandates — being empirically wrong on at least one bloc.

## §3 Falsifying outcome

**Falsifying-outcome verbatim (≤80 words from YAML, repeated here for §3-vs-YAML consistency per [auto-008 falsification-designer rubric item (iv) MANDATORY](../decisions/auto-008-phase-8-dispatch-shape.md#r2-1-falsification-designer-concreteness-rubric-3-item-mechanical)):**

> Across 6 partitioned scenarios (3 greenfield bootstrap + 3 brownfield archaeology), U-A's Compound-Knowledge Atelier promotes zero methodology-delta intervals to typed `solutions/` envelopes (`docs/solutions/` directory state at scenario close, counted via the ADR-0051 envelope's `kind: methodology-delta` content-hash records) on EITHER the greenfield bloc OR the brownfield bloc. Equivalently: promotion-rate per bloc ≤0 entries per ≥3 cycles.

**Rationale.** U-A's central wager (per [`specs/u-a.md §1 load-bearing claim`](../specs/u-a.md#1-overview)) is that the typed-node-graph substrate parameterises BOTH mandates: greenfield via `kind: bootstrap` and brownfield via `kind: archaeology`, with the SAME `kind: methodology-delta` interval class serving as the substrate-bound knowledge-promotion gate on both blocs (per [`specs/u-a.md §4 knowledge-promotion binding`](../specs/u-a.md#4-discipline-binding): "pattern → standard promotion is itself a typed interval, mandatorily L4"). The falsifier is **mandate-asymmetric promotion failure**: if U-A's promotion pathway fires on ONE bloc but produces zero promoted patterns on the other, the unified-attempt claim collapses — U-A becomes a mandate-aligned candidate in disguise, NOT a methodology that serves BOTH mandates.

**Why this falsifier and not another.** Three alternative falsifiers were considered:

- "If ≥1 bootstrap interval graduates to `lights-out` before threshold-bars are measured" — this is ADR 0050 hard floor 1 collapse, a substrate-implementation defect, NOT a methodology-load-bearing-claim failure. It is failure-mode-of-implementation, not falsification of U-A's distinctive wager.
- "If the ADR 0053 re-entry registrar's timer-handler drives a state transition" — this is failure-mode-of-implementation against the explicit asymmetry against D7-U-1; it is the D7-U-1 collision-detection test, not U-A's distinctive wager.
- "If the cross-family judge slot rule mis-fires on >5% of intervals" — this is F46 mitigation efficacy, a property U-A shares with multiple other candidates (BF-S, GF-S also bind cross-family judge); it does not distinguish U-A's typed-graph wager.

The mandate-asymmetric knowledge-promotion failure is U-A's *distinctive* load-bearing wager — the claim that distinguishes U-A from a mandate-aligned methodology. **Per [auto-008 §Falsifier discipline](../decisions/auto-008-phase-8-dispatch-shape.md#falsifier-discipline-load-bearing): unified-attempt falsifiers carry the DEC-1.a load — triggering this falsifier surfaces "U-A's Compound-Knowledge Atelier fails to serve one of its claimed mandates", not just an implementation defect.** If the brownfield bloc shows zero promotions while greenfield succeeds, U-A is empirically a greenfield-aligned methodology with brownfield ceremony; if the greenfield bloc shows zero promotions while brownfield succeeds, U-A is empirically a brownfield-aligned methodology with greenfield ceremony. Either asymmetric collapse falsifies the unified-attempt claim that DEC-1.a hypothesizes as unlikely.

**Machine-checkability.** Per [auto-008 falsification-designer rubric 4-item check](../decisions/auto-008-phase-8-dispatch-shape.md#r2-1-falsification-designer-concreteness-rubric-3-item-mechanical):

- **(i) Metric:** `methodology-delta-promotion-rate` per bloc (countable: integer count of `kind: methodology-delta` content-hash records in `docs/solutions/` divided by interval count per bloc).
- **(ii) Artifact state:** `docs/solutions/` directory state at scenario close, counted via the ADR-0051 envelope's `kind: methodology-delta` content-hash records under the `refs/notes/escrow-interval` namespace (libgit2 path) or `envelope_kind = 'escrow-interval'` Postgres discriminator with `kind = 'methodology-delta'` (specific directory + specific record schema).
- **(iii) Threshold:** `≤0` entries per ≥3 cycles per bloc (numeric, single-direction comparison).
- **(iv) §3-vs-YAML consistency:** the YAML field and this §3 statement name the SAME metric (methodology-delta-promotion-rate), SAME artifact location (`docs/solutions/` + ADR-0051 envelope), SAME threshold (≤0 entries per ≥3 cycles), and SAME mandate-partition structure (greenfield bloc OR brownfield bloc).

The falsifier passes all 4 rubric items (mandatory pass on (iv); pass on all of (i)-(iii)). **Mandate-scenario-split-verified per auto-008 R6 #1 (verdict-token format check):** §1 partition is honored (3 greenfield scenarios + 3 brownfield scenarios); YAML `mandate-scenario-split: {greenfield: 3, brownfield: 3}` populated.

## §4 Failure modes the test surfaces

The 6 partitioned scenarios surface the following F-modes — for each, the specific F-mode(s) the scenario pressure-tests, citing the candidate's spec §3-§4 or §6 where applicable:

**Greenfield-mandate scenarios:**

- **Scenario #1 cold-start bootstrap** surfaces:
  - **F1 (hallucination loop)** — bootstrap-can't-self-judge per ADR 0050 hard floor 1; cross-family judge mandatory ([specs/u-a.md §3 distinctive decision #2](../specs/u-a.md#3-methodology-shape)).
  - **F27 (bootstrap-can't-self-judge)** — `kind: bootstrap → escalate` hard stop is the substrate floor; F27 closure is foundational per [specs/u-a.md §3](../specs/u-a.md#3-methodology-shape).
  - **F46 (single-model review blindspot)** — `policies.judge-diversity: different-family` Rego enforcement per ADR 0052; F46 mitigation is substrate-bound.
- **Scenario #2 knowledge-promotion deferred** surfaces:
  - **F8 (stale knowledge / self-referential bootstrap)** — deferring promotion until methodology-delta interval prevents premature pattern crystallization at cold-start; verified at [specs/u-a.md §4 knowledge-promotion](../specs/u-a.md#4-discipline-binding).
  - **F53 (voluntary-discipline fragility)** — promotion is structurally gated by the `kind: methodology-delta` interval class, NOT voluntary; this is U-A's load-bearing F53 closure per [specs/u-a.md §1](../specs/u-a.md#1-overview).
  - **F35 (methodology-delta cross-family-judge default)** — invoked per ADR 0053 alternative B rejection (cross-family judge mandatory by default).
- **Scenario #3 self-improving-prompts pattern** surfaces:
  - **F55 (self-referential drift)** — the rewrite-event is itself audited via the `kind: methodology-delta` envelope; drift is substrate-detectable.
  - **F42 (cognitive escrow)** — STIR cascade reflection-trigger fires during the rewrite per [ADR 0019 cognitive-escrow discipline](../../docs/adr/0019-discipline-cognitive-escrow.md); typed-node-graph axis bound.
  - **F51 (Ashby-deficiency on probabilistic detection)** — the P-08 holdout test set provides the deterministic check the probabilistic detection cannot.

**Brownfield-mandate scenarios:**

- **Scenario #4 archaeology + X_UNM_B floor** surfaces:
  - **F37 (silent contradictory-prompt collapse)** — brownfield archaeology interval consumes potentially-contradictory codebase priors; cross-family judge + `escalate` floor mitigate.
  - **F46 (single-model review blindspot)** — `judge-diversity: different-family` mandatory on every downstream interval until archaeology interval audited at re-entry.
  - **X_UNM_B substrate floor (per [specs/u-a.md §2 + §6](../specs/u-a.md#2-substrate-composition))** — substrate's graceful-degradation pattern; gap is honestly named.
- **Scenario #5 regression-fix** surfaces:
  - **F33 (lethal trifecta)** — gate + holdout + sandbox all substrate-enforced slot satisfactions per [ADR 0027 trifecta-closure](../../docs/adr/0027-discipline-trifecta-closure.md).
  - **F4 (code quality)** — ADR 0052 `gate` slot rule against the failing-test acceptance record; sandbox attestation.
  - **F20 (maintenance asymmetry)** — substrate cycle is uniform across work-unit-classes; same envelope on `kind: regression-fix` as on `kind: spec-author` per [specs/u-a.md §5 + §3](../specs/u-a.md#5-mandate-fit).
- **Scenario #6 re-entry + cost-ceiling + Patrol escalation** surfaces:
  - **F47 (convenience-reclassifies-stakes)** — Patrol-tier monitors regime-distribution drift across `kind × pace-layer` ([specs/u-a.md §6 F47 carry](../specs/u-a.md#6-open-carries)).
  - **F48 (cross-interval tacit collusion via shared trajectory store)** — re-entry isolation is the F48 mitigation surface ([specs/u-a.md §6 F48 carry](../specs/u-a.md#6-open-carries)).
  - **F16 (resume-fidelity)** — re-entry registrar snapshots in-flight graph position; recovery from trajectory store + immutable log per [ADR 0053](../../docs/adr/0053-p-30-variant-u-a-re-entry.md) and [backfill-notes/u-a.md §10.3](../backfill-notes/u-a.md).
  - **F57 (regime-distribution drift)** — Patrol monitoring detector.

The cross-cutting failure-mode coverage (11 distinct F-modes spanning both blocs equally) is the lean-eval's load. **No scenario engages a failure mode F-mode is not enumerated in U-A's spec §3-§4 or §6**; the lean-eval does NOT smuggle in failure modes U-A did not commit to defending.

**F-mode coverage matrix (partitioned for unified-attempt visibility):**

| F-mode | Description (one-line) | Scenario(s) | Bloc | U-A spec § |
|---|---|---|---|---|
| F1 | Hallucination loop | #1 | greenfield | §3 + §4 + ADR 0050 hard floor 1 |
| F4 | Code quality | #5 | brownfield | §3 + §4 |
| F8 | Stale knowledge / self-referential bootstrap | #2 | greenfield | §4 knowledge-promotion |
| F16 | Resume-fidelity | #6 | brownfield | §3 step 5 + ADR 0053 |
| F20 | Maintenance asymmetry | #5 | brownfield | §3 + §5 |
| F27 | Bootstrap-can't-self-judge | #1 | greenfield | §3 + ADR 0050 hard floor 1 |
| F33 | Lethal trifecta | #5 | brownfield | §4 trifecta + ADR 0027 |
| F35 | Methodology-delta close discipline | #2 | greenfield | §4 + ADR 0053 alternative B |
| F37 | Silent contradictory-prompt collapse | #4 | brownfield | §4 + ADR 0052 |
| F42 | Cognitive escrow | #3 | greenfield | §4 + ADR 0019 |
| F46 | Single-model review blindspot | #1, #4 | both | §4 bias-guard |
| F47 | Convenience-reclassifies-stakes | #6 | brownfield | §6 (Phase-5/8 carry) |
| F48 | Cross-interval tacit collusion | #6 | brownfield | §6 (Phase-8 lean-eval candidate) |
| F51 | Ashby-deficiency on probabilistic detection | #3 | greenfield | §6 (classifier audit) |
| F53 | Voluntary-discipline fragility | #2 | greenfield | §1 load-bearing |
| F55 | Self-referential drift | #3 | greenfield | §4 + methodology-delta |
| F57 | Regime-distribution drift | #6 | brownfield | §2 + §4 + §6 |
| X_UNM_B | Codebase Model acquisition substrate floor | #4 | brownfield | §2 + §6 |

18 F-mode/cross-mandate cells; each maps to ≥1 scenario; each cell's spec §-anchor is auditable from `specs/u-a.md`. **F46 covers BOTH blocs (cross-mandate)** — the only F-mode in U-A's design with explicit bi-mandate coverage, reflecting U-A's substrate-bound bias-guard pattern. **Coverage is intentional, not coincidental:** the partitioned scenarios were designed FROM the F-mode list AND the mandate-bloc requirement, not the reverse.

## §5 Evaluator time + protocol

**Expected evaluator time: 1 day** (per [v1.2 plan § Phase 8](../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md#phase-8--lean-eval-design-one-brief-per-candidate-first-pressure-test-surface-revised-in-v12) ~1-day-per-candidate bound). Breakdown:

- **Setup (~2.5 hours).** Evaluator initializes the U-A substrate stack per [`specs/u-a.md §2`](../specs/u-a.md#2-substrate-composition): common substrate baseline (8 ADRs 0010-0017: P-01 sandbox, P-02 cost ceilings, P-05 trajectory capture, P-06 watchdog Patrol tier, P-07 telemetry, P-08 scenario storage, P-14 judge router with cross-family routing, P-22 polyglot codebase index); discipline ADRs (0018-0027); FOUR framework + per-variant pairs (ADR 0028↔0050 P-19 classifier; ADR 0029↔0051 P-28 typed envelope under `refs/notes/escrow-interval`; ADR 0030↔0052 P-29 Rego policy bundle with six core slot rules `{gate, log, sandbox, approval-gate, reflection-trigger, judge-diversity}`; ADR 0036↔0053 P-30 ReEntryIntervalWorkflow in `state-machine-class = u-a-re-entry` namespace). H-2 self-improving-prompts pattern + H-8 prompt-self-improver role are engaged via scenario #3 (see §7 historian engagement).

- **Scenario execution (~5 hours).** Run scenarios #1-#6 in mandate-partition order (greenfield bloc #1-#3 first; brownfield bloc #4-#6 second). Each scenario produces (a) a trajectory log under `solutions/audit/u-a-<bloc>/<scenario-id>.json` per [P-05 (ADR 0012)](../../docs/adr/0012-p-05-trajectory-capture.md) via the envelope's `artefacts.trajectory` slot, (b) a Patrol-tier event log under `solutions/audit/patrol/<scenario-id>.json` for regime-distribution drift detection, (c) a `solutions/lean-eval/<scenario-id>/` directory for scenario-specific artifacts (interval-graph DAGs, classifier verdicts, Rego bundle verdicts, re-entry registrar events for #6, methodology-delta envelopes for #2+#3+#5+#6). Evaluator does NOT intervene mid-scenario; substrate-and-methodology-only.

- **Verdict pass (~30 minutes).** Evaluator computes (i) per-scenario pass/fail against §2 success criteria; (ii) the §3 falsifying-outcome check (methodology-delta-promotion-rate per bloc); (iii) the partitioned "pass cleanly" verdict per [auto-008 §Falsifier discipline R6 #2 unified-attempt form](../decisions/auto-008-phase-8-dispatch-shape.md#r2-2--3-dec-1a-falsifying-pattern-canonical-terms-committed-in-this-brief). Verdicts written to `solutions/lean-eval/verdict-u-a.md` with explicit per-bloc tallies.

**Protocol invariants** (per [auto-008 §Falsifier discipline escape-hatch enumeration + structural rider R6 #5](../decisions/auto-008-phase-8-dispatch-shape.md#r2-2--3-dec-1a-falsifying-pattern-canonical-terms-committed-in-this-brief)):

- **No out-of-mandate scope claim.** U-A claims BOTH mandates; per R6 #5 structural rider, "declaring an entire mandate-bloc out-of-scope is structurally a failure to deliver on the unified-attempt claim; ≥1 mandate-bloc with <3 scenarios scored fails R2 #3 (a′) by construction." Each bloc has exactly 3 scenarios; declaring any out-of-mandate is structurally a failure.
- **No scenario-skip mid-run.** All 6 scenarios are executed; partial completion is a failure, not a skip.
- **No criterion-substitution.** §2 success criteria are committed in this brief; evaluator does NOT re-interpret them mid-run. If §2 is defective, the brief is rewritten not the criterion swapped.

**Substrate ground-truth invariants.** The evaluator records the substrate state at end-of-scenario (`ADR 0051` envelope content-hash records + `ADR 0052` Rego bundle audit_envelope hash + `ADR 0053` re-entry workflow event log + `ADR 0050` classifier verdict for each interval). The per-bloc methodology-delta-promotion-rate (the §3 falsifier metric) is reconstructable from substrate state alone via `git for-each-ref refs/notes/escrow-interval` (libgit2 path) or `SELECT * FROM envelopes WHERE envelope_kind = 'escrow-interval' AND payload->>'kind' = 'methodology-delta'` (Postgres path) filtered by bloc identifier in `solutions/audit/u-a-<bloc>/`.

**Hour-by-hour evaluator-time breakdown** (8-hour evaluator-day budget):

| Hour | Phase | Activity | Artifacts produced |
|---|---|---|---|
| 0:00-1:00 | Setup | Initialize common-substrate baseline (P-01..P-22); discipline ADRs 0018-0027 | `solutions/setup/substrate-init.log` |
| 1:00-2:30 | Setup | Initialize FOUR framework+variant pairs (0028↔0050; 0029↔0051; 0030↔0052; 0036↔0053); load U-A Rego bundle | `solutions/setup/u-a-variant-pairs.json` |
| 2:30-3:00 | Scenario #1 | Greenfield cold-start bootstrap; verify ADR 0050 hard floor 1 | `solutions/audit/u-a-greenfield/sc1-*.json` |
| 3:00-3:45 | Scenario #2 | Greenfield 5-cycle pre-promotion + methodology-delta authoring | `solutions/audit/u-a-greenfield/sc2-*.json` + `docs/solutions/sc2/*` |
| 3:45-4:30 | Scenario #3 | Self-improving-prompts rewrite + P-08 holdout verification | `solutions/audit/u-a-greenfield/sc3-*.json` |
| 4:30-5:15 | Scenario #4 | Brownfield archaeology + X_UNM_B floor check | `solutions/audit/u-a-brownfield/sc4-*.json` |
| 5:15-6:00 | Scenario #5 | Brownfield regression-fix + trifecta closure | `solutions/audit/u-a-brownfield/sc5-*.json` |
| 6:00-7:00 | Scenario #6 | Brownfield ≥3 refactor + 2 re-entry firings | `solutions/audit/u-a-brownfield/sc6-*.json` + re-entry event log |
| 7:00-7:30 | Verdict pass | Per-bloc tallies; methodology-delta promotion-rate check; partitioned "pass cleanly" verdict | `solutions/lean-eval/verdict-u-a.md` |
| 7:30-8:00 | Reporting | Write verdict-u-a.md with per-bloc detection + escape-hatch audit + structural-rider check | (same file) |

Total 8 hours; scenarios consume ~5.25 hours; setup + verdict ~2.75 hours. If any scenario over-runs, evaluator records the over-run in the verdict file but does NOT skip subsequent scenarios — partial completion = scenario fails per §5 protocol invariants no-scenario-skip clause. **Per [auto-008 R5 #5 over-budget recovery](../decisions/auto-008-phase-8-dispatch-shape.md#sub-wave-coordination-protocol):** if a scenario's substrate state cannot be initialized within its allotted hour, the scenario is recorded as failed; do not silently re-shape the timeline.

## §6 Open critique references

U-A's [`specs/u-a.md §6 Open carries`](../specs/u-a.md#6-open-carries) lists 6 open critique findings; the lean-eval engages 4 of them directly:

- **DPU-1 interval-granularity cost at year-2 scale** → engaged by scenario #6 (cost-ceiling firing + re-entry under Patrol escalation pressure). The lean-eval verifies DPU-1's load-bearing cost claim survives across 3 refactor intervals + 2 re-entry firings within the D-5 cost-ceiling budget; **if scenario #6 over-runs the cost ceiling OR fails to fire the re-entry registrar within budget, DPU-1 is escalated as a Phase-9 simulator-harness carry.**
- **Classifier audit discipline at scale (F57 amplified)** → engaged by scenario #6 (Patrol-tier regime-distribution drift detection on `kind × pace-layer` slice). The lean-eval verifies the Patrol detector fires under the seeded drift; full audit-trail completeness on graduation events is a Phase-9 carry.
- **F48 cross-interval correlation via shared trajectory store** → engaged by scenario #6 (re-entry isolation verification). The lean-eval verifies the re-entry registrar isolates in-flight graph position without leaking subsequent-interval state; **if scenario #6 reveals cross-interval state leak, F48 is escalated as a Phase-5/6 ADR-0051 envelope-partition discipline carry.**
- **X_UNM_B articulation depth** → engaged by scenario #4 (archaeology + substrate-floor verification). The lean-eval verifies the substrate honestly carries the gap (interval-grain only, not code-region-grain) and the `escalate` floor holds; the Phase-5/6 methodology-spec carry for code-region-grain typing is downstream.

The 2 open carries NOT engaged by this lean-eval:

- **Re-entry partial semantics (Phase-6 methodology spec carry)** → not engaged. `resume-with-modifications` / `redirect-to-different-kind` / partial-graph rehydration are deferred per ADR 0053; the lean-eval tests the fixed state-machine skeleton, not the partial-re-entry policy.
- **OQ-PLEF-style multi-cycle drift on the typed envelope (Phase-3 adversarial pass carry — open)** → not engaged. Whether "interval" is itself a contaminating label is a Phase-3-style blind-axis-test question; the lean-eval tests the chosen interval framing under its own claims.

## §7 Phase-7 cite obligations honored

Per the [`auto-008` per-candidate cite-obligation mapping table for U-A](../decisions/auto-008-phase-8-dispatch-shape.md#high-confidence-mandatory-cite-obligations-3-cells--n-candidates): U-A carries **the most cite obligations of any v3 candidate** (3 high-confidence mandatory cites; medium-confidence cells from §B.1; H-2 + H-8 historian gaps). Each is honored below.

### High-confidence mandatory cite obligations (3 cells)

**Cite obligation #1: Knowledge-promotion 4-token enum** (`insight / playbook / correction / pattern`).

Per [`audit-silent-absorption.md` §B.1 finding #1](../backfill-notes/audit-silent-absorption.md): U-A's `specs/u-a.md §4 knowledge-promotion binding` line 133 carries the 4-token enum *"Compound-Knowledge insight / playbook / correction / pattern envelopes"* — the four-token category set IS the Atelier `02-compound-atelier.md` §3.2 YAML enum lifted verbatim. U-A absorbed this silently; per [Phase-7 aggregation §3.1 finding #1](../backfill-notes.md#31-high-confidence-findings-3--apply-precedence-rule), U-A carries the archive-lineage cite here.

**Verbatim archive cite:** The 4-token enum appears in [`archive/architectures-v2/02-compound-atelier.md` §3.2 Knowledge document shape](../../archive/architectures-v2/02-compound-atelier.md):

> *"`type: solution | insight | playbook | correction | pattern`"*

(verbatim from `02-compound-atelier.md` line 88; the v2 YAML frontmatter enum carries 5 tokens but U-A's spec absorbs the 4-token subset `insight / playbook / correction / pattern`, treating `solution` as the umbrella type expressed via the `kind: methodology-delta` substrate interval class.) **Cite honored in this brief:** scenario #2's success criterion names the 4-token enum as the required category-field value on promoted envelopes; scenario #3's rewrite-event also takes one of these 4 tokens (typically `pattern` for prompt-class patterns). The archive lineage is from [`archive/architectures-v2/02-compound-atelier.md §3.2`](../../archive/architectures-v2/02-compound-atelier.md).

**Cite obligation #2: Compound-Engineering 4-step loop verbatim cite** → [`archive/synthesis-v1-v2/13-round-2-synthesis.md`](../../archive/synthesis-v1-v2/13-round-2-synthesis.md).

Per [`audit-silent-absorption.md` §B.1 finding #2](../backfill-notes/audit-silent-absorption.md): the phrase "Compound-Engineering plan → work → review → compound" appears verbatim across 7 specs including U-A; none cite the archive `02-compound-atelier.md` or `00-synthesis.md` where the four-step phrasing is canonicalized. U-A's `specs/u-a.md §4 three-loop binding` line 136 carries:

> *"Bound at the Compound-Engineering plan→work→review→compound loop expressed as a graph of intervals. The 'compound' step materialises as Patrol-tier (P-06) monitoring of regime-distribution drift across the `kind × pace-layer` slice — meta-loop closure is substrate-enforced."*

**Cite honored in this brief:** scenarios #2 (knowledge-promotion deferred) and #6 (Patrol-tier escalation) both engage the "compound" step of the Compound-Engineering loop. Per Phase-7 cite obligation, the lean-eval brief carries the archive lineage cite for the 4-step loop. The Round-2 synthesis at [`archive/synthesis-v1-v2/13-round-2-synthesis.md`](../../archive/synthesis-v1-v2/13-round-2-synthesis.md) is the v0.2-canonical record where the 4-step shape was promoted from `research/03-` to load-bearing methodology vocabulary; the verbatim 4-step phrasing is canonicalized at `00-synthesis.md` §0 ("Canonical compound-engineering loop is four-step (Plan → Work → Review → Compound), not five. Brainstorm is subsumed into Plan in the canonical Klaassen/Shipper statement") and at `archive/architectures-v2/02-compound-atelier.md` line 20 v0.2 note ("**Canonical compound-engineering loop is FOUR-STEP** (Plan → Work → Review → Compound), not five.").

**Cite obligation #3: 4-architecture taxonomy** → [`archive/architectures-v2/00-comparison.md §1`](../../archive/architectures-v2/00-comparison.md).

Per [`audit-silent-absorption.md` §B.1 finding #3](../backfill-notes/audit-silent-absorption.md): U-A's `specs/u-a.md §3 work-unit definition` carries "Atelier-style issue-intake / Refinery-style spec-delta entry / Attractor-DOT pipeline" as work-unit-shape taxonomy across 5 specs including U-A; specs cite registry / tracks but never the archive. The four-architecture taxonomy IS [`archive/architectures-v2/00-comparison.md §1`](../../archive/architectures-v2/00-comparison.md):

> *"| 1 | **Specification Refinery** | The spec is the product; the implementation is a probe that reveals what the spec did not say | The existing `spec-driven-ai-dev.md`, refined | | 2 | **Compound Atelier** | Each unit of work makes the next easier — by passing through specialist hands and leaving its lessons behind | Every.to's compound-engineering plugin + Symphony | | 3 | **Phase-Gated Foundry** | Pre-agile structured methodologies become the right shape when agents make them fast | Waterfall + V-Model + RUP + Cleanroom, at hour cycle time | | 4 | **Evolutionary Tournament** | The factory does not specify the right answer; it sets up the conditions under which the right answer wins | Genetic algorithms + Willison's 'code is cheap' + StrongDM satisfaction-as-judge |"*

(verbatim from `00-comparison.md` lines 33-38). **Cite honored in this brief:** scenarios #2 (knowledge-promotion deferred via methodology-delta) and #4 (archaeology) both engage the Atelier-style / Refinery-style work-unit-shape taxonomy; U-A multiplexes all 4 v2 lineages onto the typed-graph substrate per [`backfill-notes/u-a.md §1`](../backfill-notes/u-a.md). Archive lineage at `00-comparison.md §1`.

### Medium-confidence design inputs (consulted from `audit-silent-absorption.md` §B.1)

Per [`audit-silent-absorption.md` §B.1`](../backfill-notes/audit-silent-absorption.md): finding #4 (medium-confidence) names U-A × `02-compound-atelier.md` §3 (artifact stack with YAML frontmatter / stable IDs) — the typed-envelope axis with `kind`, content-hash `id`, frontmatter-discipline fields is structurally the Atelier §3.2 YAML-frontmatter knowledge-doc shape lifted to substrate. Specs cite ADR 0029 P-28; ADR 0029's lineage to Atelier §3 is not surfaced.

**Engagement in this brief:** scenario #1's bootstrap envelope authoring and scenario #2's methodology-delta envelope schema both ride the ADR 0051 envelope structure; the typed-envelope-as-Atelier-knowledge-doc-shape lineage is the design input. The lean-eval does NOT rewrite ADR 0029 / ADR 0051; the medium-confidence finding is flagged as a `tbd` row in the Phase-7 aggregation for lead-agent adjudication (Atelier-derived vs sufficiently-transformed). **Non-blocking for this lean-eval.**

### Historian load-bearing design inputs (engaged)

Per [`backfill-notes.md §4.1 historian load-bearing gaps`](../backfill-notes.md#41-load-bearing-gaps-5--phase-8-lean-eval-inputs):

- **H-2 (self-improving prompts pattern) + H-8 (prompt-self-improver role)** — paired gap; methodology decision for GF-S / GF-M / **U-A**. Per [`archive/architectures-v2/02-compound-atelier.md` line 22 + line 173](../../archive/architectures-v2/02-compound-atelier.md): the v0.2 update names the self-improving-prompts pattern explicitly and adds the "Prompt-self-improver" role — Klaassen's frustration-detector + Tedesco's Montaigne as concrete instances. 

**For U-A:** the self-improving-prompts pattern is structurally aligned with the `kind: methodology-delta` interval class (every methodology evolution is a typed interval with `judge-diversity: different-family` default per ADR 0053 alternative B rejection). The H-8 prompt-self-improver role is realized as a typed interval subclass under the methodology-delta umbrella — the operator (or substrate-fired reflection-trigger) authors a methodology-delta interval whose `policies.gate` slot verifies the rewritten-prompt against P-08 holdout.

**Decision for U-A's lean-eval:** **scenario #3 explicitly engages H-2 + H-8** via the Klaassen-pattern bar (≥80% on rewritten-prompt against P-08 holdout). The scenario is the lean-eval's H-2/H-8 engagement surface; the rewrite event is itself audited via the `kind: methodology-delta` envelope (substrate-bound). **Methodology-shape note for `specs/u-a.md §3` (carried as a Phase-8-followup advisory if not adopted):** consider naming the prompt-self-improver role explicitly as a `kind: methodology-delta` interval sub-class to make the H-2/H-8 alignment auditable. Non-blocking.

### Cite-obligation summary (YAML `phase-7-cite-obligations` field)

- `high-confidence-mandatory`: **3 cites** (knowledge-promotion 4-token enum → `02-compound-atelier.md §3.2`; Compound-Engineering 4-step loop → `13-round-2-synthesis.md`; 4-architecture taxonomy → `00-comparison.md §1`). U-A carries the most cite obligations of any v3 candidate; all 3 are honored verbatim in §7 above.
- `medium-confidence-design-inputs`: **1 §B.1 cell** (finding #4 — U-A × `02-compound-atelier.md` §3 typed-envelope-as-Atelier-knowledge-doc-shape lineage; design input only, non-blocking).
- `historian-design-inputs`: **2 (H-2 + H-8 paired)**; engaged in scenario #3's self-improving-prompts rewrite; cited from `archive/architectures-v2/02-compound-atelier.md` line 22 + line 173.

## §8 References

**Candidate spec + back-fill notes (primary inputs):**

- [`specs/u-a.md`](../specs/u-a.md) — Phase-6 U-A architecture spec; §0 ADR-citation index, §1 Overview, §2 Substrate composition (four framework+variant pairs), §3 Methodology shape, §4 Discipline binding, §5 Mandate fit, §6 Open carries.
- [`backfill-notes/u-a.md`](../backfill-notes/u-a.md) — Phase-7 back-fill audit; §1.5 D-1..D-7 defaults; §3.1.11 persona-vs-graph-node verdict; §4.3 ADR-0036 registrar-framework characterization; §7 deepest absorption section (12-of-14 cells Atelier-absorbed); §10.3 F-mode coverage (17-of-20 absorbed, 8 verified).
- [`substrate-requirements/u-a.md`](../substrate-requirements/u-a.md) — Phase-4 substrate-requirements summary (referenced by spec §2).
- [`candidate-registry.md` U-A entry](../candidate-registry.md#u-a--escrow-graph-factory-cycle--directed-graph-of-typed-nodes) — registry entry; multi-lineage statement.

**Phase-8 dispatch artifacts:**

- [`decisions/auto-008-phase-8-dispatch-shape.md`](../decisions/auto-008-phase-8-dispatch-shape.md) — this brief's parent dispatch decision; §Falsifier discipline (R2 #1-#4 rubric + R6 #1-#5 partitioned-mandate amendments load-bearing for U-A); §Phase-7 cite-obligation propagation table (U-A row with 3 high-confidence cites); §Per-candidate lean-eval brief rubric.
- [`scope-envelope-2026-05-28-phase-8.md`](../scope-envelope-2026-05-28-phase-8.md) — Phase-8 run scope envelope.
- [`lean-evals/gf-m.md`](gf-m.md) — Wave-8.1 exemplar (non-unified-attempt, single-bloc; U-A's brief partitions §1 per R6 #1).

**Phase-7 inputs (cite-obligation source):**

- [`backfill-notes.md`](../backfill-notes.md) — Phase-7 aggregation matrix; §3.1 (high-confidence cite obligations, 3 cells touching U-A), §3.2 (medium-confidence TBDs), §4.1 (historian load-bearing gaps H-2/H-8).
- [`backfill-notes/audit-silent-absorption.md`](../backfill-notes/audit-silent-absorption.md) — Phase-7 silent-absorption auditor output; §B.1 findings #1, #2, #3 (load-bearing for U-A); finding #4 (medium-confidence; design input).
- [`backfill-notes/audit-historian.md`](../backfill-notes/audit-historian.md) — Phase-7 historian auditor output; H-2 + H-8.

**ADRs cited (substrate + discipline + framework + per-variant):**

- Common substrate: [ADR 0010](../../docs/adr/0010-p-01-sandbox-runtime.md), [ADR 0011](../../docs/adr/0011-p-02-cost-ceilings.md), [ADR 0012](../../docs/adr/0012-p-05-trajectory-capture.md), [ADR 0013](../../docs/adr/0013-p-06-watchdog-tiers.md), [ADR 0014](../../docs/adr/0014-p-07-telemetry-ingestor.md), [ADR 0015](../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md), [ADR 0016](../../docs/adr/0016-p-14-judge-router.md), [ADR 0017](../../docs/adr/0017-p-22-polyglot-codebase-index.md).
- Discipline: [ADR 0018](../../docs/adr/0018-discipline-bias-guard.md) through [ADR 0027](../../docs/adr/0027-discipline-trifecta-closure.md) (all 10).
- Framework + per-variant pairs (load-bearing for U-A): [ADR 0028 (P-19)](../../docs/adr/0028-p-19-eligibility-regime-classifier.md) ↔ [ADR 0050 (U-A variant)](../../docs/adr/0050-p-19-variant-u-a-interval-kind.md); [ADR 0029 (P-28)](../../docs/adr/0029-p-28-typed-object-store.md) ↔ [ADR 0051 (U-A variant)](../../docs/adr/0051-p-28-variant-u-a-interval-envelope.md); [ADR 0030 (P-29)](../../docs/adr/0030-p-29-policy-mediator.md) ↔ [ADR 0052 (U-A variant)](../../docs/adr/0052-p-29-variant-u-a-interval-policy.md); [ADR 0036 (P-30)](../../docs/adr/0036-p-30-event-registrar-substrate.md) ↔ [ADR 0053 (U-A variant)](../../docs/adr/0053-p-30-variant-u-a-re-entry.md).

**Archive sources (Phase-7 cite obligations — 3 high-confidence mandatory):**

- [`archive/architectures-v2/02-compound-atelier.md` §3.2](../../archive/architectures-v2/02-compound-atelier.md) — Knowledge-promotion 4-token enum `insight / playbook / correction / pattern` (cite obligation #1).
- [`archive/synthesis-v1-v2/13-round-2-synthesis.md`](../../archive/synthesis-v1-v2/13-round-2-synthesis.md) — Compound-Engineering 4-step loop v0.2 canonicalization (cite obligation #2).
- [`archive/architectures-v2/00-comparison.md §1`](../../archive/architectures-v2/00-comparison.md) — 4-architecture taxonomy (cite obligation #3).
- [`archive/architectures-v2/02-compound-atelier.md` line 22 + line 173](../../archive/architectures-v2/02-compound-atelier.md) — H-2 self-improving-prompts pattern + H-8 prompt-self-improver role (historian engagement).

**Cross-cutting v3 docs:**

- [`decisions-captured.md`](../decisions-captured.md) — DEC-1.a working hypothesis (U-A IS one of 4 unified-attempt candidates carrying the DEC-1.a falsification load); DEC-2 mandate-fit-per-(architecture × work-unit-class).
- [`failure-modes-v3.md`](../failure-modes-v3.md) — F-mode catalog (18 F-modes/cross-mandate cells engaged by U-A's 6 scenarios).
- [`candidate-registry.md`](../candidate-registry.md) — U-A candidate-registry entry with multi-lineage statement (Atelier primary; Refinery / Foundry / Tournament secondary).

---

## Self-check results (items a-g per auto-008 §Per-candidate lean-eval brief rubric)

- **(a) `wc -w`**: target 5500-7200 (Heavy tier). Recorded at commit time.
- **(b) `ls` on cited paths**: all cited paths verified present at commit time (specs/u-a.md; backfill-notes/u-a.md; backfill-notes.md; audit-silent-absorption.md; decisions/auto-008; archive/architectures-v2/02-compound-atelier.md; archive/synthesis-v1-v2/13-round-2-synthesis.md; archive/architectures-v2/00-comparison.md; ADRs 0010-0027 + 0028-0053).
- **(c) `grep -cE "^## §[1-8]"`**: exactly 8 §-headers (§1 through §8).
- **(d) `grep "falsifying-outcome:"` + value ≤80 words**: YAML field present at line 11 of YAML frontmatter; field value is **66 words** (under ≤80-word limit). Load-bearing pass.
- **(e) `grep -c "phase-7-cite-obligations:"`**: YAML field present with 3 high-confidence-mandatory + 1 medium-confidence + 2 historian design inputs.
- **(f) Binding-rule-table verbatim text-pull**: PASS. The 4-token enum (cite obligation #1), the 4-architecture taxonomy table rows (cite obligation #3), and the v0.2 four-step canonicalization (cite obligation #2) are pulled verbatim from their archive sources in §7.
- **(g) `grep -cE "##? §[1-8]"`**: 8 §-headers from §1 through §8.
- **mandate-scenario-split-verified (per R6 #1 + falsification-designer rubric)**: PASS. §1 partition is honored (3 greenfield scenarios in `### Greenfield-mandate scenarios` subsection + 3 brownfield scenarios in `### Brownfield-mandate scenarios` subsection); YAML `mandate-scenario-split: {greenfield: 3, brownfield: 3}` populated; matches §1 actual count.
