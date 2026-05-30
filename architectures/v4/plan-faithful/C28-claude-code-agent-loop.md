# C28 — Claude Code Agent Loop  (Build Plan, Track A)

> Source / Spec ref: spec-faithful/C28-claude-code-agent-loop.md

## 1. Work breakdown

| Task | Description | Size | Prereqs |
|---|---|---|---|
| T1 | **Provider preset binding.** Declare the `[[agent]] provider = "claude"` block (C03 config) so C04 launches the Claude Code CLI subprocess with injected env. | S | C04, C03 |
| T2 | **Env + telemetry surface.** Wire the §13.2 env block (`CLAUDE_CODE_ENABLE_TELEMETRY`, `OTEL_*`, `OTEL_LOG_RAW_API_BODIES`) so every run emits native OTLP + raw API bodies. | S | T1, C25 |
| T3 | **Prompt/context binding.** Bind Gas City prompt template + dispatched bead context as the loop's initial prompt; confirm session-id attribution flows into beads. | M | T1, C05, C09 (prompt-binding) |
| T4 | **Hooks surface.** Register PreToolUse / PostToolUse / SessionStart / Stop hooks declaratively via `.claude/` + pack (C02); prove a PreToolUse deny + PostToolUse observe. | M | T1, C02 |
| T5 | **MCP + subprocess tool dispatch.** Make MCP servers and C02 subprocess tool nodes callable from the loop without a Go fork. | M | T1, C02, C17 |
| T6 | **Skills + subagents surface.** Enable `.claude/skills/` definitions and subagent spawn (Explore/Plan/general/custom). | S | T1 |
| T7 | **Rig partitioning.** Place C28 in the `implementer` rig with `read/write = code`, excluding `scenarios`. | S | C42 |
| T8 | **Resume/continuity check.** Verify C04 session resume + Claude Code session-id restore loop context across restart. | M | C04 |
| T9 | **Gap spikes (G12/G13/G34).** Document (not design) the Max-policy/API-key fallback contingency; capture a token-budget probe + rate-limit-ceiling measurement for review-log. | M | T1–T8 |

## 2. Dependency graph

Critical path: **C04 (session/provider) → T1 → T3 → T4/T5 → end-to-end implementer run**.
- T1 is the gate: nothing runs until the `claude` provider launches under C04.
- T2 can run as soon as T1 lands (independent of T3–T6) — it only adds env.
- T3 needs the prompt-binding component (C09); T4/T5/T6 need the pack ABI (C02).
- **Must precede C28:** C04 (host), C03 (config), C02 (tool/hook/MCP registration), C25 (telemetry sink).
- **Built concurrently with C28:** C29 (routes *to* C28 — depends on C28's existence, not internals), C24/C26/C27 (consume C28 telemetry via the C25 contract), C35 (consumes C28's hook surface).

## 3. Parallelization

After T1 lands, three independent workstreams fan out:
- **WS-A (telemetry):** T2 — env + OTLP + raw-bodies. Verifiable in isolation against a local OTel collector.
- **WS-B (tooling surface):** T4 + T5 + T6 — hooks, MCP/tool-node dispatch, skills/subagents. All pack/`.claude/`-declarative; independent of telemetry.
- **WS-C (governance):** T7 (rig partition) + T8 (resume). Independent of A/B.
T3 (prompt/context binding) is the join point that makes an end-to-end run; it serializes after T1 but runs parallel to WS-A.

## 4. Interfaces-first / contract milestones (freeze early)

1. **Provider-preset contract** (T1) — the exact `[[agent]] provider="claude"` + env schema. Freeze first; C03/C04/C25/C29 all bind to it.
2. **Telemetry emission contract** (T2) — env-var set + raw-API-bodies dir layout + correlation attrs (`session.id`, `prompt.id`). Freeze so C25/C24/C26 build stubs in parallel.
3. **Hook/tool registration contract** (T4/T5) — the `.claude/` + pack surface (overlaps C02 ABI). Freeze so C35 (override loop) builds against it.
4. **Partition contract** (T7) — `implementer` rig `read/write=code`, no `scenarios`. Freeze so C42/C32 can enforce held-out integrity.

## 5. Risks & de-risking order

1. **G12 — Max subprocess-automation permanence (highest).** Spike first: confirm current Max subprocess auth works unattended; document the undesigned API-key/Agent-SDK fallback. This gates the floor's durability and everything above C28.
2. **G13/G34 — single-seat cost/throughput ceiling.** Spike a token-budget probe + rate-limit measurement early; surface numbers to review-log (v4 gives none). Do not design horizontal scale in Track A — just quantify the ceiling.
3. **Hook/MCP-without-fork (T4/T5).** Prove the no-Go-fork extension claim early; it underpins the whole pack-only premise (AI-CONTEXT §3.5).
4. **Telemetry completeness (T2).** Verify raw-API-bodies + OTLP land before downstream (C24–C27) builds on them.

## 6. Definition of done

- **Per spec ACs:** AC1 (dispatched bead → multi-turn loop → tool dispatch → attributed work product), AC2 (OTLP + raw-bodies consumable by C25/C26), AC3 (hook deny/observe), AC4 (Skill + MCP usable, no Go fork), AC5 (no `scenarios` read), AC6 (OAuth-only, no key egress).
- **Per-task DoD:** each task's artifact (config block, hook, env, partition) is version-controlled in a pack (C02) and exercised by at least one run with telemetry captured.
- **Component DoD:** an `implementer` rig agent completes a real bead end-to-end with full trajectory in CXDB (via C24), and the three gap spikes (G12/G13/G34) have written findings in `_meta/review-log.md` — closed by escalation, not by silent assumption.
