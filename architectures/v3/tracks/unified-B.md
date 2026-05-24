---
track: unified-no-axis-B
axis: pace-layer-x-cognitive-escrow (interval-as-design-site, layered by change-rate)
mandate-scope: unified
based-on-commit: 96a949430b5c356f8b4e688b1d427348a68db468
based-on-date: 2026-05-24
---

# Unified-B — Pace-Layered Escrow Factory

## §0 Axis declaration and defense

**Chosen organizing axis.** **Pace-layer × cognitive-escrow.** The architecture organizes around (a) Brier's pace-layer stack (standards → architecture → spec → plan → code, fastest at the bottom) and (b) Kahana's *cognitive-escrow interval* as the substrate primitive — every transition between pace layers IS an escrow interval that the substrate instruments with structural controls, replacing voluntary discipline (per the F53 *voluntary-discipline fragility* class).

The mandate axis (greenfield/brownfield, UC4's organizing principle) is treated as **an input parameter** to the layered cycle, not its organizing dimension. Greenfield = top-down traversal of layers from a thin upper-layer seed; brownfield = bottom-up *inference* of layers from existing code + telemetry. Same primitives, opposite traversal direction. This is unification at the level of *which surface the factory acts on*, not at the level of *what work it does*.

**Why this axis (defense pre-responding to Phase-3 adversarial).**

1. **The corpus already has the unifier; UC4 just doesn't name it.** Brier's pace-layer model (followup/12; CTR-F1, CTR-B7) is the corpus' only framework that *natively* spans mandate boundaries: standards and architecture as slow layers, code as a fast layer, spec floating in the middle. UC4's distinction (`spec-malleable` vs `code-archaeological`) is a *projection* of pace-layer differences — greenfield has fast-moving upper layers and brownfield has slow-moving ones, but the *layers themselves* are the same artifacts.
2. **Kahana's escrow primitive natively spans mandates.** F42, F53, and the AILCCP Human-Centered fourth question (`30-cognitive-escrow.md` §2) all attach to *interval design* between any two units of attention transfer. This is mandate-agnostic at the primitive level. It is also the closest the corpus has to a *substrate-level antidote to voluntary discipline fragility* — the very class of failure that crushes most proposed mitigations across both mandates.
3. **Anticipated adversarial #1 — "Pace layers are a metaphor, not an architecture."** Counter: pace layers are operationalizable as a *typed-object hierarchy* (cf. El Kaim Ch 8 typed objects, CTR-B6) where each layer carries explicit `change-rate` and `escrow-policy` fields. Brier himself (followup/12) anchors them to ARCHITECTURE.md invariants, which is concrete enough to enforce in CI.
4. **Anticipated adversarial #2 — "Greenfield has no slow layers, so the layered model is degenerate at cold-start."** Counter: §5 below — at cold-start, the slow layers are *seeded* from priors (adjacent-domain exemplars, standards, AILCCP control catalog, INCOSE GtWR), not constructed. The layered traversal begins at the *standards* layer, not at code; cold-start is precisely the regime where the layered model bites *hardest* because the empty-codebase fallback (read the code) is unavailable.
5. **Anticipated adversarial #3 — "This is just Refinery renamed."** Counter: Refinery is spec-primary (CTR-B3 contradicted by Brier spec-third). Unified-B is *layer-primary*, with spec as one layer among five and explicit demotion of spec-as-primary in line with Brier. The escrow primitive is also novel relative to Refinery (Refinery has no interval-design layer).
6. **Anticipated adversarial #4 — "This dissolves UC4 by fiat."** Counter: explicit in §6 — Unified-B does not claim UC4 is false; it claims UC4's *phenomena* (spec-malleability vs code-archaeology) emerge as derived properties of layer-traversal direction in a single architecture, falsifying UC4's stronger reading ("we won't find one that works best with both") for *this* domain of applicability. Other architectures (the two other unified tracks; mandate-specific tracks) may still be stronger on their narrower domains.
7. **Convergence-risk preemption (D7 blind-axis discipline).** If A and C both pick a mandate-symmetric substrate axis or a regime-classification axis, B's pace-layer + escrow axis is distinct on both dimensions: it is *artifact-stack-shaped*, not substrate-primitive-shaped or regime-classification-shaped.

---

## §1 Architecture sketch

**Name.** Pace-Layered Escrow Factory (PLEF).

**The five layers (Brier, followup/12, refined).** Each is a typed-object class with its own change-rate, ownership, and escrow-policy:

| Layer | Change-rate | Greenfield source | Brownfield source | Escrow-policy default |
|---|---|---|---|---|
| L0 Standards | months–years | AILCCP 48 controls, INCOSE GtWR, EARS, SB 53 framework | Same + inherited regulatory commitments (F58) | Board-level review; STIR cascade mandatory |
| L1 Architecture | weeks–months | Adjacent-domain exemplars + Pareto sketches | Inferred from codebase via dependency mapping + ADR archaeology | Daemon + Triage + Patrol (C14) on every change |
| L2 Spec | days–weeks | El Kaim 9-field intent block (CTR-B6) | Spec-the-*change* (delta-spec against running system) | EARS-typed; GtWR-linted (F38); contradiction-check (F37) |
| L3 Plan | hours–days | Decomposition agents under spec constraint | Same, but decomposition seed comes from issue queue / production trace | Cost-ceiling gate (D-5); holdout-discipline check (D-4) |
| L4 Code | minutes–hours | Builder agents; sandboxed | Builder agents; production-scissors-default-off (F44) | Worktree isolation (F17); cross-model review (F46); attribution capture (F14) |

**The escrow primitive (substrate-level).** Every transition `Lᵢ → Lᵢ₊₁` and every output-return from a builder agent is wrapped in an *escrow interval* that the substrate instruments with:

- A **reflection question** (templated to the layer transition).
- A **success-criterion articulation** field (operator-typed during the interval).
- A **similar-past-transition surfacing** (knowledge-store lookup, F8/F55 mitigated by curation).
- A **delegation-level confirmation** (per AILCCP L1/L2/L3/L4 classification).
- A **STIR cascade** when the operator's per-cycle escrow burden exceeds a configured threshold (`30-cognitive-escrow.md` §4 primitive catalogue, items 1–6).

The escrow primitive is the **structural replacement for voluntary discipline** (F53). It fires at the substrate's natural moment (interval-by-construction) regardless of operator cognitive budget.

**Same primitives, opposite traversal.**

- **Greenfield cycle.** L0 (seed standards) → L1 (sketch architecture from priors) → L2 (intent block) → L3 (plan) → L4 (code) → upward re-evaluation of L1/L2 against L4 surprises. The spec is malleable *because* upper layers seed from priors that are themselves provisional.
- **Brownfield cycle.** L4 (existing code) → L3 (inferred plan via trace analysis) → L2 (inferred delta-spec) → L1 (inferred existing architecture) → L0 (inherited standards) → downward *change* traversal against the inferred upper stack. The architecture is `given` *because* the inference step pins L1 before any new work fires at L4.

**Knowledge store.** A single CXDB-or-equivalent event log + curated `docs/solutions/`-style summaries (CTR-H2 split resolved by carrying both: events lazily, summaries eagerly with cadence-controlled refresh per CTR-H3). Each entry tagged with the layer it pertains to, so the escrow primitive can surface layer-appropriate prior work.

**Coordination medium.** GitHub issues + PR comments (CTR-C7 resolution: CI-friendly, not mail-bus). Each layer transition produces a durable artifact (typed object) committed to the repo; the layer's git history IS the layer's audit trail (cf. Nystrom spec-history-as-changelog, CTR-B7, generalized to all five layers).

**Provider abstraction.** Per-layer model routing, not per-call (CTR-C4 partial resolution): L0/L1 prefer long-context + diverse model families; L4 prefers provider-aligned coding agents (Attractor's `do not unify` discipline). This is neither pure RouterLLM nor pure Attractor — it is *layer-aware* routing, with provider-property requirements declared per layer (OQ-B8).

**Watchdog.** Tiered Daemon/Triage/Patrol (D-6) per layer; Patrol's strategic-drift detection runs against pace-layer invariants (F34 cross-layer drift is the primary signal Patrol watches for).

---

## §2 How this addresses each load-bearing concern

### §2.1 Lights-out / L5 tension (brief §2.1, OQ-B1, CTR-A1/A4/H10)

**Vocabulary mapping (CTR-A4 test first).** Unified-B treats "lights-out" as **L4 per layer, escalating to human at layer-transition escrow intervals**. This is the brief's option (c) + (b): regime classification per layer + lights-out defined over the work-unit surface (per-cycle code-layer work; per-layer-transition human re-entry).

- **L4 (code) cycles are L4-Automation** in Jaymin's frame: builder agents run autonomously; cross-model review (F46 mitigation) provides the judge-independence the L4 bar wants; cost ceilings (D-5) and watchdog (D-6) cap blast radius. K=5 ≥90% and prompt-paraphrase 5/5 bars apply *per-task* at L4, measurable.
- **L0–L3 transitions are L3-Augmentation** with structural escrow (not voluntary). The operator re-enters at every transition, but the escrow primitive lowers per-interval evaluation cost (success-criterion articulation, similar-past surfacing).
- **L5 ("no human ever") is rejected** as Jaymin's empirical-anti-pattern claim (CTR-A1) reads on it; PLEF never operates at L5 because every layer transition has a structural escrow checkpoint.

This dissolves CTR-H10 via the WEAK-4 sharpening: the Round-2 ceiling claim is *L5-anti*, not *L3-only*; PLEF's L4-at-the-code-layer is compatible.

**Empirical bars (OQ-B6).** Adopt Jaymin's thresholds *at the code layer* (where they were measured); declare layer-transition thresholds as a separate open question (PLEF surfaces this; doesn't resolve it).

### §2.2 UC4 working hypothesis (CTR-C2, CTR-G1, CTR-B6)

PLEF is the explicit falsifier candidate for UC4's stronger reading. Mechanism:

- Spec-malleability (greenfield) and existing-architecture-as-given (brownfield) are **layer-traversal-direction artifacts**, not architecture-shape differences. The architecture (PLEF) is the same; the *direction* of layer traversal flips.
- This addresses CTR-B6 (El Kaim intent block requires upstream stability vs UC4 malleability): PLEF's L0 (standards) layer is upstream-stable in both directions; L2 (spec) is malleable in greenfield direction and inferred-then-fixed in brownfield direction; UC4 and El Kaim are both right at different layers.
- CTR-G1 (corpus admits brownfield asymmetry but designs as if it doesn't): PLEF's brownfield direction is constitutive, not retrofitted — the L4→L0 inference is a first-class cycle shape, not a special case.

### §2.3 Cold-start (mandatory per §5; previewed here)

The pace-layer model is *strongest* at cold-start because the architecture is forced to seed from priors at L0/L1 rather than reading code. See §5 for full treatment. Required reading per brief §5.1: reports 25, 26, 30, 31, followup/10 — all five are directly load-bearing for the L0–L2 seeding discipline.

### §2.4 OQ treatment (selected)

- **OQ-B2 (boundary at substrate vs methodology).** PLEF places the *escrow primitive* and *layer-typed-object schemas* at substrate; *traversal direction* and *per-layer agent populations* at methodology. The boundary is per-layer: substrate provides the typed-object class + escrow wrapper; methodology fills the layer's content.
- **OQ-B3 (human re-entry mechanism).** Re-entry is *structural*: every layer transition is an escrow interval; the substrate-level protocol is the AILCCP delegation-level confirmation primitive (`30-cognitive-escrow.md` §4 primitive 4). Conditions for hand-back: layer-transition trigger; Patrol-detected cross-layer drift (F34); cost-ceiling hit (D-5); watchdog escalation (D-6).
- **OQ-B4 (brownfield unit of work).** All three (issue / change-against-spec / codebase-evolution-proposal) map to delta-specs at L2; PLEF doesn't pick one. The methodology layer above PLEF picks.
- **OQ-B7 (alternative organizing axes).** PLEF surfaces *change-rate* (pace) and *interval-design* as load-bearing axes that the brief's mandate-axis subordinates. Phase-3 should weigh.
- **OQ-B8 (provider-property requirements).** PLEF declares per-layer requirements: L0/L1 = long-context + diversity; L2/L3 = contradiction-detection capability (F37); L4 = provider-aligned coding agents. RouterLLM-equivalent at L4 only.
- **OQ-B9 (methodology evolution).** Per-architecture concern in PLEF (each layer's methodology evolves independently); substrate provides the typed-object versioning.
- **OQ-B10.** Acknowledged as process discipline; PLEF's typed-object hierarchy makes back-fill mechanical (each archive item maps to a layer).

### §2.5 Key failure-mode coverage (greenfield/brownfield severity-aware)

- **F1/F27/F46/F48 (correlated-error cluster).** Cross-model review at L4 (F46 mitigation); L2-layer contradiction-detection between independently-drafted spec versions (F37); layer-transition escrow surfaces shared-prior risks before composition.
- **F12/F33/F44 cascade.** F44's substrate-default production-scissors-off enforced at L4; L0 standards include AILCCP Sensitive-Action Approval Gate; L3 plan-layer holdout discipline (D-4) prevents trifecta-composition emergence.
- **F34 (cross-layer drift).** Patrol watchdog's primary signal; pace-layer model makes it *natively detectable* because each layer's invariants are explicit typed-object fields.
- **F36/F37/F38/F39 (spec quality).** L2 layer is EARS-typed + GtWR-linted at the substrate level (F38 deterministic); F36 instruction-following ceiling addressed by L3 chunking (plan-layer decomposition keeps simultaneous-requirement load below threshold); F37 contradiction-detection is an L2→L3 transition escrow check.
- **F42/F53.** *Constitutive* — the escrow primitive IS the F42 mitigation; the structural-not-voluntary discipline IS the F53 mitigation.
- **F54/F55 (RSI goal-subversion / behavioural drift).** L0 standards include Kahana's three-part RSI test; layer-transition audit trail satisfies Caremark prong-1 (board-reportable RSI status, F43); behavioural-drift mitigated by L0-anchored grounding (standards never self-modify within a cycle).
- **F58 (runtime/design-time compliance split).** Layer-typed objects carry compliance-regime tags; design-time L0 and runtime L4 events both audit-trail into the same store.
- **F59 (premature decomposition).** PLEF allows L2→L3 traversal to *defer* (escrow checkpoint surfaces "is decomposition discoverable yet?"); not a phase-gate that locks.

---

## §3 Citations and grounding

**Core anchors (corpus, not bias-guard-IDs per discipline at top of contradictions.md):**

- **Brier pace-layers:** followup/12 (entire); ARCHITECTURE.md invariants framing.
- **Kahana cognitive escrow:** report 30 §1–§5; AILCCP fourth-question framing.
- **Kahana RSI / Caremark:** report 31 §1–§4 (three-part RSI test, Marchand mission-critical, Boeing design-choices-disable-monitoring).
- **AILCCP 48 controls + governance:** followup/10 §6a (full Cluster-J drain); BCG five-pillar framework; MacGregor incident anchors.
- **El Kaim 9-field intent block:** report 14 §10–17 + report 24 (product-line variability for F35 cross-layer drift).
- **INCOSE GtWR + EARS + Complexity Primer:** report 25 §2–§4.
- **Yang / Larbi prompt underspecification:** report 26 §2 + §6 (F36/F37 anchors).
- **Nystrom spec-history-as-changelog:** report 35 §2–§3 (generalized to all five layers).
- **Schillace Letter 11 Tempting-Wrong-Hybrid (F52):** report 28 §6 — direct pre-response to "you've just built a tempting wrong hybrid"; PLEF's escrow primitive is *not* a deterministic wrapper around an LLM, it is a structured-attention surface *for the human* during the LLM's interval — categorically distinct from F52's failure mode.
- **OpenHands V1 trajectory-capture cost:** report 11 §4–§6 (D-7 anchor).
- **Anthropic five-critic auto-review:** report 23 §3.5 (CTR-D4 third-position; PLEF uses this at L4 same-model-different-role).
- **Husain/Shankar same-model judge:** followup/07 §3.6 (CTR-D7/D8; PLEF uses same-model for layer-transition checks where the judging task is different from the work task).

**Contradictions directly engaged:**

- **CTR-F1** (factory vs company metaphor — Brier-vs-StrongDM): PLEF adopts neither; uses Brier's *pace-layer* framework without his metaphor-swap claim. The artifact is still a "factory" per UC1 nomenclature.
- **CTR-B3 / CTR-B7** (spec-primary vs spec-third; spec-velocity): resolved by treating spec as L2 of 5 with explicit change-rate; Nystrom's spec-git-history extends to all layers.
- **CTR-C2** (substrate-heavy vs methodology-dominates): PLEF takes neither pole; per-layer split.
- **CTR-A1/A4/H10** (L5 cluster): addressed in §2.1.
- **CTR-G1/G4** (brownfield asymmetry; code-as-opaque vs code-as-archaeological): PLEF's bidirectional traversal makes code both — opaque at L4 *write*, readable at L4→L3 *inference*.
- **CTR-D4/D7/D8** (judge diversity): per-layer policy; same-model-different-role at intra-layer; cross-model at L4 builder review.
- **CTR-H13** (substrate-vendor auto-review): adopted at L4 as the same-model-different-role pattern.

**F-modes constitutively addressed:** F1, F27, F34, F36, F37, F38, F39, F42, F44, F46, F52, F53, F54, F55, F58, F59. (Severity rationale per `failure-modes-v3.md` §7 carries through.)

---

## §4 §4 defaults: accepted vs challenged

- **D-1 (Spec is durable, version-controlled, human-curated).** **Accepted with justification** — but reframed: *every layer's typed object* is durable + version-controlled + curated; spec (L2) is one such artifact. The default holds; PLEF generalizes it. (Nystrom report 35; CTR-B7.)
- **D-2 (Scenarios live outside the codebase as holdout).** **Challenged.** PLEF carries scenarios at *layer-appropriate* locations: greenfield scenarios live in L2/L3 (outside codebase, holdout-disciplined per D-4); brownfield scenarios live partly in L4 (production traces, existing tests) + partly outside (delta-spec scenarios). The fragile-default flag in the brief is right; PLEF resolves by layering rather than enforcing a single location. Citation: CTR-B5 + WEAK-3 (StrongDM's own primary practice already permits scenario-equivalents inside the running system; D-2 oversimplifies its source).
- **D-3 (Agent = Model + Harness).** **Challenged.** PLEF agents at different layers have different shapes: L0/L1 agents are *populations* (drafting against priors), L2 agents are *persona-panels* (intent vs invariant vs non-goal critics), L3/L4 agents fit Model+Harness. Round-2 C10 holds at L4; degrades upward. Also: CTR-C10 (report 37 Portuguese-vs-English) means even at L4, `Agent = Model + Harness + Natural-Language-Register`; PLEF's L2 typed-object schema includes a `natural-language-register` field.
- **D-4 (Holdout discipline substrate-enforced).** **Accepted with justification** — substrate enforces per-layer; L3 plan-layer holdout from L4 builders is the primary instance.
- **D-5 (Hard cost ceilings non-optional in CI).** **Accepted with justification** — declared per layer. CTR-E1 unresolved variance (Cherny $100K vs $500–5000/day) means per-layer ceiling, not flat. CTR-E6 (CaMeL 7-point utility tax) acknowledged — PLEF does not assume substrate-safety is free.
- **D-6 (Tiered watchdog substrate primitive).** **Accepted with justification** — Patrol's primary signal is cross-layer drift (F34), which the pace-layer model makes natively detectable.
- **D-7 (Trajectory capture cheap and production-tested).** **Accepted with justification** — OpenHands V1 numbers (report 11 §6) hold; PLEF event-sources every layer transition + every L4 cycle.

---

## §5 Cold-start (MANDATORY)

**Day-0 question (per brief §5.2):** How does PLEF bootstrap when there are no scenarios, no issue queue, no `docs/solutions/`, no prior runs?

**PLEF's answer: seed L0 and L1 from priors; do not start at L4.**

This is where pace-layer organization pays its largest dividend. A code-first or spec-first cold-start architecture has nothing upstream to anchor on; PLEF's L0 (standards) is *constitutively prior-seeded* and never starts empty.

### 5.1 The seeded layers at t=0

- **L0 Standards (seeded, never empty).**
  - **AILCCP 48 controls catalogue** (`followup/10` §6a.B; Kahana 2026-02-16) — full catalogue installed as L0 typed objects on day 0.
  - **INCOSE GtWR v4 characteristics C1–C15 + 42 rules** (report 25 §3) — installed as the L2 lint rule set.
  - **EARS grammar** (report 25 §2) — installed as the L2 acceptance-criteria DSL.
  - **Caremark three-part RSI test + Marchand mission-critical rubric** (report 31 §1–§2) — installed as the L0 governance-exposure declaration the factory must produce.
  - **SB 53 reporting boundary** (report 31 §3) — installed as L0 conformance-check.
- **L1 Architecture (seeded from adjacent-domain exemplars).**
  - Greenfield (per brief §0 glossary): adjacent-domain exemplar architectures, operator-curated knowledge from prior factory runs (when available), library-ecosystem priors.
  - At true day-0 (no prior runs), L1 is *Pareto-sketched* from L0 standards — the architecture is constrained to satisfy L0 conformance and otherwise open.
- **L2 Spec (seeded from intent block template).**
  - El Kaim 9-field intent block (CTR-B6; report 14) as the empty-spec scaffold. The operator fills the 9 fields *during cold-start escrow intervals* — STIR cascade fires here naturally.

### 5.2 The Yang/Larbi underspecification bars (report 26)

Cold-start is the regime where F36 (instruction-following ceiling) and F37 (silent contradictory-prompt collapse) bite *worst* — the operator's intent is least articulated, the spec is most likely to be contradictory. PLEF responds:

- **F36 mitigation at cold-start.** L3 plan-layer agents chunk the L2 spec into ≤10-requirement units before any L4 builder fires. Substrate enforces the chunk-size; cold-start cannot bypass.
- **F37 mitigation at cold-start.** Every L2→L3 transition triggers a contradiction-detection escrow check; multiple model families run the check independently (Larbi MCC ≤ 0.55 means no single judge is reliable). The cold-start operator sees flagged contradictions before any code is written.

### 5.3 The cognitive-escrow bar at cold-start (report 30)

Cold-start has the highest per-cycle escrow density — the operator is constantly transitioning between empty layers. PLEF's substrate-level escrow primitive (the F42/F53 antidote) provides:

- **Reflection-question surfacing** on every L0→L1, L1→L2, L2→L3 transition (`30-cognitive-escrow.md` §4 primitive 1).
- **Success-criterion articulation** before any builder fires (primitive 2).
- **STIR cascade as default at cold-start** (primitive 6) — the discipline is *substrate-required* at cold-start, *substrate-offered* at steady-state.
- **Delegation-level confirmation** on every cycle (primitive 4) — cold-start defaults all delegations to L2 (review-before-execute) until the factory has audit-trail evidence to justify L3 escalation.

### 5.4 The governance bar at cold-start (report 31, followup/10)

Cold-start is *the* moment to install the Caremark / SB 53 / AILCCP infrastructure correctly. PLEF treats this as a day-0 L0 commitment:

- **Caremark prong-1 satisfaction (board reporting infrastructure).** The factory's L0 typed objects include the board-reportable RSI declaration (per Kahana's three-part test, report 31 §1) and the structured-reporting mechanism (F43 mitigation). Bootstrapping the factory IS bootstrapping its board-reporting surface.
- **AILCCP control instances.** Each of the 48 controls (followup/10 §6a.B) is instantiated as a typed object with `running` / `not-yet-running` / `n/a` status. Cold-start makes the gap visible rather than silent.
- **BCG "auditability by design"** (followup/10 §1.2): PLEF's pace-layered event log *is* the audit trail; cold-start writes the first entry.

### 5.5 Silent-failure protection during bootstrap

The brief asks how cold-start is protected against silent failure (no track record yet to evaluate the architecture). PLEF answer:

- **Layer-invariant checks are deterministic, not LLM-judged.** GtWR linting, EARS conformance, AILCCP control presence — all deterministic. Ashby-deficient probabilistic guards (F51) are avoided at L0/L2 layer boundaries.
- **Watchdog operates from day 0.** Daemon catches process liveness; Triage's AI reclassification is calibrated against L0 standards (not against itself); Patrol's cross-layer drift detection (F34) has L0 anchors to drift *from* on day 0.
- **Two-source seeding.** L0 standards come from two independent sources (e.g., INCOSE + AILCCP for any spec-quality control); divergence is flagged at install time.

### 5.6 Trajectory: day-0 → day-N

- **Day 0–7.** L4 cycles fire only against L0+L1+L2-seeded surfaces; L3 chunks ≤ 5 requirements; STIR mandatory; cross-model L4 review mandatory.
- **Day 7–30.** Knowledge-store accumulates layer-tagged events; escrow-interval "similar-past-transition surfacing" becomes informative; STIR transitions from mandatory to substrate-offered.
- **Day 30+.** Steady-state: per-layer Jaymin thresholds calibrated against measured performance; layer-traversal direction (greenfield top-down vs brownfield bottom-up) optimized; OQ-B6 empirical bars derived from PLEF's own audit trail.

---

## §6 What this track is NOT trying to be

- **Not trying to be the strongest greenfield-only architecture.** Three greenfield tracks exist; one of them will be stronger on the cold-start-first axis or substrate-first axis. PLEF is strong on cold-start *because of pace-layering*, not in spite of it.
- **Not trying to be the strongest brownfield-only architecture.** Three brownfield tracks exist; one will be stronger on legacy-ingestion-first or substrate-first. PLEF's bottom-up traversal is competent at brownfield, not optimal.
- **Not trying to merge with unified-A or unified-C.** The three unified tracks pick different axes deliberately. Phase-3 reconciles. D7 may dispatch an "axis-prohibited" subagent after our convergence is examined.
- **Not trying to resolve UC4 globally.** PLEF falsifies UC4's stronger reading *for the domain where pace-layer + escrow is the natural organizing surface*. Architectures where mandate-difference is itself the load-bearing surface (e.g., regulator-facing brownfield where the regulatory regime IS the architecture) may still split.
- **Not adopting Brier's metaphor-swap.** CTR-F1 ("software company not software factory") is not adopted; PLEF uses Brier's *layering* without his *metaphor reframe*. The artifact remains a factory per UC1 nomenclature.
- **Not claiming the escrow primitive is novel — claiming it is substrate-loadable.** Schillace's Attention Firewall and Anthropic's Sensitive-Action gates are prior art; PLEF's contribution is to elevate the interval to a first-class substrate primitive at *every layer transition*, not just at production-action boundaries.
- **Not picking a substrate stack** (OpenHands vs Gas City, CTR-C5). PLEF is compatible with either; the typed-object hierarchy and escrow primitive are substrate-agnostic. Phase-4 picks.

---

## §7 Open questions surfaced by this track

1. **OQ-PLEF-1 — Layer-count is empirical, not derived.** Brier asserts 5 (standards / architecture / spec / plan / code). El Kaim's typed-object hierarchy implies more (intent / decision / spec / control / feedback as 5 *spec-internal* layers). The right number for a software factory is open; PLEF picks 5 by Brier convention. Could be 3 (standards / spec / code) or 7 (adding ops + sunset). **Phase-4 work.**
2. **OQ-PLEF-2 — Escrow-interval threshold calibration.** When does the substrate transition STIR from mandatory-at-cold-start to offered-at-steady-state? Kahana doesn't say; corpus doesn't measure. Needs a Phase-8 lean-eval to calibrate.
3. **OQ-PLEF-3 — Cross-layer drift detection (F34) at populations.** Patrol detects drift against L0 invariants for a single cycle. At population scale (Tournament-style architectures running multiple PLEF instances in parallel), cross-layer drift could correlate across instances (F48 tacit collusion in layer-traversal). Mitigation unclear.
4. **OQ-PLEF-4 — Layer-traversal direction at hybrid surfaces.** A brownfield system getting a wholly-new greenfield module: which traversal direction? Both? Sequenced? PLEF's primitives accommodate both but the methodology layer must pick. May produce a third traversal direction (parallel top-down + bottom-up converging at L2).
5. **OQ-PLEF-5 — Voluntary-discipline-fragility (F53) at the operator's escrow-interval response.** PLEF moves discipline from operator-voluntary to substrate-triggered, but the *operator's response* to the escrow primitive (do they actually read the reflection question? articulate the success criterion?) is itself voluntary. F53 may have a stronger reading than PLEF addresses. **Phase-3 adversarial should challenge this.**
6. **OQ-PLEF-6 — RouterLLM-equivalent at the layer level, not the call level.** PLEF declares per-layer provider-property requirements; OQ-B8's right level of abstraction is therefore *per-layer routing*, not per-call. Whether this generalizes to other architectures is open.
7. **OQ-PLEF-7 — Same-model-different-role at non-code layers.** Anthropic's five-critic Auto-Review (CTR-H13 / WEAK-5 sharpening) works at L4. Does the pattern extend to L2 (spec-critic personas) and L1 (architecture-critic personas)? PLEF assumes yes; corpus doesn't confirm.
8. **OQ-PLEF-8 — Pace-layer model's own anti-pattern (F52 Tempting-Wrong-Hybrid).** Layering is itself a deterministic structure imposed around stochastic agents. Does the multi-layer escrow stack become an F52 instance — a wrong hybrid that pays the cost of structure without the benefits of either pure-LLM or pure-deterministic? PLEF's defense is that escrow surfaces are *human-attention surfaces*, not deterministic LLM-wrappers, but adversarial review should test this.

---

*End of unified-B.md.*
