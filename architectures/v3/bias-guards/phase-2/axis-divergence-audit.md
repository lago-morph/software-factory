---
guard: axis-divergence-auditor
phase: 2
based-on-commit: a0d4b67716d5158f7fa559344aa00463b4f5fece
based-on-date: 2026-05-24
---

# Axis-divergence audit — Phase-2 (9 tracks)

## §1 Method

I read each of the nine Phase-2 tracks end-to-end (§0 declaration, §1 architecture sketch, §2 concern coverage, §4 defaults, §5 cold-start/legacy, §6 not-this, §7 open questions) and scored on four dimensions:

1. **Axis declaration clarity** — is §0 a real defense of *why-this-axis-for-this-mandate*, or generic motherhood that could prefix any architecture?
2. **§1 axis-shapedness** — would §1 still hold if I swapped the §0 declaration to a different axis? Concretely: do the *named primitives or stages* presuppose the declared axis, or are they generic primitives labeled with the axis vocabulary?
3. **Axis-distinctive moves** — 1–3 architectural moves that would *not* appear under a different axis for the same mandate.
4. **Drift indicators** — moves that look inherited from the brief/decisions/Round-2-defaults rather than derived from the axis.

Then I ran pair-wise comparisons within each mandate, within each axis cross-mandate, and across the three unified tracks. The framing comes from [`00-brief-v3.md §3`](../../00-brief-v3.md) (D1 falsifiability framing) and the Phase-2 rerun plan's "divergence IS the design" stipulation.

Scoring scale used in §2 below: **strong** (axis is doing the structural work), **partial** (axis-flavor is real but architecture would survive axis-swap with renaming), **drifted** (the architecture is the corpus-default shape with a label glued on).

## §2 Per-track axis-compliance scorecard

### 2.1 greenfield-substrate-first — **strong**

- **§0 clarity.** Excellent. Pre-responds explicitly to the Round-2-anchor attack ("substrate-first is what Round-2 already did") and to the "you've made substrate so thick it eats spec-malleability" attack. Defends ordering on F59/F9 grounds.
- **§1 axis-shapedness.** §1 is a 9-primitive substrate stack (S1–S9) with a *deliberately under-specified* methodology that says "unit of work is not fixed at the architecture level — it is a methodology choice on top of substrate." This is the cleanest test of substrate-first: the architecture refuses to commit to a methodology shape. You cannot rewrite §0 to methodology-first without rebuilding §1.
- **Axis-distinctive moves.** (a) **S9 eligibility classifier as substrate primitive** — naming regime as a substrate-typed object rather than a policy concern; (b) **S8 four-guards-full-stop** — the explicit cap on guards as substrate F52-defense; (c) **Methodology layer left deliberately empty**, unit-of-work declared not-at-architecture-level.
- **Drift indicators.** The cold-start §5 trajectory metrics (scenario saturation, judge stability, Patrol absence-of-drift) are largely the same shape any greenfield track would produce. Some of S1–S7 are direct lifts of Round-2 defaults (D-4/D-5/D-6/D-7), but the track openly marks them so and locates the *axis claim* in S8/S9 and in the methodology-layer-emptiness.

### 2.2 greenfield-methodology-first — **strong**

- **§0 clarity.** Strong. Names methodology-first as "what cycle shape stays productive while the spec is still moving" and explicitly sits on the methodology-dominates pole of CTR-C2.
- **§1 axis-shapedness.** §1 is a two-regime cycle (spec-discovery vs. spec-anchored execution) with concrete stage shapes (intent draft → paraphrase divergence → tiny probe → promote-or-reverse). §1.3 lists what the cycle *requires* of substrate as a downstream derivation. This is the inverse stance to 2.1 and it shows.
- **Axis-distinctive moves.** (a) **Two named regimes A and B with explicit exit criterion** (slice coherence) — a methodology-layer concept the substrate-first track refuses to commit to; (b) **Paraphrase-divergence as in-cycle F37 detector** (behavioural disagreement across paraphrasers rather than LLM-judge contradiction-detection); (c) **Reversible-commitment as unit-of-work** — a methodology coinage absent from any other track.
- **Drift indicators.** §1.3's "substrate consequence" list reads as Round-2 defaults reframed (D-7, D-4, D-6, D-5). This is honest derivation but means *the substrate is identical to the substrate-first track's S1–S9 minus naming.* All 7 defaults accepted, 0 challenged — the track itself flags this as informative.

### 2.3 greenfield-cold-start-first — **strong**

- **§0 clarity.** Strongest defense in the greenfield triad. Explicitly argues cold-start is the *organizing principle*, not a section, and names five `critical`-rated F-modes (F1, F25, F40, F41, plus governance F43) converging on day 0.
- **§1 axis-shapedness.** Architecture is named "Bootstrap-Bench Factory" with five day-0 primitives (Intent Crucible, EARS-mandated Acceptance Criteria, Cold-Start Bench, Cognitive-Escrow Operator Surface, RSI-Declaration Ledger), three sub-phases, and a measurable **graduation protocol** from cold-start regime to steady-state regime. The graduation protocol is the load-bearing axis-derived move — no other track has anything like it.
- **Axis-distinctive moves.** (a) **Graduation protocol with explicit, measurable criteria** (bench saturation, K=5 baseline, cross-model judge agreement rate, RSI cadence); (b) **Two-regime substrate** where day-0 primitives differ from day-N primitives; (c) **"Micro-cold-start per new work-unit-class"** as a recurring architectural commitment.
- **Drift indicators.** Several primitives overlap with the substrate-first track (Intent Crucible ≈ S2/S8; RSI Ledger ≈ S9 governance instance; Cognitive-Escrow operator surface is also load-bearing in unified-A/B). But the axis claim is *which* primitives are load-bearing at day 0 and the graduation gate — those are unambiguously cold-start-derived.

### 2.4 brownfield-substrate-first — **strong**

- **§0 clarity.** Strong. Sub-axis explicitly named ("codebase-and-runtime as primary substrate inputs"), with three brownfield-specific reasons (codebase is primary input, codebase IS the scenario holdout, lethal-trifecta is constitutive of brownfield not optional).
- **§1 axis-shapedness.** Five substrate primitive classes (S-1 Codebase Index, S-2 Dependency/Impact Graph, S-3 Runtime/Telemetry Ingestor, S-4 Change-History/Attribution Store, S-5 Perimeter/Trifecta-Closure) — all *brownfield-specific* in content (you wouldn't put a Codebase Index in greenfield-substrate-first, and indeed greenfield-substrate-first doesn't). The methodology overlay is thin.
- **Axis-distinctive moves.** (a) **D-2 challenged with substrate role-partitioning of S-3 telemetry as the in-codebase holdout mechanism**; (b) **S-2 impact graph as the per-cycle lights-out classifier input** (regime computed from substrate evidence, not declared); (c) **F-mode-to-primitive mapping table in §2.8** is exhaustively substrate-first in framing.
- **Drift indicators.** Minor. The "Compound-as-methodology is compatible" framing is generous to neighboring tracks but doesn't dilute the substrate stance.

### 2.5 brownfield-methodology-first — **strong**

- **§0 clarity.** Strong. Six numbered defense points, including the crucial observation that "the brownfield system is already the substrate" so substrate-first would be redundant.
- **§1 axis-shapedness.** Architecture is an **8-stage per-cycle methodology contract** (Trigger → Comprehension → Intent capture → Plan → Build → Cross-model review → Acceptance → Ship-or-escalate). Each stage names methodology obligation + the substrate capability it requires *at the boundary*. The table format makes the methodology-first stance visible: substrate is named but enumerated downstream.
- **Axis-distinctive moves.** (a) **Stage-2 Comprehension producing an "archaeological brief"** as a per-cycle artifact (not a maintained substrate); (b) **Stage-3 "change-intent block" — spec the change, not the system** (a methodology framing the substrate-first track explicitly does not adopt); (c) **Stage-compression rules per work-unit-class** as the architecture's variation surface.
- **Drift indicators.** D-2 challenged on the same grounds as brownfield-substrate-first and brownfield-legacy-ingestion-first — this is corpus convergence not drift. F-mode mitigation table is brownfield-default in many cells.

### 2.6 brownfield-legacy-ingestion-first — **strong**

- **§0 clarity.** Strong. Sub-axis "code-archaeology is the primary organizing principle" with concrete distinction from substrate-first ("substrate-first builds generic primitives; ingestion-first builds *codebase-specific* primitives derived per-instance").
- **§1 axis-shapedness.** Three-loop architecture (Ingestion deep-and-slow / Work per-cycle / Maintenance continuous) over a single durable **Codebase Model** artifact with six views (structural / conventional / historical / runtime / invariant / debt). Work-unit-class taxonomy itself is *derived from the codebase model* — that's the axis claim instantiated.
- **Axis-distinctive moves.** (a) **Codebase Model as a per-instance substrate primitive that is built, queried, and refreshed** — the ingestion loop is first-class, not preparatory; (b) **Work-unit-class derivation from model profile** (not pre-decided); (c) **Regime classification per code region** (not per work-unit, not per factory).
- **Drift indicators.** Some overlap with brownfield-substrate-first's S-1/S-2/S-3 set (Codebase Model's structural/runtime views ≈ S-1/S-3), but ingestion-first treats the model as a continuously-maintained derived artifact whose evolution drives methodology parameterization — a meaningfully different stance.

### 2.7 unified-A — escrow-interval-as-substrate — **strong (axis is genuinely distinct)**

- **§0 clarity.** Strong and self-aware (explicitly invokes D7 blind-axis discipline).
- **§1 axis-shapedness.** Architecture is "Escrow-Graph Factory": every cycle is a directed graph of typed `EscrowInterval` nodes with five fields (kind / pace-layer / priors / policies / classifier / artefacts). Five substrate primitives all interval-anchored. Greenfield-vs-brownfield is *the same architecture* with different graph shapes and different `priors.in-tree`. The interval-as-typed-object move is the load-bearing novelty.
- **Axis-distinctive moves.** (a) **`EscrowInterval` as substrate-typed object with embedded policy fields** (gate/log/sandbox/approval-gate/reflection-trigger/judge-diversity); (b) **Mandate-symmetric handling: same primitives, different graphs**; (c) **Re-entry registrar as a substrate primitive whose protocol fires deterministically.**
- **Drift indicators.** AILCCP three-controls map directly onto the interval-policy fields — this is a corpus-driven move that any unified track might make. The "thin methodology = graphs of intervals" framing is hard to distinguish from a substrate-first stance at large.

### 2.8 unified-B — pace-layer × cognitive-escrow — **strong**

- **§0 clarity.** Strong. Explicitly preempts convergence with A and C by claiming the axis is *artifact-stack-shaped*, not substrate-primitive-shaped or regime-classification-shaped. (This claim survives my cross-check; see §3.3.)
- **§1 axis-shapedness.** Architecture is "Pace-Layered Escrow Factory" (PLEF) with five Brier layers (L0 Standards / L1 Architecture / L2 Spec / L3 Plan / L4 Code), each carrying change-rate and escrow-policy fields. Greenfield = top-down traversal; brownfield = bottom-up *inference*. Same primitives, opposite traversal direction. The traversal-direction move is genuinely distinct from anything else in the set.
- **Axis-distinctive moves.** (a) **Per-layer typed object with change-rate field** as the substrate's organizing primitive; (b) **Bidirectional traversal (top-down vs. bottom-up) as the mandate-difference mechanism**; (c) **Per-layer provider-property routing** (L0/L1 long-context + diverse; L4 provider-aligned) — neither pure RouterLLM nor pure Attractor.
- **Drift indicators.** The escrow primitive is *shared with unified-A* — both name Kahana's interval as load-bearing substrate. PLEF differentiates by attaching the escrow to *layer transitions*, not to all transitions. This is a real difference but reveals corpus convergence on escrow-as-substrate.

### 2.9 unified-C — distance-from-frozen-anchor — **strong**

- **§0 clarity.** Strong. Most novel axis declaration in the set. Explicitly names why it didn't pick substrate/methodology layering, L3/L4/L5 regime, or work-unit-class taxonomy (anticipating the D7 blind-axis test).
- **§1 axis-shapedness.** Architecture is "Anchor-Distance Factory" (ADF) with five primitives (Anchor object / Distance estimator / Distance-gated dispatcher / Anchor mutation queue / Distance-keyed trajectory storage). The mandate becomes a *parameter* (anchor's `kind`-content) rather than the organizing distinction. The dispatcher's three regimes (near-anchor lights-out / mid-distance Augmentation / far-anchor or anchor-edit human-required) is the load-bearing axis-derived move.
- **Axis-distinctive moves.** (a) **Distance as a substrate-typed scalar fed into a dispatcher** — no other track has this primitive; (b) **`anchor-edit` as a first-class work-unit-class** with separate queue and mandatory L4; (c) **Steady-state transition defined as a distance-distribution shift, not a calendar event.**
- **Drift indicators.** The distance estimator's components (intent-fields touched, blast radius, pace-layers crossed) directly absorb unified-B's pace-layer model — the track flags this in §0 ("partial yes; we are renaming Brier's pace-layers"). This is the most candid drift acknowledgment in the set.

## §3 Pair-wise divergence analysis

### 3.1 Intra-mandate divergence (same mandate, different axis)

**Greenfield (substrate-first vs. methodology-first vs. cold-start-first).** Divergence: **high.** The three tracks make architecturally incompatible commitments:

- substrate-first refuses to specify unit-of-work at architecture level (it is methodology choice on top of S1–S9).
- methodology-first defines a *specific cycle with named stages and a regime split* (Regime A / Regime B).
- cold-start-first defines a *two-regime substrate* (cold-start regime primitives vs. steady-state regime primitives) with a graduation protocol.

A merger would have to pick: is the unit-of-work declared at architecture level (methodology-first: yes — reversible commitment; cold-start-first: yes for day 0 — tiny EARS criterion against single scenario; substrate-first: no). The three converge on `EARS+GtWR lint as deterministic guard`, `cross-model judge mandatory at high-stakes`, and `eligibility classification as the lights-out gate` — but those are corpus defaults from reports 25/26/F46/F1, not axis-derived.

Effective overlap on substrate primitives is ~50–60%; effective overlap on architectural commitments at the methodology layer is <20%. **Axis is doing real work.**

**Brownfield (substrate-first vs. methodology-first vs. legacy-ingestion-first).** Divergence: **moderate.** All three converge on:

- D-2 challenged (scenarios from codebase).
- Cross-model judge required (F46).
- Production-scissors substrate-default-off (F44).
- Codebase index/dependency graph as a load-bearing primitive (substrate-first calls it S-1/S-2; legacy-ingestion-first calls it Codebase Model views; methodology-first calls it stage-2 archaeological brief).

What actually differs:
- substrate-first: the index is a *continuously-maintained substrate primitive* queried per cycle.
- methodology-first: the index is a *per-cycle archaeological brief* produced by stage-2 and compressed for downstream stages.
- legacy-ingestion-first: the model is *built by a dedicated phase*, has six explicit views, drives work-unit-class derivation and per-region regime classification.

Effective overlap on primitive list: ~70%. Effective overlap on *where the load-bearing investment sits*: <30%. **Axis is doing real work but the corpus signal is strong** — the brownfield F-mode set (F12/F20/F21/F34/F44/F56 brownfield-critical) over-determines large parts of all three tracks. This is closer to corpus signal than to drift, given that the three tracks differ meaningfully on continuity (substrate continuous vs. methodology per-cycle vs. ingestion-then-maintained), on whether the model drives methodology (yes for ingestion-first, no for the others), and on cycle shape (per-cycle 8 stages vs. unit-of-work-agnostic vs. work-unit-class-derived-from-model).

### 3.2 Intra-axis divergence (same axis, different mandate)

**substrate-first cross-mandate (greenfield-substrate-first vs. brownfield-substrate-first).** Primitives overlap on names (sandbox, trajectory capture, cost ceilings, watchdog, judge routing) but the *content* of substrate primitives is mandate-different:

- Greenfield S1–S9 includes spec-lint guards (S8), eligibility classifier (S9), and scenario storage with builder-blindness (S2). No codebase index. No dependency graph.
- Brownfield S-1 through S-5 is codebase-index / dependency-graph / runtime-telemetry / change-history-attribution / perimeter. No spec lint as substrate; no eligibility classifier as substrate (the dispatcher uses S-2/S-3 evidence to compute classification per-cycle).

This is exactly the divergence Phase-4 will need: substrate-first as an axis produces *different substrate enumerations* per mandate. **Mandate is doing more work than axis here.**

**methodology-first cross-mandate (greenfield vs. brownfield).** Different cycle shapes (two-regime reversible-commitment cycle vs. 8-stage trigger-to-ship). Both treat substrate as derivation. The methodology-first axis is doing similar *meta*-work in both (organize around the cycle, not the substrate) but the cycles themselves are mandate-shaped. **Axis and mandate roughly balanced.**

### 3.3 Unified-vs-unified divergence

The three unified tracks were free to pick axes. They picked:
- A: escrow-interval-as-substrate
- B: pace-layer × cognitive-escrow
- C: distance-from-frozen-anchor

**They did pick distinct axes** (a small relief — they did not all collapse to "substrate-heavy + thin-methodology"). But they share a load-bearing primitive: **all three name the cognitive-escrow interval (Kahana, report 30) as foundational substrate.** A explicitly puts the interval at the center; B uses pace-layer transitions as the interval-firing trigger; C uses the dispatcher decision moment as the interval. F53 (voluntary-discipline fragility) and F42 (cognitive-escrow negligence) are foundational to all three.

The three also converge on:
- **Per-cycle / per-interval / per-distance regime classification** as the lights-out/L5 dissolution mechanism (all three pick brief §2.1 option c+b).
- **Mandate as a parameter, not a top-level distinction** (A: differs by `priors` field; B: differs by traversal direction; C: differs by anchor `kind`).
- **D-2 challenged or sharpened** (all three reframe holdout).
- **D-3 challenged** (all three find Agent = Model + Harness insufficient; A and C explicitly extend the decomposition).

Effective overlap on substrate primitive content: ~55%. Effective overlap on the unified claim ("mandate is a parameter"): ~95%. **The corpus over-determines a fairly specific unified shape**: a typed-object substrate primitive (interval / layer / anchor) carrying policy fields, with mandate as a parameter of priors-or-traversal-direction. The three tracks differ on *what is the typed object* and *how mandate enters* — these are meaningful architectural choices, not labels — but they are three flavors of one approach.

This is the single biggest convergence in the audit. It looks like **corpus signal, not drift**: all three independent unified tracks landed on (typed object + policy + parameterized mandate) because the F42/F53/F46/F44 + D-4/D-6/D-7 + CTR-B5/CTR-C2 cluster narrows the design space sharply.

### 3.4 Same-axis-different-mandate vs. different-axis-same-mandate

For greenfield: different-axis-same-mandate (greenfield trio) produces *more* architectural divergence than same-axis-different-mandate (greenfield-substrate-first vs. brownfield-substrate-first). For brownfield: roughly equivalent. This says axis is doing meaningful work in the greenfield triad and roughly equal work to mandate in brownfield.

## §4 Findings: which axes did real work, which didn't

**Axes that did the most architectural work:**

1. **cold-start-first (greenfield).** Produces the most distinctive architecture in the entire set (two-regime substrate + measurable graduation protocol + "micro-cold-start per new work-unit-class"). No other track has anything resembling the graduation protocol. The axis is genuinely load-bearing.
2. **methodology-first (greenfield).** Produces the two-regime cycle with reversible-commitment unit-of-work — both novel coinages that wouldn't survive an axis-swap.
3. **distance-from-frozen-anchor (unified-C).** The most novel axis in the unified triad; the distance estimator + dispatcher + anchor-edit queue trio is not derivable from any other axis.
4. **legacy-ingestion-first (brownfield).** Codebase Model as a continuously-maintained derived artifact whose evolution parameterizes methodology — genuinely distinct from substrate-first.

**Axes that did partial work (axis-flavor is real, but corpus signal dominates):**

5. **substrate-first (brownfield).** The brownfield-critical F-mode set over-determines the substrate enumeration; most of S-1 through S-5 would appear in any defensible brownfield architecture. The axis claim is "this is *load-bearing investment*, not preparatory work," which is real but subtle.
6. **methodology-first (brownfield).** The 8-stage cycle is essentially Compound Engineering + Notion-Boxy + SWE-bench loop with structured staging. The axis claim ("the cycle IS the architecture") is real but the cycle itself is corpus-defaulted.
7. **substrate-first (greenfield).** The S1–S9 set is closest to Round-2's substrate-heavy framing; the axis-distinctive moves (S9 eligibility, deliberately-empty methodology) are real but smaller than the Round-2 inheritance.
8. **escrow-interval-as-substrate (unified-A).** The interval-as-typed-object is novel, but the policy fields enumerated (gate/log/sandbox/approval-gate/reflection-trigger/judge-diversity) directly absorb AILCCP + D-4/D-6 + F46 — corpus-driven.
9. **pace-layer × cognitive-escrow (unified-B).** The bidirectional-traversal move is genuinely distinct; the layer enumeration is Brier's. The axis is doing work but it is partly axis-renaming of Brier with escrow bolted on.

**Axes that drifted:** None. No track is *just* the corpus default with axis vocabulary glued on. The weakest axis-shapedness is greenfield-substrate-first (which inherits the most from Round-2), but it still differentiates via S8 four-guards-cap and S9 eligibility-classifier-as-substrate.

## §5 Implications for Phase 3

**Tracks that deserve full adversarial weight (distinctive architectural commitments that would die or survive on their merits):**

- greenfield-cold-start-first (graduation protocol is a falsifiable architectural claim).
- greenfield-methodology-first (two-regime cycle + reversible-commitment unit-of-work).
- brownfield-legacy-ingestion-first (Codebase Model as continuously-maintained per-instance substrate driving methodology parameterization).
- unified-C (distance-as-dispatcher-scalar; if the distance estimator fails adversarial gaming, the architecture collapses).
- unified-B (bidirectional pace-layer traversal; the brownfield bottom-up inference is the load-bearing novel claim).

**Tracks that look like aliases (substantial-but-not-load-bearing axis distinction):**

- greenfield-substrate-first vs. greenfield-methodology-first: substrate enumeration is ~80% identical (the methodology-first §1.3 derivation list reproduces most of substrate-first's S1–S9 minus the cap-and-classifier moves). Phase-3 merge should not treat them as fully orthogonal architectures; they are two presentations of the substrate-heavy shape with different commitments at the methodology surface.
- brownfield-substrate-first vs. brownfield-methodology-first: the brownfield S-1/S-2/S-3 substrate primitives reappear inside brownfield-methodology-first's stage-2/3/7 obligations. The difference is *whether the index is continuously maintained* (substrate-first) or *per-cycle reconstructed* (methodology-first). That is a real ADR question, not two architectures.
- unified-A and unified-B share the escrow primitive and may be one architecture with the escrow attached at different granularities (A: every interval; B: every layer transition). Phase-3 should test whether they collapse.

**Biggest Phase-3 implication.** The three unified tracks **independently converged on (typed object + policy + parameterized mandate)** as the shared substrate shape. This is strong evidence that **D1's hypothesis is partially falsifiable for unified architectures**: a defensible unified shape exists in the corpus signal. The remaining argument is *what the typed object should be* (interval vs. layer vs. anchor) and *what mandate parameterizes* (priors vs. traversal direction vs. anchor kind). Phase 3 should treat these as three candidate instantiations of one unified family rather than three competing unified architectures, and dispatch adversarial passes that attack the family-level claim before adjudicating between instantiations.

**Secondary implication.** The greenfield triad is genuinely divergent and should not be merged into a single greenfield architecture without explicit choice between two-regime-graduation (cold-start-first), two-regime-reversible-commitment (methodology-first), and methodology-deferred-to-overlay (substrate-first). These are not aliases — they make incompatible architectural commitments at the unit-of-work and regime-transition layers.

**Tertiary implication.** The blind-axis test (D7) is owed especially to **substrate-first across all three mandate scopes** (greenfield, brownfield, all unified tracks lean substrate-heavy). Three tracks independently locating their architecture in the substrate layer is a strong corpus convergence; whether it is *also* a contamination from Round-2 is the question D7 was designed to ask, and greenfield-substrate-first §7 question 7 explicitly asks for the test.

## §6 Limits

- **I am scoring axis-shapedness from §0+§1+§7 text, not from independent corpus re-derivation.** A track that argues its axis well may score "strong" even if a deeper corpus reading would show the architecture is over-determined. The Phase-3 adversarial pass is the catch.
- **I did not run the blind-axis test myself** (D7's intent). I observe convergence patterns and flag them; I cannot rule out that a *fourth* unified subagent would have produced a fourth axis with similar architectural commitments.
- **I treated "primitive overlap %" intuitively, not by token-counting or formal comparison.** Numbers in §3 are eyeballed; the qualitative claim (which axis is doing real work) is what to trust, not the exact percentages.
- **I read §5 (cold-start) on the greenfield and unified tracks but only skimmed brownfield §5 (which the brownfield tracks correctly mark N/A or recast as legacy-ingestion).** The greenfield cold-start treatments are the load-bearing comparison surface in this audit.
- **The three unified tracks' axis convergence on "mandate as parameter"** could be either corpus signal (the design space is narrow) or shared contamination from the brief §3 framing (which explicitly invites unification). My judgment is corpus signal, but I cannot prove the negative.
- **I did not cross-check claims about specific corpus reports** (report 14, 25, 26, 30, 31, etc.) in this pass. Tracks may be citing reports accurately or loosely; that is a separate audit.
- **I am one of four concurrent Phase-2 bias guards.** Anchor-detector, splitter, and lumper may surface contamination or convergence patterns I missed. Read this audit against theirs before drawing Phase-3 conclusions.

*End of axis-divergence-audit.md.*
