# C04 — Session & Provider Runtime  (Spec, Track A)

> Source: AI-CONTEXT §3.2 concept 1 "Session" (L85), §3.6 extractability findings (L131–135), §6.3 Kilroy multi-mode resume (L268–270), §13.2 config blocks (L569–580), §16 cold-pickup resume (L694–699); README §"Principle 2 — Three-layer architecture" (L113–124), §Phase 0 (L353–374); component-inventory C04 row (Depends on C01; Maps from A27, A20b, B73, B85; Key gap G12).
> Inventory ID: C04   Kind: component   Status: sweep-1

## 1. Purpose & responsibility

C04 is the **session & provider runtime**: the stable, named execution context inside which an agent
process (C28) runs, backed by a pluggable **Provider** (`tmux` / `k8s` / `subprocess` / `exec`), with
**cross-session continuity and resume**. It is Gas City's "Session" concept — *"Stable runtime backed by
Provider (tmux/k8s/subprocess/exec)"* (AI-CONTEXT §3.2 concept 1, L85) — adopted wholesale, not rebuilt.

It is responsible for:
- **Owning process lifecycle** for a unit of agent work: start, attach/detach, suspend, resume, stop of
  the backing process, independent of any single client connection (the tmux runtime is the default
  Provider per README L119 "Use Claude Code directly via Gas City tmux runtime", Phase 0 L361 "one
  `[[agent]]` pointing at Claude Code via the tmux provider").
- **Presenting the `runtime.Provider` interface** (~18 methods) as the single stable seam between Gas City
  and the backing execution substrate (AI-CONTEXT §3.6 L133). Swapping `tmux`→`k8s`→`subprocess`→`exec`
  is a Provider swap behind this interface; nothing above it changes.
- **Injecting the session environment** into the backing process: the `[[agent]]` `env = { … }` block
  (OAuth-derived Claude Code auth + `CLAUDE_CODE_ENABLE_TELEMETRY` / `OTEL_*` / `OTEL_LOG_RAW_API_BODIES`,
  AI-CONTEXT §13.2 L572–580) and the working directory / partition for the run.
- **Cross-session continuity** — *"Resume after agent restarts"* via **Gas City session resume + Claude
  Code session-id** (README L240, "Native", MIT). The session survives agent process restarts and sandbox
  death; a later attach resumes the same logical session.
- **Carrying the session-log seam** — `internal/sessionlog` parses the backing process's Claude Code JSONL
  (AI-CONTEXT §5.4 L229, §3.6 L133); C04's session-id is the parent-chain key downstream stores key on.

**What it is explicitly NOT:**
- NOT the **agent loop** (C28). C04 starts/hosts/resumes the process; the multi-turn reason→tool→observe
  loop *inside* it is C28 (C28 spec §1 "C28 *runs inside* a C04 session"; AI-CONTEXT §2 L48–52 separates
  LLM-client/agent-loop from the session that hosts them).
- NOT the **provider/model abstraction in the LLM sense** (which model answers a turn). "Provider" here is
  the **execution-substrate** Provider (tmux/k8s/subprocess), not the LLM provider; model routing is C29.
- NOT the **dispatcher** (C05 Sling). Sling decides *which* agent/pool a bead goes to and asks C04 to host
  it; C04 does not route work (AI-CONTEXT §3.2 concept 8).
- NOT the **work-graph / persistence** (C19/C20 beads, C21 CXDB). C04 emits a session-id and a JSONL
  stream; it does not own the durable trajectory or bead ledger.
- NOT **rig/partition policy** (C42). C42 declares read/write partitions and worktree isolation *per run*;
  C04 binds the working directory/env C42 specifies but does not author the partition policy.
- NOT a **scheduler / autoscaler**. C04 hosts one session per backing process; horizontal scale across
  many seats/sessions is not specified by v4 (see §6, G34 deferral).

## 2. Context & dependencies

| Direction | Piece | Relationship |
|---|---|---|
| Upstream (hosts C04) | **C01 Gas City substrate** | C04 *is* a Gas City native concept; the `gc` binary owns the Session/Provider machinery. C04 = the faithful spec of that adopted concept. |
| Upstream (asks C04 to host) | **C05 Sling / C01 dispatch** | Routes a bead/wisp to an agent/pool; C04 starts or resumes the session that runs it. |
| Upstream (configures C04) | **C03 config / C42 rig** | `[[agent]] provider=…` + `env` (C03, AI-CONTEXT §13.2); `read/write_partition` + worktree (C42, §13.3). |
| Downstream (runs inside C04) | **C28 agent loop** | The Claude Code subprocess C04 launches/resumes; C28 consumes the Provider surface and the injected env. |
| Downstream (keys on C04's id) | **C06 messaging, C24 bridge, C21 CXDB** | `session.id` is the attribution + parent-chain key (AI-CONTEXT §5.4 L229); C24 maps it to CXDB parent-turn pointer. |

C04's sole *declared* dependency is **C01** (component-inventory). It is **not foundational** but it is
**C28's sole declared dependency** — the execution context the agent loop runs in.

## 3. Interfaces / contracts (sweep-1: named + described)

**The `runtime.Provider` interface (the load-bearing seam).** ~18 methods, importing only stdlib + 4
internal packages (`internal/runtime`, `internal/sessionlog`, `internal/shellquote`, `internal/overlay`);
a `runtimetest/conformance.go` contract suite travels with it (AI-CONTEXT §3.6 L133). Named method
*families* (signatures are sweep-2):

1. **Lifecycle** — start a session (spawn backing process in a working dir with injected env), stop it,
   query liveness/status.
2. **Attach / detach** — connect a client to a running session and disconnect without killing it (the
   property that makes tmux/k8s sessions outlive any one client; the basis of resume).
3. **Resume** — re-bind to an existing session by id after an agent or harness restart (Gas City session
   resume + Claude Code session-id, README L240). Kilroy contributes the **multi-mode resume** pattern
   (AI-CONTEXT §6.3 L268 — transfusion exemplar).
4. **I/O streaming** — stream stdout/stderr (the Claude Code JSONL) out of the session; inject input in.
5. **Environment / placement** — set the working directory and the `env` map (OAuth + OTEL vars) at start.
6. **Session-log access** — surface the parsed session log (`internal/sessionlog`) and the session-id.

> [FAITHFUL-FILL] v4 states the interface exists (~18 methods) and names its package imports + conformance
> suite, but does not enumerate the methods. The six families above are the minimal faithful grouping
> implied by "Session = stable runtime with resume backed by a Provider" + the named imports
> (`internal/runtime` ⇒ lifecycle, `internal/sessionlog` ⇒ log access, `internal/shellquote` ⇒ command
> construction for start, `internal/overlay` ⇒ working-dir/filesystem placement). No method is invented
> beyond what these imports + the resume requirement entail; exact signatures are deferred to sweep-2.

**Inbound contracts:**
- **Host-a-session request (from C05/C01)** — given an `[[agent]]`/`[[rig]]` selector + bead context,
  start or resume a session for it.
- **Config surface (from C03)** — `[[agent]] provider = "claude"` selects the LLM-side preset; the
  Provider kind (`tmux`/`k8s`/`subprocess`/`exec`) is the execution-substrate selector; `env = { … }`
  (AI-CONTEXT §13.2 L572–580) is injected verbatim.
- **Partition/worktree binding (from C42)** — the working dir + read/write partition for the session
  (AI-CONTEXT §13.3 L586–597).

**Outbound contracts:**
- **Provider surface to C28** — the running process + its stdio; C28 runs its loop inside it.
- **Session-id emission** — a stable id keyed on by C06 (messaging), C24 (bridge → CXDB parent-turn),
  C21/C22 (trajectory parent-chain). (AI-CONTEXT §5.4 L229 "parent-chain via `session.id`".)
- **Resume handle** — `gc converge resume <bead_id>` is the operator-facing resume entry (AI-CONTEXT §16
  L699); the in-progress build is found via its `factory_build_in_progress` bead (§16 L695) and resumed.

**Invariants:**
- **I1 (substrate-agnostic seam):** everything above C04 binds only to `runtime.Provider`; the Provider
  kind is swappable without changing C28/C05/C03 (AI-CONTEXT §3.6 — the deliberately vocabulary-free
  runtime). The `runtimetest/conformance.go` suite is the proof obligation for any Provider.
- **I2 (continuity):** a session outlives any single client connection and survives an agent-process
  restart; resume by id restores the same logical session (README L240). Restoration is faithfully
  **Partial** for a *crashed* (vs cleanly detached) session — the durable session context (work-graph
  linkage + Claude Code session-id) is restored, but in-flight-turn / KV-cache state is not guaranteed
  to survive (F16, §6).
- **I3 (env injection is total):** C04 injects the OAuth-derived auth + full OTEL env block (§13.2) at
  every session start/resume, so that — to the extent the adopted Gas City session-config mechanism applies
  the `env` map without bypass — no turn runs un-telemetered or unauthenticated (C28 I1/I3 depend on this).
  The *injection* is C04's; the *no-bypass totality* is an adopted-substrate property verified by the
  `runtimetest/conformance.go` gate (AC5), not a guarantee C04-the-spec independently enforces.
- **I4 (id stability):** the session-id that downstream stores key on is stable across detach/resume.

## 4. Data model / state

C04 owns **session-handle state**, not durable work/trajectory state.

| State | Owner | Notes |
|---|---|---|
| Session handle (id, Provider kind, backing pid/pod, working dir, status) | C04 (in Gas City) | The live registry of sessions; the thing resume re-binds to. |
| Injected env (OAuth-derived auth, OTEL vars) | C04 at start; values from C03 §13.2 | Set per session; secrets handling is unspecified by v4 (G37, deferred — not C04's gap). |
| Session log (Claude Code JSONL) | Backing process; parsed via `internal/sessionlog` | C04 surfaces it; C24 ships it to CXDB. C04 does not durably own it. |
| Resume linkage (session-id ↔ `factory_build_in_progress` bead) | C19/C20 beads, not C04 | C04 resumes *by* id; the bead carrying the id is the work-graph's (AI-CONTEXT §16). |

**Lifecycle / state machine (named; diagram is sweep-2):**
`(none) → started → {running ⇄ detached} → suspended → resumed → running → stopped`. Detach/suspend
preserve the session; stop tears it down. Resume transitions an existing (detached/suspended/crashed)
session back to running by id.

> [FAITHFUL-FILL] v4 names "Native" resume and Kilroy "multi-mode resume" (README L240; AI-CONTEXT §6.3,
> §16) but does not enumerate the modes. The minimal faithful state set above is the smallest machine that
> supports "session outlives client + survives restart + resume by id"; the concrete *modes* (e.g.
> resume-attached vs resume-detached vs resume-from-crash) are deferred to sweep-2 and the Kilroy exemplar.

## 5. Behavior

**Start a session (dispatch path):**
1. C05/C01 routes a bead to an `[[agent]]`/`[[rig]]`; C04 is asked to host it.
2. C04 resolves the Provider kind from C03 config and the working dir + partition from C42.
3. C04 starts the backing process (e.g. tmux pane / k8s pod / subprocess) with the §13.2 env injected and
   the OAuth-derived Claude Code auth available.
4. C04 returns a session handle + stable session-id; C28 begins its loop inside it.

**Suspend / detach:** a client may detach (tmux) or the run may be suspended; the backing session persists
and idle-burn is avoided (the suspension lever C28 §6 leans on for the single-seat cost ceiling).

**Resume (cold-pickup path, AI-CONTEXT §16):**
1. Find the in-progress build's bead: `gc bd find --type factory_build_in_progress` (§16 L695).
2. `gc converge resume <bead_id>` (§16 L699) is the **workflow-level** resume entry (§16 step 5); it drives
   C04 to re-bind the session by id and restore Claude Code session context (Gas City session resume +
   Claude Code session-id, README L240). (The §16 command resumes the *build workflow*; the session re-bind
   is the C04-owned action it triggers — these are distinct seams, named here so they are not conflated.)
3. C28's loop continues from the restored context; the session-id is unchanged (I4), so downstream
   trajectory parent-chaining stays intact. Restoration is **Partial** (F16, §6): durable session context
   is restored, KV-cache / in-flight-turn state may be lost.

**Degraded behavior:** if the backing process dies, the session is recoverable by resume so long as the
session-id ↔ bead linkage survives (it lives in the durable bead store, not in C04). If resume fails, the
work re-enters via its bead — but v4 does not specify a resume-failure escalation contract (deferred, §6).

## 6. Failure modes & handling

| F-mode | Applies how | Handling per v4 |
|---|---|---|
| **F31** Substrate safety floor = weakest adapter | C04 *is* the substrate adapter layer; the default Provider is tmux and the only agent is Claude Code, so the floor is single and well-defined | Addressed by the single-adapter / single-Provider choice (F-MODE-COVERAGE L73, L148: "v4 uses only Claude Code via Gas City tmux runtime; floor is well-defined and stable"). |
| **F16** Resume-fidelity decay | C04 owns resume; a process/sandbox death mid-build is recovered by re-binding the session by id, but a *crashed* (vs detached) session is restored from the durable bead + Claude Code session-id, not a live backing process | **Partial** per F-MODE-COVERAGE L33 ("CXDB trajectory replay + Gas City session resume; **Partial — KV cache loss inherent**"). C04 restores the durable session context (work-graph linkage + Claude Code session-id, README L240) so net work is not lost and downstream parent-chaining stays intact (I4); but the in-flight-turn / KV-cache state is **not** guaranteed to survive — resume is faithfully *Partial*, not lossless. C04 does **not** build a fidelity-token mechanism for this (that is a Track-B `[DELTA]`); it records the canonical Partial rating and defers an explicit fidelity contract + resume-failure escalation to sweep-2 (OQ2). |
| **F22** Zombie agents | A run's process can stall/silently die while the session is "in flight"; the *session liveness* C04 hosts is the signal source | **Addressed at the loop level** per F-MODE-COVERAGE L44 ("Anomaly detection on session liveness (PyOD on telemetry)") — **not C04-native**. C04 hosts the session whose liveness is observed and surfaces session status (§4 handle `status`); the *detection* is anomaly-detection's (C36) and the *re-dispatch* is the reconciler's (C18) re-invoking C05 (C05 §6 F22 — C05's contribution is being re-invokable). C04 must **not** build heartbeat/zombie machinery (that is the dropped Track-B DELTA-04); it provides the session-status surface those consumers read. |

**Gap-driven failure mode (assigned: G12):**

> [AMBIGUITY: G12] **Does unattended Claude-Code-under-Max subprocess automation stay permitted for L4/L5
> operation — i.e. is C04's `claude`-provider tmux/subprocess session a durable foundation?**
> Reading A: AI-CONTEXT §4.1 (L146) — "Subprocess automation of `claude` CLI is officially supported";
> §3.6/README commit to the tmux Provider running Claude Code as the Phase-0 floor → C04's session as
> specced is valid indefinitely.
> Reading B: §14 risk register rates "Claude Code Max policy changes" Low/High with mitigation "have
> API-key fallback ready" — but §4.1 (L144) says "No separate API key issued" under Max, so the fallback
> contradicts the auth model and is **named but not designed**. If Max revokes subprocess automation, the
> `claude` provider preset C04 hosts has no sanctioned auth path.
> **Chosen (most consistent with v4):** Reading A is the operating assumption — v4 commits to Max-supported
> subprocess automation as the substrate floor (it is the basis of Phase 0, P2, F31, and the whole
> single-adapter argument). C04's relevance to G12 is **structural, not authorial**: because everything
> binds only to `runtime.Provider` (I1), a future provider swap (Agent-SDK-Max path, June 15 2026,
> §4.2 L151; or a k8s/subprocess Provider under a different auth) is **mechanically a Provider swap behind
> C04's seam** — C04 is the *place* the fallback would land, but the fallback auth path itself is C28/C29
> auth territory and is **undesigned** in v4. This is a deferral, not a resolution → review-log. C04 must
> not invent the API-key auth path (Track A); it records that its seam is where a future Provider/auth swap
> plugs in.

## 7. Cross-cutting

- **Security:** C04 injects OAuth-derived Claude Code auth + the OTEL env; it must keep OAuth tokens inside
  the Claude Code process (C28 I1: tokens never leave Claude Code/claude.ai, AI-CONTEXT §4.1 L147). Secrets
  management for the `env = { … }` block is **unspecified by v4** (G37) — flagged, not owned by C04.
- **Cost:** session **suspend/detach** is v4's lever against idle Max burn (supports C28's single-seat
  ceiling mitigation, C28 §6); no cost model exists in v4 (G32, deferred).
- **Scale:** C04 hosts **one session per backing process**; horizontal scale across multiple seats/sessions
  (the single-Max-seat ceiling, G34) is **not specified by v4** and must not be invented in Track A
  (deferred → review-log; shared with C28 OQ3).
- **Observability:** C04 emits the stable `session.id` correlation key and surfaces the Claude Code JSONL
  via `internal/sessionlog` — the input the entire C24→C21 trajectory chain keys on (AI-CONTEXT §5.4).
- **Ops:** declarative config (C03 §13.2) selects Provider kind + env; the `runtimetest/conformance.go`
  suite (AI-CONTEXT §3.6) is the per-Provider acceptance gate. No Go fork (pack-only extension, §3.5).

## 8. Acceptance criteria & test strategy (sweep-1, high level)

- **AC1 (host a session):** a dispatched bead causes C04 to start a backing session (default: tmux running
  the `claude` provider) in the configured working dir with the §13.2 env injected, and returns a stable
  session-id. (README Phase 0 L361; AI-CONTEXT §13.2.)
- **AC2 (continuity / outlive client):** a client can detach from a running session without killing it; the
  session and its id persist (I2/I4).
- **AC3 (resume by id):** after an agent-process restart, `gc converge resume <bead_id>` re-binds the same
  logical session, restores Claude Code session context, and the session-id is unchanged (README L240;
  AI-CONTEXT §16 L694–699).
- **AC4 (Provider conformance / swap):** a Provider implementation passes `runtimetest/conformance.go`; the
  same session semantics hold under the swappable Provider kinds named in §3.2 concept 1 (AI-CONTEXT §3.6).
- **AC5 (env totality):** every started/resumed session carries the full OAuth + OTEL env so no turn runs
  un-telemetered or unauthenticated (I3).
- **AC6 (seam isolation):** C28/C05/C03 bind only to `runtime.Provider`; no code above C04 references the
  Provider kind directly (I1) — verifiable by import/usage audit.

## 9. Open questions (→ review-log)

- **OQ1 (G12, top):** If Max revokes/limits unattended subprocess automation, what concrete Provider/auth
  swap lands behind C04's seam, and does it precede or follow the June-15-2026 Agent-SDK-Max path? C04 is
  the *location* of the fallback but v4 leaves the fallback auth **undesigned**. *Shared with C28 OQ1.*
- **OQ2 (resume modes):** v4 cites "multi-mode resume" (Kilroy) and "Native" Gas City resume but never
  enumerates the modes or a resume-failure escalation contract. Which modes are in scope, and what happens
  when resume fails (re-dispatch? operator gate?)? *Needed before sweep-2 state diagram.*
- **OQ3 (G34, scale ownership):** Horizontal scale across multiple sessions/seats is unspecified. Does
  multi-session scale belong to C04 (hosting), C05 (dispatch/pool), or C29 (routing)? *Shared with C28 OQ3.*
- **OQ4 (Provider-kind selection):** v4 names tmux as the Phase-0 default and lists k8s/subprocess/exec as
  alternatives but gives no selection criterion (when does a run get k8s vs tmux?). Inferred: config-driven
  via C03; the *policy* is unstated.
