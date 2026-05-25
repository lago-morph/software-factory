# Discipline: Regime / eligibility classification

Lights-out applies *only* over a declared automation-eligible surface (per work-unit-class, per region, per interval, per layer, per anchor-distance, per artifact-kind, depending on the architecture's organising axis). The classifier itself is substrate-typed, audit-able, and its drift triggers re-entry. The discipline operationalises brief §2.1 option (c)+(b) and resolves CTR-A4 (vocabulary discipline: "lights-out" ≠ L5).

## Named-by

All 10 tracks. Near-universal adoption of brief §2.1 option (c)+(b).

- `GF-S` `S9 eligibility classifier` (substrate-resident, classifies each work-unit as `automation-eligible` / `augmentation-required` / `escalate`). *"If classification is policy, drift is invisible; if classification is substrate-typed, drift is logged."* [greenfield-substrate-first.md](../tracks/greenfield-substrate-first.md) §1.S9 / §2.A.
- `BF-L` model-driven classifier per region (test coverage + telemetry density + churn cadence + Caremark/RSI exposure). [brownfield-legacy-ingestion-first.md](../tracks/brownfield-legacy-ingestion-first.md) §1 / §2.1.
- `U-A` classifier-as-substrate primitive; runs inside an interval; audit-able. [unified-A.md](../tracks/unified-A.md) §1.
- `U-C` distance-gated dispatcher (near / mid / far): three regimes by anchor-distance. [unified-C.md](../tracks/unified-C.md) §1 primitive 3.
- `GF-C` graduation protocol — work-unit-classes promote from cold-start L3-Augmentation to per-class L4-lights-out by measured bar clearance. [greenfield-cold-start-first.md](../tracks/greenfield-cold-start-first.md) §1.3.
- `BF-M` per-(work-unit-class × stage) bar clearance; bar source per cell. [brownfield-methodology-first.md](../tracks/brownfield-methodology-first.md) §2.1.
- `GF-M` Regime A (spec-discovery, L3-Augmentation) → Regime B (spec-anchored execution, L4 for promoted slices). [greenfield-methodology-first.md](../tracks/greenfield-methodology-first.md) §1.
- `BF-S` *"L4 reachable for the specific work-unit-classes where S-2/S-3 give confident inputs"*; Jaymin's brownfield L3 ceiling accepted as default with substrate evidence as eligibility gate. [brownfield-substrate-first.md](../tracks/brownfield-substrate-first.md) §2.1.
- `U-B` per-layer regime: L4 at code; L3-Augmentation at layer transitions. [unified-B.md](../tracks/unified-B.md) §2.1.
- `D7-U-1` per-artifact-kind regime, conditioned on opposing-side independence and stability. [d7-u-1-prohibit-interval-escrow.md](../bias-guards/phase-3/d7-blind-axis/d7-u-1-prohibit-interval-escrow.md) §2.

## Corpus motivation

- **[Brief §2.1](../00-brief-v3.md)** — options (a)/(b)/(c)/(d).
- **[CTR-A1 / A4 / A5 / H10](../contradictions.md)** — L5-anti-pattern empirical claim cluster; vocabulary mapping discipline.
- **Report 09 §5.5** — Jaymin Augmentation (K=5 ≥70%, paraphrase ≥3/5) vs Automation (K=5 ≥90%, paraphrase 5/5, zero medium+ safety) thresholds.
- **[Glossary §0](../00-brief-v3.md)** — "lights-out" = no human in per-cycle inner loop for automation-eligible work units.
- **F57** in [failure-modes-v3.md](../failure-modes-v3.md) — design-authority erosion / convenience reclassifies stakes (the failure mode if classification is policy not substrate).

## Open questions

- **What's the right granularity of eligibility?** Per work-unit-class (BF-S), per region (BF-L), per interval (U-A), per layer (U-B), per anchor-distance (U-C), per artifact-kind (D7-U-1). The axis-choice itself parameterises this.
- **Classifier accountability.** U-A §7 OQ-2: *"the classifier itself is the architecture's most powerful actor. F57 is amplified by giving so much weight to one substrate primitive."* Audit discipline corpus-light.
- **Can the classifier be gamed?** U-C §7 OQ-1: F47 Goodhart on the distance estimator — agents may learn to phrase work units to land just below τ_low. Patrol-tier watchdog is the proposed catch but its sufficiency is unmeasured.
- **What's the minimal viable bench / scenario set for the classifier to flip a regime?** GF-S §7 #1; GF-C §1.3 (bench saturation): N and M deferred to Phase-6 ADR.

## Substrate-enforcement options

- `GF-S` `S9 eligibility classifier` — versioned configuration; Patrol monitors classifier-output distribution.
- `BF-L` model-driven classifier — eligibility function takes coverage + telemetry + churn + RSI exposure.
- `U-A` `classifier` — interval-bracketed; its decision is logged and overrideable at re-entry interval.
- `U-C` `distance-gated dispatcher` — substrate decision table; metric accuracy itself watchdog-monitored.
- `D7-U-1` per-FC `survival-window` — registrar flags downstream artifacts for re-falsification on expiry.

Disciplines are distinct from primitives.
