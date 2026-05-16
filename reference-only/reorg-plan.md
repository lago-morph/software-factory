# `/reference-only/` Reorganization Plan

## Status

- **Last updated:** 2026-05-16
- **Current step:** not started
- **Completed steps:** (none)
- **Next step:** Step 1

Each step updates this section in its final action so a fresh agent session can pick up cleanly.

---

## How a fresh agent should use this file

1. Read the **Status** section above to find the next step.
2. Read the corresponding `## Step N` section in full.
3. Execute the step. Every step ends with the same closing actions:
   - (a) update the **Status** section of this file,
   - (b) append a `### From Step N` block to `/reference-only/reconstitute-and-index-sources-skill-spec.md` containing lessons-learned + enhancement suggestions (allowed to be messy / disorganized),
   - (c) commit,
   - (d) push to a new branch off `main` (one branch per step),
   - (e) open a **draft** PR,
   - (f) subscribe to PR activity via `mcp__github__subscribe_pr_activity`.
4. Do NOT skip ahead. Do NOT combine steps into one PR.

**The final step is always the skill-instantiation step at the bottom of this file.** Any new steps added by the user slot in *before* the final step, never after it.

---

## Scope

What this plan does:
- Reorganize `/reference-only/` into category subdirectories.
- Split the per-source inventory from `/reference-only/README.md` into per-category `INDEX.md` files.
- Eventually instantiate a `reconstitute-and-index-sources` skill capturing what we learn.

What this plan does NOT do:
- Touch `/research/` (any file under it, including `INDEX.md`, `PLAN.md`, report files).
- Restore deleted sources from past commits — that will be a future step the user adds before the final step.
- Make final category decisions — categorization in Step 1 is **interim**, refined later after restoration.

---

## Companion files

- **Skill spec:** `/reference-only/reconstitute-and-index-sources-skill-spec.md` — lessons-learned accumulator, ultimately consumed by the final step.
- **Category survey (created in Step 1.0):** `/reference-only/category-survey.md` — read-only intuition document; not modified after Step 1.

---

## Step 1 — Categorize current sources, backfill README, move into category directories

**Branch:** `claude/reference-only-step-1-categorize` (off `main`)
**PR title:** `/reference-only/: categorize and move sources (step 1)`

### 1.0 Survey report source/reference tables for category-shape intuition

- Read the source/reference tables in every numbered report under `/research/*.md` and every followup under `/research/followup/*.md`.
- Goal: get a feel for **total source count** (likely 70–100+) and the **broad themes** the eventual restored corpus will cluster around (e.g. vendor substrate docs, governance/legal, academic papers, podcast transcripts, blog/essay primary sources, books, dotfile/runner implementations, etc. — let the data tell you).
- Commit findings to a new file `/reference-only/category-survey.md` with:
  - Rough total source count (with method: how you counted).
  - A list of tentative category names with 1-line definitions and approximate counts.
  - Any sources that are obviously cross-cutting / hard to place.
- This file is reference material for later steps; do **not** modify it after Step 1.

### 1.1 Backfill missing rows in `/reference-only/README.md`

The current README inventories only 5 of the ~8 source units on disk. Add table rows for each of the missing sources:

- `anthropic-agent-skills/`
- `camel-paper/`
- `lenny-podcast-transcripts/`

For each: reconstruct `Source` / `Used by` / `Provenance` columns by reading the source's own local `README.md` (if present) and `grep`-ing across `/research/` for citing reports. Keep the existing column shape.

Do this **before** the categorization decision in 1.2 so the categorization sees the complete picture.

### 1.2 Decide interim categories

Constraints:
- Use the survey from Step 1.0 to anticipate the eventual restored corpus shape.
- Target: **~5–15 sources per category** after future reconstitution. Use judgement — a category with 1–2 sources is acceptable if it's a natural fit; split a category if it would balloon past ~15.
- A vendor doc set or multi-chapter book counts as **one source**.
- For sources that fit multiple categories: pick one home; record which other categories were considered (briefly).
- Categorization here is **interim**. Final categorization happens in a later step after sources are restored.

Document the chosen categories in the `## Categories chosen in Step 1` section at the bottom of this file. For each category: short-name (used as directory name), 1-line definition, list of currently-present sources that belong, and (for cross-cutting sources) the categories considered.

### 1.3 Add Category column to the README table

Extend the `/reference-only/README.md` inventory table with two new columns:

- **Category** — the short-name from 1.2.
- **Why this category** — one of:
  - `obvious` (when it is),
  - a short phrase explaining the choice,
  - for cross-cutting sources: the chosen category + a short list of others considered.

No prose discussion — table cells only.

### 1.4 Create category directories and move sources

- Create `/reference-only/<short-name>/` for each category from 1.2.
- For each source:
  - Multi-file subdirs (`el-kaim-book/`, `anthropic-agent-skills/`, `chatgpt-deep-research-2026-05-11/`, `camel-paper/`, `lenny-podcast-transcripts/`): keep the subdir intact; move the whole directory under the category.
  - Single-file sources (`dark-factory-article.txt`, `brier-culture-of-ai-engineering.txt`, `every-my-ai-had-already-fixed.txt`): place directly under the category dir.
  - Use `git mv` to preserve history.
- Update the `Path` column in `/reference-only/README.md` to the new path for every source.
- Update any relative links elsewhere in the README that pointed at moved files.

### 1.5 Verification

- Capture `find /reference-only -type f -not -path '*/.*'` before and after the move; diff the two lists. Every file from "before" must appear (renamed) in "after"; no new files appear other than intentional ones; no duplicates.
- Confirm no source appears under two category directories.
- Spot-check every relative link in `/reference-only/README.md` — they must resolve.

### 1.6 Closing actions

In order:
1. Update the **Status** section of this file: `Completed steps: 1`, `Next step: 2`.
2. Append a `### From Step 1` block to `/reference-only/reconstitute-and-index-sources-skill-spec.md` with lessons-learned + enhancement suggestions (can be disorganized).
3. Commit. Push to `claude/reference-only-step-1-categorize`. Open **draft** PR. Include in the PR description: the Step 1.0 survey summary, the chosen category table, before/after file lists.
4. Subscribe to PR activity (`mcp__github__subscribe_pr_activity`).

---

## Step 2 — Split README into per-category INDEX.md files

**Branch:** `claude/reference-only-step-2-split-readme` (off `main`, after Step 1 merges)
**PR title:** `/reference-only/: split README into per-category INDEX.md files (step 2)`

### 2.1 Confirm Step 1 is merged

- `git fetch origin && git log origin/main` and confirm the Step 1 PR landed. If not, stop and wait.

### 2.2 Create `INDEX.md` per category

For each `/reference-only/<category>/` directory:
- Create `/reference-only/<category>/INDEX.md`.
- Copy verbatim the inventory rows for that category's sources from the current `/reference-only/README.md` (header + rows for that category's sources only).
- **Mechanical only.** No additions, no edits, no re-prose. If the temptation arises, stop — that belongs in a later step.

### 2.3 Replace `/reference-only/README.md`

The new README contains:
1. The existing intro paragraph (unchanged or minimally re-pointed).
2. A short prose section describing the **category-based organization** introduced by this plan.
3. A **compact category table** — one row per category, columns: `Category` | `Description` | `Sources` (where `Sources` is a comma-separated list of short-name links to the actual file/subdir, not to the INDEX). Purpose: quick-jump navigation.
4. A link to each category's `INDEX.md` for rich detail.
5. The existing **"What does NOT belong here"** section — kept verbatim.

Remove the per-source inventory table entirely from the README.

### 2.4 Verification

- Diff: every row from the pre-Step-2 README's per-source table must appear in exactly one category's `INDEX.md`. Build the comparison mechanically (e.g. grep the Source column values).
- Every short-name link in the new README resolves to a real file/dir.
- Every link inside every `INDEX.md` resolves.
- The "What does NOT belong here" section is present and unchanged.

### 2.5 Closing actions

In order:
1. Update **Status**: `Completed steps: 1, 2`, `Next step: (see 'Additional steps' section below; if empty, skip to Final step)`.
2. Append `### From Step 2` to the skill spec with lessons-learned + enhancement suggestions.
3. Commit. Push to `claude/reference-only-step-2-split-readme`. Open **draft** PR. Subscribe.

---

## Additional steps (to be added by user)

> **Fresh-agent note:** If this section is empty or contains only this note, skip directly to the **Final step** below. New steps added by the user will appear between this heading and the Final step heading. They follow the same closing-action convention (update Status, append `### From Step N` to the skill spec, branch + push + draft PR + subscribe).

*(no additional steps yet)*

---

## Final step — Instantiate the `reconstitute-and-index-sources` skill

**Branch:** `claude/reference-only-final-create-skill` (off `main`, after all prior steps merge)
**PR title:** `Add reconstitute-and-index-sources skill`

### F.1 Gather inputs

- Read the full accumulated `/reference-only/reconstitute-and-index-sources-skill-spec.md`. Every `### From Step N` block is fair game; they may contradict each other — reconcile in the synthesis.
- Fetch the PR description from every prior step's PR via GitHub MCP tools (`mcp__github__pull_request_read`, etc.). Each PR description contains step-specific findings that may not have made it into the spec.
- Inspect sibling skills in `.claude/skills/` (`adr`, `research-pipeline`, `preliminary-index-pass`, `self-retrospective`, `parallel-subagent-fanout`) for the project's skill-authoring conventions.

### F.2 Author the skill

- Create `.claude/skills/reconstitute-and-index-sources/SKILL.md`.
- Distill the accumulated lessons-learned into a concrete, executable skill: clear trigger description, scope, step-by-step procedure, anti-patterns, verification rules.
- Capture as much of the *process learning* (not just the artifact recipe) as possible — what went wrong, what surprises came up, what guardrails would have helped.

### F.3 Closing actions

1. Update **Status**: `Completed steps: 1, 2, ..., Final`. Mark the plan as complete.
2. (No further additions to the spec.)
3. Commit. Push to `claude/reference-only-final-create-skill`. Open **draft** PR. Subscribe.

---

## Categories chosen in Step 1

*(filled during Step 1.2; structure below is a template)*

| Short-name | Definition | Current sources | Notes (cross-cutting / alternatives considered) |
|---|---|---|---|
| *(tbd)* | | | |

---

## Cross-references

- Skill spec accumulator: `/reference-only/reconstitute-and-index-sources-skill-spec.md`
- Survey artifact (created in Step 1.0): `/reference-only/category-survey.md`
- Final skill location: `.claude/skills/reconstitute-and-index-sources/SKILL.md`
