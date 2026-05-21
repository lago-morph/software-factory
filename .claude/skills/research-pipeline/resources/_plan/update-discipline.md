# PLAN.md update discipline

Every catalog mutation belongs in the same commit as a `research/PLAN.md` edit. This is hard rule #10 in `SKILL.md`. The check is mechanical (`check-plan-consistency.py` looks at git history and flags catalog-touching commits that left PLAN.md alone). This doc says **what** the edit should look like.

## What counts as "a catalog mutation"

Any of:

- `drain.py` run that produced new records or attached files to existing ones
- A manual jq edit to `reference-only/sources.json` (titles, tags, `pointer_to`, etc.)
- A new file landing in `reference-only/<id>/` directly (reconcile-source-dir.py)
- Catalog renaming or refactoring (rare, but counts)

Read-only operations (query.md, audit-records.py, lint-sources.sh on its own) do **not** require a PLAN.md edit.

## Session bullet format

Every catalog-mutating commit gets one Session bullet under §1. Strictest possible short form — three components only: date + 24-hour time, the run's short name, the PR link. No prose, no semicolons-as-cheat, no content summary.

Template:

```markdown
- **YYYY-MM-DD HH:MM <short-name>** [#nn](https://github.com/lago-morph/software-factory/pull/nn)
```

Example:

```markdown
- **2026-05-17 18:42 Round-11 manual drain** [#93](https://github.com/lago-morph/software-factory/pull/93)
```

Hyperlink rules:
- PR link display = `#nn`
- Rare commit link display = `abcd1234` (first 8 hex), used only when the commit message carries info not in the PR description
- Time comes from the merge-commit timestamp

The bullet says when it happened, what it was, and where to read about it. Anyone who needs the content reads the PR. Same format applies always — no tiers, no version bumps, no earlier-versions paragraph.

## §10 lookup-table row

Add a §10 lookup-table row when, **and only when**, this PR completes a numbered drain round (a row identifies "where did the work of this round live?", which means the round is over). One sentence + PR/commit hyperlinks — no prose summary of contents. Template:

```markdown
| N | Round name | ✅ Complete | One sentence + [#nn](https://github.com/lago-morph/software-factory/pull/nn). |
```

## Running the consistency check before commit

```bash
python .claude/skills/research-pipeline/scripts/check-plan-consistency.py
```

This is also called by `lint-sources.sh`. By default `lint-sources.sh` treats consistency findings as advisory warnings (exit 0); the `--strict` CI run elevates them to hard fails.

If the check flags a recent catalog commit that didn't touch PLAN.md, you have three options:

1. **Add a retro-bullet now** — write the Session bullet for that historical commit in this PR (the user, and any auditor, would rather see late-but-present than absent).
2. **Author a back-fill PR** — touch only PLAN.md, no catalog changes; reference the orphan commits by SHA in the bullet body.
3. **Suppress this one specifically** — only if the orphan commit was intentionally PLAN-irrelevant (e.g., a no-op rename). Drop a one-line comment in the PR description explaining why, and move on. The script will keep flagging it; that's expected.

## Why this is hard rule #10

The catalog is canonical for "what sources we have"; PLAN.md is canonical for "what we've done with them". Drift between the two means readers (and future-you) can't trust either as a complete record. PLAN.md is the only place the *narrative* of corpus growth lives, and the corpus is by design only useful if you can find your way around it.
