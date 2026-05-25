# ADR 0019: Discipline — cognitive escrow

- **Status**: Accepted
- **Date**: 2026-05-25
- **Deciders**: lead agent (Phase 5 Wave 5.2)

## Context

Cognitive escrow — the interval between when an instruction leaves human possession and when its consequences return — is named across the corpus (Kahana, Schillace's "Attention Firewall," Notion's standup pre-read) as a first-class design surface, not as latency to be minimised. The [per-discipline write-up](../../architectures/v3/disciplines/cognitive-escrow.md) catalogues five primitive escrow events (reflection-question, success-criterion articulation, similar-past surfacing, delegation-level confirmation, STIR cascade) and notes that the discipline operationalises [F42 (Cognitive-Escrow Negligence)](../../architectures/v3/failure-modes-v3.md) — one of two convergence-clusters that span both mandates.

The placement question — substrate-typed primitive vs methodology-layer pattern — was bound by [DEC-2](../../architectures/v3/phase-3.4-decisions-resolved.md#dec-2--cognitive-escrow-placement-methodology): **METHODOLOGY**. DEC-2's rationale: substrate support is composable from primitives the substrate already provides for other purposes — trajectory capture ([P-05](../../architectures/v3/primitives/cluster-C2.md)), event registration ([P-30](../../architectures/v3/primitives/P-30-event-registrar.md)), watchdog and alerting — so substrate-typing an `EscrowSurface` slot is overkill. The discipline binds the *methodology* to declare which cycles produce escrow events and what the attention-surface contract is; the substrate enforces only the underlying event/trajectory primitives.

Without this discipline, escrow degenerates to per-methodology ad-hoc surfaces — exactly the [F53 voluntary-discipline fragility](../../architectures/v3/failure-modes-v3.md) failure mode the discipline is meant to structurally close.

## Decision

**The cognitive-escrow discipline binds every methodology that names operator-attention surfaces (currently GF-M, GF-C, and U-* candidates carrying the discipline) to declare three things:**

1. **Which methodology cycles produce escrow events.** The methodology spec MUST name, per cycle / phase / gate-boundary, whether that transition is an escrow interval and which of the five primitive event-types fires.
2. **The attention-surface contract.** Each declared event-type carries a typed envelope (cycle-id, methodology-phase, event-class, evidence pointer into [P-05 trajectory](../../architectures/v3/primitives/cluster-C2.md)), a severity class, and an `operator-acknowledgement-required` vs `informational` bit. The contract is methodology-authored; the envelope shape is substrate-typed via [P-30 event registrar](../../architectures/v3/primitives/P-30-event-registrar.md).
3. **The substrate primitive binding.** Each declared escrow event MUST bind to [P-30 event registrar](../../architectures/v3/primitives/P-30-event-registrar.md) for surfacing and to [P-05 trajectory store](../../architectures/v3/primitives/cluster-C2.md) for the evidence trail. No methodology may invent a parallel attention channel that bypasses P-30/P-05.

Phase-6 architecture-spec authors write the per-methodology escrow declaration table. Phase-8 lean-evals MUST include at least one operator-attention pressure-test per candidate that carries the discipline (verifying acknowledgement-required events block cycle progression structurally, not voluntarily).

This discipline is METHODOLOGY-LAYER per DEC-2: no shared substrate `EscrowSurface` slot exists; each candidate composes its escrow surface from P-30 + P-05 + its own methodology-spec declarations.

## Alternatives considered

**B. Cognitive-escrow as substrate primitive (typed `EscrowSurface` slot).** *Why rejected:* bound by [DEC-2](../../architectures/v3/phase-3.4-decisions-resolved.md#dec-2--cognitive-escrow-placement-methodology). Substrate-typing the attention surface would force every candidate (including those that reject escrow at substrate, e.g., [D7-U-1](../../architectures/v3/bias-guards/phase-3/d7-blind-axis/d7-u-1-prohibit-interval-escrow.md)) to carry the slot, and the corpus convergence does not warrant that imposition — the substrate already provides P-30 and P-05 for any methodology that wants to compose escrow from them. DEC-2 names this rationale explicitly.

**C. Ad-hoc per-methodology escrow surfaces (no shared discipline).** *Why rejected:* each methodology re-invents reflection-prompt envelopes, severity classes, and acknowledgement semantics — exactly the [F53 voluntary-discipline fragility](../../architectures/v3/failure-modes-v3.md) class that the discipline is supposed to close. Without a shared contract, ops cannot write a uniform escalation runbook across methodologies, and Phase-8 lean-evals cannot pressure-test the surface uniformly. The discipline shape (declare cycles + envelope + binding) is the minimum shared structure that avoids re-invention without forcing substrate typing.

## Consequences

**Easier:** Uniform attention-surface contract across candidates that carry the discipline; ops gets a single escalation runbook shape (typed envelope + severity + acknowledgement bit). Phase-8 lean-evals have a defined pressure-test surface (does an acknowledgement-required event structurally block progression?). Evidence trail is uniform — every escrow event lands in [P-05](../../architectures/v3/primitives/cluster-C2.md) keyed by P-30 event-id.

**Harder:** Each candidate's Phase-6 architecture spec carries an explicit per-cycle escrow declaration table — non-trivial authoring work. Methodologies that resist quantifying escrow points (U-C's `inferable` rating, BF-M's stage-8-only escrow) must either name the declaration explicitly or accept the F42 risk in their architecture spec.

**Explicitly NOT promising:** that substrate-fired escrow events make the operator engage with them. [U-B §7 OQ-PLEF-5](../../architectures/v3/tracks/unified-B.md) flags this honestly: the discipline ensures the surface fires structurally, but operator engagement with the surface is itself voluntary. F53 has a stronger reading than this discipline addresses, and that gap is preserved in the candidate set (D7-U-1 carries the opposing-side topology as the F53-strong-reading sibling). The discipline closes F42 at the *substrate-surfacing* layer; F53 closure remains a candidate-level question.

## References

- [Cognitive-escrow discipline write-up](../../architectures/v3/disciplines/cognitive-escrow.md)
- [Disciplines index](../../architectures/v3/disciplines/index.md)
- [DEC-2 cognitive-escrow placement: METHODOLOGY](../../architectures/v3/phase-3.4-decisions-resolved.md#dec-2--cognitive-escrow-placement-methodology)
- [P-30 event registrar primitive sketch](../../architectures/v3/primitives/P-30-event-registrar.md)
- [P-05 trajectory capture (cluster C2)](../../architectures/v3/primitives/cluster-C2.md)
- [F42 / F53 failure modes](../../architectures/v3/failure-modes-v3.md)
- [D7-U-1 prohibit-interval-escrow blind-axis track](../../architectures/v3/bias-guards/phase-3/d7-blind-axis/d7-u-1-prohibit-interval-escrow.md)
- [auto-005 Round 2 Phase-5 dispatch shape](../../architectures/v3/decisions/auto-005-phase-5-dispatch-shape.md) — this ADR is a Wave-5.2 deliverable.
