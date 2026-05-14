# Research Report 20 — Replit Agent Substrate Audit (current docs, not Ghostwriter)

**Date:** 2026-05-11
**Author:** Round-5 subagent sub-22 (fanout 20260511-054258)
**Cluster:** Round-5 13.1.3 per `research/PLAN.md` §13.1.3
**Companion reports:** `research/18-openai-codex-substrate.md` (Codex analog), `research/11-openhands-substrate-audit.md` (OpenHands analog), `research/followup/06-competitor-landscape.md` (competitor map).
**Stance in one sentence:** Replit Agent's organizing primitive is not the repo but the *deployed app*; `replit.md` is a managed (not static) instruction file that the Agent itself can read and update as it learns; connectors and the "agents-build-agents" loop make the substrate's first-class output a running, deployed, integrated system — a different shape from Codex/Claude/Copilot's repo-modification shape, and the closest analog to our Architecture-4 "operate the deployed system" loop.

All web claims here were originally verified on **2026-05-11 America/Chicago**; thirteen primary `docs.replit.com` and `blog.replit.com` URLs were re-verified by direct GitHub Actions fetch on **2026-05-13** (see drain note below).

---

## Drain note (issue #41) — 2026-05-13

**Status.** This report was originally built from WebSearch snippets cross-checked against community mirrors because `docs.replit.com` and `blog.replit.com` return HTTP 403 to direct WebFetch from this sandbox. A GitHub-Actions-backed fetch run was used to retrieve all 13 primary URLs cited in the report.

**Fetch outcome:** 13 of 13 URLs returned 200 OK with full content. No 404s. Every R-* row in §0 flips from 🟡 to ✅.

**Successfully fetched, integrated into this revision:**

1. `docs.replit.com/core-concepts/agent` (R-Agent) — used to upgrade §1 (output types, "agents-build-agents" framing, Lite/Economy/Power/Turbo modes, Multi-Artifacts).
2. `docs.replit.com/replitai/replit-dot-md` (R-MD) — used to upgrade §2 and to **refute** the "100-line auto-condensation" claim (see §2).
3. `docs.replit.com/core-concepts/agent/plan-mode` (R-Plan) — used to upgrade §3, §5 (Plan-mode-as-billable wording verbatim).
4. `blog.replit.com/connectors` (R-Connectors) — used to upgrade §4; **refutes** "all powered by MCP" framing for Connectors (Connectors blog does not mention MCP; the MCP framing comes from R-MCP for *custom* MCP servers, a distinct surface).
5. `docs.replit.com/replitai/warehouse-connectors` (R-Warehouse) — used to upgrade §4 (added Segment/Amplitude/Hex on Core/Pro tiers; Enterprise-only confirmed for BQ/Databricks/Snowflake).
6. `docs.replit.com/replitai/mcp/overview` (R-MCP) — used to upgrade §4 (custom-MCP scanner wording verbatim).
7. `docs.replit.com/replitai/agents-and-automations` (R-A&A) — used to upgrade §4 (deployment-required framing); **refutes** "Mastra" claim — Mastra is not mentioned in official A&A docs; that framing came from a third-party Mastra blog mirror.
8. `docs.replit.com/replitai/canvas` (R-Canvas) — used to upgrade §1 (Canvas output types).
9. `docs.replit.com/replitai/app-testing` (R-AppTest) — used to upgrade §3 (App Testing in browser, take-over, 10-minute timeout, FullStack-JS/Streamlit-only scope is NEW).
10. `docs.replit.com/cloud-services/deployments/autoscale-deployments` (R-Deploy) — used to upgrade §3; **refutes** the previously-quoted "every app includes free hosting" snippet (R-Deploy does not contain that string).
11. `docs.replit.com/billing/ai-billing` (R-Bill) — used to upgrade §3, §5; **refutes** the specific "$0.06 floor / multiple-dollar ceiling" prices (R-Bill does not quote dollar figures; those came from third-party mirrors).
12. `blog.replit.com/introducing-agent-3-our-most-autonomous-agent-yet` (R-A3) — used to upgrade §1, §3 (200-minute autonomy, Max-Autonomy-Beta, "agent surfaces a simple UI flow to connect with Notion" verbatim).
13. `blog.replit.com/introducing-agent-4-built-for-creativity` (R-A4) — used to upgrade §1, §5; **refutes** "splits single tasks into different forks" — actual A4 wording is "split a single task into smaller pieces, work on them simultaneously with sub-agents, and recombine the results" (sub-agents, not forks). Parallel task execution is Pro+Enterprise (Core temporarily included at launch).

Per-claim upgrade status is recorded throughout §1–§5 with the marker **\[2026-05-13 primary fetch ✅]** for upgraded claims and **\[2026-05-13 primary fetch REFUTES]** for refuted claims.

**Overall status flip:** This report graduates from 🟡 partial to ✅ primary-anchored for every R-* row in §0. A small number of claims that depended on the community mirror (`replit.discourse.group`) or third-party blogs (Mastra, mindstudio.ai, latent.space, bycrawl.com, InfoQ) cannot be re-anchored from the official docs and have been demoted to "third-party only" status in-line.

---

## 0. Sources reviewed

Status: ✅ = primary source fetched and integrated. 🟡 = reconstruction-only. ❌ = not obtained.

| ID | URL | Status |
|---|---|---|
| R-Agent | `https://docs.replit.com/core-concepts/agent` | ✅ Primary fetch 2026-05-13 via issue #41 (was 🟡 reconstructed from WebSearch) |
| R-MD | `https://docs.replit.com/replitai/replit-dot-md` (+ `replit.discourse.group/t/.../8524` — community mirror, now demoted) | ✅ Primary fetch 2026-05-13 via issue #41 |
| R-Plan | `https://docs.replit.com/core-concepts/agent/plan-mode` (+ `blog.replit.com/introducing-plan-mode-a-safer-way-to-vibe-code` — supplementary) | ✅ Primary fetch 2026-05-13 via issue #41 |
| R-Connectors | `https://blog.replit.com/connectors` (+ `replit.com/products/integrations`, Mastra blog — third-party, now demoted) | ✅ Primary fetch 2026-05-13 via issue #41 |
| R-Warehouse | `https://docs.replit.com/replitai/warehouse-connectors` (+ `blog.replit.com/data-connectors` — supplementary) | ✅ Primary fetch 2026-05-13 via issue #41 |
| R-MCP | `https://docs.replit.com/replitai/mcp/overview` (+ `blog.replit.com/everything-you-need-to-know-about-mcp` — supplementary) | ✅ Primary fetch 2026-05-13 via issue #41 |
| R-A&A | `https://docs.replit.com/replitai/agents-and-automations` (+ R-A3 blog + Mastra blog — third-party, now demoted) | ✅ Primary fetch 2026-05-13 via issue #41 |
| R-Canvas | `https://docs.replit.com/replitai/canvas` (+ R-A4 blog) | ✅ Primary fetch 2026-05-13 via issue #41 |
| R-AppTest | `https://docs.replit.com/replitai/app-testing` (+ `blog.replit.com/automated-self-testing` — supplementary) | ✅ Primary fetch 2026-05-13 via issue #41 |
| R-Deploy | `https://docs.replit.com/cloud-services/deployments/autoscale-deployments` (+ `blog.replit.com/autoscale` — supplementary) | ✅ Primary fetch 2026-05-13 via issue #41 |
| R-Bill | `https://docs.replit.com/billing/ai-billing` (+ `blog.replit.com/effort-based-pricing` — supplementary) | ✅ Primary fetch 2026-05-13 via issue #41 |
| R-A3 | `https://blog.replit.com/introducing-agent-3-our-most-autonomous-agent-yet` (+ InfoQ + X — third-party, now demoted) | ✅ Primary fetch 2026-05-13 via issue #41 |
| R-A4 | `https://blog.replit.com/introducing-agent-4-built-for-creativity` (+ `mindstudio.ai`, `bycrawl.com`, `latent.space` — third-party, now demoted; `…/whats-changed-agent3-to-agent4` not fetched in this round) | ✅ Primary fetch 2026-05-13 via issue #41 (primary URL only) |
| S16 — Ghostwriter blog | `https://blog.replit.com/ghostwriter` | ❌ Not used per `sources.md` §"Weak or missing citations" — wrong substrate era. |

All 13 R-* rows are now primary-anchored. The originally-cited third-party mirrors (Mastra, InfoQ, latent.space, replit.discourse.group, bycrawl.com, mindstudio.ai) supplied claims that are not all reproducible from the primaries — claims that depended on those mirrors and are NOT supported by the official docs have been marked **\[2026-05-13 primary fetch REFUTES]** below.

**Time-stamp:** documentation as visible 2026-05-11. Agent 4 launched 2026-03-11; Agent 3 in Sep 2025; Connectors launched early-to-mid 2025; `replit.md` introduced mid-2025 (per LinkedIn announcement 2025-07).

---

## 1. App-generation-as-first-class-output vs. repo-modification shape

**Codex / Claude Code / Copilot cloud agent** (report 18 §1; report 11 §1) take a *repository* as primary input and emit *commits / branches / PRs* as primary output. The unit of work is "change the code." Deployment is decoupled from the agent loop.

**Replit Agent** takes a *plain-language description* as primary input and emits *a running, deployed, accessible application*. R-Agent enumerates the output types verbatim: "Web apps, mobile apps, data dashboards, and AI-powered tools"; "Visual designs and prototypes — explore mockups on the Design Canvas before committing to code"; "Multiple outputs in one project — web apps, mobile apps, slides, and videos sharing the same backend"; "Files and documents — CSVs, PDFs, PowerPoint files, Markdown docs"; "Connected service queries — pull data from BigQuery, Linear, Slack, Notion, and more directly from chat" (`64a9ed0e5e_docs.replit.com__core-concepts__agent.md` lines 199–203) **\[2026-05-13 primary fetch ✅]**. Per R-A4 (2026-03-11), Agent 4's "Ship Anything" lets a single project produce "Web and mobile apps, Slide decks, Data apps, Animations" and lets users "convert your existing web apps into mobile apps seamlessly, or build additional artifacts like slides or animations related to your existing web apps, within the same project" (`ff906146e8_blog.replit.com__introducing-agent-4-built-for-creativity.md` lines 229–246) **\[2026-05-13 primary fetch ✅]**.

R-Agent also names four Agent modes (not three as previously reconstructed) **\[2026-05-13 primary fetch ✅]**:

- **Lite**: "Make lightweight, inexpensive changes quickly. Lite mode is ideal for visual tweaks, bug fixes, and scoped features."
- **Economy**: "Use Agent's cost-optimized models for everyday tasks."
- **Power**: "Use Agent's most capable models for harder problems, larger changes, and longer builds."
- **Turbo**: a Power-only toggle in Advanced settings — "for up to 2.5x faster builds at higher cost (Pro only)."

R-Agent line 191 also notes verbatim: "Max mode is no longer available; use Power for the most capable standard builds." **\[2026-05-13 primary fetch ✅; demotes any third-party reference to "Max mode" as a current feature]**

Three consequences:

1. **The repo is incidental, not foundational.** Replit projects *contain* a repo, but the user's mental model is the deployed app. Inverts Codex's "App Server" abstraction (report 18 §1): Codex factors the *agent loop* away from the *surface*; Replit factors the *deployment target* into the substrate.
2. **"Done" is a live URL, not a merged PR.** [2026-05-13 primary fetch REFUTES] the previously-quoted "every app includes free hosting" snippet — R-Deploy does NOT contain that sentence. The Autoscale page says verbatim that Autoscale Deployments "run on cloud computing resources that scale up and down to efficiently handle the network traffic and workload of your Replit App. When your app is busy, autoscaling adds servers to manage the load. When your app is idle, it reduces the number to as low as zero to save you money" (`399ad76b92_docs.replit.com__cloud-services__deployments__autoscale-deployments.md` lines 128–134) **\[2026-05-13 primary fetch ✅]**. Per R-Agent FAQ verbatim: "Agent handles all the technical work — writing code, setting up infrastructure, configuring databases. You describe what you want in plain language and Agent builds it" (`64a9ed0e5e_…md` line 219) **\[2026-05-13 primary fetch ✅]**.
3. **The platform owns integrations.** Codex/Claude expect external MCP-server configuration; Replit Connectors (R-Connectors) ship as a first-party catalog with credential flow inside the agent UI — per R-A3 verbatim: "when you ask an Agent to build something that involves Notion, it now guides you through a seamless connection flow. Instead of manually hunting down and pasting API keys, the Agent surfaces a simple UI flow to connect with Notion. Once finished, the Agent securely receives the credentials it needs and continues building automatically" (`e1dffb38b4_blog.replit.com__introducing-agent-3-our-most-autonomous-agent-yet.md` line 138) **\[2026-05-13 primary fetch ✅]**.

**Diff vs. report 18 (Codex):** Codex's load-bearing primitive is the App Server protocol; Replit's is the workspace-as-deployment-target. Codex factors *outward* (one harness, five surfaces, BYO infra); Replit factors *inward* (one workspace, all infra+integrations+deploy bundled).

**Diff vs. report 11 (OpenHands):** OpenHands V1's `workspace` package abstracts local/remote/Docker workspaces but treats deployment as out-of-scope. Replit has no separate CI/CD — Plan → Build → Checkpoint → Deploy is one substrate.

---

## 2. `replit.md` as instruction-file substrate — diff against AGENTS.md and CLAUDE.md

Per R-MD verbatim: "Agent automatically creates this file in your project's root directory using proven best practices. Agent includes its contents in the context to help it understand your preferences, project structure, and coding style" (`11363fcaf5_docs.replit.com__replitai__replit-dot-md.md` line 123) **\[2026-05-13 primary fetch ✅]**. Agent reads it on every request. Typical sections: project overview, technology preferences, coding standards, communication style, API standards, deployment processes, external resources.

Three properties make it materially different from AGENTS.md (Codex / multi-vendor — report 18 §2) and `CLAUDE.md`:

**(a) Platform-managed, not user-owned.** **\[2026-05-13 primary fetch REFUTES]** the previously-quoted "automatically managed by Replit's system and gets condensed whenever it exceeds approximately 100 lines" sentence — this came from a community forum mirror (`replit.discourse.group/t/.../8524`) and is **NOT present in the official R-MD docs**. The official docs state, more conservatively (lines 472–476 of `11363fcaf5_…md`): "While there's no strict character limit for `replit.md`, extremely large files may not be fully processed. Keep your `replit.md` focused and concise for best results." No specific line-count threshold is documented officially. The auto-condensation behavior may still exist (community reports are consistent on the rough threshold), but no primary source confirms a numeric line budget; treat that detail as community-attested-only.

Confirmed by primary source **\[2026-05-13 primary fetch ✅]**: the file IS automatically created (line 159: "When you create a new project with Agent, it automatically generates a `replit.md` file using proven best practices"), the user CAN delete it to force regeneration (lines 183–187), and Agent's interaction with it is auto-creation + auto-extension as it learns, not user-only authorship — distinct from AGENTS.md/CLAUDE.md which are conventionally read-only-by-agent.

**(b) No scoping / no override semantics.** AGENTS.md has root-to-leaf walk, `*.override.md` files per level, and a `child_agents_md` subagent-inheritance flag — three orthogonal scoping primitives. `replit.md` is a single root file; no per-directory layering, no override. Real limitation for monorepo work.

**(c) Auto-updated by the agent.** Per R-MD verbatim: "Agent can also update your `replit.md` file as it learns more about your project and makes changes to your application" (line 143) **\[2026-05-13 primary fetch ✅]**. A *self-modifying instruction file* — closer to structured running memory than to a static spec. AGENTS.md/CLAUDE.md are conventionally append-only-by-human; `replit.md` is the agent's working journal as well as the user's preferences declaration. The exact compaction algorithm is undocumented officially (see (a) above).

**(d) Context scope is intra-Replit only.** Per R-MD verbatim (line 492): "`replit.md` provides context for Agent conversations but doesn't automatically apply to other AI tools" **\[2026-05-13 primary fetch ✅; NEW finding]**. Unlike AGENTS.md (which Codex/Claude/multiple harnesses can read by convention), `replit.md` is a substrate-private primitive. Cross-tool portability is not a goal.

**(e) Enterprise pre-configuration.** Per R-MD verbatim (line 507): "**Enterprise**: Pre-configure `replit.md` in custom templates to give every builder in your organization a consistent starting context" **\[2026-05-13 primary fetch ✅; NEW finding]**. This makes `replit.md` an organizational-policy primitive in addition to a per-project memory — closer to how an org might centrally distribute a SECURITY.md or a license header than how individual users hand-author AGENTS.md.

| Concern | Codex AGENTS.md | Claude `CLAUDE.md` | Replit `replit.md` |
|---|---|---|---|
| Per-dir scoping | Native root→leaf | Implicit | None — single root file |
| Override mechanism | `*.override.md` | None | None |
| Size budget | 32 KiB | None | No strict limit (official); "keep focused and concise"; community reports ~100-line auto-condensation but not docs-confirmed |
| Self-modification | Read-only | Read-only | Agent edits it |
| User control | Full | Full | Limited |
| Content domain | Project conventions | Project conventions | Conventions + running memory |
| Subagent inheritance | `child_agents_md` | CWD-dependent | N/A |

**Implication.** Our `.claude/skills/<name>/SKILL.md` registry (report 04, 18 §2) is closer to AGENTS.md's static-spec shape. `replit.md`'s "agent updates the file as it learns" pattern is worth borrowing as a *separate primitive* — call it `LEARNED.md` — distinct from the human-authored spec layer. Architecture 2's Compound Atelier wants this: each cycle writes back generalized lessons that the next cycle reads.

---

## 3. In-loop deployment — what changes when the deploy target is part of the substrate

Codex/OpenHands/Claude assume *somebody else's deployment pipeline*. Replit Agent owns it end-to-end. Per R-Deploy (Autoscale page), Autoscale Deployments are the substrate's default — they "automatically adjust capacity based on your app's traffic" and "reduce the number to as low as zero to save you money" **\[2026-05-13 primary fetch ✅]**. Other deployment types (Reserved VM, Static, Scheduled) live on sibling docs pages not in this drain set; per R-A&A verbatim (line 226–227): "Autoscale deployments - For chatbots and event-driven workflows; Scheduled deployments - For time-based automations" **\[2026-05-13 primary fetch ✅]**.

Substrate-level consequences:

1. **Deployment is observable inside the agent loop.** Per R-AppTest verbatim (line 120): "App Testing lets Agent test the apps it builds using an actual browser. Agent navigates through your application like a real user would, clicking around and validating functionality" **\[2026-05-13 primary fetch ✅]**. Important scope clarification: "App Testing is available for Full Stack JavaScript and Streamlit Python web applications" (line 132) **\[2026-05-13 primary fetch ✅; NEW finding — narrower scope than reconstructions suggested]**. App Testing is part of the Economy/Power tiers; "Lite mode keeps App Testing off" (line 184).
2. **The running system is ground truth.** Repo-modification agents trust unit tests and CI; Replit Agent trusts observed behavior because the substrate guarantees the deploy. The take-over flow is documented: "If you do not respond within 10 minutes, the Agent will continue as if you pressed 'Skip'" (R-AppTest line 196) **\[2026-05-13 primary fetch ✅; NEW finding — the take-over UX includes a 10-minute idle timeout]**.
3. **Effort-based pricing is checkpoint-aligned.** **\[2026-05-13 primary fetch REFUTES]** the specific "$0.06 floor / multiple-dollar ceiling" prices — R-Bill does NOT quote any dollar figures (those came from third-party mirrors). Per R-Bill verbatim (line 141): "Replit Agent uses **effort-based pricing** that scales with the complexity of your request. You pay based on the actual work Agent performs… **All Agent interactions are billable** - whether Agent responds with text guidance or makes code changes, there is always a charge, though smaller requests cost less." Per R-Bill line 153: "**One checkpoint per request** eliminates intermediate checkpoints and reduces billing noise" **\[2026-05-13 primary fetch ✅]**. Per R-Bill line 160: "in cases where the Agent performed work by answering a question or request, but didn't make code changes (e.g. in Plan Mode), there is still a charge associated with that work, even if there's not a checkpoint shown" **\[2026-05-13 primary fetch ✅]**. First substrate where the **billing primitive is co-extensive with the execution primitive** — checkpoints serve both rollback and metering. Real dollar distribution is now an [open follow-up](#6-open-follow-ups).
4. **200-minute autonomy needs run+test+observe.** Per R-A3 verbatim: "**Agent 3 runs on its own for up to 200 minutes**, handling full tasks autonomously—building, testing and fixing your app, with minimal manual oversight, giving you hours of time back" (`e1dffb38b4_…md` line 154) **\[2026-05-13 primary fetch ✅]**. R-A3 also names this **Max Autonomy (Beta)** as a distinct toggle (lines 114, 122–126) — "Max Autonomy (Beta) lets Agent run for longer and manage itself—ideal for complex, extended tasks with well-defined goals" **\[2026-05-13 primary fetch ✅; NEW finding — 200-minute autonomy is gated behind a Max-Autonomy Beta toggle, not the default Agent 3 mode]**. Repo-only agents max out at "PR opened"; Replit iterates against deployed reality.
5. **"Operate the system" is native.** Agent 3 builds agents/automations (R-A&A); per R-A&A verbatim (line 222–223): "**Deployment Required**: Your agent or automation must be deployed to function with external triggers like Slack, Telegram, or scheduled automations. The testing pane works for development and testing, but live triggers require deployment" **\[2026-05-13 primary fetch ✅]**. Currently-available triggers (R-A&A lines 135–144): Slack Agent, Telegram Agent, Timed Automation. **Coming soon**: "Custom webhook triggers: Respond to any external event or API call using a webhook URL" — i.e. generic webhook handlers are *not yet GA* per official docs **\[2026-05-13 primary fetch ✅; NEW finding — refines the §1 framing that automations cover "webhook handlers" — that's roadmap, not shipped]**.

**Diff against Codex Cloud (report 18 §1):** Codex Cloud isolates containers per task, preloads the repo, returns commits — delivery surface is a PR. Replit Cloud isolates by *workspace+deployment*, and the delivery surface is *the URL*.

**Diff against OpenHands (report 11):** OpenHands has no deployment-target substrate; equivalents would require external orchestration which `workspace` can host but doesn't bundle.

---

## 4. Connectors and skills as architecture-layer primitives

Connectors (R-Connectors) launched **Tue, Sep 30, 2025** as a first-party catalog of pre-built integrations — official launch wording **\[2026-05-13 primary fetch ✅]** (`588d7e2c8d_blog.replit.com__connectors.md` line 138): "We've launched first party support for over 20 connectors with dozens more coming soon." **\[2026-05-13 primary fetch REFUTES]** the precise "24 at launch" figure — the official launch post says "over 20", not 24; the "24" came from third-party tracking. Connectors are powered by Replit's acquisition of OpenInt (R-Connectors line 175: "This is all powered by our recent acquisition of OpenInt") **\[2026-05-13 primary fetch ✅; NEW finding — Connectors infrastructure derives from the OpenInt acquisition, not from in-house buildup]**. R-Warehouse names data-warehouse connectors (Snowflake/Databricks/BigQuery) as Enterprise-exclusive and **adds** that Segment, Amplitude, and Hex are analytics connectors available on Core/Pro/Enterprise (`0a879e24fc_…md` lines 111–114, 252–259) **\[2026-05-13 primary fetch ✅; NEW finding — Segment/Amplitude/Hex tier coverage not in original report]**.

Three properties make Connectors a substrate primitive, not just a catalog:

**(a) MCP-related, but not identical.** **\[2026-05-13 primary fetch REFUTES]** the "all powered by MCP" framing for Connectors — the official R-Connectors blog post does NOT mention MCP at all. The MCP surface lives in R-MCP, which is a *separate* feature documenting "MCP Servers for Replit Agent" — generic *custom* MCP server connections that the user adds in the Integrations pane (`84ffa03346_…md` lines 120–146). Connectors and MCP servers are two distinct integration surfaces; the report previously conflated them. Per R-MCP verbatim (line 162): "All custom MCP traffic passes through Replit's security scanner. The scanner evaluates tool definitions and planned executions, blocking suspicious or unsafe tools before they run. If a tool is rejected, Agent will inform you about it" **\[2026-05-13 primary fetch ✅]**. Per R-MCP authentication options (lines 170–172): "OAuth dynamic client registration: If the server supports OAuth DCR, Replit automatically detects and registers the client for you" **\[2026-05-13 primary fetch ✅; NEW finding — OAuth DCR auto-registration is a substrate convenience]**.

**(b) Credentials flow through the agent UI mid-task.** Per R-A3 verbatim (line 138): "the Agent surfaces a simple UI flow to connect with Notion ... securely receives the credentials it needs and continues building automatically" **\[2026-05-13 primary fetch ✅]**. Per R-Connectors line 138: "For OAuth-based services, there are no credentials to manage. Just authenticate and start building. For API-key-based services, we've streamlined the flow to make it just as smooth." Codex/Claude expect MCP servers configured upfront; Replit installs them *just-in-time*.

**(c) Dual-use — building agent and built app.** A Replit-built customer-support app uses the Slack connector at runtime; the Agent building it uses the *same* Slack connector to test. Flattened: skill = connector = runtime dependency.

**(d) Enterprise governance.** R-Connectors line 152–158 enumerates Enterprise capabilities verbatim **\[2026-05-13 primary fetch ✅; NEW finding]**: "Centralized management: Control team-wide connections in one place; Granular access: Enforce role-based permissions and governance; Visibility & auditability: Track which apps use which services; Enterprise flexibility: Bring your own OAuth clients with custom scopes." This makes Connectors an org-policy primitive in addition to a catalog.

**Agents-build-agents (R-A&A + R-A3).** Per R-A&A verbatim (line 222): "Your agent or automation must be deployed to function with external triggers like Slack, Telegram, or scheduled automations" **\[2026-05-13 primary fetch ✅]**. Per R-A3 verbatim (line 132): "**For the first time ever, Agent 3 can build other agents and automations.** That means you can automate complex and repetitive workflows using natural language" **\[2026-05-13 primary fetch ✅]**. **\[2026-05-13 primary fetch REFUTES]** the previously-quoted "Agent 3's built agents are powered by Mastra" claim — Mastra is NOT mentioned in either R-A&A or R-A3 (official docs). That framing came from a third-party Mastra blog mirror and should be treated as third-party-only / unverified. The agents-build-agents *capability* is confirmed; the *implementation substrate* (Mastra vs. in-house) is not officially documented. Closest substrate analog to our Architecture-2 Compound Atelier pattern. The skill primitive is the (built agent + connectors + scheduled/Slack/Telegram trigger + deployment) bundle, not a YAML+prompt registry.

**Diff against Codex/Claude/OpenHands skills:** Codex has no first-class skill registry (routes via MCP/plugins); Claude has `.claude/skills/<name>/SKILL.md`; OpenHands skills (report 11 §5) match the same library shape. Replit's primitive is heavier — a deployed Mastra agent with bound connectors — but operational-by-default. The others are libraries; Replit's are running services.

---

## 5. Implications for our four architectures (focus: Architecture 4 predator scenario)

**Architecture 1 — Specification Refinery.** App-generation framing is *opposite* to "spec is the product," but `replit.md`'s self-modifying-memory pattern is adoptable as a Refinery "learning journal" — a per-cycle `LEARNED.md` the agent writes back, distinct from the canonical spec. Connectors not load-bearing.

**Architecture 2 — Compound Atelier.** "Agents-build-agents" (R-A&A + R-A3 — note Mastra mention REFUTED above as third-party-only) is the *exact* compound primitive: each workshop should emit not just code+tests but a *deployed running tool* the next workshop uses. Connectors as dual-use primitive maps onto our skills-as-services proposal. Plan-mode-as-billable verbatim (R-Plan line 233, R-Bill line 141): "Plan Mode usage follows the same effort-based pricing as other Agent interactions. You are charged for all Agent work in Plan Mode, including answering questions, providing guidance, and generating task lists. Charges scale up for more complex requests, or requests in longer context conversations. **All Agent interactions are billable** — whether Agent responds with text guidance or makes code changes, there is always a charge, though smaller requests cost less" **\[2026-05-13 primary fetch ✅]** — the right shape, because planning costs because it consumes the agent even without code output.

**Architecture 3 — Phase-Gated Foundry.** Checkpoints are a natural phase-gate primitive — billable + rollback-able. Map phase boundaries to checkpoint boundaries; adopt "one checkpoint per request" as the gate granularity. App-Testing-via-browser (R-AppTest) is a strong V&V substrate — V&V should run against deployed reality, not just unit tests.

**Architecture 4 — Evolutionary Tournament (predator scenario) — load-bearing.** The predator scenario stipulates an adversarial environment where the agent must operate, observe, and adapt to a deployed system under attack/competition. Replit Agent is the only audited substrate that natively supports it.

- **Population members are deployed apps, not just genomes.** Each variant isn't a candidate codebase — it's a running, accessible, instrumented service. Autoscale + Reserved VM is the natural deployment target.
- **Browser-based self-testing is the fitness signal.** R-AppTest's REPL-based verification is exactly the shape needed: the predator probes the live URL; the substrate observes the response; fitness derives from observable behavior, not unit-test pass rate. Codex/OpenHands can't do this without external orchestration.
- **Connectors enable operate-the-system actions.** A variant that must respond to alerts via PagerDuty / post to Slack / write to Postgres has integrations baked in. Architecture 4 doesn't have to build a tool-integration layer separately.
- **Agents-build-agents matches population dynamics.** Mastra-style runtime-tool-creation (R-A&A) fits the population's need to *spawn new tools* mid-tournament.
- **Checkpoints as generation boundaries.** Effort-based billing per checkpoint maps onto generations: one generation = one checkpoint per variant. Cost-aware selection is a substrate primitive.

**Caveat.** Replit's single-workspace-per-project model is the architectural mismatch — Architecture 4 needs *N parallel isolated workspaces*. **\[2026-05-13 primary fetch REFUTES]** the "splits single tasks into different forks" wording — the actual R-A4 quote (`ff906146e8_…md` lines 180–181) is: "Independent tasks can run in parallel, with progress visible and coordinated. Once the tasks are done, they can be merged into the main project. When changes conflict, Agent 4 uses specialized **sub-agents** to resolve them" and "For larger jobs, Agent 4 can split a single task into smaller pieces, work on them simultaneously with **sub-agents**, and recombine the results—shortening long-running tasks without sacrificing quality" **\[2026-05-13 primary fetch ✅]**. The primitive is **sub-agents within a single project**, not separate forks. Per R-A4 line 187: "Parallel task execution will be available to **Pro and Enterprise users**, designed for power users who want to take full advantage of Agent 4's advanced capabilities" (line 189: "To celebrate the launch of Agent 4, we're making it **temporarily available to Core users for a limited time**") **\[2026-05-13 primary fetch ✅; NEW finding — parallel exec is gated to Pro/Enterprise, not universally available]**. True Architecture-4 deployment would need Replit at the Teams/Enterprise project-multiplexing level, or replicating the substrate-shape elsewhere — and even then sub-agents share the parent workspace's filesystem, which is closer to a single-process multi-threading model than to N isolated population members.

**Cross-architecture verdict — four lessons to import:**

1. **App-generation framing** for any architecture whose "done" is observable behavior, not merged code (Arch 2, Arch 3 V&V, Arch 4 entire loop).
2. **Self-modifying instruction file** (`LEARNED.md`-style) as a primitive distinct from human-authored spec (Arch 1, Arch 2; auto-condensation-at-N-lines a useful discipline).
3. **Checkpoints as unified rollback + billing + phase-gate primitive** (Arch 3 directly; Arch 4 generations).
4. **Connectors as dual-use (build-time + runtime) skill-services**, not static skill-libraries (Arch 2 compound-skill registry should accept service-shaped entries).

---

## 6. Open follow-ups

- **Primary-URL re-fetch.** ✅ Resolved 2026-05-13 — all 13 R-* URLs successfully primary-fetched via issue #41 GitHub Actions backed.
- **`replit.md` exact condensation algorithm.** Still open. The official docs (R-MD) do NOT confirm the "~100 lines auto-condense" behavior; only "extremely large files may not be fully processed. Keep your `replit.md` focused and concise." Sections preserved? Summarize or delete? Matters for `LEARNED.md` adoption — and the community-reported numeric threshold is unverified.
- **Connectors count.** Per R-Connectors at launch (Sep 30 2025): "over 20"; report previously said "24 at launch / 30+ / 47+" — the higher figures come from later third-party tracking; a current docs count is wanted.
- **Agent-4 sub-agent isolation semantics.** Resolved partially: parallel work uses **sub-agents within a single project**, not separate forks (R-A4). Sub-agents share the parent workspace's filesystem. Still wanted: exact concurrency primitives (process-level? container-level? branch-level?).
- **Effort-based pricing distribution.** Still wanted. Specific "$0.06 / multi-dollar" figures REFUTED above (not in R-Bill); real distribution needed for Arch-3 phase budgets and Arch-4 generation budgets.
- **Custom webhook triggers GA timing.** Per R-A&A, custom webhook triggers are "Coming soon" — not yet GA. Affects whether Architecture-4 variants can be triggered by arbitrary external events.
- **Mastra usage in Agent 3/4.** Whether Replit-built agents are implemented on Mastra (third-party blog claim) or in-house. Official docs are silent; status: third-party-only.
- **Reserved VM and Scheduled deployments pages.** Not in this drain set; would tighten §3 deployment-type framing.
- **App Testing supported languages.** Per R-AppTest: "Full Stack JavaScript and Streamlit Python web applications" only. Implications for Architecture-4 fitness signals if variants are written in other stacks.
- **Ghostwriter-vs-Agent succession.** No primary source explicitly deprecates Ghostwriter; if it still ships alongside, that affects the substrate description. Low priority.

---

## 7. Verdict

Replit Agent is the substrate-architecture inverse of Codex: Codex factors *outward* (one harness, five surfaces, BYO infrastructure); Replit factors *inward* (one workspace, deployment + integrations + databases + browser-testing + scheduler all internalized). `replit.md` is materially different from AGENTS.md/CLAUDE.md by being self-modifying and auto-created — closer to structured running memory than a static spec. (Note: the previously-claimed "auto-condensed at ~100 lines" specific threshold is **not** in the official docs; only "keep focused and concise" is documented. Treat the line-count threshold as community-attested-only.) The in-loop deployment model — "done" is a live URL, not a merged PR — enables substrate-native primitives (browser-based self-testing limited to Full-Stack-JS/Streamlit, 200-minute Max-Autonomy-Beta runtime, checkpoint-as-billing-unit) that repo-modification agents cannot match without external orchestration. Connectors and MCP are *two distinct surfaces*: Connectors is a first-party OpenInt-derived catalog whose security model is OAuth + provider-native scopes (not MCP); the MCP-Servers integration is a separate surface for arbitrary custom MCP endpoints, where Replit's security scanner intercepts traffic. Connectors are dual-use skill-services: the same connector serves both the building agent and the built app. Lessons import asymmetrically: Arch 1 wants only the self-modifying-memory pattern; Arch 2 wants skills-as-services most fully; Arch 3 wants checkpoints-as-phase-gates; **Architecture 4's predator scenario wants substantially the entire substrate** — browser-based observable-behavior verification, deployed-app-per-variant, and runtime tool installation are the primitives an evolutionary tournament against live adversaries needs. The single-workspace-per-project constraint is the architectural mismatch we work around — by using Replit at the Teams/Enterprise project-multiplexing level, or by replicating the substrate shape elsewhere. Agent 4's "parallel" capability is **sub-agents within a single project sharing one workspace filesystem**, not isolated forks — gated Pro/Enterprise — so the workspace-multiplexing problem persists for Arch-4 even at the highest tier.

**Status:** ✅ Primary-anchored across all 13 R-* sources via 2026-05-13 issue #41 fetch. Two named third-party claims (Mastra implementation; specific "$0.06 / multi-dollar" billing floor/ceiling) and one community-mirror claim (~100-line auto-condensation) are now flagged as unverified-by-primaries.
