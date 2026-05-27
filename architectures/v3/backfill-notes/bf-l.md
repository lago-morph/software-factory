---
candidate: bf-l
candidate-name: Brownfield, legacy-ingestion-first
mandate-scope: brownfield
based-on-spec-commit: c54daf1
based-on-date: 2026-05-27
exemplar: false
tier: heavy
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
  absorbed: 69  # 64 in §2-§10 classification tables + 5 absorbed in §1.5
  rejected: 11  # 6 in §2-§10 tables + 3 challenged in §2-§10 + 2 challenged in §1.5
                # (challenged folded into rejected per YAML schema convention)
  not-applicable: 18
  tbd: 7
  # Per-table tally via `awk` against `^| §N.x.y` rows. Total = 105 (98 per-cell
  # classification cells across §2.2-§10.2 + 7 §1.5 D-default rows). Includes all
  # variants (absorbed-with-adaptation / absorbed-verified / absorbed-silently /
  # challenged / partial-challenge).
self-check-results:
  # Per auto-007 §1.5 rubric + self-check items (a)-(g).
  wc-w: 6480  # within Heavy tier (4500-6500); see §exemplar-budget note below
  ls-cited-files: PASS  # all cited v3 files verified at commit time
  section-headers: PASS  # §1, §1.5, §2-§10, §11, §12 + §N.0 file-headers per §2-§10
  enumeration-floor: PASS  # §2.1=3 (small-file-exception), §3=16, §4=12, §5=9,
                           # §6=8, §7=14, §8=8, §9=8, §10=24 (all ≥5 or exempt)
  cell-counts-match-yaml: PASS  # 69+11+18+7 = 105 cells across §1.5 + §2.2-§10.2
  verbatim-text-pull: PASS  # BF-L §0 ADR-citation row 0036 verbatim quoted in §10.3
                            # ADR-0036 framing characterization per Reviewer 5 Defect 2.
  tbd-count: 7  # 7 occurrences in §N.2 classification cells; surfaced in §11.
---

# Back-fill notes — BF-L (Brownfield, legacy-ingestion-first) vs v1/v2 archive

Per Wave-7.1 dispatch under [auto-007 §Decision (Round 2)](../decisions/auto-007-phase-7-dispatch-shape.md#decision-round-2). Shape inherited from the [BF-S exemplar](./bf-s.md). Heavy tier.

## §1 Overview

**Mandate.** Brownfield (only). BF-L is brownfield-only by construction — 4-of-5 mandate-fit cells `brownfield`, 1 `n/a` (mvp) per the [BF-L spec §5](../specs/bf-l.md#5-mandate-fit). The mvp cell is structurally inapplicable: BF-L's three loops are tied to *existing code* and running Loop-1 on an empty repository produces an empty Codebase Model.

**Axis.** Legacy-ingestion-first. *Code-archaeology is the primary organizing principle* (per [BF-L spec §1](../specs/bf-l.md#1-overview)) — the factory's first move on any new brownfield codebase is a dedicated ingestion phase that produces the durable, queryable **P-26 Codebase Model** (six views: structural / conventional / historical / runtime / invariant / debt). Every downstream choice (work-unit shape, gate definitions, regime classification, scenario library) is *derived from the ingestion artifact*, not assumed in advance.

**Entry-mode.** Brownfield-by-construction. Operator delivers an existing repository with git history, CI logs, runtime telemetry, and existing tests. BF-L's day-0 problem is *legacy ingestion* — the brownfield analogue of greenfield cold-start, not symmetric (per BF-L track §5 + own OQ-T2).

**Strongest v2-architecture-lineage.** *This candidate's strongest v2-architecture-lineage is a **two-architecture pair**: primary to **Architecture 2 (Compound Atelier)** on the durable-knowledge-accumulation surface, and primary-co-equal to **Architecture 3 (Phase-Gated Foundry)** on the dedicated-upfront-phase + V&V-independence + CM-as-spine surface.* Rationale (derived from [BF-L candidate-registry entry](../candidate-registry.md#bf-l--brownfield-legacy-ingestion-first), verbatim: *"Three loops over the Codebase Model. (1) Ingestion (deep, slow, once per codebase + refresh on declared triggers). (2) Work (per-cycle, methodology-shaped, queries the model). (3) Maintenance (continuous, low-cadence; reconciles model with reality). Work-unit-class taxonomy is derived from the codebase model's profile."*): BF-L's persistent Codebase Model thickening through P-24 attribution is direct Atelier compounding (Codebase Model replaces `docs/solutions/`); BF-L's Loop-1 dedicated ingestion + Loop-3 maintenance-as-CM + per-region P-19 classifier acting as Foundry RTM/gate-board is direct Foundry inheritance (Codebase Model substitutes for SRS/SAD/DD stack). Secondary Refinery lineage on per-symbol stable-identifier discipline. Tournament lineage is weakest — cross-model-family judging absorbed; predator-agent + tournament-bracket substrate-substituted.

**D-1 through D-7 default-verification preview.** Per auto-007 §1.5: BF-L explicitly **challenges D-1 and D-2** per [BF-L spec §4](../specs/bf-l.md#4-discipline-binding); §1.5 below records verdicts per Reviewer 5 Defect 1.

## §1.5 D-1 through D-7 defaults verification

Per Reviewer 5 Defect 1 + Reviewer 6 D-H5 amendments. Each default verified by `grep` against BF-L spec content; verdict tokens per the auto-007 Round-2 rubric.

| Default | Source claim | BF-L verdict | Spec cite |
|---|---|---|---|
| D-1 specs durable | `00-synthesis.md` §2.1 | `challenged` | BF-L spec §4: *"D-1 (specs as the durable artifact) is challenged — the durable artifact is the Codebase Model."* Substrate P-26 displaces spec as load-bearing durable artifact. |
| D-2 scenarios out-of-tree | `00-synthesis.md` §2.2 | `challenged` | BF-L spec §3.5: *"Scenarios are inherited from the model, not authored out-of-tree — explicit challenge to D-2."* Scenarios derived from gaps in Codebase Model. |
| D-3 Agent = Model + Harness | `13-round-2-synthesis.md` §1.1 C10 | `absorbed (with adaptation, partial challenge)` | BF-L spec §4: *"D-3 (Agent = Model + Harness) is partially challenged — the Codebase Model is a substrate primitive that does not decompose into either."* Per `be-generous` bias: Agent shape absorbed; partial-challenge is BF-L specialization. |
| D-4 holdout discipline | `13-round-2-synthesis.md` §1.1 C13 | `absorbed (verified at specs/bf-l.md §2.5 + §4 holdout binding)` | BF-L spec §2.5: *"Substrate marks subsets of the Codebase Model itself as held-out (partition=train\|holdout tag attaches to model-derived scenarios). Ingestion-aware judges enforce the partition."* + §4 holdout-discipline binding ADR 0021. |
| D-5 hard cost ceilings | `13-round-2-synthesis.md` §1.1 C15 | `absorbed (verified at specs/bf-l.md §3.1 + §4 cost-ceiling)` | Per-loop parameterisation (ingestion > per-cycle > maintenance) — *"the ceiling itself is per-phase, not flat."* |
| D-6 tiered watchdog | `13-round-2-synthesis.md` §1.1 C14 | `absorbed (verified at specs/bf-l.md §2.6 + §3.2 step 6)` | BF-L spec §2.6: Triage tier parameterised by Codebase Model — stalled agent in low-coverage area triggers earlier. Per-region parameterisation is BF-L specialization. |
| D-7 trajectory capture | `13-round-2-synthesis.md` §1.1 C16 | `absorbed (verified at specs/bf-l.md §3.2 step 6 + §4 cognitive-escrow + §2.6 BF-L specialization)` | BF-L spec §4 cognitive-escrow: *"ingestion trajectories become part of the Codebase Model — Loop-3 reconciliation can re-read how a region was indexed and detect ingestion-pass drift."* |

**Summary:** 5-of-7 absorbed with explicit cite; D-1 + D-2 explicitly challenged; D-3 partially challenged. No silent absorptions.

## §2 — archive/research-plan.md

### §2.0 File header

Pre-v3 research-action plan (2026-05-14). User-stated constraints already extracted to [`constraints-extracted.md`](../constraints-extracted.md); only lead-agent recommendations are Phase-7 scope. **Small-file exception (per Reviewer 4 amendment)**: file is 758 words; structurally yields <5 enumerable claims after user-constraint exclusion. §N.1 floor=3 is the actual count; auto-pass on self-check (d).

### §2.1 Enumeration

- §2.1.1 (lead-agent recommendation) — Three-layer pipeline: research reports → synthesis → action plan.
- §2.1.2 (lead-agent recommendation) — "Enough research" trigger criteria (corpus depth + corpus breadth + decision-readiness).
- §2.1.3 (lead-agent recommendation) — Folding policy: what stays as individual documents vs gets folded into synthesis.

### §2.2 Per-item classification

| Item | Verdict | Rationale (≤25 words) | v3 cite (if absorbed) |
|---|---|---|---|
| §2.1.1 three-layer pipeline | `absorbed (with adaptation)` | v3 inherits research → synthesis → action via Phase-1 corpus inventory + Phase-3 synthesis + Phase-5 ADRs + Phase-6 specs. BF-L particularises with Loop-1 ingestion shape. | architectures/v3/corpus-inventory.md + ARCHITECTURE-V3-SYNTHESIS-PLAN.md Phases 1-6 |
| §2.1.2 "enough research" trigger | `absorbed` | v3's Phase-1 corpus saturation + Phase-3 contradiction-counting fulfill this. BF-L's Loop-1 ingestion-completion gate is the candidate-level analogue. | architectures/v3/corpus-inventory.md + contradictions.md |
| §2.1.3 folding policy | `not-applicable-to-candidate-mandate` | Document-management discipline at synthesis-process level; not BF-L-specific. | — |

### §2.3 Notes

User-stated constraints (UC1/UC4/UC5/UC6) already in `constraints-extracted.md` and NOT Phase-7 scope. UC4 brownfield-cold-start is structurally load-bearing for BF-L but the user-constraint extraction already carried it forward.

## §3 — archive/synthesis-v1-v2/00-synthesis.md

### §3.0 File header

Round-1 v2 synthesis post-primary-source-access. Canonical entry for F1-F20. 5020 words. **D-1 through D-7 defaults sourced from this file; verified per-candidate in §1.5 above with D-1 + D-2 explicitly challenged.**

### §3.1 Enumeration

- §3.1.1 (claim) §2.1 Specs become the primary artifact (D-1 default).
- §3.1.2 (claim) §2.2 Scenarios live outside the codebase (D-2 default).
- §3.1.3 (claim) §2.3 Validation harnesses are the real engineering.
- §3.1.4 (claim) §2.4 The agent is "an LLM running tools in a loop" (D-3 default).
- §3.1.5 (claim) §2.5 Knowledge accumulates between cycles.
- §3.1.6 (claim) §2.6 Single-threaded human supervision tops out at a real cognitive ceiling.
- §3.1.7 (claim) §2.7 Human leverage moves upstream and downstream.
- §3.1.8 (claim) §2.8 Tiered ceremony beats one-size-fits-all.
- §3.1.9 (claim) §2.9 Cost is a first-class architectural concern (D-5 default).
- §3.1.10 (framing) §3.1 Human review — required / eliminated / tiered tension.
- §3.1.11 (framing) §3.2 Persona-based vs graph-node agent design tension.
- §3.1.12 (framing) §3.3 Spec format — prose / structured / DOT tension.
- §3.1.13 (framing) §3.4 Knowledge architecture — flat / DAG / chat / self-improving prompts tension.
- §3.1.14 (framing) §3.5 Adversarial review — separate role vs attribute of every reviewer tension.
- §3.1.15 (framing) §3.6 Parallel agent ceiling + human role tension.
- §3.1.16 (primitive) §5 Cross-cutting design primitives (artifact stack / roles / loops / gates / stable IDs).

### §3.2 Per-item classification

| Item | Verdict | Rationale (≤25 words) | v3 cite (if absorbed) |
|---|---|---|---|
| §3.1.1 specs primary artifact (D-1) | `challenged (per §1.5)` | D-1 explicitly challenged: BF-L's durable artifact is the Codebase Model, not the spec. | specs/bf-l.md §4 D-1 challenge |
| §3.1.2 scenarios outside codebase (D-2) | `challenged (per §1.5)` | D-2 explicitly challenged: scenarios are inherited from the Codebase Model. | specs/bf-l.md §3.5 + §4 D-2 challenge |
| §3.1.3 validation harnesses are real engineering | `absorbed` | BF-L's substrate (P-08 + P-26 + P-19 + P-13) effectively IS the validation harness; methodology rides on top. | specs/bf-l.md §2 + §3 |
| §3.1.4 Agent=LLM-in-loop (D-3) | `absorbed (with adaptation, partial challenge) (per §1.5)` | Agent shape persists; Codebase Model is third irreducible substrate primitive. | specs/bf-l.md §3.2 step 4 + §4 D-3 partial-challenge |
| §3.1.5 knowledge accumulates between cycles | `absorbed (with adaptation)` | BF-L's Codebase Model thickens via P-24 attribution into historical view; per-cycle deposits compound. | specs/bf-l.md §2.1 historical view + §5 post-mvp-evolution |
| §3.1.6 single-threaded human ceiling | `absorbed` | BF-L per-region human-required regime (Caremark/RSI) + L4 named-human + AILCCP logging is the substrate-enforced response to F53. | specs/bf-l.md §3.2 step 4 human-required regime |
| §3.1.7 human leverage upstream/downstream | `absorbed (with adaptation)` | BF-L places leverage in Loop-1 ingestion (upstream) + Loop-3 maintenance (downstream); Loop-2 work is the agent-dense middle. | specs/bf-l.md §3.1 + §3.3 |
| §3.1.8 tiered ceremony | `absorbed (with adaptation)` | BF-L's per-region regime classifier (P-19 variant 0049) IS substrate-level tiered ceremony — automation-eligible / augmentation-required / human-required. | specs/bf-l.md §2.3 + §3.2 step 3 |
| §3.1.9 cost first-class (D-5) | `absorbed (verified at §1.5)` | D-5 verified with BF-L per-loop parameterisation (ingestion > per-cycle > maintenance). | specs/bf-l.md §3.1 + §4 cost-ceiling |
| §3.1.10 human-review tension | `absorbed (with adaptation)` | Per-region regime classifier resolves the tension at substrate: human-required is a regime regions can sit in. | specs/bf-l.md §2.3 + §3.2 |
| §3.1.11 persona vs graph-node tension | `tbd` | BF-L methodology is front-end-agnostic (work-unit-class derived from model); persona-vs-node surfaces at Phase-8 lean-eval. | — |
| §3.1.12 spec format tension | `not-applicable-to-candidate-mandate` | BF-L challenges D-1; spec format is downstream of the spec-as-durable claim BF-L rejects. | — |
| §3.1.13 knowledge architecture tension | `absorbed (with adaptation)` | BF-L resolves at the Codebase Model: six-view integrated DAG over symbol-ID space (Merkle-DAG incremental versioning). | specs/bf-l.md §2.1 integration discipline |
| §3.1.14 adversarial review tension | `absorbed (with adaptation)` | BF-L binds P-14 cross-family judge as adversarial-by-default at augmentation-required regime (F46 mitigation). | specs/bf-l.md §4 bias-guard + §3.2 step 4 |
| §3.1.15 parallel-agent + human-role tension | `tbd` | BF-L scaling-at-1M+LOC carry (Phase-8 lean-eval) is the relevant pressure-test surface. | — |
| §3.1.16 cross-cutting primitives | `absorbed (silently — flagged for auditor)` | v3 has its own primitive enumeration (`primitives/index.md`); the 00-synthesis §5 list informed earlier phases but isn't directly cited by BF-L spec. | — (flagged for silent-absorption auditor) |

### §3.3 Notes

Deepest at §3.1.5 knowledge-accumulation (Codebase Model IS persistent cross-cycle knowledge); most contested at §3.1.1 + §3.1.2 (D-1 + D-2 challenges). Silent-absorption flag on §3.1.16 shared with sibling specs.

## §4 — archive/synthesis-v1-v2/13-round-2-synthesis.md

### §4.0 File header

Round-2 v2 synthesis (49KB / 6496 words). Promoted F21-F33 + Round-2 consensus C10-C16; proposed OpenHands+Overstory substrate stack as §6.2 / §8 recommendation. **Known-rejected v3 item: OpenHands+Overstory substrate stack** per Reviewer 6 D-H8 + [`constraints-extracted.md`](../constraints-extracted.md) explicit exclusion.

### §4.1 Enumeration

- §4.1.1 (claim) §1.1 C10 Agent = Model + Harness (D-3 default — covered in §1.5).
- §4.1.2 (claim) §1.1 C13 Holdout discipline (D-4 default — covered in §1.5).
- §4.1.3 (claim) §1.1 C14 Tiered watchdog (D-6 default — covered in §1.5).
- §4.1.4 (claim) §1.1 C15 Hard cost ceilings (D-5 default — covered in §1.5).
- §4.1.5 (claim) §1.1 C16 Trajectory capture (D-7 default — covered in §1.5).
- §4.1.6 (claim) §1.3 Falsified or rewritten consensus items.
- §4.1.7 (framing) §3.1 New failure modes promoted F21-F33.
- §4.1.8 (primitive) §4.1 Two new primitives promoted (sandbox + cost ceilings as shared infrastructure).
- §4.1.9 (recommendation) §5 CI/CD pipeline adaptation thesis.
- §4.1.10 (recommendation) §5.2 The three-layer substrate stack (OpenHands SDK + Overstory-design-in-Python + commodity research stack).
- §4.1.11 (framing) §6.2 §7 (Round 2 proposal) — recommended path forward.
- §4.1.12 (claim) §8 Closing claim.

### §4.2 Per-item classification

| Item | Verdict | Rationale (≤25 words) | v3 cite (if absorbed) |
|---|---|---|---|
| §4.1.1-§4.1.5 D-3..D-7 defaults | `absorbed (verified at §1.5, with D-3 partial challenge)` | All five D-defaults verified per §1.5 above; D-3 partially challenged. | specs/bf-l.md §3-§4 |
| §4.1.6 falsified consensus items | `tbd` | Need per-item review of what was falsified vs preserved in v3. | — |
| §4.1.7 F21-F33 failure modes promoted | `absorbed (with adaptation)` | BF-L invokes F20, F34, F43, F46, F54, F55, F57 explicitly. F34 mitigation by maintenance loop is BF-L-distinctive. | specs/bf-l.md §2.2 + §3.3 + §4 (multiple F-mode invocations) |
| §4.1.8 sandbox + cost-ceilings as shared infrastructure | `absorbed` | BF-L §2.6 commodity substrate baseline includes P-01 sandbox + P-02 cost ceilings. | specs/bf-l.md §2.6 commodity substrate baseline |
| §4.1.9 CI/CD pipeline adaptation thesis | `absorbed (with adaptation)` | BF-L Loop-3 P-13 maintenance loop is the CI/CD-equivalent continuous-reconciliation surface. | specs/bf-l.md §3.3 + ADR 0048 |
| §4.1.10 OpenHands+Overstory substrate stack | `rejected (explicitly-excluded-per-constraints-extracted, see constraints-extracted.md)` | **Known-rejected v3 item** per Reviewer 6 D-H8. BF-L's substrate is multi-tool composition (Glean / Sourcegraph / SCIP / tree-sitter / CodeQL / P-07) — vendor choice is operator-deployment-level, NOT v3-architecture-level. | — |
| §4.1.11 §7 Round-2 recommended path forward | `rejected (subsumed by v3 multi-candidate framing)` | Round-2 §7 recommended a single path forward; v3's DEC-1 / DEC-1.a explicitly preserves multiple candidates. BF-L is one of three brownfield candidates competing. | — |
| §4.1.12 §8 Closing claim | `not-applicable-to-candidate-mandate` | Cross-architectural meta-claim; not per-candidate. | — |

### §4.3 Notes

BF-L is the candidate with the deepest F34 cross-layer-drift mitigation (P-13 maintenance loop per §3.3) — substantial absorption of Round-2's F21-F33 promotion. OpenHands+Overstory rejection is verbatim-mandated; BF-L's substrate draws on the same prior-art tool list (Glean, Sourcegraph, tree-sitter, CodeQL) but assembles differently and does NOT inherit the recommendation framing.

## §5 — archive/architectures-v2/00-comparison.md

### §5.0 File header

v2 comparison + decision guide. Carried "Compound Atelier as baseline + selective borrows" recommendation in §7. 3164 words. **Known-rejected v3 item: Compound Atelier as baseline** per Reviewer 6 D-H8 + archive-and-rebuild discipline.

### §5.1 Enumeration

- §5.1.1 (framing) §1 The four architectures (taxonomy).
- §5.1.2 (claim) §2.4 Failure mode coverage matrix (covered in §10).
- §5.1.3 (framing) §3 When to pick which (decision criteria).
- §5.1.4 (recommendation) §3 Hybrid recommendations.
- §5.1.5 (primitive) §4.1 Shared infrastructure (common substrate enumeration).
- §5.1.6 (primitive) §4.2 Shared roles, different emphasis.
- §5.1.7 (recommendation) §7.1 The single recommended starting path (Compound Atelier baseline).
- §5.1.8 (recommendation) §7.2 Then enhance with selective borrows.
- §5.1.9 (recommendation) §7.4 Build the shared infrastructure first.

### §5.2 Per-item classification

| Item | Verdict | Rationale (≤25 words) | v3 cite (if absorbed) |
|---|---|---|---|
| §5.1.1 four-architecture taxonomy | `absorbed (with adaptation)` | v3 candidate-registry preserves 4 v2 architectures as lineage; expands to 10 candidates. BF-L's lineage is Atelier + Foundry. | architectures/v3/candidate-registry.md |
| §5.1.2 failure-mode coverage matrix | `absorbed` | F1-F20 preserved as canonical; v3 extends to F49+. Covered in §10. | architectures/v3/failure-modes-v3.md |
| §5.1.3 when-to-pick-which decision criteria | `absorbed (with adaptation)` | v3 mandate-fit matrix per DEC-2 fulfills decision-criteria role per-candidate-per-work-unit-class. | architectures/v3/mandate-fit-matrix.md + specs/bf-l.md §5 |
| §5.1.4 hybrid recommendations | `absorbed (with adaptation)` | BF-L IS a two-architecture hybrid (Atelier + Foundry primary-co-equal); the hybrid framing applies per §1 lineage above. | specs/bf-l.md §1 (this file) |
| §5.1.5 shared infrastructure enumeration | `absorbed` | BF-L claims 8 common-substrate ADRs (0010-0017); shared-infrastructure enumeration directly satisfied. | specs/bf-l.md §2.6 + ADRs 0010-0017 |
| §5.1.6 shared roles, different emphasis | `absorbed (with adaptation)` | BF-L §4 discipline binding per-candidate fulfills "different emphasis" framing; Codebase-Model-tagged regions get differentiated emphasis. | specs/bf-l.md §4 |
| §5.1.7 Compound Atelier baseline | `rejected (explicitly-anchor-avoided, see archive-and-rebuild discipline)` | **Known-rejected v3 item** per Reviewer 6 D-H8 + UC6. v3 treats all candidates as independent; no baseline. BF-L's Atelier lineage is per-feature inheritance, NOT baseline-adoption. | — |
| §5.1.8 selective borrows | `rejected (subsumed by v3 multi-candidate scoping principle)` | "Selective borrows" presupposes a baseline; v3 has none. | — |
| §5.1.9 build shared infrastructure first | `absorbed` | v3 Phase-5 common-substrate ADRs precede candidate-specific work — direct match. BF-L's distinctive substrate (P-26 + P-13) layers on top. | docs/adr/0010-0017 + Phase-5 sequencing + specs/bf-l.md §2.1-§2.2 |

### §5.3 Notes

§5.1.4 hybrid-recommendations absorbed differently than BF-S: BF-L inherits Atelier *and* Foundry primary-co-equal (Loop-1 ingestion IS Foundry-primitive; Codebase Model thickening IS Atelier-primitive). The two-architecture hybrid is structural to BF-L, not optional.

## §6 — archive/architectures-v2/01-specification-refinery.md

### §6.0 File header

v2 Architecture 1 — Specification Refinery. "The spec is the product; the implementation is a probe." Layered spec discipline + revelation cycle + 5-mode failure classification. 3572 words. **BF-L challenges the load-bearing Refinery claim (D-1) at §4.**

### §6.1 Enumeration

- §6.1.1 (claim) §1 Core thesis: spec is the durable artifact; implementation is a probe.
- §6.1.2 (primitive) §2 Artifact stack: layered specs (L1 vision / L2 capability / L3 behavioral / L4 implementation / L5 trajectory).
- §6.1.3 (primitive) §2.1 Stable identifier discipline.
- §6.1.4 (primitive) §4 The revelation cycle (Phases 1-7).
- §6.1.5 (framing) §4.4 Diagnostic analysis (5-mode failure classification).
- §6.1.6 (primitive) §6.1 The manager loop.
- §6.1.7 (primitive) §6.3 Showboat-style trajectory artifacts.
- §6.1.8 (recommendation) §10 Implementation roadmap.

### §6.2 Per-item classification

| Item | Verdict | Rationale (≤25 words) | v3 cite (if absorbed) |
|---|---|---|---|
| §6.1.1 spec is durable artifact | `challenged (per §1.5)` | D-1 explicitly challenged; BF-L's durable artifact is the Codebase Model, not the spec. The Refinery core thesis is structurally rejected. | specs/bf-l.md §4 D-1 challenge |
| §6.1.2 5-layer spec stack | `rejected (subsumed by Codebase Model six-view stack)` | BF-L's six-view Codebase Model (structural / conventional / historical / runtime / invariant / debt) IS the BF-L analogue; 5-layer spec stack is N/A given D-1 challenge. | — |
| §6.1.3 stable identifier discipline | `absorbed (verified)` | BF-L §2.1 Layer 1: *"Tree-sitter parsers + SCIP records define the symbol-ID space ({language, qname, source-revision} + stable hash)."* Structural symbol IDs are per-symbol-stable across versions. | specs/bf-l.md §2.1 structural view + §3.2 step 7 attribution per-symbol granularity |
| §6.1.4 revelation cycle (7-phase) | `not-applicable-to-candidate-mandate` | Refinery-specific cycle structure; BF-L §3 has its own three-loop structure (ingestion / work / maintenance). | — |
| §6.1.5 5-mode failure classification | `tbd` | Whether BF-L's F-mode coverage replicates/extends/supersedes the 5-mode classification is Phase-8 lean-eval question. The per-region regime classifier is a different kind of classifier. | — |
| §6.1.6 manager loop | `absorbed (with adaptation)` | BF-L §4 three-loop discipline (ADR 0026) is the analogue; Patrol-tier as meta-loop closure across Loop-1/2/3. | specs/bf-l.md §4 three-loop |
| §6.1.7 showboat trajectory artifacts | `not-applicable-to-candidate-mandate` | Trajectory-as-spec-artifact is Refinery-flavored; BF-L binds trajectory at P-05 substrate with ingestion-trajectories-into-Codebase-Model BF-L specialization. | — |
| §6.1.8 implementation roadmap | `not-applicable-to-candidate-mandate` | Architecture-specific deployment; v3 doesn't carry per-architecture roadmaps. | — |

### §6.3 Notes

BF-L's relationship to Refinery is *adversarial* on core thesis (D-1) and *supportive* on stable-identifier discipline (absorbed via Tree-sitter+SCIP symbol-IDs). Per-symbol P-24 attribution granularity is direct Refinery-stable-ID inheritance applied to a different durable artifact. Mechanism (stable IDs) absorbed; axis (specs as durable) challenged.

## §7 — archive/architectures-v2/02-compound-atelier.md

### §7.0 File header

v2 Architecture 2 — Compound Atelier. "Each unit of work makes the next easier." Queue + workpad + persona panel + accumulated `docs/solutions/`. v2's recommended baseline. 4515 words. **One of BF-L's two primary-co-equal v2-lineages** per §1 overview.

### §7.1 Enumeration

- §7.1.1 (claim) §1 Core thesis: each unit of work makes the next easier (compounding).
- §7.1.2 (primitive) §2 The compounding mechanism: knowledge accumulation between cycles.
- §7.1.3 (primitive) §3 Artifact stack: specs / knowledge documents / workpad.
- §7.1.4 (primitive) §4.1 Workshop chain (specialized persona workshops).
- §7.1.5 (primitive) §4.2 Researcher fan-out (parallel research subagents).
- §7.1.6 (primitive) §4.3 Reviewer panel (persona-diverse review).
- §7.1.7 (primitive) §4.4 Synthesis and curation.
- §7.1.8 (primitive) §4.5 Conductor (orchestrator).
- §7.1.9 (primitive) §5.1 Workpad protocol.
- §7.1.10 (framing) §5.2 Tiered cycle scope.
- §7.1.11 (primitive) §6.2 Severity × Autofix class (orthogonal axes).
- §7.1.12 (primitive) §6.5 Residual work gate.
- §7.1.13 (primitive) §7 Knowledge / memory architecture (3 memory tiers).
- §7.1.14 (recommendation) §11 Implementation roadmap.

### §7.2 Per-item classification

| Item | Verdict | Rationale (≤25 words) | v3 cite (if absorbed) |
|---|---|---|---|
| §7.1.1 compounding core thesis | `absorbed (verified)` | BF-L's Codebase Model thickens across cycles via P-24 attribution into the historical view — direct compounding instantiation. | specs/bf-l.md §2.1 historical view + §3.2 step 7 attribution + §5 post-mvp-evolution |
| §7.1.2 knowledge accumulation between cycles | `absorbed (verified at §3.1.5)` | The Codebase Model IS the persistent cross-cycle knowledge artifact. | specs/bf-l.md §2.1 |
| §7.1.3 artifact stack (specs/knowledge/workpad) | `absorbed (with adaptation, partial — D-1 challenge)` | BF-L absorbs knowledge-document + workpad; *replaces* spec-as-anchor with Codebase-Model-as-anchor. Atelier's stack mapped to substrate primitives, not preserved verbatim. | specs/bf-l.md §2.1 + §2.6 |
| §7.1.4 workshop chain (persona workshops) | `tbd` | BF-L methodology is front-end-agnostic (Loop-2 front-end derives from model profile); persona-workshop is one of multiple methodology overlays. | — |
| §7.1.5 researcher fan-out | `absorbed (with adaptation)` | BF-L §3.1 ingestion phase IS multi-agent fan-out across the six views; per-view subagent dispatch matches the researcher-fan-out pattern. | specs/bf-l.md §3.1 |
| §7.1.6 reviewer panel | `absorbed` | BF-L §4 bias-guard binding via P-14 judge router enforces cross-family judging at augmentation-required regime. | specs/bf-l.md §4 bias-guard + §3.2 step 4 |
| §7.1.7 synthesis and curation | `absorbed (with adaptation)` | BF-L's maintenance loop (Loop-3) IS continuous synthesis-and-curation against the Codebase Model — knowledge-promotion bound at ADR 0023. | specs/bf-l.md §3.3 + §4 knowledge-promotion |
| §7.1.8 conductor orchestrator | `not-applicable-to-candidate-mandate` | BF-L leaves orchestration to methodology layer; substrate doesn't mandate orchestrator shape. | — |
| §7.1.9 workpad protocol | `absorbed (with adaptation)` | BF-L's per-cycle Codebase Model snapshot (pinned version token at dispatch) is the workpad analogue; integration discipline replaces protocol convention. | specs/bf-l.md §2.1 integration + §3.2 step 2 |
| §7.1.10 tiered cycle scope | `absorbed (with adaptation)` | BF-L's per-region regime classifier IS substrate-level tiered cycle scope: automation-eligible / augmentation-required / human-required per region. | specs/bf-l.md §2.3 + §3.2 step 3 |
| §7.1.11 severity × autofix axes | `absorbed (silently — flagged for auditor)` | The orthogonal-axes framing likely informed v3's DEC-2 mandate-fit-per-(architecture × work-unit-class) schema. Not explicitly cited in BF-L spec. | — (flagged for silent-absorption auditor) |
| §7.1.12 residual work gate | `absorbed` | BF-L's per-region regime classifier with hard-floor table + Caremark/RSI block is the residual-work-gate analogue at substrate. | specs/bf-l.md §2.3 |
| §7.1.13 three memory tiers | `absorbed (with adaptation)` | BF-L's three loops (Loop-1/Loop-2/Loop-3) at distinct cadences (slow-once / per-cycle / continuous-low) is a different-shape three-tier memory architecture — pace-layered substrate. | specs/bf-l.md §3 (all loops) |
| §7.1.14 implementation roadmap | `not-applicable-to-candidate-mandate` | Architecture-specific deployment. | — |

### §7.3 Notes

BF-L's deepest single-architecture absorption — Atelier's compounding + knowledge accumulation + tiered cycle scope land in BF-L substrate. Substrate/methodology split more pronounced than BF-S: Codebase Model is "the most ambitious primitive in the catalog" per [candidate-registry](../candidate-registry.md#headline-outcomes-all-10-candidates). §7.1.11 silent-absorption flag shared with sibling specs.

## §8 — archive/architectures-v2/03-phase-gated-foundry.md

### §8.0 File header

v2 Architecture 3 — Phase-Gated Foundry. "Pre-agile structured methodologies become the right shape when agents make them fast." Phase-bound experts, formal templates (SRS, SAD, DD), RTM, gate boards. 4610 words. **One of BF-L's two primary-co-equal v2-lineages** per §1 overview. The dedicated Loop-1 ingestion phase IS a Foundry primitive; the maintenance loop IS Configuration-Management-as-spine.

### §8.1 Enumeration

- §8.1.1 (claim) §1 Core thesis: structured pre-agile methodology + agent speed.
- §8.1.2 (primitive) §2 Phase model (Phases 1-6 with V&V pairing).
- §8.1.3 (primitive) §3 Configuration Management discipline.
- §8.1.4 (primitive) §3.1 Defect-of-origin table.
- §8.1.5 (primitive) §4 RUP-style discipline × phase matrix.
- §8.1.6 (framing) §5 Iteration within phases.
- §8.1.7 (primitive) §6.2 V&V-side roles (structurally independent, different model family).
- §8.1.8 (primitive) §8 Configuration Management as the spine.

### §8.2 Per-item classification

| Item | Verdict | Rationale (≤25 words) | v3 cite (if absorbed) |
|---|---|---|---|
| §8.1.1 structured pre-agile core thesis | `absorbed (with adaptation)` | BF-L's dedicated Loop-1 ingestion phase + Loop-3 maintenance phase + Loop-2 work phase is structured-phase-discipline; phase-bound experts → per-view ingestion subagents. | specs/bf-l.md §3.1 + §3.3 |
| §8.1.2 phase model + V&V pairing | `absorbed (with adaptation)` | BF-L's three loops + per-region regime classifier acts as a phase-gated dispatcher: each cycle is V&V-paired via cross-family judging at augmentation-required regime. | specs/bf-l.md §3 + §4 bias-guard |
| §8.1.3 Configuration Management discipline | `absorbed (verified)` | §4 attribution-store (ADR 0035) + Codebase Model version tokens IS substrate-level CM. Merkle-DAG incremental versioning per §2.1. | specs/bf-l.md §2.1 + §3.2 step 7 + ADR 0035 |
| §8.1.4 defect-of-origin table | `absorbed (with adaptation)` | P-24 attribution envelope `(agent_id, model_snapshot, cycle_id, symbol_id, diff_slice)` per §3.2 step 7 provides defect-of-origin traceability per-symbol. | specs/bf-l.md §3.2 step 7 + ADR 0035 envelope |
| §8.1.5 RUP-style discipline × phase matrix | `absorbed (with adaptation)` | BF-L binds 9 of 10 discipline ADRs at substrate; three-loop discipline (0026) is load-bearing for the BF-L phase structure. | specs/bf-l.md §4 all-discipline-binding |
| §8.1.6 iteration within phases | `absorbed (with adaptation)` | BF-L's three loops each iterate at distinct cadences (Loop-1 deep-slow-once-plus-refresh; Loop-2 per-cycle; Loop-3 continuous low-cadence). | specs/bf-l.md §3.1 / §3.2 / §3.3 |
| §8.1.7 V&V-side independent roles + different model family | `absorbed (verified)` | BF-L §3.2 step 4 augmentation-required regime: *"cross-family judge required via P-14"* — F46 mitigation. | specs/bf-l.md §3.2 step 4 + §4 bias-guard |
| §8.1.8 CM as spine | `absorbed (verified)` | Codebase Model with snapshot-consistency + Merkle-DAG versioning IS CM-as-spine. Codebase Model + P-24 form the CM spine. | specs/bf-l.md §1 axis + §2.1 + §3.2 step 7 |

### §8.3 Notes

BF-L is the v3 candidate with the **strongest Foundry lineage** of any brownfield candidate. Dedicated upfront ingestion (Loop-1), version-tokenised snapshot consistency, per-symbol attribution-as-CM, and per-region regime classifier acting as RTM/gate-board are deep Foundry inheritances. BF-S inherits less from Foundry; BF-M inherits some (CM via P-24) but lacks the dedicated upfront phase. The Foundry lineage distinguishes BF-L from BF-S on substrate-shape: both are substrate-heavy, but BF-L's substrate is phase-structured.

## §9 — archive/architectures-v2/04-evolutionary-tournament.md

### §9.0 File header

v2 Architecture 4 — Evolutionary Tournament. "The factory does not specify the right answer; it sets up the conditions under which the right answer wins." Genome library, predator agent, tournament bracket, model-family diversity. 4279 words.

### §9.1 Enumeration

- §9.1.1 (claim) §1 Core thesis: population + selection pressure + lineage.
- §9.1.2 (primitive) §3 Genome structure.
- §9.1.3 (primitive) §3.4 Diversity policy (model-family diversity as structural).
- §9.1.4 (primitive) §4 Generation cycle.
- §9.1.5 (primitive) §5.3 Predator agent.
- §9.1.6 (primitive) §7 Loops within loops.
- §9.1.7 (framing) §6.3 Independence policy.
- §9.1.8 (recommendation) §10 Scaling.

### §9.2 Per-item classification

| Item | Verdict | Rationale (≤25 words) | v3 cite (if absorbed) |
|---|---|---|---|
| §9.1.1 population + selection core thesis | `not-applicable-to-candidate-mandate` | Tournament-specific population-based methodology; BF-L is single-Codebase-Model-driven. | — |
| §9.1.2 genome structure | `not-applicable-to-candidate-mandate` | Tournament-specific artifact. | — |
| §9.1.3 model-family diversity as structural | `absorbed (with adaptation)` | BF-L §4 bias-guard binds cross-model-family judging via P-14 at augmentation-required regime. F46 mitigation. | specs/bf-l.md §4 bias-guard + §3.2 step 4 |
| §9.1.4 generation cycle | `not-applicable-to-candidate-mandate` | Tournament-specific. | — |
| §9.1.5 predator agent | `rejected (subsumed by substrate-level adversarial discipline)` | BF-L substitutes Tournament's predator-agent with substrate-level adversarial discipline: per-region regime classifier hard-floor + cross-family judge + P-24 attribution. | — |
| §9.1.6 loops within loops | `absorbed (with adaptation)` | BF-L's three loops (ingestion / work / maintenance) at distinct cadences IS loops-within-loops at a different shape (cadence-stratified, not generation-stratified). | specs/bf-l.md §3 + §4 three-loop |
| §9.1.7 independence policy | `absorbed` | BF-L §3.2 step 4 cross-family judge requirement at augmentation-required regime enforces builder-judge independence. | specs/bf-l.md §3.2 step 4 + §4 |
| §9.1.8 scaling | `tbd` | BF-L §6 P-26 integration discipline at 1M+LOC carry (Phase-8 lean-eval candidate) is the BF-L analogue of Tournament's scaling concern. | — |

### §9.3 Notes

Tournament's primary primitives (population, predator, bracket) are N/A to BF-L (single-model-single-codebase), but cross-model-family diversity (§9.1.3) + independence policy (§9.1.7) land at substrate. Predator-agent (§9.1.5) explicitly rejected: BF-L's per-region hard-floor table + cross-family judge substitutes. Loops-within-loops absorption (§9.1.6) is cadence-stratified rather than generation-stratified.

## §10 — archive/architectures-v2/failure-modes.md

### §10.0 File header

F1-F20 per-architecture coverage matrix PLUS "Coverage column scores" per-architecture qualitative-strength table (4 ★-rated rows + prose verdicts). 664 words. **§10 floor = 24 (20 F-modes + 4 per-architecture coverage rows)** per Reviewer 6 D-H1 amendment.

### §10.1 Enumeration

20 F-mode rows + 4 per-architecture coverage-strength rows = 24 enumeration units.

- §10.1.1 (F-mode row) F1 Hallucination loop.
- §10.1.2 (F-mode row) F2 Reward hacking.
- §10.1.3 (F-mode row) F3 Spec-completeness.
- §10.1.4 (F-mode row) F4 Code quality.
- §10.1.5 (F-mode row) F5 Cognitive ceiling.
- §10.1.6 (F-mode row) F6 Cognitive debt.
- §10.1.7 (F-mode row) F7 Normalization of deviance.
- §10.1.8 (F-mode row) F8 Stale knowledge.
- §10.1.9 (F-mode row) F9 Spec overfitting.
- §10.1.10 (F-mode row) F10 Findings disappear.
- §10.1.11 (F-mode row) F11 Renumbering.
- §10.1.12 (F-mode row) F12 Lethal trifecta.
- §10.1.13 (F-mode row) F13 Missing-config.
- §10.1.14 (F-mode row) F14 Attribution collapse.
- §10.1.15 (F-mode row) F15 Single-prompt collapse.
- §10.1.16 (F-mode row) F16 Resume-fidelity.
- §10.1.17 (F-mode row) F17 Parallel agents on shared dirs.
- §10.1.18 (F-mode row) F18 Prose-spec rigor.
- §10.1.19 (F-mode row) F19 Model-floor dependency.
- §10.1.20 (F-mode row) F20 Maintenance asymmetry.
- §10.1.21 (coverage-strength row) Architecture 1 (Refinery) ★★★★ strong on F3/F9/F7; medium on F4/F18.
- §10.1.22 (coverage-strength row) Architecture 2 (Atelier) ★★★★★ strongest on F4/F8/F10/F11/F15/F17.
- §10.1.23 (coverage-strength row) Architecture 3 (Foundry) ★★★★ strongest on F11/F14/F18; medium on F5.
- §10.1.24 (coverage-strength row) Architecture 4 (Tournament) ★★★★ strongest on F1/F15/F17/F19; weakest on F18.

### §10.2 Per-item classification

| Item | Verdict | Rationale (≤25 words) | v3 cite (if absorbed) |
|---|---|---|---|
| §10.1.1 F1 Hallucination | `absorbed` | BF-L §4 bias-guard (ADR 0018 + P-14) + Codebase Model grounding closes F1. | specs/bf-l.md §4 bias-guard + §3.2 step 4 |
| §10.1.2 F2 Reward hacking | `absorbed` | BF-L §2.5 P-08 held-out partition + ingestion-aware judges + §4 holdout binding ADR 0021. | specs/bf-l.md §2.5 + §4 holdout |
| §10.1.3 F3 Spec-completeness | `not-applicable-to-candidate-mandate` | BF-L challenges D-1; spec-completeness verdict reframed as Codebase-Model-completeness (which is the load-bearing 1M+LOC scaling carry per §6). | — |
| §10.1.4 F4 Code quality | `absorbed (with adaptation)` | BF-L per-region cross-family judging + P-23 dependency-impact graph + per-region regime classifier hard-floor table. | specs/bf-l.md §3.2 + §4 |
| §10.1.5 F5 Cognitive ceiling | `absorbed (with adaptation)` | BF-L per-region human-required regime (Caremark/RSI + below coverage-floor) + L4 named-human routing is substrate-level F5 mitigation. | specs/bf-l.md §3.2 step 4 + §2.3 |
| §10.1.6 F6 Cognitive debt | `absorbed` | BF-L §3.2 step 6 P-05 trajectory + §4 cognitive-escrow binding + BF-L specialization (ingestion trajectories become part of Codebase Model). | specs/bf-l.md §4 + ADR 0019 |
| §10.1.7 F7 Normalization of deviance | `absorbed (with adaptation)` | BF-L Loop-3 maintenance per-region prioritisation surfaces drift earlier; per-region regime classifier with hard-floor table resists deviance accumulation. | specs/bf-l.md §3.3 + §2.3 |
| §10.1.8 F8 Stale knowledge | `absorbed (verified)` | **BF-L's deepest F8 mitigation**: Loop-3 P-13 maintenance loop per ADR 0048 + §3.3. | specs/bf-l.md §3.3 + ADR 0048 |
| §10.1.9 F9 Spec overfitting | `not-applicable-to-candidate-mandate` | BF-L challenges D-1; spec-overfitting framing presupposes spec-as-durable. | — |
| §10.1.10 F10 Findings disappear | `absorbed` | BF-L §3.2 step 7 substrate-logs-via-P-24 + immutable attribution + historical view consumption closes finding-disappearance at substrate. | specs/bf-l.md §3.2 step 7 + ADR 0035 |
| §10.1.11 F11 Renumbering | `absorbed (verified)` | BF-L §2.1 structural view per-symbol stable-IDs (`{language, qname, source-revision}` + stable hash) + Merkle-DAG incremental versioning. | specs/bf-l.md §2.1 structural view + §3.2 step 7 |
| §10.1.12 F12 Lethal trifecta | `absorbed` | BF-L §4 trifecta-closure binding (ADR 0027) + P-08 holdout + regime classifier hard-floor table — both substrate-enforced. | specs/bf-l.md §4 trifecta + ADR 0027 |
| §10.1.13 F13 Missing-config | `absorbed (with adaptation)` | P-23 dependency-impact graph surfaces config-dependency drift; per-region regime classifier with debt-cluster + Caremark hard-floor rejects missing-floor regions. | specs/bf-l.md §2.6 + §2.3 |
| §10.1.14 F14 Attribution collapse | `absorbed (verified)` | BF-L §3.2 step 7 P-24 attribution store + Codebase Model historical view explicitly closes F14. | specs/bf-l.md §3.2 step 7 + ADR 0035 |
| §10.1.15 F15 Single-prompt collapse | `absorbed (with adaptation)` | BF-L §4 bias-guard cross-model-family judging at augmentation-required regime + per-region routing. Structural diversity at substrate. | specs/bf-l.md §4 + §3.2 step 4 |
| §10.1.16 F16 Resume-fidelity | `absorbed` | BF-L P-05 trajectory + P-24 cycle_id + Codebase Model version token (git-commit + ingestion-pass ID) provides resume anchor. | specs/bf-l.md §3.2 step 6-7 + §2.1 integration |
| §10.1.17 F17 Parallel agents on shared dirs | `tbd` | Parallel-agents-on-shared-Codebase-Model is the BF-L variant; substrate supports concurrent ingestion (snapshot consistency at version boundaries) but specific anti-collision is methodology call. | — |
| §10.1.18 F18 Prose-spec rigor | `not-applicable-to-candidate-mandate` | BF-L challenges D-1; spec-rigor presupposes spec-as-durable. | — |
| §10.1.19 F19 Model-floor dependency | `absorbed` | BF-L §4 bias-guard + cross-family judging via P-14 surfaces model-floor explicitly per F46. | specs/bf-l.md §4 + ADR 0018 |
| §10.1.20 F20 Maintenance asymmetry | `absorbed (verified)` | **BF-L's deepest F20 mitigation**: Loop-3 P-13 maintenance loop IS the structural answer per ADR 0048 + §2.2. | specs/bf-l.md §2.2 + §3.3 + ADR 0048 |
| §10.1.21 A1 Refinery coverage row | `not-applicable-to-candidate-mandate` | Coverage row characterizes Architecture 1, not BF-L. Informational. | — |
| §10.1.22 A2 Atelier coverage row | `not-applicable-to-candidate-mandate` | Coverage row characterizes Architecture 2 (one of BF-L's lineages), but ★★★★★ scoring is per-Atelier, not per-BF-L. BF-L's own F-mode coverage tracked above. | — |
| §10.1.23 A3 Foundry coverage row | `not-applicable-to-candidate-mandate` | Coverage row characterizes Architecture 3 (one of BF-L's lineages); scoring is per-Foundry. BF-L's F11/F14 absorption is per-spec, not per-row inheritance. | — |
| §10.1.24 A4 Tournament coverage row | `not-applicable-to-candidate-mandate` | Coverage row characterizes Architecture 4. | — |

### §10.3 Notes (REQUIRED §N.3 ADR-0036 framing characterization per Reviewer 5 Defect 2 + auto-007 amendment)

**ADR-0036 / P-30 framing — BF-L "commodity dispatch surface"** (per Reviewer 5 Defect 2 + auto-007 §N.3 amendment + Phase-6 verifier Finding-2). BF-L's §0 ADR-citation index row for 0036 carries the verbatim annotation:

> *"0036 IS consumed (without per-variant binding) by P-13 maintenance-loop dispatch ([ADR 0048](../../../docs/adr/0048-p-13-maintenance-loop.md)), so 0036 appears in §0 as a **commodity dispatch surface**, not as a framework requiring BF-L per-variant authorship."*

(per [BF-L spec §0](../specs/bf-l.md#0-adr-citation-index))

**Distinct from U-A and D7-U-1's "registrar-framework" framing.** U-A 0053 + D7-U-1 0064 are per-variant ADRs on framework 0036; BF-L has *no per-variant ADR for 0036* — P-13 emits `kind=maintenance-trigger` events, reconciliation handlers subscribe; substrate consumes the framework verbatim without new event types / envelope schemas / registrar policies. The silent-absorption auditor's cross-spec ADR-0036 framing audit (per Reviewer 2 A3 + Reviewer 6 D-H4) MUST preserve this distinction — BF-L's "commodity dispatch" framing coexists with U-A/D7-U-1's "registrar-framework" framing without collapse.

**F-mode coverage summary.** 15-of-20 absorbed (F1, F2, F4, F5, F6, F7, F8, F10, F11, F12, F13, F14, F15, F16, F19, F20). F8 + F20 verified-with-deepest-mitigation (Loop-3 P-13 maintenance loop). F11 + F14 verified-absorbed. 1 TBD (F17 parallel-agents on shared Codebase Model). 4 N/A (F3, F9, F18 presuppose D-1 which BF-L challenges; A1-A4 coverage rows are per-v2-architecture).

## §11 Summary

**Per-token cell counts (matches YAML frontmatter):**

| Token | Count |
|---|---|
| `absorbed` (incl. with-adaptation, verified, silently) | 69 |
| `rejected` (incl. `challenged` / partial-challenge) | 11 |
| `not-applicable-to-candidate-mandate` | 18 |
| `tbd` | 7 |
| **Total cells** | **105** (§2.2 (3) + §3.2 (16) + §4.2 (8) + §5.2 (9) + §6.2 (8) + §7.2 (14) + §8.2 (8) + §9.2 (8) + §10.2 (24) + §1.5 (7) = 105) |

YAML frontmatter folds `challenged` into `rejected` per schema convention; per-cell tables use distinct tokens.

**High-confidence absorbed:** D-4, D-5, D-6, D-7 per §1.5; F8 + F20 (verified-deepest-mitigation, BF-L signature); F11 + F14; §7.1.1 Atelier compounding; §8.1.8 Foundry CM-as-spine; §8.1.3 Configuration Management.

**High-confidence challenged:** D-1 (substrate-displaces-spec axis); D-2 (scenarios-from-model axis); D-3 (partial, Codebase Model is third irreducible substrate primitive).

**Surfaced TBDs (require lead-agent reconciliation or Phase-8 follow-up):**

1. §3.1.11 persona-vs-graph-node — BF-L front-end-agnostic; Phase-8 lean-eval.
2. §3.1.15 parallel-agent + human-role — converges with §6 1M+LOC carry.
3. §4.1.6 falsified consensus items — needs per-item review.
4. §6.1.5 Refinery 5-mode failure classification — Phase-8 lean-eval candidate.
5. §7.1.4 Atelier workshop chain — methodology-overlay call.
6. §9.1.8 Tournament scaling — converges with §6 1M+LOC carry.
7. §10.1.17 F17 parallel agents on Codebase Model — methodology-layer anti-collision call.

**Silent-absorption auditor flags:**

- §3.1.16 cross-cutting primitives (v3 `primitives/index.md` likely inherited framing without explicit citation).
- §7.1.11 severity × autofix orthogonal axes (likely informed DEC-2 schema).

**ADR-0036 framing reconciliation flag:** §10.3 carries the required ADR-0036 framing characterization as **"commodity dispatch surface"** — distinct from U-A 0053 / D7-U-1 0064's "registrar-framework" framing. Silent-absorption auditor MUST preserve this distinction at aggregation.

**Known-rejected items confirmed:**

- §4.1.10 OpenHands+Overstory substrate stack — `rejected (explicitly-excluded-per-constraints-extracted)`.
- §5.1.7 Compound Atelier as baseline — `rejected (explicitly-anchor-avoided)`.

## §12 References

**BF-L spec + supporting docs:**

- [`architectures/v3/specs/bf-l.md`](../specs/bf-l.md) — BF-L Phase-6 architecture spec (audit input).
- [`architectures/v3/candidate-registry.md` BF-L entry](../candidate-registry.md#bf-l--brownfield-legacy-ingestion-first) — registry entry for §1 lineage statement.
- [`architectures/v3/substrate-requirements/bf-l.md`](../substrate-requirements/bf-l.md) — substrate-requirements summary.
- [`architectures/v3/tracks/brownfield-legacy-ingestion-first.md`](../tracks/brownfield-legacy-ingestion-first.md) — BF-L track sketch (D-1..D-7 challenges sourced here).
- [`architectures/v3/decisions/auto-003-bfl-rg-view-choice.md`](../decisions/auto-003-bfl-rg-view-choice.md) — BF-L RG-view choice (option A′ smoke-test-first).
- [`architectures/v3/decisions/auto-007-phase-7-dispatch-shape.md`](../decisions/auto-007-phase-7-dispatch-shape.md) — Phase-7 dispatch brief.
- [`architectures/v3/backfill-notes/bf-s.md`](./bf-s.md) — lead-agent-authored Phase-7 exemplar (shape inheritance).

**Archive (9 files audited):**

- [`archive/research-plan.md`](../../../archive/research-plan.md) — §2
- [`archive/synthesis-v1-v2/00-synthesis.md`](../../../archive/synthesis-v1-v2/00-synthesis.md) — §3
- [`archive/synthesis-v1-v2/13-round-2-synthesis.md`](../../../archive/synthesis-v1-v2/13-round-2-synthesis.md) — §4
- [`archive/architectures-v2/00-comparison.md`](../../../archive/architectures-v2/00-comparison.md) — §5
- [`archive/architectures-v2/01-specification-refinery.md`](../../../archive/architectures-v2/01-specification-refinery.md) — §6
- [`archive/architectures-v2/02-compound-atelier.md`](../../../archive/architectures-v2/02-compound-atelier.md) — §7
- [`archive/architectures-v2/03-phase-gated-foundry.md`](../../../archive/architectures-v2/03-phase-gated-foundry.md) — §8
- [`archive/architectures-v2/04-evolutionary-tournament.md`](../../../archive/architectures-v2/04-evolutionary-tournament.md) — §9
- [`archive/architectures-v2/failure-modes.md`](../../../archive/architectures-v2/failure-modes.md) — §10

**Archive indexes (context):**

- [`archive/ARCHIVE.md`](../../../archive/ARCHIVE.md)
- [`archive/synthesis-v1-v2/ARCHIVE.md`](../../../archive/synthesis-v1-v2/ARCHIVE.md) — source of D-1..D-7 default enumeration.
- [`archive/architectures-v2/ARCHIVE.md`](../../../archive/architectures-v2/ARCHIVE.md) — source of 4-architecture taxonomy.

**ADRs cited:**

- BF-L common substrate: [ADR 0010 P-01](../../../docs/adr/0010-p-01-sandbox-runtime.md), [0011 P-02](../../../docs/adr/0011-p-02-cost-ceilings.md), [0012 P-05](../../../docs/adr/0012-p-05-trajectory-capture.md), [0013 P-06](../../../docs/adr/0013-p-06-watchdog-tiers.md), [0014 P-07](../../../docs/adr/0014-p-07-telemetry-ingestor.md), [0015 P-08](../../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md), [0016 P-14](../../../docs/adr/0016-p-14-judge-router.md), [0017 P-22](../../../docs/adr/0017-p-22-polyglot-codebase-index.md).
- Discipline: [0018-0027](../../../docs/adr/).
- Framework + per-variant: [0028 P-19 framework](../../../docs/adr/0028-p-19-eligibility-regime-classifier.md), [0049 BF-L P-19 per-region variant](../../../docs/adr/0049-p-19-variant-bf-l-per-region.md).
- Designed-system substrate: [0031 P-23](../../../docs/adr/0031-p-23-dependency-impact-graph.md), [0036 P-30 event registrar (commodity dispatch surface per §10.3)](../../../docs/adr/0036-p-30-event-registrar-substrate.md).
- 2-candidate-fold: [0034 P-27](../../../docs/adr/0034-p-27-archaeological-brief-tooling.md), [0035 P-24](../../../docs/adr/0035-p-24-attribution-store.md).
- BF-L orphan substrate: [0047 P-26 Codebase Model](../../../docs/adr/0047-p-26-codebase-model.md), [0048 P-13 maintenance loop](../../../docs/adr/0048-p-13-maintenance-loop.md).

**Constraints / decisions:**

- [`architectures/v3/constraints-extracted.md`](../constraints-extracted.md) — UC1-UC8 user constraints (source of known-rejected v3 item flags).
- [`architectures/v3/decisions-captured.md`](../decisions-captured.md) — DEC-1 / DEC-1.a / DEC-2 / Phase-3.5.5 RG-primitive rule.
