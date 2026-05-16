# plan-sync.md — consolidated digest for PLAN.md update

**Date created:** 2026-05-16
**Purpose:** Single file that captures the still-load-bearing content of nine files that were cleaned up from the repo root and `research/` so PLAN.md can be brought up to date without losing audit-trail or operational tooling. **Do not treat this file as authoritative once PLAN.md has been synced — at that point it is itself disposable.**

**Files consolidated here (all now deleted from the working tree; recoverable via git history):**

1. `user-next-steps.md` (root)
2. `research/blocked-urls.md` (v5, 2026-05-11)
3. `research/blocked-urls-round-2.md` (2026-05-10 / 2026-05-11)
4. `research/blocked-urls-round-6.md` (2026-05-13)
5. `research/blocked-urls-round-7.md` (2026-05-13)
6. `research/blocked-urls-round-8.md` (2026-05-13)
7. `research/fetch-from-browser.sh` (executable bash script)
8. `research/next-fetch-batch.md` (round-8 issue draft, now executed)
9. `research/unfetched-sources.md` (2026-05-11 revision, with 2026-05-13 deferred-candidate annotations)

**Cross-check against PLAN.md v0.12 (2026-05-16):** approximately 70% of what these files contained is already reflected in PLAN.md §§1–10. This document flags the remaining 30% that may need to be folded in, and preserves operational detail (the bash script body; the per-URL outcome tables; the deferred-fetch-candidate categorization) that PLAN.md only references rather than reproduces.

---

## 1. What is missing from PLAN.md and probably should be added

These are the items in the consolidated files that I could **not** locate in PLAN.md v0.12. They are candidates for the next PLAN.md edit. Listed roughly in priority order.

### 1.1 An explicit "Definition of research phase complete" checklist

`user-next-steps.md` carried an 8-point completion checklist that PLAN.md does not have in this form. As of 2026-05-16 (folding in the Cherny drain that PLAN.md §3.5 records as done, plus the Round-9 drain), items 1–5 are now ✅ and items 6–8 remain ⏳:

1. ✅ All numbered reports + followup reports exist with a "Sources reviewed" table at the bottom.
2. ✅ `research/INDEX.md` reflects current per-report status.
3. ✅ `research/PLAN.md` shows no in-flight fetch issues unaccounted for.
4. ✅ Every Priority-1 source is primary-anchored or has an "accepted gap" decision on record. The ~7 remaining outstanding URLs are documented gaps, not unknowns.
5. ✅ Both Lenny transcripts fully drained (Willison 2026-05-13, Cherny 2026-05-14).
6. ⏳ Cross-corpus propagation sweep complete — see PLAN.md §6.1.
7. ⏳ The §3.2 curated-human-review backlog + the cumulative five-retrospective decision backlog resolved one way or the other (Update or "won't fix").
8. ⏳ Either a unified Round-1–5 synthesis exists, or the user has explicitly decided not to write one (per `research-plan.md`).

**Recommendation:** insert this checklist into PLAN.md §1 or §5 so the exit criteria for "research phase done" are stated once, in one place.

### 1.2 An explicit "In-flight tracking" / next-session-resume table

`user-next-steps.md` ended with an In-flight tracking table — distinct from PLAN.md §6 (Resumption checklist) in that it pins **per-item** "what triggers the next action." Refreshed for 2026-05-16:

| Item | State | What triggers next action |
|---|---|---|
| **Issues #41 / #42** | Drains complete in PR #44; still shown OPEN on GitHub | Agent posts a one-line closure comment linking to PR #44 (`a082310`) |
| **`research-plan.md` direction** | User decision pending | User picks: unified synthesis (yes / no); v3 single architecture (yes / no) |
| **Retrospective backlog** | Five retrospectives → 13 unbuilt skills / 45 AGENTS items / 26 ADR titles | User picks scope |
| **PLAN §3.2 curated tasks** | User decision; likely folded into the v3 architecture step | Decision on §1.1 above |
| **PLAN §6.1 cross-corpus sweep** | Mechanical, ~30 min via single `Grep` pass + small subagent dispatch | User says "do the sweep" |
| **F36/F37 numbering collision** | PLAN.md §3.6 documents the collision; not yet resolved | Lead agent triage decision (see §3.6 in PLAN.md) |
| **5 × Path-B-only URLs** | Action route exhausted | User Save-Page-As → `research/manual/` → `drain` |
| **Wayback-eligible Princeton URL** | Never tried via Wayback | Single-URL fetch attempt against `web.archive.org/web/*/pli.princeton.edu/...` |
| **`docs.github.com/.../cloud-agent/risks-and-mitigations`** | Never tried via action | File a single-URL `[fetch-urls]` issue if pursued |

**Recommendation:** add to PLAN.md §6 as §6.2 or merge into the existing §6 resumption checklist.

### 1.3 An explicit categorization of the remaining gaps as "Path B only" vs "retry-eligible"

PLAN.md §4.3 prose-style lists the remaining URLs but conflates two failure classes. Cleaner table:

| Gap | URLs | Recovery route | Affects report |
|---|---|---|---|
| **Path-B only — JS-rendered SPA** | `platform.claude.com/docs/en/agent-skills/{best-practices,security}` (2) | Browser Save Page As after JS renders, drop into `research/manual/` | `research/23-anthropic-engineering-trilogy.md` §3 (security-quote attribution open) |
| **Path-B only — Cloudflare JS challenge from action** | `openai.com/index/{harness-engineering,unlocking-the-codex-harness,introducing-swe-bench-verified}` (3) | Browser Save Page As after JS solves | `research/18-openai-codex-substrate.md` (sole reason it remains 🟡) |
| **Retry-eligible — Wayback fallback may work** | `pli.princeton.edu/.../swe-bench` (1) | Try `web.archive.org/web/*/pli.princeton.edu/blog/2023/swe-bench-can-language-models-resolve-real-world-...` | `research/22-academic-foundations.md` |
| **Retry-eligible — action never attempted** | `docs.github.com/.../cloud-agent/risks-and-mitigations` (1) | Single-URL `[fetch-urls]` issue | `research/19-github-copilot-cloud-agent.md` (would re-anchor one REFUTES; low priority since report already ✅) |

That's **5 Path-B-only + 2 retry-eligible = 7 outstanding URLs total**, matching PLAN.md's prose count.

### 1.4 Reference to the deleted `next-fetch-batch.md` issue body

PLAN.md §3.3 reports issues #41/#42 as drained but does not preserve the issue-body template that was used (rounds 6/7/8 each had a draft body before filing). If future fetch-urls issues are filed, the prior templates are useful starting points. **Appendix C below preserves the round-8 issue body verbatim.** Recommendation: add a short note in PLAN.md §3.3 or §8 pointing readers to the appendix in this file (until this file is deleted post-sync), or fold the template into a permanent `fetch-blocked-urls/issue-template.md` if more rounds are anticipated.

### 1.5 Reference to the deleted `fetch-from-browser.sh` operational tooling

PLAN.md §7 lists the script as part of the fetch-loop tooling. The script body is preserved verbatim in **Appendix B** below; if a future Path-A pass is needed, restore the script from this file or from git history. **Recommendation:** if Path-A retrieval is now genuinely obsolete (the action runner has been able to reach every host we cared about except the 5 Path-B-only ones), remove the §7 reference from PLAN.md and document the obsolescence; otherwise, restore the script.

### 1.6 The retained-on-disk evidence trail for past fetch rounds

The five `blocked-urls*.md` files served as evidence directories of what was attempted per round. PLAN.md §7 still lists them. Now that they are deleted, PLAN.md §7's bullet list of these files should either:

(a) be replaced with a single "fetch round outcomes were folded into `plan-sync.md` Appendix A and removed 2026-05-16; restore from git if a per-URL re-trace is needed," **or**
(b) be deleted outright on the grounds that the per-URL outcomes are already cross-referenced from the affected reports (each report's "Sources reviewed" table flags ✅ / 🟡 / ❌ per URL).

**Appendix A below preserves the per-URL outcomes in compressed form** so option (a) is workable.

### 1.7 Cross-corpus lessons that were stated only in `blocked-urls-round-*.md`

PLAN.md captures the most important cross-corpus lessons (e.g., R8.1 arXiv `/e-print/`, the "Cloudflare-blocks did NOT propagate to action runner" finding). One lesson that I could not find an explicit citation for in PLAN.md:

- **Lesson R7.3 — sibling-URL cross-link heuristic.** When a target URL 404s but a sibling URL on the same domain returns 200, ALWAYS read the sibling for cross-links to the missing target. Issue #29's `the-five-levels-of-agentic-coding` 404 was a slug-guess miss; the correct slug `the-five-levels-from-spicy-autocomplete-to-the-software-factory` was discovered by reading the sidebar of the sibling companion post that DID fetch successfully. Recommendation: fold into PLAN.md §8 or into the `research-pipeline` skill's documented heuristics.

- **Lesson R7.1 nuance — `platform.claude.com` ≠ `code.claude.com`.** PLAN.md mentions the platform.claude.com SPA issue, but the contrast with `code.claude.com/docs/...` (server-rendered, fetchable) is useful for predicting outcomes on future Anthropic docs URLs. Worth a line in PLAN.md §4.3 or §7.

- **Lesson R8.4 — Connectors ≠ MCP.** The Replit drain refuted a corpus-wide reconstruction. The orchestrator suggested grepping for "Connectors are powered by MCP" or similar phrasings across reports to make sure the conflation didn't propagate elsewhere. PLAN.md does not appear to have queued this grep. Recommendation: add to §6.1's cross-corpus propagation flags.

- **Lesson R8.5 — third-party mirrors as fallback.** Three load-bearing Replit reconstructions (Mastra-as-implementation, ~100-line replit.md auto-condensation, "$0.06 floor / multi-dollar ceiling" billing) survived the original cross-check across ≥2 sources, then turned out to be unverified by primaries. Implication for the research-pipeline skill: when only third-party mirrors agree but the primary is absent, mark the claim 🟡 pending-primary-fetch rather than ✅. Recommendation: this is a skill update, not a PLAN.md update, but worth flagging.

### 1.8 The "Recommended future fetches" list from `blocked-urls.md` v5

`blocked-urls.md` v5 carried a "Sources surfaced by primary access" list of references to chase. Most are now resolved; the residuals worth keeping on a wishlist are:

- **From StrongDM Factory homepage footnote 1:** Luke PM "The Software Factory"; Sam Schillace "I Have Seen the Compounding Teams". (Status: not in corpus; mid-priority for any future strongdm-attribution audit.)
- **YouTube videos referenced by jaymin-book** — three K7nY3MUzDuk / njRAmppPvFk / 95TEFWdo6Mw URLs. Would need a transcript-extraction service.
- **El Kaim's broader Medium corpus** — 10+ unread posts logged in the round-7 future-research cluster. PLAN.md's "Future research" section at the bottom (not in the file segment I read) should already reference this.

These are below the bar for active follow-up but should not be silently dropped. Recommendation: gather them as a single "Future research wishlist" appendix in PLAN.md.

---

## 2. What is in those files that is ALREADY in PLAN.md

For traceability: these items appear in both the deleted files and in PLAN.md, so PLAN.md does not need editing to capture them.

- ✅ All round-6 / round-7 / round-8 per-issue summary stats (PLAN.md §3.3 + §10).
- ✅ Cherny full transcript drain status (PLAN.md §3.5).
- ✅ Willison full transcript drain status (PLAN.md §3.5 archive + §10 row "Round 8").
- ✅ Issues #41/#42 still showing OPEN; closure pending (PLAN.md §5 task 2, §6 step 3).
- ✅ The CaMeL arXiv `/e-print/` recovery (PLAN.md §3.3 round-8 row + §10).
- ✅ Replit / Codex / Copilot reports flipped status (PLAN.md §1 done-list + §10).
- ✅ El Kaim Dark Factory article unlocked (PLAN.md §1 + §10 row Round 4).
- ✅ `platform.claude.com/.../agent-skills/overview` Path-B'd → report 23 §3 attribution closed (PLAN.md §10 row 7).
- ✅ The 5 retrospectives + 13 / 45 / 26 cumulative backlog (PLAN.md §3.4).
- ✅ `research-plan.md` direction-pending status (PLAN.md §5 task 3).
- ✅ Cross-corpus propagation flags from round-7 Shapiro drain (PLAN.md §6.1).
- ✅ The "before invoking Path B, file a `[fetch-urls]` issue first" lesson (PLAN.md §3.3).
- ✅ Round-9 manual drain → reports 25 + 26 + report 12 §2.5 extension (PLAN.md §1 + §3.6 + §10 row 9).
- ✅ F36/F37 numbering collision (PLAN.md §3.6).

---

## 3. Per-file disposition (what was preserved here, what was already redundant)

### 3.1 `user-next-steps.md`

**Date:** 2026-05-14. Superseded section by section by PLAN.md v0.10–v0.12. Status of each section:

- "What changed since 2026-05-13 audit" — historical; fully absorbed by PLAN.md v0.10's §1 done-list.
- "Current state of pending drains" — fully resolved (Cherny drain landed 2026-05-14).
- "Audit: what valuable sources remain partial/blocked" — replaced by PLAN.md §4.3. **Slight gap:** the explicit Priority-1 / Priority-2 / Priority-3 tiering is not in PLAN.md; if useful, fold into §4.3 as a recommended ordering for future Path-B work. (My §1.3 above is the cleaner version.)
- "The synthesis-collapse decisions" — captured in PLAN.md §5 task 3.
- "Retrospective backlog" — captured in PLAN.md §3.4.
- "Cross-corpus propagation flags" — captured in PLAN.md §6.1.
- "Definition of research phase complete" — **NOT in PLAN.md.** See §1.1 above.
- "Recommended order of operations" — overlaps with PLAN.md §5 (work remaining); the prose-style ordering in the file is a different framing but the contents are the same.
- "In-flight tracking" — **NOT in PLAN.md in this tabular form.** See §1.2 above.

### 3.2 `research/blocked-urls.md` v5

**Date:** 2026-05-11. The cross-round canonical URL inventory.

- "What is now accessible" table — historical; the URLs listed are all ✅ in their target reports' Sources-reviewed tables.
- "What remains BLOCKED" table — was 3 URLs at v5 time; 2 (medium.com/@welkaim/about, welkaim.medium.com) since RESOLVED 2026-05-13 per PLAN.md §4.3 item 1; el-kaim Dark Factory article since RESOLVED.
- "Recommended future fetches" — see §1.8 above for residuals.
- "Effect on the architectures" — historical corrections, all now propagated into the architecture docs and into the synthesis revision notes. Specific items already captured:
  - DTU = Digital Twin Universe (corrected in all four architecture specs)
  - The "Willison 4 agents → 11 AM" reversal-of-reversal (now in synthesis §"Revision notes", §"Parallelism", §"Quick anchor data" and the round-1 HN-row table)
  - Self-improving prompts pattern added to Architecture 2
  - Scenarios partially agent-generated added to synthesis §5.1 and Architecture 1
  - Attractor "graph-structured generically; DOT community convention" correction in synthesis §3.2 / §3.8
  - Compound engineering canonical loop is 4-step not 5 (corrected in Architecture 2)
  - Looking-the-part hazard added to F7 in synthesis §4

### 3.3 `research/blocked-urls-round-2.md`

**Date:** 2026-05-10 / 2026-05-11. Per-issue retrieval log for fetch issues #4 and #8.

Compressed outcomes:
- Issue #4: 13 of 14 URLs returned HTTP 200; 1 deferred (YouTube transcripts).
- Issue #8 (Wayback supplements): Substack manifesto and arXiv HTML render recovered; Boris Cherny Lenny interview paywall persisted in Wayback (since RESOLVED via 2026-05-14 transcript drop).
- The full per-URL table is preserved verbatim in **Appendix A** below.

### 3.4 `research/blocked-urls-round-6.md`

**Date:** 2026-05-13. Issues #29 / #30 / #31 per-URL outcomes.

Compressed in **Appendix A**. Key lesson (now in PLAN.md §3.3): "Cloudflare-blocked" classifications on most hosts were stale — the runner reaches them fine.

### 3.5 `research/blocked-urls-round-7.md`

**Date:** 2026-05-13. Issue #36 per-URL outcomes (7 URLs; 5 HTTP 200 but only 2 usable).

Compressed in **Appendix A**. Three corpus-wide lessons R7.1 / R7.2 / R7.3 — R7.1 and R7.2 are in PLAN.md; R7.3 (sibling-URL cross-link heuristic) flagged in §1.7 above as missing.

### 3.6 `research/blocked-urls-round-8.md`

**Date:** 2026-05-13. Issues #41 + #42 per-URL outcomes.

Compressed in **Appendix A**. Five corpus-wide lessons R8.1–R8.5 — R8.1 (arXiv `/e-print/`) is in PLAN.md; R8.2 (openai.com/index/* JS-challenged-body) is partially in PLAN.md §4.3; R8.3 (canonical-re-find > slug-pattern-guessing) is implicit but not stated; R8.4 (Connectors ≠ MCP) is **not** in PLAN.md per §1.7 above; R8.5 (third-party-mirrors-fallback flag) is **not** in PLAN.md (skill-level recommendation per §1.7).

### 3.7 `research/fetch-from-browser.sh`

Bash script invoked locally with browser cookies to do Path-A retrieval. The script body is preserved verbatim in **Appendix B**. PLAN.md §7 references the script; if Path-A is genuinely obsolete, that reference should be removed from PLAN.md (see §1.5 above).

### 3.8 `research/next-fetch-batch.md`

Draft body for the round-8 `[fetch-urls]` issues #41 + #42. Both issues filed and drained per PLAN.md §3.3. The draft body is preserved verbatim in **Appendix C** as a template for future fetch-urls issues. If no further fetch-urls issues are expected, this is disposable; otherwise, fold the template into a permanent `fetch-blocked-urls/issue-template.md` and reference from PLAN.md §8 (which already documents the workflow).

### 3.9 `research/unfetched-sources.md`

**Date:** 2026-05-11 (with 2026-05-13 deferred-candidate annotations).

- "Currently unfetched" table — at the time it listed 4 URLs (medium.com/@welkaim/about, welkaim.medium.com, two Lenny URLs). As of 2026-05-16, the welkaim pair is RESOLVED 2026-05-13 (Path B drop, see PLAN.md §4.3 item 1); both Lenny URLs are confirmed-video-only with full YouTube transcripts dropped and drained. **Effectively the entire table is now empty.**
- "How to recover" — Path A / Path B / Path C operational instructions. Preserved verbatim in **Appendix D** as a reference for any future Path-B work.
- "Deferred fetch-action candidates" — the 9-row table cataloging URLs to file as `[fetch-urls]` issues. Status as of 2026-05-13 / 2026-05-16:
  - Row 1 (Shapiro): ✅ Filed in #29
  - Row 2 (Anthropic engineering × 4): ✅ Filed in #29
  - Row 3 (Hamel + Simon evals): ✅ Filed in #29
  - Row 4 (Simon + arXiv security): ✅ Filed in #29
  - Row 5 (Kaner/PDCA/PDSA): ⏸ Optional, not filed
  - Row 6 (Devin/Factory/8090/Superconductor/Superpowers): ✅ Filed as #31 + #36 round-7 supplement
  - Row 7 (docs.replit.com/* + blog.replit.com/*): ✅ Filed as #41 (after the file's "defer until v6 catalog updates" guidance was over-ridden 2026-05-13)
  - Row 8 (developers.openai.com/codex/* + openai.com/index/*): ✅ Filed as #41 (Codex docs all 200'd from action; openai.com/index/* still Path B)
  - Row 9 (docs.github.com/en/copilot/*): ✅ Filed as #30 + canonical re-finds in #42
  - Row 10 (every.to/chain-of-thought × 3): ✅ Resolved via earlier issue #23

**All rows except row 5 are now resolved.** Row 5 is the only outstanding deferred candidate; structural conclusions firm without it. Recommendation: if PLAN.md ever explicitly references "deferred fetch-action candidates," update the reference to point at this file (until this file is deleted post-sync) or fold the row-5 status into PLAN.md §4.4 ("Not worth fetching anymore") on the grounds it has been explicitly classified optional.

---

## Appendix A — per-round per-URL outcomes (compressed)

Preserved here so the corpus' fetch-history audit trail is not lost when the five `blocked-urls*.md` files are deleted. For each round, only the URL + final status + drain target. Long explanations cut; consult git history for the full files.

### Round 2 — issues #4 and #8

| # | URL | Final status | Drain target |
|---|---|---|---|
| 1 | jayminwest.com/agentic-engineering-book | ✅ via #4 | report 08 / 09 |
| 2 | jayminwest.com/.../6-harnesses | ✅ via #4 | report 09 |
| 3 | jayminwest.substack.com/p/a-manifesto-for-agentic-development | ✅ via #8 Wayback | report 09 §9 |
| 4 | docs.all-hands.dev/usage/how-to/headless-mode | ✅ via #4 | report 11 |
| 5 | docs.all-hands.dev/ | ✅ via #4 | report 11 |
| 6 | arxiv.org/abs/2511.03690 | ✅ via #4 | report 11 |
| 7 | arxiv.org/html/2511.03690v2 (via Wayback) | ✅ via #8 Wayback | report 11 v0.2 |
| 8 | github.com/marketplace/actions/openhands-ai-action | ✅ via #4 | report 11 |
| 13 | deepwiki.com/All-Hands-AI/OpenHands/11.3-cli-and-deployment-modes | ✅ via #4 | report 11 |
| 14 | langchain.com/blog/agentic-engineering-redefining-software-engineering | ✅ via #4 | report 12 §2.2 |
| 16 | ibm.com/think/topics/agentic-engineering | ✅ via #4 | report 12 §2.4 |
| 17 | addyosmani.com/blog/agentic-engineering/ | ✅ via #4 | report 12 §2.1 |
| 19 | kiro.dev/ | ✅ via #4 | report 12 §2.5 |
| 20 | cloud.google.com/discover/what-is-agentic-coding | ✅ via #4 | report 12 §2.3 |
| 15 | mindstudio.ai/blog/what-is-agentic-engineering | skipped (saturation) | — |
| 18 | agenticengineer.com/tactical-agentic-coding | not yet attempted | — |
| 9–12 | YouTube transcripts (×3) + skillsllm.com/skill/overstory | deferred (transcript service needed) | — |

### Round 6 — issue #29 (Anthropic / Hamel / Simon / arXiv / Shapiro × 18)

| URL pattern | Outcome | Drained into |
|---|---|---|
| anthropic.com/engineering/effective-harnesses-for-long-running-agents | ✅ 200 | report 23 §2 |
| anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills | ✅ 200 | report 23 §3 |
| anthropic.com/engineering/building-c-compiler | ✅ 200 | report 23 §4 |
| anthropic.com/engineering/harness-design-long-running-apps | ✅ 200 | report 23 §5 |
| anthropic.com/engineering/claude-code-sandboxing | ✅ 200 | report 23 §8 (NEW) |
| hamel.dev/blog/posts/evals-faq/ | ✅ 200 | followup/07 §3 |
| hamel.dev/blog/posts/llm-judge/ | ✅ 200 | followup/07 §3.9 |
| hamel.dev/blog/posts/field-guide/ | ✅ 200 | followup/07 §4.5 |
| hamel.dev/blog/posts/evals/ | ✅ 200 | followup/07 §0 |
| simonwillison.net/2025/Jul/3/faqs-about-ai-evals/ | ✅ 200 | followup/07 |
| simonwillison.net/2025/Jun/14/multi-agent-research-system/ | ✅ 200 | followup/07 §2.6 |
| simonwillison.net/2025/Apr/11/camel/ | ✅ 200 | followup/08 §3 |
| simonwillison.net/2025/Jun/16/the-lethal-trifecta/ | ✅ 200 | followup/08 §1 |
| simonwillison.net/2023/Apr/25/dual-llm-pattern/ | ✅ 200 | followup/08 §2 |
| arxiv.org/abs/2503.18813 | ✅ 200 | followup/08 §3a |
| arxiv.org/html/2503.18813v2 | ❌ 404 | (recovered via /e-print/ in round 8) |
| danshapiro.com/blog/2026/01/the-five-levels-of-agentic-coding | ❌ 404 slug-guess miss | (recovered via correct slug in round 7) |
| danshapiro.com/blog/2026/02/you-dont-write-the-code | ✅ 200 | followup/01 §"companion post" |

Major refutations from #29 drain: report 23 Opus version 4.5 not 4.6; testing tool Puppeteer MCP not Playwright; companion repo `claude-quickstarts/autonomous-coding` not `cwc-long-running-agents`; several security quotes attributed to S13 actually from platform.claude.com Skills overview. followup/08 trifecta-leg quotes 3 confabulated; CaMeL attribution corrected to Google DeepMind + ETH Zürich. followup/07 ">90% expert agreement" attribution corrected to Hamel's llm-judge (Honeycomb/Phillip Carter) not the FAQ.

### Round 6 — issue #30 (GitHub Copilot docs × 9)

3 of 9 returned HTTP 200; 6 returned HTTP 404 (GitHub docs reorgs, not blocks). The 6 URLs needed canonical re-finds, all resolved in round 8 #42. All 6 round-8 re-finds returned ✅ 200.

### Round 6 — issue #31 (Devin / Factory / 8090 / Superconductor / Superpowers × 9)

6 of 9 returned HTTP 200. **Cloudflare blocks did NOT propagate to action runner.** Major refutations: Devin pricing (Free/Pro $20/Max $200/Teams $80/Enterprise — no public ACU); Factory adds Droid Computers primitive; superconductor.io was wrong domain (live product at .com). 3 upstream 404s (cognition.ai/blog/devin, factory.ai/product, 8090.inc/blog).

### Round 7 — issue #36 (7 URLs)

- danshapiro.com/.../the-five-levels-from-spicy-autocomplete-to-the-software-factory → ✅ → followup/01
- arxiv.org/pdf/2503.18813 → 🟡 metadata-only (PDF binary; html2text can't extract; recovered as /e-print/ in round 8)
- arxiv.org/html/2503.18813v1 → ❌ 404 (same as v2)
- superconductor.com → ✅ → followup/06 §4 (replaces wrong-domain hit)
- platform.claude.com/docs/en/agent-skills/{overview, best-practices, security} × 3 → ❌ JS-SPA shells (overview later Path-B'd in round 7; the other two still pending Path B)

### Round 8 — issue #41 (Replit / Codex / SWE-bench × 24)

20 of 24 ✅. Replit (13/13 ✅) and developers.openai.com/codex/* (5/5 ✅) all drained into reports 20 and 18. 4 Cloudflare failures: openai.com/index/{harness-engineering, unlocking-the-codex-harness, introducing-swe-bench-verified}, pli.princeton.edu/.../swe-bench. Major Replit refutations: ~100-line replit.md auto-condensation not in primary; "$0.06/multi-dollar" billing not in primary; Mastra-as-implementation not in primary; Connectors are not all "powered by MCP" (Connectors derive from OpenInt acquisition; MCP-Servers is a separate scanner-gated catalog).

### Round 8 — issue #42 (GH Copilot canonical re-finds + arXiv CaMeL × 10)

6/6 Copilot canonical URLs ✅, all drained into report 19 (flipped to ✅; new §3.1 on Copilot Spaces). Major refutations: "Copilot agent can only push to copilot/* branches" no longer in canonical concept page; "Agent PRs require human approval before CI/CD" also dropped from canonical concept page. Copilot Workspace docs (2 URLs) confirmed sunset (no docs successor). **arXiv 2503.18813 paper body recovered via `arxiv.org/e-print/2503.18813` LaTeX-tarball route** (manual gunzip | tar -xf; saved to `reference-only/camel-paper/`); followup/08 §3 expanded from 7 to ~15 subsections.

---

## Appendix B — `research/fetch-from-browser.sh` (verbatim)

```bash
#!/usr/bin/env bash
# fetch-from-browser.sh — pull URLs that automated fetchers can't reach
#
# Use this when sources are behind:
#   - a paywall (Lenny, Every.to, Substack-paid posts)
#   - a Cloudflare interactive challenge that GitHub Actions runners can't solve (el-kaim)
#   - any login-required page
#
# It uses your browser's cookies (you provide a Netscape-format cookies.txt)
# plus a recent realistic User-Agent. Output goes to research/manual/, where
# the next research-pipeline-skill activation will pick it up.
#
# Usage:
#   bash research/fetch-from-browser.sh <path-to-cookies.txt> [url-list-file]
#
# Default url-list-file is research/unfetched-sources.md (the script extracts
# URLs from the markdown table). Pass any file with one URL per line to
# override.
#
# Notes:
#   - For Cloudflare interactive challenges (e.g. el-kaim), even cookies+UA
#     won't help — JavaScript challenge can't be solved by curl. For those,
#     use the browser's File → Save Page As → Web Page Complete and drop
#     the resulting .html into research/manual/ directly.
#   - For SPA / heavily JS-rendered pages, the saved HTML may be skeletal.
#     Reader View → copy text → paste into research/manual/<slug>.txt is a
#     reliable fallback.
#
# After files land in research/manual/, commit and push them. A subsequent
# research-pipeline activation will scan for new content and dispatch
# subagents to incorporate them, then delete the raw files.

set -euo pipefail

COOKIES="${1:?Usage: $0 <cookies.txt> [url-list-file]}"
URL_LIST="${2:-research/unfetched-sources.md}"
OUT_DIR="research/manual"
UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'

if [ ! -f "$COOKIES" ]; then
  echo "ERROR: cookies file not found: $COOKIES" >&2
  echo "Export from your browser via a 'Get cookies.txt' extension first." >&2
  exit 1
fi

mkdir -p "$OUT_DIR"

# Extract https://... URLs from the source file (works for plain lists or
# markdown tables — we just grep for URLs and dedupe).
mapfile -t URLS < <(grep -oE 'https?://[^[:space:]<>")|]+' "$URL_LIST" \
  | sed 's/[[:punct:]]*$//' \
  | sort -u)

if [ "${#URLS[@]}" -eq 0 ]; then
  echo "No URLs found in $URL_LIST" >&2
  exit 0
fi

slug_for() {
  local url="$1"
  local sha tail
  sha=$(printf '%s' "$url" | sha1sum | cut -c1-10)
  tail=$(printf '%s' "$url" \
    | sed -E 's|^https?://||; s|[^A-Za-z0-9._/-]|_|g; s|/+|__|g' \
    | cut -c1-80)
  printf '%s_%s' "$sha" "$tail"
}

echo "Fetching ${#URLS[@]} URL(s) into $OUT_DIR using cookies from $COOKIES"
echo

i=0
for url in "${URLS[@]}"; do
  i=$((i + 1))
  slug=$(slug_for "$url")
  out="$OUT_DIR/${slug}.html"

  echo "[$i/${#URLS[@]}] $url"
  http_code=$(curl --silent --show-error --location \
    --max-time 30 \
    --user-agent "$UA" \
    --cookie "$COOKIES" \
    --output "$out" \
    --write-out '%{http_code}' \
    "$url" || true)

  bytes=0
  [ -f "$out" ] && bytes=$(wc -c < "$out" | tr -d ' ')

  if [ "${http_code:-000}" = "200" ] && [ "$bytes" -gt 5000 ]; then
    # Quick sanity check — Cloudflare stubs are tiny and contain "Just a moment"
    if grep -q "Just a moment\|Attention Required\|cf-mitigated" "$out" 2>/dev/null; then
      echo "  -> got Cloudflare challenge ($bytes bytes); curl can't solve it. Use browser Save Page As." >&2
      mv "$out" "$out.cloudflare-stub"
    else
      echo "  -> saved $out ($bytes bytes)"
    fi
  else
    echo "  -> FAILED (HTTP ${http_code:-000}, $bytes bytes)" >&2
  fi
done

echo
echo "Done. Files in $OUT_DIR — commit, push, then ask Claude to drain new content."
```

---

## Appendix C — `research/next-fetch-batch.md` (round-8 issue-body template, verbatim)

```
Round-8 follow-up batch. 22 URLs across Replit Agent docs/blog, OpenAI Codex docs, OpenAI SWE-bench announcement, and Princeton PLI SWE-bench post. All currently 🟡 reconstructed in the corpus via WebSearch / mirror sites; never tried via the action. Round-6 lesson: older "blocked" tags on these hosts may be stale. Try the action first; escalate to Path B only on real failures.

### Replit Agent (13 URLs → research/20-replit-agent.md)

https://docs.replit.com/core-concepts/agent
https://docs.replit.com/replitai/replit-dot-md
https://docs.replit.com/core-concepts/agent/plan-mode
https://blog.replit.com/connectors
https://docs.replit.com/replitai/warehouse-connectors
https://docs.replit.com/replitai/mcp/overview
https://docs.replit.com/replitai/agents-and-automations
https://docs.replit.com/replitai/canvas
https://docs.replit.com/replitai/app-testing
https://docs.replit.com/cloud-services/deployments/autoscale-deployments
https://docs.replit.com/billing/ai-billing
https://blog.replit.com/introducing-agent-3-our-most-autonomous-agent-yet
https://blog.replit.com/introducing-agent-4-built-for-creativity

### OpenAI Codex (7 URLs → research/18-openai-codex-substrate.md)

https://developers.openai.com/codex
https://developers.openai.com/codex/guides/agents-md
https://developers.openai.com/codex/subagents
https://developers.openai.com/codex/agent-approvals-security
https://developers.openai.com/codex/cloud/environments
https://openai.com/index/harness-engineering/
https://openai.com/index/unlocking-the-codex-harness/

### SWE-bench (2 URLs → research/22-academic-foundations.md)

https://openai.com/index/introducing-swe-bench-verified/
https://pli.princeton.edu/blog/2023/swe-bench-can-language-models-resolve-real-world-github-issues/
```

**Workflow for any future fetch-urls issue:**

1. Open a GitHub issue titled `[fetch-urls] <round> — <hosts>` with the URL block above and label `fetch-urls` (Triage-role human applies the label).
2. The `fetch-blocked-urls` action commits `fetched/issue-<N>` branch and posts a per-URL HTTP-status comment.
3. Activate the `research-pipeline` skill (`/drain`) in a fresh session.
4. The drain dispatches ~3 subagents (one per target report) in parallel, anchors verbatim quotes, refutes reconstructions where they contradict primary, flips 🟡 → ✅ rows.
5. Update the relevant `research/blocked-urls-round-N.md` (or, going forward, append to the consolidated PLAN.md §3.3 round table) with per-URL outcomes — especially: which hosts were action-reachable after all.
6. Open follow-up PR.

---

## Appendix D — Manual fetch operational procedures (Path A / B / C)

Preserved from `research/unfetched-sources.md`. Reference for any future Path-B work, especially the 5 Path-B-only URLs in §1.3.

### Path A — `curl` with browser cookies (fastest if you already have a cookies file)

1. Export cookies from your browser to a Netscape-format file:
   - **Firefox:** the `cookies.txt` extension (or read directly from `~/.mozilla/firefox/<profile>/cookies.sqlite`).
   - **Chrome / Brave / Edge:** the `Get cookies.txt LOCALLY` extension.
2. Save as `~/cookies.txt` (or any path).
3. Run the bash script in Appendix B above (`bash research/fetch-from-browser.sh ~/cookies.txt`).
4. Output lands in `research/manual/`. Commit and push; a future Claude session will see the new files and incorporate them via the `research-pipeline` skill's Phase 0 drain.

**Caveat:** for Cloudflare interactive challenges (e.g. the el-kaim case, before the article was Path-B'd) even cookies+UA won't help — the JavaScript challenge can't be solved by curl. Use Path B instead.

### Path B — browser "Save Page As → Web Page, Complete"

For pages where cookies-with-curl still fails (Cloudflare interactive JS challenge; SPA-rendered docs like platform.claude.com), no headless tool will get past it. Open the page in your browser, use **File → Save Page As → Web Page, Complete**, and drop the resulting `.html` (and the companion `_files/` folder if you want assets) into `research/manual/`. Commit and push.

### Path C — Reader View → text export

For paywalled articles where you've already read the body, the browser's Reader View typically exposes the full text (paywalls are usually CSS overlays that Reader View bypasses). Copy the rendered article text and paste into `research/manual/<short-slug>.txt`. Less faithful than HTML but enough for verbatim quoting.

### Disposition after retrieval

Once new files appear under `research/manual/` (or any subdirectory of `research/`), the next research-pipeline-skill activation will scan and dispatch subagents to incorporate them into the relevant reports, then delete the raw files. To trigger that drain explicitly, prompt: *"check `research/` for new content and incorporate it"*.

---

## 4. Suggested next-step prompt for the user (when they want to sync PLAN.md)

When ready to update PLAN.md from this file, something like:

> "Update `research/PLAN.md` to fold in the items flagged in `research/plan-sync.md` §1.1–§1.8. Adjust §7 to reflect the removal of the five `blocked-urls*.md` files and `fetch-from-browser.sh`; the per-URL audit trail is in `plan-sync.md` Appendix A. After PLAN.md is current, delete `research/plan-sync.md`."

Or, scoped: "just §1.1 and §1.2" if the rest is too much to absorb in one pass.

---

*End — `research/plan-sync.md` v0.1*
