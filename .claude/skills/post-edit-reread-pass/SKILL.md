---
name: post-edit-reread-pass
description: After non-trivial multi-section edits to a long document, do at least one full top-to-bottom re-read looking for cross-section drift, and iterate until a full pass surfaces no major or factual errors. The dominant failure mode for multi-section doc edits is cross-section inconsistency — a count updated in section A but not section B; a status changed in §3 but a stale reference left in §10. These bugs are invisible from within a single edit but jump out in a full re-read. Triggers on phrases like "iterate", "double-check", "verify", "review yourself", "drift check", "is the doc internally consistent?"; and proactively after any version bump of a long-lived status doc (PLAN.md, ROADMAP.md, INDEX.md, RFC, design doc) that touched five or more sections. Skip for single-section edits or short docs (<100 lines).
---

# Post-edit re-read pass

After non-trivial multi-section edits to a long document, do at least one full
top-to-bottom re-read looking for cross-section drift, and **iterate until a
full pass surfaces no major or factual errors**.

The dominant failure mode for multi-section doc edits is *cross-section
inconsistency*: a count updated in section A but not section B; a status
changed in §3 but a stale reference left in §10; a totals row that no longer
agrees with the rows that feed it. These bugs are invisible from within a
single edit (the edit looks self-consistent) but jump out on a full re-read.

One iteration is not enough. The fixes from iteration N can themselves
introduce new drift, which iteration N+1 will catch. Plan on at least two
passes. The stopping rule is **quality-bounded, not clock-bounded**: stop
when the most recent full pass surfaces zero major findings.

---

## When to use this skill

**Activate when:**

- You've just made multi-section edits to a doc >200 lines.
- You've just done a version bump on a long-lived status doc (PLAN.md,
  ROADMAP.md, INDEX.md, RFC, design doc, runbook) touching 5+ sections.
- The user says "iterate", "double-check", "verify", "review yourself",
  "drift check", "is it internally consistent?", "make sure it's accurate".
- You're about to commit a doc-revision PR that you wrote in this session.
- You just applied `verify-counts-before-doc-claim` to several sections of
  a long doc — re-read confirms the resulting counts are consistent
  across the whole.

**Do not activate for:**

- Single-section edits with no cross-references.
- Short docs (<100 lines) where the edit already was a full read.
- Time-boxed work where the user has signaled "ship it."
- Code files. This skill is for human-readable docs where cross-section
  consistency is a meaningful invariant. Code has its own QA loop.

---

## What "drift" looks like

Drift falls into a small number of recurring shapes. Recognizing the
shape makes re-reading systematic rather than ad hoc.

### Shape 1: count drift

A numeric claim appears in multiple places (TL;DR, body section, summary
table, version-history entry). One edit updates some occurrences, leaves
others stale.

Example: a status line says "12 outstanding items" while the table below
lists 14 rows. One was authoritative for the writer; the other is now
wrong.

### Shape 2: status / state drift

A binary or enumerated state (✅ / 🟡 / ❌, open / closed / done,
RESOLVED / PENDING) is updated in the detailed section but not in the
top-of-doc snapshot — or vice versa.

Example: §3 detailed bottlenecks list says "RESOLVED" but the §1
"Open items live in" list still references §3 as an open bottleneck.

### Shape 3: cross-section reference drift

A "see §N" pointer is correct at the time it's written but goes stale
when a section is renumbered, moved, or deleted.

Example: §5 says "see §3.3 task 2" but §3.3 has been removed and the
content moved to §4.1.

### Shape 4: stale qualifier drift

Phrases like "still pending", "in-flight", "to be drained", "next batch",
"TODO" age in place. The underlying state has changed but the qualifier
hasn't been edited.

Example: §4 says "pending the next fetch issue" but that issue was
opened, drained, and closed three sessions ago.

### Shape 5: contradicted-by-newer-artifact drift

The doc says X is out-of-scope or X won't be done; a newer artifact
(another doc, a merged PR, a recorded ADR) has reversed that. Both
statements coexist without acknowledgement.

Example: a project plan's "Out of scope" section says "we will not
consolidate the four candidates" but a recently-merged proposal doc
explicitly proposes consolidating them.

### Shape 6: version-bump bookkeeping drift

Version number / date in the top-of-doc header is bumped; the version
history table at the bottom isn't updated. Or the other way around.

### Shape 7: aged-inventory drift

A list of files / directories / sources was current when written but new
items have landed without being added. "8 chapters" should now be "9".
"Three retrospectives" should now be "five".

---

## Workflow

1. **Run the edit pass** that triggered the skill. (Usually applying the
   change plan from a drift assessment, or executing the user's revision
   request.)

2. **Re-read the doc top to bottom**, not just the changed sections. The
   cross-section drift you're hunting for is, by definition, in sections
   you didn't touch in the last edit pass.

3. **Run targeted greps** for terms that should now be consistent. The
   helper script `scripts/check-doc-consistency.sh <path-to-doc>` runs a
   battery of common patterns; results are advisory (it flags candidates
   that *might* be drift, not all of which actually are).

4. **Categorize each finding:**
   - **Major** — would mislead a reviewer (wrong count, wrong status,
     contradiction between sections, factual error).
   - **Minor** — cosmetic but worth fixing (stale parenthetical, slight
     imprecision, prose tightening).
   - **Non-issue** — re-read confirmed the section is correct.

5. **Fix the findings.** Apply edits. In the commit message body, note
   one line per pass describing what was caught:

   ```
   Iteration 2 caught: count drift in §3 table; stale "still pending"
   in §5 task 4; missing version-history entry.
   Iteration 3 caught: cross-section ref §5→§3.3 was stale after §3.3
   was renumbered.
   ```

6. **Re-read again.** Each pass starts fresh from the top of the doc.

7. **Stopping condition.** Stop when **any** of:
   - The most recent full pass surfaced zero major findings (the strong
     stop — this is the target).
   - You're on iteration ≥4 and the findings have plateaued at minor
     cosmetic items (diminishing returns; ship what you have).
   - The user has explicitly said to ship.

8. **Commit.** The diff that ships is the cumulative result of all
   iteration passes; the commit message body enumerates what each
   non-trivial iteration caught.

---

## Targeted-grep cheat sheet

Generic patterns that catch drift across most doc types. Adapt to the
doc's specific vocabulary.

```bash
# Numeric framing — likely candidate counts to verify
grep -nE "\b(one|two|three|four|five|six|seven|eight|nine|ten)\b" doc.md

# Open/closed/pending qualifiers — likely status drift
grep -nE "\b(pending|outstanding|in.flight|to be|still|TBD|TODO)\b" doc.md

# Cross-section references — likely renumber/move drift
grep -nE "(see |§|section )[A-Z0-9]+(\.[A-Z0-9]+)*" doc.md

# Version refs — likely version-bump bookkeeping drift
grep -nE "v[0-9]+(\.[0-9]+)+" doc.md

# Date refs — likely aged-inventory drift
grep -nE "[0-9]{4}-[0-9]{2}-[0-9]{2}" doc.md

# Issue / PR refs — likely closed-but-still-listed drift
grep -nE "#[0-9]+" doc.md

# Status markers
grep -nE "✅|🟡|❌|⏳|RESOLVED|PENDING|DONE|OPEN" doc.md
```

The helper script `scripts/check-doc-consistency.sh` bundles these into
one invocation with line numbers and rough categorization.

---

## Concrete examples

### Example 1 — count drift caught on iteration 2

Doc: a project status doc. Iteration 1 expanded a backlog table from 3
rows to 5 rows. Iteration 2's re-read found that the top-of-doc TL;DR
still said "three open items" — drift in shape 1 (count drift).

Fix: change "three" to "five" in the TL;DR. Also grep for "(three|3)
.*backlog" — found one more stale reference in a "see §N" pointer that
also needed updating.

Iteration 3's re-read confirmed no remaining count drift.

### Example 2 — status drift across §1 and §3

Doc: a plan with a §1 "Open items live in:" bullet list and §3 "Bottlenecks"
detailed section. Iteration 1 marked §3.3 as RESOLVED in the section
heading. Iteration 2's re-read found that §1's bullet still listed §3.3
as an open bottleneck — drift in shape 2.

Fix: update the §1 bullet to remove §3.3 from the open list. Also
checked §5 "Work remaining" — it had a task referencing §3.3 work that
was now done; updated to strike-through with a "done" note.

### Example 3 — cross-section reference drift

Doc: a design doc. Iteration 1 reorganized the methodology section,
collapsing former §4.2 and §4.3 into a single §4.2. Iteration 2's grep
for `§4.3` returned a "see §4.3 for the rationale" line in §6 — drift in
shape 3.

Fix: rewrote the pointer as "see §4.2 (formerly §4.2/§4.3)".

### Example 4 — version-bump bookkeeping drift

Doc: a long-lived status doc with a top-line "Version: v1.4 (2026-MM-DD)"
header and a `## Version history` table at the bottom. Iteration 1
bumped the top-line to v1.5. Iteration 2's re-read found the version
history table still ended at v1.4 — drift in shape 6.

Fix: add a v1.5 row to the version history table with a one-line
summary of what changed.

### Example 5 — stopping at minor cosmetic floor

Doc: a runbook. Iteration 1 made substantive edits; iteration 2 caught
two major findings (a stale env-var reference and a contradicted "do not"
rule). Iteration 3 caught only one minor finding (a paragraph that
read awkwardly). Iteration 4 found nothing major and only suggested
prose tightening.

Stop after iteration 4. Commit. The commit body enumerates iterations
1–4 findings; the minor prose-tightening notes can be left for a future
pass or someone else's review.

---

## Anti-patterns

- **Re-reading only the changed sections.** The cross-section drift
  you're hunting for is, by definition, in sections you didn't touch.
  Read the whole thing.

- **Trusting the diff to show all the work.** The diff shows what changed;
  it does NOT show what should have changed but didn't. A full re-read
  surfaces the omissions.

- **One pass and done.** If iteration 1 found bugs, iteration 2 will
  probably find different bugs (the fixes from iteration 1 introduce new
  drift). Plan on N ≥ 2.

- **Going past diminishing returns.** Once you're catching only cosmetic
  minor items per pass, you've found the floor. Stop and ship.

- **Not noting what each pass caught.** A commit message recording
  "iteration 2 caught X; iteration 3 caught Y" tells the reviewer you
  actually iterated. Without it the reader has no signal — and future-you
  has no record of the drift surface.

- **Skipping targeted greps.** Manual re-reading catches drift, but
  slowly. A targeted grep for the doc's load-bearing terms runs in
  milliseconds and catches systematically. Use both.

- **Confusing this skill with QA review.** This skill is *self-review by
  the author* immediately after edits. It does not replace peer review,
  CI, or staged testing. It catches the bugs that would otherwise reach
  reviewers and waste their time.

- **Iterating without a stopping rule.** "Iterate until the user says
  stop" is not a stopping rule. "Stop when the last pass found nothing
  major" is.

---

## Acceptance criteria

1. At least one full top-to-bottom re-read happened after the last edit.
2. The most recent re-read surfaced zero major findings (no count drift,
   no status contradictions, no factual errors, no broken cross-references).
3. Targeted greps for the doc's load-bearing terms (counts, status
   markers, version refs, issue / PR numbers, section refs) return only
   correct hits.
4. The commit message body records what each non-trivial iteration pass
   caught — one line per pass is sufficient.
5. The total number of iterations is at least 1 and is bounded by "the
   most recent pass was clean," not by a fixed N.

---

## Files this skill creates / modifies

- The doc being edited (whatever long-lived doc triggered the skill).
- A brief commit-message body section enumerating iteration findings.

No artifacts on disk besides the doc itself. The discipline is the
output.

---

## Helper script

`scripts/check-doc-consistency.sh <path-to-doc>` runs the targeted-grep
cheat sheet against a single doc and reports candidates. Findings are
advisory — review each in context. The script never modifies the doc.

---

## See also

- `verify-counts-before-doc-claim` — pre-edit discipline that prevents
  count drift at write-time. Pairs naturally: that skill prevents the
  bugs; this skill catches whatever slipped through.
- `drift-assessment-before-revision` — produces the change plan that
  this skill then iterates against.
