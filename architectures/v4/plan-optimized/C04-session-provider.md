# C04 — Session & provider runtime  (Build Plan, Track B)

> Source / Spec ref: spec-optimized/C04-session-provider.md

## 1. Work breakdown

| id | task | size | prereqs |
|---|---|---|---|
| T1 | **Freeze the `SessionProvider` interface** (the ~18-method contract: `Create`/`Exec`/`Attach`/`Resume`/`Heartbeat`/`Liveness`/`Drain`/`Destroy`/`Health`) + the `SessionSpec` input shape. Distill from Gas City `runtime.Provider` (§3.6). | M | C01 dispatch boundary named |
| T2 | **Define the data schemas:** `Session`, `ResumeToken` (with the explicit fidelity map), `CapabilityBinding`, `CredentialSource` rung enum. | M | T1 |
| T3 | **tmux provider adapter** — the v4 default/floor backend; wraps Gas City's tmux runtime; passes the conformance suite. | L | T1 |
| T4 | **`CredentialSource` ladder (DELTA-03)** — Max-OAuth default adapter + Agent-SDK-credit + metered-API rungs; downgrade-event emission. | M | T1, T2 |
| T5 | **Isolation-at-spawn enforcement (DELTA-05)** — apply C43 capability profile + C42 work-partition/worktree at `Create`, before first command. | M | T2, C42/C43 binding schemas |
| T6 | **Resume path (DELTA-02)** — persist `Session`, mint/consume `ResumeToken`, report fidelity contract; bind `session.id`↔`gas_city_session_ref`. | L | T2, T3 |
| T7 | **Liveness/zombie (DELTA-04)** — heartbeat + last-progress emission; `zombie` transition; F22 signal to event bus. | M | T3 |
| T8 | **Multi-session lifecycle (DELTA-06)** — pool, ceiling, ordered drain, supervised restart. | M | T3, T6 |
| T9 | **Attribution + event plumbing** — `session.created/resumed/ended/downgraded` stamped with `created_by` + `session.id` to C23. | S | T1, C01/C41 |
| T10 | **`runtimetest/conformance.go` battery** — the contract suite every backend must pass (incl. the isolation-at-spawn and resume-fidelity tests). | L | T1; grows with each delta |
| T11 | **subprocess provider adapter** — second backend, proves the contract is real (acceptance #1). | M | T1, T10 |

## 2. Dependency graph

- **Upstream (must precede):** C01 (hosts C04; declares the Provider boundary and supplies attribution/event mounts). C03 contract (provider selection from config). Co-design schemas from C42 (work-partition) and C43 (capability profile) — only their *shapes* block T5, not their full implementations.
- **Downstream (waits on C04 contracts):** C28 (its sole dep — needs `OpenSession`/`ResumeSession`/`session.id`/credential injection/capability binding), C05 (routes to sessions), C06 (addresses sessions), C24/C25 (consume `session.id`), F22 anomaly detection (consumes liveness).
- **Critical path:** T1 → T2 → T3 → T6 (resume is the highest-value, highest-uncertainty capability and the corpus's `Partial`/F16 risk). T10 grows alongside and gates every backend.

## 3. Parallelization

Once **T1+T2 freeze the interface and schemas**, these fan out independently:
- **Stream A (default backend):** T3 tmux adapter → T6 resume → T8 multi-session.
- **Stream B (credentials):** T4 ladder — independent of the backend mechanics; only needs `SessionSpec`.
- **Stream C (isolation seam):** T5 — independent, blocked only on C42/C43 binding shapes; co-developed with those teams.
- **Stream D (observability):** T7 liveness + T9 attribution — ride the event-bus seam, independent of resume.
- **Stream E (conformance):** T10 authored in parallel from the frozen contract; T11 subprocess adapter validates it.

## 4. Interfaces-first / contract milestones

Freeze **before any dependent builds**:
1. **`SessionProvider` interface + `SessionSpec`** (T1) — unblocks C28 to build against a stub session, and unblocks all five internal streams.
2. **`Session` / `ResumeToken` schemas** (T2) — unblocks resume and any consumer of session identity (C24/C25 correlation key).
3. **`CredentialSource` rung enum + downgrade event** (T4 contract) — unblocks C28's fallback-adapter assumption (G12) and cost attribution (C29/cost).
4. **`CapabilityBinding` shape** (T5 contract) — the C04↔C43↔C42 co-design seam; freeze early so the three teams build to the same launch contract.
5. **Lifecycle event names** (`session.created/resumed/ended/downgraded`, `created_by`+`session.id`) — unblocks C23/C24/C25/F22 consumers.

## 5. Risks & de-risking order

1. **Resume fidelity (F16, highest uncertainty)** — spike T6 first: prove a killed mid-turn session resumes with work-graph intact and an *honest* fidelity report. This retires the corpus's `Partial` rating and the §12:512 Gas City↔Claude-Code session-id binding unknown.
2. **Isolation-at-spawn actually enforces (G31/G21/G28)** — spike T5's attempted-access test early: a profile denying network/`scenarios`-read must fail at the OS boundary on first command. This is the load-bearing security claim; if it can't be enforced at spawn, the pre-twins exposure window is *not* bounded and C43 must reconsider permitting such profiles.
3. **Credential ladder under Max ToS (G12)** — validate that the metered-API fallback is actually reachable/permitted (the corpus contradiction: §4.1 "no separate API key" vs. risk-register "have API-key fallback ready"). De-risk by confirming the rung exists before depending on it.
4. **Conformance suite is real** — T11 subprocess adapter is the proof that the contract isn't tmux-shaped; build it early enough to catch leaks.

## 6. Definition of done

- **Per-component:** all 7 spec acceptance criteria pass, gated by `runtimetest/conformance.go`. Specifically: contract holds across tmux + subprocess backends (#1); resume restores work-graph + reports accurate fidelity (#2); isolation-at-spawn blocks denied network/holdout-read at the OS boundary (#3, the security gate); credential ladder downgrades observably and fails-explicit when exhausted (#4); zombie detection fires within threshold (#5); every lifecycle event carries `created_by`+`session.id` (#6); N-session drain produces resumable tokens (#7).
- **Per-task:** each backend adapter passes the full conformance battery; each delta has a corresponding conformance test (no delta claimed without a test producing its signal). The first-checkpoint criterion (README:537 "Claude Code runs in the Gas City tmux runtime with attribution flowing into beads") is met by T3+T9.
- **Open questions** (Gas City↔CC session-id binding fidelity; pre-twins network-axis residual; credential-rung concurrency ceiling) are recorded in `_meta/review-log.md`, not silently closed.
