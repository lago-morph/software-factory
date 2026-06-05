# ADR: Trust-map and play-menu model for selecting factory work

- **ID**: ADR-f5e614aabe
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-06-05
- **Source retrospective**: ../2026-06-05-247.md
- **PRs covered**: #247

## Context

The session set out to plan "what to exercise the factory with next." The first plan framed it as a
rigid, gated 2–3 week sequence (a queue of steps). The operator pushed back across several brainstorm
turns: nothing about the factory is ever "proven," it just gets *gradually more trusted*; and they did
not want a queue — they wanted "a selection of things I can try next" that they could pick from by
mood or insert their own into, because this is a personal project done for enjoyment, and "if it feels
too much like work it will kind of suck." That reframing is binding on how *all* future work is
selected, so it is recorded here rather than left implicit in a plan doc.

## Decision

Work for the v4 factory is selected from a **mood-shopped board of cards** governed by a **per-capability
trust gradient** (the "trust map"), not a fixed sequence — with **fun as a first-class selection
constraint** and bookkeeping kept as a byproduct of the work, never a separate chore.

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
- **A fixed sequence / two parallel tracks (toy track + real track).** Rejected: the operator did not
  want to be marched; they wanted a menu they could pick from by appetite and energy level.
- **Heavy quantitative trust metrics.** Rejected (softened): the operator preferred to "wing it" with a
  gut rating, optionally backed by cheap evidence. Heavy metrics were explicitly deprioritized to keep
  the project enjoyable; the gradient is qualitative with optional objective nudges.

## Consequences

- **Easier**: low-friction, enjoyment-preserving work selection; the operator can act on any energy
  level; coverage still accrues because inserted cards are tagged; trust-tracking costs ~nothing because
  it is a byproduct.
- **Harder**: there is no mechanical "are we done / are we covered" gate — progress and coverage are
  softer signals that require the operator to occasionally glance at the trust map and the lonely-
  capabilities nudge.
- **Trade-off accepted**: we trade rigorous, enforced coverage for sustained engagement, on the
  explicit judgment that a for-fun project that gets *played* beats a rigorous one that gets abandoned.
- **Binding on future sessions**: the first concrete next step (build the opening board of cards) and
  all subsequent work-selection inherit this model; see the charter and handoff.

## References

- [`../2026-06-05-247.md`](../2026-06-05-247.md) — the source retrospective.
- [`../../factory-discovery-charter.md`](../../factory-discovery-charter.md) — the charter that operationalizes this model (trust map, board, vocabulary).
- [`../../next-steps-plain-english.md`](../../next-steps-plain-english.md) — the plan rewritten around the board.
- PRs the decision was made in: #247.
