# ADR 0067: Dual-track per-component v4 spec/plan layout with a _meta decision ledger

- **Status**: Accepted
- **Date**: 2026-05-30
- **Deciders**: 2026-05-30 v4 spec/plan retrospective (canonical ID `ADR-1832596c21`, drafted at [`retrospective/2026-05-30-214/`](../../retrospective/2026-05-30-214/))

## Context

The task was to produce an "incredibly detailed" spec and plan for every piece of the [`architectures/v4`](../../architectures/v4/) design, exploiting parallelism to the maximum, in both a faithful elaboration and a ruthlessly optimized one. Two structural problems had to be solved before any content was written: (1) how to lay out a 57-component, two-track corpus so dozens of independent subagents can each own a file without collision and a human can still navigate it, and (2) how to keep that corpus internally consistent when its authors are parallel agents that never share context.

Early in the run the second problem materialized concretely: independent builders produced **four** different reverse-DNS identity namespaces for the same identity space, and **two** conflicting answers to "which component authors the bead schema." This was direct evidence that an unmanaged parallel corpus drifts and needs a control plane, not just a directory of files.

## Decision

Organize the v4 spec and plan as per-component documents under `spec-/plan-{faithful,optimized}/` with a `_meta/` directory holding the canonical component inventory, standing builder/adversary briefs, and an adopted-decision `review-log.md`; cross-component conflicts are resolved as numbered decisions in that ledger and applied across the corpus by a dedicated integrator pass.

Concretely, the tree is:

```
architectures/v4/
  _meta/            inventory, charters, templates, briefs, review-log (ledger),
                    integration reports, status + handoff
  spec-faithful/    <ID>-<slug>.md  (+ .review.md siblings)
  plan-faithful/    <ID>-<slug>.md
  spec-optimized/   <ID>-<slug>.md  (+ .review.md siblings)
  plan-optimized/   <ID>-<slug>.md
```

Both tracks key off the **same** canonical component IDs, so any component diffs faithful-vs-optimized cleanly.

## Alternatives considered

**A. Single monolithic spec document.** Rejected: cannot be authored by parallel subagents (one writer, constant merge conflicts) and exceeds any reviewable size.

**B. One track only (just optimized, or just faithful).** Rejected: the user explicitly wanted both a fixed-proof baseline and an improved design; a single track loses either the fidelity baseline or the improvement, and loses the diffability that makes "what changed and why" answerable component-by-component.

**C. Per-component docs but no `_meta` ledger.** Rejected: this is exactly the shape that produced the four-namespace / two-owner drift. Without a shared decision record, parallel agents cannot converge and the corpus silently becomes inconsistent.

**D. Folder-per-component (all four docs in one directory).** Rejected in favor of track-first roots so each track diffs as a unit and faithful/optimized stay cleanly separated.

## Consequences

**Easier.** Massive parallel authoring (distinct paths, no write races); component-by-component diffing across tracks (shared IDs); cold-session resume (the `_meta/` backbone + handoff stand alone); consistent cross-cutting decisions (ledger + integrator pass).

**Harder.** More files to manage and commit; the ledger and integrator passes are extra machinery that only pays off above ~15 components; the dual track roughly doubles authoring cost, justified only when both fidelity and improvement are genuinely wanted.

**Cost of misuse.** Below ~15 components the control-plane overhead exceeds its benefit — use a single doc or a one-shot fan-out instead. If the ledger/integrator step is skipped, the parallel corpus drifts (the failure this decision exists to prevent).

## References

- [`../../retrospective/2026-05-30-214.md`](../../retrospective/2026-05-30-214.md) — the source retrospective.
- [Retrospective draft `ADR-1832596c21`](../../retrospective/2026-05-30-214/ADR-1832596c21-dual-track-per-component-v4-layout.md) — original retro-draft this ADR adopts.
- [`disk-fanout-orchestration` skill](../../.claude/skills/disk-fanout-orchestration/SKILL.md) — the orchestration pattern this layout enables.
- [`cross-component-decision-ledger` skill](../../.claude/skills/cross-component-decision-ledger/SKILL.md) — the consistency mechanism (`_meta/review-log.md` + integrator pass).
- [`architectures/v4/_meta/`](../../architectures/v4/_meta/) — the live control plane this decision describes.
- PRs the decision was made in: #213, #214.
