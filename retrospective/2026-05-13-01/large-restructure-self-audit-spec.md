# Spec: `large-restructure-self-audit`

## Intent

When restructuring a complex multi-section document (rewriting a plan, reorganizing sections, renumbering, compressing accreted content), the rewrite introduces a predictable class of bugs: stale cross-references, broken section numbers, inherited inconsistencies that surface only in the new context, fabricated claims that filled gaps in the rewriter's recollection. **These bugs are mechanical to find but invisible until specifically audited.**

This skill solves a frustrating session pattern: a 1055-line PLAN.md rewrite to 340 lines (v0.7 → v0.8 → v0.9) produced **15 bugs caught across 5 user-prompted audit passes**. Each pass had to be triggered explicitly by the user ("check the diff very critically", "ONCE AGAIN", "iterate until you don't find any more bugs"). Almost every bug was mechanically detectable: count arithmetic, dead `§N` cross-references, paths-that-don't-resolve, inherited internal inconsistencies. **The audit passes belong inside the rewrite, not as a follow-up triggered by user frustration.**

## Trigger

**Direct user phrases:**
- "Restructure this document"
- "Compress this section"
- "Rewrite this plan"
- "Reorganize sections"

**Proactive triggers (run without being asked):**
- After any rewrite that changes >100 lines OR renumbers sections OR compresses prior detail.
- After a `git mv` or directory reorganization where paths inside docs need updating.
- Before opening a PR whose primary content is a documentation restructure.

**Negative triggers:**
- Small targeted edits (<20 lines).
- Edits that don't touch section numbering or cross-references.

## Inputs

- The document path(s) restructured.
- Optional: the pre-restructure version reference (commit hash or path).

## Outputs

- A report listing each category of finding (stale cross-references, count mismatches, broken paths, unverifiable claims).
- Fixes applied to the document(s).
- A "passes-required" counter: the audit isn't done until two consecutive passes find nothing.

## Workflow

Run **all five categories** below in sequence. After fixing each batch, re-run. Continue until two consecutive passes find nothing across all categories.

### Category 1 — section-reference resolution

```bash
# Extract every §N or §N.M from the doc
grep -oE "§[0-9]+(\.[0-9]+)?" <doc> | sort -u

# For each, verify it matches an actual heading
grep -nE "^## [0-9]+\.|^### [0-9]+\.[0-9]+ " <doc>
```

Flag any `§N` reference whose target doesn't exist in the new structure. Distinguish:
- **Stale forward references** (point at non-existent section in new structure): FIX.
- **Historical references in version-history or "(was §X in v0.Y)" annotations**: KEEP as historical.

### Category 2 — count claims vs reality

For each numeric claim in the document, verify against an on-disk source:

```bash
# Counts of files
ls research/followup/*.md | wc -l
ls research/[0-9]*.md | wc -l
ls architectures/*.md | wc -l

# Counts in tables — grep for row patterns
grep -c "^| [0-9]" <doc>

# Range arithmetic — verify (high − low + 1) matches the claim
# e.g., "F21–F33" should give 13, not 21
```

Flag any count claim that doesn't match its source.

### Category 3 — path resolution

```bash
# Extract every `path/like/this` from the document
grep -oE '`[a-zA-Z0-9_-]+/[A-Za-z0-9._/-]+`' <doc> | tr -d '`' | sort -u

# For each, test existence
for p in $paths; do
  [ -e "$p" ] && echo "OK   $p" || echo "MISS $p"
done
```

Distinguish:
- **MISS as forward-looking instruction** (e.g., paths the user is told to create): OK.
- **MISS as stale documentation** (paths that used to exist but were moved): FIX.

### Category 4 — internal consistency

Check that claims within the document agree with each other:

```bash
# Same claim made in two places — do they match?
grep -E "(13|21) new failure modes" <doc>
grep -E "[0-9]+ followup reports|[0-9]+ follow-up threads" <doc>
```

Flag any two passages that make incompatible claims about the same fact.

### Category 5 — attribution / source claims

For each "via X" or "per Y" attribution claim, verify against the source data:

```bash
# Issue comments
mcp__github__issue_read --issue_number N --method get_comments

# Commit existence + subject
git log -1 <hash> --format="%h %s"

# File existence at time of claim
git log --follow <path>
```

Flag any attribution claim that doesn't match its source.

### Acceptance bar

The audit is not done until **two consecutive passes through all five categories find nothing**. Counting passes:
- Pass 1: identifies N bugs. Fix them.
- Pass 2: identifies 0 bugs. Audit is NOT done (one clean pass is insufficient).
- Pass 3: identifies 0 bugs. Audit IS done.

## Concrete examples

### Example 1: PLAN.md v0.8 → v0.9 restructure

After rewriting `research/PLAN.md` from v0.7 (1055 lines, §§1–14) to v0.8 (340 lines, §§1–17 with archive at §§11–17), five audit passes caught 15 bugs:

**Pass 1 findings (sed regressions + factual error):**
- Bulk sed `s|research/manual/|reference-only/|g` had over-reached, mangling four citations in `research/07-dark-factory.md`.
- Round-3 Thread 12 (Dark Factory, RESOLVED) was conflated with the post-Round-3 Brier work (`followup/12-brier-pace-layers.md`).

**Pass 2 findings (stale status):**
- §1 status line still said "one significant batch of unmerged work on a side branch" but this PR was resolving it.
- "Not done" subsection listed §6 as "Curated human-review tasks" — but §6 is the Resumption checklist; curated tasks live in §3.2.

**Pass 3 findings (5 stale cross-refs):**
- `11 followup reports` (should be 12 after the recovery added followup/12)
- `see §6` for spec-driven-ai-dev.md pending update (should be `§3.2 task 2`)
- `PLAN §17 (was §13.1.6)` (§17 is version history; the §13.1.6 was about Anthropic trilogy, but kaner.com is unrelated; should point at unfetched-sources.md row 5)
- `Sections 11–18 below` (highest archive section is §17, not §18)
- `(was §§1–4 of v0.1)` for Round 1 (Round 1 predates v0.1 of PLAN.md)

**Pass 4 findings (internal consistency):**
- §1 said "21 new failure modes (F21–F33)" while §11 said "13". Arithmetic: 33 − 21 + 1 = 13. §1 was wrong.
- §11 "Round 2 dispatched 6 subagents plus a synthesis run" — implied 7, but the list shows 6 (subagent 13 IS the synthesis). Ambiguous wording.

**Pass 5 findings (unverifiable / fabricated claims):**
- §9 "Round 2: ~50k × 13 subagents" — the "13" was unverifiable; Round 2 had 6 subagents per §11.
- §9 "Rounds 3–6: night run consumed ~$15–25 in Anthropic API calls per the run report" — `grep -iE "\\$15|\\$25" harness/runs/20260511-054258/*.md` returned nothing. Figure fabricated.
- §4.4 "Klaassen Every.to siblings successfully fetched **via Wayback** in issue #23" — issue #23's bot comments showed direct fetches with HTTP 200. The Wayback attribution was wrong, AND contradicted §3.1's own corpus-level lesson.

**Five passes were required**; passes 4 and 5 each found bugs that the previous four had missed. The audit completed only after pass 6 found nothing.

### Example 2: reorganizing a directory and updating in-doc references

Moving `research/manual/multi/*` → `reference-only/el-kaim-book/*` should update every report citing those paths. Run:

```bash
git mv research/manual/multi/* reference-only/el-kaim-book/

# Find every report still citing the old path
grep -rln "research/manual/multi" --include="*.md" .

# For each match, update the citation. Verify with re-grep:
grep -rln "research/manual/multi" --include="*.md" .
# (should return nothing after fixes)

# Verify the new paths resolve
for p in $(grep -ohE "reference-only/el-kaim-book/[A-Za-z0-9 ._-]+" --include="*.md" -r . | sort -u); do
  [ -f "$p" ] && echo "OK $p" || echo "MISS $p"
done
```

## Anti-patterns

- **Skipping passes because "the document looks right".** The 2026-05-13 session's `$15–25` fabrication and Wayback misattribution **looked right** in context for four audit passes. Mechanical verification was the only thing that caught them.
- **One audit pass.** A single clean pass is insufficient evidence the audit is complete; the bugs caught in passes 4 and 5 of this session prove it.
- **Stopping when the user stops prompting.** This session's audit only completed because the user kept asking. The skill should run audit passes to completion under its own authority, before handing the PR off.
- **Only verifying easy claims.** Counts and arithmetic are easy. Attribution and existence claims are where fabrication lives.
- **Trusting your own recollection of "what we did" instead of grep/log.** This is how v0.8's fabrications got committed in the first place.

## Acceptance criteria

1. Every `§N(.M)` cross-reference in the new document resolves to an existing heading or is annotated as historical (in version-history / "(was §X in v0.Y)" form).
2. Every numeric claim (count, range, file-count) is verified against an on-disk source.
3. Every path cited in code-block backticks resolves to an existing file/directory, OR is annotated as a forward-looking instruction.
4. Internal consistency: claims made in two places agree.
5. Attribution claims trace to the cited source (issue comments, commit hashes, etc.).
6. **Two consecutive passes through all categories find nothing** before declaring the audit complete.

## Files this skill creates / modifies

- Modifies the audited document(s) in place.
- Optionally: creates `restructure-audit-<UTC-date>.md` recording per-pass findings (for PR review). Not committed by default.
