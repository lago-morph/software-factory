# agent instruction

**No retrospective references in plan docs.** Retrospective management is an independent process. Plan documents (research/PLAN.md, research-plan.md, equivalents) never reference retrospective backlogs ("X unbuilt skill specs from retro Y"), pending retro decisions, or follow-up tasks owned by retro-review.

*Grounded in: user feedback on cleanup-plan v1 — "I also want to completely excise any reference to following up on retrospectives. That is an independent process that must not be in any plan documents."*

# justification

PLAN.md §3.4 ("Pending retrospective decisions") tabulated five retrospectives' worth of "13 unbuilt skill specs / 45 AGENTS suggestions / 26 proposed ADRs" with a footnote that the table was stale because 17 more retros had landed since. The §5 work-remaining list had an item ("Retrospective decisions — pick scope across the cumulative backlog") that depended on this stale table. The §6.2 in-flight tracking table had a row for it. The §1 status line referenced it. Removing the entanglement turned out to be a non-trivial sweep across five sections.

The conceptual reason for the separation: retrospectives capture lessons from completed work; plans capture intended future work. Lessons-as-tasks creates a circular ownership — does the retrospective "own" the unbuilt skill spec, or does the plan? In practice both, which means neither. By keeping retro-follow-up as an independent process (the retrospective skill produces its own artifacts; the user reviews them on their own cadence), neither register has to track the other's state.
