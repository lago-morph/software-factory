# C04 — Session & Provider Runtime  (Build Plan, canonical track)

> Source / Spec ref: spec/C04-session-provider.md (sweep-2)
> Status: sweep-2

## 1. Work breakdown (updated for Sweep-2 depth)

| Task | Description | Size | Prereqs |
|---|---|---|---|
| T1 | **Adopt the tmux Provider (Phase-0 floor).** Configure Gas City's native tmux runtime as the default Provider; `[[agent]] provider = "claude"` launching the Claude Code CLI in a tmux-backed session (README Phase 0 L361; F7 harvest-verified). No custom code — config. `[session] provider = "tmux"` in `city.toml`. | S | C01, C03 |
| T2 | **Env injection.** Inject the §13.2 `env = { … }` block (OAuth-derived Claude Code auth + `CLAUDE_CODE_ENABLE_TELEMETRY`/`OTEL_*`/`OTEL_LOG_RAW_API_BODIES`) into every `Start`/`Resume` call, so I3 (env totality) holds. Exact OTEL key set confirmed against pinned `gc` (G11). | S | T1, C03 |
| T3 | **Working-dir / partition binding.** Bind the session's working dir + read/write partition from C42 (AI-CONTEXT §13.3) into `SessionSpec.workdir` and `rig_name` at Start. | S | T1, C42 |
| T4 | **Session-id emission + log seam.** Surface the stable `SessionID` and the parsed Claude Code JSONL (`internal/sessionlog`) so C06/C24/C21 can key on it (AI-CONTEXT §5.4). Freeze the id-stability contract (I4). Emit `claude_session_id` after first JSONL line parsed. | M | T1 |
| T5 | **Continuity: detach/suspend.** Prove a session outlives client detach (`state="detached"`) and can be suspended (`state="suspended"`) without teardown (I2; the idle-burn lever). AC-C04-02. | M | T1 |
| T6 | **Resume by id — three modes.** Wire all three `ResumeMode` values (`reattach`, `cold-pickup`, `crash-recover`) as specified in §5.3. `cold-pickup` implements `gc converge resume <bead_id>` (AI-CONTEXT §16). `crash-recover` re-spawns and restores `claude_session_id`; increments `resume_count`. Freeze the escalation contract (§5.3: C04 returns E-C04-04; caller owns re-dispatch/operator gate). | M | T4, T5, C19/C20 |
| T7 | **Deployment prerequisites gate.** Before any `Start` attempt, validate §4.2 onboarding fields (`~/.claude.json` entries) and `IS_SANDBOX=1` (F12, harvest-verified). Return E-C04-01 or E-C04-02 on failure. Entrypoint writes the per-workdir trust entries at container-start. | S | T1 |
| T8 | **Provider conformance harness.** Stand up `runtimetest/conformance.go` against the tmux Provider (AI-CONTEXT §3.6); proves I1 seam isolation. AC-C04-07. | M | T1 |
| T9 | **Alternate-Provider stubs (subprocess/exec/k8s).** Confirm the seam is substrate-agnostic by sketching a second Provider that passes the conformance suite. No production k8s build on the canonical track — proof of swappability only. | M | T8 |
| T10 | **Error taxonomy wiring.** Wire E-C04-01 through E-C04-08 to their respective method call sites (§6.1). Verify each AC that exercises a failure path hits the correct E-code. | S | T1–T7 |
| T11 | **G12 / OQ-1 auth-swap seam documentation.** Document (not design) where a future Provider/auth swap lands behind C04's seam if Max subprocess automation is restricted (§5.5 auth-swap seam). Capture for review-log. No API-key auth design on the canonical track. | S | T8 |

## 2. Dependency graph

Critical path: **C01 (Gas City) → T1 (tmux Provider up) → T4 (session-id + log seam) → T6 (resume by id)**.

- **T1 is the gate**: it is also C28's gate — nothing in the agent loop runs until C04 hosts a session.
- **T7 (prerequisites gate)** must land before T1 is usable in production; bake it in with T1.
- **T4 freezes the session-id contract** that C06/C24/C21/C22 all depend on; highest-leverage early freeze.
- **T6 (resume)** needs T4 (id) + T5 (continuity) + the durable bead linkage (C19/C20).
- **T8 (conformance)** is independent of A/B workstreams; freezes the seam-isolation proof.
- **Must precede C04:** C01 (Session/Provider machinery is Gas City's), C03 (config selects Provider + env), C42 (T3 working-dir binding).
- **C04 must precede:** **C28** (its sole declared dependent — runs inside the session), C06/C24/C21 (key on session-id).

## 3. Parallelization

After T1 + T7 land (the deployment-ready session spawn gate), four independent workstreams fan out:

- **WS-A (identity/observability seam):** T4 — session-id + JSONL log seam. The contract C24/C21/C06 stub against; build first, in parallel with others. Freeze `SessionID` + `claude_session_id` + `SessionLogReader` interface early.
- **WS-B (continuity + resume):** T5 + T6 — detach/suspend + all three resume modes. Independent of id-emission internals once T4's contract is frozen. T5 must precede T6.
- **WS-C (substrate-agnosticism):** T8 + T9 — conformance suite + alternate-Provider stub. Independent of A/B; proves I1.
- **WS-D (env + partition):** T2 + T3 — env injection + partition binding. Small, run parallel to all three as soon as T1 lands.

T10 (error taxonomy wiring) and T11 (auth-swap seam doc) are tail tasks; T10 requires all method call sites from T1–T7 to be present.

## 4. Interfaces-first / contract milestones (freeze early)

1. **`runtime.Provider` interface (load-bearing seam)** — freeze the full 11-method surface (spec §3.1 signatures) FIRST. C28/C05/C03 bind only to this (I1); freezing it lets C28 build against a stub Provider in parallel with C04's real tmux implementation. **Target: before T1 merges.**
2. **`SessionID` + `SessionState` + `ResumeMode` types (T4)** — id stability across detach/resume (I4) + the parsed-JSONL access shape. Freeze so C06/C24/C21/C22 build their parent-chaining against it in parallel. **Target: immediately after T4.**
3. **Env-injection contract (T2)** — the §13.2 env map is injected verbatim and totally (I3). Freeze so C28 (telemetry) + C25 (sink) can rely on it.
4. **Resume-mode contract (T6)** — `ResumeMode` values + escalation contract (§5.3: C04 returns E-C04-04; caller owns escalation). Freeze so the bootstrap-resume path (C52) and cold-pickup (AI-CONTEXT §16) bind to it.
5. **E-code identifiers (T10)** — freeze E-C04-01 through E-C04-08 identifiers before AC tests are written, so AC cross-references are stable.

## 5. Risks & de-risking order

1. **G12 — Max subprocess-automation permanence (highest risk, shared with C28).** Spike first: confirm `tmux + claude` provider runs unattended under Max; document where a Provider/auth fallback would plug into the seam (§5.5). C04 is the *location* of the fallback; the fallback auth itself is undesigned in v4 — record (T11), do not invent.
2. **F12 deployment prerequisites.** The three onboarding dialogs + `IS_SANDBOX=1` (harvest-verified) are production blockers. The entrypoint must write `~/.claude.json` fields before any session starts; spike this with a real container before T1 is merged. Failure mode: E-C04-02, session never spawns.
3. **Resume fidelity (T6 crash-recover).** The riskiest functional claim — "same SessionID + Claude Code session-id restored" across crash. Spike against a real crash scenario early; the Partial fidelity rating (F16) is the faithful position but "durable session context restored" needs empirical verification.
4. **Seam isolation / Provider swappability (T8/T9).** Prove `runtimetest/conformance.go` passes for a second Provider; this underpins I1 and the entire "Provider swap doesn't touch C28" claim.
5. **Env totality (T2).** Verify no session starts without the full OAuth+OTEL env (I3) — a missed var breaks the C24→C27 observability chain.
6. **G11 (exact OTEL key names).** The exact key names for `CLAUDE_CODE_ENABLE_TELEMETRY`, `OTEL_*`, `OTEL_LOG_RAW_API_BODIES` need confirmation against a pinned `gc` install before T2 is called done.

## 6. Definition of done

**Per spec ACs (each must pass):**
- AC-C04-01: E2E session start with tmux Provider + stable SessionID + state=running.
- AC-C04-02: Detach/reattach continuity; session-id unchanged.
- AC-C04-03: Cold-pickup resume via `gc converge resume`; session-id unchanged.
- AC-C04-04: Crash-recover resume; same SessionID; resume_count incremented; downstream parent-chain intact.
- AC-C04-05: Resume-failure returns E-C04-04; caller receives escalation signal; C04 does not re-dispatch.
- AC-C04-06: Missing prerequisites returns E-C04-01 or E-C04-02 before pane creation.
- AC-C04-07: Provider conformance suite passes for tmux + one alternate stub.
- AC-C04-08: Teardown timeout returns E-C04-05; orphan reaped by tini.
- AC-C04-09: No code above C04 references ProviderKind (import/usage audit passes).
- AC-C04-10: Every session's turns carry the claude_session_id and full OTEL env.

**Per-task DoD:** each task's artifact (config block, method implementation, conformance test, resume wiring) is version-controlled (pack / `city.toml`, no Go fork) and exercised by at least one real session with telemetry + session-id captured.

**Component DoD:**
- A dispatched bead runs end-to-end inside a C04 tmux session.
- The session survives a forced restart and resumes by id (all three modes verified).
- The conformance suite passes for the tmux Provider plus one alternate-Provider stub.
- The G12 auth-swap seam finding is written to `_meta/review-log.md` (closed by escalation, not silent assumption).
- E-C04-01 through E-C04-08 are all exercised by at least one AC test each (E↔AC cross-reference verified).
- The deployment prerequisites gate (T7 / F12) is validated in a containerised environment before first production deployment.
