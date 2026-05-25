# ADR: Substrate primitive buildability requirement

- **ID**: ADR-a34b0b8636
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-25
- **Source retrospective**: ../2026-05-25-132.md
- **PRs covered**: #132

## Context

The v3 substrate-track Phase-2 agents (greenfield-substrate-first, brownfield-substrate-first, brownfield-legacy-ingestion-first) named substrate primitives at the **contract level** — what role each primitive plays, what API surface it exposes, what discipline it enforces — but did not produce *construction paths*. The clearest example is `CodebaseModel` (brownfield-side queryable artifact with five sub-stores: symbol index, dependency-and-impact graph, runtime/telemetry view with role-based partitioning, change-history-with-symbol-level-attribution, invariant/debt view). The tracks named the contract; they did not say "use tree-sitter + Glean-style indexed-data store + OpenTelemetry collectors with per-role filters."

The user identified this as handwaving: "Just assume `CodebaseModel` exists" is not enough. A substrate primitive that the architecture *requires* but that has no plausible construction path is a request for someone-else-to-figure-it-out, not an architectural decision. This is especially acute for primitives that are themselves active areas of academic and commercial research (which CodebaseModel-class artifacts are): they cannot be assumed available.

The original methodology routed construction-path work to Phase 5 (ADRs, "Alternatives considered") and Phase 6 (architecture specs). That is too late for the buildability filter — by Phase 5/6, the architecture has already committed to primitives that may or may not be buildable.

## Decision

**A substrate primitive can enter an architecture proposal only if it ships with (a) a construction path — existing tools, named techniques, prior-art references; research-grade-uncertainty flag if no plausible path is known — and (b) a corpus-why citation linking the primitive to a problem the corpus has identified. "Assume X exists" is rejected as handwaving.**

The methodology introduces **Phase 3.5 (buildability addendum per candidate)** between Phase 3.4 (decisions) and Phase 4 (substrate-requirements extraction). For each surviving candidate, the lead agent (or a buildability-persona subagent) enumerates the candidate's required substrate primitives and produces a buildability sketch per the two-part rule above. Primitives lacking sketches are demoted to placeholders pending defense; the candidate may still carry forward, but cannot proceed to Phase 5/6 until the sketches land.

**Methodology-to-substrate matching is deferred** to the later combination stage (Phase 4+). Orphan primitives — those no current candidate methodology claims — are deliberately preserved in the catalog as cross-pollination fuel. The justification and construction path may stimulate reviewers to recognise the primitive's relevance to alternatives proposers hadn't considered.

## Alternatives considered

- **Defer all construction-path work to Phase 5 ADRs.** Rejected as the status-quo problem: by Phase 5, architectures have already committed to primitives whose buildability is unknown.
- **Require methodology-attestation alongside buildability and corpus-why (3-part rule).** Rejected per user direction: methodology-to-substrate matching belongs at the later combination stage; requiring it at Phase 3.5 eliminates orphans that could later prove load-bearing in unanticipated ways.
- **Apply the rule only to designed-system primitives, not commodity ones.** Rejected because the commodity-vs-designed distinction is not robust (cross-family judge routing looks commodity but is methodology-load-bearing); applying the rule uniformly is cleaner than introducing a fuzzy threshold.

## Consequences

**Easier.** Phase 4 substrate-requirements extraction consumes only primitives with construction paths; Phase 5 ADRs refine paths rather than first-author them; the buildability bar surfaces research-grade primitives explicitly (rather than hiding them in optimistic architecture descriptions). The Phase-3.2 critique pass's missing "builder/implementer" persona is addressed structurally (Phase 3.5 is the placeholder for that work).

**Harder.** Substrate-track Phase-2 agents must now produce more material per primitive (Phase 3.5 work upstream-loaded). Some primitives that look architecturally compelling will be flagged research-grade, which constrains the architecture's risk profile in ways that may surprise the proposer.

**Accepted trade-off.** More upfront work in exchange for a Phase-4-onward pipeline that operates over buildable primitives. The cost is bounded (Phase 3.5 buildability sketches are ~400-800 words per primitive); the cost of skipping is potentially Phase-6 architecture specs that propose unbuildable systems.

## References

- [`../2026-05-25-132.md`](../2026-05-25-132.md) — source retrospective.
- [`./ADR-405ef4e4d3-working-definitions-architecture-substrate-methodology.md`](./ADR-405ef4e4d3-working-definitions-architecture-substrate-methodology.md) — the working definitions of architecture / substrate / methodology that the buildability rule depends on.
- [`./ADR-0550adf359-scoping-principle-carry-all-defensible-candidates.md`](./ADR-0550adf359-scoping-principle-carry-all-defensible-candidates.md) — the scoping principle; buildability is one of the three carry-forward criteria.
- PRs the decision was made in: #132.
