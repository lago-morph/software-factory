# Research Report 18 — OpenAI Codex Substrate Audit

**Date:** 2026-05-11
**Author:** Round-5 subagent sub-20 (fanout 20260511-054258)
**Cluster:** Round-5 13.1.1 per `research/PLAN.md` §13.1.1
**Companion reports:** `research/11-openhands-substrate-audit.md` (OpenHands analog), `research/04-every-skill-libraries.md` (Every skill registry analog), `research/09-jaymin-book-harnesses-practices-mental-models.md` (harness terminology), `research/00-synthesis.md` (cross-substrate framing).
**Stance in one sentence:** Codex is *not* a model — it is a five-surface harness around a stable App Server protocol, with AGENTS.md as the spec-ingestion contract, Subagents as the orchestration primitive, and a layered sandbox/approval matrix as the trifecta defense.

---

## 0. Sources reviewed

Status legend: ✅ primary URL reachable · 🟡 primary 403 from sandbox, content reconstructed from open-source mirrors and WebSearch extracts cross-checked against ≥2 independent re-hosters.

| ID | URL | Status | Reconstruction route |
|---|---|---|---|
| S8 — Codex overview | `https://developers.openai.com/codex` | 🟡 | WebSearch + App Server article's surface enumeration. |
| S9 — Harness engineering (2026-02-11) | `https://openai.com/index/harness-engineering/` | 🟡 | Verbatim quotes via `raw.githubusercontent.com/celesteanders/harness/main/docs/research/260211_openai_harness_engineering_codex.md`; cross-checked vs. latent.space and swequiz.com. |
| S10 — AGENTS.md | `https://developers.openai.com/codex/guides/agents-md` | 🟡 | WebSearch detailed extract; cross-checked vs. open-source `openai/codex/docs/agents_md.md` and `agents.md/` spec site. |
| S11 — Subagents | `https://developers.openai.com/codex/subagents` | 🟡 | WebSearch extracts. |
| S23 — Agent approvals & security | `https://developers.openai.com/codex/agent-approvals-security` | 🟡 | WebSearch + sibling `concepts/sandboxing` and `security` snippets. |
| App Server article — Celia Chen, 2026-02-04 | `https://openai.com/index/unlocking-the-codex-harness/` | 🟡 | Verbatim re-host: `raw.githubusercontent.com/newton20/harness-engineering-kb/master/raw/openai-com-index-unlocking-the-codex-harness.md`; cross-checked vs. infoq.com and `codex-rs/app-server/README.md`. |
| Open-source `codex-rs/app-server/README.md` | `github.com/openai/codex/blob/main/codex-rs/app-server/README.md` | ✅ | JSON-RPC 2.0 transports, Thread/Turn/Item primitives, endpoint surface. |
| Open-source `docs/agents_md.md` | `github.com/openai/codex/blob/main/docs/agents_md.md` | ✅ | Confirms `child_agents_md` config-toml feature flag. |
| Cloud-env docs | `https://developers.openai.com/codex/cloud/environments` | 🟡 | WebSearch: isolated containers, network off by default, allowlist mechanism. |

**Reachability note:** every `*.openai.com` URL 403s from this sandbox (consistent with `research/blocked-urls.md` v5). Content recovered via mirrors is consistent across ≥2 independent re-hosters for every load-bearing claim. No new fetch issue filed; a retroactive cookie-fetch or Wayback pass would tighten quotation fidelity but would not change any conclusion below. Recorded as open follow-up in §7.

---

## 1. The five-surface deployment model

The App Server article (Celia Chen, OpenAI, 2026-02-04 — "Unlocking the Codex harness") states:

> *"OpenAI's coding agent Codex exists across many different surfaces: the web app, the CLI, the IDE extension, and the new Codex macOS app. Under the hood, they're all powered by the same Codex harness — the agent loop and logic that underlies all Codex experiences."*

That is four surfaces by Chen's enumeration; the fifth — the SDK (Python + TypeScript at `developers.openai.com/codex/sdk`) — is a programmatic client of the same App Server protocol, distinct because it is the only surface designed to be driven by other programs rather than humans.

| # | Surface | Substrate role | OpenHands analog (`11-openhands-substrate-audit.md` §2) |
|---|---|---|---|
| 1 | **CLI** (`codex` / TUI) | Interactive power-user use; CI via `codex exec`. | OpenHands CLI (`openhands --headless`). |
| 2 | **IDE extension** (VS Code, Xcode, JetBrains) | Pair-programming/review; embeds App Server as JSON-RPC stdio child. | OpenHands GUI server (REST/WebSocket browser). |
| 3 | **App** (macOS desktop; ChatGPT mobile Codex mode) | Ambient plan-approve-merge surface. | None first-party. |
| 4 | **Cloud** ("Codex web") | Background tasks; each runs in an isolated OpenAI-managed container, repo preloaded. The actual-concurrency substrate for parallel Subagents (§3). | OpenHands cloud (`app.all-hands.dev`). |
| 5 | **SDK** (Python + TypeScript) | Programmatic embedding; controls a local App Server child over JSON-RPC. The orchestrator-target surface. | OpenHands four-package SDK (`sdk`/`tools`/`workspace`/`agent_server`). |

**The App Server is not a sixth surface** — it is the protocol substrate underneath all five, described as "both the JSON-RPC protocol between the client and the server *and* a long-lived process that hosts the Codex core threads." Same architectural move as OpenHands V1: extract the agent loop, expose via stable interface, every surface becomes "just another client." App Server ≅ OpenHands `agent_server`.

**Factory fit:** SDK is load-bearing for orchestrators across Architectures 1–4. Cloud is load-bearing for parallel execution (Architecture 4 population members; Architecture 2 reviewer panels). CLI/IDE/App are human-in-loop surfaces. Protocol uniformity means a Symphony-style orchestrator written against the SDK can hand off to the IDE for human review without re-serializing state — App Server already exposes Thread/Turn/Item primitives.

---

## 2. AGENTS.md instruction layering — full model

Per S10 + the `agents.md` open spec site:

**Discovery, root-to-leaf:** (1) **Global scope** — Codex reads `~/.codex/AGENTS.override.md` if present, else `~/.codex/AGENTS.md`; only the first non-empty file at this level is used. (2) **Project scope** — Codex walks from project root down to the current working directory, at each level checking `AGENTS.override.md`, then `AGENTS.md`, then any names in `project_doc_fallback_filenames`.

**Precedence:** files closer to the working directory override earlier guidance by appearing **later in the concatenated prompt**. Each file is injected as its own user-role message near the top of conversation history, in root-to-leaf order, prefixed with `# AGENTS.md instructions for <directory>` (path relative to repo root).

**Override semantics:** at any level where `AGENTS.override.md` exists, Codex reads it and **skips `AGENTS.md` at the same level**. Override replaces, not adds — the per-scope escape hatch.

**Size budget:** `project_doc_max_bytes` default **32 KiB**; files past the cap are dropped. Empty files skipped silently.

**Subagent layering:** with the `child_agents_md` flag (confirmed in `openai/codex/docs/agents_md.md`), Codex appends scope-and-precedence guidance so a subagent dispatched into `services/billing/` sees that subdirectory's slice, not just root.

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

Per S11:

> *"A subagent is a specialized Codex instance spawned by the main agent to handle one piece of a larger task, and Codex can now run those subagents in parallel and collect their results into a single response. ... Codex handles orchestration across agents, including spawning new subagents, routing follow-up instructions, waiting for results, and closing agent threads."*

**Composition with Cloud.** On CLI/IDE/App surfaces, parallelism is bounded by the single host process (multiple Threads exist via the App Server's `create`/`resume`/`fork` endpoints but share compute/FS). On **Cloud**, each subagent task runs in its **own isolated OpenAI-managed container**, repo preloaded — this is where Subagents become a real scaling mechanism. Cloud + Subagents + AGENTS.md scoping is the triangle that makes "weeks of work in days" plausible.

**Custom subagents:** "different model configurations and instructions depending on the task" — same shape as Claude Code's `agents/` directory and Every's `everyskill` registry, but routed through the App Server's plugins/skills surface rather than filesystem.

**Vs. OpenHands** (`11-openhands-substrate-audit.md` §4): OpenHands V1 sub-agent delegation is "blocking-parallel only, sub-agents inherit parent model/workspace." Codex differs on two axes: **non-blocking parallelism** (orchestrator collects results — fan-out, not serial) and **isolated workspaces** in Cloud (each container fresh, not parent-inherited). Codex's model maps to our `parallel-subagent-fanout` skill; OpenHands' maps to plan-and-delegate.

**Composition with AGENTS.md:** `child_agents_md` makes subagents read their target subdirectory's slice plus root plus global — they inherit the *spec gradient*, not the parent's working context.

---

## 4. Approvals, sandbox, network — the lethal-trifecta defense

Simon Willison's "lethal trifecta" (`research/05-simon-willison.md`): **untrusted input + private data + ability to exfiltrate**. Codex's defense is a *two-axis policy* — sandbox mode controls technical boundaries; approval mode controls when Codex stops at them. The two compose.

**Sandbox modes (S23 + `concepts/sandboxing`):**

| Mode | FS | Net | Use |
|---|---|---|---|
| `read-only` | none | none | Review/exploration; toggle via `/permissions`. |
| `workspace-write` (default) | within workspace | off by default | Default low-friction local. |
| `danger-full-access` | unrestricted | unrestricted | Pair with `approval_policy = "never"` for unattended disposable-container automation. |

Implementation: **Landlock + seccomp** on Linux (Seatbelt on macOS implied by macOS-app existence; not in 403'd primary). Described as "the only major agent with sandboxing enabled by default" — stronger than OpenHands V1 (sandbox opt-in per `11-openhands-substrate-audit.md` §4a) or Claude Code (permission prompts, not kernel isolation).

**Approval modes (S23):**

| Mode | Behaviour |
|---|---|
| `never` | "Never ask the user for approval; persist and work around constraints." Required for CI/cloud/eval. |
| `on-request` | "Commands run in sandbox by default; specify in your tool call to escalate without sandbox." Default interactive. |
| `on-failure` | "Allow all in sandbox; failures escalated for approval to re-run without sandbox." Trusted-but-flaky. |
| `untrusted` | "Escalate most commands for approval, apart from a limited allowlist of safe 'read' commands." Max-skepticism. |

Naming-history note: earlier Codex CLI used `suggest` / `auto-edit` / `full-auto` (inventivehq.com KB). Current canonical names are the four above; both appear in the wild.

**Auto-reviewer:** `approvals_reviewer = "auto_review"` routes eligible approval requests through a *reviewer agent* — evaluates "sandbox escalations, network requests, request_permissions prompts, or side-effecting app and MCP tool calls." Prompt-injection defense in depth: requestor ≠ evaluator. Same shape as Architecture 3's "V&V on a different model family from construction," at finer granularity.

**Cloud egress (`cloud/environments`):**

> *"Setup scripts run with internet access, but agent internet access is off by default. ... By default, Codex cloud agents have no internet access during runtime ... allowlist for common software dependency domains, add domains and trusted sites, and specify allowed HTTP methods."*

The **trifecta closure**: setup phase (where `npm install` etc. need network) gets it; agent phase (where untrusted-input lives — issue bodies, PR comments, tool output) defaults to none. Exfiltration leg severed by default on Cloud.

**Factory implications:**

| Trifecta leg | Codex control | Factory adoption |
|---|---|---|
| Untrusted input | Cached web-search vs. live (S23 recommendation). | Architecture 1 already enforces single-input-source via spec. |
| Private data | `workspace-write` default; workspace boundaries. | Mirror; every Implementer in `workspace-write` with workspace = single git worktree. |
| Exfiltration | Net off in Cloud; `auto_review` for sandbox escalations. | Strongest lift. Mandate net-off + allowlist for cloud-dispatched subagents; `auto_review` for any network-egress request. |

The two-axis split is more compositional than OpenHands V1's collapsed `ConfirmationPolicy` (per `11-openhands-substrate-audit.md` §8). Factory should copy the split.

---

## 5. Harness-engineering productivity numbers (verbatim)

From **"Harness engineering: leveraging Codex in an agent-first world"** (S9; Celia Chen et al., **2026-02-11**; quotations via the `celesteanders/harness` mirror):

> *"Over the past five months, our team has been running an experiment: building and shipping an internal beta of a software product with 0 lines of manually-written code."*

> *"Five months later, the repository contains on the order of a million lines of code across application logic, infrastructure, tooling, documentation, and internal developer utilities."*

> *"Over that period, roughly 1,500 pull requests have been opened and merged"* — with *"an average throughput of **3.5 PRs per engineer per day**."*

> *"The team grew from three engineers to seven during development."*

> *"Every line of code — application logic, tests, CI configuration, documentation, observability, and internal tooling — was written by Codex. The team estimates that they built this in about 1/10th the time it would have taken to write the code by hand."*

**Architectural context (verbatim):** *"a rigid architectural model organizing code into business domains with fixed dependency layers: Types → Config → Repo → Service → Runtime → UI"*, with cross-cutting concerns (auth, connectors, telemetry, feature flags) entering through a `Providers` interface. *"Repository knowledge is organized in a structured `docs/` directory containing design-docs, exec-plans, product-specs, and references, with a brief AGENTS.md serving as a 'table of contents.'"*

**Time-stamp:** numbers are **as of 2026-02-11**, describing the five months ending February 2026 (~mid-Sep 2025 → mid-Feb 2026). Ongoing experiment, not terminal state — by consumption time, all numbers may have shifted.

**Vs. OpenHands** (`11-openhands-substrate-audit.md` §1): OpenHands reports 61% reduction in system-attributable failures (78.0 → 30.0/1k conversations, 15-day rollout). Not commensurable — OpenHands measures *deployed-agent reliability*, Codex measures *single-team PR throughput*. Both are load-bearing for the factory thesis.

**Caveat (Willison "looking-the-part hazard," May 6 2026):** 1,500 merged ≠ 1,500 correct. S9 reports no bug-rate, regression-rate, or post-merge defect density. The "1/10th time" claim is a team self-estimate, not a controlled comparison. Productivity is necessary but not sufficient evidence; defect-of-origin metrics needed alongside, especially for Architectures 3 and 4.

---

## 6. Substrate posture per architecture

Mapping Codex's five surfaces + AGENTS.md + Subagents + sandbox×approval to each architecture:

**Arch 1 — Specification Refinery** ("the spec is the product"). AGENTS.md is a direct fit: the spec-ingestion contract in Codex's own terms; the Refinery's spec stack maps to AGENTS.md root-to-leaf. SDK is load-bearing — the seven-phase revelation cycle is an SDK orchestrator. Cloud runs the Implementer per cycle, isolated from the Spec Author. Subagents used sparingly (spawn-on-demand: scenario generation by the Scenario Designer). Defaults: `workspace-write` + `never`, Cloud net-off with `pip`/`npm` allowlist. `auto_review` routes sandbox-escalations through Scenario Designer / Reviewer.

**Arch 2 — Compound Atelier** ("each unit makes the next easier"). Per-workshop AGENTS.md slices in workshop-specific subdirectories; root AGENTS.md holds the Plan → Work → Review → Compound loop; override files are workshop escape hatches. The reviewer panel is the canonical fanout: each reviewer is a parallel Cloud-dispatched Subagent — Codex's "collect results into a single response" is exactly the panel-aggregation primitive. Cloud isolation is critical: reviewers must not share workspace with the implementer or each other. `auto_review` is less load-bearing (the panel itself is the reviewer), but the *implementer* should still run with it.

**Arch 3 — Phase-Gated Foundry** ("formal phases become right when agents make them fast"). Phase-specific AGENTS.md per phase; overrides express phase-specific spec divergence. Construction: `workspace-write` + `never`. V&V: `untrusted` (escalate anything non-allowlisted). `auto_review` is a strong fit — the architecture *requires* V&V on a different model family from construction; `auto_review` is the substrate-level enforcement. Subagents are model-typed per role (Opus for construction, Sonnet for V&V). Each phase = separate Cloud task; gates are dispatch boundaries.

**Arch 4 — Evolutionary Tournament** ("set up conditions under which the right answer wins"). Single root AGENTS.md + per-genome override files. Cloud + Subagents are maximally load-bearing — each generation is N parallel Cloud subagents, one per genome; Codex's fanout-and-collect is the selection substrate. Mandatory: `workspace-write` + `never` (validation harness selects, not the agent), network off + allowlist (exfiltration risk × N). **`auto_review` likely disabled** — per-agent review wastes compute when the validation harness is the review. S9's "rigid architectural model" (Types → Config → Repo → Service → Runtime → UI) is adoptable as the *genome envelope*: variants compete within the same dependency layering.

**Cross-architecture: the App Server primitive.** Load-bearing for all four. Stable JSON-RPC, Thread/Turn/Item primitives, transport-agnostic (stdio/websocket/unix-socket) — an SDK-targeted orchestrator can swap surfaces (develop in IDE, run unattended via CLI, scale via Cloud) without code changes. The article's framing — *"the real product boundary is the stable protocol around the agent loop, not only the model itself"* — is the strongest single architectural lesson from Codex. Our factory should adopt the same boundary: the protocol between Spec Author / Implementer / Reviewer is the load-bearing artifact; models behind roles are hot-swappable.

---

## 7. Open follow-ups

- **Primary-URL re-fetch.** All seven primary URLs (S8/S9/S10/S11/S23/App Server/cloud-env) 403 from sandbox; mirrored content consistent across ≥2 sources for every load-bearing claim, but verbatim fidelity would tighten with cookie-fetch or Wayback. File issue only if downstream needs more exact quotation.
- **App Server transport surface.** `websocket`/`unix-socket` are "experimental" per `codex-rs/app-server/README.md`. Factory dashboards likely want websocket; experimental status is a tracked risk.
- **`auto_review` model selection.** S23 confirms `approvals_reviewer = "auto_review"` exists; doesn't name the reviewer model or its configurability. Matters for Architecture 3's "different model family" enforcement.
- **Non-Cloud subagent workspace inheritance.** Cloud subagents are isolated containers (confirmed); CLI/IDE/App subagent workspace inheritance is unconfirmed. Affects Architecture 2's reviewer-panel isolation discipline.
- **GPT-5.2 Codex system cards.** PDFs at `cdn.openai.com/pdf/...gpt-5-codex...` (Sep 2025), `5p1_codex_max_card_03.pdf` (Nov 2025), `oai_5_2_Codex.pdf` (Dec 2025) contain primary attestations of sandbox/approval/prompt-injection mitigations. Not consumed here; would deepen §4.
- **Defect-rate context for the 1,500-PR figure.** S9 reports no post-merge defect density; "looking-the-part hazard" (Willison, May 6 2026) makes this load-bearing. Worth a follow-up if OpenAI publishes 6/12-month update.

---

## 8. Verdict

Codex is the most thoroughly factored coding-agent substrate currently documented: five surfaces over one stable JSON-RPC App Server, layered AGENTS.md spec-ingestion with explicit override and size-budget semantics, Subagents orchestration that composes natively with Cloud for true parallelism, and a two-axis sandbox×approval policy with `auto_review` defense-in-depth that severs the trifecta's exfiltration leg by default. The S9 harness-engineering experiment (2026-02-11) — 3-to-7 engineers, ~1M LOC, ~1,500 merged PRs in five months, ~3.5 PRs/engineer/day, ~1/10th the human-coded baseline — is the strongest single attestation that an agent-first factory works at team scale; it is also a date-stamped snapshot of an ongoing experiment, and its defect-rate counterfactual is unreported. Adopt: App Server's "stable protocol around the agent loop" as organizing principle; AGENTS.md layering as spec-ingestion contract (complementary to our `.claude/skills/` registry, not replacing it); Subagents-on-Cloud as parallelism substrate for Architectures 2 and 4; two-axis sandbox×approval with default-off network as the lethal-trifecta defense across all four.
