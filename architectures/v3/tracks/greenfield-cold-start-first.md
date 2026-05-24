---
track: greenfield-cold-start-first
axis: cold-start-first
mandate-scope: greenfield
based-on-commit: 96a949430b5c356f8b4e688b1d427348a68db468
based-on-date: 2026-05-24
---

# Track — Greenfield, cold-start-first

> Sub-axis: **Day-0 bootstrap is the load-bearing problem.** Architect the factory around getting through the first hour, the first day, and the first cycle before any scenario, any `docs/solutions/`-class artifact, any prior trajectory, and any holdout suite exists. Steady-state operation is treated as a downstream emergent regime, not the design center.

---

## §0. Axis declaration and defense (pre-respond to Phase-3 adversarial)

The brief ([`00-brief-v3.md`](../00-brief-v3.md) §5) elevated cold-start from open question OQ-B5 to a *mandatory dedicated synthesis section* on the grounds (Historian M4) that the user's [`research-plan.md`](../../../archive/research-plan.md) ranks it as "the load-bearing risk of the greenfield mandate." This track takes the further step: cold-start is the *organizing principle*, not a section. Three defenses, anticipating Phase-3 attack:

1. **Cold-start is the moment where every steady-state assumption is structurally false.** D-2 (scenarios as out-of-tree holdout, [`00-brief-v3.md`](../00-brief-v3.md) §4.1) has no holdout. D-4 (holdout discipline substrate-enforced) has nothing to enforce against. D-7 (trajectory capture is cheap and production-tested, anchored on OpenHands V1's 433-replay benchmark per [`11-openhands-substrate-audit`](../../../research/11-openhands-substrate-audit.md) §6) has no prior trajectories to replay. F1 (Hallucination Loop, [`failure-modes-v3`](../failure-modes-v3.md) §1 F1: builder + judge sample the same distribution) is at maximum severity (`critical` per F1 greenfield rating) because *the judge IS the only signal*. F25 (Design starvation, `failure-modes-v3.md` §2 F25 greenfield severity `critical`) is the cold-start regime explicitly named. F40 (Last-Mile Drift) and F41 (Under-Defined-Intent Debt) — both at greenfield severity `critical` per [`failure-modes-v3`](../failure-modes-v3.md) §5 — are also cold-start phenomena. Five `critical`-rated F-modes converge on day 0. An architecture that lands the steady-state right but the cold-start wrong ships nothing.

2. **Anticipated attack: "Cold-start is one phase; the rest of the factory dwarfs it." Response:** The corpus' empirical anchors are *all post-cold-start observations*. Cherny's 5-Claudes-steady-state ([`followup/03-cherny-interview`](../../../research/followup/03-cherny-interview.md), 10–30 PRs/day, 100% Claude-written since Nov 2025) is a *Year-N* report, not a day-0 report. Stripe's 1,300 PRs/week (Nystrom citing Stripe, [`35-lenny-howiai-spec-driven-and-team-ops`](../../../research/35-lenny-howiai-spec-driven-and-team-ops.md)) is Year-N. Every architectural inheritance from those anchors smuggles in pre-existing scenarios, pre-existing tests, pre-existing telemetry, and pre-existing team mental models. The corpus has *no primary anchor* for the first day of a lights-out greenfield factory. That gap is the design space.

3. **Anticipated attack: "You're just restating the cold-start section other tracks will include." Response:** A track that organizes around cold-start makes choices the section-treatment tracks cannot. Specifically: (a) the substrate's day-0 primitives are different from its day-N primitives — the architecture must declare both; (b) the regime classification is *cold-start regime → steady-state regime*, not a single regime; (c) the human re-entry mechanism (OQ-B3) is differently structured during cold-start (when there is no track record) than during steady-state (when watchdog Patrol-tier escalation has historical baselines); (d) the empirical bars from OQ-B6 (Jaymin's K=5 ≥90% Automation Mode, [`09-jaymin-book-harnesses-practices-mental-models`](../../../research/09-jaymin-book-harnesses-practices-mental-models.md) §5.5) *cannot be measured at day 0* because there is no run history to compute K=5 over. Cold-start-first forces an honest answer.

**Vocabulary clarification (per brief §2.1 / CTR-A4).** This track uses "lights-out" per the glossary §0 definition (no human in per-cycle inner loop *for automation-eligible work units*; humans set policy, sample-audit, watchdog-respond, declare re-entry). It does NOT assume "lights-out = L5." On the contrary, the cold-start period is explicitly designed as **L3/L4 with no automation-eligible work units yet declared**; automation-eligibility is itself a *graduated discovery* of the cold-start phase. See §2 OQ-B1 treatment.

---

## §1. Architecture sketch

**Name (working):** **Bootstrap-Bench Factory.** A factory whose substrate and methodology distinguish two regimes — a **Cold-Start Regime** (no scenarios, no priors, no track record) and a **Steady-State Regime** (everything D-2 / D-4 / D-7 assume) — with an explicit **graduation protocol** between them. The factory's day-0 deliverable is not code; it is a *bench*: a small, human-anchored scenario+invariant+intent corpus rich enough to make D-4 holdout discipline non-vacuous and rich enough to permit F1/F27 mitigation to operate. Code generation is *gated* on bench sufficiency.

### 1.1 The five day-0 primitives (substrate)

These are the primitives a greenfield factory needs *before any cycle runs*. Every primitive is anchored in the cold-start required reading.

1. **Intent Crucible** (anchored on [`14-el-kaim-book-intent-and-spec-authorship`](../../../research/14-el-kaim-book-intent-and-spec-authorship.md) §3 9-field intent block + [`25-requirements-engineering-foundations`](../../../research/25-requirements-engineering-foundations.md) §3 INCOSE GtWR C1–C15). A typed-object intake (9 fields: identity, statement, business outcomes, capability scope, policy references, invariants, non-goals, decision seeds, guardrails, feedback sources) that captures the human's day-0 intent before any LLM has touched it. Authoring is a human-only act; the substrate provides the template, the validator, and the version-control discipline. *Specifically rejects the spec-malleable framing as the upstream practice* (per CTR-B6: El Kaim's invariants are "non-negotiable conditions any valid realization must preserve"). Spec malleability is permitted *downstream of* the Intent Crucible, never upstream.

2. **EARS-mandated Acceptance Criteria** (anchored on [`25-requirements-engineering-foundations`](../../../research/25-requirements-engineering-foundations.md) §2 Mavin EARS five-pattern grammar — Rolls-Royce, adopted by Airbus / Bosch / Dyson / Honeywell / Intel / NASA). At cold-start, prose acceptance criteria are F18-vulnerable (greenfield severity `high` per [`failure-modes-v3`](../failure-modes-v3.md) §1 F18) because ambiguity dominates and there is no existing code to disambiguate against. The five EARS patterns (Ubiquitous / State-driven / Event-driven / Optional-feature / Unwanted-behaviour) are the smallest grammar that makes acceptance criteria deterministically parseable by both a builder and a judge. F38 (Vocabulary lint debt, [`failure-modes-v3`](../failure-modes-v3.md) §4 F38) mitigation: a deterministic GtWR R7/R8/R9 linter runs at the authoring boundary, rejecting hedging language before it enters the bench. This is *deterministic perimeter*, not LLM-judge — addressing F51 (Ashby-deficient probabilistic guard, [`failure-modes-v3`](../failure-modes-v3.md) §4a F51 greenfield severity `high`) at the authoring layer.

3. **Cold-Start Bench** (the day-0 holdout, addressing D-2's vacuousness on day 0). A small human-authored scenario set in Cem Kaner's 2003 scenario-testing tradition ([`followup/09-methodology-ancestors`](../../../research/followup/09-methodology-ancestors.md): story / motivating / credible / complex / easy-to-evaluate / power). Stored outside the codebase per D-2. The bench is *the* day-0 ground truth — the only out-of-distribution signal available before code exists. *Bench size is itself a graduation metric* (see §1.3). F36 (Instruction-following ceiling, gpt-4o 98.7%→85.0% as requirements grow 1→19, [`26-prompt-underspecification-academic`](../../../research/26-prompt-underspecification-academic.md) §3.4) drives a **chunking discipline**: bench scenarios are sized so any single cycle exposes ≤10 simultaneous requirements to the builder.

4. **Cognitive-Escrow-Aware Operator Surface** (anchored on [`30-cognitive-escrow`](../../../research/30-cognitive-escrow.md) §1–3 Kahana). At cold-start, the human is *necessarily* in the per-cycle inner loop (no automation-eligible work units have been declared yet). The substrate must treat the prompt→response interval as a first-class design surface, not as latency. The Schillace "Attention Firewall" ([`28-schillace-sunday-letters`](../../../research/28-schillace-sunday-letters.md) §6) and Notion's standup pre-read ([`35-lenny-howiai-spec-driven-and-team-ops`](../../../research/35-lenny-howiai-spec-driven-and-team-ops.md)) are the two corpus exemplars; the day-0 instance is *STIR-in-the-interval* (Kahana, [`30-cognitive-escrow`](../../../research/30-cognitive-escrow.md) §3) implemented as a substrate-triggered structural pause, not as voluntary operator discipline. This is the day-0 mitigation of F53 (Voluntary-discipline fragility, [`failure-modes-v3`](../failure-modes-v3.md) §5a F53 greenfield severity `high`).

5. **RSI-Declaration Ledger** (anchored on [`31-caremark-rsi-board-exposure`](../../../research/31-caremark-rsi-board-exposure.md) §1 Kahana three-part RSI test + [`followup/10-governance`](../../../research/followup/10-governance.md) §1.1 BCG "auditability by design"). On day 0, the factory commits to whether it will meet Kahana's three-part RSI test (durable self-modification + compounding ability + limited human gating) at steady-state. If yes, the AILCCP three controls (Human Approval Gate / sandboxing / immutable logging) and the Caremark prong-1 board reporting structure are scaffolded *before the first cycle runs*. F43 (RSI Board-Visibility Gap, [`failure-modes-v3`](../failure-modes-v3.md) §5 F43) is structurally closed at day 0 rather than retrofitted at day N. The ledger is BCG's "complete, versioned audit trail" ([`followup/10-governance`](../../../research/followup/10-governance.md) §1.1 verbatim) instantiated from cycle 1.

### 1.2 The cold-start methodology — three sub-phases

**Sub-phase A — Intent ingestion (human-dominant).** The human authors 1–3 Intent Crucible blocks. A *Council* of agents (anchored on [`16-el-kaim-book-council-and-delegation`](../../../research/16-el-kaim-book-council-and-delegation.md) Council pattern; family-diverse model-mix per F46 mitigation) interrogates each block with structured questions drawn from El Kaim's 9-field schema and INCOSE GtWR C3 (unambiguous) / C5 (singular) / C7 (verifiable). The human is in the loop. The output is a Crucible block that has been adversarially questioned by ≥2 model families. The Council does not write code.

**Sub-phase B — Bench construction (human-anchored, agent-assisted).** Human seeds 5–10 scenarios in Kaner-style prose. Agents (different model family from the eventual builder, per F46) propose additional scenarios; human accepts/rejects/edits. Each scenario is bound to ≥1 EARS acceptance criterion and ≥1 Intent Crucible invariant. The bench is *signed* (per F32: HMAC on coordination messages, [`failure-modes-v3`](../failure-modes-v3.md) §2 F32) and stored outside the soon-to-be codebase tree (D-2). Bench-construction agents *never see* the eventual builder's prompts (D-4 holdout discipline made non-vacuous).

**Sub-phase C — First-cycle restraint.** The first build cycle is *deliberately tiny* — a single Ubiquitous-pattern EARS criterion against a single scenario. Cycle output is judged by the Council (cross-model per CTR-D7-position, [`contradictions.md`](../contradictions.md) CTR-D7: Anthropic single-judge finding *plus* CJ Hess `kevin`/`carl` cross-model — *both* are run; if they disagree, the human is escalated). Production scissors (F44, [`failure-modes-v3`](../failure-modes-v3.md) §5 F44) are OFF; the cycle ships to a sandbox only. The substrate enforces the production-scissors-off default per F44 mitigation.

### 1.3 The graduation protocol (cold-start → steady-state)

The factory transitions from Cold-Start Regime to Steady-State Regime only when explicit, measured criteria are met. Per [`30-cognitive-escrow`](../../../research/30-cognitive-escrow.md) §3 (substrate-triggered structural discipline > voluntary operator discipline) and per CTR-A4 (vocabulary mapping: L4 ≠ L5), graduation is gated on:

- **Bench saturation.** Bench contains ≥N scenarios covering ≥M Intent Crucible invariants such that the bench's discriminative power on a held-out paraphrase of the spec exceeds a stated threshold. (Concrete N/M deferred to Phase-6 ADR; the *requirement* that they be stated is the architectural commitment.)
- **K=5 consistency baseline established.** The factory has run ≥5 independent invocations on each of ≥3 bench scenarios and Jaymin's Augmentation-Mode bar (≥70% K=5 consistency, [`09-jaymin-book-harnesses-practices-mental-models`](../../../research/09-jaymin-book-harnesses-practices-mental-models.md) §5.5) is clearable for at least the work-unit-classes proposed for automation-eligibility. This addresses OQ-B6 directly: at cold-start, the bars *cannot be measured*; graduation requires measuring them.
- **F1/F27 cross-model judge agreement rate measured.** Per F46 mitigation: cross-model review must have produced ≥M consecutive cycles of agreement on the bench. If the cross-model judges disagree at high rate, the bench is not yet rich enough.
- **RSI-declaration board-reporting cadence demonstrated** (per F43). If the factory has declared it will meet Kahana's three-part test at steady-state, the board has received at least one structured report and acknowledged it.

Until graduation, the factory operates at L3-Augmentation (per [`09-jaymin-book-harnesses-practices-mental-models`](../../../research/09-jaymin-book-harnesses-practices-mental-models.md) §5.5 Augmentation Mode thresholds) with the human in every cycle. Post-graduation, work units are classified per [`decisions-captured.md`](../decisions-captured.md) D2 mandate-fit-by-work-unit-class; only the automation-eligible classes operate at L4-lights-out. **This is the option (c)+(b) treatment of OQ-B1 the brief §2.1 named as the lead-agent's working stance**, made concrete: cold-start declares the regime is L3, names the work-unit-classes that will graduate, and measures the graduation.

### 1.4 What sits below this — substrate primitives the methodology consumes

This track does not pre-decide the substrate enumeration (per Skeptic #14, brief §1 / `decisions-captured.md` D4). It does name the *day-0-load-bearing* primitives that have to exist before the methodology can run: typed-object Intent storage with version control; deterministic GtWR/EARS linter (NOT an LLM judge — addresses F51 Ashby-deficiency at authoring layer); signed scenario store (HMAC per F32); cross-model judge router (F46 mitigation, OpenHands-V1-class per [`11-openhands-substrate-audit`](../../../research/11-openhands-substrate-audit.md) §6, though *not* a normative dependency); cognitive-escrow-aware operator surface (per [`30-cognitive-escrow`](../../../research/30-cognitive-escrow.md) §3); structural production-scissors-off default (F44); RSI-declaration ledger with board-reporting hooks. Trajectory capture (D-7) is *desired but not load-bearing on day 0* — there are no trajectories yet — but its substrate must exist by graduation.

---

## §2. How this addresses each load-bearing concern

### Cold-start (the axis itself)

Treated as the primary design problem, not a section. See §1 and §5.

### Lights-out / L5 tension (brief §2.1, OQ-B1)

**Resolved as option (c) + (b) per brief §2.1**: regime is *declared per work-unit-class and per cold-start vs. steady-state phase*. Cold-start phase is *uniformly L3-Augmentation* regardless of work-unit-class (no automation-eligible units have been declared yet). Steady-state phase classifies per [`decisions-captured.md`](../decisions-captured.md) D2 matrix. **Vocabulary discipline (CTR-A4):** the track treats "lights-out" ≠ L5; lights-out applies to the *automation-eligible work-unit-class surface* declared at graduation, and the bars used for the declaration are *measured on the bench*, not inherited from Jaymin. This sidesteps CTR-A1 (Shapiro vs. Jaymin), CTR-A2 (Shapiro self-position L4), CTR-H10 (Round-2 ceiling vs. UC1) — none of them bite because the track never claims L5. CTR-A5 (Jaymin's brownfield L3 ceiling) does not apply because mandate is greenfield.

### UC4 (greenfield is spec-malleable; falsifiability)

**Partially confirmed, partially challenged.** Confirmed: cold-start *requires* malleable downstream specs (the bench grows, the EARS acceptance criteria refine, decision seeds resolve). Challenged: per CTR-B6 (El Kaim invariants vs. UC4 spec-malleable), the *upstream* intent block is **not** malleable — non-negotiable invariants are the upstream anchor that protects against confabulation. The track's answer: malleability is a *downstream* property of acceptance criteria and decision seeds; *upstream* invariants are fixed. UC4's framing is correct about the architecture being malleable; it is incorrect (or at minimum incomplete) about the *intent* being malleable. This is the cold-start track's substantive contribution to UC4 hypothesis testing.

### Cold-start (mandatory per brief §5 — full §5 below)

See §5.

### OQ-B1 (lights-out / L5 / regime)

See "Lights-out / L5 tension" above. Treated head-on.

### OQ-B3 (human re-entry mechanism)

Cold-start *inverts* the question: the human is *in* the loop by default during cold-start; the substrate-level protocol is for the human to *leave* the loop (graduation), not to re-enter it. Post-graduation re-entry triggers are tied to the same metrics that gated graduation (K=5 consistency falling below Augmentation bar, cross-model judge disagreement rate spiking, F1/F27 cascade detection by Patrol-tier watchdog per D-6 [`failure-modes-v3`](../failure-modes-v3.md) §2 F21-F23 watchdog cadences). The substrate protocol: any of these tripwires causes the affected work-unit-class to be *de-graduated* back to Augmentation Mode and the human re-enters that class's loop. The board is notified per F43 / RSI Ledger if the factory has declared itself RSI.

### OQ-B5 (now brief §5 — cold-start required reading)

All five required-reading inputs ([`25`](../../../research/25-requirements-engineering-foundations.md), [`26`](../../../research/26-prompt-underspecification-academic.md), [`30`](../../../research/30-cognitive-escrow.md), [`31`](../../../research/31-caremark-rsi-board-exposure.md), [`followup/10`](../../../research/followup/10-governance.md)) are load-bearing for this track's primitives — see §1 and §5.

### OQ-B6 (which empirical bars)

**Answered: bars measured on the bench, not inherited.** Jaymin's K=5 ≥70%/≥90% and prompt-paraphrase robustness ≥3-of-5 / 5-of-5 ([`09-jaymin-book-harnesses-practices-mental-models`](../../../research/09-jaymin-book-harnesses-practices-mental-models.md) §5.5) are *candidate* bars but the bench is the *target* against which they are measured. CTR-E3 (CodeRabbit / Veracode / METR refute lights-out *vs.* applicability caveats) is sidestepped: those numbers were measured against populations the cold-start factory cannot map onto until it has its own bench measurements. **Honesty discipline:** at cold-start the factory cannot claim to have cleared *any* empirical bar; the graduation protocol is the act of earning the claim.

### OQ-B9 (methodology evolution as substrate or per-architecture)

This track treats methodology evolution as *per-architecture* during cold-start (the methodology is being discovered) and *substrate-tracked* post-graduation (the Compound Knowledge or Beads-class `discovered-from` edge, [`38-gas-systems-substrate`](../../../research/38-gas-systems-substrate.md), captures evolution). The transition is itself part of the graduation protocol.

### OQ-B4, OQ-B7, OQ-B8, OQ-B10

OQ-B4 (brownfield unit-of-work) is out of scope per mandate. OQ-B7 (organizing axes beyond mandate): this track is a partial answer — *cold-start-vs-steady-state phase* is a load-bearing axis the brief did not name. OQ-B8 (provider-property requirements): the track requires cross-model-family diversity for the Council/judge layer (F46 mitigation); RouterLLM-class abstraction is *useful but not normative*. OQ-B10: process discipline, not architectural.

---

## §3. Citations and grounding

Load-bearing claims by §1 primitive, with corpus anchors:

- **Intent Crucible** — [`14-el-kaim-book-intent-and-spec-authorship`](../../../research/14-el-kaim-book-intent-and-spec-authorship.md) §3 (9-field block); [`25-requirements-engineering-foundations`](../../../research/25-requirements-engineering-foundations.md) §3 (INCOSE GtWR C1–C15 1:1 mapping); CTR-B6 ([`contradictions.md`](../contradictions.md): El Kaim invariants structurally reject upstream spec-malleability — this track's challenge to UC4).
- **EARS-mandated Acceptance Criteria** — [`25-requirements-engineering-foundations`](../../../research/25-requirements-engineering-foundations.md) §2 (Mavin EARS five-pattern, Rolls-Royce + Airbus/Bosch/Dyson/Honeywell/Intel/NASA adoption); F18 ([`failure-modes-v3`](../failure-modes-v3.md) §1, greenfield `high`); F38 ([`failure-modes-v3`](../failure-modes-v3.md) §4, vocabulary lint debt, greenfield `high`); F36 ([`failure-modes-v3`](../failure-modes-v3.md) §4, instruction-following ceiling, greenfield `critical`; Yang et al. 98.7%→85.0% as 1→19 requirements via [`26-prompt-underspecification-academic`](../../../research/26-prompt-underspecification-academic.md) §3.4); F51 Ashby-deficiency ([`failure-modes-v3`](../failure-modes-v3.md) §4a, greenfield `high`).
- **Cold-Start Bench** — [`followup/09-methodology-ancestors`](../../../research/followup/09-methodology-ancestors.md) (Kaner scenario-testing); D-2 ([`00-brief-v3.md`](../00-brief-v3.md) §4.1, scenarios-outside-codebase); D-4 (holdout discipline substrate-enforced); F28 ([`failure-modes-v3`](../failure-modes-v3.md) §2 F28, holdout leakage greenfield `critical`); F37 ([`failure-modes-v3`](../failure-modes-v3.md) §4 F37, silent contradictory-prompt collapse GPT-4 73.8%→6.7% via [`26-prompt-underspecification-academic`](../../../research/26-prompt-underspecification-academic.md) §6.1–6.2, greenfield `critical`).
- **Cognitive-Escrow Operator Surface** — [`30-cognitive-escrow`](../../../research/30-cognitive-escrow.md) §1–3 (Kahana phenomenological state; STIR critique; substrate-level antidote to voluntary-discipline fragility); F42 ([`failure-modes-v3`](../failure-modes-v3.md) §5 F42); F53 ([`failure-modes-v3`](../failure-modes-v3.md) §5a F53, voluntary-discipline-fragility Kahana-class, greenfield `high`); [`28-schillace-sunday-letters`](../../../research/28-schillace-sunday-letters.md) §6 (Attention Firewall, corpus' first concrete interval-as-design-site exemplar).
- **RSI-Declaration Ledger** — [`31-caremark-rsi-board-exposure`](../../../research/31-caremark-rsi-board-exposure.md) §1 (Kahana three-part RSI test; mid-market scope); §2 (Caremark spine); F43 ([`failure-modes-v3`](../failure-modes-v3.md) §5 F43 RSI Board-Visibility Gap); F54 ([`failure-modes-v3`](../failure-modes-v3.md) §5a F54 goal subversion, greenfield `high`); F55 ([`failure-modes-v3`](../failure-modes-v3.md) §5a F55 behavioural drift, greenfield `critical`); [`followup/10-governance`](../../../research/followup/10-governance.md) §1.1 (BCG "auditability by design" verbatim: "the factory produces a complete, versioned audit trail… For regulated industries, the Dark Software Factory does not make compliance harder, it makes it structurally easier").
- **Three sub-phase methodology** — Council pattern: [`16-el-kaim-book-council-and-delegation`](../../../research/16-el-kaim-book-council-and-delegation.md). Cross-model judge: F46 ([`failure-modes-v3`](../failure-modes-v3.md) §5 F46, single-model review blindspot via [`34-lenny-howiai-personal-harnesses`](../../../research/34-lenny-howiai-personal-harnesses.md) §6.2 `kevin/carl`); CTR-D7 ([`contradictions.md`](../contradictions.md): Anthropic same-model-judge legitimacy *vs.* cross-model-critic position — this track runs both because at cold-start the cost-side argument for same-model loses to the F1-mitigation argument for cross-model). Production-scissors-off: F44 ([`failure-modes-v3`](../failure-modes-v3.md) §5 F44).
- **Graduation protocol** — Jaymin Augmentation-vs-Automation thresholds [`09-jaymin-book-harnesses-practices-mental-models`](../../../research/09-jaymin-book-harnesses-practices-mental-models.md) §5.5; F1 / F27 / F46 / F48 cascade ([`failure-modes-v3`](../failure-modes-v3.md) §8.2 cascade note); D2 work-unit-class mandate-fit ([`decisions-captured.md`](../decisions-captured.md) D2).

Most-cited contradictions and F-modes: **F1** (cited in F-mode rationale across §0, §1, §2, §3, §5); **CTR-B6** (the El Kaim-invariants vs. UC4-spec-malleable contradiction is this track's substantive UC4-hypothesis test); **F25** (Design starvation as cold-start regime named explicitly); **CTR-A4** (vocabulary discipline; lights-out ≠ L5).

---

## §4. §4 defaults: accepted vs challenged

Per [`decisions-captured.md`](../decisions-captured.md) D3, all 7 defaults marked.

- **D-1 — Specs are durable, version-controlled, human-curated.** `accepted with justification`. The Intent Crucible *is* the durable human-curated artifact; this track strengthens D-1 by structurally separating the human-curated upstream (Intent + invariants, non-malleable) from the downstream-malleable derived artifacts (EARS criteria, decision-seed resolutions). Sean Grove via [`09-jaymin-book-harnesses-practices-mental-models`](../../../research/09-jaymin-book-harnesses-practices-mental-models.md) §3.

- **D-2 — Scenarios live outside the codebase as a holdout set.** `accepted with justification` *with strengthening*. Greenfield mandate makes D-2 unambiguous (there is no codebase to inherit scenarios from on day 0). Cold-Start Bench is D-2 instantiated. *However:* at cold-start D-2 is **vacuous in practice** until the bench has been seeded — the graduation protocol's "bench saturation" criterion is what makes D-2 non-vacuous. CTR-B5 / CTR-G2 (brownfield D-2 inversion) is not in scope for greenfield.

- **D-3 — Agent = Model + Harness.** `accepted with justification` with explicit note. The track's Council and cross-model judge layer use the M+H decomposition. CTR-C1 (graph-node / population architectures don't decompose) does not bite because the track is neither graph-node nor population; it is a small council with explicit cross-model diversity. CTR-C10 (Portuguese-vs-English language effect, [`37-academic-llm-agent-collusion`](../../../research/37-academic-llm-agent-collusion.md) §5) is *flagged as a Phase-3 concern* — the natural-language register of the cold-start operator's prompts is a behaviour-influencing harness parameter D-3 does not model; this track does not resolve it but names it.

- **D-4 — Holdout discipline substrate-enforced.** `accepted with justification`. The track's substrate-level discipline is that bench-construction agents and builder agents *never share context*; this is enforced at the substrate layer, not as methodology discipline (per F53 voluntary-discipline-fragility). At cold-start D-4 is meaningful from cycle 1 because the bench exists before the first build cycle. F28 mitigation native.

- **D-5 — Hard cost ceilings non-optional in CI.** `accepted with justification`. Cold-start cycles are tiny by §1.2 sub-phase C; cost ceilings are *easy* at cold-start because per-cycle scope is bounded. The CaMeL-class ~7-point utility tax (CTR-E6, [`followup/08-security-primitives`](../../../research/followup/08-security-primitives.md) §3) is acceptable at cold-start scope. Cost ceiling at steady-state graduates with the work-unit-class declaration.

- **D-6 — Tiered watchdog (Daemon / Triage / Patrol) is a substrate primitive.** `accepted with justification`. Cold-start has *zero historical baseline* for Patrol-tier strategic drift detection — Patrol is structurally muted during cold-start because there is nothing for it to compare against. Daemon and Triage operate from cycle 1. The graduation protocol *requires* Patrol-tier baselines to exist before steady-state regime declaration; this is the cold-start formulation of D-6.

- **D-7 — Trajectory capture is cheap and production-tested.** `accepted with justification`, with cold-start framing. D-7 is accepted as a steady-state primitive; at cold-start there are no prior trajectories to replay, but trajectory capture from cycle 1 is *essential* to populate the steady-state primitive. OpenHands V1's sub-ms persist / 7.4ms crash recovery ([`11-openhands-substrate-audit`](../../../research/11-openhands-substrate-audit.md) §6) is cited as measurement evidence, not as normative substrate (per brief §0 glossary discipline).

**Summary:** 7 accepted, 0 challenged. The track's challenges to brief assumptions land on **§3 working hypothesis (UC4)** — specifically the upstream-vs-downstream spec-malleability distinction per CTR-B6 — and on **§4.1 D-2's day-0 vacuousness**, not on the defaults themselves.

---

## §5. Cold-start (mandatory)

This entire track is a cold-start treatment; this section answers the four §5.2 questions directly.

### How does a greenfield factory bootstrap on day 0?

Day 0 is the **Intent Crucible authoring session.** A human authors 1–3 Intent blocks per [`14-el-kaim-book-intent-and-spec-authorship`](../../../research/14-el-kaim-book-intent-and-spec-authorship.md) §3, with the substrate's typed-object validator and the GtWR/EARS deterministic linter providing immediate feedback. No agent has written code. The Council ([`16-el-kaim-book-council-and-delegation`](../../../research/16-el-kaim-book-council-and-delegation.md)) — staffed with at least two model families (F46 mitigation) — interrogates each block per INCOSE GtWR C1–C15 questions. The substrate provides a Cognitive-Escrow-aware operator surface ([`30-cognitive-escrow`](../../../research/30-cognitive-escrow.md) §3): the prompt→response interval surfaces structured STIR prompts, not as voluntary discipline (which F53 falsifies) but as substrate-triggered structural pauses. Day 0's output is *not code*; it is a validated Intent Crucible and an RSI declaration ([`31-caremark-rsi-board-exposure`](../../../research/31-caremark-rsi-board-exposure.md) §1 three-part test) committed to the version-controlled ledger.

Day 1–N is the **bench seeding period.** Human seeds 5–10 Kaner-style scenarios; agents propose more; human curates. Each scenario binds to ≥1 EARS criterion and ≥1 Intent invariant. The bench is signed and stored outside the (not-yet-existing) codebase. *No build cycle runs* until bench-sufficiency criteria are met.

The first build cycle (sub-phase C, §1.2) is deliberately tiny: one Ubiquitous EARS criterion, one scenario, production-scissors off, cross-model judge with mandatory escalation on disagreement.

### What priors are available?

Per brief §0 glossary's revised greenfield definition (per Skeptic #6): *priors from adjacent domains, exemplar projects, library docs, operator knowledge are permitted and expected*. The cold-start factory consumes:

- **Adjacent-domain RE/SE knowledge** — INCOSE GtWR, EARS patterns ([`25-requirements-engineering-foundations`](../../../research/25-requirements-engineering-foundations.md)). These are *deterministic priors* — the linter encodes them; the Council uses them in questioning. They do not depend on the Intent being similar to any prior intent.
- **Exemplar Intent blocks** — El Kaim Chapter 8 examples ([`14-el-kaim-book-intent-and-spec-authorship`](../../../research/14-el-kaim-book-intent-and-spec-authorship.md)) and any operator-curated prior Intent blocks from other factory runs (per glossary §0 revision).
- **Scenario-testing tradition** — Kaner's six characteristics ([`followup/09-methodology-ancestors`](../../../research/followup/09-methodology-ancestors.md)) as authoring discipline.
- **Operator's domain knowledge** — the human authoring the Intent Crucible. This is the *load-bearing* prior at cold-start; the substrate's job is to externalize and discipline that knowledge before any LLM has touched it.
- **Library and framework docs** — read as input to decision-seed resolutions, not assumed correct without bench check.
- **Empirical priors about LLM behaviour** — F36/F37 thresholds (≤10 simultaneous requirements per cycle from Yang et al.; contradictory-prompt risk from Larbi et al., [`26-prompt-underspecification-academic`](../../../research/26-prompt-underspecification-academic.md)). These shape the methodology (bench-chunking, contradiction-detection at authoring) rather than acting as Intent priors.

What is *not* available as prior: scenarios from this codebase; tests from this codebase; runtime telemetry from this codebase; prior `docs/solutions/` from this factory run; trajectory replays from prior cycles. The architecture is honest about this absence.

### How is the bootstrap protected against silent failure?

This is the hardest question and the one that justifies cold-start-first as the organizing axis. Five protections, each addressing a specific F-mode at its cold-start-worst severity:

1. **Deterministic perimeter at the authoring layer** (against F38, F18, F51-greenfield-`high`). GtWR/EARS linter is *not* an LLM-as-judge; it is a deterministic rule engine. Per CTR-D6 ([`contradictions.md`](../contradictions.md): sycophancy-as-defensive-wrap induces false positives), this avoids the LLM-judge-sycophancy trap at the authoring boundary.
2. **Cross-model judge mandatory at first cycles** (against F1-greenfield-`critical`, F27-greenfield-`critical`, F46-greenfield-`high`). At cold-start there is no prior K=5 history; the substrate enforces cross-model diversity rather than trusting a single-model judge's calibration. This adopts the F46-mitigation position over Anthropic's single-judge-is-fine position (CTR-D7, CTR-D8) for the cold-start period specifically, on the grounds that the Anthropic claim ("the judge is doing a different task than the main pipeline," [`followup/07-evals-deepdive`](../../../research/followup/07-evals-deepdive.md) §3.6) presumes a track record the cold-start factory does not have.
3. **Substrate-enforced holdout** (against F28-greenfield-`critical`). Bench-construction agents and builder agents are isolated at the substrate layer; D-4 is non-negotiable from cycle 1.
4. **Production-scissors-off default** (against F12-greenfield-`high`, F33-greenfield-`high`, F44-greenfield-`high`, F56 Replit-class-greenfield-`medium`). The first cycles ship to sandbox; production access is a graduated permission tied to bench-saturation and cross-model agreement-rate metrics.
5. **RSI declaration up-front** (against F43, F54-greenfield-`high`, F55-greenfield-`critical`, F58). If the factory will be RSI at steady-state, the Caremark prong-1 reporting structure is in place from cycle 1 — auditability is BCG's "by-design" property ([`followup/10-governance`](../../../research/followup/10-governance.md) §1.1) rather than a retrofit.

The protections compose: silent failure requires defeating all five simultaneously. The cold-start failure cases the corpus has documented (Replit DB wipe; Moltbook 1.5M API keys via missing RLS, both [`followup/10-governance`](../../../research/followup/10-governance.md) §0.1 / §3) are each closed by ≥2 of these protections.

### What is the trajectory from day 0 → day N?

Phased per §1.2 sub-phases and §1.3 graduation protocol:

- **Day 0:** Intent Crucible authored; RSI declaration made; Council questions Intent; no code.
- **Day 1–N (bench seeding):** Bench grows to sufficiency threshold; first tiny build cycle (sub-phase C) executes against a single criterion in sandbox; cross-model judge agreement-rate begins accumulating.
- **Cold-Start Regime steady-state:** Cycles run at L3-Augmentation; human in every cycle; bench grows with each cycle's discovered acceptance criteria; trajectory capture (D-7) accumulates; K=5 baselines develop on the most-repeated work-unit-class.
- **Graduation event:** Per §1.3 metrics, one (or more) work-unit-class graduates to L4-lights-out. The transition is *per-class, not per-factory*; other classes remain at Augmentation until they independently graduate. Board is notified (per F43).
- **Steady-State Regime:** D-2/D-4/D-6/D-7 are now non-vacuous; Patrol-tier watchdog has baselines; the factory operates per [`decisions-captured.md`](../decisions-captured.md) D2 work-unit-class mandate-fit matrix. Cold-start primitives (Intent Crucible, EARS linter, Council, signed bench, Cognitive-Escrow surface, RSI Ledger) remain active *because new work units continue to enter the factory* and each new work-unit-class re-enters its own cold-start sub-phase before graduation.

The trajectory is *not* "cold-start then forget cold-start" — the architecture treats new-work-unit-class arrival as a *micro-cold-start*. This is the cold-start-first track's structural commitment.

---

## §6. What this track is NOT trying to be

- **Not comprehensive across all 9-track concerns.** Steady-state operation, brownfield-fit, the Compound Knowledge / `discovered-from`-edge knowledge-store discipline ([`38-gas-systems-substrate`](../../../research/38-gas-systems-substrate.md), [`followup/11-compound-knowledge`](../../../research/followup/11-compound-knowledge.md)), the Atelier-vs-Refinery-vs-Tournament shape debate (CTR-D3, OQ-B4), the substrate-selection question (CTR-C5: OpenHands+Overstory vs. Gas City) — all of these are downstream of graduation and are deliberately under-treated here. The substrate-first and methodology-first greenfield tracks (per [`decisions-captured.md`](../decisions-captured.md) D1) are expected to develop them.

- **Not a substrate enumeration.** Per [`decisions-captured.md`](../decisions-captured.md) D4 / Skeptic #14, this track names *day-0-load-bearing* primitives without claiming they are the complete substrate. The Phase-4 substrate/methodology boundary is downstream.

- **Not a stance on the spec format debate (CTR-B1).** EARS is *mandated for acceptance criteria*; the Intent Crucible is *typed-object*. The track does not claim DOT (CTR-B1 Attractor framing) or Kiro EARS-only or prose are wrong — it claims EARS+typed-object is *the right cold-start choice*.

- **Not a position on the factory-vs-company metaphor (CTR-F1: Brier vs. corpus).** Brier's pace-layer model ([`followup/12-brier-pace-layers`](../../../research/followup/12-brier-pace-layers.md)) is acknowledged as the corpus' strongest counter-metaphor; this track operates within the factory framing per UC1 but observes that Brier's "ARCHITECTURE.md per repo" maps cleanly onto the Intent Crucible's invariants block. The metaphor question is a Phase-3 cross-track concern.

- **Not a brownfield architecture, even by analogy.** Brownfield's "legacy-ingestion" (CTR-G3) is a *symmetric* problem but with very different priors available; the brownfield tracks should treat it on its own terms.

- **Not a resolution of the F1/F27/F46/F48 cascade ([`failure-modes-v3`](../failure-modes-v3.md) §8.2).** The track *uses* cross-model diversity as the cold-start mitigation; it does not claim the cascade is closed at steady-state.

---

## §7. Open questions surfaced by this track

1. **What are the concrete bench-saturation N and M?** §1.3 commits to *having* the criteria; the numbers are deferred to Phase-6 ADR. Phase-3 may want a corpus-grounded estimate; the Yang et al. ≤10-simultaneous-requirements ceiling ([`26-prompt-underspecification-academic`](../../../research/26-prompt-underspecification-academic.md) §3.4) is the only hard anchor.

2. **Does the cold-start vs. steady-state phase distinction belong as an organizing axis in the v3 set?** OQ-B7 (Skeptic #1) named regime / stakes / synchronicity / work-unit-class / codebase-lifecycle as candidates; this track surfaces *phase* (cold-start vs. steady-state) as a sixth candidate. If multiple greenfield tracks converge on this, the v3 set may need phase-classified architecture specs rather than single-spec architectures.

3. **Is "micro-cold-start per new work-unit-class" architectural or methodological?** §5's final point is that cold-start primitives reactivate for each new work-unit-class entry. Whether this is a substrate primitive (a *re-entry protocol*) or a methodology pattern (a *human-and-Council reconvening ritual*) is unresolved and is a Phase-4 concern.

4. **How does the cross-model judge cost scale at cold-start?** Cross-model judging at every cold-start cycle costs ~2× per-cycle inference. CTR-E6 (CaMeL utility tax) is the corpus' closest empirical anchor (~7-point utility tax); cross-model judging's tax has not been measured in the corpus. CTR-E1 (Cherny $100K/mo) and the noosphr $500–$5000/day spread say nothing about cold-start specifically.

5. **Does the Intent Crucible's typed-object discipline create CTR-C10 / F50-class confusion** (architecture/specification confusion in typed objects, [`failure-modes-v3`](../failure-modes-v3.md) §4a F50)? The 9-field block is *spec*, not *architecture*, but at cold-start the architecture is partly being discovered through the Intent. If the Crucible drifts toward absorbing architectural decisions, F50 fires. The graduation protocol should test for this.

6. **Single biggest open question.** **What if the Intent Crucible itself cannot be authored at day 0?** The track assumes the operator can express intent in a form rich enough for the Council to interrogate and the bench to be seeded against. The Norheim et al. survey ([`26-prompt-underspecification-academic`](../../../research/26-prompt-underspecification-academic.md) §1) and the BCG "intent thinking is the critical new competency" claim ([`followup/10-governance`](../../../research/followup/10-governance.md) §1.2) both treat intent-articulation as a *learned* skill that most operators currently lack. If the operator cannot author a well-formed Intent Crucible block, the entire cold-start protocol stalls before it begins. The track has no mitigation for *operator-intent-illiteracy* beyond Council questioning, which is itself bounded by the quality of the seed Intent. This is the track's biggest unresolved exposure and the most-likely Phase-3 adversarial attack surface.

---

*End of greenfield-cold-start-first.md.*
