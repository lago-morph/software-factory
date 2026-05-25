---
guard: on-call-10yr
target: draft-unified-synthesis
phase: 3.2
based-on-commit: 200ad3e
based-on-date: 2026-05-25
---

# Phase-3.2 10-year on-call critique — unified draft

## §1 Persona stance

I am the on-call engineer who inherited this factory eighteen months after the original operator rotated out. I have two pagers strapped to one belt: one for greenfield engagements (we are currently bootstrapping a fintech MVP and a logistics control plane), one for brownfield (a regulated EHR refactor, a Stripe-scale checkout codebase, and three minor legacy ingestion jobs). The factory has been running 24 months. I have read the Phase-5 wave-1 file *"DPU-1: We Picked Interval"* three times. I still cannot tell you whether the EscrowInterval primitive is *the substrate* or *a substrate*. The classifier has drifted (F57 was caught two weeks ago in a quarterly). We have a Confluence page titled *"DO NOT regraduate the regression-fix class without paging on-call."* That page exists because someone regraduated the regression-fix class without paging on-call.

## §2 The 3am paging story

The page that wakes me up is bland: `PATROL/aggregate-rate-anomaly: refactor work-unit-class on engagement-EHR-2 — eligibility-promotion rate up 38% over 21-day baseline.` Standard F47 dashboard. I open the AttributedEventLog for the engagement, filter by `classifier.decision = automation-eligible`, and start reading. The events look fine. Every interval shows a `pace-layer + priors + kind` tuple, every decision is signed, every envelope content-addressed. Holdout discipline is intact. The DeterministicSpecLinter is green. By every primitive's local view the factory is healthy.

The actual failure is *cross-engagement*. The fintech-MVP greenfield bootstrap has been seeding `priors.out-of-tree.exemplars` into a shared exemplar store that the EHR-refactor brownfield engagement reads when its classifier consults the *similar-past* surface. The classifier's input distribution has shifted not because anyone retrained it, but because the population of intervals it has *seen recently* skews greenfield-bootstrap-shaped. So when a brownfield refactor work-unit-class with priors.in-tree comes in, the classifier — same primitive, same code path — silently scores it as if it were a routine near-anchor edit, because intervals "like this" have been graduating routinely on the greenfield side. This is F48 (tacit collusion via shared context) at the factory-fleet level: the substrate's shared classifier produces correlated errors across mandate-engagements, and the correlation is invisible per-engagement.

The on-call engineer's diagnostic loop fails three times. First, the AttributedEventLog has per-event lineage but no *cross-engagement aggregate* view — the immutable-logging promise of ROBUST-U9 is per-envelope, not per-classifier-input-distribution. Second, the HoldoutPartition (ROBUST-U11) was designed for in-engagement leakage; it has nothing to say about classifier *input-population* contamination across engagements. Third, the RegimeClassifier (ROBUST-U4) was promoted to substrate without a corresponding *substrate-level audit primitive*.

## §3 Specific protection-set claims that break

**ROBUST-U4 (RegimeClassifier) breaks first and breaks silently.** Promoting a learned-or-tuned decision surface to substrate without specifying *who watches the watcher* means F57 has no structural mitigation — the draft's claim that "classifier decisions are themselves intervals" creates an infinite-regress audit pattern that nobody operationalises. Brownfield convenience pressure (Stripe-scale throughput) reclassifies stakes downward; the only signal that the classifier graduated a work-unit-class too early is an *outcome* signal arriving 30–90 days later via F40 last-mile breakage. The unified factory's single classifier amplifies this versus a per-mandate factory — one drift event poisons both pipelines.

**ROBUST-U9 (AttributedEventLog) is structurally adequate but operationally unhelpful.** Per-event immutability does not give the on-call engineer a *queryable population view*. U-A OQ-4 explicitly flags this: "if many intervals share access to the same trajectory store or scenario library, the F48 multi-agent collusion surface may re-emerge at the substrate layer." It does re-emerge. F55 (behavioural drift / self-reference loop) compounds: the factory's own outputs become inputs to subsequent cycles; the multi-engagement factory does this across mandate boundaries.

**ROBUST-U11 (HoldoutPartition) is scoped to the wrong boundary.** The brownfield codebase model — refreshed many times — accumulates artifacts that re-enter the classifier's training-or-prompt-context distribution. The "codebase model has been refreshed many times" is itself an unmodeled rot vector: each refresh changes what counts as in-codebase-partition.

**DPU-3 / DPU-4 (RegimeClassifier as substrate primitive; granularity choice).** Per-interval (U-A) is the *hardest* to operate at year-2 scale because it produces the highest event-volume into the same classifier and the highest cross-engagement input mixing. Per-layer (U-B) gives 5 audit surfaces per cycle — tractable. Per-distance (U-C) reduces to a single decision per work unit but depends on the distance metric (which the draft acknowledges is gameable). The genuinely operable answer at year-2 may be **per-layer**.

**F8 (stale-knowledge inversion) × the codebase model.** After many refreshes of the codebase model across brownfield engagements, the AttributedEventLog references *symbol IDs, file paths, test names* from refreshes that no longer exist; the immutable log is honest about what it contains and dishonest about what it means. Anchor objects that pinned to runtime-trace or live-test artifacts have anchors-of-anchors that have been silently invalidated.

**Greenfield-bootstrap-misclassified vs brownfield-graduated-too-early diagnostic.** The on-call engineer cannot distinguish these in the current draft. Both manifest as *the classifier decided automation-eligibility on a work-unit it shouldn't have*. The substrate gives identical evidence in both cases. We need a substrate-level **classifier-input population audit primitive** that the draft does not currently surface.

## §4 Concrete recommendations for Phase-3.4

1. **Add ROBUST-U15: ClassifierInputPopulationAudit (new substrate primitive).** Substrate-resident, deterministic, samples the classifier's input distribution by mandate-tag, engagement-tag, and work-unit-class. Fires when distribution shifts exceed a configurable bound. Without it, F57 has no early-warning surface.

2. **Resolve DPU-4 toward per-layer (U-B granularity) for classifier audit even if per-interval (U-A) is kept for substrate granularity.** Decouple "what the classifier decides over" from "what gets audited."

3. **Add a "cross-engagement holdout" parameter to ROBUST-U11.** Extend to support inter-engagement partition: greenfield exemplars seeded into engagement E1 cannot enter the classifier-input population of engagement E2 in the same factory instance without an explicit, audit-logged transfer step.

4. **Promote F48 / F55 / F57 / F8 to first-class severity for the unified architecture specifically.** At unified scale these four interact multiplicatively. Add a unified-mandate severity column to failure-modes-v3.md.

5. **Add a substrate-level "codebase-model refresh event" object in the AttributedEventLog.** When the codebase model is refreshed, the log must capture: which symbol IDs were retired, which anchor objects became orphaned.

6. **Reframe DPU-1 to require an explicit "what-rots-first" risk register per typed-object choice.**

7. **Phase-3.4 should not lock in U-A's per-interval classifier as the unified default until ROBUST-U15 is specified.**

8. **D7-U-3 (new mandatory blind-axis test).** Dispatch one supplementary subagent: *"design the unified architecture's substrate without a RegimeClassifier primitive. Classification, if it happens, happens at methodology layer."* If this subagent produces a defensible design, ROBUST-U4 is brief-derived elevation per F-ANCHOR-4.

The on-call engineer's verdict: the unified architecture's *shape* is defensible. Its *resumption story at year 2 across mixed engagements* is not yet operationally specified. The classifier rots first, silently, with no early-warning surface, and the unified factory's shared substrate amplifies rather than mitigates the cross-engagement F48 correlation.
