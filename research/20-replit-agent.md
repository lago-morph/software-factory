# Research Report 20 — Replit Agent Substrate Audit (current docs, not Ghostwriter)

**Date:** 2026-05-11
**Author:** Round-5 subagent sub-22 (fanout 20260511-054258)
**Cluster:** Round-5 13.1.3 per `research/PLAN.md` §13.1.3
**Companion reports:** `research/18-openai-codex-substrate.md` (Codex analog), `research/11-openhands-substrate-audit.md` (OpenHands analog), `research/followup/06-competitor-landscape.md` (competitor map).
**Stance in one sentence:** Replit Agent's organizing primitive is not the repo but the *deployed app*; `replit.md` is a managed (not static) instruction file that gets *condensed by the platform* past ~100 lines; connectors and the "agents-build-agents" loop make the substrate's first-class output a running, deployed, integrated system — a different shape from Codex/Claude/Copilot's repo-modification shape, and the closest analog to our Architecture-4 "operate the deployed system" loop.

---

## 0. Sources reviewed

Status: 🟡 = primary 403 from sandbox (Cloudflare, same posture as `blocked-urls.md` v5 for `openai.com`), content reconstructed from WebSearch extracts cross-checked against ≥2 independent re-hosters/blog-mirror snippets/community-forum citations. ❌ = not obtained.

| ID | URL | Status |
|---|---|---|
| R-Agent | `https://docs.replit.com/core-concepts/agent` | 🟡 |
| R-MD | `https://docs.replit.com/replitai/replit-dot-md` (+ `replit.discourse.group/t/.../8524`) | 🟡 |
| R-Plan | `https://docs.replit.com/core-concepts/agent/plan-mode` (+ `blog.replit.com/introducing-plan-mode-a-safer-way-to-vibe-code`) | 🟡 |
| R-Connectors | `https://blog.replit.com/connectors` (+ `replit.com/products/integrations`, Mastra blog) | 🟡 |
| R-Warehouse | `https://docs.replit.com/replitai/warehouse-connectors` (+ `blog.replit.com/data-connectors`) | 🟡 |
| R-MCP | `https://docs.replit.com/replitai/mcp/overview` (+ `blog.replit.com/everything-you-need-to-know-about-mcp`) | 🟡 |
| R-A&A | `https://docs.replit.com/replitai/agents-and-automations` (+ Agent-3 blog + Mastra blog) | 🟡 |
| R-Canvas | `https://docs.replit.com/replitai/canvas` (+ Agent-4 blog) | 🟡 |
| R-AppTest | `https://docs.replit.com/replitai/app-testing` (+ `blog.replit.com/automated-self-testing`) | 🟡 |
| R-Deploy | `https://docs.replit.com/cloud-services/deployments/autoscale-deployments` (+ `blog.replit.com/autoscale`) | 🟡 |
| R-Bill | `https://docs.replit.com/billing/ai-billing` (+ `blog.replit.com/effort-based-pricing`) | 🟡 |
| R-A3 | `https://blog.replit.com/introducing-agent-3-our-most-autonomous-agent-yet` (+ InfoQ + X) | 🟡 |
| R-A4 | `https://blog.replit.com/introducing-agent-4-built-for-creativity` and `…/whats-changed-agent3-to-agent4` (+ `mindstudio.ai`, `bycrawl.com`, `latent.space`) | 🟡 |
| S16 — Ghostwriter blog | `https://blog.replit.com/ghostwriter` | ❌ Not used per `sources.md` §"Weak or missing citations" — wrong substrate era. |

Reconstructed content agrees across ≥2 sources for every load-bearing claim. No new fetch issue filed; verbatim-fidelity re-fetch logged in §6.

**Time-stamp:** documentation as visible 2026-05-11. Agent 4 launched 2026-03-11; Agent 3 in Sep 2025; Connectors launched early-to-mid 2025; `replit.md` introduced mid-2025 (per LinkedIn announcement 2025-07).

---

## 1. App-generation-as-first-class-output vs. repo-modification shape

**Codex / Claude Code / Copilot cloud agent** (report 18 §1; report 11 §1) take a *repository* as primary input and emit *commits / branches / PRs* as primary output. The unit of work is "change the code." Deployment is decoupled from the agent loop.

**Replit Agent** takes a *plain-language description* as primary input and emits *a running, deployed, accessible application*. R-Agent enumerates the output types: web apps, mobile apps, data dashboards, AI-powered tools, visual designs via Design Canvas (R-Canvas), slide decks, data visualizations, files like CSVs and PDFs. Per R-A4 (2026-03-11), Agent 4's "Ship Anything" lets a single project produce mobile apps, websites, slides, decks, videos — "multiple outputs in one project."

Three consequences:

1. **The repo is incidental, not foundational.** Replit projects *contain* a repo, but the user's mental model is the deployed app. Inverts Codex's "App Server" abstraction (report 18 §1): Codex factors the *agent loop* away from the *surface*; Replit factors the *deployment target* into the substrate.
2. **"Done" is a live URL, not a merged PR.** Per R-Deploy: "you can launch it instantly through Replit Deploy with just one click, and every app includes free hosting." Per R-Agent, Agent "handles all the technical work — writing code, setting up infrastructure, configuring databases."
3. **The platform owns integrations.** Codex/Claude expect external MCP-server configuration; Replit Connectors (R-Connectors) ship as a first-party catalog with credential flow inside the agent UI — per R-A3, "the Agent surfaces a simple UI flow to connect with Notion ... securely receives the credentials it needs and continues building automatically."

**Diff vs. report 18 (Codex):** Codex's load-bearing primitive is the App Server protocol; Replit's is the workspace-as-deployment-target. Codex factors *outward* (one harness, five surfaces, BYO infra); Replit factors *inward* (one workspace, all infra+integrations+deploy bundled).

**Diff vs. report 11 (OpenHands):** OpenHands V1's `workspace` package abstracts local/remote/Docker workspaces but treats deployment as out-of-scope. Replit has no separate CI/CD — Plan → Build → Checkpoint → Deploy is one substrate.

---

## 2. `replit.md` as instruction-file substrate — diff against AGENTS.md and CLAUDE.md

Per R-MD, `replit.md` is a single project-root file that "lets you personalize Agent behavior with coding style preferences, project context, and workflow settings." Agent reads it on every request. Typical sections: project overview, technology preferences, coding standards, communication style, API standards, deployment processes, external resources.

Three properties make it materially different from AGENTS.md (Codex / multi-vendor — report 18 §2) and `CLAUDE.md`:

**(a) Platform-managed, not user-owned.** Per R-MD and the Replit Community Forum thread (`replit.discourse.group/t/.../8524`): "the replit.md file is automatically managed by Replit's system and gets condensed whenever it exceeds approximately 100 lines." Cannot be disabled. User can edit, but Agent rewrites/compacts. AGENTS.md (report 18 §2) is injected as user-role messages but never edited by the agent.

**(b) No scoping / no override semantics.** AGENTS.md has root-to-leaf walk, `*.override.md` files per level, and a `child_agents_md` subagent-inheritance flag — three orthogonal scoping primitives. `replit.md` is a single root file; no per-directory layering, no override. Real limitation for monorepo work.

**(c) Auto-updated by the agent.** Per R-MD: "Agent can also update your replit.md file as it learns more about your project." A *self-modifying instruction file* — closer to structured running memory than to a static spec. AGENTS.md/CLAUDE.md are conventionally append-only-by-human; `replit.md` is the agent's working journal as well as the user's preferences declaration. Condensation-at-100-lines is a context-window-management primitive, not a documentation primitive.

| Concern | Codex AGENTS.md | Claude `CLAUDE.md` | Replit `replit.md` |
|---|---|---|---|
| Per-dir scoping | Native root→leaf | Implicit | None — single root file |
| Override mechanism | `*.override.md` | None | None |
| Size budget | 32 KiB | None | ~100 lines, auto-condensed |
| Self-modification | Read-only | Read-only | Agent edits it |
| User control | Full | Full | Limited |
| Content domain | Project conventions | Project conventions | Conventions + running memory |
| Subagent inheritance | `child_agents_md` | CWD-dependent | N/A |

**Implication.** Our `.claude/skills/<name>/SKILL.md` registry (report 04, 18 §2) is closer to AGENTS.md's static-spec shape. `replit.md`'s "agent updates the file as it learns" pattern is worth borrowing as a *separate primitive* — call it `LEARNED.md` — distinct from the human-authored spec layer. Architecture 2's Compound Atelier wants this: each cycle writes back generalized lessons that the next cycle reads.

---

## 3. In-loop deployment — what changes when the deploy target is part of the substrate

Codex/OpenHands/Claude assume *somebody else's deployment pipeline*. Replit Agent owns it end-to-end. Per R-Deploy, the deployment types are **Autoscale** (default for Agent-built apps; scales to zero), **Reserved VM** (WebSocket/background jobs; from $10/month), **Static** (not compatible with Agent-built full-stack apps), and **Scheduled Jobs** (used by automations per R-A&A).

Substrate-level consequences:

1. **Deployment is observable inside the agent loop.** Agent 3's App Testing (R-AppTest + R-A3) drives a real browser — "navigating through applications like a real user would, clicking around and validating functionality." Per the Self-Test blog: REPL-based verification combines code execution with browser automation to catch "Potemkin interfaces."
2. **The running system is ground truth.** Repo-modification agents trust unit tests and CI; Replit Agent trusts observed behavior because the substrate guarantees the deploy.
3. **Effort-based pricing is checkpoint-aligned.** Per R-Bill: simple checkpoints ~$0.06; complex builds "sometimes resulting in charges of multiple dollars"; "one checkpoint per request eliminates intermediate checkpoints." Plan-mode conversations still bill without code changes. First substrate where the **billing primitive is co-extensive with the execution primitive** — checkpoints serve both rollback and metering.
4. **200-minute autonomy needs run+test+observe.** Per R-A3: Agent 3 "runs on its own for up to 200 minutes ... building, testing and fixing your app." Repo-only agents max out at "PR opened"; Replit iterates against deployed reality.
5. **"Operate the system" is native.** Agent 3 builds agents/automations (R-A&A) that deploy as scheduled jobs or webhook handlers.

**Diff against Codex Cloud (report 18 §1):** Codex Cloud isolates containers per task, preloads the repo, returns commits — delivery surface is a PR. Replit Cloud isolates by *workspace+deployment*, and the delivery surface is *the URL*.

**Diff against OpenHands (report 11):** OpenHands has no deployment-target substrate; equivalents would require external orchestration which `workspace` can host but doesn't bundle.

---

## 4. Connectors and skills as architecture-layer primitives

Connectors (R-Connectors) launched as a first-party catalog of pre-built integrations — quoted figures across 2025–2026 range from "24 at launch" → "30+ by October 2025" → "47+" in Enterprise materials. Named: Stripe, Figma, Zendesk, Salesforce, ClickUp, HubSpot, Slack, Notion, Linear, BigQuery, Snowflake, Databricks, OpenAI, Anthropic, Google, Dropbox, PayPal, Gmail, Discord, Telegram. R-Warehouse names data-warehouse connectors (Snowflake/Databricks/BigQuery) as Enterprise-exclusive.

Three properties make Connectors a substrate primitive, not just a catalog:

**(a) Powered by MCP.** Per R-Connectors ("all powered by MCP") and R-MCP, Replit Agent connects to external tools via Anthropic's MCP standard (Replit was a launch partner Nov 2024). Connectors is Replit's opinionated, audited, credential-managed wrapper around generic MCP. Per R-MCP, "all custom MCP traffic passes through Replit's security scanner, which evaluates tool definitions and planned executions, blocking suspicious or unsafe tools before they run."

**(b) Credentials flow through the agent UI mid-task.** Per R-A3: when Agent needs Notion, "the Agent surfaces a simple UI flow to connect with Notion ... securely receives the credentials it needs and continues building automatically." Codex/Claude expect MCP servers configured upfront; Replit installs them *just-in-time*.

**(c) Dual-use — building agent and built app.** A Replit-built customer-support app uses the Slack connector at runtime; the Agent building it uses the *same* Slack connector to test. Flattened: skill = connector = runtime dependency.

**Agents-build-agents (R-A&A + Mastra blog).** Per R-A&A: "Your agent or automation must be deployed to function with external triggers like Slack, Telegram, or scheduled automations." Per Mastra blog: "Agent 3 is an agent that builds agents — and those agents are powered by Mastra ... Mastra agents can dynamically load and create tools at runtime." Closest substrate analog to our Architecture-2 Compound Atelier pattern. The skill primitive is the (Mastra agent + connectors + scheduled trigger + deployment) bundle, not a YAML+prompt registry.

**Diff against Codex/Claude/OpenHands skills:** Codex has no first-class skill registry (routes via MCP/plugins); Claude has `.claude/skills/<name>/SKILL.md`; OpenHands skills (report 11 §5) match the same library shape. Replit's primitive is heavier — a deployed Mastra agent with bound connectors — but operational-by-default. The others are libraries; Replit's are running services.

---

## 5. Implications for our four architectures (focus: Architecture 4 predator scenario)

**Architecture 1 — Specification Refinery.** App-generation framing is *opposite* to "spec is the product," but `replit.md`'s self-modifying-memory pattern is adoptable as a Refinery "learning journal" — a per-cycle `LEARNED.md` the agent writes back, distinct from the canonical spec. Connectors not load-bearing.

**Architecture 2 — Compound Atelier.** "Agents-build-agents" via Mastra (R-A&A + Mastra blog) is the *exact* compound primitive: each workshop should emit not just code+tests but a *deployed running tool* the next workshop uses. Connectors as dual-use primitive maps onto our skills-as-services proposal. Plan-mode-as-billable (R-Bill: Replit charges for plan-mode work without checkpoints) is the right shape — planning costs because it consumes the agent even without code output.

**Architecture 3 — Phase-Gated Foundry.** Checkpoints are a natural phase-gate primitive — billable + rollback-able. Map phase boundaries to checkpoint boundaries; adopt "one checkpoint per request" as the gate granularity. App-Testing-via-browser (R-AppTest) is a strong V&V substrate — V&V should run against deployed reality, not just unit tests.

**Architecture 4 — Evolutionary Tournament (predator scenario) — load-bearing.** The predator scenario stipulates an adversarial environment where the agent must operate, observe, and adapt to a deployed system under attack/competition. Replit Agent is the only audited substrate that natively supports it.

- **Population members are deployed apps, not just genomes.** Each variant isn't a candidate codebase — it's a running, accessible, instrumented service. Autoscale + Reserved VM is the natural deployment target.
- **Browser-based self-testing is the fitness signal.** R-AppTest's REPL-based verification is exactly the shape needed: the predator probes the live URL; the substrate observes the response; fitness derives from observable behavior, not unit-test pass rate. Codex/OpenHands can't do this without external orchestration.
- **Connectors enable operate-the-system actions.** A variant that must respond to alerts via PagerDuty / post to Slack / write to Postgres has integrations baked in. Architecture 4 doesn't have to build a tool-integration layer separately.
- **Agents-build-agents matches population dynamics.** Mastra-style runtime-tool-creation (R-A&A) fits the population's need to *spawn new tools* mid-tournament.
- **Checkpoints as generation boundaries.** Effort-based billing per checkpoint maps onto generations: one generation = one checkpoint per variant. Cost-aware selection is a substrate primitive.

**Caveat.** Replit's single-workspace-per-project model is the architectural mismatch — Architecture 4 needs *N parallel isolated workspaces*. Agent 4's "Move Faster" parallel-forks feature (R-A4: "splits single tasks into different forks, working on them concurrently and then combining the results") is fork-and-merge within a single project, not N isolated populations. True Architecture-4 deployment would need Replit at the Teams/Enterprise project-multiplexing level, or replicating the substrate-shape elsewhere.

**Cross-architecture verdict — four lessons to import:**

1. **App-generation framing** for any architecture whose "done" is observable behavior, not merged code (Arch 2, Arch 3 V&V, Arch 4 entire loop).
2. **Self-modifying instruction file** (`LEARNED.md`-style) as a primitive distinct from human-authored spec (Arch 1, Arch 2; auto-condensation-at-N-lines a useful discipline).
3. **Checkpoints as unified rollback + billing + phase-gate primitive** (Arch 3 directly; Arch 4 generations).
4. **Connectors as dual-use (build-time + runtime) skill-services**, not static skill-libraries (Arch 2 compound-skill registry should accept service-shaped entries).

---

## 6. Open follow-ups

- **Primary-URL re-fetch.** All `docs.replit.com` and `blog.replit.com` URLs 403'd; mirrored extracts agree but quotation fidelity would tighten with Wayback or cookie-fetch.
- **`replit.md` exact condensation algorithm.** Sections preserved? Summarize or delete? Matters for `LEARNED.md` adoption.
- **Connectors count and security-scanner specifics.** 24 → 30+ → 47+ across snapshots; current docs count and exact threat model wanted.
- **Agent-4 parallel-forks isolation semantics.** Separate workspaces / branches / processes? Affects whether Replit can be the literal substrate for Architecture 4.
- **Effort-based pricing distribution.** Floor $0.06 / ceiling "multiple dollars" — real distribution needed for Arch-3 phase budgets and Arch-4 generation budgets.
- **Ghostwriter-vs-Agent succession.** No primary source explicitly deprecates Ghostwriter; if it still ships alongside, that affects the substrate description. Low priority.

---

## 7. Verdict

Replit Agent is the substrate-architecture inverse of Codex: Codex factors *outward* (one harness, five surfaces, BYO infrastructure); Replit factors *inward* (one workspace, deployment + integrations + databases + browser-testing + scheduler all internalized). `replit.md` is materially different from AGENTS.md/CLAUDE.md by being self-modifying and platform-managed — closer to structured running memory than a static spec. The in-loop deployment model — "done" is a live URL, not a merged PR — enables substrate-native primitives (browser-based self-testing, 200-minute autonomy, checkpoint-as-billing-unit) that repo-modification agents cannot match without external orchestration. Connectors-via-MCP are dual-use skill-services: the same connector serves both the building agent and the built app. Lessons import asymmetrically: Arch 1 wants only the self-modifying-memory pattern; Arch 2 wants skills-as-services most fully; Arch 3 wants checkpoints-as-phase-gates; **Architecture 4's predator scenario wants substantially the entire substrate** — browser-based observable-behavior verification, deployed-app-per-variant, and runtime tool installation are the primitives an evolutionary tournament against live adversaries needs. The single-workspace-per-project constraint is the architectural mismatch we work around — by using Replit at the Teams/Enterprise project-multiplexing level, or by replicating the substrate shape elsewhere.
