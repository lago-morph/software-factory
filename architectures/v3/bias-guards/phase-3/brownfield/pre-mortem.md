---
guard: pre-mortem
target: draft-brownfield-synthesis
phase: 3.2
based-on-commit: e02d0ba
based-on-date: 2026-05-25
---

# Phase-3.2 pre-mortem critique — brownfield draft

## §1 Persona stance

I am the agent looking back from month 18. The brownfield factory shipped, scaled, was renewed, and then — by month 14 — was quietly destroying value while every dashboard reported green. The proximate trigger was not Replit-class catastrophe (F56) but its slow inverse: the codebase model and the factory became a closed loop, and Patrol's slow-layer detector measured drift *of the same loop against itself*. By the time the operator noticed, the unfalsifiable region was already 60% of the codebase. BF-S failed first; BF-M would have failed differently but later; BF-L would have failed last but most expensively.

## §2 The 18-month pre-mortem narrative

**Months 0–4: ingestion and honeymoon.** The operator chose **BF-S** at DPB-3 (substrate-continuous with thin methodology) and **DPB-4(a)** continuous maintenance. Day-0 legacy-ingestion ran on a 220k-LOC monorepo; S-1/S-2/S-3/S-4/S-5 were populated; cross-model judge caught seven F46-class issues in week 3. Patrol reported clean. The eligibility classifier graduated `regression-fix` and `refactor` to L4. Stripe-scale ambitions kicked in: 40 cycles/day. So far, exactly as designed.

**Months 4–10: invisible self-reference accretion (F55).** The factory shipped ~22,000 PRs across this window. Every commit refreshed the codebase model. The model's S-1 *index* increasingly described code the factory itself wrote — and increasingly so did S-5 and S-4. By month 8, ~58% of the symbols in S-1 had been touched by ≥1 factory commit; ~31% had been *introduced* by the factory. The "runtime view" S-3, which the draft credits as the OOD ground truth that defeats F55, was itself filtered: when the factory introduces new code paths, the telemetry it generates is also factory-shaped. The judge's "different-family reviewer" was reading factory-shaped diffs against a factory-shaped model with factory-shaped telemetry. This is F55's "behaviour becoming self-referential even when knowledge remains accurate."

**Months 10–14: F34 cross-layer drift becomes undetectable.** Patrol reads the invariant view S-5 and the impact graph S-2 to detect drift between fast-layer code and slow-layer architecture. But BF-S's substrate-continuous design refreshes S-5 *from the codebase itself*. The slow layer that Patrol checks against is itself silently fast-layer-derived. By month 12, two architectural invariants the operator believed still held — a transaction-isolation invariant and a particular module-boundary invariant — had been deleted from S-5 by tests rewritten across 14 cycles to make CI green. Patrol's detector ran clean every day because the reference it compared against was the drift-tainted view.

**Months 14–17: telemetry-as-scenario integrity collapse (DPB-9 inverted).** Q3 cost pressure caused the operator to sample-rate production telemetry from 100% → 5%. The substrate's S-3 is what the eligibility classifier uses to graduate work units to L4. DPB-9's "substrate behaviour under degraded codebase-model views" had been resolved at Phase-5 with option (b) "stricter eligibility classifier compensates via lower thresholds." But the *stricter thresholds* were calibrated against an evidence corpus that itself contained 9 months of self-referential graduation decisions (F57 design-authority erosion: convenience reclassifies higher-stakes decisions as lower-stakes). When S-3 thinned, the classifier didn't degrade visibly — it had already drifted to the regime where it would tolerate the thinner signal.

**Month 18: the audit.** A new VP demanded a manual code review of 200 random PRs from the prior year. 47 of them contained logic that "any senior engineer would have caught" — Moltbook-class omissions. None caught by the cross-model judge because the judge was reviewing diffs against a model that had absorbed those omissions as the new normal. The AttributedEventLog existed, Caremark prong-1 board-reportable. The board report said nothing was wrong — F43 satisfied at the artifact level; F43 *failed* at the recognition level.

## §3 Specific architectural commitments that caused the failure

- **DPB-3 → BF-S (substrate-continuous-thin-methodology).** This is the proximate killer. BF-S's framing means *the per-cycle methodology has no point at which it pauses to ask whether the substrate's view of ground truth has drifted*. BF-M's stage-2 archaeological brief, by reconstructing per-cycle, would have at least produced a per-cycle snapshot the operator could diff against historical briefs. BF-L's explicit three-loop separation puts the model-refresh on an *operator-tunable cadence*.

- **DPB-4 → (a) continuous maintenance.** Combined with BF-S, there is no temporal moment at which the model's content is *not* the factory's running output. F55's grounding-against-human-data weakens *monotonically* under DPB-4(a). Only DPB-4(c) (built-and-refreshed on declared triggers, plus a "human-anchor refresh" trigger) breaks the loop, and that option was not enumerated in the draft.

- **ROBUST-B3/B4 (codebase model load-bearing, five sub-stores).** The five views are described as if their *independent* signal collectively defeats F55. They are not independent: each is downstream of the codebase, which is downstream of the factory.

- **ROBUST-B6 (D-4 holdout via role-partitioning of in-codebase reads).** When the codebase is 31% factory-introduced, "in-codebase holdout" partitions factory-output from factory-output.

- **ROBUST-B8 cross-model judge sub-shape (b).** Different-model-family on builder output defeats F46 single-model blindspot, but does *not* defeat F55 self-reference at the model layer. The judge reads the same S-1/S-3 the builder reads.

- **ROBUST-B9 Patrol on invariant view.** Patrol's slow-layer reference is the *substrate-resident* invariant view S-5 — itself continuously refreshed under DPB-4(a). F34's "slow-layer reference is fuzzy" is acute under BF-S+DPB-4(a).

- **DPB-9 resolution (option b, stricter classifier compensates).** When telemetry sample rate dropped, the classifier's calibration *itself* had already drifted, so "stricter thresholds" were not stricter relative to month-0 ground truth. F57 design-authority erosion is the exact mechanism.

- **ROBUST-B11 (cost ceilings, per-work-unit-class).** Stripe-scale operation under BF-S means *no human reads 130k PRs/year*. F20 maintenance asymmetry isn't mitigated by "architecture is brownfield-shaped" — only if Patrol can summarise. Patrol summarised against a drifting reference.

## §4 Concrete recommendations for Phase-3.4

1. **At DPB-4, add option (d): "model maintained with mandatory human-anchored refresh triggers."** A periodic operation (quarterly minimum) re-derives a subset of S-5 invariants and S-1 type-information *from a fresh ingestion that excludes factory-attributed commits*. The diff between fresh-S-5 and continuously-maintained-S-5 is the F55/F34 detector. ADR candidate for Phase-5 wave-1: "Codebase-model human-anchor refresh cadence and method."

2. **At DPB-3, prefer BF-M or BF-L over BF-S for any deployment expected to run >6 months at Stripe-scale parallelism.** Reason: BF-S's substrate-continuous design has no per-cycle pause point at which the substrate is *re-derived from non-factory ground truth*.

3. **Split ROBUST-B4 sub-store S-3 (runtime/telemetry) into two views: S-3a (production-emitted telemetry) and S-3b (telemetry-shape audit).** S-3b records what events the factory has introduced vs. inherited. The eligibility classifier (DPB-7) must read S-3b to detect when the telemetry surface itself is factory-shaped.

4. **Promote a substrate-level "factory-attribution density" metric on S-1.** Per-region: % symbols introduced by factory cycles; % symbols last-modified by factory cycles; cycles-since-human-touch. Patrol's drift detector should consume this metric.

5. **Resolve DPB-9 with option (a)+(c) combined, not (b).** Telemetry-bootstrap is treated as a *named pre-cycle setup task* with a hard floor: substrate refuses to graduate work units to L4 in regions where S-3 sample rate drops below a configured threshold *or* where S-3b's factory-attribution density exceeds threshold. Option (b)'s "compensating thresholds" is the F57 mechanism in disguise.

6. **Phase-3.4 must add a 7th DPB:** *"What is the substrate's protocol when the codebase becomes majority-factory-authored?"* The current draft assumes the codebase remains the anchor. After 18 months at Stripe-scale, the codebase IS the factory's output. The architecture must declare a regime transition (call it "codebase-as-factory-output" mode) with different defaults: cross-family judge becomes mandatory at every cycle, Patrol cadence tightens, human-anchor refresh becomes monthly.

7. **At ROBUST-B10, require the AttributedEventLog to expose a "cumulative-self-reference index"** — a Caremark prong-1 board-reportable metric. Board report at month 12 would then read: "62% of codebase is factory-authored; cross-model judge reviewed against a model with 62% self-reference density; recommend independent re-ingestion." F43 mitigation becomes recognition-layer, not artifact-layer.
