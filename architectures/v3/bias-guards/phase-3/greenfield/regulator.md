---
guard: regulator
target: draft-greenfield-synthesis
phase: 3.2
based-on-commit: e02d0ba
based-on-date: 2026-05-25
---

# Phase-3.2 regulator critique — greenfield draft

## §1 Persona stance

I am reading this draft as an external regulator's counsel (CA Office of Emergency Services for SB 53; Delaware-litigation discovery; SEC IAC disclosure review) preparing a *minimum-defensibility* assessment of the v3 greenfield synthesis. My job is not to ask whether the architecture works as engineering — it is to ask whether the artifact set, as committed at day 0 and across graduation events, is sufficient for the deploying entity's board to satisfy *Caremark* prong-1 in plausible litigation, and for counsel to certify SB 53 §3 framework publication and OES periodic reporting if the deployment crosses the 10²⁶ FLOP threshold or fields RSI-meeting-the-three-part-test as "internal use." The draft is unusually self-aware on these issues — ROBUST-G19 is rare in this category and counts in the deployer's favor — but my read is that several specific design choices in the synthesis still produce *Boeing-style design-disabling-monitoring* exposure (per `research/31-caremark-rsi-board-exposure.md` §2, *In re Boeing Co. Derivative Litig.*), and that the audit surface for the eligibility-classifier and graduation events is currently insufficient to defend a *Marchand* mission-critical-risk inquiry.

## §2 Top regulator findings

**Finding R1 — ROBUST-G19 declares RSI status; it does NOT establish the three AILCCP controls actually run on every material self-modification. Severity: HIGH.**

The claim in ROBUST-G19 is that the AILCCP three-controls (Human Approval Gate / sandboxing / immutable logging) and Caremark prong-1 board reporting are *scaffolded* before the first cycle. Scaffolding is not running. Per `research/31-caremark-rsi-board-exposure.md` §5: *"The board has to be able to answer … whether the AILCCP three controls are in fact running on every material self-modification."* And per the Hughes v. Hu *"trappings of oversight"* doctrine cited in §2: a board that accepts "we have human approval gates, sandboxing, and immutable logging" without verifying they run is in the *exact posture Hughes rejected*. The graduation protocol (DPG-4) explicitly transitions work-unit-classes from `augmentation-required` to `lights-out` — i.e., removes the Human Approval Gate per work-unit-class — but the draft does not require that the substrate produce a board-visible reporting artifact at each graduation event certifying that gate, sandboxing, and immutable logging coverage *survive* the transition. Audit gap: a *Boeing*-style "design choice that disables board-level monitoring" is exactly what DPG-4 graduation looks like to a plaintiff's expert if not surfaced.

**Finding R2 — DPG-3 "substrate vs methodology classifier" question is regulator-blocking. Severity: HIGH.**

If the eligibility classifier is methodology-layer (per-architecture, per F-ANCHOR-4 in §2 DPG-3), then *the audit surface fragments*: each architecture-spec carries its own classifier semantics, and the AILCCP Acceptance Threshold Governance control (per `research/followup/10-governance.md` §6a.B) cannot be uniformly evidenced. The 187 control-to-principle linkages Kahana names (`followup/10-governance.md` §6a.C) presuppose a *single* control surface, not a per-architecture-spec one. A SB 53 §3 framework publication that says "eligibility is determined per-architecture-spec methodology" gives OES nothing to assess; an internal SEC IAC question 2 answer ("what board oversight mechanisms govern AI deployment?") cannot be answered with "consult the architecture's methodology overlay." The draft surfaces this as a *user decision*, which is procedurally correct, but regulator-readability requires the substrate-side resolution. *Methodology-layer classification is the SolarWinds posture* — framing as "business judgment" rather than "compliance obligation" (per `research/31-caremark-rsi-board-exposure.md` §2 SolarWinds discussion).

**Finding R3 — Log-retention cadence is gestured at, not specified. Severity: MEDIUM-HIGH.**

ROBUST-G12 says trajectory capture is "content-addressed, sub-ms persist, per-event" and is "co-extensive with AILCCP immutable logging." But Kahana's AILCCP Intervention Audit Trail control (`research/followup/10-governance.md` §6a.B) requires *append-only sink with attestation* — verbatim from `research/31-caremark-rsi-board-exposure.md` §5: *"the OTEL export is not by itself immutable; the immutability requirement would require a downstream append-only sink (e.g., a WORM bucket with an integrity-attested write path)."* The draft mentions OpenHands V1 sub-ms persist as *feasibility evidence, not normative dependency*; it does not name a retention cadence, an attestation mechanism, or a litigation-hold path. For *Caremark* prong-1, "the company can reconstruct" requires *retention adequate to the discovery window of plausible litigation* — typically 7 years for federal securities, longer for SaMD. The draft is silent on retention horizon; this is exactly the gap *Boeing* hit on the MAX engineering changes.

**Finding R4 — Cross-model judge mandate (ROBUST-G10) is regulator-positive; same-model carve-out at steady-state (CTR-D7 / Anthropic followup/07 §3.6) needs explicit independence evidence. Severity: MEDIUM.**

ROBUST-G10's cold-start mandate for cross-model judge is the strongest piece of the synthesis from my desk — it directly addresses the AILCCP Multi-Agent Protocol Security and Independence controls (`research/followup/10-governance.md` §6a.B + §5 control #4 "Independence policy: Verifier-on-different-model-family-than-constructor as a *compliance fact*, not just a quality fact"). However, the draft also flags CTR-D7 (Anthropic's "same model is usually fine" per `research/followup/07-evals-deepdive.md` line 280) as a potential carve-out at steady-state. From a regulator's standpoint: Anthropic's own framing requires *"high True Positive Rate (TPR) and True Negative Rate (TNR) … on a held out labeled test set"*. Adopting same-model judging *without per-architecture-spec evidence of TPR/TNR alignment on a held-out set* is a "the substrate vendor said it's fine" defense — which is exactly the *AmerisourceBergen / Teamsters v. Chou* fact pattern: management awareness without board-level evidence does not safe-harbor the board.

**Finding R5 — F58 (runtime/design-time compliance split) is unaddressed by graduation protocol. Severity: MEDIUM.**

DPG-4 graduation transitions the operating regime per-work-unit-class based on measured signals (scenario saturation, judge stability, drift absence, K=5 baselines). This *is* a runtime-compliance gesture — but F58 names *EU AI Act compliance proofs at training/design time vs. agents introducing runtime behaviors not captured at design time*. The graduation protocol gives the deployer a story about *changes in regime* but not a story about *changes in regulated behaviour*. A deliverable that was design-time-certified under `augmentation-required` and then graduated to `lights-out` has, by definition, undergone a material change in human-oversight affordances — the EU AI Act Article 14 (human oversight) treats this as a fresh conformity assessment trigger. The draft does not require re-certification evidence at graduation events.

## §3 What the architecture defensibly satisfies

First, **ROBUST-G19 itself — declaring RSI status at day 0, before the first cycle** — is the single most regulator-positive design choice in the synthesis. Kahana's framing rule is that *the more the record shows directors treating RSI as an operational efficiency project, the closer the fact pattern comes to SolarWinds*. Day-0 declaration *creates the record* that defeats SolarWinds framing. This is the highest-leverage compliance commitment in the document.

Second, **substrate-default-off production scissors (ROBUST-G9, F44 cascade)** and the **deterministic GtWR/EARS lint refusal of LLM-judge at authoring layer (ROBUST-G6)** map cleanly onto the AILCCP Rate-and-Scope-Limiter and Acceptance-Threshold-Governance controls. The explicit refusal of F51 (Ashby-deficient probabilistic guard) at the authoring layer is a defensible answer to the SEC IAC question 2 ("what board oversight mechanisms govern AI deployment?") in a way that "we have an LLM-judge" is not.

Third, **the bootstrap-cannot-self-judge rule (ROBUST-G15)** plus **cross-family judge at high-stakes cycles (ROBUST-G10)** together produce structural Independence-Policy evidence of the kind that the AILCCP 48-controls catalogue treats as a first-class compliance fact, not just a quality fact. For the SEC IAC machine-readable disclosure question this is materially helpful.

## §4 Concrete recommendations for Phase-3.4

**Rec-R1 (ADR-class clause).** Draft a Phase-5 wave-1 ADR titled **"AILCCP three-controls coverage attestation at graduation events"** that binds DPG-4 graduation: the substrate must emit a structured board-reporting artifact at each work-unit-class graduation event certifying that Human-Approval-Gate / sandboxing / immutable-logging coverage *survives* the regime transition. Without this clause, DPG-4 graduation is a *Boeing*-style design choice disabling monitoring. Owner: lead agent. Specific artifact: extend the architecture spec's YAML schema with a `graduation-attestation` block carrying per-work-unit-class coverage statements + timestamps.

**Rec-R2 (DPG-3 substrate-side resolution).** Recommend that DPG-3 resolve to substrate-side (a) at Phase-3.4 — not because it is engineering-superior but because *methodology-side fragments the regulator audit surface*. The architecture spec must declare the classifier's state schema, decision provenance, and Patrol-audit hook as substrate-typed. A SB 53 §3 framework cannot reference "consult the per-architecture methodology overlay" and remain defensible. If DPG-3 resolves methodology-side at Phase-3.4, the spec must declare the classifier as a *named AILCCP Acceptance-Threshold-Governance control* with cross-spec uniform reporting semantics.

**Rec-R3 (ROBUST-G12 retention-cadence clause).** Add to ROBUST-G12: an explicit retention-horizon parameter, an append-only-sink-with-attestation requirement (WORM bucket or equivalent per `research/31-caremark-rsi-board-exposure.md` §5), and a board-quarterly OTEL-derived report surfacing the five-event taxonomy (prompts / tool approvals / tool execution results / MCP usage / network proxy events) per `research/followup/10-governance.md` §5 cross-ref. Without this, "co-extensive with AILCCP immutable logging" is a trappings-of-oversight claim.

**Rec-R4 (CTR-D7 same-model carve-out — evidence requirement).** Any architecture spec invoking the Anthropic same-model-judging carve-out (per `research/followup/07-evals-deepdive.md` line 280) must declare and commit, in YAML frontmatter, the held-out labeled test set used for TPR/TNR calibration, the alignment numbers achieved, and the re-calibration cadence. This is the difference between *Caremark*-defensible substrate-vendor-endorsement and Hughes-trappings. Phase-5 wave-2 ADR candidate.

**Rec-R5 (F58 / graduation re-certification clause).** Add to DPG-4: a graduation event that transitions a work-unit-class to `lights-out` triggers re-evaluation of any *external regulated-deliverable certification* held by the work product (EU AI Act Article 14 human-oversight conformity; FDA SaMD if applicable; ISO 26262 if safety-critical). The architecture spec must declare its regulated-deliverable scope at day 0 (this is mostly already implicit in ROBUST-G19's RSI declaration but should be made explicit and broader: the declaration includes *which external regulatory regimes apply to the work product*, not only RSI status).

**Rec-R6 (declared evidence in YAML frontmatter — process discipline).** The architecture-spec YAML frontmatter should be extended with a `governance-evidence` block:
- `rsi-three-part-test`: `meets | does-not-meet | uncertain-pending-graduation-N`
- `ailccp-controls-coverage`: per-control attestation at last graduation event
- `sb53-applicability`: with FLOP-threshold determination and OES reporting commitment
- `sec-iac-disclosure-readiness`: per the three-question IAC frame
- `caremark-prong-1-board-reporting-cadence`: declared and dated

This is the SEC IAC machine-readable disclosure ask answered structurally rather than retroactively. It also collapses Findings R1, R2, R3, R5 into a single audit-defensible surface.

**Closing.** The draft is substantially stronger than typical: F43/F54/F58 are correctly identified and ROBUST-G19 is the right kind of structural commitment. The remaining work is hardening the audit surface around DPG-3 and DPG-4 so that graduation events are board-visible, the AILCCP three-controls coverage is *evidenced* (not scaffolded), and log retention has a named horizon. Without the Rec-R1 graduation-attestation clause specifically, the synthesis ships with a latent *Boeing*-vector.
