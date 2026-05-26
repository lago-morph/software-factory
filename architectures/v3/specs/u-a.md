---
candidate: u-a
candidate-name: Escrow-Graph Factory
mandate-scope: unified-attempt
based-on-commit: c54daf1
based-on-date: 2026-05-26
mandate-fit:
  initial-spec: both
  refactor: both
  mvp: greenfield
  post-mvp-evolution: both
  regression-fix: both
---

# Architecture spec — U-A (Escrow-Graph Factory)

## §0 ADR-citation index

| ADR ID | Title | Layer | Variant of | Citing § |
|---|---|---|---|---|
| 0010 | P-01 Sandbox runtime | common-substrate | — | §2, §3, §4 |
| 0011 | P-02 Cost ceilings | common-substrate | — | §2, §3, §4 |
| 0012 | P-05 Trajectory capture | common-substrate | — | §2, §3, §4 |
| 0013 | P-06 Watchdog tiers | common-substrate | — | §2, §3, §4 |
| 0014 | P-07 Telemetry ingestor | common-substrate | — | §2, §3 |
| 0015 | P-08 Scenario storage with runner contract | designed-system-substrate | — | §2, §4 |
| 0016 | P-14 Judge router | common-substrate | — | §2, §3, §4 |
| 0017 | P-22 Polyglot codebase index | common-substrate | — | §2, §3 |
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
| 0050 | U-A P-19 variant — interval-kind feature source | per-variant-substrate | 0028 | §2, §3, §5 |
| 0029 | P-28 Typed-object store framework | common-substrate | — | §2, §3 |
| 0051 | U-A P-28 variant — interval-typed envelope | per-variant-substrate | 0029 | §2, §3, §5 |
| 0030 | P-29 Policy mediator framework | common-substrate | — | §2, §3 |
| 0052 | U-A P-29 variant — interval-policy DSL | per-variant-substrate | 0030 | §2, §3, §4 |
| 0036 | P-30 Event registrar substrate | common-substrate | — | §2, §3 |
| 0053 | U-A P-30 variant — re-entry-interval state machine | per-variant-substrate | 0036 | §2, §3, §5 |

**Framework + per-variant pairing check.** Per [AGENTS-MD-a9fb7b42f8](../../../AGENTS.md#framework-adr-scope-boundary-discipline) each of the four common-substrate framework ADRs U-A claims is paired with U-A's per-variant ADR co-located in this index: 0028 (P-19 framework) ↔ 0050 (U-A interval-kind feature source); 0029 (P-28 framework) ↔ 0051 (U-A interval envelope); 0030 (P-29 framework) ↔ 0052 (U-A interval-policy DSL); 0036 (P-30 framework) ↔ 0053 (U-A re-entry state machine). U-A carries no orphan substrate primitive — every load-bearing substrate decision lives either in the shared common substrate (commodity / designed-system framework ADRs above) or in one of the four per-variant ADRs. This is the most variant pairings of any v3 candidate, reflecting U-A's typed-node-graph axis: the envelope, the closure DSL, the classifier feature set, and the re-entry state machine all live in U-A's own variant ADRs against shared frameworks.

## §1 Overview

**Mandate.** Unified-attempt. U-A carries both greenfield and brownfield by *parameterising the interval graph* — same substrate (envelope + policy mediator + classifier + re-entry registrar + judge router); different `kind` distribution and different policy slot contents on each cycle's interval-graph nodes.

**Axis.** Typed-node-graph over `EscrowInterval` envelopes. Per [unified-A §0](../tracks/unified-A.md#0-axis-declaration-and-defense), every cycle is a directed graph of typed interval nodes; the substrate enforces *what happens inside each interval* (gates, judges, immutable logs, sandbox attestations, reflection-trigger firings, AILCCP three-controls coverage); methodology layer composes *which intervals exist*. Per DEC-2, the escrow framing demoted to a methodology pattern at registry close; the **typed-node-graph shape** is the load-bearing substrate axis. The dispatch brief and substrate-requirements summary preserve the `EscrowInterval` envelope as the load-bearing typed envelope on top of P-28.

**Entry-mode.** Either: greenfield enters with `kind: bootstrap` (priors.in-tree=[]; priors.out-of-tree=[adjacent-domains, exemplars, operator-curated]); brownfield enters with `kind: archaeology` (priors.in-tree=[codebase, history, traces, tests]; priors.out-of-tree=[]). Steady-state on both mandates is the same interval graph — `kind` and `pace-layer` drive policy lookup; the substrate sees only the typed envelope.

**Methodology summary.** Substrate-heavy, thin-methodology per CTR-C2 ([unified-A §0 driver 5](../tracks/unified-A.md#0-axis-declaration-and-defense)). Methodology layer supplies *graphs* of intervals (declarative DAGs over interval-kinds); substrate fires `policies` slot rules at every interval boundary. Compound-Atelier issue-intake, Refinery spec-delta-entry, and Attractor-DOT pipelines are all expressible as different graph shapes on the same substrate.

**Load-bearing claim.** The interval envelope ([ADR 0051](../../../docs/adr/0051-p-28-variant-u-a-interval-envelope.md)) is U-A's single load-bearing substrate handle: classifier ([ADR 0050](../../../docs/adr/0050-p-19-variant-u-a-interval-kind.md)) writes to it, policy mediator ([ADR 0052](../../../docs/adr/0052-p-29-variant-u-a-interval-policy.md)) reads from it, re-entry registrar ([ADR 0053](../../../docs/adr/0053-p-30-variant-u-a-re-entry.md)) carries it as workflow state, and judge router ([ADR 0016](../../../docs/adr/0016-p-14-judge-router.md)) routes per its `policies.judge-diversity` field. Discipline is structural (substrate-fired), not voluntary — F53 mitigation is foundational, not bolted on.

## §2 Substrate composition

U-A carries the common substrate baseline (eight ADRs 0010–0017) and **four framework + per-variant pairs** binding U-A's typed-node-graph instantiation, plus the discipline ADRs (0018–0027). U-A carries no orphan substrate primitive — every load-bearing piece of U-A's substrate stack is either commodity common substrate or a framework-bound per-variant ADR. The four pairings:

**P-28 framework + U-A interval envelope.** The Phase-4.2 [`overlap.md` verdict on P-28](../primitives/overlap.md#p-28-typed-object-store--four-contested-variants) is verbatim:

> **"Verdict: SAME primitive (P-28 typed-object store framework), DISTINCT envelopes. All four share the construction recipe (libgit2 `git_odb_write` + `refs/notes/<envelope-kind>`; Postgres `bytea`+`jsonb`+GIN alternate path; content-addressed append-only with typed envelope per P-28 sketch). The envelope schemas are non-overlapping but the underlying primitive (typed envelope + content-hash + append-only + Glean/Postgres-compatible storage) is identical."**

The verdict binds U-A to pair the framework with U-A's per-variant envelope ADR. Framework: [ADR 0029](../../../docs/adr/0029-p-28-typed-object-store.md) records the content-addressed append-only typed-object store (libgit2 / Postgres) shared with U-B, U-C, D7-U-1. U-A variant: [ADR 0051](../../../docs/adr/0051-p-28-variant-u-a-interval-envelope.md) registers `EscrowInterval{id, kind, pace-layer, priors, policies, classifier, artefacts}` under the `refs/notes/escrow-interval` namespace (libgit2 path) or `envelope_kind = 'escrow-interval'` discriminator (Postgres path) with primary typed-filter axis `kind × pace-layer × classifier.work-unit-class`. Per [u-a.md §3 envelope schema](../substrate-requirements/u-a.md), `kind ∈ {bootstrap, refactor, spec-author, review, merge, deploy, re-entry, archaeology, methodology-delta, …}` and `pace-layer ∈ {code, plans, specs, architecture, standards}` (Brier). The envelope is the load-bearing substrate handle — every U-A cycle node is a durable content-addressed `EscrowInterval` record; D-7 trajectory capture ([ADR 0012](../../../docs/adr/0012-p-05-trajectory-capture.md)) plugs into `artefacts.trajectory` as a P-28 handle paid for at framework price.

**P-19 framework + U-A interval-kind classifier.** The Phase-4.2 [`overlap.md` verdict on P-19](../primitives/overlap.md#p-19-eligibility--regime-classifier--four-contested-variants) is verbatim:

> **"SAME primitive (P-19 classifier framework), DISTINCT feature sources + distinct output regime sets. All four share the construction recipe (Drools/OPA Rego decision tables + LLM-judge fallback via P-14 + OPA hard-floor post-check per P-19 sketch). The differences are at the *feature engineering* layer and the *output enum* layer, not the *decision-engine* layer."**

Framework: [ADR 0028](../../../docs/adr/0028-p-19-eligibility-regime-classifier.md) records the Drools / OPA Rego decision-table engine + LLM-judge fallback via [P-14](../../../docs/adr/0016-p-14-judge-router.md) + OPA hard-floor post-check shared with GF-S, BF-L, U-C. U-A variant: [ADR 0050](../../../docs/adr/0050-p-19-variant-u-a-interval-kind.md) records U-A's feature source as `{interval_kind, pace_layer, priors_out_of_tree_count, priors_out_of_tree_signatures, priors_in_tree_count, priors_in_tree_signatures, substrate_judge_agreement_recent, cost_ceiling_state}` read off the interval envelope at interval-open time. Output regime: `automation-eligibility ∈ {lights-out, sample-audit, escalate, human-required}` written back into `classifier.automation-eligibility`. Per [u-a.md §3 feature source](../substrate-requirements/u-a.md) and [unified-A §5.4](../tracks/unified-A.md#54-day-0--day-n-trajectory): day-0 default is `escalate` for every interval-kind until declared threshold-bars are measured, enforced as an OPA-post-check substrate floor. Three hard floors per ADR 0050: `kind = bootstrap → escalate` (full stop); `kind ∈ {archaeology, methodology-delta}` AND not yet audited at a re-entry interval → at-most `sample-audit`; cost-ceiling breach OR substrate-judge-agreement-recent < threshold → never `lights-out`. The classifier reads features that live next to the envelope and writes the verdict back into the same envelope — cross-primitive consistency is a typing property, not a coordination promise.

**P-29 framework + U-A interval-policy DSL.** The Phase-4.2 [`overlap.md` verdict on P-29](../primitives/overlap.md#p-29-policy-mediator--compounding-gate--three-contested-variants) is verbatim:

> **"Verdict: SAME primitive (P-29 policy mediator framework), DISTINCT policy DSLs. All three share the underlying engine (OPA Rego primary; Cedar alternate path per P-29 sketch). The policy vocabulary differs: U-A reasons about interval-slot satisfaction; U-B reasons about layer-pair closure; D7-U-1 reasons about FC-survival windows. The differences are at the *predicate vocabulary* level, not the *engine* level."**

Framework: [ADR 0030](../../../docs/adr/0030-p-29-policy-mediator.md) records the OPA Rego (primary) / Cedar (alternate) engine, content-addressed policy bundles, and `allow / reasons / obligations / audit_envelope` verdict contract shared with U-B, D7-U-1. U-A variant: [ADR 0052](../../../docs/adr/0052-p-29-variant-u-a-interval-policy.md) loads the `u-a` Rego bundle whose core predicate is `interval-slot-satisfaction(interval_id, slot_name)`. Six core slot rules in v1 — `gate`, `log`, `sandbox`, `approval-gate`, `reflection-trigger`, `judge-diversity` — one-to-one with the slot names in ADR 0051's envelope schema. Closure axis is **per-interval slot satisfaction**: the mediator's top-level `allow_close[interval_id]` rule conjoins satisfaction across every slot declared on the envelope and refuses to close otherwise; failing slots enumerate in `reasons[]`; bundle hash is captured in `audit_envelope`. Slot-record producers — [P-06 watchdog](../../../docs/adr/0013-p-06-watchdog-tiers.md), [P-14 judge router](../../../docs/adr/0016-p-14-judge-router.md), [P-01 sandbox](../../../docs/adr/0010-p-01-sandbox-runtime.md) — each emit the typed slot record the Rego rules import; record-shape drift surfaces at bundle build time (Rego compilation failure), not at runtime. F53 (voluntary-discipline fragility) is structurally closed: slot satisfaction is the close boundary, not an operator promise.

**P-30 framework + U-A re-entry state machine.** The Phase-4.2 [`overlap.md` verdict on P-30](../primitives/overlap.md#p-30-event-registrar--two-contested-variants) is verbatim:

> **"Verdict: DISTINCT primitives despite shared underlying substrate. Both use Temporal workflow engine (signal+timer+query triad) at the construction layer, but the load-bearing semantics diverge: U-A's registrar is event-driven: state transitions on external triggers; the timer half is incidental (deadline tracking only). D7-U-1's registrar is timer-driven: the load-bearing transition is `survival-window-open → window-expired`, with cascade wake-up of dependent-FC graphs."**

Framework: [ADR 0036](../../../docs/adr/0036-p-30-event-registrar-substrate.md) records the Temporal signal+timer+query triad + append-only event-log envelope shared with D7-U-1, with namespace-separation discipline (`state-machine-class` field). U-A variant: [ADR 0053](../../../docs/adr/0053-p-30-variant-u-a-re-entry.md) builds a `ReEntryIntervalWorkflow` Temporal workflow type in the `state-machine-class = u-a-re-entry` namespace with state field `state ∈ {in-flight, frozen, re-entry-open, operator-acknowledged, resumed, redirected, closed}`. Three load-bearing signals — `watchdog_escalate(tier, evidence)`, `cost_ceiling_breach(ledger_ref)`, `severity_class_trigger(class, reason)` — each transition `in-flight → frozen → re-entry-open`. The operator's `operator_acknowledge(decision ∈ {resume, redirect, close}, payload)` signal is the atomic step to a terminal state. The timer handler is incidental — it fires only to log `awaiting-operator-acknowledgement` to the audit ledger and re-arm; it **never** drives a state transition. This is the explicit asymmetry against D7-U-1 and the reason overlap.md ruled the registrars DISTINCT primitives.

**Common substrate baseline (eight commodity / designed-system ADRs).** [P-01 sandbox](../../../docs/adr/0010-p-01-sandbox-runtime.md) hosts bwrap+seccomp / container sandboxing for the `policies.sandbox` slot. [P-02 cost ceilings](../../../docs/adr/0011-p-02-cost-ceilings.md) emits cost-ceiling-state into the ADR 0050 classifier feature set and fires `cost_ceiling_breach` signals into the ADR 0053 registrar. [P-05 trajectory capture](../../../docs/adr/0012-p-05-trajectory-capture.md) is the inside-the-interval event stream; envelope wraps trajectory handle. [P-06 watchdog tiers](../../../docs/adr/0013-p-06-watchdog-tiers.md) — Daemon / Triage / Patrol — fires escalation signals into the ADR 0053 registrar and Patrol monitors F47/F57 regime-distribution drift across the typed envelope graph. [P-07 telemetry](../../../docs/adr/0014-p-07-telemetry-ingestor.md) emits the typed slot records the ADR 0052 policy bundle consumes. [P-08 scenario storage](../../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md) carries the holdout discipline (D-4 substrate enforcement) the methodology layer is expected to invert on brownfield (CTR-B5: scenarios from codebase). [P-14 judge router](../../../docs/adr/0016-p-14-judge-router.md) routes per envelope's `policies.judge-diversity` field; cross-family mandatory at stakes ≥ "modifies state outside sandbox" (F46). [P-22 polyglot codebase index](../../../docs/adr/0017-p-22-polyglot-codebase-index.md) supports `kind: archaeology` interval's structural-view ingestion in brownfield entry.

**X_UNM_B brownfield Codebase-Model acquisition** (per [u-a.md §4](../substrate-requirements/u-a.md#4-x_unm_b-articulation)). U-A as authored does not name a dedicated extraction primitive — the `kind: archaeology` interval is a methodology-layer construct whose `policies.gate` and `judge-diversity: different-family` enforce extraction quality. Of [P-26's six views](../primitives/P-26-codebase-model.md), the **conventional view** and **invariant view** are inherited from BF-L's authoring ceiling; U-A carries whatever BF-L lands. Additionally, U-A's interval envelope lacks first-class code-region typing, so structural / semantic / dependency views are reconstructable only at interval-grain, not at code-region-grain. Fallback: post-archaeology interval defaults `classifier.automation-eligibility = escalate` (substrate floor; ADR 0050 hard floor 2) and requires `policies.judge-diversity: different-family` on every interval until the archaeology interval has been audited at a re-entry interval. Graceful degradation, not silent failure; honestly named as a Phase-5/6 methodology-spec carry per §6.

## §3 Methodology shape

**Per-cycle loop.** Methodology supplies a *graph* of interval-kinds; substrate fires policy rules at every interval boundary. Each interval node:

1. **Interval open.** Methodology layer (or operator) names a typed `EscrowInterval` per [ADR 0051](../../../docs/adr/0051-p-28-variant-u-a-interval-envelope.md): declares `kind`, `pace-layer`, `priors.{out-of-tree, in-tree}`, and the `policies.{gate, log, sandbox, approval-gate, reflection-trigger, judge-diversity}` slot block. `put` validates against the JSON-Schema and assigns a content-hash `id`.

2. **Classifier dispatch.** The [ADR 0050](../../../docs/adr/0050-p-19-variant-u-a-interval-kind.md) feature extractor reads the envelope's `kind`, `pace-layer`, `priors` plus substrate-current judge-agreement-recent (from [P-14](../../../docs/adr/0016-p-14-judge-router.md) rolling stats per `kind`) and [P-02](../../../docs/adr/0011-p-02-cost-ceilings.md) cost-ceiling state. The [ADR 0028](../../../docs/adr/0028-p-19-eligibility-regime-classifier.md) decision-table engine evaluates and emits `automation-eligibility ∈ {lights-out, sample-audit, escalate, human-required}` into the envelope's `classifier.automation-eligibility` slot — pinned at interval-open time. OPA hard floors (per ADR 0050) cannot be overridden by feature-vector scoring.

3. **Interval execution.** Per the dispatched regime + the envelope's `policies` slots, the substrate fires gate / sandbox / log / reflection-trigger / approval-gate / judge-diversity rule packs. Inside-the-interval execution is bounded by `policies.sandbox` ([P-01](../../../docs/adr/0010-p-01-sandbox-runtime.md)) and `policies.log` ([P-05](../../../docs/adr/0012-p-05-trajectory-capture.md) + AILCCP immutable logging when stakes warrant). Per [unified-A §4 D-4](../tracks/unified-A.md#4-defaults-accepted-vs-challenged), the substrate refuses to close any `kind: judge`-derived interval if acceptance-criteria handles leaked into the upstream builder interval's inputs.

4. **Closure attempt.** The [ADR 0052](../../../docs/adr/0052-p-29-variant-u-a-interval-policy.md) mediator's `allow_close[interval_id]` rule conjoins `interval-slot-satisfaction(interval_id, slot)` across every declared slot. Failing slots enumerate in `reasons[]`; `obligations[]` may direct re-runs; bundle hash is captured in `audit_envelope`. The mediator refuses to close on any `allow == false`.

5. **Escalation / re-entry.** If [P-06](../../../docs/adr/0013-p-06-watchdog-tiers.md) escalates a tier, [P-02](../../../docs/adr/0011-p-02-cost-ceilings.md) breaches the ceiling, or a severity-class trigger fires, the [ADR 0053](../../../docs/adr/0053-p-30-variant-u-a-re-entry.md) `ReEntryIntervalWorkflow` transitions `in-flight → frozen → re-entry-open` and waits for `operator_acknowledge(decision ∈ {resume, redirect, close})`. The frozen-state snapshot captures the in-flight graph position; the re-entry summary derives from the trajectory store + AILCCP immutable log. Subscribers: audit ledger, classifier ([P-19](../../../docs/adr/0028-p-19-eligibility-regime-classifier.md)), trajectory store.

**Regime structure.** Per-interval, per-`automation-eligibility`. Per ADR 0050 hard floors and per [unified-A §5.3](../tracks/unified-A.md#53-bootstrap-interval-policies-strictest-defaults):

- **`lights-out`** — substrate-enforced gates only (no operator inner-loop). Permitted *only after* graduation: (a) operator confirmation at a re-entry interval, (b) measured threshold-bars per `kind`, (c) cost-ceiling headroom positive, (d) substrate-judge-agreement-recent ≥ threshold.
- **`sample-audit`** — substrate fires gates as for lights-out; cross-family judge on a configurable sample fraction.
- **`escalate`** — `policies.judge-diversity: different-family` mandatory; `approval-gate` required at 100% sample rate. Day-0 default for every `kind`.
- **`human-required`** — re-entry interval fires before close; operator acknowledge required.

**Work-unit definition.** A typed `EscrowInterval` is the work-unit. The same envelope expresses Atelier-style issue-intake (`kind: issue-intake`), Refinery-style spec-delta entry (`kind: spec-delta`), and Attractor-style DOT pipeline nodes (`kind: pipeline-stage`) — front-end-agnostic. The cost ceiling ([ADR 0011](../../../docs/adr/0011-p-02-cost-ceilings.md)) is per-`kind` parameterised; `kind: bootstrap` / `kind: methodology-delta` carry the highest caps; routine refactors carry low caps.

**Distinctive methodology decisions.** Four:

- **Day-0 default is `escalate` for every interval-kind, OPA-floor enforced.** Per ADR 0050 the floor is in the substrate, not the methodology layer. Cold-start posture cannot drift by accident.
- **Bootstrap interval cannot self-judge.** `kind: bootstrap → automation-eligibility = escalate` is a hard stop; `policies.judge-diversity: different-family` is mandatorily required on bootstrap. F1/F27/F46 closure.
- **Methodology evolution is itself a typed interval.** `kind: methodology-delta` carries `judge-diversity: different-family` by default per [unified-A §2 OQ-B9](../tracks/unified-A.md#oq-b9-methodology-evolution); F35/F55 closure.
- **Re-entry is event-driven, not timer-driven.** The operator is the proximate cause of resume/redirect/close per ADR 0053; the timer half only surfaces non-acknowledgement to the audit ledger.

## §4 Discipline binding

U-A binds all 10 discipline ADRs (0018–0027). Per-discipline:

- **Bias guard ([ADR 0018](../../../docs/adr/0018-discipline-bias-guard.md)).** Bound at the [ADR 0052](../../../docs/adr/0052-p-29-variant-u-a-interval-policy.md) `judge-diversity` slot rule: `judge-diversity: different-family` is enforced by Rego against [P-14](../../../docs/adr/0016-p-14-judge-router.md)'s provider-family tag, mechanically not by convention. F46 mitigation at substrate.
- **Cognitive escrow ([ADR 0019](../../../docs/adr/0019-discipline-cognitive-escrow.md)).** Bound at the typed-node-graph axis itself: every interval is the named escrow handoff Kahana describes; substrate-fired `policies.reflection-trigger` (STIR cascade, success-criterion articulation, delegation-confirm) replaces voluntary discipline. F42 mitigation is foundational, not bolted on.
- **Cost ceiling ([ADR 0020](../../../docs/adr/0020-discipline-cost-ceiling.md)).** Bound at [P-02 (ADR 0011)](../../../docs/adr/0011-p-02-cost-ceilings.md) with per-`kind` parameterisation; breach fires `cost_ceiling_breach` signal into the [ADR 0053](../../../docs/adr/0053-p-30-variant-u-a-re-entry.md) registrar. The cost-ceiling state is also a classifier feature ([ADR 0050](../../../docs/adr/0050-p-19-variant-u-a-interval-kind.md) feature 8) — never `lights-out` under breach.
- **Holdout ([ADR 0021](../../../docs/adr/0021-discipline-holdout.md)).** Bound at [P-08 (ADR 0015)](../../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md). The [ADR 0052](../../../docs/adr/0052-p-29-variant-u-a-interval-policy.md) `gate` slot rule refuses to close any `kind: judge` interval if acceptance-criteria handles leaked into builder inputs. D-4 substrate enforcement (per [unified-A §4 D-4 challenge](../tracks/unified-A.md#4-defaults-accepted-vs-challenged) — substrate enforces holdout-vs-builder separation regardless of which side of the tree the scenarios live on).
- **Honesty ([ADR 0022](../../../docs/adr/0022-discipline-honesty.md)).** Bound. U-A's specific honest acknowledgement: X_UNM_B articulation depth is shallow as authored (§2 above; see §6). The substrate makes the gap visible (no synthetic Codebase Model claim), but the methodology spec owed at Phase-5/6 must articulate degradation.
- **Knowledge promotion ([ADR 0023](../../../docs/adr/0023-discipline-knowledge-promotion.md)).** Bound at the `kind: methodology-delta` interval-class: pattern → standard promotion is itself a typed interval, mandatorily L4 (`judge-diversity: different-family` default per ADR 0053 alternative B rejection). Compound-Knowledge insight / playbook / correction / pattern envelopes are sub-types under the methodology-delta umbrella.
- **Regime classification ([ADR 0024](../../../docs/adr/0024-discipline-regime-classification.md)).** Bound at [P-19 (ADR 0050)](../../../docs/adr/0050-p-19-variant-u-a-interval-kind.md) per the framework-discipline contract. U-A names per-variant: feature source (envelope + judge-agreement-recent + cost-ceiling state); regime set (`{lights-out, sample-audit, escalate, human-required}`); hard-floor table (three rules in §2 above). Day-0 default `escalate` is a substrate floor.
- **Scoping ([ADR 0025](../../../docs/adr/0025-discipline-scoping.md)).** Bound at the [ADR 0050](../../../docs/adr/0050-p-19-variant-u-a-interval-kind.md) classifier: work-unit scope is bounded by the dispatched regime + the `policies` slot block. No mandate-specific scoping; envelope's `kind` is the regime axis.
- **Three-loop ([ADR 0026](../../../docs/adr/0026-discipline-three-loop.md)).** Bound at the Compound-Engineering plan→work→review→compound loop expressed as a graph of intervals. The "compound" step materialises as Patrol-tier ([P-06](../../../docs/adr/0013-p-06-watchdog-tiers.md)) monitoring of regime-distribution drift across the `kind × pace-layer` slice — meta-loop closure is substrate-enforced.
- **Trifecta closure ([ADR 0027](../../../docs/adr/0027-discipline-trifecta-closure.md)).** Bound at the [ADR 0052](../../../docs/adr/0052-p-29-variant-u-a-interval-policy.md) `gate` slot + [P-08 (ADR 0015)](../../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md) holdout + [P-01 (ADR 0010)](../../../docs/adr/0010-p-01-sandbox-runtime.md) sandbox — all three legs substrate-enforced as slot satisfactions on the interval boundary.

**Disciplines U-A is NOT silent on.** None. U-A carries all 10. Honesty's X_UNM_B carry is honest, not a silent reject.

## §5 Mandate fit

U-A's mandate-fit YAML block (in this spec's frontmatter) restated per work-unit-class. Per [DEC-1.a falsifier discipline](../decisions-captured.md#d1--unification-verdict-no-methodology-serves-both-mandates-working-hypothesis-falsifiable-by-phase-8), each cell names supporting substrate + falsifying scenario.

- **initial-spec: both.** Greenfield runs `kind: bootstrap` (priors.in-tree=[]); brownfield runs `kind: archaeology` then a `kind: spec-author` interval consuming archaeology outputs. Same substrate primitives ([ADR 0051](../../../docs/adr/0051-p-28-variant-u-a-interval-envelope.md) envelope; [ADR 0050](../../../docs/adr/0050-p-19-variant-u-a-interval-kind.md) classifier defaults to `escalate`; [ADR 0052](../../../docs/adr/0052-p-29-variant-u-a-interval-policy.md) policy bundle); different `priors` content. Falsifying scenario: if greenfield's `kind: bootstrap` interval graduates to `lights-out` before any threshold-bars are measured (against the ADR 0050 hard floor 1), or if brownfield's `kind: archaeology` interval emits a downstream interval-class taxonomy that systematically miscalibrates against held-out behaviour, the mandate-as-parameter claim fails.
- **refactor: both.** Refactor cycles run as `kind: refactor` intervals with `pace-layer ∈ {code, plans}`. Greenfield refactor (against accumulated architecture-rules in tree) and brownfield refactor (against existing live-tests + standards) share the same envelope shape; only `priors.in-tree` content differs. Supporting substrate: ADR 0051 envelope + ADR 0050 classifier (`refactor` typically graduates to `sample-audit` after measurement). Falsifying scenario: if refactor intervals on brownfield land at systematically lower `automation-eligibility` than refactor intervals on greenfield with identical envelope-feature distributions, the substrate's mandate-symmetry claim collapses.
- **mvp: greenfield.** MVP authoring (greenfield-typical) runs against the operator-authored intent block expressed as `priors.out-of-tree`. Anchor accumulation per [unified-A §5.4](../tracks/unified-A.md#54-day-0--day-n-trajectory) thickens the in-tree priors as MVP cycles deposit live-tests and architecture-rules. Brownfield MVP is not a canonical U-A work-unit-class (MVP presupposes greenfield-leaning evolution); the YAML carries `greenfield` rather than `silent` because the substrate explicitly serves greenfield MVP via `kind: bootstrap` + downstream `kind: spec-author`. Falsifying scenario: if MVP cycles never accumulate enough audited interval-classes to graduate past `escalate` (per ADR 0050 hard floor 2's audit requirement), the earned-lights-out trajectory claim fails.
- **post-mvp-evolution: both.** Steady-state cycles operate against accumulated in-tree priors on both mandates. Distance from cold-start is measured by interval-class graduation history (which `kind` values have been audited and threshold-cleared per [unified-A §5.4](../tracks/unified-A.md#54-day-0--day-n-trajectory)). Same substrate; same regime distribution converges as priors thicken. Falsifying scenario: if post-MVP cycles on brownfield require an extraction primitive U-A does not carry (i.e., the X_UNM_B gap forecloses brownfield post-MVP at the Codebase Model layer), the unified claim retreats to greenfield-only.
- **regression-fix: both.** Regression fixes run as `kind: regression-fix` intervals; the failing test IS the substrate's near-anchor (in U-C terms) and U-A treats it as the `priors.in-tree` first element. ADR 0050 classifier typically dispatches `sample-audit` after threshold measurement; ADR 0052 enforces the `gate` slot against the failing-test acceptance record. Falsifying scenario: if regression-fix intervals routinely escalate to `human-required` because the substrate cannot distinguish them from broader refactors, the per-`kind` regime structure is wrong.

**DEC-1.a falsifier-discipline observation.** U-A explicitly claims `both` on 4 of 5 work-unit-classes (initial-spec, refactor, post-mvp-evolution, regression-fix). Per [DEC-1.a](../decisions-captured.md#d1--unification-verdict-no-methodology-serves-both-mandates-working-hypothesis-falsifiable-by-phase-8), this is evidence weighing against the no-methodology-serves-both-mandates working hypothesis; pressure-tests load on Phase 8 lean-eval (§6).

## §6 Open carries

- **DPU-1 interval-granularity cost at year-2 scale (Phase-8 lean-eval candidate).** Per [u-a.md §2 / §5](../substrate-requirements/u-a.md#2-rg-primitives) and [unified-A §7 OQ 1 / OQ 6](../tracks/unified-A.md#7-open-questions-surfaced-by-this-track): process-state-node-per-cycle granularity produces many `EscrowInterval` records per cycle; the combined cost of immutable logging + cross-family judge + STIR-cascade reflection at high-parallelism is not corpus-measured. **Status: Phase-8 lean-eval; the load-bearing open carry U-A surfaces.**
- **Classifier audit discipline at scale (Phase-5/8 carry; F57 amplified).** Per [unified-A §7 OQ 2](../tracks/unified-A.md#7-open-questions-surfaced-by-this-track) the [ADR 0050](../../../docs/adr/0050-p-19-variant-u-a-interval-kind.md) classifier is the architecture's most powerful actor (decides automation-eligibility per interval). F57 (convenience reclassifies stakes) is amplified by the classifier's centrality; Patrol-tier diff of regime distributions per `kind × pace-layer` is the substrate detector, but audit-trail completeness on graduation events is owed.
- **Re-entry partial semantics (Phase-6 methodology spec carry).** Per ADR 0053 "Explicitly NOT promising": `resume-with-modifications`, `redirect-to-different-kind`, partial-graph rehydration are deferred. The state-machine skeleton is fixed; the partial-re-entry policy is owed at Phase-6 methodology spec.
- **F48 cross-interval correlation via shared trajectory store (Phase-8 lean-eval candidate).** Per [unified-A §7 OQ 4](../tracks/unified-A.md#7-open-questions-surfaced-by-this-track): if many intervals share access to the same trajectory store or scenario library, multi-agent tacit collusion may re-emerge at the substrate layer. Whether interval-object-store itself needs partition discipline is unresolved.
- **X_UNM_B articulation depth (Phase-5/6 methodology spec carry).** Per [u-a.md §4](../substrate-requirements/u-a.md#4-x_unm_b-articulation): the `kind: archaeology` interval renders in-tree priors into a typed surface but U-A does not name an extraction primitive; conventional + invariant view ceilings inherited from BF-L; code-region-grain mismatch unresolved. Substrate honestly carries the gap; methodology-spec carry is owed.
- **OQ-PLEF-style multi-cycle drift on the typed envelope (Phase-3 adversarial pass carry — open).** Per [unified-A §7 OQ 7](../tracks/unified-A.md#7-open-questions-surfaced-by-this-track): whether "interval" is itself a contaminating label; blind-axis re-test of envelope framing is appropriate if two other unified subagents converge on interval / escrow framing.

## §7 References

**ADR set (this spec's binding inputs).** Per the §0 ADR-citation index above; relative paths under `../../../docs/adr/`:

- Common substrate: [ADR 0010](../../../docs/adr/0010-p-01-sandbox-runtime.md), [ADR 0011](../../../docs/adr/0011-p-02-cost-ceilings.md), [ADR 0012](../../../docs/adr/0012-p-05-trajectory-capture.md), [ADR 0013](../../../docs/adr/0013-p-06-watchdog-tiers.md), [ADR 0014](../../../docs/adr/0014-p-07-telemetry-ingestor.md), [ADR 0015](../../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md), [ADR 0016](../../../docs/adr/0016-p-14-judge-router.md), [ADR 0017](../../../docs/adr/0017-p-22-polyglot-codebase-index.md).
- Framework substrate (four framework + per-variant pairs, load-bearing):
  - [ADR 0028 (P-19 framework)](../../../docs/adr/0028-p-19-eligibility-regime-classifier.md) ↔ [ADR 0050 (U-A P-19 variant — interval-kind feature source)](../../../docs/adr/0050-p-19-variant-u-a-interval-kind.md).
  - [ADR 0029 (P-28 framework)](../../../docs/adr/0029-p-28-typed-object-store.md) ↔ [ADR 0051 (U-A P-28 variant — interval-typed envelope)](../../../docs/adr/0051-p-28-variant-u-a-interval-envelope.md).
  - [ADR 0030 (P-29 framework)](../../../docs/adr/0030-p-29-policy-mediator.md) ↔ [ADR 0052 (U-A P-29 variant — interval-policy DSL)](../../../docs/adr/0052-p-29-variant-u-a-interval-policy.md).
  - [ADR 0036 (P-30 framework)](../../../docs/adr/0036-p-30-event-registrar-substrate.md) ↔ [ADR 0053 (U-A P-30 variant — re-entry-interval state machine)](../../../docs/adr/0053-p-30-variant-u-a-re-entry.md).
- Discipline: [ADR 0018](../../../docs/adr/0018-discipline-bias-guard.md), [ADR 0019](../../../docs/adr/0019-discipline-cognitive-escrow.md), [ADR 0020](../../../docs/adr/0020-discipline-cost-ceiling.md), [ADR 0021](../../../docs/adr/0021-discipline-holdout.md), [ADR 0022](../../../docs/adr/0022-discipline-honesty.md), [ADR 0023](../../../docs/adr/0023-discipline-knowledge-promotion.md), [ADR 0024](../../../docs/adr/0024-discipline-regime-classification.md), [ADR 0025](../../../docs/adr/0025-discipline-scoping.md), [ADR 0026](../../../docs/adr/0026-discipline-three-loop.md), [ADR 0027](../../../docs/adr/0027-discipline-trifecta-closure.md).

**Supporting docs:**

- [U-A candidate-registry entry](../candidate-registry.md#u-a--escrow-graph-factory)
- [U-A substrate-requirements summary](../substrate-requirements/u-a.md)
- [Unified-A track sketch](../tracks/unified-A.md)
- [Phase-4.2 overlap.md P-28 verdict — four contested variants](../primitives/overlap.md#p-28-typed-object-store--four-contested-variants)
- [Phase-4.2 overlap.md P-19 verdict — four contested variants](../primitives/overlap.md#p-19-eligibility--regime-classifier--four-contested-variants)
- [Phase-4.2 overlap.md P-29 verdict — three contested variants](../primitives/overlap.md#p-29-policy-mediator--compounding-gate--three-contested-variants)
- [Phase-4.2 overlap.md P-30 verdict — two contested variants DISTINCT](../primitives/overlap.md#p-30-event-registrar--two-contested-variants)
- [DEC-1.a unification-verdict working hypothesis](../decisions-captured.md#d1--unification-verdict-no-methodology-serves-both-mandates-working-hypothesis-falsifiable-by-phase-8)
- [DEC-2 mandate-fit-per-(architecture × work-unit-class)](../decisions-captured.md#d2--mandate-fit-is-per-architecture--work-unit-class-not-per-architecture)
- [Phase-5-close session handoff — U-A row](../SESSION-HANDOFF-2026-05-25-phase-5-close.md)
- [auto-006 Phase-6 dispatch-shape brief](../decisions/auto-006-phase-6-dispatch-shape.md)
- [U-C spec (Phase-6 exemplar)](u-c.md)
