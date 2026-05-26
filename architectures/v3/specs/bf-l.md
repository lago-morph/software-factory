---
candidate: bf-l
candidate-name: Brownfield, legacy-ingestion-first
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

# Architecture spec — BF-L (Brownfield, legacy-ingestion-first)

## §0 ADR-citation index

| ADR ID | Title | Layer | Variant of | Citing § |
|---|---|---|---|---|
| 0010 | P-01 Sandbox runtime | common-substrate | — | §2, §4 |
| 0011 | P-02 Cost ceilings | common-substrate | — | §2, §4 |
| 0012 | P-05 Trajectory capture | common-substrate | — | §2, §3, §4 |
| 0013 | P-06 Watchdog tiers | common-substrate | — | §2, §3, §4 |
| 0014 | P-07 Telemetry ingestor | common-substrate | — | §2, §3 |
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
| 0026 | Discipline — three-loop | discipline | — | §3, §4 |
| 0027 | Discipline — trifecta closure | discipline | — | §4 |
| 0028 | P-19 Eligibility / regime classifier framework | common-substrate | — | §2, §3 |
| 0031 | P-23 Dependency-impact graph | common-substrate | — | §2, §3 |
| 0034 | P-27 Archaeological-brief tooling | 2-candidate-fold-substrate | — | §2, §3 |
| 0035 | P-24 Attribution store | 2-candidate-fold-substrate | — | §2, §3 |
| 0036 | P-30 Event registrar substrate | common-substrate | — | §2, §3 |
| 0047 | P-26 Codebase Model | orphan-substrate | — | §2, §3, §4 |
| 0048 | P-13 Maintenance loop | orphan-substrate | — | §2, §3, §4 |
| 0049 | BF-L P-19 variant — per-region feature source | per-variant-substrate | 0028 | §2, §3 |

**Framework + per-variant pairing check.** BF-L claims framework 0028 (P-19) and pairs it with 0049 (BF-L per-region variant) per [AGENTS-MD-a9fb7b42f8](../../../AGENTS.md#framework-adr-scope-boundary-discipline). BF-L does NOT claim frameworks 0029 (P-28 typed-object store), 0030 (P-29 policy mediator), or 0036 (P-30 event registrar) as load-bearing typed-envelope substrates — but 0036 IS consumed (without per-variant binding) by P-13 maintenance-loop dispatch ([ADR 0048](../../../docs/adr/0048-p-13-maintenance-loop.md)), so 0036 appears in §0 as a commodity dispatch surface, not as a framework requiring BF-L per-variant authorship. ADRs **0034 (P-27 archaeological-brief)** and **0035 (P-24 attribution)** are 2-candidate-fold substrates (BF-M+BF-L, BF-S+BF-L respectively); BF-L's per-region usage shapes are recorded in this spec's §2/§3 but the underlying ADRs are shared. **0047 (P-26 Codebase Model)** and **0048 (P-13 maintenance loop)** are BF-L orphan substrates (per the [Phase-4.2 overlap.md orphan list](../primitives/overlap.md#coverage-tier-summary-phase-5-adr-priority-signal)). Total ADR rows: 25.

## §1 Overview

**Mandate.** Brownfield-only. BF-L explicitly does not extend to greenfield — its load-bearing claim is structurally tied to *existing code* that the factory ingests, indexes, and reconciles. The [unified-attempt question](../decisions-captured.md#d1--unification-verdict-no-methodology-serves-both-mandates-working-hypothesis-falsifiable-by-phase-8) is left to U-A/U-B/U-C/D7-U-1.

**Axis.** *Code-archaeology is the primary organizing principle.* Per the [BF-L track §0](../tracks/brownfield-legacy-ingestion-first.md), the factory's first move on any new brownfield codebase is a dedicated **ingestion phase** that produces a durable, machine- and human-readable model of what is already there — structure, conventions, test patterns, hot paths, debt clusters, idioms, latent invariants, runtime traces. Every downstream choice (work-unit shape, substrate primitive set, gate definitions, regime classification, scenario library) is *derived from the ingestion artifact*, not assumed in advance. The artifact is the **P-26 Codebase Model** — six views, integrated.

**Entry-mode.** Brownfield by construction — an operator delivers an existing repository with git history, CI logs (where present), runtime telemetry (where present), and existing test suites. BF-L's day-0 problem is *legacy ingestion* — the brownfield analogue of greenfield cold-start ([BF-L track §5](../tracks/brownfield-legacy-ingestion-first.md)).

**Methodology summary.** Three loops over the Codebase Model. **Loop 1 (Ingestion)** — deep, slow, runs once per codebase plus on declared triggers; produces the six-view artifact. **Loop 2 (Work)** — per-cycle, methodology-shaped, *queries* the model; work-unit-class taxonomy is derived from the model's profile, not pre-decided. **Loop 3 (Maintenance)** — continuous low-cadence reconciliation (per [ADR 0048](../../../docs/adr/0048-p-13-maintenance-loop.md)) between the Codebase Model and reality. Scenarios are *inherited* from the model (explicit challenge to D-2); regime classification is *per-region* (per [ADR 0049](../../../docs/adr/0049-p-19-variant-bf-l-per-region.md)).

**Load-bearing claim.** The Codebase Model is the primary substrate primitive; methodology is thin and *parameterised by ingestion fidelity*. Per [primitives/index.md](../primitives/index.md), this is "the most ambitious primitive in the catalog" — 9–18 engineer-months realistic. BF-L survives [Phase-3.5.5](../candidate-registry.md#phase-355-rule-on-load-bearing-rg-primitives-binding-user-approved-2026-05-25) with an honest research-grade-uncertainty flag on two of six views, and Phase-4 Wave-4.5 smoke-tests passed 3/3 languages on both gated views.

## §2 Substrate composition

BF-L's substrate carries 8 common-substrate ADRs (0010-0017), 10 discipline ADRs (0018-0027), one framework ADR with its per-variant pair (0028+0049), two 2-candidate-fold ADRs (0034, 0035), one commodity dispatch ADR (0036), and **two BF-L orphan ADRs (0047 P-26 Codebase Model, 0048 P-13 maintenance loop)**. The orphan pair is where the spec's distinctive substrate content lives.

### 2.1 The Codebase Model (load-bearing orphan)

**[ADR 0047 (P-26 Codebase Model)](../../../docs/adr/0047-p-26-codebase-model.md)** records the integrated six-view artifact. Per the [Phase-4.2 overlap.md orphan list](../primitives/overlap.md#coverage-tier-summary-phase-5-adr-priority-signal), P-26 is verbatim:

> **"Orphan (claimed by 1 candidate, 16 primitives): P-03, P-04, P-10, P-11, P-13, P-15, P-17, P-18, P-20, P-21, **P-26**, P-31, P-32, P-33, P-34 — candidate-specific ADRs only; preserved per scoping principle as cross-pollination fuel."**

The substrate-requirements summary names P-26 the load-bearing primitive: *"BF-L's contract is the integrated six-view artifact, not a federation of separate stores: common ID space (structural symbol IDs), join API (`model.join(symbol, version, [views])`), snapshot consistency at version boundaries, Merkle-DAG incremental versioning. The integration discipline IS what distinguishes BF-L from BF-S"* (per [bf-l.md §3](../substrate-requirements/bf-l.md#3-candidate-specific-contracts-on-each-primitive)).

**The six views (per [ADR 0047 § Decision](../../../docs/adr/0047-p-26-codebase-model.md)).**

1. **Structural view.** Tree-sitter parsers + SCIP records define the symbol-ID space (`{language, qname, source-revision}` + stable hash). Composes [P-22 polyglot codebase index (ADR 0017)](../../../docs/adr/0017-p-22-polyglot-codebase-index.md) and [P-23 dependency-impact graph (ADR 0031)](../../../docs/adr/0031-p-23-dependency-impact-graph.md). **Verdict: designed-system.** No RG flag.

2. **Conventional view.** Idiom register, lint conventions, test patterns. Per [auto-003 Round 2](../decisions/auto-003-bfl-rg-view-choice.md#decision-round-2), this view entered Phase-4 with a **research-grade-uncertainty (RG) flag**. BF-L's choice per the registry's verbatim application table row: *"BF-L | P-26 conventional view | **candidate's choice at Phase 4 entry** | Default if no choice declared: (b) accept-as-RG. BF-L may opt-in to (a) bounded sub-track for some or all of: LLM-with-structured-output + golden corpus of ≥20 idiomatic patterns per supported language."* BF-L opted to **option A′ smoke-test-first**; the Wave-4.5 [conventional smoke-test](../sub-tracks/bfl-conventional-smoke-test.md) **passed 3/3 languages** (Python Django 5.0 / TypeScript VS Code 1.95.0 / Java Spring 6.1.0 — 9 non-trivial conventions). **Wave-4.5b scaling owed at Phase 5/6 to ≥10-per-language.** Carried as a Phase-8 lean-eval candidate per [§6](#6-open-carries).

3. **Historical view.** Commit cadence per area, churn hotspots, attribution. Composes [P-24 attribution store (ADR 0035)](../../../docs/adr/0035-p-24-attribution-store.md) — BF-L is the second claimant ("BF-L via P-26 composes it" per [overlap.md](../primitives/overlap.md#coverage-tier-summary-phase-5-adr-priority-signal)). Verdict: designed-system, no RG flag.

4. **Runtime view.** Production traces, error fingerprints, performance hot paths where telemetry exists. Composes [P-07 telemetry ingestor (ADR 0014)](../../../docs/adr/0014-p-07-telemetry-ingestor.md). Tags spans with source-symbol qnames at ingest. Verdict: designed-system, no RG flag.

5. **Invariant view.** Extracted from tests, types, runtime assertions, schema constraints. Entered Phase-4 with an **RG flag**. BF-L's choice per the registry's verbatim application table row: *"BF-L | P-26 invariant view | **candidate's choice at Phase 4 entry** | Default if no choice declared: (b) accept-as-RG. BF-L may opt-in to (a) bounded sub-track: Daikon-style runtime inference + ≥5 invariants per language."* Same option-A′ smoke-test-first choice; the Wave-4.5 [invariant smoke-test](../sub-tracks/bfl-invariant-smoke-test.md) **passed 3/3 languages** (Django 4.2.11 / TanStack Query v5.28.0 / Spring 6.1.5 — 12 non-trivial invariants across tiers T1+T2+T3, with T4 Daikon-style runtime explicitly deferred per research-notes recommendation). Carried as a Phase-8 lean-eval candidate per [§6](#6-open-carries).

6. **Debt view.** TODOs, deprecation markers, known-bad regions, dependency staleness, Caremark/RSI exposure tags. Verdict: designed-system, no RG flag. Caremark tagging is the load-bearing input to [ADR 0049](../../../docs/adr/0049-p-19-variant-bf-l-per-region.md)'s OPA hard-floor.

**Integration discipline (per [ADR 0047 Layer 3](../../../docs/adr/0047-p-26-codebase-model.md)).** The six views are not co-located stores; they are joined through a common symbol-ID space (Layer 1) with a per-region typed-envelope join API at Layer 3: `model.join(symbol, version, [views]) → { structural, conventional, historical, runtime, invariant, debt }`. Snapshot consistency at version boundaries: a `version` token (git-commit + ingestion-pass ID) resolves a coherent view across all six. Without integration, BF-L collapses to BF-S (six co-located stores) and forfeits the "three loops over *one* model" load-bearing claim.

**Methodology-degradation clause (per [ADR 0047](../../../docs/adr/0047-p-26-codebase-model.md) + [auto-003 Round 2](../decisions/auto-003-bfl-rg-view-choice.md#methodology-degradation-clause-new-per-reviewer-2-a2)).** If conventional view falls back to (b) accept-as-RG at Wave-4.5b close, the eligibility function loses convention-density as a feature; cycles touching regions with no convention coverage default to L3 (not L4 lights-out), pending operator approval. If invariant view falls back, the scenario-derivation primitive (P-27) cannot pre-condition derived scenarios on invariant-satisfaction; derived scenarios are flagged "invariant-unconditioned" and routed to cross-family review rather than to L4 acceptance. **This spec carries both clauses regardless of Wave-4.5b verdict** — they are the structural defense that makes (b) fallback operationally viable rather than a fig leaf.

### 2.2 The maintenance loop (orphan)

**[ADR 0048 (P-13 maintenance loop)](../../../docs/adr/0048-p-13-maintenance-loop.md)** records BF-L's Loop-3 substrate. Per [overlap.md](../primitives/overlap.md#orphan-claimed-by-1-candidate-16-primitives), P-13 is a BF-L orphan — no other candidate claims it. Construction is commodity (cron + reconciliation worker + diff), but the *binding policy content* — drift signals, region prioritisation, dispatch surface — is BF-L-specific.

- **Cadence.** Per-codebase, slow axis (default: nightly inspection, weekly full reconciliation; per-deployment-tunable per [ADR 0026's three-loop discipline](../../../docs/adr/0026-discipline-three-loop.md)). Cycle-driven Loop-2 has its own cadence; session-driven trajectory has another; P-13 is the slowest of the three.
- **Drift signals.** Three classes: (1) test-coverage decay (runtime view of P-26); (2) runtime telemetry anomalies via [P-07 (ADR 0014)](../../../docs/adr/0014-p-07-telemetry-ingestor.md) — error-rate spikes, latency shifts; (3) churn cadence shift (historical view, >2σ from rolling baseline).
- **Per-region prioritisation.** Composite weight = drift-signal magnitude × debt-cluster membership × Caremark/RSI exposure tag. RSI-tracked or Caremark-tagged regions surface first.
- **Dispatch.** The inspector does not run reconciliation work itself; it emits typed `maintenance-trigger` events to [P-30 event-registrar (ADR 0036)](../../../docs/adr/0036-p-30-event-registrar-substrate.md). BF-L's methodology subscribes and dispatches per-region reconciliation cycles that re-ingest deltas, refresh affected views, and emit attribution per [P-24 (ADR 0035)](../../../docs/adr/0035-p-24-attribution-store.md).

P-13 is BF-L's structural defense against F20 (maintenance-vs-greenfield asymmetry, brownfield-critical), F34 (cross-layer drift), F55 (behavioural drift), F57 (design-authority erosion).

### 2.3 The per-region regime classifier (framework + per-variant pair)

Per [AGENTS-MD-a9fb7b42f8](../../../AGENTS.md#framework-adr-scope-boundary-discipline), framework ADR 0028 (P-19) must be paired with BF-L's per-variant ADR 0049.

The verbatim [Phase-4.2 overlap.md verdict on P-19](../primitives/overlap.md#p-19-eligibility--regime-classifier--four-contested-variants):

> **"Verdict: SAME primitive (P-19 classifier framework), DISTINCT feature sources + distinct output regime sets. All four share the construction recipe (Drools/OPA Rego decision tables + LLM-judge fallback via P-14 + OPA hard-floor post-check per [P-19 sketch](../../architectures/v3/primitives/P-19-eligibility-regime-classifier.md)). The differences are at the *feature engineering* layer and the *output enum* layer, not the *decision-engine* layer."**

The verbatim overlap.md row for BF-L's variant:

> **"Per-region | BF-L | Code-region features from Codebase Model (P-26): test-coverage, runtime telemetry, churn cadence, Caremark/RSI tag, debt-cluster, idiom-conformance (conditional), invariant-density (conditional) | Per-region regime (output regime is per region, not per cycle)"**

- **Framework: [ADR 0028](../../../docs/adr/0028-p-19-eligibility-regime-classifier.md).** Decision-table engine (OPA Rego preferred, Drools acceptable); LLM-judge fallback via [P-14 (ADR 0016)](../../../docs/adr/0016-p-14-judge-router.md); OPA hard-floor post-check. Inherited unchanged.
- **BF-L per-variant: [ADR 0049](../../../docs/adr/0049-p-19-variant-bf-l-per-region.md).** Three components: (1) **Per-region feature extractor** joins on the Codebase Model's structural symbol ID space at a fixed snapshot version to produce a feature vector `{test_coverage_density, runtime_telemetry_density, churn_cadence_90d, caremark_rsi_tag, debt_cluster_id, idiom_conformance_score?, invariant_density_score?}` — `?`-suffixed fields are conditional on Wave-4.5b verdicts. (2) **Per-region classification** by OPA Rego with hard floors: `caremark_rsi_tag = true → never automation-eligible`; debt-cluster → at-most `augmentation-required`; coverage-density < threshold AND telemetry-density < threshold → `human-required`. (3) **Cycle-level rollup**: a cycle touching multiple regions inherits the **strictest** per-region classification (max over the regime lattice). Per [ADR 0049](../../../docs/adr/0049-p-19-variant-bf-l-per-region.md), this is the load-bearing answer to BF-L's CTR-A4 / L5 mapping question — without per-region granularity, BF-L cannot honor the discipline that *different regions of the same codebase carry different stakes*.

### 2.4 Scenario-derivation tooling and attribution (2-candidate-fold pair)

- **[ADR 0034 (P-27 archaeological-brief tooling)](../../../docs/adr/0034-p-27-archaeological-brief-tooling.md).** 2-candidate-fold (BF-M+BF-L). BF-L uses P-27 at *ingestion time* for context briefs over codebase regions (same construction shape as BF-M's per-cycle brief, different output envelope). Per [bf-l.md §3](../substrate-requirements/bf-l.md#3-candidate-specific-contracts-on-each-primitive), scenarios are **inherited from the Codebase Model**, not authored out-of-tree (BF-L's explicit challenge to D-2). New scenarios are *derived* from gaps in the model.
- **[ADR 0035 (P-24 attribution store)](../../../docs/adr/0035-p-24-attribution-store.md).** 2-candidate-fold (BF-S+BF-L). BF-L consumes P-24 as the *historical view* — not as a separate substrate. Per [ADR 0035 § Context](../../../docs/adr/0035-p-24-attribution-store.md), "BF-L's [Codebase Model historical view](../primitives/P-26-codebase-model.md) consumes these queries; it does not own storage."

### 2.5 Held-out partition enforcement

**[ADR 0015 (P-08 scenario storage)](../../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md).** Substrate marks subsets of the Codebase Model itself as held-out (`partition=train|holdout` tag attaches to *model-derived* scenarios per [bf-l.md §3 P-08 contract](../substrate-requirements/bf-l.md#3-candidate-specific-contracts-on-each-primitive)). Ingestion-aware judges enforce the partition. Same OPA-mediated ABAC default contract as the [P-08 sketch](../primitives/cluster-C3.md); specialization at the integration layer.

### 2.6 Commodity substrate baseline

[P-01 sandbox (ADR 0010)](../../../docs/adr/0010-p-01-sandbox-runtime.md); [P-02 cost ceilings (ADR 0011)](../../../docs/adr/0011-p-02-cost-ceilings.md) — with per-loop parameterisation (ingestion has higher one-time ceiling than per-cycle work); [P-05 trajectory capture (ADR 0012)](../../../docs/adr/0012-p-05-trajectory-capture.md) — trajectories from ingestion *become* part of the Codebase Model (D-7 acceptance with BF-L specialization per [BF-L track §4](../tracks/brownfield-legacy-ingestion-first.md#4-defaults-accepted-vs-challenged-all-7-marked)); [P-06 watchdog tiers (ADR 0013)](../../../docs/adr/0013-p-06-watchdog-tiers.md) — Triage tier parameterised by the Codebase Model (stalled agent in low-coverage area triggers earlier than in high-coverage area); [P-22 polyglot index (ADR 0017)](../../../docs/adr/0017-p-22-polyglot-codebase-index.md), [P-23 dependency-impact graph (ADR 0031)](../../../docs/adr/0031-p-23-dependency-impact-graph.md), [P-07 telemetry (ADR 0014)](../../../docs/adr/0014-p-07-telemetry-ingestor.md) — all composed *into* P-26 as the structural / runtime view substrate; [P-14 judge router (ADR 0016)](../../../docs/adr/0016-p-14-judge-router.md), [P-30 event registrar (ADR 0036)](../../../docs/adr/0036-p-30-event-registrar-substrate.md).

**X_UNM_B articulation.** Not applicable. Per [bf-l.md §4](../substrate-requirements/bf-l.md#4-x_unm_b-articulation), BF-L is brownfield-only and **IS the candidate that articulates Codebase Model construction directly** — the X_UNM_B finding names BF-L's Codebase Model as the load-bearing primitive that *other* (unified-attempt) candidates owe an acquisition story for. BF-L itself does not have a Codebase-Model-acquisition gap to articulate; the construction *is* its thesis.

## §3 Methodology shape

BF-L's methodology layer is intentionally *thin* — the substrate's Codebase Model carries the load-bearing work. Per the [BF-L track §1](../tracks/brownfield-legacy-ingestion-first.md), the architecture has **three loops over a single durable artifact**, each binding to [ADR 0026 the three-loop discipline](../../../docs/adr/0026-discipline-three-loop.md) at a distinct cadence.

### 3.1 Loop 1: Ingestion (deep, slow, run once + refresh on triggers)

A dedicated multi-agent ingestion phase whose deliverable is the Codebase Model. Inputs: the repository, git history, CI logs, runtime telemetry, existing tests, existing docs, AGENTS.md/CLAUDE.md scaffolds. Outputs: a v1 Codebase Model with all six views populated at a pinned git commit + ingestion-pass ID. Cost ceiling per [ADR 0011 P-02 cost ceilings](../../../docs/adr/0011-p-02-cost-ceilings.md): ingestion has a higher one-time ceiling than per-cycle work — "the ceiling itself is per-phase, not flat" per [BF-L §4 D-5 acceptance with justification](../tracks/brownfield-legacy-ingestion-first.md#4-defaults-accepted-vs-challenged-all-7-marked).

Construction-per-view follows [ADR 0047 Layer 1-3](../../../docs/adr/0047-p-26-codebase-model.md): Tree-sitter + SCIP for structural; LLM-with-structured-output (gated on Wave-4.5b sub-track outcomes) for conventional; git-blame + P-24 composition for historical; P-07 telemetry tag-join for runtime; CodeQL + Daikon-tier-deferred for invariant; debt-marker grep + P-22 reference resolution for debt. Ingestion runs to completion before Loop-2 dispatches its first cycle.

### 3.2 Loop 2: Work (per-cycle, methodology-shaped, queries the model)

Per-cycle methodology that queries the Codebase Model. Each cycle:

1. **Work-unit declaration.** Per [BF-L track §1](../tracks/brownfield-legacy-ingestion-first.md), the **work-unit-class taxonomy is derived from the Codebase Model**, not pre-decided. A codebase with a heavy issue tracker and stable architecture surfaces *issue-from-queue* work units (Atelier-style); a codebase with active spec-driven refactoring surfaces *change-request-against-spec* (Refinery-style); a codebase whose model shows accumulating debt and no issue queue surfaces *codebase-evolution proposals*. This is BF-L's most direct architectural answer to OQ-B4.
2. **Region resolution.** The work unit's touched-region set is computed by traversing the structural view + dependency-impact graph (P-22 + P-23) for the named symbols. The Codebase Model snapshot version is pinned at dispatch.
3. **Per-region regime classification.** [P-19 dispatcher (ADR 0049)](../../../docs/adr/0049-p-19-variant-bf-l-per-region.md) reads the feature vector per touched region from P-26 and emits per-region regime labels through the [P-19 framework (ADR 0028)](../../../docs/adr/0028-p-19-eligibility-regime-classifier.md) decision-table engine. Cycle-level rollup: **strictest classification wins**.
4. **Cycle execution.** Per the dispatched regime:
   - **Automation-eligible regions only**: substrate-enforced gates — acceptance criteria from P-08 model-derived scenarios; holdout discipline; bias guard.
   - **Augmentation-required**: K=5 ≥70% bar; cross-family judge required via [P-14 (ADR 0016)](../../../docs/adr/0016-p-14-judge-router.md); paraphrase ≥3/5 (F46 mitigation).
   - **Human-required (any region with Caremark/RSI tag, or below coverage+telemetry floor)**: named-human L4 review; cooling-off windows; AILCCP logging.
5. **Scenario gate.** Cycles must pass model-derived scenarios from P-27-built brief + P-08 held-out partition. Substrate-enforced; methodology cannot opt out.
6. **Trajectory write.** [P-05 (ADR 0012)](../../../docs/adr/0012-p-05-trajectory-capture.md) appends the cycle event with the per-region regime distribution in the payload. Patrol-tier ([ADR 0013](../../../docs/adr/0013-p-06-watchdog-tiers.md)) monitors model drift against codebase reality.
7. **Attribution.** Each cycle's diff is signed and recorded via [P-24 (ADR 0035)](../../../docs/adr/0035-p-24-attribution-store.md) at per-symbol granularity — the cosigned envelope `(agent_id, model_snapshot, cycle_id, symbol_id, diff_slice)` feeds the historical view on next reconciliation.

### 3.3 Loop 3: Maintenance (continuous, low-cadence)

Per [ADR 0048 (P-13 maintenance loop)](../../../docs/adr/0048-p-13-maintenance-loop.md): cron-driven inspector that polls the Codebase Model for drift signals, prioritises by debt-weighted composite, and dispatches per-region reconciliation cycles via P-30 events. Maintenance cycles are typed as `kind=maintenance-trigger`; reconciliation handlers re-ingest deltas, refresh affected P-26 views, and emit P-24 attribution. The maintenance loop is the structural defence against F34 (cross-layer drift), F55 (behavioural drift), F57 (design-authority erosion) — and the answer to **"what changes when the codebase changes underneath us."**

### 3.4 Sub-track choice — both smoke-tests passed

BF-L's [auto-003 Round 2](../decisions/auto-003-bfl-rg-view-choice.md#decision-round-2) decision was **option A′ — smoke-test-first per view**. Two smoke-tests authored at Wave 4.5:

- **Conventional-view smoke-test** ([bfl-conventional-smoke-test.md](../sub-tracks/bfl-conventional-smoke-test.md)) — passed 3/3 languages (Python Django 5.0, TypeScript VS Code 1.95.0, Java Spring 6.1.0) with 9 non-trivial conventions extracted. **Wave-4.5b full sub-track authorised** — scale 3-per-language to ≥10-per-language.
- **Invariant-view smoke-test** ([bfl-invariant-smoke-test.md](../sub-tracks/bfl-invariant-smoke-test.md)) — passed 3/3 languages (Django 4.2.11, TanStack Query v5.28.0, Spring 6.1.5) with 12 non-trivial invariants. Tier distribution T1+T2+T3 preferred; **T4 Daikon-style runtime explicitly deferred** per research-notes recommendation. Wave-4.5b sub-track authorised.

Both smoke-tests passing means the **methodology-degradation clause did NOT activate** at smoke-test close — but [§2.1's structural clause statement](#21-the-codebase-model-load-bearing-orphan) remains, because Wave-4.5b scaling is owed at Phase 5/6 and full sub-track failure at the ≥10-per-language gate would activate the clause then. The clause is a deferred-defence, not a current-state degradation.

### 3.5 Distinctive methodology decisions

Three:

- **Scenarios are inherited from the model, not authored out-of-tree** — explicit challenge to D-2 per [BF-L §4](../tracks/brownfield-legacy-ingestion-first.md#4-defaults-accepted-vs-challenged-all-7-marked).
- **Work-unit-class is derived from the model, not pre-decided** — the model's profile picks Atelier-issue vs Refinery-change-request vs codebase-evolution-proposal per OQ-B4.
- **Regime classification is per-region, not per-cycle** — different regions of the same codebase carry different stakes; the strictest-region-wins cycle rollup is deterministic substrate logic.

## §4 Discipline binding

BF-L binds 9 of the 10 discipline ADRs (0018-0027). The three-loop discipline (0026) is load-bearing for the architecture's shape; the maintenance loop's per-codebase cadence is BF-L's per-codebase declaration of [ADR 0026's binding requirement](../../../docs/adr/0026-discipline-three-loop.md#decision).

- **Bias guard ([ADR 0018](../../../docs/adr/0018-discipline-bias-guard.md)).** Bound at the per-region dispatcher: augmentation-required regions enforce cross-family judging via P-14 (F46 mitigation). Caremark-tagged regions go straight to human-required; bias guard is supplementary, not the floor.

- **Cognitive escrow ([ADR 0019](../../../docs/adr/0019-discipline-cognitive-escrow.md)).** Bound at the [P-05 (ADR 0012)](../../../docs/adr/0012-p-05-trajectory-capture.md) trajectory + Patrol-tier ([ADR 0013](../../../docs/adr/0013-p-06-watchdog-tiers.md)). The prompt→response interval is substrate-enforced. BF-L specialization (per [BF-L §4 D-7](../tracks/brownfield-legacy-ingestion-first.md#4-defaults-accepted-vs-challenged-all-7-marked)): ingestion trajectories *become* part of the Codebase Model — Loop-3 reconciliation can re-read how a region was indexed and detect ingestion-pass drift.

- **Cost ceiling ([ADR 0020](../../../docs/adr/0020-discipline-cost-ceiling.md)).** Bound at [P-02 (ADR 0011)](../../../docs/adr/0011-p-02-cost-ceilings.md) with per-loop parameterisation (ingestion ceiling > per-cycle ceiling > maintenance ceiling). CTR-E1 cost variance is addressed by per-loop ceilings.

- **Holdout ([ADR 0021](../../../docs/adr/0021-discipline-holdout.md)).** Bound at [P-08 scenario storage (ADR 0015)](../../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md) — substrate marks subsets of the Codebase Model held-out; ingestion-aware judges enforce the partition. D-4 acceptance with BF-L specialization.

- **Honesty ([ADR 0022](../../../docs/adr/0022-discipline-honesty.md)).** Bound but with the **methodology-degradation clause** carve-out for the RG-flagged views: when conventional / invariant view falls back to (b), the per-region classifier emits `degraded-convention` / `degraded-invariant` regime variants the Patrol drift-monitor must distinguish from regular F57 drift. The clause itself is an honesty mechanism: rather than papering over the RG fallback, the substrate logs it.

- **Knowledge promotion ([ADR 0023](../../../docs/adr/0023-discipline-knowledge-promotion.md)).** Bound at the maintenance loop: drift signals that *correlate with cycle outcomes* are candidate for promotion into the per-region classifier's feature schema. Pattern→standard promotion runs over the model's historical view.

- **Regime classification ([ADR 0024](../../../docs/adr/0024-discipline-regime-classification.md)).** Bound at [P-19 (ADR 0049)](../../../docs/adr/0049-p-19-variant-bf-l-per-region.md) per the framework decision. BF-L names the per-variant declaration of feature source (P-26 features) + regime set (per-region with strictest-wins rollup) + hard-floor table (Caremark/RSI + debt-cluster + coverage-floor) per the discipline contract.

- **Scoping ([ADR 0025](../../../docs/adr/0025-discipline-scoping.md)).** Bound at the per-region dispatcher: work-unit scope is bounded by the touched-region set computed from P-22 + P-23. Regions outside the touched set are out-of-scope by construction.

- **Three-loop ([ADR 0026](../../../docs/adr/0026-discipline-three-loop.md)).** **Load-bearing for BF-L.** All three loops — ingestion, work, maintenance — have substrate touchpoints, escalation policy, and evidence-retention horizons declared per ADR 0026's binding requirement. The maintenance loop (P-13, ADR 0048) is BF-L's per-codebase cadence declaration; without it, ADR 0026 would not be satisfied.

- **Trifecta closure ([ADR 0027](../../../docs/adr/0027-discipline-trifecta-closure.md)).** Bound at the [P-08 (ADR 0015)](../../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md) holdout + the regime classifier's hard-floor table — both substrate-enforced. Cycles cannot close trifecta without holdout pass + classifier sign-off.

**Disciplines BF-L is NOT silent on but does not own.** None — BF-L carries all 10 disciplines. The carve-out on honesty (methodology-degradation clause) is a substrate-enforced honesty mechanism, not a rejection.

**Disciplines BF-L is explicitly silent on.** D-1 (specs as the durable artifact) is challenged per [BF-L §4](../tracks/brownfield-legacy-ingestion-first.md#4-defaults-accepted-vs-challenged-all-7-marked) — the durable artifact is the Codebase Model. D-2 (scenarios out-of-tree) is challenged — scenarios are inherited from the model. D-3 (Agent = Model + Harness) is partially challenged — the Codebase Model is a substrate primitive that does not decompose into either.

## §5 Mandate fit

BF-L is **brownfield-only**. Per [DEC-1.b](../candidate-registry.md), the greenfield/brownfield distinction is entry-mode (not temporal); BF-L is structurally tied to *existing code*. The mandate-fit YAML block per work-unit-class:

- **initial-spec: brownfield.** Ingestion produces an initial Codebase Model; the architecture treats the inferred model as the initial spec. The work-unit-class for initial-spec authoring on brownfield is "construct the Codebase Model" (Loop-1). Greenfield initial-spec is N/A — there's no existing code to ingest. **Falsifying scenario:** if a brownfield codebase's Codebase Model construction fails (the integration discipline at 1M+LOC / 10+ year history blows the 9-18 engineer-month estimate per [Phase-3.5.5 status](../candidate-registry.md#headline-outcomes-all-10-candidates)), BF-L's initial-spec claim collapses.

- **refactor: brownfield.** Refactor cycles operate against the Codebase Model — touched regions resolve via P-22 + P-23, regime classification is per-region, scenarios derive from the model. Caremark-tagged regions refactored only under human-required regime. **Supporting evidence:** [ADR 0047 P-26](../../../docs/adr/0047-p-26-codebase-model.md), [ADR 0049 BF-L per-region](../../../docs/adr/0049-p-19-variant-bf-l-per-region.md). **Falsifying scenario:** if refactor work units routinely classify to human-required across the full region set (no automation-eligible regions ever materialise), BF-L's per-region thesis is wrong — the model is not surfacing sufficient signal to differentiate regions.

- **mvp: n/a.** MVP authoring presupposes greenfield-leaning evolution (no existing code, no model to ingest). BF-L's three loops are structurally tied to an existing codebase; running Loop-1 on an empty repository produces an empty model and Loop-2's per-region regime classifier has no features. **Rationale:** BF-L is brownfield-only by construction per [BF-L track §6](../tracks/brownfield-legacy-ingestion-first.md#6-what-this-track-is-not-trying-to-be).

- **post-mvp-evolution: brownfield.** Post-MVP cycles operate against a Codebase Model that thickens as Loop-2 cycles deposit attribution (P-24) into the historical view and Loop-3 maintenance keeps the model current. The work-unit-class diversifies as the model's profile evolves. **Supporting evidence:** [ADR 0048 P-13 maintenance loop](../../../docs/adr/0048-p-13-maintenance-loop.md) — the model's currency *is* the post-MVP evolution mechanism. **Falsifying scenario:** if Loop-3 cadence cannot keep up with Loop-2's modification rate (the model drifts faster than the maintenance loop reconciles), BF-L's post-MVP-evolution claim collapses to F34 cross-layer drift.

- **regression-fix: brownfield.** Regression fixes are by construction *near-anchor* in the BF-L vocabulary — the failing test IS the anchor, and the fix touches a region the runtime view + structural view co-locate. High-coverage regions classify automation-eligible; low-coverage regions classify augmentation-required at minimum. **Supporting evidence:** the runtime view's telemetry density + P-08 held-out partition. **Falsifying scenario:** if regression-fix cycles routinely route to human-required (i.e., the regression-fixing region is *always* low-coverage), the model's runtime view is structurally inadequate.

**DEC-1.a falsifier-discipline observation.** BF-L claims `brownfield` on 4 of 5 work-unit-classes and `n/a` on the fifth (mvp). No `both` claims. Per [DEC-1.a](../decisions-captured.md#d1--unification-verdict-no-methodology-serves-both-mandates-working-hypothesis-falsifiable-by-phase-8), this is *consistent* with the no-methodology-serves-both-mandates working hypothesis — BF-L is mandate-specific by design. Phase-8 lean-eval will not pressure-test BF-L's `both` claims (there are none) but will pressure-test the `brownfield` claims against scaling, drift, and the methodology-degradation clause.

## §6 Open carries

Surfaced into Phase 7 (back-fill audit) / Phase 8 (lean-eval) / future ADRs:

- **P-26 integration discipline at 1M+LOC / 10+ year history (Phase-8 lean-eval candidate; soft RG on scale).** Per [ADR 0047 § Consequences](../../../docs/adr/0047-p-26-codebase-model.md), "six-view composition at 1M+LOC with 10+ years of history is unmeasured (soft RG on scale per P-26 sketch §RG-flag); Glean and SCIP publish scale numbers for structural alone." Phase-8 pressure-test: run the integration discipline against a public 1M+LOC long-history codebase (e.g., Chromium, Linux kernel) and measure join-API latency, snapshot-consistency under concurrent ingestion, and Merkle-DAG delta-version drift. **Status: Phase-8 carry.**

- **P-26 conventional-view RG carry (Phase-8 lean-eval candidate; Wave-4.5b verdict gates).** Wave-4.5 smoke-test passed 3/3 languages with 9 conventions, but Wave-4.5b is owed at Phase 5/6 to scale to ≥10-per-language (per [substrate-requirements §5](../substrate-requirements/bf-l.md#5-open-carries)). Phase-8 lean-eval: precision-against-labelled-corpus measurement across all 30+ conventions. Per the [conventional smoke-test §honest-gaps](../sub-tracks/bfl-conventional-smoke-test.md#honest-gaps-named): test-pattern conventions are the weakest sub-surface; idiom-register conventions are thinly covered at smoke-test scale. **Status: Phase-8 carry; methodology-degradation clause activates at Phase-4-close if Wave-4.5b fails.**

- **P-26 invariant-view RG carry (Phase-8 lean-eval candidate; Wave-4.5b verdict gates).** Wave-4.5 smoke-test passed 3/3 languages with 12 invariants across tiers T1+T2+T3. **T4 Daikon-style runtime inference explicitly deferred** per research-notes recommendation. Phase-8 pressure-test: scale the recipe to ≥10-per-language including cross-view-join invariants (per the [invariant smoke-test §4.3 gap (4)](../sub-tracks/bfl-invariant-smoke-test.md#43-honest-gaps-named)). The integration discipline is genuinely BF-L-specific and the smoke-test punted on it. **Status: Phase-8 carry; methodology-degradation clause activates at Phase-4-close if Wave-4.5b fails.**

- **Maintenance-loop cadence calibration (Phase-8 lean-eval candidate; own OQ-T3).** Per [ADR 0048 § Consequences](../../../docs/adr/0048-p-13-maintenance-loop.md) and [BF-L track §7 OQ-3](../tracks/brownfield-legacy-ingestion-first.md): cadence values are deployment-tunable but have no empirical anchor. Drift-signal thresholds (coverage delta, telemetry anomaly, churn σ) need empirical calibration against real codebases. **Status: Phase-8 carry.**

- **Per-region regime classifier drift under degradation regime (Phase-8 lean-eval candidate).** Per [ADR 0049 § Consequences](../../../docs/adr/0049-p-19-variant-bf-l-per-region.md) and [BF-L track §7 OQ-T4](../tracks/brownfield-legacy-ingestion-first.md): does per-region classification fragment governance (F43 board-visibility gap)? Methodology-degradation logging adds `degraded-convention` / `degraded-invariant` regime variants; the Patrol drift-monitor must distinguish them from regular F57 drift. **Status: Phase-8 carry.**

- **F54 Codebase-Model attack-surface pressure-test (Phase-8 lean-eval candidate).** Per [BF-L track §7 OQ-T6](../tracks/brownfield-legacy-ingestion-first.md): an adversary who can poison the Codebase Model can drift the factory's objectives across cycles without tripping any single guard. Kahana's framing applies; the architecture gestures at a model-integrity primitive but does not specify it. **Status: Phase-8 carry.**

- **Ingestion-as-substrate vs ingestion-as-methodology (Phase-7 back-fill carry; own OQ-T1).** Per [BF-L track §7 OQ-1](../tracks/brownfield-legacy-ingestion-first.md): BF-L places ingestion at the substrate layer; if Phase-7 back-fill or Phase-8 lean-eval finds a candidate where ingestion-as-methodology is sufficient, BF-L's load-bearing claim weakens. **Status: Phase-7 carry.**

- **F35 federation-at-the-model-level (Phase-8 lean-eval candidate; own OQ-T7).** If multiple brownfield factories share a Codebase Model schema family, F35 (federation-as-family drift) applies to the model schemas themselves. Open: is model-schema variability governance a separate ADR? **Status: Phase-8 carry.**

## §7 References

**ADR set (this spec's binding inputs).** Per the §0 ADR-citation index above; relative paths under `../../../docs/adr/`:

- **Common substrate:** [ADR 0010 P-01 sandbox](../../../docs/adr/0010-p-01-sandbox-runtime.md), [ADR 0011 P-02 cost ceilings](../../../docs/adr/0011-p-02-cost-ceilings.md), [ADR 0012 P-05 trajectory capture](../../../docs/adr/0012-p-05-trajectory-capture.md), [ADR 0013 P-06 watchdog tiers](../../../docs/adr/0013-p-06-watchdog-tiers.md), [ADR 0014 P-07 telemetry ingestor](../../../docs/adr/0014-p-07-telemetry-ingestor.md), [ADR 0015 P-08 scenario storage](../../../docs/adr/0015-p-08-scenario-storage-with-runner-contract.md), [ADR 0016 P-14 judge router](../../../docs/adr/0016-p-14-judge-router.md), [ADR 0017 P-22 polyglot codebase index](../../../docs/adr/0017-p-22-polyglot-codebase-index.md).
- **Designed-system / framework substrate:** [ADR 0028 P-19 framework](../../../docs/adr/0028-p-19-eligibility-regime-classifier.md), [ADR 0031 P-23 dependency-impact graph](../../../docs/adr/0031-p-23-dependency-impact-graph.md), [ADR 0036 P-30 event registrar](../../../docs/adr/0036-p-30-event-registrar-substrate.md).
- **2-candidate-fold substrate:** [ADR 0034 P-27 archaeological-brief tooling](../../../docs/adr/0034-p-27-archaeological-brief-tooling.md), [ADR 0035 P-24 attribution store](../../../docs/adr/0035-p-24-attribution-store.md).
- **Per-variant substrate (BF-L-specific):** [ADR 0049 BF-L P-19 per-region](../../../docs/adr/0049-p-19-variant-bf-l-per-region.md).
- **Orphan substrate (BF-L-specific):** [ADR 0047 P-26 Codebase Model](../../../docs/adr/0047-p-26-codebase-model.md), [ADR 0048 P-13 maintenance loop](../../../docs/adr/0048-p-13-maintenance-loop.md).
- **Discipline:** [ADR 0018](../../../docs/adr/0018-discipline-bias-guard.md), [ADR 0019](../../../docs/adr/0019-discipline-cognitive-escrow.md), [ADR 0020](../../../docs/adr/0020-discipline-cost-ceiling.md), [ADR 0021](../../../docs/adr/0021-discipline-holdout.md), [ADR 0022](../../../docs/adr/0022-discipline-honesty.md), [ADR 0023](../../../docs/adr/0023-discipline-knowledge-promotion.md), [ADR 0024](../../../docs/adr/0024-discipline-regime-classification.md), [ADR 0025](../../../docs/adr/0025-discipline-scoping.md), [ADR 0026](../../../docs/adr/0026-discipline-three-loop.md), [ADR 0027](../../../docs/adr/0027-discipline-trifecta-closure.md).

**Supporting docs:**

- [BF-L candidate-registry entry](../candidate-registry.md#bf-l--brownfield-legacy-ingestion-first-1)
- [BF-L substrate-requirements summary](../substrate-requirements/bf-l.md)
- [BF-L track sketch (brownfield-legacy-ingestion-first)](../tracks/brownfield-legacy-ingestion-first.md)
- [BF-L conventional-view smoke-test (Wave 4.5, passed 3/3)](../sub-tracks/bfl-conventional-smoke-test.md)
- [BF-L invariant-view smoke-test (Wave 4.5, passed 3/3)](../sub-tracks/bfl-invariant-smoke-test.md)
- [BF-L conventional-view prior-art research notes (Wave 4.4)](../research-notes/bfl-conventional-view-prior-art.md)
- [BF-L invariant-view prior-art research notes (Wave 4.4)](../research-notes/bfl-invariant-view-prior-art.md)
- [P-26 buildability sketch](../primitives/P-26-codebase-model.md)
- [Phase-4.2 overlap.md P-19 four-variant verdict — BF-L per-region row](../primitives/overlap.md#p-19-eligibility--regime-classifier--four-contested-variants)
- [Phase-4.2 overlap.md orphan list — P-26, P-13 BF-L orphans](../primitives/overlap.md#coverage-tier-summary-phase-5-adr-priority-signal)
- [auto-003 Round 2 — BF-L RG-view choice (option A′ smoke-test-first)](../decisions/auto-003-bfl-rg-view-choice.md#decision-round-2)
- [auto-006 Phase-6 dispatch-shape brief — this spec is authored under its Round-2 rubric (BF-L heavy tier 3500-5500 words)](../decisions/auto-006-phase-6-dispatch-shape.md#decision-round-2)
- [Phase-5-close session handoff — BF-L ADR set row](../SESSION-HANDOFF-2026-05-25-phase-5-close.md#candidate-set-state-at-phase-5-close)
- [DEC-1.a unification-verdict working hypothesis (BF-L is consistent — brownfield-only)](../decisions-captured.md#d1--unification-verdict-no-methodology-serves-both-mandates-working-hypothesis-falsifiable-by-phase-8)
- [DEC-2 mandate-fit-per-(architecture × work-unit-class)](../decisions-captured.md#d2--mandate-fit-is-per-architecture--work-unit-class-not-per-architecture)
- [Phase-3.5.5 RG-primitive rule (binding, user-approved)](../candidate-registry.md#phase-355-rule-on-load-bearing-rg-primitives-binding-user-approved-2026-05-25)
