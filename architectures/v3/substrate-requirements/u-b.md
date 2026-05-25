# Substrate requirements — U-B (Unified-attempt, Pace-Layered Escrow Factory)

**Candidate.** [U-B — Pace-Layered Escrow Factory (5-layer artifact stack with bidirectional traversal)](../tracks/unified-B.md). Mandate: unified-attempt. Axis: pace-layer × bidirectional traversal (per [registry §U-B](../candidate-registry.md#u-b--pace-layered-escrow-factory-5-layer-artifact-stack-with-bidirectional-traversal)).

**Phase-3.5.5 status.** `survives with deferred-defense flag` (per [registry §U-B post-smoke-test](../candidate-registry.md#u-b--pace-layered-escrow-factory)). The Phase-3.5 follow-up smoke-test [`P-31-smoke-test-invariants.md`](../primitives/P-31-smoke-test-invariants.md) produced 5/5 non-trivial cross-layer invariants per [`auto-002` Round 2](../decisions/auto-002-ub-path.md). Forward action: full Phase-4 invariant-authoring sub-track authorized (Wave 4.5 — see §5).

## §1 Primitive list (buildability-confirmed)

U-B requires 4 substrate primitives (cognitive-escrow demoted to methodology-layer per [DEC-2](../phase-3.4-decisions-resolved.md#dec-2--cognitive-escrow-placement-methodology); not listed here).

- **[P-28 — Typed-object store (layer-typed envelope variant)](../primitives/P-28-typed-object-store.md).** Store keyed on `layer` ∈ {L0 Standards, L1 Architecture, L2 Spec, L3 Plan, L4 Code} with the `TypedObject<L>` envelope carrying `change-rate`, `escrow-policy`, `invariants[]`, `parent-layer-ref`, `child-layer-refs[]`. Layer-indexed (the differentiator vs U-A's interval-indexed variant). Verdict: `designed-system`; same-vs-distinct vs other variants deferred to Phase 4.2.
- **[P-29 — Policy mediator / transition gates (per-layer-boundary variant)](../primitives/P-29-policy-mediator.md).** Gates each Lᵢ → Lᵢ₊₁ transition. Closure conditions encode the upstream layer's `escrow-policy` field; the mediator refuses to materialize the downstream object until the upstream's declared gate, log, judge-diversity, and watchdog-tier slots have satisfying records. Verdict: `designed-system`; same-vs-distinct vs U-A / D7-U-1 deferred to Phase 4.2.
- **[P-31 — Cross-layer drift detector](../primitives/P-31-cross-layer-drift-detector.md).** Holds typed-object snapshots and runs per-layer-pair invariant checks across L0↔L1, L1↔L2, L2↔L3, L3↔L4 plus the long-distance L0↔L4 anchor-to-implementation pair. Emits `LayerDriftEvent` to Patrol (P-06) and to U-B's methodology-layer escrow primitive. Load-bearing for F34 (cross-layer drift) per [unified-B §2.5](../tracks/unified-B.md). Verdict: `research-grade-uncertainty` — see §2.
- **[P-14 — Judge router (per-layer routing variant)](../primitives/P-14-judge-router.md).** Layer-aware multi-shape dispatch: L0/L1 long-context + diverse families; L2→L3 cross-family contradiction-detection; L4 provider-aligned coding agents. Verdict: `designed-system`. Not contested-fixed-header.

## §2 RG primitives

Per the [Phase-3.5.5 RG-primitive rule](../candidate-registry.md#phase-355-rule-on-load-bearing-rg-primitives-binding-user-approved-2026-05-25), U-B carries **two RG-portion entries** in the [Application to current candidates table](../candidate-registry.md#phase-355-rule-on-load-bearing-rg-primitives-binding-user-approved-2026-05-25). Both verbatim text-pulls per Reviewer 1 A3:

> | U-B | P-31 (full primitive) | (a) bounded sub-track | Smoke-test passed; full sub-track authorized at Phase 4 (scale 1-per-pair to ≥3-per-pair, ≥15 total) |

> | U-B | P-31 long-distance pair (L0↔L4 judge-arm) | (b) accept-as-RG (carry-from-smoke-test caveat) | The smoke-test's L0↔L4 invariant depends on LLM-judge for substance check; treated as accept-as-RG per the smoke-test's own caveat. Full sub-track explores whether deterministic alternatives exist; falls back to accept-as-RG if not. |

**Choice treatment per [auto-002 Round 2](../decisions/auto-002-ub-path.md).**

- **P-31 full primitive → (a) bounded sub-track.** The Phase-3.5 follow-up smoke-test produced 5/5 non-trivial invariants with verbatim corpus citations (L0↔L1 AILCCP three-controls coverage per Kahana 31; L1↔L2 `protects` linkage + binding-shape match per El Kaim Ch8; L2↔L3 chunk-load ceiling at Yang et al. F36 empirical 10-requirement bar; L3↔L4 expected-touch dependency-closure containment per F34; L0↔L4 AILCCP-control runtime-mode shape match per Kahana "trappings vs substance"). Per smoke-test verdict logic (≥4 of 5 → survives), the full Phase-4 invariant-authoring sub-track is **owed at Wave 4.5** (scale to ≥3 per pair, ≥15 total).

- **P-31 L0↔L4 judge-arm → (b) accept-as-RG.** The strongest corpus-anchored invariant (Kahana 31 §5 "trappings vs substance") leans on an LLM-judge arm bounded by F37/F51 (Larbi MCC ≤ 0.55). The deterministic-reachability arm alone is non-trivial; the substantive runtime-mode shape-match arm is research-grade. P-31's Construction-C hybrid (deterministic + judge residue via P-14 panel) is the right substrate but does not eliminate RG inheritance. Wave 4.5 explores deterministic alternatives; falls back to accept-as-RG if none.

## §3 Candidate-specific contracts on each primitive

U-B references two contested primitives (P-28, P-29) plus P-31 and P-14 (not contested-fixed-header).

- **P-28 layer-typed store.** envelope schema: `TypedObject<L>` per-pace-layer hierarchy with fields `{layer ∈ {L0 Standards, L1 Architecture, L2 Spec, L3 Plan, L4 Code}, change-rate, escrow-policy, invariants[], parent-layer-ref, child-layer-refs[]}` per [P-28 sketch § U-B layer-typed envelope](../primitives/P-28-typed-object-store.md). Typed filter keyed on `layer` first; the `(parent-layer-ref → child-layer-refs)` traversal is P-31's primary input axis. Differentiator: layer-indexed (not interval-indexed like U-A; not anchor-immutability-indexed like U-C; not FC-commitment-indexed like D7-U-1). Same-vs-distinct deferred to Phase 4.2.

- **P-29 transition gates.** policy DSL: per-layer-boundary closure rules. For each Lᵢ → Lᵢ₊₁ pair, the Rego policy encodes the upstream layer's `escrow-policy` field as a closure condition: the downstream-layer object cannot materialize until the upstream's declared boundary checks (cost-ceiling per D-5; holdout-discipline per D-4 at L3→L4; cross-family contradiction-detection at L2→L3; AILCCP delegation-level confirmation at L0→L1 and L1→L2) have satisfying records. Differentiator: per-layer-boundary DSL (not interval-closure DSL like U-A; not FC-survival DSL like D7-U-1). Same-vs-distinct deferred to Phase 4.2.

- **P-31 cross-layer drift detector.** No fixed contested-primitive header — U-B is the sole claimant. Contract: reads the P-28 layer-typed store via layer-pair queries, evaluates per-layer-pair invariants (catalog is the Wave 4.5 deliverable), emits `LayerDriftEvent{layer-pair, invariant-id, drifted-artifact-handle, severity, recommended-handback-layer}` to Patrol and to the U-B methodology-layer escrow primitive. Construction-C hybrid per [P-31 sketch](../primitives/P-31-cross-layer-drift-detector.md): deterministic OPA + Postgres CTE + property tests for declared-invariant arms; LLM-judge residue via P-14 for substance-check arms (F37 unreliability inheritance per §2).

- **P-14 per-layer judge router.** No fixed contested-primitive header. Layer-aware routing is U-B's contract per [P-14 sketch § U-B](../primitives/P-14-judge-router.md): per-layer provider-property requirements as a registry.

## §4 X_UNM_B articulation

Per the [X_UNM_B finding](../candidate-registry.md#u-a--escrow-graph-factory-cycle--directed-graph-of-typed-nodes), this candidate addresses Codebase-Model acquisition from legacy artifacts as follows:

- **Source artifact:** for brownfield, U-B reads L4 code as the entry artifact and performs bottom-up inference of L3 plan / L2 spec / L1 architecture / L0 standards through code analysis (per [unified-B §1 brownfield cycle](../tracks/unified-B.md): *"L4 (existing code) → L3 (inferred plan via trace analysis) → L2 (inferred delta-spec) → L1 (inferred existing architecture) → L0 (inherited standards)"*). Inherited regulatory commitments (F58) seed L0 directly.
- **Extraction primitive:** primarily **P-22 polyglot codebase index** + **P-23 dependency-and-impact graph** + **P-26 conventional view (CONDITIONAL on BF-L's smoke-test result)** + ADR archaeology of any preserved historical documents. P-22 indexes symbols; P-23 yields the structural skeleton for L1 architecture inference; P-26's conventional view (if BF-L's Wave-4.5 conventional-view smoke-test per [auto-003](../decisions/auto-003-bfl-rg-view-choice.md) authorizes its full sub-track) supplies idiomatic patterns for L2 spec inference. If BF-L's conventional view lands accept-as-RG, U-B inherits the same RG status for its L2 inference accuracy.
- **Completeness gap:** L0/L1/L2 reconstruction from L4 is **fundamentally lossy**. L0 standards (regulatory commitments, AILCCP control declarations, Caremark RSI three-part test status) are not derivable from code — they are extrinsic governance artifacts; only the *implementation tags* of L0 commitments are recoverable (and only when preserved as `@implements-AILCCP("...")` annotations — the very thing U-B's L0↔L4 invariant L0-L4-1 in [`P-31-smoke-test-invariants.md` §5](../primitives/P-31-smoke-test-invariants.md) would *check*, not produce). L1 inference recovers structural shape but not architectural-intent; L2 inference recovers behavioral surface from tests/types but not specification-intent (the El Kaim 9-field intent block is not in the code).
- **Fallback if missing:** if upward inference fails or produces low-confidence outputs for L0/L1, U-B degrades to **greenfield-only**: the candidate cannot serve the brownfield mandate. Honest accounting per [unified-B §6](../tracks/unified-B.md#6-what-this-track-is-not-trying-to-be) (*"PLEF's bottom-up traversal is competent at brownfield, not optimal"*). The degradation does not invalidate U-B's unified claim because the candidate explicitly does not claim global UC4-resolution.

## §5 Open carries

- **Phase-4-internal workstreams. U-B invariant-authoring sub-track — Wave 4.5 (OWED).** Per [auto-002 Round 2](../decisions/auto-002-ub-path.md) and [auto-004 Round 2 Wave 4.5](../decisions/auto-004-phase-4-dispatch-shape.md#wave-45-new-per-reviewer-2-a3): scale the [smoke-test recipe](../primitives/P-31-smoke-test-invariants.md) from 1-per-pair to ≥3-per-pair, ≥15 total. Smoke-test caveats (per [registry forward action](../candidate-registry.md#u-b--pace-layered-escrow-factory) and [smoke-test §6.3](../primitives/P-31-smoke-test-invariants.md)): (a) **sample-size bias toward 1-per-pair** — some pairs (notably L2↔L3 and L3↔L4) may not scale beyond 2 corpus-anchored invariants; (b) **L0↔L4 judge-arm RG inheritance** per §2; (c) **corpus concentration on AILCCP / EARS / El-Kaim-Ch8** — sub-track *permitted* to draw heavily on them, not required to source-diversify if that would mean fabrication; (d) **OQ-PLEF-3 multi-cycle population drift out of scope** for Wave 4.5; deferred to Phase 5 ADR or accept-as-RG at Phase 4 close. **Fallback rule:** if the full sub-track fails to scale to ≥3 per pair, fall back to the smoke-test's 1-per-pair set with explicit accept-RG flag on the substantive-drift portion.

- **Phase-5 ADR seeds.** (i) P-28 layer-typed envelope versioning under layer-count migration (OQ-PLEF-1); (ii) P-29 transition-gate policy-DSL choice (OPA vs Cedar; per-layer policy-bundle distribution); (iii) P-31 Construction-C composition rule (deterministic vs LLM-judge residue threshold; confidence-routing — touches the L0↔L4 accept-RG portion); (iv) P-14 per-layer routing registry shape.

- **Phase-8 lean-eval candidates.** (i) Wave-4.5 sub-track output pressure-test — MCC on a held-out drift corpus per [P-31 sketch §Falsifiability](../primitives/P-31-cross-layer-drift-detector.md); (ii) L0↔L4 judge-arm reliability under F37 (cross-family panel with confidence threshold); (iii) brownfield bottom-up inference accuracy under §4's completeness-gap — what fraction of L1/L2 inference loss can U-B detect-and-flag rather than silently fail-on?

## §6 Scoping-principle compliance

This summary preserves U-B as a defensible architecture proposal:

- All 4 substrate primitives carry forward; none pre-eliminated.
- The load-bearing RG primitive (P-31) is honestly surfaced with **both** its (a) bounded-sub-track and (b) accept-as-RG portions verbatim from the Phase-3.5.5 application table, and routed to Wave 4.5 with the smoke-test caveats. The 5/5 non-trivial-invariant result is the deferred-defense evidence; Wave 4.5 is the gate.
- The X_UNM_B completeness gap (§4) is honestly accounted: L0/L1/L2 reconstruction from L4 is fundamentally lossy, and U-B declares the greenfield-only degradation rather than overclaiming brownfield-fit.
- Open methodology questions (OQ-PLEF-1 layer-count, OQ-PLEF-8 own F52 risk, OQ-PLEF-3 multi-cycle drift) are routed to Phase-5 ADR / Phase-8 lean-eval / accept-as-RG rather than used to demote the candidate.
- Same-vs-distinct verdicts on P-28 / P-29 variants are deferred to Phase 4.2 per dispatch-brief constraint.

U-B survives Phase-4.1 with the deferred-defense flag intact. **Wave 4.5 invariant-authoring sub-track is the deferred-defense gate.**
