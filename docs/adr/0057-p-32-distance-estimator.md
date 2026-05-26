# ADR 0057: U-C P-32 distance estimator

- **Status**: Accepted
- **Date**: 2026-05-25
- **Deciders**: lead agent (Phase 5 Wave 5.3c2 subagent)

## Context

[U-C — Anchor-Distance Factory](../../architectures/v3/tracks/unified-C.md) is the only candidate that names **anchor-distance** as the substrate's first-class scalar: every work unit is parameterised by graph-distance to a load-bearing immutable anchor, and the L1–L4 mandate is parameterised by the anchor's `kind`. Per [U-C substrate-requirements §1](../../architectures/v3/substrate-requirements/u-c.md#1-primitive-list-buildability-confirmed), [P-32 distance estimator](../../architectures/v3/primitives/P-32-distance-estimator.md) is U-C's load-bearing primitive #2 — without it, the [P-19 distance-gated dispatcher](../../architectures/v3/primitives/P-19-eligibility-regime-classifier.md) has no features and the entire factory collapses to an undifferentiated L3 default.

The primitive sketch verdicts P-32 `designed-system` for construction, with a mandatory `research-grade-uncertainty` flag on (a) **calibration** — no corpus recipe maps weights and thresholds to operator-meaningful risk — and (b) **Goodhart resistance** of the `intent_field_touches` LLM-judged leg, which inherits [F33](../../architectures/v3/failure-modes-v3.md#f33--adversarial-prompt-defeat-of-llm-based-security-analysis) / [F51](../../architectures/v3/failure-modes-v3.md#f51--ashby-deficient-probabilistic-guard) vulnerability. Per the [Phase-3.5.5 RG-primitive rule](../../architectures/v3/candidate-registry.md#phase-355-rule-on-load-bearing-rg-primitives-binding-user-approved-2026-05-25), U-C accepts both flags routed to Phase 5/8 rather than carrying a bounded authoring sub-track.

This ADR records the **construction** decision (how the tuple is computed and how it composes over existing substrate primitives). The calibration recipe and the F33/F51 residual Patrol-detector spec are sibling ADR seeds named in [U-C §5](../../architectures/v3/substrate-requirements/u-c.md#5-open-carries) and deferred.

## Decision

**Build P-32 as a typed multi-component estimator producing a canonical `DistanceTuple{graph_distance, pace_layer_crossings, intent_field_touches, contradiction_flag}` from a frozen anchor set to a work unit, composed over three existing substrate primitives.** Each leg is constructed independently and the tuple is canonical at the substrate boundary; scalar aggregation under weights `(w_g, w_p, w_i)` is **dispatcher-local** to the P-19 variant, never substrate-baked.

- **`graph_distance` leg** is computed by a Glean Angle derived predicate (`derive python.Distance { source = W, target = A, hops = N } = path(W, A, references)`) reading the dependency edges already materialised by [ADR 0017 P-22 polyglot codebase index](0017-p-22-polyglot-codebase-index.md) (Glean fact-store) and [ADR 0031 P-23 dependency-and-impact graph](0031-p-23-dependency-impact-graph.md). The work unit's touched symbols come from `P-22.index.symbols_at(file, byte-range)`; the anchor's grounding symbols are carried at AnchorObject declaration time per [ADR 0029 P-28 typed-object store](0029-p-28-typed-object-store.md). Glean's derived-predicate compilation handles the BFS internally; the substrate reads `N` directly. Fully deterministic.
- **`pace_layer_crossings` leg** is a substrate decision table mapping (anchor `kind`, work-unit artifact-path) → Brier pace-layer ordinals 0–4, then `|layer(W) − layer(A)|`. The decision table is the same artifact [ADR 0028 P-19 eligibility/regime classifier](0028-p-19-eligibility-regime-classifier.md) uses for layer classification — one source of truth shared between primitives. Fully deterministic.
- **`intent_field_touches` leg** has two paths: a deterministic half using a stored `symbol → intent-field` map maintained as a [ADR 0048 P-13 maintenance-loop](0048-p-13-maintenance-loop.md) reconciliation artifact, and an LLM-judged fallback for unmapped symbols routed through P-14 against the El-Kaim 9-field intent block. The LLM half is the F33/F51-vulnerable leg.
- **`contradiction_flag`** is set when the diff implies anchor mutation; triggers a [F37](../../architectures/v3/failure-modes-v3.md#f37--silent-contradictory-prompt-collapse) hard-floor route to L4 regardless of composite.

The substrate exposes `(w_g, w_p, w_i, τ_low, τ_high)` as **versioned configuration** so the Phase-8 calibration sweep is tractable. The DistanceTuple is appended at write time to every [P-05 trajectory event](../../architectures/v3/primitives/cluster-C2.md) so the Patrol-tier P-06 watchdog can monitor the empirical distance distribution for [F47](../../architectures/v3/failure-modes-v3.md#f47--visible-metric-drift-goodhart-on-tokens) gaming.

The calibration metric is carried as a **Phase-8 lean-eval candidate**: historical-incident-to-distance regression plus operator-rated calibration sample, jointly correlated with the [Goodhart-resistance pressure-test](../../architectures/v3/substrate-requirements/u-c.md#5-open-carries) (lean-eval candidate (ii)).

## Alternatives considered

**B. Simple call-graph depth as a scalar distance.** A single integer — shortest call-graph path from work-unit symbol to anchor symbol, exactly the `graph_distance` leg. *Why rejected:* misses the two axes U-C's [§1 primitive #2](../../architectures/v3/tracks/unified-C.md) treats as load-bearing. Without `pace_layer_crossings`, a test-file change adjacent to an `intent-invariant` anchor reads as zero distance and routes lights-out — exactly the [F47](../../architectures/v3/failure-modes-v3.md#f47--visible-metric-drift-goodhart-on-tokens) failure the multi-component structure is designed to make harder. Without `intent_field_touches`, the dispatcher cannot see semantic anchor reach. Collapses U-C to a depth-gated variant of GF-S and forfeits the candidate's differentiating claim.

**C. LLM-judge end-to-end distance estimation.** A single P-14-routed judge call producing a real-valued distance per (work-unit, anchor) pair. *Why rejected:* non-deterministic on identical inputs (defeats the [anchor-based stability claim](../../architectures/v3/tracks/unified-C.md) that grounds U-C's regime gating), inherits F33/F51 on **every** dispatch decision rather than only the residual third leg, and offers no structural Goodhart resistance — the agent gaming surface is the entire output rather than two-of-three structurally-resistant legs plus one patrolled residual. Also forfeits Patrol-tier distribution monitoring: an LLM-judged scalar's drift is uninterpretable against a stable substrate distribution.

## Consequences

**Easier:** P-32 reuses substrate primitives already verdicted `designed-system` with High registry confidence ([P-22](../../architectures/v3/primitives/P-22-polyglot-codebase-index.md), [P-23](../../architectures/v3/primitives/P-23-dependency-impact-graph.md)). The Glean Angle realisation is named-tool concrete. Two of three legs are deterministic; the third has a deterministic majority and a typed fallback. Phase-8 calibration sweep is parameter-tractable because `(w_g, w_p, w_i, τ_low, τ_high)` is versioned config.

**Harder:** Calibration is owed at Phase 5/8 — no corpus recipe exists, and the Phase-8 lean-eval is on the critical path for operator-legibility (U-C OQ-5). The F33/F51 residual on the LLM-judged third leg is accepted-open with a Patrol-tier detector spec also owed at Phase 5. Brownfield deployments without an authored intent block degrade `intent_field_touches` to operator-attested per [U-C §4 fallback](../../architectures/v3/substrate-requirements/u-c.md#4-x_unm_b-articulation).

**Explicitly NOT promising:** closure of [F47](../../architectures/v3/failure-modes-v3.md#f47--visible-metric-drift-goodhart-on-tokens). The multi-component structure reduces the gameable surface from three legs to one-plus-patrol, not zero. Phase-8 pressure-test verdict is the gate.

## References

- [P-32 primitive sketch](../../architectures/v3/primitives/P-32-distance-estimator.md), including [§ Calibration uncertainty](../../architectures/v3/primitives/P-32-distance-estimator.md#calibration-uncertainty) and [§ Goodhart resistance](../../architectures/v3/primitives/P-32-distance-estimator.md#goodhart-resistance)
- [U-C substrate-requirements § P-32](../../architectures/v3/substrate-requirements/u-c.md#1-primitive-list-buildability-confirmed) and [§5 Phase-5 ADR seeds + Phase-8 lean-eval candidates](../../architectures/v3/substrate-requirements/u-c.md#5-open-carries)
- [ADR 0017: P-22 polyglot codebase index](0017-p-22-polyglot-codebase-index.md), [ADR 0031: P-23 dependency-and-impact graph](0031-p-23-dependency-impact-graph.md) — the upstream fact-store and graph this estimator composes over
- [ADR 0028: P-19 eligibility/regime classifier](0028-p-19-eligibility-regime-classifier.md) — the consumer of the DistanceTuple; pace-layer decision-table source of truth
- [F47 visible-metric drift](../../architectures/v3/failure-modes-v3.md#f47--visible-metric-drift-goodhart-on-tokens), [F33 adversarial-prompt defeat](../../architectures/v3/failure-modes-v3.md#f33--adversarial-prompt-defeat-of-llm-based-security-analysis), [F51 Ashby-deficient probabilistic guard](../../architectures/v3/failure-modes-v3.md#f51--ashby-deficient-probabilistic-guard), [F37 silent contradictory-prompt collapse](../../architectures/v3/failure-modes-v3.md#f37--silent-contradictory-prompt-collapse)
