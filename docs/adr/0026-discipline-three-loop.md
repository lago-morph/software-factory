# ADR 0026: Discipline — three-loop

- **Status**: Accepted
- **Date**: 2026-05-25
- **Deciders**: lead agent (Phase 5 Wave 5.2 fanout)

## Context

Several v3 candidates operate methodology layers at fundamentally different cadences over the same durable artifact. The [disciplines index](../../architectures/v3/disciplines/index.md) names three-loop as a canonical discipline; the per-discipline write-up at [`disciplines/three-loop.md`](../../architectures/v3/disciplines/three-loop.md) names three loops over a single durable model: **per-cycle** (the immediate execution loop a methodology drives each call), **per-session** (the operator-facing trajectory loop spanning a working session), and **per-codebase** (the long-running drift / maintenance loop that reconciles model with reality over weeks).

The forcing concern is that without a shared cadence-binding discipline, methodologies that operate at one cadence cannot be evidence-compared against methodologies that operate at another. [BF-L](../../architectures/v3/tracks/brownfield-legacy-ingestion-first.md) needs per-codebase ingestion + maintenance to be first-class loops, not stage-costs hidden inside per-cycle accounting. [GF-M's reversibility regime](../../architectures/v3/tracks/greenfield-methodology-first.md) needs per-cycle promote/reverse separated from per-session paraphrase scaling. [U-B's pace-layered factory](../../architectures/v3/tracks/unified-B.md) treats each pace layer as a loop cadence. F20 (maintenance-vs-greenfield asymmetry, brownfield-critical) and F34 (cross-layer drift) in [failure-modes-v3.md](../../architectures/v3/failure-modes-v3.md) name the failures when loop cadence is collapsed; UC4 ("analyzing what is there and growing it") in [constraints-extracted.md](../../architectures/v3/constraints-extracted.md) names the work that requires the slow loop to exist at all.

## Decision

**The three-loop discipline binds every methodology that operates at more than one cadence to declare three loops — per-cycle, per-session, per-codebase — and, for each loop, to declare its substrate touchpoints, escalation policy on stall/breach, and evidence-retention horizon.** Loops share a single durable artifact (the codebase model, the trajectory store, the methodology's own state); they do not share cost ceilings, judge profiles, or watchdog cadences. A methodology that genuinely runs at a single cadence (greenfield cold-start before any codebase exists) declares the other two loops as `silent` with a rationale, rather than omitting them.

Loop boundaries are part of the architecture spec (Phase 6). Phase-8 lean-evals MUST exercise at least one cross-loop interaction per candidate (e.g. per-cycle change triggering per-codebase maintenance re-index) so the loop boundary contract is pressure-tested rather than asserted.

## Alternatives considered

**B. Single-loop default — methodologies operate at one cadence and treat slower work as stage-cost inside that cadence.** *Why rejected:* this is what [BF-S](../../architectures/v3/tracks/brownfield-substrate-first.md) and [BF-M](../../architectures/v3/tracks/brownfield-methodology-first.md) do today (legacy-ingestion folded into S-1..S-4 substrate setup or into stage-2 comprehension). It works when the slow loop is genuinely one-time, but it cannot represent BF-L's per-codebase maintenance loop (continuous, low-cadence, reconciling model with code drift) in the same cadence as per-cycle work — the cost-ceiling and watchdog profiles required for each are incompatible. Single-loop forces the slow loop to be amortised into per-cycle math, hiding F34 drift cost and making cross-methodology evidence comparison impossible when one candidate amortises and another does not.

**C. Ad-hoc loop boundaries per methodology — each candidate names whatever loops it needs without a shared discipline.** *Why rejected:* this is the pre-discipline status quo. Without a shared three-loop frame, Phase-8 lean-evals cannot compare candidates on the same loop axis: BF-L's "maintenance loop" and U-B's "pace-layer L4" might be the same thing or might be incommensurable, and reviewers cannot tell. The discipline exists precisely to make per-cadence substrate touchpoints, escalation, and evidence retention comparable across candidates that organize work differently.

## Consequences

**Easier:** Cross-methodology evidence comparison on a shared cadence frame; Phase-8 lean-evals have a defined cross-loop interaction surface; BF-L's maintenance loop and U-B's pace layers can be evaluated on the same axes without translation. Candidates that pre-declare cross-loop interactions (BF-L per-codebase reindex on per-cycle commit; GF-M paraphrase-scaling at per-session) surface their cost-stacking math at architecture-spec time.

**Harder:** Each candidate's architecture spec must declare three loops with their substrate touchpoints — non-trivial authoring work in Phase 6, especially for candidates that genuinely run at one cadence and must justify two `silent` declarations. Methodologies whose loop boundaries are fuzzy (operator-judgment-heavy cycles that span session and codebase) need to pick a primary loop and name the fuzziness explicitly.

**Explicitly NOT promising:** specific loop cadences (per-cycle = "every call" vs "every commit", per-codebase = "weekly" vs "on declared trigger"). The discipline is a contract shape; cadence values are per-deployment and live in the architecture spec. See [three-loop §open-questions](../../architectures/v3/disciplines/three-loop.md) on the empirical anchor for maintenance-loop cadence.

## References

- [Three-loop discipline write-up](../../architectures/v3/disciplines/three-loop.md)
- [Disciplines index](../../architectures/v3/disciplines/index.md)
- [BF-L brownfield-legacy-ingestion-first track](../../architectures/v3/tracks/brownfield-legacy-ingestion-first.md)
- [GF-M greenfield-methodology-first track](../../architectures/v3/tracks/greenfield-methodology-first.md)
- [U-B unified-B pace-layered factory track](../../architectures/v3/tracks/unified-B.md)
- [Failure modes v3 — F20, F34, F55, F57](../../architectures/v3/failure-modes-v3.md)
- [UC4 in constraints-extracted](../../architectures/v3/constraints-extracted.md)
- [ADR 0020: Discipline — cost ceiling](./0020-discipline-cost-ceiling.md) — Wave-5.2 exemplar
