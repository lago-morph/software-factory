# ADR 0001: Catalog ID derivation — sha256(canonical_url)[:10]

## Context

The research source catalog (`reference-only/sources.json`) needs a stable identifier per source. The identifier is used as:
- The map key in `sources.json`
- The directory name in `reference-only/<id>/`
- The reference target from research reports (durable links)
- The cross-reference target from `pointer_to` fields

In prior sessions, reconstitution attempts that lacked stable identity produced "Frankenstein files" — filenames claiming one URL while content was from a different source. We needed an identity scheme that was:

1. Deterministic — same source always gets the same ID.
2. Derivable — no central registry, no auto-increment, no human invention.
3. Collision-resistant for the corpus size (~200-1000 sources).
4. Short enough to be memorable / typeable / globbable.
5. Invariant under canonicalization — `?utm_source=` or `#fragment` tweaks shouldn't produce different IDs.

## Decision

**A record's ID is the first 10 hex characters of sha256(canonical_url), where `canonical_url` is the result of running the URL through `scripts/url_canonicalize.py`.**

The canonicalizer strips `utm_*`, `fbclid`, `gclid`, substack tracking params, fragments, default ports, and trailing slashes; lowercases scheme + host; sorts remaining query params.

This is enforced by `validate-sources.py` — if a record's `id` field doesn't equal `sha256(record.canonical_url)[:10]`, lint fails.

For records without a `canonical_url` (title-only entries with `search_hints`), the ID falls back to `sha256(title)[:10]`. This is acknowledged as a weaker identity — when a URL is later discovered, the right pattern is to create a new record with the URL-derived ID and set the title-only record's `pointer_to` to the new one.

## Alternatives considered

- **UUID v4** — would be unique but not derivable. Two agents independently encountering the same URL would assign different IDs. Rejected.
- **Auto-incrementing integer** — clean but requires a central registry. Rejected for the "no coordination" property.
- **Full sha256 (64 chars)** — collision-resistant but unwieldy as a directory name. 10 hex chars (40 bits) gives a collision probability of ~0.005% for 200 records; ample.
- **Use sha256 of file content as ID** — would change when the file changes. Identity must be stable across file changes. Rejected.
- **Use canonical URL itself as ID** — too long, contains `/` which conflicts with filesystem semantics, contains arbitrary characters. Rejected.

## Consequences

**Positive:**
- New records can be created in parallel by independent agents/sessions without conflict.
- The validator catches forged or mistyped IDs immediately.
- Reports referencing `reference-only/<id>/` get durable links — files within can be added/replaced/refetched without breaking the reference.
- Migration of legacy files maps cleanly: compute ID from URL, move file.

**Negative:**
- 10-character hex IDs are not human-meaningful. Users grep by URL or title, not by ID.
- URL canonicalization rules are now load-bearing — changing them retroactively would shift IDs. The canonicalizer's behavior is therefore frozen as part of the schema contract.
- Title-only records have weaker identity (hash of title) and may collide if two different sources happen to share a title.

## References

- `.claude/skills/research-pipeline/scripts/url_canonicalize.py` — the canonicalizer
- `.claude/skills/research-pipeline/scripts/validate-sources.py` — enforces the rule
- `reference-only/sources.schema.json` — schema constraining the `id` pattern (`^[0-9a-f]{10}$`)
- [Retrospective 2026-05-17-85, Phase 2-3](../2026-05-17-85.md) — design conversation that produced this choice
