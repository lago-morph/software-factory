# Next-agent dispatch prompt — Phase 5 entry (after context-slimming implementation)

**Generated:** 2026-05-25 (Phase 4 of v3 closed, retrospective PR #157 open).
**Designed for:** the first unattended / autonomous session after PR #157 merges.
**Two parts:** (A) implement the context-slimming plan first, (B) then proceed to Phase 5 of v3 synthesis under the new lighter startup.

Copy from `START HERE` down into the new session prompt.

---

## START HERE

You are operating in autonomous (unattended) mode. The user has delegated execution for this run; do not wait for confirmations on reversible decisions.

This run has **two sequential phases**. Do NOT start Phase B until Phase A is complete and all of Phase A's PRs are merged.

---

# Phase A — Implement the context-slimming plan

## Read order (Phase A only — minimal)

In order, before any non-Read tool call:

1. [`AGENTS.md`](AGENTS.md) — binding conventions. Note the adversarial-review-MUST-be-real-subagents rule and the internal-document-references rule.
2. [`CONTEXT-SLIMMING-PLAN.md`](CONTEXT-SLIMMING-PLAN.md) — the spec for what you're about to build. Read end-to-end.
3. [`retrospective/2026-05-25-155.md`](retrospective/2026-05-25-155.md) §Part 1 (the Phase-4 phase-by-phase narrative) and §Part 3 (agents-file rules — currently proposed, not yet adopted). Skim only.

Do **NOT** read the v3 synthesis docs during Phase A. They are not needed until Phase B.

## What to build (4 stacked PRs)

Per [`CONTEXT-SLIMMING-PLAN.md` § Implementation order](CONTEXT-SLIMMING-PLAN.md#implementation-order):

### PR A1 — `AGENT-ENTRY.md` (root navigation + task-aware reading lists)

Author `AGENT-ENTRY.md` at the repo root. Strict discipline: **name what is contained in each sub-doc, do NOT restate content**. The "named topic vs restated content" test from the plan's [Part 1](CONTEXT-SLIMMING-PLAN.md#part-1--entry-document-proposal-1) is binding — apply it as a self-review pass before commit.

Sections required (per the plan):

1. Binding conventions — names AGENTS.md.
2. Current state — names the active SESSION-HANDOFF (`architectures/v3/SESSION-HANDOFF-2026-05-25-phase-4-close.md`).
3. Plan — names `ARCHITECTURE-V3-SYNTHESIS-PLAN.md` with the "read only your current phase's section" guidance.
4. Decisions (binding) — names `architectures/v3/phase-3.4-decisions-resolved.md` + `architectures/v3/candidate-registry.md`.
5. Substrate primitives — names `architectures/v3/primitives/index.md` with drill-on-demand guidance.
6. Decision briefs (historical) — names `architectures/v3/decisions/` directory; "read only if relevant".
7. Disciplines — NEW (not in the original plan but needed post-Phase-4): names `architectures/v3/disciplines/index.md` (canonical 21 disciplines after Wave 4.6 merge).
8. Reading lists by task — seed with at least the following tasks (drawn from Phase-5 entry posture per the Phase-4-close handoff):
   - "Phase 5 dispatch shape decision" (auto-005)
   - "Phase 5 ADR Wave 5.1 dispatch" (common-primitive ADRs ≥3 candidates)
   - "Phase 5 ADR Wave 5.2 dispatch" (discipline ADRs)
   - "Phase 5 ADR Wave 5.3 dispatch" (candidate-specific ADRs)
   - "Drain research/manual/" (research-pipeline skill)
   - "Adopt Phase-4 retrospective rules into AGENTS.md" (review the 7 proposed rules in PR #157)

After authoring, run `python scripts/check-internal-refs.py AGENT-ENTRY.md` (or grep equivalent if the checker doesn't exist for this file yet) to verify all relative links resolve.

Open PR. Subscribe to PR activity. Title: `Add AGENT-ENTRY.md root navigation doc per context-slimming plan`.

### PR A2 — TL;DR sections in 2 heaviest docs

Per [`CONTEXT-SLIMMING-PLAN.md` § Part 3](CONTEXT-SLIMMING-PLAN.md#part-3--tldr-first-discipline-for-heaviest-docs-proposal-4):

- `ARCHITECTURE-V3-SYNTHESIS-PLAN.md` — add `## TL;DR (≤200 words)` section at the top of the file (after the H1 title, before any other section). Seed it inline by reading the body and writing the summary yourself; do NOT dispatch a TL;DR-regeneration subagent at this stage (the autonomous-run skill's end-of-run protocol will own regeneration from PR A3 onward).
- `architectures/v3/candidate-registry.md` — same treatment.

The TL;DR must summarize **structure, not conclusions**. Example: "10 candidates across 3 mandates (greenfield, brownfield, unified-attempt). Phase 4 closed all carrying forward; Phase 5 ADR dispatch is ~54-62 ADRs in 3 waves." Not: "the scoping principle says carry every defensible candidate forward."

Stacked on PR A1. Open PR + subscribe.

### PR A3 — Autonomous-run skill update

Per [`CONTEXT-SLIMMING-PLAN.md` § What this plan changes](CONTEXT-SLIMMING-PLAN.md#what-this-plan-changes), update:

- `.claude/skills/autonomous-run/SKILL.md` — add an "End-of-run TL;DR regeneration" sub-step to the end-of-run protocol. The sub-step dispatches a subagent over each `## TL;DR (≤200 words)`-tagged doc (currently 2: the plan + registry), the subagent reads the body and writes a fresh TL;DR ≤200 words, the lead agent commits each regenerated section. Also add a "Update AGENT-ENTRY.md filename pointers" sub-step to the handoff discipline.
- `.claude/skills/autonomous-run/resources/template-handoff-doc.md` — add a "Task-aware reading lists" section template that future handoffs populate with the next likely tasks + per-task reading lists. Future AGENT-ENTRY.md updates pull from there.

Stacked on PR A2. Open PR + subscribe.

### PR A4 — Startup-prompt convention update

Per [`CONTEXT-SLIMMING-PLAN.md` § What this plan changes](CONTEXT-SLIMMING-PLAN.md#what-this-plan-changes) row 6:

Locate any documented "how to start a new session" guidance in the repo. Candidates: `AGENTS.md`, `.claude/skills/autonomous-run/SKILL.md` (already updated in A3), `README.md` if it discusses session startup, any "kickoff prompt" templates under `.claude/skills/*/resources/`. Update each so the new convention is: "the new agent should read `AGENTS.md`, then read `AGENT-ENTRY.md` and follow its navigation for the stated task" — replacing any prior "read these N files in order" lists.

If you don't find any startup-prompt templates outside what A3 already updated, this PR is empty — close it with a "no additional artifacts required" comment and proceed to Phase B.

Stacked on PR A3. Open PR + subscribe.

## Phase A completion criteria

- PRs A1, A2, A3, (A4 if non-empty) all merged into main.
- `AGENT-ENTRY.md` exists at repo root and passes internal-refs check.
- The plan + registry both carry a `## TL;DR (≤200 words)` section at the top.
- The autonomous-run skill carries the TL;DR-regeneration sub-step.
- A fresh agent given just `AGENTS.md` + `AGENT-ENTRY.md` + the active SESSION-HANDOFF can navigate to any Phase-5 dispatch task.

When all of the above are true, Phase A is closed. Begin Phase B.

---

# Phase B — Phase 5 of v3 architecture synthesis (ADR dispatch)

Phase 4 of v3 closed 2026-05-25. All 10 candidates carry forward. All 3 RG-primitive sub-tracks PASSED. 30 distinct substrate primitives. 21 architecture-level disciplines. Phase-5 ADR estimate: ~54-62 across 3 waves per the [v1.2 plan](ARCHITECTURE-V3-SYNTHESIS-PLAN.md#phase-5--adrs-per-candidate-with-cross-references-on-shared-primitives-revised-in-v12).

## Read order (Phase B)

Now that `AGENT-ENTRY.md` exists (Phase A delivered it), the read order is minimal:

1. [`AGENTS.md`](AGENTS.md)
2. [`AGENT-ENTRY.md`](AGENT-ENTRY.md) — follow its navigation.
3. The active SESSION-HANDOFF at `architectures/v3/SESSION-HANDOFF-2026-05-25-phase-4-close.md` — pickup point.
4. Pull the per-task reading list from `AGENT-ENTRY.md` § "Reading lists by task" → "Phase 5 dispatch shape decision".

Drill into individual primitive sketches, candidate substrate-requirements, disciplines, or sub-tracks only when a specific decision requires them.

## Initial tasks (in order)

### Task 1 — Write `auto-005`: Phase-5 dispatch shape

Per the [v1.2 plan § Phase 5](ARCHITECTURE-V3-SYNTHESIS-PLAN.md#phase-5--adrs-per-candidate-with-cross-references-on-shared-primitives-revised-in-v12), Phase 5 has 3 waves:

- **Wave 5.1 — Common-primitive ADRs** (~13 ADRs; primitives shared ≥3 candidates from `architectures/v3/primitives/overlap.md`)
- **Wave 5.2 — Discipline ADRs** (~8-12 ADRs from `architectures/v3/disciplines/index.md`; parallel with 5.1)
- **Wave 5.3 — Candidate-specific ADRs** (~30 orphan + ~13 per-variant; fires after 5.1 + 5.2 land)

Write `architectures/v3/decisions/auto-005-phase-5-dispatch-shape.md` in the `auto-NNN` lifecycle pattern (per the binding [SKILL-SPEC-34dd1d0274](retrospective/2026-05-25-155/SKILL-SPEC-34dd1d0274-decision-brief-adversarial-review-lifecycle.md) — read it if you want the template; the relevant retrospective rules are AGENTS-MD-8a7029647f (3-tier verdicts), AGENTS-MD-bb7fe2c5aa (Round-1 strikethrough preservation), AGENTS-MD-ffe35aa500 (honest-acknowledgements)).

Suggested defaults for the brief to consider (reviewers should pressure-test these):
- Wave-size limit per parallel fanout (≤15 ADRs per wave to keep aggregation tractable). Wave 5.1 + 5.2 may need a split.
- Per-ADR brief shape: alternative-considered text-pull discipline; relative-link discipline; per-candidate cross-reference discipline.
- Exemplar ADR authored by lead agent before the parallel fanout (per AGENTS-MD-eec503a3c2).

Dispatch ≥2 real adversarial subagent reviewers per the AGENTS.md rule. Suggested angles:
- ADR-pipeline architect (challenges wave sequencing + exemplar shape)
- ADR-quality auditor (challenges the alternatives-considered discipline + cross-reference discipline)

Land as a stacked PR. Open + subscribe.

### Task 2 — Dispatch Wave 5.1 (common-primitive ADRs)

Per the verdict of `auto-005` Round 2. Inputs:
- `architectures/v3/primitives/overlap.md` § "primitives shared ≥3 candidates" → ~13 primitives.
- Per-primitive sketches under `architectures/v3/primitives/P-NN-*.md` (drill on demand).
- Per-candidate substrate-requirements summaries under `architectures/v3/substrate-requirements/<candidate-id>.md` (for §3 candidate-specific contracts on each common primitive).
- The `adr` skill ([`.claude/skills/adr/SKILL.md`](.claude/skills/adr/SKILL.md)) — outputs land at `docs/adr/NNNN-<kebab>.md`.

Per [SKILL-SPEC-069f0f31bf](retrospective/2026-05-25-155/SKILL-SPEC-069f0f31bf-parallel-fanout-with-exemplar-and-rubric.md) parallel-fanout-with-exemplar-and-rubric:
- Author 1 exemplar ADR inline (pick a commodity primitive like P-01 sandbox — least contested).
- Dispatch the remaining ~12 ADRs as parallel subagents with the exemplar as required input + a self-check rubric (section presence, word count ≤1000, alternatives ≥2, references ≥3, all links relative — verified via tool calls per AGENTS-MD-e74e4811a2).

Stacked PR. Open + subscribe.

### Task 3 — Dispatch Wave 5.2 (discipline ADRs, parallel with 5.1)

Inputs:
- `architectures/v3/disciplines/index.md` § 21 disciplines (or whatever the canonical merged index resolved to in Wave 4.6).
- The `adr` skill.

Dispatch shape: 1 exemplar discipline ADR inline + ~8-12 parallel subagents. Same self-check discipline as Wave 5.1.

Stacked PR. Can fire concurrent with Task 2.

### Task 4 — Wave 5.3 dispatch (after 5.1 + 5.2 land)

Largest wave: ~30 orphan ADRs + ~13 per-variant ADRs across the 10 candidates. Per the plan, this fires AFTER Waves 5.1 + 5.2 so common-ADR + discipline-ADR cross-references are stable.

Sub-shape: per-candidate parallel fanout (10 subagents, each ADR'ing their candidate's unique primitives + methodology bindings). Each subagent's ADRs cross-reference the common + discipline ADRs by relative link to `docs/adr/`.

This is the largest fanout of the run. Apply all retrospective rules:
- Exemplar (lead-agent authored for the most-contested candidate's first ADR — likely BF-L given its load-bearing P-26).
- Self-check rubric with tool-call verification.
- Required text-pull when citing the Phase-3.5.5 application table or any other binding rule table.
- 3-tier verdicts in the per-fanout adversarial review.

Stacked PR. Open + subscribe.

### Task 5 — Phase 5 close + handoff

After all ADR waves merge:
- Write `architectures/v3/SESSION-HANDOFF-<UTC-DATE>-phase-5-close.md`.
- Mark the Phase-4-close handoff superseded.
- Update `AGENT-ENTRY.md` § Current state pointer.
- Update `AGENT-ENTRY.md` § Reading lists by task with the next-likely Phase-6 tasks (architecture spec authorship per candidate).
- Run end-of-run TL;DR regeneration on the plan + registry per the autonomous-run skill (which was updated in Phase A PR A3).

## Working mode reminders

- PRs default to ready-for-review, NOT draft (AGENTS.md binding).
- Adversarial reviews MUST be real subagent dispatches (AGENTS-MD-d72e1a4f3c, currently codified).
- 3-tier reviewer verdicts (AGENTS-MD-8a7029647f, proposed in #157 — adopt as your discipline regardless of whether it's been merged into AGENTS.md yet).
- Stacked-PR base selection (AGENTS-MD-de48bd24b4) — fetch `origin/main` before branching.
- Self-check rubric tool-verification (AGENTS-MD-e74e4811a2) — `wc -w`, `ls`, `grep`.
- Honest acknowledgements section in Round 2 if any wave fired pre-Round-2 (AGENTS-MD-ffe35aa500).
- Round-1 strikethrough preservation (AGENTS-MD-bb7fe2c5aa).
- Verbatim text-pull when citing binding rule tables (AGENTS-MD-bf4431be57).
- Exemplar before parallel fanout (AGENTS-MD-eec503a3c2).
- Commit-and-push-every-checkpoint (always-commit-skill-to-repo).
- Track long-running fanouts in-flight (in-flight-workflow-tracking).

The user would rather you get a lot done with reversible decisions than do nothing waiting for input. Prefer action, document the reasoning, and make every decision rewindable.

## What "Phase 5 closed" looks like

- ~54-62 ADRs landed under `docs/adr/NNNN-<kebab>.md` across the 3 waves.
- Each candidate's ADR set (common + discipline + candidate-specific) composes into a coherent architecture per the candidate-coherence auditor pattern in the v1.2 plan.
- `architectures/v3/SESSION-HANDOFF-<date>-phase-5-close.md` exists.
- `AGENT-ENTRY.md` reading-list section updated for Phase 6.
- All work committed, pushed, PR'd, and merged. No drafts; no unmerged work at session close.
