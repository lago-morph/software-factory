# C32 — LLM-as-judge Harness  (Spec, canonical track)

> Source: README §"Principle 6 — Satisfaction not test-pass" (L179–191: L181 "Probabilistic metric over
> scenario trajectories. LLM-as-judge. Boolean assertions don't survive at scale."; the 5-row table —
> "**LLM-as-judge harness** | Scores trajectories against scenarios | **Inspect AI scorer (best fit)**,
> Ragas, DeepEval | MIT/Apache 2.0 | Gas City pack"; "**Judge rubric management** | Versioned criteria |
> Inspect AI Python objects, promptfoo YAML"; "**Multi-judge ensemble** | Disagreement detection across
> judges | Inspect AI supports multiple scorers"; "**Cross-family enforcement** | Judge must be a different
> model family than coder | Custom policy on the model stylesheet"; L191 placement "Inspect AI provides the
> bulk; cross-family enforcement is configuration on the Gas City model stylesheet"); README §"Principle 5"
> (L175 "Inspect AI has the strongest **agent-trajectory model**"); README §Phase 2 (L417–442: L427 "Build
> cross-family enforcement: rule in Gas City model stylesheet — judge node must use different model family
> than coder node"; L440 "**P6** (satisfaction not test-pass): Inspect AI scorer + Gas City aggregator +
> cross-family enforcement"; L442 "the harder parts are the Inspect AI wrap and the scenario isolation
> policy"); AI-CONTEXT §1.3 (L35 "Scenarios as held-out test set — External, unread-by-agent,
> **independently judged**"); AI-CONTEXT §6.2 "Layer 2" (L294–305: L301 "LLM-as-judge | **Inspect AI
> scorer**, Ragas, DeepEval | MIT/Apache 2.0/Apache 2.0 | Mature"; L304 "Cross-family enforcement | None |
> DIY | Custom model stylesheet rule"); AI-CONTEXT §7 layer map (L373 "Inspect AI | L2: authoring + runner +
> **judge** + aggregation | MIT"); AI-CONTEXT §11 decisions (L467 "Inspect AI for Layer 2 | Yes | Most
> mature general-purpose; agent-trajectory model fits"); AI-CONTEXT §12 open questions (L514 "specific Gas
> City model stylesheet syntax for judge != coder"); AI-CONTEXT §13.3 (L582–608: the `[[rig]]` role blocks +
> the `inspect_eval` `[[tool]]` subprocess with `work_partition = "scenarios"`); F-MODE-COVERAGE §1 (F1
> "Cross-family judge enforcement (P6 component); held-out scenarios (P5)" — Addressed; F2 "Probabilistic
> satisfaction over scenario population (P6); not gate-pass" — Addressed; **F27** "Cross-family enforcement
> at judge nodes" — Addressed; **F46** "Cross-family judge ensemble (P6 component)" — Addressed; **F48**
> "Cross-family judge + independence auditor" — Partial; F39 "Inspect AI region scoring (multiple acceptable
> trajectories)" — Addressed), §6 (F33 "LLM-judge as secondary"; F51 "LLM-judge is secondary" — both gate the
> judge *behind* P4 deterministic-first); component-inventory C32 row (subsystem Evaluation & Judge; kind
> agent-role; "Scores work trajectories against scenarios; must be a different model family than coder"
> *(RELAXED to advisory per D-1; cross-family = FE-1)*;
> maps A50/A51/A52/B23; **depends on C30, C29**; gaps **G08, G20**; foundational: **yes**; Batch 3);
> review-log **D-1** (judge SAME provider/family as coder for now; cross-family → FE-1), **D-6** (canonical
> track), **D-10** (`modeldb = {id, family, cost_tier}`), **D-13** (holdout **enforcement + audit is C34**;
> **C42 provides** the partition; C32 is the **scorer, not the isolation enforcer**); the C29 spec
> (`spec/C29-model-floor-stylesheet.md` §3 — `resolveModel`/`crossFamilyRule`/`IndependenceConstraint`, the
> L0–L3 ladder, L1 Phase-0 default) and C30 spec (`spec/C30-scenario-store.md` §1 — the held-out
> Inspect-AI-`Task` corpus at `scenarios/<component>/` C32 scores against).
> Inventory ID: C32   Kind: agent-role   Status: sweep-1
> Track: canonical (faithful posture — elaborate v4 exactly; mark inferred fills `[FAITHFUL-FILL]`,
> v4 ambiguities `[AMBIGUITY: Gxx]`).

## 1. Purpose & responsibility

C32 is the factory's **LLM-as-judge harness**: the *scorer* that, given a completed (or in-progress) **work
trajectory** and the **held-out scenario** that work was meant to satisfy, produces a **satisfaction score**
— "did this trajectory satisfy the scenario?" — using an **LLM as the grader**, not boolean test assertions.
It is v4's mechanism for **Principle 6 — satisfaction not test-pass**: "Probabilistic metric over scenario
trajectories. LLM-as-judge. Boolean assertions don't survive at scale." (README:181). It serves **P5
(Ashby — requisite variety of evaluation)**: an LLM grader scoring against *regions* of acceptable behavior
gives the factory far more evaluative variety than a fixed assertion suite could, matching the variety of
the work it judges (F39 "region scoring | multiple acceptable trajectories | satisfaction distribution over
region", FM:90).

The harness is built **on the existing stack, not from scratch**: the scoring machinery is the **Inspect AI
scorer** ("LLM-as-judge harness … Inspect AI scorer (best fit)", README:185; AI-CONTEXT:301 "Mature"),
adopted as-is and exposed as a Gas City pack; the **judge model is Claude Code itself** — the *same
provider/family as the coder* for Phase 0 (review-log **D-1**), routed and constrained by **C29**. C32's own
deliverable is the thin, genuine glue the stack does not provide: **binding a trajectory + a scenario rubric
into an Inspect AI scoring run, invoking it as the judge role, and emitting a typed per-trajectory score**
for the aggregator (C33) and the holdout audit (C34).

**Responsibilities (what C32 is the spec-of-record for):**
- **Scoring one trajectory against one scenario.** Take a (trajectory, scenario) pair and produce a
  satisfaction score (the score's *shape* — scalar, label, or per-criterion vector — is fixed by the Inspect
  AI scorer's output model; C32 adopts it). The trajectory is the agent's recorded turn-DAG (CXDB, C21) /
  bead work-product; the scenario is a held-out Inspect AI `Task` (C30). C32 is "Scores trajectories against
  scenarios" verbatim (README:185, inventory C32).
- **Driving the LLM grader as the `judge` role.** C32 runs the scorer with a *judge-role* model identity it
  obtains from **C29** (`resolveModel(judge node)`), under the **independence constraint** C29 emits
  (`crossFamilyRule` / `IndependenceConstraint`). At Phase 0 that identity is **Claude Code, same provider as
  the coder** (D-1), so the judge is the *same agent family* exercised in a **separate rig with a disjoint
  rubric/role/prompt** (independence by isolation, not by family — §6, §7).
- **Rubric binding (versioned criteria).** Bind the scenario's grading criteria ("Judge rubric management |
  Versioned criteria | Inspect AI Python objects", README:186) into the scoring run. The *rubric content*
  lives with the scenario in C30's corpus; C32 owns *loading and applying it* at score time, not authoring
  it.
- **Multi-judge ensemble (disagreement signal).** Support running >1 scorer over the same trajectory and
  surfacing **disagreement** ("Multi-judge ensemble | Disagreement detection across judges | Inspect AI
  supports multiple scorers", README:187) — Inspect AI provides the multi-scorer mechanism; C32 owns the
  thin policy of *requesting N judges and emitting their disagreement* as part of the score record. This is
  the P5-Ashby variety lever and the F46 (single-model review blindspot) mitigation.
- **Emitting a typed, attributed score record.** Write each score as a structured result (per-trajectory,
  carrying the scenario id, the judge model identity + active independence level, and any ensemble
  disagreement) onto a bead / CXDB turn so **C33** can aggregate it and **C34** can audit it. v4 routes
  "judge outputs from beads" (README:426). `> [FAITHFUL-FILL]` — v4 says the aggregator reads "judge outputs
  from beads" but does not fix the per-score schema; the minimal consistent choice is *one structured score
  record per (trajectory, scenario, judge) written to a bead/CXDB turn*, attributed by C41. Concrete schema
  is sweep-2.

**Explicitly NOT (boundaries):**
- **NOT the holdout-integrity ENFORCEMENT or audit (C34) — the load-bearing boundary (D-13).** C32 is the
  *scorer, not the isolation enforcer*. It does **not** enforce that the implementer never read the
  scenarios, and it does **not** run the after-the-fact "did isolation hold?" audit ("Holdout integrity
  audit — Detects if isolation has been violated", README:173). Per **D-13**: **C34 owns** holdout-integrity
  enforcement + audit (incl. judge-independence checks under D-1); **C42 provides** the partition; C32 merely
  *consumes* its constrained judge identity and *emits* a score C34 can audit. C32 runs in the **judge rig**
  (role-isolated from the implementer; its exact partition is OQ5/OQ-C42-3); it is not the boundary policeman.
- **NOT the model router / independence policy (C29).** *Which* model the judge runs on, the floor, and the
  `family(judge) ≠ family(coder)` constraint (and its Phase-0 relaxation) are **C29's**. C32 *asks C29 for*
  the judge model + constraint and *honors* them; it does not decide them. (Inventory: C32 depends on C29.)
- **NOT the scenario store / authoring (C30).** *Where scenarios live, the DSL, the held-out repo/partition,
  day-0 signing* are **C30's**. C32 *reads* a scenario to score against; it neither authors nor stores them.
  (Inventory: C32 depends on C30.)
- **NOT the scenario runner (C31).** *Executing a scenario against the system to drive a fresh trajectory*
  (the Inspect AI runner + session-id adapter, G25) is **C31**. C32 *scores a trajectory* — it does not run
  the system under test. (C31 may invoke C32 as the scorer for a run; C32 also scores already-recorded
  trajectories from CXDB.) `> [FAITHFUL-FILL]` — Inspect AI bundles runner+scorer; v4's inventory splits
  them (C31 runner, C32 judge). Minimal consistent reading: the **scorer** half of Inspect AI is C32, the
  **runner** half is C31; they share the pack but own distinct responsibilities.
- **NOT the satisfaction-metric aggregator (C33).** Computing the *distribution* over the trajectory
  population from many judge outputs ("Satisfaction metric aggregation | Distribution over trajectory
  population", README:188) is **C33**. C32 produces the **per-trajectory** scores; C33 reduces a population
  of them. (Inventory: C33 depends on C32.)
- **NOT a deterministic boundary / primary safety guard.** v4 gates the LLM-judge *behind* P4
  deterministic-first: "Deterministic boundary typing as primary guard (P4); **LLM-judge as secondary**"
  (F33, FM:55; F51, FM:76). C32 is the **secondary, probabilistic** evaluator; it is explicitly *not* the
  last line of safety. This is a v4 invariant, not C32's choice.

## 2. Context & dependencies

| Direction | Component | Relationship |
|---|---|---|
| Depends on | **C30** Scenario store | Supplies the held-out scenario (Inspect AI `Task` + rubric) at `scenarios/<component>/` that C32 scores a trajectory against. C32 reads scenarios through the judge's role-isolated read surface (exact partition = OQ5). |
| Depends on | **C29** Model floor & stylesheet | Supplies the **judge model identity** (`resolveModel(judge node)`) and the **independence constraint** (`crossFamilyRule`/`IndependenceConstraint`, Phase-0 default `L1`, D-1). C32 honors both; it does not pick the model. |
| Reads (trajectory source) | **C21** CXDB / **C19** beads | The trajectory C32 scores is the recorded turn-DAG (CXDB) / bead work-product. `> [FAITHFUL-FILL]` — inventory names only C30/C29 as deps, but "Scores **trajectories**" requires a trajectory source; CXDB is the canonical trajectory store (inventory C21). Read-only; minimal. |
| Consumed by | **C33** Satisfaction metric aggregator | Reads C32's per-trajectory score records ("judge outputs from beads", README:426) and computes the satisfaction distribution. |
| Consumed by / audited by | **C34** Holdout integrity & audit | Audits judge-independence (D-1) and isolation after the fact (D-13). C32 emits the judge identity + active independence level into each score so C34 *can* audit; C34 owns the audit, not C32. |
| Runs inside | **C42** Rig partitioning + **C28** agent loop | The judge runs as the **judge rig** — a distinct *role* from the implementer (the `judge` role is grounded in the **inventory C42 row** "Worker/scenario/judge roles" + **spec/C42** which fixes the role set `{worker/implementer, scenario-author, judge}`; AI-CONTEXT §13.3 supplies the `scenario_authoring`/`implementer` rigs + the `inspect_eval` tool node, **not** a judge rig). The LLM grader is a Claude Code agent loop (C28) under D-1. `> [FAITHFUL-FILL]` — the judge's *partition read-surface* (own `judge` partition vs role-isolated read of `code`+scenario-outputs) is **OQ-C42-3/OQ-C34-3**, deferred (OQ5); see §6. |
| Realized over | **C17/C02** Tool-node / pack ABI | The Inspect AI scorer is exposed as a Gas City pack/tool node ("Inspect AI provides the bulk … Gas City pack", README:185,191; the `inspect_eval` `[[tool]]`, AI-CONTEXT §13.3). |
| Feeds (meta) | **C46** Meta-metrics | "judge false-positive rate" is a P12 meta-metric (README:269); C32's scores + disagreement are an input. (Downstream; not a build dep.) |

## 3. Interfaces / contracts (sweep-1: named + described)

**Inbound:**
1. **`scoreTrajectory(trajectoryRef, scenarioRef) → ScoreRecord` (primary entry).** The harness's core
   operation: given a reference to a trajectory (CXDB turn-DAG / bead) and a reference to a held-out scenario
   (Inspect AI `Task`, C30), run the Inspect AI scorer with the judge model and return a structured score.
   *Preconditions:* the scenario is resolvable through the judge's role-isolated read surface (C30/C42; the
   exact partition is OQ-C42-3, OQ5); a judge model +
   independence constraint are available from C29. *Postcondition:* exactly one `ScoreRecord` is emitted and
   persisted (to a bead/CXDB turn) for the pair, attributed (C41). Concrete signature/return schema is
   sweep-2.
2. **Judge-model + independence contract (from C29).** C32 consumes `resolveModel(judge node) →
   modelIdentity` and the emitted `IndependenceConstraint` (carrying the **active independence level**;
   Phase-0 default `L1` = same-provider judge, prompt/role/rig-isolated, D-1). C32 *honors* the constraint
   (runs the judge under the supplied identity + isolation) and *records the level* in the score; it does not
   evaluate or enforce the constraint (that audit is C34).
3. **Scenario/rubric contract (from C30).** C32 reads a scenario as an Inspect AI `Task` with versioned
   grading criteria from `scenarios/<component>/` (read-only, through the judge's role-isolated read surface;
   exact partition = OQ5). C32 binds the
   rubric into the scoring run; it does not author or mutate it.
4. **Trajectory-read contract (from C21/C19).** Read-only access to the trajectory turn-DAG / bead
   work-product to be scored.

**Outbound:**
5. **`ScoreRecord` emission (to C33 / C34).** A structured per-trajectory result written to a bead / CXDB
   turn, carrying: scenario id + version, trajectory ref, the **satisfaction score** (shape per Inspect AI
   scorer), the **judge model identity + active independence level**, and (ensemble) **disagreement**. This
   is the seam C33 aggregates and C34 audits. `> [FAITHFUL-FILL]` schema — v4 fixes only "judge outputs from
   beads" (README:426); fields above are the minimal set C33/C34/C46 need; concrete schema is sweep-2.
6. **Ensemble request (internal, optional).** A request to run N judges over the same trajectory and reduce
   to a `ScoreRecord` carrying per-judge scores + a disagreement signal ("Inspect AI supports multiple
   scorers", README:187). **The multi-scorer *execution* is Inspect AI's (off-the-shelf); C32 authors no
   ensemble engine** — only the *request* and the *disagreement field* on the record (capability-for-principle
   bar: the stack provides the mechanism). Sweep-1 names it; the reduction policy (how disagreement is
   summarized) is sweep-2.

**Invariants:**
- **I1 (secondary-guard).** C32 is the *probabilistic, secondary* evaluator; it never substitutes for the
  P4 deterministic boundary as a safety gate (F33/F51, FM:55/76). A green judge score is satisfaction
  evidence, not a safety authorization.
- **I2 (honor-don't-enforce independence).** C32 runs the judge under exactly the identity + independence
  level C29 supplies and **records** that level on every `ScoreRecord`; it performs **no** independence
  *enforcement* or *audit* (D-13 → C34). At Phase 0 the level is `L1` (same-provider, isolated by rig/role/
  prompt, D-1).
- **I3 (held-out at score time).** C32 reads the scenario only through its **role-isolated** read surface
  (the `judge` role, isolated from the implementer); it does
  not hand scenario contents back to the implementer rig. C32's *own* read is legitimate (it must see the
  scenario to grade); the guarantee that the *implementer* never saw it is C34/C42's, not C32's. *(The exact
  judge **partition** — a dedicated `judge` partition vs a role-isolated read of `code`+scenario-outputs — is
  OQ-C42-3/OQ-C34-3, deferred at OQ5; I3 asserts only the role isolation, not the partition shape.)*
- **I4 (attributed, no silent score).** Every `ScoreRecord` is attributed (C41 `created_by` = the judge
  rig/model) and recorded — there is no unlogged judgement; this is what makes "judge false-positive rate"
  (C46) and the independence audit (C34) computable.
- **I5 (one record per pair).** `scoreTrajectory` is deterministic in its *bookkeeping* (exactly one
  `ScoreRecord` per (trajectory, scenario, judge-run)); the *LLM score itself* is probabilistic — the
  population statistics (C33), not per-call determinism, are the contract (this is the point of P6).

## 4. Data model / state

C32 owns **little durable state** — it is an *agent-role/scorer*, not a store. Scenarios live in C30,
trajectories in C21/C19, the aggregated distribution in C33, the model registry in C29.

| Datum | Shape (sweep-1) | Owner | Notes |
|---|---|---|---|
| `ScoreRecord` (per trajectory) | `{scenario_id+version, trajectory_ref, score (Inspect-AI shape), judge_model_id, independence_level, disagreement?}` | C32 (emits) → persisted on bead/CXDB | The judge output C33 aggregates / C34 audits. `> [FAITHFUL-FILL]` — minimal field set; sweep-2 fixes schema. |
| Scorer pack config | Inspect AI scorer wrapped as Gas City pack/tool node (`inspect_eval`) | C02/C17 + C32 | Declarative; the Inspect AI scorer is adopted, not authored. |
| Rubric binding (transient) | the scenario `Task`'s criteria loaded for one run | C30 (content) / C32 (use) | C32 holds it only for the duration of a scoring run. |
| Judge model identity + level (transient) | from C29 per run | C29 | Recorded into the `ScoreRecord`; not owned. |

C32 is **restart-safe**: scoring is re-runnable (idempotent at the bookkeeping level, I5) because inputs
(trajectory, scenario) are durable elsewhere; a lost in-flight score is simply re-scored.

## 5. Behavior

**Scoring one trajectory (the core flow):**
1. A trajectory becomes scoreable (a build bead completes, or C31 finishes a scenario run, or a
   batch/replay requests scoring). The (trajectory, scenario) pair is the unit.
2. C32 obtains the **judge model identity + independence constraint** from C29 (`resolveModel(judge node)`;
   Phase-0 `L1`, D-1) and resolves the held-out **scenario** + rubric from C30 (judge's role-isolated read
   surface; exact partition = OQ5).
3. C32 runs the **Inspect AI scorer** with the LLM grader (Claude Code, judge rig, D-1) bound to the
   trajectory + rubric → a satisfaction score.
4. *(Ensemble, optional)* C32 runs N judges and reduces to a disagreement signal (README:187).
5. C32 emits a **`ScoreRecord`** (score + judge identity + active independence level + disagreement),
   attributed (C41), to a bead / CXDB turn → consumed by **C33** (aggregate) and auditable by **C34**.

**Degraded behavior:** if the judge model is unavailable (C29 cannot resolve / auth fails) the pair is left
*unscored* and surfaced as a bead/gate event (visible to the self-healing loop) — C32 never silently
substitutes a fabricated score (I4). If a single judge in an ensemble fails, C32 emits the partial ensemble
with reduced N and flags it (the disagreement/N is part of the record). If the scenario is unresolvable in
the partition, scoring fails closed (no score) rather than reaching outside its role-isolated read surface
(I3; exact partition = OQ5).

Sequence/state diagrams and the ensemble-reduction algorithm are **sweep-2/3**; this sweep fixes the named
flow + invariants.

## 6. Failure modes & handling

| F-mode | Source | C32's role | Status per v4 |
|---|---|---|---|
| **F2** Reward hacking | FM:18 | C32 produces a *probabilistic satisfaction* score over the scenario population (P6), not a gate-pass — the thing that makes reward-hacking harder | Addressed |
| **F1** Hallucination loop | FM:17 | At Phase 0 the guard is the **judge-independence policy at `L1`** (prompt/role/rig-isolated same-provider judge, D-1) scoring against held-out scenarios; cross-family strengthening is FE-1 | Addressed at v4 level; Phase-0 mechanism = L1 isolation |
| **F27** Circularity / same-model build+validate | FM:21 | Phase-0 guard (D-1) is **rig/role/prompt isolation** of the same-provider judge; the cross-provider strengthening is **FE-1** | Addressed at Phase-0 isolation level (isolation bounds *context* sharing, not *distribution* sharing; the distribution-sharing residual → F48/FE-1; cross-provider = FE-1) |
| **F46** Single-model review blindspot | FM:24 | The **multi-judge ensemble** (disagreement detection) is C32's variety lever (P5-Ashby); the *cross-family* ensemble is FE-1 | Partial at Phase-0 (full cross-family = FE-1); ensemble surfaces disagreement now |
| **F48** Tacit collusion via shared context | FM:25 | Cross-family judge + independence auditor; v4 marks **Partial** (shared training-distribution residual). Under D-1 the same-provider judge *shares* that distribution — residual is larger pre-FE-1, mitigated only by rig/role/prompt isolation | Partial (residual acknowledged; see §9) |
| **F39** Point-spec / region-mismatch | FM:90 | Inspect AI **region scoring** (multiple acceptable trajectories) → satisfaction *distribution over a region*, not a single point | Addressed |
| **F33** Adversarial-prompt defeat of LLM-judge | FM:55 | C32 is the **secondary** guard *behind* P4 deterministic boundary typing; twins remove the deploy-to-prod vector | Addressed (C32 is secondary by design, I1) |
| **F51** Ashby-deficient probabilistic guard | FM:76 | P4 deterministic-first is primary; **LLM-judge is secondary** — C32 must not be the sole guard | Addressed (I1) |

**Gap handling (G08 + G20) — RESOLVED by D-1, deferred to FE-1:**

> [AMBIGUITY: G08 — RESOLVED by D-1/FE-1] **"Model family" is undefined / "judge must be a different family
> than coder".** Reading (a): *family = provider* (Anthropic vs OpenAI vs Google) — the literal README:189
> reading, which implies a **second provider/API key** that AI-CONTEXT §4.1 says Max does not issue. Reading
> (b): *family = training-lineage within a provider*, so a Claude-judge scoring Claude-coder work is allowed.
> The two readings sit in tension because F27/F46/F48 want validator-from-builder independence while the Max
> floor forbids a second provider. **The integrator's ruling D-1 resolves it (the canonical track does not
> relitigate):** the **Phase-0 baseline is the same-provider judge** — effectively reading (b) — with
> independence supplied by **rig partitioning (C42) + role/prompt isolation**, not model-family diversity.
> The inventory's "**must be a different model family**" line is therefore **RELAXED to advisory** for the
> canonical track; cross-family judging is **future enhancement FE-1**. **C32's Phase-0 path:** run the
> Inspect AI scorer with a **Claude Code judge in the `judge` rig** (a distinct *role* from the coder —
> grounded in the inventory C42 row + spec/C42, **not** AI-CONTEXT §13.3, which names only
> `scenario_authoring`/`implementer`), scoring against held-out
> scenarios, under a **disjoint rubric/role/prompt** from the coder, recording the active independence level
> (`L1`) on each `ScoreRecord`. *(The judge's exact **partition** read-surface — a dedicated `judge`
> partition vs a role-isolated read of `code`+scenario-outputs — is the joint open question OQ-C42-3/OQ-C34-3,
> deferred at OQ5; C32 asserts the role/prompt isolation, not the partition shape.)* C32 builds **no
> cross-family/independent-judge machinery** and assumes **no second-provider credential** — both are FE-1.

> [G20 — RESOLVED by D-1/FE-1] **The judge model is unsourced.** v4 names no non-Claude provider, budget, or
> auth path (G20). Per **D-1** this is **no longer a Phase-0 blocker**: Phase 0 runs the **same-provider
> judge** (Claude Code), so **no second-provider credential is required** to stand up C32 and the evaluation
> tier. C29 already supplies the (Phase-0) judge identity via `resolveModel`; C32 consumes it. Sourcing a
> second family/provider, its budget, and its auth path are **FE-1**, revisited when a second-provider
> credential exists or same-family judge bias is measured as material (the residual flagged under F48/§9).

**The independence story (per D-1/D-13), explicitly:** at Phase 0 the judge's independence from the coder is
**structural, not family-based** — (i) the **`judge` rig** — a distinct *role* C42 provides and C34
enforces/audits (D-13); whether the judge gets *its own* partition or a role-isolated read of
`code`+scenario-outputs is OQ-C42-3/OQ-C34-3 (deferred, OQ5) — and (ii) a **disjoint role/prompt/rubric** so
the judge is not the coder's own context re-scoring itself. C32's contribution is to *run inside that isolation and stamp the active level
onto every score*; the *enforcement and after-the-fact audit* of the isolation (and of judge-independence
under D-1) are **C34's** (D-13), not C32's.

**Other detection/recovery:** judge-unavailable / auth failure / partition-miss are surfaced as bead/gate
events (visible to the C36–C39 self-healing loop), never as silent or fabricated scores (I4).

## 7. Cross-cutting

- **Security / isolation.** C32 runs in the **judge rig** — a distinct *role* from the implementer (the
  `judge` role is grounded in the inventory C42 row + spec/C42; AI-CONTEXT §13.3 supplies the
  `scenario_authoring`/`implementer` rigs + the `inspect_eval` tool node, not a judge rig — and the judge's
  exact *partition* read-surface is OQ-C42-3/OQ-C34-3, deferred, OQ5). It
  reads scenarios (it must, to grade) but never returns scenario contents to the implementer rig (I3). The
  isolation *enforcement + audit* is C34's (D-13). The judge's Claude Code auth is the same Max-OAuth path
  as C28 (no separate credential at Phase 0, D-1); a second-family judge credential is FE-1 + G37 (secrets,
  deferred to C03).
- **Cost (G32).** v4's only anchor is "$200/month Max" (AI-CONTEXT §4.1) and there is **no cost model** for
  scenario-suite scoring, multi-judge ensembles, or (future) second-family judge tokens. "judge
  false-positive rate" is a P12 meta-metric (README:269) C32 feeds, but **cost-per-satisfaction is C46's**;
  deferred here (G32, noted not resolved — §9). At Phase 0, judge calls consume the *same* single Max seat as
  the coder, so judge volume competes with build volume for the shared seat ceiling (cf. C28 G13/G34) —
  flagged.
- **Scale.** Same single-seat throughput ceiling as the coder (the judge is the same provider, D-1); ensemble
  judging multiplies judge calls per trajectory. Quantification is unmodeled in v4 (shared root with C28
  G13/G34); deferred.
- **Observability.** Every `ScoreRecord` is attributed (C41) and recorded (bead/CXDB) — the judge's own
  trajectory is itself captured by the C25→C27 telemetry tier (the judge is a Claude Code loop). This is what
  makes the independence audit (C34) and judge-FP-rate meta-metric (C46) computable.
- **Ops.** The scorer is adopted off-the-shelf (Inspect AI) and exposed declaratively as a Gas City pack
  (C02/C17), no Go fork; rubrics are versioned with the scenario corpus (C30).

## 8. Acceptance criteria & test strategy (sweep-1, high level)

- **AC1 (scores a trajectory against a scenario).** Given a recorded trajectory and a held-out Inspect AI
  scenario, `scoreTrajectory` runs the Inspect AI scorer with the judge model and emits exactly one
  attributed `ScoreRecord` for the pair (README:185; inventory C32). *Test:* one (trajectory, scenario) pair
  → one persisted, attributed score consumable by C33.
- **AC2 (same-provider judge, Phase-0/D-1).** The judge runs as a **Claude Code agent in the `judge` rig**
  (a distinct *role*) with a **disjoint rubric/role/prompt** from the coder, **without** any second-provider
  credential; each `ScoreRecord` records the active independence level (`L1`). *Test:* a same-provider judge
  with a distinct *role* + rubric scores successfully; the record stamps level `L1`. *(The literal
  cross-family/ cross-provider judge test belongs to FE-1, not this sweep. The judge's exact **partition**
  read-surface is OQ5/OQ-C42-3 — AC2 asserts role/prompt isolation, not the partition shape.)*
- **AC3 (probabilistic, not gate-pass).** C32 emits a satisfaction *score* (Inspect AI shape over a region),
  not a boolean test result; a population of scores is reducible by C33 to a distribution (P6, F2/F39).
  *Test:* scoring multiple trajectories for one scenario yields a score *distribution*, not a single pass/
  fail.
- **AC4 (multi-judge disagreement).** Running N judges over the same trajectory produces a `ScoreRecord`
  carrying per-judge scores + a disagreement signal (README:187; F46). *Test:* N≥2 judges → disagreement
  surfaced in the record.
- **AC5 (secondary-guard).** C32 never acts as a deterministic safety gate; its score is satisfaction
  evidence subordinate to the P4 boundary (I1; F33/F51). *Test:* a green judge score does not authorize a
  deploy that the deterministic boundary (C43/P4) would block.
- **AC6 (honor, don't enforce, independence).** C32 honors C29's independence constraint and records the
  level, but runs **no** independence audit/enforcement (D-13 → C34). *Test:* C32 emits the level on the
  record; the *audit* of independence is exercised in C34's suite, not C32's.
- **AC7 (no silent score).** Judge-unavailable / partition-miss leaves the pair unscored + surfaced as a
  bead/gate event; no fabricated score is ever emitted (I4). *Test:* induce judge auth failure → no
  `ScoreRecord`, a gate event instead.

Concrete `ScoreRecord` schema, the Inspect-AI-scorer wiring, the ensemble-reduction policy, and
judge-FP-rate test fixtures are **sweep-2**.

## 9. Open questions (→ review-log)

- **OQ1 (G08/G20 → FE-1, top).** Same-family judge **bias residual**: under D-1 the Phase-0 judge shares the
  coder's training distribution, so F48 (tacit collusion via shared context) stays **Partial** — rig/role/
  prompt isolation bounds *context* sharing but not *distribution* sharing. *When* does same-family judge
  bias become material enough to trigger FE-1 (cross-family judging), and what measurement (e.g. judge-FP-rate
  via C46, or a calibration scenario set) makes that call? *This is the deferred-not-resolved edge of D-1.*
- **OQ2 (score schema seam).** v4 fixes only "judge outputs from beads" (README:426). The concrete
  `ScoreRecord` schema is the contract C33 (aggregate), C34 (audit), and C46 (judge-FP-rate) all bind to —
  it must be frozen early (sweep-2) so those three can build against it in parallel. `[FAITHFUL-FILL]` here;
  needs a canonical schema ruling.
- **OQ3 (cost/throughput, shared with C28 G13/G34, G32).** No token-budget/cost model exists for
  judge-suite + ensemble scoring on the **single Phase-0 Max seat** the judge shares with the coder. Ensemble
  judging multiplies judge calls; v4 gives no numbers. Needs quantification (→ C46) before throughput claims
  hold.
- **OQ4 (runner↔scorer split).** Inspect AI bundles runner+scorer but v4's inventory splits them (C31 runner,
  C32 judge). The exact seam — does C31 *invoke* C32 as the scorer, or does C32 score post-hoc from CXDB, or
  both? — is `[FAITHFUL-FILL]`; confirm the C31↔C32 contract at sweep-2 (overlaps C31).
- **OQ5 (judge partition read-surface — `DEFERRED — needs orchestrator decision`).** The judge *role* is
  grounded (inventory C42 row "Worker/scenario/judge roles" + spec/C42's role set), but the judge's exact
  **partition** — a dedicated `judge` partition vs a role-isolated read of `code`+scenario-outputs — is **not**
  settled by v4 and is the **joint open question OQ-C42-3 + OQ-C34-3**. AI-CONTEXT §13.3 names only the
  `scenario_authoring`/`implementer` rigs (+ the `inspect_eval` tool), **not** a judge rig; it is therefore
  not the source for the judge partition. C32 must not pre-decide this — it asserts only the judge's *role/
  prompt isolation* and defers the partition shape to the C42/C34 joint ruling. (Resolving it pins how I3 and
  AC2 read at sweep-2.)
