# ADR 0004: Syntheses live in research/synthesis/ and carry a based-on-commit YAML header

- **ID**: ADR-24eb59b047
- **Status**: Accepted
- **Date**: 2026-05-21

## Context

The corpus has two synthesis documents — `research/00-synthesis.md` (Round-1, authored against a 7-report corpus) and `research/13-round-2-synthesis.md` (Round-2, authored against 12 reports) — sitting alongside 38+ numbered reports and 14+ followups in the same `/research/` directory. Naming by number was an artefact of dispatch order (the synthesis happened to be subagent 0 in Round 1, subagent 13 in Round 2); semantically the syntheses are a distinct artefact class from the reports they synthesize, but the flat directory layout made them look like equal siblings.

The reader-experience problem: synthesis claims age in a particular way — they remain valid only as long as the underlying corpus doesn't shift underneath them. The Round-1 synthesis's claims are anchored against a corpus that has grown several-fold since the synthesis was written. Without a header recording what commit the synthesis was last grounded against, a reader six months from now has no fast way to decide "is this synthesis still current, or has subsequent research overtaken it?" — they have to manually reconstruct the historical corpus state, which nobody does.

The same problem applies to [`architectures/*.md`](../../architectures/) — each is a decision document made against a snapshot of research. The five architecture specs were all last substantively edited on commit `c495dc9` (2026-05-10), but the corpus has grown by ~20 reports since then.

## Decision

Synthesis documents live under `research/synthesis/` (a new subdirectory) and carry a YAML `based-on-commit` + `based-on-date` header at the top. The same header convention applies to all files in the [`architectures/`](../../architectures/) directory.

Header format:
```yaml
---
based-on-commit: <short-hash>
based-on-date: YYYY-MM-DD
---
```

The hash + date are historical — they record when the file was last substantively edited, not when the header was added. When the file is next substantively edited, the writer updates the header to the new commit.

## Alternatives considered

- **Keep syntheses in `/research/` flat; rely on filename prefix only.** Rejected: the corpus already had `00-synthesis.md` and `13-round-2-synthesis.md` looking like reports 00 and 13 (which they are not). The directory separation makes the artefact-class distinction visible at a glance.
- **Use a more elaborate header (authors, change-log entries, supersedes / superseded-by links).** Rejected as YAGNI for now. The minimum useful header is the commit + date; richer metadata can be added when the use case shows up.
- **Skip the header on `architectures/*.md`; only apply to syntheses.** Rejected: architectures are decision documents grounded in research state, which is exactly what the header records. The pattern generalises.

## Consequences

What this buys:

- A reader of any synthesis or architecture file can answer "what corpus state does this document grok?" in O(1) by reading the header. No git archaeology required.
- New syntheses have an obvious home (`research/synthesis/`).
- The header convention is uniform across the two affected directories.

What this costs:

- Existing syntheses and architecture files need a one-time backfill of the historical commit. This ADR ships that backfill (`f480c8b` for `00-synthesis.md`, `8f737b3` for `13-round-2-synthesis.md`, `c495dc9` for all five architecture files). The historical-commit values were recovered by walking the visible-history boundary via parent-ref hashes.
- Future synthesis-authoring agents have to remember to update the header when they substantively edit the doc. The [`research-pipeline`](../../.claude/skills/research-pipeline/SKILL.md) skill's `_drain/stage-5-content-processing.md` should document this so it becomes part of the doc-authoring workflow.

Trade-off accepted: the one-time backfill + the discipline of updating headers on substantive edits is worth losing the historical opacity of "what corpus state was this doc grounded in?"

## References

- [`retrospective/2026-05-21-106.md`](../../retrospective/2026-05-21-106.md) — the source retrospective; full draft at [`retrospective/2026-05-21-106/ADR-24eb59b047-synthesis-subdir-and-based-on-commit.md`](../../retrospective/2026-05-21-106/ADR-24eb59b047-synthesis-subdir-and-based-on-commit.md).
- [`research/synthesis/00-synthesis.md`](../../research/synthesis/00-synthesis.md) — the Round-1 synthesis, post-move, with header backfilled.
- [`research/synthesis/13-round-2-synthesis.md`](../../research/synthesis/13-round-2-synthesis.md) — the Round-2 synthesis, post-move, with header backfilled.
- [`architectures/00-comparison.md`](../../architectures/00-comparison.md), [`01-specification-refinery.md`](../../architectures/01-specification-refinery.md), [`02-compound-atelier.md`](../../architectures/02-compound-atelier.md), [`03-phase-gated-foundry.md`](../../architectures/03-phase-gated-foundry.md), [`04-evolutionary-tournament.md`](../../architectures/04-evolutionary-tournament.md) — architecture files, all backfilled.
- [PR #106](https://github.com/lago-morph/software-factory/pull/106) — the cleanup-plan PR that surfaced the decision.
