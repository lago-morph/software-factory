# Scope envelope — Phase-5-entry autonomous run (2026-05-25)

**Author.** Lead agent, autonomous-run session 2026-05-25.
**Status.** User explicitly confirmed scope as "Do both A and B" before this envelope was written; this document formalizes the envelope for rewindability.

This document is the contract between the lead agent and the user for this unattended run. The user reviews against it in the morning. The run drives from the dispatch prompt at [`next-agent-prompt-phase-5.md`](next-agent-prompt-phase-5.md) (as amended by merged PR #158 to add a Phase A verification step).

---

## What I plan to do

**Phase A — Context-slimming implementation (4-5 stacked PRs):**

- **PR A1** — Author [`AGENT-ENTRY.md`](AGENT-ENTRY.md) at repo root per the spec in [`CONTEXT-SLIMMING-PLAN.md`](CONTEXT-SLIMMING-PLAN.md), with task-aware reading lists seeded for Phase 5 dispatch tasks.
- **PR A2** — Add `## TL;DR (≤200 words)` sections at the top of [`ARCHITECTURE-V3-SYNTHESIS-PLAN.md`](ARCHITECTURE-V3-SYNTHESIS-PLAN.md) and [`architectures/v3/candidate-registry.md`](architectures/v3/candidate-registry.md), summarizing structure (not conclusions).
- **PR A3** — Update [`.claude/skills/autonomous-run/SKILL.md`](.claude/skills/autonomous-run/SKILL.md) with end-of-run TL;DR regeneration sub-step and update [`.claude/skills/autonomous-run/resources/template-handoff-doc.md`](.claude/skills/autonomous-run/resources/template-handoff-doc.md) with a Task-aware reading lists section.
- **PR A4** — Startup-prompt convention rewrite ("read AGENTS.md, then AGENT-ENTRY.md") across any session-startup guidance still naming a "read these N files in order" list. May be empty.
- **Verification step** — Dispatch 3 parallel real-subagent verifiers (semantic-preservation, cross-document linkage, pointer-staleness) with fresh context.
- **PR A5** (conditional) — Consolidated fix PR for any verifier findings.

**Phase B — Phase 5 of v3 architecture synthesis (≥4 stacked PRs):**

- **Decision brief `auto-005`** — Phase-5 dispatch shape, two rounds of ≥3 real adversarial subagents each per AGENTS.md `AGENTS-MD-d72e1a4f3c`. Lands as its own stacked PR.
- **Wave 5.1** — Common-primitive ADRs (~13 ADRs, primitives shared ≥3 candidates). 1 exemplar authored inline + ~12 parallel subagents per [`SKILL-SPEC-069f0f31bf`](retrospective/2026-05-25-155/SKILL-SPEC-069f0f31bf-parallel-fanout-with-exemplar-and-rubric.md).
- **Wave 5.2** — Discipline ADRs (~8-12 ADRs, parallel with 5.1). Same exemplar-plus-fanout shape.
- **Wave 5.3** — Candidate-specific ADRs (~30 orphan + ~13 per-variant, fires AFTER 5.1 + 5.2 land so cross-references are stable). Per-candidate parallel fanout (10 subagents).
- **Phase-5-close handoff** — `architectures/v3/SESSION-HANDOFF-2026-05-25-phase-5-close.md`, mark prior handoff superseded, update `AGENT-ENTRY.md` § Current state + Reading lists, run TL;DR regeneration per the A3 skill update.

**Run close:**

- **Morning summary** — `overnight-summary-2026-05-25.md` at repo root, top of the stack.
- **Self-retrospective** — auto-invoked at run close.

## What I plan to NOT do

- I will NOT author the Phase-6 architecture-spec documents per candidate (that's a separate run from the dispatch prompt's perspective).
- I will NOT revise Phase-4 sketches, sub-track outcomes, or substrate-requirements summaries — those are inputs to Phase 5, not editable mid-run.
- I will NOT touch retrospective files for prior runs (#151, #155). The proposed rules from PR #157 are inputs; if I want to lift them into AGENTS.md, that's a morning-review item, not an in-run mutation.
- I will NOT drain `research/manual/` or do research-pipeline work — that's a separate task per the seeded reading list in `AGENT-ENTRY.md`.

## Scale estimate

- **Target PR count:** 12-25. Phase A: 4-5 PRs. Decision brief auto-005: 1 PR. Wave 5.1: 1-3 PRs (may need to split if >15 ADRs in one fanout). Wave 5.2: 1-3 PRs. Wave 5.3: 1-10 PRs (largest fanout, may split per-candidate). Handoff + morning summary: 2 PRs. Bounded by the 30-PR cap.
- **Subagent count estimate:** 80-130. Phase A verification: 3. auto-005 reviewers: 6 (two rounds × 3). Wave 5.1 authors: ~12. Wave 5.2 authors: ~10. Wave 5.3 authors: ~40-50. Per-fanout adversarial reviews: ~8-15 more.
- **Expected duration:** Live wall-clock 4-8 hours of lead-agent driving + queued subagent processing. Some subagent waves may complete in parallel reducing total time.

## First decision points

1. **Branching convention for stacked PRs.**
   - **Lead-agent current best:** `claude/auto-2026-05-25-<chunk-id>-<slug>` (e.g., `claude/auto-2026-05-25-A1-agent-entry`). One branch per PR; each new branch is `git checkout -b <new> <prev-tip>` off the previous chunk's tip. PR base set explicitly to the parent branch.
   - **Alternative:** A single monotonic chain (`claude/auto-2026-05-25` with cumulative commits) — rejected because the dispatch prompt requires reviewable stacked PRs.
   - **If you disagree:** revert this scope envelope's commit, rename branches before merge starts.

2. **PR A2 TL;DR authoring — lead-agent inline vs subagent.**
   - **Lead-agent current best:** Lead-agent authors both TL;DRs inline per the dispatch prompt's explicit instruction ("do NOT dispatch a TL;DR-regeneration subagent at this stage").
   - **Alternative:** Dispatch a TL;DR subagent now — explicitly forbidden by the dispatch prompt.
   - **If you disagree:** N/A — this is dispatched by the prompt itself.

3. **auto-005 Phase-5 dispatch shape — wave-size limit per parallel fanout.**
   - **Lead-agent current best:** ≤15 ADRs per parallel fanout (suggested in the dispatch prompt). Wave 5.3 (~30 orphan + ~13 per-variant) will need to split into ≥3 sub-fanouts (e.g., per-candidate clusters of ≤15 ADRs).
   - **Alternative:** Higher limit (~20-25) with tighter aggregation discipline; or per-candidate single-fanout regardless of size.
   - **If you disagree:** revert auto-005's Round-2 commit before Wave 5.3 fires.

4. **Wave 5.1 vs 5.2 concurrency — parallel or serial.**
   - **Lead-agent current best:** Concurrent (the dispatch prompt explicitly says "parallel with 5.1"). Common-primitive ADRs (5.1) and discipline ADRs (5.2) have no cross-dependencies until Wave 5.3.
   - **Alternative:** Serial — would lengthen the run by ~30-40 minutes wall-clock for no review benefit.
   - **If you disagree:** revert the Wave 5.2 dispatch commit; rebase before Wave 5.3.

## What I'll surface in the morning summary

These are decisions I will **not** auto-decide; they are written into the run's morning summary as morning-review items.

- **Phase-4 retrospective AGENTS-MD rules adoption.** PR #157 (merged) wrote rule drafts under `retrospective/2026-05-25-155/AGENTS-MD-*.md`. Lifting them into the canonical `AGENTS.md` is a meta-governance change. Lead-agent will follow each rule as discipline during the run regardless, but the canonical adoption is a morning-review item.
- **Any Round-2 adversarial-review verdict that escalates a Round-1 strikethrough to a hard switch.** If `auto-005` (or per-fanout decisions) flips alternatives between rounds, the morning user reviews the chain.
- **Any Phase-5 wave that I deliberately split or merged differently than the dispatch prompt suggested.** E.g., if Wave 5.3 ends up as 5 sub-fanouts instead of 10, that's documented as a deferral.
- **TL;DR semantic accuracy.** The verification subagents in Phase A check structure-not-conclusions discipline; if any finding is borderline, surfaced for user adjudication.

## Stop conditions

- **Allowed stops:** context-budget approaching ~70%; hard-failed dependency (auth drop, GitHub unreachable, subagent harness errors after retries); scope envelope completion; 30-PR cap reached; user-message-arrived interrupt.
- **Will NOT stop on:** sub-phase closure (proceed to next sub-phase); ambiguous subagent results (write a clarifying brief); decision-feels-like-user-judgment (handled via brief + two rounds); "I think I'm done" (re-check the deliverables list and carry-forward).

---

## User response

- **Confirm as-written:** yes (explicit, pre-envelope: "Do both A and B")
- **Adjustments:** none received
- **Implicit-confirm after wait:** N/A — explicit confirmation already on record

Run begins immediately after this envelope is committed and pushed as PR A0.
