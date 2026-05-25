# Discipline: Lethal-trifecta closure / closure-first

Production credentials, network access, and tool surface are *substrate-default-disabled*; explicit declarations escalate to a more-restricted closure profile rather than a more-permissive one; perimeter typing (CaMeL-class typed-interpreter) replaces probabilistic guards on cross-sandbox calls. The discipline operationalises Shapiro R1-R5 hardening rules at the substrate layer and refuses to rely on per-Claw discipline (F44 / F53 / F56).

## Named-by

All 10 tracks (`explicit-named`).

- `GF-S` `S1 sandbox (closure-first; substrate-default-off for production scissors)`. *"Production-credentialled scissors (F44: R1 read-anything-but-only-draft / R2 thumbprint every artifact / R3 do-not-give-production-scissors / R4 isolated env / R5 disconnect-by-default) are substrate-disabled by default in greenfield."* [greenfield-substrate-first.md](../tracks/greenfield-substrate-first.md) §1.S1 / §1.S8.
- `BF-S` lethal trifecta is *constitutive of brownfield, not optional*. *"F44 the perimeter must be substrate-default (production-scissors-off, read/write asymmetric), not per-Claw discipline. F53 generalizes the argument."* [brownfield-substrate-first.md](../tracks/brownfield-substrate-first.md) §0 reason 3 / §1.1 S-5.
- `BF-L` *"The model's `production-access-surface` view + substrate-enforced production-scissors-off makes the Replit failure shape structurally not-available, rather than instruction-shaped."* [brownfield-legacy-ingestion-first.md](../tracks/brownfield-legacy-ingestion-first.md) §2.3 F56.
- `BF-M` *"Production-scissors default-off (F44); methodology does not relax it."* [brownfield-methodology-first.md](../tracks/brownfield-methodology-first.md) §2.5 / §3.
- `GF-C` first build cycle: *"Production scissors (F44) are OFF; the cycle ships to a sandbox only. The substrate enforces the production-scissors-off default per F44 mitigation."* [greenfield-cold-start-first.md](../tracks/greenfield-cold-start-first.md) §1.2 sub-phase C / §5 protection #4.
- `GF-M` Substrate-level default-off required; methodology does not relax it. [greenfield-methodology-first.md](../tracks/greenfield-methodology-first.md) §1.3 / §2.9 F44.
- `U-A` `EscrowInterval.policies.sandbox: bwrap+seccomp | container; approval-gate: required` at production-touching intervals. [unified-A.md](../tracks/unified-A.md) §1 / §2 F12/F33/F44 / §5.3.
- `U-B` L4 layer: production-scissors-default-off (F44); L0 standards include AILCCP Sensitive-Action Approval Gate. [unified-B.md](../tracks/unified-B.md) §1 / §2.5.
- `U-C` anchor object's `mutation-protocol` field forces production-scissors prohibition for any anchor whose content includes production-touch. [unified-C.md](../tracks/unified-C.md) §2 F12/F44.
- `D7-U-1` FCs on production-touching artifacts mandate `deterministic-checker` opposing-side; CaMeL-style typed-interpreter; substrate default-off production-scissors. [d7-u-1-prohibit-interval-escrow.md](../bias-guards/phase-3/d7-blind-axis/d7-u-1-prohibit-interval-escrow.md) §2 F12/F33/F44.

## Corpus motivation

- **F12 / F33 / F44 / F56** in [failure-modes-v3.md](../failure-modes-v3.md) — lethal-trifecta cluster, brownfield-critical.
- **Report 32 §8.2** — Shapiro R1-R5 hardening rules.
- **Report 05** — Willison lethal-trifecta framing.
- **Followup 08 §3** — CaMeL paper-body, NORMAL/STRICT typed-interpreter modes, ~7-point utility tax.
- **Followup 10 §3 (G14)** — Replit prod-DB wipe under explicit code freeze (the empirical anchor for F56 / F53).
- **Report 23** — Anthropic Skills closure rule (zero network access by runtime fiat).

## Open questions

- **CTR-C9** ([contradictions.md](../contradictions.md)) — Anthropic zero-network closure vs "dreaming" overnight research. GF-S resolves by treating dreaming as a separate capability profile that the substrate gates separately. BF-M §7 #8 flags it as Phase-5-unresolved.
- **CaMeL utility-tax (CTR-E6) acceptance criterion.** Where does it apply? BF-M §7 #3: "what counts as production-adjacent is a policy boundary, not a methodology decision."
- **Anchor mutation as itself a production-touching action.** U-C makes anchor-edit always L4 with named-human approval; this is the discipline's logical extension (modifying the closure is itself the most-restricted operation).

## Substrate-enforcement options

- `GF-S` `S1 sandbox` (closure-first; capability grants per-cycle manifest) + `S8 perimeter typing`.
- `BF-S` `S-5 perimeter` — substrate-default scissors-off, read/write asymmetric, CaMeL-class typed-interpreter, cross-model judge, guard-bypass detection.
- `U-A` interval-policy `sandbox` + `approval-gate`.
- `U-C` anchor `mutation-protocol` field as substrate-typed scissors-policy declaration.
- `D7-U-1` FC `opposing-side.kind: deterministic-checker` on production-touching artifacts.

Disciplines are distinct from primitives.
