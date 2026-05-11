# Research Plan — Round 2: Jaymin West Book, Overstory, OpenHands

**Branches:** `claude/research-agentic-engineering-YxbW1` (initial plan, merged in PR #3); `claude/round-2-research-consolidation` (current — see `git log`).
**Date opened:** 2026-05-10
**Status:** **Mid-stream as of 2026-05-11.** Fetch action operational. Tier-1 web content retrieved (issue #4). Three reports written *by the lead agent in place of subagents* (08, 11, 12 — see §10 *Round-2 progress log*). Reports 08 (Foundations + Patterns), 10 (Overstory substrate audit), and the unfetched portions of 09 (Practices + Mental Models) are still pending; report 13 (synthesis) blocks on them. See §10 for next-action checklist. **§11 catalogs 12 Round-3 follow-up research threads** consolidated 2026-05-11 from a former root-level `followup.md`; these are post-Round-2 work and are not blocking anything in §10.
**Lead question:** *What can we reuse — patterns, vocabulary, or working code — from these three sources to build the software factory described in `architectures/`, given that we want to operate as a CI/CD pipeline rather than an interactive desktop?*

---

## 1. Why these sources

Three new sources have been identified beyond the Round-1 corpus already digested in `research/01-` through `research/07-`:

1. **Jaymin West — *Agentic Engineering: The Book*** ([jayminwest.com/agentic-engineering-book](https://www.jayminwest.com/agentic-engineering-book) / [github.com/jayminwest/agentic-engineering-book](https://github.com/jayminwest/agentic-engineering-book)). A 10-chapter book, CC BY-NC-SA, **written and maintained using its own subject matter** (agentic workflows on Claude Code). It contains an explicit chapter on "Software Factories" (9.7) and another on "Specs as Source Code" (9.3) — direct doctrinal overlap with our `spec-driven-ai-dev.md` baseline and our `architectures/0N-*.md` set. The book's appendix lists four working examples: **gastown, kotadb, overstory, pi-mono**. Several of those examples already appeared in the Round-1 corpus (gastown via El Kaim's Dark Factory write-up).

2. **Overstory** ([github.com/jayminwest/overstory](https://github.com/jayminwest/overstory)). Also by Jaymin West, MIT-licensed. A multi-agent orchestration framework that "turns a single coding session into a multi-agent team by spawning worker agents in isolated git worktrees, coordinating them through a custom SQLite mail system, and merging their work back with tiered conflict resolution." Supports **11 runtime adapters** (Claude Code, Pi, Gemini CLI, Aider, Goose, Amp, …) via a pluggable `AgentRuntime` interface. **This is the most architecturally complete open-source analog to the substrate `architectures/00-comparison.md` §4 calls "the shared infrastructure all four architectures need."**

3. **OpenHands** ([github.com/All-Hands-AI/OpenHands](https://github.com/All-Hands-AI/OpenHands)). MIT-licensed core (with an `enterprise/` exception). Five deployment surfaces: composable Python SDK, CLI, local GUI with REST API, cloud-hosted, and self-hosted enterprise. Has a **headless mode** documented for CI/CD use, a **GitHub Action** (`openhands-github-action`) on the marketplace, and a documented `Software Agent SDK` (paper: arXiv 2511.03690) that "scales to 1000s of agents in the cloud." **This is the most CI/CD-ready piece of public agent infrastructure that exists.**

The user's framing question is correct and worth pinning at the top of every subagent prompt:

> *Maybe not a lot, since we want to run as a CI/CD pipeline. But there must be some inspiration here.*

The Round-1 corpus had no entry that was both (a) open source and (b) CI/CD-shaped. Adding these closes that gap.

---

## 2. Initial analysis (what the lead agent established before dispatch)

What the scout pass already established, so subagents do not have to redo it:

### 2.1 Reachability from the sandbox

| URL | Status from sandbox |
|---|---|
| `https://www.jayminwest.com/agentic-engineering-book` (book web view, daily-rebuilt) | ❌ 403 |
| `https://github.com/jayminwest/agentic-engineering-book` (repo source of book) | ✅ via `raw.githubusercontent.com` |
| `https://github.com/jayminwest/overstory` | ✅ via `raw.githubusercontent.com` and GitHub API |
| `https://github.com/All-Hands-AI/OpenHands` | ✅ via `raw.githubusercontent.com` and GitHub API |
| `https://docs.all-hands.dev/...` | ❌ 403 |
| `https://jayminwest.substack.com/p/a-manifesto-for-agentic-development` | ❌ 403 |
| `https://arxiv.org/abs/2511.03690` (OpenHands SDK paper) | ❌ 403 |
| `https://www.langchain.com/blog/agentic-engineering-redefining-software-engineering` | ❌ 403 |
| `https://youtube.com/...` (Jaymin's videos) | ❌ 403 |

The sandbox blocks essentially every host except `raw.githubusercontent.com` and the GitHub MCP. **The book and Overstory are therefore mostly fetchable from inside the sandbox via raw URLs.** OpenHands' code is also fetchable; its docs and the SDK paper are not. See `research/blocked-urls-round-2.md` (companion file) for the precise URL inventory the GitHub Action should fetch.

### 2.2 Structural map of each source

**Jaymin West book — Table of Contents (verbatim from `TABLE_OF_CONTENTS.md`):**

- Part 1 (Foundations): Ch 1 Foundations, Ch 2 Prompt, Ch 3 Model, Ch 4 Context, Ch 5 Tool Use, Ch 6 Harnesses
- Part 2 (Craft): Ch 7 Patterns (11 patterns incl. Plan-Build-Review, Orchestrator, Autonomous Loops/Ralph Wiggum, ReAct, Expert Swarm, Multi-Agent Collaboration), Ch 8 Practices (Debugging, Evaluation, Cost & Latency, Production, Workflow Coordination, Knowledge Evolution, Operating Agent Swarms)
- Part 3 (Perspectives): Ch 9 Mental Models (Pit of Success, Prompt Maturity, **Specs as Source Code**, **Context as Code**, Execution Topologies, Design as Bottleneck, **Software Factories**), Ch 10 Practitioner Toolkit (Claude Code, Google ADK, IDE Integrations, Agent Frameworks, Multi-Agent Workspace Managers, Enterprise Codebase Context Tools)
- Appendices/Examples: **gastown, kotadb, overstory, pi-mono**

The bolded chapters have direct doctrinal overlap with our `architectures/` set and should be read first.

**Overstory — top-level layout:**

- `.canopy/`, `.claude/`, `.github/`, `.mulch/`, `.overstory/`, `.pi/`, `.sapling/`, `.seeds/` (many runtime-specific config dirs — Overstory itself appears to use the same set of agentic config dirs it integrates with)
- `agents/` (agent role definitions)
- `docs/` (architecture docs)
- `scripts/`, `src/`, `templates/`, `ui/`
- Top-level: `CLAUDE.md`, `STEELMAN.md` (the steelman case), `SECURITY.md`, `CHANGELOG.md`, `README.md`, plus `package.json`/`bun.lock` (Bun + TypeScript)

**OpenHands — top-level layout:**

- `openhands/` (core Python package), `openhands-ui/`, `frontend/`
- `.openhands/`, `.agents/`, `skills/` (agent skills)
- `containers/`, `kind/` (Kubernetes-in-Docker), `dev_config/`, `docker-compose.yml`
- `enterprise/` (source-available, separately licensed)
- `tests/`, `scripts/`, `.github/`, `pyproject.toml`, `poetry.lock`, `uv.lock`, `Makefile`, `config.template.toml`
- Companion repos (not yet fetched): `OpenHands-CLI`, `software-agent-sdk`, `openhands-github-action`

### 2.3 Pre-judgment of likely reusability

This is **lead-agent prejudice and should be checked, not trusted**, by the subagents:

- **Overstory's `AgentRuntime` adapter interface, SQLite mail system, worktree isolation, and 4-tier merge queue** are very likely the highest-leverage reusable artifacts in the entire Round-1+2 corpus. They map almost 1:1 to `architectures/00-comparison.md` §4.1 ("shared infrastructure: worktree per unit of work, sandboxed agent execution, manager loop / orchestrator"). The cost shape question is whether Bun/TypeScript is acceptable as a substrate or whether we'd want to re-implement in Python to match OpenHands.
- **OpenHands' SDK + headless mode + GitHub Action** are very likely the highest-leverage reusable artifacts for the *CI/CD pipeline* framing the user emphasized. The trade-off is provider lock-in and the weight of the OpenHands runtime model vs. running Claude Code as a subprocess.
- **Jaymin's book** is most likely a *vocabulary* contribution — terms like "Harness," "Execution Topologies," "Prompt Maturity Model," and the Ralph Wiggum/Autonomous Loop pattern — and a *cross-check* on whether our `architectures/` set has blind spots. It is unlikely to provide reusable code; it is likely to provide reusable mental models and a way to talk about them.
- **The "Software Factories" chapter (9.7)** specifically should be diffed against `architectures/00-comparison.md` because the chapter heading is the same.

These prejudgments should be either confirmed-with-evidence or refuted in the subagent reports.

---

## 3. Subagent assignments (parallelizable)

Six subagents, dispatchable in a single parallel batch. Each produces one report in `research/` numbered `08-` through `13-`. A seventh sequential synthesis agent reads all six and updates the existing comparison documents.

| # | Agent | Output file | Depends on |
|---|---|---|---|
| 08 | Book Part 1 + Patterns (foundations + Ch 7) | `research/08-jaymin-book-foundations-patterns.md` | — |
| 09 | Book Harnesses + Practices + Mental Models (Ch 6, 8, 9) | `research/09-jaymin-book-harnesses-practices-mental-models.md` | — |
| 10 | Overstory — full substrate audit | `research/10-overstory-substrate-audit.md` | — |
| 11 | OpenHands — full substrate audit, CI/CD lens | `research/11-openhands-substrate-audit.md` | — |
| 12 | Adjacent ecosystem — gastown, kotadb, pi-mono, agent frameworks in Ch 10 | `research/12-adjacent-ecosystem.md` | — |
| 13 | (sequential, runs last) Synthesis + diff against existing architectures | `research/13-round-2-synthesis.md` | 08-12 |

### 3.1 Subagent 08 — Jaymin Book Foundations + Patterns

**Goal:** Establish what Jaymin's book says about the topics that anchor our existing architecture catalog: prompt structure, model selection, context management, tool design, and the 11 named patterns in Chapter 7. Find areas of agreement, areas of disagreement, and any vocabulary we should adopt.

**Prompt to give the subagent (use Explore for low-cost reads, general-purpose if reads aren't enough):**

> You are reading a portion of Jaymin West's open-source book *Agentic Engineering*. Read the following files from the GitHub repo `jayminwest/agentic-engineering-book` via raw.githubusercontent.com (substitute `chapters/...` paths as appropriate). The branch is `main`.
>
> **Files to read:**
> - `chapters/1-foundations/_index.md` and all sub-files
> - `chapters/2-prompt/_index.md` and all sub-files
> - `chapters/3-model/_index.md` and all sub-files
> - `chapters/4-context/_index.md` and all sub-files
> - `chapters/5-tool-use/_index.md` and all sub-files
> - `chapters/7-patterns/_index.md` and all sub-files
>
> **Constraints:** Do NOT read chapters 6, 8, 9, 10 (subagent 09 owns those). Do NOT read existing reports in `research/01-` through `research/07-` — those reports cover different sources and you should reach your own conclusions independently. You MAY read `architectures/00-comparison.md` for context on what design decisions we have already made, since your job includes diffing the book against them.
>
> **Report structure** (write to `research/08-jaymin-book-foundations-patterns.md`):
> 1. One-paragraph summary of the book's worldview from these chapters.
> 2. The "Twelve Leverage Points of Agentic Coding" — verbatim list with one-line gloss each.
> 3. For each pattern in Chapter 7 (Plan-Build-Review, Self-Improving Experts, Orchestrator, Autonomous Loops/Ralph Wiggum, ReAct, HITL, Progressive Disclosure, Expert Swarm, Multi-Agent Collaboration, Multi-Agent Landscape, Production Multi-Agent Systems): one paragraph each — what it is, when Jaymin says to use it, where it appears (or doesn't) in our existing architecture set.
> 4. Three explicit *agreements* between Jaymin and `architectures/00-comparison.md`, with citations to specific architecture sections.
> 5. Three explicit *disagreements* — places where Jaymin would change one of our architecture decisions.
> 6. Vocabulary uptake: a short list of terms the book uses that we should adopt verbatim in our own docs (with definitions).
> 7. **A note on which book sections were not directly readable** (e.g. if the repo files differ from the website rendering).

### 3.2 Subagent 09 — Jaymin Book: Harnesses, Practices, Mental Models

**Goal:** This is the highest-doctrine subagent. Chapter 6 ("Harnesses") and Chapter 9 ("Mental Models") contain the explicit "Specs as Source Code," "Context as Code," and "Software Factories" sections that are most likely to either validate or challenge our `architectures/00-comparison.md`.

**Prompt:**

> Read the following files from `jayminwest/agentic-engineering-book` (raw.githubusercontent.com, branch `main`):
> - `chapters/6-harnesses/` — all 7 sub-files
> - `chapters/8-practices/` — all 7 sub-files (Debugging, Evaluation, Cost & Latency, Production, Workflow Coordination, Knowledge Evolution, Operating Agent Swarms)
> - `chapters/9-mental-models/` — all 7 sub-files (especially `3-specs-as-source-code.md`, `4-context-as-code.md`, `7-software-factories.md`)
>
> **Pre-reading orientation:** Our existing methodology baseline is `spec-driven-ai-dev.md` at the repo root, and our four candidate architectures live in `architectures/01-` through `architectures/04-`. The comparison index is `architectures/00-comparison.md`. You may read those to know what you are diffing against. Do NOT read `research/01-` through `07-` — they cover different sources.
>
> **Report structure** (`research/09-jaymin-book-harnesses-practices-mental-models.md`):
> 1. **Harness vocabulary.** Jaymin defines "harness" as a specific concept. State that definition. Compare to the implicit notion of "the loop the agent runs in" that appears across our four architectures. Is "harness" the right umbrella term for `architectures/00-comparison.md` §4.1?
> 2. **Software Factories chapter diff.** Read `chapters/9-mental-models/7-software-factories.md`. Diff its claims directly against `architectures/00-comparison.md`. Note (a) anywhere Jaymin says something our comparison missed, (b) anywhere our comparison goes deeper than Jaymin, (c) anywhere the two disagree.
> 3. **Specs as Source Code.** Read `chapters/9-mental-models/3-specs-as-source-code.md`. Compare to `spec-driven-ai-dev.md`. Note vocabulary differences (e.g. layers, channels, probes).
> 4. **Operating Agent Swarms.** Read `chapters/8-practices/7-operating-agent-swarms.md`. What is Jaymin's operational discipline? How does it compare to the "manager loop / 5-state queue" in our Architecture 2 (Compound Atelier)?
> 5. **Practices we should adopt.** A short list of operational practices (debugging, eval, cost, knowledge evolution) that our four architectures under-specify, with a one-paragraph proposal of how to incorporate each.
> 6. **Failure-mode additions.** Are there failure modes Jaymin names that are not in our existing 20-failure-mode list (see `architectures/00-comparison.md` §2.4)? List them.
> 7. **What is missing.** Anything Jaymin assumes that our context (CI/CD pipeline rather than interactive desktop) would invalidate. Be specific.

### 3.3 Subagent 10 — Overstory substrate audit

**Goal:** Determine, in concrete terms, whether and how Overstory can be (a) used directly as the orchestration substrate for our software factory, (b) used as a reference design we re-implement, or (c) discarded as architecturally incompatible. The CI/CD framing is especially important here because Overstory's headless mode plus its runtime adapters might already be 80% of what we need.

**Prompt:**

> Read the Overstory repository at `github.com/jayminwest/overstory`, branch `main`. Specifically:
> - `README.md`
> - `STEELMAN.md` (Jaymin's deliberate steelman case for the project — read this *first* after README)
> - `CLAUDE.md` (agent operating instructions baked into the repo)
> - `SECURITY.md`
> - `docs/` — every file
> - `agents/` — every agent role definition
> - `src/` — at minimum read the entry point, the coordinator, the mail subsystem, the worktree manager, the merge queue, and the `AgentRuntime` interface and at least three adapter implementations (Claude Code, Aider, one other)
> - `.github/` — workflows, especially anything CI-shaped
> - `package.json`, `bunfig.toml` for the runtime/build story
>
> Skip `ui/` unless you find something interesting in `docs/` that points at it.
>
> **Report structure** (`research/10-overstory-substrate-audit.md`):
> 1. **One-paragraph "what it is."** Independent of the marketing.
> 2. **Architecture map.** A diagram or labelled list of: coordinator, supervisors/leads, workers (Scout/Builder/Reviewer/Merger), the mail bus, the worktree manager, the merge queue, the watchdog, the runtime adapters. Cite line numbers / file paths.
> 3. **The `AgentRuntime` interface.** What does an adapter implement? How thin/thick is the contract? What does it imply about portability?
> 4. **Worktree isolation.** How is it actually done? `git worktree add` per worker? Branch naming? Garbage collection?
> 5. **SQLite mail.** Schema, message types, broadcast semantics, throughput (any benchmarks?), failure modes.
> 6. **4-tier conflict resolution.** What are the 4 tiers? At what cost?
> 7. **Headless / non-interactive operation.** Can Overstory run as a one-shot batch (start coordinator, dispatch issue, wait for merge, exit) suitable for CI? If yes, what is the contract? If no, what's missing?
> 8. **Diff against `architectures/00-comparison.md` §4.1 (the shared infrastructure list).** For each infrastructure primitive, does Overstory already provide it, partially provide it, or not provide it?
> 9. **Risks Jaymin names in `STEELMAN.md` or `SECURITY.md`.** Especially around merge conflicts, agent oversight, cost ceiling, and sandbox escape.
> 10. **Recommendation.** Adopt as-is / fork / re-implement in Python / steal-the-design-only / discard. Defend the choice with three reasons.

### 3.4 Subagent 11 — OpenHands substrate audit (CI/CD lens)

**Goal:** Determine whether OpenHands' SDK + headless mode + GitHub Action can be the agent runtime layer of a software factory, with the four architectures sitting *on top* of it. Pay specific attention to the CI/CD shape and the cost/sandbox model.

**Prompt:**

> Read the OpenHands repositories at:
> - `github.com/All-Hands-AI/OpenHands` (core), branch `main`
> - `github.com/OpenHands/software-agent-sdk` (the V1 SDK)
> - `github.com/OpenHands/OpenHands-CLI` (the binary CLI)
> - `github.com/OpenHands/openhands-github-action` (the marketplace action)
>
> Files of interest in the core repo:
> - `README.md`, `AGENTS.md`, `CONTRIBUTING.md`, `config.template.toml`
> - `openhands/` package — entry points, the Agent Server, the workspace abstractions
> - `containers/`, `docker-compose.yml`, `Makefile`, `pyproject.toml`
> - `.github/workflows/` — every workflow that builds or releases
> - `skills/` — read at least 3 skill definitions to understand the skill model
> - `.openhands/`, `.agents/` — repo-baked agent config
>
> In the SDK repo, read the README plus the public Python API surface. In the CLI repo, read the README plus the entry point. In the action repo, read `action.yml` plus the entry point.
>
> Note: `docs.all-hands.dev` and the SDK paper (arXiv 2511.03690) are blocked from the sandbox. If you cannot find equivalent information in the repos, list those URLs in your report and recommend they be added to the next GitHub Action fetch issue.
>
> **Report structure** (`research/11-openhands-substrate-audit.md`):
> 1. **One-paragraph "what it is."** Independent of marketing.
> 2. **Five deployment surfaces.** SDK, CLI, GUI+REST, cloud, enterprise. For each: license, intended user, CI/CD friendliness.
> 3. **The Agent Server / Workspace model.** Local Workspace vs. Remote (DockerWorkspace / APIRemoteWorkspace). What does the workspace contract look like? Why does it matter for sandboxing?
> 4. **Headless mode.** How is it invoked? What does "always-approve" do? What flags / env vars matter? Any documented restrictions?
> 5. **The GitHub Action.** What does `action.yml` accept as inputs and outputs? What's the runtime cost shape? What event types trigger it idiomatically? Could we layer the Compound Atelier reviewer-panel pattern on top of it?
> 6. **The skill model.** How are skills loaded, scoped, and composed? How does it compare to the EveryInc compound-engineering plugin's skill catalogue (already documented in `research/04-`, which you should NOT re-read — but you may take the existing summary in `architectures/00-comparison.md` §4.2 as the comparison baseline)?
> 7. **Provider strategy.** Which LLM providers are first-class? How are they configured? Could we mix providers across the four architectures' phases (relevant for Architecture 3's V&V independence)?
> 8. **Sandboxing posture.** Filesystem isolation, network egress controls, capability scoping, secrets handling. Cite specific files.
> 9. **Diff against `architectures/00-comparison.md` §4.1 (shared infrastructure).** For each primitive, OpenHands provides / partially provides / does not provide.
> 10. **Recommendation.** Possible postures: (a) embed OpenHands SDK as the agent runtime under all four architectures, (b) use only the GitHub Action and re-implement orchestration on top, (c) borrow specific subsystems (skills, workspace abstractions, sandbox) and ignore the rest, (d) discard. Defend.

### 3.5 Subagent 12 — Adjacent ecosystem

**Goal:** Several pieces named in Jaymin's book and in Overstory's adapter list are *also* potential substrate components. A short capsule review of each lets us avoid re-discovering them later, and identifies whether any of them moves a decision in subagents 10 or 11.

**Prompt:**

> Read the following repositories (all on GitHub, branch `main`):
> - `github.com/jayminwest/agentic-engineering-book/tree/main/appendices/examples/gastown`
> - `github.com/jayminwest/agentic-engineering-book/tree/main/appendices/examples/kotadb`
> - `github.com/jayminwest/agentic-engineering-book/tree/main/appendices/examples/pi-mono`
> - `github.com/jayminwest/agentic-engineering-book/tree/main/appendices/examples/overstory` (this is the *example chapter* about overstory in the book — read it, but rely on subagent 10 for the substrate audit)
> - Also read `chapters/10-practitioner-toolkit/` (all sub-files) for capsule reviews of Claude Code, Google ADK, agent frameworks, multi-agent workspace managers, enterprise codebase context tools
>
> For each adjacent project (gastown, kotadb, pi-mono), produce a one-page capsule answering:
> - What problem does it solve?
> - License + maturity?
> - Architectural pattern (compare to our four architectures)?
> - Would adopting it move a decision in `architectures/00-comparison.md` §7 (recommended path forward)? If yes, how?
>
> **Report structure** (`research/12-adjacent-ecosystem.md`):
> 1. One-paragraph framing.
> 2. Gastown capsule.
> 3. Kotadb capsule.
> 4. Pi-mono capsule.
> 5. Jaymin's book Chapter 10 — capsule of each tool family Jaymin reviews, with a one-line "should we look harder at this?" verdict.
> 6. Two-line summary at the bottom: of all items reviewed, which (if any) deserve a full substrate audit in a future round?

### 3.6 Subagent 13 — Synthesis (sequential; runs last)

**Goal:** Read every report from subagents 08-12, plus the existing `research/00-synthesis.md` and `architectures/00-comparison.md`, and produce a single Round-2 synthesis. This is the document a future reader can read alone to know what changed.

**Prompt:**

> Read every file in `research/08-` through `research/12-`. Then read `research/00-synthesis.md` and `architectures/00-comparison.md`. Do NOT read `research/01-` through `07-` directly; the synthesis is sufficient.
>
> **Report structure** (`research/13-round-2-synthesis.md`):
> 1. **What changed in the consensus.** Section-by-section diff against `research/00-synthesis.md` §2 ("Where the sources agree"). Are there new consensus items? Have old ones been falsified?
> 2. **What changed in the disagreements.** Diff against `research/00-synthesis.md` §3. Especially: did Jaymin/Overstory/OpenHands move the needle on the "humans review or not" question, the persona-vs-graph question, the prose-vs-structured-spec question?
> 3. **What changed in the failure-mode list.** Diff against `architectures/00-comparison.md` §2.4 (F1–F20). Any new failure modes? Any of F1–F20 newly contradicted by direct evidence?
> 4. **Shared-infrastructure coverage matrix.** A table: rows are the §4.1 primitives, columns are Round-1 corpus / Overstory / OpenHands. For each cell: provides / partial / absent. This tells us where the build-vs-buy decision is *available*, not just *possible*.
> 5. **CI/CD pipeline adaptation thesis.** A one-page argument for the most plausible substrate: probably some combination of (a) OpenHands SDK headless as the per-cycle runtime, (b) Overstory's coordinator+worktree+mail design (re-implemented or used directly), (c) one of our four architectures as the methodology overlay. The user's framing — "we want to run as a CI/CD pipeline" — is the constraint that breaks ties.
> 6. **Updated recommended path forward.** Replacement for `architectures/00-comparison.md` §7. Should still recommend a single starting path but may now recommend a substrate stack underneath it.
> 7. **Open questions for Round 3** (if any).

---

## 4. Synergistic structure (why these splits)

The six subagents are not arbitrary. The synergies are:

- **08 + 09 split the book by depth.** 08 reads the more numerous, less philosophical chapters; 09 reads the fewer, denser chapters most likely to challenge our architecture decisions. Both can run in parallel because they share no files.
- **10 + 11 are the two open-source substrate candidates.** They will be diffed against each other in 13; doing them in parallel preserves their independence (neither one biases the other's review).
- **12 catches the adjacent material the previous five risk missing.** Without it, gastown/kotadb/pi-mono get name-checked in 08 and 11 but never examined.
- **13 collapses the result.** It is the only sequential dependency.

The structure also defends against an information-hazard: each subagent should reach independent conclusions before being exposed to the others' findings, because Jaymin/Overstory/OpenHands cross-reference each other heavily and an early synthesis would over-collapse them.

---

## 5. The blocked-URL fetch loop

Because the sandbox blocks the live web book, the OpenHands docs, the SDK paper, the Substack manifesto, the YouTube videos, and several blog posts, we cannot fully execute this plan from inside the sandbox without help. The companion file `research/blocked-urls-round-2.md` enumerates every URL the subagents will likely need that is *not* fetchable from the sandbox.

The mechanism for getting them is a new GitHub Action defined in `.github/workflows/fetch-blocked-urls.yml`. Workflow:

1. The lead agent (or a future resumption agent) **opens an issue** in this repo with a body containing one URL per line (markdown links are tolerated; the action parses raw URLs), and applies the `fetch-urls` label to it.
2. The action triggers when (a) the issue carries the `fetch-urls` label and (b) the event type is `opened`, `edited`, `labeled`, or `reopened`. The label can only be applied by users with Triage role or higher, so the label itself is the security gate. See §6.
3. The action runs `curl` against each URL from a normal GitHub runner (which is not behind the sandbox's host allowlist), saves results into `research/fetched/<issue-number>/<slug>.html` and `.md` where possible, commits to a new branch `fetched/issue-<n>`, and posts a comment on the issue with the branch name and file list.
4. The agent then `git fetch origin fetched/issue-<n>` and merges that into the working branch, then re-runs whichever subagent needs the new content.

This loop is asynchronous: opening the issue does not require the agent to wait. A future resumption agent can simply check whether a `fetched/issue-N` branch exists and merge it.

---

## 6. GitHub Action — security stance

Threats the action must defend against:

- **Random GitHub users opening issues to spam fetches.** Mitigated by the `fetch-urls` **label** gate. Only users with Triage role or higher can apply labels in GitHub, so a drive-by user cannot satisfy the gate even by guessing the magic word. (An earlier version tried `author_association` instead, but the webhook payload and the REST API disagreed on its value for the same user, which caused every run to silent-skip.)
- **A trusted account being compromised and used to fetch malicious URLs.** This is residual risk. The action does not execute fetched content — it only stores it as files. The repository review process catches the misuse before any agent reads the malicious content. Worst case: a junk branch gets created and is deleted.
- **Excessive runner minutes.** The action caps per-issue fetches at 50 URLs, with a per-URL 30-second timeout. If the issue body contains more URLs, the action refuses with a comment.
- **Secret exfiltration.** The action has only `contents: write` and `issues: write` permissions. It does not touch secrets, does not call external APIs other than the URLs in the issue body, and does not have an `if: ${{ secrets.X != '' }}` check that would allow secret-conditioned behavior.
- **Modifying main directly.** Forbidden by the workflow: it only ever pushes to `fetched/issue-<n>` branches. Merging to a working branch is a deliberate, agent-driven step.

The author allowlist is enforced *both* in workflow `if:` (job-level) and in the very first step (re-check inside the runner) for defense in depth.

---

## 7. How to resume this plan

A future agent (or a future Claude session) should be able to pick up this plan with no extra context. Steps:

1. **Read this file (`research/PLAN.md`) end-to-end.** Then read `research/blocked-urls-round-2.md` to know what URLs are still missing.
2. **Check branch state.** Run `git branch -a | grep fetched/issue-` to see whether a previously-opened fetch issue has produced content. If yes, `git merge` those branches into the working branch.
3. **Check which reports already exist.** Run `ls research/0[89]-*.md research/1[0-3]-*.md`. Skip any subagent whose report already exists. (If a report exists but is empty or marked "BLOCKED," re-dispatch.)
4. **Dispatch missing subagents.** For each missing report, use the Agent tool with `subagent_type: general-purpose` (or `Explore` for read-only) and copy the prompt from §3 of this file verbatim. Dispatch the parallelizable ones (08-12) in a single message with multiple Agent tool calls. Run 13 only after all of 08-12 have completed.
5. **If any subagent reports `BLOCKED` due to a 403 URL it cannot reach,** add those URLs to a new fetch issue: title `[fetch-urls] round-2 supplement` and body containing the URLs. Wait for the action to comment with a branch name; merge it; re-dispatch the blocked subagent.
6. **When 13 is complete,** update `architectures/00-comparison.md` §7 ("Recommended path forward") with the new conclusions. The update should preserve the original §7 in a section called "§7 (Round 1)" so the diff is traceable.
7. **Close the plan** by writing a short "Round 2 complete" stanza at the bottom of `research/PLAN.md` with the commit hash where the last subagent landed.

Nothing in this plan requires reading the existing reports `research/01-` through `07-` — those were the Round-1 corpus and have already been synthesized in `research/00-synthesis.md`. Avoiding them keeps the Round-2 reports independently re-readable.

---

## 8. Cost and time envelope (rough)

Per-subagent expectation, assuming a ~200k-context model:

| # | Files to read | Approx tokens | Approx wall time |
|---|---|---|---|
| 08 | ~25 chapter files | ~80k input | 10–20 min |
| 09 | ~21 chapter files | ~70k input | 10–20 min |
| 10 | ~30 repo files | ~50k input | 15–30 min (needs code-walking) |
| 11 | ~40 repo files across 4 repos | ~80k input | 20–40 min |
| 12 | ~15 chapter + capsule files | ~30k input | 10–15 min |
| 13 | 5 reports + 2 existing docs | ~40k input | 15–25 min |

**Total parallel wall time: ~30–40 minutes (limited by 11). Sequential synthesis adds another ~20 minutes.** Token cost depends on the model; expect this to be the most expensive single operation in the project so far, but bounded by the size of the source material (the book and the two main repos).

---

## 9. What this plan deliberately does not do

- It does not run the subagents. It only prepares the dispatch. The user should review the plan before any subagent is launched, because the cost of a rushed plan is much higher than the cost of reviewing it.
- It does not redo Round 1. The existing `research/01-` through `07-` reports stand. The Round-2 subagents are explicitly instructed not to read them.
- It does not pre-commit to any of the four architectures in `architectures/`. The synthesis (subagent 13) may recommend changes, but the existing comparison is preserved as Round-1 history.
- It does not attempt to use OpenHands or Overstory as part of the *research* pipeline itself. That would be a useful future experiment but is out of scope for "find out what they are."

---

## 10. Round-2 progress log (added 2026-05-11)

### 10.1 Fetch action history

| Issue | Purpose | Status | Result |
|---|---|---|---|
| [#4](https://github.com/lago-morph/software-factory/issues/4) | Tier-1 + Tier-2 initial pull (14 URLs) | Closed (acted on) | 13/14 fetched; merged via `fetched/issue-4` branch into `claude/round-2-research-consolidation`. The 1 failure is the Substack manifesto (Substack 403s GitHub Actions IPs). |
| [#8](https://github.com/lago-morph/software-factory/issues/8) | Wayback supplements (Substack + arXiv HTML render + Round-1 backfill candidates) | Closed (acted on 2026-05-11) | `fetched/issue-8` produced 10 URL pairs. Outcomes: Substack manifesto ✅ → report 09 §12; arXiv HTML v2 ✅ → report 11 v0.2; Lenny "head-of-claude-code" PARTIAL (paywall persists) → new section in report 06; Lenny "an-ai-state-of-the-union" PARTIAL (paywall persists; no new info beyond #4 capture); el-kaim ❌ (Wayback never archived); 5 Round-1 backfill duplicates skipped (primary-source content already incorporated). All cache files deleted after incorporation. |
| Manual browser-cookie pass (user-driven, no GitHub issue) | Recovery attempt for the three URLs left unfetched after #8 (every.to "My AI Had Already Fixed", both Lenny interviews) plus three el-kaim / Medium URLs from the Round-3 §11.12 thread | Drained 2026-05-11 via research-pipeline Phase 0 | 6 files dropped into `research/manual/`. Outcomes: every.to "My AI Had Already Fixed" ✅ FULLY UNLOCKED — post-paywall content (five-step playbook, five Cora use cases, three project metrics, $400/$400k claim) incorporated into report 03 §"The Cora playbook"; both Lenny URLs PARTIAL again (cookies present but *not* paid-subscriber cookies — Substack gate persists; no new info beyond what was already in report 06); all three el-kaim / Medium URLs ❌ Cloudflare interactive JS challenge cookies don't bypass — need Path B (Save Page As) from a browser session that has solved the challenge. All 6 cache files deleted after incorporation/triage. |
| Manual "Save Page As" pass + book chapter drop (user-driven, no GitHub issue) | Round 2 of manual content recovery: Path B retrieval for the el-kaim Dark Factory article that round 1's cookies couldn't unlock; reader-view text exports of the two Lenny URLs with user-supplied disposition notes; plus 7 chapter files from William El Kaim's enterprise-architecture book dropped into `research/manual/multi/` for future processing | Drained 2026-05-11 via research-pipeline Phase 0 | 4 files in `research/manual/` (non-multi) plus 7 in `research/manual/multi/`. Outcomes: el-kaim "Dark Factory" article ✅ FULLY UNLOCKED via Path B (Save Page As from a browser that solved the Cloudflare challenge) — 41 KB primary source incorporated into `research/07-dark-factory.md` (full revision, 10 verbatim-quote upgrades, 10 reconstructed claims refuted or sharpened, 14 confirmed); both Lenny URLs 🎬 confirmed **VIDEO-ONLY** by user note ("just a video. Here are references at end.") — the URL has no text interview body, only a podcast landing + paywall stub of an editorial summary; canonical content is in YouTube/Spotify/Apple Podcasts audio (would require transcript-extraction service, not paywall bypass); every.to article re-exported as reader view, content already in report 03 from round 1 (consume-and-delete). The 7 `research/manual/multi/` chapter files are by **the same author as the Dark Factory article** (William El Kaim) and form an enterprise-architecture book that culminates (chapter 7) in the same "dark factory" framing; they are NOT incorporated in this drain — see §12 for the cataloguing of Round 4 work against them. The 4 non-multi cache files deleted after incorporation/triage; the 7 multi/ chapter files kept on `main` for Round-4 dispatch. |

### 10.2 Reports produced

Lead-agent-written, using the freshly-fetched content. These are *not* full subagent dispatches — each notes what is still pending and could be deepened by a future subagent pass.

| Report | Coverage | Status | Notes |
|---|---|---|---|
| 08 — Jaymin Foundations + Patterns | Ch 1, 2, 3, 4, 5, 7 of the book | **Pending.** | All source files live in `raw.githubusercontent.com/jayminwest/agentic-engineering-book/main/chapters/*` and are reachable from the sandbox. No fetch dependency. The original prompt in §3.1 stands. |
| 09 — Jaymin Harnesses + Practices + Mental Models | Ch 6, 8, 9 of the book | **Partial.** `research/09-jaymin-harnesses-partial.md` covers Ch 6's index page in depth. Ch 6 sub-pages 1–7, Ch 8, Ch 9 are pending. | Highest-priority missing piece: Ch 9.7 *Software Factories*. |
| 10 — Overstory substrate audit | The `jayminwest/overstory` repo | **Pending.** | All source files reachable via `raw.githubusercontent.com`. No fetch dependency. The original prompt in §3.3 stands. |
| 11 — OpenHands substrate audit | `All-Hands-AI/OpenHands` plus SDK/CLI/Action companion repos and docs | ✅ `research/11-openhands-substrate-audit.md` v0.2 | Substantive on CI/CD-relevant surfaces. The previously-open follow-up (full SDK paper body) is now incorporated via the issue #8 Wayback HTML render of `arxiv.org/html/2511.03690v2`. |
| 12 — Adjacent ecosystem | Tier-2 perspective pieces + book Ch 10 + appendix examples | **Partial.** `research/12-adjacent-ecosystem.md` covers the six Tier-2 pieces. gastown / kotadb / pi-mono / book Ch 10 still pending. | All remaining sources reachable via raw.githubusercontent.com. |
| 13 — Round-2 synthesis | Reads reports 08-12 + Round-1 synthesis + architectures comparison | **Blocked.** Cannot run until 08 + 10 are written, and ideally until 09 and 12 are completed past their partial state. | The synthesis prompt in §3.6 is unchanged. |

### 10.3 What the partial reports already shift

Even at partial state, the Round-2 work changes things that should be reflected in `architectures/` once 13 is written:

1. **"Harness" is the right umbrella term** for what `architectures/00-comparison.md` §4.1 calls "shared infrastructure." Adopt the term. (See report 09 §3, §10.)
2. **OpenHands SDK + CLI is a serious substrate candidate** for the per-cycle agent runtime, with a documented headless mode + JSONL event stream that satisfies our decision-log requirement. (See report 11 §3, §9, §10.)
3. **No official OpenHands GitHub Action exists.** The Marketplace listing is third-party (10 stars). For CI use, roll our own thin Docker-image wrapper. (Report 11 §7.)
4. **Cisco/LangChain piece supplies the first concrete enterprise case study** with measured numbers (93% time-to-root-cause reduction, 65% dev-cycle reduction, 200 hours saved/month/70 users). Empirical support for Architecture-2's Compound Atelier pattern. (Report 12 §2.2.)
5. **Kiro is a newly-surfaced substrate candidate** — spec-driven, EARS notation, CLI surface, native MCP. Worth a focused audit. (Report 12 §2.5.)
6. **"PR review is the bottleneck"** is now externally validated by the Cisco numbers. Strengthens the case for our architectures that move the human upstream (Architecture-1 spec author, Architecture-4 Geneticist). (Report 12 §2.2.)

### 10.4 Next actions, in order

A future agent (or future Claude session) can pick up from here. Do these in sequence.

#### Step 1 (DONE 2026-05-11) — Drained the in-flight fetch issue #8

Issue [#8](https://github.com/lago-morph/software-factory/issues/8) was processed: Wayback fetches were triaged, content was incorporated into reports 06 / 09 / 11, and cache files were deleted. See §10.1 for the per-URL outcome summary. The original step-1 instructions are retained below for reference / future Wayback-supplement issues.

<details><summary>Original step-1 instructions (preserved for future reference)</summary>

The session that wrote v0.2 of this plan shut down before issue [#8](https://github.com/lago-morph/software-factory/issues/8) finished fetching. **Before doing anything else, check whether it has landed.**

```bash
# (a) Has the workflow created the branch yet?
git fetch origin 2>&1 | grep -i fetched/issue-8

# (b) If yes, what did it get?
#     The workflow comments the per-URL summary on the issue itself.
#     Use mcp__github__issue_read with method=get_comments on issue 8.

# (c) If the branch exists, merge it into the current working branch
#     (or into a new branch off main if the prior working branch is merged).
git merge --no-ff origin/fetched/issue-8 -m "Merge Wayback fetched URLs from issue #8"
```

What issue #8 was asked to fetch (Wayback-Machine routes — see issue body for the canonical list):

- `jayminwest.substack.com/p/a-manifesto-for-agentic-development` — Jaymin's Substack manifesto. If retrieved, this may add doctrinal claims not in the book; update `research/09-jaymin-harnesses-partial.md` if so.
- `arxiv.org/html/2511.03690v2` — OpenHands SDK paper HTML render. If retrieved, this closes the open follow-up in `research/11-openhands-substrate-audit.md` §10 — feed the paper body through and update report 11 in place with deeper architecture / sandbox / cost details.
- `lennysnewsletter.com/p/head-of-claude-code-what-happens` — Cherny interview. If retrieved, this is the strongest scaling data point and feeds back into the Round-1 corpus (potential follow-up to `research/06-hn-and-lenny.md`).
- `lennysnewsletter.com/p/an-ai-state-of-the-union` — Lenny's Simon Willison interview. Same: Round-1 backfill candidate.
- `simonwillison.net/2026/Feb/7/software-factory/` and `simonwillison.net/guides/agentic-engineering-patterns/` — Round-1 backfill candidates. If retrieved, may sharpen `research/05-simon-willison.md` quotations.
- `el-kaim.com/the-dark-factory-...` — Round-1 backfill candidate for `research/07-dark-factory.md`.
- `factory.strongdm.ai/principles` and `/techniques` — Round-1 backfill candidates for `research/01-strongdm-factory.md`.
- `every.to/guides/compound-engineering` — Round-1 backfill candidate for `research/03-every-compound-engineering.md`.

For each successfully-retrieved URL, **decide whether it actually changes a claim** before editing a report — most of the Round-1 reconstructions used multi-source cross-checks and may already be accurate. Only edit if direct evidence contradicts or sharpens existing claims.

If issue #8's workflow **failed** (e.g. all URLs returned 403 from Wayback too), close the issue with a brief comment explaining what was tried and what to do next (probably: try direct Wayback `web.archive.org/web/<timestamp>/<url>` with a recent specific timestamp instead of the redirect-to-latest form). Then proceed to step 2 without those sources.

</details>

#### Step 2 — Dispatch subagent 08

**Subagent 08** (Jaymin Foundations + Patterns). The prompt in §3.1 is unchanged. All source files are accessible via raw.githubusercontent.com; no fetch action needed.

#### Step 3 — Dispatch subagent 10

**Subagent 10** (Overstory substrate audit). The prompt in §3.3 is unchanged. All source files accessible via raw.githubusercontent.com.

#### Step 4 — Dispatch subagent 09-completion

**Subagent 09-completion** (Jaymin Ch 6 sub-pages 1–7 + Ch 8 + Ch 9). Use the prompt in §3.2 but **instruct the agent that `research/09-jaymin-harnesses-partial.md` already exists** — it should read that report's §11 ("What's still pending") for context, then deepen rather than redo. Especially Ch 9.7 (*Software Factories*) is high-leverage.

#### Step 5 — Dispatch subagent 12-completion

**Subagent 12-completion** (gastown / kotadb / pi-mono / book Ch 10). Prompt in §3.5; analogous instruction that `research/12-adjacent-ecosystem.md` exists with the Tier-2 capsules done.

#### Step 6 — Dispatch subagent 13 (synthesis)

Run **only after** 08, 10, 09-completion, 12-completion are all in. Prompt in §3.6 unchanged.

#### Step 7 — Update architectures/

Update `architectures/` based on 13's recommendations. Preserve Round-1 architecture text as `architectures/0N-*.md` with a "Round 1" stanza; add Round-2 deltas as new section or sibling file.

#### Step 8 — Optional: dispatch Round 3 follow-up threads (§11)

§11 catalogs 12 self-contained follow-up research threads surfaced by the v1/v2 passes but not chased then. After Round 2 is closed (or earlier, if a specific thread becomes urgent), these can be dispatched in three parallel waves; see §11 intro for wave grouping. Reports land in `research/followup/NN-shortname.md`, deliberately outside the `research/0N-*.md` numbering so the main directory stays stable. Pick opportunistically — not all are needed.

#### Parallelism notes

Steps 2, 3, 4, 5 can be dispatched **in parallel** in a single multi-Agent message; they share no files. Steps 1 and 6 are sequential bottlenecks. Step 7 is human-curated and likely needs `AskUserQuestion` checkpoints.

**Resume-from-cold checklist:** If you are picking this up after a session shutdown, your very first commands should be:

```bash
# 1. Make sure you have all relevant branches locally
git fetch origin

# 2. See what state main is in and what fetch branches exist
git log --oneline -10 origin/main
git branch -r | grep -E "fetched/|claude/"

# 3. Read this PLAN's §10.4 step 1 above. Drain #8 if needed.
```

### 10.5 Workflow lessons learned (for future agents using the fetch action)

- **Job-level `if:` skips are silent in the Actions UI.** Always gate via logged step instead.
- **`length()` is not a GitHub Actions expression function.** Use bash `${#VAR}` at runtime.
- **`author_association` is computed differently by the REST API and the webhook payload.** Don't use it as a gate. Use a label or username allowlist.
- **`mcp__github__issue_write` with an unknown label name auto-creates the label** (default color #ededed). Apply the `fetch-urls` label at issue-creation time to fire the workflow immediately, no follow-up edit needed.

---

## 11. Round 3 — Follow-up research threads (catalog)

**Status:** Catalog only — none dispatched. Consolidated 2026-05-11 from the former root-level `followup.md` (now deleted; this section is the canonical home).

**Origin:** Outbound threads surfaced by the Round-1 and Round-2 research passes that were *not* chased then. Each thread below is a self-contained subagent brief that can be dispatched in parallel — no inter-thread dependencies.

**How to use:** Pick the threads that matter, spawn a subagent per thread with the brief verbatim, and let them run concurrently. Each brief lists its sources, extraction targets, and output path. Reports land in `research/followup/<NN-shortname>.md` so the main `research/` directory (which Round-2's `0N-*.md` numbering occupies) stays stable.

If a source returns 403 / Cloudflare in the sandbox, use the `fetch-blocked-urls` skill (`.claude/skills/fetch-blocked-urls/SKILL.md`) to file a GitHub issue (label: `fetch-urls`) that triggers the fetcher action — same mechanism described in §5 and §6 above.

### 11.0 Priority tiers and dispatch waves

- **Tier 1 — would change architecture decisions:** threads 1–4
- **Tier 2 — would refine or extend architectures:** threads 5–8
- **Tier 3 — grounding, governance, and remaining blocked sources:** threads 9–12

Total: 12 threads. All independent and parallelizable.

For maximum value per token, dispatch in three waves (each wave a single multi-Agent parallel batch):

- **First wave (highest leverage):** Thread 1 (Shapiro Five Levels — small, fast, anchors the rest), Thread 2 (Attractor implementations — empirical, parallelizes per-repo), Thread 3 (Cherny interview — scaling data), Thread 4 (Gas Town + Beads — orchestration alternatives)
- **Second wave (refinements):** Thread 5 (Klaassen siblings), Thread 6 (Competitor landscape), Thread 7 (Evals deep-dive), Thread 8 (Security primitives)
- **Third wave (grounding):** Thread 9 (Methodology ancestors), Thread 10 (Governance), Thread 11 (Compound Knowledge plugin), Thread 12 (Dark Factory archive recovery)

After each wave, consider re-synthesizing the deltas back into `research/00-synthesis.md` and the affected architecture specs.

### 11.1 Thread 1: Dan Shapiro's "Five Levels" maturity model

**One-line:** The canonical 0→5 maturity model the rest of the corpus cross-references; would let the four architectures be positioned explicitly on the maturity scale.

**Why it matters:** El Kaim, Simon Willison, and StrongDM's own homepage all cite Shapiro's Five Levels as the framing for what level of AI adoption a team has reached. The comparison doc (`architectures/00-comparison.md`) currently describes architectures by trade-offs and contexts but does not place them on the Shapiro scale. Doing so would make hybrid recommendations more crisp (e.g., "Architecture 2 reliably operates at Level 3; pushing to Level 4 requires the additions in Architecture 4").

**Sources:**
- https://www.danshapiro.com/blog/2026/01/the-five-levels-from-spicy-autocomplete-to-the-software-factory/

**Extraction targets:**
- Verbatim definitions of Levels 0–5 (or whatever the actual scale is — confirm count)
- Shapiro's named exemplars per level
- Capabilities and constraints implied at each level
- Where Shapiro positions his own work (Kilroy / DOT-graph orchestration)
- Any maturity-test heuristics ("you are at Level N if …")

**Output:** `research/followup/01-shapiro-five-levels.md` — 600–1200 words. Include a final section "Architecture mapping" placing each of our four architectures on the Shapiro scale with brief justification.

### 11.2 Thread 2: Community Attractor implementations survey

**One-line:** 17+ implementations across 12 languages are claimed; surveying 4–5 distinctive ones tells us which design choices in Attractor reproduce vs. mutate.

**Why it matters:** The `architectures/04-evolutionary-tournament.md` "diversity policy" assumes pattern-level diversity is achievable across model families. Empirical confirmation that distinct independent teams converge on (or diverge from) the same Attractor pattern tells us how robust the pattern is. Amol Kabe's Python variant is particularly important because it introduces *named persona specialists* (Coding / Validator / Debugger / Planner), which is the design move Architecture 2 commits to but Architecture 1 doesn't.

**Sources (read READMEs and any AGENTS.md / docs, NOT source code):**
- https://github.com/danshapiro/kilroy (Go reimplementation by Shapiro)
- https://github.com/smartcomputer-ai/forge (Rust by Luke Buehler)
- https://github.com/joyrexus/software-factory (synthesis repo)
- The Amol Kabe Python "multi-agent Software Factory" repo (search GitHub for it; name is in `research/01-strongdm-factory.md`)
- One of: Fabro (Bryan Helmkamp, Rust), Arc (Point Labs, TypeScript)

**Extraction targets:**
- Which Attractor primitives each implementation kept (graph structure, node types, goal gates, supervisor loops, status.json)
- Which they dropped or replaced
- Which they ADDED that aren't in StrongDM's canonical spec
- Any named persona / role specialization
- Documented assumptions about model floor, provider alignment, sandbox

**Output:** `research/followup/02-attractor-implementations.md` — 1200–2000 words. Include a comparison table: row per implementation, columns for the major design primitives (graph, personas, gates, supervisor, fidelity modes, etc.).

### 11.3 Thread 3: Boris Cherny "What happens after coding is solved"

**One-line:** Currently the strongest single scaling data point in the corpus ("10–30 PRs/day, 10–15 parallel sessions, no hand-edited code since November 2025") — known only via summary. Worth fetching the full interview.

**Why it matters:** Cherny is the head of Claude Code at Anthropic and operates further into the "Dark Factory" levels than anyone in our corpus except StrongDM. His specific claims (parallel-session count, no-hand-edit since a specific date, PR throughput) would calibrate the cost/throughput numbers in our four architectures. The comparison doc currently has a "human role" axis that's coarsely "supervises vs. schedules"; Cherny's lived experience would refine this.

**Sources:**
- https://www.lennysnewsletter.com/p/head-of-claude-code-what-happens — Lenny Rachitsky interview with Boris Cherny, Feb 19 2026. **The page is video-only** — confirmed 2026-05-11 by user-supplied reader-view export with the note *"this was just a video. Here are references at end."* No text interview body exists at the URL. YouTube video: `https://youtu.be/We7BZVKbCVw`. Partial coverage (editorial preface + topic list + references) exists in `research/06-hn-and-lenny.md`. To unlock the body: a **YouTube transcript-extraction service** against the video is the only remaining path; a paid Lenny subscription would not help. **The 10–30 PRs/day and 10–15 parallel-sessions Cherny numbers in report 06 remain un-primary-sourced.**

**Extraction targets:**
- Cherny's exact workflow (how he distributes work across parallel sessions, what each session does, how he reviews)
- The "10–15 parallel sessions" claim verbatim with context (supervisor mode? scheduler mode?)
- The "10–30 PRs/day" claim verbatim — what counts as a PR, what's the merge gate
- The Cowork product build timeline ("10 days, small team, Claude Code")
- Cherny's stated quality/review discipline
- Any cost numbers
- His prediction or normative claims about where it goes next

**Output:** `research/followup/03-cherny-interview.md` — 1000–1500 words. Note paywall status; if only the editorial summary is accessible, say so and synthesize from what's there.

### 11.4 Thread 4: Steve Yegge's Gas Town + Beads (orchestration deep-dive)

**One-line:** El Kaim's article names Gas Town as a sibling to Attractor; the SQLite-to-Dolt migration story in Beads is itself a multi-agent-infra case study.

**Why it matters:** Attractor and Gas Town are independent realizations of the same underlying pattern (graph-orchestrated agent pipelines). The diff between them tells us which design choices are pattern-level vs. team-level. The Beads migration story (the team hit SQLite write-concurrency limits and moved to Dolt — "Git for databases" — to handle multi-agent writes) is concrete evidence that "embarrassingly parallel" multi-agent workflows expose infrastructure assumptions in standard tooling.

**Sources:**
- https://2389.ai/posts/the-dark-factory-is-a-dot-file/ — the 2389 Research deep-dive on DOT-graph orchestration
- https://github.com/gastownhall/gastown — Steve Yegge's Gas Town orchestrator
- https://github.com/gastownhall/beads — Beads task-graph + the SQLite→Dolt migration story
- (Optional) https://www.dolthub.com/ — Dolt, if needed for context

**Extraction targets:**
- Gas Town's DOT-graph node types vs. Attractor's
- Gas Town's "knows when to pause for human input" criterion (Attractor uses `wait.human` hexagons; what does Gas Town use?)
- Beads's task-graph schema and how it differs from a flat `tasks.json` (Symphony) or markdown todo list
- The SQLite-to-Dolt migration: what specifically broke, what the new architecture buys, what the migration cost
- Any explicit comparison to Attractor

**Output:** `research/followup/04-gastown-beads.md` — 1500–2500 words. Include a comparison table for Gas Town vs. Attractor (rows = primitives, columns = each tool).

### 11.5 Thread 5: Klaassen's three sibling Every articles

**One-line:** Compound engineering has more depth than the single "Chain of Thought" article we have access to. Three sibling pieces add the "spec authorship as a meta-skill" angle and the Opus 4.5 model-floor argument.

**Why it matters:** The Atelier (Architecture 2) implementation roadmap (§11) is structured by mechanism adoption. The "Stop Coding and Start Planning" piece reportedly captures the *practice* of teaching the AI how you think — which is the implicit prerequisite for the whole compound-engineering loop. The "Teach Your AI to Think Like a Senior Engineer" piece likely details how the persona library is taught/curated. The Opus 4.5 piece would tell us whether the architecture relies on a specific model capability.

**Sources (all every.to; likely Cloudflare-gated — use the fetch-blocked-urls skill):**
- https://every.to/chain-of-thought/stop-coding-and-start-planning — Klaassen, Nov 6 2025
- https://every.to/chain-of-thought/teach-your-ai-to-think-like-a-senior-engineer — likely same chain-of-thought subdomain
- https://every.to/chain-of-thought/how-every-is-harnessing-the-world-changing-shift-of-opus-4-5 — likely same subdomain

**Extraction targets:**
- "Spend an hour teaching AI how you think" — what does this concretely involve? What artifacts does it produce?
- Senior-engineer thinking — what's the persona / instruction shape that produces it?
- Opus 4.5 specific capabilities Klaassen relies on
- Any new compound-engineering primitives not in the main guide

**Output:** `research/followup/05-klaassen-siblings.md` — 1200–1800 words. If sources are paywalled, capture the visible portion and flag.

### 11.6 Thread 6: Competitor factory landscape survey

**One-line:** Five named competitors (Devin, 8090, Factory/Droid, Superconductor, Jesse Vincent's Superpowers) — knowing what each is shipping helps situate our four architectures in the live market.

**Why it matters:** Our four architectures are designed against the StrongDM/Every.to/Simon/El Kaim sources. A landscape survey would tell us which architecture is *already a product*, which is unique, and which gaps in the field our architectures fill. Particularly: Factory's Droid and Devin claim to be full software factories; their actual marketing and docs would clarify what the field considers "in scope."

**Sources (homepage + docs only; no code):**
- https://devin.ai/ — Cognition's Devin
- https://8090.inc/ (or whatever the canonical 8090 URL is — search)
- https://www.factory.ai/ — Factory's Droid
- https://superconductor.io/ (or canonical URL — search)
- Jesse Vincent's "Superpowers" — find the canonical URL via Vincent's recent posts

**Extraction targets per competitor:**
- One-line product description
- Workflow primitives (do they use specs? scenarios? what's their judge?)
- Human role per their pitch
- Cost / pricing model
- Differentiator they claim
- Any methodology document or public spec

**Output:** `research/followup/06-competitor-landscape.md` — 1500–2500 words. Include a comparison table: row per competitor, columns for spec, scenarios, judge, human role, cost.

### 11.7 Thread 7: Anthropic multi-agent research + Husain/Shankar evals FAQ

**One-line:** Simon endorses both as gold-standard primers; our four architectures' eval discipline (judges, satisfaction scoring, scenario testing) would be sharpened by reading them.

**Why it matters:** Architecture 4 (Tournament) uses fitness components and predator scenarios as the core mechanism. Architecture 1 (Refinery) uses an LLM judge separated from the implementer. Architecture 3 (Foundry) uses independent V&V. All four depend on eval quality. Anthropic's multi-agent research writeup is the canonical example of small-scale-first eval design; the Husain/Shankar FAQ is the practical primer.

**Sources:**
- Anthropic's "How we built our multi-agent research system" (mid-2025; find via anthropic.com/research or Anthropic's engineering blog)
- Hamel Husain and Shreya Shankar, "Frequently Asked Questions (And Answers) About AI Evals" (find via hamel.dev or Shankar's writing)

**Extraction targets:**
- The "start small, evolve" methodology for eval sets
- LLM-as-judge: when it works, when it doesn't
- Error analysis as a percentage of development time (Husain's 60–80% claim)
- "If you're passing 100% of your evals" heuristic — what does it mean and what do you do
- Anthropic's subagent-research-system specific architecture (subagents for context preservation; eval discipline; lessons learned)

**Output:** `research/followup/07-evals-deepdive.md` — 1500–2000 words. Include a final section "Implications for the four architectures" mapping evals practices to each architecture's judge / fitness / V&V structure.

### 11.8 Thread 8: Security primitives (CaMeL + Safe YOLO + Lethal Trifecta)

**One-line:** Our four architectures all mention sandboxing and lethal-trifecta defense in passing; consolidating Willison + Anthropic + DeepMind material gives a coherent security primer.

**Why it matters:** F12 (lethal trifecta / prompt injection) is in every architecture's failure-mode coverage but is treated as "sandbox the implementer." That's necessary but not sufficient. CaMeL's capability-typed-program approach, Willison's Dual LLM pattern, and Anthropic's Safe YOLO container spec together give a layered defense model that any factory operating with real data should adopt. The comparison doc could add a row for "security posture" if this is fleshed out.

**Sources:**
- https://arxiv.org/abs/2503.18813 — Google DeepMind CaMeL paper
- https://simonwillison.net/2025/Apr/11/camel/ — Simon's explainer
- https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ — Simon's framework
- Anthropic Claude Code "Safe YOLO" docs (find via docs.anthropic.com)
- (Optional) https://simonwillison.net/2023/Apr/25/dual-llm-pattern/ — the Dual LLM pattern (April 2023 origin)

**Extraction targets:**
- Verbatim definitions of the lethal trifecta
- CaMeL's typed-capability program model — concrete enough to implement
- Dual LLM pattern's privileged-vs-quarantined LLM separation
- Anthropic's Safe YOLO container constraints (network, file access, secrets)
- Threat models the factory should defend against

**Output:** `research/followup/08-security-primitives.md` — 1500–2500 words. Include a "Security posture per architecture" section adding nuance to F12 coverage.

### 11.9 Thread 9: Methodology ancestors (Kaner / Rumelt / Deming)

**One-line:** Three pre-LLM methodology ancestors that the architectures structurally inherit from; reading them adds historical grounding and surfaces design moves the original authors made that we may want.

**Why it matters:** Cem Kaner's *Scenario Testing* (2003) is the source StrongDM repurposes. Richard Rumelt's *Good Strategy Bad Strategy* is named in compound engineering's `ce-strategy` skill. Deming's PDCA cycle is structurally identical to compound engineering's Plan → Work → Review → Compound loop. These aren't optional reading; they're the design documents the modern methodologies inherit from. Sometimes the ancestor has design moves the descendant dropped.

**Sources:**
- Cem Kaner, "An Introduction to Scenario Testing" (2003 paper, kaner.com or testingeducation.org)
- Richard Rumelt, *Good Strategy Bad Strategy* — the diagnosis / guiding policy / coherent action framework (book; use a summary/review of the framework section if full text is unavailable)
- W. Edwards Deming, PDCA cycle (Plan-Do-Check-Act) — the Wikipedia entry plus one primary Deming source if available

**Extraction targets per source:**
- The original methodology in the author's own words
- Design moves the author made that modern descendants kept
- Design moves the author made that modern descendants dropped (and why)
- Any practical guidance not yet incorporated in our four architectures

**Output:** `research/followup/09-methodology-ancestors.md` — 1500–2000 words. Three sub-sections, one per ancestor.

### 11.10 Thread 10: Governance / liability angle

**One-line:** Our four architectures address methodology and quality but say almost nothing about regulatory exposure, liability allocation, or audit-trail-for-counsel requirements.

**Why it matters:** Architecture 3 (Phase-Gated Foundry) is the most regulation-aware, but even it doesn't engage with current regulatory thinking. The Stanford CodeX piece, the BCG Platinion analysis, and the Pragmatic CTO piece together form a small but coherent governance literature that the comparison doc could synthesize into a "compliance posture" row.

**Sources:**
- https://law.stanford.edu/2026/02/08/built-by-agents-tested-by-agents-trusted-by-whom/ — Stanford CodeX
- BCG Platinion, "The Dark Software Factory" insight piece — find via bcg.com
- https://www.thepragmaticcto.com/p/the-software-factory-when-no-human — Pragmatic CTO

**Extraction targets:**
- Who is liable when an agent-written feature causes a regulatory incident? (Each source likely takes a position.)
- What evidence does counsel/insurance/regulator demand from a factory's audit trail?
- Specific failure modes named in the legal/governance literature (different from our 20 failure modes)
- How current frameworks (SOC 2, ISO 27001, GDPR Art. 22, EU AI Act) apply to agent-produced software
- Recommended controls

**Output:** `research/followup/10-governance.md` — 1500–2500 words. Include a "Compliance posture per architecture" comparison.

### 11.11 Thread 11: Compound Knowledge plugin deep-dive

**One-line:** Tedesco's knowledge-work twin of compound engineering is documented less in our research than the engineering plugin; understanding it sharpens Architecture 2's knowledge layer.

**Why it matters:** The Compound Atelier architecture treats `docs/solutions/` as the canonical knowledge store. Tedesco's plugin operates the same pattern in *knowledge work* (not code), with two-track classification (insight / playbook / correction / pattern) and a separate `stale-knowledge-checker`. The knowledge-work variant exposes design moves that didn't have to make engineering compromises — and may be cleaner.

**Sources:**
- https://github.com/EveryInc/compound-knowledge-plugin — full docs (README, AGENTS.md, plugins/*/README.md, docs/skills/kw-*.md, agents/*.md)
- https://every.to/p/the-agent-that-saved-my-brain — already read in v2 but worth re-extracting with the plugin docs as context

**Extraction targets:**
- The kw-compound + kw-refresh pair (analog to ce-compound + ce-compound-refresh)
- Two-track classification (insight / playbook / correction / pattern) vs. the engineering plugin's bug / knowledge tracks
- `stale-knowledge-checker` — how it identifies staleness
- `strategic-alignment-reviewer` and `data-accuracy-reviewer` — what they catch
- The "no silent overwrites" stance — CK agents return text only; only orchestrating skills write files
- Confidence check primitive (kw:confidence)

**Output:** `research/followup/11-compound-knowledge.md` — 1500–2200 words.

### 11.12 Thread 12: Dark Factory via archive.org ~~(still blocked)~~ — **RESOLVED 2026-05-11**

**One-line:** ~~The El Kaim article remains Cloudflare-gated.~~ **Closed.** The user retrieved the article via Path B (Save Page As → text export) from a real browser that had solved the Cloudflare challenge, and dropped the 41 KB result into `research/manual/`. The primary source was incorporated into `research/07-dark-factory.md` on 2026-05-11 — see the second manual-fetch row in §10.1. Report 07 has transitioned from reconstructed-from-secondary-sources to primary-source-anchored. Three reconstructed claims were refuted, seven were sharpened, fourteen were confirmed verbatim. Outcome: the report's "Sources reviewed" row for the el-kaim URL now reads ✅ FULL. No further work needed on this thread; the author's *book* (separate from the Medium article) is queued as Round 4 — see §12.

The two background-only URLs (the el-kaim author's Medium profile pages) remain ❌ Cloudflare-blocked, but they were always background-context-only and are not blocking any report.

**Why it matters:** Report 07 is the only report in the corpus that remains a reconstruction from secondary sources. The Wayback Machine's snapshot (if it exists) would let us verify quotes and possibly surface material the secondary sources don't quote.

**Sources:**
- https://web.archive.org/web/2026*/el-kaim.com/the-dark-factory-how-software-is-learning-to-build-itself-6496a69ba14e — Wayback Machine search
- https://web.archive.org/web/2026*/welkaim.medium.com/* — Wayback Machine search of the author's profile
- If Wayback fails: try Google Cache (`cache:`), archive.is, or scribe.rip (Medium frontend mirror)

**Extraction targets:**
- The full article text, ideally verbatim
- All direct quotes the v2 report has flagged as "reconstructed"
- Any sections the secondary sources didn't cover
- Footnotes / linked references

**Output:** `research/followup/12-dark-factory-archive.md` — variable length. If recovery succeeds, also update `research/07-dark-factory.md` with verbatim quotes and a revision note. If recovery fails, document what was tried.

### 11.13 Notes for subagents

- Save reports to `research/followup/NN-<shortname>.md` per the brief.
- If a source returns 403 / Cloudflare / paywall: use the fetch-blocked-urls skill (file an issue with the URLs, title `[fetch-urls] …`, label `fetch-urls`). Do NOT fabricate quotes.
- If a brief asks for a comparison table, produce one — the synthesis pass relies on tables for cross-thread integration.
- Flag any new external references the source surfaces (potential Tier 4 threads for a future round).
- Mark unresolved questions; the comparison/synthesis pass will pick them up.
- Aim for the word-count target; don't pad.

---

## 12. Round 4 — El Kaim "Continuous / Intent-Driven Enterprise Architecture" book (catalog)

**Status:** Catalog only — none dispatched. Consolidated 2026-05-11 from user-supplied book chapters dropped into `research/manual/multi/`.

**Source:** Seven chapters of an unpublished/draft book by William El Kaim (same author as report 07's "Dark Factory" article). Local files at `research/manual/multi/Chapter 1 The Limits of Traditional.txt` through `research/manual/multi/Chapter 7 Automating Enterprise Arc.txt`. Each chapter is 44–93 KB; ~430 KB total. All seven were read in full by the cataloguing pass on 2026-05-11.

**Applicability summary.** The book is framed as *enterprise architecture* (the discipline that governs capabilities, policies, ADRs, and the transformation portfolio at organizational scale), not as software-factory methodology. The framing is wider than ours. But the underlying mechanical claim is *identical* to the agent software factory thesis we have been developing: ambiguity becomes an operational hazard when autonomous systems can act at machine pace, and the cure is to make intent, decisions, policies, and validation criteria explicit enough that machines can consume them. Chapter 7 closes the loop by adopting StrongDM's attractor pattern by name and calling the composed result "dark factory" in the same sense report 07 does — confirming that El Kaim's book and El Kaim's Dark Factory article are two presentations of the same thought. Chapters 1–3 develop the upstream discipline (machine-checkable decisions, typed intent, executable policies). Chapter 4 introduces a multi-agent EA Council with explicit L1–L4 delegation classification and an accountability chain. Chapter 6 introduces the "Codex" as a Git-distributed skill library that is the architecture-side analog of compound engineering's `docs/solutions/` and our skill-library thread. Chapter 5 is SAP-specific and outside our scope as a *target* — but it contains one of the cleanest worked examples of the attractor pattern (SAP Activate as a phase DAG with LLM-evaluated edges) and should be mined for that one example only. Chapter 6's sections on "what changes for architects" and the EA-tool vendor landscape are largely about org-chart and procurement and out of scope; the typed-object material at the front of chapter 6 is in scope.

**MANDATORY first action when picked up.** The 7 chapter files are durable on `main` already (verified: they live in `research/manual/multi/` under git). No move/copy needed. The next session can read them directly. After all clusters are written, delete the chapter files in the cleanup pass per `research-pipeline` Phase 6 — unless the orchestrator decides to keep them as primary-source quotes.

### 12.1 Cluster A — Spec-authorship discipline: from "vibes" to typed intent

**Source chapters:** 1 (sections 3–4, 7), 3 (entire), 6 (sections 1–3 — the "vibes to codex" framing and the four-building-blocks-plus-substrate model). Chapter 7's §1 is also load-bearing here as the punchline.

**Applicability rationale.** This is the closest the book gets to *our* core question of "what is a good machine-consumable spec?" Chapter 3's 9-field structured-intent model (identity, statement, business outcomes, capability scope, policy references, invariants, non-goals, decision seeds, guardrails, feedback sources) is a direct, more disciplined cousin of our `specs/` baseline and the compound-engineering "spec" notion in report 03. The chapter is unusually explicit about *non-goals* and *decision seeds* — fields our existing spec templates do not have and probably should. Chapter 6's "vibes vs. specifications" framing is one of the cleanest one-line articulations of the agent-software-factory thesis we have encountered. Chapter 1's distinction between intent / policy / design-decision / specification / constraint / control is sharper than anything in our current synthesis. The cluster also defines three production paths for an intent artifact (manual workshop, LLM-assisted with hard validation gates, EA-tool-resident) — the LLM-assisted path with retrieval-grounded validation is essentially the workflow our factory would run.

**Target report filename:** `research/14-el-kaim-book-intent-and-spec-authorship.md`

**Expected length:** 2000–2500 words.

**Suggested subagent brief.**
> Read `research/manual/multi/Chapter 1 The Limits of Traditional.txt`, `research/manual/multi/Chapter 3 Intent-Driven Architectur.txt` in full, and `research/manual/multi/Chapter 6 The Enterprise Architectu.txt` sections 1–3 and 5 (typed objects). Skim chapter 7 §1 ("the problem is no longer documentation, it is motion") for the punchline. Extract: (a) the verbatim 9-field structured-intent model from chapter 3 §4.1, with the field semantics; (b) chapter 1's vocabulary distinctions (intent / policy / design decision / specification / constraint / control / feedback) — these sharpen our current loose usage; (c) chapter 3's three-path authoring model (manual workshop / LLM-assisted with retrieval-grounded validation / EA-tool-resident) and the OPA-Rego meta-validation gate that prevents the LLM from confabulating policy IDs; (d) the "decision seeds" and "non-goals" fields, which our current spec templates lack; (e) the Healthcare.gov and UK Universal Credit cases as evidence that under-stabilized direction is an architectural failure mode, not a project-management failure. Compare against `architectures/`, `specs/`, and report 03 (compound engineering). Output `research/14-el-kaim-book-intent-and-spec-authorship.md`. Final section should propose concrete additions to our spec template (non-goals field, decision-seed field, invariant-rule field with downstream Rego-binding hint). Do NOT incorporate SAP material here — chapter 5 has its own cluster reference.

### 12.2 Cluster B — Dark-factory operating model: BMAD + attractor + validation harnesses

**Source chapters:** 7 (entire — load-bearing), 5 (sections 2–4 and the scenario-pack examples in §5–6, as *worked example only*).

**Applicability rationale.** This is the chapter that explicitly names dark factory and explicitly adopts StrongDM's attractor as the agent-side execution mechanism. It is essentially a second, more enterprise-flavored presentation of the same material that report 07 reconstructs from the original Medium article — but it is more recent, more structured, and (crucially) presents the BMAD planning flow as the *architect-side* counterpart to the attractor. The BMAD/attractor composition gives us a vocabulary for the planning/execution split that our `architectures/0N-*.md` set has been gesturing at without naming. Chapter 7 §5–6 also articulate the scenario-pack + hidden-holdout + digital-twin pattern more cleanly than any other source in our corpus, including the original StrongDM material in report 02. The "forbidden autonomy boundaries" idea (an agent's output may be technically correct yet still fail the gate because it crossed a non-delegable line) is a primitive our current architectures do not name. Chapter 5's SAP Activate-as-DAG content belongs here purely as evidence that the attractor pattern transfers to a phase-graph governance context — pull it in *only* if the cluster needs a concrete worked example beyond the RX Pharma temperature-excursion one already in chapter 7.

**Target report filename:** `research/15-el-kaim-book-bmad-attractor-dark-factory.md`

**Expected length:** 2500–3500 words.

**Suggested subagent brief.**
> Read `research/manual/multi/Chapter 7 Automating Enterprise Arc.txt` in full. Skim `research/manual/multi/Chapter 5 Automating RISE with SAP.txt` for the attractor-as-phase-graph mapping (sections 2–4); cite that material only if it strengthens a general point. Extract: (a) the BMAD flow (Brief / Map / Act / Double-check) and how each stage feeds the attractor loop — Map produces seeds, Act produces the validation harness, Double-check consumes feedback; (b) the architecture-package YAML artifact in §2.2 as the concrete unit-of-work that binds intent → seed → evidence; (c) the scenario-pack format from §6 with visible scenarios, hidden holdouts, and approval conditions including the "forbidden autonomy boundaries" check that blocks a correct-looking output when the agent crossed a non-delegable line; (d) the digital-twin layer for partner/integration boundaries and its role in keeping scenario evaluation off production interfaces; (e) the convergence-as-satisfaction framing and the move from binary pass/fail to a steady-state metric; (f) the maturity path (minimum viable / mature / full dark factory) in §10. Compare against report 02 (StrongDM attractor), report 07 (Dark Factory), and `architectures/0N-*.md`. Note where this chapter sharpens or contradicts report 07's reconstruction — report 07's author is the same person, so divergences are second-thoughts, not disagreements. Output `research/15-el-kaim-book-bmad-attractor-dark-factory.md`. Include a comparison table: BMAD stage → attractor input/output → existing architecture analog. Do NOT propose architecture changes; flag them in a final "Implications for the four architectures" section instead.

### 12.3 Cluster C — Delegation, the multi-agent EA Council, and accountability under autonomy

**Source chapters:** 4 (entire — load-bearing), 6 §3.4 (Council as Codex object) and §9 (the Council/policy/runtime chain).

**Applicability rationale.** Chapter 4 is the most operationally specific governance text in our entire corpus. The L1/L2/L3/L4 delegation classification with named agent roles, escalation thresholds, and explicit accountability allocation is exactly what §11.10 (the Round-3 governance thread) was looking for and could not find. The chapter also names a failure mode our existing reports have only hinted at — "design authority erosion," where convenience steadily reclassifies L3 decisions as L2 and hollows out the human-judgment layer that delegation was meant to protect. Multi-agent council structure (Chief Architect orchestrator, domain agents, cross-cutting agents with veto / escalation / challenge-only authority, Red Team agent) is a sharper articulation of the multi-agent pattern than anything currently in `architectures/02-*.md` or report 03's review-agent count. The accountability chain framing ("an L2 failure is accountable to the architect who approved the finding, not to the agent") is the single cleanest answer to the regulator/insurer question that §11.10 raised.

**Target report filename:** `research/16-el-kaim-book-council-and-delegation.md`

**Expected length:** 2000–2800 words.

**Suggested subagent brief.**
> Read `research/manual/multi/Chapter 4 Why AI and Automation Cha.txt` in full. Skim `research/manual/multi/Chapter 6 The Enterprise Architectu.txt` §3.4 and §9 for the Council-as-Codex-object material. Extract: (a) the L1/L2/L3/L4 delegation classification verbatim with the agent-role / human-role / evidence-required matrix; (b) the Chief Architect orchestrator spec with its routing rules, deliberation protocol, and special authorities (veto / escalation / challenge-only); (c) the four agent shapes — domain agents, security with veto, GxP compliance with escalation, Red Team with challenge-only — and what each authority type means operationally; (d) the worked example in §5.6 (a pull request that triggers six agents in parallel and produces a structured recommendation in minutes); (e) the accountability chain in §5.7, especially the principle that "agent is not a legal actor" and the failure-mode allocation by delegation level; (f) the four named risks (hallucination, context decay, design-authority erosion, cost/lock-in) and what mitigations are operational versus aspirational. Compare against report 03 (compound engineering's 14-review-agent count) and the §11.10 governance thread — this chapter substantially answers §11.10, and the report should say so. Compare against `architectures/02-compound-atelier.md` (which is closest to a multi-agent council). Output `research/16-el-kaim-book-council-and-delegation.md`. Include a side-by-side: El Kaim Council vs. compound-engineering review army (report 03) vs. our current Atelier architecture. Final section: propose explicit delegation-classification rows for each of the four architectures in `architectures/00-comparison.md`.

### 12.4 Cluster D — The Codex as a Git-distributed skill substrate for machine-consumable architectural knowledge

**Source chapters:** 6 (load-bearing — entire chapter, but especially §§4–9 and §12). Cross-reference to chapter 4 §3 (MCP, architecture-as-code, Claude Skills) for the substrate.

**Applicability rationale.** Chapter 6's "Codex" is essentially the architecture-side twin of our skill-library work (reports 04 and the Round-3 Compound Knowledge plugin thread §11.11). Both pack governed knowledge as Markdown-frontmatter skills in a Git repo, distribute via a marketplace manifest, and load on demand into Claude clients. The chapter goes further than report 04 in two ways: it explicitly enumerates four typed object kinds (principles, standards, reference architectures, blueprints) on top of a business-domain substrate (capabilities, intent, ontology, organizational model), and it specifies *how the validation runs against the typed objects* (JSON Schema for structure, Rego for cross-field constraints, MCP for retrieval grounding). The five-layer Codex model in §12 (semantic / artifacts / operating-model / deliverables / integration) is the most complete picture in our corpus of what a mature factory's knowledge layer looks like. Section 13 (EA-tool vendor landscape, scenarios 1/2/3, Peaqview / ArcKit / Databricks) is largely orthogonal to our software-factory work and should be summarized at one paragraph at most.

**Target report filename:** `research/17-el-kaim-book-codex-and-skill-substrate.md`

**Expected length:** 1800–2400 words.

**Suggested subagent brief.**
> Read `research/manual/multi/Chapter 6 The Enterprise Architectu.txt` in full. Cross-reference chapter 4 §3 (`research/manual/multi/Chapter 4 Why AI and Automation Cha.txt`) for the MCP / architecture-as-code / Claude Skills substrate. Extract: (a) the four TOGAF building blocks (principles, standards, reference architectures, blueprints) as typed objects with schema; (b) the business-domain substrate underneath (business capabilities, enterprise intent, semantic ontology, organizational model) — this is the layer report 04 and the §11.11 compound-knowledge thread did *not* spell out; (c) the Git repository layout with SKILL.md frontmatter, marketplace.json manifest, and per-skill triggers / dependencies — diff this against `.claude/skills/` layout in this repo and report 04's findings; (d) the five-layer Codex model in §12 (semantic / artifacts / operating-model / deliverables / integration); (e) the validation chain: JSON Schema for shape, Rego for cross-field constraints, MCP for retrieval grounding, and the "Codex-as-prompts risk" failure mode in §11. Compress §13 (EA-tool vendor landscape) into one paragraph — it is procurement detail and out of scope. Compare against report 04 (skill libraries), the Round-3 Compound Knowledge plugin thread (§11.11), and this repo's `.claude/skills/` layout. Output `research/17-el-kaim-book-codex-and-skill-substrate.md`. Final section: propose a concrete extension to our skill library to carry typed principle / standard / reference-architecture objects, not only how-to skills.

### 12.5 SAP-specific material (chapter 5) — kept only as worked example, no dedicated cluster

Chapter 5 ("Automating RISE with SAP Through Specification-Driven Enterprise Architecture") is, as the user flagged, mostly outside our scope. It does contain *one* piece of material worth keeping as evidence in cluster B: the SAP Activate phase graph is presented as a directed acyclic graph whose *nodes* are deterministic phase artifacts and whose *edges* are LLM-evaluated transition conditions, with the seed (variability spec + clean-core policy) and the graph (the DAG) treated as separable governance artifacts. This is a clean transferable instance of the attractor pattern operating on a non-software-development substrate — useful as a second worked example alongside the RX Pharma temperature-excursion case already in chapter 7. Cluster B should pull that one mapping in if a second worked example helps; otherwise chapter 5 should not be opened. No dedicated SAP cluster.

### 12.6 Conflicts with and sharpenings of existing reports

- **Report 07 (Dark Factory) — same author, refined.** Chapter 7 is the book version of the article report 07 reconstructs from secondary sources. Where the two diverge, treat the book as the author's later, more deliberate statement. Specifically: report 07 says the dark factory framing comes from Dan Shapiro; chapter 7 confirms (cites Shapiro Jan 2026 in §12 sources) but also names BCG Platinion as a parallel framing. The book version also explicitly says "the architect plans, the agent executes" — a cleaner split than report 07's reconstruction. The cluster-B subagent should flag every divergence and add a revision note to report 07 if any reconstructed claim is contradicted. (Note from the 2026-05-11 orchestrator pass: report 07 is no longer a reconstruction — the Medium article's primary source has been incorporated. Cluster B should now compare the book's chapter 7 against the *primary-source-anchored* report 07, not against the older reconstruction.)
- **Report 03 (compound engineering) — orthogonal but adjacent.** Compound engineering's 14-review-agent army (report 03) is the *engineering* analog of chapter 4's EA Council. The compounding-knowledge mechanism (`docs/solutions/`, the Compound Knowledge plugin) is the *engineering* analog of chapter 6's Codex. The cluster-C and cluster-D subagents should each include an explicit comparison section. No conflicts — they sharpen each other.
- **§11.10 (Round-3 governance thread) — substantially answered by cluster C.** Chapter 4's L1–L4 delegation classification, accountability chain, and "design authority erosion" failure mode constitute roughly two-thirds of what §11.10 was looking for. The cluster-C report should say so explicitly and reduce §11.10's scope to the still-open pieces (regulator-facing evidence requirements, EU AI Act applicability, insurance/liability) that the book treats only glancingly.
- **§11.11 (Compound Knowledge plugin) — overlaps with cluster D.** Chapter 6's Codex and the Compound Knowledge plugin are independent instantiations of the same pattern (Git-distributed typed knowledge consumed by AI assistants). The cluster-D and §11.11 reports should be dispatched in the same wave so the comparison is explicit.
- **Architectures `00-comparison.md` — likely needs a new row.** Each cluster ends with a "propose addition to comparison doc" instruction. Whichever subagent runs the synthesis pass should add a "delegation-classification posture" row (from cluster C) and a "knowledge-substrate carrier" row (from cluster D) to `architectures/00-comparison.md`.

### 12.7 Notes for subagents (carry over §11.13 conventions)

- Reports land in `research/14-…md` through `research/17-…md`, **not** in `research/followup/`. Round 4 continues the main numbering because the chapter files are primary-source material on the same footing as Round-1/Round-2 sources, not follow-up threads.
- Cite chapter and section ("Chapter 4 §5.2") for every load-bearing quote. The chapter files are durable on `main`, so quotes should be traceable to the byte-for-byte file content.
- If a subagent finds material it wants to elevate to a dedicated cluster (e.g. digital-twin governance as its own thread), flag it in the report's "Open questions" section — do not split the cluster mid-dispatch.
- Do not fetch URLs from the chapter resource sections; treat those as referenced sources for future Round-5 threads, not as Round-4 obligations.
- Aim for the word-count target; don't pad. If a cluster's actual content runs short, deliver the short report and flag the over-estimate rather than padding.
- The four clusters are independent and parallelizable; dispatch as one wave of 4 subagents.
- **Naming caveat from the cataloguing pass:** the book consistently uses "ACME Pharma / RX Pharma" as the running example. Reports should reproduce that example's *shape* but rename to a generic example to avoid the pharma framing leaking into our architecture docs.

---

*End of research plan v0.4 — `research/PLAN.md`. v0.1 was structured around six subagents in §3; v0.2 records the lead-agent partial pass and the resumption checklist; v0.3 (2026-05-11) consolidates the former root-level `followup.md` into §11 as 12 Round-3 follow-up threads, and adds Step 8 in §10.4 referencing them; v0.4 (2026-05-11, same day) adds §12 as the Round-4 catalogue (4 clusters spanning the El Kaim enterprise-architecture book in `research/manual/multi/`) and updates §11.12 to "RESOLVED" after the Dark Factory primary source was incorporated into report 07 in the same drain.*
