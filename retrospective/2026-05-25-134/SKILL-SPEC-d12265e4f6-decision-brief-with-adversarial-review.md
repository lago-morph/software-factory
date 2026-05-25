# Spec: `decision-brief-with-adversarial-review`

- **ID**: SKILL-SPEC-d12265e4f6
- **Source retrospective**: ../2026-05-25-134.md

## Intent

In unattended sessions (overnight runs, scheduled jobs, webhook-triggered work), the agent will encounter questions it would normally ask the user. Stopping to wait wastes the window; proceeding silently makes the morning review unreviewable. This skill defines the protocol: when stuck, write a **decision brief** (question, alternatives, choice, reasoning, rewind point), dispatch 2-3 **adversarial-reviewer subagents** to attack the brief from independent angles, incorporate the strongest objections, commit the brief on its own **stacked branch**, and proceed as if the user authorized the chosen option. Every decision becomes reversible by reverting the stacked branch; every decision has an audit trail. Grounded in the user's session-end instruction in PR #134: "I'd rather you get a lot of work done overnight than do nothing."

## Trigger

**Direct triggers (skill activates explicitly):**
- The session is unattended AND the agent identifies an ambiguity it would normally surface to the user.
- The user invokes `/decision-brief <topic>` or types phrases like "decide this and document it", "make the call with a brief", "adversarial-review this and proceed".

**Proactive triggers (offer this protocol):**
- An overnight or unattended-mode prompt explicitly authorizes autonomous decisions (e.g., the prompt produced at the end of PR #134).
- The agent finds itself blocked waiting for input in a context where the prompt said "keep going".

**Negative triggers (do NOT use this skill):**
- Interactive sessions where the user is reachable. Use `AskUserQuestion` instead.
- Trivial choices that don't affect more than one file (the brief overhead exceeds the decision's reversibility risk).
- Tactical implementation choices (variable naming, helper-function placement) — those go through normal coding judgment, not a formal brief.

## Inputs

- The ambiguity itself: a one-sentence statement of what the agent would have asked the user.
- The work context: which feature branch the agent is on, what PR (if any), what was being done when the ambiguity arose.
- Project conventions: read [`AGENTS.md`](../../AGENTS.md) for ambient rules; check for relevant ADRs in [`docs/adr/`](../../docs/adr/).
- The relevant project documents the decision will affect.

## Outputs

- A decision brief at `<project-area>/decisions/auto-NNN-<slug>.md` (path varies by project area — e.g., `architectures/v3/decisions/` for v3 work).
- A new stacked branch off the previous feature branch with the brief as a standalone commit, then the implementation as subsequent commit(s).
- A stacked PR with `base` set to the previous feature branch (not `main`).
- An entry in the morning-summary doc at the repo root (`overnight-summary.md`) — one bullet per brief, with rewind-point and one-line "if you disagree, revert to this commit".
- The agent then proceeds with downstream work as if the user authorized the choice.

## Workflow

1. **Confirm unattended mode.** Check that this is an unattended session (the prompt should have stated it; see ADR-f702da3352). If interactive, use `AskUserQuestion` and stop.
2. **Identify the next decision-brief sequence number.** `NNN = $(ls <area>/decisions/auto-*.md 2>/dev/null | wc -l) + 1`, zero-padded to three digits.
3. **Author the decision brief** from `resources/template-decision-brief.md` (see "Files this skill creates / modifies" — template lives with this skill). Required sections:
   - **Question** — one sentence, what the user would have been asked.
   - **Alternatives considered** — 3+ when plausible, 2 only if one is genuinely strictly dominant.
   - **Chosen option** — one of the alternatives, with one-sentence justification.
   - **Reasoning** — paragraph or two, evidence-driven.
   - **If-user-overrides rewind point** — the commit hash + branch name to revert to.
4. **Commit the brief on its own stacked branch.** Branch off the previous feature branch (not `main`); name it `<parent-branch>-auto-NNN`. Commit the brief alone.
5. **Dispatch 2-3 adversarial-reviewer subagents in parallel.** Each gets:
   - The brief (as a file path).
   - A specific attack angle: e.g., "scoping-principle skeptic", "buildability-rule enforcer", "cost-hawk", "ADR-conflict checker", "downstream-rework cost reviewer". Pick attack angles that are independent of each other (don't all collapse to "is this expensive?").
   - Instruction: read the brief cold, find the strongest objection, return a one-paragraph objection + a concrete counter-proposal.
6. **Incorporate or reject each objection.** For each returned objection: either revise the brief (recompute the decision and amend the commit) or add a "rejected objections" section explaining why. Record the round in the brief itself.
7. **Push the stacked branch and open a stacked PR.** `base` is the previous feature branch. PR ready-for-review (per [`AGENTS.md`](../../AGENTS.md)).
8. **Append to `overnight-summary.md` at the repo root.** Format: `- auto-NNN: <one-line question> → <chosen option>. Brief: <path>. Rewind: revert <parent-branch-commit>.`
9. **Proceed with downstream work as if authorized.** Implementation commits land on the same auto-NNN stacked branch.

## Concrete examples

### Example 1: Phase 3.5 dispatch shape (per-cluster vs. per-primitive subagents)

Context: overnight run, agent reached Phase 3.5 buildability dispatch (per the morning's stacked-PR plan), needs to decide between per-cluster and per-primitive subagent dispatch.

Brief at `architectures/v3/decisions/auto-001-phase35-dispatch-shape.md`:

- **Question.** Should Phase 3.5 buildability sketches be dispatched per-cluster (group related primitives into ~6 clusters, one subagent each) or per-primitive (~25-30 subagents, one per primitive)?
- **Alternatives.** (a) per-cluster, (b) per-primitive, (c) hybrid (per-cluster for tactical commodity primitives, per-primitive for designed-system primitives like Codebase Model).
- **Chosen.** (c) hybrid — per-primitive for the four "designed-system" primitives flagged in the registry's per-candidate buildability scope (Codebase Model, multi-component distance estimator, FC store + opposing-side router, Intent Crucible validator); per-cluster for the rest.
- **Reasoning.** Designed-system primitives are where the buildability sketch carries the most risk and the most signal; they merit dedicated subagents. Commodity primitives (sandbox, cost ceilings, watchdog) are well-understood and clustering them is cheap.
- **Rewind.** Revert commit `<hash>` on branch `claude/keen-albattani-J2C7W-auto-001`.

Reviewers dispatched: cost-hawk (objection: 25 primitives is too many subagents — partial accept, used the hybrid to cut total count to ~10); scoping-principle skeptic (objection: clustering hides primitives that turn out to be load-bearing — rejected, with rationale: the registry's per-candidate breakdown already surfaces load-bearing primitives explicitly); ADR-conflict checker (no conflicts found).

### Example 2: Stale phrasing rewrite scope

Context: while implementing the Phase 3.5 plan revision, the agent discovers that Phase 1 and Phase 2 outputs contain multiple temporal-continuity phrasings ("greenfield codebases will eventually need...") that are stale after ADR-276d5a13e4's entry-mode reframe.

Brief at `architectures/v3/decisions/auto-007-stale-phrasing-rewrite.md`:

- **Question.** Rewrite all stale temporal-continuity phrasings in Phase 1-3 outputs now, or defer to a Phase 4 cleanup pass?
- **Alternatives.** (a) rewrite now (cost: ~2 hours, ~12 files), (b) defer to Phase 4, (c) rewrite the load-bearing ones now and leave a tracking note for the rest.
- **Chosen.** (c) — rewrite three load-bearing files (`draft-greenfield-synthesis.md`, `candidate-registry.md`, `00-brief-v3.md`); add tracking note in `phase-3.4-decisions-resolved.md` for the rest.
- **Reasoning.** Load-bearing files are read frequently; stale phrasings there cause cascading misreads. Lower-traffic Phase 1-2 files can wait without harm.
- **Rewind.** Revert range `<hash1>..<hash2>` on branch `<parent>-auto-007`.

Reviewers: completeness reviewer (objection: any stale phrasing left in could re-trigger the original misread — partial accept, added a grep'd appendix to the brief listing every file with stale phrasing); cost-hawk (no objection).

## Anti-patterns

- **Using this skill in an interactive session.** The user is reachable — ask them. The brief overhead exists because the user isn't there; if they are, it's pure friction.
- **Using a single reviewer.** Adversarial review depends on attack-angle independence; one reviewer often shares the deciding agent's framing. The user explicitly said "adversarial reviewers" plural.
- **Skipping the rewind point.** Without "revert this commit on this branch", the morning rewind path requires reconstruction. The rewind point is non-negotiable.
- **Letting the brief and the implementation share a commit.** The brief must be its own commit so the rewind unit is "the decision" not "the decision + half a day of work that depended on it".
- **Filing the brief without a stacked PR.** A brief that only lives in a commit doesn't surface in the morning review queue. The stacked PR is the review surface.
- **Authoring briefs for tactical micro-choices.** Variable names, helper-function placement, etc. don't need a brief. Reserve this protocol for choices that affect multiple files or that the user would actually want to override.

## Acceptance criteria

- [ ] Every brief is its own commit on its own stacked branch.
- [ ] Every brief has a `## Rewind point` section naming a specific revertable commit.
- [ ] Every brief lists ≥2 reviewer attack angles + their objections + accept/reject disposition.
- [ ] Every overnight session that produced briefs has an `overnight-summary.md` at the repo root listing them.
- [ ] No brief is authored in an interactive session.

## Files this skill creates / modifies

- `<area>/decisions/auto-NNN-<slug>.md` — the brief itself.
- `overnight-summary.md` (repo root) — the morning-review index; appended per brief.
- Stacked branches named `<parent-branch>-auto-NNN`.
- `.claude/skills/decision-brief-with-adversarial-review/resources/template-decision-brief.md` — the brief template (canonical structure: Question / Alternatives / Chosen / Reasoning / Reviewers / Rewind point).