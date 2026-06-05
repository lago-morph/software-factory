# ADR 0070: Trust-map and play-menu model for selecting factory work

- **Status**: Accepted
- **Date**: 2026-06-05
- **Deciders**: jonathan@manton.com, session
- **ID**: ADR-f5e614aabe

## Context

A planning session set out to decide "what to exercise the v4 factory with next." The first plan framed
it as a rigid, gated 2–3 week sequence (a queue of steps). The operator pushed back across several
brainstorm turns: nothing about the factory is ever "proven," it just gets *gradually more trusted*; and
they did not want a queue — they wanted "a selection of things I can try next" that they could pick from
by mood or insert their own into, because this is a personal project done for enjoyment, and "if it
feels too much like work it will kind of suck." That reframing governs how *all* future factory work is
selected, so it is recorded as a binding decision rather than left implicit in a plan doc.

## Decision

Work for the v4 factory is selected from a **mood-shopped board of cards** governed by a
**per-capability trust gradient** (the "trust map"), not a fixed sequence — with **fun as a first-class
selection constraint** and bookkeeping kept as a byproduct of the work, never a separate chore.

The model has three parts: (1) a **trust map** — each built capability carries a trust level on a 5-rung
gradient (🌑 Untouched → 🌒 Smoke-OK → 🌓 Poked → 🌔 Worked → 🌕 Trusted), set by gut and nudged by
evidence that falls out of work already done; (2) a **board of cards** — a browsable menu of candidate
exercises, each tagged with what it pressures, size, fun, what you'll learn, dual-use payoff, and
prereqs, shopped by mood, with a soft nudge surfacing low-trust ("lonely") capabilities as suggestions
not mandates; (3) the operator may **insert their own** card at any time and it is tagged so it still
contributes to coverage. The one ordered exception is a short up-front on-ramp that earns trust in the
*measuring instruments* (substrate reality, judge calibration, holdout integrity) before any card's
result is believed.

## Alternatives considered

- **A binary proven/unproven surface with a coverage matrix.** Rejected: the operator explicitly said
  trust is a gradient, not a flip, and a nagging matrix would make the project feel like work — fatal
  for a for-fun personal project.
- **A fixed sequence, or two parallel tracks (a toy track and a real track).** Rejected: the operator
  did not want to be marched; they wanted a menu they could pick from by appetite and energy level.
- **Heavy quantitative trust metrics.** Rejected (softened): the operator preferred to "wing it" with a
  gut rating, optionally backed by cheap evidence. Heavy metrics were explicitly deprioritized to keep
  the project enjoyable; the gradient is qualitative with optional objective nudges.

## Consequences

- **Easier**: low-friction, enjoyment-preserving work selection; the operator can act at any energy
  level; coverage still accrues because inserted cards are tagged; trust-tracking costs ~nothing because
  it is a byproduct of the work.
- **Harder**: there is no mechanical "are we done / are we covered" gate — progress and coverage are
  softer signals that require the operator to occasionally glance at the trust map and the
  lonely-capabilities nudge.
- **Trade-off accepted**: we trade rigorous, enforced coverage for sustained engagement, on the explicit
  judgment that a for-fun project that gets *played* beats a rigorous one that gets abandoned.
- **Binding on future sessions**: the first concrete next step (author the opening board of cards) and
  all subsequent work-selection inherit this model.

## References

- [ADR 0071: Factory as a prototype for discovery, co-implemented with a project portfolio](./0071-factory-as-prototype-for-discovery-portfolio.md) — the companion stance this model serves.
- [the factory discovery charter](../../factory-discovery-charter.md) — operationalizes this model (trust map, board, vocabulary).
- [the next-steps plan](../../next-steps-plain-english.md) — rewritten around the board.
- [source retrospective 2026-06-05-247](../../retrospective/2026-06-05-247.md) [§Part 4](../../retrospective/2026-06-05-247.md#part-4--proposed-adrs) — where this decision was harvested (durable ID `ADR-f5e614aabe`).
