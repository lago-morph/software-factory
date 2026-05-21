# ADR 0003: Source-availability tracking lives in sources.json, not in plan docs

- **ID**: ADR-c2922a493c
- **Status**: Accepted
- **Date**: 2026-05-21

## Context

[`research/PLAN.md`](../../research/PLAN.md) v0.17 carried three different registers of source-availability state: §4.3 ("Low priority — background completeness") with a table of "Path-B-only" and "retry-eligible" URLs, §6.2 (in-flight tracking) with rows for specific URLs, and a `## Future research` section with prose entries pointing at sources we wanted to fetch but hadn't. None of these matched the actual catalog state. Both `platform.claude.com/docs/en/agent-skills/best-practices` and `.../security` were listed as outstanding Path-B-only URLs but the catalog had them as `have+complete`. The Schillace "I have seen the compounding teams" and LukePM "The Software Factory" entries in the residuals section were already drained as records `83fdf58ee6` and `44d4c1be80` respectively, both cited in published reports.

Two registers of truth always drift; this case had three, and the drift was on the order of months. Cleaning up the divergence took a full session of cross-referencing, only to conclude that the cleanest fix was to remove the source-status tracking from PLAN.md entirely and rely on [`reference-only/sources.json`](../../reference-only/sources.json) (which is automatically validated, has a schema, has lint rules, and is the input the regen-sources-md workflow consumes).

## Decision

Wanted-source tracking lives exclusively in [`reference-only/sources.json`](../../reference-only/sources.json) via wanted-status records; plan documents ([`research/PLAN.md`](../../research/PLAN.md), [`research-plan.md`](../../research-plan.md)) never carry URL-tracking tables or outstanding-URL lists.

## Alternatives considered

- **Keep §4 in PLAN.md but cross-check it on every cleanup pass.** Rejected: this is what the prior status quo was, and it produced 4+ month drift. Manual cross-checking is exactly the labour the rule is trying to eliminate.
- **Move source-tracking to a new dedicated file (e.g., `research/outstanding-urls.md`).** Rejected: produces a third register and inherits the same drift problem unless validated mechanically. `sources.json` already has the schema + lint + regen infrastructure; adding a parallel system is duplication.
- **Treat plan docs and sources.json as different views of the same data, with a script that syncs them.** Rejected: complexity outweighs benefit. The mental model "plan = narrative work; sources.json = source state" is simple; a sync-script approach requires a maintainer's attention indefinitely.

## Consequences

What this buys:

- `sources.json` is the single answer to "what sources do we have / want / have-tried-and-lost?" — no need to consult three documents.
- PLAN.md becomes shorter and more focused on actual decisions / non-trivial work items.
- Lint catches drift between catalog and reports automatically; there's no manual cross-check loop.

What this costs:

- Adding a wanted source now requires going through the [`research-pipeline`](../../.claude/skills/research-pipeline/SKILL.md) skill's `_catalog/edit.md` patterns rather than just typing a bullet into PLAN.md. Marginal cost: ~30 seconds per addition, vs zero.
- Readers of PLAN.md who want to know "what's outstanding" have to consult `sources.json` (via `sources.md` browse view, or `jq` queries). One extra step.

Trade-off accepted: the schema-enforced single register of truth is worth losing the ability to scribble a quick TODO bullet into PLAN.md.

## References

- [`retrospective/2026-05-21-106.md`](../../retrospective/2026-05-21-106.md) — the source retrospective; full draft at [`retrospective/2026-05-21-106/ADR-c2922a493c-sources-json-is-source-of-truth-for-source-availability.md`](../../retrospective/2026-05-21-106/ADR-c2922a493c-sources-json-is-source-of-truth-for-source-availability.md).
- [`.claude/skills/research-pipeline/SKILL.md`](../../.claude/skills/research-pipeline/SKILL.md) — catalog edit conventions this ADR depends on.
- [PR #106](https://github.com/lago-morph/software-factory/pull/106) — the cleanup-plan PR that surfaced the divergence.
