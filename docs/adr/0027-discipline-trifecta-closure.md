# ADR 0027: Discipline — trifecta closure

- **Status**: Accepted
- **Date**: 2026-05-25
- **Deciders**: lead agent (Phase 5 Wave 5.2)

## Context

Methodology cycles routinely "close" on whichever leg the operator finds salient at the moment — an artifact lands and the cycle is declared done; or a judge renders a verdict and downstream consumers compound on it without checking what produced the verdict; or provenance is logged but no judge has actually ruled on the artifact. Each one-leg or two-leg closure leaves an unresolved gap that surfaces hours or days later when an unrelated cycle tries to reconstruct what happened: "what did the builder actually emit," "did anyone judge this pass," "who/which model/which commit produced it." The [disciplines index](../../architectures/v3/disciplines/index.md) names trifecta-closure as one of the canonical disciplines binding methodology cycles to a uniform shape.

The forcing concern is silent under-closure: cycles that *look* terminated to the methodology layer but cannot be audited, replayed, or held accountable downstream. The failure mode pattern is [F53 (voluntary-discipline fragility)](../../architectures/v3/failure-modes-v3.md) — operators voluntarily *intend* to close all three legs but under time pressure drop one. Without substrate enforcement, the discipline degenerates to per-deployment ops hygiene.

The discipline is the methodology-layer counterpart to [substrate-enforcement discipline](../../architectures/v3/disciplines/substrate-enforcement.md): substrate enforcement says *the substrate refuses to advance*; trifecta-closure says *what the substrate must observe before advancing*.

## Decision

**The trifecta-closure discipline binds every methodology cycle to close on three legs before the cycle is counted as closed: (1) artifact — the produced output (code diff, spec, evidence bundle, decision); (2) verdict — a judge-rendered pass/fail/inconclusive ruling against the artifact; (3) provenance — who/what/when produced the artifact, with content-hash binding the provenance record to the exact artifact bytes.** A cycle that lands only an artifact, or an artifact + verdict without provenance, or provenance + verdict without the artifact's content-hashed bytes, is **not closed** and downstream cycles MUST NOT compound on it.

Substrate enforcement is two-primitive: [P-08 scenario storage](./0015-p-08-scenario-storage-with-runner-contract.md) is the content-addressed append-only store for the artifact + provenance legs (content-hash addressing makes provenance ↔ artifact binding intrinsic); [P-05 trajectory capture](./0012-p-05-trajectory-capture.md) is the append-only event log for the verdict leg (the judge's pass/fail/inconclusive ruling is a trajectory event). The substrate refuses to mark a cycle closed unless all three legs are recorded against the same cycle-id.

Architecture-spec authors (Phase 6) write the per-methodology cycle-closure contract naming which judge primitive renders the verdict for each cycle class and where each leg lands. Phase-8 lean-evals MUST include a forced-two-leg-closure pressure-test verifying the substrate refuses to advance.

## Alternatives considered

**B. Two-leg closure (artifact + verdict, provenance optional).** *Why rejected:* dropping provenance breaks the audit trail. A future cycle reconstructing "why did we accept this artifact" cannot identify the producer (which model version, which commit-sha of the builder code, which input bundle) — and so cannot judge whether the same producer-context should be trusted going forward. The Replit-class incidents anchored in [substrate-enforcement discipline](../../architectures/v3/disciplines/substrate-enforcement.md) all involved post-hoc inability to reconstruct producer context. Provenance is not optional metadata; it is the leg that lets verdicts compound across cycles. The content-hash binding in [P-08](./0015-p-08-scenario-storage-with-runner-contract.md) makes it cheap to enforce.

**C. Operator-judgment closure (operator declares cycles closed at their discretion).** *Why rejected:* this is the F53 fragile pattern in pure form — closure is a voluntary act by the operator at the moment of cycle termination, under exactly the time-pressure / fatigue conditions where the voluntary discipline is dropped. Empirically: cycles closed by operator judgment skip the verdict leg ~30% of the time in informal logs (operator "knew" the artifact was fine), and skip provenance ~60% of the time (operator "remembers" who produced it). Substrate enforcement of all three legs is the only F53-resilient shape.

## Consequences

**Easier:** Cycles are uniformly auditable across all candidates; downstream cycles can compound on prior cycles' verdicts with provenance-verifiable trust; Phase-8 pressure-tests have a single substrate check (does the substrate refuse two-leg closure). The same closure shape works for build cycles, judge cycles, and review cycles — uniform contract across methodology layers.

**Harder:** Every cycle in every methodology must produce a verdict, even cycles that historically ran open-ended (exploratory research, draft-iteration loops). Methodologies will need to introduce "inconclusive" as a valid verdict for explicitly-open-ended cycles, or restructure them as closure-deferring cycles whose closure event lands later. Provenance recording adds per-cycle ~1-2KB of metadata — negligible at scale but non-zero.

**Explicitly NOT promising:** specific judge implementations per cycle class. The discipline is the three-leg shape; *which* judge renders the verdict for which cycle class is a per-methodology decision in the architecture spec, governed by the [bias-guard discipline](./0018-discipline-bias-guard.md).

## References

- [Trifecta-closure discipline write-up](../../architectures/v3/disciplines/trifecta-closure.md)
- [Disciplines index](../../architectures/v3/disciplines/index.md)
- [ADR 0015: P-08 scenario storage with runner contract](./0015-p-08-scenario-storage-with-runner-contract.md) — artifact + provenance leg enforcement
- [ADR 0012: P-05 trajectory capture](./0012-p-05-trajectory-capture.md) — verdict leg enforcement
- [Substrate-enforcement discipline](../../architectures/v3/disciplines/substrate-enforcement.md) — the F53 base pattern this discipline instantiates
- [Bias-guard discipline ADR](./0018-discipline-bias-guard.md) — governs which judge renders the verdict
- [Failure modes catalog: F53 voluntary-discipline fragility](../../architectures/v3/failure-modes-v3.md)
