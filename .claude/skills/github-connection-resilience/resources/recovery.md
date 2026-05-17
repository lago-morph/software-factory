# Recovery — when re-auth has decisively failed

**Load this file only if `SKILL.md` Step 4 conditions are met.** Do not
preload it during routine auth checks. Its job is to drive a clean
shutdown that preserves every byte of work and gives the user a way to
recover the session contents from a different machine.

The recovery is a six-phase procedure. Do them in order. Do not skip
phases.

---

## Phase 1 — Stop work; drain subagents

The instant you enter recovery, stop spawning new work.

1. **Halt the main agent's current chain of tool calls.** Do not start
   the next planned step. Do not call any more `mcp__github__*` tools
   except `get_me` (used by the connectivity-restored probe in Phase 5).
2. **Drain in-flight subagents.** You cannot cancel running subagents in
   the Agent tool — they will return when they return. Do this:
   - Note in your working memory which subagents are in flight.
   - **Wait** for each one to return. (Use `Monitor` or just continue the
     loop you're already in; don't dispatch new ones.)
   - When a subagent returns, capture its output into the working tree
     so it survives Phase 4. Even a partial result is worth saving.
   - Do not dispatch follow-up subagents based on partial results. Just
     save what came back.
3. **Acknowledge to the user that you have entered recovery.** Short:

   > GitHub MCP auth could not be restored. I'm entering the recovery
   > procedure: stopping new work, draining in-flight subagents, writing
   > restart instructions, committing locally, and preparing a patch
   > file you can apply on your machine if I can't push.

   Then proceed without waiting for them to reply, unless they speak up.

---

## Phase 2 — Write `restart-instructions.md`

The next session will not see this session's conversation. Everything a
fresh agent needs to pick up has to live in the file.

Path: **`restart-instructions.md` at the repo root.**

Content skeleton:

```markdown
# Restart instructions — session interrupted by GitHub MCP auth loss

**Date (UTC):** <YYYY-MM-DD HH:MM, captured via `date -u`>
**Branch:** <current branch>
**Last good push (sha):** <git rev-parse origin/<branch>, if known>
**Local HEAD (sha):** <git rev-parse HEAD>
**Unpushed commits:** <count from `git log origin/<branch>..HEAD --oneline`>
**Uncommitted files at recovery time:** <list, or "none">

## What happened

A one-paragraph plain-English summary of the failure mode. State whether
this was an auth drop, a network drop the user couldn't repair, or
something else. Quote the exact error from the last failed
`mcp__github__get_me` call.

## What the original task was

Restate the user's original goal in 2-4 sentences. Do NOT paraphrase from
a half-remembered impression — pull it from the user's actual messages
where you can.

## What I had completed before stopping

A bulleted list of substantive progress. Each bullet should reference
specific files, commits, or subagent outputs by path/sha/name. A future
agent should be able to `git log` and `git diff` against these to verify.

## What I was in the middle of when I stopped

Be precise. "Halfway through implementing X" is not enough. State:
- The exact step in the plan I was on.
- The next concrete action that was queued.
- Any decisions that had already been made about how to do it.
- Any open questions that were unresolved at the moment of stop.

## Lessons learned during this session

Anything the next agent should know that isn't obvious from the code:
- Surprising behaviors of tools or APIs.
- Dead-end approaches I tried and rejected, with the reason.
- Conventions in this repo I had to discover.
- Useful sub-results from subagents.

## How to resume

Step-by-step instructions for the next session:

1. Verify auth: run the `github-connection-resilience` skill's auth
   check.
2. Check this branch out and verify HEAD matches `<sha>`.
3. Read this file and the retrospective at
   `retrospective/YYYY-MM-DD-PPP.md`.
4. Pick up at "<exact next action from above>".

## Context the user provided

Quote the user's original request verbatim, and any clarifying
instructions they gave during the session. A fresh agent has none of
that context otherwise.

## Files touched this session

A list of every file path created/modified, with one-line summaries.
Generate from `git diff --name-status origin/<branch>...HEAD` plus
`git status` for uncommitted changes.

## Subagent results captured

For each subagent that returned during this session, a short block:
- Subagent: <subagent_type / role>
- Dispatched at: <time>
- Returned at: <time>
- Output saved to: <path or "inline above">
- Status: completed / partial / errored
```

Fill in every section honestly. **Do not omit "What I was in the middle
of"** — that is the single most valuable section for a fresh agent.

Commit this file as part of Phase 4, not now.

---

## Phase 3 — Run the retrospective

Invoke the `self-retrospective` skill. Its output lives at
`retrospective/YYYY-MM-DD-PPP.md` and complements
`restart-instructions.md`:

- `restart-instructions.md` answers *"what should the next session do?"*
- The retrospective answers *"what did we learn that's worth keeping?"*

Both go into the repo. They reference each other:

- The retrospective should link to `restart-instructions.md` in its
  inline summary.
- `restart-instructions.md` should link to the retrospective in the
  "How to resume" section.

If the `self-retrospective` skill itself fails for any reason
(unavailable, too short to be meaningful, conflicts with the recovery
state), substitute a minimal `retrospective/YYYY-MM-DD-recovery.md`
with the rough structure: what was attempted, what worked, what
broke, what's next.

---

## Phase 4 — Commit everything locally

Commit the work the user did this session **plus** the recovery
artifacts (`restart-instructions.md` and the retrospective files).
Multiple commits is fine; one consolidated commit per logical chunk is
better than one giant commit.

```bash
git status                          # know what you're about to commit
git add restart-instructions.md
git add retrospective/<...>
git add <other paths from this session>
git commit -m "Recovery: capture session state after GitHub MCP auth loss"
```

Commit the user's work first (separately, with descriptive messages),
then the recovery artifacts as a final commit. That ordering keeps the
recovery artifacts at the tip and easy to find.

**Do not push yet.** Phase 5 will try.

---

## Phase 5 — Connectivity probe (one more try)

Before producing a patch file, give the network one more chance.

1. Call `mcp__github__get_me`.
2. If **success**: connectivity is back. **Load `resources/reconnect.md`
   and follow it.** Do not continue this file.
3. If **still failing**: connectivity is genuinely down. Proceed to
   Phase 6.

The probe is cheap. The patch-file path in Phase 6 is fine but it asks
the user to do manual work, so save them that step if you can.

---

## Phase 6 — Produce a patch file and surface it to the user

The goal: a single file the user can copy to a clean checkout of the
same repo and apply to recover **every commit and every uncommitted
file** from this session.

### 6a — Determine the base

The base is the latest commit known to be on the remote for this branch.
If `git rev-parse origin/<branch>` resolves, use that. Otherwise use the
fork point with `main` (`git merge-base HEAD origin/main`).

```bash
BASE=$(git rev-parse origin/$(git branch --show-current) 2>/dev/null \
       || git merge-base HEAD origin/main)
echo "Base: $BASE"
```

### 6b — Build the patch

A `git format-patch`-style series preserves commit metadata (author,
message, individual commit boundaries). A single `git diff` against the
base preserves the cumulative change but flattens history. **Prefer
`format-patch`**:

```bash
mkdir -p /tmp/recovery-patch
git format-patch "$BASE"..HEAD -o /tmp/recovery-patch
# That writes one file per commit, e.g. 0001-foo.patch, 0002-bar.patch.
```

Then bundle them plus any uncommitted-but-tracked files. If there *are*
uncommitted changes at this point (there shouldn't be after Phase 4,
but check):

```bash
git diff > /tmp/recovery-patch/uncommitted.diff
```

For untracked-but-needed files, stage and commit them first in Phase 4
rather than carrying them out as raw files. The patch series captures
all committed work.

Finally, package the patch directory into a single archive so it
surfaces as one file:

```bash
RECOVERY_FILE=/tmp/recovery-$(date -u +%Y%m%dT%H%M%SZ).tar.gz
tar czf "$RECOVERY_FILE" -C /tmp recovery-patch
echo "$RECOVERY_FILE"
```

### 6c — Write a `RECOVERY-INSTRUCTIONS.md` alongside the archive

Drop a short, copy-pasteable instructions file at the repo root so the
next session — or the user, reading the PR or the file directly — knows
what to do with the archive even without scrolling back through chat:

```markdown
# Recovery instructions

A GitHub MCP auth drop interrupted this session. All work is captured
in a patch archive that has been surfaced via the agent harness as a
downloadable file.

## To apply on your machine

1. Download the patch archive from the file message in this thread.
   It is named `recovery-<timestamp>.tar.gz`.
2. In a fresh checkout of this repo, on the branch
   `<current branch>` rebased onto the latest `origin/<branch>` (or
   `origin/main` if the branch isn't on the remote):
   ```bash
   cd <your-checkout>
   git checkout <current branch>     # or: git checkout -b <branch> origin/main
   tar xzf recovery-<timestamp>.tar.gz -C /tmp
   git am /tmp/recovery-patch/0*.patch
   # If there are uncommitted hunks:
   git apply /tmp/recovery-patch/uncommitted.diff
   ```
3. Inspect `git log` and `git status`; you should see the
   commits from the interrupted session.
4. Push to your fork or to origin:
   ```bash
   git push -u origin <branch>
   ```
5. Open the PR (or update the existing one). Reference
   `restart-instructions.md` and the retrospective so the next
   session can resume cleanly.

## To resume agent work after applying

Start a fresh session and tell it:

> Pick up the work described in `restart-instructions.md` on branch
> `<current branch>`. Begin with the auth check from the
> `github-connection-resilience` skill.
```

Commit `RECOVERY-INSTRUCTIONS.md` to the local repo too. (It can't be
pushed yet, but a future session that recovers the patch will get it as
part of the patch series.)

### 6d — Surface the file to the user

Use `SendUserFile` with status `proactive` so it lands on the user's
device even if they have stepped away. Caption it with the timestamp
and a one-line summary so they can identify it later.

```
SendUserFile({
  files: ["/tmp/recovery-<timestamp>.tar.gz"],
  caption: "Recovery patch for session interrupted by GitHub MCP auth loss. Apply per RECOVERY-INSTRUCTIONS.md in the repo.",
  status: "proactive"
})
```

### 6e — Final report to the user

End with a single chat message that:

1. **States plainly** that the session is being safely shut down due to
   auth loss.
2. **Reports what was preserved**: branch name, list of commits made
   (sha + message), files captured, retrospective path, restart
   instructions path.
3. **Tells them what they have to do**: download the patch archive
   (which is now in the message), follow `RECOVERY-INSTRUCTIONS.md`
   to apply on their machine, then start a fresh session pointed at
   `restart-instructions.md`.
4. **Acknowledges what they will need to redo**: nothing, if Phase 4
   worked. If anything was unsalvageable (e.g. a subagent timed out
   without returning), call it out explicitly.

Then stop. Do not try more `mcp__github__*` calls. Do not start new
work. The user is now driving recovery from their end.

---

## Anti-patterns specific to recovery

- **Trying to push during recovery as a "last attempt" before Phase 5.**
  If `get_me` is failing, a push will fail too, slowly. Skip directly
  to the structured probe.
- **Writing the patch only as a `git diff` against `main`.** Loses
  commit boundaries and authorship. Use `format-patch` unless there is
  exactly one commit to save.
- **Forgetting `SendUserFile`.** A patch sitting in `/tmp` is gone the
  moment the sandbox is reclaimed. The file *must* be surfaced via the
  harness or it might as well not exist.
- **Re-running the retrospective skill after Phase 3 because "more
  happened."** Once recovery starts, the session is on rails. The
  retrospective captured before Phase 4 is the canonical one.
- **Dispatching subagents to "help with recovery."** Recovery is
  serial, short, and deterministic. New subagents during recovery is a
  way to lose more work, not less.

---

## Done state

You are done with recovery when **all** of:

- `restart-instructions.md` is in the repo and committed.
- A retrospective file is in the repo and committed.
- All other session work is committed.
- A patch archive has been emitted *and* surfaced via `SendUserFile`.
- A final chat message has reported state and next steps to the user.
- No further `mcp__github__*` calls have been attempted after the
  Phase 5 probe.

If any of these is missing, the recovery is incomplete and you have
silently lost something. Verify each one before declaring done.
