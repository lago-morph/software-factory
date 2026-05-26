# auto-006 — Phase 6 dispatch shape

**Author.** Lead agent, unattended Phase-6 dispatch session 2026-05-26.
**Status.** **Round 1 (initial brief).** Awaiting ≥3 real adversarial subagents per [AGENTS.md § Adversarial review MUST be real subagents](../../../AGENTS.md#adversarial-review-must-be-real-subagents). Round-2 dispatch follows.
**Rewind point.** This brief's commit on [`claude/phase-6-architecture-specs-NHmM3`](../../../). Reverting it returns Phase-6 dispatch to "undecided"; no per-candidate spec-authoring subagent has fired.

---

## TL;DR (≤200 words)

Phase 6 produces **10 architecture specs** (one per surviving candidate) + **1 mandate-fit matrix** + **Phase-6-close session handoff**, composing each candidate's substrate ADRs + discipline ADRs + per-variant ADRs into a coherent architecture description. This brief decides the dispatch shape. Open questions for the Round-1 reviewers: (1) **wave shape** — 10-in-one parallel fanout vs mandate-clustered sub-waves vs hybrid; (2) **per-spec rubric** — section structure, word budget, mandatory cross-reference floor; (3) **exemplar choice** — which candidate's spec the lead agent authors inline first per the [exemplar-before-fanout discipline](../../../AGENTS.md#exemplar-before-parallel-uniform-schema-fanout); (4) **matrix authorship** — lead-agent inline after specs land vs its own subagent dispatch; (5) **cross-spec consistency check** — fresh-context verification subagent(s) per the [phase-A-fresh-context-verification SKILL-SPEC](../../../retrospective/2026-05-25-170/SKILL-SPEC-ad9a173772-phase-A-fresh-context-verification.md). Lead-agent recommendation: per-candidate parallel fanout in **3 mandate-clustered sub-waves** (3 GF + 3 BF + 4 U), GF-M exemplar (the [Phase-4 exemplar](../substrate-requirements/gf-m.md)), matrix authored as **its own subagent** after specs land, **2 verification subagents** (cross-spec consistency + ADR-coverage completeness).

## The question

Phase 6 of the v3 synthesis produces per-candidate architecture specs per the [v1.2 plan § Phase 6](../../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md#phase-6--architecture-spec-authorship-one-per-surviving-candidate-revised-in-v12). Three sub-products are owed:

- **10 architecture specs**, one per candidate (3 greenfield + 3 brownfield + 4 unified-attempt). Each composes the candidate's substrate ADRs (common + orphan + per-variant) + discipline ADRs + methodology/cycle shape into a coherent description. Word budget: ≤3500 words per spec (per lead-agent draft; reviewers should challenge).
- **1 mandate-fit matrix** at [`architectures/v3/mandate-fit-matrix.md`](../mandate-fit-matrix.md) — 10 rows × work-unit-classes (5-class default per [DEC-2](../decisions-captured.md#d2--mandate-fit-is-per-architecture--work-unit-class-not-per-architecture)). Cells = `greenfield-fit | brownfield-fit | both | n/a`.
- **Phase-6-close session handoff** at `architectures/v3/SESSION-HANDOFF-<UTC-DATE>-phase-6-close.md` unblocking Phase 7 (back-fill audit per candidate against archived v1/v2).

Total ADR consumer-load per spec: ~18-25 ADRs (common substrate 0010-0017 + discipline 0018-0027 + designed-system 0028-0036 + candidate's own orphan + candidate's per-variant ADRs, per the [per-candidate ADR set table](../SESSION-HANDOFF-2026-05-25-phase-5-close.md#candidate-set-state-at-phase-5-close) in the Phase-5-close handoff).

The dispatch shape determines (i) how the 10 spec-authoring subagents are sequenced (one parallel wave? mandate-clustered sub-waves? serial?), (ii) the per-spec brief shape + rubric + section structure + word budget, (iii) which candidate's spec serves as the exemplar (lead-agent inline first), (iv) whether the mandate-fit matrix is lead-agent inline or its own subagent dispatch, and (v) which post-spec verification fires.

## Alternatives considered

### A. Per-candidate parallel fanout, 3 mandate-clustered sub-waves (GF / BF / U), GF-M exemplar — **lead-agent recommendation**

- **Wave 6.1 (greenfield, 3 subagents)**. GF-S, GF-M, GF-C. **Lead-agent authors the GF-M spec inline first as the exemplar** before the other two fire. Choice: GF-M was the [Phase-4 Wave-4.1 substrate-requirements exemplar](../substrate-requirements/gf-m.md); reusing keeps subagent calibration consistent across phases. GF-M carries no RG flags, no contested-primitive references beyond P-21 calibration, no shared-skeleton obligations — least-contested per [AGENTS-MD-eec503a3c2](../../../AGENTS.md#exemplar-before-parallel-uniform-schema-fanout).
- **Wave 6.2 (brownfield, 3 subagents)**. BF-S, BF-M, BF-L. Fires concurrent with Wave 6.1 — no cross-dependencies because each candidate's ADR set is disjoint at authoring time. **Note:** BF-L carries the largest ADR set (P-26 + P-13 + per-region variants) — flag in the subagent brief to budget toward the high end of the word range.
- **Wave 6.3 (unified-attempt, 4 subagents)**. U-A, U-B, U-C, D7-U-1. Fires concurrent with Waves 6.1 and 6.2. **Note:** D7-U-1 has 5 variant ADRs (P-28 + P-29 + P-30 per-variants); spec author flags the cross-variant invariants explicitly.
- **Aggregation step**. After all 10 specs land, lead-agent ≤10-minute checkpoint: spot-check that exemplar shape held, no rubric drift, every spec's `## References` cites the right ADR set.
- **Mandate-fit matrix subagent (Wave 6.4)**. Dispatched after the 10 specs land, with all 10 spec files + the [DEC-2 schema](../decisions-captured.md#d2--mandate-fit-is-per-architecture--work-unit-class-not-per-architecture) + the [work-unit-class enumeration](../decisions-captured.md#d2--mandate-fit-is-per-architecture--work-unit-class-not-per-architecture) as required input. The matrix subagent extracts each spec's `## Mandate fit` section into the matrix's row, with rationale-by-cell.
- **Verification subagents (Wave 6.5, 2 subagents in parallel)** per [SKILL-SPEC-ad9a173772 phase-A-fresh-context-verification](../../../retrospective/2026-05-25-170/SKILL-SPEC-ad9a173772-phase-A-fresh-context-verification.md):
  - **Verifier-1: cross-spec consistency.** Reads all 10 specs cold. Confirms every ADR is referenced by at least one spec; no spec references a non-existent ADR; mandate-fit claims are consistent with claimed substrate; no spec contradicts its own claimed substrate ADRs.
  - **Verifier-2: ADR-coverage completeness.** Reads all 55 Phase-5 ADRs cold + the 10 specs. Confirms every ADR has at least one citing spec, names any orphaned ADRs (potential dead Phase-5 work), and reports the per-candidate ADR-count distribution vs the Phase-5-close handoff's expected table.

**Per-spec brief shape.** Each spec-authoring subagent receives:

1. The candidate's [`candidate-registry`](../candidate-registry.md) entry + [`substrate-requirements/<id>.md`](../substrate-requirements/) + [`tracks/<id>.md`](../tracks/) (and `sub-tracks/<id>.md` if applicable).
2. The full ADR-ID-to-file mapping table for the candidate's ADR set (per [AGENTS-MD-8740bd7b0a](../../../AGENTS.md#adr-number-to-filename-mapping-in-subagent-dispatch-briefs)). Common ADRs 0010-0036 + per-candidate ADRs per the [per-candidate ADR set table](../SESSION-HANDOFF-2026-05-25-phase-5-close.md#candidate-set-state-at-phase-5-close).
3. The GF-M exemplar spec.
4. The rubric (see below).

**Per-spec rubric.** Section structure, word budget, citation floor:

- **H1**: `# Architecture spec — <candidate-id> (<full name>)`.
- **YAML frontmatter** per ADR-0004 + per-(work-unit-class) `mandate-fit` block per DEC-2 (`initial-spec / refactor / mvp / post-mvp-evolution / regression-fix` each ∈ `greenfield-fit | brownfield-fit | both | n/a`).
- **§1 Overview** (~200 words). Mandate, axis, entry-mode, one-paragraph methodology summary, the candidate's load-bearing claim.
- **§2 Substrate composition** (~600-800 words). Lists every substrate primitive the candidate carries with its ADR ref; explicitly names common-vs-orphan-vs-per-variant for each; per [AGENTS-MD-a9fb7b42f8](../../../AGENTS.md#framework-adr-scope-boundary-discipline), every framework-ADR reference (P-19/P-28/P-29/P-30) MUST also cite the candidate's per-variant ADR.
- **§3 Methodology shape** (~500-700 words). Cycle structure, regime structure if any (e.g., GF-M Regime-A/B; U-A day-0 → day-N trajectory), work-unit definition, the candidate's distinctive methodology decisions.
- **§4 Discipline binding** (~400-600 words). Names which of the 21 disciplines (ADRs 0018-0027) the candidate carries and how each binds to substrate + methodology. Identifies which disciplines the candidate is silent on.
- **§5 Mandate fit** (~300-500 words). Restates the YAML mandate-fit block in prose; per cell, names the supporting substrate + methodology evidence + the falsifying scenario (per the [DEC-1.a falsifier discipline](../decisions-captured.md#d1--unification-verdict-no-methodology-serves-both-mandates-working-hypothesis-falsifiable-by-phase-8)).
- **§6 Open carries** (~200-300 words). Open questions surfaced into Phase 7 (back-fill audit) / Phase 8 (lean-eval) / future Phase-5 ADRs (if any).
- **§7 References** (mandatory; relative paths only per [AGENTS.md § Internal document references](../../../AGENTS.md#internal-document-references)). Floor: ≥(candidate's full ADR set + candidate-registry entry + substrate-requirements summary + track sketch). Approximate count: ~25-35 references per spec.

**Word budget per spec: 2000-3500 words** (lead-agent draft; reviewers should challenge — too tight, too loose, or right-sized?).

**Self-check rubric extension** per [AGENTS-MD-e74e4811a2](../../../AGENTS.md#self-check-rubric-requires-tool-verification-for-measurable-items): subagent runs (a) `wc -w` on its spec to verify word budget compliance, (b) `ls` on every cited ADR file to verify the file exists, (c) `grep` for each candidate's expected per-variant ADRs to verify framework-ADR + per-variant pairs both cited, (d) `grep` for §1-§7 headers to verify section structure, (e) `grep` the YAML frontmatter for the `mandate-fit:` block.

**Pros.**
- Maximum parallelism: 3 + 3 + 4 = 10 subagents fire concurrent ⇒ all specs land in roughly one fanout's wall-clock time.
- Mandate clustering keeps each sub-wave's subagent briefs tonally consistent (same mandate's substrate + methodology framing).
- Per-spec parallelism preserves per-candidate accountability + crisp blast-radius if any spec needs re-dispatch.
- Lead-agent GF-M exemplar enforces shape consistency across the 9 sibling specs (per [AGENTS-MD-eec503a3c2](../../../AGENTS.md#exemplar-before-parallel-uniform-schema-fanout)).
- Matrix-as-its-own-subagent decouples cross-spec extraction from per-spec authoring — matrix subagent reads all 10 specs cold with no anchoring from authoring context.
- Verification subagents catch cross-spec drift (the dominant failure mode for parallel uniform-schema fanout per [SKILL-SPEC-ad9a173772](../../../retrospective/2026-05-25-170/SKILL-SPEC-ad9a173772-phase-A-fresh-context-verification.md)).

**Cons.**
- 10 concurrent subagents + 1 matrix + 2 verifiers = ~13 subagents this run. Within the ≤15-wave-size limit but at the upper end.
- Aggregation budget: 10 spec digests × ~3500 words ≈ ~35K words of subagent return content to ingest at lead-agent level. Mitigated by spec-authoring subagents committing their files directly + returning short digests (file path + word count + cross-ref count + open-questions list).
- Mandate clustering does NOT prevent cross-mandate inconsistency on shared ADRs (e.g., if GF-S and BF-L both cite ADR 0028 P-19 framework, their interpretations could drift). Mitigated by Verifier-1.
- BF-L and D7-U-1 carry the largest ADR sets and may push past the 3500-word ceiling. Brief should permit explicit per-candidate budget exceptions named in the dispatch.

### B. Single 10-subagent parallel wave (no mandate clustering)

Dispatch all 10 spec authors in one parallel wave. No greenfield/brownfield/unified clustering at dispatch time.

- **Pros.** Simpler dispatch — one brief shape, one exemplar, one parallel wave.
- **Cons.** Lead-agent must hold 10 candidate framings in head simultaneously when reading subagent returns; per-mandate cross-spec consistency (e.g., GF-S/GF-M/GF-C internal greenfield coherence) is harder to spot. Marginal benefit over Option A is small — both Option A and B have the same wall-clock; Option A adds ~5 minutes of clustering overhead at brief-shape time for clearer aggregation. **Not chosen.**

### C. Serial single-author-pass (lead-agent authors all 10 specs inline)

Lead agent authors every spec sequentially without subagent dispatch.

- **Pros.** No coordination overhead; no anchoring risk from misread briefs; cross-spec consistency by single-author.
- **Cons.** Saturates context with spec detail (10 specs × ~3500 words = ~35K words just for the bodies, plus ~25K words of ADR reading per spec = ~250K words total). Forecloses fresh-context per-spec reasoning. Wall-clock cost on the order of a full overnight run for a single agent. Loses the parallelism the [v1.2 plan § Phase 6](../../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md#phase-6--architecture-spec-authorship-one-per-surviving-candidate-revised-in-v12) explicitly endorses ("one per surviving candidate" implies independent authoring). **Not chosen.**

### D. Per-mandate sequential waves (Wave 6.1 GF, then 6.2 BF after 6.1 closes, then 6.3 U)

Dispatch waves sequentially with lead-agent aggregation between each.

- **Pros.** Each successor wave can learn from prior wave's exemplar(s) — Wave 6.2 BF subagents could read a landed Wave 6.1 GF spec as a sibling-mandate calibration point.
- **Cons.** 3× wall-clock cost vs Option A for marginal benefit (the rubric is uniform across mandates; the exemplar is mandate-clustered already in Option A by virtue of GF-M being a GF candidate that authoring-time GF subagents see directly). No structural blocker to firing all three mandates concurrent. **Not chosen.**

### E. Mandate-fit matrix lead-agent inline (no matrix subagent)

Lead agent authors the matrix inline after the 10 specs land, by reading each spec's §5 Mandate fit + extracting the YAML frontmatter mandate-fit block.

- **Pros.** Saves one subagent dispatch; lead-agent has the full Phase-5 + Phase-6 context.
- **Cons.** Lead-agent at end-of-Phase-6 has ~150K words of read-context (briefs + ADRs + spec returns); a fresh-context matrix subagent reads 10 spec files (~35K words) cold and produces a less-anchored matrix. Per [SKILL-SPEC-ad9a173772](../../../retrospective/2026-05-25-170/SKILL-SPEC-ad9a173772-phase-A-fresh-context-verification.md), fresh-context for cross-document extraction is the higher-quality default. **Not chosen unless context-budget pressure forces it.** Round-1 reviewers should challenge whether the marginal quality gain justifies the extra subagent.

## Decision (Round 1)

**Option A. Per-candidate parallel fanout, 3 mandate-clustered sub-waves (GF / BF / U), GF-M exemplar, matrix-as-its-own-subagent, 2 verification subagents.** Per the structure laid out in [Alternative A](#a-per-candidate-parallel-fanout-3-mandate-clustered-sub-waves-gf--bf--u-gf-m-exemplar--lead-agent-recommendation) above.

Concretely:

- **Lead-agent inline: GF-M exemplar spec** committed as the first Phase-6 artifact. ~3000-word target. Authored using the rubric below.
- **Waves 6.1 + 6.2 + 6.3 fire concurrent** after the GF-M exemplar lands. Total: 9 spec-authoring subagents (10 minus GF-M).
- **After all specs land**: lead-agent ≤10-minute aggregation checkpoint. Then **Wave 6.4 (matrix subagent)** + **Wave 6.5 (2 verification subagents in parallel)** all fire concurrent.
- **Verification finding triage**. If verifiers surface zero or non-blocking findings: Phase 6 closes with the handoff PR. If verifiers surface a blocking finding (a spec contradicts its own substrate; an ADR is uncited and the verifier judges it dead Phase-5 work): lead agent re-dispatches the affected spec(s) on a stacked PR. Budget for re-dispatch: ≤2 PRs.

**Total subagents this run: 9 (spec authoring, excluding GF-M exemplar) + 1 (matrix) + 2 (verifiers) = 12 ADR-authoring-equivalent dispatches**, plus ~6 adversarial reviewers across this brief's two rounds = ~18 subagents total for Phase 6.

### Revised per-ADR rubric (none — first-Round)

(Round-1 rubric reasonable as drafted. Reviewers should challenge any item.)

### Round-1 reasoning

Three drivers select Option A:

1. **The Phase-4 Wave-4.1 precedent worked cleanly** with the same shape: per-candidate parallel fanout + lead-agent exemplar + uniform rubric. GF-M was the exemplar then; reusing exploits already-calibrated subagent shape.
2. **Mandate clustering is positive-sum.** It costs ~5 minutes of brief-shape time and yields cleaner aggregation (per-mandate cross-spec coherence is checkable at sub-wave level). Total wall-clock unchanged from Option B because all three sub-waves fire concurrent.
3. **Fresh-context verification subagents** at Phase-6 close catch the dominant failure mode for parallel uniform-schema fanouts: cross-spec drift on shared ADRs and silent ADR-coverage gaps. The [SKILL-SPEC-ad9a173772](../../../retrospective/2026-05-25-170/SKILL-SPEC-ad9a173772-phase-A-fresh-context-verification.md) explicitly captures this lesson from the Phase-5 verification subagent finding.

Matrix-as-its-own-subagent (over Option E) preserves the fresh-context discipline. Lead-agent inline matrix authoring at Phase-6 close would be anchored on the spec-authoring context the lead agent already saw.

## Downstream impact

- **Phase 7** (back-fill audit per candidate against archived v1/v2) consumes the 10 specs as binding inputs. The dispatch shape here determines that the specs are stable + cross-consistent + mandate-fit-matrixed before Phase 7 fires.
- **Phase 8** (lean-eval briefs per candidate) inherits the per-candidate spec as the single source of truth for what the lean-eval pressure-tests. Open carries surfaced in spec §6 become Phase-8 inputs.
- **Mandate-fit matrix** is the first user-facing artifact that pressure-tests the [DEC-1.a working hypothesis](../decisions-captured.md#d1--unification-verdict-no-methodology-serves-both-mandates-working-hypothesis-falsifiable-by-phase-8): a unified-attempt candidate with `both` on most cells is evidence against the hypothesis.

## Honest acknowledgements

Per [AGENTS-MD-ffe35aa500](../../../AGENTS.md#honest-acknowledgements-for-pre-round-2-wave-firing) (pre-Round-2 wave firing): no Phase-6 spec-authoring subagent has fired pre-Round-2; this dispatch brief precedes the spec dispatch. Mechanically verifiable: `git log --oneline -- architectures/v3/specs/` returns empty as of this commit.

**Process-bug acknowledgement.** This run opened with a finding that the [Phase-5 work (55 ADRs + handoff + AGENT-ENTRY)](../SESSION-HANDOFF-2026-05-25-phase-5-close.md) was on a stacked branch (`claude/auto-2026-05-25-A5-verification-fixes`) and never landed in `main`. PR #181 brought it forward into main before this brief was authored. The brief is authored against the corrected main. The lead-agent finding + user-confirmed remediation path are recorded in this brief's git history; the brief's premises hold under the corrected state.

## Open questions for the Round-1 adversarial reviewers to challenge

1. **Wave shape.** Is mandate clustering (3 GF + 3 BF + 4 U) better than a single 10-wave (Option B)? Or is it false-precision dressing on a uniform shape that adds coordination cost without benefit?
2. **Exemplar choice.** Is reusing GF-M (the Phase-4 exemplar) the right call? Or does GF-M's small ADR set (5 substrate primitives + ~10 disciplines, no contested-primitive variants) miscalibrate subagents working on heavier candidates (BF-L's P-26 + RG-context; D7-U-1's 5 variant ADRs; U-A's 4 per-variants)? Counter-candidates: BF-S (small brownfield, no contested variants) or U-C (mid-difficulty unified with one P-19 per-variant).
3. **Word budget 2000-3500.** Is this right-sized? BF-L's ADR set is ~20 ADRs; D7-U-1's is ~22 ADRs. Are subagents being asked to do too much in 3500 words, or is the ceiling about right?
4. **Matrix authorship.** Is matrix-as-its-own-subagent justified, or is lead-agent inline (Option E) fine? The marginal subagent cost is ~1 PR; the marginal quality from fresh-context is ~?
5. **Verification subagent count.** 2 verifiers (cross-spec consistency + ADR-coverage completeness) — is this overkill (one fused verifier would do) or undershooting (a third verifier on mandate-fit-matrix consistency would help)?
6. **PR-cap budget.** Spec sub-waves + matrix + verifiers + handoff + summary + retro = ~7-9 PRs. Plus this brief = ~8-10 PRs against the ≤15 PR-cap. Comfortable margin or under-budgeted?
7. **Per-candidate brief production cost.** 10 unique briefs (with per-candidate ADR-ID-to-file mapping table) is non-trivial lead-agent authoring. Should the brief use a template + per-candidate substitution to reduce that load?

(Round-1 reviewers will challenge any/all of these + anything else they find.)

## Round-1 if-user-overrides rewind point

This brief's commit on `claude/phase-6-architecture-specs-NHmM3`. Revert to undo the Round-1 framing; no spec-authoring subagent has fired (this brief precedes the wave dispatch).
