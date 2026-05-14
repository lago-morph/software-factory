# Spec: `retro-coverage-audit-and-backfill`

## Intent

Find PR ranges in a repo's history that aren't covered by any retrospective ("dark zones"), and optionally produce synthetic back-filled retros for them from PR descriptions and surrounding contemporaneous retros.

The motivating problem: retrospectives are written at convenient checkpoints, not at deterministic session boundaries. Work that lands between checkpoints — especially during multi-PR bursts or weekend sprints — gets no narrative record. Three days later, no one remembers why a particular skill was authored, why a directory was reorganized, or what near-miss informed a tightened rule. The repo carries the PRs as audit trail but loses the *lessons*. A retro-coverage audit identifies these gaps mechanically; the back-fill capability lets you recover the narrative from PR descriptions while it's still reconstructable.

This skill earns its place because retrospectives are themselves a load-bearing primary source for the agents-file rules and ADRs that govern future sessions. Missing retros = missing rule-extraction = lessons get re-learned the hard way.

## Trigger

### Direct triggers — activate immediately

- "What's the coverage of retrospectives?"
- "Which PRs aren't covered by any retro?"
- "Find the dark zones in our retro history."
- "Back-fill the missing retro for [period]."
- "Audit retro coverage."

### Proactive triggers — offer the skill without being asked

- User asks for "an approximate timeline of what retrospective covered what" (the audit half of this skill).
- User notes a recent retro and asks whether earlier work has the same treatment.
- A retro is being authored and the previous retro is more than ~10 PRs behind the current PR head.

### Negative triggers — do NOT offer

- The repo has only one or zero retros (nothing to audit against).
- The repo has no `retrospective/` directory and no convention.
- The user is asking about a single PR, not coverage.

## Inputs

- A repo with `retrospective/YYYY-MM-DD-NN.md` files that follow the `self-retrospective` skill's "Commit hashes by PR" convention (an H3 per PR, listing the branch + merge state).
- GitHub access via `mcp__github__list_pull_requests` and `mcp__github__pull_request_read`, OR `gh` CLI access.
- The repo's `owner/repo` slug (for MCP calls).

Optional arguments:

- `--zone <start>..<end>` — restrict back-fill to a specific PR range.
- `--audit-only` — produce the coverage report without back-filling.
- `--backfill-all` — back-fill every dark zone the audit finds (use with care; large zones produce large retros).

## Outputs

1. **Coverage report** (inline, in the chat reply): per-retro coverage table, timeline diagram with gap durations, list of dark zones with PR numbers.
2. **Zero or more synthetic retros** at `retrospective/YYYY-MM-DD-NN.md`, each:
   - Flagged `SYNTHETIC / BACK-FILLED` in the metadata block with authoring date + provenance.
   - Dated to the merge time of the **last PR** in the covered zone (not the authoring date).
   - Sequence-numbered as the next available `NN` for that UTC date (back-fills do not retroactively insert into the sequence).
   - Accompanied by an (often-empty) sibling directory `retrospective/YYYY-MM-DD-NN/` per the standard retro layout.

## Workflow

### Audit half

1. **Inventory existing retros.** `ls retrospective/*.md`, then `Read` each to extract its "Commit hashes by PR" section. Build a mapping `retro_file -> [PR numbers explicitly named]`.
2. **Inventory all PRs.** Call `mcp__github__list_pull_requests` with `state=all`, `sort=created`, `direction=asc`, `perPage=100`. If the response exceeds the tool-result size cap (typically ~50KB-100KB), parse the saved raw file out-of-band via `python3 -c "import json; data = json.load(open('<path>')); ..."`. Extract `number`, `state`, `merged_at`, `head.ref`, `base.ref`, `title`.
3. **Recognize the PR/issue namespace.** GitHub PR numbers and issue numbers share a sequence. Gaps in the PR-number stream are not missing PRs — they are issues. Do not treat them as dark zones.
4. **Compute coverage.** For each PR, determine if any retro explicitly names it. Categorize each as:
   - **Covered** — explicitly named in a retro's "Commit hashes by PR".
   - **Retro-commit-only** — the PR that landed a retrospective file (often partially-covered: the retro discusses the work but the PR itself is the retro-commit vehicle).
   - **Acknowledged** — a retro mentions the PR in passing but doesn't author its work (e.g., parallel-agent PRs the session noted but didn't write).
   - **Dark** — no retro discusses the PR at all.
5. **Identify dark zones.** Group contiguous dark PRs into zones by merge-time proximity. A zone break occurs when (a) a covered/retro-commit PR sits between two dark PRs, or (b) a > ~24 h gap separates two dark PRs (likely a session boundary).
6. **Render the coverage report inline.** Standard shape:
   - A per-retro table (file, UTC date, PRs covered, window covered).
   - A timeline view with dark zones marked as boxes, gap durations annotated.
   - A list of dark zones with PR numbers + merge-time range + brief "what it looks like" from titles.
   - Headline numbers: total PRs, covered fraction, dark count, biggest gap.

### Back-fill half (only if invoked or user confirms)

7. **Fetch PR descriptions for the zone.** Call `mcp__github__pull_request_read` with `method=get` in a single parallel block — one call per PR in the zone. The body field carries the narrative material.
8. **Determine date + sequence for the synthetic retro.** Date = `merged_at` of the LAST PR in the zone, truncated to `YYYY-MM-DD`. Sequence = `count + 1` where count is the number of existing `retrospective/YYYY-MM-DD-*.md` files for that date.
9. **Synthesize the narrative.** From the PR bodies, extract:
   - **Phase decomposition** — group PRs by topic / branch / time-proximity into named phases.
   - **Concrete numbers** — line diffs, commit counts, file counts, refutations caught.
   - **Lessons documented in the PR bodies** — anti-patterns the author called out, rule-tightenings, "we did X because we previously hit Y" reasoning.
   - **Inferred lessons** — when PR-N+1 tightens a rule, the lesson is in the gap between PR-N's intent and PR-N+1's correction. Self-reflection is reconstructable from these gradients even though PR descriptions are forward-looking.
   - **Inferred meta-observations** — was the prior retro written mid-session? Compare its commit window to the surrounding PR stream.
10. **Write the synthetic retro** following the standard `self-retrospective` structure (Commit hashes by PR / Part 1 narrative / Metrics / Part 2 skills / Part 3 agents-file / Part 4 ADRs), with two synthetic-specific additions:
    - **Metadata flag**: `**Provenance**: SYNTHETIC / BACK-FILLED. Authored YYYY-MM-DD from PR descriptions and surrounding retros; not contemporaneous with the work it covers.`
    - **Self-reflection section** at the end, narrating the lessons inferred (not just stated) from the PR gradients.
11. **Empty sibling directory is acceptable.** A synthetic retro may judge it inappropriate to author new skill specs from material it didn't witness contemporaneously. The directory exists as a layout placeholder.
12. **Commit on the current branch.** Push. Do NOT open a PR unless the user has explicitly authorized it (synthetic retros are local-history additions; the user often wants to review on disk first).

## Concrete examples

### Example 1 — audit-only (the case this skill was extracted from)

Invocation: *"What is the coverage of retrospectives in terms of pull requests? How many PRs did each retro cover, and how many are missing?"*

Workflow:

- Step 1: found 5 retros (`2026-05-11-01`, `2026-05-13-01`, `2026-05-13-02`, `2026-05-14-01`, `2026-05-14-02`).
- Step 2: `mcp__github__list_pull_requests` returned 134 KB JSON, exceeded cap; harness saved to `/root/.claude/projects/.../tool-results/mcp-github-list_pull_requests-*.txt`; parsed via `python3 -c "import json; data = json.load(open('<path>')); ..."`.
- Step 3: 37 PRs total, numbers `#1`–`#50` with gaps at `#4, #8, #23, #24, #26–31, #36, #41, #42` (all confirmed as issues by their absence from the PR list).
- Step 4: 14 PRs covered, 5 acknowledged-only (parallel-agent round-2 work), ~14 dark, 5 retro-commit-only (`#14`, `#35`, `#45`, `#47`, `#48`).
- Step 5: dark zone 1 = `#11–#25` (15 PRs over ~11.5 h on 2026-05-11); dark zone 2 = `#49, #50` (after the day's two retros on 2026-05-14).
- Step 6: rendered the per-retro table, an ASCII timeline with the two long silences marked, and the dark-zone PR lists.

Output: inline coverage report. No on-disk artifacts.

### Example 2 — back-fill (the case immediately after Example 1)

Invocation: *"create a synthetic retrospective for the first dark zone from 11 to 25. Lean heavily on the text in the pr description. ... date it as if it was done when the last pr in the sequence was merged"*

Workflow:

- Step 7: fetched 13 PR bodies in one parallel block (`mcp__github__pull_request_read method=get` for `#11, #12, #13, #14, #15, #16, #17, #18, #19, #20, #21, #22, #25`).
- Step 8: last PR in zone is `#25`, merged `2026-05-11T12:48:03Z`. Date = `2026-05-11`. Existing files for that date: `2026-05-11-01.md`. Sequence = `02`. Path = `retrospective/2026-05-11-02.md`.
- Step 9: phase decomposition surfaced 10 phases (skill extraction → cache eviction → PR #13→#14 redundancy → ADR + retro-skill → path-flatten → PR-lifecycle hardening → three PLAN.md consolidations → two manual drains → fanout-skill hardening → 26-subagent fanout). Concrete numbers extracted from bodies. Three lessons inferred from PR gradients (the PR #13 mistake was inferable because PR #16 explicitly tightened the rule against it; the Lenny video-only reclassification was inferable because PR #19's body said "confirmed by user-supplied round-2 note 'just a video.'"; the meta-lesson that retro 1 was written mid-session was inferable from comparing retro 1's coverage window to the PR stream's continued activity).
- Step 10: wrote `retrospective/2026-05-11-02.md` (323 lines) with the SYNTHETIC / BACK-FILLED flag.
- Step 11: sibling dir created but left empty — no skill specs authored from inferred material.
- Step 12: committed `f06e2f5` on `claude/analyze-retro-coverage-WDhhM`, pushed.

## Anti-patterns

- **Synthesizing without flagging.** A retro without the SYNTHETIC / BACK-FILLED metadata is indistinguishable from a contemporaneous one. Readers must be able to tell.
- **Dating the synthetic retro to authoring time instead of last-PR merge time.** Breaks chronological browsing — readers expect `retrospective/2026-05-11-NN.md` to describe work that happened on or around 2026-05-11.
- **Renumbering sequence retroactively.** Don't make the new `2026-05-11-02.md` become `2026-05-11-03.md` later just because a "more authentic" contemporaneous retro is back-filled later. Sequence numbers are append-only.
- **Treating PR-number gaps as missing PRs.** GitHub PR and issue numbers share a namespace. Confirm with the PR-list response, not the sequence.
- **Re-loading oversized MCP responses into context.** If `mcp__github__list_pull_requests` exceeds the cap, parse the saved file out-of-band — don't re-call with finer filters and accumulate dozens of partial pages.
- **Over-relying on PR descriptions for self-reflection.** PR bodies describe what was done; they rarely confess what was botched. Self-reflection is reconstructable from gradients (PR-N+1 explicitly preventing something PR-N implicitly did wrong) but it is inference, not extraction. Mark inferred lessons as such in the retro.
- **Authoring skill specs from inferred material.** A synthetic retro's sibling directory may legitimately be empty. Don't fabricate skill specs from material the synthesizer didn't witness; surface candidates in the user-facing summary but let the user trigger their authoring.
- **Synthesizing for a zone of 1–2 PRs.** Coverage is a virtue but the ROI of a synthetic retro for a 2-PR zone is low. Use audit-only or fold the brief mention into the next contemporaneous retro.
- **Opening a PR for synthetic retros without authorization.** Synthetic retros are local-history additions; the user typically wants to review on disk before they become a PR.

## Acceptance criteria

1. **Coverage is computable.** After audit, every PR in the repo's history is classified into one of: covered, acknowledged, retro-commit-only, dark. The classification can be verified by `grep`-ing the relevant retro for the PR number.
2. **Dark zones are correctly bounded.** Zones don't span across covered or acknowledged PRs; zones don't span across > ~24 h silence gaps.
3. **Synthetic retros are auditable.** Metadata block names the authoring date, the provenance ("PR descriptions and surrounding retros"), and the date of the work it covers. A reader cannot mistake a synthetic for a contemporaneous record.
4. **PR/issue namespace is handled correctly.** Numbers absent from the PR list are not flagged as missing PRs.
5. **Inline coverage report is reviewer-friendly.** Per-retro table + timeline + dark-zone list + headline numbers, all in one reply, ~1 page of rendered output.

## Files this skill creates / modifies

- `retrospective/YYYY-MM-DD-NN.md` — one per synthesized retro. NN follows the next-available-sequence rule.
- `retrospective/YYYY-MM-DD-NN/` — sibling directory per the standard retro layout. Often empty for synthetics; that is acceptable.
- No modifications to existing retros. Existing retros are read-only inputs to this skill.

## See also

- `.claude/skills/self-retrospective/SKILL.md` — the canonical retro-authoring skill. This skill's output format mirrors that skill's structure exactly, with the added SYNTHETIC / BACK-FILLED metadata flag.
- `.claude/skills/adr/SKILL.md` — for any of the proposed ADRs surfaced by the audit or synthesis that the user decides to author.
