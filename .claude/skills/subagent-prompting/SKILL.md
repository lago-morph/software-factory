---
name: subagent-prompting
description: Reference card and brief generator for subagent dispatch. Use whenever you're about to call the Agent tool or write a subagent brief, especially for multiple subagents, long-running subagents (>5 minutes), or high-stakes work where rework is expensive. Provides a 9-section brief template, subagent type selection, parallel vs serial dispatch rules, foreground vs background guidance, recovery patterns, and anti-patterns.
---

# Skill: subagent-prompting

Reference card and brief generator for subagent dispatch. Use this skill
before writing any subagent brief. Two modes:

- **Inline mode**: copy the template below, fill in the placeholders, dispatch.
- **Generated mode**: pass a goal to this skill; it produces a populated brief.

---

## When to load this skill

Load it whenever you're about to call the `Agent` tool. Every dispatch
benefits. Mandatory for:
- Multiple subagents in flight or planned
- Long-running subagent (>5 minutes expected)
- High-stakes work where rework is expensive

---

## The brief template (the spine)

Copy this template. Fill every `<PLACEHOLDER>`. Remove optional sections if
genuinely not needed — but err on the side of including them.

```
You are <ROLE> for <TASK>. <GOAL_SENTENCE>. <WHY_NOT_DOING_IT_OURSELVES>.

## Context
<3-6 sentences: what's been done, what failed, what other agents are doing
in parallel. Reference spec / branch / prior PRs where relevant.>

## Repo
- Root: <REPO_ROOT>
- Branch: <BRANCH> (work directly here; do not switch branches)
- Spec: <SPEC_PATH or "none">

## What to <build / fix / verify>
1. <action> — success criterion: <criterion> (file: <path>)
2. <action> — success criterion: <criterion> (file: <path>)
3. ...
[5-10 items. Indent sub-items if ordering matters.]

## Don't
- Don't refactor unrelated code
- Don't add features beyond this brief
- Don't break existing tests (currently: <N> passing)
- <task-specific don'ts>

## Validation
Run: `<EXACT_COMMAND>`
Confirm <N> tests pass (was <M>). If new failures: classify as impl bug vs
test bug. Don't fix impl bugs — mark with xfail and note them in your report.

## Deliverables
When done:
1. git add -A && git commit -m "<MESSAGE_TEMPLATE>" && git push -u origin <BRANCH>
2. mcp__github__create_pull_request — title: "<TITLE>", base: main,
   head: <BRANCH>, body: <BULLET_LIST_OF_CHANGES>
3. Report: PR number, files changed, test count delta, any caveats.

[If you commit local changes at any point, push them before stopping.
The dispatcher can pick up local-but-unpushed work.]

## Known traps
[Optional — list runtime gotchas specific to this project. Examples:
- If pytest can't import X: `uv tool install pytest --with X --force`
- If git push fails with non-fast-forward: re-fetch and reset
- mcp__github__add_issue_comment appends a trailer; use JSONDecoder().raw_decode()
  not json.loads() if parsing comment bodies downstream]

## Time budget
Cap effort at ~<N> minutes. If stuck, propose a PIVOT rather than digging
deeper. Report the top 2 candidates and the recommended next diagnostic step.

## Report format
Under <WORD_BUDGET> words. Required sections: <list>.
```

---

## Subagent type selection

| Task | Subagent type |
|------|---------------|
| Implement / build | `general-purpose` |
| Review / critique | `general-purpose` (read-only emphasis in brief) |
| Find code locations / open-ended search | `Explore` |
| Design implementation approach | `Plan` |
| Configure status line | `statusline-setup` |
| GitHub Code/CLI/SDK questions | `claude-code-guide` |

Rules:
- Don't use a subagent for a 1-tool-call task (overhead > benefit).
- Use `Explore` for "where is X defined" — much faster than `general-purpose`.
- Use `Plan` when you want strategy without implementation.

---

## Parallel vs serial dispatch

**Parallel** (multiple Agent calls in one message):

Use when ALL of these are true:
- Subagents touch disjoint files
- No order dependency between subagents
- Total count ≤ 4

**Serial** (dispatch one, wait for result, dispatch next):

Use when ANY of these is true:
- Subagent N depends on subagent N-1's PR being merged
- Subagents share a branch or files
- Long-running work where the dispatcher must act on each result

When in doubt, serial is safer. Parallel failures can leave inconsistent state.

---

## Foreground vs background

The `Agent` tool has a `run_in_background` parameter.

**Foreground** (default — `run_in_background=false`):
- Dispatcher blocks until subagent finishes.
- Use when the result determines next steps.
- Use for all fanout dispatches (dispatch all foreground in one message;
  harness parallelizes them and delivers all results before dispatcher
  continues).

**Background** (`run_in_background=true`):
- Dispatcher continues; gets notification on completion.
- Use for long-running solo dispatches when there's other work to do
  (TodoWrite updates, file reads, etc.).

---

## Generated mode

When the dispatcher passes a goal, this skill produces a populated brief.

**Input format:**

```
GOAL: <what to build/fix/debug>
REPO_ROOT: <path>
BRANCH: <branch>
SPEC_PATH: <path or "none">
CURRENT_TESTS: <N passing>
TEST_COMMAND: <exact command>
TIME_BUDGET: <minutes>
WORD_BUDGET: <words>
TASK_TYPE: implement | debug | test | review
```

**Skill output:** a fully populated brief using the template above. The skill:
1. Selects the subagent type from the mapping table.
2. Infers role and identity framing from TASK_TYPE.
3. Derives 5-10 numbered deliverables from GOAL.
4. Fills in standard don'ts plus any task-specific ones.
5. Inserts the exact TEST_COMMAND into the validation section.
6. Sets TIME_BUDGET and WORD_BUDGET.
7. Leaves Known Traps blank — the dispatcher fills these in from project
   knowledge.

---

## Recovery patterns

### Context exhaustion
The subagent stops mid-task. If it committed local changes: the dispatcher
manually pushes (`git push -u origin <branch>`) and opens the PR.
Prevention: always include "If you commit local changes, push them before
stopping" in the brief.

### Brief misunderstanding
The subagent produces output that diverges from the brief. Dispatcher reviews
the report, identifies the misalignment, and dispatches a corrective subagent
with a narrow brief targeting only the delta.

### Tool failure (e.g., MCP timeout)
The subagent should report the failure rather than retrying indefinitely.
Retries are the dispatcher's decision. Include in brief: "If a tool call fails
after 2 attempts, stop and report the failure with the exact error."

---

## Anti-patterns

### 1. Vague brief
Bad: "Clean up the code in /src and add some tests."
Fix: enumerate. "Refactor src/foo.py: rename `bar` to `baz` everywhere. Add
tests for `baz` covering happy path, empty input, and error cases. Don't touch
src/quux.py."

### 2. Over-instruction
Bad: "Write tests in this exact order, with these exact names, using these
exact assertions..."
Fix: if you know every detail, do it yourself. Subagents add value when their
judgment fills gaps. Specify outcomes, not methods.

### 3. No report shape
Bad: "Build the feature and let me know when done."
Fix: "Report back in under 400 words: PR number, file list, test count delta,
any caveats."

### 4. No don'ts
Bad: brief with only a "What to build" section.
Fix: always include "don't refactor unrelated code" and "don't add features
beyond this brief." Subagents will scope-creep if not told not to.

### 5. No validation step
Bad: "Add the feature and open a PR."
Fix: always include the exact test command and expected pass count. Without
it, subagents sometimes think "looks done" without checking.

### 6. Overscoped brief
Bad: 11 deliverables across 20 files spanning code, tests, docs, and spec.
Fix: split into sequential focused briefs. Split heuristic:
- >8 deliverables → split
- >10 files to modify → split
- >3 architectural layers (e.g., code + tests + docs + spec) → split

Each split brief should be under 20 minutes, touch ≤5 files, and have one
output type (code, tests, or docs — not all three).

---

## Examples

See the `examples/` directory:
- `examples/good-brief-test-writer.md` — test-writer brief that produced 110
  tests, 92% coverage, zero rework. Annotated with why it worked.
- `examples/good-brief-debug.md` — debug brief with 7 hypotheses that found
  the root cause in 13 minutes. Annotated with why it worked.
- `examples/bad-brief-overscoped.md` — overscoped brief that ran out of
  budget mid-task, plus the corrected split into 3 focused briefs.
