# ADR: The backbone build plan and the exercising plan are distinct artifacts meeting at the Gate-B4 seam

- **ID**: ADR-925e61d87c
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-06-06
- **Source retrospective**: ../2026-06-06-251.md
- **PRs covered**: #250

## Context

When authoring the Step-2 plan this session, a naming hazard surfaced: the repo already contained a
panel-reviewed [unified plan](../../architectures/v4/_meta/next-steps/10-unified-plan.md) whose Gates
0–5 describe how to **exercise** the factory on real `agent-os` work — but its own header states its
horizon is "the 2–3 weeks *after* the 25-component backbone is built." The handoff's Step 2 asked for a
plan to **build** those 25 components, which is a different activity (standing up Gas City, writing the
spec intake, the eval tier, the fence, the bootstrap loop). Conflating the two would have produced a
plan that mixed "install and configure the substrate" with "drive agent-os components through a
calibrated judge" — two different audiences, dependency graphs, and definitions of done.

## Decision

The plan to **build** the backbone-25 and the plan to **exercise** the built factory on `agent-os` are
maintained as **two separate documents** that meet at a **single named seam** — Gate B4 of the build
plan, which is the unified plan's starting line — and must not be conflated.

## Alternatives considered

- **One combined plan covering build + exercise.** Rejected: it would re-derive the already-reviewed
  unified plan, blur the adopt-vs-build classification the operator explicitly asked for, and obscure
  the clean handoff point where instruments are calibrated and the fence is up.
- **Fold the build steps into the existing unified plan as a "Gate -1".** Rejected: the unified plan was
  adversarially reviewed at its current scope (the 8 amendments are calibrated to it); retrofitting the
  whole substrate build into it as a prequel would invalidate that review boundary and overload one
  document.

## Consequences

- **Easier:** each plan has one job and one audience; the build plan can lead with the adopt-vs-build
  split and the five build gates, while the unified plan keeps its reviewed exercising shape. A reader
  always knows which phase they are in.
- **Harder / accepted trade-off:** the seam must be kept consistent across both documents and the
  handoff — Gate B4's exit criteria (the 25 stand together, judge calibrated to a stated bar, fence up)
  must stay identical to the unified plan's stated entry assumptions. If one drifts, the two plans no
  longer meet cleanly; the build plan's "seam to the next phase" section and the handoff both restate
  the seam to keep it pinned.

## References

- [`../2026-06-06-251.md`](../2026-06-06-251.md) — the source retrospective.
- [the backbone build plan](../../architectures/v4/backbone-implementation-plan.md) — the build artifact (ends at Gate B4).
- [the unified plan](../../architectures/v4/_meta/next-steps/10-unified-plan.md) — the exercising artifact (begins where the build plan ends).
- PRs the decision was made in: #250.
