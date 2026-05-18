# Spec: `fix-data-via-skill-sweep-mode`

- **ID**: SKILL-SPEC-5a9550e6c7
- **Source retrospective**: ../2026-05-18-94.md

## Intent

When existing data is broken in N records due to a now-fixed code bug, do not hand-edit the data. Add a sweep mode to the skill itself (`--tidy-foo`, `--reconcile-bar`) that finds and fixes the pattern from the skill's own logic, then run it. This makes the data fix idempotent, repeatable, traceable to a single code path, and ready to use again if the same drift recurs.

The session moment: PR #93's drain didn't promote/clear `want` placeholders when format-final files landed. After PR #93 merged, 14 records in `reference-only/sources.json` had stale `[want]` entries despite having real files attached. The temptation: write a jq one-liner that finds and deletes the 14 wants. The better path: add `drain.py --tidy-wants` that applies the *same logic* the now-fixed drain attach path uses, run it, see "Records touched: 14", commit. Next time the bug recurs (it will, in some related form), the sweep mode is already there.

## Trigger

**Direct user phrases:**
- "Fix the existing records too."
- "Clean up the catalog."
- "Sweep / tidy / reconcile / migrate the data."
- "How do we fix the data that's already broken?"
- "Use the skill, not jq, to fix this." (← the user's literal instruction this session)

**Proactive triggers:**
- You've just fixed a code bug and N records carry the bug's footprint. N can be 1 — but N ≥ 3 makes the sweep mode unambiguously worth building.
- A schema migration: data conformed to the old shape; the new shape needs a one-shot reconciliation.
- A new validator surfaces N existing violations that previously slipped through.
- You're about to write a jq one-liner that touches more than 3 records.

**Negative triggers:**
- A single record needs a one-off correction unrelated to a code bug (e.g., a typo in a title). Just use jq.
- The data fix needs human judgment per record (e.g., re-tagging based on content). Sweep mode automates a *rule*; if there's no rule, build a tool that surfaces the records, not one that fixes them.

## Inputs

- The skill / script that contains the code bug.
- The fixed code path (the new logic that handles the case correctly going forward).
- The data file (or set of records) carrying the bug's footprint.
- A clear rule for which records need fixing (used both to detect and to fix).
- A test fixture asserting the sweep is idempotent (running twice ≡ running once).

## Outputs

- A new CLI mode on the existing skill, typically named `--tidy-<thing>` or `--reconcile-<thing>`. Same script, same imports, new flag.
- The mode applies the SAME function the fixed code path uses (no parallel rule definition — if the function exists at module scope, both the live code path and the sweep call it).
- The mode supports `--dry-run` and prints a per-record summary.
- A unit test that builds a broken fixture and runs the sweep, asserts the fix.
- An idempotency test: a second sweep run is a no-op.
- A line in the project's docs / SKILL.md / SOP describing when to use the sweep mode.

## Workflow

1. **Fix the code bug first.** The sweep mode reuses the fixed logic; it doesn't reinvent it. Do not start writing the sweep until the live code path is correct and covered by a test.
2. **Extract the rule into a module-level function.** If the fix lives inside a method on a class or inside a tight loop, refactor it out. Example: instead of having "if format-final, clear wants" inline in `drain.py::stage_2_3_per_file`, factor it into `_purge_satisfied_wants(files, canonical_url)` that both the live path and the sweep can call. The function signature should take the record (or its parts) and a context, and return the count of changes.
3. **Add the CLI flag and handler.** Argparse argument like `--tidy-wants` with help text explaining the rule. A handler function like `_run_tidy_wants(data, data_p, dry_run)` that:
   - Iterates every record.
   - Applies the same rule function.
   - Tracks touched + total-purged counts.
   - Prints a per-record summary (markdown bullets work well).
   - Writes back atomically via the project's canonical normalizer (NEVER hand-format JSON; see `json-single-source-normalizer` skill).
   - Honors `--dry-run` (no writes, banner says "_(dry-run — no changes written)_").
4. **Run dry-run, then live.** ALWAYS dry-run first. The dry-run output is the proof that you understand what the sweep will do. If the count or the records-touched surprise you, the rule is wrong (or your understanding of it is wrong) — investigate before running for real.
5. **Run lint + tests after the live run.** The data file is now mutated; the lint check confirms the catalog is still valid. The full test suite confirms the code path didn't regress.
6. **Write the unit tests.**
   - **Sweep test**: build a fixture with N broken records, run the sweep, assert all N got fixed.
   - **Idempotency test**: run the sweep twice, assert the second run is a no-op (counts return 0, file bytes unchanged).
   - **Anti-pattern test (optional but recommended)**: build a fixture with records that LOOK broken but shouldn't be touched (e.g., transcript wants vs. generic wants), run sweep, assert they were preserved.
7. **Document.** Add a one-liner to the relevant docs explaining when to use the sweep mode.

## Concrete examples

### Example 1: the session's `drain.py --tidy-wants`

**The bug.** `drain.py`'s "attach to existing record" path appended a new file entry to `files[]` without clearing any matching `want` placeholders. After several drains, 14 records carried stale `want` entries.

**The fix.**
1. Code fix first: added `is_format_final(format, canonical_url)` and `_purge_satisfied_wants(files, canonical_url)` at module scope. The live attach path now calls `_purge_satisfied_wants` after appending. (Reconcile-source-dir.py imports it too.)
2. CLI flag: `--tidy-wants` skips the normal drain pipeline, dispatches to `_run_tidy_wants`.
3. Handler iterates all 209 records, calls `_purge_satisfied_wants(files, url)` on each, tracks counts.
4. Dry-run first:
   ```
   - `175cba9347` — clearing 1 stale `want` entry  (https://developers.openai.com/codex/guides/agents-md)
   - `18856eb4cf` — clearing 1 stale `want` entry  (https://hamel.dev/blog/posts/evals-faq)
   ...
   **Records touched:** 11  |  **Total `want` entries cleared:** 11
   _(dry-run — no changes written)_
   ```
   That's only 11; the bug report said 14. Investigated, found the rule was too narrow (only triggered on format-final attach, missed records with same-format-have). Broadened the rule, dry-ran again: 14. Now consistent.
5. Live run, lint clean, all 244 tests pass.
6. Unit tests cover: a record with `html [want]` + `mhtml [have]` gets the want purged (format-final rule); a record with `youtube-transcript [want]` and an `mhtml [have]` keeps the transcript want (it has `youtube_url`); the sweep is idempotent on a clean catalog.

### Example 2: a schema-migration sweep

Suppose a project has a `users.json` where each record has a `permissions: string` field, and a new schema requires `permissions: list[string]`. After deploying the schema-validation update, 500 records fail validation.

**Apply the workflow.**
1. Code fix first: the API now writes `permissions` as a list. The deserializer accepts both forms during the migration window but always emits lists.
2. Add `usermgmt-cli migrate-permissions` as a sweep mode. The handler iterates every user, calls `_normalize_permissions(record["permissions"])` (the same function the API uses).
3. Dry-run: prints "500 records would be migrated; sample: `alice` permissions='admin' → ['admin']".
4. Run live; lint; test.
5. Unit tests: mixed-form fixture; idempotency; records already in list form are not double-wrapped.

The advantage over a bare jq script: the migration function is unit-tested, the live API and the migration share the same code, and the migration is automatically idempotent.

## Anti-patterns

- **Writing a jq one-liner to fix N records when N ≥ 3.** The one-liner is faster the first time and slower every subsequent time the same drift recurs. The sweep mode amortizes.
- **Putting the fix logic in two places.** If `--tidy-foo` reimplements the rule that the live code path uses, the two will drift. The rule lives in ONE function; both paths call it.
- **Skipping `--dry-run`.** The dry-run is your sanity check: do the touched records match your mental model? If they don't, stop and figure out why.
- **Sweeping without writing the unit test.** The sweep ran successfully today; six months from now you'll mistrust whether it's safe to re-run. A test eliminates the doubt.
- **Sweep mode that needs human judgment per record.** That's not a sweep — that's a triage tool. Build a different shape: produce a report, surface the records, let the human decide.
- **Sweep mode that mutates the file without going through the canonical normalizer.** The file ends up in a different on-disk form than every other mutator produces. See the `json-single-source-normalizer` skill.

## Acceptance criteria

1. The sweep mode is on the same script as the skill's main entry point (e.g., `drain.py --tidy-wants`, not `scripts/cleanup-wants.py`).
2. The rule applied by the sweep is the SAME function the live code path uses.
3. `--dry-run` is supported and produces a per-record summary.
4. A unit test asserts the sweep fixes a broken fixture.
5. An idempotency test asserts a second run is a no-op.
6. Running the sweep on a clean catalog touches zero records (this falls out of #5).

## Files this skill creates / modifies

- `<skill-script>.py` — new `--tidy-<thing>` argparse argument + `_run_tidy_<thing>` handler. Module-level helper function for the rule, callable by both the live code path and the sweep.
- `tests/unit/test_<skill-script>.py` — sweep test, idempotency test, anti-pattern test (records that look broken but should be preserved).
- `<skill-docs>.md` — one-liner / paragraph describing when to use the sweep mode.
- The data file itself, after running the live sweep — but ONLY in a commit dedicated to that data cleanup. Don't mix the data cleanup with unrelated changes.
