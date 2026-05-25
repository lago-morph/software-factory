# ADR 0038: GF-S P-15 four-guard mediator

- **Status**: Accepted
- **Date**: 2026-05-25
- **Deciders**: Wave 5.3a subagent (GF-S orphan ADR)

## Context

[GF-S §1.S8](../../architectures/v3/substrate-requirements/gf-s.md) names the **four-guard mediator** as the single substrate surface through which spec-and-intent inputs pass before a builder agent sees them. The [P-15 buildability sketch](../../architectures/v3/primitives/P-15-four-guard-mediator.md) verdicts the primitive `designed-system` and fixes the four guards: (1) GtWR vocabulary lint (INCOSE R7/R8/R9/R26/R35 rule pack), (2) contradiction-detector ensemble across model families, (3) requirement-count budgeter (Yang/Llama ≤10–20 ceiling), (4) CaMeL-class perimeter typing on spec-derived tool-call edges.

The forcing failure modes are clustered: [F36 instruction-following ceiling](../../architectures/v3/failure-modes-v3.md#f36--instruction-following-ceiling) (req-count), [F37 silent contradictory-prompt collapse](../../architectures/v3/failure-modes-v3.md#f37--silent-contradictory-prompt-collapse) (contradictions), [F38 vocabulary lint debt](../../architectures/v3/failure-modes-v3.md#f38--vocabulary-lint-debt) (GtWR), the [F12 / F33 / F44 lethal-trifecta cascade](../../architectures/v3/failure-modes-v3.md#f12--lethal-trifecta--prompt-injection) (perimeter), and — crucially for the *composition* itself — [F52 tempting-wrong-hybrid](../../architectures/v3/failure-modes-v3.md#f52) (the "just one more guard" anti-pattern) jointly with [F51 Ashby-deficient probabilistic guard](../../architectures/v3/failure-modes-v3.md). No single guard discharges the cluster; agent-discipline composition would be [F53-fragile](../../architectures/v3/failure-modes-v3.md).

The four substrate primitives required to assemble the mediator are already accepted: [ADR 0032 P-12 deterministic linter framework](0032-p-12-deterministic-linter-framework.md), [ADR 0011 P-02 cost ceilings](0011-p-02-cost-ceilings.md), [ADR 0014 P-07 telemetry ingestor](0014-p-07-telemetry-ingestor.md), [ADR 0016 P-14 judge router](0016-p-14-judge-router.md), and [ADR 0033 P-25 CaMeL perimeter](0033-p-25-camel-perimeter.md). What this ADR fixes is the *composition mediator* — how the four guards present one fail-closed gate decision per cycle.

## Decision

**Build P-15 as a composition mediator that hosts four typed guards behind one fail-closed gate, with per-guard substrate dependencies fixed as follows.** Guard 1 (GtWR lint) instantiates a [P-12](0032-p-12-deterministic-linter-framework.md) `Linter` loaded with the P-16 EARS+GtWR rule pack; the mediator calls `Linter.verify(specText, ruleSet)` per intent block. Guard 2 (contradiction-detector) is a 3-of-N family-diverse ensemble dispatched through the [P-14 judge router](0016-p-14-judge-router.md) configured for the contradiction-detection role; PASS requires ≥3 family-distinct judges concurring contradiction-free, with a three-valued PASS / FAIL / UNDETERMINED sub-verdict when ensemble agreement is below quorum. Guard 3 (req-count budgeter) is a deterministic [P-12](0032-p-12-deterministic-linter-framework.md) rule walking the parsed spec AST, with thresholds drawn from the cycle manifest as a [P-02 cost-ceiling](0011-p-02-cost-ceilings.md) class — req-count is a budget axis sharing the substrate's per-cycle budget enforcement plumbing. Guard 4 (perimeter typing) is the declaration-time CaMeL check that the [P-25 runtime perimeter](0033-p-25-camel-perimeter.md) re-enforces at call-time.

**Composition rule:** AND across guards, fail-closed by default. The mediator emits one typed envelope `{gtwr, contradiction, req-count, perimeter}` to [P-07 telemetry](0014-p-07-telemetry-ingestor.md) on **every** gate decision — PASS envelopes are auditable, not just FAILs. Perimeter-typing emits an extra capability-edge trace consumed by P-07's lethal-trifecta detectors. The UNDETERMINED contradiction sub-verdict may be escalated to Patrol per cycle-manifest configuration rather than hard-failing.

**Four guards, full stop.** Per [GF-S §3 contract](../../architectures/v3/substrate-requirements/gf-s.md#3-candidate-specific-contracts-on-each-primitive) the substrate refuses a fifth guard at this surface (the [F52](../../architectures/v3/failure-modes-v3.md#f52) anti-pattern). Methodology layers above the mediator may chain additional checks; the substrate itself does not accrete.

## Alternatives considered

**B. Monolithic LLM-judge replacing all four guards.** A single strong model asked to evaluate the spec across all four dimensions (vocabulary, contradictions, requirement load, capability boundary). *Why rejected:* (i) non-deterministic on guards 1 and 3, defeating the GtWR-lint and req-count-budget purposes — both are deterministic-detectable per the [P-15 sketch §Corpus-why citation](../../architectures/v3/primitives/P-15-four-guard-mediator.md#corpus-why-citation) and demanding LLM judgement on them imports [F37](../../architectures/v3/failure-modes-v3.md#f37--silent-contradictory-prompt-collapse)-class drift onto checks that have a hard right answer; (ii) inherits Larbi's single-judge MCC ≤ 0.55 ceiling on the contradiction dimension where the ensemble premise was the mitigation; (iii) collapses the typed sub-verdict envelope into one opaque bit, breaking P-07's per-guard telemetry and removing the auditability that makes the gate review-worthy.

**C. Pure deterministic linter only (drop the contradiction-detector ensemble).** Keep guards 1, 3, 4; eliminate guard 2 on the grounds that LLM-judging is itself the Ashby-deficient guard ([F51](../../architectures/v3/failure-modes-v3.md)) the substrate is supposed to avoid. *Why rejected:* [F37 silent contradictory-prompt collapse](../../architectures/v3/failure-modes-v3.md#f37--silent-contradictory-prompt-collapse) is greenfield-`critical` and *not* deterministic-detectable — contradiction between two natural-language requirements requires semantic judgement no AST visitor can supply. The mediator's mitigation is *ensemble-across-families* with the [F48 tacit-collusion](../../architectures/v3/failure-modes-v3.md#f48--tacit-collusion-via-shared-context) caveat held as partial-RG per [GF-S §2](../../architectures/v3/substrate-requirements/gf-s.md#2-rg-primitives), not abandonment. Dropping guard 2 leaves F37 unmitigated at the substrate layer.

## Consequences

**Easier:** Four substrate F-mode clusters discharge through one gate surface with one typed envelope, simplifying methodology-layer integration. P-07 sees per-guard telemetry without bespoke wiring. Adding a *fifth* gate is mechanically refused at the substrate boundary, blocking F52 accretion drift at design-review time, not at runtime.

**Harder:** Cost-stacking math on every-cycle four-guard evaluation (ensemble dispatch dominates) is owed at architecture-spec time per [GF-S §5 open carries](../../architectures/v3/substrate-requirements/gf-s.md#5-open-carries) — the [P-02 ceilings](0011-p-02-cost-ceilings.md) must be sized against guard 2's family-diverse fanout. Ensemble size N, family-rotation policy, and quorum threshold are first-class parameters Phase-8 lean-eval sweeps.

**Explicitly NOT promising:** Guard 2's effective MCC under N=3 / N=5 family-diverse ensembles. [GF-S §2](../../architectures/v3/substrate-requirements/gf-s.md#2-rg-primitives) accepts contradiction-detector reliability as partial-RG; this ADR fixes the *mediator composition*, not the empirical reliability of the ensemble premise. Phase-8 lean-eval owns the calibration.

## References

- [P-15 four-guard mediator buildability sketch](../../architectures/v3/primitives/P-15-four-guard-mediator.md) — canonical contract and per-guard construction path.
- [GF-S substrate-requirements §1.S8 and §3](../../architectures/v3/substrate-requirements/gf-s.md#3-candidate-specific-contracts-on-each-primitive) — claiming text and four-guards-full-stop contract.
- [ADR 0032: P-12 deterministic linter framework](0032-p-12-deterministic-linter-framework.md) — engine for guards 1 and 3.
- [ADR 0011: P-02 cost ceilings](0011-p-02-cost-ceilings.md) — budget plumbing reused by the req-count guard.
- [ADR 0014: P-07 telemetry ingestor](0014-p-07-telemetry-ingestor.md) — typed envelope sink.
- [ADR 0016: P-14 judge router](0016-p-14-judge-router.md) — ensemble dispatch for guard 2.
- [ADR 0033: P-25 CaMeL perimeter](0033-p-25-camel-perimeter.md) — call-time counterpart to guard 4's declaration-time check.
- [F37 silent contradictory-prompt collapse](../../architectures/v3/failure-modes-v3.md#f37--silent-contradictory-prompt-collapse), [F52 tempting-wrong-hybrid](../../architectures/v3/failure-modes-v3.md#f52) — forcing failure modes.
