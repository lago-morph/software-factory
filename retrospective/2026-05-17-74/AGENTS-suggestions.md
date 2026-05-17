# AGENTS.md suggestions — 2026-05-17-74

These are proposed additions to the project's agents file (typically `AGENTS.md` at the repo root). Each section contains:

1. **Proposed addition** — the exact text to paste.
2. **Why this earns its place in your agents file** — the argument for doing it, grounded in something that happened (or nearly happened).

Decide each on its own merits. Skip ones that don't apply to your operating posture; copy-paste the ones that do.

---

## Suggestion 1: Verify GitHub MCP auth at every multi-step pass boundary

### Proposed addition

> **GitHub MCP auth is a session pre-condition, not an error case.** Before starting any chain of work expected to take more than a few minutes — including any pass that dispatches subagents, opens a PR, or makes more than three dependent edits — call `mcp__github__get_me` to confirm auth is live. If it fails with an auth-shaped error, stop and run the `github-connection-resilience` skill before doing anything else.
>
> *Grounded in: two recent sessions lost mid-flight when GitHub MCP auth went stale silently and the failure was discovered only at "push" time, after work had already been stranded.*

### Why this earns its place in your agents file

The cost of `mcp__github__get_me` is one tool call with no side effects. The cost of skipping it is up to a session's worth of work stranded in an ephemeral sandbox — the exact failure mode the user invoked this work to address. The asymmetry isn't close. Even a 1% rate of auth drops over a multi-hour session translates to a high probability of at least one drop; encoding the check as a discipline (vs. an error-handling reflex) means it happens before the drop matters, not after.

A weaker version of this rule already exists implicitly in `always-commit-skill-to-repo` (commit and push often), but that only limits how much is *unrecoverable* when auth drops. The pre-pass auth check limits whether the drop happens *during* work in the first place, which is the more valuable property.

---

## Suggestion 2: Commit-and-push every checkpoint, not every session

### Proposed addition

> **Commit and push at every logical checkpoint — not once at session end.** A "checkpoint" is whichever comes first: a file is in a coherent state; a subagent has returned; a planned step has completed; 20 minutes of wall-clock time have passed; you're about to dispatch one or more subagents; you're about to start a session-end activity. When in doubt, commit and push. The marginal cost is zero; the cost of stranded work is hours.
>
> *Grounded in: the github-connection-resilience skill design — auth drops are detectable but not always preventable, so the second line of defense is shrinking the worst-case "lost work" window from a session to a checkpoint.*

### Why this earns its place in your agents file

This generalizes a rule that's already informally true. Most agents batch a session's commits at the end "for narrative coherence" — but commit messages are cheap, and a future reader caring about narrative coherence can rebase or squash later. The session-loss math is unforgiving: a single auth drop or sandbox reclamation wipes everything since the last push. Promoting checkpoint cadence from "good practice" to "rule" closes the gap.

Cost of adoption: one extra `git push` per ~20 minutes — negligible. Benefit: bounds maximum stranded work to ~20 minutes worth, even when *no* other resilience mechanism fires.

---

## Suggestion 3: Coverage-check table before declaring a multi-requirement task done

### Proposed addition

> **For tasks with more than three distinct user requirements, write an explicit requirement → implementation-location table before committing.** Format: one row per requirement, with the verbatim requirement (or short paraphrase) and the file/section where it is addressed. Read it once top-to-bottom before staging. Any row you cannot fill is a missed requirement.
>
> *Grounded in: the 17-row coverage-check table used in this session before committing the new skill — caught nothing missed, but produced confidence and a ready-to-send user summary as a side benefit.*

### Why this earns its place in your agents file

Long, multi-part user requests are the highest-risk surface for partial-implementation bugs that look complete from the inside ("I built a thing that does most of what you asked"). The dominant failure mode is omission, not error — features quietly dropped during the rush to ship. A coverage-check table forces an exhaustive enumeration against the original request, which is exactly the check that's hardest to do from memory after building the thing.

Cost: a 5–10 line table that takes 2 minutes to write. Benefit: catches the silent omission before it ships, and the same table doubles as the basis of the PR description and the user-facing summary.

---

## Suggestion 4: Skill resources go in `resources/`, loaded on demand

### Proposed addition

> **For skills with sizable optional procedures, split the procedure into `resources/*.md` and reference it from `SKILL.md` with explicit "only load if X" instructions.** The main file stays small enough for routine triggers; the optional procedure costs nothing until the rare path is taken. Mirrors the existing pattern in `research-pipeline/scripts/` and `parallel-subagent-fanout/spec/`.
>
> *Grounded in: this session's `github-connection-resilience` skill split into `SKILL.md` (276 lines, always loaded) + `resources/recovery.md` (368 lines, only on degraded-state) + `resources/reconnect.md` (216 lines, only after recovery). Loading all three for every "check auth" trigger would waste tokens 99% of the time.*

### Why this earns its place in your agents file

Token economy in skills compounds. Every skill that loads at trigger time consumes context window for the rest of the session. A 800-line monolithic skill loaded for a 30-second auth check is a meaningful tax; the same skill split with on-demand loading is a 30% of that. The rule generalizes: any skill with a "rare but important" procedure benefits from the split.

The pattern also improves the skill's own readability — the main file becomes the contract, the resource files become the implementation. Reviewers can audit the contract without scrolling through the recovery weeds.

---

## Suggestion 5: Patch-tarball + `SendUserFile` is the canonical agent-session escape hatch

### Proposed addition

> **When session shutdown is forced (auth loss, sandbox reclamation, hard stop) and remote push is unavailable, capture all committed-but-unpushed work as a `git format-patch` series, bundle into a tar.gz, and surface via `SendUserFile` with `status: "proactive"`. Drop a `RECOVERY-INSTRUCTIONS.md` at the repo root with copy-pasteable `git am` instructions so the patch is self-applying even without conversation context.**
>
> *Grounded in: the recovery procedure in the github-connection-resilience skill — the harness file-surface mechanism is the only post-disconnect channel back to the user, so a patch that isn't sent via `SendUserFile` is lost.*

### Why this earns its place in your agents file

The two failure modes that have to be designed for are (a) auth lost permanently, (b) sandbox reclaimed before retry. Both make the remote unreachable. `git format-patch` preserves commit metadata that a flattened `git diff` would lose (authorship, message, individual boundaries); the tar.gz keeps it as one downloadable file; `SendUserFile` is the harness mechanism that puts the file on the user's device even if they have stepped away.

A weaker fallback (e.g., paste-the-patch-into-chat) doesn't survive the conversation rolling out of the user's UI buffer or context truncation. The triple of *format-patch + tar.gz + SendUserFile* is the minimal-rigorous escape hatch.

---

## Suggestion 6: Recovery commits stay in history — no rebase, no amend

### Proposed addition

> **Once you have made a "Recovery: ..." commit (or any commit produced by the github-connection-resilience recovery procedure), do not rebase or amend it out of existence even if connectivity is later restored and the work pushes cleanly. The commit is the audit trail of the resilience event.** A future retro-coverage audit will look for these; a future debugging session reading the history will want to see them. The cost of keeping a one-line "Recovery: ..." commit is zero; the cost of erasing the evidence of a near-miss is that the system can't learn from it.
>
> *Grounded in: the reconnect.md procedure's explicit anti-pattern list — "rebasing or amending the recovery commits out of existence" was called out because the temptation is real (the work pushed fine in the end, why leave evidence?) and the wrong answer is destructive.*

### Why this earns its place in your agents file

The general principle is bigger than just recovery commits: **any commit that records a system event worth knowing about later should be immutable, even if the event was eventually resolved cleanly**. Force-pushed history loses the only evidence that the event happened. This applies equally to "rolled back X" commits, "tried Y and reverted" commits, "investigated bug Z" commits, etc. Make it a rule once, apply broadly.
