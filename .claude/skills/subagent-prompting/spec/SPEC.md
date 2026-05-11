# `subagent-prompting` — implementation spec

A reference skill that codifies the patterns that consistently
produced good subagent outputs. Loaded by the dispatcher whenever it's
about to write a subagent brief.

## 1. Trigger conditions

Activate whenever the dispatcher is about to call the `Agent` tool
(or equivalent in the harness). Every subagent dispatch can benefit;
the skill should be lightweight enough to always be in scope.

Stronger triggers:
- Multiple subagents in flight or planned
- Long-running subagent (>5 minutes expected)
- High-stakes work where rework is expensive

## 2. The brief structure (the spine)

Every subagent brief should have these sections in this order:

### 2.1 Identity + goal (1-3 sentences)

> "You are <role> for <task>. <One-sentence goal>. <One-sentence why
> this matters / why we're not doing it ourselves>."

Why: the subagent needs to know what kind of work it's doing
(implement, review, debug, test). Identity framing aligns its
default style.

### 2.2 Context (3-6 sentences)

> Brief restatement of what's been done, what failed, what other
> agents are doing in parallel. References to spec / branch /
> previous PRs.

Cap at 6 sentences. The subagent doesn't need the full conversation;
it needs enough to make local decisions.

### 2.3 Repo + branch (concrete paths)

> "- Repo: /home/user/<dir>
> - Branch: <branch> (work directly here; do not switch)
> - Spec: <path>"

Why: the #1 footgun is subagents creating their own branches or
pushing to main. Always specify.

### 2.4 What to build / fix / verify (numbered list)

Numbered list, ideally 5-10 items. Each item has:
- The action ("Add X", "Verify Y", "Fix Z")
- Concrete success criteria
- File paths or function names where relevant

If there are sub-items or ordering matters, indent.

### 2.5 Don't do (the constraints)

This section saves more rework than any other. Always include:
- "Don't refactor unrelated code"
- "Don't add features beyond this brief"
- "Don't break existing tests" (with target count)
- Plus task-specific don'ts

### 2.6 Validation / test step (concrete commands)

> "Run `python -m pytest tests/ -v --tb=short 2>&1 | tail -40`.
> Confirm <N> pass (was <M>). If new failures, classify as impl bug
> vs test bug. Don't fix impl bugs unless they're trivially yours."

Always provide the exact command to run, not "run the tests."

### 2.7 Deliverable shape

> "When done:
> 1. `git add -A && git commit -m '<message-template>'`
> 2. `git push -u origin <branch>`
> 3. `mcp__github__create_pull_request` with:
>    - title: '<exact title>'
>    - base: main
>    - head: <branch>
>    - body: <bullet list of changes>
> 4. Report: PR number, file list, test count delta, any caveats."

Without this, results vary wildly. With it, every subagent produces
the same deliverable shape.

### 2.8 Traps + known issues (optional but high-value)

> "Known traps:
> - If pytest can't import jsonschema: `uv tool install pytest --with jsonschema --with pytest-cov --force`
> - If git push fails with non-fast-forward, re-fetch and reset
> - The MCP `add_issue_comment` tool appends a Claude Code trailer;
>   parsers must use `JSONDecoder().raw_decode()` not `json.loads()`"

Each trap saves a few minutes of subagent confusion.

### 2.9 Time budget (optional)

> "Cap effort at ~30 minutes. If you can't isolate the bug after
> that, propose a pivot rather than digging deeper."

Especially valuable for debug tasks that can spiral.

### 2.10 Report format + word budget

> "Report back in under 600 words. Sections: PR number, files
> changed, test count, blocking issues if any, recommendations."

Without a word cap, reports can balloon. Caps protect dispatcher
context.

## 3. Choosing the subagent type

Map task to subagent type:

| Task | Subagent type |
|------|---------------|
| Implement / build | `general-purpose` |
| Review / critique | `general-purpose` (with read-only emphasis) |
| Find code locations / open-ended search | `Explore` |
| Design implementation approach | `Plan` |
| Configure status line | `statusline-setup` |
| GitHub Code/CLI/SDK questions | `claude-code-guide` |

Misc rules:
- Don't use a subagent for a 1-tool-call task (overhead > benefit).
- Use `Explore` instead of `general-purpose` for "where is X
  defined" questions — much faster.
- Use `Plan` when you want a strategy without implementation.

## 4. Parallel vs serial dispatch

**Parallel** (single dispatcher message, multiple Agent calls):
- Subagents touch disjoint files
- Subagents are independent (no order dependency)
- Total subagents ≤ 4 (more = notification noise)

**Serial** (dispatch one, wait, dispatch next):
- Subagent N depends on subagent N-1's PR being merged
- Shared state (same branch, same files)
- Long-running and the dispatcher needs to act on each result

In this session, parallel was used for Phase 0/1 (disjoint files) and
serial was used for the iteration loop (sequential PRs).

## 5. Run-in-background vs foreground

`Agent` tool has `run_in_background` parameter:

- **Foreground (default)**: dispatcher blocks until subagent finishes.
  Useful when the result determines next steps.
- **Background**: dispatcher continues; gets notification on
  completion. Useful when there's other work to do.

For fanouts: dispatch all in foreground in a single message — the
harness usually parallelizes, and the dispatcher gets all results
before continuing.

For long-running solo dispatches: background, so the dispatcher can
do other work (TodoWrite updates, file reads) while waiting.

## 6. Recovery patterns

Subagents can fail in these ways:

- **Context exhaustion** (rare but happened in this session). The
  subagent committed locally before stopping. Recovery: dispatcher
  picks up the local commit, pushes, opens PR, fills in remaining
  steps. Subagent prompts should encourage early commits.
- **Misunderstanding the brief**. Dispatcher reviews the report,
  identifies the misalignment, dispatches a corrective subagent (or
  fixes inline if scope is small).
- **Tool failure** (e.g., MCP timeout). Subagent should report the
  failure rather than retry indefinitely. Retries are the
  dispatcher's call.

The brief should include: "If you commit local changes, push them
before stopping. The dispatcher can pick up local-but-unpushed work."

## 7. Anti-patterns

### Vague briefs
> "Clean up the code in /src and add some tests."

What gets cleaned? What tests? Subagent picks something; dispatcher
hates the result.

Fix: enumerate. "Refactor src/foo.py: rename `bar` to `baz` everywhere.
Add tests for `baz` covering happy path, empty input, and error
cases. Don't touch src/quux.py."

### Over-instruction
> "Write tests in this exact order, with these exact names, using
> these exact assertions..."

If you know all that, do it yourself. Subagents are for tasks where
their judgment adds value.

### Forgetting the report shape
> "Build the feature and let me know when done."

Result: a 3000-word essay describing every line of code. Wastes
dispatcher context.

Fix: "Report back in under 400 words: PR number, file list, test
count delta, any caveats."

### No don'ts
Subagents will scope-creep. Always include "don't refactor unrelated
code" and "don't add features beyond this brief."

### No verification step
Without "run the tests and confirm count is X," subagents sometimes
think "looks done" without checking. Always include validation.

### Briefing every detail in long prose

If your brief is >2000 words, restructure. The numbered-list
structure (§2) is dense and scannable.

### Forgetting to ask for commit + push

The #1 way work is "lost" — subagent did the work, didn't push, then
the local clone is gone. Always include the push + PR step in the
deliverable section.

## 8. Examples

See `examples/` directory:
- `examples/good-brief-test-writer.md` — the iter 2 test-writer
  brief that produced 67 tests cleanly
- `examples/good-brief-debug.md` — the workflow-debug brief that
  enumerated hypotheses and found the root cause efficiently
- `examples/bad-brief-overscoped.md` — the lock-vs-bot fix brief that
  was too ambitious; how it could have been split into smaller pieces

## 9. Skill invocation

Two modes:

- **Inline mode**: Dispatcher imports the brief template and fills
  it in. Lightweight.
- **Generated mode**: Dispatcher passes a goal to the skill; skill
  generates the full brief. Heavier but consistent.

Most projects want inline. Generated is useful inside
`parallel-subagent-fanout`.

## 10. Test plan (when built)

- Verify the brief template renders correctly with sample inputs.
- Snapshot test: known-good briefs from this session round-trip
  through the template.
- Lint test: a brief without "Don't" or without a verification step
  triggers a warning.

## 11. Living document

Update this skill whenever a new pattern emerges from real subagent
dispatches. The accumulated patterns ARE the value.
