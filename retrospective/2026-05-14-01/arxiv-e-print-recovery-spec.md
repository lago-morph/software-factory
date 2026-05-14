# Spec: `arxiv-e-print-recovery`

## Intent

arXiv papers have three text-recoverable routes: `arxiv.org/abs/<id>` (the abstract page, server-rendered HTML), `arxiv.org/html/<id>v<v>` (full HTML render, NOT generated for many recent papers), and `arxiv.org/pdf/<id>` (PDF binary). When the HTML render is missing and the PDF is binary that `html2text` can't read, prior project rounds (notably round-7 R7.2 for the CaMeL paper) accepted the gap. But arXiv also exposes `arxiv.org/e-print/<id>` — the raw LaTeX source as a gzipped tarball. This is the MOST authoritative content (it's literally what the authors wrote), but the fetch action's html2text extractor cannot read it: gzip produces binary noise.

The 2026-05-14 round-8 drain discovered this route works when manually post-processed. The CaMeL paper body, previously documented as "accept the gap; abstract + Willison's writeup are enough," was recovered by `cp → gunzip → tar -xf` against the e-print archive. Result: 889 lines of paper body (`main.tex`), 558 lines of definitions (`defns.tex`), and bibliography. This skill codifies the recovery pattern so future arXiv-paper gaps are not "accepted" until this route is tried.

## Trigger

**Direct triggers:**
- "Recover the arXiv paper body for 2503.18813"
- "Try the e-print route"
- "The PDF is binary; get the LaTeX source"

**Proactive triggers (use without being asked):**
- When `arxiv.org/html/<id>v<v>` returns 404 in a fetch action.
- When `arxiv.org/pdf/<id>` returns HTTP 200 but its `.md` extraction is mostly binary (per `file` reporting "data" or non-ASCII).
- When a fetched arXiv `/e-print/` file is classified `binary_mis_extracted` by the `fetch-action-quality-check` skill.

**Negative triggers (skip):**
- The arXiv `/abs/<id>` page alone is sufficient for the citing report's purposes (the citing report only needs abstract-level claims).
- The paper body is already on disk under `reference-only/<paper-slug>/`.

## Inputs

- An arXiv paper ID (e.g. `2503.18813`).
- Optionally, a path to an already-fetched e-print gzip file (e.g. `research/fetched/issue-<N>/<slug>_arxiv.org__e-print__<id>.html`).
- A target report path that will cite the paper (used for the README header).

## Outputs

- A new `reference-only/<paper-slug>/` directory containing:
  - `main.tex` — the paper body (whichever `.tex` file the paper uses as its main entry — usually named `main.tex`, sometimes `paper.tex` or `<arxiv-id>.tex`).
  - Any other `.tex` files referenced by `main.tex` (typically `defns.tex` for macros, or section files).
  - `main.bbl` (or equivalent) — the bibliography in BibTeX-rendered form.
  - `README.md` — orientation file with paper title, authors, DOI, license, retrieval date, and drain-target report path.
- A `git rm` of the original gzip/binary files in `research/fetched/issue-<N>/`.
- A row in `research/blocked-urls-round-<N>.md` flipping the prior "accept the gap" decision (if any) to ✅ recovered via e-print.

## Workflow

1. **Confirm the source is gzip** (not already extracted):
   ```bash
   file research/fetched/issue-<N>/<slug>_arxiv.org__e-print__<id>.html
   # Expected: "gzip compressed data, last modified: ..."
   ```
   If it's not gzip, abort — the skill targets the gzip mis-extraction case specifically.

2. **Copy to a scratch location and gunzip**:
   ```bash
   cp research/fetched/issue-<N>/<slug>_arxiv.org__e-print__<id>.html /tmp/<paper-slug>.gz
   gunzip /tmp/<paper-slug>.gz
   file /tmp/<paper-slug>
   # Expected: "POSIX tar archive (GNU)" or similar
   ```

3. **Untar into scratch directory**:
   ```bash
   mkdir -p /tmp/<paper-slug>-src
   tar -xf /tmp/<paper-slug> -C /tmp/<paper-slug>-src
   ls /tmp/<paper-slug>-src/
   ```
   Look for: `main.tex` (or whichever file matches the paper's filename convention), `defns.tex`, `00README.json` (arXiv's metadata blob), `.bbl` files for bibliography, possibly a `figures/` subdir.

4. **Identify the paper's main file**:
   - If `main.tex` exists, use it.
   - Otherwise, look for a `.tex` file whose name matches the paper title slug or arXiv ID.
   - As a fallback, inspect the first `.tex` file containing `\begin{document}` — that's the paper body.

5. **Determine the paper slug**: kebab-case, ≤ 30 chars, derived from the paper title. (For CaMeL: `camel-paper`. For "Attention Is All You Need": `attention-paper`.)

6. **Copy relevant files into the repo**:
   ```bash
   mkdir -p reference-only/<paper-slug>
   cp /tmp/<paper-slug>-src/main.tex \
      /tmp/<paper-slug>-src/defns.tex \
      /tmp/<paper-slug>-src/main.bbl \
      reference-only/<paper-slug>/
   ```
   Include any other `.tex` files actually referenced by `\input{...}` or `\include{...}` in `main.tex`. Don't copy figures, style files, or the `00README.json` metadata blob unless they're load-bearing for a citing report.

7. **Write a `README.md`** in the new directory. Required content:
   - Paper title (verbatim).
   - Authors (comma-separated).
   - DOI.
   - arXiv ID + version.
   - License (read from `00README.json` — typically CC-BY-4.0 or arXiv non-exclusive).
   - Retrieval date and the fetch-issue ID that produced the source.
   - File inventory (one bullet per copied file with line count + role).
   - Drain-target report path (one or more `research/*.md` or `research/followup/*.md`).
   - Optional: a note on whether the orchestrator already dispatched a drain subagent.

8. **Stage the new files** (`git add reference-only/<paper-slug>/`) and **delete the misclassified raw files** (`git rm research/fetched/issue-<N>/<slug>_arxiv.org__e-print__<id>.{html,md}`).

9. **Update the per-round blocked-urls log**: add a row for the e-print URL noting `✅ recovered via gunzip|tar -xf`, and if a prior round's "accept the gap" decision exists, mark it superseded.

10. **Hand off to the drain subagent**: the orchestrator typically dispatches a subagent that reads `main.tex` and updates the citing report's CaMeL/<paper> section with verbatim quotes anchored to line ranges.

## Concrete examples

### Example 1 — CaMeL paper recovery (real session material, 2026-05-14)

Input: `research/fetched/issue-42/29366c44d4_arxiv.org__e-print__2503.18813.html` (2.5 MB).

```bash
file research/fetched/issue-42/29366c44d4_arxiv.org__e-print__2503.18813.html
# → "gzip compressed data, last modified: Wed Jun 25 00:30:46 2025, from Unix, original size modulo 2^32 4157440"

cp research/fetched/issue-42/29366c44d4_arxiv.org__e-print__2503.18813.html /tmp/camel.gz
gunzip /tmp/camel.gz
file /tmp/camel
# → "POSIX tar archive (GNU)"

mkdir -p /tmp/camel-src
tar -xf /tmp/camel -C /tmp/camel-src
ls /tmp/camel-src/
# → main.tex (889 lines), defns.tex (558 lines), main.bbl, 00README.json, dozens of .sty/.pygtex/figures/

mkdir -p reference-only/camel-paper
cp /tmp/camel-src/{main.tex,defns.tex,main.bbl} reference-only/camel-paper/
# Wrote reference-only/camel-paper/README.md
git add reference-only/camel-paper/
git rm research/fetched/issue-42/29366c44d4_arxiv.org__e-print__2503.18813.{html,md}
```

Drain target: `research/followup/08-security-primitives.md` §3. Subagent dispatched immediately after with the brief "read main.tex; update §3 from abstract-anchored to paper-body-anchored." Outcome: §3 grew from 7 to ~15 subsections with 17 verbatim quotes anchored to `main.tex` line ranges.

### Example 2 — hypothetical reuse for a future paper

Input: arXiv ID `2406.06608` ("The Prompt Report"). Suppose round-9 attempts `arxiv.org/html/2406.06608v3` → 404, and `arxiv.org/pdf/2406.06608` → 200 but binary.

```bash
# Add /e-print/2406.06608 to the next [fetch-urls] issue.
# After the fetch lands:
file research/fetched/issue-N/<slug>_arxiv.org__e-print__2406.06608.html
# → gzip compressed data

cp research/fetched/issue-N/<slug>_arxiv.org__e-print__2406.06608.html /tmp/prompt-report.gz
gunzip /tmp/prompt-report.gz
mkdir /tmp/prompt-report-src && tar -xf /tmp/prompt-report -C /tmp/prompt-report-src

# Identify main file (suppose it's named 2406.06608.tex):
ls /tmp/prompt-report-src/*.tex
# → 2406.06608.tex, sections/intro.tex, sections/methods.tex, ...

mkdir -p reference-only/prompt-report
cp /tmp/prompt-report-src/2406.06608.tex reference-only/prompt-report/main.tex
cp /tmp/prompt-report-src/sections/*.tex reference-only/prompt-report/  # if main.tex \inputs them
cp /tmp/prompt-report-src/*.bbl reference-only/prompt-report/
# Wrote README.md naming research/followup/08-security-primitives.md as the drain target.
```

## Anti-patterns

- **Trying to `pandoc` the LaTeX directly without checking dependencies.** The arXiv source often uses paper-specific macros defined in `defns.tex` or `.sty` files; `pandoc` will choke. The subagent that reads `main.tex` resolves macros by ALSO reading `defns.tex`.
- **Copying every file from the tarball.** Style files, pygmentized listings, and figure binaries bloat the repo. Copy only `.tex` files referenced by `main.tex` plus `.bbl`.
- **Skipping the README.** Without it, a future agent finding `reference-only/<paper-slug>/main.tex` cannot determine which arXiv paper it is, when it was retrieved, or which report it anchors.
- **Treating the e-print archive as a permanent canonical source for ALL of the paper's content.** Figures, captions, and tables-with-images cannot be reconstructed from LaTeX alone. Note in the README if the citing report needs figure content.
- **Running this skill on non-arXiv hosts.** Other paper hosts (OpenReview, Semantic Scholar) do not expose LaTeX sources. The skill is arXiv-specific.

## Acceptance criteria

1. The original `research/fetched/issue-<N>/<slug>_arxiv.org__e-print__<id>.{html,md}` files are deleted (no orphaned 2.5 MB gzips committed long-term).
2. `reference-only/<paper-slug>/` contains `main.tex` + any `\input`-referenced `.tex` files + `.bbl` + `README.md`.
3. `README.md` names: paper title, authors, DOI, arXiv ID + version, license, retrieval date, drain-target report path.
4. The citing report's sources-status table is updated to ✅ paper-body-anchored (or ✅ partial-paper-body if figures are load-bearing and not recovered).
5. The fetch-action's `unfetched-sources.md` / `blocked-urls-round-N.md` no longer lists the arXiv paper as "accept the gap"; the e-print route is recorded as a permanent recovery option for the future.

## Files this skill creates / modifies

- **Creates**: `reference-only/<paper-slug>/main.tex`, `defns.tex`, `main.bbl`, `README.md` (+ any `\input`-referenced files).
- **Deletes**: `research/fetched/issue-<N>/<slug>_arxiv.org__e-print__<id>.{html,md}`.
- **Modifies**: `research/blocked-urls-round-<N>.md` (adds ✅ row); citing report's sources-status table (flips to ✅).
- **Triggers**: a follow-on drain subagent dispatched by the orchestrator to read the recovered `.tex` and update the citing report.
