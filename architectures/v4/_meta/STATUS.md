# Status Ledger

Live state of the v4 spec & plan run. Updated by the primary agent every wave.

## ✅ TRACKS CONVERGED (2026-05-31) — single canonical track is `spec/`
Track A (faithful) was renamed `spec/` and adopted as the **one canonical track**. Track B (optimized) is frozen as reference (`spec-optimized/`, `plan-optimized/`). A survivor pass under the operator's capability-for-principle bar found all 25 must-have deltas **already present** in `spec/` in minimal form (zero spec edits); 117 hardening deltas were dropped and the 4 architectural "bets" deferred. See [`SURVIVOR-PASS.md`](./SURVIVOR-PASS.md) and [`FUTURE-ENHANCEMENTS.md`](./FUTURE-ENHANCEMENTS.md) (FE-1..FE-5). The build target for the 34 unbuilt components is now `spec/`.

## Current state (2026-05-31)
**Phase 2 — Sweep 1 (architecture foundation), 23/57 components built; 34 remain.** Tracks have converged: one canonical `spec/` + `plan-faithful/`. The next work is authoring the unbuilt 34 on the canonical track under the capability-for-principle bar (see `HANDOFF.md` §2). PR #213 (original 23) merged; PR #218 (convergence) merging into `main` as of this update.

## Completed (Sweep-1, both tracks) — 23 components, 4 docs each
- **Batch 1 ✅ BUILT + ADVERSARIALLY REVIEWED + INTEGRATED (consistent).** C01 C02 C03 C07 C08 C17 C19 C20
  C21 C22 C23 C41. 5 subsystem adversaries applied fixes; Integration Pass 1 applied rulings D-1..D-5.
  See `_meta/INTEGRATION-PASS-1.md`.
- **Batch 2 partial ✅ BUILT (not yet adversary-reviewed):** C04 C05 C09 C10 C12 C13 C24 C25 C28 C29 C42.

## Adopted decisions (see review-log.md)
D-1 same-provider judge (cross-family→FE-1) · D-2 bundle-id `softwarefactory.v4.{beads,trajectory,packs}`
· D-3 C20 authors bead schemas / C22 mechanism · D-4 C20 depends on C19 · D-5 C41 owns hash-chain over C23.

## NOT built (34) — resume here (see HANDOFF.md §1 for slugs)
- Batch 2 tail: C26 C27.
- Batch 3: C06 C11 C14 C15 C16 C18 C30 C31 C32 C33 C34 C35 C40.
- Batch 4: C36 C37 C38 C39 C43 C44 C45 C51 C52 C53 C54 C55 C56.
- Batch 5: C46 C47 C48 C49 C50 C57.

## Remaining passes (see HANDOFF.md §2)
- Batch-2 adversary review wave; reviews for Batches 3–5 as built; Integration Pass 2+;
  Sweep 2 (implementation-ready); Sweep 3 (exhaustive); final cross-cutting pass.
- Open human decisions in review-log: signing mandatory-vs-optional; G37 secrets store.

## Concurrency reality
Platform rate-limits subagent launches at **~8 concurrent**. Pipeline at width ~6–8, top up as agents finish. (Target "50+" is not reachable on this infra.)

## Wave log
| Wave | Phase | Dispatched | Status |
|---|---|---|---|
| W0 | 0 | Cartographer A, Cartographer B, Skeptic | done |
| W1 | 0 | Reconciler → canonical inventory (57 comps) | done |
| W2 | 2 | Batch-1 builders ×2 tracks (24 attempted) | 8 launched, 16 rate-limited |

## Sweep-1 Batch-1 dispatch queue
Launched (running): C01-F, C01-O, C02-F, C02-O, C03-F, C03-O, C07-F, C08-F.
**Pending re-dispatch:** C07-O, C08-O, C17-F, C17-O, C19-F, C19-O, C20-F, C20-O, C21-F, C21-O, C22-F, C22-O, C23-F, C23-O, C41-F, C41-O.
(F = Track A faithful, O = Track B optimized.)

## Artifacts produced
- `_meta/META-PLAN.md` ✅
- `_meta/TRACK-CHARTERS.md` ✅
- `_meta/DOC-TEMPLATES.md` ✅
- `_meta/STATUS.md` ✅ (this file)
- `_meta/component-inventory-A.md` ⏳ (Cartographer A)
- `_meta/component-inventory-B.md` ⏳ (Cartographer B)
- `_meta/ambiguities-and-gaps.md` ⏳ (Skeptic)
- `_meta/component-inventory.md` — canonical, pending reconciliation

## Next wave (planned)
- W1: Reconciler → canonical `component-inventory.md` (returns compact numbered list to primary).
- Then Phase 1 scaffolding (index docs seeded with component list) + Phase 2 Sweep-1 fan-out.

## Component completion matrix
(Populated once the canonical inventory exists: rows = component IDs, columns =
spec / plan-faithful / spec-optimized / plan-optimized × sweep level.)
