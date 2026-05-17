# Drain pipeline — overview

The drain pipeline ingests material from ingestion drop directories (`research/manual/`, `research/fetched/`) into the source catalog and then folds extracted content into research reports.

## Stages

| Stage | Purpose | Doc |
|---|---|---|
| 1 | Inventory uningested files | `stage-1-inventory.md` |
| 2 | Reverse-engineer URLs from file content | `stage-2-url-extract.md` |
| 3 | Update the catalog (create/update records, move files) | `stage-3-catalog-update.md` |
| 4 | Validate the resulting catalog before any further work | `stage-4-validation.md` |
| 5 | Extract content from registered sources into reports | `stage-5-content-processing.md` |

Sub-step: image summarization for newly-registered images — see `image-summarization.md`.

## Key principle

**Cataloging is the act of ingestion.** Old drain workflows treated raw files as the input to report-writing, which led to mismatches (filename-says-X, content-is-Y). The new pipeline:

1. Identifies the source's URL first (or trusts directory placement)
2. Registers it in the catalog with a stable id
3. Only then extracts content from the *registered* source into reports

This means content extraction (stage 5) operates on record IDs, not file paths. The same record's content can be re-extracted into multiple reports without re-processing the file.

## When to run the drain

Triggers:
- User says "drain", "process new content", or "ingest"
- Phase 0 check (every skill invocation) reveals uningested files
- After dropping new files into `research/manual/` or `research/fetched/`

Don't auto-run on every skill invocation. Surface the inventory and let the user say "go".

## High-level recipe

```bash
# Stage 1: Inventory
find research/manual research/fetched -type f \
  \( -name '*.html' -o -name '*.mhtml' -o -name '*.md' -o -name '*.txt' \
  -o -name '*.pdf' -o -name '*.ipynb' \) > /tmp/uningested.txt

# Stage 2: For each file, extract URL (per format rules)
# Stage 3: For each (file, URL) pair, create/update record + move file
# Stage 4: bash scripts/lint-sources.sh — fix any errors
# Stage 5: Process catalog content into reports
```

The actual implementation is in PR #81 — this PR (#79) ships the infrastructure that the drain depends on (the scripts, the schema, the catalog format). The drain rewrite itself happens once PR #80 (data migration) lands.

## Until PR #81 lands

The old SKILL.md (preserved as `SKILL.old.md` for one PR cycle) describes the pre-catalog drain. You can still run that old flow if needed, but every file it produces should be reconciled into the catalog afterward via:

```bash
python scripts/reconcile-source-dir.py --all
```

## Failure modes

- **URL extraction fails** for a file in an ingestion drop dir → file stays where it is, reported as an error. Move the file to `reference-only/<id>/` manually if you know what record it belongs to (then reconciler picks it up).
- **URL extraction succeeds but file is malformed** → catalog gets the record but the file's `completeness` becomes `error`. Re-fetch via fetch-blocked-urls workflow.
- **Catalog validation fails after stage 3** → drain halts. Fix the validation errors before stage 5.
- **A drained file is later found to have wrong content** → set the record's `pointer_to` to a new record with the correct URL; keep the old record for back-references.
