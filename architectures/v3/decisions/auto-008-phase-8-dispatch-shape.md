# auto-008 — Phase 8 dispatch shape

**Author.** Lead agent, unattended Phase-8 dispatch session 2026-05-28.
**Status.** **Round 2 finalized after BOTH Round-1 and Round-2 adversarial waves; 6/6 reviewers `accept-with-named-amendments`; all load-bearing amendments folded inline.** Round 1 returned 3 × `accept-with-named-amendments` (pre-mortemer + falsification-designer + cost-hawk); Round 2 returned 3 × `accept-with-named-amendments` (regulator + on-call engineer + cross-mandate attacker). Round-2 reviewers did NOT converge on a different option (Option A′ shape preserved), so amendments are folded inline as post-Round-2 patches per [§Round-2-reviewer amendments folded](#round-2-reviewer-amendments-folded-post-round-2-patches). Round-1 decision shape (Option A) is preserved with strikethrough; revised decision at [§Decision (Round 2)](#decision-round-2) flips bias-guards from A.1 per-candidate-paired to **A.2′ cross-candidate-rollup with 3 auditors serial-after-Wave-8.1** (R1 + R3 converged); tightens the falsifier discipline (3-item concreteness rubric + 4th MANDATORY §3-vs-YAML consistency item + canonical escape-hatch enumeration with structural rider for unified-attempts + canonical partitioned "pass cleanly" definition for unified-attempts + reframed "in advance" claim + mandate-scenario-split YAML field for unified-attempts) — R2 + R6 load-bearing structural defect fix; commits lead-agent cross-check artifact (R5 #1, load-bearing); splits Wave 8.1.b and Wave 8.2 into separate PRs (R1 + R3); restricts Phase-8-followup deferral threshold to unified-attempt candidates (R1 #5); drops self-check item (h); tightens Heavy ceiling 7500 → 7200; specifies verdict-token format + over-budget recovery + audit-file archive protocol. Pre-folds the auto-007 audit-trail amendments at Round-1 authoring time per the deferred [`AGENTS-MD-4a7c2e9f6b`](../../../retrospective/2026-05-27-191/AGENTS-MD-4a7c2e9f6b-adversarial-review-amendment-inheritance.md) draft (applied informally — 5 Phase-7 retro rules not adopted into canonical AGENTS.md per user election; see [§Honest acknowledgements (Round 1)](#honest-acknowledgements-round-1)).
**Rewind point.** This brief's commit on [`claude/phase-8-auto-008-4CZoC`](../../../). Round-1 commit SHA `54438e3`; Round-2 initial commit SHA `7e685c5`; Round-2 SHA-pin commit `577cea8`; Round-2-reviewer-amendments-folded commit pinned at [§Honest acknowledgements (Round 2)](#honest-acknowledgements-round-2). Reverting any of these commits returns Phase-8 dispatch progressively to its earlier state; no per-candidate lean-eval brief has fired.

---

## TL;DR (≤200 words)

This brief decides Phase-8's dispatch shape per the [v1.2 plan § Phase 8](../../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md#phase-8--lean-eval-design-one-brief-per-candidate-first-pressure-test-surface-revised-in-v12). Phase 8 produces three sub-products: **10 per-candidate lean-eval briefs** (one per candidate in [`architectures/v3/lean-evals/`](../lean-evals/)), **one cross-candidate evaluator-brief** at `architectures/v3/lean-evals/00-cross-candidate.md`, and a **Phase-8-close session handoff**. The brief decides: wave shape (per-candidate parallel fanout vs alternatives); per-candidate brief rubric (section structure with mandatory `falsifying-outcome:` YAML field, word-budget tier, scenario-set sourcing); exemplar selection + pre-fanout self-check gate; bias-guard concurrency shape (which auditors fire concurrent vs serial); Phase-7 cite-obligation propagation mechanism (lead-agent-pre-authored per-candidate mapping table vs subagent-derived); cross-candidate evaluator-brief shape with DEC-1.a falsifying-result-pattern named **in advance** (load-bearing); tier-table calibration per Phase-7 evidence; audit-trail discipline inherited from auto-007. The Round-2 decision section ([§Decision (Round 2)](#decision-round-2)) names every parameter. Round-1 reviewers' load-bearing amendments are folded in [§Round-2 final amendments folded](#round-2-final-amendments-folded); Round 1's decision is preserved with strikethrough at [§Decision (Round 1 — superseded by Round 2 below)](#decision-round-1--superseded-by-round-2-below) per [`AGENTS-MD-bb7fe2c5aa`](../../../AGENTS.md#round-1-strikethrough-preservation-in-decision-briefs). Round-1 reviewer return digests preserved verbatim at [§Appendix A](#appendix-a--round-1-reviewer-return-digests-preserved-for-traceability).

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
  candidate-mandate: <greenfield | brownfield | unified-attempt>
  scenario-set-source: <corpus | candidate-derived | hybrid>
  mandate-scenario-split:                  # R6 #1 amendment — required for all candidates
    greenfield: <N>                        # ≥3 for unified-attempts; 0 for brownfield-mandate
    brownfield: <M>                        # ≥3 for unified-attempts; 0 for greenfield-mandate
  expected-evaluator-time-days: <N>
  falsifying-outcome: |
    <Verbatim ≤80-word statement of the concrete result pattern that would
    falsify the candidate's methodology against the lean-eval. Must be
    machine-checkable in principle: a metric crossing a threshold, a
    behavior class appearing in trajectories, or a specific failure mode
    surfacing. NOT "the evaluator judges the methodology inadequate".
    Names the SAME metric + threshold + artifact-state location as §3
    (R5 #2 consistency requirement).>
  phase-7-cite-obligations:
    high-confidence-mandatory:
      - <cite-obligation-1 from the per-candidate mapping table below>
    medium-confidence-design-inputs:
      - <cell-id from backfill-notes/audit-silent-absorption.md §B.1>
    historian-design-inputs:
      - <H-N gap-id from aggregation §4.1>
  ```
- **§1 Candidate + scenario set** (~400-600 words). Restates the candidate's mandate / axis / entry-mode (one paragraph) + names the scenario set (where it comes from — corpus subset, candidate's own scenario-derivation primitives, or a hybrid). For candidates whose spec already carries a scenario-derivation primitive (e.g., U-A's Compound-Knowledge Atelier, BF-L's P-13 maintenance loop), cite that primitive's spec §-anchor verbatim. Names ≥5 specific scenarios with one-sentence each. **For unified-attempt candidates (R6 #1 amendment): scenario set MUST be partitioned into a `### Greenfield-mandate scenarios` subsection (≥3 scenarios) and a `### Brownfield-mandate scenarios` subsection (≥3 scenarios)**; the YAML `mandate-scenario-split` field counts must match.
- **§2 Success criteria** (~400-600 words). What "the candidate passes the lean-eval" looks like, in concrete terms. Per-scenario success criteria + overall pass condition. Avoid hand-waving ("the methodology produces good code"); name behaviors, artifacts, or metrics.
- **§3 Falsifying outcome** (~200-300 words; LOAD-BEARING per [§Falsifier discipline](#falsifier-discipline-load-bearing) below). The single most concrete result that would falsify this candidate's methodology under this lean-eval. The `falsifying-outcome:` YAML field is the verbatim ≤80-word distillation; §3 expands with rationale (why this falsifier and not another) + how it differs from the success-criteria negation (failing criteria might be implementation noise; the falsifier is the methodology's load-bearing claim being wrong).
- **§4 Failure modes the test surfaces** (~400-600 words). For each of the ≥5 scenarios in §1, names the failure modes the scenario is designed to reveal. Cites the candidate's spec §5 (failure modes) verbatim where applicable. Per [`AGENTS-MD-bf4431be57`](../../../AGENTS.md#verbatim-text-pull-when-citing-binding-rule-tables): if the brief cites the candidate's `specs/<id>.md` §0 ADR-citation index or §5 failure-mode table, use verbatim text-pull, not paraphrase.
- **§5 Evaluator time + protocol** (~300-500 words). Names the expected evaluator time (per [v1.2 plan](../../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md#phase-8--lean-eval-design-one-brief-per-candidate-first-pressure-test-surface-revised-in-v12), ~1 day per candidate). Names the protocol: how the evaluator runs the scenarios, what artifacts they collect, what threshold/judgment they apply for the falsifying-outcome and success-criteria.
- **§6 Open critique references** (~200-400 words). Per [`specs/<id>.md` §6](../specs/) (open carries): the candidate's open critique findings that this lean-eval is designed to pressure-test. Cite each by §-anchor.
- **§7 Phase-7 cite obligations honored** (~300-500 words). For each high-confidence cite obligation in this candidate's row of [§Phase-7 cite-obligation propagation table](#phase-7-cite-obligation-propagation-load-bearing-pre-authored-mapping) below, names how the lean-eval brief honors it (the cite appears verbatim in §1 or §4 or §6 with archive `path` + §-anchor). For each medium-confidence design input from [`backfill-notes/audit-silent-absorption.md` §B.1](../backfill-notes/audit-silent-absorption.md): if the lean-eval scenario design touches the TBD cell, name how (one paragraph). For each historian load-bearing gap touching this candidate: name how the lean-eval surface engages the gap (if at all).
- **§8 References** (mandatory; relative paths only per [`AGENTS.md § Internal document references`](../../../AGENTS.md#internal-document-references)). Floor: candidate's spec + candidate's back-fill notes + this brief + the candidate's substrate-requirements summary + any archive files cited + the relevant ADRs.

**Word budget per lean-eval brief (tiered per Phase-7 advisory carry-forward; pre-folded at Round 1 per the [Phase-7-close handoff §Open questions item 2](../SESSION-HANDOFF-2026-05-27-phase-7-close.md#open-questions--suggestions-for-the-next-agent); Heavy ceiling tightened in Round 2 per R3 #5 amendment).**

| Tier | Word budget | Candidates | Rationale |
|---|---|---|---|
| Light | 5000-6500 | GF-S, GF-M, GF-C, BF-S | Single-dominant or no-single lineage; smaller cite-obligation surface (0-2 high-confidence mandatory cites each) |
| Heavy | 5500-**7200** | BF-M, BF-L, U-A, U-B, U-C, D7-U-1 | Multiple-lineage candidates; larger cite-obligation surface (1-3 high-confidence mandatory cites each); unified-attempts carry the DEC-1.a falsification load. **Heavy ceiling tightened from 7500 → 7200 in Round 2** (aligns to Phase-7 actual median; discourages continued drift). |

Calibrated against Phase-7 actuals (median Light ~6400, median Heavy ~7200; **source per [aggregation §6.1 word-budget overrun pattern](../backfill-notes.md#61-word-budget-overrun-pattern--auto-007-round-3-calibration-warranted)** — R4 #3 amendment cite). Subagent runs `wc -w` against its tier's bounds in self-check item (a); over-budget triggers a return-digest flag for lead-agent review per [§Over-budget subagent recovery](#sub-wave-coordination-protocol) below.

**Self-check rubric** per [`AGENTS-MD-e74e4811a2`](../../../AGENTS.md#self-check-rubric-requires-tool-verification-for-measurable-items). Subagent runs **items (a)-(g); item (h) DROPPED in Round 2** per R3 #2 (cite-obligation honoring is enforced by the falsification-designer auditor + post-fanout aggregation; 3-layer enforcement was over-engineering):

- (a) `wc -w` on its lean-eval file to verify word budget compliance against its tier.
- (b) `ls` on every cited v3 file path (`specs/<id>.md`, `backfill-notes/<id>.md`, any ADR files, any archive files) to verify the file exists.
- (c) `grep` for §1-§8 headers to verify section structure.
- (d) `grep "falsifying-outcome:" <its file>` to verify the YAML field is populated AND `grep -c "^  "` (or equivalent) on the field's value to verify ≤80 words.
- (e) `grep -c "phase-7-cite-obligations:" <its file>` to verify the YAML field exists.
- (f) For each binding rule table cited (e.g., the candidate's `specs/<id>.md` §0 ADR-citation index): `grep -F '<verbatim cell text>' <source-anchor>` to verify exact-text-pull per [`AGENTS-MD-bf4431be57`](../../../AGENTS.md#verbatim-text-pull-when-citing-binding-rule-tables). If no binding rule table is cited, item (f) self-reports `n/a` with rationale.
- (g) `grep -cE "##? §[1-8]"` to verify exactly 8 §-headers (excluding YAML frontmatter and H1).
- ~~(h) Per-candidate cite-obligation check~~ — **DROPPED in Round 2 per R3 #2 amendment.** Enforcement migrates to the falsification-designer auditor (per-brief verdict at Wave 8.1.b) + post-fanout aggregation (lead-agent cross-check before Wave 8.2).

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

## Decision (Round 1 — superseded by Round 2 below)

~~**Option A. Per-candidate parallel fanout (Wave 8.1, 9 sibling subagents) + per-candidate-paired bias-guards concurrent (Wave 8.1.b, 20 subagents — see [§Bias-guard concurrency shape decision point](#bias-guard-concurrency-shape-decision-point) for fallback to 2 cross-candidate auditors if harness capacity is a concern) + hypothesis-falsifier serial after Wave 8.1 closes (Wave 8.1.c, 1 subagent) + Wave 8.2 cross-candidate evaluator-brief (lead-agent-authored by default), lead-agent exemplar first with self-check gate, tiered word-budget (Light 5000-6500 / Heavy 5500-7500), pre-authored Phase-7 cite-obligation propagation table.**~~ Round 1 preserved per [`AGENTS-MD-bb7fe2c5aa`](../../../AGENTS.md#round-1-strikethrough-preservation-in-decision-briefs); superseded by [§Decision (Round 2)](#decision-round-2) below. Three Round-1 reviewers returned `accept-with-named-amendments` and converged on (a) A.1 → A.2 default flip + (b) Wave 8.1.b / 8.2 PR split + (c) falsifier-discipline tightening (R2). See [§Round-2 final amendments folded](#round-2-final-amendments-folded) for the full list.

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

Each sub-wave fires from a separate stacked branch. **Round 2 splits Wave 8.1.b and Wave 8.2 into separate PRs** (R1 #4 + R3 #3 converged amendment) for clean rewind boundary.

- **Exemplar (PR 3)** branch: `claude/phase-8-exemplar`. Lead agent authors `lean-evals/<exemplar-id>.md` and (if not already created) `lean-evals/` directory + `lean-evals/.gitkeep`. Lead-agent self-checks (a)-(g) on exemplar before fanout dispatch (item h dropped in Round 2).
- **Wave 8.1 (PR 4 omnibus)** branch: `claude/phase-8-fanout-omnibus`. 9 per-candidate subagents write to `lean-evals/<id>.md`. All disjoint files.
- **Wave 8.1.b (PR 5 omnibus)** branch: `claude/phase-8-bias-guards`. 3 cross-candidate auditors fire in parallel SERIAL-AFTER-Wave-8.1: domain-practitioner writes `lean-evals/audit-domain-practitioner.md`; falsification-designer writes `lean-evals/audit-falsification-designer.md`; hypothesis-falsifier writes `lean-evals/audit-hypothesis-falsifier.md`. All disjoint files. Per A.2′ shape (Round-2 default; supersedes A.1 from Round 1).
- **Lead-agent falsifier cross-check (post-PR-5)** — 5-minute lead-agent task between PR 5 merging and PR 6 firing. Lead agent reads `audit-falsification-designer.md`, identifies any "rewrite §3" verdicts, and re-authors the failing briefs (in-place on `claude/phase-8-fanout-omnibus`'s merged content, via a small fix PR if needed). If 0 rewrite verdicts, no fix PR.
- **Wave 8.2 (PR 6)** branch: `claude/phase-8-cross-candidate`. Lead agent (or subagent fallback if ≥3 unified-attempt rewrite verdicts) authors `lean-evals/00-cross-candidate.md` quoting the hypothesis-falsifier pattern verbatim.
- **Phase-8-close handoff (PR 7)** branch: `claude/phase-8-handoff`. New `SESSION-HANDOFF-2026-05-28-phase-8-close.md` + `AGENT-ENTRY.md` Section-2 update.
- **Run summary + retrospective (PR 8)** branch: `claude/phase-8-summary-retro`. Top-level `run-summary-2026-05-28-phase-8.md` + `retrospective/2026-05-28-<PPP>/` full-package directory per [`AGENTS-MD-1d7c94415e`](../../../AGENTS.md#full-retrospective-package-lean-mode-is-anti-pattern).

**File uniqueness invariant**: each lean-eval subagent's file is named per the candidate's ID (`gf-s.md` / `gf-m.md` / `gf-c.md` / `bf-s.md` / `bf-m.md` / `bf-l.md` / `u-a.md` / `u-b.md` / `u-c.md` / `d7-u-1.md`). Bias-guard subagents write to fixed audit filenames. Exemplar candidate's file is authored by lead agent on PR 3 before fanout.

**Conflict protocol**: if a per-candidate subagent finds its target brief file already exists or the branch tip moved unexpectedly, surface in return digest; do not force-push. Lead agent reconciles at Wave 8.1 close.

**Wave 8.1 re-dispatch archive protocol (R5 #6 amendment).** If a Wave 8.1 brief needs full re-dispatch (e.g., a subagent stalled, returned truncated output, or produced an unfixable defect), existing audit files in `lean-evals/` are archived to `lean-evals/archived/<UTC-timestamp>/` BEFORE Wave 8.1.b re-fires. This prevents stale audit verdicts from contaminating the re-fired Wave 8.1.b auditors' reads. Single-brief re-dispatches (one candidate at a time) do NOT trigger the archive (the audit files are still relevant to the other 8 briefs); only full-Wave-8.1 re-dispatch does.

**Over-budget subagent recovery (R5 #5 amendment).** Self-check item (a) flags over-budget but the file is already written; the brief did not specify recovery action. Round-2 amendment: subagent over-budget → return-digest flag → lead-agent re-dispatches that subagent ONLY (not the whole wave) with explicit truncation guidance ("re-author within tier bounds; cite the over-budget section's content as a discard candidate"). Do not silently accept over-budget files. Re-dispatch on a stacked branch for the affected candidate; commit the re-authored file as a fix-PR if Wave 8.1 omnibus has already opened.

**Total subagents this run (Round-2 revised):** 9 (per-candidate fanout, excluding exemplar candidate) + 3 (cross-candidate bias-guards under A.2′ default) + 0 or 1 (cross-candidate evaluator-brief — lead-agent by default; subagent if ≥3 unified-attempt rewrite verdicts) + 6 adversarial reviewers (Round 1 + Round 2 of this brief) + ~3-4 retrospective-package authoring subagents at run close = **~22-23 subagents total for Phase 8** (down from Round-1's ~21-39 range; A.2′ flip resolves the upper-bound uncertainty).

**PR-cap math (Round-2 revised):** 1 (envelope #194, already opened) + 1 (this brief, R2 push) + 1 (exemplar) + 1 (Wave 8.1 fanout omnibus) + 1 (Wave 8.1.b bias-guards omnibus) + 0-1 (cross-check fix PR, conditional) + 1 (Wave 8.2 cross-candidate) + 1 (handoff) + 1 (summary+retro) = **8 PRs (9 if cross-check fix PR fires) against ≤15 Phase-8 budget cap**. Margin: 6-7 PRs.

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

**Pattern-mandate alignment note (R6 #4 amendment):** the asymmetric historian-design-input assignment is intentional, not a candidate-quality signal. H-2/H-8 (self-improving prompts pattern + role) is a greenfield-shaped methodology pattern → assigned to GF-S, GF-M, and U-A (the unified-attempt with the strongest greenfield-Atelier lineage). H-3 (Pulse report: production-trace-to-spec-amendment) is a brownfield-shaped pattern → assigned to BF-L (whose P-13 maintenance loop is the closest analog). No greenfield analog of Pulse exists in the archive; no brownfield analog of self-improving-prompts is load-bearing. Subagents authoring U-B / U-C / D7-U-1 briefs that find pattern-mandate gaps may surface them as Phase-8-followup carry-forwards but the absence of a pre-mapped design input is not a defect.

## Falsifier discipline (load-bearing)

**This discipline is what makes Phase 8 the actual pressure-testing surface** rather than another internal-consistency exercise. **Round-2 amendments (R2 #1-#4) tighten the discipline from "ceremony-risk" to "load-bearing".** The discipline has three load-bearing components plus four mechanical sub-rules:

1. **Mandatory `falsifying-outcome:` YAML frontmatter field** in every per-candidate `lean-evals/<id>.md`. The field value is a verbatim ≤80-word statement of the concrete result pattern that would falsify the candidate's methodology against the lean-eval. The falsification-designer auditor's first check is `grep "falsifying-outcome:" architectures/v3/lean-evals/*.md` — every file must have this field, populated, non-empty.

2. **Mandatory §3 falsifying-outcome statement** in every per-candidate brief. Expands the YAML field's ≤80 words into ~200-300 words of rationale: why this falsifier and not another; how it differs from the success-criteria negation (failing criteria might be implementation noise; the falsifier is the methodology's load-bearing claim being wrong); machine-checkability constraints. Per the [autonomous-run skill § Working-mode reminders](../../../.claude/skills/autonomous-run/SKILL.md#working-mode-three-rules): briefs that hand-wave the falsifier get rewritten.

3. **Mandatory cross-candidate DEC-1.a falsifying result pattern named before-simulator-runs-but-after-brief-authoring** in the hypothesis-falsifier output AND quoted verbatim in the cross-candidate evaluator-brief. The hypothesis-falsifier reads all 10 lean-eval briefs AFTER they are finalized (serial post-Wave-8.1), names the cross-candidate pattern that would falsify DEC-1.a, and commits the pattern to `lean-evals/audit-hypothesis-falsifier.md`. The cross-candidate evaluator-brief in Wave 8.2 quotes this pattern verbatim in its §X falsifying-result-pattern section, so post-hoc reinterpretation of the DEC-1.a outcome (relative to the simulator run) is mechanically blocked.

   **Honest framing (R2 #4 amendment):** Naming the pattern AFTER reading the 10 finalized briefs means the cross-candidate falsifier can be silently tuned to match patterns the 10 briefs already display. The discipline blocks reinterpretation of the simulator-run, NOT reinterpretation relative to the brief corpus. **The hypothesis-falsifier audit file's first section MUST state explicitly how the auditor guarded against fitting the observed pattern of the 10 briefs** — e.g., by drafting the pattern independent of the 10 briefs first, then verifying applicability; or by naming a falsifier the briefs would NOT predict. Without this self-account, the "before-simulator-runs" framing is honest but the audit is not.

### R2 #1: Falsification-designer concreteness rubric (3-item; mechanical)

The falsification-designer auditor's verdict on each per-candidate `falsifying-outcome:` field AND §3 statement is **pass/fail on each of 3 mechanical items**:

| Item | Pass criterion | Example pass | Example fail |
|---|---|---|---|
| **(i) Names a metric** | The statement names a countable quantity, a rate, or a categorical outcome | "knowledge-promotion-rate" / "%-of-scenarios-passing-success-criteria" / "category enum {playbook, correction, pattern}" | "the methodology produces good code" |
| **(ii) Names a directory, artifact state, or trajectory class** | The statement names a specific place where the metric can be observed | "`solutions/` directory state at scenario close" / "spec amendment commits in `architectures/v3/specs/`" / "the trajectory of agent actions during scenario N" | "the evaluator's overall impression" |
| **(iii) Names a threshold** | The statement names a numeric or categorical bar that determines pass/fail | "zero promoted patterns" / "≥80% of scenarios pass" / "any failure-mode F1-F33 surfaces" | "fewer than expected" |

**Pass = ≥2 of 3 on items (i)-(iii) AND mandatory pass on item (iv).** A statement failing items (i)-(iii) (0 or 1 pass) OR failing item (iv) triggers a "rewrite §3" verdict on that candidate. Lead-agent re-authors the failing brief before Wave 8.2 (per the [§Lead-agent falsifier cross-check](#decision-round-2)).

**Item (iv) (R5 #2 amendment, MANDATORY not 2-of-3):** **§3-vs-YAML consistency.** The §3 200-300-word falsifying-outcome statement and the YAML `falsifying-outcome:` ≤80-word distillation name the SAME metric AND the SAME threshold AND the SAME artifact-state location. If §3 says "knowledge-promotion-rate from `solutions/` directory state, threshold zero" but YAML says "trajectory class X exceeds threshold Y", the falsifier discipline fails — a subagent could write a YAML falsifier and an inconsistent §3 and pass items (i)-(iii) trivially. Required to prevent silent drift between the two falsifier surfaces.

This rubric is **mechanical** — the falsification-designer auditor applies items (i)-(iv) identically across 10 candidates rather than 10 different interpretations of "concrete".

### Verdict-token format in falsification-designer audit file (R5 #3 amendment)

The falsification-designer auditor's per-candidate verdict in `lean-evals/audit-falsification-designer.md` uses a literal token format so the lead-agent cross-check + the cross-candidate evaluator-brief subagent-fallback condition can both grep deterministically:

```
## <candidate-id>

verdict: <one of: pass / rewrite-§3>
rubric-items:
  (i)-metric: <pass | fail>
  (ii)-artifact-state: <pass | fail>
  (iii)-threshold: <pass | fail>
  (iv)-§3-yaml-consistency: <pass | fail>
mandate-scenario-split-verified: <pass | fail | n/a (non-unified-attempt)>
notes: <≤30 words rationale; if verdict is rewrite-§3, names which items failed>
```

Lead-agent cross-check uses `grep -c "verdict: rewrite-§3"` to count rewrite-verdicts. Cross-candidate evaluator-brief subagent-fallback uses `grep -B 2 "verdict: rewrite-§3"` to identify which candidate-IDs need re-authoring. **For unified-attempts, `mandate-scenario-split-verified` is an additional check** (per R6 #1: verifies the §1 partition was respected and YAML `mandate-scenario-split` field is populated).

### R2 #2 + #3: DEC-1.a falsifying pattern canonical terms (committed in THIS brief)

Per R2 amendments #2 and #3: the load-bearing terms in the DEC-1.a falsifying result pattern are committed here, not delegated to the hypothesis-falsifier. The hypothesis-falsifier USES these terms when naming the pattern.

**Canonical "escape-hatch" enumeration (R2 #2 + R6 #5 structural-rider amendment):** A candidate's lean-eval result "invokes an escape-hatch" if any of the following apply:

1. **Out-of-mandate scope claim** — the candidate's lean-eval result claims a scenario is out of the candidate's mandate (e.g., "this brownfield scenario is greenfield-only; not applicable to U-A's mandate"). Per [candidate-registry.md § Candidate set](../candidate-registry.md), unified-attempt candidates (U-A / U-B / U-C / D7-U-1) explicitly claim BOTH mandates; an out-of-mandate scope claim from a unified-attempt is structurally a failure to deliver on the unified-attempt claim. **Structural rider (R6 #5):** for a unified-attempt, declaring an entire mandate-bloc out-of-scope is structurally a failure to deliver on the unified-attempt claim; ≥1 mandate-bloc with <3 scenarios scored fails R2 #3 (a′) by construction.
2. **Scenario-skip** — the candidate's lean-eval skips a scenario rather than producing a result on it (any reason). Scenarios skipped by the brief's own §1 design (e.g., "this candidate's scenario set is only 4 scenarios") do NOT count; mid-run skips by the evaluator do count.
3. **Criterion-substitution** — the candidate's lean-eval declares "pass" on a scenario by substituting a different success criterion than the one named in §2 of its lean-eval brief. (Re-interpreting §2 mid-run is forbidden; if §2 is defective, the brief is rewritten not the criterion swapped.)

**Canonical "pass cleanly" definition (R2 #3 + R6 #2 partitioned-mandate amendment):**

**For non-unified candidates** (GF-S / GF-M / GF-C / BF-S / BF-M / BF-L), a lean-eval result "passes cleanly" iff BOTH:

- **(a) Quantitative gate:** ≥80% of the brief's §1 named scenarios pass the §2 success criteria.
- **(b) Falsifying-outcome gate:** the brief's §3 `falsifying-outcome` is NOT triggered on any scenario.

**For unified-attempt candidates** (U-A / U-B / U-C / D7-U-1; R6 #2 amendment): mandate-blind ≥80% is insufficient for DEC-1.a — a unified-attempt brief with 6 greenfield + 4 brownfield scenarios where 8/10 pass could pass the gate even if every brownfield scenario fails, masking exactly the "methodology serves one mandate not both" pattern DEC-1.a is designed to detect. Therefore a unified-attempt lean-eval result "passes cleanly" iff ALL of:

- **(a′) Partitioned quantitative gate:** ≥80% of `greenfield-mandate-scenarios` (from the §1 partition) pass the §2 success criteria AND ≥80% of `brownfield-mandate-scenarios` (from the §1 partition) pass the §2 success criteria.
- **(b) Falsifying-outcome gate:** the brief's §3 `falsifying-outcome` is NOT triggered on any scenario.

**Mandate-partition requirement for unified-attempt §1 scenario sets (R6 #1 amendment):** every unified-attempt brief MUST partition its §1 scenario set into a `greenfield-mandate-scenarios` subsection (≥3 scenarios) and a `brownfield-mandate-scenarios` subsection (≥3 scenarios). The partition is named in the YAML frontmatter:

```yaml
mandate-scenario-split:
  greenfield: N    # ≥3 for unified-attempts; 0 for mandate-aligned candidates
  brownfield: M    # ≥3 for unified-attempts; 0 for mandate-aligned candidates
```

Non-unified candidates set their non-mandate field to 0 (e.g., GF-S sets `greenfield: N / brownfield: 0`). Subagents authoring unified-attempt briefs MUST partition; subagents authoring mandate-aligned briefs MAY use a single bloc named after their mandate.

Conditions are committed in this brief and apply uniformly across all 10 candidate lean-evals (per-mandate-form for non-unified; per-bloc-form for unified-attempts).

### R2 illustrative falsifier statements (REVISED from Round-1 versions)

Per-candidate subagents and the hypothesis-falsifier author their own falsifier statements. The illustrative statements below are the **form** subagents follow — not binding content.

> **For U-A (illustrative, passes 3-of-3 rubric items):** "U-A's Compound-Knowledge Atelier produces zero promoted patterns (`solutions/` directory state at scenario close) after 5 brownfield scenarios where the existing codebase's documentation explicitly contradicts the candidate's promotion-criteria."
> *(Item i: 'zero promoted patterns' = metric ✓. Item ii: '`solutions/` directory state at scenario close' = artifact state ✓. Item iii: 'zero' = threshold ✓.)*

> **For DEC-1.a falsifying result pattern (illustrative, uses canonical escape-hatch + partitioned pass-cleanly terms verbatim; R6 #3 amendment):** "If ≥2 unified-attempt candidates (U-A / U-B / U-C / D7-U-1) pass cleanly per-mandate (per the partitioned 'pass cleanly' definition above for unified-attempts: ≥80% of `greenfield-mandate-scenarios` pass AND ≥80% of `brownfield-mandate-scenarios` pass AND falsifying-outcome NOT triggered on any scenario), AND the lean-eval result does not invoke any of the 3 escape-hatches enumerated above (including the structural rider for unified-attempts: ≥1 mandate-bloc with <3 scenarios scored fails by construction), DEC-1.a is falsified — at least one methodology serves both mandates."

The illustrative statements above are NOT binding — per-candidate subagents and the hypothesis-falsifier author their own. The point is the **form**: concrete, mechanical (passes the 3-item rubric), and pre-committed using canonical escape-hatch + pass-cleanly terms.

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

**Threshold trigger (Round-2 revised per R1 #5):** **≥1 *unified-attempt* candidate's** lean-eval brief flagged by falsification-designer as "rewrite §3" + cannot be re-authored in-run. **Restricted to unified-attempt candidates** (U-A / U-B / U-C / D7-U-1) because the Phase-8 falsification surface is for DEC-1.a; only the 4 unified-attempts carry the DEC-1.a load. A failed GF-S / GF-C / GF-M / BF-S / BF-M / BF-L lean-eval is a quality defect on that candidate but does NOT block DEC-1.a falsification; lead agent re-authors at run-close as a non-blocker. Restricting the threshold to unified-attempts prevents over-aggressive triggering.

(Round-1 threshold was "≥1 candidate", any mandate — superseded.)

## Exemplar pre-fanout self-check gate (load-bearing)

Before dispatching Wave 8.1 / Wave 8.1.b, the lead agent **runs self-check items (a)-(h) on the exemplar** and records pass/fail in this brief's [§Exemplar pre-fanout self-check results](#exemplar-pre-fanout-self-check-results) (subsection appended at exemplar-commit time). **Failure on item (d)** (`falsifying-outcome:` field populated AND ≤80 words) or item (h) (high-confidence cite obligations honored) **blocks fanout** — lead agent re-authors the exemplar before any sub-wave fires. Mirrors the Phase-6 U-C / Phase-7 BF-S exemplar gate pattern.

## Honest acknowledgements (Round 2)

Per [`AGENTS-MD-ffe35aa500`](../../../AGENTS.md#honest-acknowledgements-for-pre-round-2-wave-firing): Round-2 deviations acknowledged for the durable audit trail.

1. **No wave fired pre-Round-2.** Round-1 → Round-2 transition happened entirely within this brief's lifecycle (Round-1 commit `54438e3`; Round-2 commit pinned below). No per-candidate or bias-guard subagent fired between rounds. The pre-Round-2-wave-firing acknowledgement rule does not directly apply here, but the principle of explicit honesty about the brief's audit-trail state does.

2. **Round-1 reviewer convergence drove load-bearing amendments.** R1 (pre-mortemer) + R3 (cost-hawk) converged on flipping the bias-guard default from A.1 (per-candidate-paired) to A.2′ (cross-candidate-rollup, 3 auditors serial-after). This convergence was strong enough that the Round-2 decision flips the default rather than treating A.1/A.2 as a runtime decision. R2 (falsification-designer) drove the falsifier-discipline tightening (3-item rubric + escape-hatch enumeration + pass-cleanly definition + reframed "in advance" claim) — single-reviewer-driven but the amendments are mechanical (rubric, enumeration, definition), so single-reviewer confidence is sufficient.

3. **A.1 fallback REMOVED in Round 2.** The Round-1 brief named A.1 as default with A.2 as fallback. Round 2 inverts: A.2′ is the only shape; A.1 is rejected for both the timing-model reason (R1 #2) and the cost reason (R1 #1 + R3 #1). If a Round-2 reviewer surfaces a reason A.1 should still be admissible, they can amend.

4. **Cross-candidate evaluator-brief authorship subagent-fallback criterion is concrete.** Round 1 said "subagent-dispatched if context budget approaches 70%" (vague). Round 2 says "subagent-dispatched if ≥3 unified-attempt briefs triggered 'rewrite §3' verdicts during Wave 8.1.b" (concrete, mechanical). Improves auditability of the runtime decision.

5. **Self-check item (h) drop is conservatively scoped.** R3 #2 amendment drops item (h) (per-candidate cite-obligation honoring check). The enforcement migrates to the falsification-designer auditor + post-fanout aggregation. If both layers fail to catch a missing cite obligation, the omission would surface in the Phase-8-close handoff or at the morning summary. Acceptable two-layer enforcement.

6. **Time-anchored git log at Round-2 commit time** (per the pre-folded [`AGENTS-MD-4a7c2e9f6b`](../../../retrospective/2026-05-27-191/AGENTS-MD-4a7c2e9f6b-adversarial-review-amendment-inheritance.md) draft):
   - **Round-1 commit SHA:** `54438e3` (this brief, Round 1).
   - **Round-2 commit SHA:** `7e685c5`.
   - **origin/main tip at Round-2 commit time:** `99053b0` (Merge PR #193, dispatch prompt phase 8) — unchanged from Round-1 commit time.
   - **Phase-8 envelope commit:** `cce0f73` (merged in PR #194).

## Honest acknowledgements (Round 1)

Per [`AGENTS-MD-ffe35aa500`](../../../AGENTS.md#honest-acknowledgements-for-pre-round-2-wave-firing) (adapted): this Round-1 brief acknowledges the following deviations / context items honestly, so Round-1 reviewers operate from a clear baseline:

1. **5 Phase-7 retrospective AGENTS-MD-* rules NOT adopted into canonical AGENTS.md** (user-elected; surfaced via AskUserQuestion at envelope-time and deferred). This brief applies the patterns informally and references the retrospective drafts. **Canonical-grep guidance for future agents (R5 #4 + R4 #1 amendments):** the 5 rule hashes below will NOT match a `grep` of canonical `AGENTS.md`; they are durable IDs in retrospective directory paths. Use `grep -rn '<hash>' retrospective/2026-05-27-191/` not `grep '<hash>' AGENTS.md`. **Anchor-resilience note (R4 #1):** these citations dangle if `retrospective/2026-05-27-191/` is reorganized or pruned; mitigation = preserve the directory as-is until the rules are adopted into canonical AGENTS.md or explicitly superseded.
   - [`AGENTS-MD-4a7c2e9f6b`](../../../retrospective/2026-05-27-191/AGENTS-MD-4a7c2e9f6b-adversarial-review-amendment-inheritance.md) — adversarial-review amendment-inheritance: pre-folded the auto-007 audit-trail amendments at Round-1 authoring time (commit-SHA pinning, time-anchored honest-acks, Appendix A scaffold, 3-tier verdict commitment, TL;DR structure, PR-webhook commitment, skip-discipline auditability). Cannot cite by stable AGENTS-MD-<hash> in canonical AGENTS.md.
   - [`AGENTS-MD-8e5d3a7c4b`](../../../retrospective/2026-05-27-191/AGENTS-MD-8e5d3a7c4b-phase-followup-bias-guard-fold.md) — Phase-followup bias-guard fold: no Phase-7-followup deferral fired so this rule has no in-Phase-8 obligation, but it shaped the bias-guard mandate scopes in [§Decision (Round 1)](#decision-round-1) above.
   - [`AGENTS-MD-5b3e8a1c2f`](../../../retrospective/2026-05-27-191/AGENTS-MD-5b3e8a1c2f-silent-absorption-confidence-threshold.md) — silent-absorption confidence-threshold: the falsification-designer auditor's verdict-application uses an analogous pattern (verdict overrides per-candidate brief only if `high` machine-checkability concern; `medium` triggers re-author flag; `low` informational). Folded into the rubric informally.
   - [`AGENTS-MD-7d9c4e1b3a`](../../../retrospective/2026-05-27-191/AGENTS-MD-7d9c4e1b3a-matrix-flag-over-spec-patches.md) — matrix-flag over spec-patches: not directly applicable to Phase 8 (no spec patches in scope), but if hypothesis-falsifier surfaces a "rewrite brief vs flag in cross-candidate" question, the matrix-flag pattern applies.
   - [`AGENTS-MD-2f8a6c9d51`](../../../retrospective/2026-05-27-191/AGENTS-MD-2f8a6c9d51-per-candidate-engagement-over-blanket-skip.md) — per-candidate engagement over blanket-skip: no prior-phase defaults are skipped in Phase 8 (Phase 8 reads each candidate's spec + back-fill notes fresh); rule does not bind.
2. **Tier-table calibration (Light 5000-6500 / Heavy 5500-7500)** is pre-folded at Round-1 per the [Phase-7-close handoff §Open questions item 2](../SESSION-HANDOFF-2026-05-27-phase-7-close.md#open-questions--suggestions-for-the-next-agent) recommendation. Round-2 reviewers are invited to challenge if they think Phase-7 actuals (median Light 6400 / Heavy 7200) warrant a different calibration.
3. **Bias-guard concurrency shape (A.1 per-candidate-paired by default; A.2 cross-candidate-rollup as fallback)** is a runtime decision at exemplar-commit time, not a Round-1-bound decision. Round-2 reviewers may amend the criterion if they think the A.1 / A.2 choice should be made at Round 2 instead.
4. **Cross-candidate evaluator-brief authorship (lead-agent-default; subagent-fallback if context approaches 70%)** is a runtime decision at Wave-8.1.c close, not a Round-1-bound decision. Round-2 reviewers may amend.
5. **Time-anchored git log at Round-1 commit time**: per the pre-folded [`AGENTS-MD-4a7c2e9f6b`](../../../retrospective/2026-05-27-191/AGENTS-MD-4a7c2e9f6b-adversarial-review-amendment-inheritance.md) draft (rule 4 of the amendments pre-folded), the Round-1 commit SHA + the most-recent main commit at Round-1 commit time are pinned here. Filled in immediately post-commit:
   - **Round-1 commit SHA:** `54438e3`
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

Per [`AGENTS-MD-bb7fe2c5aa`](../../../AGENTS.md#round-1-strikethrough-preservation-in-decision-briefs): Round-1 reviewer return text is preserved verbatim here, even though amendments have been folded into Round 2 above. Round-1 dispatch fired three real adversarial reviewer subagents per [`AGENTS-MD-d72e1a4f3c`](../../../AGENTS.md#adversarial-review-must-be-real-subagents) (no inline simulation); each was given the 3-tier verdict menu per [`AGENTS-MD-8a7029647f`](../../../AGENTS.md#adversarial-review-verdict-tiers).

### Reviewer 1 — pre-mortemer

**Verdict:** `accept-with-named-amendments` — five non-load-bearing amendments and **one load-bearing amendment** (A.1/A.2 fallback criterion).

**Pre-mortem failure narrative (verbatim, ≤600w):**

> Most likely failure (6 weeks out, load-bearing). Phase 8 closes with 10 lean-eval briefs in hand. The downstream evaluator runs U-B's lean-eval and U-B "passes" — but the falsifying-outcome statement reads "U-B fails to produce promoted patterns under the brownfield scenario set", which the evaluator now reads as success-criteria-negation re-skinned, not a load-bearing-claim falsifier. Walking back: at exemplar-commit time, the lead agent looked at GF-M's exemplar `falsifying-outcome:`, judged it "machine-checkable in principle" (a low bar — any sentence containing a noun and a number passes), and fired A.1 with 30 concurrent subagents. The falsification-designer subagents, each scoped to a single brief, had no cross-candidate visibility to notice that 6-of-10 falsifiers had collapsed into "success criteria negation in disguise". The hypothesis-falsifier, reading 10 finalized briefs serially after Wave 8.1 closes, surfaces the pattern — but by then the briefs are committed and a "rewrite §3" verdict at this stage triggers the Phase-8-followup deferral (threshold ≥1), and the run runs out of PR budget. **The seed was the §Bias-guard concurrency shape decision criterion**: "mechanically auditable" is not operationally defined, so the lead agent will default-bias to A.1 under capacity pressure.
>
> Second-likely failure (harness-level). A.1 dispatches 30 concurrent subagents against the documented ~20-25 practical limit. One or more subagents return with truncated output or 429-class errors. The omnibus PR loses bias-guard coverage for 2-3 candidates silently (since each bias-guard writes to a shared audit file with per-candidate sections, missing sections are easy to miss). The hypothesis-falsifier then reads briefs whose falsifier discipline was never audited.
>
> Third (timing race). The brief says bias-guards fire concurrent with per-candidate briefs and audit "the brief draft (when ready from the per-candidate subagent's first commit)". But subagents don't commit drafts mid-run — they return digests. The actual artifact is the omnibus-PR commit at fanout close. So bias-guards either (a) audit nothing real, or (b) become serial-after-fanout, collapsing the parallelism claim.

**Amendments (verbatim):**

1. **(LOAD-BEARING) Operationalize the A.1/A.2 criterion.** "Mechanically auditable" must mean: exemplar's `falsifying-outcome:` names a specific artifact path, metric name, or trajectory class AND a numeric threshold. If either is missing, fire A.2. Default lean should flip to A.2 under any ambiguity.
2. **(non-load-bearing) Fix the bias-guard timing model.** Bias-guards cannot read per-candidate "first commits" because subagents don't commit mid-run. Either: (a) bias-guards fire serial-after-Wave-8.1 (downgrading parallelism), or (b) per-candidate subagents are instructed to commit a §1+§3 draft at the 50% mark before continuing.
3. **(non-load-bearing) Add a falsifier cross-check at fanout close, before hypothesis-falsifier.** Lead agent runs a 5-minute check: for each `falsifying-outcome:`, does it name an artifact-path/metric/threshold? Catches the success-criteria-negation collapse before the hypothesis-falsifier serial step.
4. **(non-load-bearing) PR-cap stress test.** If Wave 8.1 returns ≥3 "rewrite §3" verdicts, the omnibus PR must split (rewrite-PR before audit-PR). Pre-authorize a PR-8 contingency now; 7+1=8 PRs against ≤15 cap is still comfortable.
5. **(non-load-bearing) Phase-8-followup threshold tightening.** ≥1 trigger is correct, but add: deferral fires only if the failed candidate is a **unified-attempt** (U-A/U-B/U-C/D7-U-1). A failed GF-S/GF-C lean-eval doesn't block the DEC-1.a falsification surface; deferring on it over-triggers.
6. **(non-load-bearing) Cross-candidate evaluator-brief authorship default.** Make subagent-dispatch the default when ≥3 unified-attempt briefs triggered "rewrite §3" verdicts during Wave 8.1 — lead-agent context will be saturated by re-author cycles. Current "70% context" trigger is too vague.

### Reviewer 2 — falsification-designer

**Verdict:** `accept-with-named-amendments`. The discipline is real and load-bearing, not pure ceremony — but it has four specific weak points that subagents will exploit unless tightened.

**Falsifier-discipline assessment (verbatim, ≤600w):**

> The illustrative falsifiers are uneven. The U-A example ("knowledge-promotion-rate is machine-countable from `solutions/` directory state at scenario close") is genuinely machine-checkable in principle — it names a directory, a counting operation, a threshold ("zero promoted patterns"), and a denominator ("5 brownfield scenarios"). The DEC-1.a illustrative is much softer: **"no escape-hatches invoked"** and **"pass cleanly"** are both undefined. "Escape-hatch" has no enumeration; "cleanly" gets a parenthetical (≥80% of named scenarios pass) but the scenarios themselves vary across the 10 briefs, so the cross-candidate threshold isn't apples-to-apples. A hypothesis-falsifier writing in this register will produce a pattern that passes the `grep` but cannot be applied to a future simulator run without further adjudication.
>
> The falsification-designer auditor's verdict criterion is under-specified. The brief says the auditor checks "verbatim, concrete, not 'evaluator subjective judgment', and pre-committed". Three of those four are mechanical (grep / word-count / commit-order). "Concrete" is the load-bearing one and has **no rubric**. Across 10 candidates, 10 different auditor instances will draw the concrete/interpretive line differently. The §Bias-guard concurrency shape decision point even concedes this: "concrete-but-not-machine-checkable" is named as a real possibility that triggers the A.2 fallback — but no example, no taxonomy, no test.
>
> The "in advance" claim is partly compromised. The hypothesis-falsifier reads all 10 finalized briefs first, then names the falsifier "before evaluation runs". This is genuinely in advance of the simulator-harness, but it is **after** the per-candidate falsifiers are written — which means the cross-candidate falsifier can be silently tuned to match patterns the 10 briefs already display. The brief asserts "post-hoc reinterpretation is mechanically blocked" (§Falsifier discipline ¶3), but only blocks reinterpretation of the simulator run, not reinterpretation relative to the brief corpus. The honest framing is "named before evaluation, named after brief authoring" — Round 1 elides this.
>
> GF-S / GF-C have weaker falsifier load. They carry zero high-confidence mandatory cites and the brief gives them lighter cite-obligation §7 surfaces. But §3 falsifying-outcome is independent of cite obligations — the brief never says it's weaker for these candidates. This is actually fine; flag only because reviewers might miss it.
>
> Bias-direction prose is genuinely symmetric. I looked for anchoring; the lead-agent prose names DEC-1.a's working-hypothesis status correctly, names Phase-7 §6.4 as NEUTRAL, and the illustrative DEC-1.a falsifier is framed as falsifying-the-hypothesis ("≥2 candidates pass"), not confirming it. No detectable lean.

**Amendments (verbatim):**

1. Add to §Falsifier discipline a 3-item concreteness rubric for the falsification-designer (names a metric / names a directory or artifact state / names a threshold) — pass = ≥2 of 3.
2. Require the DEC-1.a illustrative to be replaced or supplemented with an enumeration of "escape-hatch" (e.g., "out-of-mandate scope claim, scenario-skip, criterion-substitution") before hypothesis-falsifier dispatch.
3. Define "pass cleanly" as a fixed cross-candidate threshold (e.g., ≥80% scenarios pass success-criteria AND falsifying-outcome NOT triggered) — committed in this brief, not delegated to hypothesis-falsifier.
4. Reframe the "in advance" claim in §Falsifier discipline ¶3 as "named before simulator runs but after brief authoring" and require the hypothesis-falsifier's audit file to state how it guarded against fitting the observed pattern.

### Reviewer 3 — cost/scope-hawk

**Verdict:** `accept-with-named-amendments`.

**Cost/scope assessment (verbatim, ≤600w):**

> Where the cost is justified. The 9-subagent per-candidate fanout (Wave 8.1), the lead-agent exemplar, the hypothesis-falsifier-serial, and the omnibus PR consolidation pattern are all calibrated against Phase-6/Phase-7 precedent — reusing a working shape is cheaper than reinventing. The pre-authored cite-obligation table (rejecting Option G's two-stage fanout) genuinely saves a whole sub-wave at the cost of ~30 minutes of brief-authoring; that math is clearly in the brief's favor. The falsifier-discipline triad (YAML field + §3 + hypothesis-falsifier) is what makes Phase 8 distinct from another consistency exercise, so its cost is the load-bearing cost.
>
> Where the cost is NOT justified. Three items leak budget:
>
> 1. **A.1 (20 bias-guard subagents) as default is the wrong default.** The brief's own §Cons admits 30 concurrent exceeds the harness's 20-25 practical limit. The trigger criterion ("mechanically auditable falsifying-outcome") is something the falsification-designer can already check in a roll-up — per-candidate isolation is not load-bearing here. A.2 (2 cross-candidate roll-ups) saves 18 subagents and stays under the harness limit. The brief should flip the default.
> 2. **Self-check item (h) duplicates falsification-designer + post-fanout aggregation work.** The cite-obligation honoring check is already enforced by the falsification-designer (per the brief's §Bias-guards block) and re-checked at aggregation. Three layers for one obligation is over-engineering.
> 3. **Wave 8.1.c + 8.2 omnibus PR conflates serial commits.** Hypothesis-falsifier (subagent) must land BEFORE cross-candidate evaluator-brief (lead-agent). One PR with two sequential commits muddies rewind boundary — if the evaluator-brief misquotes the falsifier pattern, you can't rewind cleanly without losing the falsifier. Split.
>
> Where the brief deserves credit for honesty. It explicitly names A.1 vs A.2, the 70%-context-budget escape on cross-candidate authorship, and the Phase-7 actuals against tier ceilings. The acknowledgements section is calibrated. The brief's word count (5778 — at auto-007's Round-2 length at Round-1) is a real concern but is the price of pre-folding the audit-trail amendments; net-net the work moves out of Round 2.

**Amendments (verbatim):**

1. **Flip A.1 / A.2 default.** A.2 (2 cross-candidate roll-up bias-guards) becomes default; A.1 (20 per-candidate-paired) is the fallback iff exemplar's falsifying-outcome is unambiguously machine-checkable.
2. **Drop self-check item (h).** Cite-obligation honoring is enforced by falsification-designer + aggregation; item (h) is redundant tool-call cost. Keep (a)-(g).
3. **Split Wave 8.1.c and Wave 8.2 into separate PRs.** Hypothesis-falsifier (subagent output) and cross-candidate evaluator-brief (lead-agent) commit on separate PRs for clean rewind boundary. Pushes PR-cap math to 8; still 7 under cap.
4. **Commit roll-up file shape now, not at exemplar-commit time.** Decide A.2 → one `audit-bias-guards.md` roll-up with per-auditor §-sections. Removes runtime decision; saves exemplar-time cycle.
5. **Tighten Heavy ceiling to 7200 (median actual), not 7500.** Light at 6500 is fine (200 over median — modest headroom); Heavy at 7500 (300 over) tolerates continued overrun. Align Heavy to median to discourage drift.
6. **Defer Phase-7 cite-obligation table population to exemplar-commit time.** Keep the table scaffold in this brief; populate at exemplar-commit (when lead agent is already in cite-mapping context). Cuts Round-1 brief by ~400 words.

(Note on R3 amendment #4: Round 2 folds it into the A.2′ flip — 3 separate audit files (`audit-domain-practitioner.md`, `audit-falsification-designer.md`, `audit-hypothesis-falsifier.md`) rather than 1 combined `audit-bias-guards.md`, because the 3 auditors have distinct mandates and per-auditor file scoping makes the falsification-designer's "rewrite §3" verdicts easier to grep. The intent — committing the roll-up file shape now rather than at exemplar-time — is honored.)

(Note on R3 amendment #6: rejected in Round 2 per [§Round-2 final amendments folded](#round-2-final-amendments-folded).)

## Appendix B — Round-2 reviewer return digests (preserved for traceability)

Round-2 dispatched 3 real adversarial reviewer subagents per [`AGENTS-MD-d72e1a4f3c`](../../../AGENTS.md#adversarial-review-must-be-real-subagents) (no inline simulation); each was given the 3-tier verdict menu per [`AGENTS-MD-8a7029647f`](../../../AGENTS.md#adversarial-review-verdict-tiers) and instructed to read the brief COLD (without consulting Appendix A Round-1 returns first). All 3 returned `accept-with-named-amendments`. Amendments are folded inline as post-Round-2 patches per [§Round-2-reviewer amendments folded](#round-2-reviewer-amendments-folded-post-round-2-patches) above.

### Reviewer 4 — regulator

**Verdict:** `accept-with-named-amendments`. Brief is "materially audit-defensible and would survive external compliance review with four amendments folded".

**Key findings (verbatim digest):**

> Strengths: Round-2 commit SHA `7e685c5` is back-filled; both rewind points (R1 `54438e3`, R2 `7e685c5`/`577cea8`) reachable; Appendix A preserves all three Round-1 reviewer returns verbatim with full pre-mortem narratives and amendments — preservation is honest, not sanitized; even rejected amendments (R3 #6) carry explicit reasons. Round-1 decision preserved with strikethrough per AGENTS-MD-bb7fe2c5aa. Honest-acks verifiably state no pre-Round-2 wave fired (git log confirms). PR-webhook commitment names the specific tool (`mcp__github__pull_request_read`). Bias-guard timing-model fix documented (R1 #2 — serial-after-Wave-8.1 is the only consistent shape).
>
> Spot-check of pre-folded auto-007 items: all 8 appear (commit-SHA pinning, time-anchored honest-acks, Appendix A scaffold, 3-tier verdict commitment, TL;DR structure-not-conclusions, PR-webhook, framework-ADR pairing, skip-discipline auditability).
>
> Defects: (1) 5 deferred Phase-7 retro AGENTS-MD-* rules cited only by retrospective-directory path — honest, but the brief should flag that these citations dangle if the retro directory is reorganized. (2) R3 #2 fold reference uses an auto-generated long-form anchor that exceeds GitHub's anchor-slug length and will not resolve — broken internal link in an audit-trail document. (3) `escape-hatch` enumeration item 1 lacks a cite to `candidate-registry.md`'s specific §-anchor for the unified-attempt-dual-mandate claim. (4) Quantitative claim "tier-table medians (6400 Light / 7200 Heavy)" not cited to a source document.

**Amendments (verbatim):**

1. Add anchor-resilience note for the 5 deferred retro rules — one sentence stating these citations will dangle if `retrospective/2026-05-27-191/` is reorganized, and naming a mitigation.
2. Fix broken §-header link at the R3 #2 fold target — replace the auto-generated long-form anchor with a stable named anchor on the rubric section or a direct line-anchor.
3. Cite source for Phase-7 tier-table medians (6400 Light / 7200 Heavy) — link to a Phase-7 word-count audit file or to the auto-007 retro that established them.
4. Cite `candidate-registry.md` §-anchor for the unified-attempt-dual-mandate claim used in escape-hatch item 1 — current cite is bare filename without §-anchor.

### Reviewer 5 — 10-year on-call engineer

**Verdict:** `accept-with-named-amendments`. "Two debug-time landmines and three small recovery gaps that a 3am-tired agent will hit."

**Key findings (verbatim digest):**

> Strengths: Decision shape is sound; pre-authored cite-obligation table is unusually thorough; fixed audit-file paths help recovery (next-agent can `ls audit-*.md` to see which auditors completed); A.2′ resolves R1's timing-model contradiction; falsifier discipline tightening (3-item rubric + escape-hatch enumeration + "pass cleanly" + honest "in advance" reframe) genuinely moves discipline from ceremony toward load-bearing; Wave 8.1.b's 3 auditors are read-only relative to each other → no race.
>
> Biggest defect: lead-agent falsifier cross-check between Wave 8.1.b and Wave 8.2 produces ZERO artifact — if lead-agent context exhausts mid-cross-check, the next agent sees `audit-falsification-designer.md` carrying "rewrite §3" verdicts and has no way to know whether re-authoring happened, is partway done, or never started. For a step the brief calls "load-bearing" via the conditional Wave-8.2 fallback, this is a recovery hole.
>
> Second: 5 Phase-7 retrospective AGENTS-MD-* hashes are cited by retrospective-directory paths, not canonical AGENTS.md anchors. A future agent grepping `AGENTS.md` for these hashes finds nothing. The brief acknowledges this but doesn't give grep guidance.
>
> Third: post-self-check failure paths are unspecified (over-budget file, §3-vs-YAML inconsistency). Subagents flag but don't recover.
>
> Smaller gaps: (a) subagent-fallback condition for Wave 8.2 evaluator-brief uses `grep` on audit file but verdict-token format is not mandated; (b) audit file behavior under Wave-8.1 re-dispatch unspecified (archive? overwrite?); (c) 3-item rubric "pass ≥2 of 3" no escalation if a brief passes 2 but fails item (iii) "threshold" (most load-bearing).

**Amendments (verbatim):**

1. **Lead-agent cross-check MUST produce an artifact** — commit `lean-evals/cross-check-falsifier.md` (≤200 words) naming which briefs were re-authored, or "0 rewrite verdicts, no action". No artifact = step did not complete.
2. **Add §3-vs-YAML consistency check** to falsification-designer rubric (item iv, mandatory not 2-of-3): §3's claim and YAML field name the same metric + threshold + artifact.
3. **Specify "rewrite §3" verdict token format** in `audit-falsification-designer.md` (e.g., literal `verdict: rewrite-§3` line per candidate-section) so the subagent-fallback grep is deterministic.
4. **Add canonical-grep instruction** for the 5 retrospective AGENTS-MD-* hashes in the §References section: "grep `retrospective/2026-05-27-191/` not `AGENTS.md`".
5. **Specify over-budget recovery action**: subagent over-budget → return-digest flag → lead agent re-dispatches that subagent only (not the whole wave) with truncation guidance; do not silently accept.
6. **Specify Wave-8.1 re-dispatch protocol for audit files**: if Wave 8.1 is re-dispatched, archive existing audit files to `lean-evals/archived/<timestamp>/` before Wave 8.1.b re-fires.

### Reviewer 6 — cross-mandate attacker

**Verdict:** `accept-with-named-amendments`. **Found load-bearing structural defect in DEC-1.a falsifying pattern vs. file model.**

**Key findings (verbatim digest):**

> The central defect is in §Falsifier discipline R2 illustrative vs. §Sub-wave coordination protocol. The DEC-1.a falsifying pattern says ≥2 unified-attempt candidates must "pass cleanly on BOTH the greenfield-mandate lean-eval AND the brownfield-mandate lean-eval." But the file uniqueness invariant names exactly one file per candidate: `u-a.md`, `u-b.md`, `u-c.md`, `d7-u-1.md`. So either (a) each unified-attempt's single brief must explicitly partition its §1 scenarios into a greenfield bloc and a brownfield bloc, with the R2 #3 quantitative gate (≥80%) applied per-bloc — or (b) the DEC-1.a pattern wording must be rewritten to "pass cleanly across a scenario set that includes ≥N greenfield-shaped and ≥M brownfield-shaped scenarios." The brief commits to neither. The hypothesis-falsifier auditor reading `u-a.md` will find a single scenario list and have to either invent the partition or punt — the falsifier loses mechanical auditability at exactly the load-bearing cell.
>
> R2 #3's quantitative-gate definition silently presumes mandate-blind scenarios. "≥80% of the brief's §1 named scenarios pass" — for a unified-attempt brief with 6 GF + 4 BF scenarios, 8/10 passing satisfies ≥80% even if every BF scenario fails. That's the exact pattern DEC-1.a is supposed to detect ("methodology serves one mandate, not both") and the gate is blind to it.
>
> The asymmetric design-input mapping is acceptable but undocumented (H-2/H-8 → GF-S/GF-M/U-A; H-3 Pulse → BF-L only; no greenfield analog of Pulse). The asymmetry is methodologically defensible but should be flagged.

**Amendments (verbatim):**

1. Partition the §1 scenario set in every unified-attempt brief into a `greenfield-mandate-scenarios` subsection and a `brownfield-mandate-scenarios` subsection, ≥3 each. Mandatory YAML field `mandate-scenario-split: {greenfield: N, brownfield: M}`.
2. Redefine R2 #3 "pass cleanly" for unified-attempts as: ≥80% greenfield-mandate scenarios pass AND ≥80% brownfield-mandate scenarios pass AND falsifying-outcome NOT triggered on any scenario. Mandate-blind ≥80% is insufficient for DEC-1.a.
3. Rewrite illustrative to use partitioned form: "≥2 unified-attempts pass cleanly per-mandate (≥80% greenfield-bloc AND ≥80% brownfield-bloc), neither bloc invoking escape-hatches." Removes "two lean-evals" ambiguity.
4. Add to historian-design-input table a note: "H-2/H-8 is greenfield-shaped (self-improving prompts); H-3 Pulse is brownfield-shaped (production-trace-to-amendment). Asymmetric assignment reflects pattern-mandate alignment, not candidate-quality."
5. Add to escape-hatch enumeration item 1 a structural rider: "For a unified-attempt, declaring an entire mandate-bloc out-of-scope is structurally a failure to deliver on the unified-attempt claim; ≥1 mandate-bloc with <3 scenarios scored fails R2 #3 (a) by construction."

## Exemplar pre-fanout self-check results

*Subsection appended at exemplar-commit time (PR 3 in the run).* Lead-agent self-check items (a)-(h) run on the exemplar brief; pass/fail recorded. Failure on item (d) or (h) blocks fanout.

## Decision (Round 2)

**Option A′. Per-candidate parallel fanout (Wave 8.1, 9 sibling subagents) + 3 cross-candidate bias-guard auditors fired in parallel SERIAL-AFTER-Wave-8.1 (Wave 8.1.b — domain-practitioner + falsification-designer + hypothesis-falsifier; each reads all 10 finalized lean-eval briefs and writes its own audit roll-up file) + lead-agent falsifier cross-check between Wave 8.1.b and Wave 8.2 + Wave 8.2 cross-candidate evaluator-brief (lead-agent-default authorship, subagent-fallback if ≥3 unified-attempt briefs triggered "rewrite §3" verdicts), lead-agent exemplar first with self-check gate (items a-g; item h dropped), tiered word-budget (Light 5000-6500 / Heavy 5500-7200), pre-authored Phase-7 cite-obligation propagation table, falsifier-discipline tightened (3-item concreteness rubric + escape-hatch enumeration + "pass cleanly" definition + reframed "in advance" claim), Phase-8-followup deferral threshold restricted to unified-attempt candidates.**

Concretely (Round-2 amended Decision):

- **Lead-agent inline: exemplar lean-eval brief** for the least-contested candidate. Candidate set: **{GF-M, BF-S}** (Light tier). Lead agent picks at exemplar-authoring time based on which produces the cleanest falsifying-outcome demonstration under the 3-item concreteness rubric (see [§Falsifier discipline (load-bearing)](#falsifier-discipline-load-bearing) below). Default lean: **GF-M** (greenfield-light, single-dominant lineage, cleanest scenario-set framing). ~5500-word target (mid-Light-tier). Committed as PR 3.
- **Wave 8.1 (9 per-candidate subagents in parallel)** fires after the exemplar lands. Each subagent reads (i) its candidate's [`specs/<id>.md`](../specs/), (ii) the candidate's [`backfill-notes/<id>.md`](../backfill-notes/), (iii) the candidate's open carries from [`specs/<id>.md` §6](../specs/), (iv) this brief's rubric + cite-obligation table row for its candidate, (v) the exemplar brief. Writes its lean-eval brief at `architectures/v3/lean-evals/<candidate-id>.md`. Returns ≤500-word digest.
- **Wave 8.1.b (3 cross-candidate bias-guards in parallel, serial-after-Wave-8.1-closes)** — A.2′ shape: 3 auditors run in parallel with each other AFTER Wave 8.1 closes. **Per Round-1 R1 #2 timing-model fix**: subagents do not commit drafts mid-run, so concurrent-with-Wave-8.1 firing was structurally broken; serial-after-Wave-8.1 firing is the only consistent shape. The 3 auditors are independent of each other (each reads the same 10 finalized briefs and writes its own audit file).
  - **Domain-practitioner subagent (1× cross-candidate).** Reads all 10 finalized `lean-evals/<id>.md` briefs. Verdict per-candidate (paragraph-level in roll-up): would the test scenarios actually validate the discipline? Practical concerns the brief misses. Output: `lean-evals/audit-domain-practitioner.md` — one cross-candidate roll-up with per-candidate §-sections. Word budget: ≤3000.
  - **Falsification-designer subagent (1× cross-candidate).** Reads all 10 finalized `lean-evals/<id>.md` briefs. For each brief: verifies the `falsifying-outcome:` YAML field is populated AND §3 falsifying-outcome statement passes the **3-item concreteness rubric** (per [§Falsifier discipline](#falsifier-discipline-load-bearing) below: names a metric / names a directory or artifact state / names a threshold; pass = ≥2 of 3). If any brief fails the rubric, the falsification-designer's verdict for that brief is "rewrite §3"; lead agent re-authors the failing brief before Wave 8.2. Output: `lean-evals/audit-falsification-designer.md` — one cross-candidate roll-up with per-candidate §-sections + per-brief pass/fail on each rubric item. Word budget: ≤3000.
  - **Hypothesis-falsifier subagent (1× cross-candidate).** Reads all 10 finalized `lean-evals/<id>.md` briefs + the [DEC-1.a working hypothesis text](../decisions-captured.md#d1--unification-verdict-no-methodology-serves-both-mandates-working-hypothesis-falsifiable-by-phase-8) + the [Phase-7 §6.4 NEUTRAL observation](../backfill-notes.md#64-dec-1-a-working-hypothesis-observation-neutral-pre-phase-8). Output: `lean-evals/audit-hypothesis-falsifier.md` — names the cross-candidate result pattern that would falsify DEC-1.a. **Honest framing (per R2 #4):** the pattern is named "before simulator runs, after brief authoring" — NOT in absolute advance. The audit file's first section MUST state explicitly **how the auditor guarded against fitting the observed pattern of the 10 briefs** (e.g., by drafting the pattern independent of the 10 briefs first, then verifying applicability; or by naming a falsifier the briefs would NOT predict). Word budget: ≤2500. **Uses the canonical "escape-hatch" enumeration AND "pass cleanly" definition** committed in [§Falsifier discipline](#falsifier-discipline-load-bearing) below.
- **Lead-agent falsifier cross-check (between Wave 8.1.b and Wave 8.2)** — per R1 #3 + R5 #1 amendments. Lead agent reads `lean-evals/audit-falsification-designer.md` and verifies the rubric-failed briefs (if any) have been re-authored before Wave 8.2 fires. **R5 #1 amendment (load-bearing):** the cross-check MUST produce an artifact `lean-evals/cross-check-falsifier.md` (≤200 words) naming which briefs were re-authored, or stating "0 rewrite verdicts; no action taken". The artifact is the durable record — without it, a context-exhausted lead-agent leaves the next agent unable to know whether re-authoring happened, is partway done, or never started. Quick 5-minute lead-agent task; not a subagent dispatch.
- **Wave 8.2 (cross-candidate evaluator-brief, lead-agent-default authorship, subagent-fallback)** — fires SERIAL after Wave 8.1.b closes AND lead-agent cross-check completes. Reads all 10 finalized per-candidate briefs + the 3 audit roll-ups. Writes `lean-evals/00-cross-candidate.md`. **Quotes the hypothesis-falsifier's DEC-1.a falsifying result pattern verbatim** in its §X (load-bearing per [§Falsifier discipline](#falsifier-discipline-load-bearing)). **Authorship default**: lead-agent inline. **Authorship fallback (per R1 #6)**: if Wave 8.1.b reports ≥3 unified-attempt candidates with "rewrite §3" verdicts (lead-agent context will be saturated by re-author cycles), Wave 8.2 dispatches a single cross-candidate evaluator-brief subagent instead.

**PR consolidation per [`AGENTS-MD-d71e845b29`](../../../AGENTS.md#sub-wave-pr-consolidation-when-files-are-disjoint):**

- **Wave 8.1 (PR 4 omnibus)** — 9 sibling per-candidate briefs. All disjoint files.
- **Wave 8.1.b (PR 5 omnibus)** — 3 cross-candidate audit roll-up files. All disjoint files. **Split from Wave 8.2 (R1 + R3 converged amendment)** for clean rewind boundary: if the evaluator-brief misquotes the hypothesis-falsifier pattern, rewind PR 6 doesn't lose the audit work.
- **Wave 8.2 (PR 6)** — single cross-candidate evaluator-brief file.

### Round-2 reasoning

Four drivers selected Option A′ over Round 1's Option A:

1. **A.1 per-candidate-paired bias-guards was structurally broken AND over-budget.** Round-1 R1 #2 surfaced the timing-model defect: subagents don't commit drafts mid-run, so concurrent-with-Wave-8.1 firing of per-candidate auditors had nothing to read. R1 #1 + R3 #1 converged on the cost: 30 concurrent subagents exceeds the harness's 20-25 practical limit. A.2′ resolves both: 3 cross-candidate auditors fire serial-after-Wave-8.1 in parallel with each other, reading the finalized briefs. The "per-candidate isolation" advantage of A.1 is recoverable because each auditor's roll-up file carries per-candidate §-sections — no information loss.

2. **Falsifier-discipline tightening (R2 amendments) moves the discipline from "ceremony" toward "load-bearing".** R2's #1 (3-item concreteness rubric) gives the falsification-designer auditor a mechanical pass/fail criterion across 10 candidates rather than 10 different interpretations of "concrete". R2's #2 (escape-hatch enumeration: "out-of-mandate scope claim, scenario-skip, criterion-substitution") + R2's #3 ("pass cleanly" = ≥80% scenarios pass success-criteria AND falsifying-outcome NOT triggered) commit the DEC-1.a falsifying pattern's load-bearing terms in this brief rather than delegating to the hypothesis-falsifier. R2's #4 (reframed "in advance" claim, honestly: "before simulator runs, after brief authoring") closes the post-hoc-reinterpretation escape route that the original framing left open.

3. **Wave 8.1.b ↔ Wave 8.2 PR split (R1 #4 + R3 #3 converged) gives a clean rewind boundary.** The hypothesis-falsifier pattern is load-bearing for Wave 8.2's cross-candidate evaluator-brief. If the evaluator-brief misquotes or misapplies the pattern, the user needs to be able to rewind Wave 8.2 (cross-candidate evaluator-brief) WITHOUT losing the 3 audit roll-ups (which themselves cost ~3 subagents of effort). Two separate PRs make this rewindable.

4. **Phase-8-followup deferral threshold restricted to unified-attempt candidates (R1 #5).** The Phase-8 falsification surface is for DEC-1.a; only the 4 unified-attempt candidates (U-A / U-B / U-C / D7-U-1) carry the DEC-1.a load. A failed GF-S / GF-C / GF-M / BF-S / BF-M / BF-L lean-eval is a quality defect on that candidate but does not block DEC-1.a falsification. Restricting the deferral threshold to unified-attempts prevents over-aggressive triggering.

The drop of self-check item (h) (R3 #2; cite-obligation honoring) is non-load-bearing — the falsification-designer auditor's per-brief verdict already checks cite-obligation honoring + the post-fanout aggregation re-checks it. Three-layer enforcement was over-engineering.

The Heavy ceiling tightening 7500 → 7200 (R3 #5) aligns the ceiling to Phase-7 actual median; the looser 7500 would tolerate continued drift.

### Round-2 final amendments folded

The Round-2 decision (Option A′) stands. Following amendments are folded:

| Amendment | Source | Status |
|---|---|---|
| Flip A.1 → A.2′ default (3 cross-candidate bias-guards serial-after-Wave-8.1) | R1 #1 + R3 #1 (converged) | **load-bearing** — folded inline at [§Decision (Round 2)](#decision-round-2) above |
| Bias-guard timing-model fix (subagents don't commit drafts mid-run) | R1 #2 | **load-bearing** — subsumed by A.1→A.2′ flip |
| 3-item concreteness rubric for falsification-designer auditor | R2 #1 | **load-bearing** — folded into [§Falsifier discipline](#falsifier-discipline-load-bearing) below |
| Escape-hatch enumeration for DEC-1.a falsifier pattern | R2 #2 | **load-bearing** — folded into [§Falsifier discipline](#falsifier-discipline-load-bearing) |
| "Pass cleanly" definition committed in this brief | R2 #3 | **load-bearing** — folded into [§Falsifier discipline](#falsifier-discipline-load-bearing) |
| Reframed "in advance" claim (honest: before-simulator-runs-after-brief-authoring) + hypothesis-falsifier audit-file requirement | R2 #4 | **load-bearing** — folded inline at [§Decision (Round 2)](#decision-round-2) above + [§Falsifier discipline](#falsifier-discipline-load-bearing) |
| Split Wave 8.1.b and Wave 8.2 into separate PRs | R1 #4 + R3 #3 (converged) | **load-bearing** — folded into [§Sub-wave coordination protocol](#sub-wave-coordination-protocol) below |
| Phase-8-followup deferral threshold restricted to unified-attempt candidates | R1 #5 | **load-bearing** — folded into [§Phase-8-followup deferral binding mechanism (load-bearing)](#phase-8-followup-deferral-binding-mechanism-load-bearing) below |
| Lead-agent falsifier cross-check between Wave 8.1.b and Wave 8.2 | R1 #3 | non-load-bearing — folded inline at [§Decision (Round 2)](#decision-round-2) above |
| Cross-candidate evaluator-brief authorship: subagent-fallback if ≥3 unified-attempt rewrite verdicts | R1 #6 | non-load-bearing — folded inline at [§Decision (Round 2)](#decision-round-2) above |
| Drop self-check item (h) | R3 #2 | non-load-bearing — folded into the Self-check rubric subsection of §A (per-candidate lean-eval brief rubric); see the "(h) DROPPED in Round 2" annotation in the self-check list below (R4 #2 amendment fixed broken auto-generated anchor) |
| Tighten Heavy ceiling 7500 → 7200 | R3 #5 | non-load-bearing — folded into tier-table below |

Amendments rejected with reason:

- **R3 #6 (defer Phase-7 cite-obligation table to exemplar-commit time).** REJECTED. The pre-authored mapping table belongs in the brief per [`AGENTS-MD-8740bd7b0a`](../../../AGENTS.md#adr-number-to-filename-mapping-in-subagent-dispatch-briefs) (analogous to ADR-number-to-filename mapping pattern; subagents need it in their dispatch input). Moving it to exemplar-commit time would force subagents to read the exemplar's commit for their dispatch input rather than the brief, breaking the dispatch-prompt-stability pattern.

### Round-2-reviewer amendments folded (post-Round-2 patches)

Round 2 dispatched 3 additional adversarial reviewers (regulator + on-call engineer + cross-mandate attacker). All 3 returned `accept-with-named-amendments`. The amendments did NOT converge on a different option (Option A′ shape preserved), so they are folded inline as post-Round-2 patches rather than triggering Round 3.

| Amendment | Source | Status |
|---|---|---|
| Partitioned-mandate scenario set for unified-attempts (mandatory YAML `mandate-scenario-split` field + §1 partition + R2 #3 "pass cleanly" redefined per-mandate) | R6 #1 + #2 (load-bearing structural defect found) | **load-bearing** — folded inline at [§Falsifier discipline](#falsifier-discipline-load-bearing) + [§Per-candidate lean-eval brief rubric YAML frontmatter](#a-per-candidate-parallel-fanout-wave-81--2-per-candidate-concurrent-bias-guards-domain-practitioner--falsification-designer-paired-per-candidate--1-serial-bias-guard-after-wave-81-hypothesis-falsifier--wave-82-cross-candidate-evaluator-brief-lead-agent-exemplar-first-with-self-check-gate-tiered-word-budget-per-phase-7-evidence--lead-agent-recommendation) above |
| DEC-1.a illustrative pattern rewritten to use partitioned form | R6 #3 | **load-bearing** — folded inline at [§Falsifier discipline](#falsifier-discipline-load-bearing) |
| Escape-hatch structural rider for unified-attempts | R6 #5 | **load-bearing** — folded inline at [§Falsifier discipline](#falsifier-discipline-load-bearing) (canonical escape-hatch enumeration item 1) |
| Cross-check produces artifact `lean-evals/cross-check-falsifier.md` (≤200w) | R5 #1 (load-bearing recovery hole) | **load-bearing** — folded inline at [§Decision (Round 2)](#decision-round-2) (lead-agent falsifier cross-check) |
| 4th rubric item (§3-vs-YAML consistency check, mandatory) for falsification-designer | R5 #2 | **load-bearing** — folded inline at [§Falsifier discipline](#falsifier-discipline-load-bearing) (item (iv); pass mandatory) |
| Verdict-token format in `audit-falsification-designer.md` | R5 #3 | non-load-bearing — folded inline at [§Falsifier discipline](#falsifier-discipline-load-bearing) (new "Verdict-token format" subsection) |
| Canonical-grep instruction for 5 deferred retro AGENTS-MD-* hashes + anchor-resilience note | R5 #4 + R4 #1 | non-load-bearing — folded inline at [§Honest acknowledgements (Round 1)](#honest-acknowledgements-round-1) item 1 |
| Wave-8.1 audit-file re-dispatch archive protocol | R5 #6 | non-load-bearing — folded inline at [§Sub-wave coordination protocol](#sub-wave-coordination-protocol) |
| Over-budget subagent recovery action | R5 #5 | non-load-bearing — folded inline at [§Sub-wave coordination protocol](#sub-wave-coordination-protocol) |
| Pattern-mandate alignment note for historian-design-input asymmetry | R6 #4 | non-load-bearing — folded inline at [§Historian load-bearing design inputs](#historian-load-bearing-design-inputs-5-gaps--n-candidates) |
| Cite source for tier-table medians (aggregation §6.1) | R4 #3 | non-load-bearing — folded inline at tier-table |
| Fix broken §-header link in Round-2 amendments table | R4 #2 | non-load-bearing — folded inline at [§Round-2 final amendments folded](#round-2-final-amendments-folded) |
| Cite candidate-registry.md §-anchor for unified-attempt dual-mandate claim | R4 #4 | non-load-bearing — folded inline at canonical escape-hatch item 1 |

### Adversarial review discipline commitment (Round 2)

Per [`AGENTS-MD-8a7029647f`](../../../AGENTS.md#adversarial-review-verdict-tiers): Round-1 + Round-2 reviewer dispatch briefs (all 6 fired) explicitly offered all 3 verdict tiers — see [§Appendix A — Round-1 reviewer return digests (preserved for traceability)](#appendix-a--round-1-reviewer-return-digests-preserved-for-traceability) below (Round-1) and [§Appendix B — Round-2 reviewer return digests (preserved for traceability)](#appendix-b--round-2-reviewer-return-digests-preserved-for-traceability) below (Round-2). All 6 reviewers returned `accept-with-named-amendments`.
