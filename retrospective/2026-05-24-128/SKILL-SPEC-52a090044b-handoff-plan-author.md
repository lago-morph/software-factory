# Spec: `handoff-plan-author`

- **ID**: SKILL-SPEC-52a090044b
- **Source retrospective**: ../2026-05-24-128.md

## Intent

Write a session-to-session handoff plan that a fresh-context next agent can execute without re-deriving context, with built-in review checks: don't front-load references to forbidden-fruit artifacts in startup-reading sections, don't include already-done tasks in the handoff, limit stop-and-ask checkpoints to major decision points, and maintain an explicit chain-to-next-phase pointer so the master plan doesn't get lost when the transient handoff is cleaned up. This skill exists because in the v3 work, the PHASE-2-RERUN-PLAN.md handoff document required five rounds of PR-comment-driven fixes before all four of these checks passed. Each round trimmed verbosity, moved references, removed forbidden-fruit pointers, or fixed bugs caused by writing the plan without an explicit review pass. The skill captures the checks as a standing discipline so the next handoff doesn't rediscover them one at a time.

## Trigger

**Direct user phrases:**
- "Write a handoff plan for the next session"
- "My context is full; can you write a takeover doc?"
- "Create a plan a fresh session can pick up"
- "Get this into a state I can start another session to pick up"

**Proactive triggers:**
- The user mentions their context window is getting full and there's substantive uncommitted work or in-flight planning.
- The session has reached a natural phase boundary (PR merged, major task complete) and there's clearly next-phase work to do.
- The user asks for a "checklist" or "next steps" doc with the expectation that another agent will execute it.

**Negative triggers:**
- The user wants a roadmap or architecture document. Those are durable; this skill is for transient handoff docs.
- The user wants documentation for human readers. This skill targets fresh-context agents specifically.

## Inputs

- The current state of the work (commits, in-flight artifacts, open questions).
- The user's intent for what the next session should do.
- The master plan or roadmap the handoff plan is a sub-doc of (if any).
- Any contamination or context-risk artifacts that need to be fenced off from the next agent.

## Outputs

- A handoff plan file (typically at the work-area root, e.g., `architectures/v3/PHASE-2-RERUN-PLAN.md`).
- One commit adding the plan, with a clear commit message naming the handoff's scope and the next session's expected entry point.
- Optionally: an updated banner in adjacent docs (e.g., `research/PLAN.md`) pointing the next agent at the handoff.

## Workflow

1. Draft the plan with these sections in this order:
   - **Purpose** — one or two sentences explaining what the next session is meant to do. Pair with a pointer to the master plan (durable upstream document).
   - **§0 Operating rule** — short, direct. "Follow this plan. Don't do side work. Stop and ask at major decision points." Cross-reference the global rule in AGENTS.md.
   - **§1 Standing intent** — the goal and any necessary background. If the prior session left state the next session needs to understand, summarize it in one or two sentences. Do NOT enumerate forbidden-fruit artifacts here.
   - **§2 Pre-flight: where everything is** — file-state table. Each row shows path + status + brief note. Do NOT name forbidden-fruit artifacts.
   - **§3 The N substantive steps** — each step has What / Why / Expected outcome. Stop-and-ask line only on major-decision steps.
   - **§4 Appendix (optional)** — single-line pointer to permalink-with-guard reference doc if applicable.
2. Apply the **four-check review** before committing:
   - **Forbidden-fruit check.** Search the plan's §0/§1/§2 (startup-reading sections) for names of contaminated files, deprecated approaches, or any artifact the next agent should not read. Move references into the specific step that uses them, or relocate the artifact via the permalink-with-guard pattern.
   - **Done-task check.** Search the plan's §3 for any step marked DONE. Remove the DONE step entirely (keep its substance as a one-sentence note in §1 if context is needed).
   - **Stop-and-ask check.** Count the stop-and-ask checkpoints in §3. They should appear only at major decision points (e.g., before dispatching N parallel subagents, before opening a PR, before running an irreversible operation). Mechanical or low-risk steps don't get checkpoints.
   - **Chain-to-next-phase check.** Does the plan have an explicit pointer to where the next session goes after this plan completes? If no, add one — usually in the cleanup step.
3. Commit the plan. The commit message names the plan, the handoff's scope, and the expected entry point.
4. Update any upstream banners (e.g., a `research/PLAN.md` banner) to point at the master plan (durable), with the master plan in turn pointing at this handoff plan (transient). Don't point upstream banners directly at the handoff plan — that strands the chain when the handoff is cleaned up.

## Concrete examples

### Example 1: Phase-2 re-run handoff

Context: contamination found in a Phase-2 dispatch; the next session needs to clean source files, dispatch fresh subagents, and open a PR.

Final structure after applying the four-check review:

```
# Phase-2 clean re-run plan (for next session)

**Purpose.** Takeover plan for the next session to execute Phase 2 of
the v3 architecture synthesis. Pairs with ARCHITECTURE-V3-SYNTHESIS-PLAN
(master plan with current-state pointer).

## 0. Operating rule

Follow this plan step by step. Don't do side work outside it.
Stop and ask before each step in §3 that has an explicit stop-and-ask
line. See AGENTS.md "Interactive operation."

## 1. Standing intent

[One paragraph: what to do, with a one-line pointer to history doc
for fenced-off artifacts.]
[One paragraph: state the prior cleanup that has already happened.]

## 2. Pre-flight: where everything is

| Path | Status | Notes |
[Clean file-state table; no forbidden-fruit names.]

## 3. The 4 substantive steps

### Step 3.1 — Re-dispatch 9 tracks (with stop-and-ask)
### Step 3.2 — Re-run bias guards (with stop-and-ask)
### Step 3.3 — Open PR (with stop-and-ask)
### Step 3.4 — Cleanup + update master plan's current-state pointer

## 4. Appendix

Historical artifacts: history/HISTORICAL-RECORD.md (do not read).
```

What the four-check review caught before commit:
- Forbidden-fruit: §2 had a list of "Important contamination references" naming the contaminated files; removed.
- Done-task: steps 3.1-3.5 were marked DONE (cleanup happened earlier this session); removed; renumbered 3.6-3.9 to 3.1-3.4; added one §1 sentence noting prior cleanup.
- Stop-and-ask: original plan had checkpoints on every step (3.1-3.9); pruned to 3.6/3.7/3.8 (now 3.1/3.2/3.3) only.
- Chain-to-next-phase: original step 3.9 just removed the upstream banner; updated to also update the master plan's current-state pointer from "in Phase 2" to "in Phase 3."

### Example 2: Small handoff for a multi-day code refactor

Context: a session refactored half of a large module and ran out of context; next session needs to finish the refactor and run tests.

Final structure:

```
# Refactor takeover plan

**Purpose.** Finish the FooModule refactor. Pairs with the issue
#NNNN tracking the work.

## 0. Operating rule

Follow this plan. Don't refactor anything outside FooModule.
Stop and ask before running the test suite (large blast radius).

## 1. State

FooModule.foo() and FooModule.bar() have been refactored; tests pass.
FooModule.baz() and the integration test still pending.

## 2. The 2 substantive steps

### Step 2.1 — Refactor FooModule.baz()
### Step 2.2 — Run integration tests (stop-and-ask before)
```

What the four-check review caught:
- Forbidden-fruit: none (no contaminated artifacts).
- Done-task: the original draft listed "refactored foo() and bar()" as steps 1 and 2; removed; folded into §1 state.
- Stop-and-ask: original had checkpoints on every step; reduced to one before running integration tests.
- Chain-to-next-phase: added "when both steps complete, close issue #NNNN and the work is done" — even small handoffs need an explicit "what does done look like."

## Anti-patterns

- **Including done tasks as a courtesy.** The next agent does not need a history lesson; they need a task list. Done tasks in the handoff get scrolled past in the best case and rediscovered in the worst case.
- **Stop-and-ask at every step "for safety."** The user gets annoyed and reads less of the plan. The discipline is to stop at *major* decision points; mechanical steps execute under the §0 rule alone.
- **Listing forbidden-fruit artifacts to "warn" the next agent.** The warning itself is the temptation. Use the permalink-with-guard pattern instead.
- **Pointing the upstream banner at the transient handoff plan.** When the handoff plan is cleaned up at the end of the work, the banner becomes a dangling pointer. Point upstream banners at the master plan; the master plan points at the current handoff.
- **Writing the plan in a single pass without the four-check review.** The Phase-2 plan went through five rounds of PR-comment fixes because each round caught one issue the prior round had introduced. The four-check review catches them all in a single pass.

## Acceptance criteria

- [ ] Plan starts with Purpose + Operating rule + Standing intent in that order.
- [ ] §0/§1/§2 contain no names of forbidden-fruit artifacts.
- [ ] §3 contains no DONE steps.
- [ ] §3 has stop-and-ask checkpoints only at major decision points.
- [ ] Plan has an explicit pointer to where the next session continues after this plan ends.

## Files this skill creates / modifies

- The handoff plan file (path depends on the work area; typically `<work-area>/PHASE-N-PLAN.md` or `<work-area>/HANDOFF.md`) — creates.
- Optionally: an upstream banner in an adjacent doc (e.g., `research/PLAN.md`) — modifies. The banner points at the master plan, not the transient handoff.
- The master plan (e.g., `ARCHITECTURE-V3-SYNTHESIS-PLAN.md`) — modifies. Adds or updates a current-state pointer.
