# ADR: Dual-track per-component v4 spec/plan layout with a _meta decision ledger

- **ID**: ADR-1832596c21
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-30
- **Source retrospective**: ../2026-05-30-214.md
- **PRs covered**: #213, #214

## Context

The task was to produce an "incredibly detailed" spec and plan for every piece of the `architectures/v4` design, exploiting parallelism to the maximum, with both a faithful elaboration and a ruthlessly optimized one. Two structural problems had to be solved before any content was written: (1) how to lay out a 57-component, two-track corpus so dozens of independent subagents can each own a file without collision and a human can still navigate it, and (2) how to keep that corpus internally consistent when its authors are parallel agents that never share context. Early in the run, independent builders produced four different identity namespaces and two conflicting "who owns the bead schema" answers — concrete evidence that an unmanaged parallel corpus drifts.

## Decision

Organize the v4 spec and plan as per-component documents under `spec-/plan-{faithful,optimized}/` with a `_meta/` directory holding the canonical component inventory, standing builder/adversary briefs, and an adopted-decision `review-log.md`; cross-component conflicts are resolved as numbered decisions in that ledger and applied across the corpus by a dedicated integrator pass.

## Alternatives considered

- **Single monolithic spec document.** Rejected: cannot be authored by parallel subagents (one writer, constant merge conflicts), and exceeds any reviewable size.
- **One track only (just optimized, or just faithful).** Rejected: the user explicitly wanted both a fixed-proof baseline and an improved design; a single track loses either the fidelity baseline or the improvement, and loses the diffability that makes "what changed and why" answerable.
- **Per-component docs but no `_meta` ledger.** Rejected: this is exactly what produced the four-namespace / two-owner drift; without a shared decision record, parallel agents cannot converge.
- **Folder-per-component (all four docs in one dir).** Rejected in favor of track-first roots so each track diffs as a unit and faithful/optimized stay cleanly separated.

## Consequences

- **Easier:** massive parallel authoring (distinct paths, no races); component-by-component diffing across tracks (shared IDs); cold-session resume (the `_meta/` backbone + handoff stand alone); consistent cross-cutting decisions (ledger + integrator).
- **Harder:** more files to manage and commit; the ledger and integrator passes are extra machinery that only pays off above ~15 components; the dual track roughly doubles authoring cost, justified only when both fidelity and improvement are wanted.
- **Accepted trade-off:** spend the overhead of a `_meta/` control plane and a second track to buy parallelism, diffability, and consistency at corpus scale.

## References

- [`../2026-05-30-214.md`](../2026-05-30-214.md) — the source retrospective.
- [`./SKILL-SPEC-3fb4e487e9-disk-fanout-orchestration.md`](./SKILL-SPEC-3fb4e487e9-disk-fanout-orchestration.md) — the orchestration pattern this layout enables.
- [`./SKILL-SPEC-05de808d79-dual-track-spec-elaboration.md`](./SKILL-SPEC-05de808d79-dual-track-spec-elaboration.md) — the dual-track method.
- PRs the decision was made in: #213, #214.
