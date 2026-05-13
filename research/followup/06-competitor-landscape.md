# Round-3 Thread 6: Competitor Landscape

**Run:** fanout 20260511-054258 sub-09
**Date:** 2026-05-11
**Scope:** Five named competitors in the AI-coding-agent / software-factory space — Cognition's Devin, 8090 Solutions, Factory's Droid, Superconductor, and Jesse Vincent's Superpowers. Goal is to situate our four candidate architectures against shipping products by extracting each vendor's workflow primitives, human role, pricing model, and differentiator.

**Fetch notes.** Original fan-out (2026-05-11) hit Cloudflare 403s on every primary homepage and assembled findings from secondary sources (GitHub READMEs, Cognition's blog, docs.factory.ai, Latent.Space, independent reviews). Issue #31 (filed 2026-05-12, drained 2026-05-13) successfully fetched 6 of 9 targeted primary pages via the GitHub Actions fetch worker: Devin homepage and pricing page, Factory homepage, 8090 homepage, Jesse Vincent's "Superpowers" blog post, and a (wrong) superconductor.io. Three URLs returned HTTP 404 from the upstream and are not retryable as listed: `cognition.ai/blog/devin`, `factory.ai/product`, `8090.inc/blog` (see "Sources reviewed" for the corrected paths). As a result, four of the five competitor sections below (Devin, Factory, 8090, Superpowers) are now anchored to primary marketing/pricing/methodology pages. The Superconductor section remains secondary-sourced because the `.io` domain we fetched is a parked-for-sale domain on Atom.com — the live product is at `superconductor.com`, which was not in the issue #31 fetch list.

## Drain note (issue #31) — 2026-05-13

**Scope of update.** Folded 6 successfully-fetched primary pages from `research/fetched/issue-31/` into this report; refuted stale pricing and re-anchored positioning. 3 URLs failed with HTTP 404 (page does not exist at that path — *not* a sandbox/Cloudflare block); these were kept in the fetched tree as evidence and recorded in Sources Reviewed at ❌.

**Per-competitor upgrade summary.**

- **Devin (Cognition).** Pricing model entirely rewritten from primary `devin.ai/pricing`. The "ACU at ~$2.00–$2.25" framing and "$500 Team / 250 ACUs" tier we had — extracted from secondary explainers — does **not appear anywhere on the current pricing page.** Current published tiers are Free / Pro $20 / Max $200 / Teams $80 / Enterprise custom. Quotas are described generically as "Devin usage quota" with pay-as-you-go beyond quota; no ACU unit is named publicly. New product surface confirmed from homepage: "Devin for Terminal," Devin Review, DeepWiki, "Managed Devins" orchestration (Advanced Capabilities). Nubank case study (8–12× efficiency, 20× cost savings, ETL monolith migration) is the homepage hero.
- **Factory.** Homepage repositioning observed: tagline is **"Agent-Native Software Development"** and the safety pitch is now **"AI that will work with you, not replace you"** — softer than the earlier autonomy framing. Five surfaces enumerated: Terminal/IDE, Desktop/Web, CLI, Slack/Teams, Project Manager. New primitive surfaced in news rail: **Droid Computers** — persistent remote (or self-hosted) machines orchestrating Droids. Series C $150M @ $1.5B valuation confirmed on-page. Specification Mode is *not* on the homepage anymore — still in docs but no longer headline.
- **8090.** Homepage repositioned around **"AI is writing your software. Who's in control?"** — governance framing, not upstream-context framing. Two-product split confirmed and named: **Software Factory** (self-serve SDLC control plane at factory.8090.ai) and **8090 Enterprise** (custom-delivery, "designed, built, and hosted by us"). Three named pillars: **documentation, collaboration, oversight.** EY partnership ("Trusted by EY," Big Four) is new external validation. Chamath co-founder/CEO confirmed by direct quote on page.
- **Superconductor.** Not upgraded. The issue-31 URL `superconductor.io` resolves to an Atom.com domain-for-sale page — completely unrelated to the product. The actual company is `superconductor.com`. Section kept as previously reconstructed; new follow-up logged.
- **Superpowers (Jesse Vincent).** Origin post (`blog.fsck.com/2025/10/09/superpowers/`) now read in full as primary source. Major correction: the published workflow is the **three-phase "brainstorm → plan → implement"** loop, not the 7-step pipeline we reconstructed. The reconstructed steps were real but were *individual skills*, not the headline workflow shape. Install path corrected to Claude Code plugin marketplace (`/plugin marketplace add obra/superpowers-marketplace`; requires Claude Code 2.0.13+). New methodology detail: skills are pressure-tested by dispatching subagents into adversarial scenarios that apply Cialdini-style persuasion principles (authority, commitment, sunk-cost, time-pressure) to ensure compliance under realistic stress. Microsoft Amplifier surfaced as a sibling framework using the same self-improving-via-SKILL.md pattern.

---

## 1. Cognition — Devin

**One-line.** Autonomous AI software engineer that takes a ticket from Linear, Jira, or Slack and returns a pull request, iterating on review comments without a human in the loop.

**Workflow primitives.**
- **Ticket / task** is the unit of work; ingested from Linear, Jira, Slack, or a chat prompt.
- **Session** runs on a dedicated cloud VM with browser, shell, and editor tools. The session emits a **plan** the user can edit before "committing ACUs" (Agent Compute Units).
- **ACU** is the billing primitive — Cognition's normalized resource unit covering VM time, model inference, and bandwidth. 1 ACU ≈ 15 minutes of active work.
- **Cognition-Golden** is their internal evaluation benchmark; they explicitly use **evaluator agents** (LLM-as-judge with browser/shell/editor tools) to score outcomes that are too complex to verify by tests alone. The blog post "A review of OpenAI's o1 and how we evaluate coding agents" describes this. So while Devin's user-facing primitive is ticket → PR, *internally* Cognition treats coding as a (task, environment, judge) triple — close to a scenarios + judge architecture but kept behind the curtain.
- No user-facing "spec" or "scenario" object. The conversation and the ticket body are the spec.

**Human role per their pitch.** Manager / reviewer. The human writes the ticket, optionally reviews Devin's proposed plan, then reviews the resulting pull request. Cognition's marketing framing is unambiguously "AI software engineer," not "AI pair-programmer."

**Cost / pricing model.** Per `devin.ai/pricing` (drained 2026-05-13) — the published tiers have been completely restructured and **no ACU pricing is publicly visible**:
- **Free** — Limited Devin usage; Devin Review; DeepWiki. (Individual plan)
- **Pro** — **$20/month.** Devin usage quota; Windsurf IDE usage quota; pay-as-you-go for usage past quota; Slack / Linear / MCP integrations. Up to 10 concurrent sessions. (Individual plan)
- **Max** — **$200/month.** Same as Pro with increased Devin and Windsurf quotas. (Individual plan)
- **Teams** — **$80/month.** Everything in Pro plus unlimited team members, share and collaborate, centralized billing, admin dashboard with analytics. Unlimited concurrent sessions. (Business plan, marked "Recommended" on the page.)
- **Enterprise** — Custom. SAML/OIDC SSO, centralized enterprise admin controls, dedicated account team, custom terms, VPC deployment, Devin Enterprise (most capable variant).

> **Refutation of prior text.** The earlier reconstructed pricing ($500 Team with 250 ACUs included, ACU ≈ 15 minutes at ~$2.00–$2.25) does not appear anywhere on the current published pricing page. The unit "ACU" itself is absent from the public pricing page. Quotas are described generically as "Devin usage quota" / "increased quota" / "Pay-as-you-go for usage past quota," and the page surfaces a $20 Pro / $200 Max / $80 Teams / Enterprise structure instead. The $500-Team-with-ACUs framing should be treated as historical (likely Devin 2.0 era, pre-2026) and not quoted externally.

**Differentiator.** End-to-end autonomy on async tickets, plus a public-facing claim of "Devin builds Devin." The eval-agent methodology described in their evaluating-coding-agents blog remains a real moat — most competitors don't publish a verification story. The homepage hero is the **Nubank case study**: 8–12× engineering-time efficiency, 20× cost savings, migrating a 6M-LOC monolithic ETL by fine-tuning a "Custom ETL Migration Devin" against an internal evaluation benchmark (the same cognition-golden methodology). New product surface visible on the homepage: **Devin for Terminal**, Devin Review (PR review + visual QA), DeepWiki (auto-generated docs/diagrams for legacy code), and **"Managed Devins" orchestration** as part of "Advanced Capabilities" — letting Devin orchestrate multiple Devins in parallel, analyze past sessions, and improve playbooks. This is essentially a multi-agent fleet primitive that did not appear in our prior secondary-sourced description.

**Public methodology docs.**
- cognition.ai/blog/evaluating-coding-agents (eval-agent / judge methodology)
- cognition.ai/blog/devin-annual-performance-review-2025
- cognition.ai/blog/how-cognition-uses-devin-to-build-devin

---

## 2. 8090 Solutions — Software Factory

**One-line.** AI-native software development platform that puts **documentation, collaboration, and oversight** at the center of the SDLC, keeping business leaders "in the driver's seat" while AI agents execute. Marketing tagline (from `8090.inc` homepage, drained 2026-05-13): *"AI is writing your software. Who's in control?"* — a governance-first framing, not just an upstream-context framing.

**Workflow primitives.** Of the five vendors here, 8090 is the most architecturally aligned with the "software factory" framing of our own project.
- **Requirements** — captured as first-class artifacts, not chat history.
- **Architecture decisions** — captured upstream of code generation.
- **Work orders** — the dispatchable unit handed to coding agents. Closest analog to a scoped spec or ticket-with-acceptance-criteria.
- **Knowledge graph** — built either forward (new builds) or retroactively via **reverse-engineering agents** for legacy modernization.
- **Validation / feedback loop** — explicit in their pitch, though the public material does not name a "judge" primitive.

**Human role.** Product / architecture lead. Humans define requirements and architecture; agents generate work orders and code; humans validate. 8090's stated philosophy is "AI with a human touch" — they sell a managed-services flavor where their engineers operate the factory on the customer's behalf.

**Two-product split** (confirmed from primary homepage). 8090 now sells two clearly-separated SKUs:
- **Software Factory** (`factory.8090.ai`) — "the AI-native SDLC control plane." Self-serve. Brings team and AI agents into a single system; define intent, coordinate execution, maintain control / visibility / auditability over every decision.
- **8090 Enterprise** (`/custom-delivery`) — purpose-built applications designed around customer workflows. "We design, build, host, and maintain. You own the business logic." This is the managed-delivery offering.

**Cost / pricing model.** The homepage does not surface specific dollar figures; pricing lives at `/pricing` and `/custom-delivery`. Prior secondary figures (Team $200/seat + tokens; Custom Delivery from $1M/yr) were not visible on the homepage drain, so they remain unverified primary-source-wise. 8090 is still the only competitor in the set offering a managed-delivery tier where the vendor hosts and maintains the resulting application.

**Differentiator.** Three pillars named verbatim on the homepage: **documentation, collaboration, oversight.** Concrete claims:
1. *"Control stays with leadership"* — business leaders define what gets built in plain English before any code; explicit rejection of "AI agents and junior devs making architectural decisions on your behalf."
2. *"Tribal knowledge dies. Documentation lives."* — upload institutional knowledge once; it becomes a "living knowledge graph that survives employee turnover, onboarding cycles, and policy changes." Knowledge-graph framing is now a top-of-funnel claim, not a buried feature.
3. *"Built for regulated industries"* — healthcare, financial services, manufacturing, federal government; backed by a Big Four partnership (**EY** confirmed by an on-page quote from Colm Sparks-Austin, EY Americas Technology Consulting Leader).

Chamath Palihapitiya appears on-page as a named **Co-founder and CEO** quote, confirming his operational (not just investor) role.

**Public methodology docs.** Beyond the homepage and the two product pages, 8090 has `/docs/general/introduction` linked from the footer — the public docs entry point, which the drain did not retrieve. Most product detail still lives behind the self-serve sign-up at `factory.8090.ai`.

---

## 3. Factory — Droid

**One-line.** "Agent-Native Software Development" — the only software-development agents *that work everywhere you do.* Droids embed into IDE, Web, CLI, Slack/Teams, and Project-Manager surfaces; delegate complete tasks like refactors, incident response, and migrations without changing tools, models, or workflow. (Primary copy lifted verbatim from `factory.ai` homepage, drained 2026-05-13.)

**Workflow primitives.**
- **Droid** — a role-scoped agent. The homepage no longer enumerates individual droid roles (Code/Review/Docs/Test/Knowledge/Product); instead it emphasizes Droid mobility across surfaces. Role-scoping remains documented at `docs.factory.ai`.
- **Five surfaces** (verbatim section numbering on the homepage):
  1. Terminal / IDE — VS Code, JetBrains, Vim; "Droids where you code"
  2. Desktop / Web — browser-based delegation, no setup; "Droids in the browser"
  3. Command Line — script and parallelize at scale for CI/CD, migrations, maintenance; "Droids at scale"
  4. Slack / Teams — shared line for support + engineering; "Droids in the war room"
  5. Project Manager — auto-trigger from issue assignment or mentions, ticket-to-PR traceability; "Droids in your backlog"
- **Ticket** — the dispatch unit for the Project-Manager surface; "Factory pulls context, implements solutions, and creates PRs while maintaining full traceability from ticket to code."
- **Droid Computers** (new since prior reconstruction) — *"persistent machines for remotely orchestrating Droids. Spin one up in Factory's cloud, or turn your own machine into a Droid Computer."* This is a meaningful new primitive: explicit, long-lived agent-host machines that mirror an IDE workspace but live in the cloud or on hardware you control.
- **Specification Mode** — no longer surfaced on the homepage; remains documented at `docs.factory.ai/cli/user-guides/specification-mode`. Its demotion from headline copy suggests Factory now leads with surface-coverage and delegation rather than spec-first methodology.
- Model-agnostic: still claimed verbatim ("any model provider, any dev tooling, any interface").

**Human role.** Ticket author and PR reviewer, but the on-page framing has softened: *"AI that will work **with you**, not replace you."* This is a notable repositioning away from autonomous-engineer rhetoric and toward augmented-engineer rhetoric. Compared with Devin's "AI software engineer" claim, Factory is now explicitly the pair-programming-coded option among the autonomous-agent vendors.

**Cost / pricing model.** Homepage links to `/pricing` but does not surface tier figures. Prior secondary-source claim "$20/month individual; Team & Enterprise via sales" was not primary-confirmed in this drain; the dedicated pricing page was not fetched. SOC-2 / SSO / audit-trail claims live at `/security` and were not retrieved.

**Differentiator.** Surface ubiquity is the new headline ("the only software-development agents that work everywhere you do"). Series C $150M @ $1.5B valuation confirmed in the on-page news rail. The **Droid Computers** primitive is the most architecturally distinctive new piece of the pitch — it's a clean abstraction for "where the agent runs" that competitors haven't named. Terminal-Bench leadership at 58.75% was secondary-sourced; the homepage now points to a code-review benchmark study (*"Which Model Reviews Code Best?"*) and an automated-QA product launch as fresh research/product proof points.

**Public methodology docs.**
- docs.factory.ai/cli/user-guides/specification-mode
- docs.factory.ai/pricing
- factory.ai/news/terminal-bench
- Latent.Space podcast "Factory.ai: The A-SWE Droid Army"

---

## 4. Superconductor

> **Drain note (issue #31).** The fetched URL `superconductor.io` resolves to a domain-for-sale page on Atom.com — *not* the Superconductor product. The actual company is at `superconductor.com`, which was not on the issue-31 URL list. This section therefore remains anchored to secondary sources (the `oscardobsonbrown/superconductor` GitHub repo and the public README/AGENTS.md). A follow-up fetch of `superconductor.com` is logged in Open Follow-ups below.

**One-line.** Workspace orchestrator that runs many CLI coding agents (Claude Code, Codex, Cursor, Gemini CLI, etc.) in parallel across isolated git worktrees, with two distinct products: a cloud platform (superconductor.com) and a native macOS app (App Store).

**Workflow primitives.**
- **Workspace** — a task scoped to its own git worktree and branch.
- **Ticket** — the user-facing unit, ingestable from the app, Slack, GitHub, or "automatic processing of signals such as email." This is unusual: Superconductor explicitly tries to *infer* tickets from inbound communication rather than only consuming hand-authored ones.
- **Agent session** — lives in the cloud (not on the user's machine), so any team member can pick up where another left off.
- **`.superset/config.json`** — declarative setup/teardown scripts the README describes as "Scenarios," giving Superconductor a lightweight scenarios primitive for environment configuration (though scoped to dev-env, not test cases).
- **Review** — built-in diff viewer with guided review panels and live previews.
- **One-click handoff** — escalates a workspace to the user's IDE or terminal when the agent is stuck.

**Human role.** Orchestrator and reviewer of a swarm. The user is explicitly cast as the conductor of many parallel agents — choosing which ticket to launch, reviewing diffs side-by-side, and intervening only when handoff is needed.

**Cost / pricing model.**
- Native macOS app is **free during alpha**.
- Cloud platform pricing not published as of fetch; sign-up gated.
- Source-available under **Elastic License 2.0** (ELv2) per the GitHub repo (oscardobsonbrown/superconductor).

**Differentiator.** Agent-agnostic orchestration ("any CLI agent works") plus parallelism as the headline feature — the pitch is "run 10+ coding agents simultaneously." Cloud-resident sessions enable team handoff in a way that local-only tools (Claude Code, Codex CLI) cannot. The Rust-native desktop client and the email-to-ticket inbound are unusual touches. Of the five vendors, Superconductor is the most explicitly multi-agent-parallel by design.

**Public methodology docs.**
- superconductor.com/docs (gated from this environment)
- github.com/oscardobsonbrown/superconductor (README and AGENTS.md gist)

---

## 5. Jesse Vincent — Superpowers

**One-line.** Open-source agentic skills framework and software-development methodology distributed as a Claude Code plugin. Imposes a disciplined three-phase workflow (**brainstorm → plan → implement**) on a coding agent through composable Markdown "skills" — small instruction files the agent searches for and consults before acting.

**Workflow primitives.** Per the origin post (`blog.fsck.com/2025/10/09/superpowers/`, drained 2026-05-13), the headline workflow is the **three-phase loop:**
1. **Brainstorm** — Claude defaults to talking through a plan with the user before any implementation; refines ideas, explores alternatives, validates design.
2. **Plan** — once brainstorming concludes, Claude auto-creates a git worktree (if in a git repo) and switches to it, so parallel tasks on the same project don't clobber each other.
3. **Implement** — Claude offers a choice between two modes: (a) the **"human-PM" mode** where the user opens a second `claude` session and acts as PM between architect and implementer (the September-2025 process), or (b) the **subagent-dispatch mode** where Claude itself dispatches tasks one-by-one to subagents and code-reviews each task before continuing. Either mode runs **RED/GREEN TDD** — write a failing test, implement just enough to pass, move on. At the end, Claude offers to open a GitHub PR, merge the worktree locally, or stop.

> **Refutation of prior reconstruction.** The earlier 7-step pipeline (Brainstorming / Git worktrees / Writing plans / Subagent-driven development / TDD / Code review / Verification-before-completion) is *not* the published workflow. Those are individual skills (each with its own `SKILL.md`), and they participate in the loop, but Vincent describes the headline as a three-phase **brainstorm → plan → implement** loop with TDD baked into implementation. The "verification-before-completion" skill is mentioned by name only as a future intent ("memories" workflow); the published post does not elevate it to a top-level phase.

Named primitives in the framework: **skill** (Markdown SKILL.md files, surfaced via a session-start-hook that injects an `EXTREMELY_IMPORTANT` directive pointing to `getting-started/SKILL.md`), **plan**, **subagent**, **worktree**, **plugin marketplace**.

**Distinctive methodology detail (new from primary source).** Vincent pressure-tests each skill by dispatching subagents into adversarial **persuasion-pressure scenarios** — explicitly built around Robert Cialdini's principles (authority, commitment, scarcity, time-pressure, sunk-cost). Sample scenarios on the page include "your production system is down, every minute costs $5k, do you read the skill first?" and "you just spent 45 minutes writing test infra, your partner asks you to commit — do you check the async-testing skill?" After each failure, Claude strengthens `getting-started/SKILL.md`. Vincent cites a Wharton GAIL study by Dan Shapiro and co-authors that puts scientific rigor behind Cialdini's principles working on LLMs.

**Sibling framework reference (new).** Vincent points to **Microsoft Amplifier** (`github.com/microsoft/amplifier`) by Sam Schillace and Brian Krabach as another integrated development framework using the same pattern of a coding agent that improves itself by writing out markdown docs and tools. This is worth a follow-up — it's a Microsoft-backed parallel to Superpowers we hadn't tracked.

**Human role.** Author of intent + checkpoint reviewer. Vincent is explicit that the human validates the design during brainstorming and at human checkpoints. The pitch is explicitly *not* "fire-and-forget" — but the post is more relaxed than the earlier reconstruction implied ("self-driving enough that you can [stop reading and play]"). Methodology > model remains the thesis.

**Cost / pricing model.** Free and open source. Install via the Claude Code plugin marketplace:
```
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
```
Requires Claude Code 2.0.13+. Vincent notes (with some regret) that the plugin system replaced the earlier install-by-symlink method of "Hey Claude, please read this URL and do what it says." The user pays only their Claude Code subscription / API spend.

**Differentiator.** The thesis: *methodology > model*. The published install path now goes through Anthropic's official plugin marketplace (released the same morning as the origin post, October 9 2025) rather than a manual git symlink. The session-start-hook bootstrap mechanism — injecting a mandatory `EXTREMELY_IMPORTANT` prompt that forces Claude to read `getting-started/SKILL.md` before doing anything else — is a concrete, copyable architectural pattern. The Cialdini-style pressure-testing of skills with adversarial subagents is the most distinctive evaluation/judging methodology in the set: not scenario-graded behavior, but compliance-graded discipline under persuasive pressure.

**Public methodology docs.**
- github.com/obra/superpowers (README + all skill SKILL.md files)
- blog.fsck.com/2025/10/09/superpowers/ (origin post — Cloudflare-blocked here but widely cited)
- github.com/obra/superpowers/blob/main/skills/verification-before-completion/SKILL.md
- github.com/obra/superpowers/blob/main/skills/test-driven-development/SKILL.md
- github.com/obra/superpowers/blob/main/skills/writing-plans/SKILL.md

---

## Comparison Table

| Vendor | Explicit Spec primitive? | Explicit Scenarios? | Explicit Judge / Eval? | Human role | Cost model |
|---|---|---|---|---|---|
| **Devin (Cognition)** | No (ticket = spec). Plan is editable pre-run. | No user-facing scenarios. Internal eval uses VM environments. | Yes, internal: evaluator-agents on cognition-golden. Not user-exposed. | Ticket author + PR reviewer; manager of an autonomous engineer (and now an orchestrator of Managed Devins). | Free / Pro $20 / Max $200 / Teams $80 / Enterprise custom (per `devin.ai/pricing`, 2026-05-13). Generic "Devin usage quota" + pay-as-you-go. ACU pricing **not** on the current public page. |
| **8090 Solutions** | Yes — business intent captured in plain English upstream; living knowledge graph of institutional context. | No public scenarios primitive. | Governance / oversight pitched as control plane; no named judge. | Product/architecture lead ("business leaders in the driver's seat"), often co-staffed by 8090 delivery team in the 8090 Enterprise SKU. | Two SKUs: **Software Factory** (self-serve SDLC control plane) + **8090 Enterprise** (designed-built-hosted by 8090). Dollar figures not surfaced on homepage; prior $200/seat + $1M/yr figures remain secondary-sourced. |
| **Factory (Droid)** | Specification Mode exists in docs but is no longer on the homepage; ticket-driven workflow is now the lead. | Sandboxed workspaces per session; **Droid Computers** as named persistent-machine primitive. | Review Droid + Test Droid play judge-like roles; new code-review benchmark study published. | Ticket author + PR reviewer; pair-programming partner ("AI that will work with you, not replace you"). | $20/mo individual + Team / Enterprise via sales (prior secondary; homepage drained does not expose pricing). Model-agnostic. |
| **Superconductor** | Tickets only; no formal spec object. | Yes, lightweight: `.superset/config.json` setup/teardown scripts. | No explicit judge; built-in diff/review UI for humans. | Orchestrator of many parallel agents; reviewer; handoff escalator. | macOS app free in alpha; cloud pricing gated; ELv2 source-available. |
| **Superpowers (obra)** | Yes — brainstorm phase produces a plan/design before implementation; explicit phase in the headline workflow. | Cialdini-style adversarial **persuasion-pressure scenarios** to compliance-test skills; no scenario object for behavior testing per se. | Per-task subagent code review built into "implement" phase; TDD RED/GREEN enforced. | Intent author + brainstorm partner + checkpoint reviewer; or full PM-mode. Methodology > model. | Free / OSS plugin via Claude Code marketplace (`obra/superpowers-marketplace`, requires CC 2.0.13+). User pays only Claude Code / API. |

---

## How this situates our four architectures

Reading across the five competitors:

- **Spec-first** as a user-facing primitive is rare and getting rarer. Factory's Specification Mode has been **demoted from the homepage** as of this drain — it still exists in CLI docs but is no longer marketing-headline material. Superpowers' brainstorm phase remains the most prominent spec-shaped primitive in the set, but the methodology framing is "talk through a plan with the agent," not "author a formal spec object." Devin, Superconductor, and (now) Factory all front-end on tickets-or-prompts; 8090 elevates "business intent in plain English" upstream but does not call it a spec. If our architectures lean on a formal Spec object, we are differentiated against five of five at the headline-primitive level, with the closest methodological neighbor still being Superpowers.

- **Scenarios** are nearly absent as a first-class primitive across the market. Cognition uses scenario-like environments internally (cognition-golden), Superconductor's `.superset` scripts are scenario-shaped but for dev-env setup, not behavior. Nobody in this competitive set sells scenarios as the unit-of-correctness in their pitch. This is plausible whitespace.

- **Judges / LLM-as-evaluator** is real but mostly invisible to users. Cognition has the most developed practice (and publishes about it). Superpowers exposes a two-stage subagent reviewer to the user. Factory ships Review and Test Droids which play partial judge roles. Nobody sells "the judge" as a primitive customers configure. Another whitespace zone.

- **Human role** clusters into three pitches: (a) **manager of an autonomous engineer** (Devin), (b) **author of well-formed tickets** (Factory, 8090, Superconductor), and (c) **enforcer of methodology with checkpoint reviews** (Superpowers). Our architecture choices imply different positions on this spectrum.

- **Pricing** ranges three orders of magnitude — $0 (Superpowers OSS) → $20/mo (Devin Core, Factory individual) → $200/seat + tokens (8090 Team) → $500/mo + ACUs (Devin Team) → $1M+/yr managed (8090). This corresponds to "self-serve methodology" vs "self-serve SaaS" vs "platform + services" — three distinct go-to-market shapes.

- **Multi-agent decomposition** is now table stakes at the top end *and Devin has flipped*: the homepage drain confirms Cognition now exposes **"Managed Devins"** as an Advanced Capability — letting Devin orchestrate multiple Devins in parallel, analyze past sessions, and improve playbooks. Combined with Factory's role-scoped droids + Droid Computers, Superconductor's parallel CLI agents, and Superpowers' subagent dispatch, *every* competitor in the set is now multi-agent at the headline-architecture level. The "one model, one process" framing is fully off-market.

- **Where the agent runs** has emerged as a named primitive only at Factory (Droid Computers — "spin one up in our cloud, or turn your own machine into one"). Devin runs on Cognition's cloud VMs implicitly. Superconductor's agent sessions are cloud-resident. Superpowers runs locally in whatever Claude Code session you have. 8090 hosts its Software Factory and (for Enterprise) the resulting applications. This is a real architectural axis — none of our four candidate architectures has staked out a position on it, and Factory has the cleanest abstraction so far.

---

## Open follow-ups

- **Devin pricing reconciliation.** The published pricing page now shows Free / Pro $20 / Max $200 / Teams $80 / Enterprise — *without* surfacing ACUs. Open question: does the ACU primitive still exist behind the Pro/Max/Teams "usage quota" wording, or has Cognition abstracted it away publicly? Worth checking the in-app billing UI or the most recent Cognition blog post for clarification.
- **Cognition's evaluating-coding-agents blog** (`cognition.ai/blog/evaluating-coding-agents`) is referenced from the homepage Nubank case study but was not in the fetch list. Highest-value primary source on judge architecture across this competitive set; worth a dedicated fetch.
- **Cognition blog index** — the `cognition.ai/blog/devin` URL returned a hard 404 in issue #31. The correct entry point is `cognition.ai/blog/1` (paginated index, linked from the Devin homepage). Re-target a future fetch to this URL.
- **Factory `/pricing` and Specification Mode docs** were not in the fetch list. `docs.factory.ai/cli/user-guides/specification-mode` would let us extract the exact spec schema; `/pricing` would primary-confirm or refute the $20/mo individual figure. The `/product` URL returned 404 — Factory's product detail now lives in five `/product/<surface>` URLs (ide, desktop, cli, slack, ai-project-manager) per the homepage nav.
- **Factory Droid Computers** is a brand-new primitive surfaced on the homepage; `factory.ai/news/droid-computers` would describe it in detail.
- **8090 docs** — `8090.inc/docs/general/introduction` is the linked entry point; not in the fetch. Would clarify whether the "knowledge graph" and "work orders" primitives have technical definitions or remain marketing language.
- **8090 blog correction.** The URL `8090.inc/blog` returned 404. The footer link goes to `/blog` but the homepage routes blog content under `/news`-style paths via the Resources mega-menu; correct path to be discovered.
- **Superconductor primary fetch.** Issue #31 hit the wrong domain (`.io` is for sale). Re-target `superconductor.com` (the live product), the macOS App Store listing, and the `oscardobsonbrown/superconductor` GitHub repo for direct primary-source anchoring of the cloud platform and the parallel-CLI-agents claim.
- **Microsoft Amplifier** (`github.com/microsoft/amplifier`) — surfaced by Jesse Vincent as a sibling framework to Superpowers using the same self-improving-via-SKILL.md pattern, backed by Sam Schillace and Brian Krabach. Not previously tracked; worth a competitor-landscape-style write-up.
- **Superpowers verification-before-completion SKILL.md** should still be read in full — Vincent's origin post mentions it only obliquely, but the report's prior framing of it as a quasi-judge primitive remains the right intuition; the skill file itself will tell us how rigorous it is.
- **Wharton GAIL persuasion study** (Cialdini + Shapiro et al., `gail.wharton.upenn.edu/research-and-insights/call-me-a-jerk-persuading-ai/`) — referenced by Vincent as evidence that Cialdini's persuasion principles work on LLMs. Direct read recommended if our architectures lean on adversarial subagent compliance testing.

---

## Sources reviewed

| URL | Status | Notes |
|---|---|---|
| `devin.ai/` | ✅ primary (issue #31) | Marketing homepage; Nubank case study hero; product surfaces enumerated. |
| `devin.ai/pricing` | ✅ primary (issue #31) | Current public tiers Free / Pro $20 / Max $200 / Teams $80 / Enterprise; **no ACU pricing visible**. |
| `www.factory.ai/` | ✅ primary (issue #31) | Agent-Native framing; five surfaces; Droid Computers; Series C confirmed. |
| `www.8090.inc/` | ✅ primary (issue #31) | Two SKUs (Software Factory / 8090 Enterprise); three pillars; EY + Chamath confirmed. |
| `blog.fsck.com/2025/10/09/superpowers/` | ✅ primary (issue #31) | Origin post; three-phase workflow corrected; Cialdini pressure-test methodology; plugin install path. |
| `www.superconductor.io/` | ✅ fetched but **wrong target** (issue #31) | Resolves to an Atom.com domain-for-sale page. The actual product is at `superconductor.com`. Section remains secondary-sourced. |
| `www.cognition.ai/blog/devin` | ❌ HTTP 404 — page does not exist at that path; not a sandbox block. | Correct index is `cognition.ai/blog/1` (linked from the Devin homepage). |
| `www.factory.ai/product` | ❌ HTTP 404 — page does not exist at that path; not a sandbox block. | Factory product detail now lives at `/product/<surface>` URLs (ide, desktop, cli, slack, ai-project-manager). |
| `www.8090.inc/blog` | ❌ HTTP 404 — page does not exist at that path; not a sandbox block. | The footer link to `/blog` 404s; site uses a Resources mega-menu instead. |
| `github.com/obra/superpowers` (README, SKILL.md files) | secondary | Used in original fan-out; still authoritative for individual skill content. |
| `github.com/oscardobsonbrown/superconductor` (README, AGENTS.md) | secondary | Still the only reachable Superconductor primary; live `.com` not yet fetched. |
| `docs.factory.ai/cli/user-guides/specification-mode` | secondary | Spec-mode docs; not fetched in issue #31. |
| `cognition.ai/blog/evaluating-coding-agents` | secondary | Eval-agent methodology; referenced from Nubank case study; not fetched. |
| Latent.Space podcast "Factory.ai: The A-SWE Droid Army" | secondary | Used in original fan-out. |
| `sundaylettersfromsam.substack.com` (Schillace on Amplifier) | secondary | Referenced from Vincent's post; not fetched. |
