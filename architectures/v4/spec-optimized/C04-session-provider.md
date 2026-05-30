# C04 — Session & provider runtime  (Spec, Track B)

> Source: AI-CONTEXT §2 concept #1 "Session — Stable runtime backed by Provider (tmux/k8s/subprocess/exec)" (85), §3.6 extractability ("`runtime.Provider` interface ~18 methods; imports stdlib + `internal/runtime`/`internal/sessionlog`/`internal/shellquote`/`internal/overlay`; ~20 Go files; `runtimetest/conformance.go` travels with it" — 133), §3.4 smallest install (`[[agent]] provider = "claude"` — 118), §4.1 auth (OAuth tied to Max, no API key, subprocess automation officially supported — 143–147), §4.2 Agent-SDK June-15 (151–153), §13.1/§13.2 city.toml + env-var session config (530–580), §3.5 migration tail ("session-first" CI migration in flight — 126), §11.1 "new runtime Provider" as the one fork-warranting change (476), §12 "Inspect AI's session-id model vs Gas City's: likely needs adapter layer" (512); README P2 three-layer table ("LLM client … Gas City `claude` provider preset"; "Use Claude Code directly via Gas City tmux runtime" — 119–120), P10 memory table ("Cross-session continuity | Resume after agent restarts | Gas City session resume + Claude Code session-id | Native" — 240), P0 "running one Claude Code session, no custom code" (355), "Verify Claude Code runs in the Gas City tmux runtime with attribution flowing into beads" first checkpoint (537), mermaid `CC -->|tmux| GC` (410), license rows (289/336 "Max subscription allows subprocess automation"); F-MODE-COVERAGE F16 "Resume-fidelity decay — CXDB trajectory replay + Gas City session resume | Partial — KV cache loss inherent" (33), F22 "Zombie agents — anomaly detection on session liveness" (44), F17 "Parallel agents on shared dirs — worktree isolation per session (native)" (86), F31 "Substrate safety floor = weakest adapter — single-adapter (Claude Code) | Addressed" (73), F12/F44/F56 lethal-trifecta rows (54–57); component-inventory C04 row (Runtime Substrate, component, NOT foundational, maps A27/A20b/B73/B85, depends C01, gap G12; sole declared dep of C28); _meta gaps G12 (Max-policy / API-key-fallback undesigned — assigned), G31 (lethal-trifecta isolation window — owned by C43, intersected here), G21/G28 (holdout read-isolation mechanism — owned by C42/C43, intersected at the session work-partition seam).
> Inventory ID: C04   Kind: component   Status: sweep-1
> Deltas: DELTA-01 (C04 is the **`SessionProvider` contract** — a stable ~18-method interface that Gas City's tmux runtime *implements*, not "the tmux runtime" hardcoded; the v4-relevant subset is named here so k8s/subprocess/exec providers are conformance-tested peers, not aspirational); DELTA-02 (**resume is a first-class typed handle with an explicit fidelity contract**, not the corpus's bare "session resume + session-id" — a `ResumeToken` carries what survives a restart vs. what is lost, making F16 "KV-cache loss inherent" a *declared, observable* degradation instead of a silent one); DELTA-03 (**credential/provider-policy is an injected `CredentialSource` with a designed fallback ladder** — Max-OAuth → Agent-SDK-credit → metered-API — so the API-key fallback G12 names is a built, conformance-passing adapter swap, not a contradiction left in the risk register); DELTA-04 (**session liveness is a substrate-owned, emitted resource** — heartbeat + last-progress + zombie detection are part of the provider contract, giving F22 a real signal source instead of "PyOD on telemetry" with no defined producer); DELTA-05 (**the session is the enforcement seam for capability/work-partition isolation** — every session is launched *inside* a declared C43 capability profile + C42 work-partition/worktree, so the G31 pre-twins blast-radius window and G21/G28 holdout-read window are bounded at process spawn by construction, not by agent-prompt discipline); DELTA-06 (**multi-session lifecycle is explicit**: pool, ceiling, drain, supervised-restart — the corpus only ever spec's one session; concurrent factory operation needs a defined fan-out, ceiling and crash-recovery story).

## 1. Purpose & responsibility

C04 is **the session/provider runtime**: the layer that turns "run an agent" into a *managed, attributed, resumable OS-level process* and hands the agent loop (C28) a place to live. It is AI-CONTEXT concept #1 — "Session: a stable runtime backed by a Provider (tmux/k8s/subprocess/exec)" (§2:85) — promoted from a one-line table cell into the contract every reasoning action in the factory physically runs inside.

C04 owns, as a component:

1. **The `SessionProvider` contract (DELTA-01).** A stable interface — the v4 distillation of Gas City's `runtime.Provider` (~18 methods, §3.6:133) — describing what *any* runtime backend must do: spawn a session, exec/stream commands inside it, attach/detach, resume it, report its liveness, and tear it down. Gas City's **tmux** provider is the v4 default and capability floor; **k8s**, **subprocess**, and **exec** are named peer backends behind the same contract and the same `runtimetest/conformance.go` suite that "travels with" the interface (§3.6).
2. **Session lifecycle.** Create → run → (detach) → resume → drain → destroy, including the **multi-session** case (DELTA-06): a pool of sessions, a concurrency ceiling, ordered drain, and supervised restart on crash. The corpus only ever describes one session (§3.4, P0:355); concurrent factory operation requires this.
3. **Cross-session continuity / resume (DELTA-02).** A typed `ResumeToken` binding a Gas City session to a Claude Code `session.id` (README P10:240) so an agent can be restarted after a crash, deploy, or operator detach and pick up its work-graph (beads survive in C19; the *session* survives here). The token carries an explicit **fidelity contract**: durable work-graph + conversation transcript resume, but KV-cache / in-flight-turn state is lost (F16 "Partial — KV cache loss inherent", :33).
4. **Credential / provider-policy injection (DELTA-03).** A `CredentialSource` abstraction supplying the agent's auth at spawn — default **Claude Code OAuth tied to Max** (§4.1: no separate API key, subprocess automation officially supported), with a designed fallback ladder to Agent-SDK credit (June-15, §4.2) and metered API (G12). C04 owns *where the credential comes from and how the ladder steps*, not the agent loop that uses it.
5. **Attribution + liveness plumbing (DELTA-04).** Every session carries an actor identity and `session.id` so that all work it produces is attributed (P9, README first checkpoint :537 "attribution flowing into beads"), and emits a **heartbeat / last-progress** signal that is the defined producer for zombie-agent detection (F22, :44).
6. **The isolation launch seam (DELTA-05).** A session is *always* launched inside a declared **capability profile** (C43) and a **work-partition / worktree** (C42, F17 "worktree isolation per session — native", :86). This is the single point where the lethal-trifecta blast radius (G31) and holdout-read exposure (G21/G28) are bounded *before the agent's first tool call*, by what the process is permitted to touch — not by prompt discipline.

What C04 is **NOT**:
- **Not the agent loop.** The multi-turn reason→act→observe loop, hooks/skills/MCP surface, and turn-budget logic are **C28**. C28 runs *inside* a C04 session; C04 hands it a process, a credential, a capability profile, and a resume handle, and never reasons.
- **Not the LLM client / model routing.** The OAuth handshake transport and the model-selection rules are the LLM-client layer / **C29**. C04 *injects* the credential; it does not pick the model or speak the wire protocol.
- **Not the dispatch decision.** *Which* work goes to *which* session is **C05 (sling)** on top of **C01**'s dispatch primitive. C04 materializes the session C05 routes to.
- **Not the capability/isolation *policy*.** C43 defines what a capability profile *means* (boundary typing, twins) and C42 defines partitions; C04 is the **enforcement seam that applies them at spawn** (DELTA-05), not their author.
- **Not the work-graph / trajectory store.** Beads (C19), events (C23), and CXDB trajectories (C21/C24) are where work and history persist. C04 persists *session* state and the resume handle, and stamps attribution; it does not own those stores.
- **Not Gas City.** C04 is the *contract Gas City's tmux runtime satisfies* (DELTA-01); adopting Gas City supplies the default implementation, and a future k8s/subprocess backend is a conformance-passing swap, not a rewrite (§11.1:476 names "new runtime Provider" as the one change that would even warrant a Gas City fork).

## 2. Context & dependencies

- **Depends on (declared in inventory):**
  - **C01 (Gas City substrate).** C01 hosts C04 and calls *into* it: C01's `Dispatch(work_unit, target)` routes agent work to a C04 session, and C01 supplies the `created_by` attribution stamp and event-bus mount C04 writes session-lifecycle events to. C04 is the **Provider boundary C01 declares it plugs into** (see C01 spec §3 "Outbound … the Provider boundary (→ C04)").
- **Inbound coupling (not a build-order dep, but co-designed seams):**
  - **C43 (isolation / lethal-trifecta boundary)** supplies the **capability profile** C04 applies at spawn (DELTA-05). Co-design seam: C04 owns *enforcement at process creation*; C43 owns *what the profile is*.
  - **C42 (rig / work-partition)** supplies the **work-partition / worktree** the session is confined to (F17). Same seam, filesystem axis.
  - **C03 (config / feature-flags)** — section presence (`[[agent]] provider = "..."`, `env = {...}`, future `[[rig]]`) tells C04 which provider to instantiate and with what env/credential config (§13.1–13.3).
- **Consumed by (downstream):**
  - **C28 (Claude Code agent loop)** — *C04 is C28's sole declared dependency.* C28 runs inside a C04 session and relies on C04 for spawn/resume, `session.id`, the injected Max credential, and the capability profile binding (see C28 spec §2: "C04 owns process lifecycle, the tmux runtime, session-id, resume, and attribution; the OAuth/Max credential pickup is a C04 concern C28 relies on").
  - **C05 (sling)** routes work to sessions C04 materializes.
  - **C06 (messaging)** is `depends C04` in the inventory — Mail/Nudge between agents address sessions by session identity.
  - **C24/C25 (CXDB bridge / OTLP export)** consume the `session.id` correlation key C04 guarantees on every signal (AI-CONTEXT §4.3 correlation attributes).
  - **C22/anomaly-detection (F22)** consume the liveness signal C04 emits (DELTA-04).
- **Sits at:** the **Runtime Substrate** subsystem, just above C01, in **Batch 2** of the build order (parallel with C05/C28/C29/C42 etc.). It is *not foundational* in the inventory sense (nothing in Batch 1 requires it), but it is the floor every agent invocation physically stands on.

## 3. Interfaces / contracts

Named-and-described (sweep 1; concrete ~18-method signatures, the `ResumeToken` / `CredentialSource` / `CapabilityBinding` schemas, the conformance battery, and a Mermaid lifecycle/state diagram land in sweep 2). The defining move (DELTA-01) is that C04 specifies a **`SessionProvider` role contract** with Gas City tmux as the default floor adapter, rather than hardcoding the tmux runtime.

**`SessionProvider` — the backend contract (DELTA-01).** Every runtime backend (tmux | k8s | subprocess | exec) implements:
- `Create(spec) → SessionHandle` — spawn a session. `spec` carries: provider kind, agent identity (for attribution), `CredentialSource` (DELTA-03), `CapabilityBinding` (C43 profile + C42 partition/worktree, DELTA-05), env (telemetry vars §13.2), and optional `ResumeToken`. **Pre:** the named capability profile and work-partition exist and are valid. **Post:** a live session exists, confined to its profile/partition *before* any agent command runs; a `session.created` event is stamped (`created_by`, `session.id`) to C23.
- `Exec(handle, command) → stream` / `Attach(handle) → io` — run/stream work inside the session. The agent loop (C28) drives turns through this; C04 does not interpret them.
- `Resume(token) → SessionHandle` — re-establish a session from a `ResumeToken` (DELTA-02). **Post:** durable work-graph + transcript restored; the **fidelity contract** is reported (what survived vs. lost, F16). Idempotent: resuming an already-live session is a no-op attach.
- `Heartbeat(handle) → Liveness` / `Liveness(handle)` — report `{ alive, last_progress_at, turn_active, pid/pod }` (DELTA-04); the defined producer for F22 zombie detection.
- `Drain(handle)` / `Destroy(handle)` — ordered shutdown (finish or checkpoint in-flight turn → emit `session.ended`) vs. hard teardown.
- `Health() → ProviderHealth` — backend-level readiness (tmux server up / k8s reachable / quota state).

**Inbound (what C04 offers C01 and upward):**
- `OpenSession(agent_ref, work_unit, binding) → SessionHandle` — the operation C01's `Dispatch` calls; selects the provider from config (C03), resolves the credential ladder, applies the capability binding, and returns a running session. **Invariant:** never returns a session that escaped its profile/partition.
- `ResumeSession(resume_token) → SessionHandle` — cross-session continuity entry point (README P10:240).
- `SessionStatus(session_id) → { liveness, fidelity, attribution }` — read model for C05/C22/observability.

**Outbound (what C04 requires):**
- **`CredentialSource` (→ C43/env/secret store, DELTA-03):** supplies auth at spawn via a **fallback ladder**: `MaxOAuth` (default, §4.1) → `AgentSDKCredit` (§4.2, ≥ 2026-06-15) → `MeteredAPIKey` (G12 fallback). Each rung is a conformance-passing adapter; the active rung is recorded on the session for attribution and cost (C29/cost).
- **`CapabilityBinding` (→ C43 + C42, DELTA-05):** the profile (allowed Bash/network/fs surface; twin-vs-production target) + work-partition/worktree the session is confined to.
- **Event/attribution sink (→ C01/C23/C41):** every lifecycle transition emits an attributed event.

**Invariants:**
- **Isolation-at-spawn (DELTA-05):** a session is confined to its declared capability profile and work-partition *before* its first command. There is no window in which a freshly spawned agent has broader access than its binding allows. This bounds G31 (pre-twins) and G21/G28 (holdout read) at the process boundary, independent of agent-prompt discipline.
- **Attribution-total (P9):** no session-affecting action is anonymous; `session.created`/`ended`/`resumed` carry `created_by` + `session.id`.
- **Resume-fidelity declared (DELTA-02):** `Resume` always reports its fidelity contract; it never silently presents a lossy resume as lossless (honest F16).
- **Credential-ladder monotone (DELTA-03):** the ladder is tried top-down; a downgrade (e.g., Max→metered-API) is an emitted, attributable event, never silent — so a policy change (G12) is observable, not a mystery outage.
- **Liveness-emitting (DELTA-04):** every live session emits heartbeat + last-progress; absence past threshold is the F22 zombie signal.
- **Conformance-pinned:** a provider backend is usable iff it passes `runtimetest/conformance.go` (§3.6); the tmux floor is the reference.

## 4. Data model / state

C04 owns **session state**, not work state:

- **`Session` (durable, per session):** `{ session_id (≙ Claude Code session.id), gas_city_session_ref, provider_kind, agent_identity/created_by, credential_rung, capability_profile_ref (C43), work_partition/worktree (C42), state ∈ {creating, live, detached, draining, ended, zombie}, created_at, last_progress_at }`. Persisted by the substrate (C01 storage mount); survives substrate restart so resume works.
- **`ResumeToken` (durable, DELTA-02):** `{ session_id, gas_city_session_ref, transcript_ref, work_graph_anchor (bead root), fidelity = { work_graph: durable, transcript: durable, kv_cache: lost, in_flight_turn: lost } }`. The explicit fidelity map is the F16-honest contract.
- **Owned (ephemeral, per session):** the OS handle — tmux pane / k8s pod / subprocess pid — and the attach I/O streams. Lifecycle-bound to `Session`; reconstructed on resume.
- **Not owned:** beads/work-graph (C19), events (C23), trajectories (C21/C24), telemetry (C25/26/27), the capability *policy* (C43) and partition *definition* (C42), model routing (C29). C04 *references* these and *emits into* C23; it stores none of their schemas.

**Consistency:** `Session` durability is what makes resume possible across a substrate crash — it must be persisted on the same store lifecycle C01 provides for beads/events, with the `session_id`↔`gas_city_session_ref` binding as the join key (the §12:512 "Inspect AI session-id vs Gas City" adapter concern lives at this binding).

## 5. Behavior

**Spawn (happy path):** C01 `Dispatch` → C04 `OpenSession` → resolve provider from C03 config → resolve `CredentialSource` ladder (Max-OAuth default) → apply `CapabilityBinding` (C43 profile + C42 worktree) → `SessionProvider.Create` materializes the confined process → stamp `session.created` (attribution) → hand `SessionHandle` to C28. C28 runs its loop via `Exec/Attach`; C04 emits heartbeats throughout.

**Resume (cross-session continuity, DELTA-02):** on restart/deploy/operator-reattach, C05/operator calls `ResumeSession(token)` → C04 reconstructs the OS handle, rebinds capability profile + partition, restores transcript + work-graph anchor, reports the fidelity contract (KV cache lost), and re-stamps `session.resumed`. The agent continues from its durable bead graph (P10:240, §13:699 `gc converge resume <bead_id>` is the workflow-level expression of this).

**Liveness / zombie (DELTA-04 → F22):** each live session emits `{ alive, last_progress_at }`; when last-progress exceeds threshold with no completion, C04 marks the session `zombie` and emits the signal F22's anomaly detection consumes — then `Drain`/`Destroy` per policy.

**Credential downgrade (DELTA-03 → G12):** if the Max-OAuth rung fails (policy change / auth expiry), C04 steps the ladder to Agent-SDK-credit, then metered-API, emitting an attributable `credential.downgraded` event each step. A fully-exhausted ladder fails the spawn explicitly (no silent hang).

**Multi-session drain (DELTA-06):** on substrate shutdown/redeploy, C04 drains the session pool in order (checkpoint in-flight turns to resume tokens, emit `session.ended`), respecting the concurrency ceiling on restart.

## 6. Failure modes & handling

| F-mode | C04 role | Handling |
|---|---|---|
| **F16 Resume-fidelity decay** (Partial) | Owns resume | `ResumeToken` declares the fidelity contract (DELTA-02); KV-cache loss is reported, not hidden; durable work-graph + transcript always restored so net work is not lost. |
| **F22 Zombie agents** (Addressed) | Owns liveness signal | Heartbeat + last-progress emission (DELTA-04) is the *defined producer* for anomaly detection; C04 transitions to `zombie` and drains. |
| **F17 Parallel agents on shared dirs** (Addressed) | Owns the launch seam | Each session is confined to a C42 work-partition/worktree at spawn (DELTA-05); no two sessions share a writable dir unless the partition policy says so. |
| **F31 Substrate floor = weakest adapter** (Addressed) | Owns the provider contract | Single capability floor = tmux/Claude Code; any added backend must pass `runtimetest/conformance.go` to be usable — the floor can't silently drop (DELTA-01). |
| **F12 / F44 / F56 Lethal trifecta** (G31, owned by C43) | Owns enforcement-at-spawn | C04 applies the C43 capability profile *before first tool call* (DELTA-05). **Before twins ship (Phase 0–3b), C04 is the only mechanism actually bounding blast radius** — it confines fs/network/Bash to the declared profile and defaults to twin targets where the profile demands. This is the concrete answer to "G31 is Addressed on paper but exposed in practice": the exposure window is bounded by *what the process can touch*, applied here, not by prompt discipline. C43 still owns the *policy*; C04 makes deferral of twins a *bounded* risk rather than an open one. |
| **G12 Max-policy / fallback** | Owns credential ladder | Designed fallback ladder (DELTA-03) turns the undesigned API-key fallback into a built, conformance-passing adapter swap with observable downgrade events. |
| **G21/G28 Holdout read-isolation** (owned C42/C43) | Owns enforcement-at-spawn | The implementer session is spawned with a work-partition that *excludes* `scenarios` (§13.3:596); C04 enforces this filesystem confinement at process creation — converting "agent-prompt discipline" into a launch-time boundary (still detect-only at the policy level until C43 lands real enforcement; C04 shrinks the window). |
| Substrate crash mid-session | Owns durable `Session` + resume | `Session` persisted on C01's store lifecycle; on restart, `ResumeSession` reconstructs from the token. |
| Provider backend unavailable (tmux server down / k8s unreachable) | `Health()` | Spawn fails fast with a typed error; no half-started session; C05 can retry/route elsewhere. |

## 7. Cross-cutting (security / cost / scale / observability / ops)

- **Security:** C04 is *the* security enforcement seam at the process boundary — capability profile + work-partition applied at spawn (DELTA-05). It is where G31/G21/G28 are bounded in practice before the C43/C42 policy machinery and twins fully land. Credentials are injected, never embedded in agent-visible config; OAuth tokens are never exposed to agent tooling (§4.1: "OAuth tokens NOT permitted outside Claude Code/claude.ai" — C04 keeps them in the provider, not the workspace).
- **Cost:** the active credential rung (Max vs. metered-API) is recorded per session, giving cost attribution a real source (intersects the G32 unmodeled-cost concern; C04 supplies the per-session credential/usage fact, C29/cost-model consume it).
- **Scale:** multi-session pool + concurrency ceiling (DELTA-06); the single-Max-seat throughput ceiling (G34, owned at C28) is *expressed* here as the pool size against available credential rungs.
- **Observability:** `session.id` correlation key guaranteed on every signal (AI-CONTEXT §4.3) so C24/C25 can reconstruct trajectories; lifecycle + liveness events are first-class on C23.
- **Ops:** drain/resume make redeploys and crash recovery non-destructive; the `runtimetest/conformance.go` suite (§3.6) gates any provider backend change — directly de-risking the "session-first" CI migration tail (§3.5:126).

## 8. Acceptance criteria & test strategy

1. **Contract holds across backends (DELTA-01).** The tmux provider and at least one peer (subprocess) both implement `SessionProvider` and pass `runtimetest/conformance.go`. Adding a backend is config-only.
2. **Resume is faithful-where-claimed and honest-where-not (DELTA-02, F16).** After a forced restart, `Resume` restores the work-graph + transcript and the agent continues from its bead root; the reported fidelity contract correctly flags KV-cache/in-flight-turn loss. *Test:* kill a live session mid-turn, resume, assert work-graph intact and fidelity report accurate.
3. **Isolation-at-spawn (DELTA-05, G31/G21/G28).** A session launched with a profile denying network/`scenarios`-read *cannot* reach the network or read the holdout partition on its first command — verified by an attempted-access test that fails at the OS boundary, not by inspecting the prompt. (This is the load-bearing security acceptance test.)
4. **Credential ladder (DELTA-03, G12).** With Max-OAuth disabled, the session spawns on the next rung and emits a `credential.downgraded` event; with all rungs disabled, spawn fails explicitly.
5. **Liveness/zombie (DELTA-04, F22).** A wedged session stops emitting progress; C04 marks it `zombie` and emits the detection signal within the threshold.
6. **Attribution-total (P9).** Every lifecycle event carries `created_by` + `session.id`; no anonymous session mutation passes the audit.
7. **Multi-session drain (DELTA-06).** N concurrent sessions drain in order on shutdown, each producing a resumable token; restart respects the ceiling.

## 9. Open questions

- **Gas City ↔ Claude Code session-id binding fidelity** (§12:512): the corpus flags an "adapter layer, impedance unknown" between Gas City's session model and external (Inspect AI / Claude Code) session-ids. The `session_id ↔ gas_city_session_ref` join is the load-bearing detail for resume; its exact semantics need sweep-2 verification. → review-log.
- **Pre-twins residual on the network axis (G31):** C04 enforces capability profiles at spawn, but where a profile *must* permit network for a legitimate task before twins exist, the bound is "declared egress allowlist," not full isolation. How much residual lethal-trifecta exposure remains in that case, and whether C43 should forbid network-permitting profiles entirely until twins ship, is a C04↔C43 co-design question. → review-log.
- **Credential-rung cost/throughput coupling (G32/G34):** the pool ceiling depends on how many concurrent sessions each credential rung legitimately supports under Max ToS — an unmodeled number. → review-log.
