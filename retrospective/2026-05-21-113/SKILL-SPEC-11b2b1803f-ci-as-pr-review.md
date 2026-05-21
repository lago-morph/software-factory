# Spec: `ci-as-pr-review`

- **ID**: SKILL-SPEC-11b2b1803f
- **Source retrospective**: ../2026-05-21-113.md

## Intent

A pattern + helper utilities for CI workflows that surface advisory findings the agent or human reviewer may override with justification. Instead of failing the CI check (which blocks merge categorically), the workflow posts a REQUEST_CHANGES PR review with the finding and explicit override instructions; on a subsequent run where the underlying condition clears, the workflow auto-dismisses any prior bot-authored review. Agents respond by either fixing the issue or dismissing the review with a justification comment that becomes the audit trail.

The motivating session moment: PR #113's first attempt at the failure-mode gate exited non-zero on lint failure, which blocks merge via branch protection. The reviewer asked: "Can the CI result be a review on the PR that you can check and either fix the edit or go ahead and ignore review with a comment on the PR why it was ignored." That's a different gate semantics — *advisory, dismissible with justification, but visible enough to require action*. The pattern emerged: workflow posts REQUEST_CHANGES + exits 0; on next clean run, dismiss prior reviews; agents dismiss-with-comment for material-but-OK overrides.

## Trigger

**Direct triggers**:
- "Make the CI gate post a review instead of failing the check."
- "I want to be able to dismiss this CI check with a comment."
- "Advisory CI gate" / "soft-fail CI" / "dismissible CI gate."

**Proactive triggers**:
- A new CI workflow is being authored whose findings are sometimes intentional (lint-warnings-as-blocking, coverage-drop-acceptable, style-drift-justified).
- A reviewer asks "why is CI red — that was intentional?"
- The user mentions "override the gate" / "skip this check just this once" patterns.

**Negative triggers**:
- The gate enforces a hard safety property (secret leaked, build broken, tests failed) — those should hard-fail the check, not request changes.
- The repo has no branch protection requiring approving reviews — REQUEST_CHANGES is non-blocking in that case, and the pattern degrades to "advisory comment".
- The finding is so frequent that posting/dismissing a review on every PR becomes noise.

## Inputs

- `workflow_name` — display name and filename slug (e.g., `failure-modes-gate`).
- `lint_command` — the command whose exit code drives the gate (e.g., `python .../lint-failure-modes.py --check-diff ${BASE_SHA}`).
- `paths_filter` — `paths:` list for the `pull_request` trigger.
- `review_body_template` — the multi-line markdown body for the REQUEST_CHANGES review on failure, with placeholders for the lint output and the override-procedure URL.
- `bot_login` — the bot whose prior reviews to dismiss (default `github-actions[bot]`).

## Outputs

- A `.github/workflows/<workflow_name>.yml` (or a skill-installed template + install script if the skill is self-bootstrapping) that:
  - Runs the lint command with `continue-on-error: true`.
  - Captures stdout into a step output for the review body.
  - Always exits 0 from the workflow itself.
  - Posts a REQUEST_CHANGES review when lint fails.
  - Dismisses any prior bot REQUEST_CHANGES review when lint passes.

## Workflow

1. **Decide on self-installing vs in-tree workflow.** If the gate has its own skill (matrix-source-coupling-gate style), the workflow lives as a template under `resources/_workflows/`; otherwise it lives directly under `.github/workflows/`.
2. **Author the workflow YAML.** Use the canonical structure:
   - `on: pull_request: types: [opened, synchronize, reopened, labeled, unlabeled]` — `labeled` is critical so override-via-label can trigger a re-run.
   - `permissions: pull-requests: write` — required for posting and dismissing reviews.
   - Step 1: any label-detection logic that sets environment variables (e.g., `FAILURE_MODE_ONLY=1`).
   - Step 2: run lint, capture output into `GITHUB_OUTPUT`. Use `continue-on-error: true` and `exit 0` inside the step.
   - Step 3: `gh api` to find prior `github-actions[bot]` REQUEST_CHANGES reviews. Branch on lint result: pass → dismiss them; fail → post a new one with the captured output + override procedure.
3. **Write the review body template.** Three sections: lint output in a code block, "What to do" with bullet points (fix vs dismiss-with-justification vs apply-override-label), link to the skill's "Handling the gate review" section.
4. **Wire in the dismissal procedure** to the agent-facing skill doc:
   - `mcp__github__pull_request_review_write` with `method=dismiss` and `review_id` + `message` arguments — preferred (runs as the session's GitHub identity).
   - `gh api -X PUT /repos/.../reviews/$REVIEW_ID/dismissals -f message="..."` fallback.
   - Always post an explanatory comment alongside (e.g., `[Dismissed failure-mode gate review: <reason>]`) so the audit trail is grep-able.
5. **Test against a synthetic failure.** Create a test PR (or branch) that triggers the lint failure; confirm the workflow posts the review, does not fail the check, and that a subsequent fix-commit causes the review to auto-dismiss.

## Concrete examples

### Example 1: Failure-mode gate workflow (PR #113's actual instance)

The workflow at `.github/workflows/failure-modes-gate.yml`:
- Lints `architectures/failure-modes.md` vs `architectures/0N-*.md` files.
- On failure: posts a REQUEST_CHANGES review with the lint errors, the override procedure ("apply `failure-mode-only` label, or fix the column, or dismiss with justification"), and a link back to `.claude/skills/architecture-failure-mode-gate/SKILL.md`.
- On pass: dismisses any prior bot REQUEST_CHANGES review on the PR with message `"Gate now passing at <HEAD_SHA>."`.

The review body's "What to do (agent or human reviewer)" section reads:

> 1. Decide whether the architecture change materially affects failure-mode coverage. The skill documents what counts as "material" at `.claude/skills/architecture-failure-mode-gate/SKILL.md` "Handling the gate review".
> 2. If YES — update only the corresponding column in `architectures/failure-modes.md` and push. This review will auto-dismiss when lint passes.
> 3. If NO — dismiss this review with a justification comment explaining why the change does not affect coverage.

### Example 2: A hypothetical coverage-drop-acceptable advisory gate

A workflow that runs the project's coverage tool, compares to the base branch coverage, and emits a REQUEST_CHANGES review if coverage dropped by >1pp. The review body lists the changed files and their coverage deltas, plus "If the drop is intentional (deleted test infrastructure, dead code removal), dismiss this review with a comment naming the specific change that justifies the drop." Branch protection requires the review to be dismissed (or coverage to come back up) before merge. Hard-failing the CI check would be wrong because intentional drops are legitimate; not gating at all would let unintentional drops accumulate silently.

## Anti-patterns

- **Posting a new review on every workflow run regardless of state.** The pattern is "post on failure, dismiss on pass" — not "post on failure, leave forever". Without the dismiss step, the PR accumulates stale REQUEST_CHANGES reviews that no longer reflect the current state.
- **Failing the check AND posting the review.** Pick one. If the check fails, the review is redundant noise; the check is the blocker. The whole point of the pattern is that the review is the dismissible signal, and the check itself stays green.
- **Forgetting the `labeled` trigger.** Without it, applying an override label doesn't re-run the workflow, so the dismissal doesn't fire. The `labeled, unlabeled` types must be in the `on: pull_request: types:` list.
- **Embedding the lint output via shell variable expansion outside of a heredoc.** Lint output may contain backticks, dollar signs, and special characters. Use a `cat <<EOF`-style heredoc to construct the review body, with the lint output passed via an env var to avoid shell parsing.
- **Skipping the audit-trail comment when dismissing.** A dismissal without an accompanying comment is invisible to future reviewers. Always pair the dismissal with a comment that explains why, in a grep-friendly format like `[Dismissed <gate-name> review: <reason>]`.

## Acceptance criteria

- [ ] On lint failure, the workflow posts exactly one REQUEST_CHANGES review with the lint output and override procedure visible in the body.
- [ ] On lint pass after a prior failure, the workflow dismisses the prior review with a non-empty message and posts no new review.
- [ ] The workflow itself exits 0 in both pass and fail cases (the review is the signal).
- [ ] Applying the override label triggers a re-run of the workflow (via the `labeled` trigger type).
- [ ] The skill doc that consumes the review documents both the MCP-based and `gh api` dismissal procedures.

## Files this skill creates / modifies

- `.github/workflows/<workflow_name>.yml` — the workflow, either directly or as a template under a parent skill's `resources/_workflows/`.
- The parent skill's `SKILL.md` (if applicable) — "Handling the gate review" section spelling out the agent's response procedure.
- (Optional) A helper script under the parent skill or `.github/scripts/` that constructs the review body from lint output + override-procedure template.
