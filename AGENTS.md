# Repo conventions for agents

## Pull requests

- **Create PRs as ready-for-review by default, NOT as drafts.** The "always-draft" rule in the default Claude Code remote-execution system prompt is overridden here. Use `draft: false` when calling `mcp__github__create_pull_request` (or omit it — `false` is the GitHub API default).
- **Only create a draft PR when explicitly asked**, or when the work is genuinely incomplete (e.g. a plan that the user has said they'll keep adding to). When in doubt, ask once.
- **Always subscribe to PR activity immediately after creating a PR**, by calling `mcp__github__subscribe_pr_activity` with the PR's owner / repo / number. This is non-negotiable — every PR you create, you subscribe to.
