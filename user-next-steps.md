# User Next Steps — End-of-Research-Phase Audit

**Date:** 2026-05-13
**Author:** Lead agent
**Status snapshot:** PR #40 awaiting merge (audit cleanup); issue #41 in-flight (round-8 fetch); Lenny full transcripts pending from user.

---

## State of pending drains

- **Phase 0 inventory empty.** `research/manual/` clean; `research/fetched/` retains only the 11 expected 404-evidence files. **Lenny full transcripts will land on `research/manual/` when the user finishes them** — drain pass at that point will trigger automatically.
- **Issue #41 (round-8 fetch) in-flight.** 22 URLs across Replit, OpenAI Codex, SWE-bench. The `fetch-blocked-urls` action will commit a `fetched/issue-41` branch and post a per-URL summary comment when done.

---

## Audit: where valuable sources are partial / reconstructed / blocked

Triaging the 93 non-✅ rows across all `research/**/*.md` Sources tables down to actionable categories.

### Priority 1 — Worth a single new batched `[fetch-urls]` issue (~28 URLs, all action-reachable per round-6 lesson) — **filed as issue #41 on 2026-05-13**

| Cluster | Affected report | URLs | Why valuable |
|---|---|---|---|
| **Replit Agent — 13 URLs all 🟡** | `research/20-replit-agent.md` | `docs.replit.com/*` (10) + `blog.replit.com/*` (3) | Every claim in report 20 is currently WebSearch-reconstructed. `docs.replit.com` was tagged "Cloudflare-gated, action probably 403s" in older blocked-urls notes; round 6 showed those tags were often wrong. |
| **OpenAI Codex — 7 URLs all 🟡** | `research/18-openai-codex-substrate.md` | `openai.com/index/*` (2) + `developers.openai.com/codex/*` (5) | Same situation — WebSearch-reconstructed via mirror sites. Tag says "known blocked from action" but never re-tested post-round-6. |
| **GitHub Copilot — 6 follow-up URLs** | `research/19-github-copilot-cloud-agent.md` | 6 `docs.github.com` URLs that 404'd in #30 | **Out of scope for issue #41** — need WebSearch first to find new canonical paths (GH docs reorganized). 5 report claims currently flagged `[2026-05-13 404; pending re-anchor]`. Stage a separate fetch issue after WebSearch surfaces new URLs. |
| **arXiv CaMeL paper body** | `research/followup/08-security-primitives.md` | `arxiv.org/e-print/2503.18813` (LaTeX source) | Body still ungettable via PDF. LaTeX source could be pandoc'd. Or just accept the gap (abstract + Willison's writeup are enough — decision already on record). |
| **OpenAI SWE-bench announcement** | `research/22-academic-foundations.md` | 2 OpenAI URLs (CF-blocked) | Small. Included in issue #41. |

### Priority 2 — Path B only (user must do these)

| Cluster | Affected report | URLs | Notes |
|---|---|---|---|
| **2 of 3 platform.claude.com Agent Skills docs** | `research/23-anthropic-engineering-trilogy.md` | `.../agent-skills/best-practices` + `.../security` | JS-rendered SPA; user already Path B'd the overview. The two remaining would close the rest of the Skills security attribution. **Lower priority** — overview is the high-value one and it's done. |

### Priority 3 — Already in user's hands

- **Lenny Cherny full transcript (60 min remainder)** → `research/followup/03` + `research/06`. **Highest leverage of all pending** — full parallel-session architecture, third "new team member principle," $/day cost, etc.
- **Lenny Willison full transcript (60 min remainder)** → `research/05` + `research/06`. Full Challenger-disaster argument, lethal-trifecta discussion.

### Priority 4 — Accept the gap (not worth chasing)

| Cluster | Affected report | Why drop |
|---|---|---|
| 2389.ai DOT-file essay + gastownhall.ai 403s | `research/followup/04-gastown-beads.md` | Six 403/404s; report itself is firm on the primitive without them. |
| 4 jaymin-book example dirs | `research/12-adjacent-ecosystem.md` | Cheap (raw.githubusercontent.com) but the substrate-audit is firm. |
| 5 OpenHands repo source-code reads | `research/11-openhands-substrate-audit.md` | Doc + paper coverage is sufficient. |
| IBM "agentic engineering" extraction nav-chrome issue | `research/12` §2.4 | Re-extraction nice-to-have only. |
| Anthropic *Demystifying evals* | `research/followup/07` | Explicitly deprioritized — Hamel llm-judge is the canonical operational manual. |

### Pending corrections that don't need new content (done on PR #40)

1. ✅ **Cross-corpus Shapiro reversal-of-reversal propagation** (PLAN §6.1): added "Note on attribution" in `research/07-dark-factory.md` §1 flagging that El Kaim's restatement of Shapiro's framework *conflates the canonical Five Levels post with the companion post* and adds his own compressions. (Reports 01/02 grep showed StrongDM team-size datum traces to the StrongDM site itself, not Shapiro — so that §6.1 item is moot.)
2. ✅ **Anthropic Skills cookbook cross-refs into report 04** (flagged by the Anthropic Skills drain): 5 specific corrections — stricter name/description schema constraints, `allowed-tools` is a Claude Code extension not canonical SKILL.md, Level-1 budget ~100 tokens not "30–50", Level-3 framing "effectively unlimited" vs report 04's 50-file/1MB cap, cross-surface non-portability.

### Bigger pending work that needs user decisions (PLAN §3.2 / §3.4)

- **`architectures/00-comparison.md` §7 + §2.4 update** (substrate-stack recommendation + F21–F33 catalogue extension)
- **`spec-driven-ai-dev.md` 4-field extension** (non-goals, decision-seeds, invariant-with-bindingHint, explicit Intent)
- **3 unbuilt skill specs from retrospective + 15 AGENTS.md suggestions + 7 proposed ADRs** — need pick-list from user

---

## Definition of "research phase complete"

The research phase is complete when:

1. ✅ All 24 numbered reports + 13 followup reports exist with a "Sources reviewed" table at the bottom.
2. ✅ `research/INDEX.md` reflects current per-report status.
3. ✅ `research/PLAN.md` shows no in-flight fetch issues unaccounted for.
4. ⏳ Every Priority-1 source is primary-anchored or has an "accepted gap" decision on record. (After issue #41 drains + the 6 GH Copilot URLs are re-found and drained, we're there.)
5. ⏳ Both Lenny transcripts are fully drained (~90 min each). (After user finishes overnight transcription + drain.)
6. ❓ The PLAN §3.2 / §3.4 curated-human-review backlog has been resolved one way or the other (Update or "won't fix").

Items 1–3 are met now. Items 4–5 are close. Item 6 needs a pick-list from the user.

---

## Recommended order of operations to close out the research phase

1. **Merge PR #40** (audit cleanup) — small, no new content.
2. **Wait for issue #41 to drain.** When `fetched/issue-41` lands on origin, trigger `drain` in a new session; ~3 parallel subagents fold 22 URLs into reports 18, 20, 22.
3. **Drain Lenny full transcripts** whenever the user drops them in `research/manual/`. Trigger `drain`. Reverses any "still un-primary-sourced" framings remaining in `research/06-hn-and-lenny.md` §"Outstanding questions" and the followup/03 / report 05 partial-status flags.
4. **(Optional) File a second fetch issue** for the 6 GitHub Copilot re-find URLs after WebSearch confirms their new canonical paths.
5. **(Optional, Path B)** User Path-B exports the remaining 2 platform.claude.com Skills pages.
6. **User decides on PLAN §3.2 / §3.4** — architecture-comparison update, spec template extension, retrospective skills + ADRs + AGENTS.md. These are *methodology synthesis*, not research. After they're picked, research phase is unambiguously closed and the next phase ("build out the chosen architecture") can begin.

---

## In-flight tracking (for next session)

| Item | State | What triggers next action |
|---|---|---|
| **PR #40** (audit cleanup) | Open, awaiting merge | User merges to main |
| **Issue #41** (round-8 fetch) | Open, action will run | `fetched/issue-41` branch appears → `drain` |
| **Lenny full transcripts** | User running overnight | Files land in `research/manual/` → `drain` |
| **GH Copilot 6 re-finds** | Not started | WebSearch for new docs paths → new fetch issue |
| **platform.claude.com 2 SPA pages** | Path B only | User Save-Page-As → `research/manual/` → `drain` |
| **PLAN §3.2 curated tasks** | User decision | User picks scope |
| **PLAN §3.4 retrospective decisions** | User decision | User picks which skill specs / AGENTS items / ADRs to author |

After items 1, 2, 3 land, the corpus should be at "research phase complete" by every meaningful measure.
