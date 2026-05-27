# ADR: Bias-guards-concurrent with per-candidate fanout when input streams independent

- **ID**: ADR-3f8c1e5b7a
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-27
- **Source retrospective**: ../2026-05-27-191.md
- **PRs covered**: #188, #190

## Context

Phase-7 auto-007 Round 1 had to decide the firing order for two distinct subagent classes: (a) **per-candidate back-fill subagents** (9 of them; each reads its candidate's spec + the 9 archive files) and (b) **bias-guard / fresh-context audit subagents** (2 of them: silent-absorption auditor reads all 10 Phase-6 specs + 9 archive files; historian reads the same input set plus the Phase-6-close handoff). The naive sequencing would have been: fanout first → bias-guards second, so that the bias-guards could read per-candidate outputs as inputs. But empirical examination of the bias-guards' mandates showed they read NONE of the per-candidate fanout outputs — both auditors operate on the same shared input set as the per-candidate subagents (specs + archive), just from a cross-cutting rather than per-candidate read angle.

Concretely, the silent-absorption auditor asks "what's in candidate X's spec that came from archive file Y without a cite?" — this only requires the specs and the archive, not the per-candidate back-fill notes. The historian audits "what archive material is silently inherited across multiple candidates?" — same input set. The per-candidate back-fill subagents ask the inverse: "what's in archive file Y that candidate X carries (with or without cite)?" — they read the candidate's spec + the archive but produce a per-candidate notes file as output.

Because all inputs are read-only and disjoint from any of the fanout outputs, both subagent classes can fire **concurrent** rather than sequenced. This saves a full fanout wall-clock — the Phase-7 silent-absorption auditor ran 411 seconds (the longest of the 11 subagents); a sequenced design would have added the bias-guards' wall-clock on top of the per-candidate fanout's wall-clock. The concurrent design returned all 11 outputs in the same ~13-minute window.

The trade-off that emerges with the concurrent design: at lead-agent aggregation, the bias-guard findings can disagree with per-candidate verdicts on overlapping cells. That disagreement requires an adjudication rule. The companion ADR-b4e7c2a9d6 governs the matrix-flag-vs-patch consequence of those findings; the confidence-threshold rule (skill SKILL-SPEC-3c5b9e8f47) governs which findings actually override per-candidate verdicts.

## Decision

Bias-guard / fresh-context audit subagents fire **concurrent** with the per-candidate fanout (in the same parallel wave), NOT after, when their input streams are demonstrably independent of the fanout outputs — meaning the auditors read only artifacts that exist before either subagent class fires (specs, archive, prior handoffs), and produce findings against those artifacts directly.

The disagreement-at-aggregation surface that concurrent firing creates is adjudicated at lead-agent aggregation via the silent-absorption-precedence-with-confidence rule, NOT by re-firing the bias-guards after the fanout completes.

## Alternatives considered

- **Bias-guards AFTER fanout (sequenced).** Rejected: wastes the bias-guards' wall-clock (411 seconds for the silent-absorption auditor in Phase 7) by adding it on top of the per-candidate fanout wall-clock, when there is no input dependency that requires the sequencing. The "we want the bias-guards to read the fanout outputs" rationale falls away once you examine the actual bias-guard mandates — they read the same shared input set as the fanout, not the fanout's outputs.
- **Bias-guards BEFORE fanout.** Rejected: the bias-guards' findings are most useful at aggregation time where the per-candidate verdicts already exist to be reconciled against. Running bias-guards first means their findings have nothing concrete to compare against beyond what's already in the specs (which the lead agent has already read when authoring the brief).
- **Multiple bias-guard rounds bracketing the fanout.** Rejected: doubles the audit cost without materially improving finding quality; the single-pass-concurrent design already captures the cross-cutting findings the auditors are dispatched to find.
- **Inline-simulated bias-guards (no real subagent).** Rejected on independent grounds per `AGENTS-MD-d72e1a4f3c` — inline-simulated reviewers inherit lead-agent anchoring. The bias-guards must be real subagents either way; the only question is when they fire.

## Consequences

**Easier.** Wall-clock saving — Phase 7 returned 11 outputs in ~13 minutes instead of the ~20 minutes a sequenced design would have taken. The omnibus PR (per `AGENTS-MD-d71e845b29`) is straightforward because all 11 outputs land in the same wave and can be consolidated cleanly. The lead-agent context is held only once for both subagent classes' dispatch, not twice.

**Harder.** Aggregation-time reconciliation MUST adjudicate disagreements between bias-guard findings and per-candidate verdicts. This requires the silent-absorption-precedence-with-confidence rule (SKILL-SPEC-3c5b9e8f47) to be in place — without the confidence threshold, the lead agent has no principled way to decide whether a bias-guard finding overrides a per-candidate `rejected` verdict or vice versa. The two rules are tightly coupled: concurrent firing creates the disagreement surface; the precedence rule resolves it.

**Trade-off accepted.** Concurrent firing pushes complexity from sequencing (compile-time-equivalent) to aggregation (runtime-equivalent). We accept that the aggregation phase carries an explicit reconciliation step in exchange for the wall-clock saving and the simpler one-wave dispatch.

## References

- [`../2026-05-27-191.md`](../2026-05-27-191.md) — the source retrospective (see Phase 5 — Wave 7.1 + 7.2 fanout).
- [`./SKILL-SPEC-6a3f1b2c8d-per-candidate-back-fill-audit-fanout.md`](./SKILL-SPEC-6a3f1b2c8d-per-candidate-back-fill-audit-fanout.md) — the per-candidate fanout skill that the bias-guards run concurrent with.
- [`./SKILL-SPEC-3c5b9e8f47-silent-absorption-precedence-with-confidence.md`](./SKILL-SPEC-3c5b9e8f47-silent-absorption-precedence-with-confidence.md) — the precedence rule that resolves the disagreement surface concurrent firing creates.
- [`./ADR-b4e7c2a9d6-matrix-flag-over-spec-patches.md`](./ADR-b4e7c2a9d6-matrix-flag-over-spec-patches.md) — the companion ADR on how to act on the auditor's findings at aggregation time.
- [`../../architectures/v3/decisions/auto-007-phase-7-dispatch-shape.md`](../../architectures/v3/decisions/auto-007-phase-7-dispatch-shape.md) — the brief that adopted the bias-guards-concurrent shape in Round 1 (preserved through Round 2).
- [`../../architectures/v3/backfill-notes/audit-silent-absorption.md`](../../architectures/v3/backfill-notes/audit-silent-absorption.md) — the silent-absorption auditor's output, produced concurrent with the per-candidate fanout.
- PRs the decision was made in: #188 (auto-007 brief), #190 (omnibus fanout PR carrying both subagent classes' outputs).
