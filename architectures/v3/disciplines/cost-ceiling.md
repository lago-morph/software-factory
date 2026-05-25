# Discipline: Cost-ceiling enforcement

Hard cost ceilings on tokens, wall-clock, and tool-call count are substrate-enforced, non-optional, declared up-front; the substrate kills the cycle at ceiling without graceful-degradation. The discipline operationalises D-5 (brief §4.1). CTR-E1 (Cherny $100K+/mo vs $500–5000/day) treats variance as configuration; the *non-optional* property survives. CTR-E6 (CaMeL ~7-point utility tax, followup 08 §3) is admitted as cost, not hidden as discount.

## Named-by

All 10 tracks; D-5 marked `accepted` or `accepted-with-justification` across the board.

- `GF-S` — *"Substrate kills the cycle at ceiling — no graceful-degradation-mode (which is a CTR-E6 CaMeL utility-tax-style hidden cost that substrate-first refuses to absorb silently)."* [greenfield-substrate-first.md](../tracks/greenfield-substrate-first.md) §1.S4.
- `GF-M` — Regime A's paraphrase fan-out is the primary cost multiplier; ceiling caps it. *"CTR-E6 sharpening acknowledged: substrate safety primitives have non-zero cost, and the cost ceiling must explicitly admit them."* [greenfield-methodology-first.md](../tracks/greenfield-methodology-first.md) §1.3 / §4 D-5 / §7 OQ-T2.
- `BF-S` — *"Brownfield's parallelism (Stripe 1,300 PRs/week per report 35; Cherny $100K/month per CTR-E1) makes cost ceilings load-bearing. The substrate's perimeter (S-5) is the enforcement point."* [brownfield-substrate-first.md](../tracks/brownfield-substrate-first.md) §4 D-5.
- `BF-M` — *"Per-cycle budget pre-declared per work-unit-class. CTR-E1's 10× cost variance and CTR-E6's CaMeL ~7-point utility tax are accepted as inputs to ceiling calibration; the ceiling itself is non-optional."* [brownfield-methodology-first.md](../tracks/brownfield-methodology-first.md) §4 D-5.
- `BF-L` — *"Ingestion phase has higher cost ceiling (one-time, deep) than work-loop cycles; both are enforced."* [brownfield-legacy-ingestion-first.md](../tracks/brownfield-legacy-ingestion-first.md) §4 D-5.
- `GF-C` — cold-start ceilings are easy because per-cycle scope is bounded; graduates with work-unit-class declaration. [greenfield-cold-start-first.md](../tracks/greenfield-cold-start-first.md) §4 D-5.
- `U-A` — *"Cost-ceiling breach is a substrate-fired re-entry trigger (per the re-entry registrar). The default is preserved; the addition is where the breach fires the gate (at the interval boundary, not at the workflow boundary)."* [unified-A.md](../tracks/unified-A.md) §4 D-5.
- `U-B` — declared per layer; per-layer ceiling, not flat. [unified-B.md](../tracks/unified-B.md) §4 D-5.
- `U-C` — per-distance ceilings: anchor-mutation queue carries higher ceiling than near-anchor cycles. [unified-C.md](../tracks/unified-C.md) §4 D-5.
- `D7-U-1` — *"Cost ceiling is the FC's `refutation-attempt.budget` field."* [d7-u-1-prohibit-interval-escrow.md](../bias-guards/phase-3/d7-blind-axis/d7-u-1-prohibit-interval-escrow.md) §4 D-5.

## Corpus motivation

- **D-5** in brief §4.1.
- **CTR-E1** ([contradictions.md](../contradictions.md)) — cost variance, Cherny vs noosphr 10× spread.
- **CTR-E6 / followup 08 §3** — CaMeL utility tax (~7-point measured).
- **F31** (minimum-adapter principle, substrate safety floor) in [failure-modes-v3.md](../failure-modes-v3.md).
- **Report 35** — Stripe 1,300 PRs/week brownfield industrial scale anchor.

## Open questions

- **Per-cycle flat vs per-phase / per-distance / per-layer / per-interval / per-work-unit-class.** Every track that goes beyond flat picks a different parameterisation, matching its organising axis.
- **GF-M §7 OQ-T2:** "Paraphrase fan-out cost vs cost ceiling (D-5) interaction is concrete and unresolved" — if cost is Nx single-cycle and ceiling is flat, throughput is sharply bounded. CTR-E1's 10× range has no methodology-side resolution.
- **U-A §7 OQ-6:** combined cost of immutable logging + cross-family judging + STIR-cascade reflection across high-parallelism interval graphs is *not corpus-measured*. The substrate-cheap thesis (Round-2 / D-7) may not survive this combination.
- **BF-L §7 #3:** Maintenance-loop cadence — too slow → F34 bites; too fast → D-5 bites. Corpus has no empirical anchor.

## Substrate-enforcement options

- `GF-S` `S4 cost ceilings` (per-cycle and per-day, three axes: tokens, wall-clock, tool-call-count).
- `BF-S` `S-5 perimeter` enforces ceiling at trifecta layer.
- `U-A` `policy mediator` fires breach as re-entry trigger.
- `D7-U-1` `FC.refutation-attempt.budget` per artifact.

Disciplines are distinct from these primitives.
