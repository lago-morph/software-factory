# ADR: Repurpose `good first issue` label as the agent-claim marker

- **ID**: ADR-0a329a8c05
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-21
- **Source retrospective**: ../2026-05-21-114.md
- **PRs covered**: #114

## Context

The `issue-management` skill (PR #114) needs a visible marker on each issue indicating "an agent has claimed this and is working on it." The natural candidate was a dedicated `in-progress` label, but a capability probe (see [SKILL-SPEC-6ffe696187-capability-probe-before-design.md](./SKILL-SPEC-6ffe696187-capability-probe-before-design.md)) confirmed the GitHub MCP server exposes no `create_label` tool — labels can only be applied if they pre-exist in the repo. A second probe enumerated GitHub's 9 default labels and confirmed all 9 are present in `lago-morph/software-factory`: `bug`, `documentation`, `duplicate`, `enhancement`, `good first issue`, `help wanted`, `invalid`, `question`, `wontfix`. Of these, `good first issue` has no project-specific meaning (the repo is not soliciting outside contributions on issues) and is therefore re-assignable without semantic conflict.

The user's secondary requirement was that the marker be **visible at a glance in the issue list view**. GitHub's issue list shows assignee avatars as small circles at the right edge of each row — too small to scan a long list. Labels render as colored pills next to the issue title and are far more legible.

## Decision

Repurpose GitHub's default `good first issue` label as the marker that an agent has claimed an issue, rather than introducing a new `in-progress` label, because the MCP server cannot create labels and the default label has no current semantic use in this project.

The STARTED behavior in the issue-management skill applies the label. The label is removed only by the discard-style closures (DUPLICATE, INVALID, WONTFIX). It is preserved through PR-merge closures (the claim was real and the work landed) and through CLOSED-NO-PR (agent's case-by-case call).

## Alternatives considered

- **Create a dedicated `in-progress` label** — rejected because the GitHub MCP server has no `create_label` tool. The user would have to create the label by hand in the GitHub UI before the skill could use it. That requirement violates the "skill works on first install" principle.
- **Use only the assignee avatar (no label)** — rejected because the avatar is too small to register at issue-list scale. The user explicitly noted this when answering "does the issue visibly change when assigned?" — yes, but only subtly.
- **Apply a non-default label that happens to be present** — there's no such label in this repo; all 9 present labels are GitHub defaults.
- **Apply both `help wanted` and a STARTED comment instead** — rejected because `help wanted` retains its conventional meaning ("we need outside help on this") and repurposing it conflicts more than `good first issue`.
- **Skip the label entirely and rely on the STARTED comment for the claim signal** — rejected because comments don't show up in the list view; the user would have to open each issue to know who claimed it.

## Consequences

**What becomes easier:** No user setup required — the skill works on any repo with default GitHub labels. The claim status is visible in the issue list at a glance. Future agents reading the SKILL.md learn the convention from one place.

**What becomes harder:** A reader who finds the label in isolation (e.g., a contributor who navigates directly to an issue) may briefly assume the original meaning ("good for newcomers"). The skill mitigates this with a note-block in the STARTED behavior section explaining the repurpose, and the comment thread itself carries the unambiguous `[STARTED]` tag.

**What we're explicitly not promising:** The repurpose is local to `lago-morph/software-factory`. If the skill is copied to another repo, that repo's `good first issue` label may carry the original semantic; the convention may need to flip via `modify-behavior mode` for that fork.

## References

- [`../2026-05-21-114.md`](../2026-05-21-114.md) — the source retrospective.
- [`./SKILL-SPEC-6ffe696187-capability-probe-before-design.md`](./SKILL-SPEC-6ffe696187-capability-probe-before-design.md) — the capability-probe skill that surfaced the constraint.
- [`./ADR-a1f4b82e27-resolve-github-mcp-identity-at-runtime-via-get-me-never-hardcoded.md`](./ADR-a1f4b82e27-resolve-github-mcp-identity-at-runtime-via-get-me-never-hardcoded.md) — companion identity ADR from the same PR.
- PR the decision was made in: #114.
