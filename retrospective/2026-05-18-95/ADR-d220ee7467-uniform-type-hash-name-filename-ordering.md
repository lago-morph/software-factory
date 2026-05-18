# ADR: Uniform TYPE-hash-name.md filename ordering across retrospective sibling-dir artifacts

- **ID**: ADR-d220ee7467
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-18
- **Source retrospective**: ../2026-05-18-95.md
- **PRs covered**: #95

## Context

Through the first 18 retrospectives the `retrospective/<UTC_DATE>-<PR>/` sibling directory accumulated three types of artifacts: per-skill specs, ADR drafts, and (originally) a consolidated `AGENTS-suggestions.md`. The skill spec convention was `<skill-id>-SKILL-SPEC-<hash>.md`; the ADR convention was `<kebab-title>-ADR-<hash>.md`. The descriptive name led, the type token sat in the middle, the durable hash trailed.

PR #95 introduced a third artifact type (per-rule agents-file fragments) and asked the question of how to name them consistently. The user clarified: TYPE should lead, hash should follow, descriptive name should trail — and applied to all three types. The legacy `<name>-TYPE-<hash>.md` ordering was abandoned in the same PR.

## Decision

All three sibling-directory artifact types use a uniform `TYPE-<hash>-<name>.md` filename ordering: type token leads, durable hash follows at a constant offset, descriptive kebab name trails. Concretely:

- `SKILL-SPEC-<hash>-<skill-id>.md`
- `ADR-<hash>-<kebab-title>.md`
- `AGENTS-MD-<hash>-<kebab-rule-name>.md`

The `ADR-DRAFT-<kebab-title>.md` placeholder remains an exception (no hash in the filename; reserved hash is declared inside the file) because the completing agent may discover the file under a different title than was forecast at reprocess time.

## Alternatives considered

- **Keep the existing `<name>-TYPE-<hash>.md` ordering.** Rejected: the durable hash sat in a variable position (after a kebab name of any length), so any CI/CD tool that wanted to parse the hash had to do a regex match against the type token. With TYPE-first, the hash sits at character offsets 11–20 for AGENTS-MD-, 5–14 for ADR-, 12–21 for SKILL-SPEC-. A simple substring extract works.

- **Use a separate manifest file (e.g., `index.json`) per sibling directory.** Rejected: introduces a second source of truth that can drift from the filenames. The filename itself is the index.

- **Put the hash at the very end.** Rejected: makes alphabetical sort cluster by descriptive name, not by type. Type-first ordering makes `ls` group same-type artifacts together visually, which is what a human reviewer wants.

## Consequences

- **Migration cost.** Reprocess mode must rename every legacy `<name>-TYPE-<hash>.md` to `TYPE-<hash>-<name>.md`, preserving the hash byte-for-byte. The `self-retrospective reprocess` workflow already includes this step.
- **Tooling becomes simpler.** CI/CD parsers can extract the hash with a fixed offset; link checkers can identify artifact type by prefix.
- **Visual sort order improves.** A directory listing of the sibling dir groups SKILL-SPEC entries together, ADR entries together, and AGENTS-MD entries together — alphabetically clustered by type.
- **One-off cognitive cost** for authors who learned the old convention; offset by the templates in `resources/` that encode the new convention so freehand authoring is unnecessary.

## References

- [`../2026-05-18-95.md`](../2026-05-18-95.md) — the source retrospective.
- [`./ADR-ecbfcc6b52-strict-two-section-agents-md-fragments.md`](./ADR-ecbfcc6b52-strict-two-section-agents-md-fragments.md) — the companion ADR on per-rule fragment format that depends on this naming convention.
- PR #95: lago-morph/software-factory#95 — the PR that introduced the uniform convention and reprocess-mode migration.
