# agent instruction

**Stacked-PR base selection.** Before creating a new stacked PR, fetch `origin/main` and inspect `git log --oneline origin/main -5`. If every PR in the previous chain has been merged, branch the new work off `origin/main` directly; if the chain is partially open, branch off the tip of the unmerged chain. Do NOT blindly branch off a previous session's "tip" branch name without first checking its merge state.

*Grounded in: Phase-4 dispatch session 2026-05-25 — the prior chain (PRs #136-#145) had all merged to main before the session started; the dispatch instructions named `claude/handoff-phase-3.5-close` as the "tip" but it was already in main.*

# justification

Sessions that "continue a chain" inherit a named tip branch from the prior session's handoff doc. If the chain merges between sessions, the named tip equals the most recent merge into main — and `git checkout -b new-work named-tip` produces a branch whose PR diff against main shows the merge state, not the new work. The fix is a 2-tool-call pre-flight (`git fetch origin main && git log --oneline origin/main -5`) that takes ~3 seconds and decides the correct base. Without it, the first stacked PR either has an empty diff (if you branch off the merged tip) or includes already-merged commits (if you push without checking). Both failure modes burn 10+ minutes to recover and confuse PR reviewers. The marginal cost of the pre-flight is two commands at session start.
