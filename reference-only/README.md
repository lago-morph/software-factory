# `/reference-only/` — primary sources we deliberately keep on disk

Sources in this directory have been **fully processed** into the numbered research reports under `research/` but are preserved here so the verbatim citations in those reports remain live and re-quotable. Files here are not "in flight" — they are the historical-record copy of primary material.

## Organisation

As of 2026-05-16, sources are grouped into **subject-matter** subdirectories. Categories are sized to anticipate the eventual restored corpus (~180–220 unique sources surveyed in `category-survey.md`), targeting the plan's ~5–15 sources-per-category rule once restoration completes.

15 categories are reserved (listed in the Categories section below). Only the **9** that currently hold sources have on-disk directories; the **6** empty categories will be created at restoration time. Step-1 categorisation is explicitly **interim**: final categorisation happens in a later step after the restored corpus is in place.

## Categories

| Short-name | Definition | Has sources now? |
|---|---|---|
| `dark-factory` | Shapiro / El Kaim Dark-Factory canon — the foundational essays and frameworks on AI-built software as a paradigm. | ✓ |
| `intent-driven-architecture` | Intent-driven / continuous enterprise architecture, RISE-style automation, software product-line variability. | ✓ |
| `spec-authorship` | Requirements engineering, BMAD, scenario testing, INCOSE primer, spec-as-prompt practice. | (empty, restored later) |
| `willison-canon` | Simon Willison's collected writings + interviews. Treated as its own subject because of dominance and breadth (≥23 essays + the SOTU transcript). | ✓ |
| `compound-engineering` | Compound-engineering workflows, personal harnesses, lived-experience practitioner accounts (Klaassen, Reed, Vincent, *How I AI*). | ✓ |
| `anthropic-substrate` | Claude Code substrate, Anthropic engineering posts on infrastructure, Cherny / Anthropic interviews. | ✓ |
| `openai-substrate` | Codex substrate, OpenAI cookbook, running-codex-safely docs. | (empty, restored later) |
| `other-vendor-substrate` | GitHub Copilot cloud-agent, Replit Agent, Google Gemini CLI, Notion, Every.to harnesses, StrongDM. | (empty, restored later) |
| `skills-composition` | Skills as a composition primitive — agentskills.io, Anthropic Agent Skills docs + cookbooks, El Kaim codex/skill substrate, MCP protocol. | ✓ |
| `evals-and-benchmarks` | SWE-bench, SWE-agent, AlphaCode, CodeGen, evals primers (Husain, Shankar), prompt-engineering survey. | (empty, restored later) |
| `academic-foundations` | Academic methodology papers: underspecification, multi-task program benchmark, CHI/ICSE/ESEC studies. | (empty, restored later) |
| `security-primitives` | Threat models, prompt-injection defenses, capability/data-flow security (CaMeL, AgentDojo). | ✓ |
| `governance-and-legal` | SOX/GDPR audit, Caremark / RSI board exposure, NHTSA levels, AUTOSAR, ISO 42010. | (empty, restored later) |
| `ai-engineering-culture` | Team-level dynamics, organisational culture, the social/operational side of AI engineering. | ✓ |
| `meta-synthesis` | Derived syntheses over the corpus (counterfactual deep-research outputs, QC re-reads). | ✓ |

## Inventory (2026-05-16)

| Path | Source | Used by | Provenance | Category | Why this category |
|---|---|---|---|---|---|
| `dark-factory/dark-factory-article.txt` | William El Kaim, *The Dark Factory: How Software Is Learning to Build Itself*, el-kaim.com, Apr 8 2026 (41 KB) | `research/07-dark-factory.md`, `research/followup/01-shapiro-five-levels.md` | User-supplied browser export 2026-05-11; deleted post-drain on 2026-05-11; restored from git history 2026-05-13 because report 07 leans heavily on verbatim quotes from it | `dark-factory` | obvious — the canonical Dark Factory essay |
| `intent-driven-architecture/el-kaim-book/` | William El Kaim, *Continuous / Intent-Driven Enterprise Architecture* (draft book, 9 chapters on disk, ~430 KB) | `research/14-el-kaim-book-intent-and-spec-authorship.md`, `research/15-el-kaim-book-bmad-attractor-dark-factory.md`, `research/16-el-kaim-book-council-and-delegation.md`, `research/17-el-kaim-book-codex-and-skill-substrate.md`, `research/24-el-kaim-book-product-line-variability.md` | User dropped into `research/manual/multi/` 2026-05-11; processed by Round-4 fanout subagents 16-19; moved here 2026-05-13 | `intent-driven-architecture` | the book's spine is intent-driven EA + product-line variability; alternatives considered: `dark-factory` (rejected — the dark-factory framing is only one chapter; the architecture/intent thread runs through all 9) |
| `willison-canon/willison-ai-state-of-the-union-full.txt` | Simon Willison, *An AI State of the Union* — full ~90-min Lenny Rachitsky transcript (2,155 lines, ~111 KB) | `research/05-simon-willison.md`, `research/06-hn-and-lenny.md` | Transcribed overnight + dropped 2026-05-13; drained 2026-05-13 | `willison-canon` | obvious — Willison's flagship state-of-the-union talk |
| `compound-engineering/every-my-ai-had-already-fixed.txt` | Kieran Klaassen, *My AI Had Already Fixed the Code Before I Saw It*, every.to (14 KB) | `research/03-every-compound-engineering.md` | User-supplied browser-cookie fetch 2026-05-11; deleted post-drain; restored from git history 2026-05-13 | `compound-engineering` | obvious — defines the compound-engineering pattern |
| `anthropic-substrate/cherny-claude-code-interview/` | Boris Cherny (head of Claude Code, Anthropic) on Lenny Rachitsky's podcast — first 30 min (drained) + full transcript (overnight); split out of the original lenny-podcast-transcripts collection on 2026-05-16 | `research/followup/03-cherny-interview.md` | First-30-min drained 2026-05-13; full transcript on disk as of 2026-05-13 | `anthropic-substrate` | content is specifically about Claude Code substrate (sub-agents, sandbox model, Cowork) |
| `skills-composition/anthropic-agent-skills/` | Anthropic Agent Skills — official platform docs page, support.claude.com explainer, and 3 cookbook notebooks (skills intro, financial apps, custom development) | `research/23-anthropic-engineering-trilogy.md` | Path B export 2026-05-13 of `platform.claude.com/docs/en/agents-and-tools/agent-skills/overview` (JS-rendered SPA the fetch action couldn't retrieve); cookbook notebooks pulled the same day | `skills-composition` | the content is about Skills as a composition primitive; alternative considered: `anthropic-substrate` (rejected — Anthropic-published but the subject is the primitive, not the substrate) |
| `security-primitives/camel-paper/` | Debenedetti et al., *Defeating Prompt Injections by Design* (CaMeL), arXiv 2503.18813 — LaTeX source (`main.tex`, `defns.tex`, `main.bbl`) | `research/followup/08-security-primitives.md` | Retrieved 2026-05-13 from `arxiv.org/e-print/2503.18813` via fetch-urls issue #42 because `/html/` returns 404 and `/pdf/` was unextractable; manually `gunzip \| tar -xf`'d to recover the LaTeX | `security-primitives` | obvious — prompt-injection defense by design |
| `ai-engineering-culture/brier-culture-of-ai-engineering.txt` | Noah Brier, *Culture of AI Engineering*, every.to, 2026-05-08 (19 KB) | Drained on a side branch into `research/followup/12-brier-pace-layers.md` — **note: that drain commit has NOT yet reached `main`**; see PLAN.md §15 bottleneck #1 | User-supplied 2026-05-11; restored from git history 2026-05-13 | `ai-engineering-culture` | obvious — the title is literal |
| `meta-synthesis/chatgpt-deep-research-2026-05-11/` | ChatGPT deep-research one-shot synthesis over the same seed inputs as our Round 5 (report.md + sources.md + README.md) | Round-5 reports 18–23 used this as counterfactual + QC input | User-supplied 2026-05-11; processed in Round 5 (PLAN §13); moved here from `research/external-syntheses/` 2026-05-13 | `meta-synthesis` | derived synthesis, not primary; alternative considered: `skills-composition` (rejected — it's a ChatGPT product output but its role here is counterfactual synthesis) |

## Note on the lenny-podcast-transcripts split

The original `lenny-podcast-transcripts/` directory bundled Boris Cherny's Claude Code interview with Simon Willison's *AI State of the Union*. Under the medium-based first pass and the 6-category subject-matter second pass, the directory stayed intact under a single home (`practitioner-harnesses`). Under the 15-category sizing-aligned taxonomy here, the two transcripts now live in their natural subject homes:

- `willison-canon/willison-ai-state-of-the-union-full.txt`
- `anthropic-substrate/cherny-claude-code-interview/` (with the two Cherny files + a new local README).

The original collection-level README was distributed: Willison provenance into this inventory row; Cherny provenance into the new local README under `anthropic-substrate/cherny-claude-code-interview/`.

## What does NOT belong here

- `research/manual/` — transient drop zone for unfinished work. See its README.
- `research/fetched/` — auto-cleaned by drain commits.
- Anything not yet incorporated into a numbered report. Run the `research-pipeline` skill's Phase 0 first.
