# agent instruction

**Commit each background subagent's disjoint files at its completion; treat the stop-hook's mid-wave uncommitted-changes warning as expected.** In a parallel background-subagent orchestration where the orchestrator owns all git, commit each subagent's disjoint output as that subagent reports completion — never mid-write, and never let the stop-hook's uncommitted-changes nag (which fires on in-flight subagent writes) push you into committing a half-written wave. The orchestrator's commit cadence is per-completed-subagent, not per-hook-fire.

*Grounded in: the Wave-2 stop-hook nags while five background subagents were still writing C52/C53/C30/C08/C34.*

# justification

During Wave 2 the orchestrator dispatched five background subagents (C52/C53/C30/C08/C34) writing disjoint file pairs, and the stop-hook fired "There are uncommitted changes" on essentially every turn-boundary while those subagents were still writing. The hook's signal is real but its timing is misleading in a fan-out: at any mid-wave instant the working tree holds the partial output of several in-flight agents, and committing *then* would capture half-written files and race the agents' own writes. The discipline that worked was to commit each subagent's two files the moment its completion receipt arrived (disjoint paths, so no index race), and to read the stop-hook nag as "a wave is in flight," not "commit now." This preserves the commit-and-push-every-wave-boundary rule and the orchestrator-owns-all-git rule simultaneously. The cost of the wrong reaction is a commit that captures a corrupt half-file (and a confusing diff); the cost of the right one is simply tolerating an expected warning until the relevant subagent reports done.
