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

## ~~Greenfield → brownfield continuity~~ — WITHDRAWN

This section originally proposed a "greenfield outputs become brownfield inputs" continuity matrix, motivated by a lead-agent misreading of the user's framing.

The user's actual greenfield/brownfield distinction is **entry-mode, not temporal** ([resolved in DEC-1.b](phase-3.4-decisions-resolved.md#dec-1b--greenfield--brownfield-artifact-continuity-na-lead-agent-misread-users-framing)): a greenfield system stays greenfield as long as the same methodology governs it, regardless of age or scale; brownfield is the entry mode where the system arrives as legacy artifacts. There is no GF → BF handoff to design.

Long-run drift concerns against greenfield candidates (F40 last-mile drift; F8 stale-knowledge) are addressed within each greenfield candidate's own methodology (steady-state regime, or whatever within-greenfield regime structure that candidate specifies), not by a cross-mandate continuity deliverable.

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

---

## Phase 3.5.5 candidate re-check (post-buildability)

Phase 3.5 ([sketches in `primitives/`](primitives/)) produced buildability sketches for the de-duplicated primitive union (P-01–P-34). This section annotates each candidate with its post-buildability status. Format per candidate: **primitive coverage** (which P-ids the candidate names + their verdict), **material findings** (shifts in defense status from sketches), **Phase 3.5.5 status** (one of: `survives`, `survives with deferred-defense flag`, `shrinks`, `self-eliminates`), **forward action** (what the candidate owes at Phase 4 if anything).

### Headline outcomes (all 10 candidates)

| Candidate | Status | Forward action at Phase 4 |
|---|---|---|
| GF-S | **survives** with one Phase-8 lean-eval flag (contradiction-detector reliability) | Carry P-15 contradiction-detector reliability as lean-eval input |
| GF-M | **survives** | Carry P-21 calibration as Phase-8 lean-eval input (OQ-T6 confirmed) |
| GF-C | **survives** with two partial-RG flags (P-17 substance-check on 2 fields) | Articulate Phase-4 plan for `business_outcomes` and `capability_scope` substance gating |
| BF-S | **survives with downgraded B7 claim** (P-23 partition-leakage is structural) | Rephrase B7 from "substrate-enforced role partition" to "rate-limited side-channel mitigation"; surface remaining leakage as accepted-open |
| BF-M | **survives** | Brief-quality calibration (P-27) carried to Phase 5/8 |
| BF-L | **survives with research-grade-uncertainty flag on Codebase Model** (P-26: 2 of 6 views are RG; 9–18 engineer-months realistic) | Articulate Phase-4 plan for the conventional + invariant views or accept them as research-grade |
| U-A | **survives** | Same-vs-distinct verdicts on P-28/P-29/P-30 variants are Phase-4.2 work |
| U-B | **conditional survival** (P-31 unbuildable without invariant authoring) | **MUST commit at Phase 4 to authoring ≥3 machine-checkable invariants per layer-pair with corpus citations**, OR self-eliminate at Phase 4 entry |
| U-C | **survives** with partial-RG on distance-estimator calibration + Goodhart-resistance | Calibration recipe + Goodhart-resistance evidence owed at Phase 5/8 |
| D7-U-1 | **survives with research-grade-uncertainty flag on independence auditor** (P-34 OQ-1 auditor-recursion has no dominating option) | Carry A+C hybrid audit-recursion option as Phase-5 ADR + accepted-open structural concern |

**No candidate self-eliminates at Phase 3.5.** U-B has a conditional survival that converts to self-elimination at Phase 4 entry if the candidate cannot commit to the invariant-authoring sub-track.

### Per-candidate detail

#### GF-S — Greenfield, substrate-first

**Primitive coverage** (with verdicts):
- S1=P-01 commodity; S2=P-08 designed-system + P-09 commodity; S3=P-05 commodity; S4=P-02 commodity; S5=P-06 commodity; S6=P-14 designed-system; S7=P-10 commodity; S8=P-15 designed-system (with contradiction-detector RG partial); S9=P-19 designed-system.

**Material findings:**
- S2 (scenario storage) primitive escalated from commodity to designed-system because the holdout-partition discipline (P-08) is load-bearing for F28 — actually *strengthens* GF-S's claim (the substrate-typing of holdout enforcement was the original GF-S thesis).
- S8 four-guard mediator (P-15) contradiction-detector sub-guard's Larbi MCC ≤ 0.55 ceiling is empirically open against F27/F48 shared-pretraining collusion risk; this is Phase-8 lean-eval work.

**Phase 3.5.5 status:** `survives`. F40 (last-mile drift) defense unchanged (still accepted-open). Cost-stacking math still owed; no new claim from buildability sketches changes that.

**Forward action at Phase 4:** carry P-15 contradiction-detector reliability ceiling as Phase-8 lean-eval candidate. No other action required at Phase 4 entry.

#### GF-M — Greenfield, methodology-first

**Primitive coverage:**
- Reversibility=P-20 designed-system; Paraphrase=P-21 designed-system (calibration is RG); Holdout=P-08 designed-system; Tiered watchdog=P-06 commodity; Cost ceiling=P-02 commodity. (Cognitive escrow demoted to methodology per DEC-2.)

**Material findings:**
- P-21 paraphrase divergence calibration confirmed open per GF-M's own OQ-T6; not a buildability blocker, but the primitive must expose N, divergence-metric, and threshold as first-class parameters so Phase-8 sweeps are possible.
- P-20 reversibility cost is sub-ms (negligible); cycle cost dominated by paraphrase fan-out N× multiplier (already GF-M's known cost concern).

**Phase 3.5.5 status:** `survives`. Defense owed (cost-ceiling math + slice-coherence operational definition) unchanged.

**Forward action at Phase 4:** the paraphrase divergence calibration is registered as a Phase-8 lean-eval candidate. Slice-coherence operational definition still owed (not a Phase-3.5 question — Phase-4 / Phase-5 methodology spec).

#### GF-C — Greenfield, cold-start-first

**Primitive coverage:**
- Intent Crucible=P-17 designed-system (with partial RG on 2 of 9 fields); EARS+GtWR=P-16 designed-system (likely absorbs into P-12 framework at Phase 4.2); Cold-Start Bench=P-11 commodity; RSI Ledger=P-18 designed-system (mitigates F43/F53). (Cognitive escrow demoted per DEC-2.)

**Material findings:**
- P-17 Intent Crucible substance-check on `business_outcomes` and `capability_scope` is research-grade — measurability + plausible-attribution + boundedness are not deterministically checkable. The structural validator is bounded designed-system work; substance gating is open.
- This *partly addresses* GF-C's OQ-6 operator-intent-illiteracy: the substrate cannot deterministically gate substance, so GF-C's pre-mortem 18-month "thin-intent → click-through-STIR → F40" cascade requires a methodology-layer answer (likely Council interrogation depth), not a substrate answer.

**Phase 3.5.5 status:** `survives` with two partial-RG flags. The flags do NOT invalidate the candidate — they sharpen what GF-C's Phase-4 methodology spec must answer.

**Forward action at Phase 4:** GF-C must articulate how the Council interrogation handles substance-uncheckable fields (Council depth requirement; named operator-intent-richness criteria). This is Phase-4 methodology work, not Phase-3.5 substrate work.

#### BF-S — Brownfield, substrate-first

**Primitive coverage:**
- S-1=P-22 designed-system (polyglot fidelity risk on cross-language types); S-2=P-23 designed-system (**partition-leakage structural**); S-3=P-07 designed-system (per-role ABAC filter); S-4=P-24 designed-system (P-22 dependency); S-5=P-25 designed-system (CaMeL utility-tax calibration partial-RG).

**Material findings (load-bearing):**
- **P-23 partition-leakage is STRUCTURAL.** Transitive closure of a connected graph leaks hidden-node information by count, edge-type, and path-length. The BF-S B7 ROBUST claim "role-partitioning of in-codebase reads" was contested in Phase 3.2 red-team; the buildability sketch confirms the contestation. Leakage is mitigable to a rate-limited side channel via role-visibility predicates joined into closure rules — but not eliminable.
- BF-S's other red-team finding (Stripe-scale 1300 PRs/week self-reference accretion) is not directly addressed by sketches — remains accepted-open per the original entry.

**Phase 3.5.5 status:** `survives with downgraded B7 claim`. BF-S does NOT self-eliminate — the B7 partition-leakage degradation is to a known-magnitude residual side channel, not a defeat of the substrate-first framing.

**Forward action at Phase 4:** BF-S's Phase-4 substrate-requirements summary must:
1. Rephrase B7 from "substrate-enforced role partition" to "rate-limited side-channel mitigation; residual leakage tracked and audited."
2. Surface the residual leakage rate as accepted-open and as a Phase-8 lean-eval candidate (how much can an adversary exfiltrate via the side channel under realistic adversarial-budget constraints?).

#### BF-M — Brownfield, methodology-first

**Primitive coverage:**
- Code-traversal=P-22 designed-system; Telemetry=P-07 designed-system; Trajectory=P-05 commodity; Sandbox=P-01 commodity; Worktree=P-03 commodity; Cost ceiling=P-02 commodity; Watchdog=P-06 commodity; Cross-family=P-14 designed-system; Det-linters=P-12 commodity; Held-out runner=P-09 commodity (possible Phase-4.2 collapse into P-08); Scenario extractor=P-27 designed-system (with partial RG on brief-quality calibration); CaMeL=P-25 designed-system (partial RG on utility-tax); PR creator=P-04 commodity.

**Material findings:**
- P-27 archaeological-brief tooling brief-quality calibration is the load-bearing open problem (three plausible approaches sketched, none empirically validated). Doesn't block construction; gates Phase-5/8 acceptance.
- P-25 CaMeL utility-tax not measurable a-priori — substrate must expose per-class bypass with audit-log. Affects BF-M's OQ-T3 (CaMeL utility-tax acceptance criterion not set) — the buildability sketch confirms the acceptance criterion has to be deferred to per-deployment measurement.

**Phase 3.5.5 status:** `survives`. Other open questions (stage-compression specification + judge-shape policy + scenarios-from-codebase governance) unchanged — those are methodology questions, not substrate.

**Forward action at Phase 4:** BF-M's stage-compression rules per work-unit-class need specification (own OQ-T1). Brief-quality calibration registered as Phase-5/8 candidate.

#### BF-L — Brownfield, legacy-ingestion-first

**Primitive coverage:**
- Codebase Model=P-26 **research-grade-uncertainty** (2 of 6 views are RG: conventional + invariant; 4 are designed-system); Ingestion engine + Model-query interface = P-26 sub-components; Scenario-derivation=P-27 designed-system; Regime classifier=P-19 designed-system; Held-out partition=P-08 designed-system; Maintenance loop=P-13 commodity.

**Material findings (load-bearing):**
- **P-26 Codebase Model is research-grade-uncertainty overall.** Structural view (Glean + SCIP + tree-sitter) and historical view (P-24 + cosign) and runtime view (P-07 + OPA) and debt view (CodeScene + SonarQube) are designed-system with named tools and integration sentences. Conventional view (LLM + golden corpus; no industry standard) and invariant view (Daikon + CodeQL + LLM, no production-grade polyglot integration) are research-grade.
- **9–18 engineer-months realistic** for full Codebase Model construction. Per-view phased delivery is plausible: ship structural + historical + debt first (highest-value, lowest-risk), then runtime, then conventional / invariant as RG R&D.
- **P-26 sketch's lead-agent recommendation: BF-L survives Phase 3.5 with honest RG flag carried into Phase 4. Do NOT self-eliminate. Phase 3.5.5 should not force shrinkage — the methodology-vs-BF-S/BF-M comparison is Phase 4 work.**

**Phase 3.5.5 status:** `survives with research-grade-uncertainty flag on Codebase Model`.

**Forward action at Phase 4:** BF-L must articulate the Phase-4 plan for the two RG views. Two acceptable shapes:
1. Phased delivery — ship 4 of 6 views first; treat conventional + invariant as Phase-2 R&D with explicit acceptance criteria for when those views are "good enough."
2. Substrate-only acceptance — the Codebase Model carries 4 of 6 views indefinitely; methodology gates that depend on conventional + invariant either degrade gracefully or are deferred until the views mature.

The X_UNM_B cross-mandate finding (CodebaseModel is the load-bearing brownfield primitive for unified-attempt candidates' brownfield-fit) interacts with this: U-A, U-B, U-C, D7-U-1 that claim brownfield-fit must address how they acquire the Codebase Model (or equivalent) — they cannot assume it exists.

#### U-A — Escrow-Graph Factory

**Primitive coverage:**
- Typed-object store=P-28 designed-system (4 variants, same-vs-distinct deferred); Policy mediator=P-29 designed-system (2 variants, same-vs-distinct deferred); Classifier=P-19 designed-system (3 variants, same-vs-distinct deferred); Judge router=P-14 designed-system; Re-entry registrar=P-30 designed-system (2 variants, same-vs-distinct deferred).

**Material findings:**
- All primitives buildable. The dominant Phase-4.2 work is the same-vs-distinct calls on P-28/P-29/P-30 — particularly U-A's typed-object store vs U-B's layer-typed store vs U-C's anchor store vs D7-U-1's FC store, each of which gets its own envelope schema in the sketches.
- DPU-1 granularity concern (process-state node, many per cycle — highest substrate cost at year-2 scale) is not addressed by sketches; remains accepted-open as a Phase-8 lean-eval candidate.

**Phase 3.5.5 status:** `survives`.

**Forward action at Phase 4:** if U-A claims brownfield-fit, must articulate how it acquires the CodebaseModel-equivalent from legacy artifacts (X_UNM_B finding). Granularity-cost trade-off remains Phase-8 lean-eval candidate.

#### U-B — Pace-Layered Escrow Factory

**Primitive coverage:**
- Layer-typed store=P-28 designed-system (per-layer variant); Transition gates=P-29 designed-system (variant); **Cross-layer drift detector=P-31 research-grade-uncertainty**; Per-layer judge=P-14 designed-system.

**Material findings (load-bearing):**
- **P-31 cross-layer drift detector is unbuildable at Phase 3.5.** Brier's pace-layer framework is descriptive, not algorithmic; no source in the corpus authors per-layer-pair invariants. Substrate scaffolding (typed-object snapshots + OPA graph-walk + LLM-judge dispatch via P-14) is commodity engineering, but the contract — flag cross-layer drift — cannot be honored without an invariant catalog.
- **U-B must commit at Phase 4 to an invariant-authoring sub-track delivering ≥3 machine-checkable invariants per layer-pair with corpus citations, OR self-eliminate at Phase 4 entry.**

**Phase 3.5.5 status:** `conditional survival`. Adjudicated at Phase 4 entry: invariant-authoring commitment converts conditional survival to `survives with deferred-defense flag`; refusal converts to `self-eliminates`.

**Forward action at Phase 4:** see above. Lead-agent recommendation: the invariant-authoring sub-track is a substantive Phase-4 work item but is plausibly executable (the 5 layer-pairs × ≥3 invariants = 15 invariants is bounded; the corpus has fragments — GtWR, EARS, AILCCP — that point at intra-layer invariants but not cross-layer ones). Defer the adjudication to user review at Phase 3.5.5 close.

#### U-C — Anchor-Distance Factory

**Primitive coverage:**
- Anchor object=P-28 designed-system (variant: typed with `frozen-since`+`mutation-protocol`); Distance estimator=P-32 designed-system (construction) + research-grade-uncertainty (calibration + partial Goodhart resistance); Distance-gated dispatcher=P-19 designed-system (variant); Anchor mutation queue=P-28 (write surface); Distance-keyed trajectory=P-05 commodity.

**Material findings:**
- P-32 distance estimator construction is solid (Glean/CodeQL/Stack-Graphs BFS over P-23 for graph_distance; deterministic decision table for pace_layer_crossings; P-22 + LLM judge for intent_field_touches). Calibration is open — no corpus recipe maps tuple components or weights to operator-meaningful risk.
- 2 of 3 distance components are structurally Goodhart-resistant (real cost on graph distance + anchor-edit gating on pace_layer_crossings); third leg (intent_field_touches LLM-judged) is F33/F51-vulnerable with patrol-tier residual detector only. Does **not** close F47.

**Phase 3.5.5 status:** `survives` with partial-RG on calibration + Goodhart-resistance.

**Forward action at Phase 4:** if U-C claims brownfield-fit, must articulate Codebase Model acquisition (X_UNM_B). Calibration recipe + Goodhart-resistance evidence owed at Phase 5/8. F33/F51 residual patrol detector must be specified at Phase 5.

#### D7-U-1 — Falsification-Topology Factory

**Primitive coverage:**
- FC store=P-28 designed-system (variant: FC-typed envelope); Opposing-side router=P-33 designed-system; Compounding gate=P-29 designed-system (variant); **Independence auditor=P-34 research-grade-uncertainty** (structural; construction is designed-system); Survival-window registrar=P-30 designed-system (variant).

**Material findings (load-bearing):**
- **P-34 independence auditor recursion (OQ-1) has no dominating option.** Option A (deterministic-ness is the assurance) has Ashby-deficient variety against novel collusion patterns (F51). Option B (recursive auditor) is infinite regress. Option C (human review at audit cadence) re-introduces F42 cognitive-escrow at the audit layer — the exact substrate-promotion D7-U-1 explicitly declined.
- Recommended A+C hybrid (deterministic-ness primary + Option C backstop) is best-current but not closure.
- P-33 opposing-side router shares substantial substrate with P-14 judge router; same-vs-distinct deferred to Phase 4.2.

**Phase 3.5.5 status:** `survives with research-grade-uncertainty flag on independence auditor`.

**Forward action at Phase 4:** carry A+C hybrid audit-recursion option as a Phase-5 ADR with explicit accepted-open structural concern. If D7-U-1 claims brownfield-fit, must articulate Codebase Model acquisition (X_UNM_B). FC-graph cost at high parallelism (own OQ-2) remains Phase-8 lean-eval candidate.

### Phase 3.5.5 close

- Phase 3.5 close criterion (per [`phase-3.4-decisions-resolved.md` refined two-part rule](phase-3.4-decisions-resolved.md#refined-two-part-rule-for-accepting-a-substrate-primitive)): each primitive named by a surviving candidate has a buildability sketch or carries an explicit research-grade-uncertainty flag.
- Coverage: 34 enumerated primitive IDs (P-01–P-34), 32 distinct after expected Phase-4.2 collapses, all sketched.
- Candidates self-eliminating at Phase 3.5: **none**.
- Candidates with conditional survival: **1** (U-B — invariant-authoring commitment adjudicated at Phase 4 entry).
- Candidates carrying research-grade-uncertainty flags into Phase 4: **3** (BF-L Codebase Model; U-B drift detector; D7-U-1 independence auditor).
- Candidates with partial-RG flags on specific sub-components or calibration: **5** (GF-S contradiction-detector reliability; GF-C 2-field substance-check; BF-M brief-quality calibration; U-C distance-estimator calibration + Goodhart-resistance; D7-U-1 already counted).

**All 10 candidates carry forward into Phase 4.** Phase 4 dispatches per-candidate substrate-requirements summaries + shared-discipline extraction + primitive-overlap analysis per the v1.2 plan revision.
