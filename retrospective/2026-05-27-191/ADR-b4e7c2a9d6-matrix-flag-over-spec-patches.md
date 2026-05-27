# ADR: Matrix-flag-aggregation over per-spec-patches when audit-recommended

- **ID**: ADR-b4e7c2a9d6
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-27
- **Source retrospective**: ../2026-05-27-191.md
- **PRs covered**: #187, #188, #189, #190, #191

## Context

The Phase-7 back-fill audit (auto-007) ran a per-candidate fanout of 9 subagents + 2 bias-guard subagents (silent-absorption auditor + historian) against 9 archive files. At lead-agent aggregation, the silent-absorption auditor returned 3 `high`-confidence findings whose silently-absorbed cells touched 7+ distinct candidate specs (the four-step Compound-Engineering loop appeared in 7 specs without an archive cite; the four-architecture taxonomy in 5 specs; the Atelier knowledge-doc category set in 1 spec — collectively 7+ candidates whose specs would each have needed a patch if every silently-absorbed cell triggered one).

The auto-007 brief's Wave-7.3 contingency named a ≤3-candidate threshold for in-run spec patches; ≥4 patches triggers Phase-7-followup deferral. The silent-absorption auditor's recommendation #5 explicitly named an alternative: matrix-flag aggregation row + Phase-8 lean-eval-brief cite obligation INSTEAD OF per-spec patches. The lead agent had to choose: fire 7+ patches → triggers deferral and 7+ unnecessary PRs; OR cherry-pick top 3 candidates → arbitrary boundary leaving 4+ unaddressed; OR adopt the matrix-flag alternative → preserves PR-cap and treats the citation gap as exactly what it is.

The substantive insight that made the matrix-flag the cleaner mechanism: silently-absorbed material is a **citation gap**, not a **content gap**. Spec patches would add cites without changing substantive content. A deferral is the wrong mechanism because deferrals imply unresolved content questions that need a successor run to decide; here there is nothing to decide — the cite obligation is mechanical and Phase-8 lean-eval briefs are the natural place to honor it.

## Decision

When an audit subagent's recommendation list includes a matrix-flag-aggregation alternative AND firing per-spec patches for every audit-flagged cell would exceed the run's deferral threshold, the lead agent prefers the matrix-flag + downstream-phase cite-obligation approach over either firing patches or firing the deferral.

Concretely: the aggregation file (a) annotates each silently-absorbed cell with a `flagged-for-Phase-N-cite` marker, (b) carries an explicit paragraph naming the alternative the auditor recommended, the patch-count check, and the lead-agent reasoning, (c) hands the cite obligation forward into the next phase's brief as a row in its scope envelope. Zero spec patches fire; zero deferrals fire.

## Alternatives considered

- **Fire all spec patches (7+ candidates).** Rejected: triggers the Phase-N-followup deferral mechanism even though there is nothing semantically to defer (mechanical cite-additions, not content rework). Wastes 4+ PR slots against the run's PR-cap budget. Future agents reading the deferral will spend effort decoding "why was this deferred?" only to find trivial cites.
- **Cherry-pick top 3 candidates for spec patches.** Rejected: the boundary is arbitrary (why these three and not the other four?). Leaves 4+ silently-absorbed cells unaddressed without any record of why they were skipped. Creates a half-state that is worse than either firing all patches or firing none.
- **Skip the cite obligation entirely.** Rejected: the auditor's `high`-confidence findings are genuine citation gaps; ignoring them leaves the silent-absorption pattern intact for the next phase to inherit silently.
- **Author one omnibus spec-patch PR touching all 7+ specs.** Rejected: violates the cluster-by-cluster discipline of the original Wave-7.3 plan; smears a single PR across 7+ specs whose patches are mechanically distinct; aggregation-matrix already captures the same information at zero PR cost.

## Consequences

**Easier.** The PR-cap budget is preserved (Phase 7 closed at 6 PRs against a 15-PR budget). The aggregation matrix becomes the citation-log-of-record for silent-absorption cells, which is the right place for cross-spec citation patterns (no single spec's patch would have captured the cross-spec view anyway). Phase-N-followup carries a smaller, more semantically-meaningful set forward (only true content gaps, not citation gaps).

**Harder.** The next phase's lean-eval briefs MUST honor the cite-obligation rows or the citation gap persists across phases. Phase-8 entry posture in the close handoff has to call this out explicitly (and it does — the Phase-7-close handoff names the cite-obligation rows as Phase-8 binding constraints). The aggregation matrix becomes a load-bearing artifact that must survive successor phases without being silently re-flattened.

**Trade-off accepted.** We accept that the aggregation matrix is the citation log of record (not the per-spec content). Readers looking for "where does spec X cite archive file Y" will find a `flagged-for-Phase-N-cite` annotation in the matrix rather than an inline cite in the spec. The trade-off is mechanically obvious and documented at the matrix-flag row.

## References

- [`../2026-05-27-191.md`](../2026-05-27-191.md) — the source retrospective (see Phase 6 — Lead-agent aggregation + Wave 7.3 decision).
- [`./SKILL-SPEC-6a3f1b2c8d-per-candidate-back-fill-audit-fanout.md`](./SKILL-SPEC-6a3f1b2c8d-per-candidate-back-fill-audit-fanout.md) — the per-candidate fanout skill that produces the matrix this ADR governs.
- [`./SKILL-SPEC-3c5b9e8f47-silent-absorption-precedence-with-confidence.md`](./SKILL-SPEC-3c5b9e8f47-silent-absorption-precedence-with-confidence.md) — the confidence-threshold reconciliation rule that scopes which auditor findings actually trigger the matrix-flag-vs-patch decision.
- [`./AGENTS-MD-7d9c4e1b3a-matrix-flag-over-spec-patches.md`](./AGENTS-MD-7d9c4e1b3a-matrix-flag-over-spec-patches.md) — the proposed AGENTS.md rule encoding this decision as a binding lead-agent obligation.
- [`../../architectures/v3/backfill-notes.md`](../../architectures/v3/backfill-notes.md) — the Phase-7 aggregation file where the matrix-flag decision is documented inline (§5 Wave-7.3 decision section).
- [`../../architectures/v3/backfill-notes/audit-silent-absorption.md`](../../architectures/v3/backfill-notes/audit-silent-absorption.md) §C #5 — the auditor recommendation that named the alternative.
- [`../../architectures/v3/decisions/auto-007-phase-7-dispatch-shape.md`](../../architectures/v3/decisions/auto-007-phase-7-dispatch-shape.md) — the brief that established the ≤3-candidate threshold and Wave-7.3 contingency.
- PRs the decision was made in: #190 (aggregation file carrying the matrix-flag), #191 (Phase-7-close handoff carrying the cite obligation forward).
