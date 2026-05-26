# ADR 0024: Discipline — regime classification

- **Status**: Accepted
- **Date**: 2026-05-25
- **Deciders**: lead agent (Phase 5 Wave 5.2)

## Context

Regime / eligibility classification is named by **all 10 tracks** as the discipline that bounds where lights-out is permitted vs. where augmentation or human-required handling is mandatory. The [regime-classification discipline write-up](../../architectures/v3/disciplines/regime-classification.md) catalogues the per-candidate naming (GF-S `S9 eligibility classifier`, BF-L per-region classifier, U-A interval-bracketed classifier, U-C distance-gated dispatcher, GF-C graduation protocol, BF-M per-(class × stage) bar, GF-M Regime A → Regime B, BF-S work-unit-class eligibility, U-B per-layer regime, D7-U-1 per-artifact-kind regime). The [disciplines index](../../architectures/v3/disciplines/index.md) names it as one of 21 canonical disciplines.

The forcing concern is **vocabulary discipline** (CTR-A4: "lights-out" ≠ L5) coupled with **classifier-as-policy drift** ([F57](../../architectures/v3/failure-modes-v3.md#f57--design-authority-erosion-convenience-reclassifies-stakes)): if regime classification is implicit or policy-only, convenience reclassifies stakes silently and the lights-out surface expands by drift rather than by measured graduation. The classifier is, per U-A §7 OQ-2, the architecture's most powerful actor — F57 is amplified by giving so much weight to one substrate primitive.

Regime-classification sits *between* substrate primitive [P-19 (eligibility / regime classifier)](../../architectures/v3/primitives/P-19-eligibility-regime-classifier.md) and the methodology layer. The [P-19 four-variant analysis](../../architectures/v3/primitives/overlap.md#p-19-eligibility--regime-classifier--four-contested-variants) established SAME primitive, DISTINCT feature sources: the **decision-engine layer** (Drools/OPA Rego + LLM-judge fallback via P-14 + OPA hard-floor post-check) is shared, but four candidates contribute distinct *feature engineering* and *output enum* variants (work-unit-class for GF-S; per-region for BF-L; distance-gated for U-C; interval-kind for U-A). This discipline is the methodology contract that names which feature source and which regime set each candidate adopts.

## Decision

**The regime-classification discipline binds every methodology to declare three things:** (a) the **set of eligibility regimes** it recognises (e.g., `automation-eligible / augmentation-required / escalate`; or `lights-out / cross-model-judging / human-required`; or per-region regime tags for BF-L; or `automation-eligibility` flag consumed by P-29/P-30 for U-A); (b) the **feature source** the candidate-specific P-19 variant consumes (intent-block fields + bar-set saturation for GF-S; Codebase-Model features for BF-L; P-32 DistanceTuple for U-C; `EscrowInterval.kind` + pace-layer + priors for U-A); (c) one or more **hard-floor post-checks** that override classifier output (e.g., `contradiction_flag → human-required` regardless of regime, per U-C's hard-floor; Caremark/RSI exposure → augmentation-required, per BF-L).

The classifier itself is substrate-typed (per P-19) and audit-able; its output distribution is monitored by Patrol-tier watchdogs ([P-06](../../architectures/v3/primitives/P-06-watchdog-tiers.md)) for drift, and drift triggers re-entry (re-classification at the next interval boundary or work-unit handoff). Architecture-spec authors (Phase 6) write the per-candidate regime set + feature source + hard-floor table. Phase-8 lean-evals MUST include both a classifier-drift pressure-test (does the regime distribution shift under controlled feature changes?) and the cross-variant correlation test ([overlap §P-19 implications](../../architectures/v3/primitives/overlap.md#p-19-eligibility--regime-classifier--four-contested-variants): do the four feature sources produce correlated regimes on a shared scenario set?).

## Alternatives considered

**B. Implicit-always-automation default (no declared regime set; lights-out unless something breaks).** *Why rejected:* this is the [F40 last-mile-drift](../../architectures/v3/failure-modes-v3.md#f40--last-mile-drift) attractor — convenience reclassifies stakes silently, and the lights-out surface expands by drift rather than by measured graduation. CTR-A4 explicitly distinguishes "lights-out" from L5; an implicit default collapses that distinction at the methodology layer and forces substrate to carry vocabulary discipline it cannot enforce without methodology contract. Brief §2.1 names option (c)+(b) (eligibility-gated lights-out with explicit augmentation) over option (a) (default-automation); this discipline operationalises that choice.

**C. Operator-only regime decisions (no substrate classifier; humans triage each work unit into a regime).** *Why rejected:* does not scale and re-introduces the human-in-inner-loop bottleneck the methodology layer exists to avoid. More importantly, operator-only regime decisions are **unauditable as a class** — each decision is defensible in isolation but the *distribution* of decisions across operators drifts in F57-shaped ways that only a substrate-typed classifier with logged outputs can detect. The substrate classifier's existence does not preclude operator override (every candidate carries an override path), but the default decision must be substrate-typed for auditability.

## Consequences

**Easier:** Vocabulary discipline (CTR-A4 holds: "lights-out" is a regime, not a default); F57 made visible at the classifier-output-distribution layer (Patrol-tier watchdog has a defined signal); the lights-out surface only expands by measured bar clearance ([GF-C graduation](../../architectures/v3/tracks/greenfield-cold-start-first.md), [BF-M per-cell bar](../../architectures/v3/tracks/brownfield-methodology-first.md)) rather than by drift. Hard-floor post-checks (contradiction → human; Caremark/RSI → augmentation) give methodology authors a single place to encode non-negotiable escalation rules.

**Harder:** Each candidate's architecture spec carries an explicit regime-set + feature-source + hard-floor table — non-trivial authoring work, and the per-candidate variants are not interchangeable (the [P-19 overlap analysis](../../architectures/v3/primitives/overlap.md#p-19-eligibility--regime-classifier--four-contested-variants) confirmed four distinct feature sources). Classifier-drift monitoring requires a baseline output distribution per regime, which is a per-deployment calibration step.

**Explicitly NOT promising:** specific regime thresholds (the K=5 ≥70% augmentation / K=5 ≥90% automation bar from Report 09 §5.5 is a corpus reference, not a discipline mandate); specific feature weights; the choice between decision-table engine implementations (Drools vs OPA Rego — that is the common [P-19 substrate ADR](../../architectures/v3/primitives/P-19-eligibility-regime-classifier.md)'s decision, not this discipline's).

## References

- [Regime-classification discipline write-up](../../architectures/v3/disciplines/regime-classification.md)
- [P-19 eligibility / regime classifier substrate primitive](../../architectures/v3/primitives/P-19-eligibility-regime-classifier.md)
- [P-19 four-variant overlap analysis](../../architectures/v3/primitives/overlap.md#p-19-eligibility--regime-classifier--four-contested-variants)
- [Disciplines index](../../architectures/v3/disciplines/index.md)
- [ADR 0020: Discipline — cost ceiling](0020-discipline-cost-ceiling.md) — Wave-5.2 exemplar; cross-references this discipline for per-regime cap-tables
- [F57 design-authority erosion](../../architectures/v3/failure-modes-v3.md#f57--design-authority-erosion-convenience-reclassifies-stakes) and [F40 last-mile drift](../../architectures/v3/failure-modes-v3.md#f40--last-mile-drift)
- [auto-005 Round 2 Phase-5 dispatch shape](../../architectures/v3/decisions/auto-005-phase-5-dispatch-shape.md)
