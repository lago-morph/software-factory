# Session handoff — 2026-05-25

This is a session-state snapshot for the next agent picking up the v3 architecture-synthesis work after this session terminates.

## Where we are in the pipeline

**Phase 3.4 is in progress.** The integration brief is published at [`phase-3.4-integration-brief.md`](phase-3.4-integration-brief.md). The user is working through the Tier-1 decisions one at a time.

**Status of the 4 Tier-1 decisions:**

| Decision | Status | Reference |
|---|---|---|
| DEC-1 (unification verdict) | **PENDING** — user said "I'll get to DEC-1 in a minute" but session ended first | [`decisions/dec-1-unification-verdict.md`](decisions/dec-1-unification-verdict.md) |
| DEC-2 (cognitive escrow placement) | **RESOLVED: methodology layer** | [`phase-3.4-decisions-resolved.md`](phase-3.4-decisions-resolved.md) |
| DEC-3 (greenfield methodology shape) | **RESOLVED: carry all defensible candidates (GF-C, GF-M, GF-S)** | same |
| DEC-4 (brownfield methodology shape) | **RESOLVED: carry all defensible candidates (BF-L, BF-M, BF-S)** | same |

## The load-bearing reframe from the user's last message

In addition to the three decisions above, the user declared two cross-cutting orientations that affect everything downstream:

### Scoping principle (immutable per user)

**Carry forward every candidate methodology / architecture that defended itself against Phase-3.2/3.3 critique. Do not eliminate at end-of-Phase-3.** The corpus has no validated working factory; source authors have incentives; crossover synergies between candidates only emerge if candidates stay alive. Pressure-testing happens in Phase-8 lean-evals and downstream simulation, not at the Phase-3.4 checkpoint.

This is a major reframe of the integration brief's framing. The brief posed each Tier-1 decision as "pick one option" (e.g., DEC-1 options A/B/C/D, DEC-3 options A/B/C/D). Under the scoping principle, most of those decisions become "carry all options that defended themselves" rather than "pick one." DEC-3 and DEC-4 are already resolved this way (carry all); DEC-1 likely resolves similarly when the user gets to it.

### Methodology-over-substrate orientation

User: "We should be trying to find **methodologies**, not substrates. The methodologies should issue requirements for a substrate. It is incredibly unlikely that a substrate requirement will not be able to be implemented quickly on any cloud platform if it is sufficiently detailed."

**Lead-agent pushback (recorded in [`phase-3.4-decisions-resolved.md`](phase-3.4-decisions-resolved.md) cross-cutting section):** directionally correct, with one substantive caveat. Some primitives the corpus called "substrate" are non-commodity designed systems — `CodebaseModel` (brownfield-side, five sub-stores including symbol index, dependency-and-impact graph, runtime/telemetry view with role-based partitioning, attribution at symbol level, invariant/debt view) is the clearest example. Calling these "easy to implement on cloud" understates the design. Refined orientation: methodology drives; substrate requirements fall out per methodology; *but* when a methodology requires a primitive that is itself a designed system (not a configuration), name that primitive explicitly.

The user did not yet acknowledge this pushback before the session-handoff request. The next agent should surface the pushback to the user as part of resolving DEC-1 and beyond.

## What needs to change in prior and future work

**Prior work survives — re-framed, not invalidated.** All Phase 1, Phase 2, and Phase 3.1/3.2/3.3 artifacts stay in the repo as inputs. Phase 3.2/3.3 critiques reframe purpose: from "should this draft be demoted?" → "what must this candidate address before carrying forward?" Critiques become improvement requirements, not elimination grounds.

**Phase 4 reframes** from "shared/divergent extraction over surviving syntheses" to "substrate-requirements extraction per surviving candidate; primitive-overlap analysis as side artifact."

**Phase 5/6/7/8 each scale up** in candidate count. ADR count grows; spec count grows (one per candidate); back-fill audit per candidate; lean-eval brief per candidate.

**Downstream** of the synthesis pipeline (post-Phase-8), the user has named simulation / mock-up evaluation of candidates against each other. The scoping principle is designed to keep candidates alive for that evaluation.

## Open questions for the next agent

1. **DEC-1 resolution.** Likely "carry all unified candidates that defended themselves alongside the mandate-specific candidates," in line with the scoping principle. Possible candidates include U-A (Escrow-Graph Factory), U-B (Pace-Layered Escrow Factory), U-C (Anchor-Distance Factory), and the D7-U-1 alternative (Adversarial-Falsification Topology / Falsification-Topology Factory). User to confirm.

2. **`X_UNM_B`'s CodebaseModel finding** under DEC-1 multi-candidate disposition. If a unified candidate carries forward without a CodebaseModel primitive equivalent, the brownfield-critical F-modes (F21, F28, F34) remain unmitigated for that candidate. Does this disqualify it (per "successfully defended itself") or does the candidate get a CodebaseModel addition?

3. **DEC-2 ripple.** Demoting cognitive escrow from substrate primitive to methodology pattern means each surviving candidate must articulate its own F42/F53 (cognitive-escrow / voluntary-discipline-fragility) mitigation. This becomes an addendum each carrying-forward draft must include.

4. **Methodology-over-substrate reframe** — the next agent should surface to the user that the lead-agent pushback is in [`phase-3.4-decisions-resolved.md`](phase-3.4-decisions-resolved.md) and confirm whether the user accepts the refined orientation or wants their original framing.

5. **Phase 4 dispatch shape under the new scoping principle.** The Phase 4 step in the synthesis plan presupposes 3 surviving syntheses (greenfield + brownfield + unified). Under "carry all candidates," Phase 4 has potentially 9 surviving candidates (3 greenfield + 3 brownfield + 3 unified) plus the D7-U-1 alternative = up to 10. The Phase 4 dispatch shape needs to be reconsidered — does it run per candidate? Per mandate-group? How does it produce a useful comparison?

## Concrete pickup steps for the next agent

1. Read [`phase-3.4-decisions-resolved.md`](phase-3.4-decisions-resolved.md) for the recorded decisions and scoping principle.
2. Read this handoff doc.
3. Read [`phase-3.4-integration-brief.md`](phase-3.4-integration-brief.md) for the Tier-1/2/3 decision queue (knowing now that the framing should be re-interpreted per the scoping principle).
4. Read the four [`decisions/`](decisions/) briefs for the Tier-1 detail.
5. Surface to the user: confirmation request on the methodology-over-substrate pushback; confirmation that DEC-1 resolves under the scoping principle; the open questions in section above.
6. Once DEC-1 resolves, update [`phase-3.4-decisions-resolved.md`](phase-3.4-decisions-resolved.md). When all four Tier-1 decisions are resolved, begin writing the post-adversarial syntheses (one per surviving candidate). This is Phase-3.4 integration proper.

## Current git state

Branch: `claude/agents-md-hook-fire-c0l3z`
PR: [#132](https://github.com/lago-morph/software-factory/pull/132)

Recent commits in order of recency:
- this commit (session handoff + DEC-2/3/4 resolution)
- `a6933e6` Tier-1 decision briefs (one file per question)
- `4e26492` primer: round-5 review fixes
- `bea6ef4` primer: round-4 review fixes
- (earlier history is the Phase 3.1/3.2/3.3 dispatch and critique work)
