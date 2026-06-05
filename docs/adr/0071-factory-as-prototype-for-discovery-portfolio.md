# ADR 0071: Factory as a prototype for discovery, co-implemented with a project portfolio

- **Status**: Accepted
- **Date**: 2026-06-05
- **Deciders**: jonathan@manton.com, session
- **ID**: ADR-6e3fa15d31

## Context

A planning session's first plan read as a march toward a *finished* v4 factory, with `agent-os` as the
single workload, run like a batched production line. The operator corrected three things: (1) `agent-os`
is "one of many projects" — a portfolio, not the goal; (2) the factory is to be built *in parallel with*
using it, where real components serve as drivers/test-cases that "solidify the factory," and the factory
"as designed will not be what I want at the end — this is a prototype to drive development and
evolution"; (3) "it's not about getting to the end, it's about discovery while using a nontrivial
real-world example." This is a binding stance on the project's purpose and working model.

## Decision

Treat the v4 factory as a **disposable prototype whose purpose is discovery**, **co-implemented** with a
**portfolio of real projects** (`agent-os` first of several) that drive its evolution — success is an
evidence-backed understanding of what to build next, not a "finished factory."

Concretely: the factory and the products advance together (each real component built is also a driver
that exercises the factory and exposes its next gap); the factory's own remaining components are
themselves drivers (self-builds); a running **factory-gap ledger** — not a roadmap guessed in advance —
decides which factory part to build next; and the factory we end up with is expected to be superseded,
having taught us how to specify its successor.

## Alternatives considered

- **Finish the factory, then build products with it.** Rejected: the operator wants co-implementation; a
  sequential "tool then use" plan defers all learning and treats the prototype as the deliverable.
- **`agent-os` as the sole, definitive workload.** Rejected: `agent-os` is explicitly "one of many," and
  binding the factory's evolution to a single Kubernetes-shaped product would over-fit it to that
  product's needs (e.g. the digital-twin gap) and dodge cheaper, more diagnostic drivers.
- **Treat the v4 design as the target architecture to complete faithfully.** Rejected: the operator
  framed v4 as scaffolding for discovery, not the end system; completing it faithfully would optimize
  the wrong objective.

## Consequences

- **Easier**: every unit of work pays double (a real artifact plus a factory lesson); the next factory
  investment is chosen empirically from the gap ledger rather than guessed; the prototype is free to be
  thrown away without sunk-cost drag.
- **Harder**: requires discipline to *capture* the discovery (the defect ledger and the factory-gap
  ledger) and to resist treating the prototype as precious; portfolio breadth must be managed so the
  factory is not over-fit to one product.
- **Trade-off accepted**: the v4 factory is transitional and partly disposable, in exchange for fast,
  evidence-driven learning about what the *real* factory and its methodology should be.
- **Binding on future sessions**: plans, handoffs, and component-selection inherit the co-implementation
  + portfolio + discovery framing.

## References

- [ADR 0070: Trust-map and play-menu model for selecting factory work](./0070-trust-map-and-play-menu-model.md) — the work-selection model this stance uses.
- [the factory discovery charter](../../factory-discovery-charter.md) — records this stance and declares it wins on framing where older docs disagree.
- [the methodology &amp; formulas report](../../methodology-and-formulas-plain-english.md) — the co-implementation loop in detail.
- [source retrospective 2026-06-05-247](../../retrospective/2026-06-05-247.md) [§Part 4](../../retrospective/2026-06-05-247.md#part-4--proposed-adrs) — where this decision was harvested (durable ID `ADR-6e3fa15d31`).
