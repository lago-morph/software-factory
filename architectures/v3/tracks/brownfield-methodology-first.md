---
track: brownfield-methodology-first
axis: methodology-first
mandate-scope: brownfield
based-on-commit: 96a949430b5c356f8b4e688b1d427348a68db468
based-on-date: 2026-05-24
---

# Brownfield, methodology-first

## §0 Axis declaration and defense

**Sub-axis chosen.** Methodology — specifically, **the per-cycle process is the architecture**. For the brownfield mandate the per-cycle process has a knowable shape: it begins at an external trigger (an issue, a change-request, a regression report, a codebase-evolution proposal, a production alert, a dependency-bump notification) and it ends at a merged PR (or an explicit no-PR closure with documented reason). Substrate, scaffold, harness, model, knowledge-store, and security primitives are organised as **whatever the cycle needs at the stage it is in**, not as a pre-decided platform that methodology has to fit on.

**Why this is the right axis for brownfield (defense, pre-responded to Phase-3 adversarial).**

1. **The corpus' brownfield-native methodology shapes already exist as recognisable per-cycle loops.** Compound Engineering's plan → work → review → compound (report [`03`](../../research/03-every-compound-engineering.md)) is a cycle. Notion-Boxy's Notion-comment → background-agent → PR (report [`35`](../../research/35-lenny-howiai-spec-driven-and-team-ops.md)) is a cycle. CJ Hess's `kevin/carl` cross-model QC inside a Ralph loop (report [`34`](../../research/34-lenny-howiai-personal-harnesses.md)) is a cycle. SWE-bench Verified's `Issue + Codebase → LM → PR → Tests` (report [`22`](../../research/22-academic-foundations.md)) is a cycle. The corpus signal for brownfield is **"the shape of one issue's life"**, not **"the shape of the platform underneath all issues."** Building the architecture around the cycle puts the load-bearing variable in the centre.
2. **Substrate-first risks importing a greenfield organising principle.** Round-2's substrate-heavy + thin-methodology recommendation ([`13-round-2-synthesis`](../../archive/synthesis-v1-v2/13-round-2-synthesis.md) §8) was synthesised in a corpus that was still mandate-agnostic; CTR-C2 names the tension between that framing and UC4's stronger-methodology hypothesis. For brownfield specifically, the existing system is *already the substrate* — runtime, schema, test suite, deploy pipeline, observability stack, code conventions are in place. A brownfield architecture that re-decides substrate first ignores the brownfield mandate's defining input (UC4, CTR-G4: code-as-readable-archaeological-input). Methodology-first does not.
3. **The contested defaults sit at the methodology layer, not the substrate layer.** D-2 (scenarios outside codebase) is brownfield-fragile (CTR-B5; the brownfield-tagged sharpening notes StrongDM itself reads runtime telemetry). D-1 spec-velocity is contested (CTR-B2, CTR-B7). The "where does the unit of work come from" question (OQ-B4) is a methodology question. A track that organises by methodology surfaces these tensions in its primary structure; a substrate-first track is forced to handle them as overlays.
4. **Brownfield has no cold-start ambiguity to hide behind.** Greenfield's cold-start problem (brief §5) gives substrate-first tracks a place to put their leverage (bootstrap primitives before methodology exists). Brownfield day-0 is concrete: there is a codebase, there is an issue queue (or there is the act of creating one), there is a deploy. Methodology-first matches the concreteness of the input.
5. **Pre-response to "but the cycle borrows everything from substrate."** A methodology-first architecture does not deny substrate — it organises substrate around the cycle's needs at each stage. Substrate primitives appear in §1 as **stage-attached capabilities** (e.g., "the comprehension stage needs a code-traversal capability whose substrate-vendor is to-be-decided in Phase-5") rather than as a pre-decided platform. This is the legitimate methodology-first answer to the substrate-first critique: substrate is *named* but its *enumeration and selection* is deferred.
6. **Pre-response to "this just smuggles in Compound Atelier."** It does not — Compound Atelier is one of several cycle shapes the methodology can host. The cycle defined in §1 is generic across "issue from a queue" (Atelier-style, glossary §0), "change request against a spec" (Refinery-style), and "codebase-evolution proposal" (the third OQ-B4 shape not in the v2 set). Phase-7 back-fill will decide whether any v2 architecture is a special case of this cycle.

## §1 Architecture sketch

### 1.1 The brownfield cycle (the architectural primary unit)

Each per-cycle run flows through eight stages. The stages are **named methodology obligations**, not a pipeline of services. Each stage declares the substrate capability it needs at the boundary, and what it must produce for the next stage.

| # | Stage | Trigger / input | Methodology obligation | Substrate capability required |
|---|---|---|---|---|
| 1 | **Trigger** | Issue, change-request, regression alert, dependency bump, scheduled patrol finding, operator-initiated proposal | Convert the trigger into a typed **work-unit-class** declaration (`regression-fix` / `refactor` / `post-mvp-evolution` / `codebase-evolution-proposal` / `mvp-extension`) per D2's taxonomy. Refuse to start if classification fails. | Trigger inbox + classifier prompt + classification audit log |
| 2 | **Comprehension** | The codebase + the trigger | Read the relevant slice of existing code, tests, recent commits, prod traces, runtime telemetry. Produce an **archaeological brief**: what is here, how it works, what constraints it enforces, what the trigger touches. | Code-traversal tools; runtime-telemetry read; trajectory-capture for the read itself |
| 3 | **Intent capture** | Trigger + archaeological brief | Author a **change-intent block** (a contraction of El Kaim's 9-field intent, report [`14`](../../research/14-el-kaim-book-intent-and-spec-authorship.md), to fit a per-PR change rather than a whole-system spec). Fields: rationale, invariants-to-preserve, observable acceptance, regression surface, blast radius, rollback plan. Spec the *change*, not the system. | Intent-block template + reviewable diff against archaeological brief |
| 4 | **Plan** | Change-intent | Produce N candidate plans (≥3) with explicit trade-offs (per Klaassen four-clause plan-prompt, followup [`05`](../../research/followup/05-klaassen-siblings.md) §"plan-prompt template"). Decompose only to the point intent-stability permits — premature decomposition is the named hazard (F59). | Multi-plan generator; per-plan adversarial critic |
| 5 | **Build** | Selected plan | Execute the plan against an isolated worktree. Code, tests, migration, docs as appropriate. Builder agent has **no access to acceptance criteria withheld at stage 7** (D-4 holdout discipline). | Sandbox; worktree isolation (F17); cost ceiling (D-5); tiered watchdog (D-6); trajectory capture (D-7) |
| 6 | **Cross-model review** | Build output + change-intent | Distinct-model reviewer (F46 mitigation per CJ Hess `kevin/carl`, report [`34`](../../research/34-lenny-howiai-personal-harnesses.md)) checks the diff against the change-intent. Specialized critics for code-quality, security, conformance to existing-codebase conventions (Anthropic Auto-Review pattern, report [`23`](../../research/23-anthropic-engineering-trilogy.md) §3.5; OpenAI Codex Auto-Review, report [`18`](../../research/18-openai-codex-substrate.md)). | Cross-family routing for reviewer; deterministic linters (F38 mitigation) |
| 7 | **Acceptance** | Build output + held-out acceptance set | Run the held-out scenario set + the existing test suite + a deterministic linter pass + an Ashby-aware deterministic perimeter check (F51 mitigation). Brownfield-specifically: scenarios MAY be drawn *from the codebase* (CTR-B5 inversion of D-2) — production traces, existing integration tests, telemetry-derived assertions. The holdout is the *unseen* subset, not the *out-of-tree* subset. | Held-out scenario runner; deterministic perimeter; codebase-derived scenario extractor |
| 8 | **Ship-or-escalate** | Acceptance verdict | Either: open PR with structured commit metadata (F14 attribution), with the change-intent + archaeological brief + trajectory pointer attached as PR body; or escalate to human under a declared trigger condition (regression severity > threshold; blast radius > policy; novel risk pattern; F56 stress-bypass detection). | PR creator; escalation routing per OQ-B3 re-entry protocol |

### 1.2 What sits across the cycle (cross-cutting, not pre-decided substrate)

Three cross-cutting concerns are **named but not pre-allocated to substrate**:

- **Tiered watchdog** (Daemon / Triage / Patrol, glossary §0 + D-6). Daemon attaches to every stage that runs an agent; Triage attaches to stages 4/5/6 where stalled-vs-thinking ambiguity (F23) is acute; Patrol observes across cycles for drift in classification (F57), tolerance (F7), gate strictness (F24), and goal (F54).
- **Knowledge accumulation**. Per-cycle outputs (decisions, surprises, corrections, patterns) are typed (followup [`11`](../../research/followup/11-compound-knowledge.md) four-way classification) and confidence-tagged (`kw:confidence`). Stale-knowledge inversion (F8) is a per-write check, not a batch refresh — but stale-knowledge handling is a methodology obligation of *the next cycle that reads*, not of a curator daemon.
- **Cost ceiling & safety floor** (D-5; F31 minimum-adapter principle). Per-cycle budget caps are pre-declared per work-unit-class; CaMeL-class typed-interpreter boundaries (followup [`08`](../../research/followup/08-security-primitives.md)) wrap the build stage when the work-unit-class is in a `production-adjacent` regime.

### 1.3 What this architecture *is*

It is **a per-cycle methodology contract**: eight stages, named obligations at each, substrate capabilities declared at boundaries, work-unit-class-dependent regime overrides (e.g., `regression-fix` may skip stage 4's multi-plan generation; `codebase-evolution-proposal` may loop stages 2-4 before committing to a plan). The architecture is the *cycle and its variations by work-unit-class*. Substrate vendors (Gas City / OpenHands / Codex / Anthropic Skills / Overstory / custom) are interchangeable at the boundaries the cycle declares.

## §2 How this addresses each load-bearing concern

### 2.1 Lights-out / L5 tension (brief §2.1, OQ-B1)

**Vocabulary mapping (CTR-A4 first).** This track maps "lights-out" to *per-stage human-out-of-loop*, not to L5. Stages 1, 2, 3, 4, 5, 6, 7 run lights-out for automation-eligible work-unit-classes; stage 8 may escalate. The mapping is **per-stage**, not whole-system — which dissolves CTR-A1 / CTR-H10 for the brownfield case.

**Bar source choice (OQ-B6).** Brownfield can clear Jaymin's Automation Mode bars (K=5 ≥90%, prompt-paraphrase 5/5, zero medium+ safety) **on a per-(work-unit-class × stage) basis**, not whole-system. A `regression-fix` cycle with an existing failing test (the test IS the held-out acceptance) is the easiest cell to clear the bars on; a `codebase-evolution-proposal` cycle is the hardest. The architecture's mandate-fit matrix (D2) becomes the bar-clearance matrix: each cell carries its empirical threshold evidence.

**Per Jaymin's brownfield-specific ~L3 claim (CTR-A5):** the cycle's stage-7 acceptance gate is the load-bearing place this claim is contested. If acceptance is held-out + deterministic + scenarios-from-codebase + cross-model-reviewed, the empirical L3 ceiling Jaymin asserts for brownfield is contested by *substrate-enforced verification* rather than by *operator review*. Whether that contests the ceiling enough to clear it is a Phase-3 measurement question.

### 2.2 UC4 working hypothesis

This track is **affirmatively brownfield-shaped** and does not pretend to also be a greenfield architecture. The cycle's stage 2 (Comprehension) and stage 3 (change-intent rather than system-intent) are the two stages that bind it to "existing-architecture-as-given." A greenfield analog would need either to substitute stages 2-3 with a different shape (which is a different methodology) or to admit cold-start as a *meta-stage* upstream of stage 1 (which is the cold-start track's territory). This is consistent with UC4's expectation that the two mandates produce different architectures.

### 2.3 OQ-B4 (unit of work)

The cycle is **work-unit-class-polymorphic**. Per D2, classes hosted: `regression-fix`, `refactor`, `post-mvp-evolution`, `codebase-evolution-proposal`, `mvp-extension`. Atelier-style (issue from a queue) is the trigger shape for `regression-fix` and `post-mvp-evolution`; Refinery-style (change-against-spec) is the trigger shape for `refactor` and `mvp-extension`; codebase-evolution-proposal is the third shape the v2 set lacked (the agent itself proposes the change after stage-2 comprehension surfaces an issue not in any queue). The cycle hosts all three; the variation is which stages compress and which expand.

### 2.4 Selected OQ-B treatments (the rest stay as open questions in §7)

- **OQ-B2 (where greenfield/brownfield boundary falls).** This track asserts: the boundary falls at the **methodology layer** for brownfield. Substrate primitives are mostly mandate-agnostic (CaMeL, trajectory capture, sandboxing, watchdog tiers), but stages 2 (Comprehension) and 3 (change-intent rather than system-intent) are brownfield-defining. Phase-4's substrate/divergence extraction is invited to test this assertion against the 3 unified tracks.
- **OQ-B3 (re-entry).** The cycle's stage 8 is the structured re-entry surface. Declared trigger conditions (regression severity, blast radius, novel risk pattern detected by Patrol, F56-style stress-bypass detection) cause escalation; the operator returns into a defined surface (the PR + change-intent + archaeological brief + trajectory pointer + the failed acceptance line) rather than into an undifferentiated session.
- **OQ-B7 (alternative axes).** This track keeps mandate primary but observes that **work-unit-class** is the second-strongest organising axis for brownfield (per stage compressions/expansions above). Regime, stakes, synchronicity are stage-7-attached attributes (acceptance gate strictness scales with stakes), not separate axes.

### 2.5 Failure-mode coverage (severity-by-stage)

| F-mode | Stage that owns the mitigation | Mechanism |
|---|---|---|
| F1, F27, F46 (correlated review failure) | 6 | Cross-family reviewer routing |
| F2 (reward hacking), F28 (holdout leakage) | 5, 7 | Stage-5 builder lacks stage-7 acceptance; stage-7 enforces holdout. |
| F20 (brownfield asymmetry) | whole cycle | The cycle IS the brownfield-asymmetry-survival argument. |
| F12, F33, F44 (Lethal Trifecta cascade) | 5, 7 | Production-scissors default-off; CaMeL boundary at stage 5 when production-adjacent; stage-7 deterministic perimeter. |
| F17 (worktree concurrency) | 5 | Per-cycle isolated worktree. |
| F21 (context exhaustion), F61 (context fragmentation) | 2 | Comprehension stage produces compressed archaeological brief; downstream stages read brief, not raw codebase. |
| F34 (cross-layer drift), F35 (federation-as-family drift) | 6, Patrol | Cross-model reviewer checks against architecture-level invariants from archaeological brief; Patrol watches across cycles. |
| F36 (instruction ceiling), F37 (contradictory prompt) | 3, 6 | Stage-3 intent capture caps simultaneous requirements; stage-6 reviewer is one place contradiction surfaces. |
| F38 (vocab lint), F39 (point-spec/region mismatch) | 3 | Deterministic GtWR R7/R8/R9 lint on the change-intent block; complexity-diagnosis field on the change-intent block. |
| F40 (last-mile drift) | 8 | Ship stage is a named obligation, not an emergent property. |
| F41 (under-defined intent) | 3 | Stage-3 is structurally an intent-capture stage; cycle refuses to advance without it. |
| F42 (cognitive escrow) | 8 | Re-entry surface designed (PR body bundles change-intent + brief + trajectory pointer + failed line). |
| F43 (RSI board visibility), F58 (runtime/design-time split) | Patrol | Patrol produces structured board-visibility reports; per-cycle metadata feeds runtime compliance. |
| F45 (language-as-harness) | informational | Brownfield language is fixed; this F-mode is known-cost, not mitigated. |
| F48, F49 (collusion / discussion-as-amplification) | 4, 6 | Stage-4 multi-plan generation uses cross-family models when work-unit-class is in `multi-agent-sensitive` regime. |
| F51 (Ashby-deficient guard) | 7 | Stage-7 perimeter is deterministic + scenarios-from-codebase, not LLM-judge-only. |
| F52 (tempting-wrong-hybrid) | architectural | Cycle does NOT accrete deterministic wrappers around LLM stages; deterministic checks live ONLY at stage 7 perimeter where they belong. |
| F53 (voluntary-discipline fragility) | architectural | All stage obligations are substrate-enforced, not operator-voluntary. The cycle refuses to advance, not the operator refusing-to-skip. |
| F54 (goal subversion across cycles) | Patrol + 3 | Stage-3 change-intent is per-cycle (no accumulating goal); Patrol watches for cross-cycle objective drift in change-intent rationales. |
| F55 (behavioural drift / self-reference) | 6 | Cross-model reviewer breaks self-reference; brownfield's codebase grounding helps too. |
| F56 (Replit-class stress bypass) | 8 + watchdog | Stage-8 escalation triggers include detected attempt to bypass code-freeze or other operator-instruction guardrails. |
| F57 (design-authority erosion) | Patrol + 1 | Patrol watches for classification drift; stage-1 classification is itself audited. |
| F59 (premature decomposition) | 4 | Stage-4 explicitly decomposes only to the point intent-stability permits; cycle may loop 2-4 before committing. |
| F60 (parallel-cycle compounding) | architectural | Per-cycle aggregate error rate is the cycle's measurement primitive; parallelism caps are work-unit-class regime parameters. |

## §3 Citations and grounding

Load-bearing claims map to corpus material:

- Cycle-as-architecture grounded in: report [`03`](../../research/03-every-compound-engineering.md) Compound Engineering loop; report [`35`](../../research/35-lenny-howiai-spec-driven-and-team-ops.md) Notion Boxy comment-to-PR loop; report [`34`](../../research/34-lenny-howiai-personal-harnesses.md) Ralph loop; report [`22`](../../research/22-academic-foundations.md) SWE-bench nutshell-bench diagram (`Issue + Codebase → LM → PR → Tests`).
- Change-intent block grounded in: report [`14`](../../research/14-el-kaim-book-intent-and-spec-authorship.md) El Kaim 9-field intent block; followup [`05`](../../research/followup/05-klaassen-siblings.md) Klaassen four-clause plan-prompt.
- Comprehension stage grounded in: UC4 ([`constraints-extracted`](../constraints-extracted.md)); CTR-G4 (code-as-readable-archaeological-input); CTR-B5 (scenarios-from-codebase inversion).
- Cross-model review grounded in: report [`34`](../../research/34-lenny-howiai-personal-harnesses.md) §6.2 `kevin/carl`; report [`23`](../../research/23-anthropic-engineering-trilogy.md) §3.5 specialized critics; report [`18`](../../research/18-openai-codex-substrate.md) Codex Auto-Review. CTR-D4, CTR-D7, CTR-D8 contest the necessity of cross-family — track takes the necessity side and pre-responds in §7.
- Holdout discipline at stage 7 grounded in: D-4 ([`constraints-extracted`](../constraints-extracted.md) note + [`13-round-2-synthesis`](../../archive/synthesis-v1-v2/13-round-2-synthesis.md) C13); F28 ([`failure-modes-v3`](../failure-modes-v3.md)).
- Watchdog tiers grounded in: D-6 + glossary §0; [`13-round-2-synthesis`](../../archive/synthesis-v1-v2/13-round-2-synthesis.md) C14.
- Patrol-level cross-cycle drift watching grounded in: F34 (followup [`12`](../../research/followup/12-brier-pace-layers.md)), F54 (report [`31`](../../research/31-caremark-rsi-board-exposure.md)), F55 (report [`31`](../../research/31-caremark-rsi-board-exposure.md)), F57 (followup [`10`](../../research/followup/10-governance.md)).
- Stage-7 perimeter (deterministic + scenarios-from-codebase, not LLM-judge-only) grounded in: F51 ([`25`](../../research/25-requirements-engineering-foundations.md) Ashby); CTR-B5 sharpening (StrongDM's "Tokens are the fuel" page already permits codebase-derived scenario equivalents — report [`01`](../../research/01-strongdm-factory.md) §1).
- CaMeL-class boundary at stage 5 grounded in: followup [`08`](../../research/followup/08-security-primitives.md) §3 (77% / 84% ≈ 7-point utility tax — this track accepts the tax for production-adjacent regimes, surfaces it as cost in §7).
- Knowledge typing grounded in: followup [`11`](../../research/followup/11-compound-knowledge.md) four-way classification + `kw:confidence`.
- Work-unit-class polymorphism grounded in: D2 ([`decisions-captured`](../decisions-captured.md)); OQ-B4 (brief §8).
- Production-scissors default-off grounded in: F44 (report [`32`](../../research/32-shapiro-completion-chat-agent-claw.md) §8.2 Shapiro R1-R5).
- Stress-bypass escalation grounded in: F56 (followup [`10`](../../research/followup/10-governance.md) §3 Replit case).
- Brownfield asymmetry F20 grounded in: archived [`00-synthesis`](../../archive/synthesis-v1-v2/00-synthesis.md) §4 (El Kaim).
- CTR-G1, CTR-G2, CTR-G3, CTR-G4 (the brownfield-specific contradictions cluster, [`contradictions`](../contradictions.md) §G) are the primary contradictions this track engages.

## §4 Defaults: accepted vs challenged

| # | Default | Marking | Justification |
|---|---|---|---|
| D-1 | Specs are durable, version-controlled, human-curated artifact | **challenged (partial)** | The cycle's load-bearing durable artifact is the **change-intent block per cycle + the archaeological brief per cycle + the PR + the codebase itself**, not a single global system spec. Per CTR-B2 / CTR-B7 / CTR-F1, brownfield does not require a global spec to be the primary artifact; the codebase IS the durable artifact (Brier pace-layer 1's "code is fashion" framing is **rejected** for brownfield — Willison's low-background-steel framing is preferred). Version-controlled and human-curated still hold for the change-intent block and PR body. |
| D-2 | Scenarios live outside the codebase as a holdout set | **challenged** | Per CTR-B5 + the WEAK-3 sharpening (StrongDM's own "Tokens are the fuel" page lists *incident replays*, *agentic simulation*, *traces* as scenario inputs that are inside or generated from the running system, report [`01`](../../research/01-strongdm-factory.md) §1) and per CTR-G2: brownfield scenarios are **drawn from the codebase, runtime telemetry, and production traces**; the holdout is the *unseen subset*, not the *out-of-tree subset*. Stage-7 enforces holdout-as-unseen, not holdout-as-out-of-tree. |
| D-3 | Agent = Model + Harness | **accepted with justification** | Per-stage agents in this cycle decompose cleanly into model + harness; the cycle as a whole is *not* an agent (it is a methodology), so the formula applies at the per-stage scope where it was minted. Acknowledge CTR-C10's natural-language-register addition as a Phase-5 ADR concern, not a blocker. |
| D-4 | Holdout discipline is substrate-enforced, not methodology-optional | **accepted with justification** | Stage 5 builder agent does not see stage 7 acceptance set; substrate enforces the air-gap. Brownfield re-defines the holdout per D-2 challenge but the discipline of *not letting builder see acceptance* is unchanged. |
| D-5 | Hard cost ceilings are non-optional in CI | **accepted with justification** | Per-cycle budget pre-declared per work-unit-class. CTR-E1's 10× cost variance and CTR-E6's CaMeL ~7-point utility tax are accepted as inputs to ceiling calibration; the ceiling itself is non-optional. |
| D-6 | Tiered watchdog (Daemon / Triage / Patrol) is substrate primitive | **accepted with justification** | All three tiers used: Daemon per-stage, Triage at stages 4/5/6, Patrol across cycles for F34/F54/F55/F57 drift. |
| D-7 | Trajectory capture is cheap and production-tested | **accepted with justification** | The PR body's *trajectory pointer* (stage 8) presumes cheap durable trajectory. OpenHands measurement context applies (report [`11`](../../research/11-openhands-substrate-audit.md) §6). The substrate vendor is open (CTR-C5) but D-7's existence as a substrate primitive is not contested. |

## §5 Cold-start

**N/A for this track.** Cold-start is the load-bearing risk of the *greenfield* mandate (brief §5). Brownfield day-0 input is a pre-existing codebase + issue queue (or the act of creating one against the codebase). Stage 2 (Comprehension) is the brownfield analog of cold-start: the first cycle's archaeological brief covers more of the codebase than subsequent cycles' briefs because the knowledge store is empty.

The brownfield analog to cold-start — *legacy-ingestion* — is named in CTR-G3 as possibly-asymmetric. This track treats legacy-ingestion as **stage-2 cost** (brief is large at first, shrinks as knowledge accumulates) rather than as a meta-stage. If Phase-3 or Phase-4 decide legacy-ingestion deserves equal weight, that would shift this track's stage-2 description to a stage-0/stage-1 split — but the methodology shape survives.

## §6 What this track is NOT trying to be

- **Not a substrate selection.** The track names substrate capabilities at boundaries but does not pick between Gas City, OpenHands, Codex, Anthropic Skills, Overstory, or custom. Phase-5 ADRs make that selection.
- **Not a greenfield architecture.** Stages 2-3 are brownfield-defining; greenfield needs a different shape.
- **Not a unified architecture.** The 3 D1 unified tracks search for cross-mandate primitives; this track is brownfield-only by deliberate construction.
- **Not a methodology-evolution architecture.** OQ-B9 (methodology evolution as substrate primitive vs. per-architecture concern) is deferred. This track's methodology is fixed at run time; evolution is a Phase-7 / operator concern.
- **Not Compound Atelier or Refinery in disguise.** Both are hostable as work-unit-class regime variations on the cycle; neither is the cycle. Phase-7 back-fill will judge.
- **Not a regime classification scheme.** Regime is a stage-7 attribute (acceptance gate strictness), not a separate top-level concept.
- **Not a comprehensive failure-mode coverage analysis.** §2.5 is the load-bearing mapping; Phase-3 adversarial passes will surface gaps.

## §7 Open questions surfaced by this track

1. **Stage compression rules per work-unit-class.** The cycle declares stages compress/expand by class, but the rules are sketched, not specified. Does `regression-fix` truly skip stage 4, or merely collapse it to N=1? Is `codebase-evolution-proposal`'s stage-2-3-4 loop bounded? Phase-3 / Phase-6 task.
2. **Cross-model review necessity under CTR-D7/D8.** Husain/Shankar's "same-model judging is fine when task differs" is empirically anchored and contradicts this track's stage-6 cross-family insistence. The track took the F46 side; the question of whether cross-family is *necessary* or *contingent* is unresolved. Phase-3 adversarial / Phase-5 ADR.
3. **CaMeL utility-tax acceptance criterion.** CTR-E6 surfaces a ~7-point utility tax for CaMeL-class boundaries. This track accepts the tax for production-adjacent regimes — but what counts as production-adjacent is a policy boundary, not a methodology decision. Phase-5 ADR.
4. **Scenarios-from-codebase governance.** D-2 challenge inverts holdout-location but does not specify how the *unseen subset* is selected from a codebase-derived pool without leaking. Phase-3 / Phase-5.
5. **Per-cycle vs. cross-cycle Patrol scope.** The track puts F34/F54/F55/F57 watching at Patrol; is Patrol per-architecture or shared-substrate (OQ-B9 adjacent)? Deferred.
6. **Brownfield regime ceiling (CTR-A5) measurability.** The track claims per-(work-unit-class × stage) Automation-Mode bar clearance contests Jaymin's brownfield ~L3 ceiling. The measurement protocol for this claim is not specified. Phase-8 lean-eval brief task.
7. **Methodology evolution disposition (OQ-B9).** Deferred; if methodology evolution is substrate-primitive, this architecture's cycle definition becomes negotiable per cycle, which is a different architecture.
8. **Anthropic Skills network-closure (CTR-C9) vs. dreaming.** Stage 2 (Comprehension) and Patrol arguably need overnight-research style "dreaming." If the substrate vendor closes network at Skill layer (Anthropic), Comprehension and Patrol need a different substrate vendor or a different mechanism. Phase-5.
9. **Knowledge-curator placement.** This track makes stale-knowledge handling the next reader's obligation, not a curator daemon's. CTR-H2 / CTR-H3 contest this. Phase-3 / Phase-5.
10. **F36 instruction-following ceiling interaction with change-intent.** Stage 3 caps simultaneous requirements per change, but if a change-intent block grows past the F36 ceiling (>10-20 specified requirements), the cycle should refuse rather than degrade silently. Refusal criterion not specified.

*End of brownfield-methodology-first.md.*
