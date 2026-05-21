---
name: architecture-failure-mode-gate
description: Owns the per-architecture coverage matrix in `architectures/failure-modes.md` and the CI gate that enforces it. Invoke whenever you (a) edit `architectures/0N-*.md`, (b) edit `architectures/failure-modes.md`, (c) propose a new failure mode that will appear as a row, (d) need to add or remove an architecture alternative, (e) handle a `failure-modes-gate` PR review left by CI, or (f) see one of these phrases — "failure-mode column", "coverage matrix", "F-mode table", "failure-mode gate". Cross-referenced from the research-pipeline skill (any time stage 5 registers a new F-mode). Self-installs its CI workflow on first invocation.
tags: [architecture, ci, governance, failure-modes, self-installing]
allowed-tools: [Bash, Read, Write, Edit]
---

# architecture-failure-mode-gate

This skill owns one tightly-coupled triple:

- The per-architecture coverage matrix in [`architectures/failure-modes.md`](../../../architectures/failure-modes.md) §2.4.
- The architecture alternatives at [`architectures/0N-*.md`](../../../architectures/).
- The CI gate workflow that detects drift between the two.

The discipline: **when you change `architectures/0N-*.md`, you must update column N — and only column N — of the failure-modes table.** When you add a new alternative, add a new column; when you remove one, drop its column. The gate enforces this mechanically so the temptation to "while I'm in here, adjust column 3 too" is removed.

## Pre-flight check (run this first, every invocation) — self-syncing

The skill is self-syncing. The canonical source for the CI workflow is `resources/_workflows/` inside this skill directory. The installed copy under `.github/workflows/` must always match the template — if it doesn't, the installer regenerates it.

Before any task that touches `architectures/` or `failure-modes.md`:

```bash
python .claude/skills/architecture-failure-mode-gate/scripts/install.py --check
```

Exit code:
- `0` — installed and identical to template. Proceed.
- `1` — missing OR drifted. **Auto-fix by running, without asking the user:**
  ```bash
  python .claude/skills/architecture-failure-mode-gate/scripts/install.py --force
  ```
  The install auto-commits with a clear message; push that commit alongside your other work. Then continue.
- `2` — template file itself is missing from the skill. This is a skill-installation defect, not a workflow-drift issue. Surface to the user and stop.

**Do not ask the user before installing/syncing.** The install is mechanical and deterministic — the workflow is regenerated from a template, nothing custom is destroyed. The whole design contract is that copying the skill directory into a fresh repo is sufficient to bootstrap; the LLM enforces that contract by running `--force` on mismatch.

The skill ALSO self-installs reactively: any time you load this skill and notice the workflow file is missing or that `lint-failure-modes.py` is not present at the path the workflow expects, run `install.py --force` before proceeding.

## Schema (enforced by `scripts/lint-failure-modes.py`)

The §2.4 coverage table in `architectures/failure-modes.md` follows a strict schema. The linter rejects anything that drifts from it.

- **Section header:** `### 2.4 Failure mode coverage` — exactly this text starts the validated region.
- **Section end:** `**Coverage column scores ...` — text after this is not validated cell-by-cell (it's the summary section).
- **Table header row:** `| Failure mode | N: ShortName | ... |` where each `N: ShortName` column matches an `architectures/0N-*.md` alternative file by integer index. Column ordering is `N` ascending. `00-comparison.md` and `failure-modes.md` are EXCLUDED from the alternative set.
- **Table body rows:** `| F<K> <Name> | <cell> | <cell> | ... |` with exactly one cell per architecture column. `F<K>` is the unique row identifier — the same number used by the proposing research report. Row order in the table does not matter.

Run the linter locally:

```bash
python .claude/skills/architecture-failure-mode-gate/scripts/lint-failure-modes.py                          # structure only
python .claude/skills/architecture-failure-mode-gate/scripts/lint-failure-modes.py --check-diff origin/main # + diff
```

## Update discipline

### When you modify an existing architecture alternative

Editing `architectures/0N-*.md` (for any N in 1..9) requires updating column N of the failure-modes table — and ONLY column N. The gate hard-checks both directions:

- Arch file changed → column N must have changed.
- Column N changed → arch file 0N-*.md must have been touched in the PR.

If your arch-doc edit genuinely does not affect coverage (a typo fix, a clarification of a non-coverage detail, a citation update), see "Handling the gate review" below — that's the override path, NOT a reason to silently skip the column update.

### When you add a new architecture alternative

1. Create `architectures/0M-<slug>.md` for the new alternative M (next free integer).
2. In `architectures/failure-modes.md` §2.4: add a new column `M: ShortName` at the right of the header row, and add a corresponding cell at the right of every F-mode row.
3. Run `python .claude/skills/architecture-failure-mode-gate/scripts/lint-failure-modes.py` — it will refuse to pass until the alternative count matches the column count.

### When you remove an architecture alternative

1. Delete `architectures/0N-<slug>.md`.
2. In `architectures/failure-modes.md` §2.4: drop column N from the header row and the corresponding cell from every F-mode row.

### When a research report proposes a new F-mode row

This is a row-level event — the gate explicitly does NOT require column-spillover correspondence for row additions or removals. A new row populates cells across all architecture columns; this is expected. See `.claude/skills/research-pipeline/resources/_drain/stage-5-content-processing.md` "Failure-mode discovery and registration" for the canonical procedure (numbering, collision detection, propagation).

### Cell-wording refinements with no arch-doc edit

Sometimes a cell's text is wrong (mis-citation, ambiguous phrasing, stale terminology) and the right fix is a cell-only edit with no architecture-doc change. For this case:

- Add the PR label **`failure-mode-only`** (set via the PR UI or `gh pr edit --add-label`).
- The gate, on its next run, sets `FAILURE_MODE_ONLY=1` for the linter, which permits column edits without a matching arch-doc edit.
- Spillover into multiple columns is STILL blocked — `failure-mode-only` is for one column at a time.

## Handling the gate review

When CI detects a violation, the workflow posts a `REQUEST_CHANGES` PR review (it does NOT fail the check itself — the review is the actionable signal). The body lists the lint errors and links back to this skill.

On receiving such a review, the agent:

1. **Investigate the diff.** Read the arch file changes that triggered the gate. Decide:
   - Does the edit change *what an architecture does* about a failure mode? (e.g., new mitigation primitive, removed primitive, changed level of guarantee, renamed pattern that the coverage cell cites) → MATERIAL.
   - Or is the edit non-coverage-bearing? (typo, formatting, citation fix, rewording that doesn't change the substantive claim about a failure-mode mitigation, expanded prose that elaborates without changing the mitigation set) → NOT MATERIAL.

2. **If MATERIAL:** edit only the corresponding column N of `architectures/failure-modes.md` to reflect the change. Push. The next CI run will dismiss the review automatically.

3. **If NOT MATERIAL:** dismiss the review programmatically and post a justification comment.

   Dismissal via GitHub MCP (preferred — runs as the session's GitHub identity):
   ```
   mcp__github__pull_request_review_write  method=dismiss
     review_id=<from the review event>
     message="<one-sentence justification>"
   ```
   Then post the explanation:
   ```
   mcp__github__add_issue_comment
     body="Dismissed failure-mode gate review: <reason>. The change at <file>:<lines>
           does not affect any column-N coverage claim because <specifics>."
   ```

   Dismissal via `gh` CLI fallback:
   ```bash
   gh api -X PUT /repos/$OWNER/$REPO/pulls/$PR/reviews/$REVIEW_ID/dismissals \
     -f message="Not material: <reason>"
   gh pr comment $PR --body "Dismissed failure-mode gate review: <reason>."
   ```

   The justification comment is the audit trail — future reviewers can grep for "Dismissed failure-mode gate review" to find override decisions.

4. **If you cannot decide,** ASK the human reviewer in a PR comment with the diff highlighted and your two reading options — don't silently dismiss.

## Authoring rules — anti-spillover

The single most-common failure mode of human-authored edits to coverage tables is "while I'm in here, polish column 2's wording too." The lint catches this. The discipline:

- **Edit one column at a time.** Make the arch-doc edit, then make the column edit. Don't reach across rows or columns to "improve" cells unrelated to the arch edit.
- **No bulk reformatting of the table in the same commit as a substantive edit.** If you want to re-sort rows, change the column-header style, or rewrite the surrounding prose, do that as a separate PR labeled `failure-mode-only`.
- **Cite your edit.** When you change a coverage cell, the commit message should name the arch primitive that motivated the change (e.g., "Atelier dropped the reliability-reviewer persona; F13 column 2 updated accordingly").

## Cross-reference from other skills

- [`research-pipeline`](../research-pipeline/SKILL.md) — its stage-5 doc points readers at this skill when registering a new F-mode (row-level event, exempt from column-spillover).

Any future skill that touches `architectures/` or proposes failure modes MUST cross-reference this skill in its own SKILL.md decision tree so authors load both at the same time.

## See also

- [`self-bootstrapping-skill`](../self-bootstrapping-skill/SKILL.md) — the pattern this skill implements (install.py with --check/--force, no-prompt pre-flight, CI gate as installed artifact).
- [`architectures/failure-modes.md`](../../../architectures/failure-modes.md) — the table itself.
- `resources/_workflows/failure-modes-gate.yml` — the installed CI workflow template.
- `scripts/lint-failure-modes.py` — the linter the workflow runs.
- `scripts/install.py` — the installer.
