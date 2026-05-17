# ADR 0005: Reports link to source directories, not individual files

## Context

Research reports under `research/` cite catalog sources. The question is what those citations look like as filesystem links:

- **Option A**: link to the specific file: `[main.mhtml](../reference-only/0a7f3b8e00/main.mhtml)`
- **Option B**: link to the directory: `[source](../reference-only/0a7f3b8e00/)`

Real-world events during the session that motivated this question:
- Files inside a record can change: a `partial.html` capture may be replaced by a complete one; a `.txt` text extract may be supplemented by an `.mhtml` browser save.
- File renames happen (the Hamel "Your AI Product Needs Evals" file went from `bfa8bd56ce_docs.github.com__...about-copilot-workspace.html` → `your-ai-product-needs-evals.html` during recovery).
- Reports are immutable as artifacts — once written, the links shouldn't break when the underlying files are improved or replaced.
- The `pointer_to` mechanism for retired records preserves IDs across URL changes, but only if the link is to the directory (the ID).

## Decision

**Reports cite sources by linking to the record's directory (`reference-only/<id>/`), not individual files inside it. The exception is markdown-embedded images (`![alt](../reference-only/<id>/figure-N.png)`), which must reference a specific file for rendering.**

Operationalization:
- `audit-records.py` (PR #86 follow-on or later) scans every `.md` in `research/`, `research/followup/`, `architecture/`, and any other directory of synthesized artifacts. For each link that points into `reference-only/<id>/`, it verifies the link targets the directory itself OR an image file (when rendered via `![alt](...)` syntax).
- Link rot due to file changes is therefore prevented — files inside the directory can be added, renamed, or replaced without breaking citations.

## Alternatives considered

- **Link to individual files** — surface-level explicit ("here's the file"), but fragile across file changes. Rejected.
- **Link to the catalog record by ID, not a path** — e.g., `[source](catalog://0a7f3b8e00)`. Cleanest semantically but requires a custom URL scheme handler. Rejected as over-engineering.
- **Allow both, no enforcement** — convention without checking drifts. Rejected.
- **Allow file links, automatically rewrite to directory links via a precommit hook** — adds magic. Rejected; explicit + audited is cleaner.

## Consequences

**Positive:**
- Files inside `reference-only/<id>/` can be reorganized (partial → full, txt → mhtml, image extraction) without breaking any report citations.
- The `pointer_to` retirement mechanism integrates cleanly: when record A is superseded by record B, B's directory exists and all links to A's directory still resolve (the superseded record's directory remains until cleanup).
- Image embeds are explicitly allowed because they MUST reference a file for rendering; the rule articulates the exception clearly.
- Audit-time enforcement (`audit-records.py`) makes the rule provable, not just stated.

**Negative:**
- Directory links are less informative at-a-glance than file links — readers can't tell from the link what file format the source is in.
- The exception for markdown-embedded images creates an asymmetry users have to remember. Mitigation: the audit script understands both forms.
- Migrating existing reports may require a one-time link-rewriting pass. Currently most reports don't link into `reference-only/` at all (they link to URLs), so the migration cost is small.

## References

- (Forthcoming) `.claude/skills/research-pipeline/scripts/audit-records.py` — implements the link-form check
- (Forthcoming) `.claude/skills/research-pipeline/resources/_catalog/audit.md` — documents the rule for users
- [Retrospective 2026-05-17-85, Phase 10](../2026-05-17-85.md) — user explicitly requested this rule when discussing PR #86 design
