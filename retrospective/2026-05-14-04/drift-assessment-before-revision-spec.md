# Spec: `drift-assessment-before-revision`

## Intent

When the user asks to update a long-lived doc, separate **assessment** from **revision** by default: produce a written drift report first, then wait for sign-off or implicit acceptance before editing. This skill encodes the workflow the user explicitly used in this session ("Don't change it yet, just assess"), which proved load-bearing: the written drift assessment became the change plan for the subsequent edit pass and prevented a wholesale rewrite that would have lost archival context. The same workflow is valuable even when not asked for — the assessment makes the change plan visible to the user and to your own iteration pass.

## Trigger

**Activate when:**

- User asks "is X up to date?", "has X drifted?", "what needs updating in X?", or similar without yet authorizing an edit.
- User asks for a doc revision >100 lines or covering 5+ sections.
- Before applying the result of `verify-counts-before-doc-claim` to a long doc — produce an assessment first so the user can see the scope.
- You're about to do a "version bump" on a long-lived status doc (PLAN.md, ROADMAP.md, INDEX.md).

**Negative triggers** (skip):

- Single-section edit with no cross-references.
- Doc is short enough that the assessment IS the edit (e.g., <50 lines).
- User has explicitly said "just do it" or has indicated time pressure.

## Inputs

- The doc being assessed.
- The known recent activity that may have caused drift: commit history since last update, PR list, related file changes, related GitHub issues.
- The doc's own internal markers of last-update (version number, date, "as of YYYY-MM-DD" lines).

## Outputs

- A structured drift report, either inline in chat or written to a scratch file (depending on size). Categorized by:
  - **Major drift** — would mislead a reviewer; factually wrong claims; contradictions with newer authoritative artifacts.
  - **Minor drift** — stale parentheticals, slight numeric imprecisions, missing additions.
  - **Not drifted** — sections that re-read confirmed are still accurate.

- A recommended revision shape (incremental patches vs wholesale rewrite vs version bump).

- A pause for user sign-off (explicit or implicit by "go").

## Workflow

1. **Read the doc top to bottom.** Note version, date, last-update markers, and the doc's claimed structure.

2. **Gather drift sources** in parallel:
   - `git log --oneline <last-update-commit>..HEAD` for commits since the doc was last touched.
   - `git log --oneline -- <doc-path>` for the doc's own update history (the most recent commit hash is the assessment baseline).
   - For each PR merged since the baseline, read its body for what it added/changed (`mcp__github__pull_request_read` if available, or the merge commit body).
   - For status docs that reference issues, list open issues (`mcp__github__list_issues` state=OPEN).
   - For status docs that reference files / inventory counts, sample a few via `ls`, `wc -l`, `grep`.

3. **Walk the doc section by section** and classify each section:
   - **Major drift** — list the specific stale claim and the authoritative correction.
   - **Minor drift** — list the specific small fix.
   - **Not drifted** — note briefly that the section is still accurate (so the user knows the assessment was complete).

4. **Surface contradictions with newer artifacts.** If a recently merged PR contradicts an "out of scope" or "we won't do X" line in the doc, flag it explicitly — this is the highest-blast-radius drift class.

5. **Identify orphan-section risk.** If the doc has archival sections (§§11–17 or similar), do NOT propose touching them unless the drift is in *their* content. Wholesale rewrites lose archival context.

6. **Write the report.** Suggested structure:

   ```markdown
   ## Assessment: <doc> drift

   The file is v0.X, dated YYYY-MM-DD. N commits/PRs have landed since.
   Significant drift in K places; minor in M more.

   ### Major drift

   1. **§N.M ...** — <specific stale claim> is wrong; should be <correction>.
   2. ...

   ### Minor drift

   N. **§N.M ...** — <specific small fix>.
   ...

   ### Not drifted (still accurate)

   - §X.Y, §X.Z — re-read confirmed.

   ### Suggested shape for the v0.Y pass

   Rather than incremental patches, this looks like a v0.Y cut similar in
   spirit to v0.<prior>: rewrite §A + §B + §C against current state,
   archive §D round-N detail into §§<archive area>, add new §E section
   for newly-discovered content. Version-history v0.Y entry to close it
   out.
   ```

7. **Pause for sign-off.** Do NOT proceed to edit until:
   - User explicitly says "go," "proceed," "update it," or equivalent.
   - User implicitly accepts by adding scope or refining the assessment.

8. **When proceeding to edit,** treat the drift report as the change plan. Cross off items as they're applied. Apply `verify-counts-before-doc-claim` for every numeric claim. Apply `post-edit-reread-pass` after the edit completes.

## Concrete examples

### Example 1 — PLAN.md v0.9 → v0.10 assessment

User: "Now look at the plan file. Has it drifted? What updates need to be made? Don't change it yet, just assess."

Walked the doc:
- §1 status — found three claims that were stale (issue count, retrospective count, "five retrospective decisions queued").
- §2 layout — missing `camel-paper/` and `lenny-podcast-transcripts/`.
- §3.3 — body was already round-8-aware (added in PR #44) but the "Follow-up fetch queue" line was incomplete.
- §3.4 — referenced only `retrospective/2026-05-11-01/`; missed four other retrospectives.
- §4.3 — listed Replit and Codex as "Cloudflare-gated" but round-8 had drained both.
- §5 task 2 — still listed #29/#30/#31 as pending drain (long done).
- §9 out-of-scope — said "comparison stays a comparison" but `research-plan.md` (PR #46) explicitly proposed the opposite.
- §14 — three stale "pending issue X drain" cells.
- §17 — version history stops at v0.9.

Categorized: 6 major + 4 minor. Recommended a v0.10 cut similar to v0.8/v0.9 — rewrite §1 + §3 + §5 against current state, add round-7/round-8 record entries, refresh §4.3, decide if §9 is reversed or kept-with-pointer, close out with v0.10 entry in §17.

User accepted with "Cleanup and then update plan. Iterate at least once."

### Example 2 — when to skip the skill

User: "Add a note to PLAN.md §3.4 that retrospective 2026-05-14-04 has been authored."

This is single-section, no cross-references beyond the one row addition, and the user has explicitly time-boxed it. Skip the drift assessment, just make the edit. The skill is for revisions, not appendings.

## Anti-patterns

- **Proceeding to edit without writing the assessment.** If the user said "Don't change it yet," you must produce a written assessment before editing — even if you "know" what's wrong. The written assessment is the artifact; verbal "I'll just fix it" loses the visibility.
- **Wholesale rewrite when the doc has archival sections.** Long-lived status docs accrete archival material that has audit-trail value. Re-write §§1–6 (the live work); preserve §§7+ (the archive).
- **Skipping the "Not drifted" list.** Without it, the user can't tell if you actually re-read the whole doc or just spot-checked.
- **Conflating drift with new content.** Drift = stale claims that contradict current state. New content = additions that the doc should now include. Both belong in the assessment but should be labeled separately.
- **Asking for sign-off on every minor finding.** The pause-for-sign-off is at the major-revision level. Minor cosmetic fixes can be batched into the major-revision edit pass.
- **Producing the assessment but then "discovering" new drift mid-edit.** If new drift surfaces during the edit, add it to the assessment first (or extend the iteration log in the commit body), then fix it — don't silently grow the diff.

## Acceptance criteria

1. The drift assessment exists as a written artifact (in chat or scratch file) before any edits to the doc begin.
2. The assessment categorizes findings as major / minor / not-drifted.
3. The assessment names the authoritative source for each stale claim (a newer PR, a current file, a fresh tool output).
4. The user has explicitly accepted (or refined) the assessment before edits begin.
5. The subsequent edit pass crosses items off the assessment; new findings encountered mid-edit are appended to the assessment, not silently absorbed.

## Files this skill creates / modifies

- The doc being assessed (read-only during the assessment phase).
- The chat / a scratch file holding the assessment.
- After sign-off: the doc itself (during the revision phase).
