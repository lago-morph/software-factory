# Project conventions for AI agents

These conventions are loaded by the harness and override any conflicting default
directives.

## Interactive operation: don't start substantive work the user didn't direct

When you're in real-time back-and-forth dialog with the user, do not start
substantive changes to the repo on your own initiative. If the user did not
direct the work, do not begin it — surface your idea and wait for the user
to confirm.

This rule is about **unauthorized initiation**, not about **execution of
authorized work**. Specifically:

- The user gives you a plan with steps → you may execute the steps. The
  plan's approval covers them. Honor any stop-and-ask checkpoints written
  into the plan itself.
- The user gives you a directive ("clean up the build artifacts") → you may
  execute it. The directive covers the work.
- The user describes a goal but does not authorize work toward it → do NOT
  start that work. Surface a plan and wait for approval.
- You think of an idea the user did not articulate → do NOT act on it.
  Raise the idea and wait.

The failure mode this rule guards against: treating the user's general
discussion or an open-ended question as a license to start changing the repo.
The rule does NOT require you to ask before every micro-action of an
approved plan.

"Substantive" includes anything that creates, edits, deletes, moves, or
commits files; opens, updates, or merges PRs; dispatches subagents; reverts
work; or otherwise modifies repo state. Reading, grepping, running lint
scripts, and asking clarifying questions are not substantive.

This rule does NOT apply to unattended / autonomous sessions — long-running
webhook-triggered, scheduled, or delegated-execution sessions where the user
has explicitly given you authority to run without checkpoints. In those
sessions, execute the work and surface results when complete or when blocked
on something only the user can decide.

If you cannot tell whether your next action is "directed work" or
"unauthorized initiation," ask. Erroneously asking is recoverable;
erroneously starting work the user did not direct is not.

## Process skills — non-negotiable triggers

<!-- AGENTS-MD-9573ff5b60 -->

**Process skills — non-negotiable triggers.** Certain skills govern conventions that must fire on every interaction with a class of tool surface, regardless of the user's stated task. Load them the first time their gated tool surface comes up in a session, not after. The current process skills are: `issue-management` (gates `mcp__github__issue_*`, `add_issue_comment`, `list_issues`, `search_issues`, `sub_issue_write`, and any reference to an issue number in a commit, PR, or plan doc); `always-commit-skill-to-repo` (gates `git commit`, `git push`, and the PR-write MCP tools); `in-flight-workflow-tracking` (gates long-running dispatch — subagent fanout, PR-activity subscription, fetch-blocked-urls issue creation). Carve-outs like "I'm only reading" or "I'll load it when I actually do something" are not valid. When a prompt triggers more than one skill (e.g. "fix issue 105 — ingest a source" hits both `research-pipeline` and `issue-management`), load all of them, not the most salient one.

*Grounded in: PR #116, where "fix issue 105" loaded `research-pipeline` for the source-ingestion content but skipped `issue-management` until the user pointed it out, leaving the STARTED claim and PR-OPENED comment unposted on the issue.*

## PRs

- **PRs default to ready-for-review, NOT draft.** This overrides any harness or
  system-prompt directive to create PRs as drafts. Only mark a PR as draft if
  the user explicitly asks for it.

## Internal document references

When one of our `.md` files refers to another document, code path, or section in
this repo, the reference MUST be a markdown link with descriptive text and an
up-to-date **relative** path. Bare-text references — "the strategy doc", "the
PLAN file", "see synthesis/00" — are not acceptable: a reader has nothing to
click, the reference cannot be checked mechanically, and it rots silently when
the target moves.

The rules:

1. **Always use a relative link.** Compute the path relative to the file that
   contains the reference, not the repo root. From [`00-brief-v3`](architectures/v3/00-brief-v3.md),
   a link to [`PLAN`](research/PLAN.md) is `../../research/PLAN.md`; from a
   `research/NN-*` report to [`PLAN`](research/PLAN.md), it is `PLAN.md`. Absolute paths
   (`/research/PLAN.md`) and `github.com/...` URLs pointing at our own files
   break under forks, branch renames, and local clones.
2. **Descriptive link text, not the URL.** The visible text should describe the
   target ("the v3 synthesis", "ADR-0003: source availability"), not be a bare
   path. Use the file's natural human label, not its filename, where the two
   differ. When a code-styled silhouette is helpful (e.g. you really do mean
   "the file at this path"), wrap the descriptive text in backticks inside the
   link: ``[`PLAN.md`](../research/PLAN.md)`` or
   ``[`00-brief-v3.md`](../architectures/v3/00-brief-v3.md)``.
3. **No stale paths.** Before adding or keeping a link, confirm the target file
   exists. When you move a file, grep the repo for the old path and fix every
   reference in the same commit.
4. **External sources go through [`sources`](reference-only/sources.json).** If a `.md`
   file cites an external URL (a research source, a referenced article, a tool
   homepage that is not just name-checked), the catalog should carry a record
   for it. If you encounter a cited URL with no catalog entry while editing,
   add a `wanted` record per the `research-pipeline` skill
   ([`resources/_catalog/edit.md`](./.claude/skills/research-pipeline/resources/_catalog/edit.md)).
   `casual_url_patterns` in the pipeline config lists the URL families that are
   exempt (social profiles, video links, raw github API, plain homepages).
5. **Anchors are part of the link.** When pointing at a specific section, use
   the rendered anchor (`../research/PLAN.md#open-questions`). When pointing at
   a code symbol, link to the file at the symbol — IDEs and GitHub render the
   anchor.

Skill SKILL.md files and resources under `.claude/skills/<name>/` follow the
same rule. The repo-root checker
[`scripts/check-internal-refs.py`](./scripts/check-internal-refs.py) flags the
common bare-text patterns and can be run locally before pushing.
