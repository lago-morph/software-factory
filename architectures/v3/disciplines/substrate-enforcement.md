# Discipline: Substrate-enforced (not voluntary)

Critical invariants are enforced by the substrate's *refusal to advance*, not by operator or methodology-layer voluntary compliance. The cycle refuses to advance; the operator does not refuse-to-skip. Kahana's *voluntary-discipline fragility* (F53) is the load-bearing argument: any control assumed to be operator-applied or methodology-applied breaks under the time-pressure conditions where it is most needed. Replit-class incidents (followup 10 §3 G14) are the empirical anchor — 1,200 executives across 1,190 companies running production-DB-wipe scenarios under explicit code freeze.

## Named-by

All 10 tracks invoke F53 by name and use it to justify substrate-typing at least one control. Representative quotes:

- `BF-M` — *"All stage obligations are substrate-enforced, not operator-voluntary. The cycle refuses to advance, not the operator refusing-to-skip."* [brownfield-methodology-first.md](../tracks/brownfield-methodology-first.md) §2.5 F53.
- `U-B` — escrow primitive is *"the structural replacement for voluntary discipline (F53). It fires at the substrate's natural moment (interval-by-construction) regardless of operator cognitive budget."* [unified-B.md](../tracks/unified-B.md) §1 + §0 reason 2.
- `D7-U-1` — *"A falsification commitment is not a discipline — it is a typed declaration, written at artifact-creation time, mechanically refused by the substrate if absent. Structural-not-voluntary property comes from substrate refusing to compound un-declared artifacts."* [d7-u-1-prohibit-interval-escrow.md](../bias-guards/phase-3/d7-blind-axis/d7-u-1-prohibit-interval-escrow.md) §0 reason 4.
- `GF-S` — substrate-triggered controls preferred to operator-discipline at every primitive ([greenfield-substrate-first.md](../tracks/greenfield-substrate-first.md) §1.S5 / §1.S8 / §1.S9 / §4 / §5.4).
- `BF-S` — F53 is the explicit argument against putting closures in methodology ([brownfield-substrate-first.md](../tracks/brownfield-substrate-first.md) §0 reason 3, §1.1 S-5).
- `GF-C` — *"STIR-in-the-interval implemented as a substrate-triggered structural pause, not as voluntary operator discipline. This is the day-0 mitigation of F53"* ([greenfield-cold-start-first.md](../tracks/greenfield-cold-start-first.md) §1.1 primitive 4).

## Corpus motivation

- **Report 30 §3** — Kahana voluntary-discipline fragility; STIR critique.
- **Report 31 §1** — Kahana three-part RSI test (durable self-mod + compounding + limited gating).
- **Followup 10 §3 (G14)** — Replit DB wipe under explicit code freeze; Moltbook 1.5M API keys via missing RLS.
- **Report 32 §8.2 (R1–R5)** — Shapiro hardening rules: read-anything-but-only-draft / thumbprint / no-production-scissors / isolated env / disconnect-by-default.
- **F53** in [failure-modes-v3.md](../failure-modes-v3.md) — voluntary-discipline-fragility, Kahana-class.

## Open questions

- **The operator's response to a substrate-fired prompt is itself voluntary.** U-B §7 OQ-PLEF-5 names this directly: the substrate can fire STIR but cannot make the operator read it. The "F53 residual" remains.
- **Where does substrate-enforcement stop and Schillace F52 (Tempting-Wrong-Hybrid) start?** Substrate enforcement is not free of utility tax; CTR-E6 ~7-point CaMeL tax is the corpus's measured cost. Accreting *more* substrate controls trades against F52.
- **D7-U-1's "honest concession":** opposing-side topology survives F53 structurally but does *not* close F42 (cognitive escrow negligence) at substrate; escrow-flavoured tracks (U-A, U-B) are stronger there. The "carry both" recommendation lives because the two F53 mitigations are not interchangeable.

## Substrate-enforcement options

This discipline is *meta-* to most primitives — it is the rule that the others MUST be substrate, not policy. Concrete primitives that exemplify it across tracks:

- `GF-S` — S1 sandbox (closure-first default-off), S4 cost ceilings (substrate-killed at ceiling), S5 watchdog tiers, S8 guard mediator (four deterministic guards), S9 eligibility classifier (substrate-typed, not policy).
- `BF-S` — S-5 perimeter (substrate-default scissors-off, not per-Claw discipline).
- `U-A` — policy mediator (refuses to close intervals with failed policies).
- `D7-U-1` — compounding gate (substrate refuses to make A available to B without survived FC).

Disciplines are distinct from primitives; this one is closer to a *constructional rule* about how primitives are built than to a primitive itself.
