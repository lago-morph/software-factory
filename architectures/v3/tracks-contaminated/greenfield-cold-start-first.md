---
track: greenfield-cold-start-first
axis: cold-start-first
mandate-scope: greenfield
based-on-commit: 9a205b6
based-on-date: 2026-05-24
---

# Greenfield Track — Cold-start-first

> **One-phrase axis.** *Day-0 is the architecture.* Build the factory as a **scaffolded escape from underspecification** — a substrate whose first job is to keep the spec honest while there is no codebase, no scenarios, no run history, and no holdout suite to fall back on; everything that looks like steady-state methodology is what falls out of the day-0 design when the day-0 inputs stop being the only inputs.

This track is one of nine Phase-2 outputs running concurrently against [`00-brief-v3`](../00-brief-v3.md). It is the **greenfield × cold-start-first** axis. It does not attempt to be comprehensive on substrate, methodology, governance, or brownfield — other tracks own those. Its job is to be **strong on the cold-start framing for greenfield** and to make §5 the load-bearing contribution.

---

## §0 — Vocabulary and axis defense

### 0.1 Working glossary (track-local; supplements brief §0)

| Term | Track-local meaning |
|---|---|
| **Day 0** | The factory's first cycle on a greenfield target: no codebase, no `docs/solutions/`, no prior trajectories, no scenario corpus, no production telemetry. Only operator-curated priors (UC6's "priors permitted, not no priors"), the spec under authoring, and whatever scaffolds the operator brings in. |
| **Cold-start window** | The interval from Day 0 to the cycle at which the factory has *enough* internally-generated artifacts (scenarios, trajectories, judge-calibration, vocabulary) that steady-state mechanisms can take load-bearing weight. Duration is emergent; track proposes empirical bars (§5.7). |
| **Spec-honesty** | The property that the spec the factory is operating against does not silently contain F37 (contradiction), F36-pressure (over-spec), F39 (point/region mismatch), or F38 (vocabulary lint debt). Spec-honesty is a *first-class invariant* under this axis. |
| **Underspec failure cone** | The four-failure-mode cluster (F36 instruction-following ceiling, F37 silent contradictory-prompt collapse, F38 vocab lint debt, F39 point-spec/region-mismatch) that operates *upstream of the agent* and is therefore unobservable at the agent or judge layer. The cold-start regime is where this cone is widest. |
| **Bootstrap-borrowed prior** | A holdout, judge, scenario, or skill imported from outside this factory's run history — operator's adjacent-domain corpus, INCOSE/EARS grammar, vendor skill libraries, exemplar projects. Treated as substrate input; tagged so steady-state can sunset them. |
| **Escrow-shaped authoring** | Per Kahana (report [`30`](../../../research/30-cognitive-escrow.md) §4), treating the prompt→response interval as a *design site* during spec authoring. For day-0 this is the only available reflection surface; for steady-state it complements automated review. |
| **Sunset edge** | An explicit edge in the trajectory store recording when a bootstrap-borrowed prior was retired in favor of a factory-generated equivalent. Cold-start exits when sunset-edge count crosses a threshold. |
| **El-Kaim invariant** | A non-negotiable condition declared in the 9-field intent block (report [`14`](../../../research/14-el-kaim-book-intent-and-spec-authorship.md) §3, Ch3 §4.1) — *"non-negotiable conditions that any valid realization of the intent must preserve."* Compiles into executable OPA/Rego (§3, El Kaim Ch6 §5). Load-bearing for the MISSED-3 resolution in §5.5. |

### 0.2 Axis defense: pre-empting "cold-start is transient"

The strongest critique of this axis: *cold-start is a transient state. Building the whole architecture around it under-serves steady-state operation; an architecture so shaped will pay forever for a regime it occupies briefly.*

Three responses, in order of strength.

**(a) The cold-start regime recurs.** A lights-out greenfield factory does not have *a* cold-start. It has one per new project (UC1 scope is "greenfield applications," plural). For an operator running the factory across multiple greenfield projects — Schillace's *"12-person team / >500 projects"* shape (report [`28`](../../../research/28-schillace-sunday-letters.md) §"team-shape" via corpus inventory) — every new project is Day 0. Cold-start-shaped substrate amortises across project-starts; methodology-shaped-around-steady-state does not. **An architecture that solves day-0 once gets steady-state for free across projects.**

**(b) The cold-start failure modes do not retire.** F36 (instruction-following ceiling, Yang et al. via report [`26`](../../../research/26-prompt-underspecification-academic.md) §2.4) bites at any spec length >10–15 active requirements regardless of factory maturity. F37 (silent contradictory-prompt collapse, Larbi et al. via report 26 §3.3, GPT-4 Pass@1 73.8% → 6.7%) bites every cycle that introduces new requirements — i.e. every cycle that is not pure regression. The four-mode underspec cone (§0.1) is *always* the regime upstream of the agent. The architecture that is honest about Day 0 is also honest about every cycle that adds spec — which is most of them.

**(c) The cold-start architecture is what an honest steady-state architecture looks like anyway.** Kahana's RSI failure modes — behavioural drift (F55), self-reference loop (F55), goal subversion (F54) (report [`31`](../../../research/31-caremark-rsi-board-exposure.md) §1) — all describe what happens *when steady-state has no anchor outside its own outputs*. The cold-start architecture's discipline of bootstrap-borrowed-priors + sunset-edges + escrow-shaped authoring is the same discipline that defeats F54/F55 in steady-state. Cold-start framing forces the architecture to never let the factory's own outputs become the only signal.

**Where the axis honestly does not stay load-bearing.** Steady-state performance optimisation (cost ceilings, parallelism scaling, CI-as-bottleneck per report [`35`](../../../research/35-lenny-howiai-spec-driven-and-team-ops.md)) is shaped by throughput, not day-0. Track-level acknowledgment: cold-start-first is wrong to be the primary axis if (i) the operator runs *one* greenfield project for years and (ii) the spec stabilises early. UC1 explicitly forecloses (i) — "greenfield applications" plural. UC4 explicitly forecloses (ii) — "spec-malleable… architecture changes during spec refinement." Within UC1+UC4, cold-start-first survives steady-state.

---

## §1 — The steady-state architecture this cold-start design produces

This section is deliberately brief. The cold-start work in §5 *is* the architecture; §1 is what it looks like after the cold-start window has closed.

### 1.1 Shape (one paragraph)

The factory is a **scaffolded escape from underspecification**. At the centre is a typed-spec authoring pipeline (El Kaim 9-field intent block + INCOSE EARS/GtWR linting + Larbi contradiction-detector); around it sit three structural layers: a **bootstrap-prior store** (operator-curated holdouts, judges, scenarios, skills imported from outside this factory's run), a **trajectory + sunset ledger** (event-sourced per OpenHands V1 D-7 cheapness per report [`11`](../../../research/11-openhands-substrate-audit.md), augmented with sunset-edges per §0.1), and a **escrow-interval harness** (Kahana's interval-as-design-site, report [`30`](../../../research/30-cognitive-escrow.md) §4, surfaced during spec authoring). Above this sits a small Methodology layer that picks work units per the El-Kaim chain (intent → decision → spec → control → feedback, report [`14`](../../../research/14-el-kaim-book-intent-and-spec-authorship.md) §2). The single load-bearing claim: the spec layer carries an Ashby-adequate substrate of deterministic checks (§3.2) so the LLM does not have to be its own judge while the cold-start window is open.

### 1.2 Primitives the architecture demands of the substrate

(Each maps to a Phase-4 substrate-vs-methodology decision; this track does not pre-resolve OQ-B2.)

| # | Primitive | Why cold-start needs it |
|---|---|---|
| P1 | **Typed spec store with stable IDs** | El Kaim 9-field intent block + ArchitectureSpecification typed object (report [`14`](../../../research/14-el-kaim-book-intent-and-spec-authorship.md) §3, §13); enables F38 vocabulary-lint and F39 region-vs-point checks at authoring time. |
| P2 | **Deterministic spec linter** (GtWR R7/R8/R9/R26/R35 + EARS pattern checker) | Closes F38 deterministically; closes F36-pressure by surfacing spec budget; runs at zero marginal cost per report [`25`](../../../research/25-requirements-engineering-foundations.md) §3.2. |
| P3 | **Contradiction-detector (substrate primitive, not LLM-judged)** | Closes F37 — the model itself cannot detect contradictions reliably (MCC ≤0.55 per report [`26`](../../../research/26-prompt-underspecification-academic.md) §3.3). Substrate must do this without delegating to the same model class building the code. |
| P4 | **Bootstrap-prior store + sunset-edge ledger** | Day 0 holdouts/judges/scenarios live here; sunset-edges track replacement; substrate enforces "no factory-generated artifact in the holdout set during the cold-start window." |
| P5 | **Escrow-interval harness hook** | Kahana's interval-as-design-site (report [`30`](../../../research/30-cognitive-escrow.md) §4 + §4-catalogue items 1–6); fires during spec authoring; substrate-triggered, not voluntary-discipline (closes F53). |
| P6 | **Trajectory capture with stable trajectory IDs** | D-7 cheap (OpenHands V1 sub-ms persist per report [`11`](../../../research/11-openhands-substrate-audit.md)); cold-start specifically needs it for forensic reconstruction of *why* the spec said what it did (F14 widening). |
| P7 | **Judge-source isolation registry** | Records which judge ran against which builder; substrate prevents same-model-family builder+judge during cold-start (closes F1/F27 amplification when out-of-distribution signal is absent). |

### 1.3 Work-unit class served (per D2)

This track is *initial-spec*-shaped first, *mvp*-shaped second. See §6 mandate-fit YAML.

---

## §2 — Lights-out / L5 / regime tension treatment (per brief §2.1)

**Vocabulary mapping test first** (per glossary §0 "F36/F37 collision" methodology applied to the L5 vocabulary question): for this track, "lights-out" ≠ L5. The cold-start regime *requires* substrate-triggered escrow-interval reflection prompts during spec authoring (§5.4) — i.e., the human IS routinely re-engaged inside the per-cycle loop during day 0, by substrate-design. This is Shapiro's L4 ("I'm here," followup [`01`](../../../research/followup/01-shapiro-five-levels.md)) at the *spec-authoring* layer, not at the implementation layer. Implementation work below the spec runs lights-out.

**Resolution path (option c + b from brief §2.1).** Regime classification by **layer**, not by work-unit-class:

- **Spec-authoring layer**: L4 during cold-start (substrate fires escrow-interval prompts; human re-engages); transitions to L4-with-reduced-cadence at cold-start exit; never goes L5 because F37 contradiction-detection is upstream of agent and the human is the residual oracle when the deterministic detector flags ambiguity it cannot classify.
- **Implementation / build / verify layers**: lights-out throughout (judge-isolated builder, deterministic gates, holdout-protected scenarios).
- **Governance / sunset layer**: human-policy with automated triggers; humans set sunset thresholds and review sunset-edge ledger on cadence (Kahana RSI three-controls per report [`31`](../../../research/31-caremark-rsi-board-exposure.md) §5).

**Why this clears Jaymin's bars (option a partially).** The factory does not clear Jaymin's 90% K=5 / 5-of-5 Automation Mode bars *for the spec layer* during cold-start by design — it runs in Augmentation Mode there. It can clear them at the implementation layer because the spec layer has been deterministically linted upstream. Track's claim: Jaymin's bars (per report [`09`](../../../research/09-jaymin-book-harnesses-practices-mental-models.md) §5.5) were measured against architectures that conflate spec authoring and implementation. Layer-split changes which bar applies where.

**OQ-B6 stance.** This track does not commit to Jaymin's thresholds as the only bar set; it adopts Larbi's RIR (Runnable but Incorrect Rate; ≤30% as a candidate cold-start exit gate) and Yang's per-requirement guess-correctly baseline (41.1% as a candidate "the LLM was right anyway" floor) as supplementary measurement primitives — both from the cold-start required reading (report [`26`](../../../research/26-prompt-underspecification-academic.md) §2.4, §3.3).

---

## §3 — Failure-mode prioritisation (greenfield severity, cold-start lens)

This track reads [`failure-modes-v3`](../failure-modes-v3.md) through the cold-start lens. The **underspec cone (F36/F37/F38/F39)** is treated as primary because the cold-start regime has no out-of-distribution ground truth (per failure-modes-v3 §7 force #1) to detect upstream-of-agent failures after-the-fact. Counted as "critical for greenfield cold-start" — promoted *above* even F1 (Hallucination Loop) in track priority because F36/F37 are the *prompts* the hallucination is sampled from.

### 3.1 Cold-start critical (must mitigate at substrate, not methodology)

| F-mode | Why critical for cold-start | Track mitigation site |
|---|---|---|
| **F36** Instruction-following ceiling | Greenfield specs grow fast; >10–15 active requirements degrades silently (98.7%→85.0% gpt-4o per [`26`](../../../research/26-prompt-underspecification-academic.md) §2.4). | P2 deterministic linter surfaces budget overrun; Yang Bayesian background-spec partitioning (§5.4). |
| **F37** Silent contradictory-prompt collapse | Spec-malleability *generates* contradictions in early cycles; LLM-judge can't detect (MCC ≤0.55). | P3 substrate primitive (deterministic + OPA/Rego per El Kaim Ch3 §5.4 Role-1). |
| **F38** Vocabulary lint debt | LLM-drafted specs accumulate GtWR R7/R8/R9 violations; deterministic. | P2 GtWR linter as authoring-boundary gate. |
| **F39** Point-spec/region-mismatch | Greenfield outcome-space is largest (Complexity Primer principle 12); point-spec mismatch is structural in greenfield. | Complexity-diagnosis field in spec head (per [`25`](../../../research/25-requirements-engineering-foundations.md) §5.6 Table 2). |
| **F1** Hallucination Loop | No out-of-dist ground truth at Day 0; builder/judge correlated errors are undetectable. | P7 judge-source isolation; bootstrap-borrowed judge from operator's prior corpus during cold-start. |
| **F27** Same-model build+validate circularity | Population-scale F1 at high parallelism. | P7 + RouterLLM-style provider diversity (CTR-C4 unresolved at substrate level; track does not pick). |
| **F25** Design starvation | Brief §5.2 explicitly names cold-start as the design-starvation regime. | Escrow-interval harness (P5) surfaces decision-seeds (El Kaim 9-field item 8) before agents idle. |
| **F41** Under-defined-intent debt | Greenfield intent constitutively under-defined in early cycles. | El Kaim 9-field intent block discipline (§5.5). |
| **F55** Behavioural drift (self-reference loop) | Greenfield has no out-of-dist ground truth; factory output becomes only signal fastest. | P4 bootstrap-prior store + sunset-edge ledger; substrate forbids factory-generated artifacts in holdout during cold-start window. |
| **F40** Last-Mile Drift | Lights-out greenfield is the "many starts" pattern; cold-start is exactly the first start. | Methodology layer: agent-shaped fit-and-finish work-unit-class declared upstream (see §6 mandate-fit). |
| **F53** Voluntary-discipline fragility | Many cold-start mitigations are voluntary-discipline-shaped (intent thinking, EARS cadence). | P5 substrate-triggered escrow harness — the *meta-mitigation* against F53 for cold-start. |
| **F59** Premature decomposition | Greenfield UC4 spec-malleability requires revisable decomposition. | Methodology: do not enforce scout/spec/build phase gates; allow re-entry to spec layer from any downstream layer (decision-seed reopening). |

### 3.2 Ashby-adequate cold-start substrate (closes F51 for the spec layer)

Per F51 (Ashby-deficient probabilistic guard, report [`25`](../../../research/25-requirements-engineering-foundations.md) §5.5): a probabilistic guard against a probabilistic agent in a high-variety environment has insufficient requisite variety. The cold-start environment *is* the highest-variety environment the factory will ever face (no prior trajectories to constrain the distribution). **Therefore the cold-start spec layer must be guarded deterministically.** This is the architectural reason P2+P3 are deterministic, not LLM-judged: at day 0, only a deterministic guard has Ashby-adequate variety. As the factory accumulates trajectory data, *probabilistic* judges become Ashby-adequate for narrower distributions; cold-start exit is partly defined by when this transition is safe.

### 3.3 Cold-start de-prioritised (matters for steady-state, not day 0)

- **F35** Federation-as-Family Drift — there is no family on day 0; severity grows over time (failure-modes-v3 §5a F35 severity rationale).
- **F47** Visible-Metric Drift / Goodhart — applies once per-operator metrics exist; absent on day 0.
- **F8** Stale knowledge inversion — no knowledge to be stale yet.
- **F11** Renumbering breaks references — applies once references exist.

These get standard substrate treatment per other tracks; this track does not specialize for them.

---

## §4 — §4 defaults: accepted vs challenged

Per D3, all seven brief §4.1 defaults marked.

### D-1. Specs are the durable, version-controlled, human-curated artifact.

**Accepted with justification.** Cold-start *requires* this — it is the only artifact that exists on day 0 (UC1 greenfield has no code yet). The cold-start architecture in §5 is built around making D-1 sustainable in the regime where the spec is also most fragile (F37/F39 bite hardest at authoring time). Justification: Nystrom's spec-git-history-as-changelog (report [`35`](../../../research/35-lenny-howiai-spec-driven-and-team-ops.md) §2) is the strongest industrial cold-start exit signal — it shows D-1 surviving the spec-malleable regime at industrial scale (Stripe 1,300 PRs/wk).

### D-2. Scenarios live outside the codebase as a holdout set.

**Challenged — with cold-start-specific replacement.** At day 0 there are no scenarios at all — neither inside nor outside any codebase, because there is no codebase. The D-2 default is silent about the cold-start regime. **Cold-start-specific replacement:** scenarios at day 0 are **bootstrap-borrowed-priors** (P4) — drawn from the operator's curated adjacent-domain corpus (UC6's "priors permitted"), from exemplar projects, or from canonical RE-domain benchmarks (HumanEval-MBPP mutation derivatives per Larbi et al. report [`26`](../../../research/26-prompt-underspecification-academic.md) §3.2). They live outside the (non-existent) codebase by construction; the substrate property D-2 names *is* preserved (acceptance criteria withheld from builders, D-4), but the *source* of the scenarios is operator-imported, not factory-generated. As factory-generated scenarios accumulate, sunset-edges (§0.1) retire bootstrap-borrowed ones. **The D-2 discipline survives day 0 by inheriting from operator-curated priors; the brief's framing under-specifies what "outside the codebase" means when there is no codebase.** This is the load-bearing cold-start adaptation of D-2.

### D-3. Agent = Model + Harness; Harness and scaffold are distinct.

**Accepted with justification, with cold-start widening.** The Agent = Model + Harness decomposition is adequate for this track's architecture (no graph-node or population shape required at the methodology layer). Widening: cold-start adds **interval** as a third harness sub-component (Kahana cognitive escrow, report [`30`](../../../research/30-cognitive-escrow.md)) — the prompt→response interval is itself harness surface, not dead time. The "Agent = Model + Harness + Natural-Language-Register" widening from CTR-C10 (report 37 Portuguese effect) is also relevant; this track does not commit but flags both widenings as substrate-vocabulary candidates Phase-4 will need to address.

### D-4. Holdout discipline is substrate-enforced, not methodology-optional.

**Accepted with justification.** Cold-start *raises* the importance of D-4: it is the only discipline that survives day 0 when judges are bootstrap-borrowed. P4 substrate registry enforces "no acceptance criteria leak into builder context." Justification: F28 holdout leakage is critical-greenfield per failure-modes-v3; cold-start makes it the single most load-bearing substrate guarantee because there is no other check on the builder's output during the cold-start window.

### D-5. Hard cost ceilings are non-optional in CI.

**Accepted with justification.** Cold-start architecturally cheap — most work is spec authoring + linting, not parallel builds — but CaMeL's measured 7-point utility tax (followup [`08`](../../../research/followup/08-security-primitives.md) §3; CTR-E6) suggests deterministic-substrate cost is non-trivial. Cold-start exit reduces the deterministic burden as probabilistic judges take over (§3.2); cost ceiling discipline carries through.

### D-6. Tiered watchdog (Daemon / Triage / Patrol) is a substrate primitive.

**Accepted with justification, with cold-start specialisation.** Patrol tier specialised: during cold-start, Patrol watches for **factory-output leakage into holdout** (sunset-edge ledger consistency) and for **escrow-interval skip rate** (operator under-engagement with reflection prompts is the F53 signature). Cold-start exit gate (§5.7) is a Patrol-tier declaration.

### D-7. Trajectory capture is cheap and production-tested.

**Accepted with justification.** Cold-start *requires* trajectory capture because there is no other signal of what happened — no codebase delta to read, no test suite to compare. Per CTR-E4, D-7 is largely resolved; this track depends on it. Cold-start widening: trajectories must carry **bootstrap-prior provenance tags** so future cycles can trace which judgments depended on which borrowed prior.

---

## §5 — Cold-start (load-bearing section)

**Brief §5.2 questions answered in order.**

### 5.1 How does a greenfield factory bootstrap on day 0?

Five-stage bootstrap, executed before the first build agent is dispatched. Each stage names which §1.2 primitives it uses and which failure modes it closes.

#### Stage 0 — Operator-curated prior import (uses P4, P7).

Operator supplies, at factory instantiation: (i) **bootstrap-borrowed scenarios** — at minimum, 20 scenarios in Kaner's 2003 scenario-testing shape (followup [`09`](../../../research/followup/09-methodology-ancestors.md)), drawn from the operator's adjacent-domain corpus or generated by Larbi et al.'s mutation engine (report [`26`](../../../research/26-prompt-underspecification-academic.md) §3.2) against a domain-canonical seed set; (ii) **bootstrap-borrowed judges** — explicit model-family identity for builder vs judge, registered in P7; cold-start mandates *cross-family* (closes F1/F27); (iii) **bootstrap-borrowed skills** — vendor skill libraries (Anthropic Agent Skills per report [`23`](../../../research/23-anthropic-engineering-trilogy.md) §3.5, Every SKILL.md per report [`04`](../../../research/04-every-skill-libraries.md)) imported as read-only substrate; (iv) **operator-curated knowledge** — the UC6 priors, tagged `bootstrap-borrowed` so future sunset-edge tracking can retire them. Stage 0 closes the day-0 "no signal" problem by importing signal.

#### Stage 1 — Intent block authoring (uses P5, P2; closes F41, F25-precursor).

Operator authors the El Kaim 9-field intent block (report [`14`](../../../research/14-el-kaim-book-intent-and-spec-authorship.md) §3, Ch3 §4.1) — Identity / Statement / Business outcomes / Capability scope / Policy references / **Invariants** / **Non-goals** / **Decision seeds** / Guardrails / Feedback sources. Per El Kaim Ch3 §5.6 mature pattern, the LLM drafts from a sponsor-interview prompt, the escrow-interval harness (P5) fires templated reflection prompts (per [`30`](../../../research/30-cognitive-escrow.md) §4 catalogue items 1, 2, 4 — reflective-question surfacing, success-criterion articulation, delegation-level confirmation) at draft completion, the operator sharpens, and the result is committed to P1 typed-spec store. The **invariants** field is load-bearing: it carries the *non-negotiable conditions* that the cold-start architecture treats as substrate-enforced (compiled to OPA/Rego per El Kaim Ch3 §5.4 Role-1) for the duration of the cold-start window.

#### Stage 2 — Deterministic spec lint pass (uses P2; closes F38, F36-pressure, partial F18).

P2 runs GtWR R7/R8/R9/R26/R35 lint (report [`25`](../../../research/25-requirements-engineering-foundations.md) §3.2) against the intent block's `statement`, `invariants`, `guardrails`, and acceptance-criteria fields; mandates one of five EARS patterns (report [`25`](../../../research/25-requirements-engineering-foundations.md) §2.2) for acceptance criteria; surfaces **specification-budget overruns** (per Yang's gpt-4o 98.7%→85.0% at 19 reqs, [`26`](../../../research/26-prompt-underspecification-academic.md) §2.4) when active-spec count exceeds ~10, prompting Yang-Bayesian background-spec partitioning (§5.4). All deterministic; zero LLM judgment in this stage. Failure here blocks Stage 3.

#### Stage 3 — Contradiction-detection pass (uses P3; closes F37).

P3 runs a deterministic + OPA/Rego pass: (i) cross-field consistency (every invariant references at least one policy; every guardrail metric maps to a feedback source — El Kaim Ch3 §5.4 Role-1); (ii) Larbi-style triangulation — paired-spec/triangulation against the bootstrap-borrowed mutation set from Stage 0 ([`26`](../../../research/26-prompt-underspecification-academic.md) §5.2 proposal); (iii) optional model-family-diversified contradiction-detector (a *separate* LLM in a different family, per P7, runs Larbi's contradiction-detection task — but its output is *informational only* and routed to escrow-interval prompt during cold-start, **not used as a gate** because MCC ≤0.55 means it would be Ashby-deficient per §3.2). Failure here returns to Stage 1 with the detected contradiction surfaced in the escrow interval.

#### Stage 4 — Complexity diagnosis + work-unit classification (uses P1; closes F39, pre-empts F59).

The spec head carries a **complexity-class field** (complicated / complex / complex-adaptive per INCOSE Complexity Primer Table 2, report [`25`](../../../research/25-requirements-engineering-foundations.md) §5.6). Cold-start default is `complex` (greenfield UC4 spec-malleability is the corpus' canonical complex-system regime); operator can downgrade with justification. The classification routes to one of three methodology pathways: complicated → waterfall-with-V&V; complex → mandatory feedback-loop instrumentation + region-of-outcome spec; complex-adaptive → continual-evolution mode (Sillitto subjective-/objective- partition, [`25`](../../../research/25-requirements-engineering-foundations.md) §5.2, drives F-mode mitigation budget). For `complex`/`complex-adaptive` the substrate **forbids point-spec acceptance criteria** — only region-spec passes Stage 4 (closes F39 at substrate). Work-unit classification per D2 happens here; cold-start architecture initial work-unit-class is *initial-spec*, transitioning to *mvp* at cold-start exit.

#### Stage 5 — First build agent dispatch (uses P6, P7, D-4 holdout).

Builder agent dispatched against the typed spec; judge from P7 (cross-family); holdout from P4 (bootstrap-borrowed). Trajectory captured per D-7. Result enters the trajectory + sunset ledger. The cold-start window remains open until §5.7 exit gates fire.

### 5.2 What priors are available?

Per UC6 brief revision ("priors permitted, not no priors"), the cold-start architecture treats *six* prior classes as substrate inputs:

1. **Domain-canonical RE/SE grammar** (EARS five patterns; INCOSE GtWR R7–R35 + C1–C15; Complexity Primer Table 2; AFIS three RE goals) — operator-independent; baked into P2.
2. **Vendor skill libraries** (Anthropic Agent Skills, Every SKILL.md, El Kaim Codex objects) — operator-selected; loaded read-only into substrate.
3. **Adjacent-domain operator corpus** (prior project specs, prior scenarios, prior judge calibrations from the operator's earlier factories) — UC6's explicit prior class.
4. **Exemplar projects** (StrongDM Attractor pipeline-as-spec per report [`02`](../../../research/02-strongdm-attractor.md); Notion Markdown-spec pattern per report [`35`](../../../research/35-lenny-howiai-spec-driven-and-team-ops.md); El Kaim 9-field intent block as the spec template itself).
5. **Academic-benchmark surfaces** (Larbi mutated HumanEval/MBPP per [`26`](../../../research/26-prompt-underspecification-academic.md) §3.2 for contradiction-detection holdouts; Yang's per-requirement validator pattern with 95.6% human agreement per §2.5).
6. **Shapiro Claw "dreaming" overnight research** (report [`32`](../../../research/32-shapiro-completion-chat-agent-claw.md) §"dreaming") — operator-configured nightly research jobs that pre-populate the bootstrap-prior store with relevant external context before the next day's cycle. *Note CTR-C9 unresolved tension* with Anthropic Skills "no network" closure; this track does not pick — the dreaming primitive is optional, off by default during cold-start to avoid F12 trifecta opening.

All six are tagged `bootstrap-borrowed` in P4; sunset-edges retire them as factory-internal equivalents accumulate.

### 5.3 How is the bootstrap protected against silent failure?

This is the hardest cold-start question. The factory has no track record yet to evaluate its own architecture against, so any silent failure during the bootstrap propagates without detection. Three layered defenses, listed in increasing trust requirement.

#### Defense 1 — Deterministic-first substrate (Ashby-adequacy, §3.2).

The substrate primitives P2 (deterministic linter) and P3 (deterministic contradiction-detector) carry the *only* Ashby-adequate variety for the cold-start regime (per §3.2). The architecture's deepest day-0 commitment is *not delegating spec-honesty to a probabilistic judge* until trajectory accumulation makes the judge's distribution observable. This closes F51 for the spec layer during the window where it is most acute.

#### Defense 2 — Cross-family judge isolation (P7) + bootstrap-borrowed holdout (P4).

For the build/verify layer that *must* use probabilistic judgment (no deterministic check exists for "does the code do what the spec says"), the substrate enforces builder/judge model-family separation (closes F1/F27/F46 single-model blindspot per report [`34`](../../../research/34-lenny-howiai-personal-harnesses.md) §6.2) and holdout-isolation from operator-imported scenarios (closes F28). Bootstrap-borrowed judges are themselves a risk class — operator might import a miscalibrated judge — but the cross-family isolation reduces the chance of *correlated* error during cold-start; Stage 0 mandates explicit judge-source documentation in the trajectory store for forensic recovery if a calibration error surfaces later.

#### Defense 3 — Escrow-interval as the residual human re-engagement surface (P5).

Per Kahana ([`30`](../../../research/30-cognitive-escrow.md) §4), the prompt→response interval is the substrate-triggered structural moment for human reflection. During cold-start, the escrow-interval harness fires (i) at intent-block draft completion (Stage 1 — reflective questions on invariants and non-goals); (ii) at contradiction-detector flag (Stage 3 — present the detected ambiguity; the human is the residual oracle for cases the MCC-≤0.55 detector cannot classify); (iii) at first-build-agent dispatch (Stage 5 — delegation-level confirmation per [`30`](../../../research/30-cognitive-escrow.md) §4 item 4). **This is not voluntary discipline** (which would be F53 fragile) — the substrate fires the prompts. The human's *response* may still be skipped under load, but the *skip* is logged; persistent skip rate is a Patrol-tier signal (§D-6 widening). This is the cold-start architecture's structural defense against the failure mode that no other layer catches: the *operator* failing to notice the factory is on a wrong track because the factory's own outputs look plausible.

#### Why three layers and not one.

Each layer has a distinct failure surface: deterministic substrate cannot judge regions of outcome-space (F39); cross-family judges share *some* training distribution and can still be circularly correlated on extreme cases (F48 tacit collusion per report [`37`](../../../research/37-academic-llm-agent-collusion.md) §8.1); escrow interval depends on the human responding (residual F53 risk). The three layers compose to make silent failure during cold-start *unlikely without all three failing in the same cycle*.

### 5.4 What is the trajectory from day 0 → day N?

Cold-start exit is **not** a switch — it is a progressive replacement of bootstrap-borrowed priors by factory-generated equivalents, tracked by sunset-edges (P6 widening) in the trajectory store.

**Trajectory phases:**

| Phase | Cycle range (illustrative) | What's borrowed | What's factory-generated | Substrate posture |
|---|---|---|---|---|
| **Cold-start (week 0)** | 0–10 | Scenarios, judges, skills, knowledge, complexity diagnosis baseline | First trajectories, first per-requirement validators, first decision-records | Deterministic-first; escrow harness on full duty; all P-primitives active |
| **Warm-start (weeks 1–4)** | 10–50 | Judges (still cross-family), some skills | Scenarios accumulating, knowledge entries (typed per Compound Knowledge four-way classification, followup [`11`](../../../research/followup/11-compound-knowledge.md)), Yang COPRO-R validators | Substrate still deterministic-first; escrow harness fires only on contradiction-detector flag |
| **Steady-state** | 50+ | Domain-canonical grammar only (EARS/GtWR baked-in) | All else | Substrate transitions to probabilistic+deterministic-hybrid; Yang background-spec partitioning lifts spec budget |

**Yang background-spec partitioning** (the specific mitigation for F36 carried across phases, per [`26`](../../../research/26-prompt-underspecification-academic.md) §2.5): when active-spec count exceeds ~10, the substrate splits requirements into *foreground* (in the active prompt) and *background* (continuously validated by background validators). Cold-start can only do this against bootstrap-borrowed validators; warm-start accumulates factory-generated background validators; steady-state can shift requirements freely. This is the single most important *cold-start-specific* methodology primitive — it converts the F36 ceiling from a hard wall to a managed surface.

### 5.5 The MISSED-3 reconciliation: El Kaim invariants vs UC4 spec-malleability

Per bias-guard MISSED-3 (uncomfortable-contradictions-audit, ref CTR-B6): El Kaim's 9-field intent block declares **invariants** as *"non-negotiable conditions that any valid realization of the intent must preserve"* — structurally upstream-stable, designed to defeat confabulation. UC4 declares greenfield **spec-malleable** — *"the system's architecture is still moving during spec refinement; commitments are reversible."* The contradiction is real and load-bearing: the deepest spec-authorship anchor in the corpus prescribes upstream stability as prerequisite for AI-driven downstream work; the user's working hypothesis makes upstream reversibility the *defining* greenfield characteristic.

**This track's resolution: split the spec into a two-velocity model.** The El Kaim 9-field intent block is *partitioned* across spec-velocity layers:

- **Slow-velocity fields (El-Kaim-invariant compatible):** `identity`, `invariants`, `non-goals`, `policy references`, `guardrails`. These are *upstream-stable* per El Kaim Ch3 §4.1. Substrate (P3) enforces immutability across cycles within a project; changes require explicit decision-record creation (El Kaim Ch6 §5 typed-object lifecycle). These compile to OPA/Rego and ground the deterministic Stage-3 check.
- **Fast-velocity fields (UC4-malleable compatible):** `statement` (prose), `business outcomes` (metric/baseline/target adjustable), `capability scope`, `decision seeds`, `feedback sources`. These move freely during cold-start spec refinement; substrate tracks the change-rate per Nystrom (spec-git-history-as-changelog per report [`35`](../../../research/35-lenny-howiai-spec-driven-and-team-ops.md)) and surfaces high-velocity drift to Patrol-tier (D-6).

**This is a real architectural commitment, not a verbal compromise.** El Kaim's slow-velocity fields close F37 (contradiction-detection has a stable upstream to check against), F39 (region-of-outcome shape declared once at invariant), F38 (the LLM-prone hedging language is forbidden from invariants by R7/R8/R9 lint), and partially F1/F27 (judges can check against a stable invariant). UC4's fast-velocity fields preserve the spec-malleability greenfield UC4 demands. **The track picks El Kaim on the slow-velocity layer and UC4 on the fast-velocity layer; both halves of the corpus's deepest tension survive.** Neither is rejected; both are respected at the layer where their evidence is strongest.

**What this implies for the architecture set.** A greenfield architecture in v3 cannot be "spec-malleable" as a single uniform property. The MISSED-3 reconciliation forces a two-velocity spec primitive into the Phase-4 substrate decision. If the user's UC4 framing is interpreted as forbidding *any* upstream stability, this track's architecture is foreclosed and the El Kaim primary anchor must be rejected. Track recommendation to lead agent: surface MISSED-3 to user as a DECISIONS-PENDING item before Phase 5 ADRs land.

### 5.6 The El-Kaim-vs-UC4 split mapped against the four required-reading sources

| Source | Contribution to cold-start |
|---|---|
| Report [`25`](../../../research/25-requirements-engineering-foundations.md) (RE/SE foundations) | EARS five patterns + GtWR R7–R35 lint as P2 deterministic substrate; Complexity Primer Table 2 routes to methodology pathway at Stage 4; AFIS strategy-3 (models-as-spec) endorsed at slow-velocity layer (compatible with Nystrom Markdown-spec-in-repo industrial anchor). |
| Report [`26`](../../../research/26-prompt-underspecification-academic.md) (prompt underspec) | F36/F37 empirical anchors set the cold-start failure cone; Yang COPRO-R/Bayesian for active/background spec partitioning (Stage 2 budget-overrun handler); Larbi mutated HumanEval/MBPP as bootstrap-borrowed contradiction-detection holdout (Stage 0/3); Larbi's per-defect Python-exception signature (Table 4) drives F4 field-failure triage during cold-start trajectory analysis. |
| Report [`30`](../../../research/30-cognitive-escrow.md) (cognitive escrow) | The interval-as-design-site is the cold-start's residual human re-engagement surface (Defense 3); Kahana's STIR-as-substrate-trigger (§3) closes F53 voluntary-discipline-fragility for the spec authoring layer; AILCCP missing-fourth-question (§2) is the governance-layer claim the cold-start architecture operationalises. |
| Report [`31`](../../../research/31-caremark-rsi-board-exposure.md) (Caremark RSI) | The three RSI failure modes (F54/F55 + self-poisoning) are *exactly* the failure surface that grows if the cold-start architecture's sunset-edge ledger is not maintained — factory output becoming the only signal is Kahana's behavioural drift. The three AILCCP controls (Human Approval Gate / sandboxing / immutable logging) map to escrow-interval (P5), build sandbox (substrate default per Anthropic Claude Code sandboxing, report [`23`](../../../research/23-anthropic-engineering-trilogy.md) §8), and D-7 trajectory capture respectively. Caremark mid-market RSI scope (cold-start factories will accumulate skill libraries that meet the three-part test) implies the cold-start architecture itself is RSI-by-definition for governance purposes and must declare so per F43. |
| Followup [`10`](../../../research/followup/10-governance.md) (governance) | Replit DB wipe (F56) anchors substrate default-off-production-scissors during cold-start; BCG Five Pillars + AILCCP map to the substrate-vs-methodology boundary the cold-start architecture proposes (Phase 4 input); Moltbook breach grounds Stage 3 contradiction-detection on missing-config blindspot (F13) as cold-start-specific. |

### 5.7 Cold-start exit gates (proposed empirical bars)

Cold-start window closes when **all** of the following hold for a contiguous window of N cycles (N≥10 candidate):

1. **Sunset-edge count ≥ K** where K = (operator-imported scenario count + bootstrap judge count + bootstrap skill count). I.e., every borrowed prior has been replaced by a factory-generated equivalent or explicitly retained-with-rationale.
2. **Larbi-RIR ≤ 30%** measured on the most recent N cycles' build outputs against the now-factory-generated holdout set. (Anchored on Larbi GPT-4 baseline RIR 24%, [`26`](../../../research/26-prompt-underspecification-academic.md) §3.3.)
3. **Escrow-interval prompt response rate ≥ 70%** (proxy for operator residual engagement; failure here means D-7 trajectory will be unreviewable post-hoc).
4. **Yang per-requirement validator agreement ≥ 95% human-LLM** on the factory-generated validators (Yang's calibration target, [`26`](../../../research/26-prompt-underspecification-academic.md) §2.5).
5. **Zero invariant-violation events in the trajectory store across the window** (El Kaim slow-velocity layer holding under load).

Gates 1–4 are measurable per cycle; gate 5 is the integrative gate. If any one fails persistently, the window stays open; the substrate stays in deterministic-first posture; bootstrap-borrowed priors stay active.

**Lead-agent decision-pending (per ADR-0005):** N=10 cycle window length and the four numeric thresholds are *track-proposed*, not anchored to a corpus measurement. The corpus does not contain a measured cold-start exit point because no corpus source has shipped a lights-out greenfield factory at cold-start. These bars should be revisited after Phase-8 lean-evaluation briefs surface empirical data.

---

## §6 — Mandate-fit YAML (per D2)

This track is greenfield-specific; brownfield cells are n/a by track scope.

```yaml
mandate-fit:
  initial-spec: greenfield     # primary work-unit-class for this track
  refactor: n/a                # not addressed by cold-start-first; refactor is a brownfield-shaped work unit
  mvp: greenfield              # cold-start exit transitions naturally into mvp work-unit-class
  post-mvp-evolution: greenfield  # supported via the sunset-edge-graduated steady state; not the focus
  regression-fix: n/a          # regression-fix presumes a stable spec; cold-start ends before this regime
```

**Justification per cell.** `initial-spec` is the load-bearing fit: the entire architecture is built around the El Kaim 9-field intent block authoring discipline, which *is* initial-spec work. `mvp` follows because Stage 4 work-unit classification transitions to mvp at cold-start exit; the architecture's substrate primitives (P1–P7) remain useful at mvp scale. `post-mvp-evolution` is supported but is not where the architecture *earns its keep* — the cold-start-specific primitives (P2 GtWR linter, P3 contradiction detector, P5 escrow harness on full duty) provide diminishing marginal return once spec-velocity slows. `refactor` and `regression-fix` are explicitly out-of-scope per track axis (cold-start-first does not address regimes with stable specs or existing code).

---

## §7 — Anticipated Phase-3 adversarial critiques and responses

### Critique A (cold-start-deniers): "Cold-start is too short to architect around."

Response: §0.2 (a) — UC1's greenfield-applications-plural framing makes cold-start *recurrent*; (b) — F36/F37 bite at every spec-additive cycle, not just day 0; (c) — F54/F55 indict architectures whose steady-state is not cold-start-shaped.

### Critique B (substrate-firsters): "P1–P7 are substrate primitives — this is a substrate track wearing a methodology mask."

Response: Accepted in part. The architecture's load-bearing decisions live at substrate (per §1.2 P1–P7). But the *methodology* is what fires when: Stages 0–5 in §5.1 are methodology, not substrate. The cold-start window itself is a methodology-tier construct (a regime declaration); the gates (§5.7) are methodology-tier. The substrate underwrites; the methodology directs. Phase 4 will need to resolve which P-primitives belong to substrate vs methodology; this track does not prejudge.

### Critique C (UC4-purists): "MISSED-3 reconciliation rejects UC4."

Response: It does *not* reject UC4. §5.5 explicitly partitions the spec: fast-velocity fields preserve UC4 spec-malleability; slow-velocity fields adopt El Kaim invariants. Both halves of the user's framing survive at the layer where their evidence is strongest. The lead-agent escalation surfaces the partition as a DECISIONS-PENDING item; the track does not unilaterally pick El Kaim over the user.

### Critique D (regime-skeptics): "L4 at spec layer + L5 below is a fudge."

Response: It is the §2.1 option (c) resolution explicitly endorsed by the brief's working stance (*"option (c) plus (b) is the most likely shape"*). The fudge is real to the extent regime classification by *layer* is corpus-novel — Shapiro's Five Levels (followup [`01`](../../../research/followup/01-shapiro-five-levels.md)) does not differentiate by layer, and Jaymin's bars apply uniformly. The corpus *should* have such a distinction — the cold-start regime forces it.

### Critique E (cost-skeptics): "Deterministic-first substrate plus escrow-interval plus two-velocity spec is expensive on day 0."

Response: Yes. UC5 explicitly de-prioritizes cost relative to accuracy ("accuracy >> speed >> tokens"). The cold-start window is also the *cheapest* part of the factory's lifecycle in absolute terms (one project, low parallelism, no production traces); paying determinism cost here is paying it when budget is most slack. Steady-state lifts the determinism cost as probabilistic judges become Ashby-adequate (§3.2).

### Critique F (single-project-deniers): "Sunset-edge ledger and bootstrap-borrowed priors assume the operator runs multiple projects. What if they run only one?"

Response: Single-project operators still benefit from Stages 0–5 (the architecture works for one cold-start), but the cross-project amortisation argument in §0.2(a) weakens. For single-project operators, the steady-state-shaped tracks (greenfield-substrate-first, greenfield-methodology-first) may be a better fit. This track is explicit that its axis is strongest under UC1 (greenfield-applications-plural) — single-project deployments are a weaker fit.

### Critique G (escrow-skeptic): "The escrow-interval harness is operator-burden in a lights-out factory."

Response: Per §2 regime treatment, the spec-authoring layer is *intentionally L4* during cold-start. The escrow-interval is the substrate-triggered structural moment for that L4 re-engagement (closes F53). For operators who genuinely want L5 spec authoring, this track's cold-start architecture is not their architecture — they should look at greenfield-substrate-first or greenfield-methodology-first, accept higher F37 risk during cold-start, and pay for it with longer cold-start windows or higher production-time correction cost.

---

## §8 — Open questions surfaced by this track

### OQ-G1 (track-local): What is the operator interface for the escrow-interval prompts during cold-start spec authoring?

The harness fires the prompts; the operator-facing UX shape is undefined. Kahana's [`30`](../../../research/30-cognitive-escrow.md) §4 catalogue items 1–6 enumerate primitives but does not commit to UI. Phase-6 architecture spec will need to.

### OQ-G2 (track-local): How does the substrate detect a bootstrap-borrowed prior is *miscalibrated* (rather than just borrowed)?

Defense 2 admits the risk; the track does not propose a mitigation beyond cross-family isolation + trajectory documentation. If a miscalibrated judge passes faulty builds during cold-start, the error surfaces only when the sunset-edge ledger's replacement is calibrated against the *same* faulty signal. Candidate mitigation: at sunset time, run the replacement against the bootstrap and require *some divergence* — pure agreement is suspicious. Not corpus-anchored.

### OQ-G3 (lifts to lead agent): MISSED-3 partition viability.

Per §5.5, the two-velocity spec primitive is the track's resolution; lead-agent confirmation of whether this is compatible with UC4's intent is required before Phase 5 ADRs.

### OQ-G4 (lifts to lead agent): Cold-start exit gates (§5.7) numeric thresholds.

N=10 window, RIR≤30%, response rate≥70%, agreement≥95%, zero invariant violations. None are corpus-anchored for the lights-out greenfield context (no corpus source has shipped one). Phase-8 lean-evaluation briefs should surface empirics; until then these are *defensible defaults*, not measured bars.

### OQ-G5 (track-local): Interaction between Shapiro's "dreaming" Claw primitive and the cold-start window.

§5.2 prior class 6 lists dreaming as optional and off-by-default during cold-start. CTR-C9 (Anthropic Skills "no network" vs Claw dreaming) is unresolved at substrate. If the substrate adopts dreaming as a cold-start prior-import accelerator, the cold-start window could close faster (more bootstrap-priors available faster) but at the cost of opening F12 lethal trifecta at the substrate boundary. Phase-4 substrate boundary will need to pick.

### OQ-G6 (track-local): Cold-start exit when the spec itself remains malleable indefinitely.

The exit gates assume convergence — sunset-edge count ≥ K presumes a finite K. UC4 spec-malleability does *not* presume convergence; some greenfield projects may legitimately keep the spec under refinement for the entire project lifetime (spec-as-product framing). In that regime, the cold-start window never closes by design. The architecture handles this gracefully (deterministic-first substrate just stays on), but it is a different operating mode than the trajectory in §5.4 assumes. Lead-agent question: is "permanent cold-start" a valid lights-out greenfield regime under UC1?

---

*End of `greenfield-cold-start-first.md`.*
