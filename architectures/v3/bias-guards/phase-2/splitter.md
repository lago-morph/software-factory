---
based-on-commit: 5c4deeb
based-on-date: 2026-05-24
position: splitter
---

# Phase-2 splitter argument

**Position.** The 9 Phase-2 tracks have produced **6 honestly distinct architectures** (not 2-3), and Phase-3 merge should preserve those 6 as separate candidate architectures rather than collapsing them. The lumper's preference for fewer-architectures replays a Round-2-style consolidation bias: it treats *convergence on substrate primitives* (which is real and was the design — D1 expected substrate-shareability per OQ-B2) as *convergence on architectures* (which it is not). Phase 6 needs the divergent load-bearing commitments that only show up when each track's primary axis is preserved.

The splitter case is **not** "9 architectures, one per track." Three tracks are genuinely weaker as standalones (see §5). It is "≥6 architectures, because the load-bearing commitments at the cycle, gate, and regime layer diverge in ways that the substrate-shareability does not erase."

---

## Section 1 — The substantive differences across tracks

### Pair: greenfield-substrate-first vs. greenfield-methodology-first

- **Lumper's likely claim:** "Both end up with a typed-intent perimeter (S3 / primitive #1), EARS lint, trajectory capture, holdout discipline, watchdog, cost ceilings, judge routing. The 8 substrate primitives in greenfield-substrate-first §1.1 are essentially congruent with the 13-primitive table in greenfield-methodology-first §1.4. Same architecture, different rhetorical entry point."
- **My counter:** The two tracks **disagree on the load-bearing dependency direction**, and Phase 6 specs are *derivations* from a primary anchor — they will diverge wherever derivation order matters.
  - greenfield-substrate-first §1.2: *"The methodology is the **minimum** process needed to use the eight primitives, no more. Greenfield methodology fits in five gates per cycle."* The cycle is residual.
  - greenfield-methodology-first §1.1: *"The work-unit is a **single regime-classified, intent-anchored, spec-bounded, judge-gated, promotion-closed cycle**."* The 9-step cycle (REGIME GATE → INTENT FREEZE → SPEC DRAFT → DECOMP → BUILD → JUDGE → HOLDOUT → PROMOTION → DRIFT CHECK) is the architecture; substrate is "what the cycle forces into existence."
  - The five-gate vs nine-stage cycle is **not the same cycle with different names**. Methodology-first has a load-bearing `DECOMP` stage with `redecompose` action (anti-F59), a `PROMOTION` stage with explicit typed classification (`insight | playbook | correction | pattern | intent-invariant | scenario | dead`), and a `DRIFT CHECK` against ARCHITECTURE.md. Substrate-first has none of these as substrate primitives — it explicitly excludes "self-improvement / methodology evolution as substrate" (§1.1 exclusions) and explicitly turns knowledge accumulation **OFF** until cold-start ends (§1.4: *"For greenfield cold-start, the default knowledge accumulation is *nothing*"*). Methodology-first turns promotion **ON from cycle 1** (§1.3: *"The promotion step (step 8) is the inverse of F10... cycle outputs are typed per followup/11"*).
  - Load-bearing for: a Phase-6 spec author needs to know whether `docs/solutions/`-class knowledge accumulation begins at cycle 1 or after the cold-start boundary. The two tracks give opposite answers.

### Pair: brownfield-substrate-first vs. brownfield-methodology-first

- **Lumper's likely claim:** "Both end up with deterministic-perimeter judges, EAI/pace-layer enforcement at merge, production-scissors default-off, holdout-partition primitives, trajectory capture. The ESS wedge (§2.1–§2.11) is just the substrate side of the cycle the methodology-first track describes (§1.2 stages). One architecture."
- **My counter:** The two tracks **disagree on what the work-unit is**, and OQ-B4 is brief-mandatory.
  - brownfield-substrate-first §6: *"Unit of work shape (OQ-B4). Issue-from-queue vs change-request-against-spec vs codebase-evolution-proposal is a methodology choice; **the substrate supports all three**."* Explicitly declines to pick.
  - brownfield-methodology-first §0.2: *"This track does not pick Atelier or Refinery. The chosen work-unit shape is the **codebase-evolution proposal** (the OQ-B4 option *not* in the v2 set)."* Explicitly picks, and the entire 8-stage cycle (PROPOSAL → CLASSIFICATION GATE → DECOMPOSITION → DISPATCH → INTENT GATE → BUILD → REVIEW GATE → MERGE GATE → COMPOUND) presupposes that pick.
  - Substrate-first treats Atelier/Refinery/proposal as interchangeable downstream methodology choices on top of the ESS wedge. Methodology-first treats Atelier and Refinery as **typed downstream specializations of the proposal cycle** — Atelier emits when the proposal touches only pace-layer 1; Refinery emits when it modifies a Spec; proposal recurses when it modifies Architecture/Standards. These are different architectural commitments about what the cycle is. A Phase-6 spec built on substrate-first inherits no opinion about OQ-B4; one built on methodology-first inherits the codebase-evolution proposal as load-bearing. F60 (parallel-cycle compounding) is owned at proposal-level in methodology-first (per §0.2 table) and is *not assigned an owner* in substrate-first.

### Pair: brownfield-substrate-first vs. brownfield-legacy-ingestion-first

- **Lumper's likely claim:** "Both lean substrate-heavy for brownfield. Both have a codebase-derived facts cache (ESS wedge / ingestion artifact). Both have pace-layer awareness. Collapse."
- **My counter:** The two tracks **disagree on whether ingestion is *a* primitive or *the* primitive that the rest hangs off**.
  - brownfield-substrate-first §2: ESS is **one of several** primitives (§2.1–§2.11), each independently justified by a critical-severity F-mode. Symbol graph, embeddings, dependency graph, test ingester, telemetry parser, PR-archaeology, EAI inference, governance-emitter, production-scissors, holdout-partition, archaeology cache — eleven primitives, no hierarchy.
  - brownfield-legacy-ingestion-first §0.4 (anticipating substrate-first critic): *"ingestion is *a* primitive, not *the* architecture. The legacy-ingestion-first axis is not 'ingestion is the architecture'; it is 'ingestion is the **organizing primitive** the rest of the architecture is downstream of, and the design of every other primitive (judge, scaffold, watchdog, scenario source) is constrained by the ingestion artifact's shape.'"*
  - Concretely: the ingestion track makes **freshness SLO + re-ingestion triggers** (§2.4) a load-bearing substrate-level protocol — patrol-tier watchdog escalates persistent freshness violations. The substrate-first track has no freshness SLO; the ESS refresh discipline is "event-sourced on git push" with no SLO and no Patrol escalation hook for staleness. This matters at Phase 6: legacy-ingestion-first declares an F-NEW-ingestion-drift candidate failure mode (§3.4) that substrate-first does not surface.
  - Additionally: legacy-ingestion-first §2.3 explicitly states *"It is **not** a methodology concern... cycles either read the artifact or the substrate refuses to dispatch them."* Substrate-first lets methodology choose how aggressively to read the ESS. These are different *substrate-vs-methodology lines for the same artifact class.* Phase-4 needs both options on the table.

### Pair: unified-A (risk-tier) vs. unified-C (stakes-tier)

- **Lumper's likely claim:** "Both organize by blast-radius × reversibility × regulatory exposure. Both classify work into tiers (5 in A, 4 in C). Both have a tier-classifier as substrate primitive. Both map regime to tier. Both treat mandate as derived distribution. **These are the same architecture with a different tier-count.**" *This is the lumper's strongest move on the unified side.*
- **My counter:** The two tracks **disagree on how the tier mechanism composes with overlay/methodology choices**, in ways that change the v2 archive's backfill semantics.
  - unified-A §1.2: the v2 architectures **absorb as tier-overlays** — *"T0 work uses Attractor-style `.dot` pipelines... T1 work uses Compound-Engineering-style... T2 work uses Refinery-style... T3 work uses Tournament-style... T4 work uses Council-style."* The v2 set becomes a **menu indexed by tier**.
  - unified-C §3: only **four overlays** (Discovery / Excavation / Production-touch / Regulated), and they are not v2 architectures — they are *purpose-built* methodologies (Discovery is greenfield-shaped, Excavation is brownfield-shaped, Production-touch and Regulated are tier-shaped). The v2 architectures do *not* map cleanly into unified-C's overlay set; they would need to be re-decomposed.
  - This is a load-bearing Phase-7 (back-fill audit) divergence: unified-A predicts ~80% of v2 material absorbs as tier-overlay configuration; unified-C predicts ~30% absorbs (the substrate-shared parts) and the rest is rejected because it presupposes the wrong overlay-set decomposition.
  - Further: unified-A treats mandate purely as a *covariate* of tier (§1.4: every cell in the work-unit-class × tier matrix is reachable; mandate is distribution-only). unified-C explicitly retains **mandate-shape** in the Discovery (greenfield) vs Excavation (brownfield) overlay names; mandate-shape is the *primary* discriminator for T0-T1 overlay selection, with tier becoming primary only at T2+. unified-C is *partially mandate-axis* and *partially tier-axis*. unified-A is mandate-axis-free.
  - Phase-3 merge that lumps these loses the *mandate-shape-survives-at-low-tier* commitment, which is the unified-C track's primary defense against UC4-purist attacks (§0.3 point 1: *"The architecture does not collapse the distinction; it relocates it"* via mandate-named overlays). unified-A explicitly rejects that move.

### Pair: unified-B (pace-layers) vs. unified-A/C (tier-axes)

- **Lumper's likely claim:** "unified-B's pace-layer regime matrix (§3.2: Code=L5, Plans=L4, Specs=L4, Architecture=L4-ratified, Standards=L4-sign-off) is **isomorphic** to a tier matrix where higher pace-layer = higher tier. Five layers ≈ five tiers. Same axis with different labels."
- **My counter:** Pace-layers organize **artifacts**; tier-axes organize **work-units**. unified-C §0.2 makes this exact point: *"Pace-layers organize *artifacts*; stakes-tier organizes *work-units*. They are orthogonal and composable."*
  - Concrete divergence: in unified-B, a single cycle that touches Code only stays at Code-layer L5 even if it deploys to T3-regulated production (because the pace-layer of the *artifact* is code). In unified-A/C, that cycle is T3 regardless of which layer the artifact lives at, because the *blast radius of the cycle* is T3. The two architectures route the same hot-fix-to-regulated-prod cycle through opposite gate sets.
  - unified-B's Sentinel (§3.1, §3.3) is a dedicated agent watching cross-layer-drift (F34) — first-class architectural primitive. unified-A and unified-C have **no Sentinel**; F34 is handled by tier-classifier reclassification of drifting work, not by a dedicated drift-detection agent. Phase-6 spec authors building from unified-B have a Sentinel role to specify; those building from A/C do not.
  - Further: unified-B (§3.3) explicitly resolves MISSED-3 by layer-assignment (El Kaim invariants live at Standards layer; UC4 spec-malleability lives at Specs layer). unified-A/C resolve MISSED-3 by tier-graded invariant ratchet (invariants append-only after T3 entry). These are different mechanisms; the unified-B resolution puts invariants at a stable artifact location; the unified-A/C resolution puts invariant-stability under tier-classifier control. A regulator auditing the factory would have different audit surfaces.

### Pair: greenfield-cold-start-first vs. other greenfield tracks

- **Lumper's likely claim:** "Cold-start-first is greenfield-substrate-first with §5 expanded. Same 8-or-so primitives; same intent-block centrality; same EARS/GtWR lint; same escrow harness; same exit gates around K=5 + RIR + agreement thresholds. Collapse into greenfield-substrate-first."
- **My counter:** Cold-start-first explicitly *redefines steady-state* as "the cold-start architecture is what an honest steady-state architecture looks like anyway" (§0.2 point c). This is a **regime-recurrence claim** the other greenfield tracks do not make.
  - greenfield-substrate-first §5.3 has a cold-start boundary crossing after which knowledge accumulation, self-improvement, and scaffold-evolution **turn on** as methodology overlays. The substrate stays the same but the regime changes.
  - greenfield-cold-start-first §0.2 (a): *"For an operator running the factory across multiple greenfield projects ... every new project is Day 0. Cold-start-shaped substrate amortises across project-starts."* The cold-start regime is **architecturally permanent**, recurring per-project; the sunset-edge ledger (§0.1) is the load-bearing substrate primitive that the other tracks don't have.
  - This produces materially different Phase-6 specs: cold-start-first's spec carries the sunset-edge ledger and bootstrap-prior store as first-class substrate; substrate-first does not. For an operator running >1 greenfield project (UC1's plural framing), this difference is load-bearing for cost and cycle-time.

---

## Section 2 — Why distinct architectures matter at Phase 3+

The brief (D1) authorized the 9-track fanout *because* the lumping-toward-one-architecture instinct was structurally baked into the 6-track design and Phase-3 was unable to falsify UC4. The same risk now appears one level up: Phase-3 merge can over-collapse Phase-2 outputs and re-create the same falsification gap at Phase 6+.

Specific reasons Phase 6 benefits from 5-8 architectures over 2-3:

1. **D2's per-(architecture × work-unit-class) mandate-fit matrix presupposes multiple architectures.** With 2-3 architectures the matrix has ≤15 cells; with 6-8 it has 30-40. The matrix's discriminative power for the user-facing `00-comparison-v3.md` artifact (brief §6 item 8, *"the single most user-facing artifact of v3"*) depends on cell-level distinctions. Collapsing architectures collapses cells; collapsed cells hide the load-bearing distinctions the user-facing comparison was built to surface.

2. **Phase-8 lean-evals are per-architecture.** Each architecture produces one 1-day lean-eval brief (brief §6 item 10). Collapsing 6 architectures to 3 means losing 3 lean-eval briefs that would have measured genuinely different operating shapes. The empirical evidence is *constructed by* the architecture count.

3. **Phase-5 ADRs are split across shared-substrate (wave 1) and mandate-specific (wave 2).** brief §6 item 6 estimates ~14 ADRs. If Phase-3 collapses to 2-3 architectures, wave 2 collapses to near-zero (no per-architecture decisions to make) and the ADR set under-specifies the load-bearing choices. The substrate-first / methodology-first / cold-start-first divergence within greenfield, for example, produces at least three wave-2 ADRs (knowledge-accumulation-on-from-cycle-1 vs after-cold-start; cycle-shape five-gate vs nine-stage; sunset-edge ledger yes/no) that disappear if those tracks collapse.

4. **Phase-7 back-fill audit semantics change with architecture count.** The audit marks each archived v1/v2 item as `absorbed`/`rejected`/`TBD`. A 2-architecture set absorbs less of v1/v2 than a 6-architecture set, because each v2 architecture (Atelier, Refinery, Tournament, Council, Foundry) only finds a clean home if a Phase-6 architecture has the shape to absorb it. unified-A explicitly absorbs all v2 architectures as tier-overlays; unified-C explicitly does not. That divergence dies on collapse.

5. **Adversarial-pass survivability is per-architecture.** brief §6 item 4: each mandate-synthesis "surviving multi-persona adversarial review." Collapsed architectures share a single adversarial-pass surface; distinct architectures get independent ones. The corpus has multiple distinct attack vectors (cost / regulator / on-call / Schillace F52 / Jaymin L5 / UC4-purist / RSI-aware); a single architecture cannot be simultaneously strong against all of them. Distinct architectures let each defend its niche; collapse forces a single architecture to defend all niches at once.

6. **CTR-C2 is itself unresolved.** *"Substrate-heavy + thin-methodology (Round-2 framing) vs. methodology-dominates (UC4 hypothesis)"* — this is a corpus contradiction the 9 tracks were dispatched to explore. Collapsing 6 substrate-axis-vs-methodology-axis tracks to 2-3 architectures means picking a side on CTR-C2 at Phase 3 (a contradictions register entry, not Phase-3's job to resolve). Per ADR-0005 concrete-task discipline, unresolved CTRs should be surfaced as DECISIONS-PENDING for the user, not silently consolidated.

---

## Section 3 — The corpus genuinely supports plurality

- **CTR-C2 (substrate-heavy vs methodology-dominates).** The corpus has both Round-2 §8 (*"configure a methodology on top of an existing substrate"*) and UC4 (*"no single architecture works best for both mandates"*) as load-bearing contributing voices. The 9 tracks split on this CTR explicitly (substrate-first tracks pick Round-2 side; methodology-first tracks pick UC4 side). Lumping mid-Phase-3 implicitly resolves CTR-C2 without the contradictions register noting the resolution.

- **Brier's pace-layers (followup 12).** unified-B's central anchor. Brier explicitly proposes multi-velocity layers as the structural alternative to single-layer architecture. unified-B operationalizes this as a **stack of five concurrent loops** (§2.1-§2.5). Lumping unified-B with the tier-axis tracks loses the multi-velocity-loop structure (tier-axes have one cycle that runs at a tier-determined cadence; pace-layers has five cycles running at five cadences in parallel). These are not the same architecture; one has 5× the concurrent loops.

- **D2 (per-(architecture × work-unit-class) matrix).** D2's authorization presupposes architectures-plural. The schema explicitly accommodates `n/a` cells; a 2-architecture set with mostly `both` cells (which is exactly what unified-A predicts in its §7 YAML and unified-C predicts in its §6) provides less information than a 6-architecture set with mixed `greenfield`/`brownfield`/`both`/`n/a` cells. The matrix's job is *discrimination*; collapsing reduces discrimination.

- **Corpus inventory tagging.** The Phase-1 corpus inventory tags reports with `greenfield-primary` / `brownfield-primary` / `both-secondary` (per the brief and CHALLENGE-6/7/8 in the miscategorization audit). The audit found that `both-primary` is rare — most reports skew mandate. If the inventory itself surfaces genuine mandate skew, the architecture set should reflect that skew, not flatten it through unified lumping. The corpus does not strongly support a `both-primary` architecture set; it supports a `greenfield + brownfield + selective both` set.

- **D1's structural argument.** Skeptic finding #3, captured at D1: the 6-track design was structurally incapable of finding a both-mandates architecture because no track was tasked to build one. The symmetric argument applies in reverse: if Phase 3 dispatches 2-3 architectures, downstream phases are structurally incapable of finding architectural divergence at the work-unit-shape, cycle-shape, knowledge-accumulation-timing, and sentinel-vs-no-sentinel layers. D1's logic generalizes: structural capacity to find divergence requires preserving divergence at each phase boundary.

- **Phase-1 bias-guard MISSED-3 (El Kaim invariants vs UC4 spec-malleable).** Different tracks resolve this differently (substrate-first: invariants at substrate, body at methodology; methodology-first: split intent/spec/code stack; cold-start-first: two-velocity partition of the 9-field block; unified-A: tier-graded invariant ratchet; unified-B: invariants at Standards layer; unified-C: invariants bound spec-malleability from above). Six tracks, six distinct resolutions. If MISSED-3 has multiple defensible resolutions, the architecture set should preserve them; the user is the one who picks (per the brief's DECISIONS-PENDING discipline).

---

## Section 4 — The lumper's strongest counter, and your rebuttal

**The lumper's strongest move:** "unified-A and unified-C are *the same architecture* — both organize by blast-radius × reversibility × regulatory-exposure tiers, both have a substrate-level tier-classifier as the central primitive, both reduce mandate to a covariate, both invoke the same Kahana RSI three-part test, both have the same per-tier judge-architecture escalation (same-model OK at low tier; cross-model required at T2; third-party at T3). The tier count (5 vs 4) and the overlay names (Compound/Attractor/Refinery/Tournament/Council vs Discovery/Excavation/Production-touch/Regulated) are surface variation. **One architecture, two voices.**"

This is the hardest counter to rebut. The substrate-primitive overlap is real (both have S1=tier classifier, S2=trajectory, S3=watchdog, S4=cost ceilings, S5=cross-model judge, S6=knowledge edge, S7=cognitive escrow); the regime-per-tier mapping is structurally identical (lights-out at low tier, AILCCP Human Approval Gate at top tier); the empirical-anchor citations are largely shared (Replit, CodeRabbit, Veracode, Kahana RSI).

**My rebuttal:**

1. **The overlay decomposition is *not* surface — it's the Phase-7 backfill commitment.** unified-A explicitly absorbs v2 Atelier/Refinery/Tournament/Council/Foundry as tier-overlay configuration choices (§1.2). unified-C explicitly invents purpose-built overlays (Discovery/Excavation/Production-touch/Regulated) that do *not* map to the v2 set. A Phase-7 audit run against unified-A would mark Compound Engineering as `absorbed (as T1 overlay)`; the same audit against unified-C would mark Compound Engineering as `rejected (overlay decomposition is mandate-shape-axis, not v2-architecture-axis)` or `partially absorbed`. These are not the same architecture for Phase-7 purposes.

2. **unified-A is mandate-axis-free; unified-C retains mandate-axis at low tier.** unified-C §3.1/§3.2 has Discovery (greenfield-shape) and Excavation (brownfield-shape) as **named, mandate-shaped** overlays at T0-T1. unified-A §1.4 explicitly rejects this: every cell of the work-unit-class × tier matrix is reachable; mandate is distribution-only. A Phase-3 merge that lumps these loses unified-C's mandate-shape-survives-low-tier commitment — the very property unified-C uses to defend against UC4-purists. The defenses against the unified-mandate-attacker (D1 Phase-3 adversarial) differ between the two; lumping picks one defense and discards the other.

3. **Even if the architectures look similar at substrate, they're different *evaluation surfaces* at Phase 8.** A lean-eval brief for unified-A measures "does the tier-classifier route 5 work-unit-classes × 5 tiers correctly across 1-day manual run." A lean-eval brief for unified-C measures "does the overlay-selector correctly fire Discovery vs Excavation at T0-T1, and does the tier-mechanism correctly fire at T2+." Different measurement instruments produce different empirical evidence. UC5 (*accuracy ≫ speed ≫ tokens*) authorizes more, not fewer, measurement instruments.

4. **The contradiction Phase-3 should surface, not resolve.** If the lumper is correct that unified-A and unified-C are "one architecture, two voices," that itself is a finding to record (e.g., "the unified architecture under a tier-axis has two defensible decompositions; the user picks"). Per ADR-0005 concrete-task discipline, the decision should be surfaced for user review, not silently made by Phase-3 merge. Phase-3's job is the *register* of decisions-pending, not the *resolution* of them.

That said: if Phase-3 absolutely must collapse the unified-A and unified-C pair into one architecture, the splitter concedes this as the *least-cost collapse* — the two genuinely share substrate primitives and tier-axis-as-primary. They should still surface to Phase 6 as **two architecture specs** under one architecture *family* (e.g., `unified-tier-family` with `-A` and `-C` variant specs), not as a single spec, so the overlay decomposition divergence survives into Phase 7/8.

---

## Section 5 — Recommendation to Phase 3 lead agent

**Recommended distinct-architecture count after Phase 3 merge: 6.**

**Mapping of 9 tracks to 6 architectures:**

| Architecture | Source tracks | Rationale |
|---|---|---|
| **G-substrate** | greenfield-substrate-first | Distinct primary commitment: substrate carries variance, methodology is residual; knowledge-accumulation OFF until cold-start ends. |
| **G-methodology** | greenfield-methodology-first | Distinct primary commitment: 9-stage cycle is the architecture; PROMOTION + DRIFT-CHECK as load-bearing structural steps; knowledge accumulation ON from cycle 1. |
| **G-cold-start** | greenfield-cold-start-first | Distinct primary commitment: cold-start regime is permanent and recurring across UC1's plural-projects framing; sunset-edge ledger + bootstrap-prior store as load-bearing substrate. |
| **B-ESS-substrate** | brownfield-substrate-first + brownfield-legacy-ingestion-first (merged as one architecture with two emphasis variants) | These two are the least-distant pair on the brownfield side — both substrate-heavy, both centered on codebase-derived facts. Merge them but preserve the freshness-SLO + Patrol-escalation commitment from legacy-ingestion-first as a load-bearing substrate property the merged architecture must keep. |
| **B-proposal-cycle** | brownfield-methodology-first | Distinct primary commitment: codebase-evolution-proposal as load-bearing work-unit shape (the OQ-B4 third option); 8-stage cycle with explicit classification gate. Does not absorb into B-ESS-substrate because the work-unit-shape commitment is structural, not stylistic. |
| **U-pace-layered** | unified-B | Distinct primary commitment: 5 concurrent loops, Sentinel as first-class drift-detection agent, MISSED-3 resolved by layer-assignment. Does not absorb into U-tier because pace-layer and tier-axis are orthogonal (per unified-C §0.2 explicit acknowledgment). |
| **U-tier-axis** | unified-A + unified-C (merged as one architecture family with two variant specs) | The hardest split case. Merge into one *family* with two Phase-6 specs (A-variant: tier-axis-only with v2-as-overlay absorption; C-variant: tier-axis with mandate-shape-retained at low tier). The family is one architecture; the variants preserve Phase-7 backfill semantics divergence. |

That is 6 architectures (7 if the unified-tier family's variants count separately at Phase 6, which is recommended). The split-then-merge inside brownfield (B-ESS) and inside unified-tier (U-tier-axis) is the splitter's concession to the lumper on the two pairs where substrate-primitive overlap is genuinely high.

**What this preserves:**
- The CTR-C2 (substrate-heavy vs methodology-dominates) split, on both mandates.
- The OQ-B4 (work-unit-shape) split, on brownfield (B-ESS-substrate doesn't pick; B-proposal-cycle picks).
- The pace-layer-vs-tier-axis split, on the unified side.
- The mandate-shape-retained-vs-eliminated split, within the unified-tier family.
- The cold-start-as-transient-vs-permanent split, on greenfield.

**What this concedes to the lumper:**
- brownfield-substrate-first and brownfield-legacy-ingestion-first merge (B-ESS-substrate). The ingestion track's distinct contribution survives as a load-bearing freshness-SLO commitment within the merged architecture rather than as a standalone architecture.
- unified-A and unified-C merge as one architecture family with two variants. The tier-axis-as-primary commitment is shared; the v2-absorption vs purpose-built-overlay divergence survives as variant specs at Phase 6.

**What this rejects from the lumper:**
- Any collapse to ≤3 architectures. The corpus, the brief's D1/D2/D3 structural commitments, the bias-guard's MISSED-3 plurality of resolutions, and Phase 6/7/8's downstream needs all argue for ≥5; 6 is the splitter's defensible floor.

*End.*

---

## Report-back (5 sentences)

1. **Recommended distinct-architecture count after Phase 3 merge: 6** (7 if unified-tier-axis's A-variant and C-variant count separately as Phase-6 specs within one architecture family, which is recommended).
2. **Most honestly distinct from all others:** greenfield-cold-start-first (cold-start as recurring regime + sunset-edge ledger primitive; structurally novel), brownfield-methodology-first (codebase-evolution-proposal work-unit + 8-stage classification-gated cycle; OQ-B4 third option), unified-B pace-layered (five concurrent loops + Sentinel + MISSED-3 by layer-assignment; orthogonal axis to tier).
3. **Weakest as standalones (conceded to lumper):** brownfield-legacy-ingestion-first (its distinct contribution — freshness SLO + ingestion-as-Patrol-input — survives best as a substrate commitment inside a merged B-ESS-substrate architecture), unified-A and unified-C as fully separate (genuinely share tier-axis-as-primary + substrate primitives; survive as variants in one architecture family).
4. **Hardest lumper argument to rebut:** "unified-A and unified-C are one architecture, two voices" — the substrate primitives, tier-axis-as-primary, and regime-per-tier mapping are nearly congruent; my best counter is that the v2-overlay-absorption vs purpose-built-overlay divergence is load-bearing for Phase 7, but I concede they belong in one architecture family rather than as two fully-separate architectures.
5. **Strongest splitter argument for preserving plurality:** D2's per-(architecture × work-unit-class) mandate-fit matrix is the single most user-facing v3 artifact (brief §6 item 8), and its discriminative power is constructed by architecture count — collapsing to 2-3 architectures empties the matrix's cell-level distinctions, the very distinctions the user asked for in the brief's headline output; plurality at Phase 3 is plurality at Phase 6 is plurality in the comparison artifact the user reads first.
