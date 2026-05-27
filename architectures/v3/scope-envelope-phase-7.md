# Scope envelope — Phase 7 back-fill audit (autonomous run)

**Author.** Lead agent, autonomous-run session 2026-05-27.
**Status.** Awaiting user confirmation (or implicit confirmation after a short wait).
**Branch base.** `claude/phase-7-backfill-audit-uwVRp` (off `origin/main`).
**Pre-flight verification (per [`AGENTS-MD-4f8c2a1b03`](../../AGENTS.md#pre-flight-prior-phase-merge-state-verification)).** ✅ PASSED at session start:
- 10 spec files in `origin/main` under [`architectures/v3/specs/`](specs/) ✓
- [Phase-6-close handoff](SESSION-HANDOFF-2026-05-26-phase-6-close.md), [`mandate-fit-matrix.md`](mandate-fit-matrix.md), [`phase-6-verification-findings.md`](phase-6-verification-findings.md) all in `origin/main` ✓
- Archive scope confirmed finite: [`archive/synthesis-v1-v2/`](../../archive/synthesis-v1-v2/) (2 substantive files) + [`archive/architectures-v2/`](../../archive/architectures-v2/) (5 architecture files + failure-modes.md) = **7 substantive files** total

This document aligns intent between the lead agent and the user before the unattended Phase-7 run begins.

---

## What I plan to do

7 PR-shaped deliverables, in order:

1. **PR 1: This scope envelope** as the first commit of the run (rewind-to-pre-run anchor).
2. **PR 2: `auto-007` Phase-7 dispatch-shape brief** with two rounds of real adversarial review (≥3 reviewers each round, 3 verdict tiers per [`AGENTS-MD-8a7029647f`](../../AGENTS.md#adversarial-review-verdict-tiers)), authored before any back-fill subagent fires per [`AGENTS-MD-a43c9584c9`](../../AGENTS.md#dispatch-prompt-edit-before-run-pattern) and the [auto-006 precedent](decisions/auto-006-phase-6-dispatch-shape.md).
3. **PR 3: Per-candidate back-fill exemplar** (lead-agent-authored back-fill notes for the least-contested candidate per [`AGENTS-MD-eec503a3c2`](../../AGENTS.md#exemplar-before-parallel-uniform-schema-fanout)) — gating fanout dispatch.
4. **PR 4: Phase-7 fanout omnibus** — 10 per-candidate back-fill notes (one per candidate spec) + 2 bias-guard outputs (silent-absorption auditor + historian per the [v1.2 plan § Phase 7](../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md#phase-7--back-fill-audit-per-candidate-against-archived-v1v2-revised-in-v12)) + lead-agent-authored aggregation file at [`backfill-notes.md`](backfill-notes.md). Consolidated per [`AGENTS-MD-d71e845b29`](../../AGENTS.md#sub-wave-pr-consolidation-when-files-are-disjoint) if files are disjoint (expected).
5. **PR 5 (conditional): Spec-patch sub-PRs** for any absorbed archive material that warrants amending a Phase-6 spec — only fires if back-fill audit surfaces material judged absorbable; if zero specs need patching, this PR is skipped and the morning summary notes that explicitly.
6. **PR 6: Phase-7-close session handoff** at `architectures/v3/SESSION-HANDOFF-2026-05-27-phase-7-close.md` with Phase 8 (lean-eval design) entry posture, AGENT-ENTRY.md Section-2 link target updated, task-aware reading lists for Phase 8 dispatch.
7. **PR 7: Morning summary** at repo-root `overnight-summary.md` + self-retrospective at `retrospective/2026-05-27-<PPP>/` with full package (main report + SKILL-SPEC + ADR-draft + per-rule AGENTS-MD files per [`AGENTS-MD-1d7c94415e`](../../AGENTS.md#full-retrospective-package-lean-mode-is-anti-pattern)).

## What I plan to NOT do

- **I will NOT begin Phase 8** (lean-eval design per candidate). Phase 8 is its own run; this run hands off the entry posture only.
- **I will NOT re-author any Phase-6 spec from scratch.** Spec patches in PR 5 are surgical amendments (additive §-level edits with §0 ADR-citation index preservation per [ADR 0065](../../docs/adr/0065-section-0-adr-citation-index-table.md)); never wholesale rewrites.
- **I will NOT reopen mandate-fit matrix decisions** (DEC-1.a, DEC-2 schema). Back-fill is additive against the archive, not a re-litigation of resolved Phase-6 cell decisions.
- **I will NOT touch the Phase-5-close handoff BF-M row** (the non-load-bearing carry-forward #3 from the Phase-6-close handoff). The [Phase-6-close erratum](SESSION-HANDOFF-2026-05-26-phase-6-close.md#adr-0049-documentation-erratum) is the canonical correction; an in-place fix is reversible and can be a Phase-8 doc-hygiene pass.

## Scale estimate

- **Target PR count:** **7 PRs** (well under the 15-PR Phase-7 budget cited in the dispatch prompt; well under the 30-PR autonomous-run cap). This is a deliberate ceiling — Phase 7 is back-fill-only and should not balloon. If PR 5 fires multiple times (multiple spec patches), the cap remains: those become sub-PRs of a single omnibus.
- **Subagent count estimate:** **~20 subagents total** — 6 adversarial reviewers across auto-007 R1+R2 + 10 per-candidate back-fill subagents (one per spec) + 2 bias-guard subagents (silent-absorption + historian) + 1-2 lead-agent-managed aggregation/patch subagents if needed + 4+ retrospective-package subagents at run close.
- **Expected duration:** **~3-5 hours** wall-clock for the lead agent (subagent waits dominate). Largest single wait: the parallel 10+2 back-fill fanout wave.

## First decision points

The 5 questions queued for `auto-007`, with my current best answers and rewind paths:

1. **Wave shape.** **Best: 10 per-candidate parallel subagents in one wave** (one per Phase-6 spec, each audits its candidate against the 7-file archive).
   - **Alternative:** sub-wave by mandate (3 GF + 3 BF + 4 U).
   - **Rewind:** revert PR 2 commit. Defer to user; alternative re-fires fanout with different sub-wave plan.
2. **Archive scope.** **Best: both `archive/synthesis-v1-v2/` AND `archive/architectures-v2/`** (7 substantive files; finite and verified).
   - **Alternative:** only `archive/synthesis-v1-v2/` (narrower; might miss v2-only material).
   - **Rewind:** revert PR 2.
3. **Per-candidate rubric classification taxonomy.** **Best: `absorbed | rejected (reason) | not-applicable-to-candidate-mandate | TBD-historian-only`** (4-token).
   - **Alternative:** the 3-token default from the dispatch prompt (`absorbed | rejected (reason) | TBD`).
   - **Rewind:** revert PR 2; relabel cells in subsequent re-fanout.
4. **Aggregation file vs per-candidate file shape.** **Best: per-candidate `backfill-notes/<id>.md` × 10 + lead-agent-authored aggregation at `backfill-notes.md`** (both, not either-or). Per-candidate files are the canonical artifacts authored by parallel subagents (disjoint writes — no merge conflicts); the aggregation is the cross-candidate view derived by the lead agent at fanout-close.
   - **Alternative:** aggregation-only (the dispatch prompt default).
   - **Rewind:** revert PR 4; aggregation file alone is preserved.
5. **Bias-guard dispatch timing.** **Best: concurrent with the per-candidate fanout** (independent input streams; both auditors are read-only against the archive and the Phase-6 specs; no cross-dependence). The two auditors are functionally independent so no waiting is justified.
   - **Alternative:** after the per-candidate fanout completes (so the silent-absorption auditor can compare per-candidate verdicts to its own findings; the historian is unaffected).
   - **Rewind:** revert PR 4.

## What I'll surface in the morning summary

Decisions and adjudications needing user input even after adversarial review rounds:

1. **Any silent-absorption auditor / historian findings that contradict a per-candidate subagent's `rejected` verdict.** Lead-agent recommendation depends on the disagreement; surface verbatim for user adjudication.
2. **Any back-fill material that the historian flags as appearing in zero candidate specs but the lead agent judges as load-bearing.** Could trigger a Phase 8 entry blocker (e.g., a missing primitive class).
3. **Whether to fire the optional Phase-6-followup #2 (cross-spec characterization audit of shared framework ADRs)** during Phase 7 or defer to Phase 8 — depending on what the per-candidate fanout surfaces about ADR 0036 framing.
4. **Whether any spec patch in PR 5 crosses the "surgical amendment" threshold** (e.g., a §0 ADR-citation index row added, a §5 falsifying-scenario clarified). The user reviews these patches at merge time.

If zero contentious findings emerge, the morning summary will say so explicitly and the merge order will be straightforward.

## Stop conditions

- **Allowed stops:** context-budget exhaustion approaching (~70% threshold per autonomous-run skill), hard-failed dependency (auth / GitHub / subagent harness — recovery via [`github-connection-resilience`](.claude/skills/github-connection-resilience/SKILL.md) first), scope envelope completion (7 deliverables shipped), 30-PR cap hit, user-message-arrived interrupt.
- **Will NOT stop on:** Phase 7 sub-step closure (start the next sub-step or write the next decision brief), ambiguous subagent results (write a follow-up brief and dispatch a clarifying subagent), decision-feels-like-user-judgment-territory (the brief + Round 1 + Round 2 protocol handles that — don't freeze).

## Rewind structure

- **Pre-run:** revert this PR (PR 1) to remove the envelope and return to bare `claude/phase-7-backfill-audit-uwVRp` HEAD.
- **Pre-fanout:** revert PR 2 (auto-007) to drop the dispatch brief but keep the envelope.
- **Pre-back-fill:** revert PR 3 (exemplar) — fanout becomes uncalibrated.
- **Pre-spec-patches:** revert PR 4 (fanout omnibus) to drop all back-fill notes.
- **Pre-handoff:** revert PR 5 (if it fires) to drop spec patches.
- **Pre-summary:** revert PR 6 to drop the handoff (next session re-inherits the Phase-6-close handoff as active).

---

## User response (filled in by user, or left blank for implicit-confirm)

- **Confirm as-written:** _(awaiting reply)_
- **Adjustments:** _(awaiting reply)_
- **Implicit-confirm after wait:** yes — autonomous-run skill default; if no reply within a short wait, the lead agent proceeds with the envelope as written.

Once confirmed (explicitly or implicitly), the run begins with `auto-007` authoring (PR 2).
