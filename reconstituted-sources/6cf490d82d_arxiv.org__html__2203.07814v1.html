# Retrospective — skill-library consolidation, PLAN.md as canonical next-steps, Round 3/4/5 catalogs, and the 26-subagent fanout

- **UTC date**: 2026-05-11 (dated to the last PR in coverage: PR #25 merged 2026-05-11T12:48:03Z)
- **Sequence**: 02 (sibling of 2026-05-11-01, which covered PRs #1, #2, #10; this back-fills the same calendar day)
- **Provenance**: **SYNTHETIC / BACK-FILLED**. Authored 2026-05-14 to close "dark zone 1" (PRs #11–#25) identified by the retro-coverage audit. The session that produced these PRs did not produce its own retrospective; this report is reconstructed from PR descriptions, commit metadata, and the surrounding retros.
- **Branch at write time**: `claude/analyze-retro-coverage-WDhhM`
- **Sibling artifacts**: [./2026-05-11-02/](./2026-05-11-02/)

---

## Commit hashes by PR

The PRs in this window cluster into four overlapping work-streams. Listed in merge order:

### PR #11 — `claude/add-three-skills` (merged into main at `f7baf76`, 2026-05-11 01:24Z)

Single squash commit, +812 lines. Three internal skills extracted from the prior session's hand-run patterns:
- `.claude/skills/research-pipeline/SKILL.md` (604 lines, 11-phase pipeline)
- `.claude/skills/always-commit-skill-to-repo/SKILL.md` (95 lines, sandbox-persistence reminder)
- `.claude/skills/in-flight-workflow-tracking/SKILL.md` (113 lines, async-work tracker)

### PR #12 — `claude/cleanup-research-files-ZUsg2` (merged into main at `8eca425`, 2026-05-11 02:22Z)

3 commits, **+568 / −39,243** (the deletions dwarfed everything). Deleted every locally-cached HTML/MD/TXT under `research/fetched/issue-4/` and the round-1 manual fetches now that the content was incorporated into reports 01/03/05/06/09/11/12. Plus 4 Cloudflare-stub deletions (el-kaim, welkaim ×2, jayminwest.substack.com).

### PR #13 — `claude/import-ai-skills` (**closed unmerged** 2026-05-11 02:34Z)

Single commit, +2589 lines across 15 files. Opened to import `self-retrospective`, `parallel-subagent-fanout`, `subagent-prompting` from `lago-morph/ai-skills` as a fresh-branch PR. **Closed in favor of folding into PR #14** on the in-flight `claude/followup-and-fetch-skill` branch — see lesson L-1 below.

### PR #14 — `claude/followup-and-fetch-skill` (merged into main at `6016fcb`, 2026-05-11 03:29Z)

3 commits, +4660 lines, 22 new files. The "rest of the session that produced retro 2026-05-11-01":
- `1aa3d87` Add three skills from lago-morph/ai-skills (the work PR #13 had attempted)
- `4bd2735` Add ADR skill + bootstrap `docs/adr/` with first real ADR (ADR-0001 fetch-blocked-urls-mechanism)
- `6016fcb` Retrospective 2026-05-11-01: align ADR with agent-os, restructure skills, on-disk retrospective output

Includes the `retrospective/report/2026-05-11-01.md` artifact and the freshly-rewritten `self-retrospective` skill that produced it.

### PR #15 — `claude/followup-and-fetch-skill` (merged at `ee71be8`, 2026-05-11 03:40Z)

Single commit, +102 / −28. Two refinements to `self-retrospective`:
- Path: `retrospective/report/YYYY-MM-DD-NN.md` → `retrospective/YYYY-MM-DD-NN.md` (drop the redundant `/report/` segment).
- New **Part 4 — proposed ADRs** template; the regenerated 2026-05-11-01 report lists 7 candidate ADRs.

### PR #16 — `claude/update-commit-skill-OkZmO` (merged at `b3a3945`, 2026-05-11 03:45Z)

Single commit to `always-commit-skill-to-repo/SKILL.md`. Removed the "skip PR" escape hatch; PR creation is now non-negotiable. Added a Step-7 PR lifecycle section: push follow-up commits to the same branch, update PR description when the diff diverges, fix CI failures, address review comments, subscribe to PR activity. Two anti-patterns added (stale-description PR; abandoned-PR-with-red-CI). This rule was authored in direct response to the PR #13/#14 episode — see L-1.

### PR #17 — `claude/update-commit-skill-OkZmO` (merged at `c8e3cbd`, 2026-05-11 03:55Z)

Single commit, +285 / −322. Folded `followup.md` (root-level 12-thread catalog from retro 2026-05-11-01) into `research/PLAN.md` as a new **§11 — Round 3 follow-up research threads**, with priority tiers + 3-wave dispatch order in §11.0 and "Notes for subagents" in §11.13. Deleted `followup.md`. Aligned heading convention to `§11.1 … §11.13`. Footer bumped to v0.3.

### PR #18 — `claude/drain-manual-research-sources` (merged at `e70c6a1`, 2026-05-11 04:25Z)

Single commit, +95 / −4245. First Phase-0 drain of user-supplied `research/manual/` content:
- **Klaassen post-paywall** every.to article: full primary-source unlock; report 03 gains a new "Cora playbook" section (5 use cases, 5-step playbook, three project-level metrics, $400/$400k framing).
- **Two Lenny URLs**: paywall persisted; cookies were not paid-subscriber cookies. Recorded as third failed retrieval route.
- **Three Cloudflare URLs**: stubs only. Cookies don't bypass JS challenges; Path B required.
Six manual files deleted post-consumption.

### PR #19 — `claude/drain-manual-round-2` (merged at `91baf1a`, 2026-05-11 04:51Z)

2 commits, +605 / −796. Second drain wave. Two parallel subagents dispatched:
- **Subagent A** — incorporated the **Dark Factory primary source** (41 KB Path-B text export) into report 07. 11 new top-level sections, 22 verbatim-quote replacements, and a refutation pass against 10 prior reconstructed claims. PLAN §11.12 RESOLVED.
- **Subagent D** — produced Round 4 catalog (§12) from the 7-chapter El Kaim book in `research/manual/multi/`: four parallelizable cluster briefs A/B/C/D.

Lenny URLs reclassified as **video-only**: the URL has no text body; the paywall stub is just an editorial-summary placeholder. Confirmed by user-supplied note ("just a video"). Cherny's 10–30 PRs/day and 10–15 parallel-sessions numbers in report 06 flipped to unprimary-sourced + unrecoverable from URL.

**Refutations of reconstructed report 07** (caught by primary source):
- "Code must not be written/reviewed by humans" charter is StrongDM's, not El Kaim's.
- El Kaim names **two** inflection points (Oct-2024 Sonnet v2 + Nov-2025 Opus 4.5/GPT-5.2), not one.
- Gas Town is an **attribution** layer; the runners are Kilroy / Mammoth / Smasher / Tracker.
- Beads is **not** "backed by Dolt" — that came from HN, not the primary source.

### PR #20 — `claude/cleanup-fetch-tooling` (merged at `9dc722c`, 2026-05-11 05:03Z)

Single commit, +25 / −15. Audited the four `research/blocked*`, `unfetched-sources.md`, `fetch-from-browser.sh` files. Two were skill-referenced but **not catalogued in PLAN.md** — surfaced as functionally orphaned. Created **PLAN.md §5.1 — Workflow tooling** to enumerate the four canonical files; added a "what does NOT belong on main" sidebar (`.fetch-work/`, post-Phase-9 `research/manual/` content, stale `fetched/issue-N` branches). Deleted `.fetch-work/urls.txt` (stale issue-#8 manifest) and added it to `.gitignore`. Identified `fetched/issue-8` remote branch as stale (drain already incorporated) but deferred deletion. PLAN.md v0.5.

### PR #21 — `claude/file-external-synthesis` (merged at `6a14579`, 2026-05-11 05:29Z)

Single commit, +188 / −1. Filed a ChatGPT deep-research synthesis as an external counterfactual artifact:
- Created `research/external-syntheses/chatgpt-deep-research-2026-05-11/` with `report.md`, `sources.md`, and a `README.md` orientation file explaining the `citeturnXXviewYY` broken-citation gotcha (decoded only by the paired sources doc).
- **§5.2 added** to PLAN.md — sibling to §5.1, cataloguing external-synthesis artifacts.
- **§13 added** to PLAN.md — Round 5 with six dispatch-ready source-cluster briefs (Codex, Copilot, Replit, Tabnine, Academic foundations, Anthropic engineering trilogy), a weak-citations QC checklist, and an explicit counterfactual-comparison instruction for the still-pending Round-2 synthesis. PLAN.md v0.6.

Deliberately **not** numbered as `research/13-*.md` — that slot is reserved for our own Round-2 synthesis.

### PR #22 — `claude/refresh-parallel-subagent-fanout-qYe8e` (merged at `6574ad2`, 2026-05-11 05:38Z)

Single commit, +188 lines, 3 files. Refresh of the `parallel-subagent-fanout` skill installed in PR #14. Two key insertions into `SKILL.md`:
- **`isolation: "worktree"` is mandatory** on every Agent call in fanout dispatches. Concrete code example included. Anti-pattern: dispatching without isolation contaminates branches and races on git operations.
- Conventions: **double-dash branch naming** (`feature--sub-N`) to avoid git-ref collisions with slash separators; **plan-order merge** for deterministic run reports; explicit **user-approval gate** on the decomposition plan.

### PR #25 — `claude/parallelize-with-subagents-SO0nR` (merged at `d48fd8b`, 2026-05-11 12:48Z)

**68 commits, +5908 / −2 lines, 32 files.** First real exercise of the just-released fanout skill: a 26-subtask drain across **Rounds 2, 3, 4, and 5** of the PLAN.md catalog. The state.json + report.md + per-sub-branch worktree pattern was load-tested at scale. Merge took ~6.5 hours from PR-open to PR-merge — the longest single PR window in the entire repo history at this point. PR body itself is empty (the initial-state-only commit message says "initialise state"; the body of work landed via the 68 child commits as the fanout drained).

(Numbering gap: there is no PR #23 or #24 — those are issue numbers in the shared issue/PR namespace.)

---

## Part 1 — what happened

This session is best read as the continuation of the one that produced retro 2026-05-11-01. **At the time retro 1 was written, work was already in flight on the same branch (`claude/followup-and-fetch-skill`) that would become PR #14.** What follows is the ~11.5 hours of work that landed *after* retro 1 froze, plus the work that produced the retro itself but landed via PRs not covered in that retro.

### Phase 1 — Skill extraction from the prior session (PR #11)

Goal: turn the patterns we'd been hand-running for two days into reusable, harness-loadable skills.

Approach: three skills authored in parallel, each in `.claude/skills/<name>/SKILL.md`, each with a deliberately broad description so the harness would load it preemptively rather than only after a trigger word matched.

- `research-pipeline` codified the 11-phase multi-source-research discipline. Conventions and naming were **consolidated into a single section near the top** so future agents find the rules mechanically without scanning the whole skill body. The bootstrap workflow YAML + scripts were inlined so the skill works in a fresh repo that doesn't yet have the fetch action.
- `always-commit-skill-to-repo` translated the sandbox-persistence model into plain language ("only files committed AND pushed survive"). The four anti-patterns are all real failures the prior session hit, including the home-dir skill install that would have rotted at shutdown.
- `in-flight-workflow-tracking` codified the per-item format and the "MANDATORY first action" promotion rule from PLAN.md §10.4 step 1.

The deliberate non-overlap with the existing `fetch-blocked-urls` skill (label-as-security-gate, Wayback fallback, html2text PDF caveat) is documented in a cross-reference section. Cleanup: the ephemeral `~/.claude/skills/research-pipeline/` copy was removed since `~/.claude/` doesn't survive shutdown.

### Phase 2 — Cache eviction (PR #12)

Goal: now that 8 reports' worth of fetched HTML/MD/TXT was incorporated, evict the cache.

Approach: delete every cached source whose content had been incorporated into a markdown report; delete every Cloudflare-stub file (~5.5 KB "Just a moment…" body) that contained no usable content. Net: **−39,243 lines** in 83 file deletions. A second wave deleted the issue-4 fetched/ subtree (all 10 sub-files) once reports 09/11/12 had been verified to fully cover them.

Unplanned but mattered: the cache had grown large enough that a single PR's diff was dominated by deletions. The `mergeable_state` was "unknown" until the PR opened — large-delete diffs can stall the GitHub UI's mergeability check.

### Phase 3 — The PR #13 → #14 redundancy (lesson L-1)

Goal: import `self-retrospective`, `parallel-subagent-fanout`, `subagent-prompting` from `lago-morph/ai-skills`.

**The mistake.** I opened **PR #13 on a fresh branch** (`claude/import-ai-skills`) for the import. Meanwhile the in-flight branch `claude/followup-and-fetch-skill` had open ADR / retro-skill work targeting the same files. After opening #13 I realized the two would conflict and that the canonical place was the in-flight branch.

**The recovery.** Closed PR #13 unmerged. Cherry-picked the 15 imported files onto `claude/followup-and-fetch-skill` as a new commit (`1aa3d87`). Those same 15 files merged via PR #14 a few minutes later, alongside the ADR skill creation and the retro-skill rewrite.

This is the **direct origin of PR #16's "push follow-up commits to the same branch rather than opening duplicate PRs"** rule.

### Phase 4 — ADR skill + the retro-skill rewrite (PR #14)

Goal: build the ADR skill from scratch aligned with `lago-morph/agent-os/adr` conventions (surveyed against 41 real ADRs); land the first real ADR (`docs/adr/0001-fetch-blocked-urls-mechanism.md`); rewire `self-retrospective` to produce on-disk artifacts.

The `self-retrospective` rewrite added what now feels load-bearing:
- **Mandatory UTC date verification via tool call** before any date-stamped artifact. Never trust the model's notion of the date. (Why: the model's training-cutoff date and the harness's wall-clock can disagree; one tool call is cheaper than dating something a year wrong.)
- **Sequence numbering** (`YYYY-MM-DD-NN`) to allow multiple retros per UTC day. This very file is `2026-05-11-02` because `01` is taken.
- **Commit hashes grouped by PR** in the main report, not by chronological commit order.
- **Sibling directory** with per-skill `-spec.md` files self-contained enough that a fresh-context agent can implement each skill from one file alone.
- **`AGENTS.md` / "agents file"**, not `CLAUDE.md`. Generic naming.

The ADR link checker landed in this PR with 7/7 GFM-slug fixtures passing — the load-bearing case being the em-dash treatment `"6. GitHub Action — security stance" → "6-github-action--security-stance"` (GFM **preserves** consecutive hyphens from stripped punctuation; the naive collapse would silently break anchor links).

### Phase 5 — Path-flatten + Part 4 (PR #15)

Two refinements landed within 11 minutes of #14 merging:
- Flatten `retrospective/report/YYYY-MM-DD-NN.md` → `retrospective/YYYY-MM-DD-NN.md`. The `/report/` segment was inherited from the upstream skill's spec example and added no information.
- Add **Part 4 — proposed ADRs** template. Titles + one-line rationale only — no specs. User decides per ADR whether to invest.

The ADR link checker caught one broken relative path (`../../../docs` → `../../docs` in `adr-spec.md`) before push — exactly the kind of mechanical regression the checker exists to catch when a directory move renumbers parent traversals.

### Phase 6 — PR-lifecycle hardening (PR #16)

Goal: bake the PR #13 lesson into the always-commit skill so future sessions don't repeat it.

Removed the "skip PR" escape hatch entirely; PR creation is now non-negotiable unless the user explicitly opts out *for that specific change*. Added a Step-7 lifecycle section enumerating six obligations: push to same branch, update description when diff diverges, fix CI (don't paper over with re-runs), address every review comment, resolve conflicts with main, subscribe to PR activity. Two new anti-patterns:
- "Opened PR with stale description after follow-up commits."
- "Opened PR and abandoned it (red CI, unanswered threads, rotting branch)."

The strengthening was small in lines (+33 / −6) but high-leverage in operational discipline.

### Phase 7 — PLAN.md as the canonical next-steps doc (PR #17, then #20, #21)

Goal: stop the proliferation of parallel "next steps" documents.

Pre-state: `followup.md` at repo root (12 threads), `research/PLAN.md` (the skill-referenced canonical), `.fetch-work/urls.txt` (ephemeral but committed), `research/fetch-from-browser.sh` (skill-referenced but not catalogued in PLAN), `research/unfetched-sources.md` (skill-referenced but not catalogued).

Three consolidations:
- **#17**: Fold `followup.md` 12 threads into `PLAN.md` as new §11 (Round 3 catalog) with priority tiers + 3-wave dispatch order. Delete `followup.md`. Bump v0.3.
- **#20**: Audit the 4 workflow-tooling files; catalog the two orphaned ones in new **§5.1 — Workflow tooling**. Delete `.fetch-work/`, add to `.gitignore`. Add a "what does NOT belong on main" sidebar. Bump v0.5.
- **#21**: File ChatGPT deep-research synthesis at `research/external-syntheses/chatgpt-deep-research-2026-05-11/`. Add **§5.2 — External-synthesis artifacts** alongside §5.1. Add **§13 — Round 5** with 6 source-cluster briefs + weak-citations QC checklist + explicit counterfactual-comparison instruction. Bump v0.6.

After this trio, **PLAN.md is the only "what's next" doc**. Every workflow file is either catalogued in §5.1/§5.2 or explicitly named in the "does NOT belong on main" sidebar. This pattern has held since.

### Phase 8 — Two Phase-0 drains (PR #18, then #19) — and the Lenny reclassification

Goal: incorporate the user's manual drops in `research/manual/` per the research-pipeline skill's Phase 0 discipline.

**Wave 1 (#18).** Six manual fetches; mixed outcomes:
- ✅ **every.to / Klaassen** — full primary-source unlock via browser cookies. Report 03 gained a new "Cora playbook" section with five use cases, the five-step compounding playbook, the $400/$400k cost framing, and three new notable-quotes entries.
- ⚠️ **Two Lenny URLs** — paywall persisted (cookies present but not paid-subscriber cookies). Stubs truncate at "This post is for paid subscribers." Recorded as the **third failed retrieval route**.
- ❌ **Three Cloudflare URLs** (el-kaim Dark Factory + welkaim ×2) — JS-challenge stubs only. **Cookies don't bypass JS challenges.** Path B required.

**Wave 2 (#19).** Two parallel subagents:
- **Dark Factory primary source** unlocked via Path B (Save Page As from a real browser that had solved the Cloudflare challenge). 41 KB text export. Report 07 transitioned from *reconstructed* to *primary-source-anchored*: 11 new top-level sections, 22 verbatim quotes replacing reconstructions, and **four refutations** of prior reconstructed claims (StrongDM-vs-El-Kaim attribution; two phase changes not one; Gas Town as attribution layer not DOT runner; Beads-not-Dolt). PLAN §11.12 RESOLVED.
- **Round 4 catalog** generated from the 7-chapter El Kaim book in `research/manual/multi/`. Four parallelizable cluster briefs A/B/C/D added as PLAN.md §12.

And the **Lenny reclassification**, which is the lesson L-3 below:
- After three failed retrieval routes for the Lenny "interview body," the user supplied a round-2 note saying simply *"just a video."*
- The URL **has no text body**. The paywall stub is an editorial-summary placeholder, not a paywalled article.
- Recovery requires a YouTube transcript extraction service, not a Lenny paid subscription.
- The 10–30 PRs/day and 10–15 parallel-sessions Cherny numbers in report 06 are now correctly flagged as **un-primary-sourced and unrecoverable from this URL**.

Three retrieval routes had been chasing a body that didn't exist. That's a P0 lesson for the research-pipeline skill (see L-3).

### Phase 9 — Building the fanout skill (PR #22)

Goal: the `parallel-subagent-fanout` skill installed in PR #14 needed operational guidance and a hardened convention before its first real exercise.

Three additions to the SKILL.md and the spec README:
- **`isolation: "worktree"` is mandatory** on every Agent call in fanout dispatches. The concrete code example was added inline. Anti-pattern documented: dispatching without isolation contaminates branches and races on git operations across subagents that share a workdir.
- **Double-dash branch naming** (`feature--sub-N`). Slashes in git refs collide with branch hierarchies (e.g., `feature/sub-1` becomes ambiguous with a `feature` branch).
- **Plan-order merge** — deterministic run reports require merging in decomposition order, not completion order, so re-runs and audits produce identical artifacts.
- **User-approval gate** on the decomposition plan, before any repo modifications.

This PR was a quiet 188-line skill update. The 26-subagent fanout in PR #25 — 19 minutes later — was its first real load test.

### Phase 10 — The 26-subagent fanout (PR #25)

Goal: drain Rounds 2, 3, 4, and 5 of the PLAN.md catalog in parallel via the just-released `parallel-subagent-fanout` skill.

- 26 subtasks decomposed across R2/R3/R4/R5 brief lists in PLAN.md §10/§11/§12/§13.
- Each subagent ran in its own worktree on a `claude/parallelize-with-subagents-SO0nR--sub-N` branch.
- **68 commits** total: one initialization commit + 26 per-subtask result commits + cross-cutting consolidation commits + bookkeeping (INDEX, blocked-urls, follow-up filings).
- **+5,908 / −2 lines across 32 files** in the final merged form.
- Wall time from PR-open (05:58Z) to merge (12:48Z): **~6 h 50 m** — the largest single-PR window in the repo's history at this point.

The fanout exercise was both an outcome and an operational stress test. It validated:
- `isolation: "worktree"` actually prevented git contamination at N=26 (zero git-ref collisions in 68 commits).
- Plan-order merge produced a clean run report.
- `state.json` + `report.md` persistence let a long-running fanout survive any single-subagent failure.

It also surfaced (per surrounding retros) that the orchestrator carries the cleanup burden — subagents leave intermediate files (`.extracted.*`, etc.) that the orchestrator must sweep before commit. That observation lived dormant until retro 2026-05-13-02 codified it as the `subagent-cleanup-sweep` skill.

### Metrics

| Metric | Value |
|---|---|
| PRs opened in window | 13 (#11, #12, #13, #14, #15, #16, #17, #18, #19, #20, #21, #22, #25) |
| PRs merged | 12 (all but #13, which was closed in favor of folding into #14) |
| Net lines changed across window | ~+13,500 / ~−45,000 (PR #12 alone deleted 39,243 lines of cached source files) |
| New skills authored or installed | 7 (`research-pipeline`, `always-commit-skill-to-repo`, `in-flight-workflow-tracking`, `self-retrospective` rewrite, `parallel-subagent-fanout`, `subagent-prompting`, `adr`) |
| New ADRs landed | 1 (`docs/adr/0001-fetch-blocked-urls-mechanism.md`) |
| PLAN.md version bumps | 4 (v0.2 → v0.3 → v0.4 → v0.5 → v0.6) |
| New PLAN.md sections | 5 (§5.1 Workflow tooling, §5.2 External-synthesis artifacts, §11 Round 3 follow-ups, §12 Round 4 El Kaim book, §13 Round 5 external-synthesis harvest) |
| Reports updated with primary-source content | 2 (report 03 — Klaassen "Cora playbook"; report 07 — Dark Factory full revision) |
| Reconstructed-claim refutations caught by primary source | 4 (StrongDM-charter attribution; one-vs-two phase changes; Gas Town role; Beads/Dolt) |
| Long-running paywall theories refuted | 1 (Lenny URLs are video-only — no text body to retrieve) |
| Subagents dispatched in PR #25 | 26 (single fanout, plan-order merge) |
| PR #25 commit count | 68 |
| PR #25 wall-time open→merge | ~6 h 50 m |
| Operational mishaps | 2 (PR #13 fresh-branch redundancy; chasing a nonexistent Lenny text body across 3 retrieval routes) |

---

## Part 2 — skills summary

Most skills the session would have benefited from were authored *in* the session — `research-pipeline`, `parallel-subagent-fanout`, `adr`, the rewritten `self-retrospective`. Three additional candidates surface from this window that were **not** captured at the time:

| Skill | Priority | Approx scope | Why earned |
|---|---|---|---|
| `manual-fetch-triage` | medium | quarter-day | The three retrieval-route failure modes (cookies-defeat-paywall, cookies-don't-defeat-Cloudflare-JS, URL-has-no-text-body) deserve a single triage checklist before any manual fetch is dispatched. Would have surfaced the Lenny video-only finding on first inspection of the 5.5 KB body. |
| `path-b-source-recovery` | medium | quarter-day | "Save Page As from a real browser session" is the canonical defeat for Cloudflare JS challenges. Demonstrated by the Dark Factory unlock in PR #19. Currently lives only in PLAN.md §6 as a paragraph; deserves a skill so future agents know to reach for it rather than re-attempting cookie fetches. |
| `plan-md-section-curator` | low | quarter-day | Three consolidations (#17, #20, #21) wrote new PLAN.md sections by hand. The pattern is reliable: add §N, bump version, add changelog line, ensure all skill-referenced files are catalogued, ensure all non-canonical files are listed in the "does NOT belong on main" sidebar. Mechanical enough to codify. |

No spec files written for these — synthetic-retro scope. Author from this section if the user decides any are worth carrying forward.

---

## Part 3 — agents-file suggestions

Two rules earn their place from this window:

### Rule 1 — Push follow-up commits to the in-flight branch; don't open a duplicate PR.

> When work on a topic is already in flight on a `claude/*` branch, additional commits in the same topic should be pushed to that branch as new commits — not opened as a fresh-branch PR. Open a new branch only when the new work is genuinely independent.

**Why it earns its place:** PR #13 opened a fresh branch (`claude/import-ai-skills`) for skill imports that belonged on the in-flight `claude/followup-and-fetch-skill` branch. PR #13 was closed unmerged, the commits were re-applied on the in-flight branch, and PR #14 merged the combined set. Net: one wasted PR, one duplicate branch, ~10 minutes of recovery time. The rule was already codified in PR #16's always-commit-skill update; lifting it to agents-file would surface it earlier.

### Rule 2 — Recognize the three "fetch failed but HTTP 200" body fingerprints.

> An HTTP 200 response is not a successful fetch. Inspect the body. Three failure fingerprints to recognize:
>
> 1. **Cloudflare JS challenge** — 5–6 KB body containing "Just a moment…" or "Attention Required". Cookies don't defeat this. Use Path B (Save Page As from a real browser).
> 2. **Paywall stub** — body truncates at "This post is for paid subscribers" or similar. May not be defeatable from cookies if the cookies aren't paid-subscriber cookies. Try once; record as a failed route.
> 3. **Video-only URL with editorial placeholder** — the URL is a podcast/video landing page; the visible text is an editorial summary, not the content. Recovery requires a transcript service, not a paywall bypass.

**Why it earns its place:** The Lenny URLs cost three retrieval rounds (Wayback, cookies, then a third pass) before the user clarified "just a video." Cataloguing the three fingerprints would have produced the right verdict on first inspection of the 5.5 KB body in PR #18.

---

## Part 4 — proposed ADRs

Architectural decisions made or reinforced in this window. **Titles + rationale only — no specs.** Author via the `adr` skill if the user decides any are worth recording.

- **`research/PLAN.md` is the single canonical "next steps" document; folded artifacts go in, parallels do not stay out** — Settled across PRs #17 (followup.md folded), #20 (workflow tooling catalogued), #21 (external-synthesis filing pattern). The pattern has held since.

- **External synthesis artifacts (ChatGPT deep research, etc.) live in `research/external-syntheses/<dated-dir>/`, not numbered `research/NN-*.md`** — Established in PR #21 to avoid collapsing two distinct things (the report-13 slot is reserved for our own Round-2 synthesis). The dated subdirectory + `report.md` + `sources.md` + `README.md` orientation file is the canonical shape.

- **`isolation: "worktree"` is mandatory on every Agent call in a fanout dispatch** — Established in PR #22 and validated at N=26 in PR #25. Zero git-ref collisions across 68 commits.

- **Double-dash branch naming (`feature--sub-N`) for fanout sub-branches** — Established in PR #22 to avoid git-ref collisions that slash-separators would produce.

- **Path B (Save Page As from a real browser session that has solved the JS challenge) is the canonical recovery for Cloudflare-JS-challenged primary sources** — Validated by the Dark Factory unlock in PR #19. Cookies do not defeat JS challenges.

- **Lenny podcast URLs are video-only landings with editorial-summary placeholders; the "interview body" does not exist as text at those URLs** — Discovered the hard way in PRs #18 and #19. Record so the next session doesn't burn three retrieval rounds re-discovering it.

- **PLAN.md §5.1 catalogues every workflow-tooling file; §5.2 catalogues external-synthesis artifacts; the sidebar names what does NOT belong on main** — Folding rule established in PR #20 and reinforced in #21. Future workflow files either get a §5.1/§5.2 entry or get explicitly named in the sidebar.

- **The `self-retrospective` skill writes to `retrospective/YYYY-MM-DD-NN.md` (flat — no `/report/` segment) with a sibling spec directory** — Final form after PR #14 → PR #15 path-flatten.

---

## Self-reflection — what I'd do differently

Three honest assessments of the work in this window:

**1. The PR #13 mistake was avoidable.** Opening a fresh branch when work was already in flight on a related branch reflected not thinking through where the new commits should land. The cost was small (~10 minutes recovery + one closed PR) but the lesson was load-bearing enough that PR #16 was written explicitly to prevent recurrence. A 30-second pause to ask "is this independent or related?" would have saved the mistake.

**2. The Lenny "interview body" cost three retrieval rounds.** The 5.5 KB paywall-stub body was inspected three times and triaged three different ways (Wayback eligible, paywall, paywall) before the user's "just a video" clarification surfaced the truth. **The body was actually telling me this on first inspection** — an editorial summary plus a reference list is not a paywalled article. A "fingerprint the body before classifying the failure" discipline (Rule 2 above) would have surfaced the correct verdict in PR #18 rather than PR #19.

**3. The 26-subagent fanout in PR #25 was the right call but barely.** The `parallel-subagent-fanout` skill was authored in PR #22 and exercised at N=26 in PR #25, 19 minutes later. That's a substantial scale jump for a first exercise. It worked — the worktree isolation held, plan-order merge produced a clean report — but a smaller validation (say, N=4 or N=8) before the big run would have been the lower-risk path. The 6 h 50 m PR window is also a reminder that very large fanouts are batchy: incremental progress is invisible until the merge happens.

**Implicit meta-lesson.** Retro 2026-05-11-01 was authored mid-session. The session kept going for **~9 more hours** after retro 1 was written, producing 11 more PRs and a 26-subagent fanout. **Retrospectives should be written at session boundaries, not at convenient checkpoints.** When retro 1 was authored the session was barely halfway through. This file exists, three days later, because of that timing mismatch.

---

*End of synthetic retrospective `2026-05-11-02`. Authored 2026-05-14 from PR descriptions and surrounding retros; not contemporaneous with the work it covers.*
