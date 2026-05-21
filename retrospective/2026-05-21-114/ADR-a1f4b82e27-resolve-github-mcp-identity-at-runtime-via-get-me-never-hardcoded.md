# ADR: Resolve GitHub MCP identity at runtime via `get_me`, never hardcoded

- **ID**: ADR-a1f4b82e27
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-21
- **Source retrospective**: ../2026-05-21-114.md
- **PRs covered**: #114

## Context

The first draft of the `issue-management` skill (PR #114, commit `f15bd16`) hardcoded the literal GitHub login `jonathanmanton` in seven places — assignee instructions in the STARTED behavior, capability tables, example commands in the workflow sections, and in the sub-skill's intake-walk side-effect checklist. This was a convenience: the agent's session is authenticated as `jonathanmanton` (the same human as the user), so the value is known and constant within the session.

In review (commit `0a02975`'s prompt) the user directed: "It should not hard code my name. It should query the mcp server for the identity used by the mcp server and use that." The directive identified a portability invariant: if the skill files are ever copied to a fork, used by a different MCP identity, or moved across orgs, every hardcoded login becomes a silent miscredit. The `mcp__github__get_me` tool returns a `login` field that resolves the current identity at runtime, with zero ambiguity.

## Decision

All skills that integrate with the GitHub MCP server resolve the authenticated login via `mcp__github__get_me` at runtime — once per session, cached as `<mcp-login>` — and never embed a literal login in skill files, templates, or examples. Documentation and templates use the placeholder string `<mcp-login>` (or equivalent) to indicate the runtime-resolved value.

The same principle applies by extension to any MCP server that exposes a `get_me`-equivalent identity probe.

## Alternatives considered

- **Hardcode the login in skill files** — rejected per user's explicit directive. Breaks portability and creates silent miscredits on fork/copy.
- **Resolve from a single project-level config file** (e.g., `.claude/identity.json`) — rejected because the MCP server already has the canonical answer via `get_me`; a config file is redundant and adds a sync risk.
- **Resolve from git config (`user.email`, `user.name`)** — rejected because git identity is not necessarily the same as the GitHub identity (different emails, no-reply addresses, bot accounts), and git config isn't authoritative for what the MCP server will accept as an assignee.
- **Document the login as a one-time install constant the user fills in** — rejected as friction. The agent already has the value at runtime; making the user copy it in by hand creates copy errors and binds the install to a single identity.

## Consequences

**What becomes easier:** Skill files are portable across forks, copies, and identity changes with no edits required. Re-auth or identity change mid-session resolves correctly on the next `get_me`. Documentation reads identically regardless of who installed it.

**What becomes harder:** Every skill that uses the identity must remember to call `get_me` (one extra MCP call at the start of the workflow). The discipline must be propagated to every future GitHub-integrating skill — captured as agents-file rule `AGENTS-MD-91e4d06700` so it stays visible.

**What we're explicitly not promising:** Resolving identity for other MCP servers. The decision is GitHub-specific; analogous rules for Cloudflare, Slack, or any other MCP server need their own ADR if and when those skills are written.

## References

- [`../2026-05-21-114.md`](../2026-05-21-114.md) — the source retrospective.
- [`./AGENTS-MD-91e4d06700-never-hardcode-the-mcp-authenticated-identity.md`](./AGENTS-MD-91e4d06700-never-hardcode-the-mcp-authenticated-identity.md) — the corresponding agents-file rule.
- [`../../.claude/skills/issue-management/SKILL.md`](../../.claude/skills/issue-management/SKILL.md) — the skill applying this pattern.
- PR the decision was made in: #114 (specifically commit `0a02975`).
