# ADR: Per-batch build-review-integrate cadence with a four-axis coverage ledger for spec-corpus runs

- **ID**: ADR-69a2e51aa2
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-31
- **Source retrospective**: ../2026-05-31-220.md
- **PRs covered**: #220

## Context

The v4 architecture is decomposed into 57 components, each owing a spec + plan + adversary review. The Sweep-1 run had to author the 34 unbuilt components under an unattended long-run mandate where "the user will cut the run off when the token window closes." It also inherited a hazard: 23 components were already built, but 11 of them had been produced in an earlier two-track phase and **never adversary-reviewed** — silent review debt invisible to a build-status view. The operator's stated requirement was explicit: "do not miss any that weren't reviewed, and make sure all checks are incorporated." A run structured as build-everything-then-review-everything would have failed catastrophically under truncation (e.g. 34 specs built, 0 reviewed at cutoff) and provided no mechanical guarantee against the inherited debt.

## Decision

Multi-component spec-corpus authoring runs use a per-batch build -> adversary-review -> integrator cadence gated by a four-axis {Built, Reviewed, Incorporated, iNtegrated} coverage ledger, rather than build-all-then-review.

Concretely: components are grouped into dependency-ordered batches; each batch is built (parallel builders), then adversary-reviewed (parallel critic-fixers), then integrated (orchestrator authors numbered cross-component decisions; one integrator subagent applies them corpus-wide and harvests open questions). A batch is "closed" only when its ledger rows are ✓ on all four axes, and the next batch opens only after the previous closes. Inherited review debt is folded into the first review wave.

## Alternatives considered

- **Build-all-then-review-all.** Maximizes early build throughput and batches the review into one phase. Rejected: under a run that can be truncated at any instant, it maximizes the unreviewed surface at every instant and would have left the inherited 11-component debt plus up to 34 new specs unreviewed at an unlucky cutoff. It also defers all cross-component conflict discovery to the very end, when fixes are most expensive.
- **Build + review per component, no integrator pass.** Simpler. Rejected: per-component review cannot resolve cross-component conflicts (naming, ownership, seam mismatches) — those need a corpus-wide pass. Without it, sibling-seam mismatches (e.g. C14↔C15, C26↔C27) and ownership questions (D-13 holdout split) would persist unresolved.
- **A flat checklist instead of a four-axis ledger.** Rejected: a single "done?" column conflates three distinct half-done states (built-but-unreviewed, reviewed-but-not-incorporated, incorporated-but-not-integrated) and cannot surface the inherited debt.

## Consequences

- **Easier:** graceful degradation under truncation (completed batches are always fully closed); mechanical completeness guarantee (every row ✓×4); early discovery of cross-component conflicts at each batch's integrator pass; silent review debt surfaced at stand-up.
- **Harder / accepted trade-offs:** more, smaller waves and more orchestration turns (≈15 waves, ~109 subagent dispatches, many checkpoint commits) than a two-phase build-then-review; the orchestrator must keep two ledgers (coverage + decisions) current every wave.
- **Neutral:** the cadence composes with existing fan-out skills (`disk-fanout-orchestration`, `parallel-subagent-fanout`, `cross-component-decision-ledger`) rather than replacing them — it adds the per-batch review-integrate rhythm and the coverage-ledger guarantee on top.

## References

- [`../2026-05-31-220.md`](../2026-05-31-220.md) — the source retrospective.
- [`./SKILL-SPEC-d7d47fca26-coverage-ledger-batch-cadence.md`](./SKILL-SPEC-d7d47fca26-coverage-ledger-batch-cadence.md) — the skill that operationalizes this decision.
- [`./AGENTS-MD-557513e54b-four-axis-coverage-ledger.md`](./AGENTS-MD-557513e54b-four-axis-coverage-ledger.md) and [`./AGENTS-MD-62c3f73209-per-batch-build-review-integrate.md`](./AGENTS-MD-62c3f73209-per-batch-build-review-integrate.md) — the two agents-file rules distilled from it.
- PR the decision was exercised in: #220.
