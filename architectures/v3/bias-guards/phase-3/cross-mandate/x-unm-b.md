---
guard: cross-mandate-unified-fails-brownfield
target: draft-unified-synthesis
phase: 3.3
based-on-commit: 52f4fb9
based-on-date: 2026-05-25
---

# Phase-3.3 `X_UNM_B` — unified-fails-brownfield falsification test

## §1 Stance

The unified architecture cannot work for brownfield, and the reasons are not subtle. The brownfield-critical F-mode set (F12, F20, F21, F33, F34, F44, F56, F58 — all brownfield-critical) is **not a list of risks that can be addressed by per-node policy fields on a substrate primitive**. It is a list of consequences of operating *inside* an observable production reality whose maintenance cadence, evidence density, and regulatory inheritance differ structurally from anything a greenfield interval / layer / anchor can carry. The unified draft has *no equivalent* to the brownfield draft's `CodebaseModel` substrate primitive with its five sub-stores (ROBUST-B3, ROBUST-B4) — and silently expects the same typed-object substrate that handles greenfield's spec malleability to also host an industrial-scale, immutable, query-sliced, role-partitioned codebase model fed by production telemetry.

## §2 Top attack findings

**Finding 1 — The codebase-model primitive is absent from the unified substrate; "priors.in-tree" is a slot, not a model. SEVERITY: CRITICAL.**

The brownfield draft makes the codebase model with five sub-stores the *load-bearing* substrate primitive. F21 (context-window exhaustion, brownfield-critical) is "structurally unavoidable without this." The unified draft's `priors.in-tree: [codebase]` is an *enumeration*, not a queryable, incrementally maintained, role-partitioned model. The unified architecture's substrate-primitive enumeration (ROBUST-U2 through ROBUST-U11) names `EscrowSurface`, `TypedJudgeCall`, `FrozenAnchor`, `AttributedEventLog`, `PerimeterClosure`, `HoldoutPartition`, `RegimeClassifier`, `DeterministicSpecLinter` — but no `CodebaseModel`. Without it, F21 is unmitigated, F34 has no invariant-view to read, and F28 cannot be substrate-enforced via role-partitioned in-codebase reads.

**Finding 2 — Per-distance / per-interval / per-layer regime classification does not map to per-region evidence density. SEVERITY: HIGH.**

DPB-6 in the brownfield draft surfaces a fourth granularity that **none** of the unified tracks expose: *per-(work-unit-class × code-region)*. The distinguishing inputs are **region-properties from the codebase model** — coverage density, churn rate, dependency centrality, telemetry density. The unified tracks' classifier inputs (interval features, layer crossings, distance tuple) are *architectural* features of the work unit, not *evidential* features of the affected code region. A unified-architecture classifier cannot answer: "is *this region* well-instrumented enough that I can trust an L4 verdict on a change to it?"

**Finding 3 — AttributedEventLog at Stripe scale collides with bootstrap-interval immutable-logging cost. SEVERITY: HIGH.**

The brownfield steady-state operating point is *Stripe 1,300 PRs/week*. At that volume, the AttributedEventLog is dominated by *shallow, frequent, high-cardinality* events. The greenfield bootstrap interval is the opposite: *deep, rare, low-cardinality, high-policy-density*. Both have to live in the same envelope. The substrate-cost trade-off is *opposite*: brownfield wants narrow events and aggressive log compaction; greenfield bootstrap wants deep events and inviolable per-event policy attachment. U-A OQ-6 names this exactly. Stripe-scale brownfield × the unified substrate's bootstrap-grade per-event policy attachment is *unaffordable*.

**Finding 4 — In-codebase holdout (CTR-B5 inversion) is silently subordinated to greenfield's out-of-tree assumption. SEVERITY: HIGH.**

Brownfield's holdout discipline (ROBUST-B6) is **role-partitioning of in-codebase reads** — not a directory choice but a substrate-level view-filter on the codebase index, dependency graph, and telemetry. The unified substrate has no codebase index (Finding 1); therefore it cannot supply view filters; therefore the `in-codebase-partition` enum value is **vacuous**.

**Finding 5 — F58 inherited compliance obligations are silently treated as greenfield-style fresh-start. SEVERITY: MEDIUM-HIGH.**

F58 (runtime/design-time compliance split) is constitutively brownfield — it is an *inherited* compliance obligation. ROBUST-U13 lists only *forward-going* artifacts. No substrate primitive in the unified architecture for **ingesting and tracking inherited compliance obligations** (EU AI Act conformity certificates, FDA SaMD certifications, ISO 26262 design-time proofs).

## §3 What the unified architecture concedes

The draft already concedes the substrate cost question (U-A OQ-6), the classifier-accountability question (U-A OQ-2), the codebase-model-as-attack-surface question (BF-L OQ-T6, not folded into unified DPUs), the maintenance-cadence question (DPB-4, not folded), and the per-region-vs-per-work-unit classification gap (DPB-6, not folded). The unified draft's DPU-1 through DPU-8 inherit DPG and DPB items asymmetrically: every DPG concern is folded; every DPB concern about codebase-model, per-region regimes, telemetry-bootstrap, and inherited compliance is *not* folded.

The axis-divergence-audit §3.3 finding the draft cites ("Effective overlap on substrate primitive content: ~55%; overlap on 'mandate is a parameter': ~95%") is itself a signal that the unified tracks converged on a *framing*, not on a substrate.

## §4 Verdict for Phase-3.4

**The unified architecture FAILS the brownfield-side attack.** Finding 1 (CodebaseModel substrate-primitive absence) is *load-bearing critical* — it is the primitive that the brownfield draft's most cited F-mode mitigations (F21, F28, F34, F58) all depend on. The unified draft cannot retrofit it without changing the substrate enumeration materially; doing so would force a sixth substrate primitive whose maintenance cadence is brownfield-specific.

This is *not* a "partially survives." The unified architecture works for *greenfield steady-state*; it works for *bootstrap intervals across both mandates*; it works at the *methodology* layer for brownfield's per-cycle process flow. But the **brownfield substrate** — the queryable, role-partitioned, incrementally maintained codebase model with five views feeding regime classification, holdout enforcement, drift detection, and inherited-compliance tracking — is not in the unified architecture's substrate enumeration. UC4 holds on the brownfield side.

Recommendation for Phase-3.4: the unified architecture should be reframed as a **greenfield-leaning unified candidate** with substrate-extension points for brownfield's CodebaseModel primitive — *or* Phase-4's shared-substrate extraction should treat the unified draft as evidence that the **typed-object envelope is shared substrate** and the **codebase model is brownfield-divergent substrate**, with the methodology layer (cycle shape, judge calls, escrow surface, holdout partition) shared. The latter is the cleaner extraction and is consistent with `X_GFB_X`'s anchor (CTR-G3).
