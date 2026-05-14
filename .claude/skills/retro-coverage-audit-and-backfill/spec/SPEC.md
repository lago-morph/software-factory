# Spec: `retro-coverage-audit-and-backfill`

This is the reference spec for the `retro-coverage-audit-and-backfill` skill. The operational entry point is `../SKILL.md`. This file carries the extended rationale, worked examples, and design notes that don't fit in the operational form.

---

## Intent

Find PR ranges in a repo's history that aren't covered by any retrospective ("dark zones") and optionally produce synthetic back-filled retros for them from PR descriptions and surrounding contemporaneous retros.

The motivating problem: retrospectives are written at convenient checkpoints, not at deterministic session boundaries. Work that lands between checkpoints — especially during multi-PR bursts or weekend sprints — gets no narrative record. Three days later, no one remembers why a particular skill was authored, why a directory was reorganized, or what near-miss informed a tightened rule. The repo carries the PRs as audit trail but loses the *lessons*.

Retrospectives are themselves a load-bearing primary source for the agents-file rules and ADRs that govern future sessions. Missing retros = missing rule-extraction = lessons get re-learned the hard way.

---

## Why two output invariants

The two mandatory output invariants (synthetic-flagging and coverage-dating) are not stylistic preferences. They preserve two distinct properties of the retrospective corpus:

### Invariant 1 — Synthetic-flagging preserves the trust gradient.

Contemporaneous retros report what the author *observed* during the session. Synthetic retros report what the author *inferred* from PR descriptions written by someone else. Those are different evidentiary classes.

Without the flag, the corpus loses this distinction. A reader auditing "what did we learn about X?" cannot tell whether the cited retro lesson was witnessed or reconstructed. The cost of the rule is one metadata line; the cost of not having it is silent provenance erosion across the entire retrospective archive.

### Invariant 2 — Coverage-dating preserves the chronological audit trail.

The retrospective corpus is browsed chronologically against the PR stream. A reader looking up "what happened around PR #25?" expects to find `retrospective/2026-05-11-25.md` (PR #25 merged on 2026-05-11), not whatever date the synthetic was authored. The PR-anchored suffix makes this lookup trivially direct: the filename's tail IS the PR number.

Dating to coverage also makes future coverage audits (re-runs of this very skill) work correctly: the audit compares retro files to PR merge dates; if synthetic retros were dated to authorship, the audit would misattribute their coverage.

Filenames are append-only for the same reason: a `2026-05-11-25.md` back-fill authored on 2026-05-14 keeps its name even if a later back-fill produces a more-authentic retro covering the same window. If two retros legitimately end at the same date and last-PR (e.g., one infra narrative, one docs narrative), the collision is resolved by an appended letter suffix (`-25-a`, `-25-b`, …) — never by renaming or renumbering. Naming stability is part of the audit trail.

---

## Two worked examples

### Example A — audit-only (no back-fill)

**Invocation:** *"What is the coverage of retrospectives in terms of pull requests? How many PRs did each retro cover, and how many are missing?"*

**Step 1 — inventory retros.** Found 5 files in `retrospective/`: `2026-05-11-01.md`, `2026-05-13-01.md`, `2026-05-13-02.md`, `2026-05-14-01.md`, `2026-05-14-02.md`. Read each; extracted "Commit hashes by PR" sections.

**Step 2 — inventory PRs.** Called `mcp__github__list_pull_requests` with `state=all, sort=created, direction=asc, perPage=100`. Response was 134 KB JSON — exceeded the tool-result cap. Harness saved to `/root/.claude/projects/.../tool-results/mcp-github-list_pull_requests-*.txt`. Parsed out-of-band:

```bash
python3 -c "
import json
data = json.load(open('/root/.claude/projects/-home-user-software-factory/.../tool-results/mcp-github-list_pull_requests-*.txt'))
for pr in data:
    print(f\"#{pr['number']}\t{pr['state']}\tmerged={pr.get('merged_at','none')}\t{pr['title']}\")
"
```

Got 37 PRs. Numbers `#1`–`#50`. Gaps at `#4, #8, #23, #24, #26–31, #36, #41, #42`.

**Step 3 — recognize the namespace.** Confirmed the gap numbers were absent from the PR list (they are issues filed in those slots — `fetch-urls` issues mostly). Ignored.

**Step 4 — compute coverage.** Classified each PR:
- 14 covered (named in some retro's "Commit hashes by PR" section).
- 5 retro-commit-only (`#14, #35, #45, #47, #48`).
- 5 acknowledged (round-2 parallel-agent PRs that retro 2026-05-11-01 noted but did not author).
- 13 dark (no retro mention).

**Step 5 — identify zones.** Two zones:
- **Zone 1** = PRs `#11–#25`, 2026-05-11 01:24Z–12:48Z, ~11 h 24 m. 12 dark PRs (plus `#14` retro-commit-only mixed in).
- **Zone 2** = PRs `#49, #50`, 2026-05-14 01:46Z–02:46Z, ~1 h. 2 dark PRs.

**Step 6 — render report.** Inline output: per-retro table, ASCII timeline marking the two ~36 h and ~17 h *silence* gaps separately from the dark *zones*, dark-zone PR lists, headline numbers (37/14/13/biggest=36h).

Output: inline coverage report. No on-disk artifacts.

### Example B — back-fill (immediately after Example A)

**Invocation:** *"create a synthetic retrospective for the first dark zone from 11 to 25. Lean heavily on the text in the pr description... date it as if it was done when the last pr in the sequence was merged"*

**Step 7 — fetch PR bodies.** Single parallel block, 13 calls to `mcp__github__pull_request_read method=get` for `#11, #12, #13, #14, #15, #16, #17, #18, #19, #20, #21, #22, #25`. All returned. `#25`'s body was empty (initialization-state PR for a fanout); recovered from title + commit-count.

**Step 8 — date and last-PR anchor.** Last PR in zone = `#25`, merged `2026-05-11T12:48:03Z`. `COVERAGE_DATE = 2026-05-11`. `PR = 25`. Path = `retrospective/2026-05-11-25.md`. (No collision with existing files — `2026-05-11-01.md` is the contemporaneous retro using the legacy day-sequence scheme; the new PR-anchored name lands in a different slot.)

**Step 9 — synthesize narrative.** From 13 PR bodies, extracted 10 phases:

1. Skill extraction (PR #11) — three internal skills authored.
2. Cache eviction (PR #12) — `−39,243` deletions of incorporated source files.
3. PR #13 → #14 redundancy — fresh-branch PR closed in favor of folding onto in-flight branch.
4. ADR + retro-skill rewrite (PR #14).
5. Path-flatten (PR #15) — `retrospective/report/` → `retrospective/`.
6. PR-lifecycle hardening (PR #16) — directly informed by the #13 mistake.
7. Three PLAN.md consolidations (PRs #17, #20, #21) — `followup.md` folded, workflow-tooling catalogued, external-synthesis filing pattern.
8. Two Phase-0 drains (PRs #18, #19) — Klaassen unlock; Dark Factory primary source via Path B; Lenny video-only reclassification.
9. Fanout-skill hardening (PR #22) — `isolation: "worktree"` mandate.
10. The 26-subagent fanout (PR #25) — 68 commits, 6 h 50 m wall time.

**Three inferred lessons** marked as inferences in the self-reflection section:

- The PR #13 → #14 fresh-branch mistake — inferable because PR #16 explicitly tightened the rule against it. The PR descriptions don't say "I made a mistake"; the gradient between #13's intent and #16's rule reveals it.
- The Lenny video-only reclassification — inferable from PR #19's body quoting the user's note ("just a video"). Three retrieval routes had chased a body that didn't exist.
- The meta-observation that retro 1 was written mid-session — inferable from comparing retro 1's coverage window (up to #10) to the PR stream's continued activity (11 more PRs after retro 1's commit).

**Step 10 — write.** `retrospective/2026-05-11-25.md`, 323 lines. Metadata block flagged `SYNTHETIC / BACK-FILLED`. End-of-file marker re-states the provenance.

**Step 11 — commit.** Hash `f06e2f5`. Pushed to `claude/analyze-retro-coverage-WDhhM`. No PR opened (synthetic retros default to local-history-only).

**Step 12 — inline summary.** ~12 lines, named the path, the PR range, the 10 phases, and 3 inferred lessons.

---

## Design notes

### Why parallel-block PR fetches

Step 7 fetches all PR bodies in a single message with N parallel tool calls (one per PR). Sequential fetching is correct but slow at N=10+. Parallel fetching is reliable because PR-read calls are independent and the MCP server can handle concurrent requests. The 13-call parallel block in Example B completed in roughly the same wall-time as a single call.

### Why an empty sibling directory is OK for synthetics

The standard retro layout pairs `retrospective/YYYY-MM-DD-PPP.md` with `retrospective/YYYY-MM-DD-PPP/` (where `PPP` is the last PR number; or the legacy `-NN` suffix for the no-PR fallback). Contemporaneous retros populate the sibling directory with skill specs and `AGENTS-suggestions.md`.

Synthetic retros should not fabricate skill specs from material they didn't witness. The directory is created for layout consistency but may be empty. Git will ignore an empty directory at commit time — that's fine; the directory is implicit and any future user-driven skill-spec authoring will materialize it.

### Why the inference / observation distinction matters

The skill explicitly asks for self-reflection in the synthetic retro (Step 10's "self-reflection section at the end"). That section is the most valuable output — it carries the lessons. But synthetic self-reflection is inference, not observation. The PR author did not write "I made a mistake"; the synthesizer is reading rule-tightenings and reconstructing the mistake.

If the synthetic retro presents inferences as observations, future readers will treat them as primary evidence and propagate them downstream as if witnessed. That's a fabrication risk. The skill mitigates it by:

1. Flagging the whole retro as synthetic (Invariant 1).
2. Asking the synthesizer to explicitly mark inferences as inferences in the self-reflection section.

The Provenance line and the inference-marking together make the evidentiary class auditable.

### Why dark-zone size matters

A zone of 1–2 dark PRs typically lacks the narrative volume to support a phase-decomposed retrospective. The synthesizer would either produce a thin document (~50 lines with one or two phases) or inflate the material with low-content commentary. Both are worse than folding a brief mention into the next contemporaneous retro.

A zone of ≥5 dark PRs typically has enough PR-description material to support 3+ phases, real metrics, and several inferred lessons. The 13-PR zone in Example B produced a 323-line retro that compares favorably to contemporaneous retros in the same corpus (12–15 KB range).

Between 3 and 5 is judgment-call territory. Surface in the audit; ask the user.

### Why the skill defaults to "no PR opened"

Synthetic retros are inherently more contested than contemporaneous ones — the user may want to revise inferences, remove fabricated-feeling phrasing, or correct the dating. Defaulting to local-history-only commits gives the user a review pass before the artifact becomes a permanent PR record.

The `--pr` flag (if added) should be deliberate.

---

## Failure modes and recovery

### Failure: PR description is empty

Some PRs (especially auto-generated fanout state commits) have empty bodies. Recovery: use the PR title + the commit log (`mcp__github__pull_request_read method=get_files` or `git log <branch> ^main`) as the narrative source. Mark the phase as "PR body empty; reconstructed from commits."

Example B's PR #25 had this — title said "fanout 20260511-054258: initialise state for 26-subtask drain of PLAN.md R2/R3/R4/R5"; commit count was 68; line diff was `+5908 / -2`. Enough to write a one-paragraph phase narrative.

### Failure: PR-list response is too large to read

The harness saves the response to `/root/.claude/projects/.../tool-results/<filename>.txt`. Parse via `python3 -c "import json; data = json.load(open('<path>')); ..."`. Do NOT re-run the MCP call with finer filters; the saved file is canonical.

### Failure: two retros disagree on which one covered a PR

Treat both as covering it. Coverage is union-typed; a PR named in multiple retros' "Commit hashes by PR" sections is over-covered, not contested.

### Failure: a contemporaneous retro exists at the same date and same last-PR you'd assign

This only happens if the synthetic's zone ends at exactly the same PR a contemporaneous retro already covered. In practice this almost always means the zone definition is wrong — re-examine the dark-zone bounds, because the contemporaneous retro probably already covered the work and the zone was misclassified as dark.

If two retros legitimately end at the same date and last-PR (e.g., a contemporaneous infra narrative and a synthetic docs narrative covering the same window from different angles), resolve the collision by appending a lowercase letter suffix: `2026-05-11-25-a.md`, `2026-05-11-25-b.md`, … Letter suffixes are append-only and never re-letter an existing file.

### Failure: the user wants the synthetic to become a PR

That's fine — open it explicitly via `mcp__github__create_pull_request` with a title like `Synthetic retrospective YYYY-MM-DD-PPP for PRs #X–#Y` (where `PPP` is the last PR in the zone, the same anchor used in the filename). Make the PR body re-state the SYNTHETIC / BACK-FILLED provenance so reviewers see it without opening the file.

---

## Files this skill creates / modifies

- `retrospective/YYYY-MM-DD-PPP.md` — one per synthesized retro. `PPP` is the number of the last PR in the zone (the same PR that anchors the coverage date). `YYYY-MM-DD` is the coverage date (Invariant 2). On collision with an existing file at the same date and last-PR, append `-a`, `-b`, … to the suffix.
- `retrospective/YYYY-MM-DD-PPP/` — sibling directory per the standard retro layout. Often empty for synthetics; acceptable.
- No modifications to existing retros. Existing retros are read-only inputs.

---

## See also

- `../SKILL.md` — operational skill file.
- `.claude/skills/self-retrospective/SKILL.md` — the canonical retro-authoring skill. This skill's output format mirrors it, with the added SYNTHETIC / BACK-FILLED metadata flag and the coverage-dating invariant.
- `.claude/skills/adr/SKILL.md` — for proposed ADRs surfaced by the audit or synthesis.
