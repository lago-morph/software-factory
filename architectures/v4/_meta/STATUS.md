# Status Ledger

Live state of the v4 spec & plan run. Updated by the primary agent every wave.

## ✅ TRACKS CONVERGED (2026-05-31) — single canonical track is `spec/`
Track A (faithful) was renamed `spec/` and adopted as the **one canonical track**. Track B (optimized) is frozen as reference (`spec-optimized/`, `plan-optimized/`). A survivor pass under the operator's capability-for-principle bar found all 25 must-have deltas **already present** in `spec/` in minimal form (zero spec edits); 117 hardening deltas were dropped and the 4 architectural "bets" deferred. See [`SURVIVOR-PASS.md`](./SURVIVOR-PASS.md) and [`FUTURE-ENHANCEMENTS.md`](./FUTURE-ENHANCEMENTS.md) (FE-1..FE-5).

## Current state (2026-05-31)
**Phase 2 — Sweep 1: building the 34 unbuilt components on canonical `spec/` + `plan-faithful/`.** PR #213 (original 23) and PR #218 (convergence) are both merged to `main`. **Active run:** autonomous long run ([scope envelope](./RUN-SCOPE-2026-05-31.md)) authoring Sweep-1 spec+plan for the 34 unbuilt, with **per-batch adversary review + integrator pass**, on branch `claude/epic-fermat-LTO4V`. Cadence: **build → review → integrate**, batch by batch.

## Adopted decisions (see [`review-log.md`](./review-log.md))
D-1 same-provider judge (cross-family→FE-1) · D-2 bundle-id `softwarefactory.v4.{beads,trajectory,packs}` · D-3 C20 authors bead schemas / C22 mechanism · D-4 C20 depends on C19 · D-5 C41 owns hash-chain over C23. *(D-6+ are added by this run's integrator passes.)*

## Coverage ledger — the no-missed-review guarantee
Four axes per component: **B**uilt (spec+plan exist) · **R**eviewed (`.review.md` exists, real adversary ran) · **I**ncorporated (every finding applied OR deferred-with-reason; none left in limbo) · i**N**tegrated (cross-component drift pass). **The run is done only when every component is ✓ on all four axes.** Legend: ✓ done · ⏳ in progress · · pending.

| Batch | Components | B | R | I | N |
|---|---|:-:|:-:|:-:|:-:|
| **1** (12) | C01 C02 C03 C07 C08 C17 C19 C20 C21 C22 C23 C41 | ✓ | ✓ | ✓ | ✓ |
| **2-partial** (11) | C04 C05 C09 C10 C12 C13 C24 C25 C28 C29 C42 | ✓ | · | · | · |
| **2-tail** (2) | C26 C27 | ⏳ | · | · | · |
| **3** (13) | C06 C11 C14 C15 C16 C18 C30 C31 C32 C33 C34 C35 C40 | · | · | · | · |
| **4** (13) | C36 C37 C38 C39 C43 C44 C45 C51 C52 C53 C54 C55 C56 | · | · | · | · |
| **5** (6) | C46 C47 C48 C49 C50 C57 | · | · | · | · |

**Review debt to clear:** Batch-2-partial (11) were built during the two-track phase but never adversary-reviewed on the canonical track → folded into the first review wave (with C26, C27). Per-component R/I/N states are tracked here as each review wave lands.

## Open human decisions (carried in review-log)
Signing mandatory-vs-optional (→ FE-3 trigger) · G37 secrets store (→ FE-3) · FE-5 enumerated DoD (decide when C32/C33 authored).

## Concurrency reality
Platform rate-limits subagent launches at **~8 concurrent**. Pipeline at width ~6–8; let it drain to ~2, then top up. (The original "50+" target is not reachable on this infra.)

## Wave log
| Wave | Phase | Dispatched | Status |
|---|---|---|---|
| W0 | 0 | Cartographer A, Cartographer B, Skeptic | done |
| W1 | 0 | Reconciler → canonical inventory (57 comps) | done |
| W2 | 2 | Batch-1 builders (×2 tracks) | done (→ PR #213) |
| — | — | *two-track → single-track convergence* | done (→ PR #218) |
| W3 | 2 | **Batch 2-tail builders: C26, C27** | ⏳ running |
