# Spec: `stale-branch-audit`

## Intent

A long-running repo accumulates branches: workflow drop-branches (e.g. `fetched/issue-N`), prior-session feature branches (`claude/<slug>`), and occasionally branches whose work was partially merged via squash + cherry-pick rather than direct merge. After a PR merge, the user typically wants to know: "which of these are completely safe to delete?" The naive answer ("anything merged into main") is wrong in two failure modes:

1. **Stale-base traps** — a branch whose tip is reachable from main may still appear ahead of main when diffed (because its base predates many main commits). Conversely, a branch with a "fix" commit may have its fix already on main via a different route.
2. **Destructive-merge traps** — a branch that looks valuable may actually contain a stale state that, if merged, would re-introduce previously-removed content or delete recently-added files.

The 2026-05-14 session encountered both. `fetched/issue-36` showed `0 commits ahead` but a 54-file diff (stale base). `claude/drain-issue36-extras` had a commit titled "Fix report 07 source table" that *sounded* valuable but the fix was already on main; merging the branch would have reverted the prior session's Lenny full-transcript drain. This skill codifies the systematic audit so future "is this branch safe?" questions are answered with evidence, not vibes.

## Trigger

**Direct triggers:**
- "Which branches can I safely delete?"
- "Audit this branch — anything unique on it?"
- "Is `<branch-name>` safe to delete?"
- "After merging PR #N, which branches can go?"

**Proactive triggers (use without being asked):**
- After a PR merges and `git fetch --prune` reveals leftover branches that did not auto-delete.
- During session wrap-up when the user mentions cleanup.

**Negative triggers (skip):**
- The branch is currently checked out and being worked on.
- The branch was created in the last 24 hours and is plausibly still WIP.
- The user already gave a kept-list or asked about a specific branch (in that case, run only on the named branch).

## Inputs

- A list of branches to audit (or "all non-`main` branches on origin" if the user said "all").
- The current state of `origin/main` (after `git fetch --prune`).

## Outputs

A per-branch verdict, one of:
- ✅ **Safe** — all unique content is already on main; deletion loses nothing.
- ⚠️ **Has unique content** — branch contains files or commits not on main; identify what and recommend a preservation path (e.g. cherry-pick into a new branch).
- ❌ **Would destroy work if merged** — branch's effect, if merged into current main, would be net-destructive (re-introduces removed content, deletes recent additions). Use the verdict to explain WHY the user should not merge.

Plus, for each branch:
- Commits-ahead count.
- Files NEW / MODIFIED / DELETED vs current main.
- If MODIFIED: which files have unique-on-branch edits (via hash compare).
- A one-paragraph explanation that names the specific risk or absence-of-risk.

## Workflow

1. **Refresh the remote view**:
   ```bash
   git fetch origin --prune
   git ls-remote --heads origin | awk '{print $2}' | sed 's|refs/heads/||'
   ```

2. **For each non-`main` branch**, gather:
   ```bash
   br=<branch>
   ahead=$(git rev-list --count origin/main..origin/$br)
   echo "ahead: $ahead"
   git log --oneline origin/main..origin/$br | head -10
   git diff --name-only --diff-filter=A origin/main..origin/$br  # files NEW on branch
   git diff --name-only --diff-filter=M origin/main..origin/$br  # files MODIFIED
   git diff --name-only --diff-filter=D origin/main..origin/$br  # files DELETED on branch vs main (i.e. main has them, branch doesn't)
   ```

3. **For each NEW-on-branch file**, decide whether it's unique-valuable:
   - If it's in `research/fetched/issue-N/` and the namespace `research/fetched/issue-N/` no longer exists on main → likely a stub-stash from an already-drained round. Probably NOT unique-valuable.
   - If it's a `retrospective/`, `docs/adr/`, `reference-only/<new-slug>/`, or new report file → likely IS unique-valuable. Flag for preservation.
   - For each candidate-valuable file, check whether main has it under a different path (`git log --all --source --diff-filter=A -- <basename>`).

4. **For each MODIFIED file**, compare branch and main hashes:
   ```bash
   bh=$(git show origin/$br:<path> | sha256sum | awk '{print $1}')
   mh=$(git show origin/main:<path> | sha256sum | awk '{print $1}')
   [ "$bh" = "$mh" ] && status=IDENTICAL || status=DIFFERENT
   ```
   If DIFFERENT, look at the actual diff content. Two outcomes:
   - The branch has an OLDER version of the file (main moved on; branch's "modification" is just being out of date) → not unique.
   - The branch has UNIQUE edits not on main → flag for preservation.

5. **For each DELETED-on-branch file**, check whether main has it as a current artifact:
   - If yes AND the branch's commit log shows it was DELIBERATELY removed → potential destructive merge. ❌
   - If yes AND the branch's commit log shows no deliberate delete → stale-base artifact. ✅ harmless.

6. **Render the verdict**:
   - Branch with all-stale modifications + non-valuable NEW files + main-has-everything-relevant → ✅ safe.
   - Branch with valuable NEW or MODIFIED content → ⚠️ has unique; recommend preservation route.
   - Branch with deliberate-deletions of main-current files → ❌ would destroy; explain the destructive effect.

7. **Output the verdict table** to the user. For ⚠️ cases, offer to create a preservation branch (e.g. `claude/preserve-<source-slug>-<date>` containing only the unique files), commit, push, and let the user open a PR.

## Concrete examples

### Example 1 — full audit of 5 branches (real session material, 2026-05-14)

Branches under audit: `claude/audit-cleanup`, `claude/drain-issue36-extras`, `fetched/issue-36`, `fetched/issue-41`, `fetched/issue-42`.

**`fetched/issue-36`** — `git rev-list --count origin/main..origin/fetched/issue-36` returns `0`. Branch tip is reachable from main; the 54-file diff is stale-base noise (the branch HEAD is an ancestor of main). Verdict: ✅ safe.

**`fetched/issue-41`** — 1 commit ahead. All NEW files are in `research/fetched/issue-41/` namespace; all were cherry-picked into PR #44, drained, then deleted. Branch's DELETED-on-branch files (`user-next-steps.md`, `research/next-fetch-batch.md`) ARE on main → naive merge would re-delete them. Verdict: ⚠️ wait — actually ✅ because content is on main and the destructive effect is only realized if merged; deletion of the branch itself has no destructive effect.

**`fetched/issue-42`** — same posture. ✅ safe.

**`claude/drain-issue36-extras`** — 1 commit titled "Fix report 07 source table: welkaim profile rows resolved 2026-05-13." Commit message sounds valuable.

Hash check on `research/07-dark-factory.md`:
```bash
git diff origin/main..origin/claude/drain-issue36-extras -- research/07-dark-factory.md | head
```

The diff reveals that main has a welkaim attribution note that the branch DOESN'T have — the "fix" is already on main via a different commit. The branch's other changes would (a) re-add the partial 30-min Lenny transcript that main no longer has, (b) re-add 10 documented-404 stubs, (c) DELETE `reference-only/camel-paper/` (which is now on main and load-bearing for `research/followup/08`).

Verdict: ✅ safe to delete (no unique value) — and ❌ NOT safe to merge.

**`claude/audit-cleanup`** — 2 commits ahead. Files NEW: 5 files in `retrospective/2026-05-13-02/` (the retrospective itself plus 4 sibling specs). Check: are they on main? `git ls-tree origin/main retrospective/2026-05-13-02` → empty. Unique-valuable: yes.

Verdict: ⚠️ has unique content. Offer to create `claude/retrospective-2026-05-13-02` with just the 5 files, commit, push.

After user accepted, PR #45 merged the retrospective; re-audit showed all 5 files now IDENTICAL on branch and main. Verdict flips to ✅ safe.

### Example 2 — simpler case: a single feature branch

Input: "is `claude/clarify-research-structure-G07Ne` safe to delete?"

```bash
git fetch origin
ahead=$(git rev-list --count origin/main..origin/claude/clarify-research-structure-G07Ne)
# Suppose ahead=0
```

If 0 ahead: ✅ safe (tip reachable from main; squash-merge or direct-merge completed).

If >0 ahead: examine the commits — were they merged via different commit hashes (e.g. squash-merge produces a new commit on main but the branch's individual commits don't appear)? Compare the branch's net file changes against main file-by-file (workflow step 4).

## Anti-patterns

- **Trusting diff-stat alone.** A diff-stat of "30 files changed, 507 insertions, 12094 deletions" tells you nothing about WHICH files matter. The session encountered this with `claude/drain-issue36-extras` — the headline numbers looked like normal cleanup work; the actual diff would have been destructive.
- **Trusting `git rev-list --count A..B == 0` as equivalence.** It means B's tip is on A; it does NOT mean B and A have identical content. Stale-base branches can show 0 ahead and still have content differences. Always also check the file diff.
- **Auto-deleting branches in bulk.** Even "safe to delete" branches deserve one-final-look at the verdict. The cost of a `git push origin :branch-name` is irreversible (for the branch object; reflogs may help locally but not the remote).
- **Assuming a "fix" commit's message describes the actual diff.** Commit messages are aspirational; diffs are factual. (Session: `claude/drain-issue36-extras` claimed to "fix report 07 source table" but the fix was already on main and the branch's actual effect was destructive.)
- **Skipping the post-merge re-audit.** After a preservation PR merges, re-run the audit on the source branch to confirm its content is now byte-identical on main. Only then flip ⚠️ → ✅.

## Acceptance criteria

1. Each non-`main` remote branch receives one of three verdicts: ✅ safe, ⚠️ has unique, ❌ would-destroy-if-merged.
2. Each ⚠️ branch has a named preservation path (cherry-pick to which branch, or which specific files to extract).
3. Each ❌ branch has a one-paragraph explanation of WHAT would be destroyed.
4. No branch is recommended for deletion based on `git rev-list --count` alone; every verdict has a file-level basis.
5. The audit reports the actual git commands and outputs used, so the user can re-verify.

## Files this skill creates / modifies

- **Reads only**: git history (`git log`, `git diff`, `git show`, `git ls-tree`, `git rev-list`).
- **May create**: a preservation branch (`claude/preserve-<source-slug>-<date>`) when unique content needs to be saved before deletion.
- **Does not modify**: any existing files or branches (deletion is the user's call, not the skill's).
