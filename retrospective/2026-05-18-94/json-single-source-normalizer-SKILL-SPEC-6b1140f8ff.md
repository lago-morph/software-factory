# Spec: `json-single-source-normalizer`

- **ID**: SKILL-SPEC-6b1140f8ff
- **Source retrospective**: ../2026-05-18-94.md

## Intent

Consolidate divergent JSON normalizers (Python `json.dumps` + jq + bot workflows) into one canonical helper script, locked by a byte-equivalence regression test. Triggered when a project's JSON data file has multiple mutators that have started to drift (typical signal: a recent merge conflict on the file that turned out to be cosmetic-only), or proactively when adding a new mutator to a file that already has one.

The session moment: PR #93 added the auto-regen workflow that ran `jq -S 'to_entries | sort_by(.key) | from_entries'` on `reference-only/sources.json`. PR #94's drain code used `json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True)`. Both produced sorted output and looked equivalent, but jq inserts new keys at the END of an object regardless of input order — so a `pointer_to` field that I set via jq landed at the end while normalize_and_write expected it alphabetically. The merge conflict was 2 lines of cosmetic diff with zero semantic content, but represented real drift that would have compounded.

## Trigger

**Direct user phrases:**
- "Consolidate these normalizers."
- "Make sure both code paths emit the same JSON."
- "Update the skill to specify the exact jq command."
- "Drift between Python and jq output."

**Proactive triggers:**
- A merge conflict on a JSON data file where the diff is cosmetic (key reordering, no value changes).
- Adding a new code path that writes to a JSON file that already has at least one writer (workflow, script, ad-hoc jq pipeline).
- A code review comment asking "why doesn't this match the other code?" about a normalize/sort/serialize function.

**Negative triggers (do NOT activate):**
- The file has exactly one writer and no inline ad-hoc jq edits.
- The file is intermediate output (a build artifact) where on-disk form doesn't matter.

## Inputs

- Path to the canonical data file (e.g., `reference-only/sources.json`).
- List of all known writers (Python functions, shell scripts, GitHub workflows, inline jq pipelines in docs).
- The project's testing convention (pytest, jest, etc.) so the regression test fits.

## Outputs

- New `scripts/normalize-<filename>.sh` (or equivalent) — the single source of truth, runs `jq -S '.'` atomically (input → temp → mv).
- Every existing writer updated to either call the helper or carry a contract docstring naming it as the reference.
- A regression test (typically named `test_normalize_<filename>.py`) that:
  - Asserts byte-equivalence between the canonical helper and every other writer that produces final output.
  - Asserts idempotency: running the helper twice yields the same bytes as running it once.
  - Asserts the live committed file is currently in canonical form (catches future commits that bypass the normalizer).
- An entry in the project's SKILL.md / AGENTS.md / equivalent calling the helper out as the prescribed normalize step.

## Workflow

1. **Inventory all writers.** `grep -rln "jq -S\|sort_keys=True\|jq.*from_entries\|json.dumps" <project>` plus a manual review of any GitHub workflows under `.github/workflows/`. The list is usually 5–15 places.
2. **Pick the simplest canonical form.** For most JSON data files this is `jq -S '.'` — recursively sorts object keys at every level, 2-space indent (jq default), preserves UTF-8, appends a trailing newline. Almost all longer invocations like `jq -S 'to_entries | sort_by(.key) | from_entries'` reduce to this.
3. **Write the helper script.** Typical content:
   ```bash
   #!/usr/bin/env bash
   set -euo pipefail
   PATH_IN="${1:-<default>}"
   TMP="${PATH_IN}.normalize.tmp"
   trap 'rm -f "$TMP"' EXIT
   jq -S '.' "$PATH_IN" > "$TMP"
   mv "$TMP" "$PATH_IN"
   ```
   `chmod +x` it. Top of file: a contract docstring naming this as the single source of truth.
4. **Point every other writer at it.** Workflows, docs, recipes — replace the inline invocation with a call to the helper. For Python writers that can't easily exec the helper, document the equivalent and write a regression test.
5. **Write the byte-equivalence regression test.** Across a spread of fixtures (unicode, nested arrays, key-order stress, edge cases like empty dict), assert `subprocess.run(["bash", helper, path])` produces the same bytes as the Python writer.
6. **Verify the live file.** `bash scripts/normalize-<filename>.sh <path>` should be a no-op against the committed file. If it isn't, commit the normalization as a separate cleanup commit before adding the helper, so the lockdown test passes on first run.
7. **Run the full test suite + lint.** The regression test should pass on first run. If it doesn't, the canonical form choice was wrong — re-check step 2.

## Concrete examples

### Example 1: the session's `sources.json` consolidation

**Before.** Five places normalized `reference-only/sources.json`, three different invocations:
- `scripts/drain.py::normalize_and_write` (Python `json.dumps(sort_keys=True)`)
- `.github/workflows/regen-sources-md-auto.yml` and `regen-sources-md-manual.yml` (`jq -S 'to_entries | sort_by(.key) | from_entries'`)
- 10 jq recipes in `resources/_catalog/`, `_drain/`, `reference-audit.md`
- Inline ad-hoc jq edits the user / agent run by hand

**The drift.** When I set a new `pointer_to` field on record `e588b9bb1a` via jq, the field landed at the end of the object instead of alphabetically. The auto-regen workflow then re-sorted via the workflow's invocation, but main and my branch diverged subtly enough to produce a merge conflict.

**The fix.**
1. Created `.claude/skills/research-pipeline/scripts/normalize-sources-json.sh` running `jq -S '.'`.
2. Updated `SKILL.md` Hard rule #2 to prescribe the helper.
3. Updated both workflows + skill-shipped templates: `run: bash …/normalize-sources-json.sh reference-only/sources.json`.
4. Updated the 10 jq recipes: each now ends with `mv /tmp/new.json "$F"` + `bash …/normalize-sources-json.sh "$F"`.
5. Updated `validate-sources.py`'s error message to point at the helper.
6. Added contract docstring to `drain.py::normalize_and_write` declaring byte-identical output.
7. Wrote `tests/unit/test_normalize_sources.py` with 3 tests: byte-equivalence across 6 fixtures, idempotency, real-catalog-is-canonical.

**Verification.** `bash scripts/normalize-sources-json.sh reference-only/sources.json` was a no-op on first run. The regression test passes. The "real catalog is canonical" test means any future commit that hand-edits the JSON will fail CI.

### Example 2: hypothetical `dependencies.json` consolidation

A project has `dependencies.json`. A `package.py` script writes it via `json.dump(data, fp, indent=2, sort_keys=True)`. A GitHub Action workflow regenerates it via `jq 'sort_by(.name)' dependencies.json`. A `scripts/add-dep.sh` uses an inline `jq '. += [...]'`. They're already drifting.

**Apply the workflow:**
1. Inventory: 3 writers above.
2. Canonical form: `jq -S '.'` won't work — the file is an array, not an object, and the user wants it sorted by `.name`. Use `jq '[.[] | to_entries | sort_by(.key) | from_entries] | sort_by(.name)'`.
3. Helper: `scripts/normalize-dependencies-json.sh`. Same atomic temp/mv pattern.
4. Update the workflow, `package.py` (write a contract docstring; Python must match this output), `add-dep.sh` (append → call helper).
5. Regression test: `test_normalize_dependencies.py`. Asserts Python output === jq output for fixtures including duplicates, unicode, nested objects.
6. Verify: helper run on committed file is a no-op (if not, commit the cleanup first).

The pattern is the same; only the canonical form expression changes.

## Anti-patterns

- **Inlining the canonical form everywhere "for clarity".** This is exactly what created the drift in the first place. Reference the helper script by path; don't paste the jq pipeline.
- **Trusting that two normalizers "must be equivalent" because they both sort keys.** Sorting is necessary but not sufficient — formatting (indent), encoding (escape policy), trailing newline, and insertion order on partial mutations all matter. Lock with a byte-equivalence test or expect drift.
- **Skipping the regression test "because it's obviously correct".** Six months from now someone will add a new writer; the test is the only thing that catches them.
- **Adopting the canonical form via a hand-edit to the data file.** Run the helper script in a clean commit, separately from any other change. The data-file diff should ONLY contain the normalization changes — otherwise reviewers can't tell what's the lockdown vs. what's the feature.
- **Letting the Python writer drift from the shell helper.** If `json.dumps` semantics don't match jq for some edge case (large numbers, NaN, lone surrogates), either route Python through the helper via subprocess or pin both sides with a fixture-based test that exercises the edge case.

## Acceptance criteria

1. There is exactly one path-named canonical normalizer script (or function) for the file.
2. Every other writer either calls the canonical normalizer or carries a docstring naming it as the reference.
3. A byte-equivalence regression test exists, runs in CI, and currently passes.
4. Running the canonical normalizer against the committed file in HEAD is a no-op (verified by an idempotency test).
5. The project's primary SKILL.md / AGENTS.md / README lists the canonical normalizer's path as the prescribed normalize step, with the others removed.

## Files this skill creates / modifies

- `scripts/normalize-<filename>.sh` (or equivalent path) — the canonical helper. Idempotent, atomic.
- `tests/unit/test_normalize_<filename>.py` — the byte-equivalence + idempotency + real-data-is-canonical regression test.
- `.github/workflows/*.yml` (if any) — updated to call the helper.
- `SKILL.md` / `AGENTS.md` / project docs — Hard rule referencing the helper.
- The Python writer(s) — docstring referencing the helper as the spec; redundant pre-sort code (e.g., manual `sorted()` calls) removed since the canonical serializer now handles it.
- Inline jq recipes in docs — updated to end with `bash <helper>` instead of the long inline invocation.
