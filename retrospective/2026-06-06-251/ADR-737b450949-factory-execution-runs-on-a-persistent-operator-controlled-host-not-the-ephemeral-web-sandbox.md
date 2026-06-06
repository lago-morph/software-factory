# ADR: Factory execution runs on a persistent operator-controlled host, not the ephemeral web sandbox

- **ID**: ADR-737b450949
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-06-06
- **Source retrospective**: ../2026-06-06-251.md
- **PRs covered**: #249, #250, #251

## Context

This session authored the opening board and the backbone build plan, both of which point at **Step 3 —
execution**, entering at Gate B0: adopt and pin the `gc` binary and run the Gas City **conformance
check** (does `gc` *prevent* a forbidden action or only *detect* it after the fact?). The operator asked
a pointed clarifying question: *"Just so I'm clear, you are going to build all this in the agent
sandbox?"* That surfaced a binding constraint that had been implicit and needed to be made explicit and
durable.

The Claude Code web sandbox the planning happened in is **ephemeral** (reclaimed after the session;
only git-committed artifacts survive), its **outbound network is policy-gated** (reachability of the
gascity-prototype is unknown until probed), and the conformance check is only meaningful against a
**real, pinned `gc`** run end-to-end. A factory installed, run, and storing state inside a container
that evaporates every session is not a factory anyone can operate, and a conformance verdict produced in
a throwaway environment is itself throwaway.

## Decision

Step 3 onward — installing and running Gas City, the Gate B0 conformance check, and operating the
factory — executes on a **persistent operator-controlled host**, while the ephemeral web sandbox is used
**only for authoring artifacts and committing them to git**.

## Alternatives considered

- **Build and run the factory inside the web sandbox.** Rejected: ephemerality means every session
  re-installs from scratch and loses all bead/process state; the network policy may block the install
  outright; and the Gate B0 verdict would not be trustworthy enough to build on (its whole purpose is to
  turn an assumption into a durable fact).
- **A throwaway in-sandbox spike, treated as the real verdict.** Rejected as the *real* verdict but
  **kept as an explicitly-labelled option**: a spike may run in-sandbox to see `gc` move, but its result
  is not trusted as the Gate B0 conformance verdict — the real check re-runs on the chosen host. This
  preserves a cheap experiment without letting it masquerade as the load-bearing measurement.

## Consequences

- **Easier:** honesty about where the factory lives; the [handoff](../../architectures/v4/SESSION-HANDOFF-2026-06-05-discovery-charter-and-next-steps.md)
  can split Step 3 into an operator entry-blocker (choose the host) plus in-sandbox prep that needs no
  answer (probe reachability; author the conformance-probe script + `city.toml`/`pack.toml` skeleton).
  Authoring work continues to flow through the normal commit/PR loop with no change.
- **Harder / accepted trade-off:** there is a venue switch between authoring (sandbox) and running
  (operator host); a future agent cannot "just run it here." The operator must stand up and maintain a
  host, and an execution session must run where `gc` actually lives. We accept that the build's center of
  gravity moves off the sandbox the moment real components are installed.

## References

- [`../2026-06-06-251.md`](../2026-06-06-251.md) — the source retrospective.
- [the backbone build plan, Gate B0](../../architectures/v4/backbone-implementation-plan.md) — the gate this constraint governs.
- [the 2026-06-06 session handoff](../../architectures/v4/SESSION-HANDOFF-2026-06-06-board-and-backbone-plan-close.md) — carries the constraint forward to the next session.
- PRs the decision was made in: #249, #250, #251.
