---
guard: cfo
target: draft-brownfield-synthesis
phase: 3.2
based-on-commit: e02d0ba
based-on-date: 2026-05-25
---

# Phase-3.2 CFO critique — brownfield draft

## §1 Persona stance

I am the person who signs the inference bill, runs the unit-economics model for a brownfield factory engagement, and explains the cost curve to a board that has already approved a number. From that seat, the brownfield synthesis is the *more* cost-exposed of the two drafts — it commits to a five-view continuously-maintained substrate, cross-family judge as default, AttributedEventLog on every cycle, and a CaMeL-class typed-interpreter perimeter, all while invoking the Stripe 1,300-PRs/week anchor. The draft acknowledges D-5 cost ceilings but treats them as a *parameter*, not as a model that has been *solved*.

## §2 Top cost findings

### Finding C1 — Cross-family judge at Stripe scale: the unit-economics aren't shown (HIGH)

**Target.** ROBUST-B8 makes cross-family judge the brownfield default at every cycle. DPB-8 quotes the multiplier verbatim: *"cross-family is ~2× per-cycle inference; same-model-different-role is ~1.1×"* (BF-M §7 OQ-T2). ROBUST-B11 cites Stripe's 1,300 PRs/week.

**Cost model.** 1,300 PRs/week × 52 weeks = 67,600 PRs/year per codebase. At the high end of CTR-E1 (Cherny ~$5/PR), the *builder-only* inference is already $6–7M/year/codebase. Cross-family judge at every cycle is a 2× multiplier on the *review* leg (Stage 6 of an 8-stage cycle, conservatively 25-40% of per-cycle inference). Net: cross-family-on-every-cycle adds **25-40% to the inference bill** vs. same-model-different-role. At Stripe scale that's $1.5-3M/year/codebase incremental. The draft surfaces this as DPB-8 but ROBUST-B8 already pre-loads the default.

**Severity HIGH** because the draft pre-locks the expensive option as the default; if Husain/Shankar's "same-model judging is fine when task differs" (CTR-D7) holds, the architecture is overpaying by 25-40% on the line item with the largest absolute dollar volume.

### Finding C2 — Incremental codebase-model maintenance on every commit is a hidden recurring cost (HIGH)

**Target.** ROBUST-B3/B4 mandates five sub-stores incrementally maintained per commit. DPB-4's BF-S/BF-L stance is *"continuously maintained on every commit."*

**Cost model.** At Stripe scale, 1,300 agent PRs/week ≈ 185 merges/day before counting human PRs. Each merge fires: codebase-index incremental update (LSP-style re-indexing); dependency-graph delta (*transitively non-local on large codebases*); invariant view refresh; attribution-store write to AttributedEventLog; Patrol-tier scan against invariants for F34 drift.

On a 1M-LOC codebase, an incremental dependency-graph update with type information is not free — the corpus offers no anchor for the per-commit cost. BF-L OQ-T3 *itself flags* "Model staleness vs. cycle latency tradeoff. The maintenance loop's cadence is a tunable. Too slow → F34 bites; too fast → cost ceiling pressure (D-5) bites. **Open: what's the empirical anchor for cadence?**" The draft commits the architecture to the substrate before knowing this number.

### Finding C3 — AttributedEventLog × every cycle × cross-family × CaMeL boundary breaks the substrate-cheap thesis (MEDIUM-HIGH)

**Target.** ROBUST-B10 mandates immutable AttributedEventLog on every cycle. ROBUST-B5 mandates CaMeL-class typed-interpreter perimeter at production-adjacent steps. CTR-E6 directly contests Round-2's substrate-cheap thesis: *"77% of tasks with provable security vs. 84% with an undefended system"* — a ~7-point utility tax.

**Cost model.** CaMeL's tax is a *utility* tax with *fat-tailed retry cost* — when CaMeL forces the Privileged LLM to *"generate different code to fix the error,"* each retry is a full inference round-trip. At 1,300 PRs/week, a 7-point baseline tax with fat-tailed retry distribution can translate to a 10-15% inference bill inflation *on top of* whatever fraction of cycles hit production-adjacent regime.

### Finding C4 — Telemetry bootstrap (DPB-9) under-prices operator labor (MEDIUM)

**Target.** ROBUST-B13 names *"if none exists, the first work-unit-class becomes adding telemetry (self-bootstrap step per BF-S §5)."* DPB-9 surfaces the question but does not resolve it.

**Cost model.** Adding telemetry to a 1M-LOC brownfield codebase that *currently has none* is a 3-12 person-month operator-engineering project. The architecture treats it as "the first cycle" — but the first cycle has *no S-3 evidence* to clear any L4 threshold, so it runs at L3-augmentation with full operator review. This is a one-time setup cost the architecture invokes casually but does not honestly price. For mid-market codebases, this is the *gating cost of adopting the factory at all*.

### Finding C5 — Where in the CTR-E1 10× band does this architecture land? (HIGH — meta-finding)

**Target.** CTR-E1 is the corpus' brightest cost anchor: $100K+/month per-engineer (Cherny) vs. $500–$5000/day per seat (noosphr) — a 10× spread. The draft does not place itself in the band.

**Cost model.** The architecture's commitments add up compoundly:
- Builder baseline: 1.0×;
- + Cross-family judge default (B8): 1.25-1.40×;
- + CaMeL boundary at production-adjacent (B5): 1.10× headline, 1.15-1.25× with retry tail;
- + Continuous codebase-model maintenance (B3/B4): unknown;
- + AttributedEventLog write amplification (B10): 1.02-1.05×.

Compounded, the architecture lands ~1.5-2× the *baseline* inference bill before counting model-maintenance. That puts it *unambiguously* at the Cherny end of CTR-E1. The architecture is implicitly a **$100K+/engineer/month architecture**.

## §3 What's cost-defensible

**(1) The hard-ceiling discipline itself (D-5) is correctly framed as non-optional and per-work-unit-class.** ROBUST-B11 names *"per-cycle and per-phase budgets... configurable per work-unit-class."* DPB-4's flagging of model-maintenance cadence as a tunable parameter honestly admits the uncertainty.

**(2) The legacy-ingestion-as-one-time-and-incremental framing (ROBUST-B13) is correctly amortized.** The cost shape — heavy day-0, lighter day-N — matches the actual technical reality. The split into ingestion / work / maintenance loops (BF-L) makes this cost-bookkeeping legible.

## §4 Concrete recommendations for Phase-3.4

1. **Add a §1.8 "Cost-anchored claims" subsection** placing the architecture explicitly in CTR-E1's 10× band. The synthesis must answer: *is brownfield-with-these-defaults a $100K-engineer-month architecture, a $5K-seat-day architecture, or something in between, and what fraction of that is builder vs. judge vs. substrate maintenance vs. CaMeL retry tail?*

2. **Promote DPB-8 (cross-family judge default) to wave-1 ADR, not wave-2.** The 25-40% inference-bill delta is the single largest tunable. Pair with **sample-rate cross-family** as an explicit option.

3. **DPB-4 (codebase-model continuity) ADR must include a per-commit incremental-maintenance cost estimate.** Force a numeric anchor — even an order-of-magnitude estimate — into the ADR template.

4. **ROBUST-B5 (CaMeL boundary) needs a "production-adjacent" definition with a quantified scope.** What fraction of cycles hit the production-adjacent regime?

5. **Add an explicit DPB-11 — "Telemetry-bootstrap operator-labor budget."** Phase-6 architecture specs should declare an explicit "telemetry prerequisite" floor.

6. **Add a compounding-cost calculator to Phase-8 lean-eval brief.** Produce a numeric multiplier — *"this architecture's per-cycle inference bill is N× a CaMeL-off / same-model-judge / per-cycle-reconstructed baseline."*

7. **DPB-10 (Compound knowledge store) needs a 5-year monotonic-growth retrieval-cost projection.** ~340K typed records on a 5-year horizon; retrieval/indexing on a 340K-record store is not free at per-cycle frequency.

The bottom line: the brownfield architecture is cost-defensible at the *direction* level but cost-naïve at the *magnitude* level. The corpus has the numbers; the draft has not yet done the multiplication.
