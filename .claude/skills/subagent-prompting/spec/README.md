# `subagent-prompting` skill

A reference skill that codifies the patterns that consistently produced good
subagent outputs. Load it whenever you're about to write a subagent brief.

## Why

Subagents start with no conversation history and no established conventions.
Vague instructions produce unpredictable results — scope creep, wrong
approaches, or work that has to be redone. A structured brief eliminates most
of that waste.

## What it provides

- **The brief spine** — 9 sections in order, each with a purpose and template.
- **Subagent type mapping** — which agent type to use for which task.
- **Parallel vs serial rules** — when to fan out vs chain.
- **Foreground vs background dispatch** — when to block vs continue.
- **Recovery patterns** — what to do when a subagent fails mid-task.
- **Anti-patterns** — the 6 brief failure modes, each with a concrete fix.

## Evidence

From ~14 dispatches in one session:
- A test-writer brief with explicit pinning targets and edge cases → 110
  targeted tests, 92% coverage, zero rework.
- A debug brief enumerating 7 hypotheses → root cause found in 13 minutes.
- An overscoped brief spanning 11 deliverables and 20 files → subagent ran
  out of budget mid-task; recovered only because of an early commit.

## Status

Spec only — see `SPEC.md`.

## See also

- `parallel-subagent-fanout` — uses this skill's brief templates for each
  subtask's dispatch brief.
- `agent-dispatch-loop` — uses this skill's templates for steps 1–6.
