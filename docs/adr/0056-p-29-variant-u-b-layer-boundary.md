# ADR 0056: U-B P-29 variant — layer-boundary policy DSL

- **Status**: Accepted
- **Date**: 2026-05-25
- **Deciders**: Wave 5.3c1 subagent

## Context

[ADR 0030](./0030-p-29-policy-mediator.md) accepted P-29 as a shared declarative policy-mediator framework (OPA + Rego primary; Cedar alternate) and explicitly deferred the per-variant policy DSL vocabularies to Wave 5.3. The [Phase-4.2 overlap verdict on P-29](../../architectures/v3/primitives/overlap.md#p-29-policy-mediator--compounding-gate--three-contested-variants) recorded three variants sharing the engine but differing at the predicate-vocabulary level:

| Variant | Candidate | Policy DSL | Closure axis |
|---|---|---|---|
| Interval-closure | U-A | Rego/Cedar; closure conditions per `EscrowInterval.policies` slots | Per-interval slot satisfaction |
| Per-layer-boundary | U-B | Rego; per Lᵢ→Lᵢ₊₁ closure encoding upstream layer's `escrow-policy` | Per-layer-pair boundary |
| FC-survival | D7-U-1 | Rego/Cedar; FC-survival vocabulary on `verdict.outcome` | FC ledger walk |

This ADR fixes the U-B (per-layer-boundary) policy DSL. The [U-B substrate-requirements summary § P-29](../../architectures/v3/substrate-requirements/u-b.md) describes the contract: for each Lᵢ → Lᵢ₊₁ pair (L0 Standards → L1 Architecture, L1 → L2 Spec, L2 → L3 Plan, L3 → L4 Code), the Rego policy encodes the upstream layer's `escrow-policy` field as a closure condition. The downstream-layer object cannot materialize until the upstream's declared boundary checks have satisfying records — cost-ceiling per D-5; holdout-discipline per D-4 at L3→L4; cross-family contradiction-detection at L2→L3; AILCCP delegation-level confirmation at L0→L1 and L1→L2.

The vocabulary axis is therefore **the layer pair**, not an interval (U-A) and not an FC ledger walk (D7-U-1). The DSL must (a) consume the layer-typed envelope produced by P-28's U-B variant (ADR 0055 — sibling Wave 5.3c1 decision on the `TypedObject<L>` envelope), (b) extract the upstream layer's `escrow-policy` field, and (c) produce a verdict whose `reasons[]` reference the failed boundary check by layer-pair plus check-id so Patrol and the calling primitive can route handbacks to the correct upstream layer.

## Decision

**Encode U-B's P-29 vocabulary as a Rego policy bundle layered on the ADR 0030 mediator, with a single load-bearing predicate-family `layer_pair_closure(parent_layer, child_layer, escrow_policy)` and one rule per `(parent_layer, child_layer)` pair.**

Concrete shape:

```rego
package p29.ub.layer_pair_closure

# Top-level entry — the boundary primitive evaluates `allow` against this rule.
allow {
    input.envelope.kind == "TypedObject"
    layer_pair_closure(input.envelope.parent_layer,
                       input.envelope.child_layer,
                       input.envelope.parent_escrow_policy)
}

# One rule per declared layer-pair. Each rule unpacks the upstream
# escrow-policy and checks all declared boundary records are satisfied.
layer_pair_closure("L3", "L4", policy) {
    holdout_discipline_satisfied(policy.holdout_records, input.candidate)
    cost_ceiling_satisfied(policy.cost_ceiling, input.candidate.cost_estimate)
}

layer_pair_closure("L2", "L3", policy) {
    contradiction_detection_satisfied(policy.cross_family_checks, input.candidate)
    cost_ceiling_satisfied(policy.cost_ceiling, input.candidate.cost_estimate)
}

layer_pair_closure("L1", "L2", policy) { ailccp_delegation_confirmed(policy, input.candidate) }
layer_pair_closure("L0", "L1", policy) { ailccp_delegation_confirmed(policy, input.candidate) }
```

The bundle is content-addressed and loaded through ADR 0030's bundle-API contract. The verdict's `reasons[]` entries are typed `{layer_pair: "Lᵢ→Lᵢ₊₁", check_id: <id>, upstream_record_ref: <handle>}` so handback routing is mechanical. The bundle exposes `bundle.l0_standards.version` per ADR 0030 so the L0→L1 rule can hard-fail on standards-version mismatch.

**Input contract.** The mediator's `input` document carries the [ADR 0055 layer-typed envelope](./0055-p-28-variant-u-b-layer-typed-envelope.md) verbatim. The U-B DSL relies on the envelope's `parent_layer`, `child_layer`, and `parent_escrow_policy` fields being populated by P-28 before the gate is called — the policy is not responsible for envelope construction.

**Boundary-check catalog vs vocabulary.** Each boundary check (`holdout_discipline_satisfied`, `cost_ceiling_satisfied`, etc.) is its own Rego rule with a stable name. New boundary checks are additions to the catalog — not changes to the layer-pair vocabulary. The vocabulary axis (the layer pair) is fixed at four pairs for U-B's five-layer ontology; the catalog is open.

## Alternatives considered

**B. Adopt U-A's interval-closure DSL.** Reuse `EscrowInterval.policies` slot satisfaction as the predicate vocabulary. *Why rejected:* U-B has no interval primitive — its closure axis per the [Phase-4.2 overlap table](../../architectures/v3/primitives/overlap.md#p-29-policy-mediator--compounding-gate--three-contested-variants) is the layer pair, and the upstream `escrow-policy` field lives on the layer-typed envelope (ADR 0055), not on an interval object. Forcing interval vocabulary on U-B would require synthesizing fake intervals around each layer boundary — pure ceremony, with no semantic gain, and it would break P-31's per-layer-pair invariant catalog which reads the same `(parent_layer, child_layer)` key.

**C. Adopt D7-U-1's FC-survival DSL.** Reuse `verdict.outcome ∈ {survived, conditionally-survived-with-window}` as the predicate vocabulary. *Why rejected:* FC-survival reasons over an FC ledger walk per the overlap table; U-B has no FC ledger. The boundary checks U-B needs (cost-ceiling, holdout-discipline, contradiction-detection, AILCCP delegation) are not survival windows — they are closure conditions on layer-pair traversal. Forcing FC vocabulary would lose the layer-pair routing that handback depends on.

Both alternatives share the engine per ADR 0030, so the cost of "wrong vocabulary" is not engine cost — it is the cost of policy text that does not match the substrate's actual closure axis, with downstream consequences for handback routing and the P-31 invariant catalog.

## Consequences

**Easier:** Per-layer-pair handback is mechanical — `reasons[].layer_pair` names the upstream layer the candidate must return to. P-31's per-layer-pair invariant catalog and the policy bundle share one `(parent_layer, child_layer)` key, so a drift event and a deny verdict are co-indexable for free. New boundary checks land as catalog additions without DSL churn.

**Harder:** Four layer-pair rules must stay in sync with the upstream `escrow-policy` field shape. Layer-count migration (e.g. adding an L2.5 spec-refinement layer) requires a new layer-pair rule plus updates to ADR 0055's envelope schema — handled by the layer-count migration ADR seed cited in U-B § Open carries.

**Scope boundary.** This ADR fixes only U-B's P-29 vocabulary. U-A and D7-U-1 vocabularies are separate Wave 5.3 ADRs; the engine and bundle-API contract are owned by ADR 0030.

## References

- [ADR 0030: P-29 policy mediator substrate framework](./0030-p-29-policy-mediator.md) — parent, engine + bundle-API contract
- [ADR 0029: P-28 typed-object-store substrate framework](./0029-p-28-typed-object-store.md) — envelope-store substrate that ADR 0055 specializes for U-B
- [Phase-4.2 overlap verdict on P-29 three contested variants](../../architectures/v3/primitives/overlap.md#p-29-policy-mediator--compounding-gate--three-contested-variants) — verbatim text-pull of the per-layer-boundary row
- [U-B substrate-requirements summary § P-29](../../architectures/v3/substrate-requirements/u-b.md) — boundary-check catalog and per-layer-pair contract
- [P-29 buildability sketch](../../architectures/v3/primitives/P-29-policy-mediator.md) — engine prior art (OPA + Rego primary; Cedar alternate)
- [F53 voluntary-discipline fragility](../../architectures/v3/failure-modes-v3.md#f53--voluntary-discipline-fragility-kahana-fragile-dependency-class) — forcing failure mode the per-layer-boundary DSL keeps structural
