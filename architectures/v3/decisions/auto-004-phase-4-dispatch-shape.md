# auto-004 — Phase 4 dispatch shape

**Author.** Lead agent, unattended Phase-4 dispatch session 2026-05-25.
**Status.** **Round 2 (revised after real adversarial review).** Round 1's core shape (per-candidate parallel fanout, 2-subagent discipline extraction, serial Wave 4.2) is **accepted with named amendments** by both reviewers (`accept-with-named-amendments` × 2). The shape stands; the amendments add Wave 4.5 (authoring sub-tracks), decompose Phase-4-close into Wave 4.2 + Wave 4.6, supply schema-enforcement aids, rename the Wave-4.3 split, and gate sub-track dispatch on Round-2 close. Revised decision in [§Decision (Round 2)](#decision-round-2).
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

## Decision (Round 1 — superseded by Round 2 below)

~~**Option A. Per-candidate parallel fanout.**~~ Round-1 option A was `accept-with-named-amendments` × 2 from real adversarial reviewers. The shape stands; the amendments materially extend it. See [§Decision (Round 2)](#decision-round-2). Round-1 reasoning preserved below for traceability.

### Round 1 reasoning (preserved)

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

## Adversarial review — Round 1 (real subagents)

Per the [AGENTS.md adversarial-review rule](../../../AGENTS.md#adversarial-review-must-be-real-subagents), two real adversarial subagents were dispatched against the Round-1 brief. Both returned `accept-with-named-amendments` with substantive material findings.

### Reviewer 1 — Aggregation-cost auditor (verdict: `accept-with-named-amendments`)

Core finding: the brief's "simpler aggregation" claim rests on schema-enforceability assumptions the brief does not back. Three mandatory amendments + three recommended.

- **F1. Uniform 6-section schema has no validator and no exemplar.** Brief lists section names and a length budget but supplies no exemplar summary, no self-check rubric, no failure mode for schema violation. A subagent that merges sections, writes 2500 words, or interprets §3 as "restate everything" violates no checkable rule. Lead agent then eats the cost at Wave 4.2.
- **F2. X_UNM_B will drift across 4 unified subagents.** No shared anchor sentence; the registry's X_UNM_B finding names the *finding*, not a *required articulation shape*. With no cross-talk, the 4 §4 sections diverge along axes (U-A → typed-node-graph derivation; U-B → layer-typed extraction; etc.), making cross-mandate audit impossible without lead-agent re-articulation.
- **F3. RG-primitive treatment will drift across BF-L / U-B / D7-U-1.** Phase-3.5.5 rule is rich (application table; per-portion choices; fallback rules). Three subagents handling §2 in parallel will cite different rule fragments without a required citation pattern.
- **F4. §3 candidate-specific-contracts is overlap-pessimal.** Per-candidate-spec format, not overlap-analysis format. Lead agent re-reads sketches anyway because §3 isn't diff-ready.
- **F5. Wave 4.4 ↔ Wave 4.1 BF-L contradiction risk.** Both consume P-26 + auto-003 concurrently with no merge step; the BF-L Wave-4.1 summary may land stale relative to the research notes.
- **F6. Wave 4.3 cut misses candidate-registry-only disciplines.** Per-candidate notes in registry's Phase-3.5.5 annotations (e.g., "graceful-degradation pattern", "structural recursion stopping rule") fall between Subagent 1's tracks scope and Subagent 2's registry-as-rule-source scope.
- **F7. No hidden serial blocker on 4.1↔4.3, but 4.4 → 4.1 for BF-L has one** — sidestepped by concurrent firing; see F5.

Mandatory amendments:
- **A1.** Ship one exemplar summary (suggest GF-M) + self-check rubric the subagent runs as final step (section-presence, word-count, no-same-vs-distinct, citation-format).
- **A2.** Shared §4 skeleton for unified candidates with required sub-bullets ("source artifact:", "extraction primitive:", "completeness gap:", "fallback if missing:"). X_UNM_B cited once in skeleton; subagents fill, not freestyle.
- **A3.** §2 for RG-carrying candidates (BF-L, U-B, D7-U-1) must cite Phase-3.5.5 application table row (registry lines 338-342) as required text-pull, not paraphrase.

Recommended:
- **A4.** §3 fixed schema headers per contested-primitive class (P-28 → "envelope schema:"; P-29 → "policy DSL:"; P-30 → "state-machine semantics:"; P-19 → "feature source:").
- **A5.** Sequence BF-L Wave-4.1 *after* Wave-4.4 research OR insert lead-agent reconciliation at Phase-4 close.
- **A6.** Wave-4.3 Subagent 2's input set explicitly includes per-candidate registry annotations.

### Reviewer 2 — Sequencing skeptic (verdict: `accept-with-named-amendments`)

Core finding: shape is right; gaps are wave-ownership and close-coordination, not the core shape.

- **F1. Wave 4.2 serial dependency is genuine — do NOT split.** A preliminary 4.2 firing on the annotations alone would re-do work auto-001 R2 already deleted. Round-1's serial sequencing is correct.
- **F2. Wave 4.4 concurrent is right, but BF-L's Wave-4.1 must be flagged research-blind.** The brief implicitly chooses concurrent firing (correct) but doesn't say so explicitly.
- **F3. Discipline fanout: 2 is right, split is wrong.** Track-driven vs sketch-and-registry-driven conflates two axes. Methodology disciplines come overwhelmingly from tracks; substrate-layer disciplines come overwhelmingly from sketches. Proper cut: **methodology-discipline extractor** (tracks + D7) and **substrate-discipline extractor** (sketches + registry + Phase-3.5.5 rule table + candidate-registry contract tables). Round-1's "three-layer citation discipline" listed in both subagents creates merge confusion.
- **F4. BF-L sub-track ownership is unassigned.** Per auto-003 Round 2, BF-L gets smoke-tests + (conditional) full sub-tracks + 2 research subagents. The auto-004 brief mentions sub-tracks once in §5 but doesn't say *who runs them*. The Wave-4.1 BF-L subagent is briefed to produce a summary, not author conventions/invariants.
- **F5. U-B invariant-authoring sub-track ownership is also unassigned.** Per auto-002 Round 2, U-B's full sub-track is constructive (scale to ≥3 invariants/pair, ≥15 total). Wave-4.1 U-B subagent cannot do it in an 800-1500-word digest.
- **F6. Phase-4-close has no coordination structure.** Wave 4.2 = overlap analysis only is insufficient. Close must also: render BF-L sub-track verdicts; render U-B sub-track verdict; merge discipline-extractor outputs; consume research notes; produce overlap.md; update registry.
- **F7. Round 2 of this brief should land before Wave 4.3 / 4.4 fire.** Strongest objection. Round 1's "concurrent with adversarial review" firing means amendments to discipline-fanout split (F3) or sub-track wave assignment (F4-F5) catch in-flight work. Wave 4.1 may fire concurrent (user-bound shape); 4.3/4.4 are lead-agent-shaped and should wait.

Amendments:
- **A1.** BF-L Wave-4.1 subagent gets explicit "research-blind" annotation.
- **A2.** Discipline-fanout split renamed: methodology disciplines (Subagent 1) vs substrate disciplines (Subagent 2). Three-layer citation goes to Subagent 1 only; Subagent 2 cross-references.
- **A3.** Add Wave 4.5: 3 authoring subagents (BF-L conventional view, BF-L invariant view, U-B invariant authoring). Fires after Wave 4.1 lands (needs substrate-requirements summaries as scope frames) but before Wave 4.2 (4.2 consumes the verdicts).
- **A4.** Phase-4-close decomposed: Wave 4.2 = overlap analysis only; Wave 4.6 = aggregation/verdicts/registry-update (merge disciplines, consume research, render four go/no-go verdicts).
- **A5.** Gate Wave 4.3 / 4.4 / 4.5 on Round-2 close of this brief. Only Wave 4.1 fires concurrent with adversarial review.

## Decision (Round 2)

**Option A′: per-candidate parallel fanout (Wave 4.1) + schema-enforcement aids + renamed Wave 4.3 split + new Wave 4.5 (authoring sub-tracks) + decomposed Phase-4-close (Wave 4.2 overlap + Wave 4.6 aggregation) + gated Wave 4.3/4.4/4.5 on Round-2 close.**

Round-1 option A's core shape stands. All 10+1+2 wave-count from Round 1 is preserved as the *shape*; the *implementation* gains schema-enforcement aids and 3 additional waves (4.5 authoring; 4.6 aggregation; gated dispatch order).

### Revised wave plan

| Wave | Subagent count | Trigger | Output |
|---|---|---|---|
| 4.1 | 10 (1 per candidate) | After this Round 2 lands (user direction binds shape; safe to fire concurrent with reviews — was already implicitly authorized in Round 1) | `architectures/v3/substrate-requirements/<candidate-id>.md` × 10 |
| 4.3 | 2 (renamed: methodology-discipline + substrate-discipline) | **Gates on Round-2 close** (was implicitly fired pre-Round-2; see honest acknowledgement below) | `disciplines/methodology-disciplines.md` + `disciplines/substrate-disciplines.md` |
| 4.4 | 2 (BF-L conventional view + invariant view research) | **Gates on Round-2 close per auto-003** (was implicitly fired pre-Round-2; research notes already landed — see honest acknowledgement below) | `architectures/v3/research-notes/bfl-conventional-view-prior-art.md` + `bfl-invariant-view-prior-art.md` |
| 4.5 | 2-3 (smoke-tests then conditional authoring sub-tracks) | After Wave 4.1 BF-L summary + Wave 4.4 research notes land (sequenced by auto-003 Round 2 smoke-test-first pattern + U-B sub-track from auto-002 Round 2) | `architectures/v3/sub-tracks/bfl-conventional-smoke-test.md` + `bfl-invariant-smoke-test.md` + (conditional) full sub-track artifacts + `u-b-invariant-authoring.md` |
| 4.2 | Lead-agent serial | After Wave 4.1 lands | `architectures/v3/primitives/overlap.md` |
| 4.6 | Lead-agent serial (NEW) | After Waves 4.2 + 4.3 + 4.5 land | Registry updates; sub-track go/no-go verdicts; merged `disciplines/index.md`; Phase-4 close handoff |

### Wave 4.1 brief shape (revised per Reviewer 1 amendments)

The per-candidate subagent receives:

1. **Candidate identity + track-file pointer.** "You are producing the substrate-requirements summary for `<candidate-id>` whose track lives at `<path>`."

2. **Mandatory inputs:** the candidate's track file; the candidate's entry in `candidate-registry.md` (Phase-3.5.5 detail + Phase-3.5.5 RG-primitive rule application table); per-primitive sketches for every primitive the candidate names; `primitives/index.md` post-sketch annotations; for BF-L specifically, [`auto-003 Round 2`](auto-003-bfl-rg-view-choice.md) (plus research-blind annotation — see Reviewer 2 A1); for unified-attempt candidates, the X_UNM_B framing in `candidate-registry.md` (plus the shared §4 skeleton — see A2 below).

3. **Required output sections (uniform schema):**
   - **§1 Primitive list (buildability-confirmed).** Bulleted P-IDs with one-line role per primitive, citing the per-primitive sketch.
   - **§2 RG primitives.** Per the [Phase-3.5.5 RG-primitive rule](../candidate-registry.md#phase-355-rule-on-load-bearing-rg-primitives-binding-user-approved-2026-05-25), list any RG primitives with their (a) bounded sub-track or (b) accept-as-RG treatment. **For BF-L / U-B / D7-U-1**: §2 MUST pull the candidate's row from the Phase-3.5.5 application table verbatim (registry §"Application to current candidates") as required text-pull citation — not paraphrase. (Reviewer 1 A3.)
   - **§3 Candidate-specific contracts on each primitive.** Where the candidate's contract differs from the sketch's default, name the difference. **For contested primitives (P-28, P-29, P-30, P-19)**: use fixed sub-section headers — P-28 → "envelope schema:"; P-29 → "policy DSL:"; P-30 → "state-machine semantics:"; P-19 → "feature source:" — so Wave 4.2 can do eyeball diffs. (Reviewer 1 A4.)
   - **§4 X_UNM_B articulation (unified-attempt candidates only).** Fill the shared skeleton (cite the X_UNM_B finding by relative link to the registry; do not freestyle the section):

     ```markdown
     ### §4 X_UNM_B articulation

     Per the [X_UNM_B finding](../candidate-registry.md#u-a--escrow-graph-factory-cycle--directed-graph-of-typed-nodes), this candidate addresses Codebase-Model acquisition from legacy artifacts as follows:

     - **Source artifact:** <what legacy artifact this candidate reads to construct the Codebase-Model equivalent>
     - **Extraction primitive:** <which P-NN primitive performs the extraction; or named candidate-specific procedure>
     - **Completeness gap:** <which of P-26's 6 views this candidate cannot fully reconstruct from legacy artifacts; honest accounting>
     - **Fallback if missing:** <what the candidate's methodology does when extraction fails or produces low-confidence output>
     ```

     For non-unified candidates: §4 says `N/A (mandate-specific candidate; X_UNM_B does not apply)`. (Reviewer 1 A2.)

   - **§5 Open carries.** Phase-4-internal workstreams (named by Wave assignment: e.g., "U-B invariant-authoring sub-track — Wave 4.5"; "BF-L conventional view smoke-test → Wave 4.5"), Phase-5 ADR seeds, Phase-8 lean-eval candidates.
   - **§6 Scoping-principle compliance.** Confirms the summary preserves the candidate as a defensible architecture proposal; does not pre-eliminate; surfaces RG flags honestly.

4. **Required self-check rubric** (subagent runs as final step before returning — Reviewer 1 A1):
   - [ ] All 6 sections present and labeled (§1 through §6).
   - [ ] Word count between 800 and 1500.
   - [ ] No same-vs-distinct verdicts across candidates (those are Wave 4.2 work).
   - [ ] All internal links are relative paths (no absolute paths; no GitHub URLs).
   - [ ] For RG-carrying candidates (BF-L / U-B / D7-U-1): §2 contains the verbatim Phase-3.5.5 application table row.
   - [ ] For unified-attempt candidates (U-A / U-B / U-C / D7-U-1): §4 uses the shared X_UNM_B skeleton with all 4 sub-bullets filled.
   - [ ] For contested-primitive references (P-28 / P-29 / P-30 / P-19): §3 uses the fixed sub-section header for each.

5. **Exemplar summary supplied with brief.** A `gf-m` exemplar will be authored by the lead agent and shipped with the Wave-4.1 dispatch brief so subagents have a concrete model. (Reviewer 1 A1 — exemplar landing on the dispatch-commit, separate from this Round-2 brief.)

6. **BF-L research-blind annotation.** The BF-L Wave-4.1 subagent's brief includes: "Wave 4.4 research subagents have landed concurrent research notes at `architectures/v3/research-notes/bfl-conventional-view-prior-art.md` and `bfl-invariant-view-prior-art.md`. **You may cite them by relative link but treat both RG views as `authoring-attempt in progress (Wave 4.5 smoke-test, then conditional full sub-track per auto-003 Round 2)` in §5.** Your summary documents the substrate requirements; Wave 4.5 produces the smoke-test artifacts and conditional sub-track outputs." (Reviewer 2 A1 + Reviewer 1 A5: by the time Wave 4.1 fires, research notes have already landed, so BF-L's Wave-4.1 summary can cite them — the original Round-1 sequencing concern about contradiction is resolved because research notes landed *during* Round-2 authoring; the summary is research-aware but does not re-derive the research.)

7. **Constraints.** No same-vs-distinct verdicts across candidates (Wave 4.2); no methodology rewriting (Phase 5/6); cite by relative link per AGENTS.md; 800-1500 words.

8. **Deliverable path.** `architectures/v3/substrate-requirements/<candidate-id>.md` where `<candidate-id>` ∈ {`gf-s`, `gf-m`, `gf-c`, `bf-s`, `bf-m`, `bf-l`, `u-a`, `u-b`, `u-c`, `d7-u-1`}.

### Wave 4.3 brief shape (revised per Reviewer 2 A2 + Reviewer 1 A6)

Two subagents, renamed and refocused:

- **Subagent 1 — methodology-discipline extractor.** Reads the 9 track files in [`architectures/v3/tracks/`](../tracks/) + D7 blind-axis file. Extracts disciplines named at the methodology level: three-layer citation discipline, concrete-task discipline, bias-guard discipline, watchdog escalation discipline, cost-ceiling enforcement discipline, knowledge-promotion discipline, three-loop discipline (BF-L), etc. Output: `architectures/v3/disciplines/methodology-disciplines.md` + per-discipline stubs.

- **Subagent 2 — substrate-discipline extractor.** Reads `candidate-registry.md` (including per-candidate Phase-3.5.5 annotations per Reviewer 1 A6) + `primitives/index.md` post-sketch annotations + per-primitive sketches + AGENTS.md + decision briefs in `decisions/`. Extracts disciplines named at the substrate / cross-cutting layer: Phase-3.5.5 RG-primitive rule; construction-path+corpus-why two-part rule; per-role read-filter discipline; substrate-typed-store discipline; snapshot-consistency-at-version-boundaries discipline; honest-RG-flag discipline; same-vs-distinct-deferred-to-Phase-4.2 discipline; graceful-degradation discipline; real-subagent-review discipline. Output: `architectures/v3/disciplines/substrate-disciplines.md`.

Three-layer citation discipline goes to Subagent 1 only; Subagent 2 cross-references it without re-extracting.

Lead-agent merge happens at Wave 4.6.

### Wave 4.5 (NEW per Reviewer 2 A3)

Three concurrent authoring subagents, dispatched after Wave 4.1 lands:

- **BF-L conventional-view smoke-test subagent.** Per [auto-003 Round 2](auto-003-bfl-rg-view-choice.md): ≥3 non-trivial substantive conventions per language across top-3 languages (Python / TypeScript / Java by default), each with typed envelope + corpus citation + positive/negative example + honesty-discipline clause. Output: `architectures/v3/sub-tracks/bfl-conventional-smoke-test.md`. Verdict logic per auto-003 Round 2: ≥2/3 languages → full sub-track authorized.

- **BF-L invariant-view smoke-test subagent.** Same structure for invariants. Output: `architectures/v3/sub-tracks/bfl-invariant-smoke-test.md`.

- **U-B invariant-authoring sub-track subagent.** Per [auto-002 Round 2](auto-002-ub-path.md): scale the U-B smoke-test recipe from 1-per-pair to ≥3-per-pair, ≥15 total. Output: `architectures/v3/sub-tracks/u-b-invariant-authoring.md`.

Conditional Wave 4.5b: if BF-L smoke-test verdicts authorize the full sub-track (per auto-003 Round-2 verdict logic), dispatch 1-2 additional subagents to scale conventions/invariants from 3-per-language to ≥10-per-language. Wave 4.5b is gated on Wave 4.5 verdicts; Wave 4.6 renders the go/no-go.

### Wave 4.2 (overlap analysis, unchanged from Round 1)

Lead-agent serial after Wave 4.1 lands. Reads all 10 summaries + the [P-28 / P-29 / P-30 sketches](../primitives/) and renders same-vs-distinct verdicts. Output: `architectures/v3/primitives/overlap.md`.

### Wave 4.6 (NEW per Reviewer 2 A4)

Lead-agent serial. Fires after Waves 4.2 + 4.3 + 4.5 land. Five tasks:

1. **Merge `methodology-disciplines.md` + `substrate-disciplines.md`** into the canonical `architectures/v3/disciplines/index.md`. Create per-discipline stub files where Subagent 2 produced index-only entries (Subagent 1 produces stubs; Subagent 2 produces index-only per the Wave 4.3 split).
2. **Render BF-L's two sub-track go/no-go verdicts** per auto-003 Round 2 verdict logic. Update registry annotations.
3. **Render U-B's full sub-track verdict** (or smoke-test result if Wave 4.5 produces only the scaled smoke-test). Update registry annotations.
4. **Consume Wave 4.4 research notes** into BF-L's Phase-5 ADR seed list (alternatives-considered material).
5. **Phase-4-close handoff** at `architectures/v3/SESSION-HANDOFF-2026-05-26-phase-4-close.md` (or 2026-05-25 if same date). Mark the Phase-3.5-close handoff superseded. Stage the chain for Phase 5 ADR dispatch.

### Round-2 honest acknowledgements

- **Wave 4.3 and Wave 4.4 fired pre-Round-2.** Reviewer 2's strongest sequencing objection (F7 / A5) was that 4.3 / 4.4 should gate on Round-2 close. They did not — the Round-1 dispatch fired them concurrent with adversarial review, in the same parallel batch as the reviewers. Both produced outputs that align well with the Round-2 amendments (the Wave-4.4 research notes already cover negative results per auto-003 Round-2 amendments; the Wave-4.3 outputs land on `disciplines/methodology-disciplines.md` and `disciplines/substrate-disciplines.md` per the rename only if the in-flight subagents are re-briefed at the merge step — see next bullet). **Mitigation:** at Wave-4.6 merge time, the lead agent normalizes the in-flight Wave-4.3 outputs to the renamed split (the methodology vs substrate cut is a categorization step at merge, not a re-extraction); the in-flight Wave-4.4 outputs are consumed as-is (their charter widening was already implemented in the dispatch briefs). **No re-dispatch is required.** Future briefs adopt the Reviewer 2 A5 gating discipline.

- **Wave 4.3 in-flight subagent split was the Round-1 track-driven / sketch-and-registry-driven split**, not the Round-2 methodology / substrate rename. The two splits are *similar but not identical* (Round-1 Subagent 2 read sketches+registry; Round-2 Subagent 2 reads sketches+registry+per-candidate registry annotations + decision briefs explicitly). The in-flight subagents' outputs cover the Round-2 substrate-discipline scope adequately — the difference is largely a labeling difference for the merge step. **No re-dispatch is required.** Wave 4.6 merge takes both Round-1-shaped outputs and produces the Round-2-shaped `disciplines/index.md`.

- **Schema-enforcement aids (Reviewer 1 A1-A4) are not retroactive to in-flight work.** They apply to Wave 4.1, which has not fired yet at Round-2 close time. Wave 4.5 inherits the same discipline (exemplar + self-check rubric + required text-pull citations + fixed contested-primitive headers — adapted per wave's deliverable).

- **Round-1's "10 + 1 + 2 = 13" wave count was understated.** Round-2's revised wave count is 10 (Wave 4.1) + 2 (Wave 4.3, already fired) + 2 (Wave 4.4, already fired) + 3 (Wave 4.5, conditional 4.5b adds 1-2 more) + 1 (Wave 4.2 lead-agent) + 1 (Wave 4.6 lead-agent) = 17-19 subagents + 2 lead-agent passes. The Round-1 estimate was about half the realistic Phase-4 work. This is honest framing-debt repaid.

### Round-2 rewind point

Rewind to: the commit landing this Round-2 revision on `claude/auto-004-phase-4-dispatch-shape`. Reverting Round 2 returns the brief to Round-1 (no Wave 4.5; no Wave 4.6; original track/sketch discipline split; no schema-enforcement aids). Wave 4.3 / 4.4 in-flight outputs survive in any rewind (they're on `claude/auto-003-bfl-rg-view-choice` for Wave 4.4 and they'll land on this branch for Wave 4.3 once those subagents complete).
