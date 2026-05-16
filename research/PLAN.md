# Software Factory Research — PLAN.md

**Version:** v0.12 (2026-05-16)
**Status:** Research phase is at "primary-source complete" by every meaningful measure. **26 numbered reports** + 12 follow-up reports + 5 architecture docs + 1 methodology doc + 1 research → action plan (`research-plan.md`). All filed fetch-urls issues are drained on main (issues #41/#42 still show OPEN on GitHub but their work landed in PR #44 — housekeeping closure pending). **Round-9 manual drain landed 2026-05-16** — opens a new methodology-discipline thread anchored in RE/SE primary sources (EARS, INCOSE TP-2020-002-06, INCOSE GtWR v4, INCOSE Complexity Primer, AFIS *Requirements and Architecture within Modelling Context*) and in academic LLM+RE empirical literature (Norheim et al. *Design Science* 2024, Yang et al. arXiv:2505.13360, Larbi et al. arXiv:2507.20439). New reports **25** (requirements-engineering-foundations) and **26** (prompt-underspecification-academic); report 12 (adjacent-ecosystem) extended with Kiro deep-spec / from-copilots-to-coworkers material. **Four new failure-mode proposals** (F36–F39 from report 25; F36–F37 from report 26 — numbering collision; lead-agent triage required). Forward work is still **decision work**, not fetch work: three curated human-review tasks pending; **13 unbuilt skill specs / 45 AGENTS suggestions / 26 proposed ADRs across five retrospectives** queued; `research-plan.md` proposes a v3 architecture collapse that requires a user decision. Only outstanding primary-source gap: ~7 URLs (5 confirmed Path-B-only; 2 still eligible for retry via action or Wayback).

**Earlier versions:** v0.1–v0.7 lived as accreted Round-by-Round sections (§§11–17 below as Archive). v0.8 rewrites the live status at the top and compresses the per-round detail; v0.9 records the pt-2 cherry-pick recovery and updates §3.1 from bottleneck → RESOLVED; v0.10 records rounds 7–8 drains (Shapiro canonical, El Kaim post-index + Chapter 9, platform.claude.com Skills overview Path B, issues #41/#42, Lenny × Willison full transcript), the four retrospectives that landed 2026-05-13/14 (which v0.9's §3.4 did not yet enumerate), and `research-plan.md`. v0.11 records the Cherny full-transcript drain (2026-05-14) that closes the last in-flight primary-source gap from the rounds 1–8 pipeline. **v0.12 records the Round-9 manual drain (2026-05-16)** — opens the RE/SE-methodology + LLM-prompt-underspecification thread as reports 25 + 26, extends report 12 with Kiro deep-spec material, surfaces 4–6 candidate failure modes (F36–F39 with internal numbering collision between the two reports). The audit trail is preserved in the archive sections; the live work is in §§1–6.

---

## 1. Current state (TL;DR)

**Done:**
- **Round 1** — 7 reports (`research/01-07-*`) + initial synthesis (`research/00-synthesis.md`).
- **Round 2** — 5 reports + synthesis (`research/08-12-*`, `research/13-round-2-synthesis.md`). 13 new failure modes (F21–F33) catalogued; never folded into `architectures/00-comparison.md` §2.4.
- **Round 3** — 12 follow-up threads (Threads 1–11 → `research/followup/01-11-*`; Thread 12 *Dark Factory via archive.org* was RESOLVED without a new file when the article was retrieved via Path B and folded into `research/07-dark-factory.md`). A separate post-Round-3 effort produced `research/followup/12-brier-pace-layers.md` plus primary-source upgrades to followup/05 and followup/07 — these were on a side branch only until the 2026-05-13 cherry-pick (see §3.1).
- **Round 4** — 4 reports off the El Kaim enterprise-architecture book (`research/14-17-*`). The book chapters are now at `reference-only/el-kaim-book/`.
- **Round 5** — 6 reports off counterfactual harvest against a ChatGPT deep-research artifact (`research/18-23-*`). The artifact is at `reference-only/chatgpt-deep-research-2026-05-11/`.
- **Round 6** — 26-subtask parallel-fanout night run on 2026-05-11 (`harness/runs/20260511-054258/`) that produced most of the above. One follow-up "pt-2" wave (3 subagents) was originally orphaned on a side branch but was recovered onto main via the 2026-05-13 cherry-pick (see §3.1).
- **Session 2026-05-13 — three drain cycles** — editorial collapse of the 09 partial into the unified report; closed 7 drained fetch-urls issues; filed 3 new batched fetch-urls issues (#29 / #30 / #31), all drained same-day; reorganized source files into `/reference-only/`. **Retrospective 2026-05-13-01** authored (4 skills, 9 AGENTS suggestions, 5 ADRs — see §3.4). **Round-7 follow-up** (issue #36 + manual drops): Shapiro canonical Five Levels post drained (8 El Kaim-vs-Shapiro discrepancies documented; cross-corpus flags in §6.1); El Kaim post-index Path B'd → 10-post Medium cluster logged as future research; El Kaim Chapter 9 manual drain → **new report 24 (el-kaim-book-product-line-variability)**; failure mode **F35 — Federation-as-Family Drift** promoted; `platform.claude.com/.../agent-skills/overview` Path B'd → report 23 attribution audit closed for overview, two SPA pages still pending. F34 (cross-layer drift) promoted by Brier pace-layers drain.
- **Session 2026-05-14 — round-8 drains + Lenny × Willison** — Issues #41 and #42 drained (PR #44): all 13 Replit URLs primary-anchored (report 20 partial → primary-anchored); 5/7 `developers.openai.com/codex/*` URLs primary-anchored (report 18 stays partial due to the 3 `openai.com/index/*` URLs returning Cloudflare JS challenges to the action runner); 6/6 GitHub Copilot canonical re-finds primary-anchored (report 19 partial → primary-anchored; new §3.1 on Copilot Spaces); **CaMeL paper body recovered via arXiv `/e-print/` LaTeX-tarball route** (followup/08 §3 expanded from 7 to ~15 subsections, paper-body-anchored). Lenny × Willison **full ~90-min transcript** drained (PR #43): reports 05 and 06 flipped to FULL (Challenger-disaster prediction, lethal-trifecta walkthrough with 97%-failing-grade doctrine, OpenClaw thesis, end-of-2026 prediction). Three retrospectives landed: 2026-05-13-02, 2026-05-14-01, 2026-05-14-02. `research-plan.md` filed (PR #46) proposing the unified-synthesis + v3-single-architecture collapse.
- **Session 2026-05-16 — Round-9 manual drain (RE/SE + LLM-prompt-underspec + Kiro)** — User dropped 11 files into `research/manual/`: 5 RE/SE primary-methodology PDFs/MHTML (EARS, INCOSE TP-2020-002-06, INCOSE GtWR v4 summary sheet, INCOSE Complexity Primer, AFIS *Requirements and Architecture within Modelling Context*); 3 academic LLM+RE papers (Norheim et al. Cambridge / *Design Science* 2024, Yang et al. arXiv:2505.13360v3 "What Prompts Don't Say", Larbi et al. arXiv:2507.20439v1 "When Prompts Go Wrong"); 2 Kiro blog posts (deep-spec-analysis + from-copilots-to-coworkers); 1 redundant Cherny YouTube transcript (different transcription of the already-drained `reference-only/lenny-podcast-transcripts/cherny-head-of-claude-code-full.txt` — deleted without drain). Drained in parallel via three subagents: subagent A → new **`research/25-requirements-engineering-foundations.md`** (5,572 words; anchors El Kaim's 9-field discipline to GtWR C1–C15 one-to-one mapping; proposes F36 vocabulary-lint debt, F37 point-spec/region-mismatch, F38 architecture/specification confusion, F39 Ashby-deficient probabilistic guard); subagent B → new **`research/26-prompt-underspecification-academic.md`** (6,187 words; first academic-empirical anchor for the corpus' spec→code-gap framing; proposes F36 instruction-following ceiling, F37 silent contradictory-prompt collapse — numbering collision with report 25's F36/F37, see §3.6); subagent C → updated `research/12-adjacent-ecosystem.md` §2.5 (+1,150 words; Kiro "deep spec analysis" mechanic, five generic spec properties, four bug classes; latency-vs-autonomy framing flip; "regeneration replacing repair" research direction in tension with audit-trail discipline). All 10 substantive sources marked ✅ in their respective reports' Sources-reviewed tables. `research/manual/` now contains only `README.md`. **Surprises:** El Kaim's 9-field intent block is one-to-one with INCOSE GtWR C1–C15 (the corpus has been treating El Kaim as novel discipline; best read as domain instantiation); Yang et al.'s 41.1% "model guesses correctly without spec" + 65.2% "requirements are often redundant" qualify the corpus' spec-maximalist tendency; Larbi et al.'s RIR 89% on contradictory HumanEval is a stronger empirical anchor for Willison's "97% is a failing grade" doctrine than expected; AFIS strategy-3 (models-as-specification) names what reports 14/22/24 have been implicitly converging on.
- **Session 2026-05-14 (later) — Lenny × Cherny full transcript drain** — User dropped the full ~90-min Cherny YouTube transcript at `research/manual/lenny-Head of Claude Code.txt`. Drained in parallel via two subagents: `research/followup/03-cherny-interview.md` flipped 🟡 → ✅ FULL (219 → 365 lines, ~30 new verbatim quotes across 9 new H2 sections including 4-layer AI-product principles, 3-layer safety framework, "multi-cladding" Anthropic-internal term, Cowork 10-day build anecdote, race-to-the-top open-source-sandbox principle, printing-press historical analog); `research/06-hn-and-lenny.md` updated with 6 net-new headline cross-references (five-agents-steady-state, 1/3-terminal+1/3-desktop+1/3-iOS surface split, 80% plan-mode workflow, less-capable-models-cost-more-tokens, $2B/$15B/$350B revenue/total/valuation triple, Sonnet-3.5→Opus-4.6 unattended-runtime 15s→30min). **Three claims downgraded to single-secondary-source confidence** because they were not mentioned in the 90-min transcript: `/loops`, `/batch`, "thousands of overnight agents". Source moved to `reference-only/lenny-podcast-transcripts/cherny-head-of-claude-code-full.txt`. Redundant arxiv 2503.18813 v1 HTML 404-stub deleted from `research/fetched/issue-36/` (e-print recovery in round 8 fully subsumes it).

**Open items live in:**
- §3 Bottlenecks — three live items: §3.2 curated human-review backlog (the original §14.4 tasks 2, 3, 5), §3.4 retrospective decisions (now five retrospectives cumulative), §3.5 YouTube-video-only Cherny claims. §3.3 fully RESOLVED (all filed issues drained).
- §4 Manual fetch instructions (prioritized).
- §5 Work remaining (priority order).
- `research-plan.md` (root) — the structural pivot proposal. Decision pending.

---

## 2. Repository layout (what lives where)

```
/architectures/         → 4 candidate methodologies + comparison
/docs/adr/              → ADR system (only ADR-0001 written; 26 more proposed across five retrospectives — see §3.4)
/harness/runs/          → Historical fanout-run records
/reference-only/        → Primary sources kept on disk for re-quoting
    el-kaim-book/       → 8 chapters of El Kaim's EA book (Ch 1–7 ~430 KB + Ch 9 manual drop)
    chatgpt-deep-research-2026-05-11/  → counterfactual synthesis artifact
    dark-factory-article.txt           → El Kaim Medium article (anchors report 07)
    brier-culture-of-ai-engineering.txt → Brier Every.to article (anchors `research/followup/12-brier-pace-layers.md`)
    every-my-ai-had-already-fixed.txt   → Klaassen Every.to article (anchors report 03)
    camel-paper/                       → CaMeL paper LaTeX source (main.tex, defns.tex, main.bbl) — recovered via arXiv /e-print/ in round-8, anchors `research/followup/08-security-primitives.md` §3
    lenny-podcast-transcripts/         → YouTube-transcribed Lenny podcasts (Willison full ~90-min ✅; Cherny full ~90-min ✅ 2026-05-14)
/research/              → 26 numbered reports + 12 followup reports + workflow tooling
    PLAN.md             → this file
    manual/             → transient drop zone for new manual fetches
    fetch-from-browser.sh, unfetched-sources.md, blocked-urls*.md → fetch-loop tooling
/retrospective/         → 5 retrospectives (2026-05-11-01, 2026-05-13-01, 2026-05-13-02, 2026-05-14-01, 2026-05-14-02) + sibling skill specs and AGENTS-suggestions files; see §3.4
/.claude/skills/        → 8 installed skills
/.github/               → fetch-blocked-urls action + scripts
spec-driven-ai-dev.md   → root-level methodology doc (pending update; see §3.2 task 2)
initial-sources.md      → original Round-1 seed list (frozen)
```

---

## 3. Bottlenecks

### 3.1 ~~Unmerged pt-2 drain work~~ **RESOLVED 2026-05-13 via cherry-pick onto `claude/recover-pt2-drain`**

PR #25 (merge commit `a67877f` on origin/main) was merged at 12:48 UTC on 2026-05-11. **18 minutes later** the same branch `origin/claude/parallelize-with-subagents-SO0nR` received the pt-2 drain — three subagents running in parallel — that had never reached main. The 2026-05-13 recovery branch `claude/recover-pt2-drain` cherry-picks the four relevant commits (`925da5b` sub-30 Brier, `2bf481b` sub-31 Klaassen, `ad565aa` sub-32 evals, `984c91d` recording commit) onto a fresh base off origin/main, resolves conflicts in favor of the cleanup-pass PLAN.md / unfetched-sources.md, and ports the path references that pointed at the now-moved `research/manual/<file>.txt` sources to their `/reference-only/` homes.

| Drain | Source (post-cleanup path) | Target report | Outcome |
|---|---|---|---|
| sub-30 | `reference-only/brier-culture-of-ai-engineering.txt` | **NEW** `research/followup/12-brier-pace-layers.md` (~2,571 words) | Brier's pace-layers pushback against the software-factory metaphor incorporated. Candidate failure mode **F34 — cross-layer drift** promoted. |
| sub-31 | fetched/issue-23 (3 Klaassen Every chain-of-thought articles) | `research/followup/05-klaassen-siblings.md` (2,330 → 5,731 words) | **4 reconstructed claims refuted** (article 3 author was Parrott, not Klaassen; fidelity tiers came from article 1, not 2; Puppeteer loop predicate was "match", not "pixel-perfect"; 4 mis-attributed claims). 15+ new primary-source claims. |
| sub-32 | fetched/issue-24 (Anthropic multi-agent-research-system + Husain/Shankar evals FAQ + 2 Simon Willison evals posts) | `research/followup/07-evals-deepdive.md` (2,150 → 4,511 words) | 2 reconstructed claims refuted (the ">90% expert agreement in 3 iterations" claim was not in the FAQ; multi-agent token tax is ~15×, not ~4×). 10 new primary-source claims. |

**Corpus-level lesson from pt-2:** `every.to/chain-of-thought/*`, `anthropic.com/engineering/`, `hamel.dev`, and `simonwillison.net` are all action-fetchable for publicly-visible bodies — the sandbox 403 does not propagate to GitHub-runner IPs. The `unfetched-sources.md` "Defer to user" label some of these previously carried was overcautious. **Recommendation:** before invoking a browser-cookie pass for any future URL, file a `[fetch-urls]` issue first; only escalate to Path B when the action also returns ❌. Now also captured in `research/unfetched-sources.md`.

The detailed per-subtask record lives at `harness/runs/20260511-054258/report-pt2.md`.

### 3.2 Curated human-review backlog (the original §14.4 tasks 2, 3, 5)

These three tasks were explicitly excluded from subagent dispatch in the original brief and are still outstanding:

| Task | What | Source of the proposed change | Risk if skipped |
|---|---|---|---|
| **Update `architectures/00-comparison.md`** | (a) Replace §7 with the substrate-stack recommendation from `research/13-round-2-synthesis.md` §6 (preserve original §7 as "§7 (Round 1)"). (b) Extend §2.4 with F21–F33 from report 09 + report 13 + G12/G13/G14 from drained report 10. | Round-2 synthesis report 13 §6; Round-2 failure-mode extension in report 09 §6 + report 13 §3 + governance drain in report 10 | The canonical comparison doc lags 4 rounds of synthesis. New readers see a 2025-era comparison; they don't see "harness" vocabulary, substrate-stack recommendation, or failure modes F21–F33. |
| **Update `spec-driven-ai-dev.md`** | Add 4 new fields proposed by Round-4 report 14 (cluster A): non-goals; decision-seeds; invariant-with-bindingHint; explicit Intent section. | `research/14-el-kaim-book-intent-and-spec-authorship.md` §"Recommendation" | Spec template ships without the El Kaim 9-field discipline. Generated specs continue to omit non-goals, which is the single highest-leverage of the four. |
| **Round 2 complete stanza** | Append a "Round 2 complete" stanza at the bottom of §11 (was §10 in v0.7) with the drain merge commit hash `423940f`. | Bookkeeping. | Audit trail is incomplete. |

### 3.3 ~~In-flight fetch-urls workflow~~ **RESOLVED 2026-05-13 — issues #29/#30/#31 + round-7 #36 + round-8 #41/#42 all drained**

Three batched fetch issues filed earlier in the session landed on origin as `fetched/issue-29`, `fetched/issue-30`, `fetched/issue-31`. A follow-up batched issue #36 (filed at the end of round 6) landed as `fetched/issue-36`. All four drained. Per-URL outcomes recorded in **`research/blocked-urls-round-6.md`** (issues #29/#30/#31) and **`research/blocked-urls-round-7.md`** (issue #36). Commit-level summary:

- **#29** (Anthropic × 5 + Hamel × 4 + Simon × 5 + arXiv + Shapiro × 2): 16/18 OK. Drained into `research/23-anthropic-engineering-trilogy.md` (5 Anthropic posts; **§8 new — Claude Code sandboxing**), `research/followup/07-evals-deepdive.md` (4 Hamel + 2 Simon), `research/followup/08-security-primitives.md` (3 Simon + arXiv CaMeL), `research/followup/01-shapiro-five-levels.md` (1 Shapiro companion post — canonical five-levels slug 404'd; correct slug now known). **Two 404s with corrected follow-up paths** (arxiv html v2, shapiro five-levels slug guess).
- **#30** (GitHub Copilot docs × 9): 3/9 OK. Drained into `research/19-github-copilot-cloud-agent.md`. **6 URLs returned 404** — GitHub docs reorganized; five report citations now flagged `[2026-05-13 404; pending re-anchor]`.
- **#31** (Devin / Factory / 8090 / Superconductor / Superpowers × 9): 6/9 OK. **Cloudflare blocks did NOT propagate to the runner.** Drained into `research/followup/06-competitor-landscape.md`. **Pricing model on Devin fully refuted** (current tiers Free/Pro $20/Max $200/Teams $80/Enterprise; no public ACU). **Factory adds "Droid Computers" primitive.** **Superconductor.io is wrong domain** — live product is at `.com`. 3 upstream 404s logged.
- **#36** (round-7 follow-ups: corrected Shapiro slug + arxiv pdf/v1 + superconductor.com + 3 platform.claude.com docs × 7): 5/7 OK by HTTP, but only 2 produced usable content. Drained into `research/followup/01-shapiro-five-levels.md` (Shapiro canonical post — **all 3 acknowledged gaps closed; Shapiro positions himself at Level 4 not Level 5; 8 El Kaim-vs-Shapiro discrepancies surfaced**) and `research/followup/06-competitor-landscape.md` §4 (Superconductor.com — the **multiplayer / "take the wheel" shared-agent-session** is its unique differentiator vs Devin/Factory/8090/Superpowers). Three failures: arxiv PDF (200 but binary), arxiv v1 html (404 same as v2), 3 `platform.claude.com` pages (200 but JS-SPA shells with `Loading...` placeholders). Recorded in `research/blocked-urls-round-7.md` with recovery routes; the platform.claude.com gap escalated to Path B.

**Cross-corpus lesson surfaced by this drain (now also in `research/blocked-urls-round-6.md`):** most of the prior "Cloudflare-only / paywall-only" classifications in `research/unfetched-sources.md` were **wrong** — the action runner reaches `simonwillison.net`, `hamel.dev`, `anthropic.com/engineering`, `arxiv.org/abs`, `danshapiro.com`, `devin.ai`, `factory.ai`, `8090.inc`, `blog.fsck.com` directly with HTTP 200. **Before invoking Path B (browser-cookie / Save Page As) for any future URL on these hosts, file a `[fetch-urls]` issue first.** This generalizes the pt-2 recommendation already in §3.1.

**Refutations surfaced (audit-trail-grade):**
- **Report 23:** Opus model is 4.5 not 4.6 (S12, S13, S15); testing tool is Puppeteer MCP not Playwright in S12; companion repo is `claude-quickstarts/autonomous-coding` not `cwc-long-running-agents`; "30–50 tokens per skill" not in S13; "Progressive disclosure that loads too eagerly defeats its purpose" not in S13; several "S13" security quotes are actually from `platform.claude.com/.../agent-skills/overview` (not yet drained — added to follow-up queue).
- **followup/08:** 3 "verbatim" trifecta-leg sentences were snippet-confabulated; "Any time a system combines access to private data..." quote not in primary (real line: "Any time you combine those three lethal ingredients together you are ripe for exploitation"); "first credible prompt injection defense" Willison quote was misquoted (load-bearing "doesn't just throw more AI" qualifier omitted); CaMeL attribution corrected to Google DeepMind + ETH Zürich; 77%/84% AgentDojo figures now exact.
- **followup/07:** prior issue-#24 removal of ">90% expert agreement in three iterations" REVERSED — the claim is real, source was wrong; it's from Hamel's llm-judge post (Honeycomb / Phillip Carter case study), not the FAQ.
- **followup/06:** Devin pricing structure entirely refuted (no public ACU pricing); Factory positioning softened; Superconductor wrong-domain. **Round-7 update:** Superconductor §4 fully re-anchored to .com; primary differentiator is the multiplayer "take the wheel" shared-agent-session primitive (no other vendor offers human-to-human handoff *during* an agent run); on-codebase agent benchmarking is a customer-exposed judge primitive; `oscardobsonbrown/superconductor` GitHub repo previously cited turns out to be a different project entirely (mis-attribution corrected).
- **followup/01 (round-7):** Shapiro positions himself at **Level 4** ("I'm here"), refuting prior corpus framings of him as a Level-5 practitioner. Eight El Kaim-vs-Shapiro discrepancies documented; the most consequential is that El Kaim's *"Nobody writes the code. Nobody reads the code."* L5 framing is NOT in Shapiro's canonical Five Levels post (it conflates the canonical post with the companion post). El Kaim added L4 "spec is the most valuable thing you produce" — Shapiro's actual L4 mentions "You craft skills (for Claude Code)" instead. **Cross-corpus propagation flags** logged in §6 below: report 07, StrongDM reports 01/02, anywhere Kilroy is called "Shapiro's Level-5 reference implementation."

**Follow-up fetch queue (next batched issue):** ~~Shapiro five-levels correct slug, arxiv 2503.18813 paper body, Superconductor.com, Cognition Devin announcement URL, 6 GitHub docs canonical URLs~~ — **all closed by rounds 6–8 drains**. Still queued (low priority, ~7 URLs total per §4.3): 2 `platform.claude.com` Agent Skills pages (best-practices + security; Path B only — JS-SPA shells); 3 `openai.com/index/*` URLs (Path B only — Cloudflare JS-challenged bodies); `pli.princeton.edu/.../swe-bench` (Wayback fallback may work); `docs.github.com/.../cloud-agent/risks-and-mitigations` (never tried via action; likely action-fetchable; would directly re-anchor a REFUTES on report 19). See `research/blocked-urls-round-8.md` §"Follow-ups" for the full actionable list.

#### Round-8 drain (issues #41 + #42) — added 2026-05-13

- **#41** (Replit + OpenAI Codex + SWE-bench × 24): 20/24 OK. Drained into `research/20-replit-agent.md` (all 13 R-* rows flipped 🟡 → ✅; 5+ refutations of community-mirror reconstructions) and `research/18-openai-codex-substrate.md` (5 `developers.openai.com/codex/*` rows flipped to ✅; 3 refutations: bwrap+seccomp not Landlock, no `on-failure` mode, AGENTS.md plain-concat not header-wrapped). 4 URLs failed Cloudflare (3 `openai.com/index/*` + 1 `pli.princeton.edu`); Path B remains the only route. Per-URL outcomes in `research/blocked-urls-round-8.md`.
- **#42** (GH Copilot canonical re-finds + arXiv CaMeL × 10): 6/6 GH Copilot canonical URLs ✅; 2 Copilot Workspace URLs documented sunset (folded into cloud-agent); arXiv CaMeL **paper body recovered via `/e-print/` LaTeX-tarball route** (gunzip|tar -xf manually; saved to `reference-only/camel-paper/`). Drained into `research/19-github-copilot-cloud-agent.md` (flipped 🟡 → ✅, 2 REFUTES on branch-restriction and CI-approval-gate framings, new §3.1 on Copilot Spaces) and `research/followup/08-security-primitives.md` (§3 expanded from 7 to ~15 subsections — PI-SEC formal game, NORMAL/STRICT modes, side-channel attacks, baseline comparison, overhead). **Lesson R8.1:** arXiv `/e-print/` is the gold-standard recovery route when html/v* 404s and pdf is binary.

### 3.4 Pending retrospective decisions

Five retrospectives now carry user-decision-pending artifacts. Cumulative backlog: **13 unbuilt skill specs / 45 AGENTS.md suggestions / 26 proposed ADRs**. The project still has no `AGENTS.md` file. Only the `adr` skill (from 2026-05-11-01) has been built; the other 13 are unbuilt.

| Retrospective | Skill specs (unbuilt) | AGENTS suggestions | Proposed ADRs |
|---|---|---|---|
| `2026-05-11-01` (original) | 3: `provenance-aware-reconstruction`, `sync-to-main-before-building`, `verbatim-fetch-via-curl` | 15 | 7 |
| `2026-05-13-01` (PLAN audit-pass cycle + pt-2 cherry-pick) | 4: `bulk-sed-audit`, `claim-verification`, `git-cherry-pick-resolution`, `large-restructure-self-audit` | 9 | 5 |
| `2026-05-13-02` (three drain cycles + cross-corpus audit) | 3: `cross-corpus-propagation`, `drain-audit`, `subagent-cleanup-sweep` | 10 | 5 |
| `2026-05-14-01` (Lenny full transcript + issues #41/#42 + stale-branch audit) | 3: `fetch-action-quality-check`, `arxiv-e-print-recovery`, `stale-branch-audit` | 7 | 4 |
| `2026-05-14-02` (short Q&A producing `research-plan.md`) | 0 | 4 | 5 |
| **Totals** | **13** | **45** | **26** |

ADR titles live in §"Part 4 — proposed ADRs" of each retrospective body. Skill specs live in the sibling directory of each retrospective (e.g., `retrospective/2026-05-14-01/`). AGENTS suggestions live in `retrospective/<date>/AGENTS-suggestions.md`.

### 3.5 YouTube-video-only content — ✅ RESOLVED 2026-05-14

The two Lenny URLs (Cherny + Willison interviews) turned out to be **video-only** with paywall-stub article landing pages. Both unlocked via manual YouTube transcript dropped into `research/manual/`.

**Status update 2026-05-14 (drain complete):** **BOTH sides are now ✅ FULL.** The Willison side was drained 2026-05-13 (see archive). The Cherny side was drained 2026-05-14: full ~90-min transcript at `reference-only/lenny-podcast-transcripts/cherny-head-of-claude-code-full.txt` (was previously partial 0–30 min). `research/followup/03-cherny-interview.md` flipped 🟡 → ✅; `research/06-hn-and-lenny.md` updated. **"5 Claudes" / "10–15 parallel sessions" architecture resolved** to *"five agents steady-state, split roughly thirds across terminal / desktop / iOS"* (the 10–15 ceiling figure remains secondary-only; "multi-cladding" emerged as the Anthropic-internal term for the parallel-desktop case). Three claims went the other way and were **downgraded** because the transcript does not mention them: `/loops`, `/batch`, "thousands of overnight agents" — kept in corpus as single-secondary-source.

### 3.6 Failure-mode numbering collision — F36/F37 dual-proposed by reports 25 and 26 (NEW 2026-05-16)

Reports 25 and 26, dispatched in parallel as part of the Round-9 manual drain, each independently proposed candidate failure modes F36 and F37. The two pairs name **different phenomena**:

| Number | Report 25 proposal (RE/SE) | Report 26 proposal (academic) |
|---|---|---|
| **F36** | **Vocabulary lint debt** — LLM-authored specs systematically violate INCOSE GtWR R7/R8/R9 (vague modifiers; ambiguous pronouns; superlatives). | **Instruction-following ceiling** — gpt-4o Pass@1 drops 98.7% → 85.0% as requirements specified grow 1 → 19 (Yang et al. arXiv:2505.13360v3 §3.4). Failure is *budget exhaustion* under a *complete* spec. |
| **F37** | **Point-spec / region-mismatch** — INCOSE Complexity Primer principle 12: when the *intended* outcome is a region in solution-space, expressing it as a point spec guarantees off-target instances. | **Silent contradictory-prompt collapse** — GPT-4 Pass@1 73.8% → 6.7% on contradictory HumanEval, RIR climbs to 89%; LLM-as-judge MCC ≤ 0.55 (Larbi et al. arXiv:2507.20439v1 §6.1–6.2). Broken code *runs*. |

All four are genuinely distinct phenomena and worth catalog inclusion. **Required triage:** lead agent (next session) decides numbering. Suggested approach: F36 → Yang-et-al. instruction-following ceiling (already has the strongest quantitative anchor); F37 → Larbi-et-al. silent contradictory-prompt collapse (paired with F36 by source paper); the two RE/SE proposals become F38 (vocabulary lint debt) and F39 (point-spec/region-mismatch). The two existing F38/F39 proposals in report 25 then shift to F40 (architecture/specification confusion in typed objects) and F41 (Ashby-deficient probabilistic guard — possibly a reframing of F33; flagged for separate call).

**Until triage, both reports' §"Implications" sections cite their own internal F36–F39 numbering.** Neither has been propagated into `research/00-synthesis.md` §4 or `research/13-round-2-synthesis.md` §3. No code paths or specs depend on the numbers; this is documentation-only cleanup.

---

## 4. Manual fetch instructions

Three priority tiers. Highest-leverage items first.

### 4.1 Highest priority — do these if you have time

**None today.** All filed `[fetch-urls]` issues (#29/#30/#31/#36/#41/#42) have been drained — see §3.3. The remaining ~7 outstanding URLs (5 confirmed Path-B-only; 2 still eligible for retry) are listed in §4.3 below.

### 4.2 Medium priority — primary-source unlock

**YouTube transcripts for the two Lenny URLs — BOTH ✅ DONE.**
- ~~`https://youtu.be/wc8FBhQtdsA` — Simon Willison on Lenny (AI state of the union)~~ — **DONE 2026-05-13.** Full ~90-min transcript dropped at `research/manual/lenny-An AI state of the union.txt`, drained into reports 05 and 06, then moved to `reference-only/lenny-podcast-transcripts/willison-ai-state-of-the-union-full.txt` (the earlier `first30min` partial was superseded and deleted).
- ~~`https://youtu.be/We7BZVKbCVw` — Boris Cherny on Lenny (head of Claude Code interview)~~ — **DONE 2026-05-14.** Full ~90-min transcript dropped at `research/manual/lenny-Head of Claude Code.txt`, drained into `research/followup/03-cherny-interview.md` (🟡 → ✅, ~30 new verbatim quotes, 9 new H2 sections) and `research/06-hn-and-lenny.md` (6 net-new headline cross-references), then moved to `reference-only/lenny-podcast-transcripts/cherny-head-of-claude-code-full.txt`.

**Both Lenny corpus claims now primary-source resolved:** "10–30 PRs/day" verbatim-anchored (Cherny minutes 0–30); "5 Claudes parallel" resolved (five agents steady-state, 1/3-terminal + 1/3-desktop + 1/3-iOS split; "10–15 sessions" ceiling figure remains secondary-only).

### 4.3 Low priority — background completeness

The remaining outstanding URLs after rounds 6–8 drains. Items 1a and 3 are confirmed Path-B-only; items 4 and 5 are still eligible for retry (via action or Wayback). All "nice to have"; the relevant reports are firm without these.

**1. ~~`medium.com/@welkaim/about` + `welkaim.medium.com/`~~** — **RESOLVED 2026-05-13** via Path B drop. Bio captured in `research/07-dark-factory.md` header; post-index revealed 10+ unread El Kaim posts (logged as future-research cluster, see "Future research" at the bottom of this file).

**1a. `platform.claude.com/docs/en/agent-skills/{best-practices,security}`** — overview was Path-B'd in round 7 and drained into `research/23-anthropic-engineering-trilogy.md` §3. The two remaining pages are still JS-SPA shells from action. **Path B only**: open each URL in a logged-in Console session, wait for the page to render, File → Save Page As → Web Page, Complete; drop the `.html` into `research/manual/`. ~2 URLs.

**2. ~~`docs.replit.com/*` + `blog.replit.com/*`~~** — **RESOLVED 2026-05-13/-14** via round-8 issue #41. All 13 R-* URLs primary-anchored; report 20 flipped 🟡 → ✅. The "Cloudflare-gated" classification turned out to be wrong (the round-6 lesson generalizes: old "blocked" tags age poorly).

**3. ~~`developers.openai.com/codex/*`~~ + `openai.com/index/{harness-engineering, unlocking-the-codex-harness, introducing-swe-bench-verified}`** — round-8 issue #41 drained 5/7 `developers.openai.com/codex/*` URLs successfully. The 3 `openai.com/index/*` URLs return Cloudflare JS-challenged bodies from the action (confirmed round 8); **Path B only.** Affects `research/18-openai-codex-substrate.md` (which remains 🟡 solely because of these 3 URLs).

**4. `pli.princeton.edu/.../swe-bench`** — round-8 Cloudflare-blocked from the action runner. **Wayback fallback may work** — `web.archive.org/web/*/pli.princeton.edu/...` is the recommended next attempt. Affects `research/22-academic-foundations.md`.

**5. `docs.github.com/.../cloud-agent/risks-and-mitigations`** — never attempted via action; surfaced in round-8 as a follow-up that would directly re-anchor one REFUTES in `research/19-github-copilot-cloud-agent.md`. **Likely action-fetchable** — file a single-URL `[fetch-urls]` issue if pursued. Low priority — report 19 already at ✅.

### 4.4 Not worth fetching anymore

- **The two Lenny URLs as articles** — confirmed video-only with paywall-stub article shell. There is no text body at the URL. See §4.2 for the YouTube route instead (Willison side done 2026-05-13; Cherny remainder still outstanding).
- **The three Klaassen Every.to siblings** — successfully fetched directly via the GH Action runner in (now-closed) fetch-urls issue #23 (the every.to URLs returned HTTP 200 from the runner despite blocking the sandbox). Re-fetch would be duplicate work.
- **`kaner.com/pdfs/ScenarioIntroVer4.pdf` + Wikipedia PDCA + Deming Institute PDSA** — optional per `research/unfetched-sources.md` "Deferred fetch-action candidates" row 5; structural conclusions firm without these.

---

## 5. Work remaining (priority order)

1. ~~**Resolve §3.1 (lost pt-2 work)**~~ — **Done 2026-05-13** via cherry-pick onto `claude/recover-pt2-drain`. See §3.1 for the recovered outcomes.

2. ~~**Drain in-flight fetch-urls issues**~~ — **Done.** Rounds 6 (#29/#30/#31), 7 (#36), and 8 (#41/#42) all drained. **Housekeeping: close GitHub issues #41 and #42** (still showing OPEN on GitHub; drains landed in PR #44).

3. **Decide on `research-plan.md` direction** — the structural pivot from research to build. Until this is decided, individual-report polish has diminishing return. Two coupled questions:
   - Cut a single unified Round-1–5 synthesis (v3 of `00-synthesis.md` or new `research/24-final-synthesis.md`), or keep the current two-synthesis-plus-followups state?
   - Collapse the four architectures to one chosen path (likely Atelier + Refinery layered-spec discipline) + "rejected alternatives" appendix, or keep all four?

4. **Curated human-review tasks (§3.2 above)** — likely fold into step 3's v3 architecture work:
   - Update `architectures/00-comparison.md` §7 + §2.4
   - Update `spec-driven-ai-dev.md` with the 4-field extension
   - Add Round 2 complete stanza (§11)

5. **Retrospective decisions (§3.4 above)** — pick scope across the cumulative 13 unbuilt skill specs / 45 AGENTS.md suggestions / 26 proposed ADRs over five retrospectives.

6. **Cross-corpus propagation sweep (§6.1)** — ~30 min mechanical edit of Shapiro L4-vs-L5 framings across reports 01, 02, 07, and any "Kilroy as Shapiro's L5 reference implementation" mentions.

7. **Optional fetches** — Cherny Lenny remainder (medium, §4.2) and Path-B URLs (low, §4.3) as motivated.

---

## 6. Resumption checklist for the next session

When picking this up cold:

1. `git status` — confirm clean working tree.
2. `git log origin/main..HEAD --oneline` — see what's ahead of main.
3. Check open issues: `mcp__github__list_issues` for `lago-morph/software-factory` state=OPEN. Expect any new `[fetch-urls]` issues — drain any `fetched/issue-N` branches that have landed. (Issues #29/#30/#31/#36 closed 2026-05-13. Issues #41/#42 drained 2026-05-14 but still show OPEN on GitHub — housekeeping closure pending.)
4. Read this PLAN.md §1 + §3 first. If §3.1 still shows the lost work as unresolved, that is the highest-leverage action.
5. If new manual content is in `research/manual/` (anything other than `README.md`), activate the `research-pipeline` skill — Phase 0 will drain it.
6. The `parallel-subagent-fanout` skill is the right tool when 4+ independent subtasks accumulate.

### 6.1 Cross-corpus propagation flags (open from round 7 Shapiro drain)

Round 7's Shapiro canonical-post drain refuted prior corpus framings of Shapiro as a Level-5 practitioner (he positions himself at L4 with the verbatim "I'm here.") and surfaced 8 El Kaim-vs-Shapiro discrepancies. The following propagation edits are PENDING — they were identified during drain but not pushed into all referenced reports:

- **`research/07-dark-factory.md`** — should note that El Kaim *paraphrases* and conflates Shapiro's canonical Five Levels post with the companion "You don't write the code" post; flag the L4 and L5 divergences. The "Nobody writes / Nobody reads" L5 framing currently in the report is El Kaim's, not Shapiro's.
- **`research/01-strongdm-factory.md`** and **`research/02-strongdm-attractor.md`** — anywhere the named StrongDM team-size datum ("less than five people" / "Justin McCarthy three-person team") is attributed to Shapiro's Five Levels post: the Five Levels post says only "less than five people"; the named StrongDM/Justin/three-person datum traces to the companion post only.
- **Anywhere in the corpus** Kilroy is called "Shapiro's Level-5 reference implementation": Kilroy is *not mentioned* in the canonical Five Levels post; that positioning exists only in the companion post.
- **Anywhere in the corpus** Shapiro is described as "a Level 5 practitioner" or "Level 4–5 practitioner-tooler": refute with Shapiro's verbatim L4 self-position ("I'm here.").

Suggested approach: a single `Grep` pass for the strings above, then a small subagent dispatch to apply the corrections. Estimated effort: ~30 min wall time. Not picked up in this session because the user did not explicitly request the cross-corpus correction sweep — this checklist exists so the next session can catch it.

---

## 7. Fetch-loop tooling (canonical companion files)

These files in `research/` are the system of record for what URLs are reachable, what isn't, and how to recover the rest:

- `research/blocked-urls.md` — cross-round canonical inventory of URLs that returned non-200 from the GitHub Actions runner. Versioned (currently v5).
- `research/blocked-urls-round-2.md` — per-issue retrieval log for Round 2's fetch passes (issues #4 and #8).
- `research/blocked-urls-round-6.md` — per-URL log + lessons learned from the round-6 drains (issues #29/#30/#31).
- `research/blocked-urls-round-7.md` — per-URL log + lessons learned from the round-7 drain (issue #36).
- `research/blocked-urls-round-8.md` — per-URL log + lessons learned from the round-8 drains (issues #41/#42); contains the canonical "lesson R8.1: arXiv `/e-print/` is the gold-standard paper-body recovery route" and the up-to-date follow-up queue.
- `research/unfetched-sources.md` — URLs the action couldn't recover; categorized by which manual recovery path (A: curl with cookies; B: Save Page As; C: Reader View) will work.
- `research/fetch-from-browser.sh` — runnable bash script the user invokes locally with browser cookies. Outputs to `research/manual/`.

External-synthesis artifacts (e.g., the ChatGPT deep-research output we use as Round-5 counterfactual) live under `/reference-only/<short-slug>-<date>/` with a `README.md` orientation file alongside the artifact.

---

## 8. GitHub Action — security stance (frozen)

The `fetch-blocked-urls` workflow uses **label-only authorization** (`fetch-urls` label, applied by a Triage-role human). This avoids the `author_association` footgun where webhook payload and REST API disagree. Documented in ADR-0001 (`docs/adr/0001-fetch-blocked-urls-mechanism.md`).

The runner has full network egress and writes to a fresh `fetched/issue-N` branch (never to `main`). All merges into `main` are human-driven.

---

## 9. Costs, scope, and what this plan does not do

**Token cost envelope (approximate):**
- Round 1: ~30k tokens × 7 subagents
- Round 2: ~50k tokens × 6 subagents + lead-agent partial passes (per §11 / §17 v0.2)
- Rounds 3–6: catalogued in the parallel-fanout night run on 2026-05-11. Token-level detail per subtask lives in `harness/runs/20260511-054258/report.md` and `report-pt2.md`; no dollar total recorded.

**Out of scope (deliberately):**
- ~~Replacing the four architectures with a single "winner". The comparison stays a comparison.~~ **Reversed by `research-plan.md` (PR #46, 2026-05-14).** That doc proposes the opposite — for the lights-out-greenfield mandate specifically, v3 should likely collapse to one chosen architecture (Atelier + Refinery layered-spec discipline) with the other three demoted to "rejected alternatives" in an ADR. Decision pending; see §5 task 3.
- Building harness code beyond the `fetch-blocked-urls` workflow primitive.
- Adopting `harness` vocabulary across the architecture documents wholesale before the user has reviewed Round 2 synthesis report 13.
- Crawling everything blocked from the sandbox — the remaining ~7 outstanding URLs (5 Path-B-only, 2 retry-eligible) per §4.3 are documented gaps, not unknowns.

---

## 10. Round-by-round canonical reports (lookup table)

| Round | Reports | Status | Key contribution |
|---|---|---|---|
| 1 | `research/01-07-*`, `research/00-synthesis.md` | ✅ Complete | 7-source initial reconstruction; F1–F20 failure modes |
| 2 | `research/08-12-*`, `research/13-round-2-synthesis.md` | ✅ Complete | Jaymin book + Overstory + OpenHands substrate audits; F21–F33 |
| 3 | `research/followup/01-12-*` | ✅ Complete | 12 threads; Thread 12 (Dark Factory archive.org) resolved into report 07 without a separate file. The post-Round-3 Brier drain at `followup/12-brier-pace-layers.md` was recovered onto main via the 2026-05-13 cherry-pick (see §3.1), along with primary-source upgrades to followup/05 and followup/07. F34 (cross-layer drift) catalogued in followup/12. |
| 4 | `research/14-17-*` + `research/24-el-kaim-book-product-line-variability.md` | ✅ Complete | El Kaim book: spec authorship, BMAD, council, codex+skills, plus Chapter 9 (product-line-variability, added 2026-05-13 from manual drain). F35 (Federation-as-Family Drift) promoted in report 24. |
| 5 | `research/18-23-*` | Reports 19/20/21/23 ✅; 22 has 2 outstanding source rows (1 Wayback-eligible, 1 cross-cited Path-B-only); **18 still 🟡** due to 3 `openai.com/index/*` Cloudflare blocks | Counterfactual harvest: OpenAI Codex, GitHub Copilot, Replit, Tabnine, academic foundations, Anthropic engineering |
| 6 | `harness/runs/20260511-054258/report.md` + `report-pt2.md`; merge `423940f` | ✅ Complete | 26-subtask parallel-fanout night run on 2026-05-11; pt-2 wave (Brier/Klaassen/evals) recovered via 2026-05-13 cherry-pick |
| 7 | drain of issue #36 + 3 manual drops | ✅ Complete | Shapiro canonical Five Levels drained (L4 self-position; 8 El Kaim discrepancies → §6.1); El Kaim post-index Path B; El Kaim Chapter 9 manual drain → report 24, F35; `platform.claude.com/.../agent-skills/overview` Path B → report 23 §3 attribution audit closed. Per-URL log: `research/blocked-urls-round-7.md`. |
| 8 | drain of issues #41 + #42 + Lenny full transcript | ✅ Complete | Reports 19, 20 flipped to ✅; followup/08 §3 paper-body-anchored via CaMeL arXiv `/e-print/` recovery; reports 05, 06 flipped to ✅ FULL via Willison transcript. Per-URL log: `research/blocked-urls-round-8.md`. |
| 9 | Round-9 manual drain (RE/SE + LLM+RE academic + Kiro) | ✅ Complete | 11 manual files (5 RE/SE PDFs + 3 academic papers + 2 Kiro blog posts + 1 redundant Cherny transcript) drained via 3-subagent parallel dispatch on 2026-05-16. Outputs: new **report 25** (requirements-engineering-foundations, 5,572 words; anchors El Kaim's 9-field discipline to INCOSE GtWR C1–C15 one-to-one mapping), new **report 26** (prompt-underspecification-academic, 6,187 words; first academic-empirical anchor for the corpus' spec→code-gap framing), report **12 §2.5** extended (+1,150 words; Kiro deep-spec mechanic). Surfaces 4–6 candidate F-modes with numbering collision (see §3.6). |

For each report, the source citations live in the report's §"Sources reviewed" or first-page status table.

---

# Archive — version history and per-round catalogs (compressed)

Sections 11–17 below preserve the per-round dispatch records that v0.1–v0.7 of this file accreted. They are reference material for "where did claim X come from?" lookups; they are not the live work plan. The live work plan is §§1–6.

## 11. Round 2 — Subagent dispatch record (was §§1–9 of v0.1–v0.4)

Round 2 dispatched 6 subagents (the last, subagent 13, was the sequential synthesis run; the other 5 ran in parallel). The lead question: *what can we reuse from Jaymin's book, the Overstory repo, and OpenHands to build the four architectures?*

Subagent dispatch:
- **08 — Jaymin Book Foundations + Patterns** (Ch 1–5, 7) → `research/08-jaymin-book-foundations-patterns.md`
- **09 — Jaymin Book Harnesses + Practices + Mental Models** (Ch 6, 8, 9) → `research/09-jaymin-book-harnesses-practices-mental-models.md` (v1.1 after the 2026-05-13 editorial collapse folded in the prior partial's Substack manifesto digest)
- **10 — Overstory substrate audit** → `research/10-overstory-substrate-audit.md`
- **11 — OpenHands substrate audit (CI/CD lens)** → `research/11-openhands-substrate-audit.md`
- **12 — Adjacent ecosystem** → `research/12-adjacent-ecosystem.md`
- **13 — Synthesis** (sequential; runs last) → `research/13-round-2-synthesis.md`

**Outputs:** 13 new failure modes (F21–F33). Substrate-stack recommendation: OpenHands SDK + Overstory-design-in-Python overlay + Compound Atelier as methodology overlay at L3. **The §7 swap in `architectures/00-comparison.md` is still pending — see §3.2 task 1.**

**Round 2 completed:** drain merge `423940f` on 2026-05-11. (Round 2 complete stanza per §3.2 task 3 still to be appended here in a follow-up edit.)

## 12. Round 3 — 12 follow-up threads (was §11 of v0.3–v0.7)

Twelve threads catalogued from a former root-level `followup.md`. Threads 1–11 were dispatched as `research/followup/01-11-*`. Thread 12 (*Dark Factory via archive.org*) was resolved without producing a separate followup file — when the user retrieved the article via Path B (Save Page As) on 2026-05-11, its content folded directly into `research/07-dark-factory.md`.

| # | Topic | Output | Status |
|---|---|---|---|
| 1 | Dan Shapiro's "Five Levels" maturity model | `followup/01-shapiro-five-levels.md` | ✅ |
| 2 | Community Attractor implementations survey | `followup/02-attractor-implementations.md` | ✅ |
| 3 | Boris Cherny "What happens after coding is solved" | `followup/03-cherny-interview.md` | ✅ best-effort; primary unlock needs YouTube transcript (§4.2) |
| 4 | Steve Yegge's Gas Town + Beads orchestration | `followup/04-gastown-beads.md` | ✅ |
| 5 | Klaassen's three sibling Every.to articles | `followup/05-klaassen-siblings.md` | ✅ primary-source-anchored (upgrade recovered onto main via the 2026-05-13 cherry-pick; see §3.1) |
| 6 | Competitor factory landscape survey | `followup/06-competitor-landscape.md` | ✅ primary-source-anchored via issues #31 (Devin/Factory/8090/Superpowers) + #36 (Superconductor.com) drains |
| 7 | Anthropic multi-agent + Husain/Shankar evals FAQ | `followup/07-evals-deepdive.md` | ✅ primary-source-anchored (upgrade recovered onto main via the 2026-05-13 cherry-pick; see §3.1; 4 anthropic.com engineering posts landed via issue #29 drain). |
| 8 | Security primitives (CaMeL + Safe YOLO + Lethal Trifecta) | `followup/08-security-primitives.md` | ✅ paper-body-anchored — issue #29 drain primary-anchored 5 sources; round-8 / issue #42 recovered CaMeL paper body via arXiv `/e-print/` LaTeX route (§3 expanded from 7 to ~15 subsections) |
| 9 | Methodology ancestors (Kaner / Rumelt / Deming) | `followup/09-methodology-ancestors.md` | ✅ structural conclusions firm; primary verification optional per §4.4 |
| 10 | Governance / liability angle | `followup/10-governance.md` | ✅ primary-source-anchored via drained issue #26 (Stanford CodeX / BCG Platinion / Pragmatic CTO) |
| 11 | Compound Knowledge plugin deep-dive | `followup/11-compound-knowledge.md` | ✅ |
| 12 | Dark Factory via archive.org | resolved into `research/07-dark-factory.md` (no separate file) | ✅ **RESOLVED 2026-05-11** via user Path-B retrieval |

**Separate post-Round-3 work (recovered onto main 2026-05-13):** the `925da5b` sub-30 commit drained Noah Brier's *Culture of AI Engineering* (every.to, 2026-05-08) into a new `research/followup/12-brier-pace-layers.md`. Originally only on a side branch; recovered via the 2026-05-13 cherry-pick. See §3.1.

## 13. Round 4 — El Kaim enterprise-architecture book (was §12 of v0.4–v0.7)

Source: 7 chapters of William El Kaim's draft book *Continuous / Intent-Driven Enterprise Architecture* (~430 KB). Now at `reference-only/el-kaim-book/Chapter [1-7] *.txt`.

Four clusters were dispatched:

- **Cluster A — Spec authorship discipline** → `research/14-el-kaim-book-intent-and-spec-authorship.md`. Recommendation: extend `spec-driven-ai-dev.md` with 4 new fields (non-goals, decision-seeds, invariant-with-bindingHint, Intent section). **Pending — see §3.2 task 2.**
- **Cluster B — BMAD + attractor + dark factory** → `research/15-el-kaim-book-bmad-attractor-dark-factory.md`.
- **Cluster C — Delegation, multi-agent EA Council, accountability** → `research/16-el-kaim-book-council-and-delegation.md`.
- **Cluster D — Codex as Git-distributed skill substrate** → `research/17-el-kaim-book-codex-and-skill-substrate.md`.

SAP-specific material (chapter 5) was kept as a worked example only.

## 14. Round 5 — External-synthesis harvest (was §13 of v0.6–v0.7)

Source: paired ChatGPT deep-research artifact at `reference-only/chatgpt-deep-research-2026-05-11/` (`report.md` + `sources.md` + `README.md`).

Six clusters were dispatched against six source families that the original ChatGPT report under-cited:

- **13.1.1 OpenAI Codex** → `research/18-openai-codex-substrate.md`
- **13.1.2 GitHub Copilot cloud agent** → `research/19-github-copilot-cloud-agent.md`. **Primary-anchored** (issue #30 drain landed 3/9; round-8 issue #42 landed 6/6 canonical re-finds. Report flipped to ✅).
- **13.1.3 Replit Agent** → `research/20-replit-agent.md`. **Primary-anchored** via round-8 issue #41 — all 13 R-* URLs ✅; multiple refutations of community-mirror reconstructions.
- **13.1.4 Tabnine enterprise** → `research/21-tabnine-enterprise.md`. Primary citations landed via drained issue #27.
- **13.1.5 Academic foundations** (AlphaCode / SWE-bench / SWE-agent / CodeGen) → `research/22-academic-foundations.md`. Primary citations landed via drained issue #28; 2 SWE-bench announcement URLs remain Cloudflare-blocked per §4.3.
- **13.1.6 Anthropic engineering trilogy** → `research/23-anthropic-engineering-trilogy.md`. **Primary-anchored** via issue #29 drain + round-7 Path-B drop of `platform.claude.com/.../agent-skills/overview`. Two remaining Skills SPA pages outstanding per §4.3 item 1a.

**Round-5 substrate-audit status as of 2026-05-14:** Reports 19, 20, 21, 23 are all ✅. Report 22 has 2 outstanding source rows (Princeton SWE-bench blog — Wayback-eligible; `openai.com/index/introducing-swe-bench-verified` — cross-cited Path-B-only). **Report 18 (OpenAI Codex) is the sole 🟡 in the Round-5 cluster** — 5/7 `developers.openai.com/codex/*` URLs ✅, but 3 `openai.com/index/*` URLs remain Cloudflare-JS-challenged from the action.

Round-5 also catalogued a "weak citations" QC checklist (in the cluster reports) and a counterfactual-comparison instruction for synthesis time.

## 15. Round 6 — 26-subtask parallel-fanout night run (was §14 of v0.7)

`harness/runs/20260511-054258/report.md` is the per-subtask record for the main wave (26 subtasks, 0 merge conflicts). A follow-up "pt-2" wave (sub-30 Brier, sub-31 Klaassen drain, sub-32 evals drain) ran cleanly on the same branch on the same night; `harness/runs/20260511-054258/report-pt2.md` is its per-subtask record. The pt-2 wave was orphaned on the side branch until the 2026-05-13 cherry-pick recovered it — see §3.1.

## 16. Round 1 — initial subagent dispatch (predates PLAN.md; reconstructed retrospectively)

Round 1 dispatched 7 subagents off the seed list in `initial-sources.md`:

- 01 StrongDM Factory, 02 StrongDM Attractor, 03 Every Compound Engineering, 04 Every Skill Libraries, 05 Simon Willison, 06 HN + Lenny, 07 Dark Factory.

Output: `research/01-07-*` plus initial synthesis `research/00-synthesis.md`. F1–F20 failure-mode catalog established. Most sources were blocked from the sandbox in Round 1; primary-source incorporation happened in Round 2 + after via the fetch-blocked-urls action.

## 17. Provenance + version history (compressed)

| Version | Date | What changed |
|---|---|---|
| v0.1 | 2026-05-10 | Initial structure for Round-2 dispatch (6 subagents in §3) |
| v0.2 | 2026-05-11 | Records the lead-agent partial pass + resumption checklist |
| v0.3 | 2026-05-11 | Consolidates a former root-level `followup.md` into §11 (12 Round-3 threads) |
| v0.4 | 2026-05-11 | Adds §12 — Round 4 (4 El Kaim-book clusters in `research/manual/multi/`); §11.12 "RESOLVED" after Dark Factory primary source incorporated into report 07 |
| v0.5 | 2026-05-11 | Adds §5.1 (4 canonical workflow-tooling files); "what doesn't belong on main" sidebar; deletes leftover `.fetch-work/`; updates `.gitignore` |
| v0.6 | 2026-05-11 | Adds §5.2 (external-syntheses) and §13 (Round-5 6-cluster harvest) |
| v0.7 | 2026-05-11 | Adds §14 (Round-6 night-run record); routes future sessions to the deferred-fetch table |
| **v0.8** | **2026-05-13** | **Cleanup pass.** Source files reorganized into `/reference-only/`. Stale §10.2/§10.4 references retired. Editorial collapse of 09 partial completed (Substack manifesto folded into §9 of unified report). 7 drained fetch-urls issues closed (#4, #8, #23, #24, #26, #27, #28). 3 new batched issues filed (#29, #30, #31). Live work moved to §§1–6; per-round detail compressed into §§11–17. **Discovered: pt-2 drain work on side branch never merged — see §3.1.** |
| **v0.9** | **2026-05-13** | **Pt-2 cherry-pick recovery.** Brought sub-30 / sub-31 / sub-32 / recording commits onto main via `claude/recover-pt2-drain`. Adds `research/followup/12-brier-pace-layers.md` (Brier pace-layers report, ~2,571 words, F34 candidate); upgrades `research/followup/05-klaassen-siblings.md` and `research/followup/07-evals-deepdive.md` from inferential to primary-source-anchored. §3.1 changed from HIGHEST-priority bottleneck to RESOLVED. |
| **v0.10** | **2026-05-14** | **Rounds 7–8 + Lenny full + retrospectives + research-plan recorded.** Round-7 captured: Shapiro canonical drain (8 El Kaim-vs-Shapiro discrepancies → §6.1 propagation flags); El Kaim post-index Path B; **El Kaim Chapter 9 manual drain → new report 24 (product-line-variability), F35 promoted**; `platform.claude.com/.../agent-skills/overview` Path B'd into report 23 §3. Round-8 captured: issues #41/#42 drained (reports 19/20 ✅, report 18 still 🟡 due to 3 `openai.com/index/*` Cloudflare-blocks); **CaMeL paper body recovered via arXiv `/e-print/` LaTeX route → followup/08 §3 paper-body-anchored**; Lenny × Willison full ~90-min transcript drained → reports 05/06 ✅ FULL. Three new retrospectives recorded (2026-05-13-02, 2026-05-14-01, 2026-05-14-02); 2026-05-13-01 (which had landed pre-v0.9 but was not enumerated in v0.9's §3.4) also folded into §3.4 so all five retrospectives are now tabulated. `research-plan.md` filed at repo root (PR #46) — proposes v3 architecture collapse; §9 "out of scope" line about keeping all four architectures explicitly reversed. §3.4 retrospective table expanded to five retrospectives / 13 unbuilt skills / 45 AGENTS / 26 ADRs. §4.3 Path-B list trimmed to actual remainder (~7 URLs). §5 work-remaining task 2 (drain in-flight issues) marked done; new task 3 added for the research-plan.md decision. §7 fetch-loop tooling list expanded to include `blocked-urls-round-6/7/8.md`. §10 lookup table extended with Rounds 7 and 8. §12 stale "pending issue drain" status cells in rows 6/7/8 corrected. §14 Round-5 substrate-audit status line added. |
| **v0.12** | **2026-05-16** | **Round-9 manual drain — RE/SE foundations + LLM+RE academic + Kiro.** Opens a new methodology-discipline thread. 11 source files in `research/manual/` drained via 3-subagent parallel dispatch: 5 RE/SE primary methodology PDFs/MHTML → new report 25; 3 academic LLM+RE papers → new report 26; 2 Kiro blog posts → report 12 §2.5 extension (+1,150 words); 1 redundant Cherny transcript deleted (different transcription of already-drained `reference-only/lenny-podcast-transcripts/cherny-head-of-claude-code-full.txt`). Numbered report count 24 → 26. **Surfaces F36–F41 candidate failure-mode proposals** with internal numbering collision between reports 25 and 26 (both reports claimed F36/F37 for distinct phenomena) — triage recipe in new §3.6. §1 Done block extended; §10 lookup table extended with row for Round 9; INDEX.md updated with rows 25 + 26 + revised F-mode lookup pointer. `research/manual/` now contains only `README.md`. Audit trail: this PR. |
| **v0.11** | **2026-05-14** | **Lenny × Cherny full-transcript drain.** Closes the last in-flight primary-source gap from the rounds 1–8 pipeline. `research/followup/03-cherny-interview.md` flipped 🟡 → ✅ FULL (219 → 365 lines; ~30 new verbatim quotes across 9 new H2 sections: 4-layer AI-product principles incl. corpus-first *"build for the model six months from now"*, 3-layer safety framework, *"multi-cladding"* Anthropic-internal term, Cowork 10-day build anecdote, race-to-the-top open-source-sandbox principle, printing-press historical analog). `research/06-hn-and-lenny.md` updated with 6 net-new headline cross-references. **"5 Claudes parallel" architecture resolved** to five-agents-steady-state + 1/3 terminal + 1/3 desktop + 1/3 iOS surface split; **3 claims downgraded to single-secondary-source confidence** because the 90-min transcript never mentions them: `/loops`, `/batch`, "thousands of overnight agents". §3.5 flipped to ✅ RESOLVED. §4.2 second item flipped to DONE. Redundant arxiv `2503.18813` v1 HTML 404-stub deleted from `research/fetched/issue-36/` (subsumed by round-8 `/e-print/` recovery; `research/fetched/` directory now empty and removed). |

---

## Future research

Captured as the research-pipeline skill prescribes: name the cluster, list sources, justify in one paragraph, estimate effort. These are leads that surfaced during drain work but were not chased in the current round.

### Future research: El Kaim's broader Medium corpus (10+ posts beyond the 9-chapter book)

**Sources** (surfaced from `welkaim.medium.com` post-index page, retrieved manually 2026-05-13):

- *From Vibes to Codex to Claw: Architecture enters the Edge era* (Feb 24, 2026)
- *When Architecture Starts Thinking: The Shift to Cognitive Infrastructure* (Feb 20, 2026)
- *The Cyrano de Bergerac Method of Prompting: One Question, a Thousand Voices* (Feb 19, 2026)
- *From Vibes to Flow: Building the Enterprise Codex for Agentic AI* (Feb 18, 2026)
- *Spec-Driven Enterprise Architecture with BMAD, AI, and LeanIX* (Feb 10, 2026)
- *From AI Discovery to AI Governance: Building an Enterprise Copilot on LeanIX* (Dec 16, 2025)
- *Designing and governing AI agents landscape and architecture with LeanIX* (Nov 10, 2025)
- *Analysis of AI and Agentic AI Features in major Enterprise Architecture Management Solutions* (Jul 14, 2025)
- *From Automation to Autonomy: The AI-Driven Transformation of the Enterprise Architecture Tool…* (Jul 13, 2025)
- *The SAP API Policy as an External Trigger: How the EA Codex absorbs vendor policy changes* (between Ch5 and Ch6; possibly a sidebar to Ch6)

**Justification.** Our four existing El Kaim reports (14–17) are anchored to the 9-chapter AI-Augmented-EA series. The post-index page shows El Kaim has published a **parallel track** of standalone posts that pre-date and accompany the book series and that touch directly on our four candidate architectures: the *Cyrano* post is almost certainly a one-question/many-agents pattern that overlaps with our Council architecture (report 16); the *BMAD/LeanIX* post (Feb 10) is the canonical primary source for material currently reconstructed across reports 15 + 16; the three *LeanIX governance* posts are primary-source material for AI-agent governance that `research/followup/10-governance.md` currently reconstructs from secondary sources; the *Cognitive Infrastructure* post likely names patterns we currently treat as anonymous. Investigating this cluster would let us flip reconstructed-from-search-snippet citations in 5+ reports to primary, and may surface 1–2 named patterns that should be added to the methodology layer.

**Effort.** ~10 Medium posts, all on the same host (`welkaim.medium.com` / `medium.com/@welkaim/...`). Host is action-reachable per round-6 testing (the about page returned content). One batched `[fetch-urls]` issue + one drain pass; ~½ session.

**Recovery path.** File a single `[fetch-urls]` issue with the 10 post URLs (need to harvest the exact URLs first — the post-index page deliberately omits them in the text export; either the user re-exports with hyperlinks preserved, or a `find / -type f -name 'welkaim.medium.com'`-style scan reveals what we already have, or WebSearch by title).

### Future research: Noah Radford — "the road runner economy"

**Sources:**
- https://nraford7.github.io/road-runner-economy/

**Justification.** Surfaced as a drafting-readers acknowledgement at the bottom of Shapiro's canonical "Five Levels — From Spicy Autocomplete to the Software Factory" post. Shapiro explicitly endorses the framing. None of our 24 reports + 12 followups references Radford or the "road runner economy" framing, yet Shapiro's L4–L5 narrative leans on it. If Radford's essay names a deflationary-economics dynamic our corpus currently treats as anonymous (e.g., the "code is becoming free; meaning is the moat" / "manual labor in a deflationary economy" framing that runs through the L0 description), we have a primary anchor we're missing. Could change the framing of `research/00-synthesis.md` §1 (why the methodology matters) or seed a new economics-of-the-software-factory section in `research/13-round-2-synthesis.md`.

**Effort.** Single GitHub Pages essay (`raw.githubusercontent.com`-style URL or its `nraford7.github.io` mirror). Expected reachable from action without issue; one-page WebFetch may be sufficient. ~½ hour wall time.

### Future research: platform.claude.com Agent Skills docs (Path B-only) — 2 of 3 pages remaining

**Sources:**
- ~~https://platform.claude.com/docs/en/agent-skills/overview~~ — Path-B'd in round 7 and drained into report 23 §3.
- https://platform.claude.com/docs/en/agent-skills/best-practices — outstanding.
- https://platform.claude.com/docs/en/agent-skills/security — outstanding.

**Justification.** Round-6 drain on `research/23-anthropic-engineering-trilogy.md` §3 surfaced that several quotes the report had attributed to Anthropic's S13 ("Equipping agents...") are not in S13 — they live in these platform docs pages instead. The overview drop in round 7 closed the attribution audit for that page. Without the best-practices and security pages, the rest of the re-anchoring stays open. Affects: report 23 §3 (security guidance for Skills), and indirectly any future architecture decision that wants to cite Anthropic's *official* skill-security stance vs. the engineering-blog framing.

**Effort.** 2 remaining pages, JS-rendered SPA so action-fetch returns content-free shells. **Path B only** (user does Save Page As after a logged-in Console session has rendered the JS). Then standard drain pass; ~20 min.

---

*End of PLAN.md v0.12.*
