# Wave 4.2 — Primitive overlap analysis (side artifact, not winner-picker)

**Author.** Lead agent, Phase 4.2 serial step per [auto-004 Round 2 § Wave 4.2](../decisions/auto-004-phase-4-dispatch-shape.md#wave-42-overlap-analysis-unchanged-from-round-1).
**Inputs.** All 10 [Wave-4.1 substrate-requirements summaries](../substrate-requirements/) + the [contested-primitive sketches](../primitives/) (P-28, P-29, P-30, P-19) + the [cluster sketches](../primitives/) (P-08↔P-09 + P-12↔P-16 collapse questions) + the [`primitives/index.md` post-sketch annotations](index.md#post-sketch-annotations-running).
**Scope (binding).** Per the [v1.2 plan revision](../../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md#phase-4--per-candidate-substrate-requirements--shared-discipline-extraction-revised-in-v12), this analysis is **informational, not winner-picking**. An overlapped primitive becomes a higher-priority ADR target in Phase 5; an orphan primitive (claimed by one candidate or none) still ships an ADR if its candidate carries it.

## §1 Same-vs-distinct verdicts on deferred questions

### P-28 (typed-object store) — four contested variants

| Variant | Candidate | Envelope schema (from §3 of substrate-requirements/<id>.md) | Primary typed-filter axis |
|---|---|---|---|
| Typed-node-graph | U-A | `EscrowInterval{id, kind, pace-layer, priors, policies, classifier, artefacts}` | `kind × pace-layer × classifier.work-unit-class` |
| Layer-typed | U-B | `TypedObject<L>{layer ∈ {L0..L4}, change-rate, escrow-policy, invariants[], parent-layer-ref, child-layer-refs[]}` | `layer × (parent-layer-ref → child-layer-refs)` traversal |
| Anchor | U-C | `Anchor{kind, content, frozen-since, owning-mandate, mutation-protocol}` | `kind × owning-mandate` with immutability-metadata first-class |
| FC | D7-U-1 | `FC{id, artifact, artifact-kind, conjecture, opposing-side, refutation-attempt, verdict, ledger}` | `artifact-kind × verdict.outcome` |

**Verdict: SAME primitive (P-28 typed-object store framework), DISTINCT envelopes.** All four share the construction recipe (libgit2 `git_odb_write` + `refs/notes/<envelope-kind>`; Postgres `bytea`+`jsonb`+GIN alternate path; content-addressed append-only with typed envelope per [P-28 sketch](P-28-typed-object-store.md)). The envelope schemas are non-overlapping but the underlying primitive (typed envelope + content-hash + append-only + Glean/Postgres-compatible storage) is identical.

**Implications for Phase 5 ADRs:**
- One **common ADR** on P-28 substrate (storage choice, content-hash scheme, append-only discipline, envelope-typing contract).
- Four **candidate-specific ADRs** on per-variant envelope schema (one each: U-A interval envelope; U-B layer envelope; U-C anchor envelope; D7-U-1 FC envelope).
- The variants are NOT mutually exclusive at substrate level — a single deployment could host multiple envelope variants on the same P-28 substrate (different `refs/notes/<envelope-kind>` namespaces). Phase 6 architecture specs determine which candidates share a substrate vs deploy separately.

### P-29 (policy mediator / compounding gate) — three contested variants

| Variant | Candidate | Policy DSL | Closure axis |
|---|---|---|---|
| Interval-closure | U-A | Rego/Cedar; closure conditions per `EscrowInterval.policies` slots | Per-interval slot satisfaction |
| Per-layer-boundary | U-B | Rego; per Lᵢ→Lᵢ₊₁ closure encoding upstream layer's `escrow-policy` | Per-layer-pair boundary |
| FC-survival | D7-U-1 | Rego/Cedar; FC-survival vocabulary on `verdict.outcome ∈ {survived, conditionally-survived-with-window}` | FC ledger walk |

**Verdict: SAME primitive (P-29 policy mediator framework), DISTINCT policy DSLs.** All three share the underlying engine (OPA Rego primary; Cedar alternate path per [P-29 sketch](P-29-policy-mediator.md)). The policy vocabulary differs: U-A reasons about interval-slot satisfaction; U-B reasons about layer-pair closure; D7-U-1 reasons about FC-survival windows. The differences are at the *predicate vocabulary* level, not the *engine* level.

**Implications for Phase 5 ADRs:**
- One **common ADR** on P-29 substrate (Rego vs Cedar choice; policy-loading discipline; bundle-API for L0-standards-versioned policies).
- Three **candidate-specific ADRs** on per-variant policy vocabulary (one each: U-A interval-policy schema; U-B layer-boundary schema; D7-U-1 FC-survival schema).

### P-30 (event registrar) — two contested variants

| Variant | Candidate | State machine | Trigger source |
|---|---|---|---|
| Re-entry interval | U-A | `in-flight → frozen → re-entry-open → operator-acknowledged → {resumed, redirected, closed}` | Event-driven (watchdog escalation / cost-ceiling breach / severity-class trigger) |
| Survival-window | D7-U-1 | `FC-declared → opposing-side-running → verdict-rendered → survival-window-open → window-expired → re-falsification-required` | Timer-driven (window expiry wakes dependent FC graphs) |

**Verdict: DISTINCT primitives** despite shared underlying substrate. Both use [Temporal workflow engine (signal+timer+query triad)](P-30-event-registrar.md) at the construction layer, but the load-bearing semantics diverge:

- U-A's registrar is **event-driven**: state transitions on external triggers; the timer half is incidental (deadline tracking only).
- D7-U-1's registrar is **timer-driven**: the load-bearing transition is `survival-window-open → window-expired`, with cascade wake-up of dependent-FC graphs. The event half is incidental (verdict-rendered is the input event but the registrar's value-add is the post-verdict timer cascade).

The state-machines have non-overlapping invariants. A single deployment hosting both candidates' methodologies would need two separate registrar instances (or a shared instance with strict namespace separation of `state-machine-class` field).

**Implications for Phase 5 ADRs:**
- One **common ADR** on the underlying Temporal substrate choice (Temporal vs AWS EventBridge vs Postgres-NOTIFY).
- Two **distinct ADRs** on per-variant state machine definitions (U-A re-entry; D7-U-1 survival-window). The variants are NOT collapsible: their invariants differ; their subscriber sets differ; their failure-mode profiles differ (U-A's re-entry can starve on operator non-acknowledgement; D7-U-1's survival-window can cascade-fail if the timer half is unreliable).

### P-19 (eligibility / regime classifier) — four contested variants

| Variant | Candidate | Feature source | Output regime set |
|---|---|---|---|
| Work-unit-class | GF-S | intent-block-fields-touched, declared stakes, scenario-set saturation, recent cross-family judge agreement, bar-set parameters | `automation-eligible / augmentation-required / escalate` |
| Per-region | BF-L | Code-region features from Codebase Model (P-26): test-coverage, runtime telemetry, churn cadence, Caremark/RSI tag, debt-cluster, idiom-conformance (conditional), invariant-density (conditional) | Per-region regime (output regime is per region, not per cycle) |
| Distance-gated | U-C | P-32 DistanceTuple (graph_distance, pace_layer_crossings, intent_field_touches) + contradiction_flag hard-floor | `lights-out / cross-model-judging / human-required` |
| Interval-kind | U-A | `EscrowInterval.kind`, `pace-layer`, `priors` fields at interval-open time + substrate-current judge agreement + cost-ceiling state | `automation-eligibility` consumed by P-29 and P-30 |

**Verdict: SAME primitive (P-19 classifier framework), DISTINCT feature sources + distinct output regime sets.** All four share the construction recipe (Drools/OPA Rego decision tables + LLM-judge fallback via P-14 + OPA hard-floor post-check per [P-19 sketch](P-19-eligibility-regime-classifier.md)). The differences are at the *feature engineering* layer and the *output enum* layer, not the *decision-engine* layer.

**Implications for Phase 5 ADRs:**
- One **common ADR** on P-19 substrate (decision-table engine choice; LLM-fallback discipline; hard-floor post-check pattern).
- Four **candidate-specific ADRs** on per-variant feature sources (one each).
- **Phase-8 lean-eval candidate:** measure whether the four feature sources produce correlated regime outputs on a shared scenario set. If yes, the candidates may be making different methodology bets on the same substrate; if no, the feature sources are genuinely distinct cognitive frames.

### P-08 ↔ P-09 — held-out runner / scenario storage collapse

[Cluster-C3 sketch](cluster-C3.md) flagged honest evidence that P-09 (held-out scenario runner) is a thin read-API on P-08 (scenario storage) with the judge-role token. BF-M's [substrate-requirements summary](../substrate-requirements/bf-m.md) names them separately; GF-S names P-08+P-09 as a composite (S2). BF-L and GF-M name only P-08.

**Verdict: P-09 ABSORBS INTO P-08.** P-09 is the **read-API contract** on P-08's substrate; not a separate primitive. The held-out runner is `P-08.read(partition='holdout', judge-role-token=...) → ScenarioResult`. P-08's contract is extended to include the runner-API (deterministic replay + verdict emission); P-09 disappears as a separate primitive ID.

**Implications for Phase 5 ADRs:**
- One **common ADR on P-08** with the runner-API as part of its contract (no separate P-09 ADR).
- BF-M's substrate-requirements summary's §5 deferral is RESOLVED here; downstream phases work with the absorbed primitive.

### P-12 ↔ P-16 — deterministic linter framework / EARS+GtWR rule library absorption

[P-16 sketch](P-16-ears-gtwr-linter.md) noted high-confidence absorption: "P-12 can host P-16." GF-C's [substrate-requirements summary](../substrate-requirements/gf-c.md) names them separately and flags the absorption question. GF-S/S8 names P-15 (4-guard mediator) over P-12 + P-16 components.

**Verdict: P-16 ABSORBS INTO P-12.** P-12 is the **rule-engine framework** (deterministic per-cycle checks); P-16 is a **specific rule library** (INCOSE R7-R35 + EARS pattern conformance) running on that framework. The framework and the library are distinct artifacts at the engineering layer (P-12 is the engine; P-16 is configuration data + rule-pack), but they are not separable as substrate primitives — a P-12 deployment without rule packs is non-functional; a rule pack without a framework is non-executable.

**Implications for Phase 5 ADRs:**
- One **common ADR on P-12** as the framework, with EARS+GtWR + other rule packs as content.
- The rule library specification (which R7-R35 rules, which EARS subset, custom rule extensions) is **per-candidate ADR content**: GF-C names the full INCOSE R7-R35 + EARS subset; GF-S/S8 names the four-guard subset (GtWR lint + contradiction-detector + req-count budgeter + perimeter typing) as the active rule set.
- P-16's ID is retired as a distinct primitive; future references resolve to "P-12 with the EARS+GtWR rule pack."

### P-33 vs P-14 — opposing-side router vs judge router

D7-U-1's [substrate-requirements summary](../substrate-requirements/d7-u-1.md) §3 honestly notes: "Shares substrate with P-14 (same-vs-distinct deferred to Phase 4.2)." The [P-33 sketch](P-33-opposing-side-router.md) confirms shared substrate (LiteLLM Router + capability registry) but flags structural differences: FC-shaped surface, unconditional builder-family exclusion, broader handler universe (includes deterministic checkers + named humans + population vote, not just LLM judges).

**Verdict: DISTINCT primitives** despite shared underlying tool. Both use LiteLLM Router at the construction layer, but:

- **P-14 (judge router)** is a *router over LLM judge endpoints* with provider-family-diverse routing and typed input/output shapes per judge role. The handler universe is LLM judges (with optional deterministic-judge inclusion as a degenerate case).
- **P-33 (opposing-side router)** is a *router over the full opposing-side handler universe* — LLM judges (with unconditional builder-family exclusion), deterministic checkers (Python predicates), named-human approvers, population votes. The router's load-bearing value-add is the *exclusion logic* (three-layer denylist: call-time computed + LiteLLM tag-exclusion + registry family-allowlists) and the *kind-dispatch logic* (FC-shaped: routes by `refutation-attempt.method`).

P-14 → P-33 is NOT a generalization-specialization relationship at the substrate level; the routers have different *contract surfaces*. A deployment could share LiteLLM Router infrastructure but the routing-policy layer is per-primitive.

**Implications for Phase 5 ADRs:**
- One **common ADR** on the shared underlying substrate (LiteLLM Router + capability registry).
- Two **distinct ADRs** on per-primitive routing contract (P-14 judge-routing; P-33 opposing-side routing). Note: P-33 has substantial shared substrate with P-14 but is NOT collapsible without losing D7-U-1's *do-not-unify* discipline (the unconditional builder-family exclusion).

## §2 Primitive overlap counts (by candidate-coverage)

Distinct-primitive count after P-09 → P-08 + P-16 → P-12 absorptions: **30 primitives** (down from 32 expected pre-Phase-4.2 collapse; down from 34 enumerated IDs).

| Primitive | Mandate-fit candidates claiming | Coverage tier |
|---|---|---|
| P-01 Sandbox | GF-S, BF-M, implicit-all | **All 10** (commodity-floor) |
| P-02 Cost ceilings | GF-S, GF-M, BF-M, implicit-all | **All 10** |
| P-05 Trajectory capture | GF-S, BF-M, U-C, implicit-most | ≥7 |
| P-06 Watchdog tiers | GF-S, GF-M, BF-M, implicit-most | ≥7 |
| P-08 Scenario storage (with runner contract) | GF-S, GF-M, BF-L, BF-M | 4 |
| P-14 Judge router | GF-S, BF-M, U-A, U-B | 4 |
| P-22 Polyglot codebase index | BF-S, BF-M, BF-L (via P-26), U-C (via P-32) | 4 |
| P-07 Telemetry ingestor | BF-S, BF-M, BF-L (via P-26) | 3 |
| P-19 Eligibility/regime classifier | GF-S, BF-L, U-A, U-C | 4 (distinct feature-sources) |
| P-28 Typed-object store | U-A, U-B, U-C, D7-U-1 | 4 (distinct envelopes) |
| P-29 Policy mediator | U-A, U-B, D7-U-1 | 3 (distinct policy DSLs) |
| P-30 Event registrar | U-A, D7-U-1 | 2 (DISTINCT primitives — registrar collapse rejected) |
| P-23 Dependency graph | BF-S, BF-L (via P-26), U-C (via P-32) | 3 |
| P-12 Linter framework (incl. EARS+GtWR rule pack) | GF-S, GF-C, BF-M | 3 |
| P-25 CaMeL perimeter | BF-S, BF-M | 2 |
| P-27 Archaeological-brief tooling | BF-M, BF-L | 2 |
| P-03 Worktree isolation | BF-M | 1 |
| P-04 PR creator | BF-M | 1 |
| P-10 Coordination medium | GF-S | 1 |
| P-11 Cold-Start Bench | GF-C | 1 |
| P-13 Maintenance loop | BF-L | 1 |
| P-15 Four-guard mediator | GF-S | 1 |
| P-17 Intent Crucible validator | GF-C | 1 |
| P-18 RSI Declaration Ledger | GF-C | 1 |
| P-20 Reversibility primitive | GF-M | 1 |
| P-21 Paraphrase divergence | GF-M | 1 |
| P-24 Attribution store | BF-S (BF-L via P-26 composes it) | 1-2 |
| P-26 Codebase Model | BF-L | 1 |
| P-31 Cross-layer drift detector | U-B | 1 |
| P-32 Distance estimator | U-C | 1 |
| P-33 Opposing-side router | D7-U-1 | 1 (DISTINCT from P-14 — router collapse rejected) |
| P-34 Independence auditor | D7-U-1 | 1 |

### Coverage-tier summary (Phase 5 ADR-priority signal)

- **Shared by ≥3 candidates (10 primitives):** P-01, P-02, P-05, P-06, P-08, P-14, P-22, P-07, P-19, P-28, P-29, P-23, P-12 — these get **common ADRs** in Wave 5.1 per the [v1.2 plan revision](../../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md#phase-5--adrs-per-candidate-with-cross-references-on-shared-primitives-revised-in-v12).
- **Shared by 2 candidates (4 primitives):** P-30, P-25, P-27, P-24 — common ADRs candidates; lead-agent call at Phase 5 dispatch.
- **Orphan (claimed by 1 candidate, 16 primitives):** P-03, P-04, P-10, P-11, P-13, P-15, P-17, P-18, P-20, P-21, P-26, P-31, P-32, P-33, P-34 — candidate-specific ADRs only; preserved per scoping principle as cross-pollination fuel.

## §3 Findings carried into Wave 4.6

1. **6 of the 8 deferred same-vs-distinct questions resolved as SAME with distinct variants** (P-28, P-29, P-19) + **2 resolved as DISTINCT** (P-30, P-33 vs P-14) + **2 absorption questions resolved YES** (P-09 → P-08, P-16 → P-12).

2. **Phase-5 ADR count estimate refined.** From the v1.2 plan's rough 50-80 total:
   - **Common ADRs (≥3-candidate primitives):** 13 (was estimated 12-18).
   - **2-candidate ADRs:** 4 (lead-agent call at Phase 5 dispatch on whether to draft as common or per-candidate).
   - **Orphan ADRs:** 16 across 10 candidates (split per-candidate per ownership: GF-M owns P-20+P-21; GF-C owns P-11+P-17+P-18; BF-S owns P-24; BF-L owns P-26+P-13; BF-M owns P-03+P-04+P-27 share; U-B owns P-31; U-C owns P-32; D7-U-1 owns P-33+P-34; GF-S owns P-10+P-15).
   - **Per-variant envelope/policy/feature-source ADRs:** P-28 × 4 = 4; P-29 × 3 = 3; P-19 × 4 = 4; P-30 × 2 = 2. Total: 13 per-variant ADRs.
   - **Discipline ADRs (Wave 4.3 outputs):** ~8-12 (Wave 4.6 merge sizes this).
   - **Total Phase-5 ADR estimate: ~54-62** (within the 50-80 v1.2 plan envelope).

3. **No candidate's substrate-requirements changed structurally** from Phase-4.1. The overlap analysis is informational; no candidate shrinks, no candidate pre-eliminates.

4. **Phase-6 architecture-spec consequences.** For shared primitives, each candidate's spec carries a YAML reference to the common ADR + its candidate-specific ADR. The mandate-fit matrix (10 rows × work-unit-classes) does not change shape from Phase-4 entry.

5. **Phase-8 lean-eval candidates surfaced or strengthened:**
   - P-19 four-variant correlation pressure-test (do the four feature sources produce correlated regimes on a shared scenario set?)
   - P-28 envelope-collision pressure-test (can multiple envelope variants coexist on one P-08-shared substrate without cross-talk?)
   - P-30 timer-half vs event-half reliability pressure-test (U-A vs D7-U-1 registrar failure-mode profiles)

## §4 Honest acknowledgements

- **The "Wave 4.2 = lead-agent serial" budget held.** All 6 same-vs-distinct verdicts were renderable from the Wave-4.1 summaries + the contested-primitive sketches + the cluster sketches. No re-dispatch was needed.
- **The §3 fixed sub-section headers (Reviewer 1 A4 amendment to auto-004 Round 2) made the Wave-4.1 → Wave-4.2 diff structurally cheap.** Each contested primitive's `envelope schema:` / `policy DSL:` / `state-machine semantics:` / `feature source:` sub-section was eyeball-comparable across candidates. Without the fixed headers, Wave 4.2 would have required re-reading the four contested sketches at full depth.
- **Same-vs-distinct verdicts are NOT winner-picking calls.** A candidate whose primitive variant is "distinct" from others has NOT been demoted; the variant is preserved as a defensible architectural choice per the [scoping principle](../phase-3.4-decisions-resolved.md#scoping-principle-immutable-overrides-any-conflicting-framing-in-the-integration-brief).
- **The Wave-4.6 (Phase-4 close aggregation) step inherits this analysis as input** for registry updates + Phase-5 ADR dispatch staging.
