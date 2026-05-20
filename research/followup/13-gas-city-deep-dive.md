# Gas City — Deep Architecture and Capabilities Reference

**Audience:** future AI sessions, contributors, and engineers who need to understand Gas City well enough to use it, extend it, or treat it as the runtime substrate for another software-factory discipline (StrongDM Dark Factory, Every.to Compound Engineering, BMAD, the parent project's four candidate architectures, etc.).

**Provenance:** Authored 2026-05-20 by a Claude Code subagent against a fresh clone of `https://github.com/gastownhall/gascity` (read-only walk; ~49 MB, ~2,300 files, post-v1.0.0, commit `183897e`). Every architectural claim cites a specific file path inside the cloned tree so future sessions can verify and extend the analysis. The official docs site (`https://docs.gascityhall.com`) is the Mintlify projection of the in-repo `docs/` tree; this analysis works from the in-repo sources directly because the public site returned HTTP 403 from the sandbox.

**Companion documents:**

- `research/followup/14-gas-town-deep-dive.md` — sibling deep-dive on Gas Town, the system Gas City was extracted from.
- `research/38-gas-systems-substrate.md` — synthesis report: how Gas City + Gas Town map to StrongDM Dark Factory and Every.to Compound Engineering, with concrete deployment sketches.
- `research/followup/04-gastown-beads.md` — earlier (Round-3) comparison of Gas Town + Beads against Attractor; this analysis supersedes it on Gas Town/Gas City primitives but remains consistent on the Attractor-comparison axis.

---

## 0. Orientation

This document is a structural, technical reference for the Gas City repository at `github.com/gastownhall/gascity` (analyzed at commit `183897e`, post-`v1.0.0`). It is written for a future AI session that needs to understand Gas City well enough to use it, extend it, or compose other software-factory disciplines on top of it. The reader is assumed to already know what an LLM coding agent is, what Claude Code is, what tmux is, what `bd` (Steve Yegge's persistent-task-graph DB on Dolt) is, and what a DOT pipeline is in the Attractor sense. Those primitives are not re-explained here; what is described is what *Gas City specifically does* with them.

---

## 1. Mission and Positioning

### What Gas City Is

Gas City is "an orchestration-builder SDK for multi-agent systems" (`README.md:14-17`). The product slogan from `docs/index.mdx:6-10` is similar:

> Gas City is an orchestration-builder SDK for multi-agent systems. This docs tree is organized for external contributors first: install the toolchain, run a local city, find the relevant subsystem, and then decide whether you need current-state architecture docs, forward-looking design docs, or archived working notes.

It is a Go-based toolkit whose single binary, `gc`, hosts (a) a CLI front-end, (b) a per-city reconciler called the controller, (c) a machine-wide supervisor process that hosts one controller per registered city, and (d) a typed HTTP+SSE control plane.

### Relation to Gas Town and Compound Engineering Lineage

Gas City is explicitly the **reusable substrate extracted from Gas Town** (Steve Yegge's multi-agent orchestration system). The framing in `AGENTS.md:1-18` is unambiguous:

> Gas City is an orchestration-builder SDK — a Go toolkit for composing multi-agent coding workflows. It extracts the battle-tested subsystems from Steve Yegge's Gas Town (github.com/steveyegge/gastown) into a configurable SDK where **all role behavior is user-supplied configuration** and the SDK provides only infrastructure. The core principle: **ZERO hardcoded roles.** The SDK has no built-in Mayor, Deacon, Polecat, or any other role. If a line of Go references a specific role name, it's a bug.
>
> You can build Gas Town in Gas City, or Ralph, or Claude Code Agent Teams, or any other orchestration pack — via specific configurations.
>
> **Why Gas City exists:** Gas Town proved multi-agent orchestration works, but all its roles are hardwired in Go code. Steve realized the MEOW stack (Molecular Expression of Work) was powerful enough to abstract roles into configuration. Gas City extracts that insight into an SDK where Gas Town becomes one configuration among many.

This is the central architectural commitment: **Gas City is the primitive substrate; Gas Town (with its mayor/deacon/polecat/refinery/witness role taxonomy) is one example pack you can run on top of it.** The Gastown role names ship inside `examples/gastown/packs/gastown/`, not inside `internal/` Go code.

### What Was Kept, Generalized, and Dropped

`docs/getting-started/coming-from-gastown.md:30-44` summarizes the abstraction shift:

| In Gas Town... | In Gas City... |
|---|---|
| mayor, deacon, witness, refinery, polecat, crew, dog roles | Configured agents — names come from pack TOML, not Go |
| `~/gt/...` directory layout | `dir`/`work_dir` config fields; directories aren't architecture |
| Plugins and convoys as named orchestration features | `pack.toml` plus orders, formulas, mail, sling |
| Role-specific managers and cwd-derived identity | Explicit agent identity + rig scope + bead metadata |
| Deacon watchdog logic | Controller + supervisor + health patrol |
| Plugin (event-triggered helper) | Order (exec or formula) |
| Convoy as runtime layer | Convoy bead + sling/formulas; no special convoy subsystem |

Concretely: the durable work model (beads), the molecule formalism, the convoy abstraction, and the dispatch idiom (sling) are kept. What is dropped from the SDK is the role taxonomy. What is generalized is config — Gas City replaces Town's filesystem-as-contract with a declarative TOML/pack composition model.

### Position in the Wider Ecosystem

The wider design framing in `AGENTS.md:36-73` introduces "**five primitives + four derived mechanisms**" — what the docs call the **Nine Concepts** (`engdocs/architecture/nine-concepts.md`). This decomposition is the most important entry point for any consumer of Gas City. It is described in §2 below.

Gas City positions itself between:

- **Bare LLM coding agents** (Claude Code, Codex, Cursor, Gemini, Copilot, Amp, OpenCode, Auggie, Kiro) — Gas City treats each of these as a **provider** behind a uniform interface.
- **Persistent work graphs** (Yegge's `bd` / Beads) — Gas City uses `bd` (or `file`/`exec`-backed alternatives) as its universal persistence substrate.
- **Application-layer orchestration patterns** (Gastown, Ralph, Claude Code Agent Teams, Attractor DOT pipelines) — these are *packs*, not SDK features.

---

## 2. Top-Level Architecture — The Nine Concepts

`engdocs/architecture/nine-concepts.md` is the canonical mental map. It is worth absorbing in full before reading anything else. The structure:

```
Layer 0-1 (Primitives, irreducible):
  1. Session       — internal/session + internal/runtime + internal/agent
  2. Bead Store    — internal/beads
  3. Event Bus     — internal/events
  4. Config        — internal/config
  5. Prompt Templates — cmd/gc/prompt.go + agents/<name>/prompt.template.md

Layer 2-4 (Derived mechanisms, provably composable):
  6. Messaging     — internal/mail + runtime.Provider.Nudge
  7. Formulas & Molecules — internal/formula + internal/molecule + .formula.toml
  8. Dispatch (Sling) — internal/sling + cmd/gc/cmd_sling.go
  9. Health Patrol — controller loop in cmd/gc/controller.go + cmd/gc/session_reconciler.go
```

Two architectural rules are stated as load-bearing invariants in `engdocs/architecture/nine-concepts.md:170-180`:

1. No upward dependencies (Layer N never imports Layer N+1).
2. Beads is the universal persistence substrate for domain state.
3. Event Bus is the universal observation substrate.
4. Config is the universal activation mechanism.
5. Side effects (I/O, process spawning) are confined to Layer 0.
6. The controller drives all SDK infrastructure operations. No SDK mechanism may require a specific user-configured agent role.

The "primitive test" in `engdocs/contributors/primitive-test.md` (referenced in nine-concepts.md:18-25) gates additions: a primitive must be Atomic (not decomposable), Bitter-Lesson-positive (gets *more* useful as models improve), and ZFC-clean (Go handles transport only, no judgment calls).

### Subsystem-to-Package Map

Below is the mapping from named subsystem to its primary internal package(s) and CLI surface. Packages without their own subsystem are utility helpers and are listed in §17.

| Subsystem | Internal package(s) | Primary CLI |
|---|---|---|
| Session runtime | `internal/runtime/` (+ `tmux/`, `subprocess/`, `exec/`, `k8s/`, `acp/`, `auto/`, `hybrid/`, `fake.go`) | `gc session`, `gc runtime` |
| Session bookkeeping | `internal/session/` (lifecycle projection, waits, blocked-turns) | `gc session wait`, `gc wait` |
| Agent helpers | `internal/agent/` (session naming, startup hints) | — |
| Bead store | `internal/beads/` (`bdstore.go`, `memstore.go`, `filestore.go`, `exec/`) | `gc bd`, `gc beads`, `gc graph` |
| Event bus | `internal/events/` (`recorder.go`, `fake.go`, `exec/`) | `gc events`, `gc event emit` |
| Config | `internal/config/` (loader, packs, patches, providers, revision hash) | `gc config`, `gc reload` |
| Pack import system | `internal/packman`, `internal/remotesource`, `internal/builtinpacks`, `internal/bootstrap` | `gc pack`, `gc import` |
| City init/scaffolding | `internal/cityinit`, `internal/citylayout`, `internal/bootstrap` | `gc init` |
| Mail | `internal/mail/` (+ `beadmail/`, `exec/`) | `gc mail` |
| Formulas | `internal/formula/` (compile, advice, graph, ralph, control flow) | `gc formula` |
| Molecules | `internal/molecule/` (artifact scoping) | `gc formula cook --attach` |
| Dispatch / Sling | `internal/sling/` | `gc sling` |
| Orders | `internal/orders/` (parsing, triggers, scanner) | `gc order` |
| Convergence loops | `internal/convergence/` (handler, gate, reconciler, retry) | `gc converge` |
| Convoys | `internal/convoy/` | `gc convoy` |
| Controller / supervisor / reconciler | `cmd/gc/controller.go`, `session_reconciler.go`, `crash_tracker.go`, `idle_tracker.go`, `wisp_gc.go`, `order_dispatch.go`, `cmd_supervisor.go`, `city_runtime.go`; `internal/supervisor/` | `gc start`, `gc supervisor`, `gc stop`, `gc restart` |
| Worker boundary | `internal/worker/` (canonical session-creation boundary) | — (internal) |
| Dispatch (DAG fanout) | `internal/dispatch/` (graph.v2 workflow execution) | `gc convoy control` |
| Telemetry | `internal/telemetry/` (OTel recorder, invocation metrics) | — |
| Logging | `internal/logutil`, `internal/sessionlog` (reads Claude JSONL) | — |
| Reliability analytics | `internal/reliability` | `gc analyze reliability` |
| Trust / auth | `internal/doltauth`, `internal/pgauth`, `internal/execenv` (secret-stripping) | — |
| External messaging | `internal/extmsg` (Phase-1 external chat fabric) | (API + adapters) |
| HTTP API | `internal/api/` (Huma-registered, generated OpenAPI) | served by `gc supervisor run` |
| Workspace services | `internal/workspacesvc` (proxy_process / proxy_socket / managed_socket) | declared in city.toml `[[service]]` |
| Doctor | `internal/doctor` | `gc doctor [--fix]` |
| Build-image | `internal/buildimage` | `gc build-image` |
| Path/work helpers | `internal/workdir`, `internal/pathutil`, `internal/searchpath`, `internal/fsys`, `internal/shellquote` | — |
| Test scaffolding | `internal/testenv`, `internal/testfixtures`, `internal/testutil`, `internal/formulatest` | — |
| Migration | `internal/migrate`, `internal/configedit` | `gc doctor --fix` |
| Pricing | `internal/pricing` | (consumed by telemetry) |
| Hooks (provider integration) | `internal/hooks` (Claude/Gemini/OpenCode/Copilot config) | `gc hook`, `gc prime` |
| Overlay | `internal/overlay` (merge-aware copy of hook/settings) | (auto on session start) |
| Process control | `internal/processgroup`, `internal/pidutil`, `internal/clock` | — |
| Review quorum | `internal/reviewquorum` (durable finalizer contract) | (consumed by `mol-review-quorum`) |
| Convoy graph routing | `internal/graphroute` (graph.v2 decorations) | (consumed by sling/dispatch) |
| Skill/MCP materialization | `internal/materialize`, `internal/promptmeta` | `gc skill`, `gc mcp` |
| Source workflow enforcement | `internal/sourceworkflow` | (CI guard) |
| Document generation | `internal/docgen` | (build-time only) |

Many of those "utility" packages (`clock`, `fsys`, `pathutil`, `shellquote`, `pidutil`, `searchpath`) exist purely for testability — they wrap stdlib facilities in interfaces that can be faked.

---

## 3. CLI Surface

The `gc` CLI is a Cobra-based command tree, fully auto-generated reference in `docs/reference/cli.md`. There are roughly **45 top-level subcommands** (plus many nested ones). Below they are grouped by intent.

### City Lifecycle

| Command | Purpose |
|---|---|
| `gc init [path]` | Scaffold a new city directory. Wizard picks template (minimal/gastown/custom) and provider. Writes `pack.toml`, `city.toml`, `.gc/`, agent dirs. |
| `gc start` | Start the city under the machine-wide supervisor. Hidden `--foreground` runs the legacy standalone controller. |
| `gc stop` | Stop all sessions in the city. Sends `Interrupt` then `Stop` after `shutdown_timeout`. |
| `gc restart` | Restart all agent sessions. |
| `gc reload [path]` | Live-reload `city.toml` without restarting the controller (structured failure mode). |
| `gc suspend` / `gc resume` | Set/clear `workspace.suspended` so the reconciler ignores all agents. |
| `gc status` | City-wide overview. |
| `gc cities list` | List cities registered with the supervisor. |
| `gc register` / `gc unregister` | Register/unregister a city with the supervisor. |

### Supervisor (machine-wide)

| Command | Purpose |
|---|---|
| `gc supervisor install` | Install user-level service file (launchd on macOS, systemd on Linux). |
| `gc supervisor run` | Canonical foreground supervisor process; hosts the typed HTTP+SSE API. |
| `gc supervisor start/stop/restart/status/logs/reload` | Lifecycle. |
| `gc supervisor uninstall` | Remove the service file. |

### Rigs (Project Registration)

| Command | Purpose |
|---|---|
| `gc rig add <path> [--name N] [--include]` | Register an external project as a rig, allocate its bead prefix, link `.beads/` to inherit the city's Dolt endpoint. |
| `gc rig list/status/remove/restart/suspend/resume` | Rig management. |
| `gc rig set-endpoint` | Pin a rig to an external Dolt endpoint. |

### Agents

| Command | Purpose |
|---|---|
| `gc agent add --name <n> [--dir D]` | Scaffold `agents/<n>/prompt.template.md` + `agent.toml`. |
| `gc agent suspend/resume <n>` | Per-agent reconciler skip. |

### Sessions

| Command | Purpose |
|---|---|
| `gc session attach/peek/logs/list/new/close/kill/nudge` | Direct session manipulation. |
| `gc session pin/unpin/rename/prune/reset` | Session lifecycle. |
| `gc session wake/wait/submit` | Wake idled sessions, wait for completion, submit prompts. |
| `gc session suspend` | Per-session suspend (different from agent suspend). |

### Work Routing and Workflow

| Command | Purpose |
|---|---|
| `gc sling <target> <bead-id\|formula> [--formula] [--var k=v] [--nudge] [--owned] [--merge direct\|mr\|local] [--no-convoy]` | Core dispatch: route a bead (or wisp from a formula) to an agent/pool. |
| `gc formula list/show/cook [--var k=v] [--attach beadID]` | Inspect and instantiate formulas. `--attach` is the late-bound sub-DAG expansion primitive. |
| `gc order list/show/run/check/history/sweep-tracking` | Manage scheduled or event-triggered dispatch. |
| `gc converge create/list/status/iterate/approve/retry/stop/test-gate` | Bounded iterative refinement loops. |
| `gc convoy create/list/status/add/check/close/control/land/delete/stranded` | Convoy graph operations. `convoy control --serve` runs the control-dispatcher loop. |
| `gc graph <ids> [--tree|--mermaid]` | Render bead dependency graph. |
| `gc handoff [--target=t] [--auto]` | Send mail to self/target and kill or restart-request the session. |

### Mail and Nudge

| Command | Purpose |
|---|---|
| `gc mail send/inbox/read/peek/reply/archive/delete/mark-read/mark-unread/thread/count/check` | Mail = beads with `type="message"`. |
| `gc nudge status` | Show deferred-nudge queue (the immediate-nudge form is `gc session nudge`). |
| `gc wait list/inspect/cancel/ready` | Durable session waits. |

### Beads (work store)

| Command | Purpose |
|---|---|
| `gc bd [args...]` | Wrapped `bd` invocation routed to the correct rig directory. Forces `BD_EXPORT_AUTO=false`. |
| `gc beads health` | Lifecycle health (delegates to provider). |
| `gc beads city use-managed/use-external` | Toggle endpoint topology. |

### Observation, Diagnostics, Operations

| Command | Purpose |
|---|---|
| `gc events [--type T] [--since D] [--watch] [--follow] [--seq] [--after N] [--after-cursor C]` | Stream events from the typed API. JSONL output. |
| `gc events rotate` | Rotate the city event log. |
| `gc event emit <type> [--payload JSON]` | Emit a custom event (best-effort, always exits 0). |
| `gc trace start/stop/status/show/tail/cycle/reasons` | Session reconciler tracing. |
| `gc doctor [--fix] [--verbose] [--json]` | Diagnostic health checks; `--fix` does safe mechanical PackV1→V2 rewrites. |
| `gc dolt-cleanup` | Dolt orphan-database / orphan-process reaping. |
| `gc analyze reliability` | Correlate session.crashed/quarantined/idle_killed/draining counts per (model, prompt_version, rig). |

### Configuration and Inspection

| Command | Purpose |
|---|---|
| `gc config show [--validate] [--provenance] [--json] [-f file]` | Dump resolved city config. |
| `gc config explain [--rig R] [--agent A] [--provider P --json]` | Per-field provenance and provider-chain attribution. |
| `gc import add/install/check/list/upgrade/remove/why` | Pack import management (V2). |
| `gc pack fetch/list` | Legacy V1 remote pack cache (still supported for migration). |
| `gc prompt synth` | Synthesize a prompt template. |
| `gc prime [--strict] [--hook-format P]` | Output the behavioral prompt for the current agent. Used by `SessionStart` hooks. |
| `gc hook [agent] [--inject]` | Check for available work via the agent's `work_query`. Exit 0 if work exists. |
| `gc mcp list --agent A|--session S` | Inspect projected MCP config. |
| `gc skill list` | List visible skills. |
| `gc shell install/remove/status` | Install Gas City shell integration. |
| `gc dashboard serve [--port 8080] [--api URL]` | Web dashboard over the supervisor API. |
| `gc service list/restart/doctor` | Workspace HTTP services. |
| `gc build-image [--tag] [--push] [--rig-path]` | Docker build context + image for prebaked agents (K8s). |
| `gc completion bash/zsh/fish/powershell` | Shell completion. |
| `gc version` | Print version. |

The CLI is a *projection* of the typed object model; the HTTP+SSE API is the other projection. Neither re-implements domain logic (`AGENTS.md:117-128`).

---

## 4. Configuration Model — `city.toml` and Packs

### Three-File Separation

PackV2 cleanly partitions concerns (`docs/guides/shareable-packs.md:9-19`):

```
my-city/
├── pack.toml      # what the system IS  (portable, shareable)
├── city.toml      # how this deployment runs (rigs, capacity, substrates)
└── .gc/           # site bindings + runtime state  (machine-local)
```

- `pack.toml`: pack identity, named imports, providers, agent defaults, named sessions, pack-level patches.
- `city.toml`: rigs, rig-level patches, capacity & scheduling policy, beads/session/mail/events provider selection, daemon config, API config, etc.
- `.gc/`: machine-local rig path bindings (`site.toml`), `events.jsonl`, runtime metadata, controller socket, controller pidfile, controller lock, bead store working files, molecule artifact directories, system formulas, etc.

### Minimal `city.toml`

The Level 0-1 minimum (from `engdocs/architecture/config.md:254-263`):

```toml
[workspace]
name = "my-city"

[[agent]]
name = "worker"
prompt_template = "prompts/worker.md"
```

### Top-Level Sections of `city.toml`

From `docs/reference/config.md:7-37`:

| Section | Purpose |
|---|---|
| `workspace` | Name + city-level provider default + `suspended` flag |
| `[[agent]]` | Inline agent definitions (legacy V1 surface; new packs use `agents/<name>/`) |
| `[[named_session]]` | Canonical alias-backed sessions built from agent templates |
| `[[rigs]]` | External projects (path + name + imports + patches + `formula_vars`) |
| `[providers.<name>]` | Provider preset overrides (claude, codex, gemini, cursor, copilot, amp, opencode, kiro by default) |
| `[packs.<name>]` | V1 remote pack source (git URL + ref + subdir) |
| `[imports.<name>]` | V2 named pack imports |
| `[patches]` | Targeted modifications applied after composition (agent, rig, provider) |
| `[beads] provider = ""` | `"bd"` (default), `"file"`, `"exec:<script>"` |
| `[session] provider = ""` | `""`/tmux, `"fake"`, `"subprocess"`, `"exec:<script>"`, `"k8s"` |
| `[mail] provider = ""` | `"beadmail"` (default) or `"exec:<script>"` |
| `[events] provider = ""` | File JSONL (default), `"fake"`, `"fail"`, `"exec:<script>"` |
| `[dolt]` | Dolt server connection overrides |
| `[formulas] dir = ""` | V1 city-local formula directory |
| `[daemon]` | `patrol_interval`, `max_restarts`, `restart_window`, `shutdown_timeout`, `wisp_gc_interval`, `wisp_ttl` |
| `[orders] skip = [...]` / `max_timeout = ""` | Global order filters |
| `[api] port` / `bind` / `allow_mutations` | HTTP API server |
| `[chat_sessions]` | Auto-suspend for chat sessions |
| `[session_sleep]` | Idle sleep policy defaults |
| `[convergence]` | Convergence loop limits |
| `[doctor]` | gc doctor thresholds/toggles |
| `[[service]]` | Workspace HTTP services mounted on the controller edge under `/svc/{name}` |
| `[agent_defaults]` | City-level defaults for `provider`, `wake_mode`, `default_sling_formula`, etc. |
| `[[pricing]]` | Per-model cost overrides |

### Progressive Activation (Levels 0-8)

`engdocs/architecture/nine-concepts.md:183-194` calls this the "Progressive Capability Model": capabilities turn on by the *presence* of config sections, not by feature flags.

| Level | Config Required | Adds |
|---|---|---|
| 0-1 | `[workspace]` + `[[agent]]` | Session + tasks |
| 2 | `[daemon]` | Controller loop |
| 3 | `[[agent]]` with `[agent.pool]` | Multiple agents + pool |
| 4 | `[mail]` | Messaging |
| 5 | Formula files + `[formulas]` | Formulas & molecules |
| 6 | `[daemon]` health fields | Health monitoring |
| 7 | `orders/` directories | Orders |
| 8 | All sections | Full orchestration |

This is one of the cleaner ideas in the codebase: there are no capability flags, no feature flags. The config IS the feature flag (`engdocs/architecture/nine-concepts.md:86-91`).

### Pack Composition

A **pack** is a portable definition directory containing `pack.toml`, `agents/`, `formulas/`, `orders/`, `commands/`, `doctor/`, `overlay/`, `skills/`, `mcp/`, `template-fragments/`, and `assets/` (`docs/guides/shareable-packs.md:22-51`). Packs compose other packs via named imports:

```toml
# pack.toml
[pack]
name = "my-city"
schema = 2

[imports.gastown]
source = "./assets/gastown"

[imports.review]
source = "github.com/gastownhall/code-review"
version = "^1.2"
```

A city imports packs at its root pack. The local binding name (`gastown` above) is what the rest of the pack references — so an agent imported from the Gastown pack is qualified as `gastown.mayor`, distinct from `review.mayor` if you also imported one from another pack. Imports are transitive by default; set `transitive = false` for internal-only imports.

### Override Layering

`engdocs/architecture/config.md:44-50` documents the override resolution chain. From least to most specific:

1. Built-in provider presets (`BuiltinProviders()` in `internal/config/provider.go`)
2. City-level `[providers]`
3. Workspace defaults (`workspace.provider`)
4. Per-agent fields (in `agents/<name>/agent.toml` or `[[agent]]`)
5. Rig-level `[[rigs.overrides]]` (rewrite a pack-stamped agent for a specific rig)
6. City-level `[patches]` (post-composition targeted edits to a fully-resolved agent)

The composition pipeline is six explicit steps (`engdocs/architecture/config.md:67-99`):

```
city.toml → parse → merge fragments (include) → resolve named packs →
expand city packs (stamp dir="" agents) → apply patches →
expand rig packs (stamp dir=rig agents) → compute formula layers
```

Steps 4 and 6 are ordered so that patches target city agents *before* rig packs stamp per-rig agents. The result is a single flat `*config.City` struct + a `Provenance` map that tracks the source file of every field.

### PackV1 → PackV2 Migration

`docs/guides/migrating-to-pack-vnext.md` explains the migration. The mental shift is:

- 0.14.0 PackV1 centered `city.toml` with explicit path wiring and `includes`.
- 0.14.1+ PackV2 centers `pack.toml` and named imports, with `city.toml` shrunk to deployment-only decisions.

The migration path is `gc doctor` → `gc doctor --fix` → `gc doctor` again. `gc import migrate` is deprecated. V1 surfaces (`workspace.includes`, `[[rigs]].includes`, `[packs.*]`, `[[agent]]`, `[formulas].dir`) still load for backward compatibility (`docs/guides/shareable-packs.md:237-249`).

### `[agent_defaults]` (City-level)

Some `[agent_defaults]` fields are tombstones from a partially-rolled-back feature (`docs/reference/config.md:117-131`): `skills` and `mcp` are accepted but ignored by the active materializer; `allow_overlay`, `allow_env_override`, `model`, `wake_mode` are parsed/composed but not yet auto-applied at runtime. The active fields that *do* inherit are `default_sling_formula` and `append_fragments`.

---

## 5. Runtime Providers

### The `runtime.Provider` Interface

`internal/runtime/runtime.go:102-184` defines the production provider contract. The signatures (abridged):

```go
type Provider interface {
    Start(ctx context.Context, name string, cfg Config) error
    Stop(name string) error
    Interrupt(name string) error
    IsRunning(name string) bool
    IsAttached(name string) bool
    Attach(name string) error
    ProcessAlive(name string, processNames []string) bool
    Nudge(name string, content []ContentBlock) error
    SetMeta(name, key, value string) error
    GetMeta(name, key string) (string, error)
    RemoveMeta(name, key string) error
    Peek(name string, lines int) (string, error)
    ListRunning(prefix string) ([]string, error)
    GetLastActivity(name string) (time.Time, error)
    ClearScrollback(name string) error
    CopyTo(name, src, relDst string) error
    SendKeys(name string, keys ...string) error
    RunLive(name string, cfg Config) error
    Capabilities() ProviderCapabilities
}
```

Optional extension interfaces (`InteractionProvider`, `IdleWaitProvider`, `ImmediateNudgeProvider`) layer on top. Idempotency, "session-not-found" semantics, and metadata persistence are governed by invariants in `engdocs/architecture/session.md:134-144`.

The session name is computed by `agent.SessionNameFor()` (`internal/agent/session_name.go`) and must be stable for a given (city, agent, template). A SHA-256 `runtime.ConfigFingerprint()` (`internal/runtime/fingerprint.go`) detects config drift across reconciler ticks; the fingerprint carries a `vN:` prefix and the controller silently rebaselines stored fingerprints when the version increments (`engdocs/architecture/session.md:196-273`).

### Provider Implementations

| Provider | Package | Use case | Notes |
|---|---|---|---|
| **tmux** | `internal/runtime/tmux/` | Primary interactive runtime | Polls process tree for `process_names`, supports attach, scrollback, dialog dismissal. The dominant production path. |
| **subprocess** | `internal/runtime/subprocess/` | Local non-interactive | Fire-and-forget child process; no attach. Used when `attach = false`. |
| **exec** | `internal/runtime/exec/` | Pluggable session backend | Calls a user-supplied script for every operation. JSON config on stdin for start. Wire protocol fully documented in `docs/reference/exec-session-provider.md`. |
| **k8s** | `internal/runtime/k8s/` | Kubernetes | Native client-go (no `kubectl` subprocess). Compatible with `gc build-image` prebaked images. Pods carry agent-specific labels and tmux inside. |
| **acp** | `internal/runtime/acp/` | Agent Client Protocol | JSON-RPC over stdio. Used when `[[agent]] session = "acp"` and the agent's resolved provider has `supports_acp = true`. |
| **auto** | `internal/runtime/auto/` | Routing layer | Dispatches between local and remote based on policy. |
| **hybrid** | `internal/runtime/hybrid/` | Routing layer | Mixed local+remote. |
| **fake** | `internal/runtime/fake.go` | Tests | Records calls; spy capability. |

### Exec Session Provider Wire Contract

The exec provider is the documented plug-point for any terminal multiplexer (screen, zellij, kitty, mosh, custom container managers). From `docs/reference/exec-session-provider.md:42-60`:

| Operation | Invocation | Stdin | Stdout |
|---|---|---|---|
| `start` | `script start <name>` | JSON config | — |
| `stop` | `script stop <name>` | — | — |
| `interrupt` | `script interrupt <name>` | — | — |
| `is-running` | `script is-running <name>` | — | `true`/`false` |
| `attach` | `script attach <name>` | tty | tty |
| `process-alive` | `script process-alive <name>` | process names | `true`/`false` |
| `nudge` | `script nudge <name>` | message | — |
| `set-meta`/`get-meta`/`remove-meta` | + key | (value on stdin for set) | (value for get) |
| `peek` | `script peek <name> <lines>` | — | captured text |
| `list-running` | `script list-running <prefix>` | — | names |
| `get-last-activity` | `script get-last-activity <name>` | — | RFC3339 |

**Exit code 2 = "unknown operation" = treated as success (forward-compatible).** That single forward-compatibility convention is critical: scripts only implement what they care about.

### Provider Capabilities Differ

`engdocs/architecture/session.md:275-282` flags this as a known limitation: not every provider supports interactive attach, idle waiting, or pending interactions. The `runtime.ProviderCapabilities` struct lets the reconciler skip inapplicable wake reasons rather than fail. The Kubernetes provider has the fewest interactive features; tmux has the most.

### Built-in Providers (LLM Agents)

`BuiltinProviders()` in `internal/config/provider.go` defines presets for: claude (Claude Code), codex (Codex CLI), gemini (Gemini CLI), cursor (Cursor Agent), copilot (GitHub Copilot), amp (Sourcegraph Amp), opencode (OpenCode), auggie (Auggie CLI), pi/omp (Pi Coding Agent / Oh My Pi), and kiro (Kiro CLI, defaulting to `kiro-cli chat --no-interactive --agent gascity --trust-all-tools`). Each preset specifies `command`, `args`, `prompt_mode` (`arg`/`flag`/`none`), `prompt_flag`, env, and `supports_acp`. Agents inherit from a provider preset and may override any field.

---

## 6. Beads Provider Abstraction

### The `beads.Store` Interface

Ten methods (`engdocs/architecture/beads.md:23-31`):

```go
type Store interface {
    Create(b Bead) (Bead, error)
    Get(id string) (Bead, error)
    Update(id string, opts UpdateOpts) error
    Close(id string) error
    List() ([]Bead, error)
    Ready() ([]Bead, error)
    Children(parentID string) ([]Bead, error)
    ListByLabel(label string, limit int) ([]Bead, error)
    SetMetadata(id, key, value string) error
    MolCook(formula, title string, vars []string) (string, error)
}
```

### Four Implementations

| Provider | Backing | Production? |
|---|---|---|
| `BdStore` | bd CLI → Dolt SQL | **Yes** (default) |
| `FileStore` | JSON file (embeds MemStore) | Tutorials, lightweight |
| `MemStore` | In-memory slice + mutex | Unit tests |
| `exec.Store` | User-supplied script | Plug-in (e.g. `beads_rust`) |

The exec store's JSON wire protocol mirrors the exec session provider's: stdin is a JSON request, stdout is a JSON response; exit code 2 = unknown operation (forward-compatible). `internal/beads/exec/br_test.go` runs the conformance suite against `beads_rust` as proof.

### Provider Selection

Resolved at `cmd/gc/main.go:openCityStore` (`engdocs/architecture/beads.md:66-74`):

1. `GC_BEADS` env var
2. `[beads].provider` in `city.toml`
3. Default `"bd"`

Set `GC_BEADS=file` (or `[beads] provider = "file"`) for a no-dependency tutorial setup. Production stays on `bd`.

### Multi-Rig Bead Topology

`docs/internals/beads-topology.md` explains this beautifully. The structure:

- One **Dolt SQL server process** per city, listening on a port recorded in `.beads/dolt-server.port`.
- The city's `.beads/config.yaml` carries `issue_prefix: <prefix>` and `gc.endpoint_origin: managed_city`.
- Each rig's `.beads/config.yaml` carries its *own* `issue_prefix` and `gc.endpoint_origin: inherited_city`.
- All `.beads/` directories point at the same Dolt server, but `bd` enforces prefix scoping on every read and write.

So a two-rig city has three logical bead scopes (city + 2 rigs) but one physical Dolt server. The four legal `gc.endpoint_origin` values, documented in `internal/beads/contract/files.go`:

| Value | Meaning |
|---|---|
| `managed_city` | This city runs its own local Dolt; the port lives in `.beads/dolt-server.port`. |
| `inherited_city` | This rig has no endpoint; resolve through the city. |
| `city_canonical` | City points at an external Dolt server. |
| `explicit` | Rig has its own external endpoint. |

The bead ID prefix (e.g. `mc-gne`, `riga-h2t`) is how `bd ready`, `bd list`, etc. know which scope to query. The mapping is also how `gc bd <args>` auto-routes — if you say `gc bd show riga-abc`, `gc` cd's into the rig directory before exec-ing `bd`.

### Status Mapping

`engdocs/architecture/beads.md:185-188` notes that `bd` has six statuses (open, in_progress, blocked, review, testing, closed) but Gas City exposes only three (`open`, `in_progress`, `closed`). `BdStore` collapses blocked/review/testing to `open` and an empty backend status to `open`.

### Architectural Boundary Tests

`internal/beads/boundary_test.go:TestNoBdExecOutsideBeads` walks the repo and fails the build if any Go file outside `internal/beads/` or `test/integration/` directly invokes the `bd` binary. That's a hard architectural invariant.

---

## 7. Workflow Primitives — Formulas, Molecules, Orders, Convergence, Sling

### Formulas

A **formula** is a `*.formula.toml` file declaring a workflow template (`docs/reference/formula.md`). Schema:

```toml
formula = "pancakes"
description = "Make pancakes"
version = 1

[[steps]]
id = "dry"
title = "Mix dry ingredients"
description = "Combine flour, sugar, baking powder."

[[steps]]
id = "wet"
title = "Mix wet ingredients"
description = "Combine eggs, milk, butter."

[[steps]]
id = "cook"
title = "Cook pancakes"
description = "Cook on medium heat."
needs = ["dry", "wet"]
```

Steps form a **DAG** via `needs`. Steps support `condition` (equality on vars), `children` (nested sub-steps), `loop` (static compile-time expansion with `count`), `check` (runtime retry with `max_attempts`), `timeout`, `extends`, and graph.v2 decorators. The compile pipeline lives in `internal/formula/compile.go`.

Formulas are layered (`engdocs/architecture/formulas.md:107-118`):

```
1. City pack formulas    (lowest)
2. City local formulas
3. Rig pack formulas
4. Rig local formulas    (highest)
```

`ResolveFormulas()` (`cmd/gc/formula_resolve.go`) scans each layer, picks the highest-priority winner by filename, and creates **symlinks** in `<target>/.beads/formulas/`. It never overwrites real files. Stale symlinks are cleaned. System formulas are embedded in the `gc` binary and materialized to `.gc/system-formulas/` at startup.

### Molecules

A **molecule** is a formula instantiated at runtime: one root bead (`type="molecule"`, `Ref=formulaName`) plus one child bead per formula step (`type="task"`, `ParentID=root`, `Ref=stepID`). Progress is tracked by closing the child beads.

The store interface seam is `MolCook(formula, title, vars)` and `MolCookOn(formula, beadID, title, vars)`. Implementations:

- `BdStore.MolCook` shells out to `bd mol wisp`.
- `BdStore.MolCookOn` calls `bd mol bond`.
- `exec.Store` forwards `mol-cook` and `mol-cook-on` to a user script.
- `MemStore` / `FileStore` create a simplified molecule root suitable for tutorials only.

**Root-only vs poured (full DAG)** depends on the backend. The architecture doc is explicit: "Full multi-step formula execution is backend-dependent today; `BdStore` is the production path" (`engdocs/architecture/formulas.md:160-162`).

### Wisps

A **wisp** is an ephemeral molecule with a TTL. Wisps are created by `gc sling --formula <name>` or by order dispatch. Closed wisps older than `[daemon].wisp_ttl` are reaped by `cmd/gc/wisp_gc.go` every `[daemon].wisp_gc_interval`. The bead store's `MolCook` is the wisp constructor.

### Orders

Orders pair a **trigger** (when to fire) with an **action** (formula or exec) and live in `orders/<name>/order.toml` files inside formula directories.

The five trigger types (`internal/orders/triggers.go`, `engdocs/architecture/orders.md:29-37`):

| Trigger | Param | Semantics |
|---|---|---|
| `cooldown` | `interval = "5m"` | Minimum time since last successful run. |
| `cron` | `schedule = "0 3 * * *"` | 5-field cron, minute granularity. |
| `condition` | `check = "test -f /tmp/flag"` | Shell command exits 0. |
| `event` | `on = "bead.closed"` | Matching events after a cursor. |
| `manual` | — | Never auto-fires; only `gc order run`. |

Actions:

- **Exec orders** run shell scripts directly on the controller. No LLM, no agent, no wisp. Get `ORDER_DIR` in env. Default timeout 60s.
- **Formula orders** call `MolCook` to instantiate a wisp and label it for pool dispatch. Default timeout 30s.

**Tracking beads** are the critical correctness mechanism. Before each dispatch goroutine starts, the controller synchronously creates a bead labeled `order-run:<scopedName>`. This prevents the cooldown trigger from re-firing on the next tick before the in-flight order has finished (`engdocs/architecture/orders.md:215-218`). Tracking beads also enable cursor-based deduplication for event triggers (`seq:<N>` labels).

**ScopedName** isolates orders across rigs: `dolt-health:rig:rig-a` vs `dolt-health:rig:rig-b`. Pool names are auto-qualified per rig too: `pool = "worker"` in rig `demo-repo` becomes `pool:demo-repo/worker` on the wisp label.

Failed orders **do not retry**; the tracking bead prevents re-fire within the cooldown window, and the operator gets an `order.failed` event.

### Convergence — Bounded Iterative Refinement

`internal/convergence/` is Gas City's analog to Attractor's convergence concept. It is **bounded iterative refinement loops over agent work**. A convergence loop is:

> A root bead + a formula + a gate = repeat until the gate passes or max iterations are reached.

From `gc converge create --help` flags:

| Flag | Purpose |
|---|---|
| `--formula` | Workflow template to run each iteration |
| `--target` | Agent to dispatch each iteration to |
| `--max-iterations` (default 5) | Hard cap on iterations |
| `--gate` (`manual`/`condition`/`hybrid`) | How to decide "are we done?" |
| `--gate-condition` | Path to gate condition script |
| `--gate-timeout` (default `5m`) | Gate script timeout |
| `--gate-timeout-action` (`iterate`/`retry`/`manual`/`terminate`) | What to do on timeout |
| `--evaluate-prompt` | Custom evaluate prompt (else `prompts/convergence/evaluate.md`) |
| `--var key=value` | Template variable |

The state machine (`internal/convergence/metadata.go:47-52`):

```
States: creating → active → waiting_manual → terminated
GateModes: manual, condition, hybrid
TimeoutActions: iterate, retry, manual, terminate
TerminalReasons: approved, no_convergence, stopped, partial_creation
GateOutcomes: pass, fail, timeout, error
```

The handler (`internal/convergence/handler.go`) consumes `wisp_closed` events and emits the next iteration. Iterations are keyed by an **idempotency key** (`converge:<beadID>:iter:<N>`) so a controller crash and restart can't double-run an iteration. After each iteration the agent writes `convergence.agent_verdict` (one of two agent-writable metadata keys; everything else under `convergence.*` requires the controller's `GC_CONVERGENCE_TOKEN`). The gate is then evaluated:

- **Manual gate**: human runs `gc converge iterate <id>` (force next) or `gc converge approve <id>` (close as approved).
- **Condition gate**: a shell script is run with a 5-min default timeout; exit 0 = pass.
- **Hybrid**: condition first, then manual approval if condition passes.

Convergence is reconcile-driven: a controller restart finds in-progress convergence beads (`internal/convergence/reconcile.go`) and resumes them. The actor that wrote `convergence.terminal_actor` (controller, agent, operator) is recorded.

This is structurally similar to Attractor DOT pipelines (bounded loops, gate-based termination), but the gating mechanism is more general: a gate can be any shell command, and the iteration body is any formula. It's a generic refinement loop, not a coding-specific one.

### Sling — Dispatch

**Sling** is the act of routing a bead (or a wisp from a formula) to a target agent or pool. The pipeline (`engdocs/architecture/dispatch.md:60-86`):

```
cmdSling()       resolve city, config, agent, store
  └─ doSlingBatch()      container expansion (convoy → children)
       └─ doSling()      single-bead dispatch:
            ├─ instantiateWisp()    [--formula]  Store.MolCook
            ├─ checkBeadState()      pre-flight warn re-route
            ├─ buildSlingCommand()   {} → bead ID
            ├─ runner(slingCmd)      execute via sh -c
            ├─ telemetry.RecordSling()
            ├─ store.SetMetadata()   [--merge] direct/mr/local
            ├─ store.Create(convoy)  [auto-convoy] unless --no-convoy
            └─ doSlingNudge()        [--nudge] wake target
```

Each agent has a `sling_query` shell template (with `{}` as bead-ID placeholder). Defaults: `bd update {} --assignee=<qualified-name>` for fixed agents, `bd update {} --label=pool:<qualified-name>` for pool agents. Operators can override per-agent.

**Container expansion**: when slung a convoy bead, dispatch lists all open children and routes each individually — the container itself becomes the convoy (no auto-convoy is created). Epics are **not** containers and are not expanded.

**Auto-convoy**: when slinging a single non-formula non-container bead, dispatch automatically wraps it in a fresh convoy bead for batch tracking. Suppressed with `--no-convoy`.

**`--owned`**: the convoy is marked "owned" (manual lifecycle, no auto-close), and the natural termination is `gc convoy land <id>`.

**`--merge`**: writes `gc.merge_strategy = direct|mr|local` to bead metadata so downstream workflow steps (notably `mol-polecat-work`) know how to land changes.

---

## 8. The Controller / Supervisor Loop

### Two Hosting Modes

`gc start` registers the city with the machine-wide supervisor and waits for the city to become active. The supervisor is the canonical long-running process (`gc supervisor run`); it hosts the typed HTTP+SSE API and runs **one `CityRuntime` per registered city** (`engdocs/architecture/controller.md:13-22`). A hidden `gc start --foreground` compatibility mode runs a standalone per-city controller. Both paths use the same `runController()` code in `cmd/gc/controller.go`.

### The Tick Loop

The reconciliation loop in `controllerLoop()` runs on a configurable ticker (default 30s) and on filesystem-notified config changes. Each tick (`engdocs/architecture/controller.md:99-127`):

1. **Dirty check** — if config files changed (debounced fsnotify), reparse `city.toml` with includes/patches, rebuild crash/idle/wisp-GC/order trackers.
2. **Agent list build** (`buildAgents(cfg)`) — re-evaluate desired agents, in parallel run `scale_check` for pool agents.
3. **Reconcile** (`reconcileSessionBeads()`) — declarative convergence: bring running sessions into match with the desired set.
4. **Wisp GC** — purge closed wisps older than `wisp_ttl`.
5. **Order dispatch** — evaluate triggers, fire due orders, create tracking beads.

### What "Desired" vs "Running" Mean

- **Desired** = the set of agents the resolved config currently requires (after `[[agent]]` + pack expansion + patches + pool `scale_check` evaluations + suspension state).
- **Running** = `runtime.Provider.ListRunning(prefix)` filtered by city prefix + the live bead-backed session projection in `internal/session/lifecycle_projection.go`.

The reconciler (`cmd/gc/session_reconciler.go`) implements a four-state machine (`engdocs/architecture/health-patrol.md:122-136`):

```
Not alive         → should wake     → Start
Healthy           → alive + desired → Skip
Orphan/suspended  → not desired     → Drain or close
Drifted           → hash differs    → Drain + restart
```

Within "running" the sub-states are: restart-requested → idle-timeout-exceeded → config-drift. Crash-loop-quarantined agents are skipped silently.

### Erlang/OTP Mapping

`engdocs/architecture/health-patrol.md:251-267` makes the Erlang/OTP comparison explicit:

| Erlang/OTP | Gas City |
|---|---|
| Supervisor | Controller (`controllerLoop`) |
| Worker | Session running an `[[agent]]` role |
| Child spec | `[[agent]]` entry |
| `one_for_one` | Restart dead agent only (default; no cascade — only one strategy supported) |
| `max_restarts`/`max_seconds` | `max_restarts` / `restart_window` |
| "Let it crash" | GUPP + beads: agent dies, hook persists, fresh session picks up persisted work |
| Process mailbox | Mail inbox (beads with `type=message`) |
| GenServer loop | Agent loop: check hook → run → repeat |

### Dependency-Aware Parallel Lifecycle

Recent work (`engdocs/design/dependency-aware-bounded-parallel-lifecycle.md`, implemented) added **dependency-ordered bounded-parallel session starts and force-stops**. Agents declare `depends_on = [...]` and the reconciler:

- Plans starts serially in topological order.
- Groups starts into dependency waves.
- Runs each wave with bounded parallelism (via worker pool).
- Applies success/failure side effects serially in stable plan order.

Bulk stop paths (`gc stop`, controller shutdown, provider swap, `gc rig restart`) send interrupts to all sessions first, then force-stop survivors in reverse dependency waves.

### Graceful Shutdown

Two-pass: send `Interrupt()` (Ctrl-C) to all sessions, wait `[daemon].shutdown_timeout`, then force-`Stop()` survivors. Order dispatch goroutines are drained with a bounded timeout so tracking-bead outcomes and `order.completed`/`order.failed` events are persisted.

### Single-Controller Invariant

`flock(LOCK_EX|LOCK_NB)` on `.gc/controller.lock` enforces at most one standalone controller per city. The Unix socket at `.gc/controller.sock` is used for discovery (status pings and the `stop` command); it is **not** the source of liveness — `runtime.Provider.IsRunning()` and `ProcessAlive()` inspect the live process tree. The principle stated in `AGENTS.md:208-212`:

> **No status files — query live state.** Never write PID files, lock files, or state files to track running processes. Always discover state by querying the system directly. Status files go stale on crash and create false positives.

---

## 9. Communication and Signaling

### Mail (Durable, Persistent)

Mail is composed entirely from the Bead Store. `mail.Provider.Send(from, to, subject, body)` → `store.Create(Bead{Type:"message", Title:subject, Description:body, Assignee:to, From:from, Labels:["thread:<id>"]})`. The inbox is `store.List()` filtered for `Type="message"`, `Status="open"`, `Assignee=recipient`, no `"read"` label.

Lifecycle (`engdocs/architecture/messaging.md:175-182`):

```
Send → [unread, open]
  ├── Read → [read label, open]   (still in Get/Thread/Count)
  │     ├── MarkUnread → [unread, open]
  │     └── Archive → [closed]    (permanent)
  ├── Peek/Get → [unread, open]    (no state change)
  └── Archive/Delete → [closed]    (permanent, skips read)
```

Threads are label-based (`thread:<id>` + `reply-to:<id>`). Two providers: `beadmail` (default) and `exec` (script). No delivery confirmation; no read receipts.

### Nudge (Ephemeral, Fire-and-Forget)

`runtime.Provider.Nudge(name, content)` types text into the agent's session. Not persisted. If the session is asleep, the nudge can be **deferred** into a persistent queue at `.gc/nudges/...` (`internal/nudgequeue/state.go`), to be delivered when the agent is at a safe interactive boundary. The deferred-nudge queue is managed by `gc nudge` (status/drain/poll).

### Waits

Durable session waits live as beads with `Type="gate"` (legacy `"wait"`). They're inspected via `gc wait list/inspect`, completed by `gc wait ready`, canceled by `gc wait cancel`. They are the primitive behind "pause this agent until external work completes." The wait helpers in `internal/session/waits.go` manage the bead state.

### Handoff

`gc handoff [subject] [message]` is convenience sugar:

- **Self-handoff (default)**: sends mail to self and requests controller restart. Blocks until controller stops the session. For controller-restartable sessions, equivalent to `gc mail send $GC_ALIAS <subject> [message]` + `gc runtime request-restart`.
- **Auto handoff (`--auto`)**: sends mail without requesting restart. For PreCompact hooks where the provider already manages context compaction.
- **Remote handoff (`--target=t`)**: sends mail to target and kills it (if controller-restartable) so the reconciler restarts it with mail waiting.

---

## 10. Multi-Project Orchestration — Rigs, Overrides, Packs

### Rigs as Projects

A **rig** is an external project directory registered in the city via `gc rig add <path> [--name N]`. Each rig:

- Gets its own bead prefix (deterministically derived from the rig name).
- Gets its own `.beads/` directory with `gc.endpoint_origin: inherited_city` (shares the city's Dolt server).
- Stamps rig-scoped agents from rig-level pack imports.
- Carries its own formula directory layer (rig-local), higher priority than city-local.

The rig's filesystem path lives in `.gc/site.toml` (machine-local site binding). `city.toml` declares the rig by name + capacity policy. The same `pack.toml` works on multiple machines.

### Override Cascade

```
Built-in provider preset
  ↓
City [providers.<name>] override
  ↓
Workspace.provider default
  ↓
[[agent]] (or agents/<n>/agent.toml) per-agent fields
  ↓
[[rigs.overrides]] for pack-stamped agents in this rig
  ↓
[patches] post-composition targeted edits
```

This lets a city use a pack's mayor agent on Claude in one rig and Codex in another rig with three lines of TOML:

```toml
[[rigs]]
name = "frontend"
[rigs.imports.gastown]
source = "./assets/gastown"

[[rigs.patches]]
agent = "gastown.polecat"
provider = "codex"
```

### Rig-Scoped Orchestration

Several primitives carry rig scope through their identity:

- **Bead prefixes**: `riga-h2t`, `rigb-gne` — `bd` queries are scoped by prefix.
- **Order scoped names**: `dolt-health:rig:rig-a` vs `dolt-health:rig:rig-b` — independent cooldowns and event cursors.
- **Pool labels**: `pool:rig-a/worker` (auto-qualified from `pool = "worker"`).
- **Formula layer stacks**: per-rig stacks computed by `ComputeFormulaLayers()` in `internal/config/pack.go`.
- **Formula vars**: `[rigs.formula_vars]` provides rig-level defaults that fold into `BuildSlingFormulaVars` at dispatch time (`engdocs/architecture/formulas.md:200-230`).

---

## 11. Observability

### Event Bus

The Event Bus is the universal observation substrate (`engdocs/architecture/event-bus.md`). Every state change emits an immutable, monotonically-sequenced JSON record to `.gc/events.jsonl` (FileRecorder default) or to the configured provider. The `events.Provider` interface:

```go
type Provider interface {
    Record(Event)                                // best-effort, never returns errors
    List(Filter) ([]Event, error)
    LatestSeq() (uint64, error)
    Watch(ctx, afterSeq uint64) (Watcher, error) // blocks on Next()
    Close() error
}
```

JSONL format is append-only with `O_APPEND` for cross-process safety. Partial writes are tolerated (malformed lines are skipped). Seq is auto-filled, monotonically increasing, and resumes across process restarts by scanning the file on `NewFileRecorder()`.

The `Watcher` polls every 250ms (no inotify) — that's an acknowledged limitation. The `Fake` provider uses channel-based notification for zero-latency tests. The `exec.Provider` shells to a user script with an NDJSON streaming wire protocol for `watch`.

### Event Types

Well over 40 typed events are emitted. The constants are defined in `internal/events/events.go:KnownEventTypes`. Highlights:

| Category | Examples |
|---|---|
| Session lifecycle | `session.woke`, `session.stopped`, `session.crashed`, `session.draining`, `session.undrained`, `session.idle_killed`, `session.updated`, `session.quarantined` (reserved), `session.suspended` (reserved) |
| Beads | `bead.created`, `bead.closed`, `bead.updated` |
| Mail | `mail.sent`, `mail.read`, `mail.archived`, `mail.marked_read`, `mail.marked_unread`, `mail.replied`, `mail.deleted` |
| Convoys | `convoy.created`, `convoy.closed` |
| Controller | `controller.started`, `controller.stopped` |
| Supervisor | `supervisor.shutdown_requested` (with trigger attribution: source, signal, client addr, mode), `supervisor.fs_pressure.skipped_tick` |
| City | `city.suspended`, `city.resumed`, `city.created`, `city.unregister_requested` |
| Async API | `request.result.city.create`, `request.result.session.create`, `request.failed`, etc. |
| Orders | `order.fired`, `order.completed`, `order.failed` |
| Provider | `provider.swapped` |
| Worker | `worker.operation` (per-invocation: model, prompt_version, agent_name, session_id) |
| Project identity | `project.identity.stamped` |
| External messaging | `extmsg.bound`, `extmsg.unbound`, `extmsg.group_created`, `extmsg.adapter_added`, `extmsg.adapter_removed`, `extmsg.inbound`, `extmsg.outbound` |
| Events | `events.rotated` |

A CI-enforced contract requires that every constant in `events.KnownEventTypes` has a registered payload via `events.RegisterPayload(constant, sample)` (`AGENTS.md:130-134`).

### OTel Telemetry

`internal/telemetry/recorder.go` emits OTel log events (→ VictoriaLogs in the canonical setup) and increments metric counters (→ VictoriaMetrics) for every tracked operation: sling dispatch, bd CLI invocations, provider startup, per-invocation cost/usage, etc. The invocation metrics (`internal/telemetry/recorder_invocation.go`) intentionally limit cardinality to `{agent_name, model, provider}` — per-bead/per-prompt-SHA detail lives in the `worker.operation` event log instead, to bound metric cardinality.

### Reliability Analysis

`gc analyze reliability` correlates session-lifecycle events with model/prompt_version/rig dimensions, computing crash rates over `--since 7d` windows. The intent is to detect provider regressions across model versions.

### Session Logs and Traces

- `gc session logs <id> [--tail N]` returns the last N entries from the session log (Unix `tail` convention).
- `gc trace start/stop/status/show/tail/cycle/reasons` controls session-reconciler tracing (`engdocs/contributors/reconciler-debugging.md`).
- `internal/sessionlog` reads Claude Code's JSONL transcript files for analysis.

### Consuming Events from Outside

The supervisor's HTTP+SSE API is the public consumption surface (`docs/reference/api.md`):

- `GET /v0/events` / `GET /v0/events/stream` — supervisor scope.
- `GET /v0/city/{cityName}/events` / `GET /v0/city/{cityName}/events/stream` — city scope.

SSE streams support `Last-Event-ID` reconnect; events have monotonic seq numbers for incremental consumption. `gc events --follow` is the CLI consumer.

---

## 12. Trust and Security Boundaries

`docs/reference/trust-boundaries.md` is unambiguous: **Gas City intentionally runs operator-configured commands. Those commands are a feature, not a sandbox.** Configs, imported packs, and exec provider scripts are *trusted code with the same review expectations as shell scripts committed to the repository.*

Three trust tiers:

| Tier | Inputs | Rule |
|---|---|---|
| **Trusted operator code** | `city.toml`, local site config | May define shell commands and explicit env |
| **Trusted dependency code** | Imported packs, rig configs | Pin/review before importing |
| **Untrusted data** | Bead titles/descriptions, mail, formula vars, PR text, API request fields | Never concatenate into shell; pass as env/JSON/stdin/argv |

### Secret Propagation

Controller-side shell helpers automatically strip ambient env vars whose keys contain `TOKEN`, `PASSWORD`, `SECRET`, `PRIVATE_KEY`, `API_KEY`, `ACCESS_KEY`, `CREDENTIAL`, `OAUTH`, `AUTH_JSON` before invoking any operator command (`internal/execenv`). Explicit env values from config are preserved (operator-intentional).

### Controller Token (`GC_CONVERGENCE_TOKEN`)

The convergence subsystem uses a token to gate access to the `convergence.*` metadata namespace (`internal/convergence/acl.go`). Only `convergence.agent_verdict` and `convergence.agent_verdict_wisp` are agent-writable; everything else (state transitions, gate config, iteration counters) requires the controller token. `ScrubTokenEnv()` removes the token before spawning agent sessions, so agents can never see it.

### API Authentication

The HTTP API requires an `X-GC-Request` header on every mutation endpoint (POST/PUT/PATCH/DELETE) as an anti-CSRF gate. Any non-empty value is accepted — the header's presence is what's checked, leveraging the same-origin policy (`docs/reference/api.md:51-60`). Default API bind is `127.0.0.1`; non-localhost binds reject mutations unless `[api] allow_mutations = true` is set.

### Single-Operator Local Trust Model

The Unix socket at `.gc/controller.sock` has no authentication. Any local process with filesystem access to it can send `stop` (`engdocs/architecture/controller.md:344-346`). File permissions (`0o755` on `.gc/`) are the only access control. This is fine on personal dev machines but is an open question for multi-user installs.

---

## 13. The Go API for Embedding

`docs/reference/api.md` is about the **HTTP** control plane. There is *no documented Go library API* for embedding Gas City in another Go program. `AGENTS.md:178-179` is explicit:

> **`internal/` packages for now.** SDK exports (`pkg/`) are future work. Everything is private to the `gc` binary until the API stabilizes.

So Gas City today is **a binary plus a typed HTTP+SSE control plane**, not a library. Programmatic consumption goes through:

1. **The `gc` CLI** (subprocess + JSON output where supported).
2. **The HTTP API** (`gc supervisor run` hosts it on `[api] port = 9443` by default).
3. **The generated Go and TypeScript clients** under `internal/api/genclient/` and `cmd/gc/dashboard/web/src/generated/`.

The API is OpenAPI 3.1 generated by Huma (the Go API framework). The single normative spec lives at `docs/schema/openapi.json` (downloadable). Endpoint families:

- Cities, agents, beads, sessions, mail, convoys, orders, formulas, molecules, participants, transcripts, adapters, events, config, packs.
- SSE streams for agent output, session output, events.
- Async operations (city create, session create/message/submit) return `202 Accepted` with `{request_id, event_cursor}` and complete via a `request.result.*` event.

Error responses are RFC 9457 Problem Details with `code:` prefixes on `detail` for semantic dispatch.

---

## 14. Pack Ecosystem

### Bundled Packs

`internal/builtinpacks/registry.go:45-54` enumerates the five packs embedded in the `gc` binary:

| Pack | Path | Purpose |
|---|---|---|
| `core` | `internal/bootstrap/packs/core` | System formulas, prompts, hooks, orders. The foundational always-loaded pack. |
| `bd` | `examples/bd` | Default bd-backed beads setup. |
| `dolt` | `examples/dolt` | Dolt-backed beads variant. |
| `maintenance` | `examples/gastown/packs/maintenance` | System-maintenance agent (`dog`) used by example cities. |
| `gastown` | `examples/gastown/packs/gastown` | The Gas Town role taxonomy as a pack: mayor, deacon, witness, refinery, polecat, crew, dog, boot. |

The `core` pack ships with formulas (`mol-do-work`, `mol-polecat-work`, `mol-polecat-commit`, `mol-polecat-base`, `mol-scoped-work`, `mol-prompt-synth`, `mol-review-quorum`), orders (`beads-health`), skills (`gc-mail`, `gc-rigs`, `gc-work`), and overlay files.

The bundled packs resolve to embedded content; in `pack.toml` they look like normal git-backed imports (`source = "github.com/gastownhall/gascity//examples/gastown/packs/gastown"`) but Gas City resolves them in-process without a network round-trip.

### Pack Extension Model

External packs are git repos with a `pack.toml` plus the conventional directories (`agents/`, `formulas/`, `orders/`, etc.). `gc import add <source> [--version V]` registers an import; `gc import install` materializes it under `.gc/imports/` and locks the commit in `packs.lock`. `gc import upgrade` advances versions within constraints. `gc import why` explains why an import is present.

There's also a legacy V1 path (`[packs.<name>]` with explicit git URL/ref/path + `gc pack fetch`) that's preserved for migration compatibility.

### Example Cities

`examples/` contains worked-example cities:

| Example | Purpose |
|---|---|
| `gastown` | The full Gas Town role taxonomy (mayor/polecat/witness/refinery/deacon/crew/dog). |
| `swarm` | Multi-agent fanout. |
| `hyperscale` | Scale-stress configuration. |
| `lifecycle` | Session lifecycle exploration. |
| `bd`, `dolt` | Beads provider variants. |

`examples/gastown/city.toml` is the canonical "everything-on" example.

---

## 15. What's NOT in Gas City but IS in Gas Town

This is the **crucial primitive-vs-application split**. From `docs/getting-started/coming-from-gastown.md`:

| Gas Town role | In Gas City? | Where it lives |
|---|---|---|
| **Mayor** | Not in Go | `examples/gastown/packs/gastown/agents/mayor/` — a pack agent |
| **Deacon** | Not in Go | Pack agent, plus the controller absorbs its watchdog/order-dispatch logic |
| **Witness** | Not in Go | Pack agent (lifecycle behaviors built from waits+formulas+session scale) |
| **Refinery** | Not in Go | Pack agent |
| **Polecat** | Not in Go | Pack agent (operating-mode convention, not a type) |
| **Crew** | Not in Go | Pack-level convention (persistent named agents) |
| **Dog** | Not in Go | Mostly absorbed as `exec` orders; some scalable agent configs |
| **Boot** | Not in Go | Pack agent |
| **Wasteland** | Not in Go | Operational pattern; not a primitive |

The hard rule from `AGENTS.md:7-9`:

> **ZERO hardcoded roles.** The SDK has no built-in Mayor, Deacon, Polecat, or any other role. If a line of Go references a specific role name, it's a bug.

What Gas City has in lieu of role types:

- Agents are **generic**, with identity from config (`name`, `dir`, `provider`).
- Behavior comes from `prompt.template.md` (rendered Go `text/template` Markdown).
- "Roles" are configuration conventions: persistent named sessions = crew, scalable on-demand sessions = polecats.
- "Plugins" are **orders** (exec or formula).
- "Convoys" stay as a bead-shaped grouping primitive, not a runtime layer.
- "Worktrees" are pack scripts that call `git worktree` from `pre_start`, not an SDK concept.

The translation table in `coming-from-gastown.md:48-62` is the most precise statement of the mapping, and it's worth reading verbatim if porting a Town concept.

---

## 16. Versioning and Release Maturity

### Status

- **`v1.0.0`** released **2026-04-21** — the first stable release (`CHANGELOG.md:138-142`):

  > First stable release. Between `v0.15.1` and `v1.0.0` the project received 610 commits across 1,273 files (+303,902 / −46,437) from the core team and 12 community contributors.

- Currently on `main` past `v1.0.0`, working on a substantial `[Unreleased]` section (~50 line items). The HEAD commit at analysis time is `183897e Adopt PR #2388: attribute supervisor shutdown triggers (#2415)`.

- Local clone shows `git tag` returns nothing — the project uses GitHub releases for tagging rather than local annotated tags.

### Evolution Velocity

The `engdocs/archive/` directory (`engdocs/archive/backlogs/k8s-backlog.md`, `mail-roadmap.md`, `scaling-backlog.md`, `startup-roadmap.md`, `telemetry-roadmap.md`, `worktree-roadmap.md`, `tutorial-progression.md`) is a substantial archive of past pivots and roadmaps, indicating active design-thinking churn.

`engdocs/design/` contains in-flight design docs (24+ documents) including the still-in-progress **PackV2 rollout** (the `packv2/` subdir has its own `skew-analysis.md` and `doc-consistency-audit.md`), the **session-first migration** (completed `dd90ac0a` Mar 8 2026), the in-progress **worker boundary** migration (started `12a0a848` Apr 17 2026), and design notes for **two-minute CI Blacksmith** and **worker-conformance** that remain `Proposed`.

`AGENTS.md:138-164` documents two **active migrations** that are CI-enforced:

1. **Worker boundary**: production `cmd/gc/*.go` files must route session creation through `internal/worker.Handle` — enforced by `TestGCNonTestFilesStayOnWorkerBoundary`.
2. **Session-first**: the former `agent.Agent`/`agent.Handle` interfaces were removed; lifecycle moved to `internal/session/` and providers to `internal/runtime/`. Do not reconstruct the old surfaces.

### Stability Promises

After `v1.0.0` the public surface is meant to be stable, but:

- The Go library API is still explicitly internal (`pkg/` doesn't exist yet).
- The HTTP API is OpenAPI-versioned at `/v0/` — still a major-zero scheme.
- Pack schema is `schema = 2` (PackV2); the migration shim for `schema = 1` is still active but deprecated.
- The formula file naming (`*.formula.toml` / `*.order.toml` infix) is acknowledged as transitional and tracked for removal under [#586](https://github.com/gastownhall/gascity/issues/586).

So Gas City should be treated as a young, opinionated, post-1.0 SDK whose surface is broadly stable but whose internals are still moving.

---

## 17. Notable Design Decisions, Idioms, and Quotes

### The Design Mantras

`AGENTS.md:192-219` lists the principles. The four most load-bearing:

> **Zero Framework Cognition (ZFC)** — Go handles transport, not reasoning. If a line of Go contains a judgment call, it's a violation. The ZFC test: does any line of Go contain a judgment call? An `if stuck then restart` is framework intelligence. Move the decision to the prompt.

> **Bitter Lesson** — every primitive must become MORE useful as models improve, not less. Don't build heuristics or decision trees.

> **GUPP** — "If you find work on your hook, YOU RUN IT." No confirmation, no waiting. The hook having work IS the assignment. This is rendered into agent prompts via templates, not enforced by Go code.

> **Nondeterministic Idempotence (NDI)** — the system converges to correct outcomes because work (beads), hooks, and molecules are all persistent. Sessions come and go; the work survives. Multiple independent observers check the same state idempotently. Redundancy is the reliability mechanism.

The "no status files — query live state" principle (§8) is the operational analog.

### Permanent Exclusions

`AGENTS.md:221-229` lists things that will **never** be added — each fails the Bitter Lesson test:

- No skills system (the model IS the skill system)
- No capability flags (a sentence in the prompt is sufficient)
- No MCP/tool registration (if a tool has a CLI, the agent uses it)
- No decision logic in Go (the agent decides from prompt and reality)
- No hardcoded role names (roles are pure configuration)

(Skills and MCP do appear in pack directories — but only as catalogs the agent can read, not as registries the SDK enforces.)

### Code Idioms

- **`cobra` for CLI**, **`BurntSushi/toml`** for config (`AGENTS.md:236`).
- **Unit tests next to code** (`config.go` → `config_test.go`); integration tests use `//go:build integration`.
- **Atomic file writes**: write to temp file → `os.Rename` (used pervasively by FileStore).
- **No panics in library code** — return errors.
- **Error messages include context**: `fmt.Errorf("adding rig %q: %w", name, err)`.
- **No `tmux kill-server`** as cleanup — target the city's socket explicitly.
- **`t.TempDir()`** for filesystem tests.
- **Conformance suites** for pluggable interfaces. Both the bead Store and the events Provider have conformance test runners (`internal/beads/beadstest/conformance.go`, `internal/events/eventstest/conformance.go`) that exercise every implementation against the same invariants.
- **Field-sync reflection tests**: `TestAgentFieldSync` enforces that any field on `config.Agent` also appears on `AgentPatch` and `AgentOverride`. Apply functions and `poolAgents` deep-copy must be checked manually.

### Test Scaffolding

- `internal/testenv` — shared test environment (referenced by `testenv_import_test.go` in every package as a compile-time assertion).
- `internal/testfixtures` — golden test data.
- `internal/testutil` — common helpers.
- `internal/formulatest` — formula-specific helpers.
- `internal/runtime/runtimetest/conformance.go` — runtime provider conformance.
- `internal/beads/beadstest/conformance.go` — bead store conformance.
- `internal/events/eventstest/conformance.go` — events provider conformance.
- `internal/mail/mailtest/` — mail provider helpers.

### Architectural Boundary Tests

Several tests enforce architectural invariants at CI time:

- `TestNoBdExecOutsideBeads` — no Go code outside `internal/beads/` may invoke `bd`.
- `TestGCNonTestFilesStayOnWorkerBoundary` — `cmd/gc` production code must route session creation through `internal/worker`.
- `TestOpenAPISpecInSync` — generated OpenAPI must match committed `internal/api/openapi.json`.
- `TestEveryKnownEventTypeHasRegisteredPayload` — every event type constant must have a registered payload sample.
- `TestAgentFieldSync` — `Agent`/`AgentPatch`/`AgentOverride` must stay structurally identical.

### Document Discipline

`engdocs/architecture/index.md:71-79` formalizes four document types:

| Type | Directory | Purpose | Lifecycle |
|---|---|---|---|
| Architecture doc | `engdocs/architecture/` | How it works now | Living; update when code changes |
| Design doc | `engdocs/design/` | How we want it to work | Proposal → Accepted → Implemented → Obsolete |
| Reference doc | `docs/reference/` | Exhaustive lookup | Must stay in sync; partially generated |
| Tutorial | `docs/tutorials/` | Learning path | Ordered progression |

Each architecture doc has a "Last verified against code: YYYY-MM-DD" header that tracks last drift check.

---

## 18. Open Questions and Pitfalls

### Acknowledged Limitations

- **No cascading restarts** (Health Patrol implements only `one_for_one`). No `depends_on` for cross-agent failure cascades.
- **Crash tracker is in-memory only**. Controller restart clears quarantine state. Intentional, but operators are surprised.
- **No retry on order dispatch failure**. Tracking bead prevents re-fire until cooldown opens.
- **`FileRecorder.Watch` uses 250ms polling**, not inotify. Adds latency, uses CPU.
- **No event retention/rotation**. `.gc/events.jsonl` grows without bound. `events.rotated` is emitted on manual rotation but there is no policy engine.
- **Sling command is shell-exec'd**. Every dispatch forks a shell process. Simple but slow at scale.
- **Container expansion is serial**. A slow sling for one child blocks subsequent children in the same convoy.
- **No built-in pool load balancing**. Sling routes to the pool label; pool members compete for work via `work_query` first-come-first-served.
- **Pool check commands can stall the tick** — `wg.Wait()` blocks reconciliation. No per-check timeout.
- **Unix socket has no authentication**. File permissions are the only ACL.
- **Tracker state is in-memory only**. Crash history, idle timestamps, and order dispatch state all reset on controller restart.
- **No hot-reload for structural changes**. `workspace.name` changes require a full controller restart.
- **MemStore.SetMetadata is a no-op**. MemStore has no metadata storage; verifies existence only.
- **BdStore.Children is client-side filtered** because `bd` lacks a parent-child query.
- **BdStore timestamps are second-precision** (Dolt limitation).
- **Pack content hot-reload is partial**. `Revision()` re-hashes pack contents on config change, but new files added outside the watched directories require manual reload.
- **Hosted/operator multi-user trust model is not yet articulated** beyond "trust the operator who started the supervisor."
- **`agent_defaults` tombstones**: several fields (`skills`, `mcp`, `model`, `wake_mode`, `allow_overlay`, `allow_env_override`) are parsed but **not yet inherited automatically at runtime** (`docs/reference/config.md:117-131`). This is a known migration tail.
- **dx-review is a future consumer for review-quorum's durable contract; the formula's synthesis step is still agent-executed** and doesn't call `reviewquorum.Finalize` directly yet.

### Active Tension: Pack Naming

- Formula files use the `.formula.toml` infix and order files use the `.order.toml` infix. The infix is acknowledged to be transitional and tracked in [#586](https://github.com/gastownhall/gascity/issues/586) for removal "after the merge."
- PackV1 (`workspace.includes`, `[packs.*]`, `[[agent]]`, `[formulas].dir`) is still loadable but officially deprecated. The migration shim is `gc doctor --fix`.

### Open Architectural Questions

- **What does "the controller drives all SDK infrastructure" mean for a hosted multi-tenant Gas City?** Today the supervisor is single-machine. Multi-tenant K8s setups exist (`internal/runtime/k8s`) but the supervisor model itself is single-machine.
- **Is the HTTP API the right embedding surface or will there eventually be a Go library?** `AGENTS.md` flags this as deliberate ("SDK exports (`pkg/`) are future work").
- **How do convergence loops compose?** `CountActiveConvergenceLoops(targetAgent)` exists (used for nested-convergence prevention), but the composition story across rigs and across formulas isn't fully fleshed out yet.
- **The dispatch DAG (graph.v2) story is still evolving.** `internal/dispatch/` and `internal/graphroute/` provide workflow execution / fanout, but the relationship between `gc convoy control --serve` (control-dispatcher loop) and the legacy convoy lifecycle is a moving target. The `mol-review-quorum` formula is described as a `graph.v2` formula.

### Pitfalls When Composing on Top

- **Don't write status files**. Use live process queries (`runtime.Provider.IsRunning()`).
- **Don't add a Go file referencing a role name**. Use config-driven dispatch.
- **Don't bypass the worker boundary** in `cmd/gc/` production code (CI-enforced).
- **Don't run `bd` from outside `internal/beads/`** (CI-enforced).
- **Don't add a Go judgment call.** Move the decision to a prompt template.
- **Don't add hand-written JSON to the HTTP wire.** All API endpoints are Huma-registered; OpenAPI is generated.
- **Don't add a new primitive without the primitive test** (Atomicity + Bitter Lesson + ZFC).

---

## 19. Quick-Reference Appendix

### One-Page Mental Model

```
A city is a directory with:
  pack.toml       (definition)
  city.toml       (deployment)
  .gc/            (site binding + runtime state)

A bead is a row in a store (anything trackable: tasks, mail, molecules, convoys).
An agent is a session running a configured LLM provider with a prompt template.
A pool is an elastic group of agents sharing a work label.
A rig is an external project with its own bead prefix, sharing the city's Dolt.

A formula is a TOML workflow DAG.
A molecule is a formula instantiated as beads.
A wisp is an ephemeral molecule with a TTL.
A convoy is a container bead grouping related child beads.

An order is "when X then run Y" — a trigger paired with a formula or exec.
A convergence loop is "iterate formula F until gate G passes or N tries."

Sling routes work to an agent or pool, optionally instantiating a wisp from a formula.
Mail is a durable message bead.
Nudge is fire-and-forget text into a session.
A wait is a durable pause bead.
A handoff is mail + restart-request.

The controller reconciles desired (config) → running (process tree) every 30s.
The supervisor is a machine-wide host of one controller per registered city.
The event bus is an append-only JSONL log of every state change.
```

### Five-Primitive Interface Cheat Sheet

```go
// Session — internal/runtime/runtime.go
type Provider interface {
    Start, Stop, Interrupt, IsRunning, Attach, Nudge,
    SetMeta, GetMeta, Peek, ListRunning, GetLastActivity, ...
}

// Beads — internal/beads/beads.go
type Store interface {
    Create, Get, Update, Close, List, Ready,
    Children, ListByLabel, SetMetadata, MolCook
}

// Events — internal/events/events.go
type Provider interface {
    Record(Event)               // best-effort
    List(Filter), LatestSeq, Watch, Close
}

// Config — internal/config/compose.go
LoadWithIncludes(fs, path) (*City, *Provenance, error)

// Prompt Templates — Go text/template in Markdown
// rendered by cmd/gc/prompt.go:renderPrompt()
```

### Four Derived Mechanism Entry Points

```go
// Messaging — internal/mail
type Provider interface {
    Send, Inbox, Get, Read, MarkRead, MarkUnread,
    Archive, Delete, Check, Reply, Thread, Count
}

// Formulas — internal/formula + store.MolCook
// Molecules — store.MolCook(formula, title, vars) → rootID

// Dispatch — internal/sling.DoSling / DoSlingBatch

// Health Patrol — cmd/gc/controller.go:controllerLoop
//   + cmd/gc/session_reconciler.go:reconcileSessionBeads
//   + crash_tracker / idle_tracker / wisp_gc / order_dispatch
```

---

## Closing Summary

Gas City is the **infrastructure layer extracted from Gas Town**: a Go SDK that provides session lifecycle, work persistence, event streams, declarative config, and prompt templates as primitives, and composes them into messaging, formulas/molecules, dispatch (sling), and health patrol as the four derived mechanisms. It enforces a strict separation between SDK infrastructure (Go code, zero roles) and application orchestration (TOML config + Markdown prompts inside packs). It is reconciler-driven (Kubernetes-style desired-state convergence, Erlang/OTP supervision semantics), bead-graph-persisted (Yegge's `bd` + Dolt as the default), and runtime-pluggable (tmux/subprocess/exec/ACP/k8s providers behind a single interface). Its convergence-loop primitive provides bounded iterative refinement with pluggable gates, structurally similar to Attractor DOT pipelines. The CLI surface is large (45+ top-level subcommands) but every subcommand is a projection of the same typed object model that also drives a generated OpenAPI 3.1 HTTP+SSE control plane. The system is post-1.0 but still rapidly evolving — PackV2 is the current schema, the worker boundary migration is in-flight, and several `[agent_defaults]` fields exist as parsed-but-not-yet-applied tombstones.

The deepest commitment is the one stated by `AGENTS.md`: **"If a line of Go references a specific role name, it's a bug."** Every other architectural choice flows from that.
