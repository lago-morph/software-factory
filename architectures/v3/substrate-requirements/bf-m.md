# Substrate requirements — BF-M (Brownfield, methodology-first)

**Candidate.** [BF-M — Brownfield, methodology-first](../tracks/brownfield-methodology-first.md). Mandate: brownfield. Axis: methodology drives; the 8-stage per-cycle contract is the architecture; substrate primitives are stage-attached capabilities, not a pre-decided platform.

**Phase-3.5.5 status.** `survives` (per [registry §BF-M](../candidate-registry.md#bf-m--brownfield-methodology-first-1)). Forward action: stage-compression rules per work-unit-class need methodology-layer specification (own OQ-T1); P-27 brief-quality calibration carried to Phase 5/8; P-25 utility-tax acceptance criterion deferred to per-deployment measurement.

## §1 Primitive list (buildability-confirmed)

BF-M is a high-primitive-count candidate (~13 primitive references per the [coverage row](../primitives/index.md#per-candidate-primitive-coverage-round-trip-check); "~10 small" per the [registry summary table](../candidate-registry.md#summary-table-one-row-per-candidate)). Mostly commodity, with designed-system anchors at P-27 and P-25.

- **[P-01 — Sandbox runtime (deny-by-default)](../primitives/cluster-C1.md).** Per-cycle isolated execution at stage 5 (Build). Verdict: `commodity`.
- **[P-02 — Cost ceilings (hard, multi-axis)](../primitives/cluster-C1.md).** Per-cycle / per-work-unit-class budget caps (D-5). Verdict: `commodity`.
- **[P-03 — Worktree isolation](../primitives/cluster-C1.md).** Per-cycle isolated worktree at stage 5; F17 mitigation. Verdict: `commodity`.
- **[P-04 — PR creator](../primitives/cluster-C1.md).** Authenticated branch-push + structured-metadata PR open at stage 8. Verdict: `commodity`.
- **[P-05 — Trajectory capture](../primitives/cluster-C2.md).** D-7 trajectory store; per-cycle PR body carries a trajectory pointer (stage 8). Verdict: `commodity`.
- **[P-06 — Watchdog tiers (Daemon / Triage / Patrol)](../primitives/cluster-C2.md).** D-6 three-tier escalation: Daemon attaches to every stage; Triage at stages 4/5/6; Patrol across cycles for F34/F54/F55/F57 drift. Verdict: `commodity`.
- **[P-07 — Telemetry ingestor (per-role read filters)](../primitives/cluster-C2.md).** Stage-2 (Comprehension) runtime-telemetry read; per-role ABAC filter is load-bearing. Verdict: `designed-system` (escalated from commodity per the [post-sketch annotations](../primitives/index.md#post-sketch-annotations-running)).
- **[P-09 — Held-out scenario runner](../primitives/cluster-C3.md).** Stage 7 (Acceptance) replay of stored scenarios; pass/fail verdict. Possible P-08↔P-09 collapse evidence raised at cluster-C3 sketch time — deferred to Phase 4.2 per the [post-sketch annotations](../primitives/index.md#post-sketch-annotations-running). Verdict: `commodity`.
- **[P-12 — Deterministic linter framework](../primitives/cluster-C3.md).** Stage 6 (Cross-model review) deterministic-linter pass; F38 mitigation. Verdict: `commodity`.
- **[P-14 — Judge router (multi-shape typed)](../primitives/P-14-judge-router.md).** Stage 6 cross-family routing for the reviewer (F46 mitigation). Verdict: `designed-system`.
- **[P-22 — Polyglot codebase index](../primitives/P-22-polyglot-codebase-index.md).** Stage 2 code-traversal substrate (BF-M's "code-traversal tools"). Verdict: `designed-system`.
- **[P-25 — CaMeL-class typed perimeter](../primitives/P-25-camel-perimeter.md).** Stage 5 boundary when the work-unit-class is in a `production-adjacent` regime. Verdict: `designed-system` (calibration is partial-RG — see §2).
- **[P-27 — Archaeological-brief generation tooling](../primitives/P-27-archaeological-brief-tooling.md).** Stage 2 archaeological-brief generator + stage 7 codebase-derived scenario extractor (the [registry coverage row](../primitives/index.md#per-candidate-primitive-coverage-round-trip-check) names both uses against P-27). Verdict: `designed-system` (brief-quality calibration is partial-RG — see §2).

## §2 RG primitives

Per the [Phase-3.5.5 RG-primitive rule](../candidate-registry.md#phase-355-rule-on-load-bearing-rg-primitives-binding-user-approved-2026-05-25), BF-M carries **two partial-RG flags**. Neither is a full load-bearing RG primitive, and BF-M does NOT appear in the [Application to current candidates table](../candidate-registry.md#phase-355-rule-on-load-bearing-rg-primitives-binding-user-approved-2026-05-25) (which is reserved for U-B, BF-L, and D7-U-1's structurally-RG primitives). Both BF-M flags are calibration-style:

- **P-27 archaeological-brief tooling — brief-quality calibration partial-RG.** Per the [P-27 sketch](../primitives/P-27-archaeological-brief-tooling.md) and the [registry §BF-M material findings](../candidate-registry.md#bf-m--brownfield-methodology-first-1): brief-quality calibration is the load-bearing open problem (three plausible approaches sketched, none empirically validated). Construction (Pydantic v2 Brief schema + Anthropic/OpenAI structured outputs + tool-use loop over P-22) is `designed-system`; calibration is the open question.
  - **Choice:** (b) accept-as-RG on calibration. The substrate exposes brief-quality metrics and gating thresholds as first-class parameters so Phase-5/8 sweeps are tractable; the calibration is methodology-layer per-deployment work.

- **P-25 CaMeL utility-tax — calibration partial-RG.** Per the [P-25 sketch](../primitives/P-25-camel-perimeter.md) and [registry §BF-M](../candidate-registry.md#bf-m--brownfield-methodology-first-1): the ~7-point utility tax (CTR-E6) is not measurable a-priori; the substrate must expose per-class bypass with audit-log. Interacts with BF-M's OQ-T3.
  - **Choice:** (b) accept-as-RG on the utility-tax calibration. Construction (released CaMeL ref impl + OPA + eBPF) is `designed-system`; the acceptance criterion for the utility cost is Phase-5 ADR (production-adjacency policy) + Phase-8 lean-eval (realized tax measurement).

Both calibration RGs route to Phase-5/8 rather than a Phase-4 bounded sub-track because the open content is per-deployment measurement, not authoring of a missing artifact (unlike U-B's invariants or BF-L's conventional/invariant views).

## §3 Candidate-specific contracts on each primitive

BF-M's contracts on each primitive align with the per-primitive sketches' defaults; named deltas below. **BF-M does not name any of P-28, P-29, P-30, or P-19** (the contested-primitive set whose fixed sub-section headers were required by [auto-004 Round 2 §3](../decisions/auto-004-phase-4-dispatch-shape.md#wave-41-brief-shape-revised-per-reviewer-1-amendments)). It names P-14, which is not in the contested-fixed-header set. No fixed sub-section headers needed.

- **P-07 telemetry ingestor.** Stage-2 runtime-telemetry read with per-role ABAC filter; sketch default (OpenTelemetry Collector + ABAC integration) taken as-is. The CTR-B5/CTR-G2 inversion — telemetry-derived assertions feeding stage-7 scenarios via P-27 — is methodology-layer use, not a substrate-contract divergence.
- **P-09 held-out scenario runner.** Stage-7 deterministic replay of the codebase-derived scenario set with the *unseen subset* discipline (D-2 challenge — holdout is unseen, not out-of-tree). Sketch default preserved; partition discipline lives on P-08 (which BF-M names indirectly through P-09's read API; cluster-C3 sketch flagged the P-09→P-08 collapse honestly). Collapse verdict deferred to Phase 4.2.
- **P-14 judge router.** Stage-6 cross-family routing (F46). Sketch default (LiteLLM `Router` + Pydantic envelopes + cross-family tags) taken as-is. OQ-T2 (cross-model necessity) is methodology-layer, not substrate-contract.
- **P-22 polyglot codebase index.** Stage-2 code-traversal. BF-M takes the sketch's single-tenant tier (tree-sitter + per-language LSP federation + SQLite-FTS/DuckDB); Sourcegraph/SCIP fleet and Glean Meta-scale tiers available if deployment outgrows single-tenant. Cross-language type-resolution fidelity at RPC boundaries is the [sketch's named Phase-4 risk marker](../primitives/P-22-polyglot-codebase-index.md) — absorbed as known-cost.
- **P-25 CaMeL perimeter.** Stage-5 boundary for `production-adjacent` regimes. Sketch default (released CaMeL ref impl + OPA + eBPF) taken as-is. Utility-tax calibration is partial-RG per §2.
- **P-27 archaeological-brief tooling.** Dual-use — stage-2 archaeological-brief generator AND stage-7 codebase-derived scenario extractor (the [coverage row](../primitives/index.md#per-candidate-primitive-coverage-round-trip-check) names P-27 twice). The sketch defaults a tool-use loop over P-26's query interface; for BF-M (no P-26), the loop runs over P-22 + P-07 + P-24-equivalent attribution directly. Brief-quality calibration is partial-RG per §2.

## §4 X_UNM_B articulation

`N/A (mandate-specific candidate; X_UNM_B does not apply)`. BF-M is brownfield-only by deliberate construction (per [§6 of the track file](../tracks/brownfield-methodology-first.md#6-what-this-track-is-not-trying-to-be) — "Not a unified architecture"); its stage-2 Comprehension is the brownfield-defining stage and presumes the existing codebase + runtime as primary inputs.

## §5 Open carries

- **Phase-4-internal workstreams.** None owed at Wave 4.5 (BF-M carries no full load-bearing RG primitive requiring an authoring sub-track). The four named open questions (stage-compression rules per work-unit-class — own OQ-T1; cross-model review necessity under same-model-fine finding — own OQ-T2; CaMeL utility-tax acceptance criterion — own OQ-T3; scenarios-from-codebase governance — own OQ-T4, per [registry §BF-M open critique findings](../candidate-registry.md#bf-m--brownfield-methodology-first-1)) are all **methodology-layer** Phase-4/5/6 work, not Phase-4.1 substrate-authoring work.
- **Phase-4.2 deferred verdicts.** P-08↔P-09 collapse: BF-M names P-09 (held-out scenario runner) as a distinct primitive from P-08 (scenario storage), per the [registry coverage row](../primitives/index.md#per-candidate-primitive-coverage-round-trip-check). The cluster-C3 sketch raised the collapse evidence honestly; verdict deferred to Phase 4.2 per scoping principle. BF-M takes the deferral as-is.
- **Phase-5 ADR seeds.** (i) Stage-compression specification per work-unit-class (`regression-fix` skip vs collapse of stage 4; `codebase-evolution-proposal` stage 2-3-4 loop bound — own OQ-T1); (ii) Cross-family routing policy under CTR-D7/CTR-D8 (own OQ-T2 — whether cross-family is necessary or contingent); (iii) CaMeL production-adjacency policy boundary (own OQ-T3); (iv) Scenarios-from-codebase unseen-subset selection mechanism (own OQ-T4); (v) Anthropic Skills network-closure interaction with stage 2 / Patrol "dreaming" needs (own OQ-8 from the track file).
- **Phase-8 lean-eval candidates.** (i) P-27 brief-quality calibration sweep (the §2 partial-RG flag — three plausible approaches in the sketch, none validated); (ii) P-25 CaMeL utility-tax realized measurement on BF-M's production-adjacent regime; (iii) Brownfield regime ceiling measurability (own OQ-T6 from the track file — does per-(work-unit-class × stage) automation bar clearance contest Jaymin's brownfield ~L3 ceiling?); (iv) F36 instruction-following ceiling interaction with change-intent block size (own OQ-T10 from the track file — refusal criterion when change-intent grows past 10-20 requirements).
- **F-mode carries.** Per [§2.5 of the track file](../tracks/brownfield-methodology-first.md#25-failure-mode-coverage-severity-by-stage), F45 (language-as-harness) is informational / known-cost; F20 (brownfield asymmetry) survives because the cycle IS the brownfield-asymmetry-survival argument. F52 (tempting-wrong-hybrid) is architectural — the track explicitly forbids deterministic-wrapper accretion around LLM stages (deterministic checks live ONLY at stage-7 perimeter). All other F-modes have stage-owners named.

## §6 Scoping-principle compliance

This summary preserves BF-M as a defensible architecture proposal per the [scoping principle](../phase-3.4-decisions-resolved.md#scoping-principle-immutable-overrides-any-conflicting-framing-in-the-integration-brief):

- No primitive has been pre-eliminated; all 13 substrate references carry forward, two designed-system anchors named with their partial-RG flags.
- The two partial-RG flags (P-27 brief-quality calibration; P-25 utility-tax calibration) are honestly surfaced and routed to Phase-5/8 rather than papered over. Both are calibration-style (not constructive content gaps) and route to (b) accept-as-RG with substrate exposing the calibration parameters first-class.
- Open methodology questions (stage-compression OQ-T1, cross-model review necessity OQ-T2, CaMeL utility-tax acceptance OQ-T3, scenarios-from-codebase governance OQ-T4) are named in §5 and routed to Phase-4-methodology-spec / Phase-5 / Phase-8 — not used to demote the candidate.
- The candidate's load-bearing claim (methodology cycle IS the architecture; substrate primitives are stage-attached capabilities at boundaries, vendor-deferred) is preserved. The high primitive-count (~13) is a *feature* of methodology-first under brownfield — each stage names what it needs at its boundary — not a substrate-bloat signal.
- The deferred P-08↔P-09 collapse verdict is preserved as Phase-4.2 work; no same-vs-distinct judgment is rendered at this layer.

BF-M survives Phase-4.1 with calibration carries on P-27 and P-25, no shrinkage, no RG-fallback on a load-bearing primitive, and no pre-elimination. The Phase-3.5.5 status (`survives`) is confirmed.
