# Sketch- and registry-driven discipline extraction (Phase 4.3, subagent 2)

Substrate-layer half of the Phase-4.3 parallel discipline-extraction fanout (auto-004 option A). Enumerates architecture-level disciplines surfaced by [`primitives/index.md`](../primitives/index.md) annotations, per-primitive sketches in [`primitives/`](../primitives/), the [`candidate-registry.md`](../candidate-registry.md) Phase-3.5.5 section, binding decisions in [`decisions/`](../decisions/), and [`AGENTS.md`](../../../AGENTS.md). Complements (does not merge with) the track-driven subagent's parallel index.

Per [Phase-3.4 working definitions](../phase-3.4-decisions-resolved.md#working-definitions-architecture-substrate-methodology), an **architecture-level discipline** is neither substrate primitive nor methodology choice — it is the rule-of-binding governing how methodology calls into substrate and what invariants hold at primitive boundaries.

Ordering by claim-strength.

---

### Construction-path + corpus-why two-part rule

- **One-line definition.** Every substrate primitive admitted to the catalog must ship (i) a construction path naming concrete tools/libraries with an integration sentence per primitive, and (ii) a corpus citation for *why* the primitive solves a corpus-named problem.
- **Governing principle.** "It is handwaving to just assume something like `CodebaseModel` just exists." Admission requires named buildability evidence AND named motivating need.
- **Surfaces in (with claim strength).**
  - [`phase-3.4-decisions-resolved.md#refined-two-part-rule-for-accepting-a-substrate-primitive`](../phase-3.4-decisions-resolved.md#refined-two-part-rule-for-accepting-a-substrate-primitive) — `binding-rule`.
  - [`auto-001` Round-2 amendments](../decisions/auto-001-phase-3.5-dispatch-shape.md#amendments-to-the-dispatch-brief-that-will-be-sent-to-subagents) — `binding-rule` (sharpens to "named tool + integration sentence + specific corpus problem").
  - Every per-primitive sketch (P-14–P-34) and cluster sketch (C1/C2/C3) is structured by this rule — `explicit-named`.
- **Anchored corpus sources.** Per-primitive: each sketch cites named tools (Glean, OPA, tree-sitter, LiteLLM, Daikon, …) and corpus-why failure modes (F28 holdout, F34 drift, F46 review, F47 Goodhart, F53 voluntary-discipline) per [`failure-modes-v3.md`](../failure-modes-v3.md).
- **Relation to specific primitives.** Universal — every P-NN sketch is an instance. The lead-agent re-check is the enforcement point.
- **Note for the lead-agent merge.** Almost certainly also in tracks. Likely canonical; merge to one.

---

### Phase-3.5.5 RG-primitive rule (bounded-sub-track-or-accept-as-RG)

- **One-line definition.** Any candidate carrying a load-bearing research-grade-uncertainty primitive must choose, per RG-portion, between (a) committing to a bounded authoring sub-track to convert RG content to designed-system, or (b) downgrading the dependent contract to accept-as-RG with substrate documenting the gap and methodology specifying graceful degradation.
- **Governing principle.** Symmetry across candidates; no per-candidate ad-hoc lifelines. Same toolkit (a/b with defaults) governs every RG primitive.
- **Surfaces in (with claim strength).**
  - [`candidate-registry.md#phase-355-rule-on-load-bearing-rg-primitives-binding-user-approved-2026-05-25`](../candidate-registry.md#phase-355-rule-on-load-bearing-rg-primitives-binding-user-approved-2026-05-25) — `binding-rule`.
  - [`auto-002` Round 2](../decisions/auto-002-ub-path.md) (U-B P-31 smoke-test); [`auto-003`](../decisions/auto-003-bfl-rg-view-choice.md) (BF-L per-view); [`P-34`](../primitives/P-34-independence-auditor.md) A+C hybrid (combined a+b); [`P-26`](../primitives/P-26-codebase-model.md); [`P-31`](../primitives/P-31-cross-layer-drift-detector.md) — `explicit-named` applications.
- **Anchored corpus sources.** Procedural rule; applications cite Brier descriptive-not-algorithmic (P-31), Daikon-scale gaps (P-26), F51 Ashby-deficient (P-34).
- **Relation to specific primitives.** P-26 (BF-L), P-31 (U-B), P-32 calibration (U-C), P-34 (D7-U-1); partial-RG on P-15, P-17, P-21, P-25, P-27.
- **Note for the lead-agent merge.** **Substrate-only.** Tracks predate this rule; it governs how the catalog admits buildability-uncertain primitives. Flag for merge as substrate-driven.

---

### Same-vs-distinct verdicts deferred to Phase 4.2

- **One-line definition.** Buildability-sketch subagents are forbidden from declaring whether two candidates' superficially-similar primitives (P-28's four envelope variants; P-29 / P-30 / P-19 variants; P-14↔P-33 overlap; P-08↔P-09 collapse; P-12↔P-16) are "the same." Each variant gets its own contract paragraph; collapse is reserved for the Phase-4.2 lead-agent diff.
- **Governing principle.** Substrate-matching is downstream-methodology work. Premature collapse forecloses cross-candidate variety the scoping principle protects.
- **Surfaces in (with claim strength).**
  - [`primitives/index.md`](../primitives/index.md) "Scope discipline" + "Same-vs-distinct" subsection — `binding-rule`.
  - [`auto-001` Round-2 cluster-subagent constraints](../decisions/auto-001-phase-3.5-dispatch-shape.md#amendments-to-the-dispatch-brief-that-will-be-sent-to-subagents) — `binding-rule`.
  - [`cluster-C1.md`](../primitives/cluster-C1.md) / [`C2`](../primitives/cluster-C2.md) / [`C3`](../primitives/cluster-C3.md) codas; [`P-28` "CRITICAL CONSTRAINT"](../primitives/P-28-typed-object-store.md); [`P-29`](../primitives/P-29-policy-mediator.md); [`P-30`](../primitives/P-30-event-registrar.md); [`P-33`](../primitives/P-33-opposing-side-router.md) — `explicit-named` propagation.
- **Anchored corpus sources.** Procedural; propagated by the [scoping principle](../phase-3.4-decisions-resolved.md#scoping-principle-immutable-overrides-any-conflicting-framing-in-the-integration-brief).
- **Relation to specific primitives.** P-28 (4 variants), P-29 (2), P-30 (2), P-19 (3), P-14↔P-33, P-08↔P-09, P-12↔P-16.
- **Note for the lead-agent merge.** **Substrate-only.** Tracks don't observe this — each names its own primitives without cross-candidate comparison. Phase-3.5-era discipline born of the sketch-dispatch shape.

---

### Real-subagent adversarial review (not inline simulation)

- **One-line definition.** Adversarial review of decision briefs, design proposals, plans, or any lead-agent-authored artifact MUST use real subagent dispatches via the `Agent` tool — inline-simulated reviewers (prose by the lead agent) are forbidden as a substitute.
- **Governing principle.** Inline simulation inherits the author's anchoring; it produces objections the author has already defused. Real subagents catch errors the author cannot see.
- **Surfaces in (with claim strength).**
  - [`AGENTS.md` § Adversarial review MUST be real subagents](../../../AGENTS.md) — `binding-rule`.
  - [`auto-001` Round-1 → Round-2](../decisions/auto-001-phase-3.5-dispatch-shape.md#adversarial-review-round-1-inline-simulated-superseded) — `explicit-named` (inline reviewers converged at lead's chosen option; real reviewers converged on a *different* option C).
  - [`auto-002` Round 1 → 2](../decisions/auto-002-ub-path.md#adversarial-review-round-1--both-reviewers-rejected-option-1-with-specific-evidence) — `explicit-named` (real reviewers caught a P-31-sketch misreading and a ~30× cost understatement).
  - [`auto-003` Round 1 → 2](../decisions/auto-003-bfl-rg-view-choice.md) — `explicit-named`.
- **Anchored corpus sources.** AGENTS.md cites the 2026-05-25 overnight run (auto-001 + auto-002 both shifted under real review).
- **Relation to specific primitives.** Not primitive-bound; governs the **decision-brief loop** that surfaces substrate-design choices. Every `auto-NNN` brief is governed.
- **Note for the lead-agent merge.** Surfaces in tracks via AGENTS.md citation; load-bearing applications are substrate-layer. Likely same discipline as Subagent-1's "adversarial review" entry; merge.

---

### Substrate-enforcement-not-operator-voluntary (deny-by-default at boundaries)

- **One-line definition.** Disciplines the methodology depends on (holdout, cost ceilings, sandbox closure, gates, attribution, signed coordination, capability boundaries) are realized as substrate-enforced typed boundaries — the calling primitive cannot complete the action without the boundary's `allow` verdict.
- **Governing principle.** F53 voluntary-discipline fragility: any gate that depends on an operator or LLM *choosing* to apply it under time pressure will be skipped exactly when it matters.
- **Surfaces in (with claim strength).**
  - [`cluster-C1.md` coda](../primitives/cluster-C1.md) — `explicit-named` verbatim: "deny-by-default at the boundary, substrate-enforced not operator-voluntary (F53 mitigation as cross-primitive invariant)." Binds P-01/02/03/04.
  - [`P-29-policy-mediator.md`](../primitives/P-29-policy-mediator.md) — `explicit-named` contract restatement.
  - [`P-08`](../primitives/cluster-C3.md), [`P-11`](../primitives/cluster-C3.md) (HMAC), [`P-25` CaMeL](../primitives/P-25-camel-perimeter.md), [`P-19` OPA hard-floor](../primitives/P-19-eligibility-regime-classifier.md) — `explicit-named`.
- **Anchored corpus sources.** F53; F56 (guardrail-bypass); F28; F32 (unsigned coordination); F44 (lethal-trifecta); F17 (parallel-shared-dirs).
- **Relation to specific primitives.** P-01–04, P-07, P-08, P-11, P-19, P-25, P-29, P-31. The cross-cutting invariant that makes the substrate worth having.
- **Note for the lead-agent merge.** Surfaces in tracks (every substrate-first track); strongest substrate-side framing in cluster-C1 coda + P-29. Merge candidate.

---

### Per-role read-filter (ABAC partition at the read API, not the filesystem)

- **One-line definition.** When the same data corpus serves both builder and judge roles, partition is enforced at the read API via attribute-based access control keyed on substrate-issued role tokens — never by filesystem convention or builder discipline.
- **Governing principle.** Filesystem partition fails the moment data lives in a connected graph (telemetry stream, dependency graph, codebase index). Substrate must partition reads via policy-engine mediation and surface residual side-channel leakage honestly.
- **Surfaces in (with claim strength).**
  - [`P-07` C2 reclassification](../primitives/cluster-C2.md) commodity → designed-system on the per-role-filter discipline — `explicit-named`.
  - [`P-08` C3 reclassification](../primitives/cluster-C3.md) on the partition discipline as a substrate-enforced role-keyed boundary — `explicit-named`.
  - [`P-23` partition-leakage-is-structural](../primitives/P-23-dependency-impact-graph.md) — `explicit-named` (BF-S B7 ROBUST contested; mitigable to rate-limited side channel, not eliminable).
  - [`P-09`](../primitives/cluster-C3.md) (judge-role token; builder credentials suppressed) — `explicit-named`.
  - [`primitives/index.md` post-sketch annotations](../primitives/index.md#post-sketch-annotations-running) — `binding-rule` (index escalates P-07 + P-08).
- **Anchored corpus sources.** F28 (holdout leakage; greenfield-critical, brownfield-high); F55 (drift); F58 (runtime/design-time split); CTR-B5/CTR-G2; BF-S §S-3 "substrate-enforced holdout discipline (D-4) generalized to telemetry-as-scenario."
- **Relation to specific primitives.** P-07, P-08, P-09, P-23, P-26 runtime view.
- **Note for the lead-agent merge.** Surfaces in BF-S / BF-L tracks; substrate-side **leakage-is-structural-not-eliminable** finding is sketch-side and **substrate-stronger** than track extraction. Flag.

---

### Honest research-grade-uncertainty flagging ("say so explicitly")

- **One-line definition.** When a primitive's contract cannot be honored with corpus-grounded construction today, the sketch must say so explicitly — flag `research-grade-uncertainty`, name the upstream gap, and refuse to manufacture confidence the corpus doesn't support.
- **Governing principle.** A primitive admitted as "designed-system" when its subject matter is unauthored poisons every downstream phase. Substrate-side analogue of the Phase-3.3 "addresses-or-accepts-as-open" discipline.
- **Surfaces in (with claim strength).**
  - [`P-31` RG section](../primitives/P-31-cross-layer-drift-detector.md) — `explicit-named` verbatim: "P-31 is an empty primitive whose construction path is real but whose subject matter is undefined."
  - [`P-26`](../primitives/P-26-codebase-model.md) — `explicit-named` (per-view verdict table rather than primitive-level handwave; 2 RG / 4 designed-system).
  - [`P-34`](../primitives/P-34-independence-auditor.md) — `explicit-named` ("RG at the *structural* level even though implementation is buildable").
  - [`P-31-smoke-test-invariants.md` "Honesty discipline"](../primitives/P-31-smoke-test-invariants.md) verbatim "fabricated invariants without corpus support do not count" — `binding-rule`.
  - Partial-RG flags on P-15 contradiction-detector, P-17 substance-check, P-21 calibration, P-25 utility-tax, P-27 brief-quality, P-32 calibration — `explicit-named`.
- **Anchored corpus sources.** Brier descriptive-not-algorithmic (P-31); no SCIP-equivalent for conventions / no production-grade Daikon-integration (P-26); F51 Ashby-deficient (P-34); F37 Larbi MCC ≤ 0.55 (P-21, P-31 fallback).
- **Relation to specific primitives.** P-26, P-31, P-32, P-34 (full); P-15, P-17, P-21, P-25, P-27 (partial). Necessary precondition for the Phase-3.5.5 RG-primitive rule above.
- **Note for the lead-agent merge.** **Substrate-only or substrate-stronger.** Sketch-side framing (per-view verdicts; refusal to collapse up) is sharper than track equivalents.

---

### Substrate-typed-store / typed-envelope discipline

- **One-line definition.** Cross-cycle coordination artifacts (intents, plans, scenarios, FC commitments, anchors, escrow intervals, audit findings) are written as **typed envelopes** to a content-addressed append-only store; the envelope schema is the contract through which downstream primitives consume the artifact.
- **Governing principle.** Coordination by typed envelope (not by free-text PR body or ad-hoc JSON) is what makes a downstream gate's "refuse unless allow" decision a substrate property rather than operator convention.
- **Surfaces in (with claim strength).**
  - [`P-28-typed-object-store.md`](../primitives/P-28-typed-object-store.md) — `explicit-named` (contract common across 4 variants; each declares a distinct envelope schema).
  - [`P-10`](../primitives/cluster-C3.md) coordination medium (Git refs + signed commits; F32 mitigation), [`P-11`](../primitives/cluster-C3.md) HMAC, [`P-30`](../primitives/P-30-event-registrar.md), [`P-18`](../primitives/P-18-rsi-declaration-ledger.md) Merkle chain, [`P-24`](../primitives/P-24-attribution-store.md) signed append-only — `explicit-named`.
- **Anchored corpus sources.** F32 (unsigned coordination); F42 (cognitive-escrow); F43/F53/F54/F58 (RSI/voluntary-discipline/goal-subversion/runtime-vs-design-time); El Kaim Ch8 typed-object examples; OpenHands V1 event-sourcing.
- **Relation to specific primitives.** P-05, P-08, P-10, P-11, P-18, P-24, P-28 (4 variants), P-30 (2 variants).
- **Note for the lead-agent merge.** Surfaces in tracks; sketch-side **envelope-schema-as-contract** framing (P-28's 4-variant analysis) is sharper. Merge candidate.

---

### Snapshot-consistency at version boundaries

- **One-line definition.** Versioned substrate artifacts (Codebase Model, pace-layer stack, FC ledger, anchor store) resolve queries against a **pinned snapshot** at cycle dispatch; within a cycle, no mid-cycle changes are visible; the maintenance loop refreshes between cycles and emits drift events at the version boundary.
- **Governing principle.** F34 cross-layer drift defense becomes structural rather than detection-shaped: cycles can't drift against substrate they never see updated. The maintenance loop, not the cycle, owns reconciliation.
- **Surfaces in (with claim strength).**
  - [`P-26` Consistency/Versioning](../primitives/P-26-codebase-model.md) — `explicit-named` verbatim: "per-cycle queries pin a version at dispatch — the cycle does not see mid-cycle changes (F34 defence at the model level)."
  - [`P-13` maintenance loop](../primitives/cluster-C3.md) — `explicit-named` (continuous reconciliation between versions).
  - [`P-31-smoke-test-invariants.md` L3↔L4 closure](../primitives/P-31-smoke-test-invariants.md) — `explicit-named` (closure-depth must be L0-versionable).
  - [`P-28` append-only + supersession-by-back-reference](../primitives/P-28-typed-object-store.md) — `inferable` (version-frame container).
- **Anchored corpus sources.** F34 (brownfield-critical); F8 stale-knowledge; F21 context-exhaustion (versioned artifact is F21 substrate defense); OpenHands V1 event-sourcing.
- **Relation to specific primitives.** P-13, P-20, P-26, P-28, P-31 (requires this discipline to even define "drift").
- **Note for the lead-agent merge.** **Substrate-only or substrate-stronger.** BF-L track frames the three-loops architecture but the snapshot-consistency invariant is sharpest in P-26. Flag.

---

### Graceful-degradation discipline (when RG portions are unavailable)

- **One-line definition.** A methodology that depends on an RG-flagged primitive must specify how it operates when that primitive is unreliable/unavailable — gates degrade to a named less-confident posture, not a silent skip.
- **Governing principle.** The (b) leg of the Phase-3.5.5 RG-primitive rule. Substrate-accepted-RG is admissible only if methodology shows what it does when the RG portion under-delivers.
- **Surfaces in (with claim strength).**
  - [`candidate-registry.md` Phase-3.5.5 (b) clause](../candidate-registry.md#phase-355-rule-on-load-bearing-rg-primitives-binding-user-approved-2026-05-25) — `binding-rule`.
  - [`auto-003`](../decisions/auto-003-bfl-rg-view-choice.md) (BF-L two views promote-or-accept-with-degradation), [`P-26` partial-completion failure modes](../primitives/P-26-codebase-model.md), [`P-31` Construction-C hybrid + reachability-only fallback](../primitives/P-31-cross-layer-drift-detector.md), [`P-34` A+C hybrid](../primitives/P-34-independence-auditor.md) — `explicit-named`.
- **Anchored corpus sources.** F40 last-mile drift; F8; F33/F51 Ashby-deficient probabilistic guards; F37 Larbi MCC ceiling on LLM-judge fallbacks.
- **Relation to specific primitives.** P-26 (per-view phased), P-31 (deterministic-vs-judge), P-32 (calibration-RG with patrol residual), P-34 (A+C), P-15 (3-of-N ensemble lifts single-judge ceiling).
- **Note for the lead-agent merge.** Likely substrate-only as a *named* discipline; tracks specify per-candidate degradation but the cross-cutting "graceful-degradation as substrate-rule companion" framing is sketch-side. Flag.

---

### Cross-family / opposing-side judge diversity

- **One-line definition.** Where substrate calls an LLM judge against an LLM-built artifact, dispatch routing enforces **model-family diversity** (different provider/family from the builder); where adversarial falsification is required, routes to a builder-family-excluded opposing-side handler.
- **Governing principle.** F27 (circularity), F46 (single-model blindspot), F48 (tacit collusion) are addressable only when judge calls are family-diverse by construction, not by operator selection.
- **Surfaces in (with claim strength).**
  - [`P-14-judge-router.md`](../primitives/P-14-judge-router.md) — `explicit-named` (LiteLLM Router + per-role envelopes; resolves CTR-C4).
  - [`P-33-opposing-side-router.md`](../primitives/P-33-opposing-side-router.md) — `explicit-named` ("do-not-unify" via `tags=["exclude:"+builder.family]`).
  - [`P-15` contradiction-detector sub-guard](../primitives/P-15-four-guard-mediator.md) (multi-model ensemble; Larbi MCC ≤ 0.55), [`P-19` LLM-fallback gated by OPA hard-floor](../primitives/P-19-eligibility-regime-classifier.md), [`P-31` Construction-B/C hybrid](../primitives/P-31-cross-layer-drift-detector.md), [`P-21` paraphrase divergence](../primitives/P-21-paraphrase-divergence.md) — `explicit-named`.
- **Anchored corpus sources.** F27, F46, F48, F37 (Larbi MCC), Anthropic same-model-fine finding (BF-M OQ-T2).
- **Relation to specific primitives.** P-14, P-15, P-19, P-21, P-29 judge-diversity slot, P-31, P-33, P-34 (deterministic auditor *as alternative* where F51 Ashby variety matters more than family diversity).
- **Note for the lead-agent merge.** Surfaces strongly in tracks (GF-S S6; BF-M F46; U-A; U-B; D7-U-1). Sketches sharpen the **substrate-routing-not-prompt-discipline** framing. Merge candidate.

---

### Decision-brief rewind-pointer discipline (decisions are reversible)

- **One-line definition.** Each `auto-NNN` brief in [`decisions/`](../decisions/) carries an explicit "rewind point" naming commit(s) whose reversion returns to pre-decision state, plus an "if-user-overrides" section listing alternatives.
- **Governing principle.** Unattended-run decisions are user-reviewable in the morning; rewindability turns "automated decision" from foreclosure into proposal-with-default.
- **Surfaces in (with claim strength).**
  - [`auto-001`](../decisions/auto-001-phase-3.5-dispatch-shape.md), [`auto-002`](../decisions/auto-002-ub-path.md), [`auto-003`](../decisions/auto-003-bfl-rg-view-choice.md) — `explicit-named` (rewind-point header + if-user-overrides section in each).
- **Anchored corpus sources.** Procedural; informed by the scoping principle's "do not eliminate prematurely" framing.
- **Relation to specific primitives.** None; governs the **decision-brief authoring loop**.
- **Note for the lead-agent merge.** **Substrate-only / decision-process-only.** Tracks predate `auto-NNN`. May belong in its own category at merge time.

---

*End of `sketch-registry-extracted-disciplines.md`.*
