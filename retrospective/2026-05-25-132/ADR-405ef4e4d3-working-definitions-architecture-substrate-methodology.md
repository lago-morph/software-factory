# ADR: Working definitions of architecture, substrate, and methodology

- **ID**: ADR-405ef4e4d3
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-25
- **Source retrospective**: ../2026-05-25-132.md
- **PRs covered**: #132

## Context

The terms "architecture," "substrate," and "methodology" appear throughout the v3 synthesis corpus and the project's working documents. Different sources use them differently — and during the session, the lead agent and the user found themselves talking past each other multiple times because the underlying definitions weren't pinned down. The substrate-vs-methodology split was explicitly contested in the Phase-2 outputs (the substrate-first tracks said substrate-is-the-architecture; the methodology-first tracks said methodology-is-the-architecture; Round-2 synthesis had recommended substrate-heavy + thin-methodology; CTR-C2 registered the tension).

The session needed an explicit binding definition so that downstream phases — buildability sketches, ADR authoring, architecture spec authoring — could refer to consistent terms. The user asked for the definitions to be recorded.

## Decision

**Substrate** is the set of platform primitives the factory consumes during operation. Each primitive has a contract (role + API surface + partition discipline), a construction path (how it gets built; required per the buildability ADR), a corpus justification (why it exists per corpus references), and is paired with at least one methodology that uses it (at the combination stage).

**Methodology** is the per-cycle process the factory runs against the substrate. Specifies the unit-of-work, the cycle shape (stages, regimes, gates, when each fires), the knowledge-accumulation pattern, and the error-handling protocol. A methodology *requires* substrate primitives but does not *own* them; the same substrate primitives can host different methodologies and the same methodology can run on different substrates that satisfy its contracts.

**Architecture** is a named composition of (a) a methodology — or a graph of methodology variants per work-unit-class — plus (b) the substrate primitives that methodology requires (with construction paths and corpus justifications) plus (c) the **discipline that binds them** — how the methodology calls into the substrate, what invariants are maintained at boundaries, what happens at transitions. An architecture is a *proposal*; a deployed factory is a *realization* of an architecture with specific tool / vendor / deployment-configuration choices.

**Architecture-level disciplines are a separate meta-layer.** Things like the three-layer citation discipline, the concrete-task discipline, the bias-guard discipline, and the cross-session-resumption discipline are *not* substrate primitives or methodology choices — they govern how the architecture's artifacts are produced. They live above both substrate and methodology.

## Alternatives considered

- **No formal definitions; let context disambiguate.** Rejected because the session demonstrated that context did not disambiguate — multiple turns were lost to substrate-vs-methodology framing confusion.
- **Substrate-only architecture (Round-2 "substrate-heavy + thin-methodology" framing).** Rejected as it forecloses methodology as a first-class architectural concern; the unified-methodology tracks demonstrate the methodology layer carries load-bearing decisions.
- **Methodology-only architecture (treating substrate as commodity infrastructure).** Rejected because some substrate primitives (notably CodebaseModel-class artifacts) are non-commodity designed systems that the architecture must explicitly name and bound.
- **Adopt the corpus's existing definitions verbatim.** Rejected because the corpus is internally inconsistent on these terms; the working definitions pin one consistent reading the project will use.

## Consequences

**Easier.** Downstream phases (buildability, ADRs, architecture specs) have a stable vocabulary. Cross-session resumption (a new agent picking up cold) starts from the definitions rather than re-deriving them. The methodology-over-substrate orientation (methodologies drive; substrate requirements fall out) becomes operationalizable: each methodology *requires* substrate primitives; the substrate inventory falls out from the union of methodology requirements.

**Harder.** Some existing material in the corpus does not align with these definitions (different sources used the terms differently). The Phase-7 back-fill audit will need to engage this — content from the archived v1/v2 architectures may need rephrasing to match. Some primitives the corpus called "substrate" may turn out to be methodology-layer under the new definitions and vice versa.

**Accepted trade-off.** Some terminology friction in exchange for downstream clarity. The cost is one ADR (this one) plus a re-reading of archived material during Phase 7; the benefit is a binding shared vocabulary for the rest of the v3 work and any subsequent synthesis runs.

## References

- [`../2026-05-25-132.md`](../2026-05-25-132.md) — source retrospective.
- [`../../architectures/v3/phase-3.4-decisions-resolved.md`](../../architectures/v3/phase-3.4-decisions-resolved.md) — the working definitions section that this ADR mirrors and formalizes.
- [`./ADR-a34b0b8636-substrate-primitive-buildability-requirement.md`](./ADR-a34b0b8636-substrate-primitive-buildability-requirement.md) — the buildability rule depends on these definitions to determine what is a substrate primitive.
- PRs the decision was made in: #132.
