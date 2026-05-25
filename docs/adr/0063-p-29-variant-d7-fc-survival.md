# ADR 0063: D7-U-1 P-29 variant — FC-survival policy DSL

- **Status**: Accepted
- **Date**: 2026-05-25
- **Deciders**: Wave 5.3c2 subagent

## Context

[ADR 0030](./0030-p-29-policy-mediator.md) accepted P-29 as a shared declarative policy-mediator framework (OPA + Rego primary; Cedar alternate) and explicitly deferred the per-variant policy DSL vocabularies to Wave 5.3. The [Phase-4.2 overlap verdict on P-29](../../architectures/v3/primitives/overlap.md#p-29-policy-mediator--compounding-gate--three-contested-variants) recorded three variants sharing the engine but differing at the predicate-vocabulary level:

| Variant | Candidate | Policy DSL | Closure axis |
|---|---|---|---|
| Interval-closure | U-A | Rego/Cedar; closure conditions per `EscrowInterval.policies` slots | Per-interval slot satisfaction |
| Per-layer-boundary | U-B | Rego; per Lᵢ→Lᵢ₊₁ closure encoding upstream layer's `escrow-policy` | Per-layer-pair boundary |
| FC-survival | D7-U-1 | Rego/Cedar; FC-survival vocabulary on `verdict.outcome ∈ {survived, conditionally-survived-with-window}` | FC ledger walk |

This ADR fixes the D7-U-1 (FC-survival) policy DSL. The [D7-U-1 substrate-requirements summary § P-29](../../architectures/v3/substrate-requirements/d7-u-1.md) and the [P-29 sketch § D7-U-1 compounding gate](../../architectures/v3/primitives/P-29-policy-mediator.md) specify the contract: artifact A is available as input to a downstream artifact B only if A's matching FalsificationCommitment has `verdict.outcome ∈ {survived, conditionally-survived-with-window}` AND (when conditionally) the current cycle is still inside the declared `survival-window`. The policy walks ledger entries (loaded as `data.fc_ledger`) and returns `allow` only on a survived-FC match.

The vocabulary axis is therefore **the FC ledger walk**, not an interval (U-A) and not a layer pair (U-B). The DSL must (a) consume the FC envelope produced by P-28's D7-U-1 variant (ADR 0062 — sibling Wave 5.3c2 decision on the canonical FC-envelope schema), (b) traverse the chain of FC envelopes from the upstream-artifact handle through any antecedent FCs, and (c) interact with the survival-window state machine from ADR 0064 (sibling — D7-U-1's P-30 survival-window registrar) when `verdict.outcome == conditionally-survived-with-window`.

## Decision

**Encode D7-U-1's P-29 vocabulary as a Rego policy bundle layered on the ADR 0030 mediator, with a single load-bearing predicate-family `fc_survival(fc_id, ledger)` and a top-level `allow` rule that walks the FC envelope chain.**

Concrete shape:

```rego
package p29.d7.fc_survival

# Top-level — the boundary primitive evaluates `allow` against this rule.
# `input.upstream_artifact.fc_id` names the FC matching the upstream artifact;
# `data.fc_ledger` is the loaded chain of P-28-D7 FC envelopes (ADR 0062).
allow {
    fc_survival(input.upstream_artifact.fc_id, data.fc_ledger)
}

# Survived outright — terminal `allow`.
fc_survival(fc_id, ledger) {
    fc := ledger[fc_id]
    fc.verdict.outcome == "survived"
}

# Conditionally survived — the survival-window registrar (ADR 0064) must
# still report the window open at input.cycle.
fc_survival(fc_id, ledger) {
    fc := ledger[fc_id]
    fc.verdict.outcome == "conditionally-survived-with-window"
    window_open(fc.survival_window, input.cycle)
}

window_open(window, cycle) {
    cycle >= window.opened_at_cycle
    cycle < window.expires_at_cycle
    not window.invalidated_by_refalsification
}
```

The bundle is content-addressed and loaded through ADR 0030's bundle-API contract. The verdict's `reasons[]` entries are typed `{fc_id: <handle>, outcome: <verdict>, window_state: <open|expired|invalidated|null>}` so that handback routing — to either the opposing-side router (P-33) for re-falsification or the survival-window registrar (ADR 0064) for cycle-bound retries — is mechanical.

**Input contract.** The mediator's `input` document carries the upstream-artifact handle (with its `fc_id` field), the candidate downstream-artifact handle, and the current `cycle` index. `data.fc_ledger` is loaded from the P-28 FC-envelope store per [ADR 0062's canonical-serialisation rule](./0029-p-28-typed-object-store.md). The policy is not responsible for ledger construction or envelope validation — both are upstream P-28 responsibilities.

**Survival-window interaction.** When `verdict.outcome == conditionally-survived-with-window`, the policy reads the `survival_window` sub-record but does NOT drive its state machine. State transitions (`window-open → window-expired` on cycle-boundary; `window-open → invalidated` on P-33 re-falsification) are owned by the timer-driven registrar of ADR 0064. The policy is a pure read against the registrar's current state.

**Vocabulary vs catalog.** The two `verdict.outcome` enum values (`survived`, `conditionally-survived-with-window`) are the fixed vocabulary. New verdict outcomes require a new ADR — they are NOT catalog extensions. This is the inverse of U-B's open boundary-check catalog: D7-U-1's vocabulary axis is closed at the verdict-enum level by design.

## Alternatives considered

**B. Adopt U-A's interval-closure DSL.** Reuse `EscrowInterval.policies` slot satisfaction as the predicate vocabulary. *Why rejected:* D7-U-1 has no interval primitive — its closure axis per the [overlap table](../../architectures/v3/primitives/overlap.md#p-29-policy-mediator--compounding-gate--three-contested-variants) is the FC ledger walk, and survival semantics live on the FC envelope (ADR 0062). Forcing interval vocabulary would synthesize fake intervals around each FC — ceremony without semantic gain — and lose the FC chain traversal compounding-gate enforcement depends on.

**C. Adopt U-B's per-layer-boundary DSL.** Reuse `(parent_layer, child_layer)` closure rules. *Why rejected:* D7-U-1's substrate is FC-graph-shaped, not layer-shaped — a single layer can produce many artifacts each with its own FC. Forcing layer-pair vocabulary would collapse the per-artifact granularity that [F53](../../architectures/v3/failure-modes-v3.md#f53--voluntary-discipline-fragility-kahana-fragile-dependency-class) and D-4 holdout-discipline mitigation requires.

Both alternatives share the engine per ADR 0030, so the cost of "wrong vocabulary" is not engine cost but the cost of policy text that does not match the substrate's actual closure axis — with downstream consequences for handback routing (P-33 re-falsification vs P-30 window-expiry).

## Consequences

**Easier:** FC-graph audit is mechanical — `reasons[].fc_id` names the FC the candidate must return to for re-falsification, and `reasons[].window_state` distinguishes "re-run opposing side" (P-33) from "wait for next cycle" (ADR 0064 timer). The fixed two-value vocabulary keeps the policy text auditable by non-engine-experts. Patrol's deny-on-stale-state contract folds in for free at the bundle-API layer per ADR 0030.

**Harder:** The policy depends on three sibling decisions staying coherent — ADR 0062 (FC envelope shape), ADR 0064 (survival-window state machine), and ADR 0030 (bundle-API). Any change to the FC envelope's `verdict.outcome` enum or `survival_window` sub-record forces a coordinated bundle update. The ledger-walk evaluator must be bounded — deeply chained FCs are a cost concern that the bundle-API's `bundle.evaluation_budget` field caps per call.

**Scope boundary.** This ADR fixes only D7-U-1's P-29 vocabulary. U-A (ADR 0052) and U-B (ADR 0056) vocabularies are separate; the engine and bundle-API contract are owned by ADR 0030. Survival-window timer semantics are owned by sibling ADR 0064. FC envelope schema is owned by sibling ADR 0062.

## References

- [ADR 0030: P-29 policy mediator substrate framework](./0030-p-29-policy-mediator.md) — parent, engine + bundle-API contract
- [ADR 0052: U-A P-29 variant — interval-policy DSL](./0052-p-29-variant-u-a-interval-policy.md) and [ADR 0056: U-B P-29 variant — layer-boundary policy DSL](./0056-p-29-variant-u-b-layer-boundary.md) — sibling per-variant vocabularies
- [Phase-4.2 overlap verdict on P-29 three contested variants](../../architectures/v3/primitives/overlap.md#p-29-policy-mediator--compounding-gate--three-contested-variants) — verbatim text-pull of the FC-survival row
- [D7-U-1 substrate-requirements summary § P-29](../../architectures/v3/substrate-requirements/d7-u-1.md) — FC-survival contract and ledger-walk semantics
- [P-29 buildability sketch § D7-U-1 compounding gate](../../architectures/v3/primitives/P-29-policy-mediator.md) — FC-survival vocabulary prior art (Rego ledger walk; survival-window expiry interaction with P-33 re-falsification)
- [D7-U-1 §1 substrate primitive #3](../../architectures/v3/bias-guards/phase-3/d7-blind-axis/d7-u-1-prohibit-interval-escrow.md#1-architecture-sketch) — compounding-gate corpus origin
- [F53 voluntary-discipline fragility](../../architectures/v3/failure-modes-v3.md#f53--voluntary-discipline-fragility-kahana-fragile-dependency-class) — forcing failure mode the FC-survival DSL keeps structural
