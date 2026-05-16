# Spec: `subagent-registry-preallocation`

## Intent

When the lead agent dispatches N≥2 subagents in parallel, and each subagent will independently propose new entries to a **shared registry** — a numbering scheme (failure-mode IDs F1, F2, F3, …; ADR numbers; report numbers; semantic-version bumps), a file-naming scheme (`NN-<slug>.md`), or any ordered ID space — collisions are nearly guaranteed unless the orchestrator allocates slot ranges *before* dispatch. Each subagent runs without visibility into what the others are proposing, looks at the latest committed number (e.g., F35), and proposes the next one (F36). When two subagents both do that, both propose F36, and the lead agent has to reconcile at integration time.

This skill makes pre-allocation a mandatory step in any parallel dispatch where shared registries are touched. The cost is small (one extra step in the orchestrator's dispatch checklist, plus one line of allocation per subagent). The cost of skipping it is a documentation-only collision that has to be untangled at merge time and may propagate confusion if not caught (the integrator could miss the collision and end up with two distinct phenomena both numbered F36).

The Round-9 manual drain demonstrated the failure mode concretely: subagents A and B each independently proposed F36 and F37 for *different phenomena* (A: vocabulary lint debt, point-spec/region-mismatch; B: instruction-following ceiling, silent contradictory-prompt collapse). The collision was caught at lead-agent integration time and resolved by adding a §3.6 to PLAN.md documenting the collision and a suggested numbering reconciliation. The pre-allocation discipline would have eliminated the collision entirely.

## Trigger

**Direct user phrases:**

- *"dispatch N subagents in parallel"*
- *"fan out this work"*
- *"do these in parallel"*

**Proactive triggers — activate without being asked:**

- Any dispatch of ≥2 subagents whose briefs include language like "propose new failure modes (F36+)" or "next available report number" or "draft an ADR".
- Any dispatch where the subagents will write to a directory whose existing files follow a strict numbering convention (`research/NN-*.md`, `docs/adr/NNNN-*.md`, `retrospective/YYYY-MM-DD-NN/`).
- Any dispatch where the subagents will append to a shared catalog (`research/00-synthesis.md` §4 failure modes; `INDEX.md` rows; `architectures/00-comparison.md` §2.4).

**Negative triggers — do NOT activate:**

- Single-subagent dispatches (no other agent to collide with).
- Parallel dispatches where each subagent writes to a uniquely-named file with no shared numbering scheme (e.g., three subagents each writing to a different existing file by name).
- Dispatches where the lead agent is the only entity assigning the IDs *after* subagents return (e.g., subagents propose anonymous candidates, lead agent numbers them at integration). This is an alternative discipline — pre-allocation is for the case where subagents bake numbers into their drafts.

## Inputs

- **The dispatch plan** — the lead agent's list of subagents about to be launched, each with its file target and proposed deliverables.
- **The shared registries touched** — the registries (numbering schemes, file-naming conventions, ID spaces) each subagent will write to or propose into.

## Outputs

- An updated dispatch plan in which each subagent's brief contains an explicit **registry-allocation block** naming the slot range that subagent is exclusively authorized to use.
- Optional: a temporary `dispatch-allocation.md` scratch note in `/tmp/` for the orchestrator's own reference. Not committed.

## Workflow

1. **Enumerate the shared registries** the dispatched subagents will touch. Common registries in this repo:
   - Failure-mode numbers (`F1`, `F2`, …) — catalogued across `research/00-synthesis.md` §4, `research/13-round-2-synthesis.md` §3, recent reports.
   - Report numbers (`research/NN-*.md`) — strict ascending sequence.
   - Followup numbers (`research/followup/NN-*.md`) — strict ascending sequence.
   - ADR numbers (`docs/adr/NNNN-*.md`) — strict ascending sequence.
   - Retrospective numbers (`retrospective/YYYY-MM-DD-NN/`) — per-day sequence, OR the per-PR scheme introduced 2026-05-14.
   - Index rows that need new entries (`research/INDEX.md`).

2. **Find the current high-water mark for each registry.** Quick recipes:
   - F-mode high-water mark: `grep -rho 'F[0-9]\+' research/ | sort -t F -k 2 -n | tail -1` — but verify by also reading `00-synthesis.md` §4 and `13-round-2-synthesis.md` §3 because failure modes get proposed in individual reports too (e.g., F34 in `followup/12-brier-pace-layers.md`).
   - Report number high-water mark: `ls research/ | grep -oE '^[0-9]+' | sort -n | tail -1`.
   - ADR high-water mark: `ls docs/adr/ | grep -oE '^[0-9]+' | sort -n | tail -1`.

3. **Allocate non-overlapping ranges to each subagent.** Reserve generously — a subagent that might propose 1–4 new F-modes should get a 4-slot range. Example for two subagents working on F-modes with high-water mark F35:

   - Subagent A: F36–F39 (4 slots).
   - Subagent B: F40–F43 (4 slots).

   Unused slots are released back to the pool after the dispatch completes; the lead agent renumbers if needed for catalog continuity.

4. **Embed the allocation in each subagent's brief.** Use a "Registry allocation (your exclusive range)" block near the top of the brief. Be explicit that the subagent must use only IDs from its allocated range; if it has more candidates than slots, it should flag the overflow in its report-back rather than reaching outside the range.

   Example brief insertion:

   > **Registry allocation (your exclusive range):**
   > - Failure-mode numbers: F36–F39 (4 slots). Use these IDs and only these IDs for any candidate failure modes you propose. If you have more candidates than slots, list the overflow in your report-back without an ID and the lead agent will allocate at integration.

5. **Cross-check the dispatch plan** before launching. If two briefs claim the same range, you misallocated — fix before dispatch, not after.

6. **At integration time, audit the actual IDs used.** `grep -ho 'F3[0-9]' research/25-*.md research/26-*.md | sort -u` — if a subagent strayed outside its range or two subagents share an ID, that's a real bug and needs reconciliation before commit.

## Concrete examples

### Example 1 — Round-9 manual drain (the session that demonstrated the failure mode)

**Dispatch plan (as it actually ran, without this skill):**

- Subagent A: write `research/25-requirements-engineering-foundations.md` from 5 RE/SE sources. Brief said *"DO NOT invent failure modes (F36+) without flagging them as proposals."*
- Subagent B: write `research/26-prompt-underspecification-academic.md` from 3 academic papers. Brief said *"DO NOT invent failure modes (F36+) without flagging them as proposals."*

**Actual outcome:**

- Subagent A proposed F36 (vocabulary lint debt), F37 (point-spec/region-mismatch), F38 (architecture/specification confusion), F39 (Ashby-deficient probabilistic guard).
- Subagent B proposed F36 (instruction-following ceiling), F37 (silent contradictory-prompt collapse).
- Collision: F36 and F37 each named two different phenomena. Caught at integration; documented in PLAN.md §3.6 as a triage item for the next session.

**Dispatch plan (as it should have run, with this skill):**

1. High-water mark = F35 (from `research/24-el-kaim-book-product-line-variability.md`).
2. Allocate:
   - Subagent A: F36–F39 (RE/SE proposals; expected count ≤4).
   - Subagent B: F40–F43 (academic-paper proposals; expected count ≤4).
3. Embed in each brief.
4. Result: no collision. F36–F41 occupied; F42–F43 released back to the pool.

The diff is one block per brief and a 30-second pre-flight check. The savings is the avoided §3.6 in PLAN.md.

### Example 2 — Hypothetical parallel ADR-authoring dispatch

**Scenario:** lead agent dispatches three subagents to draft three ADRs from a retrospective's "Proposed ADRs" list.

**With this skill:**

1. ADR high-water mark = 0001 (`docs/adr/0001-fetch-blocked-urls-mechanism.md`).
2. Allocate:
   - Subagent A: ADR-0002 (MHTML drain image-pass discipline).
   - Subagent B: ADR-0003 (parallel subagent registry pre-allocation).
   - Subagent C: ADR-0004 (PR draft-status default policy).
3. Each brief includes its assigned ADR number; the subagent names its file accordingly (`docs/adr/0002-mhtml-drain-image-pass.md`).

**Without this skill:** all three subagents independently look at `ls docs/adr/`, see `0001-*`, and propose `0002-*` for their own ADR. Three commits, all naming `docs/adr/0002-*.md`. Two have to be renamed at integration; cross-references between ADRs are wrong.

## Anti-patterns

- **Don't trust the subagent's "don't invent registry entries" instruction alone.** Subagents are good at following positive instructions ("use F36–F39"), less good at following negative-with-exception instructions ("don't propose F36+ unless flagged as proposal"). The exception clause invites them to propose anyway. Pre-allocation removes the ambiguity.
- **Don't allocate without naming the range explicitly in the brief.** A brief that says "use available F-numbers" is no better than no allocation at all; the subagent will look at HEAD and pick the next number, which is what the other subagent is also doing.
- **Don't over-allocate.** A subagent told "F36–F50" will sometimes feel obligated to fill the range. Allocate tight; the lead agent renumbers at integration if needed.
- **Don't skip pre-allocation when subagents will write *files* with sequential numbers (reports 25, 26).** This was actually handled correctly in the Round-9 session — both subagents were told their report number up front. The failure was in the *catalog-entry* registry (F-modes), not the *file-name* registry. Treat both registries.

## Acceptance criteria

1. Every subagent dispatched in parallel that touches a shared registry has a "Registry allocation (your exclusive range)" block in its brief.
2. Allocated ranges across all simultaneously-dispatched subagents are non-overlapping.
3. At integration time, every catalog entry produced by the subagents has an ID within its allocated range.
4. If a subagent flags more candidates than its range allows, the lead agent allocates the overflow at integration time (not the subagent retroactively claiming an ID outside its range).
5. The orchestrator's dispatch-time message names every registry being allocated, even if the allocation is trivial (e.g., "no F-modes expected from this dispatch — registry not touched").

## Files this skill creates / modifies

- Modifies: each subagent's brief (the lead agent's prompt to the subagent before dispatch).
- Optionally creates: `/tmp/dispatch-allocation-<YYYY-MM-DD>.md` — scratch note for the orchestrator's own reference. Not committed.
- Indirectly modifies: the registry-bearing files (e.g., `research/00-synthesis.md` §4, `docs/adr/`, `research/INDEX.md`) at integration time, but only insofar as it prevents the lead agent from having to do post-hoc collision reconciliation.
