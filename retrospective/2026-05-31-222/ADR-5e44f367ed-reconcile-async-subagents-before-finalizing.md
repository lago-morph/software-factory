# ADR: Reconcile async background subagents against committed state before finalizing a wave

- **ID**: ADR-5e44f367ed
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-31
- **Source retrospective**: ../2026-05-31-222.md
- **PRs covered**: #222

## Context

This session dispatched ten-plus subagents, several `run_in_background: true`, across overlapping waves (panel opinions, two guide authors, two spec-annotation integrators, a consistency-checker, a verdict synthesizer). Because the harness surfaced their completions asynchronously — and because the Bash tool was intermittently returning empty/garbled output during the same window — the orchestrator twice acted on an incomplete picture of what was actually on disk. In one case a spec-annotation subagent I had assumed failed (wrong-filename brief) actually completed nine minutes later, after I had already dispatched a retry; both wrote the same annotations, leaving duplicates in the working tree that had to be reverted against `git show HEAD:`. In another, a consistency subagent's committed, evidence-rich report was overwritten by a hand-reconstruction made off a corrupted read, then restored from git. The common root cause: treating "I haven't heard back" or "my last read looked empty" as equivalent to "the work isn't there," when background subagents and racing writers make the committed tree the only authority.

## Decision

When background subagents may write the same files as foreground work, reconcile every late-completing subagent's output against the committed tree — reverting duplicates and keeping the demonstrably-superior version — before declaring the wave done or finalizing the PR.

## Alternatives considered

- **Run all subagents in the foreground (no `run_in_background`).** Eliminates the async race but serializes independent work that has no dependencies, throwing away the main benefit of fan-out. Rejected: the parallelism is the point; the fix is reconciliation discipline, not giving up concurrency.
- **Forbid subagents from touching files the lead also edits.** A disjoint-file contract is the existing fan-out pattern and works when plannable, but this session's retries and the consistency-checker legitimately needed to touch the same files the lead had staged. Rejected as too restrictive for reconciliation-style waves; kept as the default where files *can* be partitioned.
- **Trust each subagent's returned receipt as the record of what changed.** Receipts are summaries, not ground truth — a receipt saying "all annotations present, no edits needed" is exactly what the late duplicate-writer returned. Rejected: the committed tree, not the receipt, is authoritative.

## Consequences

Easier: a wave's final state is trustworthy because it is reconciled against `git show HEAD:` / `git status` rather than against memory of what each subagent reported. Duplicate or stale artifacts are caught before they ship. Harder: every multi-subagent wave now ends with an explicit reconciliation step — read the committed blobs of the touched files, diff against intent, revert duplicates — which adds a few tool calls per wave. Accepted trade-off: a small, bounded reconciliation cost at each wave boundary in exchange for not shipping duplicated annotations or a clobbered report, both of which actually occurred this session and cost more to undo than the reconciliation would have cost to prevent.

## References

- [`../2026-05-31-222.md`](../2026-05-31-222.md) — the source retrospective.
- [`./AGENTS-MD-efcebc57aa-verify-committed-tree-after-revert.md`](./AGENTS-MD-efcebc57aa-verify-committed-tree-after-revert.md) — the per-rule corollary (verify committed tree, not working tree).
- [`./AGENTS-MD-5fb2170cda-distrust-corrupted-tool-output.md`](./AGENTS-MD-5fb2170cda-distrust-corrupted-tool-output.md) — the per-rule corollary on corrupted reads.
- PRs the decision was made in: #222.
