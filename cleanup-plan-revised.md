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
- **Session/round bullets use a strict short format.** One sentence + hyperlinks. PR hyperlinks display as `#nn`; rare commit hyperlinks display as the first 8 hex digits. Both are short link tags, not prose narrative.
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

8. **[REVISED]** Keep one bullet per run, but reformat all of them to the new style: one short sentence + PR/commit hyperlinks. Example:

   - OLD: `**Session 2026-05-17 — Round-11 manual drain (16 files; ingestion only, stage 5 deferred)** — User dropped 17 files into research/manual/ (15 MHTML + 2 PDFs); one PDF shipped with a companion URL of <name>.txt because its bytes carry no URL metadata. Used this PR to teach extract_url.py the companion-URL pattern...` (paragraph, ~150 words)
   - NEW: `**2026-05-17 Round-11 manual drain** — 16 files ingested; stage 5 deferred; PDF companion-URL plumbing added. [#93](https://github.com/lago-morph/software-factory/pull/93)`

   Hyperlink rules: PR link text = `#nn`; commit link text = `abcd1234` (first 8 hex); used only when commit message carries info not in the PR description.
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

35. **[REVISED]** Apply the concrete-task criterion:
    - **"El Kaim Medium corpus"** — requires URL harvesting first; not a concrete task → DELETE.
    - **"Noah Radford road runner economy"** — one URL, action-fetchable → move to `sources.json` as a `wanted (URL known)` record per N6 below. Delete the prose section.
    - **"platform.claude.com Agent Skills 2-of-3"** — both URLs now in catalog as `have+complete` → DELETE.
    - **"residuals (LukePM, Schillace compounding teams, 3 jaymin YouTube URLs)"** — LukePM and Schillace are drained; jaymin URLs require transcript-extraction service we don't have → DELETE all.
    - Result: the entire `## Future research` section disappears. Anything anyone wants tracked goes into `sources.json` as a wanted record.

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

#### N3. Metadata header — proposed format

44. Add a YAML frontmatter block at the top of each synthesis and architecture file:

    ```yaml
    ---
    based-on-commit: a6d6eff
    based-on-date: 2026-05-21
    ---
    ```

    Reader semantics: this synthesis (or architecture decision) is grounded in the corpus state at commit `a6d6eff`. Re-reading later, you know exactly what evidence base it sits on.

45. Apply the header to all existing files in `architectures/`: `00-comparison.md`, `01-specification-refinery.md`, `02-compound-atelier.md`, `03-phase-gated-foundry.md`, `04-evolutionary-tournament.md`. The commit-hash these are based on is whatever the most recent commit was when they were last substantively updated — best-effort backfill from git log per file.

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

50. Add `https://nraford7.github.io/road-runner-economy/` to `sources.json` as a `wanted (URL known)` record per `_catalog/edit.md` patterns. Tag with `compound-engineering` or `dark-factory` category (user pick at edit time). This is the only Future-research item that survives the concrete-task filter and isn't already in the catalog.

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
3. Delete obsolete files (C/D/E rewrite, F1).
4. Edit `research/PLAN.md` (all §1–§17 changes; bullet reformat; future-research deletion).
5. Edit `research-plan.md` (root).
6. Update research-pipeline skill resources (N4).
7. Add Noah Radford wanted record (N6).
8. Close issues #41, #42 (N5).
9. Single commit with all of the above. Run `bash scripts/lint-sources.sh` before commit.
10. Push, open PR ready-for-review, subscribe to PR activity.

---

*End of revised plan.*
