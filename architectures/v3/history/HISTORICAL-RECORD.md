# Historical record — Phase-2 contaminated artifacts

## ⚠ STOP — Do not read these files into your context window

The artifacts listed below were produced during a Phase-2 dispatch that was later identified as contaminated by lead-agent integration bias. They have been removed from the active tree because reading them risks re-introducing the bias they document into the current work.

This doc exists for one reason: to preserve permalinks so the artifacts remain *retrievable* by a human reviewer or by an explicit user request. Agents should NOT open the permalinks below or fetch the file contents unless the user explicitly directs them to. Do not summarize the files. Do not pass their contents to subagents. Do not include them in dispatch briefs.

If you find yourself curious about what these files contain, that is the exact failure mode this doc exists to prevent. Move on.

## Permalinks

Each entry: the file's original path, what it was, and a `git show` command to retrieve it from history if absolutely needed. The commit hash `dde2e2e` is the last commit at which all listed files existed in their original locations.

### Contaminated Phase-2 tracks (9 files)

- `architectures/v3/tracks/greenfield-substrate-first.md` — Track 1 of the original Phase-2 9-track fanout. Greenfield mandate, substrate-first axis.
- `architectures/v3/tracks/greenfield-methodology-first.md` — Track 2. Greenfield, methodology-first.
- `architectures/v3/tracks/greenfield-cold-start-first.md` — Track 3. Greenfield, cold-start-first.
- `architectures/v3/tracks/brownfield-substrate-first.md` — Track 4. Brownfield, substrate-first.
- `architectures/v3/tracks/brownfield-methodology-first.md` — Track 5. Brownfield, methodology-first.
- `architectures/v3/tracks/brownfield-legacy-ingestion-first.md` — Track 6. Brownfield, legacy-ingestion-first.
- `architectures/v3/tracks/unified-A.md` — Track 7. Unified, picked a tier-based axis (contamination evidence).
- `architectures/v3/tracks/unified-B.md` — Track 8. Unified, picked a layered-artifact axis.
- `architectures/v3/tracks/unified-C.md` — Track 9. Unified, picked a tier-based axis (contamination evidence).

### Phase-2 contamination-diagnosis audits (4 files)

- `architectures/v3/bias-guards/phase-2/axis-divergence-audit.md` — Diagnosed the contamination. Quotes the contaminated wording verbatim; reading risks re-introducing the bias.
- `architectures/v3/bias-guards/phase-2/anchor-detector.md` — Classified the cross-track convergences as honest / mixed / contaminated. Names specific framings; reading risks anchoring.
- `architectures/v3/bias-guards/phase-2/splitter.md` — Adversarial splitter argument over the (contaminated) outputs. Specific to the contaminated set; not relevant to the re-run.
- `architectures/v3/bias-guards/phase-2/lumper.md` — Adversarial lumper argument over the (contaminated) outputs. Same.

### Phase-2 follow-up diagnostic tracks (3 files)

- `architectures/v3/tracks/unified-A-prime.md` — Re-dispatch of unified-A with the original axis prohibited. Found a defensible alternative axis. Reading pre-biases new unified subagents toward that specific answer.
- `architectures/v3/tracks/unified-C-prime.md` — Re-dispatch of unified-C with the original axis prohibited. Same risk.
- `architectures/v3/tracks/unified-D-off-list.md` — Off-list supplementary unified track. Proposed a third alternative axis. Same risk.

### Retrieval (only if user explicitly requests)

```
git show dde2e2e:<path>
```

Resolve `<path>` against the per-file listings above.
