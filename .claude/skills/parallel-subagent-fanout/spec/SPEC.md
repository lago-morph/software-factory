# `parallel-subagent-fanout` — Implementation Specification

A skill for orchestrating parallel multi-agent workflows where independent
tasks can be executed concurrently and merged into one cohesive deliverable.

## 1. Trigger conditions

Activate when the request decomposes into N ≥ 2 independent subtasks:

- "Implement endpoints A, B, and C"
- "Add tests for modules X, Y, Z in parallel"
- "Do N independent things and produce one output"
- "Fan out this work across multiple agents"

Negative triggers:
- Tasks with ordering dependencies (use `agent-dispatch-loop` or serial
  dispatch instead).
- Single-subagent tasks (overhead > benefit).
- Tasks where subtasks share the same files (conflict risk too high).

## 2. Inputs

- **Goal** (string, required)
- **Spec file path** (optional)
- **Subtask list** (optional) — if provided, skip the planning phase
- **Max parallel** (default: 4) — cap on simultaneous subagents
- **Conflict strategy** (default: `fail`) — also: `ours`, `theirs`, `manual`
- **Feature branch** (optional) — auto-generated as `feat/<run_id>` if absent
- **Sub-branch prefix** (auto) — `<feature_branch>--sub-`

## 3. The pipeline

### Phase 1 — plan

The dispatcher (you) decomposes the goal into a YAML plan:

```yaml
run_id: <run_id>
goal: <GOAL>
feature_branch: <feature_branch>
subtasks:
  - id: sub-01
    title: <short name>
    description: <what this subtask does>
    files_touched: [<estimated files>]
    branch: <feature_branch>--sub-01
  - id: sub-02
    ...
```

**Show the plan to the user and wait for approval before branching.**
Catching a wrong decomposition at this stage saves substantial rework.

### Phase 2 — branch

```bash
git checkout -b <feature_branch>
git push -u origin <feature_branch>
# For each subtask:
git checkout -b <feature_branch>--sub-<id> <feature_branch>
git push -u origin <feature_branch>--sub-<id>
git checkout <feature_branch>
```

Critical: use `--sub-` (double-dash) not `/sub-` (slash). Git cannot create
a branch `foo/bar` if `foo` already exists as a branch name — the double-dash
avoids this collision.

### Phase 3 — dispatch

Build a brief for each subtask following the `subagent-prompting` skill
template (sections: identity + goal, context, repo + branch, what to build,
don't do, validation step, deliverable shape, traps). Key fields per brief:

- Branch: `<feature_branch>--sub-<id>` (work only here)
- Don't: merge, switch branches, or touch other subtask's files
- Deliverable: commit + push to sub-branch; report PR# and test delta

Dispatch all subagents in a **single dispatcher message** with multiple Agent
tool calls. The harness parallelizes them; you get all results before
continuing.

Cap at `max_parallel` subagents per wave. If N > max_parallel, dispatch in
waves: wait for wave 1 to complete before dispatching wave 2.

### Phase 4 — wait + collect

For each subagent result:
- Extract: sub-branch name, PR number (if opened), test count delta, any
  blocking issues.
- Flag failures (subagent did not complete, tests regressed) for manual
  review before merging.
- Record results in `harness/runs/<run_id>/state.json`.

### Phase 5 — merge

Merge sub-branches into the feature branch in **plan order** (not
completion order). Deterministic order ensures the run report and actual
merge outcomes stay aligned.

```bash
git checkout <feature_branch>
git merge --no-ff <feature_branch>--sub-01
# On conflict:
#   strategy=fail  → stop, report conflict, wait for user
#   strategy=ours  → git merge -X ours ...
#   strategy=theirs → git merge -X theirs ...
#   strategy=manual → open conflict markers for user
git push origin <feature_branch>
```

After each successful merge: delete the sub-branch.

```bash
git push origin --delete <feature_branch>--sub-<id>
```

### Phase 6 — PR + report

Write the run report to `harness/runs/<run_id>/report.md`:

```markdown
# Fanout run report — <run_id>

| Subtask | Branch | Status | Tests delta | PR |
|---------|--------|--------|-------------|-----|
| sub-01  | ...--sub-01 | merged | +N | #M |
| sub-02  | ...--sub-02 | merged | +N | #M |

## Merge log
[One line per merge: branch, conflicts, resolution]

## Deviations
[Any subtask that deviated from its brief]

## Final state
[Feature branch HEAD, total tests, coverage if available]
```

Commit the report:
```bash
git add harness/runs/<run_id>/
git commit -m "fanout <run_id>: run report"
git push origin <feature_branch>
```

Open a PR from `<feature_branch>` → main. Embed the run report table in the
PR body.

## 4. State schema

`harness/runs/<run_id>/state.json`:

```json
{
  "run_id": "...",
  "goal": "...",
  "feature_branch": "...",
  "conflict_strategy": "fail",
  "max_parallel": 4,
  "subtasks": [
    {
      "id": "sub-01",
      "title": "...",
      "branch": "...",
      "status": "merged",
      "pr_number": 5,
      "tests_delta": 12,
      "issues": []
    }
  ]
}
```

## 5. Critical rules

- **Always double-dash in sub-branch names.** `feature--sub-N`, not
  `feature/sub-N`. Git cannot have a branch `foo` and a branch `foo/bar`
  simultaneously.
- **Merge in plan order.** Completion order can differ; always use plan order.
- **Approve the decomposition before branching.** Show the YAML plan and wait.
- **Never force-merge on conflict without user approval.** The conflict might
  represent a genuine design issue.
- **Run reports must be committed**, not just posted to PRs — PR descriptions
  disappear from search after close.

## 6. Anti-patterns

- Using `/sub-` as separator → git reference collision.
- Merging in arrival order → non-deterministic report alignment.
- Skipping user review of the plan → wrong decomposition discovered after
  branching.
- Force-merging conflicts silently → masks integration bugs.
- Sub-branches touching the same files → near-certain conflicts.

## 7. Integration

- Briefs for each subagent are written following `subagent-prompting` patterns.
- The `agent-dispatch-loop` uses this skill for steps 1 and 3 when an
  iteration's work decomposes into parallel pieces.
- Branch cleanup follows `forensic-vs-aggressive-cleanup` conventions.

## 8. Test plan (when built)

- Unit: plan decomposition from a sample goal (snapshot test).
- Unit: sub-branch naming — verify double-dash is always used.
- Unit: merge-order logic — verify plan order is maintained.
- Integration: dry-run mode — prints all branches and briefs without
  creating them.
- Live: 2-subtask fanout on a trivial goal; verify both PRs land and
  the run report is committed.

## 9. Future variants

- Sequential chains (subtask N depends on N-1's output).
- Heterogeneous subagent types per subtask.
- Adaptive wave sizing based on subtask estimated duration.

Non-goals for v1.
