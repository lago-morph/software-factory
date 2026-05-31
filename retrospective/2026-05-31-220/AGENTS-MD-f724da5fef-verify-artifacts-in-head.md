# agent instruction

**Verify critical artifacts in HEAD independently of a subagent's git self-report.** When a subagent reports it cannot see its own output via `git status` (or any sandbox/index quirk), do not trust that self-report either way -- the orchestrator independently verifies the artifact is on disk and in the committed tree (`git ls-tree -r HEAD --name-only | grep <path>`) before declaring it saved.

*Grounded in: the v4 run, where the C57 capstone builder reported an empty `git status` but the files were present and already committed by a prior checkpoint.*

# justification

Subagents in this environment are briefed never to run git, so their view of repository state is partial and occasionally wrong — the C57 capstone builder reported `git status --porcelain` returning empty "even though the files exist," and concluded it was a sandbox quirk. Had the orchestrator taken that self-report at face value it might have either panicked (re-dispatching a completed capstone) or, worse, assumed-saved something that wasn't. The orchestrator owns git and is the only actor that can authoritatively answer "is this in the committed tree?" A single `git ls-tree -r HEAD | grep` resolved it in one call (files present, already captured by a prior checkpoint commit). The rule costs one command on the critical artifacts; it prevents both false-loss panic and false-save complacency at exactly the moment — the capstone — where either is most expensive.
