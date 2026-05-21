# agent instruction

**Never hardcode the MCP-authenticated identity.** Skills, scripts, and configuration must not embed a literal GitHub login (or other MCP-resolved identity). Resolve it at runtime via `mcp__github__get_me` (or equivalent) and cache it for the session. Use a placeholder like `<mcp-login>` in documentation.

*Grounded in: PR #114, where the user explicitly directed "it should not hard code my name; it should query the mcp server for the identity used by the mcp server and use that."*

# justification

The first draft of `issue-management/SKILL.md` hardcoded `jonathanmanton` in seven places — assignee lists, capability tables, example commands. The user explicitly instructed: "It should not hard code my name. It should query the mcp server for the identity used by the mcp server and use that." This is a portability invariant, not a style preference: if the skill files are ever copied to a fork, used by a different MCP identity, or moved across orgs, every hardcoded login becomes a silent miscredit (assignments to a stranger, commits attributed to the wrong identity, examples that say the wrong thing).

The marginal cost of `get_me` is one MCP call cached for the session. The cost of every hardcode is a future correction commit plus whatever rot accumulated in between — silently incorrect assignees on closed issues, examples that confuse new readers, and a fork-blocking dependency on one specific login.
