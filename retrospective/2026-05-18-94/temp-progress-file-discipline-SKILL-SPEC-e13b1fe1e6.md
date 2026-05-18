# Spec: `temp-progress-file-discipline`

- **ID**: SKILL-SPEC-e13b1fe1e6
- **Source retrospective**: ../2026-05-18-94.md

## Intent

When mid-session scope grows past ~5 sub-tasks or the user piles on requirements mid-stream, write a dotfile progress plan (e.g., `.feature-progress.md`) to track checkbox state across the swap-heavy main context. The file lives in the repo root, captures the live scope as the user expands it, and is deleted before commit. Solves the failure mode of losing track of which requirements have been addressed when the conversation grows past comfortable working-memory length.

The session moment: I was working on "plan-update discipline" (one item). The user added: drain.py auto-emit; plan-audit subskill; README skip-list; PDF /URL ordering; MIME title decode; want-promotion bug fix; tidy-wants sweep; record-migration via pointer_to. That's 8 sub-tasks, several with their own sub-sub-tasks (tests, lint, docs). When I'm 1500 messages deep into a session, I lose track of which I've finished. I wrote `.plan-discipline-progress.md` with a checkbox table; it kept me honest and was a 10-line file with zero downside.

## Trigger

**Direct user phrases:**
- "Make sure you don't lose track."
- "There's a lot here — keep a list."
- "Write a plan first."
- "Add this too: …" (when followed by 2+ additional asks mid-work).

**Proactive triggers:**
- The user adds 3+ new requirements in a single message after work has started.
- The session has accumulated 5+ open sub-tasks that aren't all written down.
- The user pivots scope ("oh and also fix X") and the conversation transcript is now too long to scan reliably.
- You catch yourself asking "wait, did I do step 4?" — that's already late; the file should have existed.

**Negative triggers (do NOT activate):**
- A single-task session. The overhead isn't worth it.
- A task with a natural sequence (1 → 2 → 3 → done) where checkpoint state is obvious from the codebase.
- A short session (< 30 min, < 100 messages).

## Inputs

- The user's evolving scope (running list of requirements as they expand).
- The current PR branch (so the file can be staged-and-deleted via git, not just rm).
- Knowledge of which `.gitignore` exclusions or naming conventions the project uses (so the file doesn't accidentally get committed).

## Outputs

- A single repo-root file named `.<feature-tag>-progress.md` (the leading dot is intentional — it signals "tooling, not content"). Example names: `.plan-discipline-progress.md`, `.refactor-progress.md`, `.bug-94-progress.md`.
- A short structured markdown body. Required sections:
  - `## Confirmed scope` — user-answered + user-added items, grouped by source.
  - `## Progress` — a checkbox table: task name, status (`⬜ todo` / `✅ done` / `🟡 in-progress`), one-line note.
  - `## Cleanup before commit` — explicit reminder to delete this file.
- A pre-commit cleanup: `rm .<feature-tag>-progress.md` before the final `git add -A`.

## Workflow

1. **Detect the trigger.** When the user adds 3+ requirements in a message, or you catch yourself losing track, propose the file: "Let me write a temp progress file at `.<tag>-progress.md` to track all this — I'll delete it before commit."
2. **Write the file at repo root.** Filename starts with `.` (dotfile). Body has the three required sections above. Each task in the Progress table has a status, a one-line description, and (if useful) the user message or AskUserQuestion answer that introduced it.
3. **Update inline as you work.** Mark items `✅ done` as they complete. Re-read the file when you're unsure about state — it's faster than scanning the conversation.
4. **Add new items as the user adds scope.** When the user piles on, the file gets a new row, not a separate mental note.
5. **Before commit: delete.** The file is scratch; it does not belong in the repo's history. Add `rm .<tag>-progress.md` to your pre-commit checklist. If `git status` ever shows the file as untracked at commit time, you forgot to delete it.
6. **(Optional) Reference in commit message.** It's fine to summarize the list in the commit message body, but the file itself stays out.

## Concrete examples

### Example 1: the session's `.plan-discipline-progress.md`

Scope ballooned: from "plan-update discipline" to 8 sub-tasks across two layers (code + data). I wrote:

```markdown
# Working plan — PR `claude/plan-update-discipline`

Scratch file — NOT for commit. Delete before pushing the PR.

## Confirmed scope

User-answered (AskUserQuestion):
- A. Add a plan-audit subskill
- B. drain.py auto-appends §1 + §10 entry to PLAN.md
- C. README.md skip-list in drain
- D. PDF /URL ordering: prefer arxiv/doi over github
- E. RFC 2047 MIME title decode in extract_title

User-added (later messages):
- F. Want-promotion bug fix via format-final rule
- G. Operational: only use the skill / jq for catalog edits

## Progress

| | Item | Status |
|---|---|---|
| A | plan-audit script (`check-plan-consistency.py`) | ✅ done (committed in ade1562) |
| A | `_plan/audit.md` + `_plan/update-discipline.md` resource docs | ✅ done |
| A | Wire into `lint-sources.sh` as advisory warning | ⬜ todo |
| A | Unit tests for plan-consistency | ⬜ todo |
| B | `drain.py` auto-PLAN-update on successful drain | ⬜ todo |
| ... | ... | ... |

## Cleanup before commit

- Remove this file
- Update `update-discipline.md` to mention the auto-append flow
```

When I'd finished work and ran `git status --short` I saw `?? .plan-discipline-progress.md`. Ran `rm` before `git add -A`. The PR diff is clean.

### Example 2: a refactor with cascading downstream tasks

A user asks: "rename `Foo` to `Bar` across the codebase." Halfway through, they add: "and the same for the schema files… and the docs… and update the migration guide." Now there are 5–10 codebases / paths affected.

Write `.rename-foo-bar-progress.md`:

```markdown
# Working plan — Foo → Bar rename

## Files / paths in scope

- [ ] `src/foo/` → `src/bar/` (rename dir + git mv)
- [ ] `tests/test_foo.py` → `tests/test_bar.py`
- [ ] `schemas/foo-v1.json` → `schemas/bar-v1.json` + bump version
- [ ] `docs/foo-guide.md` → `docs/bar-guide.md`
- [ ] `docs/migration-from-v0.md` — add Foo → Bar section
- [ ] `.github/workflows/foo-ci.yml` → `bar-ci.yml`
- [ ] grep for any remaining `Foo` literals (`grep -rln "Foo" .`)
- [ ] update CHANGELOG
- [ ] open PR

## Cleanup

- rm this file
```

Check items off as you go. The grep step at the end catches anything you forgot — the file's job is to keep you from forgetting *that you need to grep*.

## Anti-patterns

- **Committing the file.** It's scratch. The commit message can summarize the work; the file itself is noise to reviewers and to git log. Always `rm` before `git add -A`.
- **Writing the file as PLAN.md / TODO.md (non-dotfile).** Reviewers won't know it's scratch. The leading `.` signals "tooling, deletable" and reduces the chance of an accidental commit.
- **Writing it after the work is done.** The file is for *in-flight* tracking. Writing it retroactively to "summarize what I did" is the wrong artifact — that belongs in the commit message or the PR description.
- **Putting estimated times or priorities in the file.** It's a checklist, not a project plan. Status (`⬜ ✅ 🟡`) is enough.
- **Not deleting it because "maybe useful next time".** It captured ONE session's scope. The next session has different scope. Delete; rewrite if needed.
- **Tracking trivia.** Items like "add error handling to function X" don't need a checklist row — they're either part of doing function X or they're a separate task. Reserve rows for distinct deliverables.

## Acceptance criteria

1. The file's filename starts with `.` so it visually flags as tooling.
2. The file is at the repo root, not nested under `docs/` or `notes/`.
3. The file contains a `## Cleanup before commit` section with `rm` instructions.
4. At commit time, `git status --short` does NOT show the file (it was deleted before staging).
5. The file's existence does not show up in the PR's diff or the merged commit history.

## Files this skill creates / modifies

- `/<repo-root>/.<feature-tag>-progress.md` — the scratch file; created mid-session, mutated as scope evolves, deleted before commit. Never committed to history.
