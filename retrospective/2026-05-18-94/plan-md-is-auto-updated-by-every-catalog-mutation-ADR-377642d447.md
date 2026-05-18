# ADR: PLAN.md is auto-updated by every catalog mutation

- **ID**: ADR-377642d447
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-18
- **Source retrospective**: ../2026-05-18-94.md
- **PRs covered**: #94

## Context

`research/PLAN.md` is the human-readable narrative for the research catalog: a `**Version:**` line at the top, a §1 "Current state" with a chronological list of `**Session YYYY-MM-DD — ...**` bullets, and a §10 "Round-by-round canonical reports (lookup table)" with one row per drain round. It's intended to give a fresh reader a quick "what's happened recently" answer without having to read commit history.

Over PRs #80 through #93, PLAN.md had drifted from the catalog. `check-plan-consistency.py` (added in this session) reported 9 of the last 10 catalog-touching commits on main did not also touch PLAN.md. The narrative was stale; the only authoritative record of "what was added when" lived in `git log`.

Two failure modes contributed:

1. **Implicit responsibility.** PLAN.md was treated as "the agent should remember to update this" — soft policy, not enforced. Agents (and humans) forget.
2. **No automation.** Every PR's PLAN.md update was hand-written from scratch, even though 80% of the content was mechanical (date, round number, file counts, touched IDs).

The user explicitly asked for a discipline mechanism. The options offered (via `AskUserQuestion`): SKILL.md rule + audit; drain.py auto-emit + audit; PR template; just the audit. The user picked drain.py auto-emit + audit.

## Decision

**`research/PLAN.md` is an emitted artifact, not a hand-maintained log, for the catalog-narrative portion.**

Specifically:

1. `drain.py` Stage 4c (a new pipeline stage executed after stage 4b audit, before printing the run summary) calls `update_plan_after_drain(result, plan_path)` which:
   - Reads `research/PLAN.md` (path configurable via `plan_path` in `pipeline-config.yaml`, default `research/PLAN.md`).
   - Computes the next round number from the §10 lookup table's highest existing row.
   - Inserts a placeholder `- **Session YYYY-MM-DD — Round-N drain (auto-recorded by drain.py)** — ...` bullet under §1, after the last existing Session bullet.
   - Appends a placeholder row to §10's table.
   - Bumps the `**Version:** vX.Y` line (minor + 1; sets date to today).
   - Writes back atomically.
2. The placeholder text explicitly says it's auto-generated and asks the agent to replace it with a real description before committing. The agent's commit therefore contains BOTH the catalog change AND a real (hand-edited) Session bullet — no PLAN.md-less commits, no auto-emitted-but-unedited bullets reaching main.
3. Opt-out via `drain.py --no-plan-update` (for the rare case where the agent intends to write the entry by hand in the same commit and doesn't want the placeholder).
4. Opt-out for empty drains: if the drain produced no material catalog changes (no new records, no attachments, no orphans reconciled, no transcripts delivered, no wants purged), Stage 4c is skipped — no Session bullet for a no-op run.
5. SKILL.md gains Hard rule #10: "Every catalog mutation gets reflected in `research/PLAN.md` in the same commit." Drain runs satisfy this automatically; manual mutations (rare) must do it by hand.
6. `scripts/check-plan-consistency.py` runs as advisory in `lint-sources.sh` (warnings don't fail the lint, so a missed PLAN.md edit doesn't block unrelated catalog work) and has a `--strict` flag for CI gates.

## Alternatives considered

1. **SKILL.md rule + audit, no automation.** Rejected by the user: "we've had policies before; they aren't enforced. I want the mechanism." Soft policies depend on agents remembering; the audit catches the lapse after the fact. Better to make the right thing the default.

2. **PR template that prompts for the PLAN.md update.** Rejected: works for human contributors but agents don't see the template. Also doesn't help when the PLAN.md edit is part of an automated workflow (the auto-regen bot, a CI job).

3. **Make PLAN.md fully auto-generated from the catalog.** Rejected: the Session bullet's prose value comes from the agent's narrative (what was the round about, what surprises came up, why this particular set of sources). A fully-generated bullet would be sterile and provide no signal beyond what `git log` already gives. The hybrid — auto-skeleton + hand-edited prose — is the sweet spot.

4. **Audit-only (advisory warning in lint, no auto-emit).** Rejected: this leaves the agent on the hook to remember to write the bullet from scratch every drain. Auto-emit produces the skeleton (date, round number, counts) for free; the agent only has to write the prose.

5. **Auto-emit but fully hands-off (no agent editing required).** Rejected: would create the "sterile bullet" failure of option 3. The placeholder explicitly demands a rewrite, so the agent is forced to engage with the narrative — a feature, not a bug.

## Consequences

**Easier:**
- The PLAN.md edit is now nearly free for the agent: most of the bullet is already there; only the prose body needs writing. Agents are far more likely to actually update PLAN.md when most of it is pre-filled.
- A fresh session starting at the head of a recent PR can read PLAN.md and get a real narrative; `git log` becomes the secondary record, not the primary one.
- `check-plan-consistency.py --strict` can be added to CI for new PRs, providing a hard gate.
- Drain semantics now match the "every catalog mutation has a narrative" mental model: the drain output stream and PLAN.md update are the same workflow.

**Harder / trade-offs accepted:**
- Drain runs now mutate two files (`sources.json` AND `PLAN.md`) instead of one. Commits become "fatter" by a few PLAN.md lines. This is the desired outcome.
- The auto-emitted placeholder text MUST be rewritten before commit, but the agent is on the honor system for that. A future strict-mode addition could parse PLAN.md and reject commits with un-edited placeholder text; not in scope for this PR.
- `--no-plan-update` exists as an opt-out but should only be used when the agent will hand-write the entry in the same commit. The flag could be misused to silently skip the discipline. Mitigation: `check-plan-consistency.py --strict` in CI catches commits that touch the catalog but not PLAN.md, regardless of whether `--no-plan-update` was used.
- The Round-N numbering is global across the catalog. If two parallel drains land in different PRs, they'll race for the same round number — the second to merge will need to manually re-number. Acceptable: parallel drains are rare, and the §10 lookup table makes the conflict obvious.
- Manual catalog mutations (hand-jq edits, `pointer_to` migrations) bypass drain.py entirely and therefore bypass Stage 4c. The agent has to remember to update PLAN.md for these — exactly the case where Hard rule #10 + the audit are needed.

## References

- [`../2026-05-18-94.md`](../2026-05-18-94.md) — Phase 3 (user scope) and Phase 4 (implementation).
- `.claude/skills/research-pipeline/scripts/drain.py` — Stage 4c orchestration (~line 990); `_run_tidy_wants` exemplifies a manual mutation that does NOT trigger Stage 4c (sweep modes are out of scope for round numbering).
- `.claude/skills/research-pipeline/scripts/update_plan.py` — the `update_plan_after_drain` implementation.
- `.claude/skills/research-pipeline/scripts/check-plan-consistency.py` — the audit (5 checks).
- `.claude/skills/research-pipeline/resources/_plan/update-discipline.md` — agent-facing templates for the Session bullet, Version bump, and §10 row.
- `.claude/skills/research-pipeline/resources/_plan/audit.md` — how to run and interpret the consistency check.
- `.claude/skills/research-pipeline/SKILL.md` — Hard rule #10.
- PRs: #94 — the implementation PR.
