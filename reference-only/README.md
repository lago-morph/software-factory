# `/reference-only/` — primary sources we deliberately keep on disk

Sources in this directory have been **fully processed** into the numbered research reports under `research/` but are preserved here so the verbatim citations in those reports remain live and re-quotable. Files here are not "in flight" — they are the historical-record copy of primary material.

## Organisation

As of 2026-05-16, sources are grouped into category subdirectories (interim — see `reorg-plan.md`). Categories were chosen to anticipate the eventual restored corpus shape surveyed in `category-survey.md`. Each row below lists where the source now lives plus the category it was placed in.

## Inventory (2026-05-16)

| Path | Source | Used by | Provenance | Category | Why this category |
|---|---|---|---|---|---|
| `books/el-kaim-book/` | William El Kaim, *Continuous / Intent-Driven Enterprise Architecture* (draft book, 9 chapters on disk, ~430 KB) | `research/14-el-kaim-book-intent-and-spec-authorship.md`, `research/15-el-kaim-book-bmad-attractor-dark-factory.md`, `research/16-el-kaim-book-council-and-delegation.md`, `research/17-el-kaim-book-codex-and-skill-substrate.md`, `research/24-el-kaim-book-product-line-variability.md` | User dropped into `research/manual/multi/` 2026-05-11; processed by Round-4 fanout subagents 16-19; moved here 2026-05-13 | `books` | obvious |
| `external-syntheses/chatgpt-deep-research-2026-05-11/` | ChatGPT deep-research one-shot synthesis over the same seed inputs as our Round 5 (report.md + sources.md + README.md) | Round-5 reports 18–23 used this as counterfactual + QC input | User-supplied 2026-05-11; processed in Round 5 (PLAN §13); moved here from `research/external-syntheses/` 2026-05-13 | `external-syntheses` | counterfactual / meta-synthesis, not a primary blog or paper — distinct medium |
| `essays/dark-factory-article.txt` | William El Kaim, *The Dark Factory: How Software Is Learning to Build Itself*, el-kaim.com, Apr 8 2026 (41 KB) | `research/07-dark-factory.md`, `research/followup/01-shapiro-five-levels.md` | User-supplied browser export 2026-05-11; deleted post-drain on 2026-05-11; restored from git history 2026-05-13 because report 07 leans heavily on verbatim quotes from it | `essays` | single-essay primary source; alternatives considered: bundling with `books/el-kaim-book/` (same author) |
| `essays/brier-culture-of-ai-engineering.txt` | Noah Brier, *Culture of AI Engineering*, every.to, 2026-05-08 (19 KB) | Drained on a side branch into `research/followup/12-brier-pace-layers.md` — **note: that drain commit has NOT yet reached `main`**; see PLAN.md §15 bottleneck #1 | User-supplied 2026-05-11; restored from git history 2026-05-13 | `essays` | obvious |
| `essays/every-my-ai-had-already-fixed.txt` | Kieran Klaassen, *My AI Had Already Fixed the Code Before I Saw It*, every.to (14 KB) | `research/03-every-compound-engineering.md` | User-supplied browser-cookie fetch 2026-05-11; deleted post-drain; restored from git history 2026-05-13 | `essays` | obvious |
| `vendor-docs/anthropic-agent-skills/` | Anthropic Agent Skills — official platform docs page, support.claude.com explainer, and 3 cookbook notebooks (skills intro, financial apps, custom development) | `research/23-anthropic-engineering-trilogy.md` | Path B export 2026-05-13 of `platform.claude.com/docs/en/agents-and-tools/agent-skills/overview` (JS-rendered SPA the fetch action couldn't retrieve); cookbook notebooks pulled the same day | `vendor-docs` | obvious |
| `academic-papers/camel-paper/` | Debenedetti et al., *Defeating Prompt Injections by Design* (CaMeL), arXiv 2503.18813 — LaTeX source (`main.tex`, `defns.tex`, `main.bbl`) | `research/followup/08-security-primitives.md` | Retrieved 2026-05-13 from `arxiv.org/e-print/2503.18813` via fetch-urls issue #42 because `/html/` returns 404 and `/pdf/` was unextractable; manually `gunzip \| tar -xf`'d to recover the LaTeX | `academic-papers` | obvious |
| `podcast-transcripts/lenny-podcast-transcripts/` | Two Lenny Rachitsky podcast transcripts: Boris Cherny (head of Claude Code, Feb 19 2026 — first 30 min + full) and Simon Willison ("An AI State of the Union" — full ~90 min) | `research/05-simon-willison.md`, `research/06-hn-and-lenny.md`, `research/followup/03-cherny-interview.md` | Willison full transcript transcribed overnight + dropped 2026-05-13; Cherny first-30-min drained 2026-05-13; Cherny full transcript also now on disk | `podcast-transcripts` | obvious |

## What does NOT belong here

- `research/manual/` — transient drop zone for unfinished work. See its README.
- `research/fetched/` — auto-cleaned by drain commits.
- Anything not yet incorporated into a numbered report. Run the `research-pipeline` skill's Phase 0 first.
