# agent instruction

**Open a fresh PR for artifacts created after a mid-session merge.** "When a PR is merged mid-session its branch is deleted; pushing again recreates the branch but the new commits are not in main. Any artifact written after the merge (e.g. a handoff file) needs its own new PR to land in main."

*Grounded in: HANDOFF.md written after PR #213 merged, requiring follow-up PR #214.*

# justification

After PR #213 merged, the feature branch was deleted on the remote. The handoff file written afterward was committed and pushed — which silently *re-created* the branch — but that commit was not in `main`, only on the resurrected branch. Without noticing this, the agent could have reported "everything is preserved" while the most important resume artifact sat outside `main`. The rule makes the post-merge state explicit: a merge is a boundary, and anything authored after it needs a new PR to actually reach `main`. The cost is one extra PR; the cost of missing it is a handoff or fix that the user believes is merged but is not, discovered only when the branch is later force-deleted or diverges.
