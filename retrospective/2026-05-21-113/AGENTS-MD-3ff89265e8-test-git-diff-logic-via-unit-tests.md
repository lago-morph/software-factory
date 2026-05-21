# agent instruction

**Test git-diff-driven logic via unit tests, not sandboxed commits.** When validating a script that consumes `git diff <base>...HEAD` output, do not attempt to test it by creating commits inside a temporary `git worktree add` or `cp -r .git /tmp/...` setup — commit signing in the Claude Code sandbox is bound to the main working tree and fails with `"missing source"` inside copies. Instead, factor the diff-consuming logic into a pure function (e.g., `changed_columns(old_text, new_text)`) and unit-test it with synthetic before/after strings. The unit test is faster, deterministic, and survives the sandbox's commit-signing constraints.

*Grounded in: PR #113 `lint-failure-modes.py` verification — git worktree commits failed; Python unit tests with synthetic table strings worked.*

# justification

I tried twice to validate the lint logic by creating a sandbox via `git worktree add /tmp/...` and `cp -r .git /tmp/...`, and both attempts failed at the `git commit` step with `signing server returned status 400 ... missing source`. The signing endpoint is bound to the main working tree's path and refuses to sign commits from any copy. The recovery — factoring `changed_columns(old_text, new_text)` into a pure function and writing seven synthetic test cases (no-op, single-col change, multi-col change, header rename, row add, row delete, mixed) — took ~3 minutes and produced more thorough coverage than the commit-based test ever would have. Adopting this rule saves the next agent five-to-ten minutes of fruitless sandbox experimentation and produces a strictly better test suite. The marginal cost is "design the function to be testable in isolation," which is good code architecture regardless.
