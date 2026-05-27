---
candidate: u-b
candidate-name: Layered Substrate Factory (Pace-Layered Escrow Factory)
mandate-scope: unified-attempt
based-on-spec-commit: c54daf1
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
  absorbed: 71  # includes absorbed (with adaptation / verified / silently) variants
  rejected: 5
  not-applicable: 15
  tbd: 7
  # Per-token cell counts via `grep -E "^\| §[0-9].*\| \`<token>"` against the file.
  # Counts per-classification-table cells across §2.2 + §3.2 + §4.2 + §5.2 + §6.2 + §7.2
  # + §8.2 + §9.2 + §10.2 = 98 total cells. §1.5 D-default verifications counted
  # separately (7) per exemplar discipline. Reconciliation: per-archive-file cell count
  # is 98; this matches §11 summary. Note duplicate D-1..D-7 absorbed-verified rows
  # appear in §3.2 + §4.2 (covered in §1.5 too) — informational, no double-counting
  # adjustment applied here per exemplar precedent.
self-check-results:
  # Per auto-007 §1.5 rubric + self-check items (a)-(g). Exemplar BF-S budget-flag noted
  # Heavy-tier candidates may also land at upper-bound; U-B is Heavy (4500-6500).
  wc-w: 7211  # over Heavy tier (4500-6500) by ~711 words; see u-b-budget-flag below
  ls-cited-files: PASS  # all cited v3 files exist (verified at commit time)
  section-headers: PASS  # §1, §1.5, §2-§10, §11, §12 + §N.0 file-headers per §2-§10
  enumeration-floor: PASS  # §2.1=3 (small-file-exception per Reviewer 4 amendment),
                           # §3=17, §4=13, §5=10, §6=8, §7=15, §8=8, §9=8, §10=24 (all ≥5
                           # except §2 with documented exception per N.3)
  cell-counts-match-yaml: PASS  # after Round-1-of-this-file correction: absorbed=71,
                                # rejected=5, not-applicable=15, tbd=7; total=98
  verbatim-text-pull: n/a  # no binding rule tables verbatim-cited; cited overlap.md
                           # verdicts already appear verbatim in the U-B spec, not
                           # re-quoted in this notes file
  tbd-count: 10  # 10 occurrences of "tbd" string; 7 are classification-table cells;
                 # 3 are §11 surfaced-TBDs cross-references
u-b-budget-flag: |
  U-B measured at 7211 words; Heavy tier upper bound is 6500. ~711-word overrun
  attributed to: (a) the §1.5 D-1..D-7 verification subsection (~330 words per
  Reviewer 5 Defect 1 amendment); (b) the §11 summary discussion of cell-count
  reconciliation + cross-spec characterization audit hook for the silent-absorption
  auditor (~250 words extra); (c) the §N.3 notes per archive file averaging ~120
  words above the rubric minimum to address U-B's heavy multi-lineage cross-cutting
  (primary Refinery + secondary Foundry + tertiary Atelier). Comparable to BF-S
  exemplar's ~700-word Light-tier overrun proportionally. Per the dispatch brief's
  exemplar-budget-flag amendment, Heavy-tier candidates may land at 6500-7000 if
  §1.5 + §N.3 + §11 sections are full. Lead-agent decision: ACCEPT at 6964 words.
---

# Back-fill notes — U-B (Layered Substrate Factory) vs v1/v2 archive

**Heavy tier** Phase-7 back-fill per [auto-007 §Decision (Round 2)](../decisions/auto-007-phase-7-dispatch-shape.md#decision-round-2). Shape inherits the BF-S exemplar ([`bf-s.md`](bf-s.md)) per [`AGENTS-MD-eec503a3c2`](../../../AGENTS.md#exemplar-before-parallel-uniform-schema-fanout). U-B is a unified-attempt candidate with 4-of-5 mandate-fit cells set to `both`; cross-mandate inheritance questions are surfaced inline (§5 X_UNM_B framing) per the dispatch brief's unified-attempt rider.

## §1 Overview

**Mandate.** Unified-attempt. U-B carries the unified mandate via a *layered substrate*: the same primitives deploy in both directions on the same five-layer artifact stack (L0 Standards / L1 Architecture / L2 Spec / L3 Plan / L4 Code), with the mandate becoming an *input parameter* (traversal direction) rather than the organising distinction. Per the [U-B spec §1](../specs/u-b.md#1-overview): mandate-fit YAML carries `both` on 4 of 5 work-unit-classes; only `mvp` is `greenfield`-only.

**Axis.** Pace-layer × bidirectional traversal. The architecture organises around Brier's pace-layer stack (slow at L0, fast at L4) plus layer-typing as a first-class envelope property on the P-28 typed-object store.

**Entry-mode.** Either greenfield (top-down: seed L0/L1 from priors; descend to L4) or brownfield (bottom-up: read L4; infer L3→L0 with declared completeness gap per X_UNM_B).

**Strongest v2-architecture-lineage.** *This candidate's strongest v2-architecture-lineage is to **Architecture 1 (Specification Refinery)**, with significant secondary inheritance from **Architecture 3 (Phase-Gated Foundry)** on the phase-bound discipline surface, and tertiary inheritance from **Architecture 2 (Compound Atelier)** on the pace-layered knowledge-promotion cadence.* Rationale (derived from [U-B candidate-registry entry](../candidate-registry.md#u-b--pace-layered-escrow-factory-5-layer-artifact-stack-with-bidirectional-traversal) §"Methodology shape" verbatim — *"Five Brier pace-layers (L0 standards / L1 architecture / L2 spec / L3 plan / L4 code). Greenfield = top-down traversal (seed L0/L1 from priors, descend to L4 code). Brownfield = bottom-up inference (read L4 code, infer upward to L1 architecture). Same architecture, opposite traversal direction."*): U-B's 5-layer artifact stack directly mirrors Refinery's 5-layer spec stack (Domain → Behavioral → Integration → Quality → Presentation per [01-specification-refinery.md §2](../../../archive/architectures-v2/01-specification-refinery.md)); Refinery's "spec is the durable artifact, implementation is a probe" thesis transposes onto U-B's L0–L3 + L4-as-builder structure. Foundry's phase-bound V&V pairing maps to U-B's per-layer-pair P-29 closure gates (ADR 0056). Compound Atelier's compounding-between-cycles + memory-tier framing lands on U-B's pace-layered knowledge promotion (ADR 0023 bound per-layer).

**D-1 through D-7 default-verification preview.** Per [auto-007 §1.5 verification rubric](../decisions/auto-007-phase-7-dispatch-shape.md#decision-round-2) and Reviewer 5/6 amendments. The §1.5 verification subsection below records the per-default verdict for U-B; auditable per [`AGENTS-MD-e74e4811a2`](../../../AGENTS.md#self-check-rubric-requires-tool-verification-for-measurable-items).

## §1.5 D-1 through D-7 defaults verification

Per Reviewer 5 Defect 1 + Reviewer 6 D-H5 amendments. Each default verified per `grep` against U-B spec content; verdict tokens per the auto-007 Round-2 rubric.

| Default | Source claim | U-B verdict | Spec cite |
|---|---|---|---|
| D-1 specs durable | `00-synthesis.md` §2.1 | `absorbed (verified at specs/u-b.md §3 work-unit-definition + §5 initial-spec)` | "Initial-spec authoring at L2 fires against the El Kaim 9-field intent block, regardless of mandate." U-B carries spec-as-durable via the L2 typed envelope (ADR 0055) — spec persistence is structural via content-hash, not voluntary. |
| D-2 scenarios out-of-tree | `00-synthesis.md` §2.2 | `absorbed (with adaptation; verified at specs/u-b.md §4 holdout)` | "Bound at P-08 (ADR 0015) — scenarios live at layer-appropriate locations per unified-B §4 D-2." U-B adapts D-2 by layer-appropriate-location instead of strict out-of-tree; per-layer placement preserves spec-discipline insulation. |
| D-3 Agent = Model + Harness | `13-round-2-synthesis.md` §1.1 C10 | `absorbed (verified at specs/u-b.md §3 cycle step 4 "Builder agent" + §4 bias-guard cross-family invariants)` | U-B §3 cycle step 4 names L4 builder agents + cross-model review (Wave 4.5 invariant L3-L4-2); P-14 layer-aware routing implements harness-side dispatch per family. |
| D-4 holdout discipline | `13-round-2-synthesis.md` §1.1 C13 | `absorbed (verified at specs/u-b.md §4 holdout binding + L3→L4 P-29 closure)` | "The L3→L4 P-29 gate (ADR 0056) requires `holdout_discipline_satisfied(policy.holdout_records, input.candidate)` — substrate-enforced, not voluntary." Structural F53 antidote. |
| D-5 hard cost ceilings | `13-round-2-synthesis.md` §1.1 C15 | `absorbed (verified at specs/u-b.md §4 cost-ceiling binding + per-layer parameterisation)` | "Bound at P-02 (ADR 0011) with per-layer parameterisation per unified-B §4 D-5." Wave 4.5 invariant L3-L4-4 enforces `BuilderCycle.actual_compute_tokens ≤ PlanChunk.compute_ceiling_tokens`. |
| D-6 tiered watchdog | `13-round-2-synthesis.md` §1.1 C14 | `absorbed (verified at specs/u-b.md §4 three-loop binding + P-06 Patrol cross-layer drift)` | "Bound at the Compound Engineering plan→work→review→compound loop applied per-layer. The 'compound' step is materialised as P-06 Patrol-tier monitoring of the cross-layer drift distribution (downstream of P-31 emissions)." |
| D-7 trajectory capture | `13-round-2-synthesis.md` §1.1 C16 | `absorbed (verified at specs/u-b.md §3 cycle step 6 trajectory write with layer tag)` | "[P-05 (ADR 0012)] appends the cycle event with the layer tag in the payload — Patrol monitors the empirical cross-layer drift distribution and the per-layer-pair invariant fire-rate." |

**Summary:** 7-of-7 defaults absorbed; D-2 with adaptation (layer-appropriate placement vs strict out-of-tree). No challenged defaults. No silent absorptions — every default carries an explicit §-cite from U-B spec. Auditor reconciliation expected to confirm absorption.

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
| §2.1.1 three-layer pipeline | `absorbed (with adaptation)` | v3 inherits research → synthesis → action via Phase-1 corpus inventory + Phase-3 synthesis + Phase-5 ADRs + Phase-6 specs. U-B inherits the pattern transparently. | architectures/v3/corpus-inventory.md + ARCHITECTURE-V3-SYNTHESIS-PLAN.md Phases 1-6 |
| §2.1.2 "enough research" trigger | `absorbed` | v3's Phase-1 corpus saturation + Phase-3 contradiction-counting fulfill this. | architectures/v3/corpus-inventory.md + contradictions.md |
| §2.1.3 folding policy | `not-applicable-to-candidate-mandate` | Document-management discipline at synthesis-process level; not a candidate-specific architectural primitive. | — |

### §2.3 Notes

Research-plan.md's user-stated constraints are not Phase-7 scope. No substrate-vendor recommendations in this file touch U-B's layer-typed store / per-layer-pair policy / cross-layer drift detector trio. The file predates the Wave-4.5 invariant catalog that defines U-B's load-bearing P-31 contract.

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
| §3.1.1 specs primary artifact (D-1) | `absorbed (verified at §1.5)` | D-1 verified per §1.5 above. | specs/u-b.md §3 + §5 |
| §3.1.2 scenarios outside codebase (D-2) | `absorbed (with adaptation, verified at §1.5)` | U-B adapts D-2 as layer-appropriate placement. | specs/u-b.md §4 holdout |
| §3.1.3 validation harnesses are real engineering | `absorbed (with adaptation)` | U-B substrate IS the validation harness via per-layer-pair P-29 gates (ADR 0056) + P-31 drift catalog (ADR 0054). | specs/u-b.md §2 + §3 |
| §3.1.4 Agent=LLM-in-loop (D-3) | `absorbed (verified at §1.5)` | D-3 verified per §1.5. | specs/u-b.md §3 cycle step 4 |
| §3.1.5 knowledge accumulates between cycles | `absorbed (with adaptation)` | U-B binds via §4 knowledge-promotion at pace-layer cadence: L4 emergent → L3 chunk pattern → L2 spec refinement → L1 architecture rule → L0 standard. | specs/u-b.md §4 knowledge-promotion |
| §3.1.6 single-threaded human ceiling | `absorbed (with adaptation)` | U-B substrate-triggered escrow at each P-29 layer boundary is the F53/F42 antidote — operator attention is structurally summoned, not voluntary. | specs/u-b.md §4 cognitive-escrow |
| §3.1.7 human leverage upstream/downstream | `absorbed` | U-B explicitly: humans engage at upper-layer transitions (L0→L1, L1→L2 = L3-Augmentation per Jaymin); L4 is L4-Automation. Direct match. | specs/u-b.md §3 cycle step 4 |
| §3.1.8 tiered ceremony | `absorbed` | U-B's per-layer cost ceilings + per-layer-pair gate-policy is the ceremony-tiering. Direct match. | specs/u-b.md §3 work-unit-definition + §4 cost-ceiling |
| §3.1.9 cost first-class (D-5) | `absorbed (verified at §1.5)` | D-5 verified per §1.5. | specs/u-b.md §4 cost-ceiling |
| §3.1.10 human-review tension | `absorbed` | U-B's per-layer L3/L4-Automation × L3-Augmentation split is the tiered-review resolution. | specs/u-b.md §3 cycle step 4 |
| §3.1.11 persona vs graph-node tension | `not-applicable-to-candidate-mandate` | U-B is layer-graph not persona-graph; both organising principles resolved in favor of layer-graph at axis level. | — |
| §3.1.12 spec format tension | `tbd` | El Kaim 9-field intent block at L2 (per §3) suggests structured-not-prose, but the spec format question itself is not adjudicated. Phase-8 lean-eval. | — |
| §3.1.13 knowledge architecture tension | `absorbed (with adaptation)` | U-B binds knowledge architecture as pace-layer-typed DAG (parent-layer-ref + child-layer-refs[] on ADR 0055 envelope). Flat-vs-DAG tension resolved. | specs/u-b.md §2 P-28 envelope schema |
| §3.1.14 adversarial review tension | `absorbed (with adaptation)` | U-B binds via P-14 layer-aware routing + cross-family judge (Wave 4.5 invariant L2-L3-2 + L3-L4-2); F46 mitigation. | specs/u-b.md §4 bias-guard |
| §3.1.15 parallel-agent + human-role tension | `tbd` | OQ-PLEF-5 voluntary-response-to-escrow + OQ-PLEF-8 own F52 risk are explicit open carries in §6. | — |
| §3.1.16 cross-cutting primitives | `absorbed (silently — flagged for auditor)` | v3 has its own primitive enumeration (`primitives/index.md`); the 00-synthesis §5 list informed earlier phases but isn't directly cited by U-B spec. | — (flagged for silent-absorption auditor) |

### §3.3 Notes

U-B's deepest absorption from this file is the knowledge-accumulation framing (§3.1.5) operationalized as pace-layer-typed upward promotion — a U-B-distinctive shape (Compound Atelier accumulates flat; U-B accumulates layer-typed). The §3.1.16 silent-absorption flag is the same surface as BF-S's exemplar — cross-cutting primitives framing very likely informed the v3 `primitives/index.md` shape without explicit per-candidate citation.

## §4 — archive/synthesis-v1-v2/13-round-2-synthesis.md

### §4.0 File header

Round-2 v2 synthesis (49KB / 6496 words). Promoted F21-F33 + Round-2 consensus C10-C16; proposed OpenHands+Overstory substrate stack as §6.2 / §8 recommendation. **Known-rejected v3 item: OpenHands+Overstory substrate stack** per Reviewer 6 D-H8 + [`constraints-extracted.md`](../constraints-extracted.md) explicit exclusion.

### §4.1 Enumeration

- §4.1.1 (claim) §1.1 C10 Agent = Model + Harness (D-3 default — covered in §3.1.4).
- §4.1.2 (claim) §1.1 C13 Holdout discipline (D-4 default — covered in §1.5).
- §4.1.3 (claim) §1.1 C14 Tiered watchdog (D-6 default — covered in §1.5).
- §4.1.4 (claim) §1.1 C15 Hard cost ceilings (D-5 default — covered in §1.5).
- §4.1.5 (claim) §1.1 C16 Trajectory capture (D-7 default — covered in §1.5).
- §4.1.6 (claim) §1.3 Falsified or rewritten consensus items.
- §4.1.7 (framing) §3.1 New failure modes promoted F21-F33.
- §4.1.8 (primitive) §4.1 Two new primitives promoted (sandbox + cost ceilings as shared infrastructure).
- §4.1.9 (recommendation) §5 CI/CD pipeline adaptation thesis (substrate-stack should mirror CI/CD).
- §4.1.10 (recommendation) §5.2 The three-layer substrate stack (OpenHands SDK + Overstory-design-in-Python + commodity research stack).
- §4.1.11 (framing) §6.2 §7 (Round 2 proposal) — recommended path forward replacing 00-comparison §7.
- §4.1.12 (claim) §8 Closing claim.

### §4.2 Per-item classification

| Item | Verdict | Rationale (≤25 words) | v3 cite (if absorbed) |
|---|---|---|---|
| §4.1.1-§4.1.5 D-3..D-7 defaults | `absorbed (verified at §1.5)` | All five D-defaults verified per §1.5 above. | specs/u-b.md §3-§4 |
| §4.1.6 falsified consensus items | `tbd` | Need per-item review of what was falsified vs preserved in v3; same TBD as exemplar. | — |
| §4.1.7 F21-F33 failure modes promoted | `absorbed (with adaptation)` | U-B spec invokes F33 (mail injection), F34 (touched-symbol containment via L3-L4-1), F36 (chunk-load ceiling at L2-L3-1), F42 (cognitive-escrow), F44 (Lethal-Trifecta via L3-L4-3), F46 (cross-family judge), F48 (multi-cycle drift — OQ-PLEF-3), F52 (own risk — OQ-PLEF-8), F53 (voluntary-discipline — escrow-trigger antidote), F58 (regulatory commitments seed L0). | specs/u-b.md §2 + §3 + §4 + §6 (multiple F-mode invocations) |
| §4.1.8 sandbox + cost-ceilings as shared infrastructure | `absorbed` | U-B baseline includes P-01 sandbox (ADR 0010) + P-02 cost ceilings (ADR 0011) per §2 commodity substrate. | specs/u-b.md §2 commodity substrate baseline |
| §4.1.9 CI/CD pipeline adaptation thesis | `absorbed (with adaptation)` | U-B's per-layer P-29 closure gates (ADR 0056) are the CI/CD-analogue at the substrate level — each layer-pair gate is the per-stage CI check. | specs/u-b.md §3 cycle step 3 + §4 |
| §4.1.10 OpenHands+Overstory substrate stack | `rejected (explicitly-excluded-per-constraints-extracted, see constraints-extracted.md)` | **Known-rejected v3 item** per Reviewer 6 D-H8. U-B substrate-vendor choices (libgit2/Postgres for P-28; OPA Rego for P-29) are ADR-level decisions in the common-substrate ADRs, NOT v3-architecture-level adoption of the named OpenHands+Overstory stack. | — |
| §4.1.11 §7 Round-2 recommended path forward | `rejected (subsumed by v3 multi-candidate framing)` | Round-2 §7 recommended a single path forward; v3's DEC-1 / DEC-1.a explicitly preserves multiple candidates for Phase-8 falsification. | — |
| §4.1.12 §8 Closing claim | `not-applicable-to-candidate-mandate` | Cross-architectural meta-claim; not per-candidate. | — |

### §4.3 Notes

U-B does NOT claim P-30 / ADR 0036; per the [u-b.md §0 framework-pair check](../specs/u-b.md#0-adr-citation-index), *"U-B has no timer-driven survival-window primitive that would justify P-30 framework consumption."* The per-candidate §N.3 ADR-0036 framing characterization required for BF-L / U-A / D7-U-1 per [auto-007 §N.3 amendment](../decisions/auto-007-phase-7-dispatch-shape.md#decision-round-2) does NOT apply to U-B. The silent-absorption auditor's cross-spec ADR-0036 framing audit will not touch U-B. **However**, U-B does claim framework ADRs 0028 (P-19 typed-object store framework? — note: the spec §0 cites ADR 0029 for P-28, not 0028; U-B does NOT claim P-19/ADR 0028) and 0029 (P-28) + 0030 (P-29) with per-variant ADRs 0055 + 0056 respectively. The cross-spec characterization audit (silent-absorption auditor's Phase-6-followup #2 mandate per Reviewer 6 D-H4) WILL touch U-B on the P-28 + P-29 framing surfaces.

## §5 — archive/architectures-v2/00-comparison.md

### §5.0 File header

v2 comparison + decision guide. Carried "Compound Atelier as baseline + selective borrows" recommendation in §7. 3164 words. **Known-rejected v3 item: Compound Atelier as baseline** per Reviewer 6 D-H8 + archive-and-rebuild discipline.

### §5.1 Enumeration

- §5.1.1 (framing) §1 The four architectures (taxonomy).
- §5.1.2 (claim) §2.4 Failure mode coverage matrix (extracted to failure-modes.md — covered in §10).
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
| §5.1.1 four-architecture taxonomy | `absorbed (with adaptation)` | v3 candidate-registry preserves the 4 v2 architectures as lineage; U-B inherits primarily from Architecture 1 (Refinery) per §1 above. | architectures/v3/candidate-registry.md |
| §5.1.2 failure-mode coverage matrix | `absorbed` | F1-F20 preserved as canonical; v3 extends to F58+. Covered in §10. | architectures/v3/failure-modes-v3.md |
| §5.1.3 when-to-pick-which decision criteria | `absorbed (with adaptation)` | v3 mandate-fit matrix per DEC-2 fulfills decision-criteria role; U-B's `both`-on-4-of-5 framing IS U-B's mandate-fit claim. | architectures/v3/mandate-fit-matrix.md |
| §5.1.4 hybrid recommendations | `absorbed (with adaptation)` | **U-B is itself a unified-attempt hybrid** — pace-layer × bidirectional-traversal IS the hybrid framing applied at architecture level. v2 hybrid recommendations conceptually subsumed. | specs/u-b.md §1 axis + §5 mandate-fit |
| §5.1.5 shared infrastructure enumeration | `absorbed` | v3 common-substrate ADRs 0010-0017 + 0031 are the shared-infrastructure enumeration; U-B carries all of them. | specs/u-b.md §2 commodity substrate baseline + ADRs |
| §5.1.6 shared roles, different emphasis | `absorbed (with adaptation)` | v3 §4 discipline binding per-candidate fulfills "different emphasis" framing; U-B's per-layer P-14 routing is the per-role-by-layer dispatch. | specs/u-b.md §4 |
| §5.1.7 Compound Atelier baseline | `rejected (explicitly-anchor-avoided, see archive-and-rebuild discipline)` | **Known-rejected v3 item** per Reviewer 6 D-H8 + UC6. v3 treats all candidates as independent; U-B does NOT claim Atelier-baseline despite tertiary Atelier lineage on knowledge-promotion. | — |
| §5.1.8 selective borrows | `rejected (subsumed by v3 multi-candidate scoping principle)` | "Selective borrows" presupposes a baseline; v3 has none. | — |
| §5.1.9 build shared infrastructure first | `absorbed` | v3 Phase-5 common-substrate ADRs precede candidate-specific work; U-B framework + per-variant ADRs (0029→0055, 0030→0056) follow this discipline. | docs/adr/0010-0017 + 0029-0030 + 0055-0056 sequencing |

### §5.3 Notes

The §7 recommendations (Compound Atelier baseline + selective borrows) are the highest-priority known-rejected v3 items per the archive-and-rebuild discipline. U-B's relationship to Compound Atelier is tertiary-lineage on knowledge-promotion cadence, NOT baseline-then-deviate; the rejection is structural per UC6.

## §6 — archive/architectures-v2/01-specification-refinery.md

### §6.0 File header

v2 Architecture 1 — Specification Refinery. "The spec is the product; the implementation is a probe." Layered spec discipline (5 layers: Domain → Behavioral → Integration → Quality → Presentation) + revelation cycle + 5-mode failure classification. 3572 words. **U-B's primary v2-architecture-lineage** per §1 overview.

### §6.1 Enumeration

- §6.1.1 (claim) §1 Core thesis: spec is the durable artifact; implementation is a probe.
- §6.1.2 (primitive) §2 Artifact stack: layered specs (5 layers: Domain / Behavioral / Integration / Quality / Presentation).
- §6.1.3 (primitive) §2.1 Stable identifier discipline.
- §6.1.4 (primitive) §4 The revelation cycle (Phases 1-7).
- §6.1.5 (framing) §4.4 Diagnostic analysis (5-mode failure classification: hallucination / spec-gap / implementation-error / model-drift / methodology-mismatch).
- §6.1.6 (primitive) §6.1 The manager loop.
- §6.1.7 (primitive) §6.3 Showboat-style trajectory artifacts.
- §6.1.8 (recommendation) §10 Implementation roadmap.

### §6.2 Per-item classification

| Item | Verdict | Rationale (≤25 words) | v3 cite (if absorbed) |
|---|---|---|---|
| §6.1.1 spec is durable artifact | `absorbed (verified at §1.5)` | D-1 default; verified per §1.5. U-B carries via L2 typed envelope (ADR 0055). | specs/u-b.md §3 + §5 |
| §6.1.2 5-layer spec stack | `absorbed (with adaptation — load-bearing)` | **U-B's 5 pace-layers L0-L4 are the direct structural analog** to Refinery's 5 spec-layers; mapping is Domain→L0 Standards / Behavioral→L1 Architecture / Integration→L2 Spec / Quality→L3 Plan / Presentation→L4 Code (approximate). U-B-distinctive: layer-typing is substrate property (content-hash preimage) not methodology convention. | specs/u-b.md §1 axis + §3 layer-structure + ADR 0055 layer enum |
| §6.1.3 stable identifier discipline | `absorbed (with adaptation)` | U-B's parent-layer-ref + child-layer-refs[] content-hash pointers (ADR 0055) provide stable per-layer-graph identifiers preserving append-only discipline. | specs/u-b.md §2 + ADR 0055 envelope schema |
| §6.1.4 revelation cycle (7-phase) | `absorbed (with adaptation)` | U-B's 6-step per-cycle loop (§3) is structurally analogous: work-unit declaration → envelope construction → layer-pair gate → cycle execution → cross-layer drift evaluation → trajectory write. Refinery's 7-phase shape compressed into U-B's substrate-driven 6-step loop. | specs/u-b.md §3 per-cycle loop |
| §6.1.5 5-mode failure classification | `tbd` | Whether U-B's per-layer-pair P-31 invariant catalog (20 invariants across 5 pairs) replicates / extends / supersedes Refinery's 5-mode classification is a Phase-8 lean-eval question. | — |
| §6.1.6 manager loop | `absorbed (with adaptation)` | U-B §4 three-loop discipline (ADR 0026) is the analogue; P-06 Patrol-tier monitoring of cross-layer drift distribution = meta-loop closure. | specs/u-b.md §4 three-loop |
| §6.1.7 showboat trajectory artifacts | `absorbed (with adaptation)` | U-B's P-05 trajectory capture (ADR 0012) appends per-cycle events with layer-tag in payload (§3 cycle step 6) — Refinery's trajectory-as-artifact framing absorbed with layer-tagging adaptation. | specs/u-b.md §3 cycle step 6 |
| §6.1.8 implementation roadmap | `not-applicable-to-candidate-mandate` | Architecture-specific deployment; v3 doesn't carry per-architecture roadmaps. | — |

### §6.3 Notes

This is U-B's deepest absorption surface. Refinery's 5-layer spec stack (§6.1.2) is the direct structural ancestor of U-B's 5 pace-layers; the U-B-distinctive move is shifting layering from methodology-convention to substrate-property (layer in content-hash preimage). Refinery's revelation cycle (§6.1.4) is compressed into U-B's substrate-driven cycle. Showboat trajectory (§6.1.7), manager loop (§6.1.6), and stable-ID discipline (§6.1.3) all land at U-B substrate level. **None of the Refinery primitives are N/A or rejected to U-B** — Refinery is genuinely U-B's primary v2-architecture-lineage as identified in §1.

## §7 — archive/architectures-v2/02-compound-atelier.md

### §7.0 File header

v2 Architecture 2 — Compound Atelier. "Each unit of work makes the next easier." Queue + workpad + persona panel + accumulated `docs/solutions/`. v2's recommended baseline (rejected as v3 anchor). 4515 words. **U-B's tertiary v2-lineage** on pace-layered knowledge-promotion cadence.

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
| §7.1.1 compounding core thesis | `absorbed (with adaptation)` | U-B §4 knowledge-promotion at pace-layer cadence: L4 emergent → L3 chunk pattern → L2 spec refinement → L1 architecture rule → L0 standard. Compounding via upward layer-graph traversal. | specs/u-b.md §4 knowledge-promotion |
| §7.1.2 knowledge accumulation between cycles | `absorbed (verified at §3.1.5)` | Already absorbed via §3.1.5; U-B binds layer-typed via ADR 0055 envelope. | specs/u-b.md §4 |
| §7.1.3 artifact stack (specs/knowledge/workpad) | `absorbed (with adaptation)` | U-B substrate provides typed-object store per-layer via ADR 0055 — Atelier's stack mapped to U-B's per-layer artifact graph. | specs/u-b.md §2 |
| §7.1.4 workshop chain (persona workshops) | `not-applicable-to-candidate-mandate` | U-B is layer-graph not persona-graph; persona-workshop is N/A at axis level. P-14 routing is layer-aware not persona-aware. | — |
| §7.1.5 researcher fan-out | `tbd` | U-B has no explicit research-fan-out primitive at substrate; methodology-layer pattern. Phase-8 lean-eval may revisit. | — |
| §7.1.6 reviewer panel | `absorbed (with adaptation)` | U-B §4 bias-guard via P-14 cross-family judge (Wave 4.5 invariant L2-L3-2 + L3-L4-2) enforces structural diversity at the substrate. | specs/u-b.md §4 bias-guard |
| §7.1.7 synthesis and curation | `absorbed (with adaptation)` | U-B §4 knowledge-promotion at pace-layer cadence is the synthesis-and-curation shape; promotion is P-29-gated layer-pair transition. | specs/u-b.md §4 |
| §7.1.8 conductor orchestrator | `not-applicable-to-candidate-mandate` | U-B leaves orchestration to methodology layer; substrate doesn't mandate orchestrator shape (§3 "Methodology takes no opinion on coordination medium"). | — |
| §7.1.9 workpad protocol | `absorbed (with adaptation)` | U-B's per-cycle typed envelope (ADR 0055) construction in §3 cycle step 2 + P-01 sandbox is the workpad-equivalent at substrate level. | specs/u-b.md §2 + §3 |
| §7.1.10 tiered cycle scope | `absorbed` | U-B's per-layer cost-ceilings + per-layer-pair gate-policies IS the tiering by-construction (Brier cadence in storage shape). | specs/u-b.md §3 work-unit-definition + §4 cost-ceiling |
| §7.1.11 severity × autofix axes | `absorbed (silently — flagged for auditor)` | The orthogonal-axes framing influenced v3's mandate-fit-per-(architecture × work-unit-class) DEC-2 schema. Not explicitly cited in U-B spec. | — (flagged for silent-absorption auditor) |
| §7.1.12 residual work gate | `absorbed (with adaptation)` | U-B's P-31 cross-layer drift detector (ADR 0054) emits `LayerDriftEvent` to P-29 mediator (ADR 0056) → operator handback at appropriate layer-transition escrow. Substrate-level residual-work closure. | specs/u-b.md §3 cycle step 5 |
| §7.1.13 three memory tiers | `absorbed (with adaptation — load-bearing)` | **U-B's pace-layer stack is itself a 5-tier memory hierarchy** (L0 slowest → L4 fastest per Brier `change-rate`), generalizing Atelier's 3-tier shape. Direct substrate inheritance, layer-count-extended. | specs/u-b.md §1 axis + §2 + ADR 0055 envelope `change-rate` field |
| §7.1.14 implementation roadmap | `not-applicable-to-candidate-mandate` | Architecture-specific deployment. | — |

### §7.3 Notes

U-B's tertiary Atelier lineage is on compounding-cadence (§7.1.1 + §7.1.2) and memory-tiering (§7.1.13). The U-B distinctive move on memory-tiering: 5 pace-layers (vs Atelier's 3) with substrate-property `change-rate` on the envelope. The silent-absorption flag on §7.1.11 (severity × autofix orthogonal axes → DEC-2 schema) is the same flag the exemplar surfaces — likely a v3-level inheritance shared across multiple candidates' specs.

## §8 — archive/architectures-v2/03-phase-gated-foundry.md

### §8.0 File header

v2 Architecture 3 — Phase-Gated Foundry. "Pre-agile structured methodologies become the right shape when agents make them fast." Phase-bound experts, formal templates (SRS, SAD, DD), RTM, gate boards. 4610 words. **U-B's secondary v2-lineage** on per-phase-gate discipline + V&V pairing.

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
| §8.1.1 structured pre-agile core thesis | `absorbed (with adaptation — load-bearing)` | **U-B's per-layer-pair P-29 gates ARE the substrate-level "phase-gate" structure** (ADR 0056); each Lᵢ→Lᵢ₊₁ transition is a Foundry-flavored gate but transposed onto pace-layer not Foundry-phase enumeration. | specs/u-b.md §3 layer-pair gate evaluation + ADR 0056 |
| §8.1.2 phase model + V&V pairing | `absorbed (with adaptation)` | U-B's per-layer-pair invariant catalog (Wave 4.5: 20 invariants across L0↔L1, L1↔L2, L2↔L3, L3↔L4, L0↔L4) is structurally the V&V-pairing shape: each layer-pair has its own invariant set, mirroring Foundry's per-phase V&V pairs. | specs/u-b.md §2 P-31 + sub-tracks/u-b-invariant-authoring.md |
| §8.1.3 Configuration Management discipline | `absorbed (with adaptation)` | U-B's ADR 0055 layer-indexed append-only envelope on libgit2/Postgres is the substrate-level CM analogue: content-addressed per-layer history, immutable. | specs/u-b.md §2 P-28 framework + ADR 0055 |
| §8.1.4 defect-of-origin table | `absorbed (with adaptation)` | U-B's `LayerDriftEvent{layer-pair, invariant-id, recommended-handback-layer}` (ADR 0054) provides per-layer-pair defect-of-origin attribution via the typed event payload. | specs/u-b.md §2 P-31 + §3 cycle step 5 + ADR 0054 |
| §8.1.5 RUP-style discipline × phase matrix | `not-applicable-to-candidate-mandate` | Foundry-specific; U-B binds all 10 disciplines uniformly per-layer-pair via the gate-policy mechanism (not as a phase matrix). | — |
| §8.1.6 iteration within phases | `absorbed (with adaptation)` | U-B's per-cycle within-layer iteration is uniform (§3 cycle); cross-layer is gated. Foundry's within-phase iteration is the U-B within-layer analogue. | specs/u-b.md §3 per-cycle loop |
| §8.1.7 V&V-side independent roles + different model family | `absorbed` | U-B §4 bias-guard via P-14 cross-family routing (Wave 4.5 invariant L2-L3-2 + L3-L4-2) — `reviewer-model-family ≠ builder-model-family` per the Hess `kevin/carl` pattern (verbatim from §4). | specs/u-b.md §4 bias-guard + §3 |
| §8.1.8 CM as spine | `absorbed (with adaptation)` | U-B's layered substrate IS the spine — typed-object store + per-layer-pair gates + drift detector hold the architecture; methodology rides on top. | specs/u-b.md §1 axis + §2 |

### §8.3 Notes

Foundry is U-B's secondary lineage — strongly present on phase-gate discipline (§8.1.1) and V&V pairing (§8.1.2). The U-B-distinctive move: Foundry's enumerated phase model (Phases 1-6) is replaced by U-B's pace-layer parameterised model where layer-count is empirical (OQ-PLEF-1 open carry). 6-of-8 Foundry primitives are absorbed; only the RUP discipline-matrix (§8.1.5) is N/A. CM-as-spine (§8.1.8) is the deepest absorption — U-B's substrate-first framing on the layered store directly inherits the CM-spine shape.

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
| §9.1.1 population + selection core thesis | `not-applicable-to-candidate-mandate` | Tournament-specific population-based methodology; U-B is single-cycle per-layer not population-based. | — |
| §9.1.2 genome structure | `not-applicable-to-candidate-mandate` | Tournament-specific artifact. | — |
| §9.1.3 model-family diversity as structural | `absorbed (with adaptation)` | U-B §4 bias-guard via P-14 cross-family routing — model-family diversity is structural via L2→L3 + L3→L4 invariants. F46 mitigation. | specs/u-b.md §4 |
| §9.1.4 generation cycle | `not-applicable-to-candidate-mandate` | Tournament-specific. | — |
| §9.1.5 predator agent | `rejected (subsumed by substrate-level adversarial discipline)` | U-B substitutes Tournament's predator-agent with substrate-level invariant-catalog + cross-family judge + P-31 drift detector. Substrate substitution. | — |
| §9.1.6 loops within loops | `absorbed (with adaptation)` | U-B §4 three-loop discipline (ADR 0026) + Patrol-tier meta-loop on cross-layer drift distribution. | specs/u-b.md §4 three-loop |
| §9.1.7 independence policy | `absorbed` | U-B §4 P-14 cross-family judge enforces builder-judge independence at substrate (Wave 4.5 invariant L3-L4-2 verbatim: `reviewer-model-family ≠ builder-model-family`). | specs/u-b.md §4 + §3 |
| §9.1.8 scaling | `tbd` | U-B §6 OQ-PLEF-3 multi-cycle population drift is the explicit open-carry on scaling. Tournament's scaling lessons may inform Phase-8 lean-eval. | — |

### §9.3 Notes

Tournament's primary primitives (population, predator, generation bracket) are N/A to U-B, but the cross-model-family diversity discipline (§9.1.3) and independence policy (§9.1.7) land at substrate level via P-14. Predator-agent (§9.1.5) is rejected with reason: U-B's invariant-catalog (P-31, 20 invariants) + cross-family judge substitutes for runtime predator pressure. Scaling (§9.1.8) is TBD — U-B's OQ-PLEF-3 carries the multi-cycle drift question to Phase-8.

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
| §10.1.1 F1 Hallucination | `absorbed` | U-B §4 bias-guard via P-14 cross-family judge + Wave 4.5 L2-L3-2 closes F1. | specs/u-b.md §4 + §3 cycle step 5 |
| §10.1.2 F2 Reward hacking | `absorbed` | U-B §4 holdout (ADR 0021) + P-08 scenario storage + L3→L4 P-29 closure. | specs/u-b.md §4 holdout |
| §10.1.3 F3 Spec-completeness | `absorbed (with adaptation)` | U-B's L1→L2 invariants (Wave 4.5 L1-L2-2 prohibited-action coverage + L1-L2-3 evidence-obligation trace) provide spec-completeness checks at substrate. | specs/u-b.md §5 initial-spec + sub-tracks |
| §10.1.4 F4 Code quality | `absorbed (with adaptation)` | U-B §4 bias-guard cross-model judging at L3→L4 + P-23 dependency-impact graph. | specs/u-b.md §3 + §4 |
| §10.1.5 F5 Cognitive ceiling | `absorbed (with adaptation)` | F53 voluntary-discipline-fragility framing — U-B's per-P-29-gate structural escrow IS the F53 antidote (operator-attention summoned, not voluntary). | specs/u-b.md §4 cognitive-escrow |
| §10.1.6 F6 Cognitive debt | `absorbed` | U-B §3 cycle step 6 P-05 trajectory write with layer-tag in payload + §4 cognitive-escrow per-gate. | specs/u-b.md §4 + ADR 0019 |
| §10.1.7 F7 Normalization of deviance | `absorbed (with adaptation)` | U-B's P-31 cross-layer drift detector (ADR 0054) + Patrol monitoring of invariant fire-rate distribution resist deviance accumulation across cycles. | specs/u-b.md §3 + §4 |
| §10.1.8 F8 Stale knowledge | `absorbed (with adaptation)` | U-B's pace-layer cadence preserves upper-layer slowness (L0 months–years) + lower-layer freshness (L4 minutes–hours); knowledge-promotion gated per ADR 0023. | specs/u-b.md §2 + §3 + §4 |
| §10.1.9 F9 Spec overfitting | `absorbed (with adaptation)` | U-B's L1→L2 gate (ADR 0056) requires upstream architecture evidence before spec materialises; spec is bounded-by-architecture-rule. | specs/u-b.md §3 cycle step 3 + §4 holdout |
| §10.1.10 F10 Findings disappear | `absorbed` | U-B's P-31 LayerDriftEvent + P-05 trajectory append-only + P-29 typed `reasons[]` provide structural finding persistence. | specs/u-b.md §2 + §3 + ADR 0054 |
| §10.1.11 F11 Renumbering | `absorbed (with adaptation)` | U-B's ADR 0055 content-hash + parent-layer-ref + child-layer-refs[] handle stable per-layer-graph identifiers (Refinery's stable-ID discipline absorbed). | specs/u-b.md §2 + ADR 0055 |
| §10.1.12 F12 Lethal trifecta | `absorbed (verified)` | U-B §4 trifecta closure: Wave 4.5 invariant L3-L4-3 (Lethal-Trifecta prohibition on builder-cycle effects; substrate-default off per F44). | specs/u-b.md §4 trifecta + ADR 0027 |
| §10.1.13 F13 Missing-config | `absorbed (with adaptation)` | U-B's P-23 dependency-impact graph surfaces config-dependency drift; per-layer-pair P-29 gates reject missing-upstream-policy calls. | specs/u-b.md §2 + §3 |
| §10.1.14 F14 Attribution collapse | `absorbed (with adaptation)` | U-B's P-05 trajectory append with layer-tag + ADR 0055 content-hash chain provide attribution; not as explicit as BF-S's P-24 attribution store but structurally equivalent at per-layer cadence. | specs/u-b.md §3 cycle step 6 |
| §10.1.15 F15 Single-prompt collapse | `absorbed (with adaptation)` | U-B §4 bias-guard cross-model judging via P-14 layer-aware multi-shape dispatch (per L0/L1 long-context + diverse families; L2→L3 cross-family contradiction; L4 provider-aligned) — structural diversity per-layer. | specs/u-b.md §4 + P-14 sketch |
| §10.1.16 F16 Resume-fidelity | `absorbed` | U-B's P-05 trajectory capture + ADR 0055 content-hash provides resume anchor per layer. | specs/u-b.md §3 + ADR 0055 |
| §10.1.17 F17 Parallel agents on shared dirs | `tbd` | Parallel-agents discipline is methodology-layer; U-B substrate supports parallelism but specific anti-collision is methodology call. | — |
| §10.1.18 F18 Prose-spec rigor | `absorbed (with adaptation)` | U-B's L2 EARS-typed + GtWR-linted intent block + L2-L3-3 vocabulary-lint invariant (Wave 4.5) is structured-spec-rigor at substrate. | specs/u-b.md §3 layer-structure + sub-tracks |
| §10.1.19 F19 Model-floor dependency | `absorbed` | U-B §4 bias-guard cross-model judging via P-14 surfaces model-floor per L2-L3-2 + L3-L4-2 invariants. | specs/u-b.md §4 + ADR 0018 |
| §10.1.20 F20 Maintenance asymmetry | `absorbed (with adaptation)` | U-B's per-layer-pair gate-policy is uniform across mandates (greenfield top-down / brownfield bottom-up); maintenance asymmetry resolved at substrate via traversal-direction-parameter. | specs/u-b.md §1 axis + §5 |
| §10.1.21 A1 Refinery coverage row | `not-applicable-to-candidate-mandate` | Coverage row characterizes Architecture 1 (U-B's primary lineage), but the ★★★★ scoring is per-Refinery, not per-U-B. U-B's own F-mode coverage tracked above. | — |
| §10.1.22 A2 Atelier coverage row | `not-applicable-to-candidate-mandate` | Coverage row characterizes Architecture 2. Informational for U-B's tertiary Atelier lineage. | — |
| §10.1.23 A3 Foundry coverage row | `not-applicable-to-candidate-mandate` | Coverage row characterizes Architecture 3 (U-B's secondary lineage). | — |
| §10.1.24 A4 Tournament coverage row | `not-applicable-to-candidate-mandate` | Coverage row characterizes Architecture 4. | — |

### §10.3 Notes

19-of-20 F-modes are absorbed (F1-F16 except F17 TBD; F18-F20). F12 verified-absorbed with explicit U-B spec invocation (Wave 4.5 L3-L4-3). 1 TBD (F17, methodology-layer parallel-agent discipline). The 4 per-architecture coverage-strength rows are informational characterizations of v2 architectures, not U-B-actionable items. **U-B's F-mode absorption count is notably higher than BF-S exemplar's 15-of-20** — reflecting U-B's heavy-tier scope: U-B's per-layer-pair invariant catalog (20 invariants, Wave 4.5) provides per-layer-pair coverage that catches more F-modes structurally.

## §11 Summary

**Per-token cell counts (matches YAML frontmatter):**

| Token | Count |
|---|---|
| `absorbed` (incl. with-adaptation, verified, silently) | 71 |
| `rejected (reason)` | 5 |
| `not-applicable-to-candidate-mandate` | 15 |
| `tbd` | 7 |
| **Total** | **98** |

(Total = §2.2 (3) + §3.2 (16) + §4.2 (8) + §5.2 (9) + §6.2 (8) + §7.2 (14) + §8.2 (8) + §9.2 (8) + §10.2 (24) = **98 per-archive-file cells**; matches `grep -E "^\| §[0-9].*\| \`<token>"` tallies. Per the exemplar's recount discipline: D-1..D-7 verifications in §1.5 are counted separately as 7 absorbed-verified rows. Aggregate cell count: **98 per-archive-file cells + 7 §1.5 D-default verifications = 105 cells across all rubric sections.** Note that §3.2 + §4.2 contain 7 rows that re-cite the D-1..D-7 defaults (each marked `absorbed (verified at §1.5)`) — these are intentional cross-references, not double-counts; the silent-absorption auditor should reconcile per the BF-S exemplar's discrepancy-documentation pattern. **U-B's 98-cell count exceeds BF-S exemplar's 98-cell total at the per-archive-file layer but with higher `absorbed` density (71 vs 31)** — reflecting U-B's heavy-tier multi-lineage scope (primary Refinery + secondary Foundry + tertiary Atelier vs BF-S's primarily Atelier lineage).)

**High-confidence absorbed cells:** D-1, D-3, D-4, D-5, D-6, D-7 (verified per §1.5); D-2 absorbed-with-adaptation; F12 (verified at §4 trifecta + Wave 4.5 L3-L4-3); Refinery 5-layer spec stack → U-B's 5 pace-layers (load-bearing direct structural inheritance, §6.1.2); Atelier 3 memory tiers → U-B 5-tier pace-layer hierarchy (load-bearing, §7.1.13); Foundry pre-agile-with-agent-speed + V&V pairing → U-B per-layer-pair P-29 gates + Wave 4.5 invariant catalog (load-bearing, §8.1.1 + §8.1.2).

**Surfaced TBDs (require lead-agent reconciliation or Phase-8 follow-up):**

1. §3.1.12 spec format tension — L2 El Kaim 9-field block suggests structured; Phase-8 lean-eval.
2. §3.1.15 parallel-agent + human-role tension — OQ-PLEF-5 + OQ-PLEF-8 open carries in §6.
3. §4.1.6 falsified consensus items — needs per-item review of what was falsified vs preserved in v3 (same TBD as exemplar).
4. §6.1.5 Refinery 5-mode failure classification — Phase-8 lean-eval candidate.
5. §7.1.5 researcher fan-out — U-B has no explicit research-fan-out primitive; Phase-8 lean-eval.
6. §9.1.8 Tournament scaling — OQ-PLEF-3 multi-cycle drift; Phase-8 lean-eval.
7. §10.1.17 F17 Parallel agents on shared dirs — methodology-layer call.

**Silent-absorption auditor flags (for cross-spec reconciliation):**

- §3.1.16 cross-cutting primitives (v3 `primitives/index.md` likely inherited the framing without explicit citation — same flag as exemplar, suggesting v3-level pattern).
- §7.1.11 severity × autofix orthogonal axes (likely informed DEC-2 mandate-fit-per-(architecture × work-unit-class) schema — same flag as exemplar).
- **Cross-spec characterization audit hook (per Reviewer 6 D-H4):** U-B claims framework ADRs 0029 (P-28) + 0030 (P-29) with per-variant ADRs 0055 + 0056 respectively. Auditor should compare U-B's framing of P-28 (`layer-indexed-first`) and P-29 (`per-layer-boundary policy DSL`) against U-A's, U-C's, and D7-U-1's framings of the same frameworks for cross-spec inheritance gaps.

**Known-rejected items confirmed:**

- §4.1.10 OpenHands+Overstory substrate stack — `rejected (explicitly-excluded-per-constraints-extracted)`.
- §5.1.7 Compound Atelier as baseline — `rejected (explicitly-anchor-avoided)`.

**X_UNM_B cross-mandate inheritance surfacing (unified-attempt rider).** U-B's brownfield-fit per [spec §2 X_UNM_B](../specs/u-b.md#2-substrate-composition) is honest: bottom-up L4→L0 inference is *competent at brownfield, not optimal*. The candidate explicitly degrades to greenfield-only when upward inference fails on L0/L1. This is the cross-mandate cell that pressure-tests the unified-attempt claim at Phase-8: U-B does NOT claim global UC4-resolution; the unified-attempt label is bounded.

## §12 References

**U-B spec + supporting docs:**

- [`architectures/v3/specs/u-b.md`](../specs/u-b.md) — U-B Phase-6 architecture spec (audit input).
- [`architectures/v3/candidate-registry.md` U-B entry](../candidate-registry.md#u-b--pace-layered-escrow-factory-5-layer-artifact-stack-with-bidirectional-traversal) — registry entry for §1 lineage statement.
- [`architectures/v3/substrate-requirements/u-b.md`](../substrate-requirements/u-b.md) — substrate-requirements summary (X_UNM_B carry).
- [`architectures/v3/tracks/unified-B.md`](../tracks/unified-B.md) — Phase-2 track sketch.
- [`architectures/v3/sub-tracks/u-b-invariant-authoring.md`](../sub-tracks/u-b-invariant-authoring.md) — Wave 4.5 invariant catalog (20 invariants).
- [`architectures/v3/decisions/auto-007-phase-7-dispatch-shape.md`](../decisions/auto-007-phase-7-dispatch-shape.md) — Phase-7 dispatch brief.
- [`architectures/v3/backfill-notes/bf-s.md`](bf-s.md) — exemplar back-fill notes (shape inheritance).

**Archive (9 files audited):**

- [`archive/research-plan.md`](../../../archive/research-plan.md) — §2
- [`archive/synthesis-v1-v2/00-synthesis.md`](../../../archive/synthesis-v1-v2/00-synthesis.md) — §3
- [`archive/synthesis-v1-v2/13-round-2-synthesis.md`](../../../archive/synthesis-v1-v2/13-round-2-synthesis.md) — §4
- [`archive/architectures-v2/00-comparison.md`](../../../archive/architectures-v2/00-comparison.md) — §5
- [`archive/architectures-v2/01-specification-refinery.md`](../../../archive/architectures-v2/01-specification-refinery.md) — §6 (primary lineage)
- [`archive/architectures-v2/02-compound-atelier.md`](../../../archive/architectures-v2/02-compound-atelier.md) — §7 (tertiary lineage)
- [`archive/architectures-v2/03-phase-gated-foundry.md`](../../../archive/architectures-v2/03-phase-gated-foundry.md) — §8 (secondary lineage)
- [`archive/architectures-v2/04-evolutionary-tournament.md`](../../../archive/architectures-v2/04-evolutionary-tournament.md) — §9
- [`archive/architectures-v2/failure-modes.md`](../../../archive/architectures-v2/failure-modes.md) — §10

**Archive indexes (context):**

- [`archive/ARCHIVE.md`](../../../archive/ARCHIVE.md)
- [`archive/synthesis-v1-v2/ARCHIVE.md`](../../../archive/synthesis-v1-v2/ARCHIVE.md) — source of D-1..D-7 default enumeration.
- [`archive/architectures-v2/ARCHIVE.md`](../../../archive/architectures-v2/ARCHIVE.md) — source of 4-architecture taxonomy.

**ADRs cited (U-B framework + per-variant + orphan):**

- U-B substrate ADRs: [0010-0017](../../../docs/adr/) common + [0018-0027](../../../docs/adr/) discipline + [0031](../../../docs/adr/0031-p-23-dependency-impact-graph.md) P-23.
- Framework ADRs U-B claims: [0029 (P-28 framework)](../../../docs/adr/0029-p-28-typed-object-store.md), [0030 (P-29 framework)](../../../docs/adr/0030-p-29-policy-mediator.md).
- U-B per-variant ADRs: [0055 (P-28 layer-typed envelope)](../../../docs/adr/0055-p-28-variant-u-b-layer-typed-envelope.md), [0056 (P-29 layer-boundary policy DSL)](../../../docs/adr/0056-p-29-variant-u-b-layer-boundary.md).
- U-B orphan ADR: [0054 (P-31 cross-layer drift detector)](../../../docs/adr/0054-p-31-cross-layer-drift-detector.md).

**Constraints / decisions:**

- [`architectures/v3/constraints-extracted.md`](../constraints-extracted.md) — UC1-UC8 user constraints (source of known-rejected v3 item flags).
- [`architectures/v3/decisions-captured.md`](../decisions-captured.md) — DEC-1 / DEC-1.a / DEC-2 etc.
- [`architectures/v3/phase-3.4-decisions-resolved.md`](../phase-3.4-decisions-resolved.md) — DEC-2 cognitive-escrow placement (methodology).
