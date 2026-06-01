# Status Ledger

Live state of the v4 run (specs + plans). Updated by the primary agent every wave.

## ✅ SWEEP-1 COMPLETE (2026-05-31) — all 57 components built + reviewed + integrated
Single canonical track `spec/` + `plan-faithful/`. Every component has `spec/<ID>-*.md` + `plan-faithful/<ID>-*.md` + `spec/<ID>-*.review.md` (57/57/57), all adversary verdicts **accept-with-fixes** (0 blockers, 0 needs-rework across the run), all cross-component findings integrated via decisions **D-1..D-19** (+ XC-3 resolved). See [`RUN-SCOPE-2026-05-31.md`](./RUN-SCOPE-2026-05-31.md) and the run summary at [`run-summary.md`](../../../run-summary.md).

## ✅ TRACKS CONVERGED (2026-05-31) — single canonical track is `spec/`
Track B (optimized) is frozen reference (`spec-optimized/`, `plan-optimized/`). Survivor pass folded all 25 must-have deltas into `spec/`; 117 hardening deltas dropped, 4 bets deferred (FE-1..4); FE-5 resolved (D-15). See [`SURVIVOR-PASS.md`](./SURVIVOR-PASS.md) + [`FUTURE-ENHANCEMENTS.md`](./FUTURE-ENHANCEMENTS.md).

## Adopted decisions (see [`review-log.md`](./review-log.md))
D-1 same-provider judge · D-2 bundle-id namespace · D-3 C20 bead schemas/C22 mechanism · D-4 C20→C19 · D-5 C41 hash-chain · D-6 "canonical track" · D-7 node-kind=C12 · D-8 convoy→C05/Order→C40 · D-9 F38=C10 · D-10 modeldb fields · D-11 LangFuse traces-only · D-12 two-sink cross-refs · D-13 holdout C34/C43 split · D-14 G37≠FE-3 · D-15 satisfaction holistic (FE-5 deferred) · D-16 loop-DOT encoding=C12 · D-17 judge read-surface · **D-18 (PROVISIONAL, operator-confirm)** C43 split-sequencing · **D-19** methodology significance→C48 · **XC-3 RESOLVED** (C39 owns G18 numeric policy).

## Coverage ledger — the no-missed-review guarantee
Four axes: **B**uilt · **R**eviewed · **I**ncorporated · i**N**tegrated. **DONE only when every component is ✓ on all four — now true for all 57.**

| Batch | Components | B | R | I | N |
|---|---|:-:|:-:|:-:|:-:|
| **1** (12) | C01 C02 C03 C07 C08 C17 C19 C20 C21 C22 C23 C41 | ✓ | ✓ | ✓ | ✓ |
| **2-partial** (11) | C04 C05 C09 C10 C12 C13 C24 C25 C28 C29 C42 | ✓ | ✓ | ✓ | ✓ |
| **2-tail** (2) | C26 C27 | ✓ | ✓ | ✓ | ✓ |
| **3** (13) | C06 C11 C14 C15 C16 C18 C30 C31 C32 C33 C34 C35 C40 | ✓ | ✓ | ✓ | ✓ |
| **4** (13) | C36 C37 C38 C39 C43 C44 C45 C51 C52 C53 C54 C55 C56 | ✓ | ✓ | ✓ | ✓ |
| **5** (6) | C46 C47 C48 C49 C50 C57 | ✓ | ✓ | ✓ | ✓ |

**57/57 components fully closed. No outstanding review debt. Sweep-1 done.**

## Open human decisions / morning-review (carried in review-log)
- **D-18** — C43 split-sequencing (boundary-typing→P2 precondition; twin-isolation→P3c). **Security risk-tolerance → operator confirm.**
- **OQ-C57-3** — F54 objective-drift audit: build an owning mechanism vs register-only residual (loudest residual after G31 on a self-modifying L5 factory). **Operator call.**
- **OQ-6** — C46 dep edge should read C21/C25 (OTLP-metrics + CXDB) not just C24 (touches `component-inventory.md`).
- **C49:OQ-1** — when is an LLM-step counterfactual trustworthy enough to feed C48/C50 (v4's riskiest open question).
- **prevent-vs-detect** (C43:OQ-1 ≡ C34:OQ-1, gated on G11). **G37** secrets store (C03). Judge read-surface shape (D-17 sweep-2). Unleash license contradiction (README:273 vs :322 → C57 register).
- *Resolved:* signing→D-14, cross-family→D-1, FE-5→D-15, XC-3→C39, **XC-9 + C42:OQ-4 + C04:OQ-4 → D-23 harvest (2026-06-01, gascity-prototype-verified)**.

## Sweep-2 D-23 first action — DONE (protocol + harvest, no live run)
Per operator decision (no live agents this run). [D-23 spike protocol](D-23-gas-city-spike-protocol.md) (runnable prevent-vs-detect / `[[service]]` / Orders-durability checklist) + [D-23 substrate harvest](D-23-substrate-harvest.md) (12 facts from `gascity-prototype@b14c278`). Resolved XC-9 / C42:OQ-4 / C04:OQ-4; **0 true contradictions** after lead verification (3 flagged, all reclassified NEW-INFO). **Prevent-vs-detect (C34:OQ-C34-1 ≡ C43:OQ-C43-1) remains OPEN** — needs a Docker-capable empirical run of the protocol (the prototype deferred the smoke test).

## Passes still owed (next runs)
Integration Pass over the whole 57 (cross-batch drift) · **Sweep 2** (implementation-ready: signatures, schemas, sequence/state diagrams, error taxonomies, acceptance tests) · **Sweep 3** (exhaustive: pseudocode, skeletons, edge-cases, perf/sec/ops) · final cross-cutting README/index.

## Concurrency reality
Platform rate-limits subagent launches at ~8 concurrent. Pipelined at width 6–8 throughout.

## Wave log
| Wave | Phase | Dispatched | Status |
|---|---|---|---|
| W0–W5 | 0–2 | Grounding, Batch-1, convergence, Batch-2-tail+review+integrator | done (PR #213, #218; D-6..D-14) |
| W6–W8 | 2 | Batch 3 build (13) → review (13) → integrator (D-15..D-17) | done (Batch 3 closed) |
| W9–W11 | 2 | Batch 4 build (13) → review (13) → integrator (D-18/D-19, XC-3) | done (Batch 4 closed) |
| W12–W14 | 2 | Batch 5 build (6) → review (6) → integrator (28 OQs) | done (**Sweep-1 complete, 57/57**) |
