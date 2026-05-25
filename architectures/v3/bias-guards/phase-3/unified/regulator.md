---
guard: regulator
target: draft-unified-synthesis
phase: 3.2
based-on-commit: 200ad3e
based-on-date: 2026-05-25
---

# Phase-3.2 regulator critique — unified draft

## §1 Persona stance

I read this draft through Caremark prong-1 (Stone v. Ritter / Marchand mission-critical / Boeing design-choices-disable-monitoring / Hughes "trappings of oversight"), California SB 53 §"internal use," and the 2025-12-04 SEC IAC AI-disclosure recommendation, with the AILCCP 48-control catalogue as the controls baseline. My question for ROBUST-U13 and ROBUST-U14 is narrow but load-bearing: when *one* factory simultaneously runs a SaMD greenfield engagement and a HIPAA-regulated brownfield engagement under the same substrate, can the deploying board answer the Marchand "what is the mission-critical surface?" question, produce a Frontier AI Framework / sub-threshold RSI declaration the OES will accept, and answer the IAC three-question disclosure without revealing that the "one factory" answer collapses the per-deliverable risk classification SB 53 and the EU AI Act both presume? I find that the unified architecture **creates regulator-novel surfaces that AILCCP does not cover** — specifically a *cross-mandate substrate fungibility* surface.

## §2 Top regulator findings

### Finding R-1 — Cross-mandate substrate fungibility creates a Marchand-defeating ambiguity (HIGH)

Marchand asks: *"is this domain mission-critical to the company's operations?"* The unified factory's answer is *"yes for SaMD-deliverable-X, no for the internal HIPAA refactor running in the same interval graph at the same time."* The AILCCP per-phase ownership model presumes *one lifecycle phase, one deliverable, one owner per phase*. The unified substrate runs multiple lifecycle phases concurrently *over the same typed-object primitive*; from the board's vantage, the factory is one operational system but its mission-critical surface is per-deliverable.

Kahana's distinctive doctrinal contribution explicitly anticipates the multi-deliverable factory (research/31 §2), but the AILCCP controls do not yet exist for it. The Marchand inquiry becomes un-pleadable with particularity because the factory's audit trail surfaces interval-level facts, not deliverable-level facts. F43 mitigation via "AILCCP three-controls coverage aggregated to a board-quarterly report by the substrate's policy mediator" — but that aggregation is *per interval-policy*, not per-deliverable.

### Finding R-2 — DPU-3 classifier placement at substrate is a regulator-novel surface (HIGH)

The AILCCP "Acceptance Threshold Governance" control presumes the *threshold* is the audited object — *what counts as acceptable* — and that thresholds are per-deliverable. The unified-track classifier is a *meta-control* that decides per typed-object whether the threshold applies at all. This is a regulator-novel artifact: it is the surface where F57 lives, *and* it is the surface SB 53's *"internal use"* test attaches to — *the classifier itself determines whether a given cycle is an "RSI experiment" and therefore SB 53-reportable*. No AILCCP control governs *this meta-classifier itself*.

This is the single most regulator-novel surface in the draft. The classifier *parameterises* every other AILCCP control's activation; auditing the controls without auditing the classifier is the Hughes trappings posture.

### Finding R-3 — AttributedEventLog (ROBUST-U9) is structurally incompatible with SB 53 "internal use" reporting boundary (HIGH for SB 53-covered factories)

SB 53 reporting demands *"summaries of catastrophic-risk assessments from internal use"* periodically reported to OES, with *"RSI experiments constitute internal use before any public deployment."* The unified `AttributedEventLog` is per-interval / per-layer / per-distance — it is not per-deliverable, not per-RSI-experiment, not per-customer-engagement. To produce an OES-acceptable summary, an auditor must reconstruct deliverable-bounded reports from interval-bounded logs. The corpus' tension is already named in followup/10 §6 (*"A factory can satisfy BCG and still fail Kahana, because the regulatory ontology has not caught up"*). The unified architecture commits hard to BCG's side without engaging Kahana's.

F58 (Runtime/design-time compliance split, brownfield-HIGH) directly names this misfit.

### Finding R-4 — ROBUST-U14 graduation criteria are measurable but not regulator-legible (MEDIUM-HIGH)

The draft conflates *substrate-measurable* with *regulator-defensible*. The IAC question *"what board oversight mechanisms govern AI deployment?"* wants a *governance-event-shaped* answer (committee charter, escalation cadence, control attestation). U-B's "Jaymin thresholds calibrated" and U-C's "distance-distribution shift" are not governance events; they are observability events. The board cannot answer the IAC question by reading the graduation criteria. The unified-A.md graduation condition #3 (*"board-visibility apparatus per F43 mitigation… has produced its first quarterly report and the operator has acknowledged it"*) is the right *shape* but at the wrong granularity — *operator-acknowledged* is not *board-acknowledged*.

### Finding R-5 — F54 (RSI goal subversion) interacts adversarially with cross-mandate substrate (MEDIUM)

F54 names *"intermediate instructions… can redefine the agent's objectives incrementally across cycles."* In a cross-mandate factory, the SaMD-greenfield work generates intermediate signals (specs, judgments, methodology-delta intervals) that flow into the same substrate that runs the HIPAA-brownfield work. The substrate's content-addressed envelopes and shared classifier mean the HIPAA agents *legitimately* read context produced by the SaMD agents — the typed-object substrate makes cross-deliverable context-bleed structural rather than incidental. This is F48 (Tacit-Collusion-via-Shared-Context) lifted to the deliverable level.

## §3 What the architecture defensibly satisfies

ROBUST-U12 (Day-0 structural L3-Augmentation, no exceptions) and the U-A bootstrap interval's hard refusal to permit `lights-out` classification at bootstrap directly satisfy Caremark prong-1's "implemented a reasonable information system" element: the substrate cannot be configured to deploy without the apparatus. ROBUST-U13 (typed bootstrap output set) maps cleanly onto the AILCCP "controls table" demand for *named, principle-linked, audit-defensible* outputs. ROBUST-U7 (DeterministicSpecLinter) avoids the Ashby-deficient probabilistic-guard trap (F51). ROBUST-U8 (PerimeterClosure / substrate-default-off) is the correct posture against F44.

The U-A track in particular is well-positioned for *single-deliverable single-mandate* Caremark defense — the per-interval log policy maps directly onto Codex's OTEL stack. The defect is in the *cross-mandate* lift, not the single-mandate primitives.

## §4 Concrete recommendations for Phase-3.4

1. **Add DPU-9 — Deliverable-bounded substrate partitioning.** Phase-5 wave-1 ADR. Question: does the unified substrate enforce a `Deliverable` typed-object that bounds `AttributedEventLog`, `RegimeClassifier`, and `EscrowSurface` scopes per deliverable? Without this, R-1 (Marchand ambiguity) and R-5 (cross-deliverable context-bleed) cannot be mitigated.

2. **Extend ROBUST-U13 with a per-deliverable governance-event output.** The bootstrap output set should include — *per deliverable* — a board-attestation-shaped artifact (committee charter delta, escalation-cadence declaration, AILCCP-48 control-coverage matrix).

3. **Promote the DPU-3 classifier to its own audited control class.** Add a meta-control "Classifier Audit Trail" to the substrate primitive list: deterministic, append-only record of every classifier output with its feature inputs, version, and challenge-resolution path. This closes R-2's Hughes-trappings gap.

4. **Re-frame ROBUST-U14 graduation as a two-layer set.** Substrate-measurable criteria (current draft) plus governance-event-acknowledged criteria (new): board attestation of the classifier audit trail, counsel attestation of SB 53 applicability + IAC three-question response, audit-committee acknowledgment of AILCCP control coverage.

5. **Surface a Phase-3.3 X_REG attacker.** Add a sixth Phase-3.3 cross-mandate attacker: *"Argue that a deploying board running this unified factory across one SaMD-greenfield deliverable and one HIPAA-brownfield deliverable cannot answer the Marchand mission-critical-risk question, the SB 53 internal-use reporting question, or the IAC three-question disclosure without revealing that the unified substrate dissolves per-deliverable accountability."*

6. **Add F-mode candidate F62 — Cross-mandate substrate accountability collapse.** Deliverable-level Caremark/SB 53/IAC accountability is undermined when one typed-object substrate concurrently runs deliverables of differing regulatory regimes without per-deliverable partitioning enforced at the substrate primitive level.

The unified architecture is genuinely closer to BCG's "structurally easier" posture than any mandate-specific draft — *but only if the substrate enforces deliverable partitioning the BCG framing presumes implicitly through "the bolt" (single delivery unit, single stage-gate-evidence chain)*. The unified draft has substituted the typed-object primitive for the bolt and lost the deliverable-shape in the process.
