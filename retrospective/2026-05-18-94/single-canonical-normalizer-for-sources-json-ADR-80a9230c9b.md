# ADR: Single canonical normalizer for sources.json

- **ID**: ADR-80a9230c9b
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-18
- **Source retrospective**: ../2026-05-18-94.md
- **PRs covered**: #94

## Context

The catalog file `reference-only/sources.json` is touched by multiple agents and tools: `drain.py` (Python's `normalize_and_write` using `json.dumps(sort_keys=True)`), the auto-regen GitHub Action workflows (`jq -S 'to_entries | sort_by(.key) | from_entries'`), ten ad-hoc jq recipes in `resources/_catalog/` and `_drain/` documentation, and any inline jq edits performed by the agent during catalog work.

Each writer normalizes the file in roughly the same way — sort top-level keys, sort nested keys, pretty-print, 2-space indent — but with subtly different invocations. They were assumed equivalent. They weren't.

During PR #94, I set a `pointer_to` field on record `e588b9bb1a` via an inline jq pipeline. The jq `=` operator inserts new keys at the END of the object rather than alphabetically. The auto-regen workflow on main then re-sorted via its own invocation. My branch's `normalize_and_write` produced an `e588b9bb1a` block with `pointer_to` alphabetically placed; main's regen produced one with `pointer_to` at the end. A merge conflict followed — purely cosmetic, but real, and would have compounded over time.

The fix wasn't to manually align both forms (which would just re-introduce drift on the next inline edit). The fix was structural: pick ONE canonical normalizer, point every writer at it, and lock byte-equivalence with a regression test.

## Decision

`.claude/skills/research-pipeline/scripts/normalize-sources-json.sh` is the single source of truth for `sources.json`'s on-disk shape. The script runs `jq -S '.'` atomically (input → temp → mv) and produces:

- All object keys sorted alphabetically at every level (jq's `-S` flag — equivalent to Python's `sort_keys=True`).
- 2-space indent (jq default; matches Python `indent=2`).
- UTF-8 preserved as-is, no `\uXXXX` escapes (jq default; matches Python `ensure_ascii=False`).
- Arrays preserve their existing element order (neither tool reorders arrays).
- Trailing newline.

Every other writer must produce byte-identical output:

- `SKILL.md` Hard rule #2 prescribes the helper script as THE normalize step.
- Both regen workflows (`.github/workflows/regen-sources-md-{auto,manual}.yml`) call the helper.
- Skill-shipped workflow templates (`resources/_workflows/`) call the helper.
- Ten jq recipes in `resources/_catalog/` and `_drain/` end with `mv /tmp/new.json "$F"` followed by a call to the helper.
- `validate-sources.py`'s "not sorted" error message points users at the helper.
- `drain.py::normalize_and_write` carries a contract docstring naming the helper as the reference and uses the equivalent Python form (`json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n"`).

Byte-equivalence is locked by `tests/unit/test_normalize_sources.py` (3 tests): byte-equivalence across 6 catalog-shape fixtures, idempotency, and a "the committed catalog is currently canonical" check that catches any future commit that bypasses the normalizer.

## Alternatives considered

1. **Keep both normalizers; document that they're equivalent.** Rejected: the merge conflict proved they weren't equivalent in all cases. The drift was subtle (insertion order on partial mutations) and would have continued to surprise us. "Equivalent in theory" isn't a property we can rely on without a test, and once we have a test, we may as well consolidate.

2. **Adopt the Python normalizer as canonical (run Python from the workflow).** Rejected: jq is the lingua franca for inline catalog edits — every recipe in `resources/_catalog/` is a jq pipeline. Requiring a Python interpreter to normalize after every ad-hoc jq edit is high friction. Cheaper to make jq the spec and have Python conform.

3. **Switch to a structured-data format that doesn't require normalization (YAML with anchor sort, TOML, a real database).** Rejected: out of scope for this PR, and `sources.json` is the established interface — too many tools and reports already depend on it. Worth revisiting if normalization continues to be a friction point.

4. **Use `jq -S 'to_entries | sort_by(.key) | from_entries'` (the previous workflow invocation) as canonical.** Rejected: the longer form is fully equivalent to `jq -S '.'` because `-S` already recursively sorts all object keys; the `to_entries | sort_by | from_entries` step is redundant. Choosing the shorter form makes the rule easier to remember and impossible to typo subtly.

## Consequences

**Easier:**
- Any new writer of `sources.json` has a single artifact to call (`bash …/normalize-sources-json.sh <path>`); they can't independently pick a different normalization.
- Merge conflicts on `sources.json` due to key reordering can't recur — both sides of a merge now produce the same byte layout.
- Onboarding a new contributor: the rule is one line in SKILL.md ("always end edits with this script"), backed by a CI test.
- The Python and jq paths are coupled by an explicit test, so a future change to jq's behavior or a Python `json` library quirk will be caught immediately.

**Harder / trade-offs accepted:**
- Every new writer adds one more cross-reference for the regression test to maintain. If the test only checks Python ↔ jq today, a future Rust or Go writer needs its own assertion. This is the right cost — explicit drift detection beats implicit drift.
- The "committed catalog is currently canonical" test means every commit that touches `sources.json` must end with a normalize-script run, OR the test will fail. This is the desired behavior — it catches hand-edits — but it makes "I just want to update one comment in this record" require an extra step.
- `jq -S` has subtle behavior for numbers (it preserves precision but may rewrite scientific notation). Our catalog has no numeric records, but a future schema change that adds numerics would need to verify Python's serialization matches jq's. The byte-equivalence test would catch this; the cost is the time to investigate and fix.

## References

- [`../2026-05-18-94.md`](../2026-05-18-94.md) — Phase 5 (merge conflict) and Phase 6 (consolidation).
- [`./json-single-source-normalizer-SKILL-SPEC-6b1140f8ff.md`](./json-single-source-normalizer-SKILL-SPEC-6b1140f8ff.md) — the general pattern (skill spec) of which this is the project's first concrete application.
- `.claude/skills/research-pipeline/scripts/normalize-sources-json.sh` — the canonical helper.
- `.claude/skills/research-pipeline/scripts/drain.py::normalize_and_write` — the Python equivalent with contract docstring.
- `.claude/skills/research-pipeline/tests/unit/test_normalize_sources.py` — the byte-equivalence + idempotency + real-catalog regression tests.
- `.claude/skills/research-pipeline/SKILL.md` — Hard rule #2 (revised).
- PRs: #94, specifically commit `207f544` ("Single canonical normalizer for sources.json").
