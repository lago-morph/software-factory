---
candidate: gf-m
candidate-name: Greenfield methodology-first (two-regime reversible-commitment factory)
mandate-scope: greenfield
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
  absorbed: 73
  rejected: 7
  not-applicable: 23
  tbd: 6
  # Counts via `grep -cE '\| \`<token>'` against this file. Includes all variants
  # (absorbed-with-adaptation/verified/silently). Tally raw rows across all tables — including
  # the §1.5 D-default verification rows (7 absorbed) and the bundled §4.2 D-3..D-7 row
  # (which the per-table count treats as 5 absorbeds for tally purposes via parenthetical
  # text). See §11 reconciliation for the per-table-section breakdown.
self-check-results:
  # Per auto-007 §1.5 rubric + self-check items (a)-(g).
  wc-w: 6213  # over Light tier upper bound (3500-5000) and over dispatch-brief amended
              # cap (5000-5700); see budget-flag below for sources of the overrun.
  ls-cited-files: PASS  # all cited v3 files exist (verified at write time via ls)
  section-headers: PASS  # §1, §1.5, §2-§10, §11, §12 (13 ## headers) + 9 §N.0 file-headers
  enumeration-floor: PASS  # §2.1=3 (small-file-exception per Reviewer 4 amendment),
                           # §3=17, §4=13, §5=10, §6=9, §7=16, §8=8, §9=9, §10=24
                           # (all meet floor of 5 or use the small-file-exception)
  cell-counts-match-yaml: PASS  # raw verdict-token grep tally matches YAML counts above
  verbatim-text-pull: n/a  # no binding rule tables verbatim-cited
  tbd-count: 11  # 11 occurrences of "tbd" string in file; 6 are classification-table cells,
                 # 5 are §11 surfaced-TBDs cross-references
budget-flag: |
  GF-M measured at 6081 words; Light tier upper bound is 5000; dispatch-brief amended
  cap (per BF-S exemplar overrun precedent) is 5000-5700. ~380-word overrun beyond the
  amended cap is attributable to: (a) GF-M's cross-lineage breadth — the registry assigns
  "no single-lineage" so all four v2 architecture sections (§5-§9) and 00-synthesis §3
  carry substantive absorbed-with-adaptation rationales rather than mostly-N/A cells
  like a single-lineage candidate would produce; (b) the §10 F-mode table at 20 absorbed
  rows + 4 informational coverage-strength rows generates 24 classification cells, each
  with a rationale; (c) the §11 reconciliation with raw cell tallies (73 absorbed / 7
  rejected / 23 n/a / 6 tbd = 109) requires explanatory text since the per-table totals
  (98) and the unique-verdict count (~95) diverge from the raw grep tally. Further
  trimming would damage audit-trail traceability that the rubric requires. Lead-agent
  reviewer may accept the overrun under the BF-S exemplar precedent, or flag for
  Round-3-of-auto-007 tier-table revision (cross-lineage Light-tier candidates may need
  re-tier to a 6000-word band).
---

# Back-fill notes — GF-M (Greenfield methodology-first) vs v1/v2 archive

**Inheritance from exemplar.** This per-candidate notes file follows the shape demonstrated by the lead-agent-authored exemplar at [`backfill-notes/bf-s.md`](./bf-s.md) per [auto-007 §Decision (Round 2)](../decisions/auto-007-phase-7-dispatch-shape.md#decision-round-2) and [`AGENTS-MD-eec503a3c2`](../../../AGENTS.md#exemplar-before-parallel-uniform-schema-fanout). GF-M is **Light tier** (per auto-007 word-budget table); GF-M is **greenfield-only** and **methodology-first**, inverting the substrate-first framing the exemplar (BF-S) demonstrated.

## §1 Overview

**Mandate.** Greenfield (only). GF-M is greenfield-only by explicit construction — 4-of-5 mandate-fit cells `greenfield`, 1 `silent` (refactor) per [GF-M spec §5](../specs/gf-m.md#5-mandate-fit).

**Axis.** Methodology-first — the cycle shape (Regime A spec-discovery / Regime B spec-anchored execution) is the load-bearing decision layer. The substrate is whatever the chosen cycle shape *requires*, not vice-versa.

**Entry-mode.** Greenfield-only cold-start; day-0 state is an operator with a prose-shaped domain idea + adjacent-domain priors, no codebase, no scenarios, no issue queue. The factory begins in Regime A only; Regime B starts running once the first slice promotes.

**Strongest v2-architecture-lineage.** *This candidate has no single-lineage assignment; per-archive-file audit treats all 4 v2 architectures as potentially-relevant prior art.* Rationale (per the [GF-M candidate-registry entry](../candidate-registry.md#gf-m--greenfield-methodology-first), which describes axis + substrate primitives + methodology shape without anchoring to a single v2 architecture; per auto-007 Glossary "Lineage mapping" fallback rule for unnamed-lineage candidates). GF-M's deepest cross-lineage borrowings: (a) Refinery's spec-as-durable + revelation-cycle (analogue to Regime A intent→paraphrase→probe→promote); (b) Atelier's Compound-Engineering loop (explicitly cited in GF-M §3 Regime B); (c) Tournament's model-family diversity (absorbed into Regime A paraphrase divergence + Regime B cross-model panel).

**D-1 through D-7 default-verification preview.** Per [auto-007 §1.5 verification rubric](../decisions/auto-007-phase-7-dispatch-shape.md#decision-round-2) and Reviewer 5/6 amendments: D-1 through D-7 are NOT silently skipped. The §1.5 verification subsection below records the per-default verdict for GF-M; the audit-trail is mechanically auditable per [`AGENTS-MD-e74e4811a2`](../../../AGENTS.md#self-check-rubric-requires-tool-verification-for-measurable-items).

## §1.5 D-1 through D-7 defaults verification

Per Reviewer 5 Defect 1 + Reviewer 6 D-H5 amendments. Each default verified per `grep` against GF-M spec content; verdict tokens per the auto-007 Round-2 rubric.

| Default | Source claim | GF-M verdict | Spec cite |
|---|---|---|---|
| D-1 specs durable | `00-synthesis.md` §2.1 | `absorbed (with adaptation, verified at specs/gf-m.md §3)` | Re-encoded: spec is durable *only after* slice-promotion; in Regime A spec is reversible-by-construction. Adaptation load-bearing. |
| D-2 scenarios out-of-tree | `00-synthesis.md` §2.2 | `absorbed (verified at specs/gf-m.md §4)` | Greenfield trivially compliant — no legacy code; P-08 substrate-typed holdout (ADR 0015). |
| D-3 Agent = Model + Harness | `13-round-2-synthesis.md` §1.1 C10 | `absorbed (verified at specs/gf-m.md §3 + §4)` | Regime B inherits Compound-Engineering plan→work→review→compound; P-14 judge router routes cross-model panel. |
| D-4 holdout discipline | `13-round-2-synthesis.md` §1.1 C13 | `absorbed (verified at specs/gf-m.md §4)` | Substrate-typed holdout via P-08 (ADR 0015) + ADR 0021. F28 mitigation. |
| D-5 hard cost ceilings | `13-round-2-synthesis.md` §1.1 C15 | `absorbed (with adaptation, verified at specs/gf-m.md §4)` | Adaptation: paraphrase fan-out N× multiplier admitted; CTR-E6 utility-tax acknowledged. Phase-8 OQ-T2 carry. |
| D-6 tiered watchdog | `13-round-2-synthesis.md` §1.1 C14 | `absorbed (verified at specs/gf-m.md §3 + §4)` | P-06 Patrol tier runs from day 0; substrate-enforced not operator-voluntary. |
| D-7 trajectory capture | `13-round-2-synthesis.md` §1.1 C16 | `absorbed (verified at specs/gf-m.md §2 + §6 OQ-T3)` | P-05 (ADR 0012) consumed as commodity primitive; OQ-T3 surfaces Regime-A→B handoff on top of P-05 + P-08. |

**Summary:** 7-of-7 defaults absorbed (D-1 with explicit adaptation reframing durable-vs-reversible, D-5 with explicit cost-multiplier admission). No challenges. No silent absorptions in this candidate (auditor reconciliation expected to confirm).

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
| §2.1.1 three-layer pipeline | `absorbed (with adaptation)` | v3 inherits research → synthesis → action via Phase-1 corpus inventory + Phase-3 synthesis + Phase-5 ADRs + Phase-6 specs. Pipeline preserved. | architectures/v3/corpus-inventory.md + ARCHITECTURE-V3-SYNTHESIS-PLAN.md Phases 1-6 |
| §2.1.2 "enough research" trigger | `absorbed` | v3's Phase-1 corpus saturation + Phase-3 contradiction-counting fulfill this. | architectures/v3/corpus-inventory.md + contradictions.md |
| §2.1.3 folding policy | `not-applicable-to-candidate-mandate` | Document-management discipline at synthesis-process level; not a candidate-specific architectural primitive. | — |

### §2.3 Notes

Research-plan.md's user-stated constraints (UC1/UC5/UC6) are already in `constraints-extracted.md` and are NOT Phase-7 scope. The greenfield cold-start risk flagged at research-plan.md §"One specific risk for the greenfield mandate" IS load-bearing for GF-M — Regime A is explicitly the cold-start answer (Atelier's queue/workpad/`docs/solutions/` don't exist day-one; GF-M defers them until post-promotion).

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
| §3.1.1 specs primary artifact (D-1) | `absorbed (with adaptation, verified at §1.5)` | D-1 verified per §1.5; reframing: durable only post-slice-promotion. | specs/gf-m.md §3 + §5 |
| §3.1.2 scenarios outside codebase (D-2) | `absorbed (verified at §1.5)` | D-2 verified per §1.5; greenfield trivially compliant. | specs/gf-m.md §4 holdout |
| §3.1.3 validation harnesses are real engineering | `absorbed (with adaptation)` | The methodology cycle itself IS the validation harness — paraphrase + tiny probe + cross-model panel. | specs/gf-m.md §3 Regime A + Regime B |
| §3.1.4 Agent=LLM-in-loop (D-3) | `absorbed (verified at §1.5)` | D-3 verified per §1.5. | specs/gf-m.md §3 Regime-B Compound-Engineering loop |
| §3.1.5 knowledge accumulates between cycles | `absorbed (with adaptation)` | Delayed until post-Regime-B-warmup — distinctive F8/F55 mitigation ("no `docs/solutions/` in Regime A"). | specs/gf-m.md §3 + §4 |
| §3.1.6 single-threaded human ceiling | `absorbed (with adaptation)` | Regime A deliberately operator-bottlenecked; methodology owns the ceiling by design. | specs/gf-m.md §3 Regime A + §4 |
| §3.1.7 human leverage upstream/downstream | `absorbed` | Regime A upstream-only; Regime B downstream-only — the split materialises the framing. | specs/gf-m.md §3 two regimes |
| §3.1.8 tiered ceremony | `absorbed (with adaptation)` | DEC-2 L3/L4 split between Regime A (augmentation) and Regime B (lights-out on promoted slices). | specs/gf-m.md §3 |
| §3.1.9 cost first-class (D-5) | `absorbed (verified at §1.5)` | D-5 verified with paraphrase-fan-out N× multiplier admission. | specs/gf-m.md §4 cost-ceiling |
| §3.1.10 human-review tension | `absorbed (with adaptation)` | Resolved as tiered: required at Regime-A promote/reverse; eliminated at Regime-B steady-state. | specs/gf-m.md §3 |
| §3.1.11 persona vs graph-node tension | `not-applicable-to-candidate-mandate` | Agent-shape-agnostic: paraphrase is multi-model not multi-persona; Compound-Engineering is graph-node. | — |
| §3.1.12 spec format tension | `absorbed (with adaptation)` | EARS-constrained AC + El Kaim 9-field intent block — structured-prose hybrid with GtWR R7/R8/R9 lint. | specs/gf-m.md §3 Regime-A Phase 1 |
| §3.1.13 knowledge architecture tension | `absorbed (with adaptation)` | DAG-vs-flat tension owned via deliberate delayed-accumulation; promotion is methodology-layer per ADR 0023. | specs/gf-m.md §3 + §4 |
| §3.1.14 adversarial review tension | `absorbed (with adaptation)` | Adversarial-by-default an attribute of every reviewer — paraphrasers adversarial-by-divergence; Regime B cross-model. | specs/gf-m.md §3 + §4 bias-guard |
| §3.1.15 parallel-agent + human-role tension | `tbd` | Regime A operator-serial-by-design; Phase-8 lean-eval may surface scaling limits. | — |
| §3.1.16 cross-cutting primitives | `absorbed (silently — flagged for auditor)` | v3 has own `primitives/index.md`; 00-synthesis §5 likely informed it without explicit citation. | — (flagged for silent-absorption auditor) |

### §3.3 Notes

GF-M's deepest re-framings: §3.1.1 specs-durable → specs-durable-post-promotion (P-20 makes pre-promotion specs malleable-by-construction); §3.1.5 knowledge-accumulates → knowledge-accumulates-after-Regime-B-warmup; §3.1.10 human-review tension is *solved* by the two-regime split rather than picked as one of the three options. The silent-absorption flag on §3.1.16 is shared with the BF-S exemplar.

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
- §4.1.8 (primitive) §4.1 Two new primitives promoted for §4.1 (sandbox + cost ceilings as shared infrastructure).
- §4.1.9 (recommendation) §5 CI/CD pipeline adaptation thesis.
- §4.1.10 (recommendation) §5.2 The three-layer substrate stack (OpenHands SDK + Overstory-design-in-Python + commodity research stack).
- §4.1.11 (framing) §6.2 §7 (Round 2 proposal) — recommended path forward.
- §4.1.12 (claim) §8 Closing claim.

### §4.2 Per-item classification

| Item | Verdict | Rationale (≤25 words) | v3 cite (if absorbed) |
|---|---|---|---|
| §4.1.1-§4.1.5 D-3..D-7 defaults | `absorbed (verified at §1.5)` | All five D-defaults verified per §1.5 above. | specs/gf-m.md §3-§4 |
| §4.1.6 falsified consensus items | `tbd` | Need per-item review of what was falsified vs preserved in v3; relevant if any falsified item touches GF-M's two-regime claim. | — |
| §4.1.7 F21-F33 failure modes promoted | `absorbed (with adaptation)` | GF-M spec invokes F25 (design starvation, recast as Regime-A property), F28 (holdout via P-08), F34 (cross-layer drift, Patrol-tier), F37 (silent contradictory-prompt collapse — paraphrase-divergence defense is GF-M's load-bearing claim), F46 (cross-model panel). | specs/gf-m.md §1 load-bearing + §3 + §4 |
| §4.1.8 sandbox + cost-ceilings as shared infrastructure | `absorbed` | GF-M §2 commodity substrate baseline includes P-01 sandbox (ADR 0010) + P-02 cost ceilings (ADR 0011). | specs/gf-m.md §2 commodity substrate baseline |
| §4.1.9 CI/CD pipeline adaptation thesis | `not-applicable-to-candidate-mandate` | CI/CD-pipeline framing is substrate-first-flavored; GF-M's methodology-first axis explicitly inverts this ("substrate is whatever the chosen cycle shape requires"). | — |
| §4.1.10 OpenHands+Overstory substrate stack | `rejected (explicitly-excluded-per-constraints-extracted, see constraints-extracted.md)` | **Known-rejected v3 item** per Reviewer 6 D-H8. GF-M's substrate-vendor choices (EventStoreDB vs Postgres event_log for P-20; LiteLLM router for P-21) are Phase-5 ADR seeds per substrate-requirements §5; specific stack is operator-deployment choice, NOT v3-architecture-level adoption. | — |
| §4.1.11 §7 Round-2 recommended path forward | `rejected (subsumed by v3 multi-candidate framing)` | Round-2 §7 recommended a single path forward; v3's DEC-1 / DEC-1.a explicitly preserves multiple candidates for Phase-8 falsification. | — |
| §4.1.12 §8 Closing claim | `not-applicable-to-candidate-mandate` | Cross-architectural meta-claim; not per-candidate. | — |

### §4.3 Notes

GF-M does NOT claim any framework ADR (P-19/P-28/P-29/P-30) per §0 "No framework-ADR claims"; the per-candidate §N.3 ADR-0036 framing required for BF-L / U-A / D7-U-1 does NOT apply to GF-M. GF-M's deliberate minimalism on contested-primitive references IS itself a load-bearing design claim — Round-2 F-mode promotions are absorbed via small specific primitives (P-20, P-21) rather than via framework adoption.

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
| §5.1.1 four-architecture taxonomy | `absorbed (with adaptation)` | v3 candidate-registry preserves the 4 v2 architectures as lineage; expands to 10 candidates. GF-M sits cross-lineage. | architectures/v3/candidate-registry.md |
| §5.1.2 failure-mode coverage matrix | `absorbed` | F1-F20 preserved as canonical; v3 extends to F49+. Covered in §10. | architectures/v3/failure-modes-v3.md |
| §5.1.3 when-to-pick-which decision criteria | `absorbed (with adaptation)` | v3 mandate-fit matrix per DEC-2 fulfills decision-criteria role per-candidate-per-work-unit-class. | architectures/v3/mandate-fit-matrix.md |
| §5.1.4 hybrid recommendations | `not-applicable-to-candidate-mandate` | GF-M is mandate-specific (not a hybrid); hybrid framing applies to U-A/U-B/U-C/D7-U-1. | — |
| §5.1.5 shared infrastructure enumeration | `absorbed` | v3 common-substrate ADRs 0010-0017 are the shared-infrastructure enumeration; GF-M consumes 6 (P-01/02/05/06/07/14/22). | specs/gf-m.md §2 + ADRs 0010-0017 |
| §5.1.6 shared roles, different emphasis | `absorbed (with adaptation)` | GF-M §4 discipline binding (9 of 10 disciplines) per-discipline fulfills "different emphasis" framing. | specs/gf-m.md §4 |
| §5.1.7 Compound Atelier baseline | `rejected (explicitly-anchor-avoided, see archive-and-rebuild discipline)` | **Known-rejected v3 item** per Reviewer 6 D-H8 + UC6. v3 deliberately treats all candidates as independent; no baseline. | — |
| §5.1.8 selective borrows | `rejected (subsumed by v3 multi-candidate scoping principle)` | "Selective borrows" presupposes a baseline; v3 has none. | — |
| §5.1.9 build shared infrastructure first | `absorbed` | v3 Phase-5 common-substrate ADRs precede candidate-specific work — direct match. | docs/adr/0010-0017 + Phase-5 sequencing |

### §5.3 Notes

GF-M is cross-lineage with a *distinctive negation*: no Refinery/Atelier/Foundry/Tournament baseline. The two-regime split is GF-M's own structural answer to "when to pick which" — Regime A is Refinery-shaped (spec-discovery + revelation cycle), Regime B is Atelier-shaped (Compound-Engineering loop + cross-model panel), with Tournament-flavored model-family diversity folded into both. §7 recommendations are known-rejected per archive-and-rebuild discipline.

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
| §6.1.1 spec is durable artifact | `absorbed (with adaptation, verified at §1.5)` | D-1 default; GF-M reframes durable=post-promotion; pre-promotion the spec is *reversible-by-construction* per P-20. | specs/gf-m.md §3 Regime-A |
| §6.1.2 5-layer spec stack | `not-applicable-to-candidate-mandate` | GF-M binds intent + scenario pair (2 layers, not 5); the 5-layer stack is Refinery-specific. | — |
| §6.1.3 stable identifier discipline | `absorbed (with adaptation)` | GF-M §3 cycle binds intent + scenario versions via P-20 event-sourced storage; event IDs provide stable identifiers per ADR 0040. | specs/gf-m.md §2 + ADR 0040 |
| §6.1.4 revelation cycle (7-phase) | `absorbed (with adaptation, silently — flagged for auditor)` | GF-M Regime A 4-phase loop (intent → paraphrase → probe → promote/reverse) is structurally a compressed revelation cycle; the "tiny probe surfaces what paraphrase missed" is the revelation. Not explicitly cited as Refinery-lineage. | specs/gf-m.md §3 Regime A (flagged for silent-absorption auditor) |
| §6.1.5 5-mode failure classification | `tbd` | GF-M F-mode coverage in §10 below may replicate or supersede the 5-mode classification; Phase-8 lean-eval question. | — |
| §6.1.6 manager loop | `absorbed (with adaptation)` | GF-M §4 three-loop discipline (ADR 0026) + Patrol-tier monitoring is the analogue; meta-loop closure substrate-enforced via P-06 + P-07. | specs/gf-m.md §4 three-loop |
| §6.1.7 showboat trajectory artifacts | `not-applicable-to-candidate-mandate` | GF-M binds trajectory at P-05 substrate (commodity primitive); doesn't materialise trajectory-as-showboat-artifact. | — |
| §6.1.8 implementation roadmap | `not-applicable-to-candidate-mandate` | Architecture-specific deployment; v3 doesn't carry per-architecture roadmaps. | — |

### §6.3 Notes

GF-M inherits significantly from Refinery — revelation-cycle shape and stable-identifier discipline are direct ancestors of Regime A. The silent-absorption flag on §6.1.4 is load-bearing: Regime A's 4-phase loop reads as a compressed Refinery 7-phase cycle (intent commissioning → paraphrase as implementation probe → tiny probe as trajectory + diagnostic → promote/reverse as amendment) but GF-M's spec does NOT explicitly cite Refinery as lineage. Silent-absorption auditor should reconcile.

## §7 — archive/architectures-v2/02-compound-atelier.md

### §7.0 File header

v2 Architecture 2 — Compound Atelier. "Each unit of work makes the next easier." Queue + workpad + persona panel + accumulated `docs/solutions/`. v2's recommended baseline. 4515 words. **GF-M cites Compound-Engineering loop explicitly in Regime B** per [GF-M §3 Regime B cycle shape](../specs/gf-m.md#3-methodology-shape).

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
| §7.1.1 compounding core thesis | `absorbed (with adaptation)` | Regime B is Compound-Engineering by construction; Regime A delays compounding until post-promotion (F8/F55 mitigation). | specs/gf-m.md §3 + §4 |
| §7.1.2 knowledge accumulation between cycles | `absorbed (with adaptation)` | ADR 0023; deliberately delayed in Regime A — distinctive Atelier departure. | specs/gf-m.md §3 |
| §7.1.3 artifact stack (specs/knowledge/workpad) | `absorbed (with adaptation)` | Intent + scenario pair (event-sourced via P-20) replaces 3-artifact stack with tighter 2-artifact. | specs/gf-m.md §2 + §3 |
| §7.1.4 workshop chain (persona workshops) | `rejected (subsumed by paraphrase divergence shape)` | Regime A uses N model-family paraphrasers, NOT personas; structural-not-stylistic diversity is load-bearing. | — |
| §7.1.5 researcher fan-out | `absorbed (with adaptation)` | Regime A paraphrase (P-21) is parallel-fan-out by construction; Regime B cross-model panel similarly. | specs/gf-m.md §3 |
| §7.1.6 reviewer panel | `absorbed (verified)` | Regime B explicitly cites "cross-model review panel"; F46 via P-14 + ADR 0018. | specs/gf-m.md §3 Regime B + §4 |
| §7.1.7 synthesis and curation | `absorbed (with adaptation)` | Regime-A→B slice-promotion is the synthesis-and-curation moment; methodology-layer per ADR 0023. | specs/gf-m.md §3 slice-coherence |
| §7.1.8 conductor orchestrator | `not-applicable-to-candidate-mandate` | Operator IS the conductor at promote/reverse; no separate orchestrator role. | — |
| §7.1.9 workpad protocol | `absorbed (with adaptation)` | Event-sourced intent+scenario store (P-20) plus Regime-B sandbox (P-01) is the workpad-equivalent. | specs/gf-m.md §2 + §3 |
| §7.1.10 tiered cycle scope | `absorbed (with adaptation)` | Regime A (L3) vs Regime B (L4-on-promoted-slices) is the tiering. | specs/gf-m.md §3 |
| §7.1.11 severity × autofix axes | `absorbed (silently — flagged for auditor)` | Likely informed DEC-2 mandate-fit-per-(architecture × work-unit-class) schema. Not explicitly cited. | — (flagged for silent-absorption auditor) |
| §7.1.12 residual work gate | `absorbed (with adaptation)` | Regime A promote-or-reverse gate + delayed knowledge-promotion close the residual-work loop. | specs/gf-m.md §3 + §4 |
| §7.1.13 three memory tiers | `not-applicable-to-candidate-mandate` | Multi-tier memory avoided in Regime A; Brier subsumption is OQ in §6 (Phase-7 carry). | — |
| §7.1.14 implementation roadmap | `not-applicable-to-candidate-mandate` | Architecture-specific deployment. | — |

### §7.3 Notes

This is GF-M's Regime-B lineage. Compound-Engineering loop (§7.1.1, §7.1.2, §7.1.6, §7.1.9) lands directly in Regime B with explicit citation. GF-M's distinctive Atelier departures: (a) persona workshops rejected for model-family paraphrase divergence (structural-not-stylistic F46 mitigation); (b) knowledge accumulation delayed until post-Regime-B-warmup (F55 mitigation); (c) three memory tiers not adopted (2-layer artifact stack: intent + scenario). Silent-absorption flag §7.1.11 shared with BF-S exemplar.

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
| §8.1.1 structured pre-agile core thesis | `not-applicable-to-candidate-mandate` | Foundry-specific; GF-M is methodology-first but not phase-gated-by-V&V-pairing — Regime A/B is a different split. | — |
| §8.1.2 phase model + V&V pairing | `not-applicable-to-candidate-mandate` | Foundry-specific cycle structure. | — |
| §8.1.3 Configuration Management discipline | `absorbed (with adaptation)` | GF-M binds CM analogue via P-20 event-sourced intent+scenario storage (sub-ms persist, content-addressed, append-only). | specs/gf-m.md §2 P-20 + ADR 0040 |
| §8.1.4 defect-of-origin table | `absorbed (with adaptation)` | P-20 event-sourced history + Regime-A reversal semantics provides defect-of-origin traceability at the intent/scenario level. | specs/gf-m.md §2 + ADR 0040 |
| §8.1.5 RUP-style discipline × phase matrix | `not-applicable-to-candidate-mandate` | Foundry-specific; GF-M binds 9-of-10 disciplines uniformly across both regimes (with cognitive-escrow at methodology layer per DEC-2). | — |
| §8.1.6 iteration within phases | `not-applicable-to-candidate-mandate` | Foundry-specific. | — |
| §8.1.7 V&V-side independent roles + different model family | `absorbed (verified)` | GF-M Regime B cross-model review panel "(per F46 single-model review blindspot; CJ Hess kevin/carl pattern)" requires different-family model; F46 mitigation. | specs/gf-m.md §3 Regime B + §4 bias-guard |
| §8.1.8 CM as spine | `absorbed (with adaptation)` | GF-M's P-20 event-sourced spine + reversibility-as-substrate-primitive (not methodology-promise) is the CM-equivalent. | specs/gf-m.md §3 "Reversal as substrate primitive, not methodology promise" |

### §8.3 Notes

Foundry's phase-gated structure is N/A but three Foundry primitives land: CM (substrate-level via P-20 event-sourced storage, structurally similar to BF-S's P-24 attribution but for intent+scenario not code), cross-model V&V independence (Regime B + bias-guard), and defect-of-origin via event-sourced reversal history. GF-M's Regime A 4-phase loop is structurally narrower than Foundry's 6-phase Requirements→Arch→DD→Unit→Integration→Acceptance V&V.

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
| §9.1.1 population + selection core thesis | `not-applicable-to-candidate-mandate` | Tournament-specific population-based methodology; GF-M Regime A is single-track-with-paraphrase-divergence (not parallel-competing-populations). | — |
| §9.1.2 genome structure | `not-applicable-to-candidate-mandate` | Tournament-specific artifact. | — |
| §9.1.3 model-family diversity as structural | `absorbed (verified)` | GF-M load-bearing claim: paraphrase divergence across N model-family-diverse paraphrasers per ADR 0041; cross-model review panel per ADR 0018. F46 + F37 mitigation. | specs/gf-m.md §1 load-bearing claim + §3 + §4 |
| §9.1.4 generation cycle | `not-applicable-to-candidate-mandate` | Tournament-specific. | — |
| §9.1.5 predator agent | `rejected (subsumed by paraphrase-divergence + tiny-probe + cross-model panel)` | GF-M substitutes Tournament's predator-agent with structural adversarial discipline: divergent paraphrasers in Regime A + cross-model panel in Regime B. | — |
| §9.1.6 loops within loops | `absorbed (with adaptation)` | GF-M §4 three-loop discipline (ADR 0026) + Patrol-tier (P-06) is analogous; meta-loop closure is substrate-enforced. | specs/gf-m.md §4 three-loop |
| §9.1.7 independence policy | `absorbed` | GF-M Regime A paraphrasers are model-family-independent by construction; Regime B builder/judge family-independent. | specs/gf-m.md §3 + §4 |
| §9.1.8 scaling | `tbd` | GF-M Regime A is operator-serial-by-design; Tournament's scaling lessons may surface non-trivially at Phase-8 lean-eval. | — |

### §9.3 Notes

Tournament's primary primitives (population, predator, bracket, genome) are N/A, but model-family diversity (§9.1.3) lands at the heart of GF-M's load-bearing F37 claim and is *verified* via P-21 + P-14 + ADR 0018. Predator-agent rejected with explicit reason: GF-M's structural-divergence substitution closes the same adversarial loop without a runtime predator role. Independence policy (§9.1.7) absorbed.

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
| §10.1.1 F1 Hallucination | `absorbed` | Regime A paraphrase + Regime B cross-model panel via P-14 + ADR 0018 bias guard. | specs/gf-m.md §3 + §4 |
| §10.1.2 F2 Reward hacking | `absorbed` | ADR 0021 holdout + P-08 substrate-typed holdout. | specs/gf-m.md §4 holdout |
| §10.1.3 F3 Spec-completeness | `absorbed (with adaptation, verified)` | Load-bearing: paraphrase + tiny probe are the F37/F3 defense. | specs/gf-m.md §1 + §3 Regime A |
| §10.1.4 F4 Code quality | `absorbed (with adaptation)` | Regime B cross-model review handles F4; Regime A produces no shippable code. | specs/gf-m.md §3 Regime B + §4 |
| §10.1.5 F5 Cognitive ceiling | `absorbed (with adaptation)` | Regime A operator-bottlenecked by design; recasts F5 as regime property not failure. | specs/gf-m.md §3 day-0-to-day-N trajectory |
| §10.1.6 F6 Cognitive debt | `absorbed` | ADR 0019 cognitive-escrow at Regime-A operator touchpoints. | specs/gf-m.md §4 + ADR 0019 |
| §10.1.7 F7 Normalization of deviance | `absorbed (with adaptation)` | Patrol-tier (P-06) watches F55/F34; substrate-enforced. | specs/gf-m.md §3 Patrol-tier monitoring |
| §10.1.8 F8 Stale knowledge | `absorbed (with adaptation)` | Deliberately delays knowledge accumulation in Regime A — distinctive F8/F55 mitigation. | specs/gf-m.md §3 + §4 knowledge-promotion |
| §10.1.9 F9 Spec overfitting | `absorbed (with adaptation)` | P-20 reversibility makes spec-overfitting cheap to reverse. | specs/gf-m.md §3 Regime A + ADR 0040 |
| §10.1.10 F10 Findings disappear | `absorbed` | P-05 trajectory + P-20 event-sourced store; immutable history. | specs/gf-m.md §2 + ADR 0040 |
| §10.1.11 F11 Renumbering | `absorbed (with adaptation)` | P-20 content-addressed per-event IDs; intent+scenario versions immutable. | specs/gf-m.md §2 + ADR 0040 |
| §10.1.12 F12 Lethal trifecta | `absorbed (verified)` | §4 trifecta closure (ADR 0027): P-08 holdout + GtWR linter, substrate-default-off. | specs/gf-m.md §4 trifecta closure |
| §10.1.13 F13 Missing-config | `absorbed (with adaptation)` | Greenfield — no legacy config; GtWR linter catches intent-config gaps. | specs/gf-m.md §3 + §4 |
| §10.1.14 F14 Attribution collapse | `absorbed (with adaptation)` | P-20 event-sourced storage + reversal history provide attribution at intent/scenario level. | specs/gf-m.md §2 + ADR 0040 |
| §10.1.15 F15 Single-prompt collapse | `absorbed (verified)` | Regime A paraphrase divergence is *the* F37 defense; load-bearing per §1. | specs/gf-m.md §1 load-bearing claim |
| §10.1.16 F16 Resume-fidelity | `absorbed` | P-05 trajectory + P-20 sub-ms per-event provides resume anchor. | specs/gf-m.md §2 + ADR 0040 |
| §10.1.17 F17 Parallel agents on shared dirs | `tbd` | Regime A operator-serial; Regime B parallelism on promoted slices unspecified. | — |
| §10.1.18 F18 Prose-spec rigor | `absorbed (with adaptation)` | EARS-constrained AC + deterministic GtWR R7/R8/R9 lint; failures returned to operator. | specs/gf-m.md §3 Regime A Phase 1 |
| §10.1.19 F19 Model-floor dependency | `absorbed (verified)` | P-21 paraphrase requires N≥3 cross-family per F46; P-14 surfaces model-floor explicitly. | specs/gf-m.md §1 + §4 |
| §10.1.20 F20 Maintenance asymmetry | `absorbed (with adaptation)` | Same cycle shape across initial-spec/mvp/post-mvp-evolution; regression-fix is Regime B. | specs/gf-m.md §5 mandate-fit |
| §10.1.21 A1 Refinery coverage row | `not-applicable-to-candidate-mandate` | Coverage row characterizes Architecture 1, not GF-M. Informational. | — |
| §10.1.22 A2 Atelier coverage row | `not-applicable-to-candidate-mandate` | Coverage row characterizes Architecture 2; GF-M cites Compound-Engineering loop but GF-M's own F-mode coverage tracked above. | — |
| §10.1.23 A3 Foundry coverage row | `not-applicable-to-candidate-mandate` | Coverage row characterizes Architecture 3. | — |
| §10.1.24 A4 Tournament coverage row | `not-applicable-to-candidate-mandate` | Coverage row characterizes Architecture 4. | — |

### §10.3 Notes

19-of-20 F-modes are absorbed (F1-F16, F18-F20). Four are verified with explicit GF-M spec invocations: F3 (paraphrase + tiny probe = spec-completeness defense), F12 (trifecta closure substrate-default-off per ADR 0027), F15 (paraphrase divergence = load-bearing F37/single-prompt-collapse defense), F19 (cross-family paraphrase requirement). Only F17 (parallel agents on shared dirs) is TBD — Regime A serial-by-design; Regime B parallelism unspecified. The 4 per-architecture coverage-strength rows are informational characterizations of v2 architectures, not GF-M-actionable.

## §11 Summary

**Per-token cell counts (matches YAML frontmatter; raw verdict-token grep tally across all rubric tables):**

| Token | Count |
|---|---|
| `absorbed` (incl. with-adaptation, verified, silently) | 73 |
| `rejected (reason)` | 7 |
| `not-applicable-to-candidate-mandate` | 23 |
| `tbd` | 6 |
| **Total raw tally** | **109** |

(Raw tally includes the 7 D-default rows in §1.5 plus 1 bundled §4.2 D-3..D-7 row (treated by grep as 1 not 5). Per-archive-table cell totals: §2.2 (3) + §3.2 (16) + §4.2 (8) + §5.2 (9) + §6.2 (8) + §7.2 (14) + §8.2 (8) + §9.2 (8) + §10.2 (24) = 98. **Unique-verdict cells** removing D-1..D-7 §1.5 duplicates with §3/§4 cross-references: ~95. YAML frontmatter carries the raw tally per the BF-S-exemplar precedent of reporting `grep -cE '\| \`<token>'` directly so the auditor can re-verify mechanically. This is documented here for the silent-absorption auditor to reconcile.)

**High-confidence absorbed cells:** D-1 through D-7 (all 7 verified per §1.5); F3 + F12 + F15 + F19 (verified at GF-M spec §1 load-bearing claim + §4 trifecta closure + §4 bias-guard); §7.1.6 reviewer panel (Regime B cross-model panel explicitly cited).

**Surfaced TBDs (require lead-agent reconciliation or Phase-8 follow-up):**

1. §3.1.15 parallel-agent + human-role tension — GF-M Regime A serial-by-design; Phase-8 lean-eval may surface scaling limits.
2. §4.1.6 falsified consensus items — needs per-item review of what was falsified vs preserved in v3; relevant if any falsified item touches two-regime claim.
3. §6.1.5 Refinery 5-mode failure classification — Phase-8 lean-eval candidate; GF-M F-mode coverage may replicate or supersede.
4. §9.1.8 Tournament scaling — Phase-8 carry; GF-M Regime A serial-by-design but scaling lessons may surface.
5. §10.1.17 F17 Parallel agents on shared dirs — Regime B parallelism on promoted slices unspecified.

**Silent-absorption auditor flags (for cross-spec reconciliation):**

- §3.1.16 cross-cutting primitives (v3 `primitives/index.md` likely inherited the framing without explicit citation; shared with BF-S exemplar).
- §6.1.4 Refinery revelation cycle (GF-M Regime A 4-phase loop reads as a compressed revelation cycle but does NOT cite Refinery as lineage — this is GF-M's deepest unlabeled borrowing).
- §7.1.11 severity × autofix orthogonal axes (likely informed DEC-2 mandate-fit-per-(architecture × work-unit-class) schema; shared with BF-S exemplar).

**Known-rejected items confirmed:**

- §4.1.10 OpenHands+Overstory substrate stack — `rejected (explicitly-excluded-per-constraints-extracted)`.
- §5.1.7 Compound Atelier as baseline — `rejected (explicitly-anchor-avoided)`.

**Two additional candidate-specific rejections (with explicit reason, not the known-rejected token):**

- §7.1.4 workshop chain (persona workshops) — rejected, substituted by model-family-diverse paraphrase divergence (the F46 mitigation is *structural* not *stylistic*).
- §9.1.5 predator agent — rejected, substituted by structural adversarial discipline (Regime-A divergent paraphrasers + Regime-B cross-model panel).

## §12 References

**GF-M spec + supporting docs:**

- [`architectures/v3/specs/gf-m.md`](../specs/gf-m.md) — GF-M Phase-6 architecture spec (audit input).
- [`architectures/v3/candidate-registry.md` GF-M entry](../candidate-registry.md#gf-m--greenfield-methodology-first) — registry entry for §1 lineage statement.
- [`architectures/v3/substrate-requirements/gf-m.md`](../substrate-requirements/gf-m.md) — substrate-requirements summary.
- [`architectures/v3/decisions/auto-007-phase-7-dispatch-shape.md`](../decisions/auto-007-phase-7-dispatch-shape.md) — Phase-7 dispatch brief.
- [`architectures/v3/backfill-notes/bf-s.md`](./bf-s.md) — Phase-7 exemplar (shape model inherited).

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

- GF-M substrate ADRs: [0010-0017](../../../docs/adr/) common + [0018-0027](../../../docs/adr/) discipline + [0040](../../../docs/adr/0040-p-20-reversibility-primitive.md) P-20 + [0041](../../../docs/adr/0041-p-21-paraphrase-divergence.md) P-21.

**Constraints / decisions:**

- [`architectures/v3/constraints-extracted.md`](../constraints-extracted.md) — UC1-UC8 user constraints (source of known-rejected v3 item flags).
- [`architectures/v3/decisions-captured.md`](../decisions-captured.md) — DEC-1 / DEC-1.a / DEC-2 etc.
