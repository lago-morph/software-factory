---
based-on-commit: 5c4deeb
based-on-date: 2026-05-24
position: lumper
---

# Phase-2 lumper argument

**Position.** The 9 Phase-2 tracks have substantially converged on **2 distinct architectures (with a 3rd as a defensible variant)**, not 9. Phase-3 merge should recognize the convergence and produce a small number of merged drafts that absorb the variation as parameterization rather than as architecture. The brief's 9-track fanout was a divergence *search*; the corpus answered with *convergence*. Lumping is the honest reading.

The 9 tracks differ in framing, vocabulary, and which primitive they nominate as "organizing." They do not differ — at the level of load-bearing architectural commitments — nearly as much as 9 distinct framings would suggest. Underneath, the same five or six structural moves keep being reinvented under different names.

---

## Section 1 — The converged architectural cores

### Core 1: **Tier-Gated Shared Substrate** (TGSS)

A mandate-agnostic substrate layer (typed event-sourced trajectory, sandbox with default-off production scissors, deterministic-perimeter judge composer wrapping a probabilistic inner judge, tiered watchdog, holdout-mediator, cognitive-escrow primitive, typed knowledge store with `discovered-from`/provenance edges, cost ceilings) carries a thin methodology overlay whose configuration is **selected per work-unit by a tier/regime classifier** (blast-radius × reversibility × regulatory-exposure, or layer-of-impact, or risk-tier). Regime (L3/L4/L5) is an *output* of the classifier, not a property of the architecture. Lights-out applies to low-tier work; high-tier work runs L4 with substrate-triggered re-entry; L5 is rejected or restricted everywhere by the same mechanism.

- **Tracks that converge on this core:** **7, 9, A (greenfield-substrate-first), B (brownfield-substrate-first), C (greenfield-cold-start-first), D (greenfield-methodology-first), E (brownfield-methodology-first)** — i.e., the two of three unified tracks that are tier-shaped (unified-A, unified-C) plus the 5 mandate-specific tracks that internally adopt either a tier-router (T0–T4 / T0–T3) or an equivalent classification-gate that selects per-cycle methodology. Greenfield-substrate-first's §1.3 explicitly declares "L4 lights-out for sandboxed `initial-spec`/`mvp` work units, L4-augmented for cognitive-escrow triggers" — this *is* a 2-tier router with different vocabulary. Greenfield-methodology-first's §1.5 regime gate (`L3-augmented | L4-lights-out | escalate`) is a 3-tier router. Cold-start-first's §2 layer-split (L4 at spec-authoring, lights-out at implementation) is a 2-tier router by *layer*. Brownfield-methodology-first's Stage 2 CLASSIFICATION GATE forcing `{stakes, RSI-status, regulatory-exposure, blast-radius}` is **literally unified-A's tier-classifier** with different field names.
- **Shared moves:**
  1. **Substrate-heavy + thin-methodology + per-work-unit configuration.** Every one of the seven tracks above adopts the Round-2 CTR-C2 framing despite the brief inviting them to challenge it. Methodology-first tracks claim to invert it, then immediately enumerate a fixed substrate primitive set (`brownfield-methodology-first §6`: typed-object store + rules engine + capability tokens + event-sourced trajectories + worktree isolation + Daemon/Triage/Patrol — *identical* to substrate-first tracks' lists).
  2. **Deterministic outer perimeter + probabilistic inner judge.** Unified-A T2+ tier-overlay (deterministic perimeter + 2 cross-model judges). Unified-C T2 production-touch overlay (CaMeL typed-interpreter + cross-model required). Brownfield-substrate-first §3.2 "Deterministic-perimeter judge composer." Brownfield-methodology-first Stage 6 REVIEW GATE ("deterministic load-bearing + at most one bounded probabilistic, advisory-by-default"). Greenfield-cold-start-first §3.2 "Ashby-adequate cold-start substrate." Same architectural move, five vocabularies.
  3. **Tier/layer/regime classification is the operating-mode resolver for CTR-A4.** Every track answers OQ-B1 with brief §2.1 option (c)+(b). None picks (a), (d), or (e). Unified-A: 5 tiers. Unified-B: 5 pace layers. Unified-C: 4 tiers. Greenfield-substrate-first: 2 tiers (sandboxed vs escrow-triggered). Greenfield-methodology-first: 3 outcomes. Cold-start-first: layer-split. Brownfield-methodology-first: classification-driven dispatch. Different bin counts, same axis.
  4. **Invariant/body split resolves MISSED-3.** 7 of 9 tracks (the lead agent already noticed 6; brownfield-methodology-first makes 7 via its `intent` field in the proposal object — invariants slow, statement/decisions fast). Substrate-enforces the invariant; methodology layer owns the malleable body. Tracks 1, 2, 3, 7, 8, 9, E.
  5. **Cognitive escrow / substrate-triggered re-engagement as the F53 fix.** Greenfield-substrate-first S8. Greenfield-methodology-first §1.5 + Q-MF4. Cold-start-first P5 + Defense 3. Unified-A primitive 10. Unified-B Sentinel + Patrol-escalation. Unified-C S3. Brownfield-substrate-first §2.9 + §2.12. Brownfield-methodology-first §4.4 ("moving operator action upstream of cycle time"). Same primitive, eight names.
- **Citations (quote-level):**
  - Greenfield-substrate-first §2.4: *"the substrate primitives S1-S8 should be shared across mandates; the methodology overlays diverge."*
  - Unified-A §1.1: *"the same tier-classifier + tier-overlay matrix operates on output from either feed."*
  - Unified-C §0.3 point 2: *"no single methodology overlay works for both, but a single substrate plus a tier-aware overlay-selector does."*
  - Brownfield-substrate-first §0.3 B-2: *"The substrate provides the composer: Deterministic perimeter (substrate-provided)… Probabilistic inner layer (configurable)."*
  - Brownfield-methodology-first Stage 6: *"deterministic load-bearing + at most one bounded probabilistic, advisory-by-default."*
  - Greenfield-cold-start-first §3.2: *"only a deterministic guard has Ashby-adequate variety. As the factory accumulates trajectory data, probabilistic judges become Ashby-adequate for narrower distributions."*
  These five passages from five tracks describe the *same* composer pattern.
- **Where the tracks differ:** Vocabulary (T0–T4 vs L1–L5 vs T0–T3 vs Augmentation/Automation vs L3/L4-lights-out/escalate vs layer-split); specific substrate primitive enumerations (8 vs 9 vs 11 vs 13 vs 7 P-primitives); which CTR is named load-bearing (A4 vs MISSED-3 vs F34 vs F53); whether the organizing axis is *announced* as substrate, methodology, cold-start, ingestion, tier, pace-layer, or stakes. Vocabulary and emphasis. Not architecture.

### Core 2: **Brownfield Existing-System Wedge** (BESW)

A thin specialization of Core 1: the substrate includes a continuously-refreshed legibility layer over the existing codebase (symbol graph, dependency graph, EAI/invariant catalog, archaeology cache, holdout-partitioning over in-tree scenarios, governance-declaration emitter, production-scissors gate) that feeds the same tier-gated cycle Core 1 runs. The methodology cycle is identical to Core 1; the substrate has more primitives because the codebase exists.

- **Tracks that converge on this core:** **Brownfield-substrate-first (the ESS wedge §2.1–§2.11), brownfield-legacy-ingestion-first (the ingestion artifact §2.1–§2.4), brownfield-methodology-first (the §6 substrate dependency table, which silently requires every primitive the other two name), unified-A (`brownfield-feed` adapter), unified-C (Excavation overlay + Holdout Mediator over in-tree signal).**
- **Shared moves:**
  1. **D-2 is challenged identically.** *7 of 9 tracks challenge D-2.* All challenge it the same way: holdout discipline survives, but scenario *location* moves in-tree; the substrate enforces a builder-vs-judge partition over a corpus that may live inside the codebase. Greenfield-substrate-first formally accepts D-2 but adds the same partition substrate. Cold-start-first challenges D-2 to allow bootstrap-borrowed priors with the same partition discipline.
  2. **Codebase-as-ingested-artifact is a substrate primitive.** Brownfield-legacy-ingestion-first names it "ingestion artifact"; brownfield-substrate-first names it "ESS wedge"; unified-A names it `brownfield-feed`; brownfield-methodology-first names it "the `out-of-distribution-anchor` pointing to existing tests/production traces/runtime telemetry." Four names, one primitive.
  3. **F34 + F44 + F30 + F56 are the brownfield-critical cluster every track addresses with the same primitives** (production-scissors-gate-as-substrate-default; EAI inference / pace-layer-pinning; governance-declaration emitter or its equivalent). Brownfield-substrate-first §2.7–§2.9; brownfield-legacy-ingestion-first §3.1 + §2.4; brownfield-methodology-first §2.1+§2.4; unified-A §3 + AILCCP at T4.
- **Citations:**
  - Brownfield-substrate-first §0.3 B-1: *"Brownfield substrate must default to capability-off with explicit typed elevation."*
  - Brownfield-legacy-ingestion-first §3.1 F44: *"ingestion identifies which paths are production scissors; substrate-default-off uses the ingestion artifact to know what 'production' means."*
  - Brownfield-methodology-first §2.4: *"DISPATCH is the substrate's permission-emission point… the agent at BUILD never has more capability than its dispatch token grants."*
  Same primitive. Three tracks. The framing is "substrate-first" vs "ingestion-first" vs "methodology-first" but the design is the same.
- **Where the tracks differ:** Whether the codebase-ingestion layer is named "ESS" or "ingestion artifact" or "brownfield-feed" or "out-of-distribution-anchor." Whether it is one primitive or seven. Whether the methodology layer is described in PROPOSAL→CLASSIFICATION→DISPATCH terms (E) or just "the cycle reads it" (B, F).

### Core 3 (defensible variant, not a separate architecture): **Pace-Layered View**

Unified-B reframes Core 1 with Brier's 5 pace-layers as the regime resolver instead of stakes-tier. The substrate is the same (trajectory, holdout, watchdog, cost ceilings, `.rules` DSL, cross-model judge, CaMeL perimeter, OTEL). The judge architecture is the same (deterministic outer + probabilistic inner). The "Sentinel" judge is literally the Patrol-tier of D-6 applied to a layer-boundary input. Regime-per-layer (§3.2 matrix) maps cleanly to regime-per-tier: Code≈T0–T1, Plans≈T1–T2, Specs≈T2, Architecture≈T3, Standards≈T4. **This is Core 1 with the classifier indexed on artifact pace instead of work-unit risk.** Unified-B's own §0.2 admits: *"substrate-vs-methodology arises naturally as a per-layer question under pace-layering"* and *"convergence expected on substrate primitives, divergence expected on whether F34 is first-class architectural (this track) or absorbed into per-cycle judging (likely A/C)."* The track concedes the substrate convergence in its own report-back.

So Core 3 is real but absorbable: Phase-3 can produce Core 1 with a pace-layer-aware classifier as a parameter choice.

---

## Section 2 — The variation IS parameterization, not architecture

The differences across the 9 tracks are all expressible as parameters of one or two architectures, not as distinct architectures.

- **Tier counts.** Unified-A: T0–T4 (5 tiers). Unified-C: T0–T3 (4 tiers). Unified-B: 5 pace-layers. Greenfield-methodology-first: 3 outcomes (L3/L4/escalate). Greenfield-substrate-first: 2 regimes. Cold-start-first: 2 layers. **Same axis (work-unit-property → regime), different bin counts.** A single architecture can carry a configurable bin count; calling 5 binning choices "5 architectures" inflates the architecture count.

- **Substrate primitive enumerations.** Greenfield-substrate-first: S1–S8 (8). Brownfield-substrate-first: ESS §2.1–§2.11 (11 brownfield-specific + 7 inherited). Greenfield-methodology-first: 13. Cold-start-first: P1–P7 (7). Unified-A: 16. Unified-C: S1–S7 (7). Brownfield-methodology-first: 8-item §6 dependency table. **The overlapping core is: trajectory capture (D-7); sandbox + production-scissors default-off; tiered watchdog (D-6); cost ceilings (D-5); holdout-partitioning (D-4); cross-model judge router or composer; cognitive-escrow / re-engagement primitive; typed knowledge store with provenance edges; tier/regime classifier.** Every track ships this core under different names with different extras. The "extras" are mandate-specific overlays (ESS for brownfield) or implementation choices (Starlark `.rules` vs OPA/Rego). These are parameters of one substrate, not seven substrates.

- **Judge compositions.** "Deterministic perimeter + probabilistic inner" appears under five names: Brownfield-substrate-first §3.2 "deterministic-perimeter judge composer"; Unified-A T2+ tier-overlay; Unified-C T2 production-touch overlay + CaMeL; Brownfield-methodology-first Stage 6 REVIEW GATE composition rule; Greenfield-cold-start-first §3.2 Ashby-adequate. Same composition pattern; the variation is at which "layer" (tier / pace-layer / stage) it engages, which is itself the regime-classifier output.

- **Cold-start treatments.** Greenfield-substrate-first §5: thin methodology, knowledge accumulation off, K=5 ≥90% to graduate. Greenfield-methodology-first §5: L3 default, pattern→standard sift forbidden for N cycles. Cold-start-first §5: bootstrap-borrowed-priors with sunset-edges. Unified-A §5: bootstrap-window with T2 pin. Unified-C §5: Augmentation-mode default. Unified-B §5.1 Cold-Seed. **All five say: cold-start is a regime where probabilistic judges are not yet Ashby-adequate; default-bootstrap into Augmentation; graduate per measured bars; turn on knowledge accumulation only after track-record exists.** Same architecture with different vocabulary.

- **MISSED-3 resolution.** Seven tracks pick the same split: invariant slow, body fast, substrate enforces the invariant, methodology owns the body. Unified-B is the only one that names "pace-layers" but the structural move is identical (Standards = invariants; Specs = body). Unified-A § 2: *"the invariant set grows monotonically… invariants are append-only after T3 entry"* — tier-as-pace-layer.

---

## Section 3 — Why Phase-3 lumping is the right move

1. **D1 was a test. The test came back YES.** D1 dispatched the 3 unified tracks specifically to test whether unified architectures exist. All three return yes/conditional-yes (A: "conditional yes"; B: "unified is possible and the pace-layered shape is genuinely strong for both mandates"; C: "the unified case is possible"). Per D1: *"if 1+ produce defensible unified architectures, the hypothesis is falsified for that architecture's domain of applicability."* **All 3 produced defensible unified architectures.** UC4 is empirically falsified for the shape Core 1 names. The 6 mandate-specific tracks then become *specializations of Core 1 for one mandate*, not standalone architectures.

2. **The corpus convergence is the brief's discovery.** The brief built the 9-track fanout to surface divergence; the brief's discipline ("accuracy >> speed >> tokens") means we report what the corpus actually said, not what we hoped it would say. The corpus said: there is one substrate-heavy + thin-methodology + tier-classified architecture, plus a brownfield specialization that adds an existing-system wedge. Preserving 9 architectures that mostly differ in vocabulary creates false plurality and violates the accuracy discipline.

3. **The Phase-7 back-fill audit becomes tractable.** With 2 architectures (Core 1 + Core 2 specialization), every v1/v2 archive item maps to: a tier-overlay choice, a substrate primitive enumeration, or a methodology-overlay vocabulary. With 9 architectures, the audit surface is 9× larger for no information gain — the same archive item gets classified 9 times under 9 vocabularies.

4. **The mandate-fit matrix (D2) is easier to defend at the cell level with fewer rows.** A 2-row × 5-column matrix (Core 1, Core 2) × work-unit-class is defensible per cell because the tier-distribution per cell is the real explanation. A 9-row matrix would require defending 45 cells most of which are vocabulary differences over the same underlying answer.

5. **Phase 4 (shared/divergent extraction) is *trivially solved* if there are 2 architectures.** Substrate is shared (Core 1's substrate primitives = Core 2's substrate primitives minus the ESS wedge). Divergence is the wedge. This is the cleanest possible outcome of Phase 4 and the corpus has handed it to us.

---

## Section 4 — The splitter's strongest counter, and your rebuttal

The splitter has four serious moves; let me steelman each then rebut.

**Splitter move 1: "Unified-B (pace-layers) is genuinely different from A and C (risk-tier) — the organizing axis is artifact-pace, not work-unit-risk, and that produces a different architecture because the Sentinel is structural to B but absent in A/C."**

*Rebuttal.* Unified-B's Sentinel is described in §3.1 as "a dedicated agent that watches every artifact-mutation event from any layer (events sourced via D-7 trajectory capture) [and] verifies the derivation chain to the nearest upstream invariant" — i.e., the Patrol-tier of D-6 reading trajectory and emitting Patrol escalations to humans. Unified-A's primitive 5 (tiered watchdog) and primitive 11 (`discovered-from` edge knowledge store) compose into the same thing: cross-layer/cross-tier drift detection on the trajectory store, escalated via Patrol. Unified-C §S5 (Patrol watches stakes drift). Brownfield-legacy-ingestion-first §2.4 Patrol-tier ingestion-freshness watchdog. **The Sentinel is the Patrol-tier-of-D-6 applied to a layer-boundary input.** Unified-B's own report-back admits: *"convergence expected on substrate primitives."* The pace-layer view is a *configuration of the classifier*, not a new architecture.

**Splitter move 2: "Cold-start-first is genuinely different because it treats day-0 as architectural; substrate-first and methodology-first treat it as transient."**

*Rebuttal.* Cold-start-first §5.4 explicitly describes a phased trajectory (cold-start → warm-start → steady-state) where "the cycle structure is identical from cycle 1; the difference is the size of the knowledge store." Greenfield-substrate-first §5.3 has the same phased trajectory with identical substrate primitives running the whole time. Greenfield-methodology-first §5.4 has the same. **The three greenfield tracks differ on which day-0 risks they emphasize, not on the architecture.** Cold-start-first names "bootstrap-borrowed priors + sunset-edges" as its distinctive primitive — but it is the same primitive that unified-A's `greenfield-feed` adapter implements (pre-loaded operator priors) and that unified-C's §5.2 "priors that are permitted" enumerates. Different emphases on the same substrate move.

**Splitter move 3 (the hardest one to rebut): "Brownfield-substrate-first's ESS wedge is genuinely structural — it adds 7+ substrate primitives that have no greenfield counterpart at the same severity (B-5: governance-declaration emitter has no greenfield analog). This is a different architecture, not a configuration."**

*Rebuttal.* The wedge is the *Core 2 specialization* this section names. Conceded: Core 2 ≠ Core 1. But Core 2 is a thin specialization (one substrate wedge) of Core 1, and the cycle / methodology / regime classifier / judge composer / watchdog / cost ceilings are identical. **Two architectures, not nine.** Unified-A's `brownfield-feed` adapter and unified-C's Excavation overlay both already incorporate this wedge into the unified architecture as a feed/overlay, demonstrating that the wedge is composable with Core 1 rather than orthogonal to it. The splitter can win "Core 2 is real," but cannot win "Core 2 is one of nine."

**Splitter move 4: "Methodology-first tracks (D, E) genuinely invert CTR-C2; they are not substrate-heavy."**

*Rebuttal.* Brownfield-methodology-first §6 enumerates a substrate dependency table that is *more demanding* than brownfield-substrate-first's primitive set (typed-object store + rules engine + capability tokens + event-sourced trajectories + worktree isolation + Daemon/Triage/Patrol + holdout-enforced acceptance + parallelism budget). Greenfield-methodology-first §1.4 enumerates 13 substrate primitives. Both tracks call themselves "methodology-first" but ship substrate-heavy architectures with the methodology as a per-tier cycle. The framing is methodology-first; the architecture is substrate-heavy. This is precisely Round-2's substrate-heavy/thin-methodology shape under a different banner.

---

## Section 5 — Recommendation to Phase 3 lead agent

Phase 3 should produce **2 merged drafts**, not 3 (and certainly not 9):

1. **`unified-synthesis-v1.md` (Core 1 — Tier-Gated Shared Substrate).** Mandate-agnostic substrate (trajectory, sandbox + production-scissors-default-off, tiered watchdog, cost ceilings, holdout-partitioning, cross-model judge composer with deterministic outer perimeter + probabilistic inner, cognitive-escrow primitive, typed knowledge store with provenance edges, regime classifier with configurable bin count and configurable classification axis). Methodology is a per-tier overlay. The four "overlay" archetypes (Discovery / Excavation / Production-touch / Regulated, per unified-C; or T0–T4, per unified-A; or 5 pace-layers, per unified-B) become *configuration parameters* of one architecture. Cold-start is a regime of this architecture with a bootstrap-window default-to-Augmentation rule.
   - **Tracks that map here:** unified-A, unified-B, unified-C, greenfield-substrate-first, greenfield-methodology-first, greenfield-cold-start-first.

2. **`brownfield-synthesis-v1.md` (Core 2 — Core 1 + Existing-System Wedge).** All of Core 1, plus the ESS wedge as additional substrate primitives (codebase index + symbol graph, dependency-graph + change-impact analyzer, existing-test-suite ingester, runtime-telemetry parser, PR-archaeology cache, EAI inference + invariant store, governance-declaration emitter, in-tree holdout-partitioning, archaeology cache). Methodology cycle is identical to Core 1; the substrate has more primitives because the codebase exists.
   - **Tracks that map here:** brownfield-substrate-first, brownfield-methodology-first, brownfield-legacy-ingestion-first.

3. **No separate `greenfield-synthesis-v1.md`.** Greenfield is **Core 1 with the `greenfield-feed` adapter** (per unified-A's design) — operator-curated priors, exemplar projects, library docs, EARS/GtWR scaffolds, El Kaim intent-block templates as substrate input. This is a configuration of Core 1, not a separate architecture. The 3 greenfield tracks' contributions (cold-start protocol, intent-block discipline, regime gate composition) are absorbed as Core 1 sections.

**Headline mandate-fit matrix.** Rows: Core 1 (unified), Core 2 (brownfield + ESS wedge). Columns: 5 work-unit-classes. Most cells are `both` for Core 1 and `brownfield` for Core 2; cell-level defense is via tier-distribution per cell per mandate.

**Phase-3 adversarial pass.** The unified-mandate-attacker should attack Core 1 (one architecture, two adapters); the brownfield-attacker should attack Core 2 (does the ESS wedge actually compose with Core 1's cycle?). With 2 targets the adversarial pass is sharper and faster than with 3 or 9.

**Phase-7 back-fill audit.** Maps each archive item to: Core 1 substrate primitive / Core 2 substrate primitive / tier-overlay choice / cold-start protocol step. ~14 expected ADRs split between Core 1 substrate and the wedge — exactly the count the brief's §6 item 6 predicted.

*End.*
