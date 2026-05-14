# AGENTS.md suggestions — 2026-05-14-03

These are proposed additions to the project's agents file (typically `AGENTS.md` at the repo root). Each section contains:

1. **Proposed addition** — the exact text to paste.
2. **Why this earns its place in your agents file** — the argument for doing it, grounded in something that happened (or nearly happened).

Decide each on its own merits. Skip ones that don't apply to your operating posture; copy-paste the ones that do.

---

## Suggestion 1: Verify counts via tool calls within the same edit

### Proposed addition

> **Verify numeric claims at write-time.** Every numeric claim that lands in a long-lived status doc — "N retrospectives," "M proposed ADRs," "K outstanding URLs," "S followups" — must be tool-verified within the same edit. Do not rely on recollection from earlier in the session. Use `ls | wc -l`, `grep -c`, or category-specific `awk` blocks immediately before writing the count, and note the verification command in the commit message body.
>
> *Grounded in: 5+ count drift bugs caught across three iteration passes on `research/PLAN.md` v0.10.*

### Why this earns its place in your agents file

In a single session updating PLAN.md, four separate count drift bugs were introduced in the first edit pass: "four retrospectives" (actual: five), "~9 skill specs" (actual: 13), "~36 AGENTS suggestions" (actual: 45), "~16 proposed ADRs" (actual: 26). Each was prevented by a 1-second `ls retrospective/` or `awk '/^## Part 4/{flag=1}...'` run *during* the edit. None would have been caught by re-reading the doc, because the wrong count looks right when you wrote it. They were only caught when iteration pass 2 ran verification commands the first pass had skipped.

The marginal cost of the rule: 1–2 extra tool calls per cumulative-total claim, plus one line in the commit message. The cost of not having it: every iteration pass becomes a verification pass, and the doc ships with wrong cumulative totals that the next session must catch.

---

## Suggestion 2: Re-read full document after multi-section edits, until clean

### Proposed addition

> **After non-trivial multi-section doc edits, re-read the full doc top-to-bottom and iterate until no major or factual errors surface.** The dominant failure mode for multi-section edits is cross-section drift (count updated in §A but not §B; status changed in §3 but stale reference left in §10). One full re-read per edit pass catches almost all of it. Plan on iteration ≥ 2; stop when the most recent pass surfaces zero major findings.
>
> *Grounded in: three iteration passes on `research/PLAN.md` v0.10, each catching new self-introduced bugs.*

### Why this earns its place in your agents file

This session's PLAN.md update took three iteration passes. Iteration 1 was the initial edit. Iteration 2 caught 4 bugs introduced by iteration 1 (count drift in §1 and §3.4, stale "/retrospective/ → 2026-05-11-01" in §2 layout, wrong ADR count). Iteration 3 caught 4 more bugs (Path-B-only undercount, misattributed URL, stale "3 pages" in Future research, stale "13 followups" typo). Iteration 4 caught nothing — that was the stopping signal.

Without the iteration discipline, the PR would have shipped with at least the wrong cumulative count in the §1 status line. With a fixed "iterate once" rule, iteration 3's findings would never have surfaced. The stopping rule — "stop when the last pass is clean" — is the load-bearing piece. It bounds work by quality rather than by clock.

---

## Suggestion 3: Separate assessment from revision for long doc updates

### Proposed addition

> **For doc revisions >5 sections, produce a written drift assessment before editing; pause for user sign-off.** When the user asks to update a long-lived doc, default to producing a structured drift report first (major / minor / not-drifted), then wait for explicit or implicit acceptance before applying edits. The assessment is the artifact; the subsequent edit pass treats it as the change plan.
>
> *Grounded in: the user's "Don't change it yet, just assess" instruction in this session's PLAN.md phase 2, which produced a written drift report that became the v0.10 change plan.*

### Why this earns its place in your agents file

Without the assessment step, a doc-update task tends toward wholesale rewrite — the agent reads the doc, identifies that several sections are stale, and rewrites them in one pass. The wholesale-rewrite path loses archival context (e.g., the §§11–17 archive in PLAN.md) and conflates "drift fixes" with "structural improvements" in a single un-reviewable diff.

The assessment-first path produces a visible change plan, lets the user prune scope (e.g., "skip §11 round-2-complete stanza — that's a longstanding TODO"), and makes the subsequent edit pass faster because the plan is already written.

Cost: one extra tool-message-cycle before edits begin. Benefit: visible scope control, no surprise rewrites, and the assessment itself doubles as an iteration-pass checklist.

---

## Suggestion 4: Don't `git pull origin main` while on a just-merged feature branch

### Proposed addition

> **After a feature branch merges and its remote is deleted, do not `git pull origin main` while still on that local branch.** The pull will fast-forward the *local feature branch* (not main) into the merge commit, producing a phantom "1 unpushed commit" the stop-hook will flag. Instead: switch to main first, then pull. If more work is needed on the feature, `git branch -D <branch>` then `git checkout -b <branch>` to recreate fresh from main.
>
> *Grounded in: the Phase 3 stop-hook event in this session.*

### Why this earns its place in your agents file

The session's PR #49 merged and its remote `claude/update-next-steps-docs-xQNrQ` branch was deleted. I then ran `git pull origin main` while still on the local feature branch. Because the local branch's remote-tracking ref had been deleted, the pull silently fast-forwarded the local branch (not main) to `origin/main`'s tip — the merge commit of PR #49 itself. The stop-hook then flagged "1 unpushed commit." Strictly true, but the commit was just a merge-commit echo, not real work.

Recovery took 4 commands: `git checkout main && git pull && git branch -D <branch> && git checkout -b <branch>`. Total ~2 minutes of confusion. The rule prevents the confusion entirely. The marginal cost is one extra `git checkout main` before `git pull`.

---

## Suggestion 5: GitHub `[fetch-urls]` issues are closed by the drain PR's author

### Proposed addition

> **When a `[fetch-urls]` drain PR merges, the merging author closes the source issue(s) explicitly in the same session.** GitHub does not auto-close issues whose work landed via PR unless the PR body contains a `Closes #N` line. Open-issue lists are a working surface for the next session; stale-open issues are noise.
>
> *Grounded in: issues #41 and #42 staying OPEN on GitHub after PR #44 (their drain) merged, and persisting through three subsequent sessions.*

### Why this earns its place in your agents file

This session discovered #41 and #42 still listed as OPEN on GitHub even though their drains had been merged in PR #44 days earlier. The PLAN.md "Resumption checklist" §6 explicitly says "Check open issues" as step 3 — those stale-open issues forced repeated cross-referencing between the issue tracker and PLAN.md §3.3. Either auto-close via `Closes #N` in PR bodies or explicit-close in the merging session works; the rule just needs to *be* a rule.

The cost: one extra GitHub API call per drain PR (or two `Closes #N` lines in the PR body). The benefit: the issue list is a usable working surface, not a drift surface.

---

## Suggestion 6: `git log` dates default to local timezone; use `%aI` for strict UTC

### Proposed addition

> **For retrospective filenames and any cross-day date claim, use `git log --format="%h %aI %s"` (ISO 8601 with offset) rather than `--date=short`.** The `--date=short` form displays the *local-timezone* date, which can disagree with strict UTC for commits authored near midnight. Retrospective filenames embed the UTC date; mismatch silently breaks day-sequence numbering.
>
> *Grounded in: round-8 commits authored 2026-05-13 23:15 UTC but displayed as `2026-05-13` in local-tz `git log` — the corresponding retrospective is named `2026-05-14-01` because it was authored after UTC midnight.*

### Why this earns its place in your agents file

This session encountered round-8 commits like `0b19feb` whose author timestamp is `2026-05-13T23:15:53+00:00` (UTC) but whose `--date=short` display in `-05:00` was `2026-05-13 18:15`. Meanwhile the retrospective covering those commits is named `2026-05-14-01`. Without the strict-UTC format, it's easy to write "drains happened 2026-05-13" in some places and "drains happened 2026-05-14" in others within the same doc — both technically defensible but internally inconsistent.

The rule keeps date claims auditable. Cost: one extra character in the format string.

---

## Suggestion 7: Cross-cited URLs affect more than one report; grep before claiming attribution

### Proposed addition

> **Before claiming "URL X affects report N," grep all source-table-containing files for that URL.** A URL grouped under one heading in a `[fetch-urls]` issue may be cross-cited from a second (or third) report. Naive issue-grouping doesn't always match where the URL actually got referenced.
>
> *Grounded in: `openai.com/index/introducing-swe-bench-verified` grouped under "SWE-bench" in issue #41 (suggesting report 22) but actually cited from both `research/18-openai-codex-substrate.md` and `research/22-academic-foundations.md`.*

### Why this earns its place in your agents file

The session's iteration pass 3 caught this drift: PLAN.md §4.3 item 3 had been written to say "Affects `research/18-openai-codex-substrate.md` (which remains 🟡 solely because of these 3 URLs)." But report 22's sources table also lists the swe-bench-verified URL as a 🟡 row. A single `grep -l "swe-bench-verified" research/*.md` would have shown both files. Without the rule, the §10 lookup-table row and the §4.3 item are subtly inconsistent.

Cost: one extra `grep -l <url> research/*.md` per attribution claim. Benefit: cross-reference accuracy in inventory docs.

---

## Suggestion 8: Note iteration findings in commit message body

### Proposed addition

> **When a non-trivial doc edit went through multiple iteration passes, enumerate what each pass caught in the commit message body.** This is a reviewer-confidence signal: it shows that iteration actually happened and what kinds of drift the agent was catching. One line per pass is enough.
>
> *Grounded in: PR #50's commit message for `6d8389e`, which enumerated 8 specific iteration findings across three passes.*

### Why this earns its place in your agents file

Without enumeration, the reviewer has no way to tell whether the agent iterated meaningfully or just renamed "iteration 1" to "iteration 3." The enumeration is also useful to future-you: when a similar doc-edit task arrives next month, the prior commit's iteration log is the best available checklist.

Cost: ~5 extra lines in the commit message body. Benefit: reviewer trust, plus a written record of the drift surface for the next pass.

---

## Suggestion 9: Deferred MCP tools require an explicit `ToolSearch` before invocation

### Proposed addition

> **MCP tools that appear by name only in `<system-reminder>` lists are deferred — their schemas are not loaded until you call `ToolSearch query "select:<tool_name>"`. Calling them directly fails with InputValidationError.** Plan one `ToolSearch` per MCP-tool first-use per session.
>
> *Grounded in: needing to load `mcp__github__list_pull_requests`, `mcp__github__create_pull_request`, `mcp__github__subscribe_pr_activity`, `mcp__github__pull_request_read` schemas individually before invocation in this session.*

### Why this earns its place in your agents file

This is sandbox-mechanics knowledge that's easy to forget across sessions. Without the rule, a session that wants to use a GitHub MCP tool burns one extra round-trip per tool discovering that its schema isn't loaded. With the rule, the agent batches `ToolSearch` calls at the start of the session for tools it knows it'll need.

Cost: one extra tool call per deferred-tool first-use. Benefit: avoids `InputValidationError` round-trips and makes parallel tool calls feasible (you can't parallel-call a tool whose schema isn't loaded).

---

## Suggestion 10: Branch cleanup post-merge is a 4-command idiom

### Proposed addition

> **When more work is needed on a branch whose remote was deleted by a merge, the canonical cleanup is: `git checkout main && git pull origin main && git branch -D <branch> && git checkout -b <branch>`. Do not rebase, reset --hard, or force-push to "fix" a stop-hook flag — recreate the branch fresh from main.**
>
> *Grounded in: this session's Phase 3 cleanup after the stop-hook flagged a phantom unpushed commit on a just-merged feature branch.*

### Why this earns its place in your agents file

The phantom-unpushed-commit scenario can tempt destructive operations (reset, force-push, --no-verify). The 4-command idiom is non-destructive and produces a clean branch from main. It's also memorable enough that an agent can apply it without ad-hoc reasoning.

Cost: 4 commands. Benefit: avoids destructive git operations and keeps the local branch state interpretable.
