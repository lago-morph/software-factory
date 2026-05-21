# ADR: The concrete-task criterion applies to every entry in a plan doc

- **ID**: ADR-224e9669ef
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-21
- **Source retrospective**: ../2026-05-21-106.md
- **PRs covered**: #106

## Context

`research/PLAN.md`'s `## Future research` section had four entries:

1. **El Kaim Medium corpus (10+ posts)** — "file a single `[fetch-urls]` issue with the 10 post URLs (need to harvest the exact URLs first — the post-index page deliberately omits them in the text export; either the user re-exports with hyperlinks preserved, or a `find / -type f -name 'welkaim.medium.com'`-style scan reveals what we already have, or WebSearch by title)."
2. **Noah Radford "road runner economy"** — "Single GitHub Pages essay; Expected reachable from action without issue; one-page WebFetch may be sufficient."
3. **platform.claude.com Agent Skills 2-of-3** — already done (both URLs in catalog as `have+complete`).
4. **Residuals** — LukePM (already drained), Schillace compounding teams (already drained), and three jaymin-book YouTube videos (require a transcript-extraction service the project does not currently have).

Each was framed as a "future research" item. But only (2) is actually a concrete task an agent can execute — file the URL, fetch, drain. (1) is upstream of a task: it needs URL harvesting first, which is itself not specified ("either re-export, or scan, or WebSearch"). (3) is done. (4) is partly done and partly blocked on tooling the project doesn't have.

The user articulated the general rule when reviewing cleanup-plan v2: "37 and similar entries, there is only work if you can tell me exactly what to do. Otherwise it isn't a task. Use this criteria for all steps."

## Decision

Every entry in a plan doc must be a concrete, executable instruction; entries that cannot be reduced to exactly-what-to-do are either moved to a status tracker (sources.json wanted record for source items) or deleted from the plan.

"Concrete, executable" means: exact file paths, exact actions, exact commands or thresholds, an unambiguous owner (the agent, the user, or a named external party). Items requiring upstream investigation before they can be executed are not yet tasks; they become tasks once the investigation lands.

## Alternatives considered

- **Keep aspirational / wishlist entries in plan docs, marked with a `[?]` or `wishlist:` prefix.** Rejected: this is what the pre-cleanup state was, and it produced indefinite accretion. Wishlist items never get pruned because nobody owns deciding when to prune them. The clear partition rule ("task or not") is easier to enforce.
- **Allow non-concrete items but require an "unblock condition" field.** Rejected: this is a heavier rule (per-item structured field) that solves the same problem the simpler rule solves (just delete; if it matters, it'll come back as a real task with a real owner).
- **Apply the criterion only to "high-level" sections like §5 work-remaining; allow wishlist content in dedicated `## Future research` sections.** Rejected after testing: the cleanup ended up deleting the entire `## Future research` section anyway because most entries failed the criterion. Carving out a sandbox for wishlist content turns out to enable the rot, not prevent it.

## Consequences

**Easier:**
- Plan docs become trustworthy as work queues. Every entry is something an agent could pick up and execute.
- Pruning is mechanical: re-run the criterion on each entry periodically; demote or delete failures.
- New agents reading the plan don't waste time on items that aren't tasks.

**Harder:**
- "Aspirational" or "long-term ideas" content has no home in plan docs. It either becomes a sources.json wanted record (if it's a source), a GitHub issue (if it's a feature idea with an owner), an ADR (if it's a decision to be made), or it's lost. The last case is acceptable: if nobody cares enough to write it up in a more concrete register, it probably wasn't worth tracking.
- Cleanup passes have to apply the criterion entry-by-entry, which is more work than skimming for `~~strikethrough~~` markers.

**Trade-off accepted:** loss of "scratchpad space" in plan docs in exchange for plan docs that are trustworthy as work queues.

## References

- [`../2026-05-21-106.md`](../2026-05-21-106.md) — the source retrospective.
- [`./AGENTS-MD-d38e1d58b3-concrete-task-criterion.md`](./AGENTS-MD-d38e1d58b3-concrete-task-criterion.md) — the corresponding AGENTS.md rule.
- [`./SKILL-SPEC-d5f8b37eeb-plan-doc-curation.md`](./SKILL-SPEC-d5f8b37eeb-plan-doc-curation.md) — Step 3 of the plan-doc-curation workflow applies this criterion.
- PR the decision was made in: #106.
