# Spec: `plan-doc-curation`

- **ID**: SKILL-SPEC-d5f8b37eeb
- **Source retrospective**: ../2026-05-21-106.md

## Intent

Clean up long-lived plan, status, and roadmap documents that have accreted log-like content where done tasks mix with todo, stale facts mix with current ones, and narrative mixes with status. Read the doc in full, cross-check every claim against current repo state, classify each section as done / todo / obsolete / stale-fact, produce a numbered cleanup proposal the user reviews and refines iteratively, then collapse the doc into a crisp single-pass execution commit.

## Trigger

Direct user phrases (activate immediately):

- "clean up <PLAN.md | research-plan.md | ROADMAP.md | other long-lived plan doc>"
- "this plan is confusing"
- "PLAN.md has stale entries"
- "the plan mixes todo and done"
- "audit the plan for what's still real"

Proactive triggers (offer the skill):

- User opens a session referencing a multi-section status / plan doc that is more than ~300 lines long.
- User comments that a plan doc's status line disagrees with what's actually in the repo.
- User asks to add a task to a plan doc that already contains items the agent can see are done / superseded.

Negative triggers (do NOT offer):

- Short plan docs (<100 lines) where the user is just asking to add a single item — they don't need a curation pass; they need an edit.
- Docs that aren't plans (READMEs, ADRs, retrospectives, reports).

## Inputs

- One or more plan-doc paths (e.g., `research/PLAN.md`, `research-plan.md`).
- Read access to any catalog / status registers the plan doc may have drifted against (e.g., `reference-only/sources.json`, GitHub issue list, related skill docs).
- The repository's git log.
- User availability for iterative review (the skill produces multiple plan versions; each gets user feedback).

## Outputs

- One temp file at `cleanup-plan-revised.md` (or similar) committed on a feature branch as the working version of the cleanup proposal. Revised in-place across N user-review iterations; each version committed.
- One PR (ready-for-review per project convention) carrying the cleanup-plan temp file as a backup of the planning conversation.
- After the user approves: one cleanup-execution commit that flips the plan doc(s) from confusing to crisp. Lands in a separate commit / PR.

## Workflow

1. **Read every target doc in full** (`Read` tool, no offset truncation past what's necessary). Don't summarise from chunks — the whole-doc view is necessary to catch cross-section drift.

2. **List every claim that's a fact about the repo state** (counts, "currently outstanding", "RESOLVED", "DONE", "still pending", named open issues, named files said to be in some state). For each, cross-check against current repo state — file existence, catalog records, GitHub issue state, git log, etc. Build a table of fact-vs-truth deltas.

3. **Apply the concrete-task criterion** to every entry that claims to be a task: can the agent be told exactly what to do, exactly where, exactly with what threshold? If no, the item is either (a) a wishlist that should move to a separate status register (sources.json wanted record, GitHub issue, etc.), or (b) deleted from the plan.

4. **Classify each section** as `keep` / `update` / `delete` / `move-elsewhere`. Sections that exist purely as historical log (version-history paragraphs, completed-bottleneck sections marked RESOLVED with strikethrough, "done as of X" subsections) → delete; the git log holds the audit trail.

5. **Produce a numbered cleanup plan** with one item per intended change. Number them for user reference. Group by target file. Each item: 1-3 sentences describing what to do.

6. **Write the cleanup plan to a temp file** (`cleanup-plan-revised.md` or similar) at the repo root, commit on a feature branch, push, open a PR ready-for-review. **This is durable backup against context truncation** — see AGENTS-MD `commit-wip-planning-doc`.

7. **Iterate with the user.** For each round of feedback: revise the plan in-place, commit the revision with a `vN` message, push. Show only the things changed by the user's comments in chat — not the whole plan.

8. **Apply universally any style rules the user articulates.** When the user makes a meta-comment ("no counts in plan docs", "session bullets should be just date/time/PR-link"), capture it as a "Style rules" section at the top of the plan doc that applies to all entries. Don't re-litigate the rule per item.

9. **For any tactical fix that's incidentally executed during planning** (e.g., adding a record to sources.json that was a Future-research item), do it under the existing skill conventions (research-pipeline `_catalog/edit.md` patterns), commit alongside the planning revision, note it in the plan as "[already executed]".

10. **When the plan is approved**: hand off to a separate execution session (or the same agent's next message). The plan-doc-curation skill stops at planning; execution is a separate task to keep the planning artifact reviewable as a unit.

## Concrete examples

### Example 1: research/PLAN.md cleanup (this session)

Starting state: PLAN.md 539 lines, v0.17. §1 a 600-word run-on status paragraph; §1 done-bullet list with 17 session bullets each 100-200 words; §3 with 6 sub-bottlenecks, three of them marked RESOLVED with strikethrough; §3.4 "Pending retrospective decisions" tabulating retro backlog (user wants retrospective references entirely excised); §4 manual fetch instructions with stale URLs (`platform.claude.com` URLs listed as outstanding but actually `have+complete` in catalog); §11-§17 archive sections + version history; Future-research section with 4 entries, half of which were already drained.

After fact-checks: report counts were 37+12 in PLAN.md but 38+14 on disk; `risks-and-mitigations` URL was 404; `platform.claude.com` URLs were `have+complete`; LukePM and Schillace "compounding teams" already in catalog with reports drained; issues #41/#42 still OPEN on GitHub but PR #44 already had their drain content.

Cleanup plan v1: 49 numbered items across 6 files. User reviewed in chat. Comments produced v2: no counts anywhere, source tracking in sources.json only, no retro references, strict session-bullet format, concrete-task criterion applied universally, plus deletions/rewrites of several files (`plan-sync.md`, `reorg-plan.md`, `category-survey.md`). v3 tightened the bullet format further ("you are cheating with semicolons"); v4 actually added jaymin-transcript wanted records to sources.json per user direction. v5 added a Section L addressing linter findings (5 lint errors, all from Round-12 reports citing un-cataloged URLs). v6 added an item (52) ensuring the deferred linter items L.4 + L.5 land in cleaned-up PLAN.md §5 so a future agent finds them.

Each version committed. PR merged at v6. Actual cleanup execution deferred to a separate commit.

### Example 2: hypothetical ROADMAP.md cleanup

Starting state: a 400-line `ROADMAP.md` with "Q1 / Q2 / Q3 / Q4" sections, each holding ~10 bullets. Some bullets are "DONE [link to PR]"; some are "in progress"; some are "deferred to next year"; some are aspirational ("would be nice if X").

Apply the workflow:
- Step 2 fact-check: walk every "DONE" link to verify the PR actually merged; walk every "in progress" assignee to verify it's still in flight.
- Step 3 concrete-task: "would be nice if X" without a defined scope → delete. "Build feature Y in Q3" with a 3-line description and an owner → keep.
- Step 4 classify: Q1-Q2 sections (all DONE) → delete; the past is the git log. Q3 in-progress items → keep with current state. Q4 aspirational items → either promote to GitHub issues with owners or delete.
- Step 5-7 produce numbered cleanup plan; iterate with user; commit each version.
- After approval: execution commit collapses the file from 400 to ~80 lines.

## Anti-patterns

- **Summarising from chunks instead of reading the whole doc.** The dominant failure mode in this session would have been catching only the §1 status drift and missing the §11-§17 archive sections or the §3.4 retrospective entanglement. The fact-checks have to be against the whole doc.
- **Re-litigating user style preferences per item.** When the user says "no counts in plan docs," apply it everywhere in one pass and capture it as a universal style rule at the top of the plan. Don't ask "should §2 also have no counts?" for each section.
- **Letting the planning conversation grow without committing it.** Multi-version planning conversations crash and burn if context is truncated mid-iteration. Commit-the-plan-as-WIP after every revision (see AGENTS-MD-5b47d51ebd).
- **Executing the cleanup as part of planning.** Keep the plan reviewable as a unit. Execution is a separate task; mixing them produces a PR diff the user can't meaningfully review.
- **Trusting "DONE" markers without verifying.** This session had three `~~RESOLVED~~` bottlenecks, all of which were genuinely resolved — but PLAN.md also had `~~~Done 2026-05-13~~` items that referenced commits no longer reachable. The fact-check has to verify against current repo state, not against what the plan doc claims.
- **Failing to persist deferred items into the cleaned-up plan.** Section L of v5 lived only in the ephemeral planning doc; until v6 added item 52, the deferred L.4 + L.5 had no durable home. Anything that survives the cleanup needs an explicit landing place in the post-cleanup doc.

## Acceptance criteria

- [ ] Every fact-claim in the plan doc was cross-checked against current repo state, with deltas captured in the cleanup plan.
- [ ] Every entry in the cleaned plan passes the concrete-task criterion.
- [ ] Source-status / catalog-state items have moved to their proper status register (sources.json or equivalent), not stayed in the plan.
- [ ] The cleanup plan is committed as a WIP file on a feature branch with a PR before any execution begins.
- [ ] After cleanup execution, `wc -l` on the target doc is meaningfully lower than before (typically 40-80% reduction for a doc that had accreted unchecked).

## Files this skill creates / modifies

- `cleanup-plan-revised.md` (or similar) at repo root — temporary WIP plan, committed on feature branch, deleted by the execution commit.
- The target plan doc(s) (e.g., `research/PLAN.md`, `research-plan.md`) — edited in the execution commit.
- Files the cleanup proposes deleting (obsolete plan files, bridge files like `plan-sync.md`) — removed via `git rm` in the execution commit.
- Skill resource docs that encode the rules surfaced during cleanup (e.g., `.claude/skills/research-pipeline/resources/_plan/update-discipline.md` for new session-bullet format).
