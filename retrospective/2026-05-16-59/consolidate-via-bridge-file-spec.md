# Spec: `consolidate-via-bridge-file`

## Intent

When a repo has accumulated several stale or partially-superseded auxiliary files whose content overlaps with a single canonical doc (PLAN.md, ROADMAP.md, INDEX.md, design doc, etc.), the natural impulse is "delete the stale files and update the canonical doc in one PR." That impulse silently destroys load-bearing audit-trail content: the canonical doc covers ~70% of what the auxiliary files said, the deleted ~30% (per-row outcome tables, operational scripts, issue-body templates, manual procedures) vanishes.

This skill names the safer pattern: **two PRs, a temporary bridge file in between**. PR1 deletes the auxiliary files and creates `<target>-sync.md` (a bridge file) whose appendices preserve the ~30% verbatim and whose body classifies the rest into "already in target" / "missing from target — flag for fold-in." PR2 folds the flagged items into the canonical doc, marks the bridge disposable. The user gets a clean review at each step, the bridge file is git-traceable, and no information is silently dropped.

In the session that produced this skill, the bridge was `research/plan-sync.md`; the canonical doc was `research/PLAN.md`. Nine files were retired in PR #58 (one bridge file created with 4 appendices); PLAN.md was synced in PR #59 (one version bump, 95 inserts, 38 deletes, version-history row added).

## Trigger

**Direct triggers — activate immediately:**
- "Consolidate these files into one."
- "Clean up X, Y, Z and capture what I'd need to update PLAN.md."
- "Retire these stale files."
- Any request to delete ≥3 auxiliary files that overlap with a single canonical doc.

**Proactive triggers — offer the skill:**
- The user is about to delete or move 3+ files that look like they share content with a known canonical doc.
- The repo's `research/` or `docs/` directory has accreted "round-N-notes.md" / "log.md" / "next-steps.md" siblings that are now stale.

**Negative triggers — do not use:**
- A single stale file → just delete it; bridge is overhead.
- Files that have nothing to do with a canonical doc (the bridge serves no purpose).
- The user explicitly says "do it in one PR."

## Inputs

- A list of files to consolidate (the auxiliary set).
- A target canonical doc (the file that should absorb the load-bearing content).
- Optional: the user's explicit instruction about whether to delete the originals (default: yes, after preserving in the bridge).

## Outputs

**PR1 (consolidation):**
- `N` files deleted.
- One new file: `<target-basename>-sync.md` at the same path as the target. Body classifies the auxiliary content; Appendices A–N preserve the verbatim ~30% that doesn't fit in prose form (tables, scripts, templates, procedures).
- PR opened, merged.

**PR2 (sync):**
- The canonical doc updated: version bumped, new sections added where the bridge flagged "missing from target," section references redirected to the bridge's appendices for archived content.
- Bridge file's status updated to "disposable" (an in-flight tracking row marks the trigger for its deletion).
- PR opened, merged.

## Workflow

### PR1 — consolidation

1. Read every auxiliary file in the input list. Note: date, purpose, what's still load-bearing, what's superseded.
2. Read the canonical doc in full. Build a mental map of which sections of the canonical doc could absorb which fragments of the auxiliary files.
3. Estimate the percentage of auxiliary content already in the canonical doc. If it's <20%, the auxiliary files are still load-bearing — the bridge approach is wrong; just leave them. If it's >90%, the bridge is overhead — just delete the auxiliary files with a note in the commit message. The sweet spot is roughly 40%–85%.
4. Create `<target-basename>-sync.md` adjacent to the canonical doc. Body structure:
   - **§1 — what is missing from canonical doc and should be added** (numbered list, each item with a section-mapping recommendation like "fold into §X.Y" or "new subsection §X.Z").
   - **§2 — what is ALREADY in canonical doc** (traceability bullets; helps the future sync agent skip duplicate work).
   - **§3 — per-file disposition** (one subsection per auxiliary file, summarizing what was preserved where).
   - **Appendices A–N — verbatim preservation** of any content that resists prose form: per-URL outcome tables, runnable scripts, issue-body templates, operational procedures. These are the safety net; if the sync PR drops the ball, the appendices are still there.
5. Delete the auxiliary files in the same commit. Use `rm <file>` rather than `git rm` to keep the diff symmetric with the create.
6. Commit message: "Consolidate <auxiliary-file-class> into <bridge-file-name>". Body should list every deleted file by name (so the merge commit search-indexes them).
7. Open PR. **As ready-for-review, not draft** (see corresponding AGENTS.md rule). PR body must include a "what plan-sync.md flags as still missing from CANONICAL_DOC" section pointing at §1 of the bridge.
8. Merge.

### PR2 — sync

1. Read the bridge file (specifically §1) and the canonical doc.
2. Plan the edits as a numbered list of named passes — header bump, section additions, file-reference updates, cleanup of stale phrasing. Don't start editing until the plan is written.
3. Execute the passes via `Edit` (not `Write` — the canonical doc is long and `Edit` minimizes context cost).
4. After all named passes, **re-read the canonical doc end-to-end at least once** (see the `post-edit-reread-pass` skill). Expect to find 3–6 drift issues that single-pass editing missed: stale references in sections you didn't intend to touch, broken cross-references, out-of-order chronological tables. Fix each. Loop until a full pass surfaces nothing new.
5. Update the canonical doc's version-history row to record the sync. Cite the bridge file by name and list which of its §1 items were folded in.
6. Add a row in the canonical doc's in-flight tracking table (or equivalent) marking the bridge file as "disposable, awaiting user confirmation to delete."
7. Commit, push, open PR (ready-for-review). PR body should reference PR1's number and summarize the sections rewritten.
8. Merge.

### After PR2 merges

The bridge file can be deleted by the user. Don't preemptively delete it in PR2 — the user may want to spot-check appendices for completeness before letting it go. The "disposable" row in the canonical doc's in-flight tracking table is the explicit trigger.

## Concrete examples

### Example 1 — the originating session

**Auxiliary files (9):** `user-next-steps.md` (root), `research/blocked-urls.md` (v5), `research/blocked-urls-round-2.md`, `research/blocked-urls-round-6.md`, `research/blocked-urls-round-7.md`, `research/blocked-urls-round-8.md`, `research/fetch-from-browser.sh`, `research/next-fetch-batch.md`, `research/unfetched-sources.md`.

**Canonical doc:** `research/PLAN.md` (v0.12, 440 lines).

**Coverage estimate:** ~70% of auxiliary content already in PLAN.md.

**Bridge file produced (PR #58):** `research/plan-sync.md` with 4 appendices:
- Appendix A — per-round per-URL outcomes (compressed from the 5 `blocked-urls*.md` files).
- Appendix B — verbatim body of `fetch-from-browser.sh`.
- Appendix C — round-8 `[fetch-urls]` issue-body template.
- Appendix D — Path-A/B/C manual-fetch operational procedures.

§1 of the bridge flagged 8 items as "missing from PLAN.md": definition-of-research-phase-complete checklist, in-flight tracking table, refined Path-B-only vs retry-eligible categorization, cross-corpus lessons R7.3 / R8.4, fetch-loop-tooling section rewrite, future-research-wishlist residuals.

**Sync (PR #59):** PLAN.md bumped to v0.13. New sections: §5.0 (the definition-of-done checklist), §6.2 (in-flight tracking). Rewritten: §4.3 (Path-B table), §7 (fetch-loop tooling pointers). Folded: cross-corpus lessons into §3.3 + §6.1. 6 re-read passes; 6 drift issues caught and fixed (out-of-chronological-order version table; stale "Cherny remainder outstanding" in 3 separate places; §3.5 listed as live when it was resolved; §3.6 missing from live-items list).

### Example 2 — hypothetical small case

**Auxiliary files (3):** `docs/migration-notes-2025.md`, `docs/migration-todo.md`, `docs/migration-postmortem.md`.

**Canonical doc:** `docs/MIGRATIONS.md`.

**Coverage estimate:** ~50%.

**Bridge file produced (PR1):** `docs/MIGRATIONS-sync.md` with 2 appendices:
- Appendix A — chronological action log from the three deleted files (some entries already in MIGRATIONS.md; the ones that aren't are flagged in §1).
- Appendix B — the postmortem analysis verbatim (didn't have a home in MIGRATIONS.md but is referenced by an open RFC).

§1 flagged 3 items as "missing from MIGRATIONS.md": a runbook for the rollback case, two failure-mode entries that should be folded into the postmortem section.

**Sync (PR2):** MIGRATIONS.md gets a new "Rollback runbook" section; two new failure-mode entries in §"Failure modes". Bridge marked disposable.

## Anti-patterns

- **Doing it in one PR.** The whole point of the bridge is that the deletion and the absorption are reviewed separately. If they're in one PR, the reviewer can't tell what was preserved vs. what was silently dropped.
- **Bridge file with no appendices.** The appendices are the safety net. A bridge file that's all prose has no protection against the sync agent missing something; the verbatim appendices guarantee the load-bearing content is recoverable from the bridge even if §1 is wrong.
- **Deleting auxiliary files via `git rm`-then-commit and creating the bridge in a separate commit.** Same diff hygiene reason as the one-PR anti-pattern: each diff should tell a complete story. A reviewer reading "Delete 9 files" with no creation in the same commit cannot verify the consolidation; reading "Delete + Create bridge" together, they can.
- **Single-pass editing of the canonical doc in PR2.** Long status docs always have cross-section drift after multi-section edits. Always re-read; expect to find issues. The session that produced this skill caught 6 drift issues across 3 re-read passes; single-pass would have shipped them.
- **Preemptively deleting the bridge file in PR2.** The user gets to verify the sync is faithful before retiring the safety net. Mark it disposable; let the user pull the trigger.
- **Skipping the §2 "already in canonical doc" traceability in the bridge.** The future sync agent will otherwise re-extract content that's already there, padding the canonical doc with duplicates.
- **Estimating coverage without reading the canonical doc in full.** The percentage drives the go/no-go decision (`<20%`: don't use this pattern; `>90%`: don't use this pattern). Skipping the read leads to using the bridge pattern when it's overkill, or skipping it when it's needed.

## Acceptance criteria

1. After PR1 + PR2 both merge, the canonical doc tells a complete story: any reader who never sees the deleted files learns nothing important from their absence.
2. The bridge file's appendices, considered alone, are sufficient to reconstruct any deleted auxiliary file's load-bearing rows (not the full file — just the rows that mattered).
3. The canonical doc's version-history row for PR2 explicitly cites PR1 and the bridge file.
4. Stale references to the deleted files in the canonical doc are all updated. (Run `grep -n "<deleted-filename>" <canonical-doc>` after PR2; every remaining match should be either historical context ("originally in the now-deleted X") or a version-history-row entry.)
5. The bridge file's in-flight-tracking-table row is the explicit handle for its eventual deletion; the user never has to guess whether it's still needed.

## Files this skill creates / modifies

- **Creates:** `<canonical-doc-basename>-sync.md` (the bridge file, at the same directory level as the canonical doc).
- **Modifies (in PR2):** the canonical doc itself — version bump, new sections, refreshed file references, an in-flight-tracking-table row for the bridge's eventual deletion.
- **Deletes (in PR1):** every file in the auxiliary input list.
