---
candidate: bf-m
candidate-name: Brownfield, Methodology-First
mandate-scope: brownfield
based-on-spec-commit: 00ae134
based-on-date: 2026-05-27
exemplar: false
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
  absorbed: 69
  rejected: 5
  not-applicable: 16
  challenged: 3
  tbd: 5
  # Verdict-token totals across per-archive-file classification tables (§2.2..§10.2).
  # Total = 98 cells (matches §2.1(3)+§3.1(16)+§4.1(8)+§5.1(9)+§6.1(8)+§7.1(14)+§8.1(8)+§9.1(8)+§10.1(24)).
  # D-1..D-7 §1.5 rows are counted separately (5 absorbed-verified + 2 challenged).
self-check-results:
  # Per auto-007 §1.5 rubric + self-check items (a)-(g).
  wc-w: 6955  # over Heavy tier upper bound (6500) by ~455 words; see budget-flag below
  ls-cited-files: PASS  # all cited v3 files exist (specs/bf-m.md, ADRs 0010-0046,
                        # auto-007, candidate-registry, substrate-requirements/bf-m.md)
  section-headers: PASS  # §1, §1.5, §2-§10, §11, §12 + §N.0 file-headers per §2-§10
  enumeration-floor: PASS  # §2.1=3 (small-file-exception), §3.1=17, §4.1=13, §5.1=11,
                           # §6.1=8, §7.1=15, §8.1=8, §9.1=9, §10.1=24 (all ≥ floor;
                           # §10.1=24 per Reviewer 6 D-H1; §10 floor=24)
  cell-counts-match-yaml: PASS  # YAML per-archive-table tallies match §2.2-§10.2 grep counts
  verbatim-text-pull: n/a  # no binding rule tables verbatim-cited (per Reviewer 3 D6)
  tbd-count: 5  # 5 `tbd` verdict cells in classification tables; surfaced in §11
budget-flag: |
  Measured at 6955 words; Heavy tier upper bound is 6500 (~455 word overrun).
  Attributed to (a) the §1.5 D-1..D-7 verification subsection's two challenged-default
  rows (D-1 + D-2 each require a multi-clause spec cite); (b) the §10 24-row F-mode
  classification table (BF-M absorbs 19 of 20 F-modes with explicit substrate/ADR cites
  per cell); (c) BF-M's hybrid Atelier+Foundry lineage requiring two §1 lineage clauses;
  (d) the higher per-cell substrate-cite density (BF-M binds ~13 substrate references vs
  BF-S's 5). Consistent with the BF-S exemplar's similar overrun pattern (5698 vs 5000
  Light cap). Lead-agent decision deferred to aggregation step.
---

# Back-fill notes — BF-M (Brownfield, Methodology-First) vs v1/v2 archive

## §1 Overview

**Mandate.** Brownfield-only by deliberate construction. BF-M's mandate-fit row (per [BF-M spec §5](../specs/bf-m.md#5-mandate-fit) + frontmatter) is 3-of-5 `brownfield` cells, 2 `n/a` cells (initial-spec, mvp) — `n/a` is explicit out-of-scope rejection per [track §6](../tracks/brownfield-methodology-first.md#6-what-this-track-is-not-trying-to-be), not silence.

**Axis.** **Methodology-first** — the 8-stage per-cycle contract (Trigger → Comprehension → Intent capture → Plan → Build → Cross-model review → Acceptance → Ship-or-escalate) is the load-bearing artifact. Substrate primitives are *stage-attached capabilities at boundaries*, vendor-deferred. Per [BF-M spec §3](../specs/bf-m.md#3-methodology-shape) distinctive decision 1: "Methodology cycle IS the architecture; substrate is downstream."

**Entry-mode.** Brownfield only. Stage 2 (Comprehension) is the brownfield-defining stage — the archaeological brief presumes a pre-existing codebase. Cold-start is N/A; falsification scenario: an empty-repository BF-M run that completed stages 2-3 successfully would falsify the brownfield-defining claim.

**Strongest v2-architecture-lineage.** *This candidate's strongest v2-architecture-lineage is a **hybrid of Architecture 2 (Compound Atelier) and Architecture 3 (Phase-Gated Foundry)**, with secondary inheritance from **Architecture 1 (Specification Refinery)** on the change-intent-block surface.* Rationale (derived from [BF-M candidate-registry entry §axis + §methodology-shape](../candidate-registry.md#bf-m--brownfield-methodology-first)): BF-M's 8-stage cycle is structurally a **phase-bound progression with V&V pairing** (Foundry-flavored — stages 5/6/7 are build / cross-model review / held-out acceptance, the V&V triad), while the **work-unit-class polymorphism + per-cycle work-pad-equivalent (P-03 worktree) + compounding through PR body + change-intent block at stage 3 driving downstream stages** is Atelier-flavored (queue + persona-equivalent stage chain + accumulated typed PR-body artifact). The "change-intent block, not system-intent" (a contraction of El Kaim's 9-field intent) on stage 3 is the Refinery secondary inheritance — spec-the-change-not-the-system is the BF-M brownfield-adaptation of Refinery's spec-as-product framing.

**D-1 through D-7 default-verification preview.** Per [auto-007 §1.5 verification rubric](../decisions/auto-007-phase-7-dispatch-shape.md#decision-round-2) and Reviewer 5/6 amendments: D-1 through D-7 are NOT silently skipped. The §1.5 verification subsection below records the per-default verdict for BF-M; per Reviewer 3 / D15, the audit-trail is mechanically auditable.

## §1.5 D-1 through D-7 defaults verification

Per Reviewer 5 Defect 1 + Reviewer 6 D-H5 amendments. Each default verified per `grep` against BF-M spec content; verdict tokens per the auto-007 Round-2 rubric.

| Default | Source claim | BF-M verdict | Spec cite |
|---|---|---|---|
| D-1 specs durable | `00-synthesis.md` §2.1 | `challenged` | BF-M §3 distinctive methodology decision: "Spec the change, not the system" — the change-intent block is per-cycle, not whole-system. Per [BF-M spec §5 post-mvp-evolution](../specs/bf-m.md#5-mandate-fit): "The codebase is the durable artifact (D-1 challenged-partial per track §4)". Durable artifact is the codebase + PR-body history, not a separate spec doc. |
| D-2 scenarios out-of-tree | `00-synthesis.md` §2.2 | `challenged` | BF-M §3 stage 7 + §4 holdout binding: "Brownfield-redefined: per the D-2 challenge, the holdout is the *unseen subset* of codebase-derived scenarios, not the out-of-tree subset." (CTR-B5 inversion documented at §3 stage 7.) |
| D-3 Agent = Model + Harness | `13-round-2-synthesis.md` §1.1 C10 | `absorbed (verified at specs/bf-m.md §3 stage 5 "Builder agent" + stage 6 "Distinct-model reviewer" + §4 bias-guard binding)` | BF-M §3 stages 5-6 + §4 bias-guard ADR 0018 + P-14 judge router ADR 0016 |
| D-4 holdout discipline | `13-round-2-synthesis.md` §1.1 C13 | `absorbed (verified at specs/bf-m.md §3 stage 5 "no access to acceptance criteria withheld at stage 7" + §4 holdout binding)` | §3 stage 5 / stage 7 air-gap + §4 holdout ADR 0021 + P-08 substrate-side enforcement |
| D-5 hard cost ceilings | `13-round-2-synthesis.md` §1.1 C15 | `absorbed (verified at specs/bf-m.md §2 "P-02 cost ceilings enforce per-cycle / per-work-unit-class budget caps per D-5" + §4 cost-ceiling binding)` | §2 P-02 binding + §4 cost-ceiling ADR 0020; CTR-E1 10× variance + CTR-E6 ~7-point CaMeL utility tax accepted as inputs |
| D-6 tiered watchdog | `13-round-2-synthesis.md` §1.1 C14 | `absorbed (verified at specs/bf-m.md §2 "P-06 watchdog tiers attach Daemon to every stage, Triage at stages 4/5/6, Patrol across cycles" + §4 three-loop binding "Patrol-tier monitoring of cross-cycle drift")` | §2 P-06 binding + §4 three-loop ADR 0026 + Patrol-tier closure |
| D-7 trajectory capture | `13-round-2-synthesis.md` §1.1 C16 | `absorbed (verified at specs/bf-m.md §2 "P-05 trajectory capture records each cycle event; stage-8 PR body carries a trajectory pointer (the F42 cognitive-escrow re-entry surface)" + §4 cognitive-escrow binding)` | §2 P-05 + §4 cognitive-escrow ADR 0019; PR body IS the F42 re-entry surface |

**Summary:** 5-of-7 defaults absorbed with explicit cite (D-3, D-4, D-5, D-6, D-7); 2 defaults explicitly challenged (D-1 spec-the-change-not-the-system; D-2 codebase-derived-holdout-not-out-of-tree). BF-M's two D-default challenges are load-bearing distinctive decisions (per [BF-M spec §3](../specs/bf-m.md#3-methodology-shape) + [§4 holdout binding](../specs/bf-m.md#4-discipline-binding)) and are explicitly cited — not silent absorptions. Auditor reconciliation expected to confirm both challenges as deliberate, not as silent rejection.

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
| §2.1.1 three-layer pipeline | `absorbed (with adaptation)` | v3's research → synthesis → action pipeline preserved across Phases 1-6; BF-M inherits via Phase-6 spec authoring under DEC-1/DEC-2. | architectures/v3/corpus-inventory.md + ARCHITECTURE-V3-SYNTHESIS-PLAN.md Phases 1-6 |
| §2.1.2 "enough research" trigger | `absorbed` | v3 Phase-1 corpus saturation + Phase-3 contradiction-counting fulfilled this; BF-M's open-carries (§6) are surfaced not buried. | architectures/v3/corpus-inventory.md + contradictions.md |
| §2.1.3 folding policy | `not-applicable-to-candidate-mandate` | Document-management discipline at synthesis-process level; not a per-candidate architectural primitive. | — |

### §2.3 Notes

Research-plan.md's user-stated constraints (UC1 lights-out / UC4 brownfield-cold-start / UC5 / UC6 archive-and-rebuild) are already in `constraints-extracted.md` and out of Phase-7 scope. BF-M's UC1 / lights-out mapping is per-stage (stages 1-7 lights-out, stage 8 may escalate per BF-M §3 vocabulary-mapping); the research-plan's framing of UC1 as whole-system L5 is dissolved by BF-M's per-stage shape, not engaged here.

## §3 — archive/synthesis-v1-v2/00-synthesis.md

### §3.0 File header

Round-1 v2 synthesis post-primary-source-access. Canonical entry for F1-F20. 5020 words. **D-1 through D-7 defaults are sourced from this file; verified per-candidate in §1.5 above.**

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
| §3.1.1 specs primary artifact (D-1) | `challenged (per §1.5)` | BF-M challenges: spec-the-change-not-the-system. Codebase + PR-body history is the durable artifact. | specs/bf-m.md §3 + §5 |
| §3.1.2 scenarios outside codebase (D-2) | `challenged (per §1.5)` | BF-M challenges: holdout is unseen subset of codebase-derived scenarios (CTR-B5 inversion). | specs/bf-m.md §3 stage 7 + §4 |
| §3.1.3 validation harnesses are real engineering | `absorbed` | BF-M stage 6 + stage 7 are the V&V pairing where validation harness lives (P-12 linters + P-08 runner + Ashby perimeter). | specs/bf-m.md §3 stage 6/7 + §4 |
| §3.1.4 Agent=LLM-in-loop (D-3) | `absorbed (verified at §1.5)` | D-3 verified per §1.5. | specs/bf-m.md §3 stage 5/6 |
| §3.1.5 knowledge accumulates between cycles | `absorbed (with adaptation)` | BF-M §4 knowledge-promotion binding: stale-knowledge inversion (F8) is next-reader-check + `kw:confidence` tagging per followup/11 four-way classification. | specs/bf-m.md §4 knowledge-promotion |
| §3.1.6 single-threaded human ceiling | `absorbed (with adaptation)` | BF-M §3 vocabulary-mapping: per-stage lights-out dissolves CTR-A1/CTR-H10. Human ceiling addressed per-stage, not whole-system. | specs/bf-m.md §3 vocabulary-mapping |
| §3.1.7 human leverage upstream/downstream | `absorbed (with adaptation)` | BF-M stage 8 escalation + stage 3 intent-capture as human-leverage points; per-stage lights-out boundary. | specs/bf-m.md §3 stage 3/8 |
| §3.1.8 tiered ceremony | `absorbed` | BF-M's per-work-unit-class stage compression (regression-fix narrow + deep; codebase-evolution-proposal broad + shallow) IS tiered ceremony. | specs/bf-m.md §3 + §5 work-unit-classes |
| §3.1.9 cost first-class (D-5) | `absorbed (verified at §1.5)` | D-5 verified per §1.5. | specs/bf-m.md §2 + §4 cost-ceiling |
| §3.1.10 human-review tension | `absorbed (with adaptation)` | BF-M binds at stage 6 cross-model review + stage 8 escalation triggers; tiered-by-stage not tiered-by-cycle. | specs/bf-m.md §3 + §4 |
| §3.1.11 persona vs graph-node tension | `not-applicable-to-candidate-mandate` | BF-M is stage-as-named-obligation, neither persona-based nor graph-node. Tension orthogonal to BF-M cycle shape. | — |
| §3.1.12 spec format tension | `absorbed (with adaptation)` | BF-M binds change-intent block as structured-fields format (rationale / invariants / observable acceptance / regression surface / blast radius / rollback) — structured, not prose. | specs/bf-m.md §3 stage 3 |
| §3.1.13 knowledge architecture tension | `absorbed (with adaptation)` | BF-M binds the followup/11 four-way knowledge classification + `kw:confidence` tagging — DAG-ish but lightweight; placement contested CTR-H2/CTR-H3 carried to §6. | specs/bf-m.md §4 + §6 |
| §3.1.14 adversarial review tension | `absorbed (with adaptation)` | BF-M binds reviewer-as-separate-role (stage 6 cross-model reviewer); not attribute-of-every-reviewer. F46 mitigation via P-14. | specs/bf-m.md §3 stage 6 + §4 bias-guard |
| §3.1.15 parallel-agent + human-role tension | `absorbed (with adaptation)` | F17 (parallel agents on shared dirs) substrate-closed via P-03 worktree isolation (ADR 0045 orphan). Human-role bound at stage 8. | specs/bf-m.md §2 P-03 + §3 stage 5/8 |
| §3.1.16 cross-cutting primitives | `absorbed (silently — flagged for auditor)` | v3 `primitives/index.md` carries cross-cutting framing; BF-M spec doesn't explicitly cite 00-synthesis §5. | — (flagged for silent-absorption auditor) |

### §3.3 Notes

BF-M's deepest absorption from 00-synthesis is the **tiered-ceremony** framing (§3.1.8) which becomes BF-M's per-work-unit-class stage-compression — a load-bearing methodology decision (OQ-T1 carry). Two D-defaults (D-1, D-2) are explicitly challenged — see §1.5. The silent-absorption flag on §3.1.16 surfaces the same `primitives/index.md` inheritance noted in the BF-S exemplar; cross-spec audit territory.

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
- §4.1.10 (recommendation) §5.2 Three-layer substrate stack (OpenHands SDK + Overstory-design-in-Python + commodity research stack).
- §4.1.11 (framing) §6.2 / §7 Round-2 recommended path forward replacing 00-comparison §7.
- §4.1.12 (claim) §8 Closing claim.

### §4.2 Per-item classification

| Item | Verdict | Rationale (≤25 words) | v3 cite (if absorbed) |
|---|---|---|---|
| §4.1.1-§4.1.5 D-3..D-7 defaults | `absorbed (verified at §1.5)` | All five D-defaults verified per §1.5 above; D-3, D-4, D-5, D-6, D-7 absorbed. | specs/bf-m.md §2-§4 |
| §4.1.6 falsified consensus items | `tbd` | Need per-item review of what was falsified vs preserved in v3 BF-M context. | — |
| §4.1.7 F21-F33 failure modes promoted | `absorbed (with adaptation)` | BF-M spec invokes F12/F33/F34/F38/F39/F42/F44/F46/F51/F52/F53/F54/F55/F56/F57/F59 explicitly across §2-§4. | specs/bf-m.md §2 + §3 + §4 (multiple F-mode invocations) |
| §4.1.8 sandbox + cost-ceilings as shared infrastructure | `absorbed` | BF-M §2 commodity substrate baseline binds P-01 sandbox (ADR 0010) + P-02 cost ceilings (ADR 0011) directly. | specs/bf-m.md §2 |
| §4.1.9 CI/CD pipeline adaptation thesis | `absorbed (with adaptation)` | BF-M's 8-stage cycle IS the CI/CD-adapted pipeline — stages 5-6-7 are build/review/test analogue. Methodology-first framing makes the pipeline the architecture. | specs/bf-m.md §1 axis + §3 |
| §4.1.10 OpenHands+Overstory substrate stack | `rejected (explicitly-excluded-per-constraints-extracted, see constraints-extracted.md)` | **Known-rejected v3 item** per Reviewer 6 D-H8. BF-M substrate-vendor choice is operator-deferred (per §1 axis "vendor-deferred at boundaries"); the specific stack is NOT a v3-architecture-level adoption. | — |
| §4.1.11 §7 Round-2 recommended path forward | `rejected (subsumed by v3 multi-candidate framing)` | Round-2 §7 recommended a single path; v3 DEC-1/DEC-1.a preserves 10 candidates for Phase-8 falsification. | — |
| §4.1.12 §8 Closing claim | `not-applicable-to-candidate-mandate` | Cross-architectural meta-claim; not per-candidate. | — |

### §4.3 Notes

BF-M does NOT claim any framework ADR (no P-19 / P-28 / P-29 / P-30 — per [BF-M spec §0 framework-ADR pairing annotation](../specs/bf-m.md#0-adr-citation-index)). Consequently, the per-candidate ADR-0036 framing characterization required for BF-L / U-A / D7-U-1 per [auto-007 §N.3 amendment](../decisions/auto-007-phase-7-dispatch-shape.md#decision-round-2) does NOT apply to BF-M. The [AGENTS-MD-a9fb7b42f8 framework-scope discipline](../../../AGENTS.md#framework-adr-scope-boundary-discipline) does not bind for BF-M. The silent-absorption auditor's cross-spec ADR-0036 framing audit will not touch BF-M cells.

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
| §5.1.1 four-architecture taxonomy | `absorbed (with adaptation)` | v3 candidate-registry preserves the 4 v2 architectures as lineage anchors; BF-M lineage is Atelier+Foundry hybrid per §1 above. | architectures/v3/candidate-registry.md |
| §5.1.2 failure-mode coverage matrix | `absorbed` | F1-F20 preserved + extended; covered cell-wise in §10. | architectures/v3/failure-modes-v3.md |
| §5.1.3 when-to-pick-which decision criteria | `absorbed (with adaptation)` | v3 mandate-fit matrix (DEC-2) fulfills decision-criteria per-(architecture × work-unit-class). BF-M's mandate-fit cells per §5 are the per-candidate manifestation. | architectures/v3/mandate-fit-matrix.md + specs/bf-m.md §5 |
| §5.1.4 hybrid recommendations | `not-applicable-to-candidate-mandate` | BF-M is mandate-specific (brownfield-only); hybrid recommendations are unified-attempt territory (U-A/U-B/U-C/D7-U-1). | — |
| §5.1.5 shared infrastructure enumeration | `absorbed` | v3 common-substrate ADRs 0010-0017 + 0031/0032 are the shared-infrastructure enumeration BF-M binds wholesale. | specs/bf-m.md §2 + ADRs 0010-0017 |
| §5.1.6 shared roles, different emphasis | `absorbed (with adaptation)` | BF-M §4 binds all 10 disciplines; methodology-first shape gives emphasis at stage 3 (intent) + stage 6 (cross-model review) + stage 7 (perimeter). | specs/bf-m.md §4 |
| §5.1.7 Compound Atelier baseline | `rejected (explicitly-anchor-avoided, see archive-and-rebuild discipline)` | **Known-rejected v3 item** per Reviewer 6 D-H8 + UC6. v3 treats all candidates as independent; no baseline. | — |
| §5.1.8 selective borrows | `rejected (subsumed by v3 multi-candidate scoping principle)` | "Selective borrows" presupposes a baseline; v3 has none. | — |
| §5.1.9 build shared infrastructure first | `absorbed` | v3 Phase-5 common-substrate ADRs (0010-0017) precede candidate-specific Phase-6 work — direct match. BF-M binds the full common set. | docs/adr/0010-0017 + Phase-5 sequencing |

### §5.3 Notes

The two known-rejected items (§5.1.7 Atelier baseline + §5.1.8 selective borrows) both fire here per the archive-and-rebuild discipline. The 4-architecture taxonomy (§5.1.1) is the source of BF-M's Atelier+Foundry hybrid lineage statement in §1. BF-M's high-primitive-count substrate (~13 references per [Phase-4.1 coverage row](../primitives/index.md#per-candidate-primitive-coverage-round-trip-check)) is a *feature* of methodology-first per [BF-M substrate-requirements summary](../substrate-requirements/bf-m.md) — each stage names what it needs at its boundary, not a substrate-bloat signal.

## §6 — archive/architectures-v2/01-specification-refinery.md

### §6.0 File header

v2 Architecture 1 — Specification Refinery. "The spec is the product; the implementation is a probe." Layered spec discipline + revelation cycle + 5-mode failure classification. 3572 words. **BF-M's secondary v2-lineage** per §1 overview (the change-intent block at stage 3 is Refinery-inherited).

### §6.1 Enumeration

- §6.1.1 (claim) §1 Core thesis: spec is the durable artifact; implementation is a probe.
- §6.1.2 (primitive) §2 Artifact stack: layered specs (L1 vision / L2 capability / L3 behavioral / L4 implementation / L5 trajectory).
- §6.1.3 (primitive) §2.1 Stable identifier discipline.
- §6.1.4 (primitive) §4 The revelation cycle (Phases 1-7).
- §6.1.5 (framing) §4.4 Diagnostic analysis (5-mode failure classification: hallucination / spec-gap / implementation-error / model-drift / methodology-mismatch).
- §6.1.6 (primitive) §6.1 The manager loop.
- §6.1.7 (primitive) §6.3 Showboat-style trajectory artifacts.
- §6.1.8 (recommendation) §10 Implementation roadmap.

### §6.2 Per-item classification

| Item | Verdict | Rationale (≤25 words) | v3 cite (if absorbed) |
|---|---|---|---|
| §6.1.1 spec is durable artifact | `challenged (per §1.5)` | BF-M challenges D-1: spec-the-change-not-the-system. Per-cycle change-intent block, not whole-system spec. | specs/bf-m.md §3 + §5 |
| §6.1.2 5-layer spec stack | `not-applicable-to-candidate-mandate` | BF-M change-intent block is single-layer (rationale / invariants / acceptance / regression / blast / rollback). 5-layer is Refinery-flavored. | — |
| §6.1.3 stable identifier discipline | `absorbed` | BF-M §3 stage 8 P-04 PR creator emits typed PR-body block with required `cycle_id` + `agent_id` + per-symbol traceability via P-22. | specs/bf-m.md §2 P-04 + §3 stage 8 |
| §6.1.4 revelation cycle (7-phase) | `not-applicable-to-candidate-mandate` | Refinery-specific cycle structure; BF-M has its own 8-stage cycle. | — |
| §6.1.5 5-mode failure classification | `tbd` | Whether BF-M's F-mode coverage (per [track §2.5](../tracks/brownfield-methodology-first.md#25-failure-mode-coverage-severity-by-stage)) replicates / extends / supersedes the 5-mode classification is a Phase-8 lean-eval question. | — |
| §6.1.6 manager loop | `absorbed (with adaptation)` | BF-M §4 three-loop discipline (ADR 0026): plan → work → review → compound. Patrol-tier as meta-loop closure via P-06. | specs/bf-m.md §4 three-loop |
| §6.1.7 showboat trajectory artifacts | `absorbed (with adaptation)` | BF-M binds trajectory at P-05 substrate; the stage-8 PR body is the trajectory-pointer surface (F42 re-entry). Refinery's role-as-artifact analogue. | specs/bf-m.md §2 P-05 + §3 stage 8 |
| §6.1.8 implementation roadmap | `not-applicable-to-candidate-mandate` | Architecture-specific deployment; v3 doesn't carry per-architecture roadmaps. | — |

### §6.3 Notes

BF-M inherits the change-intent-block-as-structured-spec idea from Refinery's spec-discipline framing (Refinery's spec format is layered + DOT-capable; BF-M's change-intent block is a per-cycle structured-fields contraction of El Kaim's 9-field intent). Refinery's 5-layer spec stack itself is N/A — BF-M's single-layer change-intent block IS the deliberate brownfield-contraction. The D-1 challenge per §1.5 fires here.

## §7 — archive/architectures-v2/02-compound-atelier.md

### §7.0 File header

v2 Architecture 2 — Compound Atelier. "Each unit of work makes the next easier." Queue + workpad + persona panel + accumulated `docs/solutions/`. v2's recommended baseline. 4515 words. **BF-M's primary v2-lineage component (jointly with Foundry)** per §1 overview.

### §7.1 Enumeration

- §7.1.1 (claim) §1 Core thesis: each unit of work makes the next easier (compounding).
- §7.1.2 (primitive) §2 Compounding mechanism: knowledge accumulation between cycles.
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
| §7.1.1 compounding core thesis | `absorbed (with adaptation)` | BF-M compounds via the typed PR-body block (change-intent + brief + trajectory) + knowledge-promotion four-way classification at §4. Each cycle's PR feeds next cycle's stage-2 read. | specs/bf-m.md §3 stage 8 + §4 knowledge-promotion |
| §7.1.2 knowledge accumulation between cycles | `absorbed (verified at §3.1.5)` | Already absorbed via §3.1.5; BF-M binds at followup/11 four-way classification + `kw:confidence` tagging. | specs/bf-m.md §4 |
| §7.1.3 artifact stack (specs/knowledge/workpad) | `absorbed (with adaptation)` | BF-M stack: change-intent block (per-cycle, not spec) + PR body history (cross-cycle knowledge) + P-03 worktree (workpad). | specs/bf-m.md §2 P-03 + §3 stage 3/5/8 |
| §7.1.4 workshop chain (persona workshops) | `absorbed (with adaptation)` | BF-M's 8 stages ARE the workshop chain — each stage is a named obligation (comprehension / intent / plan / build / review / acceptance / ship). Not persona-typed but stage-typed. | specs/bf-m.md §3 cycle stages 1-8 |
| §7.1.5 researcher fan-out | `tbd` | Stage 4 N≥3 candidate plans is fan-out-shaped but bounded; whether Atelier's broader researcher fan-out applies at stage 2 (Comprehension) is Phase-8 lean-eval territory. | — |
| §7.1.6 reviewer panel | `absorbed (with adaptation)` | BF-M stage 6 cross-model reviewer + specialized critics (code-quality / security / conformance per Anthropic Auto-Review pattern). F46 mitigation. | specs/bf-m.md §3 stage 6 + §4 bias-guard |
| §7.1.7 synthesis and curation | `absorbed (with adaptation)` | BF-M's knowledge-promotion at §4 + the next-reader-check inversion (F8) is BF-M's curation choice — different from Atelier's curator-daemon. | specs/bf-m.md §4 knowledge-promotion |
| §7.1.8 conductor orchestrator | `absorbed (with adaptation)` | BF-M's cycle harness IS the conductor (stage sequencing + stage-compression by work-unit-class). Vendor-deferred at boundaries. | specs/bf-m.md §1 axis + §3 cycle |
| §7.1.9 workpad protocol | `absorbed (with adaptation)` | BF-M P-03 worktree isolation (ADR 0045 orphan) at stage 5 IS the workpad protocol; per-cycle ref namespace prevents sibling-collision. | specs/bf-m.md §2 P-03 + §3 stage 5 |
| §7.1.10 tiered cycle scope | `absorbed` | BF-M per-work-unit-class stage compression IS tiered cycle scope. regression-fix narrow + deep; codebase-evolution-proposal broad + shallow. | specs/bf-m.md §3 work-unit polymorphism |
| §7.1.11 severity × autofix axes | `absorbed (silently — flagged for auditor)` | The orthogonal-axes framing likely informed DEC-2 mandate-fit-per-(architecture × work-unit-class) schema. Not explicitly cited in BF-M spec. | — (flagged for silent-absorption auditor) |
| §7.1.12 residual work gate | `absorbed (with adaptation)` | BF-M stage 8 ship-or-escalate IS the residual-work gate. Escalation triggers (regression severity / blast radius / novel risk / F56 stress-bypass) are the gate criteria. | specs/bf-m.md §3 stage 8 |
| §7.1.13 three memory tiers | `tbd` | BF-M doesn't explicitly invoke Brier pace-layers; whether the followup/11 four-way knowledge classification subsumes the 3-tier framing is a Phase-8 question. | — |
| §7.1.14 implementation roadmap | `not-applicable-to-candidate-mandate` | Architecture-specific deployment. | — |

### §7.3 Notes

BF-M's Atelier inheritance is **structural** (8-stage cycle = workshop chain; PR body = compounding artifact; P-03 worktree = workpad; per-work-unit-class compression = tiered ceremony) but not **personnel** (BF-M is stage-typed not persona-typed). The silent-absorption flag on §7.1.11 (severity × autofix) is the same cross-spec audit point flagged in the BF-S exemplar — DEC-2's orthogonal-axes pattern likely inherits from Atelier §6.2.

## §8 — archive/architectures-v2/03-phase-gated-foundry.md

### §8.0 File header

v2 Architecture 3 — Phase-Gated Foundry. "Pre-agile structured methodologies become the right shape when agents make them fast." Phase-bound experts, formal templates (SRS, SAD, DD), RTM, gate boards. 4610 words. **BF-M's primary v2-lineage component (jointly with Atelier)** per §1 overview.

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
| §8.1.1 structured pre-agile core thesis | `absorbed (with adaptation)` | BF-M's 8-stage cycle IS structured methodology made agent-fast. "Methodology cycle IS the architecture" per §3 distinctive decision 1. | specs/bf-m.md §1 axis + §3 |
| §8.1.2 phase model + V&V pairing | `absorbed (with adaptation)` | BF-M stages 5-6-7 (Build / Cross-model review / Acceptance) are the V&V triad. Stage refuses-to-advance enforces phase-gating substrate-side. | specs/bf-m.md §3 stages 5-7 + distinctive decision 3 |
| §8.1.3 Configuration Management discipline | `absorbed (with adaptation)` | BF-M P-04 PR creator + F14 attribution trailers + typed Pydantic PR body = CM substrate analogue. Per-cycle agent_id / model_snapshot / trajectory_pointer required. | specs/bf-m.md §2 P-04 + §3 stage 8 |
| §8.1.4 defect-of-origin table | `absorbed (with adaptation)` | P-23 dependency-impact graph (ADR 0031) at stage 2 + P-22 codebase index (ADR 0017) + P-05 trajectory provide defect-of-origin traceability via blast-radius compute. | specs/bf-m.md §2 + §3 stage 2 |
| §8.1.5 RUP-style discipline × phase matrix | `not-applicable-to-candidate-mandate` | Foundry-specific matrix; BF-M binds all 10 disciplines uniformly via §4 with per-stage emphasis (intent at 3, review at 6, perimeter at 7). | — |
| §8.1.6 iteration within phases | `absorbed (with adaptation)` | BF-M cycle MAY loop stages 2-4 for `codebase-evolution-proposal` work-unit-class (per §3 stage 4). Bounded iteration is per-work-unit-class. | specs/bf-m.md §3 stage 4 |
| §8.1.7 V&V-side independent roles + different model family | `absorbed (verified)` | BF-M §3 stage 6: "Distinct-model reviewer (F46 mitigation per CJ Hess kevin/carl)" + P-14 cross-family routing (ADR 0016) enforces structural independence. | specs/bf-m.md §3 stage 6 + §4 bias-guard |
| §8.1.8 CM as spine | `absorbed (verified)` | BF-M §3 distinctive decision 3: "Stage obligations are substrate-enforced, not operator-voluntary" — F14 attribution mechanical, PR-body required-fields, perimeter check substrate-run. The PR body IS the CM spine. | specs/bf-m.md §3 distinctive decision 3 + §4 honesty |

### §8.3 Notes

BF-M's Foundry inheritance is **deep** — the 8-stage cycle is structurally Foundry's phase-bound-V&V-pairing shape applied at per-cycle granularity, with the CM-as-spine framing realized as the typed PR body. The Foundry-specific RUP matrix (§8.1.5) is N/A because BF-M binds disciplines per-stage rather than per-discipline-per-phase. Two cells verified-absorbed (V&V independence at §8.1.7; CM-as-spine at §8.1.8) — these are the substrate-enforcement decisions BF-M explicitly inherits from Foundry framing.

## §9 — archive/architectures-v2/04-evolutionary-tournament.md

### §9.0 File header

v2 Architecture 4 — Evolutionary Tournament. "The factory does not specify the right answer; it sets up the conditions under which the right answer wins." Genome library, predator agent, tournament bracket, model-family diversity. 4279 words.

### §9.1 Enumeration

- §9.1.1 (claim) §1 Core thesis: population + selection pressure + lineage.
- §9.1.2 (primitive) §3 Genome structure (spec sketch + scoring rubric + scenario corpus + diversity policy + termination criteria).
- §9.1.3 (primitive) §3.4 Diversity policy (model-family diversity as structural).
- §9.1.4 (primitive) §4 Generation cycle (commission / produce / score / select / close).
- §9.1.5 (primitive) §5.3 Predator agent (continuous adversarial pressure).
- §9.1.6 (primitive) §7 Loops within loops (generation / tournament / meta).
- §9.1.7 (framing) §6.3 Independence policy (structural independence between competing genomes).
- §9.1.8 (recommendation) §10 Scaling.

### §9.2 Per-item classification

| Item | Verdict | Rationale (≤25 words) | v3 cite (if absorbed) |
|---|---|---|---|
| §9.1.1 population + selection core thesis | `absorbed (with adaptation)` | BF-M stage 4 binds N≥3 candidate plans with explicit trade-offs (Klaassen four-clause plan-prompt) + per-plan adversarial critic. Population-of-plans within-cycle, not population-of-architectures. | specs/bf-m.md §3 stage 4 |
| §9.1.2 genome structure | `not-applicable-to-candidate-mandate` | Tournament-specific artifact at architecture scope; BF-M's analogue is the change-intent block (per-cycle), differently shaped. | — |
| §9.1.3 model-family diversity as structural | `absorbed (with adaptation)` | BF-M §3 stage 6 + §4 bias-guard bind cross-model-family judging as structural via P-14 judge router. F46 mitigation. | specs/bf-m.md §3 stage 6 + §4 |
| §9.1.4 generation cycle | `not-applicable-to-candidate-mandate` | Tournament-specific multi-genome shape. | — |
| §9.1.5 predator agent | `rejected (subsumed by stage-7-perimeter + stage-6-cross-model-review)` | BF-M substitutes Tournament's predator-agent with stage-7 deterministic perimeter (P-12 + Ashby-aware check) + stage-6 cross-model reviewer. Static perimeter + per-cycle adversarial review, not continuous predator. | — |
| §9.1.6 loops within loops | `absorbed (with adaptation)` | BF-M §4 three-loop discipline (ADR 0026) + Patrol-tier meta-loop via P-06 is the analogue (3 levels not 3-tournament-levels). | specs/bf-m.md §4 three-loop |
| §9.1.7 independence policy | `absorbed` | BF-M stage 6 cross-model judge enforces builder-judge independence; P-14 routing is structural. | specs/bf-m.md §3 stage 6 + §4 |
| §9.1.8 scaling | `tbd` | BF-M §6 carries OQ-T6 brownfield regime ceiling measurability + OQ-T10 instruction-following ceiling vs change-intent block size — Tournament's scaling lessons may inform. | — |

### §9.3 Notes

Tournament's primary primitives (population, predator, tournament bracket) are N/A or rejected at architecture scope; the cross-model-family diversity (§9.1.3) and independence policy (§9.1.7) land at BF-M's stage 6 — same substrate (P-14) as BF-S. Predator-agent (§9.1.5) is explicitly rejected with reason: BF-M's stage-7 deterministic perimeter + stage-6 per-cycle adversarial review substitute for continuous predator pressure. **F52 explicit-forbidden architecturally** is BF-M's distinctive negative inheritance — per [BF-M §3 distinctive decision 2](../specs/bf-m.md#3-methodology-shape): "Tempting-wrong-hybrid (F52) explicitly forbidden architecturally" (no deterministic wrappers around LLM stages mid-pipe; deterministic checks ONLY at stage-7 perimeter).

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
| §10.1.1 F1 Hallucination | `absorbed` | BF-M §3 stage 6 cross-model review (F46-related) + §4 bias-guard (ADR 0018) + P-14 routing closes F1. | specs/bf-m.md §3 stage 6 + §4 |
| §10.1.2 F2 Reward hacking | `absorbed` | BF-M §4 holdout (ADR 0021) + stage-5/stage-7 air-gap; codebase-derived unseen subset prevents reward-hacking-by-overfit. | specs/bf-m.md §3 stage 5/7 + §4 holdout |
| §10.1.3 F3 Spec-completeness | `absorbed (with adaptation)` | BF-M change-intent block enforces required fields (rationale / invariants / acceptance / regression / blast / rollback); P-12 GtWR R7/R8/R9 vocab lint at stage 3. | specs/bf-m.md §3 stage 3 |
| §10.1.4 F4 Code quality | `absorbed (with adaptation)` | BF-M stage 6 specialized critics for code-quality (Anthropic Auto-Review pattern) + stage 7 P-12 linters + P-23 blast-radius. | specs/bf-m.md §3 stage 6/7 |
| §10.1.5 F5 Cognitive ceiling | `absorbed (with adaptation)` | BF-M per-stage lights-out + escalation triggers at stage 8 (F56 stress-bypass detection) bound the operator cognitive load. Per-stage not whole-system. | specs/bf-m.md §3 vocabulary-mapping + stage 8 |
| §10.1.6 F6 Cognitive debt | `absorbed` | BF-M §2 P-05 trajectory + §4 cognitive-escrow binding (ADR 0019); PR body IS the F42 cognitive-escrow re-entry surface. | specs/bf-m.md §2 + §4 cognitive-escrow |
| §10.1.7 F7 Normalization of deviance | `absorbed (with adaptation)` | BF-M P-06 Patrol-tier across cycles (F34/F54/F55/F57 drift) + substrate-enforced stage refuses-to-advance (F53 mitigation). | specs/bf-m.md §2 + §3 distinctive decision 3 |
| §10.1.8 F8 Stale knowledge | `absorbed (with adaptation)` | BF-M §4 knowledge-promotion: stale-knowledge inversion is next-reader's per-write check, not curator daemon. Deliberate per OQ-9. | specs/bf-m.md §4 knowledge-promotion + §6 |
| §10.1.9 F9 Spec overfitting | `not-applicable-to-candidate-mandate` | Spec-overfitting is whole-system-spec-discipline concern; BF-M change-intent block is per-cycle, not whole-system. | — |
| §10.1.10 F10 Findings disappear | `absorbed` | BF-M stage 8 typed PR body + F14 attribution trailers + P-05 trajectory pointer ensures findings persist machine-readably. | specs/bf-m.md §3 stage 8 + §2 P-04 |
| §10.1.11 F11 Renumbering | `absorbed` | BF-M §2 P-22 polyglot codebase index + P-04 typed PR-body block carries `cycle_id` + stable references. | specs/bf-m.md §2 + §3 stage 8 |
| §10.1.12 F12 Lethal trifecta | `absorbed (verified)` | BF-M §4 trifecta-closure binding: "F12 → F33 → F44 cascade closed at the substrate by capability-typed dataflow" (P-25 CaMeL ADR 0033). | specs/bf-m.md §4 trifecta-closure + ADR 0033 |
| §10.1.13 F13 Missing-config | `absorbed (with adaptation)` | BF-M stage 2 P-23 dependency-impact graph compute + P-22 codebase index surface config-dependency drift at the brief-generation step. | specs/bf-m.md §2 P-23 + §3 stage 2 |
| §10.1.14 F14 Attribution collapse | `absorbed (verified)` | BF-M §4 honesty binding: "PR-body schema — required fields (agent_id, model_snapshot, acceptance_verdict) cannot be omitted; F14 attribution is mechanical." | specs/bf-m.md §4 honesty + §3 stage 8 |
| §10.1.15 F15 Single-prompt collapse | `absorbed (with adaptation)` | BF-M stage 4 N≥3 candidate plans + per-plan adversarial critic + stage 6 cross-model review substitute for Atelier's six-divergent-frames. | specs/bf-m.md §3 stage 4/6 |
| §10.1.16 F16 Resume-fidelity | `absorbed` | BF-M P-05 trajectory + stage-8 PR-body trajectory pointer + cycle_id provide resume anchor. F42 cognitive-escrow re-entry. | specs/bf-m.md §3 stage 8 + §4 cognitive-escrow |
| §10.1.17 F17 Parallel agents on shared dirs | `absorbed (verified)` | BF-M P-03 worktree isolation (ADR 0045 orphan) substrate-enforces F17 closure at stage 5; per-cycle ref namespace + tmpfs-mounted ephemeral checkouts. | specs/bf-m.md §2 P-03 + §3 stage 5 |
| §10.1.18 F18 Prose-spec rigor | `absorbed (with adaptation)` | BF-M change-intent block is structured-fields not prose; P-12 GtWR R7/R8/R9 vocab lint at stage 3 enforces field-rigor. | specs/bf-m.md §3 stage 3 |
| §10.1.19 F19 Model-floor dependency | `absorbed` | BF-M §4 bias-guard cross-model judging via P-14 surfaces model-floor explicitly per F46. OQ-T2 carry on cross-model necessity. | specs/bf-m.md §4 bias-guard + §6 OQ-T2 |
| §10.1.20 F20 Maintenance asymmetry | `absorbed (with adaptation)` | BF-M cycle is work-unit-class-polymorphic: regression-fix / refactor / post-mvp-evolution all routed through same 8-stage with per-class compression. | specs/bf-m.md §3 work-unit polymorphism + §5 |
| §10.1.21 A1 Refinery coverage row | `not-applicable-to-candidate-mandate` | Coverage row characterizes Architecture 1, not BF-M. Informational only. | — |
| §10.1.22 A2 Atelier coverage row | `not-applicable-to-candidate-mandate` | Coverage row characterizes Architecture 2 (one of BF-M's lineage components); ★★★★★ scoring is per-Atelier, not per-BF-M. BF-M's own F-mode coverage tracked above. | — |
| §10.1.23 A3 Foundry coverage row | `not-applicable-to-candidate-mandate` | Coverage row characterizes Architecture 3 (BF-M's other lineage component); informational only. | — |
| §10.1.24 A4 Tournament coverage row | `not-applicable-to-candidate-mandate` | Coverage row characterizes Architecture 4. | — |

### §10.3 Notes

19-of-20 F-modes absorbed (F1-F8, F10-F20); F9 N/A-to-candidate (spec-overfitting whole-system framing inapplicable to per-cycle change-intent block). F12 + F14 + F17 verified-absorbed with explicit BF-M spec invocations (F12 at §4 trifecta-closure via P-25 ADR 0033; F14 at §4 honesty via P-04 PR-body required-fields; F17 substrate-closed at P-03 worktree isolation orphan ADR 0045). The 4 per-architecture coverage-strength rows are informational characterizations of the v2 architectures, not BF-M-actionable items — but note BF-M inherits structural framing from two of them (Atelier §10.1.22 + Foundry §10.1.23) per the hybrid-lineage statement in §1. No `tbd` rows in §10 — BF-M's F-mode coverage is well-bound by the spec.

## §11 Summary

**Per-token cell counts (matches YAML frontmatter):**

| Token | Count |
|---|---|
| `absorbed` (incl. with-adaptation, verified, silently) | 69 |
| `rejected (reason)` | 5 |
| `not-applicable-to-candidate-mandate` | 16 |
| `challenged` (D-default challenges + Refinery-D-1 cross-ref) | 3 |
| `tbd` | 5 |
| **Total (per-archive-file classification cells, §2.2-§10.2)** | **98** |

(Tally matches: §2.2 (3) + §3.2 (16) + §4.2 (8) + §5.2 (9) + §6.2 (8) + §7.2 (14) + §8.2 (8) + §9.2 (8) + §10.2 (24) = 98. The §1.5 D-default verification subsection contributes a separate 7 cells (5 `absorbed (verified at §1.5)` + 2 `challenged`); these are referenced by `(per §1.5)` annotations in §3.2 / §4.2 / §6.2 to preserve traceability without double-counting at the per-archive-file level. Silent-absorption auditor uses §2.2-§10.2 table-row counts as canonical.)

**High-confidence absorbed cells:** D-3, D-4, D-5, D-6, D-7 (verified per §1.5); F12 + F14 + F17 (verified at BF-M §4 + §2 with explicit ADR cites); CM-as-spine (§8.1.8 verified) + V&V independence (§8.1.7 verified).

**Load-bearing challenges (NOT silent rejections):**

- **D-1 challenged**: spec-the-change-not-the-system. Per BF-M §3 distinctive methodology decision + §5 post-mvp-evolution row.
- **D-2 challenged**: codebase-derived holdout (unseen subset, not out-of-tree). Per BF-M §3 stage 7 + §4 holdout binding (CTR-B5 inversion).

These are the two deliberate departures from synthesis-v1-v2 defaults; both explicitly cited and reasoned in the BF-M spec.

**Surfaced TBDs (5 cells; require lead-agent reconciliation or Phase-8 follow-up):**

1. §4.1.6 falsified consensus items — needs per-item review of what was falsified vs preserved in v3 BF-M context.
2. §6.1.5 Refinery 5-mode failure classification — Phase-8 lean-eval candidate.
3. §7.1.5 Atelier researcher fan-out at stage 2 (Comprehension) applicability — Phase-8 lean-eval question.
4. §7.1.13 Atelier 3 memory tiers vs BF-M's followup/11 four-way knowledge classification — Phase-8 question on subsumption.
5. §9.1.8 Tournament scaling lessons (BF-M §6 OQ-T6 + OQ-T10 may benefit).

**Silent-absorption auditor flags (for cross-spec reconciliation):**

- §3.1.16 cross-cutting primitives (v3 `primitives/index.md` inheritance — same flag as BF-S exemplar).
- §7.1.11 severity × autofix orthogonal axes (likely informed DEC-2 schema — same flag as BF-S exemplar).

**Known-rejected items confirmed:**

- §4.1.10 OpenHands+Overstory substrate stack — `rejected (explicitly-excluded-per-constraints-extracted)`.
- §5.1.7 Compound Atelier as baseline — `rejected (explicitly-anchor-avoided)`.
- §5.1.8 Selective borrows — `rejected (subsumed by v3 multi-candidate scoping principle)`.
- §9.1.5 Tournament predator agent — `rejected (subsumed by stage-7-perimeter + stage-6-cross-model-review)`.

**BF-M-specific framing acknowledgements (no per-variant ADR claims):**

- BF-M does NOT claim any framework ADR (no P-19 / P-28 / P-29 / P-30) per [BF-M §0 framework-ADR pairing annotation](../specs/bf-m.md#0-adr-citation-index). Consequently no §N.3 ADR-0036 framing characterization is required for BF-M (per [auto-007 §N.3 amendment](../decisions/auto-007-phase-7-dispatch-shape.md#decision-round-2) — that framing applies only to BF-L / U-A / D7-U-1).
- BF-M's 2-candidate-fold ADRs (0033 P-25 with BF-S; 0034 P-27 with BF-L) and 2 orphan ADRs (0045 P-03 worktree; 0046 P-04 PR creator) are the BF-M-specific substrate inheritances.

## §12 References

**BF-M spec + supporting docs:**

- [`architectures/v3/specs/bf-m.md`](../specs/bf-m.md) — BF-M Phase-6 architecture spec (audit input).
- [`architectures/v3/candidate-registry.md` BF-M entry](../candidate-registry.md#bf-m--brownfield-methodology-first) — registry entry for §1 lineage statement.
- [`architectures/v3/substrate-requirements/bf-m.md`](../substrate-requirements/bf-m.md) — substrate-requirements summary (high-primitive-count rationale).
- [`architectures/v3/tracks/brownfield-methodology-first.md`](../tracks/brownfield-methodology-first.md) — Phase-3.5 BF-M track sketch.
- [`architectures/v3/decisions/auto-007-phase-7-dispatch-shape.md`](../decisions/auto-007-phase-7-dispatch-shape.md) — Phase-7 dispatch brief.
- [`architectures/v3/backfill-notes/bf-s.md`](./bf-s.md) — Phase-7 exemplar (shape template).

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

**ADRs cited (BF-M-specific):**

- Common substrate: [ADR 0010](../../../docs/adr/0010-p-01-sandbox-runtime.md), [ADR 0011](../../../docs/adr/0011-p-02-cost-ceilings.md), [ADR 0012](../../../docs/adr/0012-p-05-trajectory-capture.md), [ADR 0013](../../../docs/adr/0013-p-06-watchdog-tiers.md), [ADR 0014](../../../docs/adr/0014-p-07-telemetry-ingestor.md), [ADR 0015](../../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md), [ADR 0016](../../../docs/adr/0016-p-14-judge-router.md), [ADR 0017](../../../docs/adr/0017-p-22-polyglot-codebase-index.md).
- Designed-system common: [ADR 0031 (P-23)](../../../docs/adr/0031-p-23-dependency-impact-graph.md), [ADR 0032 (P-12)](../../../docs/adr/0032-p-12-deterministic-linter-framework.md).
- 2-candidate-fold: [ADR 0033 (P-25, with BF-S)](../../../docs/adr/0033-p-25-camel-perimeter.md), [ADR 0034 (P-27, with BF-L)](../../../docs/adr/0034-p-27-archaeological-brief-tooling.md).
- Orphan (BF-M-only): [ADR 0045 (P-03)](../../../docs/adr/0045-p-03-worktree-isolation.md), [ADR 0046 (P-04)](../../../docs/adr/0046-p-04-pr-creator.md).
- Discipline: [ADRs 0018-0027](../../../docs/adr/).

**Constraints / decisions:**

- [`architectures/v3/constraints-extracted.md`](../constraints-extracted.md) — UC1-UC8 user constraints (source of known-rejected v3 item flags).
- [`architectures/v3/decisions-captured.md`](../decisions-captured.md) — DEC-1 / DEC-1.a / DEC-2 etc.
- [`AGENTS.md`](../../../AGENTS.md) — framework-ADR scope discipline (AGENTS-MD-a9fb7b42f8) does NOT bind BF-M.
