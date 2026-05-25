# CLAUDE.md

This file is Claude Code's per-repo conventions loader. The actual conventions live in [AGENTS.md](./AGENTS.md) so they are visible to other coding agents (Codex, etc.) that follow the OpenAI AGENTS.md convention.

**Session-startup convention.** At the start of any session in this repo, read [`AGENTS.md`](./AGENTS.md) first (project-wide directives that override harness defaults — e.g., PR draft-vs-ready policy), then read [`AGENT-ENTRY.md`](./AGENT-ENTRY.md) and follow its navigation for the stated task. The entry doc names what each foundational doc contains so you can drill into the right sub-doc without eagerly loading the full reading list. See [`CONTEXT-SLIMMING-PLAN.md`](./CONTEXT-SLIMMING-PLAN.md) for the rationale.
