# agent instruction

**Reposition a merged session branch before the next deliverable.** After a mid-session PR merges, do not stack new commits on the pre-merge branch tip. Fast-forward the designated session branch onto current `main` first — `git stash push -u`, `git fetch origin main`, `git merge --ff-only origin/main`, `git stash pop` — then commit the next deliverable and open a fresh PR. Verify the prior work is actually in `main` (`git log --oneline origin/main`) before relying on it.

*Grounded in: three sequential deliverables (board, backbone plan, handoff) each needed the branch fast-forwarded onto the freshly-merged main before the next commit.*

# justification

This session shipped three deliverables in series, and each time the prior PR merged and its branch was deleted, leaving the local branch pointing at a now-merged commit. Committing the next deliverable on that stale tip would have produced a PR whose diff re-included already-merged files (or a confusing merge base). The stash/ff/pop sequence keeps the branch a clean single-commit delta on top of live `main`. It is four git commands at each boundary versus a tangled, hard-to-review PR — cheap insurance that complements the existing fresh-PR-after-merge rule with the concrete mechanic.
