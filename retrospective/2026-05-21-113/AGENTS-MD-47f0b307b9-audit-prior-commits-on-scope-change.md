# agent instruction

**Audit prior commits when the user introduces a mid-PR scope constraint.** When a reviewer adds a new constraint partway through a PR ("don't touch X", "keep everything in directory Y", "don't change AGENTS"), do not just comply going forward — walk every commit already on the branch, identify any change that now violates the new constraint, and revert it in a follow-up commit. The reviewer's constraint applies to the whole PR, not just future commits.

*Grounded in: PR #113 — user mid-PR direction to keep all gate machinery inside the skill directory required reverting `AGENTS.md` and `architectures/failure-modes.md` edits from earlier commits `22ee8d4` and `80962b3`.*

# justification

When user feedback arrives at commit five of a PR, the natural inclination is "OK, future commits will respect this." But the user is judging the PR as a whole — they will see the existing edits to `AGENTS.md` and the schema section in `architectures/failure-modes.md` when they next review the diff. Leaving them in produces a PR that visibly contradicts the user's constraint, forcing a second review round. The cost of compliance is one `git checkout <pre-violation-sha> -- <file>` per violated file (in PR #113: three files, four lines of shell). The cost of non-compliance is at minimum one wasted review round, at maximum a merge that lands the violations into main. The asymmetry is large enough that "audit then comply" should be the default response to mid-PR scope constraints.
