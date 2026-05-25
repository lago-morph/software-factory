---
guard: cfo
target: draft-unified-synthesis
phase: 3.2
based-on-commit: 200ad3e
based-on-date: 2026-05-25
---

# Phase-3.2 CFO critique — unified draft

## §1 Persona stance

I am the CFO. My job is to read this unified architecture against three numbers: the *unit cost per work-unit* it imposes on the substrate, the *capital cost* to build the substrate at the granularity it specifies, and the *operating-cost variance* it introduces as parallelism scales. The draft repeatedly leans on a "substrate-cheap" thesis (D-7, Round-2 C16, OpenHands V1's sub-millisecond persist) to justify promoting EscrowSurface, AttributedEventLog, and TypedJudgeCall to substrate primitives at *per-interval* granularity. That thesis was priced against trajectory-capture alone, on one benchmark, at one parallelism level. The draft now stacks four additional substrate-cost vectors on top of that base, *multiplied* by per-interval granularity (DPU-4 option U-A), *multiplied* by the unified factory's obligation to maintain two evidence streams in parallel.

## §2 Top cost findings

### F-CFO-1. TypedJudgeCall × per-interval granularity = ~2.8× LLM bill multiplier (HIGH)

**Target.** ROBUST-U5 ("`TypedJudgeCall` with sub-shape policy"; cross-family at high-stakes) + DPU-6 (per-interval provider-property routing) + DPU-4 U-A.

**Cost model.** The closest empirical anchor in the corpus is CaMeL: **2.82× input tokens and 2.73× output tokens vs. native tool calling**. TypedJudgeCall imposes a *second* model call per high-stakes interval, and ROBUST-U5 mandates *cross-family* (different vendor) for those calls. A per-interval substrate with N intervals per cycle therefore stacks: (a) base planner cost, (b) ~2.8× CaMeL-shape overhead if CaMeL is the trifecta closure, (c) one cross-family judge call per high-stakes interval, (d) STIR-cascade reflection calls. Cherny's $100K/month/engineer anchor (CTR-E1) is from a *single-call-per-cycle* regime; multiplying base by 2.8× × (judge-fanout) × (interval-count) puts a 1,300-PR/week Stripe-scale unified factory in the $300K–$1M/engineer/month range.

### F-CFO-2. ROBUST-U9 immutable-AttributedEventLog at per-interval granularity is the cost vector the corpus has *least* measurement for (HIGH)

**Cost model.** D-7's empirical basis is OpenHands V1's sub-ms persist + 7.4ms crash recovery — *on 433 SWE-Bench Verified replays at one parallelism level*. The brief's footnote concedes the measurement *"generalizes to other substrates only insofar as event-sourced persistence layers are comparable."* The unified architecture extends this primitive in three ways the OpenHands measurement does *not* cover: (a) **signed / content-addressed envelopes** (cryptographic signing cost per event — typically 100×–1000× per signed event); (b) **per-interval granularity** (event count multiplied by the *interval count per cycle*, which U-A explicitly allows to be unbounded); (c) **AILCCP three-controls compliance** for board-visibility — requires retention horizons, search/audit indices, tamper-evidence — *none of which OpenHands V1 measures*. The substrate-cheap thesis here is *one anchor measurement extrapolated three steps beyond its tested scope*.

### F-CFO-3. EscrowSurface STIR-cascade at per-interval granularity has *negative* CaMeL-shape evidence (MEDIUM-HIGH)

**Cost model.** The only corpus-measured *substrate-safety-with-utility-cost* anchor is CaMeL: **77% with provable security vs. 84% undefended — a 7-point utility tax**. CaMeL's STRICT mode raises *benign-policy-triggering rate from 33.87% → 53.23%*. STIR cascade is structurally similar: substrate-invoked user-confirmation/reflection at policy moments. The corpus' read: substrate-safety primitives carry **per-call utility tax (~7%) + per-call latency**. Per-interval STIR at high parallelism *amplifies* both costs. F-ANCHOR-2 already flags the substrate-primitive promotion as single-source; the cost model is the missing budget. U-B OQ-5 explicitly: "operator's *response* to substrate-fired escrow is itself voluntary — substrate cannot ensure the operator reads the reflection question" — i.e., the substrate pays the cost *whether or not the operator engages*.

### F-CFO-4. Unified factory has *additive* not *shared* mandate-specific evidence streams (MEDIUM-HIGH)

**Cost model.** Greenfield bench evidence is *high-cardinality, low-volume* (scenario sets, K=5 consistency runs, prompt-paraphrase robustness matrices); brownfield codebase-model views are *low-cardinality, high-volume* (full AST + dependency graph + runtime traces). A unified factory that addresses *both* mandates simultaneously carries *both* streams — additively, not as a parameter on one stream. The "mandate is a parameter" claim hides a 2× storage and indexing cost the draft never books.

### F-CFO-5. Per-interval (U-A) vs per-layer (U-B) vs per-distance (U-C) is a 5×–50× capex/opex spread (HIGH)

**Cost model.** Cycle-level work units average single-digit per-cycle for slower architectures, 10s-100s for fanout architectures. Per-layer: fixed at 5. Per-interval (U-A): unbounded per cycle, with U-A OQ-1 explicitly *refusing to commit to a cadence*. **All five substrate primitives (U4-U10) instantiate per-typed-object.** Picking U-A's per-interval granularity multiplies *every* substrate-primitive cost by 10×–50× vs. per-layer for the same cycle work. The draft surfaces this as one of seven DPUs without naming the *cost magnitude*.

## §3 What's cost-defensible

**First**, the `DeterministicSpecLinter` (ROBUST-U7) is genuinely cheap: deterministic, fail-closed, NOT-an-LLM-judge. This primitive *does not* multiply by parallelism, *does not* invoke a model.

**Second**, the `RegimeClassifier` (ROBUST-U4) is cost-defensible *if* its inputs are deterministic features (interval kind / pace-layer / priors) and its output is a small typed verdict. Per-interval classification using *typed features* rather than LLM-judging the interval is cheap relative to the other primitives.

The cold-start L3-Augmentation default (ROBUST-U12) is cost-defensible — strictest defaults at day 0 means the cost-multiplier vectors above *only fire after the factory has measured graduation criteria*. The graduation-as-substrate-measured discipline (ROBUST-U14) is the right cost-control envelope, *if* the graduation thresholds include cost-per-work-unit metrics, which the draft does not currently mandate.

## §4 Concrete recommendations for Phase-3.4

1. **Add DPU-9: Substrate-primitive cost budget.** Before the user picks DPU-1/4/6, require an explicit Phase-3.4 cost-model exhibit: token-multiplier × storage-multiplier × signing/indexing-overhead × interval-cadence, anchored on the four named measurements. Frame DPU-4 granularity as *a cost-tier choice*, not an audit-trail choice.

2. **Split ROBUST-U9 into U-9a and U-9b.** U-9a = *append-only event log with content-addressed envelopes* (OpenHands-priced primitive). U-9b = *AILCCP-compliant signed/indexed/retention-bound attribution stream* (regulator-priced primitive). The draft currently elides these. The CFO position is that *U-9a is substrate, U-9b is methodology with substrate hooks*.

3. **Add a cost-graduation criterion to ROBUST-U14.** Steady-state regime promotion currently gates on K=5 consistency, paraphrase robustness, safety-incident severity. Add: **cost-per-work-unit must be measured and within the operator-declared ceiling for K consecutive cycles**. This makes D-5's cost-ceiling a substrate-fired regime-transition input, not just a substrate-fired re-entry trigger.

4. **Mandatory STIR-cascade backoff at high parallelism.** Tie ROBUST-U10's STIR cascade to a per-interval-class allowlist *and* a parallelism-aware backoff: at >K concurrent intervals, STIR drops from substrate-mandatory to substrate-offered.

5. **CFO objection to be recorded as a Phase-3.3 dispatch input.** The `X_UNM_G` and `X_UNM_B` cross-mandate adversarial briefs should each carry a clause: "if your attack lands *on cost grounds*, that is a valid landing." Cost *is* a feasibility constraint and should be in the adversarial scope explicitly.
