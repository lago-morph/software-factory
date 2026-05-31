# Status Ledger

Live state of the v4 spec & plan run. Updated by the primary agent every wave.

## ✅ TRACKS CONVERGED (2026-05-31) — single canonical track is `spec/`
Track A (faithful) was renamed `spec/` and adopted as the **one canonical track**. Track B (optimized) is frozen as reference (`spec-optimized/`, `plan-optimized/`). A survivor pass under the operator's capability-for-principle bar found all 25 must-have deltas **already present** in `spec/` in minimal form (zero spec edits); 117 hardening deltas were dropped and the 4 architectural "bets" deferred. See [`SURVIVOR-PASS.md`](./SURVIVOR-PASS.md) and [`FUTURE-ENHANCEMENTS.md`](./FUTURE-ENHANCEMENTS.md) (FE-1..FE-5).

## Current state (2026-05-31)
**Phase 2 — Sweep 1: building the 34 unbuilt components on canonical `spec/` + `plan-faithful/`.** PR #213 + #218 merged to `main`. **Active run:** autonomous long run ([scope envelope](./RUN-SCOPE-2026-05-31.md)), one living PR **#220** on `claude/epic-fermat-LTO4V`. Cadence: **build → review → integrate**, batch by batch. **Batch 2 CLOSED** (D-6..D-14); **Batch 3 CLOSED** (build 13/13 + review 13/13 all accept-with-fixes + integrator D-15..D-17). **Batch 4 next** (self-healing + bootstrap).

## Adopted decisions (see [`review-log.md`](./review-log.md))
D-1 same-provider judge (cross-family→FE-1) · D-2 bundle-id `softwarefactory.v4.{beads,trajectory,packs}` · D-3 C20 authors bead schemas / C22 mechanism · D-4 C20 depends on C19 · D-5 C41 owns hash-chain over C23 · D-6 "canonical track" nomenclature · D-7 node-kind home=C12 · D-8 convoy→C05 / Order→C40 · D-9 F38 vocab-lint=C10 · D-10 modeldb=`{id,family,cost_tier}` · D-11 LangFuse traces-only seam · D-12 two-sink cross-refs · D-13 holdout: C34 enforce+audit / C43 lethal-trifecta · D-14 G37(secrets)≠FE-3(signing) · **D-15** satisfaction holistic (FE-5 deferred) · **D-16** loop DOT encoding=C12 (Sweep-2 joint freeze) · **D-17** judge read-surface (Sweep-1 default + C42/C34/C32 joint freeze).

## Coverage ledger — the no-missed-review guarantee
Four axes: **B**uilt · **R**eviewed (`.review.md`) · **I**ncorporated (findings applied/deferred-with-reason) · i**N**tegrated (cross-component pass). **Done only when every component is ✓ on all four.** Legend: ✓ done · ⏳ in progress · · pending.

| Batch | Components | B | R | I | N |
|---|---|:-:|:-:|:-:|:-:|
| **1** (12) | C01 C02 C03 C07 C08 C17 C19 C20 C21 C22 C23 C41 | ✓ | ✓ | ✓ | ✓ |
| **2-partial** (11) | C04 C05 C09 C10 C12 C13 C24 C25 C28 C29 C42 | ✓ | ✓ | ✓ | ✓ |
| **2-tail** (2) | C26 C27 | ✓ | ✓ | ✓ | ✓ |
| **3** (13) | C06 C11 C14 C15 C16 C18 C30 C31 C32 C33 C34 C35 C40 | ✓ | ✓ | ✓ | ✓ |
| **4** (13) | C36 C37 C38 C39 C43 C44 C45 C51 C52 C53 C54 C55 C56 | ✓ | · | · | · |
| **5** (6) | C46 C47 C48 C49 C50 C57 | · | · | · | · |

**38/57 components fully closed** (Batches 1, 2, 3). No outstanding review debt. **19 remain** (Batch 4: 13, Batch 5: 6).

## Open human decisions (carried in review-log)
~~Signing mandatory-vs-optional~~ **RESOLVED D-14** · ~~cross-family judge~~ **RESOLVED D-1** · ~~FE-5 enumerated DoD~~ **RESOLVED D-15** (holistic; enumerated deferred to Sweep-2) · G37 secrets store (open gap, owned by C03) · judge read-surface exact shape (D-17 Sweep-2 joint freeze C42/C34/C32 — morning-review).

## Concurrency reality
Platform rate-limits subagent launches at **~8 concurrent**. Pipeline at width ~6–8; drain to ~2, top up.

## Wave log
| Wave | Phase | Dispatched | Status |
|---|---|---|---|
| W0–W2 | 0–2 | Grounding + Batch-1 builders | done (→ PR #213) |
| — | — | two-track → single-track convergence | done (→ PR #218) |
| W3 | 2 | Batch 2-tail builders: C26, C27 | done |
| W4 | 2 | Batch-2 review: 13 adversaries | done (13/13 accept-with-fixes) |
| W5 | 2 | Integrator: D-6..D-14 + 54 OQs | done (Batch 2 closed) |
| W6 | 2 | Batch 3 builders (13) | done (13/13 built) |
| W7 | 2 | Batch-3 review: 13 adversaries | done (13/13 accept-with-fixes) |
| W8 | 2 | Integrator: D-15..D-17 + 55 OQs | done (Batch 3 closed) |
| W9 | 2 | Batch 4 builders (13) | done (13/13 built) |
| W10 | 2 | Batch-4 review: 13 adversaries (chunk 8+5) | ⏳ running |
