---
guard: splitter
phase: 2
based-on-commit: a0d4b67716d5158f7fa559344aa00463b4f5fece
based-on-date: 2026-05-24
---

# Phase-2 Splitter: False-Divergence Audit

## §1 Method

I read all 9 Phase-2 tracks against the v3 framing layer (brief, constraints, decisions, contradictions, failure modes, corpus inventory). For each candidate cluster I asked: do the tracks describe the **same primitive / mechanism / policy** under axis-flavored vocabulary, or do they describe different things that merely sound alike? "Same" means: same behavior, same inputs, same outputs, same position in the cycle, same failure modes defended against. I biased the cut toward unification only where the variants would compose under one name in Phase-3 without losing a load-bearing distinction. Where one variant carries a failure-mode coverage the others lack, I kept it distinct in §3.

Tracks read:
- [greenfield-substrate-first](../../tracks/greenfield-substrate-first.md) (GF-S)
- [greenfield-methodology-first](../../tracks/greenfield-methodology-first.md) (GF-M)
- [greenfield-cold-start-first](../../tracks/greenfield-cold-start-first.md) (GF-C)
- [brownfield-substrate-first](../../tracks/brownfield-substrate-first.md) (BF-S)
- [brownfield-methodology-first](../../tracks/brownfield-methodology-first.md) (BF-M)
- [brownfield-legacy-ingestion-first](../../tracks/brownfield-legacy-ingestion-first.md) (BF-L)
- [unified-A — Escrow-Graph Factory](../../tracks/unified-A.md) (U-A)
- [unified-B — Pace-Layered Escrow Factory](../../tracks/unified-B.md) (U-B)
- [unified-C — Anchor-Distance Factory](../../tracks/unified-C.md) (U-C)

---

## §2 False-divergence clusters

### Cluster 1 — Regime / eligibility classifier (load-bearing; UNIFY)

**Underlying primitive.** A substrate-typed object that, per work-unit (or per interval, per layer, per cycle phase), declares an *automation-eligibility* class drawn from a small ordered set (escalate / augmentation-required / sample-audit / lights-out). It reads context features (anchor distance, blast radius, telemetry density, bench saturation, cycle phase, work-unit-class) and emits a regime tag that the substrate then *enforces* on the per-cycle gates. Its decisions are themselves logged + Patrol-watched for drift (F57).

**Surface names across tracks.**
| Track | Name |
|---|---|
| GF-S | `S9 Eligibility classifier` |
| GF-M | Regime A vs Regime B *operating-mode declaration* |
| GF-C | *Graduation protocol* (Cold-Start → Steady-State) + per-work-unit-class promotion |
| BF-S | substrate's S-2/S-3-driven *per-work-unit-class classification* |
| BF-M | per-(work-unit-class × stage) *bar-clearance matrix* |
| BF-L | *model-driven regime classifier* (codebase-model parameterises) |
| U-A | `classifier` slot on `EscrowInterval` (`automation-eligibility` field) |
| U-B | per-layer regime declaration (L4 at code, L3 at L0–L3 transitions) |
| U-C | `distance-gated dispatcher` (near / mid / far-anchor → lights-out / Augmentation / human) |

**Evidence they're the same.** All nine tracks adopt brief §2.1 option (c)+(b) (regime-classification + lights-out over a defined surface). All nine route work to lights-out vs. augmentation vs. escalate based on per-unit features. All nine treat the classifier itself as auditable (Patrol-watched for F57 design-authority erosion). All nine refuse to classify day-0 or anchor-edit or bootstrap-interval work as lights-out. All nine use the same threshold-source candidate set (Jaymin K=5 / paraphrase + corpus alternatives) as configurable inputs, not architectural commitments.

**Evidence they might NOT be the same.** The *features* differ: U-C's distance tuple is one specific feature set; BF-L's codebase-model coverage/churn/telemetry is another; GF-C's bench-saturation + K=5-baseline-existence is a third. But these are *inputs* to a common primitive, not different primitives — the substrate object that *enforces* the regime is the same shape.

**Phase-3 recommendation.** **UNIFY** under name **`RegimeClassifier`** (or `EligibilityClassifier`), with feature-source as a typed plug-in (`AnchorDistance`, `CodebaseModelMetrics`, `BenchSaturation`, `PaceLayerCrossings`, `WorkUnitClassPriors`). This is the single most load-bearing unification because nine tracks independently invented the same primitive and would otherwise spawn nine ADR variants.

---

### Cluster 2 — Cross-model / cross-family judge (load-bearing; UNIFY with named distinct sub-shapes)

**Underlying primitive.** A substrate-typed judge call where the judging model is from a different model family than the builder (and/or the same model used for a different *role*), invoked at a defined gate to defend against F1 (hallucination loop) / F27 (circularity) / F46 (single-model review blindspot) / F48 (tacit collusion).

**Surface names.**
| Track | Name |
|---|---|
| GF-S | `S6 Judge routing` (typed `judge-diversity` parameter) |
| GF-M | *paraphrase divergence* (Regime A) + *cross-model review panel* (Regime B) |
| GF-C | *Council* + cross-model judge mandatory at first cycles |
| BF-S | cycle step 5 *cross-model judge* (kevin/carl) |
| BF-M | stage-6 *cross-model review* |
| BF-L | model-derived eligibility uses *cross-model independent signal* |
| U-A | `judge router` with `judge-diversity: different-family` policy |
| U-B | per-layer judge-diversity policy (different-family default at L4 stakes-bearing) |
| U-C | distance-gated: near-anchor single-judge permitted, mid-distance cross-model required |

**Evidence they're the same.** All cite the same corpus stack (CJ Hess kevin/carl; report 34 §6.2; Anthropic same-model Auto-Review report 23 §3.5; Husain/Shankar followup/07; CTR-D4/D7/D8). All defend the same F-mode cluster (F1/F27/F46/F48). All position the call at the same place in the cycle (post-build, pre-acceptance). All treat the *which sub-shape* (same-model-different-role vs. different-family) as a per-call policy decision.

**Evidence of genuine sub-shape distinctness worth preserving.** GF-M's *paraphrase divergence at the spec layer* (N paraphrasers cross-check intent, not code) is structurally different from cycle-step-5 builder-output judging: it is a contradiction-detection mechanism at the spec, defending F37 (Larbi MCC ≤ 0.55 → behavioural test). U-A's `judge-diversity` policy is general enough to host both; GF-M's specific *application of cross-model to spec rather than code* should survive as a documented sub-pattern.

**Phase-3 recommendation.** **UNIFY** under **`TypedJudgeCall`** (per GF-S's framing — it already names "type at substrate, decide shape at methodology"), with three documented sub-shapes: (a) same-model-different-role (Anthropic Auto-Review); (b) different-family on builder output (kevin/carl); (c) different-family on spec/intent (GF-M paraphrase divergence). The Phase-3 reconciler should NOT collapse (c) into (b) — they defend different F-modes and run at different positions in the cycle.

---

### Cluster 3 — Frozen / immutable upstream anchor (load-bearing; UNIFY)

**Underlying primitive.** A typed, version-controlled, human-authored object that captures *non-negotiable invariants* upstream of the cycle. The cycle refuses to start without it; the substrate stores it under content-addressed versioning; Patrol guards it as the slow layer against drift; mutation requires an explicit `anchor-edit`-class work unit always at L4.

**Surface names.**
| Track | Name |
|---|---|
| GF-S | *intent block as slow layer* (S2 + S5 Patrol guards it); "the substrate is thick on invariants" |
| GF-M | El Kaim 9-field intent block with `invariants` *as the only stable subfield* |
| GF-C | **Intent Crucible** (9-field typed-object, explicit "spec malleability permitted *downstream of* the Intent Crucible, never upstream") |
| BF-S | *architecture-invariant region* of S-2/S-5 (slow pace-layer) |
| BF-M | change-intent block's `invariants-to-preserve` field |
| BF-L | *codebase model's invariants view* (extracted from tests/types/runtime assertions) |
| U-A | `EscrowInterval{pace-layer: standards \| architecture}` with frozen-by-default policies |
| U-B | L0 Standards layer; "standards never self-modify within a cycle" |
| U-C | **Anchor object** (`kind: intent-invariant \| architecture-rule \| standards-rule`); `frozen-since` + `mutation-protocol` fields |

**Evidence they're the same.** All cite CTR-B6 (El Kaim invariants vs. UC4 spec-malleability) as the load-bearing tension and *resolve it the same way*: invariants are upstream-stable, the spec body around them is fast. All tracks treat this as the failure-mode anchor for F54 (goal subversion), F55 (behavioural drift), F8 (stale-knowledge inversion). All use the same shape (typed object with 9 fields per El Kaim, or a contraction).

**Evidence they might NOT be the same.** BF-L's "invariants extracted from the codebase" are *inferred*, not human-authored; this is a meaningful generation-source difference, but the *resulting object* and its role are identical (the inferred-vs-authored distinction maps to the `provenance` field of the same primitive).

**Phase-3 recommendation.** **UNIFY** under **`FrozenAnchor`** (or **`InvariantBlock`**) with a `provenance` field (`operator-authored` | `inferred-from-codebase` | `inherited-from-standards`). U-C's anchor-object schema is the most general; GF-C's Intent Crucible is the most prescriptive instance. Phase-3 should adopt U-C's typing with GF-C's authoring discipline as the greenfield default.

---

### Cluster 4 — Deterministic spec/intent lint (GtWR/EARS perimeter) (UNIFY)

**Underlying primitive.** A substrate-resident, deterministic (NOT LLM-judge) rule engine that runs on every spec / intent / acceptance-criterion artifact before the build agent sees it, applying INCOSE GtWR R7/R8/R9/R26/R35 + EARS-pattern conformance. Fail-closed: cycle does not start on violation. Defends F38 (vocabulary lint debt) and partially F36 (instruction-following ceiling — by enforcing the requirement-count budgeter).

**Surface names.**
| Track | Name |
|---|---|
| GF-S | `S8 Guard mediator` (4 guards: GtWR lint + contradiction-detector + req-count budgeter + perimeter typing) |
| GF-M | Phase-1 *EARS-constrained acceptance criteria + deterministic GtWR R7/R8/R9 lint* |
| GF-C | **EARS-mandated Acceptance Criteria** primitive (Mavin five-pattern + GtWR linter) |
| BF-S | not explicit at substrate; implied at S-5 perimeter |
| BF-M | stage-3 *deterministic GtWR R7/R8/R9 lint on change-intent block* |
| BF-L | model-extracted invariants + GtWR-derived invariant-extraction discipline |
| U-A | `kind: spec-author` interval policy mandates EARS/GtWR lint (deterministic) |
| U-B | L2 spec layer: "EARS-typed; GtWR-linted (F38); contradiction-check (F37)" |
| U-C | RE/SE-grounded prompt scaffold derived from INCOSE GtWR C1–C15 + EARS |

**Evidence they're the same.** All cite report 25 (EARS / INCOSE GtWR) verbatim as the source. All run the lint at the same cycle position (intake / spec-author boundary). All defend F38. All explicitly mark the linter as *deterministic, not LLM-judge* (F51 Ashby-deficient probabilistic guard avoidance). All fail-closed.

**Phase-3 recommendation.** **UNIFY** under **`DeterministicSpecLinter`** (substrate primitive). This is uncontroversial — the underlying corpus reference (report 25) and the rule set (R7/R8/R9/R26/R35) are identical across tracks. Phase-3 should specify the rule set as a versioned substrate dependency, not a per-architecture choice.

---

### Cluster 5 — Production-scissors / sandbox closure default-off (UNIFY)

**Underlying primitive.** Substrate-default-deny perimeter for production access, mediated by capability profiles declared per-cycle. Implemented as: deny-all sandbox + explicit grant + CaMeL-class typed-interpreter boundary when production-adjacent. Defends F12/F33/F44/F56 (Replit-class).

**Surface names.**
| Track | Name |
|---|---|
| GF-S | `S1 Sandbox` (closure-first; substrate-default-off) + `S8.4` perimeter typing |
| GF-M | §1.3 *substrate-level default-off required for production-scissors* |
| GF-C | *structural production-scissors-off default* (F44) |
| BF-S | `S-5 Perimeter / Trifecta-Closure Layer` |
| BF-M | §1.2 *CaMeL-class typed-interpreter boundaries* + production-scissors default-off |
| BF-L | model's `production-access-surface` view + substrate-enforced production-scissors-off |
| U-A | `sandbox` + `approval-gate` policies on every interval touching production state |
| U-B | F44 substrate-default production-scissors-off enforced at L4 |
| U-C | anchor's `mutation-protocol` field forces production-scissors prohibition; CaMeL closure |

**Evidence they're the same.** All cite report 32 §8.2 R1–R5 (Shapiro hardening) and followup/08 (CaMeL) as the source. All defend the same F-mode cluster. All explicitly contrast substrate-default-off against operator-discipline-default (F53 voluntary-discipline fragility).

**Phase-3 recommendation.** **UNIFY** under **`PerimeterClosure`** primitive with two layers: (a) deny-all sandbox; (b) CaMeL-class typed boundary for production-adjacent activity. All nine tracks already agree this is substrate, not methodology — Phase-3 just needs to name it.

---

### Cluster 6 — Append-only / immutable / signed log with per-cycle attribution (UNIFY)

**Underlying primitive.** Substrate-resident append-only event log with content-addressed events, per-agent/per-model attribution, and HMAC signing where coordination crosses an unsigned boundary (F32). Combines D-7 trajectory capture, F14 forensic reconstruction, F43 RSI board-visibility, F54 goal subversion across cycles. Co-extensive with the AILCCP immutable-logging control.

**Surface names.**
| Track | Name |
|---|---|
| GF-S | `S3 Trajectory capture` (content-addressed) + `S7 typed event log` |
| GF-M | §1.3 *event-sourced storage of intent / scenario versions* |
| GF-C | **RSI-Declaration Ledger** + trajectory capture from cycle 1 |
| BF-S | `S-4 Change-History/Attribution Store` (append-only, signed) |
| BF-M | trajectory pointer attached to PR body; per-cycle metadata |
| BF-L | ingestion trajectories become part of the codebase model |
| U-A | `Interval object store` (content-addressed, append-only) + `log: append-only \| OTEL-export` policy |
| U-B | per-layer event log; "auditability by design" |
| U-C | distance-keyed trajectory storage; D-7 enriched with distance tuple |

**Evidence they're the same.** All cite OpenHands V1 measurement context (report 11 §6, sub-ms persist) as the feasibility anchor. All cite AILCCP three-controls / Caremark prong-1 (report 31 + followup/10) as the governance grounding. All defend the same F-mode set. All place this at the substrate layer, not methodology.

**Phase-3 recommendation.** **UNIFY** under **`AttributedEventLog`** (or keep the D-7 / `TrajectoryStore` naming). This is already a brief default (D-7); the tracks differ only in what *envelope* metadata is attached (interval-object envelope for U-A, distance tuple for U-C, anchor-set for U-C, layer tag for U-B). Phase-3 should specify the metadata schema as extensible.

---

### Cluster 7 — Operator-attention / cognitive-escrow surface (UNIFY)

**Underlying primitive.** A substrate-triggered (not operator-voluntary) structured interaction surface at the prompt→response interval: STIR cascade, success-criterion articulation, reflection question, similar-past surfacing, delegation-level confirmation. Defends F42 (cognitive-escrow negligence) and F53 (voluntary-discipline fragility) at the substrate layer.

**Surface names.**
| Track | Name |
|---|---|
| GF-S | §2.E re-entry protocol; S5 Patrol; "STIR-in-the-interval can be substrate-triggered" |
| GF-M | §1.3 *cognitive-escrow primitive* (substrate surfaces reflection prompts) |
| GF-C | **Cognitive-Escrow-Aware Operator Surface** (STIR-in-the-interval substrate-triggered) |
| BF-S | not explicit; cited via F53 as motivation for substrate-default |
| BF-M | stage-8 PR body bundle as cognitive-escrow surface |
| BF-L | not central |
| U-A | `reflection-trigger: STIR \| success-criterion \| similar-prior-prompt \| delegation-confirm \| none` policy slot on every interval |
| U-B | escrow primitive: reflection question + success-criterion + similar-past + delegation-confirm + STIR cascade |
| U-C | substrate exposes prompt→response interval as designed surface (Schillace Attention Firewall) |

**Evidence they're the same.** All cite report 30 (Kahana cognitive escrow) §3–§4 as the source. All cite F53 as the rationale (substrate-fired vs. operator-voluntary). All cite Schillace Attention Firewall (report 28 §6) and/or AILCCP delegation-level primitives.

**Phase-3 recommendation.** **UNIFY** under **`EscrowSurface`** primitive with the five sub-primitives (reflection, success-criterion, similar-past, delegation-confirm, STIR-cascade) as composable policies. U-A's typed policy slot is the cleanest encoding. The Phase-3 reconciler should note this primitive is *more load-bearing in the unified tracks* (it is foundational in U-A and U-B); in BF-S/BF-L it is implicit. This means the unification will *promote* the primitive to substrate-first status in the merged architecture — that is the correct move per Kahana's F53 argument.

---

### Cluster 8 — Holdout discipline / scenario partition (UNIFY with brownfield-flip noted)

**Underlying primitive.** Substrate-enforced separation between scenarios/acceptance-criteria and the builder agent's input context. The substrate refuses to expose the holdout to the builder. Greenfield holdout lives out-of-tree; brownfield holdout is the *unseen subset* of a codebase-derived pool. D-4 substrate-enforcement is identical; only the holdout *location* differs.

**Surface names.**
| Track | Name |
|---|---|
| GF-S | `S2 Scenario storage` substrate-typed, builder-blind |
| GF-M | §1.3 *holdout enforcement* (sandboxed filesystem partition with substrate-enforced read masking) |
| GF-C | **Cold-Start Bench** + bench-construction agents never share context with builders |
| BF-S | `S-3` partitioned by role (builder agents cannot read holdout telemetry) |
| BF-M | stage-7 *held-out scenario runner*; holdout-as-unseen, not holdout-as-out-of-tree |
| BF-L | held-out partition enforcement within in-model partition |
| U-A | substrate refuses to close `kind: judge` interval if acceptance-criteria handles leaked into upstream builder interval's inputs |
| U-B | per-layer holdout enforcement; L3 plan-layer holdout from L4 builders |
| U-C | distance-gated dispatcher is the substrate-enforced holdout boundary; near-anchor work has acceptance criteria withheld by dispatcher itself |

**Evidence they're the same.** All cite D-4 (substrate-enforced holdout). All defend F28 (holdout leakage). All explicitly invoke F53 to argue substrate-enforced over methodology-discipline.

**Evidence of preserved sub-distinction.** D-2 location-of-scenarios *correctly* splits greenfield/brownfield (the brief flags D-2 fragile for brownfield); the unified tracks resolve by making location a parameter of the same primitive. The *discipline* unifies; the *location* genuinely varies.

**Phase-3 recommendation.** **UNIFY** under **`HoldoutPartition`** primitive (D-4 enforcement). Carry a `location` parameter (`out-of-tree` | `in-codebase-partition` | `mixed`). Document that this primitive does not unify D-2 (location remains a per-mandate / per-architecture decision), only D-4 (discipline).

---

### Cluster 9 — Cold-start / legacy-ingestion / bootstrap-interval (UNIFY-CAREFULLY)

**Underlying primitive.** A distinguished day-0 *phase* that runs before steady-state, with stricter policies (max sandboxing, max human gating, max judge-diversity, no automation-eligibility), and a *graduation event* that transitions per-work-unit-class regimes from escalation-only to lights-out based on measured criteria (bench saturation / K=5 baselines / cross-model agreement / patrol baseline existence).

**Surface names.**
| Track | Name |
|---|---|
| GF-S | §5 cold-start bootstrap protocol + day-0→day-N trajectory (substrate measures transition) |
| GF-M | §5 cold-start: Regime A + slice-coherence-based promotion |
| GF-C | the *whole architecture* (Cold-Start Regime + graduation protocol + micro-cold-start per new work-unit-class) |
| BF-S | §5 *legacy-ingestion* (S-1..S-4 bootstrap; explicitly NOT symmetric to cold-start per CTR-G3) |
| BF-M | §5 N/A — legacy-ingestion folded into stage-2 *Comprehension* cost |
| BF-L | **Loop 1 Ingestion** (deep, slow, once per codebase + refresh) — central architectural primitive |
| U-A | `kind: bootstrap` interval (singular at day-0) with strictest policies |
| U-B | §5 cold-start = "seed L0 and L1 from priors; do not start at L4" |
| U-C | §5 cold-start dispatched cycles are L4 by construction; transition is distance-distribution shift |

**Evidence they're the same (greenfield side).** All greenfield + unified tracks treat day-0 as a distinguished regime with mandatory escalation, all use the same protection set (deterministic perimeter, cross-model mandatory, production-scissors-off, substrate-enforced holdout, RSI-declaration), all gate graduation on measured criteria. The required-reading set (reports 25/26/30/31, followup/10) is identical across all tracks that treat it.

**Evidence they might NOT be the same (greenfield ↔ brownfield split).** CTR-G3 is explicit and *every* brownfield track that addresses this honors it: greenfield cold-start ≠ brownfield legacy-ingestion. The brownfield analogue is a *substrate setup* (one-time, bounded, reads existing artifacts); the greenfield problem is a *methodology problem* (recurring, ill-defined, must create artifacts from priors). These should NOT unify into one phase-shape.

**Phase-3 recommendation.** **PARTIAL UNIFY:** unify the *graduation protocol* primitive (regime transition gated on measured criteria) across all 9 tracks under **`RegimeGraduation`** (a sub-primitive of Cluster 1). Do NOT unify cold-start with legacy-ingestion; preserve the CTR-G3 distinction. The unified tracks (U-A/B/C) can host both as different `bootstrap` interval kinds with different policies but the same graduation primitive.

---

### Cluster 10 — Reversibility / promote-or-reverse / probe (LOCAL but worth flagging)

**Underlying primitive.** A small-blast-radius probe artifact + a promote-or-reverse gate that cheaply discards work to test spec-malleability without committing the system to a path. Defends F40 (last-mile drift), F59 (premature decomposition), F25 (design starvation by *not* spawning busy-work).

**Surface names.**
| Track | Name |
|---|---|
| GF-M | **Regime A** "reversible commitment" + "tiny probe" (Schillace/Klaassen fidelity-1) + promote-or-reverse step 4 |
| GF-C | **Sub-phase C — First-cycle restraint** (single Ubiquitous EARS criterion, single scenario, throwaway probe) |
| U-A | back-edges permitted in interval graph; substrate does not enforce graph-shape frozen-at-bootstrap |
| U-C | first cycles are far-anchor L4-by-construction; "anchors thicken" by promotion |

**Evidence they're the same.** All cite the same Klaassen fidelity-1 / Schillace tiny-probe lineage. All make reversal *cheap by substrate design*. All defend F59.

**Evidence of distinctness.** This is methodology-side, not substrate. The substrate-side requirement (cheap commit-and-reverse on intent artifacts → event-sourced storage) is already in Cluster 6. The promote-or-reverse *cycle pattern* is methodology.

**Phase-3 recommendation.** **DO NOT UNIFY as a substrate primitive.** Document as a recurring *methodology pattern* with the substrate support already named in Cluster 6 (event-sourced storage + content-addressed artifacts make reversal cheap). Name it `ReversibleCommitment` if useful for cross-architecture cataloguing.

---

### Cluster 11 — Codebase index / impact graph / archaeology brief (brownfield-only; UNIFY across brownfield tracks)

**Underlying primitive.** A substrate-resident, incrementally maintained, queryable representation of the existing codebase (symbols, dependencies, call graph, runtime telemetry, history). Per-cycle agents query slices; they do not re-ingest.

**Surface names.**
| Track | Name |
|---|---|
| BF-S | `S-1 Codebase Index` + `S-2 Dependency-and-Impact Graph` + `S-3 Runtime/Telemetry Ingestor` + `S-4 Change-History` |
| BF-M | stage-2 *archaeological brief* (per-cycle output, compressed) |
| BF-L | **Codebase Model** (durable artifact; built by ingestion loop, queried by work loop) |

**Evidence they're the same.** All three brownfield tracks invoke the same primitive (different name, same role). All cite UC4 "analyzing what is there." All defend F21 (context exhaustion) by returning *slices*, not whole codebase. All defend F34 (cross-layer drift) by surfacing blast radius.

**Phase-3 recommendation.** **UNIFY** under **`CodebaseModel`** (BF-L's name is best — it's the most general). BF-S's enumerated S-1..S-4 are the substrate sub-views; BF-M's archaeological brief is the per-cycle *query output* of the model. These compose: model is substrate, brief is methodology-layer query result. The Phase-3 reconciler should specify this layering explicitly.

---

## §3 Genuine divergences worth preserving

Places where the tracks really do differ — Phase-3 should NOT collapse:

1. **Cold-start vs. legacy-ingestion (CTR-G3).** Despite Cluster 9's partial unification, the *core problem shape* is asymmetric: greenfield must *create* anchors from priors with no codebase; brownfield must *read* anchors from an existing codebase. The corpus explicitly flags this in CTR-G3 and *every* brownfield track honors the asymmetry. Phase-3 must preserve two distinct day-0 protocols. **This is the strongest genuine divergence in the set.**

2. **Unit-of-work shape (OQ-B4).** GF-M's "reversible commitment" (no queue, no PR-target), BF-M's typed work-unit-class polymorphism (issue / change-request-against-spec / codebase-evolution-proposal), BF-L's *codebase-model-driven choice*, and U-A's "all three valid graph-shapes" are not the same answer. They differ on whether the unit-of-work shape is operator-fixed, deployment-fixed, model-derived, or per-methodology. Phase-3 should NOT collapse — this is a real architectural choice with downstream consequences for tooling and human-interaction surfaces.

3. **Substrate-vs-methodology boundary placement (OQ-B2).** GF-S/BF-S/U-C put nearly everything in substrate; GF-M/BF-M/U-A put more in methodology; BF-L creates a third position (substrate is *codebase-specific* not generic); U-B splits per layer. These are genuinely different stances and Phase-3 is the place they collide. Unifying primitives (this report's §2) does not resolve the boundary question.

4. **Pace-layer model (U-B's L0–L4) vs. interval-graph (U-A) vs. distance-scalar (U-C).** All three unified tracks reach for a unifying frame, but the *frames* are genuinely different: U-B's is artifact-stack-shaped (layers), U-A's is process-state-shaped (intervals as nodes), U-C's is metric-shaped (distance scalar). These produce different ADRs, different watchdog signals, and different mandate-symmetry arguments. Phase-3 should pick or merge consciously, not by lexical-look-alike.

5. **Methodology evolution disposition (OQ-B9).** GF-S/BF-S put it methodology-side; BF-L makes it partly substrate (codebase-model parameterises methodology); U-A makes it a `kind: methodology-delta` interval; U-B makes it per-architecture. Genuine divergence; corpus does not decide.

6. **Spec-format commitment (CTR-B1).** GF-C mandates EARS+typed-object; GF-M permits prose→EARS→typed-object→DOT churn; U-C is agnostic. These are real disagreements about whether the substrate prescribes a spec format.

7. **Same-model vs. different-family judge default at low stakes (CTR-D7).** U-C explicitly allows single-judge near-anchor; GF-M/GF-C/BF-S/BF-M default to cross-family. This is a real and load-bearing divergence on the F1/F46 axis.

8. **L5 mapping treatment.** Every track touches CTR-A4 (vocabulary mapping test) but they answer differently: GF-S/GF-C/U-A explicitly *reject* L5 mapping; GF-M maps to L4; U-C maps lights-out to "near-anchor automation-eligible." All reach option (c)+(b) per brief §2.1 but the *route* differs and the *bar source* (OQ-B6) differs accordingly. Worth preserving as different defensible reconciliations.

---

## §4 Recommendations to Phase 3

Reconcile in this order (load-bearingness × number of tracks affected):

1. **Cluster 1 (RegimeClassifier).** Affects all 9 tracks; the largest unification dividend. Without this, Phase-5 will produce nine variants of the same ADR. Specify the feature-source plug-in interface so Cluster 9's graduation protocol can fold in as a sub-primitive.

2. **Cluster 3 (FrozenAnchor / InvariantBlock).** Affects all 9 tracks; resolves CTR-B6 at the substrate level (which the corpus already does implicitly). U-C's anchor-object schema is the most general; adopt it with GF-C's Intent-Crucible authoring discipline as the greenfield default and BF-L's inferred-from-codebase as the brownfield default.

3. **Cluster 2 (TypedJudgeCall).** Affects all 9 tracks. Preserve the three sub-shapes (do not collapse paraphrase-divergence into post-build judging). This is the closure on the F1/F27/F46/F48 cluster.

4. **Cluster 6 (AttributedEventLog).** Already a default (D-7); Phase-3 should specify the envelope-metadata schema as extensible (distance tuple, layer tag, interval-kind, anchor-set).

5. **Cluster 7 (EscrowSurface).** Promotes from implicit (BF-S) to substrate-first (U-A/B). This is the load-bearing primitive whose status the merged architecture should *raise*, not lower.

6. **Cluster 4 (DeterministicSpecLinter), Cluster 5 (PerimeterClosure), Cluster 8 (HoldoutPartition).** Uncontested unifications; specify and move on.

7. **Cluster 11 (CodebaseModel).** Brownfield-only; specify before Phase-5 brownfield ADR wave.

8. **Cluster 9 (cold-start vs. legacy-ingestion).** Unify the graduation primitive but explicitly preserve the day-0 protocol split per CTR-G3.

9. **Cluster 10 (ReversibleCommitment).** Document as methodology pattern; no substrate primitive change.

Then attack the *genuine* divergences in §3 — those are the real Phase-3 substantive decisions.

---

## §5 Limits

- **I did not read the Phase-2 tracks against each other's failure-mode coverage tables in full detail.** Some clusters that look unifiable might split if one variant's F-mode coverage list contains a defense the others lack. I sampled but did not exhaustively diff.
- **I did not attempt to verify the corpus citations.** Where two tracks cite the same report-section as the source of "the same primitive," I treated that as evidence of sameness. A track could be citing the same report for a different sub-finding.
- **I did not exercise the anti-anchor discipline (D5) on cluster names.** I propose names (`RegimeClassifier`, `FrozenAnchor`, `EscrowSurface`, etc.) drawn from the most general track usage; Phase-3 may need to rename to avoid inheriting an axis-specific frame.
- **The 9 tracks are individually long and individually defensible; I prioritized "where multiple tracks describe the same thing differently" over "where one track describes something the others omit."** That second cut is the lumper's job (false convergence).
- **I read tracks once.** A second pass would likely find another 1–3 clusters (candidates I noticed but did not develop: *content-addressed shared filesystem coordination medium* across GF-S S7 / U-A interval-object-store / various; *typed work-unit-class declaration* across BF-M stage-1 / U-A classifier / D2 schema; *Patrol-tier cross-cycle drift detection* — though this is already mostly a single D-6 primitive).
- **The Phase-3 reconciler should run an explicit anti-lump pass before adopting these unifications.** The lumper guard exists for exactly the inverse hazard; both reports should sit on the reconciler's desk simultaneously.

*End of splitter.md.*
