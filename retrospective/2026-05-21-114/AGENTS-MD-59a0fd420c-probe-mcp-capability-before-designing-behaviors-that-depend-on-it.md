# agent instruction

**Probe MCP capability before designing behaviors that depend on it.** Before designing any skill behavior, automation, or convention that depends on an MCP server tool, perform a read-only probe of every required capability (e.g., `get_label`, `get_me`, `list_issue_types`) and document what is available, what is missing, and what is only achievable via convention. Design only what the probe confirms is feasible; downgrade or decline the rest.

*Grounded in: PR #114, where probing `list_issue_types`, `get_label`, `create_label` (absent) up front killed bad behavior proposals before they reached the design doc.*

# justification

When the user asked for an issue-management skill, the explicit first instruction was "try to figure out what is allowed with the GitHub mcp server you are connected to." That probe surfaced four hard constraints that shaped every behavior in the final skill: no `create_label` tool (forced repurposing `good first issue` instead of inventing `in-progress`), no `list_issue_types` access (forced using labels for type semantics), no `wontfix`/`invalid` state_reason enum (forced `not_planned` + label combinations), and identity-via-`get_me` rather than hardcoded login. Without the probe, all four would have been discovered as bugs *after* the design was committed to disk.

The marginal cost was ten read-only MCP calls and one tool-list survey — under two minutes of agent time. The cost of skipping it is rework: every infeasible behavior consumes a full design-implement-discover-revert cycle, which in this session would have multiplied into hours. Probing is also a documentation artifact: the capability table that lands in the resulting SKILL.md tells the *next* agent (and the next maintainer) what the MCP supports without re-running the calls, compounding the one-time investment across every future skill that touches the same server.
