# ADR 0061: D7-U-1 P-34 independence auditor

- **Status**: Accepted
- **Date**: 2026-05-25
- **Deciders**: lead agent (Phase 5 Wave 5.3c2 subagent — D7-U-1 orphan)

## Context

[D7-U-1 (Falsification-Topology Factory)](../../architectures/v3/bias-guards/phase-3/d7-blind-axis/d7-u-1-prohibit-interval-escrow.md) names [P-34 — independence auditor](../../architectures/v3/primitives/P-34-independence-auditor.md) as the substrate primitive that verifies an FC's opposing-side handler is genuinely independent of the builder. Without that verification, the falsification-topology stance collapses to declaration: ADR 0060's P-33 router can route to an opposing-side per the FC's declared `independence-evidence`, but if the declaration is wrong — same model family masked by a different provider, trajectory leakage from the builder's transcript, or population-vote subsets that overlap the builder's training set — every downstream `verdict.outcome == survived` is rubber-stamped, and the F1/F27/F46/F48 cascade reappears at the substrate layer that was supposed to close it. P-34 makes independence *measured rather than declared*.

D7-U-1 is the sole claimant of P-34 (orphan; see [d7-u-1.md §1](../../architectures/v3/substrate-requirements/d7-u-1.md#1-primitive-list-buildability-confirmed)). The [Phase-3.5 sketch](../../architectures/v3/primitives/P-34-independence-auditor.md) verdicts construction `designed-system` while flagging the structural recursion concern (OQ-1 "who audits the auditor") as research-grade-uncertainty; the [Phase-3.5.5 RG row](../../architectures/v3/substrate-requirements/d7-u-1.md#2-rg-primitives) routes that residual via the A+C hybrid (deterministic primary + human-of-record backstop). This ADR fixes the *per-FC closure-time* check; the patrol-tier distributional sweep described in the sketch is part of the same auditor pipeline at coarser cadence.

The forcing failure modes are [F27 (same model builds and validates)](../../architectures/v3/failure-modes-v3.md#f27--circularity--same-model-builds-and-validates), [F46 (single-model review blindspot)](../../architectures/v3/failure-modes-v3.md#f46--single-model-review-blindspot), and [F48 (tacit collusion via shared context)](../../architectures/v3/failure-modes-v3.md#f48--tacit-collusion-via-shared-context). Each names a distinct leakage axis (model-family, prior-trajectory, shared-population); a single-axis check misses the other two.

## Decision

**Build P-34 as a per-FC closure-time check, invoked by the [P-29 compounding gate](../../architectures/v3/primitives/P-29-policy-mediator.md) immediately before it writes `verdict.outcome` to the P-28 FC envelope, that reads the FC's `refutation-attempt` envelope and the builder's [P-05 trajectory](0012-p-05-trajectory-capture.md), runs a three-layer independence check, and emits an `IndependenceAuditFinding` event to the [P-30 event registrar](0036-p-30-event-registrar-substrate.md) keyed on the FC id.** The three layers are evaluated in order; any layer failing flips the FC's verdict from `survived` → `inconclusive (auditor-flagged: <layer>)` and queues the FC for the Option-C human-of-record reviewer.

1. **Model-family disjoint check.** The opposing-side handler's `(provider, model_family, model_snapshot)` triple is looked up in the [P-24 attribution store](0035-p-24-attribution-store.md) against every `factory_agent`-signed entry in the builder's trajectory window. Disjoint = no triple intersection on `model_family`, evaluated via the canonical [model-family taxonomy carried by P-14 / P-33](0016-p-14-judge-router.md). Provider-only difference is insufficient (same family, different reseller).
2. **Trajectory-overlap check.** The opposing-side handler's prior-context window is hashed against the builder's [P-05 trajectory](0012-p-05-trajectory-capture.md) for the same artifact and ancestors. Overlap is the fraction of input-token shingles (rolling 8-gram) shared. Threshold default `< 0.05`; tunable per `artifact-kind` in the auditor config but never disabled.
3. **Population-vote subset check.** When `opposing-side.kind == population-vote`, the declared voter-pool is checked against the builder's family-set: no voter shares `model_family` with the builder, and the pool's joint-distribution declared in `independence-evidence` covers all three of (family-disjoint, snapshot-distinct, training-window-distinct). A pool that is a proper subset of the builder's family set fails closed.

Each layer's pass/fail and the per-layer evidence (matched triples, overlap fraction, voter-pool intersection) are recorded inside the `IndependenceAuditFinding` envelope so the human-of-record can review distributions of findings per [d7-u-1.md §2 A+C hybrid](../../architectures/v3/substrate-requirements/d7-u-1.md#2-rg-primitives). The check is itself a deterministic scipy/sklearn-free function (set operations + rolling-hash + table lookup); its determinism is the Option-A assurance against recursion.

## Alternatives considered

**B. Trust-by-default — accept `independence-evidence` as declared, run no per-FC check, leave audit to the patrol-tier distributional sweep alone.** *Why rejected:* defeats the falsification-topology purpose. The patrol sweep operates at cycle-aggregation cadence, so a colluding judge-pair can rubber-stamp many FCs before any distributional signal trips. The whole point of D7-U-1 (per [D7-U-1 §2](../../architectures/v3/bias-guards/phase-3/d7-blind-axis/d7-u-1-prohibit-interval-escrow.md)) is that independence is *measured rather than declared*; per-FC closure is the measurement.

**C. Single-axis model-family check only.** *Why rejected:* closes F27 (same-family build+validate) but leaves F46 (single-model blindspot via trajectory-overlap — a different family fed the builder's transcript still inherits the builder's framing) and F48 (tacit collusion via shared-context — a population-vote pool that is a subset of the builder's family set) open. All three axes must be checked because each maps to a distinct corpus-named failure mode; closing one and not the others produces a substrate that the F1/F27/F46/F48 cascade can route around.

## Consequences

**Easier:** the [P-29 compounding gate](0030-p-29-policy-mediator.md) gets a substrate-enforced answer to "is this surviving FC trustworthy?" before exposing the artifact downstream. The auditor's findings feed the [P-30 event registrar](0036-p-30-event-registrar-substrate.md) so dependent-FC graphs can be re-falsified when an upstream FC is retroactively flagged. The Option-A deterministic-ness is real: the auditor shares no LLM distribution with the judges it audits.

**Harder:** per-FC closure adds latency to every compounding step (set-lookup + rolling-hash over the builder's trajectory window; bounded but non-zero). The thresholds (overlap `< 0.05`, training-window-distinct definition) are corpus-thin and will need [Phase-8 lean-eval calibration](../../architectures/v3/substrate-requirements/d7-u-1.md#5-open-carries) per D7-U-1 OQ-3. The Option-C human-of-record reviewer queue (per [d7-u-1.md §2](../../architectures/v3/substrate-requirements/d7-u-1.md#2-rg-primitives)) is an unfunded methodology-layer attention-design item.

**Explicitly NOT promising:** closure of the structural recursion residual. Per [P-34 sketch §"Auditor recursion engagement"](../../architectures/v3/primitives/P-34-independence-auditor.md#auditor-recursion-engagement-load-bearing-oq-1), [F51 (Ashby-deficient probabilistic guard)](../../architectures/v3/failure-modes-v3.md#f51--ashby-deficient-probabilistic-guard) against novel collusion patterns and the F42/F5 cognitive-ceiling surface re-introduced at the audit layer are accepted-open residuals. This ADR fixes only the per-FC closure-time check and its three layers; the recursion question remains research-grade-uncertainty.

## References

- [P-34 buildability sketch](../../architectures/v3/primitives/P-34-independence-auditor.md) — construction path, recursion engagement, falsifiability harness.
- [D7-U-1 substrate-requirements §1 + §2](../../architectures/v3/substrate-requirements/d7-u-1.md) — primitive list and A+C hybrid RG treatment.
- [D7-U-1 source artifact](../../architectures/v3/bias-guards/phase-3/d7-blind-axis/d7-u-1-prohibit-interval-escrow.md) — FC schema and falsification-topology mandate.
- [ADR 0012 — P-05 trajectory capture](0012-p-05-trajectory-capture.md) — trajectory substrate the auditor reads.
- [ADR 0035 — P-24 attribution store](0035-p-24-attribution-store.md) — attribution lookup for model-family disjoint check.
- [ADR 0036 — P-30 event registrar](0036-p-30-event-registrar-substrate.md) — event sink for `IndependenceAuditFinding`.
- [F27](../../architectures/v3/failure-modes-v3.md#f27--circularity--same-model-builds-and-validates) / [F46](../../architectures/v3/failure-modes-v3.md#f46--single-model-review-blindspot) / [F48](../../architectures/v3/failure-modes-v3.md#f48--tacit-collusion-via-shared-context) cascade — three axes mapped to three layers.
