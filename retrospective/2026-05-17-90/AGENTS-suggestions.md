# AGENTS.md suggestions — 2026-05-17-90

These are proposed additions to `AGENTS.md`. Each section contains:

1. **Proposed addition** — exact text to paste.
2. **Why this earns its place in your agents file** — argument grounded in what happened during PR #90.

Decide each on its own merits.

---

## Suggestion 1: Stale-artifact check before draining

### Proposed addition

> **Stale-artifact check before draining `research/manual/`.** "When Phase 0 finds `.manifest.json` or `.subagent-brief.md` (or any dotfile that looks like a session artifact) in `research/manual/`, compare its listed filenames against the actual directory contents. If fewer than half the listed files are present, treat the dotfile as a stale artifact from a previous session and surface it to the user for deletion *before* running drain — do not silently ingest around it."
>
> *Grounded in: PR #90 Phase 1.*

### Why this earns its place in your agents file

In PR #90 the `research/manual/` directory contained `.manifest.json` (61 entries) and `.subagent-brief.md` from a previous preliminary-index-pass session that never completed. None of the 61 manifest filenames matched the actual 25 files present. Without an explicit staleness check I might have followed the brief's instructions or used the manifest's themes as ground truth, contaminating the drain. The cost of the rule is one `jq -r '.[].file' | head` plus a `ls` — sub-second. The cost of skipping the rule is corrupted decisions across the entire drain.

---

## Suggestion 2: Confirm titles aren't transport-encoded after drain

### Proposed addition

> **Confirm titles aren't transport-encoded after drain.** "After running `drain.py`, before staging anything, list new records and grep their titles for `=?utf-8?` or other MIME quoted-printable / RFC-2047 markers. If any are found, decode them (Python `email.header.decode_header` or equivalent) and update the records via the standard catalog-edit pattern before committing."
>
> *Grounded in: PR #90 Phase 4 step 3.*

### Why this earns its place in your agents file

Drain stage 2 currently pulls mhtml `Subject:` headers verbatim. For five 8090 blog posts the raw header was `=?utf-8?Q?Part=201:...?=` — readable in source but useless in the catalog's category renderer, sources.md, and any future text search. Drain didn't flag this; only a spot-check after the fact caught it. One `grep -E '=\?utf-8\?' reference-only/sources.json` is enough to detect. Until `drain.py` learns to decode (see proposed ADR), the operator has to check.

---

## Suggestion 3: Manually populate `references_from` after every drain

### Proposed addition

> **Manually populate `references_from` after every drain.** "After `drain.py` succeeds, run `python .claude/skills/research-pipeline/scripts/check-source-refs.py`. For each line of the form `<id>: <report.md> cites this URL but it's not in references_from`, append the report path to that record's `references_from` (via `jq` or a short Python script + the normalize step). Do *not* trust the `--fix` flag mentioned in `edit.md` — it is not implemented as of PR #90."
>
> *Grounded in: PR #90 Phase 4 step 2.*

### Why this earns its place in your agents file

`resources/_catalog/edit.md` has a table row claiming `check-source-refs.py --fix` populates `references_from`. The flag doesn't exist (the script ignores positional args entirely; `argparse` is not even imported). I lost ~3 minutes diagnosing why `--fix` produced no effect before reading the source. Until the script gains a real `--fix` (or drain folds it in — see proposed ADR), every operator who reads `edit.md` will hit the same trap. The marginal cost of the rule is one paste of the missing-refs list into a Python loop.

---

## Suggestion 4: Always redirect `render-sources-md.sh` output explicitly

### Proposed addition

> **Always redirect `render-sources-md.sh` output explicitly.** "The script writes the rendered markdown to stdout, not to `reference-only/sources.md`. To refresh the file in a working copy, invoke as: `bash .claude/skills/research-pipeline/scripts/render-sources-md.sh > reference-only/sources.md`. Never run it without the redirect — the output will land in the chat transcript and the file will be unchanged."
>
> *Grounded in: PR #90 Phase 5.*

### Why this earns its place in your agents file

The first `render-sources-md.sh` invocation dumped 2293 lines into the chat transcript. Recovery was a single redirected re-run, but a less-careful operator would have committed without regenerating the file at all, leaving sources.md stale relative to sources.json. The auto-regen workflow on main eventually covers this — but during a PR's review cycle, reviewers see the stale sources.md and react to outdated content. One redirect operator costs nothing; forgetting it costs a review cycle.

---

## Suggestion 5: Apply category tags during the drain commit, not later

### Proposed addition

> **Apply canonical-category tags before committing a drain.** "Stage 4's audit will flag every new record with `has-category-tag: no tag from the 15 canonical categories`. Do not commit a drain until all touched records have at least one tag from `resources/_catalog/category-taxonomy.md`. The URL-pattern table in that doc covers ≥90% of cases mechanically — for the rest, read the source briefly and pick from the 15. Do not defer tagging to 'cleanup later'; the renderer's `(no category)` bucket exists for transient cases, not as a parking lot."
>
> *Grounded in: PR #90 Phase 4 step 4.*

### Why this earns its place in your agents file

The 23 records touched by PR #90's drain all failed the `has-category-tag` audit on first pass. Retagging them required ~40 jq operations spread across 7 different category-tag combinations. Had I committed before retagging, the records would have entered main without category placement, become invisible in the sources.md category view, and burdened the next drain with the same audit failure surface plus 23 records of historical drift. The audit is reliable and binary — fix-on-drain is strictly cheaper than fix-later.
