# ADR 0007: Advisory CI gates emit dismissible PR reviews, not failing checks

- **ID**: ADR-70fa46b61e
- **Status**: Accepted
- **Date**: 2026-05-21

## Context

[PR #113](https://github.com/lago-morph/software-factory/pull/113)'s first attempt at the failure-mode-coverage gate exited the workflow with the linter's status code: lint failure → CI red → merge blocked. That semantics is wrong for the kind of finding the gate produces. The gate detects a structural correspondence — when [`architectures/0N-*.md`](../../architectures/) changes, column N of [`architectures/failure-modes.md`](../../architectures/failure-modes.md) should change too. The correspondence is *usually* what we want, but sometimes an architecture-file edit is a typo fix, a citation update, or a non-coverage-bearing prose clarification that does not require a column edit. Hard-failing the CI check forced the agent to either (a) add a dummy column edit to satisfy the linter or (b) reach for the `failure-mode-only` label (which is for a different escape-hatch case). Neither captures "the gate is right to ask, and here is why I am overriding it."

The reviewer named the better shape directly: *"Can the CI result be a review on the PR that you can check and either fix the edit or go ahead and ignore review with a comment on the PR why it was ignored."* Pattern: the gate's job is to *surface* the finding and require *justification* — not to block categorically. A PR review carries that signal natively — REQUEST_CHANGES is visible, blocks merge under branch protection, and is dismissible by an authorized actor. A failing CI check has no equivalent dismissal-with-justification path.

This pattern is not unique to the failure-mode gate. Any gate whose finding might be legitimately overridden — coverage drops in PRs that delete test infrastructure, style drift in PRs that intentionally adopt a new convention, dependency-pin changes in PRs that knowingly upgrade — has the same shape. Treating these as "soft fails via review" rather than "hard fails via check" makes the override flow first-class.

## Decision

For CI gates whose findings may be intentionally overridden by an agent or human reviewer with justification, the workflow emits a REQUEST_CHANGES pull-request review carrying the finding and the override procedure, exits with status 0, and auto-dismisses any prior bot-authored review on subsequent runs where the underlying condition clears.

Each such gate's owning skill documents the dismissal procedure, preferring `mcp__github__pull_request_review_write` with `method=dismiss` and falling back to `gh api -X PUT /repos/{owner}/{repo}/pulls/{pr}/reviews/{id}/dismissals`. Every dismissal is paired with a comment in a grep-friendly format (`[Dismissed <gate-name> review: <reason>]`) so the audit trail is searchable.

Hard-failing CI checks are reserved for properties that are never legitimately overridden: tests passing, builds succeeding, secrets not leaked, security scans clean.

## Alternatives considered

- **Hard-fail CI check + escape via label.** The initial approach in PR #113. The label-based escape works for one class of override (cell-wording refinements with no arch-doc edit) but does not naturally express "the gate is correct to flag this, and here is why I am overriding it." Labels are flat metadata; a review-and-dismissal carries the conversation.
- **Workflow posts a regular PR comment instead of a review.** Comments do not block merge under branch protection, so the gate becomes purely advisory with no enforcement. The REQUEST_CHANGES review can be configured (via branch protection) to block merge, giving the project a knob between "advisory" and "blocking" without changing the workflow.
- **Use status checks with a "skippable" name.** Some projects mark certain checks as `optional-*` so branch protection skips them. This works mechanically but does not surface the *finding* — the agent sees a red check with no body. The review carries the lint output and the override procedure inline.
- **Dismiss-via-label-removal.** Agent removes a "needs-review" label to signal "I considered this and override". Inverted from the natural review-dismissal flow; reviewers would have to learn a project-specific convention. The native GitHub review-dismissal API is more discoverable.

## Consequences

Agents and human reviewers can override an advisory gate via a single action that leaves a durable audit trail (the dismissal message plus a `[Dismissed <gate>: <reason>]` comment). The gate's signal is the *content* of the review, not just a red check.

The workflow must hold `pull-requests: write` permission to post and dismiss reviews — slightly elevated from the read-only default. The dismiss-on-pass logic adds roughly ten lines to each gate workflow. The pattern only blocks merge if branch protection requires approving reviews; on repos without that branch protection rule, the gate becomes advisory-only by design.

We accept a small amount of GitHub-API-specific code in every gate workflow (the `gh api` calls for post and dismiss) in exchange for an override flow that naturally fits how reviewers think about findings. Every gate following this pattern shares the same workflow skeleton — capture lint output, post-or-dismiss based on lint exit code — so future gates can copy it directly. The proposed [`ci-as-pr-review`](../../retrospective/2026-05-21-113/SKILL-SPEC-11b2b1803f-ci-as-pr-review.md) skill spec generalizes the skeleton for reuse.

## References

- [retrospective 2026-05-21-113](../../retrospective/2026-05-21-113.md) — source retrospective for this ADR.
- [retrospective/2026-05-21-113/ADR-70fa46b61e-advisory-ci-gates-as-pr-reviews.md](../../retrospective/2026-05-21-113/ADR-70fa46b61e-advisory-ci-gates-as-pr-reviews.md) — draft this ADR was adopted from.
- [retrospective/2026-05-21-113/SKILL-SPEC-11b2b1803f-ci-as-pr-review.md](../../retrospective/2026-05-21-113/SKILL-SPEC-11b2b1803f-ci-as-pr-review.md) — proposed skill spec for the reusable pattern.
- [retrospective/2026-05-21-113/ADR-b201e941ba-failure-mode-matrix-location-and-ownership.md](../../retrospective/2026-05-21-113/ADR-b201e941ba-failure-mode-matrix-location-and-ownership.md) — sibling ADR draft; the gate built under that decision is the first instance of this pattern.
- [`architecture-failure-mode-gate` workflow template](../../.claude/skills/architecture-failure-mode-gate/resources/_workflows/failure-modes-gate.yml) — the first instance.
- [`architecture-failure-mode-gate/SKILL.md`](../../.claude/skills/architecture-failure-mode-gate/SKILL.md) — "Handling the gate review" section documents the agent's response procedure.
- PR the decision was made in: [#113](https://github.com/lago-morph/software-factory/pull/113).
