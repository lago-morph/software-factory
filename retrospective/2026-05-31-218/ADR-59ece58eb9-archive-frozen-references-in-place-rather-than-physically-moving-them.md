# ADR: Archive frozen references in place rather than physically moving them

- **ID**: ADR-59ece58eb9
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-31
- **Source retrospective**: ../2026-05-31-218.md
- **PRs covered**: #218

## Context

During the v4 single-track convergence (companion ADR `ADR-79f2bd2f4d`), the canonical instinct for the divergent track was to relocate `spec-optimized/` and `plan-optimized/` under a dedicated archive path — e.g., `architectures/v4/_meta/optimized-reference/`. The proposed move would have made the filesystem layout self-documenting: the active track lives at `spec/`, frozen references live under `_meta/`.

A pre-move audit revealed the cost: the two optimized directories together contained ~46 markdown files with relative links to the canonical track (`../spec/CXX-…md`) and to each other. After a move, every one of those relative links would change depth by one level. Inbound references compounded the cost: ~20 canonical specs cite specific `spec-optimized/<C>` siblings as cross-track provenance ("see the optimized track's alternative framing for this decision"), and several `_meta` artifacts (STATUS, HANDOFF, the three research files in `_meta/research/`) reference the optimized paths. A move would require rewriting every relative link in the moved files plus every inbound reference — a mechanically error-prone churn for a cosmetic benefit.

The operator had also explicitly weighted "don't break things" and minimal-edit discipline through the session. The cost/benefit was clear: moving costs structural-correctness risk for cosmetic clarity, and the cosmetic benefit can be obtained more cheaply.

## Decision

When converting an exploratory artifact directory to frozen reference, mark it frozen via a `README.md` at its root pointing at the canonical artifact, rather than physically relocating it under a dedicated archive path.

## Alternatives considered

**Physical relocation to a dedicated archive path** (e.g., `_meta/optimized-reference/`). Most aesthetically self-documenting. Rejected because: ~46 files would need their relative links rewritten depth-by-one, plus ~20 inbound references across the canonical track and `_meta/` would need updating — high mechanical risk for cosmetic benefit.

**Soft-delete via `.gitignore` + retain in working tree only.** Rejected because the deferred architectural bets (FE-1..FE-4) need to be discoverable by a future session that wants to revive any of them; soft-delete erases that discoverability.

**Rename the directory to `spec-optimized-FROZEN/` etc.** Rejected because the name change still forces all inbound references to be rewritten, just under a different new name — no cost savings vs. the physical move.

**Wrap the archive paths in a top-level `archive/` symlink.** Rejected because symlinks complicate git on Windows and add a maintenance surface that doesn't pay for itself.

## Consequences

**Easier:**
- Zero file moves; zero relative-link rewrites in the archived directories.
- Zero inbound-reference rewrites in the canonical track or `_meta/`.
- Cross-track provenance links in canonical specs continue to work without modification.
- The `README.md` at each archived directory's root is a small, atomic addition that's easy to write and easy to verify.
- The freeze can be reversed (e.g., to revive an FE-N) by deleting the README and updating tracking docs — no inverse-rewriting required.

**Harder:**
- Filesystem layout retains an apparently-equal-status sibling directory (`spec-optimized/` sits next to `spec/`). A fresh reader might miss that one is canonical and one is frozen.
- Mitigation requires multiple breadcrumbs: README at the archived root, convergence banner in HANDOFF, convergence banner in STATUS, banners on the standing briefs.

**Knowingly accepted trade-off:**
- Cosmetic clarity ("all archives live in one place under `_meta/`") is sacrificed for structural-correctness preservation. The mitigation is breadcrumb redundancy: a new reader hitting `spec-optimized/` will immediately see the `README.md` banner explaining the freeze; a new reader hitting `HANDOFF.md` will see the convergence banner; a new reader hitting `STATUS.md` will see the converged-state header. Three independent breadcrumbs make the freeze hard to miss.

## References

- [`../2026-05-31-218.md`](../2026-05-31-218.md) — the source retrospective.
- [`./ADR-79f2bd2f4d-adopt-single-canonical-track-for-v4-spec-plan-run.md`](./ADR-79f2bd2f4d-adopt-single-canonical-track-for-v4-spec-plan-run.md) — the companion convergence decision.
- PR the decision was made in: #218.
- Concrete realization: `architectures/v4/spec-optimized/README.md` and `architectures/v4/plan-optimized/README.md` (the frozen-reference banners).
