# ADR: Advisory CI gates emit dismissible PR reviews, not failing checks

- **ID**: ADR-70fa46b61e
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-21
- **Source retrospective**: ../2026-05-21-113.md
- **PRs covered**: #113

## Context

PR #113's first failure-mode-coverage gate exited the workflow with the linter's status code: lint failure → CI red → merge blocked. That semantics is wrong for the kind of finding the gate produces. The gate detects a structural correspondence: when `architectures/0N-*.md` changes, column N of `architectures/failure-modes.md` should change too. The correspondence is *usually* what we want — but sometimes an architecture-file edit is a typo fix, a citation update, or a non-coverage-bearing prose clarification that doesn't require a column edit. Hard-failing the CI check forces the agent to either (a) add a dummy column edit to satisfy the linter or (b) reach for the `failure-mode-only` label (which is for a different escape-hatch case). Neither captures "the gate is right to ask, and here's why I'm overriding it."

The reviewer named the better shape directly: "Can the CI result be a review on the PR that you can check and either fix the edit or go ahead and ignore review with a comment on the PR why it was ignored." Pattern: the gate's job is to *surface* the finding and require *justification* — not to block categorically. A PR review carries that signal natively: REQUEST_CHANGES is visible, blocks merge under branch protection, and is dismissible by an authorized actor. A failing CI check has no equivalent dismissal-with-justification path.

This pattern is not unique to the failure-mode gate. Any gate whose finding might be legitimately overridden — coverage drops in PRs that delete test infrastructure, style drift in PRs that intentionally adopt a new convention, dependency-pin changes in PRs that knowingly upgrade — has the same shape. Treating these as "soft fails via review" rather than "hard fails via check" makes the override flow first-class.

## Decision

For CI gates whose findings may be intentionally overridden by an agent or human reviewer with justification, emit a REQUEST_CHANGES pull-request review carrying the finding and the override procedure, exit the workflow with status 0, and auto-dismiss any prior bot review on subsequent runs where the condition clears.

The dismissal procedure is part of the gate's contract: every such gate's owning skill documents how to dismiss the review (preferring `mcp__github__pull_request_review_write` with `method=dismiss`, falling back to `gh api -X PUT /reviews/$ID/dismissals`) and what the justification comment should look like (grep-friendly marker like `[Dismissed <gate-name> review: <reason>]`).

Hard-failing CI checks are reserved for properties that are never legitimately overridden: tests passing, builds succeeding, secrets not leaked, security scans clean.

## Alternatives considered

- **Hard-fail CI check + escape via label.** Initial approach. The label-based escape works for one class of override (cell-wording refinements with no arch-doc edit) but doesn't naturally express "the gate is correct to flag this, and here is why I'm overriding it." Labels are flat metadata; a review-and-dismissal carries the conversation.
- **Workflow posts a regular PR comment instead of a review.** Considered. Comments don't block merge under branch protection, so the gate becomes purely advisory with no enforcement. The REQUEST_CHANGES review can be configured (via branch protection) to block merge, giving the project a knob between "advisory" and "blocking" without changing the workflow.
- **Use status checks with a "skippable" name.** Some projects mark certain checks as `optional-*` so branch protection skips them. This works mechanically but doesn't surface the *finding* — the agent sees a red check with no body. The review carries the lint output and the override procedure inline.
- **Dismiss-via-label-removal.** Considered: agent removes a "needs-review" label to signal "I considered this and override". Inverted from the natural review-dismissal flow; reviewers would have to learn a project-specific convention. The native GitHub review-dismissal API is more discoverable.

## Consequences

- **What becomes easier**: agents (and human reviewers) can override an advisory gate via a single action that leaves a durable audit trail (the dismissal message + a `[Dismissed <gate>: <reason>]` comment). The gate's signal is the *content* of the review, not just a red check.
- **What becomes harder**: the workflow must hold `pull-requests: write` permission to post and dismiss reviews — slightly elevated from the read-only default. The dismiss-on-pass logic adds ~10 lines to the workflow. The pattern only blocks merge if branch protection requires approving reviews; on repos without that branch protection rule, the gate becomes advisory-only.
- **Trade-off we accept**: a small amount of GitHub-API-specific code in every gate workflow (the `gh api` calls for post/dismiss) in exchange for an override flow that naturally fits how reviewers think about findings.
- **Pattern reusability**: every gate following this pattern shares the same workflow skeleton — capture lint output, post-or-dismiss based on lint exit code. Future gates can copy it directly. The [`ci-as-pr-review`](./SKILL-SPEC-11b2b1803f-ci-as-pr-review.md) skill spec generalizes the skeleton for reuse.

## References

- [`../2026-05-21-113.md`](../2026-05-21-113.md) — the source retrospective.
- [`./SKILL-SPEC-11b2b1803f-ci-as-pr-review.md`](./SKILL-SPEC-11b2b1803f-ci-as-pr-review.md) — the skill spec for the reusable pattern.
- [`./ADR-b201e941ba-failure-mode-matrix-location-and-ownership.md`](./ADR-b201e941ba-failure-mode-matrix-location-and-ownership.md) — the sibling ADR for the location-and-ownership decision; the gate built under that ADR is the first instance of this pattern.
- The first instance: `.claude/skills/architecture-failure-mode-gate/resources/_workflows/failure-modes-gate.yml`.
- PR the decision was made in: #113.

<!--
PROMOTION NOTE:
When this draft is adopted into docs/adr/ via the `adr` skill, preserve
the `**ID**: ADR-70fa46b61e` line verbatim. The NNNN number in the
docs/adr/ filename is a separate human-friendly sequence; the hash is
the durable identifier and must not drift.
-->
