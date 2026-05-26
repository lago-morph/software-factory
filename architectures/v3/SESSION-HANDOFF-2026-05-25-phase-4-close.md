# Session handoff — 2026-05-25 (Phase 4 closed) [SUPERSEDED]

> **[SUPERSEDED]** This handoff is superseded by the [Phase-5a close handoff](SESSION-HANDOFF-2026-05-25-phase-5a-close.md). Phase 5a (Wave 5.1a + 5.1b + 5.2 ADRs) is closed; Wave 5.3 is the active owed work with a binding Phase-6 gate. Read the active handoff first.

This is the pickup brief for the next agent. **Phase 4 is closed** as of the unattended Phase-4 dispatch session completed 2026-05-25 (same calendar day as Phase 3.5 close, evening run). The next work is **Phase 5** (per-candidate ADRs + common ADRs on shared primitives + discipline ADRs).

Supersedes the [Phase-3.5-close handoff](SESSION-HANDOFF-2026-05-25-phase-3.5-close.md).

## Where we are

**Phase 4 is closed.** Summary of the close state:

| Concern | State | Detail |
|---|---|---|
| Phase-4 entry blockers | **Resolved** | [auto-003 Round 2](decisions/auto-003-bfl-rg-view-choice.md) (BF-L per-RG-view choice → option A′ smoke-test-first per view); [auto-004 Round 2](decisions/auto-004-phase-4-dispatch-shape.md) (Phase-4 dispatch shape → per-candidate parallel fanout + 6-wave structure) |
| Per-candidate substrate-requirements (Wave 4.1) | **Closed** | 10 summaries landed at [`substrate-requirements/`](substrate-requirements/) (GF-M exemplar + 9 subagent-authored, all rubric-compliant 800-1500w final-iterated) |
| Primitive overlap analysis (Wave 4.2) | **Closed** | 8 deferred same-vs-distinct + absorption questions resolved at [`primitives/overlap.md`](primitives/overlap.md) |
| Shared-discipline extraction (Wave 4.3) | **Closed** | 21 disciplines in merged canonical [`disciplines/index.md`](disciplines/index.md) (13 track-driven + 8 substrate-layer; 3 overlap reconciliations dropped) |
| BF-L per-view deep research (Wave 4.4) | **Closed** | [`research-notes/bfl-conventional-view-prior-art.md`](research-notes/bfl-conventional-view-prior-art.md) (3490w; strong naming/layering precedent, idiom/test-pattern weak) + [`research-notes/bfl-invariant-view-prior-art.md`](research-notes/bfl-invariant-view-prior-art.md) (3000w; confirms Daikon-on-modern-observability unwitnessed; tiered source plan recommended) |
| Authoring sub-tracks (Wave 4.5) | **All 3 PASS** | [`sub-tracks/u-b-invariant-authoring.md`](sub-tracks/u-b-invariant-authoring.md) (20 invariants vs ≥15 target; 5/5 pairs scaled); [`sub-tracks/bfl-conventional-smoke-test.md`](sub-tracks/bfl-conventional-smoke-test.md) (3/3 languages PASS); [`sub-tracks/bfl-invariant-smoke-test.md`](sub-tracks/bfl-invariant-smoke-test.md) (3/3 languages PASS) |
| Aggregation + registry update + close (Wave 4.6) | **Closed** | Registry updated with Wave-4.5 verdicts (this commit); discipline-index merge completed (this commit); this handoff doc |

## Candidate-set state at Phase 4 close

**All 10 candidates carry forward into Phase 5.** No self-eliminations at Phase 4. No methodology-degradation clauses activated. 3 of 10 carry RG-primitive bounded sub-tracks all confirmed PASS at Wave 4.5:

| Candidate | Mandate | Phase-4 outcome | Phase-5 entry posture |
|---|---|---|---|
| [GF-S](candidate-registry.md#gf-s--greenfield-substrate-first-1) | greenfield | survives; Phase-8 lean-eval on P-15 contradiction-detector reliability | Normal Phase-5 entry; 9 primitives owed (S1–S9) — 6 common-ADR, 3 candidate-specific |
| [GF-M](candidate-registry.md#gf-m--greenfield-methodology-first-1) | greenfield | survives (exemplar candidate); P-21 calibration to Phase-8 | Normal Phase-5 entry; 5 primitives, mostly common-ADR + 2 orphan (P-20, P-21) |
| [GF-C](candidate-registry.md#gf-c--greenfield-cold-start-first-1) | greenfield | survives; 2 partial-RG flags on P-17 substance-check → methodology layer | Normal Phase-5 entry; 4 primitives; P-16 absorbed into P-12 per [overlap.md](primitives/overlap.md#p-12--p-16--deterministic-linter-framework--earsgtwr-rule-library-absorption) |
| [BF-S](candidate-registry.md#bf-s--brownfield-substrate-first-1) | brownfield | survives with downgraded B7; P-23 partition-leakage rate-limited | Normal Phase-5 entry; 5 primitives (S-1 to S-5) |
| [BF-M](candidate-registry.md#bf-m--brownfield-methodology-first-1) | brownfield | survives; P-08↔P-09 absorbed per [overlap.md](primitives/overlap.md#p-08--p-09--held-out-runner--scenario-storage-collapse); brief-quality calibration to Phase-5/8 | Normal Phase-5 entry; 13 primitives (after P-09 absorb) |
| [BF-L](candidate-registry.md#bf-l--brownfield-legacy-ingestion-first-1) | brownfield | **Both RG views PASS smoke-tests** (3/3 languages each); full Wave 4.5b owed at Phase 5/6 (scale 3-per-language to ≥10) | Phase-5 ADRs on P-26 view authoring + methodology-degradation-clause spec at Phase 6 (clause NOT activated but spec carries it for the (b) fallback's resilience) |
| [U-A](candidate-registry.md#u-a--escrow-graph-factory-cycle--directed-graph-of-typed-nodes-1) | unified-attempt | survives; X_UNM_B articulated honestly (interval-grain reconstruction; flagged for Phase-5/6 methodology-spec) | Normal Phase-5 entry; 5 primitives all designed-system with 4 contested-variant ADRs (P-28/P-29/P-30/P-19 per-variant) |
| [U-B](candidate-registry.md#u-b--pace-layered-escrow-factory-5-layer-artifact-stack-with-bidirectional-traversal-1) | unified-attempt | **U-B P-31 sub-track PASS** (20 invariants vs ≥15); `survives with deferred-defense flag` → `survives` | Phase-5 ADRs on per-layer-pair invariant registry + 7 ADR seeds from sub-track (see [`u-b-invariant-authoring`](sub-tracks/u-b-invariant-authoring.md)) |
| [U-C](candidate-registry.md#u-c--anchor-distance-factory-every-work-unit-parameterised-by-graph-distance-to-a-frozen-anchor-1) | unified-attempt | survives; P-32 calibration + Goodhart-resistance evidence owed at Phase-5/8 | Normal Phase-5 entry; X_UNM_B articulated with honest F33/F51 vulnerable third leg |
| [D7-U-1](candidate-registry.md#d7-u-1--falsification-topology-factory--ftf-every-artifact-carries-an-opposing-side-commitment-1) | unified-attempt | survives with A+C hybrid on P-34 (no Wave 4.5 needed beyond the hybrid itself); FC-catalog acquisition articulated for brownfield | Phase-5 ADR on A+C hybrid with accepted-open structural recursion residual |

## The next work — Phase 5

Per the [v1.2 plan revision](../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md#phase-5--adrs-per-candidate-with-cross-references-on-shared-primitives-revised-in-v12), Phase 5 dispatches ADRs in three waves:

- **5.1 Wave 1: Common-primitive ADRs** (~13 ADRs per Wave 4.2 verdicts). Primitives shared by ≥3 candidates. Parallel fanout. The work-unit-class taxonomy ADR (per D2) is load-bearing for the Phase-6 mandate-fit matrix; lands in this wave.
- **5.2 Wave 2: Discipline ADRs** (~8-12 from [`disciplines/index.md`](disciplines/index.md)). Parallel with Wave 1.
- **5.3 Wave 3: Candidate-specific ADRs** (~16 orphan + 13 per-variant + per-candidate methodology binding choices = ~30 total across 10 candidates). After Waves 1+2 land.

**Phase-5 ADR count estimate (per [overlap.md](primitives/overlap.md)):** ~54-62 (within v1.2 plan envelope 50-80).

### Phase-5 entry checklist

| Item | State | Action |
|---|---|---|
| Phase-3.5.5 RG-primitive rule applications closed | Yes | All 3 RG candidates have sub-track verdicts (3 PASS); no fallbacks activated |
| Same-vs-distinct verdicts rendered | Yes | [`overlap.md`](primitives/overlap.md) resolves 8 questions |
| Disciplines extracted | Yes | 21 in canonical [`disciplines/index.md`](disciplines/index.md) |
| Wave 4.5b owed work named | Yes | BF-L conventional + BF-L invariant scaling from 3-per-language to ≥10-per-language; owed at Phase 5/6 |
| Methodology-degradation clauses | Spec owed | BF-L methodology-degradation clause (for the (b) fallback's resilience) owed at Phase 6 methodology spec even though clause NOT activated by Wave 4.5 outcomes |
| Phase-8 lean-eval candidates surfaced | Many | P-15 contradiction-detector reliability; P-19 four-variant correlation; P-21 calibration; P-25 utility-tax; P-27 brief-quality; P-28 envelope-collision coexistence; P-30 timer vs event reliability; P-32 calibration + Goodhart-resistance; OQ-PLEF-3 multi-cycle drift; F40 last-mile drift |

## What carried forward (load-bearing material)

### Phase 4 outputs (all on stacked PRs from this run)

- [`decisions/auto-003-bfl-rg-view-choice.md`](decisions/auto-003-bfl-rg-view-choice.md) — Round 2 option A′ smoke-test-first per view; **both views PASSED** at Wave 4.5
- [`decisions/auto-004-phase-4-dispatch-shape.md`](decisions/auto-004-phase-4-dispatch-shape.md) — Round 2 per-candidate parallel fanout + 6-wave structure
- [`substrate-requirements/<id>.md`](substrate-requirements/) × 10 candidates (Wave 4.1; final-iterated within-rubric)
- [`primitives/overlap.md`](primitives/overlap.md) (Wave 4.2; 8 verdicts)
- [`disciplines/index.md`](disciplines/index.md) (Wave 4.6 merge; 21 disciplines)
- [`disciplines/sketch-registry-extracted-disciplines.md`](disciplines/sketch-registry-extracted-disciplines.md) (Wave 4.3 substrate-layer extraction; preserved for traceability)
- [`research-notes/bfl-conventional-view-prior-art.md`](research-notes/bfl-conventional-view-prior-art.md) + [`bfl-invariant-view-prior-art.md`](research-notes/bfl-invariant-view-prior-art.md) (Wave 4.4)
- [`sub-tracks/u-b-invariant-authoring.md`](sub-tracks/u-b-invariant-authoring.md) (Wave 4.5; 20 invariants)
- [`sub-tracks/bfl-conventional-smoke-test.md`](sub-tracks/bfl-conventional-smoke-test.md) + [`sub-tracks/bfl-invariant-smoke-test.md`](sub-tracks/bfl-invariant-smoke-test.md) (Wave 4.5; both PASS)

### Updated artifacts

- [`candidate-registry.md`](candidate-registry.md) — Phase-3.5.5 application table updated with Wave-4.5 verdicts; new "Phase 4 close — Wave 4.5 outcomes summary" section.
- [`SESSION-HANDOFF-2026-05-25-phase-3.5-close.md`](SESSION-HANDOFF-2026-05-25-phase-3.5-close.md) — marked SUPERSEDED.

### Inherited binding material (from Phase 3.5 close)

- [`phase-3.4-decisions-resolved.md`](phase-3.4-decisions-resolved.md) — all four Tier-1 decisions; scoping principle; refined two-part rule; working definitions. Binding.
- [`primitives/index.md`](primitives/index.md) — 34 primitive IDs; 30 distinct after Phase-4.2 collapse.
- [`primitives/P-01–P-34` + `cluster-C1/C2/C3`](primitives/) — 24 buildability sketches.
- [`decisions/auto-001`](decisions/auto-001-phase-3.5-dispatch-shape.md) (Phase 3.5 dispatch shape) + [`auto-002`](decisions/auto-002-ub-path.md) (U-B path).
- [`AGENTS.md`](../../AGENTS.md) — adversarial-review-MUST-be-subagents rule (binding).
- [`ARCHITECTURE-V3-SYNTHESIS-PLAN.md`](../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md) — v1.2 plan revision.

## Open questions / suggestions for the next agent to surface

1. **Phase-5 dispatch shape decision** (analogous to auto-001 and auto-004 — write an `auto-005` brief with real adversarial review per AGENTS.md). Default recommendation: 3-wave parallel fanout per the v1.2 plan (Wave 5.1 common-primitive ADRs + Wave 5.2 discipline ADRs in parallel; Wave 5.3 candidate-specific ADRs after).
2. **Wave 4.5b owed work integration into Phase 5/6.** BF-L conventional + invariant view scaling (3 → ≥10 per language) is owed; the scaling work is best authored as Phase-5/6 sub-tracks rather than Phase-5 ADRs themselves. Decide whether to dispatch Wave 4.5b at Phase 5 entry or defer to Phase 6 architecture-spec authorship.
3. **Phase-3.5 follow-up bias-guard pass (still optional, still unfired).** Per the [Phase-3.5-close handoff](SESSION-HANDOFF-2026-05-25-phase-3.5-close.md#open-questions--suggestions-for-the-next-agent-to-surface) item 5: the per-primitive bias-guard subagents named in the v1.2 plan did not fire during the overnight run. They did not fire during Phase 4 either (lead-agent inline review of each sketch served as a thin substitute throughout). If desired before Phase 5, that's a follow-up dispatch.
4. **D-Three-Layer-Citation / D-Concrete-Task discipline extraction.** The Wave 4.3 extraction surfaced these as flagged-for-attention but neither subagent's read scope covered them deeply. Phase 5 ADR authoring may surface them naturally as ADR-authoring disciplines; if not, they remain as informal carryforward.
5. **X_UNM_B per-candidate methodology-spec depth.** Unified candidates (U-A, U-B, U-C, D7-U-1) articulated X_UNM_B at the substrate-requirements level (per the Wave-4.1 shared §4 skeleton). The Phase-6 architecture spec for each needs to deepen the X_UNM_B articulation to operational detail. Lead-agent call at Phase 6 entry: dispatch per-candidate sub-track for X_UNM_B operationalization, or fold into the architecture-spec authoring directly.

## Concrete pickup steps for the next agent

1. Read [`AGENTS.md`](../../AGENTS.md) (project conventions).
2. Read [`phase-3.4-decisions-resolved.md`](phase-3.4-decisions-resolved.md) (Tier-1 decisions; binding).
3. Read this handoff doc.
4. Read [`candidate-registry.md`](candidate-registry.md) end-to-end, focusing on the Phase-3.5.5 application table (now updated with Wave-4.5 verdicts) + the new Phase-4 close summary section.
5. Skim [`primitives/overlap.md`](primitives/overlap.md) for the same-vs-distinct verdicts that shape Phase-5 ADR count.
6. Skim [`disciplines/index.md`](disciplines/index.md) for the 21 disciplines that drive Wave-5.2 discipline ADRs.
7. Decide Phase-5 dispatch shape (write `auto-005` brief; dispatch real adversarial reviewers per AGENTS.md).
8. Dispatch Phase 5.

## Current git state — Phase 4 PR chain (8 PRs from this session)

PRs opened, top to bottom of stack:

- [`claude/wave-4.6-phase-4-close`](claude/wave-4.6-phase-4-close) — this PR (registry update + disciplines merge + handoff)
- [`claude/wave-4.2-primitive-overlap`](https://github.com/lago-morph/software-factory/pull/154) — [PR #154]
- [`claude/wave-4.5-authoring-sub-tracks`](https://github.com/lago-morph/software-factory/pull/152) — [PR #152]
- [`claude/wave-4.1-substrate-requirements`](https://github.com/lago-morph/software-factory/pull/150) — [PR #150]
- [`claude/wave-4.3-disciplines`](https://github.com/lago-morph/software-factory/pull/149) — [PR #149] (parallel branch off auto-004)
- [`claude/auto-004-phase-4-dispatch-shape`](https://github.com/lago-morph/software-factory/pull/147) — [PR #147]
- [`claude/auto-003-bfl-rg-view-choice`](https://github.com/lago-morph/software-factory/pull/146) — [PR #146]
- `main` (at PR #145 close — Phase-3.5-close handoff merged)

Subagents dispatched in the Phase-4 session: **20 total** (4 adversarial reviewers + 2 BF-L research + 2 discipline extractors + 9 Wave-4.1 substrate-requirements + 3 Wave-4.5 authoring).

**Recommended merge order:** #146 → #147 → #149 (or in parallel with #150 since #149 is off #147) → #150 → #152 → #154 → (this PR). PR base auto-rebases as parents merge.

When the chain merges, this handoff becomes the canonical pickup point for Phase 5.
