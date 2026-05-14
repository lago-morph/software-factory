# User Next Steps — End-of-Research-Phase Audit

**Date:** 2026-05-14 (supersedes 2026-05-13 version)
**Author:** Lead agent
**Status snapshot:** Research phase is now ~closed by every primary-source measure. Issues #41 / #42 fully drained (PR #44); Lenny × Willison full transcript drained (PR #43); three new retrospectives (PR #45 / #47 / #48) and a research → action plan (`research-plan.md`, PR #46) landed. Only Cherny-Lenny remainder, 5 Path-B-only URLs, and the curated synthesis decisions are still outstanding.

---

## What changed since the 2026-05-13 audit

All five of the recommended-order items from the previous version are now resolved or partially resolved:

1. ✅ **PR #40 merged** (`9208cfb`) — audit cleanup landed.
2. ✅ **Issue #41 drained** via PR #44 (`a082310`): Replit 13/13 primary-anchored (🟡 → ✅); OpenAI Codex 5/7 primary-anchored (3 Cloudflare-blocked); SWE-bench 0/2 (Cloudflare-blocked). Reports 18, 20, 22 updated.
3. ✅ **Lenny × Willison full transcript drained** via PR #43 (`9d8e55a`): reports 05 and 06 flipped to ✅ FULL; +293 lines incorporating the Challenger-disaster prediction, the lethal-trifecta walkthrough with the 97%-failing-grade doctrine, OpenClaw, and the end-of-2026 prediction.
4. ✅ **Issue #42 drained** via PR #44: 6 GH Copilot canonical re-finds primary-anchored (report 19 🟡 → ✅, new §3.1 on Copilot Spaces); CaMeL paper body **recovered via the arXiv `/e-print/` LaTeX-tarball route** (followup/08 §3 now paper-body-anchored, expanded from 7 to ~15 subsections).
5. ⏳ **Path-B `platform.claude.com` SPA pages** — still outstanding (low priority).
6. ⏳ **PLAN §3.2 / §3.4 curated decisions** — still pending; the surface has grown (see below).

Additional commits in this window:
- `bc61f55` (PR #46): added `research-plan.md` — proposes the three-layer condensation (reports → unified synthesis → single chosen architecture + ADRs).
- `70e3128` (PR #45): retrospective `2026-05-13-02` — 3 proposed skills, 10 AGENTS suggestions.
- `ff0426e` (PR #47): retrospective `2026-05-14-01` — 3 proposed skills, 7 AGENTS suggestions, 4 proposed ADRs.
- `42ed807` (PR #48): retrospective `2026-05-14-02` (renumbered from -01 due to concurrent session collision) — 0 skills, 4 AGENTS suggestions, 5 proposed ADRs.

---

## Current state of pending drains

- **Phase 0 inventory empty.** `research/manual/` clean (only README); `research/fetched/` retains only the round-7 retained-404-evidence file.
- **No in-flight fetch issues.** Issues #41 and #42 are technically still in the `OPEN` state on GitHub, but their drains are complete and merged on main. **Housekeeping: close issues #41 and #42** with a one-line comment pointing to PR #44.
- **Cherny-Lenny transcript remainder** — still the only Phase-0-pending item the user can produce locally. Drain will trigger automatically when it lands in `research/manual/`.

---

## Audit: what valuable sources remain partial / blocked

### Priority 1 — Path-B only (action route exhausted)

| Cluster | Affected report | URLs | Why valuable |
|---|---|---|---|
| **3 × `openai.com/index/*`** | `research/18-openai-codex-substrate.md` | `harness-engineering`, `unlocking-the-codex-harness`, `introducing-swe-bench-verified` | Productivity-numbers and harness-design framing remain WebSearch-reconstructed. Cloudflare JS challenge confirmed for all three in round-8. Report 18 remains 🟡 *solely* because of these. |
| **1 × `pli.princeton.edu/.../swe-bench`** | `research/22-academic-foundations.md` | The original SWE-bench announcement | Cloudflare-blocked round-8. Wayback fallback may work. |
| **2 × `platform.claude.com/docs/en/agent-skills/{best-practices,security}`** | `research/23-anthropic-engineering-trilogy.md` | The remaining two Agent Skills SPA pages | JS-rendered SPA shell from action. User has already Path B'd the overview page; these two would close the Skills security-attribution audit trail. Overview is the high-value one and it's done — these are nice-to-have. |
| **1 × `docs.github.com/.../cloud-agent/risks-and-mitigations`** | `research/19-github-copilot-cloud-agent.md` | Would directly re-anchor a REFUTES in report 19 | Surfaced in round-8 follow-ups. Low priority — report 19 already flipped to ✅. |

### Priority 2 — User-only deliverable

- **Lenny Cherny full transcript** (~60 min remainder) → `research/06`, `research/followup/03`. **Highest-leverage remaining single source.** First 30 min was manually transcribed; the rest still un-primary-sourced ("10–30 PRs/day", "10–15 parallel sessions" claims are partially anchored).

### Priority 3 — Accept the gap

Same list as the prior version, all unchanged:
- 2389.ai DOT-file essay + gastownhall.ai 403s (followup/04)
- 4 jaymin-book example dirs (report 12)
- 5 OpenHands repo source-code reads (report 11)
- IBM "agentic engineering" extraction nav-chrome (report 12 §2.4)
- Anthropic *Demystifying evals* (followup/07 — explicitly deprioritized)

---

## The synthesis-collapse decisions (now the highest-leverage open work)

`research-plan.md` (PR #46) names the structural problem: the corpus has **two synthesis docs** (`00-synthesis.md` for Round 1, `13-round-2-synthesis.md` for Round 2) and **zero synthesis** for Rounds 3 / 4 / 5 + the 12 followups. F1–F33 live in those two; F34 lives in `followup/12`; F35 was just promoted in report 24. The failure-mode catalog is fragmented and getting worse.

The proposed shape from `research-plan.md`:

1. **Cut a single unified synthesis** — either v3 of `00-synthesis.md` or a new `research/24-final-synthesis.md`. One canonical F1–F35+ list, one consensus list, one tensions list, one open-questions list.
2. **Revise architectures to v3** against that synthesis. For the *lights-out greenfield* mandate specifically, Tournament and Foundry are unlikely fits; v3 likely collapses to **one chosen architecture** (probably Atelier + Refinery's layered-spec discipline on top) with the other three demoted to "rejected alternatives" in an ADR.
3. **Promote the chosen path into ADRs and a build plan** for §7.4's shared infrastructure.
4. **Run the §6 lean evaluation first** — the 1-day manual run before any orchestration work.

The cold-start question for a greenfield factory (no issue queue, no codebase to learn from, no prior scenarios) is its own design question and isn't yet addressed in `architectures/00-comparison.md`.

This is the actual research-phase exit. None of the §3.2 curated tasks individually unblocks it.

---

## Retrospective backlog (now much larger)

Four retrospectives currently carry decisions that need the user to pick scope:

| Retrospective | Skill specs proposed | AGENTS.md suggestions | Proposed ADRs |
|---|---|---|---|
| `2026-05-11-01` | 3 (provenance-aware-reconstruction, sync-to-main-before-building, verbatim-fetch-via-curl) | 15 | 7 |
| `2026-05-13-02` | 3 (cross-corpus-propagation, drain-audit, subagent-cleanup-sweep) | 10 | (titles in body) |
| `2026-05-14-01` | 3 (fetch-action-quality-check, arxiv-e-print-recovery, stale-branch-audit) | 7 | 4 |
| `2026-05-14-02` | 0 | 4 | 5 |
| **Totals** | **9 skill specs** | **~36 suggestions** | **~16 ADR titles** |

These are *methodology synthesis*, not research. Picking through them is independent from the corpus condensation in §"synthesis-collapse decisions" above — but both pieces of work block "research phase unambiguously closed."

---

## Cross-corpus propagation flags (still open)

`research/PLAN.md` §6.1 still carries the unpushed cross-corpus correction sweep from round-7 Shapiro drain:

- `research/07-dark-factory.md` — note that El Kaim conflates Shapiro's canonical Five Levels post with the companion post.
- `research/01-strongdm-factory.md` / `02-strongdm-attractor.md` — the named StrongDM team-size datum traces to the companion post only.
- Anywhere in the corpus Kilroy is called "Shapiro's Level-5 reference implementation" (Kilroy is not mentioned in the canonical Five Levels post).
- Anywhere Shapiro is described as "Level 5 practitioner" — refute with his verbatim L4 self-position.

Estimated effort: ~30 min wall time via single `Grep` + small subagent. Captured here so a future session can pick it up; not picked up to date because no explicit ask.

---

## Definition of "research phase complete"

The research phase is complete when:

1. ✅ All 24 numbered reports + 13 followup reports exist with a "Sources reviewed" table at the bottom.
2. ✅ `research/INDEX.md` reflects current per-report status.
3. ✅ `research/PLAN.md` shows no in-flight fetch issues unaccounted for.
4. ✅ Every Priority-1 source is primary-anchored or has an "accepted gap" decision on record. **(Done as of round-8 drain.)** The 4 remaining Path-B-only URLs are documented gaps, not unknowns.
5. ⏳ Both Lenny transcripts fully drained. (Willison ✅; Cherny remainder is the only outstanding user-side fetch.)
6. ⏳ Cross-corpus propagation sweep complete (PLAN §6.1).
7. ⏳ The §3.2 curated-human-review backlog + the four-retrospective decision backlog resolved one way or the other (Update or "won't fix").
8. ⏳ Either a unified Round-1–5 synthesis exists, or the user has explicitly decided not to write one (per `research-plan.md`).

Items 1–4 are met now. 5 is close. 6–8 need user decisions.

---

## Recommended order of operations to close out the research phase

1. **Close GitHub issues #41 and #42** (housekeeping — both are drained but still show OPEN). One-line comment pointing to PR #44 (`a082310`).
2. **Drain Cherny Lenny remainder** whenever the user drops it in `research/manual/`. Trigger `drain`. Closes the last user-side primary-source gap.
3. **Decide on `research-plan.md` direction** — does the user want the unified synthesis + v3 single architecture? This is the structural pivot from "research" to "build." Until it's decided, every additional polish on individual reports has diminishing return.
4. **Pick scope on retrospective backlog** — 9 skill specs / ~36 AGENTS suggestions / ~16 proposed ADRs is too large to author all of; the user needs to pick.
5. **Resolve §3.2 curated tasks** (architectures/00-comparison §7+§2.4 update, spec-driven-ai-dev.md 4-field extension, Round 2 stanza) — these are pre-requisites for the v3 architecture decision in step 3, so likely fold into that.
6. **Cross-corpus propagation sweep** (PLAN §6.1) — small, mechanical, ~30 min.
7. **(Optional, Path B)** User Save-Page-As the 2 remaining `platform.claude.com` Skills pages and the 3 `openai.com/index/*` pages if the productivity-numbers gap in report 18 matters.

---

## In-flight tracking (for next session)

| Item | State | What triggers next action |
|---|---|---|
| **Issues #41 / #42** | OPEN on GitHub; drains complete | User says "close them" or agent closes with link to PR #44 |
| **Cherny Lenny full transcript** | User to produce | File lands in `research/manual/` → `drain` |
| **`research-plan.md` direction** | User decision pending | User picks: unified synthesis? v3 single architecture? |
| **Retrospective backlog** | 4 retrospectives, 9 skills / 36 AGENTS items / 16 ADRs | User picks scope |
| **PLAN §3.2 curated tasks** | User decision | Likely folded into the v3 architecture step |
| **PLAN §6.1 cross-corpus sweep** | Mechanical, ~30 min | User says "do the sweep" |
| **5 × Path-B URLs** | Path B only | User Save-Page-As → `research/manual/` → `drain` |

The corpus is at "research phase complete" by every primary-source measure. What remains is **decision work**, not fetch work.
