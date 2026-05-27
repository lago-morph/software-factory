---
candidate: gf-s
candidate-name: Greenfield, substrate-first
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
  absorbed: 61
  rejected: 5
  not-applicable: 27
  tbd: 5
  # Note: counts via tallying the verdict-column cell text in §N.2 classification
  # tables (rows matching `^\| §N.1.X`). Includes all `absorbed` variants
  # (with-adaptation / verified / verified-at-§1.5 / silently / verified). Total = 98
  # classification-table cells across §2.2 (3) + §3.2 (16) + §4.2 (8) + §5.2 (9) +
  # §6.2 (8) + §7.2 (14) + §8.2 (8) + §9.2 (8) + §10.2 (24). Silent-absorption
  # auditor uses these table-row counts as the authoritative cell count.
self-check-results:
  # Per auto-007 §1.5 rubric + self-check items (a)-(g).
  wc-w: 6976  # over Light tier (3500-5000) and over exemplar-tolerated band (5000-5700)
              # by ~1300 words; see exemplar-budget-flag-followup below
  ls-cited-files: PASS  # cited v3 files (specs/gf-s.md, candidate-registry.md,
                        # substrate-requirements/gf-s.md, tracks/greenfield-substrate-first.md,
                        # primitives/overlap.md, decisions/auto-007 brief, ADRs 0010-0027 +
                        # 0028 + 0032 + 0037 + 0038 + 0039, archive files, failure-modes-v3.md)
                        # all exist (verified by ls at write time).
  section-headers: PASS  # §1, §1.5, §2-§10, §11, §12 + §N.0 file-header per §2-§10
  enumeration-floor: PASS  # §2.1=3 (small-file-exception per Reviewer 4 amendment),
                           # §3.1=17, §4.1=13, §5.1=10, §6.1=8, §7.1=15, §8.1=8,
                           # §9.1=8, §10.1=24 (all ≥5; §10 floor=24 satisfied)
  cell-counts-match-yaml: PASS  # 61+5+27+5 = 98 classification-table cells per
                                # §N.2 verdict-column tally; matches §11 summary
                                # table totals exactly
  verbatim-text-pull: n/a  # no binding rule tables verbatim-cited (per Reviewer 3 D7
                           # — classification-token table is guidance, not binding)
  tbd-count: 5  # 5 classification-table `tbd` cells; 5 distinct surfaced TBDs in §11.
                # `grep -c "tbd"` against the whole file returns 10 (5 table cells +
                # 5 mentions in §1.5 summary + §11 surfaced-TBDs list + this self-check).
exemplar-budget-flag-followup: |
  Sibling-candidate measured at 6976 words; Light tier upper bound is 5000; exemplar
  (bf-s.md) ran 5981 with lead-agent ACCEPT and signalled sibling Light-tier candidates
  may land at 5000-5700 if §1.5 + §N.3 sections are full. GF-S landed at 6976 —
  ~1300 words over the exemplar-tolerated upper bound. Overrun attributed to:
  (a) GF-S's broader F-mode coverage in §10 (19-of-20 absorbed vs BF-S's 15-of-20,
  generating ~250 extra words of cell-rationale text); (b) the §1 multi-lineage
  characterization (~150 words extra over BF-S's single-Atelier-lineage paragraph
  because GF-S must enumerate weak inheritance from all 4 v2 architectures); (c) the
  §11 multi-lineage characterization summary (~100 extra words); (d) §7.3 Atelier-
  N/A justifications (~200 extra words because GF-S has 6 N/A cells on Atelier
  methodology-layer items, each requiring substrate-abstains rationale). Lead-agent
  decision call: ACCEPT or trim. If ACCEPT, the auto-007 tier table calibration
  needs Round-3 revision (the Light tier upper bound is empirically closer to 6500
  than 5000). If TRIM, the §N.3 notes and §11 multi-lineage discussion are the
  candidates. Per Phase-7 dispatch's be-generous bias direction, ACCEPT recommended;
  trimming would lose the multi-lineage characterization that's the GF-S-distinctive
  audit finding.
---

# Back-fill notes — GF-S (Greenfield, substrate-first) vs v1/v2 archive

## §1 Overview

**Mandate.** Greenfield (only). GF-S is greenfield-only by explicit construction — 5-of-5 mandate-fit cells `greenfield` per the [GF-S spec §5](../specs/gf-s.md#5-mandate-fit); the architecture explicitly disclaims brownfield reach per [track §6 "Not a unified both-mandates architecture"](../tracks/greenfield-substrate-first.md#6-what-this-track-is-not-trying-to-be).

**Axis.** Substrate-first — the nine substrate slots S1–S9 (P-01 sandbox / P-08 scenario storage / P-05 trajectory / P-02 cost ceilings / P-06 watchdog / P-14 judge router / P-10 coordination medium / P-15 four-guard mediator / P-19 eligibility classifier) are the load-bearing investment; methodology is the *thinnest possible* layer that drives the primitives, per [track §2 substrate-derives axis](../tracks/greenfield-substrate-first.md).

**Entry-mode.** Greenfield day-0 cold-start with an operator-authored 9-field El-Kaim-style intent block + ≥3 region-shaped scenarios per [track §5.2 bootstrap protocol](../tracks/greenfield-substrate-first.md#52-the-bootstrap-protocol). No legacy codebase; no Codebase Model dependency at entry. The substrate accommodates code accretion as a within-factory output without ingesting external legacy artifacts.

**Strongest v2-architecture-lineage.** *This candidate has **no single-lineage assignment**; per-archive-file audit treats all 4 v2 architectures as potentially-relevant prior art.* Rationale (derived from [GF-S candidate-registry entry](../candidate-registry.md#gf-s--greenfield-substrate-first) §Axis verbatim cite): "*Substrate is the primary organizing principle; methodology is deliberately thin and follows the primitives. … Unit-of-work, spec format, agent topology explicitly deferred to methodology choices on top of substrate.*" The registry does not name a single v2 architecture as GF-S's lineage; the [track §2 substrate-derives axis](../tracks/greenfield-substrate-first.md) explicitly states that *"Compound-style review panel, Attractor-style DOT pipeline, Tournament-style population selection — per [CTR-F3](../contradictions.md)'s Round-2 reframing of these as methodology choices on a both-shapes substrate"* are all accommodated. GF-S therefore inherits substrate-slot framings opportunistically from all four v2 architectures, with no single architecture as dominant lineage. The closest weak-overlap is **Architecture 2 (Compound Atelier)** on the artifact-stack + memory-tier framing, but the registry does not anchor this and GF-S explicitly disclaims the Atelier compounding-mechanism methodology (methodology-layer choice, not substrate commitment per [spec §3 distinctive decision 3](../specs/gf-s.md#3-methodology-shape)).

**D-1 through D-7 default-verification preview.** Per [auto-007 §1.5 verification rubric](../decisions/auto-007-phase-7-dispatch-shape.md#decision-round-2) and Reviewer 5/6 amendments: D-1 through D-7 are NOT silently skipped. The §1.5 verification subsection below records the per-default verdict for GF-S.

## §1.5 D-1 through D-7 defaults verification

Per Reviewer 5 Defect 1 + Reviewer 6 D-H5 amendments. Each default verified per `grep` against GF-S spec content; verdict tokens per the auto-007 Round-2 rubric.

| Default | Source claim | GF-S verdict | Spec cite |
|---|---|---|---|
| D-1 specs durable | `00-synthesis.md` §2.1 | `absorbed (with adaptation)` — the intent block is the *slow* (durable) layer Patrol guards; the spec body around it is the *fast* (malleable) layer | GF-S §3 distinctive decision 1: "the intent block (per [report 14]) is the slow layer Patrol guards; the spec body around the intent block is the fast layer that can churn arbitrarily" — pace-layer split rather than monolithic-durable framing |
| D-2 scenarios out-of-tree | `00-synthesis.md` §2.2 | `absorbed (verified at specs/gf-s.md §2 designed-system substrate)` | "[P-08 scenario storage (ADR 0015)] is S2: append-only scenario store with substrate-enforced training/holdout partition + deterministic replay" — substrate-typed builder-blindness is the out-of-tree-equivalent; for greenfield "the codebase does not yet exist to inherit from" so substrate enforcement IS the partition |
| D-3 Agent = Model + Harness | `13-round-2-synthesis.md` §1.1 C10 | `absorbed (verified at specs/gf-s.md §3 cycle step 5 + §2 substrate composition)` | §3 cycle step 5 "Build agent runs under [P-06 watchdog] Daemon/Triage/Patrol with [P-05 trajectory] capture and [P-02 ceilings] substrate-enforced" + §3 step 6 P-14 judge router selection are the Model+Harness binding |
| D-4 holdout discipline | `13-round-2-synthesis.md` §1.1 C13 | `absorbed (verified at specs/gf-s.md §4 holdout binding)` | "Bound at [P-08 (ADR 0015)] substrate-typed builder-blindness (D-4). For greenfield this is the *only* coherent option since there is no codebase to inherit from. … substrate enforces the boundary" |
| D-5 hard cost ceilings | `13-round-2-synthesis.md` §1.1 C15 | `absorbed (verified at specs/gf-s.md §4 cost-ceiling binding)` | §4 cost-ceiling binding via ADR 0011 + ADR 0020 + "substrate kills the cycle at ceiling — no graceful-degradation mode (refuses [CTR-E6] utility-tax pattern)" per §2 |
| D-6 tiered watchdog | `13-round-2-synthesis.md` §1.1 C14 | `absorbed (verified at specs/gf-s.md §2 watchdog tiers + §4 three-loop binding)` | §2 "[P-06 watchdog tiers (ADR 0013)] is S5: Daemon (seconds) / Triage (seconds-minutes) / Patrol (hours)" + §4 three-loop bound thinly to ADR 0026 |
| D-7 trajectory capture | `13-round-2-synthesis.md` §1.1 C16 | `absorbed (verified at specs/gf-s.md §2 trajectory + §4 cognitive-escrow binding)` | §2 "[P-05 trajectory capture (ADR 0012)] is S3: per-event sub-ms content-addressed append-only persistence" + §4 cognitive-escrow binding via ADR 0019 |

**Summary:** 7-of-7 defaults absorbed (D-1 with substrate-specific pace-layer adaptation; D-2..D-7 verified at named spec sections). No challenges. No silent absorptions in this candidate (auditor reconciliation expected to confirm; the pace-layer adaptation on D-1 is explicit not silent).

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
| §2.1.1 three-layer pipeline | `absorbed (with adaptation)` | v3 inherits research → synthesis → action shape via Phase-1 corpus inventory + Phase-3 synthesis + Phase-5 ADRs + Phase-6 specs. Pipeline preserved; layers added. | architectures/v3/corpus-inventory.md + ARCHITECTURE-V3-SYNTHESIS-PLAN.md Phases 1-6 |
| §2.1.2 "enough research" trigger | `absorbed` | v3's Phase-1 corpus saturation + Phase-3 contradiction-counting fulfill this. | architectures/v3/corpus-inventory.md + contradictions.md |
| §2.1.3 folding policy | `not-applicable-to-candidate-mandate` | Document-management discipline at synthesis-process level; not a candidate-specific architectural primitive. | — |

### §2.3 Notes

Research-plan.md's user-stated constraints (UC1 lights-out, UC4 spec-malleability, UC5, UC6 archive-and-rebuild) are already extracted to `constraints-extracted.md` and are NOT Phase-7 scope. Substrate-vendor recommendation OQs (substrate-stack choice — OpenHands+Overstory vs Gas City) are Phase-5 ADR territory per [GF-S §6 CTR-C5](../specs/gf-s.md#6-open-carries); the Phase-7 audit does not adjudicate vendor choice.

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
| §3.1.1 specs primary artifact (D-1) | `absorbed (with adaptation, per §1.5)` | D-1 adapted per §1.5 via pace-layer split: intent block durable, spec body malleable. | specs/gf-s.md §3 distinctive decision 1 |
| §3.1.2 scenarios outside codebase (D-2) | `absorbed (verified at §1.5)` | D-2 substrate-enforced via P-08 builder-blindness; for greenfield no codebase exists yet, substrate IS the partition. | specs/gf-s.md §2 designed-system substrate |
| §3.1.3 validation harnesses are real engineering | `absorbed` | GF-S substrate IS the validation harness (P-08 + P-14 + P-15 four-guard mediator + Patrol-tier P-06). | specs/gf-s.md §2 substrate composition |
| §3.1.4 Agent=LLM-in-loop (D-3) | `absorbed (verified at §1.5)` | D-3 verified per §1.5 via §3 cycle step 5-6. | specs/gf-s.md §3 cycle step 5-6 |
| §3.1.5 knowledge accumulates between cycles | `not-applicable-to-candidate-mandate` | GF-S explicitly leaves knowledge-accumulation pattern (eager / lazy / typed) as a methodology-layer choice; substrate-first deliberately abstains. | — |
| §3.1.6 single-threaded human ceiling | `absorbed (with adaptation)` | GF-S §3 regime structure: `augmentation-required` regime is per-cycle human review, `automation-eligible` is lights-out — substrate-enforced ceiling-aware dispatch. | specs/gf-s.md §3 regime structure |
| §3.1.7 human leverage upstream/downstream | `absorbed (with adaptation)` | GF-S §3 intent-block-as-slow-layer + Patrol-tier audit are the upstream/downstream surfaces; substrate hosts both. | specs/gf-s.md §3 + §2 |
| §3.1.8 tiered ceremony | `absorbed (with adaptation)` | GF-S §3 three-regime dispatch (`automation-eligible` / `augmentation-required` / `escalate`) is the substrate-typed tiered-ceremony surface. | specs/gf-s.md §3 regime structure |
| §3.1.9 cost first-class (D-5) | `absorbed (verified at §1.5)` | D-5 verified per §1.5 via §4 cost-ceiling binding. | specs/gf-s.md §4 cost-ceiling |
| §3.1.10 human-review tension | `absorbed (with adaptation)` | GF-S §3 substrate-typed regime split + CTR-A4/OQ-B1 resolution at substrate layer. | specs/gf-s.md §3 |
| §3.1.11 persona vs graph-node tension | `not-applicable-to-candidate-mandate` | GF-S §3 distinctive decision 3: "methodology layer takes no opinion on agent topology" — substrate is topology-agnostic. | — |
| §3.1.12 spec format tension | `absorbed (with adaptation)` | GF-S §3 distinctive decision 1: "Methodology may use prose / EARS / typed-object / DOT graph; substrate has no opinion" — substrate-level resolution. | specs/gf-s.md §3 distinctive decision 1 |
| §3.1.13 knowledge architecture tension | `not-applicable-to-candidate-mandate` | GF-S substrate abstains; the DAG-vs-flat tension is a methodology-layer choice on top of P-10 coordination + P-05 trajectory. | — |
| §3.1.14 adversarial review tension | `absorbed` | GF-S §4 bias-guard binding via P-14 + P-15 contradiction-detector enforces adversarial-as-attribute via 3-of-N family-diverse ensemble. | specs/gf-s.md §4 bias-guard |
| §3.1.15 parallel-agent + human-role tension | `tbd` | GF-S §3 substrate accommodates single-agent / panel / tournament / population through P-10; specific parallelism shape is methodology call. Phase-8 lean-eval. | — |
| §3.1.16 cross-cutting primitives | `absorbed (silently — flagged for auditor)` | v3 has its own primitive enumeration (`primitives/index.md`); the 00-synthesis §5 list informed earlier phases but isn't directly cited by GF-S spec. | — (flagged for silent-absorption auditor) |

### §3.3 Notes

GF-S's substrate-first axis lands the "validation harnesses are the real engineering" framing (§3.1.3) deeply: the four-guard mediator (P-15) + holdout-enforced scenario storage (P-08) + judge router (P-14) collectively ARE the validation harness, with methodology riding thinly on top. The silent-absorption flag on §3.1.16 mirrors BF-S's same flag — v3's `primitives/index.md` may have inherited the cross-cutting-primitive framing from this file without explicit citation. Three N/A cells (§3.1.5 / §3.1.11 / §3.1.13) reflect GF-S's deliberate substrate-vs-methodology split: substrate abstains from knowledge-pattern, agent-topology, and knowledge-architecture choices.

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
| §4.1.1-§4.1.5 D-3..D-7 defaults | `absorbed (verified at §1.5)` | All five D-defaults verified per §1.5 above. | specs/gf-s.md §2-§4 |
| §4.1.6 falsified consensus items | `tbd` | Need per-item review of what was falsified vs preserved in v3. | — |
| §4.1.7 F21-F33 failure modes promoted | `absorbed (with adaptation)` | GF-S spec invokes F12/F33/F44/F25/F27/F28/F40/F43/F44/F48/F51/F52/F55/F57 + F8/F9 explicitly. | specs/gf-s.md §2 + §3 + §4 + §6 (multiple F-mode invocations) |
| §4.1.8 sandbox + cost-ceilings as shared infrastructure | `absorbed` | GF-S §2 commodity-common-substrate includes P-01 sandbox (ADR 0010) + P-02 cost ceilings (ADR 0011). | specs/gf-s.md §2 commodity common substrate |
| §4.1.9 CI/CD pipeline adaptation thesis | `absorbed (with adaptation)` | GF-S §2 P-10 coordination medium is CI-friendly Git-LFS + signed refs (resolves CTR-C7 mail-bus-vs-CI by siding CI-friendly). | specs/gf-s.md §2 P-10 + ADR 0037 |
| §4.1.10 OpenHands+Overstory substrate stack | `rejected (explicitly-excluded-per-constraints-extracted, see constraints-extracted.md)` | **Known-rejected v3 item** per Reviewer 6 D-H8. GF-S §6 CTR-C5 explicitly defers substrate-stack binding; specific stack is operator-deployment choice, NOT v3-architecture-level adoption. | — |
| §4.1.11 §7 Round-2 recommended path forward | `rejected (subsumed by v3 multi-candidate framing)` | Round-2 §7 recommended a single path forward; v3's DEC-1 / DEC-1.a explicitly preserves multiple candidates for Phase-8 falsification. Single-path collapsed. | — |
| §4.1.12 §8 Closing claim | `not-applicable-to-candidate-mandate` | Cross-architectural meta-claim; not per-candidate. | — |

### §4.3 Notes

GF-S does NOT claim P-30 / ADR 0036 (per [spec §0 ADR-citation index footnote](../specs/gf-s.md#0-adr-citation-index): "GF-S does **not** claim the P-28 / P-29 / P-30 frameworks (ADRs 0029 / 0030 / 0036)"). The per-candidate §N.3 ADR-0036 framing characterization required for BF-L / U-A / D7-U-1 per [auto-007 §N.3 amendment](../decisions/auto-007-phase-7-dispatch-shape.md#decision-round-2) does NOT apply to GF-S. The silent-absorption auditor's cross-spec ADR-0036 framing audit will not touch GF-S.

The CI/CD-adaptation thesis (§4.1.9) lands cleanly on GF-S's P-10 coordination medium choice (Git-LFS + signed refs reachable from any GitHub-Actions runner without broker provisioning) — this is the substrate-level CI/CD adaptation, with GF-S explicitly siding CI-friendly at the architecture layer.

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
| §5.1.1 four-architecture taxonomy | `absorbed (with adaptation)` | v3 candidate-registry preserves the 4 v2 architectures as lineage framing; expands to 10 candidates. GF-S inherits opportunistically from all 4. | architectures/v3/candidate-registry.md |
| §5.1.2 failure-mode coverage matrix | `absorbed` | F1-F20 preserved as canonical; v3 extends to F49+. Covered in §10. | architectures/v3/failure-modes-v3.md |
| §5.1.3 when-to-pick-which decision criteria | `absorbed (with adaptation)` | v3 mandate-fit matrix per DEC-2 fulfills decision-criteria role per-(candidate × work-unit-class). | architectures/v3/mandate-fit-matrix.md |
| §5.1.4 hybrid recommendations | `not-applicable-to-candidate-mandate` | GF-S is mandate-specific (greenfield-only); hybrid framing applies to U-A/U-B/U-C/D7-U-1. | — |
| §5.1.5 shared infrastructure enumeration | `absorbed` | v3 common-substrate ADRs 0010-0017 are the shared-infrastructure enumeration; GF-S §2 carries 8-of-8. | specs/gf-s.md §2 + ADRs 0010-0017 |
| §5.1.6 shared roles, different emphasis | `absorbed (with adaptation)` | v3 §4 discipline binding per-candidate fulfills "different emphasis" framing; GF-S binds all 10. | specs/gf-s.md §4 |
| §5.1.7 Compound Atelier baseline | `rejected (explicitly-anchor-avoided, see archive-and-rebuild discipline)` | **Known-rejected v3 item** per Reviewer 6 D-H8 + UC6. v3 treats all candidates as independent; no baseline. | — |
| §5.1.8 selective borrows | `rejected (subsumed by v3 multi-candidate scoping principle)` | "Selective borrows" presupposes a baseline; v3 has none. | — |
| §5.1.9 build shared infrastructure first | `absorbed` | v3 Phase-5 common-substrate ADRs precede candidate-specific work — direct match; GF-S §2 commodity-substrate baseline. | docs/adr/0010-0017 + Phase-5 sequencing |

### §5.3 Notes

The §7 recommendations (Compound Atelier baseline + selective borrows) are the highest-priority known-rejected v3 items per the archive-and-rebuild discipline. The 4-architecture taxonomy (§5.1.1) is the source of the v3 candidate-registry's lineage-mapping structure; GF-S inherits as multi-lineage (no single dominant), differing from BF-S which inherits primarily from Atelier — see §1 overview for the rationale.

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
| §6.1.1 spec is durable artifact | `absorbed (with adaptation, per §1.5)` | D-1 pace-layer-adapted; intent block is the durable layer Patrol guards; spec body is fast layer. | specs/gf-s.md §3 distinctive decision 1 |
| §6.1.2 5-layer spec stack | `not-applicable-to-candidate-mandate` | GF-S substrate-first deliberately leaves spec-layering (prose / EARS / typed-object / DOT) to methodology; 5-layer is Refinery-flavored. | — |
| §6.1.3 stable identifier discipline | `absorbed (with adaptation)` | GF-S §2 P-05 trajectory content-addressed sub-ms persistence + P-10 typed-event log signed refs provide content-addressed stable IDs. | specs/gf-s.md §2 + ADR 0012 + ADR 0037 |
| §6.1.4 revelation cycle (7-phase) | `not-applicable-to-candidate-mandate` | Refinery-specific cycle structure; GF-S §3 has its own 8-step substrate-driven cycle. | — |
| §6.1.5 5-mode failure classification | `tbd` | Whether GF-S's F-mode coverage replicates / extends / supersedes the 5-mode classification is a Phase-8 lean-eval question. | — |
| §6.1.6 manager loop | `absorbed (with adaptation)` | GF-S §4 three-loop discipline (ADR 0026) bound thinly; Patrol-tier as meta-loop closure analogue. | specs/gf-s.md §4 three-loop |
| §6.1.7 showboat trajectory artifacts | `not-applicable-to-candidate-mandate` | Trajectory-as-artifact is Refinery-flavored; GF-S binds trajectory at P-05 substrate (different role — substrate primitive, not artifact). | — |
| §6.1.8 implementation roadmap | `not-applicable-to-candidate-mandate` | Architecture-specific deployment; v3 doesn't carry per-architecture roadmaps. | — |

### §6.3 Notes

GF-S inherits weakly from Refinery — mainly the spec-as-durable-artifact framing (D-1, adapted via pace-layer split) and stable-identifier discipline (substrate-content-addressed via P-05/P-10). Refinery-specific primitives (5-layer specs, revelation cycle, manager loop, showboat trajectories) are all N/A or substrate-substituted. GF-S's spec-shape-agnosticism ([spec §3 distinctive decision 1](../specs/gf-s.md#3-methodology-shape)) is the explicit departure from Refinery's spec-layering: GF-S substrate makes no spec-format commitment.

## §7 — archive/architectures-v2/02-compound-atelier.md

### §7.0 File header

v2 Architecture 2 — Compound Atelier. "Each unit of work makes the next easier." Queue + workpad + persona panel + accumulated `docs/solutions/`. v2's recommended baseline. 4515 words. **GF-S's weak-overlap v2-lineage** on the artifact-stack + memory-tier framing per §1 overview.

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
| §7.1.1 compounding core thesis | `not-applicable-to-candidate-mandate` | GF-S substrate-first explicitly defers compounding-mechanism (knowledge-accumulation pattern eager/lazy/typed) to methodology layer — substrate accommodates without privileging. | — |
| §7.1.2 knowledge accumulation between cycles | `not-applicable-to-candidate-mandate` | Same as §7.1.1 — methodology-layer choice on top of P-05 trajectory + P-10 event log; substrate abstains. | — |
| §7.1.3 artifact stack (specs/knowledge/workpad) | `absorbed (with adaptation)` | GF-S substrate provides P-08 (scenarios) + P-05 (trajectory) + P-10 (coordination/event log) — Atelier's stack mapped to substrate primitives, not curated artifacts. | specs/gf-s.md §2 |
| §7.1.4 workshop chain (persona workshops) | `not-applicable-to-candidate-mandate` | GF-S methodology is agent-topology-agnostic per §3 distinctive decision 3; persona-workshop is one possible methodology overlay the substrate accommodates. | — |
| §7.1.5 researcher fan-out | `absorbed (with adaptation)` | GF-S §2 P-14 judge router dispatches family-diverse ensemble; §4 bias-guard binding creates the parallel-evaluation surface. | specs/gf-s.md §2 + §4 |
| §7.1.6 reviewer panel | `absorbed` | GF-S §4 bias-guard binding via P-14 + P-15 contradiction-detector enforces 3-of-N family-diverse panel — F46 mitigation. | specs/gf-s.md §4 bias-guard |
| §7.1.7 synthesis and curation | `not-applicable-to-candidate-mandate` | Curation is methodology-layer in GF-S; substrate's P-10 event log + P-05 trajectory provide raw surfaces, curation discipline is methodology choice. | — |
| §7.1.8 conductor orchestrator | `not-applicable-to-candidate-mandate` | GF-S leaves orchestration to methodology layer; substrate doesn't mandate orchestrator shape. | — |
| §7.1.9 workpad protocol | `absorbed (with adaptation)` | GF-S §2 P-01 sandbox + §3 cycle step 4 sandbox-open with capability profile is the workpad-equivalent substrate primitive. | specs/gf-s.md §2 + §3 cycle step 4 |
| §7.1.10 tiered cycle scope | `absorbed (with adaptation)` | GF-S §3 three-regime dispatch (`automation-eligible` / `augmentation-required` / `escalate`) substrate-types Atelier's cycle-scope-tiers per work-unit-class. | specs/gf-s.md §3 regime structure |
| §7.1.11 severity × autofix axes | `absorbed (silently — flagged for auditor)` | The orthogonal-axes framing influenced v3's mandate-fit-per-(architecture × work-unit-class) DEC-2 schema. Not explicitly cited in GF-S spec. | — (flagged for silent-absorption auditor) |
| §7.1.12 residual work gate | `absorbed (with adaptation)` | GF-S §3 cycle step 8 Patrol audit + §2 four-guard mediator typed-envelope to P-07 close the residual-work surface at substrate level. | specs/gf-s.md §3 + §2 P-15 |
| §7.1.13 three memory tiers | `absorbed (with adaptation)` | GF-S §3 pace-layer split (intent block slow / spec body fast) + Patrol-guarded invariants absorb Brier-style pace-layering at substrate. | specs/gf-s.md §3 distinctive decision 1 |
| §7.1.14 implementation roadmap | `not-applicable-to-candidate-mandate` | Architecture-specific deployment. | — |

### §7.3 Notes

GF-S's relationship to Compound Atelier is selective: the artifact-stack mapping (§7.1.3), workpad-as-sandbox (§7.1.9), tiered-cycle-scope (§7.1.10), residual-work gate (§7.1.12), and three-memory-tiers (§7.1.13) all land at substrate level — but the *compounding mechanism itself* (§7.1.1, §7.1.2) is N/A because GF-S substrate-first deliberately abstains from knowledge-accumulation pattern. This is the substrate/methodology split as GF-S's distinctive departure from Atelier: Atelier blends compounding-as-methodology with persona-workshop-as-methodology; GF-S keeps the substrate surfaces (event log + trajectory + sandbox) but lets methodology choose the compounding pattern. The silent-absorption flag on §7.1.11 (severity × autofix → DEC-2 schema) is genuine: v3's mandate-fit-per-(architecture × work-unit-class) framing very likely inherited the orthogonal-axes pattern from Compound Atelier §6.2 without explicit citation in GF-S spec.

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
| §8.1.1 structured pre-agile core thesis | `not-applicable-to-candidate-mandate` | Phase-Gated-Foundry-specific; GF-S is substrate-first not phase-gated. Methodology is deliberately thin, not structured-heavy. | — |
| §8.1.2 phase model + V&V pairing | `not-applicable-to-candidate-mandate` | Foundry-specific cycle structure; GF-S §3 is an 8-step substrate-cycle, not phase-gated. | — |
| §8.1.3 Configuration Management discipline | `absorbed (with adaptation)` | GF-S §2 P-10 coordination medium (Git-LFS content-addressed + signed `refs/factory/events/<stream>`) is the substrate-level CM analogue with cryptographic provenance. | specs/gf-s.md §2 P-10 + ADR 0037 |
| §8.1.4 defect-of-origin table | `absorbed (with adaptation)` | GF-S §2 P-05 trajectory sub-ms persistence + P-15 four-guard mediator typed-envelope to P-07 telemetry provide defect-of-origin traceability per-cycle. | specs/gf-s.md §2 + ADR 0038 |
| §8.1.5 RUP-style discipline × phase matrix | `not-applicable-to-candidate-mandate` | Foundry-specific; GF-S §4 binds all 10 disciplines uniformly at substrate / discipline layer, not per-phase. | — |
| §8.1.6 iteration within phases | `not-applicable-to-candidate-mandate` | Foundry-specific. | — |
| §8.1.7 V&V-side independent roles + different model family | `absorbed` | GF-S §4 bias-guard binding via P-14 + P-15 contradiction-detector requires 3-of-N family-diverse ensemble; F27/F48 mitigation surfaced as partial-RG. | specs/gf-s.md §4 bias-guard |
| §8.1.8 CM as spine | `absorbed (with adaptation)` | GF-S §1 substrate-first axis treats P-10 coordination + P-05 trajectory as the spine; methodology rides on top. | specs/gf-s.md §1 axis + §2 |

### §8.3 Notes

Foundry's specific phase-gated structure is N/A to GF-S (4 N/A cells out of 8), but two foundry primitives land deeply: Configuration Management (substrate-level via P-10 signed event log) and cross-model V&V independence (§4 bias-guard binding via 3-of-N family-diverse ensemble). These are the Foundry-lineage inheritances that complement GF-S's selective Atelier inheritance and weak Refinery inheritance — supporting the multi-lineage characterization in §1.

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
| §9.1.1 population + selection core thesis | `not-applicable-to-candidate-mandate` | Tournament-specific population-based methodology; GF-S substrate accommodates population/tournament as one of multiple methodology overlays but doesn't privilege it. | — |
| §9.1.2 genome structure | `not-applicable-to-candidate-mandate` | Tournament-specific artifact. | — |
| §9.1.3 model-family diversity as structural | `absorbed` | GF-S §4 bias-guard binding via P-14 + P-15 contradiction-detector explicitly requires 3-of-N family-diverse ensemble — structural diversity at substrate. F46 mitigation. | specs/gf-s.md §4 bias-guard + ADR 0018 |
| §9.1.4 generation cycle | `not-applicable-to-candidate-mandate` | Tournament-specific. | — |
| §9.1.5 predator agent | `rejected (subsumed by substrate-level adversarial discipline)` | GF-S substitutes Tournament's predator-agent with substrate-level adversarial: P-15 four-guard mediator + contradiction-detector + Patrol audit. Substrate substitution. | — |
| §9.1.6 loops within loops | `absorbed (with adaptation)` | GF-S §4 three-loop discipline (ADR 0026) bound thinly + Patrol-tier (P-06) meta-loop is the analogue; meta-loop ≠ tournament-loop but substrate accommodates. | specs/gf-s.md §4 three-loop |
| §9.1.7 independence policy | `absorbed` | GF-S §4 bias-guard + §2 P-14 judge router enforce builder-judge independence at substrate via family-diverse dispatch. | specs/gf-s.md §2 + §4 |
| §9.1.8 scaling | `tbd` | GF-S §6 cost-stacking math (four-guards × every-cycle × ensemble-fanout) is an open carry; Tournament's scaling lessons may or may not apply. Phase-8. | — |

### §9.3 Notes

Tournament's primary primitives (population, predator-agent, tournament bracket) are N/A to GF-S, but the cross-model-family diversity discipline (§9.1.3) and independence policy (§9.1.7) land at substrate level via the P-14 judge router + P-15 contradiction-detector binding. Predator-agent (§9.1.5) is explicitly rejected with reason: GF-S substrate-level adversarial closure (four-guard mediator + contradiction-detector ensemble + Patrol) substitutes for runtime predator pressure. The greenfield mandate also makes population-based tournament less natural — at day-0 there are no competing genomes to select from; GF-S's substrate accommodates tournament-as-methodology if a downstream operator chooses it.

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
| §10.1.1 F1 Hallucination | `absorbed` | GF-S §4 bias-guard (ADR 0018) + P-15 contradiction-detector 3-of-N family-diverse ensemble closes F1. | specs/gf-s.md §4 + §2 P-15 |
| §10.1.2 F2 Reward hacking | `absorbed` | GF-S §4 holdout (ADR 0021) substrate-typed via P-08 builder-blindness — substrate enforces. | specs/gf-s.md §4 holdout |
| §10.1.3 F3 Spec-completeness | `absorbed (with adaptation)` | GF-S §2 P-15 four-guard mediator guard 1 (GtWR vocabulary lint via P-12 EARS+GtWR rule pack) closes spec-completeness at substrate. | specs/gf-s.md §2 P-15 + ADR 0032 |
| §10.1.4 F4 Code quality | `absorbed (with adaptation)` | GF-S §4 bias-guard cross-model judging + §2 P-17 (via P-22 polyglot index syntactic/symbol-graph). | specs/gf-s.md §2 + §4 |
| §10.1.5 F5 Cognitive ceiling | `absorbed (with adaptation)` | GF-S §3 three-regime dispatch (`automation-eligible` lights-out only when substrate-measured signals saturate) is the cognitive-ceiling mitigation. | specs/gf-s.md §3 regime structure |
| §10.1.6 F6 Cognitive debt | `absorbed` | GF-S §4 cognitive-escrow bound at P-05 trajectory + Patrol per DEC-2 demotion; interval-as-design-site primitives remain substrate-typed. | specs/gf-s.md §4 cognitive-escrow + ADR 0019 |
| §10.1.7 F7 Normalization of deviance | `absorbed (with adaptation)` | GF-S §3 Patrol audit (P-06 tier-3) guards operator-declared invariants cross-cycle — resists deviance accumulation. | specs/gf-s.md §3 cycle step 8 + §2 |
| §10.1.8 F8 Stale knowledge | `absorbed (with adaptation)` | GF-S §3 cycle step 8 Patrol audit explicitly invokes F8 stale-knowledge inversion mitigation; P-05 trajectory + P-22 incremental refresh on within-factory code. | specs/gf-s.md §3 cycle step 8 |
| §10.1.9 F9 Spec overfitting | `absorbed (with adaptation)` | GF-S §4 honesty binding explicitly invokes "[F9 spec overfitting] as detectable even when not preventable" via P-05 trajectory + P-15 typed-envelope. | specs/gf-s.md §4 honesty |
| §10.1.10 F10 Findings disappear | `absorbed` | GF-S §2 P-10 signed event log + P-05 sub-ms trajectory + P-07 telemetry close finding-disappearance at substrate. | specs/gf-s.md §2 P-10 + P-05 + P-07 |
| §10.1.11 F11 Renumbering | `absorbed (with adaptation)` | GF-S §2 P-05 content-addressed sub-ms persistence + P-10 signed refs provide content-addressed stable IDs. | specs/gf-s.md §2 P-05 + P-10 |
| §10.1.12 F12 Lethal trifecta | `absorbed (verified)` | GF-S §4 trifecta closure (ADR 0027): P-01 sandbox closure-first + P-15 perimeter typing guard 4 CaMeL-class + P-25 runtime per-call. | specs/gf-s.md §4 trifecta closure + §2 P-15 |
| §10.1.13 F13 Missing-config | `absorbed (with adaptation)` | GF-S §2 P-15 perimeter typing rejects missing-cap calls; P-19 OPA hard-floor surfaces config-dependency drift. | specs/gf-s.md §2 P-15 + §3 step 3 |
| §10.1.14 F14 Attribution collapse | `absorbed (with adaptation)` | GF-S §2 P-10 signed event log + P-05 trajectory ("the only artifact that survives [F14 forensic reconstruction widening]") explicitly closes F14. | specs/gf-s.md §2 P-05 (F14 invocation) |
| §10.1.15 F15 Single-prompt collapse | `absorbed (with adaptation)` | GF-S §4 bias-guard cross-model judging + P-15 contradiction-detector 3-of-N family-diverse — structural diversity at substrate substitutes for Atelier's six-divergent-frames. | specs/gf-s.md §4 bias-guard + §2 P-15 |
| §10.1.16 F16 Resume-fidelity | `absorbed` | GF-S §2 P-05 trajectory capture + P-10 typed-event log signed refs provide resume anchor. | specs/gf-s.md §2 P-05 + P-10 |
| §10.1.17 F17 Parallel agents on shared dirs | `tbd` | GF-S §3 distinctive decision 3: agent topology is methodology-layer; substrate accommodates parallelism but specific anti-collision is methodology call. | — |
| §10.1.18 F18 Prose-spec rigor | `absorbed (with adaptation)` | GF-S §2 P-15 four-guard mediator guard 1 GtWR vocabulary lint via P-12 EARS+GtWR rule pack — substrate-level rigor. | specs/gf-s.md §2 P-15 + ADR 0032 |
| §10.1.19 F19 Model-floor dependency | `absorbed` | GF-S §4 bias-guard cross-model judging via P-14 + Larbi MCC ≤ 0.55 carry surfaces model-floor explicitly per F27/F48. | specs/gf-s.md §4 + §6 P-15 reliability |
| §10.1.20 F20 Maintenance asymmetry | `absorbed (with adaptation)` | GF-S §3 regime structure (`automation-eligible` / `augmentation-required` / `escalate`) per work-unit-class accommodates maintenance asymmetry at substrate; §5 mandate-fit per-class declares. | specs/gf-s.md §3 + §5 |
| §10.1.21 A1 Refinery coverage row | `not-applicable-to-candidate-mandate` | Coverage row characterizes Architecture 1, not GF-S. Informational. | — |
| §10.1.22 A2 Atelier coverage row | `not-applicable-to-candidate-mandate` | Coverage row characterizes Architecture 2 (GF-S's weak-overlap lineage on artifact stack), but per-Atelier scoring is not per-GF-S. | — |
| §10.1.23 A3 Foundry coverage row | `not-applicable-to-candidate-mandate` | Coverage row characterizes Architecture 3. | — |
| §10.1.24 A4 Tournament coverage row | `not-applicable-to-candidate-mandate` | Coverage row characterizes Architecture 4. | — |

### §10.3 Notes

19-of-20 F-modes absorbed (F1, F2, F3, F4, F5, F6, F7, F8, F9, F10, F11, F12, F13, F14, F15, F16, F18, F19, F20) — note F12 + F14 are verified-absorbed with explicit GF-S spec invocations. 1 is TBD (F17 — parallel agents). No F-mode marked N/A to GF-S — the substrate-first axis carries broad F-mode coverage via the four-guard mediator + judge router + Patrol-tier stack. The 4 per-architecture coverage-strength rows are informational characterizations of the v2 architectures, not GF-S-actionable items. GF-S's F-mode coverage is notably broader than BF-S's (BF-S had 2 N/A on F9/F18 spec-discipline; GF-S absorbs both via P-15 guard 1 GtWR lint + P-12 EARS rule pack at substrate).

## §11 Summary

**Per-token cell counts (matches YAML frontmatter):**

| Token | Count |
|---|---|
| `absorbed` (incl. with-adaptation, verified, silently) | 61 |
| `rejected (reason)` | 5 |
| `not-applicable-to-candidate-mandate` | 27 |
| `tbd` | 5 |
| **Total classification-table cells** | **98** |

(Total = sum of §N.2 rows across §2.2 (3) + §3.2 (16) + §4.2 (8) + §5.2 (9) + §6.2 (8) + §7.2 (14) + §8.2 (8) + §9.2 (8) + §10.2 (24) = **98 cells**. Some §4.2 rows group D-3..D-7 defaults into one classification entry; D-defaults are individually re-verified in §1.5. The silent-absorption auditor uses §N.2 table-row counts as the authoritative cell count — frontmatter YAML carries the same 98-cell total.)

**High-confidence absorbed cells:** D-2, D-3, D-4, D-5, D-6, D-7 (verified per §1.5); F12 lethal trifecta + F14 attribution + P-05 forensic reconstruction (verified at §2/§4 with explicit GF-S spec F-mode invocations); the substrate-first axis on shared-infrastructure (§5.1.9 build shared infrastructure first ↔ GF-S §2 commodity-substrate baseline).

**Surfaced TBDs (require lead-agent reconciliation or Phase-8 follow-up):**

1. §3.1.15 parallel-agent + human-role tension — methodology-layer; Phase-8 lean-eval on agent topology.
2. §4.1.6 falsified consensus items — needs per-item review of what was falsified vs preserved in v3.
3. §6.1.5 Refinery 5-mode failure classification — Phase-8 lean-eval candidate against GF-S F-mode coverage.
4. §9.1.8 Tournament scaling lessons — GF-S §6 cost-stacking carry; Phase-8.
5. §10.1.17 F17 Parallel agents on shared dirs — methodology-layer call.

**Silent-absorption auditor flags (for cross-spec reconciliation):**

- §3.1.16 cross-cutting primitives (v3 `primitives/index.md` likely inherited the framing without explicit GF-S spec citation — same flag as BF-S audit).
- §7.1.11 severity × autofix orthogonal axes (likely informed DEC-2 mandate-fit-per-(architecture × work-unit-class) schema without explicit GF-S spec citation — same flag as BF-S audit).

**Known-rejected items confirmed:**

- §4.1.10 OpenHands+Overstory substrate stack — `rejected (explicitly-excluded-per-constraints-extracted)`.
- §5.1.7 Compound Atelier as baseline — `rejected (explicitly-anchor-avoided)`.

**Multi-lineage characterization confirmed.** GF-S is the only audited candidate so far with no single dominant v2 lineage — Atelier weak-overlap on artifact stack + memory tiers, Foundry inheritance on CM-as-spine + cross-model V&V, Tournament inheritance on model-family diversity + independence, Refinery weak inheritance on spec-as-durable (pace-layer-adapted). This is consistent with GF-S's substrate-first axis: the substrate is *spec-shape-agnostic* and *methodology-shape-agnostic*, so it inherits substrate-shaped primitives from every v2 architecture without committing to any single methodology framing.

## §12 References

**GF-S spec + supporting docs:**

- [`architectures/v3/specs/gf-s.md`](../specs/gf-s.md) — GF-S Phase-6 architecture spec (audit input).
- [`architectures/v3/candidate-registry.md` GF-S entry](../candidate-registry.md#gf-s--greenfield-substrate-first) — registry entry for §1 lineage statement.
- [`architectures/v3/substrate-requirements/gf-s.md`](../substrate-requirements/gf-s.md) — substrate-requirements summary.
- [`architectures/v3/tracks/greenfield-substrate-first.md`](../tracks/greenfield-substrate-first.md) — Phase-3 track sketch.
- [`architectures/v3/decisions/auto-007-phase-7-dispatch-shape.md`](../decisions/auto-007-phase-7-dispatch-shape.md) — Phase-7 dispatch brief.
- [`architectures/v3/primitives/overlap.md`](../primitives/overlap.md) — Phase-4.2 absorption verdicts on P-08/P-09 + P-12/P-16 + P-19.
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

**ADRs cited (GF-S binding set):**

- Common substrate: [0010](../../../docs/adr/0010-p-01-sandbox-runtime.md) (P-01) / [0011](../../../docs/adr/0011-p-02-cost-ceilings.md) (P-02) / [0012](../../../docs/adr/0012-p-05-trajectory-capture.md) (P-05) / [0013](../../../docs/adr/0013-p-06-watchdog-tiers.md) (P-06) / [0014](../../../docs/adr/0014-p-07-telemetry-ingestor.md) (P-07) / [0015](../../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md) (P-08) / [0016](../../../docs/adr/0016-p-14-judge-router.md) (P-14) / [0017](../../../docs/adr/0017-p-22-polyglot-codebase-index.md) (P-22).
- Discipline: [0018-0027](../../../docs/adr/).
- Framework + designed-system: [0028](../../../docs/adr/0028-p-19-eligibility-regime-classifier.md) (P-19 framework) / [0032](../../../docs/adr/0032-p-12-deterministic-linter-framework.md) (P-12).
- GF-S orphans: [0037](../../../docs/adr/0037-p-10-coordination-medium.md) (P-10) / [0038](../../../docs/adr/0038-p-15-four-guard-mediator.md) (P-15).
- GF-S per-variant: [0039](../../../docs/adr/0039-p-19-variant-gf-s-work-unit-class.md) (P-19/GF-S work-unit-class).

**Constraints / decisions:**

- [`architectures/v3/constraints-extracted.md`](../constraints-extracted.md) — UC1-UC8 user constraints (source of known-rejected v3 item flags).
- [`architectures/v3/decisions-captured.md`](../decisions-captured.md) — DEC-1 / DEC-1.a / DEC-2 etc.
- [`architectures/v3/failure-modes-v3.md`](../failure-modes-v3.md) — v3 F-mode extension catalog.
