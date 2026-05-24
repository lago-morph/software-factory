# Software Factory Research — PLAN.md

## ⚠ Picking up work? Start at the v3 synthesis plan, not here.

The active work right now is the v3 architecture synthesis. The entry point is [`ARCHITECTURE-V3-SYNTHESIS-PLAN.md`](../ARCHITECTURE-V3-SYNTHESIS-PLAN.md) at the repo root — it carries a current-state pointer that names whichever phase is active. This file is the research-drain pipeline state and is not the entry point for current work.

---

## 1. Current state (TL;DR)

Rounds 1–12 complete (see §10 for the round-by-round lookup). What's left is the §3 and §5 items plus the `research-plan.md` direction decision.

### Sessions / drain rounds

- **2026-05-10 — Round 1** — initial 7-source subagent dispatch.
- **2026-05-11 — Round 2** — Jaymin / Overstory / OpenHands substrate audits (`423940f`).
- **2026-05-11 — Round 3** — 12 follow-up threads.
- **2026-05-11 — Round 4** — El Kaim enterprise-architecture book (4 clusters).
- **2026-05-11 — Round 5** — counterfactual harvest against ChatGPT deep-research artifact (6 clusters).
- **2026-05-11 — Round 6** — 26-subtask parallel-fanout night run + pt-2 wave (`harness/runs/20260511-054258/`).
- **2026-05-13 — Round 7** — Shapiro canonical + El Kaim post-index + El Kaim Chapter 9 + platform.claude.com Path B.
- **2026-05-13 20:30 PR #48 — research-structure clarification** [#48](https://github.com/lago-morph/software-factory/pull/48)
- **2026-05-14 — Round 8** — issues #41/#42 drained + Lenny × Willison full transcript ([#43](https://github.com/lago-morph/software-factory/pull/43), [#44](https://github.com/lago-morph/software-factory/pull/44), [#46](https://github.com/lago-morph/software-factory/pull/46)).
- **2026-05-14 09:33 Lenny × Cherny full transcript drain** [#56](https://github.com/lago-morph/software-factory/pull/56)
- **2026-05-15 23:27 fetch-loop tooling consolidation** [#58](https://github.com/lago-morph/software-factory/pull/58)
- **2026-05-15 22:35 Round-9 manual drain** [#57](https://github.com/lago-morph/software-factory/pull/57)
- **2026-05-16 10:45 Round-10 manual drain** [#67](https://github.com/lago-morph/software-factory/pull/67)
- **2026-05-16 19:41 `/reference-only/` step-1 categorization** [#71](https://github.com/lago-morph/software-factory/pull/71)
- **2026-05-17 03:32 research-pipeline schema + SKILL.md + config loader** [#79](https://github.com/lago-morph/software-factory/pull/79)
- **2026-05-17 12:20 `source-dedup.md` → `sources.json` migration** [#80](https://github.com/lago-morph/software-factory/pull/80)
- **2026-05-17 12:48 issue-82 fetch drain** [#83](https://github.com/lago-morph/software-factory/pull/83)
- **2026-05-17 13:00 15-category taxonomy + CLAUDE.md → AGENTS.md hop** [#84](https://github.com/lago-morph/software-factory/pull/84)
- **2026-05-17 15:49 22-source 8090.ai docs + Copilot drain** [#90](https://github.com/lago-morph/software-factory/pull/90)
- **2026-05-17 15:56 `youtube-transcript` schema support** [#91](https://github.com/lago-morph/software-factory/pull/91)
- **2026-05-17 17:02 Round-11 manual drain** [#93](https://github.com/lago-morph/software-factory/pull/93)
- **2026-05-17 20:39 plan-update discipline + drain mechanics fixes** [#94](https://github.com/lago-morph/software-factory/pull/94)
- **2026-05-17 20:54 single-source normalize for `sources.json`** [#97](https://github.com/lago-morph/software-factory/pull/97)
- **2026-05-17 21:47 PLAN.md audit + back-fill pass** [#98](https://github.com/lago-morph/software-factory/pull/98)
- **2026-05-20 18:01 Round-12 gas-systems substrate analysis** [#101](https://github.com/lago-morph/software-factory/pull/101)
- **2026-05-21 spec-driven-ai-dev.md → source catalog (record `3592091691`)** — issue [#105](https://github.com/lago-morph/software-factory/issues/105)

### Open items live in

- §3 Bottlenecks (§3.2 ~~curated human-review backlog~~ **superseded by v3 synthesis path 2026-05-23**; §3.6 ~~F36/F37 numbering collision~~ **resolved 2026-05-23 in v3 Phase 1B**).
- §5 Work remaining.
- §6.1 Cross-corpus propagation flags.
- ~~`research-plan.md` (root) — the structural pivot proposal. Decision pending.~~ **2026-05-23: Resolved.** User decided in favor of v3 synthesis path; [`research-plan.md`](../archive/research-plan.md) archived, constraints extracted to [`constraints-extracted`](../architectures/v3/constraints-extracted.md), execution plan in [`ARCHITECTURE-V3-SYNTHESIS-PLAN`](../ARCHITECTURE-V3-SYNTHESIS-PLAN.md).

---

## 2. Repository layout (what lives where)

```
/architectures/         → candidate methodologies + comparison; each file carries a based-on-commit YAML header
/docs/adr/              → ADR system
/harness/runs/          → historical fanout-run records
/reference-only/        → canonical source catalog
    sources.json        → canonical metadata (id, title, url, files[], tags, …). id = sha256(canonical_url)[:10]
    sources.md          → auto-regenerated browse view (managed by the regen-sources-md workflow; do not hand-edit)
    sources.schema.json → JSON Schema for sources.json (validation in CI)
    MIGRATION-EXCEPTIONS.md → URLs deliberately excluded from the catalog (casual mentions, homepages)
    <id>/               → one directory per source, containing the on-disk files
/research/              → numbered reports + followup reports + workflow tooling
    PLAN.md             → this file
    synthesis/          → cross-report synthesis docs (carry a based-on-commit YAML header)
    figures/            → per-report figure directories
    followup/           → followup reports
    manual/             → transient drop zone for new manual fetches
/retrospective/         → retrospectives + sibling skill specs / AGENTS-MD rule files / ADR draft files
/.claude/skills/        → installed skills
/.github/               → fetch-blocked-urls action + research-pipeline auto-regen workflows
initial-sources.md      → original Round-1 seed list (frozen)
```

---

## 3. Bottlenecks

### 3.2 Curated human-review backlog — **SUPERSEDED 2026-05-23 by v3 synthesis path**

**Status update.** The tasks in this section were defined against the four-architecture v2 set. Per [`ARCHITECTURE-V3-SYNTHESIS-PLAN`](../ARCHITECTURE-V3-SYNTHESIS-PLAN.md) Phase 0.4, the v2 architectures (including `00-comparison.md`) and v1/v2 syntheses have been archived to [`archive/architectures-v2/`](../archive/architectures-v2/) and [`archive/synthesis-v1-v2/`](../archive/synthesis-v1-v2/). The tasks below are preserved for historical context but are **not** the path forward — v3's Phase 1-7 work delivers the equivalent (and more, against the full post-Round-12 corpus) via a different mechanism.

**Original section (preserved verbatim for archaeology, no longer actionable):**


These three tasks were explicitly excluded from subagent dispatch in the original brief and are still outstanding:

| Task | What | Source of the proposed change | Risk if skipped |
|---|---|---|---|
| **Update [`00-comparison`](../architectures/00-comparison.md)** | (a) Replace §7 with the substrate-stack recommendation from [`13-round-2-synthesis`](synthesis/13-round-2-synthesis.md) §6 (preserve original §7 as "§7 (Round 1)"). (b) Extend §2.4 with F21–F33 from report 09 + report 13 + G12/G13/G14 from drained report 10. | Round-2 synthesis report 13 §6; Round-2 failure-mode extension in report 09 §6 + report 13 §3 + governance drain in report 10 | The canonical comparison doc lags 4 rounds of synthesis. New readers see a 2025-era comparison; they don't see "harness" vocabulary, substrate-stack recommendation, or failure modes F21–F33. |
| **Round 2 complete stanza** | Append a "Round 2 complete" stanza to the §10 lookup row with the drain merge commit hash `423940f`. | Bookkeeping. | Audit trail is incomplete. |

The original §3.2 carried a third task — "Update `spec-driven-ai-dev.md`" with the 4-field El Kaim extension from [`14-el-kaim-book-intent-and-spec-authorship`](14-el-kaim-book-intent-and-spec-authorship.md). **Retired 2026-05-21** (issue [#105](https://github.com/lago-morph/software-factory/issues/105)): `spec-driven-ai-dev.md` was reframed as a cataloged source (record [`3592091691`](../reference-only/3592091691/spec-driven-ai-dev.md)) and is no longer treated as a mutable internal artifact. The 4-field discipline from Report 14 lives on as a research finding that informs the v3 architecture choice (see `research-plan.md`); it does not amend the source document.

### 3.6 Failure-mode numbering collision — **RESOLVED 2026-05-23 in v3 Phase 1B**

**Resolution.** Lead agent accepted the suggested triage verbatim during v3 Phase-1B failure-mode consolidation. Canonical entries are in [`failure-modes-v3` §4](../architectures/v3/failure-modes-v3.md) (F36-F39) and §4a (F50-F51 for the report-25 secondary proposals). Resolution audit trail preserved in §6 of that file.

**Original section** (preserved for historical context):


Reports 25 and 26, dispatched in parallel as part of the Round-9 manual drain, each independently proposed candidate failure modes F36 and F37. The two pairs name **different phenomena**:

| Number | Report 25 proposal (RE/SE) | Report 26 proposal (academic) |
|---|---|---|
| **F36** | **Vocabulary lint debt** — LLM-authored specs systematically violate INCOSE GtWR R7/R8/R9 (vague modifiers; ambiguous pronouns; superlatives). | **Instruction-following ceiling** — gpt-4o Pass@1 drops 98.7% → 85.0% as requirements specified grow 1 → 19 (Yang et al. arXiv:2505.13360v3 §3.4). Failure is *budget exhaustion* under a *complete* spec. |
| **F37** | **Point-spec / region-mismatch** — INCOSE Complexity Primer principle 12: when the *intended* outcome is a region in solution-space, expressing it as a point spec guarantees off-target instances. | **Silent contradictory-prompt collapse** — GPT-4 Pass@1 73.8% → 6.7% on contradictory HumanEval, RIR climbs to 89%; LLM-as-judge MCC ≤ 0.55 (Larbi et al. arXiv:2507.20439v1 §6.1–6.2). Broken code *runs*. |

All four are genuinely distinct phenomena and worth catalog inclusion. Round-10 (PR #67) deliberately took F40–F49 to dodge this collision, so the remaining slots available are F36–F39 themselves. Suggested triage: F36 → Yang-et-al. instruction-following ceiling; F37 → Larbi-et-al. silent contradictory-prompt collapse; F38 → report-25 vocabulary lint debt; F39 → report-25 point-spec/region-mismatch. Report-25's "architecture/specification confusion in typed objects" and "Ashby-deficient probabilistic guard" need new numbers above F49 (F50/F51) when promoted.

**Required triage:** lead agent decides numbering. Until triage, both reports' §"Implications" sections cite their own internal F36–F39 numbering. Neither has been propagated into the existing syntheses. No code paths or specs depend on the numbers; this is documentation-only cleanup.

---

## 5. Work remaining

### 5.0 Definition of "research phase complete"

The research phase is complete when **all** of the following hold:

- Cross-corpus propagation sweep complete (§6.1).
- §3.2 curated-human-review backlog resolved one way or the other (update or won't-fix).
- Either a unified synthesis exists at `research/synthesis/final.md` (or equivalent) or the user has explicitly decided not to write one (per `research-plan.md`).
- ~~F36/F37 numbering collision triaged (§3.6)~~ **resolved 2026-05-23 in v3 Phase 1B; canonical entries in [`failure-modes-v3` §4](../architectures/v3/failure-modes-v3.md) + §4a**.

### 5.1 Concrete tasks

- **Decide on `research-plan.md` direction.** Two coupled questions: (a) cut a single unified Round-1–N synthesis, or keep the current two-synthesis-plus-followups state; (b) collapse the four architectures to one chosen path (likely Atelier + Refinery layered-spec discipline) + "rejected alternatives" appendix, or keep all four.
- **§3.2 curated human-review tasks.** Update [`00-comparison`](../architectures/00-comparison.md) §7 + §2.4; add the Round-2-complete stanza. (The §3.2 task to amend `spec-driven-ai-dev.md` with the 4-field El Kaim extension was retired 2026-05-21 when the file was reframed as a cataloged source — issue [#105](https://github.com/lago-morph/software-factory/issues/105).)
- **Cross-corpus propagation sweep (§6.1).** Mechanical grep + small subagent dispatch.
- **F36/F37 triage decision (§3.6).** Lead-agent call on numbering.
- **Locate the three jaymin YouTube transcripts.** User believes the three jaymin YouTube transcripts are on their laptop — find and drop into `research/manual/`, or confirm not-present and mark `skip-not-necessary`. (The three wanted-transcript records are already in `sources.json` on the Jaymin West Agentic Engineering Book record `992e4f88b6`.)

### Linter sanity-warning sweep (~1 hour subagent)

`bash scripts/lint-sources.sh` produces 65 advisory `sanity` warnings on
`audit-records.py`. Three buckets, processed in order:

1. **Broken-content captures (~15 records).** Files whose captured page
   is a Cloudflare interstitial, a 404 page, or a search-results page.
   For each: either re-fetch via the `fetch-blocked-urls` action (often
   succeeds from the GitHub Actions IP when sandbox is blocked), or set
   `completeness: error` + `ingestion_status: skip-not-necessary` if a
   sibling file on the same record already carries the canonical content.
   Affected records (representative): `60fbea1689`, `7dbf96d872`,
   `e6f77b9e81`, `5a9f63821f`, `3274cc670c`, `85cdf07ac2`, `2e49bcd671`,
   `a5209cf735`. See L.4 of `cleanup-plan-revised.md` (git history) for
   the full list captured at PR #106 time.
2. **Host normalization (~5 records).** File's URL host is `cognition.ai`
   but record's canonical URL host is `www.cognition.ai` (and similar).
   Fix: teach `audit-records.py` to call `url_canonicalize.py`'s
   host-normalization helper before comparing.
3. **Format-variant low-overlap (~45 records).** HTML + MD + MHTML files
   for the same source naturally have <30% token overlap because HTML
   carries nav chrome. Fix: loosen the audit threshold from "warn at
   <30%" to "warn at <10%" — a constant in `audit-records.py`.

Trigger: lint output is dominated by these. Worth doing when the sweep
cost (~1 hour) is below the irritation cost.

### PLAN.md consistency-check tightening (5 min)

`check-plan-consistency.py` warns when a catalog-touching commit didn't
also touch PLAN.md. False-positive rate is high because auto-regen
commits (`auto: regenerate sources.md from sources.json`) and merge
commits are mechanical and shouldn't trigger the warning. Fix: in
[`check-plan-consistency`](../.claude/skills/research-pipeline/scripts/check-plan-consistency.py),
skip commits whose subject starts with `auto:` or `Merge ` from the
catalog-commit window. Single-function edit.

---

## 6. Resumption checklist for the next session

When picking this up cold:

1. `git status` — confirm clean working tree.
2. `git log origin/main..HEAD --oneline` — see what's ahead of main.
3. Check open issues: `mcp__github__list_issues` for `lago-morph/software-factory` state=OPEN. Drain any `fetched/issue-N` branches that have landed.
4. Read this PLAN.md §1, §3, and §5 first.
5. If new manual content is in `research/manual/` (anything other than `README.md`), activate the `research-pipeline` skill — Phase 0 will drain it.
6. The `parallel-subagent-fanout` skill is the right tool when 4+ independent subtasks accumulate.

### 6.1 Cross-corpus propagation flags

Round 7's Shapiro canonical-post drain refuted prior corpus framings of Shapiro as a Level-5 practitioner (he positions himself at L4 with the verbatim "I'm here.") and surfaced 8 El Kaim-vs-Shapiro discrepancies. The following propagation edits are pending:

- **[`07-dark-factory`](07-dark-factory.md)** — should note that El Kaim *paraphrases* and conflates Shapiro's canonical Five Levels post with the companion "You don't write the code" post; flag the L4 and L5 divergences. The "Nobody writes / Nobody reads" L5 framing currently in the report is El Kaim's, not Shapiro's.
- **[`01-strongdm-factory`](01-strongdm-factory.md)** and **[`02-strongdm-attractor`](02-strongdm-attractor.md)** — anywhere the named StrongDM team-size datum ("less than five people" / "Justin McCarthy three-person team") is attributed to Shapiro's Five Levels post: the Five Levels post says only "less than five people"; the named StrongDM/Justin/three-person datum traces to the companion post only.
- **Anywhere in the corpus** Kilroy is called "Shapiro's Level-5 reference implementation": Kilroy is *not mentioned* in the canonical Five Levels post; that positioning exists only in the companion post.
- **Anywhere in the corpus** Shapiro is described as "a Level 5 practitioner" or "Level 4–5 practitioner-tooler": refute with Shapiro's verbatim L4 self-position ("I'm here.").

Suggested approach: a single `Grep` pass for the strings above, then a small subagent dispatch to apply the corrections.

### 6.2 In-flight tracking — what triggers the next action

Each row is an open thread; the third column states the explicit trigger that moves it forward.

| Item | State | What triggers next action |
|---|---|---|
| **`research-plan.md` direction** | User decision pending | User picks: unified synthesis (yes / no); v3 single architecture (yes / no) — see §5 |
| **§3.2 curated tasks** | User decision; likely folded into the v3 architecture step | Decision on `research-plan.md` direction (above) |
| **§6.1 cross-corpus sweep** | Mechanical, ~30 min via single `Grep` pass + small subagent dispatch | User says "do the sweep" |
| **F36/F37 numbering collision (§3.6)** | ✅ Resolved 2026-05-23 in v3 Phase 1B | n/a |

---

## 8. GitHub Action — security stance (frozen)

The `fetch-blocked-urls` workflow uses **label-only authorization** (`fetch-urls` label, applied by a Triage-role human). This avoids the `author_association` footgun where webhook payload and REST API disagree. Documented in ADR-0001 ([`0001-fetch-blocked-urls-mechanism`](../docs/adr/0001-fetch-blocked-urls-mechanism.md)).

The runner has full network egress and writes to a fresh `fetched/issue-N` branch (never to `main`). All merges into `main` are human-driven.

---

## 9. Costs, scope, and what this plan does not do

**Out of scope (deliberately):**
- ~~Replacing the four architectures with a single "winner". The comparison stays a comparison.~~ **Reversed by `research-plan.md` (PR #46, 2026-05-14).** That doc proposes the opposite — for the lights-out-greenfield mandate specifically, v3 should likely collapse to one chosen architecture (Atelier + Refinery layered-spec discipline) with the other three demoted to "rejected alternatives" in an ADR. Decision pending; see §5.
- Building harness code beyond the `fetch-blocked-urls` workflow primitive.
- Adopting `harness` vocabulary across the architecture documents wholesale before the user has reviewed Round 2 synthesis report 13.

---

## 10. Round-by-round canonical reports (lookup table)

| Round | Reports | Status | Summary |
|---|---|---|---|
| 1 | `research/01-07-*`, [`00-synthesis`](synthesis/00-synthesis.md) | ✅ Complete | 7-source initial reconstruction; F1–F20 promoted. |
| 2 | `research/08-12-*`, [`13-round-2-synthesis`](synthesis/13-round-2-synthesis.md) | ✅ Complete | Jaymin / Overstory / OpenHands substrate audits; F21–F33 promoted. Drain merge `423940f`. |
| 3 | `research/followup/01-12-*` | ✅ Complete | 12 follow-up threads; Thread 12 resolved into report 07; post-Round-3 Brier drain recovered onto main via cherry-pick (F34 promoted). |
| 4 | `research/14-17-*` + [`24-el-kaim-book-product-line-variability`](24-el-kaim-book-product-line-variability.md) | ✅ Complete | El Kaim book: spec authorship, BMAD, council, codex+skills, plus Chapter 9 (F35 promoted). |
| 5 | `research/18-23-*` | ✅ Complete | Counterfactual harvest: OpenAI Codex, GitHub Copilot, Replit, Tabnine, academic foundations, Anthropic engineering. |
| 6 | [`report`](../harness/runs/20260511-054258/report.md) + `report-pt2.md` | ✅ Complete | 26-subtask parallel-fanout night run + pt-2 wave recovered via cherry-pick. Drain merge `423940f`. |
| 7 | drain of issue #36 + 3 manual drops | ✅ Complete | Shapiro canonical Five Levels (L4 self-position; 8 El Kaim discrepancies → §6.1); El Kaim post-index Path B; El Kaim Chapter 9 → report 24; `platform.claude.com/.../agent-skills/overview` Path B → report 23 §3. |
| 8 | drain of issues #41 + #42 + Lenny full transcripts | ✅ Complete | Reports 19, 20 ✅; followup/08 §3 paper-body-anchored via CaMeL arXiv `/e-print/` recovery; reports 05, 06 ✅ FULL via Willison + Cherny transcripts. [#43](https://github.com/lago-morph/software-factory/pull/43), [#44](https://github.com/lago-morph/software-factory/pull/44), [#46](https://github.com/lago-morph/software-factory/pull/46), [#56](https://github.com/lago-morph/software-factory/pull/56). |
| 9 | Round-9 manual drain | ✅ Complete | RE/SE foundations + LLM+RE academic + Kiro: new reports 25 + 26, report 12 §2.5 extension; F36–F39 candidate proposals with numbering collision (see §3.6). [#57](https://github.com/lago-morph/software-factory/pull/57). |
| 10 | Round-10 manual drain (71 sources / 15 clusters) | ✅ Complete | 11 new reports (27–37), 8 existing-report upgrades, 5 followup updates, F40–F49 promoted, `openai.com/index/*` host class fully primary-anchored. [#67](https://github.com/lago-morph/software-factory/pull/67). |
| 11 | Round-11 manual drain (16 files; ingestion only, stage 5 deferred) | 🟡 Stage 5 deferred | 15 MHTML + 1 PDF; 5 new catalog records + 11 attachments. First drain to exercise PDF companion-URL plumbing. [#93](https://github.com/lago-morph/software-factory/pull/93). |
| 12 | Round-12 gas-systems substrate analysis | ✅ Complete | Reports 38 + followups 13 + 14. [#101](https://github.com/lago-morph/software-factory/pull/101). |

For each report, the source citations live in the report's §"Sources reviewed" or first-page status table.

---

*End of PLAN.md.*
