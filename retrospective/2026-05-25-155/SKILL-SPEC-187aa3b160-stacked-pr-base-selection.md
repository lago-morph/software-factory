# Spec: `stacked-pr-base-selection`

- **ID**: SKILL-SPEC-187aa3b160
- **Source retrospective**: ../2026-05-25-155.md

## Intent

Before creating a stacked PR off a previously-stacked chain, fetch `origin/main` and inspect recent merges; if every PR in the previous chain has merged, branch the new work off `origin/main` directly; if the chain is partially open, branch off the tip of the unmerged chain. Avoid blindly branching off a previous session's "tip" branch name without first checking its merge state. Drawn from the Phase-4 dispatch session start where the prior chain PR #136 through PR #145 had all merged before the session started, and the dispatch instructions' named "tip" branch `claude/handoff-phase-3.5-close` was already in main. Branching blindly off the named tip would have created an empty diff against the parent + a confusing chain state.

## Trigger

- A new session opens that the handoff brief tells to "continue the chain off [tip-branch]".
- Lead agent is about to create a new branch + PR that depends on prior work.
- Proactive: any time the [`stacked-pr-on-feature-branch`](../../../.claude/skills/stacked-pr-on-feature-branch/SKILL.md) skill loads, run this check first.

Negative triggers: single-PR sessions with no parent dependency; the very first PR in a chain.

## Inputs

- The named "tip" branch from the handoff or user prompt.
- `git fetch origin main` (network call).
- `git log --oneline origin/main -N` (local, post-fetch).

## Outputs

- A decision: branch off `origin/main` (chain merged) or branch off the tip-branch (chain partially open).
- The new branch created from the correct base.

## Workflow

1. Run `git fetch origin main` to refresh the remote tracking.
2. Run `git log --oneline origin/main -10` and inspect the merge subjects. Look for "Merge pull request #N from <tip-branch>" or its parents.
3. If the named tip-branch (or any branch in its chain) appears in the merge log, the chain has merged.
4. If merged: `git checkout -b claude/<new-work-slug> origin/main`.
5. If partially merged: identify the highest-numbered PR in the chain still open; branch off that branch's tip with `git checkout -b claude/<new-work-slug> claude/<tip-of-open-chain>`.
6. Verify: `git log --oneline -5` on the new branch should show the expected parent commit.
7. Begin work.

## Concrete examples

### Example 1: Phase-4 dispatch session start (this session, 2026-05-25)

- Handoff named tip: `claude/handoff-phase-3.5-close`.
- Ran `git fetch origin main && git log --oneline origin/main -5`. Output: most recent merge was `d245de2 Merge pull request #145 from lago-morph/claude/handoff-phase-3.5-close`.
- Inference: the named tip branch IS the most-recently-merged PR. Chain is fully in main.
- Action: `git checkout -b claude/auto-003-bfl-rg-view-choice origin/main`. Subsequent stacked PRs branched off the previous PR's branch (auto-004 off auto-003, etc.).

### Example 2: Mid-chain partial merge (hypothetical)

- Handoff named tip: `claude/wave-4.6-phase-4-close`.
- `git log --oneline origin/main -5` shows PRs #150 and #154 merged but #155 (the named tip) still open.
- Action: `git checkout -b claude/wave-5.1-adr-fanout claude/wave-4.6-phase-4-close` (off the unmerged tip).
- Chain continues stacked until #155 merges; then subsequent work branches off main.

## Anti-patterns

- **Blindly branching off the named tip.** If the chain has merged, the named tip equals `origin/main`'s parent — but `git checkout -b new-work tip-branch` creates a branch with a stale local-only reference. PR diff against main would be the merge state, not the new work.
- **Branching off `origin/main` when the chain is partially open.** Loses the parent dependency; new PR's diff would re-include the unmerged parent's changes, producing review confusion.
- **Skipping `git fetch` before checking merge state.** Local view of main may be stale; the named tip may have just merged and the local repo doesn't know yet.
- **Manually counting commits to figure out merge state.** Use the merge-log subject pattern — GitHub generates `Merge pull request #N from <branch>` deterministically.

## Acceptance criteria

- [ ] `git fetch origin main` was run before branching.
- [ ] Merge-log inspection produced an explicit decision on chain state.
- [ ] New branch parent matches the decision (origin/main if merged; tip-of-open-chain otherwise).
- [ ] `git log --oneline -3` on the new branch shows the expected parent commit.

## Files this skill creates / modifies

- No files created. Modifies: the current `HEAD` (via `git checkout -b`).
