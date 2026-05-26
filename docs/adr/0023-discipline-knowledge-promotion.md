# ADR 0023: Discipline — knowledge promotion

- **Status**: Accepted
- **Date**: 2026-05-25
- **Deciders**: lead agent (Phase 5 Wave 5.2 fanout)

## Context

Long-running agentic cycles emit a large volume of per-cycle outputs — scenarios authored under pressure, invariants asserted by the methodology layer, RSI declarations, judge evidence, and post-hoc insights / playbooks / corrections / patterns (Compound-Knowledge's four-way typing, [followup 11](../../architectures/v3/disciplines/knowledge-promotion.md#corpus-motivation)). Most of these outputs are reversible cycle-local artifacts; a minority describe behavior the next cycle should rely on.

Without an explicit promotion gate, two failure modes accumulate: **F8 (stale-knowledge inversion)** — durable storage filling with provisional content that future cycles cite as authoritative — and **F55 (behavioural drift / self-reference loop)** — methodology evolving against its own un-vetted prior outputs. Both are catalogued in [failure-modes-v3.md](../../architectures/v3/failure-modes-v3.md). The [disciplines index](../../architectures/v3/disciplines/index.md) names knowledge-promotion as one of the 21 canonical disciplines; the per-discipline write-up at [`disciplines/knowledge-promotion.md`](../../architectures/v3/disciplines/knowledge-promotion.md) catalogues how every track (GF-M, BF-S, BF-M, U-B, U-C, GF-C) already names it under different shapes — *promote-or-reverse*, pace-layer promotion (project doc → Skill → enforced standard), graduation protocol from Cold-Start to Steady-State.

Knowledge-promotion sits *between* substrate primitives that store promoted knowledge — [P-08 scenario storage](../../architectures/v3/primitives/cluster-C3.md) (out-of-tree, holdout-partitioned) and [P-18 RSI declaration ledger](../../architectures/v3/primitives/P-18-rsi-declaration-ledger.md) (GF-C-specific) — and the methodology layer that decides which cycle outputs cross the gate.

## Decision

**The knowledge-promotion discipline binds every methodology to (a) declare which per-cycle outputs are candidates for promotion to durable storage — minimally: scenarios, invariants, RSI declarations, and judge evidence; (b) describe the promotion gate as a conjunction of typed checks — cross-model judge agreement on the artifact's claim, [cost-ceiling](./0020-discipline-cost-ceiling.md) compliance for the work that produced it, and [holdout-replay](../../architectures/v3/disciplines/holdout.md) PASS where the artifact would affect future judge calls; and (c) name the substrate primitive that receives each promoted class — P-08 for scenarios, P-18 for RSI declarations under GF-C, and per-candidate equivalents for invariants and evidence.**

Outputs that fail the gate are *reversed* (deleted, not amended) in GF-M's promote-or-reverse shape, or held in a `provisional` partition with `kw:confidence` tagging in tracks that carry both partitions (BF-M, U-B, U-C). Architecture-spec authors (Phase 6) write the per-candidate promotion-gate table; Phase-8 lean-evals MUST include at least one promotion-gate stress-test (a deliberately marginal artifact pushed at the gate to confirm rejection behavior).

## Alternatives considered

**B. Every cycle output goes to durable storage; rely on retrieval-time filtering.** *Why rejected:* this is the no-discipline baseline. F8 is the inevitable consequence — durable storage accumulates provisional content faster than retrieval-time filters can compensate, and the filter logic itself drifts because it is reading its own prior outputs (F55). Compound-Knowledge's four-way typing presumes promotion is upstream of storage, not a retrieval-time afterthought ([knowledge-promotion §Corpus motivation](../../architectures/v3/disciplines/knowledge-promotion.md#corpus-motivation)). Without a gate, signal-to-noise collapses within a small number of cycles.

**C. Operator-only promotion (every promotion is an explicit human approval).** *Why rejected:* operator-gated promotion is tractable at the scale of a few cycles per week (GF-C cold-start) but does not scale to BF-M / U-C steady-state cadences where dozens of candidates cross the promotion surface per cycle. U-C's anchor-edit work-unit shape ([unified-C.md](../../architectures/v3/tracks/unified-C.md) §5 step 2) already routes the load-bearing class — `anchor.kind=standards-rule` promotions — through L4 multi-author review with cooling-off windows; making *every* promotion operator-gated would either re-impose that cost on every typed promotion or force ad-hoc operator shortcuts that re-introduce F55.

## Consequences

**Easier:** Durable knowledge stores (P-08, P-18, per-candidate invariant stores) carry a known signal-to-noise floor enforced at write time. F8 and F55 have a defined defensive surface. Cross-cycle audit ("why was this scenario promoted?") resolves against the gate's typed checks, not narrative reconstruction. Methodology evolution under U-C's pace-layer promotion stays bounded — provisional patterns cannot leak into enforced standards without crossing all three gate components.

**Harder:** Each candidate's Phase-6 architecture spec carries an explicit promotion-gate table per output class. Marginal artifacts that fail the gate are *destroyed* in promote-or-reverse tracks (GF-M); methodologies that want a softer middle state ("hold for re-evaluation") need to allocate a `provisional` partition explicitly and accept that the partition is not load-bearing.

**Explicitly NOT promising:** A single canonical promotion-gate formula. Per-candidate gate composition varies (GF-C Cold-Start promotes graduation-of-work-unit-class via P-18; GF-M promotes intent+scenario pairs via P-08; U-C promotes patterns into `standards-rule` anchors). The discipline mandates the *shape* (typed conjunction; substrate-named recipient; reversal-or-quarantine on failure), not the per-axis weights.

## References

- [Knowledge-promotion discipline write-up](../../architectures/v3/disciplines/knowledge-promotion.md)
- [Disciplines index](../../architectures/v3/disciplines/index.md)
- [P-08 scenario storage primitive sketch](../../architectures/v3/primitives/cluster-C3.md)
- [P-18 RSI declaration ledger primitive sketch](../../architectures/v3/primitives/P-18-rsi-declaration-ledger.md)
- [Failure modes v3 (F8, F55)](../../architectures/v3/failure-modes-v3.md)
- [ADR 0020: cost-ceiling discipline](./0020-discipline-cost-ceiling.md) — gate-component dependency
- [Holdout discipline write-up](../../architectures/v3/disciplines/holdout.md) — gate-component dependency
- [GF-M promote-or-reverse phase-4 gate](../../architectures/v3/tracks/greenfield-methodology-first.md)
- [U-C pace-layer pattern → standards-rule promotion](../../architectures/v3/tracks/unified-C.md)
- [auto-005 Round 2 Phase-5 dispatch shape](../../architectures/v3/decisions/auto-005-phase-5-dispatch-shape.md) — Wave-5.2 dispatch authorizing this ADR.
