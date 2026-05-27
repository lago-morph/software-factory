# auto-007 — Phase 7 dispatch shape

**Author.** Lead agent, unattended Phase-7 dispatch session 2026-05-27.
**Status.** **Round 1 (initial brief; first real adversarial wave pending).** Round-2 revision to follow after Round-1 reviewer findings land.
**Rewind point.** This brief's commit on [`claude/phase-7-auto-007-brief`](../../../). Reverting it returns Phase-7 dispatch to "undecided"; no per-candidate back-fill subagent has fired.

---

## TL;DR (≤200 words)

This brief decides Phase-7's dispatch shape. Phase 7 produces three sub-products: **per-candidate back-fill notes** (one per Phase-6 spec, audited against ≥8 archive files), **per-candidate spec patches** if any archive material is absorbed, and **a Phase-7-close session handoff**. The dispatch decision shape proposed: per-candidate parallel fanout (10 subagents, one per Phase-6 spec), with **archive-cluster sub-wave PRs as the PR-consolidation unit** OR an **omnibus single PR** when files are disjoint, **one lead-agent-authored exemplar slot** filled by the least-contested candidate (TBD; candidate set: BF-S or GF-M), **a 4-token classification taxonomy** (`absorbed | rejected (reason) | TBD | not-applicable-to-candidate-mandate`), **two bias-guard subagents** (silent-absorption auditor + historian per the [v1.2 plan § Phase 7](../../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md#phase-7--back-fill-audit-per-candidate-against-archived-v1v2-revised-in-v12)) firing concurrent with the per-candidate fanout, **per-candidate file as canonical artifact + lead-agent aggregation file** as a derived view, and **mandatory ≤500-word digests**. The brief also decides the **Phase-7-followup deferral binding mechanism** ([three named artifacts](#phase-7-followup-deferral-binding-mechanism-load-bearing) per the binding-artifact-triple rule) and the **be-generous-to-archive-material bias direction** per [`00-brief-v3` OQ-B10](../00-brief-v3.md). The Round-1 decision is at [§Decision (Round 1)](#decision-round-1).

## The question

Phase 7 of the v3 synthesis produces a per-candidate back-fill audit per the [v1.2 plan § Phase 7](../../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md#phase-7--back-fill-audit-per-candidate-against-archived-v1v2-revised-in-v12). Three sub-products are owed:

- **Per-candidate back-fill notes** — for each of the 10 Phase-6 candidates, an audit of every claim/framing/primitive/recommendation in the archive material, classified per-cell as `absorbed` (and v3 cite location) / `rejected (reason)` / `TBD` (and a 4th token below). Default file shape: per-candidate file × 10 + lead-agent-authored aggregation. Alternative: aggregation-only file at [`backfill-notes.md`](../backfill-notes.md).
- **Per-candidate spec patches** — for any archive material judged absorbable that isn't already in the candidate's Phase-6 spec (surgical §-level amendments only; §0 ADR-citation index preservation per [ADR 0065](../../../docs/adr/0065-section-0-adr-citation-index-table.md)).
- **Phase-7-close session handoff** at `architectures/v3/SESSION-HANDOFF-2026-05-27-phase-7-close.md` unblocking Phase 8 (lean-eval design per candidate).

**Archive scope:** **8 substantive files** total (verified at brief-write time via `ls archive/`):

| Dir | File | What it is |
|---|---|---|
| [`archive/`](../../../archive/) | [`research-plan.md`](../../../archive/research-plan.md) | 2026-05-14 pre-v3 "research → action plan" carrying user-stated constraints (already extracted into [`constraints-extracted.md`](../constraints-extracted.md)) + lead-agent recommendations (not extracted; Phase-7 scope) |
| [`archive/synthesis-v1-v2/`](../../../archive/synthesis-v1-v2/) | [`00-synthesis.md`](../../../archive/synthesis-v1-v2/00-synthesis.md) | Round-1 v2 synthesis post-primary-source-access; canonical entry for F1-F20 |
| [`archive/synthesis-v1-v2/`](../../../archive/synthesis-v1-v2/) | [`13-round-2-synthesis.md`](../../../archive/synthesis-v1-v2/13-round-2-synthesis.md) | Round-2 synthesis; promoted F21-F33 + Round-2 consensus C10-C16; proposed OpenHands+Overstory substrate stack |
| [`archive/architectures-v2/`](../../../archive/architectures-v2/) | [`00-comparison.md`](../../../archive/architectures-v2/00-comparison.md) | v2 comparison + decision guide; carried "Compound Atelier baseline" recommendation |
| [`archive/architectures-v2/`](../../../archive/architectures-v2/) | [`01-specification-refinery.md`](../../../archive/architectures-v2/01-specification-refinery.md) | v2 Architecture 1 — spec-as-product; revelation cycle; 5-mode failure classification |
| [`archive/architectures-v2/`](../../../archive/architectures-v2/) | [`02-compound-atelier.md`](../../../archive/architectures-v2/02-compound-atelier.md) | v2 Architecture 2 — queue + workpad + persona panel + accumulated `docs/solutions/` |
| [`archive/architectures-v2/`](../../../archive/architectures-v2/) | [`03-phase-gated-foundry.md`](../../../archive/architectures-v2/03-phase-gated-foundry.md) | v2 Architecture 3 — phase-bound experts, SRS/SAD/DD templates, RTM, gate boards |
| [`archive/architectures-v2/`](../../../archive/architectures-v2/) | [`04-evolutionary-tournament.md`](../../../archive/architectures-v2/04-evolutionary-tournament.md) | v2 Architecture 4 — genome library, predator agent, tournament bracket, model-family diversity |
| [`archive/architectures-v2/`](../../../archive/architectures-v2/) | [`failure-modes.md`](../../../archive/architectures-v2/failure-modes.md) | F1-F20 per-architecture coverage matrix (pre-F21+) |

(9 files including `failure-modes.md`; the brief refers to "8 substantive files" because `failure-modes.md` is a coverage matrix derived from the 4 architecture files — analytically the same source — but it IS a separate file and per-candidate back-fillers must enumerate it explicitly.)

**Already-inherited material (NOT in scope for back-fill — already absorbed):** the 7 D-1 through D-7 defaults per [`archive/synthesis-v1-v2/ARCHIVE.md`](../../../archive/synthesis-v1-v2/ARCHIVE.md#what-v3-inherits-from-these-syntheses--explicitly) were already carried forward into v3 as Round-1/Round-2 defaults. Back-fill subagents skip these or mark them `absorbed (v3 default D-N)` without further analysis.

**Bias direction:** per [`00-brief-v3` OQ-B10](../00-brief-v3.md), Phase 7 is the explicit mitigation for the archive-and-rebuild discipline's known weakness (recency bias *against* archive material). The lead agent and subagents are instructed to be **especially generous toward archive items**. A close-call between "rejected" and "absorbed" defaults to `absorbed (with adaptation)` rather than `rejected (subsumed)`.

The dispatch shape determines (i) how the 10 back-fill subagents are sequenced (parallel? sub-waves by mandate or by archive cluster? serial?), (ii) per-candidate brief shape + classification rubric + section structure + word budget, (iii) which candidate's notes file serves as the exemplar (lead-agent authored first), (iv) whether the aggregation file is its own subagent dispatch or lead-agent-authored at fanout-close, (v) which bias-guard subagents fire and when (concurrent with fanout or after), (vi) what the spec-patch flow looks like for absorbed material.

## Alternatives considered

### A. Per-candidate parallel fanout, 10 subagents in one wave, lead-agent exemplar first, omnibus PR, concurrent bias guards — **lead-agent recommendation**

- **Lead-agent inline: exemplar back-fill notes** for the least-contested candidate (TBD — candidate set {GF-M, BF-S}; lead agent picks at exemplar-authoring time based on which produces the cleanest cell-classification demonstrations for ≥6 of the 8 archive files). Committed as the first Phase-7 artifact (PR 3 in the run). Demonstrates the 4-token classification taxonomy, the per-archive-file section structure, and the cell-rationale verbatim text-pull discipline.
- **Wave 7.1 (all 10 in parallel)**. Nine remaining back-fill subagents fire concurrent after the exemplar lands. Each subagent reads (i) its candidate's Phase-6 spec, (ii) the 8 archive files, (iii) this brief's classification taxonomy + rubric, (iv) the exemplar notes file. Writes its candidate's back-fill notes file at `architectures/v3/backfill-notes/<candidate-id>.md`. Returns a ≤500-word digest.
- **Bias-guard subagents (Wave 7.2, 2 subagents in parallel)**, fire **concurrent with Wave 7.1** because they are independent (silent-absorption auditor reads only the 10 Phase-6 specs + the archive, NO per-candidate back-fill files; historian reads only the 10 Phase-6 specs + the archive). Per [v1.2 plan § Phase 7](../../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md#phase-7--back-fill-audit-per-candidate-against-archived-v1v2-revised-in-v12):
  - **Silent-absorption auditor.** Independently re-audits each Phase-6 spec against the archive. Surfaces cases where archive material appears in a spec without an explicit citation (potential silent absorption). Output: `architectures/v3/backfill-notes/audit-silent-absorption.md`.
  - **Historian.** Enumerates archive items that appear in zero Phase-6 specs in any form. Output: `architectures/v3/backfill-notes/audit-historian.md`.
- **Aggregation step.** After all 10 per-candidate files + 2 bias-guard files land, lead agent authors `architectures/v3/backfill-notes.md` aggregation file: one section per archive file × 10 candidate columns, populated by reading each per-candidate file's classifications. Reconciliation column for silent-absorption findings (any per-candidate `rejected` cell flagged by the auditor as silently absorbed gets a reconciliation row).
- **Spec patches (Wave 7.3, conditional)**. For any per-candidate absorbed material that isn't reflected in the candidate's Phase-6 spec, lead agent authors a surgical spec patch. Each patch: §-level additive edit (e.g., a new §6 Open carries item; a new §0 ADR-citation index row if an ADR is added; a new §3 methodology shape note). §0 table consistency preserved per [ADR 0065](../../../docs/adr/0065-section-0-adr-citation-index-table.md). Each patch is its own sub-PR OR consolidated into an omnibus per [`AGENTS-MD-d71e845b29`](../../../AGENTS.md#sub-wave-pr-consolidation-when-files-are-disjoint). Budget: ≤3 spec patches in-run; ≥4 triggers Phase-7-followup deferral.
- **PR consolidation: omnibus single PR** for Wave 7.1 + Wave 7.2 (10 back-fill files + 2 bias-guard files = 12 disjoint files written to the same parent branch). Per [ADR 0066](../../../docs/adr/0066-omnibus-pr-over-sub-wave-prs-when-files-are-disjoint.md), an omnibus PR is preferred over sub-wave PRs when files are disjoint and no blocking + non-blocking work bundling occurs. Each subagent writes to its own filename — no merge conflicts — so omnibus consolidation is safe.

**Per-candidate brief shape.** Each subagent receives:

1. The candidate's [`specs/<id>.md`](../specs/) (the Phase-6 spec — authoritative input for what's already in v3).
2. The full archive scope (8 files listed above) + the ARCHIVE.md indexes for context.
3. The classification taxonomy (4 tokens).
4. The exemplar back-fill notes file.
5. The rubric (see below).

**Per-candidate notes file rubric.** Section structure, word budget, citation floor:

- **H1**: `# Back-fill notes — <candidate-id> (<full name>) vs v1/v2 archive`.
- **YAML frontmatter**:
  ```yaml
  based-on-spec-commit: <commit-sha of candidate's specs/<id>.md>
  based-on-date: <YYYY-MM-DD>
  archive-files-audited:
    - archive/research-plan.md
    - archive/synthesis-v1-v2/00-synthesis.md
    - archive/synthesis-v1-v2/13-round-2-synthesis.md
    - archive/architectures-v2/00-comparison.md
    - archive/architectures-v2/01-specification-refinery.md
    - archive/architectures-v2/02-compound-atelier.md
    - archive/architectures-v2/03-phase-gated-foundry.md
    - archive/architectures-v2/04-evolutionary-tournament.md
    - archive/architectures-v2/failure-modes.md
  cell-counts:
    absorbed: <N>
    rejected: <N>
    tbd: <N>
    not-applicable: <N>
  ```
- **§1 Overview** (~150 words). Candidate's mandate + axis + entry-mode; one-paragraph statement of the candidate's relationship to the v2 architecture lineage (e.g., "U-A is closest to Architecture 2 Compound Atelier; the audit will be especially careful on Compound-Atelier-specific primitives like persona panels.").
- **§2-§9 Per-archive-file audits** (one section per archive file; ~400-600 words each, ~3000-4500 total). For each archive file:
  - **§N.0** File header: `## §N — archive/<path>`
  - **§N.1** Enumeration of claims/framings/primitives/recommendations in the file. Each as a numbered bullet (`§N.1.1`, `§N.1.2`, ...). Source the enumeration from the file's table of contents + section headers + numbered claims; **NOT** a full re-extraction (would blow the word budget). Floor: ≥5 enumeration bullets per archive file unless the file is trivially short.
  - **§N.2** Per-item classification table:
    ```
    | Item | Verdict | Rationale | v3 cite (if absorbed) |
    |---|---|---|---|
    | §N.1.1 | absorbed | The X primitive is realized as Y in this spec | specs/<id>.md §2 (ADR 00NN) |
    | §N.1.2 | rejected | The Z recommendation is mandate-rejected because… | — |
    | §N.1.3 | not-applicable | The W discipline is Architecture-4-tournament-specific; this candidate doesn't claim that axis | — |
    | §N.1.4 | tbd | Lead agent and silent-absorption auditor should reconcile | — |
    ```
  - **§N.3** Notes (any per-file observations that don't fit a per-item row).
- **§10 Summary** (~200 words). Per-token cell counts; high-confidence cells; surfaced TBDs.
- **§11 References** (mandatory; relative paths only per [`AGENTS.md § Internal document references`](../../../AGENTS.md#internal-document-references)). Floor: candidate's spec + 8 archive files + this brief + the candidate's substrate-requirements summary + any ADRs the audit cites.

**Classification taxonomy (4 tokens, lead-agent proposal — Round-1 reviewers should challenge).**

| Token | Semantics |
|---|---|
| `absorbed` | The candidate's spec carries the archive item in some form. Cite v3 location (spec section + ADR if applicable). The archive item's wording may differ; what matters is the concept is realized. |
| `rejected (reason)` | The candidate deliberately did not carry the archive item. Reason cited (e.g., "Architecture-4-tournament-specific; this candidate is greenfield-S"). |
| `not-applicable-to-candidate-mandate` | The archive item is structurally inapplicable to this candidate's mandate/axis/entry-mode. **Distinct from `rejected`:** rejected implies a deliberate choice (could have absorbed but chose not to); not-applicable implies "this token never even applied." Example: a brownfield-specific Compound-Atelier primitive being audited against GF-S — N/A, not rejected. |
| `tbd` | Lead agent and silent-absorption auditor should reconcile at aggregation time. Use sparingly — TBDs require lead-agent follow-up subagent dispatch. |

**Self-check rubric** per [`AGENTS-MD-e74e4811a2`](../../../AGENTS.md#self-check-rubric-requires-tool-verification-for-measurable-items). Subagent runs:

- (a) `wc -w` on its notes file to verify word budget compliance (3000-5500 depending on candidate complexity).
- (b) `ls` on every cited v3 file path (`specs/<id>.md`, any ADR files) to verify the file exists.
- (c) `grep` for §1-§11 headers + §N.0 file-header pattern for each archive file to verify section structure.
- (d) `grep -E '^\| §[0-9]+\.1\.[0-9]+' <file>` to verify ≥5 enumeration rows in each §N.2 table per archive file (or explicit "trivially short" note in §N.3).
- (e) `grep -cE '\| absorbed \|'` etc. to verify YAML frontmatter cell-counts match table-row counts.
- (f) `grep -F` for verbatim text-pull when invoking a binding rule table per [`AGENTS-MD-bf4431be57`](../../../AGENTS.md#verbatim-text-pull-when-citing-binding-rule-tables).
- (g) `grep -c "tbd"` on the file — surfaced TBDs reported in return digest.

**Word budget per notes file: 3000-5500 words.** Lighter candidates (GF-M, GF-S) toward lower end (3000-3500); heavier candidates (BF-L, D7-U-1, U-A) toward upper end. Lead-agent expectation: most candidates land at ~3500-4000.

**Pros.**
- Maximum parallelism: 10 + 2 bias-guards = 12 subagents fire concurrent ⇒ all files land in roughly one fanout's wall-clock time.
- Per-candidate accountability + crisp blast radius if any back-fill needs re-dispatch.
- Bias-guards-concurrent leverages their independence — no waiting for the per-candidate verdicts to materialize before they begin work.
- Lead-agent exemplar enforces shape consistency across the 9 sibling notes files (per [`AGENTS-MD-eec503a3c2`](../../../AGENTS.md#exemplar-before-parallel-uniform-schema-fanout)).
- Aggregation-as-lead-agent (not as a subagent) — lead agent at fanout-close has full context for cross-candidate reconciliation; matrix view requires that cross-candidate read.
- Omnibus single PR (per [ADR 0066](../../../docs/adr/0066-omnibus-pr-over-sub-wave-prs-when-files-are-disjoint.md)) collapses 12 files into 1 PR; significant PR-cap savings over per-cluster sub-wave PRs.

**Cons.**
- 10 concurrent back-fill subagents + 2 bias-guards = 12 subagents in one wave. At the upper end of the ~15-wave practical limit; the harness should handle it, but a stale or unfair-dispatch failure on one subagent forces a full sub-wave-re-dispatch.
- Aggregation budget: 10 notes × ≤500-word digests = ~5K words of subagent return content + 12 file contents to ingest. Manageable but at the upper end.
- Bias-guards-concurrent means the silent-absorption auditor cannot use the per-candidate verdicts as input (would create a circular dependency). Mitigation: auditor produces an independent verdict, and lead-agent reconciles at aggregation time.
- Spec-patch flow is conditional and undefined-in-advance — if many candidates need patches, the run could balloon. Mitigation: ≤3 in-run, ≥4 triggers deferral.

### B. Single 10-subagent wave (no exemplar, no bias guards run in this wave)

Dispatch all 10 back-fill subagents in one wave; bias-guards in a separate later wave; no exemplar.

- **Pros.** Simpler dispatch — no exemplar-authoring lag; no concurrent-wave coordination.
- **Cons.** Uniform-schema deliverable without an exemplar violates [`AGENTS-MD-eec503a3c2`](../../../AGENTS.md#exemplar-before-parallel-uniform-schema-fanout). Bias guards firing later wastes wall-clock time (they're independent). **Not chosen** because the exemplar discipline is binding and bias-guards firing earlier is free.

### C. Per-mandate-cluster sub-waves (3 GF + 3 BF + 4 U)

Sequentially or concurrently dispatch waves by mandate (mirroring Phase 6's Wave 6.1/6.2/6.3 shape).

- **Pros.** Mandate clustering offers a clean PR-consolidation boundary if files weren't disjoint.
- **Cons.** Files ARE disjoint (each subagent writes only its candidate's notes file under a unique filename) — so omnibus consolidation (Option A) wins on PR-cap with no review-quality loss. Per the [Phase-6-close honest-acknowledgement](../SESSION-HANDOFF-2026-05-26-phase-6-close.md#honest-acknowledgements) and [`AGENTS-MD-d71e845b29`](../../../AGENTS.md#sub-wave-pr-consolidation-when-files-are-disjoint), the Phase-6 dispatch's planned 3 sub-wave PRs collapsed to 1 omnibus PR for exactly this reason. **Not chosen** — repeats Phase-6's learned-the-hard-way pattern.

### D. Aggregation-only file (no per-candidate files)

Per the dispatch prompt's "Default = aggregation file". The aggregation file is the canonical artifact; per-candidate notes don't exist as separate files; all 10 back-fill subagents write into different sections of the same aggregation file.

- **Pros.** Fewer files; matrix view is the primary artifact (which is what Phase 8 will consume).
- **Cons.** Single-file concurrent writes by 10 subagents = serious merge-conflict surface. Even with section-level write isolation, the subagents have no clean way to commit independently. Aggregation-as-derived-from-per-candidate (Option A's shape) is strictly cleaner: per-candidate files are the writable artifacts, aggregation is the read-only derived view. **Not chosen.**

### E. Sequential per-candidate (serial fanout)

Dispatch the 10 subagents sequentially, each reading the previous candidate's notes file as a calibration point.

- **Pros.** Successor subagents could refine the exemplar's shape based on what the earlier ones produced.
- **Cons.** 10× wall-clock cost vs parallel. The exemplar (Option A) already serves the calibration purpose. **Not chosen.**

### F. Per-archive-file fanout (NOT per-candidate)

Dispatch 8 subagents, one per archive file. Each subagent audits its file against all 10 candidate specs.

- **Pros.** Per-archive-file deep-reading discipline; each subagent becomes expert in one file's content.
- **Cons.** Inverts the per-candidate scoping principle that the v1.2 plan § Phase 7 mandates ("the audit runs per candidate"). The 10 candidate columns × 8 archive rows would all be aggregated by 8 different subagents, each with partial-spec context — silent absorption is harder to detect when the auditor has read 10 specs in passing rather than 1 deeply. **Not chosen** — violates plan's explicit per-candidate framing.

### G. Lead-agent inline back-fill (no subagent dispatch)

Lead agent authors all 10 per-candidate notes files inline + the aggregation + the bias-guard audits.

- **Pros.** No coordination overhead; single-author cross-candidate consistency.
- **Cons.** Saturates context with archive + spec detail (10 specs × ~4000 words + 8 archive files × ~10K words + per-candidate analysis = ~250K words). Forecloses fresh-context per-candidate reasoning. **Not chosen.**

## Decision (Round 1)

**Option A. Per-candidate parallel fanout, 10 subagents in one wave + 2 bias-guard subagents concurrent, lead-agent exemplar first, omnibus PR, lead-agent aggregation.** Per the structure laid out in [Alternative A](#a-per-candidate-parallel-fanout-10-subagents-in-one-wave-lead-agent-exemplar-first-omnibus-pr-concurrent-bias-guards--lead-agent-recommendation) above.

Concretely:

- **Lead-agent inline: exemplar back-fill notes** for the least-contested candidate (TBD at exemplar-authoring time — candidate set is {GF-M, BF-S}; lead agent picks based on which produces the cleanest cell-classification demonstrations across all 8 archive files). ~3500-word target. Authored using the rubric below. Committed as PR 3.
- **Wave 7.1 (all 10 in parallel)** fires after the exemplar lands. 9 spec-authoring back-fill subagents (10 minus exemplar candidate).
- **Wave 7.2 (2 bias-guards in parallel)** fires concurrent with Wave 7.1 (independent input streams).
- **Aggregation step**: lead-agent authors `backfill-notes.md` aggregation file at fanout-close.
- **Wave 7.3 (conditional spec patches)**: surgical §-level edits for absorbed material; ≤3 in-run; ≥4 triggers deferral.

**Total subagents this run:** 9 (back-fill, excluding exemplar candidate) + 2 (bias-guards) = **11 back-fill-equivalent dispatches**, plus 6 adversarial reviewers across this brief's two rounds = **17 subagents total for Phase 7**.

**PR-cap math (Round-1 estimate, omnibus consolidation):** 1 (scope envelope, PR #187 already opened) + 1 (this brief R2) + 1 (exemplar) + 1 (omnibus: 9 back-fill + 2 bias-guards + 1 aggregation) + ≤1 (conditional spec patches, possibly omnibus if multiple) + 1 (handoff) + 1 (summary) + 1 (retro) = **7-8 PRs against ≤15 Phase-7 budget cap**, comfortable 7-8 PR margin.

### Round-1 reasoning

Three drivers select Option A:

1. **The Phase-6 precedent worked cleanly with the same shape** — per-candidate parallel fanout + lead-agent exemplar + uniform rubric + omnibus PR consolidation (post-collapse). The 9-spec Phase-6 omnibus PR validated the omnibus pattern at ~9 disjoint files; Phase-7's 12-file omnibus is a similar shape. Reusing the precedent exploits already-calibrated patterns.
2. **Bias-guards-concurrent is free.** The silent-absorption auditor and historian have independent input streams (they read archive + Phase-6 specs, NOT per-candidate back-fill files). Running them concurrent with Wave 7.1 saves a full fanout wall-clock without any quality loss. The aggregation-time reconciliation step is the natural place to surface any per-candidate-vs-auditor disagreements.
3. **The 4-token taxonomy resolves the not-applicable-vs-rejected ambiguity** that would otherwise emerge per-candidate. Without the `not-applicable-to-candidate-mandate` token, every Architecture-4-tournament-specific item being audited against, say, BF-S would be classified `rejected (mandate-mismatch)`, which conflates two different verdicts: "deliberate choice not to absorb" vs "structurally inapplicable." The 4-token taxonomy gives auditors a clean separator that downstream Phase-8 lean-eval design can use to identify cross-mandate inheritance candidates separately from cross-mandate exclusions.

## Phase-7-followup deferral binding mechanism (load-bearing)

If the Phase-7-followup deferral fires (≥4 candidates need spec patches, exhausting the ≤3 in-run patch budget), the deferral is bound by **three named artifacts** per [`AGENTS-MD-2adf78e54a`](../../../AGENTS.md#deferred-work-binding-artifact-triple):

1. **Session handoff doc.** `architectures/v3/SESSION-HANDOFF-2026-05-27-phase-7-close.md` carries a non-negotiable `## Phase-7-followup carry-forward (deferred from auto-007)` section. Names: (a) the candidates with deferred patches; (b) the absorbed-material findings verbatim from per-candidate back-fill notes; (c) the binding "Phase 8 MAY proceed but Phase-7-followup must close before lean-eval execution" constraint (Phase 7's deferral is less blocking than Phase 6's; lean-eval design can proceed against unpatched specs as long as the deferral is acknowledged in the lean-eval brief).
2. **Morning summary "what I deliberately did NOT do" section.** The run's morning summary carries a `Phase-7-followup spec patches for ≥4 candidates with absorbed material — deferred to <next-run-id>` bullet.
3. **Next-run dispatch prompt.** `next-agent-prompt-phase-7-followup.md` authored at this run's close (or its absence flagged as a follow-up bullet in the morning summary). Points at the Phase-7-close handoff and at this brief.

## Exemplar pre-fanout self-check gate (load-bearing)

Before dispatching Wave 7.1 / Wave 7.2, the lead agent **runs self-check items (a)-(g) on the exemplar** and records pass/fail in this brief's [§Exemplar pre-fanout self-check results](#exemplar-pre-fanout-self-check-results) (subsection appended at exemplar-commit time). **Failure on item (d)** (≥5 enumeration rows per archive file) **blocks fanout** — lead agent re-authors the exemplar before any sub-wave fires. Mirrors the Phase-6 U-C exemplar gate pattern.

## Bias-direction discipline

Per [`00-brief-v3` OQ-B10](../00-brief-v3.md), Phase 7 is the explicit mitigation for the archive-and-rebuild discipline's known weakness (recency bias *against* archive material). Subagent briefs must include this instruction verbatim:

> **Be generous toward archive items.** A close-call between `rejected (subsumed)` and `absorbed (with adaptation)` defaults to `absorbed`. The Phase-7 audit's purpose is to catch what slipped through, not to re-justify the v3 decisions. Lead agent and verifier prefer over-absorption (with a follow-up reconciliation row) to under-absorption (which is invisible at audit-close).

## Sub-wave coordination protocol

Each sub-wave / wave fires from a separate stacked branch:
- **Exemplar (PR 3)** branch: `claude/phase-7-exemplar`. Lead agent authors `backfill-notes/<exemplar-id>.md` and (if not already created) `backfill-notes/` directory + `backfill-notes/.gitkeep`.
- **Wave 7.1 + 7.2 (PR 4 omnibus)** branch: `claude/phase-7-fanout-omnibus`. 9 back-fill subagents write each to `backfill-notes/<candidate-id>.md` (one file per subagent — disjoint); 2 bias-guard subagents write to `backfill-notes/audit-silent-absorption.md` and `backfill-notes/audit-historian.md`. Lead agent writes aggregation at `backfill-notes.md` (top-level). 12 disjoint files.
- **Wave 7.3 (PR 5 conditional)** branch: `claude/phase-7-spec-patches` (only fires if ≥1 spec needs patching). Lead-agent-authored surgical edits to `specs/<id>.md` files. Single PR with multiple per-candidate spec patches as commits (omnibus per [ADR 0066](../../../docs/adr/0066-omnibus-pr-over-sub-wave-prs-when-files-are-disjoint.md)).
- **Phase-7-close handoff (PR 6)** branch: `claude/phase-7-handoff`. New `SESSION-HANDOFF-2026-05-27-phase-7-close.md` + `AGENT-ENTRY.md` Section-2 update.
- **Morning summary + retrospective (PR 7)** branch: `claude/phase-7-summary-retro`. Top-level `overnight-summary.md` (rename to `run-summary-2026-05-27.md` since this is a daytime run) + `retrospective/2026-05-27-<PPP>/` full-package directory.

**File uniqueness invariant**: each back-fill subagent's notes file is named per the candidate's ID (`gf-s.md` / `gf-m.md` / `gf-c.md` / `bf-s.md` / `bf-m.md` / `bf-l.md` / `u-a.md` / `u-b.md` / `u-c.md` / `d7-u-1.md`). Bias-guard subagents write to fixed audit filenames. Exemplar candidate's file is authored by lead agent on PR 3 before fanout.

**Conflict protocol**: if a back-fill subagent finds its target notes file already exists or the branch tip moved unexpectedly, surface in return digest; do not force-push. Lead agent reconciles at aggregation time.

## Common archive-file-to-path mapping

Pre-authored per [`AGENTS-MD-8740bd7b0a`](../../../AGENTS.md#adr-number-to-filename-mapping-in-subagent-dispatch-briefs) — every per-candidate dispatch brief inherits this table by reference.

| Slot | File path | Approximate size | Notes |
|---|---|---|---|
| §2 | [`archive/research-plan.md`](../../../archive/research-plan.md) | ~25 KB | Pre-v3 plan; user-stated constraints already extracted; back-fill audits the lead-agent recommendations |
| §3 | [`archive/synthesis-v1-v2/00-synthesis.md`](../../../archive/synthesis-v1-v2/00-synthesis.md) | ~36 KB | Round-1 v2 synthesis; F1-F20 canonical |
| §4 | [`archive/synthesis-v1-v2/13-round-2-synthesis.md`](../../../archive/synthesis-v1-v2/13-round-2-synthesis.md) | ~49 KB | Round-2 synthesis; F21-F33 + C10-C16; OpenHands+Overstory recommendation |
| §5 | [`archive/architectures-v2/00-comparison.md`](../../../archive/architectures-v2/00-comparison.md) | ~22 KB | v2 comparison + decision guide; Compound Atelier baseline recommendation |
| §6 | [`archive/architectures-v2/01-specification-refinery.md`](../../../archive/architectures-v2/01-specification-refinery.md) | ~25 KB | v2 Architecture 1 — Spec Refinery |
| §7 | [`archive/architectures-v2/02-compound-atelier.md`](../../../archive/architectures-v2/02-compound-atelier.md) | ~33 KB | v2 Architecture 2 — Compound Atelier |
| §8 | [`archive/architectures-v2/03-phase-gated-foundry.md`](../../../archive/architectures-v2/03-phase-gated-foundry.md) | ~32 KB | v2 Architecture 3 — Phase-Gated Foundry |
| §9 | [`archive/architectures-v2/04-evolutionary-tournament.md`](../../../archive/architectures-v2/04-evolutionary-tournament.md) | ~31 KB | v2 Architecture 4 — Evolutionary Tournament |
| §(addendum) | [`archive/architectures-v2/failure-modes.md`](../../../archive/architectures-v2/failure-modes.md) | ~5 KB | F1-F20 per-architecture coverage matrix (derived from §5-§9) |

(Candidate-mandate-to-v2-architecture-lineage mapping is NOT pre-authored — each candidate's back-fill subagent identifies its own closest-lineage v2 architecture in §1.)

## Glossary

(Inherited by all subagent briefs.)

- **Archive file**. One of the 9 files listed in [§Common archive-file-to-path mapping](#common-archive-file-to-path-mapping). Each file is read once per candidate by that candidate's back-fill subagent.
- **Archive item**. A single claim, framing, primitive, or recommendation enumerated from an archive file. Granularity: paragraph-or-shorter; named primitives count individually; long lists of failure modes count as one per failure mode.
- **Cell**. A (candidate × archive item) pair in the back-fill matrix. Total cell count: ~50 items × 10 candidates = ~500 cells (rough; actual count emerges from per-candidate enumeration).
- **Verdict / classification**. One of the 4 tokens: `absorbed | rejected (reason) | not-applicable-to-candidate-mandate | tbd`.
- **Lineage mapping**. Per-candidate identification of its closest v2 Architecture lineage (Architecture 1 Spec Refinery / Architecture 2 Compound Atelier / Architecture 3 Phase-Gated Foundry / Architecture 4 Evolutionary Tournament). Lead-agent best-draft mappings: GF-S~A4 tournament-flavored, GF-M~A1 refinery-flavored, GF-C~A3 foundry-flavored (or A1 hybrid), BF-S~A2 atelier-flavored, BF-M~A2 atelier+A3 hybrid, BF-L~A3 heavy-foundry, U-A~A2 atelier-flavored, U-B~A1 refinery-flavored, U-C~A3+A1 hybrid, D7-U-1~A4 tournament+A3 hybrid. **These mappings are NOT binding** — each subagent makes its own call in §1.
- **Already-inherited material**. D-1 through D-7 defaults per [`archive/synthesis-v1-v2/ARCHIVE.md`](../../../archive/synthesis-v1-v2/ARCHIVE.md#what-v3-inherits-from-these-syntheses--explicitly). Back-fill subagents skip these or mark `absorbed (v3 default D-N)` without further analysis.
- **Be-generous bias**. Per [`00-brief-v3` OQ-B10](../00-brief-v3.md); defaults close-calls to `absorbed (with adaptation)`.
- **Silent absorption**. An archive item that appears in a Phase-6 spec without an explicit citation — possibly inherited unconsciously by the spec author. Surfaced by the silent-absorption auditor bias guard.
- **Historian gap**. An archive item that appears in zero Phase-6 specs in any form. Surfaced by the historian bias guard. Could indicate (a) genuine across-the-board rejection, (b) a primitive class that all candidates missed, (c) mandate-rejection of an entire branch.

## Honest acknowledgements

Per [`AGENTS-MD-ffe35aa500`](../../../AGENTS.md#honest-acknowledgements-for-pre-round-2-wave-firing) (pre-Round-2 wave firing): no Phase-7 back-fill subagent has fired pre-Round-2; this dispatch brief precedes the wave dispatch. Mechanically verifiable: `git log --oneline -- architectures/v3/backfill-notes/` returns empty as of this commit; `ls architectures/v3/backfill-notes.md` returns "No such file or directory" as of this commit.

This brief lives at commit **`<TBD-Round-1-SHA>`** on [`claude/phase-7-auto-007-brief`](../../../).

**Process-bug carry-forward.** Pre-flight verification per [`AGENTS-MD-4f8c2a1b03`](../../../AGENTS.md#pre-flight-prior-phase-merge-state-verification) passed at session start — all 10 Phase-6 specs + handoff + mandate-fit matrix + verification findings confirmed in `origin/main` before this brief was authored.

## Open questions for the Round-1 adversarial reviewers to challenge

1. **Wave shape.** Is 10-parallel + 2-bias-guards-concurrent right? Or is the harness load too high at 12 parallel subagents? Should bias-guards fire after the per-candidate fanout completes so they can read the per-candidate verdicts (at cost of wall-clock)?
2. **Exemplar choice.** {GF-M, BF-S} candidate set — is this right? Or should a higher-complexity candidate (U-A, BF-L) be the exemplar to demonstrate the harder cell-classification cases (e.g., U-A claiming Architecture-2 Compound Atelier primitives that BF-L claims differently)?
3. **4-token classification taxonomy.** Is `not-applicable-to-candidate-mandate` a useful 4th token, or does it just dilute `rejected (reason)` and make per-candidate verdicts harder to compare? Alternative: 3-token (`absorbed | rejected | tbd`) per the dispatch prompt default. Or 5-token (add `absorbed-with-adaptation` separately from plain `absorbed`).
4. **Per-candidate file + aggregation vs aggregation-only.** Per-candidate files give canonical per-candidate artifacts but produce 10 extra files. Aggregation-only is what the dispatch prompt suggested as default. Which is the right primary artifact?
5. **Word budget 3000-5500.** Is this right-sized? 9 archive-file sections × ~400-600 words = 3600-5400 baseline; §1 + §10 + §11 add ~400 words. So 4000-5800 is realistic, exceeding the upper bound. Should the budget be raised to 4000-6500?
6. **Be-generous bias direction.** Is the verbatim bias instruction load-bearing or just a flag? Should it be a self-check item (e.g., "for any `rejected (subsumed)` verdict, justify in ≥2 sentences why `absorbed` is not appropriate")?
7. **Spec-patch threshold.** ≥4 candidates triggering deferral — is this right? Or should it be ≥3 (more conservative — deferral fires earlier) or ≥6 (more aggressive — accept significant in-run patching)?
8. **Silent-absorption auditor concurrent vs after.** Concurrent is faster but the auditor can't read per-candidate verdicts. Is the aggregation-time reconciliation step (lead agent compares auditor's `silently absorbed` findings to per-candidate `rejected` verdicts) sufficient? Or does it lose load-bearing information?
9. **PR-cap budget.** 7-8 PRs against ≤15 cap is generous. Could the run absorb more work (e.g., a Phase-7 deeper-dive cross-spec characterization audit per Phase-6-followup item #2 from the [Phase-6-close handoff](../SESSION-HANDOFF-2026-05-26-phase-6-close.md#phase-6-followup-carry-forward))? Or should PR-cap stay tight?
10. **Archive scope completeness.** 9 files enumerated — does any archive material live OUTSIDE these directories that Phase 7 should also audit? E.g., research/ reports referenced by the archive but not themselves archived? Per the [`archive/ARCHIVE.md`](../../../archive/ARCHIVE.md) note, research reports are explicitly NOT archived — they're "evidence not recommendations" and remain in `research/` for the v3 synthesis. Reviewers should confirm this scoping is correct.

(Round-1 reviewers will challenge any/all of these + anything else they find.)

## Round-1 if-user-overrides rewind point

This brief's commit on `claude/phase-7-auto-007-brief`. Revert to undo the Round-1 framing; no back-fill subagent has fired (this brief precedes the wave dispatch).

## Downstream impact

- **Phase 8** (lean-eval design per candidate) inherits the per-candidate back-fill notes as a binding input — the lean-eval brief for each candidate references its back-fill cells for any absorbed items that need pressure-testing.
- **Spec patches** (Wave 7.3) update the per-candidate Phase-6 specs in-place. Phase 8 reads the patched specs.
- **Mandate-fit matrix** is NOT touched by Phase 7 (per the [§What I plan to NOT do](../scope-envelope-phase-7.md#what-i-plan-to-not-do) section of the scope envelope). Back-fill audits don't re-litigate matrix cells.
- **DEC-1.a working hypothesis** (no methodology serves both mandates) is mildly pressure-tested by Phase 7 — historian gaps and silent-absorption findings could surface a unified-attempt candidate that absorbed Architecture-2-Compound-Atelier and Architecture-3-Phase-Gated-Foundry primitives without acknowledging the cross-mandate compatibility risk.

## Round-1 reviewer findings

(Three real subagents will be dispatched per [`AGENTS.md § Adversarial review MUST be real subagents`](../../../AGENTS.md#adversarial-review-must-be-real-subagents). Findings will be folded into the Round-2 revision below.)

_(Round-1 findings will land at this section.)_

## Exemplar pre-fanout self-check results

(Per the exemplar-self-check-gate rule. Subsection populated at exemplar-commit time. Until populated, no sub-wave fires.)

| Self-check item | Result | Notes |
|---|---|---|
| (a) `wc -w` against 3000-5500 budget | TBD | run at exemplar-commit time |
| (b) `ls` on every cited v3 file path | TBD | run at exemplar-commit time |
| (c) `grep` for §1-§11 + §N.0 file-header per archive file | TBD | run at exemplar-commit time |
| (d) `grep -E '^\| §[0-9]+\.1\.[0-9]+'` ≥5 enumeration rows per archive file | TBD | **load-bearing** — failure here blocks fanout |
| (e) `grep -cE '\| absorbed \|'` etc. cell-counts match YAML | TBD | run at exemplar-commit time |
| (f) `grep -F` verbatim text-pull when invoked | TBD | when invoked |
| (g) `grep -c "tbd"` and surface TBDs in digest | TBD | run at exemplar-commit time |
| **Exemplar commit SHA** | TBD | populated at commit time |
| **Exemplar candidate** | TBD | lead-agent picks from {GF-M, BF-S} at authoring time |

---

*(Round 1 closes when reviewers' findings land. Round-2 revision follows.)*
