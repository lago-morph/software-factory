---
name: in-flight-workflow-tracking
description: Track asynchronous work that won't complete during the current session, so a future session (or future you after a context compaction) can pick it up cleanly. Use whenever opening a GitHub issue that triggers a workflow, opening a PR awaiting CI, kicking off a long-running fetch/build/deploy, dispatching a subagent whose output won't return synchronously, or otherwise initiating work whose completion signal arrives later. Especially critical before any planned session shutdown — every piece of in-flight work that isn't explicitly tracked is silently lost. Triggers on phrases like "open an issue", "trigger the workflow", "dispatch", "kick off", "I'm going to shut down", "wrap up", "save state".
---

# In-Flight Workflow Tracking

## Why this matters

Sessions end. CI runs continue. Subagents finish minutes later. The session that started the async work is not the session that completes it — and the completing session has no memory of what's pending unless it's written down somewhere the repo persists.

Untracked in-flight work is the single most-common silent-failure mode in repo-based agent workflows. The work *appears* successful from inside the originating session (the issue is open, the workflow is running, the agent dispatched), and the failure shows up only when the next session ignores it because it doesn't know to look.

## When to invoke

Any time you have started something whose completion you won't see in this session. Examples:

- Opened a `[fetch-urls]` issue → the workflow runs in CI and comments later.
- Opened a PR → CI takes minutes; review takes hours.
- Triggered `workflow_dispatch` → background fetch/build/deploy in progress.
- Dispatched a long-running subagent → its report will land in the conversation after a delay.
- Asked the user a question whose answer changes the next step.
- Filed a fetch issue, then realized the source is also blocked by Wayback → queued a second fetch issue.

If you're about to end your turn or the user signals shutdown, **walk through everything you opened this session and confirm each is either tracked or already drained.**

## Where to record

Use the first match from this list that exists in the repo:

1. `research/PLAN.md` — if there's an active research plan, append to its "in-flight" section (see [research-pipeline](../research-pipeline/SKILL.md) for the conventions).
2. `IN-FLIGHT.md` at repo root — if there's no research-style PLAN.md but the project has long-running work.
3. The currently open PR's description — append a "## In-flight" section so reviewers can see what's still pending.
4. A new section in `CLAUDE.md` or `AGENTS.md` at repo root, titled "In-flight tracking."

Create the file if none exists. Don't write into the conversation thread alone — it doesn't persist.

## Per-item format

Every in-flight item gets this shape:

```markdown
### <category>: <short description>

- **Identifier:** issue #N / PR #M / commit <sha> / workflow run <id>
- **Opened:** <date> by <who/this-session>
- **Completion signal:** <what tells you it's done — e.g., "comment from github-actions[bot] on issue #N with merge instructions" / "PR check status all green" / "branch fetched/issue-N exists">
- **What it does when complete:** <concrete next action — e.g., "git fetch origin fetched/issue-N && git merge --no-ff" / "merge PR" / "pull from <branch> and run subagent 13">
- **Fallback if it fails:** <what to do if the completion never arrives or fails — e.g., "open Wayback-Machine retry issue with same URLs" / "close PR and reopen with simpler diff">
- **Expected wall time:** <rough — 1 min / 5 min / 1 hour / overnight>
- **Affects:** <which reports/files/branches depend on this completing>
```

If even one of those fields is unknown when you open the work, it's a sign you don't yet know enough to start. Fill in what you can; mark unknowns explicitly.

## Promotion: mandatory first action

When recording an in-flight item in a plan that has a "Next actions" or "How to resume" section, **promote drain-the-in-flight-work to the first numbered step**, with the word "MANDATORY" in the heading:

```markdown
#### Step 1 (MANDATORY FIRST ACTION) — Drain in-flight work

Before any other work, check these and process them:

- Issue #N — [fetch-urls] Tier 1 …
- PR #M — feature/foo …
- (etc.)
```

This is non-negotiable. A future agent reading the plan will follow it in order; if drain isn't first, they will skip past pending work and produce out-of-sync output.

## What to do when the session is about to end

Before signing off (e.g., the user says "shut down" / "wrap up" / "we'll continue later"), do this checklist:

1. **List everything you initiated this session.** Re-read your own turns. Look for `mcp__github__issue_write`, PR creations, branch pushes, `workflow_dispatch`, subagent invocations.
2. **For each, is it complete in-session?** If you've already seen the completion signal and acted on it, fine — it's not in-flight.
3. **For each remaining: record it.** Use the per-item format above.
4. **Commit the tracking file.** Per the [always-commit-skill-to-repo](../always-commit-skill-to-repo/SKILL.md) discipline — if the tracking isn't pushed, it doesn't exist for the next session.
5. **Tell the user what's tracked and where.** One sentence per item, plus the file path. They might be the one who picks it back up.

## What to do when starting a session

If `research/PLAN.md` has a "MANDATORY FIRST ACTION — Drain in-flight work" block, or if any of the tracking files mentioned above exist, **process them before any new work**. The session is otherwise likely to add to inconsistent state.

For each tracked item, follow its "What it does when complete" action. If the completion signal hasn't arrived yet:

- If the wall time estimate has passed, investigate (look at the workflow run logs, the PR status, the subagent transcript). Something may have failed silently.
- If the wall time is still active, leave the item tracked and start work that doesn't depend on it.

## Anti-patterns from this repo's history

- **Opened fetch issue #8 (Wayback supplements) before the session ended.** The plan was updated to mark it as the mandatory first action *only because the user explicitly asked* before shutdown. Without that prompt, the next session would have started fresh and the Wayback content would have rotted on an open issue.
- **Multiple workflow PRs (#5, #6, #7) in rapid sequence.** Each was "in flight" against `main` while subsequent fixes were being prepared. Without tracking, it was easy to lose which PR superseded which.
- **PR #3 was merged before PR #5's diagnostic refactor reached `main`.** The author thought the fix would be on `main` after the user said "merged" — but they had merged a different PR. Tracking which PR is current vs which is superseded would have caught this.

## Quick template (paste at end of any session that has in-flight work)

```markdown
## In-flight as of <date> (session ID: <short>)

### <one item per pending thing>

- Identifier: …
- Opened: …
- Completion signal: …
- What it does when complete: …
- Fallback if it fails: …
- Expected wall time: …
- Affects: …
```

If the section is empty after a session ends, all work was synchronous — that's fine, but rare for any non-trivial task.
