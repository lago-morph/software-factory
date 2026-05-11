# subagent-prompting

A reference skill that codifies the brief-writing patterns that consistently
produce good subagent outputs. Load it whenever you're about to dispatch a
subagent.

```
vague brief → scope creep, wrong approach, rework
structured brief → targeted output, measurable success, zero rework
```

## Evidence

From ~14 dispatches in one session:
- Test-writer brief with explicit pinning targets → 110 tests, 92% coverage,
  zero rework.
- Debug brief enumerating 7 hypotheses → root cause in 13 minutes.
- Overscoped brief spanning 11 deliverables and 20 files → subagent ran out
  of budget mid-task; partial recovery only.

## When to use

Use this skill every time you're about to dispatch a subagent. The overhead is
minimal; the benefit compounds across the session.

Stronger triggers:
- Multiple subagents in flight or planned
- Long-running subagent (>5 minutes expected)
- High-stakes work where rework is expensive

## The 9-section brief structure

Every brief should contain these sections in order:

| # | Section | Purpose |
|---|---------|---------|
| 1 | **Identity + goal** | Role framing (implement / debug / review / test) aligns default style |
| 2 | **Context** | 3-6 sentences of prior state, failures, parallel work |
| 3 | **Repo + branch** | Prevents wrong-branch footguns — always specify |
| 4 | **What to build/fix/verify** | Numbered list, 5-10 items, each with success criteria |
| 5 | **Don't do** | Constraints that prevent scope creep and breakage |
| 6 | **Validation** | Exact test command + expected count |
| 7 | **Deliverable shape** | Exact commit + push + PR + report instructions |
| 8 | **Known traps** | Runtime gotchas (optional but high-value) |
| 9 | **Time budget + report format** | Word cap on report; pivot instruction if stuck |

## Subagent type mapping

| Task | Subagent type |
|------|---------------|
| Implement / build | `general-purpose` |
| Review / critique | `general-purpose` (with read-only emphasis) |
| Find code locations / open-ended search | `Explore` |
| Design implementation approach | `Plan` |
| Configure status line | `statusline-setup` |
| GitHub Code/CLI/SDK questions | `claude-code-guide` |

Rules:
- Don't use a subagent for a 1-tool-call task (overhead > benefit).
- Use `Explore` for "where is X defined" — much faster than `general-purpose`.
- Use `Plan` when you want strategy without implementation.

## Parallel vs serial dispatch

**Parallel** (multiple Agent calls in one message):
- Subagents touch disjoint files
- No order dependency between subagents
- Total count ≤ 4 (more creates notification noise)

**Serial** (dispatch one, wait, dispatch next):
- Subagent N depends on subagent N-1's PR being merged
- Shared state (same branch, same files)
- Long-running work where the dispatcher must act on each result

## Foreground vs background

| Mode | When to use |
|------|------------|
| Foreground (default) | Result determines next steps; dispatcher blocks |
| Background (`run_in_background=true`) | Dispatcher has other work to do while waiting |

For fanouts: dispatch all foreground in a single message — the harness
parallelizes them and the dispatcher gets all results before continuing.

For long-running solo dispatches: background, so the dispatcher can update
todos and read files while waiting.

## Anti-patterns

| Failure mode | What happens | Fix |
|--------------|-------------|-----|
| **Vague brief** | "Clean up /src and add tests" — subagent picks something, dispatcher hates it | Enumerate: specific files, specific tests, specific assertions |
| **Over-instruction** | "Use exactly these test names in this order..." — if you know all that, do it yourself | Leave judgment to the subagent; specify outcomes not methods |
| **No report shape** | Report comes back as a 3000-word essay | Always include word cap + required sections |
| **No don'ts** | Subagent refactors adjacent code, adds unrequested features | Always include "don't refactor unrelated code" + "don't add features beyond this brief" |
| **No validation step** | Subagent thinks "looks done" without checking | Always include exact test command + expected pass count |
| **Overscoped brief** | >8 deliverables, >10 files, >3 architectural layers → subagent runs out of budget | Split into sequential focused briefs (see heuristic below) |

**Split heuristic**: if the brief has >8 deliverables, >10 files to modify,
or >3 architectural layers, break it into multiple sequential dispatches.

## Integration with other skills

| Skill | Relationship |
|-------|-------------|
| `agent-dispatch-loop` | Uses this skill's brief templates for steps 1–6 |
| `parallel-subagent-fanout` | Uses this skill's templates for each subtask's dispatch brief |

## Files in this skill

```
skills/subagent-prompting/
├── README.md                          ← this file
├── SKILL.md                           ← reference card + brief generator (the executable skill)
├── spec/
│   ├── README.md                      ← original overview from the spec repo
│   └── SPEC.md                        ← full implementation spec
└── examples/
    ├── good-brief-test-writer.md      ← iter-2 test-writer brief; 110 tests, 92% coverage
    ├── good-brief-debug.md            ← debug brief with 7 hypotheses; root cause in 13 min
    └── bad-brief-overscoped.md        ← overscoped brief; what went wrong + the 3-brief fix
```
