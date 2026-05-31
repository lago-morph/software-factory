# agent instruction

**Restart interrupted async subagents after a session or sandbox rotation.** When an async subagent was dispatched but its completion never arrived and the session/sandbox has since rotated (e.g. the task-namespace path UUID changed), treat that subagent as dead: verify its deliverable is absent on disk, then re-dispatch it. Do not assume a pre-rotation background job survives the rotation.

*Grounded in: the v4 run, where a C52 adversary launched before an interrupt never landed and was re-dispatched after the task-namespace UUID changed.*

# justification

Background subagents are tied to the session/container that launched them. When a run is paused/resumed and the harness rotates the sandbox (observable as the per-task output-file path UUID changing from one value to another), any subagent dispatched under the old namespace is orphaned — its completion notification will never arrive, but nothing announces this. This run had a C52 adversary launched moments before a user interrupt; on resume the task-namespace UUID had changed, C52's review file was absent on disk, and treating it as "still running" would have stalled the wave forever. The check is cheap and unambiguous: a `ls` of the expected deliverable plus awareness of the namespace change. The failure it prevents is a silent indefinite hang on a dead job.
