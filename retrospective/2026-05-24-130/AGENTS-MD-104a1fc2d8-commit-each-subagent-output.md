# agent instruction

**Commit each subagent's output immediately upon return.** When fanning out parallel subagents whose outputs are independent files, commit + push each artifact as soon as its completion notification arrives — do not batch. Batching across multiple notifications leaves uncommitted work in the ephemeral sandbox between turns and trips the repo's stop-hook on every reply, and a network blip or session crash mid-batch loses every still-uncommitted artifact.

*Grounded in: stop-hook fired repeatedly during Phase-2 track + bias-guard fan-out because track outputs were not committed in real time.*

# justification

In this session 9 track subagents + 4 bias-guard subagents fanned out in parallel. As each one reported back, its output file landed on disk but I committed it only intermittently — sometimes after several notifications, sometimes only when the stop-hook nagged me. The stop-hook ran on every assistant turn that ended with untracked files, repeatedly producing `stop-hook-git-check.sh] There are untracked files in the repository`. The marginal cost of committing on every notification is one extra `git add && commit && push` per artifact (≤2 tool calls); the avoided cost is (a) no stop-hook noise on any reply, and (b) zero work lost if the sandbox dies between notification N and notification N+1. In a 13-subagent fan-out, the asymmetry compounds: batching means one disconnect can erase up to 12 already-completed artifacts, all of which are expensive Opus runs.
