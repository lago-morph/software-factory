# Research Report 09 (Partial) — Jaymin West: Harnesses

**Date:** 2026-05-11
**Author:** Lead agent
**Status:** **Partial.** Original subagent prompt in `research/PLAN.md` §3.2 covered Chapter 6 (Harnesses), Chapter 8 (Practices), and Chapter 9 (Mental Models). This pass covers **only Chapter 6's index page** at full fidelity, because that's the page we fetched. The seven sub-pages of Ch 6 (1-what-is-a-harness through 7-designing-for-your-context) and all of Ch 8/9 are still pending. They are all reachable from the sandbox via `raw.githubusercontent.com` and can be read directly without needing the fetch action — a future agent can dispatch the original subagent prompt against the remaining files without further fetch ceremony.

## Sources reviewed

Status legend: ✅ full review (read end-to-end) · 🟡 reconstructed from search snippets / partial extraction · ⏳ retrieval pending · ❌ could not obtain.

| Source URL | Status | Notes |
|---|---|---|
| https://www.jayminwest.com/agentic-engineering-book/6-harnesses | ✅ | Fetched via issue #4 (113 KB rendered HTML → markdown). The index page of Ch 6. **This is the entire substantive source for this report.** Every chapter section described in this report is the chapter's *summary* of that section — not the section itself. |
| https://www.jayminwest.com/agentic-engineering-book/6-harnesses/1-what-is-a-harness | ❌ | Not yet fetched. Has the full text behind §1 "What Is a Harness?" — currently only the index-level one-paragraph summary is captured in this report. |
| https://www.jayminwest.com/agentic-engineering-book/6-harnesses/2-harness-stack | ❌ | Not fetched. Behind §5 of this report; Raschka's six-component breakdown is named but its depth lives here. |
| https://www.jayminwest.com/agentic-engineering-book/6-harnesses/3-harness-categories | ❌ | Not fetched. Mollick's 3-axis stack + capability tiers + decision table all live here. |
| https://www.jayminwest.com/agentic-engineering-book/6-harnesses/4-harness-as-control-system | ❌ | Not fetched. Behind §6 of this report; Fowler's full guides-and-sensors decomposition lives here. |
| https://www.jayminwest.com/agentic-engineering-book/6-harnesses/5-harness-engineering | ❌ | Not fetched. Behind §7 of this report; Hashimoto's six-step loop + failure taxonomy live here. |
| https://www.jayminwest.com/agentic-engineering-book/6-harnesses/6-security-permissions-trust | ❌ | Not fetched. Behind §8 of this report; the full permission/sandbox/trust treatment lives here. |
| https://www.jayminwest.com/agentic-engineering-book/6-harnesses/7-designing-for-your-context | ❌ | Not fetched. The four design questions and decision tree live here. |
| https://www.jayminwest.com/agentic-engineering-book/8-practices (all 7 sub-pages) | ❌ | Not fetched. Practices chapter (Debugging, Evaluation, Cost & Latency, Production, Workflow Coordination, Knowledge Evolution, Operating Agent Swarms). All reachable via `raw.githubusercontent.com/jayminwest/agentic-engineering-book/main/chapters/8-practices/*`. |
| https://www.jayminwest.com/agentic-engineering-book/9-mental-models (all 7 sub-pages) | ❌ | Not fetched. **Ch 9.7 *Software Factories* is the single highest-priority follow-up** — chapter title overlaps directly with this project's name. All reachable via raw.githubusercontent.com. |
| https://jayminwest.substack.com/p/a-manifesto-for-agentic-development | ⏳ | Not in the repo. Direct fetch via issue #4 returned 403; Wayback retry queued in fetch issue [#8](https://github.com/lago-morph/software-factory/issues/8). May add doctrinal claims that don't appear in the book itself. |

The entire body of this report is reconstructed from a *single* index-page source. Every named pattern (Raschka's six components, Fowler's guides/sensors, Hashimoto's harness engineering, Schmid's trajectory capture) is one or two sentences in the source. **A future deepening pass that reads the seven Ch 6 sub-pages directly would change this report from partial to authoritative.**

---

## 1. The single most important formula in the chapter

> **Agent = Model + Harness**

The harness is "everything around the model that makes it an agent." The four preceding pillars — Prompt, Model, Context, Tool Use — answer *what the agent says*, *what it can reason about*, *what it knows*, and *what it can do*. The harness answers the fifth question: **what system orchestrates and constrains the agent's execution?**

This formula is the chapter's organizing claim. Everything else in the chapter is a decomposition of "harness."

## 2. Practitioner consensus crystallized (Apr 2026)

Jaymin attributes the formula to a 2026-04-12 simultaneous arrival by **Martin Fowler**, **Ethan Mollick**, **Sebastian Raschka**, **Philipp Schmid**, and **Mitchell Hashimoto** — five practitioners independently converging on "harness" as the primary differentiator between model capability and product performance, "not through coordination, but through simultaneous arrival at the same empirical observation."

**Implication for our project:** the word *harness* is now the canonical industry term for what `architectures/00-comparison.md` §4.1 calls "shared infrastructure" — but more precisely. *Harness* refers to the **runtime** orchestration layer. Our §4.1 list (worktree, sandbox, orchestrator, decision log, etc.) IS our harness specification, even if we never called it that. **Adopt the term.**

## 3. Three eras

> Prompt engineering → Context engineering → Harness engineering

Each subsumes the previous. Prompt engineering tuned *what the model is told*. Context engineering tuned *what the model knows when it acts*. Harness engineering tunes *the system the model runs inside*. Each era arose when the prior layer was no longer the binding constraint.

**Implication:** the project we are building is explicitly "harness engineering" in Jaymin's taxonomy. This is consistent with `architectures/00-comparison.md` §4.1's bet that the substrate is shared across methodologies — the harness *is* the substrate.

## 4. Scaffold vs. harness

The chapter explicitly distinguishes:

- **Scaffold** — *pre-runtime* artifacts that shape the agent's behavior. Includes CLAUDE.md, AGENTS.md, system prompts, project conventions. Set up once; consulted by the agent at runtime; not actively steering during execution.
- **Harness** — *runtime* control system. The active loop that orchestrates the agent's tool calls, manages context, enforces permissions, captures trajectory. Steering happens here.

Most of `architectures/00-comparison.md` §4.1 is harness; AGENTS.md / CLAUDE.md / discoverability are scaffold.

## 5. Raschka's six-component harness stack

The chapter outlines Ch 6.2 ("The Harness Stack") as a six-component decomposition attributed to Sebastian Raschka. We have the *names and one-line responsibilities*; the depth lives in the sub-page we haven't fetched.

| # | Component | One-line responsibility |
|---|---|---|
| 1 | **Workspace context** | Stable facts about the codebase (repo map, conventions). What the agent loads once. |
| 2 | **Prompt shape and cache reuse** | The stable/dynamic split of the prompt that enables cache reuse. Cost optimization. |
| 3 | **Tool access** | Bounded inventories, permission filtering. What the agent is allowed to do. |
| 4 | **Context management** | Clipping, deduplication, compression of working state. What stays in the model's view. |
| 5 | **Session memory** | Working memory + full transcript duality. What survives across turns. |
| 6 | **Subagent delegation** | Bounded spawning, context scoping for delegated work. How parallel work is launched. |

**This is a new failure-mode lens.** When an agent misbehaves, the stack tells us *which component to audit*. Compare to our `architectures/00-comparison.md` §2.4 F1–F20 failure list — that list is failure-shaped (what goes wrong); this stack is component-shaped (where to look). They are complementary and should both appear in the docs.

**Direct quote from the chapter:** "much of apparent model quality is really context quality." Component 1 + Component 4.

## 6. Fowler's guides-and-sensors control system

The chapter outlines Ch 6.4 ("Harness as Control System") as Martin Fowler's frame: the harness is not passive scaffolding but an *active control system*.

- **Guides (feedforward control)** — intervene *before* agent actions. Two flavors:
  - Computational guides (deterministic): linters, type checkers, schema validators, allow-listed paths.
  - Inferential guides (model-based): a separate model that vets the next action before execution.
- **Sensors (feedback control)** — observe *after* agent actions and steer subsequent behavior. Two flavors:
  - Computational sensors (deterministic): test runners, status checks, exit codes.
  - Inferential sensors (model-based): a judge model that scores the result.

**Direct mapping to our four architectures:**

| | Computational guide | Inferential guide | Computational sensor | Inferential sensor |
|---|---|---|---|---|
| Arch 1 (Refinery) | Probe brief constraints | — | Playwright (test executor) | Diagnostic Agent |
| Arch 2 (Atelier) | Workpad scope; pre-flight | Adversarial reviewer (pre-merge) | Test runner | Reviewer panel |
| Arch 3 (Foundry) | Phase contracts; SRS/SAD/DD templates | V&V independence check | CI + acceptance tests | Independent V&V agents |
| Arch 4 (Tournament) | Diversity policy; seed constraints | Pre-selection screen | Fitness scoring (deterministic) | Primary + Secondary judge |

Every architecture is a different mix of computational + inferential, feedforward + feedback. Fowler's framework gives us a *single vocabulary* for talking about these mixes.

**Cost tradeoff (from the chapter):** computational guides/sensors are cheap, deterministic, and limited in scope. Inferential ones are expensive, fuzzy, but broadly applicable. The harness designer chooses the mix.

**Agent Psychometrics formula** (also Ch 6.4): scaffold quality is **additively independent** from LLM capability. That is, harness investment yields gains regardless of model selection — switching models doesn't reset the harness investment. This is direct support for our decision in `architectures/00-comparison.md` §4 to invest in the substrate first.

## 7. Hashimoto's harness engineering methodology

Coined by Mitchell Hashimoto on **2026-02-05** (per the chapter).

> **The core discipline: when an agent makes a mistake, engineer the surrounding system so that mistake cannot recur.**

This is the canonical articulation of the discipline we have been calling "failure-classification-then-fix" in `spec-driven-ai-dev.md` §1.3. Specifically:

- Failure classification (model / context / prompt / harness / tool) → we have model / context / prompt / harness / tool as the five layers; our spec doc has *silence / ambiguity / incorrectness / inconsistency / undiscovered preference* as the five spec failure modes. **They are orthogonal axes**, not the same list.
- Six-step engineering loop → details live in Ch 6.5 (not yet fetched).
- **Trajectory capture as competitive infrastructure** — Schmid's thesis. Every session run through a well-instrumented harness produces training data, evaluation data, and edge-case documentation. The compounding effect accumulates over months.

**This connects directly to** `research/00-synthesis.md` §2.5 ("knowledge accumulates between cycles") **and Every.to's compound-engineering thesis**. Schmid's framing adds the *competitive* angle: a harness that captures trajectories well outcompetes one that doesn't, over time.

## 8. Security, permissions, and trust

Ch 6.6 makes a sharp, load-bearing claim:

> **The harness is the primary security boundary in an agentic system. The model does not enforce permissions — the harness does.**

This is a direct rebuttal to "the model will refuse if asked to do something bad." The model is a probabilistic policy; the harness is the deterministic enforcement layer.

Dimensions named in the chapter:

- **Permission models:** scope, operation, session dimensions
- **Sandbox architecture:** filesystem, network, process, resource boundaries
- **Token-level vs. session-level access control**
- **Trust hierarchies in multi-agent systems** (principle of least privilege)
- **Observability surfaces:** tool call logs, permission logs, session transcripts

**Implication for our failure-mode list:** F12 (lethal trifecta) is fundamentally a harness failure, not a model failure. Our architectures' "sandbox per cycle" line item should be relabeled "harness enforces sandbox" to capture the doctrinal point.

## 9. The chapter's short version (verbatim)

Worth pinning. Three rules:

> **1. Default to an existing full agentic harness for most work.** Building a harness from scratch is a significant investment. Claude Code, Codex, and equivalent tools ship with Anthropic's harness defaults already set. Start there.

> **2. When an agent fails repeatedly, the first audit target is the harness, not the model.** Raschka's diagnostic: "much of apparent model quality is really context quality." Context quality is a harness concern.

> **3. Instrument the harness for trajectory capture from the beginning — this is infrastructure, not a nice-to-have.** Every session run through a well-instrumented harness produces training data, evaluation data, and edge-case documentation. The compounding effect accumulates over months.

**Tension with our project.** Rule 1 says *don't build a harness from scratch* — and yet our four architectures all describe a harness we'd build. The resolution: our architectures should be **layered on top of** an existing harness (Claude Code, OpenHands), not built parallel to one. Report 11 reaches the same conclusion from the OpenHands direction.

## 10. Vocabulary additions

To be carried into `architectures/` and the synthesis:

- *Harness* — the runtime control system. Replaces "shared infrastructure" as the primary noun in §4.1.
- *Scaffold* — pre-runtime artifacts (CLAUDE.md, AGENTS.md, conventions). Distinct from harness.
- *Guides / sensors* — feedforward / feedback control mechanisms. Computational or inferential.
- *Agent Psychometrics formula* — harness quality is additively independent from model capability.
- *Harness engineering* (Hashimoto) — the discipline of fixing recurrent mistakes by changing the surrounding system, not the prompt.
- *Trajectory capture* (Schmid) — the competitive moat of well-instrumented runtimes.

## 11. What's still pending

The original subagent prompt (PLAN §3.2) asked the agent to read:

- Ch 6 sub-pages 1–7 (we have only the index)
- Ch 8 sub-pages 1–7 (Practices: Debugging, Evaluation, Cost & Latency, Production Concerns, Workflow Coordination, Knowledge Evolution, Operating Agent Swarms) — **none read**
- Ch 9 sub-pages 1–7 (Mental Models: Pit of Success, Prompt Maturity Model, Specs as Source Code, Context as Code, Execution Topologies, Design as Bottleneck, **Software Factories**) — **none read**

The Ch 9 *Software Factories* sub-page in particular is the highest-leverage missing piece, because its title overlaps directly with this project's name and `architectures/00-comparison.md`'s framing. A focused read of `chapters/9-mental-models/7-software-factories.md` should be the next high-priority subagent dispatch.

All remaining pages are reachable from the sandbox via `raw.githubusercontent.com` and need no fetch action.

---

*End of report 09 (partial) — `research/09-jaymin-harnesses-partial.md` v0.1*
