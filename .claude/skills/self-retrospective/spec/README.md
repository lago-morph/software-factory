# `self-retrospective` skill

A skill that turns a long session into reusable knowledge before it's lost to
context truncation.

## Why

Long sessions accumulate real value: bugs found and fixed, workarounds invented,
orchestration patterns that worked, brief structures that failed. Without
deliberately harvesting that value, it evaporates when context resets.

## The three parts

1. **What happened** — phase-by-phase narrative with metrics table.
2. **Skills to extract** — each candidate skill in a uniform template with
   purpose, trigger, core content, anti-patterns, and example.
3. **Repo conventions** — AGENTS.md-ready rules grounded in session events.

## Two modes

- **Mode A (chat-only)**: a markdown document delivered inline. Default.
- **Mode B (package)**: a filesystem directory tree committed to a feature
  branch — each skill gets its own `README.md`, `SPEC.md`, and optional
  `excerpts.jsonl` / `examples/`. Best for sessions with 5+ skill candidates.

## Trigger phrases

Direct: "Do a retrospective", "What did we learn?", "What skills could we
extract?", "Lessons learned?", "Anything to add to AGENTS.md?"

Proactive (offer when): session spanned multiple phases, surfaced unexpected
real-world findings, used ≥5 subagents, ran >2 hours, or user says something
session-wrapping like "OK we're done", "good work", "let's stop here".

## Status

Spec only — see `SPEC.md`.

## See also

- `agent-dispatch-loop` exit reporting — complements this skill (iteration
  report goes in the repo; session retrospective produces the input to build
  new skills).
- `parallel-subagent-fanout` — frequently mentioned as a skill to extract
  during retrospectives.
