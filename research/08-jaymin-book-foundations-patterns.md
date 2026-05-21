# 08 — Jaymin West, *Agentic Engineering* — Foundations (Ch. 1–5) + Patterns (Ch. 7)

**Round:** 2 — fanout `20260511-054258`, sub-01
**Date:** 2026-05-11
**Sources:** `jayminwest/agentic-engineering-book` (`main` branch), chapters 1–5 (`1-foundations`, `2-prompt`, `3-model`, `4-context`, `5-tool-use`) and chapter 7 (`7-patterns`, 11 sub-files).
**Out of scope for this report:** Ch. 6 (Harnesses), 8 (Practices), 9 (Mental Models), 10 (Toolkit) — owned by sub-09 and sub-12.
**Diff target:** [`00-comparison`](../architectures/00-comparison.md).

---

## 1. Worldview summary (one paragraph)

Jaymin West frames agentic engineering as a **five-pillar discipline** — **Prompt, Model, Context, Tool Use, Harness** — and then layers a Donella-Meadows-style **Twelve Leverage Points** hierarchy on top of those pillars, with the top four leverage points (ADWs, Templates, Plans, Architecture) explicitly identified as *structural* changes that cascade through the system, and the bottom four (Tools, Prompt, Model, Context) as *local fixes*. The guiding aphorism is **"one agent, one purpose, one prompt"**: focused agents outperform general agents, focused context outperforms long context, focused tools outperform sprawling toolboxes. Harness is treated as a *fifth pillar* that the original "core four" of agenticengineer.com missed, and Jaymin elevates it on the grounds that **`Agent = Model + Harness`** — without orchestration, safety, loop control, and tool dispatch, a model only produces text. The book's stance on hierarchy is empirical and recent: pre-2025 the model dominated; through 2024–2026 the frontier compressed (Claude 3.5 Sonnet, GPT-4o, Gemini 1.5 Pro all within reach of each other), and the *harness* now contributes the larger marginal gain. The Chapter 7 pattern catalog is openly pragmatic — patterns are "options with tradeoffs," not prescriptions — with **Plan-Build-Review as the explicit default** and the others framed as deviations to address specific limitations of that default (parallelism, iteration, learning, safety, context budget). Across all five chapters the book treats *measurement* (Husain's three-level eval hierarchy, "testing theatre" as named failure mode) and *learning* (self-improving prompts, Plan-Build-Improve as a learning loop) as first-class.

---

## 2. The Twelve Leverage Points of Agentic Coding (verbatim, with one-line glosses)

From `chapters/1-foundations/1-twelve-leverage-points.md`. Guiding philosophy: **"One agent, one purpose, one prompt."** Levels follow Meadows' inversion — *higher number = lower leverage = local fix; lower number = higher leverage = structural change*.

| # | Leverage Point | One-line gloss |
|---|---|---|
| 12 | **Context** | What does the agent actually know? Is the context window full of necessary tokens? |
| 11 | **Model** | What model is being used? What is the cost/speed/intelligence tradeoff? |
| 10 | **Prompt** | Are the instructions concrete and followable? Can the prompt actually be executed? |
| 9 | **Tools** | What actions can agents take, and in what form (internal vs. MCP vs. CLI)? |
| 8 | **Standard Out** | Can agents and operators *see* what is happening? Is output self-documenting? |
| 7 | **Types** | Is typing consistent and enforced? Are agents informed when they violate types? |
| 6 | **Documentation** | Can agents navigate, trust, and update the documentation? Is it self-improving? |
| 5 | **Tests** | Are tests helping agents, or is this "testing theatre"? Real tests vs. mock-heavy fakes. |
| 4 | **Architecture** | Is the codebase agentically intuitive? Does its shape match common patterns in training data? |
| 3 | **Plans** | Plans are MASSIVE prompts the agent can finish without further human input. |
| 2 | **Templates** | Do agents know what good output looks like? Are templates reusable and lean? |
| 1 | **ADWs (AI Developer Workflows)** | How does work *flow* between agents? The highest-leverage intervention in the framework. |

Jaymin also names **seven anti-patterns** that "corrupt" specific leverage points: **Isolated Prompting** (corrupts #12), **Tool Proliferation** (#9), **Testing Theatre** (#5), **Metric Over-Aggregation** (#5), **Design Delegation** (#3–#4), **Post-Hoc Learning** (#1), and **Automated Optimization Before Understanding** (#1–#2). The anti-pattern set is just as load-bearing as the leverage-point list itself: it names *where* practitioners trip up.

---

## 3. Chapter 7 patterns — paragraph each, with cross-reference to our `architectures/`

### 3.1 Plan-Build-Review (`7-patterns/1-plan-build-review.md`)
A three-phase workflow — Plan → Build → Improve — with an optional Research phase prepended for complex domains. Jaymin's strongest emphasis is the **Improve** phase, which closes a learning loop by updating the *Expertise* sections of the Plan and Build commands from production observations; this is what makes the pattern recurrently labeled "Plan-Build-Review" *and* "Research-Plan-Build-Improve" interchangeably. Jaymin makes it the *default*: "if you're unsure, start here." **Where it lives in our set:** This is the most pervasive shape across all four `architectures/`. Architecture 1's revelation cycle (probe → judge → diagnose → amend), Architecture 2's compound-engineering four-step (Plan → Work → Review → Compound), Architecture 3's six-phase Foundry, and Architecture 4's tournament generations are all Plan-Build-Review variants with different emphasis. Architecture 2's "Compound" step is the cleanest match to Jaymin's "Improve" — explicit knowledge accumulation back into prompts.

### 3.2 Self-Improving Experts (`7-patterns/2-self-improving-experts.md`)
A specialization of Plan-Build-Review where the Improve phase **rewrites the prompts themselves** — specifically the "Expertise" sections, while leaving the "Workflow" sections stable. Each command (`*_plan.md`, `*_build.md`) is split into a *mutable* Expertise block and an *immutable* Workflow block; only the former gets updated. Jaymin cites Nous Research's **Hermes Agent** as evidence the pattern has migrated from developer tooling to general-purpose personal agents (skills generate procedurally; consolidation runs out-of-band). **Where in our set:** This is the heart of [`02-compound-atelier`](../architectures/02-compound-atelier.md) — its "refresh skill" and `docs/solutions/` knowledge store are exactly the "Expertise" external storage Jaymin describes. The `00-comparison.md` v2 revision notes (line 17) explicitly mention "self-improving prompts (Klaassen's frustration-detector, Tedesco's Montaigne)" as a v1→v2 upgrade. Our F8 ("stale knowledge") row credits the Atelier as strongest here; Jaymin would agree but would push us to make the *mutable-vs-stable section split* explicit in our prompt templates, which our architecture specs do not yet require.

### 3.3 Orchestrator (`7-patterns/3-orchestrator-pattern.md`)
Hub-and-spoke: a Main Coordinator invokes specialized sub-agents (Scout → Planning Council → Build Agents → Review Panel → Validation), synthesizes their outputs, and manages workflow transitions. Jaymin's **load-bearing insight is "single-message parallelism"** — all parallel sub-agents must be invoked in *one* message for true concurrency; sequential messages serialize execution. **Where in our set:** Architecture 2's reviewer panel and Architecture 4's tournament are Orchestrator instances; Architecture 3's gate boards and Architecture 1's diagnostic role are weaker variants. None of our architectures currently calls out the *single-message* invariant explicitly. This is a concrete vocabulary borrow.

### 3.4 Autonomous Loops / Ralph Wiggum (`7-patterns/4-autonomous-loops.md`)
The canonical implementation is **`while :; do cat PROMPT.md | claude-code ; done`** — a fresh context window per iteration, with **git history as the only memory** and **failures committed as data**. Jaymin frames it as "the loop is the hero, not the model": 20 mediocre attempts inside the "smart zone" of 40–60% context fill outperform one perfect plan. Used for mechanical tasks with machine-verifiable completion criteria (migrations, coverage expansion, refactoring). **Where in our set:** Architecture 4's tournament generations *partially* implement this — each candidate runs fresh — but the Tournament's emphasis is *diversity* across candidates, not *persistence* across iterations on a single problem. The Ralph Wiggum pattern is **largely absent from our four architectures**, and is a strong candidate for adoption as an implementer-mode option inside Architecture 2's "Work" step or Architecture 3's Phase-3.5 construction.

### 3.5 ReAct (`7-patterns/5-react-pattern.md`)
Interleaved Reasoning + Action: `Thought → Action → Observation → Thought → ...`. Three properties earn its place: grounded decisions (no hallucinated retrievals), observable traces (post-hoc auditability), and adaptive behavior (each observation can redirect the plan). Jaymin frames ReAct as the right default for **exploratory and tool-heavy** tasks — debugging, codebase exploration, dynamic decisions — and explicitly *contrasts* it with Plan-Build-Review, which is the right default for tasks with well-defined specs. **Where in our set:** ReAct is the *micro-loop* inside every implementer agent in all four architectures (we just don't name it), but it is not invoked at the *methodology* level. Architecture 1's "probe brief" agent and Architecture 4's per-candidate run are the closest macro-level ReAct stances.

### 3.6 Human-in-the-Loop (`7-patterns/6-human-in-the-loop.md`)
Strategic insertion of human approval gates with a risk-based decision matrix (Reversibility × Blast radius × Cost × Sensitivity × Precedent). Jaymin's key constraint: "too few gates and you risk costly mistakes; too many and you've just built an expensive chatbot." Gate placement matters more than gate frequency. **Where in our set:** Every one of our four architectures has a human role and gates; the question of *where* gates go is treated differently in each (Refinery's classify-before-amend, Atelier's residual-work gate, Foundry's phase gates, Tournament's gallery-pick). Jaymin's risk matrix is a usable refinement — none of our architectures presents a structured *gate decision matrix*; we should adopt his Reversibility/Blast/Cost/Sensitivity/Precedent five-axis grid.

### 3.7 Progressive Disclosure (`7-patterns/7-progressive-disclosure.md`)
A three-tier context loading model: **(1)** Metadata index always resident (~1–5% of budget), **(2)** Full content loaded only when the index entry is selected (~10–30%), **(3)** Detailed resources fetched on-demand (unbounded). The pattern mirrors the human mental model of an encyclopedia: TOC in working memory, contents fetched on demand. Used to enable "effectively unlimited expertise within fixed context budgets." **Where in our set:** None of our four architectures currently formalizes context loading. `00-comparison.md` §4.1 lists "Trajectory capture" and "AGENTS.md / discoverability" as shared infrastructure but does not name a Progressive Disclosure tier. This is the most directly *liftable* primitive in the chapter — it cleanly fits the shared substrate.

### 3.8 Expert Swarm (`7-patterns/8-expert-swarm-pattern.md`)
A domain Expert Lead seeds a shared `expertise.yaml`, then dispatches *N* narrow workers that inherit it. Cited example: 10 parallel agents writing 3,082 lines across 20 files in ~4 minutes with consistent style because they share the same expertise file. Resolves the "generic orchestrators have parallelism but no domain context; domain experts have context but execute sequentially" tension. **Where in our set:** Architecture 4's diversity-policy population and Architecture 2's persona panel are *non*-swarm shapes — they deliberately reject inheritance for diversity. Architecture 3's phase-bound experts are sequential. Expert Swarm has no direct analog in our set and would be a meaningful addition for *consistency-critical* parallel work (doc generation, schema migrations, large refactors). It is the right shape for the "Atelier-issued parallel construction with shared style" use case.

### 3.9 Multi-Agent Collaboration (`7-patterns/9-multi-agent-collaboration.md`)
Orchestrated *real-time* collaboration ("party mode"): 2–3 selected agents respond *in character* in a single conversation, building on and disagreeing with each other while a human steers. Distinct from Orchestrator (sequential handoffs) and Expert Swarm (parallel but isolated). Jaymin emphasizes **role authenticity and genuine disagreement** — artificial consensus is the failure mode. **Where in our set:** None of our architectures use this pattern. The closest gesture is Architecture 2's panel-of-personas review, but our panel runs *post-hoc* on a finished workpad, not in a live conversation. Multi-Agent Collaboration could be a useful *upstream* pattern at brainstorm/plan time within any of the four architectures.

### 3.10 The Multi-Agent Landscape (`7-patterns/10-multi-agent-landscape.md`)
Less a pattern than a *map*: Jaymin codifies the 2026 protocol stack — **MCP** (agent-to-tool, vertical), **A2A** (agent-to-agent, horizontal), **ACP** (lightweight REST), **ANP** (decentralized W3C/DID) — and the three execution paradigms (**Handoff**, **Shared State**, **Async Mail/Hooks**) with framework evidence (AutoForge, LangGraph, ADK, Gas Town, Overstory). The "structured-communication trend" finding (JSON-RPC over natural language for inter-agent messages) is the load-bearing takeaway. **Where in our set:** `00-comparison.md` §8 names this gap explicitly: "MCP / tool ecosystem strategy — all four assume tooling exists; none specify how the factory exposes tools to agents." Jaymin's protocol-stack vocabulary fills that gap directly.

### 3.11 Production Multi-Agent Systems (`7-patterns/11-production-multi-agent-systems.md`)
Six production patterns for 10–30 parallel workers — Persistent Identity / Ephemeral Sessions, **Tiered Watchdog Chains** (Daemon → Triage → Patrol — i.e., mechanical → fast AI → strategic AI), Async Mail bus, resource-lifecycle discipline, work tracking, and integration via merge queue. Cited production evidence: **Gas Town** (Go) and **Overstory** (TypeScript/Bun). The "factories not workshops" framing — *any* station can break at any time, the system continues because failures are routine — is the chapter's worldview. **Where in our set:** This is the chapter that most directly diffs against [`00-comparison`](../architectures/00-comparison.md) §4.1 ("shared infrastructure"). Our §4.1 names worktree-per-unit, sandbox, stable IDs, manager loop, decision log; Jaymin's list adds **persistent agent identity**, **tiered watchdog**, **async mail bus**, and **resource lifecycle hygiene** — every one of which is missing or under-specified in our §4.1. The watchdog tier in particular (Daemon seconds → Triage seconds-to-minutes → Patrol minutes-to-hours) is more concrete than anything in our four architectures. Subagent 10's substrate audit of Overstory is the natural follow-up.

---

## 4. Three explicit agreements with [`00-comparison`](../architectures/00-comparison.md)

### Agreement 1 — Plan-Build-Review is the right default
Jaymin's Chapter 7 selection guidance is unambiguous: "if you're unsure, start with Plan-Build-Review." `00-comparison.md` §7.1 makes the analog recommendation by name: **"Pick Architecture 2 (Compound Atelier) as the working baseline,"** because the Atelier is precisely a Plan-Build-Review specialization with knowledge accumulation. Both documents argue from the same evidence base (Every.to compound-engineering plugin, Symphony) and reach the same default.

### Agreement 2 — Shared infrastructure is methodology-agnostic
Jaymin's pattern catalog repeatedly emphasizes that the *underlying* primitives (orchestrator coordinators, watchdog daemons, mail buses, worktrees) are reusable across patterns. `00-comparison.md` §4 takes the strongest possible version of this stance: **"The architecture is the methodology; the infrastructure is shared"** (line 176). The Production Multi-Agent Systems chapter (§7.11 above) names the same primitives our §4.1 names, with overlapping vocabulary (worktree per unit, async mail, manager loop). The two documents agree both in claim and in primitive list — modulo the gaps in §5 below.

### Agreement 3 — Diversity protects against single-prompt collapse
Jaymin's Orchestrator and Expert Swarm patterns explicitly call out multiple-perspective execution as the antidote to homogeneity. `00-comparison.md` §2.4 row F15 ("Single-prompt collapse") names this directly as a tracked failure mode and credits the Atelier's "six divergent frames" and the Tournament's "Diversity policy ≥4 scaffolds" as strongest coverage. The agreement is structural: both documents treat *prompt diversity* as a load-bearing engineering control, not a stylistic flourish.

---

## 5. Three explicit disagreements — where Jaymin would change a decision

### Disagreement 1 — Harness should be a named substrate primitive, not implicit
Our `00-comparison.md` §4.1 lists nine shared-infrastructure primitives, none of which is named "Harness." Jaymin's Chapter 1 elevates Harness to a *fifth pillar* on equal footing with Prompt/Model/Context/Tool-Use, with the formula **`Agent = Model + Harness`** and the historical claim that "harness quality is often the distinguishing factor — apparent model quality differences frequently resolve to harness design differences." If we adopt Jaymin's stance, §4.1 should be reframed: the nine primitives are *components of the harness*, the harness is the *named container*, and architecture choice becomes choice of *harness configuration*. This is more than a vocabulary change — it organizes our shared-infrastructure case in a way our v2 document does not.

### Disagreement 2 — ADWs (workflow-as-artifact) outrank single-issue queues
`00-comparison.md` §7.4 lists "Manager-loop / orchestrator with the 5-state queue or the manager_loop primitive" as the highest-priority infrastructure to build. Jaymin's Twelve Leverage Points puts **ADWs (#1) — "how does work *flow* between agents"** — at the very top of the leverage hierarchy, *above* templates, plans, and architecture. Jaymin's framing would imply the durable artifact is the *flow specification* (a versioned ADW document), not the *queue of issues* the flow operates over. Architecture 2's `STRATEGY.md` and Architecture 3's phase-contract files are gestures in this direction; Jaymin would push for an explicit `ADW.md` or `workflow.yaml` at the root of every project, on the same footing as `AGENTS.md`. None of our four architectures requires this.

### Disagreement 3 — Watchdog tiering is missing from our shared-infrastructure list
`00-comparison.md` §4.1 mentions "manager loop / orchestrator" once and does not differentiate failure-detection layers. Jaymin's Production Multi-Agent Systems chapter (§7.11) gives a three-tier model (**Daemon → Triage → Patrol**) with separate cadences (seconds → seconds-to-minutes → minutes-to-hours) and separate failure surfaces (process crashes → reasoning failures → strategic drift), supported by two production implementations (Gas Town in Go, Overstory in TS/Bun). Our four architectures have no equivalent of the *Daemon* tier — they all assume the manager loop's heartbeat is sufficient. Jaymin would (and the production evidence does) argue that conflating mechanical liveness with AI-driven supervision is exactly how 30-agent fleets fall over. We should adopt the Daemon/Triage/Patrol decomposition into §4.1.

---

## 6. Vocabulary uptake — terms to adopt verbatim

| Term | Definition (from book) |
|---|---|
| **Harness** | The execution environment that wraps the model — manages tool dispatch, context flow, safety enforcement, loop control. Without a harness, a model produces text; with a harness, it completes tasks. `Agent = Model + Harness`. |
| **ADW (AI Developer Workflow)** | A versioned, explicit specification of *how* work flows between agents. The #1 leverage point. Distinct from the *queue* of work items. |
| **Leverage Point (1–12)** | A ranked, Meadows-style intervention site in an agentic system. Lower number = structural change; higher number = local fix. Used to triage *where* to invest engineering effort. |
| **Testing Theatre** | Tests that execute correctly, produce numbers, and inform nothing — usually because their targets are wrong (generic benchmarks) or their resolution is too coarse (aggregate metrics hiding subtype regressions). Named anti-pattern on Leverage Point #5. |
| **Pit of Success** | A design stance that makes correct actions easier than incorrect actions. Cross-referenced from Foundations §"Common Mistakes" into Mental Models 9.1 (out of scope for this report). |
| **Single-Message Parallelism** | The discipline that *all* parallel sub-agent invocations must occur in one orchestrator message; sequential messages serialize execution regardless of agent design. |
| **Smart Zone** | The 40–60% context-window fill region where reasoning quality is empirically highest. Used to size Autonomous-Loop iterations. |
| **Ralph Wiggum** | The Autonomous Loop pattern — `while :; do cat PROMPT.md | claude-code ; done` — fresh context per iteration, git history as memory, failures committed as data. |
| **Expertise vs. Workflow sections** | Mandatory split inside Self-Improving Expert prompts: Expertise is *mutable* (updated by the Improve phase); Workflow is *stable* (defines the process). Updates only ever touch Expertise. |
| **Tiered Watchdog Chain (Daemon / Triage / Patrol)** | Three-tier supervision: Daemon (seconds, mechanical PID/tmux checks), Triage (seconds-to-minutes, fast AI classification), Patrol (minutes-to-hours, strategic AI sweep). Each tier watches the tier below it. |
| **Async Mail Bus** | Persistent message queue (typically SQLite-backed) decoupling agents — coordination overhead grows with team size but liveness survives crashes/restarts. |
| **Persistent Identity / Ephemeral Sessions** | Pattern decoupling agent *identity* (durable, lives in external storage) from agent *session* (disposable, dies when context fills). Solves model upgrades and crash recovery without losing accumulated expertise. |
| **Progressive Disclosure** | Three-tier context loading: metadata index always resident, full content on selection, supporting resources on-demand. Enables "effectively unlimited expertise within fixed context budgets." |
| **Protocol Stack (MCP / A2A / ACP / ANP)** | The 2026 inter-agent communication stratification — MCP for agent-to-tool, A2A for agent-to-agent, ACP for lightweight REST, ANP for decentralized DID-based discovery. |
| **Design Delegation** | Anti-pattern: an engineer defers architectural decisions to AI during implementation, then cannot write complete plans because the architecture was never consciously designed. Corrupts Leverage Points #3 and #4. |
| **Post-Hoc Learning** | Anti-pattern: engineers acquire AI tooling knowledge ad-hoc rather than through structured programs; point-tool knowledge accumulates without ADW design literacy. Corrupts Leverage Point #1. |

These 16 terms are recommended for direct verbatim adoption in our `architectures/` documents and any future v3 methodology document, where they fill gaps our current vocabulary does not. The first three (Harness, ADW, Leverage Point) should be promoted to *organizing* vocabulary — they restructure how the documents are written, not merely how they read. (`spec-driven-ai-dev.md` is a cataloged source — record [`3592091691`](../reference-only/3592091691/spec-driven-ai-dev.md), per issue [#105](https://github.com/lago-morph/software-factory/issues/105) — and is not amended directly; vocabulary adoption applies to project-authored documents.)

---

## 7. Book sections not directly readable

All requested chapter contents (1, 2, 3, 4, 5, 7) were successfully retrieved via `raw.githubusercontent.com`. The following limitations applied:

- **`api.github.com/repos/.../contents/...` directory-listing endpoints returned HTTP 403** from the sandbox (matching the PLAN.md §2.1 reachability table); chapter sub-file enumeration was therefore inferred from the *navigation tables and links inside `_index.md`* and from the verbatim catalog table in `chapters/7-patterns/_index.md`.
- **The book's live web view** (`jayminwest.com/agentic-engineering-book`) is 403-blocked from the sandbox (per PLAN.md §2.1) — I did not consult the web rendering and worked exclusively from the repository markdown sources.
- **For the foundations chapters (Ch. 2 Prompt, Ch. 3 Model, Ch. 4 Context, Ch. 5 Tool Use)** I read the `_index.md` files in full plus headline-level samples; the individual sub-files (e.g. `2-prompt/1-prompt-types.md`, `3-model/1-model-selection.md`, `4-context/2-context-strategies.md`, `5-tool-use/3-tool-restrictions.md`) were not exhaustively read. The §1 worldview synthesis and §6 vocabulary list rest on the index files plus the verbatim Twelve Leverage Points file; the §3 pattern reviews rest on the full pattern sub-files (1-plan-build-review through 11-production-multi-agent-systems).
- **Cross-chapter references that point into Ch. 6, 8, 9, 10** (e.g. links to `9-mental-models/1-pit-of-success.md`, `8-practices/2-evaluation.md`, `6-harnesses/_index.md`) were *not* followed — those chapters belong to sub-09 and sub-12.
- **Anti-pattern source footnotes [1]–[7]** (Liu, Husain, Willison) in the Twelve Leverage Points file were captured but not chased to their primary sources; those sources overlap heavily with the Round-1 corpus already digested in [`05-simon-willison`](05-simon-willison.md) and elsewhere.

No book section *intended* for this report was unreadable; the gaps above are deliberate scope-restrictions of this subagent's mandate.

---

*End of report — sub-agent 08, fanout `20260511-054258` sub-01, branch `claude/parallelize-with-subagents-SO0nR--sub-01`.*
