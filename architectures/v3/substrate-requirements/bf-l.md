# Substrate requirements — BF-L (Brownfield, legacy-ingestion-first)

**Candidate.** [BF-L — Brownfield, legacy-ingestion-first](../tracks/brownfield-legacy-ingestion-first.md). Mandate: brownfield. Axis: code-archaeology is the primary organizing principle; the **Codebase Model** is the load-bearing substrate primitive and the methodology is three loops over it.

**Phase-3.5.5 status.** `survives with research-grade-uncertainty flag on Codebase Model` (per [registry §BF-L](../candidate-registry.md#bf-l--brownfield-legacy-ingestion-first-1)). Two of P-26's six views (conventional, invariant) land RG; four (structural, historical, runtime, debt) plus the integration discipline land designed-system. Forward action per [`auto-003` Round 2](../decisions/auto-003-bfl-rg-view-choice.md): option A′ — **smoke-test-first per view**.

**Research-blind annotation.** Wave-4.4 research notes have landed at [`bfl-conventional-view-prior-art.md`](../research-notes/bfl-conventional-view-prior-art.md) and [`bfl-invariant-view-prior-art.md`](../research-notes/bfl-invariant-view-prior-art.md) per [`auto-004` Round 2](../decisions/auto-004-phase-4-dispatch-shape.md#wave-41-brief-shape-revised-per-reviewer-1-amendments). This summary is **research-aware but not research-derived**: Wave 4.5 (smoke-test then conditional sub-track) is the consumer of those notes.

## §1 Primitive list (buildability-confirmed)

BF-L requires 5 substrate primitive families. P-26 is the load-bearing one; the others are commodity-or-near-commodity composition partners.

- **[P-26 — Codebase Model (6 views, integrated)](../primitives/P-26-codebase-model.md).** Durable, versioned, queryable artifact integrating structural / conventional / historical / runtime / invariant / debt views. *Built* by ingestion (Loop 1), *queried* per-cycle (Loop 2), *refreshed* by maintenance (Loop 3). Verdict: **`research-grade-uncertainty` overall** — gated by 2 of 6 views; 9-18 engineer-months realistic. "The most ambitious primitive in the catalog" per [primitives/index.md](../primitives/index.md).
- **[P-27 — Scenario-derivation tooling](../primitives/P-27-archaeological-brief-tooling.md).** BF-L's *scenario-derivation* primitive (Pydantic-typed envelope, LLM-with-structured-output over the P-26 query surface). Same construction shape as BF-M's archaeological-brief, different output schema. Verdict: `designed-system` (partial RG on brief-quality calibration — sketch's own flag).
- **[P-19 — Eligibility / regime classifier (per-region variant)](../primitives/P-19-eligibility-regime-classifier.md).** Maps a code region (tagged by the Codebase Model) to a regime label; substrate enforces via OPA hard floors. Verdict: `designed-system`.
- **[P-08 — Scenario storage (out-of-tree, holdout-partitioned)](../primitives/cluster-C3.md).** BF-L enforces *held-out partition* discipline *within* the inherited scenario set (subsets of the Codebase Model marked held-out; ingestion-aware judges enforce the partition). Verdict: `designed-system`.
- **[P-13 — Maintenance loop](../primitives/index.md).** Continuous low-cadence reconciliation between the Codebase Model and reality (the Loop-3 mechanism). Verdict: `commodity`.

Sub-primitives composed inside P-26 but not separately named: P-22 (polyglot index), P-23 (dependency / blast-radius), P-24 (signed attribution), P-07 (telemetry ingestor).

## §2 RG primitives

BF-L is the **canonical case the [Phase-3.5.5 RG-primitive rule](../candidate-registry.md#phase-355-rule-on-load-bearing-rg-primitives-binding-user-approved-2026-05-25) was authored for** — a full load-bearing RG primitive with two RG-uncertain views, each governed independently by the (a)/(b) choice.

**Application-table rows (verbatim text-pull from registry §"Application to current candidates"):**

> BF-L | P-26 conventional view | **candidate's choice at Phase 4 entry** | Default if no choice declared: (b) accept-as-RG. BF-L may opt-in to (a) bounded sub-track for some or all of: LLM-with-structured-output + golden corpus of ≥20 idiomatic patterns per supported language.

> BF-L | P-26 invariant view | **candidate's choice at Phase 4 entry** | Default if no choice declared: (b) accept-as-RG. BF-L may opt-in to (a) bounded sub-track: Daikon-style runtime inference + ≥5 invariants per language.

**Choice (per [`auto-003` Round 2](../decisions/auto-003-bfl-rg-view-choice.md#decision-round-2)).** For *both* views: **option A′ — smoke-test-first per view; full sub-track if smoke-test passes; otherwise (b) accept-as-RG with the methodology-degradation clause activating**. The smoke-test pattern mirrors U-B's auto-002 Round 2 constructive-existence shape — ≥3 non-trivial substantive conventions/invariants per language across top-3 languages (Python / TypeScript / Java by default), each carrying typed envelope + corpus citation + positive/negative example + honesty-discipline clause. Verdict logic: ≥2/3 languages → full Wave-4.5b sub-track for that view (scale to ≥10-per-language); 1/3 → contract restates per-language; 0/3 → (b) for that view. The two views are evaluated independently. Both smoke-tests and the conditional sub-tracks are **Wave 4.5 work**, not Wave 4.1 work.

## §3 Candidate-specific contracts on each primitive

BF-L's contracts on each named primitive — deltas from the sketches' defaults named where they exist.

- **P-26 Codebase Model (load-bearing).** BF-L's contract is the **integrated** six-view artifact, not a federation of separate stores: common ID space (structural symbol IDs), join API (`model.join(symbol, version, [views])`), snapshot consistency at version boundaries, Merkle-DAG incremental versioning. The integration discipline IS what distinguishes BF-L from BF-S. BF-L takes the [P-26 sketch's](../primitives/P-26-codebase-model.md) construction-per-view defaults; the methodology-degradation clause (per [`auto-003` Round 2](../decisions/auto-003-bfl-rg-view-choice.md#methodology-degradation-clause-new-per-reviewer-2-a2)) names what happens when conventional or invariant view falls back to (b).

- **P-19 Eligibility / regime classifier (contested primitive).**

  **feature source:** Code-region features pulled from the Codebase Model (P-26) — test-coverage density (runtime view), runtime-telemetry density (runtime view), historical churn cadence (historical view), Caremark/RSI exposure tag (debt + structural views), debt-cluster membership (debt view), conventional-view idiom-conformance score (conventional view, *conditional*), invariant-density score (invariant view, *conditional*). Output regime is *per region*, not per cycle — a cycle touching multiple regions inherits the strictest classification. Per the [P-19 sketch's BF-L bullet](../primitives/P-19-eligibility-regime-classifier.md), this per-region variant is the load-bearing answer to BF-L's CTR-A4 lights-out / L5 mapping question. The conventional and invariant feature-source components are gated on Wave 4.5 outcomes: when either view falls back to (b), the corresponding feature drops and the methodology-degradation clause activates.

- **P-27 Scenario-derivation tooling.** Scenarios are **inherited from the Codebase Model**, not authored out-of-tree (BF-L's explicit challenge to D-2). New scenarios are *derived* from gaps in the model (low-coverage regions; runtime patterns no test exercises; invariants extracted from code but not enforced).

- **P-08 Holdout partition.** Substrate marks subsets of the Codebase Model itself as held-out — ingestion-aware judges enforce the partition. Same OPA-mediated ABAC default contract as the sketch; specialization: the `partition=train|holdout` tag attaches to *model-derived* scenarios.

- **P-13 Maintenance loop.** Default contract; BF-L runs the cadence on the Codebase Model itself (delta-version ingestion + reconciliation + F34 cross-layer drift detection).

## §4 X_UNM_B articulation

`N/A (mandate-specific candidate; X_UNM_B does not apply)`. BF-L is brownfield-only and **IS the candidate that articulates Codebase Model construction directly** — the X_UNM_B finding names BF-L's Codebase Model as the load-bearing primitive that *other* (unified-attempt) candidates owe an acquisition story for. BF-L itself does not have a Codebase-Model-acquisition gap to articulate; the construction *is* its thesis.

## §5 Open carries

- **Phase-4-internal workstreams (Wave 4.5 ownership).** Four workstreams are owed for BF-L at Wave 4.5:
  1. **BF-L conventional-view smoke-test subagent** — produces [`sub-tracks/bfl-conventional-smoke-test.md`](../sub-tracks/bfl-conventional-smoke-test.md) per the [`auto-003` Round 2 smoke-test recipe](../decisions/auto-003-bfl-rg-view-choice.md#phase-35-follow-up-smoke-test-new-wave-45-pre-lead-agent-coordinated). Consumes [`bfl-conventional-view-prior-art.md`](../research-notes/bfl-conventional-view-prior-art.md) as prior-art frame.
  2. **BF-L invariant-view smoke-test subagent** — produces [`sub-tracks/bfl-invariant-smoke-test.md`](../sub-tracks/bfl-invariant-smoke-test.md). Consumes [`bfl-invariant-view-prior-art.md`](../research-notes/bfl-invariant-view-prior-art.md) as prior-art frame.
  3. **Conditional Wave 4.5b** — if either smoke-test verdict authorizes the full sub-track (≥2/3 languages produce non-trivial artifacts), 1-2 additional subagents scale the recipe from 3-per-language to ≥10-per-language for the qualifying view(s). Wave 4.6 renders the go/no-go.
  4. **Methodology-degradation clause specification (Phase 6 owed; carried from Phase 4)** — when either RG view falls back, BF-L's regime classifier loses the corresponding feature and degrades per the [`auto-003` Round 2 clause](../decisions/auto-003-bfl-rg-view-choice.md#methodology-degradation-clause-new-per-reviewer-2-a2): convention fallback → no-convention regions default to L3 (operator approval) pending re-classification; invariant fallback → derived scenarios are flagged "invariant-unconditioned" and routed to cross-family review.

- **Phase-5 ADR seeds.** (i) **P-26 integrated-view schema ADR** — common ID space, join API call shape, snapshot-consistency / Merkle-DAG versioning choice, eventual-consistency boundaries within an ingestion pass. (ii) **P-27 scenario-derivation calibration ADR** — brief-quality calibration approach (hold-out brief evaluation vs cross-family second-pass diff vs adversarial reviewer); shares structure with BF-M's archaeological-brief calibration. (iii) **P-19 BF-L variant feature-source design ADR** — feature schema, OPA hard floors (Caremark / RSI / debt-cluster), conditional-feature handling when conventional / invariant views are unavailable, drift monitoring of classifier output distribution. (iv) **Per-view ADRs (two)** for the conventional and invariant views — each cites the Wave-4.5 verdict (designed-system promoted vs accept-as-RG fallback) and the Wave-4.4 research notes as alternatives-considered material; status `accepted` or `accepted-with-RG-flag` per the [Phase-3.5.5 rule](../candidate-registry.md#phase-355-rule-on-load-bearing-rg-primitives-binding-user-approved-2026-05-25).

- **Phase-8 lean-eval candidates.** (i) P-26 six-view integration discipline at 1M+LOC, 10+ year history (soft RG on scale per the sketch); (ii) per-region regime classifier drift behavior under the methodology-degradation regime (L3-default's drift; cross-family-review overhead); (iii) maintenance-loop cadence calibration (own OQ-T3 — no corpus anchor for cadence); (iv) Codebase Model integrity / F54 attack-surface pressure-test.

- **F-mode carries.** F25 (design starvation), F40 (last-mile drift), F47 (Goodhart on visible metric) remain accepted-open or partially-addressed per BF-L track §2; no new substrate-layer carry surfaces here.

## §6 Scoping-principle compliance

This summary preserves BF-L as a defensible architecture proposal under explicit acknowledgement that the load-bearing P-26 RG views are **gated on Wave 4.5 smoke-test verdicts**:

- No primitive has been pre-eliminated; all 5 primitive families carry forward, including the load-bearing P-26 with its two RG views.
- The two RG views are **honestly surfaced**, not papered over — the (a)/(b) choice is explicitly the auto-003 Round 2 smoke-test pattern, with the (b) accept-as-RG fallback operationalized via the methodology-degradation clause (rather than left as a fig leaf).
- The candidate's load-bearing claim (three loops over one Codebase Model; methodology parameterized by ingestion fidelity) is preserved in full; the conditional path (full sub-track on smoke-test pass; graceful degradation on failure) means BF-L survives in either branch of the Wave-4.5 verdict, with different methodology consequences but no candidate collapse.
- No same-vs-distinct verdicts are rendered for BF-L's P-19 variant vs other candidates' variants (GF-S work-unit-class variant; U-C distance-gated dispatcher) — those are deferred to Phase 4.2 per the [Round-1 amendment to `auto-001`](../decisions/auto-001-phase-3.5-dispatch-shape.md#amendments-to-the-dispatch-brief-that-will-be-sent-to-subagents).
- The BF-S / BF-M asymmetry (BF-L gets two Wave-4.5 sub-tracks while BF-S accepts B7 as structural and BF-M accepts brief-quality calibration as Phase-5/8) is justified on **load-bearing magnitude** per [`auto-003` Round 2 Reviewer 2 A4](../decisions/auto-003-bfl-rg-view-choice.md#bf-sbf-m-asymmetry-justification-new-per-reviewer-2-a4): P-26 is BF-L's entire thesis, while BF-S's B7 is a measured residual and BF-M's P-27 calibration is one input among many.

BF-L survives Phase-4.1 with the load-bearing RG flag carried honestly into Wave 4.5; the Phase-3.5.5 status (`survives with research-grade-uncertainty flag on Codebase Model`) is confirmed. The scoping principle is preserved: no shrinkage forced at this layer; the conditional path is real on both branches; the honest framing of P-26 as the most ambitious primitive in the catalog is maintained.
