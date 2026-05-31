# C04 — Session & Provider Runtime  (Build Plan, Track A)

> Source / Spec ref: spec/C04-session-provider.md

## 1. Work breakdown

| Task | Description | Size | Prereqs |
|---|---|---|---|
| T1 | **Adopt the tmux Provider (Phase-0 floor).** Configure Gas City's native tmux runtime as the default Provider; `[[agent]] provider = "claude"` launching the Claude Code CLI in a tmux-backed session (README Phase 0 L361). No custom code — config. | S | C01, C03 |
| T2 | **Env injection.** Inject the §13.2 `env = { … }` block (OAuth-derived Claude Code auth + `CLAUDE_CODE_ENABLE_TELEMETRY`/`OTEL_*`/`OTEL_LOG_RAW_API_BODIES`) into every started session, so I3 (env totality) holds. | S | T1, C03, C25 |
| T3 | **Working-dir / partition binding.** Bind the session's working dir + read/write partition from C42 (AI-CONTEXT §13.3) at start. | S | T1, C42 |
| T4 | **Session-id emission + log seam.** Surface the stable `session.id` and the parsed Claude Code JSONL (`internal/sessionlog`) so C06/C24/C21 can key on it (AI-CONTEXT §5.4). Freeze the id-stability contract (I4). | M | T1 |
| T5 | **Continuity: detach/suspend.** Prove a session outlives client detach and can be suspended without teardown (I2; the idle-burn lever). | M | T1 |
| T6 | **Resume by id.** Wire `gc bd find --type factory_build_in_progress` → `gc converge resume <bead_id>` so a session re-binds by id after restart with session-id unchanged (AI-CONTEXT §16; README L240). Transfuse Kilroy multi-mode resume pattern (§6.3). | M | T4, T5, C19/C20 |
| T7 | **Provider conformance harness.** Stand up `runtimetest/conformance.go` against the tmux Provider as the per-Provider acceptance gate (AI-CONTEXT §3.6); proves I1 seam isolation. | M | T1 |
| T8 | **Alternate-Provider stubs (k8s/subprocess/exec).** Confirm the seam is substrate-agnostic by sketching a second Provider that passes the conformance suite (no production k8s build in Track A — proof of swappability only). | M | T7 |
| T9 | **Gap spike (G12).** Document (not design) where a future Provider/auth swap lands behind C04's seam if Max subprocess automation is restricted; capture for review-log. *No API-key auth design in Track A.* | S | T7 |

## 2. Dependency graph

Critical path: **C01 (Gas City) → T1 (tmux Provider up) → T4 (session-id + log seam) → T6 (resume by id)**.
- **T1 is the gate**: it is also C28's gate — nothing in the agent loop runs until C04 hosts a session.
- T4 freezes the **session-id contract** that C06/C24/C21/C22 all depend on; it is the highest-leverage
  early freeze (more dependents than resume itself).
- T6 (resume) needs T4 (id) + T5 (continuity) + the durable bead linkage (C19/C20).
- **Must precede C04:** C01 (the Session/Provider machinery is Gas City's), C03 (config selects Provider +
  env). C42 (T3) and C25 (T2 env target) can land concurrently.
- **C04 must precede:** **C28** (its sole declared dependent — runs inside the session), and transitively
  C06/C24/C21 keying on the session-id.

## 3. Parallelization

After T1 lands, three independent workstreams fan out:
- **WS-A (identity/observability seam):** T4 — session-id + JSONL log seam. The contract C24/C21/C06 stub
  against; build first, in parallel.
- **WS-B (continuity):** T5 + T6 — detach/suspend + resume-by-id. Independent of the id-emission internals
  once T4's contract is frozen.
- **WS-C (substrate-agnosticism):** T7 + T8 — conformance suite + alternate-Provider stub. Independent of
  A/B; proves I1.
T2 (env) and T3 (partition) are small, run parallel to all three as soon as T1 lands.

## 4. Interfaces-first / contract milestones (freeze early)

1. **`runtime.Provider` interface (the load-bearing seam)** — freeze the ~18-method surface (six families,
   spec §3) FIRST. C28/C05/C03 bind only to this (I1); freezing it lets C28 build against a stub Provider
   in parallel with C04's real tmux implementation.
2. **Session-id contract (T4)** — id stability across detach/resume (I4) + the parsed-JSONL access shape.
   Freeze so C06/C24/C21/C22 build their parent-chaining against it in parallel.
3. **Env-injection contract (T2)** — the §13.2 env map is injected verbatim and totally (I3). Freeze so
   C28 (telemetry) + C25 (sink) can rely on it.
4. **Resume contract (T6)** — `gc converge resume <bead_id>` semantics + session-id-unchanged guarantee.
   Freeze so the bootstrap-resume path (C52) and cold-pickup (AI-CONTEXT §16) bind to it.

## 5. Risks & de-risking order

1. **G12 — Max subprocess-automation permanence (highest, shared with C28).** Spike first: confirm tmux +
   `claude` provider runs unattended under Max; document where a Provider/auth fallback would plug into the
   seam. C04 is the *location* of the fallback; the fallback auth itself is undesigned in v4 — record, do
   not invent (Track A).
2. **Resume fidelity (T6).** The riskiest functional claim — "session-id unchanged + Claude Code context
   restored" across restart. Spike against a real restart + sandbox-death scenario early; v4 asserts
   "Native" but the multi-mode detail is unspecified (OQ2). De-risk before sweep-2.
3. **Seam isolation / Provider swappability (T7/T8).** Prove `runtimetest/conformance.go` passes for a
   second Provider; this underpins I1 and the entire "Provider swap doesn't touch C28" claim — and is the
   structural answer to G12.
4. **Env totality (T2).** Verify no session starts without the full OAuth+OTEL env (I3) — a missed var
   means un-telemetered turns that break the whole C24→C27 observability chain.

## 6. Definition of done

- **Per spec ACs:** AC1 (host tmux session with §13.2 env, stable id), AC2 (detach/continuity), AC3
  (resume by id, id unchanged), AC4 (Provider conformance + swap), AC5 (env totality), AC6 (seam
  isolation — no code above C04 references Provider kind).
- **Per-task DoD:** each task's artifact (config block, conformance test, resume wiring) is version-
  controlled (pack / `city.toml`, no Go fork) and exercised by at least one real session with telemetry +
  session-id captured.
- **Component DoD:** a dispatched bead runs end-to-end inside a C04 tmux session; the session survives a
  forced restart and resumes by id with an unchanged session-id and intact downstream parent-chaining; the
  conformance suite passes for the tmux Provider plus one alternate-Provider stub; and the G12 spike
  finding is written to `_meta/review-log.md` (closed by escalation, not silent assumption).
