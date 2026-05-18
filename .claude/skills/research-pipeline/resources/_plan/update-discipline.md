# PLAN.md update discipline

Every catalog mutation belongs in the same commit as a `research/PLAN.md` edit. This is hard rule #10 in `SKILL.md`. The check is mechanical (`check-plan-consistency.py` looks at git history and flags catalog-touching commits that left PLAN.md alone). This doc says **what** the edit should look like.

## What counts as "a catalog mutation"

Any of:

- `drain.py` run that produced new records or attached files to existing ones
- A manual jq edit to `reference-only/sources.json` (titles, tags, `pointer_to`, etc.)
- A new file landing in `reference-only/<id>/` directly (reconcile-source-dir.py)
- Catalog renaming or refactoring (rare, but counts)

Read-only operations (query.md, audit-records.py, lint-sources.sh on its own) do **not** require a PLAN.md edit.

## Minimum footprint — a new Session bullet

Every catalog-mutating commit gets at least a Session bullet under §1 (Current state TL;DR). The bullet replaces nothing — it accretes. Template:

```markdown
- **Session YYYY-MM-DD — <one-line topic>** — <one to three sentences describing the change>. <Important records added by id>. <Anything follow-up-worthy>.
```

Concrete example (the Round-11 drain that landed in PR #93):

```markdown
- **Session 2026-05-17 — Round-11 manual drain (16 files; ingestion only, stage 5 deferred)** — User dropped 17 files into `research/manual/` (15 MHTML + 2 PDFs); one PDF shipped with a companion `URL of <name>.txt` because its bytes carry no URL metadata. Used this PR to teach extract_url.py the companion-URL pattern. **Drain output:** 5 new catalog records (...) + 11 attachments to existing records. Audit clean. **Outstanding for follow-up:** README.md skip-list, PDF /URL annotation ordering, MIME-encoded MHTML titles, stage 5 deferred.
```

## When to do MORE than the minimum

Bump `**Version:** vX.Y (YYYY-MM-DD)` on the second line if **any** of these are true for the work in the PR:

- It's a new drain round (Round-N)
- It introduces a new failure mode (F-number)
- It promotes a report from 🟡 partial to ✅ FULL
- It changes the §3 bottleneck list, §4 fetch-priority list, or §5 work-remaining list
- It removes or relocates a section of the file

Also add an `**Earlier versions:**` paragraph line summarising the new version, **after** the existing earlier-versions paragraph.

Add a §10 lookup-table row when, **and only when**, this PR completes a numbered drain round (a row identifies "where did the work of this round live?", which means the round is over). Template:

```markdown
| N | Round name | Status | One-sentence summary + links. |
```

Statuses we've used: `✅ Complete`, `🟡 Ingestion complete, stage 5 deferred`, `🟡 Partial`.

## When NOT to bump the Version

- Trivial typo fixes
- Filling in titles or tags on already-existing records when the underlying drain bullet is already in place
- Refactoring of `plan-sync.md` or another non-PLAN file

In these cases the Session bullet alone is enough.

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
