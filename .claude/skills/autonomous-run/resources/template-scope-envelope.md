# Scope envelope — `<run-name>`

**Author.** Lead agent, autonomous-run session `<YYYY-MM-DD>`.
**Status.** Awaiting user confirmation (or implicit confirmation after a short wait).

This document aligns intent between the lead agent and the user before the unattended run begins. It is the contract: what the run will produce, what it will *not* touch, and how the lead agent will handle the first decision points. The morning user reviews against this envelope.

---

## What I plan to do

3-7 bulleted deliverables. Each one sentence. Be specific (PR-shaped chunks, not vague themes).

- `<Deliverable 1>` — example: "Open Phase 4 with per-candidate substrate-requirements summaries (10 subagents + lead-agent aggregation), landing as one PR per candidate."
- `<Deliverable 2>` — example: "Resolve Phase-4 entry blocker on BF-L's per-RG-view choice via decision brief auto-003 with two rounds of adversarial review."
- `<Deliverable 3>` — etc.

## What I plan to NOT do

2-4 bulleted boundaries. Adjacent work I will not touch unless you explicitly authorize.

- `<Boundary 1>` — example: "I will NOT begin Phase 5 ADR authoring; that's a separate run."
- `<Boundary 2>` — example: "I will NOT re-open Phase 3.5 sketches; the buildability outcomes are final unless a Phase-4 brief specifically requests revision."

## Scale estimate

- **Target PR count:** `<N>` (aim for upper-bound of 30-PR cap; typical 20-30 for a full unattended run).
- **Subagent count estimate:** `<M>` (rough; depends on dispatch shapes chosen at decision briefs).
- **Expected duration:** `<H>` hours of live wall-clock work + queued subagent processing.

## First decision points

The 2-4 questions I will hit early in the run that would normally need user input. For each, I list my current best answer and the alternative.

1. **`<Question 1>`**
   - **Lead-agent current best:** `<option>` because `<reasoning>`.
   - **Alternative:** `<option>`.
   - **If you disagree:** revert commit `<TBD>` on PR `<TBD>`.
2. **`<Question 2>`** — same structure.

## What I'll surface in the morning summary

Explicit list of items that will land as morning-review items (not auto-decided). These are decisions that genuinely need user input even after adversarial review rounds — e.g., meta-governance changes (lifting a per-candidate rule to a global rule), or substantive scope decisions that affect downstream phases.

- `<Item 1>` — example: "Should the Phase-3.5.5 RG-primitive rule lift to a global synthesis rule (apply to all future RG primitives)? Lead-agent recommendation: yes."
- `<Item 2>` — etc.

If there are zero items I expect to surface, say so explicitly: "I expect to close all decisions in-run; no morning-review items anticipated."

## Stop conditions

What would cause me to stop the run early:

- **Allowed stops:** context-budget exhaustion approaching, hard-failed dependency (auth / GitHub / subagent harness), scope envelope completion, 30-PR cap, user-message-arrived interrupt.
- **Will NOT stop on:** sub-phase closure, ambiguous subagent results, decision-feels-like-user-judgment-territory (decision briefs handle those).

---

## User response (filled in by user, or left blank for implicit-confirm)

- **Confirm as-written:** yes / no
- **Adjustments:** `<free-text>`
- **Implicit-confirm after wait:** yes (if no reply within `<duration>`)

Once confirmed (explicitly or implicitly), the run begins. The envelope is committed as the first file of the run for rewindability.
