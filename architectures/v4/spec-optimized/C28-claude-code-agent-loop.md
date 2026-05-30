# C28 — Claude Code Agent Loop  (Spec, Track B)

> Source: README §"Principle 2 — Three-layer architecture" (113–124: "Agent loop | Multi-turn reasoning + tool dispatch | Claude Code CLI | Anthropic ToS — Max subscription allows | Gas City `claude` provider preset"; LLM-client row 119; pipeline/persistence rows 121–122), README mermaid LC node (68 "LLM client / model provider abstraction"), README P0/P2 phasing (355 "one Claude Code session, no custom code"; 368 "Claude Code as agent + LLM client"; 537–539 first-checkpoint), README override-hook rows (212, 218, 457), README license rows (289 "Max subscription allows subprocess automation", 336); AI-CONTEXT §2 layer table (32, 49–50 "Agent loop — multi-turn reasoning + tool dispatch (Claude Code, OpenHands, Overstory, Codex)"), §4 "Claude Code under Max" (139–190: §4.1 auth/OAuth, §4.2 Agent SDK June-15 credit, §4.3 telemetry surface, §4.4 skills/subagents/hooks/MCP), §14 risk register (624 "Claude Code Max policy changes | Low | High | … have API-key fallback path ready"), §13 env-vars (569), §3.6 extractability; F-MODE-COVERAGE F12/F44/F56 (lethal trifecta rows 54–57), F19 (model-floor dependency, 71), F31 (substrate floor = weakest adapter, 73/148), F21 (context-window exhaustion caution, 116), F55 (behavioural drift, 78/156); component-inventory C28 row (subsystem Agent Loop, agent-role, foundational, maps A04/A04b/A05/A28d–h/B20/B21, depends C04, gaps G12/G13/G34); _meta gaps G12 (Max-policy/API-key-fallback undesigned), G13 (token-budget math absent), G34 (single-Max-seat throughput ceiling), G31 (lethal-trifecta isolation gap — owned by C43, but the *agent-side* exposure surface lives here).
> Inventory ID: C28   Kind: agent-role   Status: sweep-1
> Deltas: DELTA-01 (C28 is a **provider-abstracted agent-loop role with a stable internal contract**, not "Claude Code CLI" hardcoded — Claude Code is the *default capability-floor adapter* behind an `AgentLoopProvider` seam so the API-key/Agent-SDK fallback G12 names is a swappable adapter, not a rewrite), DELTA-02 (**explicit token/quota governor + admission control** in front of every turn — makes the G13/G34 single-seat budget a measured, enforced resource instead of an unstated assumption; emits back-pressure to C05 dispatch), DELTA-03 (**multi-seat / seat-pool abstraction**: the role addresses a *pool* of N Max seats + optional Agent-SDK-credit + metered-API seats behind one scheduler, lifting the single-seat throughput ceiling G34 names without changing the per-worker contract), DELTA-04 (**capability/egress profile is a declared, enforced input to the loop** — the agent never gets ambient Bash+network+fs; C28 binds a C43 capability profile per invocation, shrinking the G31 blast-radius window that exists *before* twins ship), DELTA-05 (**deterministic context-budget management** — turn-count/token ceilings, compaction policy, and a "stuck-loop" detector are owned, observable resources, turning F21 from "methodology-level, undetected" into a runtime-enforced limit), DELTA-06 (**provider-floor conformance suite**: any adapter claiming to satisfy the role must pass a capability-floor test battery — operationalizes the F19/F31 "floor by declaration" so a fallback adapter can't silently drop below it), DELTA-07 (**hooks/skills/subagents/MCP surface is a typed, version-pinned configuration owned by C28**, not ad-hoc `.claude/` files — every PreToolUse/PostToolUse/Stop gate, skill, and MCP server is declared in the pack and reconciled, so override-discipline C35 and isolation C43 have a single enforcement seam).

## 1. Purpose & responsibility

C28 is the **agent-loop role**: the multi-turn reason→act→observe loop that takes a unit of work (a spec/formula step, a bead, a repair task) and drives it to a result by interleaving model reasoning with tool calls until a stop condition is met. It is **the implementer worker** of the factory — the probabilistic half of the three-layer architecture (README 113–122), counterpart to the deterministic tool-node path (C17). In v4 this role is filled by **Claude Code CLI under Max, invoked as a subprocess through Gas City's `claude` provider preset** (README 120). C28 owns, as a role:

1. **The agent-loop contract (DELTA-01).** A stable internal interface — `AgentLoopProvider` — describing what *any* agent-loop adapter must do: accept a task + context + capability profile + tool surface, run the multi-turn loop, stream telemetry, and return a structured outcome. Claude Code is the **default, capability-floor adapter** behind this seam; the API-key/Agent-SDK fallback that G12 names becomes a *second adapter passing the same conformance suite*, not a contradiction.
2. **The turn loop + stop conditions (DELTA-05).** The reason→tool-dispatch→observe cycle, plus the runtime-owned ceilings that bound it: max turns, token budget, wall-clock, and a stuck-loop/no-progress detector. v4 treats the loop as Claude Code-internal and opaque; C28 wraps it with *observable, enforced* limits so context-window exhaustion (F21) and runaway loops are detected and stopped, not just hoped-against.
3. **The tool / hook / skill / subagent / MCP surface (DELTA-07).** The declared, version-pinned configuration of what tools the loop can call, which deterministic gates fire around them (PreToolUse/PostToolUse/SessionStart/Stop hooks — AI-CONTEXT §4.4), which skills and subagents are available, and which MCP servers are mounted. This is the seam where **override-discipline (C35)** and **isolation (C43)** attach.
4. **The capability/egress binding (DELTA-04).** Per invocation, C28 binds a C43 capability profile (which Bash commands, which network egress, which filesystem partitions) so the agent never runs with ambient lethal-trifecta access.
5. **The seat/quota governor (DELTA-02/03).** Admission control over a pool of Max/Agent-SDK/API seats, with measured token accounting and back-pressure — the operational answer to G13/G34.

The load-bearing reason C28 is **foundational**: it is *the thing that writes the software*. Every build, repair, diagnosis, and self-optimization action that requires reasoning routes through this role. Its contract is what C29 (model floor/routing) selects an adapter/model *for*, what C25 telemetry instruments, what C05 dispatches *to*, and what C43 must bound. If the role's contract is unstable or its resource envelope is unmeasured, the factory's entire "specs-in → software-out" thesis has no governable engine.

What C28 is **NOT**:
- **Not the model-selection / routing policy.** **C29** declares the capability floor and the CSS-like cost/family-aware routing rules ("use Haiku-class for X, floor-class for Y"). C28 *consumes* a model/adapter selection from C29 per invocation; it does not own the routing rules. (C28 owns the *role contract*; C29 owns *which model/adapter fills it when*.)
- **Not the LLM client / provider transport.** The raw provider abstraction (OAuth handshake, HTTP transport, LiteLLM when off-Max — README 119) is the LLM-client layer. C28 is the *loop* on top; it depends on the client but does not reimplement it. (In Claude Code, client+loop ship as one binary; C28's `AgentLoopProvider` seam is where they are conceptually split so a non-Claude-Code client can be swapped under the same loop contract.)
- **Not the session/provider runtime.** **C04** (session/provider) owns process lifecycle, the tmux runtime, session-id, resume, and attribution plumbing. C28 runs *inside* a C04 session; C04 is its upstream substrate.
- **Not the deterministic tool-node path.** **C17/C02** own model-free tool nodes. C28 is the probabilistic worker that *calls* tools; the deterministic half is explicitly elsewhere (README 154/Principle 4).
- **Not telemetry export.** **C25** owns OTLP/raw-API-body export; **C24** owns the CXDB bridge. C28 *emits* the events/spans (via env-var config) and guarantees they carry correlation keys; it does not own the export pipeline.
- **Not the isolation mechanism itself.** **C43** owns boundary typing and twin isolation; **C44** owns twins. C28 owns only the *binding point* — it declares and enforces the capability profile C43 defines, and is the surface where the G31 exposure is measured and bounded.
- **Not the judge.** **C32** scores trajectories and must be a *different model family* (F48/G08). C28 is the coder; a judge invocation is a *separate* C28-role instance with a C29-selected non-coder family — the role contract is shared, the configured family is not.
- **Not the override-discipline loop.** **C35** detects/logs/converts operator overrides into rules; C28 only *hosts the hooks* (PreToolUse/PostToolUse) C35's detection rides on.

## 2. Context & dependencies

- **Depends on:**
  - **C04 (session/provider)** — owns the runtime (Gas City tmux), process spawn/resume, `session.id`, and attribution. C28's loop executes inside a C04 session; the OAuth/Max credential pickup (AI-CONTEXT §4.1–4.2) is a C04 concern C28 relies on.
  - **C29 (model floor & routing)** — supplies, per invocation, the model/adapter selection and the floor guarantee. C28 is `depends C04` in the inventory; the C29 coupling is *inbound selection*, and C29 in turn `depends C28` for the role contract it selects against (the two co-design the `AgentLoopProvider` interface; see §3).
  - **C03 (config/feature-flags)** — enables/disables adapters, sets seat-pool size, quota ceilings, hook/skill/MCP enablement, and the Max-vs-fallback feature flag (G12).
  - **C43 (isolation boundary)** — defines the capability/egress profiles C28 binds (DELTA-04). C28 is the *enforcement attach point* on the agent side.
  - **C02 (pack ABI)** — the hooks/skills/MCP/subagent surface (DELTA-07) is declared in a pack via C02; MCP servers and tool nodes the loop calls are pack-registered.
  - **C41 (identity/attribution)** — every turn/tool call/PR/commit the loop emits carries attribution; C28 stamps the worker identity onto its outputs.
- **Consumed by / drives:**
  - **C05 (sling/dispatch)** dispatches work units *to* C28 instances and receives back-pressure/admission signals from the C28 governor (DELTA-02).
  - **C25 (OTLP export) / C24 (CXDB bridge)** consume the telemetry C28 emits; C28 guarantees correlation keys (`prompt.id`, `session.id`, `user.account_uuid`, `organization.id`) per AI-CONTEXT §4.3 land on every signal.
  - **C32 (judge harness)** is a sibling instantiation of the same role with a different configured family.
  - **C35 (override loop)** rides the PreToolUse/PostToolUse hooks C28 hosts.
  - **C57 (failure-mode coverage)** depends on C28's measured resource/exposure surface to honestly rate F12/F19/F21/F31/F44/F55/F56.
- **Sits at:** the **Agent Loop** subsystem (inventory §"Agent Loop — C28, C29"), in Batch 2 of the build order (depends Batch-1 substrate; parallel with C04/C05/C29/C25/C26/C27/C24). It is the single role every reasoning action in the factory is performed *by*.

## 3. Interfaces / contracts

Named-and-described (sweep 1; concrete signatures, the outcome/error JSON schema, the env-var/hook manifest schema, and a Mermaid turn-loop sequence land in sweep 2). The defining move (DELTA-01) is that C28 specifies a **provider-abstracted role contract**, with Claude Code as the default floor adapter, rather than hardcoding the CLI.

### 3a. `AgentLoopProvider` — the role contract (DELTA-01)

The stable interface every agent-loop adapter must satisfy. Inbound, per invocation:
- **`task`** — the work unit: spec/formula-step reference, bead id, or repair directive, plus the desired-state/acceptance hint.
- **`context`** — working-directory/repo handle, prior-turn resume handle (`session.id`), and any seeded conversation/memory.
- **`model_selection`** — the C29-supplied adapter + model family + cost class (the floor guarantee travels with this).
- **`capability_profile`** — the C43 egress/Bash/fs/network profile to enforce (DELTA-04).
- **`tool_surface`** — the resolved set of tool nodes (C17), MCP servers, skills, subagents, and the hook chain (DELTA-07).
- **`budget`** — max turns, token ceiling, wall-clock, granted by the governor (DELTA-02/05).

Outbound:
- **`AgentOutcome`** — `{ status (succeeded | budget-exhausted | stuck | tool-denied | provider-error | policy-halt), artifacts (diffs/PRs/files produced), turn_count, tokens_in/out, cost, session_id, stop_reason, attribution }`.
- **Telemetry stream** — OTLP metrics/events/(beta)traces + raw-API-body dump, with correlation keys (C25/C24 consume).
- **Invariant (floor conformance, DELTA-06):** any adapter must pass the capability-floor conformance suite (multi-turn tool use, sub-agent fan-out, structured-edit fidelity, hook honoring) before C03 may select it. A fallback adapter that fails the suite is *rejected*, not silently downgraded (closes the F19/F31 "floor by declaration" loophole and the G12 "named-but-undesigned fallback").

### 3b. Turn loop + stop conditions (DELTA-05)

The reason→dispatch→observe cycle, with **runtime-owned, observable ceilings**: `max_turns`, `token_budget`, `wall_clock`, and a **no-progress detector** (repeated identical tool calls / no artifact delta over K turns → `stuck`). On any ceiling breach the loop halts with the corresponding `AgentOutcome.status` and emits a telemetry event. **Compaction policy** (when/how to summarize context) is a declared input, not a hidden adapter default — so F21 exhaustion is bounded and attributable.

### 3c. Tool / hook / skill / subagent / MCP surface (DELTA-07)

A **typed, version-pinned manifest** (declared in a C02 pack, reconciled — not loose `.claude/` files):
- **Hooks** — `PreToolUse` (capability check + C35 override-detect), `PostToolUse` (result audit + override-detect), `SessionStart`, `Stop`. PreToolUse is the deterministic gate enforcing the `capability_profile`.
- **Skills** (`.claude/skills/`-shaped), **subagents** (Explore/Plan/general/custom — for parallel fan-out), **MCP servers** (the tool layer).
- **Invariant:** the active surface is fully derivable from the manifest + config; no ambient tools. This makes the agent's actual authority auditable by C43/C57.

### 3d. Seat/quota governor (DELTA-02/03)

Admission-control interface to C05: `acquire(estimated_tokens, model_family) → grant | back-pressure(retry-after)`. Accounts measured tokens against a **seat pool** (N Max seats + Agent-SDK credit + metered-API seats). Exposes utilization for C29 routing and C25 metrics. This is the enforced form of the G13/G34 budget.

## 4. Data model / state

- **Owned (ephemeral, per invocation):** the live turn loop state — turn counter, token tally, conversation/context buffer (subject to compaction), `session.id`, no-progress window. Lifecycle = bound to one C04 session; C04 owns persistence/resume of the session itself.
- **Owned (durable, role-level):** the **seat-pool ledger** (seats, live leases, rolling token/cost accounting, rate-limit state per seat) and the **adapter registry** (which adapters are conformance-passed + enabled). DELTA-02/03/06.
- **Configuration (owned, declared):** the tool/hook/skill/MCP manifest (DELTA-07), the budget defaults and compaction policy (DELTA-05), the capability-profile bindings (DELTA-04, defined by C43, selected here).
- **Not owned:** trajectory storage (CXDB via C24), telemetry storage (C25/C26/C27), bead/work-ledger state (C19/C20), session credentials (C04), routing rules (C29). C28 *emits* into these; it does not store them.
- **Consistency:** seat-pool accounting must be strongly-consistent enough to never over-grant a hard Max cap (admission is the enforcement point); telemetry emission is best-effort/at-least-once (C24 owns ordering/back-pressure at its seam).

## 5. Behavior

Sweep-1 prose; Mermaid sequence + state diagram land in sweep 2.

**Primary flow (one work unit):**
1. C05 dispatches a task; C28 governor `acquire()`s a seat grant (or returns back-pressure to C05).
2. C29 supplies `model_selection`; C28 resolves `capability_profile` (C43) and `tool_surface` (pack manifest).
3. C04 session starts/resumes; the floor adapter (Claude Code) is invoked as a subprocess with the env-var telemetry + capability config.
4. Loop: model reasons → proposes tool call → **PreToolUse hook** checks capability profile (deny → `tool-denied` outcome or skip) and runs C35 override-detect → tool dispatched (C17 node / MCP / Bash within egress profile) → **PostToolUse hook** audits result → observation fed back. Repeat until success, or a ceiling/stuck condition halts the loop (DELTA-05).
5. On stop: emit `AgentOutcome` + final telemetry; release the seat; stamp attribution (C41); artifacts (diffs/PRs) surface to the dispatcher.

**Degraded flows:**
- *Quota/rate-limit hit:* governor refuses admission → C05 queues/throttles; if a hard Max cap is reached mid-run, the loop is allowed to drain its current turn, then halts `budget-exhausted` (no silent retry against a capped seat).
- *Max policy revocation (G12):* feature-flag (C03) flips the default adapter to the API-key/Agent-SDK fallback adapter; the fallback must already be conformance-passed (DELTA-06), so the switch is config, not a build.
- *Provider error / context exhaustion (F21):* compaction triggers at the configured threshold; if still exhausted, halt `budget-exhausted` with a resumable `session.id`.

## 6. Failure modes & handling

| F-mode | Relevance to C28 | C28 handling (Track-B) |
|---|---|---|
| **F19** Model-floor dependency | C28 *is* the floor's runtime surface | DELTA-06 conformance suite: floor is *tested*, not just declared; sub-floor adapters rejected |
| **F31** Substrate floor = weakest adapter | Multiple adapters (G12 fallback) could lower the floor | Same conformance gate applies to *every* adapter before C03 enables it |
| **F21** Context-window exhaustion | The loop is where it happens | DELTA-05: owned token/turn ceilings + compaction policy + stuck-detector → detected & bounded, not "methodology-level/undetected" |
| **F12 / F44 / F56** Lethal trifecta / scissors-default / guardrail-bypass-under-stress | C28 is the agent that *has* Bash+network+fs | DELTA-04: no ambient access — per-invocation C43 capability profile enforced at PreToolUse; default-deny egress. Bounds the **G31** pre-twin exposure window. (Twins C44/boundary C43 remain the full fix; C28 owns the agent-side enforcement seam.) |
| **F55** Behavioural drift / self-reference | Coder + judge sharing the role | Judge is a *separate family* instance (C29-selected); external grounding owned by C30/C32 |
| **F48** Tacit collusion (shared context) | Coder/judge as sibling C28 roles | Enforced family separation at config; same-context reuse forbidden between coder and judge instances |

**G31 note (deferred-with-mitigation):** the full lethal-trifecta fix (twins + deterministic boundary typing) is owned by C43/C44/C57 and ships late (the G31 blocker). C28 cannot close G31, but DELTA-04 **shrinks the exposed surface from day one** by making the agent's Bash/network/fs authority an explicit, default-deny, PreToolUse-enforced profile rather than ambient access — so the "no isolation through Phase 3b" window is bounded by capability profile even before twins exist. This is the single most important Track-B improvement on the agent side.

## 7. Cross-cutting (security / cost / scale / observability / ops)

- **Security:** capability profile + default-deny egress + PreToolUse enforcement (DELTA-04); typed/version-pinned tool surface (DELTA-07) makes the agent's real authority auditable (C43/C57). OAuth tokens never leave Claude Code (AI-CONTEXT §4.1) — the fallback adapter uses a *separate* credential path, never the OAuth token.
- **Cost (G13):** the governor turns "thousands of scenarios/hour under $200/mo" from an unstated assumption into **measured, admission-controlled token accounting** with per-task cost in `AgentOutcome`. Token-budget math becomes observable; C29 routing can shift cheap work off the floor.
- **Scale (G34):** DELTA-03 seat-pool lifts the single-seat ceiling — N Max seats + Agent-SDK credit + metered-API seats behind one scheduler. The throughput ceiling is now a *provisioned, monitored* quantity, not a hidden bound. Back-pressure to C05 prevents thrashing a capped seat.
- **Observability:** native OTLP (metrics/events/beta-traces) + raw-API-body dump (AI-CONTEXT §4.3) with correlation keys on every signal; governor utilization + stop-reason histograms as first-class metrics.
- **Ops:** Max-vs-fallback is a C03 feature flag (G12); seat-pool size and budgets are config; the conformance suite is a CI gate for any new adapter.

## 8. Acceptance criteria & test strategy

Sweep-1 (high-level; concrete cases in sweep 2):
1. **Role contract holds across adapters.** Claude Code adapter and at least one fallback adapter (API-key/Agent-SDK) both implement `AgentLoopProvider` and pass the floor conformance suite (DELTA-01/06). Swapping adapters is config-only (G12).
2. **Budgets are enforced and observable.** A task exceeding `max_turns`/`token_budget`/`wall_clock` halts with the correct `status` and emits the corresponding telemetry; a no-progress loop is detected as `stuck` (DELTA-05, F21).
3. **No ambient authority.** A tool call outside the bound `capability_profile` is denied at PreToolUse and surfaces `tool-denied`; default egress is deny (DELTA-04, F12/F44/F56). Auditable from the manifest alone.
4. **Quota governance works.** Under a saturated seat pool, admission returns back-pressure to C05 rather than over-granting a capped Max seat; per-task cost/tokens appear in `AgentOutcome` and metrics (G13/G34).
5. **Telemetry correlation.** Every emitted signal carries `prompt.id`/`session.id`/`account_uuid`/`organization.id` so C24/C25 can reconstruct the trajectory.
6. **Coder/judge separation.** A judge-role instance refuses to run with the same model family or shared context as the coder instance that produced the work (F48/F55 hook, full enforcement in C32).

## 9. Open questions

- **OQ-1 (→ review-log, G12/G34):** Is the **multi-seat pool (DELTA-03) compatible with Anthropic Max ToS?** Pooling N seats behind one scheduler for unattended automation may violate per-seat terms even though subprocess automation of a single seat is permitted (AI-CONTEXT §4.1). If pooling is disallowed, the throughput ceiling G34 names is *structural*, not provisionable — and the cost/scale story must fall back to metered-API seats (re-opening G13). **This is the top open question** and gates the entire P7 "thousands/hour" rationale.
- **OQ-2 (G12):** Does the API-key/Agent-SDK fallback adapter actually clear the floor conformance suite (DELTA-06), or are there loop behaviors (sub-agent fan-out, hook semantics, structured-edit fidelity) only Claude Code provides? If it can't pass, the "fallback ready" mitigation in AI-CONTEXT §14 is hollow.
- **OQ-3 (DELTA-04 vs G31):** How much of the capability profile can PreToolUse hooks *actually* enforce against a Bash-capable agent before twins exist? A shell can exfiltrate within a single allowed command; the profile bounds but does not eliminate the trifecta. Need C43 to confirm the deterministic-boundary-typing primitives C28 binds against.
