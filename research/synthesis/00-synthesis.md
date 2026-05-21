---
based-on-commit: f480c8b
based-on-date: 2026-05-13
---

# Research Synthesis — Findings, Tensions, and Failure Modes
**Date:** 2026-05-10
**Version:** 2 — revised after primary-source access
**Inputs:** 7 source reports (`research/01-*.md` through `07-*.md`)
**Purpose:** Distill what the sources agree on, what they disagree about, and what failure modes any software-factory architecture must defend against. This document is shared background for the four architecture options in `architectures/`.

---

## 0. Revision notes (v2)

The original synthesis was produced when six of seven source domains returned 403 from the sandbox. Primary sources have since been committed to the repo root (and most subagent reports have been revised against them). The substantive changes in v2:

**Corrections of v1 reconstruction errors:**
- **DTU = Digital Twin *Universe*** (not "Digital Twin Users"). The URL slug `dtu` misled v1. This correction propagates through every architecture spec and the comparison doc.
- **"Willison: 4 agents → exhausted by 11 AM" is CORRECT (reversal-of-reversal, 2026-05-13).** The earlier "softened to remove the specific number" correction in this revision note was itself wrong. The Lenny × Willison podcast transcript (first 30 of 90 min, drained 2026-05-13 from manual upload) contains the verbatim line: *"I can fire up like four agents in parallel and have him work on four different problems, and by like, 11am I am wiped out for the day."* Both the 4-agent count AND the 11 AM exhaustion are real and primary-anchored. The Lenny editorial paraphrase ("mentally exhausted by 11 a.m.") was an editorial compression of a quote that DOES include the count.
- **HN comment id 46955602 cited in v1 does not exist.** The "Programming as a professional discipline will be over in a year or two" quote was a v1 fabrication. Closest real analogue: bitwize HN 46955522, *"I think you're going to see drastic shrinkage of SWE departments over 2026 and 2027"* — substantially more nuanced.
- **"6,000–7,000 lines of natural-language spec" for StrongDM** was a third-party reconstruction; Simon's actual post mentions *three markdown files* (Attractor) plus a separate `cxdb` release with 16k Rust / 9.5k Go / 6.7k TS — and even the LOC numbers come from third-party summaries, not primary sources.
- **"Cal Newport" attribution for the Dark Factory framing** was wrong. Only Dan Shapiro is cited on this; Newport was not mentioned.
- **Attractor is "graph-structured"** generically per the canonical page; "DOT-graph" is a community-implementation convention (used by `strongdm/attractor` repo specifically but not stated as canonical).
- **Canonical compound-engineering loop is four-step** (Plan → Work → Review → Compound), not five. Brainstorm is subsumed into Plan in the canonical Klaassen/Shipper statement; the plugin's longer chain is an elaboration.
- **"Reviewer must be a human" stance for Simon is more nuanced than v1 suggested.** Simon's May 6, 2026 post ("Vibe coding and agentic engineering are getting closer than I'd like") admits he no longer reviews every line and articulates a "team analogy" — though he names the drift as a possible instance of *normalization of deviance*.

**Newly resolved open questions:**
- **Where do scenarios come from?** (v1 OQ#2 in report 06, OQ#5 in report 01) — the StrongDM homepage shows a "synthetic scenario curation and shaping interface" image, confirming scenarios are *partially agent-generated*. Not fully resolved (we don't know the human/agent ratio) but materially more clarity.
- **Self-improving prompts / "agents writing each other's instructions"** (v1 OQ#5 in report 03) — Klaassen's frustration-detector example is a concrete instance: Claude runs its own detection prompt 10x, analyzes chain-of-thought from the 6 failures, and *rewrites the original prompt* to look for hedged language. Tedesco's Montaigne is a second instance: "told it to update its own instructions to rely on this as the source of truth." Pattern is real and documented.
- **Team-scale at Every.to** (v1 OQ#6 in report 03) — Every runs *"five products—Cora, Monologue, Sparkle, Spiral, and our website Every.to—with primarily single-person engineering teams"* serving *"thousands of people every day."*

**Newly captured material that affects architectures:**
- **The Filesystem** is a first-class StrongDM technique (entirely missing from v1).
- **"Apply More Tokens"** enumerated representations of state: traces, screen capture, transcripts, incident replays, adversarial use, agentic simulation, customer interviews, price elasticity tests.
- **Code as opaque ML weights:** StrongDM's framing — "correctness is inferred exclusively from externally observable behavior."
- **17+ community Attractor implementations** across 12 languages — the pattern is reproducible.
- **StrongDM was acquired by Delinea** weeks before the HN post (confirmed in-thread by simonw and navanchauhan).
- **Jay Taylor's DTU origin story** (HN 46931812): started August 2025 with Sonnet 3.5; reimplementing in Rust with gpt-5.2 + gpt-5.3-codex; Slack was harder to clone than all of G-Suite; 100%-SDK-compatibility was the key insight.
- **Independent practitioner cost data** (noosphr, HN 46925882): $500–$5000/day per seat for a trading firm's internal-tool builder. The only non-StrongDM-affiliated cost report in the corpus.
- **Compound engineering 80/20 + 50/50 rules** — 80/20 is *per cycle* (planning+review vs work+compound); 50/50 is *across all engineering time* (feature work vs system-improvement work).
- **Five-stage adoption ladder** for compound engineering (Stage 0 manual → Stage 5 parallel cloud).
- **"Looking-the-part hazard"** (Simon, May 6): a repo with 100 commits and tests no longer proves care.
- **Solomon Hykes definition** "An AI agent is an LLM wrecking its environment in a loop" — adopted by Simon as a complement to his tools-in-a-loop framing.
- **Hannah Moran (Anthropic) provenance** for "Agents are models using tools in a loop" — coined at a workshop, not by Simon.
- **Simon's evals corpus** is denser than v1 captured: Hamel Husain (60–80% of dev time on error analysis), Anthropic multi-agent-research, Armin Ronacher ("Testing and evals remains the single hardest problem in AI engineering"), plus Simon's meta-claim that *"evals are the single most important distinguishing factor"* between effective and ineffective AI engineers.
- **Simon's guide has 16 chapters across 6 sections** (not the 12 v1 enumerated). New chapters: *AI should help us produce better code*, *Using Git with coding agents*, two "Annotated prompts" walkthroughs.

**Still blocked:** El Kaim's "Dark Factory" article remains behind a Cloudflare challenge. The v1 reconstruction stands; report 07 documents the block status explicitly.

---

## 1. Reachability status

Primary sources accessed from local saved copies (committed at repo root): factory.strongdm.ai (10 pages), every.to (4 articles), simonwillison.net (23 pages), news.ycombinator.com (the thread, 459 comments), lennysnewsletter.com (visible portion; **interview body remains paywalled** — only the editorial summary, sponsors, and 45-entry references list are accessible). **Still inaccessible:** el-kaim.com and welkaim's Medium author pages (all three local files are Cloudflare challenge pages).

GitHub repos (Attractor, Every.to plugins, Every.to skill libraries) were directly accessible throughout. Their reports were not affected by the v1 reconstruction issue.

## 2. Where the sources agree

The seven sources, despite different orientations, converge on a small number of methodology primitives. These are the "consensus" — the things any software factory architecture should probably contain in some form.

### 2.1 Specs become the primary artifact

Every source treats the spec — not the code — as the durable, version-controlled, human-curated artifact. StrongDM publishes Attractor as nothing but markdown specs. Compound engineering bookends a strategy document with retrospective knowledge documents. The existing baseline `spec-driven-ai-dev.md` opens with the same claim: "the specification, not the implementation, is the scarce and valuable artifact." Simon's own May 6 post explicitly acknowledges the artifact-of-record has shifted toward the spec even in his own practice.

### 2.2 Scenarios live outside the codebase

The single most-cited innovation across the corpus is StrongDM's repurposing of Cem Kaner's 2003 "scenario testing" — end-to-end user stories, in prose, stored *outside* the codebase the agent can read, judged by an LLM separate from the implementing agent. Treats scenarios as an ML-style holdout set. Every source that engages with validation discusses this pattern; none object to it. **New in v2:** scenario *authorship* is at least partially agent-assisted at StrongDM (homepage caption confirms a "synthetic scenario curation and shaping interface").

### 2.3 Validation harnesses are the real engineering

The HN consensus, Simon Willison, and El Kaim all converge on the same point: orchestration is the easy part; *validation* is the hard part. StrongDM's Digital Twin Universe (DTU) — behavioral clones of Okta, Slack, Jira, Google Workspace, etc. — is the most-praised innovation in the corpus. The point is that real-environment fidelity is what makes long-horizon agentic loops *converge instead of diverge*. **New in v2:** Jay Taylor's DTU origin (HN 46931812) makes the engineering investment visible: started August 2025; reimplementing in Rust by spring 2026; Slack was the hardest to clone; 100%-SDK-compatibility is the design discipline.

### 2.4 The agent is "an LLM running tools in a loop"

Simon Willison's deflationary definition is treated as load-bearing across the corpus. Agents are not magic; they are tool loops. The design problem is *which* tools, *which* termination condition, and *which* sandbox. **New in v2:** the canonical wording in Simon's guide is *"Agents run tools in a loop to achieve a goal"*; the May 22 2025 origin note credits Anthropic's Hannah Moran with the formulation "Agents are models using tools in a loop." Solomon Hykes added the complementary framing: *"An AI agent is an LLM wrecking its environment in a loop"* — which Simon endorses.

### 2.5 Knowledge accumulates between cycles

Every.to's compound-engineering thesis — *"each unit of engineering work should make subsequent units easier — not harder"* — is not unique; StrongDM has CXDB (immutable observability DAG), El Kaim names "filesystem as memory," Simon names "hoard things you know how to do," compound-engineering has `docs/solutions/` with stable IDs and YAML frontmatter. The substrates differ, but the principle is universal: *some* artifact must persist outside the chat window so that future agents read it.

**New in v2:** the most striking variant of this pattern is *self-improving prompts*. Klaassen's frustration-detector iterates from 4/10 success to 9/10 by analyzing its own chain-of-thought and rewriting its own detection prompt. Tedesco's Montaigne is told to "update its own instructions" to use newly-discovered numbers as a source of truth. The pattern is documented, concrete, and reproducible.

### 2.6 Single-threaded human supervision tops out at a real cognitive ceiling

The cognitive ceiling is real. The Lenny × Willison podcast transcript (drained 2026-05-13) contains the verbatim line *"I can fire up like four agents in parallel and have him work on four different problems, and by like, 11am I am wiped out for the day."* — confirming both the 4-agent count AND the 11 AM exhaustion. The earlier "softened to remove the specific number" correction (above) was itself wrong; the count is 4 and is now primary-anchored. Cherny — also now primary-anchored via the Lenny × Cherny transcript drained 2026-05-13 — claims 10–30 PRs/day, 100% Claude-written, across 5+ parallel sessions (with the corpus's first concrete $100K+/month per-engineer token-spend number) because his role is *scheduling*, not *supervision*. The implication for any factory: the human role has to change shape as parallelism increases — from per-agent supervisor to scheduler, batcher, and high-level reviewer.

### 2.7 The human's leverage moves upstream and downstream

Across the corpus, the human's repositioning is consistent: out of line-by-line code review (the inner loop), into spec authorship, scenario design, environment construction, and high-level supervision (the boundary). **New in v2:** even Simon Willison — the canonical advocate for human review — admits in his May 6, 2026 post that he no longer reviews every line of agent-written code and reaches for a "team analogy" to justify the practice. He names this drift as a candidate instance of *normalization of deviance*. The human-stays-in-review stance is itself eroding under load.

### 2.8 Tiered ceremony beats one-size-fits-all

Compound engineering's Lightweight / Standard / Deep / Deep-product tiers, Symphony's per-issue 9-phase prompt with optional fan-out, and StrongDM's "scenarios scale to risk" all reflect the same finding: process discipline must scale to the work. A bug fix and a greenfield feature should not run the same pipeline.

### 2.9 Cost is a first-class architectural concern

$1,000/day/engineer floor (StrongDM, verbatim from `/principles`) and ~$20,000/engineer/month (Willison's reading of StrongDM) anchor every economic conversation. **New in v2:** independent corroboration from `noosphr` (HN 46925882) — a trading firm's internal-tool builder ran *"$500 to $5000 per day per seat"* — the first non-StrongDM-affiliated data point. Cost routing to cheap models (Every.to's `model-hierarchy` skill) and surfacing per-loop cost telemetry as a first-class metric are common defenses.

---

## 3. Where the sources disagree

These tensions are unresolved across the corpus. Each architecture option must take a position on them.

### 3.1 Human review — required, eliminated, or tiered?

- **StrongDM:** explicitly eliminated. *"Code must not be written by humans. Code must not be reviewed by humans."* (canonical wording, verbatim from `/principles`).
- **Simon Willison:** required *in principle*, **but eroding in practice.** v1 said "required, always." Revised: Simon names *"inflicting unreviewed code on collaborators"* as the only named anti-pattern, but the May 6, 2026 post admits *"vibe coding and agentic engineering are getting closer than I'd like"* and confesses he no longer reviews every line. The position is now: **review is morally required but practically slipping under load** — which makes Simon a more interesting (and honest) data point than v1 framed.
- **Compound engineering:** tiered. Most reviews are agent-to-agent persona panels; humans review at gates with synthesis already produced.
- **El Kaim:** repositioned. Humans review *systems that build software*, not the software itself.
- **The existing spec-driven baseline:** required, but Channel-1 (compliance) failures are automatable; only Channel-2 (completeness) failures need humans.

### 3.2 Persona-based vs. graph-node agent design

- **Compound engineering:** 50+ named persona reviewers (`ce-correctness-reviewer`, `ce-dhh-rails-reviewer`, `ce-adversarial-reviewer`). Persona is the unit.
- **Attractor / StrongDM / Gas Town:** named *node types* (codergen, wait.human, conditional, parallel, fan_in, manager_loop). The graph is the unit; persona is incidental. **Note:** Attractor itself is described canonically as *"graph-structured"*, not "DOT-graph." DOT is a community implementation convention (the `strongdm/attractor` repo uses it; some of 17+ community ports use other shapes).
- **Symphony:** interchangeable agents (no per-issue specialization).
- **Tradeoff:** personas give clarity-of-voice but grow without bound; graph nodes are minimal but harder to understand at a glance.

### 3.3 Spec format — prose, structured, or DOT?

- **StrongDM NLSpec:** prose markdown.
- **Compound engineering:** prose with structured stable IDs (R/A/F/AE → U).
- **Attractor:** prose for the spec being implemented; the workflow itself is *graph-structured* (DOT in the published repo).
- **Existing baseline:** prose layered into 5 abstraction tiers with Given/When/Then acceptance criteria.

The synthesis: the *spec* is prose; the *pipeline* may be structured (DOT-graph or its equivalent); the *traceability metadata* is structured (stable IDs).

### 3.4 Knowledge architecture — flat files, DAG, chat history, or self-improving prompts?

- **Compound engineering:** flat markdown files with YAML frontmatter, anti-duplication, and discoverability checks — **plus self-improving prompts** (Klaassen's frustration-detector, Tedesco's Montaigne).
- **CXDB / StrongDM:** turn-by-turn DAG of every agent interaction, blob-deduplicated, branchable from any turn. Performance: p50 < 1ms append, 70%+ storage reduction via BLAKE3 CAS.
- **Simon:** personal hoard of recipes/prompts, plus the deeper "hoard things you know how to do" pattern.
- **El Kaim:** "filesystem as memory."
- **StrongDM "The Filesystem"** is a named first-class technique on its own.

The deeper question: is knowledge captured *eagerly* (compound-engineering, with `/ce-compound` auto-invoked on phrases like "that worked") or *lazily* (CXDB-style, everything is logged and queried later)? And is the captured knowledge *static* (re-read by future agents) or *active* (rewrites prompts based on its own failure analysis)? Compound engineering does both; the other sources are predominantly static.

### 3.5 Adversarial review — separate role or attribute of every reviewer?

Compound engineering elects to have named adversarial reviewers (`ce-adversarial-reviewer`, `ce-adversarial-document-reviewer`) rather than asking every reviewer to be adversarial. The tradeoff is clarity of voice (when "the adversarial review" is itself a finding) vs. reviewer count growth. None of the other sources have a concrete answer.

### 3.6 Parallel agent ceiling and human role

- **Willison:** 4 agents in parallel → mentally exhausted by 11 a.m. (both verbatim-anchored in the Lenny × Willison transcript drained 2026-05-13). The earlier v2 "specific count fabricated" framing was wrong — reversal-of-reversal.
- **Cherny:** 5+ parallel sessions, 10–30 PRs/day, 100% Claude-written since November 2025; productivity per engineer +200%; $100K+/month per-engineer token spend (all primary-anchored from Lenny × Cherny transcript drained 2026-05-13, minutes 0–30).
- **Symphony:** hard cap at 4 concurrent agents in the public demo.

The architecture decision is whether the human is *supervising* (low ceiling, deep review) or *scheduling* (high ceiling, async batched review). The factory tooling determines which mode is enforced.

### 3.7 Provider — unified abstraction or aligned profiles?

Attractor takes a strong stance: *do not unify provider tool interfaces.* "Each model family works best with its native agent's tools and system prompts" — codex-rs for OpenAI, Claude Code for Anthropic, gemini-cli for Gemini. This is a minority position; most other sources are agnostic. The implication is that "the agent" is not portable across providers — a fact that bites factories that try to swap models.

### 3.8 Workflow language — prose, code, or graph?

Symphony's WORKFLOW.md is prose. Attractor's pipelines are graph-structured (DOT in practice). Compound engineering's workflows are skill chains. Each has distinct affordances:
- **Prose** — easy to read, hard to lint, prone to drift.
- **Graph (DOT or equivalent)** — diffable, validatable, renderable; learning curve.
- **Skill chains** — composable, but the chain is implicit in skill descriptions.

---

## 4. Failure modes any architecture must defend against

These are the recurring "this went wrong" findings across the corpus. An architecture's *quality* can be measured in part by which of these it explicitly addresses.

| # | Failure mode | What it is | Source |
|---|---|---|---|
| F1 | **Hallucination Loop** | Same model class writes the code AND the validators/twins; both inherit the same blind spots. Tests pass; production fails. | StrongDM (admission); HN polyglotfacto 46961871 (sharpest version) |
| F2 | **Reward hacking** | Agents minimize test-pass effort, not user value. `assert True` / `return true` is the canonical example. | StrongDM; HN (japhyr 46925496) |
| F3 | **Spec-completeness fallacy** | Specs cannot enumerate everything that *should not* happen. Mass AI Breach (1.5M API keys leaked) was a missing config, not a buggy line. | HN |
| F4 | **Code-quality teardown** | Agents converge on "passes tests," not "code a senior would mentor a junior to write." StrongDM's open-sourced `cxdb` had `Arc<Mutex>` anti-patterns surfaced within hours. | HN (polyglotfacto) |
| F5 | **Cognitive ceiling** | One human supervising parallel agents loses signal by mid-morning. Specific N varies with role (supervise vs schedule). | Willison (Lenny summary, verbatim) |
| F6 | **Cognitive debt** | Letting agents build code you no longer understand erodes future planning capacity. | Willison ("Interactive explanations" chapter) |
| F7 | **Normalization of deviance** | Every accepted plausible-but-slightly-wrong output drifts the team's tolerance upward. 3% error rates compound across thousands of decisions. *Now also includes the "looking-the-part hazard"* — a repo with 100 commits and tests no longer proves care. | Willison (Vaughan, Challenger); May 6, 2026 post |
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
| F18 | **Prose specs lack rigor** | Markdown NLSpecs lack TLA+/Lean-style guarantees; "amateur formal methods." | HN (polyglotfacto) |
| F19 | **Model-floor dependency** | The methodology only works once a specific model capability arrives. StrongDM credits "the second revision of Claude 3.5" (Oct 2024) as the inflection. | StrongDM, El Kaim |
| F20 | **Maintenance vs. greenfield asymmetry** | Most agent demos are greenfield; the dark factory only proves itself if it can sustain a living codebase. | El Kaim |

The architectures are evaluated against this 20-row failure set in the comparison doc.

---

## 5. Cross-cutting design primitives

Vocabulary the four architecture options share. Stated once here so each spec can reference rather than redefine.

### 5.1 Artifact stack

- **Strategy** — durable upstream anchor (1–2 page constitution, rarely amended). Compound engineering's `STRATEGY.md`.
- **Spec** — the layered, prose-with-structured-IDs description of what's wanted. The existing baseline's primary artifact. StrongDM's "NLSpec" naming.
- **Scenario** — end-to-end prose user story stored outside the codebase. ML-holdout discipline. At StrongDM, scenarios are partially agent-generated via a "synthetic scenario curation and shaping interface."
- **Plan** — WHAT not HOW: decisions, units, scope boundaries, test categories. Atomic implementation units carry stable IDs.
- **Workpad** — per-unit-of-work persistent comment/file containing plan, acceptance criteria, validation strategy, and progress checkboxes. Symphony's coordination artifact.
- **Decision log** — per-implementation structured record of every decision encountered and how it was resolved. The baseline's diagnostic surface.
- **Trajectory** — the captured execution path of an agent. CXDB's atom. Stored in a turn DAG with branch-from-any-turn, blob-deduplicated.
- **Pulse report** — short, time-windowed read on user/system outcomes; PII-free; read-only. Compound engineering's downstream loop closer.
- **Knowledge document** — captured solution or insight, YAML-frontmatter-tagged, deduplication-checked, refresh-curated.
- **Probe** — implementation built to reveal spec gaps, not to be used. The baseline's central insight.
- **The Filesystem** — used as memory; named first-class technique by StrongDM.

### 5.2 Roles (named here as functions, not necessarily as separate agents)

- **Strategist** — owns strategy, scope boundaries, success definitions.
- **Spec author / Brainstormer** — turns intent into a spec with stable IDs.
- **Planner** — turns spec into atomic implementation units with test scenarios.
- **Implementer** — builds the artifact (this is the "coding agent" in most sources).
- **Scenario designer** — authors out-of-repo end-to-end user stories. At StrongDM, partially agent-assisted.
- **Twin / environment builder** — constructs validation environments. Per Jay Taylor (HN 46931812), this is an order-of-magnitude effort: Slack alone took longer than all of G-Suite.
- **Judge / satisfaction evaluator** — LLM (or test suite) that scores trajectories against scenarios.
- **Reviewer panel** — multiple personas with different stances (correctness, security, maintainability, adversarial, etc.).
- **Synthesizer** — reconciles reviewer findings, dedupes, promotes on cross-persona agreement.
- **Diagnostician / Healer** — clusters anomalies, spawns investigators, writes prescriptions.
- **Knowledge curator** — captures learnings, refreshes the store, enforces discoverability.
- **Prompt-self-improver** — a special-case curator. Klaassen's frustration-detector pattern: agent analyzes its own failure chain-of-thought and rewrites the original prompt.
- **Conductor / Manager loop** — supervises a fleet of workers; observes, steers, escalates.
- **Human operator** — owns the boundary: strategy, scenarios, environment, escalation.

### 5.3 Loops

- **Inner loop (per-unit)** — one implementation cycle from probe to convergence.
- **Outer loop (per-feature)** — many inner loops cooperating to deliver a feature; the level at which the workpad lives.
- **Meta-loop (per-week)** — knowledge curation, spec maturity assessment, architectural drift correction.
- **Heal loop (continuous)** — observability → clustering → diagnosis → prescription → feedback into specs/scenarios.
- **Self-improvement loop** — agents analyzing their own outputs and rewriting their own instructions (compound engineering, documented in 2 articles).

### 5.4 Gates

- **Goal gate** — the implementer cannot exit without satisfying named criteria. Attractor's primitive.
- **Human gate** — a node where the pipeline pauses for an answer from the operator.
- **Adversarial gate** — a named adversarial reviewer must register a finding (or affirmatively pass) before progression.
- **Residual work gate** — findings autofix didn't resolve must be explicitly disposed (apply / file / accept-with-durable-sink / stop) before merge.
- **Discoverability gate** — knowledge stores must be reachable from `AGENTS.md` / `CLAUDE.md` or the gate fails.

### 5.5 Stable identifiers

Compound engineering's discipline is the most coherent statement of the trace pattern:

| Tier | ID | Origin | Flows into |
|---|---|---|---|
| Requirements | `R-N` | brainstorm | plan, tests |
| Actors | `A-N` | brainstorm | plan, permissions |
| Key flows | `flow:F-N` | brainstorm | implementation units |
| Acceptance examples | `AE-N` | brainstorm | test scenarios (`Covers AE3`) |
| Implementation units | `U-N` | plan | commits, PRs |
| Scenarios | `S-N` | scenario design | judge |
| Findings | `finding:F-N` | review | residual gate, knowledge docs |
| Knowledge | `K-N` | compound | future plan grounding |

The rule across all of them: **never renumber.** Splits keep the original ID; deletions leave gaps.

---

## 6. The bets each architecture takes

A summary of how the four architectures (full specs in `architectures/`) divide the unresolved tensions of §3.

| Tension | Arch 1: Specification Refinery | Arch 2: Compound Atelier | Arch 3: Phase-Gated Foundry | Arch 4: Evolutionary Tournament |
|---|---|---|---|---|
| Human review | Tiered: humans for Channel-2 only | Tiered: humans at synthesis gates | Required at every phase gate | Humans select winners, never line-review |
| Personas vs. nodes | Few named roles; layered spec drives | Many specialized personas | Distinct phases × disciplines (RUP-style) | Lineages with model-family diversity |
| Spec format | Prose, deeply layered, Given/When/Then ACs | Prose with stable IDs (R/A/F/AE → U) | Formal: SRS, SAD, DD, TRS | Genome: prose seed + scoring rubric |
| Knowledge | Pending-buffer + spec history | Flat files + auto-curation + refresh + self-improving prompts | Phase artifacts (RTM, traceability matrix) | Lineage telemetry; promote winning patterns |
| Adversarial | Diagnostic agent for compliance failures | Named adversarial reviewer roles | Independent V&V org (V-model) | Selection pressure *is* adversarial |
| Parallel ceiling | Low: layered probing is sequential | Medium: tiered ceremony adapts | Low at phase gates; high within phase | High: many candidates by design |
| Provider | Agnostic | Persona-aligned by stack-specific reviewers | Policy: different provider per phase | Diverse: family is part of the genome |
| Workflow language | Prose phases (revelation cycle) | Skill chain (Lightweight/Standard/Deep) | Phase contracts with formal artifacts | Tournament bracket + graph for inner loop |

---

## 7. Reading guide

The four architecture specs are written to be standalone — each can be read alone by someone unfamiliar with the others. They share this synthesis as background but do not cross-reference each other in their main bodies.

- **[`01-specification-refinery`](../../architectures/01-specification-refinery.md)** — The closest descendant of the existing `spec-driven-ai-dev.md`. Refines its layered-spec / revelation-cycle / 5-failure-mode core with scenarios-as-holdouts, an LLM judge separated from the implementer, stable-ID traceability, and a mature knowledge store. Best when: spec quality matters more than throughput; problem is high-stakes and badly understood; team is small and willing to invest in upstream rigor.
- **[`02-compound-atelier`](../../architectures/02-compound-atelier.md)** — Inspired by Every.to's compound engineering. Many specialized agent personas, persona-based parallel review with cross-persona promotion, mandatory knowledge curation, tiered ceremony scaling to work, WHAT-vs-HOW separation, optional self-improving prompts. Best when: you ship continuously, value cross-cutting expertise (security, performance, accessibility, etc.), and want compounding velocity over time.
- **[`03-phase-gated-foundry`](../../architectures/03-phase-gated-foundry.md)** — Pre-agile reconsidered for fast cycles. Distinct phases (Requirements → Architecture → Detailed Design → Implementation → V&V → Deployment) with formal entry/exit criteria, V-model paired verification, RUP-style discipline × phase matrix, Cleanroom no-debugging principle. Cycle time measured in *hours*, not months. Best when: regulatory/contractual environment requires audit trails; cross-team interfaces are stable; you want defects caught at the earliest possible phase.
- **[`04-evolutionary-tournament`](../../architectures/04-evolutionary-tournament.md)** — Out-of-the-box. Many parallel candidate implementations from a shared seed; selection pressure via scenario satisfaction; lineage tracking; explicit model-family diversity to defeat the Hallucination Loop. Best when: "writing code is cheap" is the binding mindset; you have rich scenarios and a strong judge; the problem space rewards exploration over precision.

The companion comparison document is [`00-comparison`](../../architectures/00-comparison.md).

---

## 8. Appendix — taxonomy of source contributions

A quick map of what each source contributes most distinctively:

| Source | Most distinctive contribution |
|---|---|
| StrongDM Factory site | Cardinal rules (verbatim from `/principles`); "code as opaque ML weights"; satisfaction-as-judge; **Digital Twin Universe** (DTU; four properties, boundary-replication recipe); pyramid summaries (Map/Cluster/Reduce); gene transfusion (3 propagation modes); semports (3 variants); shift work; **the Filesystem** as a named technique; "Apply More Tokens" (8+ enumerated state representations) |
| StrongDM Attractor repo | Graph-structured workflow (DOT in the published repo); named node types; goal gates with retry targets; supervisor (manager_loop); context-fidelity routing; provider-aligned (not unified) profiles; 17+ community implementations across 12 languages |
| Every.to compound engineering | Compounding thesis ("each unit makes the next easier"); **four-step canonical loop** (Plan→Work→Review→Compound); 80/20 + 50/50 rules; stable-ID traceability; persona-based parallel review with cross-persona promotion; residual work gate; auto-curated knowledge store; **self-improving prompts** (Klaassen's frustration-detector; Tedesco's Montaigne); five-stage adoption ladder; tool-agnostic (Claude Code, Factory Droid, Codex CLI) |
| Every.to skill libraries | Workpad protocol (one persistent comment per issue); 5-state queue with Human Review; symphony orchestration model; checklist-emitting review skills; skill granularity = one verb |
| Simon Willison | Tools-in-a-loop framing (Hannah Moran provenance); Solomon Hykes "wrecking its environment in a loop"; 16-chapter Agentic Engineering Patterns guide; red/green TDD with agents; first run the tests; subagents for context preservation; **cognitive debt**; **looking-the-part hazard**; Showboat for trajectory review; "code is cheap" mindset; evals-as-distinguishing-factor (Husain, Ronacher, Anthropic multi-agent-research) |
| HN + Lenny | Practitioner anchor data (Cherny 10–30 PRs/day, 100% Claude-written, +200% productivity, $100K+/month per-engineer tokens; Willison 4 agents in parallel → mentally exhausted by 11 a.m. — all now primary-anchored via Lenny transcripts drained 2026-05-13); $1k/day and ~$20k/month cost anchors; **noosphr's independent $500–5000/day-per-seat data point**; five sharpest skepticism critiques (Hallucination Loop, reward hacking, spec-completeness, code-quality, normalization of deviance); **Jay Taylor's DTU origin story**; **StrongDM acquired by Delinea**; Dan Shapiro 5-level taxonomy; Three Attractor reimplementations (kilroy, forge, software-factory) |
| El Kaim Dark Factory | Lights-out factory metaphor; descriptive-prescriptive stance; Healer/diagnosis/prescription medical metaphor; humans-at-the-boundary repositioning; October 2024 phase change claim. **Caveat:** primary source remains Cloudflare-blocked; this report's content is reconstructed from cross-referenced secondary coverage. |

The four architectures draw differently from this menu; the comparison doc maps which architecture borrows what.
