# Research Synthesis — Findings, Tensions, and Failure Modes
**Date:** 2026-05-10
**Inputs:** 7 source reports (`research/01-strongdm-factory.md` through `research/07-dark-factory.md`)
**Purpose:** Distill what the sources agree on, what they disagree about, and what failure modes any software-factory architecture must defend against. This document is shared background for the four architecture options in `architectures/`.

---

## 1. Reachability caveat

Six of seven research subagents reported HTTP 403 from the assigned source domains in this sandbox (factory.strongdm.ai, every.to, simonwillison.net, news.ycombinator.com, lennysnewsletter.com, el-kaim.com). The reports were reconstructed from heavily-quoted secondary sources (gists, mirrored content, third-party recaps, cross-linked posts on accessible domains) with cross-checking across at least two independent sources where possible. The accessible primary sources were the StrongDM Attractor GitHub repo and the Every.to plugin repos; both produced unusually rich primary findings. **A second pass with direct page access would tighten quotations and possibly surface chapters added after this snapshot.** This caveat is loud here so it doesn't have to be repeated in the architecture specs.

## 2. Where the sources agree

The seven sources, despite different orientations, converge on a small number of methodology primitives. These are the "consensus" — the things any software factory architecture should probably contain in some form.

### 2.1 Specs become the primary artifact

Every source treats the spec — not the code — as the durable, version-controlled, human-curated artifact. StrongDM publishes Attractor as nothing but markdown specs. Compound engineering bookends a strategy document with retrospective knowledge documents. The existing baseline `spec-driven-ai-dev.md` opens with the same claim: "the specification, not the implementation, is the scarce and valuable artifact."

### 2.2 Scenarios live outside the codebase

The single most-cited innovation across the corpus is StrongDM's repurposing of Cem Kaner's 2003 "scenario testing" — end-to-end user stories, in prose, stored *outside* the codebase the agent can read, judged by an LLM separate from the implementing agent. Treats scenarios as an ML-style holdout set. Every source that engages with validation discusses this pattern; none object to it.

### 2.3 Validation harnesses are the real engineering

The HN consensus, Simon Willison, and El Kaim all converge on the same point: orchestration is the easy part; *validation* is the hard part. StrongDM's Digital Twin Universe (behavioral clones of Okta, Slack, Jira, Google Workspace, etc.) is the most-praised innovation in the corpus. The point is that real-environment fidelity is what makes long-horizon agentic loops *converge instead of diverge*.

### 2.4 The agent is "an LLM running tools in a loop"

Simon Willison's deflationary definition is treated as load-bearing across the corpus. Agents are not magic; they are tool loops. The design problem is *which* tools, *which* termination condition, and *which* sandbox.

### 2.5 Knowledge accumulates between cycles

Every.to's compound-engineering thesis — "each unit of engineering work should make the next easier" — is not unique; StrongDM has CXDB (immutable observability DAG), El Kaim names "filesystem as memory," Simon names "hoard things you know how to do," compound-engineering has `docs/solutions/` with stable IDs and YAML frontmatter. The substrates differ, but the principle is universal: *some* artifact must persist outside the chat window so that future agents read it.

### 2.6 Single-threaded human supervision tops out around 4–15 agents

The cognitive ceiling is real. Willison reports being exhausted by 4 parallel agents at 11 AM; Cherny claims 10–15 because his role is *scheduling*, not *supervision*. The implication for any factory is that the human role has to change shape as parallelism increases — from per-agent supervisor to scheduler, batcher, and high-level reviewer.

### 2.7 The human's leverage moves upstream and downstream

Across the corpus, the human's repositioning is consistent: out of line-by-line code review (the inner loop), into spec authorship, scenario design, environment construction, and high-level supervision (the boundary). Even the sources that retain human code review (Simon, the existing spec-driven baseline) reposition the human's *primary* time toward spec quality.

### 2.8 Tiered ceremony beats one-size-fits-all

Compound engineering's Lightweight / Standard / Deep / Deep-product tiers, Symphony's per-issue 9-phase prompt with optional fan-out, and StrongDM's "scenarios scale to risk" all reflect the same finding: process discipline must scale to the work. A bug fix and a greenfield feature should not run the same pipeline.

### 2.9 Cost is a first-class architectural concern

$1,000/day/engineer floor (StrongDM) and ~$20,000/engineer/month (Willison's reading of StrongDM) anchor every economic conversation. A factory architecture that can't operate inside a defined budget envelope is incomplete. This includes routing cheap tasks to cheap models (Every.to's `model-hierarchy` skill) and surfacing per-loop cost telemetry as a first-class metric.

---

## 3. Where the sources disagree

These tensions are unresolved across the corpus. Each architecture option must take a position on them; that's part of what makes them different architectures.

### 3.1 Human review — required, eliminated, or tiered?

- **StrongDM:** explicitly eliminated. *"Code must not be written by humans. Code must not be reviewed by humans."*
- **Simon Willison:** required, always. Calls the no-review stance "wildly irresponsible" outside StrongDM's specific niche.
- **Compound engineering:** tiered. Most reviews are agent-to-agent persona panels; humans review at gates with synthesis already produced.
- **El Kaim:** repositioned. Humans review *systems that build software*, not the software itself.
- **The existing spec-driven baseline:** required, but Channel-1 (compliance) failures are automatable; only Channel-2 (completeness) failures need humans.

### 3.2 Persona-based vs. graph-node agent design

- **Compound engineering:** 50+ named persona reviewers (`ce-correctness-reviewer`, `ce-dhh-rails-reviewer`, `ce-adversarial-reviewer`). Persona is the unit.
- **Attractor / StrongDM / Gas Town:** named *node types* (codergen, wait.human, conditional, parallel, fan_in, manager_loop). The graph is the unit; persona is incidental.
- **Symphony:** interchangeable agents (no per-issue specialization).
- **Tradeoff:** personas give clarity-of-voice but grow without bound; graph nodes are minimal but harder to understand at a glance.

### 3.3 Spec format — prose, structured, or DOT?

- **StrongDM NLSpec:** prose markdown.
- **Compound engineering:** prose with structured stable IDs (R/A/F/AE → U).
- **Attractor:** prose for the spec being implemented, **DOT** for the workflow that implements it.
- **Existing baseline:** prose layered into 5 abstraction tiers with Given/When/Then acceptance criteria.

The synthesis: the *spec* is prose; the *pipeline* may be structured (DOT or its equivalent); the *traceability metadata* is structured (stable IDs).

### 3.4 Knowledge architecture — flat files, DAG, or chat history?

- **Compound engineering:** flat markdown files with YAML frontmatter, anti-duplication, and discoverability checks.
- **CXDB / StrongDM:** turn-by-turn DAG of every agent interaction, blob-deduplicated, branchable from any turn.
- **Simon:** personal hoard of recipes/prompts.
- **El Kaim:** "filesystem as memory."

The deeper question: is knowledge captured *eagerly* (compound-engineering, with `/ce-compound` auto-invoked on phrases like "that worked") or *lazily* (CXDB-style, everything is logged and queried later)?

### 3.5 Adversarial review — separate role or attribute of every reviewer?

Compound engineering elects to have named adversarial reviewers (`ce-adversarial-reviewer`, `ce-adversarial-document-reviewer`) rather than asking every reviewer to be adversarial. The tradeoff is clarity of voice (when "the adversarial review" is itself a finding) vs. reviewer count growth. None of the other sources have a concrete answer.

### 3.6 Parallel agent ceiling and human role

- **Willison:** 4 agents → exhausted by 11 AM.
- **Cherny:** 10–15 sessions, but as a *scheduler*, not a supervisor.
- **Symphony:** hard cap at 4 concurrent agents.

The architecture decision is whether the human is *supervising* (low ceiling, deep review) or *scheduling* (high ceiling, async batched review). The factory tooling determines which mode is enforced.

### 3.7 Provider — unified abstraction or aligned profiles?

Attractor takes a strong stance: *do not unify provider tool interfaces.* "Each model family works best with its native agent's tools and system prompts" — codex-rs for OpenAI, Claude Code for Anthropic, gemini-cli for Gemini. This is a minority position; most other sources are agnostic. The implication is that "the agent" is not portable across providers — a fact that bites factories that try to swap models.

### 3.8 Workflow language — prose, code, or graph?

Symphony's WORKFLOW.md is prose. Attractor's pipelines are DOT graphs. Compound engineering's workflows are skill chains. Each has distinct affordances:
- **Prose** — easy to read, hard to lint, prone to drift.
- **DOT** — diffable, validatable, renderable; learning curve.
- **Skill chains** — composable, but the chain is implicit in skill descriptions.

---

## 4. Failure modes any architecture must defend against

These are the recurring "this went wrong" findings across the corpus. An architecture's *quality* can be measured in part by which of these it explicitly addresses.

| # | Failure mode | What it is | Source |
|---|---|---|---|
| F1 | **Hallucination Loop** | Same model class writes the code AND the validators/twins; both inherit the same blind spots. Tests pass; production fails. | StrongDM, HN |
| F2 | **Reward hacking** | Agents minimize test-pass effort, not user value. `return true` is the canonical example. | StrongDM, HN |
| F3 | **Spec-completeness fallacy** | Specs cannot enumerate everything that *should not* happen. Mass AI Breach (1.5M API keys leaked) was a missing config, not a buggy line. | HN |
| F4 | **Code-quality teardown** | Agents converge on "passes tests," not "code a senior would mentor a junior to write." StrongDM's open-sourced Rust had anti-patterns within hours. | HN |
| F5 | **Cognitive ceiling** | One human supervising >4 agents loses signal by mid-morning. | Willison |
| F6 | **Cognitive debt** | Letting agents build code you no longer understand erodes future planning capacity. | Willison |
| F7 | **Normalization of deviance** | Every accepted plausible-but-slightly-wrong output drifts the team's tolerance upward. 3% error rates compound across thousands of decisions. | Willison (Vaughan, Challenger) |
| F8 | **Stale-knowledge inversion** | Without curation, knowledge stores rot; bad learnings make work harder, not easier. Compounding inverts. | Compound engineering |
| F9 | **Spec overfitting** | The spec evolves to describe what the AI happened to build rather than what the user actually wants. | Existing baseline |
| F10 | **Findings disappear into chat** | Issues raised in a session and not landed in a durable artifact are lost when the session ends. | Compound engineering |
| F11 | **Renumbering breaks references** | Numbered units get renumbered during edits; PR / chat / blocker references silently become wrong. | Compound engineering |
| F12 | **Lethal trifecta / prompt injection** | Agents with private data + untrusted input + exfiltration capability are exploitable. | Willison (CaMeL) |
| F13 | **Missing-config blindspot** | Specs say what the system *does*; specs rarely say what the *environment* must contain. | HN (Mass AI Breach) |
| F14 | **Attribution collapse** | Every commit "AI Assistant" makes accountability, reliability tracking, and model selection impossible. | El Kaim |
| F15 | **Single-prompt ideation collapse** | Single ideation prompts collapse into the model's most-trained directions. Without divergent frames + grounding, you get slop. | Compound engineering |
| F16 | **Resume-fidelity decay** | In-memory LLM session state can't be serialized; resuming a checkpoint loses one hop of full fidelity. | Attractor |
| F17 | **Parallel agents on shared dirs lose data** | Without worktree isolation or explicit serialization, concurrent agent edits silently overwrite. | Compound engineering, Symphony |
| F18 | **Prose specs lack rigor** | Markdown NLSpecs lack TLA+/Lean-style guarantees; "amateur formal methods." | HN |
| F19 | **Model-floor dependency** | The methodology only works once a specific model capability arrives. StrongDM credits Claude 3.5 Sonnet v2 (Oct 2024) as the inflection. | StrongDM, El Kaim |
| F20 | **Maintenance vs. greenfield asymmetry** | Most agent demos are greenfield; the dark factory only proves itself if it can sustain a living codebase. | El Kaim |

The architectures will each be evaluated against this 20-row failure set in the comparison doc.

---

## 5. Cross-cutting design primitives

Vocabulary the four architecture options share. Stated once here so each spec can reference rather than redefine.

### 5.1 Artifact stack

- **Strategy** — durable upstream anchor (1–2 page constitution, rarely amended). Compound engineering's `STRATEGY.md`.
- **Spec** — the layered, prose-with-structured-IDs description of what's wanted. The existing baseline's primary artifact.
- **Scenario** — end-to-end prose user story stored outside the codebase. ML-holdout discipline.
- **Plan** — WHAT not HOW: decisions, units, scope boundaries, test categories. Atomic implementation units carry stable IDs.
- **Workpad** — per-unit-of-work persistent comment/file containing plan, acceptance criteria, validation strategy, and progress checkboxes. Symphony's coordination artifact.
- **Decision log** — per-implementation structured record of every decision encountered and how it was resolved. The baseline's diagnostic surface.
- **Trajectory** — the captured execution path of an agent. CXDB's atom.
- **Pulse report** — short, time-windowed read on user/system outcomes; PII-free; read-only. Compound engineering's downstream loop closer.
- **Knowledge document** — captured solution or insight, YAML-frontmatter-tagged, deduplication-checked, refresh-curated.
- **Probe** — implementation built to reveal spec gaps, not to be used. The baseline's central insight.

### 5.2 Roles (named here as functions, not necessarily as separate agents)

- **Strategist** — owns strategy, scope boundaries, success definitions.
- **Spec author / Brainstormer** — turns intent into a spec with stable IDs.
- **Planner** — turns spec into atomic implementation units with test scenarios.
- **Implementer** — builds the artifact (this is the "coding agent" in most sources).
- **Scenario designer** — authors out-of-repo end-to-end user stories.
- **Twin / environment builder** — constructs validation environments.
- **Judge / satisfaction evaluator** — LLM (or test suite) that scores trajectories against scenarios.
- **Reviewer panel** — multiple personas with different stances (correctness, security, maintainability, adversarial, etc.).
- **Synthesizer** — reconciles reviewer findings, dedupes, promotes on cross-persona agreement.
- **Diagnostician / Healer** — clusters anomalies, spawns investigators, writes prescriptions.
- **Knowledge curator** — captures learnings, refreshes the store, enforces discoverability.
- **Conductor / Manager loop** — supervises a fleet of workers; observes, steers, escalates.
- **Human operator** — owns the boundary: strategy, scenarios, environment, escalation.

### 5.3 Loops

- **Inner loop (per-unit)** — one implementation cycle from probe to convergence.
- **Outer loop (per-feature)** — many inner loops cooperating to deliver a feature; the level at which the workpad lives.
- **Meta-loop (per-week)** — knowledge curation, spec maturity assessment, architectural drift correction.
- **Heal loop (continuous)** — observability → clustering → diagnosis → prescription → feedback into specs/scenarios.

### 5.4 Gates

- **Goal gate** — the implementer cannot exit without satisfying named criteria. Attractor's primitive.
- **Human gate** — a hexagon node where the pipeline pauses for an answer from the operator.
- **Adversarial gate** — a named adversarial reviewer must register a finding (or affirmatively pass) before progression.
- **Residual work gate** — findings autofix didn't resolve must be explicitly disposed (apply / file / accept-with-durable-sink / stop) before merge.
- **Discoverability gate** — knowledge stores must be reachable from `AGENTS.md` / `CLAUDE.md` or the gate fails.

### 5.5 Stable identifiers

Compound engineering's discipline is the most coherent statement of the trace pattern:

| Tier | ID | Origin | Flows into |
|---|---|---|---|
| Requirements | `R-N` | brainstorm | plan, tests |
| Actors | `A-N` | brainstorm | plan, permissions |
| Key flows | `F-N` | brainstorm | implementation units |
| Acceptance examples | `AE-N` | brainstorm | test scenarios (`Covers AE3`) |
| Implementation units | `U-N` | plan | commits, PRs |
| Scenarios | `S-N` | scenario design | judge |
| Findings | `F-N`* | review | residual gate, knowledge docs |
| Knowledge | `K-N` | compound | future plan grounding |

*disambiguating from Key flows: prefix scope where collision is possible (`flow:F-3`, `finding:F-3`).

The rule across all of them: **never renumber.** Splits keep the original ID; deletions leave gaps.

---

## 6. The bets each architecture takes

A summary of how the four architectures (full specs in `architectures/`) divide the unresolved tensions of §3.

| Tension | Arch 1: Specification Refinery | Arch 2: Compound Atelier | Arch 3: Phase-Gated Foundry | Arch 4: Evolutionary Tournament |
|---|---|---|---|---|
| Human review | Tiered: humans for Channel-2 only | Tiered: humans at synthesis gates | Required at every phase gate | Humans select winners, never line-review |
| Personas vs. nodes | Few named roles; layered spec drives | Many specialized personas | Distinct phases × disciplines (RUP-style) | Lineages with model-family diversity |
| Spec format | Prose, deeply layered, Given/When/Then ACs | Prose with stable IDs (R/A/F/AE → U) | Formal: SRS, SAD, DD, TRS | Genome: prose seed + scoring rubric |
| Knowledge | Pending-buffer + spec history | Flat files + auto-curation + refresh | Phase artifacts (RTM, traceability matrix) | Lineage telemetry; promote winning patterns |
| Adversarial | Diagnostic agent for compliance failures | Named adversarial reviewer roles | Independent V&V org (V-model) | Selection pressure *is* adversarial |
| Parallel ceiling | Low: layered probing is sequential | Medium: tiered ceremony adapts | Low at phase gates; high within phase | High: many candidates by design |
| Provider | Agnostic | Persona-aligned by stack-specific reviewers | Policy: same provider per phase | Diverse: family is part of the genome |
| Workflow language | Prose phases (revelation cycle) | Skill chain (Lightweight/Standard/Deep) | Phase contracts with formal artifacts | Tournament bracket + DOT for inner loop |

---

## 7. Reading guide

The four architecture specs are written to be standalone — each can be read alone by someone unfamiliar with the others. They share this synthesis as background but do not cross-reference each other in their main bodies.

- **`architectures/01-specification-refinery.md`** — The closest descendant of the existing `spec-driven-ai-dev.md`. Refines its layered-spec / revelation-cycle / 5-failure-mode core with scenarios-as-holdouts, an LLM judge separated from the implementer, stable-ID traceability, and a mature knowledge store. Best when: spec quality matters more than throughput; problem is high-stakes and badly understood; team is small and willing to invest in upstream rigor.
- **`architectures/02-compound-atelier.md`** — Inspired by Every.to's compound engineering. Many specialized agent personas, persona-based parallel review with cross-persona promotion, mandatory knowledge curation, tiered ceremony scaling to work, WHAT-vs-HOW separation. Best when: you ship continuously, value cross-cutting expertise (security, performance, accessibility, etc.), and want compounding velocity over time.
- **`architectures/03-phase-gated-foundry.md`** — Pre-agile reconsidered for fast cycles. Distinct phases (Requirements → Architecture → Detailed Design → Implementation → V&V → Deployment) with formal entry/exit criteria, V-model paired verification, RUP-style discipline × phase matrix, Cleanroom no-debugging principle. Cycle time measured in *hours*, not months. Best when: regulatory/contractual environment requires audit trails; cross-team interfaces are stable; you want defects caught at the earliest possible phase.
- **`architectures/04-evolutionary-tournament.md`** — Out-of-the-box. Many parallel candidate implementations from a shared seed; selection pressure via scenario satisfaction; lineage tracking; explicit model-family diversity to defeat the Hallucination Loop. Best when: "writing code is cheap" is the binding mindset; you have rich scenarios and a strong judge; the problem space rewards exploration over precision.

The companion comparison document is `architectures/00-comparison.md`.

---

## 8. Appendix — taxonomy of source contributions

A quick map of what each source contributes most distinctively:

| Source | Most distinctive contribution |
|---|---|
| StrongDM Factory site | Cardinal rules; satisfaction-as-judge; Digital Twin Universe; pyramid summaries; gene transfusion; semports |
| StrongDM Attractor repo | DOT-graph workflow; named node types; goal gates with retry targets; supervisor (manager_loop); context-fidelity routing; provider-aligned (not unified) profiles |
| Every.to compound engineering | Compounding thesis; stable-ID traceability; persona-based parallel review with cross-persona promotion; residual work gate; auto-curated knowledge store; tiered ceremony |
| Every.to skill libraries | Workpad protocol (one persistent comment per issue); 5-state queue with Human Review; symphony orchestration model; checklist-emitting review skills; skill granularity = one verb |
| Simon Willison | Tools-in-a-loop framing; red/green TDD with agents; first run the tests; subagents for context preservation; cognitive debt; Showboat for trajectory review; "code is cheap" mindset |
| HN + Lenny | Practitioner anchor data (Cherny 10–30 PRs/day; Willison 4-agent ceiling; $1k/$20k cost anchors); five sharpest skepticism critiques; Lenny bibliography; Dan Shapiro 5-level taxonomy |
| El Kaim Dark Factory | Lights-out factory metaphor; descriptive-prescriptive stance; Healer/diagnosis/prescription medical metaphor; humans-at-the-boundary repositioning; October 2024 phase change claim |

The four architectures draw differently from this menu; the comparison doc maps which architecture borrows what.
