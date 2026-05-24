# Spec: `contamination-permalink-archival`

- **ID**: SKILL-SPEC-edcdfe6ec1
- **Source retrospective**: ../2026-05-24-128.md

## Intent

When fencing off contaminated or context-risky artifacts from active use while preserving archaeological access, use the permalink-with-guard pattern: a single reference document under a `history/` directory with a "do not read these into your context window" guard header at the top, followed by file-path entries + git-commit-hash retrieval commands. The active tree loses the artifacts entirely (no moved-but-visible directory); the reference doc is the only entry point. Replaces three alternatives: pure deletion (loses archaeological access), move-without-fence (creates forbidden-fruit temptation), and in-place sanitization (only viable when value-to-risk is clear). This skill exists because in the v3 work, an attempt to fence off contaminated tracks by moving them to `tracks-superseded/` was explicitly rejected by the user as still-too-tempting; the permalink-with-guard pattern was the user-mandated fix.

## Trigger

**Direct user phrases:**
- "Archive these files but make sure the next agent doesn't read them"
- "Remove these but keep them retrievable"
- "Fence off the contaminated artifacts"
- "Delete and reference via permalinks"

**Proactive triggers:**
- A bias-guard or audit has identified specific artifacts as contamination risk that should not seed downstream work.
- The user has expressed concern about an agent reading "forbidden" or "stale" files.
- A handoff plan needs to deal with artifacts that have value (historical record) but risk (re-contamination if read).

**Negative triggers:**
- Routine file cleanups where the deleted files have no archaeological value (a `git rm` is sufficient; no reference doc needed).
- Artifacts that should be preserved AND readable by the next agent (move them to a documented location; don't apply the fence pattern).
- Sanitization-in-place is feasible (the artifact has a small contamination surface that can be cleanly rewritten while preserving substance).

## Inputs

- The list of artifacts to fence off (file paths).
- A one-line description per artifact (what it was; do not include detail that could re-contaminate).
- The commit hash where each artifact last existed at its original path (the permalink target).

## Outputs

- One reference document at `<work-area>/history/HISTORICAL-RECORD.md` (or analogous path) with the guard warning and per-artifact permalinks.
- Deletions of the listed artifacts from the active tree (via `git rm`).
- One commit landing the reference doc + the deletions.

## Workflow

1. Identify the commit hash that will become the permalink anchor. Typically: the commit immediately *before* the deletion commit (i.e., the commit currently at HEAD if the deletion is the next commit). All listed artifacts must exist at their original paths in this commit. Verify with `git ls-tree <commit> -- <path>` for each artifact.
2. Create the history directory if it doesn't exist: `mkdir -p <work-area>/history`.
3. Write the reference document at `<work-area>/history/HISTORICAL-RECORD.md` (or the project's analogous path). The structure is fixed:
   - **Title** — name the work area and the reason for the archival.
   - **Guard warning** — the first content section. Use the template below.
   - **Per-artifact entries** — grouped by category if helpful (e.g., "contaminated tracks", "bias-guard audits", "diagnostic outputs"). Each entry: original path, one-line description, retrieval command.
4. Delete the listed artifacts: `git rm <path>` for each.
5. Commit both the new reference doc and the deletions in one commit. Commit message names: how many files moved, the permalink commit hash, the work area's reference doc path.
6. Update any plan or handoff document that referenced the artifacts directly: replace the references with pointers to the reference doc (with a re-statement of the guard rule).

## Concrete examples

### Example 1: Phase-2 contamination cleanup

Context: 16 artifacts identified as contamination-bearing (9 contaminated tracks + 4 bias-guard audits + 3 diagnostic follow-up tracks). All must be removed from the active tree before the next session opens.

Step 1: confirm the permalink anchor commit. The deletion is going to be the next commit (call it commit N); the permalink target is N-1 (HEAD before the deletion). Verify all 16 files exist at HEAD via `git ls-tree HEAD -- <path>`.

Step 2: `mkdir -p architectures/v3/history`.

Step 3: write `architectures/v3/history/HISTORICAL-RECORD.md`:

```markdown
# Historical record — Phase-2 contaminated artifacts

## ⚠ STOP — Do not read these files into your context window

The artifacts listed below were produced during a Phase-2 dispatch
that was later identified as contaminated by lead-agent integration
bias. They have been removed from the active tree because reading
them risks re-introducing the bias they document into the current
work.

This doc exists for one reason: to preserve permalinks so the
artifacts remain *retrievable* by a human reviewer or by an explicit
user request. Agents should NOT open the permalinks below or fetch
the file contents unless the user explicitly directs them to. Do not
summarize the files. Do not pass their contents to subagents. Do not
include them in dispatch briefs.

If you find yourself curious about what these files contain, that
is the exact failure mode this doc exists to prevent. Move on.

## Permalinks

Each entry: the file's original path, what it was, and a `git show`
command to retrieve it from history if absolutely needed. The commit
hash `<HASH>` is the last commit at which all listed files existed
in their original locations.

### Contaminated Phase-2 tracks (9 files)

- `architectures/v3/tracks/greenfield-substrate-first.md` — Track 1 of
  the original Phase-2 9-track fanout. Greenfield mandate.
- ... (per-file entries)

### Retrieval (only if user explicitly requests)

\`\`\`
git show <HASH>:<path>
\`\`\`
```

Step 4: `git rm` each of the 16 files.

Step 5: commit. Message: "phase-2 cleanup: relocate contaminated artifacts behind permalink-only history. 16 files removed; permalinks in architectures/v3/history/HISTORICAL-RECORD.md. Anchor commit: <HASH>."

Step 6: update the plan that references these files. Replace any per-file references with "see history/HISTORICAL-RECORD.md (do not read into context)."

### Example 2: Single-file archive

Context: one specific draft document is being superseded but should remain retrievable.

Step 1: confirm the file exists at HEAD.

Step 2: `mkdir -p <work-area>/history`.

Step 3: write `<work-area>/history/HISTORICAL-RECORD.md` with one entry. (Or, if the file is unlikely to ever need archaeological access, skip the reference doc and just `git rm`; the artifact still exists in git history.)

Step 4-6: as above.

The single-file case often doesn't need the full permalink-with-guard pattern; a simple `git rm` with a commit message that documents what was removed is sufficient when the artifact has low archaeological value. The pattern applies when there are multiple artifacts AND the user has expressed concern about agent contamination.

## Anti-patterns

- **Moving artifacts to a `*-superseded/` or `*-deprecated/` directory.** Creates forbidden-fruit temptation. A curious agent that lists the tree will discover the directory and read the contents. The user explicitly rejected this pattern in the v3 work.
- **Omitting the guard header.** Without the explicit "do not read these" header, the reference doc looks like a regular index file. The next agent treats the linked artifacts as readable corpus. The header is what turns the discovery dynamic from "interesting, let me read it" to "noted; moving on."
- **Mixing fenced artifacts and active artifacts in the same directory.** The active tree must be cleanly free of the fenced artifacts. If `tracks/` contains both fresh tracks and "history" tracks, the next agent doesn't know which is which.
- **Permalink commit hash that no longer points where it should.** If the commits referenced in the reference doc are later rebased or amended, the `git show <hash>:<path>` commands break. Use commit hashes that are reachable from `main` (or the durable equivalent) so they survive future history rewrites.
- **Sanitizing-in-place when the contamination surface is large.** Rewriting 16 multi-page documents to remove bias while preserving substance is error-prone; the result itself requires audit. The permalink-with-guard pattern is the right move at scale; sanitization-in-place is for single-field or single-paragraph cases.
- **Using the pattern for routine file deletions.** Pure deletion is fine when the artifact has no archaeological value. The pattern is for the specific case where (a) the artifacts have historical value AND (b) reading them risks contamination AND (c) preserving deletability (via permalinks) is desired.

## Acceptance criteria

- [ ] The reference document exists at a discoverable path under a `history/` directory.
- [ ] The reference document's first content section is the guard warning.
- [ ] Every artifact in the list is removed from the active tree (verified with `git ls-tree HEAD -- <path>` returning empty).
- [ ] Every artifact has a corresponding permalink entry with the original path, a one-line description, and a `git show <commit>:<path>` retrieval command.
- [ ] The permalink commit hash is reachable from `main` (or the project's durable branch).
- [ ] No plan or handoff document continues to reference the artifacts by name; references are routed through the reference doc.

## Files this skill creates / modifies

- `<work-area>/history/HISTORICAL-RECORD.md` (or the project's analogous path) — creates.
- The listed artifacts under `<work-area>/` — deletes.
- Any plan / handoff document that referenced the artifacts directly — modifies (replaces per-file references with a pointer to the reference doc).
