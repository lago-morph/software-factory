---
candidate: gf-c
candidate-name: Bootstrap-Bench Factory
mandate-scope: greenfield
based-on-commit: c54daf1
based-on-date: 2026-05-26
mandate-fit:
  initial-spec: greenfield
  refactor: silent
  mvp: greenfield
  post-mvp-evolution: silent
  regression-fix: silent
---

# Architecture spec — GF-C (Bootstrap-Bench Factory)

## §0 ADR-citation index

| ADR ID | Title | Layer | Variant of | Citing § |
|---|---|---|---|---|
| 0010 | P-01 Sandbox runtime | common-substrate | — | §2, §3 |
| 0011 | P-02 Cost ceilings | common-substrate | — | §2, §4 |
| 0012 | P-05 Trajectory capture | common-substrate | — | §2, §3, §4 |
| 0013 | P-06 Watchdog tiers | common-substrate | — | §2, §4 |
| 0014 | P-07 Telemetry ingestor | common-substrate | — | §2, §3 |
| 0015 | P-08 Scenario storage with runner contract | designed-system-substrate | — | §2, §3 |
| 0016 | P-14 Judge router | common-substrate | — | §2, §3, §4 |
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
| 0032 | P-12 Deterministic linter framework | designed-system-substrate | — | §2, §3 |
| 0042 | P-11 Cold-start bench | orphan-substrate | — | §2, §3, §6 |
| 0043 | P-17 Intent crucible validator | orphan-substrate | — | §2, §3, §6 |
| 0044 | P-18 RSI declaration ledger | orphan-substrate | — | §2, §3, §6 |

**GF-C distinctive minimalism.** GF-C carries no framework-ADR + per-variant pairs. P-19/P-28/P-29/P-30 are not claimed as substrate primitives (per [gf-c.md §3](../substrate-requirements/gf-c.md)); the three orphan ADRs (0042/0043/0044) carry the load-bearing distinctive substance.

## §1 Overview

**Mandate.** Greenfield. GF-C is greenfield-only (per [gf-c.md §4](../substrate-requirements/gf-c.md): "`N/A (greenfield-only)`. X_UNM_B does not apply").

**Axis.** Cold-start posture. The day-0 bootstrap problem is treated as the *organising* problem, not as a section of a steady-state architecture. Every primitive, every methodology sub-phase, and every graduation criterion is shaped by "what does the factory need before any scenario, any prior trajectory, any holdout, any code exists?"

**Entry-mode.** Greenfield cold-start. The factory begins on day 0 with no codebase, no scenarios, no trajectories, no prior solutions. The first deliverable is *not code* — it is a validated Intent Crucible block plus an RSI declaration plus a small human-anchored Cold-Start Bench. Code generation is *gated* on bench sufficiency.

**Methodology summary.** Substrate-heavy at the day-0 layer; three-sub-phase cold-start methodology (Intent ingestion → Bench construction → First-cycle restraint) gated by a four-criterion graduation protocol transitioning Cold-Start Regime (L3-Augmentation) to Steady-State Regime (per-class L4-lights-out). Steady-state is a *downstream emergent regime*.

**Load-bearing claim.** Cold-start is the bootstrap discipline materialised as substrate primitives, not methodology defaults. P-11 (Cold-Start Bench), P-17 (Intent Crucible validator), and P-18 (RSI-Declaration Ledger) are the three orphan primitives that exist *only* because GF-C names them — the substrate-enforced answer to the five-`critical`-F-mode convergence (F1 / F25 / F40 / F41 / F46) at day 0. Every other candidate treats cold-start as a one-off; GF-C treats it as a recurring micro-phase that reactivates each time a new work-unit-class enters.

## §2 Substrate composition

GF-C carries three orphan-substrate ADRs beyond the common substrate baseline (0010-0017) and discipline ADRs (0018-0027). Critically, **GF-C does not claim any framework-ADR ↔ per-variant primitive**. Per [gf-c.md §3](../substrate-requirements/gf-c.md): "No contested-primitive references. GF-C does not name any of P-28, P-29, P-30, or P-19 (the Phase-4.2 same-vs-distinct candidates). No fixed sub-section headers needed." GF-C's load-bearing distinctiveness lives entirely in the orphans.

**Orphan substrate (the three day-0 primitives):**

- **P-11 Cold-Start Bench ([ADR 0042](../../../docs/adr/0042-p-11-cold-start-bench.md)).** HMAC-signed scenario store; the day-0 instance of [P-08 (ADR 0015)](../../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md) holdout substrate, instantiated *before* any code exists. ADR 0042's load-bearing decision: cold-start scenarios are a `scenario.kind=cold-start` partition tagged on P-08's substrate (no new storage substrate), the runner is P-08's runner-API verbatim with a `kind` filter, scenarios are operator-authored plus community-contributed via PR against the catalog, and the calibration metric is `% of catalog scenarios reaching automation-eligible regime within N cycles`. HMAC-SHA256 envelope via operator-controlled KMS key + OPA append-policy gate enforces the `bench-frozen` event (per [cluster-C3 P-11 sketch](../primitives/cluster-C3.md)). The bench is the **only out-of-distribution signal that exists before code exists** ([gf-c.md §1](../tracks/greenfield-cold-start-first.md)); without it, D-2's holdout substrate is vacuous on day 0. Mitigates F32 (signing) and underwrites the five-`critical`-F-mode convergence (F1 / F25 / F40 / F41 / F46) GF-C's track-axis defends against.

- **P-17 Intent Crucible validator ([ADR 0043](../../../docs/adr/0043-p-17-intent-crucible-validator.md)).** 9-field typed-object intake (identity, statement, business outcomes, capability scope, policy references, invariants, non-goals, decision seeds, guardrails / feedback sources) keyed to El Kaim Chapter 8. Three surfaces: `schema-validate(blob) → (parsed_block, [violations])`, `submit(block, author_id) → versioned commit to P-18`, `diff(va, vb)`. ADR 0043's load-bearing decision: build the substance-check surface as an LLM-judge ensemble dispatched through the [P-14 judge router (ADR 0016)](../../../docs/adr/0016-p-14-judge-router.md) under a dedicated `substance-check` judge role, with rubric-driven per-field evaluation and a `vacuous`-flag return path. The structural validator is bounded Pydantic v2 work; the *substance* check on `business_outcomes` and `capability_scope` is F41/F50-class semantic judgment — carried with two **partial-RG flags** per [gf-c.md §2](../substrate-requirements/gf-c.md). The rubric encodes three load-bearing questions per field: (1) testable acceptance criteria? (2) falsification surface? (3) cost ceiling? A `vacuous` or majority-`borderline` ensemble verdict blocks `submit` until the operator revises or invokes Council escalation. P-17 is the substrate-enforced first line of defence against F41 (Under-Defined-Intent Debt, greenfield `critical`) at authoring time — without it, methodology-Council depth alone is F53-fragile under operator-pressure.

- **P-18 RSI-Declaration Ledger ([ADR 0044](../../../docs/adr/0044-p-18-rsi-declaration-ledger.md)).** Append-only typed declaration ledger committing day-0 to whether the factory satisfies Kahana's three-part RSI test at steady-state. ADR 0044's load-bearing decision: build P-18 as an envelope-typed view on a typed-object content-addressed store substrate (Merkle-chained content-addressed JSON-blob entries; libgit2 ODB or Postgres `bytea + jsonb` + immutability trigger). Records initial RSI declaration, per-cycle AILCCP-control attestations, Human-Approval-Gate exercise events, board-report renderings, SB-53 reportability classifications, and declaration amendments (each a new append, never a rewrite). The `RSIDeclaration` envelope schema carries `subkind ∈ {declaration, attestation, gate-exercise, report-emit, sb53-classification, amendment}`, `agent_id`, `cycle_id`, `declared_scope`, `evidence_pointer`, `judge_verdict`, `operator_ack_state`, `prior_hash` (Merkle chain over kind-filtered sequence), plus operator signature on declaration and amendment subkinds. Closes [F43 RSI Board-Visibility Gap](../failure-modes-v3.md) at day 0 rather than retrofitted; contributes to F54 (goal subversion) and F55 (behavioural drift) closure. The append-only contract lives in the storage layer per F53 (voluntary-discipline fragility), not in the calling agent.

**Note on P-28 substrate borrow.** ADR 0044 implements P-18 by composing on the same content-addressed typed-object machinery other candidates name as their P-28 substrate primitive. GF-C does **not** name P-28 as a substrate primitive in its own right (per [gf-c.md §3](../substrate-requirements/gf-c.md)) — the composition is an implementation choice at the orphan-ADR level, not a framework-ADR ↔ per-variant pairing. GF-C carries no per-variant ADR and no framework citation in §0.

**Commodity substrate baseline.** [P-01 sandbox (ADR 0010)](../../../docs/adr/0010-p-01-sandbox-runtime.md), [P-02 (ADR 0011)](../../../docs/adr/0011-p-02-cost-ceilings.md), [P-05 (ADR 0012)](../../../docs/adr/0012-p-05-trajectory-capture.md), [P-06 (ADR 0013)](../../../docs/adr/0013-p-06-watchdog-tiers.md), [P-07 (ADR 0014)](../../../docs/adr/0014-p-07-telemetry-ingestor.md), [P-08 (ADR 0015)](../../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md), [P-14 (ADR 0016)](../../../docs/adr/0016-p-14-judge-router.md), [P-22 (ADR 0017)](../../../docs/adr/0017-p-22-polyglot-codebase-index.md). P-08 is what P-11 composes on (kind-filter partition). P-14 is what P-17's substance-check ensemble dispatches through. P-06's Patrol-tier is *structurally muted* during cold-start (no historical baseline); Daemon and Triage operate from cycle 1. P-22 is consumed post-first-cycle but is not load-bearing on day 0.

**Designed-system substrate.** [P-12 deterministic linter framework (ADR 0032)](../../../docs/adr/0032-p-12-deterministic-linter-framework.md) hosts the EARS + INCOSE GtWR rule library (per [gf-c.md §3](../substrate-requirements/gf-c.md): "P-12 is the engine, P-16 is the rule library."). The EARS five-pattern grammar and INCOSE GtWR R7 / R8 / R9 / R26 / R35 run as deterministic rule-function plug-ins inside P-12, addressing F38 / F18 / F51 at the authoring boundary. **This is deterministic perimeter, not LLM-as-judge** — explicit per [gf-c.md §5 protection 1](../tracks/greenfield-cold-start-first.md) and per avoidance of CTR-D6 (sycophancy-as-defensive-wrap at the authoring layer).

**X_UNM_B brownfield acquisition.** `N/A (greenfield-only)`. GF-C is a greenfield-mandate candidate; X_UNM_B does not apply.

## §3 Methodology shape

**Three sub-phases for cold-start** (per [gf-c.md §1.2](../tracks/greenfield-cold-start-first.md)).

**Sub-phase A — Intent ingestion.** Human authors 1–3 Intent Crucible blocks. The [P-17 validator (ADR 0043)](../../../docs/adr/0043-p-17-intent-crucible-validator.md) runs structural validation deterministically (Pydantic v2 + cross-field rules + [P-12 (ADR 0032)](../../../docs/adr/0032-p-12-deterministic-linter-framework.md) for form-checks via the EARS+GtWR rule library), then dispatches the substance-check ensemble through [P-14 (ADR 0016)](../../../docs/adr/0016-p-14-judge-router.md) under `judge_role='substance-check'`. A **Council** of agents (family-diverse model-mix per F46) interrogates form-correct + substance-passing blocks via INCOSE GtWR C1–C15 questions. The Council does not write code. Output: validated Intent committed to [P-18 (ADR 0044)](../../../docs/adr/0044-p-18-rsi-declaration-ledger.md) as `subkind=declaration`.

**Sub-phase B — Bench construction.** Human seeds 5–10 Kaner-style scenarios. Agents (different model family from the eventual builder, per F46) propose additions; human curates. Each scenario binds to ≥1 EARS criterion and ≥1 Intent invariant. The bench is **HMAC-signed** ([P-11 ADR 0042](../../../docs/adr/0042-p-11-cold-start-bench.md): HMAC-SHA256 envelope + OPA append-policy gate enforcing the `bench-frozen` event) and stored on P-08's `scenario.kind=cold-start` partition with `partition=holdout`. **Bench-construction agents never see the builder's prompts** — D-4 holdout enforced at the substrate via [P-01 sandbox (ADR 0010)](../../../docs/adr/0010-p-01-sandbox-runtime.md), not as voluntary discipline.

**Sub-phase C — First-cycle restraint.** A single Ubiquitous-pattern EARS criterion against a single scenario. Output is judged cross-model via [P-14 (ADR 0016)](../../../docs/adr/0016-p-14-judge-router.md); on disagreement, human escalation. Production scissors OFF; ships to [P-01 sandbox (ADR 0010)](../../../docs/adr/0010-p-01-sandbox-runtime.md). [P-05 trajectory capture (ADR 0012)](../../../docs/adr/0012-p-05-trajectory-capture.md) writes from cycle 1 — no prior trajectories on day 0, but capture is essential to populate the steady-state primitive.

**The graduation protocol (cold-start → steady-state).** Per [gf-c.md §1.3](../tracks/greenfield-cold-start-first.md), the factory transitions from Cold-Start Regime to Steady-State Regime only when four explicit, measured criteria are met:

1. **Bench saturation.** Bench contains ≥N scenarios covering ≥M Intent Crucible invariants such that discriminative power on a held-out paraphrase of the spec exceeds a stated threshold. (Concrete N/M deferred to Phase-6 ADR; the *requirement* that they be stated is the architectural commitment.)
2. **K=5 consistency baseline established.** ≥5 independent invocations on each of ≥3 bench scenarios; Jaymin's Augmentation-Mode bar (≥70% K=5 consistency) is clearable for the work-unit-classes proposed for automation-eligibility.
3. **Cross-model judge agreement rate measured.** Per F46 mitigation: cross-model review has produced ≥M consecutive cycles of agreement on the bench.
4. **RSI-declaration board-reporting cadence demonstrated.** If the factory declared it will meet Kahana's three-part test at steady-state, the board has received at least one [P-18 (ADR 0044)](../../../docs/adr/0044-p-18-rsi-declaration-ledger.md) `subkind=report-emit` rendering and acknowledged it (`operator_ack_state` set).

Until graduation, the factory operates at **L3-Augmentation** — human in every cycle. Post-graduation, work units are classified per [decisions-captured.md D2](../decisions-captured.md) mandate-fit-by-work-unit-class; only automation-eligible classes operate at L4-lights-out.

**Work-unit definition.** A *cold-start-typed* work unit is a `(scenario_id, EARS_criterion, Intent_invariant_binding)` triple drawn from the bench. [P-02 (ADR 0011)](../../../docs/adr/0011-p-02-cost-ceilings.md) cost ceilings are tight during cold-start; they graduate with the work-unit-class declaration.

**Distinctive methodology decisions.** Three:

- **Day-0 deliverable is not code — it is a validated Intent Crucible plus an RSI declaration plus a small bench.** [P-17 `submit`](../../../docs/adr/0043-p-17-intent-crucible-validator.md) is blocked until structural + substance validation passes; [P-18 (ADR 0044)](../../../docs/adr/0044-p-18-rsi-declaration-ledger.md) records the RSI declaration before any cycle runs; [P-11 bench (ADR 0042)](../../../docs/adr/0042-p-11-cold-start-bench.md) is HMAC-signed and frozen before sub-phase C. Code generation is *gated* on bench sufficiency.

- **Micro-cold-start per new work-unit-class.** Cold-start primitives reactivate for each new work-unit-class entry post-graduation. New-work-unit-class arrival is treated as a *re-entry* into sub-phases A → B → C scoped to that class. Graduation is per-class, not per-factory.

- **Cross-model judge mandatory at first cycles** (F1-greenfield-`critical`, F46-greenfield-`high`). At cold-start there is no prior K=5 history; the substrate enforces cross-model diversity via [P-14 (ADR 0016)](../../../docs/adr/0016-p-14-judge-router.md) rather than trusting single-model calibration. This adopts F46-mitigation over Anthropic's single-judge-is-fine position (CTR-D7, CTR-D8) for cold-start specifically: the Anthropic claim presumes a track record the cold-start factory does not have.

## §4 Discipline binding

GF-C binds all 10 discipline ADRs (0018-0027). Per-discipline binding:

- **Bias guard ([ADR 0018](../../../docs/adr/0018-discipline-bias-guard.md)).** Bound at the [P-14 judge router (ADR 0016)](../../../docs/adr/0016-p-14-judge-router.md): cross-model judging is mandatory during Cold-Start Regime (no K=5 history yet to license single-family review). Family-diverse model-mix is required at both the substance-check ensemble (ADR 0043) and the first-cycle restraint cross-model judge (ADR 0042 / §1.2 sub-phase C).

- **Cognitive escrow ([ADR 0019](../../../docs/adr/0019-discipline-cognitive-escrow.md)).** Bound at [P-05 (ADR 0012)](../../../docs/adr/0012-p-05-trajectory-capture.md) + Patrol-tier ([P-06 (ADR 0013)](../../../docs/adr/0013-p-06-watchdog-tiers.md)). At cold-start the operator is necessarily in the per-cycle inner loop; substrate-triggered STIR prompts in the prompt→response interval (per Kahana) replace voluntary discipline (F53 mitigation). DEC-2 routes the escrow primitive to methodology layer; GF-C honours this by treating the surface as substrate-enforced via [P-06 (ADR 0013)](../../../docs/adr/0013-p-06-watchdog-tiers.md) Patrol-tier triggers + operator-feedback hooks, not a typed `EscrowSurface` slot.

- **Cost ceiling ([ADR 0020](../../../docs/adr/0020-discipline-cost-ceiling.md)).** Bound at [P-02 (ADR 0011)](../../../docs/adr/0011-p-02-cost-ceilings.md). Cold-start cycles are tiny by §1.2 sub-phase C; cost ceilings are *easy* at cold-start scope. Cross-model judge ensemble cost (multiple inferences per cycle) is enforced per-call. Cost ceiling at steady-state graduates with the work-unit-class declaration.

- **Holdout ([ADR 0021](../../../docs/adr/0021-discipline-holdout.md)).** Bound at [P-08 (ADR 0015)](../../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md) — the Cold-Start Bench ([ADR 0042](../../../docs/adr/0042-p-11-cold-start-bench.md)) is a `kind=cold-start` partition with `partition=holdout`. Bench-construction agents and builder agents are isolated at the substrate layer ([P-01 (ADR 0010)](../../../docs/adr/0010-p-01-sandbox-runtime.md) sandboxing); D-4 is non-negotiable from cycle 1. F28 (holdout leakage greenfield `critical`) mitigation native.

- **Honesty ([ADR 0022](../../../docs/adr/0022-discipline-honesty.md)).** Bound at the graduation protocol. At cold-start the factory cannot claim to have cleared any empirical bar; the graduation protocol is the act of *earning* the claim. Until graduation, no automation-eligible work-unit-class exists. The track is explicit: "Honesty discipline: at cold-start the factory cannot claim to have cleared any empirical bar; the graduation protocol is the act of earning the claim" ([gf-c.md §2 OQ-B6](../tracks/greenfield-cold-start-first.md)).

- **Knowledge promotion ([ADR 0023](../../../docs/adr/0023-discipline-knowledge-promotion.md)).** Bound at the [P-11 bench (ADR 0042)](../../../docs/adr/0042-p-11-cold-start-bench.md) catalog-growth path: each cycle's discovered acceptance criteria are candidates for bench-PR promotion against the Kaner+EARS+invariant rubric. Promotion is gated by the eligibility-regime classifier (per ADR 0042 decision 3).

- **Regime classification ([ADR 0024](../../../docs/adr/0024-discipline-regime-classification.md)).** Bound at the graduation protocol per [gf-c.md §1.3](../tracks/greenfield-cold-start-first.md). Cold-Start Regime is uniformly L3-Augmentation; Steady-State Regime classifies per-work-unit-class. The transition is *per-class, not per-factory*. GF-C does not claim a P-19 substrate primitive; regime classification is methodology-layer at the graduation gate.

- **Scoping ([ADR 0025](../../../docs/adr/0025-discipline-scoping.md)).** Bound at sub-phase C first-cycle restraint: a single Ubiquitous EARS criterion against a single scenario. Per-cycle scope is explicitly bounded by Yang et al.'s ≤10-simultaneous-requirements ceiling (F36 mitigation).

- **Three-loop ([ADR 0026](../../../docs/adr/0026-discipline-three-loop.md)).** Bound at the three-sub-phase methodology (A intent ingestion → B bench construction → C first-cycle restraint) and at the graduation protocol's measurement loop. Compound-style plan→work→review→compound runs per cycle; the "compound" step at cold-start writes to [P-05 (ADR 0012)](../../../docs/adr/0012-p-05-trajectory-capture.md) and to the [P-11 catalog (ADR 0042)](../../../docs/adr/0042-p-11-cold-start-bench.md) (PR-against-bench mechanism).

- **Trifecta closure ([ADR 0027](../../../docs/adr/0027-discipline-trifecta-closure.md)).** Bound at the [P-08 holdout (ADR 0015)](../../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md) + the [P-12 deterministic linter (ADR 0032)](../../../docs/adr/0032-p-12-deterministic-linter-framework.md) + the [P-17 structural validator (ADR 0043)](../../../docs/adr/0043-p-17-intent-crucible-validator.md). All three are substrate-enforced.

**Disciplines GF-C is silent on.** None — GF-C binds all 10 disciplines. The honesty discipline's earned-bar framing is the substantive cold-start contribution: lights-out is not declared, it is *earned* by graduation.

## §5 Mandate fit

GF-C's mandate-fit YAML block (in this spec's frontmatter) restated per work-unit-class:

- **initial-spec: greenfield.** Initial-spec authoring is GF-C's canonical day-0 work-unit-class. The Intent Crucible authoring session ([P-17 ADR 0043](../../../docs/adr/0043-p-17-intent-crucible-validator.md) + Council interrogation per §1.2 sub-phase A) *is* the initial-spec work unit. No other candidate centres this surface as substrate. Supporting substrate evidence: ADR 0043 (substance-check ensemble), ADR 0044 (RSI declaration as append), ADR 0042 (bench seeded before first build cycle). Falsifying scenario: if operators on greenfield can produce code *without* first passing the Intent Crucible substance gate, GF-C's day-0-deliverable-is-not-code claim is wrong. GF-C is silent on brownfield initial-spec (X_UNM_B is N/A per §2).

- **refactor: silent.** GF-C takes no position on refactor work-units. Refactoring presupposes a steady-state codebase; GF-C's design centre is day 0 before code exists. Post-graduation, refactor work units would be handled by whatever methodology the work-unit-class declaration adopts — but GF-C makes no claim on the steady-state refactor surface. This is `silent`, not `n/a` — silence is not a rejection.

- **mvp: greenfield.** MVP authoring is GF-C's primary post-Intent work-unit-class. The bench seeds against the operator-authored intent block; sub-phase C first-cycle restraint runs the MVP's first build cycle against a single EARS criterion. Anchor set thickens as MVP cycles deposit live-tests and architecture-rules. Supporting substrate evidence: ADR 0042 (bench-as-MVP-ground-truth), ADR 0043 (Intent invariants binding scenarios), ADR 0044 (declared scope at MVP start). Falsifying scenario: if MVP work units never accumulate enough bench coverage to clear graduation criterion 1 (bench saturation), GF-C's earned-graduation claim is wrong. Brownfield MVP is `silent` — not a canonical GF-C work-unit-class.

- **post-mvp-evolution: silent.** Post-MVP evolution operates against a thickened anchor set and a graduated work-unit-class taxonomy; GF-C does not claim a post-graduation methodology. The micro-cold-start re-entry mechanism (§3) is GF-C's only post-graduation surface: when a new work-unit-class enters, sub-phases A → B → C reactivate scoped to that class. Post-MVP work *within* a graduated class is downstream of GF-C's design centre.

- **regression-fix: silent.** Regression-fix presupposes a failing test and a steady-state codebase; GF-C's day-0 design centre is before tests exist. The Cold-Start Bench provides the *initial* test set, but regression-fix work units operating against an established test suite are not a canonical GF-C work-unit-class. `silent`, not `n/a`.

**DEC-1.a falsifier-discipline observation.** GF-C explicitly claims `greenfield` on 2 of 5 work-unit-classes (initial-spec, mvp) and is `silent` on the other 3. Per [DEC-1.a](../decisions-captured.md), the `silent` posture is evidence *for* the no-methodology-serves-both-mandates working hypothesis: GF-C is making no unification claim. The Phase-8 lean-eval will pressure-test the two `greenfield` claims (initial-spec and mvp), particularly whether the substance-check ensemble (ADR 0043) actually salvages thin operator intent or converges to click-through over multi-month cold-start.

## §6 Open carries

Surfaced into Phase 7 (back-fill) / Phase 8 (lean-eval) / future ADRs:

- **OQ-6 operator-intent-illiteracy resilience (Phase-8 lean-eval candidate, biggest single OQ).** Per [gf-c.md §5](../substrate-requirements/gf-c.md) and [track §7 q.6](../tracks/greenfield-cold-start-first.md): does the Council-interrogation methodology actually salvage thin operator intent, or does it converge to click-through over a multi-month cold-start? The pre-mortem walks the 18-month "thin-intent → click-through-STIR → F40" failure cascade. This is GF-C's biggest unresolved exposure and the most-likely Phase-3 adversarial attack surface. **Status: Phase-8 lean-eval; pressure-tests the P-17 substance-check ensemble (ADR 0043) and Council interrogation depth.**

- **P-17 substance-check reliability and ensemble agreement (Phase-5 ADR carry, partial-RG flags).** Per ADR 0043 and [gf-c.md §2](../substrate-requirements/gf-c.md): the substance-check on `business_outcomes` and `capability_scope` is F41/F50-class semantic judgment. Two partial-RG flags carry: (i) substance-check reliability (stable verdicts on thin-vs-rich Intents?), (ii) cross-family ensemble agreement convergence on this rubric. **Status: Phase-8 lean-eval candidates.**

- **Bench-saturation N / M concrete values (Phase-6 ADR carry).** Per [gf-c.md §1.3](../tracks/greenfield-cold-start-first.md) graduation criterion 1: concrete N (scenario count) and M (invariant coverage) are deferred. Yang et al.'s ≤10-simultaneous-requirements ceiling is the only hard anchor. **Status: Phase-6 ADR; lean-eval-instrumentable.**

- **Cross-model judge agreement-rate baseline (Phase-8 lean-eval candidate).** Graduation criterion 3 is named but the baseline rate is unmeasured in the corpus. CTR-E6 (CaMeL ~7-point utility tax) is the closest empirical anchor; cross-model judging cost at cold-start scale is not. **Status: Phase-8 measures the baseline.**

- **HMAC-key custody (Phase-5 ADR seed).** Per [gf-c.md §5](../substrate-requirements/gf-c.md): Yubikey vs cloud KMS vs Vault Transit for the [P-11 (ADR 0042)](../../../docs/adr/0042-p-11-cold-start-bench.md) bench-frozen HMAC. **Status: deferred ADR.**

- **Intent-richness probe construction (DPG-10 / Phase-5 wave-1 ADR carry).** Per [P-17 sketch](../primitives/P-17-intent-crucible-validator.md) and [gf-c.md §5](../substrate-requirements/gf-c.md): the substantive Council-interrogation-depth ADR is owed. The methodology layer carries the residual F41 closure burden the substrate alone cannot fully close. **Status: Phase-5 wave-1 ADR seed.**

- **F43 / RSI Caremark board-reporting Phase-7 / Phase-8 carries.** Per [gf-c.md §5 F-mode carries](../substrate-requirements/gf-c.md): F43 (RSI Board-Visibility Gap) is **structurally closed at day 0 via [P-18 (ADR 0044)](../../../docs/adr/0044-p-18-rsi-declaration-ledger.md)** per the sketch. Residual carries: (i) per-cycle AILCCP-control attestation *running* vs *scaffolded* (the regulator critique's Hughes-trappings risk flagged in [candidate-registry GF-C](../candidate-registry.md)); (ii) SB-53 classification rubric is out of scope of ADR 0044 — P-18 stores the classification, it does not derive it; (iii) F54 (goal subversion, greenfield `high`) and F55 (behavioural drift, greenfield `critical`) contribute via the durable declared-objective record but full closure is Phase-8 lean-eval. **Status: Phase-7 back-fill on Caremark prong-1 reporting cadence; Phase-8 lean-eval on attestation-running vs scaffolded.**

- **P-16 ↔ P-12 absorption (Phase-4.2 verdict, resolved).** Per [gf-c.md §3](../substrate-requirements/gf-c.md): the P-16 EARS+GtWR linter is hosted inside [P-12 (ADR 0032)](../../../docs/adr/0032-p-12-deterministic-linter-framework.md) as a rule library — P-12 is the engine, P-16 is the rule content. No separate primitive needed.

## §7 References

**ADR set (this spec's binding inputs).** Per the §0 ADR-citation index above; relative paths under `../../../docs/adr/`:

- Common substrate: [ADR 0010](../../../docs/adr/0010-p-01-sandbox-runtime.md), [ADR 0011](../../../docs/adr/0011-p-02-cost-ceilings.md), [ADR 0012](../../../docs/adr/0012-p-05-trajectory-capture.md), [ADR 0013](../../../docs/adr/0013-p-06-watchdog-tiers.md), [ADR 0014](../../../docs/adr/0014-p-07-telemetry-ingestor.md), [ADR 0015](../../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md), [ADR 0016](../../../docs/adr/0016-p-14-judge-router.md), [ADR 0017](../../../docs/adr/0017-p-22-polyglot-codebase-index.md).
- Designed-system substrate: [ADR 0032 (P-12 deterministic linter framework)](../../../docs/adr/0032-p-12-deterministic-linter-framework.md).
- Orphan substrate (GF-C-specific): [ADR 0042 (P-11 Cold-Start Bench)](../../../docs/adr/0042-p-11-cold-start-bench.md), [ADR 0043 (P-17 Intent Crucible validator)](../../../docs/adr/0043-p-17-intent-crucible-validator.md), [ADR 0044 (P-18 RSI Declaration Ledger)](../../../docs/adr/0044-p-18-rsi-declaration-ledger.md).
- Discipline: [ADR 0018](../../../docs/adr/0018-discipline-bias-guard.md), [ADR 0019](../../../docs/adr/0019-discipline-cognitive-escrow.md), [ADR 0020](../../../docs/adr/0020-discipline-cost-ceiling.md), [ADR 0021](../../../docs/adr/0021-discipline-holdout.md), [ADR 0022](../../../docs/adr/0022-discipline-honesty.md), [ADR 0023](../../../docs/adr/0023-discipline-knowledge-promotion.md), [ADR 0024](../../../docs/adr/0024-discipline-regime-classification.md), [ADR 0025](../../../docs/adr/0025-discipline-scoping.md), [ADR 0026](../../../docs/adr/0026-discipline-three-loop.md), [ADR 0027](../../../docs/adr/0027-discipline-trifecta-closure.md).

**Supporting docs:**

- [GF-C candidate-registry entry](../candidate-registry.md#gf-c--greenfield-cold-start-first)
- [GF-C substrate-requirements summary](../substrate-requirements/gf-c.md)
- [Greenfield-cold-start-first track sketch](../tracks/greenfield-cold-start-first.md)
- [P-17 buildability sketch](../primitives/P-17-intent-crucible-validator.md)
- [P-18 buildability sketch](../primitives/P-18-rsi-declaration-ledger.md)
- [P-11 cluster-C3 sketch](../primitives/cluster-C3.md)
- [DEC-1.a unification-verdict working hypothesis](../decisions-captured.md)
- [DEC-2 mandate-fit-per-(architecture × work-unit-class)](../decisions-captured.md)
- [auto-006 Phase-6 dispatch-shape brief](../decisions/auto-006-phase-6-dispatch-shape.md) — this spec is authored under its Round-2 rubric.
- [Phase-5-close session handoff](../SESSION-HANDOFF-2026-05-25-phase-5-close.md) — GF-C ADR set row.
