# C28 — Claude Code Agent Loop  (Build Plan, canonical track)

> Source / Spec ref: spec/C28-claude-code-agent-loop.md  (Sweep-2)

## 1. Work breakdown

| Task | Description | Size | Prereqs |
|---|---|---|---|
| T1 | **Provider preset binding.** Declare the `[[agent]] provider = "claude"` + `[workspace] provider = "claude"` blocks in `city.toml` (per the prototype's `city.toml.example` pattern) and C03 config so C04 launches the Claude Code CLI subprocess with the full env block (§3.3). | S | C04, C03 |
| T2 | **Env + telemetry surface.** Wire the §3.3 env table (`IS_SANDBOX`, `CLAUDE_CODE_ENABLE_TELEMETRY`, `OTEL_*`, `OTEL_LOG_RAW_API_BODIES`) in the `[[agent]] env = { … }` block so every session emits native OTLP + raw API bodies. Freeze the env-var key names (pending G11); use AI-CONTEXT §13.2 names as the provisional floor. | S | T1, C25 |
| T3 | **Onboarding-prerequisite entrypoint writes.** Add the `~/.claude.json` write to the container entrypoint (pattern from prototype `entrypoint.sh`): global flags + per-rig-path `projects[path]` trust acks. Verify no C28 session hangs on onboarding dialogs (E-C28-01 absent). | S | T1 (workdir paths known only after C04 rig binding) |
| T4 | **Prompt/context binding.** Bind Gas City prompt template + dispatched bead context as the loop's initial prompt; confirm `session.id` attribution flows into beads after the first turn. | M | T1, C05, C09 (prompt-binding) |
| T5 | **Hooks surface.** Register PreToolUse / PostToolUse / SessionStart / Stop hooks via `[[hook]]` blocks in `pack.toml` (C02 pack ABI §3.4); prove a PreToolUse deny (E-C28-03 gate) + PostToolUse observe round-trip. | M | T1, C02 |
| T6 | **MCP + subprocess tool dispatch.** Make MCP servers (`[[service]] protocol = "mcp"`) and C02 subprocess tool nodes callable from the loop without a Go fork. Prove E-C28-07 (MCP-connection failure) surfaces as a tool result, not a loop crash. | M | T1, C02, C17 |
| T7 | **Skills + subagents surface.** Enable `.claude/skills/` definitions and subagent spawn (Explore/Plan/general/custom). No TOML declaration needed for Skills — file presence is registration. | S | T1 |
| T8 | **Rig partitioning + D-30 gate.** Place C28 in the `implementer` rig with `read/write = code`, excluding `scenarios`. Prove E-C28-08 fires on a partition-violation attempt via the PreToolUse hook gate. | S | C42, C34 |
| T9 | **Resume/continuity check.** Verify C04 crash-recover resume + `claude --resume <claude_session_id>` restore loop context; confirm same `session.id` on downstream C24/C21. Prove E-C28-02 fires when JSONL is absent. | M | C04, T4 |
| T10 | **Gap spikes (G12/G13/G34).** Document (not design) the Max-policy/API-key fallback contingency; capture a token-budget probe (OTLP cost metrics from C28) + rate-limit-ceiling measurement for C46; surface the E-C28-03/E-C28-04 auth/rate-limit paths to review-log. | M | T2 (OTLP path live) |

## 2. Dependency graph

Critical path: **C04 (session/provider) → T1 → T3 → T4 → T5/T6 → end-to-end implementer run**.

- T1 is the gate: nothing runs until the `claude` provider launches under C04 with the correct env.
- T3 must run after T1 (workdir paths are known only after C04 rig binding) and before T4 (a hanging onboarding dialog blocks T4).
- T2 can run as soon as T1 lands (independent of T3–T7) — it only adds env vars.
- T4 needs the prompt-binding component (C09); T5/T6 need the pack ABI (C02).
- T8 (rig partitioning) depends only on C42 — can run in parallel with T5/T6.
- T9 depends on T4 (session must have run at least once to have a `claude_session_id`).
- T10 depends on T2 (OTLP path must be live to measure token budget).

**Must precede C28:** C04 (host), C03 (config), C02 (tool/hook/MCP registration), C25 (telemetry sink).
**Built concurrently with C28:** C29 (routes *to* C28 — depends on C28's existence, not internals), C24/C26/C27 (consume C28 telemetry via the C25 contract), C35 (consumes C28's hook surface).

## 3. Parallelization

After T1 + T3 land, three independent workstreams fan out:
- **WS-A (telemetry):** T2 — env + OTLP + raw-bodies. Verifiable in isolation against a local OTel collector.
- **WS-B (tooling surface):** T5 + T6 + T7 — hooks, MCP/tool-node dispatch, skills/subagents. All pack/`.claude/`-declarative; independent of telemetry.
- **WS-C (governance):** T8 (rig partition + D-30 gate) + T9 (resume). Independent of A/B.
T4 (prompt/context binding) is the join point that makes an end-to-end run; it serializes after T1+T3 but can run in parallel with WS-A.
T10 (gap spikes) is post-join — runs after T2 produces live OTLP.

## 4. Interfaces-first / contract milestones (freeze early)

1. **Env + onboarding contract** (T1+T3) — the exact `[[agent]] env` key set + `~/.claude.json` field set. Freeze first; C04/C03/C25 all bind to it. Serves as the C28 bring-up checklist.
2. **Telemetry emission contract** (T2) — env-var set + raw-API-bodies dir layout + correlation attrs (`session.id`, `prompt.id`). Freeze so C25/C24/C26 build stubs in parallel.
3. **Hook registration contract** (T5) — the `[[hook]]` + `[[service]]` pack surface (C02 ABI §3.4). Freeze so C35 (override loop) builds against it.
4. **Partition contract** (T8) — `implementer` rig `read/write=code`, no `scenarios`. Freeze so C42/C34 enforce held-out integrity.

## 5. Risks & de-risking order

1. **E-C28-01 / onboarding dialog hang (highest day-1 risk).** Spike first: run the entrypoint `~/.claude.json` write and confirm no dialog hangs in the target container. Prototype's `entrypoint.sh` is the reference; any deviation in workdir paths will create new hang conditions (F12).
2. **G12 — Max subprocess-automation permanence.** Spike: confirm current Max subprocess auth works unattended; document the undesigned API-key/Agent-SDK fallback (E-C28-03, OQ-1). This gates the floor's durability and everything above C28.
3. **G13/G34 — single-seat cost/throughput ceiling.** Spike a token-budget probe (OTLP cost metrics, T10) + rate-limit measurement early; surface numbers to review-log (v4 gives none). Do not design horizontal scale on the canonical track — just quantify the ceiling (E-C28-04).
4. **Hook/MCP-without-fork (T5/T6).** Prove the no-Go-fork extension claim early; it underpins the whole pack-only premise (AI-CONTEXT §3.5). E-C28-06 (missing hook binary) is the failure mode to exercise.
5. **Telemetry completeness (T2).** Verify raw-API-bodies + OTLP land before downstream (C24–C27) builds on them.

## 6. Definition of done

**Per spec ACs:**
- AC-C28-01: dispatched bead → multi-turn loop → tool dispatch → attributed work product
- AC-C28-02: E-C28-05 sandbox-flag-missing fires correctly
- AC-C28-03: OTLP + raw-bodies consumable by C25/C26 with correct correlation attrs
- AC-C28-04: PreToolUse hook deny works; AC-C28-05: PostToolUse observe works
- AC-C28-06: Skill + MCP usable, no Go fork; E-C28-07 surfaces on MCP failure
- AC-C28-07: partition-violation blocked (E-C28-08); D-30 gate exercised
- AC-C28-08: crash-recover resume restores `session.id`; E-C28-02 fires on missing JSONL
- AC-C28-09: auth-expiry (E-C28-03) surfaces in OTLP stream
- AC-C28-10: OAuth-only, no key egress

**Per-task DoD:** each task's artifact (config block, hook, env, partition) is version-controlled in a pack (C02) and exercised by at least one run with telemetry captured.

**Component DoD:** an `implementer` rig agent completes a real bead end-to-end with full trajectory in CXDB (via C24), and the three gap spikes (G12/G13/G34) have written findings in `_meta/review-log.md` — closed by escalation, not by silent assumption.

## 7. E-code coverage matrix

Each AC exercises at least one E-code or asserts its absence on the happy path:

| E-code | AC that verifies it | Mode |
|---|---|---|
| E-C28-01 | AC-C28-01 (asserts absent); AC-C28-03 prerequisite | Absent on happy path; trigger: missing `~/.claude.json` |
| E-C28-02 | AC-C28-08 | Asserted present when JSONL missing |
| E-C28-03 | AC-C28-04, AC-C28-09 | PreToolUse deny (AC-04); auth-expiry (AC-09) |
| E-C28-04 | T10 spike | Rate-limit ceiling; quantify not design |
| E-C28-05 | AC-C28-02 | Asserted present when IS_SANDBOX absent as root |
| E-C28-06 | AC-C28-06 | Asserted absent when hook binary present; trigger by removing binary |
| E-C28-07 | AC-C28-06 | Asserted present when MCP server unreachable |
| E-C28-08 | AC-C28-07 | Partition-violation gate (D-30 surface) |
