# Research Report 12 — Adjacent Ecosystem and Vocabulary Cross-Check

**Date:** 2026-05-11
**Author:** Lead agent (lead-agent pass; the original subagent prompt in `research/PLAN.md` §3.5 covered more — specifically gastown / kotadb / pi-mono / Jaymin's Ch 10 toolkit — which still need a deeper read.)
**Status:** Capsule-quality on the six Tier-2 perspective pieces we fetched; the gastown / kotadb / pi-mono / Ch 10 reads are deferred.
**Primary sources (fetched 2026-05-10):**
- `addyosmani.com/blog/agentic-engineering/` — Addy Osmani's framing piece, *Feb 4, 2026*
- `cloud.google.com/discover/what-is-agentic-coding` — Google Cloud explainer
- `www.ibm.com/think/topics/agentic-engineering` — IBM Think reference
- `www.langchain.com/blog/agentic-engineering-redefining-software-engineering` — Cisco/LangChain pilot study, *April 17, 2026*
- `kiro.dev/` — Kiro IDE landing page
- `deepwiki.com/All-Hands-AI/OpenHands/11.3-cli-and-deployment-modes` — third-party wiki (consumed mostly by report 11)

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

*End of report 12 — `research/12-adjacent-ecosystem.md` v0.1*
