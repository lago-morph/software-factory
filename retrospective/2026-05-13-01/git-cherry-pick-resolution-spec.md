# Spec: `git-cherry-pick-resolution`

## Intent

Cherry-picking commits from a side branch onto a different base is a recovery pattern for orphaned work — commits authored after a PR merged but never re-merged. The cherry-pick itself is mechanical; what's tricky is **resolving conflicts when the commits' parent state references files or paths that no longer exist (or have moved) on the target base.**

This skill solves a specific scenario from the 2026-05-13 session: four commits on `origin/claude/parallelize-with-subagents-SO0nR` (the pt-2 drain) were authored 18 minutes after PR #25 merged. They never reached `origin/main`. A naive cherry-pick produced three conflicts:

- **Rename/delete conflict** — sub-30 wanted to delete `research/manual/2026-05-08-every-noah-brier-culture-of-ai-engineering.txt`, but the cleanup pass had moved that content to `reference-only/brier-culture-of-ai-engineering.txt`.
- **Content conflict** — sub-32 wanted to update `research/followup/07-evals-deepdive.md` referencing `09-jaymin-harnesses-partial.md`, but that partial had been deleted and the unified report's new name was different.
- **Large structural conflict** — the recording commit (984c91d) wanted to add a §14.3.1 to v0.7's PLAN.md structure; main had v0.8's totally different structure.

All three were resolved successfully. The pattern: **restore-from-history what's missing before the cherry-pick, then resolve the per-conflict surface using "keep cleanup-pass version + port valuable content" rules.**

## Trigger

**Direct user phrases:**
- "Do the cherry-pick"
- "Recover the orphaned commits"
- "Bring those commits onto main"

**Proactive triggers:**
- After discovering commits on a side branch that the target branch lacks.
- When asked to "merge that other work in" where the other work is on a stale branch.

**Negative triggers:**
- The side branch can be merged with `--no-ff` cleanly (no conflicts) — just merge.
- The work hasn't been reviewed; do that first.

## Inputs

- The side branch name (e.g., `origin/claude/parallelize-with-subagents-SO0nR`).
- The list of commits to cherry-pick (or a range).
- The target base branch (typically `origin/main`).

## Outputs

- A new branch with cherry-picked commits applied + conflicts resolved.
- A PR to the target base.
- A summary of conflict-resolution decisions for reviewer context.

## Workflow

1. **Sync and inspect the source branch.**

   ```bash
   git fetch origin
   git log <source-branch> --not <target-base> --oneline
   ```

   Read each commit's subject + stat:

   ```bash
   git show --stat <commit>
   ```

   Note any commits that:
   - Add or modify files that are still relevant.
   - Delete files that have since been MOVED on the target base (the deletion will likely conflict).
   - Reference paths that no longer exist on the target base (text edits will likely conflict).

2. **Pre-fix expected conflicts via restore-from-history.** For any file the side branch will try to delete that was MOVED on the target base, restore the source content under its new name BEFORE the cherry-pick:

   ```bash
   # The Brier txt source is in <parent-of-deletion-commit>
   git show <commit>^:<old-path> > <new-path>
   ```

   Commit the restore separately so the conflict resolution is reviewable.

3. **Create a recovery branch off the target base.**

   ```bash
   git checkout -b claude/recover-<description> <target-base>
   ```

4. **Cherry-pick commits one at a time.**

   ```bash
   git cherry-pick <commit>
   ```

   If clean: proceed.

   If conflict: read the conflict type from `git status`:
   - **`Unmerged paths: deleted by them: <file>`** — the side branch wanted to delete a file that exists on the recovery branch. Decide: keep the file (run `git add <file>`) or delete it (run `git rm <file>`). Then `git cherry-pick --continue`.
   - **`Unmerged paths: both modified: <file>`** — content conflict. Open the file, look for `<<<<<<<`/`=======`/`>>>>>>>` markers. Resolve by either taking HEAD's version, taking the cherry-pick's version, or combining both. Then `git add <file>` and `git cherry-pick --continue`.
   - **`Auto-merging <file>`** without "CONFLICT" — clean automatic merge; usually no action needed.

5. **Conflict-resolution rules of thumb:**
   - **Keep the cleanup-pass version of structural files** (PLAN.md, unfetched-sources.md) — these have been deliberately rewritten and shouldn't be reverted.
   - **Port valuable side-branch content into the cleanup-pass structure** — read what the cherry-pick wanted to add; find where it belongs in the new structure; add it there.
   - **Update path references inside cherry-picked files** — if the side branch references `research/manual/<file>` but the file is now at `reference-only/<new-name>`, edit the cherry-picked file to point at the new path before `--continue`.

6. **After all commits applied, write a reconciliation commit** that updates the target-base structural files (e.g., PLAN.md) to reflect that the recovery has landed. Mark previous "lost work" sections as RESOLVED.

7. **Push and open a PR.** Document each conflict-resolution decision in the PR body so the reviewer can spot-check.

## Concrete examples

### Example 1: rename/delete conflict resolution (2026-05-13 session)

**Setup:**
- Side branch: `origin/claude/parallelize-with-subagents-SO0nR`
- Commit to cherry-pick: `925da5b` ("sub-30 drain Brier")
- Side-branch parent: had `research/manual/2026-05-08-every-noah-brier-culture-of-ai-engineering.txt`
- Side-branch effect: deletes that file + adds `research/followup/12-brier-pace-layers.md`
- Target base (after cleanup pass): file at `reference-only/brier-culture-of-ai-engineering.txt`, not at the old path

**Cherry-pick attempt:**
```bash
git cherry-pick 925da5b
# CONFLICT (rename/delete): research/manual/2026-05-08-every-noah-brier-culture-of-ai-engineering.txt
#   renamed to reference-only/brier-culture-of-ai-engineering.txt in HEAD,
#   but deleted in 925da5b
```

Git correctly detected the rename and flagged the conflict. Resolution:
```bash
# Keep the renamed file (don't honor the deletion)
git add reference-only/brier-culture-of-ai-engineering.txt

# Continue
git cherry-pick --continue --no-edit
```

The `research/followup/12-brier-pace-layers.md` was added cleanly by the cherry-pick.

**Follow-up:** the new `followup/12-brier-pace-layers.md` had a path reference at the top that said `drain of research/manual/...`. Update it to point at the new location:
```diff
- **Thread:** Round-3 fanout 20260511 sub-30 — drain of `research/manual/2026-05-08-every-noah-brier-culture-of-ai-engineering.txt`
+ **Thread:** Round-3 fanout 20260511 sub-30 — drain of `reference-only/brier-culture-of-ai-engineering.txt` (was at `research/manual/2026-05-08-every-noah-brier-culture-of-ai-engineering.txt` at drain time; moved to `/reference-only/` in the 2026-05-13 cleanup pass)
```

### Example 2: content conflict — preserve cleanup-pass version

**Setup:**
- Commit to cherry-pick: `ad565aa` ("sub-32 evals drain")
- Modified line on side branch: `Cross-reference with research/09-jaymin-harnesses-partial.md`
- Target base: that partial was deleted, unified report is `09-jaymin-book-harnesses-practices-mental-models.md`

**Cherry-pick:**
```bash
git cherry-pick ad565aa
# CONFLICT (content): Merge conflict in research/followup/07-evals-deepdive.md
```

Conflict region:
```
<<<<<<< HEAD
- Verbatim retrieval of the four primary URLs ... (cleanup-pass line)
- Cross-reference with `research/09-jaymin-book-harnesses-practices-mental-models.md` ...
=======
- Cross-reference with `research/09-jaymin-harnesses-partial.md` ...
>>>>>>> ad565aa (...)
```

Resolution: **take the cleanup-pass reference** (the partial is deleted; unified report is correct) **and apply the cherry-pick's intent** (which was to remove the "Verbatim retrieval..." TODO line because the verbatim content was just retrieved):

```diff
- Cross-reference with `research/09-jaymin-book-harnesses-practices-mental-models.md` for how Overstory frames its own evaluation
```

(Drop the TODO line. Keep the cleanup-pass reference target.)

Then:
```bash
git add research/followup/07-evals-deepdive.md
git cherry-pick --continue --no-edit
```

### Example 3: large structural conflict — port valuable content into new structure

**Setup:**
- Commit to cherry-pick: `984c91d` (recording commit)
- Side-branch change: adds a §14.3.1 to v0.7's PLAN.md
- Target base: v0.8 PLAN.md is fully restructured, no §14.3.1 exists

**Cherry-pick:** large conflict on PLAN.md (and another on unfetched-sources.md).

Resolution: **keep v0.8 structure** (don't revert the rewrite) but **port the valuable side-branch content** (the corpus-level lesson about every.to being action-fetchable) into the new structure. Find the natural home for it: PLAN.md §3.1 (pt-2 bottleneck section) and unfetched-sources.md (header note above the deferred-candidates table).

```diff
+ **Corpus-level lesson from pt-2:** `every.to/chain-of-thought/*`, `anthropic.com/engineering/`, `hamel.dev`, and `simonwillison.net` are all action-fetchable for publicly-visible bodies — the sandbox 403 does not propagate to GitHub-runner IPs. The `unfetched-sources.md` "Defer to user" label some of these previously carried was overcautious. **Recommendation:** before invoking a browser-cookie pass for any future URL, file a `[fetch-urls]` issue first; only escalate to Path B when the action also returns ❌.
```

Then `git add` and `git cherry-pick --continue`.

## Anti-patterns

- **Cherry-picking without first inspecting commit stats.** Some commits delete files that have moved; some reference files that no longer exist. Look first.
- **Reverting the target-base structural changes during conflict resolution.** Use the rule: **keep the cleanup-pass version of structural files**. Port valuable content INTO that structure, don't replace it.
- **Cherry-picking the merge commit instead of the underlying commits.** Merge commits have two parents; cherry-picking them requires `-m 1` and produces confusing diffs. Use the underlying single-parent commits.
- **Skipping the path-reference update inside cherry-picked files.** A cherry-picked file may reference paths that no longer exist on the target base. Update those references AS PART of the cherry-pick resolution, not later.
- **Forgetting to bump the target-base structural docs to mark recovery complete.** The PLAN.md §3.1 went from "HIGHEST-priority bottleneck" to "RESOLVED" only because of an explicit follow-up edit. Without it, future readers still see a bottleneck claim.

## Acceptance criteria

1. All commits from the source branch are applied OR explicitly marked skipped.
2. Each conflict has a documented resolution decision (in commit messages or PR body).
3. No file references a path that doesn't exist on the new branch.
4. The target-base structural docs (PLAN.md, README.md) are updated to reflect that the recovery has landed.
5. The new branch passes whatever CI / link-check / test commands the repo runs.
6. The PR body explains the conflict-resolution rationale so the reviewer can spot-check.

## Files this skill creates / modifies

- A new recovery branch at `claude/recover-<description>`.
- Modifies files per the cherry-pick.
- May restore deleted files from git history via `git show <hash>^:<path>`.
- Bumps target-base structural docs (PLAN.md, README.md, status sections) to reflect recovery.
- Opens a PR.
