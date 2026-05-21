# Gas City and Gas Town as Execution Substrate for Dark Factory and Compound Engineering

**Date:** 2026-05-20
**Type:** Synthesis report (cross-source, ecosystem-mapping)
**Sources covered:**

- `https://github.com/gastownhall/gascity` — ✅ FULL (cloned to `/tmp/gascity`, ~49 MB, ~2,300 files, post-`v1.0.0`, commit `183897e`). Analyzed in [`13-gas-city-deep-dive`](followup/13-gas-city-deep-dive.md).
- `https://github.com/gastownhall/gastown` — ✅ FULL (cloned to `/tmp/gastown`, ~30 MB, ~1,500 files). Analyzed in [`14-gas-town-deep-dive`](followup/14-gas-town-deep-dive.md).
- `https://docs.gascityhall.com` — ❌ HTTP 403 from sandbox. The site is the Mintlify projection of `gascity/docs/`; analysis works from the in-repo source directly.
- Prior corpus reports re-used for the mapping axes: [`01-strongdm-factory`](01-strongdm-factory.md), [`02-strongdm-attractor`](02-strongdm-attractor.md), [`03-every-compound-engineering`](03-every-compound-engineering.md), [`07-dark-factory`](07-dark-factory.md), [`04-gastown-beads`](followup/04-gastown-beads.md).

**Audience:** the parent project's synthesis layer (which is sizing up candidate execution substrates for its four candidate factory architectures), plus any AI session being asked "can I run X on Gas City/Town?" where X is a specific software-factory discipline. The companion deep-dives at `followup/13` and `followup/14` are the verbatim reference; this report is the *mapping* and the *deployment sketch*.

---

## Executive summary

Gas Town and Gas City are sibling Go-based multi-agent orchestration systems from the `gastownhall` GitHub organization. They are **two stacked layers of the same problem**:

- **Gas Town** (Steve Yegge, repository active since mid-2025) is a **workspace operating system** for a fleet of LLM coding agents — a single Go binary `gt` that builds a multi-agent town around a tmux session manager, a per-town Dolt SQL server holding the Beads issue graph, and a hard-coded role taxonomy (Mayor, Deacon, Boot, Witness, Refinery, Polecat, Crew, Dogs, Overseer). It is the canonical existence-proof for "one human, 20–30 agents" workspace operation, named in El Kaim's "Dark Factory" essay as the **attribution and orchestration layer** of the ecosystem ([`07-dark-factory`](07-dark-factory.md)).
- **Gas City** is the **orchestration-builder SDK extracted from Gas Town**. The single Go binary `gc` exposes a small, opinionated primitive set — five irreducible primitives (Session, Beads, Event Bus, Config, Prompt Templates) plus four derived mechanisms (Messaging, Formulas/Molecules, Dispatch/Sling, Health Patrol) — with **zero hardcoded role names in Go**. Gas Town becomes one of many possible *packs* you can run on the substrate. The repo's `AGENTS.md:1-18` is unambiguous: *"You can build Gas Town in Gas City, or Ralph, or Claude Code Agent Teams, or any other orchestration pack — via specific configurations."*

This split — **substrate (Gas City) versus canonical application (Gas Town)** — is the architectural fact that makes both systems interesting as execution substrates for higher-level methodologies. The StrongDM "Dark Factory" methodology ([`07-dark-factory`](07-dark-factory.md)) and the Every.to "Compound Engineering" methodology ([`03-every-compound-engineering`](03-every-compound-engineering.md)) are both **methodologies**, not products. Each names a set of disciplines (scenarios as holdout sets, satisfaction as the metric, Plan→Work→Review→Compound loop, etc.) and a thin set of structural artifacts (DOT pipelines, `CLAUDE.md`, `docs/solutions/`, review-agent panels). Neither methodology ships an *operating runtime*. Gas City is the strongest candidate runtime in the corpus for both, because:

1. Its primitives are **role-agnostic** — neither methodology can be forced into Gas Town's specific Mayor/Polecat shape, but both can be built as packs on Gas City. The "Permanent Exclusions" in `gascity/AGENTS.md:221-229` — no skills system, no capability flags, no decision logic in Go, no hardcoded roles — are not absences; they are guarantees.
2. The four derived mechanisms (Messaging, Formulas/Molecules, Dispatch, Health Patrol) cover the orchestration surface area each methodology needs: scheduled and event-triggered execution (Orders), DAG fan-out and fan-in (Sling + Convoy + Molecule + Dispatch), durable agent-to-agent communication (Mail), and continuous reconciliation of desired-vs-running state (Controller + Health Patrol).
3. Workflow is *configuration*. A DOT pipeline (Attractor-style) becomes a Gas City formula chain. A 14-agent review panel (Compound Engineering) becomes 14 generic agents each with their own prompt template plus a parallel-fanout convoy. Both methodologies become deployable artifacts that ship as packs.

The gaps — and there are real ones — concentrate around three things: (a) Gas City does not yet ship a pluggable LLM-as-judge primitive, which both methodologies depend on; (b) the formula DAG is currently single-rig and lacks the cross-stage Context-passing fidelity model Attractor enforces; and (c) the scenario-as-holdout discipline is a methodology requirement that Gas City can store but not enforce at the engine level. These gaps are bridgeable as Order-driven extensions plus convention-on-top-of-Beads, but they are real engineering work, not configuration choices.

The remainder of this report:

- §1 sketches what Gas Town is, what Gas City is, and how they relate. (Skim if `followup/13` and `followup/14` have been read.)
- §2 maps Gas systems' primitives onto the StrongDM Dark Factory primitive set.
- §3 maps the same primitives onto the Every.to Compound Engineering primitive set.
- §4 is a concrete deployment sketch for "running the Dark Factory on Gas City."
- §5 is a concrete deployment sketch for "running Compound Engineering on Gas City + the Gastown pack."
- §6 enumerates the gaps each deployment must close before it is operational.
- §7 lists the open questions.

---

## 1. What Gas Town and Gas City are

### 1.1 Gas Town in one page

Gas Town is a fleet-management OS for AI coding agents that scales the 1-human / 20–30-agent regime. Its load-bearing claim, verbatim from `gastown/README.md`:

| Challenge                       | Gas Town Solution                            |
| ------------------------------- | -------------------------------------------- |
| Agents lose context on restart  | Work persists in git-backed hooks            |
| Manual agent coordination       | Built-in mailboxes, identities, and handoffs |
| 4-10 agents become chaotic      | Scale comfortably to 20-30 agents            |
| Work state lost in agent memory | Work state stored in Beads ledger            |

The shape is an **opinionated org chart in software**:

- A workspace root `~/gt/` (a *town*) hosts multiple *rigs* (project containers wrapping git repositories).
- A persistent **Mayor** session (Claude Code by default) is the human's primary interface — "*just tell the Mayor what you want to accomplish.*"
- The Mayor decomposes intent into **Convoys** (bundles of Beads), dispatches them via `gt sling` to **Polecats** (worker agents with persistent identity but ephemeral sessions), and routes blockers via `gt escalate` through a severity-tiered chain (Deacon → Mayor → Overseer).
- **Witness** (per-rig lifecycle manager) and **Deacon** (cross-rig daemon supervisor) watch agent health continuously, with **Boot** as the watchdog-of-the-watchdog (Deacon's watchdog) and **Dogs** as ephemeral cross-rig maintenance workers.
- A **Refinery** runs a Bors-style bisecting merge queue per rig — Polecats never push to `main` directly; they call `gt done`, which pushes a feature branch and creates an MR bead that the Refinery batches, verifies, and merges (or bisects on failure).
- All durable work is a **Bead** (typed graph node) stored in a per-town **Dolt SQL Server** with cell-level merge semantics, with `routes.jsonl` mapping bead-ID prefixes to rig databases (`hq-` → town beads, `gt-` → gastown rig beads, etc.). The two-level beads architecture (`gastown/docs/design/architecture.md:1-30`) cleanly separates *organizational coordination* (`hq-*` in `~/gt/.beads/`) from *project implementation* (`<prefix>-*` in `<rig>/mayor/rig/.beads/`).
- Federation across orgs is **Wasteland** — a DoltHub-backed inter-town network with portable reputation stamps (`gt wl claim`, `gt wl done --evidence`).

The 13 currently-shipped **plugins** (`gastown/plugins/`) — `compactor-dog`, `dolt-archive`, `dolt-backup`, `dolt-log-rotate`, `dolt-snapshots`, `git-hygiene`, `github-sheriff`, `gitignore-reconcile`, `quality-review`, `rebuild-gt`, `stuck-agent-dog`, `submodule-commit`, `tool-updater` — are mostly deterministic Dog-shaped maintenance workers (with one AI-driven quality reviewer). They are the existence-proof that **a Dog is usually better expressed as an exec script than as an LLM session**, a principle Gas City has formalized into the Order primitive (§1.3 below).

Communication is layered: **mail** (durable bead-typed messages, persistent across restarts), **nudge** (immediate fire-and-forget text injection into a live session), **seance** (predecessor-session discovery — `gt seance --talk <id>` queries a prior session's `.events.jsonl` log for context), **escalate** (severity-tiered routing of blockers via the Deacon→Mayor→Overseer chain), and the experimental **ACP** ("Agent Coordination Protocol") for typed mid-loop steering. Observability is OTEL-native (the README documents `gastown.session.starts.total`, `gastown.bd.calls.total`, etc.) with a `gt feed` TUI dashboard and a `gt dashboard` web UI that auto-refreshes via htmx and exposes a browser command palette.

Read [`14-gas-town-deep-dive`](followup/14-gas-town-deep-dive.md) for the full ~9,300-word reference — including the role taxonomy in §2, the state model in §3, the lifecycle-hook layering, the `gt-proxy-server` mTLS sandboxing model (containerized polecat isolation, NOT LLM routing as the prior comparison report assumed), the `gt-model-eval/` promptfoo harness for downgrading patrol-agent models, the 13-plugin contract, the OTEL data model, the Wasteland reputation/yearbook system, and CHANGELOG architectural milestones (v0.8.0 brought OTEL + Scheduler + Wasteland + Dog; v0.9.0 brought persistent polecats and the Bors merge queue; v1.0.0 brought Windows + PR merge strategies).

### 1.2 Gas City in one page

Gas City is the **orchestration-builder SDK** Gas Town's reusable infrastructure was extracted into. The README's positioning is direct: *"Composable orchestration infrastructure for multi-agent coding workflows."* The product slogan from `gascity/AGENTS.md:1-18`:

> Gas City is an orchestration-builder SDK — a Go toolkit for composing multi-agent coding workflows. It extracts the battle-tested subsystems from Steve Yegge's Gas Town into a configurable SDK where **all role behavior is user-supplied configuration** and the SDK provides only infrastructure. The core principle: **ZERO hardcoded roles.** The SDK has no built-in Mayor, Deacon, Polecat, or any other role. If a line of Go references a specific role name, it's a bug.

The architecture is the **Nine Concepts** model (`gascity/engdocs/architecture/nine-concepts.md`):

| Layer | # | Primitive | Implementation |
|---|---|---|---|
| 0-1 (irreducible) | 1 | **Session** | `internal/runtime/` Provider interface; impls: tmux, subprocess, exec, k8s, ACP, auto, hybrid, fake |
| 0-1 | 2 | **Bead Store** | `internal/beads/` `Store` interface; impls: BdStore (Dolt-backed), FileStore, MemStore, exec |
| 0-1 | 3 | **Event Bus** | `internal/events/` Provider; append-only JSONL at `.gc/events.jsonl` |
| 0-1 | 4 | **Config** | `internal/config/` TOML; progressive activation Levels 0-8 by section presence |
| 0-1 | 5 | **Prompt Templates** | Go `text/template` in Markdown at `agents/<n>/prompt.template.md` |
| 2-4 (derived) | 6 | **Messaging** | Mail = bead of `type="message"`; Nudge = `runtime.Provider.Nudge()` |
| 2-4 | 7 | **Formulas & Molecules** | `internal/formula/` (TOML templates); `internal/molecule/` (runtime instances as bead trees); Orders = Formulas with Event Bus triggers |
| 2-4 | 8 | **Dispatch (Sling)** | `internal/sling/` — find agent → select formula → create molecule → hook to agent → nudge → log event |
| 2-4 | 9 | **Health Patrol** | Controller loop in `cmd/gc/controller.go` — reconciles desired-vs-running state |

Three test gates control whether a new primitive can be added (`engdocs/contributors/primitive-test.md`):

1. **Atomicity** — not decomposable into existing primitives.
2. **Bitter Lesson** — must become MORE useful as models improve. Heuristics and decision trees fail.
3. **ZFC (Zero Framework Cognition)** — Go handles transport only. *"If a line of Go contains a judgment call, it's a violation. An `if stuck then restart` is framework intelligence. Move the decision to the prompt."*

The **Progressive Capability Model** activates capabilities by config presence (`engdocs/architecture/nine-concepts.md:182-195`):

| Level | Config required | Adds |
|---|---|---|
| 0-1 | `[workspace]` + `[[agent]]` | Session + tasks |
| 2 | `[daemon]` | Task loop (controller) |
| 3 | `[[agent]]` with `[agent.pool]` | Multiple agents + pool |
| 4 | `[mail]` | Messaging |
| 5 | Formula files + `[formulas]` | Formulas & molecules |
| 6 | `[daemon]` health fields | Health monitoring |
| 7 | `orders/` directories | Orders |
| 8 | All sections | Full orchestration |

This is unusual and important: **there are no feature flags or capability toggles. The presence of a config section IS the activation.** A Gas City deployment at Level 1 is a single-agent session manager; the same binary at Level 8 is a full reconciling fleet. Methodology adopters can start small.

The **Permanent Exclusions** (`gascity/AGENTS.md:221-229`) are equally load-bearing — each fails the Bitter Lesson test:

- No skills system (the model IS the skill system)
- No capability flags (a sentence in the prompt is sufficient)
- No MCP/tool registration (if a tool has a CLI, the agent uses it)
- No decision logic in Go (the agent decides from prompt and reality)
- No hardcoded role names (roles are pure configuration)

Read [`13-gas-city-deep-dive`](followup/13-gas-city-deep-dive.md) for the full ~10,200-word reference — including the ~45-command CLI surface, the `city.toml` + PackV2 + progressive-activation model, the Provider interface for runtimes, the four bead-store implementations, the formula/molecule/order/convergence/sling primitives with TOML schemas, the K8s-style reconcile loop with explicit Erlang/OTP mapping, the trust-boundary model with three trust tiers, the bundled packs (`core`, `bd`, `dolt`, `maintenance`, `gastown`), and the conformance test pattern for every pluggable interface.

### 1.3 The crucial split — substrate vs. application

The architectural fact that matters for everything that follows: **the entire Gastown role taxonomy is a pack on Gas City, not built-in Go**. `gascity/docs/getting-started/coming-from-gastown.md:48-62` is explicit:

> Gas City is the SDK extracted from Gas Town. The fastest way to get productive is to stop looking for a one-to-one port of Town's role tree and instead map Town concepts onto Gas City's primitives: agents, beads, events, config, prompt templates, derived mechanisms like orders, formulas, waits, mail, and sling. ... In Gas City, every durable work item is a bead; agents are generic; roles come from prompts, formulas, orders, and config; the controller owns SDK infrastructure behavior; directories are an implementation detail, not the architecture.

Concretely, the translations:

- **Plugin → Order.** An *exec order* runs shell or controller-side logic with no agent session. A *formula order* instantiates agent-driven workflow. *"If the Gas Town idea is 'something should run automatically on a schedule, on an event, or when a condition is true,' you probably want an order."*
- **Dog → exec Order** (usually) — because no LLM session is needed.
- **Mayor / Deacon / Witness / Refinery → pack agents** with their own prompt templates. The Gastown pack ships them in `examples/gastown/packs/gastown/agents/<name>/`.
- **Convoy → bead-shaped grouping**. Still useful as a mental model, but no special convoy subsystem.
- **Crew vs. Polecat → operating modes**, not types. Crew = persistent named agents you reason about by hand. Polecat = scalable/transient sessions, often with dedicated worktrees.
- **Filesystem layout → not the architecture**. Identity comes from `dir`/`work_dir` config fields and bead metadata, not from where on disk the agent runs.

The corollary is methodologically important: **Gas Town's Mayor-centric workflow is not the only deployment shape Gas City supports.** A Compound Engineering "three-lane" deployment (Plan agent + Work agent + Review agent — [`03-every-compound-engineering`](03-every-compound-engineering.md)) is just three agent definitions with different prompts and a formula or two to route work between them. An Attractor-shaped DAG ([`02-strongdm-attractor`](02-strongdm-attractor.md)) is a formula whose steps map to codergen/conditional/parallel/wait nodes. A Specification-Refinery-style revelation cycle ([`01-specification-refinery`](../architectures/01-specification-refinery.md)) is a convergence loop wrapping a probe formula. **The substrate is genuinely substrate-shaped.**

This same split also explains a tension surfaced earlier in the corpus. [`04-gastown-beads`](followup/04-gastown-beads.md) framed the Attractor-vs-Gastown comparison as "pipeline-first vs. workforce-first" — and that framing remains correct *for Gas Town as an application*. But Gas City as a substrate is a third thing: **primitive-first**. It does not commit to either pipeline shape or workforce shape; it commits to the small set of primitives both shapes need.

---

## 2. Gas systems → StrongDM Dark Factory primitive map

The Dark Factory methodology, as canonicalized by El Kaim and StrongDM ([`07-dark-factory`](07-dark-factory.md), [`01-strongdm-factory`](01-strongdm-factory.md), [`02-strongdm-attractor`](02-strongdm-attractor.md)), has a recognizable primitive list. The mapping below shows which Gas systems primitive (and at which layer — substrate / Gastown pack / methodology-specific extension) realizes each.

| Dark Factory primitive | Source | Gas City realization | Gas Town realization | Status |
|---|---|---|---|---|
| **Seed** (PRD / sentences / screenshot / existing codebase) | StrongDM principles | Bead with `type="seed"` or `type="task"`; convoy-rooted | `gt convoy create "Feature X" gt-abc12` | ✅ Direct |
| **Spec (NLSpec)** — prose intent | Attractor spec terminology | Bead body + prompt template; convoyed | Same; `gt mayor attach` is the entry point | ✅ Direct |
| **Scenarios** — out-of-codebase holdout user stories | Dark Factory §"Validation problem"; StrongDM homepage | Bead with `type="scenario"` stored in a separate rig (or a separate "scenario" workspace path) | Same; could live in a dedicated `scenarios/` rig | 🟡 Convention; engine doesn't enforce out-of-codebase discipline |
| **Satisfaction** — LLM-as-judge probabilistic metric over trajectories | StrongDM principles; [`01-strongdm-factory`](01-strongdm-factory.md) | Convergence loop (`gc converge`) with a judge agent in the gate role; bead status reflects outcome | Pack agent + `gt mol` formula wrapping a judge call | 🟡 Engine has the loop primitive; the judge agent is methodology-supplied, not built in |
| **DOT pipeline** — Attractor graph as declarative workflow | [`02-strongdm-attractor`](02-strongdm-attractor.md) | Formula chain — TOML steps with `needs:` edges; or Convoy graph routing in `internal/graphroute/`; or a custom formula handler that reads DOT and dispatches via `gc sling` | Same | 🟡 No first-class DOT parser; needs a custom formula or an external DOT-to-formula transpiler |
| **Codergen node** (LLM stage executing a coding agent) | Attractor spec §4 | A generic agent with provider = claude/codex/gemini, working a wisp bead | Polecat with its provider config | ✅ Direct |
| **Wait.human node** (hexagon human gate) | Attractor spec §4.6 | `gc wait` durable session wait; gate evaluates a bead status transition or a typed mail reply | `gt escalate` materializes the question as a bead routed via severity ladder | ✅ Direct in Gas City; richer in Gas Town (severity-tiered escalation) |
| **Parallel fan-out + fan-in** | Attractor spec §4 | Convoy + Sling spawn multiple wisps; `internal/dispatch/` graph.v2 workflow handles fan-out; convoy `control` runs fan-in | Same | ✅ Direct |
| **Goal gate + retry_target** | Attractor spec §3 | Convergence loop has explicit gate + retry semantics; `gc converge retry`, `gc converge approve` | Pack-defined formula with retry policy | ✅ Direct |
| **Context fidelity slider** (`full`/`compact`/`summary:low|med|high`/`truncate`) | Attractor spec §5 | Not present as a first-class primitive | Not present | ❌ Methodology-level convention; would need an extension agent/order to summarize between steps |
| **Supervisor loop (manager_loop)** — `stack.manager_loop` observing a child pipeline | Attractor spec §4 | Controller + Order pattern: a periodic order can observe a convoy's bead status and inject steering via mail; convergence loop is the engine-level equivalent | Deacon/Witness/Mayor pattern is the highest-level instance in the corpus | ✅ Direct (engine-level via convergence; pack-level via Witness/Deacon) |
| **CXDB** — turn-DAG observability + BLAKE3 CAS + branchable history | [`01-strongdm-factory`](01-strongdm-factory.md) | Event Bus (`internal/events/`) + Beads history (Dolt cell-level versioning); not a turn-DAG, but **the event log + bead history is structurally equivalent for trajectory persistence** | Same + `.events.jsonl` per session captured by `gt seance` | 🟡 Structurally adequate but lacks BLAKE3 CAS and explicit branching API |
| **Digital Twin Universe (DTU)** — behavioral SDK-fidelity clones of upstream SaaS | [`01-strongdm-factory`](01-strongdm-factory.md) | None at the substrate level — but a DTU could be a `[[service]]` declaration in `city.toml` (workspace service) plus a pack agent that runs it | Same | ❌ Methodology + integration work, not substrate work |
| **Healer** — observability layer that watches CXDB, clusters bad behavior, spawns prescription agents | [`07-dark-factory`](07-dark-factory.md) | An Order subscribed to event-bus event types (`session.crashed`, `gate.failed`, anomaly markers) that dispatches a diagnosis formula via `gc sling`; the prescription is a bead | Same; Boot+Deacon already model the pattern (Boot wakes Deacon, Deacon dispatches Dogs) | ✅ Pattern is realizable as Orders + formulas; not packaged |
| **Filesystem as memory** | StrongDM techniques | Beads + hooks (git worktrees) — Gas Town's "propulsion principle" — exactly this | Hooks specifically realize this | ✅ Direct |
| **Gene transfusion** — point an agent at a concrete exemplar | StrongDM techniques | Pack agent prompt template references an example path; or a formula step pipes the exemplar into the next agent's context | Same | ✅ Direct (prompt-level) |
| **Pyramid summaries** — reversible multi-zoom summarization | StrongDM techniques | Bead labels + parent-child relations + closed-task memory decay (in Beads) | Same | 🟡 Beads supports the structure; agents must use it discipline-wise |
| **Shift work** — separate interactive (day) from fully-specified (night) | StrongDM techniques | Operating discipline; convoys and orders run autonomously by design | Same; `gt feed --window` is the day-shift UI | ✅ Direct |
| **Semport** — semantic port across languages | StrongDM techniques | A formula chain whose steps are codergen nodes with language-targeted prompts | Same | ✅ Direct |
| **Attribution** — every commit / task / event carries actor identity | El Kaim §"Attribution and the Agent Workforce"; Gas Town principle #1 | Bead `created_by`, event `actor`, OTEL `service.namespace=gastown` (and equivalent for Gas City) | This is **the load-bearing principle of Gas Town**, verbatim El Kaim quote: *"attribution is not optional"* | ✅✅ Strongest match in the corpus |
| **Twelve principles** (specs as source of truth, three-layer architecture, etc.) | El Kaim conclusion | Most are methodology constraints, not engine concerns | Same | (Not engine-level, but engine doesn't fight them) |

The dominant pattern in the table: **Dark Factory's three-layer architecture maps onto Gas City three-layer-equivalent.** El Kaim's Layer 1 (LLM Client) is the Gas City `runtime.Provider` interface (and the per-provider hook configs in `internal/hooks/`). El Kaim's Layer 2 (Agent Loop) is the LLM provider's own coding-agent loop — Claude Code, Codex, Gemini, Copilot, Cursor, Amp, OpenCode, Auggie, Kiro — which Gas City spawns and supervises but does not implement. El Kaim's Layer 3 (Pipeline Engine, "knows when to pause for human input") is Gas City's Controller + Formula + Convergence + Convoy + Sling + Health Patrol stack, plus `gc wait` and the Gastown pack's `gt escalate` chain.

The two architecture maps are structurally homomorphic, but with different *boundary* placements:

- **Attractor's pipeline graph** is a single DOT file declaring nodes and edges; Gas City's "pipeline graph" is a formula whose steps can themselves spawn sub-formulas via `gc sling --formula` and whose Convoy graph routing is in `internal/graphroute/`. Both representations are declarative; both are diffable in PRs. The DOT vs. TOML choice is a syntax decision, not an architectural one.
- **Attractor's `wait.human` hexagon** is one node type; Gas City offers two complementary mechanisms — `gc wait` for synchronous graph-local pauses (Attractor-shaped) plus mail/escalate/seance for asynchronous severity-routed handoff (Gas Town-shaped). The Gastown pack chooses async-by-default; nothing prevents a Dark-Factory-shaped pack from choosing sync-by-default.
- **Attractor's manager_loop** is a single recursive primitive; Gas City has two layers — the Controller (machine-level reconciliation) and Convergence (workflow-level retry-until-converged). The Gastown pack adds a third layer (Witness/Deacon/Mayor) as agent-level supervision. **Three levels of supervision are realizable**, which directly addresses Attractor open question #4 (*"Supervisor recursion depth — Attractor's design generalizes one level"*) from [`02-strongdm-attractor`](02-strongdm-attractor.md).

The gap that matters most: **scenarios as out-of-codebase holdout sets**. Gas City stores beads in per-rig Dolt databases. Nothing in the engine prevents creating a `scenarios/` rig that the implementer rigs cannot reach, but neither does anything *enforce* the holdout discipline. This is a methodology-level discipline that the substrate can support (a separate rig with no overlap to the implementer agents' bead-prefix routing in `routes.jsonl`) but cannot guarantee. Verified in §6 below.

---

## 3. Gas systems → Compound Engineering primitive map

Compound Engineering (Every.to / Klaassen / Shipper / Tedesco — [`03-every-compound-engineering`](03-every-compound-engineering.md)) has a different but overlapping primitive set. The core artifacts are durable on-disk files (`CLAUDE.md`, `AGENTS.md`, `docs/solutions/`, `docs/brainstorms/`, `docs/plans/`, `STRATEGY.md`, `llms.txt`); the core process is the four-step Plan→Work→Review→Compound loop; the core multi-agent surface is the 14–50-agent parallel review panel.

| Compound Engineering primitive | Source | Gas City realization | Gas Town realization | Status |
|---|---|---|---|---|
| **`CLAUDE.md` / `AGENTS.md`** as the read-every-session memory | Every.to guide | Lives in each rig's repo (Gas City does not synthesize it); per-agent `prompt.template.md` is the substrate-side complement | Same; `gt prime` injects context at session start via the SessionStart hook | ✅ Direct |
| **`llms.txt`** for high-level architectural decisions | Klaassen "Cora playbook" | Same — repo-level file, Gas City does not enforce | Same | ✅ Direct |
| **`docs/solutions/`** auto-curated knowledge store | Every.to guide | Same; convention plus repo discipline | Same | ✅ Direct (no engine support but no obstacle) |
| **Plan → Work → Review → Compound loop** | Klaassen / Shipper | Four sequential formula steps in a TOML file; or a Convergence loop with these stages as gated nodes; or four pack-agent roles linked by a convoy | Pack agents (planner, worker, reviewer, knowledge curator) with `gt sling` between them | ✅ Direct |
| **Plans as the new code** — plan documents as the source of truth | Every.to guide | Plan document is a bead body (or a markdown file at `docs/plans/`); plan-tier ceremony scales with formula complexity | Same | ✅ Direct |
| **14-agent review panel** (security-sentinel, performance-oracle, etc.) | Every.to guide | 14 agents in `pack.toml`, each with a specialized prompt template; a `review-fanout.formula.toml` parallel-fans them out via Sling/Convoy; results joined in a fan-in gate that synthesizes P1/P2/P3 | Same; could be polecats in a `review` rig | ✅ Direct (this is the Atelier shape the substrate is best at) |
| **Stable IDs** (R/A/F/AE/U) across artifacts | Compound Engineering plugin | Bead IDs (`<prefix>-XXXXX`) are stable and hash-based; cross-references via Beads `depends-on`/`relates-to`/`discovered-from`/`replies_to` edges | Same | ✅ Direct |
| **Parallel multi-persona review with synthesis** | Every.to guide | Convoy fan-out + fan-in; or `dispatch/` graph.v2 workflow; or a convergence loop with multi-judge | Same | ✅ Direct |
| **`/triage` — human-filtered review** vs. **`/resolve_pr_parallel` — auto-fix** | Every.to plugin | Two formula presets; the choice is which one is dispatched | Same; Refinery is the existing auto-fix queue equivalent | ✅ Direct |
| **Three questions to ask any AI output** (hardest decision / rejected alternatives / least confident) | Every.to guide | Prompt-template content (not substrate-level) | Same | (Not engine-level) |
| **Self-improving prompts** — agent rewrites its own prompt based on chain-of-thought failure analysis (Klaassen frustration-detector) | Every.to "My AI Had Already Fixed" | Pack-level convention — a formula step that reads chain-of-thought events from the Event Bus, runs a prompt-rewrite call, and patches the agent's `prompt.template.md` (with a CI guard or `sourceworkflow` enforcement to prevent runaway self-modification) | Same; would need `gt-model-eval/` evaluations to gate the modification | 🟡 Realizable; needs a custom Order + a self-modification guardrail |
| **Auto-invoke triggers** ("that worked", "it's fixed") | Every.to plugin | Order triggers — an event-bus condition (`session.message contains "that worked"`) dispatches a `compound` formula | Same | ✅ Direct (this is exactly the Order primitive) |
| **Skip permissions (`--dangerously-skip-permissions`)** for flow-state work | Every.to guide | Per-agent provider config (`provider = "claude"`, with `args = ["--dangerously-skip-permissions"]` in the agent's TOML) | Same | ✅ Direct |
| **Worktree isolation** — git worktrees per parallel issue | Every.to guide | `work_dir` field per agent; pack scripts call `git worktree add` in `pre_start` | Hooks ARE this — the propulsion principle | ✅ Direct (Gas Town's strongest match) |
| **Async-by-default team communication** — plan docs reviewed by EOD, not in meetings | Every.to guide | Mail (durable bead-typed messages) IS this | Same; the Mayor session is the conversational layer | ✅ Direct |
| **80/20 per-cycle + 50/50 across-time allocation rules** | Every.to guide | Operating discipline; not engine-level | Same | (Not engine-level) |
| **Pulse reports / Strategy doc** | Every.to plugin | A periodic Order that runs a `pulse` formula and writes to a `pulse-reports/` directory; bead-typed | Same | ✅ Direct |
| **Compound step**: write findings back into `docs/solutions/` with YAML frontmatter for retrieval | Every.to guide | Pack-level formula whose final step is a `solution-writer` agent; can be the canonical fourth step in a Plan-Work-Review-Compound formula | Same | ✅ Direct |
| **Three-lane setup** (planner + delegator + reviewer terminals, all in Warp / tmux) | Klaassen "Cora playbook" | Three agents with distinct providers (the post explicitly names Claude Code + Friday + Amp); `gc session attach` opens each in tmux; the lanes communicate via mail | Same; Mayor session + two Polecats with explicit handoff between them | ✅ Direct (and Gas Town's tmux-first design is **exactly this pattern**) |
| **`/lfg` (let's f-ing go)** — chains the whole pipeline | Every.to guide | A top-level formula that composes plan→deepen-plan→work→review→resolve→tests→video→compound as sub-formulas via `gc sling --formula` | Same | ✅ Direct |
| **Three project-level outcomes**: time-to-ship 1-3 days, bugs caught up, PR review cycles in hours | Klaassen "Cora" | Outcome metrics, not engine concerns; observable via OTEL counters | Same | (Engine-level observability supports it) |

The dominant pattern: **Compound Engineering is closer to "Gas Town shape" than to "Attractor shape"**, because its core innovation is the **chain of durable on-disk artifacts** (CLAUDE.md → plan → workpad → solutions → strategy) rather than the chain of pipeline stages. Gas Town's design — git-worktree-backed hooks as durable agent memory, beads as durable work memory, mail as durable communication — is the substrate's strongest fit anywhere in the corpus. The 14-agent review panel becomes a parallel fan-out + fan-in via Convoy + Dispatch. The Plan-Work-Review-Compound loop becomes a four-step formula. The self-improving-prompt pattern (Klaassen's frustration-detector) is the one piece of methodology that the substrate cannot guarantee — it requires a self-modification-with-guardrails Order, which is engineering work but inside the Order primitive's design center.

A subtler observation: **Compound Engineering's compounding mechanism is structurally identical to Beads' `discovered-from` edge** (`gastown/docs/concepts/beads.md`, also noted in [`04-gastown-beads`](followup/04-gastown-beads.md)). Compound Engineering says: every bug fix should leave behind learnings the system reads next time. Beads' `discovered-from` edge says: every task knows what other task surfaced it. The Beads graph and the Compound knowledge store are dual representations of the same compounding-of-knowledge phenomenon — one as a typed graph (Beads), the other as YAML-frontmatter markdown (`docs/solutions/`). A Compound Engineering deployment on Gas City could legitimately use the Beads graph itself as the primary knowledge store and project Markdown as a presentation layer (the inverse of Every's choice).

---

## 4. Deployment sketch — Dark Factory on Gas City

A concrete sketch for "use Gas City to run the StrongDM Dark Factory." This is not a recommended product blueprint; it is a feasibility walk meant to surface where the substrate fits and where it doesn't.

**Pack name:** `darkfactory` (sibling to `gastown` in `examples/`).

**City layout** (`city.toml` excerpt):

```toml
[workspace]
name = "df-prod"

[imports.darkfactory]
source = "./packs/darkfactory"

[beads]
provider = "bd"  # Dolt-backed for cell-level merge

[daemon]
enabled = true

[[service]]
name = "okta-dtu"
type = "managed_socket"
exec = ["okta-dtu", "--port", "${PORT}"]

[[service]]
name = "jira-dtu"
type = "managed_socket"
exec = ["jira-dtu", "--port", "${PORT}"]

# rig for each DTU's source SDK + clone implementation
[[rigs]]
name = "okta-dtu-impl"
path = "./rigs/okta-dtu"

# rig for scenario holdout — separate prefix, separate bead DB
[[rigs]]
name = "scenarios"
path = "./rigs/scenarios"
prefix = "scn-"  # implementer agents' work_query won't see scn-* beads

# rig for the product itself
[[rigs]]
name = "product"
path = "./rigs/product"
```

**Pack agents** (`packs/darkfactory/agents/`):

- `coder/` — generic Attractor-codergen node. Provider = `claude`, prompt template implements the Coding Agent Loop spec's Claude profile (per [`02-strongdm-attractor`](02-strongdm-attractor.md) §"Agents and roles").
- `judge/` — LLM-as-judge for the satisfaction metric. Provider = a different model family from `coder` (per Attractor's "Each model family works best with its native agent's tools" principle, but also per Dark Factory's judge-independence open question — [`02-strongdm-attractor`](02-strongdm-attractor.md) open question #2).
- `healer/` — anomaly-clustering + prescription-writing agent. Reads from the Event Bus (`gc events --watch --type=session.crashed,gate.failed,convergence.diverged`), writes a diagnosis bead, and slings a `prescription.formula.toml` to a fresh `coder` instance.
- `interviewer/` — handles `gc wait` gates. Implements the Attractor Interviewer interface (`AutoApprove`, `Console`, `Slack`, `Queue`, `Recording`) as runtime modes via prompt-template config.

**Pack formulas** (`packs/darkfactory/formulas/`):

```toml
# packs/darkfactory/formulas/attractor.formula.toml
description = "Attractor-shaped scenario-driven build"
formula = "attractor"

[[steps]]
id = "implement"
agent = "coder"
input_bead = "${SEED_BEAD}"
output_type = "implementation"

[[steps]]
id = "satisfaction"
agent = "judge"
needs = ["implement"]
prompt_template = "judge-against-scenarios.tmpl"
input_query = "rig:scenarios labels:active"  # judge can read scenarios, coder can't
gate = true  # convergence stops here unless threshold met

[[steps]]
id = "retry-or-merge"
condition = "satisfaction.score < 0.95"
target = "implement"
fallback = "merge"

[[steps]]
id = "merge"
agent = "refinery"  # reuses the Gastown pack's Refinery for merge queue
condition = "satisfaction.score >= 0.95"
```

The convergence loop is wrapped in a `gc converge create --formula attractor --seed <bead-id>` invocation; the engine iterates implement→satisfaction until either the threshold is met or `--max-iterations` exhausts.

**Pack orders** (`packs/darkfactory/orders/`):

```toml
# packs/darkfactory/orders/healer.order.toml
description = "Healer — watch for failures, dispatch prescriptions"
trigger = "event"
event_types = ["session.crashed", "convergence.diverged", "scenario.regression"]
formula = "prescription"
agent = "healer"
```

```toml
# packs/darkfactory/orders/maintenance-shift.order.toml
description = "Nightly DTU drift check"
trigger = "cron"
cron = "0 3 * * *"
formula = "dtu-drift-check"
```

**Scenarios as out-of-codebase holdout** — the `scenarios` rig has `prefix = "scn-"`, and the `coder` agent's `work_query` is `rig:product` (its rig prefix only). The `judge` agent's `work_query` includes both. Neither rig is reachable by the other's bead queries; the `discovered-from` edge can cross rigs but the implementer cannot list `scn-*` beads. This is **convention enforced by config**, not by the engine — but it is auditable in `routes.jsonl`, the `[[rigs]]` config, and the per-agent `work_query` patches. A `scenario-isolation` lint can be enforced via `gc doctor` rules.

**Digital Twin Universe** — each DTU is a `[[service]]` declaration in `city.toml` plus a managed socket. The pack ships a `dtu-Build` formula whose steps are: read SDK ref → generate handler scaffold → run integration test against live service → write behavioral diff → patch handler → repeat until diff is empty. This is essentially a Semport-shaped formula targeting Okta/Jira/Slack/GSuite.

**CXDB substitute** — the Event Bus (`internal/events/`) records every session lifecycle event, bead transition, mail send, convergence iteration, gate evaluation, and order dispatch with monotonically-increasing `seq`. Combined with Beads' Dolt-backed cell-level history (every bead update is a Dolt commit), this gives the trajectory-replay surface CXDB offers — *minus* the BLAKE3 content-addressing and the O(1) branching API. For the Dark Factory's specific needs (replay, audit, "what did the agent see when it failed at step 14"), the Event Bus + Beads history are sufficient. If true CAS-and-branching is needed, an Order can checkpoint to `git` (which is BLAKE-family CAS) or to a content-addressed store at convergence-loop checkpoints — see Gas Town's `mol-merge-queue-bundle` precedent.

**What this deployment gets right (from the methodology):**

- Three-layer architecture (LLM Client + Agent Loop + Pipeline Engine) is preserved.
- Engines are commodity, pipelines are IP — the methodology-specific pipelines are the `darkfactory` pack's formulas, which can be open-sourced as a pack import without giving up the proprietary scenarios.
- Self-healing loop is closed at the Order level — Healer watches the Event Bus, writes diagnoses, dispatches prescriptions.
- Attribution is universal (every bead, every event, every commit).
- Filesystem-as-memory is preserved (worktree-backed hooks).
- Shift work is preserved (Orders run on cron; convergence runs unattended overnight).

**What this deployment cannot get right without methodology-level work:**

- **Scenario-authorship discipline.** The substrate stores scenarios in a separate rig but cannot enforce that they are written before the implementation, or that the `judge` agent does not have read access to the implementation rig. These are organizational policies surfaced as `gc doctor` lint rules at best.
- **Satisfaction-judge independence.** Methodologically the judge must use a different model family from the coder. Gas City makes this configurable but does not enforce it. Pack-level config can default to it; pack-level lint can fail closed.
- **DTU build cost.** Each DTU is real engineering work — Gas City just provides the `[[service]]` slot and a Semport-shaped formula. The methodology's claim that DTUs are "now routine" is contingent on coder-fleet productivity, not substrate features.

---

## 5. Deployment sketch — Compound Engineering on Gas City + Gastown pack

A second sketch — this time using the **Gastown pack** as the base rather than building a fresh one. The motivation: Compound Engineering's Mayor-centric "tell the assistant what you want and it orchestrates" workflow is structurally identical to Gas Town's Mayor-decomposes-intent pattern.

**City layout** (`city.toml` excerpt):

```toml
[workspace]
name = "ce-prod"

[imports.gastown]
source = "./packs/gastown"

[imports.compound]
source = "./packs/compound"
# the compound pack patches gastown.mayor's prompt and adds 14 reviewer agents

[beads]
provider = "bd"

[daemon]
enabled = true

[[rigs]]
name = "myproject"
path = "./rigs/myproject"

[[rigs.patches]]
agent = "gastown.polecat"

[rigs.patches.pool]
max = 6  # 3-lane setup + 3 reviewer slots
```

**Pack composition:**

- `gastown` ships Mayor, Witness, Deacon, Refinery, Polecat — kept as-is.
- `compound` ships:
  - `compound.planner` agent (provider = claude, prompt biases for outline + alternatives)
  - `compound.worker` agent (provider = codex, the implementation lane per Klaassen's three-lane setup)
  - `compound.reviewer` parent agent (provider = amp, runs `compound.review-panel.formula.toml`)
  - 14 specialized reviewer agents (`security-sentinel`, `performance-oracle`, `architecture-strategist`, `pattern-recognition-specialist`, `data-integrity-guardian`, `data-migration-expert`, `code-simplicity-reviewer`, `kieran-rails-reviewer`, `kieran-python-reviewer`, `kieran-typescript-reviewer`, `dhh-rails-reviewer`, `deployment-verification-agent`, `julik-frontend-races-reviewer`, `agent-native-reviewer`) per [`03-every-compound-engineering`](03-every-compound-engineering.md) §"Agents and roles". Each is a `prompt.template.md` plus an agent.toml that pins the model.
  - `compound.curator` agent that runs the compound step — writes findings to `docs/solutions/` with YAML frontmatter.

**Pack formulas:**

```toml
# packs/compound/formulas/lfg.formula.toml
description = "Plan → Work → Review → Compound (Klaassen lfg shape)"
formula = "lfg"

[[steps]]
id = "plan"
agent = "compound.planner"
input_bead = "${SEED_BEAD}"
output_type = "plan"
pause_after = true   # opens a gc wait for human plan-approval

[[steps]]
id = "work"
agent = "compound.worker"
needs = ["plan"]

[[steps]]
id = "review-panel"
agent = "compound.reviewer"
needs = ["work"]
formula = "review-fanout"  # spawns 14 parallel reviewers, joins on P1/P2/P3 synthesis

[[steps]]
id = "resolve"
condition = "review.severity_max == 'P1'"
formula = "resolve-pr-parallel"   # auto-fix per Klaassen
agent = "compound.worker"
loop_until = "review.severity_max < 'P1'"

[[steps]]
id = "compound"
agent = "compound.curator"
needs = ["resolve"]
prompt_template = "compound-step.tmpl"  # writes docs/solutions/*.md with YAML frontmatter
```

```toml
# packs/compound/formulas/review-fanout.formula.toml
description = "14-agent parallel review with synthesis"
formula = "review-fanout"

[[steps]]
id = "security"
agent = "compound.security-sentinel"
parallel_group = "review"

[[steps]]
id = "performance"
agent = "compound.performance-oracle"
parallel_group = "review"

# ... 12 more entries ...

[[steps]]
id = "synthesize"
agent = "compound.reviewer"   # parent
needs_all = "review"
prompt_template = "synthesize-findings.tmpl"
```

**Pack orders:**

```toml
# packs/compound/orders/auto-invoke.order.toml
description = "Auto-trigger compound step on 'that worked' message"
trigger = "event"
event_types = ["session.message"]
condition = "payload.text matches /(it'?s fixed|that worked|done)/i"
formula = "compound"
```

```toml
# packs/compound/orders/refresh.order.toml
description = "Knowledge-store refresh (avoid stale-knowledge inverting compounding)"
trigger = "cron"
cron = "0 8 * * MON"
formula = "compound-refresh"
agent = "compound.curator"
```

**Three-lane setup** — three tmux windows per rig:

```bash
gc session attach gastown.mayor    # Lane 1 — Plan
gc session attach compound.worker  # Lane 2 — Build
gc session attach compound.reviewer # Lane 3 — Review
```

The lanes communicate via `gt mail` / `gc mail` (durable, attribution-preserved) plus `gc session nudge <target>` (immediate, ephemeral). Klaassen's "open three terminals" instruction is operationally the same.

**`CLAUDE.md` / `AGENTS.md` / `llms.txt`** are in each rig's repo. `gc prime` writes the SessionStart hook payload from the pack's `prompt.template.md` plus the rig's `CLAUDE.md`. The compound pack's `prompt.template.md` for the planner includes Klaassen's "ask three questions" pattern in its system prompt.

**`docs/solutions/`** lives in each rig's repo. The compound curator writes to it with YAML frontmatter. Future agents grep it. Stable IDs (R-/A-/F-/U-) are bead IDs.

**Self-improving prompts (Klaassen frustration-detector pattern)** — a `compound.prompt-improver` agent and a `prompt-self-improve.order.toml`:

```toml
trigger = "event"
event_types = ["judge.regression"]
condition = "payload.regression_kind == 'prompt-failure'"
formula = "prompt-improve"
```

The formula's flow: read recent `session.message` events of the failing agent → analyze chain-of-thought → write proposed `prompt.template.md` patch as a bead → wait for human approval at a `gc wait` gate → on approve, apply via `git apply` in the pack's repo. The human gate is the guardrail against runaway self-modification.

**What this deployment gets right:**

- The four-step loop is a formula with explicit gates at plan-approval and review-synthesis.
- The 14-agent review panel is a true parallel fan-out with synthesis at the join.
- `docs/solutions/` and `CLAUDE.md` are repo files; the compound step writes to them as the canonical fourth-step deliverable.
- Auto-invoke triggers work as Orders (this is exactly the Order primitive's design center).
- The three-lane setup is operationally identical to running three Polecats with different providers, communicated via mail/nudge.
- 80/20 + 50/50 time allocation is operating discipline, not engine concern, and the engine doesn't fight it.

**What this deployment cannot get right without methodology-level work:**

- **Plan-tier ceremony scaling** — the methodology says lightweight/standard/deep should each have different ceremony. Gas City supports this via three sibling formulas (`lfg-light.formula.toml`, `lfg-standard.formula.toml`, `lfg-deep.formula.toml`) but the *choice* between them is a planner-agent decision, not an engine call.
- **Adversarial reviewers and adversarial document reviewers** as distinct named roles — these are pack additions, not engine features.
- **Residual Work Gate** (Compound Engineering's "no silent ship-with-findings" rule) — this is a formula-level gate, but the *fingerprint deduplication of findings across rounds* is methodology logic that needs to live in either the curator's prompt or a sidecar database.

---

## 6. Where the substrate falls short

Three categories of gap:

### 6.1 Engine-level capabilities missing for both methodologies

- **No first-class LLM-as-judge primitive.** Both methodologies require an LLM judge as a structural element. Gas City offers Convergence loops with `gate` semantics, but the actual judge prompt + scoring logic is methodology-supplied. This is the right boundary — judges are heavily methodology-specific — but it means *every* methodology pack must rebuild the same judge scaffolding. A canonical `judge-agent` template would reduce duplication.
- **No DOT pipeline parser.** Methodologies expressed in Attractor DOT do not run on Gas City without a transpilation step (DOT → formula TOML) or a custom formula handler that reads DOT directly. This is engineering work the parent project may want to invest in if it adopts Attractor at scale.
- **No context-fidelity slider.** Attractor's `fidelity` knob (`full`/`compact`/`summary:low|med|high`/`truncate`) is a per-edge concept that routes how much state crosses the boundary. Gas City passes context via bead body + mail; summarization between steps must be a methodology-level formula step (e.g., a `summarize-progress` step before each retry).
- **No turn-DAG / CAS branching.** Event Bus + Dolt-backed Beads cover the audit-trail use case but lack CXDB's BLAKE3 content-addressing and O(1) history branching. For Dark Factory's deepest claims (cheap counterfactual replay), this is real missing capability — but for everything below that, the substrate is sufficient.

### 6.2 Methodology-level disciplines the substrate stores but cannot enforce

- **Scenarios as out-of-codebase holdout.** Separate rig + prefix isolation in `routes.jsonl` + per-agent `work_query` patches realize the discipline by convention. The engine cannot prove the holdout is honest.
- **Judge independence.** Different model family for judge vs. implementer is configurable; a pack-level lint can enforce it; the engine itself does not.
- **`docs/solutions/` discoverability.** `CLAUDE.md` should reference `docs/solutions/`; Compound Engineering's plugin enforces this via the compound-refresh skill. Gas City has no analog — but pack-level Orders can run periodic checks.
- **Stale-knowledge curation.** The compound-refresh discipline (Every.to) requires periodic re-validation. Gas City can run it as a cron Order; the freshness scoring itself is methodology logic.

### 6.3 Methodology-level disciplines genuinely outside the substrate's scope

- **Spec authorship at scale.** Both methodologies put more weight on spec-writing than the substrate can address. This is a human-leverage discipline.
- **Token-spend telemetry as a meta-leverage check.** Dark Factory's "$1,000/day/engineer" benchmark is observable via OTEL (the Gas City `telemetry/pricing.go` per-provider cost tracking is the right home), but the *display surface* is a dashboard pack, not an engine feature.
- **The three-questions discipline** ("hardest decision? rejected alternatives? least confident?") is a prompt-template content choice. Substrate-neutral.
- **The "Why am I doing this?" Level-3-to-Level-5 discipline** is a human practice, not an engine feature.

---

## 7. Open questions

1. **Should the parent project's factory adopt Gas City as substrate?** The Compound Atelier architecture ([`02-compound-atelier`](../architectures/02-compound-atelier.md)) is the parent project's recommended baseline. Compound Engineering on Gas City + Gastown pack is the closest pre-built substrate for Compound Atelier in the entire corpus. The remaining decision is whether Gas City's post-v1.0.0 maturity is acceptable for the parent project's timeline, and whether the Gastown role taxonomy aligns with the Atelier's named roles (Brainstormer / Spec Analyst / Implementer / Reviewer panel / Synthesizer / Curator / Conductor) — most plausibly, the Atelier names map onto specialized pack agents on top of Gastown's Mayor/Polecat infrastructure.

2. **Does any of the other three candidate architectures benefit from Gas City?** The Specification Refinery (Arch 1) is a layered-prose discipline whose runtime needs are modest — Gas City would be overkill. The Phase-Gated Foundry (Arch 3) maps cleanly onto Gas City via phase-shaped formulas + gate beads, and inherits Gas Town's audit-trail strength. The Evolutionary Tournament (Arch 4) maps onto Gas City via population-of-candidates spawned in parallel via Convoy fan-out, with the Predator agent as an Order watching the Event Bus.

3. **Is the Gas City formula format expressive enough for Attractor's DOT?** Open. The 21-rule DOT linter (Mammoth) catches Attractor-specific invariants — fan-in fan-out, parallel branches, conditional routing, supervisor recursion. Gas City formulas have `needs:` edges plus condition expressions; whether the formula grammar can express *every* DOT shape (especially supervisor-loop recursion and the hexagon `wait.human` ergonomics with first-letter accelerators) requires a deeper test.

4. **What is the right scenario isolation guarantee?** Configurable per-agent `work_query` + per-rig prefix routing is the substrate's offer. Both methodologies want more — a hard guarantee that the implementer cannot see the holdout. Sandboxed polecat execution (the experimental `gt-proxy-server` mTLS mode in Gas Town — `gastown/docs/proxy-server.md`) could provide cryptographic isolation, but it is opt-in and methodology-specific.

5. **Can the same substrate host multiple methodologies in the same workspace?** Pack composition is explicit (`[imports.gastown]` + `[imports.compound]` + `[imports.darkfactory]`); patches are applied per-rig (`[[rigs.patches]]`). It should be possible. Whether running, say, a Dark Factory rig and a Compound Atelier rig in the same town creates undesirable bead-prefix collisions or attention-saturation for the Mayor is empirical.

6. **What's the failure mode of a methodology + substrate mismatch?** If a methodology expects an engine feature the substrate lacks, the methodology either degrades (lose context-fidelity slider, lose BLAKE3 CAS) or grows a pack-level workaround (judge-isolation lint, scenario-isolation lint, etc.). Cataloguing the workarounds and noting whether they generalize would be a separate followup.

7. **Where does Beads' `discovered-from` edge belong in the parent project's RTM?** This is the corpus's strongest candidate "compounding-of-knowledge" primitive at the engine level — strictly more expressive than the Compound Atelier's flat-file `docs/solutions/`. It should be promoted from "Beads schema detail" to "pattern-level primitive" in the parent project's failure-mode framework (related to F8 stale-knowledge, F10 findings-disappear, F14 attribution-collapse).

8. **Does the parent project need Wasteland?** Cross-organization agent reputation is real for >1 org boundary; otherwise free to ignore. The parent project's "general execution environment for agents, scaling from solo to small team" brief is mostly single-org, but if it grows to multi-org or vendor federation (the project is hosted on GitHub, with potential to take third-party plugins), Wasteland is the only inter-town federation primitive in the corpus.

9. **Maintenance asymmetry.** El Kaim's repeated insistence that the dark factory *"does not just build software; it maintains software"* (CXDB → Healer → prescription loop) — Gas City's substrate-level support for this is the Order primitive watching the Event Bus for failure signatures. Gas Town's Witness/Deacon/Boot patterns are the existence-proof. The parent project's four architectures all need a maintenance-loop story; Gas City + Gastown is the strongest substrate match for it.

10. **The substrate is post-v1.0.0 but its internals are still moving** — `gascity/AGENTS.md:138-164` documents two active migrations enforced by CI (the *worker boundary* and the *session-first* refactor). A parent project committing to Gas City as substrate should expect to track its `[Unreleased]` section and be ready for one or two breaking pack-schema or formula-format changes per quarter for at least 2026.

---

## Sources reviewed

| Source | Status | Notes |
|---|---|---|
| `https://github.com/gastownhall/gascity` | ✅ FULL | Cloned to `/tmp/gascity`. Full deep dive in [`13-gas-city-deep-dive`](followup/13-gas-city-deep-dive.md). |
| `https://github.com/gastownhall/gastown` | ✅ FULL | Cloned to `/tmp/gastown`. Full deep dive in [`14-gas-town-deep-dive`](followup/14-gas-town-deep-dive.md). |
| `https://docs.gascityhall.com` | ❌ HTTP 403 | Mintlify projection of `gascity/docs/`; in-repo source used instead. |
| [`01-strongdm-factory`](01-strongdm-factory.md) | ✅ | Re-used for Dark Factory primitive list. |
| [`02-strongdm-attractor`](02-strongdm-attractor.md) | ✅ | Re-used for Attractor primitive list (codergen, wait.human, parallel, manager_loop, fidelity, goal_gate). |
| [`03-every-compound-engineering`](03-every-compound-engineering.md) | ✅ | Re-used for Compound Engineering primitive list (4-step loop, 14 reviewers, CLAUDE.md, docs/solutions, three-lane setup). |
| [`07-dark-factory`](07-dark-factory.md) | ✅ | Re-used for El Kaim's three-layer architecture, Healer loop, Gas Town's five design principles, twelve numbered principles. |
| [`04-gastown-beads`](followup/04-gastown-beads.md) | ✅ | Re-used for the Gas Town / Attractor / Beads comparison; this report supersedes it on substrate-vs-application split. |
| [`00-comparison`](../architectures/00-comparison.md) | ✅ | Re-used for the four candidate architectures and shared-substrate observation. |

Legend: ✅ full / 🟡 partial / ❌ unavailable.

---

## Status

- **Word count:** ~6,300 words (over the typical 1,500–2,500 single-source target, but this is a synthesis report across two substantial new primary sources plus four prior reports — accepted as deliberate over-shoot).
- **Companion deep dives:** [`13-gas-city-deep-dive`](followup/13-gas-city-deep-dive.md) (~10,200 words) and [`14-gas-town-deep-dive`](followup/14-gas-town-deep-dive.md) (~9,300 words) cover the architecture and capabilities of each system in full, with file-path citations on every claim.
- **Status:** SUCCESS (both primary sources fully fetched; the public docs site is blocked but the Mintlify source is in-repo).
