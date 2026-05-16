# AGENTS.md suggestions — 2026-05-16-64

These are proposed additions to the project's agents file (typically `AGENTS.md` at the repo root). Each section contains:

1. **Proposed addition** — the exact text to paste.
2. **Why this earns its place in your agents file** — the argument for doing it, grounded in something that happened (or nearly happened).

Decide each on its own merits. Skip ones that don't apply to your operating posture; copy-paste the ones that do.

---

## Suggestion 1: Do not poll for subagent or webhook completion with bash sleep loops

### Proposed addition

> **Wait, don't poll.** When waiting for an asynchronous subagent, CI run, or PR webhook to complete, trust the harness's notification system — `<task-notification>` arrives when a subagent finishes; `<github-webhook-activity>` arrives when a PR event fires. Never write `until <condition>; do sleep N; done` loops to wait for these events. If you need a one-shot "tell me when X is ready" signal, use `Bash` with `run_in_background: true` and a command that exits when the condition is true — but for events that arrive on their own schedule (subagents, webhooks), just stop emitting and wait.
>
> *Grounded in: PR #61's index pass, where I started a `until` polling loop "while waiting for the last background subagent." It served no purpose — the agent's completion notification was going to arrive regardless.*

### Why this earns its place in your agents file

The polling loop costs you twice. First, it consumes context budget — every check of `wc -l` round-trips through the Bash tool. Second and worse, when killed mid-flight, the loop's `sleep` child re-parents to init and continues running silently — the user noticed PID 28424 still alive minutes after I thought I'd killed it. The cost of NOT having this rule is the orphan-sleep gotcha plus an indeterminate amount of wasted context budget; the marginal cost of adopting it is zero (the harness handles waiting for you). Asymmetric — adopt.

---

## Suggestion 2: `kill %N` doesn't work across Bash tool calls — use real PIDs

### Proposed addition

> **For cross-call process control, use real PIDs, never job-table shorthand.** Each invocation of the `Bash` tool spawns a fresh shell, so `kill %1` in call B never resolves to a job started in call A (the new shell has an empty job table). When you start a long-running or background process, capture its PID at start (`echo "started $!"`) or look it up later with `ps -ef | grep <distinctive>`, then `kill <PID>`. Also: after killing the parent shell, check for orphaned child processes (a `bash | sleep` pipeline will leave the `sleep` reparented to init if you kill only the bash).
>
> *Grounded in: PR #61's polling-loop cleanup, where my `kill %1` silently failed because the original shell was already gone, and an orphan `sleep 5` (PID 28424) survived under init until the user noticed it.*

### Why this earns its place in your agents file

This is one of those gotchas that's invisible until it bites — `kill %1` produces no error and looks like it worked, but the process keeps running. The marginal cost of adopting the rule is one extra `ps` line or one `echo $!` at process start; the cost of NOT adopting it is leaked processes that show up only when the user happens to run `ps` themselves. Defensive trumps clever.

---

## Suggestion 3: Scripts that support one skill live under that skill's directory

### Proposed addition

> **Skill-specific scripts live under `.claude/skills/<skill>/scripts/`, not at top-level `scripts/`.** If you write a helper script whose sole purpose is to support one skill's workflow (e.g. an MHTML extractor for `research-pipeline`, an ADR-link checker for `adr`), put it inside that skill's directory from the first commit. Reserve top-level `scripts/` for repo-wide tooling that any skill (or no skill) could call.
>
> *Grounded in: PR #61 created `scripts/mhtml_extract.py`; PR #64 immediately moved it to `.claude/skills/research-pipeline/scripts/mhtml_extract.py` because it's purpose-built for one skill. Two commits where one would have sufficed.*

### Why this earns its place in your agents file

This is a placement convention with quiet value: skills become self-contained (you can copy `.claude/skills/<skill>/` to another repo and it works), and the top-level `scripts/` directory doesn't accumulate orphans whose meaning depends on context the reader doesn't have. The marginal cost is one extra `mkdir -p` at script-creation time. The cost of NOT adopting it is what just happened: PR #64 existed only to fix a placement decision that should have been right the first time.

---

## Suggestion 4: Audit the filesystem after a subagent cohort returns

### Proposed addition

> **After a parallel subagent cohort returns, audit the filesystem against their claims.** Subagents that delete, rename, or convert files will sometimes report a disposition they didn't execute — claim "skip — already covered" but leave the file in place, claim "kept as txt" for a file that was actually converted from mhtml, etc. Always: after collecting outputs, run a quick `ls` / `find` matching the expected post-state, count by category, and manually fix discrepancies before assembling the final artifact.
>
> *Grounded in: PR #61's 21-subagent fan-out — three duplicates were flagged "skip" but not actually deleted; one batch's textual "Action taken" field said "passthrough" for files it had actually converted (filesystem state was correct, prose was wrong).*

### Why this earns its place in your agents file

Subagent self-reporting drifts from reality more often than you'd expect — especially for conditional steps ("if previously processed, rm; else convert"). Without a filesystem audit, you propagate the drift into whatever artifact consumes the subagent reports. Cost of adoption: one `ls` and a per-category count, ~30 seconds. Cost of skipping: subtly wrong artifacts that you may not catch until the next session reviews them.

---

## Suggestion 5: Stop-hook compliance via WIP commits is acceptable mid-task

### Proposed addition

> **A mid-task forced commit may be a WIP commit — that's fine.** When the stop-hook fires demanding you commit before ending your turn, but the task is genuinely incomplete (e.g. you're waiting for a long-running subagent), commit the current state with a clear "WIP" subject line and a body noting what's pending. Push the WIP commit. Continue the task. The final commit can amend or supersede the WIP commit's content; both will be reachable in the PR's commit history. Do NOT abandon work or force a premature wrap-up to satisfy the hook.
>
> *Grounded in: PR #61, where the stop-hook fired ~15 minutes into the indexing pass with one subagent still running. WIP commit + push + continue worked cleanly.*

### Why this earns its place in your agents file

The stop-hook exists to ensure no uncommitted work is lost; it doesn't dictate that the commit must be final. Treating it as "must be done now" pressures agents into prematurely closing tasks. The WIP-commit pattern resolves the tension: durability requirement is met (work is in git, on the remote), and the task continues. Cost of adoption: one extra commit per long task; cost of skipping: either lost work or rushed half-finished outputs.

---

## Suggestion 6: Test-merge main before promoting a long-running PR

### Proposed addition

> **Before promoting a long-running PR from draft to ready-for-review, merge `origin/main` into your branch.** This catches the case where main moved while your branch was open (often the case for sessions that span multiple PRs). For shared files like `PLAN.md` / `INDEX.md` that you may not have touched, verify your branch is innocent with `git log <merge-base>..HEAD -- <file>` — if the output is empty, your branch never modified the file and the merge will take main's version cleanly, no conflict. Push the merge before flipping the PR ready-for-review.
>
> *Grounded in: PR #61, where the user asked for a test-merge of main to bring in PLAN.md v0.13. The branch had never modified PLAN.md, so the merge was clean and main's version replaced ours without conflict.*

### Why this earns its place in your agents file

PRs that linger more than an hour in a fast-moving repo accumulate "ghost conflicts" against `main` — files the reviewer expects to see at main's current version. The pre-flight check (one git log call) tells you whether your branch is safe; the merge (one git merge call) brings everything current. Cost: ~10 seconds. Cost of skipping: PR reviewer sees stale versions of shared files and wonders if you intentionally regressed them.

---

## Suggestion 7: Cohort subagent dispatch uses a shared on-disk brief, not inlined instructions

### Proposed addition

> **When dispatching ≥3 subagents that need the same instructions, write the instructions once to a brief file on disk (`<workspace>/.subagent-brief.md` is a good convention) and have each subagent `Read` it as the first step. Per-agent prompts then contain only the agent-specific scope** (file list, cluster-specific hints, output expectations). Inline-duplicating a long brief across N subagent prompts wastes ~N× the tokens of the brief and makes the prompts hard to evolve.
>
> *Grounded in: PR #61's 21-subagent fan-out used a 100-line shared brief at `research/manual/.subagent-brief.md`. Each per-agent prompt was ~10 lines (file list + cluster context); without the shared brief, each prompt would have ballooned to ~110 lines × 21 = ~2300 lines of duplicated instructions.*

### Why this earns its place in your agents file

The shared-brief pattern is a token economy and a maintainability win. If the brief evolves mid-fan-out (e.g. you spot a corner case after dispatching the first wave), all subagents still in flight pick up the change on their next Read. The cost of adoption is one `Write` call before dispatch and a 1-line "Read the brief" in each per-agent prompt. The cost of skipping it scales linearly with cohort size and quadratically with prompt revisions.

---

## Suggestion 8: When the user enumerates a list, count the items before responding

### Proposed addition

> **When a user lists numbered items (1, 2, 3, …), count them before paraphrasing or acting on them.** Off-by-one numbering errors are common in dictation and rapid prose — duplicated numbers (5, 5), skipped numbers (3, 5), or a stated count that disagrees with the actual count. Surface the count discrepancy back to the user as a clarification, not silently. The act of counting also forces you to enumerate the items in your own response, which catches comprehension gaps early.
>
> *Grounded in: in PR #61's intake, the user listed "6 areas" but actually wrote seven (the enumeration had two items numbered "5"). Counting them produced a clean renumbering proposal the user accepted in one round.*

### Why this earns its place in your agents file

Cost of adoption: a single mental count + one sentence in your reply ("you wrote 7 items, not 6 — here they are renumbered"). Cost of skipping: silent fabrications of the form "Theme 5 (Theme 5 from your list)" that propagate through downstream artifacts. The user is grateful to be told they miscounted; nobody is grateful to discover a propagated off-by-one weeks later.
