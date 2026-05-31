# C31 — Scenario Runner  (Build Plan, canonical track)

> Source / Spec ref: spec/C31-scenario-runner.md

## 1. Work breakdown

| Task | Description | Size | Prerequisites |
|---|---|---|---|
| T1 | **Freeze the runner-node contract (M1)** — the input contract (`{scenario_path}` from C30 + `{task}`), the invocation contract (`[[service]] type="inspect_ai"` + `[[tool]] type="subprocess"` `inspect eval … --task …`, `work_partition="scenarios"`, AI-CONTEXT §13.3), and the **output contract** (trajectory/sample log + run `session.id` + exit status, bound to a bead). This is the interface that unblocks C32 (judge) and C24 (CXDB delivery). | S | C30 scenario-reference shape, C17 tool-node ABI, C02 subprocess ABI |
| T2 | **Spike the session-id adapter (G25/OQ-1)** — direct Inspect AI experiment: can the caller set/propagate the run's session identity (**thin** 1:1 translation of `session.id`) or does Inspect AI mint its own (**thick** id-map)? Resolves the single load-bearing uncertainty (AI-CONTEXT §12 line 512). **De-risker — do first.** | M | Inspect AI installed (pinned), T1 |
| T3 | **Pack + service/tool skeleton (I1/I2)** — install pinned Inspect AI; declare the `[[service]] type="inspect_ai"` provider block (A28j) + the `[[tool]] type="subprocess"` `inspect eval` node (A28i) per C02/C03 model; place it via C17 by-name. No in-process import of Inspect AI Python (INV-5). | S | C02/C17 ABI, T1 |
| T4 | **Session-id adapter (I4/INV-2, addresses G25)** — implement the adapter the T2 spike selected: inject the run's `session.id` into `inspect eval` (mechanism per OQ-2) and surface it on the output, so emitted turns thread into one trajectory. **C31's core custom deliverable.** | M | T2 (depth), T3 |
| T5 | **Run-execution wiring (I3→I5)** — substitute `{scenario_path}`/`{task}` into the node, run `inspect eval`, and surface the trajectory/sample log + `session.id` + exit status as the node's declared output, bound to a bead (README:439). Inspect AI is the runner — no custom eval loop (INV-1). | M | T3, T4 |
| T6 | **Trajectory→judge / →CXDB handoff (I5)** — ensure the emitted trajectory + run identity are discoverable by C32 (judge scores the right trajectory) and that the threaded `session.id` lets C24 parent-chain the run's turns into one CXDB trajectory (AI-CONTEXT §5.4). | S | T4, T5, (coordinates w/ C32, C24) |
| T7 | **Status/failure surfacing (INV-1/INV-4)** — a nonzero `inspect eval` exit surfaces as the C02 tool-node status for C18/C40 to re-drive; C31 adds **no** custom retry loop, **no** scoring, **no** verdict (verdict-blind). | S | T5 |
| T8 | **Runner-health events** — emit eval exit status / run latency / adapter id-threading success-rate as events on C23 for observability; no custom dashboard. | S | T5, C23 emit seam |
| T9 | **Integration pack (AC-1…AC-9)** — synthetic C30 scenario in the `scenarios` partition + pinned Inspect AI + (stub or real) C24/C32; drive all acceptance tests, especially the **session-id threading** end-to-end (multi-turn scenario → one CXDB-parent-chained trajectory under the run's `session.id`). | L | T4–T7, pinned Inspect AI, C24/C32 (or stubs) |

## 2. Dependency graph

**Must precede C31:**
- **Inspect AI** installed + **version-pinned** (the wrapped runner; README:423) — the `inspect eval` CLI
  surface + trajectory schema the adapter and C32 bind to must be reproducible.
- **C30** scenario store (the `{scenario_path}` reference C31 executes; author/execute split, D-13).
- **C17 / C02** tool-node abstraction + subprocess ABI (to place + invoke the `inspect eval` node).

**C31 must precede (its consumers assume runs execute + trajectories thread):**
- **C32** judge harness (scores the trajectory C31 emits) and **C33** satisfaction aggregation (downstream of
  C32) — the **bootstrap-validation milestone** (README:429) exercises this chain.
- **C24** telemetry→CXDB bridge depends on the adapter's correct `session.id` to parent-chain the run's turns
  (AI-CONTEXT §5.4) — coordination edge, not a build-order block (C24 is Batch 2, already up).

**Governed-by (not a build dep):** **C34** (holdout enforcement) + **C42** (rig partition) — C31 *runs inside*
the `scenarios` partition they govern (INV-3); it does not enforce, so it does not build against them.

**Critical path inside C31:** T1 → **T2 (adapter spike)** → T4 (adapter) → T5 (run wiring) → T6 (handoff) →
T9. The **session-id adapter (T2+T4)** is the load-bearing work — it is C31's only genuine custom code (the
runner is off-the-shelf) and the one v4-flagged "impedance unknown" (G25). Everything else (T3/T5/T7/T8) is
thin wrap + surfacing.

## 3. Parallelization

Once **T1 (contract freeze)** lands, two workstreams fan out — but note **T2 (the adapter spike) is the
serial gate** that both ultimately depend on for correctness, so run it first/concurrently:

- **WS-A (wrap):** T3 (service/tool skeleton) → T5 (run-execution wiring) → T7 (status surfacing). The
  invoke-and-surface spine; can build against a stub scenario + synthetic trajectory while WS-B resolves the
  adapter.
- **WS-B (adapter — the custom core):** **T2 (spike)** → T4 (adapter) → T6 (threading handoff to C24/C32).
  The G25 spine; the spike (T2) can run **immediately** against a pinned Inspect AI in parallel with WS-A's
  skeleton, since it only needs Inspect AI installed, not C31's wiring.
- **WS-C (ops):** T8 (runner-health events) — independent of A/B internals; only needs the C23 emit seam.

T9 (integration pack) joins all three. WS-A and WS-B meet at T5↔T4 (the run carries the adapter's
`session.id`) and at T6 (the threaded trajectory reaches C32/C24).

## 4. Interfaces-first / contract milestones

- **M1 — runner-node contract freeze (T1):** the three contracts dependents/sub-streams build against:
  (a) **input** = `{scenario_path}` (C30 reference) + `{task}`,
  (b) **invocation** = `[[service]] type="inspect_ai"` + `[[tool]] type="subprocess"` `inspect eval … --task …`,
      `work_partition="scenarios"` (AI-CONTEXT §13.3),
  (c) **output** = trajectory/sample log + run `session.id` + exit status, bound to a bead.
  Freezing M1 lets WS-A build against a stub scenario and WS-B resolve the adapter in parallel, and lets C32
  build its scorer against the output shape.
- **M2 — adapter contract frozen (T2/T4, resolves G25/OQ-1):** the `session.id` ⇄ Inspect-AI-run-identity
  mapping + injection mechanism (thin vs thick, OQ-2), **before** C32 scores and C24 parent-chains run turns.
  This is the milestone that unblocks the trajectory-threading guarantee (INV-2) the whole P5/P6 chain leans on.
- **M3 — run-target boundary confirmed (OQ-5):** confirm the scenario/task (C30) — not C31 — selects twin
  (C44) vs real system, so C31 stays target-agnostic, before twins land in Phase 3.

## 5. Risks & de-risking order

1. **Spike first — session-id adapter depth (T2/G25/OQ-1).** The single highest-value/highest-risk
   uncertainty: does Inspect AI accept an injected `session.id` (thin) or mint its own (thick map)? A wrong
   assumption breaks trajectory threading (AC-3) and silently corrupts C24's parent-chain + C32's scoring.
   Retire by a direct Inspect AI experiment **before** building T4. This *is* the "harder part — the Inspect
   AI wrap" v4 flags (README:442).
2. **Confirm — `session.id` injection mechanism (T4/OQ-2)** against the real `inspect eval` CLI (env var vs
   `--metadata`/`-T` vs sample tag vs hook). Drives the adapter's concrete implementation.
3. **Confirm — run/`session.id` granularity (OQ-3):** does one `inspect eval` (many samples/epochs) map to
   one `session.id` or one-per-sample? Sets the trajectory granularity C24/C32 see; confirm against Inspect
   AI's sample model (B49) with C32.
4. **Pin + verify — Inspect AI version (OQ-4):** freeze the `inspect eval` CLI surface + trajectory-log schema
   C32 must parse; a version drift silently breaks the judge handoff.
5. **Guard against over-build (AC-9).** Continuously verify C31 stays a *wrap + adapter*: no custom
   runner/scheduler/eval-loop, no parallel-run engine, no retry policy, no scoring, no scenario store, no CXDB
   delivery. When in doubt, **DROP** to the OSS/owning component (Inspect AI / C18,C40 / C32,C33 / C30 / C24).

## 6. Definition of done

**Per-component DoD:** the integration pack (T9) passes **AC-1…AC-9** against a pinned Inspect AI — runner
wrap (Inspect AI is the runner, no custom loop), executes a C30 scenario, **session-id threads** (run's turns
land as one CXDB parent-chained trajectory under one `session.id`; AC-3/AC-4 with the spike-resolved adapter),
runs in the `scenarios` partition without enforcing holdout, verdict-blind, pack-not-import (Python behind the
subprocess boundary), trajectory→judge handoff works, and **no over-build** (AC-9 review). C31 is a Gas City
pack (the `[[service]] type="inspect_ai"` + `[[tool]]` blocks), Inspect-AI-version-pinned.

**Per-task DoD:**
- T1: M1 contracts written + agreed with C30/C32/C24/C17 owners; sub-streams can build against stubs.
- T2: spike resolves thin-vs-thick (OQ-1) with evidence from the real Inspect AI; the adapter approach is chosen.
- T3: the `[[service]]`/`[[tool]]` blocks register + invoke `inspect eval`; no in-process Python import (AC-7).
- T4: the run's `session.id` is threaded such that AC-3 (one trajectory) passes under the chosen adapter.
- T5: a scenario executes end-to-end and surfaces trajectory + `session.id` + status (AC-1/AC-2).
- T6: C32 can locate + score the right trajectory; C24 parent-chains the run's turns (AC-8).
- T7: a nonzero `inspect eval` exit surfaces as tool-node status for C18/C40; no custom retry/scoring/verdict
  (AC-6/AC-9).
- T8: runner-health events visible on C23.
- T9: full AC suite green; **must pass before C32/C33 build on C31's trajectories** (the P5 execution half the
  bootstrap-validation milestone exercises, README:429).

**Open questions to resolve before sweep 2** (mirrored to review-log): OQ-1 (adapter depth — thin vs thick,
G25), OQ-2 (`session.id` injection mechanism), OQ-3 (one-run vs per-sample `session.id` granularity), OQ-4
(`inspect eval` CLI surface + trajectory-log schema, version-pinned), OQ-5 (run-target/twin selection is
C30/C44's, not C31's).
