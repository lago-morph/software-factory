---
name: stacked-pr-on-feature-branch
description: Open a child PR targeting a parent's branch (not main) when current work logically depends on the parent's unmerged changes. GitHub auto-updates the child's base to main when the parent merges, keeping the child's diff narrow throughout review. Use when you're working on a PR that imports from / references / extends an open unmerged PR — instead of waiting for the parent to merge. Triggers on phrases like "this depends on PR #N", "stack on top of", "build on the open PR", or proactively when about to branch off main for work that won't compile without an open parent PR's changes.
tags: [git, github, pr, workflow]
allowed-tools: [Bash, mcp__github__create_pull_request]
---

# stacked-pr-on-feature-branch

When new work logically depends on an open, unmerged PR (uses its files, references its APIs, extends its schema), the standard "wait for parent to merge before starting" pattern adds avoidable latency. GitHub natively supports stacked PRs via cross-branch targeting; this skill is the procedure.

## When to use

Use when:
- Current work imports, references, or structurally depends on code in an open unmerged PR.
- The dependency is real (compilation/schema/API), not just informational.
- Both PRs will eventually need to merge; neither is exploratory.

Do NOT use when:
- Work is independent and only happens to be in the same area.
- The parent PR is likely to undergo major review changes (child would need expensive rebases).
- You're stacking 3+ levels deep (review becomes unmanageable).

## The workflow

### 1. Branch off the parent

```bash
# Make sure parent's branch is current
git fetch origin <parent-branch>
git checkout <parent-branch>
git pull --ff-only

# Create child branch
git checkout -b claude/<child-name>
```

### 2. Do the work, commit, push

```bash
# Work happens normally
git add <files>
git commit -m "..."
git push -u origin claude/<child-name>
```

### 3. Open PR targeting the parent's branch

```python
mcp__github__create_pull_request(
    base="<parent-branch>",      # NOT "main"
    head="claude/<child-name>",
    title="PR #N: <scope>",
    body="""
## Summary

<what's new in THIS PR (the child)>

**Targets `<parent-branch>`** (PR #<parent-number>) so this PR's diff
only shows the child's work. When PR #<parent-number> merges to main,
GitHub will auto-update this PR's base to main.

<rest of body>
""",
    draft=False,
    owner="...",
    repo="...",
)
```

### 4. Verify the diff is narrow

In the GitHub UI, the PR should show only the child's commits — not the parent's. If the diff includes the parent's changes, the base was set wrong; close the PR and recreate with the correct base.

### 5. When the parent merges

**No action needed.** GitHub auto-updates the child PR's base from the parent's branch to `main`. The child's diff narrows further (any shared files in the parent now appear as "already in main" instead of "in the child's diff").

Verify via the API or the PR's "base" field in the UI.

### 6. Recovery: parent gets force-pushed

If the parent receives post-review changes that require force-pushing (e.g., user feedback uncovers a bug; user requests scope changes), the child needs to rebase:

```bash
git checkout claude/<child-name>
git fetch origin <parent-branch>
git rebase origin/<parent-branch>

# Conflicts on files the parent also touched are normal; take parent's version:
git checkout origin/<parent-branch> -- <conflicted-file>
git add <conflicted-file>
git rebase --continue

git push --force-with-lease
```

The child PR's diff updates automatically on GitHub after the push.

### 7. Recovery: parent is closed without merging

The child PR is now invalid — its base branch will never reach main. Two options:

1. **Rebase onto main** if the parent's work was duplicated elsewhere or its scope absorbed into another PR:
   ```bash
   git rebase --onto main <parent-branch> claude/<child-name>
   git push --force-with-lease
   # Update child PR's base to main via mcp__github__update_pull_request(base="main", ...)
   ```

2. **Close and start over** if the parent was rejected because the approach was wrong (which probably invalidates the child too).

## Concrete examples

### Example 1: drain orchestrator on top of catalog migration

This session's canonical example:
- PR #80 (parent): migrates `source-dedup.md` → `reference-only/sources.json`. Branch `claude/migrate-source-dedup`.
- PR #81 (child): adds `drain.py` that reads the new `sources.json` schema. Branch `claude/drain-orchestrator` off `claude/migrate-source-dedup`, targeting that branch.

When PR #80 merged, PR #81's base auto-updated to main. The child's diff went from "drain.py + everything in #80" to just "drain.py + tests + report-conventions doc."

### Example 2: stacked PRs through a refactor sequence

When tackling a multi-step refactor:
- PR A: introduces a new schema. Branch `claude/schema-v2`.
- PR B: migrates data to new schema. Branch `claude/migrate-to-v2` off A, targeting A.
- PR C: removes old schema support. Branch `claude/remove-v1` off B, targeting B.

A merges → B's base auto-becomes main. B merges → C's base auto-becomes main. The three PRs reviewed in parallel; merge order is enforced by the base chain.

Note: 3 levels is roughly the practical limit. Beyond that, reviewers lose track.

## Anti-patterns

- **Targeting `main` to be safe** — defeats the point. The child's diff will include all of the parent's commits, making review confusing.
- **Cherry-picking parent's commits into child** — duplicates them. When parent merges, the child's PR shows those commits as already-in-main but the SHA differs; weird visual + may cause cherry-pick conflicts later.
- **Stacking 4+ levels** — review burden becomes unmanageable; reviewers can't track the dependency chain.
- **Force-pushing the parent without warning child's reviewer** — if both PRs have separate reviewers, communicate.
- **Forgetting to update the child's PR body description** when scope changes — leave the "targets X" note in sync with reality.
- **Opening child PR before the parent's branch is pushed** — `mcp__github__create_pull_request(base="<branch>")` will fail because the branch doesn't exist on origin. Always push parent first.

## Acceptance criteria

1. Child PR's "base" field on GitHub shows the parent's branch (not main) until the parent merges.
2. Child PR's diff shows only the child's commits when viewed on GitHub.
3. PR body explicitly documents the stacking so reviewers aren't surprised.
4. When parent merges, child's base auto-updates to main (verify in the UI or API).
5. Recovery procedure (rebase + force-push) works without losing child commits.

## Files this skill creates / modifies

This skill is procedural — it doesn't create files. It changes which `base` value gets passed to `mcp__github__create_pull_request` and documents the recovery pattern.

## See also

- [ADR 0008 — stacked PR pattern](../../../retrospective/2026-05-17-85/ADR-0008-stacked-pr-pattern.md) — design rationale
- [`always-commit-skill-to-repo`](../always-commit-skill-to-repo/SKILL.md) — the broader git/PR discipline this works within
