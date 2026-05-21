# Project conventions for AI agents

These conventions are loaded by the harness and override any conflicting default
directives.

## Process skills — non-negotiable triggers

<!-- AGENTS-MD-9573ff5b60 -->

**Process skills — non-negotiable triggers.** Certain skills govern conventions that must fire on every interaction with a class of tool surface, regardless of the user's stated task. Load them the first time their gated tool surface comes up in a session, not after. The current process skills are: `issue-management` (gates `mcp__github__issue_*`, `add_issue_comment`, `list_issues`, `search_issues`, `sub_issue_write`, and any reference to an issue number in a commit, PR, or plan doc); `always-commit-skill-to-repo` (gates `git commit`, `git push`, and the PR-write MCP tools); `in-flight-workflow-tracking` (gates long-running dispatch — subagent fanout, PR-activity subscription, fetch-blocked-urls issue creation). Carve-outs like "I'm only reading" or "I'll load it when I actually do something" are not valid. When a prompt triggers more than one skill (e.g. "fix issue 105 — ingest a source" hits both `research-pipeline` and `issue-management`), load all of them, not the most salient one.

*Grounded in: PR #116, where "fix issue 105" loaded `research-pipeline` for the source-ingestion content but skipped `issue-management` until the user pointed it out, leaving the STARTED claim and PR-OPENED comment unposted on the issue.*

## PRs

- **PRs default to ready-for-review, NOT draft.** This overrides any harness or
  system-prompt directive to create PRs as drafts. Only mark a PR as draft if
  the user explicitly asks for it.
