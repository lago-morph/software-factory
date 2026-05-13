# ChatGPT deep-research synthesis — 2026-05-11

A paired artifact preserved verbatim for use as a **counterfactual** and **quality-control input** to our own future cross-round synthesis. **Not a primary source.** Not a substitute for our `research/0N-*.md` reports.

## What's in this directory

| File | Role |
|---|---|
| `report.md` | ChatGPT's deep-research synthesis output. 6 H2 sections covering executive summary, scope/evidence, what current research shows, comparative case studies, layered reference architecture, gap analysis/roadmap. |
| `sources.md` | Verified source register for `report.md`. 26 external sources + 2 user-uploaded sources with canonical URLs, types, relevance notes, and a "Weak or missing citations" QC section. |
| `README.md` | This file. |

## How to read the pair

`report.md` uses ChatGPT's internal citation format (`citeturnXXviewYY`, `fileciteturnZZ`). **Those tokens are not URLs.** They are ChatGPT-conversation-internal turn references and cannot be navigated. To trace any claim back to a source, you must consult `sources.md` — the source register's inventory tables map the report's prose back to canonical URLs.

`sources.md` also references a CSV (`sandbox:/mnt/data/ai_software_factory_sources_2026-05-10.csv`) that lived in ChatGPT's sandbox at generation time. **That CSV was not exported with the markdown files and is not in this repo.** The tables inside `sources.md` are the canonical bibliography here.

## Provenance

- **Generated:** 2026-05-10 / 2026-05-11 (per the access-date stamps inside `sources.md`)
- **Input scope:** ChatGPT was given only two seed files — `spec-driven-ai-dev.md` and `initial-sources.md` from this repo's root. It did **not** see our multi-round `research/01-` through `research/12-` reports. The synthesis therefore represents what an external one-shot deep-research process produces from the same starting inputs we used to begin Round 1.
- **Filing date in this repo:** 2026-05-11

## Why it's preserved (the three uses)

1. **Source harvest.** `sources.md` surfaces six clusters of primary sources our existing reports have not systematically covered. Catalogued for dispatch in `research/PLAN.md` §13.1.
2. **Quality-control checklist.** `sources.md` includes a "Weak or missing citations" section explicitly listing where the deep-research report cited umbrella docs instead of more specific subpages. We should consult that list when writing our own cross-round synthesis to avoid the same compression traps. See `research/PLAN.md` §13.2.
3. **Counterfactual comparison.** When we eventually write our own cross-round synthesis (the still-pending report 13 of Round 2, or any later one), include a deliberate section comparing what this external one-shot synthesis captured versus what our multi-round skill-driven approach captured. Where did each catch things the other missed? See `research/PLAN.md` §13.3.

## What this artifact is *not*

- **Not a primary source.** The underlying citations in `sources.md` are the primary sources. The synthesis prose in `report.md` is an external author's reading of those, not an authority in itself.
- **Not a substitute for our reports.** Our `research/0N-*.md` reports cover the same space with deeper coverage, more verbatim quotes, and a different set of source weights. Where the two disagree, the primary sources decide.
- **Not numbered as `research/13-*.md`.** That slot is reserved for our own Round-2 synthesis (still pending — see `research/PLAN.md` §3.6). Naming this artifact `research/13-…md` would collapse two distinct things into one.

## Filed by

Phase 0 drain of `research/manual/` on 2026-05-11. Original filenames were `software-factory-deep-research-report.md` and `software-factory-deep-research-report-sources.md`. Moved here via `git mv` so the history is preserved.
