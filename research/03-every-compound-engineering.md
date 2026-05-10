# Every.to Compound Engineering — Research Report

**Sources covered:**
- https://every.to/guides/compound-engineering (blocked by 403 / Cloudflare; the guide's thesis was reconstructed from the plugin's READMEs and skill docs, which the guide is the textual companion to)
- https://github.com/EveryInc/compound-engineering-plugin — root `README.md`, `AGENTS.md`, `CHANGELOG.md`, `plugins/compound-engineering/README.md`, and `docs/skills/*.md` for the major skills (`ce-strategy`, `ce-ideate`, `ce-brainstorm`, `ce-plan`, `ce-work`, `ce-debug`, `ce-code-review`, `ce-doc-review`, `ce-compound`, `ce-compound-refresh`, `ce-optimize`, `ce-product-pulse`, `ce-simplify-code`, `ce-polish-beta`)
- https://github.com/EveryInc/compound-knowledge-plugin — root `README.md`, plugin `README.md`, `AGENTS.md`, and the `kw-compound` skill plus the `strategic-alignment-reviewer`, `data-accuracy-reviewer`, `knowledge-base-researcher`, `stale-knowledge-checker` agents
- Referenced (not accessible from this sandbox but cited verbatim in the plugin README): https://every.to/chain-of-thought/compound-engineering-how-every-codes-with-agents and https://every.to/source-code/my-ai-had-already-fixed-the-code-before-i-saw-it and https://every.to/p/the-agent-that-saved-my-brain

**Date:** 2026-05-10

---

## Executive summary

Compound engineering, as practiced by Every Inc., is the thesis that **each unit of engineering work should make the next unit easier, not harder**. It is an explicit inversion of the conventional "every feature adds technical debt" curve. The mental model is borrowed from compound interest: small, durable artifacts produced *per cycle* — a sharpened brainstorm, a guardrail-style plan, a calibrated review verdict, a captured learning — get re-read by future cycles and bend the cost curve downward over time. The plugin embodies the methodology as 37+ skills and 50+ agents that orchestrate a single human running many specialized sub-agents.

The core slogan from the root `README.md` is unusually load-bearing for a methodology: **"80% is in planning and review, 20% is in execution."** Execution is treated as the cheap, parallelizable, recoverable part; the expensive moments are upstream (deciding what to build, what shape it should take, what guardrails the implementer must honor) and downstream (catching pattern-level issues during review and codifying lessons so the same investigation never happens twice).

What actually compounds is a small, deliberately-bounded set of durable artifacts that future agents are *engineered to consult*:

- `STRATEGY.md` (the upstream anchor) and `docs/pulse-reports/` (the downstream read on what users experienced) bracket the loop with product reality.
- `docs/brainstorms/*-requirements.md` carry stable identifiers (R-IDs, A-IDs, F-IDs, AE-IDs) for requirements, actors, key flows, and acceptance examples. These flow into plans.
- `docs/plans/*-plan.md` carry stable U-IDs (Implementation Units) that flow into commit messages, PR descriptions, and test scenarios. Plans are guardrails over choreography — "WHAT, not HOW."
- `docs/solutions/[category]/*.md` is the knowledge store of solved problems, with YAML frontmatter (`module`, `tags`, `problem_type`, `confidence`, `created`, `source`). Future runs of `ce-plan`, `ce-ideate`, `ce-debug`, `ce-work` automatically consult this folder.
- `docs/knowledge/*.md` is the equivalent store in the knowledge-work plugin.

Several recurring design moves are explicit:

1. **Specialized agents, not a generalist.** Reviewers are persona-shaped (`ce-correctness-reviewer`, `ce-security-sentinel`, `ce-dhh-rails-reviewer`, `ce-adversarial-reviewer`, etc.). Persona selection is diff-aware ("agent judgment, not keyword matching") and dispatched in parallel.
2. **Stable identifiers across the chain.** R/A/F/AE → U → commit messages → PR. Renumbering is forbidden so cross-references survive plan edits.
3. **Confidence gating and cross-persona promotion.** Two reviewers spotting the same issue raises its priority; reviewers express severity (P0-P3) and an orthogonal autofix class (`safe_auto`, `gated_auto`, `manual`, `advisory`).
4. **Knowledge capture is a first-class step in the loop, not a postscript.** `/ce-compound` runs at the moment context is freshest, with auto-invoke triggers (`"that worked"`, `"it's fixed"`).
5. **Maintenance of the knowledge store is a separate, deliberate skill** (`/ce-compound-refresh`) — otherwise the store decays and the compounding inverts.

The whole shape can be read as "build the engineering org's writing habits, then make sure the agents read what gets written."

---

## The compounding mechanism

What compounds: **durable artifacts on disk that future agents are wired to read.** Not session memory, not chat history, not heuristics encoded in weights — flat markdown files in the repo, git-tracked and greppable.

The loop that produces compounding (the central core in the root `README.md`):

> "The core loop is: brainstorm the requirements, plan the implementation, work through the plan, review the result, compound the learning, then repeat with better context."

Five mechanisms make iteration `n+1` cheaper than iteration `n`:

1. **Reusable upstream anchors.** `STRATEGY.md` is written once and read by every downstream skill (`ce-ideate`, `ce-brainstorm`, `ce-plan`, `ce-product-pulse`). Anything strategy-relevant in cycle `n` automatically biases cycle `n+1` without re-prompting.
2. **Stable IDs across artifacts.** R-IDs (requirements), A-IDs (actors), F-IDs (key flows), AE-IDs (acceptance examples) from brainstorm flow into the plan's Requirements section and into test scenarios (`Covers AE3. <scenario>`); plans then expose U-IDs that survive reordering/splitting/deletion. Cross-references in PRs and downstream conversations don't go stale.
3. **Knowledge store auto-consulted at planning time.** `ce-learnings-researcher` is a Phase-1 research agent inside `/ce-plan`; `/ce-ideate` reads `docs/solutions/` during grounding; `/ce-debug` reads it for prior context. The first time you solve "N+1 query in brief generation" takes 30 minutes; the second time, the doc surfaces automatically. Quote from `ce-compound`: *"The first time you solve 'N+1 query in brief generation' takes 30 minutes of research; the second time, you find the doc and the fix takes 2 minutes."*
4. **Pattern-promotion during review.** Cross-persona agreement (two reviewers spot the same issue) raises severity; learnings researcher is one of the always-on reviewers; review findings flag candidates for new learnings.
5. **Periodic hygiene.** `/ce-compound-refresh` reviews learnings against the current codebase under a five-outcome model (Keep / Update / Consolidate / Replace / Delete). Without it, the compounding inverts — stale learnings make work harder, not easier.

The dual anti-decay mechanism is critical: **capture (`/ce-compound`) without maintenance (`/ce-compound-refresh`) corrodes the asset.** The skill doc for refresh states this explicitly: *"Without active maintenance, the knowledge store loses trustworthiness. Future agents (and humans) consult docs that are partially wrong, take advice that no longer applies, and the compound effect inverts."*

A subtler compounding mechanism: **discoverability is enforced.** Every `/ce-compound` run checks whether `AGENTS.md` / `CLAUDE.md` would lead a future agent to discover `docs/solutions/`, and proposes the smallest addition that surfaces it. Knowledge that exists but isn't found doesn't compound.

---

## Agents and roles

The plugin ships 50+ named subagents. They are grouped functionally; only the human and the skills call them directly.

### Reviewers (code)

- `ce-correctness-reviewer` — logic errors, edge cases, state bugs (always-on).
- `ce-testing-reviewer` — test coverage gaps, weak assertions (always-on).
- `ce-maintainability-reviewer` — coupling, complexity, naming, dead code (always-on).
- `ce-project-standards-reviewer` — CLAUDE.md / AGENTS.md compliance (always-on).
- `ce-agent-native-reviewer` — verifies features are agent-native (action + context parity).
- `ce-security-reviewer` / `ce-security-sentinel` — exploitable vulnerabilities; the sentinel does broader audits.
- `ce-performance-reviewer` / `ce-performance-oracle` — runtime performance with calibrated confidence; oracle is the deeper analyst.
- `ce-reliability-reviewer` — production reliability and failure modes.
- `ce-api-contract-reviewer` — detect breaking API changes.
- `ce-architecture-strategist` — architectural decisions and compliance.
- `ce-data-integrity-guardian`, `ce-data-migrations-reviewer`, `ce-data-migration-expert`, `ce-schema-drift-detector`, `ce-deployment-verification-agent` — database/migration safety stack.
- `ce-pattern-recognition-specialist` — patterns and anti-patterns.
- `ce-code-simplicity-reviewer` — final pass for simplicity.
- `ce-adversarial-reviewer` — explicitly *constructs failure scenarios to break implementations across component boundaries*; this is the named adversarial peer.
- Stack-specific: `ce-dhh-rails-reviewer`, `ce-kieran-rails-reviewer`, `ce-kieran-python-reviewer`, `ce-kieran-typescript-reviewer`, `ce-julik-frontend-races-reviewer`, `ce-swift-ios-reviewer` — these encode named-expert personas (DHH for Rails, Kieran's strict conventions per language, Julik on JS race conditions).

### Reviewers (document)

- `ce-coherence-reviewer` (always-on) — internal consistency, contradictions, terminology drift.
- `ce-feasibility-reviewer` (always-on) — will this survive contact with reality.
- `ce-design-lens-reviewer` — missing design decisions, interaction states, AI slop risk.
- `ce-product-lens-reviewer` — challenge problem framing, scope, goal misalignment.
- `ce-scope-guardian-reviewer` — challenge unjustified complexity, scope creep, premature abstractions.
- `ce-security-lens-reviewer` — plan-level auth/data/API gaps.
- `ce-adversarial-document-reviewer` — challenges premises, surfaces unstated assumptions, stress-tests decisions.

### Researchers

- `ce-best-practices-researcher`, `ce-framework-docs-researcher`, `ce-web-researcher` — external grounding.
- `ce-repo-research-analyst` — local conventions, architecture, technology stack.
- `ce-learnings-researcher` — searches `docs/solutions/` for relevant past learnings. **This is the agent that closes the knowledge-store loop.**
- `ce-git-history-analyzer` — code evolution context.
- `ce-issue-intelligence-analyst` — clusters GitHub issue themes.
- `ce-session-historian` — searches prior Claude Code / Codex / Cursor sessions across harnesses.
- `ce-slack-researcher` — organizational context from Slack.
- `ce-spec-flow-analyzer` — edge-case completeness on user flows.

### Design / workflow / docs

- `ce-design-iterator`, `ce-figma-design-sync`, `ce-design-implementation-reviewer` — design loop agents.
- `ce-pr-comment-resolver` — addresses PR comments and implements fixes.
- `ce-ankane-readme-writer` — README authorship in a specific style.

### Compound Knowledge plugin (knowledge-work twin)

Six skills (`/kw:brainstorm`, `/kw:plan`, `/kw:confidence`, `/kw:review`, `/kw:work`, `/kw:compound`), three research agents (`knowledge-base-researcher`, `past-work-researcher`, `stale-knowledge-checker`), and two review agents (`strategic-alignment-reviewer`, `data-accuracy-reviewer`). The CK agents return text only; only the orchestrating skill writes files — a deliberate concurrency/safety constraint copied verbatim from the CE plugin's "no silent overwrites" stance.

---

## Workflows and cycles

The canonical full cycle from `plugins/compound-engineering/README.md`:

```
/ce-strategy   (upstream anchor — written once, maintained)
   |
   v
/ce-ideate     "What's worth exploring?"        → docs/ideation/*
   |
   v
/ce-brainstorm "What does this need to be?"     → docs/brainstorms/*-requirements.md (R/A/F/AE-IDs)
   |
   v
/ce-plan       "What's needed to accomplish?"   → docs/plans/*-plan.md (U-IDs)
   |
   v
/ce-work       "Build it."                      → commits + PR
   |
   v
/ce-code-review  (Tier 2 escalation; Tier 1 is harness-native)
   |
   v
/ce-compound   → docs/solutions/[category]/*.md (knowledge captured)
   |
   v
/ce-product-pulse  → docs/pulse-reports/*  (closes downstream loop)
```

Numbered description of how compounding happens at each step:

1. **`/ce-strategy`** — Interview-driven, Rumelt-inspired (diagnosis / guiding policy / coherent action), written to repo-root `STRATEGY.md` with a `last_updated` frontmatter. Pushback rules per section. Re-runs preserve strong sections. This document is read as grounding by every downstream skill — a single edit propagates across all future cycles.

2. **`/ce-ideate`** — Parallel grounding agents (codebase, learnings, external prior art, optional Slack, issue intelligence) feed six divergent ideation sub-agents (pain & friction, inversion, assumption-breaking, leverage & compounding, cross-domain analogy, constraint-flipping). Topic is decomposed into 3-5 *orthogonal axes*; an axis-coverage check forces dispatch into untouched areas. Every surviving candidate carries a tagged **basis** — `direct:` (quoted evidence), `external:` (named prior art), or `reasoned:` (written-out argument). Survivors come with a rejection summary.

3. **`/ce-brainstorm`** — One question per turn (a discipline forced by the harness's blocking question tool). Named "gap lenses" (Evidence, Specificity, Counterfactual, Attachment, Durability) pressure-test premises before generating approaches. 2-3 concrete approaches with tradeoffs; a Synthesis Summary (Stated / Inferred / Out) before the doc lands. Output: a right-sized requirements doc with R/A/F/AE-IDs.

4. **`/ce-plan`** — Up to 5 research agents in parallel (`repo-research-analyst`, `learnings-researcher`, `framework-docs-researcher`, `best-practices-researcher`, `spec-flow-analyzer`). After plan is written, a confidence check runs automatically, scores sections, dispatches targeted sub-agents (correctness reviewer for unit lists, data-integrity guardian for migrations, architecture strategist for technical decisions) to strengthen weak sections. Plans capture **WHAT**, not **HOW**: decisions, scope boundaries, atomic units, files touched, test scenarios per unit, risks — but explicitly not exact API signatures or step-by-step shell commands. Plans carry U-IDs that never renumber.

5. **`/ce-work`** — Plan-aware idempotency check before each task (don't reimplement already-shipped work). Worktree-isolated parallel subagents for independent units (no silent overwrites). Test-quality gates before "done." Tiered review (harness-native default, escalate to `ce-code-review` for sensitive/large diffs). Residual Work Gate forces apply / file / accept-with-durable-sink / stop on findings. Every PR carries a `Post-Deploy Monitoring & Validation` section.

6. **`/ce-code-review`** — Diff-aware persona selection (4 always-on code reviewers + 2 CE always-on agents, plus cross-cutting and stack-specific reviewers chosen for what was actually touched). Parallel dispatch. Synthesis pipeline: validate → anchor → dedupe → **promote on cross-persona agreement** → resolve contradictions → auto-promote `safe_auto` → route. Findings carry orthogonal severity (P0-P3) and autofix class.

7. **`/ce-compound`** — Auto-invoked on phrases like *"that worked"*, *"it's fixed"*, *"working now"*. Full mode dispatches three subagents in parallel (Context Analyzer / Solution Extractor / Related Docs Finder). Overlap detection (five dimensions) routes high-overlap to *update existing doc*, not create a duplicate. Discoverability check ensures `AGENTS.md` surfaces the knowledge store. Selective refresh trigger handed to `/ce-compound-refresh` only when a specific older doc is suspect.

8. **`/ce-compound-refresh`** — Maintenance counterpart. Five explicit outcomes (Keep / Update / Consolidate / Replace / Delete). Inbound-link classification (decorative vs substantive) determines whether deletion is safe. Auto-delete fires only when implementation is gone, problem domain is gone, and inbound links are absent or decorative — all three.

9. **`/ce-product-pulse`** — Single-page (30-40 lines, hard), time-windowed report saved to `docs/pulse-reports/`. PII-free. Read-only invariant. Past pulses form a browseable timeline of user outcomes. Seeds future strategy / brainstorms with real signal.

Two important specialized variants of the loop:

- **`/ce-debug`** is the bug-shaped sibling to `/ce-work`. It runs the same compounding hygiene (causal-chain gate before fix, prediction per uncertain link, assumption audit, test-first fix, conditional defense-in-depth). Wrong-prediction-but-fix-works is explicitly flagged as a symptom fix.
- **`/ce-optimize`** is metric-driven parallel experimentation (Karpathy-inspired autoresearch generalized for multi-file changes). Three-tier evaluation (degenerate gates → LLM-as-judge → diagnostics). Persistence discipline: *"If you produce a results table without writing those results to disk first, you have a bug."* Strategy digests from each batch drive the next batch's hypotheses — a tight micro-compounding loop within a session.

---

## Specification / brief methodology

The brief/spec format is the most fully specified artifact in the methodology. Three observations:

**1. Briefs are tiered to scope.** `/ce-brainstorm` picks a tier: Lightweight / Standard / Deep / Deep-product. Ceremony scales to work, not the other way around. Lightweight emits no doc at all if alignment is brief; Deep-product additionally establishes product shape (actors, core outcome, positioning, durability) instead of inheriting it.

**2. Briefs are stable-ID-bearing.** A `/ce-brainstorm` requirements doc carries:
- **R-IDs** (Requirements) — flow into the plan's Requirements section.
- **A-IDs** (Actors) — carry forward into behavior/permissions.
- **F-IDs** (Key Flows) — cite into implementation units that realize them.
- **AE-IDs** (Acceptance Examples) — cite into test scenarios that enforce them. Format: `Covers AE3. <scenario>`.

Every section of the origin doc is verified against the plan before finalization. "Nothing silently drops."

**3. Briefs separate Stated / Inferred / Out before any artifact lands.** The Synthesis Summary is the last cheap moment to correct scope. In headless mode, `Inferred` bets route to a `## Assumptions` section so downstream review can scrutinize them. This is explicit epistemic hygiene at the artifact level.

For plans:

- Plans are *decision documents with execution guardrails*, not implementation choreography. Scope, decisions, units, files, test scenarios, risks — but not signatures or pseudo-code dressed as spec.
- Plans carry U-IDs (`U1`, `U2`, etc.); the stability rule is **never renumber** after reordering, splitting, or deleting. Splits keep the original U-ID on the original concept; new units take next unused number; deletions leave gaps.
- Test scenarios per unit are categorized: happy path, edge cases (boundaries, empty/nil, concurrency), error/failure paths, integration. Each scenario names input/action/expected outcome.

This separation — brainstorm decides product behavior, plan decides execution guardrails, work figures out HOW with code in front of it — is what makes plans portable across implementer (human or AI) and across weeks of code change.

---

## Review and feedback patterns

This is the single richest area of the methodology. Four patterns deserve attention.

**1. Persona-based parallel review with synthesis.** `/ce-code-review` and `/ce-doc-review` both follow the same shape: diff-aware (or doc-content-aware) persona selection → parallel dispatch → synthesis pipeline → routing. Persona selection is *agent judgment over actual content, not keyword matching*. Synthesis is more than concatenation: it validates against schema, anchors findings to actual content, deduplicates across personas, **promotes on cross-persona agreement** (two reviewers spotting the same issue raises priority), resolves contradictions (different personas disagree about what to do), and routes by tier.

**2. Severity (P0-P3) and autofix class are orthogonal.** From `ce-code-review`:

> "Severity answers urgency (P0=critical breakage, P3=user discretion). The autofix class answers who acts next: `safe_auto` → review-fixer enters the in-skill fixer queue automatically; `gated_auto` → fix exists but changes behavior, contracts, or sensitive boundaries — routes to a downstream resolver or human; `manual` → actionable work for handoff; `advisory` → report-only output."

This means findings have both *how bad* and *who owns the next move*, which lets autofix sweep low-risk hygiene without users decoupling from policy decisions.

**3. Adversarial peer review is a first-class named role.** `ce-adversarial-reviewer` (code) and `ce-adversarial-document-reviewer` (docs) are listed alongside the constructive reviewers. The code adversarial reviewer's job: *"Construct failure scenarios to break implementations across component boundaries."* The doc adversarial reviewer's job: *"Challenge premises, surface unstated assumptions, and stress-test decisions."* They are not gates; they are voices in the synthesis.

**4. Round-to-round suppression.** `/ce-doc-review` carries a "decision primer" between rounds: applied findings flow forward so the next round can verify the fix landed; rejected findings (skip / defer / acknowledge) are suppressed via fingerprint + evidence-substring overlap matching so the same issue does not re-surface. This is what makes iterative review actually iterate instead of looping.

The bulk-action preview (when the user picks "Auto-resolve with best judgment" or "Append to Open Questions") is a safety valve before mass changes commit.

---

## Knowledge / memory architecture

The Compound Knowledge plugin is the explicit cleanest statement of the architecture:

> "/kw:plan searches docs/knowledge/ for past learnings saved by /kw:compound. Knowledge compounds."

The architecture has five components:

**1. Flat-file storage.** `docs/knowledge/` (CK) and `docs/solutions/[category]/*.md` (CE). Plain markdown, git-tracked, greppable. The CK README says explicitly: *"The knowledge files are plain markdown, git-tracked, and greppable."*

**2. YAML frontmatter for search.** From the CK example:

```yaml
---
type: insight
tags: [trials, conversion, campaigns]
confidence: high
created: 2026-02-15
source: Q1 trial campaign analysis
---
```

In CE, frontmatter includes `module`, `tags`, `problem_type`, plus `last_updated` for refresh tracking. Validated via `scripts/validate-frontmatter.py` to catch silent corruption.

**3. Two-track classification.** CE: bug track (Symptoms / What Didn't Work / Solution / Why This Works / Prevention) vs knowledge track (Context / Guidance / Why This Matters / When to Apply / Examples). CK: insight / playbook / correction / pattern. The track determines section order and frontmatter fields; forcing the wrong shape onto a learning produces structurally wrong docs.

**4. Mandatory anti-duplication.** Five-dimensional overlap check (problem statement, root cause, solution approach, referenced files, prevention rules). High overlap (4-5 dimensions) updates the existing doc rather than creating a duplicate. *"Two docs describing the same problem inevitably drift apart."*

**5. Mandatory discoverability.** The CE compound skill checks every run whether `AGENTS.md` / `CLAUDE.md` surfaces `docs/solutions/`, and proposes the minimal addition if not. *"The check runs every time because the knowledge store only compounds value when it's findable."*

**Stale-knowledge handling.** CK's `stale-knowledge-checker` is run by `/kw:compound` automatically and surfaces existing entries that may be contradicted by the new learning. CE's separate `/ce-compound-refresh` skill maintains the store under five outcomes (Keep / Update / Consolidate / Replace / Delete) with strict auto-delete safety conditions (all three: implementation gone, problem domain gone, inbound citations absent or decorative).

**Session memory.** `ce-session-historian` (CE) searches prior sessions across Claude Code, Codex, and Cursor — a memory layer separate from the knowledge store, used for *"what was tried before, what didn't work, key decisions"*. Findings are folded into "What Didn't Work" (bug track) or "Context" (knowledge track) when running `/ce-compound`. Off by default because of token cost.

**Strategy as memory.** `STRATEGY.md` is the smallest, most persistent piece of memory; the `last_updated` field lets downstream skills flag it as potentially stale.

---

## Human leverage techniques

The plugin design encodes several explicit techniques for a human steering many agents.

**1. 80/20 framing.** *"80% is in planning and review, 20% is in execution."* The human invests time in upstream sharpening and downstream sense-making; execution is delegated to parallel agents in isolated worktrees.

**2. Tiered ceremony.** Every skill right-sizes (Lightweight / Standard / Deep). Trivial bug fixes don't require the full chain. The human chooses where the work warrants ceremony.

**3. One-question-at-a-time during brainstorm.** Stacking three questions in one message produces diluted answers; the discipline forces sharpness. *"Empirically faster to convergence."*

**4. Synthesis Summary before any artifact lands.** A three-bucket Stated / Inferred / Out summary is the user's *last cheap moment* to correct scope. Failing to read it costs implementation cycles.

**5. Headless mode for orchestration.** Skills with a `mode:headless` variant return structured output and emit a one-line summary (e.g., `"Doc review applied 2 fixes. 3 decisions, 1 FYI remain."`) above the caller's next menu — so the human can keep flying at altitude.

**6. Worktree isolation for parallel agents.** Predicted overlaps surface as merge conflicts the orchestrator handles explicitly. Where isolation is unavailable, subagents are barred from staging or committing — the orchestrator merges serially. **No silent data loss.**

**7. Residual Work Gate.** When deep review surfaces things autofix didn't resolve, the system refuses to silently ship; it forces the user into apply / file ticket / accept-with-durable-sink / stop. *"'Accept' requires a real durable record — findings can't live only in the session."*

**8. Quick-review short-circuit.** When the user says "quick", "fast", or "light", `/ce-code-review` defers to the harness-native `/review` instead of dispatching the full multi-agent pipeline. Respecting intent prevents over-application.

**9. Auto-invoke triggers for capture.** Phrases like "that worked", "it's fixed", "problem solved" auto-invoke `/ce-compound` so capture happens at the moment context is freshest — not at session-end clutter.

**10. Decision primer for iterative review.** Round-to-round, rejected findings are suppressed via fingerprint + evidence overlap. Without this, the same finding re-surfaces every round and the user re-decides the same thing.

**11. Confidence check as a callable interrupt.** `/kw:confidence` (CK) can be invoked at any point — *"Pauses to honestly assess what Claude knows and doesn't know — in plain language, not a table."* This is a deliberate intervention point.

**12. Explicit non-goals.** `STRATEGY.md` has an optional "Not working on" section. Plans have scope boundaries with "Outside this product's identity" preserved verbatim from origin. The methodology codifies *what to refuse*.

---

## Pitfalls and lessons learned

These come directly from the plugins' design rationale.

- **Pre-written implementation in plans is brittle.** *"Plans that pre-write implementation are brittle: pre-committed signatures don't compile, choreographed steps go stale, and they rob the implementer of judgment that should be made with current context."* The WHAT/HOW separation exists because the opposite has been observed to fail.
- **Renumbering breaks references.** U-IDs and R/A/F/AE-IDs exist because numbered units get renumbered during edits and every downstream PR / chat / blocker reference silently becomes wrong.
- **Two docs on the same problem inevitably drift apart.** This is why `ce-compound` updates the existing doc rather than creating duplicates, and why `ce-compound-refresh` consolidates.
- **Wrong hypothesis vs wrong assumption.** `ce-debug` enforces an assumption audit because *"Many 'wrong hypotheses' are actually correct hypotheses tested against a wrong assumption."*
- **Fix-without-investigation traps.** *"When a prediction is wrong but a fix appears to work, the skill flags it: you found a symptom, not the cause."*
- **Stale knowledge inverts compounding.** Without `/ce-compound-refresh`, *"bad learnings make work harder, not easier."*
- **Parallel agents on shared directories silently lose data.** Worktree isolation, or the orchestrator forbids subagents from staging/committing.
- **Findings disappearing into chat is a failure mode.** Residual Work Gate; durable sinks; "Append to Open Questions."
- **Single-prompt ideation collapses into the model's most-trained directions.** Six divergent frames in `ce-ideate` exist specifically to counter this; basis requirement + comprehensive grounding are the dual anti-slop mechanism.
- **Persona advice that doesn't fit the doc shape produces noise.** `/ce-doc-review` scopes persona techniques by doc shape (premise-level on requirements, implementation-level on plans).
- **Discoverability silently kills compounding.** Knowledge that exists but isn't surfaced in `AGENTS.md` / `CLAUDE.md` is invisible to future agents.
- **Long strategy docs aren't read.** `STRATEGY.md` is constrained to 1-2 pages on purpose. *"If you find yourself wanting more sections, the answer is usually 'those belong in ce-brainstorm or the issue tracker, not in strategy.'"*
- **Caching surprises.** From `AGENTS.md`: plugin agents and skills cache at session start, so iterating on agent prose inside the same session tests pre-edit content.
- **Author lock-in is acceptable to the author.** The CE README contains an unusually frank note: *"I do not accept outside contributions for any of my projects … I'd also have to worry about other 'stakeholders,' which seems unwise for tools I mostly make for myself for free … it's the only way I can move at this velocity and keep my sanity."* For a methodology meant to scale to teams, this is a lessons-learned signal: tightly-couple to one author or split the asset.

---

## Notable quotes

1. *"Each unit of engineering work should make subsequent units easier -- not harder."* — `compound-engineering-plugin/README.md` (Philosophy section, root)
2. *"Traditional development accumulates technical debt. … Compound engineering inverts this. 80% is in planning and review, 20% is in execution."* — `compound-engineering-plugin/README.md`
3. *"A good brainstorm makes the plan sharper. A good plan makes execution smaller. A good review catches the pattern, not just the bug. A good compound note means the next agent does not have to learn the same lesson from scratch."* — `compound-engineering-plugin/README.md`
4. *"The core loop is: brainstorm the requirements, plan the implementation, work through the plan, review the result, compound the learning, then repeat with better context."* — `compound-engineering-plugin/README.md`
5. *"Each cycle compounds: brainstorms sharpen plans, plans inform future plans, reviews catch more issues, patterns get documented."* — `compound-engineering-plugin/README.md`
6. *"Decisions belong in the plan; implementation choices belong at execution time."* — `docs/skills/ce-plan.md`
7. *"The first time you solve 'N+1 query in brief generation' takes 30 minutes of research; the second time, you find the doc and the fix takes 2 minutes."* — `docs/skills/ce-compound.md`
8. *"Knowledge only compounds value when it's findable."* — `docs/skills/ce-compound.md` (Discoverability check)
9. *"If you produce a results table without writing those results to disk first, you have a bug. Conversation context is for the user; the experiment log file is for durability."* — `docs/skills/ce-optimize.md`
10. *"Each cycle makes the next one faster. /kw:plan searches docs/knowledge/ for past learnings saved by /kw:compound. Knowledge compounds."* — `compound-knowledge-plugin/README.md`
11. *"Construct failure scenarios to break implementations across component boundaries."* — `ce-adversarial-reviewer` description (plugin README)
12. *"Without active maintenance, the knowledge store loses trustworthiness. … the compound effect inverts: bad learnings make work harder, not easier."* — `docs/skills/ce-compound-refresh.md`

---

## Recommended additional sources

1. **https://every.to/chain-of-thought/compound-engineering-how-every-codes-with-agents** — The full narrative version of the methodology, cited as the canonical writeup in the plugin README. Cloudflare-blocked from this sandbox; needs a human-driven fetch.
2. **https://every.to/source-code/my-ai-had-already-fixed-the-code-before-i-saw-it** — The origin-story article for the compound-engineering thesis, also cited as canonical.
3. **https://every.to/p/the-agent-that-saved-my-brain** — Companion narrative for the Compound Knowledge plugin (cited in `compound-knowledge-plugin/README.md`).
4. **Richard Rumelt, *Good Strategy Bad Strategy*** — explicitly named in `ce-strategy` as the source for the diagnosis / guiding policy / coherent action structure and the "bad strategy" anti-patterns the interview pushes past. Worth scanning for the methodology framing.
5. **Andrej Karpathy on autoresearch / experiment loops** — cited as the inspiration for `ce-optimize`; the parallel-experiments-with-judge pattern is the same idea generalized for multi-file software changes.

---

## Open questions for synthesis

1. **Spec-driven vs compound: where do they intersect?** The baseline `spec-driven-ai-dev.md` (project context) emphasizes spec authorship up front; compound engineering puts equally heavy weight on *retroactive* knowledge capture (`/ce-compound`). Are these complementary tiers (spec = forward, compound = backward), or do they overlap on the brainstorm/plan artifacts?
2. **What's the right artifact granularity?** Every uses brainstorm + plan + solution as three separate artifact classes with different lifecycles. Some other agent-coding methodologies collapse these. The lead designer should consider whether collapsing them recovers velocity at the cost of compounding.
3. **Adversarial peer review as a separate role vs an attribute of every reviewer.** Every elects to have named adversarial reviewers (`ce-adversarial-reviewer`, `ce-adversarial-document-reviewer`) rather than asking every reviewer to be adversarial. Trade-off: clarity of voice vs reviewer-count growth.
4. **Stable-ID discipline costs.** R/A/F/AE/U-IDs require tooling and discipline to maintain. Are they essential to compounding, or do they ride along with another mechanism (rich-enough plans + diff-aware review) that would work without them?
5. **The "agents that write each other's instructions" thesis is *not* explicitly named** in either plugin's docs. The plugins have meta-layers (`/ce-compound` writes docs that `/ce-plan` reads; `/ce-compound-refresh` curates the docs); but I did not find evidence of *agents updating other agents' system prompts*. This may be in the every.to articles I could not access — worth confirming during synthesis.
6. **Single-author velocity vs team scale.** The CE README explicitly trades collaboration for velocity. Software-factory architectures aimed at "one human, many agents, eventually a small team" will need to decide where contribution gates and codified-judgment gates sit.
7. **Knowledge-store curation cost at scale.** `/ce-compound-refresh` is a deliberate maintenance burden. Without it, the asset decays. What's the curation cadence that keeps compounding net-positive vs net-negative?
8. **Headless mode as the "team interface."** Many skills support `mode:headless` returning structured text. This is the natural composition point for higher-level orchestration. The lead designer might consider whether all factory skills should expose a headless mode as a contract.
9. **Strategy and pulse-report as the *only* persistent non-versioned-by-code state.** `STRATEGY.md` (upstream anchor) and `docs/pulse-reports/` (downstream read on outcomes) bracket the loop with product reality. This is a much smaller persistent surface than typical PM tooling — worth examining whether more or less product memory belongs in the factory.
10. **Failure recovery vs compounding.** Crash recovery in `/ce-optimize` (per-experiment `result.yaml` markers, resume on restart) is a different shape of memory than the knowledge store. A robust factory may need three memory tiers: immediate (recovery), local-cycle (plan + brainstorm), durable-compounding (solutions + strategy).
