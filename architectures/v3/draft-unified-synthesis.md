---
artifact: draft-unified-synthesis
phase: 3.1
inputs:
  - tracks/unified-A.md
  - tracks/unified-B.md
  - tracks/unified-C.md
bias-guard-inputs:
  - bias-guards/phase-2/anchor-detector.md
  - bias-guards/phase-2/axis-divergence-audit.md
  - bias-guards/phase-2/lumper.md
  - bias-guards/phase-2/splitter.md
based-on-commit: b65ec23a502c12706ab387b8e9fe4076c7b2f969
based-on-date: 2026-05-25
---

# Draft Unified Synthesis (Phase 3.1, pre-adversarial)

**Status.** Lead-agent merge of the three Phase-2 unified tracks (no-axis-prescribed per [decisions-captured.md D1](decisions-captured.md)). The three tracks were free to pick distinct axes; they picked:

- **U-A.** *Escrow-Interval-as-Substrate*. Every cycle is a directed graph of `EscrowInterval` typed objects.
- **U-B.** *Pace-Layer × Cognitive-Escrow*. Five Brier layers; greenfield = top-down traversal, brownfield = bottom-up inference.
- **U-C.** *Distance-from-Frozen-Anchor*. Every work unit is parameterised by graph distance to its mandate-specific anchor.

**Critical caveat.** Per axis-divergence audit §3.3:

> *"The three unified tracks **independently converged on (typed object + policy + parameterized mandate)** as the shared substrate shape. Effective overlap on substrate primitive content: ~55%. Effective overlap on the unified claim ('mandate is a parameter'): ~95%."*

This is the most significant convergence in Phase-2 outputs. It is either *strong corpus signal* (the F42 / F53 / F46 / F44 + D-4 / D-6 / D-7 + CTR-B5 / CTR-C2 cluster narrows the design space sharply) *or* *brief-derived* (the three tracks all inherited the same Kahana / cognitive-escrow + AILCCP framing through brief §5.1's required-reading list — anchor-detector F-ANCHOR-2 and F-ANCHOR-3). The two D7 blind-axis tests dispatched at Phase-3.2 resolve which it is.

If the convergence is genuine corpus signal: Phase-3 should treat U-A / U-B / U-C as **three candidate instantiations of one unified family** rather than three competing unified architectures (axis-divergence-audit §5 implication).

If the convergence is partially anchored: D1's falsifiability test for UC4 is weakened — the unified-mandate-attacker pass in Phase-3.3 operates on three drafts that are less independent than they look.

---

## §1 ROBUST claims (all three tracks support)

### §1.1 Unified architecture shape (load-bearing claim)

- **ROBUST-U1.** **Mandate is a parameter, not a top-level architecture distinction.** All three tracks make this the core unification move; this is the 95% convergence cited above.
  - **U-A.** Mandate differs by `EscrowInterval.priors` (greenfield: `priors.in-tree: []`, `priors.out-of-tree: [scenarios, exemplars]`; brownfield: `priors.in-tree: [tests, traces, codebase]`).
  - **U-B.** Mandate differs by *traversal direction* of the same pace-layer stack (greenfield: top-down from L0 standards; brownfield: bottom-up inference from L4 code).
  - **U-C.** Mandate differs by anchor's `kind`-content (greenfield: intent-block invariants; brownfield: existing codebase's slow-layer invariants + tests + telemetry).
  - *Bias-guard caveat (anchor-detector F-ANCHOR-3).* This convergence trips the D7 blind-axis threshold: "two or more parallel subagents converge on the same axis / framing / pattern-name." Mandatory D7 test at Phase-3.2 (D7-U-1 in §4).

- **ROBUST-U2.** **The substrate carries a typed-object primitive that hosts policy fields.** All three tracks instantiate this, varying the typed-object:
  - **U-A.** `EscrowInterval` with fields `kind / pace-layer / priors / policies / classifier / artefacts`.
  - **U-B.** Layer-typed object (L0..L4) with fields `change-rate / priors / escrow-policy / provider-property-requirements / threshold-bar`.
  - **U-C.** `Anchor` object with fields `kind / content / frozen-since / owning-mandate / mutation-protocol`.
  - **Splitter Cluster-3 unify recommendation** confirms this is one primitive across all 9 Phase-2 tracks (`FrozenAnchor` / `InvariantBlock`); the unified tracks' instantiations are different *names for the same primitive*, parameterised by mandate-as-content.

- **ROBUST-U3.** **Greenfield and brownfield mandate-specific concerns map to per-node policy fields, not to architecture-shape differences.** Spec-malleability (greenfield UC4) is `EscrowInterval{kind: spec-author, pace-layer: specs}` with revisable graph back-edges (U-A); or *L2 spec layer* with greenfield-top-down velocity (U-B); or *near-anchor at intent-block-invariants* (U-C). Code-archaeology (brownfield UC4) is the inverse traversal direction (U-B) or `priors.in-tree: [codebase]` (U-A) or anchor's `kind=runtime-trace | live-test | architecture-rule` (U-C).

### §1.2 Substrate primitives (cross-track agreement)

- **ROBUST-U4.** **`RegimeClassifier`** (splitter Cluster-1). All three tracks have a substrate primitive that, per cycle-unit, declares automation-eligibility on the basis of typed feature inputs:
  - **U-A.** `classifier` slot on each EscrowInterval; decides `automation-eligibility` from `pace-layer + priors + kind` at open time.
  - **U-B.** Per-layer regime declaration (L4 = lights-out at code; L0–L3 transitions = L3-Augmentation).
  - **U-C.** `distance-gated dispatcher` routes to near-anchor / mid-distance / far-anchor regimes based on the typed distance tuple.
  - *Anchor-detector flag (F-ANCHOR-4, MEDIUM).* Promoting the D2 mandate-fit matrix from documentation to substrate-runtime classifier is itself a brief-derived elevation. Surfaced as DPU-3.

- **ROBUST-U5.** **`TypedJudgeCall`** with sub-shape policy (splitter Cluster-2). All three tracks type the judge call; cross-family at high-stakes; same-model-different-role permissible at lower-stakes. Lumper Cluster-1 split requires preserving the three sub-shapes (same-model-different-role / different-family-on-builder / different-family-on-spec).

- **ROBUST-U6.** **`FrozenAnchor`** / **`InvariantBlock`** (splitter Cluster-3) substrate-primitive — see ROBUST-U2.

- **ROBUST-U7.** **`DeterministicSpecLinter`** (splitter Cluster-4). Substrate-resident, deterministic, GtWR R7/R8/R9/R26/R35 + EARS-pattern conformance; fail-closed. NOT LLM-judge (F51 mitigation).

- **ROBUST-U8.** **`PerimeterClosure`** (splitter Cluster-5). Deny-all sandbox default; CaMeL boundary for production-adjacent activity; substrate-default-off (F44).

- **ROBUST-U9.** **`AttributedEventLog`** (splitter Cluster-6). Append-only / immutable / signed per-event log with content-addressed envelopes. U-A wraps in `EscrowInterval` envelope; U-B tags with layer; U-C enriches with distance tuple. Splitter recommends extensible-metadata schema.

- **ROBUST-U10.** **`EscrowSurface`** (splitter Cluster-7). Substrate-triggered cognitive-escrow surface (reflection-question / success-criterion / similar-past / delegation-confirm / STIR-cascade) at structural moments — not operator-voluntary.
  - *Anchor-detector flag (F-ANCHOR-2, HIGH).* Promoting Kahana's interval (report [`30`](../../research/30-cognitive-escrow.md)) to substrate primitive is single-source. The phenomenon is corpus-multi-anchored but the substrate-primitive *promotion* is single-source. Surfaced as DPU-5.
  - *Anchor-detector flag (F-ANCHOR-3, MEDIUM-HIGH).* U-A and U-B both have "interval" / "escrow" in their axis names. D7 blind-axis test required (D7-U-1 in §4).

- **ROBUST-U11.** **`HoldoutPartition`** (splitter Cluster-8) substrate-enforced. D-4 unified; location parameter (`out-of-tree` / `in-codebase-partition` / `mixed`) handles per-mandate variants.

### §1.3 Per-cycle / per-unit shape (substantially shared)

Each track's "cycle" is a graph or sequence of typed objects with declared policies:

- **U-A.** Cycle = directed graph of EscrowInterval nodes. Graph back-edges permitted for revisable greenfield work.
- **U-B.** Cycle = layer traversal (top-down for greenfield, bottom-up for brownfield). Each layer transition is an escrow interval.
- **U-C.** Cycle = work-unit at declared anchor-distance, dispatched to one of three regimes. Anchor-edit work is always L4.

The *shapes* differ; the *contained primitives* (above) are shared. This is what justifies treating them as instantiations of one family (axis-divergence-audit §3.3 implication).

### §1.4 Cold-start / bootstrap (mandatory per brief §5; all three address)

- **ROBUST-U12.** **Day-0 is structural L3-Augmentation**, no exceptions. None of the three tracks permits `automation-eligible` classification at bootstrap.
  - **U-A.** `EscrowInterval{kind: bootstrap}` has `classifier.automation-eligibility: escalate`, cannot be set to `lights-out` for the bootstrap interval itself, *full stop*.
  - **U-B.** Bootstrap policies are *strictest defaults* — different-family judge mandatory; 100% approval-gate; STIR cascade; production-scissors off.
  - **U-C.** First cycles are far-anchor *L4 by construction* (no near-anchor anchors exist beyond the intent block); the architecture refuses lights-out at day 0.

- **ROBUST-U13.** **Bootstrap-Output is typed.** All three tracks produce a typed bootstrap output set:
  - El Kaim 9-field intent block (report [`14`](../../research/14-el-kaim-book-intent-and-spec-authorship.md)).
  - `EvaluationSuite` (per El Kaim §4.1 `protects: RULE-ID` linkage).
  - Initial scenario set (Kaner-style or EARS-criteria-bound per glossary §0 sub-shapes).
  - RSI declaration (Kahana three-part test, [`report 31 §1`](../../research/31-caremark-rsi-board-exposure.md)) + AILCCP three-controls instantiation.
  - Scaffold (`AGENTS.md` / `CLAUDE.md` / skills / policy templates).

- **ROBUST-U14.** **Graduation criteria are measurable.** All three tracks tie steady-state regime promotion to *measured* criteria (not calendar / not operator-declared):
  - **U-A.** Three conditions: non-empty methodology DAG with measured threshold-bars per work-unit-class; classifier audit at re-entry interval; board-visibility apparatus producing first quarterly report.
  - **U-B.** Day-0 → day-7 (L3 only) → day-7→day-30 (knowledge accumulates) → day-30+ (Jaymin thresholds calibrated).
  - **U-C.** Steady-state transition is a *distance-distribution shift* — when ≥X% of work units sit at d ≤ τ_low for K consecutive cycles.
  - *Lumper Cluster-9 partial-unify recommendation* applies: the graduation primitive (regime transition gated on measured criteria) is one primitive; the specific criteria are per-architecture parameters.

### §1.5 Defaults marking (§4 of brief)

| Default | Unified stance | Justification |
|---|---|---|
| D-1 | **mostly accepted, all 3** | Specs are durable artifacts in this architecture, but they are *one of many* typed-object content-handles (U-A) / one of five layers (U-B) / one of the anchor kinds (U-C). The default holds *if read per-typed-object*, not globally. |
| D-2 | **challenged, all 3** | Substrate accommodates both mandates: greenfield-bootstrap has `priors.out-of-tree`; brownfield has `priors.in-tree` per ROBUST-U1. Substrate enforces *holdout-vs-builder separation* (D-4) regardless of which side of the tree scenarios live on. |
| D-3 | **challenged, all 3** | The typed-object substrate doesn't require Model+Harness decomposition. Graph-node and population agents are encoded as typed-object content, not Model+Harness. CTR-C10 (Portuguese-vs-English register, report [`37`](../../research/37-academic-llm-agent-collusion.md)) suggests extension: U-A's `policies` slot, U-B's natural-language-register field at L2 spec, U-C's anchor-context as third-term. **Surfaced as DPU-2.** |
| D-4 | **accepted with justification, all 3** | The substrate's policy mediator refuses to close a judge interval if acceptance-criteria handles leaked into the upstream builder interval's inputs (U-A); per-layer holdout enforcement (U-B); distance-gated dispatcher is the holdout boundary (U-C). |
| D-5 | **accepted with justification, all 3** | Cost-ceiling breach is a substrate-fired re-entry trigger; ceiling enforcement at interval / layer / anchor-mutation-queue boundary. |
| D-6 | **accepted with justification, all 3** | Three watchdog tiers map onto interval-policy enforcement (Daemon liveness, Triage classification, Patrol drift) — same as in greenfield + brownfield. |
| D-7 | **accepted with justification, all 3** | Trajectory is the inside-the-interval (or per-layer / per-cycle) event stream; primitive envelope varies but the substrate cost is the same. |

---

## §2 DECISIONS-PENDING (tracks diverge; user input required at Phase-3.4)

### DPU-1. What is the typed object? Interval / layer / anchor?

- **Divergence (the load-bearing one).**
  - **U-A.** **EscrowInterval** — a typed process-state node. Every transition where intent leaves human possession and the consequences are not yet observable. Carries `kind`, `pace-layer`, `priors`, `policies`, `classifier`, `artefacts`.
  - **U-B.** **Layer** — a typed artifact-stack node (L0..L4). Carries `change-rate`, `priors`, `escrow-policy`. Greenfield top-down, brownfield bottom-up traversal.
  - **U-C.** **Anchor** — a typed *immutable upstream object* (intent-invariant / architecture-rule / standards-rule / live-test / runtime-trace). Carries `frozen-since`, `mutation-protocol`. Work units are parameterised by graph-distance to the anchor.
- **Splitter Cluster-3 partial unify.** The three are alike enough to share a primitive name (`FrozenAnchor` / `InvariantBlock`), but their *granularity and topology* differ. U-A's interval is a process-state node (many per cycle); U-B's layer is an artifact-stack position (5 of them); U-C's anchor is one or a few per architecture.
- **Axis-divergence-audit finding (§5).** "Phase 3 should treat these as three candidate instantiations of one unified family rather than three competing unified architectures, and dispatch adversarial passes that attack the family-level claim before adjudicating between instantiations." The family-level adversarial passes resolve whether the family unifies at all; *if it does*, then DPU-1 is the choice within the family.
- **User question.** Pick one typed-object as the substrate-primitive granularity: interval (process-state-shaped) / layer (artifact-stack-shaped) / anchor (immutable-upstream-shaped). Or commit to multiple at different scales (e.g., interval as runtime primitive, layer as artifact-stack derived from intervals, anchor as a special interval kind that cannot be re-graphed).
- **Concrete next action.** User-resolved at Phase-3.4. Phase-5 wave-1 ADRs cannot proceed without this choice.

### DPU-2. D-3 decomposition: which third term, if any?

- **Divergence (sharper than greenfield / brownfield).**
  - **U-A.** D-3 challenged — natural-language-register fits in the `policies` slot of EscrowInterval (substrate carries the third term).
  - **U-B.** D-3 challenged — natural-language-register field at L2 spec layer; population and graph-node agents are encoded as interval-kind + policy.
  - **U-C.** D-3 challenged — *anchor-context* is the missing third term. Proposes `Agent = Model + Harness + Anchor-Context`.
- **User question.** Among the three proposed third terms (natural-language-register / interval-or-layer-kind / anchor-context), is one *the* generalisation, or are they three different axes that all need to be carried? Does the brief's D-3 default get retired in favor of an extended decomposition?
- **Concrete next action.** Phase-5 wave-1 ADR ("D-3 decomposition: agent layering for substrate-typed primitives"). Folds DPG-1 and DPB-2 from the mandate-specific drafts.

### DPU-3. Eligibility classifier (RegimeClassifier): substrate primitive or methodology / policy concern?

- **Folds DPG-3 and DPB-7.** All three unified tracks place the classifier at substrate; this is itself the F-ANCHOR-4 (MEDIUM) concern. The unified tracks' classifier inputs vary by axis (interval features in U-A; layer-crossings in U-B; distance tuple in U-C) — these are *feature sources*, not different classifiers.
- **User question.** Same as DPG-3/DPB-7. The unified-track answer is "yes, substrate primitive" — but if that resolves to "no, methodology" at the greenfield or brownfield level, the unified-tracks' substrate enumeration loses a primitive and the methodology-vs-substrate boundary moves.
- **Concrete next action.** Same Phase-5 wave-1 ADR as DPG-3/DPB-7.

### DPU-4. Per-cycle / per-layer / per-interval / per-distance granularity for regime classification

- **Divergence on what RegimeClassifier is computed *over*.**
  - **U-A.** Per-interval (many per cycle). Each EscrowInterval gets its own classification at open time.
  - **U-B.** Per-layer (5 per cycle). L4 work units are lights-out; L0-L3 transitions are L3-Aug. Less granular than U-A.
  - **U-C.** Per-work-unit at declared anchor-distance (one per work unit, ~1-N per cycle depending on cycle shape).
- **Lumper Cluster-3 (lights-out-surface) confirms** five candidate surfaces under brief §2.1 option (c)+(b) (work-unit-class / per-stage / per-interval / per-distance / per-cold-start-phase / per-layer). The unified tracks span three of these.
- **User question.** Granularity choice: per-interval (highest substrate cost; highest auditability) / per-layer (medium; conceptually clean) / per-distance (lowest; depends on distance-metric quality)?
- **Concrete next action.** Phase-5 wave-1 ADR. Trade-offs: substrate cost (immutable-logging at finer granularity, anchor-detector F-ANCHOR-4 concern); regime audit-trail clarity for F43 board-visibility; classifier gaming surface (U-C §7 OQ-1 F47 Goodhart).

### DPU-5. Cognitive-escrow as substrate primitive — same as DPG-7 / unified-track level

- **Folds DPG-7.** The unified tracks all promote `EscrowSurface` to substrate. F-ANCHOR-2 (Kahana single-source) and F-ANCHOR-3 (interval/escrow as axis convergence) both apply. The mandatory D7 blind-axis test (D7-U-1, see §4) is *the* resolution mechanism. If the test produces a defensible alternative axis, DPU-5 resolves toward methodology; if the test concedes, the substrate-primitive promotion is genuine corpus signal.

### DPU-6. Per-layer vs. per-call vs. per-interval provider-property requirements (OQ-B8)

- **Divergence.**
  - **U-A.** Provider-property requirements declared per `EscrowInterval.policies.judge-diversity`; cross-family at high-stakes, RouterLLM-style at intra-family.
  - **U-B.** **Per-layer routing**, not per-call. L0/L1 = long-context + diverse; L2 = contradiction-detection capability; L4 = provider-aligned coding agents. Neither pure RouterLLM nor pure Attractor.
  - **U-C.** Cross-family at mid/far-distance; single-judge permitted near-anchor.
- **CTR-C4** (RouterLLM unification vs. Attractor per-provider non-unification) plays out differently across the three.
- **User question.** Is provider-property routing (a) per-interval (U-A), (b) per-layer (U-B), or (c) per-distance-regime (U-C)? Or is the abstraction itself open?
- **Concrete next action.** Phase-5 wave-2 ADR ("Provider-routing abstraction granularity").

### DPU-7. Methodology evolution: per-architecture / substrate-tracked / interval-typed

- **Divergence.**
  - **U-A.** Methodology evolution is a graph-shape change, captured as `kind: methodology-delta` interval. Whether *that* interval runs lights-out is the question — substrate does not pre-decide.
  - **U-B.** Per-architecture concern (each layer's methodology evolves independently); substrate provides typed-object versioning.
  - **U-C.** Substrate-driven *methodology parameterisation* — methodology rules are model-parameterised (as the codebase / anchor set / distance distribution changes, methodology changes mechanically).
- **Folds DPB-10** (Compound Engineering as substrate or methodology).
- **User question.** Is methodology evolution (a) typed at the substrate (U-A); (b) per-architecture without substrate involvement beyond storage (U-B); or (c) substrate-parameterised (U-C)?
- **Concrete next action.** Phase-5 wave-2 ADR. Connects to F35 (federation-as-family drift) and F55 (behavioural drift in self-reference loops).

### DPU-8. Whether the unified architecture survives Phase-3.3 cross-mandate adversarial

- **Pre-decision question.** This is the falsification test for UC4 (D1's hypothesis). Phase-3.3 dispatches:
  - `X_UNM_G` — *unified-mandate-attacker for greenfield*. Argues: this architecture cannot work for greenfield because of \[concrete corpus-grounded reason — likely targets cold-start primitives or `priors.out-of-tree` semantics\].
  - `X_UNM_B` — *unified-mandate-attacker for brownfield*. Argues: this architecture cannot work for brownfield because of \[likely targets codebase-model fidelity or in-codebase holdout semantics\].
- **Possible outcomes.**
  - Both attacks fail to land: UC4 is *falsified for the unified architecture's domain* per ROBUST-U1.
  - One attack lands: the unified architecture is mandate-leaning, not genuinely unified; reframe as the leaning-mandate's mandate-specific architecture.
  - Both attacks land: UC4 holds; the unified architecture cannot reach either mandate without sacrificing its unification claim. Phase-4 substrate/divergence extraction proceeds without a survived unified synthesis.
- **No user input required at Phase-3.4 for this** — the adversarial pass results are themselves the decision input. But the user must be aware that the unified-track output may not survive Phase 3 in its current form, and the Phase-4 shared-substrate extraction depends on what survives.

---

## §3 Open questions surfaced by individual tracks (preserved for Phase-3 adversarial reference)

- **U-A OQ-1 (biggest).** Interval-granularity — at what cadence is an interval an EscrowInterval? Per send/receive pair? Per cycle? Per gate-boundary? Phase-5 ADR.
- **U-A OQ-2.** Classifier accountability — F57 (design-authority erosion via convenience-reclassifies-stakes) is *amplified* by giving so much weight to one substrate primitive. Audit discipline needed.
- **U-A OQ-3.** Re-entry registrar protocol completeness (OQ-B3 partial answer; protocol detail open).
- **U-A OQ-4.** Cross-interval correlation against F48 (tacit collusion via shared context).
- **U-A OQ-5.** Multi-codebase intervals (out of scope for v3 but flagged).
- **U-A OQ-6.** Cost model for full immutable logging at high parallelism; substrate-cheap thesis may not survive cross-family-judge × STIR × immutable-logging combination.
- **U-A OQ-7.** D7 owed on interval/escrow framing — same as F-ANCHOR-3 / DPU-5.
- **U-B OQ-1.** Layer-count is empirical, not derived. Brier asserts 5; El Kaim implies more; could be 3 or 7.
- **U-B OQ-2.** Escrow-interval threshold calibration (when does substrate transition STIR from mandatory to offered)?
- **U-B OQ-3.** Cross-layer drift detection (F34) at populations.
- **U-B OQ-4.** Layer-traversal direction at hybrid surfaces (greenfield module in brownfield codebase).
- **U-B OQ-5 (biggest).** F53 may have a stronger reading — the operator's *response* to substrate-fired escrow primitives is itself voluntary; substrate cannot ensure the operator reads the reflection question.
- **U-B OQ-6.** RouterLLM-equivalent at layer vs. call level (DPU-6).
- **U-B OQ-7.** Same-model-different-role at non-code layers (does the pattern extend to L2, L1)?
- **U-B OQ-8.** Pace-layer model's F52 risk — layering is itself a deterministic structure imposed around stochastic agents.
- **U-C OQ-1.** Distance estimator adversarial gaming — F47 Goodhart on tokens; agents may phrase work-units to land just below τ_low.
- **U-C OQ-2.** Does the contradiction-flag close F37, or merely narrow it? F33/F51 Ashby-deficient-probabilistic-guard suggests probabilistic detection has variety limits.
- **U-C OQ-3.** How are anchor invariants kept honest over multi-month cold-start? F8 stale-knowledge + F35 federation-drift interact.
- **U-C OQ-4.** Does anchor-distance correctly subsume Brier's pace-layers, or is it a strictly weaker re-encoding?
- **U-C OQ-5 (biggest).** Can the distance estimator be made operator-legible at the moment of dispatch? If not, the substrate is opaque in the way F42 names.

---

## §4 Phase-3.2 adversarial dispatch notes

The 6 persona-adversarial subagents per draft. Specific instructions per persona:

- **Red-team.** Target ROBUST-U1 (mandate-as-parameter — the 95% convergence). Argue: this is brief-derived unification (per F-ANCHOR-3) and not corpus-supported. Counter-example required from corpus.
- **Pre-mortem.** Target the typed-object choice (DPU-1). 18 months in, which of interval / layer / anchor fails first under operational load — and how does that failure cascade?
- **Regulator.** Target ROBUST-U13 / ROBUST-U14 (typed bootstrap output + measurable graduation). Is the Caremark prong-1 board-visibility surface (AILCCP three-controls + RSI declaration) defensible for SB 53 / SEC IAC at the *unified* level, or does the cross-mandate factory create regulator-novel surfaces that AILCCP does not cover?
- **CFO.** Target ROBUST-U5 (TypedJudgeCall), ROBUST-U9 (immutable AttributedEventLog), ROBUST-U10 (EscrowSurface). The substrate-cheap thesis may not survive *combined* cross-family-judge × full-immutable-logging × STIR-cascade across high-parallelism interval graphs (U-A OQ-6). What's the cost model?
- **10-year on-call.** Target the unified architecture's resumption story. A factory has been running 24 months across mixed greenfield + brownfield engagements. The classifier has drifted slightly (F57). The codebase model has been refreshed many times. The original operator has rotated out. What does the on-call engineer see, and which substrate primitive is most likely to silently rot?
- **Naive newcomer.** Target the entire draft for jargon, hidden anchors. Specifically: is the "mandate is a parameter" claim (ROBUST-U1) intuitive, or does it require pre-loading on UC4 and brief §3?

### Mandatory D7 blind-axis tests (anchor-detector recommendations)

- **D7-U-1 (mandatory).** Dispatch one supplementary unified-mandate subagent with the brief: *"pick an organizing axis for a unified greenfield + brownfield architecture. Axes mentioning 'interval', 'escrow', or 'cognitive escrow' are PROHIBITED. Substrate primitives derived from Kahana (report [`30`](../../research/30-cognitive-escrow.md), report [`31`](../../research/31-caremark-rsi-board-exposure.md)) — specifically EscrowSurface, EscrowInterval, escrow-as-substrate-primitive promotion — are PROHIBITED. The phenomenon (cognitive escrow) may be acknowledged at the methodology layer; the substrate-primitive promotion is what is prohibited. Produce a track-shaped output with §0 axis defense, §1 architecture sketch, and §4 defaults marked."*
  - If the supplementary subagent finds a defensible alternative unified axis: F-ANCHOR-2 + F-ANCHOR-3 are at least partially confirmed; the unified-track convergence on interval/escrow is brief-derived rather than pure corpus signal. DPU-5 resolves toward methodology-layer.
  - If the supplementary subagent concedes the interval/escrow framing is the corpus' strongest answer: the convergence is genuine; DPU-5 confirms substrate-primitive promotion.

- **D7-U-2 (mandatory).** Dispatch one supplementary subagent with the brief: *"address brief §2.1 OQ-B1 without using option (c) or option (b). Defend an (a), (d), or (e) resolution from the corpus."* This is the same blind-axis test recommended in the greenfield draft (D7-G-1); for the unified architecture, the same test applies.

### Cross-mandate adversarial (Phase-3.3, 4 subagents)

The unified-mandate-attacker pair (`X_UNM_G`, `X_UNM_B`) is the falsification test for UC4 per DPU-8. Brief for each:

- **`X_UNM_G`.** *"Argue that the unified architecture (typed-object substrate carrying mandate-as-parameter; unified-A/B/C as candidate instantiations) CANNOT work for greenfield. Use the cold-start required-reading (reports [`25`](../../research/25-requirements-engineering-foundations.md), [`26`](../../research/26-prompt-underspecification-academic.md), [`30`](../../research/30-cognitive-escrow.md), [`31`](../../research/31-caremark-rsi-board-exposure.md), [`followup/10`](../../research/followup/10-governance.md)) as your evidence base. Specific attack surfaces: (a) the typed-object primitive's bootstrap shape — can it actually be authored at day 0 in a way that the per-cycle agent reads correctly? (b) the substrate-primitive promotion of EscrowSurface — does the operator-attention-fragility problem (Kahana F42/F53) generalize to unified factories operating across multiple codebases simultaneously? (c) the graduation protocol — can a unified factory measure greenfield graduation when its own substrate is also handling brownfield work?"*
- **`X_UNM_B`.** *"Argue that the unified architecture CANNOT work for brownfield. Use the brownfield-critical F-mode set (F12 / F20 / F21 / F33 / F34 / F44 / F56 — all brownfield-critical per [`failure-modes-v3.md`](failure-modes-v3.md)) as your evidence base. Specific attack surfaces: (a) the codebase-model maintenance cadence — can a typed-object substrate that also handles greenfield's volatile intent blocks maintain a stable codebase model? (b) per-distance vs. per-region regime classification — does this work for brownfield's varied evidence density? (c) the AttributedEventLog at brownfield scale (Stripe 1,300 PRs/week per [`report 35`](../../research/35-lenny-howiai-spec-driven-and-team-ops.md))?"*

The cross-mandate pair (`X_GFB_A`, `X_GFB_X`) attack and defend whether the separate greenfield + brownfield drafts can collapse into the unified architecture:

- **`X_GFB_A`** (advocate). *"Argue that the separate greenfield and brownfield drafts (from `draft-greenfield-synthesis.md` and `draft-brownfield-synthesis.md`) could collapse into the unified architecture. Show that the methodology divergences (DPG-2 vs. DPB-3) are work-unit-class variations on the unified architecture's per-typed-object cycle shape. Show that the substrate primitives are 80%+ shared (per splitter clusters 1-8) and the residual is mandate-parameter-data, not architecture-shape."*
- **`X_GFB_X`** (attacker). *"Argue that the separate drafts CANNOT collapse. Use CTR-G3 (cold-start ≠ legacy-ingestion asymmetry, lumper Cluster-4) as your primary anchor. Show that the substrate primitives required at greenfield day-0 (Intent Crucible, Cold-Start Bench, RSI declaration) have no brownfield analog; show that the brownfield primitives (codebase model with five views, dependency graph, telemetry ingestor) have no greenfield analog. The unified architecture's '`priors.in-tree: []`' for greenfield is a vacuous slot; same for brownfield's bootstrap-from-priors story."*

---

*End of draft-unified-synthesis.md (Phase-3.1).*
