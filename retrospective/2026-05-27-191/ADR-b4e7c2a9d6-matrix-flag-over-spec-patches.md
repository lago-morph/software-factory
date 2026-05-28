# ADR: Matrix-flag-aggregation over per-spec-patches when audit-recommended

- **ID**: ADR-b4e7c2a9d6
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-27
- **Source retrospective**: ../2026-05-27-191.md
- **PRs covered**: #187, #188, #189, #190, #191, #192

## Context

Phase 7 of the v3 architecture synthesis ran a per-candidate parallel back-fill audit (9 candidates against 9 archive files) plus a silent-absorption auditor + a historian as bias-guard subagents. At fanout-close, the silent-absorption auditor surfaced 15 findings (3 high-confidence / 7 medium / 5 low), and the per-candidate subagents themselves surfaced an additional set of cells where the candidate's spec carried archive content "with adaptation" — i.e., the substance was absorbed but the explicit archive citation was missing.

The auto-007 brief defined Wave 7.3 as a conditional spec-patch fanout: ≥4 candidates needing patches triggers Phase-7-followup deferral. At aggregation time the realistic patch count was 7+ candidates if every silently-absorbed cell triggered a patch — well above the threshold. Firing the deferral would have produced a binding-artifact triple (handoff stub + morning-summary bullet + next-run dispatch prompt) for ~7 candidate-level spec-patch tasks the next run would have to drain.

But the auditor itself, in its recommendation #5, explicitly named an alternative: instead of patching specs, flag the cells in the aggregation matrix and carry the cite obligations forward as inputs to the Phase-8 lean-eval briefs. This works because the silently-absorbed material is a *citation gap* (the spec content already includes the substance; only the archive cite is missing), not a *content gap* (which would require substantive spec edits).

## Decision

When an audit / bias-guard subagent's recommendation list explicitly names a "matrix-flag + downstream-phase cite obligation" alternative to per-spec patches, AND the lead-agent verifies that firing per-candidate patches would exceed the run's deferral threshold, the lead agent SHALL prefer the matrix-flag alternative — documenting the decision inline in the aggregation file with explicit reasoning and a user-override path — instead of firing the deferral.

## Alternatives considered

- **Fire all patches (≥7 candidates) → trigger Phase-7-followup deferral.** Rejected because (a) the deferral mechanism is designed for *content* gaps the current run cannot resolve; (b) it would push 7 mechanically-trivial cite-additions to the next run, where they would re-saturate context for no analytical benefit; (c) the binding-artifact triple instantiation cost (handoff stub, morning-summary line, dispatch prompt) is asymmetric with the trivial patch work.
- **Cherry-pick the top 3 candidates' patches (stay under threshold).** Rejected because the cherry-pick boundary is arbitrary — any defensible rank ordering would have to be by silent-absorption auditor confidence, but that ordering is exactly what the matrix-flag alternative captures more cleanly without the cherry-pick.
- **Defer the question to the morning user as a blocker** (zero PRs in the run; ask user at run close). Rejected because the autonomous-run skill explicitly handles decisions of this shape via decision brief + adversarial review + lead-agent call, not via deferral to the morning user. The user-override surface remains available regardless.
- **Fire no patches; do not flag in matrix; rely on Phase-8 briefs to rediscover the gap.** Rejected because the cite obligations are knowable now and would be silently lost if not flagged.

## Consequences

What becomes easier:
- PR-cap preservation. Phase 7 ran in 6 PRs against the 15-PR cap; firing 7+ patches would have made it 13 PRs.
- Separation of concerns. Citation gaps become explicit Phase-8 brief inputs rather than late-Phase-7 surgical edits.
- The aggregation matrix becomes the citation log of record. Future agents reading the matrix know which cells carry cite-forward obligations.

What becomes harder:
- The Phase-8 brief authoring task inherits a structured cite obligation it must honor (per the Phase-7-close handoff's "3 Phase-8 load-bearing inputs" section). If Phase-8 dispatch ignores the matrix flags, the cite obligations are lost.
- The morning-review user must explicitly verify the lead-agent matrix-flag decision (or override). The decision is rewindable but requires a follow-up run to undo.

Trade-off accepted: the aggregation matrix is the durable citation log; Phase-8 lean-eval briefs are the implementation surface for honoring cite obligations. We are explicitly NOT treating "every silently-absorbed cell needs a spec patch" as a binding rule.

## References

- [`../2026-05-27-191.md`](../2026-05-27-191.md) — the source retrospective.
- [`./ADR-3f8c1e5b7a-bias-guards-concurrent-with-fanout.md`](./ADR-3f8c1e5b7a-bias-guards-concurrent-with-fanout.md) — sibling ADR; the bias-guard pattern that produces the audit recommendations this ADR governs.
- [`./SKILL-SPEC-6a3f1b2c8d-per-candidate-back-fill-audit-fanout.md`](./SKILL-SPEC-6a3f1b2c8d-per-candidate-back-fill-audit-fanout.md) — related skill spec (back-fill audit fanout pattern).
- [`./AGENTS-MD-7d9c4e1b3a-matrix-flag-over-spec-patches.md`](./AGENTS-MD-7d9c4e1b3a-matrix-flag-over-spec-patches.md) — proposed AGENTS.md rule codifying the matrix-flag preference.
- Source aggregation document: [`architectures/v3/backfill-notes.md` §5 Wave 7.3 decision](../../architectures/v3/backfill-notes.md#5-wave-7-3-spec-patch-decision-lead-agent-decision).
- PRs the decision was made in: #190 (aggregation), #191 (handoff carries the decision forward to Phase 8).
