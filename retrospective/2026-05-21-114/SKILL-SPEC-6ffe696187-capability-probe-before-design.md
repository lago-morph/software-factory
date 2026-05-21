# Spec: `capability-probe-before-design`

- **ID**: SKILL-SPEC-6ffe696187
- **Source retrospective**: ../2026-05-21-114.md

## Intent

Before designing or coding any skill, agent behavior, or workflow that depends on external API capabilities (especially MCP servers), systematically probe each required capability via a read-only call. Record what is available, what is missing, and what is only achievable via convention. The probe results then dictate which behaviors can be implemented as-is, which must be downgraded, and which must be declined. This prevents the common failure mode of proposing automation that depends on a capability the MCP server does not expose, caught only after writing the design doc and committing to it. The skill was demonstrated in PR #114 (`issue-management`): a ten-call probe before design surfaced the lack of `create_label`, the 403 on `list_issue_types`, the `state_reason` enum constraints, and the identity model — every one of which directly shaped a behavior decision that would otherwise have been wrong-on-arrival.

## Trigger

**Direct triggers** — activate immediately:

- "Design a skill that uses the GitHub / Cloudflare / Slack MCP server."
- "Write a behavior that integrates with `<MCP tool name>`."
- "Before you start, figure out what's allowed with the MCP server."
- Any user prompt that asks for automation against an MCP-hosted API.

**Proactive triggers** — invoke without being asked when:

- The agent is about to author a skill SKILL.md that references one or more `mcp__<server>__<tool>` tool calls in its workflow.
- A planned behavior depends on a write tool (e.g., `issue_write`, `create_branch`); probe whether the matching read tool (e.g., `issue_read`, `list_branches`) and any prerequisites (labels, milestones, identities) are available first.
- The agent is migrating a skill from one MCP server to another (e.g., GitHub → GitLab) and assumptions must be re-validated.

**Negative triggers** — do NOT use this skill for:

- Local CLI tool usage (use `--help` or man pages, not a probe).
- Pure-local file manipulation that touches no external service.
- Repeated invocations against the same MCP server within a session — probe once, cache the result.

## Inputs

- The list of MCP tools the planned design intends to call (from the skill's draft workflow, or from a list the user supplies).
- Free credentials for read-only calls against the target MCP server (assumed: the same identity the agent is already authenticated as).
- Optional: a list of "convention-based" capabilities the design assumes (e.g., GitHub's `Closes #N` keyword in PR bodies) that warrant a one-line lookup to confirm.

## Outputs

- A markdown capability table (rows = capability, columns = "Achievable?" + how) that the calling skill embeds in its SKILL.md (typically near the bottom in a "Capability reference" section).
- For each design-blocked capability: a downgrade proposal (use a comment instead of a label; require the user to pre-create the artifact in the UI; etc.) OR a clear "decline" with reason.
- A one-paragraph "what was probed" subsection that the calling skill's PR body cites, so reviewers can audit the assumptions.

## Workflow

1. **Enumerate the required capabilities.** Read the draft SKILL.md (or the user's request) and list every distinct MCP tool the design intends to call. For each, also list any prerequisites the design assumes (e.g., a label being applicable assumes the label exists).
2. **For each capability, identify the probing read-only call.** Examples: for label-application, probe `get_label`. For assignee-write, probe `get_me`. For org-level features, probe a list-or-get tool at the org scope.
3. **Execute the probes.** Make all read-only calls. Record the verbatim response (or error code + message) for each.
4. **Classify each capability** into Yes / No / Yes-via-convention. Convention examples: `Closes #N` in PR body to close an issue (not a tool); `state_reason="not_planned"` + label to represent wontfix (not a state value).
5. **For every No row**, draft three responses: (a) **downgrade** to a feasible mechanism (e.g., "use a comment instead of a label"), (b) **defer** by asking the user to pre-create the missing artifact in the UI, or (c) **decline** with a clear reason. Offer (a) before (c).
6. **Write the capability table** into the calling skill's SKILL.md, with each row linked back to the probe call that confirmed it. Keep the verbatim probe responses out of the table (they go in the retrospective's evidence pool if needed).
7. **Cite the probe in the PR description** so reviewers can verify the assumptions without re-running every call.

## Concrete examples

### Example 1: PR #114 — `issue-management` skill design

The user asked for an issue-management skill. The capability probe before design:

- `mcp__github__get_me` → `{"login":"jonathanmanton",…}` → identity model: agent and user share a login; "claim" via assignee is technically self-assignment.
- `mcp__github__list_issue_types` → `403 Resource not accessible by integration` → can't set `issue.type`; must use labels for type semantics.
- `mcp__github__get_label` for `in-progress` → `404 not found` → no pre-existing label for "claimed by agent."
- `mcp__github__get_label` for each of `bug`, `documentation`, `duplicate`, `enhancement`, `good first issue`, `help wanted`, `invalid`, `question`, `wontfix` → all present, all are GitHub defaults.
- ToolSearch for `create_label` → no match → cannot create new labels via MCP.

Design impact:
- Dropped the planned "create `in-progress` label" approach. Repurposed the existing `good first issue` default as the claim marker.
- Used `not_planned` + the `wontfix` / `invalid` label to represent those closure types (no matching state_reason enum value).
- Switched all "assign self" steps from a hardcoded login to a runtime `get_me` lookup.

The capability table landed in the SKILL.md as a "Capability reference" section; the PR body cited the probe results so the reviewer could audit.

### Example 2: Hypothetical future Cloudflare-MCP-using skill

User says: "Design a skill that creates a D1 database, runs a migration, and emits a status comment."

Probe sequence:

- `mcp__cloudflare__d1_database_create` schema present → can create.
- `mcp__cloudflare__d1_database_query` schema present → can run migration SQL.
- `mcp__cloudflare__accounts_list` to find the account ID prereq → confirms the user must supply or `set_active_account` to one.
- ToolSearch for any "status comment" or "post to issue" Cloudflare tool → no match → status emission needs another MCP server (GitHub) or a local file.

Design impact: the "emit status comment" step is *not* Cloudflare-native; the skill must call out that it needs a separate GitHub-MCP path for that step, or downgrade to "write status to a local file."

## Anti-patterns

- **Designing first, probing after.** Half the design becomes throw-away when the probe surfaces an infeasibility. Probe first.
- **Probing only the write tools.** A write tool's success often depends on a read prerequisite (a label existing, an identity being a collaborator). Probe the prerequisites too.
- **Skipping the convention-based capabilities.** `Closes #N` in PR bodies is not a tool — but the skill must document it as the way PR-closes-issue is achieved. Forgetting it leads to writing a "tie PR to issue" behavior with no implementation.
- **Trusting a tool name's implied scope.** `list_issue_types` reads "list issue types" but is org-scoped and may 403 on read for non-admin tokens. Always probe; never assume.
- **Re-probing within a session.** Cache results. The probe is one-time at design time, not per-call.

## Acceptance criteria

- [ ] Every MCP tool referenced in the calling skill's workflow has a row in the capability table.
- [ ] Every "No" row has either a downgrade, a defer-to-user, or a decline documented inline.
- [ ] The calling skill's SKILL.md cites the probe (link or inline table) so future maintainers don't re-derive it.
- [ ] The PR description names the probe and what it found, so reviewers can audit without re-running calls.
- [ ] No probe call is repeated within a session.

## Files this skill creates / modifies

- The **calling skill's `SKILL.md`** — appends or refreshes a "Capability reference" section.
- The **PR description** of the work that adopts the calling skill — cites probe findings.
- No standalone files of its own; this skill is a workflow pattern applied to other skills' creation.
