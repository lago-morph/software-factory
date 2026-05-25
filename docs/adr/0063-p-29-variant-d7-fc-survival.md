# ADR 0063: D7-U-1 P-29 variant — FC-survival policy DSL

- **Status**: Accepted
- **Date**: 2026-05-25
- **Deciders**: Wave 5.3c2 subagent

## Context

This is a **variant ADR** of the [P-29 policy-mediator common framework (ADR 0030)](0030-p-29-policy-mediator.md). ADR 0030 ships the shared substrate (OPA Rego primary, Cedar alternate; content-addressed bundles; binding `allow / reasons[] / obligations[] / audit_envelope` verdict). This ADR specifies the **policy DSL vocabulary** D7-U-1 loads onto that mediator — deferred from Wave 5.1b to Wave 5.3 per [auto-005 Round 2](../../architectures/v3/decisions/auto-005-phase-5-dispatch-shape.md#decision-round-2).

The [Phase-4.2 overlap verdict on P-29's three contested variants](../../architectures/v3/primitives/overlap.md#p-29-policy-mediator--compounding-gate--three-contested-variants) is verbatim:

> **Verdict: SAME primitive (P-29 policy mediator framework), DISTINCT policy DSLs.** All three share the underlying engine (OPA Rego primary; Cedar alternate path per [P-29 sketch](../../architectures/v3/primitives/P-29-policy-mediator.md)). The policy vocabulary differs: U-A reasons about interval-slot satisfaction; U-B reasons about layer-pair closure; D7-U-1 reasons about FC-survival windows. The differences are at the *predicate vocabulary* level, not the *engine* level.

The overlap.md row for D7-U-1 names the DSL **"Rego/Cedar; FC-survival vocabulary on `verdict.outcome ∈ {survived, conditionally-survived-with-window}`"** with closure axis **"FC ledger walk"**. D7-U-1's substrate-requirements [§ P-29 compounding gate](../../architectures/v3/substrate-requirements/d7-u-1.md) states the load-bearing rule: *artifact A is available to artifact B iff A's matching FC has `verdict.outcome ∈ {survived, conditionally-survived-with-window}` AND (when conditionally) the cycle is inside the declared `survival-window`*. The policy walks ledger entries (loaded as `data.fc_ledger`) and returns `allow` only on a survived-FC match — D7-U-1's structural replacement for voluntary review ([F53](../../architectures/v3/failure-modes-v3.md#f53--voluntary-discipline-fragility-kahana-fragile-dependency-class)) and D-4 holdout discipline at every artifact boundary ([F28](../../architectures/v3/failure-modes-v3.md#f28--holdout-leakage--acceptance-criteria-seen-by-builders)).

The DSL consumes the FC envelope shape specified by [ADR 0062 (D7-U-1 P-28 variant — FC envelope)](0062-p-28-variant-d7-fc-envelope.md) and interacts with the survival-window state machine specified by [ADR 0064 (D7-U-1 P-30 variant — survival-window registrar)](0064-p-30-variant-d7-survival-window.md).

## Decision

**Adopt a Rego policy bundle in the `d7_u_1` namespace of the [ADR 0030](0030-p-29-policy-mediator.md) mediator with the core predicate `fc_survival(fc_id)` as the closure-condition vocabulary.** The bundle declares a top-level rule `allow_compound[artifact_b]` invoked by any boundary primitive about to expose an upstream artifact A to a downstream artifact B; the rule conjoins survived-FC checks over the FC graph for A by walking `data.fc_ledger` — the chain of FC envelopes from [ADR 0062](0062-p-28-variant-d7-fc-envelope.md) loaded into the policy `data` document via the bundle's data-source binding.

Rule shape:

```rego
package d7_u_1

# Survival predicate: an FC has survived iff its verdict outcome is survived,
# or it is conditionally-survived-with-window and the current cycle is inside
# the declared survival-window.
fc_survival(fc_id) {
    fc := data.fc_ledger[fc_id]
    fc.verdict.outcome == "survived"
}

fc_survival(fc_id) {
    fc := data.fc_ledger[fc_id]
    fc.verdict.outcome == "conditionally-survived-with-window"
    now := time.now_ns()
    now <= fc.verdict.survival_window.expires_at_ns
}

# Ledger walk: artifact A is gate-eligible iff every FC declared about A has
# survived, AND every upstream FC the ledger references has survived.
artifact_survival(artifact_id) {
    fcs := [fc_id | fc := data.fc_ledger[fc_id]; fc.artifact == artifact_id]
    count(fcs) > 0
    every fc_id in fcs { fc_survival(fc_id) }
    every fc_id in fcs {
        every up_id in data.fc_ledger[fc_id].ledger.upstream_fcs {
            fc_survival(up_id)
        }
    }
}

allow_compound[artifact_b] {
    input.boundary == "compounding-gate"
    artifact_b := input.downstream_artifact
    every up_id in input.upstream_artifacts { artifact_survival(up_id) }
}
```

**Boundary contract.** The compounding-gate boundary primitive serialises `{boundary: "compounding-gate", downstream_artifact, upstream_artifacts[]}` as the mediator `input`, calls `data.d7_u_1.allow_compound`, and refuses the write on any `allow == false`. `reasons[]` enumerates failing upstream FCs (`fc_id`, `outcome`, and on conditional-survival the window expiry). The bundle hash is captured in `audit_envelope` per ADR 0030.

**Conditional-survival window interaction.** When an FC has `verdict.outcome == "conditionally-survived-with-window"`, the policy admits compounding **only** while the cycle is inside `verdict.survival-window`. The [P-30 D7-U-1 survival-window registrar (ADR 0064)](0064-p-30-variant-d7-survival-window.md) emits a `window-expired` event; the policy needs no separate predicate for expiry — the `time.now_ns() <= expires_at_ns` clause fails after the deadline. On expiry, the registrar cascades `re-falsification-required` to dependent FCs; downstream boundary checks then deny until a fresh refutation attempt yields a new `survived` verdict.

**Ledger-walk semantics.** `data.fc_ledger` is loaded from the [ADR 0062 FC envelope store](0062-p-28-variant-d7-fc-envelope.md) under `refs/notes/falsification-commitment` (libgit2 path) or `envelope_kind = 'falsification-commitment'` rows (Postgres path) via the bundle's data-source binding. The recursive walk over `ledger.upstream_fcs` is bounded by the FC graph's depth (corpus-unmeasured per D7-U-1 OQ-2); Rego's incremental evaluation memoises `fc_survival` per `fc_id` within a pass.

## Alternatives considered

**B. Interval-policy vocabulary (U-A's variant).** Encode closure as `interval-slot-satisfaction(interval_id, slot_name)` over an `EscrowInterval.policies` slot set. *Why rejected:* D7-U-1's substrate has no escrow-interval handoff — its boundary checks compounding of *one artifact's FC graph* against *another artifact's FC graph*, not slot satisfaction at an interval-close. Importing U-A's vocabulary would force D7-U-1 to invent an interval-and-slot decomposition for every compounding boundary, erasing the falsification-commitment indirection ([ADR 0062](0062-p-28-variant-d7-fc-envelope.md)) that makes survived-FC enforcement work. Preserved as [ADR 0052](0052-p-29-variant-u-a-interval-policy.md), rejected here.

**C. Layer-boundary vocabulary (U-B's variant).** Encode closure as per-Lᵢ→Lᵢ₊₁ layer-pair predicates reading the upstream layer's `escrow-policy` block. *Why rejected:* D7-U-1's substrate is not layered — every artifact carries its own FC graph regardless of pace layer, and the closure axis is the **FC ledger walk**, not layer-pair traversal. A layer-pair encoding has nowhere to place the survival-window timer and would erase the timer-driven re-falsification cascade that is D7-U-1's load-bearing structural property per [d7-u-1.md § P-30](../../architectures/v3/substrate-requirements/d7-u-1.md). Preserved as [ADR 0056](0056-p-29-variant-u-b-layer-boundary.md), rejected here.

## Consequences

**Easier.** Survived-FC compounding becomes a structural property of every artifact-exposing boundary, not an operator discipline — F53 closed at substrate. The same Rego bundle handles both `survived` and `conditionally-survived-with-window` via one `time.now_ns()` comparison. FC-graph traversal is queryable along its natural axis (`artifact-kind × verdict.outcome` per [ADR 0062](0062-p-28-variant-d7-fc-envelope.md)) via `data.fc_ledger`. Bundle-hash drift across deployments is Patrol-monitorable per ADR 0030.

**Harder.** The bundle's `data.fc_ledger` binding must stay in lockstep with the FC envelope schema (ADR 0062) — a `verdict.outcome` enum bump forces a Rego rule bump here, and version mismatch is a deny condition caught at bundle-build via Rego compilation against the schema. FC-graph traversal cost at high parallelism (D7-U-1 OQ-2) is corpus-unmeasured and carries to Phase-8 lean-eval. Authors need Rego fluency plus the FC-survival mental model.

**Explicitly NOT promising.** Survival-window expiry duration defaults (Phase-6 deployment config), the Cedar-equivalent rule set (deferred to Cedar deployments per ADR 0030), and `opposing-side` independence-evidence thresholds (consumed by [P-34 independence auditor (ADR 0061)](0061-p-34-independence-auditor.md), not this DSL) are out of scope.

## References

- [ADR 0030: P-29 policy mediator framework](0030-p-29-policy-mediator.md) — PARENT common ADR; engine substrate, bundle-API, and audit-envelope contract this variant plugs into
- [Phase-4.2 overlap verdict on P-29 three contested variants](../../architectures/v3/primitives/overlap.md#p-29-policy-mediator--compounding-gate--three-contested-variants) — `SAME primitive, DISTINCT policy DSLs` verdict and the FC-survival row this ADR instantiates
- [D7-U-1 substrate-requirements § P-29 compounding gate](../../architectures/v3/substrate-requirements/d7-u-1.md) — FC-survival vocabulary, ledger-walk semantics, conditional-survival window interaction
- [P-29 buildability sketch — D7-U-1 compounding gate](../../architectures/v3/primitives/P-29-policy-mediator.md) — engine choice corpus citation and `designed-system` buildability verdict
- [ADR 0062: D7-U-1 P-28 variant — FC envelope](0062-p-28-variant-d7-fc-envelope.md) — envelope shape this DSL consumes; chain of FC envelopes walked by `data.fc_ledger`
- [ADR 0064: D7-U-1 P-30 variant — survival-window registrar](0064-p-30-variant-d7-survival-window.md) — sibling ADR; timer cascade that drives re-falsification on window expiry
- [ADR 0052: U-A P-29 variant — interval-policy DSL](0052-p-29-variant-u-a-interval-policy.md), [ADR 0056: U-B P-29 variant — layer-boundary DSL](0056-p-29-variant-u-b-layer-boundary.md) — sibling variant ADRs (rejected vocabularies here)
- [F53 voluntary-discipline fragility](../../architectures/v3/failure-modes-v3.md#f53--voluntary-discipline-fragility-kahana-fragile-dependency-class), [F28 holdout leakage](../../architectures/v3/failure-modes-v3.md#f28--holdout-leakage--acceptance-criteria-seen-by-builders) — forcing failure modes
- [auto-005 Round 2 Phase-5 dispatch shape](../../architectures/v3/decisions/auto-005-phase-5-dispatch-shape.md#decision-round-2) — Wave-5.3 per-variant ADR scope
