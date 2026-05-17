# ADR 0002: Catalog is intentional, not exhaustive

## Context

When PR #80 migrated `source-dedup.md` into the new catalog, the migration script also scanned every `research/[0-9][0-9]-*.md` and `research/followup/*.md` report for cited URLs and auto-created "wanted" records for any URL not already in the catalog. The result: 215 new wanted records on top of the 145 with-content records.

Inspecting the 215 revealed they were noise:
- 7 x.com URLs (author profiles + tweet permalinks)
- 5 YouTube videos
- 24 pure homepage URLs (`cursor.com`, `anthropic.com`, `news.ycombinator.com`)
- 3 LinkedIn profiles
- App store links, marketplace listings, "see also" repo references

The signal — actual blog posts, papers, docs we wanted — was about 30 records lost among ~180 of casual mentions.

This raised the question: **what is the catalog FOR?**

## Decision

**The catalog reflects sources we have deliberately decided to track, not every URL ever mentioned in research material.**

Operationalization:
1. New records require a deliberate decision — either we have the content (`have`) OR we explicitly want it (`want` with a non-trivial file entry). Mass URL extraction is not a decision.
2. URLs cited in reports that aren't substantive sources are categorized:
   - **Casual hosts** (social media, video, app stores, homepage-only URLs): excluded by `casual_url_patterns` config in SKILL.md. `check-source-refs.py` skips them silently.
   - **Substantive-looking but not deliberately tracked**: listed in `reference-only/MIGRATION-EXCEPTIONS.md` as a register. `check-source-refs.py` reads this file and skips listed URLs.
3. The catalog's coverage discipline is enforced by `check-source-refs.py`: every URL cited in a report must be either in the catalog, in `MIGRATION-EXCEPTIONS.md`, or matching a casual pattern. New URLs that satisfy none of these trigger a lint error, forcing a decision.

## Alternatives considered

- **Catalog as comprehensive index** — every URL ever cited gets a record. Rejected: 80% noise crowds out the 20% signal; the catalog becomes unusable as a wishlist.
- **Catalog as wishlist only** — drop the `references_from` field, don't track citations at all. Rejected: the URL↔report cross-reference is genuinely useful for synthesis work.
- **Tag noise records with `casual-mention` and keep them** — adds clutter to renders, doesn't materially change behavior. Rejected for cleanliness.

## Consequences

**Positive:**
- Catalog stays focused on what we actually want to track and use.
- Render output (`reference-only/sources.md`) is browsable; the "wanted" section is the actual fetch wishlist, not a junk pile.
- The decision to track a source becomes an explicit gate (you have to actually run `process-url-list.py` or add the record via `edit.md`).
- `MIGRATION-EXCEPTIONS.md` serves as a register of "we considered this and said no" — preserves the audit trail.

**Negative:**
- Two-tier identity: catalog records + exception-list URLs. New users have to understand both.
- Manual judgment is required when a new URL appears — the linter pushes the decision but can't make it.
- The `casual_url_patterns` regex list will need maintenance as new junk-domain patterns emerge.

## References

- `.claude/skills/research-pipeline/scripts/check-source-refs.py` — enforces three-way disposition
- `.claude/skills/research-pipeline/SKILL.md` — `casual_url_patterns` config
- `reference-only/MIGRATION-EXCEPTIONS.md` — the exception register
- [Retrospective 2026-05-17-85, Phase 4](../2026-05-17-85.md) — the discovery moment + redesign
