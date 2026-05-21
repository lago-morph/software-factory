# agent instruction

**Commit iterative plan docs as WIP backup.** When iterating on a multi-version planning conversation (any plan that the user reviews and revises across several rounds), commit the in-progress plan to a temp file on a feature branch after each significant revision. Push and open a draft or ready-for-review PR. This is durable against context truncation and session crashes; the planning conversation's state survives.

*Grounded in: user feedback on cleanup-plan v1 — "Write the whole thing to some temporary file and commit just in case." Pattern recurred across six plan versions in this session.*

# justification

This session went through six successive plan revisions (v1 → v6) with user feedback at each step. None of them were the final execution; all of them were planning artifacts. Committing each version as `cleanup-plan-revised.md` on a feature branch meant:

1. The planning conversation's state was durable across any context truncation. If the session had been compacted mid-iteration, the latest plan version was already on disk, on a branch, ready for resumption.
2. The user could review the whole plan in the PR UI rather than scrolling through chat. By v5 the plan was 250+ lines — past the point of comfortable in-chat review.
3. The version history was preserved by git, so "what changed between v3 and v4?" was a `git diff` away.

The user's explicit ask — "Write the whole thing to some temporary file and commit just in case" — generalises beyond this session. Any multi-version planning conversation gets the same protection. The marginal cost is one commit per revision; the cost of skipping it is potentially losing the whole conversation if the session dies mid-iteration.
