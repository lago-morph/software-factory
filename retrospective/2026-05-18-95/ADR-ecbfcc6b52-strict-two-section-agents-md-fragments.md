# ADR: Per-rule agents-file fragments use a strict two-section format with the ID in the filename only

- **ID**: ADR-ecbfcc6b52
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-18
- **Source retrospective**: ../2026-05-18-95.md
- **PRs covered**: #95

## Context

Each retrospective historically proposed 5–15 additions to the project's `AGENTS.md` via a single consolidated `AGENTS-suggestions.md` file with `## Suggestion N:` sections, each containing the rule and a "Why this earns its place" persuasion paragraph. To enable a downstream CI/CD pipeline to assemble selected rules into the canonical `AGENTS.md` mix-and-match, the consolidated file was split into one file per rule.

The fragment format went through three iterations within PR #95:

1. **First iteration**: rule body in a blockquote under H1 title, with `**ID**` and `**Source retrospective**` metadata bullets; "Why this earns its place" persuasion moved to Part 3 of the retrospective report.
2. **Second iteration** (after user clarification): same format, but with `AGENTS-MD-` filename prefix instead of `AGENT-`.
3. **Third iteration** (user changed their mind): no metadata bullets in the file; body is exactly two H1 sections — `# agent instruction` and `# justification` — and nothing else. The ID lives in the filename only.

The final iteration was driven by the realization that a downstream CI/CD assembler needs a *strict structural contract* (machine-parseable boundaries) rather than a soft convention ("please don't use ## here"). And by the realization that reviewers reading a per-rule file in isolation (via grep results or GitHub's file viewer) need the justification co-located with the rule, not buried in Part 3.

## Decision

Each per-rule `AGENTS-MD-<hash>-<kebab-name>.md` fragment has a strict two-H1-section body: `# agent instruction` (the rule text the CI/CD assembler concatenates into `AGENTS.md`) followed by `# justification` (the persuasion text the assembler strips out). No metadata bullets appear inside the file body; the `AGENTS-MD-<hash>` ID is encoded in the filename only. The canonical template is shipped at `resources/template-agents-md-rule.md`; freehand authoring is an anti-pattern.

The retrospective report's Part 3 duplicates both sections inline for retro-review convenience, with a link to the per-rule file under each suggestion heading.

## Alternatives considered

- **Keep `**ID**` and `**Source retrospective**` metadata bullets in the file body.** Rejected: the bullets complicate the CI/CD assembler's parsing (it has to know to skip them) and provide no benefit not already covered by the filename + `<!-- AGENTS-MD-<hash> -->` comments the assembler can emit into the generated `AGENTS.md`.

- **Put the justification only in Part 3, leave the per-rule file rule-only.** Rejected: a reviewer who finds a per-rule file via grep or GitHub's file viewer has no context for why it exists. The justification stays with the rule.

- **Use HTML comments (`<!-- BEGIN RULE -->...<!-- END RULE -->`) to mark the assembler boundary.** Rejected: less human-readable than H1 headings, and the H1 headings already do the job machine-parseably.

- **Soft convention ("the body has no ## headers, just paste the rule").** Rejected: parsing depends on convention discipline; drift across 50+ retros silently breaks the assembler. The strict contract is robust.

## Consequences

- **Strict format discipline required.** Every per-rule file must follow the exact two-section structure. The template in `resources/template-agents-md-rule.md` enforces this for new files; reprocess mode enforces it for legacy `AGENTS-suggestions.md` splits.
- **The assembler is trivially correct.** A `grep` for `^# agent instruction`, an `awk` that captures until the next `^# ` line, and concatenation of those captures is the entire AGENTS.md assembly. No markdown parser needed.
- **The justification is duplicated** between the per-rule file (under `# justification`) and Part 3 of the retro report. Acceptable: the per-rule file is the source of truth for the assembler; Part 3 is the source of truth for the retro reviewer. Different audiences, both want the content.
- **Reprocess mode gains a third responsibility.** When migrating a legacy retro's `AGENTS-suggestions.md`, split into per-rule files AND copy the entire original body verbatim into Part 3 (heading levels demoted) AND delete the consolidated file. Already implemented in PR #95.

## References

- [`../2026-05-18-95.md`](../2026-05-18-95.md) — the source retrospective.
- [`./ADR-d220ee7467-uniform-type-hash-name-filename-ordering.md`](./ADR-d220ee7467-uniform-type-hash-name-filename-ordering.md) — companion ADR on the filename ordering this fragment naming depends on.
- `.claude/skills/self-retrospective/resources/template-agents-md-rule.md` — the canonical template.
- `.claude/skills/self-retrospective/SKILL.md` Step 6 — forward-mode authoring procedure.
- `.claude/skills/self-retrospective/SKILL.md` "Reprocess mode" step 3 — migration procedure for legacy `AGENTS-suggestions.md`.
- PR #95: lago-morph/software-factory#95 — the PR that arrived at the final format.
