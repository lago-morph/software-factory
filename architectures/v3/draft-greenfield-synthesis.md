---
artifact: draft-greenfield-synthesis
phase: 3.1
inputs:
  - tracks/greenfield-substrate-first.md
  - tracks/greenfield-methodology-first.md
  - tracks/greenfield-cold-start-first.md
bias-guard-inputs:
  - bias-guards/phase-2/anchor-detector.md
  - bias-guards/phase-2/axis-divergence-audit.md
  - bias-guards/phase-2/lumper.md
  - bias-guards/phase-2/splitter.md
based-on-commit: b65ec23a502c12706ab387b8e9fe4076c7b2f969
based-on-date: 2026-05-25
---

# Draft Greenfield Synthesis (Phase 3.1, pre-adversarial)

**Status.** Lead-agent merge of three Phase-2 greenfield tracks, marking each claim as **ROBUST** (all three tracks support, with corpus grounding) or **DECISIONS-PENDING** (tracks diverge in a way that requires a user-level decision before Phase 4). Phase-2 bias-guard findings (anchor-detector, axis-divergence, lumper, splitter) are inlined where they shift the weight of a claim.

**Discipline.** Per the [`ARCHITECTURE-V3-SYNTHESIS-PLAN`](../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md) §Phase-3.1, this draft is the *input* to the Phase-3.2 adversarial pass, not the output. ROBUST claims are candidates for `architectures/v3/greenfield-synthesis-v1.md` after the 6 adversarial subagents + cross-mandate pair land. DECISIONS-PENDING items are surfaced to the user at the Phase-3.4 checkpoint.

---

## §1 ROBUST claims (all three tracks support)

### §1.1 Operating mode / regime

- **ROBUST-G1.** Greenfield's day-0 (cold-start) regime is **L3-Augmentation**, with humans in the per-cycle inner loop. No work unit is classified `automation-eligible` (UC1 lights-out surface) at day 0; eligibility is *graduated*, not declared. All three tracks adopt some variant of brief §2.1 option (c)+(b) (regime classification + lights-out over a defined surface).
  - *Anchor-detector flag (F-ANCHOR-1, HIGH):* the option-(c)+(b) convergence is 9-of-9 across all Phase-2 tracks and inherits its shape from one sentence in the brief. The robustness of (c)+(b) itself is open for D7 blind-axis test in Phase 3.2; the underlying claim that day-0 = L3 is independently corpus-grounded (F25 design-starvation greenfield-critical; F1/F27 greenfield-critical without out-of-distribution ground truth).

- **ROBUST-G2.** Steady-state lights-out applies *only* to work units the substrate has classified `automation-eligible` after a measured graduation event. All three tracks reject blanket L5 (`no human ever`) and treat Jaymin's empirical anti-pattern claim (CodeRabbit 1.4× / Veracode 45% / METR 19% — report [`09`](../../research/09-jaymin-book-harnesses-practices-mental-models.md) §2c/§7) as binding for *un-graduated* work, not for the architecture as a whole.

- **ROBUST-G3.** Vocabulary mapping per brief §2.1 / CTR-A4: lights-out (UC1) ≠ L5 (Jaymin). The mapping is *per work-unit-class*, not architecture-wide. All three tracks invoke the brief §0 glossary definition.

### §1.2 Bootstrap / cold-start primitives

- **ROBUST-G4.** Day 0 begins with **operator-authored intent block** in El Kaim's 9-field shape (report [`14`](../../research/14-el-kaim-book-intent-and-spec-authorship.md) §3/§4.1), populated `invariants` field mandatory. The intent block is the *upstream-stable* artifact (resolves CTR-B6: invariants are the slow layer; spec body around them is the fast layer). Splitter Cluster-3 unifies this across all 9 Phase-2 tracks under `FrozenAnchor` / `InvariantBlock`.

- **ROBUST-G5.** Day 0 also requires **≥3 region-shaped scenarios** (report [`25`](../../research/25-requirements-engineering-foundations.md) INCOSE Complexity Primer principle 12; F39 region-vs-point spec) authored by the operator in Kaner-style ([`followup/09`](../../research/followup/09-methodology-ancestors.md)). Substrate refuses to start the first cycle without this. Out-of-tree storage (D-2) is *accepted with justification for greenfield* by all three tracks because there is no codebase to inherit from.

- **ROBUST-G6.** **Deterministic GtWR/EARS lint** on every spec / intent / acceptance-criterion artifact at the substrate boundary, before any build agent reads it. Substrate-typed; runs at zero marginal cost. Rules: INCOSE GtWR R7/R8/R9/R26/R35 + EARS five-pattern conformance (report [`25`](../../research/25-requirements-engineering-foundations.md) §2–§3). Fail-closed. **Not LLM-judge** — explicit refusal of F51 (Ashby-deficient probabilistic guard) at the authoring layer. Splitter Cluster-4 confirms this is uncontested across all 9 tracks; Phase-3 should adopt as substrate dependency.

- **ROBUST-G7.** **Requirement-count budgeter** on the spec: warns / chunks at the Yang et al. 10–20 simultaneous-requirement ceiling (report [`26`](../../research/26-prompt-underspecification-academic.md) §3.4, gpt-4o 98.7% → 85.0% as requirements grow 1→19). F36 (instruction-following ceiling) is structurally bounded by chunking, not by judge.

- **ROBUST-G8.** **Contradiction detection at spec layer** via behavioural disagreement across model-family-diverse paraphrasers, not LLM-judge. Larbi MCC ≤ 0.55 is treated as disqualifying for single-judge contradiction detection. F37 (silent contradictory-prompt collapse) mitigation. *Splitter Cluster-2 sub-shape (c):* this is the **paraphrase-divergence-at-spec** judge call, distinct from post-build cross-model review (sub-shape (b)) and same-model-different-role (sub-shape (a)).

### §1.3 Substrate primitives (cross-track agreement)

- **ROBUST-G9.** **Production-scissors substrate-default-off** (`PerimeterClosure`, Splitter Cluster-5). Deny-all sandbox by default; capability profiles declared per cycle; production-adjacent activity wrapped in CaMeL-class typed-interpreter boundary ([`followup/08`](../../research/followup/08-security-primitives.md) §3, ~7-point utility tax accepted per CTR-E6). Anchored on report [`32`](../../research/32-shapiro-completion-chat-agent-claw.md) §8.2 R1–R5. Defends F12/F33/F44 *as a four-layer cascade*, not one mitigation (lumper Cluster-10).

- **ROBUST-G10.** **Cross-model judge at high-stakes cycles** (`TypedJudgeCall`, Splitter Cluster-2). Anchored on CJ Hess kevin/carl (report [`34`](../../research/34-lenny-howiai-personal-harnesses.md) §6.2) and F46. *Sub-shape (b):* different-family on builder output. The three judge sub-shapes (same-model-different-role; different-family-on-builder; different-family-on-spec) are *distinct primitives* and must remain distinct in Phase-3 (lumper Cluster-1). At cold-start the corpus warrant for single-judge (Anthropic followup [`07`](../../research/followup/07-evals-deepdive.md) §3.6) does not apply because the "track record" precondition is unmet.

- **ROBUST-G11.** **Tiered watchdog Daemon / Triage / Patrol** (D-6) substrate-resident. All three tracks accept; Patrol's primary signal at cold-start is invariant-drift detection against the operator-declared intent block (the only stable layer at day 0). F22 (zombie agents) / F23 (stalled-vs-thinking) at Daemon+Triage tiers; F8/F34/F55/F57 at Patrol tier.
  - *Lumper Cluster-9 split:* "Patrol detects drift" lumps four F-modes (F34 cross-layer drift, F54 goal subversion, F55 behavioural drift, F57 design-authority erosion) into one mechanism. Phase-3 must require Patrol-mitigation claims to *name the F-mode* and *the detector* per claim.

- **ROBUST-G12.** **Trajectory capture (D-7)** content-addressed, sub-ms persist, per-event. Anchored on OpenHands V1 measurement context (report [`11`](../../research/11-openhands-substrate-audit.md) §6) cited as feasibility evidence, *not* as normative dependency (per brief §0 discipline). Co-extensive with AILCCP immutable logging.

- **ROBUST-G13.** **Hard cost ceilings non-optional (D-5)**. Per-cycle and per-day budgets in tokens, wall-clock, and tool-call-count. Substrate enforces; methodology proposes. Per-phase calibration permitted (cold-start cycles bounded smaller; steady-state larger). The 10× variance across CTR-E1 anchors (Cherny $100K/mo vs. independent $500–$5K/day) is a parameter, not a contention.

- **ROBUST-G14.** **Substrate-triggered cognitive-escrow surface** for operator touchpoints (`EscrowSurface`, Splitter Cluster-7). Reflection-question / success-criterion / similar-past-surfacing / delegation-level / STIR cascade — substrate-fired at structural moments, not operator-voluntary. Defends F42 (cognitive-escrow negligence) and F53 (voluntary-discipline fragility) at substrate, not methodology.
  - *Anchor-detector flag (F-ANCHOR-2, HIGH):* promoting Kahana's interval (report [`30`](../../research/30-cognitive-escrow.md) §3) to *substrate primitive* (vs. *phenomenology*) is single-source (one author, two papers). The phenomenon is corpus-multi-anchored (Schillace Attention Firewall, Anthropic Sensitive-Action Approval, Notion standup pre-read). Promotion to substrate primitive is itself a DECISIONS-PENDING item — see §2 DPG-7.

### §1.4 Bootstrap protections (silent-failure guards)

All three tracks land essentially the same protection set for day 0, varying only in which they call out by name:

- **ROBUST-G15.** Bootstrap cycles **cannot self-judge**. Cross-family judge mandatory; substrate refuses same-model bootstrap-judging. (F1/F27/F46 all greenfield-critical at cold-start.)
- **ROBUST-G16.** **Production access OFF** by default (ROBUST-G9 applied at cold-start with no exception).
- **ROBUST-G17.** **D-4 holdout discipline substrate-enforced** from cycle 1: bench-construction agents and builder agents never share context. Substrate-partitioned, not operator-disciplined.
  - *Lumper Cluster-2 split:* D-4 is *one discipline*, but its *enforcement locus* varies (out-of-tree directory vs. in-codebase partition vs. telemetry-as-scenario vs. co-authored-bench temporal partition). Greenfield day-0 hits the **out-of-tree directory** and **co-authored-bench temporal partition** variants; brownfield hits others. Phase-4 must split per variant.
- **ROBUST-G18.** **No `docs/solutions/`-style knowledge accumulation** during cold-start. F8 (stale-knowledge inversion) / F55 (behavioural drift in self-reference) gate accumulation until enough graduated cycles exist to evaluate the accumulated knowledge against outcomes.
- **ROBUST-G19.** **RSI-declaration day-0** (report [`31`](../../research/31-caremark-rsi-board-exposure.md) §1 three-part test). If the factory will meet Kahana's three-part RSI test at steady-state, AILCCP three-controls (Human-Approval-Gate / sandboxing / immutable logging) and Caremark prong-1 board-reporting are scaffolded *before the first cycle*. F43 (RSI Board-Visibility Gap) closed structurally, not retrofitted.

### §1.5 Defaults marking (§4 of brief)

All three tracks marked all 7 defaults. Aggregate stance for the greenfield mandate:

| Default | Greenfield stance | Justification |
|---|---|---|
| D-1 (specs durable / version-controlled / human-curated) | **accepted, all 3 tracks** | Specs are durable *the moment* an intent is promoted from `reversible` to `durable`; the intent block is the durable seed from day 0. Spec malleability (UC4) is orthogonal to durability — moving fast makes the git history rich (CTR-B7 / Nystrom). |
| D-2 (scenarios outside the codebase as holdout set) | **accepted, all 3 tracks** | Structurally the *only* coherent option for greenfield — there is no codebase to inherit scenarios from. Brief's fragile-for-brownfield flag does not bite greenfield. |
| D-3 (Agent = Model + Harness) | **mixed: 2 accepted with note, 1 challenged** | GF-M and GF-C accept with explicit acknowledgement of CTR-C10 (Portuguese-vs-English register, report [`37`](../../research/37-academic-llm-agent-collusion.md) §5). GF-S challenges: the typed-judge primitive needs "Agent = Model + Harness + Natural-Language-Register" as the more complete decomposition. **Surfaced as DPG-1 below.** |
| D-4 (holdout discipline substrate-enforced) | **accepted, all 3 tracks** | F28 (holdout leakage) is greenfield-critical; substrate enforcement is the only credible mechanism given F53 fragility. |
| D-5 (hard cost ceilings non-optional in CI) | **accepted, all 3 tracks** | See ROBUST-G13. |
| D-6 (tiered watchdog substrate primitive) | **accepted, all 3 tracks** | See ROBUST-G11. |
| D-7 (trajectory capture cheap and production-tested) | **accepted, all 3 tracks** | See ROBUST-G12. Measurement-evidence framing per brief §0 (not normative dependency). |

---

## §2 DECISIONS-PENDING (tracks diverge; user input required at Phase-3.4)

Each item names: the divergence; the specific user-actionable question; the concrete next action per ADR-0005's concrete-task discipline.

### DPG-1. D-3 decomposition: does the substrate model `Agent = Model + Harness` or `Agent = Model + Harness + Natural-Language-Register`?

- **Divergence.** GF-S §4 D-3 marks **challenged**, citing CTR-C10 / report 37 (Portuguese-vs-English policy-layer effect) and proposing that the typed-judge primitive carry prompt-template ID as a first-class parameter precisely because the harness vocabulary is insufficient to express prompt-natural-language as a behaviour-influencing parameter. GF-M and GF-C accept D-3 *with* the acknowledgement that CTR-C10 is real but treat it as a Phase-5 ADR concern, not a substrate-layer change.
- **User question.** Does the substrate primitive surface for prompts carry a typed `register` / `natural-language` field, or is that a methodology-layer detail invoked at judge-call time?
- **Concrete next action.** A Phase-5 ADR titled "Prompt-register typing at the substrate layer" — either adopted (substrate carries `register` field on every prompt artifact, methodology composes) or rejected (methodology layer owns prompt language, substrate is register-agnostic). Owner: lead agent + Phase-5 wave-1.

### DPG-2. Methodology-layer shape: thin / two-regime / three-sub-phase?

- **Divergence.** Three structurally incompatible methodology proposals:
  - **GF-S.** Methodology is *deliberately thin*: 8-step cycle (operator authors → guards run → eligibility classifier → sandbox opens → build runs → judge runs → coordination writes → Patrol audits). Unit-of-work shape, spec format, agent topology, and knowledge-accumulation pattern are all explicitly **methodology choices on top of substrate, not architectural commitments**.
  - **GF-M.** Methodology defines **two regimes** (Spec-discovery / Spec-anchored execution) with explicit transition: Regime A's unit-of-work is a *reversible commitment* (paraphrase divergence → tiny probe → promote-or-reverse); Regime B's unit-of-work is *a scenario from the durable set* (Compound-style plan→work→review→compound with cross-model review). Slice-coherence-based promotion (an end-to-end scenario passes through the slice without intent gap).
  - **GF-C.** Methodology is the **three sub-phase Bootstrap-Bench protocol** (Intent ingestion / Bench construction / First-cycle restraint) with a **measurable graduation protocol** transitioning the factory from Cold-Start Regime to Steady-State Regime per-work-unit-class. First build cycle is "deliberately tiny" — single Ubiquitous EARS criterion against single scenario, production-scissors off, cross-model judge with mandatory escalation on disagreement.
- **Axis-divergence-audit finding (§3.1).** "Effective overlap on substrate primitives is ~50–60%; effective overlap on architectural commitments at the methodology layer is <20%. Axis is doing real work." — i.e., these are not aliases. GF-S vs. GF-M overlap on substrate is ~80% by the axis-divergence audit, however, suggesting GF-S and GF-M are closer than either is to GF-C.
- **User question.** Pick one of three structural commitments for the greenfield methodology layer, or commit to a combination (e.g., GF-C's bootstrap protocol + GF-M's Regime A/B steady-state + GF-S's substrate-stack underneath).
- **Concrete next action.** A user-resolved choice at the Phase-3.4 checkpoint, before Phase-4 substrate/methodology extraction can begin. Phase-4 substrate enumeration depends on which methodology shape is canonical.

### DPG-3. Eligibility classifier: substrate primitive or methodology / policy concern?

- **Divergence.** GF-S puts the eligibility classifier at the substrate layer (S9 substrate-typed eligibility-classifier; regime is a substrate decision). GF-M expresses regime as an *operating-mode declaration* per cycle phase (methodology-layer). GF-C ties graduation to a substrate-resident protocol (per-work-unit-class graduation event).
- **Anchor-detector flag (F-ANCHOR-4, MEDIUM).** D2's mandate-fit matrix was *documentation discipline* in `decisions-captured.md`. Seven of nine Phase-2 tracks promoted it to a substrate-resident *classifier* — a non-trivial elevation. Corpus warrant for "a substrate-resident classifier that names regime and automation-eligibility per work-unit-class at cycle-open time" is weaker than the warrant for "per-work-unit regime declaration in general."
- **User question.** Is the eligibility classifier (a) a substrate primitive whose state is part of the substrate's typed object store and whose decisions are Patrol-audited, or (b) a methodology-layer policy that consumes substrate evidence (S2/S3/S4 in BF-S's terminology, intent/bench/trajectory in GF-C's) but lives in the per-architecture layer?
- **Concrete next action.** Phase-4 substrate/methodology extraction must adjudicate; if substrate, a Phase-5 wave-1 ADR ("Regime-classifier as substrate primitive") drafts the typed-object schema. If methodology, the classifier is per-architecture-spec and the substrate provides only the evidence streams.

### DPG-4. Cold-start exit criteria: which measured signals graduate the regime?

- **Divergence.**
  - **GF-S.** Substrate measures three signals: scenario-set saturation (≥N region-spec scenarios with low cross-correlation); cross-family judge stability on the work-unit-class; Patrol absence-of-drift over W cycles. *N, W are configurable; not pre-set.*
  - **GF-M.** Slice-coherence-based: a slice promotes from Regime A to Regime B when an end-to-end scenario passes through it without intent-gap. Different slices transition at different times. The empirical signal is *paraphrase-divergence-test re-run at slice scope agreeing across N paraphrasers*.
  - **GF-C.** Four explicit criteria: (1) bench saturation (≥N scenarios covering ≥M invariants, discriminative power on held-out paraphrase exceeds threshold); (2) Jaymin K=5 baseline established (≥5 invocations × ≥3 scenarios, ≥70% K=5 consistency clearable); (3) cross-model judge agreement rate measured (≥M consecutive cycles agreement); (4) RSI-declaration board-reporting cadence demonstrated (first report sent, acknowledged).
- **Lumper Cluster-9 partial unify recommendation.** The *graduation protocol primitive* (regime transition gated on measured criteria) unifies; the *specific criteria* genuinely differ. Phase-3 should adopt the primitive and leave criteria as per-architecture-spec parameters or as a user-decided default set.
- **User question.** Adopt GF-C's four-criteria set as the default graduation gate, or leave criteria as an open Phase-5 ADR parameter set?
- **Concrete next action.** If adopted, the criteria become part of the architecture spec's YAML schema (Phase 6). If deferred, Phase-5 wave-2 ADR drafts criteria after substrate-primitive shape lands.

### DPG-5. Spec-format commitment: agnostic / malleable / EARS-mandated?

- **Divergence.** GF-S is **agnostic**: "the spec can move from prose → EARS → typed-object → DOT graph across cycles; the substrate has no opinion." GF-M permits the *same* movement but treats `invariants` (within the El Kaim intent block) as the only stable subfield. GF-C **mandates EARS** for acceptance criteria and **typed-object** for the Intent Crucible, explicitly rejecting prose as F18-vulnerable.
- **User question.** Does the substrate's spec-lint primitive enforce a *specific format* (EARS for acceptance, typed-object for intent), or does it enforce a *set of properties* (deterministic-parseability, ambiguity-free per GtWR R7/R8/R9) that any conforming format may satisfy?
- **Concrete next action.** Phase-5 wave-2 ADR. Drafts: "Spec-format commitment: EARS + typed-object mandate" (GF-C side); "Spec-format agnostic with property-set lint" (GF-S side). User picks.

### DPG-6. Empirical bars: which threshold source(s) does the substrate enforce?

- **Divergence.** GF-S: substrate stores threshold sets as configurable parameters of the eligibility classifier; Jaymin's are one candidate but not adopted as defaults. GF-M: explicitly adopts Jaymin K=5 (≥70% Augmentation, ≥90% Automation) and paraphrase robustness (3-of-5 / 5-of-5) with the cycle's paraphrase step *as the K-sample mechanism*. GF-C: bench-derived bars, Jaymin as one input alongside Husain/Shankar binary-judge alignment and Anthropic same-model Auto-Review precedent.
- **Lumper Cluster-3 (lights-out-surface) related.** Brief §2.1 option (c)+(b) is a *family of answers*; the choice of *which surface* (per work-unit-class / per-stage / per-interval / per-distance / per-layer / per-cold-start-phase) interacts directly with which bar source applies — Jaymin's K=5 is measured against work units, not stages or intervals.
- **User question.** Bind to Jaymin's thresholds as the substrate-enforced default, or treat threshold sets as configurable per-deployment, or require bench-derived bars per-architecture-spec?
- **Concrete next action.** Phase-5 wave-1 ADR ("Empirical-bar source for automation-eligibility"). Three candidate decisions documented; user picks.

### DPG-7. Cognitive-escrow primitive at substrate vs. methodology layer

- **Divergence.** All three tracks invoke the cognitive-escrow surface; GF-C makes it explicitly substrate-loadable (`Cognitive-Escrow-Aware Operator Surface` as a substrate primitive in §1); GF-M treats it as a substrate primitive but with substrate firing reflection prompts *in the interval*; GF-S has it as a substrate-cadence Patrol primitive (escrow is a watched property, not a typed-object slot).
- **Anchor-detector flag (F-ANCHOR-2, HIGH).** Kahana (report 30) is *one author / one finding*; corpus has multiple voluntary-discipline-fragility surrogates (Schillace Attention Firewall, Anthropic Auto-Review sensitive-action gates, Notion standup pre-read) but the corpus does *not* multi-source the *substrate-primitive* promotion specifically.
- **User question.** Is the cognitive-escrow surface (a) a substrate-typed primitive (an `EscrowSurface` object with five sub-primitives — reflection, success-criterion, similar-past, delegation-confirm, STIR-cascade — as composable policies, per splitter Cluster-7), or (b) a methodology-layer convention that the substrate enables (via D-6 Patrol and trajectory capture) but does not type?
- **Concrete next action.** Phase-3.2 adversarial includes a D7 blind-axis test where cognitive-escrow / interval-as-substrate-primitive is *prohibited as a substrate primitive*. If the resulting alternative defends, the substrate-primitive promotion was at least partially brief-anchored. If the alternative concedes the substrate-primitive shape is correct, the promotion is genuine corpus signal. Lead agent then chooses (a) or (b) at Phase-3.4 informed by the test.

### DPG-8. F40 (last-mile drift) treatment

- **Divergence.** GF-S explicitly does *not* solve F40: "substrate enables many starts and tracks last-mile state, but bridging the agent-shaped middle vs. manual fit-and-finish tail requires methodology choices the substrate explicitly does not make." GF-M addresses F40 in Regime B's promotion criterion (end-to-end scenario must pass before slice is promoted). GF-C addresses F40 implicitly through cross-cycle slice-graduation but does not name it as a load-bearing concern.
- **User question.** Is F40 a *load-bearing methodology decision* the greenfield architecture must address (GF-M's stance), or an *open standing concern* the substrate cannot close (GF-S's stance)?
- **Concrete next action.** Phase-6 architecture spec must declare its F40 treatment; if GF-M's slice-coherence is adopted, it folds into DPG-4 (graduation criteria). If GF-S's "substrate cannot close F40" is adopted, F40 surfaces as an open Phase-7 / Phase-8 back-fill concern.

### DPG-9. Unit-of-work shape at architecture vs. methodology

- **Divergence.** GF-S: *not architectural*. GF-M: *architectural by regime* — `reversible-commitment` in Regime A; `scenario from durable set` in Regime B. GF-C: *architectural by phase* — `tiny EARS criterion against single scenario` at day 0, transitions per work-unit-class graduation.
- **Folds into DPG-2** (methodology-layer shape) — same user decision resolves this.

---

## §3 Open questions surfaced by individual tracks (preserved for Phase-3 adversarial reference)

Not promoted to DECISIONS-PENDING because each is a Phase-5/6/8 work item, not a Phase-3.4 user-checkpoint question. Listed so adversarial subagents can target them.

- **GF-S OQ-T1.** What's the minimal viable S2 scenario set size for the eligibility classifier to flip a work-unit-class regime from `augmentation-required` to `automation-eligible`?
- **GF-S OQ-T2.** Does the "four guards full stop" (F52 defense in S8) hold under methodology-imposed guards above the substrate?
- **GF-S OQ-T3.** Is the eligibility classifier itself an LLM-judge primitive? If so, does F51 (Ashby-deficient probabilistic guard) recurse into the substrate's own self-classification?
- **GF-S OQ-T4.** What happens when the slow layer (intent-block invariants) is itself moved by the operator mid-flight?
- **GF-S OQ-T5 (cited as ROBUST-G7).** Day-0 operator labor cost is irreducible at bootstrap; can the substrate scaffold an interview-style cycle to help?
- **GF-M OQ-T1.** Slice coherence as Regime A→B transition criterion is operationally underdefined.
- **GF-M OQ-T2.** Paraphrase fan-out cost (~Nx) interaction with D-5 ceiling is unresolved at the Cherny vs. independent scale.
- **GF-M OQ-T3.** Regime A→Regime B handoff requires a substrate protocol that does not exist in the corpus.
- **GF-M OQ-T4.** Cross-model paraphrase divergence presupposes multi-provider access; interaction with OQ-B8 (provider abstraction) unresolved.
- **GF-M OQ-T6 (biggest).** Whether paraphrase divergence is adequate as F37 defense, or whether the Larbi MCC ≤ 0.55 anchor generalises to the multi-paraphraser case in ways the corpus does not measure. Phase-8 lean-eval candidate.
- **GF-C OQ-1.** Concrete bench-saturation N and M values (deferred to Phase-6 ADR).
- **GF-C OQ-2.** Does cold-start vs. steady-state phase belong as an organising axis in the v3 set (OQ-B7 candidate)?
- **GF-C OQ-3.** Is "micro-cold-start per new work-unit-class" architectural or methodological?
- **GF-C OQ-4.** Cross-model judge cost scale at cold-start (Cherny / noosphr anchors silent on cold-start specifically).
- **GF-C OQ-5.** Does the Intent Crucible's typed-object discipline create CTR-C10 / F50-class architecture/specification confusion?
- **GF-C OQ-6 (biggest).** What if the Intent Crucible itself cannot be authored at day 0 — operator-intent-illiteracy as the architecture's biggest unresolved exposure?

---

## §4 Citations and grounding

This draft cites only what is cited in the three Phase-2 tracks. New citations added at this merge level:

- **Phase-2 bias-guard outputs** (anchor-detector, axis-divergence-audit, lumper, splitter) — cited as Phase-2 findings, not as corpus authority (per the bias-guard discipline in [`decisions-captured.md`](decisions-captured.md) D5).
- **Brief §0 glossary, §2.1, §3, §4.1, §5** — the framing this draft inherits.
- **[`decisions-captured.md`](decisions-captured.md)** — D1, D2, D3, D5, D7 — discipline this draft applies.

All other claims trace back through the three Phase-2 greenfield tracks to underlying reports / followups / contradictions.

---

## §5 Phase-3.2 adversarial dispatch notes

The 6 persona-adversarial subagents (red-team, pre-mortem, regulator, CFO, 10-year on-call, naive newcomer) attack this draft. Specific instructions per persona that the dispatcher should encode:

- **Red-team.** Target ROBUST-G1 (the option (c)+(b) convergence). Anchor-detector flagged this as the highest brief-anchored claim. Pre-respond expected: argue brief §2.1 options (a), (d), or (e) from corpus.
- **Pre-mortem.** Target DPG-2 (methodology-layer shape). 6 months in: which of GF-S / GF-M / GF-C fails first, and how?
- **Regulator.** Target ROBUST-G19 (RSI declaration day-0) and DPG-3 (eligibility classifier). Is the AILCCP three-controls + Caremark prong-1 scaffolding sufficient for SB 53 / SEC IAC obligations, or does the graduation protocol create new regulator-visible surfaces?
- **CFO.** Target ROBUST-G10 (cross-model judge) and DPG-4 (graduation criteria). What is the cost-per-graduation, and how does cross-family judging at cold-start interact with CTR-E1 / CTR-E6?
- **10-year on-call.** Target the entire bootstrap protection set (§1.4). Which protection breaks first when the factory has been running 18 months, the operator who authored the original Intent Crucible has rotated out, and a new operator inherits the running factory?
- **Naive newcomer.** Target the entire draft for jargon, hidden anchors, places where the doc smuggles in unstated context. Specifically: is the EscrowSurface primitive's status (substrate vs. methodology, DPG-7) understandable to someone who has not read Kahana's papers?

Additional D7 blind-axis test (anchor-detector recommendation):
- **D7-G-1.** Subagent dispatched with the instruction: "address brief §2.1 OQ-B1 for the greenfield mandate without using option (c) or option (b). Defend an (a), (d), or (e) resolution from the corpus." If a defensible alternative emerges, ROBUST-G1 partially demotes; if the subagent concedes (c)+(b), ROBUST-G1 confirms.
- **D7-G-2.** Subagent dispatched with the instruction: "draft a greenfield architecture whose substrate primitives do *not* include a cognitive-escrow / EscrowSurface / interval-as-typed-object primitive. If a defensible alternative emerges, DPG-7 resolves to methodology-side; if not, the substrate-primitive promotion is genuine corpus signal."

---

*End of draft-greenfield-synthesis.md (Phase-3.1).*
