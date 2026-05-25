# Phase 3.5 substrate-primitive index — de-duplicated union across all 10 candidates

This file is the canonical primitive enumeration for [Phase 3.5](../../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md#phase-35--substrate-primitive-buildability-sketches-new-in-v12). It is the input to the dispatch shape determined in [`decisions/auto-001-phase-3.5-dispatch-shape.md`](../decisions/auto-001-phase-3.5-dispatch-shape.md) (hybrid, option C).

**Scope discipline.** Per the [scoping principle](../phase-3.4-decisions-resolved.md#scoping-principle-immutable-overrides-any-conflicting-framing-in-the-integration-brief) and Round-2 adversarial review of the dispatch brief: each primitive is enumerated once with all claiming candidates listed. **Same-vs-distinct verdicts on primitives that look similar across candidates (e.g., U-A typed-object store vs. U-B layer-typed store vs. D7-U-1 FC store) are NOT rendered here.** Those judgments belong at Phase 4.2 / methodology-matching. The de-duplication this file performs is only for primitives whose contract, role, and construction recipe are uncontroversially the same across candidates (commodity primitives like sandbox, watchdog, cost-ceiling).

**Cognitive escrow exclusion.** Per [DEC-2](../phase-3.4-decisions-resolved.md#dec-2--cognitive-escrow-placement-methodology), the cognitive-escrow surface is methodology-layer, not substrate. Primitives originally named in GF-M and GF-C as escrow-related are excluded from this index.

## Summary

- **Total primitive IDs enumerated:** 34 (P-01 through P-34). Two IDs may collapse at sketch time (P-12 deterministic-linter-framework vs P-16 EARS+GtWR linter rule library; P-08 scenario storage vs P-09 held-out runner) — left as distinct IDs pre-sketch and resolved by the sketches themselves.
- **Dispatch tier `cluster` (commodity):** 13 primitives across 3 clusters (P-01 through P-13).
- **Dispatch tier `per-primitive` (designed-system / research-grade):** 21 primitives (P-14 through P-34).
- **Anticipated subagent count:** 3 cluster subagents + 21 per-primitive subagents = **24 total**.
- **Research-grade-uncertainty flags expected:** P-26 (Codebase Model), P-31 (cross-layer drift detector), P-34 (independence auditor); possibly P-32 (distance estimator calibration). Confirmed at sketch time.

Cost-hawk's sequencing fix (per [auto-001 Round 2](../decisions/auto-001-phase-3.5-dispatch-shape.md#sequencing-change)) was: enumerate first, then re-pick the shape. Result: 34 enumerated primitives, ~22 distinct after collapse, hybrid (option C) remains the right shape — count is above cost-hawk's "≤15 → switch to per-primitive" threshold, below the "≥23 → keep option B per-cluster" threshold. Hybrid stands.

## Per-primitive enumeration

### Commodity primitives (dispatch-tier: `cluster`)

#### Cluster C1 — Execution & resource control

| ID | Name | Contract (one-line) | Claimed by | Registry buildability scope |
|---|---|---|---|---|
| P-01 | Sandbox runtime (deny-by-default) | Isolated execution env; deny-all default; allow-list for tool/net/fs | [GF-S/S1](../tracks/greenfield-substrate-first.md), [BF-M](../tracks/brownfield-methodology-first.md), implicit in all | commodity |
| P-02 | Cost ceilings (hard, multi-axis) | Per-cycle / per-cycle-class hard caps on tokens, calls, $; enforced by mediator | [GF-S/S4](../tracks/greenfield-substrate-first.md), [GF-M](../tracks/greenfield-methodology-first.md), [BF-M (D-5)](../tracks/brownfield-methodology-first.md) | commodity |
| P-03 | Worktree isolation | Per-cycle worktree; F17 contamination mitigation | [BF-M (F17)](../tracks/brownfield-methodology-first.md) | commodity |
| P-04 | PR creator | Authenticated branch-push + PR-open with structured metadata | [BF-M](../tracks/brownfield-methodology-first.md) | commodity |

#### Cluster C2 — Observation & control

| ID | Name | Contract (one-line) | Claimed by | Registry buildability scope |
|---|---|---|---|---|
| P-05 | Trajectory capture | Per-event append-only persistence of agent step/tool-use trace | [GF-S/S3](../tracks/greenfield-substrate-first.md), [BF-M (D-7)](../tracks/brownfield-methodology-first.md), [U-C distance-keyed variant](../tracks/unified-C.md) | commodity |
| P-06 | Watchdog tiers (Daemon / Triage / Patrol) | 3-tier escalation: Daemon (per-event) → Triage (per-cycle anomaly) → Patrol (cross-cycle distribution) | [GF-S/S5](../tracks/greenfield-substrate-first.md), [GF-M](../tracks/greenfield-methodology-first.md), [BF-M (D-6)](../tracks/brownfield-methodology-first.md) | commodity |
| P-07 | Telemetry ingestor (per-role read filters) | Production telemetry pull/subscribe with attribute-based access control | [BF-S/S-3](../tracks/brownfield-substrate-first.md), [BF-M runtime-telemetry-read](../tracks/brownfield-methodology-first.md), [BF-L Codebase Model runtime view component](../tracks/brownfield-legacy-ingestion-first.md) | commodity (per-role filter is the non-trivial part — see notes) |

#### Cluster C3 — Scenario storage & holdout

| ID | Name | Contract (one-line) | Claimed by | Registry buildability scope |
|---|---|---|---|---|
| P-08 | Scenario storage (out-of-tree, holdout-partitioned) | Append-only scenario store with substrate-enforced training/holdout partition | [GF-S/S2](../tracks/greenfield-substrate-first.md), [GF-M holdout enforcement](../tracks/greenfield-methodology-first.md), [BF-L held-out partition enforcement](../tracks/brownfield-legacy-ingestion-first.md), [BF-M held-out scenario runner](../tracks/brownfield-methodology-first.md) | commodity (key partition discipline is the design content) |
| P-09 | Held-out scenario runner | Deterministic replay of stored scenarios against current agent; pass/fail verdict | [GF-S/S2 component](../tracks/greenfield-substrate-first.md), [GF-M](../tracks/greenfield-methodology-first.md), [BF-M](../tracks/brownfield-methodology-first.md), [BF-L](../tracks/brownfield-legacy-ingestion-first.md) | commodity |
| P-10 | Coordination medium (CI-friendly, content-addressed) | Shared blob/object medium accessible by CI + agents with content-hash addressing | [GF-S/S7](../tracks/greenfield-substrate-first.md) | commodity |
| P-11 | Cold-Start Bench (HMAC-signed scenario store) | Crypto-signed seed scenario bench, immutable after day-0 sign | [GF-C](../tracks/greenfield-cold-start-first.md) | commodity (HMAC + scenario storage) |
| P-12 | Deterministic linter framework | Rule-engine for deterministic per-cycle checks (separate primitive from the rule set itself) | [BF-M (F38)](../tracks/brownfield-methodology-first.md), [GF-S/S8 component](../tracks/greenfield-substrate-first.md) | commodity |
| P-13 | Maintenance loop (continuous reconciliation) | Low-cadence continuous job that compares model with reality and flags drift | [BF-L](../tracks/brownfield-legacy-ingestion-first.md) | commodity (cron + diff infrastructure) |

### Designed-system / research-grade primitives (dispatch-tier: `per-primitive`)

| ID | Name | Contract (one-line) | Claimed by | Registry buildability scope |
|---|---|---|---|---|
| P-14 | Judge router (multi-shape typed) | Provider-family-diverse model dispatch with typed input/output shapes per judge role | [GF-S/S6](../tracks/greenfield-substrate-first.md), [BF-M cross-family routing (F46)](../tracks/brownfield-methodology-first.md), [U-A judge router](../tracks/unified-A.md), [U-B per-layer judge routing](../tracks/unified-B.md) | designed-system (registry: Medium) |
| P-15 | Four-guard mediator | Composition of 4 deterministic guards: GtWR lint + contradiction-detector + req-count budgeter + perimeter typing — gated single mediator surface | [GF-S/S8](../tracks/greenfield-substrate-first.md) | designed-system (contradiction-detector needs multi-model judge ensemble) |
| P-16 | EARS+GtWR linter | Deterministic rule engine for INCOSE R7–R35 + EARS pattern conformance | [GF-C](../tracks/greenfield-cold-start-first.md), [GF-S/S8 component](../tracks/greenfield-substrate-first.md) | designed-system (specific rule library) |
| P-17 | Intent Crucible validator | 9-field typed-object intake with deterministic structural validators | [GF-C](../tracks/greenfield-cold-start-first.md) | designed-system |
| P-18 | RSI-Declaration Ledger | Append-only declaration ledger tracking RSI commitments + invariants | [GF-C](../tracks/greenfield-cold-start-first.md) | designed-system |
| P-19 | Eligibility / regime classifier | Per-(work-unit-class × region) classifier deciding which regime/cycle applies | [GF-S/S9](../tracks/greenfield-substrate-first.md), [BF-L per-region regime classifier](../tracks/brownfield-legacy-ingestion-first.md), [U-C distance-gated dispatcher (related)](../tracks/unified-C.md) | designed-system (classifier may itself be LLM judge — open) |
| P-20 | Reversibility primitive (event-sourced) | Cheap commit-and-reverse on intent / scenario / artifact objects via event-sourced storage | [GF-M](../tracks/greenfield-methodology-first.md) | designed-system (event-sourcing pattern is well-understood; integration with intent artifacts is the design content) |
| P-21 | Paraphrase divergence primitive | N model-family-diverse paraphrasers callable in parallel with deterministic prompt-paraphrase generators | [GF-M](../tracks/greenfield-methodology-first.md) | designed-system |
| P-22 | Polyglot codebase index | Per-language incremental queryable index of symbols/AST/types | [BF-S/S-1](../tracks/brownfield-substrate-first.md), [BF-M code-traversal](../tracks/brownfield-methodology-first.md), component-of [BF-L Codebase Model](../tracks/brownfield-legacy-ingestion-first.md) | designed-system (registry: High) |
| P-23 | Dependency-and-impact graph | Per-symbol blast-radius compute; cross-language reference graph | [BF-S/S-2](../tracks/brownfield-substrate-first.md), component-of [BF-L Codebase Model](../tracks/brownfield-legacy-ingestion-first.md), used by [U-C distance estimator](../tracks/unified-C.md) | designed-system (registry: High) |
| P-24 | Change-history / attribution store (append-only, signed) | Per-symbol attribution at fine granularity with signed append-only history | [BF-S/S-4](../tracks/brownfield-substrate-first.md), component-of [BF-L Codebase Model historical view](../tracks/brownfield-legacy-ingestion-first.md) | designed-system (git plumbing + symbol-level granularity is the design content) |
| P-25 | CaMeL-class typed perimeter | Capability-typed boundary mediating production-adjacent reads/writes | [BF-S/S-5](../tracks/brownfield-substrate-first.md), [BF-M](../tracks/brownfield-methodology-first.md) | designed-system (registry: prior art is CaMeL paper + AgentDojo) |
| P-26 | Codebase Model (6 views, integrated) | Durable versioned queryable artifact integrating structural / conventional / historical / runtime / invariant / debt views | [BF-L](../tracks/brownfield-legacy-ingestion-first.md) | **research-grade-uncertainty** (registry: Highest; "the most ambitious primitive in the catalog") |
| P-27 | Archaeological-brief generation tooling | LLM-driven codebase summarization with structured outputs feeding Phase-comprehension stage | [BF-M](../tracks/brownfield-methodology-first.md) | designed-system (uses Codebase Model + LLM-with-structured-output) |
| P-28 | Typed-object store (content-addressed, append-only) | Append-only blob store with typed envelope + content-hash addressing | [U-A typed-object store](../tracks/unified-A.md), [U-B layer-typed object store (per-layer variant)](../tracks/unified-B.md), [D7-U-1 FC store (FC-typed variant)](../bias-guards/phase-3/d7-blind-axis/d7-u-1-prohibit-interval-escrow.md), [U-C anchor object store (anchor-typed variant)](../tracks/unified-C.md), related-to [P-10 coordination medium](#cluster-c3--scenario-storage--holdout) | designed-system (variants are pre-identified contested — same-vs-distinct deferred to Phase 4.2 per scoping principle) |
| P-29 | Policy mediator (declarative gates) | OPA / Cedar-style declarative policy enforcement at primitive boundaries | [U-A policy mediator](../tracks/unified-A.md), [D7-U-1 compounding gate (variant)](../bias-guards/phase-3/d7-blind-axis/d7-u-1-prohibit-interval-escrow.md) | designed-system (prior art: OPA, Cedar) |
| P-30 | Re-entry / event registrar | Substrate-typed event protocol registering re-entry events into the cycle graph | [U-A re-entry registrar](../tracks/unified-A.md), [D7-U-1 survival-window registrar (variant)](../bias-guards/phase-3/d7-blind-axis/d7-u-1-prohibit-interval-escrow.md) | designed-system |
| P-31 | Cross-layer drift detector | Per-layer-pair invariant checker; flags inter-layer drift on pace-layer artifact stack | [U-B](../tracks/unified-B.md) | **research-grade-uncertainty** (registry: "Brier's pace-layer framework is a description, not a tool — needs substrate-side detector implementation") |
| P-32 | Distance estimator (multi-component, typed) | Compute graph-distance + pace-layer-crossings + intent-field-touch count to a frozen anchor | [U-C](../tracks/unified-C.md) (depends on P-22, P-23) | designed-system, near-research-grade (composition of well-understood components; calibration may be research-grade) |
| P-33 | Opposing-side router | Provider-property-driven routing for adversarial / falsification dispatch; model-family taxonomy + capability registry | [D7-U-1](../bias-guards/phase-3/d7-blind-axis/d7-u-1-prohibit-interval-escrow.md) | designed-system |
| P-34 | Independence auditor | Patrol-tier deterministic anomaly detection on FC log distributions for collusion/correlation | [D7-U-1](../bias-guards/phase-3/d7-blind-axis/d7-u-1-prohibit-interval-escrow.md) | **research-grade-uncertainty** (auditor recursion is the candidate's own load-bearing OQ) |

### Notes on numbering

The numbered IDs run P-01 through P-34 (13 cluster + 21 per-primitive). Two pairs may collapse at sketch time:

- **P-12 (deterministic linter framework) vs P-16 (EARS+GtWR linter rule library)** — P-12 is the rule-engine substrate; P-16 is a specific rule set running on that engine. If a sketch determines they are not separable in practice, P-16 absorbs into P-12.
- **P-08 (scenario storage) vs P-09 (held-out runner)** — P-08 is the partitioned store; P-09 is the deterministic replay loop. If the registry's "held-out scenario runner" is just the store with a read-API, P-09 absorbs into P-08.

These determinations happen at sketch time, not pre-judged here. Best-estimate distinct count after collapse: 32.

## Per-tier subagent dispatch plan

### Cluster subagents (3 total)

- **C1 subagent** — sketches P-01 through P-04 (sandbox + cost ceiling + worktree + PR creator).
- **C2 subagent** — sketches P-05 through P-07 (trajectory capture + watchdog tiers + telemetry ingestor with per-role filters).
- **C3 subagent** — sketches P-08 through P-13 (scenario storage + held-out runner + coordination medium + Cold-Start Bench + deterministic linter framework + maintenance loop).

### Per-primitive subagents (21 total, one each for P-14 through P-34)

The per-primitive dispatch will fire as a single parallel fanout wave to keep elapsed time bounded.

### Brief shape sent to each subagent

Per Round 2 of the [dispatch decision brief](../decisions/auto-001-phase-3.5-dispatch-shape.md#amendments-to-the-dispatch-brief-that-will-be-sent-to-subagents):

- **Construction path** must name at least one tool/library AND one **integration sentence** (how that tool's specific API/feature realizes the primitive's contract). No tool-name-only or shared-citations-across-primitives.
- **Corpus-why** must cite the specific corpus problem the primitive solves (not "this is commodity cloud engineering").
- **Research-grade-uncertainty flag** is mandatory when no plausible construction path is known.
- **Buildability verdict** is one of: `commodity`, `designed-system`, `research-grade-uncertainty`.

Cluster subagents are **forbidden** from rendering same-vs-distinct verdicts on primitives that look similar across candidates (defer to Phase 4.2 per scoping principle).

## Per-candidate primitive coverage (round-trip check)

This section confirms every primitive each candidate names appears somewhere in the enumeration above (with the cognitive-escrow primitives excluded per DEC-2).

| Candidate | Primitive IDs covered |
|---|---|
| [GF-S](../tracks/greenfield-substrate-first.md) | S1=P-01, S2=P-08+P-09, S3=P-05, S4=P-02, S5=P-06, S6=P-14, S7=P-10, S8=P-15 (+P-12, P-16 components), S9=P-19 |
| [GF-M](../tracks/greenfield-methodology-first.md) | Reversibility=P-20, Paraphrase=P-21, Holdout=P-08, Watchdog=P-06, Cost ceiling=P-02 (escrow demoted per DEC-2) |
| [GF-C](../tracks/greenfield-cold-start-first.md) | Intent Crucible=P-17, EARS+GtWR=P-16, Cold-Start Bench=P-11, RSI Ledger=P-18 (escrow demoted per DEC-2) |
| [BF-S](../tracks/brownfield-substrate-first.md) | S-1=P-22, S-2=P-23, S-3=P-07, S-4=P-24, S-5=P-25 |
| [BF-M](../tracks/brownfield-methodology-first.md) | Code-traversal=P-22, Telemetry=P-07, Trajectory=P-05, Sandbox=P-01, Worktree=P-03, Cost ceiling=P-02, Watchdog=P-06, Cross-family=P-14, Det-linters=P-12, Held-out runner=P-09, Scenario extractor=P-27, CaMeL=P-25, PR creator=P-04, Archaeological-brief=P-27 |
| [BF-L](../tracks/brownfield-legacy-ingestion-first.md) | Codebase Model=P-26 (composes P-22+P-23+P-07+P-24+conventional view+debt view), Ingestion engine=P-26 sub-component, Model-query interface=P-26 sub-component, Scenario-derivation=P-27, Regime classifier=P-19, Held-out partition=P-08, Maintenance loop=P-13 |
| [U-A](../tracks/unified-A.md) | Typed-object store=P-28, Policy mediator=P-29, Classifier=P-19, Judge router=P-14, Re-entry registrar=P-30 |
| [U-B](../tracks/unified-B.md) | Layer-typed store=P-28 (variant), Transition gates=P-29 (variant), Drift detector=P-31, Per-layer judge=P-14 |
| [U-C](../tracks/unified-C.md) | Anchor object=P-28 (variant), Distance estimator=P-32, Distance-gated dispatcher=P-19 (variant), Anchor mutation queue=P-28 (write surface), Distance-keyed trajectory=P-05 |
| [D7-U-1](../bias-guards/phase-3/d7-blind-axis/d7-u-1-prohibit-interval-escrow.md) | FC store=P-28 (variant), Opposing-side router=P-33, Compounding gate=P-29 (variant), Independence auditor=P-34, Survival-window registrar=P-30 (variant) |

**Same-vs-distinct verdicts deferred to Phase 4.2:** the typed-object store variants (P-28 across U-A / U-B / U-C / D7-U-1), the policy mediator / compounding gate variants (P-29 across U-A / D7-U-1), the registrar variants (P-30 across U-A / D7-U-1), the classifier / dispatcher variants (P-19 across GF-S / BF-L / U-C). Each variant gets its own per-primitive sketch focused on that candidate's specific contract; whether multiple variants collapse to a single primitive at the methodology-to-substrate matching stage is the Phase-4.2 question.

## Post-sketch annotations (running)

Updates from Phase-3.5.3 cluster-sketch subagents that change this index's pre-tags:

- **P-07 (Telemetry ingestor) — escalated `commodity` → `designed-system`.** Cluster-C2 sketch confirmed the per-role read-filter discipline is load-bearing for F28 holdout enforcement under the brownfield CTR-B5/CTR-G2 inversion. The storage half is commodity (OpenTelemetry Collector); the ABAC integration on top is not. See [`cluster-C2.md` § P-07](cluster-C2.md).
- **P-08 (Scenario storage) — escalated `commodity` → `designed-system`.** Cluster-C3 sketch confirmed the substrate-enforced role-keyed partition (OPA ABAC over `partition=train|holdout` against builder/judge role tokens) is the load-bearing F28-critical integration; storage half is commodity. See [`cluster-C3.md` § P-08](cluster-C3.md).
- **P-08 / P-09 collapse question raised but not decided.** Cluster-C3 sketch flagged honest evidence that P-09 (held-out scenario runner) reduces to a thin read-API on P-08 with the judge-role token; the cluster subagent did NOT render a same-vs-distinct verdict (per the cluster-subagent constraints). Deferred to Phase 4.2.

Updated counts after C2/C3 reclassifications: 11 commodity (C1: 4 + C2 P-05/P-06 + C3 P-09/P-10/P-11/P-12/P-13) + 23 designed-system / research-grade (was 21; +P-07, +P-08). The dispatch tiers don't change retroactively — the cluster sketches landed correctly under the original dispatch — but the *index's* commodity-vs-designed classification updates to reflect the sketches' findings.

### Per-primitive sketch annotations (P-14 through P-34)

Per-primitive sketches landed in wave 2 (subagent fanout per Round-2 hybrid dispatch). Final verdicts and key findings:

| ID | Verdict | Key construction tool | Notable finding |
|---|---|---|---|
| P-14 Judge router | `designed-system` | LiteLLM `Router` + Pydantic per-role envelopes | Resolves CTR-C4 via typed choice; F46 mitigation |
| P-15 Four-guard mediator | `designed-system` (contradiction-detector sub-guard carries partial RG flag) | Composition over P-12 engine + LiteLLM ensemble | Larbi MCC ≤ 0.55 ceiling for contradiction-detector is empirically open (F27/F48 collusion risk) |
| P-16 EARS+GtWR linter | `designed-system` | Custom Python rule engine on spaCy | **P-12 can host P-16** (high confidence); likely absorption into P-12 at Phase 4.2 |
| P-17 Intent Crucible validator | `designed-system` (partial RG flag on substance-check) | Pydantic v2 + `@model_validator` + structured-outputs | 2 of 9 fields (`business_outcomes`, `capability_scope`) substance-check is RG; structural validation is bounded |
| P-18 RSI Declaration Ledger | `designed-system` | SQLite WAL + abort triggers + Merkle hash chain | RSI = Recursive Self-Improvement (Kahana/Stanford-CodeX); mitigates F43, F53; F54/F55/F58 |
| P-19 Eligibility / regime classifier | `designed-system` | Hybrid: Drools/OPA Rego decision tables + LLM-judge fallback via P-14 + OPA hard-floor post-check | F25 / F57 hard-floor enforcement; F51 recursion question is Phase-4.2 / Phase-8 |
| P-20 Reversibility primitive | `designed-system` | EventStoreDB (`AppendToStream`); axon-framework / Postgres event_log fallback | Composes on P-05; cost dominated by paraphrase fan-out (OQ-T2), not by reversibility itself |
| P-21 Paraphrase divergence | `designed-system` (calibration is RG, not buildability) | LiteLLM + asyncio.gather + Jinja2 seeded macros + sentence-transformers | N, divergence metric, threshold vs Larbi MCC ≤ 0.55 are Phase-8 lean-eval candidates (OQ-T6) |
| P-22 Polyglot codebase index | `designed-system` | tree-sitter + per-language LSP federation + SQLite-FTS/DuckDB (single-tenant); Sourcegraph/SCIP (fleet); Glean (Meta-scale) | Type fidelity uneven across languages; cross-language type resolution at RPC boundaries is near-zero (Phase-4 risk marker) |
| P-23 Dependency-impact graph | `designed-system` | Glean (Datalog) + Stack Graphs cross-language resolver | **BF-S B7 partition-leakage is structural** — transitive closure leaks hidden-node info; mitigable to rate-limited side channel only. Critical for Phase-3.5.5 BF-S re-check. |
| P-24 Attribution store | `designed-system` | Git plumbing (`git verify-commit` + `git blame --line-porcelain`) + Sigstore/cosign + Postgres projection | Hard P-22 dependency for per-symbol granularity (rename-edges → `parent_event_id`) |
| P-25 CaMeL perimeter | `designed-system` (partial RG on utility-tax calibration) | Released CaMeL ref impl (`google-research/camel-prompt-injection`) + OPA + eBPF | Utility-tax not measurable a-priori; substrate must expose per-class bypass with audit-log |
| P-26 Codebase Model | **`research-grade-uncertainty`** (gated by 2 of 6 RG views: conventional + invariant) | Glean + SCIP + Tree-sitter (structural); P-24 + cosign (historical); P-07 + OPA (runtime); CodeScene + SonarQube (debt); LLM + golden corpus (conventional, RG); Daikon + CodeQL + LLM (invariant, RG) | 9-18 engineer-months realistic. **BF-L recommended to SURVIVE Phase 3.5 with RG flag carried forward to Phase 4** (do not self-eliminate). |
| P-27 Archaeological-brief tooling | `designed-system` (partial RG on brief-quality calibration) | Pydantic v2 Brief schema + Anthropic/OpenAI structured outputs + tool-use loop over P-26 query interface | Brief-quality gating mirrors P-17 structural-vs-substance split; calibration deferred to Phase 5/8 |
| P-28 Typed-object store | `designed-system` (all 4 variants viable) | libgit2 (`git_odb_write` + `refs/notes/<envelope-kind>`); Postgres `bytea`+`jsonb`+GIN | Per-variant envelope schemas distinct (U-A typed-node-graph, U-B layer-typed L0–L4, U-C anchor with `frozen-since`+`mutation-protocol`, D7-U-1 FC commitment). Same-vs-distinct DEFERRED to Phase 4.2. |
| P-29 Policy mediator | `designed-system` (both variants viable) | OPA Rego (`opa eval` at boundary); Cedar alternative | Per-variant policy DSL is design content; same-vs-distinct DEFERRED to Phase 4.2 |
| P-30 Event registrar | `designed-system` (both variants viable) | Temporal workflow engine (signal+timer+query triad); AWS EventBridge / Kafka / Postgres-NOTIFY alternatives | Per-variant state machines distinct (U-A re-entry interval; D7-U-1 survival-window). Same-vs-distinct DEFERRED to Phase 4.2 |
| P-31 Cross-layer drift detector | **`research-grade-uncertainty`** | Substrate (OPA graph-walk + LLM judge via P-14) is commodity; **the invariants don't exist** | Brier's framework is descriptive, not algorithmic. **U-B must commit at Phase 4 to an invariant-authoring sub-track delivering ≥3 machine-checkable invariants per layer-pair with corpus citations**, otherwise P-31 cannot be defended. |
| P-32 Distance estimator | `designed-system` (construction); `research-grade-uncertainty` (calibration + partial Goodhart resistance) | Per-component: Glean/CodeQL/Stack-Graphs BFS over P-23 (graph_distance); deterministic decision table (pace_layer_crossings); P-22 + LLM judge (intent_field_touches) | Calibration recipe absent in corpus; 2 of 3 legs Goodhart-resistant, third leg F33/F51-vulnerable with patrol-tier detector only (does not close F47) |
| P-33 Opposing-side router | `designed-system` | LiteLLM `Router` + FC-typed dispatch + YAML/SQLite capability registry | "Do-not-unify" enforced via `tags=["exclude:"+builder.family]`; honest evidence: shares substantial substrate with P-14 but has FC-shaped surface, unconditional builder-family exclusion, broader handler universe. Same-vs-distinct DEFERRED to Phase 4.2 |
| P-34 Independence auditor | **`research-grade-uncertainty`** (structural; construction is designed-system) | scipy `binomtest` + Fisher exact + IsolationForest pipeline over P-28 FC log | **Recommended audit-recursion**: Option A (deterministic-ness is the assurance) as primary + Option C (named human review at low cadence) as backstop. No option dominates; corpus does not name a recursion-stopping rule. |

### Critical findings for Phase 3.5.5 candidate re-check

The post-sketch annotations surface several findings that **change candidate defense status** and must be processed at Phase 3.5.5:

1. **BF-S partition-leakage is structural** (P-23 sketch). BF-S's B7 ROBUST claim of substrate-enforced role-partition was contested in Phase 3.2 red-team; the buildability sketch confirms the contestation. BF-S cannot fully defend on B7 — partition leakage is mitigable to a rate-limited side channel but not eliminable. BF-S survives Phase 3.5 but with a downgraded B7 claim.

2. **BF-L Codebase Model survives with research-grade flag** (P-26 sketch). The conventional + invariant views are RG-uncertainty; the other 4 views are designed-system. 9-18 engineer-months realistic. BF-L does NOT self-eliminate at Phase 3.5 — the candidate carries forward with the RG flag honestly displayed.

3. **U-B cross-layer drift detector unbuildable without invariant authoring** (P-31 sketch). U-B's P-31 cannot be defended at Phase 3.5; U-B must commit at Phase 4 to authoring ≥3 machine-checkable invariants per layer-pair. If U-B accepts that commitment, the candidate survives Phase 3.5 with the deferred-defense flag. If U-B cannot accept, U-B self-eliminates at Phase 3.5 — adjudicate at 3.5.5.

4. **D7-U-1 independence auditor is structurally research-grade** (P-34 sketch). Auditor-recursion (OQ-1) has no dominating option; recommended A+C hybrid is best-current but not closure. D7-U-1 carries forward with explicit RG flag on P-34.

5. **GF-S contradiction-detector reliability is empirically open** (P-15 sketch). The sub-guard's Larbi MCC ≤ 0.55 ceiling is single-judge; the 3-of-N ensemble lifts effective reliability but the empirical question is Phase-8. GF-S survives Phase 3.5 with this carried as Phase-8 lean-eval input.

6. **P-12 likely absorbs P-16** (P-16 sketch). At Phase 4.2 same-vs-distinct resolution, P-16's rule library likely becomes content on P-12's framework. The two are not the same primitive at Phase 3.5 — sketches landed independently — but the absorption is high-confidence and recorded for Phase 4.2 work.

7. **Same-vs-distinct on 4 contested primitive variants is honestly deferred** (P-28, P-29, P-30 sketches). All three primitives' variant pairs (U-A/U-B/U-C/D7-U-1 envelope variants on P-28; U-A/D7-U-1 variants on P-29 and P-30) have viable buildability paths per variant; the same-vs-distinct question is genuinely Phase-4.2 work, not pre-judged.

8. **P-08 ↔ P-09 collapse evidence** (C3 sketch). Same as #7 but for the held-out scenario runner / scenario storage pair. Deferred to Phase 4.2.

### Final distinct-primitive count after Phase 3.5 sketches

- **Commodity**: 11 (P-01, P-02, P-03, P-04, P-05, P-06, P-09, P-10, P-11, P-12, P-13)
- **Designed-system**: 19 (P-07, P-08, P-14, P-15, P-16, P-17, P-18, P-19, P-20, P-21, P-22, P-23, P-24, P-25, P-27, P-28, P-29, P-30, P-32, P-33)
- **Research-grade-uncertainty**: 4 (P-26 Codebase Model, P-31 Cross-layer drift detector, P-34 Independence auditor; P-32 partial RG on calibration)
- **Total**: 34 enumerated IDs; ~32 distinct after expected Phase 4.2 collapses (P-12+P-16, P-08+P-09).

Note: many designed-system primitives carry *partial* RG flags on specific sub-components or calibration questions (P-15 contradiction-detector, P-17 substance-check, P-21 calibration, P-25 utility-tax, P-27 brief-quality, P-32 calibration + Goodhart-resistance). These do not move the primary verdict but are recorded for Phase 4 / Phase 5 / Phase 8 work.
