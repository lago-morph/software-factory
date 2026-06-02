# ADR 0069: The spec–scenarios–system triangle as the evaluation invariant for unattended self-building

- **Status**: Accepted
- **Date**: 2026-06-02
- **Deciders**: jonathan@manton.com, autonomous-run session

## Context

The factory's defining goal is to build components **for itself, unattended**. The hard problem underneath that goal is not code generation — it is **trust without a human in every loop**. If the same agent that writes a component also writes the checks that certify it, the certification is self-referential: the agent grades its own homework, and "all tests pass" means nothing. This is the gaming failure that makes naive self-building unsafe.

The first Sweep-2 design of the evaluation tier under-modelled this. It treated the judge as a **scorer**: the judge produced a single `satisfaction_score`, a distribution was reduced from many such scores, and a go/no-go threshold was applied. That framing conflates four distinct failure sources — a wrong implementation, a wrong test, a wrong spec, and a wrong judge — into one opaque number. An opaque number cannot tell you *what to fix*, and a threshold on it cannot be trusted unless the judge itself is known-good, which a self-building system cannot self-certify.

The operator supplied the missing structure: every build is a **triangle of three representations that must be made to agree, with each edge verified by a different party and a different trust property**. This is the structural decomposition that lets the grading be independent and the failures be diagnosable — and that is precisely the precondition for running the factory without a human watching every build.

## Decision

Model every factory build as a triangle of three representations — **Spec (S)**, hold-out **Scenarios (H)**, and the implemented **System (I)** — joined by three edges, each with a distinct owner and trust property:

| Edge | Relationship that must hold | Owned / enforced by | Independent of the implementer? |
|---|---|---|---|
| **S ↔ H** | the scenarios correctly and completely describe the use of the system the spec describes | the **scenario builder working with the spec builder** | authoring-side (both) |
| **S ↔ I** | the system faithfully implements the spec | the system's **own** unit / integration / end-to-end tests | **No** — implementer-written, therefore gameable |
| **H ↔ I** | the hold-out scenarios pass against the system | the **judge**, evaluated independently | **Yes** — this is the anti-gaming check |

**The judge directly measures only the H ↔ I edge, and a failure there is a non-specific alarm.** The misalignment can be caused by a defect in *any* corner:

- **judge** — incorrectly running scenarios or misinterpreting results;
- **spec** — ambiguity, incompleteness, contradictions;
- **scenarios** — incompleteness, misrepresentation, ambiguity, or contradiction *relative to the spec*;
- **system** — failure to meet the spec (and its own in-system tests being wrong for the same reasons).

The judge's job is therefore to **surface where the defect lives** (root-cause attribution across the four sources) and to inform the repair decision between two modes:

1. **Incremental fix** — converge the three representations in place (patch the spec ambiguity, the scenario, and/or the system), when the defect is localized; versus
2. **Discard and reimplement** — throw away the system, fix the spec and/or scenarios via the **independent authoring path**, and reimplement from the revised spec, when the defect is structural (the system faithfully built the *wrong* target, so patching it is futile).

**A component is complete only when all three edges align.** 100%-pass on the hold-out is *necessary but not sufficient*; the spec must be unambiguous and complete, the scenarios must correspond to it, and the system must satisfy both its own tests and the independent hold-out. The integration bar is therefore 100% hold-out pass **plus** the tri-alignment judgment **plus** human review — with the human-review and judge-trust oversight relaxing only as the judge earns calibrated trust, and the 100%-pass floor never lowering.

**The intent — why this is the load-bearing structure for an unattended factory:** the independence of the H ↔ I edge from the implementer is what safely removes the human from the inner loop. The implementer cannot both build the system and certify it against checks it controls; the hold-out, authored by a separate party and evaluated in a separate rig, is the only check it cannot game. The triangle separates *who builds* from *who checks*, and the judge's root-cause attribution converts an opaque pass/fail into an actionable, auditable repair route. Without the triangle, self-building verification is self-referential and the factory cannot be trusted to run unattended. With it, every build failure is independently detected and attributable to a specific representation — which is exactly what a human would otherwise have to do by hand on every build.

## Alternatives considered

**Single satisfaction score + threshold gate** (the initial Sweep-2 design). Rejected: it collapses four orthogonal defect sources into one number, so it cannot route a repair, and the threshold is only meaningful if the judge is trustworthy — a property a self-building system cannot self-certify. It also invites threshold-lowering as a release valve, which is the Goodhart path to shipping bad components.

**Implementer-written tests only (the S ↔ I edge alone).** Rejected: gameable by construction. An agent can write tests that its own code passes; "green" certifies nothing about correctness against an independent reading of the spec. The S ↔ I tests are kept (they are how the implementer enforces faithfulness locally), but they are explicitly *not* the trust boundary.

**Human review of every build.** Rejected: it defeats the unattended goal. Human review is retained as a gate during the trust-building phase and relaxes as the judge is calibrated, but it cannot be the per-build correctness mechanism at scale.

## Consequences

**Easier:** every evaluation failure becomes attributable and actionable (which representation is wrong, and whether to polish or rebuild); the anti-gaming property is structural rather than aspirational; the completion criterion is unambiguous (tri-alignment); and judge fallibility is made a first-class, named defect source rather than an unstated assumption.

**Harder / accepted trade-offs:** the judge must become a **diagnostician**, not just a scorer (richer output: root-cause attribution + repair recommendation). The factory needs an **independent spec-and-scenario authoring/correction path** that the implementing worker cannot drive (otherwise the "fix the spec" branch reintroduces gaming). The bootstrap loop gains a **repair router** (polish vs. discard-and-reimplement). Completion is stricter and therefore slower. And because the judge is itself a defect source, **judge calibration** (a human-audited sample before its verdicts are trusted) becomes a standing requirement, not optional polish.

**Explicitly not promising:** that the hold-out alone proves correctness (it does not — it proves H ↔ I agreement, which is only one edge), nor that any sub-100% hold-out result is ever acceptable for integration.

## References

- [`../../architectures/v4/_meta/HANDOFF.md`](../../architectures/v4/_meta/HANDOFF.md) — the §0′ implementation plan for encoding this principle into the eval-tier specs (mechanics + intent for the next session).
- [`../../architectures/v4/_meta/review-log.md`](../../architectures/v4/_meta/review-log.md) — the decision ledger; this ADR is recorded there as **D-42** (and refines D-15/D-38/D-39).
- [`../../architectures/v4/_meta/decisions/auto-002-c53-go-no-go-rule-shape.md`](../../architectures/v4/_meta/decisions/auto-002-c53-go-no-go-rule-shape.md) — the go/no-go rule-shape brief this principle reframes (the gate is one edge of the triangle).
- [`../../architectures/v4/spec/C32-judge-harness.md`](../../architectures/v4/spec/C32-judge-harness.md) — the judge, to be reframed from scorer to diagnostician.
- [`../../architectures/v4/spec/C30-scenario-store.md`](../../architectures/v4/spec/C30-scenario-store.md), [`../../architectures/v4/spec/C31-scenario-runner.md`](../../architectures/v4/spec/C31-scenario-runner.md), [`../../architectures/v4/spec/C33-satisfaction-metric.md`](../../architectures/v4/spec/C33-satisfaction-metric.md) — the rest of the H ↔ I evaluation tier.
- [`../../architectures/v4/spec/C34-holdout-integrity.md`](../../architectures/v4/spec/C34-holdout-integrity.md) — enforces the independence property that makes H ↔ I an anti-gaming check.
- [`../../architectures/v4/spec/C52-self-bootstrap.md`](../../architectures/v4/spec/C52-self-bootstrap.md), [`../../architectures/v4/spec/C53-bootstrap-validation.md`](../../architectures/v4/spec/C53-bootstrap-validation.md) — the bootstrap loop + go/no-go that gain the repair router and the tri-alignment completion criterion.
- [ADR-0021: holdout discipline](./0021-discipline-holdout.md) — the prior holdout-independence decision this principle builds on.
- [ADR-0043: intent-crucible validator](./0043-p-17-intent-crucible-validator.md) — the spec-validation component that anchors the independent spec-correction path.
