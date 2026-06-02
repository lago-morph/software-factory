# Architecture Decision Records

This directory holds the project's Architecture Decision Records (ADRs):
numbered, dated, immutable markdown files that record binding
architectural choices and their context.

The conventions, lifecycle rules, and authoring workflow are defined by
the [`adr` skill](../../.claude/skills/adr/SKILL.md). Run the link
checker before committing a new ADR:

```bash
python3 .claude/skills/adr/scripts/check_adr_links.py docs/adr/
```

## Index

| ID | Title | Status | Date |
|----|-------|--------|------|
| [0000](./0000-template.md) | Template | n/a | — |
| [0001](./0001-fetch-blocked-urls-mechanism.md) | Use `fetch-blocked-urls` action for sandbox-blocked sources | Accepted | 2026-05-11 |
| [0002](./0002-three-layer-research-pipeline.md) | Three-layer research-to-architecture knowledge pipeline | Accepted | 2026-05-21 |
| [0007](./0007-advisory-ci-gates-emit-dismissible-pr-reviews.md) | Advisory CI gates emit dismissible PR reviews, not failing checks | Accepted | 2026-05-21 |
| [0008](./0008-self-installing-pretooluse-hooks-for-skill-load-enforcement.md) | Self-installing PreToolUse hooks as the canonical mechanism for skill-load enforcement | Accepted | 2026-05-21 |
| [0009](./0009-help-wanted-label-as-permanent-marker-of-agent-authored-issues.md) | Repurpose the GitHub default `help wanted` label as the permanent marker of agent-authored issues | Accepted | 2026-05-21 |
| [0067](./0067-dual-track-per-component-v4-layout.md) | Dual-track per-component v4 spec/plan layout with a _meta decision ledger | Accepted | 2026-05-30 |
| [0068](./0068-organize-v4-build-order-docs-by-product.md) | Organize v4 build-order documentation by adopted product, not by dependency phase | Accepted | 2026-06-01 |
| [0069](./0069-spec-scenarios-system-triangle-evaluation-invariant.md) | The spec–scenarios–system triangle as the evaluation invariant for unattended self-building | Accepted | 2026-06-02 |

## Conventions in one screen

- **Filename**: `NNNN-kebab-title.md`, zero-padded to 4 digits, numbers
  permanent (never reuse — not even for abandoned proposals).
- **H1**: `# ADR NNNN: Title in Sentence Case` (matches the agent-os
  convention).
- **Section order**: Status / Date / Context / Decision /
  Alternatives considered / Consequences / References. Heading case is
  lowercase `c` in "Alternatives considered" — preserved for anchor-slug
  compatibility.
- **Internal links are relative.** No `https://github.com/.../blob/main/...`
  for repo content. External sources (papers, blog posts) use absolute URLs.
- **Direct subsection linking** in References is encouraged for dense
  cross-references: one bullet can name a target file and then carry
  multiple anchor links to sections within it. See ADR-0001's References
  section for an example.
- **Immutable after Accepted.** Substantive changes require a superseding
  ADR. The only legal in-place edits are: Status changes (to Deprecated or
  `Superseded by ADR-NNNN`), and typo / link fixes.
- **Bidirectional supersession.** When ADR-NNNN supersedes ADR-MMMM, both
  files are updated in the same commit: MMMM's Status changes to
  `Superseded by ADR-NNNN`.

## When to write a new ADR

- A decision affects multiple files / lasts beyond this session.
- A default tool, library, framework, or pattern is being chosen.
- A non-obvious choice is being made where the next agent might second-guess
  it without context.
- A prior decision is being reversed.

When in doubt, write one. The cost of an extra ADR is small; the cost of a
silent re-decision two months later is large.
