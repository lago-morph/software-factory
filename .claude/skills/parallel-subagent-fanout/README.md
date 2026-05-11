# parallel-subagent-fanout

An AI skill for orchestrating parallel multi-agent workflows. Turns a single
goal into a fully-managed fanout run: **plan → branch → dispatch → wait →
merge → PR + report**.

```
plan → branch → dispatch (parallel) → wait → merge (plan order) → PR + report
```

## When to use

Use this skill when a goal decomposes into N ≥ 2 **independent** subtasks
that can run concurrently:

- "Implement endpoints A, B, and C"
- "Add tests for modules X, Y, and Z in parallel"
- "Do these N independent things and produce one output"
- "Fan out this work across multiple agents"

**Not** for tasks with ordering dependencies (use `agent-dispatch-loop`),
single-subagent tasks (overhead exceeds benefit), or subtasks that touch the
same files (near-certain merge conflicts).

## The 10 mechanical steps it replaces

This skill automates:

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

## Inputs

| Parameter | Default | Description |
|-----------|---------|-------------|
| `GOAL` | required | What to build or do |
| `SPEC_PATH` | none | Path to a spec file for subagents to follow |
| `SUBTASK_LIST` | none | Pre-defined subtask list; skips planning phase if provided |
| `MAX_PARALLEL` | `4` | Cap on simultaneous subagents per wave |
| `CONFLICT_STRATEGY` | `fail` | Conflict resolution: `fail`, `ours`, `theirs`, `manual` |
| `FEATURE_BRANCH` | `feat/<run_id>` | Branch for all merged work |

`run_id` is auto-generated as `YYYYMMDD-HHMMSS`.

## The 6-phase pipeline

| Phase | What happens |
|-------|--------------|
| 1 — plan | Dispatcher decomposes goal into a YAML subtask list. Shows plan to user and **waits for approval** before doing anything to the repo. |
| 2 — branch | Creates feature branch, then one sub-branch per subtask as `<feature_branch>--sub-<id>`. Initialises `state.json`. |
| 3 — dispatch | Writes a `subagent-prompting`-style brief per subtask. Dispatches all as a **single message** with multiple Agent calls (parallel). Waves if N > MAX_PARALLEL. |
| 4 — wait + collect | Collects results from all subagents. Extracts sub-branch, PR number, test delta, blocking issues. Flags failures. Updates `state.json`. |
| 5 — merge | Merges sub-branches into feature branch in **plan order** using `--no-ff`. Applies CONFLICT_STRATEGY on conflict. Deletes each sub-branch after a successful merge. |
| 6 — PR + report | Writes `report.md` (table + merge log + deviations + final state). Commits it. Opens PR from feature branch → main with report embedded. |

## Critical rules

- **Double-dash in sub-branch names.** Always `feature--sub-N`, never
  `feature/sub-N`. Git cannot have both a branch `foo` and a branch `foo/bar`
  at the same time — the double-dash avoids this collision entirely.
- **Merge in plan order, not completion order.** Subagents finish at different
  times; using arrival order makes the run report non-deterministic.
- **User approves the decomposition before branching.** Catching a wrong
  decomposition at plan time is far cheaper than discovering it post-branch.
- **Never force-merge a conflict without user approval.** A conflict can
  represent a genuine design issue, not just a trivial textual overlap.
- **Commit the run report to the repo.** PR descriptions disappear from search
  after a PR is closed; a committed `report.md` is permanent.

## Anti-patterns

| Anti-pattern | Why it fails |
|--------------|-------------|
| Using `/sub-` as branch separator | Git reference collision with the feature branch |
| Merging in arrival order | Non-deterministic report alignment; harder to reproduce |
| Skipping user review of the plan | Wrong decomposition discovered after all branches exist |
| Force-merging conflicts silently | Masks integration bugs; can corrupt feature branch |
| Sub-branches that touch the same files | Near-certain merge conflicts for every merge |
| Dispatching subagents across multiple messages | Harness runs them serially instead of in parallel |

## Integration with other skills

| Skill | Used where |
|-------|-----------|
| `subagent-prompting` | Brief templates for each subtask dispatch |
| `agent-dispatch-loop` | Uses this skill for steps 1 and 3 when an iteration's work decomposes into parallel pieces |
| `forensic-vs-aggressive-cleanup` | Sub-branch deletion conventions after merge |

## Outputs

- One PR per fanout run, feature branch → main, with an embedded run report table.
- `harness/runs/<run_id>/state.json` — machine-readable subtask history (enables recovery).
- `harness/runs/<run_id>/report.md` — human-readable run report, committed to the repo.

## Files in this skill

```
skills/parallel-subagent-fanout/
├── README.md            ← this file
├── SKILL.md             ← dispatcher instructions (the executable skill)
└── spec/
    ├── README.md        ← original overview from the spec repo
    └── SPEC.md          ← full implementation spec
```
