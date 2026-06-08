# ADR 0072: Operator tooling is an instrument alongside the backbone, not a backbone component

- **Status**: Accepted
- **Date**: 2026-06-08
- **Deciders**: session (operator + AI seat)
- **ID**: ADR-a14da885a2 (durable retrospective hash; preserved on promotion)

## Context

Issue idea-pipeline #21 requested a "Gascity progress tracker" TUI and explicitly asked that it "be added as a component of the software-factory-prototype in backbone, next thing to build in the backbone build." Taken literally, that would make the TUI a 26th entry in the [backbone implementation plan](../../architectures/v4/backbone-implementation-plan.md), whose entire design is a closed, dependency-justified set of 25 components aimed at one apex (C53 behind the fence C43) — the safe self-build thesis. The TUI depends on the substrate but nothing in the dependency graph depends on *it*; folding it into the 25 would distort the coverage map the build order is organized around. The on-ramp already frames this class of artifact: "until you trust the factory's instruments you can't trust the result of any card."

## Decision

Operator-facing and observability tooling (such as the progress-tracker TUI) is recorded as an **instrument built alongside** the v4 backbone rather than as a numbered backbone capability component.

It remains first-class in the build order — it is the next thing built once the substrate (Gate B0) is up, and it grows as each backbone component lands (each new capability is a new thing to watch) — it simply is not counted among the 25.

## Alternatives considered

- **Insert the TUI as a 26th backbone component (the issue's literal wording).** Rejected: the 25 are justified by a strict dependency graph and the self-build thesis; a viewer that nothing depends on distorts that accounting and the coverage matrix for no analytical gain.
- **Track the TUI only on Board 1 (Card 8) with no plan-level mention.** Rejected: the operator wanted it institutionalized in durable plans and built next; a board card alone does not record the build-order placement or the instrument-vs-component framing.

## Consequences

- Easier: the backbone plan's 25-component accounting and dependency graph stay clean; the instrument can be enhanced continuously via board cards without re-opening backbone scope.
- Harder / accepted trade-off: "instrument vs component" is a distinction future readers must respect — there is now a category of build artifact that is planned and built but deliberately excluded from the numbered set. The backbone plan carries a short "built alongside (not one of the 25)" section to make that explicit.
- Establishes a reusable category: future operator/observability tooling follows the same instrument-alongside pattern rather than inflating the component count.

## References

- [tui-operator-instrument-plan.md](../../architectures/v4/tui-operator-instrument-plan.md) — the instrument plan this decision produced.
- [backbone-implementation-plan.md](../../architectures/v4/backbone-implementation-plan.md) — carries the "built alongside" section.
- [BOARD.md](../../BOARD.md) — Board 1 Card 8, the instrument's enhancement-card lineage.
- [source retrospective 2026-06-08-258](../../retrospective/2026-06-08-258.md) and its [ADR draft](../../retrospective/2026-06-08-258/ADR-a14da885a2-operator-tooling-instrument-not-component.md).
- Decided in PRs: software-factory #257, software-factory-prototype #12.
