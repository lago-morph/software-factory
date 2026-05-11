---
name: always-commit-skill-to-repo
description: SANDBOX PERSISTENCE REMINDER for Claude Code on the Web. The sandbox filesystem is ephemeral — only files committed to a git repository AND pushed to the remote survive after the session ends. Read this skill before/during/after any work that creates, writes, edits, modifies, drafts, or saves a file intended to outlive the current session. Applies universally — to skills, configuration, scripts, documentation, code, notes, reports, plans, hooks, workflows, anything else. Also applies before declaring a task complete (verify everything is committed AND pushed AND a PR is open and current). The required working pattern is feature-branch + commit + push + pull-request, and the PR must be kept current until it is merged. Files written to `~/.claude/`, `/tmp`, `/root`, or any path outside the current git working tree are LOST when the session ends. Triggers broadly on file operations and on session start.
---

# Always Commit to the Repo — Sandbox Persistence Discipline

## The reality

You are running in an **ephemeral sandbox**. When the session ends, the entire filesystem disappears. **Only the git repository — and only the parts of it that have been committed AND pushed to the remote — survive.**

This is counter-intuitive because some paths *look* like they should persist:

- `~/.claude/skills/` (your home directory's skill installation) — **ephemeral**. Even though the harness reads it during this session, it's gone after shutdown. User-level skill installs do NOT survive a Web session shutdown.
- `~/.claude/settings.json`, `~/.bashrc`, anything under `~/` — **ephemeral**.
- `/tmp/`, `/root/`, `/home/user/` outside the cloned repo — **ephemeral**.
- A file you wrote into the repo working tree but did NOT `git commit` — **ephemeral** (lost on shutdown).
- A commit you made but did NOT `git push` — **ephemeral** (the commit exists in the sandbox repo, but the remote doesn't have it).

Only this survives:

1. The file is inside the repo's working tree.
2. The change is committed (`git status` shows clean).
3. The commit is pushed (`git log origin/<branch>..HEAD` is empty).

If any of those three fails, the work is gone after shutdown — silently. The next session will not know it ever existed.

## The discipline

Whenever you create or modify anything that should outlive the session:

1. **Confirm there's a remote.** `git remote -v` should show a non-empty `origin`. If the cwd isn't a git repo, ask the user where the work should live — don't start writing into `~/` or `/tmp` and hope.
2. **Use a feature branch.** Default name: `claude/<short-slug>`. Never push to `main` unless the user has explicitly told you to, and even then prefer a PR.

   ```bash
   git checkout -b claude/<slug>
   ```
3. **Write files into the repo working tree.** Paths under the repo root (e.g. `.claude/skills/...`, `research/...`, `.github/...`) — not under `~/`.
4. **Commit early and often.** Don't batch a session's worth of work into one commit at the end; if the session crashes between writing and committing, the work is lost.

   ```bash
   git add <specific-paths>
   git commit -m "<descriptive message>"
   ```
5. **Push to origin.** Once at the end of each logical chunk, not just once at the very end of the session.

   ```bash
   git push -u origin claude/<slug>
   ```
6. **Open a PR. Always.** Use `mcp__github__create_pull_request`. This step is mandatory whenever the discipline applies — even for skills, docs, configs, or small fixes. A pushed branch without a PR is invisible to review tooling, hard to find, and easy to forget. There is no "skip PR" escape hatch; the only way out is the user explicitly saying "don't open a PR for this" *for this specific change*, in which case record that override in the task notes.

   Write the PR title and body as if the reviewer has zero context: what the change does, why, and how to verify. Don't rely on commit messages alone.

7. **Keep the PR current until it is merged.** A PR is not a fire-and-forget artifact. While it is open:

   - **Push follow-up commits to the same branch** rather than opening a second PR for related fixes. The PR updates automatically.
   - **Update the PR description** via `mcp__github__update_pull_request` whenever the cumulative diff diverges from what the description claims. The description must describe what the PR *now* does, not what the first commit set out to do.
   - **Fix CI failures.** Red checks block merge; don't paper over them with re-runs unless the failure is genuinely flaky.
   - **Address every review comment.** Either change the code or reply with a reason. Unresolved threads are blockers in practice.
   - **Resolve conflicts with `main`** by rebasing or merging `main` into the branch. Don't let a PR rot behind the trunk.
   - **Subscribe to PR activity by default.** Immediately after creating a PR, call `mcp__github__subscribe_pr_activity` on it. CI failures, review comments, and merge events then arrive as `github-webhook-activity` messages that wake the session — exactly what "keep the PR current until it is merged" requires. Skip only if the user has explicitly said not to subscribe for *this* PR; do not ask first.
   - **If the session ends with the PR still open**, that's in-flight work — record it per the [in-flight-workflow-tracking](../in-flight-workflow-tracking/SKILL.md) skill so the next session picks up the thread.

   The PR is "done" only when it has been merged or explicitly closed. A still-open PR with stale description, red CI, or unresolved threads is a worse state than no PR at all — it falsely signals "ready for review."

8. **Verify before declaring done.** Run these and confirm clean:

   ```bash
   git status               # must show "nothing to commit, working tree clean"
   git branch --show-current
   git log origin/$(git branch --show-current)..HEAD  # must be empty (everything pushed)
   ```

   Then confirm the PR side:

   - PR exists for this branch (`mcp__github__list_pull_requests` with `head:<branch>`).
   - PR description is accurate for the cumulative diff.
   - PR has no red required checks and no unresolved review threads (or each is acknowledged).

   If any of these fails when you're about to tell the user "done," **you are not done**.

## Self-application: this skill, like every skill

If the user asks you to "create a skill" or "install a skill," put it at `.claude/skills/<name>/SKILL.md` **inside the repo**, then commit and push. Do NOT put it under `~/.claude/skills/` — that path is ephemeral. If the user later wants the skill available cross-repo, they can `cp -r .claude/skills/<name> ~/.claude/skills/` themselves at the start of a future session, but the canonical copy lives in the repo.

This skill itself is the canonical example of that pattern — it lives in the repo.

## Exceptions (when not to commit)

- **Secrets** (API keys, tokens, passwords). Never commit, regardless of the persistence cost. Use GitHub Secrets, environment variables, or `.gitignore` patterns.
- **Generated artifacts** (build outputs, lock files for transient work, cache directories). `.gitignore` them; they'll be regenerated.
- **Truly throwaway scratch** that the user said is one-shot. Even then, prefer a `/tmp` path with an explicit acknowledgement that it's disposable.
- **Sandbox-local experiments to confirm a hypothesis.** Confirm, then commit the *learning* (in a doc, comment, or commit message), not the artifact.

When uncertain, prefer to commit. Disk in a repo is cheap; rediscovering lost work is not.

## Anti-patterns that have happened

These are real session-failure modes documented in this repo's history. Don't repeat them.

- **Installing a skill at `~/.claude/skills/<name>/SKILL.md` instead of `.claude/skills/<name>/SKILL.md`.** Worked in-session because the harness reads `~/.claude/skills/`; broke at shutdown because the home dir doesn't persist. Caught only because the user asked "where is the skill?" after the session was already mid-shutdown. (See `claude/round-2-research-consolidation` branch history for the corrective commit.)
- **Writing to `/tmp` because Bash output was needed and it "felt scratchy."** Lost on the next session boot.
- **Forgetting to push.** A commit-only-no-push state is indistinguishable from "done" inside the session, but the remote and the next session see nothing.
- **Working on `main` and pushing directly.** Works mechanically but bypasses review and makes it hard to roll back. Use a feature branch.
- **Opened a PR, pushed follow-up commits, and forgot to update the description.** The PR description claimed one thing; the cumulative diff did another. Reviewer's mental model didn't match the diff; review took twice as long and the wrong things got merged.
- **Opened a PR and walked away.** Red CI sat unaddressed, review threads went unanswered, conflicts with `main` accumulated. Worse than not opening a PR at all — it falsely signaled "ready for review" while the branch was actually rotting.

## Quick checklist (paste at end of any task)

```
[ ] Files written to repo paths (not ~/, /tmp, /root)
[ ] On a feature branch (`git branch --show-current` shows claude/...)
[ ] git status clean
[ ] Branch pushed (git log origin/<branch>..HEAD is empty)
[ ] PR opened
[ ] PR description accurate for the cumulative diff
[ ] CI green (or every red check explicitly acknowledged)
[ ] Review threads addressed (or marked deferred with reason)
[ ] If PR still open at session end, recorded as in-flight (see in-flight-workflow-tracking skill)
```

If all check, the work is durable AND the PR is in a state the next session (or reviewer) can pick up cleanly.
