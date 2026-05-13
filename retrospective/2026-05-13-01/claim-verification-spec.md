# Spec: `claim-verification`

## Intent

When writing or revising any structured document (plan, ADR, retrospective, report), every factual claim — counts, dollar figures, dates, attributions, hashes, cross-references — must trace to a source before commit. The default failure mode is **plausible-sounding fabrication** that survives multiple audit passes because it reads naturally in context.

This skill solves a specific failure pattern observed in the 2026-05-13 session: a `~$15–25 in Anthropic API calls per the run report` cost claim was written into `research/PLAN.md` v0.8's §9, survived **four** user-prompted audit passes, and was only caught on the fifth pass when the auditor checked the run reports for the figure. The figure did not exist in any run report. Similarly, a "Klaassen siblings fetched via Wayback in issue #23" attribution survived four audit passes before pass 5 checked the issue's bot comments and found the fetch was direct, not Wayback. Both fabrications contradicted other claims in the same document.

The cost of un-audited claims compounds: downstream readers anchor on the fabricated number, and the lie outlives the document version. The cost of running this skill on a claim is one tool call.

## Trigger

**Direct user phrases:**
- "Verify this claim"
- "Is this correct?"
- "Check the numbers"

**Proactive triggers (run without being asked):**
- Before committing any document with new counts, dollar figures, dates, or attributions.
- After a bulk rewrite of a structured document (any rewrite >100 lines).
- When auditing a PR's diff at user request.
- Before claiming a span like "F21–F33" (verify arithmetic).
- Before citing a commit hash, issue number, or PR number.

**Negative triggers:**
- Pure prose narrative without verifiable claims.
- Quotations from sources already cited verbatim.

## Inputs

- The document path or diff to audit.
- Optional: the specific claims to verify (otherwise: extract them automatically).

## Outputs

- A list of verified-vs-unverified claims.
- For each unverified claim: the source the agent checked (and what it found).
- Fixes applied to the document (or a list of fixes the user should make).

## Workflow

1. **Extract verifiable claims from the document.** Use regex/grep to find:
   - Counts: `\b\d+ (reports|threads|subagents|failure modes|skills|rows|chapters|files|URLs|words)\b`
   - Dollar figures: `\$\d+`
   - Date claims: `\d{4}-\d{2}-\d{2}`
   - Commit hashes: `\b[0-9a-f]{7,40}\b`
   - Issue/PR references: `#\d+`
   - Range claims: `F\d+–F\d+`, `§\d+(\.\d+)?–§\d+(\.\d+)?`
   - Attribution claims: `via (Wayback|GitHub Action|browser cookies|Path B)`, `authored by`, `produced by`

2. **For each claim, identify the source-of-truth:**
   - Counts → `ls`, `wc -l`, `grep -c`
   - Dollar figures → the run report or invoice that should contain them
   - Dates → `git log -1 <hash> --format=%ai` or `date -u`
   - Commit hashes → `git log -1 <hash>` (does it exist? does the subject match?)
   - Issue/PR references → `mcp__github__issue_read` or `mcp__github__pull_request_read`
   - Range claims → arithmetic (33 − 21 + 1 = 13)
   - Attribution claims → the issue's bot comments, the source file's content, the git history

3. **Run the verification command. Compare against the claim:**
   - If match: mark verified.
   - If mismatch: flag with the actual value, propose a fix.
   - If no source: mark unverifiable. The document must either (a) cite a source or (b) drop the claim.

4. **Apply fixes** (or list them for user review).

5. **Re-grep the fixed document** to confirm no new instances of the old claim remain.

## Concrete examples

### Example 1: fabricated dollar figure

**Document context (research/PLAN.md §9):**
> Rounds 3–6: night run consumed ~$15–25 in Anthropic API calls per the run report.

**Extraction:** matched `\$\d+` → `$15-25 ... per the run report`. Source-of-truth: `harness/runs/20260511-054258/report.md` and `report-pt2.md`.

**Verification:**
```bash
grep -iE "15-25|15–25|\\\$15|\\\$25|api cost|api call" \
  /home/user/software-factory/harness/runs/20260511-054258/report.md \
  /home/user/software-factory/harness/runs/20260511-054258/report-pt2.md
# (no matches)
```

**Outcome:** unverifiable. The figure does not exist in the cited source.

**Fix applied:**
```diff
- Rounds 3–6: night run consumed ~$15–25 in Anthropic API calls per the run report
+ Rounds 3–6: catalogued in the parallel-fanout night run on 2026-05-11. Token-level detail per subtask lives in `harness/runs/20260511-054258/report.md` and `report-pt2.md`; no dollar total recorded.
```

### Example 2: range-claim arithmetic

**Document context (research/PLAN.md §1):**
> 21 new failure modes (F21–F33) catalogued

**Extraction:** matched `F\d+–F\d+` → `F21–F33`. Verification:
```python
>>> 33 - 21 + 1
13
```

But the claim says "21". This contradicts §11 in the same document ("13 new failure modes (F21–F33)").

**Outcome:** internal inconsistency; arithmetic gives 13, §11 agrees with 13. Apply fix.

**Fix applied:**
```diff
- 21 new failure modes (F21–F33) catalogued
+ 13 new failure modes (F21–F33) catalogued
```

### Example 3: attribution claim verified against issue comments

**Document context (research/PLAN.md §4.4):**
> The three Klaassen Every.to siblings — successfully fetched via Wayback in (now-closed) fetch-urls issue #23. Re-fetch would be duplicate work.

**Extraction:** matched `via Wayback in (now-closed) fetch-urls issue #23`. Source-of-truth: `mcp__github__issue_read` with `method: get_comments` on issue #23.

**Verification:** issue #23's bot comments show the URLs were `https://every.to/chain-of-thought/...` (direct), with HTTP 200 + byte counts — NOT Wayback URLs (which would have `https://web.archive.org/web/...`).

**Outcome:** attribution claim is wrong; the fetch was direct.

**Fix applied:**
```diff
- The three Klaassen Every.to siblings — successfully fetched via Wayback in (now-closed) fetch-urls issue #23. Re-fetch would be duplicate work.
+ The three Klaassen Every.to siblings — successfully fetched directly via the GH Action runner in (now-closed) fetch-urls issue #23 (the every.to URLs returned HTTP 200 from the runner despite blocking the sandbox). Re-fetch would be duplicate work.
```

## Anti-patterns

- **Verifying only the easy claims.** Counts and arithmetic are easy. Attribution and source-existence claims are where fabrication lives. Don't stop at the easy ones.
- **"It sounds right" as verification.** A natural-sounding claim is exactly the kind of fabrication this skill is designed to catch.
- **Trusting your own memory of "what we did".** The 2026-05-13 session author wrote two fabricated claims into v0.8 with high confidence; they survived four audits. Verify against the actual data.
- **Stopping after one audit pass.** This session's `$15–25` fabrication and the Wayback misattribution both survived four passes. Run two consecutive passes that find nothing before declaring an audit clean.
- **Only running the skill when prompted.** This skill is most valuable as a proactive trigger before committing structured documents. Once a fabrication is committed, downstream readers (and future agent sessions) anchor on it.

## Acceptance criteria

1. Given a document with at least one fabricated count/figure/attribution, the skill catches it in pass 1.
2. The skill explicitly reports per-claim verification status: verified / mismatched / unverifiable.
3. The skill produces concrete fix proposals for mismatched and unverifiable claims (not vague "consider revising").
4. After a fix is applied, a re-grep of the same regex returns no instances of the original wrong text.
5. The skill is idempotent: a second pass on a clean document produces no findings.

## Files this skill creates / modifies

- Modifies the audited document(s) in place with corrections.
- Creates an audit log (optional, for diff-review purposes): `audit-claims-<UTC-date>.md` with per-claim verification status. Not committed by default — surfaced inline in chat.
