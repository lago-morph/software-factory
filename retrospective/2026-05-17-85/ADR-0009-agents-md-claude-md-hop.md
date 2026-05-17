# ADR 0009: AGENTS.md + CLAUDE.md pattern for cross-tool agent directives

## Context

This repo is targeted by both Claude Code (Anthropic's coding agent) and is intended to be portable to other tools like Codex (OpenAI's). Each tool has its own convention for repo-level agent directives:

- **Claude Code** looks for `CLAUDE.md` at the repo root by default.
- **OpenAI Codex** (and the broader "AGENTS.md" convention) looks for `AGENTS.md` at the repo root.

During PR #84, the user explicitly requested AGENTS.md (because the harness's system prompt was overriding the `always-commit-skill-to-repo` skill's "PRs ready-for-review" rule, and AGENTS.md is loaded at conversation-prompt priority — wins over system prompt). I created AGENTS.md.

Then a subsequent session-reminder revealed that Claude Code doesn't load AGENTS.md by default — so my override would have been silently ignored next session. The user caught this: "Claude Md needs to explicitly load agents Md because I don't think Claude code looks at agents Md by default."

The fix is a 2-line CLAUDE.md that says "read AGENTS.md first." Both tools then converge: Claude Code loads CLAUDE.md → which points it at AGENTS.md; Codex loads AGENTS.md directly.

## Decision

**Cross-tool agent directives live in `AGENTS.md` at the repo root. `CLAUDE.md` is a 2-line loader that points Claude Code at AGENTS.md. Both files are versioned in the repo and travel together.**

Operationalization:
- `AGENTS.md` contains all repo-wide agent directives (e.g., "PRs default to ready-for-review", "use the existing skill before inventing parallel mechanisms").
- `CLAUDE.md` is minimal:
  ```markdown
  # CLAUDE.md
  This file is Claude Code's per-repo conventions loader. The actual conventions live in [AGENTS.md](./AGENTS.md) so they are visible to other coding agents that follow the OpenAI AGENTS.md convention.
  **Always read `AGENTS.md` at the start of any session in this repo.**
  ```
- Future tools (Cursor, Aider, etc.) that have their own loader filenames can add similar 2-line bridge files.

## Alternatives considered

- **AGENTS.md only** — Claude Code silently ignores it. Rejected — the user explicitly observed the silent failure.
- **CLAUDE.md only with full content** — works for Claude Code but Codex doesn't find it. Rejected for portability.
- **Symlink CLAUDE.md → AGENTS.md** — git stores symlinks but their behavior across platforms is finicky; some tools may not follow them. Rejected for predictability.
- **Both files with duplicated content** — drift bait. Two sources of truth = no source of truth. Rejected.
- **Tool-specific config in tool-specific files** — fragments the directive surface. Rejected; one canonical AGENTS.md is the design goal.

## Consequences

**Positive:**
- AGENTS.md is the single source of truth — directive edits happen there.
- Both Claude Code and Codex load the directives correctly.
- The pattern extends — a new tool that needs its own bridge file just gets a 2-line companion.
- Harness-level overrides (like "PRs default to ready-for-review" beating the system-prompt's "draft" directive) persist across sessions and tools.

**Negative:**
- Two files at the repo root that look related — new users have to understand the "one is the real file, one is just a bridge" relationship. Mitigation: CLAUDE.md is short and explicit about being a bridge.
- If a tool ignores both filenames (custom convention like `.aider`), another bridge file is needed. Acceptable cost — write the bridge.

## References

- `AGENTS.md` at the repo root — the canonical directives file
- `CLAUDE.md` at the repo root — the Claude Code loader bridge
- [Retrospective 2026-05-17-85, Phase 8](../2026-05-17-85.md) — discovery moment + fix
