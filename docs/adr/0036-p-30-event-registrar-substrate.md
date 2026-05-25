# ADR 0036: P-30 event registrar substrate (Temporal substrate only)

- **Status**: Accepted
- **Date**: 2026-05-25
- **Deciders**: lead agent (Phase 5 Wave 5.1b fanout)

## Context

Two candidates claim P-30 event registrar as a load-bearing substrate primitive: [U-A re-entry registrar](../../architectures/v3/tracks/unified-A.md#1-architecture-sketch) and [D7-U-1 survival-window registrar (variant)](../../architectures/v3/bias-guards/phase-3/d7-blind-axis/d7-u-1-prohibit-interval-escrow.md#1-architecture-sketch). The [Phase-3.5 buildability sketch](../../architectures/v3/primitives/P-30-event-registrar.md) verdicts the primitive `designed-system` — the workflow engine is commodity-grade; the per-variant state machine + subscriber catalog is the load-bearing design content.

The [Phase-4.2 overlap analysis](../../architectures/v3/primitives/overlap.md#p-30-event-registrar--two-contested-variants) renders the same-vs-distinct verdict verbatim:

> **Verdict: DISTINCT primitives** despite shared underlying substrate. Both use Temporal workflow engine (signal+timer+query triad) at the construction layer, but the load-bearing semantics diverge:
>
> - U-A's registrar is **event-driven**: state transitions on external triggers; the timer half is incidental (deadline tracking only).
> - D7-U-1's registrar is **timer-driven**: the load-bearing transition is `survival-window-open → window-expired`, with cascade wake-up of dependent-FC graphs. The event half is incidental (verdict-rendered is the input event but the registrar's value-add is the post-verdict timer cascade).
>
> The state-machines have non-overlapping invariants. A single deployment hosting both candidates' methodologies would need two separate registrar instances (or a shared instance with strict namespace separation of `state-machine-class` field).

Per that verdict, Phase 5 ships **one common ADR on the underlying Temporal substrate choice** (this ADR) plus **two distinct per-variant state-machine ADRs** (deferred to Wave 5.3 next run per [auto-005 Round 2 § Wave-5.1b scope boundary](../../architectures/v3/decisions/auto-005-phase-5-dispatch-shape.md#decision-round-2)).

## Decision

**Build P-30's underlying substrate on [Temporal](https://temporal.io) workflow engine, using the signal+timer+query triad as the registrar's contract surface, with an append-only event-log contract published alongside.** Each registrar variant is realized as a Temporal workflow *type*; domain events are Temporal **signals**; state transitions are workflow *steps* gate-checked by deterministic predicates; survival windows and re-entry deadlines are Temporal **timers** (durable across worker restarts); subscribers consume workflow **queries** plus signal-driven child workflows.

The **event-log contract** (substrate-level, candidate-independent): the workflow's event history *is* the append-only log; entries are typed envelopes `{event-id, state-machine-class, from-state, to-state, signal-payload-hash, timestamp, replay-cursor}`; the log is replayable end-to-end; Temporal's deterministic-replay guarantee gives the substrate the "no silent state divergence" property both variants need. Per-variant state machines plug into this contract as `state-machine-class` namespaces with their own transition tables, subscriber sets, and invariant predicates — defined in the per-variant ADRs.

## Alternatives considered

**B. AWS EventBridge + Step Functions.** Typed event schemas natively; rule-based routing native; state-machine portion bolted on via Step Functions. *Why rejected:* (1) vendor lock-in to AWS; (2) Step Functions' timer guarantees are weaker than Temporal's durable-timer semantics (Step Functions wait-states are billed and capped; long survival windows risk silent expiry); (3) the two-tool split (EventBridge for events, Step Functions for state) fragments the append-only-log contract — two systems to reason about for replay. See [P-30 sketch construction-path alternates](../../architectures/v3/primitives/P-30-event-registrar.md#construction-path-with-integration-sentence).

**C. Postgres-NOTIFY + advisory-locks + state-transition table.** Low-scale alternative for deployments where Temporal is over-engineered. *Why rejected:* (1) no built-in workflow state — the implementer must hand-roll a bespoke state-machine layer on top of NOTIFY + locks; (2) that bespoke layer would be re-implemented in *each* per-variant ADR (U-A re-entry + D7-U-1 survival-window), duplicating substrate-level concerns the per-variant ADRs should not own; (3) timer guarantees rely on external schedulers (cron / pg_cron) with no replay semantics — D7-U-1's load-bearing timer-cascade transition is structurally fragile here. See [overlap.md timer-half reliability concern](../../architectures/v3/primitives/overlap.md#p-30-event-registrar--two-contested-variants).

## Consequences

**Easier:** Both candidates' registrar variants share one substrate-deployment skill (Temporal cluster + workers); both inherit Temporal's deterministic-replay guarantee for free; the append-only event log is the workflow history (no separate log primitive); operators familiar with Temporal from one variant transfer that fluency to the other; the Phase-8 [timer-half vs event-half reliability pressure-test](../../architectures/v3/primitives/overlap.md#3-findings-carried-into-wave-46) measures both variants on a uniform substrate.

**Harder:** Temporal cluster operation (worker fleets, persistence backend, namespace management) becomes a per-environment ops requirement; teams without prior Temporal exposure pay a learning-curve cost; deployments hosting both U-A and D7-U-1 methodologies need strict `state-machine-class` namespace separation (or two registrar instances) to prevent cross-variant signal leakage.

**Explicitly NOT promising:** Per the auto-005 Round 2 Wave-5.1b dispatch brief, this ADR's scope is the Temporal substrate and event-log contract only. Phase-6 architecture specs for U-A and D7-U-1 MUST reference BOTH (a) this common substrate ADR AND (b) the candidate's per-variant state-machine ADR from Wave 5.3 next run (P-30-variant-u-a-re-entry; P-30-variant-d7-u-1-survival-window). Referencing only this ADR for state-machine semantics is a known scope error.

## References

- [P-30 buildability sketch](../../architectures/v3/primitives/P-30-event-registrar.md) — construction path and per-variant difference enumeration
- [Phase-4.2 overlap verdict on P-30 (two contested variants — DISTINCT)](../../architectures/v3/primitives/overlap.md#p-30-event-registrar--two-contested-variants)
- [U-A re-entry registrar §1 primitive 5](../../architectures/v3/tracks/unified-A.md#1-architecture-sketch) and [§2 OQ-B3 resolution](../../architectures/v3/tracks/unified-A.md#oq-b3-human-re-entry-mechanism)
- [D7-U-1 survival-window registrar §1 primitive 5](../../architectures/v3/bias-guards/phase-3/d7-blind-axis/d7-u-1-prohibit-interval-escrow.md#1-architecture-sketch)
- [auto-005 Round 2 Phase-5 dispatch shape](../../architectures/v3/decisions/auto-005-phase-5-dispatch-shape.md#decision-round-2) — Wave-5.1b scope boundary defining this ADR's Temporal-substrate-only remit and deferring per-variant state machines to Wave 5.3
- [ADR 0015: P-08 scenario storage with runner contract](0015-p-08-scenario-storage-with-runner-contract.md) — Wave-5.1a exemplar this ADR follows in structure
