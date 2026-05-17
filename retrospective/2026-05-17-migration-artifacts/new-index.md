# `research/manual/` — new-source index

**Status:** preliminary indexing pass (drafted 2026-05-16). NOT a drain. PLAN.md is intentionally untouched. The next agent will use this index to plan how to chunk the incorporation into existing reports / new reports.

This document indexes ~71 sources newly dropped into `research/manual/`. Each source has been classified along the seven thematic axes below and (where relevant) checked against the existing 27 numbered reports + 12 followups for prior processing. Sources that were already drained have been deleted; sources without any informative images have been converted to `.txt` (the original `.mhtml` deleted); sources whose images carry real informational content (architecture diagrams, dot-graph renders, taxonomy figures, etc.) are kept as `.mhtml`.

---

## The seven themes (the next agent should use these to chunk ingestion)

The user articulated seven thematic motivations for this batch. Every per-source block below is tagged with the theme numbers it speaks to.

### 1. Human attention as a scarce resource

Human attention is the **binding constraint** of the software factory. Human interaction must be **infrequent and batched** — the factory cannot scale if every decision triggers a context-switch.

**Review-summary discipline (verbatim from the brief):**
- 8–10-word headline summary
- 2–3-sentence brief summary
- 1-page guide covering rationale, pros, cons, and follow-on effects

A number of articles in this batch address how humans interact with increasingly agentic systems — collaboration patterns, attention firewalls, cognitive escrow, the "choosing the work" bottleneck — and feed directly into this theme.

### 2. Agent self-improvement, drift, and collusion

Agents can and should self-improve, but the same mechanisms create new failure modes: **drift** (gradual divergence from intent) and **collusion** (independent agents converging on undesirable joint behavior). One or two papers in this batch directly model agent collusion in a market-like setting; others address the recursive-self-improvement → board-fiduciary-exposure pipeline.

### 3. Governance and guardrails

The factory could in principle run **fully sandboxed**, but the value comes from letting it reach web resources, external tools, and the MCP ecosystem — which requires guardrails to retain trust. The tension behind reducing human interaction is therefore: **how do you automate guardrails, and even set policy so that certain decisions no longer require a human review step?** Stanford CodeX's AILCCP / 48-controls / Cognitive-Escrow / Caremark-RSI series is the densest governance cluster.

### 4. StrongDM-attractor infrastructure (dotfile + harness implementations)

There is a cluster of infrastructure built in the spirit of the StrongDM attractor:
- The **dotfile** library/example is a portable methodology — a single DOT graph that any compliant runner can execute. This batch contains the canonical 2389 Research dot-file article + the literal `dotpowers.dot` payload + the four 2389-family runners (Coven, Mammoth, Smasher, Tracker).
- Various **implemented harnesses**: danshapiro/kilroy and strongdm/attractorbench round out the picture.

### 5. Agent evaluation / probing

To know whether agents are building what we want, we have to probe them. This batch includes SWE-bench (original + Verified), Notion's spec-driven CI loop, Replit's app-testing self-validation, model-vs-model code review (CJ Hess's `kevin`/`carl` aliases), and the Tencent language benchmark — i.e. multiple primary anchors for automating evaluation.

### 6. Harness engineering

The shell around the agent matters so much that **rewriting the harness changes benchmark performance with the same LLM**. The architecture implication is that we must engineer + monitor + evaluate + optimize harnesses with explicit feedback loops. OpenAI's three previously-Cloudflare-blocked harness posts (Harness Engineering, Unlocking the Codex Harness, Running Codex Safely) and Schillace's "What is a harness" four-panel diagram are the canonical primary anchors in this batch; the Codex `.rules` Starlark DSL and Codex subagent TOML are the load-bearing primitives.

### 7. Agents as team members

If the factory is going to approach "dark factory" operation, coordination of many agents has to use **traditional management techniques alongside new ones**. Sources in this batch include Cherny's five-agents-steady-state, Schillace's "compounding teams" + Amplifier, Kim's Sendbird quest-marketplace / token-tier leaderboards, Nystrom's Boxy-from-Notion-comment background agent, and Shapiro's claw-printer / one-claw-per-employee proposal.

---

## How to read each per-source block

Each `###` block has:

- **Title** (cleaned of mojibake)
- **URL** (reconstructed from MHTML `Snapshot-Content-Location` / `Content-Location` headers)
- **Type** — `mhtml` | `txt` | `pdf` | `converted-txt`
- **Themes** — one or more of 1–7 from above
- **Summary** — 1–2 sentences in our voice, content-bearing
- **Image inventory** — total image count and whether any are informationally useful (diagrams, architecture, data) versus chrome (avatars, decorative hero art, UI screenshots)
- **Action taken** — `kept mhtml (useful images preserved)` / `converted to TXT, deleted mhtml` / `deleted (already drained into report NN)` / `txt/pdf passthrough`
- **Prior processing** — citation of any existing report/followup that already drained this URL
- **Recommendation** — one of: `incorporate into report NN`, `supplement to followup/NN`, `new report — <slug> — <one-line angle>`, `skip — already covered in report NN`, `low-priority — <reason>`

---

## Orchestrator decisions (2026-05-16, post-index, pre-drain)

The indexing pass left several `fold into X` / `alternative scope` choices to the next agent. Decisions, with rationale:

| # | Question | Decision | Rationale |
|---|---|---|---|
| 1 | New `27-dotfile-pipelines-as-product` vs separate `2389-dotpowers-portable-methodology` | **Single report 27** covering Dark Factory essay + `dotpowers.dot` blob + dotpowers methodology page. | One thesis ("blueprint, not engine"); fragmenting weakens it. |
| 2 | `schillace-attention-economy` vs `schillace-sunday-letters` super-report | **Single super-report 28-schillace-sunday-letters** covering all 11 Schillace pieces. | Theme-1/6/7 framing recurs across all eleven; a single report supports cross-letter cross-references and avoids triple-counting. |
| 3 | Schillace's *What is a harness* — report 28 or report 09? | **Both.** Primary anchor in report 28; the four-panel diagram and the "gene transfer" coinage also imported into report 09 as the non-OpenAI canonical harness visual. | The diagram is corpus-canonical; report 09 needs it independent of the Schillace super-report. |
| 4 | `27-prompt-engineering-survey` vs fold into report 26 | **Separate new report 29-prompt-engineering-survey.** | Schulhoff's PRISMA taxonomy is a 76-page meta-anchor that overflows report 26's scope (prompt-underspecification). |
| 5 | `cognitive-escrow-and-harness-as-design-site` vs fold into followup/10 | **Separate new report 30-cognitive-escrow.** | Bridges Theme 1 (attention) + Theme 3 (governance) + Theme 6 (harness as design site); the STIR-as-structural-trigger angle is directly actionable for harness design. |
| 6 | `caremark-rsi-board-exposure` vs fold into followup/10 | **Separate new report 31-caremark-rsi-board-exposure.** Cross-cite from followup/10. | Case-law density (8 Delaware/SEC anchors) + RSI-specific scope justifies a dedicated home. |
| 7 | `shapiro-completion-chat-agent-claw` new report? | **Yes — new report 32-shapiro-completion-chat-agent-claw.** | Distinct from existing Shapiro Five-Levels followup; "Claw" is a new top-level taxonomy step (memory + goals + autonomy) and the read/write asymmetry rules are immediately actionable. |
| 8 | `language-choice-as-harness` standalone or fold into 23/followup/07 | **Separate new report 33-language-choice-as-harness.** | Opens a vertical (compiler-as-AI-reviewer + type-system tightness as harness primitive) that is orthogonal to current Anthropic and evals chapters. |
| 9 | `lenny-howiai-personal-harnesses` (CJ Hess) | **Separate new report 34-lenny-howiai-personal-harnesses.** Folds in BOTH the "How I AI" txt (Tenex / Flowy / `kevin`/`carl`) AND the `lenny-build-your-own-ai-developer-tools-with-claude-code.txt` transcript (10X / Flowy / Skills / Ralph loop). | Same engineer, same workflow, two captures — single report cleanest. |
| 10 | `lenny-howiai-spec-driven-and-team-ops` (Nystrom) vs `notion-spec-driven-boxy` | **Single new report 35-lenny-howiai-spec-driven-and-team-ops** covering `lenny-spec-driven-development.txt` AND `The AI engineering workflow at Noti.txt`. | Same engineer (Nystrom), same Boxy stack, two captures. Notion spec-driven detail is also cross-linked into existing report 25. |
| 11 | `sendbird-quests-token-tiers` new report? | **Yes — new report 36-sendbird-quests-token-tiers.** | Quest-marketplace + per-employee token-tier leaderboard ("AI God > 100M/day") is a novel org-design primitive not present elsewhere in the corpus. |
| 12 | `academic-llm-agent-collusion` new report? | **Yes — new report 37-academic-llm-agent-collusion.** | First academic-empirical anchor in the corpus for Theme-2 collusion in market settings (Neves & Bussmann SABM, CADE / Cerebro Project). |
| 13 | LukePM "Software Factory" article | **Low-priority: one-paragraph attribution note into report 01 (footnote-1 chain).** | Definitional / speculative; only durable value is provenance. |

**Report numbering plan (this drain creates reports 27–37, i.e. 11 new numbered reports):**

| # | Slug | Anchor sources | Theme cluster |
|---|---|---|---|
| 27 | `dotfile-pipelines-as-product` | Dark Factory essay (mhtml) + `dotpowers.dot` blob + dotpowers methodology page | 4, 6, 2 |
| 28 | `schillace-sunday-letters` | 11 Schillace pieces (incl. "What is a harness" w/ 4-panel diagram) | 1, 6, 7, 4 |
| 29 | `prompt-engineering-survey` | Schulhoff et al. *The Prompt Report* (arXiv:2406.06608) | 6, 5, 3 |
| 30 | `cognitive-escrow` | Kahana *Cognitive Escrow* (Stanford CodeX) | 3, 1, 6 |
| 31 | `caremark-rsi-board-exposure` | Kahana *Ungovernable Machine* (Stanford CodeX) | 3, 2 |
| 32 | `shapiro-completion-chat-agent-claw` | Shapiro *Completion, Chat, Agent, Claw* | 2, 3, 7 |
| 33 | `language-choice-as-harness` | MacGregor *Does Language Choice Matter?* + Valim/Tencent benchmark | 6, 5, 3 |
| 34 | `lenny-howiai-personal-harnesses` | CJ Hess (Tenex/10X) — Flowy + Skills + Ralph loop + `kevin`/`carl` | 6, 4, 1 |
| 35 | `lenny-howiai-spec-driven-and-team-ops` | Ryan Nystrom (Notion) — Boxy + standup-pre-read + Whisper→spec→Codex | 7, 6, 1 |
| 36 | `sendbird-quests-token-tiers` | John Kim (Sendbird) — Automators + AI-God leaderboard | 7, 1, 5 |
| 37 | `academic-llm-agent-collusion` | Neves & Bussmann SABM (Stanford Computational Antitrust v.6) | 2, 5, 3 |

**Existing-report upgrades during this drain (no new report):**

- Report 01 — LukePM footnote-1 attribution paragraph.
- Report 09 — Schillace "What is a harness" four-panel diagram + Schillace "Artisans and Factory Lines" recipe diagram (both kept as embedded canonical visuals).
- Report 18 — primary-source upgrades for `harness-engineering`, `unlocking-the-codex-harness`, `running-codex-safely`, `developers.openai.com/codex/rules` (replace 🟡 / fill ❌).
- Report 20 — Mastra confirmation from Agent-3 Playground screenshot + new "App Monitoring" substrate-extension subsection.
- Report 22 — primary-source upgrades for `swe-bench-verified` and Princeton PLI SWE-bench blog (replace ❌); save the SWE-bench loop diagram into the report.
- Report 25 — Notion spec-driven workflow as industrial AFIS strategy-3 instance (cross-link to report 35).
- Report 07 (Dark Factory) — refresh 2389 ecosystem (Mammoth→Tracker library extraction, Tracker `Audit/Diagnose/Doctor` API, autopilot personas, budget caps, `.dip` files).
- followup/02-attractor-implementations — add Coven, Mammoth, Smasher, Tracker, dotpowers, post-Feb-2026 Kilroy evolution.
- followup/07-evals-deepdive — drain AttractorBench tier structure, conformance contract, cost-aware scoring, v13 Gemini=0.508 anchor.
- followup/10-governance — incorporate AILCCP principle definitions + 48-controls catalog + AILCCP structural-overview (37 principles / 43 standards / 10 phases / 18 risks); cross-link from new report 30 and report 31.

**Processing order:** clusters A → O. Skip D and G (all duplicates already deleted). One subagent per cluster (for context preservation, NOT for parallelism). After each cluster commit a checkpoint and update PLAN.md.

---

## Per-source entries

## Roll-up summary

### File counts after this pass

| Disposition | Count |
|---|---|
| Kept as `.mhtml` (informative images preserved) | 7 |
| Converted to `.txt` (no informative images, mhtml deleted) | 34 |
| Passthrough `.txt` / `.pdf` (no MHTML conversion needed) | 6 |
| Deleted as already-drained duplicate | 24 |
| **Total sources processed** | **71** |

### Recommendation roll-up

Proposed new reports (the next agent should triage these against current corpus shape — many can be merged):

| Proposed slug | Anchor source(s) | Primary themes |
|---|---|---|
| `27-dotfile-pipelines-as-product` | Harper Reed's *Dark Factory Is a .dot file* + `dotpowers.dot` blob | 4, 6 |
| `2389-dotpowers-portable-methodology` | `2389.ai/products/dotpowers` page (alt: fold into above) | 4, 6, 2 |
| `schillace-attention-economy` (or `schillace-sunday-letters` super-report) | 11 Schillace Sunday Letters covering attention + harness + agent-shaped surfaces + compounding teams + last-mile | 1, 6, 7 |
| `27-prompt-engineering-survey` | Schulhoff et al. *The Prompt Report* (arXiv:2406.06608) | 6, 5, 3 |
| `cognitive-escrow-and-harness-as-design-site` | Kahana's *Cognitive Escrow* | 3, 1, 6 |
| `caremark-rsi-board-exposure` | Kahana's *Ungovernable Machine* (Delaware case-law spine + SB 53) | 3, 2 |
| `academic-llm-agent-collusion` | Neves & Bussmann *Smart Agent-Based Modelling* (Stanford Computational Antitrust) | 2, 5, 3 |
| `shapiro-completion-chat-agent-claw` | Shapiro's *Completion, Chat, Agent, Claw* | 2, 3, 7 |
| `language-choice-as-harness` | MacGregor's *Does Language Choice Matter?* + Valim/Tencent benchmark | 6, 5, 3 |
| `lenny-howiai-personal-harnesses` | Lenny × CJ Hess (Flowy + Skills + Ralph loop) | 6, 4, 1 |
| `lenny-howiai-spec-driven-and-team-ops` | Lenny × Nystrom (Notion's Boxy + standup pre-read) | 7, 6, 1 |
| `sendbird-quests-token-tiers` | Kim's Sendbird Automators + AI-God leaderboard | 7, 1, 5 |
| `notion-spec-driven-boxy` (alt: fold into `lenny-howiai-spec-driven-and-team-ops`) | Nystrom *AI engineering workflow at Notion* | 6, 1, 7 |

Primary-source upgrades to existing reports (replace `🟡` or `❌` rows with `✅` primary anchors):

| Target report | Source | Notes |
|---|---|---|
| `18-openai-codex-substrate` | `openai.com/index/harness-engineering` | Cloudflare-blocked URL now drainable from manual capture (S9 anchor) |
| `18-openai-codex-substrate` | `openai.com/index/unlocking-the-codex-harness` | App Server article — Cloudflare-blocked → primary |
| `18-openai-codex-substrate` | `openai.com/index/running-codex-safely` | New OpenAI-internal deployment posture + OpenTelemetry telemetry stack |
| `18-openai-codex-substrate` | `developers.openai.com/codex/rules` | `.rules` Starlark DSL — load-bearing primitive, not currently anchored |
| `22-academic-foundations` | `openai.com/index/introducing-swe-bench-verified` | Cloudflare-blocked → primary |
| `22-academic-foundations` | `pli.princeton.edu/blog/2023/swe-bench-...` | Princeton PLI blog Cloudflare-blocked → primary |
| `20-replit-agent` | `blog.replit.com/app-monitoring` | New substrate-extension into post-deploy observability |
| `20-replit-agent` | `blog.replit.com/introducing-agent-3-...` | Agent-3 Playground screenshot reads "Powered by Mastra" → first-party Mastra confirmation |

Existing-report extensions (text-only, no status flip):

- `02-strongdm-attractor` + `followup/02-attractor-implementations`: add **Coven, Mammoth, Smasher, Tracker, dotpowers** (the four runners + the methodology payload + the GitHub READMEs document new evolution signals — Mammoth→Tracker library extraction, Tracker now has 52 releases / programmatic Audit/Diagnose/Doctor API + autopilot personas / `.dip` files / budget caps).
- `02-strongdm-attractor` + `followup/02-attractor-implementations`: add **Coven** as Rust swarm/workspace orchestrator (gRPC, MCP packs) — a sibling to the DOT-pipeline cluster.
- `followup/02-attractor-implementations`: add **AttractorBench** (Apache-2.0 GitHub benchmark with tiered scoring, v13 Gemini=0.508 anchor), **Kilroy post-Feb-2026 evolution** (Platform reframe PR #81, `KILROY_PREDECESSOR_NODE/OUTCOME` handler env, `progress.ndjson`, `.agents/skills`/`.claude`/`.gemini/skills` triple-skill substrate).
- `followup/07-evals-deepdive`: drain **AttractorBench**'s tier structure (tier0 smoke → unified LLM SDK → coding agent loop → full pipeline runner), the language-agnostic conformance contract, the cost-aware scoring, and the AGENTS.md curation runbook.
- `followup/10-governance`: incorporate **Kahana's 48-controls** catalog (named controls: Agent Kill Switch, Rollback and Quarantine, Rate and Scope Limiter, Intervention Audit Trail, Acceptance Threshold Governance, Supply Chain Vetting, Multi-Agent Protocol Security, Confidential Computing Environment, Context-to-Output Lineage, Continuous Validation, Culture & Capability Index) plus the AILCCP structural-overview (37 principles / 43 standards / 10 phases / 18 risks / 500+ cross-references / named per-phase metrics).
- `followup/10-governance`: incorporate the **AI Life Cycle Core Principles** primary article — anchor Metrics/Accuracy/Accountability/Workforce-Compatible/Trustworthy/Human-Centered principle definitions and ISO cross-references.
- `25-requirements-engineering-foundations`: add **Notion's spec-driven workflow** as an industrial instance of "specs-as-source-of-truth" (Strategy 3 from AFIS/INCOSE-FR mapping).
- `09-jaymin-book-harnesses-practices-mental-models`: add **Schillace's "What is a harness"** four-panel diagram as the canonical non-OpenAI primary anchor for the harness-engineering concept, and **Schillace's "Artisans and Factory Lines"** recipe diagram for the syntactic↔semantic boundary.
- `23-anthropic-engineering-trilogy` (or `12-adjacent-ecosystem`): incorporate **CJ Hess's Flowy + `kevin`/`carl` model-vs-model QC loop** as a personal-harness case study and a model-as-critic pattern.

Already-drained duplicates (deleted in this pass, see per-source entries below for the disposition reference):
- `Codex _ OpenAI Developers.mhtml` (report 18)
- `Agent approvals & security – Codex _ OpenAI Developers.mhtml` (report 18)
- `Cloud environments – Codex web _ OpenAI Developers.mhtml` (report 18)
- `Custom instructions with AGENTS.md – Codex _ OpenAI Developers.mhtml` (report 18)
- `Subagents – Codex _ OpenAI Developers.mhtml` (report 18)
- All eight `Replit Docs *.mhtml` pages + both `Replit — Introducing *` Agent-3/4 product pages + `Replit — Introducing Connectors` (report 20)
- `Built by Agents, Tested by Agents, Trusted by Whom?.mhtml` (followup/10-governance §1.1)
- `The Software Factory: When No Human Writes or Reviews the Code.mhtml` (followup/10-governance §1.3)
- `Head of Claude Code What happens after coding is solved Boris Cherny.txt` (followup/03-cherny-interview)
- `How Every Is Harnessing the World-c.txt` (followup/05-klaassen-siblings §3)
- `Stop Coding and Start Planning.txt` (followup/05-klaassen-siblings)
- `Teach Your AI to Think Like a Senio.txt` (followup/05-klaassen-siblings)
- `You Don't Write the Code. You Don't Read the Code Either. – Dan Shapiro's Blog.txt` (followup/01-shapiro-five-levels)

---

## Per-source entries

The blocks below are grouped by source cluster (preserving the chunking the indexing subagents used — a natural unit for the next ingestion-planning pass).

---

### Cluster A — 2389 Research product pages (2389.ai/products/*)

#### Coven — 2389 Research, Inc.txt
- **Original filename:** Coven — 2389 Research, Inc.mhtml
- **Title:** Coven — 2389 Research, Inc
- **URL:** https://2389.ai/products/coven/
- **Type:** converted-txt
- **Themes:** 4 (StrongDM-attractor infrastructure), 6 (harness engineering), 7 (agents as team members)
- **Summary:** Coven is a self-hosted agent-orchestration platform (Go gateway + Rust mux agents + iOS/macOS app + TUI) that routes messages between Claude Code sessions and chat bridges (Matrix/Slack/Telegram) over Tailscale, providing identity, persistence, and tool access without exposing anything to the public internet.
- **Image inventory:** 1 total; 0 useful — single stylized hero illustration showing an octagonal hub with eight spokes to geometric node-shape glyphs (decorative reinterpretation of attractor node shapes, no readable data).
- **Action taken:** converted to TXT, deleted mhtml
- **Prior processing:** not found in existing reports (2389.ai/products/coven URL not cited anywhere; "Coven" name not in any report or followup)
- **Recommendation:** supplement to followup/02-attractor-implementations — Coven is a sixth 2389-family implementation not surveyed there. Adds the "self-hosted Tailscale gateway + native client" axis to the comparison.

#### Mammoth — 2389 Research, Inc.txt
- **Original filename:** Mammoth — 2389 Research, Inc.mhtml
- **Title:** Mammoth — 2389 Research, Inc
- **URL:** https://2389.ai/products/mammoth/
- **Type:** converted-txt
- **Themes:** 4, 6, 3 (human gates)
- **Summary:** Mammoth is a Go DOT-pipeline runner that executes directed graphs node-by-node, dispatching each stage to an OpenAI/Anthropic/Gemini coding agent with checkpointing, retry, multi-provider support, and human-in-the-loop gates; it validates DOT files against 21 lint rules before walking the DAG.
- **Image inventory:** 1 total; 0 useful — decorative hero flow art with labeled boxes (PROCESSING / HUMAN REVIEW / ANALYSIS / VALIDATION / PUBLISH / FORK).
- **Action taken:** converted to TXT, deleted mhtml
- **Prior processing:** referenced in 07-dark-factory as secondary (named with a one-line quote and a GitHub link); the marketing page itself is not cited.
- **Recommendation:** supplement to followup/02-attractor-implementations — Mammoth deserves a row alongside Kilroy/Forge/Fabro; the 21-lint-rule detail and model-stylesheet mention are concrete additions.

#### Smasher — 2389 Research, Inc.txt
- **Original filename:** Smasher — 2389 Research, Inc.mhtml
- **Title:** Smasher — 2389 Research, Inc
- **URL:** https://2389.ai/products/smasher/
- **Type:** converted-txt
- **Themes:** 4, 6, 1 (in-browser human-gate answering)
- **Summary:** Smasher is an explicit Rust reimplementation of strongDM's attractor — five crates running DOT directed graphs through nine node types (box/diamond/oval/house/hexagon/parallelogram/component etc.), with streaming output, a web dashboard for live pipeline observation, and in-browser human-gate question answering.
- **Image inventory:** 1 total; 0 useful — decorative woodcut-style factory illustration, not an architecture diagram.
- **Action taken:** converted to TXT, deleted mhtml
- **Prior processing:** referenced in 07-dark-factory as secondary; the marketing page itself is not cited.
- **Recommendation:** supplement to followup/02-attractor-implementations — the explicit "Rust reimplementation of strongDM's attractor" self-description + nine-node-type taxonomy directly supports the followup's convergence thesis.

#### Tracker — 2389 Research, Inc.txt
- **Original filename:** Tracker — 2389 Research, Inc.mhtml
- **Title:** Tracker — 2389 Research, Inc
- **URL:** https://2389.ai/products/tracker/
- **Type:** converted-txt
- **Themes:** 4, 6, 3 (checkpoints + human gates)
- **Summary:** Tracker is a Go implementation of strongDM's Attractor framework that executes DOT DAGs in topological order with concurrent branches, automatic checkpoint/resume from `.tracker/runs/<runID>/checkpoint.json`, human-in-the-loop gates, LLM-powered nodes, retry logic, and a bubbletea TUI for live pipeline observation.
- **Image inventory:** 1 total; 0 useful — decorative hero art only.
- **Action taken:** converted to TXT, deleted mhtml
- **Prior processing:** referenced in 07-dark-factory as secondary; the marketing page itself is not cited.
- **Recommendation:** supplement to followup/02-attractor-implementations — `bubbletea` TUI + per-run checkpoint-directory contract is a useful contrast with Kilroy's CXDB and Forge's JSONL event stream.

#### dotpowers — 2389 Research, Inc.txt
- **Original filename:** dotpowers — 2389 Research, Inc.mhtml
- **Title:** dotpowers — 2389 Research, Inc
- **URL:** https://2389.ai/products/dotpowers/
- **Type:** converted-txt
- **Themes:** 4, 6, 2 (multi-model review)
- **Summary:** dotpowers is a single ~1300-line DOT file that encodes the "superpowers" development methodology (brainstorm → plan with TDD → build with multi-model review → ship) as a six-phase pipeline graph runnable by any attractor-compliant runner (tracker, mammoth, smasher), turning a one-line `idea.md` into a tested, reviewed project in a git branch.
- **Image inventory:** 1 total; 0 useful — decorative six-phase icon strip.
- **Action taken:** converted to TXT, deleted mhtml
- **Prior processing:** referenced in 07-dark-factory as secondary (GitHub URL listed); marketing page not cited and dotpowers not in followup/02 (which surveys runners, not pipeline payloads).
- **Recommendation:** **new report — `2389-dotpowers-portable-methodology`** — first concrete evidence in this corpus that an Attractor DOT file is being shipped as a **portable methodology payload** (run on any compliant engine), separating the "what" (methodology graph) from the "how" (runner). A different abstraction layer than the runner comparison in followup/02. Alternatively fold into the proposed `27-dotfile-pipelines-as-product` report.

---

### Cluster B — 2389 Research GitHub repos

#### 2389-research_coven_ Rust platform for orchestrating AI agents with tool capabilities and gRPC streaming.txt
- **Original filename:** `2389-research_coven_ Rust platform for orchestrating AI agents with tool capabilities and gRPC streaming.mhtml`
- **Title:** 2389-research/coven: Rust platform for orchestrating AI agents with tool capabilities and gRPC streaming
- **URL:** https://github.com/2389-research/coven
- **Type:** converted-txt
- **Themes:** 4, 6, 7
- **Summary:** Coven is a 2389 Research Rust monorepo for orchestrating Claude-backed AI agents: a coven-agent single-workspace binary, a coven-swarm multi-workspace supervisor, a Go coven-gateway (routing, storage, pack registry), gRPC streaming via coven-proto, and a Pack SDK (mcp-bridge-pack, productivity-pack) for shipping tools — distinct from the dotpowers/mammoth/smasher/tracker DOT-pipeline family.
- **Image inventory:** 6 total; 0 useful — all GitHub avatar PNGs <12 KB.
- **Action taken:** converted to TXT, deleted mhtml
- **Prior processing:** not found (Coven is not URL-cited in 07-dark-factory).
- **Recommendation:** incorporate into report 02-strongdm-attractor as new entry in the Attractor-implementations roster + supplement to followup/02-attractor-implementations as "Coven (2389 Research, Rust) — swarm/workspace orchestrator with gRPC streaming, MCP pack bridge".

#### 2389-research_dotpowers_ a superpowers implementation for attractors.txt
- **Original filename:** `2389-research_dotpowers_ a superpowers implementation for attractors.mhtml`
- **Title:** 2389-research/dotpowers: a superpowers implementation for attractors
- **URL:** https://github.com/2389-research/dotpowers
- **Type:** converted-txt
- **Themes:** 4, 6, 1
- **Summary:** dotpowers DOT pipeline (~1300 lines) encoding the "superpowers" dev methodology for any attractor-compliant runner: idea.md → Brainstorm → Plan (GPT-5.2 drafts, Opus audits, max 5 iter) → Setup → TDD Implement (Opus spec-check + GPT-5.4 quality-check per task; batch human checkpoint every 3 tasks) → 3-model cross-critiqued Review → human-chosen Ship. Documents concrete failure modes including "burned 3.5M OpenAI tokens on a single bad run before adding loop limits".
- **Image inventory:** 6 total; 0 useful — GitHub avatars.
- **Action taken:** converted to TXT, deleted mhtml
- **Prior processing:** referenced in 07-dark-factory sources block (URL only); README content not drained.
- **Recommendation:** incorporate into report 07-dark-factory as a worked example of "batch human review every N tasks + 3-model cross-critique + hard loop caps" + supplement to followup/02 with concrete model assignments (Opus 4.6 = audits, GPT-5.4 = TDD, GPT-5.2 = planning, Gemini 3.5 Flash = third-opinion review).

#### 2389-research_mammoth.txt
- **Original filename:** `2389-research_mammoth.mhtml`
- **Title:** 2389-research/mammoth
- **URL:** https://github.com/2389-research/mammoth
- **Type:** converted-txt
- **Themes:** 4, 6
- **Summary:** Mammoth is a Go DOT-based pipeline runner for LLM agent workflows whose pipeline execution is now delegated to the external 2389-research/tracker library — Mammoth keeps the DOT parser/validator, the web UI (port 2389), the Bubble Tea TUI, an MCP server, the CLI, plus a unified llm/ client for OpenAI/Anthropic/Gemini and an event-sourced spec builder. README claims 5,200+ tests, current v0.8.0 (Feb 2026), Homebrew distribution.
- **Image inventory:** 6 total; 0 useful — GitHub avatars.
- **Action taken:** converted to TXT, deleted mhtml
- **Prior processing:** referenced in 07-dark-factory sources block (URL only) and quoted via El Kaim; README content not drained.
- **Recommendation:** incorporate into report 07-dark-factory as evidence of Mammoth→Tracker library-extraction (2389 ecosystem itself converging on tracker as canonical engine, refining "independent convergence" claim) + supplement to followup/02.

#### 2389-research_smasher_ A builder.txt
- **Original filename:** `2389-research_smasher_ A builder.mhtml`
- **Title:** 2389-research/smasher: A builder
- **URL:** https://github.com/2389-ai/smasher (note org is `2389-ai`, not `2389-research`)
- **Type:** converted-txt
- **Themes:** 4, 6, 3
- **Summary:** Smasher is a Rust five-crate reimplementation of strongDM's attractor — smasher-llm (multi-provider client), smasher-agent (read/write/edit/shell/grep/glob tools + steering rules + sandboxed subagents), smasher-attractor (DOT graph engine that resolves node types from DOT *shapes*: circle=start, box=codergen, diamond=conditional, oval=interviewer, house=manager human-approval-gate, parallelogram=parallel fan-out, hexagon=tool, component=sub-pipeline), smasher-cli, and an HTMX dashboard (port 21541) with SSE event streaming. ~2,700 tests.
- **Image inventory:** 6 total; 0 useful — GitHub avatars.
- **Action taken:** converted to TXT, deleted mhtml
- **Prior processing:** referenced in 07-dark-factory sources block (URL only) and quoted via El Kaim; README content not drained.
- **Recommendation:** incorporate into report 07-dark-factory as concrete evidence of the DOT-shape→node-type mapping convention (transferable Attractor-spec invariant) + supplement to followup/02.

#### 2389-research_tracker.txt
- **Original filename:** `2389-research_tracker.mhtml`
- **Title:** 2389-research/tracker
- **URL:** https://github.com/2389-research/tracker
- **Type:** converted-txt
- **Themes:** 4, 6, 3, 5
- **Summary:** Tracker is the Go pipeline runtime that now powers Mammoth and is the runner referenced by dotpowers — 9 contributors, v0.28.2 (May 14 2026, 52 releases), programmatic Go API (tracker.Run, tracker.Audit, tracker.Diagnose, tracker.DiagnoseMostRecent, tracker.Simulate, tracker.Doctor, tracker.NewNDJSONWriter) + CLI with built-in workflows, autopilot personas (lax/mid/hard/mentor) that replace human gates with an LLM judge, --auto-approve for fully headless runs, webhook-driven human gates with timeout policy, run-level budget caps (--max-tokens, --max-cost, --max-wall-time), tool denylist/allowlist with output-size ceiling, Cloudflare AI Gateway routing, portable `--export-bundle` git-bundle output. Pipelines are .dip files (legacy `.dot` deprecated).
- **Image inventory:** 13 total; 0 useful — GitHub contributor avatars.
- **Action taken:** converted to TXT, deleted mhtml
- **Prior processing:** referenced in 07-dark-factory sources block (URL only) and quoted via El Kaim ("a weekend-scale implementation with automatic checkpointing"); the description is badly stale.
- **Recommendation:** incorporate into report 07-dark-factory as a major update — tracker is no longer "weekend-scale" but the canonical engine; its `Diagnose`/`Audit`/`Doctor`/`Simulate` API plus autopilot-persona gates + budget caps + denylist directly answer the report's open questions on pause/gate semantics and maintenance loop. Also supplement to followup/02 + cross-cite from followup/10-governance's gate-policy discussion.

---

### Cluster C — Dotfile + harness implementations

#### The Dark Factory Is a .dot file — 2389 Research, Inc.mhtml *(kept)*
- **Title:** The Dark Factory Is a .dot file — 2389 Research, Inc
- **URL:** https://2389.ai/posts/the-dark-factory-is-a-dot-file/
- **Type:** mhtml
- **Themes:** 4, 6, 2 (convergence)
- **Summary:** Harper Reed's Mar-9-2026 essay arguing the attractor convergence thesis empirically: StrongDM's NLSpec produced four independent implementations (Kilroy, Mammoth, Smasher, Tracker) that all converged on the same three-layer architecture (LLM client / agent loop / DOT pipeline engine), and the next leverage point is the .dot pipeline files themselves — reusable Graphviz blueprints with human gates, fan-in joins, verification nodes, multi-model review — which are mostly being kept private even as the engines proliferate. Names dorodango (Jesse Vincent), AttractorBench tiers, and contrasts a deterministic vulnerability-analyzer pipeline (no LLM nodes) with the dotpowers superpowers-as-a-pipeline DAG.
- **Image inventory:** 9 total; **3 useful** — dotpowers DOT-graph render (huge multi-stage DAG: brainstorm → plan-TDD → implement → multi-model review → ship), sprint-exec DOT-graph render (Ensure Ledger → Find/Set/Read Sprint → Implement → Validate → Commit → parallel Claude/Codex/Gemini reviews → cross-critiques → Review Analysis pass/fail), build-pong DOT-graph render (linear Plan → Scaffold → Implement → Compile → Review → Polish loop). Four product-hero PNGs are decorative.
- **Action taken:** kept mhtml (useful images preserved)
- **Prior processing:** not found.
- **Recommendation:** **new report — `27-dotfile-pipelines-as-product`** — frame the .dot pipeline file (not the runner) as the durable artifact. Drain the four-implementation convergence table, the vulnerability-analyzer / sprint-exec / build-pong / dotpowers pipeline styles, and the "engines open / blueprints private" asymmetry; cross-cite into 07-dark-factory and followup/02.

#### dotpowers_dotpowers.dot at main · 2389-research_dotpowers.txt
- **Original filename:** `dotpowers_dotpowers.dot at main · 2389-research_dotpowers.mhtml`
- **Title:** dotpowers/dotpowers.dot at main · 2389-research/dotpowers
- **URL:** https://github.com/2389-research/dotpowers/blob/main/dotpowers.dot
- **Type:** converted-txt
- **Themes:** 4, 6, 7
- **Summary:** GitHub blob view of `dotpowers.dot` — the canonical Graphviz source of the "Superpowers as a Mammoth Pipeline" DAG, ~114 KB of attribute-laden DOT defining nodes for brainstorm/idea-refinement, TDD planning, multi-model implementation, multi-model review/consensus, and ship. The actual graph syntax (node shapes, edge labels, retry policies, prompts) is the substantive payload.
- **Image inventory:** 3 total; 0 useful — GitHub avatars.
- **Action taken:** converted to TXT, deleted mhtml
- **Prior processing:** repo URL appears in 07-dark-factory link list and followup/04-gastown-beads; the specific `dotpowers.dot` blob is not drained.
- **Recommendation:** incorporate into the proposed `27-dotfile-pipelines-as-product` report as the worked example — quote the graph header (label/goal/rankdir/default_max_retry) and a node-attribute block to show how prompts, retries, and join policies are encoded inline in DOT.

#### danshapiro_kilroy.txt
- **Original filename:** `danshapiro_kilroy.mhtml`
- **Title:** danshapiro/kilroy
- **URL:** https://github.com/danshapiro/kilroy
- **Type:** converted-txt
- **Themes:** 4, 6, 3 (git-worktree isolation)
- **Summary:** GitHub repo landing page at main@b55fb0f — 944 commits, 197 stars, 49 forks, MIT, Go; latest commit "feat: expose KILROY_PREDECESSOR_NODE/OUTCOME env to handlers"; structure includes `cmd/kilroy`, `internal`, `.agents/skills`, `.claude`, `.gemini/skills`, demo, docs, research subdirs, plus a Platform reframe ("layered engine, tmux agents, workflow packages", PR #81, Apr 17 2026) and recent run-completion event emission to `progress.ndjson`.
- **Image inventory:** 16 total; 0 useful — GitHub avatars.
- **Action taken:** converted to TXT, deleted mhtml
- **Prior processing:** referenced in followup/02-attractor-implementations as a canonical attractor implementation row; the repo landing page itself was not drained.
- **Recommendation:** supplement to followup/02-attractor-implementations — add post-Feb-2026 evolution signals (PR #81 Platform reframe, `KILROY_PREDECESSOR_NODE/OUTCOME` handler env vars, `progress.ndjson` terminal events, `.agents/skills`/`.claude`/`.gemini/skills` triple-skill-substrate layout).

#### strongdm_attractorbench_ ... NLSpec instruction following benchmark.txt
- **Original filename:** `strongdm_attractorbench_ NLSpec instruction following benchmark for https___factory.strongdm.ai_products_attractor.mhtml`
- **Title:** strongdm/attractorbench — NLSpec instruction-following benchmark for factory.strongdm.ai/products/attractor
- **URL:** https://github.com/strongdm/attractorbench
- **Type:** converted-txt
- **Themes:** 5, 4, 6
- **Summary:** GitHub repo landing for AttractorBench at main@cb5797e (Feb 26 2026), 17 stars, 8 forks, Apache-2.0; commits include "Add v13 slate results and update Gemini best to 0.508", "Rename full-stack to main and drop tier0 from headline scores" — a live tiered benchmark (tier0 smoke + main tiers) scoring how well coding agents implement the attractor NLSpec, with curated logs, a LEADERBOARD.md, AGENTS.md runbook, and a `specs/` corpus. Best Gemini score 0.508 anchors current SoTA.
- **Image inventory:** 4 total; 0 useful — GitHub avatars.
- **Action taken:** converted to TXT, deleted mhtml
- **Prior processing:** referenced in 07-dark-factory link list and flagged in followup/02 as "the corpus's only behavioral benchmark for NLSpec-driven coding agents. Worth a follow-up" — explicitly NOT yet drained.
- **Recommendation:** supplement to followup/07-evals-deepdive — drain the tier structure, the conformance contract, deterministic verification, cost-aware scoring, the v13 leaderboard Gemini=0.508 anchor, and the AGENTS.md curation runbook; cross-link from followup/02.

---

### Cluster D — Codex developer docs (core)

#### Codex _ OpenAI Developers.mhtml *(deleted — duplicate)*
- **URL:** https://developers.openai.com/codex
- **Themes:** 6, 3
- **Summary:** Marketing/landing overview describing Codex with five-surface IA (App / IDE Extension / CLI / Web / Integrations & Automation).
- **Image inventory:** 6 total; 0 useful — brand wallpapers and SVG logo.
- **Action taken:** deleted (already drained into report 18)
- **Prior processing:** primary source in report 18 (S8) — primary-fetched 2026-05-13 via issue #41.
- **Recommendation:** skip — already covered in report 18.

#### Agent approvals & security – Codex _ OpenAI Developers.mhtml *(deleted — duplicate)*
- **URL:** https://developers.openai.com/codex/agent-approvals-security
- **Themes:** 3, 1, 6
- **Summary:** Approval-mode matrix (read-only / workspace-write / danger-full-access × on-failure / untrusted / never) × macOS Seatbelt and Linux Landlock/seccomp sandboxes — the trifecta defense (capability + approval + network gating) that report 18 §4 anchors on.
- **Image inventory:** 1 total; 0 useful — SVG logo.
- **Action taken:** deleted (already drained into report 18)
- **Prior processing:** primary source in report 18 (S23).
- **Recommendation:** skip — already covered in report 18.

#### Cloud environments – Codex web _ OpenAI Developers.mhtml *(deleted — duplicate)*
- **URL:** https://developers.openai.com/codex/cloud/environments
- **Themes:** 3, 6, 4
- **Summary:** Codex-web cloud-task substrate: isolated OpenAI-managed container per task, repo preloaded, network off by default, outbound restricted to per-environment allowlist — the actual-concurrency surface that makes parallel Subagents practical.
- **Image inventory:** 1 total; 0 useful — SVG logo.
- **Action taken:** deleted (already drained into report 18)
- **Prior processing:** primary source in report 18 (Cloud-env row).
- **Recommendation:** skip — already covered in report 18.

#### Custom instructions with AGENTS.md – Codex _ OpenAI Developers.mhtml *(deleted — duplicate)*
- **URL:** https://developers.openai.com/codex/guides/agents-md
- **Themes:** 6, 3, 7
- **Summary:** Canonical AGENTS.md spec — global→project discovery order, AGENTS.override.md per-scope escape hatch, root-to-leaf concatenation joined with blank lines (files closer to cwd take precedence), 32 KiB `project_doc_max_bytes`, `project_doc_fallback_filenames`, `CODEX_HOME`.
- **Image inventory:** 1 total; 0 useful — SVG logo.
- **Action taken:** deleted (already drained into report 18)
- **Prior processing:** primary source in report 18 (S10).
- **Recommendation:** skip — already covered in report 18.

---

### Cluster E — Codex developer docs (control surfaces)

#### Rules – Codex _ OpenAI Developers.txt
- **Original filename:** `Rules – Codex _ OpenAI Developers.mhtml`
- **Title:** Rules — Codex | OpenAI Developers
- **URL:** https://developers.openai.com/codex/rules
- **Type:** converted-txt
- **Themes:** 3, 6
- **Summary:** Documents Codex's experimental `.rules` file (Starlark-based `prefix_rule(...)` with `allow`/`prompt`/`forbidden` decisions, optional inline `match`/`not_match` unit tests, and "most restrictive wins" merging) used to control which shell commands Codex may run outside the sandbox. Covers tree-sitter-based safe splitting of `bash -lc` compound commands (per-command evaluation when scripts are linear chains; conservative whole-string evaluation when scripts use redirection / substitution / env-vars / wildcards / control flow), the `codex execpolicy check` test harness, and admin enforcement via `requirements.toml`.
- **Image inventory:** 1 total; 0 useful — SVG logo.
- **Action taken:** converted to TXT, deleted mhtml
- **Prior processing:** not found (report 18 mentions `rules` only as the name of an approval-category; the `.rules` file format and Starlark DSL are unindexed).
- **Recommendation:** incorporate into report 18-openai-codex-substrate as a new subsection on the Rules DSL — this is the load-bearing primitive that makes V&V auto-rejection auditable.

#### Subagents – Codex _ OpenAI Developers.mhtml *(deleted — duplicate)*
- **URL:** https://developers.openai.com/codex/subagents
- **Themes:** 7, 6, 3
- **Summary:** Primary spec for Codex subagent orchestration: built-in `default`/`worker`/`explorer` + user-defined TOML custom agents (required `name`/`description`/`developer_instructions`; optional `nickname_candidates`, `model`, `model_reasoning_effort`, `sandbox_mode`, `mcp_servers`, `skills.config`); global `[agents]` knobs `max_threads` (default 6), `max_depth` (default 1 — warns raising it converts broad delegation prompts into runaway fan-out), `job_max_runtime_seconds` (default 1800s). Documents `/agent` CLI, parent-turn override re-application, experimental `spawn_agents_on_csv` batch primitive (CSV in, `report_agent_job_result` per worker, CSV out).
- **Image inventory:** 1 total; 0 useful — SVG logo.
- **Action taken:** deleted (already drained into report 18, S11)
- **Prior processing:** primary source in report 18 (S11).
- **Recommendation:** skip — already covered. (Optional: the `spawn_agents_on_csv` CSV-fan-out contract and the explicit `max_depth=1` runaway-fan-out warning are useful supporting quotes if report 18 expands its multi-agent section.)

#### Running Codex safely at OpenAI _ OpenAI.txt
- **Original filename:** `Running Codex safely at OpenAI _ OpenAI.mhtml`
- **Title:** Running Codex safely at OpenAI | OpenAI
- **URL:** https://openai.com/index/running-codex-safely/
- **Type:** converted-txt
- **Themes:** 3, 6, 1
- **Summary:** OpenAI security-team blog (May 8 2026) on how OpenAI itself deploys Codex: sandbox-defines-execution-boundary + approval-policy-defines-when-to-ask, with `Auto-review` mode delegating routine approvals to an auto-approval subagent so humans are interrupted only for higher-risk or unintended-consequence actions. Documents managed network policy (`allowed_domains`/`denied_domains`, `allow_local_binding`, `allowed_web_search_modes = ["cached"]`), OS-keyring credential storage, forced ChatGPT-workspace pinning, admin-enforced `requirements.toml` (cloud-managed requirements + macOS managed preferences + local requirements), and **OpenTelemetry log export** of prompts / tool-approvals / tool-results / MCP-usage / network-proxy decisions — feeding an internal AI-powered security triage agent that reconstructs intent (the "why") rather than SIEM-style "what". Confirms `openai.com/index/*` host is now reachable.
- **Image inventory:** 0 total; 0 useful.
- **Action taken:** converted to TXT, deleted mhtml
- **Prior processing:** not found.
- **Recommendation:** incorporate into report 18-openai-codex-substrate as a new section on operational/deployment posture and agent-native telemetry stack — directly addresses report 18's still-🟡 "operational productivity numbers" gap; also worth cross-citing from followup/10-governance (concrete agent-native-telemetry exemplar) and followup/08-security-primitives. Also note this is a previously-Cloudflare-blocked URL now successfully captured.

---

### Cluster F — OpenAI Index harness articles

#### Harness engineering_ leveraging Codex in an agent-first world _ OpenAI.txt
- **Original filename:** `Harness engineering_ leveraging Codex in an agent-first world _ OpenAI.mhtml`
- **Title:** Harness engineering: leveraging Codex in an agent-first world | OpenAI
- **URL:** https://openai.com/index/harness-engineering/
- **Type:** converted-txt
- **Themes:** 6, 1, 2
- **Summary:** Ryan Lopopolo (OpenAI, Feb 11 2026) — internal experiment: 3-to-7-engineer team shipped ~1M LOC across ~1,500 merged PRs (3.5 PRs/engineer/day) in five months with zero hand-written lines, all generated by Codex; engineers' role shifted to designing environments, AGENTS.md spec ingestion, increasing application/agent legibility, taste enforcement, throughput-driven merge philosophy, levels of autonomy, and entropy/garbage-collection regimes.
- **Image inventory:** 0 total; 0 useful (text-only).
- **Action taken:** converted to TXT, deleted mhtml
- **Prior processing:** primary source in report 18 (S9 anchor) — quoted via `celesteanders/harness` mirror because canonical URL was Cloudflare-blocked; this is the first canonical fetch.
- **Recommendation:** incorporate into report 18 as primary-fetch upgrade for S9 (replace 🟡 mirror provenance with ✅; verify all existing quotations against canonical text and update sources table).

#### Introducing SWE-bench Verified _ OpenAI.txt
- **Original filename:** `Introducing SWE-bench Verified _ OpenAI.mhtml`
- **Title:** Introducing SWE-bench Verified | OpenAI
- **URL:** https://openai.com/index/introducing-swe-bench-verified/
- **Type:** converted-txt
- **Themes:** 5, 6
- **Summary:** OpenAI's Aug 13 2024 (updated Feb 24 2025) announcement of SWE-bench Verified — 500-instance human-validated subset built in collaboration with SWE-bench authors after Preparedness-framework testing found many original instances under-specified or unsolvable; details annotation methodology, FAIL_TO_PASS / PASS_TO_PASS mechanics, re-measured GPT-4o lift on cleaner subset.
- **Image inventory:** 0 total; 0 useful.
- **Action taken:** converted to TXT, deleted mhtml
- **Prior processing:** referenced in report 22 as ❌ unobtainable (Cloudflare-blocked); swebench.com/verified was used as proxy.
- **Recommendation:** incorporate into report 22-academic-foundations as primary-fetch upgrade — replace ❌ row with ✅, quote the 500-instance / human-validation rationale + Preparedness Framework framing; also candidate citation for report 18.

#### Unlocking the Codex harness_ how we built the App Server _ OpenAI.txt
- **Original filename:** `Unlocking the Codex harness_ how we built the App Server _ OpenAI.mhtml`
- **Title:** Unlocking the Codex harness: how we built the App Server | OpenAI
- **URL:** https://openai.com/index/unlocking-the-codex-harness/
- **Type:** converted-txt
- **Themes:** 6, 4 (protocol substrate)
- **Summary:** Celia Chen (OpenAI, Feb 4 2026) — Codex App Server as a bidirectional JSON-RPC API born from the VS Code extension's need to reuse the CLI's agent loop after MCP proved unfit; harness internals, Thread/Turn/Item conversation primitives, client integration patterns (CLI / IDE / Xcode / JetBrains / macOS app), and the protocol-choice rationale that made App Server the stable platform surface underneath every Codex client.
- **Image inventory:** 0 total; 0 useful (text-only).
- **Action taken:** converted to TXT, deleted mhtml
- **Prior processing:** primary source in report 18 (App Server anchor) — quoted via `newton20/harness-engineering-kb` mirror because canonical URL was Cloudflare-blocked; first canonical fetch.
- **Recommendation:** incorporate into report 18 as primary-fetch upgrade — replace 🟡 mirror provenance with ✅; re-verify five-surface enumeration and Thread/Turn/Item primitive definitions; update blocked-urls.md.

---

### Cluster G — Replit Docs (deleted — all primary in report 20)

All eight Replit Docs pages and the warehouse-connectors page **were already primary-anchored in report 20 (R-* rows, ✅ FULL via issue #41)**. Per-page tag block:

| Filename (mhtml deleted) | URL | Primary anchor in report 20 |
|---|---|---|
| `Replit Docs.mhtml` | https://docs.replit.com/core-concepts/agent | R-Agent |
| `Replit Docs agents and automations.mhtml` | https://docs.replit.com/core-concepts/agent/agents-and-automations | R-A&A |
| `Replit Docs app testing.mhtml` | https://docs.replit.com/core-concepts/agent/app-testing | R-AppTest |
| `Replit Docs autoscale deployments.mhtml` | https://docs.replit.com/cloud-services/deployments/autoscale-deployments | R-Deploy |
| `Replit Docs canvas.mhtml` | https://docs.replit.com/replitai/canvas | R-Canvas |
| `Replit Docs mcp servers.mhtml` | https://docs.replit.com/replitai/mcp/overview | R-MCP |
| `Replit Docs plan mode.mhtml` | https://docs.replit.com/core-concepts/agent/plan-mode | R-Plan (upstream for the "80% plan-mode" claim in followup/03-cherny-interview) |
| `Replit Docs replitmd.mhtml` | https://docs.replit.com/core-concepts/agent/replit-dot-md | R-MD (refutes "100-line auto-condensation") |
| `Replit Docs warehouse connectors .mhtml` | https://docs.replit.com/connectors/warehouses/overview | R-Warehouse |
| `Replit — Introducing Connectors.mhtml` | https://blog.replit.com/connectors | R-Connectors (Connectors ≠ MCP refutation) |

**Themes (all):** 6, 3 (with subset hitting 1, 7).
**Action taken:** all 10 deleted (already drained into report 20).
**Recommendation:** skip — already covered.

---

### Cluster H — Replit blog product launches

#### Replit — Introducing Agent 3_ Our Most Autonomous Agent Yet.mhtml *(deleted — duplicate, but with new finding)*
- **URL:** https://blog.replit.com/introducing-agent-3-our-most-autonomous-agent-yet
- **Themes:** 6, 7, 3
- **Summary:** Sep 10 2025 launch of Agent 3 — "10x more autonomous", proprietary browser-testing claimed 3x faster / 10x more cost-effective than Computer Use models, up to **200-minute autonomous runs** (Max-Autonomy Beta), and the first version that can **build other agents and automations** from natural language.
- **Image inventory:** 12 total; **1 useful** — the "Automation testing environment" Playground screenshot (134 KB) where the bottom-right corner reads **"Powered by Mastra"**, directly substrate-confirming.
- **Action taken:** deleted (already drained into report 20 as R-A3)
- **Prior processing:** primary source in report 20 (200-min autonomy, Max-Autonomy-Beta, Connectors UI flow, agents-build-agents).
- **Recommendation:** **incorporate into report 20-replit-agent as Mastra-substrate confirmation** — this single Playground screenshot reads "Powered by Mastra" and directly **refutes** the report's current §followup-questions caveat that "Mastra usage in Agent 3/4 ... Official docs are silent; status: third-party-only". First-party visual confirmation. Worth a small primary-source upgrade pass. (The screenshot has been preserved in the mhtml capture before deletion via the user's local backup if needed — alternatively re-fetch from blog.replit.com.)

#### Replit — Introducing Replit Agent 4_ Built for Creativity _ Blog.mhtml *(deleted — duplicate)*
- **URL:** https://blog.replit.com/introducing-agent-4-built-for-creativity
- **Themes:** 6, 7, 2
- **Summary:** Mar 11 2026 launch of Agent 4 — three pillars (Creative Expression, Creative Execution, Creative Collaboration). Parallel task execution via **sub-agents within a single project** (Pro/Enterprise, temporarily Core); "Ship Anything" extends a project to web/mobile/slide-deck/data-app/animation outputs sharing one backend.
- **Image inventory:** 17 total; 0 useful — all large images are Wistia video stills + decorative.
- **Action taken:** deleted (already drained into report 20 as R-A4)
- **Prior processing:** primary source in report 20 (sub-agents refutation, Pro/Enterprise gating, "Ship Anything" multi-output quote).
- **Recommendation:** skip — already covered.

#### Replit — Introducing Replit App Monitoring.mhtml *(kept)*
- **URL:** https://blog.replit.com/app-monitoring
- **Type:** mhtml
- **Themes:** 6, 3, 5
- **Summary:** Apr 29 2026 launch of Replit App Monitoring: email alerts on downtime, at-a-glance uptime in publishing view, "Investigate downtime with Agent" button that hands a background task to Agent with read-only production-log + read-only production-DB access to diagnose root cause (app bug vs. misbehaving query vs. integration error). Frames Replit as moving past build-only into "built, launched, and looked after."
- **Image inventory:** 15 total; **1 useful** — the in-product Agent chat screenshot ("Can you look through my production database and inform me of why customers are struggling..." → Agent responds with "Loaded **database skill**", "Analyzing production database schema"); plus an adjacent UI capture showing a downtime-investigation chat with bulleted recent outage windows.
- **Action taken:** kept mhtml (useful images preserved)
- **Prior processing:** not found.
- **Recommendation:** incorporate into report 20-replit-agent as substrate-extension into post-deploy observability — Replit Agent now has first-party tooling to read prod logs + read-only prod DB, closing the "done = live URL" loop with a runtime probe path. Also note the "Loaded database skill" UI string — direct evidence that Replit's connector/tool surfaces are exposed as "skills" inside the Agent loop, which report 20 currently only infers.

---

### Cluster I — Sam Schillace (Sunday Letters Substack)

#### Artisans and Factory Lines - by Sam Schillace.mhtml *(kept)*
- **URL:** https://sundaylettersfromsam.substack.com/p/artisans-and-factory-lines
- **Type:** mhtml
- **Themes:** 6, 3
- **Summary:** Schillace argues senior engineers reflexively try to "wrap" LLMs in deterministic code to escape stochasticity — a "tempting wrong hybrid" — and that code should retreat from doing cognitive work to instead shape meta-cognitive scaffolding (control, memory, orchestration, evaluation); the factory analogy is that you cannot drop an artisan into the middle of a production line. Sets up a "Recipe for the Semantic Era" with five ingredients (syntactic code, determinism, semantic reasoning, stochastic behavior, meta-cognitive code) and a four-step method.
- **Image inventory:** 4 total; **1 useful** — richly detailed hand-drawn "Recipe for Building in the Semantic Era" diagram (1448×1086) showing the old syntactic factory vs. the new semantic foundry, the "tempting wrong hybrid" of patch-wrapping the LLM, five labelled ingredients, and a four-step method panel.
- **Action taken:** kept mhtml (useful images preserved)
- **Prior processing:** not found.
- **Recommendation:** incorporate into report 09-jaymin-book-harnesses-practices-mental-models as the "meta-cognitive code" framing — same-model-different-harness articulated as artisan/factory-line metaphor; the recipe diagram is corpus-grade illustration.

#### AI and the marshmallow test - by Sam Schillace.txt
- **URL:** https://sundaylettersfromsam.substack.com/p/ai-and-the-marshmallow-test
- **Type:** converted-txt
- **Themes:** 1, 6
- **Summary:** Schillace names a new tech-debt species created by agentic harnesses — code that is functionally/syntactically correct and even well-organized, but poorly thought-out because the human kicked off the agent without disciplining intent; the model later cannot debug what it built because the spec was under-defined. Prescription: use the model itself to pressure-test the plan and have it ask clarifying questions before any code runs.
- **Image inventory:** N/A (now txt) — Sub-agent reviewed images and found none informative.
- **Action taken:** converted to TXT, deleted mhtml
- **Prior processing:** not found.
- **Recommendation:** incorporate into report 26-prompt-underspecification-academic as a practitioner-voice anchor for the "spec → code gap" failure mode (F36/F37 family) — Schillace's "modern marshmallow test" is the popular-press name for the effect Yang et al. and Larbi et al. measure quantitatively.

#### Attention and collaboration in the AI world.txt
- **URL:** https://sundaylettersfromsam.substack.com/p/attention-and-collaboration-in-the
- **Type:** converted-txt
- **Themes:** 1, 7
- **Summary:** Field observation across valley teams using Claude Code / Amplifier — productive agentic teams stay at ≤3 humans because each human is already saturated managing 5–10 concurrent agents; a 3-person team "feels like a 30-person team." Argues human attention is the binding constraint on collaboration, predicts Jevon's paradox on attention-management tools, and calls for modular org/process design plus norms for centering/de-centering the tool in meetings.
- **Image inventory:** N/A (now txt).
- **Action taken:** converted to TXT, deleted mhtml
- **Prior processing:** not found.
- **Recommendation:** **new report — `schillace-attention-economy`** — co-anchor with "Attention is all ya got" and "The one scarce resource AI can't replace"; the corpus' Theme-1 (3-tier summary discipline, batched human review) currently lacks a Schillace-voice primary anchor.

#### Attention is all ya got - by Sam Schillace - Sunday Letters.txt
- **URL:** https://sundaylettersfromsam.substack.com/p/attention-is-all-ya-got
- **Type:** converted-txt
- **Themes:** 1, 6
- **Summary:** Names the metric "output per unit of human attention" and frames AI use as financial compounding: Warren-Buffet users invest attention in tools that build more tools (compounding leverage); working-stiff users spend attention task-by-task; lottery-winner users use AI to make more work for themselves (attentional bankruptcy). Cites a Harvard study showing agentic coding can *increase* workload; warns of an "always smart/productive" expectation analogous to "always on"; calls compounding the load-bearing discipline.
- **Image inventory:** N/A (now txt).
- **Action taken:** converted to TXT, deleted mhtml
- **Prior processing:** not found.
- **Recommendation:** new report — `schillace-attention-economy` — co-anchor; "output per unit of human attention" is the explicit economic statement of the corpus' Theme-1 scarcity argument.

#### How it will happen - by Sam Schillace - Sunday Letters.txt
- **URL:** https://sundaylettersfromsam.substack.com/p/how-it-will-happen
- **Type:** converted-txt
- **Themes:** 6, 1
- **Summary:** Schillace argues code crossed a tipping point in 2025 where models, longer-horizon reasoning, and self-improving scaffolding (Claude Code / Codex) became strongly net-positive, producing "advanced teams that don't read code at all" with no near-term token ceiling — the binding constraint is now human attention, and the same curve (curiosity → hobby → early adopter → mandatory) is about to repeat across other knowledge-work domains via "meta-orchestration" tools that increase machine work per unit of attention.
- **Image inventory:** N/A (now txt) — only image >30 KB was a decorative AI brain/cityscape illustration.
- **Action taken:** converted to TXT, deleted mhtml
- **Prior processing:** not found.
- **Recommendation:** new report — `schillace-attention-economy` (or super-report `schillace-sunday-letters`).

#### I have seen the compounding teams - by Sam Schillace.txt
- **URL:** https://sundaylettersfromsam.substack.com/p/i-have-seen-the-compounding-teams
- **Type:** converted-txt
- **Themes:** 7, 6, 4
- **Summary:** First-hand sightings of 2–3 "compounding" teams that don't write code at all but instead wrap a model in a custom Amplifier-style framework with callback hooks, tool calling, and flow control, relying heavily on filesystem/git/markdown/kubernetes/xml as substrate; compounding comes from a recursive "build a tool for making a tool" mindset where the system writes and commits its own tools — leading to 5–10 parallel processes, hundreds of dollars/day API spend, and code review treated as "a firing offense" because human attention is the bottleneck.
- **Image inventory:** N/A (now txt) — all images <3 KB.
- **Action taken:** converted to TXT, deleted mhtml
- **Prior processing:** referenced in 01-strongdm-factory as secondary (StrongDM homepage footnote 1 mention only — not drained).
- **Recommendation:** new report — `schillace-sunday-letters` — primary-anchor Amplifier-style compounding-teams pattern, "code review as firing offense", filesystem/git/markdown as agent-native substrate; directly substantiates theme-7 "agents as team members" and adds a Microsoft-internal data point alongside Anthropic (report 23) and Every (reports 03/04). Cross-link to followup/06 (Amplifier flag).

#### Machine with Concrete - by Sam Schillace - Sunday Letters.txt
- **URL:** https://sundaylettersfromsam.substack.com/p/machine-with-concrete
- **Type:** converted-txt
- **Themes:** 6, 7, 1
- **Summary:** Schillace describes Amplifier's tool surface (architecture experts, "session analyzers", a "dev foundry" that stamps out bespoke "dev machines" running for days/weeks, and a "Crusty Old Engineer" critic) and notes his GitHub went from 0 to 100+ repos but very little ships — the next two priorities are (a) the "last mile" problem (finishing should be as easy as starting; fit/finish and context understanding are still not "agent-shaped") and (b) multi-agent coordination plus team coordination (his 12-person team already has >500 projects). Frame: each technology bottleneck reveals the next; harness problem largely solved, last-mile problem now exposed.
- **Image inventory:** N/A (now txt) — only image >30 KB was decorative AI-illustration.
- **Action taken:** converted to TXT, deleted mhtml
- **Prior processing:** not found.
- **Recommendation:** new report — `schillace-sunday-letters` — primary anchor for the "last-mile" failure-mode candidate (proposed F-mode: starting-is-easy-finishing-is-not) and for Amplifier internals (Dev Foundry, Crusty-Old-Engineer critic role, session-analyzer reflective loop).

#### The agent-shaped world - by Sam Schillace - Sunday Letters.txt
- **URL:** https://sundaylettersfromsam.substack.com/p/the-agent-shaped-world
- **Type:** converted-txt
- **Themes:** 6, 4, 1
- **Summary:** Schillace's "shipping-container" thesis: the people who compound with AI have reshaped their work to give agents "surfaces to grab onto" (iterable data, decomposed observable steps, machine-navigable docs, machine-drivable interfaces, plus recursive self-process audits), exactly analogous to McLean's standardized shipping container — the revolution wasn't the box, it was "what the ship could now assume about the cargo"; the unsettling part is that those left behind don't know it (Borders / newspapers analogy) because the scoreboard hasn't changed yet.
- **Image inventory:** N/A (now txt) — only image >30 KB was decorative AI-illustration.
- **Action taken:** converted to TXT, deleted mhtml
- **Prior processing:** not found.
- **Recommendation:** new report — `schillace-sunday-letters` — primary anchor for the "agent-shaped surfaces" framing (proposed candidate failure mode: non-agent-shaped-workflow). Strong conceptual sibling of report 07 (dark-factory) and the StrongDM Attractor thesis in reports 01/02. Worth cross-linking from report 13 (round-2-synthesis).

#### The hard part isn't doing the work now; it's choosing the work..txt
- **URL:** https://sundaylettersfromsam.substack.com/p/the-hard-part-isnt-doing-the-work
- **Type:** converted-txt
- **Themes:** 1, 6, 7
- **Summary:** Schillace argues the bottleneck in agentic coding has shifted from doing the work to choosing it: coding agents make it trivial to start parallel tasks, so attention saturates fast and the scarce skill becomes picking what to build, judging output, and managing many concurrent agents like a team — with "Why Not / What If" framing for skeptics and an "Internet Stages" analogy for AI maturation timing.
- **Image inventory:** N/A (now txt) — hero image was stylized retro-illustration (decorative).
- **Action taken:** converted to TXT, deleted mhtml
- **Prior processing:** not found.
- **Recommendation:** new report — `schillace-sunday-letters` — primary anchor for theme-1; secondary supplement to followup/06-competitor-landscape (Amplifier author's first-person account).

#### The one scarce resource AI can't replace - by Sam Schillace.txt
- **URL:** https://sundaylettersfromsam.substack.com/p/laundry-lists-and-building-blocks
- **Type:** converted-txt
- **Themes:** 1, 6, 3 ("Attention Firewall" tool)
- **Summary:** Schillace reframes "nothing ships" complaints by distinguishing mass-audience software (books) from transient AI-generated software (shopping lists); since inference cost removes the zero-marginal-cost game and AI removes creation friction, the only durable scarcity is human attention, so the premium is on low-maintenance, agent-friendly building blocks (github, markdown, html, yaml, python, rust, go) and tools like his team's "Attention Firewall" notification filter.
- **Image inventory:** N/A (now txt).
- **Action taken:** converted to TXT, deleted mhtml
- **Prior processing:** not found.
- **Recommendation:** new report — `schillace-sunday-letters` — co-primary anchor for theme-1; specific quotables for INDEX/00-synthesis: "human attention is all you need," the shopping-list-vs-book duality, the agent-OS building-block list, and the "Attention Firewall" pattern (concrete instance of theme-3 automated policy so humans aren't in every loop).

#### What is a harness and why do I care_ - by Sam Schillace.mhtml *(kept)*
- **URL:** https://sundaylettersfromsam.substack.com/p/what-is-a-harness-and-why-do-i-care
- **Type:** mhtml
- **Themes:** 6, 2 ("gene transfer"), 4 (Amplifier)
- **Summary:** Schillace's first-person definition of a harness as the orchestration layer around a model — covering Semantic Kernel lineage, Context Query, subagents, containers, recipes (yaml workflows), external memory management, and Microsoft Amplifier's self-improving experts (session analyst, foundation expert, "Crusty Old Engineer"); he names the self-improvement pattern "gene transfer" where a harness ingests another codebase or paper and grafts capabilities into itself, with explicit reference to compounding (harness builds tools that help build the next tools).
- **Image inventory:** 9 total; **1 useful** — high-quality four-panel architecture diagram titled "What Is an AI Harness?" with labelled stages (Start with a model / The harness orchestrates / It manages memory and context / It compounds) plus a "full picture" bottom strip (Models → Tools → Data connectors → Memory systems → Harnesses). Genuine teaching diagram; canonical visual for the harness concept from a non-OpenAI source.
- **Action taken:** kept mhtml (useful images preserved)
- **Prior processing:** not found (Schillace/Amplifier referenced in 01-strongdm-factory and followup/06-competitor-landscape only as a secondary pointer; this specific post is not drained).
- **Recommendation:** incorporate into report 09-jaymin-book-harnesses-practices-mental-models as a non-OpenAI primary anchor for the harness-engineering definition (the four-panel diagram is corpus-canonical), AND supplement to followup/06-competitor-landscape for Microsoft Amplifier ("gene transfer," session analyst, foundation expert, Crusty Old Engineer subagents, yaml "recipes"); secondary cross-link from 18-openai-codex-substrate to contrast with the OpenAI framing.

---

### Cluster J — Stanford Law School / CodeX (governance)

#### AI Life Cycle Core Principles - CodeX - Stanford Law School.txt
- **URL:** https://law.stanford.edu/2023/03/17/ai-life-cycle-core-principles/
- **Type:** converted-txt
- **Themes:** 3, 1
- **Summary:** Eran Kahana's foundational 2023 article enumerates the AI Life Cycle Core Principles (AILCCP) framework as a long table of named principles — Accessibility, Accountability, Accuracy, Bias, Big Data, Consent, Cooperation, Efficiency, Enabling (sandboxing), Equity, Ethics, Explainability (XAI), Fairness, Fidelity, Fundamental Rights, Governance, Human-Centered, Inclusive, Interpretability, Metrics, and more — each mapped to specific ISO standards (ISO/IEC 23053:2022, 42001:2023, 24027:2021, 24368:2022, 31000:2018, etc.) and to cross-referencing principles. Source-of-truth principles enumeration that Kahana's later StrongDM/Cognitive-Escrow articles invoke by name.
- **Image inventory:** 8 total; 0 useful — Stanford site chrome only.
- **Action taken:** converted to TXT, deleted mhtml
- **Prior processing:** not found (AILCCP framework name appears only in Kahana's downstream article cited from followup/10).
- **Recommendation:** supplement to followup/10-governance — anchor the AILCCP principle definitions Kahana invokes (Metrics, Accuracy, Accountability, Workforce Compatible, Trustworthy, Human-Centered) directly to their primary definitions, including ISO cross-references absent from downstream pieces.

#### Built by Agents, Tested by Agents, Trusted by Whom?.mhtml *(deleted — duplicate)*
- **URL:** https://law.stanford.edu/2026/02/08/built-by-agents-tested-by-agents-trusted-by-whom/
- **Themes:** 3, 5, 2
- **Summary:** Kahana reads StrongDM's Software Factory manifesto through the AILCCP framework and concludes its no-human-writes/no-human-reviews architecture inverts software liability assignment; names three concrete gaps (liability, disclosure, contractual), AI-as-judge circularity, the Goodhart-law `return true` failure, and insurance-underwriting inertia.
- **Image inventory:** 8 total; 0 useful — Stanford site chrome only.
- **Action taken:** deleted (already drained into followup/10-governance §1.1 via issue #26)
- **Prior processing:** primary source in followup/10-governance §1.1.
- **Recommendation:** skip — already covered.

#### Cognitive Escrow_ The Human-Centered Principle Has a Blind Spot - CodeX - Stanford Law School.txt
- **URL:** https://law.stanford.edu/2026/03/07/cognitive-escrow-the-human-centered-principle-has-a-blind-spot/
- **Type:** converted-txt
- **Themes:** 3, 1, 6
- **Summary:** Kahana names a previously unnamed phenomenological state — "cognitive escrow," the interval between when a human presses send and when an AI response returns, during which the thought has left the sender's possession but has not returned — and argues the AILCCP Human-Centered principle has a structural blind spot because its three current questions (meaningful oversight, expertise preservation, automation bias) all assume the human is present and engaged, missing this third "between loops" suspension state. Proposes that latency-minimization is the wrong design reflex; systems should instead use the interval as a design site for re-engagement/reflection (triggering the STIR — Stop, Think, Investigate, Research — discipline structurally rather than aspirationally), and calls for adding a fourth question to the Human-Centered principle.
- **Image inventory:** 8 total; 0 useful — Stanford site chrome only.
- **Action taken:** converted to TXT, deleted mhtml
- **Prior processing:** not found.
- **Recommendation:** **new report — `cognitive-escrow-and-harness-as-design-site`** — frame the prompt→response interval as a primary harness-engineering surface (not a latency-minimization target); cross-cut with followup/10-governance (Human-Centered control gap) and report themes on harness engineering and human-attention scarcity. The STIR-as-structural-trigger angle is directly actionable for harness designers and should feed back into any human-in-the-loop oversight rubric.

#### From Principles to Practice_ The 48 Controls That Make Responsible AI Auditable, Defensible, and Real - CodeX - Stanford Law School.txt
- **URL:** https://law.stanford.edu/2026/02/16/from-principles-to-practice-the-48-controls-that-make-responsible-ai-auditable-defensible-and-real/
- **Type:** converted-txt
- **Themes:** 3, 1
- **Summary:** Kahana presents the Controls Table of the AILCCP — 48 actionable controls (e.g., Agent Kill Switch, Rollback and Quarantine, Rate and Scope Limiter, Intervention Audit Trail, Acceptance Threshold Governance, Supply Chain Vetting, Multi-Agent Protocol Security) classified by domain (Security, Technical, Governance, Monitoring, Testing & Assurance, etc.) and function (Preventive, Detective, Directive, Corrective, Compensating, External Benchmarking), each mapped to AILCCP principles. Five practical use cases (regulatory compliance readiness, security threat mitigation, AI incident response planning, board-level risk governance, third-party vendor assessment) mapping controls to EU AI Act / ISO/IEC 42001 obligations.
- **Image inventory:** 8 total; 0 useful — Stanford site chrome only.
- **Action taken:** converted to TXT, deleted mhtml
- **Prior processing:** not found.
- **Recommendation:** incorporate into followup/10-governance.md as a concrete control catalog — Kahana's named-control vocabulary is directly usable as the operational vocabulary the governance follow-up has been groping toward; pairs with report 10-overstory-substrate-audit (F-modes G12/G13/G14) as the named-control side of the same gap.

#### The Ungovernable Machine - CodeX - Stanford Law School.txt
- **URL:** https://law.stanford.edu/2026/03/17/the-ungovernable-machine/
- **Type:** converted-txt
- **Themes:** 3, 2
- **Summary:** Kahana argues boards of companies deploying Recursive Self-Improvement (RSI) — defined as durable self-modification of mechanisms producing intelligence, compounding ability to self-modify, and limited human gating — face Delaware *Caremark*-line duty-of-oversight exposure (Stone v. Ritter, Marchand v. Barnhill, In re McDonald's, In re Boeing, Hughes v. Hu, Teamsters v. Chou, SolarWinds), heightened by California SB 53's Frontier AI Framework reporting and the SEC Investor Advisory Committee's 2025-12-04 AI-disclosure recommendation. Names three RSI failure modes (behavioral drift, self-poisoning, goal subversion) and three AILCCP controls that map to them (Human Approval Gate for Sensitive Actions, sandboxing, immutable logging); the relevant fact pattern reaches mid-market firms (logistics routing agent rewriting its own scheduler) not just frontier labs.
- **Image inventory:** 8 total; 0 useful — Stanford site chrome only.
- **Action taken:** converted to TXT, deleted mhtml
- **Prior processing:** not found.
- **Recommendation:** **new report — `caremark-rsi-board-exposure`** — first primary source we have for board-level fiduciary exposure on agent self-improvement; provides Delaware case-law spine, the SB 53 overlay, and three named AILCCP controls that map to F-modes around drift/collusion. Alternatively major supplement to followup/10-governance alongside the 48-controls piece, but case-law density and RSI-specific scope arguably justify its own report.

#### Turning AI Governance Into Operational Infrastructure - CodeX - Stanford Law School.txt
- **URL:** https://law.stanford.edu/2026/04/05/turning-ai-governance-into-operational-infrastructure/
- **Type:** converted-txt
- **Themes:** 3, 1
- **Summary:** Kahana presents the full AILCCP architecture and the new interactive AILCCP Explorer: 37 principles (across 15 categories, 10 pillars) + 48 controls + 43 international standards (IEEE/ISO/IEC/NIST) + 10 life-cycle phases + 18 identified risks, all wired with 500+ explicit cross-references (187 control-to-principle, 215 standard-to-principle, 84 phase-to-principle, 23 risk-to-standard). Bidirectional traceability (auditor enters via finding, dev team via phase, regulator via risk); ownership built in (Product/UX/Legal/Risk/ML Engineering/Data Science/QA/Security/SRE/Comms named per phase) with concrete per-phase metrics (e.g., Evaluation tracks bias delta and attack success; Operations tracks MTTR, drift alerts/month, SLO attainment); coverage-gap visibility (8 of 37 principles have no mapped standard); the "enabling risk" concept where three Medium-severity transparency/explainability gaps function as force-multipliers for the more severe harms.
- **Image inventory:** 8 total; 0 useful — framework diagrams not embedded in the MHTML capture.
- **Action taken:** converted to TXT, deleted mhtml
- **Prior processing:** not found.
- **Recommendation:** incorporate into followup/10-governance.md as the structural-overview anchor (use alongside "48 Controls" piece) — supplies the 37-principles / 43-standards / 10-phases / 18-risks scaffold and the named per-phase metrics that the followup currently lacks; also useful methodology reference for report 10-overstory-substrate-audit.

---

### Cluster K — Dan Shapiro blog

#### Completion, Chat, Agent, Claw – Dan Shapiro's Blog.mhtml *(kept)*
- **URL:** https://www.danshapiro.com/blog/2026/05/completion-chat-agent-claw/
- **Type:** mhtml
- **Themes:** 2, 3, 7
- **Summary:** Shapiro proposes a successor four-step ladder — Completion → Chat → Agent → Claw — where a "Claw" is an agent with memory, goals, and autonomy that "works without you," learning and acting on your behalf; he recounts shredding his first OpenClaw install via the Lethal Trifecta, then rebuilding responsibly with hand-crafted read/write asymmetries (read anything, but only create drafts; thumbprints on all generated artifacts) and a personal-contacts/Google Docs claw, and announces Glowforge is moving from one claw to a "claw printer" issuing custom claws per coworker/department.
- **Image inventory:** 2 total; **1 useful** — clean four-panel diagram of the Completion / Chat / Agent / Claw progression with subtitle definitions ("Autocompletes", "Completion + responses", "Chat + tools + loop", "Agent + memory + goals + autonomy") and one-line role captions ("Finishes your thought" → "Plans, remembers, and acts autonomously to achieve goals").
- **Action taken:** kept mhtml (useful images preserved)
- **Prior processing:** not found (URL `completion-chat-agent-claw` is uncited; the post is referenced obliquely only via OpenClaw discussions in 05-simon-willison and 06-hn-and-lenny, which predate this May 13 2026 piece).
- **Recommendation:** **new report — `shapiro-completion-chat-agent-claw`** — drain as Shapiro's *successor* taxonomy to the Five Levels (NOT the source of "five levels" framing, which already lives in `followup/01`). A parallel four-stage capability ladder, compositionally defined (chat = stacked completions; agent = chat + tools + loop; claw = agent + memory + goals + autonomy). Key net-new claims: (a) Simon-Willison-credited agent definition "LLMs using tools in a loop"; (b) Allie Miller refactor — memory is the tool, *learning/self-improvement in pursuit of goals* is the impact; (c) the "Teddy Ruxpin / heartbeats and dreaming" framing for proactive initiative; (d) Shapiro's **personal-claw hardening rules** (read-anything-but-only-draft, thumbprint every artifact, "do not give it production scissors") — direct evidence for Theme 3 governance; (e) the **claw-printer / one-claw-per-employee** organizational pattern — direct evidence for Theme 7.

#### You Don't Write the Code. You Don't Read the Code Either. – Dan Shapiro's Blog *(deleted — duplicate)*
- **URL:** https://www.danshapiro.com/blog/2026/02/you-dont-write-the-code/
- **Themes:** 1, 3, 6
- **Summary:** Shapiro's companion post to the Five Levels, distilling the "software factory" into a four-step index card (AI writes the code → you stop reading it → you confront the resulting validation crisis → solving that crisis becomes your job) anchored to StrongDM as the named Level-5 exemplar, plus the CXDB observability layer, the Healer self-repair loop, Jay's two-week digital-twin universe, the "Why am I doing this?" mantra.
- **Image inventory:** 2 total; 0 useful — `follow.it` logo SVG and decorative `wave.webp`.
- **Action taken:** deleted (already drained into followup/01-shapiro-five-levels)
- **Prior processing:** primary source in followup/01.
- **Recommendation:** skip — already covered.

---

### Cluster L — Academic papers (large)

#### SWE-bench_ Can Language Models Resolve Real-World GitHub Issues_ _ Princeton Language and Intelligence.mhtml *(kept)*
- **URL:** https://pli.princeton.edu/blog/2023/swe-bench-can-language-models-resolve-real-world-github-issues
- **Type:** mhtml
- **Themes:** 5, 6
- **Summary:** Princeton PLI blog announcing SWE-bench by Jimenez, Yang, Wettig, Yao, Pei, Press, and Narasimhan: a 2,294-instance benchmark built from Issue-PR pairs across 12 popular Python repos, constructed via a 3-stage pipeline (repo selection + scraping → attribute-based filtering for merged PRs that touch tests → execution-based filtering verifying Fail-to-Pass before/after). State-of-the-art LMs are shown to largely fail at real-codebase issue resolution; the post also releases SWE-Llama 7b/13b fine-tunes and the SWE-bench training dataset.
- **Image inventory:** 10 total; **1 useful** — canonical "nutshell-bench" diagram showing the full SWE-bench loop (Issue + Codebase → Language Model → Generated PR over real sklearn files → Unit Tests scoring 2/5 → 5/5 Fail-to-Pass).
- **Action taken:** kept mhtml (useful images preserved)
- **Prior processing:** referenced in report 22 as secondary — sources table lists this Princeton PLI blog URL with ❌ (Cloudflare-blocked); swebench.com was substituted.
- **Recommendation:** incorporate into report 22-academic-foundations as primary-source upgrade — replace ❌ row with ✅ (mhtml snapshot) and quote the authors' own framing of the 3-stage construction pipeline.

#### The Prompt Report_ A Systematic Survey of Prompt Engineering Techniques.mhtml *(kept)*
- **URL:** https://arxiv.org/html/2406.06608v6
- **Type:** mhtml
- **Themes:** 6, 5, 3
- **Summary:** Schulhoff et al.'s 76-page PRISMA-style meta-analysis distilling 1,565 prompt-engineering papers into a taxonomy of 58 text-based techniques (in-context learning, thought generation, decomposition, ensembling, self-criticism), plus extensions covering multilingual, multimodal, agent (tool-use, code-gen, observation-based, RAG), and LLM-as-judge evaluation prompting; closes with a prompting-issues section on prompt injection / jailbreaking, prompt-sensitivity, sycophancy, bias, and ambiguity, and includes a case study showing prompt-engineering effects are real but brittle (DSPy outperforms hand-crafted CoT).
- **Image inventory:** 15 total; **3 useful** — (a) `eval_strategies.png`: 2x2x2 grid of do/dont exemplar-selection diagrams; (b) `x4.png` (1.34 MB): bar chart of F1/Recall/Precision across 10-Shot AutoDiCoT / 20-Shot AutoDiCoT / DSPy Default / DSPy + Small Modifications, showing DSPy beating hand-crafted prompts; (c) `x3.png`: PRISMA-style screening pipeline (4,797 records → 4,247 after title dedup → 3,985 papers human reviewed → 2,352 after removing papers that don't contain "prompt" → 1,565 records in qualitative synthesis).
- **Action taken:** kept mhtml (useful images preserved)
- **Prior processing:** not found — Schulhoff cited in 06-hn-and-lenny and 05-simon-willison only via Lenny's-newsletter security podcast ("CaMeL endorsement"); arXiv:2406.06608 is not a sources-table anchor anywhere.
- **Recommendation:** **new report — `27-prompt-engineering-survey`** — anchor the harness/eval discussion in 22 and 26 to Schulhoff's 58-technique taxonomy and PRISMA methodology, with hooks for: (a) DSPy + small modifications beats hand-crafted AutoDiCoT (Theme 6, harness optimization surface), (b) §5 Prompting Issues taxonomy of prompt injection / jailbreaking / sycophancy / prompt-drift (Theme 3, guardrails + Theme 2 agent drift), (c) §4.2 LLM-as-judge evaluation prompting catalogue (Theme 5, eval suites). Alternative tighter scope: incorporate into report 26-prompt-underspecification-academic.

---

### Cluster M — "Software factory" voices (other blogs)

#### The Software Factory _ LukePM.com.txt
- **URL:** https://lukepm.com/blog/the-software-factory/
- **Type:** converted-txt
- **Themes:** 2, 7
- **Summary:** A short 2024-12-24 blog post by "luke" sketching a near-future "software factory" of specialized AI agents (AI Business Analyst, AI DevOps, AI QA) collaborating via an "AI compiler" that auto-optimizes generated code, arguing speed/agility will displace code quality and correctness as primary engineering concerns. Definitional and speculative; no benchmarks, no architecture detail, no governance discussion.
- **Image inventory:** 0 total.
- **Action taken:** converted to TXT, deleted mhtml
- **Prior processing:** referenced in 01-strongdm-factory as secondary (homepage footnote-1 attribution noted in `plan-sync.md` as "not in corpus").
- **Recommendation:** low-priority — shallow / definitional. Only durable value is as an attribution anchor for report 01's footnote-1 chain. Optionally incorporate into report 01 as a one-paragraph attribution-provenance note confirming the homepage footnote-1 source.

#### The Software Factory: When No Human Writes or Reviews the Code.mhtml *(deleted — duplicate)*
- **URL:** https://www.thepragmaticcto.com/p/the-software-factory-when-no-human
- **Themes:** 3, 5, 2
- **Summary:** Allan MacGregor's 2026-02-18 piece treats StrongDM's three cardinal rules as the empirical-skepticism counterweight to BCG's structural optimism: praises "scenarios as holdout sets" (agents can't game tests they can't see) and the Digital Twin Universe of Go-binary SaaS clones as "worth stealing / worth studying," but anchors a hard governance refusal in defect-rate data (CodeRabbit Dec-2025: 1.4x critical / 1.7x major issues, 10.83 vs 6.45 issues/PR; Veracode 2025: 45% vulnerable, XSS 86%, SQLi 20%; FormAI: 51.24% of 112k ChatGPT C programs vulnerable) plus named failures (Replit July-2025 production DB wipe; Moltbook Jan-2026 1.5M API-key leak).
- **Image inventory:** 5 total; 0 useful — Substack avatars + header banner all below threshold.
- **Action taken:** deleted (already drained into followup/10-governance §1.3)
- **Prior processing:** primary source in followup/10-governance §1.3 (also cross-referenced from 21-tabnine-enterprise).
- **Recommendation:** skip — already covered.

#### When AI Agents Write Your Code, Does Language Choice Matter?.txt
- **URL:** https://www.thepragmaticcto.com/p/when-ai-agents-write-your-code-does
- **Type:** converted-txt
- **Themes:** 6, 5, 3
- **Summary:** Allan MacGregor's 2026-02-17 piece (paywalled past the cut) reframes Jose Valim's "Why Elixir is the best language for AI" (Feb 5 post; Tencent benchmark — Elixir 97.5% completion rate across 20 languages; Claude Opus 4 80.3% Elixir vs 74.9% C# vs 72.5% Kotlin) as a structural claim about the *compiler-as-AI-code-reviewer*: typed/functional languages (Scala, Haskell, Rust, Elixir) tighten the LLM feedback loop because the type system rejects invalid code before it reaches a human, and stateless / immutable / pure-function code matches LLMs' tokenized, context-window-bounded operational model — citing Alexandru Nedelcu on Scala-3 macros via LSP and Jonathan de Montalembert ("the more flexible and forgiving the target language, the more dangerous the AI partner becomes"). Free portion ends at "The Training Data Problem" cliffhanger — Berra epigraph signaling MacGregor will counter-argue that ecosystem-churn and training-data abundance dominate in practice.
- **Image inventory:** 4 total; 0 useful — author avatars + banner below threshold.
- **Action taken:** converted to TXT, deleted mhtml
- **Prior processing:** not found.
- **Recommendation:** **new report — `language-choice-as-harness`** — frames programming-language selection as a first-class harness-engineering decision (compiler-as-AI-reviewer, FP-fit-with-LLM-architecture, ecosystem-churn-as-training-data-problem). Alternatives: incorporate into report 23-anthropic-engineering-trilogy as a "language substrate" extension to the harness chapter, or supplement to followup/07-evals-deepdive for the Tencent multi-language benchmark — but the article opens a distinct vertical (substrate-language choice) not currently covered. Note: a full drain will require fetching the paywalled tail via fetch-blocked-urls.

---

### Cluster N — TXT-format Lenny / Every / Notion / Sendbird sources

#### Head of Claude Code What happens after coding is solved Boris Cherny.txt *(deleted — duplicate)*
- **URL:** https://www.lennysnewsletter.com/p/head-of-claude-code-what-happens (YouTube: https://youtu.be/We7BZVKbCVw)
- **Themes:** 2, 6, 7
- **Summary:** Full ~90-min Lenny × Boris Cherny interview transcript: "100% of my code is written by Claude Code since November", 10–30 PRs/day, five-agents-steady-state with 1/3 terminal / 1/3 desktop / 1/3 iOS split ("multi-cladding"), Sonnet 3.5 ~15–30s vs Opus 4.6 ~10–30min unattended runtime, Cowork 10-day build, race-to-the-top open-source-sandbox principle.
- **Action taken:** deleted (already drained into followup/03-cherny-interview)
- **Prior processing:** primary source in followup/03 (✅ FULL primary-source-anchored as of 2026-05-14; canonical copy at `reference-only/lenny-podcast-transcripts/cherny-head-of-claude-code-full.txt`).
- **Recommendation:** skip — already covered.

#### How Every Is Harnessing the World-c.txt *(deleted — duplicate)*
- **URL:** https://every.to/chain-of-thought/how-every-is-harnessing-the-world-changing-shift-of-opus-4-5
- **Themes:** 6, 7, 2
- **Summary:** Katie Parrott's Dec 9 2025 write-up of Every's Opus 4.5 Claude Code Camp; core claims: Opus 4.5 is the "infinite coding machine" that doesn't hit the three-step error wall, can fix bugs across dependency layers, enables "10 projects at once" parallel delegation; "your brain is the bottleneck."
- **Action taken:** deleted (already drained into followup/05-klaassen-siblings §3)
- **Prior processing:** primary source in followup/05.
- **Recommendation:** skip — already covered.

#### How I AI CJ Hess on Building Custom.txt
- **URL:** N/A — Claire Vo's "How I AI" newsletter/podcast (CJ Hess at Tenex, Feb 9 2026)
- **Type:** txt
- **Themes:** 6, 7, 5
- **Summary:** Tenex SWE CJ Hess walks through two workflows: (1) Flowy, a custom dev tool he built that takes JSON node/edge definitions and renders interactive flowcharts/UI mockups, invoked via a Claude Code "skill" (`~/.claude/skills/flowy-flowchart/SKILL.md`) and a `kevin` alias for Claude with bypass-permissions; (2) a model-vs-model QC loop where after Claude implements a feature, a `carl` alias invokes GPT-5.2 Codex as a "curmudgeonly staff engineer" to git-diff-review the change for plan-fidelity, code smells, and refactor opportunities, then asks Codex to implement its own suggested fixes.
- **Image inventory:** N/A (txt).
- **Action taken:** txt passthrough
- **Prior processing:** not found (CJ Hess / Flowy / Tenex / Claire Vo / "How I AI" / `kevin`/`carl` aliases all return zero hits).
- **Recommendation:** incorporate into report 23-anthropic-engineering-trilogy or report 12-adjacent-ecosystem as "bespoke dev-tool authoring (Flowy) + two-model QC loop" — strong evidence for theme-6 (per-engineer custom skills are becoming a primary optimization surface) and theme-7 (model-vs-model review as a structural team pattern, distinct from Cherny's "Claude reviews 100% of Anthropic PRs" because the reviewer is a *different* model class). Alternative: new short followup `followup/NN-how-i-ai-cj-hess` if the corpus wants a "personal-harness-stack case study" anchor.

#### Quests token leaderboards and a s.txt
- **URL:** N/A — Lenny's Newsletter "How I AI" episode (John Kim, Sendbird CEO); companion blog at https://www.chatprd.ai/how-i-ai/john-kims-playbook-for-ai-transformation
- **Type:** txt
- **Themes:** 7, 1, 5 ("AI Gods" tier measurement)
- **Summary:** Sendbird CEO John Kim describes his "Automators" platform — a gamified internal marketplace where any employee files a "quest" (automation request) tagged with risk level / weeks-saved / beneficiary, engineers or AI agents claim it, completers earn XP redeemable for gift cards or exec time, and per-person daily-token tiers (Beginner < 1M/day → AI God > 100M/day) make AI fluency a visible org-wide leaderboard. Pairs with InfoSec-vetted secure templates for non-engineer builders, weekly cross-functional AI-task-force unblocking, exec-modeled top token usage, and a hiring rewrite optimizing for curiosity / agency / energy over years of experience.
- **Image inventory:** N/A (txt).
- **Action taken:** txt passthrough
- **Prior processing:** not found.
- **Recommendation:** **new report — `sendbird-quests-token-tiers`** — gamified internal AI-adoption marketplace + per-employee token-tier leaderboards as a novel org-design primitive for AI fluency measurement (theme 7 + theme 1); only manual-corpus source that operationalizes "AI Gods" tiering and a quest-marketplace funnel.

#### Stop Coding and Start Planning.txt *(deleted — duplicate)*
- **URL:** https://every.to/chain-of-thought/stop-coding-and-start-planning
- **Themes:** 1, 6, 2
- **Summary:** Klaassen's "planning beats vibe-coding" essay: four-clause plan-prompt template, three fidelity tiers (F1/F2/F3 with "vibe planning" prototype-grid escalation), and the Figma → plan-agent → build → Puppeteer-diff-review-agent chain on Cora's email-bankruptcy feature.
- **Action taken:** deleted (already drained into followup/05-klaassen-siblings §1).
- **Prior processing:** primary source in followup/05 (drained via issue-23 GitHub Action).
- **Recommendation:** skip — already covered.

#### Teach Your AI to Think Like a Senio.txt *(deleted — duplicate)*
- **URL:** https://every.to/chain-of-thought/teach-your-ai-to-think-like-a-senior-engineer
- **Themes:** 6, 2, 7
- **Summary:** Klaassen's strategy-library companion to "Stop Coding": parallel-specialized research agents (Strategy 1 "Reproduce and document" with `@kieran-rails-reviewer` checklist-extension; Strategy 2 "Ground in best practices" with `@agent-best-practices-researcher` and `docs/*.md` local research-cache; Strategy 3 onwards body paywalled in snapshot).
- **Action taken:** deleted (already drained into followup/05; paywall caveat documented).
- **Prior processing:** primary source in followup/05.
- **Recommendation:** skip — already covered.

#### The AI engineering workflow at Noti.txt
- **URL:** N/A — Lenny's Newsletter "How I AI" episode (Ryan Nystrom, Notion); companion blog at https://www.chatprd.ai/how-i-ai/ryan-nystrom-notion-workflows-for-engineering-velocity
- **Type:** txt
- **Themes:** 6 (harness — Boxy + fast-CI), 1 (standup pre-reads, "yap your spec" voice-to-spec), 7 (background agents shipping PRs from Slack/Notion mentions)
- **Summary:** Notion engineering manager Ryan Nystrom describes the team's spec-driven AI workflow: Markdown spec files in-repo are the source of truth (Codex implements + verifies + ships against them, spec version history becomes the changelog); a "Boxy" agent triggered by @mentioning Codex from a Notion task returns a PR with UI verification screenshots and a preview URL in ~20 minutes; CI is being cut to 25% of current time because slow CI is the binding constraint on agent iteration count; "yap your spec" (Whisper transcript → Codex with spec examples → comprehensive technical doc); "you're wrong; defend your argument with evidence" as a sycophancy-breaking prompt pattern; line managers should still write code daily because AI removed the meeting-prep tax.
- **Image inventory:** N/A (txt).
- **Action taken:** txt passthrough
- **Prior processing:** not found (Notion appears in reports 06/20/23/03 in unrelated contexts; Nystrom / Boxy / Notion spec-driven workflow not cited anywhere).
- **Recommendation:** incorporate into report 25-requirements-engineering-foundations as a Notion-internal industrial instance of "models-as-spec / specs-as-source-of-truth" (Strategy 3 from AFIS/INCOSE-FR mapping) — provides empirical anchor for "spec-version-history-as-changelog" pattern and "fast-CI as agent-throughput bottleneck" claim. **Alternative:** new report `lenny-howiai-spec-driven-and-team-ops` (alongside `lenny-howiai-personal-harnesses` for CJ Hess).

#### lenny-build-your-own-ai-developer-tools-with-claude-code.txt
- **URL:** https://www.lennysnewsletter.com/p/this-week-on-how-i-ai-how-to-build
- **Type:** txt
- **Themes:** 6, 4, 1
- **Summary:** CJ Hess (10X) walks Claire Vo through his personal Claude Code "harness": a folder of markdown plans paired with a self-built tool **Flowy** that turns Claude-emitted JSON files into editable wireframe/flowchart mockups, plus a set of Claude Code Skills (`flowy-flowchart`, `flowy-ui-mockup`) that the model invokes to generate and iterate on those JSONs — including a "Ralph loop" self-prompted dev cycle and a workflow where Claude reads Git diffs to write its own retrospectives. Argues Claude Code's edge over Codex/Cursor is harness quality and "intent understanding" rather than raw model intelligence ("I'd honestly argue GPT 5.2 is a smarter model").
- **Image inventory:** N/A (txt).
- **Action taken:** txt passthrough
- **Prior processing:** not found (distinct How I AI episode; no overlap with the drained Cherny / Willison transcripts).
- **Recommendation:** **new report — `lenny-howiai-personal-harnesses`** — personal-harness ecosystems (Flowy + Skills + Ralph loops) as the "harness engineering" practitioner anchor, with cross-references into 06-hn-and-lenny, 04-every-skill-libraries, and followup/02-attractor-implementations.

#### lenny-spec-driven-development.txt
- **URL:** https://www.lennysnewsletter.com/p/spec-driven-development-the-ai-engineering
- **Type:** txt
- **Themes:** 7, 6, 1
- **Summary:** Ryan Nystrom (engineering manager at Notion, ex-iOS, leading "Project Afterburner" to cut CI time to a quarter) demonstrates a Notion-AI custom agent that compiles a daily standup pre-read by scraping the last 24 h of Slack, closed Notion tasks, merged PRs, and yesterday's meeting transcript — so meetings become decision/finding exchanges rather than round-robin status. Then shows **Boxy**, Notion's internal VM-based background agent, and a workflow where engineers `@codex` Notion comments to dispatch fixes, plus his spec-driven habit of opening Whisper, yapping a feature into a markdown doc, asking Codex to "write a spec" and then a second Codex run to "build it" — one-shotting features without code, meetings, or design review. Frames it as a win-win-win against the classic "pick two" of speed/quality/cost.
- **Image inventory:** N/A (txt).
- **Action taken:** txt passthrough
- **Prior processing:** not found (distinct How I AI episode).
- **Recommendation:** **new report — `lenny-howiai-spec-driven-and-team-ops`** — Boxy + standup pre-read agent + Whisper→spec→Codex one-shot loop as practitioner anchors for Theme 7 (agents as team members) and Theme 1 (human attention as scarce); cross-link to 14-el-kaim-book-intent-and-spec-authorship, 03-every-compound-engineering, and followup/03-cherny-interview.

---

### Cluster O — PDF

#### Neves-Bussmann.pdf
- **Title:** Smart Agent-Based Modelling with LLMs: Leveraging Large Language Models for a Better Understanding of Algorithmic Collusion
- **URL:** Stanford Computational Antitrust, Vol. 6 (2026); authors at CADE / Cerebro Project, Brazil (no DOI on first pages; `carlos.neves@cade.gov.br`)
- **Type:** pdf (31 pages, A4, 1.5 MB)
- **Themes:** 2 (drift / **collusion** — direct hit), 5 (SABM as regulatory eval framework), 3 (antitrust policy implications)
- **Summary:** Neves & Bussmann (CADE / Cerebro Project, Brazil) introduce a **Smart Agent-Based Modelling (SABM)** framework — agent-based simulation in which agent behaviors are produced entirely by LLM prompts (the "homo silicus" paradigm of Filippas/Horton/Manning, EC'24) rather than hand-coded rules — and apply it to a Bertrand-duopoly pricing game. They document that LLM-driven agents reach **tacit collusion**, stabilizing prices above competitive levels *without being explicitly instructed to collude*, and that the effect varies with language (English vs Portuguese) and is potentiated by inter-agent communication — including agents *mimicking concerns about collusion* once it's discussed. Positioned as a computational-antitrust tool for regulators.
- **Image inventory:** N/A (pdf; image triage applies only to mhtml per brief).
- **Action taken:** pdf passthrough
- **Prior processing:** not found.
- **Recommendation:** **new report — `academic-llm-agent-collusion`** — SABM / Bertrand-duopoly tacit-collusion evidence as the academic anchor for Theme 2's "collusion among self-organizing agents" failure mode; companion to 22-academic-foundations and 26-prompt-underspecification-academic and a primary source for followup/10-governance (regulatory/antitrust implications when multiple LLM-driven agents coordinate in a shared market or shared codebase).

---

## End notes

- The original raw `manual/` README explicitly states this directory is a "transient drop zone — every file here gets drained into a numbered report by the next `research-pipeline` activation, then deleted per Phase 6." That deletion phase is **not** triggered by this indexing pass — only files already drained in prior rounds were deleted here. The `.mhtml` files kept (7 of them) are explicitly kept because the next agent should see their embedded images before deciding how to drain (e.g., Schillace's four-panel harness diagram, the SWE-bench loop diagram, the Prompt Report PRISMA pipeline, the dotpowers / sprint-exec / build-pong DOT-graph renders, the Replit App Monitoring "Loaded database skill" UI capture, the Agent-3 "Powered by Mastra" Playground screenshot, and the Shapiro Completion → Chat → Agent → Claw four-panel ladder).
- `.claude/skills/research-pipeline/scripts/mhtml_extract.py` was written for this pass and lives under the `research-pipeline` skill. It supports `info` (JSON metadata) / `text` (plain body) / `save-image` (extract Nth embedded image) / `to-txt` (write a clean .txt with TITLE/URL header). The research-pipeline skill documents its use in the filesystem table + Phase 7 MHTML caveat — future drains pick it up automatically.
- The intermediate manifest `research/manual/.manifest.json` and the subagent brief `research/manual/.subagent-brief.md` are hidden files retained for provenance.

