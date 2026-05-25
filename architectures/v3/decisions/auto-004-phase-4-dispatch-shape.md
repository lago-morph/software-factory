# auto-004 — Phase 4 dispatch shape

**Author.** Lead agent, unattended Phase-4 dispatch session 2026-05-25.
**Status.** **Round 1 (lead-agent's best call, prior to adversarial review).** Round 2 will be appended after real adversarial subagents return per the [AGENTS.md adversarial-review rule](../../../AGENTS.md#adversarial-review-must-be-real-subagents).
**Rewind point.** This brief's commit on `claude/auto-004-phase-4-dispatch-shape`. Reverting it returns the Phase-4 dispatch shape to "undecided"; the substrate-requirements fanout has not fired yet and is dispatch-shape-agnostic.

**User direction (received 2026-05-25 with this dispatch).** The user has directed: "Per-candidate parallel fanout: 10 per-candidate substrate-requirements subagents in parallel + 1 lead-agent primitive-overlap analysis + a small fanout for discipline extraction." This brief records the **lead-agent framing** of how that direction implements (per-subagent brief shape, deliverable schema, discipline-extraction fanout size, sequencing against Phase 4.2). Adversarial review focuses on the framing, not the user's underlying choice.

---

## The question

Phase 4 produces three sub-products per the [v1.2 plan revision](../../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md#phase-4--per-candidate-substrate-requirements--shared-discipline-extraction-revised-in-v12):

- **4.1** Per-candidate substrate-requirements summary (×10 candidates).
- **4.2** Primitive-overlap analysis (1 file; informational, not winner-picker).
- **4.3** Shared-discipline inventory (architecture-level disciplines named across candidates).

The dispatch shape determines whether 4.1 fires as 10 parallel per-candidate subagents, or 3 batched per-mandate subagents (GF / BF / U), or a hybrid (lead-agent-inline for simplest candidates + per-primitive subagents for the rest); and how 4.3 fanout is sized; and where 4.2 sits in the sequence.

## Alternatives considered

### A. Per-candidate parallel fanout — **chosen** (per user direction)

- **4.1:** 10 per-candidate substrate-requirements subagents in one parallel fanout wave.
- **4.2:** 1 lead-agent primitive-overlap analysis, after 4.1 lands.
- **4.3:** Small parallel fanout for discipline extraction (1-2 subagents — see "Discipline-fanout sizing" below).

- **Per-subagent scope (4.1).** One candidate. The subagent consumes the candidate's track file (or D7-U-1's blind-axis file) + [`candidate-registry.md`](../candidate-registry.md) entry + the [primitive sketches](../primitives/) for primitives the candidate names + the [`primitives/index.md`](../primitives/index.md) post-sketch annotations + BF-L's [auto-003](auto-003-bfl-rg-view-choice.md) per-view choice (binding for BF-L only) + the X_UNM_B caveat (binding for unified-attempt candidates). Output: `architectures/v3/substrate-requirements/<candidate-id>.md` listing buildability-confirmed primitives by ID, open RG primitives with their (a)/(b) treatment, candidate-specific contracts on each primitive, and the X_UNM_B Codebase-Model-acquisition articulation for unified candidates claiming brownfield-fit.

- **Pros.**
  - Honors the user's direct choice.
  - Simpler aggregation than per-mandate batched: each subagent produces exactly one file at a known path. Lead-agent diff for 4.2 reads 10 files of known shape rather than 3 batched-output files that themselves require de-batching.
  - No cluster-boundary judgment overhead at dispatch time (per-mandate batched would require choosing whether U-A/U-B/U-C/D7-U-1 batch as one "unified-attempt" subagent or split per-axis; per-candidate sidesteps).
  - Crisp per-candidate accountability — easy to identify which candidate's summary is weak and re-dispatch only that one.
  - Same total cost as batched (per the user's prompt observation): one subagent reads one candidate's tracks vs one subagent reads multiple candidates' tracks; the per-token cost of substrate-requirements work scales with candidate count, not with dispatch shape.
  - Maximum parallelism (10 concurrent), shortest wall-clock to Phase-4.1 close.

- **Cons.**
  - 10 subagents to brief and monitor — higher coordination overhead than 3 batched. Mitigated by uniform brief shape and uniform output schema (see "Brief shape" below).
  - Risk of cross-candidate inconsistency in interpretation (e.g., two candidates handling the X_UNM_B caveat differently). Mitigated by the uniform brief explicitly naming X_UNM_B as a required section for unified candidates.
  - No cross-candidate same-vs-distinct verdicts surface at subagent level — those are deferred to 4.2 by design. Counter: this is feature, not bug; the [Round-2 amendment to auto-001](auto-001-phase-3.5-dispatch-shape.md#amendments-to-the-dispatch-brief-that-will-be-sent-to-subagents) already established that same-vs-distinct verdicts belong at the lead-agent overlap level, not at the per-candidate level.

### B. Per-mandate batched (3 GF + 3 BF + 4 U)

3 subagents: greenfield (GF-S+GF-M+GF-C), brownfield (BF-S+BF-M+BF-L), unified-attempt (U-A+U-B+U-C+D7-U-1). Each produces 3-4 substrate-requirements files within a single subagent context.

- **Pros.** Fewer dispatches; per-mandate context-sharing within a subagent (the unified subagent reads all 4 unified tracks once).
- **Cons.** Aggregation re-decomposes 3 batched outputs into 10 candidate files. Cluster-boundary judgment overhead (D7-U-1 from the blind-axis file batches with U-A/B/C or separately?). Loss of crisp per-candidate accountability. **Not chosen** per user direction.

### C. Hybrid (lead-agent-inline for simplest + per-candidate for the rest)

Lead-agent-inline summaries for candidates whose substrate-requirements are essentially "the cluster primitives + standard methodology hooks" (plausibly GF-M, BF-M); per-candidate subagents for the rest.

- **Pros.** Lower cost.
- **Cons.** "Simplest" classification itself requires judgment + risks anchoring (lead agent's inline summaries inherit the lead agent's framing without fresh subagent challenge); breaks uniform output schema. **Not chosen** per user direction.

### D. Lead-agent-inline for all 10

Lead agent writes all 10 substrate-requirements summaries in one pass.

- **Pros.** Lowest cost.
- **Cons.** Saturates context with candidate details; forecloses per-candidate subagent independence; cannot run parallel. **Not chosen** per user direction.

## Decision (Round 1)

**Option A. Per-candidate parallel fanout.**

Concretely:

- **Wave 4.1 (parallel fanout, 10 subagents).** One subagent per candidate. Brief shape below. Dispatch follows the [auto-003](auto-003-bfl-rg-view-choice.md) verdict landing (the BF-L brief depends on the (a)/(b) choice for both views being declared) and follows this brief landing (for the X_UNM_B framing).

- **Wave 4.3 (parallel fanout, 1-2 subagents).** Discipline extraction. See "Discipline-fanout sizing" below. Can run concurrent with Wave 4.1 — disciplines don't depend on per-candidate substrate-requirements decisions.

- **Wave 4.2 (lead-agent serial).** After Wave 4.1 lands. Lead-agent diff over the 10 per-candidate summaries. Resolves the deferred same-vs-distinct questions (P-28 / P-29 / P-30 variants; P-19 classifier variants; P-08↔P-09 collapse; P-12↔P-16 absorption). Output: `architectures/v3/primitives/overlap.md`.

- **Wave 4.4 (BF-L parallel research dispatch, NEW per auto-003).** 2 deep-research subagents on BF-L's conventional + invariant views. Concurrent with Wave 4.1; outputs feed Phase 5 + Phase 8 directly.

### Brief shape sent to each Wave-4.1 subagent

The per-candidate subagent receives:

1. **Candidate identity + track-file pointer.** "You are producing the substrate-requirements summary for `<candidate-id>` whose track lives at `<path>`."
2. **Mandatory inputs:** the candidate's track file; the candidate's entry in `candidate-registry.md` (including Phase-3.5.5 detail + the Phase-3.5.5 RG-primitive rule application table); the per-primitive sketches for every primitive the candidate names; `primitives/index.md` post-sketch annotations; for BF-L specifically, [`auto-003`](auto-003-bfl-rg-view-choice.md); for unified-attempt candidates, the X_UNM_B framing in `candidate-registry.md`.
3. **Required output sections** (uniform schema across all 10 subagents):
   - **§1 Primitive list (buildability-confirmed).** Bulleted P-IDs the candidate names with one-line role per primitive, citing the per-primitive sketch.
   - **§2 RG primitives.** Per the [Phase-3.5.5 RG-primitive rule](../candidate-registry.md#phase-355-rule-on-load-bearing-rg-primitives-binding-user-approved-2026-05-25), list any RG primitives with their (a) bounded sub-track or (b) accept-as-RG treatment, citing the sketch and the registry table.
   - **§3 Candidate-specific contracts on each primitive.** Where the candidate's contract differs from the sketch's default contract, name the difference. (E.g., U-B's layer-typed envelope on P-28 vs U-A's typed-node-graph envelope.)
   - **§4 X_UNM_B articulation.** For unified-attempt candidates only — how the candidate acquires the Codebase Model equivalent from legacy artifacts if it claims brownfield-fit. For other candidates, this section says "N/A (mandate-specific candidate)" or "N/A (greenfield-only)".
   - **§5 Open carries.** Phase-4-internal workstreams (e.g., U-B invariant-authoring sub-track; BF-L per-view sub-tracks), Phase-5 ADR seeds, Phase-8 lean-eval candidates.
   - **§6 Scoping-principle compliance.** Confirms the summary preserves the candidate as a defensible architecture proposal; does not pre-eliminate; surfaces RG flags honestly.
4. **Constraints.**
   - **No same-vs-distinct verdicts** across candidates (those belong at Wave 4.2). The subagent reads only its assigned candidate's primitives; cross-candidate comparison is forbidden at this layer.
   - **No methodology rewriting.** The summary captures substrate requirements; it does not edit the candidate's methodology shape (that's Phase 5/6).
   - **Cite the sketches and registry by relative link** per the [internal-document-references rule](../../../AGENTS.md#internal-document-references).
   - **Length budget.** 800-1500 words per summary. The summary is a digest, not a re-derivation of the sketches.
5. **Deliverable path.** `architectures/v3/substrate-requirements/<candidate-id>.md` where `<candidate-id>` is the lowercase candidate ID per the registry (`gf-s`, `gf-m`, `gf-c`, `bf-s`, `bf-m`, `bf-l`, `u-a`, `u-b`, `u-c`, `d7-u-1`).

### Discipline-fanout sizing (Wave 4.3)

The user named "a small fanout" without size. Lead-agent default: **2 subagents** running in parallel.

- **Subagent 1 — methodology-track-driven discipline extractor.** Reads the 9 track files in [`architectures/v3/tracks/`](../tracks/) + the D7 blind-axis files in [`architectures/v3/bias-guards/phase-3/d7-blind-axis/`](../bias-guards/phase-3/d7-blind-axis/). Extracts named architecture-level disciplines: three-layer citation discipline, concrete-task discipline, bias-guard discipline, watchdog escalation discipline, cost-ceiling enforcement discipline, knowledge-promotion discipline, holdout-partition discipline, etc. Output: `architectures/v3/disciplines/index.md` + initial per-discipline stubs.

- **Subagent 2 — sketch-and-registry-driven discipline extractor.** Reads [`candidate-registry.md`](../candidate-registry.md) + [`primitives/index.md`](../primitives/index.md) post-sketch annotations + the per-primitive sketches. Extracts cross-cutting disciplines named *in the substrate layer* that aren't substrate primitives or methodology choices (per-role read-filter discipline, snapshot-consistency-at-version-boundaries discipline, RG-primitive rule, three-layer citation discipline as observed in the sketches' citation patterns, etc.). Output: a parallel index that the lead agent merges with Subagent 1's output before Phase 4 close.

Both subagents are forbidden from making per-candidate decisions; they extract disciplines, not adjudicate candidate use of them. The merge is a lead-agent step at Phase-4-close time.

Alternative: 1 subagent doing both reads. Rejected because the two passes (track-file reading vs sketch-reading) are different cognitive operations and benefit from independent framings before merge. Cost is 1 additional subagent for meaningfully higher robustness.

### Wave 4.2 sequencing

Lead-agent-serial, post-Wave-4.1. Reads all 10 summaries + the [P-28 / P-29 / P-30 sketches](../primitives/) and renders verdicts on:

- P-28 variants (U-A typed-node-graph vs U-B layer-typed vs U-C anchor vs D7-U-1 FC): same primitive with per-variant envelope schema, or distinct primitives?
- P-29 variants (U-A policy mediator vs D7-U-1 compounding gate): same with per-variant policy DSL, or distinct?
- P-30 variants (U-A re-entry registrar vs D7-U-1 survival-window registrar): same with per-variant state machine, or distinct?
- P-19 variants (GF-S eligibility / BF-L per-region regime / U-C distance-gated dispatcher): same classifier framework with different feature sources, or distinct?
- P-08 ↔ P-09 collapse: is P-09 a thin read-API on P-08, or a separate runner primitive?
- P-12 ↔ P-16 absorption: does P-16's rule library absorb into P-12's framework?

Output: `architectures/v3/primitives/overlap.md`. Informational — not winner-picking — per the v1.2 plan.

## Downstream impact

- **Phase 5 (ADRs).** ADR count and shape depend on Wave-4.2 verdicts (e.g., if P-28 variants collapse to one primitive with envelope-variant ADRs, the ADR count shrinks; if they stay distinct, the count grows).

- **Phase 6 (architecture specs).** One spec per candidate, drawing on the candidate's substrate-requirements summary as the substrate scaffold + the methodology shape from the track file.

- **Phase 8 (lean-evals).** Pressure-tests both the substrate-requirements claims and the methodology claims. The substrate-requirements summary's §5 "Open carries" feeds the lean-eval design directly.

- **In-flight tracking.** Wave 4.1 (10 parallel subagents) + Wave 4.3 (2 parallel subagents) + Wave 4.4 (2 parallel research subagents) = 14 subagents total, running concurrent with this brief's adversarial review (4 reviewers across auto-003 + auto-004). Per the [in-flight-workflow-tracking skill](../../../.claude/skills/in-flight-workflow-tracking/SKILL.md), this is tracked as a long-running async dispatch.

## If-user-overrides rewind point

Rewind to: the commit on `claude/auto-004-phase-4-dispatch-shape` that lands this brief. Reverting it returns the dispatch shape to undecided; the user can then pick option B (per-mandate batched), option C (hybrid), or option D (lead-agent-inline). Wave 4.1, 4.3, 4.4 have not fired at brief-landing time — only this brief is committed; the subagent dispatches happen in a subsequent commit and are independently revertable.

## Adversarial review

**Status: pending.** Per the [AGENTS.md adversarial-review rule](../../../AGENTS.md#adversarial-review-must-be-real-subagents), real adversarial subagents will be dispatched against this brief before its final commit. Reviewer angles:

1. **Aggregation-cost auditor.** Challenges whether 10 parallel subagents' uniform schema actually delivers the "simpler aggregation" the brief claims, vs hidden costs (e.g., cross-candidate inconsistency, X_UNM_B drift across the 4 unified subagents, RG-flag treatment drift between BF-L and U-B). Probes whether the brief's uniform-output-schema strategy is enforceable in practice.

2. **Discipline-fanout-size skeptic.** Challenges the 2-subagent split for Wave 4.3. Tests whether 1 subagent or 3 would be a better allocation; whether the track-vs-sketch split is the right cut; whether the lead-agent merge step adds enough value to justify the parallel passes.

3. **Sequencing skeptic.** Challenges the Wave 4.2 / Wave 4.1 sequencing. Probes whether Wave 4.2 could run concurrent with Wave 4.1 (using preliminary summaries) or whether the serial dependency is genuine. Tests whether Wave 4.4 (BF-L research dispatch from auto-003) sequencing relative to Wave 4.1 is right.

Round 2 will follow with the reviewers' findings + the lead-agent's revised decision (or confirmation of Round 1) + amendments to the brief shape and discipline-fanout sizing.
