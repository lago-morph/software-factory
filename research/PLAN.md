# Research Plan — Round 2: Jaymin West Book, Overstory, OpenHands

**Branches:** `claude/research-agentic-engineering-YxbW1` (initial plan, merged in PR #3); `claude/round-2-research-consolidation` (current — see `git log`).
**Date opened:** 2026-05-10
**Status:** **Mid-stream as of 2026-05-11.** Fetch action operational. Tier-1 web content retrieved (issue #4). Three reports written *by the lead agent in place of subagents* (08, 11, 12 — see §10 *Round-2 progress log*). Reports 08 (Foundations + Patterns), 10 (Overstory substrate audit), and the unfetched portions of 09 (Practices + Mental Models) are still pending; report 13 (synthesis) blocks on them. See §10 for next-action checklist.
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
| [#8](https://github.com/lago-morph/software-factory/issues/8) | Wayback supplements (Substack + arXiv HTML render + Round-1 backfill candidates) | In flight | Should produce `fetched/issue-8`. Apply the workflow's standard merge instructions when comment lands. |

### 10.2 Reports produced

Lead-agent-written, using the freshly-fetched content. These are *not* full subagent dispatches — each notes what is still pending and could be deepened by a future subagent pass.

| Report | Coverage | Status | Notes |
|---|---|---|---|
| 08 — Jaymin Foundations + Patterns | Ch 1, 2, 3, 4, 5, 7 of the book | **Pending.** | All source files live in `raw.githubusercontent.com/jayminwest/agentic-engineering-book/main/chapters/*` and are reachable from the sandbox. No fetch dependency. The original prompt in §3.1 stands. |
| 09 — Jaymin Harnesses + Practices + Mental Models | Ch 6, 8, 9 of the book | **Partial.** `research/09-jaymin-harnesses-partial.md` covers Ch 6's index page in depth. Ch 6 sub-pages 1–7, Ch 8, Ch 9 are pending. | Highest-priority missing piece: Ch 9.7 *Software Factories*. |
| 10 — Overstory substrate audit | The `jayminwest/overstory` repo | **Pending.** | All source files reachable via `raw.githubusercontent.com`. No fetch dependency. The original prompt in §3.3 stands. |
| 11 — OpenHands substrate audit | `All-Hands-AI/OpenHands` plus SDK/CLI/Action companion repos and docs | ✅ `research/11-openhands-substrate-audit.md` v0.1 | Substantive on CI/CD-relevant surfaces. One open follow-up: full SDK paper body (PDF didn't text-extract; HTML render queued in #8). |
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

#### Step 1 (MANDATORY FIRST ACTION) — Drain the in-flight fetch issue #8

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

*End of research plan v0.2 — `research/PLAN.md`. Originally v0.1 was structured around six subagents in §3; v0.2 records the lead-agent partial pass and the resumption checklist.*
