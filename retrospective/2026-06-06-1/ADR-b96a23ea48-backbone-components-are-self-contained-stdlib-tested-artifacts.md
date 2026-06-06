# ADR: Backbone components are self-contained stdlib-tested artifacts under factory/

- **ID**: ADR-b96a23ea48
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-06-06
- **Source retrospective**: ../2026-06-06-1.md
- **PRs covered**: #1

## Context

With the Gate B0 substrate in place, the session added Gate B1 backbone components (C20 bead schema, C08/C09 spec intake, C43 fence boundary-typing, C29 model-floor) using four parallel subagents. Each component faithfully implements an upstream v4 spec interface and a Gate exit criterion. Wiring each one deeply into the gc pack at authoring time would have coupled four parallel work streams to the same integration surface and made offline testing impossible — yet the components needed to be verifiable green before the orchestrator committed them. This made the component packaging shape a binding decision about how the backbone is built and tested.

## Decision

Implement each Gate B1 backbone component as a self-contained directory under `factory/` with its artifact, a pure-stdlib validator, fixtures, and a `test.sh`, faithful to the upstream v4 spec's interface and Gate exit criterion (sweep-1), deferring deep gc-pack wiring to sweep-2.

## Alternatives considered

- **Wire each component directly into the gc pack now (sweep-2 work brought forward)** — rejected: it couples the four parallel authoring streams to one integration surface, prevents offline stdlib-only testing, and bloats the substrate-plus-B1 increment beyond what the orchestrator could verify and commit cleanly in this session.

## Consequences

Each component is testable offline with no external dependencies (pure stdlib + fixtures + `test.sh`), so the four parallel subagents could be verified independently and the orchestrator could confirm all green before committing. The trade-off is that gc-pack integration becomes explicit follow-up (sweep-2): the components exist and pass their own gates but are not yet wired into the live pack. This keeps the B0+B1 increment small and reviewable while leaving a clear, named seam for the next pass.

## References

- [`../2026-06-06-1.md`](../2026-06-06-1.md) — the source retrospective.
- PRs the decision was made in: #1 (lago-morph/software-factory-prototype).
