---
name: parallel-subagent-fanout
description: Orchestrate a parallel multi-agent workflow that decomposes a goal into independent subtasks, dispatches them concurrently to subagents on separate sub-branches, merges results in plan order, and delivers one PR with an embedded run report. Use this skill whenever the user asks to fan out work across multiple agents, implement N independent endpoints/modules/features in parallel, run multiple subagents at once, or do several independent things and produce one combined output, even if they don't explicitly say "fanout".
---

# Skill: parallel-subagent-fanout

Orchestrate a parallel multi-agent workflow: decompose a goal into independent
subtasks, dispatch them concurrently, collect results, merge in plan order, and
deliver one PR with an embedded run report.

The dispatcher (you) owns planning, branching, state, and merging.
Subagents own the work inside their sub-branches.

---

## Trigger phrases

Use this skill when the user says any of:

- "Implement endpoints A, B, and C"
- "Add tests for modules X, Y, and Z in parallel"
- "Do these N independent things and produce one output"
- "Fan out this work across multiple agents"
- "Run the parallel-subagent-fanout skill"

Do **not** use for tasks with ordering dependencies (use `agent-dispatch-loop`),
single-subagent tasks (overhead exceeds benefit), or subtasks that touch the
same files (near-certain merge conflicts).

---

## Step 0 — collect inputs

Resolve these values before doing anything. Ask the user for any required value
that is missing.

| Input | Default | Notes |
|-------|---------|-------|
| `GOAL` | (required) | What to build or do |
| `SPEC_PATH` | none | Path to a spec file subagents should follow |
| `SUBTASK_LIST` | none | Pre-defined subtask list; if provided, skip planning |
| `MAX_PARALLEL` | `4` | Cap on simultaneous subagents per dispatch wave |
| `CONFLICT_STRATEGY` | `fail` | `fail`, `ours`, `theirs`, or `manual` |
| `FEATURE_BRANCH` | `feat/<run_id>` | Branch for all merged work |
| `REPO_ROOT` | current working directory | Absolute path |

Generate `run_id` as `YYYYMMDD-HHMMSS` from the current timestamp.

If `FEATURE_BRANCH` is not provided, set it to `feat/<run_id>`.

---

## Step 1 — plan and get user approval

**If `SUBTASK_LIST` was provided**, skip decomposition and jump to Step 2 using
those subtasks.

**Otherwise**, decompose `GOAL` into N ≥ 2 independent subtasks. Produce a YAML
plan in this exact shape:

```yaml
run_id: <run_id>
goal: <GOAL>
feature_branch: <FEATURE_BRANCH>
subtasks:
  - id: sub-01
    title: <short name, ≤8 words>
    description: <one sentence: what this subtask builds or does>
    files_touched: [<estimated file paths>]
    branch: <FEATURE_BRANCH>--sub-01
  - id: sub-02
    title: ...
    description: ...
    files_touched: [...]
    branch: <FEATURE_BRANCH>--sub-02
```

Rules for good decomposition:
- Each subtask must be **independent**: it must not depend on another subtask's
  output, and must not write to the same files as another subtask.
- Use zero-padded two-digit IDs: `sub-01`, `sub-02`, ..., `sub-N`.
- Sub-branch name is always `<FEATURE_BRANCH>--sub-<id>` — double-dash, never
  slash.

**Show the YAML plan to the user. Wait for explicit approval or revision.**
Do not proceed to Step 2 until the user confirms.

If the user requests changes, revise the plan and show it again. Repeat until
approved.

---

## Step 2 — create branches and initialise state

Once the plan is approved, create all branches.

```bash
# Create the feature branch from current HEAD (usually main)
git checkout -b <FEATURE_BRANCH>
git push -u origin <FEATURE_BRANCH>

# For each subtask, in plan order:
git checkout -b <FEATURE_BRANCH>--sub-<id> <FEATURE_BRANCH>
git push -u origin <FEATURE_BRANCH>--sub-<id>

# Return to feature branch
git checkout <FEATURE_BRANCH>
```

Critical: `--sub-` (double-dash) not `/sub-` (slash). Git cannot have both a
branch `foo` and a branch `foo/bar` simultaneously — double-dash prevents this.

Create `harness/runs/<run_id>/state.json` with:

```json
{
  "run_id": "<run_id>",
  "goal": "<GOAL>",
  "spec_path": "<SPEC_PATH or null>",
  "feature_branch": "<FEATURE_BRANCH>",
  "conflict_strategy": "<CONFLICT_STRATEGY>",
  "max_parallel": <MAX_PARALLEL>,
  "subtasks": [
    {
      "id": "sub-01",
      "title": "<title>",
      "branch": "<FEATURE_BRANCH>--sub-01",
      "status": "pending",
      "pr_number": null,
      "tests_delta": null,
      "issues": []
    }
  ]
}
```

Add one entry per subtask, all with `"status": "pending"`.

Commit the initial state:

```bash
git add harness/runs/<run_id>/state.json
git commit -m "fanout <run_id>: initialise state"
git push origin <FEATURE_BRANCH>
```

---

## Step 3 — write and dispatch subagent briefs

Build a brief for **each subtask** following the `subagent-prompting` template.
Each brief must have these sections:

```
## Identity + goal
You are implementing <subtask.title> as part of a parallel fanout run.
Run ID: <run_id>
Your subtask: <subtask.description>

## Context
<If SPEC_PATH exists: "The overall spec is at <SPEC_PATH>.">
Overall goal: <GOAL>

## Repo and branch
- Repo root: <REPO_ROOT>
- Branch: <FEATURE_BRANCH>--sub-<id>  ← commit and push here ONLY

## What to build
<3–7 bullet points derived from subtask.description and files_touched.
Be specific: name files, function signatures, API routes, etc.>

## Don't do
- Do NOT merge this branch into anything.
- Do NOT switch to another branch.
- Do NOT touch files listed in other subtasks' files_touched.
- Do NOT add features beyond this subtask's scope.

## Validation step
Before reporting back, verify:
1. `git status` on <FEATURE_BRANCH>--sub-<id> shows no uncommitted changes.
2. Tests pass (run: <TEST_COMMAND if known, else "run the project's test suite">).
3. Your work is pushed to origin/<FEATURE_BRANCH>--sub-<id>.

## Deliverable shape
Report back with:
- Sub-branch name: <FEATURE_BRANCH>--sub-<id>
- PR number (open via mcp__github__create_pull_request targeting <FEATURE_BRANCH>)
- Tests delta: +N new tests, or "no tests added"
- Any blocking issues (if none: "none")

## Traps
- Branch name uses double-dash: <FEATURE_BRANCH>--sub-<id>
- Push to origin before reporting back.
- Do not open a PR against main — target <FEATURE_BRANCH>.
```

**Dispatch all subagents in a single dispatcher message** using multiple Agent
tool calls. The harness runs them in parallel; you will receive all results
before continuing.

**Always pass `isolation: "worktree"` to every Agent call in a fanout.**
Without it, every concurrent subagent shares the dispatcher's working
directory. A subagent's `git checkout <its-sub-branch>` then races against
the other subagents' checkouts, and they stomp on each other's branches —
files get committed onto the wrong sub-branch, untracked files leak between
sibling workdirs, and cleanup at merge time becomes a manual cherry-pick
exercise. With `isolation: "worktree"` each subagent gets its own
git-worktree on its assigned branch and these collisions cannot happen.

```
Agent({
  description: "...",
  subagent_type: "general-purpose",
  isolation: "worktree",   // ← required for any fanout dispatch
  prompt: "...the brief from the template above..."
})
```

The skill's recovery patterns (Step 4 failure handling, Step 5 conflict
strategies) cover *intended* divergence between subagents. Cross-workdir
contamination is *unintended* and avoidable; don't make those patterns work
overtime to clean it up.

**Wave limit:** if N > MAX_PARALLEL, split into waves:
- Wave 1: dispatch subtasks sub-01 through sub-<MAX_PARALLEL>.
- Wait for all wave-1 results.
- Wave 2: dispatch sub-<MAX_PARALLEL+1> onward.
- Continue until all subtasks are dispatched and completed.

Do not dispatch wave 2 until wave 1 is fully complete.

---

## Step 4 — collect results

For each subagent response, extract:

| Field | How to extract |
|-------|---------------|
| Sub-branch name | From "Sub-branch name:" in the report |
| PR number | From "PR number:" |
| Tests delta | From "Tests delta:" |
| Blocking issues | From "Any blocking issues:" |
| Success | Subagent completed without errors |

For each subtask, update `harness/runs/<run_id>/state.json`:
- Set `"status"` to `"dispatched_ok"` if the subagent succeeded.
- Set `"status"` to `"failed"` if the subagent did not complete, reported
  blocking issues, or tests regressed.
- Fill in `pr_number` and `tests_delta`.
- Add any blocking issues to the `"issues"` array.

**Flag failures before merging.** If any subtask has `"status": "failed"`:
- Report the failure(s) to the user with details.
- Ask the user whether to: (a) skip that subtask, (b) re-dispatch it, or
  (c) abort the fanout.
- Do not proceed to Step 5 until failures are resolved or explicitly skipped
  by the user.

---

## Step 5 — merge in plan order

Merge sub-branches into the feature branch in **plan order** — not completion
order. Always use the sequence from the approved YAML plan.

For each subtask in plan order:

```bash
git checkout <FEATURE_BRANCH>
git merge --no-ff <FEATURE_BRANCH>--sub-<id>
```

**On merge conflict**, apply CONFLICT_STRATEGY:

| Strategy | Action |
|----------|--------|
| `fail` | Stop immediately. Report the conflicting files to the user. Wait for the user to resolve and tell you to continue. |
| `ours` | `git merge -X ours <FEATURE_BRANCH>--sub-<id>` — prefer the feature branch side. |
| `theirs` | `git merge -X theirs <FEATURE_BRANCH>--sub-<id>` — prefer the sub-branch side. |
| `manual` | Leave conflict markers in place. Tell the user which files to edit. Wait for them to resolve and run `git merge --continue`. |

Never silently force-merge a conflict — this masks integration bugs.

After a **successful** merge:
1. Push the feature branch: `git push origin <FEATURE_BRANCH>`
2. Delete the sub-branch: `git push origin --delete <FEATURE_BRANCH>--sub-<id>`
3. Update `state.json`: set `"status": "merged"` for this subtask.

If a subtask was **skipped** (user decision in Step 4), do not attempt to merge
it. Record `"status": "skipped"` in `state.json`.

---

## Step 6 — write the run report and open PR

### Write the report

Write `harness/runs/<run_id>/report.md`:

```markdown
# Fanout run report — <run_id>

Run on <DATE>. Goal: <GOAL>

## Summary

| Subtask | Branch | Status | Tests delta | PR |
|---------|--------|--------|-------------|-----|
| sub-01  | <FEATURE_BRANCH>--sub-01 | merged | +N | #M |
| sub-02  | <FEATURE_BRANCH>--sub-02 | merged | +N | #M |

## Merge log

- sub-01 (<FEATURE_BRANCH>--sub-01): merged, no conflicts.
- sub-02 (<FEATURE_BRANCH>--sub-02): merged, 1 conflict in foo.py — resolved via <strategy>.

## Deviations

[Any subtask that deviated from its brief — scope creep, wrong files,
missing deliverables. If none: "None."]

## Final state

- Feature branch: <FEATURE_BRANCH> at <HEAD commit SHA>
- Total tests (post-merge): <count or "not measured">
- Coverage: <percent or "not measured">
- Sub-branches deleted: <list>
- Sub-branches skipped: <list or "none">
```

One row per subtask in the summary table. Use actual values from `state.json`.

### Commit the report

```bash
git add harness/runs/<run_id>/
git commit -m "fanout <run_id>: run report"
git push origin <FEATURE_BRANCH>
```

### Open the PR

Open a PR from `<FEATURE_BRANCH>` → `main` via `mcp__github__create_pull_request`.
Embed the summary table from `report.md` in the PR body. Include the run_id in
the PR title: `fanout <run_id>: <GOAL> (truncated to 60 chars)`.

Tell the user the fanout is complete and print the PR URL.

---

## Anti-patterns (never do these)

- **Use `/sub-` as branch separator.** `feature/sub-01` collides with the
  `feature` branch in git — always use `feature--sub-01`.
- **Merge in arrival order.** Subagents finish at different times; arrival
  order is non-deterministic and makes the report unreproducible.
- **Skip user review of the plan.** The decomposition is the most impactful
  decision; wrong decomposition discovered post-branch is expensive.
- **Force-merge a conflict silently.** Conflicts can represent genuine design
  issues; always surface them.
- **Dispatch subagents across multiple messages.** The harness only parallelises
  Agent calls within a single message — split calls serialize the work.
- **Dispatch without `isolation: "worktree"`.** Concurrent subagents that share
  the dispatcher's workdir race on `git checkout` and contaminate each other's
  branches; the merge phase then has to clean up commits that should never
  have existed. Always isolate.
- **Skip committing the report.** PR descriptions disappear from search when
  a PR is closed; the committed `report.md` is permanent.

---

## Recovery from restart

If the dispatcher is interrupted mid-run:

1. Read `harness/runs/<run_id>/state.json` to find the last known state.
2. Check which subtasks have `"status": "pending"`, `"dispatched_ok"`, `"merged"`,
   `"failed"`, or `"skipped"`.
3. Resume from the earliest incomplete phase:
   - Any `"pending"` subtasks → re-dispatch them (Step 3).
   - All dispatched, none merged → proceed to Step 5.
   - Some merged, some not → continue merging in plan order (Step 5).
   - All merged, no report → write report (Step 6).
4. Never re-dispatch a subtask whose `pr_number` is already recorded and
   whose branch exists — just collect the existing result.
5. Never re-merge a sub-branch with `"status": "merged"` — it has already been
   deleted from origin.
