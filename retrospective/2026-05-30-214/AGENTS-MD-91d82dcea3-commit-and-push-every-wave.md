# agent instruction

**Commit and push at every wave boundary.** "In the ephemeral web sandbox, commit and push after each subagent wave completes - never mid-wave. Subagents never run git; the orchestrator owns all commits to avoid working-tree races."

*Grounded in: 100+ docs produced across many waves with zero lost work despite a mid-run remote reset.*

# justification

The sandbox is ephemeral and was observed to reset mid-session (the git remote URL changed between pushes, and a merged PR's branch was deleted out from under the working tree). Because the orchestrator committed and pushed after every wave — and never let subagents touch git — not a single one of the 100+ generated documents was lost, and there were no working-tree races from concurrent writers. The marginal cost is one commit+push per wave (a few seconds, with backoff retry). The cost of skipping it is catastrophic and unrecoverable: an entire wave of expensive subagent output vanishes when the container is reclaimed. Centralizing git in the orchestrator also means the dozens of parallel subagents only ever write their own distinct files, so there is never a staging conflict.
