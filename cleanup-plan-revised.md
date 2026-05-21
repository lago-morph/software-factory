# Research-plan cleanup — revised plan (v2)

**Status:** WORKING DOCUMENT — committed as a backup of the planning conversation. Delete after cleanup execution merges. Not the cleanup itself; just the plan for it.

**Branch:** `claude/cleanup-research-plans-ITJUh`

---

## Style rules (apply universally)

These come from user feedback on v1 and override prior style assumptions.

- **No hardcoded counts of reports / followups / retrospectives / sources in `PLAN.md`.** Counts become stale the moment they're written. Refer to the directories or files themselves; let the reader count.
- **Source-availability tracking lives in `sources.json`, not in `PLAN.md`.** Every "wanted URL" or "outstanding source" becomes a wanted-status record in `sources.json` — never a TODO bullet in `PLAN.md`.
- **No references to retrospective follow-up anywhere.** Retrospectives are a separate process; their backlog does not belong in the research plan.
- **A task is only a task if it's a concrete, executable instruction.** "Maybe revisit X someday" is not a task. "Decide X" with a defined input and output is. Wishlist items either become sources.json wanted records (if they're sources) or are deleted.
- **Session/round bullets use the strictest possible short format.** Three components only: date + 24-hour time, the run's short name, the PR link. No prose, no semicolons-as-cheat. PR hyperlinks display as `#nn`; rare commit hyperlinks display as the first 8 hex digits. Both are short link tags, not narrative.
- **Syntheses live in `research/synthesis/`.** Both existing syntheses get moved; future ones get authored there.
- **Synthesis docs and architecture docs carry a `based-on-commit` header.** This is the only way a reader can tell what corpus state a synthesis is grounded in.

---

## Files affected

| File | Action |
|---|---|
| `/research-plan.md` (root) | Edit in place |
| `/research/PLAN.md` | Heavy edit |
| `/research/00-synthesis.md` | `git mv` to `/research/synthesis/00-synthesis.md` + add header |
| `/research/13-round-2-synthesis.md` | `git mv` to `/research/synthesis/13-round-2-synthesis.md` + add header |
| `/research/plan-sync.md` | Delete |
| `/architectures/00-comparison.md` | Add header |
| `/architectures/01-04-*.md` (4 files) | Add header each |
| `/reference-only/reorg-plan.md` | Delete |
| `/reference-only/category-survey.md` | Delete |
| `/reference-only/README.md` | Rewrite |
| `.claude/skills/research-pipeline/resources/_plan/update-discipline.md` | Update bullet format |
| `.claude/skills/research-pipeline/resources/_drain/stage-5-content-processing.md` | Add synthesis-subdir + header conventions |
| `.claude/skills/research-pipeline/SKILL.md` | Possible touch-up (decision tree row) |
| GitHub issues #41, #42 | Close with one-line comment |
| `/reference-only/sources.json` | Add Noah Radford as wanted record (only concrete future-research item) |

---

## Numbered changes

Numbering matches v1 where the change still applies; revised items are marked **[REVISED]**; new items use the **N**-prefix.

### A. `/research-plan.md` (root)

1. Update the "three-layer pipeline" inventory paragraph: don't quote report counts; describe each layer by directory name only. Note that ten rounds of material now sit between Round 2 and the present with no unified synthesis.
2. Update the failure-mode footprint description to mention that F35 sits in report 24, F40–F49 sit in reports 28/30/31/32/33/34/36/37, and the F36–F39 collision (reports 25/26) is unresolved. No counts.
3. **[REVISED]** Replace the proposed filename `research/24-final-synthesis.md` with `research/synthesis/final.md` (or whichever slug the user prefers). The slot `research/24-*` is taken (Chapter 9); syntheses now live in their own subdirectory per N1 below.
4. Update the failure-mode-catalog count language in step 1 from "F1–F34+" to "F1 through F49 plus the unresolved F36/F37 collision."
5. **[OK as-is per user]** Extend the "single specific risk" paragraph to acknowledge that Rounds 9–11 added an RE/SE-methodology thread and a governance thread that weren't on the radar when this doc was first written.

### B. `/research/PLAN.md`

#### B.1 §1 status

6. Rewrite the §1 status line as a short status statement: rounds 1–12 complete (reference §10 for detail), what's left is the §3 / §5 items and the `research-plan.md` decision. No counts, no retrospective references, no fetch-loop history.
7. Delete the entire "Earlier versions" paragraph (line 6). It's a 17-version changelog with no operational value; the git log holds version provenance.

#### B.2 §1 done-bullet list

8. **[REVISED — v3]** Keep one bullet per run, in the strictest possible form. Three components only: date + time (24-hour), the run's short name, the PR link. **No prose sentences. No semicolons-as-cheat. No content summary.** Example:

   - OLD: `**Session 2026-05-17 — Round-11 manual drain (16 files; ingestion only, stage 5 deferred)** — User dropped 17 files into research/manual/ (15 MHTML + 2 PDFs); one PDF shipped with a companion URL of <name>.txt because its bytes carry no URL metadata. Used this PR to teach extract_url.py the companion-URL pattern...` (~150 words)
   - NEW: `**2026-05-17 18:42 Round-11 manual drain** [#93](https://github.com/lago-morph/software-factory/pull/93)`

   The bullet says when it happened, what it was, and where to read about it. Anyone who needs the content reads the PR. Hyperlink rules: PR link display = `#nn`; rare commit link display = `abcd1234` (first 8 hex), used only when the commit message carries info not in the PR description. Time comes from the merge-commit timestamp.
9. Add a bullet for Round 12 (gas-systems substrate analysis, [#101](https://github.com/lago-morph/software-factory/pull/101)) — the round itself isn't in PLAN.md yet because v0.17 predates it.
10. Update the "Open items live in" sub-list at the end of §1 to reference only the live sections that survive cleanup (§3, §5, §6.1, and `research-plan.md`).

#### B.3 §2 Repository layout

11. **[REVISED]** Remove all counts (e.g., "37 numbered reports + 12 followup reports", "22 retrospectives"). Describe each directory's purpose; let the reader count.
12. **[REVISED]** Same: remove the count of installed skills (line 85) — describe the directory's purpose instead.
13. Remove the `/docs/adr/` parenthetical pointing at §3.4 (which is being deleted).
14. Remove the `plan-sync.md` line (file deleted per F1 below).
15. Update the `/research/` description to mention the new `synthesis/` subdirectory (per N1).

#### B.4 §3 Bottlenecks

16. Delete §3.1 (RESOLVED with strikethrough).
17. Keep §3.2 (real curated-human-review backlog with concrete tasks).
18. Delete §3.3 (RESOLVED with strikethrough). Cross-corpus lessons R7.1/R7.3/R8.1/R8.3/R8.4/R8.5 either move into research-pipeline skill resource docs (if still load-bearing) or are deleted.
19. Delete §3.4 (retrospective decisions — per user, no retro content in PLAN).
20. Delete §3.5 (RESOLVED).
21. Keep §3.6 (F36/F37 collision triage — concrete suggested mapping exists, just needs decision). Condense the long "Structural constraint added by Round-10" paragraph into one sentence.
22. **[deleted — see below]**

#### B.5 §4 Manual fetch instructions

23. **[REVISED]** Delete §4 in its entirety. Source-availability tracking moves to `sources.json` via wanted-status records. Operational procedures (Path A/B/C, fetch-blocked-urls workflow) live in the research-pipeline + fetch-blocked-urls skills. **Includes**: §4.1 (no outstanding), §4.2 (Lenny YouTube — done), §4.3 (Path-B-only / retry-eligible table — `platform.claude.com` URLs are already in catalog as `have+complete`; the `docs.github.com/.../risks-and-mitigations` URL returns 404 per user — drop entirely), §4.4 (not-worth-fetching).

#### B.6 §5 Work remaining

24. **[REVISED]** Rewrite §5.0 "Definition of research phase complete" as a concrete-tasks-only checklist:
    - Item: Cross-corpus propagation sweep complete (§6.1)
    - Item: §3.2 curated-human-review backlog resolved one way or the other (Update or won't fix)
    - Item: Either a unified synthesis exists or the user explicitly decided not to write one (per `research-plan.md`)
    - Item: F36/F37 numbering collision triaged (§3.6)
    - **Delete** the old items 1–5 (DONE; the documents themselves are the proof) and item 7's retrospective half.
25. Delete the original work-remaining items 1, 2 (both DONE with strikethrough), and the retrospective-decisions item (line 260). Renumber what remains.
26. **[REVISED]** §5 list shrinks to: (a) decide on `research-plan.md` direction, (b) §3.2 curated tasks, (c) cross-corpus sweep (§6.1), (d) F36/F37 triage (§3.6). No "optional fetches" item — that's sources.json's job now.

#### B.7 §6 Resumption checklist

27. Update §6 resumption checklist (lines 270–277) — remove references to closed issues (#29/#30/#31/#36/#41/#42) and to `research/fetched/` (no longer exists).
28. Keep §6.1 cross-corpus propagation flags. Drop the R8.4 paragraph (it's pipeline operational knowledge — propagate to the research-pipeline skill instead). Drop the closing "not picked up in this session because…" paragraph.
29. **[REVISED]** Rewrite §6.2 in-flight tracking table — keep only non-source items:
    - `research-plan.md` direction (decision pending)
    - §3.2 curated tasks
    - §6.1 cross-corpus sweep
    - §3.6 F36/F37 collision
    - **Delete** all rows about specific URLs, retrospective backlog, `plan-sync.md`, issues #41/#42. Source tracking → `sources.json`; the rest is gone.

#### B.8 §7 Fetch-loop tooling

30. Delete §7 in its entirety (the bridge file `plan-sync.md` is being deleted per F1; the section becomes a pointer to nothing).

#### B.9 §10 lookup table

31. Add a Round-12 row: `| 12 | Round-12 gas-systems substrate analysis | ✅ Complete | Reports 38 + followups 13 + 14. [#101](https://github.com/lago-morph/software-factory/pull/101) |`
32. **[REVISED]** Rewrite every existing row to the new compact format: one sentence + PR/commit hyperlinks. No prose summaries of contents — those live in the reports themselves.

#### B.10 §11–§17 archive

33. **[REVISED]** §11–§16 (Rounds 1–6 dispatch detail) — collapse each into a one-sentence summary + PR/commit hyperlinks, then merge into the corresponding §10 row. Delete the §11–§16 sections entirely. §10 becomes the single source of truth for "what each round produced."
34. Delete §17 (version history) entirely. The git log is the version history.

#### B.11 Future research

35. **[REVISED — v4]** Apply the concrete-task criterion:
    - **"El Kaim Medium corpus"** — requires URL harvesting first; not a concrete task → DELETE.
    - **"Noah Radford road runner economy"** — one URL, action-fetchable → move to `sources.json` as a `wanted (URL known)` record per N6 below. Delete the prose section.
    - **"platform.claude.com Agent Skills 2-of-3"** — both URLs now in catalog as `have+complete` → DELETE.
    - **"residuals — LukePM, Schillace compounding teams"** — both drained → DELETE.
    - **"residuals — 3 jaymin YouTube URLs (K7nY3MUzDuk / njRAmppPvFk / 95TEFWdo6Mw)"** — **KEEP on plan** per user recollection of having provided transcripts (likely on their laptop). **Added to `sources.json` in this same commit** as three `youtube-transcript` wanted entries on the embedding record `992e4f88b6` (Jaymin West "Agentic Engineering Book") per the convention in `_drain/youtube-transcripts.md` — `format: youtube-transcript`, `ingestion_status: want`, `filename: null`, `youtube_url` set to canonical form. When the user drops the `.txt` transcripts into `research/manual/`, the drain pipeline will auto-promote them to `have`. The PLAN.md task description: "User believes the three jaymin YouTube transcripts are on their laptop — find and drop into `research/manual/`, or confirm not-present and mark `skip-not-necessary`."
    - Result: the `## Future research` section disappears. All wanted-source tracking is now in `sources.json`; the jaymin-transcript-locate task lives in PLAN.md §5 because the action (search the user's laptop) sits with the user, not with the catalog pipeline.

### C. `/reference-only/reorg-plan.md`

36. Delete the file. Step 1 was superseded by PR #80; Step 2 never started; the terminal-step skill was eclipsed by `research-pipeline`. Lessons-learned content is already absorbed into the live skill.

### D. `/reference-only/category-survey.md`

37. Delete the file. It was a Step-1.0 input to the now-deleted reorg-plan; its corpus-shape estimate is absorbed into the category taxonomy that ships in `.claude/skills/research-pipeline/resources/_catalog/category-taxonomy.md`.

### E. `/reference-only/README.md`

38. Rewrite to match current reality. Replace the 15-category-subdirectory description with: this directory holds the source catalog; canonical data is `sources.json`; browse view is `sources.md`; per-source files live in `<id>/` subdirs where `id = sha256(canonical_url)[:10]`; see `.claude/skills/research-pipeline/SKILL.md` for editing procedures. Keep the "What does NOT belong here" section and the `MIGRATION-EXCEPTIONS.md` cross-reference.

### F. `/research/plan-sync.md`

39. Delete the file. Always intended as disposable; PLAN.md v0.13 finished the fold-in; the historical files it preserves remain in git history.

### N. New tasks added by user feedback

#### N1. Move syntheses to `research/synthesis/`

40. `git mv research/00-synthesis.md research/synthesis/00-synthesis.md`
41. `git mv research/13-round-2-synthesis.md research/synthesis/13-round-2-synthesis.md`
42. Add the metadata header (see N3) to each file in the new location.

#### N2. Filename question — kept or renamed?

43. Filenames as moved keep their existing prefixes (`00-`, `13-`). Future syntheses get whichever number is appropriate (e.g., `39-final-synthesis.md` or simply `final.md` — user preference; I'll default to the numbered scheme for consistency with the rest of `/research/`).

#### N3. Metadata header — proposed format, with historical commits per file

44. Add a YAML frontmatter block at the top of each synthesis and architecture file:

    ```yaml
    ---
    based-on-commit: f480c8b
    based-on-date: 2026-05-13
    ---
    ```

    Reader semantics: this synthesis (or architecture decision) is grounded in the corpus state at commit `f480c8b`. Re-reading later, you know exactly what evidence base it sits on. **The commit hash + date are historical — they record when the file was last substantively edited, not when the header was added.**

45. **[REVISED — v3]** Specific historical commit + date for each file, established from `git log <parent-ref> -- <file>` walks across the visible-history boundary:

    | File | based-on-commit | based-on-date | Source commit message |
    |------|------|------|------|
    | `research/00-synthesis.md` | `f480c8b` | 2026-05-13 | "Reversal-of-reversal + cross-corpus updates + move sources to reference-only" |
    | `research/13-round-2-synthesis.md` | `8f737b3` | 2026-05-13 | "Editorial collapse: fold 09-partial Substack manifesto into report 09; delete partial" |
    | `architectures/00-comparison.md` | `c495dc9` | 2026-05-10 | "v2: update synthesis, blocked-URLs, architectures, and comparison" |
    | `architectures/01-specification-refinery.md` | `c495dc9` | 2026-05-10 | (same) |
    | `architectures/02-compound-atelier.md` | `c495dc9` | 2026-05-10 | (same) |
    | `architectures/03-phase-gated-foundry.md` | `c495dc9` | 2026-05-10 | (same) |
    | `architectures/04-evolutionary-tournament.md` | `c495dc9` | 2026-05-10 | (same) |

    Note: the visible history in the current repo starts at the PR #48 merge commit `42ed807` (2026-05-13), but the parent commits accessible by hash extend further back. The hashes above are from the pre-squash history; they're stable references even though `git log --all` doesn't surface them.

#### N4. Update research-pipeline skill

46. Edit `.claude/skills/research-pipeline/resources/_drain/stage-5-content-processing.md` to encode:
    - synthesis docs live in `research/synthesis/`
    - synthesis docs carry the `based-on-commit` YAML frontmatter
    - same header convention applies to `architectures/*.md` (cross-reference only; the skill doesn't own that directory)

47. Edit `.claude/skills/research-pipeline/resources/_plan/update-discipline.md` to:
    - change the Session-bullet template to the new short format (one sentence + `#nn` PR hyperlink, rare `abcd1234` commit hyperlink)
    - drop the "minimum-footprint vs more-than-minimum" tier complexity; one format applies always
    - drop the Version-bump and Earlier-versions-paragraph rules (those die with the cleanup)

48. Touch up `.claude/skills/research-pipeline/SKILL.md` decision tree if any row needs to point at the new synthesis convention.

#### N5. Close GitHub issues #41 and #42

49. Post a one-line comment on each: `Closed by [#44](https://github.com/lago-morph/software-factory/pull/44).` then close. Removes the phantom from GitHub state. Don't reference in PLAN.md.

#### N6. Add Noah Radford as a wanted source

50. Add `https://nraford7.github.io/road-runner-economy/` to `sources.json` as a `wanted (URL known)` record per `_catalog/edit.md` patterns. Tag with `compound-engineering` or `dark-factory` category (user pick at edit time). This is the only **wanted-source** future-research item that survives the concrete-task filter as a new catalog record.

51. **[ADDED v4 — already executed in the current branch's HEAD commit]** Three jaymin YouTube URLs added as `youtube-transcript` wanted entries on the Jaymin West Agentic Engineering Book record `992e4f88b6`. Canonical YouTube URLs:
    - `https://www.youtube.com/watch?v=K7nY3MUzDuk` (The Agentic Engineering Meta)
    - `https://www.youtube.com/watch?v=njRAmppPvFk` (Six Levels of Agentic Engineering)
    - `https://www.youtube.com/watch?v=95TEFWdo6Mw` (I'm Open Sourcing The Cutting Edge)
    Schema-validated (209 records valid). When user drops `.txt` transcript files with the canonical URL on the first line into `research/manual/` (or the record's `<id>/` dir), drain auto-promotes them to `have`.

---

## L. Linter findings — separate work item (deferred from this cleanup)

`bash scripts/lint-sources.sh` currently exits non-zero. Schema validation passes (209 records valid); the lint failure is concentrated in the URL-vs-reports cross-check plus a stack of advisory sanity warnings. Captured here so a future agent has the full context + a concrete fix path without re-running diagnostic loops.

### L.1 URL-vs-reports — 5 errors (the only hard FAIL)

**Context.** Round-12 (gas-systems substrate analysis, PR #101, 2026-05-20) added `research/38-gas-systems-substrate.md` + `research/followup/13-gas-city-deep-dive.md` + `research/followup/14-gas-town-deep-dive.md` without running the catalog drain afterward. As a result the reports cite URLs that have no record in `sources.json`:

| # | URL | Cited in | Substantive? |
|---|------|------|------|
| 1 | `http://localhost:8428/api/v1/write` | followup/14 | No — Gas Town config example reference |
| 2 | `http://localhost:9428/insert/jsonline` | followup/14 | No — same |
| 3 | `https://github.com/gastownhall/gascity` | report 38 + followup/13 | **Yes** — primary repo subagent walked |
| 4 | `https://github.com/gastownhall/gascity/issues/586` | followup/13 | **Yes** — specific issue cited |
| 5 | `https://github.com/gastownhall/gastown` | report 38 + followup/14 | **Yes** — primary repo subagent walked |

**Proposed solution.**
- **Localhost URLs (1, 2):** Add to `reference-only/MIGRATION-EXCEPTIONS.md` under a new "casual host: localhost (2 records)" section. These are config-illustration URLs inside source code samples, not substantive external sources — same handling as `api.github.com`, `x.com` etc. (See existing MIGRATION-EXCEPTIONS.md for the exact format.)
- **GitHub repo + issue URLs (3, 4, 5):** Create three proper catalog records. Use the standard URL → id → record flow per `_catalog/edit.md` Case 1 (no files — `wanted` status). Tag with category `other-vendor-substrate` (or `dark-factory` — the user picks at edit time). The repos *were* walked by Round-12 subagents but the working clones lived in ephemeral `/tmp/` and weren't preserved; mark `ingestion_status: want` for now. If the user wants the repos re-cloned and the worktrees persisted, that's a separate ingestion task (likely needs `git clone --depth 1` + a custom file-naming convention because the catalog isn't designed to hold full git checkouts).
- **Also update `references_from`** on all five new/excepted records: run `python .claude/skills/research-pipeline/scripts/check-source-refs.py --fix` after the records exist, which back-populates the array from the actual report citations.

### L.2 references_from drift on `e588b9bb1a` — 1 warning

**Context.** Record `e588b9bb1a` is the superseded CaMeL arXiv record (`pointer_to → 24ca29ee98`). `research/followup/08-security-primitives.md` cites the old URL but `references_from` on `e588b9bb1a` wasn't updated when the citation pattern changed.

**Proposed solution.** `python .claude/skills/research-pipeline/scripts/check-source-refs.py --fix` will repopulate `references_from`. Single-record fix; takes seconds.

### L.3 Filesystem ↔ catalog — 4 stray-file warnings

| Stray | Disposition |
|------|------|
| `reference-only/MIGRATION-EXCEPTIONS.md` | **Keep** — accurate audit trail; expected stray. The linter has no concept of "intentional top-level docs"; either suppress this specific warning or accept it permanently. |
| `reference-only/category-survey.md` | **Delete** — this cleanup already proposes deleting it (item 37). The warning disappears after the cleanup PR lands. |
| `reference-only/reorg-plan.md` | **Delete** — this cleanup already proposes deleting it (item 36). The warning disappears after the cleanup PR lands. |
| `reference-only/f3b49991be/` (orphan directory, no record) | **Delete** — Investigated in this session: the dir contains `software-factory-deep-research-report.md` (a `git ls-tree` dump, not actual report content — likely an accidental shell-redirect commit) and `software-factory-deep-research-report-sources.md` (a Cloudflare "Just a moment…" interstitial captured by mistake). Neither file has substantive content; the directory's id `f3b49991be` doesn't match any current canonical URL. **Action:** `git rm -r reference-only/f3b49991be/` as part of the cleanup commit. |

### L.4 Sanity warnings — 65 advisory items

**Context.** Title / word-overlap heuristic warnings. Three distinct sub-categories:

1. **"Just a moment…" / "404 / Not Found" / "Search code, repositories…" titled files (~15 warnings).** Files where the captured page is actually a Cloudflare challenge, an interstitial, or a search-results page — not the intended content. **Examples:** records `60fbea1689`, `7dbf96d872`, `e6f77b9e81` (Cloudflare on Medium / Substack), `5a9f63821f` (404 on platform.claude.com `security` page HTML), `3274cc670c` (Cognition 404), `85cdf07ac2` (8090 blog 404), `2e49bcd671` (saved dotpowers page instead of Copilot doc), `a5209cf735` (GitHub search), `1e18da4d24` (`report.md` title mismatch — the file is the legit content but its `title` metadata doesn't reflect the canonical record title).
2. **Host normalization warnings (~5 warnings).** File's URL host is `cognition.ai` but the record's canonical URL is `www.cognition.ai` (and similar for `factory.ai` / `www.factory.ai`, `jayminwest.com` / `www.jayminwest.com`, `docs.openhands.dev` / `docs.all-hands.dev`). Either canonicalize the file's recorded host on ingestion, or relax the audit to treat `www.X` and `X` as the same host.
3. **Format-variant low-overlap (~45 warnings).** HTML + MD + MHTML files for the same source naturally have <30% token overlap because HTML carries navigation chrome and MD doesn't. Most of these are false positives — the threshold is set too tight for multi-format records. Examples: `5cc5a296b6` (Replit Agent 3 HTML+MHTML 11%), `9c9554d27e` (lethal-trifecta HTML+MHTML 13%), `f8007cc630` (Lenny + transcripts).

**Proposed solution — process in three passes, ordered by leverage:**
- **Pass 1 (high-leverage, ~15 records):** Re-fetch the broken-content files via the `fetch-blocked-urls` action runner (Cloudflare-blocked records often work from GitHub Actions IP), OR mark them `completeness: error` and `ingestion_status: skip-not-necessary` if the canonical content lives in another file on the same record. The fetch-blocked-urls skill has the workflow.
- **Pass 2 (low-leverage, ~5 records):** Normalize `host` handling — either in the records or in the audit. Cheapest fix is to teach the audit that bare-host and `www.host` are equivalent. Edit `.claude/skills/research-pipeline/scripts/audit-records.py` (the host-comparison check) to call `url_canonicalize.py`'s host-normalization helper before comparing.
- **Pass 3 (no-leverage, ~45 records):** Loosen the multi-format word-overlap threshold from "warn at <30%" to "warn at <10%" — `audit-records.py` constant. The 11–25% range for HTML+MD+MHTML pairs is normal and produces only noise.

The whole set is processable in ~1 hour by a focused subagent once the criterion calls are made.

### L.5 PLAN.md consistency — 2 warnings (advisory only)

**Context.** `check-plan-consistency.py` reports that 8 of the last 10 catalog-touching commits didn't also touch PLAN.md, including auto-regen commits (`auto: regenerate sources.md from sources.json`) which are mechanical, and merge commits.

**Proposed solution.** Either (a) suppress the warning class for `auto:`-prefixed commits and merge commits in `check-plan-consistency.py`, or (b) accept the noise (it's advisory; lint exits 0 on it). The cleanup PR will reset the window — once PLAN.md is rewritten as part of the cleanup, the next 10 commits land with PLAN.md updates per Hard rule #10, and the warning self-resolves until skill drift recurs.

### L.6 Config validation — 1 warning

`research/fetched/` (in `ingestion_paths` config) doesn't exist on disk. **Proposed solution:** remove `research/fetched/` from the pipeline config YAML in `SKILL.md`, since the fetch-blocked-urls workflow now writes to a `fetched/issue-N/` branch (not a top-level dir) and drain consumes from that branch directly. Single-line edit.

---

### Summary of L items by execution cost

| Item | Type | Effort | Blocking? |
|------|------|------|------|
| L.1 (5 URL errors) | Catalog edits | ~20 min | **Yes — this is what makes lint exit non-zero** |
| L.2 (1 references_from) | Script run | 30 sec | No (advisory warning) |
| L.3 (4 stray files) | Already covered by main cleanup | 0 min extra | No |
| L.4 (65 sanity warnings) | Re-fetch + audit tuning | ~1 hour subagent | No (advisory) |
| L.5 (PLAN.md consistency) | Script tweak | 5 min | No (advisory) |
| L.6 (config warning) | One-line config edit | 1 min | No |

**Recommendation:** Address L.1 in the same cleanup commit (it's the only one that flips lint from FAIL to PASS), L.3 already lands with the main cleanup, L.6 alongside the SKILL.md updates per N4, and L.2 as a one-liner. Defer L.4 + L.5 to a follow-up PR — they're noise, not correctness, and they don't gate anything.

---

## Out of scope (flagged but not in this cleanup)

- **Architectures §2.4 / §7 swap, `spec-driven-ai-dev.md` extension, Round-2 stanza** — the three §3.2 tasks. They remain pending in §3.2 after cleanup; this PR doesn't execute them.
- **F36/F37 triage decision** — surfaced in §3.6; needs user/lead decision; this PR doesn't make it.
- **Cross-corpus propagation sweep (§6.1)** — surfaced; this PR doesn't run the grep + subagent dispatch.
- **Unified-synthesis vs four-architectures decision** — the central `research-plan.md` decision; this PR doesn't make it.

---

## Execution order (when user approves)

1. Move syntheses (N1) and add headers (N3).
2. Add architecture headers (N3).
3. Delete obsolete files (C/D/E rewrite, F1, L.3 orphan dir).
4. Edit `research/PLAN.md` (all §1–§17 changes; bullet reformat; future-research deletion).
5. Edit `research-plan.md` (root).
6. Update research-pipeline skill resources (N4 + L.6 config).
7. Add Noah Radford wanted record (N6).
8. Address L.1 — add MIGRATION-EXCEPTIONS entries (localhost URLs) + 3 catalog records (gas-systems repos + issue).
9. Run `python .claude/skills/research-pipeline/scripts/check-source-refs.py --fix` (L.2).
10. Close issues #41, #42 (N5).
11. Single commit with all of the above. Run `bash scripts/lint-sources.sh` and confirm it exits clean (only L.4/L.5 advisory warnings remain, both deferred).
12. Push, open PR ready-for-review, subscribe to PR activity.

---

*End of revised plan.*
