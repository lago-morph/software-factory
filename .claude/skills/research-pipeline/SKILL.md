---
name: research-pipeline
description: Manage a structured research source catalog and the drain pipeline that feeds it. Use this skill whenever the user asks to (a) add a new source / URL / file to the library, (b) query what we have on a topic, (c) "drain", "process", or "ingest" content from research/manual/ or research/fetched/, (d) write or extend a research report that needs source-status traceability, (e) reconcile manual file drops into reference-only/<id>/ directories. Also runs Phase 0 (inventory uningested files) on every invocation so a fresh session never misses pending work.
---

# research-pipeline

This skill owns the **canonical source catalog** (`reference-only/sources.json`) and the **drain pipeline** that populates it from incoming research material. Every source the project has ever cited or wants to cite is tracked here as a record with a stable 10-character ID. Files for each source live at `reference-only/<id>/<filename>`. Research reports cite sources by URL; the catalog provides URL ↔ files ↔ reports traceability.

## Configuration

Scripts and resources reference paths via the YAML block below. **Do not edit the sentinels.** Use `python scripts/validate-config.py` after any edit.

<!-- BEGIN PIPELINE CONFIG -->
```yaml
skill_path:   .claude/skills/research-pipeline
library_path: reference-only
schema_path:  reference-only/sources.schema.json
data_path:    reference-only/sources.json
md_path:      reference-only/sources.md
trigger_path: reference-only/.regen-trigger
report_paths:
  - research
  - research/followup
ingestion_paths:
  - research/manual
  - research/fetched
github:
  owner: lago-morph
  repo:  software-factory
  fetch_branch_prefix: fetched/issue-
  fetch_issue_label:   fetch-urls
```
<!-- END PIPELINE CONFIG -->

If anything in this config looks off — paths that don't exist, owner/repo wrong for this repo, syntax that won't parse cleanly — run `python .claude/skills/research-pipeline/scripts/validate-config.py` before doing anything else. If it fails, surface the failure to the user and stop. Do not proceed with operations on a misconfigured pipeline.

## Pre-flight check (run this first, every invocation)

Before any catalog or drain operation:

```bash
ls .github/workflows/regen-sources-md-auto.yml \
   .github/workflows/regen-sources-md-manual.yml \
   .github/workflows/test-research-pipeline.yml 2>/dev/null | wc -l
```

If the count is less than 3, the pipeline workflows aren't installed. Ask the user: *"Pipeline workflows aren't installed in `.github/workflows/`. Install them now? (y/N)"*. On yes, run:

```bash
python .claude/skills/research-pipeline/scripts/install-workflows.py
```

On no, abort the current operation — the pipeline can't run safely without auto-regeneration of `sources.md`.

## Decision tree — load the right resource for the job

| You're about to... | Read |
|---|---|
| Add a new source / URL / file to the catalog | `resources/_catalog/edit.md` |
| Edit any field on an existing record | `resources/_catalog/edit.md` |
| Look up data on a source without changing anything | `resources/_catalog/query.md` |
| Bootstrap a fresh catalog (`sources.json` doesn't exist or is `{}`) | `resources/_catalog/bootstrap.md` |
| Add multiple files to an existing record's directory | `resources/_catalog/manual-additions.md` |
| Run the drain pipeline (process `research/manual/` or `research/fetched/`) | `resources/_drain/workflow-overview.md` |
| Write a new research report or extend one | `resources/_drain/stage-5-content-processing.md` |
| Modify any script under `scripts/` | `resources/testing.md` |
| Install or update the pipeline workflows | `resources/github-action.md` |
| Investigate a linter failure | `resources/_catalog/validation.md` |
| Investigate a URL-vs-reports mismatch | `resources/reference-audit.md` |

Each resource doc is self-contained for its task. Loading two or three is normal; loading all of them at once is wasteful and noisy.

## Hard rules (always apply)

1. **Never edit `sources.json` with `Edit` or `Write` directly.** All changes go through `jq` transformations piped to a temp file then `mv`-replaced. See `resources/_catalog/edit.md` for the safe patterns.
2. **Always re-normalize after editing.** `jq -S 'to_entries | sort_by(.key) | from_entries' /tmp/new.json > reference-only/sources.json`. Sort keys, sort by id, pretty-print. This keeps diffs minimal.
3. **Always run `bash scripts/lint-sources.sh` before staging.** It runs schema validation + reference audit + filesystem audit + fetch-provenance audit + record sanity checks. Fix all errors before committing.
4. **Record IDs are derived, not invented.** ID = `sha256(canonical_url)[:10]` after canonicalization (see `resources/_catalog/schema-reference.md`). Use `python scripts/url_canonicalize.py <url>` to compute.
5. **Never delete a record.** To retire one, set its `pointer_to` field to its replacement record's id. Deletion would break references from reports and pointers from other records.
6. **Files belong in `reference-only/<id>/`.** The directory IS the source identity. A file dropped into a record's directory is reconciled by id, not by content. Exceptions go in `files[].location` overrides.
7. **A file with no extractable URL is fine IF it's in a known `<id>/` directory.** Directory placement substitutes for URL extraction. Files in ingestion drop directories WITHOUT a URL ARE flagged.
8. **The `.regen-trigger` file is for debugging.** Normal operation uses the auto-regen workflow that fires on `sources.json` changes on `main`. The trigger file is the manual escape hatch when something goes wrong.

## Phase 0 — inventory pending work (run on every invocation)

Even if the user asked you to do something specific, scan first:

```bash
# What's sitting in ingestion drop dirs?
find research/manual research/fetched -type f \
  \( -name '*.html' -o -name '*.mhtml' -o -name '*.md' -o -name '*.txt' \
  -o -name '*.pdf' -o -name '*.ipynb' \) 2>/dev/null | head -50

# What files are sitting in reference-only/<id>/ dirs but not in any record's files[]?
python .claude/skills/research-pipeline/scripts/check-source-dirs.py 2>&1 | grep "not registered" | head -20
```

If either list has content, mention it to the user before starting their requested work — they may want to drain first. Don't auto-drain unless they ask.

## Common entry points

| User says... | Skill response |
|---|---|
| "drain" / "process new content" / "ingest" | Load `resources/_drain/workflow-overview.md`, run the 5-stage pipeline. |
| "what do we have on X?" | Load `resources/_catalog/query.md`, run the right jq query. |
| "add this URL to track" | Load `resources/_catalog/edit.md`, create a wanted record. |
| "I dropped some files into reference-only/0a7f3b8e/" | Load `resources/_catalog/manual-additions.md`, run reconcile-source-dir.py. |
| "build me an INDEX of the sources" | The MD is auto-generated. Trigger it with the `.regen-trigger` file or wait for the auto-workflow. |
| "the linter is failing" | Load `resources/_catalog/validation.md`, walk the specific error. |
| "find references to URL X that aren't in the catalog" | Load `resources/reference-audit.md`, run check-source-refs.py. |
| "research [topic]" | Load `resources/_drain/workflow-overview.md` AND start a new report following `resources/_drain/stage-5-content-processing.md`. |

## What this skill no longer does (legacy notes)

Earlier versions of this skill embedded the drain workflow directly in this SKILL.md (~669 lines). That content has moved into `resources/_drain/*` for progressive disclosure. The original `SKILL.old.md` is preserved alongside this file for one PR cycle so the drain-rewrite PR (PR #81) can verify nothing was lost; it gets deleted then.

The fetch-blocked-urls infrastructure is delegated to the [fetch-blocked-urls](../fetch-blocked-urls/SKILL.md) skill, which this skill calls when a record needs a URL fetched from the GitHub Actions runner.

## Where to read more

- **`resources/_catalog/schema-reference.md`** — field-by-field semantics, value sets, gotchas
- **`resources/_catalog/jq-recipes.md`** — copy-pasteable jq for every common operation
- **`resources/_drain/workflow-overview.md`** — the 5-stage drain pipeline
- **`resources/testing.md`** — running the unit + integration test suite
- **`resources/github-action.md`** — the auto-regen and manual-tickle workflows
