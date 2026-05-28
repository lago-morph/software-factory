# auto-008 — Phase 8 dispatch shape

**Author.** Lead agent, unattended Phase-8 dispatch session 2026-05-28.
**Status.** **Round 1 (initial brief; awaiting first adversarial wave).** Pre-folds the auto-007 audit-trail amendments at Round-1 authoring time (per the deferred [`AGENTS-MD-4a7c2e9f6b`](../../../retrospective/2026-05-27-191/AGENTS-MD-4a7c2e9f6b-adversarial-review-amendment-inheritance.md) draft, applied informally — see [§Honest acknowledgements (Round 1)](#honest-acknowledgements-round-1) for the deferral acknowledgement).
**Rewind point.** This brief's commit on [`claude/phase-8-auto-008-4CZoC`](../../../). Round-1 commit SHA pinned post-commit at the end of [§Honest acknowledgements (Round 1)](#honest-acknowledgements-round-1). Reverting it returns Phase-8 dispatch to "undecided"; no per-candidate lean-eval brief has fired.

---

## TL;DR (≤200 words)

This brief decides Phase-8's dispatch shape per the [v1.2 plan § Phase 8](../../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md#phase-8--lean-eval-design-one-brief-per-candidate-first-pressure-test-surface-revised-in-v12). Phase 8 produces three sub-products: **10 per-candidate lean-eval briefs** (one per candidate in [`architectures/v3/lean-evals/`](../lean-evals/)), **one cross-candidate evaluator-brief** at `architectures/v3/lean-evals/00-cross-candidate.md`, and a **Phase-8-close session handoff**. The brief decides: wave shape (per-candidate parallel fanout vs alternatives); per-candidate brief rubric (section structure with mandatory `falsifying-outcome:` YAML field, word-budget tier, scenario-set sourcing); exemplar selection + pre-fanout self-check gate; bias-guard concurrency shape (which auditors fire concurrent vs serial); Phase-7 cite-obligation propagation mechanism (lead-agent-pre-authored per-candidate mapping table vs subagent-derived); cross-candidate evaluator-brief shape with DEC-1.a falsifying-result-pattern named **in advance** (load-bearing); tier-table calibration per Phase-7 evidence; audit-trail discipline inherited from auto-007. The Round-1 decision section ([§Decision (Round 1)](#decision-round-1)) names every parameter. Round-1 reviewers' load-bearing amendments will be folded in Round 2 at [§Decision (Round 2)](#decision-round-2-pending) (currently empty scaffold).

## The question

Phase 8 of the v3 synthesis produces a per-candidate lean-eval brief per the [v1.2 plan § Phase 8](../../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md#phase-8--lean-eval-design-one-brief-per-candidate-first-pressure-test-surface-revised-in-v12). Three sub-products are owed:

- **10 per-candidate lean-eval briefs** at `architectures/v3/lean-evals/<candidate-id>.md` (one per Phase-6 candidate). Each carries: target candidate; test scenario set (drawn from corpus or from the candidate's own scenario-derivation primitives); success criteria; failure modes the lean-eval is designed to surface; expected evaluator time (~1 day per [v1.2 plan](../../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md#phase-8--lean-eval-design-one-brief-per-candidate-first-pressure-test-surface-revised-in-v12)); references to candidate's open critique findings; **Phase-7 cite obligations that apply to this candidate**; and **mandatory `falsifying-outcome:` YAML frontmatter field** (per [§Falsifier discipline](#falsifier-discipline-load-bearing) below).
- **1 cross-candidate evaluator-brief** at `architectures/v3/lean-evals/00-cross-candidate.md`. Names comparison axes across all 10 lean-evals + names **in advance** the cross-candidate result pattern that would falsify the [DEC-1.a working hypothesis](../decisions-captured.md#d1--unification-verdict-no-methodology-serves-both-mandates-working-hypothesis-falsifiable-by-phase-8), so post-hoc reinterpretation is impossible.
- **Phase-8-close session handoff** at `architectures/v3/SESSION-HANDOFF-2026-05-28-phase-8-close.md` unblocking the downstream simulator-harness work (post-v3 scope).

**Bias-guards** (per [v1.2 plan § Phase 8](../../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md#phase-8--lean-eval-design-one-brief-per-candidate-first-pressure-test-surface-revised-in-v12)):

- **Domain practitioner.** For each of the 10 per-candidate briefs, names whether the test scenarios would actually validate the discipline (or are an internal-consistency check disguised as a lean-eval).
- **Falsification-designer.** For each of the 10 per-candidate briefs, names the falsifying outcome verbatim; if the brief cannot articulate one, the brief is too soft and gets rewritten.
- **Hypothesis-falsifier.** Cross-candidate; names *in advance* the result pattern that would falsify the DEC-1.a working hypothesis. Reads all 10 lean-eval briefs.

**Phase-7 load-bearing inputs** (each per-candidate Phase-8 brief MUST honor these; pre-authored mapping at [§Phase-7 cite-obligation propagation table](#phase-7-cite-obligation-propagation-load-bearing-pre-authored-mapping) below):

1. **3 high-confidence silently-absorbed cells** (per [aggregation §3.1](../backfill-notes.md#31-high-confidence-findings-3--apply-precedence-rule)) → mandatory archive cites in named candidates' lean-eval briefs.
2. **7 medium-confidence TBD reconciliation cells** (per [aggregation §3.2](../backfill-notes.md#32-medium-confidence-findings-7--trigger-tbd-reconciliation-rows)) → per-candidate design inputs (subagents read [`backfill-notes/audit-silent-absorption.md` §B.1](../backfill-notes/audit-silent-absorption.md) for cells touching their candidate).
3. **5 historian load-bearing gaps** (per [aggregation §4.1](../backfill-notes.md#41-load-bearing-gaps-5--phase-8-lean-eval-inputs)) → per-candidate design inputs for H-1 (U-C or D7-U-1), H-2 + H-8 (GF-S / GF-M / U-A), H-3 (BF-L), H-5 (glossary, non-blocking).

The dispatch shape determines (i) how the 10 lean-eval subagents are sequenced (parallel? sub-waves? serial?), (ii) per-candidate brief shape + rubric + section structure + word budget + YAML frontmatter, (iii) which candidate's brief serves as the exemplar (lead-agent authored first), (iv) whether the cross-candidate evaluator-brief is a separate subagent dispatch or lead-agent-authored at fanout-close, (v) which bias-guard subagents fire concurrent vs serial, (vi) how Phase-7 cite obligations propagate (lead-agent pre-authored mapping vs subagent-derived).

## Alternatives considered

### A. Per-candidate parallel fanout (Wave 8.1) + 2 per-candidate-concurrent bias-guards (domain-practitioner + falsification-designer, paired per-candidate) + 1 serial bias-guard after Wave 8.1 (hypothesis-falsifier) + Wave 8.2 cross-candidate evaluator-brief, lead-agent exemplar first with self-check gate, tiered word-budget per Phase-7 evidence — lead-agent recommendation

- **Lead-agent inline: exemplar lean-eval brief** for the least-contested candidate (TBD — lead agent picks at exemplar-authoring time from {GF-M, BF-S}; GF-M default lean for cleanest single-dominant lineage + greenfield-light scenario-set framing). ~5500-word target (mid-Light-tier). Demonstrates the §1-§8 rubric, the YAML frontmatter with `falsifying-outcome:` field populated, the per-candidate Phase-7 cite-obligation honoring pattern, and the §3 falsifying-outcome verbatim discipline. Committed as the first Phase-8 work artifact (PR 3 in the run, after envelope #194 and this brief).
- **Wave 8.1 (9 sibling per-candidate subagents in parallel)** fires after the exemplar lands. Each subagent reads: (i) its candidate's [`specs/<id>.md`](../specs/), (ii) the candidate's [`backfill-notes/<id>.md`](../backfill-notes/), (iii) the candidate's open carries from [`specs/<id>.md` §6](../specs/), (iv) this brief's rubric + cite-obligation table row for its candidate, (v) the exemplar brief. Writes its lean-eval brief at `architectures/v3/lean-evals/<candidate-id>.md`. Returns a ≤500-word digest.
- **Bias-guards (Wave 8.1.b, fire concurrent with Wave 8.1 per-candidate, paired per-candidate)** — per the [ADR-3f8c1e5b7a precedent](../../../retrospective/2026-05-27-191/ADR-3f8c1e5b7a-bias-guards-concurrent-with-fanout.md): bias-guards fire concurrent IF their input streams are independent of per-candidate outputs.
  - **Domain-practitioner subagent (10× per-candidate).** For each candidate, reads the candidate's `specs/<id>.md` + the candidate's lean-eval brief draft (when ready from the per-candidate subagent's first commit) + the candidate's open carries. Verdict: would the test scenarios actually validate the discipline? Practical concerns the brief misses. Output: a ≤300-word verdict appended to each `lean-evals/<candidate-id>.md` §9 (or written to `lean-evals/audit-domain-practitioner.md` cross-candidate roll-up — decide at exemplar-authoring time). **Independent of sibling per-candidate briefs.**
  - **Falsification-designer subagent (10× per-candidate).** For each candidate, verifies the `falsifying-outcome:` YAML field is populated AND the §3 falsifying-outcome statement is verbatim, concrete (not "evaluator subjective judgment"), and pre-committed (i.e., a result pattern that could be machine-checked against a future simulator run). If the brief hand-waves the falsifier, the falsification-designer's verdict is "rewrite §3"; lead agent re-authors. **Independent of sibling per-candidate briefs.**
- **Bias-guard (Wave 8.1.c, fires SERIAL after Wave 8.1 closes)** — the hypothesis-falsifier reads all 10 lean-eval briefs to name the cross-candidate falsifying result pattern. Cannot fire concurrent.
  - **Hypothesis-falsifier subagent (1× cross-candidate).** Reads all 10 finalized `lean-evals/<candidate-id>.md` briefs + the [DEC-1.a working hypothesis text](../decisions-captured.md#d1--unification-verdict-no-methodology-serves-both-mandates-working-hypothesis-falsifiable-by-phase-8) + the [Phase-7 §6.4 NEUTRAL observation](../backfill-notes.md#64-dec-1-a-working-hypothesis-observation-neutral-pre-phase-8). Output: `lean-evals/audit-hypothesis-falsifier.md` — names the cross-candidate result pattern that would falsify DEC-1.a (e.g., "If ≥2 unified-attempt candidates pass BOTH the greenfield AND brownfield lean-eval cleanly with no escape-hatches invoked, DEC-1.a is falsified"). The pattern is committed BEFORE the cross-candidate evaluator-brief lands, so the falsifier discipline is mechanically auditable: the evaluator-brief MUST quote the hypothesis-falsifier's pattern verbatim in its §X falsifying-result-pattern section.
- **Wave 8.2 (cross-candidate evaluator-brief, lead-agent-authored OR subagent-dispatched, fires SERIAL after Wave 8.1.c)**. Reads all 10 per-candidate briefs + the hypothesis-falsifier output. Writes `lean-evals/00-cross-candidate.md`. Names comparison axes (e.g., scenario-set overlap; falsifying-outcome severity; expected evaluator time; failure-mode coverage). Quotes the hypothesis-falsifier's DEC-1.a falsifying result pattern verbatim.
  - **Lead-agent-authored is the default** (analogous to Phase-7 aggregation: lead agent at fanout-close has all 10 briefs in context for cross-candidate reasoning; subagent dispatch loses that integration). May be subagent-dispatched if context budget approaches 70%.
- **PR consolidation per [`AGENTS-MD-d71e845b29`](../../../AGENTS.md#sub-wave-pr-consolidation-when-files-are-disjoint):**
  - **Wave 8.1 + 8.1.b** → omnibus PR (9 sibling per-candidate briefs + 2 sets of 10 bias-guard outputs OR 2 audit roll-up files; all disjoint files). 1 PR.
  - **Wave 8.1.c (hypothesis-falsifier)** + **Wave 8.2 (cross-candidate evaluator-brief)** → omnibus PR (2 disjoint files at `lean-evals/audit-hypothesis-falsifier.md` + `lean-evals/00-cross-candidate.md`). Note: Wave 8.1.c is serial after Wave 8.1 closes, so requires PR-2 to merge first OR a stacked-PR base off the omnibus branch.

**Per-candidate lean-eval brief rubric.** Section structure, word budget, YAML frontmatter, self-check.

- **H1**: `# Lean-eval brief — <candidate-id> (<full name>)`.
- **YAML frontmatter** (mandatory; the falsification-designer subagent's first check is `grep "falsifying-outcome:" architectures/v3/lean-evals/*.md` to verify every file has this field):
  ```yaml
  based-on-spec-commit: <commit-sha of candidate's specs/<id>.md>
  based-on-backfill-commit: <commit-sha of candidate's backfill-notes/<id>.md>
  based-on-date: <YYYY-MM-DD>
  candidate-tier: <Light | Heavy>
  scenario-set-source: <corpus | candidate-derived | hybrid>
  expected-evaluator-time-days: <N>
  falsifying-outcome: |
    <Verbatim ≤80-word statement of the concrete result pattern that would
    falsify the candidate's methodology against the lean-eval. Must be
    machine-checkable in principle: a metric crossing a threshold, a
    behavior class appearing in trajectories, or a specific failure mode
    surfacing. NOT "the evaluator judges the methodology inadequate".>
  phase-7-cite-obligations:
    high-confidence-mandatory:
      - <cite-obligation-1 from the per-candidate mapping table below>
    medium-confidence-design-inputs:
      - <cell-id from backfill-notes/audit-silent-absorption.md §B.1>
    historian-design-inputs:
      - <H-N gap-id from aggregation §4.1>
  ```
- **§1 Candidate + scenario set** (~400-600 words). Restates the candidate's mandate / axis / entry-mode (one paragraph) + names the scenario set (where it comes from — corpus subset, candidate's own scenario-derivation primitives, or a hybrid). For candidates whose spec already carries a scenario-derivation primitive (e.g., U-A's Compound-Knowledge Atelier, BF-L's P-13 maintenance loop), cite that primitive's spec §-anchor verbatim. Names ≥5 specific scenarios with one-sentence each.
- **§2 Success criteria** (~400-600 words). What "the candidate passes the lean-eval" looks like, in concrete terms. Per-scenario success criteria + overall pass condition. Avoid hand-waving ("the methodology produces good code"); name behaviors, artifacts, or metrics.
- **§3 Falsifying outcome** (~200-300 words; LOAD-BEARING per [§Falsifier discipline](#falsifier-discipline-load-bearing) below). The single most concrete result that would falsify this candidate's methodology under this lean-eval. The `falsifying-outcome:` YAML field is the verbatim ≤80-word distillation; §3 expands with rationale (why this falsifier and not another) + how it differs from the success-criteria negation (failing criteria might be implementation noise; the falsifier is the methodology's load-bearing claim being wrong).
- **§4 Failure modes the test surfaces** (~400-600 words). For each of the ≥5 scenarios in §1, names the failure modes the scenario is designed to reveal. Cites the candidate's spec §5 (failure modes) verbatim where applicable. Per [`AGENTS-MD-bf4431be57`](../../../AGENTS.md#verbatim-text-pull-when-citing-binding-rule-tables): if the brief cites the candidate's `specs/<id>.md` §0 ADR-citation index or §5 failure-mode table, use verbatim text-pull, not paraphrase.
- **§5 Evaluator time + protocol** (~300-500 words). Names the expected evaluator time (per [v1.2 plan](../../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md#phase-8--lean-eval-design-one-brief-per-candidate-first-pressure-test-surface-revised-in-v12), ~1 day per candidate). Names the protocol: how the evaluator runs the scenarios, what artifacts they collect, what threshold/judgment they apply for the falsifying-outcome and success-criteria.
- **§6 Open critique references** (~200-400 words). Per [`specs/<id>.md` §6](../specs/) (open carries): the candidate's open critique findings that this lean-eval is designed to pressure-test. Cite each by §-anchor.
- **§7 Phase-7 cite obligations honored** (~300-500 words). For each high-confidence cite obligation in this candidate's row of [§Phase-7 cite-obligation propagation table](#phase-7-cite-obligation-propagation-load-bearing-pre-authored-mapping) below, names how the lean-eval brief honors it (the cite appears verbatim in §1 or §4 or §6 with archive `path` + §-anchor). For each medium-confidence design input from [`backfill-notes/audit-silent-absorption.md` §B.1](../backfill-notes/audit-silent-absorption.md): if the lean-eval scenario design touches the TBD cell, name how (one paragraph). For each historian load-bearing gap touching this candidate: name how the lean-eval surface engages the gap (if at all).
- **§8 References** (mandatory; relative paths only per [`AGENTS.md § Internal document references`](../../../AGENTS.md#internal-document-references)). Floor: candidate's spec + candidate's back-fill notes + this brief + the candidate's substrate-requirements summary + any archive files cited + the relevant ADRs.

**Word budget per lean-eval brief (tiered per Phase-7 advisory carry-forward; pre-folded at Round 1 per the [Phase-7-close handoff §Open questions item 2](../SESSION-HANDOFF-2026-05-27-phase-7-close.md#open-questions--suggestions-for-the-next-agent)).**

| Tier | Word budget | Candidates | Rationale |
|---|---|---|---|
| Light | 5000-6500 | GF-S, GF-M, GF-C, BF-S | Single-dominant or no-single lineage; smaller cite-obligation surface (0-2 high-confidence mandatory cites each) |
| Heavy | 5500-7500 | BF-M, BF-L, U-A, U-B, U-C, D7-U-1 | Multiple-lineage candidates; larger cite-obligation surface (1-3 high-confidence mandatory cites each); unified-attempts carry the DEC-1.a falsification load |

Calibrated against Phase-7 actuals (median Light ~6400, median Heavy ~7200). Subagent runs `wc -w` against its tier's bounds in self-check item (a); over-budget triggers a return-digest flag for lead-agent review.

**Self-check rubric** per [`AGENTS-MD-e74e4811a2`](../../../AGENTS.md#self-check-rubric-requires-tool-verification-for-measurable-items). Subagent runs:

- (a) `wc -w` on its lean-eval file to verify word budget compliance against its tier.
- (b) `ls` on every cited v3 file path (`specs/<id>.md`, `backfill-notes/<id>.md`, any ADR files, any archive files) to verify the file exists.
- (c) `grep` for §1-§8 headers to verify section structure.
- (d) `grep "falsifying-outcome:" <its file>` to verify the YAML field is populated AND `grep -c "^  "` (or equivalent) on the field's value to verify ≤80 words.
- (e) `grep -c "phase-7-cite-obligations:" <its file>` to verify the YAML field exists.
- (f) For each binding rule table cited (e.g., the candidate's `specs/<id>.md` §0 ADR-citation index): `grep -F '<verbatim cell text>' <source-anchor>` to verify exact-text-pull per [`AGENTS-MD-bf4431be57`](../../../AGENTS.md#verbatim-text-pull-when-citing-binding-rule-tables). If no binding rule table is cited, item (f) self-reports `n/a` with rationale.
- (g) `grep -cE "##? §[1-8]"` to verify exactly 8 §-headers (excluding YAML frontmatter and H1).
- (h) Per-candidate cite-obligation check: `grep -F '<archive cite text from this candidate's row in the cite-obligation mapping>' <its file>` for each high-confidence mandatory cite obligation; ALL must pass. Failures triggered re-authoring before fanout closes.

**Pros.**
- Maximum parallelism: 10 + 20 (paired per-candidate bias-guards) = 30 concurrent subagents (Wave 8.1 + 8.1.b). At the upper end of the ~20-25 practical limit per the [autonomous-run skill § Subagent fanout cadence](../../../.claude/skills/autonomous-run/SKILL.md#subagent-fanout-cadence) — see [§Honest acknowledgements (Round 1)](#honest-acknowledgements-round-1) for mitigation.
- Bias-guards-concurrent leverages independence per ADR-3f8c1e5b7a — no waiting for per-candidate verdicts to materialize before bias-guards begin.
- Hypothesis-falsifier-serial-after-fanout honors the cross-candidate read it requires; no premature firing.
- Lead-agent exemplar enforces shape consistency across 9 sibling briefs per [`AGENTS-MD-eec503a3c2`](../../../AGENTS.md#exemplar-before-parallel-uniform-schema-fanout).
- Falsifier-discipline gate (§3 + YAML field + falsification-designer auditor + hypothesis-falsifier in advance) makes Phase 8 the actual pressure-testing surface, not another internal-consistency exercise.
- Phase-7 cite-obligation propagation via pre-authored mapping is mechanically robust — subagents don't have to derive obligations from the aggregation matrix; they read their row of the table.

**Cons.**
- 30 concurrent subagents (10 per-candidate + 20 bias-guard) is at the upper end of harness capacity. **Mitigation:** if bias-guards' per-candidate isolation is unclear at exemplar-authoring time, collapse domain-practitioner + falsification-designer to **2 cross-candidate auditors** (each reads all 10 briefs, produces a roll-up). Decided at exemplar-commit time; see [§Bias-guard concurrency shape decision point](#bias-guard-concurrency-shape-decision-point) below.
- Per-candidate paired bias-guards produce 20 verdict outputs that must aggregate cleanly. **Mitigation:** each subagent writes its verdict to a single audit roll-up file (one per auditor type) with §-per-candidate sectioning, not 20 separate files. Or appended to each `lean-evals/<id>.md` §9 (TBD at exemplar-authoring time).
- Hypothesis-falsifier serial-after-fanout adds wall-clock latency (Wave 8.1 → 8.1.c → 8.2). **Mitigation:** Wave 8.2 cross-candidate evaluator-brief depends on hypothesis-falsifier output (must quote DEC-1.a falsifier pattern verbatim), so the serialization is necessary, not waste.

### B. Cross-candidate evaluator-brief authored FIRST (inverted order)

Lead agent authors `lean-evals/00-cross-candidate.md` first; it names the comparison axes + DEC-1.a falsifying pattern. Per-candidate subagents then author their briefs against the cross-candidate axes.

- **Pros.** Cross-candidate consistency built in by construction; per-candidate subagents have shared design vocabulary from the start.
- **Cons.** Inverts the falsifier discipline: the hypothesis-falsifier's job is to name the cross-candidate falsifying pattern AFTER reading the 10 per-candidate briefs (so the pattern is grounded in their content). Authoring cross-candidate first means the lead agent guesses the pattern, then per-candidate briefs are shaped to fit the guess — circular reasoning. **Not chosen.**

### C. Per-mandate-cluster sub-waves (3 GF + 3 BF + 4 U)

Dispatch in waves by mandate (Wave 8.1.GF, Wave 8.1.BF, Wave 8.1.U).

- **Pros.** Mandate-clustering would offer a clean PR-consolidation boundary if files weren't disjoint.
- **Cons.** Files ARE disjoint (each subagent writes only its candidate's brief). Omnibus consolidation per [`AGENTS-MD-d71e845b29`](../../../AGENTS.md#sub-wave-pr-consolidation-when-files-are-disjoint) wins on PR-cap. **Not chosen** (repeats Phase-6 + Phase-7 learned-the-hard-way pattern).

### D. Sequential per-candidate (serial fanout, 10 subagents one after another)

Dispatch the 10 subagents sequentially; later ones read earlier briefs as additional calibration points.

- **Pros.** Successor subagents could refine the exemplar's shape based on what earlier ones produced.
- **Cons.** 10× wall-clock cost vs parallel. Exemplar (Option A) already serves the calibration purpose. **Not chosen.**

### E. Per-archive-scenario fanout (NOT per-candidate)

Dispatch ~8-10 subagents, one per scenario class (e.g., one per archive failure mode F1-F33). Each subagent designs scenarios for all 10 candidates against its assigned failure-mode class.

- **Pros.** Per-failure-mode deep-reading discipline.
- **Cons.** Inverts the per-candidate scoping principle that the v1.2 plan § Phase 8 mandates ("one brief per candidate"). The cross-candidate evaluator-brief is the explicit cross-cutting view; per-candidate is the primary unit. **Not chosen.**

### F. Lead-agent inline (no subagent dispatch)

Lead agent authors all 10 per-candidate briefs + cross-candidate brief + bias-guard outputs inline.

- **Pros.** Single-author cross-candidate consistency.
- **Cons.** Saturates context with 10 specs × ~7K words + 10 back-fill notes × ~7K words = ~140K words of input + per-candidate analysis. Forecloses fresh-context per-candidate reasoning. **Not chosen.**

### G. Two-stage fanout (cite-obligation-only first, full-brief second)

Wave 8.0.a: 10 subagents each derive their candidate's Phase-7 cite obligations from the aggregation matrix + back-fill notes. Wave 8.0.b: 10 subagents author the full lean-eval briefs using the Wave-8.0.a-derived obligations.

- **Pros.** Cite-obligation derivation isolated from brief authoring.
- **Cons.** Lead agent CAN pre-author the cite-obligation table at Round-1 brief authoring time (the obligations are mechanically derivable from aggregation §3.1 + §4.1). Wave 8.0.a is wasteful. **Not chosen** — see [§Phase-7 cite-obligation propagation table](#phase-7-cite-obligation-propagation-load-bearing-pre-authored-mapping) below.

## Decision (Round 1)

**Option A. Per-candidate parallel fanout (Wave 8.1, 9 sibling subagents) + per-candidate-paired bias-guards concurrent (Wave 8.1.b, 20 subagents — see [§Bias-guard concurrency shape decision point](#bias-guard-concurrency-shape-decision-point) for fallback to 2 cross-candidate auditors if harness capacity is a concern) + hypothesis-falsifier serial after Wave 8.1 closes (Wave 8.1.c, 1 subagent) + Wave 8.2 cross-candidate evaluator-brief (lead-agent-authored by default), lead-agent exemplar first with self-check gate, tiered word-budget (Light 5000-6500 / Heavy 5500-7500), pre-authored Phase-7 cite-obligation propagation table.**

### Reasoning

Three drivers select Option A:

1. **The Phase-6 + Phase-7 precedent worked cleanly with per-candidate parallel fanout + lead-agent exemplar + omnibus PR consolidation.** The same shape pattern applies to Phase 8's deliverable family. Reusing the calibrated pattern over inventing a new one.
2. **The falsifier discipline is the actual point of Phase 8.** Naming the falsifying outcome **in advance** (per per-candidate YAML field + per-candidate §3 + cross-candidate hypothesis-falsifier output) makes the lean-eval the genuine pressure-testing surface the v1.2 plan describes. Without the YAML field + falsification-designer auditor + hypothesis-falsifier-serial-after-Wave-8.1, Phase 8 collapses into another internal-consistency exercise where post-hoc reinterpretation can rescue any candidate from any result.
3. **Pre-authoring the cite-obligation table at brief Round-1 saves a wave of derivation work.** The 3 high-confidence cells + 5 historian gaps from Phase-7 are mechanically known per the aggregation matrix; lead agent maps them to candidates in the brief; subagents read their row, not the matrix. Mirrors auto-007's "common archive-file-to-path mapping" pre-authored pattern.

### Bias-guard concurrency shape decision point

Two viable configurations for domain-practitioner + falsification-designer:

| Config | Subagent count | Pros | Cons |
|---|---|---|---|
| **A.1 Per-candidate-paired (default)** | 20 (10 + 10) | Per-candidate isolation; each auditor's verdict targets a specific brief | At the upper end of harness capacity (30 concurrent in Wave 8.1 + 8.1.b) |
| **A.2 Cross-candidate roll-up (fallback)** | 2 (1 + 1) | Lighter harness load; each auditor reads all 10 briefs and writes one roll-up | Loses per-candidate isolation; verdict-per-brief is paragraph-level inside the roll-up rather than dedicated subagent output |

**Lead-agent decision criterion:** at exemplar-commit time, if the exemplar's `falsifying-outcome:` YAML field + §3 verbatim falsifying-outcome statement is **mechanically auditable** (machine-checkable in principle), fire **A.1 per-candidate-paired** — the falsification-designer subagent's job is narrow and well-defined per candidate. If the exemplar's falsifying-outcome is more interpretive (concrete-but-not-machine-checkable), fall back to **A.2 cross-candidate roll-up** — interpretation benefits from the cross-candidate context.

**Default lean: A.1** (the falsifier discipline encourages machine-checkable verbatim statements per [§Falsifier discipline](#falsifier-discipline-load-bearing) below).

The hypothesis-falsifier is always 1× cross-candidate serial after Wave 8.1 — that doesn't change between A.1 and A.2.

### Sub-wave coordination protocol

Each sub-wave fires from a separate stacked branch:

- **Exemplar (PR 3)** branch: `claude/phase-8-exemplar`. Lead agent authors `lean-evals/<exemplar-id>.md` and (if not already created) `lean-evals/` directory + `lean-evals/.gitkeep`. Lead-agent self-checks (a)-(h) on exemplar before fanout dispatch.
- **Wave 8.1 + 8.1.b (PR 4 omnibus)** branch: `claude/phase-8-fanout-omnibus`. 9 per-candidate subagents write to `lean-evals/<id>.md`. Bias-guards write to `lean-evals/audit-domain-practitioner.md` + `lean-evals/audit-falsification-designer.md` (A.1: per-candidate sections within each audit file; A.2: each file is one cross-candidate roll-up).
- **Wave 8.1.c + 8.2 (PR 5 omnibus)** branch: `claude/phase-8-cross-candidate`. Lead agent dispatches hypothesis-falsifier subagent (1× cross-candidate); when its output lands at `lean-evals/audit-hypothesis-falsifier.md`, lead agent authors `lean-evals/00-cross-candidate.md` quoting the falsifier pattern verbatim.
- **Phase-8-close handoff (PR 6)** branch: `claude/phase-8-handoff`. New `SESSION-HANDOFF-2026-05-28-phase-8-close.md` + `AGENT-ENTRY.md` Section-2 update.
- **Run summary + retrospective (PR 7)** branch: `claude/phase-8-summary-retro`. Top-level `run-summary-2026-05-28-phase-8.md` + `retrospective/2026-05-28-<PPP>/` full-package directory per [`AGENTS-MD-1d7c94415e`](../../../AGENTS.md#full-retrospective-package-lean-mode-is-anti-pattern).

**File uniqueness invariant**: each lean-eval subagent's file is named per the candidate's ID (`gf-s.md` / `gf-m.md` / `gf-c.md` / `bf-s.md` / `bf-m.md` / `bf-l.md` / `u-a.md` / `u-b.md` / `u-c.md` / `d7-u-1.md`). Bias-guard subagents write to fixed audit filenames. Exemplar candidate's file is authored by lead agent on PR 3 before fanout.

**Conflict protocol**: if a per-candidate subagent finds its target brief file already exists or the branch tip moved unexpectedly, surface in return digest; do not force-push. Lead agent reconciles at Wave 8.1 close.

**Total subagents this run:** 9 (per-candidate fanout, excluding exemplar candidate) + 2 or 20 (bias-guards per A.1 or A.2) + 1 (hypothesis-falsifier) + 0 or 1 (cross-candidate evaluator-brief — lead-agent by default) + 6 adversarial reviewers (Round 1 + Round 2 of this brief) + ~3-4 retrospective-package authoring subagents at run close = **~21-39 subagents total for Phase 8** (range driven by A.1 vs A.2).

**PR-cap math**: 1 (envelope #194, already opened) + 1 (this brief, R2) + 1 (exemplar) + 1 (Wave 8.1 + 8.1.b omnibus) + 1 (Wave 8.1.c + 8.2 omnibus) + 1 (handoff) + 1 (summary+retro) = **7 PRs against ≤15 Phase-8 budget cap**. Comfortable 8-PR margin.

## Phase-7 cite-obligation propagation (load-bearing pre-authored mapping)

Per [`AGENTS-MD-8740bd7b0a`](../../../AGENTS.md#adr-number-to-filename-mapping-in-subagent-dispatch-briefs) (analogous to the ADR-number-to-filename mapping pattern): lead agent pre-authors the per-candidate Phase-7 cite-obligation mapping at brief Round-1 authoring time. Each per-candidate Wave-8.1 subagent receives its row of this table as part of its dispatch input.

### High-confidence mandatory cite obligations (3 cells × N candidates)

Per [aggregation §3.1](../backfill-notes.md#31-high-confidence-findings-3--apply-precedence-rule). Each named candidate's Phase-8 lean-eval brief MUST honor the cite obligation (verbatim archive cite in §1 or §4 or §6 + the YAML `phase-7-cite-obligations.high-confidence-mandatory` field).

| Candidate | Mandatory cite obligations |
|---|---|
| **GF-S** | *(none)* — GF-S aggregation matrix shows no high-confidence silent-absorption findings for this candidate. |
| **GF-M** | **Compound-Engineering 4-step loop verbatim cite** → cite `archive/synthesis-v1-v2/13-round-2-synthesis.md` (v0.2 canonicalization of `plan → work → review → compound`). |
| **GF-C** | *(none)*. |
| **BF-S** | **(1) Compound-Engineering 4-step loop verbatim cite** → `archive/synthesis-v1-v2/13-round-2-synthesis.md`. **(2) 4-architecture taxonomy cite** → `archive/architectures-v2/00-comparison.md` §1 (Atelier-style / Refinery-style / Foundry-style / Tournament-style work-unit-shape taxonomy). |
| **BF-M** | **(1) Compound-Engineering 4-step loop** → `archive/synthesis-v1-v2/13-round-2-synthesis.md`. **(2) 4-architecture taxonomy** → `archive/architectures-v2/00-comparison.md` §1. |
| **BF-L** | **4-architecture taxonomy cite** → `archive/architectures-v2/00-comparison.md` §1. |
| **U-A** | **(1) Knowledge-promotion 4-token enum** (`insight / playbook / correction / pattern`) → `archive/architectures-v2/02-compound-atelier.md` §3.2. **(2) Compound-Engineering 4-step loop** → `archive/synthesis-v1-v2/13-round-2-synthesis.md`. **(3) 4-architecture taxonomy** → `archive/architectures-v2/00-comparison.md` §1. |
| **U-B** | **Compound-Engineering 4-step loop verbatim cite** → `archive/synthesis-v1-v2/13-round-2-synthesis.md`. |
| **U-C** | **Compound-Engineering 4-step loop verbatim cite** → `archive/synthesis-v1-v2/13-round-2-synthesis.md`. |
| **D7-U-1** | **(1) Compound-Engineering 4-step loop** → `archive/synthesis-v1-v2/13-round-2-synthesis.md`. **(2) 4-architecture taxonomy** → `archive/architectures-v2/00-comparison.md` §1. |

### Medium-confidence design inputs (7 cells × N candidates)

Per [aggregation §3.2](../backfill-notes.md#32-medium-confidence-findings-7--trigger-tbd-reconciliation-rows). Specific cells in [`backfill-notes/audit-silent-absorption.md` §B.1](../backfill-notes/audit-silent-absorption.md). Each per-candidate Wave-8.1 subagent consults §B.1 for cells touching its candidate; cells become per-candidate design inputs ("is the candidate's framing distinguishable from the archive item, or silent inheritance worth citing?"). Subagent flags any cell in its lean-eval brief's §7 with one-paragraph engagement.

### Historian load-bearing design inputs (5 gaps × N candidates)

Per [aggregation §4.1](../backfill-notes.md#41-load-bearing-gaps-5--phase-8-lean-eval-inputs).

| Candidate | Historian design inputs |
|---|---|
| **GF-S** | H-2 + H-8 paired (self-improving-prompts pattern + role) — methodology decision in §1 (scenario set) or §5 (protocol). |
| **GF-M** | H-2 + H-8 paired — methodology decision. |
| **U-A** | H-2 + H-8 paired — methodology decision. |
| **BF-L** | H-3 Pulse report (production-trace-to-spec-amendment) → BF-L's P-13 maintenance loop is the closest analog; flag in §1 or §6 if the lean-eval engages the Pulse-report-style downstream surface. |
| **U-C OR D7-U-1** (one of two — lead agent does NOT pre-pick) | H-1 stable-ID lettering convention (R/A/F/AE/U/S/K). Recommend ONE candidate adopts in their lean-eval methodology. Either candidate's Wave-8.1 subagent can volunteer; if both decline, lead agent picks at Wave 8.1 close. Flagged in §1 or §6. |

H-5 (scaffold/harness C11 vocabulary) is a glossary addition opportunity, NOT a Phase-8 brief input; lead agent or Phase-8-close handoff carries it as non-blocking carry-forward.

## Falsifier discipline (load-bearing)

**This discipline is what makes Phase 8 the actual pressure-testing surface** rather than another internal-consistency exercise. The discipline has three load-bearing components:

1. **Mandatory `falsifying-outcome:` YAML frontmatter field** in every per-candidate `lean-evals/<id>.md`. The field value is a verbatim ≤80-word statement of the concrete result pattern that would falsify the candidate's methodology against the lean-eval. The falsification-designer auditor's first check is `grep "falsifying-outcome:" architectures/v3/lean-evals/*.md` — every file must have this field, populated, non-empty.

2. **Mandatory §3 falsifying-outcome statement** in every per-candidate brief. Expands the YAML field's ≤80 words into ~200-300 words of rationale: why this falsifier and not another; how it differs from the success-criteria negation (failing criteria might be implementation noise; the falsifier is the methodology's load-bearing claim being wrong); machine-checkability constraints. Per the [autonomous-run skill § Working-mode reminders](../../../.claude/skills/autonomous-run/SKILL.md#working-mode-three-rules): briefs that hand-wave the falsifier get rewritten.

3. **Mandatory cross-candidate DEC-1.a falsifying result pattern named in advance** in the hypothesis-falsifier output AND quoted verbatim in the cross-candidate evaluator-brief. The hypothesis-falsifier reads all 10 lean-eval briefs AFTER they are finalized (serial post-Wave-8.1), names the cross-candidate pattern that would falsify DEC-1.a, and commits the pattern to `lean-evals/audit-hypothesis-falsifier.md`. The cross-candidate evaluator-brief in Wave 8.2 quotes this pattern verbatim in its §X falsifying-result-pattern section, so post-hoc reinterpretation of the DEC-1.a outcome is mechanically blocked.

Example falsifying-outcome statements (illustrative; per-candidate subagents author their own based on their candidate's methodology):

> **For U-A (illustrative):** "U-A's Compound-Knowledge Atelier produces zero promoted patterns after 5 brownfield scenarios where the existing codebase's documentation explicitly contradicts the candidate's promotion-criteria. The knowledge-promotion-rate is machine-countable from `solutions/` directory state at scenario close."

> **For DEC-1.a falsifying result pattern (illustrative):** "If ≥2 unified-attempt candidates (U-A / U-B / U-C / D7-U-1) pass BOTH the greenfield-mandate lean-eval AND the brownfield-mandate lean-eval cleanly (≥80% of named scenarios pass success-criteria; falsifying-outcome NOT triggered) AND neither lean-eval invokes an escape-hatch (e.g., 'this scenario is out of mandate'), DEC-1.a is falsified — at least one methodology serves both mandates."

The illustrative statements above are NOT binding — per-candidate subagents and the hypothesis-falsifier author their own. The point is the **form**: concrete, machine-checkable in principle, pre-committed (named BEFORE evaluation runs).

## Bias-direction discipline

Phase 8 is the falsification surface for the [DEC-1.a working hypothesis](../decisions-captured.md#d1--unification-verdict-no-methodology-serves-both-mandates-working-hypothesis-falsifiable-by-phase-8). Per the [Phase-7 §6.4 NEUTRAL observation](../backfill-notes.md#64-dec-1-a-working-hypothesis-observation-neutral-pre-phase-8): the lead agent and subagents **do NOT pre-judge** the DEC-1.a outcome. Subagent briefs include this instruction verbatim:

> **Be neutral on DEC-1.a.** The matrix pattern from Phase 7 is structurally consistent with DEC-1.a but Phase-8 lean-evals are the explicit falsification surface. Subagents authoring per-candidate briefs do NOT inflate or deflate the candidate's falsifying-outcome statement to favor or disfavor DEC-1.a. The hypothesis-falsifier auditor names the cross-candidate pattern AFTER reading all 10 finalized briefs.

Note this discipline differs from the Phase-7 bias-direction (be-generous-to-archive-material). Phase 8 has a SYMMETRIC bias direction: do not pre-judge.

## Adversarial review discipline commitment

Per [`AGENTS-MD-8a7029647f`](../../../AGENTS.md#adversarial-review-verdict-tiers): each adversarial reviewer dispatch brief (Round 1 + Round 2) explicitly offers the **3-tier verdict menu** (`accept-as-is` / `accept-with-named-amendments` / `reject-with-counter-proposal`). The reviewer prompts are reproduced in [§Appendix A](#appendix-a--round-1-reviewer-return-digests-preserved-for-traceability) (scaffolded; populated at Round-1 fire time).

Per [`AGENTS-MD-d72e1a4f3c`](../../../AGENTS.md#adversarial-review-must-be-real-subagents): all 6 adversarial reviewers across Round 1 + Round 2 are dispatched as real subagents (the `Agent` tool); no inline simulation.

## PR-webhook handling commitment

Per [`AGENTS-MD-c5a92e6017`](../../../AGENTS.md#pr-webhook-merged-is-advisory-not-authoritative): any `merged` webhook event arriving for any Phase-8 PR (#194 envelope, this brief's PR, or any subsequent Phase-8 PR) MUST be verified via `mcp__github__pull_request_read` (method `get`) before the lead agent acts on the notification. The verification costs one API roundtrip and prevents the lead agent from re-creating PRs that already exist or skipping PRs that did not actually merge.

## Phase-8-followup deferral binding mechanism (load-bearing)

If a Phase-8-followup deferral fires (any Wave-8.1 subagent's lean-eval brief fails the falsification-designer's verdict AND lead agent cannot re-author within run budget), the deferral is bound by **three named artifacts** per [`AGENTS-MD-2adf78e54a`](../../../AGENTS.md#deferred-work-binding-artifact-triple):

1. **Session handoff doc.** `architectures/v3/SESSION-HANDOFF-2026-05-28-phase-8-close.md` carries a non-negotiable `## Phase-8-followup carry-forward (deferred from auto-008)` section. Names: (a) the candidates with deferred lean-eval briefs; (b) the falsification-designer's verdict text verbatim; (c) the binding "downstream simulator-harness MAY proceed but Phase-8-followup must close before the deferred candidate's lean-eval executes" constraint.
2. **Run summary "what I deliberately did NOT do" section.** The run's summary carries a `Phase-8-followup lean-eval re-author for <candidates> — deferred to <next-run-id>` bullet.
3. **Next-run dispatch prompt.** `next-agent-prompt-phase-8-followup.md` authored at this run's close (or its absence flagged as a follow-up bullet in the run summary). Points at the Phase-8-close handoff and at this brief.

**Threshold trigger:** ≥1 candidate's lean-eval brief flagged by falsification-designer as "rewrite §3" + cannot be re-authored in-run. (Lower threshold than Phase 7's ≥4 candidates because Phase-8 deliverables are smaller in number — 10 briefs total — and any candidate's lean-eval failing the falsifier discipline is a real defect.)

## Exemplar pre-fanout self-check gate (load-bearing)

Before dispatching Wave 8.1 / Wave 8.1.b, the lead agent **runs self-check items (a)-(h) on the exemplar** and records pass/fail in this brief's [§Exemplar pre-fanout self-check results](#exemplar-pre-fanout-self-check-results) (subsection appended at exemplar-commit time). **Failure on item (d)** (`falsifying-outcome:` field populated AND ≤80 words) or item (h) (high-confidence cite obligations honored) **blocks fanout** — lead agent re-authors the exemplar before any sub-wave fires. Mirrors the Phase-6 U-C / Phase-7 BF-S exemplar gate pattern.

## Honest acknowledgements (Round 1)

Per [`AGENTS-MD-ffe35aa500`](../../../AGENTS.md#honest-acknowledgements-for-pre-round-2-wave-firing) (adapted): this Round-1 brief acknowledges the following deviations / context items honestly, so Round-1 reviewers operate from a clear baseline:

1. **5 Phase-7 retrospective AGENTS-MD-* rules NOT adopted into canonical AGENTS.md** (user-elected; surfaced via AskUserQuestion at envelope-time and deferred). This brief applies the patterns informally and references the retrospective drafts:
   - [`AGENTS-MD-4a7c2e9f6b`](../../../retrospective/2026-05-27-191/AGENTS-MD-4a7c2e9f6b-adversarial-review-amendment-inheritance.md) — adversarial-review amendment-inheritance: pre-folded the auto-007 audit-trail amendments at Round-1 authoring time (commit-SHA pinning, time-anchored honest-acks, Appendix A scaffold, 3-tier verdict commitment, TL;DR structure, PR-webhook commitment, skip-discipline auditability). Cannot cite by stable AGENTS-MD-<hash> in canonical AGENTS.md.
   - [`AGENTS-MD-8e5d3a7c4b`](../../../retrospective/2026-05-27-191/AGENTS-MD-8e5d3a7c4b-phase-followup-bias-guard-fold.md) — Phase-followup bias-guard fold: no Phase-7-followup deferral fired so this rule has no in-Phase-8 obligation, but it shaped the bias-guard mandate scopes in [§Decision (Round 1)](#decision-round-1) above.
   - [`AGENTS-MD-5b3e8a1c2f`](../../../retrospective/2026-05-27-191/AGENTS-MD-5b3e8a1c2f-silent-absorption-confidence-threshold.md) — silent-absorption confidence-threshold: the falsification-designer auditor's verdict-application uses an analogous pattern (verdict overrides per-candidate brief only if `high` machine-checkability concern; `medium` triggers re-author flag; `low` informational). Folded into the rubric informally.
   - [`AGENTS-MD-7d9c4e1b3a`](../../../retrospective/2026-05-27-191/AGENTS-MD-7d9c4e1b3a-matrix-flag-over-spec-patches.md) — matrix-flag over spec-patches: not directly applicable to Phase 8 (no spec patches in scope), but if hypothesis-falsifier surfaces a "rewrite brief vs flag in cross-candidate" question, the matrix-flag pattern applies.
   - [`AGENTS-MD-2f8a6c9d51`](../../../retrospective/2026-05-27-191/AGENTS-MD-2f8a6c9d51-per-candidate-engagement-over-blanket-skip.md) — per-candidate engagement over blanket-skip: no prior-phase defaults are skipped in Phase 8 (Phase 8 reads each candidate's spec + back-fill notes fresh); rule does not bind.
2. **Tier-table calibration (Light 5000-6500 / Heavy 5500-7500)** is pre-folded at Round-1 per the [Phase-7-close handoff §Open questions item 2](../SESSION-HANDOFF-2026-05-27-phase-7-close.md#open-questions--suggestions-for-the-next-agent) recommendation. Round-2 reviewers are invited to challenge if they think Phase-7 actuals (median Light 6400 / Heavy 7200) warrant a different calibration.
3. **Bias-guard concurrency shape (A.1 per-candidate-paired by default; A.2 cross-candidate-rollup as fallback)** is a runtime decision at exemplar-commit time, not a Round-1-bound decision. Round-2 reviewers may amend the criterion if they think the A.1 / A.2 choice should be made at Round 2 instead.
4. **Cross-candidate evaluator-brief authorship (lead-agent-default; subagent-fallback if context approaches 70%)** is a runtime decision at Wave-8.1.c close, not a Round-1-bound decision. Round-2 reviewers may amend.
5. **Time-anchored git log at Round-1 commit time**: per the pre-folded [`AGENTS-MD-4a7c2e9f6b`](../../../retrospective/2026-05-27-191/AGENTS-MD-4a7c2e9f6b-adversarial-review-amendment-inheritance.md) draft (rule 4 of the amendments pre-folded), the Round-1 commit SHA + the most-recent main commit at Round-1 commit time are pinned here. Filled in immediately post-commit:
   - **Round-1 commit SHA:** *(filled in post-commit — see git log)*
   - **origin/main tip at Round-1 commit time:** `99053b0` (Merge PR #193, dispatch prompt phase 8).
   - **Phase-8 envelope commit:** `cce0f73` (Phase-8 scope envelope; merged in PR #194; this brief is stacked on the envelope branch per [`AGENTS-MD-de48bd24b4`](../../../AGENTS.md#stacked-pr-base-selection)).

## Glossary

(Inherited by all subagent briefs.)

- **Lean-eval brief** = a per-candidate ≤1-day evaluation design (test scenario set + success criteria + falsifying outcome + failure modes surfaced + evaluator time + protocol + open critique references + Phase-7 cite obligations). Phase 8's deliverable family. Distinct from a substrate-harness "test" (which the downstream simulator-harness implements).
- **Falsifying outcome** = the concrete result pattern that, if observed, would falsify the candidate's methodology against the lean-eval. Machine-checkable in principle. Named BEFORE evaluation runs. Distinct from "success-criteria negation" — failing the success criteria might be implementation noise; the falsifying outcome is the methodology's load-bearing claim being wrong.
- **DEC-1.a falsifying result pattern** = the cross-candidate result pattern that, if observed across the 10 lean-evals, would falsify the [DEC-1.a working hypothesis](../decisions-captured.md#d1--unification-verdict-no-methodology-serves-both-mandates-working-hypothesis-falsifiable-by-phase-8) ("no methodology serves both mandates"). Named in advance by the hypothesis-falsifier auditor.
- **Phase-7 cite obligation** = a high-confidence silently-absorbed archive item from [aggregation §3.1](../backfill-notes.md#31-high-confidence-findings-3--apply-precedence-rule); the Phase-8 lean-eval brief MUST carry the archive cite (verbatim path + §-anchor).
- **Wave 8.1 / 8.1.b / 8.1.c / 8.2** = the four sub-waves of Phase 8 per [§Sub-wave coordination protocol](#sub-wave-coordination-protocol).

## References

- [`AGENTS.md`](../../../AGENTS.md) — project conventions; 17 active rules.
- [`ARCHITECTURE-V3-SYNTHESIS-PLAN.md` § Phase 8](../../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md#phase-8--lean-eval-design-one-brief-per-candidate-first-pressure-test-surface-revised-in-v12) — v1.2 plan for Phase 8.
- [`AGENT-ENTRY.md`](../../../AGENT-ENTRY.md) — root navigation; Phase-7-close handoff is the active state.
- [Phase-7 close handoff](../SESSION-HANDOFF-2026-05-27-phase-7-close.md) — Phase-7 deliverables + Phase-8 entry posture.
- [Phase-7 aggregation matrix](../backfill-notes.md) — cite-obligation source.
- [Phase-7 silent-absorption auditor output](../backfill-notes/audit-silent-absorption.md) — §B.1 medium-confidence cells.
- [Phase-7 historian auditor output](../backfill-notes/audit-historian.md) — H-1 / H-2 / H-3 / H-5 / H-8 gaps.
- [auto-007 brief](auto-007-phase-7-dispatch-shape.md) — Phase-7 dispatch shape; precedent template for this brief.
- [DEC-1.a working hypothesis](../decisions-captured.md#d1--unification-verdict-no-methodology-serves-both-mandates-working-hypothesis-falsifiable-by-phase-8) — what Phase 8 is the falsification surface for.
- [Phase-7 §6.4 NEUTRAL observation](../backfill-notes.md#64-dec-1-a-working-hypothesis-observation-neutral-pre-phase-8) — pre-Phase-8 stance on DEC-1.a.
- [`AGENTS-MD-d72e1a4f3c`](../../../AGENTS.md#adversarial-review-must-be-real-subagents) — adversarial review must be real subagents.
- [`AGENTS-MD-8a7029647f`](../../../AGENTS.md#adversarial-review-verdict-tiers) — 3-tier verdict scheme.
- [`AGENTS-MD-bb7fe2c5aa`](../../../AGENTS.md#round-1-strikethrough-preservation-in-decision-briefs) — Round-1 preservation discipline.
- [`AGENTS-MD-bf4431be57`](../../../AGENTS.md#verbatim-text-pull-when-citing-binding-rule-tables) — verbatim text-pull for binding rule tables.
- [`AGENTS-MD-eec503a3c2`](../../../AGENTS.md#exemplar-before-parallel-uniform-schema-fanout) — exemplar before uniform-schema fanout.
- [`AGENTS-MD-e74e4811a2`](../../../AGENTS.md#self-check-rubric-requires-tool-verification-for-measurable-items) — self-check requires tool-verification.
- [`AGENTS-MD-d71e845b29`](../../../AGENTS.md#sub-wave-pr-consolidation-when-files-are-disjoint) — omnibus PR consolidation.
- [`AGENTS-MD-2adf78e54a`](../../../AGENTS.md#deferred-work-binding-artifact-triple) — deferred-work triple.
- [`AGENTS-MD-4f8c2a1b03`](../../../AGENTS.md#pre-flight-prior-phase-merge-state-verification) — pre-flight prior-phase merge-state verification.
- [`AGENTS-MD-c5a92e6017`](../../../AGENTS.md#pr-webhook-merged-is-advisory-not-authoritative) — PR webhook merged is advisory.
- [`AGENTS-MD-1d7c94415e`](../../../AGENTS.md#full-retrospective-package-lean-mode-is-anti-pattern) — full retrospective package.
- [`AGENTS-MD-a43c9584c9`](../../../AGENTS.md#dispatch-prompt-edit-before-run-pattern) — dispatch-prompt edit-before-run.
- [`AGENTS-MD-de48bd24b4`](../../../AGENTS.md#stacked-pr-base-selection) — stacked-PR base selection.
- [`AGENTS-MD-8740bd7b0a`](../../../AGENTS.md#adr-number-to-filename-mapping-in-subagent-dispatch-briefs) — pre-authored mapping pattern.
- [`AGENTS-MD-ffe35aa500`](../../../AGENTS.md#honest-acknowledgements-for-pre-round-2-wave-firing) — honest-acknowledgements for pre-Round-2 deviations.
- [`AGENTS-MD-a1ca4ac935`](../../../AGENTS.md#tldr-structure-not-conclusions-test) — TL;DR structure-not-conclusions test.
- [`AGENTS-MD-a9fb7b42f8`](../../../AGENTS.md#framework-adr-scope-boundary-discipline) — framework-ADR scope-boundary.
- [autonomous-run skill](../../../.claude/skills/autonomous-run/SKILL.md) — procedural backbone of unattended runs.
- [Phase-7 retrospective `ADR-3f8c1e5b7a`](../../../retrospective/2026-05-27-191/ADR-3f8c1e5b7a-bias-guards-concurrent-with-fanout.md) — bias-guards-concurrent precedent.

## Appendix A — Round-1 reviewer return digests (preserved for traceability)

*Scaffolded; populated at Round-1 reviewer return time.* Per [`AGENTS-MD-bb7fe2c5aa`](../../../AGENTS.md#round-1-strikethrough-preservation-in-decision-briefs): Round-1 reviewer return text is preserved verbatim here, even if amendments are folded into Round 2 and the Round-1 decision is strikethrough'd above.

### Reviewer 1 — *(angle TBD at dispatch time; default: pre-mortemer)*

*Populated after Round 1 fires.*

### Reviewer 2 — *(angle TBD; default: cost-hawk)*

*Populated after Round 1 fires.*

### Reviewer 3 — *(angle TBD; default: regulator)*

*Populated after Round 1 fires.*

## Exemplar pre-fanout self-check results

*Subsection appended at exemplar-commit time (PR 3 in the run).* Lead-agent self-check items (a)-(h) run on the exemplar brief; pass/fail recorded. Failure on item (d) or (h) blocks fanout.

## Decision (Round 2 — pending)

*Section scaffolded; populated after Round-1 adversarial wave returns and amendments are folded.* Per [`AGENTS-MD-bb7fe2c5aa`](../../../AGENTS.md#round-1-strikethrough-preservation-in-decision-briefs): if Round-2 amendments supersede the Round-1 decision shape, the Round-1 decision section is strikethrough'd (~~text~~) above and the Round-2 decision lands here.
