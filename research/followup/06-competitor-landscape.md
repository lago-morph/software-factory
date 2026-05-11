# Round-3 Thread 6: Competitor Landscape

**Run:** fanout 20260511-054258 sub-09
**Date:** 2026-05-11
**Scope:** Five named competitors in the AI-coding-agent / software-factory space — Cognition's Devin, 8090 Solutions, Factory's Droid, Superconductor, and Jesse Vincent's Superpowers. Goal is to situate our four candidate architectures against shipping products by extracting each vendor's workflow primitives, human role, pricing model, and differentiator.

**Fetch notes.** All five primary homepages (devin.ai, factory.ai, 8090.inc, superconductor.io, blog.fsck.com) returned HTTP 403 to the WebFetch tool — they sit behind Cloudflare bot challenges. Web Archive is also blocked from this environment. Findings below were assembled from indirect sources: GitHub READMEs (obra/superpowers, oscardobsonbrown/superconductor), Factory's docs site (docs.factory.ai), Cognition's blog (cognition.ai), Latent.Space podcast, and several independent reviews and pricing-explainer pages indexed by web search. Treat numeric pricing figures as recent-but-secondhand. No `[fetch-urls]` issue was filed because workable info was reachable for all five.

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

**Cost / pricing model.** Three tiers (relaunched in Devin 2.0 in early 2025):
- **Core** — $20/month, ACUs at ~$2.25 each. Targeted at individuals and trial usage.
- **Team** — $500/month, 250 ACUs included, $2.00 per extra ACU. SOC-2, multi-seat.
- **Enterprise** — custom; SaaS or VPC deployment.
The original 2024 launch was $500/month flat; the $20 Core tier was added to compete with cheaper IDE assistants.

**Differentiator.** End-to-end autonomy on async tickets, plus a public-facing claim of "Devin builds Devin" — Cognition publishes how they self-host, including a "How Cognition Uses Devin to Build Devin" post. The eval-agent methodology is a real moat: most competitors don't publish a verification story.

**Public methodology docs.**
- cognition.ai/blog/evaluating-coding-agents (eval-agent / judge methodology)
- cognition.ai/blog/devin-annual-performance-review-2025
- cognition.ai/blog/how-cognition-uses-devin-to-build-devin

---

## 2. 8090 Solutions — Software Factory

**One-line.** AI-native SDLC orchestration platform that captures requirements, architecture decisions, and work orders upstream so downstream coding agents have enough context to produce aligned code; sold alongside high-touch enterprise delivery.

**Workflow primitives.** Of the five vendors here, 8090 is the most architecturally aligned with the "software factory" framing of our own project.
- **Requirements** — captured as first-class artifacts, not chat history.
- **Architecture decisions** — captured upstream of code generation.
- **Work orders** — the dispatchable unit handed to coding agents. Closest analog to a scoped spec or ticket-with-acceptance-criteria.
- **Knowledge graph** — built either forward (new builds) or retroactively via **reverse-engineering agents** for legacy modernization.
- **Validation / feedback loop** — explicit in their pitch, though the public material does not name a "judge" primitive.

**Human role.** Product / architecture lead. Humans define requirements and architecture; agents generate work orders and code; humans validate. 8090's stated philosophy is "AI with a human touch" — they sell a managed-services flavor where their engineers operate the factory on the customer's behalf.

**Cost / pricing model.**
- **Team plan** — $200/seat/month + token-based usage.
- **Enterprise** — custom.
- **Custom Factory Lines** — modernization projects, custom-quoted.
- **Custom Delivery** — fully managed engagements starting at $1M/year.
This is the only competitor in the set with a seven-figure managed-service tier; 8090 is selling consulting-with-a-platform, not pure self-serve SaaS.

**Differentiator.** Upstream context capture (requirements + architecture + decisions) rather than chat-driven code generation. Backed/founded by Chamath Palihapitiya, which gives them enterprise-sales reach. The reverse-engineering agents for legacy codebases are a distinctive wedge into the brownfield modernization market that pure code-gen tools struggle to serve.

**Public methodology docs.** 8090's website itself was 403-blocked from this environment, but Ry Walker's research note "8090 Solutions (Software Factory)" and Oreate AI's writeup describe the workflow. There is no obvious public methodology whitepaper — most material is sales-led.

---

## 3. Factory — Droid

**One-line.** Agent-native software development platform where a coordinator agent dispatches a fleet of role-scoped Droids (code, review, docs, test, knowledge, product) into sandboxed workspaces, embedded in IDE/Web/CLI/Slack/Linear.

**Workflow primitives.**
- **Droid** — a role-scoped agent (Code Droid, Review Droid, Docs Droid, Test Droid, Knowledge Droid, Product Droid). The coordinator dispatches work across them.
- **Ticket** — the native unit of work; Linear and Jira integrations make tickets the default surface ("write a good ticket, label it for the droid swarm, hand it off").
- **Session** — each conversation/run is a session bound to a sandboxed workspace mirroring the project's toolchain.
- **Specification Mode** — a CLI mode (Shift+Tab) that produces an explicit plan; can "Save spec as Markdown" to commit the approved plan to disk. This is the most explicit "spec" primitive of any vendor in the set.
- **Acceptance criteria** are read off the ticket and used as the agent's working contract.
- Model-agnostic: Claude, GPT, Gemini, or custom, picked per task.

**Human role.** Ticket author + reviewer. The pitch is "ticket-first, not chat-first" — humans communicate intent through structured tickets with acceptance criteria, and review the PR. There is also an interactive IDE mode for pair-programming-style work.

**Cost / pricing model.**
- Paid plans start at **$20/month** (individual).
- **Team** and **Enterprise** tiers require Sales contact.
- SOC-2 Type II, SSO/SAML, audit trails baked in. Customer code is not used for training.

**Differentiator.** Multi-droid role decomposition is the headline architectural bet — rather than one omni-agent, Factory ships a small society of specialists with explicit boundaries. They have led Terminal-Bench at 58.75%. Their $150M Series C at a ~$1.5B valuation (2026) gives them enterprise sales momentum. Specification Mode is the closest competitor primitive to our own spec-first architecture candidates.

**Public methodology docs.**
- docs.factory.ai/cli/user-guides/specification-mode
- docs.factory.ai/pricing
- factory.ai/news/terminal-bench
- Latent.Space podcast "Factory.ai: The A-SWE Droid Army"

---

## 4. Superconductor

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

**One-line.** Open-source agentic skills framework and software development methodology distributed as a Claude Code plugin, imposing a disciplined multi-phase workflow on a coding agent through composable Markdown "skills."

**Workflow primitives.** Superpowers is the methodology-richest of the five — it ships an explicit phased pipeline:
1. **Brainstorming** — refine ideas, explore alternatives, validate design in sections, save design doc. Closest to a `spec` artifact.
2. **Git worktrees** — isolate workspace per task and verify a clean test baseline.
3. **Writing plans** — break work into bite-sized 2–5-minute tasks, each with exact file paths, complete code stubs, and verification steps.
4. **Subagent-driven development** — dispatch a fresh subagent per task with **two-stage review**: first spec-compliance, then code-quality.
5. **Test-driven development** — enforced RED → GREEN → REFACTOR with strict YAGNI/DRY.
6. **Code review** — review against plan; critical issues block.
7. **Verification before completion** — re-read plan, build checklist, run commands, read output, then report. No claim without evidence.

Named primitives in the framework: **skill** (Markdown SKILL.md files), **spec / design document** (output of brainstorming), **plan**, **subagent**, **verification checklist**. The two-stage subagent review is the closest analog to a judge primitive in the set, though it is "LLM-as-reviewer-of-spec-compliance" rather than scenario-based grading.

**Human role.** Author of intent + checkpoint reviewer. The framework is explicit that the human validates the design in sections during brainstorming and at human checkpoints between batches of plan tasks. The pitch is *not* "fire-and-forget like Devin" — Vincent explicitly argues that methodology beats model upgrades, and the human's job is to enforce the discipline.

**Cost / pricing model.** Free and open source (license per repo). The cost is whatever Claude Code subscription / API spend the user incurs running the framework. Distributed as an Anthropic Claude Code marketplace plugin since early 2026.

**Differentiator.** The thesis: *methodology > model*. Vincent argues that imposing a rigorous 5–7-phase discipline on an existing model outperforms letting a stronger model run unconstrained. The plugin reportedly has ~93k–174k GitHub stars within 7 months — by far the most viral methodology framework in this set. The verification-before-completion skill in particular is something none of the commercial vendors expose as a first-class primitive.

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
| **Devin (Cognition)** | No (ticket = spec). Plan is editable pre-run. | No user-facing scenarios. Internal eval uses VM environments. | Yes, internal: evaluator-agents on cognition-golden. Not user-exposed. | Ticket author + PR reviewer; manager of an autonomous engineer. | $20 Core / $500 Team (250 ACUs) / Enterprise custom. ACU ≈ 15 min, ~$2/ACU. |
| **8090 Solutions** | Yes — Requirements + Architecture decisions captured upstream; Work Orders dispatched. | No public scenarios primitive; validation loop mentioned generically. | Validation/feedback loop in pitch; not named as judge. | Product/architecture lead, often co-staffed by 8090 delivery team. | $200/seat/mo + tokens; Enterprise custom; Custom Delivery from $1M/yr. |
| **Factory (Droid)** | Yes — Specification Mode (Shift+Tab in CLI), can save spec as Markdown. Acceptance criteria from tickets. | Sandboxed workspaces per session; no scenarios object per se. | Review Droid + Test Droid play judge-like roles; no public scenario-graded benchmark. | Ticket author + PR reviewer; orchestrator of droid swarm. | $20/mo individual; Team & Enterprise via sales. SOC-2, model-agnostic. |
| **Superconductor** | Tickets only; no formal spec object. | Yes, lightweight: `.superset/config.json` setup/teardown scripts. | No explicit judge; built-in diff/review UI for humans. | Orchestrator of many parallel agents; reviewer; handoff escalator. | macOS app free in alpha; cloud pricing gated; ELv2 source-available. |
| **Superpowers (obra)** | Yes — brainstorming produces a saved design document (spec). | Implicit via verification checklists + TDD red/green; no scenario data model. | Two-stage subagent review (spec compliance + code quality); verification-before-completion skill. | Intent author + section validator + checkpoint reviewer. Methodology enforces discipline. | Free / OSS plugin; user pays only Claude Code / API costs. |

---

## How this situates our four architectures

Reading across the five competitors:

- **Spec-first** as a user-facing primitive is rare. Only Factory (Specification Mode) and Superpowers (brainstorming → design doc) expose it directly. Devin and Superconductor both collapse it into "the ticket." 8090 elevates requirements/architecture upstream but bundles them with services delivery. If our architectures lean on a formal Spec object, we are differentiated against three of five, partially aligned with Factory's CLI mode, and methodologically aligned with Superpowers.

- **Scenarios** are nearly absent as a first-class primitive across the market. Cognition uses scenario-like environments internally (cognition-golden), Superconductor's `.superset` scripts are scenario-shaped but for dev-env setup, not behavior. Nobody in this competitive set sells scenarios as the unit-of-correctness in their pitch. This is plausible whitespace.

- **Judges / LLM-as-evaluator** is real but mostly invisible to users. Cognition has the most developed practice (and publishes about it). Superpowers exposes a two-stage subagent reviewer to the user. Factory ships Review and Test Droids which play partial judge roles. Nobody sells "the judge" as a primitive customers configure. Another whitespace zone.

- **Human role** clusters into three pitches: (a) **manager of an autonomous engineer** (Devin), (b) **author of well-formed tickets** (Factory, 8090, Superconductor), and (c) **enforcer of methodology with checkpoint reviews** (Superpowers). Our architecture choices imply different positions on this spectrum.

- **Pricing** ranges three orders of magnitude — $0 (Superpowers OSS) → $20/mo (Devin Core, Factory individual) → $200/seat + tokens (8090 Team) → $500/mo + ACUs (Devin Team) → $1M+/yr managed (8090). This corresponds to "self-serve methodology" vs "self-serve SaaS" vs "platform + services" — three distinct go-to-market shapes.

- **Multi-agent decomposition** is now table stakes at the top end: Factory's role-scoped droids, Superconductor's parallel CLI agents, Superpowers' subagent dispatch. Devin is the holdout single-agent pitch (though internally it's a hierarchy). Whatever architecture we pick, the "one model, one process" framing is increasingly off-market.

---

## Open follow-ups

- 8090's actual product surface is underdescribed in public material — only secondary-source coverage was available. Worth a direct demo or sales call for primary-source confirmation of whether they have a real scenarios/judge primitive or just a planning UI.
- Factory's Specification Mode docs are public at docs.factory.ai/cli/user-guides/specification-mode — a follow-up thread could fetch the full doc directly and extract their exact spec schema for direct comparison to our architecture proposals.
- Superpowers verification-before-completion SKILL.md should be read in full — it appears to be the closest open analog to a "judge" primitive in the set and is the simplest to lift conceptually.
- Cognition's "evaluating coding agents" blog is the single highest-value primary source on judge architecture across this competitive set; worth a dedicated read.
- Pricing figures here are from secondary sources; verify against each vendor's pricing page before quoting externally.
