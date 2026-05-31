# C28 — Claude Code Agent Loop  (Spec, Track A)

> Source: README §"Principle 2 — Three-layer architecture" (L113–124, L60–74), §"Concrete first steps" Phase-0 checklist (L533–543), §"Cross-session continuity" (L240), §"Event substrate" (L252); AI-CONTEXT §2 (L46–56), §4 (L139–190), §13.2 (L569–580), §13.3 (L587–596), §14 (L624); one-shot-specs §"Specs library" agent-loop row (L21).
> Inventory ID: C28   Kind: agent-role   Status: sweep-1
> Maps from: A04, A04b, A05, A28d, A28e, A28f, A28g, A28h, B20, B21. Depends on: C04. Key gaps: G12, G13, G34.

## 1. Purpose & responsibility

C28 is the **implementer worker**: the agent that turns a dispatched unit of work (a bead/wisp carrying a spec or sub-task) into running, tested software through **multi-turn reasoning + tool dispatch**. In v4's convergent **three-layer-plus-persistence** shape (AI-CONTEXT §2 L48–52 "Three-layer + persistence"; README §"Principle 2 — Three-layer architecture" L113–115) it occupies **layers 1+2 simultaneously** — it is both the *LLM client* (provider abstraction, list item 1) and the *agent loop* (multi-turn reasoning + tool dispatch, list item 2) — because v4 fixes both to **Claude Code CLI under a Claude Max subscription** (README L119–120: "Use Claude Code directly via Gas City tmux runtime", "Gas City `claude` provider preset").

It is responsible for:
- Running the **Claude Code CLI as a subprocess** under Max-OAuth auth (AI-CONTEXT §4.1 L141–147), driven by the Gas City `claude` provider preset inside a C04 session.
- Executing the agent's inner loop: read context → reason → call a tool → observe result → repeat → emit work product (code, edits, PRs, commits).
- Exposing the four **extension surfaces** Claude Code offers under Max (AI-CONTEXT §4.4 L182–190): **Skills** (`.claude/skills/`), **Subagents** (Explore/Plan/general/custom), **Hooks** (PreToolUse/PostToolUse/SessionStart/Stop), and **MCP servers** (tool layer).
- Emitting native telemetry (the OTLP env-var surface) so its full trajectory is captured (handed to C25).

**What it is explicitly NOT:**
- NOT the **provider/session runtime** — process lifecycle, tmux/k8s/subprocess backing, resume, and cross-session continuity belong to **C04** (component-inventory C04 row; AI-CONTEXT §3.2 concept 1). C28 *runs inside* a C04 session.
- NOT the **pipeline/workflow engine** — DAG orchestration, formulas, molecules, dispatch ordering belong to Gas City (C01) / Sling (C05). C28 executes one dispatched node; it does not own the graph (README L60–74 places AL *below* PE in the layer diagram).
- NOT the **model-routing policy** — which model/family/cost tier handles a given bead is **C29** (model floor & stylesheet). C28 is the floor C29 declares and routes *to*.
- NOT the **telemetry exporter or CXDB bridge** — C28 only *emits* native OTLP/raw-API-bodies; **C25** owns the export config and **C24** owns the bridge to CXDB.
- NOT the **tool-node implementations** — deterministic steps are C02/C17 tool nodes; C28 *dispatches* tools but does not define the tool-node ABI.
- NOT a **judge/scenario** role — that is a different rig (C42 partitioning, C32 judge). C28 is partitioned to `read/write = code` and explicitly excludes `scenarios` (AI-CONTEXT §13.3 L592–596, the `implementer` rig block).

## 2. Context & dependencies

| Direction | Piece | Relationship |
|---|---|---|
| Upstream (hosts it) | **C04 session/provider** | Provides the stable tmux/subprocess runtime, OAuth-credential environment, resume, and continuity. C28 is the process that runs in the C04 session. |
| Upstream (dispatches to it) | **C05 Sling / C01 Gas City** | Routes a bead/wisp to the C28 `[[agent]]` / `[[rig]]`. |
| Upstream (configures it) | **C03 config / C29 model floor** | C29 declares C28 as capability floor and routes work to it; C03 carries the `[[agent]] provider="claude"` block + env (AI-CONTEXT §13.2 L572–580). |
| Downstream (consumes its output) | **C25 OTLP export** | Receives C28's native OTLP metrics/events/traces and the `OTEL_LOG_RAW_API_BODIES` dump (→ C24 → CXDB). |
| Lateral (it invokes) | **C02 pack/tool-node ABI, C17 tool-node abstraction** | The tools C28 dispatches (subprocess tool nodes, MCP servers). |
| Lateral (it registers) | **C35 override loop** | C28's PreToolUse/PostToolUse hooks are the detection surface for the override→why→rule loop. |

## 3. Interfaces / contracts (sweep-1: named + described)

**Inbound:**
1. **Dispatch entry** — a Gas City dispatch (Sling) hands C28 a bead/wisp + working context (worktree, partition, prompt template binding). C28 starts/resumes a Claude Code subprocess for it. (AI-CONTEXT §3.2 concept 8; §13.3 rig blocks.)
2. **Provider/session contract (from C04)** — the `runtime.Provider` surface that starts the `claude` CLI subprocess, injects env (OAuth + OTEL vars), and streams stdout/stderr. C28 consumes this; it does not implement it.
3. **Config surface (from C03)** — `[[agent]] provider="claude"` with `env = { CLAUDE_CODE_ENABLE_TELEMETRY, OTEL_* , OTEL_LOG_RAW_API_BODIES }` (AI-CONTEXT L572–580); plus `.claude/{skills,hooks}` and MCP-server declarations.

**Outbound:**
4. **Tool-dispatch contract** — C28 calls tools via (a) Claude Code built-in tools, (b) MCP servers, (c) subprocess tool nodes (C02 ABI). Hooks gate each call (PreToolUse → allow/deny; PostToolUse → observe).
5. **Telemetry emission contract** — native OTLP (metrics 60s, logs 5s; traces under `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1`) + raw-API-bodies JSON to a watched dir. Correlation attrs: `prompt.id`, `session.id`, `user.account_uuid`, `organization.id`, `terminal.type` (AI-CONTEXT §4.3 L171–180). Consumed by C25.
6. **Work-product contract** — code edits, commits, PRs, and bead state transitions, attributed via session-id (README L240 "Cross-session continuity — Resume after agent restarts ... Gas City session resume + Claude Code session-id").

**Extension-surface contracts (Max, AI-CONTEXT §4.4):**
- **Skills** — multi-step workflow definitions in `.claude/skills/`.
- **Subagents** — parallel sub-work (Explore/Plan/general/custom).
- **Hooks** — PreToolUse, PostToolUse, SessionStart, Stop deterministic gates.
- **MCP servers** — the tool layer.

> [FAITHFUL-FILL] v4 names these four surfaces but does not give a registration schema. Minimal consistent choice: registration is **declarative via C03 config + `.claude/` files** (the same TOML-section-presence = feature-flag pattern Gas City uses, AI-CONTEXT §3.2 concept 4), since v4 mandates "no Go fork / pack-only extension" (§3.5 L128). No new interface invented.

**Invariants:**
- I1: C28 authenticates **only** via Max OAuth picked up from Claude Code login; OAuth tokens are **never** used outside Claude Code/claude.ai (AI-CONTEXT §4.1 L147 — a ToS hard constraint).
- I2: C28 runs **inside** a C04 session; it never owns process lifecycle directly.
- I3: Every C28 action is attributed (session-id) and telemetered (raw API bodies) — no silent turns. The no-bypass *totality* of this is not C28's to enforce: it rests on **C04 injecting the full OTEL env at every session start/resume** (C04 I3) and is verified by C04's `runtimetest/conformance.go` gate; C28 only *emits* given that injection.
- I4: C28 partition is `code`; it has **no read access to `scenarios`** (held-out integrity, AI-CONTEXT §13.3).

## 4. Data model / state

C28 owns **little durable state**; it is a compute role, not a store.

| State | Owner | Notes |
|---|---|---|
| Conversation / turn history | Claude Code (JSONL on disk) + raw-API-bodies dump | Content-addressed into CXDB downstream by C24; C28 just emits. |
| Session id / prompt id | Claude Code, surfaced via C04 | Used for attribution + parent-chaining (AI-CONTEXT §5.4 L229: parent-chain via `session.id`). |
| Skills / hooks / MCP config | `.claude/` + pack (C02) | Declarative, version-controlled; not runtime-mutable by the loop. |
| Work-graph state (beads) | C01/C20 beads, not C28 | C28 transitions beads but does not own the ledger. |

Persistence/continuity is delegated to C04 (resume) and CXDB (trajectory). C28 is restart-safe insofar as C04 + Claude Code session-id resume restore context (README L240 "Cross-session continuity").

## 5. Behavior

**Inner loop (one dispatched bead):**
1. C04 starts/resumes the `claude` subprocess with injected env (OAuth, OTEL vars) inside the assigned worktree/partition.
2. Gas City binds the prompt template + bead context as the initial prompt.
3. Claude Code runs its native agent loop: reason → propose tool call → **PreToolUse hook gate** → execute (built-in tool / MCP / subprocess tool node) → **PostToolUse hook** observes result → continue.
4. Subagents may be spawned for parallel Explore/Plan sub-work; Skills encapsulate multi-step routines.
5. Throughout, native OTLP + raw-API-bodies stream out (→ C25 → C24 → CXDB).
6. On completion/`Stop`, C28 emits work product (edits/commits/PR), transitions the bead, and the session may be suspended (C04) for later resume.

**Degraded behavior:** if a tool/MCP node fails, the loop observes the failure as a tool result and may retry/route around it (standard agent-loop semantics); hard failures surface as bead/gate events for the C11 self-healing loop. If Max auth/policy fails, see §6 (G12).

> [FAITHFUL-FILL] v4 does not spell out the per-turn loop in prose; the above is the standard Claude-Code agent loop (the very thing v4 adopts wholesale, README L120). No deviation — purely making the adopted behavior explicit.

## 6. Failure modes & handling

| F-mode | Applies how | Handling per v4 |
|---|---|---|
| **F19** Model-floor dependency | C28 *is* the floor; v4 declares Claude Code as the explicit floor | Addressed by declaration (F-MODE-COVERAGE L71); C29 owns the routing policy above it. |
| **F31** Substrate safety floor = weakest adapter | C28 is the single adapter (Claude Code only), so the floor is well-defined and stable | Addressed by single-adapter choice (F-MODE-COVERAGE L73, L148). |

**Gap-driven failure modes (must address per brief):**

> [AMBIGUITY: G12] **Does unattended Claude-Code-under-Max stay permitted for L4/L5 operation?**
> Reading A: AI-CONTEXT §4.1 (L146) states subprocess automation is "officially supported" → C28 as specced is valid indefinitely.
> Reading B: §14 (L624) rates "Claude Code Max policy changes" Low/High with mitigation "have API-key fallback ready" — but §4.1 (L144) says "No separate API key issued" under Max, so the fallback contradicts the auth model and is **named but not designed**.
> **Chosen (most consistent with v4):** Reading A is the operating assumption — v4 commits to Max-supported subprocess automation as the floor (it is the basis of P2, F31, and the whole single-adapter argument). The API-key fallback is recorded as a **latent, undesigned contingency** triggered only on a policy change. C28's spec therefore assumes Max-OAuth subprocess auth (I1) and treats provider-swap as out-of-scope until the Agent SDK Max path (June 15 2026, §4.2 L151) or an API-key path is actually designed. *This is a deferral, not a resolution — escalated to review-log.*

> [AMBIGUITY: G13 (cost/throughput vs the $200 subscription) + G34 (agent-side scale ceiling)] **Single-Max-seat throughput & cost ceiling.** (Two distinct gaps with one shared root cause and one shared deferral; split back out into OQ2 (G13/G32) and OQ3 (G34) below.)
> Reading A (P7 optimism): scenarios run "thousands per hour without rate limits" → no agent-side ceiling.
> Reading B (the gap): P7's rate-limit relief is on the *twinned-dependency* side; the **coder/judge agent still hits Max rate limits** (G34), and L5-volume scenario/judge/A-B replay against one $200 Max seat has **no token-budget math anywhere** (G13/G32).
> **Chosen:** Reading B is correct on the facts; v4 simply has not modeled it. Faithful position: C28 inherits a **single-seat throughput/cost ceiling** that v4 leaves unquantified. The minimal consistent mitigation already present in v4 is C29 (model-floor/stylesheet **cost/family-aware routing**) — i.e. v4's own answer to "don't burn the floor model on everything" — plus C04 session suspension to avoid idle burn. No new mechanism may be invented in Track A; the quantification is **deferred** (token budgets, seat-count, rate-limit backoff) to review-log.

**Other detection/recovery:** auth failure, MCP-connection failure, and permission-change events are all in Claude Code's native event stream (AI-CONTEXT §4.3 L173) → visible to C11 self-healing.

## 7. Cross-cutting

- **Security:** OAuth-only, no key egress (I1); hooks (PreToolUse) are the deterministic permission gate before any tool runs; partition `code` (no `scenarios` read) preserves held-out integrity (I4).
- **Cost:** unmodeled in v4 (G32) — single $200/mo Max seat is the only figure; routing economy delegated to C29. *Open.*
- **Scale:** single-seat ceiling (G34) — horizontal scale via multiple C04 sessions/seats is **not** specified by v4; do not invent. *Open.*
- **Observability:** first-class — native OTLP (metrics/events/traces) + raw-API-bodies; correlation via `session.id`/`prompt.id`. This is C28's strongest property and the input to the entire C24–C27 observability tier.
- **Ops:** declarative config (C03) + `.claude/` + packs (C02); no Go fork (AI-CONTEXT §3.5 L128).

## 8. Acceptance criteria & test strategy (sweep-1, high level)

- **AC1:** A bead dispatched to the `claude` agent starts a Claude Code subprocess in its C04 session, runs a multi-turn loop, dispatches at least one tool, and emits a work product attributed by `session.id`. (README L537, Phase-0 checklist: "Verify Claude Code runs in the Gas City tmux runtime with attribution flowing into beads. This is your first checkpoint.")
- **AC2:** With the §13.2 env block set, native OTLP events + a raw-API-bodies file appear for the run and are consumable by C25/C26 (README L539, Phase-0 checklist: "Set up an OpenTelemetry Collector receiving Claude Code's OTLP output. Verify events flow.").
- **AC3:** A registered PreToolUse hook can deny a tool call and a PostToolUse hook observes a result (override-detection surface for C35).
- **AC4:** A Skill and an MCP server declared via config/`.claude/` are usable by the loop without any Go fork.
- **AC5:** C28 in the `implementer` rig has no read access to the `scenarios` partition.
- **AC6 (auth):** C28 authenticates via Max OAuth only; no API key is present and no token leaves Claude Code.

## 9. Open questions (→ review-log)

- **OQ1 (G12, top):** The Max→API-key fallback is named but undesigned and contradicts the no-API-key auth model. What is the concrete provider-swap path if Max policy shifts, and does it land before or after the June-15-2026 Agent SDK Max path? *Blocks the floor's durability claim.*
- **OQ2 (G13/G32):** No token-budget/cost model exists for L5-volume implementer runs on one Max seat. Needs quantification before throughput claims hold.
- **OQ3 (G34):** Agent-side rate-limit ceiling under a single Max subscription is unaddressed; is multi-seat / multi-session horizontal scale in scope, and who owns it (C04 vs C28 vs C29)?
- **OQ4:** Registration schemas for Skills/Subagents/Hooks/MCP are inferred as declarative ([FAITHFUL-FILL]); v4 should confirm the pack-level contract (overlaps C02).
