# Research Report 18 — OpenAI Codex Substrate Audit

**Date:** 2026-05-11 (drained 2026-05-13 against fetched primaries — see drain note below)
**Author:** Round-5 subagent sub-20 (fanout 20260511-054258)
**Cluster:** Round-5 13.1.1 per `research/PLAN.md` §13.1.1
**Companion reports:** `research/11-openhands-substrate-audit.md` (OpenHands analog), `research/04-every-skill-libraries.md` (Every skill registry analog), `research/09-jaymin-book-harnesses-practices-mental-models.md` (harness terminology), `research/00-synthesis.md` (cross-substrate framing).
**Stance in one sentence:** Codex is *not* a model — it is a five-surface harness around a stable App Server protocol, with AGENTS.md as the spec-ingestion contract, Subagents as the orchestration primitive, and a layered sandbox/approval matrix as the trifecta defense.

---

## Drain note (manual MHTML capture, Clusters E + F) — 2026-05-16

**Status.** Four primary sources were drained from `research/manual/` on 2026-05-16 across two clusters (per the orchestrator's `research/manual/new-index.md` Cluster E and Cluster F blocks):

**Cluster E (landed earlier on 2026-05-16):**

1. **`developers.openai.com/codex/rules`** — the `.rules` Starlark DSL spec. Not previously anchored in this report (the term "rules" appeared only as the name of a `granular`-approval-policy *category* in §4). Drained as new §4.3 ("The `.rules` DSL — Starlark-anchored auditable auto-rejection").
2. **`openai.com/index/running-codex-safely/`** — OpenAI security team blog (2026-05-08) on OpenAI-internal deployment posture. Previously in the "Cloudflare-blocked → Path B only" list (PLAN.md §3.3/§4.3); manual MHTML capture **demonstrates canonical fetch reachability via human-attended browser path** for the `openai.com/index/*` host class. Drained as new §4.4 ("Operational posture at OpenAI — the agent-native telemetry stack"). Directly addresses the still-🟡 "operational productivity numbers" gap flagged in §7.

**Cluster F (this drain):**

3. **`openai.com/index/harness-engineering/`** — Ryan Lopopolo's *"Harness engineering: leveraging Codex in an agent-first world"* (OpenAI, 2026-02-11). Previously anchored via the `celesteanders/harness` open-source mirror because the canonical URL Cloudflare-blocked the action runner. Manual MHTML capture re-verifies the §5 numbers, **refutes the prior author attribution** (Ryan Lopopolo, not Celia Chen — Chen wrote the App Server article a week earlier), **refines the headline 3.5 PRs/engineer/day figure** (canonical says the throughput was the small-team-of-three baseline and *increased* as the team grew to seven, contradicting the mirror-era framing that treated 3.5 as a flat average across the whole period), and adds net-new material — verbatim `docs/` tree layout, "Humans steer. Agents execute." line, six-hour single-agent runs, "20% of the week" pre-golden-principles cleanup overhead, end-to-end-feature autonomy ten-step list. §5 rewritten throughout.
4. **`openai.com/index/unlocking-the-codex-harness/`** — Celia Chen's *"Unlocking the Codex harness: how we built the App Server"* (OpenAI, 2026-02-04). Previously anchored via the `newton20/harness-engineering-kb` open-source mirror. Manual capture re-verifies the §1 five-surface quote verbatim (Chen herself enumerates four interactive surfaces; the SDK as a fifth surface is the report's IA-based extrapolation, not Chen's own framing — and Chen describes Codex SDK as a *"TypeScript library"*, **refining** the report's "Python + TypeScript" surface-table cell which appears to reflect a later sdk-page state). Adds net-new material: the four-component App Server architecture (stdio reader / Codex message processor / thread manager / core threads), the "JSON-RPC lite" footnote (1) explicitly omitting the `"jsonrpc": "2.0"` header and framing as JSONL over stdio, the WebSocket-tunnelled-stdio footnote (2) for Codex Web, the MCP-was-insufficient origin story, the five-language client landscape (Go / Python / TypeScript / Swift / Kotlin), `codex app-server generate-ts` / `generate-json-schema` codegen primitives, and Chen's own pros/cons table for App Server vs. MCP vs. SDK vs. Exec.

Provenance: drained from manual `research/manual/` capture on 2026-05-16 (the `openai.com/index/*` host was previously Cloudflare-blocked for the action runner; manual MHTML capture now anchors all four `openai.com/index/*` URLs in scope). All four new/upgraded sections carry `[2026-05-16 manual drain ✅]` (or `— NEW`) markers throughout.

Cross-references: see followup/08-security-primitives.md §6 (operational-deployment companion to §4 threat-model framing) and followup/10-governance.md §5 (admin-enforced `requirements.toml` as concretization of the "automate policy so humans aren't in every loop" stance); followup/06-competitor-landscape.md gains a "compounding-team output rates" anchor pointing back to §5 (Cluster-F update, 2026-05-16).

---

## Drain note (issue #41) — 2026-05-13

**Status.** This report was originally built from WebSearch + open-source-mirror reconstruction because every `*.openai.com` URL 403s from this sandbox (consistent with `research/blocked-urls.md` v5). A GitHub-Actions-backed fetch run (issue #41) retrieved primary content for 5 of the 8 originally-🟡 rows in §0.

**Fetch outcome (8 originally-🟡 rows in §0):**

**Successfully primary-fetched (5 of 8 rows, all `developers.openai.com/codex/*`) — content drained into this revision:**

1. `https://developers.openai.com/codex` (S8 — Codex overview) — fetched.
2. `https://developers.openai.com/codex/guides/agents-md` (S10 — AGENTS.md) — fetched.
3. `https://developers.openai.com/codex/subagents` (S11 — Subagents) — fetched.
4. `https://developers.openai.com/codex/agent-approvals-security` (S23 — Approvals) — fetched.
5. `https://developers.openai.com/codex/cloud/environments` (Cloud env docs) — fetched.

**Cloudflare-blocked at the action runner (3 of 8 rows, all `openai.com/index/*`) — action route exhausted for this host:**

- `https://openai.com/index/harness-engineering/` (S9)
- `https://openai.com/index/unlocking-the-codex-harness/` (App Server article)
- (and the SWE-bench-verified URL, not separately rowed in §0 but cited in §5)

The fetcher action runs from a GitHub Actions IP block that `openai.com/index/*` serves Cloudflare JS challenges to (small response bodies containing `"Just a moment..."`). Path B (Wayback / cookie-fetch from a human-attended browser) remains the only realistic recovery option for these three URLs. The corresponding fetched stubs were deleted from `research/fetched/issue-41/` before this drain. These rows stay 🟡 with that explanation; per-claim quotations in §1 and §5 continue to rely on the open-source mirrors documented previously.

**Per-claim upgrade status is recorded in §1–§4 with the marker `[2026-05-13 primary fetch ✅]` for upgraded claims and `[2026-05-13 primary fetch REFUTES]` for claims the primary contradicts.** Two REFUTES were found (Linux sandbox primitive; approval-mode names), corrected in place. The five `developers.openai.com/codex/*` rows flip to ✅ in §0; the three `openai.com/index/*` rows stay 🟡.

---

## 0. Sources reviewed

Status legend: ✅ primary URL reachable (or successfully primary-fetched 2026-05-13 via issue #41) · 🟡 primary 403/CF-blocked from sandbox AND action runner, content reconstructed from open-source mirrors and WebSearch extracts cross-checked against ≥2 independent re-hosters.

| ID | URL | Status | Reconstruction route |
|---|---|---|---|
| S8 — Codex overview | `https://developers.openai.com/codex` | ✅ | ✅ Primary fetch 2026-05-13 via issue #41 (prior route: WebSearch + App Server article's surface enumeration). |
| S9 — Harness engineering (Ryan Lopopolo, 2026-02-11) | `https://openai.com/index/harness-engineering/` | ✅ FULL | ✅ Primary MHTML capture drained on 2026-05-16 (`research/manual/Harness engineering_ leveraging Codex in an agent-first world _ OpenAI.txt`). Prior route was `raw.githubusercontent.com/celesteanders/harness/...` open-source mirror; the manual capture verifies the mirror reproduced the numbers accurately but **refutes prior author attribution** (the article is by Ryan Lopopolo, not Celia Chen — Chen wrote the App Server article a week earlier). The `openai.com/index/*` host was previously Cloudflare-blocked at the action runner — manual capture is the first canonical anchor. |
| S10 — AGENTS.md | `https://developers.openai.com/codex/guides/agents-md` | ✅ | ✅ Primary fetch 2026-05-13 via issue #41 (prior route: WebSearch detailed extract; cross-checked vs. open-source `openai/codex/docs/agents_md.md` and `agents.md/` spec site). |
| S11 — Subagents | `https://developers.openai.com/codex/subagents` | ✅ | ✅ Primary fetch 2026-05-13 via issue #41 (prior route: WebSearch extracts). |
| S23 — Agent approvals & security | `https://developers.openai.com/codex/agent-approvals-security` | ✅ | ✅ Primary fetch 2026-05-13 via issue #41 (prior route: WebSearch + sibling `concepts/sandboxing` and `security` snippets). |
| App Server article — Celia Chen, 2026-02-04 | `https://openai.com/index/unlocking-the-codex-harness/` | ✅ FULL | ✅ Primary MHTML capture drained on 2026-05-16 (`research/manual/Unlocking the Codex harness_ how we built the App Server _ OpenAI.txt`). Prior route was `raw.githubusercontent.com/newton20/harness-engineering-kb/...` open-source mirror; the manual capture verifies the mirror reproduced the five-surface enumeration and Thread/Turn/Item definitions accurately, plus adds the four App Server components (stdio reader / Codex message processor / thread manager / core threads) and the JSON-RPC-lite framing footnote. The `openai.com/index/*` host was previously Cloudflare-blocked at the action runner — manual capture is the first canonical anchor. |
| Open-source `codex-rs/app-server/README.md` | `github.com/openai/codex/blob/main/codex-rs/app-server/README.md` | ✅ | JSON-RPC 2.0 transports, Thread/Turn/Item primitives, endpoint surface. |
| Open-source `docs/agents_md.md` | `github.com/openai/codex/blob/main/docs/agents_md.md` | ✅ | Confirms `child_agents_md` config-toml feature flag. |
| Cloud-env docs | `https://developers.openai.com/codex/cloud/environments` | ✅ | ✅ Primary fetch 2026-05-13 via issue #41 (prior route: WebSearch: isolated containers, network off by default, allowlist mechanism). |
| Rules DSL (`.rules`) — Codex Developers | `https://developers.openai.com/codex/rules` | ✅ FULL | ✅ Manual MHTML capture drained on 2026-05-16 (`research/manual/Rules – Codex _ OpenAI Developers.txt`); not previously anchored in this report (the term "rules" appeared only as the name of a `granular`-approval-policy category). Drives §4.3. |
| Running Codex safely at OpenAI — OpenAI security team blog (2026-05-08) | `https://openai.com/index/running-codex-safely/` | ✅ FULL | ✅ Manual MHTML capture drained on 2026-05-16 (`research/manual/Running Codex safely at OpenAI _ OpenAI.txt`). The `openai.com/index/*` host was previously Cloudflare-blocked for the action runner (see "Reachability note" below); manual capture is the first canonical anchor. Drives §4.4. |

**Reachability note:** the five `developers.openai.com/codex/*` URLs are primary-anchored (issue #41 action route). All four `openai.com/index/*` URLs in scope for this report are now primary-anchored from manual MHTML capture: `running-codex-safely` (drained 2026-05-16 Cluster E, §4.4), `harness-engineering` (drained 2026-05-16 Cluster F, §5), `unlocking-the-codex-harness` (drained 2026-05-16 Cluster F, §1 + §3 supporting), plus the newly-indexed `developers.openai.com/codex/rules` (Cluster E, §4.3). **The `openai.com/index/*` host is therefore now FULLY primary-anchored for this report** — the action runner remains Cloudflare-blocked for that host class (`"Just a moment..."` bodies under 6 KB), but the human-attended browser path (Path B) has now successfully captured every `openai.com/index/*` URL this report cites. The corresponding open follow-up in §7 (Cloudflare-blocked `openai.com/index/*`) is **CLOSED**.

---

## 1. The five-surface deployment model

The App Server article (Celia Chen, OpenAI, 2026-02-04 — "Unlocking the Codex harness") states [2026-05-16 manual drain ✅ — verified verbatim against canonical capture]:

> *"OpenAI's coding agent Codex exists across many different surfaces: the web app, the CLI, the IDE extension, and the new Codex macOS app. Under the hood, they're all powered by the same Codex harness — the agent loop and logic that underlies all Codex experiences. The critical link between them? The Codex App Server, a client-friendly, bidirectional JSON-RPC1 API."*

That is four interactive surfaces by Chen's own enumeration; the fifth — the SDK at `developers.openai.com/codex/sdk` — is a programmatic client of the same App Server protocol, distinct because it is the only surface designed to be driven by other programs rather than humans. **[2026-05-16 manual drain — refinement]** Chen's article itself describes Codex SDK as a *"TypeScript library for programmatically controlling local Codex agents from within your own application,"* explicitly noting it *"shipped earlier than the App Server, it currently supports fewer languages and a smaller surface area"* — the surface-table cell below ("Python + TypeScript") reflects a later state of `developers.openai.com/codex/sdk`, not Chen's Feb-2026 snapshot.

**[2026-05-16 manual drain ✅ — NEW]** The App Server's *four-component process architecture*, verbatim from Chen: *"an App Server process has four main components: the stdio reader, the Codex message processor, the thread manager, and core threads. The thread manager spins up one core session for each thread, and the Codex message processor then communicates with each core session directly to submit client requests and receive updates."* The translation-layer responsibility is split between the stdio reader and the Codex message processor, which *"translate client JSON-RPC requests into Codex core operations, listen to Codex core's internal event stream, and then transform those low-level events into a small set of stable, UI-ready JSON-RPC notifications."*

**[2026-05-16 manual drain ✅ — NEW]** The protocol is **JSON-RPC-lite**, not strict JSON-RPC 2.0. Footnote 1 of the canonical article (verbatim): *"We use a 'JSON-RPC lite' variant: it keeps the request/response/notification shape, but omits the `\"jsonrpc\": \"2.0\"` header and is framed as JSONL over stdio rather than strict JSON-RPC 2.0."* And footnote 2: *"'stdio' refers to the app-server's stdin/stdout inside the container. In hosted setups, those streams are often tunneled over a persistent network connection (e.g., WebSocket-like) to the container runtime — so it behaves like stdio even if it isn't a literal local pipe."* This refines the open-source `codex-rs/app-server/README.md`'s "JSON-RPC 2.0" framing — the *shape* matches, the *headers and transport* do not.

**[2026-05-16 manual drain ✅ — NEW]** The MCP-was-insufficient origin story (verbatim): *"We first experimented with exposing Codex as an MCP server, but maintaining MCP semantics in a way that made sense for VS Code proved difficult. Instead, we introduced a JSON-RPC protocol that mirrored the TUI loop, which became the unofficial first version of the App Server."* This is the canonical statement that **MCP is insufficient as a coding-agent platform protocol** — the App Server's birth was specifically a response to that gap. Factory-relevance: any orchestrator that tries to use MCP as the agent-coordination substrate is reproducing a problem OpenAI explicitly walked away from.

**[2026-05-16 manual drain ✅ — NEW]** Multi-language client landscape (verbatim): *"Codex surfaces and partner integrations have implemented App Server clients in languages including Go, Python, TypeScript, Swift, and Kotlin."* Code-generation primitives: `codex app-server generate-ts` produces TypeScript bindings directly from the Rust protocol; `codex app-server generate-json-schema` produces a schema bundle for any other-language codegen. This is the substrate-level mechanism that makes "factory orchestrator in language X" viable across the JVM / Go / Swift / Python ecosystems without re-implementing protocol semantics.

**The primary `developers.openai.com/codex` overview page [2026-05-13 primary fetch ✅]** (`da15743d70_developers.openai.com__codex.md` lines 754-775) is a short marketing landing page that describes Codex as "OpenAI's coding agent for software development" available on "ChatGPT Plus, Pro, Business, Edu, and Enterprise plans," with five capability bullets (write code, understand unfamiliar codebases, review code, debug and fix problems, automate development tasks). It does **not** itself enumerate the five surfaces in body copy — but the page's documentation sidebar (`da15743d70` lines 272-310, 646-682) **organizes the entire docs corpus into exactly the surface groups: "App" (overview/features/settings/review/automations/worktrees/local-environments/in-app browser/Chrome extension/Computer Use/Commands/Windows/Troubleshooting), "IDE Extension" (overview/features/settings/IDE Commands/Slash commands), "CLI" (overview/features/Command Line Options/Slash commands), "Web" (overview/Environments/Internet Access), and a separate "Integrations" group (GitHub/Slack/Linear)** plus "Automation" containing "Codex SDK," "App Server," "MCP Server," and "GitHub Action." So the canonical IA recognizes four interactive surfaces (App, IDE, CLI, Web/Cloud) **plus** the SDK as a fifth "automation" surface (matching the report's count), with Integrations + GitHub Action as cross-cutting glue rather than surfaces in their own right. This is consistent with — and slightly tightens — the original five-surface taxonomy.

| # | Surface | Substrate role | OpenHands analog (`11-openhands-substrate-audit.md` §2) |
|---|---|---|---|
| 1 | **CLI** (`codex` / TUI) | Interactive power-user use; CI via `codex exec`. | OpenHands CLI (`openhands --headless`). |
| 2 | **IDE extension** (VS Code, Xcode, JetBrains) | Pair-programming/review; embeds App Server as JSON-RPC stdio child. | OpenHands GUI server (REST/WebSocket browser). |
| 3 | **App** (macOS desktop; ChatGPT mobile Codex mode) | Ambient plan-approve-merge surface. | None first-party. |
| 4 | **Cloud** ("Codex web") | Background tasks; each runs in an isolated OpenAI-managed container, repo preloaded. The actual-concurrency substrate for parallel Subagents (§3). | OpenHands cloud (`app.all-hands.dev`). |
| 5 | **SDK** (Python + TypeScript) | Programmatic embedding; controls a local App Server child over JSON-RPC. The orchestrator-target surface. | OpenHands four-package SDK (`sdk`/`tools`/`workspace`/`agent_server`). |

**The App Server is not a sixth surface** — it is the protocol substrate underneath all five, described as "both the JSON-RPC protocol between the client and the server *and* a long-lived process that hosts the Codex core threads." Same architectural move as OpenHands V1: extract the agent loop, expose via stable interface, every surface becomes "just another client." App Server ≅ OpenHands `agent_server`.

**[2026-05-16 manual drain ✅ — verbatim Thread/Turn/Item definitions]** Chen defines the three conversation primitives explicitly:

> *"1. **Item:** An item is the atomic unit of input/output in Codex. Items are typed (e.g., user message, agent message, tool execution, approval request, diff) and each has an explicit lifecycle: `item/started` when the item begins, optional `item/*/delta` events as content streams in (for streaming item types), `item/completed` when the item finalizes with its terminal payload."*
>
> *"2. **Turn:** A turn is one unit of agent work initiated by user input. It begins when the client submits an input (for example, 'run tests and summarize failures') and ends when the agent finishes producing outputs for that input. A turn contains a sequence of items that represent the intermediate steps and outputs produced along the way."*
>
> *"3. **Thread:** A thread is the durable container for an ongoing Codex session between a user and an agent. It contains multiple turns. Threads can be created, resumed, forked, and archived. Thread history is persisted so clients can reconnect and render a consistent timeline."*

The protocol is **fully bidirectional**: the server can initiate requests *back to the client* when the agent needs input — *"the server can initiate requests when the agent needs input, like an approval, and then pause the turn until the client responds."* This is the substrate-level mechanism that makes interactive approvals (§4) cleanly representable: an approval is just a server-initiated request that pauses the turn until the client replies allow / deny.

**Factory fit:** SDK is load-bearing for orchestrators across Architectures 1–4. Cloud is load-bearing for parallel execution (Architecture 4 population members; Architecture 2 reviewer panels). CLI/IDE/App are human-in-loop surfaces. Protocol uniformity means a Symphony-style orchestrator written against the SDK can hand off to the IDE for human review without re-serializing state — App Server already exposes Thread/Turn/Item primitives.

---

## 2. AGENTS.md instruction layering — full model

Per S10 + the `agents.md` open spec site [2026-05-13 primary fetch ✅ for S10]:

**Discovery, root-to-leaf** [2026-05-13 primary fetch ✅] (`77457a7169_developers.openai.com__codex__guides__agents-md.md` lines 769-772, **verbatim**): *"Codex builds an instruction chain when it starts (once per run; in the TUI this usually means once per launched session). Discovery follows this precedence order: 1. **Global scope:** In your Codex home directory (defaults to `~/.codex`, unless you set `CODEX_HOME`), Codex reads `AGENTS.override.md` if it exists. Otherwise, Codex reads `AGENTS.md`. Codex uses only the first non-empty file at this level. 2. **Project scope:** Starting at the project root (typically the Git root), Codex walks down to your current working directory. If Codex cannot find a project root, it only checks the current directory. In each directory along the path, it checks for `AGENTS.override.md`, then `AGENTS.md`, then any fallback names in `project_doc_fallback_filenames`. Codex includes at most one file per directory."*

**Precedence** [2026-05-13 primary fetch ✅] (`77457a7169_*.md` line 773, **verbatim**): *"Codex concatenates files from the root down, joining them with blank lines. Files closer to your current directory override earlier guidance because they appear later in the combined prompt."*

**[2026-05-13 primary fetch REFUTES]** the earlier claim that "each file is injected as its own user-role message near the top of conversation history... prefixed with `# AGENTS.md instructions for <directory>` (path relative to repo root)." The primary page says **concatenation joined with blank lines**, with no per-file user-role-message wrapper and no `# AGENTS.md instructions for <dir>` header convention. The header convention was a WebSearch-era reconstruction artifact; the actual mechanism is plain concatenation. Operationally this matters for provenance debugging — there is **no** built-in header marking the boundary between scopes; provenance comes from the file content itself and from session logs (`~/.codex/log/codex-tui.log` or `session-*.jsonl`).

**Override semantics** [2026-05-13 primary fetch ✅] (`77457a7169_*.md` lines 769-772 + 838-842 + 851): at any level where `AGENTS.override.md` exists, Codex reads it and **skips `AGENTS.md` at the same level** (primary illustration line 849: *"AGENTS.md Ignored because an override exists"*). Override replaces, not adds — the per-scope escape hatch.

**Size budget** [2026-05-13 primary fetch ✅] (`77457a7169_*.md` line 777, **verbatim**): *"Codex skips empty files and stops adding files once the combined size reaches the limit defined by `project_doc_max_bytes` (32 KiB by default)."* Configurable; primary example raises it to 65536 (line 872).

**Fallback filenames** [2026-05-13 primary fetch ✅] (`77457a7169_*.md` lines 869-872): the `project_doc_fallback_filenames` knob accepts a list of additional filenames (e.g. `["TEAM_GUIDE.md", ".agents.md"]`) treated as instruction files; **filenames not on this list are ignored for instruction discovery**.

**`CODEX_HOME` env var** [2026-05-13 primary fetch ✅] (`77457a7169_*.md` lines 771, 898-902): the global-scope directory is overridable via `CODEX_HOME`, useful for project-scoped automation users.

**Verification & troubleshooting** [2026-05-13 primary fetch ✅] (`77457a7169_*.md` lines 905-921): primary recommends `codex --ask-for-approval never "Summarize the current instructions."` to confirm load order, and points at `~/.codex/log/codex-tui.log` or `session-*.jsonl` for auditing which instruction files Codex loaded.

**Subagent layering:** with the `child_agents_md` flag (confirmed in `openai/codex/docs/agents_md.md` open source), Codex appends scope-and-precedence guidance so a subagent dispatched into `services/billing/` sees that subdirectory's slice, not just root. **Note:** the primary `developers.openai.com/codex/guides/agents-md` page does **not** mention `child_agents_md`; the flag is documented only in the open-source `docs/agents_md.md`. The subagents primary page (S11) instead specifies in `77457a7169` line 807 (and `d179e7b09d` line 807) that *"Subagents inherit your current sandbox policy"* — separate concern from AGENTS.md inheritance.

**Cloud composition** [2026-05-13 primary fetch ✅] (`bf11b65a14_developers.openai.com__codex__cloud__environments.md` line 776, **verbatim**): *"If your repo includes `AGENTS.md`, the agent uses it to find project-specific lint and test commands."* — confirms AGENTS.md drives cloud-environment task discovery.

**Diff against our `.claude/` equivalents** (we use `.claude/skills/<name>/SKILL.md` plus optional `CLAUDE.md`):

| Concern | Codex AGENTS.md | Our `.claude/` | Diff implication |
|---|---|---|---|
| Per-dir scoping | Native root→leaf concatenation | Implicit; nearest `CLAUDE.md` | AGENTS.md stricter for monorepos. |
| Override | First-class `*.override.md` | None | Adopt an override convention. |
| Size budget | 32 KiB default | None | Cheap discipline to copy. |
| Injection header | `# AGENTS.md instructions for <dir>` | None | Aids provenance debugging. |
| Subagent inheritance | `child_agents_md` flag | CWD-dependent only | Worth adopting for `parallel-subagent-fanout`. |
| Skill registry | None first-class (MCP/plugins) | `.claude/skills/<name>/SKILL.md` with YAML trigger (see `04-every-skill-libraries.md`) | **We are ahead** here. |
| Content domain | Project conventions, build/test, "read first" | Same, via root `CLAUDE.md` | Direct analog; AGENTS.md is now multi-vendor (Cursor, Sourcegraph, etc.). |

**Recommendation:** adopt dual files — keep `.claude/skills/<name>/SKILL.md` for the registry (no AGENTS.md equivalent; more important primitive), add root `AGENTS.md` alongside `CLAUDE.md` for cross-tool conventions, with a 32 KiB self-imposed budget.

---

## 3. Subagents — orchestration primitive

Per S11 [2026-05-13 primary fetch ✅] (`d179e7b09d_developers.openai.com__codex__subagents.md`):

**Core definition** [2026-05-13 primary fetch ✅] (`d179e7b09d_*.md` lines 765-767, **verbatim**): *"Codex can run subagent workflows by spawning specialized agents in parallel and then collecting their results in one response. This can be particularly helpful for complex tasks that are highly parallel, such as codebase exploration or implementing a multi-step feature plan. With subagent workflows, you can also define your own custom agents with different model configurations and instructions depending on the task."*

**Orchestration** [2026-05-13 primary fetch ✅] (`d179e7b09d_*.md` lines 781-785, **verbatim**): *"Codex handles orchestration across agents, including spawning new subagents, routing follow-up instructions, waiting for results, and closing agent threads. When many agents are running, Codex waits until all requested results are available, then returns a consolidated response. Codex only spawns a new agent when you explicitly ask it to do so."*

**Availability** [2026-05-13 primary fetch ✅] (`d179e7b09d_*.md` lines 771-777): subagent workflows are enabled by default in current Codex releases; "currently surfaced in the Codex app and CLI. Visibility in the IDE Extension is coming soon." Token consumption is higher than single-agent runs because each subagent does its own model and tool work.

### 3.1. Built-in agents [2026-05-13 primary fetch ✅ — NEW]

Codex ships with three built-in agents (`d179e7b09d_*.md` lines 819-823, **verbatim**):

- **`default`**: general-purpose fallback agent.
- **`worker`**: execution-focused agent for implementation and fixes.
- **`explorer`**: read-heavy codebase exploration agent.

These map roughly to the construction / V&V split central to Architecture 3. The triad is small enough that the factory should plausibly adopt the same naming convention for its own substrate-agnostic role taxonomy.

### 3.2. Custom-agent TOML schema [2026-05-13 primary fetch ✅ — NEW]

Custom agents are defined as standalone TOML files at `~/.codex/agents/` (personal scope) or `.codex/agents/` (project scope) (`d179e7b09d_*.md` line 827). Required fields: `name`, `description`, `developer_instructions`. Optional inheritable fields: `nickname_candidates`, `model`, `model_reasoning_effort`, `sandbox_mode`, `mcp_servers`, `skills.config` — all inherit from parent session when omitted (line 839). If a custom-agent `name` matches a built-in (e.g. `explorer`), the custom version takes precedence (line 856).

Global settings live under `[agents]` in config.toml:

| Field | Default | Purpose |
|---|---|---|
| `agents.max_threads` | **6** | Concurrent open agent thread cap |
| `agents.max_depth` | **1** | Spawned agent nesting depth (root session = 0) |
| `agents.job_max_runtime_seconds` | 1800 | Per-worker timeout for `spawn_agents_on_csv` jobs |

The `max_depth = 1` default is load-bearing: *"allows a direct child agent to spawn but prevents deeper nesting. Keep the default unless you specifically need recursive delegation. Raising this value can turn broad delegation instructions into repeated fan-out"* (`d179e7b09d_*.md` line 854). **Factory implication:** the default disallows the "grandchild" subagent pattern; Architecture 4's per-genome subagents must be flat, not hierarchical, unless `max_depth` is explicitly raised.

### 3.3. Subagent sandbox inheritance [2026-05-13 primary fetch ✅] — RESOLVES open follow-up

The original report §7 listed *"Non-Cloud subagent workspace inheritance"* as an open follow-up. The primary page resolves it (`d179e7b09d_*.md` lines 805-815, **verbatim**):

> *"Subagents inherit your current sandbox policy. ... Codex also reapplies the parent turn's live runtime overrides when it spawns a child. That includes sandbox and approval choices you set interactively during the session, such as `/approvals` changes or `--yolo`, even if the selected custom agent file sets different defaults. You can also override the sandbox configuration for individual custom agents, such as explicitly marking one to work in read-only mode."*

So: on CLI/IDE/App, subagents share the parent's sandbox policy (including any live `/approvals` or `--yolo` overrides), with per-agent file-level overrides possible (e.g. forcing `sandbox_mode = "read-only"` for an `explorer`-type agent). On Cloud, each subagent runs in its own container (separately confirmed at S23 line 784). **Factory implication for Architecture 2 reviewer panels:** without Cloud, all reviewer subagents share workspace with the implementer — the reviewer-panel isolation discipline must explicitly use Cloud dispatch, or accept that CLI/IDE reviewer panels see the implementer's working tree.

### 3.4. Custom-agent examples — three-agent PR-review pattern [2026-05-13 primary fetch ✅ — NEW]

The primary docs ship a complete three-agent PR-review pattern (`d179e7b09d_*.md` lines 898-963) that is directly adoptable for Architecture 2's reviewer panel:

- `pr_explorer` — `model = "gpt-5.3-codex-spark"`, `sandbox_mode = "read-only"`, maps codebase + gathers evidence
- `reviewer` — `model = "gpt-5.4"`, `model_reasoning_effort = "high"`, `sandbox_mode = "read-only"`, correctness/security/missing-tests
- `docs_researcher` — `model = "gpt-5.4-mini"`, `sandbox_mode = "read-only"`, MCP-backed docs verification

This is the canonical "different-model-for-V&V" pattern made concrete at the substrate level. Architecture 3's "different model family for V&V" requirement maps directly to the `model = "..."` per-file knob.

### 3.5. CSV-fanout primitive [2026-05-13 primary fetch ✅ — NEW]

`spawn_agents_on_csv` (marked **experimental** by primary, line 965) lets Codex *"spawn one worker subagent per row, wait for the full batch to finish, and export the combined results to CSV"* (`d179e7b09d_*.md` lines 965-1007). Inputs: `csv_path`, `instruction` (with `{column}` placeholders), `id_column`, `output_schema`, `output_csv_path`, `max_concurrency`, `max_runtime_seconds`. Each worker must call `report_agent_job_result` exactly once.

**Factory implication:** this is the substrate-level fan-out primitive for the Compound Atelier's per-workshop reviewer panel and the Evolutionary Tournament's per-genome dispatch. It is **experimental** — relying on it for Architecture 4's tournament infrastructure should be flagged as a substrate-stability risk.

### 3.6. Composition with Cloud and AGENTS.md (existing analysis, retained)

**Composition with Cloud.** On CLI/IDE/App surfaces, parallelism is bounded by the single host process (multiple Threads exist via the App Server's `create`/`resume`/`fork` endpoints but share compute/FS). On **Cloud**, each subagent task runs in its **own isolated OpenAI-managed container**, repo preloaded — this is where Subagents become a real scaling mechanism. Cloud + Subagents + AGENTS.md scoping is the triangle that makes "weeks of work in days" plausible.

**Vs. OpenHands** (`11-openhands-substrate-audit.md` §4): OpenHands V1 sub-agent delegation is "blocking-parallel only, sub-agents inherit parent model/workspace." Codex differs on two axes: **non-blocking parallelism** (orchestrator collects results — fan-out, not serial) and **isolated workspaces** in Cloud (each container fresh, not parent-inherited). Codex's model maps to our `parallel-subagent-fanout` skill; OpenHands' maps to plan-and-delegate.

**Composition with AGENTS.md:** `child_agents_md` makes subagents read their target subdirectory's slice plus root plus global — they inherit the *spec gradient*, not the parent's working context.

---

## 4. Approvals, sandbox, network — the lethal-trifecta defense

Simon Willison's "lethal trifecta" (`research/05-simon-willison.md`): **untrusted input + private data + ability to exfiltrate**. Codex's defense is a *two-axis policy* — sandbox mode controls technical boundaries; approval mode controls when Codex stops at them. The two compose. [2026-05-13 primary fetch ✅] (`ed3b262d33_developers.openai.com__agent-approvals-security.md` lines 773-779, **verbatim**): *"Codex security controls come from two layers that work together: **Sandbox mode**: What Codex can do technically (for example, where it can write and whether it can reach the network) when it executes model-generated commands. **Approval policy**: When Codex must ask you before it executes an action (for example, leaving the sandbox, using the network, or running commands outside a trusted set)."*

**Sandbox modes** [2026-05-13 primary fetch ✅] (`ed3b262d33_*.md` lines 769, 782-787, 859):

| Mode | FS | Net | Use |
|---|---|---|---|
| `read-only` | none | none | Review/exploration; toggle via `/permissions`. |
| `workspace-write` (default) | within workspace | **off by default** (verbatim line 785) | Default low-friction local. |
| `danger-full-access` | unrestricted | unrestricted | Pair with `approval_policy = "never"` for unattended disposable-container automation; alias `--yolo` / `--dangerously-bypass-approvals-and-sandbox`. |

The default of "off by default" for network access is verbatim from primary line 769: *"By default, the agent runs with network access turned off."*

**[2026-05-13 primary fetch REFUTES]** the previous claim that Codex enforces "**Landlock** + seccomp on Linux." The primary page is explicit (`ed3b262d33_*.md` lines 953-957, **verbatim**):

> *"Codex enforces the sandbox differently depending on your OS:*
> *• **macOS** uses Seatbelt policies and runs commands using `sandbox-exec` with a profile (`-p`)...*
> *• **Linux** uses `bwrap` plus `seccomp` by default.*
> *• **Windows** uses the Linux sandbox implementation when running in WSL2... When running natively on Windows, Codex uses a Windows sandbox implementation."*

So the Linux primitive is **`bwrap` (Bubblewrap) + `seccomp`**, not Landlock. This matters for any threat-model analysis: bwrap is a setuid user-namespace wrapper (different security envelope and different host-config dependencies than Landlock — line 979 notes the sandbox *"may not work if the host or container configuration blocks the namespace, setuid `bwrap`, or `seccomp` operations that Codex needs"*).

**Approval modes** [2026-05-13 primary fetch ✅ partial; one prior row REFUTED]. Primary (`ed3b262d33_*.md` lines 853-861, 888-899) describes these by flag:

| Flag value | Behaviour |
|---|---|
| `--ask-for-approval never` (or `-a never`) | "Never ask the user for approval"; works with any `--sandbox` mode; Codex makes best effort within constraints (line 856-857). |
| `--ask-for-approval on-request` | Default for `Auto` preset. Codex can read/edit/run in workspace automatically; asks approval to edit outside workspace or to run commands needing network (line 789-791). |
| `--ask-for-approval untrusted` | "Codex runs only known-safe read operations automatically. Commands that can mutate state or trigger external execution paths (for example, destructive Git operations or Git output/config-override flags) require approval" (line 901). |

**[2026-05-13 primary fetch REFUTES]** the previous table row for `on-failure` ("Allow all in sandbox; failures escalated for approval to re-run without sandbox. Trusted-but-flaky."). The primary `agent-approvals-security` page **does not list `on-failure` as a current approval mode** — the documented modes are `never`, `on-request`, and `untrusted` (plus the `granular` approval policy for fine-grained category control, line 861). The `on-failure` row appears to be a WebSearch-era artifact, possibly from an older Codex CLI version (or conflated with the earlier `suggest`/`auto-edit`/`full-auto` naming generation). Treat `on-failure` as **not currently documented**; the `untrusted` row is correctly characterized.

A new mode-of-modes appears in primary: **`approval_policy = { granular = { ... } }`** (line 861, 917-924) which lets you keep specific approval categories interactive while auto-rejecting others. Categories: `sandbox_approval`, `rules` (execpolicy), `mcp_elicitations`, `request_permissions`, `skill_approval`. **Factory implication:** the granular policy is the cleanest fit for Architecture 3's V&V phase, where the desired posture is "auto-reject everything except sandbox-escapes, which still require human sign-off."

**Auto-reviewer** [2026-05-13 primary fetch ✅] (`ed3b262d33_*.md` lines 863-886, **verbatim**): default is `approvals_reviewer = "user"`; setting `approvals_reviewer = "auto_review"` routes eligible approval requests through a reviewer agent. *"The reviewer evaluates only actions that already need approval, such as sandbox escalations, blocked network requests, `request_permissions` prompts, or side-effecting app and MCP tool calls. Actions that stay inside the sandbox continue without an extra review step."* (line 878).

**Auto-reviewer risk lattice [2026-05-13 primary fetch ✅ — NEW]** (line 880, **verbatim**): *"The reviewer policy checks for data exfiltration, credential probing, persistent security weakening, and destructive actions. Low-risk and medium-risk actions can proceed when policy allows them. The policy denies critical-risk actions. High-risk actions require enough user authorization and no matching deny rule. Prompt-build, review-session, and parse failures fail closed. Timeouts are surfaced separately, but the action still does not run."*

This is a **four-tier risk lattice** (low / medium / high / critical) with **fail-closed semantics** on prompt-build / review / parse failures — substantially stronger than the original report's binary characterization. The default reviewer policy is at `github.com/openai/codex/blob/main/codex-rs/core/src/guardian/policy.md` (line 882; open-source — a follow-up fetch target). Enterprises can replace the tenant-specific section via `guardian_policy_config` in managed requirements (line 882). **This resolves report §7's open follow-up on `auto_review` model configurability** — the policy text is configurable; the reviewer-model identity itself is still not surfaced on this page but can be constrained with `allowed_approvals_reviewers` (line 886).

**Web search [2026-05-13 primary fetch ✅ — NEW detail]** (`ed3b262d33_*.md` lines 805-810, **verbatim**): *"Codex defaults to using a web search cache to access results. The cache is an OpenAI-maintained index of web results, so cached mode returns pre-indexed results instead of fetching live pages. This reduces exposure to prompt injection from arbitrary live content, but you should still treat web results as untrusted. If you are using `--yolo` or another full access sandbox setting, web search defaults to live results."* Config: `web_search = "cached"` (default) / `"live"` / `"disabled"`. The cached-by-default web search is itself a trifecta defense — it pinches off the "untrusted input" leg unless the operator explicitly opts in to live browsing.

**Cloud egress** [2026-05-13 primary fetch ✅] (`bf11b65a14_developers.openai.com__cloud__environments.md` lines 769-775, **verbatim** for steps 3-4): *"Codex applies your internet access settings. Setup scripts run with internet access. Agent internet access is off by default, but you can enable limited or unrestricted access if needed."* And `ed3b262d33_*.md` line 784, **verbatim**: *"Codex cloud: Runs in isolated OpenAI-managed containers, preventing access to your host system or unrelated data. Uses a two-phase runtime model: setup runs before the agent phase and can access the network to install specified dependencies, then the agent phase runs offline by default unless you enable internet access for that environment. Secrets configured for cloud environments are available only during setup and are removed before the agent phase starts."*

The **trifecta closure** still holds: setup phase (where `npm install` etc. need network) gets it; agent phase (where untrusted-input lives — issue bodies, PR comments, tool output) defaults to none, and **secrets are wiped from environment between phases** (a stronger guarantee than the original report captured — the agent phase cannot see setup-phase secrets even with full network access enabled).

### 4.1. Cloud-environment substrate details [2026-05-13 primary fetch ✅ — NEW]

From `bf11b65a14_*.md` (cloud environments primary):

- **Default container image** (lines 781-789): `universal` image, pre-installed with common languages/packages/tools. Reference Dockerfile at `github.com/openai/codex-universal` is pullable and testable locally — this is a **substrate-level reproducibility lever**: factory CI can pull the same image to reproduce cloud-agent runs locally.
- **Container caching** (lines 822-840): Codex caches container state **for up to 12 hours**; cache invalidates automatically on changes to setup script, maintenance script, env vars, or secrets. **Business/Enterprise: caches are shared across all users who have access to the environment.** This is a parallelism-friendly substrate primitive: a fleet of Architecture 4 tournament runs hits a warm cache after the first.
- **Network proxy** (line 846): *"Environments run behind an HTTP/HTTPS network proxy for security and abuse prevention purposes. All outbound internet traffic passes through this proxy."* — implies all cloud egress is observable / loggable at the proxy.
- **Maintenance script** (line 774, 833-835): an optional script that runs when a cached container is resumed — *"useful when the setup script ran on an older commit and dependencies need to be updated."*

### 4.2. Workspace protected paths [2026-05-13 primary fetch ✅ — NEW]

From `ed3b262d33_*.md` lines 828-851: in default `workspace-write`, the workspace is writable but four classes of paths are kept read-only:

- `<writable_root>/.git` (whether directory or pointer file; if pointer, the resolved git dir too)
- `<writable_root>/.agents` (if a directory)
- `<writable_root>/.codex` (if a directory)
- Protection is **recursive** under those paths.

Additionally, **named filesystem permission profiles** can deny **reads** for exact paths or glob patterns (line 847-851 example: `"**/*.env" = "none"`) — important for local secrets that would otherwise be readable.

**Factory implication:** the `.git`-read-only default protects the implementer-agent's repo from mid-session mutation by the agent itself, and the `.codex`/`.agents` read-only defaults protect the configuration substrate from feedback loops where an agent rewrites its own AGENTS.md or subagent definitions mid-task. The factory should adopt the same convention: any "config-of-the-agent" surface lives at a read-only well-known path.

### 4.3. The `.rules` DSL — Starlark-anchored auditable auto-rejection [2026-05-16 manual drain ✅ — NEW]

The granular approval policy in §4 ("auto-reject everything except sandbox-escapes") needs a *declarative substrate* — otherwise V&V auto-rejection is just hand-written conditionals scattered through the codebase. Codex's answer is a separate file format: experimental `.rules` files written in **Starlark** (`developers.openai.com/codex/rules` — "Rules are experimental and may change"). This is the load-bearing primitive that makes V&V auto-rejection *auditable*. Provenance: manual MHTML capture drained on 2026-05-16; the URL was not previously anchored in this report (the term "rules" appeared only as the name of an approval-policy *category* — see §4 `granular = { rules = ... }`).

**File location and discovery** (primary, **verbatim**): *"Create a .rules file under a rules/ folder next to an active config layer (for example, `~/.codex/rules/default.rules`).  ... Codex scans `rules/` under every active config layer at startup, including Team Config locations and the user layer at `~/.codex/rules/`. Project-local rules under `<repo>/.codex/rules/` load only when the project `.codex/` layer is trusted."*

When the user adds a command to the TUI allow-list, Codex writes back to `~/.codex/rules/default.rules` — the rule file is therefore both an admin-authored static input *and* a session-mutated artifact (a substrate-level provenance gotcha: the same file is dual-sourced).

**`prefix_rule(...)` shape** (verbatim from the primary example):

```starlark
prefix_rule(
    pattern = ["gh", "pr", "view"],
    decision = "prompt",
    justification = "Viewing PRs is allowed with approval",
    match = [
        "gh pr view 7888",
        "gh pr view --repo openai/codex",
        "gh pr view 7888 --json title,body,comments",
    ],
    not_match = [
        # Does not match because the `pattern` must be an exact prefix.
        "gh pr --repo openai/codex view 7888",
    ],
)
```

Fields (verbatim from primary "Understand rule fields"):

- **`pattern`** (required, non-empty list): each element is either a literal string (e.g. `"pr"`) **or** a union of literals (e.g. `["view", "list"]`) to match alternatives at that argument position. Codex compares the command's argument list to `pattern` "like what `execvp(3)` receives" — i.e. tokenised argv, not the shell-string.
- **`decision`** (defaults to `"allow"`, three values): `allow` (run outside sandbox without prompting), `prompt` (prompt per matching invocation), `forbidden` (block without prompting). **"Most restrictive wins"** when multiple rules match: `forbidden > prompt > allow`.
- **`justification`** (optional): human-readable rationale surfaced in approval prompts / rejection messages. Primary recommends including a *recommended alternative* in `forbidden` justifications.
- **`match` / `not_match`** (defaults `[]`): inline unit tests validated when Codex *loads* the rules file — the rule file ships with its own conformance tests, catching errors before a rule takes effect rather than at policy-decision time.

**Tree-sitter-based safe-splitting of `bash -lc`** (primary "Shell wrappers and compound commands"). Wrappers like `["bash", "-lc", "git add . && rm -rf /"]` could otherwise smuggle dangerous commands past prefix matching. Codex treats `bash -lc`, `bash -c`, and `zsh` / `sh` equivalents specially:

- **Safe-split path** — if the script is a *linear chain of commands* made only of plain words (no variable expansion, no `VAR=...`, no `$FOO`, no `*`) joined by safe operators (`&&`, `||`, `;`, `|`), Codex **parses it with tree-sitter** and splits it into individual commands, evaluating each against the rules. Most-restrictive-wins still applies. The primary's example: `git add . && rm -rf /` becomes two argv lists `["git", "add", "."]` and `["rm", "-rf", "/"]`, and even with an `allow` for `["git", "add"]`, the whole invocation is blocked because the `rm -rf /` portion is evaluated separately.
- **Conservative whole-string path** — if the script uses redirection (`>`, `>>`, `<`), substitution (`$(...)`, backticks), env-var assignments (`FOO=bar`), wildcards (`*`, `?`), or control flow (`if`, `for`, `&&` with assignments), Codex does not try to interpret it; the entire invocation is treated as a single `["bash", "-lc", "<full script>"]` argv and rules apply against that one string.

The split is a security primitive, not a convenience: "you get the security of per-command evaluation when it's safe to do so, and conservative behavior when it isn't." This is the inverse of the failure mode that bites most prefix-allow-list implementations (which split on `&&` themselves and get fooled by quoting).

**Smart approvals integration** (verbatim): *"When Smart approvals are enabled (the default), Codex may propose a `prefix_rule` for you during escalation requests. Review the suggested prefix carefully before accepting it."* The substrate generates candidate rules during escalation — but a human still reviews them. (For factory adoption this raises a "rule-proposal-poisoning" risk dual to scenario-corpus poisoning in followup/10 §6: an attacker who can shape an escalation prompt can shape the *suggested* `prefix_rule`.)

**Test harness** (verbatim): *"Use `codex execpolicy check` to test how your rules apply to a command."* Example: `codex execpolicy check --pretty --rules ~/.codex/rules/default.rules -- gh pr view 7888 --json title,body,comments`. The command "emits JSON showing the strictest decision and any matching rules, including any justification values from matched rules. Use more than one `--rules` flag to combine files." This makes rules files first-class CI artifacts — the factory can run policy unit tests in PR checks before merging rule changes.

**Admin enforcement** (verbatim): *"Admins can also enforce restrictive `prefix_rule` entries from `requirements.toml`."* `requirements.toml` is the admin-side configuration channel (cf. §4.4 below) that users cannot override — the precedence stack is admin-rules > user-rules > session-mutations, mirroring the same precedence as managed sandbox / network policy.

**Language**: Starlark (the rules engine "can run it without side effects, e.g. touching the filesystem"). The sandboxed-DSL choice is exactly the same architectural move as CaMeL (followup/08 §3): use a side-effect-free interpreter as the policy substrate so the policy itself can't exfiltrate during evaluation.

**Factory implication.** Architecture 3's V&V phase ("auto-reject everything except sandbox-escapes") needs `.rules` as the *declarative substrate* — otherwise the rejection logic is hand-coded in Python and is itself a defect risk. The combination of (a) inline `match`/`not_match` tests, (b) `codex execpolicy check` CI harness, (c) admin-`requirements.toml`-enforced precedence makes the V&V auto-rejection layer auditable in a way no other substrate currently surfaces. Adopt: rule files with inline unit tests, CI policy-check step, admin-enforced precedence stack, side-effect-free DSL.

### 4.4. Operational posture at OpenAI — the agent-native telemetry stack [2026-05-16 manual drain ✅ — NEW]

OpenAI's security team published *"Running Codex safely at OpenAI"* (2026-05-08, `openai.com/index/running-codex-safely/`) describing their internal deployment posture. This URL was previously in the "Cloudflare-blocked → Path B only" list (PLAN.md §3.3 / §4.3); the manual MHTML capture drained on 2026-05-16 is the first canonical anchor for this content. **It directly complements the §5 harness-engineering throughput numbers** by providing concrete operational-posture and telemetry primitives — the agent-native telemetry stack is the substrate that explains *why OpenAI dares run Codex at the throughput Lopopolo reports*.

**Two-axis discipline, reaffirmed** (verbatim, slightly distinct framing from §4): *"Approvals and sandboxing work together. The sandbox defines the technical execution boundary, including where Codex can write, whether it can reach the network, and which paths remain protected. Approval policy determines when Codex must ask to perform an action, such as when it needs to do something outside of the sandbox. Users can approve the action once, or approve that type of action for that session."* — confirms the sandbox-defines-boundary / approval-defines-when-to-ask split as the architectural backbone of OpenAI's *own* deployment, not just public docs framing.

**`Auto-review` mode — the routine-approval delegation primitive** (verbatim): *"For requests that cross the sandbox boundary, we are using `Auto-review` mode, which is a feature that, when turned on, auto-approves certain kinds of requests to reduce how often users have to stop and approve Codex actions. Codex sends the planned action and recent context to the auto-approval subagent, which can automatically approve low-risk actions — or high-risk actions with sufficient level of user authorization — instead of interrupting the user. That keeps Codex moving on routine work while still stopping on higher-risk or actions with unintended consequences."* This is the operational extension of the §4 `approvals_reviewer = "auto_review"` knob — and the canonical statement that **OpenAI internally delegates routine approvals to a subagent**, not to humans-in-loop.

Sample baseline (verbatim TOML from primary):

```toml
# config.toml
approvals_reviewer = "auto_review"
sandbox_workspace_write.writable_roots = ["~/development"]

# requirements.toml
allowed_sandbox_modes = ["read-only", "workspace-write"]
```

The `requirements.toml` line is the admin-enforcement primitive — the sandbox modes available to the user are *constrained at the admin layer*; users cannot opt into `danger-full-access` even by editing their own config.

**Managed network policy** (verbatim TOML from primary):

```toml
# requirements.toml
allowed_web_search_modes = ["cached"]

[experimental_network]
enabled = true
allow_local_binding = true
denied_domains = ["pastebin.com"]
allowed_domains = ["login.microsoftonline.com", "*.openai.com"]
```

Five keys, all primary-anchored:

- **`allowed_web_search_modes = ["cached"]`** — pins web search to the OpenAI-maintained cache, blocking the live-browse opt-out documented in §4 (the user cannot override into `"live"` mode under this admin policy). Closes the "untrusted input" leg of the trifecta at admin scope.
- **`[experimental_network] enabled = true`** — turns on the managed network proxy.
- **`allow_local_binding = true`** — agents can serve on localhost (necessary for dev-server workflows).
- **`denied_domains`** — hard block list (the primary example uses `pastebin.com`, a canonical exfiltration target).
- **`allowed_domains`** — auto-allow list (the primary example uses `login.microsoftonline.com` + `*.openai.com`). Anything not in `allowed_domains` and not in `denied_domains` requires approval per the running policy.

This is the **most concrete public articulation** of an enterprise-grade managed network policy for a coding agent. The factory should adopt the same five-key shape verbatim.

**Identity and credentials** (verbatim TOML from primary):

```toml
cli_auth_credentials_store = "keyring"
mcp_oauth_credentials_store = "keyring"
forced_login_method = "chatgpt"
forced_chatgpt_workspace_id = "<workspace-uuid>"
```

OS-keyring credential storage (rather than file-on-disk); login forced through ChatGPT; pinned to a single ChatGPT enterprise workspace. The workspace-pin is what makes Codex activity appear in the **ChatGPT Compliance Logs Platform** — pinning is the workspace-level identity gate that connects per-agent activity to org-level audit.

**Managed-config precedence** (verbatim): *"We apply this posture through a combination of cloud-managed requirements, macOS managed preferences, and local requirements files. **Requirements are admin-enforced controls that users cannot override.** The macOS managed preferences and local requirements files allow us to keep a consistent baseline while still testing different configurations by team, user group, or environment. These configurations apply across local Codex surfaces, including the desktop app, CLI, and IDE extension."* Three-layer admin stack: cloud-managed requirements (org-wide baseline) → macOS managed preferences (per-fleet test variants via MDM) → local requirements files (per-machine experimental tweaks). Users cannot override any of them.

**Rules at OpenAI scale** — the primary's example `default.rules` snippet uses the union-of-literals form documented in §4.3 (verbatim):

```starlark
prefix_rule(
    pattern = ["gh", "pr", ["view", "list"]],
    decision = "allow",
    justification = "Allows read-only GitHub PR inspection via gh CLI.",
)
prefix_rule(
    pattern = ["kubectl", ["get", "describe", "logs"]],
    decision = "allow",
    justification = "Allows Kubernetes resource inspection for debugging.",
)
```

— so the §4.3 DSL is not theoretical; OpenAI is using it operationally to allow-list `gh pr {view,list}` and `kubectl {get,describe,logs}` without prompting.

**Agent-native telemetry — the OpenTelemetry export primitive** (verbatim): *"Traditional security logs are still useful when looking at actions taken by Codex, but they mostly answer **what** happened: a process started, a file changed, a network connection was attempted. Defenders are still left to figure out **why** Codex did something, or the user's intent. Codex can give security teams a more agent-aware view. **Codex supports OpenTelemetry log export for various Codex events such as user prompts, tool approval decisions, tool execution results, MCP server usage, and network proxy allow or deny events.**"*

Five event categories, primary-anchored:

1. **User prompts** — the original intent input (the "why")
2. **Tool approval decisions** — every approval / rejection by user or `auto_review` subagent
3. **Tool execution results** — what the tool actually did / returned
4. **MCP server usage** — per-MCP-call accounting
5. **Network-proxy allow/deny events** — egress decisions

Sample exporter config (verbatim from primary):

```toml
[otel]
log_user_prompt = true
environment = "prod"

[otel.exporter.otlp-http]
endpoint = "http://localhost:14318/v1/logs"
protocol = "binary"
```

OTLP-HTTP transport on localhost, binary protocol. Localhost-binding means the OTEL collector is itself a sandboxed sidecar — agent telemetry never traverses the network without the collector mediating.

**AI-powered security triage agent** (verbatim): *"At OpenAI, we use Codex logs alongside our AI-powered security triage agent. When an endpoint alert says Codex did something unusual, the endpoint security tool tells us that a suspicious event occurred. Codex logs then help explain the surrounding intent by the user and agent. Our AI security triage agent uses Codex logs to inspect the original request, tool activity, approval decisions, tool results, and any relevant network policy decision or block. The AI security triage agent surfaces its analysis to our security team for review to distinguish between expected agent behavior, benign mistakes, and activity that truly warrants escalation."*

So OpenAI's internal security review is itself a *two-stage agent pipeline*: endpoint-security tool says "something happened" (the "what"); a triage agent reconstructs intent from Codex's OTEL logs (the "why"); a human reviews the triage agent's classification. This is the operational refutation of Kahana's *"tracing difficult by design"* objection in followup/10 §6: tracing is not difficult by design *if* the agent emits structured intent-aware telemetry by default. The factory should adopt the same posture — every agent emits OTEL events for prompts, approvals, tool-results, MCP, network — and a triage-agent layer reconstructs intent before human review.

**Operational reuse** (verbatim): *"We also use the same telemetry operationally. We use these logs to understand how internal adoption is changing, which tools and MCP servers are being used, how often the network sandbox is blocking or prompting, and where the rollout still needs tuning."* Same logs power security review *and* productivity analytics — the "agent-native telemetry" is the singular substrate that supports both. (The Lopopolo throughput numbers in §5 are what an OTEL-anchored productivity dashboard would surface, and the OTEL primitive is now the canonical way to get them.)

**Factory implication.** Operational-posture adoption for the factory is concrete: (i) admin-enforced `requirements.toml` with the five-key managed network policy verbatim, (ii) OS-keyring credential storage, (iii) workspace pinning at the identity layer, (iv) OpenTelemetry export of the five event categories with a localhost-bound OTLP-HTTP collector, (v) an AI triage agent that reconstructs intent from OTEL events before security review escalates to humans. Architecturally these compose with §4.1–§4.3 — sandbox + approval + rules define the *boundary*; managed-config requirements define the *admin-enforced minimum*; OTEL + triage agent define the *observability and review surface*. The combined stack is the agent-native answer to "control + visibility + audit" — which is precisely what followup/08 §6 and followup/10 §1.3 demand from any factory operating outside the dark-factory unattended-mode.

**Factory implications:**

| Trifecta leg | Codex control | Factory adoption |
|---|---|---|
| Untrusted input | Cached web-search vs. live (S23 recommendation). | Architecture 1 already enforces single-input-source via spec. |
| Private data | `workspace-write` default; workspace boundaries. | Mirror; every Implementer in `workspace-write` with workspace = single git worktree. |
| Exfiltration | Net off in Cloud; `auto_review` for sandbox escalations. | Strongest lift. Mandate net-off + allowlist for cloud-dispatched subagents; `auto_review` for any network-egress request. |

The two-axis split is more compositional than OpenHands V1's collapsed `ConfirmationPolicy` (per `11-openhands-substrate-audit.md` §8). Factory should copy the split.

---

## 5. Harness-engineering productivity numbers (verbatim) [2026-05-16 manual drain ✅ — primary-anchored]

From **"Harness engineering: leveraging Codex in an agent-first world"** (S9; **Ryan Lopopolo**, OpenAI Member of Technical Staff, **2026-02-11**; primary MHTML capture drained 2026-05-16). Author attribution refutes the prior mirror-era citation of "Celia Chen et al." — Lopopolo is the sole bylined author; Chen wrote the App Server article (§1) a week earlier and is unrelated to this piece. Acknowledgements credit *"Victor Zhu and Zach Brock who contributed to the post, as well as to the entire team that built this new product."*

**Headline experiment (verbatim):** *"Over the past five months, our team has been running an experiment: building and shipping an internal beta of a software product with 0 lines of manually-written code."*

**Scale (verbatim):** *"Five months later, the repository contains on the order of a million lines of code across application logic, infrastructure, tooling, documentation, and internal developer utilities."* The first commit landed *"in late August 2025."*

**Per-engineer throughput (verbatim — refined attribution):** *"Over that period, roughly 1,500 pull requests have been opened and merged with a small team of just three engineers driving Codex. This translates to an average throughput of **3.5 PRs per engineer per day**, and surprisingly the throughput has increased as the team has grown to now seven engineers."*

**[2026-05-16 manual drain — refinement of mirror-era claim]** The mirror-era quote attributed *"3.5 PRs per engineer per day"* to the whole 3-to-7 team across the whole five-month period. The canonical text is more specific: the 3.5 figure is the **three-engineer-baseline average**, and the throughput-per-engineer *increased* as the team grew to seven. The mirror's "team grew from three to seven during development" framing is a paraphrase of the canonical's "has grown to now seven engineers" — both are accurate, but the canonical implies the three-engineer figure is the **lower bound** for what the harness can support, not an average across all sizes. **Factory implication:** Lopopolo's text is the strongest published claim that per-engineer agent-driven throughput **scales superlinearly** with team size at this stage of the technology — a refutation of the standard Brooks's Law assumption that adding engineers reduces per-engineer throughput.

**Generation provenance (verbatim):** *"every line of code — application logic, tests, CI configuration, documentation, observability, and internal tooling — has been written by Codex. We estimate that we built this in about 1/10th the time it would have taken to write the code by hand."* The "1/10th the time" is a team self-estimate, not a controlled comparison. The team philosophy is captured in Lopopolo's three-word epigram: ***"Humans steer. Agents execute."***

**Internal user validation (verbatim):** *"the product has been used by hundreds of users internally, including daily internal power users"* — and the experiment *"has so far worked well up through internal launch and adoption at OpenAI."* Importantly, not just a research artifact — a real shipped product with real internal usage.

**Initial scaffold provenance (verbatim — NEW):** *"The initial scaffold — repository structure, CI configuration, formatting rules, package manager setup, and application framework — was generated by Codex CLI using GPT-5, guided by a small set of existing templates. Even the initial AGENTS.md file that directs agents how to work in the repository was itself written by Codex."* The recursive observation matters: AGENTS.md (the harness contract) is itself an agent artifact, not a hand-written input.

**Architectural model (canonical phrasing — NEW with verbatim layer list):** *"Each business domain is divided into a fixed set of layers, with strictly validated dependency directions and a limited set of permissible edges."* The verbatim layer list: *"within each business domain (e.g. App Settings), code can only depend 'forward' through a fixed set of layers (**Types → Config → Repo → Service → Runtime → UI**). Cross-cutting concerns (auth, connectors, telemetry, feature flags) enter through a single explicit interface: **Providers**."* Lopopolo's framing: *"This is the kind of architecture you usually postpone until you have hundreds of engineers. With coding agents, it's an early prerequisite: the constraints are what allows speed without decay or architectural drift."*

**Repository-as-system-of-record (verbatim docs tree — NEW):** instead of a single AGENTS.md the team uses *"a structured `docs/` directory treated as the system of record. A short AGENTS.md (roughly **100 lines**) is injected into context and serves primarily as a map, with pointers to deeper sources of truth elsewhere."* The canonical tree (verbatim):

```
AGENTS.md
ARCHITECTURE.md
docs/
├── design-docs/
│   ├── index.md
│   ├── core-beliefs.md
│   └── ...
├── exec-plans/
│   ├── active/
│   ├── completed/
│   └── tech-debt-tracker.md
├── generated/
│   └── db-schema.md
├── product-specs/
│   ├── index.md
│   ├── new-user-onboarding.md
│   └── ...
└── references/
    ├── design-system-reference-llms.txt
    ├── nixpacks-llms.txt
    ├── uv-llms.txt
    └── ...
DESIGN.md
FRONTEND.md
PLANS.md
PRODUCT_SENSE.md
QUALITY_SCORE.md
RELIABILITY.md
SECURITY.md
```

The four canonical failure modes of the "one big AGENTS.md" anti-pattern (verbatim, with Lopopolo's framing): *"Context is a scarce resource… Too much guidance becomes non-guidance… It rots instantly… It's hard to verify."* The doc-gardening cleanup is itself automated: *"A recurring 'doc-gardening' agent scans for stale or obsolete documentation that does not reflect the real code behavior and opens fix-up pull requests."*

**Application legibility for the agent (verbatim — NEW):** *"we made the app bootable per git worktree, so Codex could launch and drive one instance per change. We also wired the Chrome DevTools Protocol into the agent runtime and created skills for working with DOM snapshots, screenshots, and navigation."* Observability is similarly agent-facing: *"Logs, metrics, and traces are exposed to Codex via a local observability stack that's ephemeral for any given worktree… Agents can query logs with LogQL and metrics with PromQL."* With this surface available, prompts like *"ensure service startup completes in under 800ms"* or *"no span in these four critical user journeys exceeds two seconds"* are tractable.

**Long-run autonomy (verbatim):** *"We regularly see single Codex runs work on a single task for upwards of **six hours** (often while the humans are sleeping)."* This is the canonical anchor for the "overnight agent" pattern Cherny references (followup/03 §"Overnight agent") and Willison sketches (`research/05-simon-willison.md`).

**End-to-end feature autonomy threshold (verbatim ten-step list — NEW):** Lopopolo claims the team *"recently crossed a meaningful threshold where Codex can end-to-end drive a new feature."* Given a single prompt, the agent now: (1) validates the current state of the codebase, (2) reproduces a reported bug, (3) records a video demonstrating the failure, (4) implements a fix, (5) validates the fix by driving the application, (6) records a second video demonstrating the resolution, (7) opens a pull request, (8) responds to agent and human feedback, (9) detects and remediates build failures, (10) escalates to a human *"only when judgment is required,"* and finally merges the change. Lopopolo's own caveat: *"This behavior depends heavily on the specific structure and tooling of this repository and should not be assumed to generalize without similar investment — at least, not yet."*

**Entropy / garbage-collection regime (verbatim — NEW):** *"Our team used to spend every Friday (**20% of the week**) cleaning up 'AI slop.' Unsurprisingly, that didn't scale."* The replacement: *"'golden principles' directly into the repository and built a recurring cleanup process… On a regular cadence, we have a set of background Codex tasks that scan for deviations, update quality grades, and open targeted refactoring pull requests. Most of these can be reviewed in under a minute and automerged."* The framing — *"Technical debt is like a high-interest loan: it's almost always better to pay it down continuously in small increments than to let it compound and tackle it in painful bursts"* — is the canonical statement of continuous, agent-driven technical-debt amortization.

**Merge philosophy (verbatim — NEW):** *"The repository operates with **minimal blocking merge gates**. Pull requests are short-lived. Test flakes are often addressed with follow-up runs rather than blocking progress indefinitely. In a system where agent throughput far exceeds human attention, corrections are cheap, and waiting is expensive."* Lopopolo immediately flags this as a regime-specific posture: *"This would be irresponsible in a low-throughput environment. Here, it's often the right tradeoff."*

**Review philosophy (verbatim — NEW):** *"Humans may review pull requests, but aren't required to. Over time, we've pushed almost all review effort towards being handled agent-to-agent."* This is the strongest published claim from inside OpenAI that **human PR review is no longer load-bearing at the per-PR level** in their internal agent-driven product — a non-obvious refutation of "human review is the trust anchor" doctrine.

**The agent-legibility framing (verbatim):** *"From the agent's point of view, anything it can't access in-context while running effectively doesn't exist. Knowledge that lives in Google Docs, chat threads, or people's heads are not accessible to the system. Repository-local, versioned artifacts (e.g., code, markdown, schemas, executable plans) are all it can see."* And the rule: *"We learned that we needed to push more and more context into the repo over time. That Slack discussion that aligned the team on an architectural pattern? If it isn't discoverable to the agent, it's illegible in the same way it would be unknown to a new hire joining three months later."*

**Time-stamp:** numbers are **as of 2026-02-11**, describing the five months ending February 2026 (~mid-Sep 2025 → mid-Feb 2026). Ongoing experiment, not terminal state — by consumption time, all numbers may have shifted.

**Vs. OpenHands** (`11-openhands-substrate-audit.md` §1): OpenHands reports 61% reduction in system-attributable failures (78.0 → 30.0/1k conversations, 15-day rollout). Not commensurable — OpenHands measures *deployed-agent reliability*, Codex measures *single-team PR throughput*. Both are load-bearing for the factory thesis.

**Caveat (Willison "looking-the-part hazard," May 6 2026):** 1,500 merged ≠ 1,500 correct. The canonical text reports **no** bug-rate, regression-rate, or post-merge defect density. The "1/10th time" claim is a team self-estimate, not a controlled comparison. Productivity is necessary but not sufficient evidence; defect-of-origin metrics needed alongside, especially for Architectures 3 and 4. Lopopolo's own concluding caveat (verbatim): *"What we don't yet know is how architectural coherence evolves over years in a fully agent-generated system."*

---

## 6. Substrate posture per architecture

Mapping Codex's five surfaces + AGENTS.md + Subagents + sandbox×approval to each architecture:

**Arch 1 — Specification Refinery** ("the spec is the product"). AGENTS.md is a direct fit: the spec-ingestion contract in Codex's own terms; the Refinery's spec stack maps to AGENTS.md root-to-leaf. SDK is load-bearing — the seven-phase revelation cycle is an SDK orchestrator. Cloud runs the Implementer per cycle, isolated from the Spec Author. Subagents used sparingly (spawn-on-demand: scenario generation by the Scenario Designer). Defaults: `workspace-write` + `never`, Cloud net-off with `pip`/`npm` allowlist. `auto_review` routes sandbox-escalations through Scenario Designer / Reviewer.

**Arch 2 — Compound Atelier** ("each unit makes the next easier"). Per-workshop AGENTS.md slices in workshop-specific subdirectories; root AGENTS.md holds the Plan → Work → Review → Compound loop; override files are workshop escape hatches. The reviewer panel is the canonical fanout: each reviewer is a parallel Cloud-dispatched Subagent — Codex's "collect results into a single response" is exactly the panel-aggregation primitive. Cloud isolation is critical: reviewers must not share workspace with the implementer or each other. `auto_review` is less load-bearing (the panel itself is the reviewer), but the *implementer* should still run with it.

**Arch 3 — Phase-Gated Foundry** ("formal phases become right when agents make them fast"). Phase-specific AGENTS.md per phase; overrides express phase-specific spec divergence. Construction: `workspace-write` + `never`. V&V: `untrusted` (escalate anything non-allowlisted) **or** `granular` approval policy with sandbox-escape and request_permissions categories left interactive [2026-05-13 primary fetch ✅ for `granular`]. `auto_review` is a strong fit — the architecture *requires* V&V on a different model family from construction; the auto-review four-tier risk lattice (low/medium/high/critical, fail-closed) is the substrate-level enforcement, with custom `guardian_policy_config` available for enterprise tightening. Subagents are model-typed per role via the custom-agent TOML `model = "..."` knob (`d179e7b09d_*.md` lines 920, 934, 948); the primary three-agent PR-review pattern (§3.4) is directly adoptable. Each phase = separate Cloud task; gates are dispatch boundaries.

**Arch 4 — Evolutionary Tournament** ("set up conditions under which the right answer wins"). Single root AGENTS.md + per-genome override files. Cloud + Subagents are maximally load-bearing — each generation is N parallel Cloud subagents, one per genome; Codex's fanout-and-collect is the selection substrate. Mandatory: `workspace-write` + `never` (validation harness selects, not the agent), network off + allowlist (exfiltration risk × N). **`auto_review` likely disabled** — per-agent review wastes compute when the validation harness is the review. S9's "rigid architectural model" (Types → Config → Repo → Service → Runtime → UI) is adoptable as the *genome envelope*: variants compete within the same dependency layering.

**Cross-architecture: the App Server primitive.** Load-bearing for all four. Stable JSON-RPC, Thread/Turn/Item primitives, transport-agnostic (stdio/websocket/unix-socket) — an SDK-targeted orchestrator can swap surfaces (develop in IDE, run unattended via CLI, scale via Cloud) without code changes. The article's framing — *"the real product boundary is the stable protocol around the agent loop, not only the model itself"* — is the strongest single architectural lesson from Codex. Our factory should adopt the same boundary: the protocol between Spec Author / Implementer / Reviewer is the load-bearing artifact; models behind roles are hot-swappable.

---

## 7. Open follow-ups

- **~~Primary-URL re-fetch.~~ [2026-05-16 CLOSED — Cluster F manual drain]** All 8 originally-🟡 URLs in scope are now ✅ primary-anchored: 5 `developers.openai.com/codex/*` via issue #41 (2026-05-13); `running-codex-safely/` via Cluster E manual drain (2026-05-16, §4.4); `harness-engineering/` and `unlocking-the-codex-harness/` via Cluster F manual drain (2026-05-16, §5 and §1 respectively); plus the newly-indexed `developers.openai.com/codex/rules` (2026-05-16, §4.3). The `openai.com/index/*` host remains Cloudflare-blocked for the action runner but is fully primary-anchored via the human-attended browser path (Path B) for every URL this report cites. The corresponding entry in `research/blocked-urls.md` for the `openai.com/index/*` host class can now be down-prioritized for this report's scope.
- **App Server transport surface.** `websocket`/`unix-socket` are "experimental" per `codex-rs/app-server/README.md`. Factory dashboards likely want websocket; experimental status is a tracked risk.
- **~~`auto_review` model selection.~~ [2026-05-13 partially resolved]** S23 primary (line 882) places the default reviewer policy at `github.com/openai/codex/blob/main/codex-rs/core/src/guardian/policy.md` (open-source; fetchable) and confirms enterprises can override via `guardian_policy_config` in managed requirements; `allowed_approvals_reviewers` can constrain reviewer selection (line 886). **Remaining unknown:** the *identity* of the default reviewer model is still not surfaced on this page.
- **~~Non-Cloud subagent workspace inheritance.~~ [2026-05-13 RESOLVED via §3.3]** Primary S11 (lines 805-815) confirms subagents inherit parent sandbox policy plus live runtime overrides; per-agent file-level overrides possible. Architecture 2 reviewer-panel isolation discipline must explicitly use Cloud dispatch if isolation from the implementer is required.
- **Open-source `guardian/policy.md` fetch.** New follow-up: the auto-review default policy text is open-source — fetching it would deepen §4.1 with the actual rule definitions (currently we only have the abstract risk lattice).
- **`spawn_agents_on_csv` stability.** Marked **experimental** by primary; if Architecture 4 relies on it, monitor for breaking changes in changelog.
- **GPT-5.2 Codex system cards.** PDFs at `cdn.openai.com/pdf/...gpt-5-codex...` (Sep 2025), `5p1_codex_max_card_03.pdf` (Nov 2025), `oai_5_2_Codex.pdf` (Dec 2025) contain primary attestations of sandbox/approval/prompt-injection mitigations. Not consumed here; would deepen §4.
- **Defect-rate context for the 1,500-PR figure.** S9 reports no post-merge defect density; "looking-the-part hazard" (Willison, May 6 2026) makes this load-bearing. Worth a follow-up if OpenAI publishes 6/12-month update.
- **macOS / Windows sandbox primitives.** Now anchored at primary (Seatbelt + sandbox-exec on macOS; Windows sandbox or WSL2-Linux on Windows) — but the macOS Seatbelt profile text is not surfaced; threat-model audit would want the actual `-p` profile content.

---

## 8. Verdict

Codex is the most thoroughly factored coding-agent substrate currently documented: five surfaces over one stable JSON-RPC App Server, layered AGENTS.md spec-ingestion with explicit override and size-budget semantics (primary-anchored 2026-05-13), Subagents orchestration with three built-in agents (`default`/`worker`/`explorer`) plus per-project custom-agent TOML files (primary-anchored 2026-05-13) that composes natively with Cloud for true parallelism, and a two-axis sandbox×approval policy with `auto_review` defense-in-depth (four-tier risk lattice with fail-closed semantics, primary-anchored 2026-05-13) that severs the trifecta's exfiltration leg by default. Linux sandbox primitive is **`bwrap` + `seccomp`** (not Landlock as originally reconstructed) [2026-05-13 primary fetch REFUTES]; macOS is Seatbelt; Windows uses WSL2 (Linux sandbox) or a native Windows sandbox. The S9 harness-engineering experiment (Ryan Lopopolo, 2026-02-11; primary-anchored 2026-05-16) — three engineers ramping to seven, ~1M LOC, ~1,500 merged PRs in five months, **3.5 PRs/engineer/day as the small-team baseline with per-engineer throughput *increasing* as the team grew**, ~1/10th the human-coded baseline, six-hour single-agent runs, end-to-end feature autonomy from prompt to merge — is the strongest single attestation that an agent-first factory works at team scale; it is also a date-stamped snapshot of an ongoing experiment, and its defect-rate counterfactual is unreported. Adopt: App Server's "stable protocol around the agent loop" as organizing principle; AGENTS.md layering as spec-ingestion contract (complementary to our `.claude/skills/` registry, not replacing it); Subagents-on-Cloud as parallelism substrate for Architectures 2 and 4; two-axis sandbox×approval with default-off network and `granular` approval categories as the lethal-trifecta defense across all four.
