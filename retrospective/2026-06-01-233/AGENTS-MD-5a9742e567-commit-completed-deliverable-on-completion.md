# agent instruction

**Commit each completed subagent deliverable on its completion signal.** In the ephemeral sandbox with a git-state stop-hook, do not batch-wait a whole wave of async subagents before committing — commit each deliverable the moment its agent reports complete, adding explicit paths so a sibling's in-progress edit is not captured. Use a background stabilization watcher, not a foreground wait, to bridge to a still-running agent.

*Grounded in: the git stop-hook fired repeatedly while sibling builders were mid-write; committing each completed component by explicit path resolved it without capturing partial edits.*

# justification

The "commit at every wave boundary, never mid-wave" guidance assumes a wave completes before the turn ends. With background subagents writing to the shared tree and a stop-hook that fires at every turn-end on any uncommitted change, batch-waiting the whole wave makes the hook fire repeatedly while files are mid-write — and committing then risks staging a half-written file. The resolution is to commit each deliverable the moment its own completion signal arrives, using explicit `git add <paths>` so an in-flight sibling's edits are never captured; this satisfies both the stop-hook and sandbox-loss protection without ever staging partial work. When the only outstanding work is a still-running agent, a background stabilization watcher (poll mtimes, exit when stable) bridges the gap without a blocked foreground `sleep` (which the harness blocks anyway).
