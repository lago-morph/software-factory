# C31 — Scenario Runner  (Build Plan, canonical track)

> Source / Spec ref: spec/C31-scenario-runner.md (Sweep-2)
> Binding decisions: D-36 (trajectory = Inspect AI log, NOT CXDB), D-37 (post-hoc scoring; C31 does NOT invoke C32 inline), D-13 (holdout enforcement = C34), D-6 (canonical track).

## 1. Work breakdown

| Task | Description | Size | Prerequisites |
|---|---|---|---|
| T1 | **Freeze the runner-node contract (M1)** — freeze all three contracts that dependents build against: (a) **input** = `ScenarioRef { scenario_path, task }` (from C30); (b) **invocation** = `[[service]] type="inspect_ai"` + `[[tool]] type="subprocess"` `inspect eval … --task … --log-dir … --model …`, `work_partition="scenarios"`; (c) **`TrajectoryLog` schema** (§4.1 envelope + §4.2 on-disk log shape). Agree with C30 (task DSL owner), C32 (TrajectoryLog consumer), C17 (tool-node ABI), C02 (subprocess ABI). **This is the new critical seam** — TrajectoryLog is the frozen hand-off artifact (D-37). | S | C30 scenario-reference shape, C17 tool-node ABI, C02 subprocess ABI |
| T2 | **Spike the session-id adapter (G25/OQ-1)** — direct Inspect AI experiment: (a) set `GC_SESSION_ID` in subprocess env and confirm the task can read it (thin baseline §3.3); (b) if Inspect AI overrides the env or the task cannot embed it in `samples[*].metadata`, activate thick fallback design. Resolves the single load-bearing uncertainty. **De-risker — do first.** | M | Inspect AI installed (pinned), T1 |
| T3 | **Pack + service/tool skeleton (I1/I2)** — install pinned Inspect AI; declare the `[[service]] type="inspect_ai"` provider block + the `[[tool]] type="subprocess"` node with `work_partition="scenarios"` per T1 contract. `cmd`/`command` spelling per D-34 (G11-gated; document both and use the verified one). No in-process Python import (INV-5). | S | C02/C17 ABI, T1 |
| T4 | **Session-id adapter (I4/INV-2, addresses G25)** — implement the adapter the T2 spike selected: set `GC_SESSION_ID=<session.id>` in subprocess env (thin) or maintain `inspect_run_id → session_id` map (thick); surface `session_id` on the `TrajectoryLog` output. Also freeze the task wrapper hook with C30 (OQ-2: how the task embeds `session_id` in `samples[*].metadata`). **C31's core custom deliverable.** | M | T2 (depth), T3 |
| T5 | **Run-execution wiring (I3→I5)** — substitute `scenario_path`/`task` into the node args; capture `log_path` from `--log-dir`; run `inspect eval`; build the `TrajectoryLog` envelope (§4.1) with all required fields; surface as tool-node output bound to bead (README:439). Inspect AI is the runner — no custom eval loop (INV-1). Record `run_started_at`, `run_completed_at`, `inspect_version`. | M | T3, T4 |
| T6 | **TrajectoryLog → judge handoff (I5 / D-37)** — confirm C32 can locate and read `log_path` post-hoc: C32 is invoked (by the engine, separately) with the `TrajectoryLog` envelope fields; it reads the `.eval` log without any C31 involvement. Validate the §4.2 on-disk schema against the pinned Inspect AI version. | S | T5, (coordinates w/ C32) |
| T7 | **Status/failure surfacing + E-codes** — surface E-C31-01..05 (§8): nonzero exit → `exit_code` in TrajectoryLog + C02 tool-node error status; run timeout → E-C31-03 with sentinel exit_code; adapter failure → E-C31-04 with `session_id` EMPTY + block C32 forwarding; log file missing → E-C31-05. C31 adds NO retry logic (INV-1). | S | T5 |
| T8 | **Runner-health events** — emit eval exit status / run latency / adapter id-threading success-rate as events on C23 for observability; no custom dashboard. | S | T5, C23 emit seam |
| T9 | **Integration pack (AC-C31-01…AC-C31-13)** — synthetic C30 scenario + pinned Inspect AI + stub or real C32; drive all acceptance tests: session-id threading end-to-end (AC-C31-03/04), post-hoc scoring (AC-C31-05), all E-code assertions (AC-C31-10/11/12), no-over-build review (AC-C31-13). | L | T4–T7, pinned Inspect AI, C32 (or stub for AC-C31-05) |

## 2. Dependency graph

**Must precede C31:**
- **Inspect AI** installed + **version-pinned** (the wrapped runner; README:423) — the `inspect eval` CLI
  surface + `TrajectoryLog` on-disk schema must be pinned before C32 can build its scorer.
- **C30** scenario store (the `{scenario_path}` reference C31 executes; author/execute split, D-13); also the
  task wrapper hook that embeds `session_id` (OQ-2 freeze with C30).
- **C17 / C02** tool-node abstraction + subprocess ABI.

**C31 must precede (its consumers assume runs execute + TrajectoryLog is available post-hoc):**
- **C32** judge harness (reads `log_path` from TrajectoryLog and scores post-hoc; D-37). **The TrajectoryLog
  schema (§4) is the seam C32 builds against — it must be frozen (T1/M1) before C32 builds its scorer.**
- **C33** satisfaction aggregation (downstream of C32).
- **C24** telemetry→CXDB bridge (coordination edge: adapter's `session_id` must be correct for C24 to
  parent-chain turns; non-spine per D-36 but C24 reads the `session_id` that C31 threads).

**Governed-by (not a build dep):** **C34** (holdout enforcement) + **C42** (rig partition) — C31 *runs inside*
the `scenarios` partition they govern (INV-3); it does not build against them.

**Critical path inside C31:** T1 (contract freeze, incl. TrajectoryLog schema) → **T2 (adapter spike)** →
T4 (adapter) → T5 (run wiring) → T6 (post-hoc handoff validated) → T9. The **TrajectoryLog schema freeze
(T1)** and **adapter spike (T2)** are the two serial gates; everything else fans out.

**NEW SEAM (→ orchestrator ledger):** The `TrajectoryLog` schema (§4) is the frozen contract C32 (judge)
builds its scorer against. C31 writes it; C32 reads it post-hoc (D-37). If C31's Inspect AI version pin or
field names drift from what C32 expects (especially `samples[*].messages` path and `session_id` field in the
envelope), scoring is silently broken. **Both C31 and C32 MUST pin the same Inspect AI version.** This is
the highest-priority cross-component seam introduced at Sweep-2.

## 3. Parallelization

Once **T1 (contract freeze, incl. TrajectoryLog schema)** lands and **T2 (adapter spike)** starts, two
workstreams fan out:

- **WS-A (wrap):** T3 (service/tool skeleton) → T5 (run-execution wiring) → T7 (status/E-codes). Can build
  against a stub scenario + synthetic TrajectoryLog while WS-B resolves the adapter.
- **WS-B (adapter — the custom core):** **T2 (spike)** → T4 (adapter + OQ-2 freeze with C30) → T6 (post-hoc
  handoff validation with C32). The G25 spine; the spike (T2) can run immediately against a pinned Inspect AI
  in parallel with WS-A's skeleton.
- **WS-C (ops):** T8 (runner-health events) — independent of A/B internals; only needs the C23 emit seam.

T9 (integration pack) joins all three. WS-A and WS-B meet at T5↔T4 (the run carries the adapter's
`session_id`) and at T6 (the TrajectoryLog reaches C32 post-hoc).

**C32 can start building its scorer** against the frozen §4.2 on-disk schema as soon as T1 (M1) is done —
it does not need T2–T6 to complete. C32's scorer is not C31's responsibility; the schema freeze (T1) is the
unblocking deliverable.

## 4. Interfaces-first / contract milestones

- **M1 — TrajectoryLog + runner-node contract freeze (T1):** the three contracts dependents build against:
  (a) **input** = `ScenarioRef { scenario_path, task }`,
  (b) **invocation** = `[[service]] type="inspect_ai"` + `[[tool]] type="subprocess"` `inspect eval …`, `work_partition="scenarios"`,
  (c) **`TrajectoryLog` schema** (§4.1 envelope fields + §4.2 on-disk `.eval` log field table).
  Freezing M1 lets WS-A build against a stub scenario, WS-B resolve the adapter, and **C32 start building
  its scorer** against the §4.2 schema — all in parallel.
- **M2 — Adapter contract frozen (T2/T4, resolves G25/OQ-1/OQ-2):** the `session.id` injection mechanism
  (thin env-var baseline vs thick map fallback) + OQ-2 task wrapper hook frozen with C30, **before** C32
  scores and C24 parent-chains run turns. Unblocks the trajectory-threading guarantee (INV-2).
- **M3 — Post-hoc handoff validated (T6, resolves OQ-4 for C32 seam):** confirmed that C32 can read `log_path`
  post-hoc from the frozen §4.2 schema with the pinned Inspect AI version. Gates C32's scorer greenlight.
- **M4 — Run-target boundary confirmed (OQ-5, RESOLVED at Sweep-2):** confirmed — scenario/task (C30)
  selects the target; C31 is target-agnostic. No build work needed; boundary closed.

## 5. Risks & de-risking order

1. **Spike first — session-id adapter depth (T2/G25/OQ-1).** The single highest-value/highest-risk
   uncertainty: does Inspect AI accept a `GC_SESSION_ID` env var in the task (thin), or does it mint its own
   unalterable session identity (thick map needed)? A wrong assumption breaks trajectory threading (AC-C31-03)
   and silently corrupts C32's scoring. Retire by a direct Inspect AI experiment **before** building T4.
2. **Freeze TrajectoryLog schema with C32 (T1/M1).** The schema is the cross-component seam C32 builds
   against. Drift here breaks scoring silently. Both C31 and C32 must pin the same Inspect AI version.
3. **Confirm OQ-2 (task wrapper hook) with C30 (T4).** The exact Inspect AI task-level hook that embeds
   `session_id` in `samples[*].metadata` must be agreed with C30 (the Task DSL owner) before C31 ships.
4. **Pin + verify — Inspect AI version (OQ-4).** Freeze the `inspect eval` CLI surface + on-disk log schema
   C32 must parse; a version drift silently breaks the post-hoc judge handoff (the most dangerous drift point).
5. **Guard against over-build (AC-C31-13).** Continuously verify C31 stays a *wrap + adapter*: no custom
   runner/scheduler/eval-loop, no retry, no scoring, no CXDB interaction (D-36), no inline C32 invocation
   (D-37). When in doubt, DROP to the owning component.

## 6. Definition of done

**Per-component DoD:** the integration pack (T9) passes **AC-C31-01…AC-C31-13** against a pinned Inspect AI:
- Runner wrap works (Inspect AI is the runner, no custom loop)
- `TrajectoryLog` schema fully populated (§4.1 + §4.2 readable by C32)
- Session-id threads (one `session_id` per run; AC-C31-03/04 with spike-resolved adapter)
- Runs in the `scenarios` partition, does not enforce holdout (AC-C31-07)
- Verdict-blind (AC-C31-08)
- Pack-not-import (Python behind subprocess boundary; AC-C31-09)
- Post-hoc handoff validated: C32 reads `log_path` without C31 involvement (AC-C31-05; D-37)
- All E-codes trigger correctly (AC-C31-10/11/12)
- No over-build (AC-C31-13 review)

C31 is a Gas City pack (the `[[service]] type="inspect_ai"` + `[[tool]]` blocks), Inspect-AI-version-pinned.
**TrajectoryLog schema (§4) frozen and agreed with C32 before C32 builds its scorer.**

**Per-task DoD:**
- T1: M1 contracts (incl. TrajectoryLog schema) written + agreed with C30/C32/C24/C17 owners.
- T2: spike resolves thin-vs-thick (OQ-1) with evidence from the real Inspect AI.
- T3: the `[[service]]`/`[[tool]]` blocks register + invoke `inspect eval`; no in-process Python import (AC-C31-09).
- T4: `session_id` threaded; AC-C31-03/04 pass; OQ-2 frozen with C30.
- T5: a scenario executes end-to-end and surfaces TrajectoryLog (AC-C31-01/02).
- T6: C32 can locate + read `log_path` post-hoc (AC-C31-05); §4.2 schema pinned (OQ-4 seam).
- T7: all E-C31-01..05 fire correctly (AC-C31-10/11/12); no custom retry/scoring/verdict.
- T8: runner-health events visible on C23.
- T9: full AC suite green; **must pass before C32/C33 build on C31's trajectories**.

**Open questions resolved at Sweep-2 (no longer open):** OQ-3 (eval-level `session.id` granularity), OQ-5
(run-target/twin selection is C30's — confirmed). **Still open:** OQ-1 (adapter depth — spike needed), OQ-2
(task wrapper hook — freeze with C30 at T4), OQ-4 (Inspect AI version pin + `cmd`/`command` spelling per D-34).
