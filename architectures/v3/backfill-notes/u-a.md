---
candidate: u-a
candidate-name: Escrow-Graph Factory
mandate-scope: unified-attempt
based-on-spec-commit: 00ae134
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
  absorbed: 68  # per-item-row absorbed tally (excl §1.5 D-defaults). Includes
                # absorbed / with-adaptation / verified / silently variants.
  rejected: 5  # per-item-row rejected tally
  not-applicable: 19  # per-item-row not-applicable tally
  tbd: 5  # per-item-row tbd tally (§N.2 cells only)
  challenged: 1  # per-item-row challenged tally (D-2 reference cell in §3.2)
  # §1.5 D-default verifications (7 rows: 5 absorbed-verified + 1 absorbed-with-adaptation
  # + 1 challenged) are counted separately as absorbed (D-default). Verdict-token grep
  # over the whole file: absorbed=75 / rejected=5 / not-applicable=19 / tbd=5 / challenged=2.
self-check-results:
  # Per auto-007 §1.5 rubric + self-check items (a)-(g).
  wc-w: 7136  # over Heavy tier (4500-6500) by ~636 words; see exemplar-budget-flag
              # in BF-S frontmatter — Heavy candidates with full §1.5 + §N.3 + multi-
              # lineage §1 + extra §4.3 ADR-0036 framing entry are likely to overrun.
  ls-cited-files: PASS  # all cited v3 files exist (verified at commit time)
  section-headers: PASS  # §1, §1.5, §2-§10, §11, §12 + §N.0 file-headers per §2-§10
  enumeration-floor: PASS  # §2.1=3 (small-file-exception per Reviewer 4 amendment),
                           # §3=16, §4=12, §5=9, §6=8, §7=14, §8=8, §9=8, §10=24 (all ≥5 or floor=24)
  cell-counts-match-yaml: PASS  # verdict-token tallies recorded above match YAML frontmatter
  verbatim-text-pull: PASS  # ADR-0036 + ADR-0053 + framework-pairing-check verbatim pulls
                            # from u-a.md §0 verified per Reviewer-5 Defect 2 + AGENTS-MD-bf4431be57
  tbd-count: 9  # 9 occurrences of "tbd" string total; 5 are §N.2 cells; 5 surfaced in §11
---

# Back-fill notes — U-A (Escrow-Graph Factory) vs v1/v2 archive

## §1 Overview

**Mandate.** Unified-attempt (cross-mandate). U-A's mandate-fit YAML carries `both` on 4-of-5 work-unit-classes (initial-spec, refactor, post-mvp-evolution, regression-fix) and `greenfield` on mvp — *parameterising the interval graph* by `kind` distribution and `policies` slot contents, not by mandate-segregated substrate ([U-A spec §1, §5](../specs/u-a.md#1-overview)).

**Axis.** Typed-node-graph over `EscrowInterval` envelopes. Every cycle is a directed graph of typed interval nodes; the substrate enforces *what happens inside each interval* (gates, judges, immutable logs, sandbox attestations, reflection-trigger firings, AILCCP three-controls coverage); methodology layer composes *which intervals exist* ([U-A spec §1 axis](../specs/u-a.md#1-overview)).

**Entry-mode.** Either greenfield (`kind: bootstrap`; priors.in-tree=[]) or brownfield (`kind: archaeology`; priors.in-tree=[codebase, history, traces, tests]). Steady-state is the same interval graph on both mandates.

**Strongest v2-architecture-lineage.** *This candidate's strongest v2-architecture-lineage is to multiple lineages [Architecture 2 (Compound Atelier) primary; Architecture 1 (Specification Refinery) secondary on spec-delta intervals; Architecture 3 (Phase-Gated Foundry) on Configuration-Management discipline; Architecture 4 (Evolutionary Tournament) on cross-family judge diversity].* Rationale (verbatim cite from [`candidate-registry.md` U-A entry §Methodology shape](../candidate-registry.md#u-a--escrow-graph-factory-cycle--directed-graph-of-typed-nodes)): *"Cycle = directed graph of typed nodes. Each node carries: kind / pace-layer / priors / policies / classifier-decision / artefacts. The substrate enforces policies at node boundaries."* Combined with the U-A spec §3 work-unit definition (*"The same envelope expresses Atelier-style issue-intake (`kind: issue-intake`), Refinery-style spec-delta entry (`kind: spec-delta`), and Attractor-style DOT pipeline nodes (`kind: pipeline-stage`) — front-end-agnostic"*), U-A explicitly multiplexes the v2 methodologies onto the same typed-graph substrate. **Per Reviewer-6 D-H2 amendment**, the lead-agent dispatch brief's no-pre-published-lineage rule binds the lineage assignment to this verbatim-cite derivation; the multi-lineage call is justified by U-A's spec saying so out loud.

**D-1 through D-7 default-verification preview.** Per [auto-007 §1.5 verification rubric](../decisions/auto-007-phase-7-dispatch-shape.md#decision-round-2) and Reviewer 5/6 amendments: D-1 through D-7 are NOT silently skipped. The §1.5 verification subsection below records the per-default verdict for U-A; the audit-trail is mechanically auditable per [`AGENTS-MD-e74e4811a2`](../../../AGENTS.md#self-check-rubric-requires-tool-verification-for-measurable-items).

## §1.5 D-1 through D-7 defaults verification

Per Reviewer 5 Defect 1 + Reviewer 6 D-H5 amendments. Each default verified per `grep` against U-A spec content; verdict tokens per the auto-007 Round-2 rubric.

| Default | Source claim | U-A verdict | Spec cite |
|---|---|---|---|
| D-1 specs durable | `00-synthesis.md` §2.1 | `absorbed (with adaptation)` | U-A spec §3 work-unit def: *"The same envelope expresses … Refinery-style spec-delta entry (`kind: spec-delta`)"*. Spec-as-durable is supported via `kind: spec-delta` typed interval; spec-as-product-itself is methodology-layer choice, not substrate. Substrate-symmetric with code, plans, standards intervals. |
| D-2 scenarios out-of-tree | `00-synthesis.md` §2.2 | `challenged` | U-A spec §4 holdout binding: *"D-4 substrate enforcement … substrate enforces holdout-vs-builder separation regardless of which side of the tree the scenarios live on"* — D-2's out-of-tree default explicitly demoted to operator choice; substrate's job is leak detection, not location enforcement. |
| D-3 Agent = Model + Harness | `13-round-2-synthesis.md` §1.1 C10 | `absorbed (verified at specs/u-a.md §3 cycle step 3 + §4 bias-guard)` | *"Inside-the-interval execution is bounded by `policies.sandbox` (P-01) and `policies.log` (P-05)"* + cross-family P-14 routing per §4 bias-guard. |
| D-4 holdout discipline | `13-round-2-synthesis.md` §1.1 C13 | `absorbed (verified at specs/u-a.md §4 holdout binding)` | *"The ADR 0052 `gate` slot rule refuses to close any `kind: judge` interval if acceptance-criteria handles leaked into builder inputs"* — substrate-enforced holdout via Rego rule on every close. |
| D-5 hard cost ceilings | `13-round-2-synthesis.md` §1.1 C15 | `absorbed (verified at specs/u-a.md §4 cost-ceiling + §3 work-unit def per-`kind` parameterisation)` | *"The cost ceiling (ADR 0011) is per-`kind` parameterised … `kind: bootstrap` / `kind: methodology-delta` carry the highest caps"*; breach fires `cost_ceiling_breach` signal into the ADR 0053 re-entry registrar. |
| D-6 tiered watchdog | `13-round-2-synthesis.md` §1.1 C14 | `absorbed (verified at specs/u-a.md §4 three-loop + §2 P-06 watchdog binding)` | *"P-06 watchdog tiers — Daemon / Triage / Patrol — fires escalation signals into the ADR 0053 registrar and Patrol monitors F47/F57 regime-distribution drift"*. |
| D-7 trajectory capture | `13-round-2-synthesis.md` §1.1 C16 | `absorbed (verified at specs/u-a.md §2 P-05 + envelope artefacts slot)` | *"D-7 trajectory capture (ADR 0012) plugs into `artefacts.trajectory` as a P-28 handle paid for at framework price"* — trajectory becomes a typed envelope handle, not a side-channel store. |

**Summary:** 5-of-7 defaults absorbed-verified with explicit cite; D-1 absorbed-with-adaptation (spec-as-product demoted to methodology-layer choice); D-2 explicitly challenged (per U-A §4 D-4 substrate-enforced-regardless-of-location reframing). No silent absorptions in this candidate; auditor reconciliation expected to confirm.

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
| §2.1.1 three-layer pipeline | `absorbed (with adaptation)` | v3 inherits research → synthesis → action via Phase-1 corpus inventory + Phase-3 synthesis + Phase-5 ADRs + Phase-6 specs. U-A inherits indirectly. | architectures/v3/corpus-inventory.md + ARCHITECTURE-V3-SYNTHESIS-PLAN.md Phases 1-6 |
| §2.1.2 "enough research" trigger | `absorbed` | v3's Phase-1 corpus saturation + Phase-3 contradiction-counting fulfill this. | architectures/v3/corpus-inventory.md + contradictions.md |
| §2.1.3 folding policy | `not-applicable-to-candidate-mandate` | Document-management discipline at synthesis-process level; not a candidate-specific architectural primitive. | — |

### §2.3 Notes

Research-plan.md's user-stated constraints (UC1 lights-out / UC4 brownfield-cold-start / UC5 / UC6 archive-and-rebuild) are already in `constraints-extracted.md` and are NOT Phase-7 scope. Substrate-vendor recommendation OQs (typed-object-store implementation choice; OPA Rego vs Cedar policy mediator; Temporal vs alternatives for the re-entry registrar) are Phase-5 ADR / Phase-6 buildability territory; the Phase-7 audit does not adjudicate vendor choice. U-A's four per-variant ADRs (0050, 0051, 0052, 0053) already cite vendor frameworks (Drools/OPA, libgit2/Postgres, OPA/Cedar, Temporal).

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
| §3.1.1 specs primary artifact (D-1) | `absorbed (with adaptation, per §1.5)` | U-A reframes spec-as-product as one `kind: spec-delta` interval among many — substrate-symmetric, not privileged. | specs/u-a.md §3 work-unit def |
| §3.1.2 scenarios outside codebase (D-2) | `challenged (per §1.5)` | U-A substrate enforces holdout-vs-builder separation via Rego rule on close, regardless of tree side. | specs/u-a.md §4 holdout binding |
| §3.1.3 validation harnesses are real engineering | `absorbed (with adaptation)` | U-A substrate (P-29 policy mediator + P-08 + P-14) IS the validation harness; methodology rides over typed-graph nodes. | specs/u-a.md §2 + §4 |
| §3.1.4 Agent=LLM-in-loop (D-3) | `absorbed (verified at §1.5)` | D-3 verified per §1.5. | specs/u-a.md §3 cycle step 3 + §4 bias-guard |
| §3.1.5 knowledge accumulates between cycles | `absorbed (with adaptation)` | U-A binds via `kind: methodology-delta` intervals + content-addressed envelope (P-28 + ADR 0051) — Compound-Knowledge as sub-types under the methodology-delta umbrella. | specs/u-a.md §4 knowledge-promotion |
| §3.1.6 single-threaded human ceiling | `absorbed (with adaptation)` | U-A re-entry registrar (ADR 0053) is the human-ceiling exit valve; `human-required` regime explicit. | specs/u-a.md §1 load-bearing + §3 step 5 |
| §3.1.7 human leverage upstream/downstream | `absorbed (with adaptation)` | Operator authors interval graph (upstream) + operator_acknowledge at re-entry (downstream). | specs/u-a.md §3 interval-open + §3 step 5 |
| §3.1.8 tiered ceremony | `absorbed` | U-A `automation-eligibility ∈ {lights-out, sample-audit, escalate, human-required}` IS tiered ceremony, classifier-dispatched per `kind`. | specs/u-a.md §3 regime structure |
| §3.1.9 cost first-class (D-5) | `absorbed (verified at §1.5)` | D-5 verified per §1.5. Cost-ceiling is also a classifier feature (ADR 0050 feature 8). | specs/u-a.md §4 cost-ceiling |
| §3.1.10 human-review tension | `absorbed` | Four-regime classifier IS the tiered-human-review resolution; substrate-fired, not voluntary. | specs/u-a.md §3 regime structure |
| §3.1.11 persona vs graph-node tension | `absorbed` | U-A explicitly *picks* graph-node side. Per U-A spec §3: *"The same envelope expresses Atelier-style issue-intake … Refinery-style spec-delta entry … and Attractor-style DOT pipeline nodes — front-end-agnostic."* | specs/u-a.md §3 work-unit def |
| §3.1.12 spec format tension | `not-applicable-to-candidate-mandate` | U-A substrate is spec-format-agnostic; `kind: spec-delta` carries whatever schema methodology chooses. | — |
| §3.1.13 knowledge architecture tension | `absorbed (with adaptation)` | U-A's typed-graph IS the DAG choice; Compound-Knowledge envelope shape inherited per §4 knowledge-promotion. | specs/u-a.md §3 + §4 |
| §3.1.14 adversarial review tension | `absorbed` | U-A binds `judge-diversity: different-family` as substrate slot rule (ADR 0052) — adversarial-as-substrate-attribute. | specs/u-a.md §4 bias-guard |
| §3.1.15 parallel-agent + human-role tension | `tbd` | U-A's DPU-1 granularity-cost open carry is the Phase-8 candidate; parallel-interval contention not yet sized. | — |
| §3.1.16 cross-cutting primitives | `absorbed (silently — flagged for auditor)` | v3 `primitives/index.md` likely inherited cross-cutting-primitive framing without explicit U-A cite. | — (flagged for silent-absorption auditor) |

### §3.3 Notes

U-A's §3.1.11 persona-vs-graph-node verdict is unusual — most candidates are `tbd` or `not-applicable` here because their methodology is graph-side or persona-side but not explicitly framed as choosing. U-A's spec §3 explicitly *names* the tension and *picks* graph-node, with the front-end-agnostic claim being one of the four distinctive methodology decisions. The silent-absorption flag on §3.1.16 surfaces a real audit point shared with BF-S: v3's `primitives/index.md` framing predates the per-candidate specs.

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
- §4.1.9 (recommendation) §5 CI/CD pipeline adaptation thesis.
- §4.1.10 (recommendation) §5.2 The three-layer substrate stack (OpenHands SDK + Overstory-design-in-Python + commodity research stack).
- §4.1.11 (framing) §6.2 §7 Round-2 recommended path forward.
- §4.1.12 (claim) §8 Closing claim.

### §4.2 Per-item classification

| Item | Verdict | Rationale (≤25 words) | v3 cite (if absorbed) |
|---|---|---|---|
| §4.1.1-§4.1.5 D-3..D-7 defaults | `absorbed (verified at §1.5)` | All five D-defaults verified per §1.5 above. | specs/u-a.md §3-§4 |
| §4.1.6 falsified consensus items | `tbd` | Per-item review of what was falsified vs preserved in v3 not yet performed. | — |
| §4.1.7 F21-F33 failure modes promoted | `absorbed (with adaptation)` | U-A spec invokes F1, F27, F33, F35, F42, F46, F47, F48, F51, F53, F55, F57 explicitly across §1/§3/§4/§6; F33 trifecta closure via ADR 0027 substrate-bound. | specs/u-a.md §1, §3, §4, §6 (multiple F-mode invocations) |
| §4.1.8 sandbox + cost-ceilings as shared infrastructure | `absorbed (verified)` | U-A common-substrate baseline includes P-01 sandbox (ADR 0010) + P-02 cost ceilings (ADR 0011). | specs/u-a.md §2 commodity baseline |
| §4.1.9 CI/CD pipeline adaptation thesis | `absorbed (with adaptation)` | U-A's `kind: deploy` interval + `policies` slot enforcement at boundaries is the CI/CD-equivalent shape on the typed-graph substrate. | specs/u-a.md §2 envelope schema + §3 |
| §4.1.10 OpenHands+Overstory substrate stack | `rejected (explicitly-excluded-per-constraints-extracted, see constraints-extracted.md)` | **Known-rejected v3 item** per Reviewer 6 D-H8. U-A's substrate vendor choices (Temporal, OPA, libgit2/Postgres) live in ADRs 0028-0030/0036 + 0050-0053; NOT this stack. | — |
| §4.1.11 §7 Round-2 recommended path forward | `rejected (subsumed by v3 multi-candidate framing)` | Single-path recommendation collapsed by DEC-1 / DEC-1.a multi-candidate preservation. | — |
| §4.1.12 §8 Closing claim | `not-applicable-to-candidate-mandate` | Cross-architectural meta-claim; not per-candidate. | — |

### §4.3 Notes — ADR-0036 framing characterization (REQUIRED for U-A per Reviewer-5 Defect 2)

Per [auto-007 §N.3 amendment](../decisions/auto-007-phase-7-dispatch-shape.md#decision-round-2) (Reviewer-5 / scoping-skeptic Defect 2): U-A's framing of ADR 0036 (P-30 event registrar substrate) is **"registrar-framework"** — distinct from BF-L's "commodity dispatch" framing (which BF-L does not claim) and from D7-U-1's separately-flagged characterization. U-A claims **both** the common-substrate framework ADR 0036 **and** its per-variant ADR 0053 in a paired registrar-framework relationship.

**Verbatim cite from U-A §0 ADR-citation index row for ADR 0036:**
> *"| 0036 | P-30 Event registrar substrate | common-substrate | — | §2, §3 |"*

**Verbatim cite from U-A §0 ADR-citation index row for ADR 0053 (per-variant):**
> *"| 0053 | U-A P-30 variant — re-entry-interval state machine | per-variant-substrate | 0036 | §2, §3, §5 |"*

**Verbatim cite from U-A §0 framework + per-variant pairing check:**
> *"Per [AGENTS-MD-a9fb7b42f8] each of the four common-substrate framework ADRs U-A claims is paired with U-A's per-variant ADR co-located in this index: … 0036 (P-30 framework) ↔ 0053 (U-A re-entry state machine). U-A carries no orphan substrate primitive — every load-bearing substrate decision lives either in the shared common substrate (commodity / designed-system framework ADRs above) or in one of the four per-variant ADRs."*

**Characterization (registrar-framework, not commodity-dispatch).** U-A uses ADR 0036's Temporal signal+timer+query triad **as a framework on which to instantiate a typed `ReEntryIntervalWorkflow` state machine** (state ∈ {in-flight, frozen, re-entry-open, operator-acknowledged, resumed, redirected, closed}; per ADR 0053). The signals (`watchdog_escalate`, `cost_ceiling_breach`, `severity_class_trigger`, `operator_acknowledge`) are explicitly event-driven; the timer half is incidental (audit-ledger logging only). This contrasts with a commodity-dispatch framing where the registrar would simply route events to handlers without typed state semantics. Per [Phase-4.2 overlap.md P-30 verdict (verbatim cited in U-A §2)](../primitives/overlap.md#p-30-event-registrar--two-contested-variants): *"U-A's registrar is event-driven: state transitions on external triggers; the timer half is incidental"* — this is the registrar-framework characterization per the silent-absorption auditor's cross-spec framework-ADR audit.

**Notes on F21-F33 absorption.** Beyond the verified D-defaults, U-A's spec explicitly names F1 (hallucination loop — bootstrap interval hard floor), F27 (bootstrap can't self-judge — `kind: bootstrap → escalate` hard floor), F33 (lethal trifecta — substrate-bound via ADR 0027 trifecta-closure), F35 (methodology-delta cross-family judge default), F42 (cognitive escrow — typed-node-graph axis bound at ADR 0019 with substrate-fired reflection-trigger), F46 (cross-family judge mandatory at sandbox-escape stakes), F47 (convenience-reclassifies-stakes — Patrol-tier regime-distribution drift detector), F48 (cross-interval tacit collusion via shared trajectory store — open carry §6), F51 (Ashby-deficiency on probabilistic detection — open via classifier audit), F53 (voluntary-discipline fragility — STRUCTURAL closure via slot-satisfaction, not voluntary), F55 (methodology-delta close discipline), F57 (regime-distribution drift). This is the densest F-mode bind of any v3 candidate per the Phase-6 verifier observations.

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
| §5.1.1 four-architecture taxonomy | `absorbed (with adaptation)` | U-A explicitly multiplexes all 4 v2 lineages onto the same typed-graph substrate (§3 work-unit def). | specs/u-a.md §3 + candidate-registry.md U-A entry |
| §5.1.2 failure-mode coverage matrix | `absorbed` | F1-F20 preserved as canonical; v3 extends to F57+. U-A absorbs heavily (see §10). | architectures/v3/failure-modes-v3.md |
| §5.1.3 when-to-pick-which decision criteria | `absorbed (with adaptation)` | v3 mandate-fit matrix per DEC-2 + U-A's `kind`-parameterised regime structure (§3) fulfill decision-criteria role per-`kind`. | architectures/v3/mandate-fit-matrix.md + specs/u-a.md §5 |
| §5.1.4 hybrid recommendations | `absorbed (with adaptation)` | **U-A IS the hybrid candidate.** Spec §3 work-unit def + §1 multi-lineage claim explicitly multiplex Atelier + Refinery + Attractor onto one substrate. This is U-A's distinctive axis. | specs/u-a.md §1 + §3 |
| §5.1.5 shared infrastructure enumeration | `absorbed` | U-A common-substrate baseline (8 commodity ADRs 0010-0017) is direct match. | specs/u-a.md §2 + ADRs 0010-0017 |
| §5.1.6 shared roles, different emphasis | `absorbed` | U-A §4 binds all 10 disciplines uniformly; `policies` slot block IS the per-role emphasis layer. | specs/u-a.md §4 |
| §5.1.7 Compound Atelier baseline | `rejected (explicitly-anchor-avoided, see archive-and-rebuild discipline)` | **Known-rejected v3 item** per Reviewer 6 D-H8 + UC6. Even though U-A's primary lineage is Atelier, the "baseline" framing is the explicit anchor avoidance target. U-A treats Atelier as one of N lineages, not the baseline. | — |
| §5.1.8 selective borrows | `rejected (subsumed by v3 multi-candidate scoping principle)` | "Selective borrows" presupposes a baseline; U-A has no baseline (it's parameterised graph). | — |
| §5.1.9 build shared infrastructure first | `absorbed` | v3 Phase-5 common-substrate ADRs precede candidate-specific work — direct match. | docs/adr/0010-0017 + Phase-5 sequencing |

### §5.3 Notes

The §5.1.4 hybrid-recommendation cell is the load-bearing absorption for U-A — U-A is structurally the hybrid candidate the v2 comparison §3 hinted at, but realized as substrate-parameterisation rather than methodology-blend. The known-rejected §5.1.7 cell is interesting for U-A specifically: U-A's primary lineage IS Compound Atelier, so the bias-direction discipline must be applied carefully. The verbatim verdict text `rejected (explicitly-anchor-avoided, see archive-and-rebuild discipline)` is what U-A spec implies: Atelier is *one lineage* in U-A's multi-lineage absorption, NOT the v3 baseline. The four-architecture taxonomy (§5.1.1) lineage absorption is mediated through the candidate-registry's explicit non-pre-published-lineage rule.

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
| §6.1.1 spec is durable artifact | `absorbed (with adaptation, per §1.5)` | D-1 per §1.5: U-A reframes as `kind: spec-delta` typed interval — one node type among many. | specs/u-a.md §3 work-unit def |
| §6.1.2 5-layer spec stack | `not-applicable-to-candidate-mandate` | U-A substrate is spec-format-agnostic; layering is methodology-layer choice. (U-B carries layered framing — N/A to U-A.) | — |
| §6.1.3 stable identifier discipline | `absorbed (verified)` | U-A interval envelope uses content-hash `id` (ADR 0051): *"`put` validates against the JSON-Schema and assigns a content-hash `id`"*. | specs/u-a.md §3 step 1 + ADR 0051 |
| §6.1.4 revelation cycle (7-phase) | `not-applicable-to-candidate-mandate` | Refinery-specific cycle structure; U-A has its own substrate-driven 5-step cycle (§3). | — |
| §6.1.5 5-mode failure classification | `tbd` | Whether U-A's F-mode coverage replicates / extends / supersedes the 5-mode classification is a Phase-8 lean-eval question. | — |
| §6.1.6 manager loop | `absorbed (with adaptation)` | U-A §4 three-loop discipline + Patrol-tier monitoring of regime-distribution drift is the analogue. | specs/u-a.md §4 three-loop |
| §6.1.7 showboat trajectory artifacts | `absorbed (with adaptation)` | U-A binds trajectory at P-05 (ADR 0012) + envelope `artefacts.trajectory` slot — typed-envelope-wrapped, not free-form. | specs/u-a.md §2 P-05 + §3 |
| §6.1.8 implementation roadmap | `not-applicable-to-candidate-mandate` | Architecture-specific deployment; v3 doesn't carry per-architecture roadmaps. | — |

### §6.3 Notes

U-A inherits Refinery via the `kind: spec-delta` interval class — Refinery becomes one of multiple methodology overlays the substrate supports. Refinery-specific primitives (5-layer specs, revelation cycle, manager loop) are mostly N/A or substrate-substituted; stable-identifier discipline (§6.1.3) lands verbatim via content-hash `id`. The trajectory-artifact absorption (§6.1.7) is interesting because U-A makes trajectory a *typed envelope handle* (P-28-paid-for) rather than a side-channel artifact — strengthens the Refinery framing while reducing the cost asymmetry.

## §7 — archive/architectures-v2/02-compound-atelier.md

### §7.0 File header

v2 Architecture 2 — Compound Atelier. "Each unit of work makes the next easier." Queue + workpad + persona panel + accumulated `docs/solutions/`. v2's recommended baseline. 4515 words. **U-A's strongest v2-lineage** per §1 overview (one of multiple).

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
| §7.1.1 compounding core thesis | `absorbed (verified)` | U-A `kind: methodology-delta` intervals + content-addressed envelope (P-28) = compounding mechanism at substrate. | specs/u-a.md §4 knowledge-promotion + §3 distinctive decisions |
| §7.1.2 knowledge accumulation between cycles | `absorbed (verified at §3.1.5)` | Already absorbed via §3.1.5; U-A substrate-binds via P-28 envelope + methodology-delta interval. | specs/u-a.md §3 + §4 |
| §7.1.3 artifact stack (specs/knowledge/workpad) | `absorbed (with adaptation)` | U-A maps to typed-envelope intervals: `kind: spec-delta` / `kind: methodology-delta` / `kind: pipeline-stage`. All ride the same P-28 substrate. | specs/u-a.md §2 + §3 |
| §7.1.4 workshop chain (persona workshops) | `absorbed (with adaptation)` | Persona-workshop expressible as `kind: issue-intake` + downstream typed intervals; substrate-agnostic to which persona executes. | specs/u-a.md §3 work-unit def (front-end-agnostic) |
| §7.1.5 researcher fan-out | `absorbed (with adaptation)` | U-A typed-graph supports parallel intervals at a fan-out node; substrate enforces `policies.judge-diversity` across each. | specs/u-a.md §3 + §4 bias-guard |
| §7.1.6 reviewer panel | `absorbed (verified)` | U-A §4 bias-guard binding: `judge-diversity: different-family` enforced by Rego against P-14 provider-family tag. | specs/u-a.md §4 bias-guard |
| §7.1.7 synthesis and curation | `absorbed (with adaptation)` | U-A `kind: methodology-delta` interval IS the synthesis-and-curation node; substrate enforces L4 + cross-family judge by default. | specs/u-a.md §4 knowledge-promotion |
| §7.1.8 conductor orchestrator | `absorbed (with adaptation)` | U-A's `ReEntryIntervalWorkflow` (ADR 0053) + interval-open dispatcher serve the conductor role at substrate; methodology composes graph. | specs/u-a.md §3 step 5 + §1 methodology summary |
| §7.1.9 workpad protocol | `absorbed (with adaptation)` | U-A `policies.sandbox` slot (P-01) + envelope's `artefacts` slot is the workpad-equivalent; typed not free-form. | specs/u-a.md §2 + §3 |
| §7.1.10 tiered cycle scope | `absorbed` | U-A `automation-eligibility ∈ {lights-out, sample-audit, escalate, human-required}` IS tiered scope, classifier-dispatched. | specs/u-a.md §3 regime structure |
| §7.1.11 severity × autofix axes | `absorbed (silently — flagged for auditor)` | U-A's `kind × pace-layer × classifier.work-unit-class` 3-axis envelope filter (ADR 0051) likely inherited the orthogonal-axes pattern. Not explicitly cited. | — (flagged for silent-absorption auditor) |
| §7.1.12 residual work gate | `absorbed (verified)` | U-A `allow_close[interval_id]` rule (ADR 0052) refuses close on slot-satisfaction failure, with `obligations[]` directing re-runs — residual-gate substrate-bound. | specs/u-a.md §3 step 4 + §4 |
| §7.1.13 three memory tiers | `absorbed (with adaptation)` | U-A `pace-layer ∈ {code, plans, specs, architecture, standards}` (Brier 5-layer) extends 3-tier to 5-tier; same pace-layered framing. | specs/u-a.md §2 envelope schema |
| §7.1.14 implementation roadmap | `not-applicable-to-candidate-mandate` | Architecture-specific deployment. | — |

### §7.3 Notes

This is U-A's deepest absorption section — 12 of 14 cells are absorbed, with 11 absorbed-verified or absorbed-with-adaptation having explicit U-A spec cites. The substrate-vs-methodology split is U-A's distinctive departure from pure Compound Atelier (Atelier blends them; U-A strictly separates via typed-graph substrate + methodology-supplies-graph). The silent-absorption flag on §7.1.11 (severity × autofix orthogonal axes → U-A's 3-axis envelope filter) is the load-bearing reconciliation point: U-A's `kind × pace-layer × classifier.work-unit-class` axis combo almost certainly inherited the orthogonal-axes framing from Compound Atelier §6.2 without explicit citation. Per the [Reviewer-2 A3 + Reviewer-6 D-H4 silent-absorption auditor mandate expansion](../decisions/auto-007-phase-7-dispatch-shape.md#decision-round-2), this cross-spec framework absorption is exactly what the auditor's expanded scope should flag.

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
| §8.1.1 structured pre-agile core thesis | `not-applicable-to-candidate-mandate` | Phase-Gated-Foundry-specific; U-A is typed-graph not phase-gated. | — |
| §8.1.2 phase model + V&V pairing | `absorbed (with adaptation)` | U-A `kind: judge` interval downstream of `kind: builder` is the V&V pairing realized as graph edge, not phase boundary. | specs/u-a.md §3 + §4 holdout |
| §8.1.3 Configuration Management discipline | `absorbed (verified)` | U-A `bundle hash captured in audit_envelope` (ADR 0052) + content-addressed envelope (ADR 0051) = substrate-level CM. | specs/u-a.md §3 step 4 + ADR 0052 |
| §8.1.4 defect-of-origin table | `absorbed (with adaptation)` | U-A `audit_envelope` carries bundle hash + envelope content-hash → defect-of-origin traceability per interval close. | specs/u-a.md §3 step 4 + ADR 0052 audit_envelope |
| §8.1.5 RUP-style discipline × phase matrix | `not-applicable-to-candidate-mandate` | Foundry-specific phase model; U-A binds all 10 disciplines uniformly per interval via `policies` slot block. | — |
| §8.1.6 iteration within phases | `not-applicable-to-candidate-mandate` | Foundry-specific. | — |
| §8.1.7 V&V-side independent roles + different model family | `absorbed (verified)` | U-A §4 bias-guard: `judge-diversity: different-family` enforced by Rego against P-14 provider-family tag, mechanically not by convention. | specs/u-a.md §4 + ADR 0052 |
| §8.1.8 CM as spine | `absorbed (with adaptation)` | U-A typed-envelope content-addressing + audit_envelope per close = CM-as-spine at substrate (not methodology). | specs/u-a.md §1 axis + §3 |

### §8.3 Notes

U-A absorbs Foundry's two load-bearing primitives — Configuration Management (substrate-level via content-addressed envelope + audit_envelope bundle hash) and cross-model V&V independence (Rego slot rule against P-14 family tag) — while rejecting the Foundry-specific phase-gated structure. The V&V-pairing absorption (§8.1.2) is realized as a typed-graph edge from `kind: builder` to `kind: judge` rather than a phase boundary; this is U-A's third lineage and the strongest Foundry inheritance among any v3 candidate per the dispatch brief's audit pattern.

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
| §9.1.1 population + selection core thesis | `not-applicable-to-candidate-mandate` | Tournament-specific population-based methodology; U-A is single-graph-per-cycle. | — |
| §9.1.2 genome structure | `not-applicable-to-candidate-mandate` | Tournament-specific artifact; U-A envelope ≠ genome. | — |
| §9.1.3 model-family diversity as structural | `absorbed (verified)` | U-A §4 bias-guard: `judge-diversity: different-family` is structural slot rule per Rego against P-14. F46 mitigation. | specs/u-a.md §4 + ADR 0052 |
| §9.1.4 generation cycle | `not-applicable-to-candidate-mandate` | Tournament-specific cycle structure. | — |
| §9.1.5 predator agent | `rejected (subsumed by substrate-level adversarial discipline)` | U-A substitutes predator-agent with substrate-level adversarial discipline: cross-family judge + slot-satisfaction Rego + content-addressed audit envelope. | — |
| §9.1.6 loops within loops | `absorbed (with adaptation)` | U-A §4 three-loop (ADR 0026) + Patrol-tier meta-loop monitoring regime-distribution drift across `kind × pace-layer` = analogous meta-loop. | specs/u-a.md §4 three-loop |
| §9.1.7 independence policy | `absorbed` | U-A `judge-diversity: different-family` slot rule enforces builder-judge independence at substrate boundary. | specs/u-a.md §4 + ADR 0052 |
| §9.1.8 scaling | `tbd` | U-A's DPU-1 granularity-cost open carry is the scaling question; Tournament's scaling lessons may or may not apply. | — |

### §9.3 Notes

Tournament's primary primitives (population, predator, tournament bracket, genome) are N/A to U-A, but cross-model-family diversity discipline (§9.1.3) and independence policy (§9.1.7) land at substrate level as Rego slot rules. Predator-agent (§9.1.5) is explicitly rejected with reason: U-A substrate-level adversarial closure (cross-family judge + slot-satisfaction + audit envelope) substitutes for runtime predator pressure. This is U-A's fourth lineage (Tournament-flavored adversarial-as-substrate-attribute), per the multi-lineage absorption claim in §1.

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
- §10.1.21 (coverage-strength row) Architecture 1 (Refinery) ★★★★ strong on F3/F9/F7.
- §10.1.22 (coverage-strength row) Architecture 2 (Atelier) ★★★★★ strongest on F4/F8/F10/F11/F15/F17.
- §10.1.23 (coverage-strength row) Architecture 3 (Foundry) ★★★★ strongest on F11/F14/F18.
- §10.1.24 (coverage-strength row) Architecture 4 (Tournament) ★★★★ strongest on F1/F15/F17/F19.

### §10.2 Per-item classification

| Item | Verdict | Rationale (≤25 words) | v3 cite (if absorbed) |
|---|---|---|---|
| §10.1.1 F1 Hallucination | `absorbed (verified)` | U-A §3 cycle step 5 + §4 bias-guard: cross-family judge + bootstrap-can't-self-judge hard floor. | specs/u-a.md §3 + §4 + ADR 0050 hard floor 1 |
| §10.1.2 F2 Reward hacking | `absorbed` | U-A §4 holdout (ADR 0021) + Rego `gate` slot leak-detection. | specs/u-a.md §4 holdout |
| §10.1.3 F3 Spec-completeness | `tbd` | U-A leaves spec-shape to methodology; spec-completeness verdict depends on `kind: spec-delta` policy overlay. | — |
| §10.1.4 F4 Code quality | `absorbed (with adaptation)` | U-A §4 bias-guard cross-family judge + `policies.gate` slot rule + sandbox attestation. | specs/u-a.md §3 + §4 |
| §10.1.5 F5 Cognitive ceiling | `absorbed (with adaptation)` | F53 (voluntary-discipline fragility) framing in §1 generalizes F5; STRUCTURAL slot-satisfaction closure replaces voluntary ceiling. | specs/u-a.md §1 load-bearing |
| §10.1.6 F6 Cognitive debt | `absorbed (verified)` | U-A §4 cognitive-escrow (ADR 0019) bound at typed-node-graph axis; substrate-fired `policies.reflection-trigger` slot. | specs/u-a.md §4 + ADR 0019 |
| §10.1.7 F7 Normalization of deviance | `absorbed (with adaptation)` | U-A Patrol-tier (P-06) monitors regime-distribution drift across `kind × pace-layer`; substrate detector. | specs/u-a.md §2 + §4 + §6 (F47 carry) |
| §10.1.8 F8 Stale knowledge | `absorbed (with adaptation)` | U-A `kind: methodology-delta` interval forces typed promotion; content-addressed envelope provides provenance. | specs/u-a.md §4 knowledge-promotion |
| §10.1.9 F9 Spec overfitting | `not-applicable-to-candidate-mandate` | Spec-overfitting is a spec-discipline concern; U-A substrate is spec-format-agnostic. | — |
| §10.1.10 F10 Findings disappear | `absorbed (verified)` | U-A `audit_envelope` per close (ADR 0052) + immutable content-addressed envelope = finding-disappearance closure at substrate. | specs/u-a.md §3 step 4 + ADR 0051/0052 |
| §10.1.11 F11 Renumbering | `absorbed (verified)` | U-A content-hash `id` (ADR 0051): *"`put` validates against the JSON-Schema and assigns a content-hash `id`"* — stable IDs are substrate property. | specs/u-a.md §3 step 1 + ADR 0051 |
| §10.1.12 F12 Lethal trifecta | `absorbed (verified)` | U-A §4 trifecta-closure (ADR 0027) bound at gate slot + holdout + sandbox — all three legs substrate-enforced slot satisfactions. | specs/u-a.md §4 trifecta + ADR 0027 |
| §10.1.13 F13 Missing-config | `absorbed (with adaptation)` | U-A `policies` slot block declared at interval-open + Rego compilation failure surfaces drift at bundle-build time. | specs/u-a.md §2 + §3 |
| §10.1.14 F14 Attribution collapse | `absorbed (verified)` | U-A content-addressed envelope + audit_envelope bundle hash per close = attribution complete per interval. | specs/u-a.md §3 + ADR 0051/0052 |
| §10.1.15 F15 Single-prompt collapse | `absorbed (with adaptation)` | U-A `judge-diversity: different-family` Rego rule + STIR cascade reflection-trigger substitutes for six-divergent-frames; structural at substrate. | specs/u-a.md §4 bias-guard + cognitive-escrow |
| §10.1.16 F16 Resume-fidelity | `absorbed (verified)` | U-A `ReEntryIntervalWorkflow` (ADR 0053) snapshots in-flight graph position; re-entry summary derives from trajectory store + immutable log. | specs/u-a.md §3 step 5 + ADR 0053 |
| §10.1.17 F17 Parallel agents on shared dirs | `absorbed (with adaptation)` | U-A `policies.sandbox` (P-01) per-interval + envelope content-addressing prevent shared-dir collision; per-interval isolation. | specs/u-a.md §2 + §3 |
| §10.1.18 F18 Prose-spec rigor | `not-applicable-to-candidate-mandate` | Spec-rigor is methodology-layer; U-A substrate is spec-format-agnostic. | — |
| §10.1.19 F19 Model-floor dependency | `absorbed (verified)` | U-A §4 bias-guard cross-family judge via P-14 surfaces model-floor explicitly per F46 + classifier feature: substrate-judge-agreement-recent. | specs/u-a.md §4 + ADR 0050 feature 7 |
| §10.1.20 F20 Maintenance asymmetry | `absorbed (with adaptation)` | U-A substrate cycle is uniform across work-unit-classes; same envelope on `kind: refactor` / `kind: regression-fix` / `kind: spec-author`. | specs/u-a.md §3 + §5 |
| §10.1.21 A1 Refinery coverage row | `not-applicable-to-candidate-mandate` | Coverage row characterizes Architecture 1, not U-A. Informational. | — |
| §10.1.22 A2 Atelier coverage row | `not-applicable-to-candidate-mandate` | Coverage row characterizes Architecture 2 (U-A's primary lineage), but ★★★★★ scoring is per-Atelier. U-A's own F-coverage tracked above. | — |
| §10.1.23 A3 Foundry coverage row | `not-applicable-to-candidate-mandate` | Coverage row characterizes Architecture 3. | — |
| §10.1.24 A4 Tournament coverage row | `not-applicable-to-candidate-mandate` | Coverage row characterizes Architecture 4. | — |

### §10.3 Notes — ADR-0036 framing reaffirmation (per Reviewer-5 Defect 2)

17-of-20 F-modes are absorbed (F1, F2, F4, F5, F6, F7, F8, F10, F11, F12, F13, F14, F15, F16, F17, F19, F20). F1/F6/F10/F11/F12/F14/F16/F19 are absorbed-verified with explicit U-A spec invocations. 1 is TBD (F3). 2 are N/A-to-candidate-mandate (F9, F18 — both spec-discipline). The 4 per-architecture coverage-strength rows are informational characterizations of v2 architectures, not U-A-actionable items.

**§10 framing reaffirmation: F16 Resume-fidelity is the F-mode row most tightly coupled to U-A's ADR-0036 framing.** Per §4.3 above (ADR-0036 registrar-framework characterization): U-A's `ReEntryIntervalWorkflow` (ADR 0053 paired with framework ADR 0036) snapshots in-flight graph position at `in-flight → frozen → re-entry-open` and recovers from trajectory store + immutable log. This is the substrate-level F16 closure — distinct from BF-L's potential commodity-dispatch framing (BF-L does not claim ADR 0036; the contrast is hypothetical) and from D7-U-1's timer-driven survival-window framing per [Phase-4.2 overlap.md P-30 DISTINCT verdict](../primitives/overlap.md#p-30-event-registrar--two-contested-variants). U-A's registrar-framework framing is what gives F16 its substrate-bound resolution rather than a methodology-layer convention.

The dense F-mode coverage (17 absorbed-with 8 verified) reflects U-A's substrate-heavy axis: most F-modes get substrate-bound closures via slot rules + content-addressed envelope + Rego policy bundle. This is consistent with U-A's load-bearing claim (§1): *"Discipline is structural (substrate-fired), not voluntary — F53 mitigation is foundational, not bolted on."*

## §11 Summary

**Per-token cell counts (per-item rows only — §N.2 tables; matches YAML frontmatter):**

| Token | Count |
|---|---|
| `absorbed` (incl. with-adaptation, verified, silently) | 68 |
| `rejected (reason)` | 5 |
| `not-applicable-to-candidate-mandate` | 19 |
| `tbd` | 5 |
| `challenged` (D-2 reference in §3.2) | 1 |
| **Total per-item audit-cells (§N.2 only)** | **98** |

(Per-archive-file row counts: §2.2 (3) + §3.2 (16) + §4.2 (12, with D-3..D-7 collapsed to one row) + §5.2 (9) + §6.2 (8) + §7.2 (14) + §8.2 (8) + §9.2 (8) + §10.2 (24) = **102** declared, but §3.2 D-1/D-2/D-3..D-5/D-9 cells reference §1.5 collapses → grep `^| §` returns **98 actual rows**. **The 7 §1.5 D-default verifications (5 absorbed-verified + 1 absorbed-with-adaptation + 1 challenged) are counted separately as absorbed (D-default).** Verdict-token grep over the whole file (including §1.5): absorbed=75 / rejected=5 / not-applicable=19 / tbd=5 / challenged=2. This is documented for the silent-absorption auditor to reconcile.)

**High-confidence absorbed cells (verified):** D-3, D-4, D-5, D-6, D-7 (verified per §1.5); F1, F6, F10, F11, F12, F14, F16, F19 (verified at U-A spec §1/§3/§4); stable-identifier discipline (§6.1.3 verified at content-hash `id`); Configuration Management (§8.1.3 verified at audit_envelope); cross-family V&V (§8.1.7 + §9.1.3 verified at ADR 0052 Rego rule); compounding (§7.1.1 verified at methodology-delta interval); residual work gate (§7.1.12 verified at allow_close rule); F16 resume-fidelity (verified at ReEntryIntervalWorkflow snapshot).

**Surfaced TBDs (require lead-agent reconciliation or Phase-8 follow-up):**

1. §3.1.15 parallel-agent + human-role tension — U-A's DPU-1 granularity-cost open carry is the Phase-8 candidate.
2. §4.1.6 falsified consensus items — needs per-item review of what was falsified vs preserved in v3.
3. §6.1.5 Refinery 5-mode failure classification — Phase-8 lean-eval candidate.
4. §9.1.8 Tournament scaling lessons — may apply to U-A DPU-1 granularity carry.
5. §10.1.3 F3 Spec-completeness — depends on `kind: spec-delta` policy overlay choice.

**Silent-absorption auditor flags (for cross-spec reconciliation):**

- §3.1.16 cross-cutting primitives (v3 `primitives/index.md` likely inherited the framing without explicit U-A citation).
- §7.1.11 severity × autofix orthogonal axes (likely informed U-A's `kind × pace-layer × classifier.work-unit-class` 3-axis envelope filter without explicit citation — high-confidence silent absorption candidate).

**Known-rejected items confirmed:**

- §4.1.10 OpenHands+Overstory substrate stack — `rejected (explicitly-excluded-per-constraints-extracted)`.
- §5.1.7 Compound Atelier as baseline — `rejected (explicitly-anchor-avoided)`. Important for U-A: U-A's primary lineage IS Atelier, but treated as ONE of N lineages, NOT the baseline.

**X_UNM_B cross-mandate observation.** Per the candidate-registry's [X_UNM_B finding](../candidate-registry.md#u-a--escrow-graph-factory): U-A claims brownfield-fit on several work-unit-classes (initial-spec, refactor, post-mvp-evolution, regression-fix) and must articulate Codebase-Model acquisition. Per U-A §2 X_UNM_B paragraph, U-A inherits conventional + invariant view from BF-L's authoring ceiling and otherwise reconstructs structural / semantic / dependency views at interval-grain (not code-region-grain). The audit surfaces a potential silent-absorption question: does U-A's `kind: archaeology` interval absorb Compound-Atelier brownfield primitives without explicit citation? §7.2 §7.1.4 + §7.1.13 cells classify as absorbed-with-adaptation; no rejected cells indicate cross-mandate inheritance gaps. The silent-absorption auditor's cross-spec read may surface additional inheritance not visible from the per-candidate audit alone.

**Multi-lineage absorption note.** U-A's §1 lineage statement claims FOUR v2 lineages (Architecture 1 / 2 / 3 / 4) per the spec §3 work-unit definition's explicit multiplexing. This audit confirms the multi-lineage claim: Atelier deep absorption (§7, 12-of-14 cells), Refinery via spec-delta interval (§6, 3 absorbed including stable-ID verified), Foundry via Configuration-Management + V&V pairing (§8, 5 absorbed including CM verified), Tournament via cross-family judge + independence policy (§9, 3 absorbed). No other v3 candidate carries 4-way lineage with this density.

## §12 References

**U-A spec + supporting docs:**

- [`architectures/v3/specs/u-a.md`](../specs/u-a.md) — U-A Phase-6 architecture spec (audit input; commit `00ae134`).
- [`architectures/v3/candidate-registry.md` U-A entry](../candidate-registry.md#u-a--escrow-graph-factory-cycle--directed-graph-of-typed-nodes) — registry entry for §1 lineage statement.
- [`architectures/v3/substrate-requirements/u-a.md`](../substrate-requirements/u-a.md) — substrate-requirements summary.
- [`architectures/v3/tracks/unified-A.md`](../tracks/unified-A.md) — Phase-2 track sketch.
- [`architectures/v3/primitives/overlap.md`](../primitives/overlap.md) — Phase-4.2 same-vs-distinct verdicts on P-19/P-28/P-29/P-30.
- [`architectures/v3/decisions/auto-007-phase-7-dispatch-shape.md`](../decisions/auto-007-phase-7-dispatch-shape.md) — Phase-7 dispatch brief.
- [`architectures/v3/backfill-notes/bf-s.md`](bf-s.md) — exemplar (BF-S).

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

- U-A common-substrate ADRs: [0010-0017](../../../docs/adr/) (P-01 / P-02 / P-05 / P-06 / P-07 / P-08 / P-14 / P-22).
- U-A discipline ADRs: [0018-0027](../../../docs/adr/) (all 10 disciplines).
- U-A framework + per-variant pairs: [0028](../../../docs/adr/0028-p-19-eligibility-regime-classifier.md) ↔ [0050](../../../docs/adr/0050-p-19-variant-u-a-interval-kind.md); [0029](../../../docs/adr/0029-p-28-typed-object-store.md) ↔ [0051](../../../docs/adr/0051-p-28-variant-u-a-interval-envelope.md); [0030](../../../docs/adr/0030-p-29-policy-mediator.md) ↔ [0052](../../../docs/adr/0052-p-29-variant-u-a-interval-policy.md); [0036](../../../docs/adr/0036-p-30-event-registrar-substrate.md) ↔ [0053](../../../docs/adr/0053-p-30-variant-u-a-re-entry.md).

**Constraints / decisions:**

- [`architectures/v3/constraints-extracted.md`](../constraints-extracted.md) — UC1-UC8 user constraints (source of known-rejected v3 item flags).
- [`architectures/v3/decisions-captured.md`](../decisions-captured.md) — DEC-1 / DEC-1.a / DEC-2 (escrow framing demoted to methodology).
- [`architectures/v3/phase-6-verification-findings.md`](../phase-6-verification-findings.md) — Finding-2 source of ADR-0036 framing characterization.
