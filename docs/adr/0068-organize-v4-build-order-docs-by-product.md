# ADR 0068: Organize v4 build-order documentation by adopted product, not by dependency phase

- **Status**: Accepted
- **Date**: 2026-06-01
- **Deciders**: 2026-06-01 v4 implementation-dependencies restructure (canonical ID `ADR-6b1c1235d5`, drafted at [`retrospective/2026-06-01-227/`](../../retrospective/2026-06-01-227/))

## Context

The v4 implementation build-order document, [`architectures/v4/implementation-dependencies.md`](../../architectures/v4/implementation-dependencies.md), originally ordered the 57 components into ten dependency phases (build-waves). A later pass observed that most of the substrate is off-the-shelf software — one Gas City install brings up eleven backbone components at once — and began clustering by product, but layered that view on top of the still-intact phase structure. The result was incoherent: a single product's components were scattered across phases 1, 2, and 3, so the phase organization actively *hid* the natural clustering the build actually has.

The operator's instruction was to make "the software products being installed a first-class organization, not the prior phase organization." This is a binding documentation-architecture choice, not a tactical edit: it governs how this document is structured, how its sibling human-facing docs ([`build-order-plain-english.md`](../../build-order-plain-english.md), [`architecture-guide-for-engineers.md`](../../architecture-guide-for-engineers.md)) frame the same material, and how future editors add a component (by assigning it to a product, not by inventing a phase slot).

## Decision

v4 implementation build-order documentation is organized with the adopted or built **product** as the first-class unit — external off-the-shelf adoptions and internal custom build-test-integrate units — rather than by dependency phase or wave.

A *product* is the thing you build, test, and integrate as a whole: either an **external** product you adopt and configure (Gas City, Claude Code, CXDB, Inspect AI, OpenTelemetry+LangFuse, PyOD/HDBSCAN, MLflow/Aim, DSPy/Unleash/scipy, …) or an **internal** custom product — a cohesive cluster of original engineering, sometimes a single component (spec intake, bead-type schema, the fence, bootstrap, self-heal, self-optimization, governance docs). Every per-component dependency edge from the [component inventory](../../architectures/v4/_meta/component-inventory.md) is preserved, but expressed *within and across products* (a "Build order across products" section) rather than as phase-waves. The inventory remains the source of truth for edges; the product organization is the presentation layer over it.

## Alternatives considered

**A. Keep the ten-phase organization (status quo ante).** Rejected: it scatters one product's components across phases and obscures that adopting a single binary discharges roughly fifteen "components" at once — the exact insight the operator wanted foregrounded.

**B. Keep both views in one document** (products on top, phases below as a reference appendix). This was put to the operator as an explicit option; the operator chose "fold into products" — dissolve the phase framing entirely. Rejected because two competing organizing structures in one document is precisely the incoherence this change set out to remove.

**C. Organize by capability milestone** (foundations → human-driven → unattended → self-heal → self-optimize → bootstrap). Rejected for this document: that axis already belongs to [`build-order-plain-english.md`](../../build-order-plain-english.md); duplicating it here would re-create the two-axis problem. The implementer document's distinct value is the product/dependency view.

## Consequences

**Easier.** A reader sees at a glance that ~15 components are one Gas City install and that real cost lives in a small set of custom products; adding a component means assigning it to a product, not inventing a phase; the document matches how work is actually staffed (one workstream per product).

**Harder / accepted trade-offs.** Dependency ordering and parallelism must be re-expressed across products rather than read off phase tables — a "Build order across products" section carries it, and a critical-path diagram preserves the depth/width facts. A component can occasionally belong to two products (in practice only C46, split between an adopted tracking store and custom definitions); this must be flagged as a sanctioned exception to the one-component-one-product partition.

**Scope limit.** This decision governs the v4 build-order documentation. Sibling docs should be aligned to the same convention over time to avoid cross-doc drift, but this ADR does not itself rewrite them.

## References

- [`../../retrospective/2026-06-01-227.md`](../../retrospective/2026-06-01-227.md) — the source retrospective.
- [Retrospective draft `ADR-6b1c1235d5`](../../retrospective/2026-06-01-227/ADR-6b1c1235d5-organize-v4-build-order-docs-by-product.md) — the original retro-draft this ADR adopts.
- [`paradigm-shift-reconciliation` skill spec](../../retrospective/2026-06-01-227/SKILL-SPEC-c207874125-paradigm-shift-reconciliation.md) — the reconciliation pattern that applied this decision.
- [`architectures/v4/implementation-dependencies.md`](../../architectures/v4/implementation-dependencies.md) — the document this decision governs.
- [ADR-0067: Dual-track per-component v4 spec/plan layout](./0067-dual-track-per-component-v4-layout.md) — the sibling v4 documentation-layout decision.
- PR the decision was made in: #227.
