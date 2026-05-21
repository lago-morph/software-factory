# agent instruction

**Use `origin/main`, not local `main`, as the diff base for review.** When computing what changed on a feature branch — for a PR review, a retrospective scope check, a "what did this session do?" survey, or any cross-branch diff — use `origin/main` as the base reference, never the local `main` branch. Examples: `git diff origin/main..HEAD`, `git log origin/main..HEAD`, `git merge-base origin/main HEAD`. The same applies inside scripts that compute scope (e.g., the retrospective skill's session-scope detection).

*Grounded in: PR #122 review pass — local `main` was stale relative to `origin/main`, making the YAML frontmatter on architecture docs appear "added in this PR" when it was already on `origin/main`.*

# justification

The remote execution environment clones the repo fresh per session, which means the local `main` branch reflects whatever `main` looked like at clone time. By the time an agent is reviewing or retrospecting partway through a session, `origin/main` may have advanced (other PRs merged, auto-regeneration commits landed) but the local `main` branch still points at the original clone state. `git diff main..HEAD` therefore shows a larger diff than the PR's reviewer-visible diff — and the divergent lines look like changes this session made.

In PR #122 specifically, the YAML `based-on-commit` / `based-on-date` frontmatter on `architectures/01..03` showed as added in the `main..claude/fix-issue-104-5LzU6` diff, which would have made me explain (or panic-fix) something I hadn't actually touched. `origin/main..claude/fix-issue-104-5LzU6` showed the truth: my changes are exactly the one-line Lineage edits the bot reviewed. The cost of getting this wrong is wasted investigation time and the risk of "correcting" something that doesn't need correcting. The cost of the rule is one extra character (`origin/`) at every diff invocation — trivial. The rule generalises beyond review: scope detection, commit-walking, retro-coverage analysis all depend on the same base.
