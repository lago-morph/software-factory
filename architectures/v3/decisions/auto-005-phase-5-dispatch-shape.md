# auto-005 — Phase 5 dispatch shape

**Author.** Lead agent, unattended Phase-5 dispatch session 2026-05-25.
**Status.** Round 1 (initial brief; awaiting first adversarial wave). Per [SKILL-SPEC-34dd1d0274 decision-brief adversarial-review lifecycle](../../../retrospective/2026-05-25-155/SKILL-SPEC-34dd1d0274-decision-brief-adversarial-review-lifecycle.md), two rounds of ≥3 real adversarial subagents follow before a final decision is locked.
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

## Decision (Round 1)

**Option A. Per-wave parallel fanout with exemplar + ≤15-subagent wave-size limit.**

Concretely:

- **Wave 5.1** fires first (per-primitive ADRs, ~13 subagents, P-01 exemplar by lead agent inline).
- **Wave 5.2** fires concurrent with 5.1 (~10 subagents, cost-ceiling exemplar by lead agent inline).
- After Waves 5.1 + 5.2 close, lead-agent aggregation pass: verify cross-reference integrity + rubric compliance over all ~23 merged ADRs.
- **Wave 5.3** fires after the aggregation pass: 10 per-candidate sub-fanouts, each with 1-5 ADRs to author; lead-agent authors 1 exemplar (BF-L P-26 ADR) before the first sub-fanout fires.
- Total subagents: ~12 (Wave 5.1, excluding exemplar) + ~9 (Wave 5.2, excluding exemplar) + ~28 (Wave 5.3, excluding exemplar) = ~49 ADR-authoring subagents + ~3 lead-agent exemplars = ~52 ADRs. Plus ~6 adversarial reviewers across this brief's two rounds.

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

*(Round 2 section will be appended after Round-1 adversarial findings land. Per [AGENTS-MD-bb7fe2c5aa](../../../retrospective/2026-05-25-155/AGENTS-MD-bb7fe2c5aa-round-1-strikethrough-preservation.md), the Round-1 decision will be marked `superseded by Round 2` with strikethrough on any flipped option, preserving the text for traceability. Per [AGENTS-MD-ffe35aa500](../../../retrospective/2026-05-25-155/AGENTS-MD-ffe35aa500-honest-acknowledgements-pre-round-2-firing.md), no Phase-5 ADR-authoring subagent has fired pre-Round-2; the brief is the contract.)*
