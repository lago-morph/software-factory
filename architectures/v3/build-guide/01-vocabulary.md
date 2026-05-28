# 01 — Vocabulary

The v3 pipeline invented its own terminology for concepts that already have widely-used names in the corpus you've read (Shapiro, El Kaim, Willison, the StrongDM Factory docs, the 2389-research projects, Vincent, Yegge, the every.to compound-engineering writers). This file fixes that. The rest of the build guide uses the corpus names.

## Terms used in this guide

These are the building blocks. Every candidate description in `04-candidates.md` is composed of these.

### About the paradigm

- **Dark factory** — the destination: a system that turns specs into working software with humans neither writing nor reading the code in between. Name from Fanuc's lights-off robot factory. The term refers to the *paradigm*, not a product.
- **Five Levels** — Shapiro's maturity model (NHTSA-style): 0 manual, 1 intern, 2 pair-programmer, 3 human-in-loop diff-reviewer, 4 PM-mode-with-specs, 5 dark. Most v3 candidates aim at level 4 or 5.
- **Attractor** — the name (from dynamical systems) for the convergent pipeline pattern: a system that evolves toward a stable shape regardless of where it starts. StrongDM published it as a spec; multiple independent runners (Kilroy, Mammoth, Smasher, Tracker, dotpowers, Fabro) implement it. The implementations independently converge on the same three-layer architecture.

### About the architecture

- **Three-layer architecture** — the convergent shape: (1) **LLM client** (model-provider abstraction), (2) **agent loop** (reasoning core with tool dispatch), (3) **pipeline engine** (DOT-graph runner with checkpoints and gates). Every working Attractor implementation lands here.
- **Pipeline file** — the DOT graph that defines the workflow. Nodes = stages (tool node or LLM node), edges = control flow, hexagons (in Fabro's convention) = HITL gates. The pipeline file is the architectural document; the runner is commodity.
- **Tool node** vs. **LLM node** — deterministic shell command vs. model call. Mature pipelines mix both; tool nodes are cheap and reproducible, LLM nodes are expensive and nondeterministic. Use models only where reasoning is required.
- **HITL gate** — a node that pauses for human approval before proceeding. Often drawn as a hexagon. The lower the count, the closer to level 5.

### About specs and validation

- **Spec** — natural-language description of what should exist, precise enough for autonomous implementation. In the dark-factory paradigm, the spec is the source of truth; code is disposable.
- **Scenario** — an end-to-end behavioral test stored *outside the codebase*, written in natural language, evaluated by an independent LLM judge. Scenarios are the holdout set; the codebase is the model; the satisfaction rate is the validation loss. This is the load-bearing idea that makes no-review development defensible.
- **Holdout set** — the collection of scenarios the agent cannot read during work. Direct ML analogy, not metaphor — same reward-hacking dynamics, same external-evaluation solution.
- **LLM judge** — a separate model that scores whether a trajectory satisfied the scenario's intent. Multi-model judge ensembles are standard for high-stakes calls.
- **Satisfaction** — the probabilistic metric: of all observed trajectories through all scenarios, what fraction likely satisfy the user? Replaces binary "did the tests pass." Harder to game.
- **DTU (Digital Twin Universe)** — behavioral clones of external dependencies (SaaS APIs, infrastructure services), built to match the SDK's view of the service. Lets scenarios run thousands per hour without hitting rate limits or production. Building one is a pipeline task, not a project.

### About memory and observability

- **CXDB-style content-addressed DAG** — observability layer that stores every agent interaction (prompts, tool outputs, model responses) in an immutable graph. Lets you trace, replay, and query any past behavior. StrongDM's CXDB is the reference implementation (~30k LOC, OSS).
- **Work ledger** — a persistent dependency-aware task graph that survives across agent sessions. Replaces flat markdown scratchpads. Beads is the reference implementation.
- **Pyramid summaries** — multi-zoom-level representations of a large artifact (one-sentence, paragraph, section, full). Agent navigates between zoom levels. Reversible — agent can always expand back to full detail. Makes large codebases tractable for finite context windows.
- **Filesystem as memory** — a related technique: directories, indexes, and on-disk state become persistent memory that survives context window limits. A well-organized repo is an interface agents can navigate.

### About attribution and self-healing

- **Attribution** — every commit, task, and event carries an actor identity (`gastown/polecats/toast`, e.g.). Foundation for debugging, performance management, compliance. Gas Town/Gas City's design centers this.
- **Self-healing loop** — the closed loop where observability (CXDB) feeds anomaly detection, anomaly detection produces diagnoses, diagnoses become agent-driven fix tasks, and the loop runs without human intervention. StrongDM's "Healer" pattern. The thing that makes the factory continuous rather than batch.

### About techniques

- **Gene transfusion** — applying a working pattern from one codebase to another by pointing the agent at a concrete exemplar and asking it to reproduce the behavior, instead of describing the pattern from scratch. Reliable in ways that from-scratch description is not.
- **Shift work** — interactive clarification (day shift) followed by autonomous execution (night shift). Once intent is complete, agents run end-to-end without back-and-forth.
- **Semport (semantic port)** — code migration that preserves behavioral intent rather than syntax. Agent understands the purpose and reimplements in the target language. Makes 200k-line ports tractable.
- **Dorodango** — Jesse Vincent's name for the discipline of iterative polishing: spec carefully, hand to agent, polish what comes out, throw away when fundamentally wrong, rebuild from spec. Named after the Japanese art of polishing a mud ball into a high-gloss sphere.
- **Multi-model review** — same artifact critiqued by N independent models; synthesis node resolves disagreements. Catches errors any single model passes. Standard pattern for high-stakes decisions.
- **Model stylesheet** — CSS-like syntax for routing pipeline nodes to different models. Cheap models for cheap tasks; frontier models for critical steps. Cost-aware autonomous operation. Fabro's distinctive feature; conceptually applicable everywhere.

## Translation table: v3-pipeline jargon → plain name

The v3 pipeline invented terms. Most of them mean things the corpus already named.

| v3 pipeline term | Plain name from the corpus |
|---|---|
| paraphrase divergence | multi-model review (N independent paraphrasers as the F37 contradictory-prompt defense) |
| paraphrase divergence primitive (P-21) | LiteLLM-style cross-family router + sentence-transformer divergence metric |
| knowledge promotion | pattern library / accumulated solutions (Compound Atelier convention) |
| Compound-Knowledge envelope | typed knowledge artifact (4-token enum: insight / playbook / correction / pattern) |
| dispatcher regime | work-router (per-task or per-region routing to different methodologies/models) |
| substrate-typed holdout | scenarios as holdout sets (external store, OPA-mediated access) |
| trajectory capture (P-05) | CXDB-style content-addressed DAG |
| Patrol-tier watchdog | self-healing-loop observer (Healer pattern) |
| Daemon / Triage / Patrol tiers | three watchdog tiers: mechanical / AI-triage / agent-monitor (Overstory's pattern) |
| cognitive escrow | "ask why am I doing this" discipline (operator reflection at decision boundaries) |
| silent-absorption auditor | citation-gap audit (did we accidentally copy archive content without saying so?) |
| reversibility primitive (P-20) | event-sourced storage with cheap commit-and-reverse |
| Intent Crucible | structured-intent schema (typed-object intake with EARS lint) |
| Cold-Start Bench | signed scenario store (HMAC-signed initial scenario set) |
| Compound-Engineering 4-step loop | plan → work → review → compound (the every.to / Klaassen pattern) |
| trifecta closure | holdout + perimeter + judge separation (CaMeL-class boundary discipline) |
| scoping discipline | work-unit boundary enforcement |
| GtWR linter | INCOSE rules R7-R35 (publicly specified requirements-engineering lint) |
| 4-guard mediator (P-15) | ensemble of deterministic guards: lint + contradiction-detector + budgeter + perimeter type-checker |
| pace-layer (Brier) | 5-layer artifact stack (L0 standards / L1 architecture / L2 spec / L3 plan / L4 code) |
| Falsification Commitment (FC) | opposing-side declaration (which adversary tries to refute the artifact before it compounds forward) |
| anchor (U-C) | frozen reference point a work unit is parameterized against |
| Codebase Model (BF-L) | a 6-view queryable index of a legacy codebase (structural / conventional / historical / runtime / invariant / debt) |
| Pulse report | production-trace-to-spec-amendment (close-the-loop event from prod back into the work ledger) |

## What this guide does not rename

A few v3-pipeline terms have no clean corpus equivalent and stay as-is:

- **Mandate scope** (greenfield / brownfield / unified-attempt) — the v3 pipeline's own framing for whether a candidate addresses new-system construction, legacy intervention, or both. Useful distinction, no corpus collision.
- **F-modes** (F1-F58, CTR-A1 through CTR-G3) — the v3 catalog of failure modes and contradictions. The numbers are stable references; the underlying failures often have corpus-standard names too (e.g., F37 = "silent contradictory-prompt collapse" = the Larbi MCC-on-single-judge failure).
- **DEC-1.a** — the v3 working hypothesis "no methodology serves both mandates." Pipeline-internal framing.
- **Candidate IDs** (GF-S, GF-M, GF-C, BF-S, BF-M, BF-L, U-A, U-B, U-C, D7-U-1) — the v3 enumeration. Stable references; this guide uses them.

## What this guide does opinionatedly

When the corpus has multiple competing terms for the same concept (e.g., "compound engineering" vs. "attractor" vs. "spec refinery"), I pick one and put the alternatives in this glossary. The picks are noted; you can override them.

| Concept | This guide uses | Other names you'll see |
|---|---|---|
| The convergent pipeline pattern | **Attractor** | Compound engineering pipeline, dot-file workflow |
| The continuous fix loop | **Self-healing loop** | Healer, autonomous remediation |
| External behavioral test | **Scenario** | Holdout test, behavioral spec, evaluation case |
| The artifact that defines what to build | **Spec** | Pipeline file (when it's specifically the DOT graph), intent, ADR |
| Per-cycle review by a different model than wrote it | **Cross-model review** | Bias guard, multi-model judge, opposing-side panel |

The picks lean toward what's been adopted most widely in the corpus (Shapiro/Willison/El Kaim consistency) and what's most concrete for an engineer.
