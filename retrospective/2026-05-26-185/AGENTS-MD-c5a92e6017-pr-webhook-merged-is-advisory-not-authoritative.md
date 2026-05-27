# agent instruction

**PR webhook `merged` is advisory, not authoritative.** When a `<github-webhook-activity>` event reports a PR as merged, the agent MUST verify via `mcp__github__pull_request_read` (`method: "get"`) before acting on the notification. The webhook's `state` field is event-time, not necessarily current; webhook delivery is asynchronous and can fire on a transient "merged" signal that the API later contradicts. The verification call costs one API roundtrip and prevents the agent from re-creating PRs that already exist or skipping PRs that did not merge.

*Grounded in: 2026-05-26 Phase-6 run — PR #183 webhook fired `merged` while the PR was still open. Lead agent continued committing on the same branch (which the still-open PR auto-accumulated); subsequent attempt to open a second PR for the Phase-6 omnibus failed with `A pull request already exists for ...`. Net outcome was positive (the consolidation saved 3 PRs against the cap) but the resolution required updating PR #183's title and body in-place.*

# justification

The webhook is a useful early signal but not a contract. Verifying via the read API is cheap (one tool call) and catches the rare false-positive. The Phase-6 case was net-positive — the consolidation worked out — but the same mechanism could just as easily skip a PR that actually didn't merge, causing real work loss. Rule cost: one API call per `merged` webhook event. Asymmetric cost without: each false-positive risks PR-shape decisions made on bad data.
