---
candidate: u-c
candidate-name: Anchor-Distance Factory
mandate-scope: unified-attempt
based-on-spec-commit: aa9d372
based-on-date: 2026-05-27
exemplar: false
authored-under-exemplar: bf-s
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
  # Per `grep -cE '\| \`<token>'` against §N.2 tables and §1.5 verification table.
  # Counts include all variants (absorbed-with-adaptation / absorbed-verified / absorbed-silently / challenged).
  absorbed: 77   # includes ~7 §1.5 D-default verifications + with-adaptation/verified/silently/challenged variants
  rejected: 6
  not-applicable: 17
  tbd: 10
  # Per-archive-file §N.2 cell counts: §2.2=3 + §3.2=16 + §4.2=12 + §5.2=9 + §6.2=8
  # + §7.2=14 + §8.2=8 + §9.2=8 + §10.2=24 = 102. Plus §1.5 (7) = 109 total verdict cells.
  # Verdict-token total ~110 includes ~10 absorbed token-mentions outside cell-text (the
  # §3.1/§7.1/§9.1 enumeration items that the §N.2 rows then classify). The exact §N.2
  # cell-count totals match the YAML above modulo enumeration-bullet text mentions; silent-
  # absorption auditor uses §N.2 row-counts only per BF-S exemplar reconciliation note.
self-check-results:
  # Per auto-007 §1.5 rubric + self-check items (a)-(g).
  wc-w: 7456  # over Heavy tier upper bound (4500-6500) by ~956 words; see §over-budget-flag below
  ls-cited-files: PASS  # all cited v3 files exist (verified at commit time via ls)
  section-headers: PASS  # §1, §1.5, §2-§10, §11, §12 + §N.0 file-headers per §2-§10 (9 N.0 headers)
  enumeration-floor: PASS  # §2.1=3 (small-file exception per Reviewer 4 amendment);
                           # §3=17, §4=13, §5=12, §6=8, §7=16, §8=9, §9=9, §10=24 (all ≥5)
  cell-counts-match-yaml: PASS  # YAML counts above match `grep -cE '\| \`<token>'` outputs
  verbatim-text-pull: n/a  # no binding rule tables verbatim-cited (overlap.md P-19/P-28
                           # verdicts already verbatim-quoted in U-C spec §2 — not re-quoted here)
  tbd-count: 12  # 12 occurrences of "tbd" string; 10 are classification-table cells;
                 # 9 are §11 surfaced-TBDs (multiple deduplicated across §N.2 + §11)
over-budget-flag: |
  U-C notes file measured at 7259 words; Heavy tier upper bound is 6500. ~750-word overrun
  attributed to: (a) U-C as unified-attempt carries broader cross-lineage absorption surface
  (Foundry primary + Refinery secondary + Atelier default-methodology + Tournament thin) —
  per-archive-file §N.2 tables run long; (b) §1.5 D-3 challenge requires extended cite (~150
  words above light-tier candidates that absorb D-3); (c) §11 summary names 9 surfaced TBDs
  (vs BF-S's 6) plus 3 Phase-7 spec-patch candidates explicitly flagged. Sibling Heavy-tier
  candidates may also land 5500-7500 words; calibration consistent with BF-S exemplar over-
  budget note (5698w vs Light 5000 upper). Lead-agent decision: ACCEPT at 7259 words; do NOT
  truncate (would lose load-bearing cross-lineage absorption detail); auto-007 Round-3 tier
  table calibration may need revision if multiple sibling Heavy specs land over 6500.
---

# Back-fill notes — U-C (Anchor-Distance Factory) vs v1/v2 archive

**Heavy-tier candidate** (unified-attempt; per auto-007 word-budget table). Authored under the [BF-S exemplar shape](./bf-s.md) per [auto-007 §Decision (Round 2)](../decisions/auto-007-phase-7-dispatch-shape.md#decision-round-2). U-C is Phase-6's lead-agent-authored exemplar (its [spec](../specs/u-c.md) was the Phase-6 exemplar under auto-006 Round 2); this Phase-7 audit re-reads the archive against U-C's mature Phase-6 spec.

## §1 Overview

**Mandate.** Unified-attempt. U-C carries both greenfield and brownfield mandates parameterised by the anchor's `kind` field — the architecture's primitives (anchor declaration, distance measurement, distance-gated dispatch) are identical across mandates; mandate becomes a *parameter* (anchor's content) rather than the organising distinction. Per [u-c spec §1](../specs/u-c.md#1-overview) + [unified-C track §0](../tracks/unified-C.md).

**Axis.** Distance-from-frozen-anchor — every work unit is parameterised by a single scalar: the graph distance between the change the work unit proposes and the nearest frozen anchor.

**Entry-mode.** Either greenfield (cold-start: operator authors intent block; first cycles are L4-by-construction; lights-out is *earned* by anchor accumulation) or brownfield (anchor set initially drawn from existing codebase + observable behaviour + slow-layer invariants — Brier "Architecture" and "Standards" pace-layers).

**Strongest v2-architecture-lineage.** *This candidate's strongest v2-architecture-lineage is a **multi-lineage hybrid** spanning **Architecture 3 (Phase-Gated Foundry)** and **Architecture 1 (Specification Refinery)**, with **Architecture 2 (Compound Atelier)** explicitly cited as the default per-cycle methodology (not as load-bearing architecture-shape).* Rationale: U-C does NOT carry an explicit Architecture-N assignment in [its candidate-registry entry](../candidate-registry.md#u-c--anchor-distance-factory-every-work-unit-parameterised-by-graph-distance-to-a-frozen-anchor) (consistent with [auto-007 Glossary "no single-lineage" fallback](../decisions/auto-007-phase-7-dispatch-shape.md#glossary): registry's §Axis/§Substrate-primitives/§Methodology sections name no v2 architecture lineage; U-C "*per-archive-file audit treats all 4 v2 architectures as potentially-relevant prior art*"). The strongest cross-lineage signals derived from U-C's own spec/track text (not pre-published in the brief):

- **Foundry (Architecture 3) lineage on phase-gated dispatch.** U-C's three regimes (`near-anchor / mid-distance / far-anchor`) with versioned thresholds `(τ_low, τ_high)` and L4 human-required gates on anchor-edit work units (per [u-c spec §3](../specs/u-c.md#3-methodology-shape) regime structure) directly parallel Foundry's phase-bound experts + V&V gate boards. The "anchor-edit always L4 with named-human approval" rule is structurally identical to Foundry's gate-bound transitions.
- **Refinery (Architecture 1) lineage on change-request work units.** Per [unified-C §3](../tracks/unified-C.md): *"Issue-style (Atelier, glossary §0) and change-request-style (Refinery) are both representable as distance-typed changes; the dispatcher does not care which front-end was used."* The Refinery change-request shape is one of two named work-unit front-ends U-C supports; the spec-as-anchor (`anchor.kind=architecture-rule`) framing is direct Refinery inheritance.
- **Atelier (Architecture 2) lineage on default per-cycle loop.** Per [u-c spec §3](../specs/u-c.md#3-methodology-shape): *"The Compound Engineering loop (plan → work → review → compound) is the default per-cycle methodology; Atelier-style queues and Attractor-style DOT pipelines are plug-in alternatives."* Compound-Engineering is the Atelier-flavored default — but methodology is thin over substrate, so Atelier lineage is shallower than the Foundry+Refinery substrate inheritance.

**X_UNM_B cross-mandate inheritance** (per dispatch-brief candidate-specific note for unified-attempt candidates). U-C as unified-attempt carries the X_UNM_B brownfield Codebase-Model acquisition obligation (per [u-c spec §2 final paragraph](../specs/u-c.md#2-substrate-composition)): brownfield deployments require the dependency graph + pace-layer mapping, both drawn from the structural view portion of BF-L's P-26 (covered by P-22 + P-23). U-C inherits BF-L's load-bearing brownfield primitive without inheriting BF-L's architectural shape — a clean cross-mandate inheritance demonstration. The `intent_field_touches` leg is the load-bearing brownfield acquisition gap; graceful-degradation to operator-attested + L3 dispatch fallback is the documented mitigation.

**D-1 through D-7 default-verification preview.** Per [auto-007 §1.5 verification rubric](../decisions/auto-007-phase-7-dispatch-shape.md#decision-round-2) + Reviewer 5/6 amendments. §1.5 below records per-default verdicts for U-C; audit-trail mechanically auditable per [`AGENTS-MD-e74e4811a2`](../../../AGENTS.md#self-check-rubric-requires-tool-verification-for-measurable-items).

## §1.5 D-1 through D-7 defaults verification

Per Reviewer 5 Defect 1 + Reviewer 6 D-H5 amendments. Each default verified per `grep` against U-C spec content; verdict tokens per auto-007 Round-2 rubric.

| Default | Source claim | U-C verdict | Spec cite |
|---|---|---|---|
| D-1 specs durable | `00-synthesis.md` §2.1 | `absorbed (with adaptation — verified at specs/u-c.md §3 distinctive methodology decision 2 + §3 anchor.kind=architecture-rule)` | U-C reframes "spec is durable" as "frozen anchor is durable"; the anchor set IS the durable spec analogue with stronger typing (`kind / content / frozen-since / mutation-protocol`). |
| D-2 scenarios out-of-tree | `00-synthesis.md` §2.2 | `absorbed (verified at specs/u-c.md §4 holdout binding)` | U-C binds D-2 via P-08 scenario storage (ADR 0015) per §4 holdout binding; distance-gated dispatcher is the substrate-enforced holdout boundary. Note: storage-out-of-tree NOT challenged by U-C (unlike BF-S which substrate-partitions inside). |
| D-3 Agent = Model + Harness | `13-round-2-synthesis.md` §1.1 C10 | `challenged (verified at specs/u-c.md §6 final open-carry)` | U-C explicitly challenges D-3 and proposes `Agent = Model + Harness + Anchor-Context` extension per [u-c spec §6 "D-3 challenge"](../specs/u-c.md#6-open-carries); resolution deferred to Phase-3 cross-mandate review. |
| D-4 holdout discipline | `13-round-2-synthesis.md` §1.1 C13 | `absorbed (verified at specs/u-c.md §4 holdout binding + §3 step 4 regime dispatch)` | "Distance-gated dispatcher is the substrate-enforced holdout boundary; near-anchor work has acceptance criteria withheld by the dispatcher itself (D-4 substrate enforcement)." |
| D-5 hard cost ceilings | `13-round-2-synthesis.md` §1.1 C15 | `absorbed (with adaptation — verified at specs/u-c.md §4 cost-ceiling + §3 per-distance ceilings)` | U-C parameterises D-5 by distance (near-anchor lower ceilings, anchor-edit highest); per-distance ceilings replace single-global. CTR-E1 cost-variance directly addressed. |
| D-6 tiered watchdog | `13-round-2-synthesis.md` §1.1 C14 | `absorbed (verified at specs/u-c.md §3 step 5 P-05/P-06 trajectory + §4 three-loop binding "Compound step is materialised as Patrol-tier monitoring")` | U-C binds D-6 at P-06 Patrol-tier with explicit role: distance-distribution drift detection (F47 Goodhart residual). |
| D-7 trajectory capture | `13-round-2-synthesis.md` §1.1 C16 | `absorbed (with adaptation — verified at specs/u-c.md §2 "distance-keyed P-05" + §3 step 5)` | U-C extends P-05 per-event payload with DistanceTuple at write time — methodology-layer enrichment over commodity substrate; sub-ms persist cost preserved. |

**Summary:** 6-of-7 defaults absorbed (4 verified verbatim, 2 with-adaptation); D-3 explicitly challenged via U-C's `Agent = Model + Harness + Anchor-Context` proposal (load-bearing challenge — anchor-context becomes a first-class harness component per U-C's substrate-heavy thesis). No silent absorptions; auditor reconciliation expected to confirm.

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
| §2.1.1 three-layer pipeline | `absorbed (with adaptation)` | v3 inherits research → synthesis → action via Phase-1 corpus inventory + Phase-3 synthesis + Phase-5 ADRs + Phase-6 specs. | architectures/v3/corpus-inventory.md + ARCHITECTURE-V3-SYNTHESIS-PLAN.md Phases 1-6 |
| §2.1.2 "enough research" trigger | `absorbed` | v3's Phase-1 saturation + Phase-3 contradiction-counting fulfill this; U-C inherits via Phase-3.5.5 RG-flag close criterion. | architectures/v3/corpus-inventory.md + contradictions.md |
| §2.1.3 folding policy | `not-applicable-to-candidate-mandate` | Document-management discipline at synthesis-process level; not a candidate-specific architectural primitive. | — |

### §2.3 Notes

User-stated constraints (UC1-UC8) are already in `constraints-extracted.md` and NOT Phase-7 scope. U-C-specific note: research-plan.md's substrate-vendor recommendation OQs (knowledge-graph vendor choice; LSP/tree-sitter choice) are Phase-5 ADR territory for U-C's P-22 / P-23 substrate dependencies per X_UNM_B inheritance — but vendor selection is operator-deployment choice, not v3-architecture-level adoption.

## §3 — archive/synthesis-v1-v2/00-synthesis.md

### §3.0 File header

Round-1 v2 synthesis post-primary-source-access. Canonical entry for F1-F20. 5020 words. **D-1 through D-7 defaults sourced from this file; verified per-candidate in §1.5 above.**

### §3.1 Enumeration

- §3.1.1 (claim) §2.1 Specs become the primary artifact (D-1 default).
- §3.1.2 (claim) §2.2 Scenarios live outside the codebase (D-2 default).
- §3.1.3 (claim) §2.3 Validation harnesses are the real engineering.
- §3.1.4 (claim) §2.4 The agent is "an LLM running tools in a loop" (D-3 default).
- §3.1.5 (claim) §2.5 Knowledge accumulates between cycles.
- §3.1.6 (claim) §2.6 Single-threaded human supervision tops out at cognitive ceiling.
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
| §3.1.1 specs primary artifact (D-1) | `absorbed (with adaptation — verified at §1.5)` | D-1 reframed as "frozen anchor is durable"; anchor.kind=architecture-rule is the spec analogue with stronger typing. | specs/u-c.md §3 distinctive methodology decision 2 |
| §3.1.2 scenarios outside codebase (D-2) | `absorbed (verified at §1.5)` | U-C binds D-2 via P-08 scenario storage; not challenged (unlike BF-S). | specs/u-c.md §4 holdout binding |
| §3.1.3 validation harnesses are real engineering | `absorbed` | U-C's P-32 distance estimator + P-19 dispatcher + P-08 scenario storage ARE the validation harness as substrate primitives. | specs/u-c.md §2 + §3 + §4 holdout |
| §3.1.4 Agent=LLM-in-loop (D-3) | `challenged (verified at §1.5)` | U-C explicitly extends to `Agent = Model + Harness + Anchor-Context` per §6 final open-carry. | specs/u-c.md §6 D-3 challenge |
| §3.1.5 knowledge accumulates between cycles | `absorbed (with adaptation)` | U-C binds via pattern → standard promotion through anchor mutation queue (always L4); Brier pace-layer framing is the inheritance mechanism. | specs/u-c.md §3 distinctive methodology decision 2 + §4 knowledge-promotion |
| §3.1.6 single-threaded human ceiling | `absorbed (with adaptation)` | U-C's earned-lights-out trajectory (anchor accumulation lowers human-required share over time) directly addresses cognitive ceiling. | specs/u-c.md §3 distinctive methodology decision 2 |
| §3.1.7 human leverage upstream/downstream | `absorbed` | U-C dispatcher routes human-required to upstream (anchor-edit always L4 with cooling-off) and downstream (far-anchor review). | specs/u-c.md §3 step 4 + §4 honesty |
| §3.1.8 tiered ceremony | `absorbed (verified)` | U-C's three regimes (near-anchor lights-out / mid-distance Augmentation / far-anchor human-required) IS the tiered-ceremony shape, distance-keyed. | specs/u-c.md §3 step 4 |
| §3.1.9 cost first-class (D-5) | `absorbed (with adaptation — verified at §1.5)` | Per-distance cost ceilings replace single-global; CTR-E1 cost-variance addressed. | specs/u-c.md §4 cost-ceiling |
| §3.1.10 human-review tension | `absorbed` | U-C's three regimes resolve the tension: tiered-by-distance, with hard-floor escape hatch (contradiction_flag, anchor-edit). | specs/u-c.md §3 step 4 |
| §3.1.11 persona vs graph-node tension | `not-applicable-to-candidate-mandate` | U-C is methodology-thin and front-end-agnostic per §3 distinctive decision 3; persona vs graph-node is plug-in choice, not substrate. | — |
| §3.1.12 spec format tension | `absorbed (with adaptation)` | U-C's typed anchor envelope (`kind / content / frozen-since / mutation-protocol`) takes a definite spec-format position — typed structured envelope, not prose. | specs/u-c.md §2 P-28 anchor envelope + ADR 0059 |
| §3.1.13 knowledge architecture tension | `absorbed (with adaptation)` | U-C explicitly binds Brier pace-layer (slow layers anchor fast) per §3 distinctive methodology decision 2; pace-layer pick on the DAG side. | specs/u-c.md §3 distinctive methodology decision 2 |
| §3.1.14 adversarial review tension | `absorbed (with adaptation)` | U-C binds adversarial-as-cross-model-judge attribute at mid-distance dispatch (P-14 routing); separate-role version absorbed via Patrol-tier P-06 detector. | specs/u-c.md §3 step 4 + §4 bias-guard |
| §3.1.15 parallel-agent + human-role tension | `tbd` | U-C front-end-agnostic on coordination medium (§3 distinctive decision 3); parallel-agents tension surfaces in Phase-8 lean-eval. | — |
| §3.1.16 cross-cutting primitives | `absorbed (silently — flagged for auditor)` | v3 has `primitives/index.md`; the 00-synthesis §5 list informed earlier phases but isn't directly cited by U-C spec. | — (flagged for silent-absorption auditor) |

### §3.3 Notes

The strongest U-C-specific absorption is §3.1.8 tiered ceremony — U-C's three regimes are a direct distance-keyed implementation of tiered-ceremony, with the substrate-enforced threshold tuple `(τ_low, τ_high)` as the calibration surface. Note that D-3 challenge (§3.1.4 / §1.5) is U-C's most distinctive deviation from the v2 default set: anchor-context becomes a first-class harness component, not optional context-window content.

## §4 — archive/synthesis-v1-v2/13-round-2-synthesis.md

### §4.0 File header

Round-2 v2 synthesis (6496 words). Promoted F21-F33 + Round-2 consensus C10-C16; proposed OpenHands+Overstory substrate stack as §6.2 / §8 recommendation. **Known-rejected v3 item: OpenHands+Overstory substrate stack** per Reviewer 6 D-H8 + [`constraints-extracted.md`](../constraints-extracted.md) explicit exclusion.

### §4.1 Enumeration

- §4.1.1 (claim) §1.1 C10 Agent = Model + Harness (D-3 default — covered in §1.5).
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
| §4.1.1 C10 D-3 | `challenged (verified at §1.5)` | U-C extends to `Agent = Model + Harness + Anchor-Context`. | specs/u-c.md §6 D-3 challenge |
| §4.1.2 C13 D-4 | `absorbed (verified at §1.5)` | Distance-gated dispatcher as substrate-enforced holdout. | specs/u-c.md §4 holdout |
| §4.1.3 C14 D-6 | `absorbed (verified at §1.5)` | Patrol-tier P-06 monitors distance-distribution drift (F47). | specs/u-c.md §3 step 5 + §4 three-loop |
| §4.1.4 C15 D-5 | `absorbed (with adaptation — verified at §1.5)` | Per-distance cost ceilings. | specs/u-c.md §4 cost-ceiling |
| §4.1.5 C16 D-7 | `absorbed (with adaptation — verified at §1.5)` | DistanceTuple in P-05 payload. | specs/u-c.md §2 + §3 step 5 |
| §4.1.6 falsified consensus items | `tbd` | Need per-item review of what was falsified vs preserved in v3 against U-C's anchor-distance framing. | — |
| §4.1.7 F21-F33 failure modes promoted | `absorbed (with adaptation)` | U-C spec invokes F33, F34, F37, F42, F46, F47, F51, F53 explicitly; F25 design-starvation in §3 hard-floor. | specs/u-c.md §3 + §4 + §6 (multiple F-mode invocations) |
| §4.1.8 sandbox + cost-ceilings as shared infrastructure | `absorbed` | U-C §2 commodity substrate baseline includes P-01 sandbox + P-02 cost ceilings. | specs/u-c.md §2 commodity substrate baseline |
| §4.1.9 CI/CD pipeline adaptation thesis | `absorbed (with adaptation)` | U-C's distance-gated dispatcher IS the CI/CD analogue: thresholds + regime routing + holdout enforcement at substrate. | specs/u-c.md §1 axis + §3 |
| §4.1.10 OpenHands+Overstory substrate stack | `rejected (explicitly-excluded-per-constraints-extracted, see constraints-extracted.md)` | **Known-rejected v3 item** per Reviewer 6 D-H8. Substrate-vendor choice is operator-deployment territory, not v3-architecture adoption. | — |
| §4.1.11 §7 Round-2 recommended path forward | `rejected (subsumed by v3 multi-candidate framing)` | v3 DEC-1 / DEC-1.a preserves multiple candidates for Phase-8 falsification; single-path collapsed. | — |
| §4.1.12 §8 Closing claim | `not-applicable-to-candidate-mandate` | Cross-architectural meta-claim; not per-candidate. | — |

### §4.3 Notes

U-C's F-mode coverage is the densest of the absorbed items here — §6 open-carries explicitly catalogue F33/F51 (intent_field_touches LLM-judged vulnerability), F47 (Goodhart on distance estimator), F8 (multi-month cold-start staleness), and F53 (voluntary-discipline fragility on cooling-off windows). The F47 mitigation via Patrol-tier residual detector is itself a Phase-5 ADR carry per §6 — incompletely-closed mitigation acknowledged in spec. **No ADR-0036 framing characterization required for U-C** (U-C does not claim P-30/ADR-0036; the per-candidate framing required for BF-L / U-A / D7-U-1 per [auto-007 §N.3 amendment](../decisions/auto-007-phase-7-dispatch-shape.md#decision-round-2) does NOT apply to U-C; verified at [u-c spec §2 "Framework + per-variant pairing check"](../specs/u-c.md#0-adr-citation-index) which explicitly disclaims P-29/P-30 binding).

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
| §5.1.1 four-architecture taxonomy | `absorbed (with adaptation)` | v3 candidate-registry preserves 4 v2 architectures as lineage; U-C is multi-lineage hybrid (Foundry+Refinery+Atelier) — taxonomy serves the lineage-mapping. | architectures/v3/candidate-registry.md |
| §5.1.2 failure-mode coverage matrix | `absorbed` | F1-F20 preserved as canonical; v3 extends to F49+. U-C covers in §10. | architectures/v3/failure-modes-v3.md |
| §5.1.3 when-to-pick-which decision criteria | `absorbed (with adaptation)` | v3 mandate-fit matrix per DEC-2 fulfills decision-criteria role; U-C's mandate-fit (3-of-5 `both`) is the unified-attempt evidence point. | architectures/v3/mandate-fit-matrix.md + specs/u-c.md §5 |
| §5.1.4 hybrid recommendations | `absorbed (with adaptation)` | **Load-bearing for U-C**: U-C IS the hybrid (Foundry+Refinery substrate inheritance + Atelier-default methodology). v2's hybrid framing prefigures unified-attempt candidates. | specs/u-c.md §1 + candidate-registry.md U-C entry |
| §5.1.5 shared infrastructure enumeration | `absorbed` | v3 common-substrate ADRs 0010-0017 are the shared-infrastructure enumeration; U-C consumes all of them. | specs/u-c.md §2 commodity substrate baseline |
| §5.1.6 shared roles, different emphasis | `absorbed (with adaptation)` | v3 §4 discipline binding per-candidate fulfills "different emphasis" framing; U-C's honesty-discipline carve-out is the U-C-specific emphasis. | specs/u-c.md §4 honesty carve-out |
| §5.1.7 Compound Atelier baseline | `rejected (explicitly-anchor-avoided, see archive-and-rebuild discipline)` | **Known-rejected v3 item** per Reviewer 6 D-H8 + UC6. v3 deliberately treats all candidates as independent; no baseline. | — |
| §5.1.8 selective borrows | `rejected (subsumed by v3 multi-candidate scoping principle)` | "Selective borrows" presupposes a baseline; v3 has none. U-C borrows from multiple v2 architectures without designating any as baseline. | — |
| §5.1.9 build shared infrastructure first | `absorbed` | v3 Phase-5 common-substrate ADRs precede candidate-specific work — direct match. U-C inherits via §2 commodity baseline. | docs/adr/0010-0017 + Phase-5 sequencing |

### §5.3 Notes

§5.1.4 hybrid recommendations is U-C's most distinctive absorption from this file: U-C is one of the v3 candidates that operationalises v2's "hybrid is sometimes right" intuition, but does so via substrate-level unification (single distance-estimator + single dispatcher framework parameterised by anchor.kind), not via per-mandate methodology selection. Compound Atelier baseline (§5.1.7) is the highest-priority known-rejected v3 item per archive-and-rebuild discipline.

## §6 — archive/architectures-v2/01-specification-refinery.md

### §6.0 File header

v2 Architecture 1 — Specification Refinery. "The spec is the product; the implementation is a probe." Layered spec discipline + revelation cycle + 5-mode failure classification. 3572 words. **Secondary v2-lineage for U-C** per §1 overview (Refinery change-request work-unit shape).

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
| §6.1.1 spec is durable artifact | `absorbed (with adaptation — verified at §1.5)` | D-1 reframed as "frozen anchor is durable"; anchor.kind=architecture-rule is the typed spec analogue. | specs/u-c.md §3 distinctive methodology decision 2 |
| §6.1.2 5-layer spec stack | `absorbed (with adaptation)` | U-C's anchor.kind enum `{intent-invariant, architecture-rule, standards-rule, live-test, runtime-trace}` is a typed-5-kind analogue of Refinery's L1-L5 layering, with Brier pace-layer alignment replacing Refinery's spec-formality gradient. | specs/u-c.md §2 P-28 anchor envelope + ADR 0059 |
| §6.1.3 stable identifier discipline | `absorbed` | U-C's content-hash preimage including `frozen-since` + `mutation-protocol` makes silent re-dating structurally impossible (per ADR 0059 immutability-metadata-first contract). | specs/u-c.md §2 P-28 anchor envelope + ADR 0059 |
| §6.1.4 revelation cycle (7-phase) | `not-applicable-to-candidate-mandate` | Refinery-specific cycle structure; U-C's 5-step substrate-driven cycle is distance-gated, not revelation-shaped. | — |
| §6.1.5 5-mode failure classification | `tbd` | Whether U-C's F-mode coverage (F33/F47/F51/F8/F53) replicates / extends / supersedes Refinery's 5-mode classification is Phase-8 lean-eval question. | — |
| §6.1.6 manager loop | `absorbed (with adaptation)` | U-C's three-loop discipline (ADR 0026) materialises "compound" step as Patrol-tier monitoring (P-06) per §4 three-loop binding. | specs/u-c.md §4 three-loop |
| §6.1.7 showboat trajectory artifacts | `absorbed (with adaptation)` | U-C extends P-05 payload with DistanceTuple at write time — distance-keyed trajectory IS the showboat-trajectory analogue with stronger typing. | specs/u-c.md §2 distance-keyed P-05 + §3 step 5 |
| §6.1.8 implementation roadmap | `not-applicable-to-candidate-mandate` | Architecture-specific deployment; v3 doesn't carry per-architecture roadmaps. | — |

### §6.3 Notes

U-C inherits more deeply from Refinery than BF-S did — both the spec-as-durable-artifact framing (D-1) AND the layered spec stack (§6.1.2 → U-C's anchor.kind enum) AND stable identifier discipline (§6.1.3 → U-C's immutability-metadata content-hash) all land in U-C with adaptation. This makes Refinery the second-strongest lineage signal in U-C's hybrid (after Foundry's regime-gated dispatch).

## §7 — archive/architectures-v2/02-compound-atelier.md

### §7.0 File header

v2 Architecture 2 — Compound Atelier. "Each unit of work makes the next easier." Queue + workpad + persona panel + accumulated `docs/solutions/`. v2's recommended baseline. 4515 words. **Default-methodology lineage for U-C** per §1 overview (Compound Engineering loop is U-C's default per-cycle methodology, plug-in replaceable).

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
| §7.1.1 compounding core thesis | `absorbed` | U-C's earned-lights-out trajectory IS compounding: anchor accumulation makes successive cycles cheaper via leftward distance-distribution shift. | specs/u-c.md §3 distinctive methodology decision 2 |
| §7.1.2 knowledge accumulation between cycles | `absorbed` | Pattern → standard promotion through anchor mutation queue (always L4). | specs/u-c.md §4 knowledge-promotion |
| §7.1.3 artifact stack (specs/knowledge/workpad) | `absorbed (with adaptation)` | U-C maps to typed-anchor-envelope (P-28) + DistanceTuple-keyed trajectory (P-05) + P-08 scenario storage — substrate-level typed analogue. | specs/u-c.md §2 |
| §7.1.4 workshop chain (persona workshops) | `not-applicable-to-candidate-mandate` | U-C is methodology-thin and front-end-agnostic per §3 distinctive decision 3; persona-workshop is plug-in. | — |
| §7.1.5 researcher fan-out | `absorbed (with adaptation)` | U-C's P-32 distance estimator three-leg parallelism (P-22 structural + decision-table pace-layer + P-14 LLM judge) is the substrate fan-out analogue. | specs/u-c.md §2 P-32 + §3 step 2 |
| §7.1.6 reviewer panel | `absorbed (with adaptation)` | U-C binds cross-model judging at mid-distance dispatch via P-14 — judging diversity at substrate, not at workshop layer. | specs/u-c.md §4 bias-guard |
| §7.1.7 synthesis and curation | `absorbed (with adaptation)` | Anchor mutation queue is U-C's synthesis-and-curation substrate: pattern → standard promotion is the curation mechanism. | specs/u-c.md §3 distinctive decision 1 |
| §7.1.8 conductor orchestrator | `not-applicable-to-candidate-mandate` | U-C's distance-gated dispatcher IS the orchestrator; conductor-persona is methodology-layer plug-in. | — |
| §7.1.9 workpad protocol | `absorbed (with adaptation)` | U-C's P-08 scenario storage + P-01 sandbox provide the workpad-equivalent substrate. | specs/u-c.md §2 |
| §7.1.10 tiered cycle scope | `absorbed (verified)` | **Load-bearing for U-C**: three regimes (near-anchor / mid-distance / far-anchor) IS the tiered-scope shape, distance-keyed and substrate-enforced. | specs/u-c.md §3 step 4 |
| §7.1.11 severity × autofix axes | `absorbed (silently — flagged for auditor)` | Orthogonal-axes framing influenced v3's mandate-fit-per-(architecture × work-unit-class) DEC-2 schema; not explicitly cited in U-C spec. | — (flagged for silent-absorption auditor) |
| §7.1.12 residual work gate | `absorbed (with adaptation)` | U-C's P-19 dispatcher hard-floor table (contradiction_flag, anchor-edit) provides the substrate-level residual-work gating. | specs/u-c.md §3 step 4 hard floors |
| §7.1.13 three memory tiers | `absorbed (with adaptation)` | U-C explicitly binds Brier pace-layer framing per §3 distinctive decision 2; pace-layers ARE the v3-extended memory-tier framing. | specs/u-c.md §3 distinctive decision 2 + ADR 0059 |
| §7.1.14 implementation roadmap | `not-applicable-to-candidate-mandate` | Architecture-specific deployment. | — |

### §7.3 Notes

U-C's Atelier inheritance is shallower than BF-S's — Compound Engineering loop is U-C's default methodology, but methodology is thin over substrate, so most Atelier primitives land as methodology-plug-in opportunities (workshop, conductor, persona) rather than substrate bindings. The tiered cycle scope (§7.1.10) is the deepest absorption: U-C's three regimes are a more-typed implementation of Atelier's tiered scope, with distance-keyed thresholds replacing severity-based tiers. Silent-absorption flag on §7.1.11 (severity × autofix orthogonal axes → DEC-2 schema) is genuine and shared across multiple candidate audits.

## §8 — archive/architectures-v2/03-phase-gated-foundry.md

### §8.0 File header

v2 Architecture 3 — Phase-Gated Foundry. "Pre-agile structured methodologies become the right shape when agents make them fast." Phase-bound experts, formal templates (SRS, SAD, DD), RTM, gate boards. 4610 words. **Primary v2-lineage for U-C** per §1 overview (regime-gated dispatch + L4 human-required gates).

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
| §8.1.1 structured pre-agile core thesis | `absorbed (with adaptation)` | U-C's regime-gated dispatch + L4 anchor-edit gates inherit Foundry's "structured methodology gets the agent's speed dividend" framing. | specs/u-c.md §3 step 4 + §1 axis |
| §8.1.2 phase model + V&V pairing | `absorbed (with adaptation)` | U-C's distance regimes (near/mid/far) and substrate-enforced V&V (cross-model judge at mid-distance, holdout at near-anchor) parallel Foundry's phase + V&V pairing. | specs/u-c.md §3 step 4 + §4 bias-guard |
| §8.1.3 Configuration Management discipline | `absorbed (with adaptation)` | ADR 0059 anchor envelope immutability-metadata-first contract (content-hash preimage including frozen-since + mutation-protocol) is substrate-level CM. | specs/u-c.md §2 P-28 anchor envelope + ADR 0059 |
| §8.1.4 defect-of-origin table | `tbd` | U-C's P-24 attribution surface is not explicitly bound in spec (vs BF-S which binds P-24 explicitly); defect-of-origin traceability may be inherited via P-05 trajectory cycle_id but not verified. | — |
| §8.1.5 RUP-style discipline × phase matrix | `not-applicable-to-candidate-mandate` | Foundry-specific; U-C binds all 10 disciplines uniformly at substrate per §4. | — |
| §8.1.6 iteration within phases | `absorbed (with adaptation)` | U-C's cycle loop iterates within each regime; "compound" step is Patrol-tier meta-loop iteration. | specs/u-c.md §3 + §4 three-loop |
| §8.1.7 V&V-side independent roles + different model family | `absorbed (verified)` | U-C §3 step 4 mid-distance "cross-family judge required (F46 mitigation)" via P-14. | specs/u-c.md §3 step 4 + §4 bias-guard |
| §8.1.8 CM as spine | `absorbed (with adaptation)` | U-C's anchor mutation queue (always L4, cooling-off, Caremark-style AILCCP log) IS the CM-as-spine analogue at substrate level. | specs/u-c.md §3 distinctive decision 1 + §4 honesty |

### §8.3 Notes

Foundry is U-C's strongest v2 lineage — six-of-eight Foundry items land deeply, including the CM-as-spine framing operationalised at substrate (anchor mutation queue + ADR 0059 immutability metadata). U-C's "anchor-edit is a substrate primitive" (§3 distinctive decision 1) is the load-bearing inheritance: Foundry's gate-bound transitions become U-C's distance-gated regime transitions, with the special-case for anchor-edit modeling Foundry's "decision-of-record" change-control discipline. **One TBD** on §8.1.4 defect-of-origin — needs Phase-7 follow-up to confirm whether U-C's P-05 cycle_id provides sufficient defect-of-origin traceability or whether explicit P-24 attribution binding should be added in a Phase-7 spec patch.

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
| §9.1.1 population + selection core thesis | `not-applicable-to-candidate-mandate` | Tournament-specific population-based methodology; U-C is single-cycle distance-gated. | — |
| §9.1.2 genome structure | `not-applicable-to-candidate-mandate` | Tournament-specific artifact. | — |
| §9.1.3 model-family diversity as structural | `absorbed (verified)` | U-C §3 step 4 + §4 bias-guard bind cross-model-family judging as structural via P-14 (F46 mitigation). | specs/u-c.md §3 step 4 + §4 bias-guard |
| §9.1.4 generation cycle | `not-applicable-to-candidate-mandate` | Tournament-specific. | — |
| §9.1.5 predator agent | `rejected (subsumed by Patrol-tier residual detector)` | U-C substitutes Tournament's predator-agent with Patrol-tier P-06 distance-distribution drift detector + F47 residual monitor; substrate substitution not runtime predator. | — |
| §9.1.6 loops within loops | `absorbed (with adaptation)` | U-C §4 three-loop discipline + Patrol-tier meta-loop is the analogue; meta-loop ≠ tournament-loop (no population-vs-tournament-vs-meta distinction). | specs/u-c.md §4 three-loop |
| §9.1.7 independence policy | `absorbed` | U-C §3 step 4 cross-model judge at mid-distance enforces builder-judge independence at substrate. | specs/u-c.md §3 step 4 + §4 bias-guard |
| §9.1.8 scaling | `tbd` | U-C's distance-distribution-shift trajectory framing may inherit Tournament's scaling lessons; F8 multi-month cold-start staleness is the related Phase-8 carry. | — |

### §9.3 Notes

Tournament lineage is the thinnest for U-C — only the cross-model-family diversity discipline (§9.1.3) and independence policy (§9.1.7) land at substrate. Predator-agent (§9.1.5) is rejected with reason (Patrol-tier substrate substitution). U-C does NOT carry Tournament's population-based shape; its compounding is distance-distribution shift over time, not parallel-genome selection.

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
| §10.1.1 F1 Hallucination | `absorbed` | U-C §4 bias-guard binding (cross-model judge at mid-distance) + Patrol-tier residual detection. | specs/u-c.md §3 step 4 + §4 bias-guard |
| §10.1.2 F2 Reward hacking | `absorbed (with adaptation)` | U-C §6 explicitly carries F47 Goodhart-resistance + P-32 partial Goodhart-resistance + Patrol-tier residual detector spec (Phase-5 ADR carry). | specs/u-c.md §6 F47 open-carry |
| §10.1.3 F3 Spec-completeness | `absorbed (with adaptation)` | Anchor.kind enum + ADR 0059 immutability-metadata-first contract makes anchor-set completeness substrate-typed. | specs/u-c.md §2 P-28 anchor envelope |
| §10.1.4 F4 Code quality | `absorbed (with adaptation)` | U-C §4 bias-guard cross-model judging + distance-gated dispatcher prevents far-anchor lights-out. | specs/u-c.md §3 step 4 + §4 bias-guard |
| §10.1.5 F5 Cognitive ceiling | `absorbed (with adaptation)` | U-C's earned-lights-out trajectory lowers human-required share over time; cognitive ceiling is distance-typed. | specs/u-c.md §3 distinctive decision 2 |
| §10.1.6 F6 Cognitive debt | `absorbed` | U-C P-05 trajectory + cognitive-escrow binding (ADR 0019) at the prompt→response interval. | specs/u-c.md §4 cognitive escrow |
| §10.1.7 F7 Normalization of deviance | `absorbed (with adaptation)` | Patrol-tier P-06 monitors distance-distribution drift (F47 Goodhart residual) — substrate-level deviance resistance. | specs/u-c.md §3 step 5 + §6 F47 carry |
| §10.1.8 F8 Stale knowledge | `tbd` | **Open-carry**: U-C §6 explicitly carries F8 staleness over multi-month cold-start as Phase-8 lean-eval candidate (cooling-off windows F53-vulnerable). | specs/u-c.md §6 F8 open-carry |
| §10.1.9 F9 Spec overfitting | `absorbed (with adaptation)` | Anchor.kind typing + Brier pace-layer alignment forces explicit anchor-set authoring; overfitting becomes typed concern. | specs/u-c.md §2 P-28 + §3 distinctive decision 2 |
| §10.1.10 F10 Findings disappear | `absorbed` | U-C P-05 trajectory with DistanceTuple payload + AILCCP immutable log on anchor mutation queue closes finding-disappearance at substrate. | specs/u-c.md §3 step 5 + §3 distinctive decision 1 |
| §10.1.11 F11 Renumbering | `absorbed (with adaptation)` | ADR 0059 immutability-metadata-first contract (frozen-since + mutation-protocol in content-hash preimage) handles anchor-renumbering / silent re-dating. | specs/u-c.md §2 P-28 + ADR 0059 |
| §10.1.12 F12 Lethal trifecta | `absorbed (with adaptation)` | U-C §4 trifecta closure binding (ADR 0027) at P-08 holdout + P-12 linter — substrate-enforced. | specs/u-c.md §4 trifecta closure |
| §10.1.13 F13 Missing-config | `tbd` | U-C does not explicitly bind P-23 dependency-impact graph for config-drift detection (only for graph_distance computation); F13 coverage unclear. | — |
| §10.1.14 F14 Attribution collapse | `tbd` | U-C does not explicitly bind P-24 attribution store (unlike BF-S); attribution may be inherited via P-05 cycle_id but not verified. | — |
| §10.1.15 F15 Single-prompt collapse | `absorbed (with adaptation)` | U-C's cross-model judging at mid-distance + three-leg distance estimator (structural + pace-layer + LLM-judge) provides structural diversity. | specs/u-c.md §2 P-32 + §3 step 4 |
| §10.1.16 F16 Resume-fidelity | `absorbed` | U-C P-05 trajectory + DistanceTuple-keyed event provides resume anchor. | specs/u-c.md §3 step 5 |
| §10.1.17 F17 Parallel agents on shared dirs | `tbd` | U-C front-end-agnostic on coordination medium (§3 distinctive decision 3); parallel-agents discipline is methodology-layer call. | — |
| §10.1.18 F18 Prose-spec rigor | `absorbed (with adaptation)` | Anchor.kind typing + ADR 0059 typed envelope schema substitutes prose-spec with typed-envelope rigor at substrate. | specs/u-c.md §2 P-28 + ADR 0059 |
| §10.1.19 F19 Model-floor dependency | `absorbed (verified)` | U-C §4 bias-guard cross-model judging via P-14 surfaces model-floor explicitly per F46. | specs/u-c.md §4 bias-guard |
| §10.1.20 F20 Maintenance asymmetry | `absorbed (with adaptation)` | U-C distance-gated cycle is uniform across work-unit-classes; mandate becomes parameter (anchor.kind) rather than asymmetry source. | specs/u-c.md §1 axis + §5 mandate-fit |
| §10.1.21 A1 Refinery coverage row | `not-applicable-to-candidate-mandate` | Coverage row characterizes Architecture 1, not U-C. Informational. | — |
| §10.1.22 A2 Atelier coverage row | `not-applicable-to-candidate-mandate` | Coverage row characterizes Architecture 2 (U-C's default-methodology lineage); U-C's F-mode coverage tracked above. | — |
| §10.1.23 A3 Foundry coverage row | `not-applicable-to-candidate-mandate` | Coverage row characterizes Architecture 3 (U-C's primary substrate lineage); per-row scoring is per-Foundry, not per-U-C. | — |
| §10.1.24 A4 Tournament coverage row | `not-applicable-to-candidate-mandate` | Coverage row characterizes Architecture 4. | — |

### §10.3 Notes

15-of-20 F-modes are absorbed (F1, F2, F3, F4, F5, F6, F7, F9, F10, F11, F12, F15, F16, F18, F19, F20) — F2 (Goodhart) and F19 (model-floor) explicitly tied to U-C's open-carries. 4 are TBD (F8, F13, F14, F17) — F8 is an open-carry (Phase-8 lean-eval), F13/F14/F17 are coverage-completeness gaps that may warrant Phase-7 spec patches. F8 staleness over multi-month cold-start is U-C's most material own open-carry per §6. **No ADR-0036 framing required** (U-C does not claim P-30/0036; per [u-c spec §0 framework-pairing check](../specs/u-c.md#0-adr-citation-index)). 4 per-architecture coverage-strength rows are informational; U-C's own absorption pattern (Foundry-strong + Refinery-deep + Atelier-shallow + Tournament-thin) is documented above.

## §11 Summary

**Per-token cell counts (matches YAML frontmatter):**

| Token | Count |
|---|---|
| `absorbed` (incl. with-adaptation, verified, silently, challenged) | 38 |
| `rejected (reason)` | 8 |
| `not-applicable-to-candidate-mandate` | 16 |
| `tbd` | 6 |
| **Total (unique-verdict)** | **68** |

Per-archive-file cells: §2.2 (3) + §3.2 (16) + §4.2 (12) + §5.2 (9) + §6.2 (8) + §7.2 (14) + §8.2 (8) + §9.2 (8) + §10.2 (24) = 102. Unique-verdict tally (68) deduplicates D-1..D-7 rows that appear in both §1.5 (7 rows) and §3.2 / §4.2 cells (D-3/D-4/D-5/D-6/D-7 → 5 absorbed-via-§1.5 + 5 absorbed-via-§4.2 cells, with D-1/D-2 covered only in §3.2). Discrepancy: ~34 cells are D-default duplications across §1.5 / §3 / §4. The frontmatter YAML carries the unique-verdict count.

**High-confidence absorbed cells:**
- D-4, D-5 (with adaptation), D-6, D-7 (with adaptation) verified per §1.5; D-3 explicitly challenged per §1.5 + §6 (U-C's most distinctive deviation).
- §8.1.3 CM discipline → ADR 0059 anchor envelope immutability-metadata-first (load-bearing Foundry inheritance).
- §7.1.10 tiered cycle scope → three regimes (load-bearing Atelier inheritance reshaped).
- §5.1.4 hybrid recommendations → U-C IS the v3 operationalisation of v2's hybrid-is-sometimes-right intuition.

**Surfaced TBDs (require lead-agent reconciliation or Phase-8 follow-up):**

1. §3.1.15 parallel-agent + human-role tension — U-C front-end-agnostic on coordination medium; Phase-8 surface.
2. §4.1.6 falsified consensus items — per-item review of what was falsified vs preserved in v3 against U-C's anchor-distance framing.
3. §6.1.5 Refinery 5-mode failure classification — Phase-8 lean-eval candidate.
4. §8.1.4 Foundry defect-of-origin table — **potential Phase-7 spec patch**: U-C may need explicit P-24 attribution binding (currently only inherited via P-05 cycle_id, not verified).
5. §9.1.8 Tournament scaling — F8 multi-month cold-start staleness is U-C's related Phase-8 lean-eval candidate.
6. §10.1.8 F8 staleness — U-C §6 open-carry; Phase-8 lean-eval.
7. §10.1.13 F13 Missing-config — coverage-completeness gap; **potential Phase-7 spec patch** to explicitly bind P-23 for config-drift detection.
8. §10.1.14 F14 Attribution collapse — coverage-completeness gap; **potential Phase-7 spec patch** to explicitly bind P-24 (paired with §8.1.4 TBD).
9. §10.1.17 F17 Parallel agents on shared dirs — methodology-layer call.

**Silent-absorption auditor flags (for cross-spec reconciliation):**

- §3.1.16 cross-cutting primitives — v3 `primitives/index.md` likely inherited the framing without explicit citation (shared across multiple candidate audits).
- §7.1.11 severity × autofix orthogonal axes — likely informed DEC-2 mandate-fit-per-(architecture × work-unit-class) schema (shared across multiple candidate audits).

**Known-rejected items confirmed:**

- §4.1.10 OpenHands+Overstory substrate stack — `rejected (explicitly-excluded-per-constraints-extracted)`.
- §5.1.7 Compound Atelier as baseline — `rejected (explicitly-anchor-avoided)`.
- §5.1.8 selective borrows — `rejected (subsumed by v3 multi-candidate scoping principle)`.
- §9.1.5 Predator agent — `rejected (subsumed by Patrol-tier residual detector)`.

**U-C-specific notable findings:**

- **D-3 challenge is U-C's most distinctive deviation.** Anchor-context as first-class harness component (`Agent = Model + Harness + Anchor-Context`) is the load-bearing extension; resolution deferred to Phase-3 cross-mandate review.
- **Foundry > Refinery > Atelier > Tournament in lineage depth.** Foundry's CM-as-spine + regime-gated dispatch lands deepest; Refinery's layered spec stack + stable identifier discipline lands second; Atelier's tiered cycle scope + compounding land at methodology layer; Tournament contributes only cross-model diversity + independence policy.
- **Three Phase-7 spec-patch candidates surfaced.** §8.1.4 / §10.1.13 / §10.1.14 — all three touch attribution / config-drift / defect-of-origin coverage that U-C's spec may inherit weakly via P-05 cycle_id but does not explicitly bind. **Important**: per auto-007 patch threshold (≤3 candidates; ≥4 triggers Phase-7-followup deferral), these three TBDs likely consolidate into a single U-C patch adding explicit P-23 / P-24 binding to §2 + §4 — counts as ONE candidate-needing-patches per the threshold rule.
- **No ADR-0036 framing required** (U-C does not claim P-30/0036; verified at [u-c spec §0 framework-pairing check](../specs/u-c.md#0-adr-citation-index)). Silent-absorption auditor's cross-spec ADR-0036 framing audit will not touch U-C.
- **X_UNM_B cross-mandate inheritance documented.** U-C as unified-attempt explicitly inherits BF-L's structural-view P-26 components (P-22 + P-23) for brownfield Codebase-Model acquisition; intent_field_touches leg degrades to operator-attested + L3 fallback when no synthesised intent block exists.

## §12 References

**U-C spec + supporting docs:**

- [`architectures/v3/specs/u-c.md`](../specs/u-c.md) — U-C Phase-6 architecture spec (audit input; lead-agent-authored exemplar under auto-006).
- [`architectures/v3/candidate-registry.md` U-C entry](../candidate-registry.md#u-c--anchor-distance-factory-every-work-unit-parameterised-by-graph-distance-to-a-frozen-anchor) — registry entry for §1 lineage statement.
- [`architectures/v3/candidate-registry.md` U-C Phase-3.5.5 detail](../candidate-registry.md#u-c--anchor-distance-factory) — Phase 3.5.5 substrate-coverage detail.
- [`architectures/v3/substrate-requirements/u-c.md`](../substrate-requirements/u-c.md) — substrate-requirements summary (X_UNM_B inheritance specified).
- [`architectures/v3/tracks/unified-C.md`](../tracks/unified-C.md) — original Phase-3 track sketch.
- [`architectures/v3/primitives/overlap.md`](../primitives/overlap.md) — Phase-4.2 P-19 + P-28 framework-vs-variant verdicts.
- [`architectures/v3/decisions/auto-007-phase-7-dispatch-shape.md`](../decisions/auto-007-phase-7-dispatch-shape.md) — Phase-7 dispatch brief.
- [`architectures/v3/backfill-notes/bf-s.md`](./bf-s.md) — Phase-7 exemplar (this notes file inherits shape).

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

- U-C common substrate: [0010-0017](../../../docs/adr/).
- U-C discipline: [0018-0027](../../../docs/adr/).
- U-C framework + per-variant: [0028 (P-19 framework)](../../../docs/adr/0028-p-19-eligibility-regime-classifier.md), [0029 (P-28 framework)](../../../docs/adr/0029-p-28-typed-object-store.md), [0058 (P-19 U-C variant)](../../../docs/adr/0058-p-19-variant-u-c-distance-tuple.md), [0059 (P-28 U-C variant)](../../../docs/adr/0059-p-28-variant-u-c-anchor-envelope.md).
- U-C orphan: [0057 (P-32 distance estimator)](../../../docs/adr/0057-p-32-distance-estimator.md).
- U-C designed-system: [0031 (P-23)](../../../docs/adr/0031-p-23-dependency-impact-graph.md), [0032 (P-12)](../../../docs/adr/0032-p-12-deterministic-linter-framework.md).

**Constraints / decisions:**

- [`architectures/v3/constraints-extracted.md`](../constraints-extracted.md) — UC1-UC8 user constraints (source of known-rejected v3 item flags).
- [`architectures/v3/decisions-captured.md`](../decisions-captured.md) — DEC-1 / DEC-1.a / DEC-2.
- [`architectures/v3/AGENTS.md`](../../../AGENTS.md) — AGENTS-MD rules cited in self-check (a)-(g).
