# ADR: Repurpose the GitHub default `help wanted` label as the permanent marker of agent-authored issues

- **ID**: ADR-1a742b7f91
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-21
- **Source retrospective**: ../2026-05-21-117.md
- **PRs covered**: #117

## Context

Both the human user and the agent author issues in this repo. Scanning the open-issues list for "what's mine vs. what's the agent's" was guesswork: the assignee column doesn't help (the MCP authenticates as the user's GitHub identity, so agent-created issues appear under `jonathanmanton` regardless), and the first-comment author has the same problem. A label-based marker solves it in one look.

The GitHub MCP can apply labels but **cannot create them** (`create_label` isn't exposed). So any marker has to be a label that already exists in the repo, which in practice means one of the GitHub defaults: `bug`, `documentation`, `duplicate`, `enhancement`, `good first issue`, `help wanted`, `invalid`, `question`, `wontfix`. The repo already repurposes `good first issue` to mean "an agent has claimed this issue" (PR-pre-#117 convention in `issue-management`'s STARTED behavior). `help wanted` is the only remaining default whose original semantic ("we'd like community help on this") doesn't clash with an existing convention in this repo.

## Decision

Every issue created by the agent receives the `help wanted` label in the same `issue_write method=create` call, and that label is preserved for the lifetime of the issue — never removed by any subsequent behavior (STARTED, ANSWERS, closure of any kind). The label is the agent-authorship marker; its presence on a closed issue is exactly as informative as on an open one. The mechanism lives in the `issue-management` skill's CREATE-ISSUE behavior (added in PR #117).

## Alternatives considered

- **Create a dedicated `agent-authored` label.** Strictly preferable on semantics, but the MCP can't create labels. Requires a one-time human setup step in the GitHub UI before the skill can apply it. Rejected for now — the marginal-cost gap (zero with `help wanted`, "user has to remember to create a label" with `agent-authored`) outweighs the semantic drift. Revisit if the MCP grows `create_label`.
- **Per-comment `<!-- agent-authored -->` marker in the issue body.** Survives copy-paste, doesn't require any pre-existing label, but isn't visible in the issue list — the whole point of the marker is one-look scannability of the list view. Rejected.
- **No marker at all.** Status quo. Rejected because the scan-for-mine cost recurs every time the user opens the issue list and is purely opportunistic for the agent to file follow-ups (the friction discourages doing the right thing).
- **Apply the marker but treat it as transient (removed on close).** Rejected because the agent-authorship signal is just as useful on a closed issue as an open one — retrospective triage often asks "did the agent file this?", and the answer should still be visible.

## Consequences

**Easier**: scanning the issue list for agent-authored items is one filter (`label:"help wanted"`). Filing follow-up issues from the agent becomes friction-free — the labeling is silent and automatic, no comment, no extra round-trip. Issue #118 was filed via the new behavior immediately after PR #117's commit and the label landed in the same create call.

**Harder**: the GitHub default semantic of `help wanted` ("we'd welcome community contributions") is gone in this repo. New contributors will likely misread it. Documentation in `AGENTS.md` and the `issue-management` skill's label-lifecycle summary calls this out, but the misread is a real cost. The cost is bounded because the repo's contributor surface is small (one human + one agent today).

**Trade-off accepted**: semantic-drift cost on a default label vs. the friction-removal benefit of a built-in marker. The judgment is that the friction cost compounds (every issue list scan, every agent follow-up filing) while the semantic-drift cost is a one-time misread per new contributor. If the contributor base grows, the right move is to migrate to a `agent-authored` label (assuming `create_label` exists by then) and run a one-off relabel script over historical issues.

## References

- [`../2026-05-21-117.md`](../2026-05-21-117.md) — the source retrospective.
- [`./ADR-dec26d09fd-self-installing-pretooluse-hooks-for-skill-load-enforcement.md`](./ADR-dec26d09fd-self-installing-pretooluse-hooks-for-skill-load-enforcement.md) — sibling decision (the gate that ensures CREATE-ISSUE actually fires).
- PRs the decision was made in: #117 (added the CREATE-ISSUE behavior). First exercise: issue #118.
- The `issue-management` skill's CREATE-ISSUE section in `.claude/skills/issue-management/SKILL.md` (post-PR #117) — the operational spec; this ADR records the binding rationale.
