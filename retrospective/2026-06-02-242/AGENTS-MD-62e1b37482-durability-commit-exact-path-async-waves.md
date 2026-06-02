# agent instruction

**Durability-commit by exact path on the stop-hook nag during async subagent waves.** "In an ephemeral sandbox with async subagents whose files land before their completion receipts, commit completed files by their exact paths on each stop-hook reminder rather than waiting for the whole wave — and never blanket-`git add` while sibling subagents are mid-write on a *different* branch's files. Intermediate states are corrected by a later commit; lost work is not recoverable."

*Grounded in: the Sweep-2 run committed ~25 waves this way, across two concurrently-pipelined product branches, with no lost work and no cross-branch file mixing.*

# justification

Async subagents write their files and then return a completion receipt some time later; the sandbox's stop hook fires whenever the working tree is dirty. Waiting for an entire wave before committing risks losing finished work if the sandbox is reclaimed mid-wait; blanket-committing risks two distinct harms — capturing a sibling subagent's half-written file, and mixing one product's files onto another product's branch when products are pipelined on one working tree. Committing the completed files by exact path on each nag resolves both at once: durability without contamination. This discipline carried 44 commits across 7 stacked branches with no lost work and no branch cross-contamination.
