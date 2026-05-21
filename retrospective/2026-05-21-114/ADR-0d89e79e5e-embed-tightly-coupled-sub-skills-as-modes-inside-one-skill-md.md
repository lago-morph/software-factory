# ADR: Embed tightly coupled sub-skills as modes inside one SKILL.md

- **ID**: ADR-0d89e79e5e
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-21
- **Source retrospective**: ../2026-05-21-114.md
- **PRs covered**: #114

## Context

PR #114 originally shipped two sibling skills: `issue-management` (the primary, codifying issue-thread conventions) and `add-issue-behavior` (the meta, walking the user through adding/changing a behavior in the primary). The two were conceptually separate concerns and lived in separate directories under `.claude/skills/`.

In review the user requested: "I wanted the sub skill to be embedded inside main skill so there is one distribution file to worry about." The motivation was operational: there's only one skill cluster to copy, version, and reason about; the sub-skill's content is meaningful only in the context of the primary; and the harness picks them up from a single SKILL.md so there's no benefit to keeping them as siblings.

The precedent for this pattern already exists in this repo's skill library — `self-retrospective` carries a primary "forward mode" and a secondary "reprocess mode" in one SKILL.md, distinguished by trigger phrases and section headers.

## Decision

When two skills are tightly coupled — specifically, when the secondary's purpose is to edit, configure, or extend the primary — embed the secondary as a top-level "mode" section inside the primary's SKILL.md, rather than as a sibling skill directory.

The mode receives its own trigger surface (declared in the primary's frontmatter `description`), its own workflow section, its own anti-patterns, and may share the primary's templates and capability tables. The two modes are mutually exclusive within a turn; the agent identifies which mode the user's request matches and stays in it.

## Alternatives considered

- **Keep sibling-skill directories with cross-links** — rejected per user's explicit request. The cross-links worked but doubled the discovery surface and split the documentation across two files; copying the cluster to another repo means copying two directories and remembering which order to install.
- **Embed via a `spec/` subdirectory** (one SKILL.md, one spec doc) — partial match but doesn't solve trigger separation. The harness reads only `SKILL.md`'s frontmatter for trigger matching; a spec doc would have no trigger.
- **Generate a combined "umbrella" SKILL.md from two source files via a build step** — rejected as overkill. Adds a build step and a drift risk for one-tenth the maintenance saving.
- **Always inline meta-skills into their primaries** — too strong. The convention applies only when the meta exists *for* the primary and has no independent use.

## Consequences

**What becomes easier:** Single file to copy, version, and review. Single frontmatter `description` lists all trigger surfaces. No risk of one half being orphaned by a partial copy. The harness loads one skill where two existed before, reducing trigger-matching ambiguity.

**What becomes harder:** The SKILL.md is longer (the consolidated `issue-management/SKILL.md` is ~700 lines). The agent must explicitly identify which mode applies to the current turn before acting — this is documented as an anti-pattern ("don't conflate the two modes"). Cross-references that previously pointed at the sibling skill directory must be updated to anchor links within the same file.

**What we're explicitly not promising:** Independence between modes. They share frontmatter, capability tables, and templates by design. Splitting them again later is straightforward (move the section back to a sibling directory + restore cross-links) but counts as a substantive change.

## References

- [`../2026-05-21-114.md`](../2026-05-21-114.md) — the source retrospective.
- [`../../.claude/skills/issue-management/SKILL.md`](../../.claude/skills/issue-management/SKILL.md) — the consolidated SKILL.md applying this pattern.
- [`../../.claude/skills/self-retrospective/SKILL.md`](../../.claude/skills/self-retrospective/SKILL.md) — pre-existing precedent (forward + reprocess modes).
- PR the decision was made in: #114 (specifically commit `c4d4f8d`).
