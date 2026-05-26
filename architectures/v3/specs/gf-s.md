---
candidate: gf-s
candidate-name: Greenfield, substrate-first
mandate-scope: greenfield
based-on-commit: c54daf1
based-on-date: 2026-05-26
mandate-fit:
  initial-spec: greenfield
  refactor: greenfield
  mvp: greenfield
  post-mvp-evolution: greenfield
  regression-fix: greenfield
---

# Architecture spec — GF-S (Greenfield, substrate-first)

## §0 ADR-citation index

| ADR ID | Title | Layer | Variant of | Citing § |
|---|---|---|---|---|
| 0010 | P-01 Sandbox runtime | common-substrate | — | §2, §3, §4 |
| 0011 | P-02 Cost ceilings | common-substrate | — | §2, §3, §4 |
| 0012 | P-05 Trajectory capture | common-substrate | — | §2, §3, §4 |
| 0013 | P-06 Watchdog tiers | common-substrate | — | §2, §3, §4 |
| 0014 | P-07 Telemetry ingestor | common-substrate | — | §2, §3, §4 |
| 0015 | P-08 Scenario storage with runner contract | designed-system-substrate | — | §2, §3, §4 |
| 0016 | P-14 Judge router | common-substrate | — | §2, §3 |
| 0017 | P-22 Polyglot codebase index | common-substrate | — | §2 |
| 0018 | Discipline — bias guard | discipline | — | §4 |
| 0019 | Discipline — cognitive escrow | discipline | — | §4 |
| 0020 | Discipline — cost ceiling | discipline | — | §4 |
| 0021 | Discipline — holdout | discipline | — | §4 |
| 0022 | Discipline — honesty | discipline | — | §4 |
| 0023 | Discipline — knowledge promotion | discipline | — | §4 |
| 0024 | Discipline — regime classification | discipline | — | §4 |
| 0025 | Discipline — scoping | discipline | — | §4 |
| 0026 | Discipline — three-loop | discipline | — | §4 |
| 0027 | Discipline — trifecta closure | discipline | — | §4 |
| 0028 | P-19 Eligibility / regime classifier framework | common-substrate | — | §2, §3 |
| 0032 | P-12 Deterministic linter framework | designed-system-substrate | — | §2, §3 |
| 0037 | GF-S P-10 coordination medium | orphan-substrate | — | §2, §3 |
| 0038 | GF-S P-15 four-guard mediator | orphan-substrate | — | §2, §3, §4 |
| 0039 | GF-S P-19 variant — work-unit-class feature source | per-variant-substrate | 0028 | §2, §3, §4 |

**Framework + per-variant pairing check.** GF-S claims the P-19 framework ([ADR 0028](../../../docs/adr/0028-p-19-eligibility-regime-classifier.md)) and pairs it with its work-unit-class per-variant ADR ([ADR 0039](../../../docs/adr/0039-p-19-variant-gf-s-work-unit-class.md)) per [AGENTS-MD-a9fb7b42f8](../../../AGENTS.md#framework-adr-scope-boundary-discipline). GF-S does **not** claim the P-28 / P-29 / P-30 frameworks (ADRs 0029 / 0030 / 0036): its S7 coordination medium is [P-10 (ADR 0037)](../../../docs/adr/0037-p-10-coordination-medium.md), not a typed-object store; it carries no policy-mediator or event-registrar primitive. Per the [Phase-4.2 overlap.md P-19 verdict](../primitives/overlap.md#p-19-eligibility--regime-classifier--four-contested-variants), GF-S's variant is one of four sharing a common decision-engine substrate but with distinct feature-source and output-regime layers.

## §1 Overview

**Mandate.** Greenfield. GF-S explicitly disclaims unified-mandate reach per [track §6 "Not a unified both-mandates architecture"](../tracks/greenfield-substrate-first.md#6-what-this-track-is-not-trying-to-be); the architecture commits to greenfield's defining property of [UC4 spec-malleability](../../../research/00-brief-v3.md) and treats brownfield as a different mandate requiring a different framing.

**Axis.** Substrate-derives: substrate primitives are the primary organising principle, methodology is the thinnest layer that drives the primitives. The "how" (substrate semantics) is upstream of the "what" (cycle methodology). Each of S1–S9 commits only to primitive *semantics* that are *spec-shape-agnostic* — a sandbox is a sandbox whether the spec is one sentence or twenty pages.

**Entry-mode.** Greenfield day-0 cold-start with an operator-authored intent block + ≥3 region-shaped scenarios (per [track §5.2 bootstrap protocol](../tracks/greenfield-substrate-first.md#52-the-bootstrap-protocol)). No legacy codebase; no Codebase Model dependency.

**Methodology summary.** Deliberately thin 8-step per-cycle protocol composing the nine substrate primitives (S1–S9). The unit-of-work shape, agent topology, spec format choice (prose / EARS / typed-object), and knowledge-accumulation pattern are *methodology choices* the substrate accommodates without privileging. Day-0 work units default to `augmentation-required` per [ADR 0039](../../../docs/adr/0039-p-19-variant-gf-s-work-unit-class.md) OPA hard-floor; transition to `automation-eligible` is *substrate-measured* from scenario-set saturation + cross-family judge agreement + Patrol absence-of-drift.

**Load-bearing claim.** For greenfield specifically, substrate-first ordering is defensible because the substrate's invariants (sandbox shape, trajectory format, cost-ceiling enforcement, watchdog tiers, four-guard mediator, regime classifier) are the parts that *do not move during spec refinement* — exactly the parts UC4 names as stable while the spec is malleable. CTR-C2 ("substrate-heavy may not serve both mandates") is the shape GF-S defends for greenfield, not avoids.

## §2 Substrate composition

GF-S names nine substrate slots S1–S9 covered by twelve ADRs (8 common + 1 framework + 1 designed-system engine + 2 GF-S orphans + 1 per-variant). The slot-to-ADR map and the load-bearing contracts:

**Commodity common substrate (S1, S3, S4, S5, S6).** [P-01 sandbox (ADR 0010)](../../../docs/adr/0010-p-01-sandbox-runtime.md) is S1: deny-all default with per-cycle allow-list. Production-credentialled scissors per [F44](../failure-modes-v3.md) are *substrate-disabled by default* for greenfield because there is no production yet; "dreaming"-class long-running research is a distinct capability profile gated separately, resolving [CTR-C9](../contradictions.md) at the substrate layer. [P-05 trajectory capture (ADR 0012)](../../../docs/adr/0012-p-05-trajectory-capture.md) is S3: per-event sub-ms content-addressed append-only persistence; the only artifact that survives [F14 forensic reconstruction widening](../failure-modes-v3.md) when UC4 spec-malleability rewrites the architecture mid-flight. [P-02 cost ceilings (ADR 0011)](../../../docs/adr/0011-p-02-cost-ceilings.md) is S4: hard multi-axis (tokens / wall-clock / tool-call-count); substrate kills the cycle at ceiling — no graceful-degradation mode (refuses the [CTR-E6](../contradictions.md) utility-tax pattern). [P-06 watchdog tiers (ADR 0013)](../../../docs/adr/0013-p-06-watchdog-tiers.md) is S5: Daemon (seconds) / Triage (seconds-minutes) / Patrol (hours) — Patrol guards operator-declared *invariants* (substrate-stored) rather than historical baselines because no baselines exist at day-0. [P-14 judge router (ADR 0016)](../../../docs/adr/0016-p-14-judge-router.md) is S6: provider-family-diverse typed dispatch; the substrate does not pick which judge shape is right (that is methodology), but it makes the choice typed, auditable, and reversible — resolves [CTR-C4](../contradictions.md) (RouterLLM unification vs Attractor per-provider non-unification) at the substrate layer.

**Telemetry + index commodity substrate.** [P-07 telemetry ingestor (ADR 0014)](../../../docs/adr/0014-p-07-telemetry-ingestor.md) consumes the typed envelopes emitted by the four-guard mediator (one envelope per gate decision, PASS or FAIL) and the perimeter-typing capability-edge traces; this feeds the [F12 / F33 / F44](../failure-modes-v3.md) lethal-trifecta detector pipelines. [P-22 polyglot codebase index (ADR 0017)](../../../docs/adr/0017-p-22-polyglot-codebase-index.md) is consumed *only* for syntactic / symbol-graph analysis of agent-produced code as it accretes within the greenfield cycle — not as a Codebase-Model input the way BF-L's P-26 uses it.

**Designed-system common substrate (S2).** [P-08 scenario storage with runner contract (ADR 0015)](../../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md) is S2: append-only scenario store with substrate-enforced training/holdout partition + deterministic replay (per the [Phase-4.2 P-08↔P-09 absorption](../primitives/overlap.md#p-08--p-09--held-out-runner--scenario-storage-collapse) which folded P-09 into P-08 as the read-API contract). Per the [Phase-4.2 verdict](../primitives/overlap.md#p-08--p-09--held-out-runner--scenario-storage-collapse) folded into ADR 0015:

> **"P-09 ABSORBS INTO P-08."** P-09 is the **read-API contract** on P-08's substrate; not a separate primitive. The held-out runner is `P-08.read(partition='holdout', judge-role-token=...) → ScenarioResult`.

For greenfield, S2 is the *only* ground-truth signal that survives the absence of an existing codebase (per [failure-modes §7 force-1: out-of-distribution ground truth](../failure-modes-v3.md)) — the substrate must enforce builder-blindness or [F28 holdout leakage](../failure-modes-v3.md) becomes ambient. [CTR-B5](../contradictions.md) (scenarios outside codebase vs brownfield-inverted) does not bite greenfield: the codebase does not yet exist to inherit from.

**Orphan substrate (S7, S8) — single-candidate primitives.**

- **S7 = P-10 coordination medium ([ADR 0037](../../../docs/adr/0037-p-10-coordination-medium.md)).** GF-S is the only candidate naming P-10; per ADR 0037 it is built as Git-LFS content-addressed object store + signed fast-forward-only Git refs `refs/factory/events/<stream>` for the typed event log. Reachable from any GitHub-Actions runner without provisioning a broker (resolves [CTR-C7](../contradictions.md) mail-bus-vs-CI-friendly at substrate level by siding CI-friendly). Signing discipline ([F32 mail-injection](../failure-modes-v3.md)) satisfied by `git verify-commit` on every event-log append.

- **S8 = P-15 four-guard mediator ([ADR 0038](../../../docs/adr/0038-p-15-four-guard-mediator.md)).** Four typed guards behind one fail-closed gate: (1) GtWR vocabulary lint via [P-12 (ADR 0032)](../../../docs/adr/0032-p-12-deterministic-linter-framework.md) loaded with the EARS+GtWR rule pack (the [overlap.md P-12↔P-16 absorption verdict](../primitives/overlap.md#p-12--p-16--deterministic-linter-framework--earsgtwr-rule-library-absorption) folded P-16 into P-12 as configuration); (2) contradiction-detector — 3-of-N family-diverse ensemble dispatched through P-14 with three-valued PASS/FAIL/UNDETERMINED sub-verdict; (3) requirement-count budgeter — deterministic P-12 rule with thresholds drawn from the cycle manifest as a P-02 cost-ceiling class; (4) CaMeL-class perimeter typing on spec-derived tool-call edges. Composition is **AND across guards, fail-closed by default**, with a typed envelope `{gtwr, contradiction, req-count, perimeter}` emitted to P-07 telemetry on every decision (PASS envelopes auditable, not just FAILs). **Four guards, full stop** per [substrate-requirements §3](../substrate-requirements/gf-s.md#3-candidate-specific-contracts-on-each-primitive) — the substrate refuses a fifth guard at this surface ([F52](../failure-modes-v3.md) tempting-wrong-hybrid defense at design-review time, not runtime). Contradiction-detector reliability ceiling (Larbi single-judge MCC ≤ 0.55 against [F27/F48](../failure-modes-v3.md) shared-pretraining collusion) is **partial-RG** per [substrate-requirements §2](../substrate-requirements/gf-s.md#2-rg-primitives) — accepted-as-RG on the sub-component, with ensemble N / family-rotation / quorum / UNDETERMINED-to-Patrol escalation exposed as first-class parameters for Phase-8 lean-eval pressure-test.

**Framework + per-variant (S9).**

- **S9 = P-19 eligibility classifier.** Framework: [ADR 0028](../../../docs/adr/0028-p-19-eligibility-regime-classifier.md) records the shared decision-table engine (Drools / OPA Rego) + LLM-judge fallback via P-14 + OPA hard-floor post-check. GF-S variant: [ADR 0039](../../../docs/adr/0039-p-19-variant-gf-s-work-unit-class.md) registers GF-S's feature schema as a typed five-tuple `(intent_block_fields_touched, declared_stakes, scenario_set_saturation, recent_cross_family_judge_agreement, bar_set_parameters)` and the output regime enum as `automation-eligible / augmentation-required / escalate`. The [Phase-4.2 overlap verdict on P-19](../primitives/overlap.md#p-19-eligibility--regime-classifier--four-contested-variants) is verbatim:

> **"Verdict: SAME primitive (P-19 classifier framework), DISTINCT feature sources + distinct output regime sets. All four share the construction recipe (Drools/OPA Rego decision tables + LLM-judge fallback via P-14 + OPA hard-floor post-check per [P-19 sketch](../../architectures/v3/primitives/P-19-eligibility-regime-classifier.md)). The differences are at the *feature engineering* layer and the *output enum* layer, not the *decision-engine* layer."**

GF-S-specific OPA hard floors fixed in ADR 0039: (a) cold-start cycle count `< N ⇒ augmentation-required` ([F25 design starvation](../failure-modes-v3.md) mitigation — substrate refuses to lights-out a cold-start factory); (b) `declared_stakes = caremark ⇒` forbid `automation-eligible` ([F57 design-authority erosion](../failure-modes-v3.md)); (c) `scenario_set_saturation < S_min ⇒ augmentation-required` (F25); (d) RSI-flagged classes ⇒ forbid `automation-eligible` ([F43 RSI board-visibility gap](../failure-modes-v3.md)).

**X_UNM_B articulation.** N/A — GF-S is greenfield-only per [substrate-requirements §4](../substrate-requirements/gf-s.md#4-x_unm_b-articulation) and does not need to acquire a Codebase Model from legacy artifacts because no legacy artifacts exist at greenfield day 0.

## §3 Methodology shape

**Per-cycle protocol (the thin methodology).** Eight steps per [track §1 Methodology layer](../tracks/greenfield-substrate-first.md#methodology-layer-deliberately-thin):

1. **Intent + scenarios ingest.** Operator (or upstream cycle) authors a 9-field El-Kaim-style intent block and ≥3 region-shaped scenarios; both are stored as typed objects in [P-08 (ADR 0015)](../../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md) with substrate-enforced builder-blindness.
2. **Four-guard gate.** The [P-15 mediator (ADR 0038)](../../../docs/adr/0038-p-15-four-guard-mediator.md) runs on the inputs — GtWR lint + contradiction-detector ensemble + req-count budgeter + perimeter typing. Fail-closed: cycle does not start if any guard fails.
3. **Eligibility classification.** The [P-19 variant (ADR 0039)](../../../docs/adr/0039-p-19-variant-gf-s-work-unit-class.md) extracts the five-feature work-unit-class vector, writes it to [P-05 trajectory (ADR 0012)](../../../docs/adr/0012-p-05-trajectory-capture.md), and hands it to the [ADR 0028 framework](../../../docs/adr/0028-p-19-eligibility-regime-classifier.md) decision-table engine. Output regime ∈ {`automation-eligible`, `augmentation-required`, `escalate`} drives the next two steps.
4. **Sandbox open.** [P-01 (ADR 0010)](../../../docs/adr/0010-p-01-sandbox-runtime.md) opens with the capability profile selected by the eligibility regime (`escalate` ⇒ operator-required; `augmentation-required` ⇒ supervised closure; `automation-eligible` ⇒ deny-all default with intent-declared allow-list).
5. **Build under watchdog.** Build agent runs under [P-06 (ADR 0013)](../../../docs/adr/0013-p-06-watchdog-tiers.md) Daemon/Triage/Patrol with [P-05 trajectory](../../../docs/adr/0012-p-05-trajectory-capture.md) capture and [P-02 ceilings (ADR 0011)](../../../docs/adr/0011-p-02-cost-ceilings.md) substrate-enforced.
6. **Judge against holdout.** [P-14 (ADR 0016)](../../../docs/adr/0016-p-14-judge-router.md) runs against [P-08](../../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md) holdout scenarios; methodology declares which judge shape (same-model-different-task / cross-model / same-model-different-role) — substrate logs the choice.
7. **Coordination write.** [P-10 (ADR 0037)](../../../docs/adr/0037-p-10-coordination-medium.md) writes outputs as Git-LFS content-addressed artifacts + a signed-commit event on `refs/factory/events/<stream>`.
8. **Patrol audit.** [P-06 (ADR 0013)](../../../docs/adr/0013-p-06-watchdog-tiers.md) tier-3 audits cross-cycle against operator-declared invariants ([F55 behavioural drift](../failure-modes-v3.md), [F57 design-authority erosion](../failure-modes-v3.md), [F8 stale-knowledge inversion](../failure-modes-v3.md)).

**Regime structure.** Three regimes named in the P-19/GF-S enum: `automation-eligible` (lights-out per UC1), `augmentation-required` (per-cycle human review), `escalate` (operator must design the work unit before the cycle starts). The substrate enforces the regime: an `augmentation-required` unit *cannot bypass* the human-review gate; an `automation-eligible` unit *cannot summon* the human (it escalates to Patrol, which then summons). This is the substrate-level resolution of [CTR-A4 / OQ-B1](../contradictions.md) lights-out vs L5: lights-out applies *only* to the classifier-named `automation-eligible` surface; methodology + operator policy controls which work-unit-classes are in that surface.

**Work-unit definition.** *Methodology choice, not substrate commitment.* The substrate accommodates issue / change-request / candidate / first-feature shapes without privileging any. The classifier types the work unit by *work-unit class* (the spec-shape-agnostic equivalence class assigned by intent-block typing per [ADR 0039](../../../docs/adr/0039-p-19-variant-gf-s-work-unit-class.md)), not by topology shape.

**Distinctive methodology decisions.** Three:

- **Spec-shape agnosticism.** Methodology may use prose / EARS / typed-object / DOT graph; substrate has no opinion. The intent block (per [report 14](../../../research/14-el-kaim-book-intent-and-spec-authorship.md)) is the slow layer Patrol guards; the spec body around it is the fast layer that can churn arbitrarily without invalidating substrate guarantees. This is [CTR-B6](../contradictions.md) (El-Kaim intent-stability vs UC4 spec-malleability) resolved by slow/fast pace-layer split.

- **Day-0 default `augmentation-required` for all work units** ([ADR 0039](../../../docs/adr/0039-p-19-variant-gf-s-work-unit-class.md) OPA floor (a)). The substrate refuses to lights-out a cold-start factory ([F25 design starvation](../failure-modes-v3.md) mitigation). Transition to `automation-eligible` is substrate-measured from three signals: scenario-set saturation (S2), judge stability across model families (S6), Patrol absence-of-drift (S5 tier-3) — *the operator does not declare the transition*.

- **Methodology layer takes no opinion on agent topology.** Single-agent / panel / tournament / population are all methodology choices the substrate accommodates through P-10's coordination medium (which scales down to one log-reader and up to multi-agent merge through a Refinery-like resolver as a methodology-layer primitive, not substrate).

## §4 Discipline binding

GF-S binds 9 of the 10 discipline ADRs (0018-0027); cognitive-escrow is bound at the substrate-cadence layer with a methodology-layer carve-out. Per-discipline:

- **Bias guard ([ADR 0018](../../../docs/adr/0018-discipline-bias-guard.md)).** Bound at [P-14 judge router (ADR 0016)](../../../docs/adr/0016-p-14-judge-router.md) and at the four-guard mediator's contradiction-detector (guard 2, [ADR 0038](../../../docs/adr/0038-p-15-four-guard-mediator.md)). 3-of-N family-diverse ensemble agreement is the substrate's bias-guard surface; the [F27 / F48](../failure-modes-v3.md) shared-pretraining collusion residual is the partial-RG carry surfaced to Phase-8.

- **Cognitive escrow ([ADR 0019](../../../docs/adr/0019-discipline-cognitive-escrow.md)).** Bound at [P-05 trajectory (ADR 0012)](../../../docs/adr/0012-p-05-trajectory-capture.md) sub-ms persist cadence + [P-06 Patrol tier (ADR 0013)](../../../docs/adr/0013-p-06-watchdog-tiers.md). Per [DEC-2](../decisions-captured.md), cognitive-escrow demoted from substrate to methodology — but the *interval-as-design-site* primitives ([report 30 §4](../../../research/30-cognitive-escrow.md)) remain substrate-typed (the prompt→response interval is a designed substrate surface).

- **Cost ceiling ([ADR 0020](../../../docs/adr/0020-discipline-cost-ceiling.md)).** Bound at [P-02 (ADR 0011)](../../../docs/adr/0011-p-02-cost-ceilings.md) and per-axis at the four-guard mediator (req-count guard 3 shares the substrate's per-cycle budget plumbing via [ADR 0038](../../../docs/adr/0038-p-15-four-guard-mediator.md)). [CTR-E1](../contradictions.md) (Cherny $100K/mo vs independent $500-$5000/day) is substrate-configurable; the *non-optional* part survives.

- **Holdout ([ADR 0021](../../../docs/adr/0021-discipline-holdout.md)).** Bound at [P-08 (ADR 0015)](../../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md) substrate-typed builder-blindness (D-4). For greenfield this is the *only* coherent option since there is no codebase to inherit from. The Phase-4.2 P-09 absorption folded the held-out runner contract into P-08; substrate enforces the boundary.

- **Honesty ([ADR 0022](../../../docs/adr/0022-discipline-honesty.md)).** Bound at the four-guard mediator's typed envelope to P-07 telemetry — PASS *and* FAIL envelopes are auditable per [ADR 0038](../../../docs/adr/0038-p-15-four-guard-mediator.md), removing the opacity that makes the gate review-worthy. Coupled with [P-05 trajectory](../../../docs/adr/0012-p-05-trajectory-capture.md) which exposes spec→artifact divergence ([F9 spec overfitting](../failure-modes-v3.md)) as detectable even when not preventable.

- **Knowledge promotion ([ADR 0023](../../../docs/adr/0023-discipline-knowledge-promotion.md)).** Bound *thinly* — substrate provides the trajectory and event log; methodology decides which observations promote. GF-S's substrate-first stance means knowledge-accumulation pattern (eager / lazy / typed) is explicitly a methodology choice on top.

- **Regime classification ([ADR 0024](../../../docs/adr/0024-discipline-regime-classification.md)).** Bound at [P-19/GF-S variant (ADR 0039)](../../../docs/adr/0039-p-19-variant-gf-s-work-unit-class.md) per the framework decision in [ADR 0028](../../../docs/adr/0028-p-19-eligibility-regime-classifier.md). GF-S declares per-variant feature source (the five-feature work-unit-class vector) + regime set + hard-floor table per the discipline contract. [F57 design-authority erosion](../failure-modes-v3.md) (convenience reclassifies stakes) is mitigated at substrate by versioned-config Rego policies that Patrol diffs across versions.

- **Scoping ([ADR 0025](../../../docs/adr/0025-discipline-scoping.md)).** Bound at the [P-15 four-guard mediator's req-count budgeter](../../../docs/adr/0038-p-15-four-guard-mediator.md) (guard 3 — Yang/Llama ≤10-20 simultaneous-requirement ceiling per [F36 instruction-following ceiling](../failure-modes-v3.md)) and at [P-02 cost ceilings (ADR 0011)](../../../docs/adr/0011-p-02-cost-ceilings.md).

- **Three-loop ([ADR 0026](../../../docs/adr/0026-discipline-three-loop.md)).** Bound thinly — the substrate hosts whatever evolution-state methodologies need (P-05 trajectory + P-10 typed-event log per [ADR 0037](../../../docs/adr/0037-p-10-coordination-medium.md)). [CTR-C3](../contradictions.md) methodology-evolution-as-primitive is resolved methodology-side per [track §2.H](../tracks/greenfield-substrate-first.md). GF-S does not embed a meta-loop; it provides the substrate surfaces methodologies can compose into one.

- **Trifecta closure ([ADR 0027](../../../docs/adr/0027-discipline-trifecta-closure.md)).** Bound at [P-01 sandbox (ADR 0010)](../../../docs/adr/0010-p-01-sandbox-runtime.md) closure-first + [P-15 perimeter typing (ADR 0038)](../../../docs/adr/0038-p-15-four-guard-mediator.md) guard 4 (CaMeL-class at declaration-time; P-25 runtime perimeter re-enforces at call-time per [ADR 0038 decision](../../../docs/adr/0038-p-15-four-guard-mediator.md)). Probabilistic guards ([F33 / F51 Ashby-deficient](../failure-modes-v3.md)) explicitly *not* trusted as primary closure per [F52 tempting-wrong-hybrid](../failure-modes-v3.md) discipline.

**Disciplines GF-S is silent on.** None — GF-S carries all 10. The cognitive-escrow demotion (per [DEC-2](../decisions-captured.md)) is a *layer* re-assignment, not silence.

## §5 Mandate fit

GF-S's mandate-fit YAML restated per work-unit-class. Per [DEC-2](../decisions-captured.md), mandate-fit is declared per (architecture × work-unit-class). GF-S is a mandate-specific candidate (greenfield-only); every work-unit-class is fit as `greenfield`.

- **initial-spec: greenfield.** Day-0 initial-spec authoring is the canonical GF-S work-unit-class — operator authors the 9-field intent block, [P-15 (ADR 0038)](../../../docs/adr/0038-p-15-four-guard-mediator.md) lints it, [P-08 (ADR 0015)](../../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md) stores the scenarios, [P-19/GF-S (ADR 0039)](../../../docs/adr/0039-p-19-variant-gf-s-work-unit-class.md) defaults to `augmentation-required`. Falsifying scenario: if initial-spec cycles fail because the operator cannot author the intent block under the four-guard lint (R7/R8/R9 violations exceed threshold and the operator cannot iterate to PASS), the substrate-enforced intent-discipline precondition is wrong — surfaced as [substrate-requirements §5 Phase-8 carry](../substrate-requirements/gf-s.md#5-open-carries) and [track §7 OQ-8 operator-illiteracy](../tracks/greenfield-substrate-first.md#7-open-questions-surfaced-by-this-track).

- **refactor: greenfield.** Refactor within a greenfield factory (after some code accretes but before brownfield-mode acquisition) is dispatched by the P-19 classifier: low-distance refactors against accumulated invariants route to `automation-eligible` after scenario-saturation thresholds clear; high-distance refactors route to `augmentation-required`. Supporting substrate evidence: [ADR 0017 P-22](../../../docs/adr/0017-p-22-polyglot-codebase-index.md) (syntactic / symbol-graph analysis on within-factory code), [ADR 0039](../../../docs/adr/0039-p-19-variant-gf-s-work-unit-class.md) (work-unit-class typing). Falsifying scenario: if refactor work units on within-factory code routinely escalate because the classifier cannot distinguish refactor-class from feature-class on the work-unit-class feature vector alone, the five-feature schema is under-parametrised.

- **mvp: greenfield.** MVP authoring is the canonical greenfield trajectory (day-0 → day-N) per [track §5.3](../tracks/greenfield-substrate-first.md#53-day-0--day-n-trajectory). Substrate-measured transition signals (scenario-set saturation + judge stability + Patrol absence-of-drift) drive the regime flip per work-unit-class. Falsifying scenario: if MVP cycles never accumulate enough scenarios to flip *any* work-unit-class to `automation-eligible` within a Phase-8-realistic timescale, the substrate-measured-transition claim collapses; cold-start would be the steady-state and GF-S's substrate-first ordering would over-budget for the lights-out surface that never materialises.

- **post-mvp-evolution: greenfield.** Post-MVP cycles operate against the thickened scenario set + accumulated invariants + Patrol-monitored distribution. Same substrate, same classifier, regime distribution shifted toward `automation-eligible`. Falsifying scenario: if post-MVP cycles routinely require fundamentally different primitives (a Codebase-Model-equivalent acquired from the now-extant code), GF-S would have *become* brownfield in practice, refuting the entry-mode-not-temporal framing per [DEC-1.b](../decisions-captured.md).

- **regression-fix: greenfield.** Regression fixes in a greenfield factory are dispatched by the classifier: the failing scenario *is* the holdout anchor, the fix's work-unit-class is regression-class, and the OPA hard-floor on `declared_stakes` controls escalation. Substrate evidence: [ADR 0015 holdout contract](../../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md) + [ADR 0039 OPA floors](../../../docs/adr/0039-p-19-variant-gf-s-work-unit-class.md). Falsifying scenario: if regression-fix cycles routinely classify to `escalate` (operator must design the work unit), the regression-class feature vector is under-discriminated against feature-class.

**DEC-1.a falsifier-discipline observation.** GF-S declares `greenfield` on all 5 work-unit-classes — *no* `both` cells. This is evidence *for* the [DEC-1.a working hypothesis](../decisions-captured.md) ("no methodology serves both mandates"): GF-S explicitly disclaims brownfield reach per [track §6](../tracks/greenfield-substrate-first.md#6-what-this-track-is-not-trying-to-be), and the substrate's S2 holdout-discipline + S9 work-unit-class feature source are *only* coherent at greenfield day-0 where no Codebase Model exists.

## §6 Open carries

Surfaced into Phase 7 (back-fill audit) / Phase 8 (lean-eval) / future ADRs:

- **F40 last-mile drift (accepted-open).** Per [substrate-requirements §5](../substrate-requirements/gf-s.md#5-open-carries) and [track §7 OQ-5](../tracks/greenfield-substrate-first.md#7-open-questions-surfaced-by-this-track): the substrate enables many starts and tracks last-mile state, but bridging the "agent-shaped middle vs manual fit-and-finish tail" requires methodology choices the substrate explicitly does not make. **Status: substrate-unaddressed; the strongest standing critique of the substrate-first axis. Carries forward to Phase-8 methodology lean-eval, not Phase-5 ADR.**

- **P-15 contradiction-detector reliability (Phase-8 lean-eval candidate).** Per [substrate-requirements §2](../substrate-requirements/gf-s.md#2-rg-primitives): does 3-of-N family-diverse agreement raise effective MCC above Larbi's single-judge ≤ 0.55 ceiling against F27/F48 shared-pretraining collusion? Substrate exposes ensemble N / family-rotation / quorum / UNDETERMINED-to-Patrol as first-class parameters for the sweep. **Status: Phase-8 lean-eval; the load-bearing GF-S lean-eval candidate.**

- **Cost-stacking math for the four-guard mediator (accepted-open; CFO flag).** Per [registry GF-S entry](../candidate-registry.md#gf-s--greenfield-substrate-first) and [substrate-requirements §5](../substrate-requirements/gf-s.md#5-open-carries): cost compounding of four-guards × every-cycle × ensemble-fanout against P-02 ceilings is owed. **Status: Phase-5/8 architecture-spec time pressure-test; substrate exposes the parameters.**

- **S9 minimal viable scenario-set size N (Phase-8 lean-eval).** Per [track §7 OQ-1](../tracks/greenfield-substrate-first.md#7-open-questions-surfaced-by-this-track): the substrate measures the regime transition but the threshold parameter `S_min` is unspecified by the corpus. **Status: Phase-8 lean-eval empirical sweep.**

- **F51 recursion — is S9 itself an LLM-judge primitive (Phase-8 lean-eval)?** Per [track §7 OQ-3](../tracks/greenfield-substrate-first.md#7-open-questions-surfaced-by-this-track): if the classifier's LLM fallback is itself a probabilistic guard, the Ashby-deficiency critique recurses. ADR 0039 mitigates by making the rules-only path the day-0 default (deterministic) and degrading LLM fallback gracefully; the recursion may still bite at steady-state. **Status: Phase-8 lean-eval.**

- **Day-0 operator-intent-illiteracy (Phase-7 / Phase-8 carry).** Per [track §7 OQ-8](../tracks/greenfield-substrate-first.md#7-open-questions-surfaced-by-this-track): can the substrate scaffold operator intent richness, or is this an irreducible operator-skill requirement? GF-S currently requires operator-authored intent at day-0; STIR-in-the-interval primitives ([report 30 §4](../../../research/30-cognitive-escrow.md)) are one direction but not specified. **Status: Phase-7 back-fill check on Compound-Knowledge / Crucible alternatives.**

- **CTR-C5 substrate-stack binding (deferred to Phase-5/architecture).** GF-S refused to bind to OpenHands+Overstory vs Gas City per [track §6](../tracks/greenfield-substrate-first.md#6-what-this-track-is-not-trying-to-be). **Status: future ADR carry; not Phase-6 closure.**

## §7 References

**ADR set (this spec's binding inputs):**

- Common substrate: [ADR 0010](../../../docs/adr/0010-p-01-sandbox-runtime.md), [ADR 0011](../../../docs/adr/0011-p-02-cost-ceilings.md), [ADR 0012](../../../docs/adr/0012-p-05-trajectory-capture.md), [ADR 0013](../../../docs/adr/0013-p-06-watchdog-tiers.md), [ADR 0014](../../../docs/adr/0014-p-07-telemetry-ingestor.md), [ADR 0015](../../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md), [ADR 0016](../../../docs/adr/0016-p-14-judge-router.md), [ADR 0017](../../../docs/adr/0017-p-22-polyglot-codebase-index.md).
- Designed-system / framework substrate: [ADR 0028 (P-19 framework)](../../../docs/adr/0028-p-19-eligibility-regime-classifier.md), [ADR 0032 (P-12)](../../../docs/adr/0032-p-12-deterministic-linter-framework.md).
- Orphan substrate (GF-S-specific): [ADR 0037 (GF-S P-10 coordination medium)](../../../docs/adr/0037-p-10-coordination-medium.md), [ADR 0038 (GF-S P-15 four-guard mediator)](../../../docs/adr/0038-p-15-four-guard-mediator.md).
- Per-variant substrate (GF-S P-19): [ADR 0039 (GF-S P-19 variant — work-unit-class feature source)](../../../docs/adr/0039-p-19-variant-gf-s-work-unit-class.md).
- Discipline: [ADR 0018](../../../docs/adr/0018-discipline-bias-guard.md), [ADR 0019](../../../docs/adr/0019-discipline-cognitive-escrow.md), [ADR 0020](../../../docs/adr/0020-discipline-cost-ceiling.md), [ADR 0021](../../../docs/adr/0021-discipline-holdout.md), [ADR 0022](../../../docs/adr/0022-discipline-honesty.md), [ADR 0023](../../../docs/adr/0023-discipline-knowledge-promotion.md), [ADR 0024](../../../docs/adr/0024-discipline-regime-classification.md), [ADR 0025](../../../docs/adr/0025-discipline-scoping.md), [ADR 0026](../../../docs/adr/0026-discipline-three-loop.md), [ADR 0027](../../../docs/adr/0027-discipline-trifecta-closure.md).

**Supporting docs:**

- [GF-S candidate-registry entry](../candidate-registry.md#gf-s--greenfield-substrate-first)
- [GF-S substrate-requirements summary](../substrate-requirements/gf-s.md)
- [Greenfield-substrate-first track sketch](../tracks/greenfield-substrate-first.md)
- [Phase-4.2 overlap.md P-19 verdict](../primitives/overlap.md#p-19-eligibility--regime-classifier--four-contested-variants)
- [Phase-4.2 overlap.md P-08↔P-09 absorption verdict](../primitives/overlap.md#p-08--p-09--held-out-runner--scenario-storage-collapse)
- [Phase-4.2 overlap.md P-12↔P-16 absorption verdict](../primitives/overlap.md#p-12--p-16--deterministic-linter-framework--earsgtwr-rule-library-absorption)
- [DEC-1.a unification-verdict working hypothesis](../decisions-captured.md)
- [DEC-2 mandate-fit-per-(architecture × work-unit-class)](../decisions-captured.md)
- [auto-006 Phase-6 dispatch-shape brief](../decisions/auto-006-phase-6-dispatch-shape.md)
- [U-C exemplar spec](u-c.md)
