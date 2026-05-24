---
based-on-commit: 9a205b6
based-on-date: 2026-05-24
track: greenfield-substrate-first
axis: substrate-first
mandate-scope: greenfield
---

# Phase-2 track: greenfield-substrate-first — *the greenfield factory is whatever survives running on a substrate whose primitives are designed to keep an evolving spec coherent, falsifiable, and reversible*

## §0 — Axis declaration and defense

**Claim.** For a lights-out greenfield factory (UC1 × UC4), substrate is the right *primary* organizing principle because greenfield methodology is *constitutively unstable*. The spec is malleable (UC4), the work-unit class shifts mid-flight (`initial-spec` → `mvp` → `post-mvp-evolution`), the knowledge store starts empty, the scenarios do not yet exist, and the architecture-of-the-target-system is itself a moving artifact of the same cycles producing the code. **Methodology cannot be the load-bearing layer here, because there is no stable methodology to load-bear with.** What remains stable across the regime is the *substrate*: the sandbox the agent runs in, the trajectory store that captures what it did, the typed-intent perimeter that prevents spec-malleability from degrading into spec-drift (F9, F41, F55), the cost ceilings that bound exploration (D-5), the judge-routing layer that prevents the agent's own outputs from becoming its only ground truth (F1/F27/F55), and the cognitive-escrow interval (report 30) that designs the human re-entry surface when watchdog tiers escalate (D-6).

The substrate-first framing has a sharper greenfield-specific defense than the symmetric brownfield case: brownfield has the existing codebase, runtime telemetry, and inherited tests as out-of-distribution signal (failure-modes-v3.md §7, force 1); greenfield does not. **The substrate is the *only* out-of-distribution anchor a greenfield factory can hold onto across the malleable phase.** Methodology overlays come and go cycle-to-cycle; the substrate is the part that does not move.

**Strongest critique against this axis (pre-response).** *"Substrate-first is premature for greenfield because there is nothing yet to substrate — the architecture is still being discovered. A substrate built before the methodology has stabilised will be the wrong substrate, and substrate is the most expensive layer to migrate. Methodology-first is the right framing because the methodology of the spec-malleable phase is itself the artifact under design."* The response: this critique mistakes *substrate-the-built-thing* for *substrate-the-design-discipline*. We are not committing to OpenHands V1 or Gas City or Overstory on day 0 (CTR-C5 is unresolved and not the question this track answers); we are committing to *deriving the methodology from a fixed primitive set that is itself derivable from the failure modes greenfield cannot survive without*. Cold-start in particular (brief §5) requires substrate to exist *before* the first methodology cycle, because the first cycle has no prior cycle's knowledge store to bootstrap from — the substrate must supply the bootstrapping invariants (typed-intent perimeter, holdout discipline, watchdog, sandbox) or the first cycle has nothing to fail safely against. Substrate-first is the only framing that takes the cold-start risk seriously *before* it bites.

## §1 — Architecture sketch

### §1.1 The substrate primitive set (load-bearing for greenfield)

Eight primitives, derived from the F-modes greenfield cannot survive and the CTRs that contest each primitive's shape. Numbered for cross-reference, not ordered by priority.

**S1. Sandbox with default-off production scissors.** Per F44 (Lethal-Trifecta Production-Scissors Default; greenfield severity `high`, brownfield `critical`) and Willison's R3 (report 32 §8.2). The substrate denies network egress, denies write-anywhere, and denies production credentials *by default*; the methodology layer must explicitly request and justify each capability per work-unit. This mitigates F12 (lethal trifecta, greenfield `high`) and F33 (LLM-judge-against-trifecta is probabilistic, greenfield `high`) — *not* by making the agent safer per cycle, but by making the substrate's safety floor independent of the agent's per-cycle behaviour. Greenfield can afford this default because greenfield has no production yet; the substrate-default-off becomes the methodology's privilege-escalation discipline.

**S2. Trajectory capture as event-sourced ground-truth log.** D-7 (accepted; see §4). OpenHands V1 sub-ms per-event persist, 7.4ms median crash recovery across 433 SWE-Bench Verified replays (report 11; CTR-E4 largely resolved). Trajectory captures everything the agent saw and did: prompts, tool calls, tool results, judge scores, watchdog signals. For greenfield, trajectory is load-bearing because it is the *only* artifact that survives the spec-malleable phase intact — when the spec rewrites itself for the third time, the trajectory still records what each prior version of the spec produced. Mitigates F10 (findings disappear into chat, greenfield `high`) and F16 (resume-fidelity decay, greenfield `medium`) at substrate level. The "knowledge accumulation" debate (CTR-H2 Compound eager vs CXDB lazy; CTR-H3 inline-staleness vs batch-refresh) is a *methodology* choice on top of this primitive — both work if the trajectory exists.

**S3. Typed-intent perimeter (the El Kaim 9-field block enforced at the substrate, not the methodology).** This is the load-bearing greenfield primitive and the most contested. Per MISSED-3 (bias-guard `uncomfortable-contradictions-audit.md`) and CTR-B6: El Kaim Ch 3 §4.1 (report 14) prescribes a typed intent block with `invariants` defined as *"Non-negotiable conditions that any valid realization of the intent must preserve"* — explicitly designed as the **stable upstream** anchor against confabulation. UC4 frames greenfield as spec-malleable. **This track accepts that the contradiction is real and resolves it at the substrate layer**: the *intent invariants* are non-negotiable per cycle and require an out-of-band human action to alter (substrate-enforced); the *spec body* (decisions, constraints, design language) remains malleable methodology-layer artifact that can rewrite freely cycle-to-cycle. Greenfield's malleability lives below the invariants and above the trajectory; the invariants are the only fixed point. Mitigates F9 (spec overfitting, greenfield `critical`), F41 (under-defined-intent debt, greenfield `critical`), F38 (vocabulary lint debt, greenfield `high`), F39 (point-spec / region-mismatch, greenfield `critical`), and F55 (behavioural drift via self-reference loop, greenfield `critical`). The El Kaim "intent invariants are stable; spec is malleable" reading is also consistent with Brier's pace-layers framing (followup 12): invariants live at pace-layer 4-5 (architecture/standards); spec body lives at pace-layer 3.

**S4. Holdout-discipline-as-substrate-enforcement (D-4 accepted).** Acceptance criteria are stored in a substrate-managed space the builder agents cannot read; only the judge tier and the human can. Without this, F28 (holdout leakage; greenfield `critical`) is structurally unmitigable — and for greenfield specifically, acceptance criteria are the *only* ground-truth signal the cold-start factory has access to (force 1 of three forces, failure-modes-v3.md §7). Implementation note: the substrate enforces the read-barrier via filesystem perimeter + role-tagged credentials, not via prompt instructions (F49 explicitly falsifies prompt-instruction-as-control).

**S5. Judge routing layer with model-family diversity declared as a per-judge property.** OQ-B8 territory; CTR-C4 (OpenHands `RouterLLM` vs Attractor provider-aligned profiles); CTR-D7/D8 (Anthropic same-model-judge-is-fine vs F46 single-model-review-blindspot vs Tournament model-family-diversity). **This track does not resolve which framing wins** — that is for Phase-3 cross-mandate work — but the substrate must support both: each judge declares its provider/family and its task-shape (per Anthropic's "judge doing a different task than your main pipeline" framing, followup 7 §3.6); the orchestrator can enforce family-diversity for high-stakes work units and same-family for cost/latency where the task differs sufficiently. Mitigates F1 (Hallucination Loop, greenfield `critical`), F27 (circularity, greenfield `critical`), F46 (Single-Model Review Blindspot, greenfield `high`), and F48 (tacit collusion, greenfield `high`).

**S6. Tiered watchdog (Daemon / Triage / Patrol) as substrate primitive — D-6 accepted.** Daemon = mechanical liveness (seconds); Triage = AI reclassification of stalled-vs-thinking (seconds-to-minutes); Patrol = strategic drift detection (hours, escalates to human). Mitigates F22 (zombie agents), F23 (stalled-vs-thinking ambiguity), F54 (goal subversion across RSI cycles, greenfield `high`). Greenfield-specific tuning: the Patrol tier is the substrate's hook into the cognitive-escrow interval (S8) — Patrol escalations are exactly the human re-entry trigger OQ-B3 asks for.

**S7. Hard cost ceilings enforced in CI — D-5 accepted.** Per-cycle and per-work-unit caps; substrate kills runs that exceed budget rather than relying on operator vigilance. Empirical anchor range is contested (CTR-E1: Cherny $100K+/month vs $500–$5000/day; CTR-E6: CaMeL ~7-point utility tax shows substrate-safety has measurable cost). Greenfield needs aggressive ceilings during the spec-malleable phase precisely because the work is exploratory and feedback signals are weak; the substrate enforces the ceiling regardless of whether the methodology-layer judge believes the run is making progress (F22, F23).

**S8. Cognitive-escrow interval primitive (report 30 / Kahana / F42).** The interval between an operator pressing send and the response returning is itself a substrate-designed surface, not dead latency. For greenfield, this primitive is the human re-entry mechanism (OQ-B3) and the meta-failure-mode-class fix for F53 (voluntary-discipline fragility — every voluntary cognitive discipline in the corpus is structurally fragile, per Kahana). The substrate triggers structured re-engagement at three trigger conditions: Patrol-tier escalations (S6); judge-disagreement above a threshold (S5); cost-ceiling approach (S7). The methodology layer cannot opt out of these triggers — they are substrate-enforced. This is the *only* substrate-level fix for F53 in the corpus.

**Substrate primitives I am NOT including, with reason.**

- **AGENTS.md / scaffold discoverability as substrate primitive** — CTR-C6 (bitter-lesson vs scaffold-substrate, sharpened) is unresolved at the corpus level. For greenfield specifically, scaffold contents are themselves a moving artifact (the AGENTS.md changes as the spec changes), so promoting scaffold-discoverability to substrate without resolving CTR-C6 imports too much methodology. Defer to Phase-5 ADR.
- **Coordination medium (mail bus vs GitHub-issues-as-coordination)** — CTR-C7 unresolved; greenfield single-codebase scope per brief §7 makes high-parallelism less load-bearing than for brownfield. The substrate provides *some* coordination primitive (the trajectory store doubles as a low-rate coordination medium); the choice between mail-bus and issue-coordination is methodology-layer.
- **Self-improvement / methodology evolution as substrate vs methodology** — CTR-C3 unresolved; OQ-B9. For greenfield cold-start specifically, treating self-improvement as substrate is *dangerous* (F55 behavioural drift, greenfield `critical`) because a cold-start factory has no out-of-distribution ground truth against which to anchor self-improvement. Greenfield should explicitly *prohibit* substrate-level self-improvement until the factory has crossed cold-start (see §5).

### §1.2 Methodology derived from the substrate

The methodology is the *minimum* process needed to use the eight primitives, no more. Greenfield methodology fits in five gates per cycle, none of which require the methodology to take a position on contested CTRs:

1. **Intent gate** (S3). Cycle begins by reading the typed intent invariants (substrate-fixed). If the proposed work-unit violates an invariant, the substrate rejects the cycle before it begins. This is where the El Kaim discipline lives.
2. **Sandbox gate** (S1). The cycle declares its required capabilities (network? write? prod creds?); the substrate denies anything not justified. Greenfield's default is "nothing" — every capability is explicit.
3. **Work** — the agent runs in its sandbox with its declared capabilities. Trajectory (S2) records everything. Cost ceiling (S7) bounds the run.
4. **Judge gate** (S5 + S4). Output is evaluated against substrate-held holdout criteria by routed judges with declared model-family. Judge disagreement above threshold triggers cognitive-escrow (S8).
5. **Patrol post-cycle** (S6). Daemon/Triage ran during the cycle; Patrol reviews aggregate drift across the last N cycles, escalates to human via cognitive-escrow if drift detected. Trajectory is appended to.

This is deliberately thin. The "what is the work unit" question (OQ-B4) is a methodology choice not a substrate one: the substrate accepts any work unit shape that can declare its capabilities (S1), invariants-satisfied (S3), and acceptance criteria (S4). Initial-spec, mvp, post-mvp-evolution, and regression-fix all fit. For greenfield in cold-start (§5), the dominant work-unit class is `initial-spec` and the methodology overlay is thinnest; as the factory matures the work-unit mix shifts.

### §1.3 Regime classification (OQ-B1 treatment for this track)

The substrate supports declaring per-work-unit-class regime per D2. For greenfield specifically, the architecture's working regime is **L4 lights-out for sandboxed `initial-spec` and `mvp` work units, with L4-augmented (S8 cognitive-escrow triggered on watchdog Patrol, judge-disagreement, or cost-approach) as the structural human re-entry mode**. This explicitly *rejects* L5 — Shapiro is at L4 by his own statement (CTR-A2); Jaymin's L5-as-anti-pattern claim (CTR-A1) is engaged by the cognitive-escrow primitive (S8) being structurally present rather than absent. The vocabulary mapping (CTR-A4) is treated as: "lights-out" = L4 with substrate-triggered re-entry, *not* L5. This dissolves the apparent CTR-A1 contradiction along the lines the bias-guard WEAK-4 sharpening of CTR-H10 suggests (Round-2's ceiling claim is L5-anti, not L3-only).

The empirical bars (OQ-B6) — Jaymin's K=5 ≥90% Automation Mode threshold — are *measured by the substrate* (trajectory replay = K=5 consistency) rather than asserted by the methodology. This is a deliberate choice: the substrate-first framing means the bars become observable substrate properties, not methodology-author assertions.

### §1.4 Knowledge accumulation

The substrate provides only the trajectory store (S2). Knowledge accumulation patterns (Compound Engineering's `docs/solutions/`, CXDB lazy log, Beads' `discovered-from` edge from report 38) are methodology-layer overlays on the trajectory. For greenfield cold-start, the default knowledge accumulation is *nothing* — no `docs/solutions/`, no skill library, no scaffolds-evolved-by-agents — because F55 (behavioural drift via self-reference) is `critical` until the factory has out-of-distribution ground truth. Knowledge accumulation turns on as a methodology overlay only after the factory crosses the cold-start boundary (§5).

### §1.5 Error handling

The substrate provides four error-handling primitives that compose: sandbox-denial (S1) is the cheapest, kills the cycle before work; cost-ceiling-kill (S7); judge-disagreement-triggered cognitive-escrow (S8); Patrol-tier human escalation (S6). None of these require the agent to behave correctly — they are substrate-side. Methodology-layer error handling (retry, repair, re-spec) sits on top but cannot override the substrate's kills.

### §1.6 Work-unit shape

Substrate-shape-agnostic per §1.2. Greenfield's load-bearing class is `initial-spec`; the per-(architecture × work-unit-class) mandate-fit YAML (D2) for this track:

```yaml
mandate-fit:
  initial-spec: greenfield
  refactor: n/a              # greenfield has no prior code
  mvp: greenfield
  post-mvp-evolution: greenfield
  regression-fix: greenfield
```

## §2 — How this architecture addresses each load-bearing concern

### §2.1 Lights-out / L5 / regime tension (§2.1 of brief, OQ-B1)

Resolved at §1.3. The track's reading: the substrate supports L4-with-substrate-triggered-re-entry; this is what "lights-out" maps to per the glossary §0 definition; this is *not* L5 in Jaymin's sense; Jaymin's CodeRabbit/Veracode/METR refutation (footnoted in brief §2.1, CTR-E3) applies to L5 and does not refute L4-with-re-entry. The substrate-enforced cognitive-escrow primitive (S8) is the structural answer to Jaymin's fragile-discipline critique (F53). This is brief §2.1's option (c) + (b) combined.

### §2.2 UC4 spec-malleable hypothesis

Engaged head-on via MISSED-3. The substrate's typed-intent perimeter (S3) makes intent *invariants* non-negotiable while leaving the spec body malleable. UC4's "spec-malleable" reading is *partly accepted* (the body is malleable) and *partly rejected* (the invariants are not). This is consistent with both UC4's prose (which names a phenomenon, not a structure) and with El Kaim's framework (CTR-B6 resolution). Greenfield cycles can rewrite specs freely below the invariants; invariants drift requires substrate-mediated human action — which means UC4's "reversible commitments" property holds *at the methodology layer*, not *at the substrate layer*. The El Kaim structural-stability claim is **accommodated, not rejected** — the bias-guard's MISSED-3 framing is satisfied.

### §2.3 Cold-start (mandatory; full treatment in §5)

Summary: the eight substrate primitives exist on day 0 *before* any cycle runs. The first cycle's `initial-spec` work-unit is a substrate-supplied bootstrapping ceremony (read brief; author intent invariants with human; author first holdout scenarios with human; substrate-record-everything). The trajectory store starts populating on day 0. Knowledge-accumulation overlays are explicitly OFF until the factory crosses the cold-start boundary. The substrate-first framing is the only one that has day-0 primitives because methodology-first frames have to invent the methodology *before* anything records what they invented — substrate-first has the recording layer already running.

### §2.4 OQ-B2 (greenfield/brownfield substrate vs methodology boundary)

This track's claim: the substrate primitives S1-S8 should be *shared* across mandates; the methodology overlays diverge. Greenfield methodology is thin (5 gates, §1.2); brownfield methodology will be heavier (codebase ingestion, etc., per brownfield tracks). Substrate-sharing is the only design that survives CTR-C2 (substrate-heavy + thin-methodology vs UC4 different-solutions): the methodology can diverge per mandate without forcing substrate divergence. *Not for this track to resolve* — flagged for Phase-4.

### §2.5 OQ-B3 (human re-entry mechanism)

S8 (cognitive-escrow primitive) is the substrate-level protocol. Trigger conditions are substrate-side (Patrol escalation, judge-disagreement, cost-approach); hand-back protocol is via the same trajectory store the agent uses. This is the most opinionated substrate primitive this track promotes, on the grounds that F53 (voluntary-discipline fragility) is otherwise unmitigable.

### §2.6 OQ-B4 — work-unit shape

Substrate-agnostic per §1.6. For greenfield, no commitment between Atelier-issue-from-queue and Refinery-change-against-spec; both fit. The corpus has CTR-H9 (Compound Atelier as baseline contested) and the inventory re-tags report 03 as `brownfield-primary` (queue-of-issues presupposes a system that has issues), which independently supports that greenfield work-unit shape should NOT default to the Atelier model. Likely greenfield default: an intent-driven cycle (initial-spec or mvp) until the factory accumulates issues, then a hybrid.

### §2.7 OQ-B6 — empirical bars

Substrate-measured, not methodology-asserted. Trajectory replay = K=5 consistency measurement; prompt-paraphrase robustness can be a substrate-scheduled re-run. The bars themselves stay Jaymin's (provisional) because the corpus has no better-grounded source, but the framing change is significant: the substrate makes the bars observable.

### §2.8 OQ-B7 — organizing axes beyond mandate

This track's framing (substrate-first) is itself one such axis. The substrate primitive set is largely mandate-agnostic; the regime declaration is per-work-unit-class (D2). Other axes (regime, stakes, synchronicity) are *methodology* layers on top of a shared substrate. Punt to Phase-3.

### §2.9 OQ-B8 — provider-property requirements

S5 (judge routing) declares provider-property as a first-class judge attribute. The RouterLLM vs Attractor-provider-aligned debate (CTR-C4) is *not resolved* at substrate; the substrate exposes both axes (per-call routing + per-judge family declaration); the methodology chooses. Greenfield's default: declare judge model-family for high-stakes work-units; allow same-family for low-stakes.

### §2.10 OQ-B9 — methodology evolution

Per §1.4 + §1.1 (S2 + exclusion from substrate primitives), self-improvement is *methodology-layer, not substrate*. For greenfield specifically, methodology evolution is *off during cold-start* and turned on as an overlay later. CTR-C3 partially resolved in greenfield's favour.

## §3 — Citations and grounding

Every load-bearing claim above cites at least one CTR-ID, F-number, or inventory anchor. Key concentrations:

| Claim | Anchor |
|---|---|
| Substrate is the only stable layer across spec-malleable phase | UC4 + failure-modes-v3.md §7 force 1 |
| S1 sandbox default-off | F44 (greenfield `high`), report 32 §8.2 R3 |
| S2 trajectory capture | D-7, CTR-E4 (resolved), report 11 §6 |
| S3 typed-intent invariants | MISSED-3, CTR-B6, report 14 Ch 3 §4.1, F9/F41/F38/F39/F55 |
| S4 holdout discipline | D-4, F28 (greenfield `critical`) |
| S5 judge routing + family-diversity | CTR-C4, CTR-D7, CTR-D8, F1/F27/F46/F48 |
| S6 tiered watchdog | D-6, F22/F23/F54 |
| S7 cost ceilings | D-5, CTR-E1, CTR-E6 |
| S8 cognitive-escrow | report 30, F42, F53 |
| Knowledge-accumulation OFF in cold-start | F55 (greenfield `critical`), CTR-H2 |
| L4-with-re-entry (not L5) | CTR-A1/A2/A4, bias-guard WEAK-4 sharpening of CTR-H10 |
| UC4 reconciliation via invariants/body split | MISSED-3, CTR-B6, CTR-B2, CTR-B7 |
| Greenfield work-unit default ≠ Atelier | corpus-inventory.md report 03 re-tag (CHALLENGE-6), CTR-H9 |
| Self-improvement off during cold-start | F55, CTR-C3 |

Top three single citations carrying most weight: **MISSED-3 / CTR-B6** (the El Kaim ↔ UC4 collision that the substrate's S3 resolves); **F44 / report 32** (the substrate-default-off-production-scissors discipline); **report 30 / F42 / F53** (cognitive escrow as the substrate-level fix for fragile voluntary discipline, which underwrites the entire L4-with-re-entry framing).

## §4 — Defaults: accepted vs challenged

- **D-1 (Specs are the durable, version-controlled, human-curated artifact).** **Accepted with modification.** The *intent invariants* are durable, version-controlled, human-curated (S3). The spec *body* is malleable. Both are version-controlled (trajectory captures spec versions), but only the invariants are curated per cycle. Citation: MISSED-3, CTR-B6, CTR-B7 (spec-velocity disagreement Brier vs Nystrom — both can hold if we split intent from body).
- **D-2 (Scenarios live outside the codebase as a holdout set).** **Accepted** (S4). Greenfield has no codebase to inherit scenarios from; the brief's fragile-flag is for brownfield, which is not this track's scope.
- **D-3 (Agent = Model + Harness).** **Accepted with caveat.** The substrate-first framing decomposes agents as model + harness; this works for greenfield because greenfield does not require graph-node or population shapes at cold-start. CTR-C10 (Portuguese-vs-English policy-layer drift, report 37) suggests "Agent = Model + Harness + Natural-Language-Register" is the more complete vocabulary; the substrate exposes natural-language-register as a judge-attribute under S5, which sidesteps the D-3 fragility for this track. Tournament-style population architectures would need a different framing; this track does not propose Tournament.
- **D-4 (Holdout discipline is substrate-enforced).** **Accepted** (S4) — this track *strengthens* it: substrate-enforced via filesystem perimeter + role-tagged credentials, not via prompt instructions (F49 rules out prompt-as-control).
- **D-5 (Hard cost ceilings are non-optional in CI).** **Accepted** (S7). The empirical anchor range remains unresolved (CTR-E1, CTR-E6), but the substrate's job is to enforce *whatever* ceiling the operator sets; the value is a per-deployment knob.
- **D-6 (Tiered watchdog).** **Accepted** (S6). Patrol tier is enriched in this track via its hook into S8 (cognitive-escrow), which addresses F53 in a way the original Round-2 framing did not.
- **D-7 (Trajectory capture is cheap and production-tested).** **Accepted** (S2). CTR-E4 largely resolved per the contradictions register itself.

## §5 — Cold-start (MANDATORY for greenfield)

### §5.1 The cold-start problem in this track's framing

A greenfield factory on day 0 has: no scenarios, no issue queue, no `docs/solutions/`, no prior runs, no codebase, no telemetry. **It does have the substrate.** The substrate-first framing is the only Phase-2 axis that takes seriously that day 0 is structurally distinct from day N — because day 0 is when the substrate is *all* there is.

### §5.2 Required-reading integration

**Report 25 (RE/SE foundations).** The substrate's S3 (typed-intent perimeter) is informed by EARS five-pattern grammar (report 25 §2.2) and INCOSE GtWR C1-C15 characteristics (report 25 §3.1). Specifically: cold-start intent invariants must be authored in EARS form (`While… when… the system shall…`) so the substrate can mechanically check well-formedness; the GtWR characteristics C3 (unambiguous), C5 (singular), C7 (verifiable) are substrate-enforced as authoring-gate properties on the invariants block before the first cycle runs. This is the substrate-side implementation of F38 (vocabulary lint debt) mitigation. Report 25's AFIS strategy-3 framing (models-as-spec, also seen in Nystrom/Notion via report 35) is the cold-start authoring discipline: the spec body is Markdown in the repo from cycle 1.

**Report 26 (prompt underspecification academic).** Cold-start authoring is exactly the regime Yang et al. measured (Pass@1 drops 98.7%→85.0% as 1→19 requirements specified) and Larbi et al. measured (GPT-4 Pass@1 73.8%→6.7% on contradictory prompts). The substrate's mitigation: S3's invariants block is capped at a small number (≤10 per the F36 instruction-following-ceiling) and the substrate runs a contradiction-detection pass *between* invariants before accepting them. This is the substrate-side implementation of F37 (silent contradictory-prompt collapse) mitigation. Yang's "underspecification = essential requirements omitted such that multiple valid but inconsistent behaviors remain possible" (report 26 §2.1) is the operational definition that S3's invariants block is shaped against.

**Report 30 (cognitive escrow).** S8 directly imports Kahana's framing. The cold-start operator is *most* exposed to F42 because the cold-start factory has no track record to evaluate it against; the interval between operator-issuing-the-first-bootstrap-intent and the substrate-accepting-it-as-well-formed is exactly the kind of interval Kahana names as un-designed. The substrate's cold-start protocol explicitly surfaces re-engagement questions during this interval ("you've declared invariant X; would invariant Y also need to hold? Does invariant X assume the agent has capability Z?"). This is the substrate-side implementation of Kahana's "fourth question" and the structural fix for F53.

**Report 31 (Caremark RSI board-exposure).** Cold-start is the moment the substrate's logging and reporting infrastructure is committed to; per Kahana's Marchand "mission-critical" framing, if the factory will ever cross into RSI territory (durable self-modification + compounding + limited human gating), the substrate must produce board-readable reporting from day 0. The substrate's S2 (trajectory) + S6 (Patrol) + S8 (cognitive-escrow) compose into a Kahana-compliant audit surface. Implication: the cold-start cycle is *also* the moment the factory's RSI-status declaration is made (per F43, RSI Board-Visibility Gap). Greenfield default: declare non-RSI explicitly, document substrate guards that would have to be relaxed for RSI to apply, refuse to relax them without human-mediated action (S8-triggered).

**Followup 10 (governance).** BCG's "auditability by design" claim (followup 10 §1.2) is operationally achievable because the substrate produces the audit trail as a side-effect of S2/S6/S8; the methodology does not have to do additional work for it. Replit production-database-wipe incident (1,200 executives' data destroyed during code freeze) is the F56 anchor (guardrail-bypass under stress); greenfield cold-start mitigates F56 by having no production scissors to bypass (S1 default-off). AILCCP 48-controls catalogue is the regulator-recognizable shape S6 Patrol reports should produce.

### §5.3 Day 0 → Day N trajectory

**Day 0.** Substrate stands up: sandbox templates (S1), trajectory store (S2), intent-perimeter authoring tool (S3), holdout store (S4), judge registry (S5, populated with at least two model-family entries), watchdog tiers (S6), cost ceilings (S7), cognitive-escrow surface (S8). No agent has run.

**Day 1 (first cycle).** Operator drafts intent invariants via the substrate's authoring tool (EARS-checked, GtWR-checked, contradiction-checked per S3 + report 25/26). Operator drafts first holdout scenarios (≤5; out-of-tree per D-2/S4). Substrate produces well-formedness verdict; operator iterates via cognitive-escrow surface (S8 triggers re-engagement on each authoring decision). Authoring concludes when substrate accepts. First work-unit declared: `initial-spec`. Agent runs in sandbox (S1, capabilities = read-only access to substrate-supplied brief + intent invariants; no network; no write outside sandbox). Trajectory captured. Judge tier evaluates against holdout. Patrol logs cycle aggregate.

**Days 2–N (cold-start phase).** Cycles proceed under thin methodology (§1.2). Knowledge accumulation OFF. Self-improvement OFF. Each cycle's outputs feed into the *next* cycle only as artifacts in the substrate-managed repo, not as scaffold/skill/`docs/solutions/` overlays. The thin methodology is *deliberately monotonous* — substrate-first means the substrate carries the variance, not the methodology.

**Cold-start boundary crossing.** The substrate-measured criteria for declaring cold-start complete:

1. Trajectory store contains ≥ N cycles (suggested N=30, methodology knob).
2. K=5 consistency on the same work-unit ≥ 90% measured by substrate-replay (S2 + Jaymin Automation Mode bar per OQ-B6).
3. Patrol drift detector reports stable for ≥ 14 days.
4. At least one watchdog Patrol escalation has been worked through end-to-end via S8 (operator confirms the human re-entry surface is functional).

When all four are met, methodology overlays may turn on: knowledge accumulation patterns (Compound, CXDB, Beads-style), self-improvement loops (with substrate-enforced ground-truth anchor — *not* fully autonomous), scaffold-evolution. This is when the factory transitions from cold-start to steady-state.

**Day N (steady-state).** Substrate primitives are unchanged. Methodology overlays carry the variance. The substrate is now serving as the audit floor for a factory that has accumulated trajectory, judges, scenarios, intent-invariant version history, and (post-boundary) a knowledge store. New work-unit classes (`post-mvp-evolution`, `regression-fix`) come online. The substrate has not had to migrate, because it was designed to be the stable layer from day 0.

### §5.4 Bootstrap silent-failure protection

Per the brief's §5.2 third question: how does the substrate protect against silent failure when there is no track record yet? Three substrate-side answers:

1. **The substrate's invariants on its own primitives are themselves verifiable** — well-formedness of EARS-formatted invariants (report 25), contradiction-detection (report 26), cost-ceiling-not-exceeded (S7), sandbox-perimeter-not-breached (S1) are all *deterministically checkable* and do not depend on judge quality.
2. **Cold-start cycles run with mandatory cognitive-escrow on every cycle output** (S8 triggers on every cycle, not just on judge-disagreement) until the cold-start boundary is crossed. The operator is functionally augmenting the substrate during cold-start; substrate-first does not mean operator-absent during the regime where substrate alone cannot signal silent failure.
3. **The trajectory store enables replay-once-the-factory-has-track-record** — silent failures on day 5 can be detected on day 35 by re-running day 5's trajectories against day 35's judges and comparing. This is structurally available because the substrate captures trajectory; methodology-first frames lose this option because they do not commit to trajectory until methodology stabilises.

## §6 — What this track is NOT trying to be

This track is **strong on substrate-first axis for greenfield**, not comprehensive. The following are *deliberately* under-treated and rely on sibling tracks:

- **Methodology-first greenfield track.** Will treat the unit-of-work choice (Atelier vs Refinery vs initial-spec-driven) and the per-work-unit gate composition in depth. This track sketches a 5-gate minimum and stops.
- **Cold-start-first greenfield track.** Will treat the day-0 bootstrapping ceremony, operator role, and required operator skill profile in depth. This track sketches §5.3 trajectory and stops.
- **Brownfield tracks (3).** Are not this track's scope. Substrate-sharing between mandates is flagged for Phase-4 (§2.4) but not designed.
- **Unified / both-mandates tracks (3).** The substrate-sharing case (§2.4) is consistent with what a unified track might propose; this track does not pre-empt that work.
- **Phase-4 substrate-vs-methodology boundary.** This track proposes one cut (S1-S8 substrate, everything else methodology) but does not claim it survives cross-mandate scrutiny.
- **Phase-5 substrate ADRs.** This track does not commit to OpenHands V1 vs Gas City vs Overstory (CTR-C5 unresolved); the primitive set is implementation-substrate-agnostic.
- **Architecture count.** This track does not claim it is the only greenfield architecture. The substrate-first framing is one architecture; siblings will propose others.

## §7 — Open questions surfaced by this track

Beyond brief §8:

- **OQ-T1 (substrate-vs-methodology line at the intent perimeter).** §1.1 S3 puts the *invariants* at substrate level and the *body* at methodology level. Is this the right cut, or should the body's syntactic form (Markdown vs typed object) also be substrate-enforced? Report 14 vs report 35 disagree on this (typed object vs Markdown-in-repo); the bias-guard's MISSED-6 (Brier vs Nystrom spec-velocity) is unresolved at the spec-form layer.
- **OQ-T2 (cognitive-escrow trigger calibration).** S8 triggers on Patrol/judge-disagreement/cost-approach. Calibration of each threshold is unspecified and is likely to be the dominant source of F47 (Goodhart-on-Tokens) operator gameability if exposed as a per-operator metric. The substrate's response should perhaps be: never expose S8 trigger frequencies as a per-operator metric.
- **OQ-T3 (cold-start boundary criteria sufficiency).** §5.3's four criteria (N=30 cycles, K=5 ≥90%, 14-day stable drift, one full S8 round-trip) are lead-agent-suggested values, not corpus-derived. Each is a methodology knob; the substrate enforces *some* values for them but does not derive them.
- **OQ-T4 (intent-invariants-as-substrate vs CTR-C2).** This track resolves CTR-C2 (substrate-heavy + thin-methodology vs UC4 different-solutions) in favour of substrate-heavy for greenfield specifically. Whether this resolution survives brownfield (where the codebase itself constrains invariants) is for Phase-3.
- **OQ-T5 (cold-start substrate-instance choice).** The substrate primitives are agnostic to OpenHands V1 vs Gas City vs Overstory vs greenfield-bespoke. But cold-start has a substrate-instance-choice question that steady-state does not: which substrate is cheapest to *deploy* on day 0, given that the operator has no prior experience with any substrate? This may be a load-bearing Phase-5 ADR question.
- **OQ-T6 (Schillace Tempting-Wrong-Hybrid risk for S1-S8).** F52 (Tempting-Wrong-Hybrid; greenfield `high`) names the senior-engineer reflex of wrapping deterministic guards around stochastic LLMs as the most common transition failure. The eight primitives in §1.1 are exactly the kind of substrate-layer accretion that could trigger this critique. The defense: each primitive is justified by a `critical`-severity greenfield F-mode it mitigates and an `accepted` brief default it operationalises, and none of them claims to make the agent itself deterministic. But the critique deserves a Phase-3 adversarial-pass rebuttal.

*End of greenfield-substrate-first.md.*
