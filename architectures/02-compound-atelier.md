---
based-on-commit: c495dc9
based-on-date: 2026-05-10
---

# Architecture 2 — The Compound Atelier
## A Software Factory Built on Specialized Persona Workshops with Knowledge Compounding

**Version:** 0.2
**Status:** Draft architecture proposal
**Lineage:** Inspired by Every.to's compound-engineering plugin and symphony-thumbtack orchestration model; refined with findings from `research/00-synthesis.md` (v2, post-primary-source-access)
**Stance in one sentence:** *Each unit of work makes the next one easier — by passing through specialist hands and leaving its lessons behind.*

---

## 0. Revision notes (v0.2)

Changes from v0.1 driven by the v2 research pass against primary every.to sources:

- **Canonical compound-engineering loop is FOUR-STEP** (Plan → Work → Review → Compound), not five. The original report mis-stated this from plugin-internal language; the every.to articles consistently state four. Brainstorming is subsumed into Plan. The plugin's longer chain is an elaboration, not the canonical statement. This architecture's §5 (workshop chain) is unchanged in structure but the framing in §1 has been updated to match.
- **80/20 + 50/50 rules are paired, not merged.** 80/20 is *per cycle* (planning+review vs work+compound). 50/50 is *across all engineering time* (feature work vs system-improvement work). Both are documented in the every.to guide.
- **Self-improving prompts are now a documented pattern.** Klaassen's frustration-detector example — the agent analyzes its own chain-of-thought from failed runs and *rewrites the original prompt* — is a concrete, reproducible instance. Tedesco's Montaigne is a second instance. The architecture now names this pattern in §4.4 (Synthesis and curation) and adds a "Prompt-self-improver" role; existing personas remain unchanged.
- **Team-scale evidence is now concrete.** Every runs five products with "primarily single-person engineering teams" serving "thousands of people every day." The original open question #5 about single-author vs team scale is partially resolved: the methodology operates at single-person scale per product; cross-product coordination is via shared knowledge stores and plugin updates.
- **Five-stage adoption ladder** (Stage 0 manual → Stage 5 parallel cloud) is documented in the guide. This architecture's implementation roadmap (§11) maps onto roughly stages 1–4.
- **Tool-agnostic statement:** Every uses Claude Code primarily, but also Factory's Droid and OpenAI's Codex CLI. The architecture is provider-agnostic; this is now reinforced.

No structural changes to the artifact stack or the role catalog.

---

## 1. Core thesis

The expensive parts of software work are upstream (deciding what to build and how to shape it) and downstream (catching pattern-level issues during review and codifying lessons). Execution is comparatively cheap, parallelizable, and recoverable. A factory that invests heavily in **specialized workshops** for the expensive parts — and that **mandates** the codification of every cycle's lessons — bends the cost curve of subsequent cycles downward.

This architecture explicitly rejects the "one general-purpose agent does everything" model. Instead it employs many small, deeply-specialized agent personas — a brainstorming partner, a planner, an implementer, a panel of reviewer specialists (correctness, security, performance, architecture, adversarial), a curator. Each persona has narrow scope, narrow inputs, and a narrow output. The orchestrator chains them.

The slogan that captures the architecture: **"80% is in planning and review, 20% is in execution."** This is also the slogan that captures Every.to's own compound-engineering plugin, which is the closest existing realization of this architecture.

---

## 2. The compounding mechanism

What compounds is **durable, structured artifacts on disk that future agents are wired to read.** Not session memory, not chat history, not heuristics encoded in agent prompts — flat markdown files in the repository, version-controlled, greppable, with stable identifiers and YAML frontmatter for retrieval.

The five mechanisms that make iteration *n+1* cheaper than iteration *n*:

1. **Reusable upstream anchors.** A single strategy document is read by every downstream persona. Edits to it propagate without re-prompting.
2. **Stable IDs across artifacts.** R/A/F/AE → U → commit → PR. Cross-references survive plan edits.
3. **Knowledge store auto-consulted at planning time.** Specialized researcher agents grep the store before the planner runs, surfacing relevant prior solutions.
4. **Pattern-promotion during review.** When two reviewers spot the same issue, severity rises automatically; the finding becomes a candidate for a knowledge document.
5. **Periodic hygiene.** A separate refresh skill curates the store under five outcomes (Keep / Update / Consolidate / Replace / Delete) — without it, stale knowledge inverts compounding.

The dual asymmetry is critical: capture without curation rots the asset, but curation without capture has nothing to curate. The architecture mandates both as separate, named, reviewable activities.

---

## 3. Artifact stack

| Tier | Artifact | Lifecycle | Stable IDs |
|---|---|---|---|
| Strategy | `STRATEGY.md` (1–2 page anchor) | Rarely amended | — |
| Brainstorm / Requirements | `docs/brainstorms/<topic>-requirements.md` | One per major topic | R, A, F, AE |
| Plan | `docs/plans/<topic>-plan.md` | One per implementation cycle | U |
| Workpad | One persistent comment per issue | Per-issue, mutable | issue ID |
| Implementation | git commits + PR | Per-cycle, immutable | U references |
| Code review | Review verdict (synthesized) | Per-cycle, immutable | finding IDs |
| Knowledge | `docs/solutions/<category>/*.md` | Curated continuously | K |
| Pulse report | `docs/pulse-reports/<date>.md` | Time-windowed (30–40 lines, hard cap) | — |
| Adversarial verdict | `docs/reviews/adversarial-<id>.md` | One per cycle's adversarial pass | finding IDs |

### 3.1 Spec tiering

The Brainstormer picks a tier based on scope:

- **Lightweight** — alignment-only conversation; emits no document if convergence is fast.
- **Standard** — full requirements doc with R/A/F/AE-IDs.
- **Deep** — Standard + extensive grounding from researcher agents + scenario-flow analysis.
- **Deep-product** — Deep + product-shape (actors, core outcome, positioning, durability).

Ceremony scales to the work; trivial bug fixes do not run the full chain.

### 3.2 Knowledge document shape

Every `docs/solutions/<category>/*.md` follows a strict template:

```yaml
---
type: solution | insight | playbook | correction | pattern
module: payments-core
tags: [retry, idempotency, race]
problem_type: bug | knowledge
confidence: high | medium | low
created: 2026-05-10
last_updated: 2026-05-10
source: cycle-127 / U3
---
```

Two-track body:

- **Bug track:** Symptoms / What Didn't Work / Solution / Why This Works / Prevention
- **Knowledge track:** Context / Guidance / Why This Matters / When to Apply / Examples

Forcing the wrong shape onto a learning produces structurally wrong docs; the Curator enforces the choice.

---

## 4. Roles

The Compound Atelier defines four broad role categories. Within each, multiple specialized personas can be added, removed, or substituted depending on the project.

### 4.1 Workshop chain (the pipeline)

These personas run in sequence on a unit of work.

- **Strategist** — owns `STRATEGY.md`. Rarely invoked. Rumelt-style: diagnosis / guiding policy / coherent action / explicit non-goals.
- **Brainstormer** — turns vague intent into a tier-appropriate requirements doc. One question per turn (this discipline is enforced; stacking questions produces diluted answers). Named "gap lenses" (Evidence, Specificity, Counterfactual, Attachment, Durability) pressure-test premises.
- **Planner** — turns requirements into atomic implementation units (`U-N`). Plans are *decision documents with execution guardrails*, not implementation choreography. WHAT, not HOW. Decisions, scope boundaries, atomic units, files touched, test scenarios per unit, risks — but not signatures or pseudocode.
- **Implementer** — executes the plan in a per-issue git worktree. Makes HOW decisions with current code in front of it. Documents reasoning in the workpad on each progress checkpoint.

### 4.2 Researcher fan-out (called by the chain)

Up to *k* researcher agents run in parallel to ground the chain personas. Each is narrowly scoped.

- `repo-research-analyst` — local conventions, architecture, technology stack
- `learnings-researcher` — searches `docs/solutions/` for relevant prior context
- `framework-docs-researcher` — external library/framework documentation
- `best-practices-researcher` — external prior art
- `spec-flow-analyzer` — edge-case completeness on user flows
- `git-history-analyzer` — code evolution context
- `issue-intelligence-analyst` — clusters issues for theme detection
- `session-historian` — searches prior sessions for "what was tried before"

The Brainstormer and Planner are the primary callers; the Implementer calls a smaller subset (typically `learnings-researcher` and `repo-research-analyst`).

### 4.3 Reviewer panel (run after the Implementer)

The single richest part of the architecture. Reviewers are persona-shaped, run in parallel, and produce findings that the Synthesizer reconciles.

**Always-on code reviewers:**
- `correctness-reviewer` — logic, edge cases, state bugs
- `testing-reviewer` — test coverage and assertion strength
- `maintainability-reviewer` — coupling, naming, dead code
- `project-standards-reviewer` — `AGENTS.md` / `CLAUDE.md` compliance

**Stack-specific code reviewers (loaded by repo language/stack):**
- `<expert>-rails-reviewer`, `<expert>-frontend-races-reviewer`, etc.

**Cross-cutting code reviewers (selected diff-aware):**
- `security-reviewer` and `security-sentinel`
- `performance-reviewer` and `performance-oracle`
- `reliability-reviewer`
- `api-contract-reviewer`
- `architecture-strategist`
- `data-integrity-guardian`, `migrations-reviewer`, `schema-drift-detector`
- `pattern-recognition-specialist`
- `code-simplicity-reviewer`
- **`adversarial-reviewer`** — *constructs failure scenarios to break implementations across component boundaries.* This persona is named separately and runs alongside the constructive reviewers.

**Always-on document reviewers (for plans/specs):**
- `coherence-reviewer` — internal consistency, terminology drift
- `feasibility-reviewer` — will this survive contact with reality?

**Cross-cutting document reviewers:**
- `design-lens-reviewer`, `product-lens-reviewer`, `scope-guardian-reviewer`, `security-lens-reviewer`
- **`adversarial-document-reviewer`** — *challenges premises; surfaces unstated assumptions; stress-tests decisions.*

### 4.4 Synthesis and curation

- **Synthesizer** — runs after the reviewer panel. Pipeline: validate → anchor (each finding to actual content) → dedupe → **promote on cross-persona agreement** → resolve contradictions → auto-promote `safe_auto` → route by tier. Output: a single ordered finding list with severity (P0–P3) and autofix class (`safe_auto` / `gated_auto` / `manual` / `advisory`).
- **Knowledge Curator** — runs after every cycle. Captures durable lessons (typically auto-invoked on phrases like "that worked," "it's fixed"). Five-dimensional overlap check (problem statement, root cause, solution approach, files referenced, prevention rules) routes high-overlap content to update an existing doc rather than create a duplicate. Mandatory discoverability check on `AGENTS.md` / `CLAUDE.md`.
- **Refresh Curator** — runs on a separate cadence (e.g., weekly). Five outcomes per knowledge doc: Keep / Update / Consolidate / Replace / Delete. Auto-delete only when (a) implementation is gone, (b) problem domain is gone, (c) inbound citations are absent or decorative — all three.
- **Prompt-self-improver** (optional, documented pattern) — runs after a Knowledge Curator captures a failure mode that is *itself a prompt failure*. Example pattern from Every.to's primary sources: Klaassen's frustration-detector runs its own detection prompt 10 times, finds it succeeds 4/10, analyzes Claude's chain-of-thought from the 6 failures, identifies the missing signal (e.g., hedged language like "Hmm, not quite"), and **rewrites the original prompt** to look for it. On the next iteration, the rewritten prompt succeeds 9/10. The Prompt-self-improver is a special-case curator: its output is not a knowledge document but an updated agent prompt. The factory checks the updated prompt against a held-out test set before promoting it to live use. This pattern is documented in Klaassen's "My AI Had Already Fixed the Code Before I Saw It" and Tedesco's "The Agent That Saved My Brain."

### 4.5 Conductor (the orchestrator)

The orchestrator is structurally separate from any persona. It:

- Picks issues off a queue (`tasks.json`, Linear, GitHub Issues — interchangeable)
- Allocates worktrees per issue
- Dispatches the workshop chain
- Enforces concurrency caps (default 4 concurrent workpieces)
- Maintains the 5-state queue (`Backlog → Todo → In Progress → Human Review → Merging → Done`, plus `Rework`)
- Reconciles human actions on the queue (drag to Merging = approve; drag to Rework = reject)

The orchestrator does not invent the workflow; it executes the *score* defined by the workshop chain plus the per-issue prompt template.

### 4.6 The human

One human role at solo scale (the **Operator**). Three roles at small-team scale:

- **Strategist-human** — owns `STRATEGY.md` and the long-arc choice of priorities.
- **Operator-human** — handles `Human Review` queue: approves plans, approves PRs, approves knowledge captures, handles `Rework` decisions.
- **Curator-human** — owns the knowledge store's health: runs refresh cycles, judges overlap-update calls, prunes dead knowledge.

These can be the same person, or distinct. The interfaces between them are the artifacts on disk.

---

## 5. The cycle

A unit of work is one **issue**. Its lifecycle traces the 5-state queue with 9 internal phases.

```
Backlog
  ↓ (human or trigger picks it up)
Todo
  ↓ (orchestrator dispatches → "In Progress")
In Progress  ============================
  Phase 1 — Kickoff & Routing
    Hydrate issue state; determine tier
  Phase 2 — Brainstorm (if needed at this tier)
    Brainstormer + researcher fan-out → requirements doc with R/A/F/AE-IDs
  Phase 3 — Plan
    Planner + researcher fan-out → plan with U-IDs and per-unit test scenarios
    (Confidence check: weak sections trigger targeted reviewer dispatch)
  Phase 4 — Document review (plan goes through document reviewer panel)
    Synthesizer reconciles findings; user approves or revises plan
  Phase 5 — Implementation
    Worktree-isolated agents (one per U-ID, fanout if independent); workpad updated each checkpoint
    Plan-aware idempotency check (don't reimplement shipped work)
  Phase 6 — Code review (panel)
    Diff-aware persona selection (always-ons + cross-cutting + stack-specific + adversarial)
    Synthesizer reconciles; cross-persona promotion; auto-fix for safe_auto
  Phase 7 — Validation
    Tests run; acceptance criteria checked (Covers AE-N references); workpad updated
  Phase 8 — Push & PR
    PR body composed (What / Why / How / Validation); residual work gate
  Phase 9 — PR Feedback Sweep
    Address PR comments via parallel sub-agents; synthesizer reconciles
  ↓
Human Review  (waiting; agent must not modify code)
  ↓ (human approves)
Merging
  ↓ (land skill: squash-merge, mark PR MERGED)
Done
  ↓ (curator runs)
Knowledge captured to docs/solutions/
Pulse report updated
```

`Rework` is a destructive reset (re-read issue + comments, close PR, **delete the workpad**, fresh branch from main). It forces re-planning rather than band-aid patching.

### 5.1 Workpad protocol

The workpad is the single persistent coordination artifact per issue. Exactly one per issue, marked `## Workpad`, sections:

- **Plan** (linked to the corresponding `<topic>-plan.md` document)
- **Acceptance criteria** (with `Covers AE-N` references)
- **Validation strategy** (what tests and what manual checks)
- **Progress checkboxes** (one per U-ID + key validation step)

Agents update it on every progress checkpoint. All agent-authored comments on the issue (separate from the workpad itself) are prefixed `[claude]` so the human can scan for `non-[claude]` comments to find what needs an answer.

### 5.2 Tiered cycle scope

| Tier | Phases run |
|---|---|
| Lightweight | 1, 5, 7, 8 (skip brainstorm, plan, full review; defer to harness-native review) |
| Standard | 1–9 |
| Deep | 1–9 with extended researcher fan-out and full reviewer panel |
| Deep-product | Standard + Phase 0 (product-shape brainstorm) |

The orchestrator picks the tier from issue labels or from the brainstorm-tier classifier.

---

## 6. Review and feedback patterns

The richest part of the architecture; reproduces Every.to's most distinctive design moves.

### 6.1 Persona-based parallel review with synthesis

Diff-aware (or doc-aware) **persona selection** by agent judgment over actual content (not keyword matching). Selected personas dispatch in parallel. The Synthesizer:

1. **Validates** each finding against schema.
2. **Anchors** each finding to specific lines / sections of the artifact.
3. **Deduplicates** across personas (fingerprint + evidence-substring overlap).
4. **Promotes** findings that two or more personas independently raise — cross-persona agreement is signal.
5. **Resolves contradictions** when personas disagree about the right action; surfaces them to the human if no automatic resolution.
6. **Auto-applies** `safe_auto` findings via a fixer queue.
7. **Routes** the rest by tier (Operator review, durable sink, advisory log).

### 6.2 Severity × Autofix class (orthogonal axes)

| Severity | Meaning |
|---|---|
| P0 | Critical breakage; release-blocking |
| P1 | Significant defect; should fix before merge |
| P2 | Quality concern; fix in this cycle if possible |
| P3 | Discretionary; reviewer judgment |

| Autofix class | Meaning |
|---|---|
| `safe_auto` | Fix is mechanical; reviewer queue auto-applies |
| `gated_auto` | Fix is mechanical but changes contracts/behavior; routes to a downstream resolver or human |
| `manual` | Actionable handoff to a human or another agent |
| `advisory` | Report-only; no expected action |

A finding is *both* a severity and an autofix class. P0+`advisory` is rare but legal (e.g., "this is a data integrity issue, but the right fix requires a product decision").

### 6.3 Round-to-round suppression

Iterative review must not re-surface findings the user explicitly rejected. The Synthesizer maintains a **decision primer** between rounds: applied findings flow forward (the next round verifies the fix landed); rejected findings (skip / defer / acknowledge) are suppressed via fingerprint + evidence-substring overlap matching.

### 6.4 Adversarial review as a named, separate role

Two named adversarial personas (`adversarial-reviewer` for code, `adversarial-document-reviewer` for documents). Their job is *not* gating; they are voices in the synthesis. Trade-off: clarity of voice and separation from constructive reviewers, at the cost of one more persona.

### 6.5 Residual work gate

When deep review surfaces things autofix didn't resolve, the system refuses to silently ship. The Operator must dispose of every residual finding via:

- **Apply** — fix it now
- **File** — open a follow-up ticket; finding moves to backlog with a stable ID
- **Accept-with-durable-sink** — explicit acceptance recorded in a durable artifact (knowledge doc, PR description, decision log); not just in the session
- **Stop** — abort the cycle; do not merge

"Findings disappearing into chat" is failure mode F10. The residual work gate is the architectural defense.

### 6.6 Quick-review short-circuit

When the user signals "quick" / "fast" / "light," the Synthesizer defers to harness-native review and skips the full multi-persona pipeline. Respecting intent prevents over-application of process.

---

## 7. Knowledge / memory architecture

### 7.1 Storage

Flat markdown files in `docs/solutions/<category>/*.md`, version-controlled and greppable. YAML frontmatter is required and validated by a schema script (`scripts/validate-frontmatter.py`) to catch silent corruption.

### 7.2 Discoverability

`AGENTS.md` and/or `CLAUDE.md` at the repo root must lead a future agent to discover `docs/solutions/`. The Curator checks this every run and proposes the smallest addition if the path is missing or misleading. *Knowledge that exists but isn't found doesn't compound.*

### 7.3 Capture

The `compound` skill auto-invokes on phrases like "that worked," "it's fixed," "working now." Three subagents run in parallel on a capture call:

- **Context Analyzer** — what was the situation; what made it complete
- **Solution Extractor** — extract the durable lesson
- **Related Docs Finder** — find adjacent docs that should reference or be referenced by this new one

A five-dimensional overlap check determines whether to *update existing* or *create new*. The discoverability gate runs at the end.

### 7.4 Refresh

The `compound-refresh` skill runs periodically (default weekly) over the entire knowledge store. Five outcomes per doc:

- **Keep** — still accurate, still relevant
- **Update** — mostly accurate, needs revision
- **Consolidate** — should merge with another doc
- **Replace** — superseded by a better understanding
- **Delete** — no longer relevant (auto-delete only when implementation gone, problem domain gone, inbound links absent or decorative)

### 7.5 Three memory tiers

The architecture distinguishes three memory tiers that should not be conflated:

1. **Recovery memory** (per-cycle) — checkpoint files, partial run state. Discardable after cycle closes.
2. **Local-cycle memory** (per-issue) — workpad, plan, requirements, decision log. Lives with the issue.
3. **Durable compounding memory** (cross-cycle) — strategy, knowledge store, pulse reports. Surfaces in future cycles.

A factory that conflates these (e.g., putting recovery state into the knowledge store) corrodes the asset.

---

## 8. Human leverage techniques

- **80/20 framing.** The Operator invests time in upstream sharpening and downstream sense-making; execution is delegated to parallel agents in isolated worktrees.
- **One persistent workpad per issue.** A scannable, predictable surface; 10 workpads scan faster than 10 disparate agent outputs.
- **Five-state queue with one waiting-on-human state.** The Operator's inbox is a sortable list of "needs human attention."
- **Tile layout for monitoring.** Recommended terminal layout: orchestrator log, queue, agent activity, browser. Attention distributed across panes by role, not interleaved.
- **One question at a time during brainstorm.** The Brainstormer is forbidden from stacking questions in a single message. Empirically faster to convergence.
- **Synthesis Summary before any artifact lands.** Three-bucket Stated / Inferred / Out summary, the user's last cheap moment to correct scope.
- **Headless mode for orchestration.** Skills with a `mode:headless` variant return structured output and a one-line summary so the Operator can keep flying at altitude.
- **Worktree isolation.** Predicted overlaps surface as merge conflicts the orchestrator handles explicitly. Subagents barred from staging or committing where isolation is unavailable.
- **Default to acting unattended.** "Never ask a human to perform follow-up actions inline — the human is not at the console." Combined with: "Stop early ONLY for a true blocker."
- **Auto-invoke triggers for capture.** "That worked" / "it's fixed" / "problem solved" auto-invoke the capture skill while context is freshest.
- **Decision primer for iterative review.** Rejected findings suppressed via fingerprint + evidence overlap; the user does not re-decide the same thing every round.
- **Explicit non-goals.** `STRATEGY.md` has an optional "Not working on" section. Plans have scope boundaries with "Outside this product's identity" preserved verbatim from origin. *Codifying what to refuse.*
- **Cost routing.** The `model-hierarchy` skill provides a cost rubric so the Conductor (or the agent itself) routes sub-tasks to cheap models. Frees the human from micro-managing spend.

---

## 9. Defenses against the 20 failure modes

| Failure | Defense in this architecture |
|---|---|
| F1 Hallucination Loop | Reviewer panel diversity (different personas, possibly different models); adversarial-reviewer as named separate role |
| F2 Reward hacking | Adversarial-reviewer constructs failure scenarios; testing-reviewer checks assertion strength; cross-persona promotion catches shortcuts |
| F3 Spec-completeness | Brainstormer's gap lenses; spec-flow-analyzer; document reviewers' feasibility & coherence checks |
| F4 Code-quality | The strongest coverage — multi-persona panel includes maintainability, simplicity, pattern-recognition, stack-specific reviewers |
| F5 Cognitive ceiling | 4-concurrent default; 5-state queue with `Human Review` as sortable inbox |
| F6 Cognitive debt | Workpad surfaces what was done; plans capture WHAT not HOW so the human always has a readable model |
| F7 Normalization of deviance | Surprise/finding rate tracked per cycle; refresh-curator periodically reviews accepted patterns |
| F8 Stale-knowledge | Refresh-curator runs explicitly; auto-delete safety conditions prevent over-pruning |
| F9 Spec overfitting | Plans are decision documents not implementation choreography; pre-written implementation in plans is the named anti-pattern |
| F10 Findings disappear | Residual work gate forces explicit disposition; `[claude]`-prefix on agent comments distinguishes them from human asks |
| F11 Renumbering | Stable-ID rule (R/A/F/AE/U/K) — never renumber; splits keep original ID, deletions leave gaps |
| F12 Lethal trifecta | Worktree isolation + sandbox; security-reviewer + security-sentinel as always-on cross-cutting reviewers |
| F13 Missing-config blindspot | Reliability-reviewer; deployment-verification-agent; adversarial-document-reviewer surfaces unstated assumptions |
| F14 Attribution collapse | Stable IDs flow through commits and PRs; PR body has explicit Validation section |
| F15 Single-prompt collapse | Brainstormer's six divergent frames + four research agents in parallel; basis requirement (`direct:` / `external:` / `reasoned:`) |
| F16 Resume-fidelity decay | Workpad is the resume surface; it survives session restarts |
| F17 Parallel agents on shared dirs | Worktree isolation per issue; orchestrator merges serially; no silent overwrites |
| F18 Prose-spec rigor | Acceptance examples (AE-IDs) are concrete and per-scenario; plans carry per-unit test scenarios; orthogonal severity/autofix-class formalizes finding quality |
| F19 Model-floor dependency | Persona prompts can be tuned per-model; `model-hierarchy` skill makes provider/model choice explicit |
| F20 Maintenance asymmetry | The same chain runs for greenfield and maintenance; pulse reports + knowledge store accumulate maintenance signal |

This architecture has the broadest coverage of the four — particularly strong on F4, F8, F9, F10, F11, F15.

---

## 10. Stance on cost and scaling

This architecture is **medium-cost steady-state** with strong amortization. Per-cycle cost is higher than a one-shot agent because of the persona panel and the researcher fan-out — but the knowledge store reduces the *effective* cost of subsequent cycles in the same domain. After 20–50 cycles in a stable domain, the "cycle 21" is materially cheaper than "cycle 1" because researchers find prior solutions immediately.

For solo operation, the Operator can run 2–4 issues in parallel comfortably. The 5-state queue is the sortable inbox.

For team scale-up, the architecture splits cleanly:

- **Strategist-human** owns `STRATEGY.md` and prioritization; talks to product/business
- **Operator-human(s)** run the daily queue; many can share if partitioned by label/area
- **Curator-human** owns the knowledge store's health

Multiple Operators on the same project work because the workpad-per-issue + worktree-per-issue model isolates work. Conflicts surface at merge time.

The biggest scaling risk is **persona explosion.** Adding a reviewer persona is cheap and tempting; the population grows from 5 to 50 to 500. The architecture mandates a periodic persona-pruning ritual (a reviewer that produces only `safe_auto` advisory findings for 50 cycles is a candidate for retirement).

---

## 11. Implementation roadmap

**Stage 1 — Strategy + Brainstormer + Workpad.** Establish the three load-bearing artifacts (`STRATEGY.md`, the brainstorm-with-IDs format, the workpad protocol). Run cycles end-to-end with one Implementer and only the harness-native review. Goal: validate the upstream artifact discipline produces clearer plans.

**Stage 2 — Planner + WHAT-not-HOW discipline.** Add the Planner persona; enforce U-IDs and the WHAT/HOW separation. Goal: validate that plans produce more recoverable cycles.

**Stage 3 — Reviewer panel (small).** Add the four always-on code reviewers + the document reviewers + the synthesizer. Cross-persona promotion goes live. Goal: validate that synthesized findings are actionable.

**Stage 4 — Knowledge store.** Add the Knowledge Curator and the discoverability gate. Establish the two-track template. Goal: cycle *n+1* should be measurably cheaper than cycle *n* in the same domain.

**Stage 5 — Researcher fan-out.** Add the researcher agents called by the Brainstormer and Planner. Goal: persona output quality should rise with grounding.

**Stage 6 — Adversarial reviewers + residual gate.** Add the named adversarial roles and the residual work gate. Goal: catch the failure modes the constructive panel misses.

**Stage 7 — Refresh discipline.** Add the refresh skill and run it weekly. Goal: knowledge store stays net-positive for compounding.

**Stage 8 — Stack-specific reviewers + tiered ceremony.** Add language-specific reviewers; let issues opt into Lightweight / Standard / Deep tiers. Goal: cycle cost scales to work scope.

Each stage runs for at least 5 issues before the next is added. The sequence preserves the rule that *each new mechanism must justify its existence in operational reality before becoming a hard requirement.*

---

## 12. What this architecture is not

- **Not a single-agent factory.** Persona specialization is the central bet.
- **Not "the Specification Refinery with reviewers." ** It does not run a layered-spec / revelation-cycle. The artifact lifecycle is brainstorm → plan → workpad → PR, not layer-by-layer probing.
- **Not waterfall.** Phases are scoped to a single issue; ceremony is tiered; the cycle time is hours, not months.
- **Not a no-human-review architecture.** The Operator approves at `Human Review` state and disposes residual findings.
- **Not an orchestration framework.** The orchestrator is structurally separate; this spec describes the methodology that the orchestrator runs, not the orchestrator's internals.

---

## 13. Open questions

1. **Persona granularity.** When does a new persona earn its keep vs. when is it a dilution of an existing one? The architecture mandates pruning but doesn't specify the test.
2. **Cross-persona promotion thresholds.** "Two reviewers spotting the same issue raises priority" — does the threshold scale with reviewer count? With confidence scores? With reviewer family diversity?
3. **Stable-ID collisions across projects.** R-7 in project A and R-7 in project B — when knowledge documents reference both, namespace prefix becomes essential. How rigid?
4. **Adversarial isolation.** The adversarial reviewer reads the same artifact as the constructive ones. Is that enough independence? Or should adversarial run on a different model family?
5. **Knowledge curation cadence at scale.** Weekly refresh is a default. The right cadence for a 1,000-document store is probably different from a 50-document store. Self-tuning?
6. **The "agents that write each other's instructions" thesis.** This architecture has agents that write *artifacts* other agents consume; it does not have agents that update other agents' system prompts. Whether that move belongs here is unresolved.
7. **Tiered ceremony for review.** Brainstorm and plan tiers exist; review tiers (Quick / Standard / Deep) are implicit. Should they be first-class?

---

*End of architecture spec — Compound Atelier v0.1*
