# ADR: Organize v4 build-order documentation by adopted product, not by dependency phase

- **ID**: ADR-6b1c1235d5
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-06-01
- **Source retrospective**: ../2026-06-01-227.md
- **PRs covered**: #227

## Context

The v4 implementation build-order document (`architectures/v4/implementation-dependencies.md`) originally ordered the 57 components into ten dependency phases (build-waves). A later pass observed that most of the substrate is off-the-shelf software — one Gas City install "lights up" eleven backbone components at once — and began clustering by product, but layered that view on top of the still-intact phase structure. The result was incoherent: a single product's components were scattered across Phases 1, 2, and 3, so the phase organization actively *hid* the natural clustering. The operator's instruction was to make "the software products being installed a first-class organization, not the prior phase organization."

This is a binding documentation-architecture choice, not a tactical edit: it affects how `implementation-dependencies.md` is structured, how its sibling human-facing docs ([`build-order-plain-english.md`](../../build-order-plain-english.md), [`architecture-guide-for-engineers.md`](../../architecture-guide-for-engineers.md)) should frame the same material, and how future editors add components (by product, not by inventing a phase slot).

## Decision

v4 implementation build-order documentation is organized with the adopted or built **product** as the first-class unit — external off-the-shelf adoptions and internal custom build-test-integrate units — rather than by dependency phase or wave.

A *product* is the thing you build, test, and integrate as a whole: either an **external** product you adopt and configure (Gas City, Claude Code, CXDB, Inspect AI, OTel+LangFuse, PyOD/HDBSCAN, MLflow/Aim, DSPy/Unleash/scipy, …) or an **internal** custom product — a cohesive cluster of original engineering, sometimes a single component (spec intake, bead-type schema, the fence, bootstrap, self-heal, self-optimization, governance docs). Every per-component dependency edge from the component inventory is preserved, but expressed *within and across products* (a "Build order across products" section) rather than as phase-waves. The dependency inventory remains the source of truth for edges; the product organization is the presentation layer over it.

## Alternatives considered

- **Keep the ten-phase organization (status quo ante).** Rejected: it scatters one product's components across phases and obscures that adopting a single binary discharges a dozen "components" at once — the exact insight the operator wanted foregrounded.
- **Keep both views in one doc (products on top, phases below as a reference).** This was offered to the operator as an option ("products first, phases as appendix"); the operator chose "fold into products" — dissolve the phase framing entirely. Rejected because two competing organizing structures in one document is the incoherence this change set out to remove.
- **Organize by capability milestone** (foundations → human-driven → unattended → self-heal → self-optimize → bootstrap). Rejected for this doc: that axis already belongs to the plain-English build-order doc; duplicating it here would re-create the two-axis problem. The implementer doc's value is the product/dependency view.

## Consequences

- **Easier:** a reader sees at a glance that ~15 components are one Gas City install and that real cost lives in a small set of custom products; adding a component means assigning it to a product, not inventing a phase; the doc matches how work is actually staffed (one workstream per product).
- **Harder / accepted trade-offs:** dependency ordering and parallelism must be re-expressed across products rather than read off phase tables — a "Build order across products" section carries it, and a critical-path diagram preserves the depth/width facts. A component can plausibly belong to two products (only C46, split between an adopted tracking store and custom definitions, in practice); this must be flagged as a sanctioned exception to the one-component-one-product partition. Sibling docs should be aligned to the same convention over time to avoid cross-doc drift.

## References

- [`../2026-06-01-227.md`](../2026-06-01-227.md) — the source retrospective.
- [`./SKILL-SPEC-c207874125-paradigm-shift-reconciliation.md`](./SKILL-SPEC-c207874125-paradigm-shift-reconciliation.md) — the reconciliation pattern that applied this decision.
- [`../../architectures/v4/implementation-dependencies.md`](../../architectures/v4/implementation-dependencies.md) — the document this decision governs.
- PR the decision was made in: #227.
