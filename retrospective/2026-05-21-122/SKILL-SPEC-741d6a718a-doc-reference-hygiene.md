# Spec: `doc-reference-hygiene`

- **ID**: SKILL-SPEC-741d6a718a
- **Source retrospective**: ../2026-05-21-122.md

## Intent

Run an audit-and-fix loop for internal markdown references across a documented in-scope set of `.md` files, combining git-log rename detection, repo-relative-vs-file-relative dual resolution, batch transform of backtick-wrapped paths into descriptive markdown links, opportunistic external-citation backfill into `reference-only/sources.json`, and a final pass with `scripts/check-internal-refs.py` to verify no broken links remain. The skill exists because issue #104 surfaced ~1093 backtick-wrapped path references across ~307 markdown files in this repo and several recurring categories of stale paths (notably `research/00-synthesis.md` → `research/synthesis/00-synthesis.md` per ADR-0004, and retired `research/blocked-urls*.md` files). Manual sweep is unworkable; an ad-hoc script run leaves stale paths silently in place. The skill is the durable workflow that ties the existing scripts to a disciplined scope decision.

## Trigger

Direct user phrases:

- "fix internal references / doc links / cross-references in `<scope>`"
- "audit doc links"
- "convert bare paths to markdown links"
- "are my doc references current?"
- "run the internal-refs check"

Proactive triggers:

- A user moves or renames a `.md` file with grep-able cross-references elsewhere in the repo.
- A user adds a "Last updated" or "rename pass" note to a navigational hub (e.g., `research/INDEX.md`, `research/PLAN.md`).
- An ADR is adopted that documents a directory move (e.g., the synthesis subdir convention).

Negative triggers (do NOT activate):

- The user is editing a single `.md` file's prose — small in-line edits don't need the full audit.
- The reference change is inside a code block or YAML literal — those are intentional non-references.
- The target directory is one of the pipeline's input drop zones (`research/manual/`, `research/fetched/`, `reference-only/<id>/`).

## Inputs

- A scope specifier: directory prefixes, file names, or "all in-scope" (the project's living-docs + research-reports set as declared in the trigger conversation).
- The current working tree (clean or dirty — the skill warns on dirty).
- Optional: explicit known rename pairs from the user (e.g., "X.md moved to Y/X.md").

## Outputs

- File-level edits in the in-scope set converting bare-text backtick paths into ``[`label`](file-relative/path)`` links.
- A commit on the current branch with a clear "convert bare-text refs to relative markdown links" message naming the scope.
- A summary report to chat: files touched, total conversions, stale-path renames applied, remaining broken-link count (0 if clean, with a list otherwise), and the diff vs `origin/main` summary.
- Optionally: a follow-up issue if material work remains out of session scope.

## Workflow

1. **Verify pre-flight scripts exist.** Confirm [`scripts/check-internal-refs.py`](../../../scripts/check-internal-refs.py) and [`scripts/fix-internal-refs.py`](../../../scripts/fix-internal-refs.py) are present and executable. If either is missing, this skill is operating in a different repo than the canonical one — surface to user and stop.
2. **Confirm the AGENTS.md convention is loaded.** The "Internal document references" section of [`AGENTS.md`](../../../AGENTS.md) defines the rule (descriptive text + file-relative path, no bare-text, no stale paths). If absent, surface to user — without the convention, this skill is undercut at the project level.
3. **Establish scope.** Ask the user (via AskUserQuestion + per the `issue-management` skill if an issue is in flight): living-docs-only, living-docs + research reports, everything, or convention-only. Record the choice. The default exclusions are `retrospective/`, `harness/runs/`, `reference-only/`, `research/manual/`, `research/fetched/`.
4. **Detect known renames from git history.** Run `git log --diff-filter=R --name-status --all -- '*.md'` for the top stale paths (use `check-internal-refs.py` first to enumerate candidates). For each rename detected, also check the most recent ADR commits (`git log --all -- 'docs/adr/'`) for moves that an ADR ratifies.
5. **Apply known renames first.** Use a sed-style Python pre-pass: for each `(stale, current)` pair, walk in-scope files and rewrite both the backtick form (`` `stale` `` → `` `current` ``) and any existing markdown link target (`(stale)` or `(../stale)` → `(current)` or `(../current)`).
6. **Run the bulk transform.** Invoke `python scripts/fix-internal-refs.py --apply <in-scope paths>`. The script converts backtick-paths whose target resolves (file-relative first, then repo-relative) to ``[`stem`](file-relative/path)`` links and skips wildcards / template placeholders.
7. **Verify with the checker.** Run `python scripts/check-internal-refs.py --only BROKEN_LINK --include <in-scope prefixes>`. Expect zero findings. If non-zero, classify each: rename-detectable (loop back to step 4), genuinely-deleted (decide: redirect to a current mechanism, or remove the reference).
8. **Handle genuinely-deleted targets.** For each unique stale reference with no replacement (e.g., retired inventory files), edit the references manually to point at the current mechanism (e.g., "issues labelled `fetch-urls`") rather than leaving broken links.
9. **Opportunistic external-citation backfill.** While editing, if you encounter cited external URLs that don't have a `reference-only/sources.json` record, add a `wanted` record per the `research-pipeline` skill's [`resources/_catalog/edit.md`](../../../.claude/skills/research-pipeline/resources/_catalog/edit.md). Do NOT run a full `check-source-refs.py` audit unless explicitly asked — that's a separate concern.
10. **Commit and surface.** Commit with a clear message naming the conversion count, the scope, and any rename pre-passes. Print a one-paragraph summary to chat: files touched, conversions applied, broken-link count (must be 0), and a list of any out-of-scope follow-ups documented for later.

## Concrete examples

### Example 1: issue #104 — full living-docs + research reports sweep

User: "fix issue 104" → references convention plus bulk fix.

Operations applied (from this very retrospective's session):

- Scope: living docs (AGENTS.md, CLAUDE.md, research-plan.md, architectures/, docs/adr/, research/PLAN.md, research/INDEX.md) plus all research/* reports.
- Renames detected from git log + ADR-0004: `research/00-synthesis.md` → `research/synthesis/00-synthesis.md`; `research/13-round-2-synthesis.md` → `research/synthesis/13-round-2-synthesis.md`. Applied via Python sed-pass to 16 files.
- Bulk transform: `python scripts/fix-internal-refs.py --apply <73 files>` → 476 conversions across 58 files.
- Broken-link verification: `python scripts/check-internal-refs.py --only BROKEN_LINK --include AGENTS.md --include CLAUDE.md --include research-plan.md --include architectures --include docs/adr --include research` → `✓ no issues found across 73 scanned files`.
- Genuinely-deleted references (`research/blocked-urls.md`, `research/blocked-urls-round-2.md`, `research/unfetched-sources.md`) redirected to current mechanism (GitHub issues labelled `fetch-urls`) in ADR-0001 and `research/INDEX.md`.
- Commit message: `research+architectures: convert bare-text refs to relative markdown links` with a structured body naming scope decisions and the renames.

### Example 2: single-skill cross-reference cleanup

User: "fix the cross-references in `.claude/skills/research-pipeline/`".

Operations:

- Scope: `.claude/skills/research-pipeline/**/*.md`.
- Detect renames: none in recent history for this subtree.
- Bulk transform: `python scripts/fix-internal-refs.py --apply .claude/skills/research-pipeline/`. Output: small number of conversions because most paths inside skills are already linked or are skill-relative (which the convention treats as a known exception — flag for user).
- Broken-link verification: one off-by-one finding (`../../../../fetch-blocked-urls/SKILL.md` — should be `../../../fetch-blocked-urls/SKILL.md`). Manual fix.
- Skill-relative paths: surface to user — should those be in scope? Convention says file-relative; skill-relative is a known implicit base. Decision: leave for separate ticket unless user explicitly wants them migrated.

## Anti-patterns

- **Running the bulk transform without scope discussion.** The convention's strict reading covers 307 .md files and ~1093 references; doing all of it in one session produces low-quality, low-review-effort output. The scope-decision step is mandatory.
- **Trusting `git log main..HEAD` to compute "what changed".** Local `main` is often stale relative to `origin/main`; always use `origin/main` as the diff base. (This bit the session reviewing PR #122 — apparent "frontmatter added" turned out to already be on `origin/main`.)
- **Auto-rewriting backtick paths containing wildcards or template placeholders.** Paths like `architectures/0N-*.md`, `docs/adr/NNNN-kebab-title.md`, `<topic>-requirements.md` are documentation patterns, not references. The `fix-internal-refs.py` script skips these; if you write a one-off sed, add the exclusion.
- **Declaring a path stale without checking git history.** Before redirecting a reference, run `git log --all --follow -- <path>` to see if the file was renamed. ADR-0004 (synthesis subdir convention) is the example — 20 of the most-common stale references were a single rename event.
- **Editing an ADR's Context section to "update" the historical layout.** ADRs are immutable historical records. Update the Decision-era artifacts (link maintenance is OK in References), but never rewrite Context to retroactively reflect the post-decision world.

## Acceptance criteria

- [ ] `python scripts/check-internal-refs.py --only BROKEN_LINK --include <scope>` returns 0 issues after the skill completes.
- [ ] Every `.md`-to-`.md` backtick path in the scope is either (a) a link, (b) a wildcard/template placeholder, (c) a documented exception (e.g., skill-relative path inside a skill resource).
- [ ] The commit message names the scope, the rename pre-passes applied (if any), and the conversion count.
- [ ] A one-paragraph chat summary lists files-touched, conversions-applied, broken-link-count-at-end, and any out-of-scope follow-ups.
- [ ] No `.md` file outside the declared scope is modified.

## Files this skill creates / modifies

- The in-scope `.md` files — converts bare-text backtick paths into markdown links; fixes stale renames; redirects genuinely-deleted references to current mechanisms.
- `reference-only/sources.json` — opportunistically, for any external URL encountered without a catalog record.
- A new commit on the current branch with a structured message.

## References

- [`scripts/check-internal-refs.py`](../../../scripts/check-internal-refs.py) — the audit tool.
- [`scripts/fix-internal-refs.py`](../../../scripts/fix-internal-refs.py) — the batch transformer.
- [`AGENTS.md`](../../../AGENTS.md) `## Internal document references` — the project-level rule the skill enforces.
- [`docs/adr/0004-synthesis-subdir-and-based-on-commit-header.md`](../../../docs/adr/0004-synthesis-subdir-and-based-on-commit-header.md) — example rename ADR the skill detects and respects.
- [`.claude/skills/research-pipeline/SKILL.md`](../../../.claude/skills/research-pipeline/SKILL.md) — pairs with this skill for external-citation backfill.
