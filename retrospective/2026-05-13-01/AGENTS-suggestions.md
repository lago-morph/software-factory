# AGENTS.md suggestions — 2026-05-13-01

These are proposed additions to the project's agents file (typically `AGENTS.md` at the repo root). Each section contains:

1. **Proposed addition** — the exact text to paste.
2. **Why this earns its place in your agents file** — the argument for doing it, grounded in something that happened (or nearly happened) this session.

Decide each on its own merits. Skip ones that don't apply to your operating posture; copy-paste the ones that do.

---

## Suggestion 1: Never fabricate numbers, even in "approximate" sections

### Proposed addition

> **Verify claims before writing them.** If you can't trace a count, dollar figure, date, attribution, or commit hash to a source via a tool call, do not write it. "Approximate" qualifiers do not authorize fabrication. When estimating, write `unknown` or cite a method ("see X for token-level detail") instead of a made-up round number.
>
> *Grounded in: 2026-05-13 PLAN.md v0.8 audit pass 5.*

### Why this earns its place in your agents file

The 2026-05-13 cleanup-pass commit introduced a `Rounds 3–6: night run consumed ~$15–25 in Anthropic API calls per the run report` claim into `research/PLAN.md` §9. No such figure existed in `harness/runs/20260511-054258/report.md` or `report-pt2.md` — the auditor checked. The claim survived four user-prompted audit passes before pass 5 caught it, because in context it reads naturally — a small-dollar approximation is exactly the shape of claim that "approximate" sections invite. A fabricated $15–25 anchors a downstream reader's mental model of cost; a future ROI calculation built on it is built on a lie.

Cost of adopting the rule: one extra `grep` per claim, ~30 seconds. Cost of not adopting it: four audit passes to catch one fabricated number.

---

## Suggestion 2: After bulk regex / sed, read the per-file diff before committing

### Proposed addition

> **Bulk regex / sed audit.** Before committing a `sed -i` or `xargs sed -i` that touched >2 files, read the per-file `git diff` in full. Look for matches that landed inside narrative prose rather than literal path / code contexts — those are usually unintended. When in doubt, prefer targeted `Edit` calls over bulk sed.
>
> *Grounded in: 2026-05-13 PR #33 cleanup pass sed regression.*

### Why this earns its place in your agents file

The 2026-05-13 cleanup pass ran a five-substitution sed pipeline over 14 markdown files. The last substitution (`s|research/manual/|reference-only/|g`) over-reached, mangling four citations in `research/07-dark-factory.md` whose original paths were historical-provenance references. Recovery required restoring three files from git history with new filenames and four targeted re-edits. Total cost: ~25 minutes of cleanup. Total cost of reading the diff before commit: ~3 minutes.

Sed is a power tool; the audit is the safety. Make the audit non-optional.

---

## Suggestion 3: After major section restructure, re-resolve every cross-reference

### Proposed addition

> **Cross-reference re-resolution after restructure.** After any document rewrite that renumbers sections or moves >100 lines, grep for every `§N(.M)`, every cited file path, and every commit hash in the new document. Verify each against the new structure (does the section exist? does the path resolve? does the hash exist?). Treat unresolved references as bugs even if the prose around them reads naturally.
>
> *Grounded in: 2026-05-13 PLAN.md v0.8 audit passes 2 and 3.*

### Why this earns its place in your agents file

The 2026-05-13 PLAN.md rewrite renumbered ten sections. The first commit shipped with five stale cross-references: `see §6` (was the curated review section in v0.7, became Resumption checklist in v0.8); `PLAN §17 (was §13.1.6)` (§17 became Version history; §13.1.6 was Anthropic trilogy); `Sections 11–18` (highest archive section is §17); `was §§1–4 of v0.1` (Round 1 predates v0.1); `11 followup reports` (became 12). None of these were caught by a manual read-through because in context they sound right.

The audit is mechanical: `grep -oE '§[0-9]+(\.[0-9]+)?'` followed by per-reference verification. Five-minute task that would have prevented two audit passes.

---

## Suggestion 4: When claiming a count over a range, verify the arithmetic

### Proposed addition

> **Range-claim arithmetic verification.** Any claim of the form "N items in range A–B" must satisfy `N = B − A + 1`. Verify with arithmetic before committing.
>
> *Grounded in: 2026-05-13 PLAN.md v0.8 §1 "21 new failure modes (F21–F33)".*

### Why this earns its place in your agents file

PLAN.md v0.8's §1 claimed "21 new failure modes (F21–F33)". F21 through F33 inclusive is 13 modes (33 − 21 + 1 = 13). The same document's §11 correctly said "13 new failure modes (F21–F33)". The mismatch survived three audit passes before pass 4 caught it. A reader trusting §1 over §11 would carry the wrong count into downstream work.

This is a five-second arithmetic check. It catches a class of bugs that are otherwise invisible.

---

## Suggestion 5: Audit passes are part of the work, not a follow-up

### Proposed addition

> **Iterative self-audit after large changes.** After any single change that modifies >100 lines of a structured document, run at least three internal audit passes before declaring the work complete. The audit checks: section cross-references resolve, counts verify, paths exist, internal consistency holds, attribution claims trace to sources. The work is not done until two consecutive audit passes find nothing.
>
> *Grounded in: 2026-05-13 PR #34 audit-pass cycle (5 user-prompted passes catching 15 bugs).*

### Why this earns its place in your agents file

PR #34's PLAN.md changes took five audit passes, each user-prompted, to fully clean up. Pass 4 caught a fabricated cost figure that had survived three prior passes. Pass 5 caught a wrong factual attribution that had survived four. The user's visible frustration ("It is very frustrating that you keep finding bugs in your updates") signaled that the audit cadence was reactive rather than proactive.

Make the audit the agent's responsibility, not the user's. Three to five self-audit passes during the work prevents the user from having to keep prompting. The cost is a few minutes per pass; the benefit is one PR instead of five.

---

## Suggestion 6: `git fetch` before any branch-base operation

### Proposed addition

> **Sync remote refs before branching.** Run `git fetch origin` before any operation that depends on remote branch state: branching off main, comparing against another branch, checking PR mergeability. Local refs can be many commits stale; reasoning from a stale local view produces wrong conclusions.
>
> *Grounded in: 2026-05-13 PR #33 cleanup pass.*

### Why this earns its place in your agents file

When inspecting the side branch at the start of the cleanup pass, local `main` was 30+ commits behind `origin/main`. A `git log main..` query returned a misleading commit list. Without fetching first, the agent would have concluded the pt-2 work was on main when it wasn't. The fetch took 2 seconds.

The pattern "always fetch first" is cheap insurance against reasoning from stale state.

---

## Suggestion 7: Verify attribution claims against the actual source, not memory

### Proposed addition

> **Attribution claims trace to source data.** Statements of the form "X was retrieved via Y" or "X is sourced from Z" must be verified against the source data (issue comments, commit content, file existence, log) before commit. Do not write attribution claims from recollection alone.
>
> *Grounded in: 2026-05-13 PLAN.md v0.8 "Klaassen siblings fetched via Wayback in issue #23" misattribution.*

### Why this earns its place in your agents file

PLAN.md v0.8 included the claim "The three Klaassen Every.to siblings — successfully fetched via Wayback in (now-closed) fetch-urls issue #23." This was wrong. Issue #23's bot comments showed the URLs were fetched directly (HTTP 200 from the runner), not via Wayback. The misattribution survived four audit passes because in context it read naturally. Worse, it directly contradicted another claim in the same document (§3.1's corpus-level lesson "every.to is action-fetchable"). The auditor only caught it on pass 5 by running `mcp__github__issue_read` with `method: get_comments` against issue #23.

Memory-based attribution is a high-confidence source of fabrications. Tool-based verification is the antidote.

---

## Suggestion 8: When deleting via editorial collapse, identify unique content first

### Proposed addition

> **Editorial collapse content audit.** Before deleting a file whose content is being merged into a successor file, identify any content unique to the deleted file and explicitly preserve it. Do NOT assume the successor already covers everything — read both end-to-end and tabulate the union.
>
> *Grounded in: 2026-05-13 PR #32 editorial collapse of `09-jaymin-harnesses-partial.md`.*

### Why this earns its place in your agents file

The editorial collapse of `research/09-jaymin-harnesses-partial.md` into the unified `09-jaymin-book-harnesses-practices-mental-models.md` would have lost the Substack manifesto digest (the partial's §12, with seven verbatim rules) if the agent had assumed the unified report covered the same ground. The partial's §1–§11 were Ch 6 index-page summaries (fully superseded by the unified report's direct sub-page reads); §12 was unique. Identifying the unique content and folding it into a new §9 of the unified report was the right move; the deletion happened after.

The opposite mistake — assuming "the new file covers it" — would have silently lost ~70 lines of verbatim quoted material from a primary source.

---

## Suggestion 9: Prefer discrete commits per audit pass over `git commit --amend`

### Proposed addition

> **Audit-pass commits over amending.** When iteratively fixing bugs in a single PR, prefer discrete commits per audit pass (e.g., "audit-pass-N: fix X, Y, Z") over `git commit --amend`. The discrete commits give the reviewer an audit trail; each pass's findings stay legible.
>
> *Grounded in: 2026-05-13 PR #34 commit history.*

### Why this earns its place in your agents file

PR #34 ended with 10 commits: 4 cherry-picks, 1 main update, and 5 audit-pass fixes (`8eee478`, `20da79f`, `a7ec210`, `d827316`, `411a0ae`). The reviewer can see exactly what each audit pass caught. An amend strategy would have hidden the audit cadence and made review harder.

Cost: the PR has more commits. Benefit: the commit log IS the audit trail. For PRs under review, this trade is almost always worth it.
