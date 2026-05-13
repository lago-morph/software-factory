# Research Report 12 — Adjacent Ecosystem and Vocabulary Cross-Check

**Date:** 2026-05-11
**Author:** Lead agent (lead-agent pass; the original subagent prompt in `research/PLAN.md` §3.5 covered more — specifically gastown / kotadb / pi-mono / Jaymin's Ch 10 toolkit — which still need a deeper read.)
**Status:** Capsule-quality on the six Tier-2 perspective pieces we fetched; the gastown / kotadb / pi-mono / Ch 10 reads are deferred.

## Sources reviewed

Status legend: ✅ full review (read end-to-end) · 🟡 reconstructed from search snippets / partial extraction · ⏳ retrieval pending · ❌ could not obtain.

| Source URL | Status | Notes |
|---|---|---|
| https://addyosmani.com/blog/agentic-engineering/ | ✅ | Fetched via issue #4 (182 KB). Primary source for §2.1. Read full article body. |
| https://www.langchain.com/blog/agentic-engineering-redefining-software-engineering | ✅ | Fetched via issue #4 (167 KB). Cisco/LangChain pilot study; primary source for §2.2. Read full article body including pilot numbers. |
| https://cloud.google.com/discover/what-is-agentic-coding | ✅ | Fetched via issue #4 (2.2 MB). Read the article body including the "Best practices for secure agentic coding workflows" checklist; primary source for §2.3. |
| https://www.ibm.com/think/topics/agentic-engineering | 🟡 | Fetched via issue #4 (253 KB) but the article body did not cleanly separate from the page navigation chrome in the html2text output. §2.4's findings are based on the navigation tree and the visible introductory framing only. A re-fetch with a different HTML extractor, or a manual read of the rendered page, would deepen this capsule. |
| https://kiro.dev/ | ✅ | Fetched via issue #4 (232 KB). Landing page only — subpages (`/docs/specs/`, `/docs/chat/autopilot/`, `/docs/steering/`) were NOT fetched. §2.5 explicitly flags that a focused audit of Kiro is still warranted. |
| https://deepwiki.com/All-Hands-AI/OpenHands/11.3-cli-and-deployment-modes | ✅ | Fetched via issue #4 (2.1 MB). Mostly consumed by report 11; §2.6 covers the residual that didn't fit there. |
| https://github.com/jayminwest/agentic-engineering-book/tree/main/appendices/examples/gastown | ❌ | Not read in this session. Original subagent prompt covered this — see §4 "What's left unanswered." Reachable via raw.githubusercontent.com; no fetch action needed. |
| https://github.com/jayminwest/agentic-engineering-book/tree/main/appendices/examples/kotadb | ❌ | Same as above. |
| https://github.com/jayminwest/agentic-engineering-book/tree/main/appendices/examples/pi-mono | ❌ | Same as above. |
| https://github.com/jayminwest/agentic-engineering-book/tree/main/chapters/10-practitioner-toolkit (Ch 10 sub-pages) | ❌ | Same — reachable via raw.githubusercontent.com. Ch 10 covers Claude Code, Google ADK, IDE Integrations, Agent Frameworks, Multi-Agent Workspace Managers, Enterprise Codebase Context Tools — each merits a capsule. |

**Primary sources** for the six §2 capsules are all ✅ except IBM (🟡). The ❌ items are deferred to the subagent 12-completion dispatch tracked in `research/PLAN.md` §10.4.

## 1. Framing

The Tier-2 pieces don't change architecture decisions but they harden vocabulary, surface one new concrete case study, and confirm that the *industry vocabulary is converging* on "agentic engineering" — exactly the framing this project is now built around. The pieces also reveal one genuinely new substrate candidate (Kiro) and one new control-plane reference architecture (Cisco/LangChain) that the Round-1 corpus did not cover.

## 2. Capsules

### 2.1 Addy Osmani — *Agentic Engineering* (2026-02-04)

The cleanest taxonomic argument in our corpus on **"vibe coding" vs. "agentic engineering."** Distilled:

| | Vibe coding | Agentic engineering |
|---|---|---|
| Defining stance | Prompt → accept → run → iterate by pasting errors. "Don't review the code." | Spec → direct → review → test → own the codebase. Discipline kept. |
| Where it works | Prototypes, MVPs, personal scripts, learning, brainstorm | Professional engineering at scale |
| Failure mode | "It demos great, then reality arrives." | "Different kind of hard — trading typing time for review time." |
| Skill prerequisite | Low (anyone can prompt) | High; "disproportionately benefits senior engineers" |
| Karpathy traceback | The original coinage (~Feb 2025) | His follow-up term (~Feb 3, 2026) |

Three direct quotes worth keeping:

- "AI didn't cause the problem; skipping the design thinking did."
- "The fundamentals matter more, not less."
- "The trajectory is clear: AI agents are getting more capable, and the agentic engineering workflow is becoming default for a growing number of professional developers. This is going to accelerate."

**Implication for our project:** the term *agentic engineering* is now industry-default with attribution to Karpathy; we should adopt it without further negotiation. Our four architectures all describe the agentic-engineering (not vibe-coding) end of the spectrum — the distinction makes our docs more legible.

### 2.2 Cisco / LangChain — *Agentic Engineering: How Swarms of AI Agents Are Redefining Software Engineering* (2026-04-17)

**The first concrete enterprise case study in our corpus with measured numbers.** Authored by Renuka Kumar (Principal SE Director) and Prashanth Ramagopal (Senior Director of Engineering) at Cisco, opining personally, published as a LangChain guest post.

**Architecture:** A two-tier control plane.

- **Worker Agents** — digital counterparts of individual engineers. Plan, gather context, execute, validate, report. Loosely coupled, horizontally scalable.
- **Leader Agent** — digital project leader. Provides shared prompt library, common tool gateway, long-term memory, global observability, orchestration. Separates *execution* from *coordination*.

Built on **LangGraph** (orchestration), **LangSmith** (observability + evals), **LangMem** (long-term memory). Worker agents talk to each other via the **A2A protocol**; AI coding agents (Codex / Claude) that don't speak A2A are bridged with an MCP adapter that routes their requests to the worker agent.

**Pilot results:** 70 unique users, 512 debug sessions in one month, 200+ engineer-hours saved.

- Debug workflow: **93% reduction** in time-to-root-cause vs. historical baseline.
- Development workflow: **65% reduction** in execution time.
- Notable finding: "the primary gains were not limited to faster code generation … but from compressing downstream workflows for functional testing after PR merge through coordinated agent execution. **PR review process itself became the bottleneck introduced by human-in-the-loop.**"

**Distinction the piece draws:** "AI coding agents excel at translating intent into code within a single user-driven session. Agentic engineering operates at a higher level of abstraction: it's a control plane that orchestrates cross-team workflows, maintains long-term memory across agents, and manages state and traceability across the full software delivery lifecycle." Coding agents like Codex/Claude run *inside* worker agents.

**Implication for our project:**

1. **The Worker + Leader two-tier architecture** maps almost exactly to our Architecture-2 (Compound Atelier) Operator + worker chain. Cisco's results are external validation of the pattern.
2. **A2A + MCP adapter** is a real wire protocol pattern for agent-to-agent comms. We should note it as a candidate for cross-cycle messaging if we ever exceed the single-orchestrator model.
3. **The PR-review-is-the-bottleneck finding** is empirical support for the architectures that move the human upstream (Architecture-1's spec author, Architecture-4's Geneticist) rather than gating at code review.

### 2.3 Google Cloud — *What is agentic coding?*

A polished enterprise explainer. Mostly definitional, but two parts are useful for our security and governance posture:

**Definition consistency check.** Their phrasing — *"agentic coding tools take a high-level instruction and execute it … function more like a skilled contractor than a passive consultant"* — matches our spec-driven baseline and Jaymin's harness definition.

**Best practices for secure agentic coding workflows** — a checklist of safeguards. Worth lifting into our `architectures/` security section:

- *Governance & scope control:* define scope and guardrails (no `DROP DATABASE`, no direct push to prod); strict dependency governance (no typosquat); proof-of-compliance audit trail.
- *Oversight & integration:* PR review required before merge; enterprise dashboards for usage quotas; monitor for new vulnerability classes (prompt injection, hallucinated code paths).
- *Testing & assurance:* red-team exercises; layered SAST + DAST.

**Direct hook into our failure-mode list:** F12 (lethal trifecta) and F19 (model-floor dependency) are visible in the prompt-injection and dependency-governance points respectively. F4 (code quality) is covered by the layered-testing point.

### 2.4 IBM Think — *What is agentic engineering?*

Mostly a navigation hub for IBM's Watson-orchestrated agentic content. The substantive page content (below the chrome) wasn't captured cleanly by our html2text path, but the nav tree itself is informative — IBM's taxonomy organizes agentic engineering under "AI agents → AI agent development → Agentic engineering," alongside *agentic coding* and *AgentOps* as siblings. The framing of **AgentOps** as a discipline distinct from coding is a useful organizing concept: AgentOps is to agentic engineering what DevOps is to software engineering.

**Verdict:** low-leverage on its own; revisit if we need a corporate-friendly definitions section. Not changing any architecture.

### 2.5 Kiro — *Bring engineering rigor to agentic development* (kiro.dev)

A potential substrate candidate we missed in Round 1. Kiro is **a spec-driven agentic IDE / CLI**:

- Natural prompt → structured requirements in **EARS notation** (a formal requirements syntax — directly relevant to our `spec-driven-ai-dev.md` baseline).
- Spec → architecture design → discrete task list → execution. Sounds very similar to Architecture-3 (Phase-Gated Foundry).
- **Autopilot mode** — long-running unattended tasks, user-in-control via approvals.
- Native MCP integration (remote + local).
- Steering files (`/docs/steering/`) for project-level + global behavior — the same idea as AGENTS.md / CLAUDE.md but with a vendor-curated convention.
- Models: Claude Sonnet 4.5 or Auto-routing across frontier models.
- VS Code compatible (Open VSX plugin ecosystem).
- CLI install via `curl … cli.kiro.dev/install | bash` — has a CLI surface.

**Verdict:** **worth a focused substrate audit in a future round.** Kiro's emphasis on EARS-notation requirements, executable specs, and explicit phase progression (requirements → design → tasks → execution) makes it a near-peer of our Architecture-1 (Specification Refinery) and Architecture-3 (Phase-Gated Foundry) — but as a *product*, not as a methodology. Two questions worth answering:

1. Does Kiro's spec → design → tasks → execution loop satisfy the layered-spec discipline of our Architecture 1, or does it conflate layers?
2. Is Kiro's CLI invocable from CI in a headless-like mode? (Their landing page emphasizes terminal/IDE; CI-friendliness is not stated.)

### 2.6 DeepWiki — *OpenHands CLI & Deployment Modes*

Already digested in report 11. Two pieces of information unique to DeepWiki that didn't make it to the official docs:

- The complete `V0 Legacy / V1` architectural split is mapped in the wiki TOC. Important because the SDK paper says V1 was a "complete architectural redesign" — the wiki gives us the layer-by-layer fingerprint.
- The presence of sections like `Sandbox Specification Service` and `Conversation Storage and V0/V1 Dual Path` confirms that OpenHands is currently shipping *both* the V0 and V1 implementations — the V0 surface is legacy but not deleted. Anyone embedding OpenHands needs to pick V0 or V1 explicitly.

## 3. Vocabulary uptake

These terms now have multi-source attribution and should be used consistently across our docs:

| Term | Source / origin | Use |
|---|---|---|
| **Agentic engineering** | Karpathy (Feb 2026), broadly adopted | The umbrella term for disciplined agent-assisted dev. Use this; retire "AI-assisted engineering" as an alias. |
| **Vibe coding** | Karpathy (Feb 2025) | The *undisciplined* end of the spectrum. Useful as a contrast term, not a positive descriptor. |
| **Worker agent / Leader agent** | Cisco / LangChain | A clean naming for the two-tier control plane. Our existing Operator/Implementer pattern aligns. |
| **A2A protocol** | LangChain ecosystem | Agent-to-agent wire protocol. Note for future cross-cycle messaging. |
| **AgentOps** | IBM Think | The operations discipline around agentic systems. Useful for the "production" section of our architectures. |
| **Harness** | Jaymin / Fowler / Mollick / Raschka / Schmid / Hashimoto (Apr 2026 consensus) | The runtime layer between model and useful work. Covered in `research/09-...` (this round). |
| **EARS notation** | Kiro / standard requirements engineering | A formal pattern for acceptance criteria — directly substitutable for our Given/When/Then if we want stricter rigor. |

## 4. What's left unanswered

The original subagent prompt for this position (PLAN §3.5) called for:

1. ✅ Skim of Jaymin Ch 10 (Practitioner Toolkit): **deferred** — Ch 10 sub-pages live at `chapters/10-practitioner-toolkit/`, fetchable via raw.githubusercontent.com.
2. ❌ Capsule of `appendices/examples/gastown` — not yet read.
3. ❌ Capsule of `appendices/examples/kotadb` — not yet read.
4. ❌ Capsule of `appendices/examples/pi-mono` — not yet read.

These three are the named exemplars in Jaymin's book — gastown specifically came up in `research/07-dark-factory.md`. A short read of their `_index.md` files in a future pass would close this loop. Cost: ~30 min of agent time.

---

# Round-2 sub-04 completion (appended 2026-05-11)

The sections below close out the gastown / kotadb / pi-mono / Chapter 10 capsules that were deferred in v0.1. All content fetched from `raw.githubusercontent.com/jayminwest/agentic-engineering-book/main/...` on 2026-05-11. Section numbering continues from §2.6 (last Tier-2 capsule); §3 reframes the section index away from the v0.1 `## 3. Vocabulary uptake` / `## 4. What's left unanswered` headings — those sections are preserved verbatim above, but the prompt's required section numbers (3 Gastown, 4 Kotadb, 5 Pi-mono, 6 Ch 10, 7 final summary) are answered as §A.3 through §A.7 below to avoid duplicating heading numbers.

## A.3 Gastown capsule

**Source:** `appendices/examples/gastown/_index.md` (the book's case-study chapter) + cross-references to `github.com/steveyegge/gastown`.

**Problem solved.** Gas Town is a **multi-agent workspace manager**: a system for running 20–30 parallel AI coding agents on real software projects with persistent identity, structured work decomposition, automated merge coordination, and supervisory recovery from individual agent failures. Steve Yegge built it as a production-scale answer to the question "what happens when you try to run more concurrent agents than a single human can supervise interactively?" The system's distinguishing concerns are persistence across context exhaustion, evidence-based capability routing, and a quality gate that prevents low-quality code from reaching `main`.

**License + maturity.** MIT license; Go (~189K LOC); 9,000+ GitHub stars; two production binaries (`gt` workspace manager, `bd` git-backed issue tracking). As of early 2026: production-capable but **not production-proven at scale across diverse organizations** — primarily validated by Yegge's own team, Go-centric, and accessible only to well-funded teams (~$100/hour in token cost). The book explicitly flags PRs sometimes needing human cleanup, offsetting some productivity gains.

**Architectural pattern compared to our four architectures.** Gas Town is best read as a **substrate** (a workspace + orchestration layer), not a methodology. Mapped against our architectures:

| Our architecture | Gas Town overlap | Gap |
|---|---|---|
| 1 — Specification Refinery | Weak — Gas Town does not enforce layered specs; humans design at the Formula level and the system instantiates Protomolecules. No analog to layered acceptance criteria. | Refinery's spec layers are not in Gas Town's vocabulary. |
| 2 — Compound Atelier | **Strong** — Mayor ↔ Operator, Polecat ↔ worker, Witness ↔ reviewer, Refinery ↔ residual gate. Convoy + Beads ↔ Atelier's queue and workpad. Five design axioms (Attribution, Work-as-Data, History, Scale, Verification-over-Trust) map almost line-for-line onto Atelier's discipline. | Atelier's *knowledge accumulation* (Compound plugin, `docs/solutions/`) is not a first-class Gas Town primitive — CVs accumulate but only per-agent, not per-pattern. |
| 3 — Phase-Gated Foundry | Moderate — molecules are explicit step sequences with `bd close <step> --continue`; the Batch-Closure Heresy enforces phase ordering. But there's no defect-of-origin attribution practice. | Foundry's audit-trail-as-product is partially present (Beads is the audit trail), but no upstream-defect classification. |
| 4 — Evolutionary Tournament | Weak — no parallel-variants-then-select pattern. The "swarm" is parallel work on *different* tasks, not parallel attempts at the *same* task. | Tournament's adversarial logic is absent. |

**Direct architectural primitives we could borrow.** From Gas Town specifically:

1. **GUPP (idle agent = system failure).** A scheduling discipline rather than an architecture choice — but it changes how queue depth is monitored. If we adopt it: empty queues trigger investigation, not celebration.
2. **Refinery as a dedicated merge-queue agent.** Direct substitute for our §4.1 "shared infrastructure" merge-discipline item. Re-imagination (when conflicts are complex, re-implement against updated main) is a non-trivial capability not present in our current architectures.
3. **Persistent identity + ephemeral session.** Substitutes for our "trajectory capture" infrastructure goal — a CV-per-agent is a cheaper, more legible form of trajectory capture than a CXDB-style turn DAG.
4. **Seancing.** Targeted retrieval from per-agent persistent state. Useful primitive for our "manager-loop survives across sessions" requirement.

**Would adopting it move a decision in `architectures/00-comparison.md` §7?**

- **§7.1 (recommended starting path: Architecture 2 Atelier).** **No change** — Gas Town *strengthens* the case for Atelier by providing an external production-scale validation of the pattern. Mayor/Polecat/Witness/Refinery is the Operator/Worker/Reviewer/Gate pattern.
- **§7.2 (selective borrows).** **Add a fifth borrow**: from Gas Town, adopt the Refinery merge-queue pattern and the persistent-identity/ephemeral-session separation. Both fit cleanly into Atelier's existing primitives without requiring the full Gas Town stack.
- **§7.3 (full-architecture adoption contexts).** **No change.**
- **§7.4 (build the shared infrastructure first).** **Strengthens the argument.** Gas Town's success rests on its substrate (workspace isolation, typed mail, Beads). Our §7.4 already says "infrastructure first"; Gas Town is direct evidence.

**Verdict:** Gas Town does not change the *choice* of recommended architecture, but it is the strongest external candidate to be the *substrate underneath* it. It deserves a full substrate audit in a future round, alongside Overstory and OpenHands. (Sub-02 covers Overstory in this round; sub-03 covers OpenHands; Gas Town belongs in the same comparison row.)

## A.4 Kotadb capsule

**Source:** `appendices/examples/kotadb/CASE_STUDY.md` plus the embedded `.claude/` configuration documented inline.

**Problem solved.** KotaDB is an **HTTP API service for code indexing** (Bun + TypeScript + Supabase) — but the book treats it as a case study **of agentic-engineering patterns in production**, not of code indexing per se. The interesting artifact is the `.claude/` directory: 90+ slash commands, 4 specialized agents (scout, build, review, orchestrator), 7 domain experts each with plan/review/improve commands, and a machine-readable `agent-registry.json` providing capability/model/tool indexes.

**License + maturity.** The book frames KotaDB as a "mature implementation of agentic engineering patterns" — no explicit license is quoted in the case study, but the `.claude/` configuration is the reusable artifact (the codebase itself is product). Maturity is structural: it implements Ch. 6.1–6.3 patterns end-to-end with explicit anti-pattern avoidance.

**Architectural pattern compared to our four architectures.** KotaDB is a near-perfect **Compound Atelier** implementation with a layer of **Phase-Gated Foundry** rigor on top:

| KotaDB component | Maps to |
|---|---|
| 5-phase workflow (Scout → Plan → Build → Review → Validate) | Atelier's Operator + worker + reviewer pipeline; Foundry's phase gates |
| `docs/specs/<name>.md` as shared artifact through all phases | Architecture-1 (Refinery)-style spec-as-source; **`STRATEGY.md`** in our `architectures/01-specification-refinery.md` |
| Single-message parallelism for build agents (`Use Task tool — multiple calls in SINGLE message`) | Atelier's parallel worker dispatch |
| Tool-restricted scout (read-only) + tool-restricted orchestrator (no Edit/Write/Bash) | Capability minimization — `architectures/00-comparison.md` §4.1 sandboxed-execution + capability-scoping |
| 7-expert planning council + review panel with explicit aggregation rules | **Compound Engineering's 14-review-agent army** from `research/03-every-compound-engineering.md`, in production. |
| Self-improving expert commands (PRESERVE / APPEND / DATE / REMOVE rules) | Architecture-2's knowledge-accumulation loop (`docs/solutions/` analog) |
| Model tier assignment (haiku scout/review, sonnet build, opus orchestrator) | Cost discipline absent from our four architectures — a useful borrow |
| `agent-registry.json` with capability/model/tool indexes | New primitive — not in any of our four architectures |

**Direct architectural primitives we could borrow.**

1. **`docs/specs/` + `docs/reviews/` as the durable artifacts that survive phases.** Concrete file-system convention for the Atelier-style shared workpad.
2. **Phase-gate prerequisite checks** (`test -f {spec_file_path}` before build). A simple, mechanical Foundry-style gate that doesn't require a full audit-trail product.
3. **The `*_improve` self-improvement command pattern.** Codified rules — PRESERVE existing patterns unless obsolete, APPEND new learnings, DATE entries with commit references, REMOVE only with multi-implementation evidence — directly executable. Our `architectures/02-compound-atelier.md` describes this loop conceptually; KotaDB shows what the command file looks like.
4. **The `agent-registry.json` capability index.** Dynamic agent selection instead of hardcoded routing. Particularly valuable when the agent inventory grows past ~5.
5. **Output discipline (forbidden meta-commentary patterns).** Eliminates "Based on the changes..." / "Here is the..." preambles. Useful for any agent whose output is piped into another agent.

**Would adopting it move a decision in `architectures/00-comparison.md` §7?**

- **§7.1.** **No change** — KotaDB is itself a Compound Atelier implementation; it confirms §7.1 rather than challenging it.
- **§7.2.** **Add to the "from Architecture 1" borrow**: KotaDB shows that the layered-spec discipline doesn't require a whole methodology — a single `docs/specs/<name>.md` artifact threaded through phases is enough. **Add a "from KotaDB" borrow**: self-improvement command pattern with PRESERVE/APPEND/DATE/REMOVE rules; capability registry.
- **§7.4.** **Strengthens.** The agent-registry.json + scoped tool matrices are direct examples of what §7.4's "stable-ID enforcement and a cross-artifact RTM-equivalent" can look like in practice.

**Verdict:** KotaDB is **not a substrate** (it's a project's `.claude/` configuration, not a runtime) — but it is the highest-fidelity reference implementation of the Atelier pattern we have seen and probably the single most copy-pasteable artifact in the entire Round-2 corpus. Worth a *configuration audit* (not a substrate audit) in a future round to catalogue every command + agent file as a candidate for our own factory.

## A.5 Pi-mono capsule

**Source:** `appendices/examples/pi-mono/_index.md` (the book's case study of the Pi monorepo agent toolkit by Mario Zechner / libGDX creator).

**Problem solved.** Pi-mono is the case study of **Pi**, a TypeScript monorepo agent toolkit that takes the opposite stance from Claude Code, Gas Town, and Overstory: instead of bundling orchestration, permissions, plan mode, sub-agents, MCP, and to-do lists into the product, the core remains minimal and **every behavior is an extension**. The framework's design philosophy: "the core remains minimal, every behavior is an extension, and the framework exists to enable customization rather than to encode it." Pi deliberately rejects: MCP protocol support in core, sub-agent spawning in core, permission popups, plan mode, to-do lists in core.

**License + maturity.** MIT license; ~15,900 GitHub stars; created by Mario Zechner (libGDX maintainer). Maturity: extension system is non-trivial (20+ lifecycle hooks from `session_start` through `session_shutdown`), and 25+ LLM providers are unified behind one interface — uniquely among compared frameworks, Pi supports provider-switching mid-conversation via a serializable context.

**Architectural pattern compared to our four architectures.** Pi-mono is a **substrate philosophy choice**, not a methodology. Mapped:

| Our architecture | Pi-mono compatibility |
|---|---|
| 1 — Specification Refinery | Compatible if you write a spec-management extension; no built-in spec primitives. |
| 2 — Compound Atelier | Compatible — extensions can implement queue, workpad, reviewers. But the Atelier's "knowledge accumulation across sessions" requires writing a memory extension. |
| 3 — Phase-Gated Foundry | Compatible — lifecycle hooks give you phase boundaries for free. Audit trail requires an extension. |
| 4 — Evolutionary Tournament | Compatible — provider abstraction is actually a *help*; you can run tournament variants across different models trivially. |

**Direct architectural primitives we could borrow.**

1. **Lifecycle hooks as the integration surface.** Pi's 20+ hooks (`session_start`, `before_tool_call`, `after_tool_call`, `compaction`, `session_shutdown`, etc.) are a clean event model. Our `architectures/00-comparison.md` §4.1 calls for "trajectory capture" and "manager-loop / orchestrator"; lifecycle hooks are how you wire those without coupling them to a specific runtime.
2. **Serializable context enabling provider switching.** Useful for cost-discipline and for the Tournament architecture's per-variant model assignment.
3. **`steer()` (interrupts after tool calls) and `followUp()` (queues messages for next turn).** Concrete primitives for the human-in-the-loop interruption modes we've left under-specified.
4. **Unified `AGENTS.md` for humans and agents.** Reinforces Simon Willison's `AGENTS.md` preference noted in §8 of `architectures/00-comparison.md`.

**The trust-model concern.** Pi's no-permission-system stance ("the user launched the agent, the agent should do its job") is **incompatible with most of our four architectures' security posture**, which assume capability-scoped sandboxes and PR-gated merges. Adopting Pi would mean either (a) writing a permission extension or (b) accepting Pi's stance and relying on user extension selection for safety. The book itself flags this honestly: "only install extensions you trust."

**Would adopting it move a decision in `architectures/00-comparison.md` §7?**

- **§7.1.** **No change** — Pi is a substrate, not an architecture; choice of methodology unaffected.
- **§7.2.** **No change.**
- **§7.4 (infrastructure first).** **Subtle change.** Pi-mono is evidence that the §7.4 infrastructure layer can be assembled from a hook-based extension system rather than from a hard-coded runtime. **If we build our own substrate, a Pi-style lifecycle-hook surface is a strong candidate for the architecture.** That said, the no-permission-system stance is a hard tradeoff — we would have to write the permission extension ourselves, which negates the simplicity argument for adopting Pi wholesale.

**Verdict:** Pi-mono is **the conceptual counterweight** to Gas Town/Overstory's batteries-included substrates. Both directions are viable; the choice is about whether we want to *configure* a vendor's opinions or *encode* our own. Worth a focused read in a future round only if we decide to build a custom substrate rather than adopt OpenHands/Overstory/Gas Town wholesale. It does not deserve a full substrate audit *unless* that build-our-own decision is made.

## A.6 Jaymin book Chapter 10 — Practitioner Toolkit

The chapter is a tool catalog organized by category, with operational rather than evaluative framing ("what works, what doesn't, and patterns discovered through production use"). Capsules below; final column is our "should we look harder?" verdict.

### A.6.1 Claude Code (Anthropic CLI coding agent)

**What the chapter says.** Claude Code is "a programmable orchestrator, not just a chatbot that writes code." Subagent system with context isolation + parallelization. Agent teams (experimental) for peer-to-peer coordination. Five coordination patterns: Leader-Worker, Swarm, Pipeline, Council, Plan Approval. Skills system with progressive disclosure. `.claude/rules/` for path-scoped behavioral config. Real-time message steering. Hot-reload for Skills. Hooks. **Key quote:** "the harness can often be the distinguishing factor" separating model capability from product performance.

**Mapped to our architectures.** Claude Code is the de-facto substrate underneath Compound Atelier (it powers Every.to's compound-engineering plugin), the Refinery (it can host the spec → review → implement loop), the Foundry (hooks + Skills give you phase gates), and the Tournament (Task tool gives you parallel variants).

**Should we look harder?** **Already covered** in `research/09-jaymin-book-harnesses-practices-mental-models.md`. No additional dispatch needed.

### A.6.2 Google ADK (Agent Development Kit)

**What the chapter says.** Code-first framework with multi-agent coordination as core. **Workflow primitives** (SequentialAgent, ParallelAgent, LoopAgent) handle deterministic orchestration *without* LLM calls — "when your orchestration logic is deterministic, don't pay for intelligence you don't need." State persistence with lifecycle-aware prefixes (`session:`, `user:`, `app:`, `temp:`). Bidirectional MCP. Framework interop wrappers for LangChain and CrewAI. Production-ready for Google Cloud users; outside that ecosystem DX is still maturing. Common gotchas: asyncio requirements, env-var naming conflicts, stateful MCP connections limiting horizontal scaling.

**Mapped to our architectures.** ADK's SequentialAgent + ParallelAgent + LoopAgent is the **deterministic-orchestration primitive** that all four of our architectures need but none specify. The lifecycle-prefixed state model (`session:`, `user:`, `app:`, `temp:`) is the workpad-vs-knowledge-base distinction made concrete.

**Should we look harder?** **Yes, but light.** A focused read of ADK's workflow-primitives docs would harden the §4.1 manager-loop/orchestrator requirement. Not a full substrate audit — ADK is GCP-coupled enough that adoption is unlikely outside a GCP-native deployment — but the *concepts* (workflow agents, lifecycle-prefixed state) are portable. Half-day's work.

### A.6.3 IDE Integrations (Cursor, Windsurf, Copilot, Continue.dev, JetBrains AI, Aider)

**What the chapter says.** Three approaches: extension-based (Copilot, Continue.dev, JetBrains AI), fork-based (Cursor, Windsurf), CLI (Aider). Cursor is the industry standard; Composer runs at "~2x the speed of Claude 3.5 Sonnet." Windsurf differentiates via external integrations (GitHub/Slack/Figma) and autonomous memory persistence. GitHub Copilot's Coding Agent operates in "ephemeral CI environments to generate pull requests." Continue.dev for air-gapped. JetBrains AI uses IDE-native static analysis. Aider is terminal-native + git-centric + model-agnostic. **Verdict:** tools are "not mutually exclusive" — match tools to tasks.

**Mapped to our architectures.** IDE integrations are **complementary** to all four architectures, not substitutes. They live on the human side of the human-agent boundary — the human's editing environment — while our architectures live on the factory side. The exception: Copilot's Coding Agent in ephemeral CI environments is a degenerate version of Gas Town/Overstory's workspace-manager model.

**Should we look harder?** **No.** IDE integrations are an input to the human side of the loop; they don't change factory design. Brief mention in our docs for completeness; no audit.

### A.6.4 Agent Frameworks (LangGraph, CrewAI, Microsoft Agent Framework, Claude Agent SDK)

**What the chapter says.** **LangGraph** is the production leader for complex workflows ("reached v1.0 as first stable major release"; Uber/LinkedIn/JP Morgan). Best for deterministic branching logic with durable state. **CrewAI** dominates rapid prototyping; "executes 5.76x faster than LangGraph in certain task types"; "60% Fortune 500 adoption." **Microsoft Agent Framework** consolidates Azure (merged AutoGen; AutoGen now in maintenance); SOC 2/HIPAA native. **Claude Agent SDK** prioritizes tool-native autonomy without multi-agent complexity — "the agent harness powering Claude Code." **Selection rule:** framework choice depends on *deployment environment tier* before any technical choice. **Emerging category:** persistent personal runtimes (Nous Research's Hermes Agent) addressing continuity rather than orchestration topology.

**Mapped to our architectures.** LangGraph is the Cisco/LangChain pilot's substrate (§2.2 above). CrewAI's role-based teams overlap with Compound Atelier's persona pattern. Claude Agent SDK underlies Claude Code (§A.6.1).

**Should we look harder?** **LangGraph — yes, light.** Cisco's pilot results (§2.2) are an external validation of LangGraph's production fitness; a focused read of LangGraph's durable-state and human-in-the-loop primitives would harden our Architecture-2 implementation. **CrewAI — no, but keep in vocabulary.** **Microsoft Agent Framework — no** (Azure-coupled; unlikely substrate). **Claude Agent SDK — already covered** in `research/09-...`.

### A.6.5 Multi-Agent Workspace Managers (Gas Town, Overstory)

**What the chapter says.** Workspace managers are infrastructure for orchestrating 10–30+ concurrent coding agents — solving coordination problems "that single-agent tools and frameworks cannot handle at scale." Compared to Docker:VMs. **Gas Town** (Go, MIT, Yegge, Dec 2025) — git worktrees for isolation, beads for state, external daemon (Mayor) for coordination, 20–30 agents, ~$100/hour, automated merge queue with AI-assisted conflict resolution. **Overstory** (TypeScript/Bun, MIT, Feb 2026) — zero runtime deps, session-as-orchestrator model (your active Claude Code session coordinates workers), 4-tier merge escalation (Clean → Auto → AI → Re-Imagine), better fit for 10–15 agents. **Good fit:** 10–30 parallel agents, complex merge coordination, regulated environments, long-running projects. **Poor fit:** 1–5 agents, small projects, early-stage practitioners, cost-sensitive work.

**Mapped to our architectures.** Both are direct substrate candidates for Compound Atelier. The book explicitly positions them as the *infrastructure layer*, not the methodology — which exactly matches our §7.4 framing.

**Should we look harder?** **Gas Town — yes, full substrate audit** (see §A.3 verdict). **Overstory — already in progress** (sub-02 of this fanout).

### A.6.6 Enterprise Codebase Context Tools (Aider Repo Map, Augment, Sourcegraph Amp, Continue.dev, Qdrant+tree-sitter, hierarchical CLAUDE.md, ADRs as context, Serena MCP, Cognition Devin, Tabnine Enterprise)

**What the chapter says.** Survey of 9 tools organized around **7 durable patterns** rather than vendor offerings. Author's thesis: "the patterns documented in Context at Codebase Scale are durable; the specific products that implement those patterns are not." Patterns: semantic indexing (Aider Repo Map, Augment, Sourcegraph Amp, Continue.dev, Qdrant+tree-sitter); hierarchical navigation (CLAUDE.md files); ADRs as context (plain markdown); LSP-backed dependency navigation (Serena MCP); retrospective documentation in legacy systems (Cognition Devin); graduated adoption / air-gapped (Tabnine Enterprise). **Universal recommendation:** nested CLAUDE.md files across all strategies — "they capture what semantic search cannot infer." **Honest gaps:** (1) no tool filters PII at indexing time; (2) cross-language dependency tracing remains unsolved; (3) cost models for high-frequency agent loops are underdocumented.

**Mapped to our architectures.** Context tools are **shared infrastructure** (§4.1 row). The chapter's "patterns are durable; products are not" framing exactly matches our `architectures/00-comparison.md` §7.4 "build the infrastructure first" stance.

**Should we look harder?** **Patterns — yes, light** (a half-page borrow of the 7-pattern taxonomy into our `architectures/00-comparison.md` §4.1). **Specific products — no audit needed.** ADRs-as-context is the cheapest, highest-leverage practice and we should adopt it explicitly. (Project already uses ADRs — see `adr` skill.)

## A.7 Final two-line summary

Of all items reviewed (six Tier-2 perspective pieces in §2 plus gastown/kotadb/pi-mono/Ch10 in §A): **Gas Town deserves a full substrate audit** in a future round (alongside Overstory and OpenHands — the three workspace-manager candidates should be diffed head-to-head); **KotaDB deserves a configuration audit** (its `.claude/` is the most copy-pasteable reference we have for the Atelier pattern); **Kiro** (from §2.5) deserves a focused product audit since its EARS-notation spec discipline is a near-peer of our Architecture 1. **Pi-mono, ADK, LangGraph, and the Ch 10 context-tool patterns** warrant only light reads — concept borrows, not full audits — unless we decide to build our own substrate (in which case Pi-mono's hook surface and ADK's workflow primitives become primary references).

---

*End of report 12 — `research/12-adjacent-ecosystem.md` v0.2 (sub-04 completion)*
