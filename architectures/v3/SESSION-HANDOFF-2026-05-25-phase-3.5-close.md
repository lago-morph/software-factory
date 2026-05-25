# Session handoff — 2026-05-25 (Phase 3.5 closed) — SUPERSEDED

> **STATUS: SUPERSEDED 2026-05-25 by [Phase-4-close handoff](SESSION-HANDOFF-2026-05-25-phase-4-close.md).** Phase 4 closed in the same calendar day as Phase 3.5; this brief was the pickup brief for Phase 4 work and is now historical. The Phase-4-close handoff is the canonical pickup point for Phase 5.

This is the pickup brief for the next agent. Phase 3.5 is **closed** as of the overnight run completed 2026-05-25. The next work is **Phase 4** (per-candidate substrate-requirements + shared-discipline extraction + primitive-overlap analysis).

Supersedes the [Phase-3.4-close handoff](SESSION-HANDOFF-2026-05-25-phase-3.4-close.md).

## Where we are

**Phase 3.5 is closed.** Summary of the close state:

| Concern | State | Detail |
|---|---|---|
| Substrate-primitive buildability | **Closed** | 34 primitive IDs enumerated (P-01–P-34); 24 sketches landed (3 cluster + 21 per-primitive); see [`primitives/index.md`](primitives/index.md) |
| Candidate re-check | **Closed** | All 10 candidates carry forward into Phase 4; see [`candidate-registry.md` § Phase 3.5.5](candidate-registry.md#phase-355-candidate-re-check-post-buildability) |
| U-B P-31 conditional survival | **Resolved** | Smoke-test produced 5/5 non-trivial cross-layer invariants; U-B survives with full Phase-4 sub-track authorized. See [`auto-002` Round 2](decisions/auto-002-ub-path.md) and [`P-31-smoke-test-invariants`](primitives/P-31-smoke-test-invariants.md). |
| Phase-3.5.5 RG-primitive rule | **Binding (user-approved 2026-05-25)** | Any candidate with a load-bearing RG primitive may either (a) commit to a bounded authoring sub-track at Phase 4, or (b) downgrade dependent contract to accept-as-RG. See [`candidate-registry.md` § Phase-3.5.5 RG-primitive rule](candidate-registry.md#phase-355-rule-on-load-bearing-rg-primitives-binding-user-approved-2026-05-25). |
| Adversarial-review discipline | **Binding (AGENTS.md)** | Reviews of decision briefs MUST be real subagent dispatches; inline-simulated reviewers forbidden as substitute. See [`AGENTS.md` § Adversarial review MUST be real subagents](../../AGENTS.md#adversarial-review-must-be-real-subagents). |

## Candidate-set state at Phase 3.5 close

10 candidates carry forward into Phase 4. **No self-eliminations, no conditional survivals.**

| Candidate | Mandate | Buildability outcome | Phase-4 entry posture |
|---|---|---|---|
| [GF-S](candidate-registry.md#gf-s--greenfield-substrate-first) | greenfield | All primitives buildable; P-15 contradiction-detector reliability is Phase-8 lean-eval input | Normal Phase-4 entry |
| [GF-M](candidate-registry.md#gf-m--greenfield-methodology-first) | greenfield | All buildable; P-21 paraphrase calibration is Phase-8 lean-eval input | Normal Phase-4 entry |
| [GF-C](candidate-registry.md#gf-c--greenfield-cold-start-first) | greenfield | All buildable; P-17 substance-check on 2 of 9 fields is RG | Council interrogation depth becomes Phase-4 methodology work |
| [BF-S](candidate-registry.md#bf-s--brownfield-substrate-first) | brownfield | All buildable; B7 ROBUST claim downgraded (P-23 partition-leakage is structural) | Rephrase B7 to "rate-limited side-channel mitigation"; surface residual leakage as accepted-open |
| [BF-M](candidate-registry.md#bf-m--brownfield-methodology-first) | brownfield | All buildable; P-27 brief-quality calibration carried to Phase 5/8 | Normal Phase-4 entry + stage-compression specification owed |
| [BF-L](candidate-registry.md#bf-l--brownfield-legacy-ingestion-first) | brownfield | P-26 Codebase Model RG overall (2 of 6 views RG); 9–18 engineer-months realistic | **Phase-3.5.5 RG-primitive rule applies**: pick option (a) bounded sub-track per RG view (conventional / invariant) or (b) accept-as-RG (default). User input or candidate-author input needed at Phase 4 entry. |
| [U-A](candidate-registry.md#u-a--escrow-graph-factory-cycle--directed-graph-of-typed-nodes) | unified-attempt | All buildable | If claims brownfield-fit, must articulate Codebase Model acquisition (X_UNM_B) |
| [U-B](candidate-registry.md#u-b--pace-layered-escrow-factory-5-layer-artifact-stack-with-bidirectional-traversal) | unified-attempt | P-31 smoke-test passed (5/5 pairs produced non-trivial invariants) | Full Phase-4 invariant-authoring sub-track authorized (scale 1-per-pair to ≥3-per-pair; ≥15 total). X_UNM_B caveat if brownfield-fit claimed. |
| [U-C](candidate-registry.md#u-c--anchor-distance-factory-every-work-unit-parameterised-by-graph-distance-to-a-frozen-anchor) | unified-attempt | All buildable; P-32 distance estimator calibration + Goodhart-resistance RG | Calibration recipe + Goodhart-resistance evidence owed at Phase 5/8. X_UNM_B caveat. |
| [D7-U-1](candidate-registry.md#d7-u-1--falsification-topology-factory--ftf-every-artifact-carries-an-opposing-side-commitment) | unified-attempt | P-34 independence auditor RG (auditor-recursion); A+C hybrid recommended | A+C hybrid as Phase-5 ADR with accepted-open structural concern. X_UNM_B caveat. |

3 candidates carry RG flags into Phase 4 (BF-L, U-B, D7-U-1); 5 carry partial-RG flags on specific sub-components or calibration questions.

## The next work — Phase 4

Per the [v1.2 plan revision](../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md#phase-4--per-candidate-substrate-requirements--shared-discipline-extraction-revised-in-v12), Phase 4 produces:

- **4.1 Per-candidate substrate-requirements summary** (×10 candidates) — for each candidate, list buildability-confirmed primitives by ID + open RG primitives + the candidate's specific contracts. Consumes [`primitives/index.md`](primitives/index.md) post-sketch annotations + per-primitive sketches as inputs. Output: `architectures/v3/substrate-requirements/<candidate-id>.md`.
- **4.2 Primitive-overlap analysis** (1 file) — informational, not winner-picker. Resolves the deferred same-vs-distinct questions on P-28/P-29/P-30 contested variants; resolves the P-08/P-09 collapse question; confirms or rejects the P-12/P-16 absorption. Output: [`primitives/overlap.md`](primitives/overlap.md).
- **4.3 Shared-discipline inventory** — extract architecture-level disciplines named across candidates (three-layer citation, concrete-task, bias-guard, watchdog escalation, cost-ceiling enforcement, etc.). Output: `architectures/v3/disciplines/index.md` + per-discipline files.

### Phase-4 entry blockers (user-input territory)

1. **BF-L's per-RG-view choice.** Per the Phase-3.5.5 RG-primitive rule, BF-L should declare its choice for each of the 2 RG views (conventional, invariant): bounded sub-track or accept-as-RG. The candidate-author (a Phase-2 subagent's role) doesn't exist in the live state — the lead agent should either (a) write a brief recommending one default per view and dispatch adversarial review per the AGENTS.md rule, or (b) surface to user for direct decision. **Recommendation:** brief + adversarial review per the rule, with sensible defaults — accept-as-RG for conventional view (LLM-with-structured-output is non-trivial calibration work; deferring to use-time is honest); bounded sub-track for invariant view if Daikon-style runtime inference is plausible against a representative test corpus.

2. **Phase-4 dispatch shape.** 10 per-candidate substrate-requirements subagents in parallel (lead-agent default), or per-mandate batched (3 GF + 3 BF + 4 U), or hybrid. Per AGENTS.md, this decision should be brief'd + reviewed before dispatch. Lead-agent default recommendation: per-candidate parallel — same total cost, simpler aggregation.

### Phase-4 work that doesn't need user input

- The discipline-extraction work (4.3) can start in parallel with substrate-requirements work; it doesn't depend on per-candidate decisions.
- The primitive-overlap analysis (4.2) is a lead-agent diff over per-candidate summaries; runs after 4.1.

## What carried forward (load-bearing material)

- [`phase-3.4-decisions-resolved.md`](phase-3.4-decisions-resolved.md) — all four Tier-1 decisions; scoping principle; refined two-part rule; working definitions of architecture/substrate/methodology/discipline + entry-mode greenfield/brownfield. Binding.
- [`candidate-registry.md`](candidate-registry.md) — 10 candidates, per-candidate Phase-3.5.5 status, Phase-3.5.5 RG-primitive rule (binding).
- [`primitives/index.md`](primitives/index.md) — 34 primitive IDs with dispatch tiers, post-sketch annotations, and per-candidate primitive coverage round-trip check.
- [`primitives/P-01–P-34` + `cluster-C1/C2/C3`](primitives/) — 24 buildability sketches with construction paths (named tools + integration sentences) and corpus-why citations.
- [`decisions/auto-001-phase-3.5-dispatch-shape.md`](decisions/auto-001-phase-3.5-dispatch-shape.md) — hybrid dispatch decision (Round 2 supersedes Round 1).
- [`decisions/auto-002-ub-path.md`](decisions/auto-002-ub-path.md) — U-B smoke-test variant decision (Round 2 supersedes Round 1).
- [`primitives/P-31-smoke-test-invariants.md`](primitives/P-31-smoke-test-invariants.md) — the smoke-test result that resolved U-B's conditional survival.
- [`../../AGENTS.md`](../../AGENTS.md) — adversarial-review-MUST-be-subagents rule (binding).
- [`../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md`](../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md) — v1.2 plan revision (Phase 3.5 + rescoped Phase 4–8 for 10 candidates).
- [`../../overnight-summary.md`](../../overnight-summary.md) — the morning-review entry point for the 2026-05-25 overnight run.

## Open questions / suggestions for the next agent to surface

1. **BF-L's per-RG-view choice** (see Phase-4 entry blockers above). Highest-priority morning surface.
2. **Phase-4 dispatch shape** (per-candidate vs per-mandate batched). Brief + review per AGENTS.md.
3. **X_UNM_B follow-through.** All 4 unified-attempt candidates (U-A, U-B, U-C, D7-U-1) that claim brownfield-fit must articulate how they acquire the Codebase Model equivalent from legacy artifacts. This is a Phase-4 per-candidate substrate-requirements question; each unified candidate's summary must address it.
4. **P-08/P-09 collapse + P-12/P-16 absorption.** These are Phase-4.2 same-vs-distinct questions raised by sketches. They land at Phase 4.2 primitive-overlap analysis.
5. **Phase-3.5 follow-up bias-guard pass (optional).** The v1.2 plan revision named per-primitive bias-guard subagents (buildability-skeptic, corpus-citation-auditor, orphan-defender-replaced-by-orphan-cluster-defender). These did not fire during the overnight run — lead-agent inline review of each sketch served as a thin substitute. The most material findings (P-26 RG, P-31 no-invariants, P-23 structural leakage) were honestly reported by the subagents themselves, so the bias guards' value-add is plausibly marginal. If the user wants the bias guards formally run, that's a follow-up dispatch.

## Concrete pickup steps for the next agent

1. Read [`AGENTS.md`](../../AGENTS.md) (project conventions, including the new adversarial-review rule).
2. Read [`phase-3.4-decisions-resolved.md`](phase-3.4-decisions-resolved.md) — Tier-1 decisions, scoping principle, refined two-part rule, working definitions. Binding.
3. Read this handoff doc.
4. Read [`candidate-registry.md`](candidate-registry.md) end-to-end, focusing on the Phase-3.5.5 section + RG-primitive rule.
5. Skim [`primitives/index.md`](primitives/index.md) post-sketch annotations to understand the buildability landscape; drill into individual primitive sketches only as needed.
6. Read [`../../overnight-summary.md`](../../overnight-summary.md) for the rewind points if any decision needs reversal.
7. Surface to the user: BF-L's per-RG-view choice (Phase-4 entry blocker #1) + Phase-4 dispatch shape decision (entry blocker #2). Per AGENTS.md, draft a brief + dispatch real adversarial reviewers; do NOT inline-simulate.
8. Once blockers resolved, dispatch Phase 4.

## Current git state

Branch chain at handoff (top to bottom):
- `claude/handoff-phase-3.5-close` (this commit; PR pending)
- `claude/codify-review-rule-and-bfl-option` ([PR #144](https://github.com/lago-morph/software-factory/pull/144))
- `claude/ub-smoke-test-result` ([PR #143](https://github.com/lago-morph/software-factory/pull/143))
- `claude/auto-002-ub-path` ([PR #142](https://github.com/lago-morph/software-factory/pull/142))
- `claude/overnight-summary` ([PR #141](https://github.com/lago-morph/software-factory/pull/141))
- `claude/phase-3.5.5-candidate-recheck` ([PR #140](https://github.com/lago-morph/software-factory/pull/140))
- `claude/phase-3.5-per-primitive` ([PR #139](https://github.com/lago-morph/software-factory/pull/139))
- `claude/phase-3.5-cluster-sketches` ([PR #138](https://github.com/lago-morph/software-factory/pull/138))
- `claude/phase-3.5-enumeration` ([PR #137](https://github.com/lago-morph/software-factory/pull/137))
- `claude/busy-mayer-d1pjJ` ([PR #136](https://github.com/lago-morph/software-factory/pull/136))
- `main` (at PR #134 close + PR #133 + PR #135 retrospective merges).

Subagents dispatched in the overnight run: 30 total.

When the chain merges, the SESSION-HANDOFF state above becomes the canonical pickup point for the next agent.
