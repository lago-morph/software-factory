---
artifact: draft-brownfield-synthesis
phase: 3.1
inputs:
  - tracks/brownfield-substrate-first.md
  - tracks/brownfield-methodology-first.md
  - tracks/brownfield-legacy-ingestion-first.md
bias-guard-inputs:
  - bias-guards/phase-2/anchor-detector.md
  - bias-guards/phase-2/axis-divergence-audit.md
  - bias-guards/phase-2/lumper.md
  - bias-guards/phase-2/splitter.md
based-on-commit: b65ec23a502c12706ab387b8e9fe4076c7b2f969
based-on-date: 2026-05-25
---

# Draft Brownfield Synthesis (Phase 3.1, pre-adversarial)

**Status.** Lead-agent merge of three Phase-2 brownfield tracks. Same convention as the [greenfield draft](draft-greenfield-synthesis.md): ROBUST (all three tracks support) vs. DECISIONS-PENDING (tracks diverge in a user-actionable way). Phase-2 bias-guard findings inlined where they shift the weight of a claim.

---

## §1 ROBUST claims (all three tracks support)

### §1.1 Mandate framing

- **ROBUST-B1.** Brownfield is constitutively **code-archaeological**: every cycle's first operation is reading the existing system as it currently is (UC4 second clause; CTR-G4 resolved on the code-as-readable side). The existing codebase, its tests, dependency graph, runtime telemetry, and change history are *primary inputs that constrain* what the factory can do — not optional context. CTR-G1 (corpus admits brownfield asymmetry but designs as if it doesn't) is honored, not retrofitted.

- **ROBUST-B2.** **Brownfield is *not* symmetric to greenfield cold-start** (CTR-G3). All three tracks honor this distinction explicitly. The brownfield analogue is *legacy-ingestion* — a substrate setup operation, one-time-and-incremental, that reads the existing codebase and produces a queryable model. Greenfield's cold-start (brief §5) is methodology-creation from priors; brownfield's legacy-ingestion is methodology-application against an existing artifact. Lumper Cluster-4 confirms the corpus distinguishes these phenomena; the brownfield §5 treatments correctly *recast* the brief's greenfield-only cold-start mandate as a legacy-ingestion analog rather than claiming symmetry.

### §1.2 Substrate / codebase model (load-bearing)

- **ROBUST-B3.** A queryable, incrementally maintained **codebase model** (`CodebaseModel`, splitter Cluster-11) is load-bearing. The model is built by an ingestion phase, queried by per-cycle agents, and refreshed by a maintenance loop. Per-cycle agents query *slices*; they do not re-ingest. F21 (context-window exhaustion, brownfield-critical) is structurally unavoidable without this.
  - *Lumper Cluster-6 split:* "the codebase" as a monolithic input lumps brief §0's enumerated five categories (code / tests / dependencies / runtime telemetry / accumulated history). The model has *five views/sub-stores*, not one — Phase-3 must require any "the codebase reader" claim to enumerate which views it consumes.

- **ROBUST-B4.** The model's **five sub-stores** (the splitter Cluster-11 / lumper Cluster-6 unified shape):
  1. **Codebase index** (symbols, definitions, references, call graph, type information where available; incremental updates per commit).
  2. **Dependency-and-impact graph** (per-symbol and per-module edges; per-change blast-radius computation; surfaces F34 cross-layer-drift signals).
  3. **Runtime/telemetry view** (production traces, OpenTelemetry events, error rates per module, hot paths; partitioned-by-role per ROBUST-B6).
  4. **Change-history / attribution view** (per-commit, per-PR, per-issue attribution; per-agent and per-model attribution for prior cycles per F14 widened forensic-reconstruction).
  5. **Invariant / debt view** (extracted from tests, types, runtime assertions, schema constraints; TODOs, deprecation markers, known-bad regions, dependency staleness).
  *Tracks differ in nomenclature only:* BF-S's S-1/S-2/S-3/S-4 list; BF-L's six-view enumeration (structural/conventional/historical/runtime/invariant/debt); BF-M's per-cycle stage-2 archaeological brief (which is the *query output* of the model, not the model itself — these compose: model is substrate, brief is methodology-layer query result).

### §1.3 Substrate primitives (cross-mandate-shared, brownfield-specifics)

- **ROBUST-B5.** **Production-scissors substrate-default-off** (F44 brownfield-critical; CaMeL-class typed-interpreter boundary at production-adjacent code). Same primitive as ROBUST-G9 in the greenfield draft; brownfield is the regime where it is *most* load-bearing (F12 / F33 / F44 / F56 all brownfield-critical). Splitter Cluster-5 unifies as `PerimeterClosure`.

- **ROBUST-B6.** **D-4 holdout discipline substrate-enforced via role-partitioning of in-codebase reads.** All three tracks accept D-4 *with expansion*: substrate enforces role-based view filters on the codebase index, dependency graph, and telemetry — not file-system partition. Lumper Cluster-2 splits this from out-of-tree-directory D-4: it is the **in-codebase-partitioned** locus of the same discipline. F28 (holdout leakage) mitigated at substrate; methodology cannot opt out.

- **ROBUST-B7.** **D-2 explicitly challenged for brownfield.** All three brownfield tracks challenge D-2 (scenarios live outside the codebase as holdout set). Brownfield scenarios are drawn from production traces, existing tests, runtime telemetry — the *unseen* subset is the holdout, not the *out-of-tree* subset. CTR-B5 + WEAK-3 sharpening (StrongDM's own primary docs already permit in-tree scenarios via incident replays / agentic simulation). This is the corpus signal anchor-detector G-CONV-3 confirms.
  - *Lumper Cluster-5 split:* "scenarios" lumps four distinct artifact shapes (Kaner / EARS-criteria / regression-tests / production-telemetry). Brownfield holdouts predominantly use the *regression-test* and *production-telemetry* shapes; Phase-3 should preserve the taxonomy.

- **ROBUST-B8.** **Cross-model judge at high-stakes cycles** (`TypedJudgeCall`, splitter Cluster-2). Per-cycle V&V step runs different-model-family review on builder output (F46 mitigation; CJ Hess kevin/carl, report [`34`](../../research/34-lenny-howiai-personal-harnesses.md) §6.2). The three judge sub-shapes (same-model-different-role / different-family-on-builder / different-family-on-spec) remain distinct per lumper Cluster-1; brownfield primarily uses sub-shape (b) — different-family on builder output. Anthropic same-model-different-role auto-review (report [`23`](../../research/23-anthropic-engineering-trilogy.md) §3.5) is acknowledged as a valid sub-shape but is *not* the brownfield default given the absence of pre-graduated work-unit-class evidence at the start of any new factory's brownfield engagement.

- **ROBUST-B9.** **Tiered watchdog Daemon / Triage / Patrol (D-6)** substrate-resident. Patrol's primary signal in brownfield is *cross-layer drift* — the explicit F34 (brownfield-critical) detector lives here. The model's invariant view feeds Patrol; Patrol watches for drift between the fast-layer code changes and the slow-layer invariants. Lumper Cluster-9 split still applies: the F34 / F54 / F55 / F57 lump must be split per-F-mode with named detectors.

- **ROBUST-B10.** **Trajectory capture (D-7) and immutable attribution (`AttributedEventLog`, splitter Cluster-6)** substrate-resident, content-addressed, signed. Required for F35 (federation-as-family drift), F43 (RSI Board-Visibility Gap, brownfield-high), F54 (goal subversion, brownfield-critical), F58 (runtime/design-time compliance split, brownfield-high). HMAC signing where coordination crosses an unsigned boundary (F32). The substrate enforces; methodology cannot bypass attribution.

- **ROBUST-B11.** **Hard cost ceilings non-optional (D-5).** Per-cycle and per-phase budgets. Brownfield is the regime where ceilings *matter most*: Stripe's 1,300 PRs/week (report [`35`](../../research/35-lenny-howiai-spec-driven-and-team-ops.md)) and Cherny's $100K+/mo (CTR-E1) anchor industrial-scale brownfield in a 10× cost-variance band. Ceilings are per-cycle parameters, configurable per work-unit-class.

### §1.4 Cycle / methodology shape (substantially shared)

- **ROBUST-B12.** The per-cycle process flows through approximately 6–8 named obligations (BF-M lists 8; BF-S lists 8; BF-L abstracts to 3-loop architecture but the work-loop's per-cycle expansion lands in the same 8-stage shape). Cross-track aggregate:

  1. **Trigger / classification.** Issue / change-request / regression alert / dependency bump / scheduled patrol finding / operator-initiated proposal. Convert to typed work-unit-class declaration (D2 taxonomy: `regression-fix` / `refactor` / `post-mvp-evolution` / `codebase-evolution-proposal` / `mvp-extension`). Cycle refuses to start on classification failure.
  2. **Comprehension.** Read the codebase model's relevant slice. Produce an archaeological brief (per BF-M) or surface the relevant model views (per BF-S/BF-L).
  3. **Intent capture.** Author a *change-intent block* (per-cycle; BF-M § 1.1 stage-3) — a contraction of El Kaim's 9-field intent block fit to a per-PR change rather than a whole-system spec. Fields: rationale, invariants-to-preserve, observable acceptance, regression surface, blast radius, rollback plan. *Spec the change, not the system.*
  4. **Plan.** Multiple candidate plans (BF-M's N ≥ 3; per Klaassen four-clause plan-prompt, [`followup/05`](../../research/followup/05-klaassen-siblings.md)) with adversarial critic. Decompose only to the point intent-stability permits — F59 (premature decomposition) is the explicit hazard.
  5. **Build.** Execute the plan in an isolated worktree (F17 mitigation). Cost ceiling (D-5), tiered watchdog (D-6), trajectory capture (D-7), production-scissors-off (F44) all substrate-enforced.
  6. **Cross-model review.** Different-family reviewer (F46 mitigation, ROBUST-B8). Specialized critics for code-quality, security, conformance-to-existing-conventions (Anthropic Auto-Review pattern, [`report 23 §3.5`](../../research/23-anthropic-engineering-trilogy.md); Codex Auto-Review, [`report 18`](../../research/18-openai-codex-substrate.md)).
  7. **Acceptance.** Run the held-out scenario set + existing test suite + deterministic linter + Ashby-aware deterministic perimeter check (F51 mitigation). *Holdout is unseen subset, not out-of-tree subset* (ROBUST-B7). Scenarios MAY be drawn from codebase per CTR-B5 inversion.
  8. **Ship-or-escalate.** Open PR with structured commit metadata (F14 attribution), with change-intent block + archaeological brief + trajectory pointer attached as PR body; or escalate to human under declared trigger conditions (regression severity > threshold; blast radius > policy; novel risk pattern; F56 stress-bypass detection).

### §1.5 Bootstrap (legacy-ingestion)

- **ROBUST-B13.** **Legacy-ingestion is a substrate setup operation, one-time-and-incremental.** Day-0 of a new brownfield factory engagement:
  - Index the codebase (one-time bulk pass, incremental thereafter).
  - Derive the dependency-and-impact graph (may require human-curated module-boundary hints for codebases without clean module boundaries).
  - Connect to existing telemetry; if none exists, the first work-unit-class becomes *adding telemetry* (self-bootstrap step per BF-S §5).
  - Ingest git history; tag pre-factory commits as unattributed (from day 0 forward, attribution is substrate-enforced).
  - Declare the trifecta perimeter (production-scissors off; sandbox configuration; cross-model judge slot) — upfront policy, applies before the first cycle.

- **ROBUST-B14.** **Day-0 brownfield cycles default to L3-Augmentation per work-unit-class until evidence accumulates.** Same graduation discipline as the greenfield (ROBUST-G1, ROBUST-G2): no work unit is `automation-eligible` until per-cycle evidence (S-2 impact graph stability; S-3 telemetry density; S-1 coverage; cross-model judge agreement rate) clears a declared bar. Per Jaymin CTR-A5 (brownfield L3 ceiling), this is *the regime claim itself* — and the brownfield-fit of substrate evidence is what makes L4-lights-out reachable for the specific work-unit-classes where evidence is dense.

### §1.6 Failure-mode coverage

All three tracks address the brownfield-critical F-mode set with substantially identical mitigations:

| F-mode (brownfield severity) | Mitigation locus (shared across tracks) |
|---|---|
| F12 / F33 / F44 (lethal trifecta cascade, critical) | `PerimeterClosure` (ROBUST-B5); CaMeL boundary at production-adjacent build steps; cross-model judge at cycle step 6; substrate-default-off (Lumper Cluster-10: four cascade layers, not one) |
| F14 (forensic reconstruction widened) | `AttributedEventLog` (ROBUST-B10) |
| F20 (maintenance asymmetry, critical) | The architecture's shape itself addresses this — by being brownfield-shaped, not greenfield-with-context |
| F21 (context exhaustion, critical) | Codebase model returns slices (ROBUST-B3); per-cycle agents query the model, not the raw codebase |
| F22 / F23 (zombie agents, stalled-vs-thinking) | D-6 Daemon + Triage tiers |
| F28 (holdout leakage, critical) | D-4 substrate-enforced role-partitioning (ROBUST-B6) |
| F32 (unsigned coordination injection) | HMAC signing on coordination crossing unsigned boundary |
| F34 (cross-layer drift, critical) | Patrol-tier watchdog reads invariant view of codebase model |
| F35 (federation-as-family drift, high) | Cross-cycle attribution + Patrol cross-cycle scan |
| F43 (RSI Board-Visibility Gap, high) | `AttributedEventLog` produces Caremark prong-1 board-reporting surface |
| F46 / F48 (single-model review blindspot, tacit collusion) | Cross-family judge at cycle step 6 (ROBUST-B8) |
| F51 (Ashby-deficient probabilistic guard, high) | Deterministic perimeter at cycle step 7 (acceptance) — *not* LLM-judge as primary closure |
| F52 (Tempting-Wrong-Hybrid) | All three tracks cap deterministic wrappers at substrate layer; methodology runs an LLM-based cycle, not a deterministic-wrapped LLM |
| F53 (voluntary-discipline fragility, high) | Substrate-default rather than operator-instruction (substrate-side of every "do the discipline" surface) |
| F54 (goal subversion across cycles, critical) | Per-cycle attribution + Patrol cross-cycle goal-frame audit + cross-cycle change-intent rationale comparison |
| F55 (behavioural drift / self-reference, high) | Cross-model reviewer breaks self-reference; codebase model's runtime view provides out-of-distribution ground truth |
| F56 (Replit-class stress bypass, critical) | Substrate-default production-scissors-off (F44); cycle step 8 escalation triggers include detected attempt-to-bypass |
| F57 (design-authority erosion) | Classifier decisions are themselves attributed; Patrol audit-trail of classifier drift |
| F58 (runtime/design-time compliance split, high) | Trajectory + telemetry views share the attribution store |
| F60 (parallel-cycle compounding error) | Cycle parallelism caps are per-work-unit-class regime parameters |
| F61 (context fragmentation across agents) | Shared canonical codebase-model views; agents don't fragment context, they query the model |

### §1.7 Defaults marking (§4 of brief)

| Default | Brownfield stance | Justification |
|---|---|---|
| D-1 (specs durable / version-controlled / human-curated) | **mostly accepted** | Spec content differs: change-intent blocks per cycle + the codebase itself + (optionally) maintained intent layer above. BF-M challenged partial: "the cycle's load-bearing durable artifact is the change-intent block + archaeological brief + PR + codebase, not a single global system spec." BF-L challenged: "the codebase model is the primary artifact; specs are layer-on-top." BF-S accepted with the codebase-as-spec framing per UC4. **Surfaced as DPB-1.** |
| D-2 (scenarios outside the codebase as holdout set) | **challenged, all 3 tracks** | See ROBUST-B7. Holdout is *unseen subset*, not *out-of-tree subset*. |
| D-3 (Agent = Model + Harness) | **mixed: 2 accepted with note, 1 challenged** | BF-S accepts with CTR-C10 flag; BF-M accepts at per-stage scope (the cycle as a whole is not an agent); BF-L challenges partially — the codebase model is a substrate primitive that does not decompose into M+H; ingestion-phase agents are graph-shaped. **Surfaced as DPB-2.** |
| D-4 (holdout discipline substrate-enforced) | **accepted with expansion, all 3 tracks** | See ROBUST-B6. |
| D-5 (hard cost ceilings non-optional in CI) | **accepted, all 3 tracks** | See ROBUST-B11. |
| D-6 (tiered watchdog substrate primitive) | **accepted, all 3 tracks** | See ROBUST-B9. |
| D-7 (trajectory capture cheap and production-tested) | **accepted, all 3 tracks** | See ROBUST-B10. |

---

## §2 DECISIONS-PENDING (tracks diverge; user input required at Phase-3.4)

### DPB-1. Primary durable artifact: change-intent blocks / codebase / external spec?

- **Divergence.**
  - **BF-S.** D-1 accepted: "spec" includes the existing codebase (UC4) plus any intent layer the operator chooses to maintain. The codebase IS the durable artifact.
  - **BF-M.** D-1 challenged (partial): "the cycle's load-bearing durable artifact is the change-intent block per cycle + the archaeological brief per cycle + the PR + the codebase itself, not a single global system spec." Per CTR-B2 / CTR-B7 / CTR-F1, brownfield does not require a global spec to be primary; the codebase IS the durable artifact (Brier pace-layer 1 "code is fashion" framing **rejected** for brownfield; Willison's low-background-steel framing preferred).
  - **BF-L.** D-1 challenged: the durable, version-controlled artifact is the **codebase model** (derived from the codebase, refreshed per cycle), not a human-authored spec. Specs exist for *change requests* but are derived from the model and re-anchored to it. Brier (followup [`12`](../../research/followup/12-brier-pace-layers.md), pace-layer-3-not-1) and CTR-B3 / CTR-B7 weaken D-1's claim that the spec is *the* primary artifact.
- **User question.** What is the brownfield architecture's primary durable artifact: (a) the codebase itself (BF-S); (b) the per-cycle change-intent block + PR + codebase (BF-M); or (c) the codebase model as derived artifact, with specs as layer-on-top (BF-L)? This shapes Phase-6 architecture spec authoring — specifically the architecture's "what does the operator maintain" surface.
- **Concrete next action.** User-resolved choice at Phase-3.4. If (a), brownfield architecture specs declare "no global spec maintained"; if (b), specs declare a change-intent template; if (c), specs declare a maintained codebase-model schema.

### DPB-2. D-3 decomposition: same question as DPG-1, with brownfield variant

- **Divergence.** BF-L explicitly challenges D-3 because the codebase model is a substrate primitive that does not decompose into "Model" or "Harness," and ingestion-phase agents are graph-shaped (per CTR-F3 reframing). BF-S accepts with CTR-C10 caveat; BF-M accepts at per-stage scope.
- **Folds into DPG-1** — same user resolution.

### DPB-3. Methodology shape: continuous substrate query / 8-stage cycle / three-loop architecture?

- **Divergence.** Three structural shapes, more aligned than the greenfield trio but still distinguishable:
  - **BF-S.** Methodology overlay is **thin** — work-unit selection, per-cycle composition of substrate queries, per-cycle V&V, knowledge promotion. Substrate is continuous (incrementally maintained S-1–S-5 on every push); methodology composes queries. Single cycle is 8 steps that lean heavily on substrate.
  - **BF-M.** Methodology is **the 8-stage cycle** *as the architecture*. The cycle's stages are named methodology obligations with substrate capabilities declared at the boundary; stages compress/expand by work-unit-class. Substrate is downstream, not upstream.
  - **BF-L.** Methodology is **a 3-loop architecture** (Ingestion deep-and-slow / Work per-cycle 8-stage / Maintenance continuous) over a shared codebase model. Work-unit-class taxonomy itself is *derived from the codebase model*; cycle stages are similar to BF-M but the methodology *consumes* the model's profile.
- **Axis-divergence-audit finding (§3.1).** "Effective overlap on primitive list: ~70%. Effective overlap on *where the load-bearing investment sits*: <30%. Axis is doing real work but the corpus signal is strong." The three brownfield tracks are *closer* to aliases than the greenfield trio, but the load-bearing-investment differences are real.
- **User question.** Pick one of three structural framings: substrate-continuous-with-thin-methodology (BF-S); methodology-cycle-as-architecture (BF-M); three-loop-over-codebase-model (BF-L). Or commit to a combination.
- **Concrete next action.** User resolves at Phase-3.4. Phase-4 substrate/methodology extraction needs the chosen framing to assign primitives.

### DPB-4. Codebase-model continuity: maintained vs. per-cycle-reconstructed

- **Divergence.** BF-S: codebase model is *continuously maintained* on every commit (incremental, substrate-resident). BF-M: model is *per-cycle reconstructed* as the archaeological brief during stage 2 (not maintained between cycles). BF-L: model is *built by ingestion phase, refreshed by maintenance loop* — closer to continuous but with explicit refresh cadence as a tunable.
- **Lumper Cluster-11 unify recommendation.** Splitter recommends unifying as `CodebaseModel` substrate primitive; BF-L's framing is "most general." This is a unification recommendation — but the three tracks differ on whether the model is *maintained between cycles* (BF-S, BF-L) or *reconstructed per cycle* (BF-M). That difference has architectural consequences for cost and freshness.
- **User question.** Is the codebase model (a) continuously maintained on every commit (BF-S); (b) per-cycle-reconstructed (BF-M); or (c) built-and-refreshed on declared triggers (BF-L)?
- **Concrete next action.** Phase-5 wave-1 ADR ("Codebase-model maintenance cadence"). Cost, freshness, and F34 (cross-layer drift) detection sensitivity are the relevant trade-offs.

### DPB-5. Work-unit-class taxonomy: pre-decided vs. model-derived

- **Divergence.** BF-S and BF-M use the D2 default 5-class taxonomy (`regression-fix` / `refactor` / `mvp-extension` / `post-mvp-evolution` / `codebase-evolution-proposal`). BF-L *derives* the taxonomy from the codebase model's profile: a codebase with heavy issue tracker and stable architecture surfaces issue-from-queue work; one with active spec-driven refactoring surfaces change-request-against-spec; one with accumulating debt and no issue queue surfaces codebase-evolution-proposals.
- **Anchor-detector flag (F-ANCHOR-4, MEDIUM).** D2's matrix was *documentation discipline*. BF-L's derive-from-model approach is more general than D2's flat taxonomy but also more substrate-load-bearing.
- **User question.** Is the work-unit-class taxonomy (a) a fixed default per D2, (b) per-deployment configurable by the operator, or (c) substrate-derived from codebase-model profile (BF-L)?
- **Concrete next action.** Phase-5 wave-1 ADR ("Work-unit-class taxonomy source"). Interacts with DPG-3 / DPB-7 below (eligibility classifier).

### DPB-6. Per-region vs. per-work-unit-class regime classification

- **Divergence.** BF-L's eligibility classifier classifies *per code region*: a regression-fix against a high-coverage, low-churn module flows to L4-lights-out; the same fix against a low-coverage, high-churn region flows to L3-augmented. BF-S/BF-M classify *per work-unit-class* (D2 default).
- **BF-L's own §7 question 4 flags:** "does per-region regime classification fragment governance (F43 board-visibility gap) by making the 'what regime is the factory at' answer a function of which region is being touched?"
- **User question.** Is the eligibility classifier (a) per-work-unit-class (BF-S/BF-M; matches D2), or (b) per-(work-unit-class × code-region), where region-properties feed the classifier?
- **Concrete next action.** Phase-5 wave-1 ADR. Note F43 (board-visibility gap) interaction: per-region classification creates a more granular surface that may be harder to summarise for Caremark prong-1 reporting.

### DPB-7. Eligibility classifier: substrate primitive or methodology / policy concern?

- **Folds into DPG-3** — same divergence with brownfield specifics. BF-S/BF-L both place classifier at substrate; BF-M places its trigger-and-classification at stage 1 of the methodology cycle (between substrate and methodology). The brownfield-specific dimension: classifier *inputs* are substrate-evidence-heavy in brownfield (S-2 impact graph, S-3 telemetry density) vs. graduation-history-heavy in greenfield. The placement question is the same.
- **Concrete next action.** Same Phase-5 wave-1 ADR as DPG-3, with brownfield-specific evidence-inputs section.

### DPB-8. Same-model vs. cross-family judge default

- **Divergence.** All three tracks adopt cross-family as the brownfield default. BF-M flags in §7 OQ-T2: "Husain/Shankar same-model judging fine when task differs is empirically anchored and contradicts this track's stage-6 cross-family insistence." BF-L sides "partially with the F46-mitigation position over Anthropic's single-judge-is-fine position for the cold-start period specifically" — implying steady-state might allow same-model.
- **Lumper Cluster-1 split (load-bearing).** The three judge sub-shapes must remain distinct in Phase-3. CTR-D7 (Anthropic same-model-different-role suffices) and CTR-D8 (model-family diversity necessary) are the corpus split; the brownfield default sits on the F46 / kevin/carl side, but the "necessary vs. contingent" question is unresolved at the architecture layer.
- **User question.** For brownfield steady-state (post-evidence-accumulation), is cross-family judge *necessary* (BF default) or *contingent* (allowing same-model-different-role per Anthropic)? Cost impact is non-trivial — cross-family is ~2× per-cycle inference; same-model-different-role is ~1.1× (per BF-M §7 OQ-T2).
- **Concrete next action.** Phase-5 wave-2 ADR ("Judge sub-shape per work-unit-class × evidence-density cell"). Empirical question — interacts with Phase-8 lean-eval brief.

### DPB-9. Telemetry-bootstrap: what if S-3 doesn't exist yet?

- **Divergence implicit, surfaced by BF-S §7 OQ-T3.** "Many brownfield codebases (especially mid-market per Kahana report [`31`](../../research/31-caremark-rsi-board-exposure.md)) lack production telemetry. The substrate's self-bootstrap step (add telemetry as first work-unit-class) needs to be safe to run at L3 (operator-gated), but the cycle that adds telemetry has none of the S-3 evidence to clear an L4 threshold."
- **All three tracks agree** that adding telemetry can be the first work-unit-class; none specify *how* the substrate's eligibility classifier handles the degraded-S-3 starting condition.
- **User question.** Does the brownfield substrate (a) refuse to engage codebases without production telemetry until telemetry is added (gating); (b) accept degraded-S-3 with a stricter eligibility classifier that compensates via lower automation thresholds; or (c) treat telemetry-addition as a special pre-cycle setup task, like legacy-ingestion?
- **Concrete next action.** Phase-5 wave-2 ADR ("Substrate behaviour under degraded codebase-model views"). Connects to ROBUST-B13 (legacy-ingestion as substrate setup).

### DPB-10. Compound Engineering / Compound Knowledge: methodology pattern or substrate primitive?

- **Divergence.** All three tracks allow Compound-Engineering-style loops (plan → work → review → compound, [`report 03`](../../research/03-every-compound-engineering.md)) and Compound-Knowledge-style typed learnings ([`followup/11`](../../research/followup/11-compound-knowledge.md), brownfield-primary per inventory CHALLENGE-7) but place them differently. BF-S allows Compound-as-methodology-overlay running on the substrate. BF-M makes Compound's plan/work/review the cycle steps 4/5/6. BF-L treats the typed knowledge store as a methodology concern (the substrate owns records / S-4; the rules for promoting / retiring patterns live in methodology).
- **Lumper Cluster-9 partial-keep recommendation.** Compound Engineering / Compound Knowledge family is corpus-faithful; unify the family identity. But whether the *knowledge store* (Compound's `docs/solutions/` directory, Beads `discovered-from` edges) is substrate or methodology is the per-track placement question.
- **User question.** Is the knowledge store (a) a substrate primitive (BF-L's "S-4 attribution + Compound-Knowledge typed records"), or (b) a methodology-layer artifact stored in the substrate's general-purpose store?
- **Concrete next action.** Phase-4 substrate/methodology extraction question. If (a), a Phase-5 wave-1 ADR drafts the typed-knowledge-store schema. If (b), Phase-6 architecture specs each declare their knowledge-store convention.

---

## §3 Open questions surfaced by individual tracks (preserved for Phase-3 adversarial reference)

- **BF-S OQ-T1.** Substrate-vendor choice for brownfield (CTR-C5 unresolved; OpenHands measurement context is single-cycle replay; Gas City's Beads `discovered-from` edge is closer to S-4 needs).
- **BF-S OQ-T2.** S-2 dependency-graph maintenance for polyglot codebases (corpus does not directly address; F45 Language-as-Harness Mismatch interacts).
- **BF-S OQ-T3 (cited as DPB-9).** "Telemetry doesn't exist yet" failure mode for S-3.
- **BF-S OQ-T4.** Cross-model judge availability and cost (CTR-E1 / CTR-E6 anchors; sample-rate cross-model judging open question).
- **BF-S OQ-T5.** D-2 challenge cascading to D-4 — substrate-vs-methodology boundary issues for Phase 4.
- **BF-S OQ-T6.** Legacy-ingestion bounded vs. continuous (vendored libraries, acquired-company code can re-trigger).
- **BF-M OQ-T1.** Stage-compression rules per work-unit-class (Phase-3/Phase-6 task).
- **BF-M OQ-T2 (cited as DPB-8).** Cross-model review necessity under CTR-D7/D8.
- **BF-M OQ-T3.** CaMeL utility-tax acceptance criterion (~7-point, CTR-E6).
- **BF-M OQ-T4.** Scenarios-from-codebase governance (D-2 challenge inverts holdout-location but does not specify how unseen subset is selected from codebase-derived pool without leaking).
- **BF-M OQ-T5.** Per-cycle vs. cross-cycle Patrol scope (substrate or per-architecture?).
- **BF-M OQ-T6.** Brownfield regime ceiling (CTR-A5) measurability — Phase-8 lean-eval candidate.
- **BF-M OQ-T7 (cited as DPB-10).** Methodology evolution disposition.
- **BF-M OQ-T8.** Anthropic Skills network-closure (CTR-C9) vs. dreaming during Comprehension and Patrol.
- **BF-M OQ-T9.** Knowledge-curator placement (next-reader's obligation vs. curator daemon).
- **BF-M OQ-T10.** F36 instruction-following ceiling interaction with change-intent block growth.
- **BF-L OQ-T1.** Ingestion-as-substrate vs. ingestion-as-methodology (Phase 4 placement).
- **BF-L OQ-T2.** Symmetry with greenfield cold-start (CTR-G3 surfaced; not resolved).
- **BF-L OQ-T3.** Model staleness vs. cycle latency tradeoff (maintenance loop cadence — interacts with DPB-4).
- **BF-L OQ-T4 (cited as DPB-6).** Per-region vs. per-work-unit-class regime.
- **BF-L OQ-T5.** Ingestion vs. work provider-profile split (OQ-B8 interaction).
- **BF-L OQ-T6.** Codebase model as attack surface — F54 goal subversion via model poisoning. Model-integrity primitive not specified.
- **BF-L OQ-T7.** F35 federation-as-family drift at model-schema level.
- **BF-L OQ-T8.** CaMeL utility-tax applied to model queries.

---

## §4 Phase-3.2 adversarial dispatch notes

The 6 persona-adversarial subagents per draft. Specific instructions per persona:

- **Red-team.** Target ROBUST-B7 (D-2 challenged: scenarios from codebase). Argue: in-codebase scenarios cannot be cleanly partitioned from builder context; substrate role-partitioning is theoretical and breaks in practice. Counter-example required from corpus or from sound architectural reasoning.
- **Pre-mortem.** Target DPB-3 (methodology shape) and DPB-4 (codebase-model continuity). 18 months in, the codebase has changed substantially, the model has been refreshed many times, agents have made suggestions that became commits which the model now indexes. Which of BF-S / BF-M / BF-L fails first, and how?
- **Regulator.** Target ROBUST-B10 (`AttributedEventLog`) and DPB-6 (per-region regime). SOC 2 / SEC IAC / SB 53 audit obligations: does per-region regime classification create a defensible audit trail or a fragmented one? What does a Caremark prong-1 board report look like for a factory whose regime varies by code region?
- **CFO.** Target ROBUST-B8 (cross-model judge) and ROBUST-B11 (cost ceilings). At Stripe scale (1,300 PRs/week, [`report 35`](../../research/35-lenny-howiai-spec-driven-and-team-ops.md)), cross-family judge at every cycle is N PRs × ~2× inference × N codebases. What's the unit economics for cross-family vs. sample-rate cross-family?
- **10-year on-call.** Target the codebase model (ROBUST-B3/B4). Three years in, the model has accreted views, the original ingestion was on a 200k-LOC codebase that's now 800k-LOC, with three acquired-codebase merges. Which view's maintenance is most likely to silently rot? How does the on-call engineer diagnose stale-S-2 vs. stale-S-3?
- **Naive newcomer.** Target the entire draft for jargon, hidden anchors. Specifically: is BF-L's "codebase model as substrate primitive" understandable, or does it presume reading 10 research reports first?

Cross-mandate dispatch (with greenfield draft):
- **G+B unify advocate.** Argue: the brownfield and greenfield drafts can collapse into one architecture. Use the unified-tracks' typed-object framing (interval / layer / anchor) as the unifier; show that the methodology divergences (DPG-2 vs. DPB-3) are work-unit-class variations on a shared cycle shape.
- **G+B cannot-unify attacker.** Argue: the cold-start vs. legacy-ingestion asymmetry (CTR-G3) is structurally load-bearing — the substrate primitives required at greenfield day-0 (Intent Crucible, Cold-Start Bench) have no brownfield analog, and the brownfield primitives (codebase model, dependency graph) have no greenfield analog. The drafts CANNOT collapse without losing mandate-specific load-bearing primitives.

---

*End of draft-brownfield-synthesis.md (Phase-3.1).*
