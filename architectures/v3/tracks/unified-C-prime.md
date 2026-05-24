---
based-on-commit: 1127c71
based-on-date: 2026-05-24
track: unified-no-axis-C-prime
axis: judge-architecture / verification-topology (the shape and independence of the judge ensemble that closes the per-cycle V&V loop)
mandate-scope: both
prior-track-superseded: unified-C
---

# Unified architecture — track C-prime: **Judge-Topology Factory** (axis: verification-topology)

## §0 — Axis declaration, prohibition acknowledgment, defense, pre-response, glossary

### 0.1 Chosen axis

**Primary organizing axis:** **judge-architecture / verification-topology** — i.e., the *shape* of the judge ensemble that closes the per-cycle V&V loop is the architectural primitive that everything else (cycle structure, watchdog cadence, knowledge accumulation, regime declaration, mandate handling) is configured around. Concretely: which judges run, what they each see, what model family backs each, what they each are allowed to *fail to detect*, and how their outputs compose into a decision to merge / hand back / escalate.

This is **not** a tier axis (the same topology runs on all work units; differences across cycles are inputs to the judges, not different ensembles per stake-class), **not** a pace-layers axis (no layer/cadence stack), and not a mandate-bifurcated axis (the topology is identical greenfield and brownfield; the *inputs to the judges* differ — which is the mechanism by which one architecture serves both mandates).

### 0.2 Acknowledgment of prohibition

I am unified-C-prime, the bias-correction re-dispatch of unified-C. I have read the [axis-divergence-audit](../bias-guards/phase-2/axis-divergence-audit.md) in full. The prohibition is:

- **No tier / risk-tier / stakes-tier / blast-radius** (track A and original C both picked it; the convergence is partly prompt-bias per F57's tier-presupposing framing and the brief's OQ-B7 candidate-list).
- **No pace-layers / Brier-style layering** (track B picked it).

I have also read F57 critically. F57's mechanism description — *"the factory classifies work units into automation-eligible vs human-required by stakes / risk tier"* — presupposes tier-classification as the factory's organizing primitive. **My architecture does not assume tier-classification at all.** Eligibility-for-merge in this architecture is determined by *whether the judge topology can close on the artifact*, not by a pre-assigned stakes label. F57 in this architecture re-reads as a *judge-coverage erosion* mode: convenience pressure reclassifies work as "judge-topology-T closes on it" when in fact T's blind spots have grown — a degradation of judge fitness rather than of a tier classifier. (See §3 / F57 treatment.)

### 0.3 Defense of the axis choice

Five reasons judge-topology is a credible primary axis, with corpus citations:

1. **The most load-bearing failure modes in the catalog are judge-shape failures.** F1 (Hallucination Loop), F27 (Circularity), F46 (Single-Model Review Blindspot), F33 (Adversarial-prompt defeat of LLM-based security analysis), F48/F49 (multi-agent collusion), F2 (Reward hacking), F4 (Code-quality teardown), F9 (Spec overfitting), F10 (Findings disappear into chat), F15 (Single-prompt collapse), F26 (Telephone). The catalog's first eleven F-modes are predominantly *about what the judges fail to catch and why*. An axis that puts judge-topology at the center engages this concentration directly rather than treating it as a per-tier overlay.

2. **The corpus' three most load-bearing contradictions about V&V are judge-topology contradictions.** CTR-D4 (F1: substrate-routing-mitigated vs. cross-model-architecture-mitigated), CTR-D7 (Anthropic single-judge-finding vs. cross-model-critic), CTR-D8 (same-model-judge legitimacy vs. Tournament model-family-diversity). All three contest *the topology of the judging layer*, not the tier of the work being judged. Phase-1 bias-guard WEAK-5 explicitly adds a **third** position (Anthropic Auto-Review: same-model-different-role specialization, five named critics — [report 23](../../research/23-anthropic-engineering-trilogy.md) §3.5) — making this a *three-position* corpus split that no other axis cleanly hosts.

3. **Judge-topology is mandate-agnostic at the primitive level but mandate-shaped at the input level.** This is the structural feature that lets one architecture serve both mandates. The judges (e.g., a Spec-Conformance judge, a Differential-Behavior judge, a Style/Maintainability judge, an Adversarial-Safety judge, an Idiom-Conformance judge) are the same primitives greenfield and brownfield. What differs is their *inputs*: greenfield's Differential-Behavior judge reads against synthesized scenarios + adjacent-exemplar oracles; brownfield's reads against the existing test suite + production telemetry deltas. The Idiom-Conformance judge is *vestigial* in greenfield (nothing to conform to except adjacent-corpus norms — low weight) and *load-bearing* in brownfield (the existing codebase's idioms are the norm — high weight). The mandate-difference is expressed as **input routing + judge weights**, not as different architectures. This is exactly the substrate-heavy + thin-methodology shape Round-2 framed as the unified-architecture target (CTR-C2) — but instantiated through judge-topology rather than through a tier classifier.

4. **The strongest commercial substrates ship judge-topology as their main differentiator.** [Report 18](../../research/18-openai-codex-substrate.md) (OpenAI Codex Auto-Review subagent), [report 23](../../research/23-anthropic-engineering-trilogy.md) §3.5 (Anthropic's five named specialist critics: duplicate-code coalescer / compiler-performance / efficiency / Rust code-quality / documentation), [report 11](../../research/11-openhands-substrate-audit.md) §6 (OpenHands RouterLLM as model-family-diversity primitive). Both A.G.I. labs ship a judge-topology as a *first-class substrate primitive*. The axis is not a synthesis construct; it is what the substrate-vendor doctrine already centers (CTR-H13, MISSED-4).

5. **Judge-topology dissolves the lights-out / L5 / regime tension (OQ-B1 / CTR-A4) at a level neither tier nor pace-layers can.** "Lights-out" maps cleanly to "the judge topology closes the cycle without human input." The Jaymin empirical anchors (CodeRabbit 1.4×, Veracode 45%, METR 19% — per [report 09](../../research/09-jaymin-book-harnesses-practices-mental-models.md) §2c) are about *what review-and-judge layers fail to catch*. Re-framing them as *judge-topology fitness measurements* rather than as *L-level ceiling claims* lets the v3 lights-out mandate (UC1) be defended on judge-topology grounds (i.e., "the bars Jaymin names are clearable when the judge topology has these specific properties"), and it side-steps the L5-as-target-vs-anti-pattern argument (CTR-A1) entirely.

**Defense against the obvious objection ("judge-topology is just one component of any architecture; calling it the axis is a category error"):** The same objection applies to tier-class ("classification is just one component") and to pace-layers ("artifact lifecycle is just one component"). The axis is whatever you elevate to the *first* design move — the move from which other choices fall out. Elevating judge-topology means the cycle structure, sandbox shape, watchdog cadence, cost ceiling discipline, scaffold posture, and mandate-input routing are all derived from "what does this judge ensemble require to close." That this is a credible first-move is precisely what reports 18, 23, and the F-mode catalog's center-of-gravity attest to.

### 0.4 Pre-responses to Phase-3 adversarial

- **"This is substrate-vs-methodology in disguise."** No: substrate-vs-methodology is a *layering* axis (which primitives live at which level); judge-topology is a *content* axis (which judges run, what they each cover). They are orthogonal. My architecture commits to "judge-topology is substrate-defined" but the *choice of topology* is the architectural move.
- **"This is just CTR-D4 made primary; insufficient signal."** CTR-D4 + CTR-D7 + CTR-D8 + CTR-D3 (Tournament-F27) + CTR-D5 (CaMeL multi-agent closure) + CTR-D1 (F36/F37/F38/F39 instruction-following + contradictory-prompt + vocabulary-lint + region-mismatch — all judge-detectable or judge-failed-to-detect) is six contradictions on the judge axis, not one. Compare to tier-axis (which is anchored on the F-mode severity gradient + Kahana RSI + Shapiro R3 — *also* six load-bearing items). Comparable corpus weight.
- **"What about Jaymin's three-position judge contradiction (CTR-D4 WEAK-5)?"** Treated directly in §2.2 as the central architectural decision; my answer is the **Layered-Judge Ensemble** (a fixed set of mandatory specialist judges *plus* a single cross-family arbiter for high-uncertainty decisions) — i.e., Anthropic-style specialization is the *default* topology, cross-family critic is the *escalation* topology. This is a synthesis of the three positions, not a vote for one.
- **"Why is this not just 'multi-agent V&V'?"** Because the architectural commitment is to a *named, fixed* topology declared as a substrate primitive with measured fitness, not to "many judges, hope they disagree." The judges have named roles, named blind-spots (declared up front), named inputs, and a named composition rule.
- **"This bakes in F46 cross-model and doesn't honor Anthropic's same-model-different-task finding."** It honors both — see §2.2.
- **"Cold-start has no inputs to feed judges."** Treated in §5; the cold-start substrate runs a *reduced judge topology* until the operator-curated scenario set and adjacent-exemplar corpus reach a coverage threshold, at which point the full topology activates.
- **"This is greenfield-shaped because brownfield has its own test suite as judge already."** Engaged in §6; brownfield's existing test suite is *one input* to the Differential-Behavior judge, not a substitute for the topology.

### 0.5 Mini-glossary for this track

| Term | Definition in this track |
|---|---|
| **Judge topology** | The named set of judges + their inputs + their model-family backing + their composition rule. Substrate-declared, version-pinned, measured. |
| **Mandatory judge** | A judge every cycle must run; failure to run is a substrate-level error, not a methodology choice. |
| **Specialist judge** | A judge with a narrow declared remit (e.g., "spec-conformance only"). Same-family backing permitted per Anthropic's finding. |
| **Cross-family arbiter** | A single judge running on a model family different from the builder; invoked when specialists disagree above threshold or when an escalation rule fires. |
| **Judge fitness** | The measured rate at which a judge catches the failures it claims to cover, against a holdout. Substrate-tracked. F-mode coverage map. |
| **Coverage map** | The declared (failure-mode × judge) matrix: which judge is responsible for catching which F-modes. Auditable. Required artifact. |
| **Closure** | A cycle is *closed* when the topology issues a merge decision; *not-closed* triggers re-cycle, escalate, or hand-back. |
| **Mandate-input router** | The substrate component that feeds each judge the right inputs for the active mandate (greenfield-shape vs. brownfield-shape inputs). |

---

## §1 — The unified case (architectural sketch)

A single architecture, **Judge-Topology Factory** (JTF), addresses both mandates by:

- **Fixing the judge topology as substrate.** The topology is the same for greenfield and brownfield cycles.
- **Routing mandate-specific inputs to the judges.** What changes across mandates is *what each judge reads*, not which judges run.
- **Tracking judge fitness against a coverage map.** The substrate maintains a (F-mode × judge) coverage matrix and a measured per-judge fitness score against a substrate-managed holdout. Drift in either is the canonical escalation trigger.

### 1.1 The fixed topology (substrate declaration)

Eight named judges, declared as substrate primitives:

1. **Spec-Conformance Judge.** Reads: the spec (in whatever format the methodology chose — CTR-B1 is orthogonal here). Inputs: builder's claim of which spec clauses are satisfied + diff. Outputs: per-clause satisfied / unsatisfied / unverifiable. Mandate input difference: greenfield reads operator-authored spec; brownfield reads spec-of-the-change (issue + spec-delta).
2. **Differential-Behavior Judge.** Reads: the artifact + a scenario set. Mandate input difference: greenfield uses operator-curated + synthesized scenarios + adjacent-exemplar oracles; brownfield uses existing test suite + production-telemetry-derived scenarios + scenarios extracted from the codebase ([report 01](../../research/01-strongdm-factory.md) §1 "Tokens are the fuel" — scenario-equivalents already inside the running system per CTR-B5 WEAK-3 sharpening; D-2 default explicitly inverted here for brownfield, accepted with justification for greenfield).
3. **Idiom-Conformance Judge.** Reads: artifact + a corpus of idioms. Mandate input difference: greenfield reads adjacent-exemplar corpus (low weight, vestigial); brownfield reads the existing codebase (high weight, load-bearing). This judge is the architectural answer to F4 (code-quality teardown) and CTR-G4 (code-as-opaque vs. code-archaeological): code is *not* opaque to JTF; the Idiom-Conformance judge is structurally a code-reading judge.
4. **Adversarial-Safety Judge.** Reads: artifact + a safety-scenario set. Always cross-family per F33 mitigation. Anchored on CaMeL/Trifecta closure (followup 08) plus the F12/F33 cluster. Mandate input difference: greenfield runs against synthesized adversarial scenarios; brownfield additionally runs against incident-replay scenarios extracted from runtime telemetry.
5. **Production-Scissors Gate.** Not a judge — a *gate*. Mechanical check that no production-mutating action is invoked outside an explicit allow-list. F44 mitigation. Identical greenfield / brownfield in substrate code; the *allow-list* differs (greenfield typically has no production target; brownfield has an explicit narrow list per F56 Replit-anchored mitigation).
6. **Spec-Authorship Judge.** Reads: spec deltas during spec authorship (greenfield cold-start, brownfield spec-of-the-change). Detects F36/F37/F38/F39 (instruction-following ceiling, contradictory-prompt collapse, vocabulary lint debt, point-spec/region-mismatch — per CTR-D1 resolution). Greenfield-heavier load; brownfield runs it on each change-spec.
7. **Cross-Family Arbiter.** A *single* judge running on a model family *different* from the builder and from the specialist judges. Invoked when (a) specialists disagree above threshold, (b) the Spec-Conformance judge returns "unverifiable" on a clause, (c) the Adversarial-Safety judge flags low-confidence, or (d) Patrol watchdog (D-6) detects judge-fitness drift. Honors F46 (cross-model critic catches what same-model misses); honors Anthropic's single-judge-finding (a single LLM call doing a different task is the most consistent — [followup 07](../../research/followup/07-evals-deepdive.md) §2.3) because the Arbiter's task is different (arbitration, not specialist judgment).
8. **Sentinel.** Not a per-cycle judge — a *meta-judge*. Runs against the substrate's recorded trajectory of the other seven (per D-7 trajectory-capture-as-substrate), measuring judge fitness over time against the holdout. Detects F55 (substrate-feedback dependence) and F57 (rebranded here as judge-coverage erosion). Anthropic's "single LLM call with single prompt outputting 0.0-1.0 + pass-fail" finding (followup 07 §3.6 verbatim) is the Sentinel's evaluation primitive.

### 1.2 Composition rule (substrate-declared)

A cycle closes *merge* iff:

- All mandatory judges return satisfied (or `not-applicable` with substrate-tracked justification).
- The Production-Scissors Gate passes.
- No judge fitness has crossed its alarm threshold within the last N cycles (Sentinel-tracked).
- No Adversarial-Safety judge low-confidence flag is outstanding.

Otherwise: re-cycle, escalate to Cross-Family Arbiter, or hand back to human re-entry (per OQ-B3 protocol). The exact composition algebra is a Phase-5 ADR.

### 1.3 What this architecture *isn't*

It isn't Tournament (no population; the judges are a *fixed ensemble*, not selection pressure on builders). It isn't Refinery (no layered spec stack; the spec is one of multiple inputs). It isn't Atelier (work-unit is not "an issue from a queue" by commitment — work-unit shape is a methodology choice on top of this judge primitive). It can *host* Atelier-style and Refinery-style work-unit shapes, but its commitment is to the topology, not the queue.

---

## §2 — Engagement with load-bearing tensions

### 2.1 OQ-B1 / CTR-A1 / CTR-A4 (lights-out vs. L5 vs. regime)

**Resolution strategy:** option (a) from brief §2.1 — *"explain how the lights-out mandate clears Jaymin's bars at a per-cycle level, by what mechanism, measured how"* — operationalized through the Sentinel + coverage map. Specifically:

- Lights-out is operationally defined as *"the judge topology closes the cycle without human input."*
- Jaymin's empirical bars (K=5 ≥90%, prompt-paraphrase 5-of-5, zero medium-or-high safety incidents — glossary §0) are re-cast as *judge-topology fitness targets*: K=5 consistency is measured per-judge by the Sentinel; prompt-paraphrase robustness applies to the *spec interpretation* under the Spec-Conformance judge; safety-incident severity is the Adversarial-Safety judge's output class.
- The Jaymin numbers (CodeRabbit 1.4×, Veracode 45%, METR 19%) are re-read per CTR-E3: as *judge-coverage measurements* on populations whose judge topologies were absent or impoverished. The factory's defense against the numbers is that its declared topology has named coverage of the F-modes those numbers expose; the substrate measures whether it does.
- The CTR-A4 "lights-out ≠ L5" mapping test: lights-out = topology-closes-cycle. L5 (Jaymin) = no-human-ever-in-loop, *as a regime claim about a population of cycles*. JTF declares lights-out *cycle-level*, not regime-level; humans are out of the inner loop per cycle but in the outer loop on Sentinel-triggered escalation and operator-curated scenario maintenance. This is **not L5** in Jaymin's sense; it is L4 plus a substrate primitive that aspires to L5 per-cycle. CTR-A1 mostly dissolves because the contested term ("L5") doesn't apply to JTF's commitment.

### 2.2 CTR-D4 / D7 / D8 + WEAK-5 (the three-position F1 mitigation split)

The corpus has three positions on F1/F27 mitigation:

- (i) **Substrate-routing-mitigated** (OpenHands RouterLLM, CTR-D4 Claim 1).
- (ii) **Cross-model-architecture-mitigated** (CJ Hess `kevin`/`carl`, F46, CTR-D4 Claim 2 / CTR-D7 Claim 2).
- (iii) **Same-model-different-role specialized** (Anthropic Auto-Review five critics, WEAK-5 third position; CTR-D7 Claim 1 — *"using the same model is usually fine because the judge is doing a different task"*).

JTF synthesizes all three:

- **Specialist judges (3 + Spec-Authorship)** use same-model-different-role per Anthropic's finding. They are *different tasks* from the builder (spec-conformance, behavior-differential, idiom-conformance, spec-authorship-quality), so the Anthropic anchor applies.
- **The Cross-Family Arbiter** uses cross-family per F46 / CJ Hess. It is the escalation path for disagreement and uncertainty, not the default judge — preserving the Anthropic empirical anchor at the common-case default and the CJ Hess anchor at the high-uncertainty edge.
- **Routing (RouterLLM-equivalent)** is *substrate plumbing*, not an architectural mitigation in its own right; it's what lets the substrate fulfill the topology's family-diversity declaration. The OpenHands position is downgraded from "the mitigation" to "the infrastructure the mitigation runs on" — CTR-D4 dissolves at the architectural layer; CTR-D7/D8 dissolves by accepting Anthropic's same-model finding *for specialists* and CJ Hess's cross-model finding *for the arbiter*.

### 2.3 UC4 working hypothesis (CTR-C2)

UC4 says greenfield and brownfield need different solutions because greenfield is spec-malleable and brownfield is code-archaeological. JTF says:

- The *judge topology* is the same. The *inputs* to specific judges differ in well-defined ways (per §1.1).
- Spec-malleability is honored at the Spec-Conformance judge's input level: greenfield specs are explicitly versioned + the Spec-Authorship judge runs per spec-change (high frequency); brownfield specs are spec-of-the-change (small, change-scoped) and the Spec-Authorship judge runs per change. The *malleability* is in the spec lifecycle the substrate hosts, not in the topology.
- Code-archaeology is honored at the Idiom-Conformance judge's weighting and the Differential-Behavior judge's scenario sourcing. Brownfield's existing tests / production traces are first-class inputs (CTR-B5 D-2 *inverted* for brownfield, per the WEAK-3 sharpening showing StrongDM itself permits in-tree scenario-equivalents).
- UC4 is **falsified for the unified architecture's domain** — but its phenomenology (spec-malleable / code-archaeological) is preserved as input-routing shapes, not erased.

### 2.4 MISSED-3 (El Kaim invariants vs. UC4 spec-malleable, CTR-B6)

El Kaim's invariant pack is the *Adversarial-Safety judge's policy table* in JTF — a typed, non-negotiable set of conditions any artifact must preserve. Spec-malleability lives at the Spec-Conformance judge's level. These coexist because the topology assigns them to different judges: invariants live at the safety layer (rarely changing, operator-curated, hard-coded as Adversarial-Safety inputs); malleable spec lives at the conformance layer (per-cycle versioned). No contradiction at the architectural level. MISSED-3 dissolves into "different judge, different input."

### 2.5 CTR-A4 (vocabulary mapping) + brief §2.1 strategy

As above: JTF's mapping is "lights-out = topology-closes-cycle, *per cycle*; not a regime claim." This is option (b) from brief §2.1 (*redefine the operating mode at a defined surface*) layered with option (a) (defend at per-cycle empirical bars). Option (c)'s regime classifier is *not* used — there's no tier classification in JTF.

---

## §3 — F-mode treatment (selected)

I treat the F-modes most directly engaged. Full coverage map is a Phase-5 ADR artifact.

| F-mode | Judge | Notes |
|---|---|---|
| F1 (Hallucination Loop) | Cross-Family Arbiter + Sentinel | Topology family-diversity declaration covers the substrate-routing angle (CTR-D4 (i)); Arbiter covers the architecture angle (ii); Specialists cover Anthropic's (iii). |
| F2 (Reward hacking) | Differential-Behavior + Spec-Conformance | Two judges with different inputs catch the gate-game mismatch. |
| F3 (Spec-completeness fallacy) | Adversarial-Safety + Spec-Authorship | Authorship-quality catches incomplete enumerations; Adversarial-Safety catches unspecified-complement failures. |
| F4 (Code-quality teardown) | Idiom-Conformance | The reason this judge exists. |
| F5 (Cognitive ceiling) | n/a — operator-side | Honored by topology being closure-by-judges-not-by-humans; F5 reduces to *Sentinel escalation rate* the operator must keep up with. |
| F8 (Stale-knowledge inversion) | Sentinel | Tracks judge fitness over time; stale knowledge surfaces as fitness drift. |
| F9 (Spec overfitting) | Spec-Authorship + Spec-Conformance composition | Two judges with adversarial relation prevent retroactive spec-fit. |
| F12 / F33 (Trifecta / adversarial-prompt) | Adversarial-Safety (cross-family) | CaMeL pattern from followup 08 instantiated as this judge's policy core. |
| F15 / F26 (Single-prompt collapse / Telephone) | Cross-Family Arbiter | Family-diversity defeats the "most-trained direction" attractor. |
| F36 / F37 / F38 / F39 (CTR-D1 cluster) | Spec-Authorship | Per CTR-D1 resolution. |
| F44 (Production scissors) | Production-Scissors Gate | Gate not judge. |
| F46 (Single-Model Review Blindspot) | Topology declaration | Architectural: specialists are different roles, arbiter is different family. F46 is the topology's first-principles motivation. |
| F48 / F49 (Multi-agent collusion) | Cross-Family Arbiter + Sentinel | Report 37 Portuguese-prompt effect (CTR-C10) is a Sentinel-tracked observable. |
| F55 (Substrate-feedback dependence) | Sentinel | The reason Sentinel exists. |
| F56 (Guardrail-bypass under stress) | Production-Scissors Gate + Adversarial-Safety | Mechanical gate + adversarial judge cross-check. |
| F57 (Design-authority erosion) | **Re-read as judge-coverage erosion.** | In JTF, F57 is *judge-coverage erosion*: the Sentinel's role is precisely to detect when the topology's coverage of stated F-modes has degraded. F57's tier-classification presupposition is replaced with judge-fitness-tracking. |
| F59 (Premature decomposition) | n/a — methodology-layer | JTF is judge-topology; F59 affects spec/build decomposition which is methodology-overlay. |
| F60 (Parallel-cycle compounding) | Sentinel + composition rule | Substrate tracks aggregate; the composition rule's holdout discipline (D-4 accepted) keeps per-cycle judge fitness measurable. |
| F61 (Context fragmentation) | n/a primarily — substrate concern | The judges have orthogonal context boundaries; F61 is a methodology concern at the builder layer, not the judge layer. |

**Most-cited F-mode in this track:** **F46** (Single-Model Review Blindspot) — it is the topology's first-principles motivation. **Runner-up:** F1/F27 cluster.

---

## §4 — §4 defaults: accepted vs. challenged

Per D3, each Round-1/Round-2 default marked.

- **D-1 (specs are durable, version-controlled, human-curated artifact):** `accepted with justification`. Specs are the Spec-Conformance judge's primary input and the Spec-Authorship judge's authoring target; their durability is what makes the topology auditable across mandates.
- **D-2 (scenarios outside codebase as holdout):** `challenged for brownfield, accepted for greenfield`. Per CTR-B5 + WEAK-3 sharpening, brownfield scenarios *are* legitimately inherited from the codebase (production traces, existing tests, incident replays — the Differential-Behavior judge's brownfield input mode). Greenfield retains the out-of-tree discipline. The judge topology accommodates both via input routing without changing the topology.
- **D-3 (Agent = Model + Harness):** `accepted with justification` — *augmented*. JTF's primary primitive is *judge topology*, but per Round-2 C10 the agents (builder + each judge) decompose into model + harness. The brief's fragile-flag (graph-node and population architectures) doesn't apply here — JTF is neither.
- **D-4 (holdout discipline substrate-enforced):** `accepted with justification`. Sentinel cannot measure judge fitness without holdout; D-4 is structurally load-bearing for JTF. (This is more than accepting; it's promoting.)
- **D-5 (hard cost ceilings in CI):** `accepted with justification`. The topology's cost is dominated by judge invocations; the Sentinel's holdout-evaluation is the cost-control surface. CTR-E1 / CTR-E6 (CaMeL utility tax) acknowledged: judge-topology costs are non-trivial and substrate-enforced.
- **D-6 (tiered watchdog: Daemon / Triage / Patrol):** `accepted with justification`. Patrol is the substrate component that escalates Sentinel-detected fitness drift to humans. Note: this is a *substrate cadence* primitive, not a stakes-tier — the prohibition is on stakes/risk tiers, not on temporal cadence tiers.
- **D-7 (trajectory capture cheap and production-tested):** `accepted with justification`. Sentinel reads trajectories; D-7 is structurally load-bearing for JTF.

---

## §5 — Cold-start (mandatory per Historian M4/M5)

The greenfield cold-start problem in JTF: day 0 has no operator-curated scenarios, no holdout, no incident-replay corpus, no codebase to extract idioms from. The judge topology cannot run at full fitness yet.

### 5.1 Cold-start posture: reduced topology + scaffolded holdout

**Substrate runs a *reduced* judge topology** until coverage and holdout reach declared thresholds:

- **Active from day 0:** Spec-Conformance judge (reads operator-authored spec), Spec-Authorship judge (catches CTR-D1 cluster: F36/F37/F38/F39 in spec drafting), Adversarial-Safety judge (operator-seeded invariants from El Kaim-style intent pack per CTR-B6 / report 14), Production-Scissors Gate (gate, mandate-trivial in greenfield), Cross-Family Arbiter (on all decisions, not just escalations, until specialist fitness is measurable).
- **Reduced / scaffolded from day 0:** Differential-Behavior judge runs against (a) operator-curated initial scenarios + (b) scenarios synthesized from adjacent-exemplar projects (per report 25 RE foundations) + (c) prompt-underspecification stress scenarios (per report 26). Coverage is declared *partial* and flagged as such.
- **Inactive from day 0:** Idiom-Conformance judge (no codebase to read; vestigial in greenfield anyway).
- **Sentinel runs from day 0** against an operator-authored bootstrap holdout (per report 30 cognitive escrow: the operator's holdout-authoring is the *interval-as-design-surface* primitive; the time the operator spends authoring scenarios is the cognitive-escrow budget).

### 5.2 Required inputs invoked

- **Report 25** (RE foundations) — INCOSE GtWR R7/R8/R9 anchor the Spec-Authorship judge's policy table for vocabulary lint (F38).
- **Report 26** (prompt underspecification) — Yang instruction-following ceiling (F36) + Larbi contradictory-prompt collapse (F37) are scenario classes the cold-start Spec-Authorship judge runs against.
- **Report 30** (cognitive escrow) — the operator's cold-start authoring time *is* the cognitive escrow; the Sentinel's bootstrap holdout is what the operator escrows by authoring it.
- **Report 31** (Caremark RSI) — the three-part RSI test informs the Adversarial-Safety judge's policy; if the greenfield target falls in RSI scope, JTF declares it and routes through the Caremark-board-exposure escalation path before lights-out activates.
- **Followup 10** (governance) — BCG-vs-Kahana (CTR-H5) is the audit-trail discipline; JTF's substrate trajectories satisfy BCG's "structurally easier to audit" claim, and the coverage map + Sentinel logs are the audit-discoverable evidence Kahana asks for.

### 5.3 Trajectory day-0 → day-N

- **Day 0:** reduced topology active; operator hand-authors the bootstrap holdout (scenarios + invariants + adversarial cases). Sentinel measures specialist fitness against bootstrap holdout; results published.
- **Day 1–N (during which N is operator-set, not predetermined):** factory cycles accumulate; each cycle's trajectory is captured (D-7); the Sentinel re-evaluates fitness; operator audits Sentinel deltas weekly.
- **Transition to steady-state:** declared by the Sentinel when (a) coverage map fitness ≥ declared threshold for each mandatory judge for ≥ K cycles, and (b) holdout has expanded past initial bootstrap. The Cross-Family Arbiter de-escalates from "all decisions" to "disagreement-and-uncertainty" mode at the same point.
- **Silent-failure protection:** the bootstrap holdout is operator-authored (not factory-authored) and never overwritten by factory-generated content (D-4 substrate-enforced); F55 (substrate-feedback dependence) is structurally defeated for the bootstrap-evaluation surface. Sentinel reports flat or rising fitness as suspicious if accompanied by stable cycle output — the *silent* failure detection per F47 (Goodhart) is *Sentinel-Goodhart-watch* on the fitness metric itself.

### 5.4 What this *doesn't* solve

- Cold-start cannot make the factory match its steady-state coverage; declared transparently.
- The operator's bootstrap-holdout-authoring labor is real (CTR-E6 CaMeL utility-tax analogue); JTF makes the labor visible rather than hidden (per UC5 accuracy-over-speed; per cognitive-escrow framing).

---

## §6 — Brownfield treatment

JTF on brownfield runs the **full** judge topology from day 0 — the existing codebase, test suite, runtime telemetry, and incident archive *are* the inputs the cold-start version had to bootstrap.

- **Spec-Conformance judge** reads spec-of-the-change (per CTR-G3 legacy-ingestion treatment), not a global spec.
- **Differential-Behavior judge** runs existing test suite + production-telemetry-derived scenarios (D-2 inverted, accepted with justification). Per CTR-B5 / WEAK-3, this is closer to StrongDM's *actual* practice than the simplified D-2 default.
- **Idiom-Conformance judge** runs at full weight against the existing codebase. CTR-G4 (code-as-opaque vs. code-archaeological): brownfield JTF treats code as *readable archaeology*, contradicting StrongDM's pure-opaque-weight discipline. This is an explicit divergence from StrongDM; defended on the basis that brownfield's existing code is necessarily a primary input (UC4) — StrongDM's discipline was implicitly greenfield-shaped (CTR-G1).
- **Adversarial-Safety judge** runs against synthesized adversarial + incident-replay-derived scenarios from the brownfield system's history.
- **Spec-Authorship judge** runs on each change-spec (high frequency in active brownfield).
- **Production-Scissors Gate** carries the brownfield allow-list (F44 / F56 anchor); production access narrow and explicit.
- **Cross-Family Arbiter** in normal escalation mode (specialist disagreement + low-confidence).
- **Sentinel** runs against a holdout the substrate maintains from production behavior the factory has *not* yet modified (D-4 substrate-enforced).

OQ-B4 (work-unit shape): JTF's topology is work-unit-shape-agnostic. Atelier-style (issue-queue), Refinery-style (change-against-spec), and codebase-evolution-proposal are all hostable on the same topology — they differ in how the methodology *frames* the input to the Spec-Conformance and Spec-Authorship judges. JTF doesn't prescribe; it hosts.

---

## §7 — Substrate primitive set implied

A non-exhaustive list (Phase-4 derives the canonical set):

1. **Judge-topology declaration primitive** — typed, version-pinned, coverage-map-attached.
2. **Mandate-input router** — routes the right inputs to each judge for the active mandate.
3. **Holdout discipline** (D-4 promoted; substrate-enforced; cold-start operator-seeded).
4. **Trajectory capture** (D-7; Sentinel reads).
5. **Family-diversity plumbing** (RouterLLM-equivalent, per CTR-C4 — *not* the architectural mitigation, just the substrate plumbing).
6. **Production-scissors gate primitive** (F44/F56).
7. **Sandbox primitive** (followup 08 / CaMeL).
8. **Cost ceiling primitive** (D-5; judge-invocation cost is the dominant surface).
9. **Tiered watchdog** (D-6 — Daemon / Triage / Patrol; Patrol surfaces Sentinel-escalation; *temporal* cadence tier, not stakes tier).
10. **Coverage-map artifact primitive** — auditable, BCG-Kahana-friendly.
11. **Scaffold discoverability** (AGENTS.md / SKILL.md per CTR-C6 — *accepted; this track sides with the scaffold-substrate camp* over the bitter-lesson camp; defended on the basis that the judge topology itself is a scaffolded structure JTF needs the substrate to encode).

---

## §8 — Comparison and honest report-back

**Most-cited contradictions / F-modes in this track:** **CTR-D4 / D7 / D8** (the three-position F1 mitigation split — central to §2.2); **CTR-A4** (vocabulary mapping — engaged in §2.1); **CTR-B5** (D-2 fragility — engaged via input routing); **F46** (single-model review blindspot — topology's first-principles motivation); **F1/F27** (loop / circularity); **F57** (re-read as judge-coverage erosion).

**Honest comparison of my axis (judge-topology) vs. A-prime's expected pick:** A-prime is dispatched concurrently with the same prohibition. The open list the orchestrator floated includes substrate-vs-methodology split, regime (Augmentation/Automation), work-unit-class taxonomy, codebase-lifecycle stage, knowledge-accumulation, judge-architecture, scaffold-vs-substrate, language-as-harness, governance-tier. A-prime's most likely picks (by conviction value) are probably **knowledge-accumulation strategy** (anchored on CTR-H2 / CTR-H3 / F8 / F55) or **substrate-vs-methodology** (Round-2 baseline framing) — both are well-cited, and both are structurally distinct from judge-topology. If A-prime picks knowledge-accumulation, the two tracks complement: judge-topology is the per-cycle V&V primitive; knowledge-accumulation is the cross-cycle compounding primitive. If A-prime picks substrate-vs-methodology, the tracks are partly competing — substrate-vs-methodology subsumes "judge-topology is substrate" as a sub-question but loses the architectural commitment to a specific topology.

**Honest comparison vs. the original tier / pace-layers axes (A, B, original C):**

- vs. **tier (A, original C):** Tier organizes by *what the work is*; judge-topology organizes by *how V&V closes*. Tier's strongest move is the F-mode severity gradient (real corpus signal per audit §4); judge-topology's strongest move is the F-mode catalog's *judge-shaped* concentration (F1/F2/F4/F9/F15/F26/F27/F33/F46/F48/F49 — eleven of the catalog's center-of-gravity). Both are corpus-supported; the prohibition pushed me to judge-topology, and on reflection judge-topology is genuinely defensible on independent grounds. Tier handles RSI/regulated cleanly (T3/T4 in A); JTF handles RSI by *Adversarial-Safety judge policy* + the Caremark RSI escalation path — less elegant for governance-heavy deployments but equivalent in coverage. **Honest weakness:** JTF does not naturally produce a "lights-out cleared / not cleared" per-work-unit label; a deployer who wants tier-class labels has to derive them from the coverage map.
- vs. **pace-layers (B):** Pace-layers organizes by artifact churn cadence; judge-topology by V&V shape. They are nearly orthogonal — a JTF deployment could *also* declare pace-layers per its spec/architecture/standards artifacts (the Spec-Conformance and Spec-Authorship judges could be layered to honor Brier's stack). B's strongest move is dissolving CTR-A4 at the regime-per-layer level; JTF dissolves CTR-A4 at the per-cycle-closure level. Both work. JTF has a sharper F-mode story; B has a sharper artifact-lifecycle story.

**Verdict on unified-possibility:** **Yes, defensibly unified under the judge-topology axis.** The topology is identical greenfield and brownfield; mandate differences route through inputs, not through architecture. UC4 is *partly* falsified (one architecture *can* serve both mandates), with the phenomenology preserved as input-routing. The unified case is strong specifically on the F1/F27/F46 cluster and on the Anthropic-vs-CJ-Hess-vs-OpenHands three-way V&V contradiction (CTR-D4/D7/D8 + WEAK-5) — which no other axis handles natively.

---

*End of unified-C-prime.md.*
