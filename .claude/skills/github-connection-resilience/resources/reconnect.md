# Reconnect — connectivity restored mid-recovery

**Load this file only if a `mcp__github__get_me` call succeeds *after*
you have already entered the recovery procedure in `resources/recovery.md`.**
Do not preload it.

The case this addresses: the original failure was a **network drop**, not
a permanent auth loss. You committed everything in Phase 4, you may
even have produced a patch in Phase 6, and then in Phase 5 (the final
connectivity probe) the network came back. Now you can both finish the
push *and* salvage the patch artifacts.

Do not flip back to "business as usual." The session has been in
recovery; some artifacts were authored on the assumption you would not
recover. Those artifacts need to be cleaned up before resuming, or they
will rot in the repo.

---

## Phase R1 — Confirm connectivity is real and not a flicker

1. Call `mcp__github__get_me` **twice**, 10 seconds apart. Both must
   succeed.
2. Try one read call that exercises the repo, e.g.
   `mcp__github__list_branches` for the working repo. It must succeed.
3. If any of these flake or fail, **abandon reconnect** and return to
   `resources/recovery.md` Phase 6. Treat the apparent restore as a
   false positive — better to ship a patch the user doesn't need than
   to assume connectivity you don't have.

Only proceed past R1 if all three probes returned cleanly.

---

## Phase R2 — Push the work

Push every committed-but-unpushed thing.

```bash
git status                                       # confirm tree is clean (Phase 4 should have left it that way)
git log origin/$(git branch --show-current)..HEAD --oneline
# ^^ inspect; this is what you're about to ship to the remote
git push -u origin $(git branch --show-current)
```

If the push fails with a network error, retry up to 4 times with
exponential backoff (2s, 4s, 8s, 16s). If it fails with an auth error,
the apparent restore was a lie — return to recovery Phase 6.

After a successful push:

```bash
git log origin/$(git branch --show-current)..HEAD --oneline
# ^^ must be empty now
```

If anything is still listed, push again with explicit refspec
(`git push -u origin HEAD:<branch>`) and re-verify.

---

## Phase R3 — Delete the patch artifacts

The patch archive and instructions were a fallback for the case where
the user would have to recover from outside the session. The user does
not have to do that anymore. Leaving the artifacts in place would:

- Mislead a future session into thinking the work was *not* recovered.
- Pollute the repo root with `RECOVERY-INSTRUCTIONS.md` and a stale
  patch reference.
- Risk an inconsistent state if the user does apply the patch
  unnecessarily.

Delete them. Specifically:

1. **Local patch tarball.** Remove from `/tmp`:
   ```bash
   rm -f /tmp/recovery-*.tar.gz
   rm -rf /tmp/recovery-patch
   ```
   (Sandbox cleanup will eat these anyway; remove them now for clarity.)
2. **`RECOVERY-INSTRUCTIONS.md` at the repo root.** Delete and commit
   the deletion:
   ```bash
   git rm RECOVERY-INSTRUCTIONS.md
   git commit -m "Reconnect: drop recovery-instructions after successful push"
   ```
3. **Any "patch produced" marker** you may have committed. Search the
   recovery commit for references and remove them via a follow-up commit
   if they're awkward. **Do not** rewrite history (no rebase, no amend);
   the recovery commits are part of the audit trail.

Do **not** delete:
- `restart-instructions.md` — it's still useful as the handoff for the
  next session, see R4.
- The retrospective file — keep it; it captured real session learnings.

Push the cleanup commits:

```bash
git push origin $(git branch --show-current)
```

If you have not yet surfaced the patch file via `SendUserFile` (e.g.
the reconnect happened *before* Phase 6d), skip that step entirely.
If you already did `SendUserFile` and the user has the patch on their
device, tell them in your final message that they should ignore /
discard it — the work has been pushed.

---

## Phase R4 — Follow the restart-instructions to resume

The restart-instructions file you wrote in recovery Phase 2 is exactly
the document a fresh agent would have used to pick up the work. **Use
it the same way now**, just inside the same session.

1. Re-read `restart-instructions.md` end-to-end. Treat it as
   authoritative for "what was I doing?" — the file is now more
   reliable than your in-context memory, which has been through the
   recovery procedure.
2. Recover the **"What I was in the middle of when I stopped"** section
   into your working plan. That is your resume point.
3. Re-engage subagents only after confirming you are in a clean state.
   If subagents were drained in recovery Phase 1, do not silently
   re-dispatch them — explicitly note to the user that you are
   continuing X subagent task because the original drained-with-partial-result.

Once you have resumed, the rest of the session proceeds normally, with
two carry-over rules:

- **Increase commit-and-push cadence.** The session has demonstrated
  network fragility. Commit and push after every checkpoint without
  exception. Do not extend the 20-minute wall-clock window.
- **Run the SKILL.md auth check before every multi-step pass** for the
  remainder of the session, not just once. If a network drop happened
  once, it will likely happen again.

---

## Phase R5 — Update the PR (if one exists)

If the work is part of an open PR, the PR description should now reflect
that recovery commits exist on the branch. Append a short "Recovery
note" section to the PR body via `mcp__github__update_pull_request`:

```markdown
## Recovery note

This branch contains recovery commits (see `restart-instructions.md`
and `retrospective/<file>.md`) from a mid-session GitHub MCP
network drop. Work was preserved locally and pushed once connectivity
returned. No data was lost.
```

This is helpful for reviewers wondering why there are commits with
"Recovery:" in their messages.

If no PR exists yet (e.g. the session ended before the PR step), create
one normally per `always-commit-skill-to-repo`. The recovery commits
are part of the history; nothing special needs to be done.

---

## Phase R6 — Final report to the user

Send one chat message that:

1. **Confirms** the work was recovered without the user having to apply
   a patch.
2. **Lists** what was pushed (sha + message for each recovery commit;
   pointer to `restart-instructions.md` and the retrospective).
3. **Tells** the user to discard the patch archive if you already
   surfaced one.
4. **States** whether you are continuing the original task or stopping
   here for the user to confirm next steps.

Then either continue with the original work (re-run the auth check
first, per the elevated discipline above), or stop and wait, depending
on whether the user has indicated they want to keep going.

---

## Anti-patterns specific to reconnect

- **Skipping R1 (the double-probe).** Tempting because you "just saw"
  the network come back. Don't. The double-probe rules out a
  single-packet flicker.
- **Rebasing or amending the recovery commits out of existence.**
  They are evidence the session went through recovery. A future
  retro-coverage audit will look for them. Leave them.
- **Forgetting to delete `RECOVERY-INSTRUCTIONS.md`.** If left, a
  future session will read it, assume there is unpushed work, and try
  to apply a nonexistent patch.
- **Forgetting to push the cleanup commits.** The whole point is that
  the remote is now reachable. Push them.
- **Re-dispatching subagents on the assumption they "would have
  finished by now."** They were drained. Anything you didn't capture
  in Phase 1 is gone. Restart them explicitly if you need their work.

---

## Done state

Reconnect is complete when **all** of:

- Both R1 probes succeeded and the read call succeeded.
- `git log origin/<branch>..HEAD` is empty.
- `RECOVERY-INSTRUCTIONS.md` has been removed and the deletion committed
  and pushed.
- Any pre-emptively-sent recovery patch has been acknowledged to the
  user as discardable.
- The PR (if any) has a recovery note.
- A final report has gone to the user.
- You have either resumed work under elevated discipline or stopped at
  a clean checkpoint.
