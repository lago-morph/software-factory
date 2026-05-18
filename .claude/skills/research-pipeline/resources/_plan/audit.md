# PLAN.md consistency audit

The script `scripts/check-plan-consistency.py` flags drift between `research/PLAN.md` and the catalog. It's called as a warning step by `lint-sources.sh` and can be run on demand.

## What it checks

| # | Level | Check |
|---|---|---|
| 1 | error | The `**Version:** vX.Y (YYYY-MM-DD)` line exists in the first 4 KB and parses. |
| 2 | warn  | The most recent commit touching the catalog also touched PLAN.md. |
| 3 | warn  | In the last N commits touching the catalog (default 10), every one also touched PLAN.md. |
| 4 | warn  | The set of `Round-N` numbers named in session bullets matches the rows in the §10 lookup table. |
| 5 | info  | The Version-line date is not older than the most recent catalog commit. |

## CLI

```bash
# Default — exit 0 unless an `error` check fails
python .claude/skills/research-pipeline/scripts/check-plan-consistency.py

# CI gate — exit 2 on warnings as well
python .claude/skills/research-pipeline/scripts/check-plan-consistency.py --strict

# Tune the window for check #3 (default 10)
python .claude/skills/research-pipeline/scripts/check-plan-consistency.py --window 30
```

## Exit codes

| Code | Meaning |
|---|---|
| 0 | OK (any warnings printed but tolerated) |
| 1 | At least one `error` finding (structural defect in PLAN.md itself) |
| 2 | `--strict` and at least one `warn` finding |
| 3 | Could not invoke (missing PLAN.md, git not available, ...) |

## When `check #4` (round-consistency) trips

The script treats any `- **Session ...** ... Round N ...` bullet as evidence the round is mentioned, and any `| N | ... |` row inside §10 (the round-by-round lookup table) as evidence a row exists. Mismatches are usually one of:

- **Bullet without a row** — a drain round happened but §10 wasn't updated. Fix: add the row per `update-discipline.md`.
- **Row without a bullet** — usually a back-fill row whose Session line uses a different wording. Fix: ensure at least one session bullet references the round number explicitly (`Round-N`, `Round N`, or `round N`, case-insensitive).
- **Number outside §10** — the table-row regex is anchored to §10, so stray `| N |` rows elsewhere won't be miscounted. But a renumbering accident (e.g., changing column widths) can produce a row that looks like `| 10 |` when it's actually a different column; visually verify the §10 table when this trips.

## Limitations (deliberately not checked)

- Section-by-section content quality — the audit is structural, not editorial.
- Bullet-author identity — git author is preserved by commit history; PLAN.md tracks topic, not who.
- Whether the §3 / §5 / §6 lists have actually been updated for the corresponding work — would require deep content matching; out of scope for v1.

## Wiring into `lint-sources.sh`

The script runs at the end of `lint-sources.sh`. Its **non-zero warning** exit code is intentionally swallowed in the default lint flow so a single missed PLAN.md edit doesn't block unrelated catalog work. In CI (or when explicitly run with `--strict`), warnings escalate to failures.

## When to suppress a finding

The script does not support per-finding suppression. The right way to silence a recurring orphan-commit warning is to author the back-fill Session bullet for it (option 2 in `update-discipline.md`). The right way to silence a §10-vs-bullet mismatch is to fix the mismatch.

If a finding is genuinely spurious (false positive from regex limitations), open an issue describing the reproducer; we'll tighten the check rather than adding a suppression mechanism.
