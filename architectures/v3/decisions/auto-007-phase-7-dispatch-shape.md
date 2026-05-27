# auto-007 — Phase 7 dispatch shape

**Author.** Lead agent, unattended Phase-7 dispatch session 2026-05-27.
**Status.** **Round 2 (revised after first real adversarial wave).** Round 1 returned 3 × `accept-with-named-amendments`. Round-1 decision shape (Option A: per-candidate parallel fanout, 10+2 concurrent subagents, lead-agent exemplar, omnibus PR, 4-token classification) is **preserved**; revised decision in [§Decision (Round 2)](#decision-round-2) folds in: archive file count reconciliation (9 not 8 throughout) + per-file rubric extension to §10 + failure-modes.md enumeration-floor exception; word-budget tier (3500-6500 across two tiers) per auto-006 precedent; patch-threshold disambiguation (≥4 candidates not ≥4 patches); silent-absorption precedence rule for reconciliation; bias-guard mandate expansion to fold Phase-6-followup #1 (BF-L vs U-A/D7-U-1 ADR-0036 framing); 3-tier verdict-menu commitment in reviewer prompts; TL;DR rewrite to structure-not-conclusions; Appendix A scaffold for Round-1 reviewer-return-text preservation; commit-SHA pinning; time-anchored honest-acknowledgement; framework-ADR + per-variant pairing rule for spec patches; PR-webhook handling acknowledgement; skip-discipline auditability for D-1..D-7 defaults; mapping table converted from byte sizes to word counts.
**Rewind point.** This brief's commit on [`claude/phase-7-auto-007-brief`](../../../) (SHAs pinned post-commit: Round 1 was `9c77389` per Round-2 honest-acknowledgement; Round 2 SHA back-filled at commit time). Reverting it returns Phase-7 dispatch to "undecided"; no per-candidate back-fill subagent has fired.

---

## TL;DR (≤200 words)

This brief decides Phase-7's dispatch shape. Phase 7 produces three sub-products: **per-candidate back-fill notes**, **per-candidate spec patches** (conditional on absorbed material), and **a Phase-7-close session handoff**. The brief decides: wave shape (parallel-fanout-with-concurrent-bias-guards vs alternatives); per-candidate notes file rubric (section structure, word-budget tier, classification taxonomy token set); exemplar selection + pre-fanout self-check gate; PR-consolidation unit; aggregation file authorship; bias-guard mandate scope (whether they fold the Phase-6-followup ADR-framing-alignment audit); spec-patch threshold + Phase-7-followup deferral trigger; reviewer-prompt verdict-tier menu; reconciliation precedence when bias-guards disagree with per-candidate verdicts; archive-scope completeness (9 files in scope; D-1..D-7 defaults explicitly skipped); be-generous-to-archive-material bias direction per [`00-brief-v3` OQ-B10](../00-brief-v3.md); audit-trail discipline elements inherited from auto-006 (SHA pinning, time-anchored honest-acknowledgement, Round-1 reviewer-return-text appendix). The Round-2 decision section ([§Decision (Round 2)](#decision-round-2)) names every parameter; Round-1 reviewers' load-bearing amendments are folded in [§Round-2 final amendments folded](#round-2-final-amendments-folded). Round 1's preserved at [§Decision (Round 1 — superseded by Round 2 below)](#decision-round-1--superseded-by-round-2-below).

## The question

Phase 7 of the v3 synthesis produces a per-candidate back-fill audit per the [v1.2 plan § Phase 7](../../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md#phase-7--back-fill-audit-per-candidate-against-archived-v1v2-revised-in-v12). Three sub-products are owed:

- **Per-candidate back-fill notes** — for each of the 10 Phase-6 candidates, an audit of every claim/framing/primitive/recommendation in the archive material, classified per-cell as `absorbed` (and v3 cite location) / `rejected (reason)` / `TBD` (and a 4th token below). Default file shape: per-candidate file × 10 + lead-agent-authored aggregation. Alternative: aggregation-only file at [`backfill-notes.md`](../backfill-notes.md).
- **Per-candidate spec patches** — for any archive material judged absorbable that isn't already in the candidate's Phase-6 spec (surgical §-level amendments only; §0 ADR-citation index preservation per [ADR 0065](../../../docs/adr/0065-section-0-adr-citation-index-table.md)).
- **Phase-7-close session handoff** at `architectures/v3/SESSION-HANDOFF-2026-05-27-phase-7-close.md` unblocking Phase 8 (lean-eval design per candidate).

**Archive scope:** **9 files** total (verified at brief-write time via `ls archive/`). Per-candidate back-fill subagents must enumerate all 9 explicitly. Word counts measured at Round-2 commit (per Reviewer 2 cost-hawk Amendment 4):

| Slot | Dir | File | Words | What it is |
|---|---|---|---|---|
| §2 | [`archive/`](../../../archive/) | [`research-plan.md`](../../../archive/research-plan.md) | 758 | 2026-05-14 pre-v3 "research → action plan" carrying user-stated constraints (already extracted into [`constraints-extracted.md`](../constraints-extracted.md)) + lead-agent recommendations (not extracted; Phase-7 scope) |
| §3 | [`archive/synthesis-v1-v2/`](../../../archive/synthesis-v1-v2/) | [`00-synthesis.md`](../../../archive/synthesis-v1-v2/00-synthesis.md) | 5,020 | Round-1 v2 synthesis post-primary-source-access; canonical entry for F1-F20 |
| §4 | [`archive/synthesis-v1-v2/`](../../../archive/synthesis-v1-v2/) | [`13-round-2-synthesis.md`](../../../archive/synthesis-v1-v2/13-round-2-synthesis.md) | 6,496 | Round-2 synthesis; promoted F21-F33 + Round-2 consensus C10-C16; proposed OpenHands+Overstory substrate stack |
| §5 | [`archive/architectures-v2/`](../../../archive/architectures-v2/) | [`00-comparison.md`](../../../archive/architectures-v2/00-comparison.md) | 3,164 | v2 comparison + decision guide; carried "Compound Atelier baseline" recommendation |
| §6 | [`archive/architectures-v2/`](../../../archive/architectures-v2/) | [`01-specification-refinery.md`](../../../archive/architectures-v2/01-specification-refinery.md) | 3,572 | v2 Architecture 1 — spec-as-product; revelation cycle; 5-mode failure classification |
| §7 | [`archive/architectures-v2/`](../../../archive/architectures-v2/) | [`02-compound-atelier.md`](../../../archive/architectures-v2/02-compound-atelier.md) | 4,515 | v2 Architecture 2 — queue + workpad + persona panel + accumulated `docs/solutions/` |
| §8 | [`archive/architectures-v2/`](../../../archive/architectures-v2/) | [`03-phase-gated-foundry.md`](../../../archive/architectures-v2/03-phase-gated-foundry.md) | 4,610 | v2 Architecture 3 — phase-bound experts, SRS/SAD/DD templates, RTM, gate boards |
| §9 | [`archive/architectures-v2/`](../../../archive/architectures-v2/) | [`04-evolutionary-tournament.md`](../../../archive/architectures-v2/04-evolutionary-tournament.md) | 4,279 | v2 Architecture 4 — genome library, predator agent, tournament bracket, model-family diversity |
| §10 | [`archive/architectures-v2/`](../../../archive/architectures-v2/) | [`failure-modes.md`](../../../archive/architectures-v2/failure-modes.md) | 664 | F1-F20 per-architecture coverage matrix (pre-F21+). **Structurally flat coverage matrix** — see [Reviewer-1 amendment A1 / Round-2 amendment](#round-2-final-amendments-folded) for per-F-mode enumeration-floor exception. |
| | | **Total archive corpus** | **~33,078** | Per-subagent input: candidate spec (~3-5K) + archive (~33K) + brief (~6K) + exemplar (~3.5K) ≈ **~46K words**; comfortably within harness budget per Reviewer 2 cost-hawk audit. |

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
- **Spec patches (Wave 7.3, conditional)**. For any per-candidate absorbed material that isn't reflected in the candidate's Phase-6 spec, lead agent authors a surgical spec patch. Each patch: §-level additive edit (e.g., a new §6 Open carries item; a new §0 ADR-citation index row if an ADR is added; a new §3 methodology shape note). §0 table consistency preserved per [ADR 0065](../../../docs/adr/0065-section-0-adr-citation-index-table.md). **If a patch adds a framework-ADR reference (P-19 / P-28 / P-29 / P-30; ADRs 0028 / 0029 / 0030 / 0036), the candidate's per-variant ADR MUST be added in the same patch** per [`AGENTS-MD-a9fb7b42f8`](../../../AGENTS.md#framework-adr-scope-boundary-discipline) (Reviewer 3 / D12 amendment). Each patch is its own sub-PR OR consolidated into an omnibus per [`AGENTS-MD-d71e845b29`](../../../AGENTS.md#sub-wave-pr-consolidation-when-files-are-disjoint). **Budget threshold (Reviewer 1 A2 + Reviewer 2 A2 disambiguation): the trigger is on candidate count, not patch count. ≤3 *candidates* with any patches in-run; ≥4 *candidates* needing patches triggers Phase-7-followup deferral.** "Needs a patch" = `absorbed-with-adaptation AND the adaptation introduces a new primitive / ADR-cite / methodology-shape not currently in the spec`. Pure rephrasing or de-novo absorption-via-cite does NOT count as needing a patch.
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
- **§1 Overview** (~200 words). Candidate's mandate + axis + entry-mode; one-paragraph statement of the candidate's relationship to the v2 architecture lineage (e.g., "U-A is closest to Architecture 2 Compound Atelier; the audit will be especially careful on Compound-Atelier-specific primitives like persona panels."). **MUST include a one-sentence statement** that the D-1 through D-7 defaults per [`archive/synthesis-v1-v2/ARCHIVE.md`](../../../archive/synthesis-v1-v2/ARCHIVE.md#what-v3-inherits-from-these-syntheses--explicitly) are skipped from the audit because they are already-inherited material (per Reviewer 3 / D15 amendment for skip-discipline auditability).
- **§2-§10 Per-archive-file audits** (one section per archive file; 9 sections total — see [§Archive scope](#the-question) table for §N → file mapping; ~400-600 words each, ~3500-5500 total). For each archive file:
  - **§N.0** File header: `## §N — archive/<path>`
  - **§N.1** Enumeration of claims/framings/primitives/recommendations in the file. Each as a numbered bullet (`§N.1.1`, `§N.1.2`, ...). Source the enumeration from the file's table of contents + section headers + numbered claims; **NOT** a full re-extraction (would blow the word budget). Floor: ≥5 enumeration bullets per archive file. **Exception for `failure-modes.md`** (§10 only): the file is a structurally-flat F1-F20 coverage matrix — treat **each F-mode row as one enumeration unit**; floor is **20**, not 5, for §10 (per Reviewer-1 pre-mortemer A1 amendment).
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
- **§11 Summary** (~200 words). Per-token cell counts; high-confidence cells; surfaced TBDs. (Renumbered from §10 → §11 in Round 2 because the per-archive-file section count is 9 sections at §2-§10.)
- **§12 References** (mandatory; relative paths only per [`AGENTS.md § Internal document references`](../../../AGENTS.md#internal-document-references)). Floor: candidate's spec + all 9 archive files + this brief + the candidate's substrate-requirements summary + any ADRs the audit cites. (Renumbered from §11 → §12 in Round 2.)

**Classification taxonomy (4 tokens, lead-agent proposal — Round-1 reviewers should challenge).**

| Token | Semantics |
|---|---|
| `absorbed` | The candidate's spec carries the archive item in some form. Cite v3 location (spec section + ADR if applicable). The archive item's wording may differ; what matters is the concept is realized. |
| `rejected (reason)` | The candidate deliberately did not carry the archive item. Reason cited (e.g., "Architecture-4-tournament-specific; this candidate is greenfield-S"). |
| `not-applicable-to-candidate-mandate` | The archive item is structurally inapplicable to this candidate's mandate/axis/entry-mode. **Distinct from `rejected`:** rejected implies a deliberate choice (could have absorbed but chose not to); not-applicable implies "this token never even applied." Example: a brownfield-specific Compound-Atelier primitive being audited against GF-S — N/A, not rejected. |
| `tbd` | Lead agent and silent-absorption auditor should reconcile at aggregation time. Use sparingly — TBDs require lead-agent follow-up subagent dispatch. |

**Self-check rubric** per [`AGENTS-MD-e74e4811a2`](../../../AGENTS.md#self-check-rubric-requires-tool-verification-for-measurable-items). Subagent runs:

- (a) `wc -w` on its notes file to verify word budget compliance against the candidate's tier (see word-budget tier table below; per Reviewer 2 cost-hawk Amendment 1).
- (b) `ls` on every cited v3 file path (`specs/<id>.md`, any ADR files) to verify the file exists.
- (c) `grep` for §1-§12 headers + §N.0 file-header pattern for each archive file to verify section structure (9 §N.0 headers expected across §2-§10).
- (d) `grep -E '^\| §[0-9]+\.1\.[0-9]+' <file>` to verify ≥5 enumeration rows in each §N.2 table per archive file. **Exception for §10 (failure-modes.md)**: floor is 20, not 5, per Round-2 amendment.
- (e) `grep -cE '\| absorbed \|'` etc. to verify YAML frontmatter cell-counts match table-row counts.
- (f) For each binding rule table cited in the notes file, `grep -F '<verbatim cell text>' <source-anchor>` to verify exact-text-pull per [`AGENTS-MD-bf4431be57`](../../../AGENTS.md#verbatim-text-pull-when-citing-binding-rule-tables); report exit code in digest. **If the notes file cites no binding rule tables, item (f) self-reports `n/a` with rationale.** (Per Reviewer 3 / D6 amendment.)
- (g) `grep -c "tbd"` on the file — surfaced TBDs reported in return digest.

**Word budget per notes file (tiered per Reviewer 2 cost-hawk Amendment 1; mirrors auto-006 tier discipline).** Section budgets sum to ~4200-6000 baseline:

| Tier | Word budget | Candidates | Rationale |
|---|---|---|---|
| Light | 3500-5000 | GF-S, GF-M, GF-C, BF-S | Single dominant v2-architecture-lineage; smaller absorption surface |
| Heavy | 4500-6500 | BF-M, BF-L, U-A, U-B, U-C, D7-U-1 | Multiple v2-architecture-lineage overlaps; larger absorption surface; brownfield + unified-attempt candidates carry more cross-lineage cells |

(Tier boundaries calibrated on auto-006 precedent. Subagent runs `wc -w` against its tier's bounds in self-check item (a); over-budget triggers a return-digest flag for lead-agent review.)

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

## Decision (Round 1 — superseded by Round 2 below)

~~**Option A. Per-candidate parallel fanout, 10 subagents in one wave + 2 bias-guard subagents concurrent, lead-agent exemplar first, omnibus PR, lead-agent aggregation.**~~ Round 1 **preserved as decision shape but superseded with amendments**. All three Round-1 reviewers returned `accept-with-named-amendments`; Option A's dispatch shape survives, but the per-archive-file count, word-budget tier, patch-threshold semantics, reconciliation precedence, bias-guard mandate scope, and audit-trail discipline are all amended. See [§Decision (Round 2)](#decision-round-2). Round-1 text preserved below for traceability per [`AGENTS-MD-bb7fe2c5aa`](../../../AGENTS.md#round-1-strikethrough-preservation-in-decision-briefs).

### Round 1 reasoning (preserved)

~~Concretely:~~

- ~~**Lead-agent inline: exemplar back-fill notes** for the least-contested candidate (TBD at exemplar-authoring time — candidate set is {GF-M, BF-S}; lead agent picks based on which produces the cleanest cell-classification demonstrations across all 8 archive files). ~3500-word target. Authored using the rubric below. Committed as PR 3.~~
- ~~**Wave 7.1 (all 10 in parallel)** fires after the exemplar lands. 9 spec-authoring back-fill subagents (10 minus exemplar candidate).~~
- ~~**Wave 7.2 (2 bias-guards in parallel)** fires concurrent with Wave 7.1 (independent input streams).~~
- ~~**Aggregation step**: lead-agent authors `backfill-notes.md` aggregation file at fanout-close.~~
- ~~**Wave 7.3 (conditional spec patches)**: surgical §-level edits for absorbed material; ≤3 in-run; ≥4 triggers deferral.~~

~~**Total subagents this run:** 9 (back-fill, excluding exemplar candidate) + 2 (bias-guards) = **11 back-fill-equivalent dispatches**, plus 6 adversarial reviewers across this brief's two rounds = **17 subagents total for Phase 7**.~~

~~**PR-cap math (Round-1 estimate, omnibus consolidation):** 1 (scope envelope, PR #187 already opened) + 1 (this brief R2) + 1 (exemplar) + 1 (omnibus: 9 back-fill + 2 bias-guards + 1 aggregation) + ≤1 (conditional spec patches, possibly omnibus if multiple) + 1 (handoff) + 1 (summary) + 1 (retro) = **7-8 PRs against ≤15 Phase-7 budget cap**, comfortable 7-8 PR margin.~~

### Round-1 reasoning (preserved for traceability)

Three drivers selected Option A in Round 1:

1. **The Phase-6 precedent worked cleanly with the same shape** — per-candidate parallel fanout + lead-agent exemplar + uniform rubric + omnibus PR consolidation (post-collapse). The 9-spec Phase-6 omnibus PR validated the omnibus pattern at ~9 disjoint files; Phase-7's 12-file omnibus is a similar shape. Reusing the precedent exploits already-calibrated patterns.
2. **Bias-guards-concurrent is free.** The silent-absorption auditor and historian have independent input streams (they read archive + Phase-6 specs, NOT per-candidate back-fill files). Running them concurrent with Wave 7.1 saves a full fanout wall-clock without any quality loss. The aggregation-time reconciliation step is the natural place to surface any per-candidate-vs-auditor disagreements.
3. **The 4-token taxonomy resolves the not-applicable-vs-rejected ambiguity** that would otherwise emerge per-candidate. Without the `not-applicable-to-candidate-mandate` token, every Architecture-4-tournament-specific item being audited against, say, BF-S would be classified `rejected (mandate-mismatch)`, which conflates two different verdicts: "deliberate choice not to absorb" vs "structurally inapplicable." The 4-token taxonomy gives auditors a clean separator that downstream Phase-8 lean-eval design can use to identify cross-mandate inheritance candidates separately from cross-mandate exclusions.

## Decision (Round 2)

**Option A′. Per-candidate parallel fanout, 10 back-fill subagents + 2 bias-guard subagents concurrent in one wave, lead-agent exemplar first with self-check gate, omnibus PR, tiered word-budget (Light 3500-5000 / Heavy 4500-6500), 4-token classification taxonomy with silent-absorption-precedence reconciliation rule, expanded bias-guard mandates folding Phase-6-followup #1, candidate-count-based patch threshold, Appendix A scaffolding, audit-trail polish per auto-006 precedent inheritance.**

Concretely (Round-2 amended Decision):

- **Lead-agent inline: exemplar back-fill notes** for the least-contested candidate. Candidate set: **{GF-M, BF-S}** (Light tier). Lead agent picks at exemplar-authoring time based on which produces the cleanest cell-classification demonstrations across all 9 archive files (i.e., the candidate whose lineage to one of Architectures 1-4 is least ambiguous, giving the cleanest §1 lineage-statement model). ~4000-word target (mid-Light-tier). Committed as PR 3.
- **Wave 7.1 (all 10 in parallel)** fires after the exemplar lands. 9 spec-authoring back-fill subagents (10 minus exemplar candidate). Each writes its candidate's notes file at `architectures/v3/backfill-notes/<candidate-id>.md`. Returns ≤500-word digest.
- **Wave 7.2 (2 bias-guards in parallel)** fires concurrent with Wave 7.1.
  - **Silent-absorption auditor.** Reads all 10 Phase-6 specs + the 9 archive files. Flags spec content that looks like archive material without explicit citation. **Expanded mandate (Reviewer 2 cost-hawk Amendment 3):** also folds the Phase-6-followup carry-forward #1 — the BF-L "commodity dispatch surface" vs U-A/D7-U-1 "registrar-framework" framing of ADR 0036, per [Phase-6-close verifier Finding-2](../SESSION-HANDOFF-2026-05-26-phase-6-close.md#what-phase-6-closed-looks-like-verification-of-close-conditions). Output: `architectures/v3/backfill-notes/audit-silent-absorption.md`. Word budget: ≤2500 (~500 extra for the ADR-0036 framing audit).
  - **Historian.** Reads all 10 Phase-6 specs + the 9 archive files. Enumerates archive items appearing in zero Phase-6 specs in any form. Output: `architectures/v3/backfill-notes/audit-historian.md`. Word budget: ≤2000.
- **Aggregation step**: lead-agent authors `backfill-notes.md` aggregation file at fanout-close. **Reconciliation precedence rule** (Reviewer 1 pre-mortemer Amendment A3 — load-bearing):
  > **Silent-absorption auditor's `silently-absorbed` finding overrides any per-candidate `rejected` verdict on the same cell**; the aggregation cell is downgraded to `absorbed (silently, flagged for Phase-8 cite)`. Per-candidate `not-applicable-to-candidate-mandate` is NEVER overridden by historian or silent-absorption findings (the not-applicable verdict reflects structural mandate-mismatch that auditors cannot re-litigate). For `tbd` cells, the silent-absorption auditor's verdict is folded in if available; otherwise the cell remains `tbd` and surfaces in the morning summary's review items.
- **Wave 7.3 (conditional spec patches)**: surgical §-level edits for absorbed material per the Round-2 rubric (framework-ADR + per-variant pairing per [`AGENTS-MD-a9fb7b42f8`](../../../AGENTS.md#framework-adr-scope-boundary-discipline)). **Threshold (Reviewer 1 A2 + Reviewer 2 A2): on candidate count, not patch count.** ≤3 *candidates* with any patches in-run; ≥4 *candidates* needing patches triggers Phase-7-followup deferral. "Needs a patch" defined verbatim in [§A Per-candidate fanout rubric](#a-per-candidate-parallel-fanout-10-subagents-in-one-wave-lead-agent-exemplar-first-omnibus-pr-concurrent-bias-guards--lead-agent-recommendation) above.

**Total subagents this run (Round-2 revised per Reviewer 2 cost-hawk):** 9 (back-fill, excluding exemplar candidate) + 2 (bias-guards) = 11 back-fill-equivalent dispatches + 6 adversarial reviewers (Round 1 + Round 2) + 1 spec-patch authorer (if conditional patches fire) + ~3-4 retrospective-package authoring subagents at run close (SKILL-SPEC / ADR-draft / per-rule AGENTS-MD subagents per the autonomous-run skill end-of-run protocol) = **~21 subagents total for Phase 7** (~17 was the Round-1 undercount).

**PR-cap math (Round-2 revised per Reviewer 2 cost-hawk):** 1 (scope envelope #187, already opened) + 1 (this brief R2) + 1 (exemplar) + 1 (omnibus: 9 back-fill + 2 bias-guards + 1 aggregation) + ≤1 (conditional spec patches, omnibus if multiple) + 1 (handoff) + 1 (summary+retro combined or 2 if separate) = **6-7 PRs against ≤15 Phase-7 budget cap** (Reviewer 2 noted Round-1 double-counting; PR-cap margin is **8-9 PRs**, not 7-8).

### Round-2 reasoning

Three drivers selected Option A′ over Round 1's Option A:

1. **Archive file count reconciliation eliminates the failure-modes.md off-by-one collision.** Round-1 prose said "8 substantive" but the table had 9; the §2-§9 rubric covered only 8 sections; self-check (d) ≥5 enumeration rows would fail on the structurally-flat failure-modes.md coverage matrix. The Round-2 fix (§2-§10, 9 sections, failure-modes.md floor=20 exception) makes the rubric mechanically applicable to all 9 archive files; Reviewer 1's pre-mortemer "most-likely failure path" no longer fires.
2. **Reconciliation precedence rule prevents aggregation-time deadlock.** Without the explicit precedence rule (silent-absorption > per-candidate `rejected`; per-candidate `not-applicable` is never overridden), the lead agent at fanout-close faces an underspecified adjudication on every disagreement cell. The Round-2 rule converts what would have been ad-hoc lead-agent decisions into a mechanical rule that downstream Phase-8 lean-eval design can audit.
3. **Bias-guard mandate expansion folds Phase-6-followup #1 at zero PR cost.** The silent-absorption auditor is already reading all 10 specs + the archive; adding the ADR-0036 framing-alignment check to its scope costs ~500 words of output and zero additional subagents. The carry-forward from Phase 6 lands in this run instead of being deferred to Phase 8 — opportunistic, not in-scope creep.

The tiered word budget (3500-5000 / 4500-6500) honors the realistic ~4200-6000 floor that Reviewer 2 calculated, with the auto-006 tiering precedent applied. The "needs a patch" definition resolves the bias-direction-inflates-patch-count failure path Reviewer 1 surfaced.

### Round-2 final amendments folded

The Round-2 decision (Option A′) stands. Following amendments are folded:

| Amendment | Source | Status |
|---|---|---|
| Archive file count 8→9 throughout + §2-§10 rubric + failure-modes.md floor=20 exception | Reviewer 1 A1 | **load-bearing** — folded inline above |
| Patch threshold defined as candidate-count not patch-count; "needs a patch" definition | Reviewers 1 A2 + 2 A2 | **load-bearing** — folded inline above |
| Silent-absorption precedence rule for cell reconciliation | Reviewer 1 A3 | **load-bearing** — folded inline above |
| Word-budget tier (3500-5000 / 4500-6500) | Reviewer 2 A1 | **load-bearing** — folded inline above |
| Silent-absorption auditor mandate expansion to fold Phase-6-followup #1 | Reviewer 2 A3 | **load-bearing** — folded inline above |
| Mapping table converted from byte sizes to word counts | Reviewer 2 A4 | **load-bearing** — folded into [§Archive scope table](#the-question) |
| 3-tier verdict menu commitment in reviewer prompts | Reviewer 3 D2 | **load-bearing** — see [§Adversarial review discipline commitment](#adversarial-review-discipline-commitment) below |
| TL;DR rewrite to structure-not-conclusions | Reviewer 3 D3 | **load-bearing** — TL;DR rewritten above |
| Appendix A scaffold for Round-1 reviewer return text | Reviewer 3 D5 | **load-bearing** — see [§Appendix A](#appendix-a--round-1-reviewer-return-digests) below |
| Self-check item (f) made unconditional with `n/a` fallback | Reviewer 3 D6 | **load-bearing** — folded inline above |
| Framework-ADR + per-variant pairing rule for spec patches | Reviewer 3 D12 | **load-bearing** — folded into Wave 7.3 above |
| PR-webhook handling acknowledgement for PR #187 | Reviewer 3 D14 | **load-bearing** — see [§PR-webhook handling commitment](#pr-webhook-handling-commitment) below |
| Skip-discipline auditability for D-1..D-7 defaults in §1 | Reviewer 3 D15 | **load-bearing** — folded into §1 rubric above |
| Round-1 SHA pinning annotation | Reviewer 3 D1 | **load-bearing** — folded into header above |
| Rewind-point SHA pinning | Reviewer 3 D8 | **load-bearing** — folded into header above |
| Time-anchored honest-acknowledgement git log | Reviewer 3 D9 | **load-bearing** — see [§Honest acknowledgements (Round 2)](#honest-acknowledgements-round-2) below |

Non-load-bearing amendments folded:
- Reviewer 3 D7: classification taxonomy table is guidance, not binding; subagents may paraphrase token semantics. No amendment needed but flagged in [§Glossary](#glossary).

Amendments rejected with reason:
- Reviewer 2 alternative: sub-fan the historian 9 ways per archive file. **Rejected** — historian's value is cross-file pattern detection ("appears in zero specs in any form" requires holding all 9 files in one head). Sub-fanning would lose the load-bearing property.

### Adversarial review discipline commitment

Per [`AGENTS-MD-8a7029647f`](../../../AGENTS.md#adversarial-review-verdict-tiers): each adversarial reviewer dispatch brief (Round 1 + Round 2) explicitly offers the **3-tier verdict menu** (`accept-as-is` / `accept-with-named-amendments` / `reject-with-counter-proposal`). Round-1 dispatch briefs (already fired) offered all three tiers — see Appendix A reviewer-return text where each verdict is one of the three. Round-2 dispatch briefs likewise offer the menu.

### PR-webhook handling commitment

Per [`AGENTS-MD-c5a92e6017`](../../../AGENTS.md#pr-webhook-merged-is-advisory-not-authoritative): any `merged` webhook event arriving for any Phase-7 PR (#187 scope envelope, or any subsequent Phase-7 PR) MUST be verified via `mcp__github__pull_request_read` (method `get`) before the lead agent acts on the notification. The verification costs one API roundtrip and prevents the lead agent from re-creating PRs that already exist or skipping PRs that did not actually merge.

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

## Honest acknowledgements (Round 2)

Per [`AGENTS-MD-ffe35aa500`](../../../AGENTS.md#honest-acknowledgements-for-pre-round-2-wave-firing) (pre-Round-2 wave firing): no Phase-7 back-fill subagent has fired pre-Round-2; this dispatch brief precedes the wave dispatch.

This brief lives at commit **`e1ca9b4`** on [`claude/phase-7-auto-007-brief`](../../../) (Round 2 commit; Round 1 was **`9c77389`** at authordate 2026-05-27).

Mechanical verifiability (time-anchored per Reviewer 3 / D9 amendment): a later auditor can reproduce the no-back-fill-subagent-fired claim by running, from this brief's Round-2 commit:

```bash
git ls-tree <Round-2-SHA> -- architectures/v3/backfill-notes/ 2>/dev/null  # empty (directory does not yet exist)
git ls-tree <Round-2-SHA> -- architectures/v3/backfill-notes.md 2>/dev/null  # empty (file does not yet exist)
git log --all --oneline --before=<Round-2-authordate> -- architectures/v3/backfill-notes/  # empty
```

**Process-bug carry-forward.** Pre-flight verification per [`AGENTS-MD-4f8c2a1b03`](../../../AGENTS.md#pre-flight-prior-phase-merge-state-verification) passed at session start — all 10 Phase-6 specs + handoff + mandate-fit matrix + verification findings confirmed in `origin/main` before this brief was authored. Verifiable: see [scope envelope pre-flight section](../scope-envelope-phase-7.md#pre-flight-verification-per-agents-md-4f8c2a1b03).

## Round-2 if-user-overrides rewind point

This brief's Round-2 commit on `claude/phase-7-auto-007-brief` (SHA back-filled at commit time). Revert to undo the Round-2 framing; no back-fill subagent has fired. Reverting all the way back to before Round 1 returns Phase-7 dispatch to "undecided"; see Round-1 rewind point below for the Round-1-only revert.

## Open questions for the Round-2 adversarial reviewers to challenge

These are the Round-2-specific challenges (Round-1 reviewers' questions were folded into amendments above):

1. **Round-2 amendment density.** 17 named amendments folded in one Round-2 pass — is this too dense? Did any amendment introduce a new defect (e.g., the silent-absorption precedence rule creates a new failure mode where the auditor's confidence threshold isn't specified)?
2. **Reconciliation precedence asymmetry.** Silent-absorption auditor overrides per-candidate `rejected`; per-candidate `not-applicable` is never overridden. Is this asymmetry correct? Or should `not-applicable` also be overridable by an auditor with sufficient evidence?
3. **Failure-modes.md floor=20 exception.** Round-2 fix makes per-F-mode enumeration mandatory; floor 20 = enumerate all 20 F-modes. Is this too rigid (what if the auditor judges only 8 F-modes load-bearing for this candidate) or too loose (no quality bar on the per-F-mode classification)?
4. **Word-budget Heavy tier 4500-6500.** Six candidates in Heavy tier. Is the band wide enough that the budget becomes non-binding? Should there be a finer split (e.g., 4500-5500 for U-A/U-B; 5500-6500 for BF-L/D7-U-1)?
5. **Bias-guard mandate expansion (Phase-6-followup #1 fold).** Reviewer 2 A3 amendment expands silent-absorption auditor's scope. Does this overload the auditor? Should the ADR-0036 framing audit be a separate (third) bias-guard subagent instead?
6. **"Needs a patch" definition narrowness.** Round-2 rule: `absorbed-with-adaptation AND adaptation introduces a new primitive / ADR-cite / methodology-shape`. Does this miss legitimate patches (e.g., a §5 mandate-fit rationale clarification that doesn't add an ADR but is still load-bearing)?
7. **Appendix A verbatim text.** Three reviewer return texts preserved verbatim totaling ~2500 words. Does the brief's audit trail need the full text, or would per-reviewer ≤200-word summaries suffice?
8. **Phase-6-followup #3 (Phase-5-close handoff erratum sweep) not folded.** Phase-6-close handoff carried 3 carry-forwards; this brief folds #1 (ADR-0036 framing) but not #2 (cross-spec characterization audit — Reviewer 2 noted it could fold but the brief left it as optional) or #3 (Phase-5-close handoff erratum sweep). Should any of those also fold?
9. **Pre-author-everything-in-the-brief convergent pattern.** Reviewer 3 noted that Round-1 defects D1-D9 directly repeat auto-006 Reviewer 6 findings. Should the lead agent author a SKILL-SPEC for "audit-trail-discipline inheritance from prior auto-NNN briefs"? Or is this overhead?
10. **Round-1 "Open questions" still present.** This brief preserves Round-1 OQs as historical context (per [§Open questions for the Round-1 adversarial reviewers to challenge](#open-questions-for-the-round-1-adversarial-reviewers-to-challenge) below). Should they be marked `[resolved]` cell-by-cell, or is preservation sufficient?

(Round-2 reviewers will challenge any/all of these + anything else they find.)

## Open questions for the Round-1 adversarial reviewers to challenge (historical context — Round 1 closed)

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

Three real subagents dispatched per [`AGENTS.md § Adversarial review MUST be real subagents`](../../../AGENTS.md#adversarial-review-must-be-real-subagents). Each was offered the 3-tier verdict menu (`accept-as-is` / `accept-with-named-amendments` / `reject-with-counter-proposal`) per [`AGENTS-MD-8a7029647f`](../../../AGENTS.md#adversarial-review-verdict-tiers). Verbatim reviewer return text preserved at [§Appendix A](#appendix-a--round-1-reviewer-return-digests).

### Reviewer 1 — pre-mortemer (`accept-with-named-amendments`)

- **Most-likely failure path: archive file count "8 vs 9" off-by-one collides with self-check (d) ≥5 enumeration rows + the structurally-flat failure-modes.md coverage matrix.** Exemplar author hits item (d) on the failure-modes addendum (5KB / one structural unit / ≥5 floor) and either fabricates fake claims (contaminating calibration) or stalls. The be-generous bias direction makes silent absorption of phantom F-mode rows worse — up to 200 phantom-absorbed cells downstream.
- **Secondary failures: (2a) Wave 7.3 spec-patch budget collapses because be-generous bias systematically inflates `absorbed (with adaptation)` and "needs a patch" is never defined. (2b) Bias-guard reconciliation deadlock at aggregation — no rule for which verdict wins when silent-absorption auditor disagrees with per-candidate `rejected`; lead agent either invents ad-hoc rule (drift) or punts to `tbd` (defeats discipline).**
- **Amendments (3):** A1 archive file count reconciliation + §2-§10 rubric + failure-modes.md floor=20 exception; A2 "needs a patch" definition + patch-threshold rubric; A3 reconciliation precedence rule (silent-absorption overrides per-candidate `rejected`; per-candidate `not-applicable` never overridden).

### Reviewer 2 — cost/scope hawk (`accept-with-named-amendments`)

- **Per-subagent context budget over-estimated (not under).** Real archive corpus: **~33K words** (not ~250 KB / ~40K words as brief implied — file sizes are bytes, largest file is 6.5K words). Per-subagent input ~46K words; comfortable.
- **Per-notes-file word budget under-estimated.** Section budgets sum to ~4200-6000 baseline; brief's 3000-5500 under-shoots on bottom and clips at top. Tier per auto-006 precedent: ≤6500 for U-A/BF-L/D7-U-1 (cross-lineage); ≤5000 for GF-S/GF-M/GF-C/BF-S (single-lineage).
- **PR-cap math.** Real margin is 8-9 PRs, not 7-8 (brief double-counted PR #187 envelope + miscounted retro+summary). **Patch threshold ambiguous**: "≤3 patches" vs "≥4 candidates" — pick one. Recommend candidate-count.
- **Subagent count miscount.** Brief said 17; real ~21 (missed retrospective-package subagents per autonomous-run end-of-run protocol).
- **12-concurrent-subagent wave** — acceptable (3-subagent margin to ~15 practical limit). No amendment.
- **Bias-guard sub-fanning rejected** — historian's value is cross-file pattern detection requiring all 9 files in one head; sub-fanning loses load-bearing property.
- **Amendments (4):** A1 raise word budget to tiered 3500-5000 (Light) / 4500-6500 (Heavy); A2 patch threshold = candidate count not patch count; A3 expand silent-absorption auditor mandate to fold Phase-6-followup #1 (BF-L vs U-A/D7-U-1 ADR-0036 framing); A4 mapping table to show word counts not byte sizes.

### Reviewer 3 — regulator / audit-trail (`accept-with-named-amendments`)

15 audit-trail dimensions audited; 9 defects identified + 6 passes.

- **D1 SHA-pinning placeholder acceptable but needs explicit annotation.**
- **D2 3-tier verdict menu** not promised in brief text (was offered in dispatch briefs, but brief should state this).
- **D3 TL;DR fails structure-not-conclusions test** ≥3 lines (specific conclusions: "10 subagents", "two bias-guards", "≤500-word digests").
- **D5 Round-1 reviewer-return-text Appendix A scaffolding missing.**
- **D6 Self-check item (f) conditional and underspecified** — when is verbatim text-pull triggered?
- **D8 Rewind-point pinning defect inherited from auto-006** — branches named, SHAs not pinned.
- **D9 Honest-acknowledgement git log not time-anchored** — `git log` would return non-empty post-Wave-7.1, defeating the verifiability claim.
- **D12 Framework-ADR + per-variant pairing rule missing from Wave 7.3 spec-patch instructions.**
- **D14 PR-webhook handling rule** (newly-adopted AGENTS-MD-c5a92e6017) not acknowledged for PR #187 monitoring.
- **D15 Skip discipline for D-1..D-7 defaults** not auditable — subagents should explicitly state in §1 that defaults are skipped.

Passing items: D4 deferral triple-bind ✓, D10 sub-wave coordination ✓, D11 §0 ADR-citation index preservation ✓ (modulo D12), D13 mapping table ✓ (modulo Reviewer 2 A4 byte-size→word-count swap).

Note from reviewer: defects D1, D2, D3, D5, D8, D9 directly repeat auto-006 Reviewer 6 findings — should have been pre-folded as inherited precedent (process bug, not blocker).

**Amendments (10):** D1 SHA-pinning annotation; D2 3-tier menu commitment; D3 TL;DR rewrite; D5 Appendix A scaffold; D6 self-check (f) made unconditional with `n/a` fallback; D8 + D9 SHA-pinning and time-anchored git log; D12 framework-ADR pairing in patches; D14 PR-webhook handling commitment; D15 skip-discipline auditability in §1.

### Convergence

All three reviewers returned `accept-with-named-amendments` — no `reject-with-counter-proposal`. The dispatch shape (per-candidate parallel fanout + bias guards concurrent + omnibus PR) is correct; load-bearing amendments are at the rubric (Reviewer 1 archive count + Reviewer 2 word budget), reconciliation discipline (Reviewer 1 precedence), bias-guard scope (Reviewer 2 mandate expansion), and audit-trail discipline (Reviewer 3 inherits from auto-006).

**Convergent observation across reviewers:** all three flagged places where the brief deferred to runtime ("trivially short" exception, "needs a patch" definition, reconciliation tie-breaking, conditional self-check). The convergent amendment is **pre-author every runtime decision in the brief** — same pattern as auto-006 Round 2's "pre-author-everything-in-the-brief" convergence.

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

## Appendix A — Round-1 reviewer return digests

(Per [Reviewer 3 / D5 amendment](#round-2-final-amendments-folded). Preserved verbatim from the three Round-1 subagent returns. Verdicts confirmed via the 3-tier menu offered per [`AGENTS-MD-8a7029647f`](../../../AGENTS.md#adversarial-review-verdict-tiers).)

### Round-1 Reviewer 1 — pre-mortemer (verdict: `accept-with-named-amendments`)

**Most-likely failure path: "9-vs-8 archive file" off-by-one collides with self-check item (d) and blocks fanout indefinitely (or worse, ships inconsistent notes).**

Causal chain:
- The brief's prose says "**8 substantive files**" (TL;DR, §The question paragraph 6, and the parenthetical at line 35 which then admits it's actually 9).
- The YAML frontmatter at lines 71-80 enumerates **9** entries (`archive-files-audited` includes `failure-modes.md`).
- The per-archive-file rubric (§N.0..§N.3) is keyed to **§2-§9** = 8 sections (line 88: "§2-§9 Per-archive-file audits"), but the path mapping table (line 250) introduces a 9th slot labelled "§(addendum)" with no rubric for what `§(addendum).1` enumeration rows must look like.
- Self-check item (d) demands `≥5 enumeration rows per archive file unless trivially short` — and `failure-modes.md` (which I read: 5 KB, one coverage matrix table + 4 score rows) has effectively **one** enumerable structural unit (the F1-F20 matrix). It is not "trivially short" by word count; it is structurally flat.
- Exemplar author hits (d) on the failure-modes addendum: either (i) inflates 5 fake "claims" out of a coverage matrix, contaminating the exemplar's calibration, (ii) marks it "trivially short" — but the brief reserves that escape only for "trivially short" files, and 5KB isn't obviously trivially-short, or (iii) blocks per the load-bearing gate at line 215, stalling the run while the lead agent re-authors the brief.

The fanout then either fires off an exemplar that the 9 sibling subagents copy with fabricated enumeration rows for `failure-modes.md`, *or* it stalls. The "be-generous-to-archive" bias direction makes (i) worse: each F1-F20 row absorbed by lineage proximity inflates `absorbed` counts in 10 candidates × 20 F-modes = up to 200 phantom-absorbed cells that downstream Phase-8 lean-eval treats as binding inputs.

**Secondary failures (2):**

**(2a) Wave 7.3 spec-patch budget collapse.** Brief sets `≤3 in-run; ≥4 triggers deferral`, but the be-generous bias direction systematically inflates `absorbed (with adaptation)` verdicts. "With adaptation" implies the candidate's spec doesn't *quite* carry it as-is — i.e., a patch. With 10 candidates × 9 archive files × be-generous default on close calls, the probability that ≥4 candidates surface ≥1 patchable absorption is high. The Phase-7-followup deferral fires immediately on first run, defeating the in-run patch path. Worse: brief never specifies what counts as "needs a patch" vs "absorbed-as-is" — each subagent decides independently.

**(2b) Bias-guard reconciliation deadlock.** Silent-absorption auditor runs concurrent reading only Phase-6 specs + archive. It will produce findings keyed to "spec §X looks like archive item Y." Per-candidate subagents will independently classify the same cells `rejected` or `not-applicable`. Aggregation-time reconciliation is described in one sentence ("a reconciliation row") with no rule for which verdict wins. Lead agent at aggregation faces 10-50 reconciliation rows with no adjudication rubric and either invents one ad-hoc (drift) or punts every conflict to `tbd` (defeating the 4-token discipline).

**Amendments:** A1 archive file count reconciliation (8→9 throughout, §2-§10 rubric, failure-modes.md per-F-mode floor=20 exception); A2 patch threshold rubric defining "needs a patch" = absorbed-with-adaptation introducing new primitive/ADR-cite/methodology-shape; A3 reconciliation precedence rule (silent-absorption overrides per-candidate `rejected`; per-candidate `not-applicable` never overridden).

### Round-1 Reviewer 2 — cost/scope hawk (verdict: `accept-with-named-amendments`)

**Per-subagent context budget over-estimated (not under).** The brief implicitly treats the 9 archive files as ~250 KB / ~40K words (§Common archive-file-to-path mapping shows the byte sizes). **Actual word counts:** research-plan.md 758 + 00-synthesis.md 5020 + 13-round-2-synthesis.md 6496 + 00-comparison.md 3164 + 01-specification-refinery.md 3572 + 02-compound-atelier.md 4515 + 03-phase-gated-foundry.md 4610 + 04-evolutionary-tournament.md 4279 + failure-modes.md 664 = **~33,078 total**.

Per-subagent input: candidate spec (~3-4.7K) + archive (~33K) + brief (~4.8K) + exemplar (~3.5K) ≈ **~45K words**. Well within harness budget.

**Per-notes-file word budget under-estimated.** OQ-5 already flagged 4000-5800 realistic vs 3000-5500 budgeted. But §N rubric mandates "one section per archive file × 9 files × 400-600 words = 3600-5400" plus §1 (~150) + §10 (~200) + §11 references + YAML. Realistic floor is ~4200; realistic ceiling is ~6000. Budget under-shoots on the bottom and clips at the top.

**Amendment 1:** Raise word budget to **3500-6500** (not 3000-5500). Tier per auto-006 precedent: ≤6500 for U-A / BF-L / D7-U-1 (4-architecture-lineage overlaps); ≤5000 for GF-S/GF-M/GF-C/BF-S (single-lineage candidates).

**PR-cap math.** Brief claims 7-8 PRs. Recount: scope envelope (#187, **already opened — DOUBLE-COUNTED if both this brief and envelope claim PR #1**) + this brief R2 + exemplar + omnibus fanout + ≤1 conditional spec patches + handoff + summary/retro = **6-7 PRs**, not 7-8. Brief's auto-006 precedent collapsed 12-13 → 6 PRs; same dynamic here. **Margin is genuinely 8-9 PRs, not 7-8.** Comfortable.

But: the **spec-patch threshold of ≥4 candidates → deferral** is ambiguous. If 3 candidates need 2 patches each (= 6 patches), the threshold doesn't fire and the omnibus carries 6 commits. The brief says "≤3 spec patches in-run" once (Alt A) and "≥4 candidates" elsewhere (§Phase-7-followup).

**Amendment 2:** Resolve threshold to be on **candidate count, not patch count** (≥4 *candidates* needing any patch → defer); make this verbatim in §Phase-7-followup binding mechanism.

**Subagent count.** Brief: 11 back-fill-equivalent + 6 reviewers = 17. **Missed:** retrospective-package subagents (per autonomous-run skill end-of-run protocol — typically 3-4 sub-dispatches for SKILL-SPEC / ADR-draft / AGENTS-MD authoring + the omnibus retro report). Real total: **~21**. Not a blocker, but the scope envelope's "~20" is more honest than the brief's "17."

**12-concurrent-subagent wave.** Brief acknowledges 12 vs ~15 practical limit (3-subagent margin). Phase-6 ran 9 in parallel cleanly. Brief is correctly conservative; no amendment.

**Bias-guard sub-scoping.** Each bias guard reads 10 specs (~38K words) + 9 archive files (~33K words) ≈ **~71K words**, then produces ~2K-word verdict. This is heavy but doable for one fresh-context subagent. Sub-fanning the historian 9 ways (one per archive file) would **lose the cross-file pattern detection** that's the historian's actual purpose ("appears in zero specs in any form" requires holding all 9 files in one head). Silent-absorption is similar. **Do NOT split.** No amendment.

**Wall-clock + absorbing Phase-6-followup #2.** 3-5 hours scope-envelope estimate is realistic given Phase-6's similar shape ran in one autonomous-run session. **Cross-spec characterization audit (Phase-6-followup #2)** could fold into the silent-absorption auditor's mandate without a separate subagent (already reading all 10 specs + archive).

**Amendment 3:** Expand silent-absorption auditor's mandate to **also** flag the BF-L vs U-A/D7-U-1 ADR-0036 framing divergence (Phase-6-followup carry-forward #1). Zero PR cost, +~500 words to that auditor's output.

**Amendment 4:** Tighten the brief's §Common archive-file-to-path mapping table to show **word counts, not byte sizes** (more relevant for context budget reasoning).

### Round-1 Reviewer 3 — regulator / audit-trail (verdict: `accept-with-named-amendments`)

15 dimensions audited; 9 defects identified + 6 passes:

- **D1. Round-1 commit SHA placeholder is acceptable but the back-reference path is**. Pre-pinning is structurally impossible; auto-006 precedent pins Round-1 SHA *retrospectively at Round-2 commit time*. **Amendment:** add annotation that placeholder is deliberate-and-load-bearing, not forgotten.
- **D2. 3-tier verdict menu not promised to reviewers.** §Round-1 reviewer findings cites the real-subagents rule but does NOT state the 3-tier menu will be offered. **Amendment:** add one sentence: "Each reviewer brief explicitly offers the 3-tier menu per AGENTS-MD-8a7029647f."
- **D3. TL;DR fails structure-not-conclusions test on ≥3 lines.** TL;DR contains specific conclusions: "(10 subagents, one per Phase-6 spec)", "two bias-guard subagents... fire concurrent", "≤500-word digests". **Amendment:** rewrite to structural.
- **D4. Phase-7-followup deferral triple ✓ acceptable.** Names all three artifacts by filename. Passes [`AGENTS-MD-2adf78e54a`](../../../AGENTS.md#deferred-work-binding-artifact-triple).
- **D5. Round-1 reviewer-return-text preservation infrastructure missing.** "Round-1 findings will land at this section" but no Appendix A scaffolding for verbatim subagent returns. **Amendment:** add stub section "Appendix A — Round-1 reviewer return text (verbatim)" with one subsection per reviewer.
- **D6. Self-check rubric items mostly pass; one weak.** Items (a)-(e), (g) specify tool commands. Item (f) "`grep -F` for verbatim text-pull when invoked" is conditional and underspecified. **Amendment:** "(f) For each binding rule table cited in the notes file, `grep -F '<verbatim cell text>'` against the source AGENTS.md anchor; report exit code in digest."
- **D7. Classification taxonomy table — guidance, not binding.** The 4-token table is Phase-7-internal classification scheme proposed by lead agent. NOT a binding rule table per [`AGENTS-MD-bf4431be57`](../../../AGENTS.md#verbatim-text-pull-when-citing-binding-rule-tables). Subagents may paraphrase token semantics. No amendment needed — but flag this distinction.
- **D8. Rewind-point pinning defect inherited from auto-006.** Branches named not SHAs. Auto-006 Reviewer 6 Amendment 8 flagged identical defect. **Amendment:** add "(SHA pinned post-commit: `<TBD-Round-1-SHA>` Round 1 / `e1ca9b4` Round 2)" to both lines.
- **D9. Honest-acknowledgement `git log` not time-anchored.** Command `git log --oneline -- architectures/v3/backfill-notes/` is unanchored — a later auditor running it post-Wave-7.1 would get non-empty output and the claim would appear false. **Amendment:** rewrite as `git log --all --oneline --before=<Round-1-authordate> -- architectures/v3/backfill-notes/` and use `git ls-tree <SHA>` for SHA-anchored verifiability.
- **D10. Sub-wave coordination protocol** ✓ Branch names unique, files disjoint, conflict protocol stated. Passes.
- **D11. §0 ADR-citation index preservation** ✓ Explicitly invokes ADR 0065. Passes.
- **D12. Framework-ADR + per-variant pairing.** Mentions §0 index but does NOT instruct patch authors to add per-variant ADR when a framework-ADR is added per [`AGENTS-MD-a9fb7b42f8`](../../../AGENTS.md#framework-adr-scope-boundary-discipline). **Amendment:** add one sentence to Wave 7.3 description.
- **D13. Archive-file-to-path mapping** ✓ Complete, verifiable, all 9 files enumerated.
- **D14. PR webhook handling for PR #187.** Brief does NOT acknowledge [`AGENTS-MD-c5a92e6017`](../../../AGENTS.md#pr-webhook-merged-is-advisory-not-authoritative) anywhere. **Amendment:** add to §Sub-wave coordination protocol acknowledgement of webhook-verification rule.
- **D15. Skip discipline auditability.** Instructs subagents to mark D-1 through D-7 as `absorbed (v3 default D-N)`. **Amendment:** require subagents to state explicitly in §1 that defaults are skipped (currently implicit).

**Summary:** Brief reproduces ~70% of auto-006's audit-trail discipline cleanly (triple-bind, mapping table, self-check rubric structure). Defects D1, D2, D3, D5, D8, D9 are direct repeats of auto-006 Reviewer 6 findings that should have been pre-folded as inherited precedent — minor process bug. D14 (webhook rule) is genuinely new. None block dispatch; all surgically fixable in Round-2 close.

---

*(Round 1 closed 2026-05-27 at commit `9c77389`. Round-2 revision authored above.)*

*(Round 2 closes when reviewers' findings land. Round 3 only if Round-2 reviewers return `reject-with-counter-proposal`.)*
