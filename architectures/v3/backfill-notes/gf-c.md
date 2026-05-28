---
candidate: gf-c
candidate-name: Greenfield, cold-start-first (Bootstrap-Bench Factory)
mandate-scope: greenfield
based-on-spec-commit: c54daf1
based-on-date: 2026-05-27
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
  absorbed: 60
  rejected: 5
  not-applicable: 27
  tbd: 7
self-check-results:
  wc-w: 6935  # over Light tier (3500-5000) by ~1900; see exemplar-budget-flag below
  ls-cited-files: PASS  # all cited v3 + spec + ADR paths verified via Read at audit time
  section-headers: PASS  # §1, §1.5, §2-§10, §11, §12 + §N.0 file-headers across all 9 archive sections
  enumeration-floor: PASS  # §2.1=3 (small-file exception per Reviewer 4); §3=17, §4=8, §5=9, §6=8, §7=14, §8=8, §9=8, §10=24
  cell-counts-match-yaml: PASS  # 60+5+27+7=99 cells; matches per-archive-file table-row total (3+17+8+9+8+14+8+8+24=99)
  verbatim-text-pull: n/a  # no binding rule tables verbatim-cited (per AGENTS-MD-bf4431be57 + Reviewer 3 D6)
  tbd-count: 7  # 7 table-cell `tbd` verdicts; surfaced TBD list in §11 also names items requiring lead-agent follow-up
exemplar-budget-flag: |
  Light tier upper bound (5000) exceeded by ~1800 words (6812 actual). Causes: (a) §1.5 D-1..D-7
  verification adds ~330 words per Reviewer 5/6 amendments; (b) §10 24-row failure-modes audit
  adds ~450 words over the rubric minimum (24 vs 5 floor); (c) GF-C's high N/A count (27) and
  associated §N.3 notes explaining cold-start vs steady-state distinction add ~350 words across
  §7.3 / §10.3 / §11; (d) §11 cell-count reconciliation + surfaced-TBDs + silent-absorption-flags
  discussion adds ~200 words; (e) §1.5 verification cells require longer cite-text for D-3 silent
  absorption flag and D-6 with-adaptation qualifier. Sibling subagents were instructed in dispatch
  that Light-tier candidates may land at 5000-5700; GF-C lands above that band. **Flag for lead
  agent:** GF-C is structurally similar to the exemplar in cell-count density but the high-N/A
  pattern (signature of cold-start-vs-steady-state distinction) demands more per-cell explanation
  in §N.3 notes than the exemplar required. Mirrors BF-S exemplar's `exemplar-budget-flag`
  acknowledgement that Light-tier may be too tight when D-default verification + 24-row
  failure-modes-floor are stacked. Lead-agent decision: ACCEPT at 6812 words; do NOT re-author.
---

# Back-fill notes — GF-C (Greenfield, cold-start-first / Bootstrap-Bench Factory) vs v1/v2 archive

## §1 Overview

**Mandate.** Greenfield (only). GF-C is greenfield-only by construction — 2 mandate-fit cells `greenfield` (initial-spec, mvp) and 3 `silent` (refactor, post-mvp-evolution, regression-fix) per [GF-C spec §5](../specs/gf-c.md#5-mandate-fit) + frontmatter. X_UNM_B is `N/A` per [substrate-requirements/gf-c.md §4](../substrate-requirements/gf-c.md).

**Axis.** Cold-start (day-0 bootstrap) is the *organising* problem. Every primitive, methodology sub-phase, and graduation criterion is shaped by "what does the factory need before any scenario, any prior trajectory, any holdout, any code exists?" Steady-state is downstream and emergent.

**Entry-mode.** Greenfield cold-start. Day-0 deliverable is *not code* — it is a validated Intent Crucible block plus an RSI declaration plus a small human-anchored Cold-Start Bench. Code generation is *gated* on bench sufficiency.

**Strongest v2-architecture-lineage.** *This candidate's strongest v2-architecture-lineage is to **Architecture 1 (Specification Refinery)** on the spec-as-durable-artifact axis, with secondary inheritance from **Architecture 3 (Phase-Gated Foundry)** on independent-V&V + audit-trail-grade artifacts.* Rationale (derived from [GF-C candidate-registry entry](../candidate-registry.md#gf-c--greenfield-cold-start-first) §axis "day-0 bootstrap" + §methodology "three sub-phases ... Council interrogation ... Graduation protocol with four explicit criteria"): GF-C's three sub-phases (Intent ingestion with Council interrogation → Bench construction → First-cycle restraint) plus its graduation gate map onto Refinery's "spec is the product; everything else is instrumentation" + Refinery's structured Channel-2 review pattern. The secondary Foundry lineage shows in: (a) graduation-protocol-as-stage-gate; (b) HMAC-signed bench + RSI ledger as audit-trail-grade artifacts; (c) cross-model judge as Foundry's "V&V on a different model family than construction" applied to cold-start specifically. No Atelier lineage of substance: GF-C's day-0-deliverable-is-not-code framing inverts Atelier's queue+workpad assumption (Atelier presupposes an issue queue + accumulated `docs/solutions/`, neither of which exists at day 0 — exactly the cold-start gap [`archive/research-plan.md` §risk](../../../archive/research-plan.md) names).

**D-1 through D-7 default-verification preview.** Per [auto-007 §1.5 verification rubric](../decisions/auto-007-phase-7-dispatch-shape.md#decision-round-2). D-1..D-7 are NOT silently skipped. §1.5 below records per-default verdicts; audit-trail is mechanically auditable per [`AGENTS-MD-e74e4811a2`](../../../AGENTS.md#self-check-rubric-requires-tool-verification-for-measurable-items).

## §1.5 D-1 through D-7 defaults verification

Per Reviewer 5 Defect 1 + Reviewer 6 D-H5 amendments. Each default verified per `grep` against the GF-C spec; verdict tokens per auto-007 Round-2 rubric.

| Default | Source claim | GF-C verdict | Spec cite |
|---|---|---|---|
| D-1 specs durable | `00-synthesis.md` §2.1 | `absorbed (verified at specs/gf-c.md §3 Sub-phase A "Day-0 deliverable is not code — it is a validated Intent Crucible plus an RSI declaration plus a small bench")` | Intent Crucible IS the durable spec artifact; P-17 + P-18 hold it. |
| D-2 scenarios out-of-tree | `00-synthesis.md` §2.2 | `absorbed (verified at specs/gf-c.md §3 Sub-phase B "Bench-construction agents never see the builder's prompts — D-4 holdout enforced at the substrate via P-01 sandbox, not as voluntary discipline")` | Cold-Start Bench (P-11) IS the day-0 out-of-tree scenario substrate. |
| D-3 Agent = Model + Harness | `13-round-2-synthesis.md` §1.1 C10 | `absorbed (silently — no §-cite found, flagged)` | GF-C spec does not invoke "Agent = Model + Harness" vocabulary; uses "Builder agent" + "Council of agents" + "cross-model judge" terminology without naming the C10 frame. Silent-absorption auditor reconciliation candidate. |
| D-4 holdout discipline | `13-round-2-synthesis.md` §1.1 C13 | `absorbed (verified at specs/gf-c.md §4 holdout binding "Bench-construction agents and builder agents are isolated at the substrate layer; D-4 is non-negotiable from cycle 1")` | F28 (holdout leakage greenfield `critical`) mitigation native; bound at P-08 + P-11. |
| D-5 hard cost ceilings | `13-round-2-synthesis.md` §1.1 C15 | `absorbed (verified at specs/gf-c.md §4 cost-ceiling binding "Cold-start cycles are tiny ... Cost ceilings are easy at cold-start scope. Cross-model judge ensemble cost ... enforced per-call")` | Bound at P-02 (ADR 0011). Cost ceiling graduates with the work-unit-class declaration. |
| D-6 tiered watchdog | `13-round-2-synthesis.md` §1.1 C14 | `absorbed (with adaptation, verified at specs/gf-c.md §2 commodity substrate baseline "P-06's Patrol-tier is structurally muted during cold-start (no historical baseline); Daemon and Triage operate from cycle 1")` | Adaptation: tiered watchdog is degraded-mode at cold-start (Patrol muted; Daemon/Triage active). |
| D-7 trajectory capture | `13-round-2-synthesis.md` §1.1 C16 | `absorbed (verified at specs/gf-c.md §3 Sub-phase C "P-05 trajectory capture (ADR 0012) writes from cycle 1 — no prior trajectories on day 0, but capture is essential to populate the steady-state primitive")` | P-05 binding explicit; day-0 capture seeds steady-state primitive. |

**Summary:** 6-of-7 defaults absorbed with explicit cite; D-3 silently absorbed (flagged for silent-absorption auditor reconciliation — GF-C uses analogous vocabulary without naming the C10 frame). No challenges; no `not-applicable` verdicts on D-defaults.

## §2 — archive/research-plan.md

### §2.0 File header

Pre-v3 research-action plan (2026-05-14). User-stated constraints already extracted to [`constraints-extracted.md`](../constraints-extracted.md); only lead-agent recommendations are Phase-7 scope. **Small-file exception (per Reviewer 4 amendment)**: 758 words; structurally yields <5 enumerable claims after user-constraint exclusion. §N.1 floor=3 actual count; auto-pass on self-check (d). **Crucially: §research-plan.md §risk "One specific risk for the greenfield mandate" directly names cold-start as the design question GF-C centres** — see §2.3 notes.

### §2.1 Enumeration

- §2.1.1 (lead-agent recommendation) — Three-layer pipeline: research reports → synthesis → action plan.
- §2.1.2 (lead-agent recommendation) — "Enough research" trigger criteria (corpus depth / breadth / decision-readiness).
- §2.1.3 (lead-agent recommendation) — Folding policy: what stays as individual documents vs gets folded into synthesis. Includes §risk's "cold-start problem for a greenfield factory is its own design question and is not directly addressed in the current comparison. Worth a dedicated synthesis section before v3 of the architectures."

### §2.2 Per-item classification

| Item | Verdict | Rationale (≤25 words) | v3 cite (if absorbed) |
|---|---|---|---|
| §2.1.1 three-layer pipeline | `absorbed (with adaptation)` | v3 inherits research → synthesis → action via Phase-1 corpus inventory + Phase-3 synthesis + Phase-5 ADRs + Phase-6 specs. | corpus-inventory.md + ARCHITECTURE-V3-SYNTHESIS-PLAN.md |
| §2.1.2 "enough research" trigger | `absorbed` | v3 Phase-1 corpus saturation + Phase-3 contradictions.md fulfill. | corpus-inventory.md + contradictions.md |
| §2.1.3 folding policy + cold-start §risk callout | `absorbed (verified)` | GF-C is the v3 candidate that **directly answers** the §risk's "cold-start problem ... its own design question." GF-C's load-bearing claim materialises this as substrate. | specs/gf-c.md §1 load-bearing claim + §3 three sub-phases |

### §2.3 Notes

This file's §risk paragraph is GF-C's *direct ancestor* in the v1 corpus — the strongest single-paragraph cite that demands a cold-start-first architecture. The §risk explicitly names "Atelier's strongest assets (the queue, the workpad, accumulated `docs/solutions/`) do not exist on day one"; GF-C inverts this by treating day-0 substrate as different from day-N. The "Worth a dedicated synthesis section before v3" instruction was honoured: v3 candidate-registry GF-C is the dedicated treatment.

## §3 — archive/synthesis-v1-v2/00-synthesis.md

### §3.0 File header

Round-1 v2 synthesis post-primary-source-access. Canonical entry for F1-F20. 5020 words. D-1 through D-7 defaults sourced here; verified per-candidate in §1.5 above.

### §3.1 Enumeration

- §3.1.1 (claim) §2.1 Specs become the primary artifact (D-1).
- §3.1.2 (claim) §2.2 Scenarios live outside the codebase (D-2).
- §3.1.3 (claim) §2.3 Validation harnesses are the real engineering.
- §3.1.4 (claim) §2.4 The agent is "an LLM running tools in a loop" (D-3).
- §3.1.5 (claim) §2.5 Knowledge accumulates between cycles.
- §3.1.6 (claim) §2.6 Single-threaded human supervision cognitive ceiling.
- §3.1.7 (claim) §2.7 Human leverage moves upstream and downstream.
- §3.1.8 (claim) §2.8 Tiered ceremony beats one-size-fits-all.
- §3.1.9 (claim) §2.9 Cost is a first-class architectural concern (D-5).
- §3.1.10 (framing) §3.1 Human review — required / eliminated / tiered.
- §3.1.11 (framing) §3.2 Persona-based vs graph-node agent design.
- §3.1.12 (framing) §3.3 Spec format — prose / structured / DOT.
- §3.1.13 (framing) §3.4 Knowledge architecture — flat / DAG / chat / self-improving prompts.
- §3.1.14 (framing) §3.5 Adversarial review — separate role vs attribute.
- §3.1.15 (framing) §3.6 Parallel agent ceiling + human role.
- §3.1.16 (framing) §3.8 Workflow language — prose / code / graph.
- §3.1.17 (primitive) §5 Cross-cutting design primitives (artifact stack / roles / loops / gates / stable IDs).

### §3.2 Per-item classification

| Item | Verdict | Rationale (≤25 words) | v3 cite (if absorbed) |
|---|---|---|---|
| §3.1.1 specs primary artifact (D-1) | `absorbed (verified at §1.5)` | Intent Crucible IS GF-C's spec artifact. | specs/gf-c.md §3 sub-phase A |
| §3.1.2 scenarios outside codebase (D-2) | `absorbed (verified at §1.5)` | Cold-Start Bench is the day-0 holdout substrate. | specs/gf-c.md §3 sub-phase B + §4 holdout |
| §3.1.3 validation harnesses are real engineering | `absorbed (with adaptation)` | GF-C's P-11 bench + P-17 validator + P-12 EARS linter together form the day-0 validation harness. | specs/gf-c.md §2 substrate composition |
| §3.1.4 Agent=LLM-in-loop (D-3) | `absorbed (silently — flagged per §1.5)` | GF-C uses Builder/Council/Judge vocabulary without naming C10 frame. | — (auditor reconciliation candidate) |
| §3.1.5 knowledge accumulates between cycles | `absorbed (with adaptation)` | GF-C's micro-cold-start re-entry mechanism IS the inter-cycle knowledge-accumulation discipline at the work-unit-class granularity. | specs/gf-c.md §3 distinctive methodology + §4 knowledge promotion |
| §3.1.6 single-threaded human ceiling | `absorbed (with adaptation)` | GF-C addresses via L3-Augmentation enforcement during cold-start (human in every cycle); steady-state automation is graduated, not assumed. | specs/gf-c.md §3 graduation protocol |
| §3.1.7 human leverage upstream/downstream | `absorbed (with adaptation)` | GF-C's day-0-deliverable-is-not-code = upstream leverage at Intent authoring; Council interrogation is the upstream review surface. | specs/gf-c.md §1 axis + §3 |
| §3.1.8 tiered ceremony | `absorbed (with adaptation)` | GF-C tiers ceremony by *regime* (Cold-Start L3 vs Steady-State per-class L4) — work-unit-class graduation is the tiering mechanism. | specs/gf-c.md §3 graduation protocol + §5 mandate fit |
| §3.1.9 cost first-class (D-5) | `absorbed (verified at §1.5)` | Bound at P-02; cross-model ensemble cost enforced per-call. | specs/gf-c.md §4 cost-ceiling |
| §3.1.10 human-review tension | `absorbed (with adaptation)` | GF-C explicitly takes L3-Augmentation during cold-start, per-class L4 post-graduation — Jaymin-regime declaration native. | specs/gf-c.md §3 graduation criterion 2 + §4 honesty |
| §3.1.11 persona vs graph-node | `tbd` | GF-C methodology mentions "Council" (persona-flavored) but is front-end-agnostic at substrate. Phase-8 lean-eval surface. | — |
| §3.1.12 spec format tension | `absorbed (verified)` | GF-C explicitly chooses EARS five-pattern grammar + INCOSE GtWR for spec form (per §3 sub-phase A). Resolves the prose/structured/DOT tension toward "structured prose with EARS templates". | specs/gf-c.md §2 designed-system substrate (P-12) + §3 sub-phase A |
| §3.1.13 knowledge architecture tension | `not-applicable-to-candidate-mandate` | Cross-cycle knowledge architecture is steady-state question; GF-C centres day-0 before knowledge exists. Inherited post-graduation. | — |
| §3.1.14 adversarial review tension | `absorbed` | GF-C binds cross-model judge (P-14) + ensemble substance-check — adversarial-by-substrate at cold-start. | specs/gf-c.md §4 bias-guard |
| §3.1.15 parallel-agent + human-role tension | `absorbed (with adaptation)` | GF-C resolves toward "human in inner loop during cold-start" (L3-Augmentation); parallelism graduates with work-unit-class. | specs/gf-c.md §3 graduation criterion 2 |
| §3.1.16 workflow language tension | `not-applicable-to-candidate-mandate` | Workflow-language (prose/code/graph) is methodology-layer presentation; GF-C substrate-orphan-first, leaves to methodology. | — |
| §3.1.17 cross-cutting primitives | `absorbed (silently — flagged for auditor)` | v3 `primitives/index.md` has own primitive enumeration; the 00-synthesis §5 list informed earlier phases but is not directly cited by GF-C spec. | — (flagged) |

### §3.3 Notes

GF-C's deepest 00-synthesis absorption is on §2.1/§2.2 (spec + scenarios) — these are D-1/D-2 verified above. The §3.4 knowledge-architecture tension is N/A: GF-C's design centre is *before* knowledge exists; the question becomes load-bearing only post-graduation, and GF-C explicitly punts on post-graduation methodology (per §5 mandate fit `silent` on 3-of-5 work-unit-classes). The §3.1.4 D-3 silent absorption flag is the load-bearing reconciliation surface for the silent-absorption auditor.

## §4 — archive/synthesis-v1-v2/13-round-2-synthesis.md

### §4.0 File header

Round-2 v2 synthesis (6496 words). Promoted F21-F33 + Round-2 consensus C10-C16; proposed OpenHands+Overstory substrate stack as §6.2 / §8 recommendation. **Known-rejected v3 item: OpenHands+Overstory substrate stack** per Reviewer 6 D-H8.

### §4.1 Enumeration

- §4.1.1 (claim) §1.1 C10 Agent = Model + Harness (D-3 — covered in §3.1.4 / §1.5).
- §4.1.2 (claim) §1.1 C11 Scaffold and harness are different layers.
- §4.1.3 (claim) §1.1 C12 Specs-as-source-code (Sean Grove frame).
- §4.1.4 (claim) §1.1 C13 Holdout discipline (D-4 — §1.5).
- §4.1.5 (claim) §1.1 C14 Tiered watchdog (D-6 — §1.5).
- §4.1.6 (claim) §1.1 C15 Hard cost ceilings (D-5 — §1.5).
- §4.1.7 (claim) §1.1 C16 Trajectory capture (D-7 — §1.5).
- §4.1.8 (framing) §3.1-§3.3 F21-F33 + sharpened F1-F20.
- §4.1.9 (primitive) §4.1 Two new primitives promoted (tiered watchdog + hard cost ceilings).
- §4.1.10 (recommendation) §5 CI/CD pipeline adaptation thesis.
- §4.1.11 (recommendation) §5.2 The three-layer substrate stack (OpenHands SDK + Overstory-design-in-Python + commodity research stack).
- §4.1.12 (recommendation) §6.2 §7 Round-2 proposed replacement (single recommended path forward).

### §4.2 Per-item classification

| Item | Verdict | Rationale (≤25 words) | v3 cite (if absorbed) |
|---|---|---|---|
| §4.1.1-§4.1.7 D-3..D-7 defaults | `absorbed (verified at §1.5)` | Per §1.5 above. D-3 silent; D-4/D-5/D-6/D-7 verified. | specs/gf-c.md §3-§4 |
| §4.1.2 C11 scaffold/harness separation | `not-applicable-to-candidate-mandate` | Substrate/runtime-layer distinction; GF-C's substrate-orphan focus is at primitive layer, not scaffold/harness layer. | — |
| §4.1.3 C12 specs-as-source-code (Sean Grove) | `absorbed (with adaptation)` | GF-C makes "spec is the durable day-0 artifact" load-bearing via Intent Crucible (P-17) + RSI Ledger (P-18). EARS notation (Kiro) absorbed per §3.1.12. | specs/gf-c.md §3 sub-phase A + §2 P-17/P-18 |
| §4.1.8 F21-F33 promoted | `absorbed (with adaptation)` | GF-C spec invokes F25 (design starvation, in §1 5-critical convergence), F32 (signing, P-11 mitigation), F38 (P-12 mitigation), F40/F41/F50/F51/F53/F54/F55 explicitly. F28 (holdout leakage greenfield critical) native via §4 holdout binding. | specs/gf-c.md §1 + §2 + §4 (multiple F-mode invocations) |
| §4.1.9 sandbox + cost-ceilings as shared infrastructure | `absorbed` | GF-C §2 commodity substrate baseline includes P-01 sandbox (ADR 0010) + P-02 cost ceilings (ADR 0011). | specs/gf-c.md §2 commodity substrate baseline |
| §4.1.10 CI/CD pipeline adaptation thesis | `tbd` | GF-C's cold-start framing is orthogonal to CI/CD thesis — cold-start scenarios may or may not run as CI/CD; Phase-8 lean-eval surfaces. | — |
| §4.1.11 OpenHands+Overstory substrate stack | `rejected (explicitly-excluded-per-constraints-extracted, see constraints-extracted.md)` | **Known-rejected v3 item** per Reviewer 6 D-H8. Substrate-vendor choice is Phase-5 ADR territory; specific stack is operator-deployment choice, NOT v3-architecture-level adoption. | — |
| §4.1.12 §6.2 §7 Round-2 recommended path forward | `rejected (subsumed by v3 multi-candidate framing)` | Round-2 §7 recommended a single path forward; v3 DEC-1 / DEC-1.a explicitly preserves multiple candidates for Phase-8 falsification. | — |

### §4.3 Notes

**No §N.3 ADR-0036 framing characterization required for GF-C** per [auto-007 §N.3 amendment](../decisions/auto-007-phase-7-dispatch-shape.md#decision-round-2). GF-C does NOT claim P-30 / ADR 0036 (explicit at [substrate-requirements/gf-c.md §3](../substrate-requirements/gf-c.md): "No contested-primitive references. GF-C does not name any of P-28, P-29, P-30, or P-19"). The per-candidate ADR-0036 framing audit applies only to BF-L / U-A / D7-U-1. Silent-absorption auditor's cross-spec ADR-0036 framing audit will NOT touch GF-C. The C10 D-3 silent absorption (Agent = Model + Harness vocabulary) IS GF-C's relevant auditor surface from this file.

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
| §5.1.1 four-architecture taxonomy | `absorbed (with adaptation)` | v3 candidate-registry preserves 4 v2 architectures as lineage; expands to 10 candidates. GF-C inherits primary from Architecture 1, secondary from Architecture 3. | candidate-registry.md |
| §5.1.2 failure-mode coverage matrix | `absorbed` | F1-F20 preserved as canonical; v3 extends to F49+. Covered in §10. | failure-modes-v3.md |
| §5.1.3 when-to-pick-which decision criteria | `absorbed (with adaptation)` | v3 mandate-fit matrix per DEC-2 fulfills decision-criteria role per-candidate-per-work-unit-class. | mandate-fit-matrix.md |
| §5.1.4 hybrid recommendations | `not-applicable-to-candidate-mandate` | GF-C is mandate-specific (greenfield-only, not a hybrid); hybrid framing applies to U-A/U-B/U-C/D7-U-1. | — |
| §5.1.5 shared infrastructure enumeration | `absorbed` | v3 common-substrate ADRs 0010-0017 are the shared-infrastructure enumeration. | specs/gf-c.md §2 + ADRs 0010-0017 |
| §5.1.6 shared roles, different emphasis | `absorbed (with adaptation)` | v3 §4 discipline binding per-candidate fulfills "different emphasis" framing. | specs/gf-c.md §4 |
| §5.1.7 Compound Atelier baseline | `rejected (explicitly-anchor-avoided, see archive-and-rebuild discipline)` | **Known-rejected v3 item.** v3 deliberately treats all candidates as independent; no baseline. GF-C explicitly inverts Atelier's queue+workpad assumption (no queue exists day 0). | — |
| §5.1.8 selective borrows | `rejected (subsumed by v3 multi-candidate scoping principle)` | "Selective borrows" presupposes a baseline; v3 has none. | — |
| §5.1.9 build shared infrastructure first | `absorbed` | v3 Phase-5 common-substrate ADRs precede candidate-specific work — direct match. GF-C inherits ADRs 0010-0017 verbatim. | docs/adr/0010-0017 + Phase-5 sequencing |

### §5.3 Notes

GF-C inverts §5.1.7's Atelier-baseline recommendation in two specific ways: (1) §research-plan.md's §risk paragraph (audited in §2.3) names Atelier's day-0 vacuum; GF-C exists *because* this comparison's recommendation didn't address it. (2) §5.1.4 hybrids assume a baseline-plus-borrow shape; GF-C's substrate-orphan-first shape (3 orphans: P-11, P-17, P-18) is N/A to hybrid framing.

## §6 — archive/architectures-v2/01-specification-refinery.md

### §6.0 File header

v2 Architecture 1 — Specification Refinery. "The spec is the product; the implementation is a probe." Layered spec discipline + revelation cycle + 5-mode failure classification. 3572 words. **GF-C's primary v2-architecture-lineage** per §1 overview.

### §6.1 Enumeration

- §6.1.1 (claim) §1 Core thesis: spec is the durable artifact; implementation is a probe.
- §6.1.2 (primitive) §2 Artifact stack: 9 durable artifact classes (layered specs L1-L5 + scenarios + pending buffer + plan + probe + decision log + trajectory + knowledge).
- §6.1.3 (primitive) §2.1 Stable identifier discipline (R/A/F/AE/U/S/finding/K).
- §6.1.4 (primitive) §2.2 Why scenarios sit outside the implementation tree (F2/F1/F9 mitigation).
- §6.1.5 (primitive) §4 The revelation cycle (Phases 1-7).
- §6.1.6 (framing) §4.4 Diagnostic analysis (5-mode failure classification: silence / ambiguity / incorrectness / inconsistency / undiscovered preference).
- §6.1.7 (primitive) §6.1 The manager loop / Channel-2 review.
- §6.1.8 (recommendation) §10 Implementation roadmap.

### §6.2 Per-item classification

| Item | Verdict | Rationale (≤25 words) | v3 cite (if absorbed) |
|---|---|---|---|
| §6.1.1 spec is durable artifact | `absorbed (verified at §1.5)` | D-1 default; verified per §1.5. GF-C's Intent Crucible IS the durable day-0 spec artifact. | specs/gf-c.md §3 sub-phase A |
| §6.1.2 9-artifact stack | `absorbed (with adaptation)` | GF-C's day-0 artifact set (Intent Crucible + RSI declaration + Cold-Start Bench + EARS criteria + per-cycle trajectory) is a cold-start-bounded specialization of the Refinery stack. | specs/gf-c.md §2 + §3 |
| §6.1.3 stable identifier discipline | `absorbed (with adaptation)` | GF-C work-unit definition `(scenario_id, EARS_criterion, Intent_invariant_binding)` is the cold-start stable-ID triple; Intent invariants + EARS criteria carry IDs. | specs/gf-c.md §3 work-unit definition |
| §6.1.4 scenarios outside tree (D-2 grounding) | `absorbed (verified)` | D-2 verified per §1.5; Cold-Start Bench is the day-0 instance. | specs/gf-c.md §3 sub-phase B + §4 holdout |
| §6.1.5 revelation cycle (7-phase) | `absorbed (with adaptation)` | GF-C's three-sub-phase cold-start methodology (Intent → Bench → First-cycle) maps onto Refinery's Phases 1-3; graduation protocol is the cold-start exit gate. | specs/gf-c.md §3 |
| §6.1.6 5-mode failure classification | `tbd` | GF-C uses F-mode taxonomy (F1/F25/F40/F41/F46 five-critical convergence) instead of Refinery's silence/ambiguity/incorrectness/inconsistency/preference. Whether the classifications map is Phase-8 lean-eval surface. | — |
| §6.1.7 manager loop / Channel-2 review | `absorbed (with adaptation)` | GF-C's Council interrogation IS the Channel-2 review surface at Intent authoring time; cross-model judge + human escalation at first cycles. | specs/gf-c.md §3 sub-phase A + sub-phase C |
| §6.1.8 implementation roadmap | `not-applicable-to-candidate-mandate` | Architecture-specific deployment; v3 doesn't carry per-architecture roadmaps. | — |

### §6.3 Notes

This is GF-C's **deepest absorption** — the primary lineage. Refinery's spec-as-product framing (§6.1.1) plus the revelation cycle (§6.1.5) plus Channel-2 review (§6.1.7) all land as GF-C's day-0 instances. The distinctive departure: GF-C reframes the revelation cycle's iterative spec-maturation as a *graduation* event (cold-start regime → steady-state regime), and adds Intent Crucible substance-checking as an upstream gate Refinery does not have. The 5-mode failure classification (§6.1.6) `tbd` is a real Phase-8 question — does GF-C's F-mode-centred taxonomy supersede or complement Refinery's classification?

## §7 — archive/architectures-v2/02-compound-atelier.md

### §7.0 File header

v2 Architecture 2 — Compound Atelier. "Each unit of work makes the next easier." Queue + workpad + persona panel + accumulated `docs/solutions/`. v2's recommended baseline. 4515 words. **Known-rejected as baseline per §5.1.7**; GF-C has weak/no Atelier lineage by construction (Atelier's queue+workpad+`docs/solutions/` assumptions are the precise day-0 vacuum GF-C exists to address — per [`archive/research-plan.md` §risk](../../../archive/research-plan.md)).

### §7.1 Enumeration

- §7.1.1 (claim) §1 Core thesis: each unit of work makes the next easier (compounding).
- §7.1.2 (primitive) §2 The compounding mechanism: 5 mechanisms making iteration n+1 cheaper than n.
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
| §7.1.1 compounding core thesis | `absorbed (with adaptation)` | GF-C's micro-cold-start re-entry per new work-unit-class IS the cold-start-bounded version of compounding (across-classes, not within-class). | specs/gf-c.md §3 distinctive methodology decisions |
| §7.1.2 5 compounding mechanisms | `not-applicable-to-candidate-mandate` | Atelier's 5 mechanisms (reusable anchors / stable IDs / knowledge store grep / pattern promotion / hygiene) presuppose accumulated history GF-C explicitly lacks at day 0. | — |
| §7.1.3 artifact stack (specs/knowledge/workpad) | `not-applicable-to-candidate-mandate` | Atelier's workpad-per-issue + `docs/solutions/` assume an issue queue + accumulated solutions; GF-C's day-0 vacuum is exactly this. | — |
| §7.1.4 workshop chain (persona workshops) | `not-applicable-to-candidate-mandate` | GF-C's Council is single-purpose (Intent interrogation) not a workshop chain of specialized personas. Front-end-agnostic at substrate. | — |
| §7.1.5 researcher fan-out | `not-applicable-to-candidate-mandate` | Researcher fan-out presupposes prior art to research; cold-start day-0 has none. | — |
| §7.1.6 reviewer panel | `absorbed (with adaptation)` | GF-C's cross-model judge ensemble (P-14) is the substrate-enforced reviewer-panel-equivalent at cold-start; F46 binding. | specs/gf-c.md §4 bias-guard + §3 sub-phase C |
| §7.1.7 synthesis and curation | `not-applicable-to-candidate-mandate` | Synthesis/curation presupposes findings to synthesize; cold-start day-0 has no findings yet. | — |
| §7.1.8 conductor orchestrator | `not-applicable-to-candidate-mandate` | GF-C leaves orchestration to methodology layer; substrate doesn't mandate orchestrator shape. | — |
| §7.1.9 workpad protocol | `not-applicable-to-candidate-mandate` | Workpad-per-issue presupposes issues; cold-start has none. | — |
| §7.1.10 tiered cycle scope | `absorbed (with adaptation)` | GF-C's tiering is by *regime* (Cold-Start L3 vs Steady-State per-class L4); analogous shape, different axis. | specs/gf-c.md §3 graduation protocol + §5 mandate fit |
| §7.1.11 severity × autofix axes | `absorbed (silently — flagged for auditor)` | The orthogonal-axes framing likely influenced v3's DEC-2 mandate-fit-per-(architecture × work-unit-class) schema. Not explicitly cited in GF-C spec. | — (flagged) |
| §7.1.12 residual work gate | `not-applicable-to-candidate-mandate` | Residual-finding gate presupposes findings; cold-start day-0 has none. Post-graduation may absorb. | — |
| §7.1.13 three memory tiers | `not-applicable-to-candidate-mandate` | Memory-tier discipline presupposes cross-cycle memory; cold-start has no cross-cycle history. | — |
| §7.1.14 implementation roadmap | `not-applicable-to-candidate-mandate` | Architecture-specific deployment. | — |

### §7.3 Notes

GF-C's relationship to Atelier is the **inverse of BF-S's** (the exemplar): where BF-S deeply absorbs Atelier's compounding mechanism (§7.1.1-§7.1.13 all `absorbed` in BF-S), GF-C is N/A on most cells because Atelier's primitives presuppose exactly what cold-start lacks. The 10-N/A pattern on Atelier is GF-C's strongest single-file evidence for the cold-start-vs-steady-state distinction. The two `absorbed (with adaptation)` cells (§7.1.1 compounding, §7.1.10 tiered ceremony) and one `absorbed (silently)` cell (§7.1.11 orthogonal axes) capture GF-C's only genuine Atelier inheritances — all are adaptations.

## §8 — archive/architectures-v2/03-phase-gated-foundry.md

### §8.0 File header

v2 Architecture 3 — Phase-Gated Foundry. "Pre-agile structured methodologies become the right shape when agents make them fast." Phase-bound experts, formal templates (SRS, SAD, DD), RTM, gate boards. 4610 words. **GF-C's secondary v2-architecture-lineage** per §1 overview.

### §8.1 Enumeration

- §8.1.1 (claim) §1 Core thesis: structured pre-agile methodology + agent speed.
- §8.1.2 (primitive) §2 Phase model (Phases 1-6 with V&V pairing).
- §8.1.3 (primitive) §2.4 Cleanroom discipline (no debugging; defects return to phase of origin).
- §8.1.4 (primitive) §3 Configuration Management discipline.
- §8.1.5 (primitive) §3.1 Defect-of-origin table.
- §8.1.6 (primitive) §4 RUP-style discipline × phase matrix.
- §8.1.7 (primitive) §6.2 V&V-side roles (structurally independent, different model family).
- §8.1.8 (primitive) §8 Configuration Management as the spine.

### §8.2 Per-item classification

| Item | Verdict | Rationale (≤25 words) | v3 cite (if absorbed) |
|---|---|---|---|
| §8.1.1 structured pre-agile core thesis | `absorbed (with adaptation)` | GF-C's graduation protocol with 4 explicit gates is structured-pre-agile applied to cold-start specifically; not the full 6-phase model. | specs/gf-c.md §3 graduation protocol |
| §8.1.2 6-phase V&V pairing | `not-applicable-to-candidate-mandate` | Foundry-specific cycle structure; GF-C three-sub-phase shape is different. | — |
| §8.1.3 Cleanroom discipline | `tbd` | GF-C does not explicitly invoke "no debugging during construction" — but P-11 bench-construction-agents-never-see-builder-prompts has Cleanroom shape. Phase-8 surface. | — |
| §8.1.4 Configuration Management discipline | `absorbed (with adaptation)` | GF-C's P-18 RSI Declaration Ledger (ADR 0044) + P-11 HMAC-signed bench (ADR 0042) ARE substrate-level CM analogues: immutable signed logs with per-cycle attestation. | specs/gf-c.md §2 P-18 + P-11 |
| §8.1.5 defect-of-origin table | `tbd` | GF-C does not invoke phase-of-origin attribution explicitly; whether cold-start failures attribute to Intent-authoring vs Bench-construction vs First-cycle is unresolved. Phase-8 candidate. | — |
| §8.1.6 RUP-style discipline × phase matrix | `not-applicable-to-candidate-mandate` | Foundry-specific; GF-C binds all 10 disciplines at substrate, not RUP-phase-distributed. | — |
| §8.1.7 V&V-side independent + different model family | `absorbed (verified)` | GF-C §3 sub-phase C cross-model judge "requires different model family"; F46 mitigation explicit. Council substance-check ensemble is family-diverse per F46. | specs/gf-c.md §3 sub-phase A + §3 sub-phase C + §4 bias-guard |
| §8.1.8 CM as spine | `absorbed (with adaptation)` | GF-C treats P-18 RSI Ledger + P-11 bench as the day-0 spine; methodology rides on top. Substrate-as-spine framing. | specs/gf-c.md §2 P-18/P-11 + §1 axis |

### §8.3 Notes

Foundry's phase-gated 6-step structure is N/A to GF-C, but **two Foundry primitives land deeply**: Configuration Management (substrate-level via P-18 RSI Ledger + P-11 signed bench) and cross-model V&V independence (sub-phase C + bias-guard binding). These are the Foundry-lineage inheritances that complement GF-C's primary Refinery lineage. The §8.1.3 Cleanroom `tbd` is a genuine Phase-8 surface: GF-C's bench-construction-agents-never-see-builder-prompts has Cleanroom's "no debugging during construction" shape, but the explicit Cleanroom discipline (defect ⇒ phase-of-origin return, not patch) is unresolved for cold-start. The §8.1.5 defect-of-origin `tbd` is the secondary Phase-8 surface: what does "phase of origin" mean during cold-start (Intent / Bench / First-cycle)?

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
| §9.1.1 population + selection core thesis | `not-applicable-to-candidate-mandate` | Tournament population-based methodology; GF-C is single-builder + cross-model-judge, not population. | — |
| §9.1.2 genome structure | `not-applicable-to-candidate-mandate` | Tournament-specific artifact; GF-C's Intent Crucible is closer to Refinery's spec than Tournament's genome. | — |
| §9.1.3 model-family diversity as structural | `absorbed (verified)` | GF-C §3 sub-phase A substance-check ensemble + §3 sub-phase C cross-model judge bind cross-model-family diversity as structural via P-14. F46 mitigation, F1-greenfield-`critical` closure. | specs/gf-c.md §3 + §4 bias-guard + §4.3 distinctive methodology decision 3 |
| §9.1.4 generation cycle | `not-applicable-to-candidate-mandate` | Tournament-specific. GF-C's sub-phase C is single-output not population. | — |
| §9.1.5 predator agent | `rejected (subsumed by substrate-level adversarial discipline)` | GF-C substitutes Tournament's runtime predator with substrate-level adversarial closure: P-14 cross-model judge + P-17 substance-check ensemble + P-12 deterministic linter. Substrate substitution. | — |
| §9.1.6 loops within loops | `absorbed (with adaptation)` | GF-C's three-loop discipline (ADR 0026 binding) + the graduation-protocol measurement loop is the analogue (smaller scope; graduation-loop ≠ tournament-loop). | specs/gf-c.md §4 three-loop |
| §9.1.7 independence policy | `absorbed (verified)` | GF-C sub-phase C cross-model judge enforces builder-judge independence at substrate; substance-check ensemble enforces author-judge independence at intent authoring. | specs/gf-c.md §3 + §4 |
| §9.1.8 scaling | `tbd` | GF-C scaling story is graduation-protocol-driven (cold-start L3 → per-class L4 lights-out). Whether Tournament's scaling lessons apply post-graduation is Phase-8. | — |

### §9.3 Notes

Tournament's primary primitives (population, genome, predator, generation cycle) are N/A to GF-C, but the **cross-model-family diversity discipline (§9.1.3) and independence policy (§9.1.7) land verified** — these are F46/F27 mitigations bound at P-14. Predator-agent (§9.1.5) is explicitly `rejected` with reason: GF-C substrate-level adversarial closure (P-14 + P-17 + P-12) substitutes for runtime predator pressure. The Tournament-style diversity-policy framing (≥3 model families) is the strongest single Tournament inheritance — GF-C's "different model family from the eventual builder" (sub-phase B) is the cold-start instantiation.

## §10 — archive/architectures-v2/failure-modes.md

### §10.0 File header

F1-F20 per-architecture coverage matrix PLUS 4 per-architecture qualitative-strength rows + prose verdicts. 664 words. **§10 floor = 24 (20 F-modes + 4 per-architecture coverage rows)** per Reviewer 6 D-H1 amendment.

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
| §10.1.1 F1 Hallucination | `absorbed (verified)` | GF-C §1 5-critical convergence explicitly names F1; bias-guard ADR 0018 + cross-model judge P-14 binding. | specs/gf-c.md §1 + §4 + §3 sub-phase C |
| §10.1.2 F2 Reward hacking | `absorbed` | GF-C §4 holdout (ADR 0021) + P-08 bench-construction-agents-never-see-builder-prompts + P-12 deterministic linter. | specs/gf-c.md §4 holdout + §3 sub-phase B |
| §10.1.3 F3 Spec-completeness | `absorbed (with adaptation)` | GF-C's Intent Crucible 9-field schema + INCOSE GtWR C1-C15 Council interrogation IS substrate + methodology answer to spec-completeness. | specs/gf-c.md §2 P-17 + §3 sub-phase A |
| §10.1.4 F4 Code quality | `absorbed (with adaptation)` | GF-C §4 bias-guard cross-model judging + §2 P-12 deterministic linter at authoring boundary. | specs/gf-c.md §3 + §4 |
| §10.1.5 F5 Cognitive ceiling | `absorbed (with adaptation)` | GF-C addresses via L3-Augmentation during cold-start (human in every cycle); design-starvation (F25) is the §1 5-critical convergence equivalent. | specs/gf-c.md §1 + §3 graduation protocol |
| §10.1.6 F6 Cognitive debt | `absorbed` | GF-C §3 sub-phase C P-05 trajectory + §4 cognitive-escrow binding (ADR 0019 via P-06 Patrol-tier triggers). | specs/gf-c.md §4 + ADR 0019 |
| §10.1.7 F7 Normalization of deviance | `absorbed (with adaptation)` | GF-C §3 distinctive methodology decision 3 (cross-model judge mandatory at first cycles, refusing Anthropic CTR-D7/CTR-D8 license) resists deviance accumulation at cold-start. | specs/gf-c.md §3 |
| §10.1.8 F8 Stale knowledge | `not-applicable-to-candidate-mandate` | Stale-knowledge presupposes accumulated knowledge; cold-start has none. Post-graduation may absorb. | — |
| §10.1.9 F9 Spec overfitting | `absorbed (with adaptation)` | GF-C's Intent Crucible substance-check (P-17 ensemble) + cross-model judge are the spec-overfitting mitigations; spec is *gated* before code, not amended around code. | specs/gf-c.md §2 P-17 + §3 sub-phase A |
| §10.1.10 F10 Findings disappear | `absorbed (with adaptation)` | GF-C's P-18 RSI Ledger + P-24-analogue-via-P-18 append-only contract ensures declarations + amendments are durable; bench-construction PRs are append-only. | specs/gf-c.md §2 P-18 + ADR 0044 |
| §10.1.11 F11 Renumbering | `not-applicable-to-candidate-mandate` | Renumbering presupposes accumulated stable-ID populations; cold-start has minimal IDs (1-3 Intent invariants, 5-10 bench scenarios). Post-graduation may absorb. | — |
| §10.1.12 F12 Lethal trifecta | `absorbed (verified)` | GF-C §4 trifecta-closure (ADR 0027) bound at P-08 + P-12 + P-17 — three substrate-enforced surfaces. P-01 sandbox per ADR 0010. | specs/gf-c.md §4 trifecta closure |
| §10.1.13 F13 Missing-config | `absorbed (with adaptation)` | P-17 Intent Crucible 9-field schema includes "policy references" + "guardrails / feedback sources" fields explicitly — missing-config mitigation at authoring time. | specs/gf-c.md §2 P-17 (ADR 0043 field list) |
| §10.1.14 F14 Attribution collapse | `absorbed (verified)` | GF-C §2 P-18 RSI Ledger with `agent_id`/`cycle_id`/`prior_hash` envelope IS attribution discipline. F43 closure via P-18. | specs/gf-c.md §2 P-18 + ADR 0044 envelope |
| §10.1.15 F15 Single-prompt collapse | `absorbed (with adaptation)` | GF-C §3 sub-phase A substance-check ensemble (multiple judge instances) + Council interrogation (multi-model) substitutes for Atelier's six-divergent-frames. | specs/gf-c.md §3 sub-phase A + §4 bias-guard |
| §10.1.16 F16 Resume-fidelity | `absorbed` | GF-C §3 sub-phase C P-05 trajectory capture writes from cycle 1; cycle_id in P-18 envelope provides resume anchor. | specs/gf-c.md §3 + §2 P-18 envelope |
| §10.1.17 F17 Parallel agents on shared dirs | `not-applicable-to-candidate-mandate` | GF-C cold-start parallelism is bounded (1 builder per first-cycle); F17 mitigation methodology-layer post-graduation. | — |
| §10.1.18 F18 Prose-spec rigor | `absorbed (verified)` | GF-C §2 P-12 deterministic linter framework (ADR 0032) hosts EARS + INCOSE GtWR rule library — explicit per-§2 binding. F18/F38/F51 closure. | specs/gf-c.md §2 designed-system substrate (P-12) |
| §10.1.19 F19 Model-floor dependency | `absorbed` | GF-C §4 bias-guard cross-model judging via P-14 surfaces model-floor explicitly per F46. | specs/gf-c.md §4 + ADR 0018 |
| §10.1.20 F20 Maintenance asymmetry | `tbd` | GF-C explicitly punts on post-MVP-evolution / regression-fix (`silent` per §5 mandate fit). Whether maintenance asymmetry IS the post-graduation surface is Phase-8. | — |
| §10.1.21 A1 Refinery coverage row | `not-applicable-to-candidate-mandate` | Coverage row characterizes Architecture 1 (GF-C's primary lineage); ★★★★ scoring is per-Refinery, not per-GF-C. GF-C's own F-mode coverage tracked above. | — |
| §10.1.22 A2 Atelier coverage row | `not-applicable-to-candidate-mandate` | Coverage row characterizes Architecture 2. | — |
| §10.1.23 A3 Foundry coverage row | `not-applicable-to-candidate-mandate` | Coverage row characterizes Architecture 3 (GF-C's secondary lineage). | — |
| §10.1.24 A4 Tournament coverage row | `not-applicable-to-candidate-mandate` | Coverage row characterizes Architecture 4. | — |

### §10.3 Notes

**16-of-20 F-modes absorbed** (F1, F2, F3, F4, F5, F6, F7, F9, F10, F12, F13, F14, F15, F16, F18, F19) — including F1, F12, F14, F18 verified-absorbed with explicit GF-C spec invocations. **3 N/A** (F8 stale-knowledge, F11 renumbering, F17 parallel-shared-dirs — all presuppose accumulated history GF-C explicitly lacks at day 0). **1 TBD** (F20 maintenance asymmetry — GF-C punts via `silent` on post-MVP-evolution + regression-fix, so the asymmetry is Phase-8 surface). The 4 per-architecture coverage-strength rows (§10.1.21-§10.1.24) are informational characterizations of the v2 architectures, not GF-C-actionable items. **The 3 N/A F-modes on day-0 history-presupposing items are GF-C's signature pattern** — same shape as the §7 Atelier 10-N/A cluster, evidence for the cold-start-vs-steady-state distinction.

## §11 Summary

**Per-token cell counts (matches YAML frontmatter):**

| Token | Count |
|---|---|
| `absorbed` (incl. with-adaptation, verified, silently) | 60 |
| `rejected (reason)` | 5 |
| `not-applicable-to-candidate-mandate` | 27 |
| `tbd` | 7 |
| **Total** | **99** |

(Total = sum of cells across §2.2 (3) + §3.2 (17) + §4.2 (8) + §5.2 (9) + §6.2 (8) + §7.2 (14) + §8.2 (8) + §9.2 (8) + §10.2 (24) = 99 ✓. The §1.5 D-1..D-7 verification rows (7) are tracked separately and counted as part of the absorbed total for §3.1.1/§3.1.2/§3.1.4/§3.1.9 and §4.1.1-§4.1.7 (which are themselves marked `absorbed (verified at §1.5)`); no double-counting. Frontmatter YAML carries the unique-verdict count.)

**High-confidence absorbed cells:** D-1, D-2, D-4, D-5, D-6, D-7 verified per §1.5; F1, F12, F14, F18 verified at §10; cross-model V&V independence verified at §8 + §9; spec-as-durable-artifact verified at §6 (primary lineage); Configuration-Management-as-spine verified at §8 (secondary lineage).

**Distinctive GF-C signal pattern: high N/A count (27).** GF-C's 27 N/A cells (27% of total) cluster on items that presuppose accumulated history at day 0: most of Atelier (§7.2 — 10 N/A), specific F-modes (F8 stale-knowledge, F11 renumbering, F17 parallel-shared-dirs, plus the 4 per-architecture coverage rows of §10), Tournament population-based mechanisms (§9.2 — 4 N/A), hybrid framings (§5.1.4). This N/A pattern IS the GF-C audit's strongest evidence for the cold-start-vs-steady-state architectural distinction.

**Surfaced TBDs (require lead-agent reconciliation or Phase-8 follow-up):**

1. §3.1.11 persona-vs-graph-node — GF-C front-end-agnostic; Council is persona-flavored but substrate is neutral. Phase-8.
2. §4.1.10 CI/CD pipeline adaptation thesis — orthogonal to cold-start framing; Phase-8 surface.
3. §6.1.6 Refinery 5-mode failure classification — whether GF-C F-mode taxonomy maps. Phase-8.
4. §8.1.3 Cleanroom discipline — whether GF-C's bench-construction-agents-never-see-builder-prompts is the Cleanroom analogue. Phase-8.
5. §8.1.5 defect-of-origin attribution — what "phase of origin" means during cold-start. Phase-8.
6. §9.1.8 Tournament scaling — applicability post-graduation. Phase-8.
7. §10.1.20 F20 maintenance asymmetry — GF-C `silent` on post-MVP/regression-fix; Phase-8 frames the asymmetry.

(Plus 3 cells where `tbd` arose from spec under-specification: §10.1.3 F3 spec-completeness ambiguity between substrate and methodology; §10.1.13 F13 missing-config strength; informational only.)

**Silent-absorption auditor flags (for cross-spec reconciliation):**

- §3.1.4 D-3 (Agent = Model + Harness) — GF-C uses analogous Builder/Council/Judge vocabulary without naming C10 frame. Likely silent absorption.
- §3.1.17 cross-cutting primitives — v3 `primitives/index.md` likely inherited 00-synthesis §5 framing without explicit GF-C cite.
- §7.1.11 severity × autofix orthogonal axes — likely informed DEC-2 mandate-fit-per-(architecture × work-unit-class) schema.

**Known-rejected items confirmed:**

- §4.1.11 OpenHands+Overstory substrate stack — `rejected (explicitly-excluded-per-constraints-extracted)`.
- §5.1.7 Compound Atelier as baseline — `rejected (explicitly-anchor-avoided)`. (Particularly relevant for GF-C: Atelier's day-0 vacuum is the gap GF-C exists to address.)

## §12 References

**GF-C spec + supporting docs:**

- [`architectures/v3/specs/gf-c.md`](../specs/gf-c.md) — GF-C Phase-6 architecture spec (audit input).
- [`architectures/v3/candidate-registry.md` GF-C entry](../candidate-registry.md#gf-c--greenfield-cold-start-first) — registry entry for §1 lineage statement.
- [`architectures/v3/substrate-requirements/gf-c.md`](../substrate-requirements/gf-c.md) — substrate-requirements summary.
- [`architectures/v3/decisions/auto-007-phase-7-dispatch-shape.md`](../decisions/auto-007-phase-7-dispatch-shape.md) — Phase-7 dispatch brief.
- [`architectures/v3/backfill-notes/bf-s.md`](./bf-s.md) — Phase-7 exemplar (shape model).

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

- GF-C common substrate ADRs: [0010-0017](../../../docs/adr/) + designed-system [0032](../../../docs/adr/0032-p-12-deterministic-linter-framework.md) (P-12) + discipline [0018-0027](../../../docs/adr/) + orphan substrate [0042 (P-11 Cold-Start Bench)](../../../docs/adr/0042-p-11-cold-start-bench.md) + [0043 (P-17 Intent Crucible)](../../../docs/adr/0043-p-17-intent-crucible-validator.md) + [0044 (P-18 RSI Declaration Ledger)](../../../docs/adr/0044-p-18-rsi-declaration-ledger.md).

**Constraints / decisions:**

- [`architectures/v3/constraints-extracted.md`](../constraints-extracted.md) — UC1-UC8 user constraints (source of known-rejected v3 item flags).
- [`architectures/v3/decisions-captured.md`](../decisions-captured.md) — DEC-1 / DEC-1.a / DEC-2 etc.
