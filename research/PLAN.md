# Software Factory Research — PLAN.md

**Version:** v0.9 (2026-05-13)
**Status:** Five rounds of research complete (24 numbered reports + 12 follow-up reports + 5 architecture docs + 1 methodology doc). Source files reorganized: live primary material is in `/reference-only/`; transient drop zone is `research/manual/`. Three fetch-urls issues open and awaiting action runs; three curated human-review tasks pending; five retrospective decisions queued.

**Earlier versions:** v0.1–v0.7 lived as accreted Round-by-Round sections (§§11–17 below as Archive). v0.8 rewrites the live status at the top and compresses the per-round detail; v0.9 records the pt-2 cherry-pick recovery and updates §3.1 from bottleneck → RESOLVED. The audit trail is preserved in the archive sections; the live work is in §§1–6.

---

## 1. Current state (TL;DR)

**Done:**
- **Round 1** — 7 reports (`research/01-07-*`) + initial synthesis (`research/00-synthesis.md`).
- **Round 2** — 5 reports + synthesis (`research/08-12-*`, `research/13-round-2-synthesis.md`). 13 new failure modes (F21–F33) catalogued; never folded into `architectures/00-comparison.md` §2.4.
- **Round 3** — 12 follow-up threads (Threads 1–11 → `research/followup/01-11-*`; Thread 12 *Dark Factory via archive.org* was RESOLVED without a new file when the article was retrieved via Path B and folded into `research/07-dark-factory.md`). A separate post-Round-3 effort produced `research/followup/12-brier-pace-layers.md` plus primary-source upgrades to followup/05 and followup/07 — these were on a side branch only until the 2026-05-13 cherry-pick (see §3.1).
- **Round 4** — 4 reports off the El Kaim enterprise-architecture book (`research/14-17-*`). The book chapters are now at `reference-only/el-kaim-book/`.
- **Round 5** — 6 reports off counterfactual harvest against a ChatGPT deep-research artifact (`research/18-23-*`). The artifact is at `reference-only/chatgpt-deep-research-2026-05-11/`.
- **Round 6** — 26-subtask parallel-fanout night run on 2026-05-11 (`harness/runs/20260511-054258/`) that produced most of the above. One follow-up "pt-2" wave (3 subagents) was originally orphaned on a side branch but was recovered onto main via the 2026-05-13 cherry-pick (see §3.1).
- **Session 2026-05-13** — editorial collapse of the 09 partial into the unified report; closed 7 drained fetch-urls issues; filed 3 new batched fetch-urls issues (#29 / #30 / #31); reorganized source files into `/reference-only/`.

**Open items live in:**
- §3 Bottlenecks — four live items: §3.2 curated human-review backlog (the original §14.4 tasks 2, 3, 5), §3.3 in-flight fetch-urls workflow (#29 / #30 / #31), §3.4 retrospective decisions, §3.5 YouTube-video-only Cherny claims.
- §4 Manual fetch instructions (prioritized).
- §5 Work remaining (priority order).

---

## 2. Repository layout (what lives where)

```
/architectures/         → 4 candidate methodologies + comparison
/docs/adr/              → ADR system (only ADR-0001 written; 7 more proposed in retrospective)
/harness/runs/          → Historical fanout-run records
/reference-only/        → Primary sources kept on disk for re-quoting
    el-kaim-book/       → 7 chapters of El Kaim's EA book (~430 KB)
    chatgpt-deep-research-2026-05-11/  → counterfactual synthesis artifact
    dark-factory-article.txt           → El Kaim Medium article (anchors report 07)
    brier-culture-of-ai-engineering.txt → Brier Every.to article (anchors `research/followup/12-brier-pace-layers.md`)
    every-my-ai-had-already-fixed.txt   → Klaassen Every.to article (anchors report 03)
/research/              → 24 numbered reports + 12 followup reports + workflow tooling
    PLAN.md             → this file
    manual/             → transient drop zone for new manual fetches
    fetch-from-browser.sh, unfetched-sources.md, blocked-urls*.md → fetch-loop tooling
/retrospective/         → 2026-05-11-01 retrospective + 4 sibling skill specs
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

**Follow-up fetch queue (next batched issue):** ~~Shapiro five-levels correct slug, arxiv 2503.18813 paper body, Superconductor.com, Cognition Devin announcement URL, 6 GitHub docs canonical URLs~~ — **all closed by rounds 6–8 drains**. Still queued (low priority): `platform.claude.com` Agent Skills security guidance (Path B only — JS-SPA shells); `openai.com/index/*` 3 URLs (Path B only — Cloudflare JS-challenged bodies); `docs.github.com/en/copilot/concepts/agents/cloud-agent/risks-and-mitigations` (would directly re-anchor a REFUTES on report 19). See `research/blocked-urls-round-8.md` §"Follow-ups" for the full actionable list.

#### Round-8 drain (issues #41 + #42) — added 2026-05-13

- **#41** (Replit + OpenAI Codex + SWE-bench × 24): 20/24 OK. Drained into `research/20-replit-agent.md` (all 13 R-* rows flipped 🟡 → ✅; 5+ refutations of community-mirror reconstructions) and `research/18-openai-codex-substrate.md` (5 `developers.openai.com/codex/*` rows flipped to ✅; 3 refutations: bwrap+seccomp not Landlock, no `on-failure` mode, AGENTS.md plain-concat not header-wrapped). 4 URLs failed Cloudflare (3 `openai.com/index/*` + 1 `pli.princeton.edu`); Path B remains the only route. Per-URL outcomes in `research/blocked-urls-round-8.md`.
- **#42** (GH Copilot canonical re-finds + arXiv CaMeL × 10): 6/6 GH Copilot canonical URLs ✅; 2 Copilot Workspace URLs documented sunset (folded into cloud-agent); arXiv CaMeL **paper body recovered via `/e-print/` LaTeX-tarball route** (gunzip|tar -xf manually; saved to `reference-only/camel-paper/`). Drained into `research/19-github-copilot-cloud-agent.md` (flipped 🟡 → ✅, 2 REFUTES on branch-restriction and CI-approval-gate framings, new §3.1 on Copilot Spaces) and `research/followup/08-security-primitives.md` (§3 expanded from 7 to ~15 subsections — PI-SEC formal game, NORMAL/STRICT modes, side-channel attacks, baseline comparison, overhead). **Lesson R8.1:** arXiv `/e-print/` is the gold-standard recovery route when html/v* 404s and pdf is binary.

### 3.4 Pending retrospective decisions

`retrospective/2026-05-11-01/` contains user-decision-pending artifacts not tracked elsewhere:

- **3 unbuilt skill specs** (only `adr` was built in that session):
  - `provenance-aware-reconstruction-spec.md` (high priority, ~¼ day)
  - `sync-to-main-before-building-spec.md` (high priority, ~¼ day)
  - `verbatim-fetch-via-curl-spec.md` (medium priority, ~¼ day)
- **15 AGENTS.md additions** in `AGENTS-suggestions.md`. The project has no `AGENTS.md` yet.
- **7 proposed ADRs** (titles only in the retrospective; specs would be authored via the `adr` skill).

### 3.5 YouTube-video-only content (un-primary-sourced)

The two Lenny URLs (Cherny + Willison interviews) turned out to be **video-only** with paywall-stub article landing pages. Unlocked only by a YouTube transcript-extraction service (NOT a paywall bypass). See §4.

**Status update 2026-05-13 (drain):** The **Willison side is now ✅ FULL** — the user dropped the full ~90-min YouTube transcript at `research/manual/lenny-An AI state of the union.txt` and it has been fully drained into `research/05-simon-willison.md` and `research/06-hn-and-lenny.md`. Lethal-trifecta walkthrough (with the **97%-failing-grade** doctrine), Challenger-disaster prediction (including the self-falsification clause), OpenClaw/Claws latent-demand exemplar, end-of-2026 prediction, and macroeconomic worry are all now primary-source-anchored. **The Cherny side remains 🟡 partial** — only the first ~30 min was manually transcribed; the corpus-quoted Cherny claims ("10–30 PRs/day", "10–15 parallel sessions") are partially anchored but the remaining ~60 min is outstanding (still the §4.2 task).

---

## 4. Manual fetch instructions

Three priority tiers. Highest-leverage items first.

### 4.1 Highest priority — do these if you have time

**None today.** The #29 / #30 / #31 in-flight batches landed and were drained 2026-05-13 — see §3.3. The remaining follow-up URLs are queued for a future single batched issue (see `research/blocked-urls-round-6.md` §"Follow-ups"); none requires manual fetch.

### 4.2 Medium priority — primary-source unlock

**YouTube transcripts for the two Lenny URLs.**
- ~~`https://youtu.be/wc8FBhQtdsA` — Simon Willison on Lenny (AI state of the union)~~ — **DONE 2026-05-13.** Full ~90-min transcript dropped at `research/manual/lenny-An AI state of the union.txt`, drained into reports 05 and 06, then moved to `reference-only/lenny-podcast-transcripts/willison-ai-state-of-the-union-full.txt` (the earlier `first30min` partial was superseded and deleted).
- `https://youtu.be/We7BZVKbCVw` — Boris Cherny on Lenny (head of Claude Code interview) — **still outstanding.** Only the first ~30 min has been manually transcribed.

How (Cherny remainder):
1. Open the YouTube URL in a browser logged into your YouTube account.
2. Click "Show transcript" under the video description (or use the three-dot menu).
3. Copy the full transcript text.
4. Paste it into `research/manual/lenny-cherny-transcript-full.txt` (or replace the existing partial).
5. Commit and push.

Alternative: use a transcript service (Otter.ai, Tactiq, etc.) that returns cleaner timestamps.

Drains into `research/06-hn-and-lenny.md` and `research/followup/03-cherny-interview.md`. **Primary unlock for the "10–30 PRs/day" and "10–15 parallel sessions" Cherny claims** that the corpus quotes but has never been fully primary-sourced.

### 4.3 Low priority — background completeness

These three URL families are known-or-likely action-blocked. Path B (browser "Save Page As → Web Page, Complete") is the only realistic route. Each is "nice to have"; the relevant reports are firm without verbatim source-level fidelity.

**1. ~~`medium.com/@welkaim/about` + `welkaim.medium.com/`~~** — **RESOLVED 2026-05-13** via Path B drop. Bio captured in `research/07-dark-factory.md` header; post-index revealed 10+ unread El Kaim posts (logged as future-research cluster, see "Future research" at the bottom of this file).

**1a. `platform.claude.com/docs/en/agent-skills/{overview,best-practices,security}`** — **NEW Path B item from round 7.** The action returned HTTP 200 but the body is a JS-rendered SPA shell (~17 `Loading...` placeholders); curl can't execute the JS. Affects `research/23-anthropic-engineering-trilogy.md` §3 (security-quote attribution still open — several quotes attributed to S13 are actually from these pages per the round-6 drain). **Path B only**: open each URL in a logged-in Console session, wait for the page to render, File → Save Page As → Web Page, Complete; drop the `.html` into `research/manual/`. ~3 URLs.

**2. `docs.replit.com/*` + `blog.replit.com/*` (~20 URLs).** Affects `research/20-replit-agent.md`. Cloudflare-gated; action success uncertain (per `blocked-urls.md` v5 the `*.openai.com` analog is known-blocked from action too).

How:
- Try filing a `[fetch-urls]` issue first. If action 403s, fall back to Path B for the URLs listed in `research/20-replit-agent.md`'s blocked-URL section.

**3. `developers.openai.com/codex/*` + `openai.com/index/{harness-engineering, unlocking-the-codex-harness}`.** Affects `research/18-openai-codex-substrate.md`. Listed in `blocked-urls.md` v5 as known-blocked from action. Path B only.

### 4.4 Not worth fetching anymore

- **The two Lenny URLs as articles** — confirmed video-only with paywall-stub article shell. There is no text body at the URL. See §4.2 for the YouTube route instead (Willison side done 2026-05-13; Cherny remainder still outstanding).
- **The three Klaassen Every.to siblings** — successfully fetched directly via the GH Action runner in (now-closed) fetch-urls issue #23 (the every.to URLs returned HTTP 200 from the runner despite blocking the sandbox). Re-fetch would be duplicate work.
- **`kaner.com/pdfs/ScenarioIntroVer4.pdf` + Wikipedia PDCA + Deming Institute PDSA** — optional per `research/unfetched-sources.md` "Deferred fetch-action candidates" row 5; structural conclusions firm without these.

---

## 5. Work remaining (priority order)

1. ~~**Resolve §3.1 (lost pt-2 work)**~~ — **Done 2026-05-13** via cherry-pick onto `claude/recover-pt2-drain`. See §3.1 for the recovered outcomes.

2. **Drain in-flight fetch-urls issues** when the action completes:
   - `fetched/issue-29` → drain into reports 23, followup/01, followup/07, followup/08
   - `fetched/issue-30` → drain into report 19
   - `fetched/issue-31` → drain into followup/06 (Cloudflare partial-success likely; document gaps)

3. **Curated human-review tasks (§3.2 above)**:
   - Update `architectures/00-comparison.md` §7 + §2.4
   - Update `spec-driven-ai-dev.md` with the 4-field extension
   - Add Round 2 complete stanza

4. **Retrospective decisions (§3.4 above)** — pick which of the 3 skill specs to build, which of the 15 AGENTS.md additions to adopt, which of the 7 ADRs to author.

5. **Optional fetches** — medium priority (YouTube transcripts §4.2) and low priority (§4.3) as motivated.

---

## 6. Resumption checklist for the next session

When picking this up cold:

1. `git status` — confirm clean working tree.
2. `git log origin/main..HEAD --oneline` — see what's ahead of main.
3. Check open issues: `mcp__github__list_issues` for `lago-morph/software-factory` state=OPEN. Expect any new `[fetch-urls]` issues — drain any `fetched/issue-N` branches that have landed. (Issues #29/#30/#31/#36 are all drained and closed as of 2026-05-13.)
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

These four files in `research/` are the system of record for what URLs are reachable, what isn't, and how to recover the rest:

- `research/blocked-urls.md` — cross-round canonical inventory of URLs that returned non-200 from the GitHub Actions runner. Versioned (currently v5).
- `research/blocked-urls-round-2.md` — per-issue retrieval log for Round 2's fetch passes (issues #4 and #8).
- `research/unfetched-sources.md` — URLs the action couldn't recover; categorized by which manual recovery path (A: curl with cookies; B: Save Page As; C: Reader View) will work. Includes a "Deferred fetch-action candidates" table (now 6 rows filed via #29/#30/#31 + 1 row retrospectively resolved via #23; 3 rows still deferred).
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
- Replacing the four architectures with a single "winner". The comparison stays a comparison.
- Building harness code beyond the `fetch-blocked-urls` workflow primitive.
- Adopting `harness` vocabulary across the architecture documents wholesale before the user has reviewed Round 2 synthesis report 13.
- Crawling everything blocked from the sandbox — the Klaassen / Lenny / kaner / Replit / OpenAI clusters all have either lower priority or Path-B-only recovery routes. See §4.

---

## 10. Round-by-round canonical reports (lookup table)

| Round | Reports | Status | Key contribution |
|---|---|---|---|
| 1 | `research/01-07-*`, `research/00-synthesis.md` | ✅ Complete | 7-source initial reconstruction; F1–F20 failure modes |
| 2 | `research/08-12-*`, `research/13-round-2-synthesis.md` | ✅ Complete | Jaymin book + Overstory + OpenHands substrate audits; F21–F33 |
| 3 | `research/followup/01-12-*` | ✅ Complete | 12 threads; Thread 12 (Dark Factory archive.org) resolved into report 07 without a separate file. The post-Round-3 Brier drain at `followup/12-brier-pace-layers.md` was recovered onto main via the 2026-05-13 cherry-pick (see §3.1), along with primary-source upgrades to followup/05 and followup/07. |
| 4 | `research/14-17-*` | ✅ Complete | El Kaim book: spec authorship, BMAD, council, codex+skills |
| 5 | `research/18-23-*` | ✅ Complete | Counterfactual harvest: OpenAI Codex, GitHub Copilot, Replit, Tabnine, academic foundations, Anthropic engineering |

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
| 6 | Competitor factory landscape survey | `followup/06-competitor-landscape.md` | ✅ inferential; primary upgrade pending issue #31 drain |
| 7 | Anthropic multi-agent + Husain/Shankar evals FAQ | `followup/07-evals-deepdive.md` | ✅ primary-source-anchored (upgrade recovered onto main via the 2026-05-13 cherry-pick; see §3.1). The remaining 4 anthropic.com engineering posts are pending issue #29 drain. |
| 8 | Security primitives (CaMeL + Safe YOLO + Lethal Trifecta) | `followup/08-security-primitives.md` | ✅ inferential; primary upgrade pending issue #29 drain |
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
- **13.1.2 GitHub Copilot cloud agent** → `research/19-github-copilot-cloud-agent.md`. Direct-doc primary citations pending issue #30 drain.
- **13.1.3 Replit Agent** → `research/20-replit-agent.md`. Most cluster URLs Cloudflare-gated — see §4.3.
- **13.1.4 Tabnine enterprise** → `research/21-tabnine-enterprise.md`. Primary citations landed via drained issue #27.
- **13.1.5 Academic foundations** (AlphaCode / SWE-bench / SWE-agent / CodeGen) → `research/22-academic-foundations.md`. Primary citations landed via drained issue #28.
- **13.1.6 Anthropic engineering trilogy** → `research/23-anthropic-engineering-trilogy.md`. Primary citations pending issue #29 drain.

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

**Justification.** Surfaced as a drafting-readers acknowledgement at the bottom of Shapiro's canonical "Five Levels — From Spicy Autocomplete to the Software Factory" post. Shapiro explicitly endorses the framing. None of our 24 reports + 13 followups references Radford or the "road runner economy" framing, yet Shapiro's L4–L5 narrative leans on it. If Radford's essay names a deflationary-economics dynamic our corpus currently treats as anonymous (e.g., the "code is becoming free; meaning is the moat" / "manual labor in a deflationary economy" framing that runs through the L0 description), we have a primary anchor we're missing. Could change the framing of `research/00-synthesis.md` §1 (why the methodology matters) or seed a new economics-of-the-software-factory section in `research/13-round-2-synthesis.md`.

**Effort.** Single GitHub Pages essay (`raw.githubusercontent.com`-style URL or its `nraford7.github.io` mirror). Expected reachable from action without issue; one-page WebFetch may be sufficient. ~½ hour wall time.

### Future research: platform.claude.com Agent Skills docs (Path B-only)

**Sources:**
- https://platform.claude.com/docs/en/agent-skills/overview
- https://platform.claude.com/docs/en/agent-skills/best-practices
- https://platform.claude.com/docs/en/agent-skills/security

**Justification.** Round 6 drain on `research/23-anthropic-engineering-trilogy.md` §3 surfaced that several quotes the report had attributed to Anthropic's S13 ("Equipping agents...") are not in S13 — they live in these platform docs pages instead. Current §3 retains the misattributed quotes flagged for re-anchoring. Without the actual platform-docs body, we cannot complete the re-anchoring cleanly. Affects: report 23 §3 (security guidance for Skills), and indirectly any future architecture decision that wants to cite Anthropic's *official* skill-security stance vs. the engineering-blog framing.

**Effort.** 3 pages, JS-rendered SPA so action-fetch returns content-free shells. **Path B only** (user does Save Page As after a logged-in Console session has rendered the JS). Then standard drain pass; ~30 min.

---

*End of PLAN.md v0.9.*
