---
guard: on-call-10yr
target: draft-greenfield-synthesis
phase: 3.2
based-on-commit: e02d0ba
based-on-date: 2026-05-25
---

# Phase-3.2 10-year on-call critique — greenfield draft

## §1 Persona stance

I am the engineer who inherits a factory that has been ticking over for 18 months. The operator who wrote the original Intent Crucible has rotated out. The trajectory store is in tens of terabytes. The Patrol's drift-detection thresholds have been "tuned a few times — see git log." My job at 3am is not to admire the substrate's elegance; it is to answer *"why did Patrol not catch this"* with evidence I can hand to counsel before the morning standup. From that seat, the draft's §1.4 bootstrap protection set reads less like a guarantee and more like a set of claims whose decay I now have to audit.

## §2 The 3am paging story

The page fires because Patrol escalates *"invariant drift detected: WORK-UNIT-CLASS=regression-fix flipped to automation-eligible 14 cycles ago; cross-family judge agreement rate has trended from 0.94 to 0.71 over the past 30 days."* I do exactly what the draft tells me I can do: (a) pull the operator-declared intent block, (b) pull the trajectory store, (c) pull the Patrol log. Three things go wrong, fast.

First, the intent block I am holding is not the intent block as of cycle 1. Per GF-S §2.B and ROBUST-G4, the `invariants` field is the *slow layer* that everything else moves against. But GF-S §7 OQ-T4 explicitly raised — and the draft did not resolve — *"what happens when the slow layer is itself moved by the operator mid-flight?"* The substrate stores the spec under content-addressed versioning. In practice, with 18 months of operator-driven amendments, I do not know which invariant was load-bearing for which automation-eligibility decision. F8 (stale-knowledge inversion) is operative and the draft is silent on what *curation* means at month 18.

Second, the Patrol log tells me what Patrol *fired on*. It does not tell me what Patrol's *threshold was* at each firing. Per ROBUST-G11 lumper Cluster-9 split, Patrol is supposed to name the F-mode and the detector per claim — but the draft does not require Patrol's *threshold-tuning history* to be audited the same way trajectory events are. The watcher-of-the-watcher problem is structurally unaddressed. I cannot tell counsel whether Patrol missed the drift or whether someone quietly raised Patrol's threshold to stop the noise.

Third, I try to run report 30 §3's STIR-in-the-interval cascade (ROBUST-G14 / DPG-7) and discover that the new operator has built dismiss-by-default muscle memory against it. Kahana's *very own* critique of voluntary STIR ("the professional will impose the discipline voluntarily, at the right moments, with sufficient cognitive energy to do so. **That is a fragile dependency.**") applies to substrate-fired reflection prompts whenever the prompts can be dismissed without an audit trail. F53 has been *re-introduced through the back door* by alert fatigue.

## §3 Specific protection-set claims that break under operational reality

**ROBUST-G4 (intent block as upstream-stable artifact) — breaks first.** GF-S OQ-T4 explicitly flagged this as unresolved. F34 cross-layer drift is *defined* as "locally satisfies spec/plan/code, but violates architecture or standards above." Brier's whole point is that pace-layers work *only when slow layers move slowly*. The draft does not constrain operator-amendment rate on the intent block; it does not require that invariant amendments themselves be cross-family-judged; it does not require that automation-eligibility flips be invalidated when their grounding invariant changes.

**ROBUST-G11 (Patrol watches for drift) — second to break.** Lumper Cluster-9 already flagged that "Patrol detects drift" lumps F34/F54/F55/F57 into one mechanism. The draft says Phase-3 must require Patrol-claims to name the F-mode and the detector — but does not say the detector's *threshold* must be itself versioned, signed, and audited. F57 design-authority erosion is *exactly* "convenience steadily reclassifies higher-stakes decisions as lower-stakes." If Patrol's threshold is operator-tunable and the tuning history is not audited at the same fidelity as trajectory events, F57 has a structural pipeline straight through the substrate's primary defense.

**ROBUST-G18 (no `docs/solutions/`-style accumulation during cold-start) — third.** Expiry is left implicit. F8 and F55 (behavioural drift self-reference loop) both become operative *post-graduation*. F55's source quote: *"agent outputs become self-referential without external anchor."* At month 18 the inherited operator cannot tell which accumulated skill / scenario / scaffold encodes a genuine factory learning versus a once-correct-now-stale shortcut versus a factory-output-feeding-itself loop. The draft has no graduation criterion for *demoting* an accumulated artifact.

**ROBUST-G14 / DPG-7 (cognitive-escrow substrate primitive) — fourth.** F-ANCHOR-2 flag is honest about Kahana being single-source for the substrate-primitive promotion. The operational decay path: STIR cascade fires; operator click-throughs accumulate; the prompt becomes a modal-dismiss reflex; F53 reasserts itself with substrate complicity.

**ROBUST-G12 (trajectory capture) — fifth, slow-rotting.** Sub-ms persist at write side is feasibility evidence. The draft is silent on *query* performance, *index discipline*, *retention policy*, and *forensic reconstruction* cost at year-2 volume. The Replit G14 incident is exactly the case where the audit trail exists but the operator cannot *use* it. Trajectory-as-storage is necessary; trajectory-as-queryable-evidence is the bar the draft has not set.

**ROBUST-G15 (no bootstrap self-judge) — silently degrades.** At month 18, *what counts as bootstrap* is a definitional drift point. When a new work-unit-class is introduced post-graduation, is its first cycle "bootstrap"? The draft is silent. F46 single-model-review-blindspot re-emerges through the seam.

## §4 Concrete recommendations for Phase-3.4

**Operational-discipline ADRs needed (Phase-5 wave-1):**

- **ADR — Intent-block amendment audit.** Require that every operator amendment to `invariants` be: (i) cross-family-judged at amendment time, (ii) stored with a *human-readable amendment rationale* field, (iii) invalidate (mark for re-graduation) every work-unit-class whose automation-eligibility decision cited the amended invariant.
- **ADR — Patrol-threshold immutability discipline.** Patrol's drift-detection thresholds must persist to the trajectory store with the same per-event discipline as agent actions. Threshold-tuning events are themselves audit-class events.
- **ADR — Cognitive-escrow engagement audit.** STIR-cascade dismissals must be logged with a typed dismissal-reason field; recurring dismiss-by-default patterns surface as a Patrol-detectable F53 instance.

**Maintenance-cadence specs needed (Phase-6 architecture-spec YAML):**

- **Trajectory index discipline and retention.** Per-architecture spec must declare its trajectory-query SLOs (forensic-reconstruction time-to-evidence at year-N volume) and retention policy.
- **Accumulated-knowledge demotion protocol.** Per-architecture spec must declare how `docs/solutions/`-class artifacts get re-evaluated post-graduation.

**Operator-rotation runbook needed (Phase-8 lean-eval candidate):**

- **The new-operator inheritance drill.** Lean-eval brief: simulate handing the factory to a new operator who has not authored the original Intent Crucible. Measure (a) time-to-reconstruct the current invariant set from trajectory + Patrol logs alone, (b) time-to-discover whether Patrol thresholds have been tuned, (c) time-to-trace one shipped artifact back to the intent it served. If any of these exceeds an hour, the substrate has not actually replaced the rotated operator's tacit knowledge.

The corpus has been telling us for 18 months that voluntary discipline rots, classifiers drift, accumulated knowledge inverts, and post-incident reconstruction is the binding constraint. The draft has named all of these as failure modes but routes their *operational decay* to "Phase 5 ADR" or "configurable parameter" or "open question." The 10-yr on-call ask is: name them as **maintenance-discipline** load-bearing claims, not as configuration parameters.
