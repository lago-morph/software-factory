# CaMeL paper — LaTeX source

LaTeX source for *"Defeating Prompt Injections by Design"* (arXiv 2503.18813), the Google DeepMind / ETH Zürich paper that introduces CaMeL.

- **Authors:** Edoardo Debenedetti, Ilia Shumailov, Tianqi Fan, Jamie Hayes, Nicholas Carlini, Daniel Fabian, Christoph Kern, Chongyang Shi, Andreas Terzis, Florian Tramèr.
- **DOI:** `10.48550/arXiv.2503.18813`
- **License:** CC-BY-4.0
- **Retrieved:** 2026-05-13 from `https://arxiv.org/e-print/2503.18813` via fetch-urls issue #42.

## Why these files exist

Per `research/blocked-urls-round-7.md` (Lesson R7.2), the canonical `arxiv.org/html/2503.18813v{1,2}` render returns 404 and the `arxiv.org/pdf/` route returns a binary PDF that `html2text` cannot extract. The `/e-print/` route returns a gzipped tarball of the LaTeX source — recoverable, but the fetch action's `html2text` extractor produced 4.6 MB of binary noise instead of text. The orchestrator manually `gunzip | tar -xf`'d the archive on 2026-05-13 and saved the relevant `.tex` and `.bbl` files here.

## Files

- **`main.tex`** — 889 lines, the paper body.
- **`defns.tex`** — 558 lines, macro definitions used by `main.tex` (helpful for resolving custom commands).
- **`main.bbl`** — bibliography in BibTeX-rendered form (resolves `\cite{...}` references).

## Drain target

`research/followup/08-security-primitives.md` — the existing section on CaMeL is anchored on the arXiv abstract + Willison's writeup. With `main.tex` now available, the formal threat model, the capability/data-flow semantics, and the AgentDojo evaluation tables can be primary-source-anchored.

The orchestrator dispatched a subagent on 2026-05-13 to do this drain; check that report's "Drain note" for the outcome.
