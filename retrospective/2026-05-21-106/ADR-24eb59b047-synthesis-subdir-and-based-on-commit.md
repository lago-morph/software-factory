# ADR: Syntheses live in research/synthesis/ and carry a based-on-commit YAML header

- **ID**: ADR-24eb59b047
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-21
- **Source retrospective**: ../2026-05-21-106.md
- **PRs covered**: #106

## Context

The corpus has two synthesis documents — `research/00-synthesis.md` (Round-1, authored against a 7-report corpus) and `research/13-round-2-synthesis.md` (Round-2, authored against 12 reports) — sitting alongside 38 numbered reports and 14 followups in the same `/research/` directory. Naming by number was an artefact of dispatch order (the synthesis happened to be subagent 0 in Round 1, subagent 13 in Round 2); semantically the syntheses are a distinct artefact class from the reports they synthesize, but the flat directory layout made them look like equal siblings.

The reader-experience problem: synthesis claims age in a particular way — they remain valid only as long as the underlying corpus doesn't shift underneath them. `00-synthesis.md`'s claims are anchored against a corpus that has grown 5x since the synthesis was written. Without a header recording what commit the synthesis was last grounded against, a reader six months from now has no fast way to decide "is this synthesis still current, or has subsequent research overtaken it?" — they have to manually reconstruct the historical corpus state, which nobody does.

The same problem applies to `architectures/*.md` — each is a decision document made against a snapshot of research. The five architecture specs were all last edited 2026-05-10 (commit `c495dc9`), but the corpus has grown by ~20 reports since then.

## Decision

Synthesis documents live under `research/synthesis/` (a new subdirectory) and carry a YAML `based-on-commit` + `based-on-date` header at the top. The same header convention applies to all files in the `architectures/` directory.

Header format:
```yaml
---
based-on-commit: <short-hash>
based-on-date: YYYY-MM-DD
---
```

The hash + date are historical — they record when the file was last substantively edited, not when the header was added. When the file is next substantively edited, the writer updates the header to the new commit.

## Alternatives considered

- **Keep syntheses in `/research/` flat; rely on filename prefix only.** Rejected: the corpus already had `00-synthesis.md` and `13-round-2-synthesis.md` looking like reports 00 and 13 (which they are not). The directory separation makes the artefact-class distinction visible at-a-glance.
- **Use a more elaborate header (authors, change-log entries, supersedes/superseded-by links).** Rejected as YAGNI for now. The minimum useful header is the commit + date; richer metadata can be added when the use case shows up.
- **Skip the header on `architectures/*.md`; only apply to syntheses.** Rejected: architectures are decision documents grounded in research state, which is exactly what the header records. The pattern generalises.

## Consequences

**Easier:**
- A reader of any synthesis or architecture file can answer "what corpus state does this document grok?" in O(1) by reading the header. No git archaeology required.
- New syntheses have an obvious home (`research/synthesis/`).
- The header convention is uniform across the two affected directories.

**Harder:**
- Existing syntheses + architecture files all need a one-time backfill of the historical commit (this session researched the values: `f480c8b`, `8f737b3`, `c495dc9`). The git history walk required parent-ref navigation past the visible-history boundary; the values are recorded in cleanup-plan v3's N3 table for the executing agent.
- Future synthesis-authoring agents have to remember to update the header when they substantively edit the doc. The research-pipeline skill's `_drain/stage-5-content-processing.md` should document this so it becomes part of the doc-authoring workflow.

**Trade-off accepted:** the one-time backfill + the discipline of updating headers on substantive edits is worth losing the historical opacity of "what corpus state was this doc grounded in?"

## References

- [`../2026-05-21-106.md`](../2026-05-21-106.md) — the source retrospective.
- [`./AGENTS-MD-4c195c2603-based-on-commit-header.md`](./AGENTS-MD-4c195c2603-based-on-commit-header.md) — the corresponding AGENTS.md rule.
- [`./AGENTS-MD-6242d6edd9-git-archaeology-via-parent-refs.md`](./AGENTS-MD-6242d6edd9-git-archaeology-via-parent-refs.md) — git-archaeology pattern needed for the backfill.
- PR the decision was made in: #106.
- Pre-existing skill resource to update: `.claude/skills/research-pipeline/resources/_drain/stage-5-content-processing.md` (encode subdirectory placement + header convention).
