---
guard: pre-mortem
target: draft-unified-synthesis
phase: 3.2
based-on-commit: 200ad3e
based-on-date: 2026-05-25
---

# Phase-3.2 pre-mortem critique — unified draft (DPU-1 attack)

## §1 Persona stance

I am the 18-months-later operator looking backward at a unified-architecture factory that was deployed across mixed greenfield + brownfield engagements. The architecture survived its Phase-3 adversarial passes, the user picked a typed-object granularity at Phase-3.4, the Phase-5 ADRs landed, and for the first six months everything looked elegant. The pre-mortem question — "why did it fail?" — is not whether ROBUST-U1 was wrong (mandate-as-parameter is in fact the corpus's strongest move) but which of DPU-1's three candidate typed-object granularities collapses first under sustained mixed-mandate operational load. My answer: **all three candidates fail in different ways at the same operational stress point — the place where greenfield and brownfield work share a single AttributedEventLog and a single RegimeClassifier population**.

## §2 The 18-month pre-mortem narrative

**Month 0-3 (honeymoon).** The factory was deployed against a greenfield engagement (a new internal billing service) and a brownfield engagement (a legacy logistics codebase) running on the same substrate. ROBUST-U1 worked: the same `EscrowInterval`/Layer/Anchor primitive carried both via `priors` content. The operator felt clever. DPU-1 was resolved to *interval-per-process-state* (U-A flavor) per a Phase-3.4 user call: maximum auditability, finest-grained classifier feedback. ROBUST-U9 AttributedEventLog persistence ran sub-millisecond per event.

**Month 4-9 (the silent compression).** The greenfield side accumulated `methodology-delta` intervals at a high rate (UC4 spec-malleability). The brownfield side accumulated `codebase-model-refresh` intervals at a moderate rate. The substrate-cheap thesis (U-A OQ-6) survived in isolation, but **the operator's attention budget for the EscrowSurface (ROBUST-U10) did not scale**. F42 / F53 / F-ANCHOR-2 had warned this exactly: substrate-fired escrow surfaces are only effective if the operator's evaluation budget per surface is preserved. With per-interval granularity (DPU-4) across two concurrent engagements, the surfaces fired too often; she developed a "skim and click through" reflex. This is F53 realised at the unified-mandate scale: the substrate could fire the surface, but could not force the read.

**Month 10-15 (classifier drift through the cross-mandate seam).** The RegimeClassifier (ROBUST-U4) takes its features from `pace-layer + priors + kind`. With both mandates feeding the same classifier population, the feature distribution shifted: brownfield-typical intervals drove the classifier's notion of "automation-eligible boring work" downward in stakes-perception, and greenfield-typical intervals silently inherited an automation-eligibility threshold calibrated by brownfield's evidence-density. **F57 (design-authority erosion)** is the named mechanism — convenience reclassifies stakes. The unified substrate amplified F57 because the classifier population was shared across mandates that needed different thresholds. The operator did not see this because the *audited* eligibility-decision at any moment looked consistent; only the cross-mandate threshold-distribution drifted. **DPU-3's elevation of the classifier to substrate primitive was the load-bearing mistake** — promoting it from methodology removed the per-mandate methodology-layer recalibration that would have kept the thresholds independent.

**Month 16-18 (the AttributedEventLog itself becomes an attack surface).** F55 lands at the unified layer in a form no single-mandate draft anticipated. The `EscrowInterval.policies` field accumulated across 18 months becomes a *policy corpus* that subsequent cycles read at open-time to select their own policies. This is policy self-reference (Kahana RSI three-part test trips). Worse, the immutable AttributedEventLog — supposed to be the auditor's friend — became an **attack surface for goal subversion (F54)**: an adversary or emergent error embedded in any single interval's `policies` field propagates to every subsequent interval that inherits the policy template.

**Month 18 (failure surface, observed).** The brownfield codebase shipped a defect into production via a logistics-domain regression. Post-mortem revealed the defect's interval had been classified `lights-out` by a classifier whose threshold had drifted *because of greenfield-side traffic*; the holdout-partition for the brownfield work was technically correct but its meaning had shifted; the EscrowSurface for the operator review had fired but had been muscle-clicked-through. UC4 was empirically reconfirmed but *worse than the brief framed it*: not "no single architecture works for both" but "a unified architecture works for both until cross-mandate interaction degrades both, after which neither mandate is recoverable without rebuilding the substrate".

## §3 Specific architectural commitments that caused the failure

| Commitment | What broke | F-modes that landed |
|---|---|---|
| **DPU-1 = interval** | Per-interval granularity made the AttributedEventLog a forensic-debt mountain; shared classifier feature population drove cross-mandate threshold drift. Per-layer (U-B) would have failed by under-granularity; per-anchor (U-C) would have failed by anchor-distance gaming. All three fail; interval fails last but loudest. | F14, F42, F53, F55, F57 |
| **DPU-3** | Shared classifier population across mandates. F-ANCHOR-4 (MEDIUM) flagged this. Removing methodology-layer recalibration removed the natural per-mandate threshold isolation. | F57, F47 |
| **DPU-4** | At high parallelism, the AttributedEventLog *itself* becomes the attack surface. Substrate-cheap-per-event ≠ substrate-cheap-aggregate. | F54, F55, F61 |
| **ROBUST-U10** | Substrate can fire surfaces; substrate cannot force the read. At mixed-mandate cadence the operator's read-budget per surface is cut roughly in half. | F42, F53 |
| **ROBUST-U1** | The unification is real *at the primitive level* but the cross-mandate interaction effects are *not* parameter-encodable. | F35, F55, F57 |
| **ROBUST-U11** | The partition declaration is honest at write-time but the *meaning* drifts as the classifier drifts. Holdout-discipline preserved syntactically; lost semantically. | F28, F57 |

## §4 Concrete recommendations for Phase-3.4

1. **Make DPU-1 a recoverable choice, not a permanent one.** Phase-5 wave-1 must include an **ADR for substrate-rebuild without engagement-loss** — the typed-object primitive will rot; the architecture needs a documented forward-migration story.

2. **Refuse to share the RegimeClassifier population across mandates.** Resolve DPU-3 toward "substrate primitive with **mandate-scoped feature populations**" — the classifier code is shared; the feature distribution and threshold calibration are per-mandate.

3. **Cap per-cycle EscrowSurface fire rate at the operator-budget level.** ROBUST-U10's "substrate-triggered" framing is correct; what's missing is a **budget-aware surface throttler** that detects muscle-click-through and escalates rather than fires more surfaces.

4. **Treat the AttributedEventLog's policy field as a corpus subject to F55, not as audit metadata.** When `EscrowInterval.policies` is read by later intervals to template their own policies, the substrate is doing RSI on itself. Phase-5 needs an ADR for **policy-corpus grounding**: every K cycles, the policy templates must be re-grounded against an out-of-substrate reference (human-curated baseline / first-principles re-derivation).

5. **Add a 4th decision-pending item to DPU-8: cross-mandate interaction effects.** Add `X_UNM_SEAM`: *"argue that the unified architecture fails not on either mandate but on their interaction — using F35/F55/F57 as the F-mode triad and the shared substrate primitives as the attack surface."*

6. **Re-rank failure-mode severity for the unified architecture.** F55 ranked as critical-greenfield/high-brownfield and F57 medium-greenfield/high-brownfield. **At the unified layer, both should be `critical`** because the mandates' worst-case severities compose, not average.

The honest answer: **the unified architecture's 18-month failure is not in the typed-object choice — it is in pretending that "mandate is a parameter" extends to the substrate's emergent cross-mandate behaviour.** Pick interval, layer, or anchor — the failure mode is the same.
