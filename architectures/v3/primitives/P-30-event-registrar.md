# P-30 — Re-entry / event registrar

**Dispatch tier:** per-primitive (designed-system).
**Claimed by:** [U-A re-entry registrar](../tracks/unified-A.md#1-architecture-sketch); [D7-U-1 survival-window registrar (variant)](../bias-guards/phase-3/d7-blind-axis/d7-u-1-prohibit-interval-escrow.md#1-architecture-sketch).
**Same-vs-distinct verdict:** **NOT RENDERED HERE.** Per [Phase-3.4 scoping principle](../phase-3.4-decisions-resolved.md#scoping-principle-immutable-overrides-any-conflicting-framing-in-the-integration-brief) and [auto-001 Round-2 convergent finding #2](../decisions/auto-001-phase-3.5-dispatch-shape.md#convergent-findings-across-reviewers), whether U-A's re-entry registrar and D7-U-1's survival-window registrar collapse to a single primitive at methodology-to-substrate matching is a Phase-4.2 question. Per-variant paragraphs only below.

## Contract restatement

A substrate-typed **event-state-machine** that registers domain events (re-entry events; survival-verdict / window-expiration events) as durable typed objects, drives **deterministic state transitions** between event-states, and exposes a **subscription surface** so other substrate primitives (policy mediator P-29, watchdog tiers P-06, judge router P-14, FC compounding gate) can listen for specific event types and react. The registrar is **not** a generic message bus: each event carries a typed schema, transitions are gate-checked, and the event log is append-only and replayable. The registrar is the connective tissue that turns isolated substrate primitives into a **cycle graph** with explicit edges.

## Construction path (with integration sentence)

Primary candidate: **Temporal** ([temporal.io](https://temporal.io)) workflow engine. Each registrar variant is a Temporal workflow type; events are Temporal **signals**; state transitions are workflow steps; survival windows / re-entry timers are Temporal **timers** (durable across worker restarts); subscribers are workflow queries plus signal-driven child workflows. *Integration sentence:* Temporal's signal+timer+query triad realizes the registrar's "register event / await deterministic transition / expose subscription surface" contract directly — the workflow's event history *is* the append-only log, and the deterministic-replay guarantee gives the substrate the "no silent state divergence" property both variants need.

Alternates (Phase-5 ADR knobs, not commitments here):
- **AWS EventBridge** with typed event schemas + rule-based routing + Step Functions for state-machine portion (subscription surface is native; state machine is bolted on).
- **Apache Kafka** with Protobuf/Avro schemas + consumer groups + Kafka Streams for state transitions (high-throughput; less ergonomic for human-in-loop timers).
- **Custom Postgres-NOTIFY + advisory-locks + a state-transition table** for low-scale deployments where Temporal is over-engineered.

## Per-candidate variant differences

### U-A (re-entry registrar)

The registrar's events are **re-entry events** — typed `EscrowInterval{kind: re-entry}` open/close transitions. Triggered by the policy mediator (P-29) when watchdog escalation, cost-ceiling breach, severity-class trigger, or operator-of-record decision promotes an in-flight interval to `escalate`. State machine: `in-flight → frozen → re-entry-open → operator-acknowledged → resumed | redirected | closed`. Subscribers: the substrate's audit ledger (AILCCP immutable log), the classifier (re-classification on resume), the trajectory store (frozen-state snapshot). See [unified-A §1 primitive 5](../tracks/unified-A.md#1-architecture-sketch) and [§2 OQ-B3 resolution](../tracks/unified-A.md#oq-b3-human-re-entry-mechanism).

### D7-U-1 (survival-window registrar — variant)

The registrar's events are **FC survival-window timers and survival-verdict events** — typed transitions on Falsification Commitments. State machine: `FC-declared → opposing-side-running → verdict-rendered (survived | refuted | inconclusive | budget-exhausted) → survival-window-open → window-expired → re-falsification-required`. The timer half is load-bearing in a way U-A's re-entry registrar is not: the registrar must wake up dependent-FC graphs when a parent's `survival-window` expires, flagging every downstream artifact that depended on the expired verdict. Subscribers: the compounding gate (which refuses to compound past-window artifacts), the independence auditor (which monitors verdict-distribution drift), the FC store (which marks expired FCs for re-run). See [D7-U-1 §1 primitive 5](../bias-guards/phase-3/d7-blind-axis/d7-u-1-prohibit-interval-escrow.md#1-architecture-sketch).

## Corpus-why citation (per variant)

- **U-A.** Solves [OQ-B3](../tracks/unified-A.md#oq-b3-human-re-entry-mechanism) — the corpus has no canonical primitive for human re-entry into an automated cycle. Anchored on [report 30 §5 / Kahana Cognitive Escrow](../../../research/30-cognitive-escrow.md) (interval-as-design-site) and [report 31 §5 / AILCCP](../../../research/31-caremark-rsi-board-exposure.md) (Human-Approval-Gate as substrate control). Without this primitive, re-entry collapses to ad-hoc operator interruption — the corpus' F42 / F53 failure mode.
- **D7-U-1.** Solves [open question §7.3 — survival-window calibration](../bias-guards/phase-3/d7-blind-axis/d7-u-1-prohibit-interval-escrow.md#7-open-questions). Anchored on [Tournament / kevin-carl cross-model patterns (report 34 §6.2)](../../../research/34-lenny-howiai-personal-harnesses.md), the [F1/F27/F46/F48 correlated-error cascade](../failure-modes-v3.md#f46--single-model-review-blindspot), and the architecture's structural answer to F53 (the substrate, not voluntary discipline, refuses to compound past-window FCs).

## Research-grade-uncertainty flag

**None.** Temporal (and the alternates) are production-grade workflow / event-stream engines with well-understood semantics for typed events + deterministic transitions + timer-driven subscriptions. The Phase-5 ADR work is integration design (schema, transition rules, subscriber discovery), not invention.

## Buildability verdict

**`designed-system`.** Construction is a wiring exercise over an existing production-grade workflow engine; per-variant schemas + state machines + subscriber catalogs are the design content. No same-vs-distinct verdict between U-A and D7-U-1 variants — deferred to Phase 4.2.
