---
candidate: bf-s
candidate-name: Brownfield, Substrate-First
mandate-scope: brownfield
based-on-commit: c54daf1
based-on-date: 2026-05-26
mandate-fit:
  initial-spec: brownfield
  refactor: brownfield
  mvp: n/a
  post-mvp-evolution: brownfield
  regression-fix: brownfield
---

# Architecture spec — BF-S (Brownfield, Substrate-First)

## §0 ADR-citation index

| ADR ID | Title | Layer | Variant of | Citing § |
|---|---|---|---|---|
| 0010 | P-01 Sandbox runtime | common-substrate | — | §2, §4 |
| 0011 | P-02 Cost ceilings | common-substrate | — | §2, §4 |
| 0012 | P-05 Trajectory capture | common-substrate | — | §2, §3, §4 |
| 0013 | P-06 Watchdog tiers | common-substrate | — | §2, §4 |
| 0014 | P-07 Telemetry ingestor | common-substrate | — | §2, §3, §4 |
| 0015 | P-08 Scenario storage with runner contract | designed-system-substrate | — | §2, §3, §4 |
| 0016 | P-14 Judge router | common-substrate | — | §2, §3 |
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
| 0031 | P-23 Dependency-impact graph | common-substrate | — | §2, §3, §4 |
| 0033 | P-25 CaMeL perimeter | 2-candidate-fold-substrate | — | §2, §3, §4 |
| 0035 | P-24 Attribution store | 2-candidate-fold-substrate | — | §2, §3, §4 |

**Framework + per-variant pairing check.** BF-S claims **no** framework ADR (0028 P-19 / 0029 P-28 / 0030 P-29 / 0036 P-30) as a substrate primitive — per the [BF-S substrate-requirements §3 closing line](../substrate-requirements/bf-s.md), "BF-S does not name any of P-28, P-29, P-30, or P-19 (the Phase-4.2 same-vs-distinct candidates). No fixed sub-section headers needed." Regime decisions are computed inline by methodology from substrate-produced views (per §3 below), not bound to a framework classifier substrate. The framework-ADR-pair pairing rule per [AGENTS.md framework-ADR scope boundary](../../../AGENTS.md#framework-adr-scope-boundary-discipline) is therefore trivially satisfied — BF-S carries no per-variant ADRs because it carries no framework ADRs to pair them with.

## §1 Overview

**Mandate.** Brownfield. BF-S is brownfield-only — the candidate explicitly does not pretend to serve greenfield work-unit-classes (per [brownfield-substrate-first §6](../tracks/brownfield-substrate-first.md)).

**Axis.** Substrate is the primary organising principle. The brownfield factory's design begins from the substrate primitives that ingest the existing codebase, its tests, its dependency graph, its runtime telemetry, and its issue/PR history — and treats those ingestion-and-maintenance primitives as the load-bearing investment.

**Entry-mode.** Brownfield-only. The "bootstrap" is legacy-ingestion against an existing codebase (per [brownfield-substrate-first §5](../tracks/brownfield-substrate-first.md)) — a bounded one-time substrate setup, *not* symmetric to greenfield cold-start. S-1 (P-22 index), S-2 (P-23 graph), S-3 (P-07 telemetry), S-4 (P-24 attribution) build incrementally; S-5 (P-25 perimeter) is upfront policy.

**Methodology summary.** Thin methodology overlay over a five-primitive substrate (S-1 codebase index, S-2 dependency-impact graph, S-3 role-partitioned telemetry, S-4 attribution store, S-5 CaMeL perimeter). Per-cycle process is generic: pick a work unit; query substrate views; propose a diff inside the P-25 perimeter; cross-model judge per [P-14](../../../docs/adr/0016-p-14-judge-router.md); check the diff against P-23 blast-radius predictions; append to the P-24 attribution store; decide knowledge promotion. The substrate owns the durable facts; the methodology layer owns durable practices that change.

**Load-bearing claim.** **The CaMeL-class typed perimeter (P-25, ADR 0033) is the substrate-level brownfield boundary** — the trifecta closure (F12 / F33 / F44 / F56) cannot live in methodology under brownfield pressure because every brownfield cycle necessarily touches production data, production credentials, deploy paths, and live tests (per [BF-S §0 reason 3](../tracks/brownfield-substrate-first.md)). F53 (voluntary-discipline fragility) generalises the argument: any control assumed to be operator-applied or methodology-applied breaks under the time-pressure conditions where it is most needed. Substrate-first for brownfield is the F53-resistant shape.

## §2 Substrate composition

BF-S carries **five designed-system substrate primitives** plus the **commodity substrate baseline** (the universal primitives the brief assumes will land in Phase 4 as cross-cutting commodities — sandbox / cost ceilings / trajectory capture / watchdog / telemetry / scenario storage / judge router / polyglot index). Per [BF-S §3 closing line](../substrate-requirements/bf-s.md), BF-S claims **no contested framework primitives** — no P-28 / P-29 / P-30 / P-19 references.

**Commodity substrate baseline.** [P-01 sandbox (ADR 0010)](../../../docs/adr/0010-p-01-sandbox-runtime.md), [P-02 cost ceilings (ADR 0011)](../../../docs/adr/0011-p-02-cost-ceilings.md), [P-05 trajectory capture (ADR 0012)](../../../docs/adr/0012-p-05-trajectory-capture.md), [P-06 watchdog tiers (ADR 0013)](../../../docs/adr/0013-p-06-watchdog-tiers.md), [P-07 telemetry ingestor (ADR 0014)](../../../docs/adr/0014-p-07-telemetry-ingestor.md), [P-08 scenario storage (ADR 0015)](../../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md), [P-14 judge router (ADR 0016)](../../../docs/adr/0016-p-14-judge-router.md), [P-22 polyglot codebase index (ADR 0017)](../../../docs/adr/0017-p-22-polyglot-codebase-index.md), [P-23 dependency-and-impact graph (ADR 0031)](../../../docs/adr/0031-p-23-dependency-impact-graph.md). P-22 is BF-S's **S-1**; P-23 is BF-S's **S-2**; P-07 is BF-S's **S-3**. P-08 is consumed as the scenario surface; held-out scenarios from the in-codebase test suite are stored here with the [holdout discipline (ADR 0021)](../../../docs/adr/0021-discipline-holdout.md) gate.

**Distinctive substrate (the BF-S brownfield boundary).** Per the [BF-S §S-5 sketch](../tracks/brownfield-substrate-first.md), the trifecta-closure layer is what makes BF-S brownfield-defensible. Two designed-system ADRs (folded as 2-candidate primitives per [auto-005 Round 2](../decisions/auto-005-phase-5-dispatch-shape.md)) carry this load:

- **P-25 CaMeL perimeter (ADR 0033 — 2-candidate-fold; shared with BF-M).** [ADR 0033](../../../docs/adr/0033-p-25-camel-perimeter.md) records the substrate decision: a capability-typed perimeter implemented as a typed-boundary library wrapping the released [CaMeL reference implementation](../primitives/P-25-camel-perimeter.md#construction-path) (`google-research/camel-prompt-injection`). Privileged-LLM / Quarantined-LLM split; restricted-Python-AST interpreter; per-value `(provenance, readers, inner-source)` capability tokens; tools typed by required-capability sets. **Production-scissors default-off (F44)**; **read/write asymmetric (R1 per [report 32](../../../research/32-shapiro-completion-chat-agent-claw.md))**; **substrate-default closure, not per-Claw discipline**. BF-S binds this primitive as the always-on substrate-level boundary for every cycle's build stage. Per [BF-S substrate-requirements §3](../substrate-requirements/bf-s.md), BF-S accepts [~7-point CaMeL utility tax per CTR-E6](../tracks/brownfield-substrate-first.md#11-substrate-primitive-classes-the-load-bearing-layer) and adds a substrate-level configurable per-work-unit-class bypass with substrate-logged bypass events (the bypass is itself a typed substrate call, not an agent instruction — F53-resistant per ADR 0033 decision text). NORMAL vs STRICT mode is per-work-unit-class config; under `production-adjacent` regimes the perimeter is mandatory and bypass is denied.

- **P-24 attribution store (ADR 0035 — 2-candidate-fold; shared with BF-L).** [ADR 0035](../../../docs/adr/0035-p-24-attribution-store.md) records the substrate decision: typed-object store on the P-08 content-addressed blob substrate, each entry an attribution envelope `(artifact_hash, agent_id, model_snapshot, cycle_id, signer_class, parent_artifact_hashes[], diff_slice, ts, signature_blob)`. Three signer classes — `human_git` (verified by `git verify-commit`), `factory_agent` (Sigstore `cosign sign-blob` against OIDC), `factory_root` (long-lived factory key, chained hash over the projection table at board-report cadence per [F43](../failure-modes-v3.md#f43--rsi-board-visibility-gap)). Per-symbol granularity via P-22's symbol-range index joined to `git blame --line-porcelain`. BF-S binds this as S-4: it is the immutable signed log that closes [F14](../failure-modes-v3.md#f14--attribution-collapse), [F32](../failure-modes-v3.md#f32--mail-injection--unsigned-coordination-messages), [F43](../failure-modes-v3.md#f43--rsi-board-visibility-gap), [F54](../failure-modes-v3.md#f54--goal-subversion-rsi-prompt-injection-over-cycles), [F58](../failure-modes-v3.md#f58--runtime-vs-design-time-compliance-split) at the substrate, not at agent discipline.

**Candidate-specific contracts on commodity substrate.** Per [BF-S substrate-requirements §3](../substrate-requirements/bf-s.md):

- **P-22 (S-1).** BF-S takes the sketch default — "updated on every push (incremental, not full rebuild)" and "returns *slices* sized to the caller's context budget." BF-S explicitly accepts the polyglot type-fidelity ceiling per its own [§7 OQ-T2](../tracks/brownfield-substrate-first.md#7-open-questions-surfaced-by-this-track): "the architecture has to accept S-2 fidelity will vary." S-1 is the F21 (context-exhaustion, brownfield-critical) mitigation point — agents that try to ingest the codebase whole saturate context.

- **P-23 (S-2) — DOWNGRADED B7 CLAIM.** Per the [Phase-3.5.5 BF-S forward action](../candidate-registry.md#bf-s--brownfield-substrate-first-1), BF-S's original B7 ROBUST claim ("substrate-enforced role partition over S-2's transitive closure") is restated as: **"rate-limited side-channel mitigation over S-2's transitive closure; residual count-and-aggregate leakage is tracked and audited; methodology layers must not assume zero leakage."** This is verbatim from [BF-S substrate-requirements §3](../substrate-requirements/bf-s.md). Substrate-side implementation: Glean Angle `visible_to(s, r)` predicate joined into closure rules, reducing leakage to a count-and-aggregate side channel; the count itself is rate-limited and audit-logged via P-05 + P-24. Residual leakage is accepted-open and registered as Phase-8 lean-eval candidate (see §6).

- **P-07 (S-3).** BF-S takes the sketch default with the architectural framing that telemetry reads flow through P-25's capability-typed perimeter (per [P-07 §Alternative construction paths](../primitives/cluster-C2.md#p-07-telemetry-ingestor-per-role-read-filters)). The per-role read filter is the holdout-discipline enforcement point (D-4 generalized to telemetry-as-scenario per [BF-S §S-3](../tracks/brownfield-substrate-first.md)).

**Brier pace-layer absorption.** Per [BF-S §2.9 CTR-F1](../tracks/brownfield-substrate-first.md#29-specific-contradictions-this-track-takes-a-position-on), Brier's pace-layer framing is absorbed as the substrate's **layered fact store**: S-1 fastest, S-2 medium, S-3 medium-slow, S-4 slow, S-5 enforced invariants slowest — pace-layer-as-substrate, factory-as-methodology.

**X_UNM_B (N/A).** BF-S is brownfield-only; X_UNM_B is the cross-mandate finding for unified-attempt candidates' brownfield-fit and does not apply.

## §3 Methodology shape

**Per-cycle loop.** Thin and generic. Per [BF-S §1.3 cycle shape](../tracks/brownfield-substrate-first.md#13-cycle-shape):

1. **Substrate maintains S-1..S-4 continuously** (incremental on every push). P-22 indexes; P-23 recomputes blast-radius edges; P-07 ingests telemetry; P-24 appends signed attribution events.
2. **Methodology picks a work unit** (from the S-4 issue store; or human-injected). The OQ-B4 work-unit shape — issue (Atelier), change-request-against-spec (Refinery), or codebase-evolution proposal — is deferred to per-deployment methodology choice; the substrate supports all three.
3. **Methodology queries** S-1 (P-22) for relevant code slices, S-2 (P-23) for blast radius, S-3 (P-07) for relevant telemetry partitioned by builder-role per the [P-23 §3 restated contract](../substrate-requirements/bf-s.md): role-visibility predicate joined into closure rules; residual leakage rate-limited and audited.
4. **Builder agent (inside S-5 sandbox, with substrate-typed perimeter)** proposes a diff. [P-25 (ADR 0033)](../../../docs/adr/0033-p-25-camel-perimeter.md) provides the typed-interpreter pattern at the syscall and tool-call boundary; production-scissors default-off; capability traces feed [P-05 (ADR 0012)](../../../docs/adr/0012-p-05-trajectory-capture.md).
5. **Cross-model judge reviews** (F46 mitigation) via [P-14 (ADR 0016)](../../../docs/adr/0016-p-14-judge-router.md); substrate enforces same-change cannot be its own judge (F1, F27, F48). The judge slot requires a different-family model per BF-S's [OQ-B8 stance](../tracks/brownfield-substrate-first.md#25-oq-b8-provider-property-requirements) (substrate declares provider-property requirements without mandating router-style abstraction).
6. **Methodology checks diff against S-2's predicted blast radius**; discrepancies escalate. This is the F34 (cross-layer drift, brownfield-critical) and F35 (federation-as-family drift) catch.
7. **Substrate logs to S-4 (P-24)** with per-agent, per-model attribution per the [ADR 0035 envelope schema](../../../docs/adr/0035-p-24-attribution-store.md).
8. **Knowledge-promotion step decides what to persist** (Beads `discovered-from` edge to S-4 record per [report 38](../../../research/38-gas-systems-substrate.md)).

**Regime structure.** Per [BF-S §2.1](../tracks/brownfield-substrate-first.md#21-lights-out--l5-tension-brief-21-oq-b1), BF-S does **not** assert architecture-wide L5. The lights-out classification is **per work-unit-class**, computed per-cycle from substrate evidence: a change with small P-23 blast radius, in-distribution P-07 telemetry, and prior-cycle precedent in P-24 is automation-eligible; a change crossing module boundaries, hitting cold-path telemetry, or violating P-23's predicted blast radius is escalation-required. Per CTR-A5 (Jaymin's brownfield L3 ceiling): the *default* brownfield work-unit-class operates around L3-L4 (matching brownfield-critical severities of F12/F33/F56) and the substrate is what makes L4 reachable for the specific work-unit-classes where S-2/S-3 give confident inputs. **The classification is computed by methodology, not by a P-19 framework substrate primitive** — BF-S explicitly does not carry P-19 as substrate; the regime decision is downstream of S-2 + S-3 + S-4 substrate views.

**Work-unit definition.** Front-end-agnostic (Atelier issue / Refinery change-request / codebase-evolution proposal); the substrate supports all three per [BF-S §2.3 OQ-B4](../tracks/brownfield-substrate-first.md#23-oq-b4-unit-of-work). Per-cycle [P-02 (ADR 0011)](../../../docs/adr/0011-p-02-cost-ceilings.md) ceilings are load-bearing at Stripe scale (1,300 PRs/week per [report 35](../../../research/35-lenny-howiai-spec-driven-and-team-ops.md)).

**Distinctive methodology decisions.**

- **Substrate owns durable facts; methodology owns durable practices.** Per [BF-S §2.6 OQ-B9](../tracks/brownfield-substrate-first.md#26-oq-b9-methodology-evolution), methodology evolution is methodology-owned. The substrate owns the *records* (P-24) and the *knowledge store* (Compound-Knowledge-style, [followup 11](../../../research/followup/11-compound-knowledge.md)) but the rules for promoting, retiring, and reorganising methodology patterns live in the methodology layer.
- **Holdout discipline is substrate-enforced via S-3 read partitioning** (the D-4 expansion, per [BF-S §4 D-2 challenge](../tracks/brownfield-substrate-first.md#4-defaults-accepted-vs-challenged)). Builder agents cannot read holdout telemetry; only the V&V agent role can. This is the substrate-level resolution of CTR-B5 / CTR-G2 (scenarios inside vs outside codebase): inside, substrate-partitioned-by-role.
- **Methodology layer is silent on coordination medium and on which methodology overlay runs.** Compound Engineering, Refinery, or Atelier — any of them can run on this substrate. BF-S is **not** a refutation of any of them per [§6 closing](../tracks/brownfield-substrate-first.md#6-what-this-track-is-not-trying-to-be).

## §4 Discipline binding

BF-S binds all 10 discipline ADRs (0018-0027) at the substrate layer. Per-discipline binding:

- **Bias guard ([ADR 0018](../../../docs/adr/0018-discipline-bias-guard.md)).** Bound at cycle step 5: cross-model judging via [P-14 (ADR 0016)](../../../docs/adr/0016-p-14-judge-router.md) enforces model-family diversity (F46 mitigation). BF-S adopts CTR-D4 / CTR-D7 / CTR-D8 cross-model judge default; Anthropic same-model-fine claim acknowledged but not adopted given F46 + CTR-D8 Tournament-spec corpus support.

- **Cognitive escrow ([ADR 0019](../../../docs/adr/0019-discipline-cognitive-escrow.md)).** Bound at the [P-05 (ADR 0012)](../../../docs/adr/0012-p-05-trajectory-capture.md) trajectory + Patrol-tier ([P-06 (ADR 0013)](../../../docs/adr/0013-p-06-watchdog-tiers.md)) tier. Kahana fragile-dependency framing addressed by substrate-default closure, not operator-voluntary discipline.

- **Cost ceiling ([ADR 0020](../../../docs/adr/0020-discipline-cost-ceiling.md)).** Bound at [P-02 (ADR 0011)](../../../docs/adr/0011-p-02-cost-ceilings.md); the [P-25 (ADR 0033)](../../../docs/adr/0033-p-25-camel-perimeter.md) perimeter is the enforcement point. Brownfield parallelism at Stripe scale (1,300 PRs/week; CTR-E1 $100K/month) makes cost ceilings load-bearing.

- **Holdout ([ADR 0021](../../../docs/adr/0021-discipline-holdout.md)).** Bound at [P-08 scenario storage (ADR 0015)](../../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md) + [P-07 (ADR 0014)](../../../docs/adr/0014-p-07-telemetry-ingestor.md) role-partitioned reads. D-4 generalised to telemetry-as-scenario per [BF-S §4 D-2 challenge](../tracks/brownfield-substrate-first.md#4-defaults-accepted-vs-challenged).

- **Honesty ([ADR 0022](../../../docs/adr/0022-discipline-honesty.md)).** Bound at the [P-24 (ADR 0035)](../../../docs/adr/0035-p-24-attribution-store.md) signed immutable log: per-agent, per-model attribution is structurally required at substrate, not best-effort at calling-agent layer (F53-resistant per ADR 0035). The honesty discipline rides the attribution substrate.

- **Knowledge promotion ([ADR 0023](../../../docs/adr/0023-discipline-knowledge-promotion.md)).** Bound at cycle step 8 (Beads `discovered-from` edges from [report 38](../../../research/38-gas-systems-substrate.md)); knowledge store is Compound-Knowledge-shaped per [followup 11](../../../research/followup/11-compound-knowledge.md). Methodology-owned per BF-S CTR-C3 stance.

- **Regime classification ([ADR 0024](../../../docs/adr/0024-discipline-regime-classification.md)).** Bound at methodology, not at a framework substrate primitive. The work-unit-class L3/L4 classification is computed inline from P-23 blast-radius + P-07 telemetry + P-24 prior-cycle precedent (per §3 regime structure). BF-S deliberately does not carry P-19 as substrate.

- **Scoping ([ADR 0025](../../../docs/adr/0025-discipline-scoping.md)).** Bound at the per-cycle work-unit selection (step 2). Substrate is brownfield-mandate-specific; mandate selection happens at substrate-choice time, not per-cycle. BF-S explicitly declares greenfield out-of-scope (per [BF-S §6](../tracks/brownfield-substrate-first.md#6-what-this-track-is-not-trying-to-be)).

- **Three-loop ([ADR 0026](../../../docs/adr/0026-discipline-three-loop.md)).** Bound at the per-cycle plan→work→review→compound loop with [P-06 (ADR 0013)](../../../docs/adr/0013-p-06-watchdog-tiers.md) Patrol-tier as the meta-loop closure (F55 self-reference detection — Phase-8 lean-eval candidate per §6).

- **Trifecta closure ([ADR 0027](../../../docs/adr/0027-discipline-trifecta-closure.md)).** Bound at the [P-25 perimeter (ADR 0033)](../../../docs/adr/0033-p-25-camel-perimeter.md) — substrate-default closure rather than per-Claw discipline. F12 / F33 / F44 / F56 cascade is closed at substrate by capability-typed dataflow rather than per-agent discipline (verbatim from [ADR 0033 Consequences](../../../docs/adr/0033-p-25-camel-perimeter.md)).

**Disciplines BF-S is silent on.** None. BF-S carries all 10 disciplines at substrate layer.

## §5 Mandate fit

BF-S's mandate-fit YAML block (in this spec's frontmatter) restated per work-unit-class. BF-S is brownfield-only by construction; 4-of-5 cells are `brownfield`; 1-of-5 is `n/a` (mvp — see below):

- **initial-spec: brownfield.** For brownfield, "initial-spec" includes the existing codebase (UC4) plus any intent layer the operator chooses to maintain (per [BF-S §4 D-1 accepted](../tracks/brownfield-substrate-first.md#4-defaults-accepted-vs-challenged)). The durable / version-controlled / human-curated property applies; the *content* differs ([report 14](../../../research/14-el-kaim-book-intent-and-spec-authorship.md) typed spec objects on top of S-1's view of the existing code). Supporting substrate: P-22 (S-1) + P-24 (S-4). Falsifying scenario: if initial-spec authoring on a brownfield codebase routinely requires methodology-side state the substrate doesn't surface, the substrate-first claim is wrong.

- **refactor: brownfield.** Refactor is BF-S's canonical work-unit-class. P-23 (S-2) blast radius is the load-bearing input; P-07 (S-3) telemetry is the in-distribution check; P-25 (S-5) perimeter is the trifecta closure. Falsifying scenario: if refactor cycles routinely produce diffs whose blast radius exceeds P-23's predictions by a wide margin, the substrate-first F34 mitigation is wrong.

- **mvp: n/a.** MVP authoring presupposes greenfield-leaning evolution (no pre-existing codebase to read). BF-S is brownfield-only by explicit construction (per [BF-S §6 "Not a unified architecture"](../tracks/brownfield-substrate-first.md#6-what-this-track-is-not-trying-to-be)); MVP is **deliberately rejected** as a BF-S work-unit-class. The substrate's load-bearing primitives (P-22 index, P-23 graph, P-07 telemetry, P-24 attribution) all presuppose an existing codebase. This is `n/a` not `silent` — BF-S rejects MVP, it doesn't simply have no position.

- **post-mvp-evolution: brownfield.** Post-MVP cycles operate against a thickened P-22 + P-24 substrate. Distance from prior cycles is in P-24; blast radius from P-23; telemetry baseline from P-07. Supporting substrate: P-22 + P-23 + P-07 + P-24. Falsifying scenario: if post-MVP cycles under brownfield require fundamentally different primitives than refactor cycles, BF-S's "substrate is uniform across brownfield work-unit-classes" claim collapses.

- **regression-fix: brownfield.** Regression fixes are by construction near-anchor in P-23 terms (the failing test IS the anchor; the fix's blast radius is small). Substrate evidence: P-08 (held-out scenario storage) + P-21 (holdout discipline) + P-23 (blast radius). Falsifying scenario: if regression-fix cycles routinely require P-25 STRICT-mode bypass or escalate beyond the small-blast-radius regime, the substrate-first regression claim is wrong.

**DEC-1.a falsifier-discipline observation.** BF-S explicitly claims `brownfield` on 4-of-5 cells with 1 `n/a` (mvp). Per [DEC-1.a](../decisions-captured.md#d1--unification-verdict-no-methodology-serves-both-mandates-working-hypothesis-falsifiable-by-phase-8), this is evidence *for* the no-methodology-serves-both-mandates working hypothesis — BF-S is a mandate-specific candidate that does not pretend to serve both mandates. The Phase-8 lean-eval will pressure-test whether the `brownfield` claims hold operationally.

## §6 Open carries

Surfaced into Phase 7 (back-fill) / Phase 8 (lean-eval) / future ADRs per [BF-S substrate-requirements §5](../substrate-requirements/bf-s.md):

- **P-23 B7 residual-leakage rate (Phase-8 lean-eval candidate; Phase-3.5.5 BF-S forward action #2).** The transitive-closure side channel is mitigable to rate-limited count-and-aggregate but not eliminable. **Phase-8 measurement:** how much can an adversary exfiltrate via the count-and-aggregate side channel under realistic adversarial-budget constraints? **Status: accepted-as-RG; Phase 8 pressure-tests degradation magnitude.**

- **P-25 utility-tax calibration (partial-RG per [P-25 sketch](../primitives/P-25-camel-perimeter.md#research-grade-uncertainty-flag); accept-as-RG per [BF-S substrate-requirements §2](../substrate-requirements/bf-s.md)).** The ~7-point AgentDojo headline tax is buildable today; whether it holds for *this* factory's mix of work-unit-classes is empirically open. **Phase-8 measurement:** perimeter-on vs perimeter-off task-success delta per work-unit-class. Substrate exposes configurable per-work-unit-class bypass; calibration is per-deployment work, not substrate-layer work.

- **Stripe-scale self-reference accretion (Phase-8 lean-eval candidate; original pre-mortem finding).** Per the [BF-S registry entry](../candidate-registry.md#bf-s--brownfield-substrate-first-1): "BF-S fails first at Stripe scale (1300 PRs/week) due to self-reference accretion — the substrate refreshes from the factory's own output." Not addressed by sketches; remains accepted-open. P-07 (S-3) production telemetry as out-of-distribution ground truth is the F55 mitigation surface; the residual concern is empirical.

- **S-3 silent endpoint-drift detection (Phase-8 lean-eval candidate; on-call finding).** Telemetry endpoints can silently drift; the substrate must surface drift detection.

- **OQ-T4 cross-model judge sample-rate sufficiency (Phase-8 lean-eval candidate).** Whether sample-rate cross-model judging satisfies F1/F27 mitigation is an empirical question the corpus does not answer.

- **S-1 substrate-vendor choice for brownfield (Phase-5 ADR seed per OQ-T1).** OpenHands+Overstory vs Gas City vs tree-sitter+LSP vs Sourcegraph vs Glean. Phase-5 ADR work.

- **S-3 starting-condition handling when telemetry doesn't yet exist (Phase-5 ADR seed per OQ-T3).** First-work-unit-class adds telemetry under degraded-S-3 perimeter; substrate must accept the degraded-S-3 starting condition.

## §7 References

**ADR set (this spec's binding inputs).** Relative paths under `../../../docs/adr/`:

- Common substrate: [ADR 0010](../../../docs/adr/0010-p-01-sandbox-runtime.md), [ADR 0011](../../../docs/adr/0011-p-02-cost-ceilings.md), [ADR 0012](../../../docs/adr/0012-p-05-trajectory-capture.md), [ADR 0013](../../../docs/adr/0013-p-06-watchdog-tiers.md), [ADR 0014](../../../docs/adr/0014-p-07-telemetry-ingestor.md), [ADR 0015](../../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md), [ADR 0016](../../../docs/adr/0016-p-14-judge-router.md), [ADR 0017](../../../docs/adr/0017-p-22-polyglot-codebase-index.md), [ADR 0031 (P-23)](../../../docs/adr/0031-p-23-dependency-impact-graph.md).
- 2-candidate-fold substrate: [ADR 0033 (P-25 CaMeL perimeter)](../../../docs/adr/0033-p-25-camel-perimeter.md), [ADR 0035 (P-24 attribution store)](../../../docs/adr/0035-p-24-attribution-store.md).
- Discipline: [ADR 0018](../../../docs/adr/0018-discipline-bias-guard.md), [ADR 0019](../../../docs/adr/0019-discipline-cognitive-escrow.md), [ADR 0020](../../../docs/adr/0020-discipline-cost-ceiling.md), [ADR 0021](../../../docs/adr/0021-discipline-holdout.md), [ADR 0022](../../../docs/adr/0022-discipline-honesty.md), [ADR 0023](../../../docs/adr/0023-discipline-knowledge-promotion.md), [ADR 0024](../../../docs/adr/0024-discipline-regime-classification.md), [ADR 0025](../../../docs/adr/0025-discipline-scoping.md), [ADR 0026](../../../docs/adr/0026-discipline-three-loop.md), [ADR 0027](../../../docs/adr/0027-discipline-trifecta-closure.md).

**Supporting docs:**

- [BF-S candidate-registry entry](../candidate-registry.md#bf-s--brownfield-substrate-first-1)
- [BF-S substrate-requirements summary](../substrate-requirements/bf-s.md)
- [Brownfield-substrate-first track sketch](../tracks/brownfield-substrate-first.md)
- [Phase-4.2 overlap.md P-25 coverage tier (2-candidate fold)](../primitives/overlap.md#coverage-tier-summary-phase-5-adr-priority-signal)
- [Phase-4.2 overlap.md P-24 coverage tier (2-candidate fold)](../primitives/overlap.md#coverage-tier-summary-phase-5-adr-priority-signal)
- [DEC-1.a unification-verdict working hypothesis](../decisions-captured.md#d1--unification-verdict-no-methodology-serves-both-mandates-working-hypothesis-falsifiable-by-phase-8)
- [DEC-2 mandate-fit-per-(architecture × work-unit-class)](../decisions-captured.md#d2--mandate-fit-is-per-architecture--work-unit-class-not-per-architecture)
- [Phase-5-close handoff BF-S row](../SESSION-HANDOFF-2026-05-25-phase-5-close.md#candidate-set-state-at-phase-5-close)
- [auto-006 Phase-6 dispatch-shape brief](../decisions/auto-006-phase-6-dispatch-shape.md) — Round-2 rubric
- [U-C exemplar spec](u-c.md)
