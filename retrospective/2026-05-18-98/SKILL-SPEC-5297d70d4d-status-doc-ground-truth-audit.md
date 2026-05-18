# Spec: `status-doc-ground-truth-audit`

- **ID**: SKILL-SPEC-5297d70d4d
- **Source retrospective**: ../2026-05-18-98.md

## Intent

Audit a long-lived status document (PLAN.md, ROADMAP.md, INDEX.md, RFC, design doc) by querying ground truth — filesystem counts, catalog record counts, retrospective directory counts, git history — *before* reading any of the doc's narrative claims. The dominant failure mode for these docs is that prose claims drift while underlying counts move: "26 numbered reports" lingers in §1 long after Round-10 added reports 27–37; "8 installed skills" lingers in §2 long after the .claude/skills/ directory grew to 15. Content-first reading internalizes the wrong numbers before any verification happens. This skill inverts the order: count first, read second, fix third.

## Trigger

Direct triggers:
- User says "audit PLAN.md" / "audit the roadmap" / "is this doc still correct?" / "what's stale in X.md?"
- User asks to "iterate until correct" on a long-lived status doc.
- The target doc has a `**Version:**` line, a §2-style "Repository layout" section, or numeric claims in its TL;DR ("N reports", "M retrospectives", "K records").

Proactive triggers:
- About to bump the Version line on a status doc.
- About to add a Session bullet that references counts (reports, retros, sources) the doc tabulates elsewhere.
- The `research-pipeline` skill's `_plan/audit.md` is being followed and the lint or `check-plan-consistency.py` flags warnings.

Negative triggers:
- Single-section edits (use direct Edit + `post-edit-reread-pass`).
- Docs without numeric or structural claims (pure narrative).
- Code files (this skill is for human-readable docs).

## Inputs

- Path to the doc being audited (default `research/PLAN.md` in this repo).
- Optional: a JSON list of ground-truth queries with expected keys (filesystem + git + catalog). If absent, the skill uses the built-in default set below.

## Outputs

- A printed findings table grouped by drift shape (count drift / status drift / cross-section ref drift / version-bump bookkeeping drift / stale path drift).
- Fixes applied directly to the doc via Edit calls.
- A commit on the current branch + push + PR (ready-for-review per project convention).

## Workflow

1. **Verify the doc exists** and read its first ~100 lines to identify section structure (`grep -n "^## " <doc>`).
2. **Run a ground-truth queries batch** in a single Bash call. The default for the software-factory repo:
   ```bash
   echo "Numbered reports:  $(ls research/ 2>/dev/null | grep -E '^[0-9][0-9]-' | wc -l)"
   echo "Followup reports:  $(ls research/followup/ 2>/dev/null | grep -E '^[0-9][0-9]-' | wc -l)"
   echo "Skills installed:  $(ls -d .claude/skills/*/ 2>/dev/null | wc -l)"
   echo "Retrospectives:    $(ls -d retrospective/*/ 2>/dev/null | wc -l)"
   echo "Catalog records:   $(jq 'length' reference-only/sources.json 2>/dev/null)"
   ```
   Save the output as the **ground-truth snapshot** for the rest of the audit.
3. **Grep the doc for each ground-truth quantity** to find every place it appears, looking for both the right and a plausible-wrong value:
   ```bash
   for n in 26 12 8 5 209 37 22 15; do
     grep -nE "[^0-9]$n (numbered|followup|installed|retrospectives|records)" research/PLAN.md
   done
   ```
   Any occurrence that doesn't match ground truth is **count drift** — flag with line number.
4. **Run the doc-specific consistency script** if one exists:
   ```bash
   python .claude/skills/research-pipeline/scripts/check-plan-consistency.py --window 50
   ```
   Surface warnings as advisory; the script doesn't know about content drift, only commit-touch drift.
5. **Read the doc top to bottom** (chunked if >25k tokens — use `Read` with offset/limit) looking for the other drift shapes from `post-edit-reread-pass`: stale paths (named paths that no longer exist on disk), stale status markers (✅/🟡/❌ that don't match current report state), cross-section `see §N` references whose target moved, "still pending" qualifiers whose underlying state changed, out-of-scope statements newer commits may have reversed.
6. **Categorize findings** by major (would mislead a reviewer) vs minor-with-factual-error vs cosmetic. Only fix the first two categories.
7. **Apply fixes via Edit** — one fix per Edit call, preferring smaller targeted edits over big rewrites. Bump the Version line + extend the Earlier-versions paragraph + update the file footer in the same edit batch.
8. **Iterate** per `post-edit-reread-pass`: re-run the ground-truth queries, re-grep for the load-bearing quantities, look for new drift the iteration-N fixes introduced. Stop when a full pass surfaces zero major or factually-wrong-minor findings (typically 3–6 iterations on a 500-line doc).
9. **Run lint** before committing:
   ```bash
   bash .claude/skills/research-pipeline/scripts/lint-sources.sh
   ```
   Fix any errors; advisory warnings (especially the plan-consistency ones) are OK to push through.
10. **Commit + push + open PR** ready-for-review (per `AGENTS.md` convention in this repo).

## Concrete examples

### Example 1: report-count drift in PLAN.md §1

Ground-truth query: `ls research/ | grep -E "^[0-9][0-9]-" | wc -l` → **38** (counting 00-synthesis + reports 01–37).

Doc claim (line 4): "**26 numbered reports** + 12 follow-up reports".

Fix: replace "26 numbered reports" with "37 numbered reports" (excluding 00-synthesis per the doc's convention — verify by reading how the count was historically scoped).

Cross-section sweep: same quantity also appears in §2 layout ("/research/ → 26 numbered reports + 12 followup reports"). Updated to "37" there too. After fix: `grep -n "26 numbered" research/PLAN.md` returns zero hits.

### Example 2: stale §2 repository-layout paths

Ground-truth query: `ls reference-only/el-kaim-book/ 2>/dev/null` → **"No such file or directory"**.

Doc claim (§2 line 74): "el-kaim-book/ → 8 chapters of El Kaim's EA book (Ch 1–7 ~430 KB + Ch 9 manual drop)".

Investigation: `git log --diff-filter=R --name-status reference-only/el-kaim-book/` shows PR #80 migrated the named subdirectory to per-id directories. Query the new locations: `jq -r 'to_entries[] | select(.value.title | test("El Kaim Book")) | "\(.key)  \(.value.title)"' reference-only/sources.json` → 11 records matched, one per chapter + author/index pages.

Fix: rewrite the §2 reference-only block to describe the per-id-directory layout, with example records (`8c295c7e*`, `c94a94f2*`, etc.) and the catalog files (`sources.json`, `sources.md`, `sources.schema.json`) as siblings.

## Anti-patterns

- **Reading the doc first and trusting its numbers.** Dominant failure mode — internalize the wrong number before verification. Always run ground-truth queries before reading the prose.
- **Fixing one section without grepping for the same quantity elsewhere.** A count appears in §1 status, §2 layout, §10 lookup table, §17 history — fix one and the others diverge. Iteration 3 of PR #98 caught five "~7 URLs" residues across §4.1/§4.3/§5/§9/§14 that iteration 2's §1 fix introduced.
- **Stopping after iteration 1.** Fixes from iteration 1 introduce new drift the iteration-1 reader can't see; iteration 2 catches it. Plan for ≥2.
- **Treating archive/history sections as needing the same level of update.** A §17 v0.10 row saying "26 ADRs" is historical (records what v0.10 *did*) — leave it alone. Drift only matters for live sections.
- **Recounting tabular sub-sections opportunistically.** If §3.4 lists 5 retrospectives and 22 actually exist on disk, the right move is usually to flag the table as a stale snapshot and add a caveat — not to recount 17 retros' AGENTS suggestions / ADR proposals in the same audit. That's a separate, dedicated retro-coverage-audit pass.

## Acceptance criteria

- [ ] Ground-truth snapshot is captured (in chat or commit message) before any doc edits.
- [ ] Every numeric claim in §1 status line + §2 layout matches the ground-truth snapshot.
- [ ] No stale paths in the doc that no longer exist on disk.
- [ ] Version line bumped if any section changed substantively; Earlier-versions paragraph extended; file footer (if any) updated.
- [ ] Doc-specific consistency script (if any) exits 0 or reports only the expected advisory warnings.
- [ ] At least one full re-read pass after the last edit surfaces zero major findings.

## Files this skill creates / modifies

- `research/PLAN.md` (or other target status doc) — direct Edits.
- No new files. Commits go on the current branch.
