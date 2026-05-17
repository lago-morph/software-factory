# Spec: `stacked-pr-on-feature-branch`

## Intent

When a piece of work logically depends on an unmerged PR but is itself complete and reviewable, the standard "wait for the parent to merge before opening the child" pattern adds latency and review friction. GitHub supports a cleaner alternative: open the child PR against the parent's branch instead of `main`. When the parent merges, GitHub auto-updates the child's base to `main`, and the child's diff narrows to just its own changes. This skill documents the workflow so future sessions don't reflexively wait or reflexively rebase.

Pattern emerged from PR #80 → PR #81 in the `software-factory` project: PR #81 (drain orchestrator) genuinely needed the catalog data structure that PR #80 (migration) introduced. Branching PR #81 off `claude/migrate-source-dedup` and targeting it kept PR #81's diff clean to just `drain.py + tests` without waiting for PR #80 to land.

## Trigger

Use when:
- Current work depends on code in an open, not-yet-merged PR
- The dependency is structural (imports, file paths, schema) not just informational
- Both PRs will eventually need to merge; neither is exploratory

Do NOT use when:
- Work is independent and only happens to be in the same area
- The parent PR is likely to undergo major review changes (child would need expensive rebases)
- You're not sure whether the parent will merge at all

## Inputs

- The parent PR's branch name and number
- A clear scope for the child PR (what's in it that isn't already in the parent)

## Outputs

- A new branch off the parent's branch
- A PR targeting the parent's branch (not main)
- Documentation of the stacking in the PR body so the reviewer doesn't get confused

## Workflow

1. **Verify the parent's branch is currently checked out**:
   ```bash
   git checkout claude/parent-branch-name
   ```
2. **Create child branch off parent**:
   ```bash
   git checkout -b claude/child-branch-name
   ```
3. **Do the work, commit, push**:
   ```bash
   git push -u origin claude/child-branch-name
   ```
4. **Open PR with `base` set to the parent's branch**:
   ```python
   mcp__github__create_pull_request(
       base="claude/parent-branch-name",   # NOT "main"
       head="claude/child-branch-name",
       title="PR #N: <scope>",
       body="""
       ## Summary
       <what's new>

       **Targets `claude/parent-branch-name`** (PR #<parent>'s branch) so the diff
       only shows this PR's work. Once PR #<parent> merges to main, GitHub will
       auto-update this PR's base to main and the diff will narrow further.
       """,
       ...
   )
   ```
5. **Verify PR diff is clean** — should show only the child's commits, not the parent's.
6. **When parent merges to main**: GitHub auto-updates the child's base to main. **No manual rebase needed.** Verify via the PR's "base" field in the API.
7. **If the parent's branch gets force-pushed** (e.g., user requests changes that require rewrites): `git rebase claude/parent-branch-name` on the child, resolve conflicts (typically none if the child added new files), `git push --force-with-lease`.

## Concrete examples

### Example 1: Drain orchestrator depending on catalog migration

- PR #80 (parent): migrates `source-dedup.md` → `reference-only/sources.json`. Branch `claude/migrate-source-dedup`.
- PR #81 (child): adds `drain.py` that reads the new `sources.json` schema. Branch `claude/drain-orchestrator` off `claude/migrate-source-dedup`, targeting that branch.

When PR #80 merged:
- PR #81's base auto-updated from `claude/migrate-source-dedup` → `main`
- PR #81's diff narrowed from "drain.py + everything PR #80 added" to "just drain.py + tests + report-conventions doc"
- No `git rebase` was needed on PR #81's branch

### Example 2: Recovery when the parent is force-pushed

PR #80 had to be force-pushed twice (user feedback uncovered a silent data-drop bug, then asked for noise filtering). PR #81 needed to track those changes:

```bash
git checkout claude/drain-orchestrator
git fetch origin claude/migrate-source-dedup
git rebase origin/claude/migrate-source-dedup
# Resolve conflicts on shared files (sources.json) by taking the parent's version
git checkout origin/claude/migrate-source-dedup -- reference-only/sources.json reference-only/sources.md
git add reference-only/sources.json reference-only/sources.md
git rebase --continue
git push --force-with-lease
```

## Anti-patterns

- **Targeting `main` "to be safe"** — the diff will then include all of the parent's commits, making review confusing.
- **Cherry-picking the parent's commits into the child branch** — duplicates them; when the parent merges, the child's PR will show those same commits as "already in main" and look weird.
- **Waiting for the parent to merge before opening the child** — adds latency; the child's review can proceed in parallel.
- **Force-pushing the parent without telling the child's reviewer** — if both PRs have reviewers, communicate. Child's diff will change when parent changes.
- **Stacking 3+ levels deep** — review burden becomes unmanageable. If you have A → B → C, consider whether B and C can merge into A.

## Acceptance criteria

1. Child PR's diff shows only the child's commits when viewed on GitHub.
2. Child PR's base automatically tracks main when parent merges.
3. No manual rebase needed unless parent was force-pushed.
4. PR body explicitly documents the stacking so reviewers aren't confused.
5. The skill's recovery procedure (rebase + force-push) works when the parent changes.

## Files this skill creates / modifies

Nothing beyond the standard PR workflow. This skill is procedural — it changes which `base` value gets passed to `mcp__github__create_pull_request` and documents the recovery pattern.
