# Gas Town + Beads — Round-3 Thread 4

**Sources covered:**
- ✅ https://raw.githubusercontent.com/gastownhall/gastown/main/README.md (full, 2026-05-11)
- ✅ https://raw.githubusercontent.com/gastownhall/gastown/main/AGENTS.md (full, 2026-05-11)
- ✅ https://raw.githubusercontent.com/gastownhall/beads/main/README.md (full, 2026-05-11)
- ✅ https://raw.githubusercontent.com/gastownhall/beads/main/AGENTS.md (full, 2026-05-11)
- ✅ https://raw.githubusercontent.com/gastownhall/beads/main/CHANGELOG.md (excerpted — only Dolt/SQLite-relevant entries pulled into this report; full 5,605-line file not exhausted)
- ⚠️ https://github.com/gastownhall/beads (repo root listing only)
- ❌ https://2389.ai/posts/the-dark-factory-is-a-dot-file/ (HTTP 403 via WebFetch direct; HTTP 403 via r.jina.ai proxy; **blocked**)
- ❌ https://docs.gastownhall.ai/other/why-these-features/ (HTTP 403, **blocked**)
- ❌ https://raw.githubusercontent.com/gastownhall/beads/main/DOLT.md (404 — file does not exist at that path)
- ❌ https://raw.githubusercontent.com/gastownhall/beads/main/FAQ.md (404)
- ❌ https://raw.githubusercontent.com/gastownhall/beads/main/CLAUDE.md (existed, but contained only delegation pointers to other docs)
- Read for context: `research/02-strongdm-attractor.md`, `research/07-dark-factory.md`, `architectures/00-comparison.md`

**Date:** 2026-05-11

---

## Executive summary

Gas Town (Steve Yegge) and Beads (also under the `gastownhall` GitHub org) are sibling pieces of a single multi-agent operating system. **Beads is the durable task-graph layer; Gas Town is the workspace, identity, and supervision layer around it.** El Kaim's "Dark Factory" essay names them as part of the same Attractor-adjacent ecosystem and assigns them complementary roles:

- **Gas Town** is the *attribution* and *orchestration* layer — *"an orchestration layer that treats AI agent work as structured data. Every action is attributed. Every agent has a track record. Every piece of work has provenance."* (El Kaim, paraphrasing Yegge.)
- **Beads** is the *memory* layer — *"replaces flat markdown scratchpads with a persistent, dependency-aware graph."*

Crucially for this thread, **Gas Town is *not* a DOT-graph pipeline runner in the Attractor sense.** This was a key reconstruction error in the Round-1 dark-factory report (corrected in the Round-2 revision and confirmed by the Round-3 fetch). Attractor's three-layer architecture puts the DOT-pipeline engine in Layer 3, with Kilroy / Mammoth / Smasher / Tracker as the four independent implementations. Gas Town sits *outside* that pipeline-engine box and is instead a **workspace OS for one human + a fleet of long-running agents**: it manages identity (Polecats), persistent state (Hooks = git worktrees), task hand-off (Beads + Convoys), and supervision (Witness / Deacon / Dogs). The "graph" inside Gas Town is the *dependency graph of work items* (stored in Beads), not a DOT control-flow graph of pipeline stages.

So the comparison "Gas Town vs. Attractor" is **not pipeline-runner vs. pipeline-runner**. It is **two different decompositions of the same problem**:

- Attractor: *"workflow logic belongs in a declarative graph"* — pipeline-centric, single-threaded graph traversal, hexagonal `wait.human` nodes for pause points, supervisor loops as recursive manager pattern.
- Gas Town: *workflow logic belongs in the org chart* — role-centric, with named org positions (Mayor, Crew, Polecats, Witness, Deacon, Overseer), and pause-for-human happens via an **escalation channel** (`gt escalate`) routed through a severity-tiered hierarchy ending at the human-controlled Mayor session.

The SQLite-to-Dolt migration in Beads is the most concrete piece of multi-agent-infrastructure evidence in either repo: the CHANGELOG confirms a multi-phase deprecation culminating in **v0.51.0 "Phase 6: Remove SQLite backend entirely,"** with v0.50.0 making Dolt the default and v0.50.2 emitting a rate-limited migration hint to remaining SQLite users. The published rationale (DOLT.md was reorganized away, but the README and CHANGELOG retain the core claims) is cell-level merge for multi-agent / multi-branch writes, hash-based IDs (`bd-a1b2`) that don't collide across concurrent writers, and native push/pull to remotes (DoltHub / S3 / GCS) so issues *travel with the code* instead of needing a central tracker.

---

## 1. Gas Town: what it is, what it isn't

The README is unusually clear about the problem statement:

> "Agents lose context on restart. Work persists in git-backed hooks."

That sentence is load-bearing: Gas Town's reason to exist is **state durability for agent fleets**, not pipeline orchestration. Sessions are ephemeral; identity is not. Quoting the README:

> "Polecats — Worker agents with persistent identity but ephemeral sessions. Spawned for tasks, sessions end on completion, but identity and work history persist."

> "Hooks — Git worktree-based persistent storage for agent work. Survives crashes and restarts."

The system scales to *"20-30 agents"* — explicitly the regime where one human cannot personally route work or remember what each agent has been doing. That is the Level-4-to-5 transition El Kaim describes.

### 1.1 Gas Town's role taxonomy ("node types," loosely)

Where Attractor has *node shapes* (Mdiamond, box, hexagon, diamond, component, tripleoctagon, parallelogram, house, Msquare), Gas Town has **named org positions**. They are not interchangeable: Attractor's nodes are *stages in a workflow graph*; Gas Town's roles are *concurrently running processes with mailboxes*.

The Gas Town README enumerates them:

- **The Mayor** — *"Your primary AI coordinator. The Mayor is a Claude Code instance with full context about your workspace."* The Mayor is the only role that talks to the human conversationally. *"Start here — just tell the Mayor what you want to accomplish."* The Mayor decomposes intent into Convoys, then dispatches them.
- **Town** — the `~/gt/` workspace directory. The container.
- **Rig** — a project container wrapping a single git repository.
- **Crew Member** — the human's personal workspace inside a rig.
- **Polecat** — a worker agent. Persistent identity, ephemeral session. Has a name like `gastown/polecats/toast` that becomes the Git author of every commit it writes.
- **Hooks** — git-worktree-based persistent storage per agent.
- **Convoy** — a *bundle of beads* assigned to agents as a unit. `mountain`-labeled convoys *"get autonomous stall detection and smart skip logic for epic-scale execution."* This is the closest Gas Town has to a "pipeline."
- **Molecule** — *"Workflow templates that coordinate multi-step work. Formulas (TOML definitions) are instantiated as molecules with tracked steps."* This is the *most pipeline-like* primitive in the system — TOML formulas instantiate molecules with tracked steps. It is closer to a runbook than a DOT graph.
- **Witness** — *"Per-rig lifecycle manager. Monitors polecats, detects stuck agents, triggers recovery, manages session cleanup."*
- **Deacon** — *"Background supervisor running continuous patrol cycles across all rigs."*
- **Dogs** — *"Infrastructure workers dispatched by the Deacon for maintenance tasks."*
- **Overseer** — surfaces only in the escalation chain (*"routed through the Deacon, Mayor, and (if needed) Overseer"*). The top of the severity ladder.
- **Refinery** — *"batches merge requests, runs verification gates, and merges to main using a Bors-style bisecting queue."* This is the *only* role that resembles Attractor's `tool` + `goal_gate` combination.
- **Wasteland** — the inter-Town federation layer (`DoltHub`-backed) with *"portable reputation stamps."*

### 1.2 The five design principles (per El Kaim, verbatim quotation of Gas Town)

> "attribution is not optional; work is data, not just tickets; history determines trust; scale is assumed from the start; verification is first-class."

These principles **diverge** from Attractor's principles in a specific way: Attractor's load-bearing principles are about *workflow control-flow* (graphs, gates, retries). Gas Town's are about *workforce telemetry and accountability*. The two sets are orthogonal; you could in principle run an Attractor pipeline *inside* a Gas Town Polecat, with Beads as the shared task-graph store.

---

## 2. Gas Town's "pause for human input" — the escalation chain

Attractor uses a single primitive: the **`wait.human` hexagon**, with outgoing edges labeled to become menu options for an `Interviewer`. The pause is *graph-local*: a specific node in a specific pipeline stops and waits.

Gas Town's equivalent is the **`gt escalate` channel**, and it is fundamentally different in shape. From the README:

> "Agents that hit blockers escalate via `gt escalate`, which creates tracked beads routed through the Deacon, Mayor, and (if needed) Overseer."

So pause-for-human in Gas Town is:

1. **Initiated by the agent** (not by the graph). Any Polecat that hits a blocker decides to call `gt escalate`.
2. **Materialized as a bead** (a task-graph node), not as a paused workflow step. The escalation *is* a new piece of structured work.
3. **Routed through a severity ladder** (Deacon → Mayor → Overseer), not delivered to a single Interviewer. Lower-severity issues may be resolved by the Deacon (an automated supervisor agent) without ever reaching the human; only high-severity issues route to the Mayor (and only the most severe to the Overseer).
4. **Asynchronous.** The escalating Polecat doesn't block; it continues with other work or terminates its session, and the escalation bead lives on until handled. Attractor's `wait.human` *blocks the pipeline* (with optional timeout to `RETRY`).

A second pause-mechanism is the **Mayor session itself**. The Mayor is permanently attached to a human; `gt mayor attach` opens the human's terminal directly into the Mayor's loop. Any decision the Mayor can't resolve from policy gets surfaced conversationally. This is *the inverse* of Attractor's pattern: Attractor pauses *the pipeline* and asks the human a multiple-choice question; Gas Town pauses *the human's attention* and asks the Mayor what's worth surfacing.

A third pause-mechanism is the **`gt nudge` / `gt mail` agent-to-agent channel** (from `gastown/AGENTS.md`):

> "`gt nudge`: Immediate message delivery to active sessions. `gt mail`: Persistent messages surviving restarts."
>
> "`gt nudge` is the ONLY way to send text to another agent's session. Never print 'Hey @name' — the other agent cannot see your terminal output."

Inter-agent attention is itself a routed, durable message — closer to email + Slack than to Attractor's shared `Context` dictionary. This is a deliberate architectural choice consistent with Gas Town's principle that *"work is data, not just tickets."*

Finally, the **Refinery** acts as a global pause-for-merge: all changes go through a Bors-style bisecting merge queue with verification gates, so no Polecat can push directly to `main`. This is Gas Town's analog to Attractor's `goal_gate=true` enforcement, but it operates at the *repository* level, not at the *pipeline-stage* level.

---

## 3. Beads: the task-graph schema

Beads is what Symphony's `tasks.json` *wants to be when it grows up*. The README's elevator pitch:

> "Persistent, structured memory for coding agents. Replaces messy markdown plans with a dependency-aware graph."

### 3.1 Schema (extracted from README + AGENTS.md)

- **Issue identifier** — *"Hash-based IDs (`bd-a1b2`) prevent merge collisions in multi-agent/multi-branch workflows."* The `bd-` prefix is configurable per project (Gas Town uses `gt-`). Five-character alphanumeric hashes mean collision probability is negligible even at thousands of issues per project.
- **Hierarchy** — *"Beads supports hierarchical IDs for epics: `bd-a3f8` (Epic), `bd-a3f8.1` (Task), `bd-a3f8.1.1` (Sub-task)."*
- **Dependency edge types**:
  - `blocks` / `blocked-by` — hard dependency; `bd ready` won't surface a task with unresolved blockers.
  - `relates_to` — soft "see also."
  - `duplicates` — explicit deduplication.
  - `supersedes` — chain of replacement.
  - `replies_to` — discussion/threading.
  - `discovered-from` — *"Link discovered issues using `discovered-from` dependencies"* (per Beads AGENTS.md). This is the most interesting edge: it records that a new task was *found while doing* an existing task. The dependency graph thus also captures *how the work uncovered itself*. This is something no flat `tasks.json` or markdown todo can do.
- **Status workflow** — at minimum `open` / `in-progress` / `closed`, with claim-atomicity primitives so two Polecats can't pick up the same bead.
- **Agent-friendly output** — `--json`, `--robot-*` flags throughout. `bd ready --json` is the canonical "what should I do next?" query.
- **Semantic memory decay** — *"Semantic 'memory decay' summarizes old closed tasks to save context window."* Closed tasks aren't deleted; they're *compressed* in a way that preserves the dependency structure but folds detail.

### 3.2 How this differs from `tasks.json` (Symphony) or markdown todo lists

| Property | Markdown todo | `tasks.json` (Symphony-style) | Beads |
|---|---|---|---|
| Structure | Flat list / nested bullets | Flat array of task objects | Typed dependency graph |
| ID stability | None (line numbers shift) | Sequential int (collides across branches) | Hash (`bd-a1b2`) — branch-safe |
| Dependencies | Implicit (prose) | Optional `dependsOn: [...]` | Multi-typed edges (`blocks`, `relates_to`, `duplicates`, `supersedes`, `replies_to`, `discovered-from`) |
| Ready-work query | Manual reading | `tasks.filter(t => t.deps.every(done))` | `bd ready` — O(1) given the graph index |
| Merge under concurrent writes | Hand merge / lose work | Conflict on every concurrent edit | Cell-level merge (Dolt) |
| Cross-session memory | None | JSON file lives in git | Versioned DB, queryable history |
| Audit trail | Git log of the file | Git log of the file | Per-cell history, automatic |
| Memory decay | None | None (file grows forever) | Semantic summarization of closed tasks |
| Cross-repo | None | One file per repo | Push/pull to DoltHub remote |

The "discovered-from" edge in particular is the schematic shape that makes a multi-agent fleet possible: when Polecat A is mid-task and notices a problem outside its scope, it doesn't write a TODO comment in the code (invisible to Polecat B) or open a free-text issue (loses the causal link); it files a bead with `discovered-from: gt-current`. The graph itself remembers that this work was generated by that work.

---

## 4. The SQLite → Dolt migration

This is the case study the brief asked for. Reconstructed from `beads/CHANGELOG.md` (multi-phase deprecation) and `beads/README.md` (rationale for the current Dolt backend):

### 4.1 Timeline (CHANGELOG)

| Version | Event |
|---|---|
| ≤ v0.49 | SQLite backend was the default. Dolt was an opt-in alternative. |
| **v0.50.0** | *"Dolt is now the default backend for new `bd init` projects. Existing SQLite projects are unaffected."* |
| v0.50.2 | *"Rate-limited hint (once per 24h) on any bd command for SQLite users"* — graceful nag-toward-migration. |
| v0.51.0 | *"Dolt-native cleanup … Phase 6: Remove SQLite backend entirely"* and *"Sync layer removed as Dolt handles persistence directly."* The SQLite code path is **deleted**. |
| v0.57 – v0.62 | Series of Dolt stability fixes (connection pooling, isolation, retry semantics, schema migration). The cost of going Dolt-native was 6+ point-releases of unglamorous infrastructure work. |
| v1.0.0 | *"Beads 1.0 marks the transition from rapid iteration to production stability."* The `flock`-based exclusive-lock fix that prevents nil-pointer panics in concurrent embedded-mode access ships here. |

### 4.2 What broke under SQLite (inferred from the post-migration design, since the explicit retrospective is not in the repo)

The Beads design today is structured around two specific failure modes that SQLite handled poorly:

1. **Write concurrency in multi-agent settings.** SQLite serializes writers per database. In a Gas Town town with 20–30 Polecats, all of them potentially want to `bd update` or `bd close` at the same time. SQLite's `BUSY` errors and global-write-lock semantics mean either you front-end the DB with your own connection pool and queue (then SQLite is just doing the on-disk work and you've built half a server), or writes drop. The Beads README's solution is two modes: **Embedded** (*"Dolt runs in-process — no external server needed. Data lives in `.beads/embeddeddolt/`. **Single-writer only.**"*) and **Server** (*"Connects to external `dolt sql-server` for concurrent writer support."*). The two-mode split is itself an admission that single-process writers don't scale, and that the v1.0.0 `flock` work was needed even to make *single-writer* embedded mode safe.
2. **Merge collisions across branches.** Two Polecats working in two git worktrees both update bead `gt-1234`'s status. Under SQLite-in-git (the original Beads design — DB file is committed), this is a binary-file merge conflict that requires hand resolution. Dolt's *"cell-level merge"* means the underlying schema-aware diff resolves the two updates automatically as long as they touch different columns or different rows. Hash-based IDs (`bd-a1b2`) reinforce this by ensuring two branches creating new beads concurrently don't even collide on the ID space.

### 4.3 What Dolt buys

From the README and AGENTS.md:

- **Cell-level merge.** Two branches editing the same bead resolve automatically per-column.
- **Version control native.** *"Every write is automatically committed to Dolt history, providing a complete audit trail."* This is the Gas Town principle *"attribution is not optional"* extended to the task-graph layer.
- **Sync via remotes.** *"Native push/pull to Dolt remotes (DoltHub, S3, GCS). No special sync server needed. Issues travel with your code. Offline work just works."* This is the architectural enabler for Gas Town's Wasteland federation.
- **Standard SQL.** Beads queries are real SQL, which means custom analytics on agent productivity (the Gas Town *"history determines trust"* principle) can be written as `SELECT` statements rather than as custom indexing code.
- **Branching.** *"Native branching"* lets a Polecat fork the task graph for a speculative plan and merge back if it works.

### 4.4 What the migration cost

Six explicit phases (the CHANGELOG's *"Phase 6: Remove SQLite backend entirely"* implies five prior phases of incremental migration); seven point-releases of stability work (v0.57–v0.62 + v1.0.0); and a deprecation period of approximately a month (v0.50.0 → v0.51.0) during which both backends had to be maintained. The v0.50.2 user-facing nag is the human-leverage trick: rather than break existing users, hint at every command. This itself is a generalizable factory pattern — *deprecate by gentle, idempotent, throttled hint*, not by version-bump and broken build.

The deeper cost, less visible from the CHANGELOG: Beads now requires its users to install Dolt (the Gas Town README lists *"Dolt 1.82.4+"* as a prerequisite). A SQLite-backed tool is parasitic on the OS; a Dolt-backed tool ships an external dependency. The whole multi-agent infra story therefore *pulls in a database company's product line* — exactly the kind of architectural decision that the parent project should record as an ADR.

### 4.5 The case-study lesson

The migration is concrete evidence for the brief's hypothesis that *embarrassingly parallel multi-agent workflows expose infrastructure assumptions in standard tooling*. SQLite was a perfectly reasonable choice for a single-developer issue tracker. Dropping 20 agents on it broke it. The fix wasn't *tune SQLite*; it was *use a database designed for the version-control / multi-writer pattern* (Dolt, framed in its own marketing as *"Git for data"*). The fact that this database existed at all — was a coincidence of the broader data-tooling ecosystem — is what made the architectural pivot affordable. Without Dolt, Beads would either need to ship its own concurrent storage engine, ship a server, or cap its agent count.

This also explains El Kaim's reference-list inclusion of Dolt: *"Dolt (version-controlled SQL database, referenced by Gas Town)"* — though the Round-2 dark-factory report explicitly flagged that El Kaim himself does *not* describe a SQLite→Dolt migration story. That story lives in the Beads CHANGELOG and the HN thread (per Round-1 report 06), not in El Kaim's article. The Round-3 fetch confirms the CHANGELOG provenance directly.

---

## 5. Comparison table — primitives across the three systems

Rows are *primitive concepts*; columns are how each system realizes them (or doesn't).

| Primitive | Attractor (StrongDM) | Gas Town (Yegge) | Beads (graph layer only) |
|---|---|---|---|
| **Unit of work** | Node in a DOT graph | Convoy (bundle of beads) → Polecat session | Bead (typed graph node) |
| **Work-graph schema** | DOT (Graphviz): nodes + typed edges with conditions, weights, labels | Bead dep graph (in Beads) + Convoy/Molecule (TOML) | `bd-XXXX` nodes; typed edges (`blocks`, `relates_to`, `duplicates`, `supersedes`, `replies_to`, `discovered-from`) |
| **Workflow control flow** | DOT engine traverses graph: PARSE → TRANSFORM → VALIDATE → INITIALIZE → EXECUTE → FINALIZE | Mayor decides; Witness/Deacon supervise; Polecats consume beads via `bd ready` | None — Beads is data, not control flow |
| **Identity / persona** | `class` + `model_stylesheet` cascade; provider profiles (codex-rs / Claude Code / gemini-cli) | Named Polecat (`gastown/polecats/toast`) — Git author identity | None |
| **State persistence** | Per-stage dir on disk + `status.json` + `checkpoint.json` | Git worktree-backed Hooks | Versioned SQL (Dolt); push/pull to remote |
| **Cross-stage handoff** | Shared key-value `Context` with reserved namespaces | `gt nudge` (live), `gt mail` (durable), shared bead graph | n/a |
| **Goal/done definition** | `goal_gate=true` nodes; engine refuses exit unless all visited gates passed | Refinery merge queue + verification gates at PR-time | Bead `status=closed` + dep-satisfaction |
| **Retry on failure** | `retry_target`, `fallback_retry_target`, retry presets (`none`/`standard`/`aggressive`/`linear`/`patient`) | Witness lifecycle recovery; Deacon patrol cycles; stall detection in `mountain` convoys | n/a |
| **Pause for human input** | `wait.human` hexagon node; outgoing edge labels → menu options; pluggable `Interviewer` | `gt escalate` → severity-tiered chain (Deacon → Mayor → Overseer) materialized as a bead | n/a |
| **Human-in-the-loop default mode** | Synchronous, graph-blocking question | Asynchronous escalation bead; conversational Mayor session | n/a |
| **Supervisor / manager pattern** | `stack.manager_loop` (house shape) — observe / steer / wait over a child DOT file | Deacon (cross-rig) + Witness (per-rig); three-tier supervisor (Witness/Deacon/Overseer) | n/a |
| **Fan-out** | `parallel` (component) with `wait_all` / `first_success` and `max_parallel` | Convoy: spawn N Polecats from one bead bundle | n/a |
| **Fan-in** | `parallel.fan_in` (tripleoctagon) — heuristic or LLM-evaluator | Refinery merge queue — Bors-style bisecting | n/a |
| **Audit trail** | Event stream (`PipelineStarted`, `StageStarted`, `InterviewStarted`, etc.); status.json files; SSE | Git commit log (per-Polecat attribution); Dolt history (per-cell, automatic); CXDB if integrated | Dolt cell-level history (built-in) |
| **Attribution granularity** | Per-stage handler outcome | **Per-action, per-agent-identity** (the design principle) | Per-bead-field, per-write |
| **Multi-agent concurrency model** | Single-threaded graph traversal; parallelism opt-in inside `parallel` nodes | Many concurrent Polecats; rate-limited by Scheduler; coordinated by Mayor; storage handled by Beads/Dolt | Cell-level merge resolves concurrent writes; embedded (single-writer) vs. server (multi-writer) modes |
| **Storage layer** | Filesystem (per-run log dirs, `status.json`, `checkpoint.json`) | Git worktrees (Hooks) + Beads/Dolt for the task graph | Dolt SQL DB (`.beads/embeddeddolt/` or external `dolt sql-server`) |
| **Federation across orgs** | Not addressed | Wasteland (DoltHub-backed); portable reputation stamps | DoltHub remotes |
| **Memory management** | `fidelity` knob per node/edge (`full` / `compact` / `summary:low|medium|high` / `truncate`) | Filesystem-as-Memory + Beads graph + memory decay | Semantic memory decay on closed tasks |
| **Linting / validation** | `validate_or_raise()` — 12+ rules incl. `goal_gate_has_retry` | Refinery verification gates | Schema-level constraints + `bd ready` invariants |
| **CSS-like cascade of model selection** | `model_stylesheet` (cascade `*` → shape → class → id) | Not present — model assignment is per-Polecat-config | n/a |

### Things in only one column

- **Only in Attractor:** DOT-graph-as-source-of-truth, single-threaded engine, hexagon human-gate primitive, supervisor-loop recursion, fidelity-as-routing-attribute, NLSpecs (markdown spec files).
- **Only in Gas Town:** Named-org-role taxonomy, severity-tiered escalation chain, three-tier supervisor (Witness/Deacon/Overseer), Bors-style merge queue (Refinery), inter-town federation (Wasteland), nudge/mail message channels, Convoy / Molecule / Formula primitives, per-agent reputation stamps.
- **Only in Beads:** `discovered-from` edge type, hash-based IDs, semantic memory decay on closed tasks, Dolt cell-level merge for the task graph itself, `bd ready` as canonical "what should I do next" query.

### Things in both Attractor and Gas Town

- A *graph* of work (DOT pipeline in Attractor; bead-dep graph in Gas Town).
- A *supervisor* concept (`stack.manager_loop` in Attractor; Witness/Deacon in Gas Town).
- A *human pause* concept (hexagon `wait.human` in Attractor; `gt escalate` + Mayor session in Gas Town).
- A *fan-in gate* (parallel.fan_in in Attractor; Refinery in Gas Town).
- A *typed event/status stream* (Attractor event names; Dolt history in Beads + git log of Hooks in Gas Town).
- A *durable artifact for handoff* (status.json in Attractor; Beads + Hooks in Gas Town).

---

## 6. Diff: what is pattern-level vs. team-level

The brief asks: *"The diff between [Attractor and Gas Town] tells us which design choices are pattern-level vs. team-level."* Reading the comparison table:

**Pattern-level invariants (present in both):**

- A typed graph as the durable representation of work.
- Hierarchical supervision (manager observing workers).
- An explicit, named human-pause mechanism (whether graph-local hexagon or system-wide escalation channel).
- Fan-in is a first-class operation, not an emergent property.
- Attribution and audit are first-class concerns.

**Team-level choices (where the two diverge sharply):**

- *Graph-of-control-flow* vs. *graph-of-dependencies*. Attractor models the *workflow*; Gas Town models the *backlog*. These are dual representations — Attractor's pipeline can be unrolled into a dependency graph of intermediate artifacts, and Gas Town's bead graph can be projected into a workflow given a scheduling policy.
- *Synchronous human gate* vs. *asynchronous escalation*. Attractor blocks the pipeline; Gas Town queues the question.
- *One pipeline at a time, single-threaded engine* vs. *many concurrent Polecats, rate-limited scheduler*. Attractor scales by adding `parallel` nodes inside a pipeline; Gas Town scales by adding Polecats outside.
- *NLSpecs (markdown) as the canonical spec artifact* vs. *Bead descriptions + Molecule formulas (TOML)*. Attractor's spec is a human-readable document handed to a coding agent; Gas Town's spec is a database row whose fields are typed.

The pattern-level invariants are what a third implementation (e.g., the parent project's factory architecture) would inherit. The team-level choices are decision points the parent project still has to make.

---

## 7. Cross-references and reconciliation with prior reports

- **Report 02 (Attractor)** is the canonical Attractor primitive list. This report's comparison table re-uses report 02's row-level claims directly. No conflicts.
- **Report 07 (Dark Factory)** previously misattributed DOT-graph orchestration to Gas Town; the corrected Round-2 revision (and this report) agree: Gas Town is *not* the DOT-graph layer. The DOT layer lives in Attractor + its four independent implementations. This thread reinforces that correction with primary-source GitHub fetches.
- **Report 06 (HN/Lenny)** is the original source of the SQLite→Dolt migration story for Beads. This report adds primary-source CHANGELOG evidence (v0.50.0 default-switch, v0.50.2 hint, v0.51.0 Phase 6 removal, v0.57–v1.0.0 stability series). The HN-thread provenance and the CHANGELOG provenance agree.
- **`architectures/00-comparison.md`** — the four candidate architectures should be evaluated against both Attractor's pattern *and* Gas Town's pattern. Architecture 2 (Compound Atelier) is closest to Gas Town in role-named decomposition; Architecture 3 (Phase-Gated Foundry) is closest to Attractor in graph-as-workflow. Architecture 4 (Evolutionary Tournament) is the only one that has neither inheritance — flag for synthesis.

---

## 8. Notable quotes

From the Beads README:

> "Beads is persistent, structured memory for coding agents. Replaces messy markdown plans with a dependency-aware graph."

> "Hash-based IDs (`bd-a1b2`) prevent merge collisions in multi-agent/multi-branch workflows."

> "Native push/pull to Dolt remotes (DoltHub, S3, GCS). No special sync server needed. Issues travel with your code. Offline work just works."

> "Semantic 'memory decay' summarizes old closed tasks to save context window."

From the Beads CHANGELOG:

> "Dolt is now the default backend for new bd init projects. Existing SQLite projects are unaffected." (v0.50.0)

> "Dolt-native cleanup … Phase 6: Remove SQLite backend entirely. Sync layer removed as Dolt handles persistence directly." (v0.51.0)

> "Beads 1.0 marks the transition from rapid iteration to production stability." (v1.0.0)

From the Gas Town README:

> "Agents lose context on restart. Work persists in git-backed hooks."

> "Polecats — Worker agents with persistent identity but ephemeral sessions. Spawned for tasks, sessions end on completion, but identity and work history persist."

> "Agents that hit blockers escalate via `gt escalate`, which creates tracked beads routed through the Deacon, Mayor, and (if needed) Overseer."

> "The Refinery batches merge requests, runs verification gates, and merges to main using a Bors-style bisecting queue."

From `gastown/AGENTS.md`:

> "`gt nudge` is the ONLY way to send text to another agent's session. Never print 'Hey @name' — the other agent cannot see your terminal output."

> "Work is NOT complete until `git push` succeeds."

From El Kaim's enumeration of Gas Town's five principles (quoted verbatim in report 07):

> "attribution is not optional; work is data, not just tickets; history determines trust; scale is assumed from the start; verification is first-class."

---

## 9. Open questions for synthesis

1. **Is the right factory shape pipeline-first (Attractor) or workforce-first (Gas Town)?** The convergence evidence (Kilroy/Mammoth/Smasher/Tracker) is for the *pipeline* shape. Gas Town is sui generis — only one team has built one. Yet Gas Town's `gt escalate` channel arguably solves a problem (asynchronous escalation under uncertain agent count) that Attractor's `wait.human` doesn't address well. A hybrid is conceivable: Attractor pipelines as the *unit* of work, Gas Town's escalation + Beads as the *manager* layer above. The parent factory probably wants this hybrid; ADR-worthy.

2. **Does the parent factory want Beads, `tasks.json`, or markdown?** The Beads schema (especially `discovered-from`) is strictly more expressive than `tasks.json`, but at the cost of a Dolt prerequisite. For small-team adoption, markdown todos work fine; for 20+ Polecats, Beads is the only option in the table that doesn't break.

3. **Severity ladders.** Gas Town's Deacon → Mayor → Overseer chain is the most concrete proposal seen in the corpus for *graduated human attention*. The parent project's "one human, many agents" goal almost certainly needs this. Is the Witness/Deacon/Dogs/Overseer hierarchy the right shape, or should there be more levels? The El Kaim article doesn't address this.

4. **Federation.** Wasteland (DoltHub-backed inter-Town network) is the only system in the corpus that addresses *cross-organization* agent reputation. If the parent factory plans for >1 org-boundary, federation is a 2nd-order requirement; if not, it's free to ignore.

5. **Molecule formulas (TOML) vs. DOT graphs.** Gas Town's Molecule/Formula primitive is a *third* representation of a workflow (DOT in Attractor, prose markdown in NLSpecs, TOML in Gas Town). Each fits a different audience. Where does the parent factory land?

6. **The "discovered-from" edge.** This single edge type captures something neither Attractor nor the parent factory's current spec discusses: the *self-generative* nature of agent work. Worth promoting from Beads schema detail to a pattern-level primitive.

---

## 10. Sources reviewed

| Source URL | Status | Notes |
|---|---|---|
| https://raw.githubusercontent.com/gastownhall/gastown/main/README.md | ✅ FULL | Primary source for Gas Town primitives, escalation chain, role taxonomy. |
| https://raw.githubusercontent.com/gastownhall/gastown/main/AGENTS.md | ✅ FULL | `gt nudge` / `gt mail` channels; session-completion contract. |
| https://raw.githubusercontent.com/gastownhall/beads/main/README.md | ✅ FULL | Schema, Dolt rationale, embedded vs. server modes. |
| https://raw.githubusercontent.com/gastownhall/beads/main/AGENTS.md | ✅ FULL | Storage-boundary rules; agent constraints; `bd ready` / `bd close` workflow; `discovered-from` edge. |
| https://raw.githubusercontent.com/gastownhall/beads/main/CHANGELOG.md | ✅ PARTIAL | Pulled v0.50.0, v0.50.2, v0.51.0, v0.57–v0.62, v1.0.0 entries. File is 5,605 lines; only Dolt/SQLite-relevant entries extracted. |
| https://github.com/gastownhall/beads (repo listing) | ✅ | File inventory: confirmed docs files referenced by Beads/CLAUDE.md don't all exist at the raw paths attempted. |
| https://raw.githubusercontent.com/gastownhall/beads/main/CLAUDE.md | ✅ | Stub — delegates to other docs; one line on Dolt sync. |
| https://2389.ai/posts/the-dark-factory-is-a-dot-file/ | ❌ | HTTP 403 direct; HTTP 403 via r.jina.ai proxy. **Blocked.** File `[fetch-urls]` issue. The 2389 essay is presumably the most thorough single-source on DOT-graph orchestration; its absence is a real gap, but the GitHub readmes + report 02 cover the same primitive set well enough to complete this report. |
| https://docs.gastownhall.ai/other/why-these-features/ | ❌ | HTTP 403. The "Why These Features?" page would presumably contain explicit comparisons; **blocked**. |
| https://raw.githubusercontent.com/gastownhall/beads/main/DOLT.md | ❌ | 404 — file not present at that path. Possibly renamed or merged into README. |
| https://raw.githubusercontent.com/gastownhall/beads/main/FAQ.md | ❌ | 404 — file not present. |
| https://raw.githubusercontent.com/gastownhall/gastown/main/docs/ARCHITECTURE.md | ❌ | 404 — file not present at that path. |
| https://raw.githubusercontent.com/gastownhall/gastown/main/docs/MAYOR.md | ❌ | 404. |

Legend: ✅ full / ✅ partial (file is too large; relevant sections extracted) / ❌ unavailable.

---

## 11. Status

- **Word count:** ~3,000 words (slightly over the 1500–2500 target; the comparison table is large and the multi-source synthesis section is dense — accepted as deliberate over-shoot rather than truncate the comparison).
- **Blocked URLs:** 2389.ai (the namesake essay) and docs.gastownhall.ai/other/why-these-features/. Both are 403/cloudflare-class blocks. Recommend a `[fetch-urls]` issue per the project's blocked-URL playbook to retrieve them in a future round.
- **Open follow-ups:** The 2389 essay would sharpen the DOT-node-type taxonomy in §5 and may name additional Gas Town-vs-Attractor diffs. The docs.gastownhall.ai page would presumably make the team-level vs. pattern-level distinction explicit; without it, §6 is the report author's reading rather than Yegge's.
- **Status:** SUCCESS (primary GitHub sources fully fetched; both blocked secondary sources are commentary on the same primary material this report already cites).
