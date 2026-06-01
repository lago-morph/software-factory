# agent instruction

**Locate the paradigm-shift commit before reconciling a half-applied restructure.** When asked to finish, reconcile, or fix a document whose organizing principle changed partway through its history (a newer style bolted on top of an older one), first run `git log -- <file>` and `git show` on the candidate commits to pinpoint where the paradigm shifted and what the old vs new organizing principle is, before editing. Do not start from a guess about where the inconsistency lives.

*Grounded in: locating the phases-to-products shift in implementation-dependencies.md via git archaeology before restructuring.*

# justification

The user's own instruction was "if you look at diffs on the edits to the file you will find where the paradigm shifted." Acting on that literally — `git log --oneline -- <file>` then `git show` on the two most recent commits — turned a vague "the doc mixes two styles" complaint into a precise map: the original commit organized by phase, two later commits introduced product-clustering on top without removing the phase skeleton. That map made the whole restructure tractable; every subsequent edit knew exactly which structure was the keeper and which was residue. The marginal cost is two or three git commands at the start of the task. The cost of skipping it is editing from a guess: you discover the second, deeper structural layer only after you have already reworked the first, and you redo the work. For any "reconcile / finish / fix the inconsistency" task on a versioned document, the diff is the cheapest possible source of ground truth about what changed and why.
