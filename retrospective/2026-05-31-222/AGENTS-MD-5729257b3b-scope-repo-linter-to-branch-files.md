# agent instruction

**Scope a repo-wide linter to branch-touched files before calling it red.** When a whole-repo checker reports thousands of issues, compare its result against the same checker run on the base branch (or filter its output to `git diff --name-only origin/main..HEAD`) before treating the failure as something this branch introduced.

*Grounded in: `scripts/check-internal-refs.py` reporting ~4,483 issues in this session, which on inspection was a ~4,421-issue pre-existing baseline already red on `main`, not a regression from the wrap-up work.*

# justification

The internal-reference checker exited non-zero with thousands of findings, which at first glance looked like the wrap-up branch had broken something badly. Filtering to the files this branch actually touched, and re-running the checker on `origin/main`, showed the corpus carried ~4,421 of those issues before the branch existed — almost all cosmetic `BACKTICK_PATH` suggestions that the repo had already logged as a corpus-wide sweep-2 editorial item. Only a handful of genuinely-fixable bare references traced to this branch's new files, and those were fixed in minutes. Without the baseline comparison, an agent either wastes a long pass trying to drive a repo-wide pre-existing count to zero, or wrongly blocks a merge on a red check that was red before it started. The marginal cost of the rule is one extra checker run on the base branch plus a `git diff --name-only` filter; the cost of skipping it is a potential multi-hour wild-goose chase against 4,000+ findings that were never yours.
