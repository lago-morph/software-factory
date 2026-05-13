# Research Index

**Last updated:** 2026-05-13 (after issue #29/#30/#31 drain).

Single-glance index of every numbered report and followup in `research/`. For per-source provenance see each report's "Sources reviewed" table; for round-level reachability status see `research/blocked-urls.md` (canonical, v5) and `research/blocked-urls-round-6.md` (most recent batch). The resumable plan is `research/PLAN.md`.

**Status legend:** ✅ complete · 🟡 partial · 📝 draft · ⏳ blocked-on-fetch · 🗑️ deprecated.

---

## Numbered reports (rounds 1–5)

| # | Slug | Status | Primary subject |
|---|---|---|---|
| 00 | synthesis | ✅ | Round-1 synthesis across all 7 Round-1 reports; canonical entry for failure-mode framework F1–F20. |
| 01 | strongdm-factory | ✅ | StrongDM's `factory.strongdm.ai` site, principles, techniques (DTU, gene-transfusion, pyramid-summaries, semport). |
| 02 | strongdm-attractor | ✅ | StrongDM's Attractor product page + 17+ community ports (Kilroy, Forge, etc.). |
| 03 | every-compound-engineering | ✅ | Every's compound-engineering guide + Klaassen "My AI had already fixed" (Cora playbook drained from primary). |
| 04 | every-skill-libraries | ✅ | Every's SKILL.md convention; Compound Knowledge plugin. |
| 05 | simon-willison | ✅ | Simon Willison's `agentic-engineering-patterns` 12-chapter guide + software-factory post. **Extended 2026-05-13** with partial Lenny × Willison podcast transcript (first 30 of 90 min): new H2 with "Challenger disaster of AI" prediction; **reversal-of-reversal on the "4 agents → 11 AM" claim** (the v3 "fabrication" correction was itself wrong — the count is real and verbatim). |
| 06 | hn-and-lenny | ✅ | HN thread on dark factories + Lenny Cherny/Willison interview references. **Updated 2026-05-13:** both Lenny podcasts now primary-anchored via partial transcripts (30 of 90 min each); Cherny "10–30 PRs/day, 100% Claude-written" verbatim; reversal-of-reversal on Willison's "4 agents → 11 AM" applied. Full transcripts pending (user offered overnight run). |
| 07 | dark-factory | ✅ | El Kaim's "The Dark Factory" Medium article (anchored on `reference-only/dark-factory-article.txt`). |
| 08 | jaymin-book-foundations-patterns | ✅ | Jaymin West's book: Chapters 1–5 (foundations + patterns). |
| 09 | jaymin-book-harnesses-practices-mental-models | ✅ | Jaymin West's book: Chapter 6 (harnesses) + practices + mental models. Replaces the deleted partial. |
| 10 | overstory-substrate-audit | ✅ | Overstory substrate audit (governance F-modes G12/G13/G14). |
| 11 | openhands-substrate-audit | ✅ | OpenHands substrate audit (arXiv paper + docs.all-hands.dev). |
| 12 | adjacent-ecosystem | ✅ | Adjacent ecosystem (Cisco/LangChain, IBM, Cloud, AddyOsmani, Kiro, others). |
| 13 | round-2-synthesis | ✅ | Round-2 synthesis; introduces substrate-stack recommendation; catalogs F21–F33. |
| 14 | el-kaim-book-intent-and-spec-authorship | ✅ | El Kaim EA book — intent + spec authorship (Chapters 1, 3, 6, 7, 8; 9-field spec discipline; ArchitectureSpecification typed object with derivedFrom rules; EvaluationSuite with `protects: RULE-ID` linkage). **Extended 2026-05-13** with Chapter 8 manual drain. |
| 15 | el-kaim-book-bmad-attractor-dark-factory | ✅ | El Kaim EA book — BMAD + Attractor + Dark Factory linkage. |
| 16 | el-kaim-book-council-and-delegation | ✅ | El Kaim EA book — Council pattern + delegation. |
| 17 | el-kaim-book-codex-and-skill-substrate | ✅ | El Kaim EA book — Codex + skill substrate. |
| 18 | openai-codex-substrate | 🟡 | OpenAI Codex substrate audit. Several `openai.com/index/*` and `developers.openai.com/codex/*` URLs still blocked-on-fetch (Path B only). |
| 19 | github-copilot-cloud-agent | 🟡 | GitHub Copilot cloud-agent substrate. **Updated 2026-05-13** with issue-#30 primary-source upgrades on umbrella how-to + CodeQL/Autofix; 5 claims still flagged `[2026-05-13 404; pending re-anchor]` because 6 of 9 docs.github.com URLs returned 404 (reorg). |
| 20 | replit-agent | 🟡 | Replit Agent substrate audit. `docs.replit.com/*` Cloudflare-gated; not yet attempted via action. |
| 21 | tabnine-enterprise | ✅ | Tabnine enterprise substrate. |
| 22 | academic-foundations | ✅ | Academic foundations across software-engineering research. |
| 23 | anthropic-engineering-trilogy | ✅ | Anthropic engineering posts S12–S15 + Claude Code sandboxing post + Agent Skills primary docs + 3 cookbook notebooks. **Updated 2026-05-13** with issue-#29 drain (full primary anchoring, 6 refutations, new §8 sandboxing) + issue-#36-extras drain (round-6 attribution-gap closed, 5 cookbook findings change methodology recommendation, concrete schema constraints: name max 64 chars, Level-1 budget ~100 tokens not 30–50, API-surface Skills have ZERO network access by runtime fiat). |
| 24 | el-kaim-book-product-line-variability | ✅ | El Kaim EA book — Chapter 9: software product lines, variability, family-based architecture. **New 2026-05-13** from manual fetch. Introduces ProductLineDefinition / ProductLineSpec Codex object; anchors on Linux Kconfig + Azure Landing Zones + AUTOSAR; proposes candidate failure mode **F35 — Federation-as-Family Drift**. |

## Follow-up reports (round 3 threads + post-round-3 additions)

| # | Slug | Status | Primary subject |
|---|---|---|---|
| 01 | shapiro-five-levels | ✅ | Shapiro's 0–5 maturity model. **Canonical post fully drained 2026-05-13 via issue #36** (correct slug `the-five-levels-from-spicy-autocomplete-to-the-software-factory`). All 3 prior gaps closed; Shapiro positions himself at L4 ("I'm here"); 8 El Kaim-vs-Shapiro discrepancies documented (cross-corpus propagation flags in PLAN.md §6.1). |
| 02 | attractor-implementations | ✅ | Community Attractor ports (~17 named, Go/Rust/Python/...). |
| 03 | cherny-interview | 🟡 | Boris Cherny Lenny interview. **Updated 2026-05-13** to partial primary-source-anchored: first 30 of 90 min transcript drained; 8 corpus claims verbatim-anchored + 8 new primary findings (notably $100K+/month per-engineer token spend at Anthropic). Full 60-min remainder outstanding — user offered overnight run. |
| 04 | gastown-beads | ✅ | Gas Town's DOT-graph orchestration. |
| 05 | klaassen-siblings | ✅ | Klaassen's three every.to "Stop Coding..." sibling articles (drained pt-2 / issue-23). |
| 06 | competitor-landscape | ✅ | Five named competitors (Devin / Factory / 8090 / Superconductor / Superpowers). **Updated 2026-05-13** with issue-#31 + issue-#36 drains; Devin pricing refuted, Factory adds Droid Computers primitive, Superconductor §4 fully re-anchored to .com (multiplayer "take the wheel" shared-agent-session is its unique differentiator). |
| 07 | evals-deepdive | ✅ | Anthropic multi-agent + Husain/Shankar FAQ + Hamel tetralogy + Simon FAQ. **Updated 2026-05-13** with issue-#29 drain: 4 Hamel posts now primary-anchored; new sections on Critique Shadowing, Capability Funnel, fifteen-five, synthetic data. |
| 08 | security-primitives | ✅ | Lethal trifecta + Dual LLM + CaMeL + Claude Code sandboxing. **Updated 2026-05-13** with issue-#29 drain: 5 refutations of prior reconstruction; CaMeL section now seven subsections with verbatim primary quotes. |
| 09 | methodology-ancestors | ✅ | Methodology ancestors (lean, agile, V&V, etc.). |
| 10 | governance | ✅ | Governance/oversight literature; complements report 10 substrate audit. |
| 11 | compound-knowledge | ✅ | Every's Compound Knowledge plugin (companion to report 04). |
| 12 | brier-pace-layers | ✅ | Brier's pace-layers pushback against the software-factory metaphor (anchored on `reference-only/brier-culture-of-ai-engineering.txt`); proposes failure mode F34 (cross-layer drift). |

---

## How to use this index

- **Looking for a specific source?** Grep the URL across `research/*.md research/followup/*.md`; the citation will be at the point of claim, not just in the sources table.
- **Looking for a failure mode (F1–F34)?** See `research/00-synthesis.md` §4 for F1–F20, `research/13-round-2-synthesis.md` §3 for F21–F33, `research/followup/12-brier-pace-layers.md` for the F34 proposal.
- **Looking for what's blocked / pending?** `research/blocked-urls.md` (canonical v5), `research/blocked-urls-round-6.md` (most recent), `research/unfetched-sources.md` (manual fetch routes).
- **Looking for the next action?** `research/PLAN.md` §1 (TL;DR) → §3 (Bottlenecks) → §5 (Work remaining).
