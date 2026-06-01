# Scope envelope — Phase 8 (lean-eval design per candidate)

**Author.** Lead agent, autonomous Phase-8 dispatch session 2026-05-28.
**Status.** Posted to user; awaiting confirmation (or implicit confirmation after a short wait per the [autonomous-run skill](../../.claude/skills/autonomous-run/SKILL.md)).

This document aligns intent between the lead agent and the user before the Phase-8 unattended run begins. It is the contract: what the run will produce, what it will *not* touch, and how the lead agent will handle the first decision points. The morning user reviews against this envelope.

Per [`AGENTS-MD-a43c9584c9`](../../AGENTS.md#dispatch-prompt-edit-before-run-pattern): the dispatch prompt [`next-agent-prompt-phase-8.md`](../../archive/PR-193-next-agent-prompt-phase-8.md) was committed at `1077358` on main before this run fired; this envelope cites it verbatim.

---

## What I plan to do

- **PR 1 — Scope envelope.** This file. Rewind-to-pre-run anchor for Phase 8.
- **PR 1.5 (conditional on user confirmation) — Adoption of 5 Phase-7 retro AGENTS-MD rules** into canonical [`AGENTS.md`](../../AGENTS.md). See [§First decision points](#first-decision-points) item 1.
- **PR 2 — `auto-008` decision brief** for Phase-8 dispatch shape at `architectures/v3/decisions/auto-008-phase-8-dispatch-shape.md`. Two rounds of real adversarial review, ≥3 reviewers each per [`AGENTS-MD-d72e1a4f3c`](../../AGENTS.md#adversarial-review-must-be-real-subagents). Pre-folds the auto-007 audit-trail amendments at Round-1 authoring time (commit-SHA pinning, time-anchored honest-acks, Appendix A scaffold, 3-tier verdict commitment, TL;DR structure-not-conclusions, PR-webhook commitment, framework-ADR pairing, skip-discipline auditability) per the candidate [`AGENTS-MD-4a7c2e9f6b`](../../retrospective/2026-05-27-191/AGENTS-MD-4a7c2e9f6b-adversarial-review-amendment-inheritance.md) rule.
- **PR 3 — Lead-agent-authored exemplar lean-eval brief** for the least-contested candidate (likely GF-M or BF-S; chosen at authoring time). Pre-fanout self-check gate before Wave 8.1 dispatch.
- **PR 4 — Wave 8.1 fanout omnibus.** 9 sibling per-candidate lean-eval briefs at `architectures/v3/lean-evals/<id>.md`. Mandatory `falsifying-outcome:` YAML field; Phase-7 cite obligations propagated per-candidate from the auto-008 brief's pre-authored mapping. Consolidated per [`AGENTS-MD-d71e845b29`](../../AGENTS.md#sub-wave-pr-consolidation-when-files-are-disjoint).
- **PR 5 — Wave 8.2 cross-candidate evaluator-brief** at `architectures/v3/lean-evals/00-cross-candidate.md` + 3 bias-guards (domain-practitioner concurrent per-candidate; falsification-designer concurrent per-candidate; hypothesis-falsifier serial after Wave 8.1 — see [§First decision points](#first-decision-points) item 3). May split into two PRs if coordination forces a boundary.
- **PR 6 — Phase-8-close session handoff** at `architectures/v3/SESSION-HANDOFF-2026-05-28-phase-8-close.md` + [`AGENT-ENTRY.md`](../../AGENT-ENTRY.md) Section-2 rotation; downstream simulator-harness entry posture.
- **PR 7 — Run summary + full-package retrospective** at `run-summary-2026-05-28-phase-8.md` + `retrospective/2026-05-28-NNN/` (full package authored inline per [`AGENTS-MD-1d7c94415e`](../../AGENTS.md#full-retrospective-package-lean-mode-is-anti-pattern)).

## What I plan to NOT do

- **No simulator-harness execution.** Phase 8 designs the lean-evals; running them against simulator harnesses is post-v3 work (per v1.2 plan).
- **No Phase-6 spec patches.** Wave 7.3 was deliberately NOT FIRED with matrix-flag alternative per [aggregation §5](backfill-notes.md#5-wave-7-3-spec-patch-decision-lead-agent-decision); Phase 8 honors that decision (cite obligations land inside lean-eval briefs, not spec patches).
- **No re-authoring of Phase-6 specs or Phase-7 back-fill notes.** They are inputs only; if a per-candidate lean-eval brief surfaces a defect in its candidate's spec, the brief flags it in §6 (open critique references) and the spec is left as-is.
- **No new candidate-set changes.** The 10-candidate registry is frozen post-Phase-4 ([`candidate-registry.md`](candidate-registry.md)).

## Scale estimate

- **Target PR count:** 7-8 (against ≤15 phase budget cap; comfortable margin). Phase 7 closed at 6 PRs; Phase 8 adds one for the cross-candidate evaluator-brief if it's stacked separately from bias-guards.
- **Subagent count:** ~22-23 total.
  - 6 adversarial reviewers on auto-008 (3 Round-1 + 3 Round-2)
  - 9 Wave-8.1 fanout subagents (10 candidates minus exemplar)
  - 1 Wave-8.2 cross-candidate evaluator-brief subagent
  - 3 bias-guards (domain-practitioner, falsification-designer, hypothesis-falsifier)
  - ~3-4 retrospective-package authoring subagents at run close
- **Expected duration:** several hours of live wall-clock work + queued subagent processing.

## First decision points

The 4 questions I will hit early in the run that would normally need user input. For each, I list my lead-agent best-call and the alternative.

### 1. Adopt 5 Phase-7 retro `AGENTS-MD-*` rules into canonical [`AGENTS.md`](../../AGENTS.md) before auto-008 fires?

- **Lead-agent best:** **Adopt all 5 in a dedicated PR 1.5 before auto-008**, so auto-008 can cite them by stable AGENTS-MD-<hash> ID. The 5 rules are all directly relevant to auto-008's authoring discipline:
  - [`AGENTS-MD-4a7c2e9f6b`](../../retrospective/2026-05-27-191/AGENTS-MD-4a7c2e9f6b-adversarial-review-amendment-inheritance.md) — adversarial-review amendment-inheritance from prior auto-NNN. **Directly load-bearing** for auto-008 (which inherits structure from auto-007).
  - [`AGENTS-MD-8e5d3a7c4b`](../../retrospective/2026-05-27-191/AGENTS-MD-8e5d3a7c4b-phase-followup-bias-guard-fold.md) — Phase-followup carry-forward absorption into bias-guard mandates. Relevant for Wave-8.2 bias-guards' input scope.
  - [`AGENTS-MD-5b3e8a1c2f`](../../retrospective/2026-05-27-191/AGENTS-MD-5b3e8a1c2f-silent-absorption-confidence-threshold.md) — silent-absorption-finding confidence-threshold rule. Generalizes to any cross-cutting auditor (the hypothesis-falsifier qualifies).
  - [`AGENTS-MD-7d9c4e1b3a`](../../retrospective/2026-05-27-191/AGENTS-MD-7d9c4e1b3a-matrix-flag-over-spec-patches.md) — matrix-flag over spec-patches when bias-guard recommends it. Could fire in Phase 8 if a bias-guard surfaces a "rewrite brief vs flag in cross-candidate" question.
  - [`AGENTS-MD-2f8a6c9d51`](../../retrospective/2026-05-27-191/AGENTS-MD-2f8a6c9d51-per-candidate-engagement-over-blanket-skip.md) — per-candidate engagement over blanket-skip for prior-phase defaults. Relevant if auto-008 proposes to "skip" any Phase-6/Phase-7 inherited material.
- **Alternative:** Defer adoption; follow the patterns informally in auto-008 and flag the gap in honest-acks.
- **If you disagree with the lead-agent best-call:** revert PR 1.5; auto-008 Round-1 reviewers will not be able to ground the patterns by AGENTS-MD-<hash> but can still apply them as drafts.
- **Will surface via [`AskUserQuestion`](#)** as the [dispatch prompt](../../archive/PR-193-next-agent-prompt-phase-8.md) explicitly directs.

### 2. Tier-table calibration at auto-008 Round 1

- **Lead-agent best:** Adopt **Light 5000-6500 / Heavy 5500-7500** at Round-1 authoring time, per the Phase-7 advisory carry-forward ([aggregation §6.1](backfill-notes.md#61-word-budget-overrun-pattern--auto-007-round-3-calibration-warranted)) — 9-of-10 candidates landed over their Phase-7 tier budgets. Don't wait for Round-2 reviewers to surface what we already know.
- **Alternative:** Hold to auto-007's Light 3500-5000 / Heavy 4500-6500 baseline.
- **If you disagree:** override at auto-008 Round-2 (the reviewers will likely amend).

### 3. Bias-guard concurrency shape

- **Lead-agent best:** **Domain-practitioner + falsification-designer fire per-candidate, concurrent with Wave 8.1** (their input is per-brief, independent of sibling briefs). **Hypothesis-falsifier fires serial after Wave 8.1 closes** (depends on reading all 10 briefs to name the cross-candidate falsifying result pattern). Honors the [ADR-3f8c1e5b7a precedent](../../retrospective/2026-05-27-191/ADR-3f8c1e5b7a-bias-guards-concurrent-with-fanout.md): concurrent IF input streams are independent of per-candidate outputs.
- **Alternative:** All 3 bias-guards fire serial after Wave 8.1. Loses the wall-clock advantage of concurrent firing for domain-practitioner and falsification-designer.
- **If you disagree:** rewind the bias-guard PR(s) and re-dispatch.

### 4. Exemplar candidate selection (GF-M vs BF-S)

- **Lead-agent best:** Decide at exemplar-authoring time based on which candidate produces the cleanest **falsifying-outcome demonstration**. Default lean toward **GF-M** (greenfield-light; single-dominant lineage; least cross-mandate noise; cleanest scenario-set framing for §1).
- **Alternative:** **BF-S** (Phase-7 already used it as exemplar; reduces lead-agent context-switching cost; brownfield-light has known-good Atelier-primary lineage).
- **If you disagree:** swap before exemplar PR opens.

## What I'll surface in the morning summary

- Outcome of the auto-008 brief (Round-1 + Round-2 verdicts; whether any `reject-with-counter-proposal` surfaced).
- Whether any per-candidate lean-eval brief was re-authored due to subagent self-check failure.
- The DEC-1.a falsifying result pattern as named in the cross-candidate evaluator-brief — for user review before downstream simulator-harness execution (this is the load-bearing falsifier surface and the morning user should sanity-check it).
- Any per-candidate lean-eval whose `falsifying-outcome:` field reads as soft/hand-wavy (the falsification-designer's verdict on each brief).
- Phase-8-followup deferrals if any (none anticipated; Phase 8 produces design artifacts only, not patches).

## Stop conditions

- **Allowed stops:** context-budget exhaustion at ~70%; hard-failed dependency (auth/GitHub/subagent harness); 7-8 PR target met with all deliverables landed; 15-PR phase cap hit; user-message-arrived interrupt.
- **Will NOT stop on:** sub-wave closure (continue to next wave); ambiguous subagent results (re-dispatch clarifying subagent); decision-feels-like-user-judgment-territory (write decision brief, run two adversarial rounds, pick a side).

---

## User response (filled in by user, or left blank for implicit-confirm)

- **Confirm as-written:** *(pending)*
- **Adjustments:** *(pending)*
- **Implicit-confirm after wait:** yes (the [autonomous-run skill](../../.claude/skills/autonomous-run/SKILL.md) treats no-reply as implicit confirmation in unattended mode)

Once confirmed (explicitly or implicitly), the run begins. The envelope is committed as PR 1 of the Phase-8 stack for rewindability.
