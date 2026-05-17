---
name: github-connection-resilience
description: Survive GitHub MCP authentication drops and network blips in long sessions. Triggered (a) by the user typing "check auth", "sign in", "reauth", "verify github", "am I signed in", or similar; (b) automatically at the start of any multi-step pass (verify we can still commit and push before doing more work); (c) automatically when any `mcp__github__*` tool returns an auth or network error mid-session. The skill always tries a quick re-auth first; only if re-auth fails or times out does it load the recovery procedure from `resources/recovery.md` (stop main + drain subagents, write `restart-instructions.md`, run `self-retrospective`, commit locally, try push once more, otherwise emit a patch file and surface it to the user via `SendUserFile`). If connectivity returns mid-recovery, loads `resources/reconnect.md` (push everything, delete the patch file, follow the restart-instructions to resume). Also enforces a **commit-and-push-every-checkpoint** discipline so a drop never strands more than one checkpoint of work in the ephemeral sandbox.
---

# GitHub Connection Resilience

A long session is a network of small, fragile assumptions. The single most
common silent failure in Claude Code on the Web sessions that touch GitHub
is the MCP authentication going stale partway through — the agent keeps
working, then discovers at "push" time that everything done since the last
push is stranded in an ephemeral sandbox.

This skill exists to make that failure mode impossible to ignore and
cheap to recover from. It does three things:

1. **Check auth on demand and at every multi-step pass start** — so a stale token is caught at the boundary, not after another hour of work.
2. **Enforce a commit-and-push-every-checkpoint discipline** — so even an undetected drop costs at most one checkpoint of work.
3. **Drive a clean shutdown when re-auth fails** — capture restart context, retrospective, and a patch file the user can apply locally to recover.

The skill is split into three files so the main file stays small. Only load
the resource files when you actually need them:

- **`SKILL.md` (this file)** — triggers, auth check, frequent-commit discipline. Always loaded when the skill activates.
- **`resources/recovery.md`** — full degraded-state recovery. **Only load if re-auth has failed or timed out.**
- **`resources/reconnect.md`** — what to do if connectivity returns mid-recovery. **Only load if a `mcp__github__get_me` call succeeds after you have already entered recovery.**

---

## Trigger detection

### Direct triggers — activate immediately

The user typing **any** of these is an unambiguous request to run the
auth-check flow below:

- "check auth" / "check authentication" / "check github auth"
- "sign in" / "log in" / "login"
- "reauth" / "re-auth" / "re-authenticate"
- "am I signed in?" / "am I authenticated?" / "verify github"
- "is github working?" / "is the mcp working?"

For the literal verbs **"sign in"**, **"log in"**, **"reauth"**, treat the
intent as: *check state first; if state is bad, trigger authentication*.
For passive verbs ("check auth", "am I signed in?"), treat the intent as:
*report state; do not initiate authentication unless the user says so*.

### Implicit triggers — activate without being asked

- **Start of any multi-step pass.** Before you spawn subagents, before
  you start a chain of edits/commits intended to run for more than a few
  minutes, before you open a PR, run [the auth check](#the-auth-check)
  below. The cost is one tool call. The cost of skipping it is up to an
  hour of stranded work.
- **Any `mcp__github__*` tool returns an auth-shaped or network-shaped
  error mid-session.** Symptoms include: HTTP 401/403 from a GitHub MCP
  call, "Unauthorized", "Bad credentials", "token expired", "MCP server
  disconnected", repeated timeouts on a tool that worked five minutes ago.
  Stop the current chain of tool calls and run the auth check before
  anything else.
- **A subagent reports a GitHub MCP failure.** Treat the same as if the
  main agent had hit it. Do not dispatch more subagents until auth is
  verified.

### Non-triggers

- A single transient network blip on a non-GitHub tool (e.g. WebFetch).
  That's a different problem.
- A GitHub MCP call that returns a 404 or "not found." That's a real
  answer, not an auth failure.
- The user asking a question about *how* GitHub auth works in the
  abstract. Answer their question; don't run the check unless they ask.

---

## The auth check

This is the procedure to run on any direct or implicit trigger. It is
deliberately small and fast — three steps, no destructive operations.

### Step 1 — Probe with `get_me`

`mcp__github__get_me` is the canonical lightweight authenticated call.
It returns the authenticated user's identity or fails with an auth-shaped
error. Call it with no arguments. **Do this first, every time.**

Classify the result:

- **Success** — auth is live. Capture `login` and scopes if reported.
  Report state to the user and stop. Do not "refresh" working auth.
- **Auth-shaped failure** — 401/403, "Unauthorized", "Bad credentials",
  "token expired", "no authentication". Treat as stale auth. Go to Step 2.
- **Network-shaped failure** — timeout, connection reset, "MCP server
  disconnected", "transport closed". Treat as a transient drop. Wait
  briefly and **retry `get_me` up to 3 times with backoff (2s, 4s, 8s).**
  If all 3 retries fail, treat as stale auth and go to Step 2.
- **Ambiguous failure** — anything else. Treat as stale auth and go to
  Step 2. False positives are cheap; false negatives strand work.

### Step 2 — Try to re-authenticate

The Claude Code on the Web harness owns the OAuth flow for the GitHub
MCP server. The agent cannot complete the flow by itself; the user
must click through it in the harness UI. **Your job is to tell the
user what is wrong, what to do, and what state will be when they're
done.**

Emit a message that says, in plain language:

> The GitHub MCP authentication looks stale. The probe `get_me` failed
> with `<short error summary>`. Please re-authenticate the GitHub
> integration in the harness UI (typically: open the connections /
> integrations panel, find the GitHub MCP server, click "Reconnect" or
> "Re-authenticate"). When that's done, reply here and I'll re-verify.

Then **stop and wait.** Do not start more work. Do not dispatch
subagents. Do not retry on a loop — wait for the user to tell you they
have completed the re-auth.

If the user explicitly invoked one of the **passive** auth-check phrases
("check auth", "am I signed in?") rather than an **active** sign-in
phrase, you may instead just report the bad state and ask whether they
want to re-authenticate now or defer.

### Step 3 — Re-verify after user reports they re-authenticated

Once the user replies that they have re-authenticated:

1. Call `mcp__github__get_me` again.
2. **Success** → report identity, state "auth restored," and ask if you
   should resume the in-flight work (if any). If you are already inside
   the recovery procedure, **load `resources/reconnect.md`** and follow
   it.
3. **Failure** → tell the user re-auth did not take, show the new error,
   and ask them to try again. Track how many re-auth attempts have
   failed.

### Step 4 — Escalate to recovery only if re-auth has decisively failed

Decisive failure means **any one** of:

- The user has attempted re-auth and Step 3 still fails.
- The user has explicitly given up ("forget it", "I can't sign in",
  "just save what we have").
- A reasonable timeout has elapsed with no response from the user *and*
  there is committed-but-unpushed work that risks loss at session
  shutdown.

When any of these conditions hold, **load `resources/recovery.md`** and
follow it. Until then, do not load that file.

---

## Commit-and-push-every-checkpoint discipline

The auth check above limits how much work can be stranded by an
*undetected* drop. This section limits how much work can be stranded
by a drop the check missed.

### The rule

Every time you finish a logically self-contained unit of work, **commit
it and push it before starting the next one.** Do not batch a session's
worth of work into one commit at the end.

A "logically self-contained unit" is whichever of these applies first:

- A file (or small group of related files) is in a coherent state — not
  mid-edit, not with half-broken syntax, not with TODO placeholders that
  block the next step.
- A subagent has returned its output and you have merged it into the
  working tree.
- You have just completed a step in a multi-step plan.
- 20 minutes of wall-clock time have passed since the last push.
- You are about to dispatch one or more subagents.
- You are about to start a session-end activity (retrospective, PR,
  handoff).

When in doubt, commit and push. The cost of an extra commit is zero;
the cost of stranded work is hours.

### The mechanics

This is the same pattern the
[always-commit-skill-to-repo](../always-commit-skill-to-repo/SKILL.md)
skill enforces. Reuse it; don't reinvent.

```bash
git add <specific-paths>          # never `git add -A` without thinking
git commit -m "<descriptive>"     # WHY-focused message
git push -u origin <branch>       # always with -u on first push
```

If a push fails with a network error, retry up to 4 times with
exponential backoff (2s, 4s, 8s, 16s) per the repo's git-operations
guidance. If a push fails with an **auth-shaped** error, that is an
implicit trigger for this skill — stop and run [the auth check](#the-auth-check).

### Multi-step pass preamble (mandatory)

Before starting any multi-step pass (more than ~3 dependent steps, or
anything that will dispatch subagents):

1. `git status` — confirm clean or know exactly what's dirty.
2. `git branch --show-current` — confirm you're on the intended feature branch.
3. `git remote -v` — confirm origin exists and points where you think.
4. Run [the auth check](#the-auth-check) (Step 1).
5. If anything fails, fix or escalate before starting the pass.

This is cheap. Five tool calls. It is the single most effective
prophylactic against the failure mode this skill exists to address.

---

## Reporting state

When the user invokes a passive trigger ("check auth", "am I signed in?"),
report in this shape:

```
GitHub MCP auth: ✅ live
  - Identity: <login> (<name if available>)
  - Scopes: <scopes if reported by get_me>
  - Repo access: <repo from environment scope list>
  - Last successful call: just now (get_me)
Git working tree:
  - Branch: <branch>
  - Clean / N uncommitted files
  - Unpushed commits: <count>
```

If auth is bad:

```
GitHub MCP auth: ❌ stale
  - Probe: get_me → <error>
  - Last successful call: <if known>
  - Action: please re-authenticate in the harness UI, then say so here.
Git working tree:
  - Branch: <branch>
  - Clean / N uncommitted files
  - Unpushed commits: <count>     ← these are at risk if you can't re-auth
```

Always include the unpushed-commits line. It is the user's "how much do I
lose if this goes badly" indicator.

---

## What this skill does NOT do

- It does not authenticate by itself. Only the user can complete the
  OAuth flow in the harness UI.
- It does not loop-retry indefinitely. After re-auth fails decisively,
  it hands off to the recovery procedure and produces a portable artifact.
- It does not replace `always-commit-skill-to-repo`. That skill defines
  the broader commit/push/PR hygiene; this one specifically adds the
  resilience layer for GitHub MCP auth drops.
- It does not subscribe to PRs or follow CI. That is in-flight tracking;
  see [in-flight-workflow-tracking](../in-flight-workflow-tracking/SKILL.md).

---

## Quick checklist (run at any trigger)

```
[ ] Trigger classified (direct passive / direct active / implicit / subagent-reported)
[ ] mcp__github__get_me called
[ ] Result classified (success / auth / network / ambiguous)
[ ] If network: retried 3x with backoff
[ ] If success: reported state, stopped
[ ] If still failing: asked user to re-auth via harness UI
[ ] After user reports re-auth: re-ran get_me
[ ] If re-auth decisively failed: loaded resources/recovery.md
[ ] If commit-and-push discipline is overdue: caught up before continuing
```
