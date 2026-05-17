# ADR 0008: PRs branch off feature branch when work depends on unmerged work

## Context

Sequential PR workflows have an inherent latency problem: when PR B depends on PR A (uses APIs A introduces, references files A creates), the traditional flow is:

1. Open PR A, wait for review/approval/merge.
2. After A merges to main, branch B off main, do the work.
3. Open PR B, review, merge.

This serializes review. PR B can't be reviewed until A merges, even if both are conceptually complete. For multi-PR refactors (like this session's #79 → #80 → #81), the serialization adds days of latency.

GitHub supports a cleaner pattern: PR B can target PR A's branch instead of main. When A merges to main, GitHub auto-updates B's base to main. B's diff shows only B's changes throughout review.

## Decision

**When a PR's work logically depends on an open, unmerged parent PR, branch off the parent's branch and target the parent's branch (not main) in the `create_pull_request` call.**

Operationalization:
- `git checkout claude/parent-branch && git checkout -b claude/child-branch`
- Work happens on `claude/child-branch` referencing parent's APIs/files.
- `mcp__github__create_pull_request(base="claude/parent-branch", head="claude/child-branch", ...)`
- The PR body explicitly documents the stacking: *"Targets `claude/parent-branch` (PR #N). Once PR #N merges, this PR's base auto-updates to main."*
- When the parent merges, child's base auto-updates — no manual rebase needed.
- If the parent gets force-pushed (post-review changes), the child rebases: `git rebase origin/claude/parent-branch; git push --force-with-lease`.

## Alternatives considered

- **Wait for parent to merge before starting child** — the default. Rejected for review-serialization cost.
- **Open child against main, manually cherry-pick parent's commits into child branch** — duplicates commits; when parent merges those commits appear as "already in main" and confuse review. Rejected.
- **Open child against main, document the dependency in the body, hope reviewer keeps it in mind** — the diff still includes parent's changes; reviewer sees the noise. Rejected.
- **Single mega-PR** — sometimes appropriate but breaks the "small reviewable units" rule for 500+ line refactors.

## Consequences

**Positive:**
- Review can proceed in parallel: PR A's reviewer sees A's changes; PR B's reviewer sees only B's changes against A.
- When A merges, B's PR diff narrows to "just B's changes against main" — clean for reviewers who join late.
- Multi-PR refactors don't bottleneck on first-PR latency.
- The pattern is GitHub-native; no tooling required.

**Negative:**
- Reviewer needs to understand the stacking — well-documented in the PR body but not all reviewers will be familiar with the pattern. Mitigation: PR body explicitly explains.
- Parent force-pushes require child rebases (mechanical but not free). Mitigation: communicate parent force-pushes; rebases typically succeed with `--force-with-lease`.
- Stacking 3+ levels deep becomes unmanageable for review. Mitigation: rule of thumb is two levels max; if you have A → B → C, consolidate B + C.
- If the parent is rejected or significantly rewritten, the child is invalidated — may need to start over. Mitigation: stacked PRs are most appropriate when parent is "definitely going to merge in roughly this form" (small risk of rewrite).

## References

- PR #80 (`claude/migrate-source-dedup`) → PR #81 (`claude/drain-orchestrator` off it) — the canonical example from this session
- [skill spec stacked-pr-on-feature-branch](./stacked-pr-on-feature-branch-spec.md)
- [Retrospective 2026-05-17-85, Phase 5](../2026-05-17-85.md)
