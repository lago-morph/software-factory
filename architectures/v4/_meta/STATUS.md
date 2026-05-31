# Status Ledger

Live state of the v4 spec & plan run. Updated by the primary agent every wave.

## ✅ TRACKS CONVERGED (2026-05-31) — single canonical track is `spec/`
Track A (faithful) was renamed `spec/` and adopted as the **one canonical track**. Track B (optimized) is frozen reference (`spec-optimized/`, `plan-optimized/`). Survivor pass found all 25 must-have deltas already present in `spec/`; 117 hardening deltas dropped, 4 bets deferred. See [`SURVIVOR-PASS.md`](./SURVIVOR-PASS.md) + [`FUTURE-ENHANCEMENTS.md`](./FUTURE-ENHANCEMENTS.md) (FE-1..FE-5).

## Current state (2026-05-31)
**Phase 2 — Sweep 1.** Autonomous long run ([scope envelope](./RUN-SCOPE-2026-05-31.md)), one living PR **#220** on `claude/epic-fermat-LTO4V`. Cadence: build → review → integrate, batch by batch. **Batches 2-tail, 3, 4 all CLOSED.** **Batch 5 (final 6: C46–C50, C57) is next** — then run-summary + retro.

## Adopted decisions (see [`review-log.md`](./review-log.md))
D-1 same-provider judge · D-2 bundle-id namespace · D-3 C20 bead schemas/C22 mechanism · D-4 C20→C19 · D-5 C41 hash-chain · D-6 "canonical track" · D-7 node-kind=C12 · D-8 convoy→C05/Order→C40 · D-9 F38=C10 · D-10 modeldb fields · D-11 LangFuse traces-only · D-12 two-sink cross-refs · D-13 holdout C34/C43 split · D-14 G37≠FE-3 · D-15 satisfaction holistic (FE-5 deferred) · D-16 loop-DOT encoding=C12 · D-17 judge read-surface · **D-18 (PROVISIONAL, operator-confirm)** C43 split-sequencing (boundary-typing→P2, twin-isolation→P3c) · **D-19** methodology significance→C48. **XC-3 RESOLVED** (C39 owns G18 numeric policy).

## Coverage ledger — the no-missed-review guarantee
Four axes: **B**uilt · **R**eviewed · **I**ncorporated · i**N**tegrated. Done only when every component is ✓ on all four.

| Batch | Components | B | R | I | N |
|---|---|:-:|:-:|:-:|:-:|
| **1** (12) | C01 C02 C03 C07 C08 C17 C19 C20 C21 C22 C23 C41 | ✓ | ✓ | ✓ | ✓ |
| **2-partial** (11) | C04 C05 C09 C10 C12 C13 C24 C25 C28 C29 C42 | ✓ | ✓ | ✓ | ✓ |
| **2-tail** (2) | C26 C27 | ✓ | ✓ | ✓ | ✓ |
| **3** (13) | C06 C11 C14 C15 C16 C18 C30 C31 C32 C33 C34 C35 C40 | ✓ | ✓ | ✓ | ✓ |
| **4** (13) | C36 C37 C38 C39 C43 C44 C45 C51 C52 C53 C54 C55 C56 | ✓ | ✓ | ✓ | ✓ |
| **5** (6) | C46 C47 C48 C49 C50 C57 | · | · | · | · |

**51/57 components fully closed.** No outstanding review debt. **6 remain (Batch 5).**

## Open human decisions / morning-review (carried in review-log)
- **D-18** — C43 split-sequencing (pull boundary-typing/blast-radius to P2 precondition; twin-isolation stays P3c). **Security risk-tolerance call → operator confirm.**
- **OQ-5** — G14 class-level transfusion-failure hedge ownership across C51/C52/C54 (if a P3 sub-phase's transfusion bet fails: re-sequence vs hand-build?).
- **prevent-vs-detect** — C43:OQ-1 ≡ C34:OQ-1 (does `gc` prevent out-of-partition/production access, or permit-with-detect?), gated on G11 (real `gc`).
- G37 secrets store (open gap, owned C03). Judge read-surface exact shape (D-17 Sweep-2 joint freeze).
- *Resolved:* signing→D-14, cross-family→D-1, FE-5→D-15.

## Concurrency reality
Platform rate-limits subagent launches at ~8 concurrent. Pipeline at width ~6–8.

## Wave log
| Wave | Phase | Dispatched | Status |
|---|---|---|---|
| W0–W5 | 0–2 | Grounding, Batch-1, convergence, Batch-2-tail+review+integrator | done (PR #213, #218; D-6..D-14) |
| W6–W8 | 2 | Batch 3 build (13) → review (13) → integrator (D-15..D-17) | done (Batch 3 closed) |
| W9–W11 | 2 | Batch 4 build (13) → review (13) → integrator (D-18/D-19, XC-3) | done (Batch 4 closed) |
| W12 | 2 | Batch 5 builders (6: C46–C50, C57) | ⏳ dispatching |
