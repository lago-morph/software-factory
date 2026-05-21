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
plan_path:    research/PLAN.md
trigger_path: reference-only/.regen-trigger
report_paths:
  - research
  - research/followup
ingestion_paths:
  - research/manual
github:
  owner: lago-morph
  repo:  software-factory
  fetch_branch_prefix: fetched/issue-
  fetch_issue_label:   fetch-urls

# When to run scripts/audit-records.py against records the drain pipeline
# touched. The audit is a record-scoped mechanical checklist (file existence,
# sha256, title-not-placeholder, category tag presence, format-ext match,
# canonical URL round-trip, pointer chain integrity, fetch_provenance hygiene).
#
#   always    — audit after every drain run on every touched record. Default.
#   sometimes — audit only when a touched record changed status (e.g., wanted
#               → have). Cheaper for large bulk drains.
#   never     — skip the audit. Use only if you accept the risk of latent
#               record defects. The user can re-enable any time.
#
# When mode is `always`, the drain output includes a one-line reminder telling
# the user where this knob lives so they can flip it without grepping.
audit_after_ingestion: always

# URLs matching these regex patterns are "casual mentions" — `check-source-refs.py`
# skips them when verifying that every cited URL has a catalog record. Use for
# things like social-media profiles, video links, app store entries, and tool
# homepages that get name-checked in reports without being substantive sources
# worth cataloguing. Each pattern is a Python regex (anchored at start of URL).
casual_url_patterns:
  - 'https?://x\.com/'
  - 'https?://twitter\.com/'
  - 'https?://(www\.)?youtube\.com/'
  - 'https?://youtu\.be/'
  - 'https?://(www\.)?linkedin\.com/'
  - 'https?://(www\.)?facebook\.com/'
  - 'https?://apps\.apple\.com/'
  - 'https?://play\.google\.com/'
  - 'https?://api\.github\.com/'
  # GitHub PR URLs used as audit-trail links inside plan docs
  - 'https?://github\.com/[^/]+/[^/]+/pull/\d+'
  # Pure homepage URLs (no path beyond /) — name-check mentions, not articles
  - 'https?://[^/]+/?$'
```
<!-- END PIPELINE CONFIG -->

If anything in this config looks off — paths that don't exist, owner/repo wrong for this repo, syntax that won't parse cleanly — run `python .claude/skills/research-pipeline/scripts/validate-config.py` before doing anything else. If it fails, surface the failure to the user and stop. Do not proceed with operations on a misconfigured pipeline.

## Pre-flight check (run this first, every invocation) — self-syncing

**The skill is self-syncing.** The canonical source for all workflow YAML is `resources/_workflows/` inside this skill directory. The copies that actually run (under `.github/workflows/`) are derived artifacts; they must always match the templates. If they don't, the skill's `install-workflows.py` regenerates them.

Before any catalog or drain operation:

```bash
python .claude/skills/research-pipeline/scripts/install-workflows.py --check
```

Exit code:
- `0` — all workflows installed and identical to templates. Proceed.
- `1` — at least one is missing OR drifted (template edited but `.github/workflows/` still has the old content). **Auto-fix by running, without asking the user:**
  ```bash
  python .claude/skills/research-pipeline/scripts/install-workflows.py --force
  ```
  Then continue with the user's request. The install script auto-commits with a clear message; push that commit alongside your other work.
- `2` — template file itself is missing from the skill. This is a skill-installation defect, not a workflow-drift issue. Surface to the user and stop.

**Do not ask the user before installing/syncing.** The install is mechanical and deterministic — every workflow is regenerated from a template, nothing custom is destroyed. The whole design contract is that copying the skill directory into a fresh repo is sufficient to bootstrap; the LLM enforces that contract by running `--force` on mismatch.

This same `--check` runs as a hard gate in CI for skill modifications (see `test-research-pipeline.yml`), so a template edit that doesn't propagate to `.github/workflows/` blocks the PR.

## Decision tree — load the right resource for the job

| You're about to... | Read |
|---|---|
| Add a new source / URL / file to the catalog | `resources/_catalog/edit.md` |
| Edit any field on an existing record | `resources/_catalog/edit.md` |
| Look up data on a source without changing anything | `resources/_catalog/query.md` |
| Bootstrap a fresh catalog (`sources.json` doesn't exist or is `{}`) | `resources/_catalog/bootstrap.md` |
| Add multiple files to an existing record's directory | `resources/_catalog/manual-additions.md` |
| Tag a record with one of the 15 canonical categories | `resources/_catalog/category-taxonomy.md` |
| Run the post-ingestion audit on specific records | `resources/_catalog/audit.md` |
| Run the drain pipeline (process `research/manual/` or `research/fetched/`) | `resources/_drain/workflow-overview.md` |
| Update `research/PLAN.md` after a drain or catalog mutation | `resources/_plan/update-discipline.md` |
| Audit `research/PLAN.md` for consistency with catalog + recent git history | `resources/_plan/audit.md` |
| Handle a YouTube video found embedded in an ingested document | `resources/_drain/youtube-transcripts.md` |
| Write a new research report or extend one | `resources/_drain/stage-5-content-processing.md` |
| Propose, name, or register a new failure mode (F-mode) | `resources/_drain/stage-5-content-processing.md` "Failure-mode discovery and registration" |
| Modify any script under `scripts/` | `resources/testing.md` |
| Install or update the pipeline workflows | `resources/github-action.md` |
| Investigate a linter failure | `resources/_catalog/validation.md` |
| Investigate a URL-vs-reports mismatch | `resources/reference-audit.md` |

Each resource doc is self-contained for its task. Loading two or three is normal; loading all of them at once is wasteful and noisy.

## Hard rules (always apply)

1. **Never edit `sources.json` with `Edit` or `Write` directly.** All changes go through `jq` transformations piped to a temp file then `mv`-replaced. See `resources/_catalog/edit.md` for the safe patterns.
2. **Always re-normalize after editing.** Hand-jq edits MUST end with `bash scripts/normalize-sources-json.sh reference-only/sources.json`. That script runs `jq -S '.'` in place atomically and is the **single source of truth** for what a normalized `sources.json` looks like on disk — every record's keys sorted alphabetically at every level, 2-space indent, UTF-8 preserved, trailing newline. `drain.py`'s `normalize_and_write` produces byte-identical output (verified in `tests/unit/test_normalize_sources.py`). The auto-regen workflow uses the same script. Never write a different normalization invocation inline — drift between tools is exactly what this rule prevents.
3. **Always run `bash scripts/lint-sources.sh` before staging.** It runs schema validation + reference audit + filesystem audit + fetch-provenance audit + record sanity checks. Fix all errors before committing.
4. **Record IDs are derived, not invented.** ID = `sha256(canonical_url)[:10]` after canonicalization (see `resources/_catalog/schema-reference.md`). Use `python scripts/url_canonicalize.py <url>` to compute.
5. **Never delete a record.** To retire one, set its `pointer_to` field to its replacement record's id. Deletion would break references from reports and pointers from other records.
6. **Files belong in `reference-only/<id>/`.** The directory IS the source identity. A file dropped into a record's directory is reconciled by id, not by content. Exceptions go in `files[].location` overrides.
7. **A file with no extractable URL is fine IF it's in a known `<id>/` directory.** Directory placement substitutes for URL extraction. Files in ingestion drop directories WITHOUT a URL ARE flagged.
8. **The `.regen-trigger` file is for debugging.** Normal operation uses the auto-regen workflow that fires on `sources.json` changes on `main`. The trigger file is the manual escape hatch when something goes wrong.
9. **Audit findings are a forward-thinking signal.** When `scripts/audit-records.py` flags an issue on a record drain just touched, either fix the record OR extend `drain.py` so the next ingestion produces records that satisfy the check. Don't bypass the audit; that defeats the loop. See `resources/_catalog/audit.md`.
10. **`/failure-modes.md` is the canonical index of failure modes.** Whenever a report proposes a new failure mode, register it in `/failure-modes.md` in the same commit. Renumber on collision; propagate the renumber to every reference (grep with word-boundary `\b`). Procedure: `resources/_drain/stage-5-content-processing.md` "Failure-mode discovery and registration".
11. **Every catalog mutation gets reflected in `research/PLAN.md` in the same commit.** Drain runs, manual additions, `pointer_to` retirements, title/tag fix-ups — anything that changes `reference-only/sources.json` or the file tree under it. The minimum acceptable footprint is a new `**Session YYYY-MM-DD — ...**` bullet under §1; bigger work (a new drain round) also gets a `**Version:**` bump and a §10 lookup-table row. See `resources/_plan/update-discipline.md` for the templates. `bash scripts/lint-sources.sh` includes `check-plan-consistency.py` as an advisory warning; `--strict` (CI) elevates it to a hard fail.

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
