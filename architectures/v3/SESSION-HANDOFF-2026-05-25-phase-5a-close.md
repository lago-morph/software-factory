# Session handoff — 2026-05-25 (Phase 5a closed; Wave 5.3 owed) [SUPERSEDED]

> **[SUPERSEDED]** This handoff is superseded by the [Phase-5 close handoff](SESSION-HANDOFF-2026-05-25-phase-5-close.md). Wave 5.3 was delivered in the same run that authored this handoff (the run continued past the original deferral); Phase 6 is now unblocked. Read the active handoff first.

This is the pickup brief for the next agent. **Phase 5a is closed** as of the autonomous run completed 2026-05-25 (Phase-5 ADR dispatch split per [auto-005 Round 2](decisions/auto-005-phase-5-dispatch-shape.md#decision-round-2): this run = Wave 5.1a + 5.1b + 5.2; Wave 5.3 deferred). **The next work is Wave 5.3** (~29 candidate-specific + per-variant ADRs) which is **non-negotiable owed before Phase 6 dispatch** per the binding constraint below.

Supersedes the [Phase-4-close handoff](SESSION-HANDOFF-2026-05-25-phase-4-close.md).

## Where we are

| Concern | State | Detail |
|---|---|---|
| auto-005 decision brief (Phase-5 dispatch shape) | **Closed** | Round 2 final: Option A′ (split Wave 5.1, defer Wave 5.3, raised rubric). [auto-005](decisions/auto-005-phase-5-dispatch-shape.md). |
| Wave 5.1a — Commodity substrate ADRs (8) | **Closed** | [`docs/adr/0010-0017`](../../docs/adr/). Exemplar: 0015 P-08 scenario storage. |
| Wave 5.2 — Discipline ADRs (10) | **Closed** | [`docs/adr/0018-0027`](../../docs/adr/). Exemplar: 0020 cost-ceiling. |
| Wave 5.1b — Designed-system + 2-candidate substrate ADRs (9) | **Closed** | [`docs/adr/0028-0036`](../../docs/adr/). Variant-bearing primitives (P-19, P-28, P-29, P-30) explicitly scope-bounded to framework-only with Wave-5.3 deferral. |
| Wave 5.3 — Candidate-specific + per-variant ADRs (~29) | **Owed; non-negotiable before Phase 6** | This handoff is the binding artifact. See [Wave 5.3 binding constraint](#wave-53-binding-constraint-non-negotiable) below. |
| Phase 5b-this-run-close summary | **Closed** | [`overnight-summary-2026-05-25.md`](../../overnight-summary-2026-05-25.md) (top of stack). |
| Self-retrospective | **Closed** | [`retrospective/2026-05-25-167.md`](../../retrospective/2026-05-25-167.md) (final PR-N covered by retro). |
| Phase 6 (architecture-spec authorship per candidate) | **BLOCKED** | Pending Wave 5.3 close OR adversarially-reviewed waiver decision brief. |

## Wave 5.3 binding constraint (non-negotiable)

Per [auto-005 Round 2 § Wave-5.3 binding artifact](decisions/auto-005-phase-5-dispatch-shape.md#wave-53-binding-artifact-convergent-round-2-amendment), this section IS the binding artifact. The next run's lead agent inherits:

### Wave 5.3 scope (~29 ADRs)

**Per-variant ADRs (13 total):**
- **P-28 envelopes × 4** — U-A interval-typed; U-B layer-typed; U-C anchor; D7-U-1 FC.
- **P-29 policy DSLs × 3** — U-A interval-policy schema; U-B layer-boundary schema; D7-U-1 FC-survival schema.
- **P-19 feature sources × 4** — GF-S work-unit-class features; BF-L per-region features (via P-26); U-C distance-tuple (via P-32); U-A interval-kind features.
- **P-30 state machines × 2** — U-A re-entry; D7-U-1 survival-window.

**Orphan ADRs (16 total, one per orphan primitive):**
- GF-S: P-10 (coordination medium), P-15 (4-guard mediator).
- GF-M: P-20 (reversibility), P-21 (paraphrase divergence).
- GF-C: P-11 (Cold-Start Bench), P-17 (Intent Crucible validator), P-18 (RSI Declaration Ledger).
- BF-S: – (no remaining orphans; P-24 folded into Wave 5.1b common ADR).
- BF-M: P-03 (worktree isolation), P-04 (PR creator).
- BF-L: P-26 (Codebase Model), P-13 (Maintenance loop).
- U-B: P-31 (Cross-layer drift detector).
- U-C: P-32 (Distance estimator).
- D7-U-1: P-33 (Opposing-side router), P-34 (Independence auditor).

**Total Wave 5.3 estimate: 13 + 16 = 29 ADRs.**

### ADR-ID-to-file mapping table (this run's outputs)

The Wave-5.3 dispatch brief in the next run uses this table to publish cross-references from per-variant ADRs to their parent common ADRs.

| Primitive / Discipline | ADR ID | File path | Wave |
|---|---|---|---|
| P-01 sandbox runtime | 0010 | `docs/adr/0010-p-01-sandbox-runtime.md` | 5.1a |
| P-02 cost ceilings | 0011 | `docs/adr/0011-p-02-cost-ceilings.md` | 5.1a |
| P-05 trajectory capture | 0012 | `docs/adr/0012-p-05-trajectory-capture.md` | 5.1a |
| P-06 watchdog tiers | 0013 | `docs/adr/0013-p-06-watchdog-tiers.md` | 5.1a |
| P-07 telemetry ingestor | 0014 | `docs/adr/0014-p-07-telemetry-ingestor.md` | 5.1a |
| P-08 scenario storage + runner | 0015 | `docs/adr/0015-p-08-scenario-storage-with-runner-contract.md` | 5.1a (exemplar) |
| P-14 judge router | 0016 | `docs/adr/0016-p-14-judge-router.md` | 5.1a |
| P-22 polyglot codebase index | 0017 | `docs/adr/0017-p-22-polyglot-codebase-index.md` | 5.1a |
| Discipline: bias-guard | 0018 | `docs/adr/0018-discipline-bias-guard.md` | 5.2 |
| Discipline: cognitive-escrow | 0019 | `docs/adr/0019-discipline-cognitive-escrow.md` | 5.2 |
| Discipline: cost-ceiling | 0020 | `docs/adr/0020-discipline-cost-ceiling.md` | 5.2 (exemplar) |
| Discipline: holdout | 0021 | `docs/adr/0021-discipline-holdout.md` | 5.2 |
| Discipline: honesty | 0022 | `docs/adr/0022-discipline-honesty.md` | 5.2 |
| Discipline: knowledge-promotion | 0023 | `docs/adr/0023-discipline-knowledge-promotion.md` | 5.2 |
| Discipline: regime-classification | 0024 | `docs/adr/0024-discipline-regime-classification.md` | 5.2 |
| Discipline: scoping | 0025 | `docs/adr/0025-discipline-scoping.md` | 5.2 |
| Discipline: three-loop | 0026 | `docs/adr/0026-discipline-three-loop.md` | 5.2 |
| Discipline: trifecta-closure | 0027 | `docs/adr/0027-discipline-trifecta-closure.md` | 5.2 |
| P-19 eligibility classifier framework | 0028 | `docs/adr/0028-p-19-eligibility-regime-classifier.md` | 5.1b |
| P-28 typed-object store framework | 0029 | `docs/adr/0029-p-28-typed-object-store.md` | 5.1b |
| P-29 policy mediator framework | 0030 | `docs/adr/0030-p-29-policy-mediator.md` | 5.1b |
| P-23 dependency-impact graph | 0031 | `docs/adr/0031-p-23-dependency-impact-graph.md` | 5.1b |
| P-12 deterministic linter (EARS+GtWR pack) | 0032 | `docs/adr/0032-p-12-deterministic-linter-framework.md` | 5.1b |
| P-25 CaMeL perimeter | 0033 | `docs/adr/0033-p-25-camel-perimeter.md` | 5.1b |
| P-27 archaeological-brief tooling | 0034 | `docs/adr/0034-p-27-archaeological-brief-tooling.md` | 5.1b |
| P-24 attribution store | 0035 | `docs/adr/0035-p-24-attribution-store.md` | 5.1b |
| P-30 event registrar substrate (Temporal) | 0036 | `docs/adr/0036-p-30-event-registrar-substrate.md` | 5.1b |

Wave 5.3 ADRs will assign IDs starting at 0037 in commit order.

### Phase 6 gate

**Phase 6 (architecture-spec authorship per candidate) MAY NOT START** until either:

1. **Wave 5.3 ADRs are Accepted** (per the auto-005 Round 2 plan); OR
2. **A future decision brief explicitly waives the dependency** with two rounds of real adversarial review per AGENTS.md `AGENTS-MD-d72e1a4f3c`. The waiver brief MUST justify why Phase 6 can proceed without the per-variant ADRs (e.g., scope-narrowing the architecture spec to non-variant-bearing candidates only; or accepting partial-spec drafts pending Wave-5.3 close).

This gate is binding. The next agent's first task on Phase-6 dispatch is to either dispatch Wave 5.3 OR author the waiver brief.

## Candidate-set state at Phase 5a close

**All 10 candidates carry forward.** No Phase-5 ADR authoring changed any candidate's structural defensibility — the wave outputs are uniform shared substrate + discipline ADRs that all candidates consume. Per-candidate ADRs (orphan + per-variant) are Wave 5.3 next run.

## What carried forward (load-bearing material)

### This run's outputs

- **auto-005 decision brief.** [`decisions/auto-005-phase-5-dispatch-shape.md`](decisions/auto-005-phase-5-dispatch-shape.md). Two rounds of real adversarial review per AGENTS.md. Round-2 final decision: Option A′.
- **27 Phase-5 ADRs.** [`docs/adr/0010-0036`](../../docs/adr/). All ≤1000 words, canonical 5-section structure, all internal links relative, all cross-references resolved.
- **Context-slimming artifacts (Phase A of this run).** [`AGENT-ENTRY.md`](../../AGENT-ENTRY.md) (root navigation); TL;DR sections on [`ARCHITECTURE-V3-SYNTHESIS-PLAN.md`](../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md) + [`candidate-registry.md`](candidate-registry.md); [`autonomous-run` skill updates](../../.claude/skills/autonomous-run/SKILL.md) (TL;DR regeneration + handoff-discipline AGENT-ENTRY pointer maintenance); [`CLAUDE.md`](../../CLAUDE.md) two-step session-startup convention.

### Inherited binding material (from Phase 4 close)

- [`phase-3.4-decisions-resolved.md`](phase-3.4-decisions-resolved.md) — all four Tier-1 decisions; scoping principle; refined two-part substrate-buildability rule; working definitions.
- [`primitives/index.md`](primitives/index.md) — 30 distinct primitives after Phase-4.2 collapse.
- [`primitives/overlap.md`](primitives/overlap.md) — Phase-4.2 same-vs-distinct verdicts.
- [`disciplines/index.md`](disciplines/index.md) — 21 canonical disciplines.
- [`substrate-requirements/`](substrate-requirements/) — 10 per-candidate summaries.
- [`AGENTS.md`](../../AGENTS.md) — binding conventions (real-subagent adversarial review; internal-document-references).
- [`ARCHITECTURE-V3-SYNTHESIS-PLAN.md`](../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md) — v1.2 plan revision.
- [`auto-001` (Phase 3.5 dispatch shape)](decisions/auto-001-phase-3.5-dispatch-shape.md), [`auto-002` (U-B path)](decisions/auto-002-ub-path.md), [`auto-003` (BF-L per-RG-view)](decisions/auto-003-bfl-rg-view-choice.md), [`auto-004` (Phase 4 dispatch shape)](decisions/auto-004-phase-4-dispatch-shape.md) — precedent decision briefs.

## Task-aware reading lists

Per the PR-A3 update to the [`autonomous-run` handoff template](../../.claude/skills/autonomous-run/resources/template-handoff-doc.md), this section feeds the next handoff's update to [`AGENT-ENTRY.md` § Reading lists by task](../../AGENT-ENTRY.md#reading-lists-by-task).

### Wave 5.3 dispatch brief authoring (next run's first task)

- Read: [`AGENTS.md`](../../AGENTS.md), [`AGENT-ENTRY.md`](../../AGENT-ENTRY.md), this handoff, [`auto-005` Round 2 final](decisions/auto-005-phase-5-dispatch-shape.md#decision-round-2), [`SKILL-SPEC-34dd1d0274` decision-brief-adversarial-review-lifecycle](../../retrospective/2026-05-25-155/SKILL-SPEC-34dd1d0274-decision-brief-adversarial-review-lifecycle.md), the ADR-ID-to-file mapping table above.
- Skip: per-candidate substrate-requirements (only needed when Wave 5.3 fires).

### Wave 5.3 parallel fanout (per-candidate sub-fanouts)

- Read: [`AGENTS.md`](../../AGENTS.md), [`AGENT-ENTRY.md`](../../AGENT-ENTRY.md), the candidate's [`substrate-requirements/<id>.md`](substrate-requirements/), the parent common ADR(s) from this run's outputs (per the mapping table above), [`overlap.md`](primitives/overlap.md) verdicts for the candidate's variant-bearing primitives, [`adr` skill](../../.claude/skills/adr/SKILL.md), [`SKILL-SPEC-069f0f31bf` parallel-fanout-with-exemplar-and-rubric](../../retrospective/2026-05-25-155/SKILL-SPEC-069f0f31bf-parallel-fanout-with-exemplar-and-rubric.md).

### Phase-6 architecture-spec authorship (BLOCKED until Wave 5.3 closes or waiver)

- Read: [`AGENTS.md`](../../AGENTS.md), this handoff, [`auto-005` Round 2 § Phase 6 gate](decisions/auto-005-phase-5-dispatch-shape.md#wave-53-binding-artifact-convergent-round-2-amendment), all 27 + Wave-5.3 ADRs once Accepted.

## Open questions / suggestions for the next agent to surface

1. **Phase-6 gate enforcement.** This handoff IS the binding artifact. Next agent's first task on Phase-6 dispatch is either (a) dispatch Wave 5.3, or (b) author the waiver brief. Mechanically verifiable.
2. **Per-variant ADR rubric.** Per auto-005 Round 2, variant ADRs have a raised reference floor (≥4) including (parent common ADR + overlap.md verdict + substrate-requirements §3 + corpus citation). Codified in this run's [auto-005 § Revised per-ADR rubric](decisions/auto-005-phase-5-dispatch-shape.md#revised-per-adr-rubric-round-2-amendments-folded-in). Wave 5.3 dispatch brief will reaffirm.
3. **2-candidate primitive scope re-check.** P-25, P-27, P-24 folded as common ADRs in Wave 5.1b. P-30-substrate folded; per-variant state machines deferred. If a Wave-5.3 reviewer flags any 2-candidate fold as inappropriate, the Wave-5.3 brief can split into per-candidate ADRs by authoring an addendum decision brief.
4. **AGENTS.md adoption of retrospective rules.** The 7 [`AGENTS-MD-*`](../../retrospective/2026-05-25-155/) rule drafts from PR #157 stayed un-lifted into canonical `AGENTS.md` during this run. The next agent (or a separate meta-governance run) should propose adoption.

## Concrete pickup steps for the next agent

1. Read [`AGENTS.md`](../../AGENTS.md) (project conventions).
2. Read [`AGENT-ENTRY.md`](../../AGENT-ENTRY.md) (navigation).
3. Read this handoff (pickup brief).
4. Read [`auto-005` Round 2 final decision](decisions/auto-005-phase-5-dispatch-shape.md#decision-round-2) (the parent decision).
5. Author the Wave 5.3 dispatch brief (`auto-006-wave-5.3-candidate-specific-adrs.md`) following the auto-NNN lifecycle pattern with two rounds of real adversarial subagent review per [AGENTS.md `AGENTS-MD-d72e1a4f3c`](../../AGENTS.md#adversarial-review-must-be-real-subagents).
6. Dispatch Wave 5.3 per the brief's verdict.
7. After Wave 5.3 closes, Phase 6 dispatch is unblocked.

## Current git state — Phase-5 PR chain (8 PRs from this session)

PRs opened, top to bottom of stack:

- B5 (forthcoming) — Morning summary `overnight-summary-2026-05-25.md`
- B4 — This handoff doc (this commit)
- B3 — Wave 5.1b ADRs (PR #167)
- B2 — Wave 5.1a + 5.2 ADRs (PR #166)
- B1 — auto-005 decision brief (PR #165)
- A5 — Phase-A verification finding fix (PR #164)
- A4 — CLAUDE.md startup-convention update (PR #163)
- A3 — autonomous-run skill update (PR #162)
- A2 — TL;DR sections (PR #161)
- A1 — AGENT-ENTRY.md (PR #160)
- A0 — Scope envelope (PR #159)
- (Modification to next-agent-prompt-phase-5.md, merged as PR #158)

Subagents dispatched in this run: **22 total** (3 Round-1 + 3 Round-2 adversarial reviewers on auto-005; 16 Wave-5.1a+5.2 ADR-authoring subagents; 9 Wave-5.1b ADR-authoring subagents — wait, that's 31; plus 4 Phase-A verification subagents earlier). Total: **35 subagents** across the run.

When the chain merges, this handoff becomes the canonical pickup point for Wave 5.3.

## Mark prior handoff superseded

Per the handoff discipline, the prior handoff [`SESSION-HANDOFF-2026-05-25-phase-4-close.md`](SESSION-HANDOFF-2026-05-25-phase-4-close.md) is **SUPERSEDED** by this handoff. The pointer in [`AGENT-ENTRY.md` § 2 Current state](../../AGENT-ENTRY.md#2-current-state) is updated by [PR B4](#) to point at this file.
