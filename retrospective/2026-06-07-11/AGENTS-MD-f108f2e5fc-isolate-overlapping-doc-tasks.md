# agent instruction

**Isolate overlapping doc-edit tasks with selective staging.** When two tasks edit the same lines (for example a bug-fix and a later restructure of the same section), ship them as separate sequential PRs: complete and merge the smaller fix first, then `git stash` or selectively `git add` the second task's changes so each PR diff is reviewable in isolation. Do not let the second task's changes contaminate the first commit, and rebase the second onto the merged main before opening its PR.

*Grounded in: Task #1 (nudge quoting) and Task #2 (autonomous-flow rewrite) both edited the same README and GETTING-STARTED nudge lines; stashing Task #2 kept PR #9 a clean two-file diff.*

# justification

This session had two deliverables that touched the *same lines*: Task #1 fixed the `gc session nudge` invocation, and Task #2 then rewrote those very sections into the autonomous flow. Worked naively in one branch, the two would have collapsed into one indistinguishable diff — the small, independently-verifiable doc fix buried inside a large feature change. Stashing Task #2's code (`git stash push -u entrypoint.sh pack/orders/`) kept PR #9 a clean two-file diff that merged on its own merit; after the merge, `reset --hard origin/main` + `stash pop` rebased Task #2 onto the new main so PR #10 showed only its own changes. The marginal cost is a couple of stash/reset commands; the payoff is two reviewable PRs instead of one muddy one, and the ability to land the verified fix even if the feature had hit a snag.
