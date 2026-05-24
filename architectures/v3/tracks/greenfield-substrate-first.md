---
track: greenfield-substrate-first
axis: substrate-first
mandate-scope: greenfield
based-on-commit: 96a949430b5c356f8b4e688b1d427348a68db468
based-on-date: 2026-05-24
---

# Track: greenfield-substrate-first

## §0 Axis declaration and defense

**Axis (verbatim from the dispatch).** Substrate is the primary organizing principle. Start from substrate primitives (sandbox, scenario storage, trajectory capture, cost ceilings, watchdog tiers, judge routing, coordination medium, guard mediator) and derive methodology as the minimum process needed to use them. The "how" is upstream of the "what."

**Why substrate-first is the right axis for greenfield specifically.** Greenfield's defining property under [UC4](../constraints-extracted.md#uc4) is **spec-malleability**: the architecture moves while the spec is being discovered. A methodology-first design picks a unit-of-work shape early (issue / change-request / candidate) and freezes the loop around it; the malleable spec then has to dance to the methodology's tune. A substrate-first design inverts that ordering: it commits to primitives whose semantics are *spec-shape-agnostic* (a sandbox is a sandbox whether the spec is one sentence or twenty pages; trajectory capture records the cycle whether the cycle's purpose is invention, refinement, or regression-fix), and lets methodology be the *thinnest possible* layer that drives the primitives. Whatever methodology a cycle adopts (Compound-style review panel, Attractor-style DOT pipeline, Tournament-style population selection — per [CTR-F3](../contradictions.md)'s Round-2 reframing of these as methodology choices on a both-shapes substrate), the *substrate is the same*; the spec can churn arbitrarily without invalidating the primitive set.

This axis also pre-respondes to two of greenfield's load-bearing failure modes. **F59 (premature decomposition)** names "scout-spec-build separates exploration from implementation, but the right design is usually discovered *during* implementation" ([failure-modes §5a F59](../failure-modes-v3.md)) — a methodology-first design at greenfield cold-start *cannot avoid* committing to a decomposition before the spec is discoverable. A substrate-first design defers decomposition: the only commitments made on day 0 are to primitive semantics. **F9 (spec overfitting)** is structurally accelerated by methodology-first design because the methodology's loop shape *is* the implicit spec that the LLM's outputs catch up to ([failure-modes §1 F9](../failure-modes-v3.md)). Substrate-first does not eliminate F9 but does not amplify it.

**Pre-response to Phase-3 adversarial axes I anticipate:**

- *"Substrate-first is what Round-2 already converged on and v3 was supposed to test from scratch (per [CTR-H9](../contradictions.md))."* True that Round-2 ended in substrate-heavy + thin-methodology. This track does **not** inherit Round-2's particular substrate list ([CTR-C5](../contradictions.md) is open: OpenHands+Overstory vs. Gas City; this track adopts neither stack normatively). What it inherits is the *axis-ordering* claim, which is defensible against [CTR-C2](../contradictions.md) only by demonstrating that the greenfield primitives below are spec-shape-agnostic — not by deferring to Round-2.
- *"Substrate-first hides where the actual greenfield difficulty lives (intent capture, EARS-discipline, INCOSE GtWR lint) — that's all methodology and the substrate-first frame demotes it."* This track absorbs the [report 25](../../../research/25-requirements-engineering-foundations.md) GtWR R7/R8/R9/R26/R35 deterministic lint set and the [report 26](../../../research/26-prompt-underspecification-academic.md) Yang/Larbi findings into substrate primitives (the spec lint pass is a substrate primitive, not a methodology one; see §1.S8). The intent-discipline that methodology-first treats as the load-bearing artifact, this track treats as a substrate-enforced precondition for entry into the cycle loop.
- *"You haven't addressed [CTR-A4](../contradictions.md) — lights-out vs L5 mapping — at the substrate layer."* See §2.A. Short version: this track adopts brief §2.1 option (c)+(b): regime-classification scheme where the substrate's eligibility-classifier names per-work-unit-class regimes; lights-out applies *only* to work units the classifier rates automation-eligible per substrate-enforced thresholds. Mapping to Shapiro's L4 vs L5 is then a methodology declaration on top of substrate.
- *"You've made substrate so thick it eats the spec-malleability that justifies treating greenfield as its own mandate."* The substrate is thick on *invariants* (sandbox shape, trajectory format, cost ceiling enforcement, watchdog tiers, guard mediator) and thin on *spec-shape commitments*. The thick parts are precisely the parts UC4 says do not move during spec refinement (an [F12 lethal-trifecta closure](../failure-modes-v3.md) does not depend on whether the spec is in v0.1 or v5.0). The thin parts are the parts spec-malleability needs to deform.

---

## §1 Architecture sketch

The architecture is a **substrate stack** of nine primitives, each declared at primitive-semantics level (not vendor-binding level). Methodology is then a *thin* set of cycle-driver conventions that compose these primitives. The unit of work is **not** fixed at the architecture level — it is a methodology choice on top of substrate.

### §1.S1 — Sandbox (closure-first; substrate-default-off for production scissors)

- **Semantics.** Each cycle runs inside an isolated execution environment with explicit allow-lists for filesystem, network, and tool access. Substrate-default is **deny-all**; capability grants are per-cycle declarations carried in the cycle's manifest. Production-credentialled scissors ([F44](../failure-modes-v3.md): R1 read-anything-but-only-draft / R2 thumbprint every artifact / R3 do-not-give-production-scissors / R4 isolated env / R5 disconnect-by-default per [Shapiro report 32 §8.2](../../../research/32-shapiro-completion-chat-agent-claw.md)) are substrate-disabled by default in greenfield; an explicit declaration that the cycle requires production access triggers escalation to a separate, more-restricted closure profile.
- **Defense.** Greenfield does not need production access in early cycles by definition (there is no production yet). This makes the substrate-default-off rule cheap to enforce for greenfield specifically and exactly aligned with [Anthropic's API-surface-Skills closure rule](../../../research/23-anthropic-engineering-trilogy.md) (zero network access by runtime fiat) for the bulk of cycle time. [CTR-C9](../contradictions.md) (zero-network closure vs. dreaming) is resolved for greenfield by declaring "dreaming"-class long-running research as a *distinct* capability profile that the substrate gates separately — not by collapsing the closure rule.
- **Citations.** [F12 / F33 / F44 cascade](../failure-modes-v3.md); [report 32 §8.2 R1–R5](../../../research/32-shapiro-completion-chat-agent-claw.md); [followup/08 §3 CaMeL paper-body](../../../research/followup/08-security-primitives.md) (NORMAL/STRICT interpreter modes inform the closure-mode shape).

### §1.S2 — Scenario storage (canonical, holdout-enforced, substrate-typed)

- **Semantics.** Scenarios live as typed objects in a substrate-managed store that builder agents *cannot read* (D-4 holdout discipline as substrate primitive, not methodology-optional). Each scenario carries: (a) prose statement, (b) acceptance-criterion shape declaration (point spec vs. region spec per [F39](../failure-modes-v3.md)), (c) provenance (operator-authored / generated / scaffolded from priors), (d) staleness timestamp, (e) `protects: RULE-ID` linkage to invariants ([report 14](../../../research/14-el-kaim-book-intent-and-spec-authorship.md) `EvaluationSuite` shape).
- **Defense for greenfield-fit.** For greenfield, scenario storage is the **only ground-truth signal** that survives the absence of an existing codebase (per [failure-modes §7 force-1: out-of-distribution ground truth](../failure-modes-v3.md)). The substrate must enforce builder-blindness or [F28 (holdout leakage)](../failure-modes-v3.md) becomes ambient. [CTR-B5](../contradictions.md) (scenarios outside codebase vs. brownfield-inverted) does not bite greenfield: the codebase does not yet exist to inherit from.
- **D-2 status:** **accepted with justification** for greenfield (see §4).

### §1.S3 — Trajectory capture (per-event, sub-ms persist, content-addressed)

- **Semantics.** Every tool call, model invocation, judge call, guard decision, and operator action persists as a content-addressed event before it returns to the caller. Crash-resume = replay from the last persisted event. Cost: per-event sub-ms; per-cycle crash recovery 7.4ms median per [OpenHands V1 measurement context](../../../research/11-openhands-substrate-audit.md) (this report is cited as measurement evidence only per brief §0, not a normative dependency). This is the D-7 default carried forward (accepted; see §4).
- **Why it matters more for greenfield than methodology-first designs admit.** Trajectory-as-substrate enables [F14 forensic-reconstruction widening](../failure-modes-v3.md): when a greenfield architecture changes its own structure mid-flight (UC4 spec-malleability), the trajectory is the only persistent artifact that records *which cycle of which spec-version produced which output*. Without it, the architecture's history rewrites silently as the spec moves. With it, F9 (spec overfitting) and F55 (behavioural drift) become *detectable* via cross-cycle audit even if not preventable.
- **Citations.** [Round-2 C16](../../../archive/synthesis-v1-v2/13-round-2-synthesis.md), [report 11 §6](../../../research/11-openhands-substrate-audit.md), [F14 widened](../failure-modes-v3.md), [F55](../failure-modes-v3.md).

### §1.S4 — Cost ceilings (hard, multi-axis, substrate-enforced)

- **Semantics.** Per-cycle and per-day budgets in three axes: tokens, wall-clock, tool-call-count. Substrate kills the cycle at ceiling — no graceful-degradation-mode (which is a [CTR-E6](../contradictions.md) CaMeL utility-tax-style hidden cost that substrate-first refuses to absorb silently). Ceilings are parameters of the cycle manifest; the substrate enforces, methodology proposes.
- **Greenfield calibration.** Greenfield cycles are exploratory; ceilings should default *higher* than steady-state but should be **declared on cycle entry**, not raised mid-cycle. [CTR-E1](../contradictions.md) (Cherny $100K+/mo vs. independent $500–$5000/day) puts the design centre an order of magnitude apart; the substrate treats both as configurable, not as a baked default.
- **D-5 status:** **accepted with justification** (see §4).

### §1.S5 — Watchdog tiers (Daemon / Triage / Patrol; substrate-resident; required for lights-out)

- **Semantics.** Three tiers per [brief glossary §0](../00-brief-v3.md) and [Round-2 C14](../../../archive/synthesis-v1-v2/13-round-2-synthesis.md):
  - **Daemon** (substrate, seconds cadence): heartbeat, resource caps, liveness — detects process death.
  - **Triage** (substrate-resident AI judge, seconds-to-minutes cadence): "is this agent stalled or thinking?" — detects [F22 (zombie agents) and F23 (stalled-vs-thinking)](../failure-modes-v3.md).
  - **Patrol** (substrate, hours cadence): cross-cycle drift detection — escalates to human. Detects [F55 (behavioural drift)](../failure-modes-v3.md), [F57 (design-authority erosion)](../failure-modes-v3.md), [F8 (stale-knowledge inversion)](../failure-modes-v3.md).
- **Greenfield-specific Patrol scope.** Because greenfield specs are malleable, Patrol must compare *current cycle outputs* against *operator-declared invariants* (substrate-stored, [report 14](../../../research/14-el-kaim-book-intent-and-spec-authorship.md) intent-block-shaped) rather than against historical baselines (which do not exist yet). This is the substrate's resolution of [CTR-B6](../contradictions.md) (El Kaim intent-block stability vs. UC4 spec-malleability): the invariants are the slow layer, the spec around them is the fast layer; Patrol guards the slow layer.
- **D-6 status:** **accepted with justification** (see §4).

### §1.S6 — Judge routing (multi-shape, model-family-tagged, substrate-typed)

- **Semantics.** The substrate exposes a `judge` primitive that callers parameterise with (a) judge type — same-model-different-task vs. cross-model-different-task vs. same-model-different-role; (b) model-family tag (substrate carries the canonical taxonomy); (c) prompt template ID (substrate-stored, content-addressed); (d) holdout-criterion reference (resolves to a scenario the builder did not see). The substrate **does not pick** which judge shape is right — that is methodology — but it makes the choice declared, auditable, and reversible.
- **Why this is substrate, not methodology.** [CTR-D4 / CTR-D7 / CTR-D8](../contradictions.md) split the corpus three ways on whether judge-diversity is necessary, contingent, or counterproductive (Anthropic's single-judge finding vs. CJ Hess kevin/carl cross-model vs. Anthropic's five same-model specialist critics). Methodology-first designs pick a side; substrate-first declares the choice typed and the type checkable, leaving the *which-shape-when* as a per-cycle decision the substrate logs.
- **Resolves.** [CTR-C4](../contradictions.md) (RouterLLM unification vs. Attractor per-provider non-unification) at the substrate level: the substrate primitive is *typed-judge-call*, not *unified-router*; per-provider profiles are a configuration of the primitive, not a competing primitive.

### §1.S7 — Coordination medium (CI-friendly; substrate-resident; no in-memory mail bus)

- **Semantics.** The substrate coordinates cycles through **content-addressed shared filesystem** and **typed event log**, not through in-memory mail buses. Per [Round-2 §5.1](../../../archive/synthesis-v1-v2/13-round-2-synthesis.md), Overstory-style mail-bus does not survive translation to CI-runner environments that share only `git` + GitHub issues/comments. The substrate explicitly chooses the translatable form.
- **Greenfield-specific.** Greenfield cycles may be solo (single agent + single human) or multi-cycle (multiple agents on the same spec); the substrate's coordination medium must work for both without re-architecture. The filesystem + typed-event-log approach scales down (single agent reads the log) and up (multi-agent merge through Refinery-like merge resolver).
- **Resolves.** [CTR-C7](../contradictions.md) (mail bus vs. GitHub-issues-as-coordination) at the substrate layer.

### §1.S8 — Guard mediator (spec-lint + perimeter typing + closure rules)

- **Semantics.** The substrate runs four mandatory guards on every cycle's spec-input *before* the build agent sees it:
  1. **GtWR vocabulary lint** — deterministic check against R7/R8/R9/R26/R35 ([F38](../failure-modes-v3.md), per [report 25 §3.2](../../../research/25-requirements-engineering-foundations.md)). Vague terms ("approximate," "as needed"), escape clauses, open-ended clauses, absolutes, temporal vagueness — substrate-typed, deterministic, runs at zero marginal cost.
  2. **Contradiction-detector** — runs Larbi-style ([report 26 §6.1](../../../research/26-prompt-underspecification-academic.md), MCC ≤ 0.55 acknowledged as ceiling) with multiple judge calls per [F37](../failure-modes-v3.md). Cannot close the gap; substrate logs the residual.
  3. **Requirement-count budgeter** — counts simultaneously-specified requirements; warns if > 10 ([F36](../failure-modes-v3.md) Yang/Llama empirical ceiling). Mandates chunking if exceeded.
  4. **Perimeter typing** — typed-interpreter boundary à la CaMeL ([followup/08 §3](../../../research/followup/08-security-primitives.md)) for any tool call crossing the sandbox boundary. Probabilistic guards ([F33](../failure-modes-v3.md), [F51](../failure-modes-v3.md)) are explicitly *not* trusted as primary closure.
- **Defense against the "Tempting Wrong Hybrid" ([F52](../failure-modes-v3.md)).** The four guards are deterministic where possible; the substrate refuses to accrete *more* control layers around the LLM than the four named primitives. Schillace's warning ("if you find yourself thinking 'just one more patch' to your controller, you have probably fallen into this trap") is read at the substrate-design level: four typed guards, full stop.

### §1.S9 — Eligibility classifier (regime-naming substrate primitive)

- **Semantics.** A substrate-resident classifier that, per work-unit, declares regime: `automation-eligible` (lights-out per UC1) vs. `augmentation-required` (per-cycle human review) vs. `escalate` (operator-must-design-the-work-unit-first). The substrate enforces the regime: an `augmentation-required` unit *cannot bypass* the human-review gate; an `automation-eligible` unit *cannot summon* the human (it can escalate to Patrol, which then summons).
- **Why this is substrate, not policy.** [F57 (design-authority erosion: convenience reclassifies stakes)](../failure-modes-v3.md) is exactly the failure mode where eligibility-classification drifts. If classification is policy, drift is invisible; if classification is substrate-typed, drift is logged. The substrate stores the classifier's parameters as versioned configuration; Patrol monitors classifier-output distribution; reclassification is itself a typed event.
- **Resolves the lights-out / L5 tension** at the substrate layer (see §2.A). The substrate does not *answer* whether the architecture is L4 or L5 — it declares the *per-work-unit regime* and lets methodology + operator policy decide which regimes are eligible.

### Methodology layer (deliberately thin)

The methodology on top of these nine primitives is just enough to drive them. A greenfield cycle is:

1. Operator (or upstream cycle) authors an intent block + scenarios (S2 substrate-typed).
2. Substrate guards (S8) run on the inputs. Failures block the cycle.
3. Eligibility classifier (S9) declares regime.
4. Sandbox (S1) opens with capability profile derived from regime + intent declaration.
5. Build agent runs under watchdog tiers (S5), with trajectory capture (S3) and cost ceilings (S4) substrate-enforced.
6. Judge primitive (S6) runs against holdout (S2) scenarios; methodology declares which judge shape.
7. Coordination medium (S7) writes outputs as content-addressed artifacts + typed events.
8. Patrol (S5 tier-3) audits cross-cycle.

The unit of work, the spec format choice (prose vs. EARS vs. typed-object), the agent topology (single agent vs. panel vs. tournament vs. graph), and the knowledge-accumulation pattern (eager / lazy / typed) are all **methodology choices** the substrate accommodates without privileging.

---

## §2 How this addresses each load-bearing concern

### §2.A — Lights-out / L5 tension (brief §2.1; OQ-B1)

**Vocabulary mapping test.** Per [brief §2.1](../00-brief-v3.md) the first task is testing whether "lights-out" (UC1) and "L5" (Jaymin, [report 09 §2c](../../../research/09-jaymin-book-harnesses-practices-mental-models.md)) map. **This track's stance:** they do *not* map identically. UC1's lights-out is defined ([glossary §0](../00-brief-v3.md)) as "no human in the per-cycle inner loop for work units the factory has classified as automation-eligible" — which is *compatible* with Shapiro's L4 ("I'm here" — operator setting policy and re-entering on triggers per [followup/01](../../../research/followup/01-shapiro-five-levels.md)) for the policy-setting and re-entry layers, and lights-out *within* the automation-eligible surface. This is brief §2.1 option (c)+(b).

**Substrate-level resolution.** The eligibility classifier (S9) is the substrate primitive that makes the (c)+(b) resolution operational. Lights-out applies *only* to the classified-automation-eligible surface; methodology + operator policy controls which work-unit-classes are in that surface. Patrol (S5 tier-3) monitors the classifier itself for drift ([F57](../failure-modes-v3.md)).

**Empirical-bar question (OQ-B6).** This track does **not** adopt Jaymin's K=5 ≥90% / paraphrase-5/5 / zero-medium-or-high-safety thresholds as the substrate-enforced bar; it carries them as one *configurable* threshold set on the eligibility classifier. The substrate enforces *some* bar set declared at deployment; which bar set is a Phase-3 decision per [CTR-E3](../contradictions.md) (CodeRabbit / Veracode / METR applicability gap). [CTR-A4](../contradictions.md) (vocabulary mapping) is treated as decisive: if the mapping does not hold, the Jaymin numbers do not refute UC1 ([CTR-H10](../contradictions.md) sharpening per WEAK-4).

### §2.B — UC4 spec-malleability

**The substrate is spec-shape-agnostic, the invariants are stable.** UC4's "malleable architecture during spec refinement" is accommodated because none of S1–S9 commits to a spec format. The spec can move from prose → EARS → typed-object → DOT graph across cycles; the sandbox shape, trajectory format, watchdog tiers, judge primitive type-signatures, coordination medium semantics, guards, and eligibility classifier do not change. [CTR-B6](../contradictions.md) (El Kaim intent-block vs. UC4 spec-malleability) is the load-bearing tension here; this track resolves it by treating the **intent block as the slow layer** (S5 Patrol guards it) and the spec body around the intent block as the fast layer (substrate accommodates churn). This is consistent with [Brier's pace-layers](../../../research/followup/12-brier-pace-layers.md) and [Nystrom's spec-git-history-as-changelog](../../../research/35-lenny-howiai-spec-driven-and-team-ops.md) ([CTR-B7](../contradictions.md)): the substrate stores the spec under content-addressed versioning (S3 trajectory + S7 coordination), so the spec's git history *is* the changelog by construction.

**[F9 (spec overfitting)](../failure-modes-v3.md) defense.** Methodology-first designs accelerate F9 because the methodology's loop *is* the spec the LLM catches up to. Substrate-first does not (the substrate has no opinion about what counts as good); it instead exposes the spec→artifact divergence in trajectory (S3) and Patrol (S5 tier-3).

**[F59 (premature decomposition)](../failure-modes-v3.md) defense.** No decomposition is committed at substrate level; methodology can revise decomposition arbitrarily without invalidating substrate guarantees. This is the structural defense against F59 that methodology-first designs cannot provide.

### §2.C — Cold-start (greenfield) — see §5 (mandatory)

### §2.D — OQ-B2 (greenfield/brownfield boundary)

This is a Phase-4 question. **This track's contribution:** S1–S9 are explicitly *not* greenfield-specific in their semantics; S2's holdout-discipline and S9's eligibility-classifier are the surfaces most likely to diverge for brownfield (brownfield scenarios may inherit from codebase per [CTR-B5](../contradictions.md); brownfield eligibility-classification is more constrained by inherited regulatory exposure per [F30 / F43](../failure-modes-v3.md)). Track does not resolve.

### §2.E — OQ-B3 (human re-entry)

The substrate-level protocol: Patrol (S5 tier-3) is the *only* substrate-authorised escalation channel into the human inner loop during a lights-out cycle. The eligibility classifier (S9) is the substrate-level admission gate. Re-entry triggers are typed events stored in S7; handing back is a typed event that re-enters the cycle under S9 re-classification.

### §2.F — OQ-B6 (empirical bars)

Substrate stores the bar set as configurable parameters of S9; the architecture does not pre-commit. Jaymin's thresholds, [CodeRabbit / Veracode / METR](../../../research/09-jaymin-book-harnesses-practices-mental-models.md) numbers, [Husain/Shankar](../../../research/followup/07-evals-deepdive.md) judge-alignment bar, and any future bar are all expressible as parameter sets.

### §2.G — OQ-B8 (provider-property requirements)

S6 (judge routing) lifts provider-property declarations to substrate-typed configuration. Architectures declare *required properties* (model-family diversity, long-context, vision); the substrate enforces availability. [CTR-C4](../contradictions.md) (RouterLLM vs. Attractor per-provider non-unification) becomes a config-versus-config choice on a single substrate primitive, not a substrate-vs-substrate choice.

### §2.H — OQ-B9 (methodology evolution as primitive vs. concern)

This track explicitly treats **methodology evolution as a methodology concern**, not a substrate primitive. The substrate does not auto-evolve; methodologies on top of it may (Compound Knowledge / Claw "dreaming" / Schillace "gene transfer"), and the substrate hosts whatever evolution-state those methodologies need (S3 trajectory + S7 typed-event-log). [CTR-C3](../contradictions.md) resolved on the methodology side at the architecture layer.

---

## §3 Citations and grounding

**Contradictions cited:** [CTR-A4](../contradictions.md) (vocabulary mapping — decisive for §2.A), [CTR-B5](../contradictions.md) (scenarios-outside-codebase — accepted-with-justification for greenfield), [CTR-B6](../contradictions.md) (intent stability vs. UC4 — resolved by slow/fast-layer split), [CTR-B7](../contradictions.md) (Brier/Nystrom spec-velocity — substrate accommodates), [CTR-C2](../contradictions.md) (substrate-heavy vs. UC4 different solutions — track defends substrate-heavy for greenfield), [CTR-C3](../contradictions.md) (methodology evolution — resolved methodology-side), [CTR-C4](../contradictions.md) (RouterLLM vs. per-provider — resolved by typed-judge primitive), [CTR-C5](../contradictions.md) (OpenHands+Overstory vs. Gas City — track adopts neither), [CTR-C7](../contradictions.md) (mail bus vs. CI-friendly — track sides CI-friendly), [CTR-C9](../contradictions.md) (Anthropic closure vs. dreaming — distinct capability profiles), [CTR-D4 / D7 / D8](../contradictions.md) (judge-diversity three-way split — typed at substrate, decided at methodology), [CTR-E1](../contradictions.md) (cost ceiling order-of-magnitude — substrate-configurable), [CTR-E3](../contradictions.md) (Jaymin numbers applicability — substrate parametric), [CTR-E6](../contradictions.md) (CaMeL utility tax — no graceful degradation), [CTR-F3](../contradictions.md) (persona vs. graph-node — both-shapes substrate), [CTR-H10](../contradictions.md) (L3 ceiling vs. UC1 — sharpened to L5-anti per WEAK-4).

**Failure modes cited:** [F1 / F27 / F46 / F48 cluster](../failure-modes-v3.md) (judge primitive S6 design responds), [F3 / F13](../failure-modes-v3.md) (spec-completeness — S8 guards do partial mitigation; substrate acknowledges F3 cannot be closed), [F8](../failure-modes-v3.md) (stale knowledge — S5 Patrol), [F9](../failure-modes-v3.md) (spec overfitting — substrate-detectable not preventable), [F12 / F33 / F44](../failure-modes-v3.md) (trifecta cascade — S1 closure-first + S8 perimeter typing), [F14 widened](../failure-modes-v3.md) (forensic reconstruction — S3 trajectory), [F22 / F23](../failure-modes-v3.md) (zombie / stalled — S5 Triage), [F28](../failure-modes-v3.md) (holdout leakage — S2 substrate-enforced builder-blindness), [F34](../failure-modes-v3.md) (cross-layer drift — S5 Patrol), [F36 / F37 / F38 / F39](../failure-modes-v3.md) (S8 guards: lint + contradiction + count budgeter; F39 region-vs-point spec is the S2 shape-declaration field), [F40 (Last-Mile)](../failure-modes-v3.md) (substrate does not solve this; greenfield is most exposed — see §7), [F42](../failure-modes-v3.md) (cognitive escrow — S5 Patrol cadence + S7 typed-event-log give interval-as-design-site primitives per [report 30 §4](../../../research/30-cognitive-escrow.md)), [F43](../failure-modes-v3.md) (RSI board-visibility — S3 + S7 produce auditable record per [report 31](../../../research/31-caremark-rsi-board-exposure.md)), [F51](../failure-modes-v3.md) (Ashby-deficient probabilistic guard — explicit refusal to trust probabilistic guards as primary closure), [F52](../failure-modes-v3.md) (tempting-wrong-hybrid — substrate caps at four named guards), [F53](../failure-modes-v3.md) (voluntary discipline fragility — substrate-triggered controls preferred to operator-discipline), [F54](../failure-modes-v3.md) (goal subversion — S5 Patrol + S3 trajectory + S9 classification), [F55](../failure-modes-v3.md) (behavioural drift — S5 Patrol + S2 holdout integrity), [F56](../failure-modes-v3.md) (guardrail-bypass-under-stress — S1 closure-first + S8 perimeter typing as substrate, not instruction), [F57](../failure-modes-v3.md) (design-authority erosion — S9 substrate-typed eligibility), [F59](../failure-modes-v3.md) (premature decomposition — defense via substrate-first ordering), [F60 / F61](../failure-modes-v3.md) (parallel-cycle compounding + context fragmentation — S7 coordination medium + S3 trajectory aggregation).

**Inventory anchors cited:** [report 11](../../../research/11-openhands-substrate-audit.md) (measurement evidence for S3), [report 14](../../../research/14-el-kaim-book-intent-and-spec-authorship.md) (intent-block shape for S2 + invariants for S5 Patrol), [report 25](../../../research/25-requirements-engineering-foundations.md) (GtWR R7/R8/R9/R26/R35 for S8 lint), [report 26](../../../research/26-prompt-underspecification-academic.md) (Yang req-count ceiling for S8 budgeter; Larbi contradiction detector empirical ceiling), [report 30](../../../research/30-cognitive-escrow.md) (STIR substrate-anchored; interval-as-design-site primitives for S5/S7), [report 31](../../../research/31-caremark-rsi-board-exposure.md) (RSI three-part test + Caremark spine motivate S3 + S9), [followup/08](../../../research/followup/08-security-primitives.md) (CaMeL NORMAL/STRICT informs S1 closure modes + S8 perimeter typing), [followup/10](../../../research/followup/10-governance.md) (AILCCP controls inform S5 Patrol + S9 classifier; Replit / Moltbook incidents motivate S1 + S8), [followup/12](../../../research/followup/12-brier-pace-layers.md) (pace-layers informs slow/fast split in §2.B).

---

## §4 §4 defaults: accepted vs challenged (all 7 marked)

- **D-1 (Specs are the durable, version-controlled, human-curated artifact).** **Accepted with justification.** For greenfield, the spec is the only durable artifact during pre-code cycles; the substrate stores it under content-addressed versioning (S3 + S7). The spec's *malleability* (UC4) is orthogonal to its durability — moving fast does not make it ephemeral, it makes the git history rich (per [CTR-B7](../contradictions.md) / Nystrom). The intent-block within the spec is the slow layer per §2.B.

- **D-2 (Scenarios live outside the codebase as a holdout set).** **Accepted with justification** *for greenfield*. Brief flags fragile-for-brownfield; for greenfield this is structurally the *only* coherent option since there is no codebase to inherit from. S2 substrate-enforces builder-blindness ([F28](../failure-modes-v3.md)). [CTR-B5 WEAK-3 sharpening](../contradictions.md) (StrongDM's own practice already permits inside-codebase scenarios via incident replays / agentic simulation) is acknowledged but does not bite greenfield day-0.

- **D-3 (Agent = Model + Harness).** **Challenged** for the substrate's typed-judge primitive (S6). [CTR-C10 / MISSED-8](../contradictions.md) ([report 37](../../../research/37-academic-llm-agent-collusion.md) Portuguese-vs-English policy-layer effect) suggests "Agent = Model + Harness + Natural-Language-Register" is the more complete decomposition. S6 typed-judge takes prompt-template ID as a first-class parameter precisely because the harness vocabulary is insufficient to express prompt-natural-language as a behaviour-influencing parameter. The substrate primitive *carries* the richer decomposition by typing prompts; the slogan is not load-bearing.

- **D-4 (Holdout discipline is substrate-enforced).** **Accepted with justification.** This is one of the most defensible Round-2 defaults — S2 makes it substrate-typed and S6 (judge routing) checks it. Greenfield is the regime where it matters most (per [F28 severity rationale](../failure-modes-v3.md)).

- **D-5 (Hard cost ceilings non-optional in CI).** **Accepted with justification.** S4 substrate-enforces. Order-of-magnitude variance ([CTR-E1](../contradictions.md)) is configuration; the *non-optional* part survives.

- **D-6 (Tiered watchdog Daemon / Triage / Patrol is substrate primitive).** **Accepted with justification.** S5; with the greenfield-specific Patrol-against-invariants framing in §2.B because there are no historical baselines yet.

- **D-7 (Trajectory capture cheap and production-tested).** **Accepted with justification.** S3. The OpenHands measurement context is cited as evidence-of-feasibility, not as normative dependency per brief §0.

---

## §5 Cold-start (MANDATORY for greenfield)

### §5.1 What priors are available on day 0

Per [glossary §0](../00-brief-v3.md) revision (Skeptic #6): greenfield is "no pre-existing *implementation*," not "no priors." Day-0 priors the substrate can ingest:

1. **Adjacent-domain operator-curated knowledge** — invariants the operator brings from prior factory runs ([report 14](../../../research/14-el-kaim-book-intent-and-spec-authorship.md) intent-block discipline; [followup/11](../../../research/followup/11-compound-knowledge.md) Compound Knowledge typed-learnings).
2. **RE/SE foundational artifacts** — EARS templates, GtWR linter rules, INCOSE Complexity Primer region-vs-point spec shape ([report 25](../../../research/25-requirements-engineering-foundations.md)). These are loadable into S8 (guard mediator) at substrate-bootstrap time and are not project-specific.
3. **Exemplar projects in the domain** — read-only, as scaffolds (per [report 04 / report 23 Skills schema](../../../research/23-anthropic-engineering-trilogy.md)). Scaffold-as-substrate-primitive is contested ([CTR-C6](../contradictions.md) Jaymin-book vs. Jaymin-manifesto; bitter-lesson vs. scaffold-substrate cleavage per WEAK-2); this track sides **scaffold-substrate** for cold-start because the alternative (bitter-lesson: just read the code) requires a code that does not yet exist.
4. **Operator-authored intent block + initial scenario set** — the single bootstrap artifact the operator *must* produce. Substrate refuses to start the cycle without it (S8 guards block).
5. **AILCCP control set** ([followup/10 §A/B/C](../../../research/followup/10-governance.md)) — 48 controls, applied as substrate configuration; [report 31](../../../research/31-caremark-rsi-board-exposure.md) three-part RSI test as substrate-evaluated property of the cycle definition; if RSI-true, additional Caremark-shaped board-visibility controls auto-engage.

### §5.2 The bootstrap protocol

Day 0 of a greenfield factory under substrate-first:

1. **Operator authors intent block** (9-field El Kaim-style; [report 14 §4.1](../../../research/14-el-kaim-book-intent-and-spec-authorship.md)). Substrate-typed; non-goals + invariants required per S8 lint.
2. **Operator authors ≥3 region-shaped scenarios** ([F39](../failure-modes-v3.md) — point specs are the bootstrap anti-pattern). Substrate-typed; stored in S2 holdout.
3. **Substrate runs S8 guards** on the intent + scenarios. Fail-closed: cycle does not start if R7/R8/R9 violations exceed threshold or contradictions detected.
4. **Substrate boots S1 sandbox** with capability profile derived from intent (greenfield default: maximal closure — no production-anything; full-network only if intent declares research / dreaming).
5. **Substrate initialises S3 trajectory** with the intent + scenarios as the bootstrap event (content-addressed).
6. **Substrate sets S4 cost ceilings** from intent declarations + bootstrap defaults (per [CTR-E1](../contradictions.md) lower-bound — greenfield bootstrap is exploratory but ceilinged).
7. **Substrate configures S9 eligibility classifier** with bootstrap parameters: *all* day-0 work units default to `augmentation-required` (per [F25 design starvation](../failure-modes-v3.md) — cold-start IS the design-starvation regime; operator must be in the loop to bootstrap).
8. **First cycle runs**. Methodology declares unit-of-work shape (issue / change-request / first-feature); substrate accommodates.

### §5.3 Day-0 → Day-N trajectory

The factory transitions from `augmentation-required` to `automation-eligible` per work-unit-class as the trajectory accumulates evidence. Three substrate-recorded signals drive the transition:

1. **Scenario set saturation.** When S2 accumulates ≥ N region-spec scenarios with low cross-correlation, the eligibility classifier (S9) can ground its judgements. *N is a configurable parameter; not pre-set.*
2. **Judge stability across model families.** S6 substrate-logs whether same-task / cross-family judge calls agree within tolerance. When the substrate observes stable cross-family agreement on the work-unit-class, the regime can flip per S9.
3. **Patrol absence-of-drift.** S5 tier-3 Patrol's drift-detector reports no [F55](../failure-modes-v3.md) / [F57](../failure-modes-v3.md) signal across W cycles. Substrate-determined; not operator-set.

This is the substrate-first answer to brief §5.2's "when does the factory transition from cold-start to steady-state": the **substrate measures the transition** from trajectory and eligibility-classifier output; the operator does not declare it. The transition is itself a typed event (per S7) and Patrol-auditable (per S5 tier-3).

### §5.4 Cold-start failure modes and substrate-level mitigations

- **[F25 (design starvation)](../failure-modes-v3.md):** mitigated by S9 default-to-augmentation-required for day-0 work units, forcing the operator into the loop until the substrate has trajectory evidence to flip the regime. Substrate refuses to lights-out a cold-start factory.
- **[F36 (instruction-following ceiling) on day-0](../failure-modes-v3.md):** S8 requirement-count budgeter prevents the day-0 spec from exceeding the Yang/Llama 10-20 simultaneous-requirement ceiling; substrate forces chunking.
- **[F39 (point-spec / region-mismatch)](../failure-modes-v3.md):** S2 scenario type-tag forces region-vs-point declaration at authoring time; INCOSE Complexity Primer principle 12 substrate-baked.
- **[F41 (under-defined-intent debt)](../failure-modes-v3.md):** S8 lint on intent block (9-field discipline; non-goals + invariants required).
- **[F54 (goal subversion across cycles)](../failure-modes-v3.md):** S3 trajectory + S5 Patrol cross-cycle audit; goal-frame deltas flagged as typed events.
- **[F55 (behavioural drift)](../failure-modes-v3.md):** S2 maintains an *operator-authored* scenario floor that never gets agent-generated replacements; substrate-enforced lower-bound on ground-truth purity. Acknowledges per [report 31](../../../research/31-caremark-rsi-board-exposure.md) that grounded-in-human-data is a substrate property, not a methodology aspiration.
- **[F43 (RSI board-visibility gap)](../failure-modes-v3.md):** if S9 + S3 detect RSI-three-part-test conditions ([report 31 §1](../../../research/31-caremark-rsi-board-exposure.md): durable self-mod + compounding + limited gating), substrate auto-engages structured board-reporting outputs. Avoids the SolarWinds framing failure mode by treating safety as substrate-typed, not operator-declared business risk.

### §5.5 What cold-start does **not** solve

- The **F40 last-mile drift** ([report 28 §10.1](../../../research/28-schillace-sunday-letters.md), Letter 9) is critical-severity for greenfield and substrate-first does not solve it: the substrate enables many starts and tracks last-mile state, but bridging the "agent-shaped middle vs. manual fit-and-finish tail" requires methodology choices the substrate explicitly does not make. Surfaced in §7.
- The **substrate cannot author the day-0 intent block**. Operator labor is irreducible at bootstrap. STIR-in-the-interval ([report 30 §3](../../../research/30-cognitive-escrow.md)) can be substrate-triggered as a cognitive-escrow primitive but only *after* the operator has authored *something* to reflect on.

---

## §6 What this track is NOT trying to be

- **Not a brownfield design.** S2 holdout discipline accepted-with-justification specifically because the codebase does not yet exist; brownfield will require a different framing of where scenarios live and what the eligibility classifier inherits.
- **Not a unified both-mandates architecture.** This is a greenfield-first track; whether S1–S9 generalise to brownfield is a Phase-4 question. The three no-axis-prescribed tracks have that mandate.
- **Not a vendor binding.** S1–S9 are primitive-semantics-level. Whether they're realised on OpenHands, Gas City, Overstory, or something else is a Phase-5 ADR question. The track refuses [CTR-C5](../contradictions.md)'s either/or framing as premature.
- **Not a complete methodology.** The methodology layer is sketched in §1 ("just enough to drive the primitives") but the unit-of-work shape, agent topology, spec format, and knowledge-accumulation pattern are deliberately left as methodology choices on top.
- **Not a refutation of methodology-first tracks.** This track makes the claim that *for greenfield specifically*, substrate-first ordering is defensible. Methodology-first tracks may produce stronger designs for steady-state greenfield (after cold-start) or for narrower work-unit-classes. The comparison happens at Phase 3.
- **Not a closure on OQ-B7.** The track does not claim mandate is the only correct primary axis; substrate-first is itself an alternative axis. Whether substrate is *the* primary axis or one of N is a Phase-3 question.

---

## §7 Open questions surfaced by this track

1. **What's the minimal viable S2 scenario set size for an eligibility classifier (S9) to flip a work-unit-class regime from `augmentation-required` to `automation-eligible`?** The substrate measures the transition (§5.3) but the threshold parameter is unspecified. Corpus does not give a number; Phase-3 / Phase-8 lean-eval should attempt empirically.

2. **Does the substrate's "four guards full stop" ([F52](../failure-modes-v3.md) defense in S8) hold under the addition of methodology-imposed guards?** A methodology layer could accrete its own controllers around the substrate primitives and reinstate the tempting-wrong-hybrid at a higher layer. Whether substrate can constrain methodology-layer guard-accretion is unclear.

3. **Is S9 (eligibility classifier) itself an LLM-judge primitive — and if so, does the [F51 Ashby-deficient probabilistic guard](../failure-modes-v3.md) critique recurse into the substrate's own self-classification?** This track says "S9 is substrate-typed but its implementation is open"; the recursion of probabilistic-guard critique into the substrate's own regime-classification is unresolved.

4. **What happens when the slow layer (intent block invariants per §2.B) is itself moved by the operator mid-flight?** UC4 spec-malleability technically extends to invariants in some readings. This track makes invariants the slow layer guarded by Patrol; if invariants move, Patrol's reference moves with them, and drift-detection degrades. Substrate-level mitigation unclear.

5. **F40 last-mile drift is critical-severity and substrate-unaddressed.** Methodology must close this; the substrate cannot. Whether *any* substrate-first design can close F40 without smuggling in methodology commitments is the strongest standing critique of the axis.

6. **CTR-C5 (OpenHands+Overstory vs. Gas City) deferral.** This track refuses to bind to either substrate stack; Phase-5 ADRs must pick. Deferring may itself be a track weakness.

7. **The blind-axis test (D7) is owed to this track.** Three greenfield tracks running in parallel, two converging on substrate-first would trigger the D7 standing safeguard. Lead-agent's call.

8. **Day-0 operator labor cost is irreducible at bootstrap (§5.5).** Whether the substrate can *help* the operator author the bootstrap intent + scenarios (e.g., via a scaffolded interview-style cycle that does not yet engage the rest of the substrate) is open. STIR-in-the-interval primitives ([report 30 §4](../../../research/30-cognitive-escrow.md)) are one direction; not specified here.

*End of greenfield-substrate-first.md.*
