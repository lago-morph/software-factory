# ADR: Bias-guards concurrent with per-candidate fanout when input streams are independent

- **ID**: ADR-3f8c1e5b7a
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-27
- **Source retrospective**: ../2026-05-27-191.md
- **PRs covered**: #188, #190

## Context

In a per-candidate parallel fanout pattern, two classes of subagents operate on overlapping but distinct input streams. The **per-candidate workers** (Phase 7: 9 back-fill subagents, one per candidate-spec) read their assigned candidate's spec + the shared archive + the exemplar + the dispatch brief. The **bias-guard subagents** (Phase 7: silent-absorption auditor + historian) read all candidate specs + the shared archive — but NOT the per-candidate audit outputs (which don't exist yet at dispatch time and would create a circular dependency if waited-on).

Phase 6's Wave 6.5 verification subagent ran AFTER the per-candidate fanout closed — natural fit for a verifier whose job is to read each finished spec. But Phase-7's bias-guards have a different job: produce an *independent* cross-spec read against the archive, deliberately uncorrelated with the per-candidate subagents' classifications. The Phase-7 silent-absorption auditor's purpose is to surface absorptions the per-candidate subagents missed; the historian's purpose is to surface gaps that appear in zero specs. Neither needs the per-candidate outputs as input.

The auto-007 brief's design choice was to fire bias-guards CONCURRENT with the per-candidate fanout (in the same wave, not in a serial successor wave), and then reconcile any disagreements at lead-agent aggregation via a precedence rule with a confidence threshold. This saves a full fanout's wall-clock and preserves the independence of the bias-guards' read.

## Decision

In any parallel-fanout pattern where the bias-guard / audit subagent's input stream is genuinely independent of the per-candidate workers' outputs (i.e., the auditor reads the shared corpus, not the per-candidate work products), the bias-guards SHALL fire in the same wave as the per-candidate workers — not in a serial successor wave — and disagreements SHALL be reconciled at lead-agent aggregation via a precedence rule with confidence labels.

## Alternatives considered

- **Bias-guards fire serially AFTER the per-candidate fanout** (the Phase-6 Wave-6.5 pattern). Rejected because (a) wall-clock cost is ~one fanout duration for no quality benefit; (b) the auditor would be tempted to read per-candidate outputs and lose the independent-read property — exactly the failure mode the bias-guard exists to mitigate; (c) the silent-absorption auditor's job is specifically to find what per-candidate subagents missed, which is harder if the auditor has seen the per-candidate outputs first.
- **Bias-guards fire BEFORE the per-candidate fanout.** Rejected because the bias-guard's value depends on having a corpus to compare against. With nothing yet produced by per-candidate workers, the silent-absorption auditor has nothing to compare; only the historian's job (zero-spec-gaps) is technically possible, and even that is better timed concurrent with the per-candidate read so the historian's findings can be reconciled against the per-candidate verdicts immediately.
- **Skip the bias-guards entirely** (rely on per-candidate workers + aggregation only). Rejected because Phase 6's verifier surfaced 2 cross-spec findings that no per-candidate worker found; Phase-7 silent-absorption auditor surfaced 15 findings of which 3 high-confidence required Phase-8 cite obligations. The bias-guards earn their cost.
- **Sub-fan the bias-guards by archive file** (one subagent per archive file instead of one auditor reading all 9). Rejected because the silent-absorption and historian roles BOTH depend on cross-file pattern detection — "this archive item appears in zero specs in any form" requires holding all 9 archive files in one head. Sub-fanning would lose the load-bearing property.

## Consequences

What becomes easier:
- Wall-clock. Phase-7 saved roughly one fanout duration by running bias-guards concurrent — the wave completed in ~13 minutes instead of ~25.
- Bias-guard independence. The silent-absorption auditor literally cannot inherit per-candidate verdicts because they don't exist yet at dispatch time. This is structurally enforced.
- Aggregation discipline. The lead agent must do real reconciliation work (compare per-candidate verdicts against bias-guard findings), which is exactly the discipline the precedence rule + confidence threshold codifies.

What becomes harder:
- Aggregation work is now load-bearing. The lead agent at fanout-close must compare two independent readings of overlapping content. A precedence rule + confidence threshold is required — see the sibling [silent-absorption-precedence-with-confidence](./SKILL-SPEC-3c5b9e8f47-silent-absorption-precedence-with-confidence.md) skill spec.
- Harness load. 11 concurrent subagents (9 workers + 2 bias-guards) is at the upper end of the practical wave-size limit. Phase-7 ran cleanly but ~15 is the documented ceiling.

Trade-off accepted: parallelism + independence-of-read at the cost of more aggregation work. Worth it because the bias-guards' independent read is the actual product — sequential firing would undermine the audit's purpose.

## References

- [`../2026-05-27-191.md`](../2026-05-27-191.md) — the source retrospective.
- [`./ADR-b4e7c2a9d6-matrix-flag-over-spec-patches.md`](./ADR-b4e7c2a9d6-matrix-flag-over-spec-patches.md) — sibling ADR; the matrix-flag decision that becomes possible because the bias-guard findings landed at aggregation time, not after.
- [`./SKILL-SPEC-6a3f1b2c8d-per-candidate-back-fill-audit-fanout.md`](./SKILL-SPEC-6a3f1b2c8d-per-candidate-back-fill-audit-fanout.md) — the fanout skill; describes the wave shape this ADR formalizes.
- [`./SKILL-SPEC-3c5b9e8f47-silent-absorption-precedence-with-confidence.md`](./SKILL-SPEC-3c5b9e8f47-silent-absorption-precedence-with-confidence.md) — the reconciliation precedence rule this ADR depends on.
- Source brief: [`architectures/v3/decisions/auto-007-phase-7-dispatch-shape.md` §Decision (Round 2)](../../architectures/v3/decisions/auto-007-phase-7-dispatch-shape.md#decision-round-2).
- PRs the decision was made in: #188 (auto-007 brief), #190 (fanout omnibus where the wave actually ran).
