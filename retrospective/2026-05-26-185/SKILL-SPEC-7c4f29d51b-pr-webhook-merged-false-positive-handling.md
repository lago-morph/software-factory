# SKILL-SPEC-7c4f29d51b — pr-webhook-merged-false-positive-handling

## Name
`pr-webhook-merged-false-positive-handling`

## Priority
**Medium.** Webhook false-positives are rare but can corrupt the PR-shape decision tree.

## Description (for skill discovery)
When a `<github-webhook-activity>` event reports a PR as merged, verify before acting. Triggers automatically on `<github-webhook-activity>` events with `outcome` field containing "merged".

## What this skill does

1. Receives a `<github-webhook-activity>` event reporting PR #N as merged.
2. **Before** unsubscribing or making any PR-shape decision based on the merge, calls `mcp__github__pull_request_read` (`method: "get"`, `pullNumber: N`).
3. Inspects the response:
   - `state == "closed"` AND `merged == true` → confirmed merged; proceed as normal.
   - `state == "open"` OR `merged == false` → webhook false-positive; **do not unsubscribe**; treat the PR as still open.
4. If false-positive: log a one-line acknowledgement in the next PR description or session handoff so the audit trail captures the event.

## When NOT to use
- For non-PR webhook events.
- When acting on the merged signal would be cheap to undo (e.g., closing an issue that can be reopened).

## Recovery if a false-positive was already acted on
- If a second PR was opened on the same branch and rejected by GitHub (`A pull request already exists for ...`): update the original PR in-place via `mcp__github__update_pull_request` to reflect the new scope. Document the consolidation in the PR body's "deviation acknowledgement" section.
- If commits continued onto the still-open PR's branch: the PR auto-accumulated the new work; verify scope-fit and update the PR's title and body accordingly.

## Origin event
2026-05-26 Phase-6 autonomous run: PR #183 webhook fired `merged` while PR was still open (state="open", merged=false). Lead agent continued committing on the same branch; subsequent attempt to open a second PR failed with the existing-PR error. Recovery via in-place PR-body update worked (and saved 3 PRs against the cap as an unintended positive), but the same mechanism could just as easily skip a PR that didn't merge.
