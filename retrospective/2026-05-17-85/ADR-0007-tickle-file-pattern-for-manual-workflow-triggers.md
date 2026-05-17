# ADR 0007: Tickle-file pattern for manual workflow triggers

## Context

GitHub Actions supports two manual-trigger mechanisms:
1. `workflow_dispatch` — clickable from the Actions UI by users with write access.
2. `repository_dispatch` — programmatic via the GitHub API with a dispatch event payload.

For the research-pipeline's `regen-sources-md-manual.yml` workflow (the manual escape hatch for regenerating `reference-only/sources.md` when something goes wrong), neither default is ideal:
- `workflow_dispatch` requires logging into the GitHub UI — annoying mid-AI-session.
- `repository_dispatch` requires API token management and isn't accessible from a restricted MCP server.

We needed a manual trigger that an AI in a sandbox could invoke using only the operations available in the restricted MCP server: commit + push.

## Decision

**Manual workflow triggers use a "tickle file" pattern: a sentinel file whose creation triggers the workflow, and which the workflow deletes as part of its commit.**

Operationalization:
- Workflow listens on `push: paths: ['reference-only/.regen-trigger']` (in addition to `workflow_dispatch` for the UI path).
- To trigger manually: AI creates `reference-only/.regen-trigger` (any content; we use a one-line note), commits, pushes.
- The workflow fires, performs the manual regen, **deletes** `.regen-trigger` as part of its own auto-commit.
- The tickle file's existence is therefore transient — typically <60 seconds between creation and workflow deletion.

The path filter scopes the trigger narrowly — only changes to that one file fire the workflow. The deletion-in-workflow prevents the trigger from re-firing on the auto-commit (different file changed). The `[skip ci]` in the auto-commit message is belt-and-suspenders.

## Alternatives considered

- **`workflow_dispatch` only** — requires UI access. Rejected for AI-driven scenarios.
- **`repository_dispatch` only** — requires API + token. Rejected for restricted-MCP scenarios.
- **`push: branches: [main]` with no path filter** — fires on every main commit, wastes runner minutes. Rejected.
- **`schedule: cron` with a "trigger file present?" check** — adds latency (cron resolution). Rejected.
- **Mark a comment with a magic string on the PR** — clever but hard to discover. Rejected.

## Consequences

**Positive:**
- AI agents in restricted-MCP environments can trigger workflows using commit + push, no special tooling.
- Path-filtered trigger is unambiguous — only one file fires the workflow.
- The pattern is observable in git history (the tickle file commit + workflow's auto-deletion commit) — debuggable.
- Combines with `workflow_dispatch` cleanly — both triggers can coexist; UI clickers and AI agents both work.

**Negative:**
- The tickle file is conceptually weird ("why is there an empty file with a special name in this directory?"). Mitigation: the workflow's auto-deletion keeps the lifetime short; SKILL.md documents the pattern.
- Race: if two agents create the tickle file in rapid succession, the second push fails (file already exists or merge conflict). Mitigation: the workflow runs idempotent regen, second trigger is harmless if the first completed; if the first didn't complete, the user investigates.
- If the workflow fails before deleting the tickle file, it stays in the tree (visible noise). Mitigation: SKILL.md instructs the AI to check whether `.regen-trigger` still exists after ~60 seconds and to investigate if so.

## References

- `.claude/skills/research-pipeline/resources/_workflows/regen-sources-md-manual.yml` — the workflow with the tickle pattern
- `.claude/skills/research-pipeline/SKILL.md` — config field `trigger_path: reference-only/.regen-trigger`
- `.claude/skills/research-pipeline/resources/github-action.md` — user-facing docs
- [Retrospective 2026-05-17-85, design conversation](../2026-05-17-85.md)
