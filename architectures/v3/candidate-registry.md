# Methodology candidate registry — v3 catalog (as of Phase 3.4 close)

This file is the next-session reference for the methodology candidates carried forward per [`phase-3.4-decisions-resolved.md`](phase-3.4-decisions-resolved.md). Ten candidates total: 3 greenfield-mandate, 3 brownfield-mandate, 4 unified-mandate-attempt. Each entry: source track file, mandate scope, axis declaration, substrate primitives the methodology requires, methodology shape, open critique findings (Phase-3.2 / Phase-3.3 / blind-axis), defense status, buildability sketches owed for Phase 3.5.

**Carry-forward criterion** (recap from handoff): a candidate is carried forward when (i) each Phase-3.2/3.3 critique finding against it is either addressed in its track/draft or noted as an accepted open concern; (ii) each substrate primitive it requires has a Phase-3.5 buildability sketch or is a placeholder pending one; (iii) its load-bearing claims are corpus-grounded. Candidates with open items (i) or missing (ii) carry forward as *placeholders pending defense* — preserved in this registry but cannot proceed to Phase 5/6 until the defense lands.

**Effect of DEC-2 on cross-cutting**: in every candidate that listed cognitive-escrow as a substrate primitive, that primitive now drops to a methodology pattern. The candidate may still describe operator-attention-surface design as part of its methodology; the substrate just doesn't carry a typed `EscrowSurface` slot.

---

## Greenfield candidates

### GF-S — Greenfield, substrate-first

- **Source.** [`tracks/greenfield-substrate-first.md`](tracks/greenfield-substrate-first.md)
- **Axis.** Substrate is the primary organizing principle; methodology is deliberately thin and follows the primitives.
- **Substrate primitives required.** S1 sandbox (deny-all default); S2 scenario storage (out-of-tree, holdout-enforced); S3 trajectory capture; S4 cost ceilings (hard, multi-axis); S5 watchdog tiers (Daemon/Triage/Patrol); S6 judge routing (multi-shape typed); S7 coordination medium (CI-friendly content-addressed); S8 guard mediator (4 deterministic guards: GtWR lint + contradiction-detector + req-count budgeter + perimeter typing); S9 eligibility classifier (regime-naming substrate primitive).
- **Methodology shape.** Deliberately thin. 8-step per-cycle process that drives the primitives. Unit-of-work, spec format, agent topology explicitly deferred to methodology choices on top of substrate.
- **Open critique findings.** F40 (last-mile drift) explicitly unaddressed; CFO flagged compounding-guards cost; anchor-detector flagged the option-(c)+(b) regime-classification convergence as brief-anchored.
- **Defense status.** Carries forward; defense owed on F40 (accepted as open) and cost-stacking math.
- **Buildability owed for Phase 3.5.** S6 (judge routing with typed sub-shapes — prior art: cross-family routers in OpenHands V1 and Codex); S8 (4-guard composition — GtWR lint is deterministic INCOSE R7-R35; contradiction-detector requires multi-model judge ensemble); S9 (eligibility classifier — feature-source plug-ins; whether the classifier is itself an LLM judge is open).

### GF-M — Greenfield, methodology-first

- **Source.** [`tracks/greenfield-methodology-first.md`](tracks/greenfield-methodology-first.md)
- **Axis.** Methodology (per-cycle process) is primary. The cycle shape determines what state has to persist; substrate is downstream derivation.
- **Substrate primitives required.** Reversibility primitive (cheap commit-and-reverse on intent artifacts; needs event-sourced storage); paraphrase divergence primitive (N model-family-diverse paraphrasers callable in parallel); holdout enforcement (substrate-partitioned, not agent-discipline); tiered watchdog; cost ceiling (with Regime-A paraphrase fan-out as known multiplier); cognitive-escrow surface (now methodology-layer per DEC-2).
- **Methodology shape.** Two regimes. Regime A (spec-discovery, L3-Augmentation): unit-of-work is a reversible commitment; cycle = intent draft → paraphrase divergence → tiny probe → promote-or-reverse. Regime B (spec-anchored execution, L4): unit-of-work is a scenario from the durable set; Compound-style cycle with cross-model panel. Slice-coherence transition A→B.
- **Open critique findings.** Paraphrase fan-out × cost-ceiling interaction (CFO; GF-M's own OQ-T2); slice-coherence operationally underdefined (own OQ-T1); paraphrase-divergence MCC ceiling vs. F37 untested (own OQ-T6 — Phase-8 lean-eval candidate).
- **Defense status.** Carries forward; defense owed on cost-ceiling math + slice-coherence operational definition.
- **Buildability owed for Phase 3.5.** Reversibility primitive (event-sourced versioning of intent/scenario artifacts — prior art: OpenHands V1's sub-ms per-event persist; D-7 default); paraphrase divergence primitive (multi-provider parallel calls — prior art: Anthropic + OpenAI + Google API parallel dispatch, with deterministic prompt-paraphrase generators).

### GF-C — Greenfield, cold-start-first

- **Source.** [`tracks/greenfield-cold-start-first.md`](tracks/greenfield-cold-start-first.md)
- **Axis.** Cold-start (day-0 bootstrap) is the primary organizing principle.
- **Substrate primitives required.** Intent Crucible (9-field typed-object intake with deterministic validator); EARS-mandated Acceptance Criteria + GtWR linter; Cold-Start Bench (signed scenario store, HMAC-signed); Cognitive-Escrow-Aware Operator Surface (now methodology-layer per DEC-2); RSI-Declaration Ledger.
- **Methodology shape.** Three sub-phases (Intent ingestion with Council interrogation → Bench construction → First-cycle restraint). Graduation protocol with four explicit criteria transitions per-work-unit-class from Cold-Start Regime to Steady-State Regime.
- **Open critique findings.** Operator-intent-illiteracy as biggest unresolved exposure (own OQ-6); regulator critique is positive but flags Hughes-trappings risk on AILCCP three-controls *running* vs. *being scaffolded*; pre-mortem walked through 18-month thin-intent → click-through-STIR → F40 failure cascade.
- **Defense status.** Carries forward; defense centrally owed on operator-intent-illiteracy (can the substrate scaffold operator intent richness, or is this an irreducible operator-skill requirement?).
- **Buildability owed for Phase 3.5.** Intent Crucible validator (9-field typed-object schema with structural validators — prior art: El Kaim Chapter 8 typed-object examples); EARS+GtWR linter (deterministic R7-R35 rule engine — prior art: INCOSE GtWR is publicly specified; ARCAS / Doors); Cold-Start Bench (HMAC-signed scenario store — basic crypto infra).

---

## Brownfield candidates

### BF-S — Brownfield, substrate-first

- **Source.** [`tracks/brownfield-substrate-first.md`](tracks/brownfield-substrate-first.md)
- **Axis.** Substrate is primary. The pre-existing implementation is the primary input; the codebase-reading-and-maintenance primitives are the load-bearing investment.
- **Substrate primitives required.** S-1 codebase index (incremental, queryable); S-2 dependency-and-impact graph (per-symbol blast-radius compute); S-3 runtime/telemetry ingestor (role-partitioned reads); S-4 change-history/attribution store (append-only, signed); S-5 perimeter/trifecta-closure layer (CaMeL-class typed boundary).
- **Methodology shape.** Thin overlay: work-unit selection, per-cycle composition of substrate queries, per-cycle V&V, knowledge promotion.
- **Open critique findings.** Red-team: role-partitioning of in-codebase reads leaks via S-2 dependency edges (B7 ROBUST claim contested). Pre-mortem: BF-S fails first at Stripe scale (1300 PRs/week) due to self-reference accretion (the substrate refreshes from the factory's own output). On-call: polyglot S-2 fidelity uneven; telemetry endpoint can silently drift.
- **Defense status.** Carries forward; defense owed on partition-leakage mechanism + scale-dependent failure mode.
- **Buildability owed for Phase 3.5.** S-1 (polyglot codebase index — prior art: tree-sitter for parsing, Glean / Kythe / Sourcegraph code intelligence for indexed-data store, LSP servers for per-language type info); S-2 (dependency-and-impact graph — prior art: Glean schema, Stack Graphs, GitHub's stack-graphs); S-3 (telemetry with per-role read filters — prior art: OpenTelemetry collectors with attribute-based access control); S-4 (per-symbol attribution — prior art: git plumbing + git blame at granularity, GitHub's REST commit API).

### BF-M — Brownfield, methodology-first

- **Source.** [`tracks/brownfield-methodology-first.md`](tracks/brownfield-methodology-first.md)
- **Axis.** Methodology cycle is the architecture. Substrate is downstream.
- **Substrate primitives required.** Code-traversal tools; runtime-telemetry read; trajectory capture (D-7); sandbox; worktree isolation (F17); cost ceiling (D-5); tiered watchdog (D-6); cross-family routing for reviewer (F46); deterministic linters (F38); held-out scenario runner; codebase-derived scenario extractor; CaMeL-class boundary when production-adjacent; PR creator.
- **Methodology shape.** 8-stage per-cycle contract: Trigger → Comprehension → Intent capture (change-intent block, not system-intent) → Plan (N candidate plans) → Build → Cross-model review → Acceptance (held-out scenarios from codebase) → Ship-or-escalate. Stages compress/expand per work-unit-class.
- **Open critique findings.** Stage-compression rules per work-unit-class are sketched not specified (own OQ-T1); cross-model review necessity under Anthropic same-model-fine finding is unresolved (own OQ-T2); CaMeL utility-tax acceptance criterion not set (own OQ-T3); scenarios-from-codebase governance unspecified (own OQ-T4).
- **Defense status.** Carries forward; defense owed on stage-compression specification + judge-shape policy + CaMeL acceptance criterion.
- **Buildability owed for Phase 3.5.** Archaeological-brief generation tooling (LLM-driven codebase summarization with structured outputs); cross-family-routing infrastructure (multi-provider abstraction); CaMeL-class typed-interpreter (prior art: CaMeL paper itself + AgentDojo benchmarks).

### BF-L — Brownfield, legacy-ingestion-first

- **Source.** [`tracks/brownfield-legacy-ingestion-first.md`](tracks/brownfield-legacy-ingestion-first.md)
- **Axis.** Code-archaeology is the primary organizing principle. Ingestion fidelity constrains the substrate's primitive set and parameterises the methodology's gates.
- **Substrate primitives required.** **Codebase Model** (durable, versioned, queryable; 6 views — structural / conventional / historical / runtime / invariant / debt); ingestion engine; model-query interface; scenario-derivation primitive; regime classifier (per-region); held-out partition enforcement; maintenance loop.
- **Methodology shape.** Three loops over the Codebase Model. (1) Ingestion (deep, slow, once per codebase + refresh on declared triggers). (2) Work (per-cycle, methodology-shaped, queries the model). (3) Maintenance (continuous, low-cadence; reconciles model with reality). Work-unit-class taxonomy is *derived from the codebase model's profile*.
- **Open critique findings.** Ingestion-as-substrate vs. ingestion-as-methodology (own OQ-T1, Phase-4 question); symmetry with greenfield cold-start unresolved per CTR-G3 (own OQ-T2); model staleness vs. cycle latency tradeoff has no corpus anchor (own OQ-T3); per-region regime fragments governance (own OQ-T4 — F43 board-visibility); codebase model as F54 attack surface (own OQ-T6).
- **Defense status.** Carries forward; defense centrally owed on **Codebase Model buildability** — this is the most ambitious substrate primitive in the entire catalog and the X_UNM_B cross-mandate finding identifies it as the load-bearing brownfield primitive.
- **Buildability owed for Phase 3.5.** Extensive — Codebase Model is six views integrated into one queryable artifact. Prior art to draw on: Meta Glean (Datalog-backed code-knowledge store), Sourcegraph (multi-language code intelligence at scale), GitHub semantic / stack-graphs (cross-language symbol-graph indexer), tree-sitter (universal parser), CodeQL (semantic-database queries), Codescene (technical-debt + code-churn analytics), OpenTelemetry (runtime instrumentation). Each Codebase Model view maps to one or more of these as foundation. Construction effort: substantial — this is a 6-12 engineer-month engineering project, not a Terraform module.

---

## Unified-mandate-attempt candidates (per DEC-1 reframe, these are candidate methodologies; not yet committed as "the unified architecture")

### U-A — Escrow-Graph Factory (cycle = directed graph of typed nodes)

- **Source.** [`tracks/unified-A.md`](tracks/unified-A.md)
- **Axis.** Originally: escrow-interval-as-substrate. **After DEC-2:** the typed-node-graph shape stays as a methodology; the escrow framing demotes to methodology pattern.
- **Substrate primitives required.** Typed-object store (content-addressed, append-only); policy mediator; classifier (now methodology-layer per DEC-3 question); judge router; re-entry registrar.
- **Methodology shape.** Cycle = directed graph of typed nodes. Each node carries: kind / pace-layer / priors / policies / classifier-decision / artefacts. The substrate enforces policies at node boundaries.
- **Open critique findings.** DPU-1 granularity (process-state node, many per cycle — highest substrate cost at year-2 scale); X_UNM_B CodebaseModel gap if applied to brownfield; X_UNM_G graduation criteria not cross-mandate measurable.
- **Defense status.** Carries forward; defense owed on granularity-cost trade-off + cross-mandate-measurability + CodebaseModel gap if used for brownfield.
- **Buildability owed for Phase 3.5.** Typed-object store with content-addressing (prior art: IPFS, Git's object store); policy mediator with declarative gates (prior art: OPA, Cedar); re-entry registrar (substrate-typed event protocol).

### U-B — Pace-Layered Escrow Factory (5-layer artifact stack with bidirectional traversal)

- **Source.** [`tracks/unified-B.md`](tracks/unified-B.md)
- **Axis.** Originally: pace-layer × cognitive-escrow. **After DEC-2:** pace-layer stays; escrow demotes to methodology pattern.
- **Substrate primitives required.** Layer-typed object store (one per pace-layer); transition gates per layer-boundary; cross-layer drift detector; per-layer judge routing.
- **Methodology shape.** Five Brier pace-layers (L0 standards / L1 architecture / L2 spec / L3 plan / L4 code). Greenfield = top-down traversal (seed L0/L1 from priors, descend to L4 code). Brownfield = bottom-up inference (read L4 code, infer upward to L1 architecture). Same architecture, opposite traversal direction.
- **Open critique findings.** Layer-count is empirical not derived (Brier asserts 5; El Kaim implies more; own OQ-PLEF-1); pace-layer model own F52 risk (deterministic structure around stochastic agents — own OQ-PLEF-8); OQ-PLEF-5 (operator engagement with substrate-fired prompts is itself voluntary — now moot per DEC-2).
- **Defense status.** Carries forward; defense owed on layer-count argument + pace-layer's own F52 risk + how-bottom-up-inference-works-mechanically.
- **Buildability owed for Phase 3.5.** Layer-typed object store; cross-layer drift detector with per-layer invariants (Brier's pace-layer framework is a description, not a tool — needs substrate-side detector implementation).

### U-C — Anchor-Distance Factory (every work unit parameterised by graph-distance to a frozen anchor)

- **Source.** [`tracks/unified-C.md`](tracks/unified-C.md)
- **Axis.** Distance-from-frozen-anchor. Every work unit declares an anchor and measures distance to it; dispatcher routes by distance regime.
- **Substrate primitives required.** Anchor object (typed: kind / content / frozen-since / mutation-protocol); Distance estimator (typed multi-component); Distance-gated dispatcher; Anchor mutation queue (separate; always L4 with named-human approval); Distance-keyed trajectory storage.
- **Methodology shape.** Three regimes: near-anchor (lights-out, K=5 ≥90% bar); mid-distance (Augmentation, cross-family judge required); far-anchor or anchor-edit (human-required). Mandate is parameterised by anchor's `kind` content.
- **Open critique findings.** F47 Goodhart on distance estimator (agents game distance scoring — own OQ-1); F33/F51 Ashby-deficiency on probabilistic detection (own OQ-2); F8 stale-knowledge over multi-month cold-start (own OQ-3); does anchor-distance subsume Brier's pace-layers cleanly (own OQ-4); operator-legibility of distance estimator at dispatch time (own OQ-5).
- **Defense status.** Carries forward; defense owed on Goodhart-resistance argument + Ashby-variety on the contradiction-flag + operator-legibility.
- **Buildability owed for Phase 3.5.** Distance estimator (typed multi-component implementation — graph distance on dependency graph + pace-layer crossings + intent-field-touch count; needs the substrate primitives from BF-L's Codebase Model for the dependency-graph component); anchor object store (typed content-addressed store with mutation-protocol enforcement).

### D7-U-1 — Falsification-Topology Factory / FTF (every artifact carries an opposing-side commitment)

- **Source.** [`bias-guards/phase-3/d7-blind-axis/d7-u-1-prohibit-interval-escrow.md`](bias-guards/phase-3/d7-blind-axis/d7-u-1-prohibit-interval-escrow.md)
- **Axis.** Adversarial-falsification topology. Every load-bearing artifact (spec / plan / code-change / eval / ADR / skill / classifier-decision / scaffold) is parameterised by a typed *Falsification Commitment* (FC): which opposing side (model-family-different agent / deterministic checker / named human / population vote) must try to falsify it before it can compound forward. The architecture is the topology of build/break pairs.
- **Substrate primitives required.** FC store (content-addressed, append-only, ledger-style); opposing-side router (Attractor "do-not-unify" discipline); compounding gate (refuses to make artifact available downstream unless declared FC survived); independence auditor (Patrol-tier; monitors FC log for collusion/correlation); survival-window registrar.
- **Methodology shape.** Cycle = artifact creation → FC declaration → opposing-side refutation attempt → survival verdict → compounding gate. Graphs of artifacts each with attached FCs. Greenfield: sparse initial FC catalog, operator-as-opposing-side at day-0. Brownfield: rich initial FC catalog (existing tests, telemetry, type checks already serve as opposing sides).
- **Open critique findings.** Independence-auditor recursion (who audits the auditor? — own OQ-1, the load-bearing concern); FC-graph cost at high parallelism untested (own OQ-2); survival-window calibration corpus-thin (own OQ-3); opposing-side gaming under F47 Goodhart (own OQ-4); operator-as-opposing-side scalability under F42/F53 (own OQ-5 — F42 itself is the candidate's honest acknowledgement that FTF doesn't close it at substrate, now moot per DEC-2 since escrow is methodology anyway).
- **Defense status.** Carries forward; defense owed on auditor-recursion + cost model at industrial scale + Goodhart-resistance.
- **Buildability owed for Phase 3.5.** FC store + schema (content-addressed append-only log with typed envelope); opposing-side router (provider-property-driven routing — needs model-family taxonomy + capability registry); independence auditor (deterministic where possible — anomaly detection on FC log distributions); survival-window registrar (typed event-state-machine).

---

## Greenfield → brownfield continuity (per user's DEC-1 reframe)

User's claim: greenfield efforts eventually turn into maintaining an active codebase; greenfield-built codebases are guaranteed to have certain artifacts that make working with them easier. This table makes the continuity concrete — what each greenfield candidate *produces* that a brownfield candidate can *consume*.

| Greenfield methodology produces… | Brownfield methodology consumes it as… |
|---|---|
| **GF-C Intent Crucible** (9-field typed intent block, operator-authored, versioned) | An *operator-curated spec layer above the codebase* that brownfield's BF-M change-intent block contracts back to. The brownfield factory inherits a richer "what is this system supposed to do" artifact than a codebase-archaeology pass can reconstruct. |
| **GF-C / GF-M / GF-S out-of-tree scenario set** (Kaner-style with EARS criteria) | Becomes the *out-of-tree minority* of the brownfield holdout set, complementing the in-codebase-derived scenarios (tests, traces, incident replays). |
| **GF-C RSI-Declaration Ledger** + AILCCP control instantiation | Carries forward as the brownfield factory's *governance-evidence baseline*. Caremark prong-1 reporting, SB 53 conformance — the deploying entity inherits the day-0 declarations without retroactive reconstruction. |
| **GF-M Regime-B durable intent set** (post-promotion) | Becomes the brownfield factory's *spec layer*. Intent items already paraphrase-divergence-validated and probe-survived — much higher confidence than archaeology-inferred spec. |
| **GF-M cross-model judge agreement history** (per work-unit-class) | Brownfield's TPR/TNR-aligned judge baselines start with this history rather than from scratch. The classifier feature populations are populated. |
| **GF-S S3 trajectory history** (per-event content-addressed) | Brownfield's pre-cycle attribution baseline. F14 forensic reconstruction can reach back across the greenfield→brownfield boundary instead of bottoming out at "pre-factory commit (unattributed)." |
| **GF-S S2 scenario storage** (substrate-typed, builder-blind) | Becomes the *initial population* of the brownfield factory's holdout partition; the partition discipline transfers without re-establishment. |
| **GF-S S9 eligibility-classifier baselines** | Brownfield's classifier inherits feature priors from greenfield's measured K=5 / paraphrase robustness data rather than starting from no measurement. |

The pattern: **greenfield methodologies that produce typed, versioned, queryable artifacts give the brownfield methodology a head start that codebase-archaeology alone cannot produce.** This is the substantive content of the user's continuity claim.

The corollary: greenfield candidates that *don't* produce these artifact types (or produce them in formats brownfield methodologies can't easily consume) lose the continuity benefit. This is a Phase-4 evaluation criterion: greenfield methodologies are stronger candidates if they ship continuity-compatible artifact contracts.

---

## Summary table (one row per candidate)

| ID | Mandate | Axis | Substrate-primitive count | Open critique findings | Buildability scope |
|---|---|---|---|---|---|
| GF-S | greenfield | substrate-first | 9 (S1-S9) | 3 | Medium (S6/S8/S9 are designed systems) |
| GF-M | greenfield | methodology-first | 6 | 3 | Low (most substrate is commodity event-sourcing + multi-provider) |
| GF-C | greenfield | cold-start-first | 5 | 3 | Medium (Intent Crucible validator + GtWR linter are designed) |
| BF-S | brownfield | substrate-first | 5 (S-1 to S-5) | 3 | High (S-1, S-2 are designed knowledge-graph systems) |
| BF-M | brownfield | methodology-first | ~10 small | 4 | Medium (archaeological-brief tooling is the most ambitious) |
| BF-L | brownfield | legacy-ingestion-first | 7 (incl. Codebase Model with 6 views) | 5 | **Highest** (Codebase Model is the most ambitious primitive in the catalog) |
| U-A | unified-attempt | typed-graph-of-nodes | 5 | 3 | Medium (typed-object store + policy mediator) |
| U-B | unified-attempt | pace-layer × bidirectional traversal | 4 | 3 | Medium (layer-typed store + cross-layer detector) |
| U-C | unified-attempt | distance-from-anchor | 5 | 5 | Medium-High (distance estimator is multi-component) |
| D7-U-1 | unified-attempt | adversarial-falsification topology | 5 | 4 | Medium-High (FC store + opposing-side router + independence auditor) |

**Total**: 10 candidate methodologies in the catalog. Roughly 60 substrate primitives across them (with significant overlap — the union after de-duplication is ~25-30). Phase 3.5 needs buildability sketches for the de-duplicated union before Phase 4 dispatches.
