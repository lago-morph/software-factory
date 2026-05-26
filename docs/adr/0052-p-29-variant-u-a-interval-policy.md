# ADR 0052: U-A P-29 variant — interval-policy DSL

- **Status**: Accepted
- **Date**: 2026-05-25
- **Deciders**: lead agent (Phase 5 Wave 5.3c1 subagent)

## Context

This is a **variant ADR** of the [P-29 policy-mediator common framework (ADR 0030)](0030-p-29-policy-mediator.md). ADR 0030 ships the shared substrate (OPA Rego primary engine, Cedar alternate path; content-addressed policy bundles; binding `allow / reasons / obligations / audit_envelope` verdict contract); this ADR specifies the **policy DSL vocabulary** U-A loads onto that mediator — deferred from Wave 5.1b to Wave 5.3 per [auto-005 Round 2](../../architectures/v3/decisions/auto-005-phase-5-dispatch-shape.md#decision-round-2).

The [Phase-4.2 overlap verdict on P-29's three contested variants](../../architectures/v3/primitives/overlap.md#p-29-policy-mediator--compounding-gate--three-contested-variants) is verbatim:

> **Verdict: SAME primitive (P-29 policy mediator framework), DISTINCT policy DSLs.** All three share the underlying engine (OPA Rego primary; Cedar alternate path per [P-29 sketch](../../architectures/v3/primitives/P-29-policy-mediator.md)). The policy vocabulary differs: U-A reasons about interval-slot satisfaction; U-B reasons about layer-pair closure; D7-U-1 reasons about FC-survival windows. The differences are at the *predicate vocabulary* level, not the *engine* level.

U-A's claim per [substrate-requirements §3 policy DSL](../../architectures/v3/substrate-requirements/u-a.md#3-candidate-specific-contracts-on-each-primitive): closure conditions are expressed per `EscrowInterval.policies` slot — `gate`, `log`, `sandbox`, `approval-gate`, `reflection-trigger`, `judge-diversity` — and the closure axis is **per-interval slot satisfaction**: the mediator refuses to close the interval unless every declared slot has a satisfying upstream record. This consumes the interval envelope shape specified by [ADR 0051 (U-A P-28 variant — interval envelope)](0051-p-28-variant-u-a-interval-envelope.md).

Forcing failure modes: [F53 voluntary-discipline fragility](../../architectures/v3/failure-modes-v3.md#f53--voluntary-discipline-fragility-kahana-fragile-dependency-class) (without a declarative per-slot check the operator can skip slots under stress) and [F28 holdout leakage](../../architectures/v3/failure-modes-v3.md#f28--holdout-leakage--acceptance-criteria-seen-by-builders) (the `judge-diversity: different-family` slot must verify P-14's provider-family tag mechanically, not by convention).

## Decision

**Adopt a Rego policy bundle in the `u-a` namespace of the [ADR 0030](0030-p-29-policy-mediator.md) mediator with the core predicate `interval-slot-satisfaction(interval_id, slot_name)` as the closure-condition vocabulary.** The bundle declares one rule per known slot name; the boundary primitive (interval-close call) invokes a single top-level rule `allow_close[interval_id]` that conjoins satisfaction over the slot set declared in the interval envelope.

Rule shape:

```rego
interval-slot-satisfaction(interval_id, "gate") :-
    envelope := data.intervals[interval_id]
    gate_record := data.records.gates[interval_id]
    gate_record.verdict == "pass"
    gate_record.bundle_hash == envelope.policies.gate.expected_bundle_hash

interval-slot-satisfaction(interval_id, "judge-diversity") :-
    envelope := data.intervals[interval_id]
    envelope.policies["judge-diversity"] == "different-family"
    judge_record := data.records.judges[interval_id]
    count({f | f := judge_record.calls[_].provider_family}) >= 2

allow_close[interval_id] :-
    envelope := data.intervals[interval_id]
    every slot in envelope.policies {
        interval-slot-satisfaction(interval_id, slot)
    }
```

Six slot rules ship in v1 — `gate`, `log`, `sandbox`, `approval-gate`, `reflection-trigger`, `judge-diversity` — corresponding 1:1 to the slot names declared in [ADR 0051](0051-p-28-variant-u-a-interval-envelope.md)'s envelope schema. Adding a slot is a bundle-version bump (new Rego rule + envelope-schema bump in ADR 0051); removing a slot is a breaking change requiring a superseding ADR.

**Boundary contract.** The interval-close primitive serialises `{interval_envelope, slot_records[]}` as the mediator's `input`, calls `data.u_a.allow_close`, and refuses to close on any `allow == false`. `reasons[]` enumerates failing slots; `obligations[]` may direct re-runs (e.g. "re-evaluate gate after bundle hash X is re-loaded"); the bundle hash is captured in `audit_envelope` per ADR 0030.

**Re-entry interaction.** When [P-30 (ADR 0036)](0036-p-30-event-registrar-substrate.md) drives an interval into `re-entry-open`, the policy bundle re-evaluates against the post-re-entry slot records — the same `interval-slot-satisfaction` predicate, no separate vocabulary. `automation-eligibility` from [ADR 0050 (U-A P-19 variant — interval-kind features)](0050-p-19-variant-u-a-interval-kind.md) feeds the `approval-gate` slot's threshold via Rego data import, not via a separate engine.

## Alternatives considered

**B. Layer-boundary policy vocabulary (U-B's variant).** Encode closure as per-Lᵢ→Lᵢ₊₁ layer-pair predicates, reading the upstream layer's `escrow-policy` block. *Why rejected:* U-A's substrate has no layered pace-graph — its closure axis is per-`EscrowInterval` slot satisfaction, not per-layer-pair boundary. Importing U-B's vocabulary would force U-A to invent a layer assignment for every interval, an alien structure that erases the methodology bet U-A places on **intervals as the closure unit**. Per the overlap verdict's "DISTINCT policy DSLs" clause, this vocabulary is U-B's variant ADR's scope, not U-A's. The engine is shared (ADR 0030); the vocabulary is not.

**C. FC-survival policy vocabulary (D7-U-1's variant).** Encode closure as `verdict.outcome ∈ {survived, conditionally-survived-with-window}` walks over the FC ledger. *Why rejected:* U-A's substrate does not carry an FC ledger — its closure records are typed `EscrowInterval.policies` slot satisfactions, not falsifiable-claim survival verdicts. The FC-survival vocabulary presupposes a survival-window state machine ([D7-U-1's P-30 variant](../../architectures/v3/bias-guards/phase-3/d7-blind-axis/d7-u-1-prohibit-interval-escrow.md#1-architecture-sketch)) which U-A does not bind; re-using this vocabulary would collapse two of the three variants Phase-8 is meant to pressure-test against the shared engine. Reserved for D7-U-1's variant ADR.

## Consequences

**Easier.** Slot satisfaction becomes a structural property of the interval-close boundary, not an operator discipline (F53 closed). Adding a new slot is a Rego rule + envelope-schema bump, not a re-design of the mediator. Patrol can diff the bundle hash across deployments to detect F57-class drift. Re-entry re-evaluation reuses the same vocabulary, no second engine.

**Harder.** The interval envelope schema (ADR 0051) and this policy bundle co-evolve; out-of-sync schema/bundle pairs are a deny-condition (bundle-hash mismatch on the envelope's `expected_bundle_hash` field), which surfaces clearly but does require coordinated version bumps. Slot-record producers (P-06 watchdog, P-14 judge router, sandbox runtime) must each emit the typed record shape the Rego rules import; record-shape drift is detected by Rego compilation failures during bundle build, not at runtime. Authors need Rego fluency for the six core rules.

**Explicitly NOT promising.** This ADR does not specify cut-points for `automation-eligibility` thresholds (ADR 0050 + deployment config), the Cedar-equivalent rule set (deferred to deployments that choose Cedar per ADR 0030), or the bar-set parameter values feeding the `approval-gate` slot (Phase-6 deployment config).

## References

- [ADR 0030: P-29 policy mediator framework](0030-p-29-policy-mediator.md) — PARENT common ADR; engine substrate, bundle-API, and audit-envelope contract this variant plugs into
- [Phase-4.2 overlap verdict on P-29 three contested variants](../../architectures/v3/primitives/overlap.md#p-29-policy-mediator--compounding-gate--three-contested-variants) — `SAME primitive, DISTINCT policy DSLs` verdict and the three-row variant table
- [U-A substrate-requirements §3 policy DSL](../../architectures/v3/substrate-requirements/u-a.md#3-candidate-specific-contracts-on-each-primitive) — closure conditions per `EscrowInterval.policies` slots, per-interval slot satisfaction closure axis
- [P-29 buildability sketch](../../architectures/v3/primitives/P-29-policy-mediator.md) — engine choice corpus citation and `designed-system` buildability verdict
- [ADR 0051: U-A P-28 variant — interval envelope](0051-p-28-variant-u-a-interval-envelope.md) — envelope shape this DSL consumes (`EscrowInterval.policies` slot set)
- [ADR 0050: U-A P-19 variant — interval-kind features](0050-p-19-variant-u-a-interval-kind.md) — `automation-eligibility` source feeding the `approval-gate` slot
- [ADR 0036: P-30 event-registrar substrate](0036-p-30-event-registrar-substrate.md) — re-entry registrar driving re-evaluation of this bundle
- [F53 voluntary-discipline fragility](../../architectures/v3/failure-modes-v3.md#f53--voluntary-discipline-fragility-kahana-fragile-dependency-class), [F28 holdout leakage](../../architectures/v3/failure-modes-v3.md#f28--holdout-leakage--acceptance-criteria-seen-by-builders) — forcing failure modes
- [auto-005 Round 2 Phase-5 dispatch shape](../../architectures/v3/decisions/auto-005-phase-5-dispatch-shape.md#decision-round-2) — Wave-5.3 per-variant ADR scope
