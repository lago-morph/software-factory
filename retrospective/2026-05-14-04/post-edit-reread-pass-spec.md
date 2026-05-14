# Spec: `post-edit-reread-pass`

## Intent

After any non-trivial edit to a long document — particularly one that touches multiple sections — do at least one full top-to-bottom re-read looking for cross-section drift. Continue iterating until a full pass surfaces no major or factual errors. The dominant failure mode for multi-section doc edits is *cross-section inconsistency* (a count updated in section A but not section B; a status changed in §3 but a stale reference left in §10); these are invisible from within a single edit but jump out in a full re-read. In the session this skill derives from, three iteration passes on `research/PLAN.md` each caught new self-introduced bugs (8+ total across the three passes). One iteration would have shipped a document with bugs the user would have caught in review.

## Trigger

**Activate when:**

- Just made multi-section edits to a doc >200 lines.
- Just performed a version bump on a long-lived status doc (PLAN.md, ROADMAP.md, etc.) that touched 5+ sections.
- The user explicitly says "iterate," "double-check," "verify," "review yourself," or similar.
- About to commit a doc-revision PR.

**Negative triggers** (skip the skill):

- Single-section edit (one heading touched, no cross-references).
- The doc is short enough that the edit was already a full read (<100 lines).
- The user has explicitly time-boxed the work and the time is up.

## Inputs

- The doc just edited.
- The list of sections / claims that were changed in the most recent edit pass.
- The git diff of the edit pass (to remind yourself what *should* now be consistent).

## Outputs

- A clean doc with no cross-section drift detected in the final re-read.
- Optionally: a summary in the commit message of what each iteration pass caught (useful for reviewer confidence).

## Workflow

1. **Run the edit pass** that triggered the skill.

2. **Re-read the doc top to bottom**, not just the changed sections. Read for:
   - Counts / totals / cumulative claims that should now be consistent across sections.
   - Status markers (✅ / 🟡 / ❌ / RESOLVED / PENDING) that should agree across §1 TL;DR and the detailed sections.
   - References to "N <items>" / "M <Y>" that may have aged when the underlying inventory changed.
   - Cross-section "see §N" references that may now point to wrong sections or wrong content.
   - Phrases like "still pending," "in-flight," "outstanding," "queued" that may now be stale.
   - Dates and version numbers in the version history.

3. **Run targeted greps** for terms that should now be consistent. Examples:
   - `grep -nE "(four|3|three) <thing>"` to spot stale numeric framing.
   - `grep -nE "still.*pending|in.flight|outstanding"` to spot status drift.
   - `grep -nE "issue #[0-9]+" file.md` to verify all referenced issues are accurately classified (open/closed/drained).
   - `grep -nE "v0\.[0-9]" file.md` to spot stale version refs.

4. **Categorize each finding:**
   - **Major** — would mislead a reviewer (wrong count, wrong status, contradiction with another section).
   - **Minor** — cosmetic but still worth fixing (stale parenthetical, slight numeric imprecision).
   - **Non-issue** — re-read confirmed correctness.

5. **Fix the findings.** Apply edits. Note in the commit message body (one line per pass): "Iteration 2 caught: count drift in §3.4 row; stale 'still pending' in §5 task 4."

6. **Re-read again.** Continue until a full pass surfaces zero major findings and at most a handful of minor ones (or none).

7. **Stopping condition.** Stop when:
   - The last full re-read found zero major findings, OR
   - The user has indicated they want to ship and minor findings can wait, OR
   - You're on iteration ≥4 and the findings have plateaued at minor cosmetic items (diminishing returns).

8. **Commit.** The diff that ships is the cumulative result of all iteration passes. The commit message body may briefly enumerate what each pass caught, as a reviewer-confidence signal.

## Concrete examples

### Example 1 — count drift caught on iteration 2

After iteration 1 of PLAN.md v0.10, the §3.4 table had been expanded to five retrospectives. The §1 TL;DR still said "four retrospectives that landed 2026-05-13/14." Iteration 2's full re-read caught the mismatch at line 6 (the "Earlier versions" paragraph). Fix: change "four" to "five" in the TL;DR; also update line 22-23's "Open items" bullet that said "(now four retrospectives cumulative)."

### Example 2 — status drift caught on iteration 3

After iteration 2, §4.3 item 4 said "round-8 Cloudflare-blocked; Wayback fallback may work" and item 5 said "low priority follow-up." But §4.3's section header said "Path-B-only background completeness." Items 4 and 5 are NOT strictly Path-B-only; item 4 is Wayback-eligible and item 5 has never been action-tried. Iteration 3 caught this by re-reading the section header against its items. Fix: rephrase the §4.3 intro to distinguish strict-Path-B (items 1a, 3) from retry-eligible (items 4, 5), and update §1 and §9 to match the new framing.

### Example 3 — non-issue confirmed

After iteration 1, line 22 said "§3 Bottlenecks — three live items: §3.2 ..., §3.4 ..., §3.5 ..." The re-read could have flagged "three" as a candidate count to verify. Verification: §3.1 RESOLVED, §3.2 OPEN, §3.3 RESOLVED, §3.4 OPEN, §3.5 OPEN. That's three open. Confirmed. No fix needed.

## Anti-patterns

- **Re-reading only the changed sections.** The cross-section drift you're hunting for is, by definition, in sections you didn't touch in the last edit pass. Read the whole thing.
- **Trusting the diff to show all the work.** The diff shows what changed; it does NOT show what should have changed but didn't. A full re-read does.
- **One pass and done.** If iteration 1 found bugs, iteration 2 will probably find different ones (the fixes from iteration 1 themselves may introduce drift). Plan on N ≥ 2.
- **Going past diminishing returns.** Once you're catching only cosmetic minor items on each pass, you've found the floor. Stop and ship.
- **Not noting what each pass caught.** The commit message that records "iteration 2 caught X; iteration 3 caught Y" tells the reviewer you actually iterated. Without it the reader has no signal.
- **Skipping the targeted greps.** Manual re-reading is good but slow. `grep -nE "(four|3|three) retrospective"` runs in 50ms and catches systematically.

## Acceptance criteria

1. At least one full top-to-bottom re-read happened after the last edit.
2. The last re-read surfaced zero major findings (count drift, status contradictions, factual errors).
3. Targeted greps for the doc's load-bearing terms (counts, status markers, version refs, issue numbers) return only correct hits.
4. The commit message body records what each non-trivial iteration pass caught.
5. The total number of iterations is at least 1 and is bounded by "the most recent pass found nothing major," not by a fixed N.

## Files this skill creates / modifies

- The doc being edited.
- Optionally: a brief commit-message body section enumerating iteration findings.
