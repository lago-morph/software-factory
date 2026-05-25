# ADR 0064: D7-U-1 P-30 variant — survival-window state machine

- **Status**: Accepted
- **Date**: 2026-05-25
- **Deciders**: Wave 5.3c2 subagent

## Context

[ADR 0036](0036-p-30-event-registrar-substrate.md) records the **common P-30 substrate** — Temporal (signal+timer+query triad) + append-only event-log — shared between U-A's re-entry registrar and D7-U-1's survival-window registrar. It defers per-variant state-machine definitions to Wave 5.3; this ADR is the D7-U-1 one (U-A sibling: [ADR 0053](0053-p-30-variant-u-a-re-entry.md)).

The [Phase-4.2 overlap verdict on P-30](../../architectures/v3/primitives/overlap.md#p-30-event-registrar--two-contested-variants) is verbatim:

> **Verdict: DISTINCT primitives** despite shared underlying substrate. Both use Temporal workflow engine (signal+timer+query triad) at the construction layer, but the load-bearing semantics diverge:
>
> - U-A's registrar is **event-driven**: state transitions on external triggers; the timer half is incidental (deadline tracking only).
> - D7-U-1's registrar is **timer-driven**: the load-bearing transition is `survival-window-open → window-expired`, with cascade wake-up of dependent-FC graphs. The event half is incidental (verdict-rendered is the input event but the registrar's value-add is the post-verdict timer cascade).
>
> The state-machines have non-overlapping invariants. A single deployment hosting both candidates' methodologies would need two separate registrar instances (or a shared instance with strict namespace separation of `state-machine-class` field).

The overlap.md table row for D7-U-1 specifies the state machine as `FC-declared → opposing-side-running → verdict-rendered → survival-window-open → window-expired → re-falsification-required`, trigger source **timer-driven** (window expiry wakes dependent-FC graphs).

[D7-U-1's substrate-requirements §3 P-30 contract](../../architectures/v3/substrate-requirements/d7-u-1.md) names the same machine and adds the load-bearing claim: the timer half drives cascade wake-up of dependent-FC graphs when a parent's `survival-window` expires, flagging every downstream artifact that depended on the expired verdict. Subscribers: compounding gate ([ADR 0030 P-29](0030-p-29-policy-mediator.md)), independence auditor (P-34), FC store ([ADR 0029 P-28](0029-p-28-typed-object-store.md) — the D7-U-1 FC envelope variant is the sibling Wave 5.3c2 ADR 0062 on the `FalsificationCommitment` envelope chain).

The substrate, signal+timer+query primitives, event-log envelope, namespace separation, and deterministic-replay guarantee are inherited unchanged from ADR 0036; this ADR specifies only what plugs into them as a `state-machine-class = d7-u-1-survival-window` namespace.

## Decision

**Build D7-U-1's P-30 instantiation as a Temporal workflow type `SurvivalWindowWorkflow` (Python SDK), timer-driven via durable timer handlers, with signal and query handlers as incidental supports.**

Four components:

1. **Workflow type + state field.** `SurvivalWindowWorkflow` carries an authoritative `state ∈ {FC-declared, opposing-side-running, verdict-rendered, survival-window-open, window-expired, re-falsification-required}` and an FC envelope reference (per ADR 0062's `FalsificationCommitment` chain — the workflow holds the commitment ID, not the envelope body). Initial state is `FC-declared` on workflow start; the workflow runs for the lifetime of the FC (long-running by design — survival windows are days-to-weeks).

2. **Timer handlers (load-bearing timer-driven semantics).** A durable `@timer` armed at `survival-window-open` entry fires when `verdict.survival-window` elapses and transitions `survival-window-open → window-expired → re-falsification-required` atomically. On expiry the handler (a) reads the FC envelope's `ledger.immutable-log-ref` to enumerate dependent FCs (children whose `conjecture` depended on this FC's `verdict.outcome ∈ {survived, conditionally-survived-with-window}`) via the FC envelope chain from ADR 0062, (b) signals each dependent workflow with `@signal parent_window_expired(parent_fc_id)` to cascade re-falsification-required, and (c) writes a typed envelope to the append-only event log per ADR 0036's `{event-id, state-machine-class=d7-u-1-survival-window, from-state, to-state, signal-payload-hash, timestamp, replay-cursor}` schema. Temporal's durable-timer guarantee (timers survive worker restarts and cluster failover) is the construction-layer property the cascade rests on.

3. **Signal handlers (incidental — input events).** `@signal opposing_side_started()`, `@signal verdict_rendered(outcome, survival_window, counter_evidence)`, and `@signal parent_window_expired(parent_fc_id)` drive the early-stage transitions and the cascade-receiver side. `verdict_rendered` is the input that arms the load-bearing timer (extracting `survival_window` duration); it is not itself load-bearing — the registrar's value-add begins after the verdict.

4. **Query handlers (state introspection).** `@query get_state()`, `@query get_fc_id()`, `@query get_dependent_fc_set()`, `@query get_event_log_cursor()` allow compounding-gate, independence-auditor, and FC-store subscribers to read state without signalling, satisfying the overlap.md subscriber-set contract.

The `state-machine-class = d7-u-1-survival-window` namespace separates this workflow type from U-A's sibling workflow on the same Temporal cluster, per ADR 0036's namespace-separation discipline.

## Alternatives considered

**B. Event-driven only (U-A's variant shape).** *Why rejected:* event-driven semantics defeat D7-U-1's load-bearing claim that survival-window expiry is a **timer event** that wakes dependent FC graphs without external prompting. Per [overlap.md](../../architectures/v3/primitives/overlap.md#p-30-event-registrar--two-contested-variants), the load-bearing transition is `survival-window-open → window-expired` driven by elapsed time, not by an external signal. Importing U-A's event-driven shape would require an external scheduler to poll FCs for window expiry — a structurally fragile design the Phase-4.2 DISTINCT verdict explicitly forbids. The two registrars cannot share semantics.

**C. Pure cron without Temporal (cron + Postgres state-transition table).** *Why rejected:* loses ADR 0036's signal+timer+query triad as a single contract surface. Cron's timer semantics are non-durable (a missed tick on operator outage silently delays cascade wake-up; D7-U-1's compounding gate would then admit artifacts whose parent FC has *de facto* expired — F1/F27/F46/F48 cascade per [d7-u-1.md §5 F-mode carries](../../architectures/v3/substrate-requirements/d7-u-1.md)). The bespoke layer would also re-implement durable signals (for `verdict_rendered`, for cascade), queryable state, and replay separately — re-specifying substrate concerns ADR 0036 already settled.

## Consequences

**Easier:** D7-U-1's cascade-wake-up semantics land on substrate: Temporal's durable timer fires `window-expired` deterministically; the cascade reads the FC envelope chain ([ADR 0062 sibling](0062-p-28-variant-d7-fc-envelope.md)) to enumerate dependents; subscribers receive the expiry event via signal + event log per ADR 0036's envelope schema. The Phase-8 [timer-half vs event-half reliability pressure-test](../../architectures/v3/primitives/overlap.md#3-findings-carried-into-wave-46) can measure D7-U-1's timer-driven path against U-A's event-driven path on the same cluster with isolated namespaces.

**Harder:** The named failure mode — **cascade-fail if the timer half is unreliable** (per [overlap.md P-30 implications](../../architectures/v3/primitives/overlap.md#p-30-event-registrar--two-contested-variants)) — is mitigated but not eliminated by Temporal's durable-timer guarantee. Persistence-backend outages, worker-fleet sizing errors, and clock-skew across cluster nodes remain operational risks; the compounding gate must treat absent-cascade as fail-closed (artifacts whose parent FC has no fresh `survived` verdict within window are unavailable). Dependent-FC enumeration cost is linear in the FC graph's fanout — wide fanouts at large scale (D7-U-1 OQ-2 corpus-unmeasured) carry latency risk.

**Explicitly NOT promising:** Re-falsification orchestration (how `re-falsification-required` is actually scheduled, which opposing-side handler runs, conditional vs unconditional re-run) is deferred to a Phase-6 methodology spec per [D7-U-1 §5 open carries](../../architectures/v3/substrate-requirements/d7-u-1.md#5-open-carries). This ADR fixes the state-machine skeleton and the cascade-emission contract only.

## References

- [ADR 0036: P-30 event registrar substrate (Temporal)](0036-p-30-event-registrar-substrate.md) — parent common ADR (signal+timer+query triad, event-log envelope, deterministic-replay guarantee, namespace separation)
- [ADR 0053: U-A P-30 variant — re-entry-interval state machine](0053-p-30-variant-u-a-re-entry.md) — event-driven sibling on the same substrate; documents the explicit asymmetry this ADR mirrors in reverse
- [Phase-4.2 overlap.md P-30 verdict — two contested variants DISTINCT](../../architectures/v3/primitives/overlap.md#p-30-event-registrar--two-contested-variants) — verbatim DISTINCT verdict and the timer-driven row this ADR instantiates
- [D7-U-1 substrate-requirements §3 P-30 contract](../../architectures/v3/substrate-requirements/d7-u-1.md) — state-machine sequence, load-bearing cascade wake-up, subscriber set, distinction from U-A
- [D7-U-1 track §1 architecture sketch primitive 5](../../architectures/v3/bias-guards/phase-3/d7-blind-axis/d7-u-1-prohibit-interval-escrow.md#1-architecture-sketch) — survival-window registrar as cascade-driver over the FC graph
- [P-30 buildability sketch](../../architectures/v3/primitives/P-30-event-registrar.md) — D7-U-1 bullet naming the survival-window registrar as timer-driven workflow type
- [ADR 0062: D7-U-1 P-28 FC envelope variant](0062-p-28-variant-d7-fc-envelope.md) — sibling Wave 5.3c2 ADR defining the `FalsificationCommitment` envelope chain the cascade reads to enumerate dependents
