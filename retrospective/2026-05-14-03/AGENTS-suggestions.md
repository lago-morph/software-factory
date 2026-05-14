# AGENTS.md suggestions — 2026-05-14-03

These are proposed additions to the project's agents file (typically `AGENTS.md` at the repo root). Each section contains:

1. **Proposed addition** — the exact text to paste.
2. **Why this earns its place in your agents file** — the argument for doing it, grounded in something that happened (or nearly happened).

Decide each on its own merits.

---

## Suggestion 1: Synthetic retros must be flagged as such in metadata.

### Proposed addition

> **Synthetic retros are flagged.** When a retrospective is back-filled after the fact (i.e., not written contemporaneously with the work it covers), the metadata block must include a `**Provenance**: SYNTHETIC / BACK-FILLED.` line naming the authoring date and the source material used (typically "PR descriptions and surrounding retros"). The retro's filename date and metadata UTC-date line refer to the *work* it covers, not the authoring date.
>
> *Grounded in: production of `retrospective/2026-05-11-02.md` on 2026-05-14.*

### Why this earns its place in your agents file

A retro without the synthetic flag is indistinguishable from a contemporaneous record. That matters for two reasons. First, the trust gradient: contemporaneous retros report what the author observed; synthetic retros report what the author inferred from PR descriptions. Readers should be able to tell which they're looking at, because synthetic retros are weaker evidence for "what really happened" and stronger evidence for "what the PR descriptions document." Second, the date-disambiguation gradient: a synthetic retro authored 2026-05-14 for work that happened 2026-05-11 has *two* meaningful dates. The filename and metadata convention pins both, so future audits can correctly attribute each. The cost of the rule is one extra metadata line. The cost of not having it is silent provenance erosion across the retrospective corpus.

---

## Suggestion 2: Date retros to the merge time of the last PR they cover, not the authoring time.

### Proposed addition

> **Retros are dated to coverage, not authorship.** A retrospective's filename date (`retrospective/YYYY-MM-DD-NN.md`) and metadata `UTC date` field refer to the *work* the retro covers — specifically, the UTC date of the merge of the **last PR** in its coverage window. Contemporaneous retros happen to satisfy this naturally (work and authorship share a date); synthetic retros must be deliberately dated to the work, not the authoring session. Sequence numbers within a date are append-only: a back-fill takes the next available `NN` regardless of when the work happened.
>
> *Grounded in: the synthetic `retrospective/2026-05-11-02.md` was authored 2026-05-14 but dated 2026-05-11 (PR #25 merged 2026-05-11T12:48:03Z).*

### Why this earns its place in your agents file

The retrospective corpus is browsed chronologically against the PR stream — readers expect `retrospective/2026-05-11-*.md` to describe work that landed on 2026-05-11. If synthetic retros are dated to authoring time, the corpus becomes non-monotonic against the PR timeline, and any future automated coverage audit (per `retro-coverage-audit-and-backfill`) has to special-case the authoring-vs-coverage skew. The cost of the rule is a deliberate choice at authoring time; the cost of not having it is that retros become harder to reconcile with the PR history they're auditing. Sequence numbers append-only also matter: if a 2026-05-11-02 back-fill exists and a later 2026-05-11-01.5 "more authentic" retro is found, do NOT renumber — take 2026-05-11-03. Numbering stability is part of the audit trail.

---

## Suggestion 3: Oversized MCP / tool responses are parsed out-of-band, not re-fetched.

### Proposed addition

> **Oversized tool results are processed via the saved file.** When a tool result exceeds the in-context token cap, the harness saves the full output to a file under `/root/.claude/projects/.../tool-results/`. Read fields from that file via a one-off script (e.g., `python3 -c "import json; data = json.load(open('<path>')); ..."`) rather than re-running the tool call with narrower filters and accumulating partial pages. The saved file is the canonical source; the partial in-context result is not.
>
> *Grounded in: `mcp__github__list_pull_requests` returned 134 KB JSON, exceeded the result cap, was parsed via python out-of-band to extract `number / state / merged_at / head.ref / base.ref / title` fields.*

### Why this earns its place in your agents file

This is the pattern that prevents pagination spirals on large MCP / API responses. Re-fetching with finer filters multiplies tool calls and accumulates partial coverage that's hard to reconcile. The saved-file path is reliable: the harness produces it, the path is in the truncation error, and `python3` is universally available for ad-hoc JSON / text slicing. The cost of the rule is one extra line in the agents file; the cost of not having it is unbounded re-fetch cost on every large response. This rule also generalizes beyond GitHub PR lists — any MCP server that returns large search results, file contents, or directory listings will hit the same cap. The pattern is the same: read the saved file.

---
