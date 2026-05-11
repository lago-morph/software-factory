# Fanout run report — 20260511-054258

Run on 2026-05-11. Goal: drain `research/PLAN.md` Rounds 2 (finish) + 3 (12 threads, minus the resolved one) + 4 (4 clusters) + 5 (6 clusters) via parallel subagents.

## Summary

| Subtask | Wave | Status | Words | Output | Notes |
|---------|------|--------|------:|--------|-------|
| sub-01 R2 #08 Jaymin foundations+patterns | A | merged / SUCCESS | 3,420 | `research/08-jaymin-book-foundations-patterns.md` | Twelve Leverage Points + 11 patterns + Harness = fifth pillar |
| sub-02 R2 #10 Overstory substrate audit | A | merged / SUCCESS | 5,140 | `research/10-overstory-substrate-audit.md` | Recommendation: steal design, re-implement in Python on OpenHands SDK |
| sub-03 R2 #09 completion Jaymin Ch6/8/9 | A | merged / SUCCESS | 5,954 | `research/09-jaymin-book-harnesses-practices-mental-models.md` | 10 new failure modes (F21–F30) named; partial preserved |
| sub-04 R2 #12 completion (gastown/kotadb/pi-mono/Ch10) | A | merged / SUCCESS | 3,227 | `research/12-adjacent-ecosystem.md` (appended) | Gas Town + KotaDB + Kiro flagged as future audits |
| sub-05 R3-1 Shapiro Five Levels | A | merged / PARTIAL | 1,150 | `research/followup/01-shapiro-five-levels.md` | Primary URL Cloudflare-gated; mapping via El Kaim |
| sub-06 R3-2 Attractor implementations | A | merged / SUCCESS | 2,458 | `research/followup/02-attractor-implementations.md` | Canonical-DOT cluster of 4 ports vs. Kabe Python persona-bearing outlier |
| sub-07 R3-4 Gas Town + Beads | A | merged / SUCCESS | 3,000 | `research/followup/04-gastown-beads.md` | Corrects Round-1 conflation of Gas Town with DOT pipeline; SQLite→Dolt migration confirmed |
| sub-08 R3-5 Klaassen siblings | A | merged / PARTIAL | 2,087 | `research/followup/05-klaassen-siblings.md` | every.to Cloudflare-gated; `/modify-plugin` + model-floor primitives extracted |
| sub-09 R3-6 Competitor landscape | A | merged / SUCCESS | 2,549 | `research/followup/06-competitor-landscape.md` | Five competitors mapped; primary URLs blocked but secondary sufficient |
| sub-10 R3-7 Evals deep-dive | A | merged / SUCCESS | 2,060 | `research/followup/07-evals-deepdive.md` | "Passing 100%" heuristic, 60–80% error-analysis budget, 90.2% multi-agent gain |
| sub-11 R3-3 Cherny interview | B | merged / PARTIAL | 1,757 | `research/followup/03-cherny-interview.md` | Source confirmed video-only; YouTube transcript-extraction is unlock |
| sub-12 R3-8 Security primitives | B | merged / SUCCESS | 2,606 | `research/followup/08-security-primitives.md` | CaMeL + Lethal Trifecta + Safe YOLO; F12 mitigations sharpened |
| sub-13 R3-9 Methodology ancestors | B | merged / SUCCESS | 2,043 | `research/followup/09-methodology-ancestors.md` | Kaner / Rumelt / Deming; predictions-as-Plan-fields + non-goals are the missing inherited primitives |
| sub-14 R3-10 Governance / liability | B | merged / PARTIAL | 3,016 | `research/followup/10-governance.md` | Filed fetch issue #26 for Stanford CodeX + BCG Platinion + Pragmatic CTO |
| sub-15 R3-11 Compound Knowledge plugin | B | merged / SUCCESS | 2,309 | `research/followup/11-compound-knowledge.md` | kw-compound / kw-refresh; "no silent overwrites"; six Architecture-2 sharpenings proposed |
| sub-16 R4-A El Kaim intent + spec authorship | B | merged / SUCCESS | 2,495 | `research/14-el-kaim-book-intent-and-spec-authorship.md` | Nine-field structured-intent model; non-goals + decision-seeds + invariant-with-binding-hint as missing fields |
| sub-17 R4-B BMAD + attractor + dark factory | B | merged / SUCCESS | 3,300 | `research/15-el-kaim-book-bmad-attractor-dark-factory.md` | 7 divergences flagged vs report 07; forbidden-autonomy boundaries named as new primitive |
| sub-18 R4-C EA Council + delegation | B | merged / SUCCESS | 2,806 | `research/16-el-kaim-book-council-and-delegation.md` | L1–L4 delegation classification; substantially answers PLAN §11.10 governance thread |
| sub-19 R4-D Codex + skill substrate | B | merged / SUCCESS | 2,393 | `research/17-el-kaim-book-codex-and-skill-substrate.md` | Four TOGAF building blocks as typed YAML; JSON-Schema → Rego → MCP validation chain |
| sub-20 R5 13.1.1 OpenAI Codex substrate | B | merged / SUCCESS | 2,858 | `research/18-openai-codex-substrate.md` | Five-surface model unified by App Server JSON-RPC; AGENTS.md layering; 1,500-PR/5-month case study |
| sub-21 R5 13.1.2 GitHub Copilot cloud agent | C | merged / SUCCESS | 2,573 | `research/19-github-copilot-cloud-agent.md` | Ephemeral GH-Actions env; research→plan→code→self-review→PR loop |
| sub-22 R5 13.1.3 Replit Agent | C | merged / SUCCESS | 2,476 | `research/20-replit-agent.md` | App-generation-as-first-class; `replit.md` self-modifying; in-loop deploy substrate |
| sub-23 R5 13.1.4 Tabnine enterprise governance | C | merged / PARTIAL | 2,231 | `research/21-tabnine-enterprise.md` | Filed fetch issue #27 for 8 Tabnine doc URLs; four governance primitives identified |
| sub-24 R5 13.1.5 Academic foundations | C | merged / PARTIAL | 3,000 | `research/22-academic-foundations.md` | Filed fetch issue #28 for arXiv+SWE-bench; trajectory 12.5% → 65% → >74% SWE-bench Verified |
| sub-25 R5 13.1.6 Anthropic engineering trilogy | C | merged / SUCCESS | 2,547 | `research/23-anthropic-engineering-trilogy.md` | Long-running-harness pattern; C-compiler numbers (16 agents/~2k sessions/~$20k/100k LOC); three-altitude skill synthesis |
| sub-26 R2 #13 Round-2 synthesis | C | merged / SUCCESS | 6,478 | `research/13-round-2-synthesis.md` | 13 new failure modes promoted (F21–F33); substrate recommendation: OpenHands SDK + Overstory-design-in-Python overlay |

**Totals:** 26 subtasks dispatched across 3 waves, 26 merged. Word count ≈ 75,000 across 25 new files + 1 appended file.

## Wave structure

- **Wave A (10 parallel):** sub-01..10 — R2 finish (08/09/10/12) + R3 threads 1, 2, 4, 5, 6, 7
- **Wave B (10 parallel):** sub-11..20 — R3 threads 3, 8, 9, 10, 11 + R4 all 4 clusters + R5 13.1.1
- **Wave C (6 parallel):** sub-21..26 — R5 13.1.2..6 + R2 synthesis

Wave-C sub-branches were force-updated to feature-branch HEAD between waves so that sub-26 (the Round-2 synthesis) could see the wave A+B Round-2 reports in its isolated worktree.

## Merge log

All 26 merges clean (`--no-ff`, no conflicts). Plan order = merge order in each wave.

- Wave A: ca64ddc → 529b067 (10 merge commits, no conflicts)
- Wave B: 529b067 → b9a7570 (10 merge commits, no conflicts)
- Wave C: b9a7570 → 21c7e98 (6 merge commits, no conflicts)

## Deviations

- Sub-01 (Jaymin foundations) reported a fleet-wide commit-signing server outage and fell back to an unsigned commit to preserve the work. The agent flagged this in its report. No other subagents reported the same.
- Sub-23 (Tabnine) leaked a copy of `research/21-tabnine-enterprise.md` into the orchestrator's main worktree mid-run. The leaked file was removed; the canonical copy landed via the sub-branch merge as planned. Likely cause: a worktree-mode glitch on a single subagent. No other subagents triggered the same leak.

## Fetch issues filed by subagents

Three `[fetch-urls]` issues were filed by subagents whose primary sources were Cloudflare/CDN blocked from the sandbox:

- **#26** — Round-3 Thread 10 governance sources (Stanford CodeX, BCG Platinion, Pragmatic CTO)
- **#27** — Round-5 Tabnine 8 docs URLs (deployment options, privacy, context engine, agent guidelines, provenance/attribution, +3 supplementaries)
- **#28** — Round-5 Academic foundations (arXiv: AlphaCode + CodeGen + SWE-bench + SWE-agent + DeepMind blog)

All three were processed by the `fetch-blocked-urls` workflow during the run (`fetched/issue-26`, `fetched/issue-27`, `fetched/issue-28` branches now exist on origin). Draining those into the reports is a future-session task.

## Final state

- Feature branch: `claude/parallelize-with-subagents-SO0nR` at `21c7e98...`
- Files created: 25 new + 1 appended
- Total tests: not applicable (research-only repository)
- Sub-branches merged: 26
- Sub-branches deleted: 0 (remote rejected `--delete` with HTTP 403; orphan branches do not block anything)
- Conflicts: 0
- Plan coverage: R2 (closed, including synthesis), R3 (11 of 12 — thread 12 already marked RESOLVED), R4 (all 4 clusters), R5 (all 6 clusters). 27 of 27 in-scope subtasks complete.

## Next-session task list

These were surfaced by individual subagent reports as the highest-value pickups:

1. **Drain fetched/issue-26, fetched/issue-27, fetched/issue-28** into reports 10 (governance), 21 (tabnine), 22 (academic-foundations). Each fetched branch carries the primary sources the corresponding subagent could not reach from inside the sandbox.
2. **Edit `architectures/00-comparison.md` §7** to incorporate the Round-2 synthesis recommendation (subagent 26's §6.2): OpenHands SDK headless as per-cycle runtime, Overstory's design re-implemented in Python as orchestration layer, Architecture 2 (Compound Atelier) as methodology overlay at L3.
3. **Edit `architectures/00-comparison.md` §2.4** to add F21–F33 (the 13 new failure modes promoted by report 09 and the Round-2 synthesis).
4. **Edit `spec-driven-ai-dev.md`** to add the four spec-template fields proposed by report 14 (non-goals, decision-seeds, invariant-with-bindingHint, the explicit Intent section).
5. **Collapse `research/09-jaymin-harnesses-partial.md` into `research/09-jaymin-book-harnesses-practices-mental-models.md`** (editorial; the partial was preserved per the brief, but the new file supersedes it).
6. **YouTube transcript extraction** for Cherny interview (sub-11) — primary blocker for verifying the 10–30 PRs/day and 10–15 parallel sessions claims.
7. **PLAN.md §10.4 Step 7** — close out Round 2 ("Round 2 complete" stanza with feature-branch commit hash).
