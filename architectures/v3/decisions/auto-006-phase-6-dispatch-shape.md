# auto-006 — Phase 6 dispatch shape

**Author.** Lead agent, unattended Phase-6 dispatch session 2026-05-26.
**Status.** **Round 2 (revised after first real adversarial wave).** Round 1 returned 3 × `accept-with-named-amendments`. Round-1 decision shape (per-candidate parallel fanout, 3 mandate-clustered sub-waves, GF-M exemplar, 2 verifiers, ≤3500-word ceiling) is **superseded**; revised decision in [§Decision (Round 2)](#decision-round-2) swaps exemplar to U-C, tiers the word budget, consolidates spec PRs to 3 per-sub-wave PRs, collapses to 1 verifier + inline ADR-coverage script, adds a mandatory §0 ADR-citation index table, mandates subagent return digests ≤500 words, and resolves the mandate-fit YAML schema ambiguity.
**Rewind point.** This brief's commit on [`claude/phase-6-architecture-specs-NHmM3`](../../../). Reverting it returns Phase-6 dispatch to "undecided"; no per-candidate spec-authoring subagent has fired.

---

## TL;DR (≤200 words)

This brief decides Phase-6's dispatch shape. Phase 6 produces three sub-products: **10 per-candidate architecture specs**, **1 mandate-fit matrix**, **1 Phase-6-close session handoff**. The dispatch decision shape is: per-candidate parallel fanout, with **mandate-clustered sub-wave PRs as the PR-consolidation unit** (greenfield / brownfield / unified), **one lead-agent-authored exemplar slot** filled by a mid-difficulty unified candidate, **a tiered per-spec word budget indexed by ADR count**, **a mandatory §0 ADR-citation index table per spec**, **a single fresh-context verification subagent** for cross-spec consistency + lead-agent inline script for ADR-coverage, and **mandatory ≤500-word subagent return digests**. The brief also decides the **Phase-6-followup deferral binding mechanism** (three named artifacts per the binding-artifact-triple rule) and a **per-sub-wave-PR contingency clause** isolating the highest-risk spec (D7-U-1) into its own PR. The Round-2 decision section ([§Decision (Round 2)](#decision-round-2)) names every parameter; reviewers' load-bearing amendments are folded in [§Round-2 final amendments folded](#round-2-final-amendments-folded).

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

## Decision (Round 1 — superseded by Round 2 below)

~~**Option A. Per-candidate parallel fanout, 3 mandate-clustered sub-waves (GF / BF / U), GF-M exemplar, matrix-as-its-own-subagent, 2 verification subagents.** Per the structure laid out in [Alternative A](#a-per-candidate-parallel-fanout-3-mandate-clustered-sub-waves-gf--bf--u-gf-m-exemplar--lead-agent-recommendation) above.~~ Round 1 superseded — all three reviewers returned `accept-with-named-amendments` with convergent load-bearing amendments (exemplar swap, word budget tiering, PR consolidation, verifier collapse, §0 index table, digest cap, schema disambiguation). See [§Decision (Round 2)](#decision-round-2). Round-1 text preserved below for traceability per [AGENTS-MD-bb7fe2c5aa](../../../AGENTS.md#round-1-strikethrough-preservation-in-decision-briefs).

### Round 1 reasoning (preserved)

~~Concretely:~~

- ~~**Lead-agent inline: GF-M exemplar spec** committed as the first Phase-6 artifact. ~3000-word target. Authored using the rubric below.~~
- ~~**Waves 6.1 + 6.2 + 6.3 fire concurrent** after the GF-M exemplar lands. Total: 9 spec-authoring subagents (10 minus GF-M).~~
- ~~**After all specs land**: lead-agent ≤10-minute aggregation checkpoint. Then **Wave 6.4 (matrix subagent)** + **Wave 6.5 (2 verification subagents in parallel)** all fire concurrent.~~
- ~~**Verification finding triage**. If verifiers surface zero or non-blocking findings: Phase 6 closes with the handoff PR. If verifiers surface a blocking finding (a spec contradicts its own substrate; an ADR is uncited and the verifier judges it dead Phase-5 work): lead agent re-dispatches the affected spec(s) on a stacked PR. Budget for re-dispatch: ≤2 PRs.~~

~~**Total subagents this run: 9 (spec authoring, excluding GF-M exemplar) + 1 (matrix) + 2 (verifiers) = 12 ADR-authoring-equivalent dispatches**, plus ~6 adversarial reviewers across this brief's two rounds = ~18 subagents total for Phase 6.~~

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

## Round 1 reviewer findings

Three real subagents dispatched per [AGENTS.md § Adversarial review MUST be real subagents](../../../AGENTS.md#adversarial-review-must-be-real-subagents).

### Reviewer 1 — Phase-6-pipeline architect (`accept-with-named-amendments`)

- **Objection 1: GF-M exemplar miscalibrates the heavier candidates.** GF-M has 5 primitives, no P-19/P-28/P-29/P-30 contested-primitive references, no §3 fixed-header sub-sections, X_UNM_B is N/A, zero load-bearing RG primitives. Compare D7-U-1: 5 primitives but with 3 contested-primitive sub-sections, full X_UNM_B articulation, load-bearing RG primitive. The auto-005 Round-1 reviewer raised this exact objection ("least-contested ≠ best calibration; want smallest cross-cutting obligations"); this brief repeats it.
- **Objection 2: The §2 Substrate composition rubric is shaped by a candidate that has nothing to demonstrate there.** GF-M cites none of P-19/P-28/P-29/P-30. The framework-ADR + per-variant pairing — the load-bearing discipline of the rubric — is not demonstrated by the exemplar. Seven of nine downstream subagents need to see this pattern done correctly.
- **Objection 3: Mandate clustering at brief-shape time is theater on this dispatch shape.** Concurrent firing means no learning between waves, no per-mandate aggregation gate, no rubric divergence. The clustering reduces to labeling.
- **Objection 4: Verifier-1 cannot catch the dominant cross-spec failure mode.** Verifier-1 as scoped checks structural citation existence, not interpretation drift on shared framework ADRs.
- **Amendments (5):** swap exemplar to U-C; rewrite §A footnote into explicit per-candidate budget exceptions (BF-L + D7-U-1 → 4500 ceiling); narrow Verifier-1 to "structural citation integrity", broaden Verifier-2 to "cross-spec semantic consistency"; either drop mandate clustering or add a real reason for it; pre-author common ADR-ID-to-file mapping table in the brief.

### Reviewer 2 — Spec-quality auditor (`accept-with-named-amendments`)

- **Objection 1: Framework-ADR + per-variant cross-reference floor not mechanically testable.** `grep` cannot verify pairing — a spec could cite ADR 0050 in §6 References and ADR 0028 in §3 and they'd never be co-located. Need `## ADR-citation index` table making the pairing a single-row grep target.
- **Objection 2: Mandate-fit YAML schema carries hidden ambiguity.** DEC-2 schema is `greenfield | brownfield | both | n/a`; brief uses `greenfield-fit | brownfield-fit | both | n/a` — pick one. Neither distinguishes "candidate is silent on this work-unit-class" from "deliberately not-applicable."
- **Objection 3: Word budget 2000-3500 is under-budgeted.** §2 (600-800) + §3 (500-700) + §4 (400-600) + §5 (300-500) + §1 (200) + §6 (200-300) + §7 references (400 min) = **2425-3500 baseline**, leaving zero headroom for BF-L (20 ADRs) or D7-U-1 (22 ADRs).
- **Objection 4: Missing critical section: §0 ADR-citation index table.** A spec composing 18-25 ADRs needs an upfront index so verifier doesn't have to grep prose.
- **Objection 5: Citation floor "~25-35 references" is hand-wavy.** Make floor exact per the Phase-5-close handoff table.
- **Objection 6: Self-check rubric misses verbatim text-pull discipline (AGENTS-MD-bf4431be57).**
- **Amendments (6):** add §0 ADR-citation index table; word budget 2500-4500 + 500/extra-per-variant; replace hand-wavy reference count with exact per-candidate ADR floor from handoff; resolve `-fit` suffix discrepancy; add `silent` value to mandate-fit YAML or require `n/a` rationale; add self-check items (f) verbatim text-pull and (g) framework+variant co-location.

### Reviewer 3 — Cost/scope hawk (`accept-with-named-amendments`)

- **Objection 1: PR-cap math under-counted.** Realistic count: 1 (brief) + 1 (exemplar) + 9 (specs at one-per-PR) + 1 (matrix) + 2 (verifiers) + 1 (handoff) + 1 (summary) + 1 (retro) + 2 (re-dispatch) = **18-20 PRs vs ≤15 cap**.
- **Objection 2: Two verifiers is overkill.** Verifier-2 ("every ADR has at least one citing spec") is a `grep -L` against `docs/adr/` — a script, not a subagent. Collapse to 1 verifier + inline script. Saves 1 dispatch + 1 PR.
- **Objection 3: Re-dispatch budget ≤2 PRs is unrealistic at 9 concurrent specs.** Base rate for verifier surfacing a blocking finding on at least one spec is non-trivial.
- **Objection 4: Lead-agent ingest of ~35K words of returns is operationally optimistic.** Brief doesn't mandate digest length.
- **Objection 5: Per-candidate ADR-ID-to-file mapping table production cost unaccounted for.** ~225 mapping table rows the lead agent must hand-author into briefs.
- **Amendments (5):** consolidate spec PRs to 3 per-sub-wave PRs (one per mandate); collapse to 1 verifier + lead-agent inline script for ADR-coverage; mandate subagent return digest ≤500 words; raise re-dispatch budget to 3 PRs OR explicitly accept Phase-6-followup deferral; pre-author one ADR-mapping table per mandate cluster + parameterize per-candidate.

### Convergence

All three reviewers returned `accept-with-named-amendments` — no `reject-with-counter-proposal`. The dispatch shape (per-candidate parallel fanout + exemplar + verification) is correct; the load-bearing amendments are at the rubric + verifier + PR-consolidation layers, not the dispatch shape layer.

**Load-bearing convergent amendments:**
1. **Exemplar swap** (Reviewer 1): GF-M → U-C. Mid-difficulty unified candidate that demonstrates framework-ADR + per-variant pairing.
2. **Word budget tiering** (Reviewers 1 & 2): tier by ADR count, not uniform.
3. **PR consolidation** (Reviewer 3): 3 sub-wave PRs (not 9 per-spec PRs). Saves ~6 PRs.
4. **Verifier collapse** (Reviewer 3): 2 → 1 verifier + inline script. Saves ~1 PR + ~1 dispatch.
5. **§0 ADR-citation index table** (Reviewer 2): mandatory in every spec.
6. **Subagent return digest ≤500 words** (Reviewer 3): mandate.
7. **Mandate-fit YAML schema** (Reviewer 2): pin to DEC-2 canonical tokens; add `silent` value.

**Non-load-bearing amendments folded:**
- Common ADR-ID-to-file mapping table pre-authored in this brief (Reviewers 1 & 3).
- Verbatim text-pull self-check addition (Reviewer 2).
- Per-candidate exact reference floor (Reviewer 2).

**Amendments rejected with reason:**
- Drop mandate clustering entirely (Reviewer 1 alternative): rejected; mandate clustering is preserved because consolidating PRs by mandate (Reviewer 3 amendment) requires the cluster boundary at dispatch time. Reviewer 1's objection ("clustering is theater") is correct under Round 1's "9 per-spec PRs" framing; under Round 2's "3 sub-wave PRs" framing, mandate clustering becomes load-bearing.
- Raise re-dispatch budget to 3 (Reviewer 3): partially accepted at 3 PRs but flagged as a budget *ceiling* — if more than 1 spec needs re-author, lead agent must consider Phase-6-followup deferral per [AGENTS-MD-cb08b5a7f3](../../../AGENTS.md#self-imposed-deferrals-re-validate-before-honoring).

## Decision (Round 2)

**Option A′. Per-candidate parallel fanout, 3 mandate-clustered sub-waves consolidated to 3 sub-wave PRs, U-C exemplar, tiered word budget, §0 ADR-citation index table, 1 verifier + inline ADR-coverage script, mandatory ≤500-word digests.**

Concretely:

- **Lead-agent inline: U-C exemplar spec** committed as the first Phase-6 artifact. ~3500-word target. Authored using the rubric below. Demonstrates the framework-ADR + per-variant pairing (ADR 0028 + ADR 0058 for P-19; ADR 0029 + ADR 0059 for P-28) for 7-of-9 downstream candidates to inherit.
- **Wave 6.1 (greenfield, 3 specs in 1 sub-wave PR)**. GF-S + GF-M + GF-C. Three parallel subagents commit to the same sub-wave branch; one PR carries all three spec files.
- **Wave 6.2 (brownfield, 3 specs in 1 sub-wave PR)**. BF-S + BF-M + BF-L. Same pattern. BF-L's word budget tier: 3500-5500.
- **Wave 6.3a (unified-attempt mid-tier, 2 specs in 1 sub-wave PR)**. U-A + U-B. Same pattern (U-C is the lead-agent-authored exemplar, not in this wave).
- **Wave 6.3b (unified-attempt heavy-tier, 1 spec in its own PR)**. D7-U-1 alone. Per [Round-2 pre-mortemer Amendment 1](#round-2-reviewer-findings) — D7-U-1 is the run's single highest-risk spec (22 ADRs, 5 per-variant ADRs across P-28/P-29/P-30, tier `Heavy` 3500-5500 words). Isolating it into its own PR contains the blast radius if it fails verification. PR-cap impact: +1 PR (11-12 → 12-13 against ≤15 cap; still 2-3 PR margin).
- **All four sub-waves (6.1 + 6.2 + 6.3a + 6.3b) fire concurrent** after U-C exemplar lands. Total: 9 spec-authoring subagents across 4 sub-wave PRs.
- **After all specs land**: lead-agent ≤10-minute aggregation checkpoint + runs `grep -L` ADR-coverage check inline (deterministic script per Reviewer 3 Amendment 2). Then **Wave 6.4 (matrix subagent)** + **Wave 6.5 (1 verification subagent)** fire concurrent.
- **Verification subagent scope** (revised per Reviewer 1 Objection 4 + Reviewer 2 Objection 1 + Reviewer 3 Amendment 2): **structural citation integrity** (every ADR cited exists; framework-ADR references always paired with per-variant per [AGENTS-MD-a9fb7b42f8](../../../AGENTS.md#framework-adr-scope-boundary-discipline) via §0 index table) **+ cross-spec semantic consistency** (read every paragraph in every spec that cites ADRs 0010-0036, flag interpretation drift on shared framework ADRs). ADR-coverage completeness check moves to lead-agent inline script (not a subagent).
- **Verification finding triage**. If verifier surfaces zero or non-blocking findings: Phase 6 closes. If verifier surfaces ≤1 spec needing re-author: lead agent re-dispatches on a stacked PR (≤1 re-dispatch PR budgeted). If verifier surfaces ≥2 specs needing re-author: lead agent invokes Phase-6-followup deferral per [AGENTS-MD-cb08b5a7f3](../../../AGENTS.md#self-imposed-deferrals-re-validate-before-honoring) (deferral re-validates at fire-time) and surfaces this as a binding-artifact-triple item per [AGENTS-MD-2adf78e54a](../../../AGENTS.md#deferred-work-binding-artifact-triple).

**Total subagents this run:** 9 (spec authoring, excluding U-C exemplar) + 1 (matrix) + 1 (verifier) = **11 ADR-authoring-equivalent dispatches**, plus 6 adversarial reviewers across this brief's two rounds = **17 subagents total for Phase 6**.

**PR-cap math (Round-2 revised, Wave-6.3 split per pre-mortemer Amendment 1):** 1 (this brief R2) + 1 (U-C exemplar) + 4 (sub-wave PRs: GF / BF / U-mid / U-heavy) + 1 (matrix) + 1 (verifier findings) + 1 (handoff) + 1 (summary) + 1 (retro) + ≤1 (re-dispatch) = **11-12 PRs against ≤15 cap, 3-4 PRs margin**. Plus 1 already-consumed PR (#181 bring-forward, pre-Phase-6) = **12-13 PRs run total**.

### Revised per-spec rubric (Round-2 amendments folded in)

Each spec-authoring subagent receives:

1. The candidate's [`candidate-registry`](../candidate-registry.md) entry + [`substrate-requirements/<id>.md`](../substrate-requirements/) + [`tracks/<id>.md`](../tracks/) (and `sub-tracks/<id>.md` if applicable).
2. The full ADR-ID-to-file mapping table — common 0010-0036 published once in this brief (see [§Common ADR-ID-to-file mapping](#common-adr-id-to-file-mapping-0010-0036) below); candidate-specific (variant + orphan) mapping appended per-subagent-brief.
3. The U-C exemplar spec (when authored).
4. The rubric (below).

**Per-spec rubric (Round-2 revised).** Section structure, word budget, citation floor:

- **H1**: `# Architecture spec — <candidate-id> (<full name>)`.
- **YAML frontmatter** per ADR-0004 + per-(work-unit-class) `mandate-fit` block per [DEC-2 canonical schema](../decisions-captured.md#d2--mandate-fit-is-per-architecture--work-unit-class-not-per-architecture):
  ```yaml
  based-on-commit: <commit-sha>
  based-on-date: <YYYY-MM-DD>
  mandate-fit:
    initial-spec: greenfield | brownfield | both | n/a | silent
    refactor: greenfield | brownfield | both | n/a | silent
    mvp: greenfield | brownfield | both | n/a | silent
    post-mvp-evolution: greenfield | brownfield | both | n/a | silent
    regression-fix: greenfield | brownfield | both | n/a | silent
  ```
  Token semantics (Reviewer 2 Amendment): `greenfield` = candidate is greenfield-fit on this class; `brownfield` = brownfield-fit; `both` = candidate explicitly claims both; `n/a` = candidate deliberately rejects this class as in-scope (with one-line reason inline in §5); `silent` = candidate has no position (different from `n/a` — silence is not a claim).
- **§0 ADR-citation index table** (mandatory, new per Reviewer 2 Objection 4):
  ```
  | ADR ID | Title | Layer | Variant of (if per-variant) | Citing § |
  |---|---|---|---|---|
  | 0010 | P-01 Sandbox runtime | common | — | §2 |
  | 0028 | P-19 framework | common | — | §2, §3 |
  | 0058 | P-19 variant U-C | per-variant | 0028 | §2, §3 |
  ...
  ```
  Single-row grep target for `(framework-ADR-id) → (variant-ADR-id)` pairing per [AGENTS-MD-a9fb7b42f8](../../../AGENTS.md#framework-adr-scope-boundary-discipline). Verification subagent reads §0 to enforce the pairing rule.
- **§1 Overview** (~200 words). Mandate, axis, entry-mode, one-paragraph methodology summary, candidate's load-bearing claim.
- **§2 Substrate composition** (~600-1000 words depending on tier). Lists every substrate primitive the candidate carries with its ADR ref; explicitly names common-vs-orphan-vs-per-variant for each; framework-ADR references MUST be accompanied by per-variant ADR references per the §0 index pairing.
- **§3 Methodology shape** (~500-900 words depending on tier). Cycle structure, regime structure if any, work-unit definition, the candidate's distinctive methodology decisions.
- **§4 Discipline binding** (~400-600 words). Names which of the 21 disciplines (ADRs 0018-0027) the candidate carries and how each binds to substrate + methodology. Names disciplines the candidate is silent on.
- **§5 Mandate fit** (~300-600 words). Restates the YAML mandate-fit block in prose; per cell, names supporting substrate + methodology evidence + falsifying scenario per the [DEC-1.a falsifier discipline](../decisions-captured.md#d1--unification-verdict-no-methodology-serves-both-mandates-working-hypothesis-falsifiable-by-phase-8). For any `n/a` cell, one-line reason inline.
- **§6 Open carries** (~200-300 words). Open questions surfaced into Phase 7 / Phase 8 / future ADRs.
- **§7 References** (mandatory; relative paths only per [AGENTS.md § Internal document references](../../../AGENTS.md#internal-document-references)). Floor: **exact per-candidate ADR set** (per the Phase-5-close handoff per-candidate table) **+ ≥4 supporting docs** (candidate-registry entry + substrate-requirements + track + overlap.md entry).

**Word budget tiering (Round-2 amendment per Reviewers 1 & 2):**

| Tier | Word budget | Candidates | Rationale |
|---|---|---|---|
| Light | 2500-3500 | GF-S, GF-M, GF-C, BF-S | Small ADR set (≤15 ADRs); minimal contested-primitive references |
| Mid | 3000-4500 | BF-M, U-A, U-B, U-C | Medium ADR set (16-19 ADRs); 1-2 per-variant ADRs |
| Heavy | 3500-5500 | BF-L, D7-U-1 | Large ADR set (20-22 ADRs); 3-5 per-variant ADRs OR significant orphan content |

**Self-check rubric (Round-2 revised)** per [AGENTS-MD-e74e4811a2](../../../AGENTS.md#self-check-rubric-requires-tool-verification-for-measurable-items). Subagent runs:

- (a) `wc -w` on its spec to verify word budget compliance against its tier.
- (b) `ls` on every cited ADR file path to verify the file exists.
- (c) `grep` for §0-§7 headers to verify section structure.
- (d) `grep` the YAML frontmatter for the `mandate-fit:` block and each work-unit-class key.
- (e) `grep -E '^\| 0[0-9]+'` on §0 table to verify ≥(candidate's per-handoff-table ADR-count) rows present.
- (f) `grep -F` for verbatim quoted text-pulls when the spec invokes overlap.md or decisions-captured rows per [AGENTS-MD-bf4431be57](../../../AGENTS.md#verbatim-text-pull-when-citing-binding-rule-tables) (new per Reviewer 2 Amendment).
- (g) `grep` per framework-ADR ID (0028, 0029, 0030, 0036) in §0 row to verify the per-variant column is non-empty when the candidate claims the framework (new per Reviewer 2 Amendment).

**Subagent return digest mandate (Round-2 amendment per Reviewer 3):** Subagent return ≤500 words, structured as: file path + final `wc -w` count + final `wc -l` count + 3-bullet cross-ref summary + open-questions list + self-check results (each item pass/fail). The spec body itself is in the committed file, not the return.

## Common ADR-ID-to-file mapping (0010-0036)

Pre-authored per [AGENTS-MD-8740bd7b0a](../../../AGENTS.md#adr-number-to-filename-mapping-in-subagent-dispatch-briefs) — every per-candidate dispatch brief inherits this table by reference.

| ADR | File | Layer | Notes |
|---|---|---|---|
| 0010 | [`docs/adr/0010-p-01-sandbox-runtime.md`](../../../docs/adr/0010-p-01-sandbox-runtime.md) | common substrate | Commodity |
| 0011 | [`docs/adr/0011-p-02-cost-ceilings.md`](../../../docs/adr/0011-p-02-cost-ceilings.md) | common substrate | Commodity |
| 0012 | [`docs/adr/0012-p-05-trajectory-capture.md`](../../../docs/adr/0012-p-05-trajectory-capture.md) | common substrate | Commodity |
| 0013 | [`docs/adr/0013-p-06-watchdog-tiers.md`](../../../docs/adr/0013-p-06-watchdog-tiers.md) | common substrate | Commodity |
| 0014 | [`docs/adr/0014-p-07-telemetry-ingestor.md`](../../../docs/adr/0014-p-07-telemetry-ingestor.md) | common substrate | Commodity |
| 0015 | [`docs/adr/0015-p-08-scenario-storage-with-runner-contract.md`](../../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md) | common substrate | Designed-system |
| 0016 | [`docs/adr/0016-p-14-judge-router.md`](../../../docs/adr/0016-p-14-judge-router.md) | common substrate | Commodity |
| 0017 | [`docs/adr/0017-p-22-polyglot-codebase-index.md`](../../../docs/adr/0017-p-22-polyglot-codebase-index.md) | common substrate | Commodity |
| 0018 | [`docs/adr/0018-discipline-bias-guard.md`](../../../docs/adr/0018-discipline-bias-guard.md) | discipline | — |
| 0019 | [`docs/adr/0019-discipline-cognitive-escrow.md`](../../../docs/adr/0019-discipline-cognitive-escrow.md) | discipline | — |
| 0020 | [`docs/adr/0020-discipline-cost-ceiling.md`](../../../docs/adr/0020-discipline-cost-ceiling.md) | discipline | — |
| 0021 | [`docs/adr/0021-discipline-holdout.md`](../../../docs/adr/0021-discipline-holdout.md) | discipline | — |
| 0022 | [`docs/adr/0022-discipline-honesty.md`](../../../docs/adr/0022-discipline-honesty.md) | discipline | — |
| 0023 | [`docs/adr/0023-discipline-knowledge-promotion.md`](../../../docs/adr/0023-discipline-knowledge-promotion.md) | discipline | — |
| 0024 | [`docs/adr/0024-discipline-regime-classification.md`](../../../docs/adr/0024-discipline-regime-classification.md) | discipline | — |
| 0025 | [`docs/adr/0025-discipline-scoping.md`](../../../docs/adr/0025-discipline-scoping.md) | discipline | — |
| 0026 | [`docs/adr/0026-discipline-three-loop.md`](../../../docs/adr/0026-discipline-three-loop.md) | discipline | — |
| 0027 | [`docs/adr/0027-discipline-trifecta-closure.md`](../../../docs/adr/0027-discipline-trifecta-closure.md) | discipline | — |
| 0028 | [`docs/adr/0028-p-19-eligibility-regime-classifier.md`](../../../docs/adr/0028-p-19-eligibility-regime-classifier.md) | common substrate | **Framework** — has 4 per-variant ADRs (0039, 0049, 0050, 0058) |
| 0029 | [`docs/adr/0029-p-28-typed-object-store.md`](../../../docs/adr/0029-p-28-typed-object-store.md) | common substrate | **Framework** — has per-variant ADRs (0051, 0055, 0059, 0062) |
| 0030 | [`docs/adr/0030-p-29-policy-mediator.md`](../../../docs/adr/0030-p-29-policy-mediator.md) | common substrate | **Framework** — has per-variant ADRs (0052, 0056, 0063) |
| 0031 | [`docs/adr/0031-p-23-dependency-impact-graph.md`](../../../docs/adr/0031-p-23-dependency-impact-graph.md) | common substrate | Designed-system |
| 0032 | [`docs/adr/0032-p-12-deterministic-linter-framework.md`](../../../docs/adr/0032-p-12-deterministic-linter-framework.md) | common substrate | Designed-system |
| 0033 | [`docs/adr/0033-p-25-camel-perimeter.md`](../../../docs/adr/0033-p-25-camel-perimeter.md) | common substrate | 2-candidate fold (BF-S, BF-M) |
| 0034 | [`docs/adr/0034-p-27-archaeological-brief-tooling.md`](../../../docs/adr/0034-p-27-archaeological-brief-tooling.md) | common substrate | 2-candidate fold (BF-M, BF-L) |
| 0035 | [`docs/adr/0035-p-24-attribution-store.md`](../../../docs/adr/0035-p-24-attribution-store.md) | common substrate | 2-candidate fold (BF-S, BF-L) |
| 0036 | [`docs/adr/0036-p-30-event-registrar-substrate.md`](../../../docs/adr/0036-p-30-event-registrar-substrate.md) | common substrate | **Framework** — has per-variant ADRs (0053, 0064) |

Candidate-specific (orphan + per-variant) mapping appended per-subagent-brief from the [Phase-5-close handoff per-candidate table](../SESSION-HANDOFF-2026-05-25-phase-5-close.md#candidate-set-state-at-phase-5-close).

## Round-2 reasoning

Three drivers select Option A′ over Round 1's Option A:

1. **Exemplar U-C demonstrates the framework-ADR + per-variant pattern.** U-C has 1 P-19 variant (ADR 0058) + 1 P-28 variant (ADR 0059) + 1 orphan (ADR 0057 P-32). The exemplar §0 ADR-citation index table will show the framework-ADR + per-variant pairing pattern for 7-of-9 downstream subagents (those whose candidates carry per-variant ADRs) to inherit. GF-M (Round-1 choice) had nothing to demonstrate there.

2. **PR consolidation to 3 sub-wave PRs preserves PR-cap margin.** 11-12 PRs run-total against ≤15 cap gives 3-4 PRs margin for re-dispatch + unanticipated work. Round-1's 18-20 estimate blew the cap.

3. **§0 ADR-citation index table makes framework+variant pairing mechanically testable.** Verification subagent reads §0 rows; the pairing is a single-row grep target rather than a cross-section semantic check. Round-1 rubric required pairing but couldn't enforce it.

The tiered word budget honors that BF-L and D7-U-1 carry larger ADR sets without bloating the light/mid tier specs. The 1-verifier + inline-script collapse saves 1 PR + 1 dispatch.

## Round-2 if-user-overrides rewind point

This brief's commit on `claude/phase-6-architecture-specs-NHmM3`. Revert to undo the Round-2 framing; no spec-authoring subagent has fired (this brief precedes the wave dispatch).

## Honest acknowledgements (Round 2)

Per [AGENTS-MD-ffe35aa500](../../../AGENTS.md#honest-acknowledgements-for-pre-round-2-wave-firing): no Wave-6.1/6.2/6.3/6.4/6.5 ADR-authoring subagent has fired pre-Round-2; this dispatch brief precedes the wave dispatch. Mechanically verifiable: `git log --oneline -- architectures/v3/specs/` returns empty as of this Round-2 commit.

**Process-bug carry-forward.** This run's first action was PR #181 (Phase-5 bring-forward), executed before this brief was authored. The brief's premises hold under the corrected main state.

## Open questions for the Round-2 adversarial reviewers to challenge

1. **U-C exemplar choice.** Is U-C right? Or does U-C's specific shape (interval-kind P-19 variant + anchor-envelope P-28 variant) miscalibrate subagents on candidates with different variant shapes (BF-L per-region P-19; D7-U-1 timer-driven P-30)?
2. **Tiered word budget enforceability.** Each tier has a 1000-word band. Is that wide enough that the budget becomes non-binding (specs always run to the ceiling)? Should the tier be tighter or expressed as a function (e.g., `2000 + 150 × ADR-count`)?
3. **PR consolidation downside.** 3 sub-wave PRs (3-4 specs each) means a single bad spec blocks merging the whole sub-wave PR. Should the 4 unified-attempt specs (Wave 6.3) be 2 PRs (U-A+U-B together; D7-U-1 alone) given D7-U-1's high complexity?
4. **Verifier collapse risk.** 1 verifier doing both structural integrity + semantic consistency may be too much for one fresh-context subagent. Split or keep collapsed?
5. **§0 index table production cost.** Per-spec ADR-citation index is ~18-25 rows the subagent authors. Is this material extra work, or does it land naturally as part of §2/§7 authoring?
6. **Phase-6-followup deferral trigger ("≥2 specs needing re-author").** Is this threshold right? Or should it be ≥3 (more aggressive in-session work) or ≥1 (more conservative)?
7. **Mandate clustering still surviving in Round 2.** Reviewer 1 said clustering was theater; the Round-2 fix (3 sub-wave PRs) makes clustering load-bearing for PR-consolidation purposes. Is the clustering then justified, or is there a cleaner shape (e.g., 1 omnibus PR with 9 specs)?

## Round 2 reviewer findings

Three real subagents dispatched with fresh angles per [AGENTS-MD-d72e1a4f3c](../../../AGENTS.md#adversarial-review-must-be-real-subagents). Each was offered the 3-tier verdict menu (`accept-as-is` / `accept-with-named-amendments` / `reject-with-counter-proposal`) per [AGENTS-MD-8a7029647f](../../../AGENTS.md#adversarial-review-verdict-tiers).

### Reviewer 4 — pre-mortemer (`accept-with-named-amendments`)

**Most-likely failure path: Wave 6.3's 4-spec consolidated sub-wave PR cannot merge because D7-U-1 fails verification and blocks U-A + U-B + sibling specs.** D7-U-1 is the heaviest spec in the run (22 ADRs, 5 variants, tier `Heavy`). When D7-U-1's verifier finding lands (high base rate given complexity), re-dispatch budget allows ≤1 PR — but the sibling U-A + U-B specs are on the same branch, so either cherry-pick (inflates PRs + risks merge conflicts) or block whole Wave-6.3 (serializes what was supposed to be parallel). Open Question 3 named this risk but Round-2 didn't resolve it.

Secondary failures: Phase-6-followup deferral fires but lacks the triple-binding artifact instantiation (handoff stub, morning-summary line, next-run prompt slot must be pre-authored, not deferral-time); matrix subagent (Wave 6.4) runs over context budget reading 10 specs cold; U-C exemplar §0 ADR-citation-index pairing might be wrong and all 7 downstream variant-bearing specs inherit the bug.

**Amendments:** (1) split Wave 6.3 into 2 PRs (U-A+U-B together; D7-U-1 alone); (2) pre-author deferral triple-bind artifacts by filename now; (3) U-C exemplar self-check gate — lead agent runs (a)-(g) on U-C exemplar before fanout, records pass/fail in brief.

### Reviewer 5 — naive newcomer (`accept-with-named-amendments`)

**18 glossary gaps + ambiguity findings:** "framework-ADR + per-variant pairing" never defined inline (must infer from table); "common / orphan / per-variant" never defined; "designed-system" overlaps inconsistently with "common substrate" in §0 table; the partition between "orphan" and "per-variant" in the per-candidate ADR set table is not given so subagents can't mechanically classify their ADRs; jargon "RG primitive / X_UNM_B / F-mode / F47 / F33 / F51 / F37" used without definition; "tracks/<id>.md" and "sub-tracks/<id>.md" never explained; "DEC-1.a / DEC-2 / AGENT-ENTRY" linked without DEC unpacked; "Phase-3.5.5" used in upstream docs without brief glossary; non-U-C subagent can't author §0 because per-variant ADR IDs deferred to handoff prose; §0 column conventions (sort order, Layer enum, separator) unspecified; sub-wave PR coordination (branch name, file-uniqueness convention, conflict protocol) unstated; subagent-count inconsistency ("17 subagents total" vs Open-Q-7); self-check (c) and (g) ambiguous regarding which framework ADRs the candidate actually claims; "exact per-candidate ADR set" not enumerated (handoff has prose "Common substrate set" — which subset?); exemplar timing unstated (committed-on-feature-branch vs merged-to-main); "needing re-author" never defined.

**Path-reference findings:** Brief lives at `architectures/v3/decisions/`; specs live at `architectures/v3/specs/`. Most relative paths work because incidental depth-3 equivalence, but the brief should state this explicitly; line 5 rewind-point link target `../../../` resolves to repo root (placeholder bug); overlap.md path missing.

**Amendments:** add Glossary section; pre-author full per-candidate ADR enumeration (orphan + per-variant per candidate, not deferred to handoff prose); disambiguate sub-wave coordination (branch name, file convention, conflict protocol); enumerate §0 table conventions; restate exemplar timing; refine self-check (g) predicate-from-known-ADR-set; fix line 5 rewind-point link; reconcile mandate clustering tension once with one-line "purely PR-consolidation unit".

### Reviewer 6 — regulator / governance (`accept-with-named-amendments`)

**8 audit-trail defects:** (1) Round-1 reviewer findings paraphrased not preserved verbatim — auto-005 regulator flagged this same defect and required a verbatim transcript appendix; (2) honest-acknowledgement not commit-SHA-verifiable — needs Round-2 commit SHA + Round-1 commit SHA + `--before=<authordate>` filter; (3) Phase-6-followup deferral does not name the three binding-artifact-triple artifacts by filename per AGENTS-MD-2adf78e54a; (4) TL;DR fails structure-not-conclusions test in 3 lines (exemplar name, word budget numerics, PR-cap math); (5) Reviewer 1 Amendment 5 (pre-author common ADR-ID-to-file mapping) misclassified as non-load-bearing — it's actually load-bearing; (6) 3-tier verdict menu never stated as offered to reviewers; (7) Round-1 Reviewer 1 Objection 3 (mandate clustering theater) recharacterized into agreement with the lead agent's revised prior — pattern of suppression-via-paraphrase; (8) rewind-point branch named but commit SHA not pinned.

**Honest-acknowledgement verifiability gap:** the bare `git log` command in §Honest-acknowledgements (Round 2) is unanchored in time. Needs Round-2 commit SHA + `--before=<authordate>`.

**Deferral binding-artifact assessment:** the Phase-6-followup deferral names AGENTS-MD-2adf78e54a by reference but does NOT instantiate the triple (no session handoff filename, no morning-summary section text, no next-run dispatch prompt filename). Auto-005 lines 218-225 did all three concretely; this brief commits to the rule only.

**Amendments:** Round-1 reviewer-return-text appendix (verbatim) under `retrospective/2026-05-26-PPP-supplement-round1/`; rewrite honest-acknowledgement with SHAs + `--before=`; add Phase-6-followup deferral binding mechanism subsection naming the three artifacts by filename; rewrite TL;DR to structural elements; promote ADR-ID-to-file mapping to load-bearing list; add sentence under Round-1 reviewer findings confirming 3-tier menu offered; rephrase mandate-clustering rebuttal as lead-agent counter-argument not reviewer concurrence; pin rewind-point lines to commit SHAs post-commit.

### Round 2 convergence observation

All three Round-2 reviewers converge on the **pre-author-everything-in-the-brief** discipline from different angles:
- **Pre-mortemer**: pre-author deferral triple-bind artifacts; pre-run U-C exemplar self-check.
- **Newcomer**: pre-author per-candidate ADR enumeration; pre-state sub-wave coordination protocol.
- **Regulator**: pre-name deferral artifacts by filename; pre-author Round-1 reviewer-return-text appendix.

This is the load-bearing convergent amendment. Remaining amendments are quality-of-life (glossary, TL;DR rewrite, link fixes, audit-trail polish).

**No Round-2 reviewer pushed a different dispatch shape** — all three operate on Option A′ as-is with amendments. Per [AGENTS-MD-8a7029647f](../../../AGENTS.md#adversarial-review-verdict-tiers) verdict-tier semantics, three `accept-with-named-amendments` verdicts mean **Round 3 is NOT triggered**.

## Round-2 final amendments folded

The Round-2 decision (Option A′) stands. Following amendments are folded below.

### Wave-6.3 split (Reviewer 4 Amendment 1) — load-bearing

Wave 6.3 fires as 2 PRs, not 1: **PR-6.3a carries U-A + U-B** (mid-tier siblings, 2 parallel subagents); **PR-6.3b carries D7-U-1 alone** (heavy-tier, isolated blast radius). Folded into [§Decision (Round 2)](#decision-round-2) Wave-6.3 bullet (already updated above). PR-cap math updated.

### Phase-6-followup deferral binding mechanism (Reviewers 4 + 6) — load-bearing

If the Phase-6-followup deferral fires (≥2 specs fail verification, exhausting the ≤1 re-dispatch PR budget), the deferral is bound by **three named artifacts** per [AGENTS-MD-2adf78e54a](../../../AGENTS.md#deferred-work-binding-artifact-triple):

1. **Session handoff doc.** `architectures/v3/SESSION-HANDOFF-2026-05-26-phase-6-close.md` (or `…-phase-6-partial-close.md` if deferral fires). Carries a non-negotiable `## Phase-6-followup carry-forward (deferred from auto-006)` section. Names: (a) the failing spec(s); (b) the verifier findings verbatim; (c) the binding "Phase 7 MAY NOT START until Phase-6-followup is Accepted" constraint OR an explicit waiver-with-adversarial-review path.

2. **Morning summary "what I deliberately did NOT do" section.** The run's morning summary (per the autonomous-run skill end-of-run protocol) carries a `Phase-6-followup re-dispatch of ≥2 specs failing verification (per auto-006 re-dispatch threshold) — deferred to <next-run-id>` bullet.

3. **Next-run dispatch prompt.** `next-agent-prompt-phase-6-followup.md` authored at this run's close (or its absence flagged as a follow-up bullet in the morning summary). Points at the Phase-6-close handoff and at this brief.

### U-C exemplar self-check gate (Reviewer 4 Amendment 3) — load-bearing

Before dispatching Waves 6.1 / 6.2 / 6.3a / 6.3b, the lead agent **runs self-check items (a)-(g) on the U-C exemplar** and records pass/fail in this brief's [§U-C exemplar pre-fanout self-check results](#u-c-exemplar-pre-fanout-self-check-results) (subsection appended at exemplar commit time). **Failure on item (g)** (framework+variant co-location in §0) **blocks fanout** — lead agent re-authors the exemplar before any sub-wave fires.

### Per-candidate ADR set enumeration (Reviewer 5) — load-bearing

Pre-authored at [§Per-candidate ADR sets (full enumeration)](#per-candidate-adr-sets-full-enumeration) below. Replaces the "candidate-specific mapping appended per-subagent-brief" deferral; every subagent brief now inherits its candidate's exact ADR list directly from this brief.

### Sub-wave coordination protocol (Reviewer 5) — load-bearing

Each sub-wave fires from a separate stacked branch:
- **Wave 6.1 (GF)** branch: `claude/phase-6-wave-6.1-greenfield-specs`. 3 subagents: GF-S, GF-M, GF-C. Each writes exactly **one file** at `architectures/v3/specs/<id>.md` and **no other files**. Subagents dispatched in parallel; each commits independently (no rebase coordination — they write disjoint files).
- **Wave 6.2 (BF)** branch: `claude/phase-6-wave-6.2-brownfield-specs`. 3 subagents: BF-S, BF-M, BF-L. Same convention.
- **Wave 6.3a (U-mid)** branch: `claude/phase-6-wave-6.3a-unified-mid-specs`. 2 subagents: U-A, U-B. Same convention.
- **Wave 6.3b (U-heavy)** branch: `claude/phase-6-wave-6.3b-d7-u-1-spec`. 1 subagent: D7-U-1. Same convention.

**File uniqueness invariant**: each subagent's spec file is named per the candidate's ID (gf-s.md / gf-m.md / gf-c.md / bf-s.md / bf-m.md / bf-l.md / u-a.md / u-b.md / d7-u-1.md). U-C's exemplar (`specs/u-c.md`) is authored by the lead agent on `claude/phase-6-architecture-specs-NHmM3` (the parent branch) before any sub-wave branches off.

**Conflict protocol**: if a subagent finds its target spec file already exists or the branch tip moved unexpectedly, surface in return digest; do not force-push. Lead agent reconciles at aggregation time.

### Round-2 honest-acknowledgement (commit-SHA-pinned per Reviewer 6) — load-bearing

This brief lives at commit **`b3dc6d8`** on [`claude/phase-6-architecture-specs-NHmM3`](../../../) (Round 2 commit; Round 1 was **`1de1f9c`**). No Wave-6.1 / 6.2 / 6.3a / 6.3b / matrix / verifier subagent has fired pre-Round-2 close. Mechanically verifiable: `git log --all --oneline --before=<b3dc6d8-authordate> -- architectures/v3/specs/` returns empty at this commit. U-C exemplar authored AFTER this Round-2 brief closes — see [§U-C exemplar pre-fanout self-check results](#u-c-exemplar-pre-fanout-self-check-results) for the exemplar's commit reference.

### Round-1 reviewer-return-text appendix (Reviewer 6) — non-load-bearing

The three Round-1 review subagent return digests are preserved at [§Appendix A — Round-1 reviewer return digests](#appendix-a--round-1-reviewer-return-digests) below. For audit-defensibility, the appendix contains each reviewer's verdict + top-objection list + amendments + things-got-right list as the subagent returned them.

### TL;DR rewritten to structure-not-conclusions (Reviewer 6) — non-load-bearing

The TL;DR at the top of the brief has been rewritten to name structural elements (sub-products, dispatch shape parameters, binding mechanism) rather than conclusions (specific exemplar name, specific numeric tiers, specific PR-cap totals). The rewrite preserves the audit-trail discipline that TL;DRs don't restate conclusions.

### Reviewer 5 sub-amendments folded

- **Glossary**: see [§Glossary (Round-2 amendment)](#glossary-round-2-amendment) below.
- **§0 table conventions**: see [§§0 ADR-citation index table conventions (Round-2 amendment)](#0-adr-citation-index-table-conventions-round-2-amendment) below.
- **Self-check (g) refinement**: rewritten in the Round-2 revised rubric to predicate-on-candidate's-claimed-frameworks (see the revised self-check items in the rubric block).
- **Line 5 rewind-point link**: fixed to point at the branch name verbatim (no `../../../` placeholder).

### Reviewer 6 sub-amendments folded

- **3-tier verdict menu confirmation**: the Round-1 reviewer dispatch briefs offered all three tiers (`accept-as-is` / `accept-with-named-amendments` / `reject-with-counter-proposal`); confirmed by the dispatcher commits in this brief's git history.
- **Mandate-clustering rebuttal rephrased**: see [§Round-2 lead-agent counter-argument on mandate clustering](#round-2-lead-agent-counter-argument-on-mandate-clustering) below — explicitly framed as lead-agent rebuttal, not reviewer concurrence.
- **ADR-ID-to-file mapping pre-authoring**: re-classified as load-bearing in the Round-2 convergence summary.

## Glossary (Round-2 amendment)

(Per Reviewer 5. Subagent briefs inherit this section by reference.)

- **Common ADR**. Substrate ADR (in range 0010-0036) carried by ≥3 candidates. Captures a shared contract.
- **Discipline ADR**. ADR 0018-0027. Captures one of the 21 canonical disciplines (per [`disciplines/index.md`](../disciplines/index.md)).
- **Orphan ADR**. Substrate ADR for a primitive claimed by exactly one candidate. Distinguishable from "per-variant" because it has no framework parent. Example: ADR 0037 (P-10 coordination medium, GF-S only); ADR 0057 (P-32 distance estimator, U-C only); ADR 0061 (P-34 independence auditor, D7-U-1 only).
- **Per-variant ADR**. Substrate ADR for one candidate's variant of a *framework* primitive (P-19 / P-28 / P-29 / P-30). Each per-variant ADR has a parent framework ADR (0028 / 0029 / 0030 / 0036) by `Variant of` linkage. Example: ADR 0050 is the U-A variant of the P-19 framework (parent ADR 0028).
- **Framework ADR**. A common substrate ADR (currently 0028, 0029, 0030, 0036) whose contract intentionally varies by candidate via per-variant child ADRs. Per [AGENTS-MD-a9fb7b42f8](../../../AGENTS.md#framework-adr-scope-boundary-discipline), any spec citing a framework ADR MUST also cite the candidate's per-variant ADR.
- **Designed-system substrate ADR**. A common substrate ADR whose construction recipe is designed-system tier (not commodity). Currently: 0015 (P-08), 0031 (P-23), 0032 (P-12). The "designed-system" descriptor is the substrate-construction tier, orthogonal to the framework/orphan/per-variant classification.
- **2-candidate-fold ADR**. Substrate ADR for a primitive carried by exactly 2 candidates, folded into the common substrate ADR set with explicit 2-candidate cross-references. Currently: ADR 0033 (P-25, BF-S+BF-M), ADR 0034 (P-27, BF-M+BF-L), ADR 0035 (P-24, BF-S+BF-L). Treated like common ADRs in the citation rules.
- **RG primitive**. Research-gated primitive — a substrate primitive whose construction requires open research not yet resolved at synthesis time. Per [Phase-3.5.5 RG-primitive rule](../candidate-registry.md#phase-355-rule-on-load-bearing-rg-primitives-binding-user-approved-2026-05-25); spec authors carry these terms verbatim from each candidate's [`substrate-requirements/<id>.md`](../substrate-requirements/) without re-defining.
- **X_UNM_B**. The "Unified-Mandate-Brownfield" cross-mandate finding from Phase 3 — names how a unified-attempt candidate acquires the CodebaseModel-equivalent from legacy artifacts if it claims brownfield-fit. Spec §2 must articulate this if the candidate is unified-attempt and not n/a-out of all brownfield columns in §5.
- **F-mode (F1, F33, F37, F47, F51, F57, etc.)**. Failure mode identifiers from [`failure-modes-v3.md`](../failure-modes-v3.md). Specs reference F-modes when naming what discipline addresses them; spec authors carry F-mode IDs verbatim from substrate-requirements / tracks without re-deriving.
- **DEC-1, DEC-1.a, DEC-1.b, DEC-2, DEC-3, DEC-4**. Tier-1 binding decisions resolved at Phase 3.4 close (per [`decisions-captured.md`](../decisions-captured.md) — DEC-1 = unification verdict; DEC-2 = mandate-fit-is-per-(architecture × work-unit-class); DEC-3 = greenfield methodology framing; DEC-4 = brownfield methodology framing).
- **Tracks** (`tracks/<id>.md`). Phase-2 track sketches for each of the 10 candidates. Spec authors cite their candidate's track for cycle-structure + regime-structure + methodology-derivation source material.
- **Sub-tracks** (`sub-tracks/<id>.md`). Per-candidate sub-track authoring outputs from Wave 4.5. Currently exist for BF-L (smoke-test alternatives) and U-B (invariant authoring); other candidates have no sub-track files.
- **Phase 3.5.5**. The Phase-3.5 RG-primitive recheck step that surfaced the load-bearing RG-primitive rule. Spec authors do not need to engage with this phase's internal mechanics; carry RG-primitive citations verbatim from substrate-requirements.
- **Mandate-fit YAML value semantics** (Round-2 amendment per Reviewer 2):
  - `greenfield` — candidate is greenfield-fit on this work-unit-class.
  - `brownfield` — candidate is brownfield-fit on this work-unit-class.
  - `both` — candidate explicitly claims both mandates' fit on this work-unit-class.
  - `n/a` — candidate deliberately rejects this work-unit-class as in-scope. **MUST be accompanied by a one-line reason in §5.**
  - `silent` — candidate has no position on this work-unit-class. Different from `n/a`: silence is not a claim.

## §0 ADR-citation index table conventions (Round-2 amendment)

(Per Reviewer 5. Subagent briefs inherit by reference.)

- **Sort order**: ascending by ADR ID.
- **Layer enum**: `common-substrate` / `discipline` / `designed-system-substrate` / `orphan-substrate` / `per-variant-substrate` / `2-candidate-fold-substrate`. (Specs may use shorter labels — `common` / `discipline` / `orphan` / `per-variant` — as long as the Layer column is consistent within the spec.)
- **Variant-of column**: `—` (em-dash) when the ADR is not per-variant; otherwise the parent framework ADR ID (4-digit zero-padded, e.g., `0028`).
- **Citing § column**: comma-separated section numbers where the ADR's content is invoked in the spec (e.g., `§2, §3`).
- **Markdown table format** with pipes; not YAML, not CSV.

## Per-candidate ADR sets (full enumeration)

(Per Reviewer 5. Pre-authored to replace the per-subagent-brief deferral. Each candidate's spec author inherits this section verbatim.)

**Common-substrate baseline** (every candidate cites all 8 commodity ADRs unless otherwise noted): 0010 (P-01), 0011 (P-02), 0012 (P-05), 0013 (P-06), 0014 (P-07), 0015 (P-08), 0016 (P-14), 0017 (P-22).

**Discipline baseline** (every candidate cites all 10 discipline ADRs unless the candidate explicitly rejects a discipline): 0018 (bias-guard), 0019 (cognitive-escrow), 0020 (cost-ceiling), 0021 (holdout), 0022 (honesty), 0023 (knowledge-promotion), 0024 (regime-classification), 0025 (scoping), 0026 (three-loop), 0027 (trifecta-closure).

**Designed-system / framework substrate** (most candidates cite these, with framework ADRs requiring per-variant pairings):
- 0028 (P-19 framework) + candidate's per-variant ADR.
- 0029 (P-28 framework) + candidate's per-variant ADR.
- 0030 (P-29 framework) + candidate's per-variant ADR.
- 0031 (P-23) — cited by candidates that need dependency-impact graphs.
- 0032 (P-12) — cited by candidates that need a deterministic linter framework.
- 0036 (P-30 framework) + candidate's per-variant ADR (only the candidates that claim P-30).

**2-candidate-fold substrate** (cited by 2 candidates each):
- 0033 (P-25 camel-perimeter) — BF-S + BF-M.
- 0034 (P-27 archaeological brief) — BF-M + BF-L.
- 0035 (P-24 attribution store) — BF-S + BF-L.

**Candidate-specific ADRs (orphan + per-variant)** per the [Phase-5-close handoff](../SESSION-HANDOFF-2026-05-25-phase-5-close.md#candidate-set-state-at-phase-5-close):

| Candidate | Orphan ADRs | Per-variant ADRs | Total exact ADR count |
|---|---|---|---|
| **GF-S** | 0037 (P-10), 0038 (P-15) | 0039 (P-19/GF-S) | 8 common + 10 discipline + 0015 (P-08 designed-system) + 0031 (P-23) + 0032 (P-12) + 0028 (P-19 framework) + 0039 (per-variant) + 2 orphans = ~20-23 ADRs |
| **GF-M** | 0040 (P-20), 0041 (P-21) | (none) | 8 common + 10 discipline + 0015 + 2 orphans = ~21 ADRs |
| **GF-C** | 0042 (P-11), 0043 (P-17), 0044 (P-18) | (none) | 8 common + 10 discipline + 0015 + 3 orphans = ~22 ADRs |
| **BF-S** | (none) | (none) | 8 common + 10 discipline + 0015 + 0017 (P-22) + 0033 (P-25 fold) + 0035 (P-24 fold) = ~22 ADRs |
| **BF-M** | 0045 (P-03), 0046 (P-04) | 0049 (P-19/BF-M) [or BF-L; verify against handoff prose] | 8 common + 10 discipline + 0015 + 0033 + 0034 + 2 orphans + 1 variant + 0028 framework = ~25 ADRs |
| **BF-L** | 0047 (P-26), 0048 (P-13) | 0049 (P-19/BF-L) | 8 common + 10 discipline + 0015 + 0034 + 0035 + 2 orphans + 1 variant + 0028 framework = ~25 ADRs |
| **U-A** | (none) | 0050 (P-19/U-A), 0051 (P-28/U-A), 0052 (P-29/U-A), 0053 (P-30/U-A) | 8 common + 10 discipline + 0015 + 0028/0029/0030/0036 frameworks + 4 per-variants = ~26 ADRs |
| **U-B** | 0054 (P-31) | 0055 (P-28/U-B), 0056 (P-29/U-B) | 8 common + 10 discipline + 0015 + 0029/0030 frameworks + 1 orphan + 2 per-variants = ~24 ADRs |
| **U-C** (exemplar) | 0057 (P-32) | 0058 (P-19/U-C), 0059 (P-28/U-C) | 8 common + 10 discipline + 0015 + 0028/0029 frameworks + 1 orphan + 2 per-variants = ~23 ADRs |
| **D7-U-1** | 0060 (P-33), 0061 (P-34) | 0062 (P-28/D7-U-1), 0063 (P-29/D7-U-1), 0064 (P-30/D7-U-1) | 8 common + 10 discipline + 0015 + 0029/0030/0036 frameworks + 2 orphans + 3 per-variants = ~26 ADRs |

(Spec authors must verify their candidate's exact ADR count against the Phase-5-close handoff before authoring §0. The table above is the lead-agent best draft of the canonical breakdown; any discrepancy with the handoff prose is a spec-author-time finding to surface in the return digest.)

## Round-2 lead-agent counter-argument on mandate clustering

(Per Reviewer 6 Amendment 7. Round-1 Reviewer 1 Objection 3 stated mandate clustering is "theater" because all sub-waves fire concurrent with the same brief shape. The Round-2 lead-agent counter-argument, NOT reviewer concurrence:)

Mandate clustering survives Round 2 because the PR-consolidation amendment (Reviewer 3) requires a cluster boundary at dispatch time — the unit of PR consolidation IS the mandate cluster. Without mandate clustering, the PR-consolidation amendment has no natural grouping (alphabetical by candidate? randomly assigned to 3 PRs?). Mandate clustering thus is preserved purely as the unit of PR consolidation; it carries no rubric or dispatch-ordering implication; the four sub-waves fire concurrent.

Reviewer 1 may not concur with this counter-argument. The lead agent records the reasoning here so the audit trail shows the disagreement explicitly.

## U-C exemplar pre-fanout self-check results

(Per Reviewer 4 Amendment 3. Subsection populated at exemplar-commit time. Until populated, no sub-wave fires.)

| Self-check item | Result | Notes |
|---|---|---|
| (a) `wc -w` against tier 3000-4500 | TBD | run at exemplar-commit time |
| (b) `ls` on every cited ADR file | TBD | run at exemplar-commit time |
| (c) `grep` for §0-§7 headers | TBD | run at exemplar-commit time |
| (d) `grep` YAML frontmatter `mandate-fit:` block | TBD | run at exemplar-commit time |
| (e) `grep -E '^\| 0[0-9]+'` on §0 table | TBD | row count vs handoff table |
| (f) `grep -F` verbatim text-pull from overlap.md / decisions-captured rows | TBD | when invoked |
| (g) `grep` per framework-ADR ID (0028, 0029) in §0 — U-C claims P-19 + P-28 frameworks → expect non-empty Variant-of column | TBD | **load-bearing** — failure here blocks fanout |
| **Exemplar commit SHA** | TBD | populated at commit time |

## Round-2 final decision

**Option A′** (per [§Decision (Round 2)](#decision-round-2) above), **with all Round-2 amendments folded in**: Wave-6.3 split into 6.3a + 6.3b; Phase-6-followup deferral triple-bind by named artifacts; U-C exemplar self-check gate; per-candidate ADR set enumeration pre-authored; sub-wave coordination protocol; commit-SHA-pinned honest-acknowledgement; Round-1 reviewer-return-text appendix; TL;DR structure-not-conclusions rewrite; Glossary section; §0 table conventions; mandate-clustering rebuttal as lead-agent counter-argument.

**Decision is locked. U-C exemplar authoring fires next.**

---

## Appendix A — Round-1 reviewer return digests

(Per [Reviewer 6 Amendment 1](#reviewer-6--regulator--governance-accept-with-named-amendments). Preserved verbatim from the three Round-1 subagent returns. Verdicts confirmed via the 3-tier menu offered per AGENTS-MD-8a7029647f.)

### Round-1 Reviewer 1 — Phase-6-pipeline architect (verdict: `accept-with-named-amendments`)

**Top objections (4)**:
1. GF-M exemplar miscalibrates the heavier candidates — repeats the auto-005 Round-1 mistake. GF-M has 5 primitives, no contested-primitive references, no §3 fixed-header sub-sections, X_UNM_B is N/A, zero load-bearing RG primitives. Compare D7-U-1 (5 primitives but 3 contested-primitive sub-sections, full X_UNM_B articulation, load-bearing RG primitive).
2. The §3 "Substrate composition" rubric is shaped by a candidate that has nothing to demonstrate there. GF-M cites none of P-19/P-28/P-29/P-30. The framework-ADR/per-variant citation pair (load-bearing discipline of the rubric) is not demonstrated by the exemplar.
3. Mandate clustering at brief-shape time is theater on this dispatch shape. Concurrent firing means no learning between waves, no per-mandate aggregation gate. Clustering reduces to labeling.
4. Verifier-1 cannot catch the dominant cross-spec failure mode it claims to. Verifier-1 as scoped checks structural citation existence, not interpretation drift.

**Amendments**: swap exemplar to U-C; rewrite §A footnote into per-candidate budget exceptions (BF-L + D7-U-1 ceiling 4500); narrow Verifier-1 + broaden Verifier-2; drop mandate clustering OR add real reason; pre-author common ADR-ID-to-file mapping table.

### Round-1 Reviewer 2 — spec-quality auditor (verdict: `accept-with-named-amendments`)

**Top objections (6)**:
1. Framework-ADR + per-variant cross-reference floor is not mechanically testable. `grep` cannot verify pairing across distant sections. Need `## ADR-citation index` table making pairing a single-row grep target.
2. Mandate-fit YAML schema carries hidden ambiguity. DEC-2 schema is `greenfield | brownfield | both | n/a`; brief uses `-fit` suffix. Neither distinguishes "silent" from "deliberately not-applicable."
3. Word budget 2000-3500 is under-budgeted: sum of all section budgets = 2425-3500 baseline, leaving zero headroom for BF-L (20 ADRs) or D7-U-1 (22 ADRs).
4. Missing critical section: §0 ADR-citation index table.
5. Citation floor "~25-35 references" is hand-wavy. Make floor exact per Phase-5-close handoff table.
6. Self-check rubric misses verbatim text-pull discipline (AGENTS-MD-bf4431be57).

**Amendments**: add §0 ADR-citation index; word budget 2500-4500 + 500/extra-per-variant; replace hand-wavy reference count with exact per-candidate ADR floor; resolve `-fit` suffix; add `silent` value or require `n/a` rationale; add self-check (f) verbatim text-pull and (g) framework+variant co-location.

### Round-1 Reviewer 3 — cost/scope hawk (verdict: `accept-with-named-amendments`)

**Top objections (5)**:
1. PR-cap math under-counted: realistic count is 18-20 PRs vs ≤15 cap.
2. Two verifiers is overkill — Verifier-2 ("every ADR cited") is a `grep -L` script, not a subagent.
3. Re-dispatch budget ≤2 PRs is unrealistic at 9 concurrent specs.
4. Lead-agent ingest of ~35K words of returns is operationally optimistic — brief doesn't mandate digest length.
5. Per-candidate ADR-ID-to-file mapping table production cost unaccounted for (~225 mapping table rows).

**Amendments**: consolidate spec PRs to 3 per-sub-wave PRs; collapse to 1 verifier + lead-agent inline `grep -L` script; mandate subagent return digest ≤500 words; raise re-dispatch budget to 3 PRs OR accept Phase-6-followup deferral; pre-author one ADR-mapping table per mandate cluster.

---

*(Round 2 closed 2026-05-26. No Round 3 needed — Round-2 reviewers converged on amendments, not different dispatch shapes.)*
