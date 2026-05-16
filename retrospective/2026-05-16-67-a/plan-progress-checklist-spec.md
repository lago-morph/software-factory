# Spec: `plan-progress-checklist`

## Intent

For multi-cluster / multi-subagent / multi-phase work that lands as a single PR, PLAN.md should contain a **live in-progress checklist** that the orchestrator updates after each subagent return. This skill codifies the structure of that checklist (legend, row format, surprise capture, completion flip) and — critically — the discipline of **flipping rows immediately, before the next subagent dispatch**.

Grounded in PR #67: a 13-cluster Round-10 drain that ran ~9 hours overnight. The PLAN.md `Round-10 manual drain` block was the orchestrator's working memory across the session. It carried the cluster-by-cluster checkboxes, the per-cluster surprises (3–8 each, ~45 total), and the outputs summary. After PR merge, the user caught one lapse: Cluster A and Cluster B had been combined into a single subagent run but their checkbox rows had been left ⬜.

## Trigger

Direct:
- "Set up a progress checklist for this drain"
- "How should I track cluster progress in PLAN.md?"

Proactive:
- A new session begins a multi-cluster / multi-subagent workflow that will produce >3 commits.
- The user signals an overnight or all-day session: "work on this while I sleep", "process these one at a time".

Negative:
- One-shot work that completes in a single subagent run — no checklist needed.

## Inputs

- A path to the project's PLAN.md (or equivalent status doc).
- A scope document (index, brief, plan) enumerating the units of work (clusters, subtasks, phases).
- A PR number once the PR opens.

## Outputs

- A new "Session YYYY-MM-DD ... (Round-N ...; in progress)" bullet under PLAN.md's "Done:" list (or equivalent).
- A nested per-unit checklist under that bullet, using the legend `✅ committed; 🔄 in flight; ⬜ pending`.
- Inline surprise bullets under each ✅ row, captured from the subagent change report.
- A final "✅ COMPLETE" flip + outputs summary at the round-bullet level when all units land.

## Workflow

1. **Create the round-bullet** at session start, immediately after the orchestrator-decisions table commits. Include: date, scope summary, PR number (or placeholder), and "in progress" tag.
2. **Write the legend line** verbatim: `Per-unit progress (✅ committed; 🔄 in flight; ⬜ pending):`
3. **Add one row per unit of work.** Each row: `    - ⬜ **Unit name** (sub-scope) → target outputs`. Indent for nesting.
4. **After each subagent return (or unit completion)**:
   a. Flip `⬜ → ✅`.
   b. Inline 3–8 surprises from the subagent's change report after the `✅` row, formatted as a long bullet sub-paragraph (NOT a nested list — keep it as one flowing description so it survives markdown rendering and grep).
   c. **Do this BEFORE dispatching the next subagent.** The discipline is: subagent returns → orchestrator updates checklist → commits → pushes → only then next dispatch.
5. **If a single subagent run covers multiple checklist rows** (combined drain), flip ALL covered rows. Leaving any ⬜ behind is the dominant lapse pattern.
6. **At session end**: flip the round-bullet header from "in progress" → "✅ COMPLETE". Add an inline "**Outputs:**" summary listing all new files, all upgraded files, all promoted failure modes, all primary-source closures, the retrospective filename, and the PR number.
7. **Cross-check the legend.** A `grep -cE "⬜|🔄" PLAN.md` should show 0 (or 1 if the legend line itself uses the symbols).

## Concrete examples

### Example 1: The PR #67 round-bullet (final state, post-fix)

```
- **Session 2026-05-16 (overnight) — Round-10 manual drain (71 sources / 15 clusters; ✅ COMPLETE)** — User dropped ~71 new sources into `research/manual/` ... PR #67 ready-for-review (non-draft, subscribed for activity). **Outputs:** 11 new numbered reports (27–37) + 8 existing-report upgrades + 5 followup updates + 10 new failure modes promoted F40–F49 + 9 figures across 6 figure dirs + `openai.com/index/*` host class FULLY primary-anchored. Retrospective at `retrospective/2026-05-16-67.md` with 2 skill specs + 8 AGENTS suggestions + 5 proposed ADRs.
  - Per-cluster progress (✅ committed; 🔄 in flight; ⬜ pending):
    - ✅ **Cluster A — 2389 product pages** (Coven/Mammoth/Smasher/Tracker/dotpowers) → followup/02 + report 07 (combined with Cluster B in a single subagent run; details in the Cluster A+B drain note below)
    - ✅ **Cluster B — 2389 GitHub repos** (5 READMEs) → followup/02 + report 07 (combined with Cluster A in a single subagent run; details in the Cluster A+B drain note below)
    - ✅ **Cluster A+B drain (combined subagent, completed 2026-05-16):** Updated ... +3 paragraphs of surprises ...
    - ✓ **Cluster D — Codex developer docs (core)** — all duplicates, skipped
    - ... [13 more cluster rows, all ✅] ...
```

### Example 2: The lapse and the fix

In PR #67, the post-merge state initially had:

```
    - ⬜ **Cluster A — 2389 product pages** ...
    - ⬜ **Cluster B — 2389 GitHub repos** ...
    - ✅ **Cluster A+B drain (combined subagent, completed 2026-05-16):** ...
```

Cluster A and B individual rows ⬜; the combined drain note ✅. The user caught this and asked "Is plan.md updated?". The fix: flip both ⬜ → ✅ and add the "(combined with the other in a single subagent run)" suffix to both rows.

Lesson: when one subagent run covers multiple pre-allocated checklist rows, every one of those rows needs flipping at the same commit, not in a separate corrective commit.

## Anti-patterns

- **Batching checkbox flips across multiple subagent returns.** Defeats the working-memory purpose; if the session terminates, the in-flight state is corrupted.
- **Letting a subagent edit the checklist.** The orchestrator owns PLAN.md exclusively. Subagents return change reports; orchestrator transcribes.
- **Skipping the surprise inline.** Surprises captured at the moment of transcription are crisp; surprises reconstructed from re-reading the diff later are lossy. Always inline at flip time.
- **Combining the flip with the next commit.** One commit per cluster — the checklist update is part of *that* cluster's commit, not the next.
- **Removing the legend line at completion.** Keep it; it's the audit trail for the symbol convention.
- **Renaming the round-bullet from "Round-N (in progress)" to "Round-N" instead of "Round-N (✅ COMPLETE)".** Keep the explicit completion marker — searchable downstream.
- **Flipping the round-bullet to COMPLETE while ⬜ checklist rows remain.** The cross-check `grep -cE "⬜|🔄" PLAN.md` exists for exactly this case.

## Acceptance criteria

1. The PLAN.md round-bullet legend includes `⬜` / `🔄` / `✅` and a header naming the round.
2. Every unit of work has a checklist row that is exactly one of `✅` / `🔄` / `⬜` at any given commit.
3. Each `✅` row has an inline 3–8-surprise bullet captured at flip time.
4. The grep cross-check (`grep -cE "⬜|🔄" PLAN.md`) returns 0 at session end (or 1 if the legend line itself uses the symbols).
5. The round-bullet header carries explicit COMPLETE status with an outputs summary at session end.
6. No ⬜ row outlives the subagent run that covers it — flip happens *before* the next dispatch.

## Files this skill creates / modifies

- `research/PLAN.md` — the round-bullet + checklist + surprises + final COMPLETE flip.
- Optional template at `.claude/templates/plan-round-bullet.md`.
