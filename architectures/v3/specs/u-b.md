---
candidate: u-b
candidate-name: Layered Substrate Factory
mandate-scope: unified-attempt
based-on-commit: c54daf1
based-on-date: 2026-05-26
mandate-fit:
  initial-spec: both
  refactor: both
  mvp: greenfield
  post-mvp-evolution: both
  regression-fix: both
---

# Architecture spec — U-B (Layered Substrate Factory)

## §0 ADR-citation index

| ADR ID | Title | Layer | Variant of | Citing § |
|---|---|---|---|---|
| 0010 | P-01 Sandbox runtime | common-substrate | — | §2, §4 |
| 0011 | P-02 Cost ceilings | common-substrate | — | §2, §4 |
| 0012 | P-05 Trajectory capture | common-substrate | — | §2, §3, §4 |
| 0013 | P-06 Watchdog tiers | common-substrate | — | §2, §3, §4 |
| 0014 | P-07 Telemetry ingestor | common-substrate | — | §2, §3 |
| 0015 | P-08 Scenario storage with runner contract | designed-system-substrate | — | §2, §4 |
| 0016 | P-14 Judge router | common-substrate | — | §2, §3, §4 |
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
| 0029 | P-28 Typed-object store framework | common-substrate | — | §2, §3 |
| 0055 | U-B P-28 variant — layer-typed envelope `TypedObject<L>` | per-variant-substrate | 0029 | §2, §3 |
| 0030 | P-29 Policy mediator framework | common-substrate | — | §2, §3, §4 |
| 0056 | U-B P-29 variant — per-layer-boundary policy DSL | per-variant-substrate | 0030 | §2, §3, §4 |
| 0031 | P-23 Dependency-impact graph | common-substrate | — | §2, §3 |
| 0054 | P-31 Cross-layer drift detector | orphan-substrate | — | §2, §3, §6 |

**Framework + per-variant pairing check.** U-B claims frameworks 0029 (P-28) and 0030 (P-29) — each load-bearing per [AGENTS-MD-a9fb7b42f8](../../../AGENTS.md#framework-adr-scope-boundary-discipline) — and pairs each framework reference with U-B's per-variant ADR in the index above: 0029 with 0055 (`TypedObject<L>` layer-typed envelope); 0030 with 0056 (per-layer-boundary policy DSL). The U-B-distinctive orphan ADR 0054 (P-31 cross-layer drift detector) carries no Variant-of row — U-B is the sole claimant. U-B does NOT claim frameworks 0028 (P-19 eligibility/regime classifier) or 0036 (P-30 event registrar) as substrate primitives: per the [u-b.md §1 primitive list](../substrate-requirements/u-b.md), the only regime-classification surface U-B carries is the per-layer-pair P-31 invariant catalog (which is *not* an eligibility classifier — it produces typed `LayerDriftEvent` outputs, not a regime label feeding a dispatcher), and U-B has no timer-driven survival-window primitive that would justify P-30 framework consumption. The methodology-layer cognitive-escrow primitive that U-B's [track sketch §1](../tracks/unified-B.md) names lives at methodology per [DEC-2](../phase-3.4-decisions-resolved.md#dec-2--cognitive-escrow-placement-methodology) and does not appear in the substrate index.

## §1 Overview

**Mandate.** Unified-attempt. U-B carries the unified mandate via a *layered substrate*: same primitives are deployed in both directions on the same five-layer artifact stack (L0 Standards / L1 Architecture / L2 Spec / L3 Plan / L4 Code), with the mandate becoming an *input parameter* (which direction the cycle traverses) rather than the organising distinction (per [unified-B §0](../tracks/unified-B.md)).

**Axis.** Pace-layer × bidirectional traversal. The architecture organises around (a) Brier's pace-layer stack (slow at L0, fast at L4) and (b) layer-typing as a first-class envelope property on the P-28 typed-object store. Greenfield = top-down traversal (seed L0/L1 from priors; descend to L4). Brownfield = bottom-up traversal (read L4; infer L3→L0 with explicit completeness gaps).

**Entry-mode.** Either greenfield (cold-start: L0 seeded from AILCCP catalogue + INCOSE GtWR + EARS + Caremark/SB-53 priors; L1 Pareto-sketched from L0; L2 from El Kaim 9-field intent block) or brownfield (L4 entry, P-22 + P-23 + ADR archaeology for L1 inference, with declared lossiness per [u-b.md §4 X_UNM_B](../substrate-requirements/u-b.md)).

**Methodology summary.** Substrate-heavy, layer-thin-methodology. Per-cycle process is generic — agent receives a work unit, the unit targets a specific pace-layer, the layer-typed envelope (ADR 0055) carries the cycle's typed object, the per-layer-pair P-29 gate (ADR 0056) refuses to materialise the downstream object until the upstream layer's `escrow-policy` field has satisfying records, and the orphan P-31 detector (ADR 0054) emits `LayerDriftEvent` against the Wave 4.5 invariant registry on any cross-layer drift the per-pair invariants catch.

**Load-bearing claim.** *Layer typing is the substrate's first-class property.* P-28 envelopes carry `layer ∈ {L0,L1,L2,L3,L4}` as their primary index; P-29 mediates each Lᵢ → Lᵢ₊₁ boundary; P-31 detects cross-layer drift across all five pace-layer pairs (including the long-distance L0↔L4). The architecture defends *layered substrate* as a discipline, not as a methodology pattern.

## §2 Substrate composition

U-B carries three substrate-layer ADRs beyond the common substrate baseline (0010-0017) and discipline ADRs (0018-0027): the P-28 layer-typed envelope, the P-29 per-layer-boundary policy DSL, and the orphan P-31 cross-layer drift detector. The framework-pair structure is load-bearing per [AGENTS-MD-a9fb7b42f8](../../../AGENTS.md#framework-adr-scope-boundary-discipline).

**Framework substrate (with per-variant pairing).** The [Phase-4.2 overlap.md verdict on P-28](../primitives/overlap.md#p-28-typed-object-store--four-contested-variants) is verbatim:

> **"Verdict: SAME primitive (P-28 typed-object store framework), DISTINCT envelopes. All four share the construction recipe (libgit2 `git_odb_write` + `refs/notes/<envelope-kind>`; Postgres `bytea`+`jsonb`+GIN alternate path; content-addressed append-only with typed envelope per P-28 sketch). The envelope schemas are non-overlapping but the underlying primitive (typed envelope + content-hash + append-only + Glean/Postgres-compatible storage) is identical."**

The [overlap.md verdict on P-29](../primitives/overlap.md#p-29-policy-mediator--compounding-gate--three-contested-variants) is verbatim:

> **"Verdict: SAME primitive (P-29 policy mediator framework), DISTINCT policy DSLs. All three share the underlying engine (OPA Rego primary; Cedar alternate path per P-29 sketch). The policy vocabulary differs: U-A reasons about interval-slot satisfaction; U-B reasons about layer-pair closure; D7-U-1 reasons about FC-survival windows. The differences are at the predicate vocabulary level, not the engine level."**

Both verdicts bind U-B's spec to pair every framework ADR with its U-B per-variant ADR. Concretely:

- **P-28 layer-typed envelope (`TypedObject<L>`).** Framework: [ADR 0029](../../../docs/adr/0029-p-28-typed-object-store.md) records the common substrate decision (libgit2 `git_odb_write` + `refs/notes/<envelope-kind>` namespaces, or Postgres `bytea`+`jsonb`+GIN alternate path; content-addressed append-only) shared across four contested variants. U-B variant: [ADR 0055](../../../docs/adr/0055-p-28-variant-u-b-layer-typed-envelope.md) registers the `typed-object-layer` envelope-kind with schema `{layer ∈ {L0 Standards, L1 Architecture, L2 Spec, L3 Plan, L4 Code}, change-rate, escrow-policy, invariants[], parent-layer-ref, child-layer-refs[]}` and typed-filter axis `layer × (parent-layer-ref → child-layer-refs)` traversal. U-B's contract is **layer-indexed-first** — `layer` is the primary GIN index (a sub-namespace per layer under `refs/notes/typed-object-layer/L{0..4}/`); `parent-layer-ref` and `child-layer-refs[]` are content-hash pointers (preserving ADR 0029's append-only discipline across the layer graph), powering the graph-traversal queries P-31 uses. Differentiator: layer-indexed (not interval-indexed like U-A; not anchor-immutability-indexed like U-C; not FC-commitment-indexed like D7-U-1). Per-layer semantics — `change-rate` (slow at L0, fast at L4) and `escrow-policy` — are first-class envelope fields, preserving Brier pace-layer cadence in storage shape rather than reconstructing it at the application layer.

- **P-29 per-layer-boundary policy DSL.** Framework: [ADR 0030](../../../docs/adr/0030-p-29-policy-mediator.md) records the substrate decision (OPA Rego primary; Cedar alternate; content-addressed bundles with `audit_envelope`-replayable verdicts) shared across three contested variants. U-B variant: [ADR 0056](../../../docs/adr/0056-p-29-variant-u-b-layer-boundary.md) encodes U-B's vocabulary as a Rego bundle with one load-bearing predicate-family `layer_pair_closure(parent_layer, child_layer, escrow_policy)` and one rule per `(parent_layer, child_layer)` pair. For each Lᵢ → Lᵢ₊₁ pair (L0→L1, L1→L2, L2→L3, L3→L4), the Rego policy encodes the upstream layer's `escrow-policy` field as a closure condition: the downstream-layer object cannot materialise until the upstream's declared boundary checks have satisfying records — cost-ceiling per D-5; holdout-discipline per D-4 at L3→L4; cross-family contradiction-detection at L2→L3; AILCCP delegation-level confirmation at L0→L1 and L1→L2. The verdict's `reasons[]` entries are typed `{layer_pair, check_id, upstream_record_ref}` so handback routing is mechanical — Patrol and the calling primitive route the operator back to the correct upstream layer.

**Orphan substrate (single-candidate primitive):**

- **P-31 cross-layer drift detector.** [ADR 0054](../../../docs/adr/0054-p-31-cross-layer-drift-detector.md) records U-B's orphan: a per-layer-pair invariant registry layered on the ADR 0029 P-28 substrate with envelope kind `LayerPairInvariant{layer-pair, invariant-id, construction-shape ∈ {OPA-Rego, Postgres-CTE, property-test, LLM-judge-hybrid}, corpus-citation, severity-default, recommended-handback-layer}`. The invariant evaluator runs at per-cycle boundaries (Patrol cadence; any commit to an L0–L3 typed object; any L4 builder cycle touching a symbol P-23 (ADR 0031) traces to an upper-layer invariant tag); it reads typed-object snapshots via the ADR 0055 envelope and emits `LayerDriftEvent{layer-pair, invariant-id, drifted-artifact-handle, severity, recommended-handback-layer}` to the ADR 0030/0056 P-29 policy mediator, which converts the event into an operator handback at the appropriate layer-transition escrow interval through closure evaluation. The registry seeds with the **Wave 4.5 verified 20 invariants** (≥15 target met) across L0↔L1, L1↔L2, L2↔L3, L3↔L4, and the long-distance L0↔L4 pair per [u-b-invariant-authoring.md](../sub-tracks/u-b-invariant-authoring.md). Construction-C *hybrid* is the canonical composition rule: deterministic OPA + Postgres CTE + property tests for declared-invariant arms; LLM-judge residue (via P-14 cross-family panel) only for substance-check arms (notably L0↔L4 runtime-mode shape) — judge verdicts are advisory, never deterministic, with explicit confidence thresholds and cross-family panel composition. Per [u-b.md §2 (b) accept-as-RG flag](../substrate-requirements/u-b.md), the L0↔L4 judge-arm carries research-grade-uncertainty inheritance (Larbi MCC ≤ 0.55 for LLM-as-judge); the deterministic-reachability arm alone is non-trivial (see [Wave 4.5 invariant L0-L4-2 verbatim five-category coverage](../sub-tracks/u-b-invariant-authoring.md#5-l0--l4--standards--code-long-distance--anchor-to-implementation) — the fully-deterministic counterpart to the judge-arm).

**Commodity substrate baseline.** [P-01 sandbox](../../../docs/adr/0010-p-01-sandbox-runtime.md), [P-02 cost ceilings](../../../docs/adr/0011-p-02-cost-ceilings.md), [P-05 trajectory capture](../../../docs/adr/0012-p-05-trajectory-capture.md), [P-06 watchdog tiers](../../../docs/adr/0013-p-06-watchdog-tiers.md), [P-07 telemetry](../../../docs/adr/0014-p-07-telemetry-ingestor.md), [P-08 scenario storage](../../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md), [P-14 judge router](../../../docs/adr/0016-p-14-judge-router.md), [P-22 polyglot index](../../../docs/adr/0017-p-22-polyglot-codebase-index.md), [P-23 dependency-impact graph](../../../docs/adr/0031-p-23-dependency-impact-graph.md). U-B's per-layer routing pattern on P-14 (per the [P-14 sketch §U-B](../primitives/P-14-judge-router.md): layer-aware multi-shape dispatch — L0/L1 long-context + diverse families; L2→L3 cross-family contradiction-detection; L4 provider-aligned coding agents) is a methodology-layer configuration over the commodity P-14 substrate, not a per-variant ADR claim. P-06 is the Patrol-tier monitoring substrate for cross-layer drift distribution (downstream of P-31 LayerDriftEvent emissions); P-23 is the trigger surface for L3↔L4 expected-touch closure (the [Wave 4.5 invariant L3-L4-1 touched-symbol containment check](../sub-tracks/u-b-invariant-authoring.md#4-l3--l4--plan--code)). P-12 deterministic linter framework is **not** carried as a U-B substrate primitive — the L2 vocabulary-lint discipline (Wave 4.5 invariant L2-L3-3) is encoded directly as a P-31 invariant on the existing P-28 store, not as a separate substrate primitive.

**X_UNM_B brownfield Codebase-Model acquisition** (per [u-b.md §4](../substrate-requirements/u-b.md)). For brownfield deployments, U-B reads L4 code as the entry artifact and performs bottom-up inference of L3 plan / L2 spec / L1 architecture / L0 standards through P-22 (polyglot codebase index) + P-23 (dependency-and-impact graph) + ADR archaeology of any preserved historical documents. Inherited regulatory commitments (F58) seed L0 directly. The **completeness gap** is honest: L0/L1/L2 reconstruction from L4 is fundamentally lossy — L0 standards (regulatory commitments, AILCCP control declarations, Caremark RSI three-part test status) are not derivable from code, they are extrinsic governance artifacts; only the *implementation tags* of L0 commitments are recoverable (when preserved as `@implements-AILCCP("...")` annotations — the very thing U-B's L0↔L4 invariant L0-L4-1 *checks*, not produces). If upward inference fails or produces low-confidence outputs for L0/L1, U-B degrades to greenfield-only: the candidate honestly cannot serve the brownfield mandate. The degradation does not invalidate U-B's unified claim because the candidate explicitly does not claim global UC4-resolution per [unified-B §6](../tracks/unified-B.md#6-what-this-track-is-not-trying-to-be) (*"PLEF's bottom-up traversal is competent at brownfield, not optimal"*).

## §3 Methodology shape

**Per-cycle loop.** Generic and layer-typed. Each cycle:

1. **Work-unit declaration.** Agent (or operator) declares a typed work unit naming its target pace-layer Lᵢ.
2. **Layer-typed envelope construction.** The cycle's typed object is constructed against the ADR 0055 schema: `TypedObject<L=Lᵢ>{layer, change-rate, escrow-policy, invariants[], parent-layer-ref, child-layer-refs[]}`. The `parent-layer-ref` points (content-hash) at the Lᵢ₋₁ object that authorised the cycle; `child-layer-refs[]` accumulates as downstream cycles fan out.
3. **Layer-pair gate evaluation.** [ADR 0056](../../../docs/adr/0056-p-29-variant-u-b-layer-boundary.md)'s `layer_pair_closure(parent_layer, child_layer, escrow_policy)` predicate evaluates against the ADR 0030 P-29 substrate engine. The verdict is binding: the downstream-layer object refuses to materialise unless `allow == true`. Reasons-typed handback routes the operator to the correct upstream layer.
4. **Cycle execution.** Per the dispatched layer:
   - **L4 (code)** is L4-Automation in Jaymin's frame: builder agents run autonomously; cross-model review (Wave 4.5 invariant L3-L4-2; F46 mitigation) supplies judge-independence; P-23-traced touched-symbol containment (L3-L4-1) caps blast radius; lethal-trifecta default-off (L3-L4-3) caps F44.
   - **L0–L3 transitions** are L3-Augmentation with structural escrow at each P-29 layer boundary (not voluntary discipline — the F53 antidote).
   - **L5 ("no human ever")** is rejected by construction: every layer transition is a structural P-29 gate.
5. **Cross-layer drift evaluation.** [ADR 0054 P-31](../../../docs/adr/0054-p-31-cross-layer-drift-detector.md) evaluates the per-layer-pair invariant catalog (Wave 4.5: 20 invariants across L0↔L1, L1↔L2, L2↔L3, L3↔L4, L0↔L4) against the current and parent typed objects; any drift emits `LayerDriftEvent` to P-06 Patrol and to the U-B methodology-layer escrow primitive.
6. **Trajectory write.** [P-05 (ADR 0012)](../../../docs/adr/0012-p-05-trajectory-capture.md) appends the cycle event with the layer tag in the payload — Patrol monitors the empirical cross-layer drift distribution and the per-layer-pair invariant fire-rate.

**Layer structure** (per [unified-B §1](../tracks/unified-B.md)). Five pace-layers (Brier convention): L0 Standards (months–years; AILCCP/INCOSE/EARS/Caremark seeds) / L1 Architecture (weeks–months; ADR + dependency graph) / L2 Spec (days–weeks; EARS-typed + GtWR-linted intent block) / L3 Plan (hours–days; chunk-load-ceiling decomposition) / L4 Code (minutes–hours; sandboxed builder cycles). Layer-count is empirically picked at 5 per Brier; OQ-PLEF-1 is the open carry (§6).

**Work-unit definition.** A *layer-typed proposed change* whose target layer is named explicitly. Both Atelier-style issue work units and Refinery-style change-request work units are representable; the dispatcher is layer-direction-agnostic. The unit-of-work cost ceiling is per-layer ([P-02 (ADR 0011)](../../../docs/adr/0011-p-02-cost-ceilings.md); CTR-E1 variance handled per-layer not flat per [unified-B §4 D-5](../tracks/unified-B.md)): L4 code cycles have low ceilings; L0 standards revision cycles have the highest.

**Distinctive methodology decisions.** Three:

- **Layer typing is a substrate property, not a methodology convention.** The `layer` field is in the content-hash preimage (ADR 0055) — silent layer mis-tagging is structurally impossible. Per-layer escrow-policy lives on the envelope, not on a sidecar.

- **Day-0 → day-N trajectory is a top-down layer-seeding cadence, not a calendar date.** Per [unified-B §5](../tracks/unified-B.md): at cold-start (greenfield), L0 standards are seeded from priors (AILCCP 48 controls; INCOSE GtWR v4; EARS grammar; Caremark/SB-53 framework) and never start empty; L1 Pareto-sketched from L0 constraints; L2 from the El Kaim 9-field intent block; L3 chunks ≤5 requirements (Wave 4.5 invariant L2-L3-1 cold-start parameter); L4 builders fire only against seeded upper layers. Day-0 to Day-7 fires L4 against seeded upper surfaces; Day-7 to Day-30 the knowledge store accumulates layer-tagged events; Day-30+ steady-state per-layer thresholds calibrated against measured performance.

- **Methodology layer takes no opinion on coordination medium.** GitHub-issues vs commit-message vs mail-bus is methodology-layer detail orthogonal to substrate. U-B is agnostic; deployment chooses (per [unified-B §1 coordination medium](../tracks/unified-B.md)).

**Brownfield traversal direction.** Bottom-up: L4 (existing code) → L3 (inferred plan via P-23 trace analysis) → L2 (inferred delta-spec) → L1 (inferred architecture via P-22 + P-23) → L0 (inherited standards). The architecture is `given` because the inference step pins L1 before any new work fires at L4. The completeness gap per [u-b.md §4](../substrate-requirements/u-b.md) is honest: bottom-up inference is competent at brownfield, not optimal.

## §4 Discipline binding

U-B binds all 10 discipline ADRs (0018-0027). Per-discipline binding:

- **Bias guard ([ADR 0018](../../../docs/adr/0018-discipline-bias-guard.md)).** Bound at the L2→L3 P-29 gate: cross-family contradiction-detection (Wave 4.5 invariant L2-L3-2) enforces model-family diversity (F46 mitigation). Bound at the L3→L4 gate: cross-model review (Wave 4.5 invariant L3-L4-2) requires `reviewer-model-family ≠ builder-model-family` per the Hess `kevin/carl` pattern.

- **Cognitive escrow ([ADR 0019](../../../docs/adr/0019-discipline-cognitive-escrow.md)).** Methodology-layer per [DEC-2](../phase-3.4-decisions-resolved.md#dec-2--cognitive-escrow-placement-methodology). Bound at every P-29 layer-boundary gate (ADR 0056) — each Lᵢ→Lᵢ₊₁ transition is itself an escrow interval; the substrate triggers the structural reflection-question/success-criterion/similar-past-transition surfacing at boundary time rather than relying on voluntary operator discipline (F53 antidote).

- **Cost ceiling ([ADR 0020](../../../docs/adr/0020-discipline-cost-ceiling.md)).** Bound at [P-02 (ADR 0011)](../../../docs/adr/0011-p-02-cost-ceilings.md) with per-layer parameterisation per [unified-B §4 D-5](../tracks/unified-B.md). Wave 4.5 invariant L3-L4-4 enforces `BuilderCycle.actual_compute_tokens ≤ PlanChunk.compute_ceiling_tokens` (the per-chunk ceiling is set by L3 per D-5 hard-cost-ceiling discipline; per-layer-not-flat).

- **Holdout ([ADR 0021](../../../docs/adr/0021-discipline-holdout.md)).** Bound at [P-08 (ADR 0015)](../../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md) — scenarios live at layer-appropriate locations per [unified-B §4 D-2](../tracks/unified-B.md). The L3→L4 P-29 gate (ADR 0056) requires `holdout_discipline_satisfied(policy.holdout_records, input.candidate)` — substrate-enforced, not voluntary.

- **Honesty ([ADR 0022](../../../docs/adr/0022-discipline-honesty.md)).** Bound at the X_UNM_B completeness gap (§2): U-B declares the brownfield bottom-up inference is fundamentally lossy and degrades to greenfield-only rather than overclaiming. Honest carve-out: OQ-PLEF-5 (operator engagement with substrate-fired escrow prompts is itself voluntary) is named as a Phase-3 adversarial carry, not silently waved off.

- **Knowledge promotion ([ADR 0023](../../../docs/adr/0023-discipline-knowledge-promotion.md)).** Bound at the pace-layer cadence: lower-layer patterns promote upward through the layer graph (L4 emergent → L3 chunk pattern → L2 spec refinement → L1 architecture rule → L0 standard). Promotion is itself a P-29-gated layer-pair transition (always upward, always with the full layer-boundary closure).

- **Regime classification ([ADR 0024](../../../docs/adr/0024-discipline-regime-classification.md)).** Bound at the per-layer-pair P-31 invariant catalog: each layer-pair has its own invariant set with severity defaults and recommended handback layers. U-B does NOT carry P-19 (eligibility classifier) — the per-layer-pair invariant catalog is the regime-classification surface, not an eligibility classifier.

- **Scoping ([ADR 0025](../../../docs/adr/0025-discipline-scoping.md)).** Bound at the [P-29 layer-boundary gate (ADR 0056)](../../../docs/adr/0056-p-29-variant-u-b-layer-boundary.md): work-unit scope is bounded by the target layer's `escrow-policy` field. No mandate-specific scoping; traversal direction parameterises mandate.

- **Three-loop ([ADR 0026](../../../docs/adr/0026-discipline-three-loop.md)).** Bound at the Compound Engineering plan→work→review→compound loop applied per-layer. The "compound" step is materialised as P-06 Patrol-tier monitoring of the cross-layer drift distribution (downstream of P-31 emissions) — meta-loop closure is substrate-enforced.

- **Trifecta closure ([ADR 0027](../../../docs/adr/0027-discipline-trifecta-closure.md)).** Bound at [P-08 (ADR 0015)](../../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md) holdout + Wave 4.5 invariant L3-L4-3 (Lethal-Trifecta prohibition on builder-cycle effects per Shapiro R1+R3; substrate-default off per F44). The trifecta-justification requires an L3 PlanChunk signature per the AILCCP Human Approval Gate.

**Disciplines U-B is silent on.** None — U-B carries all 10. The honest-carve-out on OQ-PLEF-5 (operator response to substrate-fired prompts) and OQ-PLEF-8 (own F52 risk) is carried to Phase 8 lean-eval, not used to demote disciplines.

## §5 Mandate fit

U-B's mandate-fit YAML block (in this spec's frontmatter) restated per work-unit-class:

- **initial-spec: both.** Initial-spec authoring at L2 fires against the El Kaim 9-field intent block, regardless of mandate. Greenfield: L2 spec is constructed against seeded L0/L1. Brownfield: L2 spec is the *delta-spec* against the running system inferred from L4 (per [u-b.md §4 X_UNM_B](../substrate-requirements/u-b.md)). Supporting substrate evidence: ADR 0055 (L2 envelope schema); ADR 0056 (L1→L2 gate); Wave 4.5 invariants L1-L2-2/L1-L2-3 (prohibited-action coverage + evidence-obligation trace). Falsifying scenario: if brownfield initial-spec authoring requires fundamentally different substrate primitives than greenfield (e.g., a separate inference engine not reducible to P-22 + P-23 + ADR-archaeology), the unified claim collapses.

- **refactor: both.** Refactoring is naturally layer-typed — the proposed change's target layer determines the gate set. Greenfield refactor (against an L1 architecture rule): the rule was Pareto-sketched from L0; refactor is L1→L2 traversal under the existing L0 envelope. Brownfield refactor (against inferred L1 + existing L4): the inference step pins L1 first; refactor is then L2 delta-spec → L3 plan → L4 code. Supporting substrate evidence: ADR 0054 P-31 (cross-layer drift detection during refactor); ADR 0056 (per-layer gates). Falsifying scenario: if refactor cycles land at indistinguishable layer-pair distributions on greenfield vs brownfield with identical gate fire-rates, the mandate-as-parameter claim is wrong.

- **mvp: greenfield.** MVP authoring (greenfield-typical) operates against the seeded L0/L1/L2 stack from priors; L3 plan chunks ≤5 requirements at cold-start per [unified-B §5.6](../tracks/unified-B.md). Falsifying scenario: if MVP work units never accumulate enough lower-layer artifacts to leave the L4-by-construction cold-start regime, U-B's earned-steady-state claim is wrong. Brownfield MVP is not a canonical U-B work-unit-class (MVP presupposes greenfield-leaning evolution); U-B does not claim it.

- **post-mvp-evolution: both.** Post-MVP cycles operate against an accumulated typed-object graph on either mandate. Greenfield: seeded upper layers + accumulated L2/L3/L4 artifacts. Brownfield: inferred upper layers + delta-spec work at L2. Supporting substrate evidence: ADR 0055 (envelope) and ADR 0056 (gate) are uniform across mandates. Falsifying scenario: if post-MVP cycles on brownfield require fundamentally different layer-pair gates than on greenfield, the unified claim collapses.

- **regression-fix: both.** Regression fixes are by construction L4 cycles whose `expected-touch[]` field is narrowly scoped to the failing test's call-graph closure (Wave 4.5 invariant L3-L4-1). Substrate evidence: ADR 0054 P-31 (regression that drifts cross-layer fires immediately); ADR 0021 holdout discipline at L3→L4. Falsifying scenario: if regression-fix cycles routinely require L0/L1 traversal rather than L3/L4-bounded fixes, regression-as-L4-bounded is wrong.

**DEC-1.a falsifier-discipline observation.** U-B explicitly claims `both` on 4 of 5 work-unit-classes (initial-spec, refactor, post-mvp-evolution, regression-fix). Per [DEC-1.a](../decisions-captured.md#d1--unification-verdict-no-methodology-serves-both-mandates-working-hypothesis-falsifiable-by-phase-8), this is evidence weighing against the no-methodology-serves-both-mandates working hypothesis — but qualified by U-B's honest X_UNM_B completeness-gap declaration (§2) which surfaces brownfield lossiness rather than papering over it. The Phase-8 lean-eval will pressure-test these `both` claims against the completeness gap.

## §6 Open carries

Surfaced into Phase 7 (back-fill) / Phase 8 (lean-eval) / future ADRs per [u-b.md §5](../substrate-requirements/u-b.md):

- **OQ-PLEF-1 layer-count migration (Phase-5 ADR seed (i)).** Per [ADR 0055 § Consequences](../../../docs/adr/0055-p-28-variant-u-b-layer-typed-envelope.md): adding or removing a pace-layer changes the envelope's `layer` enum and requires a migration discipline. Layer-count is empirical (Brier asserts 5; El Kaim implies more spec-internal layers; the right number is open). **Status: Phase-5 ADR seed; deferred.**

- **OQ-PLEF-3 multi-cycle population drift (Phase-5 ADR or accept-as-RG).** Per [ADR 0054 § Consequences](../../../docs/adr/0054-p-31-cross-layer-drift-detector.md): Wave 4.5 invariants are per-cycle snapshots; population-scale drift (F48 tacit collusion across multiple PLEF instances) is not yet substrate-detectable. **Status: Phase-5 ADR seed or accept-as-RG at Phase 4 close.**

- **L0↔L4 judge-arm research-grade-uncertainty inheritance (accept-as-RG with carry-from-smoke-test caveat).** Per [u-b.md §2 (b)](../substrate-requirements/u-b.md): the substantive runtime-mode shape-match arm of L0-L4-1 leans on LLM-judge (Larbi MCC ≤ 0.55); P-31 Construction-C hybrid contains the residue behind cross-family confidence threshold but does not eliminate it. Wave 4.5 invariant L0-L4-2 (deterministic five-category coverage) is the deterministic counterpart. **Status: accept-as-RG; Phase 8 pressure-tests judge-arm reliability on a held-out drift corpus.**

- **OQ-PLEF-8 own F52 (Tempting-Wrong-Hybrid) risk (Phase-3 adversarial carry — open).** Per [unified-B §7 OQ-PLEF-8](../tracks/unified-B.md): the multi-layer escrow stack could itself be an F52 instance — deterministic structure imposed around stochastic agents. U-B's defense is that the P-29 layer-pair gates are *human-attention surfaces* not deterministic LLM-wrappers, but adversarial review should test this. **Status: Phase-3 adversarial pass carry — open.**

- **OQ-PLEF-5 voluntary-discipline-fragility at operator response (Phase-3 adversarial carry — open).** U-B moves discipline from operator-voluntary to substrate-triggered, but the operator's response to the escrow primitive (do they read the reflection question? articulate the success criterion?) is itself voluntary. F53 may have a stronger reading than U-B addresses. **Status: Phase-3 adversarial pass carry.**

- **Wave-4.5 invariant catalog evolution as L0 evolves (Phase-8 lean-eval candidate).** Per [ADR 0054 § Consequences](../../../docs/adr/0054-p-31-cross-layer-drift-detector.md): maintaining the invariant registry as L0 standards evolve is a per-cycle methodology obligation. Wave 4.5 produced 20 invariants exceeding the ≥15 target; per-invariant precision/recall on a held-out drift corpus + cross-invariant correlation are Phase-8 work.

- **Brier metaphor-swap not adopted (Phase-3 adversarial pass carry — closed-with-justification).** Per [unified-B §6](../tracks/unified-B.md#6-what-this-track-is-not-trying-to-be): U-B uses Brier's *layering* without his *metaphor reframe* (CTR-F1 not adopted; the artifact remains a factory per UC1 nomenclature). Not load-bearing for the spec.

## §7 References

**ADR set (this spec's binding inputs).** Per the §0 ADR-citation index above; relative paths under `../../../docs/adr/`:

- Common substrate: [ADR 0010](../../../docs/adr/0010-p-01-sandbox-runtime.md), [ADR 0011](../../../docs/adr/0011-p-02-cost-ceilings.md), [ADR 0012](../../../docs/adr/0012-p-05-trajectory-capture.md), [ADR 0013](../../../docs/adr/0013-p-06-watchdog-tiers.md), [ADR 0014](../../../docs/adr/0014-p-07-telemetry-ingestor.md), [ADR 0015](../../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md), [ADR 0016](../../../docs/adr/0016-p-14-judge-router.md), [ADR 0017](../../../docs/adr/0017-p-22-polyglot-codebase-index.md), [ADR 0031](../../../docs/adr/0031-p-23-dependency-impact-graph.md).
- Framework substrate: [ADR 0029 (P-28 framework)](../../../docs/adr/0029-p-28-typed-object-store.md), [ADR 0030 (P-29 framework)](../../../docs/adr/0030-p-29-policy-mediator.md).
- Per-variant substrate (U-B-specific): [ADR 0055 (U-B P-28 layer-typed envelope)](../../../docs/adr/0055-p-28-variant-u-b-layer-typed-envelope.md), [ADR 0056 (U-B P-29 layer-boundary policy DSL)](../../../docs/adr/0056-p-29-variant-u-b-layer-boundary.md).
- Orphan substrate: [ADR 0054 (P-31 cross-layer drift detector)](../../../docs/adr/0054-p-31-cross-layer-drift-detector.md).
- Discipline: [ADR 0018](../../../docs/adr/0018-discipline-bias-guard.md), [ADR 0019](../../../docs/adr/0019-discipline-cognitive-escrow.md), [ADR 0020](../../../docs/adr/0020-discipline-cost-ceiling.md), [ADR 0021](../../../docs/adr/0021-discipline-holdout.md), [ADR 0022](../../../docs/adr/0022-discipline-honesty.md), [ADR 0023](../../../docs/adr/0023-discipline-knowledge-promotion.md), [ADR 0024](../../../docs/adr/0024-discipline-regime-classification.md), [ADR 0025](../../../docs/adr/0025-discipline-scoping.md), [ADR 0026](../../../docs/adr/0026-discipline-three-loop.md), [ADR 0027](../../../docs/adr/0027-discipline-trifecta-closure.md).

**Supporting docs:**

- [U-B candidate-registry entry](../candidate-registry.md#u-b--pace-layered-escrow-factory-5-layer-artifact-stack-with-bidirectional-traversal)
- [U-B substrate-requirements summary](../substrate-requirements/u-b.md)
- [Unified-B track sketch](../tracks/unified-B.md)
- [U-B invariant-authoring sub-track (Wave 4.5; 20 invariants ≥15 target)](../sub-tracks/u-b-invariant-authoring.md)
- [Phase-4.2 overlap.md P-28 verdict](../primitives/overlap.md#p-28-typed-object-store--four-contested-variants)
- [Phase-4.2 overlap.md P-29 verdict](../primitives/overlap.md#p-29-policy-mediator--compounding-gate--three-contested-variants)
- [P-31 smoke-test invariants (5/5 non-trivial)](../primitives/P-31-smoke-test-invariants.md)
- [DEC-1.a unification-verdict working hypothesis](../decisions-captured.md#d1--unification-verdict-no-methodology-serves-both-mandates-working-hypothesis-falsifiable-by-phase-8)
- [DEC-2 cognitive-escrow placement (methodology)](../phase-3.4-decisions-resolved.md#dec-2--cognitive-escrow-placement-methodology)
- [auto-002 Round 2 (U-B path)](../decisions/auto-002-ub-path.md) — smoke-test verdict logic and full sub-track authorization
- [auto-006 Phase-6 dispatch-shape brief](../decisions/auto-006-phase-6-dispatch-shape.md) — this spec is authored under its Round-2 rubric.
