# auto-005 — Phase 5 dispatch shape

**Author.** Lead agent, unattended Phase-5 dispatch session 2026-05-25.
**Status.** **Round 2 (revised after first real adversarial wave).** Round 1 returned 1 `accept-with-named-amendments` (ADR-quality auditor) + 2 `reject and counter-propose` (ADR-pipeline architect; cost/scope hawk). Round-1 decision shape (3-wave concurrent fanout in one run) is **superseded**; revised decision in [§Decision (Round 2)](#decision-round-2) defers Wave 5.3 to a subsequent run, splits Wave 5.1, swaps the exemplar, folds the 2-candidate primitives into Wave 5.1, and raises the per-ADR rubric on variant references + binding-table enumeration + self-check H1-path alignment.
**Rewind point.** This brief's commit on `claude/auto-2026-05-25-B1-auto-005-dispatch-shape`. Reverting it returns Phase-5 dispatch to "undecided"; no Wave-5.1/5.2/5.3 work has fired yet.

---

## The question

Phase 5 of the v3 synthesis produces ADRs (architecture decision records) per the [v1.2 plan revision § Phase 5](../../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md#phase-5--adrs-per-candidate-with-cross-references-on-shared-primitives-revised-in-v12). Three sub-products are owed:

- **Wave 5.1 — Common-primitive ADRs.** ~13 ADRs on primitives shared by ≥3 candidates (per [`overlap.md` § Coverage-tier summary](../primitives/overlap.md#coverage-tier-summary-phase-5-adr-priority-signal): P-01, P-02, P-05, P-06, P-08, P-14, P-22, P-07, P-19, P-28, P-29, P-23, P-12).
- **Wave 5.2 — Discipline ADRs.** ~8-12 ADRs over the 21 disciplines in [`disciplines/index.md`](../disciplines/index.md) (sub-set: those that warrant ADR-shaped capture; the rest stay as discipline write-ups).
- **Wave 5.3 — Candidate-specific ADRs.** ~16 orphan + ~13 per-variant = ~29 ADRs across the 10 candidates ([P-28 × 4, P-29 × 3, P-19 × 4, P-30 × 2 per-variant per overlap.md; orphans per candidate ownership](../primitives/overlap.md#3-findings-carried-into-wave-46)).

Total Phase-5 ADR count: **~54-62**, within the v1.2 plan envelope (50-80).

The dispatch shape determines (i) how Waves 5.1 and 5.2 are sequenced (parallel? serial?), (ii) the per-wave fanout size and per-ADR brief shape, (iii) whether Wave 5.3 splits into per-candidate sub-fanouts or fires as one ~29-subagent wave, (iv) what aggregation lead-agent steps are required between waves, and (v) where the exemplar-ADR-before-fanout discipline lands.

## Alternatives considered

### A. Per-wave parallel fanout with exemplar + ≤15-subagent wave-size limit — **lead-agent recommendation**

- **Wave 5.1 (parallel, ~13 subagents).** Lead-agent authors 1 exemplar ADR inline first (suggest P-01 sandbox — most-commodity, least-contested primitive). Dispatch remaining ~12 ADR-authoring subagents in one parallel wave with the exemplar + the [parallel-fanout-with-exemplar-and-rubric SKILL-SPEC](../../../retrospective/2026-05-25-155/SKILL-SPEC-069f0f31bf-parallel-fanout-with-exemplar-and-rubric.md) as required input.
- **Wave 5.2 (parallel, ~8-12 subagents, concurrent with 5.1).** Lead-agent authors 1 discipline-ADR exemplar (suggest cost-ceiling — most-broadly-applicable, simplest contract). Dispatch remaining 7-11 subagents concurrent with Wave 5.1. Per the [v1.2 plan revision](../../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md#phase-5--adrs-per-candidate-with-cross-references-on-shared-primitives-revised-in-v12) and the [SESSION-HANDOFF](../SESSION-HANDOFF-2026-05-25-phase-4-close.md#the-next-work--phase-5), 5.1 and 5.2 have no cross-dependencies until Wave 5.3.
- **Wave 5.3 (parallel sub-fanouts, ~29 ADRs split into per-candidate clusters).** After Waves 5.1 + 5.2 land (so cross-references are stable). Each candidate owns its orphan + per-variant ADRs; one parallel sub-fanout per candidate (10 candidates → 10 sub-fanouts of 1-5 subagents each). Lead-agent authors 1 exemplar per the most-contested candidate's first ADR (suggest BF-L's P-26 ADR — load-bearing for the brownfield methodology-degradation clause).
- **Aggregation between waves.** After Waves 5.1 and 5.2 close, lead-agent inline diff over the merged ADR set to verify cross-reference completeness + rubric compliance; before Wave 5.3 fires, lead-agent confirms common+discipline ADR IDs are stable.

**Wave-size limit: ≤15 ADRs per parallel fanout.** Wave 5.3's largest per-candidate cluster (BF-L with P-26 + P-13 + 4 RG-context ADRs) is well under 15. Wave 5.1's 13 ADRs are at the limit; Wave 5.2's ~10 are under. The 2026-05-25 overnight runs landed parallel fanouts of 10-13 subagents cleanly per [SKILL-SPEC-069f0f31bf](../../../retrospective/2026-05-25-155/SKILL-SPEC-069f0f31bf-parallel-fanout-with-exemplar-and-rubric.md); pushing past 15 would risk aggregation tractability.

**Per-ADR brief shape.** Each ADR-authoring subagent receives:

1. The primitive sketch (for Wave 5.1) or discipline write-up (Wave 5.2) or candidate's substrate-requirements (Wave 5.3) as required input.
2. The exemplar ADR for the wave.
3. The rubric: H1 `# ADR NNNN: Title` per the [`adr` skill](../../../.claude/skills/adr/SKILL.md); section order Context → Decision → Alternatives considered → Consequences → References; word budget ≤1000 words; alternatives ≥2 named options; references ≥3 (sketch / overlap entry / corpus citation); all internal links relative per [AGENTS.md § Internal document references](../../../AGENTS.md#internal-document-references); self-check rubric tool-call verification per [AGENTS-MD-e74e4811a2](../../../retrospective/2026-05-25-155/AGENTS-MD-e74e4811a2-self-check-rubric-tool-verification.md) (subagent runs `wc -w`, `ls`, `grep`).
4. Per-candidate cross-reference discipline (Wave 5.3 only): each candidate-specific ADR must `## References` the merged common+discipline ADRs from Waves 5.1+5.2 by relative link to `docs/adr/NNNN-<kebab>.md`.
5. **Alternative-considered text-pull discipline.** Per [AGENTS-MD-bf4431be57](../../../retrospective/2026-05-25-155/AGENTS-MD-bf4431be57-verbatim-text-pull-binding-rule-tables.md), when the ADR cites a binding rule table (e.g., the Phase-3.5.5 RG-primitive application table), the subagent must verbatim-pull the relevant rows into the `## Alternatives considered` or `## Context` section rather than reference-by-link only.

**Pros.**
- Maximum parallelism: Wave 5.1 + 5.2 fire concurrent ⇒ ~13 + ~10 = ~23 ADRs land in roughly one fanout's wall-clock time.
- Exemplar-before-fanout enforces shape consistency across all wave's ADRs (per [AGENTS-MD-eec503a3c2](../../../retrospective/2026-05-25-155/AGENTS-MD-eec503a3c2-exemplar-before-parallel-fanout.md)).
- ≤15-subagent wave-size limit keeps each fanout's aggregation tractable; the 2026-05-25 retros named >15 as the risk threshold.
- Per-candidate split for Wave 5.3 means no single subagent owns multiple candidates' ADRs (preserves per-candidate accountability + crisp blast-radius if any sub-fanout needs re-dispatch).
- Wave-5.3-after-5.1+5.2 sequencing keeps cross-references stable (no race conditions on ADR ID assignment).

**Cons.**
- Three sequential waves of dispatch + aggregation has wall-clock cost (~30-50 minutes of aggregation per wave at lead-agent reading speed).
- Wave 5.1+5.2 concurrent dispatch means lead-agent must hold two exemplars in head at brief-shape time. Mitigated by the rubric being uniform across both waves.
- Wave 5.3's per-candidate split = 10 sub-fanouts to brief — coordination overhead. Mitigated by each sub-fanout sharing the same per-ADR rubric.

### B. Single Wave 5.1+5.2+5.3 mega-fanout (~50 subagents at once)

Dispatch all ~54-62 ADR-authoring subagents in one parallel wave. No staging between common, discipline, and candidate-specific.

- **Pros.** Shortest wall-clock; one exemplar suffices.
- **Cons.** Far exceeds the ≤15-subagent wave-size limit from [SKILL-SPEC-069f0f31bf](../../../retrospective/2026-05-25-155/SKILL-SPEC-069f0f31bf-parallel-fanout-with-exemplar-and-rubric.md). Candidate-specific ADRs would race against common ADR ID assignment; cross-references would all break at first commit. Aggregation budget at lead-agent level becomes unmanageable (50+ subagent return digests in one head-pass). **Not chosen.**

### C. Per-candidate-first (10 candidate-owners, each authoring all their ADRs)

Each of the 10 candidates gets one subagent that authors ALL ADRs that candidate touches (common + discipline references + candidate-specific). Reverses the wave structure.

- **Pros.** Each subagent has full candidate context in one place.
- **Cons.** Common ADRs get authored 3-7 times (once per candidate that claims the primitive); cross-candidate inconsistency on the same primitive's "common" ADR is structural. The v1.2 plan explicitly rejects this in favor of one-common-ADR-per-primitive. **Not chosen.**

### D. Lead-agent inline (write all ~54-62 ADRs in one pass)

Lead agent authors every ADR sequentially without subagent dispatch.

- **Pros.** No coordination overhead; no anchoring risk from misread subagent briefs.
- **Cons.** Saturates context with ADR detail (~54-62 × ≤1000 words = ~54-62K words = ~80K tokens just for the bodies). Forecloses fresh-context per-ADR reasoning. Wall-clock cost on the order of a full overnight run. **Not chosen.**

## Decision (Round 1 — superseded by Round 2 below)

~~**Option A. Per-wave parallel fanout with exemplar + ≤15-subagent wave-size limit.**~~ Round 1 superseded — two of three reviewers `reject and counter-propose`, third reviewer `accept-with-named-amendments`. See [§Decision (Round 2)](#decision-round-2). Round-1 text preserved below for traceability per [AGENTS-MD-bb7fe2c5aa](../../../retrospective/2026-05-25-155/AGENTS-MD-bb7fe2c5aa-round-1-strikethrough-preservation.md).

### Round 1 reasoning (preserved)

~~Concretely:~~

- ~~**Wave 5.1** fires first (per-primitive ADRs, ~13 subagents, P-01 exemplar by lead agent inline).~~
- ~~**Wave 5.2** fires concurrent with 5.1 (~10 subagents, cost-ceiling exemplar by lead agent inline).~~
- ~~After Waves 5.1 + 5.2 close, lead-agent aggregation pass: verify cross-reference integrity + rubric compliance over all ~23 merged ADRs.~~
- ~~**Wave 5.3** fires after the aggregation pass: 10 per-candidate sub-fanouts, each with 1-5 ADRs to author; lead-agent authors 1 exemplar (BF-L P-26 ADR) before the first sub-fanout fires.~~
- ~~Total subagents: ~12 (Wave 5.1, excluding exemplar) + ~9 (Wave 5.2, excluding exemplar) + ~28 (Wave 5.3, excluding exemplar) = ~49 ADR-authoring subagents + ~3 lead-agent exemplars = ~52 ADRs. Plus ~6 adversarial reviewers across this brief's two rounds.~~

## Round 1 reviewer findings

Three real subagents dispatched per AGENTS.md `AGENTS-MD-d72e1a4f3c`:

### Reviewer 1 — ADR-pipeline architect (`reject and counter-propose`)

- **Objection 1: P-01 sandbox exemplar is calibration-poor for Wave 5.1.** P-01 is least-contested; subagents reading P-01 then authoring P-19 / P-28 / P-29 ADRs will not learn the right shape. The [parallel-fanout SKILL-SPEC](../../../retrospective/2026-05-25-155/SKILL-SPEC-069f0f31bf-parallel-fanout-with-exemplar-and-rubric.md) wants exemplars with *smallest cross-cutting obligations*, not globally-simplest. Recommend P-08 scenario storage (designed-system, 4-candidate footprint, runner contract + partition semantics).
- **Objection 2: BF-L P-26 Wave-5.3 exemplar inverts the heuristic.** Exemplars should have fewest contested references; P-26 is the most-contested orphan in the wave. Recommend least-contested candidate exemplar (BF-S or U-C).
- **Objection 3: Wave 5.1 at 13 has no headroom for re-dispatch.** Split into Wave 5.1a (≤10) + Wave 5.1b (≤5) with checkpoint between.

### Reviewer 2 — ADR-quality auditor (`accept-with-named-amendments`)

- **Amendment 1: Raise per-ADR reference floor to ≥4 for variant ADRs** (parent common ADR + overlap.md verdict + substrate-requirements §3 + corpus citation).
- **Amendment 2: Enumerate "binding rule tables"** subject to the verbatim-text-pull rule: Phase-3.5.5 RG-primitive application table rows; overlap.md same-vs-distinct verdict paragraphs for P-28/P-29/P-19/P-30; substrate-requirements §3 feature/envelope/policy rows.
- **Amendment 3: Add Wave-5.3-brief amendment step** publishing the ADR-ID-to-file mapping table before Wave 5.3 fires.
- **Amendment 4: Extend self-check rubric** to confirm H1 (`# ADR NNNN: Title`) matches assigned number + file basename.

### Reviewer 3 — cost/scope hawk (`reject and counter-propose`)

- **Objection 1: PR-cap risk.** Current run is at PR #165 (auto-005 brief); ~9 PRs already in flight. Full 3-wave Phase 5 plausibly consumes 10-15 more PRs leaving zero margin against the 30-PR cap when Phase-B handoff + summary + retro PRs land. Recommend two-run split: Wave 5.1 + 5.2 this run; Wave 5.3 next run.
- **Objection 2: Aggregation context budget underestimated.** ~5000 words of subagent return digests + 3 lead-agent exemplars (~3000 words) + per-wave aggregation work could consume 40-45% of context. Brief does not surface this risk.
- **Objection 3: 2-candidate primitives (P-30, P-25, P-27, P-24) should fold into Wave 5.1 NOW.** Common-ADR-with-2-candidate-cross-refs is the right shape; deferral to Wave 5.3 is a decision punt.

## Decision (Round 2)

**Option A′. Per-wave parallel fanout with exemplar, ≤10-subagent wave-size limit, split Wave 5.1, defer Wave 5.3 to next run, raised per-ADR rubric.**

Concretely:

- **Wave 5.1 split into 5.1a + 5.1b** with lead-agent aggregation checkpoint between:
  - **Wave 5.1a** (8 ADRs, commodity-tier ≥3-candidate primitives): P-01, P-02, P-05, P-06, P-08, P-14, P-22, P-07.
  - **Wave 5.1b** (9 ADRs, designed-system + 2-candidate primitives folded as common): P-19, P-28, P-29, P-23, P-12, P-25, P-27, P-24, **P-30-substrate** (the shared Temporal substrate; the two distinct per-variant state-machine ADRs for U-A re-entry and D7-U-1 survival-window stay in Wave 5.3 next run).
- **Wave 5.1 exemplar: P-08 scenario storage** (lead-agent inline before Wave 5.1a fires). Designed-system primitive, 4-candidate footprint, teaches runner-API contract + partition semantics + cross-reference shape.
- **Wave 5.2** fires concurrent with Wave 5.1a (~10 discipline ADRs). Exemplar: cost-ceiling discipline (lead-agent inline). 5.2 is concurrent with 5.1a only — not 5.1b — so the lead agent can hold two exemplars in head during the first parallel phase without overload.
- **Wave 5.3 DEFERRED to a subsequent run.** Wave 5.3's ~29 candidate-specific + per-variant ADRs (including BF-L P-26, the per-variant ADRs for P-28/P-29/P-19/P-30, U-B P-31, U-C P-32, D7-U-1 P-33+P-34, GF-C P-11/P-17/P-18, GF-M P-20/P-21, GF-S P-10/P-15, BF-S P-24-orphan, BF-L P-13, BF-M P-03/P-04/P-27-orphan) will be dispatched in a successor unattended run. The deferral allows: (a) Phase-6 architecture-spec authorship to inform per-candidate ADRs, (b) PR-cap budget preserved for this run's Wave 5.1+5.2 + handoff + summary + retro, (c) the Wave-5.3-brief amendment (ADR-ID-to-file mapping table) authored fresh with stable Wave-5.1+5.2 ADR IDs.
- **Aggregation between waves.** After Wave 5.1a closes, lead-agent ≤5-minute checkpoint: verify exemplar discipline held, no rubric drift, cross-ref skeletons in place. Before Wave 5.1b fires, the same P-08 exemplar is re-issued with a Wave-5.1b-specific note about variant complexity (P-19/P-28/P-29 carry variants — the Wave 5.1b ADR for each describes the common framework only; variants are deferred to Wave 5.3 next run).
- **Total subagents this run:** ~7 (5.1a, excluding P-08 exemplar) + ~8 (5.1b, excluding any deferred) + ~9 (5.2, excluding cost-ceiling exemplar) = ~24 ADR-authoring subagents + 2 lead-agent exemplars = ~26 ADRs this run. Plus ~6 adversarial reviewers across this brief's two rounds. Wave 5.3 next run: ~29 ADRs + reviewers.

### Revised per-ADR rubric (Round-2 amendments folded in)

Each ADR-authoring subagent receives:

1. The primitive sketch (Wave 5.1) or discipline write-up (Wave 5.2) as required input.
2. The exemplar ADR for the wave.
3. The rubric: H1 `# ADR NNNN: Title` per the [`adr` skill](../../../.claude/skills/adr/SKILL.md); section order Context → Decision → Alternatives considered → Consequences → References; word budget ≤1000 words; alternatives ≥2 named options each with a one-sentence "why-rejected" + corpus citation; **references ≥3 for Wave 5.1/5.2 baseline; ≥4 for variant ADRs in Wave 5.3 next run** (mandatory: parent common ADR + overlap.md verdict + substrate-requirements §3 + corpus citation); all internal links relative per [AGENTS.md § Internal document references](../../../AGENTS.md#internal-document-references); **self-check rubric extended** per [AGENTS-MD-e74e4811a2](../../../retrospective/2026-05-25-155/AGENTS-MD-e74e4811a2-self-check-rubric-tool-verification.md): subagent runs `wc -w` (word count), `ls` (file exists at expected path), `grep` (all §-headers present), **and `grep` the H1 to confirm it matches the assigned ADR number + file basename** (`NNNN-kebab-title.md`).
4. **Verbatim text-pull discipline** per [AGENTS-MD-bf4431be57](../../../retrospective/2026-05-25-155/AGENTS-MD-bf4431be57-verbatim-text-pull-binding-rule-tables.md). Binding rule tables the rule applies to (enumerated):
   - The [Phase-3.5.5 RG-primitive application table](../candidate-registry.md#phase-355-rule-on-load-bearing-rg-primitives-binding-user-approved-2026-05-25) rows.
   - The [overlap.md same-vs-distinct verdict paragraphs](../primitives/overlap.md#1-same-vs-distinct-verdicts-on-deferred-questions) for P-28 / P-29 / P-19 / P-30.
   - The candidate substrate-requirements summary §3 feature/envelope/policy rows in [`substrate-requirements/<id>.md`](../substrate-requirements/).
   Paraphrase of these is not acceptable; quote the row verbatim, or link to the section with a short bracketed summary if the row itself is narrative prose.
5. **Wave-5.3 cross-reference mapping** is deferred to the Wave-5.3 dispatch brief in the next run. At Wave-5.3 dispatch time, the lead agent publishes a mapping table (primitive/discipline name → assigned ADR number → relative path under `docs/adr/`) so per-variant ADR subagents can emit correct cross-references. Not needed this run.

## Round-2 reasoning

Three drivers select Option A′ over Round 1's Option A:

1. **PR-cap safety.** Two-run split (this run: 5.1a + 5.1b + 5.2; next run: 5.3) leaves ~10-12 PRs margin against the 30-PR cap. Round-1 plan put margin at risk.
2. **Exemplar calibration.** P-08 scenario storage exemplar teaches subagents the actual cognitive load of Wave 5.1 ADRs (designed-system contract; partition semantics; runner-API) — better than P-01's commodity-floor minimalism.
3. **Reviewer-2 amendments raise floor quality.** Variant-ADR reference floor at ≥4 + enumerated binding-rule tables + H1-path self-check + Wave-5.3 mapping table are all positive-sum quality improvements at near-zero cost.

The 2-candidate primitives fold-in (P-30 substrate, P-25, P-27, P-24) settles a deferred Round-1 question early — they belong as common ADRs in Wave 5.1b given their shared-substrate nature.

## Round-2 if-user-overrides rewind point

This brief's commit. Revert to undo the Round-2 framing; Wave 5.1a has not fired (this brief precedes the wave dispatch).

## Honest acknowledgements

Per [AGENTS-MD-ffe35aa500](../../../retrospective/2026-05-25-155/AGENTS-MD-ffe35aa500-honest-acknowledgements-pre-round-2-firing.md): no Wave-5.x ADR-authoring subagent has fired pre-Round-2; the dispatch brief precedes the dispatch. The Round-1 reviewers' findings are folded in honestly (no Round-1 amendments suppressed or paraphrased into agreement with the lead agent's prior).

## Open questions for the Round-2 adversarial reviewers to challenge

1. Is splitting Wave 5.1 into 5.1a + 5.1b *better* than running Wave 5.1 as one 13-subagent wave? Or does the extra checkpoint add coordination cost without proportional safety?
2. Is folding the 4 two-candidate primitives into Wave 5.1b right? P-30-substrate fold is contested by overlap.md noting P-30's "DISTINCT primitives" verdict — does the *substrate* fold survive that distinction?
3. Is deferring Wave 5.3 to a subsequent run defensible? Or does the deferral risk Phase-5 staying half-finished if the next run's dispatch prompt drifts?
4. Is the P-08 scenario-storage exemplar choice now over-fitted to Wave 5.1a's commodity-shape needs? Could it MISDIRECT Wave 5.1b's designed-system subagents (P-19 / P-28 / P-29)?
5. Is the "≥4 for variant ADRs" reference floor enforceable? The variant ADRs are all in Wave 5.3 next run — does the rubric need amending in the Wave-5.3 dispatch brief, or is having it codified here sufficient?

## Reasoning

Three drivers select Option A:

1. **The 30 substrate primitives map cleanly to a 3-wave dispatch.** ~13 shared (Wave 5.1) + ~16 orphan + ~13 per-variant (Wave 5.3) leaves 21 disciplines (Wave 5.2 subset). No primitive sits in two waves; no ADR ID is contested between waves.

2. **Wave 5.1 and 5.2 are formally independent** per the v1.2 plan: common-primitive ADRs do not cite discipline ADRs and vice versa. Running them concurrent saves wall-clock with zero correctness risk.

3. **Wave 5.3 cross-references the merged Wave-5.1+5.2 ADR set** by relative-path link. If 5.3 fires concurrent with 5.1+5.2, the references break (ADR IDs not yet assigned). Sequencing 5.3 after the aggregation pass is the conservative choice.

## Downstream impact

- **Phase 6** (architecture spec authorship per candidate) consumes the merged ADR set as binding inputs. Each candidate's Phase-6 spec carries a `## References` to its common+discipline+candidate-specific ADRs. The dispatch shape here determines that those refs are stable + cross-consistent before Phase 6 fires.
- **Phase 8** (lean-eval briefs per candidate) inherits the per-variant ADRs from Wave 5.3 (P-19 four-variant correlation, P-28 envelope-collision, P-30 timer-vs-event reliability per [overlap.md § Phase-8 lean-eval candidates surfaced or strengthened](../primitives/overlap.md#3-findings-carried-into-wave-46)). Wave 5.3's per-candidate split keeps the lean-eval candidate-pointers clean.

## Round-1 if-user-overrides rewind point

This brief's commit. Revert to undo the Round-1 framing; Wave 5.1 has not fired (this brief precedes the wave-1 dispatch).

## Open questions for the adversarial reviewers to challenge

1. **Wave-size limit.** Is ≤15 too generous? Too conservative? Should Wave 5.1 (at 13) be split to leave headroom? Should Wave 5.3's largest per-candidate cluster face an additional sub-split?
2. **Concurrency of 5.1 + 5.2.** Is there a hidden cross-dependency (e.g., the cost-ceiling discipline ADR depends on the P-02 cost-ceilings common ADR?) that the brief's "formally independent" claim misses?
3. **Exemplar choice.** P-01 sandbox is least-contested but also potentially LEAST representative of the harder ADRs in Wave 5.1 (P-19 classifier framework, P-28 typed-object store). Would a mid-difficulty exemplar (e.g., P-08 scenario storage with runner contract) better calibrate subagent shape across the wave?
4. **2-candidate ADRs.** [`overlap.md`](../primitives/overlap.md#coverage-tier-summary-phase-5-adr-priority-signal) flags 4 primitives shared by 2 candidates (P-30, P-25, P-27, P-24) as "lead-agent call at Phase 5 dispatch on whether to draft as common or per-candidate." This brief implicitly defers them to Wave 5.3 (orphans). Is that right? Or should they fold into Wave 5.1 as common with 2-candidate cross-refs?
5. **Per-candidate cross-reference discipline in Wave 5.3.** Is requiring cross-refs to relative `docs/adr/NNNN-<kebab>.md` paths the right convention? Or should refs be by ADR ID with a separate lookup table?

(Round-1 reviewers will challenge any/all of these + anything else they find.)

---

*(Round 2 above. Awaiting Round-2 adversarial wave: ≥3 real subagents with fresh angles. Round-3 will only fire if Round-2 reviewers converge on a material change.)*
