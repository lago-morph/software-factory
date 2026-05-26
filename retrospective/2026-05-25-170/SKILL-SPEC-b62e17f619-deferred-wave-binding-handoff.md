# Spec: `deferred-wave-binding-handoff`

- **ID**: SKILL-SPEC-b62e17f619
- **Source retrospective**: ../2026-05-25-170.md

## Intent

When an autonomous run defers in-scope work to a successor run, encode the deferral as a binding constraint in three mutually-agreeing artifacts: the session handoff doc, the morning summary's "what I deliberately did NOT do" section, and the next-run dispatch prompt. Divergence among the three is a process bug. In the 2026-05-25 Phase-5-entry run, the auto-005 Round-1 cost-hawk correctly argued for splitting Phase 5 across two runs. But the deferral mechanism was underspecified until Round 2, when all three fresh-angle reviewers (pre-mortemer, naive newcomer, regulator/governance) independently raised the "binding artifact" concern. The Round-2 amendment promoted the Phase-5a-close handoff to a binding artifact carrying the Phase-6 gate. This skill codifies the pattern so future deferrals do not need to be re-discovered through adversarial review.

## Trigger

Activate when an autonomous run reaches a decision-brief stage and the reviewer set (or the lead agent's own scope analysis) concludes that in-scope work must be deferred to a successor run. Direct triggers: "defer this wave / phase / sub-track", "we'll do that in the next run", "PR-cap pressure forces a split". Proactive trigger: any decision-brief Round-2 finding that includes "binding artifact" or "successor run" language. Negative trigger: deferral of out-of-scope work (which needs no binding artifact — it stays out of scope by definition).

## Inputs

- The decision brief that finalized the deferral.
- The list of artifacts produced this run that the deferred work will reference (typically an ADR-ID-to-file mapping, but could be sub-track outputs, primitive sketches, etc.).
- The shape of the next run's dispatch prompt (if known) or a commitment to author one at run-close.

## Outputs

Three mutually-agreeing binding artifacts:

1. **Session handoff doc** (`architectures/<dir>/SESSION-HANDOFF-<date>-<phase>-close.md`) with a "deferred work" section carrying:
   - The deferred-work scope enumeration (full count + per-item list).
   - Reference to the parent decision brief.
   - The ADR-ID-to-file mapping table (or analog) for cross-references from deferred work to this-run outputs.
   - Any downstream phase gate ("Phase 6 MAY NOT START until …").
2. **Morning summary** "what I deliberately did NOT do" section naming the deferred work with the same scope language.
3. **Next-run dispatch prompt** (`next-agent-prompt-<phase>.md` or analog) describing the deferred work as Phase 1 or first-task scope. If the dispatch prompt is not authored this run, flag the omission in the morning summary's follow-up section.

## Workflow

1. After the decision brief locks the deferral, draft the deferral language as a single 3-5 sentence block: (a) what is deferred, (b) why (cite the cost/scope/PR-cap argument), (c) when ("next run", "Phase X dispatch", or named successor run), (d) the binding mechanism (handoff + summary + next-prompt).
2. Author the session handoff doc as a separate PR (`B<N>-handoff`). Stack on the last work-PR of the run.
3. Add the "deferred work" section to the handoff with the canonical structure:
   - § Scope enumeration (full list of deferred items with IDs).
   - § Cross-reference inputs (the ADR-ID-to-file mapping or analog).
   - § Downstream gate (the explicit "MAY NOT START until …" sentence).
   - § Pickup brief for next agent (read order, first task, expected adversarial review depth).
4. Mark the prior handoff `[SUPERSEDED]` with banner.
5. Update `AGENT-ENTRY.md` § Current state link target per the autonomous-run handoff discipline.
6. Author the morning summary as the next PR. The "what I deliberately did NOT do" section must contain the same deferred-work language, cross-linked to the handoff doc.
7. If the next-run dispatch prompt exists, edit it to inherit the deferred work. If it doesn't yet exist, flag in the morning summary's follow-up section: "Next-run dispatch prompt at `next-agent-prompt-<phase>.md` not yet authored; deferred-work pickup is owed before next run."
8. Run a final consistency check: grep all three artifacts for the deferred-work item names; if any item appears in one but not all three, fix before run-close.

## Concrete examples

### Example 1: Wave 5.3 deferral in 2026-05-25 run

- **Handoff doc** ([`architectures/v3/SESSION-HANDOFF-2026-05-25-phase-5a-close.md`](../../architectures/v3/SESSION-HANDOFF-2026-05-25-phase-5a-close.md)) carries: 29-ADR scope (13 per-variant + 16 orphan); ADR-ID-to-file mapping table for the 27 ADRs this run produced; Phase-6 gate: "Phase 6 MAY NOT START until Wave 5.3 Accepted OR adversarially-reviewed waiver brief authored."
- **Morning summary** ([`overnight-summary-2026-05-25.md`](../../overnight-summary-2026-05-25.md) § "What I deliberately did NOT do") names Wave 5.3 explicitly with reference back to the handoff and to auto-005 Round 2.
- **Next-run dispatch prompt** NOT YET AUTHORED — flagged in the morning summary's follow-up section as a deferred-deferred item. The user can author it now or at next-session start.

### Example 2: Hypothetical Phase-3.6 deferral

A future run dispatches Phase 3.5 sketches + a Phase 3.6 cross-cluster comparison, but Phase 3.6 turns out larger than expected. The lead agent surfaces the deferral in the Round-1 decision brief: "Phase 3.6 deferred to next run." Three artifacts:
- Handoff: 14 cross-cluster comparison items enumerated.
- Morning summary: deferral noted.
- Next-run dispatch prompt: written this run as `next-agent-prompt-phase-3.6.md`, points back at this run's handoff.

## Anti-patterns

- **Encoding the deferral in only one artifact**. If only the handoff has the deferral, the morning user (who reads the summary first) won't see it. If only the summary, the next agent (who reads the handoff first) won't see it. All three are needed.
- **Informal deferral in narrative prose**. "We'll get to that later" without scope enumeration is just a wish. The binding-artifact pattern requires a named scope, a named target, a named gate.
- **Skipping the cross-reference table**. If the deferred work needs to cross-reference this-run outputs (ADR IDs, sub-track outputs, primitive sketches), the next run will either re-discover the references (cost) or speculatively cross-reference (drift). Author the table at handoff time.
- **Deferring without a gate.** "We'll do it eventually" is not a binding constraint. The handoff must name the downstream phase or work-item that is blocked, with the explicit "MAY NOT START" language.

## Acceptance criteria

- [ ] Three artifacts agree on the deferred-work scope (grep-verifiable).
- [ ] The handoff carries the cross-reference table (ADR-ID-to-file mapping or analog).
- [ ] The downstream gate is stated as an explicit prohibition with a defined release condition.
- [ ] Prior handoff is marked `[SUPERSEDED]` and `AGENT-ENTRY.md` pointer is updated.

## Files this skill creates / modifies

- `architectures/<dir>/SESSION-HANDOFF-<date>-<phase>-close.md` — new file.
- The prior SESSION-HANDOFF — adds `[SUPERSEDED]` banner.
- `AGENT-ENTRY.md` — updates § Current state link target.
- The morning summary — adds deferral language to "what I deliberately did NOT do".
- Optionally `next-agent-prompt-<phase>.md` — new dispatch prompt for the successor run.
