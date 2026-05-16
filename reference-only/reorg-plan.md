# `/reference-only/` Reorganization Plan

## Status

- **Last updated:** 2026-05-16
- **Current step:** Step 1 in PR review
- **Completed steps:** 1
- **Next step:** Step 2

Each step updates this section in its final action so a fresh agent session can pick up cleanly.

---

## How a fresh agent should use this file

**Before doing any git or PR work, read `.claude/skills/always-commit-skill-to-repo/SKILL.md`.** That skill is the canonical source for git/PR discipline in this repo: feature-branch + commit + push + ready-for-review PR (NOT draft) + immediate subscribe via `mcp__github__subscribe_pr_activity`. It is mandatorily triggered before every git operation and every GitHub MCP PR call. The closing actions below are a specialization of that skill for this plan; if the two ever conflict, the skill wins.

1. Read the **Status** section above to find the next step.
2. Read the corresponding `## Step N` section in full.
3. Execute the step. Every step ends with the same closing actions:
   - (a) update the **Status** section,
   - (b) fill in the `### Lessons learned` subsection at the end of the step (see "Why lessons learned" below),
   - (c) commit,
   - (d) push to a new branch off `main` (one branch per step),
   - (e) open a **ready-for-review** PR (NOT draft) with the lessons-learned bullets included verbatim in the description,
   - (f) subscribe to PR activity via `mcp__github__subscribe_pr_activity`.
4. Do NOT skip ahead. Do NOT combine steps into one PR.

**The final step is always the skill-instantiation step at the bottom of this file.** Any new steps added by the user slot in *before* the final step, never after it.

---

## Why "Lessons learned" subsections exist

The terminal step of this plan creates a reusable skill, `reconstitute-and-index-sources`, that is the **general** form of what this plan is doing in a **specific** case. The skill needs to capture not just the recipe but the **process knowledge** — the surprises, the gotchas, the rules that prevented the work from going off the rails, the things that turned out to be harder than expected.

Each step has a `### Lessons learned` subsection at the bottom. Fill it in at the *end* of the step, **just before opening the PR**, while the experience is fresh. The block:

- Can be disorganized. Bullets, half-thoughts, links, contradictions all welcome.
- Should capture *process learning*, not artifact recipe. ("Categorization step took 3 iterations because vendor docs cluster against book chapters in the count" is better than "I categorized 8 sources.")
- Should call out things a future skill-user would benefit from knowing: pitfalls, time sinks, decisions that turned out wrong, heuristics that worked.
- Will be reconciled and synthesized into the actual skill in the final step. Don't pre-edit.

This is the *only* mechanism that lets the final-step skill be informed by what we learn here. If a step skips its lessons-learned subsection, that knowledge is permanently lost.

---

## Scope

What this plan does:
- Reorganize `/reference-only/` into category subdirectories.
- Split the per-source inventory in `/reference-only/README.md` into per-category `INDEX.md` files.
- Eventually instantiate a `reconstitute-and-index-sources` skill that generalizes what we learn here.

What this plan does NOT do:
- Touch `/research/` (any file under it, including `INDEX.md`, `PLAN.md`, reports).
- Restore deleted sources from past commits — that will be a future step the user adds before the final step.
- Make final category decisions — categorization in Step 1 is **interim**, refined later after restoration.

---

## Companion files

- **Category survey (created in Step 1.0):** `/reference-only/category-survey.md` — read-only intuition document used to inform category choice; not modified after Step 1.

---

## Step 1 — Categorize current sources, backfill README, move into category directories

**Branch:** `claude/reference-only-step-1-categorize` (off `main`)
**PR title:** `/reference-only/: categorize and move sources (step 1)`

### 1.0 Survey report source/reference tables for category-shape intuition

- Read source/reference tables in every numbered report under `/research/*.md` and every followup under `/research/followup/*.md`.
- Goal: get a feel for **total source count** (likely 70–100+) and **broad themes** the eventual restored corpus will cluster around (e.g. vendor substrate docs, governance/legal, academic papers, podcast transcripts, blog/essay primary sources, books, dotfile/runner implementations, etc. — let the data tell you).
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
- For sources that fit multiple categories: pick one home; note which other categories were considered. **Brief — we are not having a long discussion about this, just recording that they are in multiple places.**
- **Expect to redo this step 2–3 times before settling.** Categories that look right on paper often turn out lopsided once you start placing sources. Do the choice-of-category step multiple times to get the right size.
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
1. Update the **Status** section: `Completed steps: 1`, `Next step: 2`.
2. Fill in **Lessons learned (Step 1)** below (see "Why lessons learned" at the top of this file — these feed the eventual skill).
3. Commit. Push to `claude/reference-only-step-1-categorize`. Open **ready-for-review** PR (NOT draft, per `.claude/skills/always-commit-skill-to-repo/SKILL.md`). Include in the PR description: the Step 1.0 survey summary, the chosen category table, before/after file lists, and the lessons-learned bullets verbatim.
4. Subscribe to PR activity (`mcp__github__subscribe_pr_activity`).

### Lessons learned (Step 1)

- **The Step 1.0 survey needed a subagent.** Surveying 50 reports' source/reference tables in the main agent context would have blown out the budget — fanned out to an Explore subagent with a tight "under 600 words, no full inventory" cap. The cluster counts came back close enough to ground-truth to inform categorization. Future skill should make subagent-delegation explicit when the citing corpus exceeds ~15-20 reports.
- **Counting-rule ambiguity bit immediately.** The plan says "a vendor doc set or multi-chapter book counts as one source", but `anthropic-agent-skills/` contains *both* (2 vendor-doc pages + 3 cookbook notebooks). Decided to treat the whole subdirectory as one source on grounds that it's one *unit of curated material* drained to one report. The skill should explicitly cover the "mixed-medium subdirectory" case: the cohesion of the subdir wins over the medium-purity of its individual files.
- **Discovered the README was stale beyond just missing rows.** The El Kaim book README claimed 7 chapters but disk now has 9 (chapters 8 and 9 had been added later). Fixed inline during the row-update. The skill should explicitly tell users to **read each source's local `README.md` AND `ls` the actual directory** when backfilling — never trust the parent README's chapter count.
- **Cherny "full" transcript already on disk.** The lenny-podcast-transcripts/README.md flagged the full Cherny transcript as outstanding, but `cherny-head-of-claude-code-full.txt` was already present alongside the first-30-min file. Didn't update the local README this round (out of scope for Step 1; the lenny-transcript README's "what's outstanding" claim is now stale). Future skill: when backfilling, also flag stale claims in the source's *own* README, even if fixing them is out of scope.
- **`git mv` of a directory works as expected** even with intermediate target dirs that already exist. Used a single chained shell with `&&` to do all 8 moves; no breakage. The before/after `find` diff was the fast verification — every "before" path appeared with a renamed prefix in "after" and no new paths showed up. Recommend skill bake this exact verification pattern as a hard requirement.
- **Categorization iteration count: 2.** A first pass produced a medium-based taxonomy (`books`, `essays`, `vendor-docs`, `academic-papers`, `podcast-transcripts`, `external-syntheses`) which the orchestrator rejected in favour of subject-matter. The second pass is the one that landed. The plan's "expect 2-3 iterations" rule held up — but the dimension that drove the rework wasn't *sizing* (the medium taxonomy was perfectly sized), it was the **axis of categorization itself**. Skill must therefore frame the iteration warning around two distinct axes: (a) what dimension are you categorizing by? — subject vs medium vs functional-role; (b) within that dimension, are the categories well-sized? Both can independently trigger a redo.
- **Subject-matter wins over medium when the corpus is curated for citation.** The first-pass medium taxonomy made the categories' *physical shape* legible (a book directory vs a `.txt` essay) but obscured *why a future reader would ever look here*. A reader hunting for "how do practitioners describe their personal harnesses?" doesn't care whether the answer is a blog post or a podcast transcript — they want the harness content. Medium-based categorisation buries the navigation cue inside the medium. Skill should default to **subject-matter** and only fall back to medium-based when the corpus is a heterogeneous dump with no curated subject through-line.
- **Cross-cutters get more interesting under subject-matter taxonomy.** The lenny-podcast-transcripts subdir is a textbook cross-cutter: Willison talks about personal harnesses, Cherny talks about Claude Code substrate. Under the medium taxonomy this was invisible (both are transcripts, end of story). Under subject taxonomy the tension surfaces and has to be resolved (initially chose `practitioner-harnesses` on word-count grounds). Skill should highlight that subject-matter categorisation *generates* cross-cutter discussions that medium-based categorisation hides — and that this is a *feature*, because it forces an explicit decision about what the source is *for*.
- **The sizing rule must drive category count from the start, not from the at-risk warning at the end.** Second pass (subject-matter, 6 categories) was sized for the **current** corpus of 8 sources — not the restored corpus of ~180–220. 6 categories ÷ 200 sources = 33 sources/category average, which breaches the plan's ~15-source ceiling by 2x even before considering cluster imbalance. The orchestrator caught this and triggered a third pass. **Lesson: when the survey gives a corpus-size estimate, compute `target_categories = ceil(estimated_total / target_size)` (so ~13–40 categories for ~200 sources @ 5–15/cat) BEFORE proposing any category list.** The third pass landed on 15 categories, with 6 of them empty pending restoration. The current corpus only populates 9 of the 15.
- **`AskUserQuestion` preview options are framing-bias amplifiers when the option set is below the sizing target.** The "fine-grained (6) vs coarser (4)" question presented both options as if "fine-grained" meant "fine-enough" — but the actually-fine-grained option for a 200-source corpus was ~15 categories. The user picked the better of two undersized options. **Skill should require: when offering option choices for a sizing-sensitive decision, the option set must include at least one option at or above the size-rule's target. If the option set is entirely below target, that's not a redirect — that's a math error.**
- **Existing source units can be split as part of a sizing-driven re-categorisation, but the split has metadata cost.** The third pass split `lenny-podcast-transcripts/` into Willison (→ `willison-canon`) and Cherny (→ `anthropic-substrate/cherny-claude-code-interview/`). The original collection's per-source README had to be either redistributed or replaced; chose to `git rm` the original, fold Willison provenance into the top-level inventory README, and write a fresh README for the Cherny subdir. Skill should note: splitting an existing source unit during a re-categorisation is allowed when the original was a collection-of-convenience (e.g. "both came from the same podcast feed") rather than a curated unit (e.g. multi-chapter book, vendor doc set). The metadata redistribution is small but non-zero — budget 5–10 minutes per split.
- **Empty categories are first-class.** The 15-category taxonomy includes 6 categories with no current on-disk sources. Resisted creating placeholder `.gitkeep` directories — instead, the README lists all 15 categories with a "currently on-disk?" column, and only the 9 populated categories get on-disk directories. Skill should explicitly allow empty categories in the taxonomy as long as they're documented in the top-level README — they encode the *anticipated* shape, which is the entire point of sizing for the restored corpus.
- **"Why this category" column degenerates to mostly `obvious`** when the corpus is small and the categories are medium-based. Only the cross-cutters (`dark-factory-article` essay-vs-book, `chatgpt-deep-research` external-synthesis-vs-vendor-doc) needed real prose. Skill should call out that the column earns its keep at restoration-time when cross-cutters multiply — and warn against the temptation to write verbose "why" cells just because the column is there.
- **Branch-name mismatch caught early.** The session bootstrap branch (`claude/execute-reference-step-one-FZ07O`) and the plan's specified branch (`claude/reference-only-step-1-categorize`) were different. Followed the plan's name on grounds that the plan-specified branch is the durable identifier across resumed sessions, while the bootstrap branch is session-ephemeral. Skill should note: **trust the plan's branch names, not the session's**.
- **No `reference-only/INDEX.md` was created in Step 1.** The plan reserves INDEX creation for Step 2's mechanical split. Resisted the urge to make per-category INDEX stubs in passing. The discipline of "Step 1 moves and categorizes; Step 2 indexes" held cleanly — but the temptation to one-shot is real and the skill should name it.
- **Survey doc (`category-survey.md`) usefulness was more about anticipating size than about choosing names.** The cluster names that came back from the subagent (vendor docs, academic papers, books, blogs, github repos, transcripts, governance, specs) closely matched the final category list — but the *counts* (40-50 papers, 25-35 essays) were the real input: they told me which categories will need a future split. The skill should frame the survey output that way: the counts matter more than the cluster-naming, because the categorisation step will be redone anyway after restoration.

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
3. A **compact category table** — one row per category, columns: `Category` | `Description` | `Sources` (where `Sources` is a comma-separated list of short-name links to the actual file/subdir, not to the INDEX). Purpose: quick-jump navigation, **not** rich commentary — that lives in each category's `INDEX.md`.
4. A link to each category's `INDEX.md` for the rich detail.
5. The existing **"What does NOT belong here"** section — kept verbatim.

Remove the per-source inventory table entirely from the README.

### 2.4 Verification

- Diff: every row from the pre-Step-2 README's per-source table must appear in exactly one category's `INDEX.md`. Build the comparison mechanically (e.g. grep the Source column values).
- Every short-name link in the new README resolves to a real file/dir.
- Every link inside every `INDEX.md` resolves.
- The "What does NOT belong here" section is present and unchanged.

### 2.5 Closing actions

In order:
1. Update **Status**: `Completed steps: 1, 2`, `Next step: (see "Additional steps" section below; if empty, skip to Final step)`.
2. Fill in **Lessons learned (Step 2)** below.
3. Commit. Push to `claude/reference-only-step-2-split-readme`. Open **ready-for-review** PR (NOT draft) with lessons-learned bullets verbatim in the description. Subscribe.

### Lessons learned (Step 2)

*(populate at end of step, before the PR is opened — disorganized bullets welcome; this feeds the skill in the final step)*

---

## Additional steps (to be added by user)

> **Fresh-agent note:** If this section is empty or contains only this note, skip directly to the **Final step** below. New steps added by the user appear between this heading and the Final step heading. They follow the same closing-action convention (update Status, fill in their own `### Lessons learned` subsection, branch + push + ready-for-review PR + subscribe).

*(no additional steps yet)*

---

## Final step — Instantiate the `reconstitute-and-index-sources` skill

**Branch:** `claude/reference-only-final-create-skill` (off `main`, after all prior steps merge)
**PR title:** `Add reconstitute-and-index-sources skill`

This step turns the experience captured in this plan into a reusable skill. The skill is the **general** form of what this plan did in a **specific** case. Treat this plan (steps + lessons-learned subsections) plus the PR descriptions as the corpus.

### F.1 Gather inputs

- **Read this entire plan file** end to end, paying particular attention to:
  - The "Why lessons learned" section (framing for what each step's lessons capture).
  - Every step's `### Lessons learned` subsection.
  - The Scope section — especially "What this plan does NOT do" — these are the natural boundary conditions for the skill.
  - The "Principles to bake in" and "Anti-patterns to bake in" lists below (these are this session's pre-execution wisdom, already extracted from the user-conversation that produced this plan).
- **Fetch the PR description from every prior step's PR** via GitHub MCP tools (`mcp__github__pull_request_read` with `method=get`). Each PR description contains step-specific findings.
- **Inspect sibling skills** in `.claude/skills/` (`adr`, `research-pipeline`, `preliminary-index-pass`, `self-retrospective`, `parallel-subagent-fanout`) for the project's skill-authoring conventions: frontmatter style, section ordering, length, anti-pattern lists, trigger phrasing, when-to-skip rules.

### F.2 Synthesize and author the skill

Create `.claude/skills/reconstitute-and-index-sources/SKILL.md`. Match the conventions of the sibling skills you inspected.

#### Intent (suggested starting point — refine from lessons learned)

When a corpus of primary-source material has been spread across many directories, partially deleted across past commits, or has outgrown its original flat-file inventory, this skill reconstitutes the full set, categorizes it into balanced and navigable groups, and produces a top-level navigation README plus per-category `INDEX.md` files.

#### Trigger phrases (starting candidates)

- "reorganize the reference-only directory"
- "reshape the corpus"
- "split the sources into categories"
- README inventory table has grown past ~20 rows
- sources have been restored from git history and need re-indexing

Refine from the lessons-learned blocks — additional triggers may have surfaced.

#### Principles to bake in (from this session's pre-execution discussion)

These were established by user direction during the planning session. Lessons-learned blocks may refine, contradict, or extend them; reconcile rather than discard.

- **Sizing target ~5–15 sources per category** after the corpus is at full size, with explicit permission for tiny natural categories (1–2 sources OK if that's the natural shape) and a hard rule to split when a category would balloon past ~15.
- **Counting rule:** vendor doc sets and multi-chapter books count as **one source**.
- **Cross-cutting sources:** pick one home, note alternatives briefly — *not* a long discussion. Just record that they're conceptually in multiple places.
- **Survey before categorizing:** scan the existing corpus (report source/reference tables in this case) to get a feel for total count and natural clustering *before* deciding category names. Never categorize blind.
- **Iterative categorization:** expect to redo the choice-of-categories step 2–3 times before settling. Paper-good categories often turn out lopsided once you actually place sources.
- **Interim vs final categorization:** when sources will be restored later, the first categorization is explicitly *interim*. Frame it that way so the next pass isn't blocked by sunk-cost thinking.
- **Mechanical-split discipline:** when splitting an inventory file into per-category sub-files, do *only* the mechanical split. No additions, no rewrites, no commentary. The temptation to "improve while splitting" is the single biggest threat to the integrity of this step.
- **Two-table separation:** top-level README is for **quick-jump navigation only** (compact category table with short-name links). Rich per-source detail lives in per-category INDEX files. Never duplicate.
- **Fresh-agent handoff:** a single Status section in the plan file is the source of truth for what's done and what's next. Update it as the *last* action of each step.
- **Lessons-learned-as-skill-feedstock:** the explicit purpose of the per-step Lessons learned subsections is to capture process knowledge for the skill being authored in the final step. Without these, the skill is just a recipe; with them, it carries hard-won judgement.
- **Branch-per-step + ready-for-review PR + subscribe pattern:** never combine steps into one PR. Each step is independently reviewable and revertible. PRs are ready-for-review by default, not draft (per `.claude/skills/always-commit-skill-to-repo/SKILL.md`).
- **Terminal-step rule for skill instantiation:** the skill-creation step is always last. New steps added later slot in *before* it. Skill instantiation depends on accumulated lessons-learned from all prior steps.

#### Anti-patterns to bake in

- Splitting the README into INDEX files **before** the physical move (links won't resolve; categorization isn't yet pressure-tested by the actual move).
- Adding prose or commentary during the mechanical split step.
- Combining steps into one PR.
- Putting new steps *after* the skill-instantiation step.
- Categorizing without first surveying the eventual corpus shape.
- Treating the first-pass categorization as final when restoration is still pending.
- Letting any step skip its `### Lessons learned` subsection ("we'll fill it in later" — knowledge will be lost).
- Editing the lessons-learned bullets to be "presentable" before they reach the final synthesizer (preserves contradictions and surprises that the synthesizer needs).

#### Verification rules to bake in

- **Before/after `find` diff** to prove no files lost or duplicated when moving sources between directories.
- **Mechanical row-by-row check** that every README inventory row landed in exactly one INDEX.md after a split.
- **Relative-link resolution check** on both the rewritten README and every per-category INDEX.md.

#### Synthesis discipline

Preserve *specific, surprising, hard-won learnings* from the lessons-learned blocks — process gotchas, not just the recipe. Reconcile contradictions explicitly (state both, name the resolution). Discard verbose contradictions only after reconciling them.

### F.3 Closing actions

1. Update **Status** in this plan file: `Completed steps: 1, 2, …, Final`. Mark the plan as complete.
2. (No further lessons-learned additions to this plan — this step's reflections go in the PR description.)
3. Commit. Push to `claude/reference-only-final-create-skill`. Open **ready-for-review** PR (NOT draft) with: the path of the new skill, a summary of the principles and anti-patterns baked in, and a brief note on which lessons-learned bullets were dropped and why. Subscribe.

---

## Categories chosen in Step 1

15 interim **subject-matter** categories. (First pass: medium-based, 6 cats. Second pass: subject-matter, 6 cats. Third pass — this one: subject-matter, 15 cats, sized to anticipate the ~180–220-source restored corpus. See Lessons learned for the iteration history.) Categories are listed below; only the 9 that hold current sources have physical on-disk directories — the other 6 will be created at restoration time.

| Short-name | Definition | Currently on-disk sources | Notes |
|---|---|---|---|
| `dark-factory` | Shapiro / El Kaim Dark-Factory canon — the foundational essays and frameworks on AI-built software as a paradigm. | `dark-factory-article` | — |
| `intent-driven-architecture` | Intent-driven / continuous enterprise architecture, RISE-style automation, software product-line variability. | `el-kaim-book` (9 chapters) | The book is multi-subject (architecture + intent + spec authorship + product-line); placed here because the intent-driven thread runs through all 9 chapters. Alternatives considered: `dark-factory`, `spec-authorship`. |
| `spec-authorship` | Requirements engineering, BMAD, scenario testing, INCOSE primer, spec-as-prompt practice. | (none yet — restoration target) | — |
| `willison-canon` | Simon Willison's collected writings + interviews. Treated as its own subject because of dominance and breadth. | `willison-ai-state-of-the-union-full.txt` (Lenny transcript) | Author-named category, justified by Willison's outsized share of the practitioner-voice corpus. |
| `compound-engineering` | Compound-engineering workflows, personal harnesses, lived-experience practitioner accounts. | `every-my-ai-had-already-fixed.txt` | — |
| `anthropic-substrate` | Claude Code substrate, Anthropic engineering posts on infrastructure, Cherny / Anthropic interviews. | `cherny-claude-code-interview/` (split out of original lenny-podcast-transcripts) | The Cherny interview was split out of the lenny-podcast-transcripts collection because under the sizing-aligned subject taxonomy, the two transcripts no longer share a natural home. |
| `openai-substrate` | Codex substrate, OpenAI cookbook, running-codex-safely docs. | (none yet — restoration target) | — |
| `other-vendor-substrate` | GitHub Copilot cloud-agent, Replit Agent, Google Gemini CLI, Notion, Every.to harnesses, StrongDM factory. | (none yet — restoration target) | Likely the first category to split further once restored, by vendor. |
| `skills-composition` | Skills as a composition primitive — agentskills.io, Anthropic Agent Skills docs + cookbooks, El Kaim codex/skill substrate, MCP protocol. | `anthropic-agent-skills/` (docs + cookbook notebooks) | Anthropic-published material; placed here (not `anthropic-substrate`) because the subject is the *primitive*, not the substrate it ships from. |
| `evals-and-benchmarks` | SWE-bench, SWE-agent, AlphaCode, CodeGen, evals primers (Husain, Shankar), prompt-engineering survey. | (none yet — restoration target) | — |
| `academic-foundations` | Academic methodology papers: underspecification, multi-task program benchmark, CHI/ICSE/ESEC studies. | (none yet — restoration target) | — |
| `security-primitives` | Threat models, prompt-injection defenses, capability/data-flow security. | `camel-paper/` (LaTeX) | — |
| `governance-and-legal` | SOX/GDPR audit, Caremark / RSI board exposure, NHTSA levels, AUTOSAR, ISO 42010. | (none yet — restoration target) | — |
| `ai-engineering-culture` | Team-level dynamics, organisational culture, the social/operational side of AI engineering. | `brier-culture-of-ai-engineering.txt` | — |
| `meta-synthesis` | Derived syntheses over the corpus (counterfactual deep-research outputs, QC re-reads). | `chatgpt-deep-research-2026-05-11/` | Considered `skills-composition` (it is a ChatGPT product output) and rejected — its role is counterfactual synthesis. |

---

## Cross-references

- Survey artifact (created in Step 1.0): `/reference-only/category-survey.md`
- Final skill location: `.claude/skills/reconstitute-and-index-sources/SKILL.md`
