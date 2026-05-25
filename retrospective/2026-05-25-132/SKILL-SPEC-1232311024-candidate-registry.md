# Spec: `candidate-registry`

- **ID**: SKILL-SPEC-1232311024
- **Source retrospective**: ../2026-05-25-132.md

## Intent

When a multi-candidate exploration carries forward many candidates (e.g., a research-synthesis methodology evaluating multiple architectural proposals), the question "what is the current status of candidate X?" becomes context-expensive to answer by reading individual artifacts. The skill produces a single-file registry of all surviving candidates with status, dependencies, defense placeholders, and buildability sketches owed, so the next session can pick up cold without re-deriving per-candidate status from scratch. Grounded in the v3-synthesis end-of-session work: 10 candidate methodologies (3 greenfield + 3 brownfield + 4 unified-mandate-attempt) were carried forward per the scoping principle; the registry consolidated their state into one ~3000-word lookup so the next agent does not have to re-read 9 Phase-2 tracks + 24 critique files + 4 decision briefs to know "what's the defense status of candidate U-C?"

## Trigger

**Direct triggers** (activate immediately):
- "Build a candidate registry"
- "Summarize the candidates we're carrying forward"
- "What's the state of each candidate?"
- "Per-candidate status doc"

**Proactive triggers** (offer the skill):
- A session has resolved a scoping decision to "carry all defensible candidates" or similar multi-candidate disposition.
- The next phase of work depends on knowing the state of multiple candidates that are scattered across separate artifacts.
- Session is winding down with multiple candidates still alive.

**Negative triggers** (do NOT use):
- Only 1-2 candidates survived (a registry is overkill).
- Candidates are still in active flux (the registry rots before the next session reads it).
- The user wants a deeper analysis rather than a state summary.

## Inputs

- **Candidate list** (required): the set of candidates to include. Either explicit names, or a pattern (e.g., "all candidates from `tracks/`" or "all candidates referenced in the integration brief").
- **Per-candidate evidence sources** (required): for each candidate, paths to its source track / draft / critique files. The skill reads these to fill the registry entries.
- **Working definitions** (recommended): the architecture/substrate/methodology vocabulary the registry will use. Without these the registry can drift into ad-hoc terminology.
- **Scope label** (optional): a short descriptor of why these candidates were carried forward (e.g., "Phase 3.4 scoping principle: all defensible candidates"). Goes at the top of the registry.

## Outputs

- A single registry markdown file (typically named `candidate-registry.md` in the same directory as the source candidates).
- Per-candidate entry: source path, axis/identity declaration, substrate primitives required, methodology shape (one paragraph), open critique findings (list), defense status (carries forward / carries forward as placeholder pending defense / removed), buildability sketches owed.
- Summary table at the end: one row per candidate × columns (mandate, axis, substrate-primitive count, open critique count, buildability scope).
- Optional: a continuity table if the candidates have downstream cross-references (e.g., greenfield → brownfield artifact flow).

## Workflow

1. Confirm the candidate list and the per-candidate evidence sources. If sources are pattern-based, expand the pattern via `git ls-files` or `find`.
2. For each candidate, read the source artifacts and extract:
   - Source path (link to track / draft file).
   - Axis declaration (one line, from the candidate's §0 or equivalent).
   - Substrate primitives required (list — read from §1.1 or §1 of the source).
   - Methodology shape (one paragraph — summarize the candidate's per-cycle structure).
   - Open critique findings (read from Phase-3.2 / Phase-3.3 critique files that target this candidate; list each finding with severity).
   - Defense status (apply the carry-forward criterion: "all critiques addressed or accepted as open" → carries forward; "some critiques open" → carries forward as placeholder pending defense).
   - Buildability sketches owed (for each substrate primitive the candidate requires that is not yet covered by a buildability sketch).
3. Compose the registry markdown:
   - Top matter: scope label + working definitions (or pointer to them) + carry-forward criterion.
   - One section per candidate (consistent structure: ID, source, axis, primitives, methodology, critiques, status, buildability owed).
   - Summary table at the end.
   - Optional continuity table if applicable.
4. Write the registry to the output path. Commit with a descriptive message naming the candidate count.
5. Print a one-line summary: candidate count + path to registry + any candidates marked as placeholders.

## Concrete examples

### Example 1: v3 synthesis candidate registry (the source-session example)

Input:
- Candidate list: 10 methodologies — GF-S, GF-M, GF-C (greenfield); BF-S, BF-M, BF-L (brownfield); U-A, U-B, U-C (unified Phase-2 tracks); D7-U-1 (alternative unified axis from the mandated blind-axis test).
- Sources per candidate: `architectures/v3/tracks/<name>.md` plus `architectures/v3/bias-guards/phase-3/{greenfield,brownfield,unified,cross-mandate,d7-blind-axis}/*.md`.
- Working definitions: from `phase-3.4-decisions-resolved.md` "Working definitions" section.
- Scope label: "10 methodology candidates carried forward per the Phase-3.4 scoping principle."

Output: `architectures/v3/candidate-registry.md` — 10 per-candidate sections + greenfield→brownfield continuity table + summary table. ~3000 words. Each entry: source, axis, ~5-9 substrate primitives, methodology shape paragraph, 3-5 open critique findings, defense status, buildability scope.

The registry is the entry point for the next session's Phase-4 work; it absorbed ~4000 lines of source artifacts into a 350-line lookup.

### Example 2: hypothetical ADR-set registry (across architecture-implementation candidates)

Input:
- Candidate list: 3 proposed implementations (Implementation-A, Implementation-B, Implementation-C) of a single architecture.
- Sources: per-implementation spec docs.
- Working definitions: from the architecture's ADR set.

Output: `implementations/registry.md` — 3 per-implementation entries with implementation shape, deployment dependencies, open ADR-trade-offs, status. Summary table contrasts cost, ops complexity, and capability coverage.

## Anti-patterns

- **Re-deriving everything per session.** The registry exists so the next session doesn't re-read every candidate's source artifacts. If the registry's per-candidate entries defer to "see the source for details," the registry has failed.
- **Letting the registry rot.** When candidates change status (defense placeholders closed, buildability sketches landed, candidates eliminated by later evidence), update the registry. A stale registry is worse than no registry.
- **Building a registry for 1-2 candidates.** Overkill. A simple bullet list in the handoff doc is sufficient.
- **Omitting the summary table.** The per-candidate sections are for depth; the summary table is for scanning. Both are needed.
- **Including candidate analysis (recommendations, preferences) inline.** The registry is a state lookup, not an analysis. Analysis belongs in decision briefs.

## Acceptance criteria

- [ ] One entry per candidate, all entries follow the same structure.
- [ ] Each entry includes source path, axis, substrate primitives, methodology shape, open critiques, defense status, buildability owed.
- [ ] Summary table at the end with one row per candidate.
- [ ] Top-matter includes scope label + carry-forward criterion (or pointer to it).
- [ ] Registry is committed and links resolve when the file is viewed on GitHub.

## Files this skill creates / modifies

- `<output-path>/candidate-registry.md` — the registry itself
- (git commit on current branch)
