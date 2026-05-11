---
name: always-commit-skill-to-repo
description: SANDBOX PERSISTENCE REMINDER for Claude Code on the Web. The sandbox filesystem is ephemeral — only files committed to a git repository AND pushed to the remote survive after the session ends. Read this skill before/during/after any work that creates, writes, edits, modifies, drafts, or saves a file intended to outlive the current session. Applies universally — to skills, configuration, scripts, documentation, code, notes, reports, plans, hooks, workflows, anything else. Also applies before declaring a task complete (verify everything is committed AND pushed). The default working pattern is feature-branch + commit + push + pull-request. Files written to `~/.claude/`, `/tmp`, `/root`, or any path outside the current git working tree are LOST when the session ends. Triggers broadly on file operations and on session start.
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
6. **Open a PR at the end.** Use `mcp__github__create_pull_request`. The user can review and merge. If the user has explicitly said "no PR needed," skip this step — but ask if unsure.
7. **Verify before declaring done.** Run these three and confirm clean:

   ```bash
   git status               # must show "nothing to commit, working tree clean"
   git branch --show-current
   git log origin/$(git branch --show-current)..HEAD  # must be empty (everything pushed)
   ```

   If any of these is non-empty when you're about to tell the user "done," **you are not done**.

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

## Quick checklist (paste at end of any task)

```
[ ] Files written to repo paths (not ~/, /tmp, /root)
[ ] On a feature branch (`git branch --show-current` shows claude/...)
[ ] git status clean
[ ] Branch pushed (git log origin/<branch>..HEAD is empty)
[ ] PR opened (or user said skip PR)
```

If all five check, the work is durable.
