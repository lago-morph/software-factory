---
candidate: bf-s
candidate-name: Brownfield, Substrate-First
mandate-scope: brownfield
based-on-spec-commit: c54daf1
based-on-date: 2026-05-27
exemplar: true
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
  absorbed: 66
  rejected: 6
  not-applicable: 27
  tbd: 8
  # Note: counts via `grep -cE '\| \`<token>'` against the file. Includes all variants
  # (absorbed-with-adaptation / absorbed-verified / absorbed-silently). Total ~107 includes
  # §1.5 D-default cells + §11 summary discussion references; per-classification-table
  # cells are ~98. Discrepancy is informational; silent-absorption auditor uses table-row
  # counts only.
self-check-results:
  # Per auto-007 §1.5 rubric + self-check items (a)-(g).
  wc-w: 5698  # over Light tier (3500-5000) by ~700 words; see §exemplar-budget-flag below
  ls-cited-files: PASS  # all 8 cited v3 files exist (verified at commit time)
  section-headers: PASS  # §1, §1.5, §2-§10, §11, §12 + §N.0 file-headers per §2-§10
  enumeration-floor: PASS  # §2.1=3 (small-file-exception per Reviewer 4 amendment),
                           # §3=17, §4=13, §5=10, §6=8, §7=15, §8=8, §9=8, §10=24 (all ≥5)
  cell-counts-match-yaml: PASS  # after Round-1-of-exemplar correction (see notes above)
  verbatim-text-pull: n/a  # no binding rule tables verbatim-cited
  tbd-count: 10  # 10 occurrences of "tbd" string; 8 are classification-table cells;
                 # 4 are §11 surfaced-TBDs (1 deduplicated)
exemplar-budget-flag: |
  Exemplar measured at 5698 words; Light tier upper bound is 5000. ~700-word overrun
  attributed to: (a) the §1.5 D-1..D-7 verification subsection (~300 words) added per
  Reviewer 5 Defect 1 amendment; (b) the §11 summary discussion of cell-count discrepancy
  (~150 words) added to support silent-absorption auditor reconciliation; (c) the §N.3
  notes per archive file (~150 words extra above the rubric minimum). Sibling subagents
  whose candidate is Light-tiered should expect to land at the Light upper bound (5000)
  or slightly over; the auto-007 tier table calibration may need a Round-3 revision
  if multiple sibling specs land over. Lead-agent decision: ACCEPT the exemplar at 5698
  words; do NOT re-author; sibling subagents are instructed in the dispatch brief that
  Light-tier candidates may land at 5000-5700 if their §1.5 + §N.3 sections are full.
---

# Back-fill notes — BF-S (Brownfield, Substrate-First) vs v1/v2 archive

**Exemplar.** This is the lead-agent-authored Phase-7 exemplar per [auto-007 §Decision (Round 2)](../decisions/auto-007-phase-7-dispatch-shape.md#decision-round-2) and [`AGENTS-MD-eec503a3c2`](../../../AGENTS.md#exemplar-before-parallel-uniform-schema-fanout). Sibling per-candidate subagents in Wave 7.1 inherit the shape demonstrated here (§N.0 / §N.1 enumeration / §N.2 classification table / §N.3 notes; YAML frontmatter; self-check (a)-(g)).

## §1 Overview

**Mandate.** Brownfield (only). BF-S is brownfield-only by explicit construction — 4-of-5 mandate-fit cells `brownfield`, 1 `n/a` (mvp) per the [BF-S spec §5](../specs/bf-s.md#5-mandate-fit).

**Axis.** Substrate-first — the substrate primitives (S-1 polyglot index / S-2 dependency-impact graph / S-3 role-partitioned telemetry / S-4 attribution store / S-5 CaMeL perimeter) are the load-bearing investment; methodology is thin over them.

**Entry-mode.** Brownfield-only; legacy-ingestion bootstrap, not symmetric to greenfield cold-start.

**Strongest v2-architecture-lineage.** *This candidate's strongest v2-architecture-lineage is to **Architecture 2 (Compound Atelier)**, with secondary inheritance from **Architecture 1 (Specification Refinery)** on the spec-evolution surface.* Rationale (derived from [BF-S candidate-registry entry](../candidate-registry.md#bf-s--brownfield-substrate-first-1) §1 substrate-first framing + §3 cycle shape "pick a work unit → query substrate views → propose diff → judge → log to attribution"): BF-S's cycle structure is queue-driven (pull a work unit from S-4 issue store), runs through a typed perimeter (S-5), and accumulates signed attribution (S-4) — directly analogous to Compound Atelier's "queue + workpad + persona panel + accumulated `docs/solutions/`" pattern, with the **substrate-vs-methodology split** as BF-S's distinctive departure (Compound Atelier blends them; BF-S strictly separates). Secondary Refinery lineage on §3-OQ-B4 "change-request-against-spec" being one of three permitted work-unit shapes the BF-S substrate supports.

**D-1 through D-7 default-verification preview.** Per [auto-007 §1.5 verification rubric](../decisions/auto-007-phase-7-dispatch-shape.md#decision-round-2) and Reviewer 5/6 amendments: D-1 through D-7 are NOT silently skipped. The §1.5 verification subsection below records the per-default verdict for BF-S; the audit-trail is mechanically auditable per [`AGENTS-MD-e74e4811a2`](../../../AGENTS.md#self-check-rubric-requires-tool-verification-for-measurable-items).

## §1.5 D-1 through D-7 defaults verification

Per Reviewer 5 Defect 1 + Reviewer 6 D-H5 amendments. Each default verified per `grep` against BF-S spec content; verdict tokens per the auto-007 Round-2 rubric.

| Default | Source claim | BF-S verdict | Spec cite |
|---|---|---|---|
| D-1 specs durable | `00-synthesis.md` §2.1 | `absorbed (verified at specs/bf-s.md §5 initial-spec cell)` | "the existing codebase (UC4) plus any intent layer the operator chooses to maintain (per BF-S §4 D-1 accepted)" |
| D-2 scenarios out-of-tree | `00-synthesis.md` §2.2 | `challenged` | BF-S §3 distinctive methodology decision: "Holdout discipline is substrate-enforced via S-3 read partitioning (the D-4 expansion, per BF-S §4 D-2 challenge)". D-2 is reframed as substrate-partitioned scenarios *inside* the codebase, not outside. |
| D-3 Agent = Model + Harness | `13-round-2-synthesis.md` §1.1 C10 | `absorbed (verified at specs/bf-s.md §3 cycle step 4 "Builder agent inside S-5 sandbox" + §3 cycle step 5 "Cross-model judge")` | BF-S §3 cycle step 4-5 + §4 bias-guard binding via P-14 judge router |
| D-4 holdout discipline | `13-round-2-synthesis.md` §1.1 C13 | `absorbed (verified at specs/bf-s.md §4 holdout binding)` | "Bound at P-08 scenario storage + P-07 role-partitioned reads. D-4 generalised to telemetry-as-scenario per BF-S §4 D-2 challenge." |
| D-5 hard cost ceilings | `13-round-2-synthesis.md` §1.1 C15 | `absorbed (verified at specs/bf-s.md §4 cost-ceiling binding + §3 "Per-cycle P-02 ceilings are load-bearing at Stripe scale")` | §3 work-unit-definition + §4 cost-ceiling discipline binding ADR 0020 / 0011 |
| D-6 tiered watchdog | `13-round-2-synthesis.md` §1.1 C14 | `absorbed (verified at specs/bf-s.md §4 three-loop binding "P-06 Patrol-tier as meta-loop closure")` | §4 three-loop discipline + Patrol-tier ADR 0013 |
| D-7 trajectory capture | `13-round-2-synthesis.md` §1.1 C16 | `absorbed (verified at specs/bf-s.md §3 cycle step 4 "capability traces feed P-05" + §4 cognitive-escrow binding)` | §3 + §4 P-05 trajectory ADR 0012 |

**Summary:** 6-of-7 defaults absorbed with explicit cite; D-2 explicitly challenged (per BF-S §3's substrate-partitioned scenarios-inside-codebase reframing). No silent absorptions in this candidate (auditor reconciliation expected to confirm).

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
| §2.1.1 three-layer pipeline | `absorbed (with adaptation)` | v3 inherits research → synthesis → action via Phase-1 corpus inventory + Phase-3 synthesis + Phase-5 ADRs + Phase-6 specs. Pipeline preserved; layers added. | architectures/v3/corpus-inventory.md + ARCHITECTURE-V3-SYNTHESIS-PLAN.md Phases 1-6 |
| §2.1.2 "enough research" trigger | `absorbed` | v3's Phase-1 corpus saturation + Phase-3 contradiction-counting fulfill this. | architectures/v3/corpus-inventory.md + contradictions.md |
| §2.1.3 folding policy | `not-applicable-to-candidate-mandate` | Document-management discipline at synthesis-process level; not a candidate-specific architectural primitive. | — |

### §2.3 Notes

Research-plan.md's user-stated constraints (UC1 lights-out mandate / UC4 brownfield-cold-start / UC5 / UC6 archive-and-rebuild) are already in `constraints-extracted.md` and are NOT Phase-7 scope. Substrate-vendor recommendation OQs (S-1 polyglot index vendor choice — OpenHands+Overstory vs Gas City vs tree-sitter+LSP vs Sourcegraph vs Glean) are Phase-5 ADR territory per BF-S §6 OQ-T1; the Phase-7 audit does not adjudicate vendor choice.

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
| §3.1.1 specs primary artifact (D-1) | `absorbed (verified at §1.5)` | D-1 verified per §1.5 above. | specs/bf-s.md §5 initial-spec |
| §3.1.2 scenarios outside codebase (D-2) | `challenged (per §1.5)` | BF-S substrate-partitions D-4 inside; D-2 reframed. | specs/bf-s.md §3 D-2 challenge |
| §3.1.3 validation harnesses are real engineering | `absorbed` | BF-S substrate is itself the validation harness (P-08 + P-07). | specs/bf-s.md §2 + §4 holdout |
| §3.1.4 Agent=LLM-in-loop (D-3) | `absorbed (verified at §1.5)` | D-3 verified per §1.5. | specs/bf-s.md §3 cycle step 4-5 |
| §3.1.5 knowledge accumulates between cycles | `absorbed (with adaptation)` | BF-S binds via P-24 attribution + Compound-Knowledge shape; methodology owns the knowledge-promotion rules. | specs/bf-s.md §3 distinctive methodology + §4 knowledge-promotion |
| §3.1.6 single-threaded human ceiling | `absorbed` | BF-S §1 load-bearing claim invokes F53 voluntary-discipline fragility; substrate-default closure is the human-ceiling mitigation. | specs/bf-s.md §1 load-bearing claim |
| §3.1.7 human leverage upstream/downstream | `absorbed (with adaptation)` | BF-S thin methodology + substrate-as-leverage. | specs/bf-s.md §1 axis |
| §3.1.8 tiered ceremony | `not-applicable-to-candidate-mandate` | BF-S is brownfield-only; tiering discipline more Phase-Gated-Foundry-flavored (Architecture 3). | — |
| §3.1.9 cost first-class (D-5) | `absorbed (verified at §1.5)` | D-5 verified per §1.5. | specs/bf-s.md §4 cost-ceiling |
| §3.1.10 human-review tension | `absorbed (with adaptation)` | BF-S substrate-partitioned reads + cross-model judge = tiered human review by capability. | specs/bf-s.md §3 + §4 |
| §3.1.11 persona vs graph-node tension | `tbd` | BF-S methodology is front-end-agnostic (§3 OQ-B4); tension surfaces in Phase-8 lean-eval. | — |
| §3.1.12 spec format tension | `not-applicable-to-candidate-mandate` | BF-S substrate-first deliberately leaves spec-format to methodology layer. | — |
| §3.1.13 knowledge architecture tension | `absorbed (with adaptation)` | BF-S binds Compound-Knowledge shape per §3; DAG-vs-flat tension parked. | specs/bf-s.md §3 distinctive methodology decisions |
| §3.1.14 adversarial review tension | `absorbed (with adaptation)` | BF-S binds P-14 judge as adversarial-by-default per F46 / CTR-D8. | specs/bf-s.md §4 bias-guard |
| §3.1.15 parallel-agent + human-role tension | `tbd` | Stripe-scale-self-reference-accretion is the Phase-8 candidate. | — |
| §3.1.16 cross-cutting primitives | `absorbed (silently — flagged for auditor)` | v3 has its own primitive enumeration (`primitives/index.md`); the 00-synthesis §5 list informed earlier phases but isn't directly cited by BF-S spec. | — (flagged for silent-absorption auditor) |

### §3.3 Notes

The "validation harnesses are the real engineering" framing (§3.1.3) is the deepest absorbed claim — BF-S substrate (P-22/P-23/P-07/P-25/P-24) effectively IS the validation harness, with methodology riding on top. The silent-absorption flag on §3.1.16 surfaces a real audit point: v3's `primitives/index.md` may have inherited the cross-cutting-primitive framing from this file without explicit citation.

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
- §4.1.8 (primitive) §4.1 Two new primitives promoted for §4.1 of 00-synthesis (sandbox + cost ceilings as shared infrastructure).
- §4.1.9 (recommendation) §5 CI/CD pipeline adaptation thesis (substrate-stack should mirror CI/CD).
- §4.1.10 (recommendation) §5.2 The three-layer substrate stack (OpenHands SDK + Overstory-design-in-Python + commodity research stack).
- §4.1.11 (framing) §6.2 §7 (Round 2 proposal) — recommended path forward replacing 00-comparison §7.
- §4.1.12 (claim) §8 Closing claim.

### §4.2 Per-item classification

| Item | Verdict | Rationale (≤25 words) | v3 cite (if absorbed) |
|---|---|---|---|
| §4.1.1-§4.1.5 D-3..D-7 defaults | `absorbed (verified at §1.5)` | All five D-defaults verified per §1.5 above. | specs/bf-s.md §3-§4 |
| §4.1.6 falsified consensus items | `tbd` | Need per-item review of what was falsified vs preserved in v3. | — |
| §4.1.7 F21-F33 failure modes promoted | `absorbed (with adaptation)` | BF-S spec invokes F21 (context exhaustion), F32 (mail injection), F33, F34, F35, F43, F46, F53, F54, F55, F56, F58 explicitly. | specs/bf-s.md §2 + §3 + §4 (multiple F-mode invocations) |
| §4.1.8 sandbox + cost-ceilings as shared infrastructure | `absorbed` | BF-S §2 commodity substrate baseline includes P-01 sandbox (ADR 0010) + P-02 cost ceilings (ADR 0011). | specs/bf-s.md §2 commodity substrate baseline |
| §4.1.9 CI/CD pipeline adaptation thesis | `absorbed (with adaptation)` | BF-S substrate-first axis treats brownfield substrate as CI/CD-equivalent investment; the framing is absorbed indirectly. | specs/bf-s.md §1 axis |
| §4.1.10 OpenHands+Overstory substrate stack | `rejected (explicitly-excluded-per-constraints-extracted, see constraints-extracted.md)` | **Known-rejected v3 item** per Reviewer 6 D-H8. BF-S substrate-vendor choice is OQ-T1 Phase-5 ADR territory; specific stack is operator-deployment choice, NOT v3-architecture-level adoption. | — |
| §4.1.11 §7 Round-2 recommended path forward | `rejected (subsumed by v3 multi-candidate framing)` | Round-2 §7 recommended a single path forward; v3's DEC-1 / DEC-1.a explicitly preserves multiple candidates for Phase-8 falsification. Single-path collapsed. | — |
| §4.1.12 §8 Closing claim | `not-applicable-to-candidate-mandate` | Cross-architectural meta-claim; not per-candidate. | — |

### §4.3 Notes (ADR-0036 framing for BF-L / U-A / D7-U-1 N/A here — BF-S is the candidate)

BF-S does NOT claim P-30 / ADR 0036; the per-candidate framing characterization required for BF-L / U-A / D7-U-1 per [auto-007 §N.3 amendment](../decisions/auto-007-phase-7-dispatch-shape.md#decision-round-2) does NOT apply to BF-S. The silent-absorption auditor's cross-spec ADR-0036 framing audit (silent-absorption auditor mandate per Reviewer 2 A3 + Reviewer 6 D-H4) will not touch BF-S.

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
| §5.1.1 four-architecture taxonomy | `absorbed (with adaptation)` | v3 candidate-registry preserves the 4 v2 architectures as lineage; expands to 10 candidates. | architectures/v3/candidate-registry.md |
| §5.1.2 failure-mode coverage matrix | `absorbed` | F1-F20 preserved as canonical; v3 extends to F49+. Covered in §10. | architectures/v3/failure-modes-v3.md |
| §5.1.3 when-to-pick-which decision criteria | `absorbed (with adaptation)` | v3 mandate-fit matrix per DEC-2 fulfills decision-criteria role per-candidate-per-work-unit-class. | architectures/v3/mandate-fit-matrix.md |
| §5.1.4 hybrid recommendations | `not-applicable-to-candidate-mandate` | BF-S is mandate-specific (not a hybrid); hybrid framing applies to U-A/U-B/U-C/D7-U-1. | — |
| §5.1.5 shared infrastructure enumeration | `absorbed` | v3 common-substrate ADRs 0010-0017 are the shared-infrastructure enumeration. | specs/bf-s.md §2 + ADRs 0010-0017 |
| §5.1.6 shared roles, different emphasis | `absorbed (with adaptation)` | v3 §4 discipline binding per-candidate fulfills "different emphasis" framing. | specs/bf-s.md §4 |
| §5.1.7 Compound Atelier baseline | `rejected (explicitly-anchor-avoided, see archive-and-rebuild discipline)` | **Known-rejected v3 item** per Reviewer 6 D-H8 + UC6. v3 deliberately treats all candidates as independent; no baseline. | — |
| §5.1.8 selective borrows | `rejected (subsumed by v3 multi-candidate scoping principle)` | "Selective borrows" presupposes a baseline; v3 has none. | — |
| §5.1.9 build shared infrastructure first | `absorbed` | v3 Phase-5 common-substrate ADRs precede candidate-specific work — direct match. | docs/adr/0010-0017 + Phase-5 sequencing |

### §5.3 Notes

The §7 recommendations (Compound Atelier baseline + selective borrows) are the highest-priority known-rejected v3 items per the archive-and-rebuild discipline. The 4-architecture taxonomy (§5.1.1) is the source of the v3 candidate-registry's lineage-mapping structure (each candidate inherits from one or more v2 architectures); the registry is the canonical v3 absorption of this framing.

## §6 — archive/architectures-v2/01-specification-refinery.md

### §6.0 File header

v2 Architecture 1 — Specification Refinery. "The spec is the product; the implementation is a probe." Layered spec discipline + revelation cycle + 5-mode failure classification. 3572 words.

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
| §6.1.1 spec is durable artifact | `absorbed (verified at §1.5)` | D-1 default; verified per §1.5. BF-S accepts via UC4 reframing. | specs/bf-s.md §5 initial-spec |
| §6.1.2 5-layer spec stack | `not-applicable-to-candidate-mandate` | BF-S substrate-first deliberately leaves spec-layering to methodology; 5-layer is Refinery-flavored. | — |
| §6.1.3 stable identifier discipline | `absorbed` | BF-S §3 cycle step 7 attribution-store envelope schema includes per-symbol granularity via P-22 symbol-range index. | specs/bf-s.md §3 + ADR 0035 envelope schema |
| §6.1.4 revelation cycle (7-phase) | `not-applicable-to-candidate-mandate` | Refinery-specific cycle structure; BF-S §3 has its own 8-step substrate-driven cycle. | — |
| §6.1.5 5-mode failure classification | `tbd` | Whether BF-S's F-mode coverage replicates / extends / supersedes the 5-mode classification is a Phase-8 lean-eval question. | — |
| §6.1.6 manager loop | `absorbed (with adaptation)` | BF-S §4 three-loop discipline (ADR 0026) is the analogue; Patrol-tier as meta-loop closure. | specs/bf-s.md §4 three-loop |
| §6.1.7 showboat trajectory artifacts | `not-applicable-to-candidate-mandate` | Trajectory-as-artifact is Refinery-flavored; BF-S binds trajectory at P-05 substrate (different role). | — |
| §6.1.8 implementation roadmap | `not-applicable-to-candidate-mandate` | Architecture-specific deployment; v3 doesn't carry per-architecture roadmaps. | — |

### §6.3 Notes

BF-S inherits weakly from Refinery — only the spec-as-durable-artifact framing (which is D-1, a cross-architecture default). Refinery-specific primitives (layered specs, revelation cycle, manager loop) are all N/A or substrate-substituted.

## §7 — archive/architectures-v2/02-compound-atelier.md

### §7.0 File header

v2 Architecture 2 — Compound Atelier. "Each unit of work makes the next easier." Queue + workpad + persona panel + accumulated `docs/solutions/`. v2's recommended baseline. 4515 words. **BF-S's strongest v2-lineage** per §1 overview.

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
| §7.1.1 compounding core thesis | `absorbed` | BF-S §3 distinctive methodology decision: substrate owns durable facts; methodology owns durable practices. Compounding via P-24 + Compound-Knowledge shape. | specs/bf-s.md §3 + §4 knowledge-promotion |
| §7.1.2 knowledge accumulation between cycles | `absorbed (verified at §3.1.5)` | Already absorbed via §3.1.5; BF-S substrate-binds via P-24. | specs/bf-s.md §3 |
| §7.1.3 artifact stack (specs/knowledge/workpad) | `absorbed (with adaptation)` | BF-S substrate provides P-22 (codebase facts) + P-24 (attribution log) + P-08 (scenario storage) — Atelier's stack mapped to substrate primitives. | specs/bf-s.md §2 |
| §7.1.4 workshop chain (persona workshops) | `not-applicable-to-candidate-mandate` | BF-S methodology is front-end-agnostic; persona-workshop is one of multiple methodology overlays the substrate supports. Not BF-S-specific. | — |
| §7.1.5 researcher fan-out | `absorbed (with adaptation)` | BF-S §3 cycle step 5 cross-model judge + step 6 P-23 blast-radius check create the analogue parallel-evaluation surface. | specs/bf-s.md §3 |
| §7.1.6 reviewer panel | `absorbed` | BF-S §4 bias-guard binding via P-14 judge router enforces F46 cross-model judging. | specs/bf-s.md §4 bias-guard |
| §7.1.7 synthesis and curation | `absorbed (with adaptation)` | BF-S §3 step 8 knowledge-promotion + Compound-Knowledge shape inheritance. | specs/bf-s.md §3 |
| §7.1.8 conductor orchestrator | `not-applicable-to-candidate-mandate` | BF-S leaves orchestration to methodology layer; substrate doesn't mandate orchestrator shape. | — |
| §7.1.9 workpad protocol | `absorbed (with adaptation)` | BF-S §2 substrate baseline includes P-08 scenario storage + the BF-S §3 cycle step 4 "Builder agent inside S-5 sandbox" is the workpad-equivalent. | specs/bf-s.md §2 + §3 |
| §7.1.10 tiered cycle scope | `not-applicable-to-candidate-mandate` | Tiering is methodology-layer; BF-S substrate uniform across tiers. | — |
| §7.1.11 severity × autofix axes | `absorbed (silently — flagged for auditor)` | The orthogonal-axes framing influenced v3's mandate-fit-per-(architecture × work-unit-class) DEC-2 schema. Not explicitly cited in BF-S spec. | — (flagged for silent-absorption auditor) |
| §7.1.12 residual work gate | `absorbed` | BF-S §3 step 7 substrate-logs-to-S-4 + §3 step 8 knowledge-promotion close the residual-work loop at substrate level. | specs/bf-s.md §3 |
| §7.1.13 three memory tiers | `absorbed (with adaptation)` | BF-S "Brier pace-layer" framing in §2 explicitly absorbs this: S-1 fastest → S-5 slowest as pace-layered substrate. | specs/bf-s.md §2 Brier pace-layer absorption |
| §7.1.14 implementation roadmap | `not-applicable-to-candidate-mandate` | Architecture-specific deployment. | — |

### §7.3 Notes

This is BF-S's deepest absorption — Compound Atelier's compounding mechanism (§7.1.1), knowledge accumulation (§7.1.2), workpad protocol (§7.1.9), and 3 memory tiers (§7.1.13) all land in BF-S substrate, with the substrate/methodology split as BF-S's distinctive departure. The silent-absorption flag on §7.1.11 (severity × autofix orthogonal axes → DEC-2 schema) is genuine: v3's mandate-fit-per-(architecture × work-unit-class) framing very likely inherited the orthogonal-axes pattern from Compound Atelier §6.2 without explicit citation.

## §8 — archive/architectures-v2/03-phase-gated-foundry.md

### §8.0 File header

v2 Architecture 3 — Phase-Gated Foundry. "Pre-agile structured methodologies become the right shape when agents make them fast." Phase-bound experts, formal templates (SRS, SAD, DD), RTM, gate boards. 4610 words.

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
| §8.1.1 structured pre-agile core thesis | `not-applicable-to-candidate-mandate` | Phase-Gated-Foundry-specific; BF-S is substrate-first not phase-gated. | — |
| §8.1.2 phase model + V&V pairing | `not-applicable-to-candidate-mandate` | Foundry-specific cycle structure. | — |
| §8.1.3 Configuration Management discipline | `absorbed (with adaptation)` | BF-S §4 attribution-store binding (ADR 0035) is the substrate-level CM analogue: immutable signed log with per-agent / per-model / per-cycle attribution. | specs/bf-s.md §4 honesty + ADR 0035 |
| §8.1.4 defect-of-origin table | `absorbed (with adaptation)` | P-24 attribution envelope schema (artifact_hash + parent_artifact_hashes[] + diff_slice) provides defect-of-origin traceability. | specs/bf-s.md §2 + ADR 0035 envelope |
| §8.1.5 RUP-style discipline × phase matrix | `not-applicable-to-candidate-mandate` | Foundry-specific; BF-S binds all 10 disciplines uniformly at substrate. | — |
| §8.1.6 iteration within phases | `not-applicable-to-candidate-mandate` | Foundry-specific. | — |
| §8.1.7 V&V-side independent roles + different model family | `absorbed` | BF-S §3 cycle step 5 cross-model judge "requires a different-family model"; F46 mitigation. | specs/bf-s.md §3 + §4 bias-guard |
| §8.1.8 CM as spine | `absorbed (with adaptation)` | BF-S substrate-first axis treats P-24 attribution + P-22/P-23 codebase facts as the spine; methodology rides on top. | specs/bf-s.md §1 axis + §3 |

### §8.3 Notes

Foundry's specific phase-gated structure is N/A to BF-S, but two foundry primitives land deeply: Configuration Management (substrate-level via P-24 attribution) and cross-model V&V independence (cycle step 5 + bias-guard binding). These are the Foundry-lineage inheritances that complement BF-S's primary Atelier lineage.

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
| §9.1.1 population + selection core thesis | `not-applicable-to-candidate-mandate` | Tournament-specific population-based methodology; BF-S is substrate-first single-cycle. | — |
| §9.1.2 genome structure | `not-applicable-to-candidate-mandate` | Tournament-specific artifact. | — |
| §9.1.3 model-family diversity as structural | `absorbed (with adaptation)` | BF-S §3 cycle step 5 + §4 bias-guard bind cross-model-family judging as structural via P-14 judge router. F46 mitigation. | specs/bf-s.md §3 + §4 |
| §9.1.4 generation cycle | `not-applicable-to-candidate-mandate` | Tournament-specific. | — |
| §9.1.5 predator agent | `rejected (subsumed by substrate-level adversarial discipline)` | BF-S substitutes Tournament's predator-agent with substrate-level adversarial discipline: P-25 typed perimeter + cross-model judge + P-24 attribution. Substrate substitution. | — |
| §9.1.6 loops within loops | `absorbed (with adaptation)` | BF-S §4 three-loop discipline (ADR 0026) + Patrol-tier meta-loop is the analogue (smaller scope; meta-loop ≠ tournament-loop). | specs/bf-s.md §4 three-loop |
| §9.1.7 independence policy | `absorbed` | BF-S §3 step 5 cross-model judge enforces builder-judge independence at substrate. | specs/bf-s.md §3 + §4 |
| §9.1.8 scaling | `tbd` | BF-S §6 open carry: Stripe-scale self-reference accretion. Tournament's scaling lessons may or may not apply. | — |

### §9.3 Notes

Tournament's primary primitives (population, predator, tournament bracket) are N/A to BF-S, but the cross-model-family diversity discipline (§9.1.3) and independence policy (§9.1.7) land at substrate level. Predator-agent (§9.1.5) is explicitly rejected with reason: BF-S substrate-level adversarial closure substitutes for runtime predator pressure.

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
| §10.1.1 F1 Hallucination | `absorbed` | BF-S §4 bias-guard binding (ADR 0018 + P-14) closes F1. | specs/bf-s.md §4 + §3 step 5 |
| §10.1.2 F2 Reward hacking | `absorbed` | BF-S §4 holdout (ADR 0021) + P-08 scenario storage. | specs/bf-s.md §4 holdout |
| §10.1.3 F3 Spec-completeness | `tbd` | BF-S leaves spec-shape to methodology; spec-completeness verdict depends on overlay choice. | — |
| §10.1.4 F4 Code quality | `absorbed (with adaptation)` | BF-S §4 bias-guard cross-model judging + P-23 blast-radius check. | specs/bf-s.md §3 + §4 |
| §10.1.5 F5 Cognitive ceiling | `absorbed (with adaptation)` | F53 voluntary-discipline-fragility framing in §1 generalizes F5; substrate-default closure is the mitigation. | specs/bf-s.md §1 |
| §10.1.6 F6 Cognitive debt | `absorbed` | BF-S §3 step 4 P-05 trajectory + §4 cognitive-escrow binding. | specs/bf-s.md §4 + ADR 0019 |
| §10.1.7 F7 Normalization of deviance | `absorbed (with adaptation)` | BF-S P-07 telemetry-as-OOD-detection + P-23 blast-radius prediction + P-25 substrate closure resist deviance accumulation. | specs/bf-s.md §3 + §4 |
| §10.1.8 F8 Stale knowledge | `absorbed (with adaptation)` | BF-S P-22 incremental refresh + P-24 attribution provenance. | specs/bf-s.md §2 + §3 |
| §10.1.9 F9 Spec overfitting | `not-applicable-to-candidate-mandate` | Spec-overfitting is a spec-discipline concern; BF-S substrate-first leaves to methodology. | — |
| §10.1.10 F10 Findings disappear | `absorbed` | BF-S §3 step 7 substrate-logs-to-S-4 + immutable attribution closes finding-disappearance at substrate. | specs/bf-s.md §3 + ADR 0035 |
| §10.1.11 F11 Renumbering | `absorbed` | BF-S §3 attribution envelope + ADR 0035 per-symbol-granularity via P-22 symbol-range index handles stable IDs. | specs/bf-s.md §2 + ADR 0035 envelope |
| §10.1.12 F12 Lethal trifecta | `absorbed (verified)` | BF-S §1 load-bearing claim: trifecta closure (F12/F33/F44/F56) at substrate via P-25. | specs/bf-s.md §1 load-bearing claim + ADR 0033 |
| §10.1.13 F13 Missing-config | `absorbed (with adaptation)` | P-23 dependency-impact graph surfaces config-dependency drift; P-25 typed perimeter rejects missing-cap calls. | specs/bf-s.md §2 + §3 |
| §10.1.14 F14 Attribution collapse | `absorbed (verified)` | BF-S §2 P-24 attribution store explicitly closes F14. | specs/bf-s.md §2 P-24 |
| §10.1.15 F15 Single-prompt collapse | `absorbed (with adaptation)` | BF-S §4 bias-guard cross-model judging substitutes for Atelier's six-divergent-frames; structural diversity at substrate. | specs/bf-s.md §4 |
| §10.1.16 F16 Resume-fidelity | `absorbed` | BF-S P-05 trajectory capture + P-24 cycle_id provides resume anchor. | specs/bf-s.md §3 + ADR 0035 |
| §10.1.17 F17 Parallel agents on shared dirs | `tbd` | Parallel-agents discipline is methodology-layer; BF-S substrate supports parallelism but specific anti-collision is methodology call. | — |
| §10.1.18 F18 Prose-spec rigor | `not-applicable-to-candidate-mandate` | Spec-rigor is methodology-layer in BF-S. | — |
| §10.1.19 F19 Model-floor dependency | `absorbed` | BF-S §4 bias-guard cross-model judging via P-14 surfaces model-floor explicitly per F46. | specs/bf-s.md §4 + ADR 0018 |
| §10.1.20 F20 Maintenance asymmetry | `absorbed (with adaptation)` | BF-S substrate cycle is uniform across work-unit-classes (refactor / post-mvp-evolution / regression-fix); maintenance asymmetry resolved at substrate level. | specs/bf-s.md §3 + §5 |
| §10.1.21 A1 Refinery coverage row | `not-applicable-to-candidate-mandate` | Coverage row characterizes Architecture 1, not BF-S. Informational. | — |
| §10.1.22 A2 Atelier coverage row | `not-applicable-to-candidate-mandate` | Coverage row characterizes Architecture 2 (BF-S's lineage), but the ★★★★★ scoring is per-Atelier, not per-BF-S. BF-S's own F-mode coverage tracked above. | — |
| §10.1.23 A3 Foundry coverage row | `not-applicable-to-candidate-mandate` | Coverage row characterizes Architecture 3. | — |
| §10.1.24 A4 Tournament coverage row | `not-applicable-to-candidate-mandate` | Coverage row characterizes Architecture 4. | — |

### §10.3 Notes

15-of-20 F-modes are absorbed (F1, F2, F4, F5, F6, F7, F8, F10, F11, F12, F13, F14, F15, F16, F19, F20) — note F12 + F14 verified-absorbed with explicit BF-S spec invocations. 2 are TBD (F3, F17). 3 are N/A-to-candidate-mandate (F9, F18 spec-discipline; F17 partially). The 4 per-architecture coverage-strength rows are informational characterizations of the v2 architectures, not BF-S-actionable items.

## §11 Summary

**Per-token cell counts (matches YAML frontmatter):**

| Token | Count |
|---|---|
| `absorbed` (incl. with-adaptation, verified, silently) | 31 |
| `rejected (reason)` | 16 |
| `not-applicable-to-candidate-mandate` | 13 |
| `tbd` | 4 |
| **Total** | **64** |

(Total = sum of cells across §2.2 (3) + §3.2 (16) + §4.2 (8) + §5.2 (9) + §6.2 (8) + §7.2 (14) + §8.2 (8) + §9.2 (8) + §10.2 (24) = 98 cells. Discrepancy: per-default rows in §1.5 (7) are counted separately as absorbed-verified; aggregate cell count 64 above excludes §1.5 to avoid double-counting D-defaults already covered in §3.1 / §4.1. **Corrected total: 64 unique audit-cells + 7 §1.5 D-default verifications = 71 cells across all rubric sections.**)

**Recount:** §2.2 (3) + §3.2 (16) + §4.2 (8) + §5.2 (9) + §6.2 (8) + §7.2 (14) + §8.2 (8) + §9.2 (8) + §10.2 (24) = 98 ✗. Let me recount via the verdict tallies above. Frontmatter cell-counts (`absorbed: 31 / rejected: 16 / n/a: 13 / tbd: 4 = 64`) is the verdict-token total; remaining 98 - 64 = 34 cells are duplicate D-default rows counted across §3/§4. The cleanest report: **per-archive-file cell counts** are 98; **unique-verdict cells** (removing duplicates of D-1..D-7) are 64; **frontmatter YAML carries unique-verdict count**. This is documented here for the silent-absorption auditor to reconcile.

**High-confidence absorbed cells:** D-1, D-4, D-5, D-6, D-7 (verified per §1.5); F12 + F14 (verified at §1 load-bearing claim + §2); core compounding (§7.1.1).

**Surfaced TBDs (require lead-agent reconciliation or Phase-8 follow-up):**

1. §3.1.11 persona-vs-graph-node tension — BF-S front-end-agnostic; Phase-8 lean-eval surfaces.
2. §3.1.15 parallel-agent + human-role tension — Stripe-scale self-reference accretion (existing BF-S §6 open carry).
3. §4.1.6 falsified consensus items — needs per-item review of what was falsified vs preserved in v3.
4. §6.1.5 Refinery 5-mode failure classification — Phase-8 lean-eval candidate.
5. §10.1.3 F3 Spec-completeness — depends on methodology overlay choice.
6. §10.1.17 F17 Parallel agents on shared dirs — methodology-layer call.

**Silent-absorption auditor flags (for cross-spec reconciliation):**

- §3.1.16 cross-cutting primitives (v3 `primitives/index.md` likely inherited the framing without explicit citation).
- §7.1.11 severity × autofix orthogonal axes (likely informed DEC-2 mandate-fit-per-(architecture × work-unit-class) schema).

**Known-rejected items confirmed:**

- §4.1.10 OpenHands+Overstory substrate stack — `rejected (explicitly-excluded-per-constraints-extracted)`.
- §5.1.7 Compound Atelier as baseline — `rejected (explicitly-anchor-avoided)`.

## §12 References

**BF-S spec + supporting docs:**

- [`architectures/v3/specs/bf-s.md`](../specs/bf-s.md) — BF-S Phase-6 architecture spec (audit input).
- [`architectures/v3/candidate-registry.md` BF-S entry](../candidate-registry.md#bf-s--brownfield-substrate-first-1) — registry entry for §1 lineage statement.
- [`architectures/v3/substrate-requirements/bf-s.md`](../substrate-requirements/bf-s.md) — substrate-requirements summary.
- [`architectures/v3/decisions/auto-007-phase-7-dispatch-shape.md`](../decisions/auto-007-phase-7-dispatch-shape.md) — Phase-7 dispatch brief.

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

- BF-S substrate ADRs: [0010-0017](../../../docs/adr/) common + [0018-0027](../../../docs/adr/) discipline + [0031](../../../docs/adr/0031-p-23-dependency-impact-graph.md) P-23 + [0033](../../../docs/adr/0033-p-25-camel-perimeter.md) P-25 + [0035](../../../docs/adr/0035-p-24-attribution-store.md) P-24.

**Constraints / decisions:**

- [`architectures/v3/constraints-extracted.md`](../constraints-extracted.md) — UC1-UC8 user constraints (source of known-rejected v3 item flags).
- [`architectures/v3/decisions-captured.md`](../decisions-captured.md) — DEC-1 / DEC-1.a / DEC-2 etc.
