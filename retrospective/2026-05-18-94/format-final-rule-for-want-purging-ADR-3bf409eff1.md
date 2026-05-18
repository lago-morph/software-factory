# ADR: Format-final rule for want-purging in catalog records

- **ID**: ADR-3bf409eff1
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-18
- **Source retrospective**: ../2026-05-18-94.md
- **PRs covered**: #93, #94

## Context

The catalog stores entries for research sources at `reference-only/sources.json`. Each record's `files[]` array holds two kinds of file descriptors: `have` entries (with a filename and sha256 — actual files on disk under `reference-only/<id>/`) and `want` entries (filename: null — a placeholder meaning "we want this URL fetched"). For most records, a `want` is created when a URL is added to a list before content is available; later, when a file lands, `drain.py` should resolve the placeholder.

PR #93 attached 11 MHTML files to existing wanted records and merged. The auto-regen workflow then produced `sources.md`, which still asked for URLs we'd just provided files for. Root cause: drain.py's "attach to existing record" path appended new `have` entries but never cleared matching `want` placeholders on the same record. The promotion logic existed for YouTube transcripts (which carry a `youtube_url` field) but not for generic page-content wants. Three more records (`24ca29ee98`, `5a9f63821f`, `f8007cc630`) had the same drift from earlier ingestion paths.

Doing a hand-tuned "clear all wants when any have lands" rule was tempting but wrong: some wants are genuinely meaningful even when a have exists (e.g., we have an `html` capture of a paywalled SPA but want a clean fetch). The decision was about how to define "this want is satisfied" formally.

## Decision

A generic `[want]` entry on a record is cleared iff EITHER (a) some `have` file on the record is *format-final* for the record's `canonical_url`, OR (b) some `have` file on the record has the same `format` as the `want`. **Format-final** is defined as:

- **MHTML** for any URL — always format-final (highest-fidelity HTML save; embeds CSS + images; nothing strictly better exists).
- **PDF / TXT / MD / CSV / JSON / IPYNB** for a URL whose terminal path extension matches the file's format — format-final (the file IS the URL's payload).
- **HTML / HTM** for a URL whose terminal path extension is `.html` / `.htm` — format-final. For URLs without `.html` / `.htm`, plain HTML is NOT format-final (MHTML could still be better).
- Anything else — not format-final.

Transcript-format wants (those carrying a `youtube_url` field) are NEVER touched by this rule — they're a different ingestion track.

The rule is implemented as two module-level functions in `drain.py` — `is_format_final(file_format, canonical_url)` and `_purge_satisfied_wants(files, canonical_url)` — called from both the live attach path in `drain.py::stage_2_3_per_file` and the reconcile path in `reconcile-source-dir.py`. A catalog-wide sweep mode `drain.py --tidy-wants` reuses the same function to fix existing broken records.

## Alternatives considered

1. **"Any have on the record clears all wants" (the naive rule).** Rejected: incorrectly clears wants on records where a partial capture exists but a full one is still wanted. The Lenny newsletter record `f8007cc630` had a paywalled `html [have]` plus a YouTube transcript `txt [have]` plus an `html [want]` for a clean fetch — the want is meaningful and the naive rule would have cleared it. Result: lost intent, hard to recover.

2. **"Only purge wants when an exact format match is added" (the narrow rule).** Rejected: misses the most common case — we drop in an MHTML for a record whose `want` was `html` (the URL didn't end `.html`). MHTML is strictly better than HTML for that URL, but the formats don't match string-equal. The narrow rule would leave the want stale.

3. **"Let the user manually clear wants via a UI / API."** Rejected: there's no UI, the catalog has 209 records, and the broken state already exists for 14 records right now. The catalog needs an automated rule; manual review is the fallback when the rule can't decide.

4. **"Score-based satisfaction" (each want has a quality threshold; haves contribute points).** Rejected as over-engineered. The two-clause rule above covers every observed case in the catalog as of 2026-05-18; no record demonstrated a need for partial / weighted satisfaction.

## Consequences

**Easier:**
- The "I gave you the file but the catalog still asks for the URL" failure mode (which is what triggered PR #94) cannot recur. The drain attach path, the reconcile path, and the sweep mode all share the same rule function; a regression in any one of them is caught by `tests/unit/test_drain.py::TestDrainWantPromotion`.
- New ingestion paths automatically inherit the rule by calling `_purge_satisfied_wants`. No copy-paste of the logic.
- Cleaning up a stale catalog is `python drain.py --tidy-wants` — idempotent, dry-runnable, traceable.

**Harder / trade-offs accepted:**
- The rule is conservative. A record with `html [want]` and `html [have]` for a URL like `https://hamel.dev/blog/posts/x` (no extension) gets the want cleared even though MHTML would still be a strict upgrade. We accept this because the user's verbal spec was "if you have a format that matches the URL's extension OR is MHTML, it's not going to get better" — clause (b) of the rule honors that.
- HTML for an extension-less URL is *not* format-final under this rule. A record with HTML-have only stays flagged as "could still use an MHTML" via the audit. Trade-off: false-positive flags on records where we'll likely never get a better capture. Mitigation: the audit's `completeness` field can be hand-set to `complete` for those records.
- Transcript wants are special-cased (via `youtube_url`). Any future "specialized want" (e.g., a `paywall_bypass_url`) needs an explicit exception added to `_purge_satisfied_wants`. This is the right cost — special wants are rare and adding a new exception is a localized change.

## References

- [`../2026-05-18-94.md`](../2026-05-18-94.md) — the source retrospective; see Phase 2 (bug surfaces) and Phase 4 (implementation).
- [`./fix-data-via-skill-sweep-mode-SKILL-SPEC-5a9550e6c7.md`](./fix-data-via-skill-sweep-mode-SKILL-SPEC-5a9550e6c7.md) — the sweep-mode pattern used to fix the 14 existing broken records.
- `.claude/skills/research-pipeline/scripts/drain.py` — `is_format_final` (~line 100), `_purge_satisfied_wants` (~line 140), `_run_tidy_wants` (~line 860).
- `.claude/skills/research-pipeline/scripts/reconcile-source-dir.py` — imports and uses `_purge_satisfied_wants`.
- `.claude/skills/research-pipeline/tests/unit/test_drain.py::TestDrainWantPromotion` — the regression tests (5 tests covering the rule's clauses + transcript-want preservation).
- PRs: #93 (which exposed the bug), #94 (which implemented the fix + swept 14 records).
