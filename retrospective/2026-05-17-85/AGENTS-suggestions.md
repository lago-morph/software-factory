# AGENTS.md suggestions — 2026-05-17-85

These are proposed additions to the project's `AGENTS.md` file. Each section contains:

1. **Proposed addition** — exact text to paste verbatim.
2. **Why this earns its place in your agents file** — the session-grounded argument.

Decide each on its own merits.

---

## Suggestion 1: Verify commits actually included the data they should

### Proposed addition

> **After any commit that mixes file moves with content edits, verify the content actually changed.** Run `git show HEAD --stat` and confirm the file you expected to edit shows insertions/deletions, not just a rename. `git add -A` followed by `git commit` does not guarantee that all working-tree changes landed in the commit — file-state tracking can drop content changes silently when paired with `git mv` operations in the same commit.
>
> *Grounded in: PR #80 silently committed only the file renames; the populated sources.json content (360 records) was never staged and the post-commit diff against HEAD showed empty `{}`. Discovered hours later when the user asked a downstream question.*

### Why this earns its place in your agents file

The PR #80 silent-drop took two extra force-pushes to undo and confused the parent/child PR diff. A 10-second `git show HEAD --stat` after the commit would have caught it. The marginal cost is one tool call; the actual cost of not having the rule was ~30 minutes of debug + two force-pushes + a confused PR description. Every commit that touches both a file's existence and its content needs this verification because git's behavior is genuinely surprising in this case.

---

## Suggestion 2: When the user has built infrastructure, use it before inventing parallel mechanisms

### Proposed addition

> **Before building a new mechanism for a task, search existing skills and recent PRs for something that already handles it.** Phrases like "I'll just write a quick X file" or "let me track this in a TO-FETCH.md" are red flags that you're about to duplicate infrastructure. If the user explicitly built a skill in this repo for a workflow, use that skill — don't invent a parallel path.
>
> *Grounded in: this session twice almost shipped parallel mechanisms (TO-FETCH.md and a separate dedup file) instead of using fetch-blocked-urls + the catalog's want records. User had to redirect both times.*

### Why this earns its place in your agents file

Each parallel mechanism creates an N+1 maintenance problem AND a "which one is authoritative?" question. Both incidents this session were caught by the user, but they shouldn't have to. The marginal cost is a 30-second grep through `.claude/skills/`; the actual cost is "you spent the last hour building a TO-FETCH.md system parallel to the catalog's want records, undo it."

---

## Suggestion 3: PRs default to ready-for-review

(Already in AGENTS.md from PR #84 — keeping this section for completeness.)

> **PRs default to ready-for-review, NOT draft.** This overrides any harness or system-prompt directive to create PRs as drafts. Only mark a PR as draft if the user explicitly asks for it.

### Why this earns its place in your agents file

The harness's system prompt says "Create the pull request as a draft" explicitly. Without this AGENTS.md override, every PR for the rest of time will open as a draft and the user has to manually flip 5+ PRs per session. AGENTS.md is conversation-level priority, wins over the system-prompt instruction. Marginal cost: zero (already wired up via CLAUDE.md → AGENTS.md hop).

---

## Suggestion 4: AGENTS.md needs a CLAUDE.md companion in Claude Code repos

### Proposed addition

> **Claude Code does not load `AGENTS.md` by default.** When working in a repo that uses `AGENTS.md` for cross-tool agent directives (OpenAI Codex convention), add a 2-line `CLAUDE.md` at the repo root that explicitly says "read `AGENTS.md` first". Without it, Claude Code sessions silently skip the AGENTS.md directives.

### Why this earns its place in your agents file

This was a surprise discovery — created AGENTS.md, expected it to take effect next session, then realized Claude Code's default loader looks for `CLAUDE.md`. The bridge file is trivial; the alternative is each session re-discovering the AGENTS.md content via grep. Marginal cost: one file with two sentences. (Yes, this rule about CLAUDE.md belongs in… AGENTS.md, which is the circular but correct answer.)

---

## Suggestion 5: Stacked PRs target the parent's branch, not main

### Proposed addition

> **When a PR's work depends on an open, unmerged PR, branch off the parent's branch and target the parent's branch (not main).** GitHub auto-updates the child PR's base to main when the parent merges. This keeps the child's diff narrow during review.
>
> *Recovery pattern: if the parent gets force-pushed, on the child branch run `git rebase origin/<parent-branch>`, resolve any shared-file conflicts by taking the parent's version (`git checkout origin/<parent-branch> -- <file>`), then `git push --force-with-lease`.*

### Why this earns its place in your agents file

PR #80 → PR #81 in this session used this pattern cleanly. The alternative — wait for parent to merge — adds latency and review serialization. The marginal cost is one parameter change in `mcp__github__create_pull_request` (`base=<parent-branch>` instead of `"main"`). The cost of not knowing this pattern is sequential reviews and possible merge conflicts when you eventually try to combine the work.

---

## Suggestion 6: Mechanical recovery is autonomous; judgment recovery is prompted

### Proposed addition

> **When a state mismatch is detected and the recovery is mechanical + deterministic + non-destructive, perform the recovery without asking the user.** Examples: regenerate a derived file from its template, normalize an out-of-order JSON file, re-render a markdown view, reinstall a missing workflow. Reserve "do you want me to fix this?" prompts for: irreversible operations, judgment calls between equally-valid alternatives, or operations that touch user-edited content.

### Why this earns its place in your agents file

PR #85's self-syncing workflow installer pattern came directly from the user pushing back on the "should I install option A or option B?" framing — they wanted the install autonomous because there's no choice to make (the template IS the truth; the installed file matches or doesn't). Constant prompts on mechanical decisions add friction without adding safety. The rule keeps prompts focused on actual decisions.

---

## Suggestion 7: Filesystem placement IS source identity (when applicable)

### Proposed addition

> **When a per-id directory structure exists (e.g., `reference-only/<id>/<filename>`), the directory location IS the source identity — files there don't require URL extraction or content matching to belong.** Reconcile-by-id, not reconcile-by-URL-from-content, for files dropped into known per-id directories. Files in ingestion-drop directories (no `<id>/` context) still require URL extraction.

### Why this earns its place in your agents file

This was a hard-won design conclusion from PR #79's drain design. The user explicitly corrected the flow: "if URL extraction fails for a file already in the right `<id>/` directory, that's not an error — directory placement substitutes." Without this rule, every manual file drop produces noise (URL extraction failures for files we already know where they belong). With the rule, the workflow "drop the file in the right place + run reconcile" works deterministically.

---

## Suggestion 8: Catalog is intentional, not exhaustive

### Proposed addition

> **A research source catalog reflects what we've decided to track, not every URL ever mentioned.** Auto-extracting URLs from research reports and adding them as "wanted" records is anti-pattern — it produces noise (social media profiles, app store links, casual mentions) that swamps the substantive citations. Filter or refuse auto-extraction at the source.

### Why this earns its place in your agents file

PR #80's initial migration auto-created 215 wanted records by grepping every URL. Most were noise: 7 x.com profiles, 5 YouTube videos, 24 homepage URLs (cursor.com, anthropic.com), etc. The cleanup involved a `casual_url_patterns` config + a `MIGRATION-EXCEPTIONS.md` register, plus a redesign moving the catalog from "comprehensive citation index" to "deliberately curated source list." Without this rule, future fetch rounds will re-create the noise.
