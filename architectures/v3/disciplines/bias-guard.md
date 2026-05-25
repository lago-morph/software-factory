# Discipline: Bias-guard / adversarial-review

Every load-bearing artifact is subjected to an *opposing-side* attempt to refute it — cross-model judge, deterministic checker, named human, or population vote — before downstream compounding is permitted. The discipline encodes the corpus finding that F1 (Hallucination Loop) / F27 (Circularity) / F46 (single-model review blindspot) / F48 (tacit collusion) are a single cascade with one mechanism: *no opposing side committed to falsifying the output*. Independence is **measured**, not declared — same-model self-review inherits the author's blind spots.

## Named-by

- `D7-U-1` (entire architecture; "Falsification Commitment" substrate primitive). Verbatim: *"All four canonical correlated-error failure modes share one mechanism: no opposing side was committed to falsifying the output. The substrate primitive (falsification commitment) is exactly the missing typed object the corpus needs."* — [d7-u-1-prohibit-interval-escrow.md](../bias-guards/phase-3/d7-blind-axis/d7-u-1-prohibit-interval-escrow.md) §0 reason 2.
- `BF-M` — stage-6 cross-model review constitutive. [brownfield-methodology-first.md](../tracks/brownfield-methodology-first.md) §1.1 (stage 6: *"Distinct-model reviewer (F46 mitigation per CJ Hess `kevin/carl`)"*), §2.5.
- `GF-M` — Regime A's paraphrase-divergence step IS the F37 in-cycle detector; Regime B uses cross-model review panel. [greenfield-methodology-first.md](../tracks/greenfield-methodology-first.md) §1.1 / §1.2 / §2.9.
- `GF-C` — cross-model judge mandatory at first cycles; both single-judge and cross-model run, escalate on disagreement. [greenfield-cold-start-first.md](../tracks/greenfield-cold-start-first.md) §1.2 sub-phase C / §5 protection #2.
- `U-A` — `EscrowInterval.policies.judge-diversity` slot; cross-family default at high-stakes intervals. [unified-A.md](../tracks/unified-A.md) §1.
- `U-B` — per-layer judge-diversity policy; cross-model at L4 builder review, same-model-different-role at intra-layer. [unified-B.md](../tracks/unified-B.md) §2.5 / §3.
- `U-C` — distance-gated dispatcher mandates cross-model at mid-distance; single-judge permitted near-anchor only. [unified-C.md](../tracks/unified-C.md) §1 primitive 3.
- `BF-S` — cycle-step 5 (cross-model judge), substrate enforces same-change cannot self-judge. [brownfield-substrate-first.md](../tracks/brownfield-substrate-first.md) §1.3.
- `BF-L` — F46 mitigation as substrate-level codebase-model + runtime-traces cross-model independent signal. [brownfield-legacy-ingestion-first.md](../tracks/brownfield-legacy-ingestion-first.md) §2.3.

## Corpus motivation

- **F1 / F27 / F46 / F48 cascade** — [failure-modes-v3.md](../failure-modes-v3.md) §8.2 cascade note.
- **Report 34 §6.2** — CJ Hess `kevin`/`carl` cross-model QC.
- **Report 23 §3.5** — Anthropic five specialist critics (Auto-Review subagent).
- **Followup 07 §3.6** — Husain/Shankar "same-model judging is fine when task differs" (the partial-corpus dissent).
- **Report 26 §6.1-6.2** — Larbi MCC ≤ 0.55 (single-judge contradiction-detection ceiling).
- **Report 02 / [CTR-C4](../contradictions.md)** — Attractor *do-not-unify* discipline.

## Open questions

- **Same-model-different-role vs cross-model-different-family is unresolved.** [CTR-D4 / D7 / D8](../contradictions.md) split. Most tracks insist cross-model at high-stakes; followup 07 says same-model is fine when the *task* differs — U-A and U-B accept it at lower-stakes intervals; GF-M and BF-M refuse it for greenfield-specific reasons (no out-of-distribution ground truth) or cycle-stage reasons (stage 6 cross-model insistence).
- **Cost of cross-model judging at high parallelism.** D7-U-1 §7 OQ-2 and U-A §7 OQ-6 both flag the corpus is empty on this; CTR-E6 CaMeL ~7-point utility tax is the closest empirical anchor.
- **"Independence" of judges is itself measurable but the measurement may collude.** D7-U-1 §7 OQ-1: "what if the measurement itself colludes?"

## Substrate-enforcement options

- **GF-S `S6 judge routing`** — substrate-typed judge call with model-family-tag, prompt-template ID, holdout-criterion reference. Substrate does not pick which judge shape is right (that is methodology) but makes the choice declared, auditable, reversible.
- **U-A `judge router`** — routes to same-model / different-role / different-family per interval-policy.
- **U-C `distance-gated dispatcher`** — routes to cross-model at mid-distance; near-anchor permits single-family.
- **D7-U-1 `opposing-side router`** — produces the actual judging surface; honours Attractor's do-not-unify.
- **D7-U-1 `independence auditor` (Patrol-tier)** — measures, not declares, judge independence.

Disciplines are distinct from these primitives by working-definition. The discipline *governs which primitive is fired when*.
