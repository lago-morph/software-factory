# ADR 0022: Discipline — honesty

- **Status**: Accepted
- **Date**: 2026-05-25
- **Deciders**: lead agent (Phase 5 Wave 5.2 fanout)

## Context

Honesty / no-fabrication appears in the [disciplines index](../../architectures/v3/disciplines/index.md) as one of 21 canonical disciplines; the per-discipline write-up at [`disciplines/honesty.md`](../../architectures/v3/disciplines/honesty.md) names its surfaces — track §6 "what this track is NOT", §7 "open questions", the buildability + corpus-why two-part rule, and per-primitive RG (research-grade-uncertainty) flagging.

Three forcing concerns motivate substrate-binding rather than narrative-only treatment:

1. **RG-primitive disclosure.** [Phase-3.4 buildability rule](../../architectures/v3/phase-3.4-decisions-resolved.md#refined-two-part-rule-for-accepting-a-substrate-primitive) keeps primitives without a corpus-why out and flags research-grade construction paths. The [Phase-3.5.5 RG-primitive rule](../../architectures/v3/candidate-registry.md#phase-355-rule-on-load-bearing-rg-primitives-binding-user-approved-2026-05-25) (binding) then forces any candidate with a load-bearing RG primitive to *either* commit to a bounded authoring sub-track *or* downgrade dependent contract to accept-as-RG. The discipline is the contract that says "do not hide an RG dependency by silent assumption."
2. **Accepted-open concerns.** Every track's §6 / §7 sections concede gaps (e.g., [`GF-S §5.5`](../../architectures/v3/tracks/greenfield-substrate-first.md) on F40 last-mile drift; [`D7-U-1` "Honest assessment"](../../architectures/v3/bias-guards/phase-3/d7-blind-axis/d7-u-1-prohibit-interval-escrow.md) recommending *both* architectures be carried forward rather than choosing). Without the discipline, these concede-sections collapse to advocacy under selection pressure.
3. **Pre-Round-2 wave firing.** Per [`AGENTS-MD-ffe35aa500`](../../retrospective/2026-05-25-155/AGENTS-MD-ffe35aa500-honest-acknowledgements-pre-round-2-firing.md), when Round-1-authorized parallel waves fire concurrently with adversarial review, the Round-2 brief MUST emit an explicit "Round-2 honest acknowledgements" section naming the deviation, the mitigation, and whether re-dispatch is required.

Honesty is the *meta-discipline* preventing [F53 (voluntary-discipline fragility)](../../architectures/v3/failure-modes-v3.md#f53--voluntary-discipline-fragility-kahana-fragile-dependency-class) from self-camouflaging — i.e., a methodology silently weakening its own discipline-applications and reporting success.

## Decision

**The honesty discipline binds every methodology to three substrate-checkpointed obligations:** (a) explicitly mark RG-flagged primitives as such, with the Phase-3.5.5 bounded sub-track or accept-as-RG treatment chosen in the architecture spec, not deferred; (b) carry accepted-open concerns through to architecture-spec time as named open questions rather than papering them over in synthesis; (c) emit "Round-2 honest acknowledgements" sections in decision briefs when any wave fired pre-Round-2.

Substrate enforcement is **partial.** The trajectory store ([ADR 0012](./0012-p-05-trajectory-capture.md), P-05) records the audit trail that makes (c) reconstructable post-hoc — every dispatch, review-return, and amendment timestamps into the per-cycle event log. The [decision-brief-adversarial-review-lifecycle skill](../../retrospective/2026-05-25-155/SKILL-SPEC-34dd1d0274-decision-brief-adversarial-review-lifecycle.md) encodes the Round-2 honest-acknowledgements checkpoint mechanically. (a) and (b) remain process-level — authored at architecture-spec time, enforceable only by adversarial review.

Architecture-spec authors (Phase 6) declare each candidate's RG-primitive treatment. Decision-brief authors at any phase invoke the lifecycle skill, which forces the acknowledgements section when applicable.

## Alternatives considered

**B. Optimistic-reporting default (no honesty binding).** *Why rejected:* this is methodology self-camouflage — the failure mode F53 names. A methodology that under-reports its RG dependencies and accepted-open concerns reads as more mature than one that names them; under selection pressure, candidates competing on optimistic-reporting drive honest ones out. The discipline's purpose is to inoculate the methodology layer against this dynamic. See [`disciplines/honesty.md`](../../architectures/v3/disciplines/honesty.md) and the [F53 write-up](../../architectures/v3/failure-modes-v3.md#f53--voluntary-discipline-fragility-kahana-fragile-dependency-class).

**C. Ad-hoc honesty in narrative only (no substrate-checkpoint).** *Why rejected:* not enforceable. Every track currently uses §6 / §7 narrative honesty (per [`disciplines/honesty.md` Named-by](../../architectures/v3/disciplines/honesty.md#named-by)); the question this ADR settles is whether *any* checkpoint binds the methodology to keep doing it. Without (a) the Phase-3.5.5 RG-rule binding architecture-spec content, (b) the trajectory-store audit trail anchoring acknowledgements to actual session timeline, and (c) the lifecycle skill mechanically requiring the section, the narrative pattern is a convention with no enforcement surface — the textbook F53 shape.

## Consequences

**Easier:** RG dependencies surface at Phase-4-entry (when the Phase-3.5.5 rule fires) rather than at first deployment. Decision-brief audit trails are reconstructable from the trajectory store: a future reader can determine which waves fired pre-Round-2 and whether the Round-2 amendments were applied. Adversarial reviewers (per [`AGENTS.md` real-subagent rule](../../AGENTS.md#adversarial-review-must-be-real-subagents)) have a named surface to attack — "where is the honest-acknowledgements section?" is now a structured question.

**Harder:** Architecture-spec authoring must carry explicit RG-treatment declarations (a Phase-3.5.5 obligation now binding at Phase-6 spec-write time). Decision-brief lifecycle ships heavier — the lifecycle skill's nine-step checklist (including the acknowledgements step) replaces the looser "Round 1 → reviewers → Round 2" shape.

**Explicitly NOT promising:** full substrate enforcement of (a) and (b). The architecture-spec content (RG-treatment declarations, named open questions) is authored by methodology layer; the substrate records *that* the spec was authored, not whether the content is honest. Adversarial review is the only real check on the content's honesty; F53 is reduced, not eliminated.

## References

- [Honesty discipline write-up](../../architectures/v3/disciplines/honesty.md)
- [Disciplines index](../../architectures/v3/disciplines/index.md)
- [F53 voluntary-discipline fragility](../../architectures/v3/failure-modes-v3.md#f53--voluntary-discipline-fragility-kahana-fragile-dependency-class)
- [Phase-3.5.5 RG-primitive rule (binding)](../../architectures/v3/candidate-registry.md#phase-355-rule-on-load-bearing-rg-primitives-binding-user-approved-2026-05-25)
- [Phase-3.4 buildability + corpus-why two-part rule](../../architectures/v3/phase-3.4-decisions-resolved.md#refined-two-part-rule-for-accepting-a-substrate-primitive)
- [ADR 0012: P-05 trajectory capture](./0012-p-05-trajectory-capture.md) — substrate audit trail for honest-acknowledgements
- [`AGENTS-MD-ffe35aa500`](../../retrospective/2026-05-25-155/AGENTS-MD-ffe35aa500-honest-acknowledgements-pre-round-2-firing.md) — Round-2 honest-acknowledgements rule
- [`SKILL-SPEC-34dd1d0274`: decision-brief adversarial-review lifecycle](../../retrospective/2026-05-25-155/SKILL-SPEC-34dd1d0274-decision-brief-adversarial-review-lifecycle.md) — mechanical enforcement of the acknowledgements checkpoint
- [`AGENTS.md` real-subagent adversarial-review rule](../../AGENTS.md#adversarial-review-must-be-real-subagents)
- [auto-005 Phase-5 dispatch shape](../../architectures/v3/decisions/auto-005-phase-5-dispatch-shape.md) — Wave-5.2 fanout context
