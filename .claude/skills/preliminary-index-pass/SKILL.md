---
name: preliminary-index-pass
description: Triage a large drop of mixed-media research sources in `research/manual/` BEFORE they go through a full drain. Produces `research/manual/new-index.md` cataloging every source with title, reconstructed URL, summary, image-usefulness verdict, prior-processing check, and incorporate/new-report/skip recommendation — so the subsequent drain agent has a planned, chunked attack rather than open-ended triage. Use whenever `research/manual/` (or any incoming-sources directory) contains more than ~20 files, the drop is mixed-media (`.mhtml` + `.txt` + `.pdf`), or the user says "index these", "catalog what's in here", "triage these before we drain them", or "what's in there?" with reference to a recent bulk drop. Distinct from `research-pipeline` Phase 0, which is a drain — this skill is index-only and intentionally does NOT modify `research/PLAN.md`, `research/INDEX.md`, or any existing report.
---

# Skill: preliminary-index-pass

Insert a planning step between "files have arrived" and "drain begins." When a manual-drop batch is small (≤5 files), the drain agent can triage in-line and skip this skill. When the batch is large (>20 files), in-line triage collapses: the drain agent has to simultaneously decide which existing report each file belongs to, whether it's already covered, whether it warrants a new report, whether the embedded images carry information, and how to phrase the incorporation — all while writing prose. The cognitive surface is too wide; recommendations get inconsistent across batches and the orchestrator has no way to chunk the work.

This skill produces a single planning artifact — `research/manual/new-index.md` — that turns the unstructured pile into a structured plan. The subsequent drain agent then reads the index, picks chunks, and dispatches focused subagents who each have one clear assignment.

## When to invoke

**Direct user phrases:**

- "Index these sources" / "index this batch"
- "Catalog what's in `research/manual/`"
- "Triage these before we drain them"
- "What's in there?" (with reference to a recently-dropped batch)
- "Preliminary index pass" / "preliminary pass"

**Proactive triggers — activate without being asked:**

- `research/manual/` (or the project's equivalent incoming-sources directory) contains more than 20 files that are not all of the same kind.
- The user has just done a bulk drop (>10 files in one push or message), regardless of total count.
- The drop includes ≥5 `.mhtml` files (which require image triage anyway, where this skill's image discipline shines).

**Negative triggers — do NOT activate:**

- `research/manual/` contains ≤5 files — go straight to `research-pipeline` Phase 0 drain.
- The drop is monolingual and obviously one cluster (e.g. five chapters of the same book) — Phase 0 handles this.
- The user explicitly asks for a drain ("drain it", "process these into reports", "fold these in"). That is `research-pipeline`'s job, not this skill's.
- The user has asked for retrospective, ADR, or any non-research task.

## Inputs

- A populated `research/manual/` directory (or whichever directory the project uses for incoming sources).
- The repo's existing reports (`research/*.md`, `research/followup/*.md`) and `research/INDEX.md` — needed for prior-processing detection.
- The MHTML extractor at `.claude/skills/research-pipeline/scripts/mhtml_extract.py` (commands: `info`, `text`, `save-image`, `to-txt`).
- Optionally: a user-supplied list of thematic motivations for the batch ("themes 1..N"). If absent, the skill can run without them, but they significantly improve the index's planning value.

## Outputs

- **`research/manual/new-index.md`** — the deliverable. Contains a themes block (if the user supplied themes), a rollup table, a recommendations table, and one structured block per source.
- **Per-source side effects:**
  - Sources with **no informative images**: converted to `.txt` via `mhtml_extract.py to-txt`, original `.mhtml` deleted.
  - Sources confirmed **previously drained** into an existing report: deleted entirely.
  - Sources with **informative images** (diagrams, architecture, dot-graphs, data visualizations, code-with-substantive-content): `.mhtml` kept as-is so the next drain sees the visuals.
  - `.txt` and `.pdf` sources: passthrough (no conversion), but still indexed and still subject to the previously-processed deletion rule.
- A **draft PR** opened against `main`, promoted to ready-for-review once the file count math closes.
- The skill **never** modifies `research/PLAN.md`, `research/INDEX.md`, or any existing `research/*.md` / `research/followup/*.md` report. It is index-only.

## Workflow

### 1. Verify scope and the user's framing

Run `ls research/manual/ | wc -l` and confirm the count justifies an index pass. If ≤5, suggest skipping straight to `research-pipeline` Phase 0 drain instead.

If the user enumerated themes in their prompt, **count the items before paraphrasing**. Off-by-one numbering errors are common (duplicated indices, stated count disagreeing with actual count). Surface any discrepancy back to the user as a clarification, then proceed with the corrected numbering. Echo the themes verbatim — paraphrasing loses the user's framing.

Before dispatching anything, summarize the plan back to the user (file counts by extension, planned subagent batching, explicit confirmation that `PLAN.md` is off-limits) and wait for a go signal if there's any ambiguity.

### 2. Pre-build a metadata manifest

For every `.mhtml` in the incoming directory, run `mhtml_extract.py info` to capture title / reconstructed URL / image count / per-image sizes and URLs / text length. Save the aggregate as `research/manual/.manifest.json` (hidden, retained for provenance).

```python
import json, subprocess
from pathlib import Path

manual = Path("research/manual")
out = []
for f in sorted(manual.iterdir()):
    if not f.name.endswith(".mhtml"):
        continue
    r = subprocess.run(
        ["python3", ".claude/skills/research-pipeline/scripts/mhtml_extract.py", "info", str(f)],
        capture_output=True, text=True, timeout=60,
    )
    d = json.loads(r.stdout)
    out.append({
        "file": f.name,
        "title": d.get("title"),
        "url": d.get("snapshot_url") or d.get("main_url"),
        "n_images": d.get("n_images", 0),
        "text_len": d.get("text_len", 0),
        "size_bytes": f.stat().st_size,
    })
Path("research/manual/.manifest.json").write_text(json.dumps(out, indent=2))
```

This is cheap (~30s for 60 files) and lets you batch by topical cluster, not by alphabetical accident.

### 3. Write a shared subagent brief on disk

Path: `research/manual/.subagent-brief.md` (hidden, retained for provenance). The brief contains:

- The user's themes (verbatim).
- The disposition decision tree (kept-mhtml / converted-to-txt / deleted-as-duplicate / passthrough).
- The image-triage heuristic (see step 5).
- The prior-processing check recipe (grep title fragment and URL against `research/*.md research/followup/*.md`).
- The exact per-file output format (markdown block with fixed field names + final rollup line).
- Anti-patterns (don't Read mhtml directly; don't modify PLAN.md / INDEX.md / any existing report).

Writing the brief once on disk and having all subagents `Read` it (rather than inlining instructions into each Agent prompt) saves roughly N× the brief's token count and ensures uniform instructions across the cohort. See `.claude/skills/parallel-subagent-fanout/SKILL.md` for the broader fan-out pattern this builds on.

### 4. Group sources into batches

Target 2–5 files per subagent, grouped by **topical cluster** (e.g. all Codex/OpenAI docs in one batch, all Replit Docs in another, all Sam Schillace posts in a third). Heterogeneous batches blunt the subagent's ability to share prior-processing context across its files. Aim for 15–25 batches total — enough parallelism to finish in one round, few enough that any single batch is digestible.

The pre-built manifest is the input to this step: sort by URL hostname, then by URL path prefix, then by title-token clustering, and bucket adjacent groups of 2–5.

### 5. Dispatch all subagents in one parallel message

Each Agent invocation receives:

- An instruction to `Read` the shared brief at `research/manual/.subagent-brief.md`.
- A tight, specific file list (just filenames, one per line).
- 2–4 sentences of cluster-specific context hints ("These are Replit docs; report 20 may already cover them — check carefully and skip duplicates", or "These are Stanford CodeX policy posts; none of them are in the existing corpus, treat as new").

Use `subagent_type: general-purpose` for these (they need filesystem write access to delete and convert). Do NOT inline the brief — let the agent `Read` it. Do NOT poll for completion with bash `sleep` loops — the harness will notify you when each subagent finishes.

**Image-triage heuristic** (subagent brief embeds this):

- **Skip** images where size < 30 000 bytes, OR URL/path contains `avatar`/`profile`/`logo`/`icon`/`favicon`/`emoji`/`sprite`/`og-image`/`gravatar`/`social`, OR content-type is `image/svg+xml` and size < 100 KB (decorative SVG).
- Among the remainder, pick the **top 3 largest** by size. Save each to `/tmp/<basename>_img<idx>.png` via `mhtml_extract.py save-image`, then `Read` to inspect.
- **Useful**: diagrams, architecture, flowcharts, tables of data, eval graphs, dot-graph renders, code-on-screen with substantive content.
- **Not useful**: headshots, author photos, generic stock photos, UI screenshots that just show product chrome, decorative illustrations, social-share cards.
- If at least one image is useful → **keep** the `.mhtml`. Otherwise → `mhtml_extract.py to-txt` and `rm` the `.mhtml`.

### 6. Collect outputs as they arrive

Some subagents return synchronously, others go to background dispatch and notify later via `<task-notification>` events. **Wait passively** — do not poll. Each completion notification carries the subagent's full markdown stream as its result.

### 7. Audit the filesystem against subagent claims

This step catches the ~10% of subagents that misreport their dispositions (claim "skip — already covered" but leave the file in place; claim "passthrough" for a file they actually converted from mhtml). After all subagents have returned:

```bash
ls research/manual/*.mhtml 2>/dev/null | wc -l  # remaining mhtml
ls research/manual/*.txt 2>/dev/null | wc -l    # txt (originals + conversions)
```

Cross-check the counts against the subagent rollups. For every "skip — already covered" claim, verify the file is actually gone; if not, `rm` it manually. For every "converted to TXT" claim, verify the .txt exists and the .mhtml is gone.

### 8. Assemble `new-index.md`

Header block (in order):

1. Title + a one-paragraph "what this is" framing.
2. **Themes section** if the user supplied themes — each as an H3 with the user's wording plus a 1–2-sentence paraphrase that names *why* the theme matters for the factory. Themes are the most valuable content for the next agent's planning.
3. **How to read each per-source block** — explain the field names and disposition vocabulary.
4. **Rollup tables**:
   - Disposition rollup (kept-mhtml / converted-to-txt / deleted-as-duplicate / passthrough counts).
   - Proposed new reports (with one-line angle each).
   - Existing-report primary-source upgrades (cite the report number).
   - Existing-report extensions (cite the report number and which section).
   - Already-covered deletions (cite which report drained it).
5. **Per-source blocks**, grouped by cluster, each using the brief's fixed format.

### 9. Commit, push, open a draft PR

Commit on a feature branch (per `always-commit-skill-to-repo` conventions). Push. Open the PR as a **draft** — promote it to ready-for-review only after step 10.

### 10. If the branch lingers, merge `main` in before final review

If the branch has been open across other PRs that touched shared files like `PLAN.md` or `INDEX.md`, merge `origin/main` into your branch before flipping the PR ready-for-review. Verify innocence via:

```bash
git log $(git merge-base HEAD origin/main)..HEAD -- research/PLAN.md
```

If the output is empty, your branch never modified `PLAN.md` and the merge will take `main`'s version cleanly — no conflict. Push the merge commit before promoting the PR.

## Concrete examples

### Example 1: 71-source mixed batch (real, PR #61, 2026-05-16)

**Setup:** User dropped 61 `.mhtml` + 9 `.txt` + 1 `.pdf` into `research/manual/`. Articulated seven thematic motivations (after correcting a double-5 numbering bug in the user's original prose; counting them caught the off-by-one).

**Execution:**

1. Built manifest: ran `mhtml_extract.py info` on all 61 `.mhtml` in a Python loop, wrote `.manifest.json` (17 KB, ~30 seconds).
2. Identified 15 topical clusters by sorting manifest entries by URL hostname + path prefix (2389 product pages, 2389 GitHub repos, dotfile infra, Codex core docs, Codex control surfaces, OpenAI Index posts, Replit Docs ×3, Replit blog launches, Schillace ×3, Stanford CodeX ×2, Dan Shapiro blog, academic papers, software-factory blogs, txt batches ×3).
3. Wrote shared brief (~100 lines) at `research/manual/.subagent-brief.md`.
4. Dispatched 21 subagents in one parallel message. Sixteen returned synchronously; five went to background dispatch and notified over the next ~5 minutes.
5. Filesystem audit caught **three duplicates** flagged as "skip — already covered" but not actually deleted (Klaassen "Stop Coding", Klaassen "Teach Your AI", Shapiro "You Don't Write the Code") — manually `rm`'d.
6. Assembled 864-line `new-index.md`: 7-theme header + 4-row rollup table + 13-row new-reports table + 8-row primary-source-upgrade table + 15 cluster sections with per-source blocks.

**Outputs:** 7 mhtml kept (informative diagrams), 34 mhtml converted to txt, 6 txt/pdf passthrough, 24 deleted as duplicates. 13 proposed new reports, 8 primary-source upgrades, ~10 existing-report extensions. PR merged same day.

### Example 2: 8-source small batch (negative example)

**Setup:** User drops 6 `.mhtml` + 2 `.txt` (8 total). All on one topic (e.g. five chapters of one book + supporting material).

**Decision:** Skip this skill. 8 files is under the threshold; running an index pass adds an extra round-trip without enough planning payoff. Go straight to `research-pipeline` Phase 0 drain — the drain subagents can do their own triage inline at this scale.

**Anti-example takeaway:** if you find yourself activating this skill for ≤10 files, you've turned an O(1) drain into an O(2) drain for no incremental value.

## Anti-patterns

- **Touching `PLAN.md`, `INDEX.md`, or any existing `research/*.md` report.** This skill is index-only. All changes to existing reports happen in the subsequent drain. If you find yourself editing a report file, stop — you've crossed into `research-pipeline` Phase 0 territory and should be writing a different commit.
- **Inlining the subagent brief into each Agent call.** With 20 subagents, that wastes ~50× the tokens vs. writing the brief once on disk. Always: brief on disk + short per-agent prompt that says "Read the brief at /path, then process [files]".
- **Polling for subagent completion with `bash sleep` loops.** The harness notifies asynchronously. Polling loops orphan their `sleep` children to init when killed, consume context budget needlessly, and are explicitly flagged anti-patterns. Wait passively.
- **Trusting subagent textual reports without auditing the filesystem.** ~10% of subagents in a 20-batch fan-out will claim a disposition they didn't execute. The audit is mandatory, not optional.
- **Producing a free-form index.** The per-source block format must be fixed (Title / URL / Type / Themes / Summary / Image inventory / Action taken / Prior processing / Recommendation) so the downstream drain agent can mechanically parse it.
- **Forgetting to capture the user's themes verbatim.** The themes section is half the value to the next agent; paraphrasing loses the user's framing. If the user enumerates 1..N, count and check before pasting.
- **Letting the working files leak into the drain.** `research/manual/.manifest.json` and `research/manual/.subagent-brief.md` are hidden (dot-prefixed) for a reason: they're provenance artifacts for this skill's run, not source material. The drain skill should ignore them.

## Acceptance criteria

A successful index pass produces:

1. `research/manual/new-index.md` exists, is committed, and renders cleanly on GitHub (no broken markdown, no orphaned `<!-- placeholder -->` blocks).
2. **File-count math closes** in the rollup table: `kept_mhtml + converted + passthrough + deleted == original_count`.
3. Every per-source block has all required fields populated (no `TBD`, `?`, or empty fields).
4. Every "previously processed" claim is grounded in a real grep hit citing the report number/slug. Spot-check 3 random claims.
5. The user's themes (if supplied) appear at the top of the index, in the order they specified, with the count they specified (or with a correction note if the user's numbering was off).
6. No file under `research/` outside `research/manual/` has been modified by this skill's run.

## Provenance

This skill was promoted from `retrospective/2026-05-16-64/preliminary-index-pass-spec.md` — see that spec for the original-session evidence base. The motivating session was PR #61 (the 71-source indexing pass that demonstrated the pattern works at scale).

## See also

- `.claude/skills/research-pipeline/SKILL.md` — the drain skill this skill feeds. Phase 0 is where the index produced here gets consumed.
- `.claude/skills/research-pipeline/scripts/mhtml_extract.py` — the MHTML helper this skill drives.
- `.claude/skills/parallel-subagent-fanout/SKILL.md` — the broader fan-out pattern this skill specializes.
- `.claude/skills/subagent-prompting/SKILL.md` — for the per-subagent brief structure.
