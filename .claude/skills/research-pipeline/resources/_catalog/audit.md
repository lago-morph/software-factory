# Post-ingestion audit

`scripts/audit-records.py` runs a record-scoped mechanical checklist over a
specific set of record IDs. It's distinct from `lint-sources.sh` (whole-catalog,
runs pre-commit) in two ways:

1. **Scope** — audit only inspects record IDs you pass; lint inspects everything.
2. **Intent** — audit's findings are a *signal that drain is missing a step*.
   When `drain.py` produces a record that fails the audit, the fix is usually
   to extend drain.py to produce records that pass the check, not just patch
   the one record by hand.

## When it runs

`drain.py` calls audit on every record it touched in a run. Behavior is
governed by the `audit_after_ingestion` knob in SKILL.md's YAML config:

| Value | When audit runs after drain |
|---|---|
| `always` (default) | Every run with ≥ 1 touched record. Drain's summary appends a footer telling the user the knob's filename so they can flip it. |
| `sometimes` | Only when drain materially changed disk state (new have-files attached, new records created, orphans reconciled). Pure URL-list expansion is skipped. |
| `never` | Skip entirely. The drain summary notes the skip so it's not invisible. |

You can also override per-invocation:

```bash
python scripts/drain.py --audit-mode never    # one-off skip
python scripts/drain.py --no-audit            # equivalent
python scripts/drain.py --audit-mode always   # force even if config says never
```

## Running it directly

```bash
# Audit one record
python scripts/audit-records.py 0a7f3b8e21

# Audit several
python scripts/audit-records.py 0a7f3b8e21 1bc2d3e4f5

# Audit the entire catalog (CI gate use case)
python scripts/audit-records.py --all

# JSON output for tooling
python scripts/audit-records.py --all --json
```

Exit codes: `0` clean, `1` findings, `2` could not load catalog.

## The 12 checks (today)

| # | Check | Drain hook that produces passing records |
|---|---|---|
| 1 | `title-not-placeholder` | drain extracts title from file content via `extract_title.py` |
| 2 | `has-canonical-url` | drain only ingests files with extractable URLs (or via known `<id>/` dirs) |
| 3 | `url-is-canonical` | drain canonicalizes via `url_canonicalize.py` before computing id |
| 4 | `id-derivation` | drain derives id = `sha256(canonical_url)[:10]` |
| 5 | `has-files` | drain attaches a file entry for every ingested file |
| 6 | `file-on-disk` | drain `git mv`s files into `reference-only/<id>/` |
| 7 | `file-sha256-matches` | drain computes sha256 from file content during ingestion |
| 8 | `format-matches-extension` | drain maps extension → format via `EXT_TO_FORMAT` |
| 9 | `has-category-tag` | **not yet automated** — agent assigns tags from `category-taxonomy.md` |
| 10 | `pointer-chain-ok` | only created manually when retiring a record |
| 11 | `fetch-provenance-ok` | drain doesn't set fetch_provenance directly — that's the fetch-blocked-urls skill |
| 12 | `image-has-summary` | **not yet automated** — agent populates `files[].comment` post-drain |

The "not yet automated" rows are the open audit-driven gaps. When you next
work on drain, those are the next planned upgrades. If you find a NEW check
that should exist, add it to `audit-records.py` AND add the corresponding
drain step at the same time — never just one.

## Adding a new check

1. Add the check function inside `audit_record()` in `audit-records.py`.
   Use a short, hyphenated check name like `has-bibliographic-year`.
2. Decide if drain should produce records that satisfy it automatically:
   - If yes: extend `drain.py` (typically `stage_2_3_per_file`) to populate
     the field. Update `resources/_drain/stage-*.md` to document the step.
   - If no (it's a manual data-quality check): add a row to the table above
     marking it "agent populates after drain", and document the workflow in
     the relevant `_catalog/*.md`.
3. Add a unit test in `tests/unit/test_audit_records.py`.
4. Run a sample drain locally and confirm the audit passes on freshly-drained
   records.

## Why findings are warnings, not errors

`drain.py` exit code reflects `lint-sources.sh` only. Audit findings print to
the drain summary but do NOT fail the run. Rationale:

- Lint enforces *current* invariants (schema, fs consistency, ref bidirectional).
  Violating those is a defect — must be fixed before commit.
- Audit raises *aspirational* invariants ("every record should have a category
  tag"). Many of those can't be auto-populated by drain yet; some require
  human judgment (image summaries). If audit failures blocked drain, you'd
  never be able to drain anything until every aspirational check was automated.

The contract: audit findings are **a TODO list for either the records or for
drain.py**, surfaced where the agent will see them.

## See also

- `scripts/audit-records.py` — the script itself
- `scripts/drain.py` — Stage 4b is the audit invocation
- `resources/_catalog/category-taxonomy.md` — the 15 canonical tags
- `resources/_catalog/validation.md` — `lint-sources.sh` walkthrough
