# 04 — The 10 candidates side-by-side

This file is the side-by-side comparison. For each candidate: the distinctive bet, methodology shape, what's already covered by OSS substrate, what you'd actually have to build, buildability estimate, what the bias-guards said about it, and what could kill it.

## The "at-a-glance" table

| # | Candidate | Mandate | Distinctive bet (one sentence) | Buildability | Practitioner verdict |
|---|---|---|---|---|---|
| 1 | **GF-S** | Greenfield | The substrate is the architecture; a 4-guard ensemble (lint + contradiction-detector + budgeter + perimeter type-check) makes the methodology run safely on auto-pilot. | Medium (4-guard mediator is the new piece) | Mechanically clean; practitioner-relevance medium |
| 2 | **GF-M** | Greenfield | The per-cycle process *is* the architecture; cross-model paraphrasers on the spec are a stronger contradiction defense than any single LLM judge. | **Low** (paraphrase harness is the new piece) | Mechanically clean; practitioner-relevance medium |
| 3 | **GF-C** | Greenfield (cold-start) | Day-0 is the load-bearing surface; a structured 9-field intent schema + EARS-linted acceptance criteria + signed scenario bench prevents the cold-start failure cascade. | Medium (Intent Crucible + GtWR lint) | **High practitioner-relevance** (substance-check on intent) |
| 4 | **BF-S** | Brownfield | A heavy substrate (codebase index + dependency graph + perimeter-typed boundary) makes the methodology thin and reliable on small/medium codebases. | High (codebase indexing is the new piece) | **High practitioner-relevance** (perimeter-bypass test) |
| 5 | **BF-M** | Brownfield | The 8-stage cycle (Trigger→Comprehension→Intent→Plan→Build→Review→Acceptance→Ship) is the architecture; an archaeological-brief generator carries the codebase context. | Medium (archaeological-brief tooling) | **High practitioner-relevance** (brief-recall measurable) |
| 6 | **BF-L** | Brownfield (legacy) | Code archaeology is the work; a 6-view Codebase Model is the substrate the methodology queries; everything else is a thin overlay. | **Highest** (Codebase Model = 6-12 engineer-months) | Medium practitioner-relevance (Pulse-loop closure visible) |
| 7 | **U-A** | Unified | Every work cycle is a directed graph of typed nodes (intent, plan, build, review, etc.); policies enforced at node boundaries; the typed-graph is the methodology. | Medium (typed-object store + policy mediator) | Mechanically clean; **practitioner-thin** (substrate-emitted evidence) |
| 8 | **U-B** | Unified | Five pace-layers (L0 standards → L4 code); greenfield is top-down traversal, brownfield is bottom-up inference; same architecture, opposite direction. | Medium (layer-typed store + drift detector) | Mechanically clean; **practitioner-thin** |
| 9 | **U-C** | Unified | Every work unit is parameterized by graph-distance to a frozen anchor; three regimes (near=lights-out / mid=Augmentation / far=human-required); mandate is a parameter of the anchor's kind. | Medium-High (distance estimator + anchor store) | Mechanically clean; medium practitioner-relevance (dispatcher tests legible) |
| 10 | **D7-U-1** | Unified | Every load-bearing artifact carries an opposing-side "Falsification Commitment" that must survive refutation before compounding forward; the architecture is the topology of build/break pairs. | Medium-High (FC store + opposing-side router + independence auditor) | Mechanically clean; **practitioner-thin** |

**Reading the table:** the "buildability" column is rough effort beyond the shared substrate baseline (Kilroy + OpenHands + CXDB + Beads + LiteLLM + scenario harness, ~2-4 engineer-weeks). The "practitioner verdict" comes from the Phase 8 domain-practitioner audit — `practitioner-thin` means the candidate's falsifier measures substrate-emitted distributions/counts rather than software-quality outcomes a practitioner would care about.

The pattern in the table: **the mandate-aligned candidates (greenfield-only or brownfield-only) tend to be practitioner-stronger than the unified-attempts.** Three of four unified-attempts (U-A, U-B, D7-U-1) score practitioner-thin. U-C is the exception.

## Per-candidate cards

### GF-S — Greenfield, substrate-first

**Distinctive bet.** The substrate, not the methodology, is the safety surface. A four-guard ensemble (GtWR lint + multi-model contradiction-detector + req-count budgeter + perimeter type-checker) sits between the agent and any consequential action. The methodology can be thin because the substrate refuses unsafe outputs.

**Methodology shape.** Deliberately thin 8-step per-cycle process. Substrate primitives dominate the design surface. Unit-of-work, spec format, agent topology are explicitly left to "methodology choices on top of substrate."

**Substrate composition.**
- Pipeline engine: Kilroy or Fabro (default).
- Agent runtime: OpenHands.
- Event store: CXDB.
- Work ledger: Beads.
- **New build:** The 4-guard mediator. GtWR lint = INCOSE R7-R35 rule engine (~1-2 weeks). Contradiction-detector = multi-model judge ensemble using LiteLLM (~1-2 weeks). Budgeter and perimeter type-checker are smaller (~1 week combined).

**Buildability estimate.** ~3-5 engineer-weeks beyond shared substrate.

**What could kill it.** Compounding-guard cost (CFO concern: every guard fires on every cycle; aggregate cost may make L5 economically infeasible at scale). F40 last-mile drift is explicitly unaddressed — the methodology has no story for what happens when the substrate-enforced specs drift from production reality.

**Practitioner verdict (from Phase 8 audit).** Mechanically clean; medium practitioner-relevance.

---

### GF-M — Greenfield, methodology-first

**Distinctive bet.** Run the spec past N (≥3) cross-family paraphrasers in parallel and look for behavioral disagreement at the post-condition level. Disagreement is the contradiction signal — more reliable than asking one LLM judge "are these consistent?" because single-judge MCC on contradiction-detection caps at ~0.55.

**Methodology shape.** Two regimes. Regime A (spec-discovery, mostly cold-start): 4-phase cycle = intent draft → paraphrase divergence → tiny probe → promote-or-reverse. Regime B (spec-anchored execution, steady-state): standard compound-engineering loop (plan→work→review→compound) with cross-model review panel. Slice-coherence is the A→B transition criterion.

**Substrate composition.**
- Pipeline engine: Kilroy.
- Agent runtime: OpenHands.
- Event store: CXDB.
- Work ledger: Beads.
- LLM client: LiteLLM (specifically needed for the cross-family routing).
- **New build:** Paraphrase divergence harness (LiteLLM router with N=3 cross-family tags + sentence-transformer divergence metric + 95-percentile threshold). ~1 engineer-week.

**Buildability estimate.** ~1-2 engineer-weeks beyond shared substrate. **Cheapest of the 10 candidates to first pressure-test.**

**What could kill it.** Paraphrase divergence might have its own MCC ceiling on contradiction detection (this is GF-M's own load-bearing falsifier per the Phase 8 lean-eval). Paraphrase fan-out × cost-ceiling interaction (N× cost per cycle could be prohibitive). Slice-coherence is operationally underdefined — "an end-to-end scenario passes through the slice without an intent gap" needs a substrate-implementable check.

**Practitioner verdict.** Mechanically clean; medium practitioner-relevance.

---

### GF-C — Greenfield, cold-start-first

**Distinctive bet.** Day-0 is when greenfield projects fail, and the failure is operator-intent-illiteracy. A structured 9-field intent schema (Intent Crucible) + EARS-linted acceptance criteria + a signed scenario bench (cryptographic holdout from day-0) forces the operator to author a substantive intent before any agent work fires.

**Methodology shape.** Three sub-phases: (1) Intent ingestion with Council interrogation (multi-model questioning to surface ambiguity); (2) Bench construction (scenarios authored *before* code); (3) First-cycle restraint (don't accept the first plausible-looking output). Graduation protocol with four explicit criteria moves work-units from Cold-Start regime to Steady-State.

**Substrate composition.**
- Pipeline engine: Kilroy.
- Agent runtime: OpenHands.
- Event store: CXDB.
- Work ledger: Beads.
- **New build:** Intent Crucible (9-field typed-object schema validator — small). EARS+GtWR linter (INCOSE R7-R35 rules — ~2-3 weeks). Cold-Start Bench (HMAC-signed scenario store — ~1 week).

**Buildability estimate.** ~3-5 engineer-weeks beyond shared substrate.

**What could kill it.** Operator-intent-illiteracy is the candidate's own biggest unresolved concern. The substrate can scaffold operator intent richness, but if the operator routinely click-throughs the structured intake (Hughes-trappings risk), the cold-start safeguards become theater. The 18-month thin-intent → click-through → F40 failure cascade is the pre-mortem.

**Practitioner verdict.** High practitioner-relevance. The bias-guard audit specifically liked the substance-check on intent fields (blind-labeled thin-vs-rich Intent discrimination is a measurable signal practitioners can read).

---

### BF-S — Brownfield, substrate-first

**Distinctive bet.** For small/medium brownfield codebases, build a heavy substrate (codebase index + dependency-and-impact graph + role-partitioned telemetry + per-symbol attribution + perimeter-typed boundary) once, and the methodology becomes a thin overlay. The substrate does the codebase reading; the methodology composes substrate queries.

**Methodology shape.** Thin overlay: work-unit selection, per-cycle composition of substrate queries, per-cycle V&V, knowledge promotion. Most of the design surface is in the substrate, not the methodology.

**Substrate composition.**
- Pipeline engine: Kilroy.
- Agent runtime: OpenHands.
- Event store: CXDB.
- Work ledger: Beads.
- **New build:** Codebase index (Tree-sitter + Glean or Sourcegraph as foundation, ~4-6 weeks). Dependency-and-impact graph (Stack-graphs + GitHub stack-graphs, ~1-2 weeks). Telemetry with per-role read filters (OpenTelemetry collectors with attribute-based access control, ~1 week). Per-symbol attribution (git plumbing + GitHub commit API, ~1 week). CaMeL-class perimeter (~2 weeks).

**Buildability estimate.** ~8-12 engineer-weeks beyond shared substrate. This is the second-most expensive after BF-L.

**What could kill it.** Role-partition of in-codebase reads leaks via dependency-graph edges (the ROBUST claim was downgraded to "rate-limited side-channel mitigation"). At Stripe-scale (~1300 PRs/week), self-reference accretion is the predicted failure mode — the substrate refreshes from the factory's own output, so the index becomes a hall of mirrors over time.

**Practitioner verdict.** High practitioner-relevance. Perimeter-bypass-rate is a directly observable metric a practitioner cares about.

---

### BF-M — Brownfield, methodology-first

**Distinctive bet.** The 8-stage per-cycle contract IS the architecture: Trigger → Comprehension → Intent capture → Plan (N candidates) → Build → Cross-model review → Acceptance (held-out scenarios from codebase) → Ship-or-escalate. An archaeological-brief generator (LLM-driven structured codebase summarization) carries the codebase context into each cycle; substrate is downstream.

**Methodology shape.** Disciplined 8-stage cycle. Stages compress/expand per work-unit-class (regression-fix collapses stages 2-4; refactor expands stage 3). Cross-model review is the F46 single-model-blindspot defense.

**Substrate composition.**
- Pipeline engine: Kilroy.
- Agent runtime: OpenHands.
- Event store: CXDB.
- Work ledger: Beads.
- LLM client: LiteLLM (cross-family routing for the review panel).
- **New build:** Archaeological-brief generator (LLM with structured output schema, ~1-2 weeks). CaMeL-class typed-interpreter (from the CaMeL paper + AgentDojo benchmarks, ~2 weeks). Held-out scenario runner that pulls scenarios from the codebase itself (~1 week).

**Buildability estimate.** ~4-6 engineer-weeks beyond shared substrate.

**What could kill it.** Stage-compression rules per work-unit-class are sketched, not specified. Cross-model review necessity under Anthropic's finding that same-model review can be fine is unresolved. CaMeL utility-tax acceptance criterion not set (how much overhead is too much?). Scenarios-from-codebase governance unspecified.

**Practitioner verdict.** High practitioner-relevance. Brief-recall MCC against labeled invariants is a directly measurable engineering signal.

---

### BF-L — Brownfield, legacy-ingestion-first

**Distinctive bet.** For large legacy codebases (1M+ LOC, 18+ month history, multiple languages), ingestion is the dominant cost and the dominant risk. Invest heavily in a Codebase Model with six views (Structural / Conventional / Historical / Runtime / Invariant / Debt) before any work fires; the methodology then queries the model rather than the codebase.

**Methodology shape.** Three loops over the Codebase Model: (1) Ingestion (deep, slow, once per codebase + refresh on triggers); (2) Work (per-cycle, methodology-shaped, queries the model); (3) Maintenance (continuous, low-cadence, reconciles model with reality — this IS the Pulse-report / self-healing-loop pattern). Work-unit-class taxonomy is derived from the codebase model's own profile.

**Substrate composition.**
- Pipeline engine: Kilroy.
- Agent runtime: OpenHands.
- Event store: CXDB.
- Work ledger: Beads.
- **New build (the load-bearing investment):** The Codebase Model. Six views, each backed by one or more existing OSS foundations:
  - Structural: Tree-sitter + Stack-graphs
  - Conventional: custom (idiomatic-pattern extraction)
  - Historical: git plumbing + GitHub APIs + Codescene-style churn
  - Runtime: OpenTelemetry collectors
  - Invariant: CodeQL semantic database
  - Debt: custom (Codescene + per-view debt metrics)
  - Integration: custom (the unified queryable layer over all six)

**Buildability estimate.** ~6-12 engineer-months. **The most expensive primitive in the entire catalog.** Don't start here unless the lean-eval evidence specifically demands the Pulse-loop pattern for your domain.

**What could kill it.** Codebase Model staleness vs. cycle latency (refresh cost). Per-region regime fragments governance (F43 board-visibility). The Codebase Model itself is a F54 attack surface (if it's poisoned, every methodology decision is poisoned). Ingestion-as-substrate vs. ingestion-as-methodology is unresolved — should the ingestion logic live in the substrate or be runnable as a pipeline?

**Practitioner verdict.** Medium practitioner-relevance. The Pulse-loop closure is directly visible (drift events surfaced + acted on), but the upfront cost dominates the decision.

**Don't start with this one for pressure-testing.** Build it only after you've validated the methodology shape against smaller candidates.

---

### U-A — Escrow-Graph Factory (Unified)

**Distinctive bet.** Every work cycle is a directed graph of typed nodes (intent, plan, build, review, ship, etc.); each node carries its kind, pace-layer, priors, policies, classifier-decision, and artifacts; the substrate enforces policies at node boundaries. The typed-graph shape IS the methodology — universal across mandates because mandate becomes a node attribute, not a separate methodology.

**Methodology shape.** Cycle = typed-node DAG. Policies are declarative (OPA or Cedar). Re-entry registrar handles node restarts. Classifier decides routing at each node boundary.

**Substrate composition.**
- Pipeline engine: Kilroy or Mammoth (typed-node fit Mammoth's DOT linter well).
- Agent runtime: OpenHands or Overstory (Overstory's fleet shape maps to U-A's per-node-as-agent posture).
- Event store: CXDB.
- Work ledger: Beads.
- **New build:** Typed-object store (content-addressed, append-only — IPFS or git's object store as foundation, ~1-2 weeks). Policy mediator (OPA or Cedar — config + integration, ~1 week). Re-entry registrar (substrate-typed event protocol, ~1 week).

**Buildability estimate.** ~3-4 engineer-weeks beyond shared substrate.

**What could kill it.** DPU-1 granularity concern: process-state node is many nodes per cycle, highest substrate cost at year-2 scale (~thousands of nodes/day). If applied to brownfield: U-A doesn't address the BF-L Codebase Model gap (would need to bolt one on). Graduation criteria are not cross-mandate measurable (how do you know a node is "done" in a way that means the same thing across greenfield and brownfield?).

**Practitioner verdict.** Mechanically clean; **practitioner-thin**. U-A's falsifier measures `methodology-delta` count in the `solutions/` directory — substrate-emitted evidence rather than software-quality outcomes a practitioner can see.

---

### U-B — Pace-Layered Escrow Factory (Unified)

**Distinctive bet.** Five Brier pace-layers (L0 standards / L1 architecture / L2 spec / L3 plan / L4 code). Greenfield = top-down traversal (seed L0/L1 from priors, descend to L4 code). Brownfield = bottom-up inference (read L4 code, infer upward to L1 architecture). Same architecture, opposite direction; mandate becomes traversal-direction parameter.

**Methodology shape.** Per-layer typed object store, transition gates at each layer boundary, cross-layer drift detector. The pace-layer model is the architectural document.

**Substrate composition.**
- Pipeline engine: Kilroy.
- Agent runtime: OpenHands.
- Event store: CXDB.
- Work ledger: Beads.
- **New build:** Layer-typed object store (one per pace-layer, ~1 week). Cross-layer drift detector with per-layer invariants (Brier's pace-layer framework is a description, not a tool — needs substrate-side detector implementation, ~2-3 weeks).

**Buildability estimate.** ~3-4 engineer-weeks beyond shared substrate.

**What could kill it.** Layer count is empirical, not derived — Brier asserts 5, El Kaim implies more. If the right number is 6 or 7, the architecture is wrong. Bottom-up inference's mechanics are not specified — "read L4 code, infer L3 plan" sounds clean but isn't a defined procedure. F52 risk: deterministic structure imposed on stochastic agents may produce a brittle process.

**Practitioner verdict.** Mechanically clean; **practitioner-thin**. U-B's falsifier measures `LayerInferenceConfidence` distribution — substrate-emitted, not practitioner-felt.

---

### U-C — Anchor-Distance Factory (Unified)

**Distinctive bet.** Every work unit declares an anchor (a frozen reference: a spec section, a deployed system, a regulatory document, etc.) and measures distance to it; a dispatcher routes by distance regime. Near-anchor work is lights-out (high confidence; tight contract). Mid-distance work is Augmentation (cross-family judge required). Far-anchor or anchor-edit work is human-required. Mandate is parameterized by the anchor's `kind`.

**Methodology shape.** Three regimes (near / mid / far). Dispatcher reads the distance estimator's output and routes. Anchor mutation queue is separate from work queue (anchor edits are always human-approved, by name).

**Substrate composition.**
- Pipeline engine: Kilroy.
- Agent runtime: OpenHands.
- Event store: CXDB.
- Work ledger: Beads.
- **New build:** Distance estimator (multi-component: graph distance on dependency graph + pace-layer crossings + intent-field-touch count, ~2 weeks). Anchor object store (typed content-addressed with mutation-protocol enforcement, ~1 week). Distance-gated dispatcher (~1 week). Anchor mutation queue (separate work queue with named-human approval gates, ~1 week).
- **Cross-candidate dependency:** the graph-distance component needs BF-L's Codebase Model if you want brownfield coverage. Otherwise you'd build a simpler dependency-graph substrate just for U-C.

**Buildability estimate.** ~4-6 engineer-weeks beyond shared substrate. **Plus** Codebase Model dependency if brownfield.

**What could kill it.** F47 Goodhart on distance estimator (agents game the scoring to land work in the lights-out regime). F33/F51 Ashby-deficiency on probabilistic detection (the distance signal may not have enough variety to discriminate the regimes). F8 stale-knowledge over multi-month cold-start. Operator-legibility of distance estimator at dispatch time — can the operator understand WHY this work-unit was routed to lights-out vs. mid?

**Practitioner verdict.** Mechanically clean; medium practitioner-relevance. The dispatcher's regime-distribution is directly observable; H-1 stable-ID adoption (U-C volunteered) makes anchor traceability legible.

---

### D7-U-1 — Falsification-Topology Factory / FTF (Unified)

**Distinctive bet.** Every load-bearing artifact (spec / plan / code-change / eval / ADR / skill / classifier-decision / scaffold) is parameterized by a typed **Falsification Commitment (FC)** that names which opposing side (model-family-different agent / deterministic checker / named human / population vote) must try to falsify it before it can compound forward. The architecture IS the topology of build/break pairs. Compounding-gate refuses to let an artifact propagate downstream unless its declared FC survived.

**Methodology shape.** Per-artifact cycle: creation → FC declaration → opposing-side refutation attempt → survival verdict → compounding gate. Greenfield: sparse initial FC catalog, operator-as-opposing-side at day-0. Brownfield: rich initial FC catalog (existing tests, telemetry, type checks already serve as opposing sides).

**Substrate composition.**
- Pipeline engine: Kilroy or Mammoth.
- Agent runtime: OpenHands.
- Event store: CXDB.
- Work ledger: Beads.
- **New build:** FC store with typed envelope schema (content-addressed append-only log, ~1-2 weeks). Opposing-side router (provider-property-driven; needs model-family taxonomy + capability registry, ~1-2 weeks). Independence auditor (Patrol-tier; anomaly detection on FC log distributions to catch collusion/correlation, ~1-2 weeks). Survival-window registrar (typed event-state-machine, ~1 week).

**Buildability estimate.** ~4-6 engineer-weeks beyond shared substrate.

**What could kill it.** Independence-auditor recursion (who audits the auditor? — this is D7-U-1's own load-bearing open question with no dominating answer). FC-graph cost at high parallelism is untested. Survival-window calibration is corpus-thin (how long does an FC stay "fresh" before re-falsification is required?). Opposing-side gaming under F47 Goodhart (the opposing side learns to falsify weakly so things compound). Operator-as-opposing-side scalability at greenfield day-0 (F42/F53 — does the operator actually exercise enough adversarial pressure?).

**Practitioner verdict.** Mechanically clean; **practitioner-thin**. D7-U-1's falsifier measures KL divergence of opposing-side `kind` distributions — substrate-emitted, mathematically rigorous, but not legibly tied to software-quality outcomes a practitioner experiences.

---

## Three observations across the 10 candidates

### Observation 1: substrate cost varies by ~40x

GF-M (~1-2 weeks of candidate-specific work) vs. BF-L (~6-12 engineer-months). This is a real range and it should drive your pressure-testing order — try the cheap ones first, only escalate to BF-L if smaller candidates fail and the failures specifically suggest the Codebase Model is needed.

### Observation 2: practitioner-thin clusters in the unified-attempts

3 of 4 unified-attempts (U-A, U-B, D7-U-1) are mechanically-rigorous but their falsifiers measure substrate-emitted distributions rather than software-quality outcomes. This was the Phase 8 domain-practitioner audit's load-bearing finding. The lean-evals will mechanically pass or fail; you should weight practitioner-felt scenarios heavily when deciding which to actually trust.

U-C is the unified-attempt with the strongest practitioner-relevance score, though it's also the most expensive of the four to build.

### Observation 3: mandate-aligned candidates are stronger evidence

Per the Phase 8 audit: the top three practitioner-relevance scores were GF-C, BF-S, BF-M (all mandate-aligned). If DEC-1.a holds ("no methodology serves both mandates"), the recommendation is to ship one mandate-aligned candidate per mandate: probably BF-S, BF-M, or BF-L for brownfield (depending on codebase size), and GF-C or GF-M for greenfield (depending on whether cold-start is the hardest part).

If DEC-1.a falls (a unified-attempt passes cleanly per-mandate without invoking escape-hatches), the recommendation is the unified-attempt that achieves practitioner-pass-cleanly, not just mechanical-pass-cleanly. The strength gradient in the cross-candidate evaluator-brief makes this distinction explicit.

## What's next

This file gives you the side-by-side framework but does not include per-candidate Mermaid diagrams of the methodology cycles, the discipline bindings, or the substrate compositions. Those are the next batch (items 5-6 from my previous recommendation) and should be produced once you've signed off on the vocabulary, paradigm, and substrate framing in this guide.

If anything in the four files reads wrong, fix it before I produce the diagrams. The diagrams will inherit the framework.
