# Discipline: Deterministic-perimeter-at-authoring (spec lint)

Spec / intent / acceptance-criteria pass through *deterministic, rule-based linters* (EARS five-pattern grammar; INCOSE GtWR R7/R8/R9/R26/R35; requirement-count budgeter; contradiction-detector with multiple judges) *before* any LLM-judge runs. Deterministic checks are used where possible; probabilistic guards only where no deterministic option exists (F51 Ashby-deficiency); the number of deterministic wrappers is capped to avoid Schillace F52 (Tempting-Wrong-Hybrid).

## Named-by

- `GF-S` `S8 guard mediator` — *four mandatory deterministic guards* on every cycle's spec-input *before* the build agent sees it: GtWR vocabulary lint, contradiction-detector, requirement-count budgeter, perimeter typing. *"The substrate refuses to accrete more control layers around the LLM than the four named primitives."* [greenfield-substrate-first.md](../tracks/greenfield-substrate-first.md) §1.S8.
- `GF-C` *"GtWR/EARS linter is not an LLM-as-judge; it is a deterministic rule engine. Per CTR-D6 (sycophancy-as-defensive-wrap induces false positives), this avoids the LLM-judge-sycophancy trap at the authoring boundary."* [greenfield-cold-start-first.md](../tracks/greenfield-cold-start-first.md) §1.1 primitive 2 / §5 protection #1.
- `GF-M` *"Deterministic lint against GtWR R7/R8/R9 (mitigating F38 vocabulary lint debt) runs at this gate; failures are returned to the operator, not silently rewritten by an agent."* *"This track has only one deterministic wrapper (the GtWR linter at Phase 1) and one cross-model check (paraphrase divergence). Everything else is the cycle itself. This is a deliberate guard against control-layer accretion."* [greenfield-methodology-first.md](../tracks/greenfield-methodology-first.md) §1.1 / §2.9 F52.
- `BF-M` Stage 3 — *"Deterministic GtWR R7/R8/R9 lint on the change-intent block; complexity-diagnosis field on the change-intent block."* Stage 7 — *"Stage-7 perimeter is deterministic + scenarios-from-codebase, not LLM-judge-only."* [brownfield-methodology-first.md](../tracks/brownfield-methodology-first.md) §1.1 stage 3 + 7 / §2.5 F38 + F51.
- `U-A` `EscrowInterval{kind: spec-author}` interval policy mandates *"deterministic EARS/GtWR lint (F38 mitigation) + LLM-judge with `judge-diversity: different-family` (F36/F37/F46 mitigation) + complexity-diagnosis field at open (F39 mitigation)."* [unified-A.md](../tracks/unified-A.md) §5.3.
- `U-B` *"Layer-invariant checks are deterministic, not LLM-judged. GtWR linting, EARS conformance, AILCCP control presence — all deterministic. Ashby-deficient probabilistic guards (F51) are avoided at L0/L2 layer boundaries."* [unified-B.md](../tracks/unified-B.md) §2.5 / §5.5.
- `U-C` operator supported by RE/SE-grounded prompt scaffold derived from INCOSE GtWR C1-C15 and EARS at intent authoring. [unified-C.md](../tracks/unified-C.md) §5 step 0.
- `BF-S` `S-5 deterministic perimeter` (with cross-model judge as separate primitive). [brownfield-substrate-first.md](../tracks/brownfield-substrate-first.md) §1.1 S-5.
- `BF-L` `inferable` — substrate enforces invariants extracted from tests/types/runtime assertions/schema constraints, but does not separately name an authoring linter.
- `D7-U-1` `deterministic-checker` is one of four `opposing-side.kind` values; spec FCs include GtWR/EARS deterministic check. [d7-u-1-prohibit-interval-escrow.md](../bias-guards/phase-3/d7-blind-axis/d7-u-1-prohibit-interval-escrow.md) §2 F36/F37/F38/F39.

## Corpus motivation

- **Report 25 §2 (EARS) + §3 (INCOSE GtWR)** — Mavin five-pattern + R7/R8/R9/R26/R35 + INCOSE Complexity Primer principle 12.
- **Report 26 §3.4 / §6.1-6.2** — Yang et al. (98.7%→85.0% instruction-following ceiling as 1→19 reqs); Larbi et al. (73.8%→6.7% on contradictory prompts; MCC ≤ 0.55).
- **F36 / F37 / F38 / F39 / F51 / F52** in [failure-modes-v3.md](../failure-modes-v3.md).
- **Report 28 Letter 11 (Schillace)** — Tempting-Wrong-Hybrid; cap on deterministic-wrapper accretion.

## Open questions

- **How many deterministic layers can accrete before F52 fires?** GF-S says "four guards full stop"; GF-M says "only one deterministic wrapper"; U-B §7 OQ-PLEF-8 raises the F52-risk of pace-layer-as-deterministic-wrapper. The corpus does not specify a numerical ceiling; the discipline is *some discipline of restraint exists*, not *the precise restraint*.
- **Where deterministic options run out and probabilistic begins.** Larbi's MCC ≤ 0.55 says contradiction-detection cannot be closed by LLM-judge; the corpus does not say whether a heavier deterministic checker (theorem-prover, SAT) could.
- **Sycophancy-as-defensive-wrap (CTR-D6).** GF-C names this as the reason to keep authoring-boundary checks deterministic; whether the same risk applies to other-layer LLM-judges is unresolved.

## Substrate-enforcement options

- `GF-S` `S8 guard mediator` — four-guard primitive.
- `BF-S` `S-5 deterministic perimeter`.
- `U-A` `gate.deterministic` policy slot on every interval.
- `U-C` `contradiction-flag` in distance estimator.

Disciplines are distinct from primitives.
