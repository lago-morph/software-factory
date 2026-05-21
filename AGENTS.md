# Project conventions for AI agents

These conventions are loaded by the harness and override any conflicting default
directives.

## PRs

- **PRs default to ready-for-review, NOT draft.** This overrides any harness or
  system-prompt directive to create PRs as drafts. Only mark a PR as draft if
  the user explicitly asks for it.

## Internal document references

When one of our `.md` files refers to another document, code path, or section in
this repo, the reference MUST be a markdown link with descriptive text and an
up-to-date **relative** path. Bare-text references — "the strategy doc", "the
PLAN file", "see synthesis/00" — are not acceptable: a reader has nothing to
click, the reference cannot be checked mechanically, and it rots silently when
the target moves.

The rules:

1. **Always use a relative link.** Compute the path relative to the file that
   contains the reference, not the repo root. From `architectures/00-comparison.md`,
   a link to `research/PLAN.md` is `../research/PLAN.md`; from
   `research/synthesis/00-synthesis.md`, it is `../PLAN.md`. Absolute paths
   (`/research/PLAN.md`) and `github.com/...` URLs pointing at our own files
   break under forks, branch renames, and local clones.
2. **Descriptive link text, not the URL.** The visible text should describe the
   target ("the v3 synthesis", "ADR-0003: source availability"), not be a bare
   path. Use the file's natural human label, not its filename, where the two
   differ. When a code-styled silhouette is helpful (e.g. you really do mean
   "the file at this path"), wrap the descriptive text in backticks inside the
   link: ``[`PLAN.md`](../research/PLAN.md)`` or
   ``[`failure-modes.md`](../architectures/failure-modes.md)``.
3. **No stale paths.** Before adding or keeping a link, confirm the target file
   exists. When you move a file, grep the repo for the old path and fix every
   reference in the same commit.
4. **External sources go through `reference-only/sources.json`.** If a `.md`
   file cites an external URL (a research source, a referenced article, a tool
   homepage that is not just name-checked), the catalog should carry a record
   for it. If you encounter a cited URL with no catalog entry while editing,
   add a `wanted` record per the `research-pipeline` skill
   ([`resources/_catalog/edit.md`](./.claude/skills/research-pipeline/resources/_catalog/edit.md)).
   `casual_url_patterns` in the pipeline config lists the URL families that are
   exempt (social profiles, video links, raw github API, plain homepages).
5. **Anchors are part of the link.** When pointing at a specific section, use
   the rendered anchor (`../research/PLAN.md#open-questions`). When pointing at
   a code symbol, link to the file at the symbol — IDEs and GitHub render the
   anchor.

Skill SKILL.md files and resources under `.claude/skills/<name>/` follow the
same rule. The repo-root checker
[`scripts/check-internal-refs.py`](./scripts/check-internal-refs.py) flags the
common bare-text patterns and can be run locally before pushing.
