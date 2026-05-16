# Spec: `preliminary-index-pass`

> **Status: PROMOTED** — this spec has been promoted to a live skill at `.claude/skills/preliminary-index-pass/SKILL.md` (PR opened against `main`, 2026-05-16). Future readers should treat the live SKILL.md as canonical and consult this file only for the original-session evidence base.

## Intent

When a research drop into `research/manual/` is unusually large (>20 sources, especially mixed media — `.mhtml` + `.txt` + `.pdf`), the natural reflex of `research-pipeline`'s Phase 0 is to immediately fan out subagents that drain each file into the relevant report. For a 71-file batch this collapses: the drain agent has to simultaneously decide which existing report each file belongs to, whether it's already covered, whether it warrants a new report, whether the images carry information, and how to phrase the incorporation — all while writing prose. The cognitive surface is too wide; recommendations get inconsistent across batches, and the orchestrator has no way to plan or chunk the work.

This skill inserts a **preliminary indexing pass** between "files have arrived" and "drain begins." The output is one markdown file (`research/manual/new-index.md`) containing: a one-line title for every source, its reconstructed URL, a 1–2-sentence content summary, an image-usefulness verdict (with action: keep-mhtml / convert-to-txt / delete-duplicate), a prior-processing check, and an incorporate/new-report/skip recommendation. The drain agent then reads this index, plans the actual drain in chunks, and dispatches focused subagents who each have one clear assignment instead of an open-ended triage.

The cost is one batch of ~20 parallel subagents, ~5–10 minutes of clock time, and one merged PR. The session that motivated this skill processed 71 sources in 21 batches, surfaced 13 proposed new reports, 8 primary-source upgrades, and 24 already-drained duplicates to delete — none of which would have been visible from inside a "just start draining" approach.

## Trigger

**Direct user phrases:**
- "Index these sources" / "index this batch"
- "Catalog what's in research/manual/"
- "Triage these before we drain them"
- "What's in there?" (with reference to a recently-dropped batch)

**Proactive triggers — offer the skill without being asked:**
- The orchestrator notices `research/manual/` contains >20 files that aren't all of the same kind.
- The user has just done a bulk drop (>10 files in one push or message), regardless of total count.
- The drop includes ≥5 `.mhtml` files (which require image triage anyway).

**Negative triggers — do NOT activate:**
- `research/manual/` contains ≤5 files — go straight to Phase 0 drain.
- The drop is monolingual and obviously one cluster (e.g. five chapters of the same book) — Phase 0 handles this.
- The user explicitly asks for a drain ("drain it", "process these into reports").
- The user has just asked for retrospective, ADR, or any non-research task.

## Inputs

- A populated `research/manual/` directory.
- The repo's existing reports (`research/*.md`, `research/followup/*.md`) and `research/INDEX.md` — needed for prior-processing detection.
- The MHTML extractor at `.claude/skills/research-pipeline/scripts/mhtml_extract.py`.
- Optionally: a user-supplied list of thematic motivations for the batch (themes 1..N). If absent, the skill can run without them, but they significantly improve the index's planning value.

## Outputs

- `research/manual/new-index.md` — the deliverable. One header block (themes, format spec, roll-up table), one block per source, one recommendation roll-up at the end.
- Per-source side effects:
  - Sources with no informative images: converted to `.txt` (with TITLE/URL header), `.mhtml` deleted.
  - Sources confirmed previously drained into an existing report: deleted entirely.
  - Sources with informative images (diagrams, architecture, dot-graphs, data viz): `.mhtml` kept as-is.
- A draft PR opened against `main`, ready-for-review (not draft) once verified clean.
- The skill **does NOT** modify `research/PLAN.md`, `research/INDEX.md`, or any existing report. It is index-only.

## Workflow

1. **Verify scope.** Run `ls research/manual/ | wc -l` and confirm the count justifies an index pass. If ≤5, suggest skipping straight to Phase 0 drain instead.

2. **Echo the plan to the user and wait for confirmation.** Specifically: enumerate the user's themes back to them, fix any obvious numbering bugs (e.g. duplicated indices), state file counts by extension, state the planned subagent batching, and confirm `PLAN.md` is off-limits.

3. **Pre-build a metadata manifest.** For every `.mhtml` in `research/manual/`, run `mhtml_extract.py info` to capture title / reconstructed URL / image count / image sizes / text length. Save as `research/manual/.manifest.json` (hidden). This is cheap (~30s for 60 files) and lets you batch by topical cluster, not by alphabetical accident.

4. **Write a shared subagent brief** at `research/manual/.subagent-brief.md`. Include: the user's themes (verbatim), the disposition decision tree, the image-triage heuristic (skip <30 KB / avatar/icon URLs; inspect top-3-by-size with `Read` after `save-image`; keep mhtml if ≥1 image is informationally useful), the prior-processing check recipe, and the exact output format (markdown block per file with fixed field names + final rollup line).

5. **Group sources into batches.** Aim for 2–5 files per subagent, grouped by topical cluster (e.g. all Codex/OpenAI docs in one batch, all Replit Docs in another). Heterogeneous batches blunt the subagent's ability to share prior-processing context across its files. Target 15–25 batches total for fan-out parallelism.

6. **Dispatch all subagents in one parallel message.** Each agent receives: `Read the brief at /path/.subagent-brief.md` + a tight, specific file list + 2–4 sentences of cluster-specific context hints (e.g. "These are Replit docs; report 20 may already cover them — check carefully"). Do NOT inline the brief — let the agent Read it.

7. **Collect outputs as they arrive.** Some will return synchronously; others go to background dispatch and notify later. Do not poll with `sleep` — wait for notifications.

8. **Audit the filesystem against subagent claims.** Some subagents will misreport their dispositions (e.g. claim "passthrough" for a file they actually converted). Run `ls research/manual/*.mhtml` and `ls research/manual/*.txt` and confirm the counts match. Manually delete any duplicates subagents flagged but kept (this happens in ~10% of cases).

9. **Assemble the index.** Use a single `Edit` to replace the placeholder in a pre-written header with: a rollup table, a recommendations table (proposed new reports + existing-report upgrades + existing-report extensions + deletions list), then the per-source blocks grouped by cluster.

10. **Commit, push, open a draft PR. Then promote to ready-for-review** once you've verified the file counts and the index renders sensibly.

11. **If the branch has been open across other PRs that touched `PLAN.md` or other shared files**, merge `main` in before final PR ready-for-review. Verify via `git log <merge-base>..HEAD -- <file>` that your branch hasn't touched the contested file — if empty, merge will be clean.

## Concrete examples

### Example 1: 71-source mixed batch (this session)

**Setup:** User dropped 61 `.mhtml`, 9 `.txt`, 1 `.pdf` into `research/manual/`. Articulated seven thematic motivations (after correcting a double-5 numbering bug).

**Execution:**
- Built manifest: `python3 mhtml_extract.py info` on all 61 mhtml in a loop, wrote `.manifest.json` (17 KB).
- Identified 15 topical clusters: 2389 product pages, 2389 GitHub repos, dotfile infra, Codex core docs, Codex control surfaces, OpenAI Index posts, Replit Docs ×3, Replit blog launches, Schillace ×3, Stanford CodeX ×2, Dan Shapiro, academic papers, software-factory blogs, txt batches ×3.
- Dispatched 21 subagents in one parallel message.
- 16 returned synchronously; 5 went to background, notifications arrived over ~5 min.
- Filesystem audit caught 3 duplicates flagged-but-not-deleted (Klaassen "Stop Coding", Klaassen "Teach Your AI", Shapiro "You Don't Write the Code") — manually `rm`'d.
- Assembled 864-line `new-index.md` with header + 4-row rollup table + 13-row new-reports table + 8-row primary-source-upgrade table + 15 cluster sections.

**Outputs:**
- 7 mhtml kept (informative diagrams), 34 mhtml converted to txt, 6 txt/pdf passthrough, 24 deleted as duplicates.
- 13 proposed new reports, 8 primary-source upgrades, ~10 existing-report extensions.
- PR opened draft, merged 2026-05-16.

### Example 2: 8-source small batch (hypothetical / negative example)

**Setup:** User drops 6 `.mhtml` + 2 `.txt` (8 total). All on one topic.

**Decision:** Skip this skill. 8 files is under the threshold; running an index pass adds an extra round-trip without enough value. Go straight to Phase 0 drain — the drain subagents can do their own triage in-line.

**Anti-example takeaway:** if you find yourself activating this skill for ≤10 files, you've turned an O(1) drain into an O(2) drain for no payoff.

## Anti-patterns

- **Touching `PLAN.md`, `INDEX.md`, or any existing `research/*.md` report.** This skill is index-only. All changes to existing reports happen in the subsequent drain. If you find yourself editing a report file, stop — you've crossed into Phase 0 territory and should be writing a different commit.
- **Inlining the subagent brief in each Agent call.** With 20 subagents, that wastes ~50× the tokens vs. writing the brief once on disk. Always: brief on disk + short per-agent prompt that says "Read the brief, then process [files]".
- **Polling for subagent completion with `bash sleep` loops.** The harness notifies asynchronously. A polling loop will (a) orphan its `sleep` child to init when the parent bash dies, (b) consume context budget needlessly, and (c) get explicitly flagged by the system as an anti-pattern.
- **Trusting subagent textual reports without auditing the filesystem.** ~10% of subagents will claim a disposition they didn't execute (especially: claim "skip — already covered" but leave the file in place). Always `ls` after collecting outputs.
- **Producing a free-form index.** The per-source block format must be fixed (Title / URL / Type / Themes / Summary / Image inventory / Action taken / Prior processing / Recommendation) so the downstream drain agent can mechanically parse it.
- **Forgetting to capture the user's themes verbatim.** The themes section is half the value to the next agent; paraphrasing them loses the user's framing. If the user enumerates 1..N, count and check before pasting.

## Acceptance criteria

A successful index pass produces:

1. `research/manual/new-index.md` exists, is committed, and renders cleanly on GitHub (no broken markdown, no orphaned `<!-- placeholder -->` blocks).
2. File-count math closes: `kept_mhtml + converted + passthrough + deleted == original_count` (verify in the rollup table).
3. Every per-source block has all required fields populated (no `TBD` or `?`).
4. Every "previously processed" claim is grounded in a real grep hit, citing the report number/slug. Spot-check 3 random ones.
5. The user's themes appear at the top of the index, in the order they specified, with the count they specified.

## Files this skill creates / modifies

- `research/manual/new-index.md` — created (the deliverable)
- `research/manual/.manifest.json` — created (hidden working artifact, retained for provenance)
- `research/manual/.subagent-brief.md` — created (hidden working artifact, retained for provenance)
- `research/manual/*.mhtml` — most deleted (after conversion) or deleted (duplicates); ~10% kept
- `research/manual/*.txt` — most created (from conversion); some deleted (duplicates)

**Never modified by this skill:**
- `research/PLAN.md`
- `research/INDEX.md`
- Any `research/*.md` numbered report
- Any `research/followup/*.md` report
- `.claude/skills/research-pipeline/*` (this skill is sibling to research-pipeline, not part of it)
