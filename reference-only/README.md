# `/reference-only/` — primary sources we deliberately keep on disk

Sources in this directory have been **fully processed** into the numbered research reports under `research/` but are preserved here so the verbatim citations in those reports remain live and re-quotable. Files here are not "in flight" — they are the historical-record copy of primary material.

## Inventory (2026-05-13)

| Path | Source | Used by | Provenance |
|---|---|---|---|
| `el-kaim-book/` | William El Kaim, *Continuous / Intent-Driven Enterprise Architecture* (draft book, 7 chapters, ~430 KB) | `research/14-el-kaim-book-intent-and-spec-authorship.md`, `research/15-el-kaim-book-bmad-attractor-dark-factory.md`, `research/16-el-kaim-book-council-and-delegation.md`, `research/17-el-kaim-book-codex-and-skill-substrate.md` | User dropped into `research/manual/multi/` 2026-05-11; processed by Round-4 fanout subagents 16-19; moved here 2026-05-13 |
| `chatgpt-deep-research-2026-05-11/` | ChatGPT deep-research one-shot synthesis over the same seed inputs as our Round 5 (report.md + sources.md + README.md) | Round-5 reports 18–23 used this as counterfactual + QC input | User-supplied 2026-05-11; processed in Round 5 (PLAN §13); moved here from `research/external-syntheses/` 2026-05-13 |
| `dark-factory-article.txt` | William El Kaim, *The Dark Factory: How Software Is Learning to Build Itself*, el-kaim.com, Apr 8 2026 (41 KB) | `research/07-dark-factory.md`, `research/followup/01-shapiro-five-levels.md` | User-supplied browser export 2026-05-11; deleted post-drain on 2026-05-11; restored from git history 2026-05-13 because report 07 leans heavily on verbatim quotes from it |
| `brier-culture-of-ai-engineering.txt` | Noah Brier, *Culture of AI Engineering*, every.to, 2026-05-08 (19 KB) | Drained on a side branch into `research/followup/12-brier-pace-layers.md` — **note: that drain commit has NOT yet reached `main`**; see PLAN.md §15 bottleneck #1 | User-supplied 2026-05-11; restored from git history 2026-05-13 |
| `every-my-ai-had-already-fixed.txt` | Kieran Klaassen, *My AI Had Already Fixed the Code Before I Saw It*, every.to (14 KB) | `research/03-every-compound-engineering.md` | User-supplied browser-cookie fetch 2026-05-11; deleted post-drain; restored from git history 2026-05-13 |

## What does NOT belong here

- `research/manual/` — transient drop zone for unfinished work. See its README.
- `research/fetched/` — auto-cleaned by drain commits.
- Anything not yet incorporated into a numbered report. Run the `research-pipeline` skill's Phase 0 first.
