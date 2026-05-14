# Spec: `verify-counts-before-doc-claim`

## Intent

Every numeric claim in a long-lived status document — "N retrospectives," "M proposed ADRs," "K outstanding URLs," "S followups" — must be tool-verified within the same edit. Self-recollection on counts is unreliable across long sessions, and counts are the highest-blast-radius drift surface in a status doc: a wrong count in one place propagates to every cross-reference. In the session this skill derives from (PLAN.md v0.10), five separate count drift bugs were caught across three iteration passes — every single one would have been prevented by a 1-second `ls | wc -l` or `grep -c` immediately before writing the count.

## Trigger

**Activate when:**

- About to write a phrase like "N <items>", "the project has M <X>", "we now have K <Y>" into a doc that will be merged to main.
- Updating a status-line / TL;DR / cumulative-backlog table in a long-lived doc.
- Replacing or extending a section that contains totals (especially in retrospective tables, version histories, file inventories).

**Negative triggers** (skip the skill):

- The count is a literal, just-computed result (e.g., "I just ran `ls` and saw 5 files" — that IS the verification).
- The count is in a transient artifact (chat reply, scratch notes).
- The count is from a clearly authoritative source already cited in the edit (e.g., "per `INDEX.md` row 22").

## Inputs

- The doc being edited.
- The specific claim being written (the literal phrase that contains the count).
- The git working tree (for `ls`, `grep`, `wc -l`, `find`).

## Outputs

- A verified count in the doc.
- A trace of the verification command in the commit message body (one line per verified count is sufficient).

## Workflow

1. **Identify the count** about to be written. Examples: "5 retrospectives", "26 proposed ADRs", "7 outstanding URLs", "24 numbered reports".

2. **Pick the verification command** by category:
   - **File counts** → `ls <pattern> | wc -l` or `find <dir> -name '<pattern>' | wc -l`.
   - **Markdown section / heading counts** → `grep -c "^## " <file>` or similar.
   - **Specific-section item counts** (e.g., "Part 4 — proposed ADRs") → `awk '/^## Part 4/{flag=1} /^## /{flag=0} flag' <file> | grep -cE "^- \*\*"`.
   - **Cross-doc inventory** → grep all relevant files and sum.
   - **Cumulative totals across multiple sources** → run the per-source verification for each source, then sum visibly.

3. **Run the command.** Record the actual numeric output.

4. **Write the count into the doc** using the verified number. If the verified count contradicts the claim you were about to write, write the verified one.

5. **Note the verification source** somewhere the reviewer can audit:
   - In the commit message body (recommended): "Verified `ls retrospective/ → 5 dirs`, `awk ... | grep -c → 26 ADRs`."
   - Or in the doc itself (parenthetical) if it's a load-bearing claim.

6. **When updating a cumulative total** (e.g., "13 unbuilt skills across 5 retrospectives"), verify *each component* and the sum. The bug pattern in PLAN.md v0.10 iteration was "I added a new row but didn't update the Totals row."

7. **Cross-reference check.** After writing the count, grep the rest of the doc for the same count to confirm consistency. `grep -nE "13 unbuilt|45 AGENTS|26 ADRs"` should return the table row plus any TL;DR mentions; all should agree.

## Concrete examples

### Example 1 — retrospective count

Editing PLAN.md §3.4 (the retrospective backlog table). Drafting:

> Four retrospectives now carry user-decision-pending artifacts.

**Verification:**
```bash
ls -d retrospective/2026-*/
# retrospective/2026-05-11-01/
# retrospective/2026-05-13-01/
# retrospective/2026-05-13-02/
# retrospective/2026-05-14-01/
# retrospective/2026-05-14-02/
```

Five, not four. Update the doc.

### Example 2 — per-retrospective ADR count

Drafting the §3.4 table row for `2026-05-13-02`. Need the proposed-ADR count.

**Verification:**
```bash
awk '/^## Part 4 — proposed ADRs/{flag=1; next} /^## /{flag=0} flag' \
  retrospective/2026-05-13-02.md \
  | grep -cE "^- \*\*"
# 5
```

Write "5" into the table cell.

### Example 3 — cumulative totals row

Drafting the "Totals" row of the §3.4 retrospective table. Components: per-retrospective skill specs are 3, 4, 3, 3, 0.

**Verification:**
```bash
echo $((3 + 4 + 3 + 3 + 0))
# 13
```

Write **13** as the Totals row value. Then `grep -n "13 unbuilt" research/PLAN.md` — should appear in §1 and §3.4 and §5 task 5 and §17 v0.10 entry. If any of those still say "9" or "12", they're stale.

### Example 4 — outstanding-URL count

Drafting §1 status line. Claim: "~7 outstanding URLs."

**Verification:** count entries in §4.3:
- Item 1a (platform.claude.com): 2 URLs.
- Item 3 (openai.com/index/*): 3 URLs.
- Item 4 (pli.princeton.edu): 1 URL.
- Item 5 (docs.github.com risks-and-mitigations): 1 URL.

Total = 7. But: items 4 and 5 are not strictly Path-B-only (Princeton is Wayback-eligible; risks-and-mitigations has never been action-tried). So the claim must qualify: "~7 outstanding URLs (5 confirmed Path-B-only; 2 still eligible for retry)."

## Anti-patterns

- **"I summarized this earlier, let me just incorporate it."** That's the recipe for count drift. The earlier summary may have been wrong, or may have aged. Re-verify.
- **Skipping verification because the count "feels right."** The whole point of this skill is that count intuition decays as the doc grows. The 1-second tool call is cheaper than the iteration pass that finds the bug.
- **Writing the count and the Totals row but not regrepping.** A new row in a table updates the Totals row by *summation*, but the existing cross-references (e.g., §1 TL;DR, §5 task list) update by *editor action*. Each cross-reference is a separate edit that can drift.
- **Using "approximately" or "~" to dodge precision.** Sometimes appropriate (e.g., "~½ day estimate") but never for inventory counts. "~5 Path-B URLs" was a fudge; the precise answer was 5 plus 2 retry-eligible, and the precision is what made the doc trustworthy.
- **Letting one edit pass own the verification for all cross-references.** Each edit pass must re-verify any count it touches, even if you "just verified it last pass."

## Acceptance criteria

1. Every numeric claim in the new edit traces to a tool call run within the same session (not from prior recollection).
2. The commit message body or the doc itself notes the verification command for at least the load-bearing counts (top-of-doc totals, cumulative backlogs).
3. After the edit, `grep -nE "<the number>"` across the doc shows the count appearing only where it should, with no stale alternate values.
4. When a cumulative total is written, all its components are verified within the same edit.
5. Mismatch between a draft count and the verified count is resolved in favor of the verified count, with the mismatch noted briefly so the reviewer can see what was caught.

## Files this skill creates / modifies

- The doc under edit (whatever long-lived status doc triggered the skill).
- Optionally: a short verification trace in the commit message body. No separate verification artifact is needed.
