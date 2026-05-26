# ADR 4b8d29a715: Omnibus PR over sub-wave PRs when files are disjoint

## Status
Proposed (retrospective draft from 2026-05-26 Phase-6 run).

## Context

Briefs for multi-sub-wave parallel-fanout dispatch typically plan N sub-wave PRs (one per cluster) to keep per-cluster review boundaries clean and isolate blast radius. auto-006 Round 2 committed to 4 sub-wave PRs for Phase 6: Wave 6.1 GF (3 specs), Wave 6.2 BF (3 specs), Wave 6.3a U-mid (2 specs), Wave 6.3b U-heavy (D7-U-1 isolated).

At Phase-6 delivery time, all 9 sibling spec files landed on the same parent branch (`claude/phase-6-architecture-specs-NHmM3`) because the dispatch happened in one Agent-tool batch and each subagent wrote a disjoint file (`specs/<id>.md`). The 4-sub-wave PR pattern would have required: (a) creating 4 sub-wave branches; (b) cherry-picking or moving each subagent's commit to the right branch; (c) opening 4 PRs; (d) sequencing the merges. The shared parent branch + disjoint files made all of this overhead with zero review-quality benefit.

Compounding factor: PR #183 was already open (carrying the U-C exemplar) on the parent branch. The webhook-false-positive meant the omnibus accumulated naturally onto PR #183.

## Decision

**When a brief's N planned sub-wave PRs share a parent branch and write disjoint files, the lead agent SHALL consolidate to 1 omnibus PR at delivery time** if all three conditions hold (per [AGENTS-MD-d71e845b29](AGENTS-MD-d71e845b29-sub-wave-pr-consolidation-when-files-are-disjoint.md)):

1. Disjoint files invariant (no spec overlap).
2. Cluster rationale survives in the omnibus PR description (per-cluster sections preserved).
3. Blocking-isolation preserved (a failing spec is re-authorable without affecting siblings).

The consolidation MUST be explicitly acknowledged in: (a) the omnibus PR body's "Sub-wave PR consolidation deviation" section; (b) the run's morning summary; (c) the session handoff.

## Alternatives considered

**A. Honor the brief mechanically.** Open 4 sub-wave PRs as planned. Rejected: burns 3 extra PRs against the ≤15 cap; adds 4 branches + 4 PRs of management overhead for zero review-quality gain.

**B. Pivot silently (omnibus PR without acknowledgement).** Rejected: breaks audit trail. A future reader of the brief + the actual PR-history would not understand the divergence.

**C. Open a new "decision-deviation" PR ahead of the omnibus.** Rejected: adds 1 PR back. The deviation acknowledgement inside the omnibus PR body is sufficient.

## Consequences

**Easier.** PR-cap math relaxes. Single PR is easier to review as one coherent unit (per-cluster sections still navigable via the PR body's table of contents). Branch management simplified.

**Harder.** The deviation-acknowledgement discipline is non-trivial — must appear in 3 places (PR body, morning summary, handoff). The omnibus PR body is necessarily longer because it covers per-cluster context. A failing spec is still isolatable for re-author (the consolidation doesn't bundle work; the 9 specs are independent files), but the omnibus PR can't merge until any failing spec is fixed — a small coupling risk.

**Cost of misuse.** If condition (a) is violated (specs overlap), the omnibus has merge conflicts and the consolidation collapses. If (c) is violated (blocking + non-blocking bundled), re-author requires re-landing the whole omnibus. The skill spec `sub-wave-pr-consolidation-decision-rule` enforces all three conditions.

## References

- [AGENTS-MD-d71e845b29 — sub-wave PR consolidation when files are disjoint](AGENTS-MD-d71e845b29-sub-wave-pr-consolidation-when-files-are-disjoint.md) — the universal trigger rule.
- [SKILL-SPEC-9e5b2a814f — sub-wave-pr-consolidation-decision-rule](SKILL-SPEC-9e5b2a814f-sub-wave-pr-consolidation-decision-rule.md) — the procedure.
- [auto-006 Round 2](../../architectures/v3/decisions/auto-006-phase-6-dispatch-shape.md) — the brief that planned 4 sub-wave PRs.
- [Phase-6 omnibus PR #183](https://github.com/lago-morph/software-factory/pull/183) — the actual consolidated delivery.
- [Phase-6-close session handoff](../../architectures/v3/SESSION-HANDOFF-2026-05-26-phase-6-close.md) — the handoff's "Honest acknowledgements" section.
