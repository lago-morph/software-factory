# `parallel-subagent-fanout` skill

A skill that turns a single request into a fully-orchestrated parallel
multi-agent workflow: **plan → branch → dispatch → wait → merge → PR + report**.

## Why

Users reach for this pattern constantly but it involves a lot of typing each
time: naming branches correctly, writing identical boilerplate across multiple
subagent briefs, invoking the merge helpers (which exist but are fiddly), and
assembling the run report. This skill automates all of that.

## The 10 mechanical steps it replaces

1. Create the feature branch
2. Decompose the goal into subtasks
3. Name sub-branches (`feature--sub-N` — double-dash, not slash)
4. Write each subagent brief
5. Dispatch all subagents in a single message (parallel)
6. Wait for completions; flag failures
7. Merge sub-branches into the feature branch in plan order
8. Resolve conflicts per configured strategy
9. Open a PR with an embedded run report
10. Delete sub-branches

## Usage

```
Run the parallel-subagent-fanout skill.
Goal: implement endpoints A, B, and C
Spec: specs/api.md
Max parallel: 4
Conflict strategy: fail
```

## Outputs

- One PR per fanout run, with an embedded run report.
- `harness/runs/<run_id>/state.json` for recovery.
- `harness/runs/<run_id>/report.md` persisted to the repo.

## Status

Spec only — see `SPEC.md`.

## See also

- `subagent-prompting` — brief templates used when writing each subagent's brief.
- `agent-dispatch-loop` — the iterative variant of this pattern.
