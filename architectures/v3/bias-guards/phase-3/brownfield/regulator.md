---
guard: regulator
target: draft-brownfield-synthesis
phase: 3.2
based-on-commit: e02d0ba
based-on-date: 2026-05-25
---

# Phase-3.2 regulator critique — brownfield draft

## §1 Persona stance

I read this draft as outside regulatory counsel auditing a system that the firm's CTO has begun describing as a "software factory." My loyalty is to the board's defensibility surface under Delaware Caremark, to operational compliance with SB 53's "internal use" reporting trigger, to the SEC IAC's three disclosure questions, and to the AILCCP three-RSI-controls triad. The draft's brownfield architecture **plausibly** satisfies Kahana's three-part RSI test (durable self-modification of the codebase model and accumulated skills; compounding via attribution-store and Compound-Knowledge typed records; limited human gating once work-unit-classes graduate to L4). That puts the design squarely in the regime where Marchand mission-critical-risk reporting attaches and where Hughes-style "trappings of oversight" is the most likely failure shape.

## §2 Top regulator findings

### Finding R1 — Per-region regime classification is a Caremark prong-1 aggregation failure surface (HIGH)

**Target.** DPB-6 contemplates per-(work-unit-class × code-region) eligibility classification. BF-L's own §7 question 4 already flags this concern.

**Audit gap.** A factory whose regime varies by code region cannot produce **one coherent board-level risk summary** answering Kahana's three operational questions. The board instead receives an N-row table where the aggregation rule from "5 regions running L4, 12 regions at L3, 33 regions at L3-augmented-with-cross-family-judge-disabled-by-cost-ceiling" → "does the deployment meet the RSI test?" is *not specified by the architecture*. This is the Hughes v. Hu "trappings of oversight" trap: the audit committee receives information that *appears* granular and rigorous but cannot answer the Marchand mission-critical-risk inquiry as a single yes/no with provenance. The SEC IAC's question 2 becomes *unanswerable as posed*.

### Finding R2 — `AttributedEventLog` doesn't specify integrity, retention, or jurisdictional residency (HIGH)

**Target.** ROBUST-B10: "Trajectory capture (D-7) and immutable attribution (`AttributedEventLog`) substrate-resident, content-addressed, signed."

**Audit gap.** AILCCP names *Intervention Audit Trail* and *Context-to-Output Lineage* as the controls. The draft says "content-addressed, signed, HMAC where coordination crosses an unsigned boundary." It does **not** say: where the append-only sink lives; whether it is WORM-attested; what retention horizon; what happens when a region's data-residency regime forbids exporting trajectory events outside-jurisdiction; what the verification path is from a regulator's *"show me the AI's reasoning for this 2026-Q3 commit"* request back to a reproducible artifact. Boeing's holding is precisely that *design choices that disable board-level monitoring can ground Caremark liability*.

### Finding R3 — Brownfield codebases inherit prior-regime compliance obligations that the architecture neither inventories nor preserves (CRITICAL for regulated brownfield)

**Target.** ROBUST-B1 / ROBUST-B13: brownfield is code-archaeological; legacy-ingestion reads the existing codebase, tests, telemetry, history.

**Audit gap.** Nothing in the draft inventories the codebase's **inherited regulatory commitments** before the first cycle runs. A codebase whose tests presume HIPAA Safe Harbor de-identification, PCI-DSS Requirement 6.5 secure-coding-practice traceability, SOX 404(b) ICFR change-management evidence, or FDA SaMD V&V cycle attestation comes with *design-time certifications*. Once an L3-or-L4 cycle modifies that codebase, the architecture has performed F58. Worse: under F30 brownfield-critical, the *certification itself silently lapses*. ROBUST-B13's legacy-ingestion step does not produce an inherited-compliance-obligations register; ROBUST-B4's five-sub-store model has no view for "inherited compliance artifacts the existing codebase ships with."

### Finding R4 — Telemetry-bootstrap (DPB-9) is itself an SB 53 / Caremark-visible event the architecture does not flag (MEDIUM-HIGH)

**Audit gap.** Each DPB-9 option has different regulatory visibility:
- **Option (a) gating refusal** — defensible; clean record-creating event.
- **Option (b) degraded acceptance** — *not defensible*. The factory begins recursive self-modification of a codebase whose own runtime invariants it cannot observe; that is precisely Kahana's first RSI condition without the immutable-logging control's *Detective* function operational.
- **Option (c) telemetry-as-pre-cycle setup** — defensible *only if* the setup cycle is itself attributed and bounded.

### Finding R5 — Per-cycle attribution does not yet support "show me the AI's reasoning for this decision" reconstruction (HIGH)

**Audit gap.** A regulator request is **not "what model was used"** but *"reconstruct the chain of reasoning the system used to make decision X."* The draft enumerates *attribution dimensions* (agent / model / prompt) but not *reasoning-trace defensibility*. The draft's F58 mitigation row says "Trajectory + telemetry views share the attribution store" — that is *availability of inputs*, not *defensible reconstruction of outputs*. A factory operating across DPB-6 per-region regimes will be asked: "for region X, on commit Y, the deployed code violated invariant Z; reconstruct *why the factory believed* the change was eligible for L4-lights-out." The architecture has no named reconstruction protocol.

## §3 What the architecture defensibly satisfies

The draft is **substantially stronger than its predecessors** on three AILCCP fronts. ROBUST-B5 (production-scissors substrate-default-off) is the explicit *Agent Kill Switch* + *Rate and Scope Limiter* substrate; ROBUST-B6 (D-4 substrate-enforced via role-partitioning) is the *Confidential Computing Environment* posture; ROBUST-B10 names the immutable-logging slot. Together these cover the AILCCP three-RSI-controls triad in *intent* — Human-Approval-Gate (cycle step 8), sandboxing (B5 + B6), immutable logging (B10).

Additionally, ROBUST-B9 (tiered Daemon/Triage/Patrol) and the F34/F54/F55/F57/F58 mitigation rows give the architecture an explicit *Continuous Validation* + *Intervention Audit Trail* posture. ROBUST-B11 (hard cost ceilings as Acceptance Threshold Governance proxy) and DPB-5/DPB-7 (eligibility classifier as the substrate site where Acceptance Threshold lives) — *if* the open questions resolve with regulator-defensibility as a weighting factor.

## §4 Concrete recommendations for Phase-3.4

1. **ROBUST-B10 engineering specification ADR (Phase-5 wave-1, regulator-counsel-reviewed).** Must specify: append-only sink residency by jurisdiction; WORM attestation; signing key custody; retention horizon per regulated regime; the reconstruction protocol from a single commit-hash to "the reasoning the factory used at that decision."

2. **Add ROBUST-B15 (proposed): Inherited-compliance-obligations register as a sixth codebase-model sub-store.** ROBUST-B4's five sub-stores miss the inherited compliance surface. Add: *Compliance / certification inheritance view* — the existing codebase's HIPAA / PCI-DSS / SOX / FDA-SaMD / ISO-26262 / EU-AI-Act certification artifacts. The legacy-ingestion phase (ROBUST-B13) must produce this register on day 0.

3. **Resolve DPB-6 with a Caremark-aggregation gate.** Phase-3.4 user resolution on per-region vs per-work-unit-class regime must include an explicit *board-summary aggregation rule*: if per-region wins, the architecture must declare how N region-summaries roll up into one *"does the deployment meet Kahana's three-part RSI test?"* answer.

4. **Resolve DPB-9 with a regulator-counsel sign-off gate.** Default to option (a) gating refusal unless counsel signs off on degraded acceptance.

5. **Add an F-mode catalog entry for "inherited-certification lapse" or widen F58 explicitly.** Either widen F58's mechanism text or promote a new F-mode (F62 candidate, *Inherited-Certification Lapse*) with brownfield-critical severity.

6. **Cross-mandate dispatch note:** the per-region regime question is a *brownfield-specific* defensibility surface; greenfield does not inherit pre-existing regions with distinct regimes. Structural argument *for* the cannot-unify side.

7. **Add explicit AILCCP-coverage-table to §1.6.** The §1.6 F-mode mitigation table should be supplemented with an AILCCP-48-controls coverage row.

**Summary.** The brownfield draft is regulator-aware but is *not yet regulator-defensible*. The gap is engineering specification of ROBUST-B10, an explicit inherited-obligations sub-store, and DPB-6's aggregation rule.
