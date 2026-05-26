# ADR 0053: U-A P-30 variant — re-entry-interval state machine

- **Status**: Accepted
- **Date**: 2026-05-25
- **Deciders**: Wave 5.3c1 subagent

## Context

[ADR 0036](0036-p-30-event-registrar-substrate.md) records the **common P-30 substrate** — Temporal workflow engine (signal+timer+query triad) + append-only event-log contract — shared between U-A's re-entry registrar and D7-U-1's survival-window registrar. It explicitly defers the per-variant state-machine definitions to Wave 5.3 (this ADR is the U-A one; D7-U-1's is a sibling).

The [Phase-4.2 overlap verdict on P-30](../../architectures/v3/primitives/overlap.md#p-30-event-registrar--two-contested-variants) is verbatim:

> **Verdict: DISTINCT primitives** despite shared underlying substrate. Both use Temporal workflow engine (signal+timer+query triad) at the construction layer, but the load-bearing semantics diverge:
>
> - U-A's registrar is **event-driven**: state transitions on external triggers; the timer half is incidental (deadline tracking only).
> - D7-U-1's registrar is **timer-driven**: the load-bearing transition is `survival-window-open → window-expired`, with cascade wake-up of dependent-FC graphs. The event half is incidental (verdict-rendered is the input event but the registrar's value-add is the post-verdict timer cascade).
>
> The state-machines have non-overlapping invariants. A single deployment hosting both candidates' methodologies would need two separate registrar instances (or a shared instance with strict namespace separation of `state-machine-class` field).

The overlap.md table row for U-A specifies the state machine as `in-flight → frozen → re-entry-open → operator-acknowledged → {resumed, redirected, closed}`, trigger source **event-driven** (watchdog escalation / cost-ceiling breach / severity-class trigger).

[U-A's substrate-requirements §3 P-30 contract](../../architectures/v3/substrate-requirements/u-a.md) names the same machine and adds: transitions are driven by typed events from [P-29](0030-p-29-policy-mediator.md) when [P-06 watchdog tiers](0013-p-06-watchdog-tiers.md) escalate, [D-5 cost-ceiling](0020-discipline-cost-ceiling.md) breaches, or a severity-class trigger promotes an in-flight interval to `escalate`. The frozen-state snapshot captures the in-flight graph position; the re-entry summary derives from the trajectory store + AILCCP immutable log. Subscribers: audit ledger, classifier, trajectory store.

The substrate, signal+timer+query primitives, event-log envelope, and deterministic-replay guarantee are inherited unchanged from ADR 0036; this ADR specifies only what plugs into them as a `state-machine-class = u-a-re-entry` namespace.

## Decision

**Build U-A's P-30 instantiation as a Temporal workflow type `ReEntryIntervalWorkflow` (Python SDK), event-driven via signal handlers, with timer and query handlers as incidental supports.**

Four components:

1. **Workflow type + state field.** `ReEntryIntervalWorkflow` carries an authoritative `state ∈ {in-flight, frozen, re-entry-open, operator-acknowledged, resumed, redirected, closed}` and an `EscrowInterval` envelope (per [ADR 0051 U-A P-28 interval envelope](0051-p-28-variant-u-a-interval-envelope.md), U-A's typed-node-graph variant of the [ADR 0029 P-28 typed-object store](0029-p-28-typed-object-store.md)). Initial state is `in-flight` on workflow start. Terminal states are `resumed`, `redirected`, `closed`.

2. **Signal handlers (load-bearing event-driven semantics).** Three external-trigger signals drive the load-bearing transitions: `@signal watchdog_escalate(tier, evidence)`, `@signal cost_ceiling_breach(ledger_ref)`, `@signal severity_class_trigger(class, reason)` — each transitions `in-flight → frozen` if not already past frozen, captures a graph-position snapshot, and emits `re-entry-open`. A fourth signal `@signal operator_acknowledge(decision ∈ {resume, redirect, close}, payload)` transitions `re-entry-open → operator-acknowledged → {resumed | redirected | closed}` as a single atomic step. Each signal handler writes a typed envelope to the append-only event log per ADR 0036's `{event-id, state-machine-class=u-a-re-entry, from-state, to-state, signal-payload-hash, timestamp, replay-cursor}` schema.

3. **Timer handler (incidental — deadline tracking only).** `@timer` fires a deadline on `re-entry-open`-state intervals to surface non-acknowledgement to the audit ledger (subscriber). The timer **never** drives a state transition by itself — it logs `awaiting-operator-acknowledgement` to the ledger and re-arms. This is the explicit asymmetry against D7-U-1's variant where the timer is load-bearing.

4. **Query handlers (state introspection).** `@query get_state()`, `@query get_envelope()`, `@query get_event_log_cursor()` allow audit-ledger, classifier ([P-19](0028-p-19-eligibility-regime-classifier.md)), and trajectory-store subscribers to read current state without signalling, satisfying the overlap.md subscriber-set contract.

The `state-machine-class = u-a-re-entry` namespace separates this workflow type from D7-U-1's sibling workflow on the same Temporal cluster, per ADR 0036's namespace-separation discipline.

## Alternatives considered

**B. Timer-driven only (D7-U-1's variant shape).** *Why rejected:* timer-driven semantics defeat U-A's load-bearing claim that re-entry is an **operator-decision event**, not a window-expiry. U-A's [§5.4 day-0 trajectory](../../architectures/v3/tracks/unified-A.md#54-day-0--day-n-trajectory) requires the operator be the proximate cause of resume/redirect/close — a timer firing `re-entry-open → resumed` automatically would erase the human-in-the-loop discipline U-A's mandate-fit rests on. Per [overlap.md](../../architectures/v3/primitives/overlap.md#p-30-event-registrar--two-contested-variants), U-A and D7-U-1 cannot share semantics; importing D7-U-1's shape into U-A is a category error the Phase-4.2 DISTINCT verdict forbids.

**C. Pure handler chain without Temporal (FastAPI + Postgres state-transition table).** *Why rejected:* loses ADR 0036's signal+timer+query triad as a single contract surface; the bespoke handler layer would have to re-implement durable signals, durable timers (for deadline tracking), and the queryable state field separately, against three different libraries; deterministic replay vanishes (ADR 0036's "no silent state divergence" guarantee is Temporal's, not a bespoke layer's); and the per-variant ADR ends up re-specifying substrate concerns ADR 0036 already settled.

## Consequences

**Easier:** U-A's [OQ-B3 human re-entry mechanism](../../architectures/v3/tracks/unified-A.md#oq-b3-human-re-entry-mechanism) lands on substrate: external triggers signal the workflow, operator acknowledgement closes the loop, audit ledger receives a complete event-log trail per ADR 0036's envelope schema. The Phase-8 [timer-half vs event-half reliability pressure-test](../../architectures/v3/primitives/overlap.md#3-findings-carried-into-wave-46) can measure U-A's event-driven path against D7-U-1's timer-driven path on the same Temporal cluster with isolated namespaces.

**Harder:** The named failure mode — **starve on operator non-acknowledgement** (an interval enters `re-entry-open` and the operator never sends `operator_acknowledge`) — is not prevented by the substrate; it must be surfaced by the timer-driven ledger alert (component 3 above) and escalated through Patrol-tier watchdog ([ADR 0013 P-06](0013-p-06-watchdog-tiers.md)). Operators carry an SLA on acknowledgement latency that this ADR records but does not enforce.

**Explicitly NOT promising:** Partial-re-entry semantics (`resume-with-modifications`, `redirect-to-different-kind`, partial-graph rehydration) are deferred to a Phase-6 methodology spec per [U-A §7 OQ 3](../../architectures/v3/tracks/unified-A.md#7-open-questions-surfaced-by-this-track). This ADR fixes the state-machine skeleton only.

## References

- [ADR 0036: P-30 event registrar substrate (Temporal)](0036-p-30-event-registrar-substrate.md) — parent common ADR (signal+timer+query triad, event-log envelope, deterministic-replay guarantee, namespace separation)
- [Phase-4.2 overlap.md P-30 verdict — two contested variants DISTINCT](../../architectures/v3/primitives/overlap.md#p-30-event-registrar--two-contested-variants) — verbatim DISTINCT verdict and the event-driven row this ADR instantiates
- [U-A substrate-requirements §3 P-30 contract](../../architectures/v3/substrate-requirements/u-a.md) — state-machine sequence, trigger sources, subscriber set, distinction from D7-U-1
- [U-A track §1 architecture sketch primitive 5 and OQ-B3](../../architectures/v3/tracks/unified-A.md#oq-b3-human-re-entry-mechanism) — re-entry mechanism as operator-decision event
- [P-30 buildability sketch](../../architectures/v3/primitives/P-30-event-registrar.md) — U-A bullet naming the re-entry registrar as event-driven workflow type
- [ADR 0051: U-A P-28 interval envelope variant](0051-p-28-variant-u-a-interval-envelope.md) — `EscrowInterval` envelope carried in this workflow
