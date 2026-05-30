# C28 — Claude Code Agent Loop  (Build Plan, Track B)

> Source / Spec ref: spec-optimized/C28-claude-code-agent-loop.md

## 1. Work breakdown

| id | description | size | prerequisites |
|---|---|---|---|
| T1 | **Freeze `AgentLoopProvider` role contract** (inbound task/context/model_selection/capability_profile/tool_surface/budget; outbound `AgentOutcome` + telemetry stream). The interface every adapter binds to. (DELTA-01) | M | C04 session shape, C29 selection shape, C43 profile shape (stub) |
| T2 | **Claude Code default adapter** — wrap the `claude` CLI subprocess via Gas City `claude` provider preset (README 120); wire OAuth/Max credential pickup through C04; set telemetry env vars (AI-CONTEXT §4.3). | M | T1, C04 |
| T3 | **Tool/hook/skill/subagent/MCP manifest** — typed, version-pinned config in a C02 pack; PreToolUse/PostToolUse/SessionStart/Stop chain; MCP mount; subagent registration. (DELTA-07) | M | T1, C02 |
| T4 | **Capability/egress binding + PreToolUse enforcement** — bind a C43 profile per invocation; default-deny Bash/network/fs; deny → `tool-denied`. (DELTA-04) | M | T3, C43 (profile primitives) |
| T5 | **Turn-loop ceilings + compaction + stuck-detector** — max_turns/token/wall-clock budgets, compaction policy, no-progress detector; map breaches to `AgentOutcome.status`. (DELTA-05) | M | T1, T2 |
| T6 | **Seat/quota governor** — `acquire()` admission control, measured token/cost accounting, seat-pool ledger, back-pressure to C05. (DELTA-02) | L | T5 |
| T7 | **Seat-pool scheduler** — N Max + Agent-SDK-credit + metered-API seats behind one scheduler; per-seat rate-limit state. (DELTA-03) | L | T6; OQ-1 ToS resolution |
| T8 | **Fallback adapter (API-key / Agent-SDK)** — second `AgentLoopProvider` impl behind a C03 feature flag. (G12) | M | T1, T11 |
| T9 | **Floor conformance suite** — capability-floor test battery (multi-turn tool use, subagent fan-out, structured-edit fidelity, hook honoring) gating any adapter via C03. (DELTA-06) | M | T1, T2 |
| T10 | **Telemetry correlation guarantee** — ensure `prompt.id`/`session.id`/`account_uuid`/`organization.id` on every signal for C24/C25. | S | T2 |
| T11 | **Config surface** — C03 flags: adapter enablement, seat-pool size, budget defaults, hook/skill/MCP enablement, Max-vs-fallback. | S | T1 |
| T12 | **Judge-instance separation guard** — refuse same-family/shared-context between coder and judge role instances. (F48/F55 hook) | S | T1, C29 |

## 2. Dependency graph

- **Upstream (must precede):** C04 (session/runtime), C02 (pack ABI for the manifest), C29 (selection shape — co-designed), C43 (capability-profile primitives), C03 (config).
- **Critical path:** T1 → T2 → T5 → T6 → T7 (governor/pool is the longest pole and is gated by **OQ-1**, the Max-ToS pooling question). T9 conformance suite is the gate that unblocks T8 fallback.
- **Downstream consumers:** C05 (dispatch/back-pressure), C25/C24 (telemetry), C32 (judge sibling), C35 (override hooks), C57 (coverage ratings).
- **Concurrent with:** C29, C25, C26, C27, C24 (all Batch 2).

## 3. Parallelization

Once **T1 freezes the contract**, fan out:
- **Stream A (adapters):** T2 Claude Code adapter → T9 conformance suite → T8 fallback adapter.
- **Stream B (loop control):** T5 ceilings/compaction/stuck-detector — independent of adapter internals.
- **Stream C (resource):** T6 governor → T7 seat-pool scheduler (gated by OQ-1).
- **Stream D (surface):** T3 manifest → T4 capability enforcement.
- **Stream E (glue):** T10 telemetry, T11 config, T12 judge-guard — small, parallel against stubs.

Streams A–E build against the T1 contract + stubs concurrently.

## 4. Interfaces-first / contract milestones

Freeze early so dependents build against stubs:
1. **`AgentLoopProvider` interface + `AgentOutcome` schema (T1)** — unblocks C05 (dispatch target), C29 (selection consumer), C32 (judge), and every adapter.
2. **Governor admission contract `acquire()/back-pressure` (T6)** — unblocks C05 throttling logic.
3. **Tool/hook/MCP manifest schema (T3)** — unblocks C35 (override hooks) and C43 (auditability).
4. **Telemetry correlation-key guarantee (T10)** — unblocks C24/C25 against a stub emitter.

## 5. Risks & de-risking order

1. **OQ-1 — Max multi-seat ToS (spike first).** Before building T7, confirm whether pooling N Max seats for unattended automation is permitted. If not, T7 collapses to metered-API seats and the G13/G34 cost story changes materially. Highest-uncertainty, gates the throughput thesis.
2. **OQ-2 — fallback adapter conformance.** Prototype T8 against T9 early; if the API-key/Agent-SDK adapter can't pass the floor suite, the G12 "fallback ready" mitigation is hollow and must be escalated.
3. **OQ-3 — PreToolUse enforcement strength vs a Bash-capable agent.** Spike T4 against C43 primitives; confirm how much the capability profile actually bounds the trifecta before twins (G31).
4. **Stuck-detector false-positives (T5)** — tune the no-progress window so legitimate long reasoning isn't killed.

## 6. Definition of done

- **Per-component:** spec acceptance criteria 1–6 all pass; both Claude Code and fallback adapters pass T9 conformance; budgets/capability-profile/governance enforced and observable; telemetry correlation verified end-to-end into C24/C25.
- **Per-task exits:** T1 — contract reviewed + frozen, consumers building against it. T2/T8 — adapter passes T9. T4 — out-of-profile tool call denied at PreToolUse, auditable from manifest. T5 — ceiling/stuck breaches map to correct `status` + emit events. T6/T7 — saturated pool returns back-pressure, never over-grants a capped seat; per-task cost in `AgentOutcome`. T12 — judge refuses shared family/context.
- **Open-question gates:** OQ-1/OQ-2/OQ-3 resolved or explicitly carried into review-log before C28 is declared production-ready; T7 not merged until OQ-1 resolves.
