# Gas Town — Deep Architecture and Capabilities Reference

**Audience:** future AI sessions, contributors, and engineers who need to understand Gas Town well enough to operate, extend, or treat it as the canonical runtime substrate for another software-factory discipline (StrongDM Dark Factory, Every.to Compound Engineering, the parent project's four candidate architectures, etc.).

**Provenance:** Authored 2026-05-20 by a Claude Code subagent against a fresh clone of `https://github.com/gastownhall/gastown` (read-only walk; ~30 MB, ~1,500 files). Every architectural claim cites a specific file path inside the cloned tree so future sessions can verify and extend. Note: the canonical org is `gastownhall`, not `steveyegge` — older docs and El Kaim's "Dark Factory" essay still point at the old URL; both resolve to the same repository, but the `gastownhall` form is current.

**Companion documents:**

- `research/followup/13-gas-city-deep-dive.md` — sibling deep-dive on Gas City, the SDK Gas Town's reusable infrastructure was extracted into.
- `research/38-gas-systems-substrate.md` — synthesis report: how Gas City + Gas Town map to StrongDM Dark Factory and Every.to Compound Engineering, with concrete deployment sketches.
- `research/followup/04-gastown-beads.md` — earlier (Round-3) comparison report from before the deep walk; this document supersedes it on internal-package structure and design-doc coverage, and reaches additional subsystems (Boot, Dogs, `gt feed`, `gt seance`, proxy server, OTEL data model, `gt-model-eval/`, CHANGELOG architectural milestones).

---

## 0. Orientation

Reference compiled from a read-only walk of the repository at `https://github.com/gastownhall/gastown` (canonical org). Citations are file paths inside the cloned tree.

---

## 1. Mission and Positioning

Gas Town is a Go binary (`gt`) that builds a **workspace operating system**
on top of git worktrees, tmux sessions, and a Dolt SQL server holding a
persistent issue-graph (Beads / `bd`). Its self-description is
"workspace manager that lets you coordinate multiple AI coding agents
… working on different tasks" (`README.md:7`).

The load-bearing scale claim is in the "What Problem Does This Solve"
table (`README.md:9-17`):

| Challenge                       | Gas Town Solution                            |
| ------------------------------- | -------------------------------------------- |
| Agents lose context on restart  | Work persists in git-backed hooks            |
| Manual agent coordination       | Built-in mailboxes, identities, and handoffs |
| 4-10 agents become chaotic      | Scale comfortably to 20-30 agents            |
| Work state lost in agent memory | Work state stored in Beads ledger            |

Where Attractor / Kilroy / Mammoth / Smasher / Tracker are
**pipeline runners** (they execute DOT pipelines once and exit), Gas Town
is a **persistent fleet manager** for sessions. The unit of work is not
a pipeline run, it's a long-lived multi-agent town whose members come and
go but whose ledger and identities persist. Two ideas in the README and
`docs/overview.md:5-19` make the framing explicit:

1. *Work is structured data, not just tickets.* Every action is attributed,
   every agent has a CV, every piece of work has provenance (`docs/why-these-features.md:21-27`).
2. *Sessions are pistons, agents are pistons firing — the steam engine
   metaphor.* Throughput depends on agents finding work and firing
   immediately ("GUPP" — Gas Town Universal Propulsion Principle —
   `docs/glossary.md:10-12`, `docs/concepts/propulsion-principle.md:3-7`).

Gas Town is also the source repo for **Gas City** — a forward-looking
"provider contract" (`docs/agent-provider-integration.md:539-608`) that
formalises the implicit tmux-shim interface into an explicit
`AgentProvider` Go interface. The relevant note: "Gas Town is being
succeeded by Gas City, which formalises the implicit provider interface
into an explicit contract." Gas Town is the runtime; Gas City is intended
to be the SDK.

### El Kaim's five design principles

The README and `docs/why-these-features.md:253-262` state the same five
principles, verbatim from "Design Philosophy":

1. **Attribution is not optional.** Every action has an actor.
2. **Work is data.** Not just tickets — structured, queryable data.
3. **History matters.** Track records determine trust.
4. **Scale is assumed.** Multi-repo, multi-agent, multi-org from day one.
5. **Verification over trust.** Quality gates are first-class primitives.

These principles drive every architectural choice from `BD_ACTOR` env-var
plumbing (`docs/concepts/identity.md:90-109`) to the merge queue's
verification-before-merge gates (`docs/design/architecture.md:206-237`).

---

## 2. The Role Taxonomy in Full

There are nine first-class roles. They divide along two axes — town-level
vs rig-level, and worker vs supervisor. All role definitions live as
"role beads" with `hq-*-role` IDs (`docs/design/architecture.md:48-58`):

| Role        | Scope      | Lifecycle             | Bead ID                          | Process kind                |
|-------------|------------|-----------------------|----------------------------------|-----------------------------|
| **Mayor**   | town       | persistent, singleton | `hq-mayor` (role `hq-mayor-role`)| AI session in tmux          |
| **Deacon**  | town       | persistent, singleton | `hq-deacon`                      | AI session in tmux          |
| **Boot**    | town       | ephemeral per-tick    | `hq-boot`                        | AI session, fresh each tick |
| **Dogs**    | town       | ephemeral / per-task  | `hq-dog-<name>`                  | mostly Go, some AI          |
| **Witness** | rig        | persistent per-rig    | `<prefix>-<rig>-witness`         | AI session in tmux          |
| **Refinery**| rig        | persistent per-rig    | `<prefix>-<rig>-refinery`        | AI session + Go merge engine|
| **Polecat** | rig        | persistent identity, ephemeral session | `<prefix>-<rig>-polecat-<name>` | AI session, ephemeral worktree |
| **Crew**    | rig        | persistent (human-managed) | `<prefix>-<rig>-crew-<name>` | full clone, human-driven    |
| **Overseer**| human      | the human owner       | n/a — derived from `GIT_AUTHOR_EMAIL` | human                |

Beyond these there are three additional infrastructure entities that are
not "roles" per se but appear in the design docs:

- **Scheduler** — Go process inside the daemon that does capacity-controlled
  dispatch (`docs/design/scheduler.md`).
- **Seance** — a CLI tool, not a daemon, that lets an agent talk to its
  predecessor sessions (`internal/cmd/seance.go`).
- **Daemon** — `gt daemon`, the Go heartbeat process that owns the Dolt
  server lifecycle and runs Boot every 3 minutes
  (`docs/design/dog-infrastructure.md:67-91`).

### 2.1 Mayor

The Mayor is the global coordinator (`docs/overview.md:28-31`). It is a
Claude Code session running in tmux, attached via `gt mayor attach`. It
lives in `~/gt/mayor/` (`docs/design/architecture.md:97-105`) which holds
`town.json`, `rigs.json`, `daemon.json`, and `accounts.json` — the
authoritative configuration for the entire town. Its bead is `hq-mayor`
in the town-level beads database. The Mayor doesn't implement work
directly; it creates convoys, slings beads, and orchestrates other agents
(`README.md:48-50`).

### 2.2 Deacon

The Deacon is the cross-rig supervisor daemon (`docs/glossary.md:30-32`):
"Daemon beacon running continuous Patrol cycles … the system's watchdog."
It is implemented as a long-running AI session in `~/gt/deacon/`. It
writes a freshness heartbeat to `~/gt/deacon/heartbeat.json` on every
patrol cycle (`docs/design/dog-infrastructure.md:84-96`), and the daemon
treats anything older than 15 minutes as "very stale" and prompts a wake.

The Deacon's job is conceptually simple — observe witness health, dispatch
Dogs for maintenance, run `gt escalate stale` to catch unacked
escalations — but the implementation is intricate because the Deacon is
itself an AI session that can get stuck. The chain of accountability is:

```
Daemon (Go process)          <- 3-min heartbeat, can't reason
    |
    +-> Boot (AI agent)       <- intelligent triage, fresh each tick
            |
            +-> Deacon (AI agent)  <- continuous patrol, long-running
                    |
                    +-> Witnesses & Refineries  <- per-rig agents
```
Source: `docs/design/dog-infrastructure.md:7-17`.

### 2.3 Boot — the Dog that watches the Deacon

Boot is the single most distinctive role in Gas Town and the one the
prior research report doesn't fully cover. It exists because the daemon
**can't reason** about whether the Deacon is genuinely stuck or merely
thinking hard, and the Deacon **can't observe itself**
(`docs/design/dog-infrastructure.md:23-54`).

Boot is a narrow, ephemeral AI agent that:

- Runs fresh each daemon tick (no accumulated context debt).
- Makes a single decision: should Deacon wake?
- Exits immediately after deciding.

Boot's decision matrix is captured at
`docs/design/dog-infrastructure.md:108-118`:

| Condition                         | Action  | Command                                          |
| --------------------------------- | ------- | ------------------------------------------------ |
| Session dead                      | START   | Exit; daemon calls `ensureDeaconRunning()`       |
| Heartbeat > 15 min                | WAKE    | `gt nudge deacon "Boot wake: check your inbox"`  |
| Heartbeat 5-15 min + pending mail | NUDGE   | `gt nudge deacon "Boot check-in: pending work"`  |
| Heartbeat fresh                   | NOTHING | Exit silently                                    |

Boot uses a marker file (`~/gt/deacon/dogs/boot/.boot-running`, 5-min
TTL) to prevent double-spawning. Boot lives at the bead `hq-boot` and in
the directory `~/gt/deacon/dogs/boot/`. When tmux is unavailable, Boot
degrades to mechanical Go thresholds (`docs/design/dog-infrastructure.md:162-176`).

### 2.4 Dogs

Dogs are the Deacon's helpers (`docs/overview.md:97-111`). The repo
explicitly insists: "**Dogs are NOT workers.** This is a common
misconception." Dogs do infrastructure / maintenance tasks. There are
two execution models (`docs/design/dog-execution-model.md`):

1. **Imperative Go dogs** (reliability-critical) — Doctor (466 LOC),
   Reaper (658 LOC), Compactor, JSONL Backup, Dolt Backup. These run
   from the daemon heartbeat and have no agent dependency.
2. **Plugin-dispatched dogs** (opportunistic) — agents that interpret a
   `plugin.md` formula. Most current "AI dogs" run as plugins (e.g.
   `compactor-dog`, `stuck-agent-dog`, `quality-review`).

There is also a `internal/dog/` package distinct from the plugin model
that manages a fixed pool of 5 "dance dogs" — lightweight goroutines
that execute the shutdown-dance state machine (`WARRANT →
INTERROGATE → EVALUATE → PARDON|EXECUTE`) when a session must be killed.
The pool design lives at `docs/design/dog-infrastructure.md:188-296`:

```go
const (
    DefaultPoolSize = 5
    MaxPoolSize     = 20
)
type DogPool struct {
    mu       sync.Mutex
    dogs     []*Dog
    idle     chan *Dog
    active   map[string]*Dog
    stateDir string  // ~/gt/deacon/dogs/active/
}
```

The dance state machine has three interrogation attempts with timeouts
of 60s, 120s, and 240s (`docs/design/dog-infrastructure.md:348-353`).

### 2.5 Witness

The Witness is the per-rig polecat lifecycle manager
(`docs/design/witness-at-team-lead.md` and `docs/design/polecat-lifecycle-patrol.md`).
It lives at `<rig>/witness/` and has no clone of its own — only a
home directory and a beads redirect. Its job is to:

- Process its inbox (POLECAT_DONE, MERGE_FAILED, RECOVERED_BEAD…).
- Detect zombie polecats (`witness/handlers.go: DetectZombiePolecats`).
- Detect orphaned beads (in-progress with no live polecat).
- Forward `MERGE_READY` to the Refinery after verifying clean state.
- Mountain-eat large convoys (`internal/witness/mountain.go`).

A planned but unimplemented architecture in `witness-at-team-lead.md`
would convert the Witness into a Claude Code "Agent Teams" (AT) team
lead in `permissionMode: delegate`. In that future, the Witness
literally cannot edit files — coordination-only is enforced
structurally. Today the Witness uses a tmux-based session manager and
gets all mail/nudge primitives.

### 2.6 Refinery

The Refinery is the per-rig merge queue processor (`internal/refinery/`,
~9 source files). It runs as both a Go merge engine and a long-running
AI session (`internal/refinery/engineer.go`). It implements a
**Bors-style batch-then-bisect merge queue**
(`docs/design/architecture.md:206-237`):

```
MRs waiting:  [A, B, C, D]
                    ↓
Batch:        Rebase A..D as a stack on main
                    ↓
Test tip:     Run tests on D (tip of stack)
                    ↓
If PASS:      Fast-forward merge all 4 → done
If FAIL:      Binary bisect → test B (midpoint)
              If B passes: C or D broke it → bisect [C,D]
              If B fails:  A or B broke it → bisect [A,B]
```

Three merge strategies are configurable (added in v0.7.0):
`direct`, `mr` (uses `gh pr merge`), `local`. The Refinery also runs
`internal/refinery/score.go` for quality scoring and emits
`quality-review-result` wisps consumed by the `quality-review` plugin.

### 2.7 Polecat

Polecats are the workers (`docs/concepts/polecat-lifecycle.md`). The key
distinction made repeatedly in the docs is the **three-layer model**
(`docs/concepts/polecat-lifecycle.md:96-101`):

| Layer        | Component                  | Lifecycle           | Persistence                              |
| ------------ | -------------------------- | ------------------- | ---------------------------------------- |
| **Identity** | Agent bead, CV chain, work history | Permanent  | Never dies                                |
| **Sandbox**  | Git worktree, branch       | Persistent across assignments | Created once, reused; branch repaired |
| **Session**  | Claude (tmux pane), context window | Ephemeral per step | Cycles per step/handoff             |

Polecats run in `<rig>/polecats/<name>/` worktrees, based on
`mayor/rig/` (`docs/design/architecture.md:120-129`). The four operating
states are `Working`, `Idle`, `Stalled`, `Zombie`. The healthy cycle is
`IDLE → WORKING → IDLE` — no `nuke` in the happy path.

### 2.8 Crew

Crew members are persistent, human-managed workspaces with full git
clones at `<rig>/crew/<name>/` (`docs/overview.md:71-93`). The key
contrast with polecats: crew "pushes to main directly" (modulo PR
flow) while polecats "work on branch, Refinery merges." Cleanup is
manual for crew, automatic for polecats.

### 2.9 Overseer

The Overseer is **the human user**. They receive escalations of severity
`HIGH` and `CRITICAL` via mail, email, and SMS (`docs/design/escalation.md:12-18`).
The overseer is not a session; they are identified by
`GIT_AUTHOR_EMAIL` (the global identity per `docs/concepts/identity.md:184-194`).

---

## 3. The State Model

Gas Town's state model is a layered hierarchy. Top to bottom:

| Term | Location | Definition |
|------|----------|------------|
| **Town** | `~/gt/` | The root workspace, e.g. `~/gt/` |
| **Rig**  | `~/gt/<rig>/` | Project container (NOT a git clone) wrapping one git repo |
| **Crew Member** | `<rig>/crew/<name>/` | Human workspace (full clone) |
| **Hook** | git worktree under polecat dir | Persistent work-state substrate (one per polecat) |
| **Convoy** | bead `hq-cv-*` | Cross-rig work-tracking unit |
| **Molecule** | wisp bead | A workflow instance (one root wisp, optionally sub-wisps) |
| **Wisp** | ephemeral bead | Per-step substate; destroyed after runs |
| **Formula** | TOML template | Source workflow definition embedded in the binary |

The directory tree (`docs/design/architecture.md:84-130`) is highly
specific:

```
~/gt/                           Town root
├── .beads/                     Town-level beads (hq-* prefix)
├── .dolt-data/                 Centralized Dolt data
│   ├── hq/                     Town beads database
│   └── <rig>/                  Per-rig databases
├── daemon/                     Daemon runtime state
├── deacon/                     Deacon workspace
│   └── dogs/<name>/            Dog working directories
├── mayor/
│   ├── town.json               Town configuration
│   ├── rigs.json               Rig registry
│   ├── daemon.json             Daemon patrol config
│   └── accounts.json           Claude Code account management
├── settings/                   Town-level settings
│   ├── config.json             Town settings
│   └── escalation.json         Escalation routes
├── directives/                 Town-level role directives (operator policy)
├── formula-overlays/           Town-level formula overlays
└── <rig>/                      Project container
    ├── config.json
    ├── directives/             Rig-level role directives
    ├── formula-overlays/       Rig-level overlays
    ├── mayor/rig/              Canonical clone (beads live here)
    ├── refinery/rig/           Worktree from mayor/rig
    ├── witness/                Witness home (no clone)
    ├── crew/<name>/            Human workspaces (full clones)
    └── polecats/<name>/<rigname>/  Worker worktrees from mayor/rig
```

Key non-obvious points:

- **Rig ≠ clone.** A "rig" is a container that holds one canonical bare
  clone at `mayor/rig/` plus worktrees for each polecat/refinery. Crew
  members get their own full clones in parallel.
- **Beads are redirected via `.beads/redirect`** (`docs/design/architecture.md:194-205`).
  Worktrees don't have their own beads DB; they point to the canonical
  one in `mayor/rig/.beads/`. `ResolveBeadsDir()` follows the redirect
  chain (max depth 3) with circular detection.
- **All beads writes land on `main`** (`docs/design/architecture.md:166-171`).
  Concurrency is managed through `BEGIN`/`DOLT_COMMIT`/`COMMIT` atomicity.
  Earlier per-polecat Dolt branches were removed in 0.8.0.
- **Wisps vs molecules**: a "root-only wisp" is one row that represents
  an entire workflow instance — agents read step text inline from the
  embedded formula at prime time. A "poured" molecule materializes each
  step as a sub-wisp with checkpoint recovery (`docs/concepts/molecules.md:18-26`).
  The root-only default cuts ~6,000 ephemeral rows/day to ~400.

The **Hook** specifically is "a special pinned Bead for each agent"
(`docs/glossary.md:69-71`). When work appears on your hook, GUPP says
you must run it. Mechanically the hook is a polecat's git worktree —
the work-state substrate — but logically it is the pinned bead that
governs the polecat's identity for the duration of an assignment
("propulsion principle", `docs/concepts/propulsion-principle.md`).

---

## 4. The Beads Integration

Beads (`bd`) is the persistent agent-task graph DB, stored in a single
Dolt SQL server per town (port 3307; `docs/design/dolt-storage.md:13-21`).

### 4.1 Bead IDs

The format is `<prefix>-<5-char-alphanum>`. Prefixes correspond to
two-level bead storage (`docs/design/architecture.md:6-46`):

| Level    | Location                         | Prefix         | Purpose                                  |
| -------- | -------------------------------- | -------------- | ---------------------------------------- |
| **Town** | `~/gt/.beads/`                   | `hq-*`         | Cross-rig coordination, Mayor mail       |
| **Rig**  | `<rig>/mayor/rig/.beads/`        | project prefix | Implementation work, MRs, project issues |

Examples: `hq-mayor`, `hq-cv-abc12` (convoy), `gt-abc12` (gastown rig),
`bd-x7k2m` (beads rig), `w-abc123` (wasteland wanted), `c-abc123`
(wasteland completion).

Routing is governed by `routes.jsonl` (`docs/design/architecture.md:179-193`):

```jsonl
{"prefix":"hq-","path":"."}
{"prefix":"gt-","path":"gastown/mayor/rig"}
{"prefix":"bd-","path":"beads/mayor/rig"}
```

### 4.2 Agent beads, role beads, work beads

Every agent has an agent bead (`docs/design/architecture.md:33-46`)
whose lifecycle tracks `hook_bead`, `agent_state`, `cleanup_status`.
Role beads are global templates with `hq-*-role` IDs that agent beads
reference via the `role_bead` field. The work itself (issues, tasks,
features) is a separate bead.

### 4.3 The six-stage data lifecycle

`docs/design/architecture.md:260-275` lays out the data-plane pipeline:

```
CREATE → LIVE → CLOSE → DECAY → COMPACT → FLATTEN
  │        │       │        │        │          │
  Dolt   active   done   DELETE   REBASE     SQUASH
  commit  work    bead    rows    commits    all history
                         >7-30d  together   to 1 commit
```

Stages 1-3 are agent-driven. Stages 4-6 are Dog-driven: `Reaper` does
DELETE (gt-at0i), `Compactor` does REBASE (gt-l8dc), `Doctor` does GC
(gt-emm4). All five reliability-critical dogs are imperative Go
(`docs/design/dog-execution-model.md:25-49`).

### 4.4 How `gt` calls `bd`

`gt` invokes `bd` as a subprocess for nearly every state operation
(`internal/beads/`). The proxy server even auto-discovers the safe
subcommand list by running `gt proxy-subcmds`
(`docs/proxy-server.md:129-139`). Default `bd` allowlist via the proxy
is `create, update, close, show, list, ready, dep, export, prime, stats,
blocked, doctor`.

---

## 5. CLI Surface

Gas Town's CLI is enormous — ~421 Go source files in `internal/cmd/`
(`ls internal/cmd | wc -l`). The cobra command tree has well over 250
distinct `Use:` clauses. The top-level commands worth knowing:

### 5.1 Workspace / install

| Command | Source | Purpose |
|---------|--------|---------|
| `gt install [path]` | `cmd/install.go` | Initialize a workspace at the given path |
| `gt up` | `cmd/up.go` | Bring up the daemon and core agents |
| `gt down` | | Tear down |
| `gt prime` | `cmd/prime.go` | Context recovery: emits role context + mail + hooked work for ingestion at session start |
| `gt config [subcommand]` | `cmd/config.go` | Town/rig settings (set/get/list) |
| `gt doctor` | `cmd/doctor.go` (and `internal/doctor/`) | Run health checks; auto-fix where safe |
| `gt upgrade` | | Migrate config files after binary upgrade |
| `gt version` | `cmd/version.go` | Display version |
| `gt vitals` | | Unified health dashboard |
| `gt maintain` | | One-command Dolt maintenance (flatten + gc) |

### 5.2 Rig / crew

| Command | Purpose |
|---------|---------|
| `gt rig add <name> <git-url>` | Add project |
| `gt rig list` / `gt rig remove` / `gt rig adopt` | Rig CRUD |
| `gt rig dock` / `gt rig park` / `gt rig undock` / `gt rig unpark` | Lifecycle of rig participation |
| `gt crew add <name> --rig <rig>` | Create crew workspace |
| `gt crew list` / `gt crew status` / `gt crew at <rig>` | Crew CRUD + cd helper |
| `gt crew start` / `gt crew cycle` | Session lifecycle |

### 5.3 Agent operations

| Command | Purpose |
|---------|---------|
| `gt agents` | List active agents |
| `gt sling <bead-or-formula> [target]` | Assign work to agent (the central dispatch primitive) |
| `gt unsling [bead-id] [target]` | Reverse a sling |
| `gt mayor attach` / `gt mayor start --agent auggie` | Run Mayor session |
| `gt witness <rig>` / `gt refinery <rig>` | Per-rig agent commands |
| `gt boot triage` / `gt boot <rig>` | Manual Boot run |
| `gt deacon pending` / `gt deacon redispatch <bead-id>` / `gt deacon feed-stranded` | Deacon ops |
| `gt polecat nuke <rig>/<polecat>` | Destroy a polecat (sandbox) |
| `gt hook [bead-id] [target]` | Read or assign work to a hook |
| `gt done` | (in-session) submit and self-clean |
| `gt handoff [bead-or-role]` | Cycle session, preserve sandbox + identity |
| `gt nudge <target> [message]` | Immediate, ephemeral message via tmux send-keys |
| `gt prime` | Reload full context |

### 5.4 Convoy / scheduler

| Command | Purpose |
|---------|---------|
| `gt convoy create <name> [issues...]` | Create convoy |
| `gt convoy add <id> <issue>...` / `gt convoy list` / `gt convoy show <id>` | Convoy CRUD |
| `gt convoy stage <epic-id \| convoy-id>` | Pre-flight DAG check (Kahn's algorithm) |
| `gt convoy launch <id>` | Launch a staged convoy |
| `gt convoy land <id>` | Finalize an owned convoy |
| `gt convoy stranded` | List convoys missing assigned polecats |
| `gt convoy mountain <epic-id>` | "Mountain mode" autonomous epic grinding |
| `gt scheduler status / list / run / pause / resume / clear` | Capacity-controlled dispatch ops |

### 5.5 Communication

| Command | Purpose |
|---------|---------|
| `gt mail inbox / read / send / archive / delete / mark-read / drain` | Durable agent mail |
| `gt mail group create / channel create / queue create` | Beads-native messaging primitives |
| `gt nudge <target> [message]` | Ephemeral message (no bead created) |
| `gt escalate -s <SEVERITY> "desc"` / `gt escalate list / ack / stale / close` | Severity-routed escalation |
| `gt seance [--talk <id>] [-p "question"]` | Resume + query a predecessor session |
| `gt broadcast <message>` | Town-wide broadcast |
| `gt callbacks` | Callback registry inspection |

### 5.6 Monitoring / dashboard

| Command | Purpose |
|---------|---------|
| `gt feed [--problems] [--since 1h]` | Real-time activity feed TUI |
| `gt dashboard [--port 3000] [--open]` | Web dashboard (htmx-driven) |
| `gt activity` | Plain-text event stream |
| `gt audit --actor=<bd_actor>` | Work history by agent |
| `gt agent-log <name>` | Agent log inspection |
| `gt logs` | Daemon/server logs |
| `gt status [target]` | Town/rig/agent status |
| `gt peek <rig/polecat> [count]` | Tmux pane preview |
| `gt vitals` | One-screen health summary |

### 5.7 Wasteland (federation)

| Command | Purpose |
|---------|---------|
| `gt wl join <upstream>` | One-time join |
| `gt wl browse` / `gt wl claim <id>` / `gt wl done <id> --evidence <url>` | Wanted-board interaction |
| `gt wl post --title "..."` | Post new wanted item |
| `gt wl sync` | Pull upstream changes |
| `gt wl stamp` / `gt wl stamps <rig>` / `gt wl charsheet <handle>` | Reputation stamps |
| `gt wl scorekeeper` | Internal scorekeeper |

### 5.8 Beads passthroughs and helpers

| Command | Purpose |
|---------|---------|
| `gt bead <bead-id>` / `gt cat <bead-id>` | Show bead in TUI |
| `gt mol attach / detach / dag / cook / pour / wisp` | Molecule ops (mostly delegating to `bd mol`) |
| `gt formula list / show / edit` | Formula management |
| `gt patrol [witness|deacon|refinery]` | Patrol cycle command |
| `gt reaper scan / databases` | Run wisp reaper manually |
| `gt compact` / `gt compact report` | Compaction ops |

### 5.9 Misc / advanced

| Command | Purpose |
|---------|---------|
| `gt account` / `gt accounts switch` | Claude Code account management |
| `gt costs record` / `gt costs` | Cost telemetry |
| `gt daemon start / stop / status` | Daemon control |
| `gt dolt start / stop / sql / status / pull` | Dolt server control |
| `gt feed-stranded` / `gt feed-stranded-state` | Auto-feed stranded convoys |
| `gt acp` | Agent Coordination Protocol proxy (see §7) |
| `gt proxy-subcmds` | Print the safe sub-command list for the proxy server |
| `gt theme [name]` | Tmux theme |
| `gt quota` | Quota management |
| `gt estop` | Emergency stop |
| `gt thaw` / `gt burn` | Recover / destroy resources |

This is a substantial CLI surface — substantially larger than what
prior comparison documents enumerate. The `internal/cmd` directory has
421 Go files and the cobra `Use` clauses include ~250 distinct
sub-commands as captured by `grep -hrE 'Use:\s+"[a-z]'`.

---

## 6. Agent Provider / Runtime Integration

`docs/agent-provider-integration.md` documents four integration tiers:

| Tier | Effort | What you get | What you provide |
| ---- | ------ | ------------ | ---------------- |
| 0 | Nothing | Basic tmux orchestration | A CLI that runs in a terminal |
| 1 | JSON config | Full lifecycle, resume, process detection | Preset entry in `agents.json` |
| 2 | Hooks | Context injection, tool guards, mail delivery | Hook installer function |
| 3 | Deep | Non-interactive, session forking, wrapper | Native API integration |

Built-in presets (from `README.md:416`): `claude`, `gemini`, `codex`,
`cursor`, `auggie`, `amp`, `opencode`, `copilot`, `pi`, `omp`.

The capability matrix at `docs/agent-provider-integration.md:524-535`:

| Agent | Hooks | Resume | Non-Interactive | Fork | Prompt Mode | Process Names |
| ----- | ----- | ------ | --------------- | ---- | ----------- | ------------- |
| Claude | Yes (settings.json) | `--resume` (flag) | Native | Yes | arg | node, claude |
| Gemini | Yes | `--resume` (flag) | `-p` | No | arg | gemini |
| Codex | No | `resume` (subcmd) | `exec` subcmd | No | none | codex |
| Cursor | Yes (`.cursor/hooks.json`) | `--resume` (flag) | `-p`/`--print` + `--output-format` | No | arg | cursor-agent, agent |
| Auggie | No | `--resume` (flag) | No | No | arg | auggie |
| AMP | No | `threads continue` (subcmd) | No | No | arg | amp |
| OpenCode | Yes (plugin JS) | No | `run` subcmd | No | none | opencode, node, bun |
| Copilot | Yes (`.github/hooks/gastown.json`) | `--resume` (flag) | n/a | No | arg | copilot |

Three hook delivery patterns exist (`docs/agent-provider-integration.md:268-414`):

- **Pattern A** — Claude-compatible `settings.json` with `SessionStart`,
  `PreCompact`, `UserPromptSubmit`, `PreToolUse`, `Stop` (Claude, Gemini).
- **Pattern B** — Plugin/script (OpenCode JS). The reference plugin at
  `/tmp/gastown/.opencode/plugins/gastown.js` shows `event.session.created`
  → `loadPrime('startup')`; `event.session.compacted` → `loadPrime('compact')`;
  `event.session.deleted` → `gt costs record --session <id>`.
- **Pattern C** — Informational instructions file (older Copilot;
  agents without executable hooks).

The hook commands are agent-agnostic (`gt prime --hook`, `gt mail check
--inject`, `gt nudge deacon session-started`). The fallback matrix
(`docs/agent-provider-integration.md:417-427`):

| Has hooks | Has prompt | Context source | Work instructions |
| --------- | ---------- | -------------- | ----------------- |
| Yes | Yes | Hook runs `gt prime` | In CLI prompt arg |
| Yes | No | Hook runs `gt prime` | Sent via nudge |
| No | Yes | "Run `gt prime`" in prompt | Delayed nudge |
| No | No | "Run `gt prime`" via nudge | Delayed nudge |

The environment variables Gas Town injects into every agent
(`docs/agent-provider-integration.md:783-794`):

```bash
GT_ROLE=gastown/crew/jack      # Agent's role
GT_RIG=gastown                 # Which rig
GT_ROOT=/Users/me/gt           # Town root
BD_ACTOR=gastown/crew/jack     # Beads identity
GIT_AUTHOR_NAME=gastown/crew/jack
GT_AGENT=kiro                  # Active preset
GT_SESSION_ID_ENV=KIRO_SESSION_ID
```

There is also an experimental **NOS Town** runtime
(`docs/runtimes/NOS_TOWN.md`) that wraps Gas Town with Groq-hosted open
models, multi-model routing, councils, and a Historian. Importantly,
NOS Town is NOT a fork — it imports `gastown` as a dependency, and
`kab0rn/gastown` tracks upstream via normal fork/sync.

---

## 7. Communication Primitives

Gas Town has six distinct communication channels (see
`docs/design/mail-protocol.md`):

| Channel | Persistence | Where it goes | Cost |
| ------- | ----------- | ------------- | ---- |
| **Mail** (`gt mail send`) | Durable bead in Dolt | Subject + body, addressed | High (commit) |
| **Nudge** (`gt nudge`) | Ephemeral | tmux send-keys appearing as `<system-reminder>` | Free |
| **Escalation** (`gt escalate`) | Durable bead + multi-channel | Severity-routed | High |
| **Seance** (`gt seance`) | Ephemeral | Spawns Claude subprocess against a predecessor session | One-shot |
| **Broadcast** (`gt broadcast`) | Either | Town-wide |  varies |
| **ACP** (Agent Coordination Protocol) | Stream proxy | wraps stdin/stdout of an agent | Process |

### 7.1 Mail vs nudge

The mail protocol doc (`docs/design/mail-protocol.md:365-395`) is
emphatic about a discipline rule:

> **Default to `gt nudge`. Only use `gt mail send` when the message
> MUST survive the recipient's session death.**

The litmus test: "If the recipient's session dies and restarts, do they
need this message?" If yes → mail. If no → nudge.

Mail subject prefixes encode protocol type
(`docs/design/mail-protocol.md:9-225`):

| Type | Route | Trigger | Handler |
|------|-------|---------|---------|
| `POLECAT_DONE <name>` | Polecat → Witness | `gt done` runs | Witness cleans up |
| `MERGE_READY <name>` | Witness → Refinery | Witness verifies clean | Refinery merges |
| `MERGED <name>` | Refinery → Witness | Successful merge | Witness acknowledges |
| `MERGE_FAILED <name>` | Refinery → Witness | Tests/build fail | Witness mails polecat |
| `REWORK_REQUEST <name>` | Refinery → Witness | Merge conflict | Witness asks polecat to rebase |
| `RECOVERED_BEAD <id>` | Witness → Deacon | Zombie + abandoned work | Deacon re-dispatches |
| `RECOVERY_NEEDED <name>` | Witness → Deacon | Dirty polecat needs manual work | Deacon coordinates |
| `HELP: <topic>` | Any → escalation target | Stuck/blocked | Escalation target intervenes |
| `🤝 HANDOFF: <context>` | Agent → self | `gt handoff` | Next session reads |

Each role has a mail budget (`docs/design/mail-protocol.md:397-405`):

| Role     | Mail Budget          | When to Mail | When to Nudge |
|----------|----------------------|--------------|---------------|
| Polecat  | 0-1 per session      | HELP/ESCALATE only | Everything else |
| Witness  | Protocol msgs only   | MERGE_READY, RECOVERED_BEAD, escalations | Polecat health checks |
| Refinery | Protocol msgs only   | MERGED, MERGE_FAILED, REWORK_REQUEST | Status updates |
| Deacon   | Escalations only     | Escalations to Mayor, HANDOFF to self | TIMER/HEALTH_CHECK |
| Dogs     | Zero                 | Never | Report via nudge |
| Mayor    | Strategic only       | Cross-rig coordination, HANDOFF | Instructions |

There are also three beads-native messaging primitives layered on top:
**Groups** (`gt:group`, bead ID `hq-group-<name>`), **Queues**
(`gt:queue`, `hq-q-<name>` for town-level, `gt-q-<name>` for rig),
and **Channels** (`gt:channel`, `hq-channel-<name>`) — see
`docs/design/mail-protocol.md:481-540`.

### 7.2 Seance — predecessor session discovery

`internal/cmd/seance.go` implements a unique primitive: spawning a
Claude subprocess that **resumes a predecessor session** so the current
agent can ask its predecessor questions. The discovery mechanism is the
`.events.jsonl` log written by SessionStart hooks. The CLI:

```bash
gt seance                       # List discoverable predecessor sessions
gt seance --talk <id> -p "Where did you put X?"  # One-shot question
```

Implementation: `claude --fork-session --resume <id>` (line 50 of
seance.go cites this). This loads the predecessor's full context
without modifying it. The session resume mechanism is governed by the
preset's `supports_fork_session: true` flag.

### 7.3 ACP — Agent Coordination Protocol

`internal/acp/` implements a stdin/stdout proxy
(`forward_from_agent.go`, `propulsion.go`, `keepalive_test.go`).
Mentions in the design docs are sparse; the package appears to be a
plumbing layer for agents whose runtimes export structured JSON
messages. The `gt acp` CLI command is in the cobra tree.

### 7.4 Escalation

`docs/design/escalation.md` defines a severity-routed escalation system.
Three severity levels and the default routes:

| Level | Priority | Default Route |
|-------|----------|---------------|
| **CRITICAL** | P0 | bead + mail + email + SMS |
| **HIGH** | P1 | bead + mail + email |
| **MEDIUM** | P2 | bead + mail mayor |

The escalation flow is Deacon → Mayor → Overseer
(`docs/design/escalation.md:21-31`). Each tier may resolve or forward;
the chain is recorded via bead comments. A `stale_threshold` (default
4h) triggers re-escalation that bumps severity (MEDIUM→HIGH→CRITICAL),
capped by `max_reescalations` (default 2). Configuration lives at
`~/gt/settings/escalation.json`.

The escalation bead labels are structured
(`docs/design/escalation.md:81-91`):

| Label | Values |
| ----- | ------ |
| `severity:<level>` | MEDIUM/HIGH/CRITICAL |
| `source:<type>:<name>` | `plugin:rebuild-gt`, `patrol:deacon` |
| `acknowledged:<bool>` | true/false |
| `reescalated:<bool>` | true/false |
| `reescalation_count:<n>` | 0, 1, 2 |
| `original_severity:<level>` | MEDIUM/HIGH |

---

## 8. Scheduler and Capacity Governance

The scheduler (`docs/design/scheduler.md`, `internal/scheduler/`)
provides back-pressure and concurrency control for `gt sling`. By
default (`scheduler.max_polecats = -1`) every sling dispatches
immediately. When set to a positive integer, sling creates a **sling
context bead** (`bd create --ephemeral` with label `gt:sling-context`)
and the daemon dispatches incrementally on each heartbeat tick (step 14).

### 8.1 Sling context beads

A key 0.9.0-era refactor (per `docs/design/scheduler.md:96-141`):
scheduling state lives on a separate ephemeral bead, NOT on the work
bead itself. The work bead is "pristine — no description mutation, no
label manipulation."

A sling context bead carries JSON fields:

| Field | Type | Notes |
|-------|------|-------|
| `version` | int | currently 1 |
| `work_bead_id` | string | the actual work being scheduled |
| `target_rig` | string | destination |
| `formula` | string | formula to apply (e.g. `mol-polecat-work`) |
| `args` / `vars` | string | natural-language instructions + key=value pairs |
| `merge` | string | `direct` / `mr` / `local` |
| `convoy` | string | parent convoy bead |
| `dispatch_failures` | int | circuit-breaker counter (threshold 3) |

State machine: `SCHEDULED → DISPATCHED | CIRCUIT-BROKEN | CLEARED`.
The circuit breaker closes the context after 3 failures
(`docs/design/scheduler.md:333-355`).

### 8.2 Dispatch counting

Active polecats are counted by scanning tmux sessions and matching role
via `session.ParseSessionName()` — this counts BOTH scheduler-dispatched
and directly-slung polecats, because API rate limits and CPU are
shared. The dispatch formula:

```
toDispatch = min(capacity, batchSize, readyCount)

where:
  capacity   = maxPolecats - activePolecats
  batchSize  = scheduler.batch_size (default 1)
  readyCount = sling contexts whose work bead appears in `bd ready`
```

### 8.3 Daemon integration

The scheduler runs as step 14 of the daemon heartbeat (every 3 minutes),
AFTER all health checks and agent recovery
(`docs/design/scheduler.md:75-93`). It uses `flock` for serialization
and a 5-minute subprocess timeout.

---

## 9. Refinery — the Bors-Style Merge Queue

`internal/refinery/` is one of the larger packages (engineer.go,
batch.go, score.go, pr_provider_*.go, manager.go). The batch-then-bisect
merge model is described in §2.6 above and in
`docs/design/architecture.md:206-237`.

### 9.1 The cleanup pipeline

After `gt done`, the cleanup chain (per
`docs/design/polecat-lifecycle-patrol.md:124-163`) is:

```
Polecat → POLECAT_DONE mail → Witness
   Witness verifies cleanup_status → MERGE_READY → Refinery
      Refinery claims MR → acquires merge slot → runs quality gates
         → squash-merges → MERGED mail → Witness
            Witness verifies commit on main → acknowledges
```

Failure handling at each stage (`docs/design/polecat-lifecycle-patrol.md:166-176`):

| Failure | Detection | Recovery |
|---------|-----------|----------|
| `gt done` fails mid-execution | Zombie state (session alive, `done-intent` label) | Witness `DetectZombiePolecats()` |
| `POLECAT_DONE` mail lost | Witness patrol finds dead session w/ `hook_bead` | `DetectZombiePolecats()` |
| Merge conflict | Refinery `doMerge()` | Conflict resolution task, MR blocked |
| `MERGED` mail lost | Witness patrol finds closed bead w/ live session | `DetectZombiePolecats()` |

### 9.2 Merge strategies

Configurable in rig settings (`docs/agent-provider-integration.md` 1.0.0
CHANGELOG, `docs/design/architecture.md`):

- `direct` — squash to local main + push
- `mr` — open GitHub PR + `gh pr merge`
- `local` — local merge, no push

The `require_review=true` setting (1.0.0) makes merge wait for an
approving GitHub review. Quality gates are configurable per rig and run
in parallel (`GatesParallel` from gt-8b2i — 0.9.0).

### 9.3 Quality scoring

`internal/refinery/score.go` and the `quality-review` plugin
(`plugins/quality-review/plugin.md`) work together: the Refinery emits
`quality-review-result` wisps on each merge; the plugin queries them
every 6h and computes per-worker trends, escalating breaches.

---

## 10. Wasteland — Federation Across Orgs

Wasteland (`docs/WASTELAND.md`, `internal/wasteland/`) is the federated
work-coordination network. Implementation is split between
`wasteland.go`, `spider.go` (fraud detection — added 0.12.1), and
`trust.go`.

### 10.1 Concept

Wasteland is "a federated work coordination network linking Gas Towns
through DoltHub" (`README.md:115-117`). Status is currently **Phase 1
(wild-west mode)**: all operations write directly to your local fork
of the commons database; no trust-level enforcement yet.

A "rig" in Wasteland context is your participant identity — distinct
from local Gas Town rigs. When you join via `gt wl join <upstream>`
(typically `hop/wl-commons`), the command:

1. Forks the upstream DoltHub repo to your org.
2. Clones the fork locally into `~/gt/.wasteland/<org>/<db>/`.
3. Registers your rig in the shared `rigs` table.
4. Pushes the registration.
5. Saves config to `mayor/wasteland.json`.

### 10.2 The wanted board

Items in the `wanted` table have fields: `id` (`w-<hash>`), `title`,
`project`, `type` (feature/bug/design/rfc/docs), `priority` (0-4),
`effort` (trivial..epic), `posted_by`, `status`
(open/claimed/in_review/completed/withdrawn).

Workflow: `gt wl browse` → `gt wl claim <id>` → external work → `gt wl
done <id> --evidence <url>` → maintainer issues a `stamp`.

### 10.3 Stamps — multi-dimensional reputation

The `stamps` table (`docs/WASTELAND.md:436-453`) records attestations
with fields `author`, `subject`, `valence` (JSON of quality/reliability/creativity),
`confidence`, `severity`. The schema enforces the "yearbook rule" at
the DB level: `CHECK (NOT(author = subject))` — you cannot stamp your
own work.

Trust levels are tracked but not enforced in Phase 1
(`docs/WASTELAND.md:147-162`):

| Level | Name | Planned Capabilities |
|-------|------|---------------------|
| 0 | Registered | Browse, post |
| 1 | Participant | Claim, submit |
| 2 | Contributor | Proven work history |
| 3 | Maintainer | Validate and stamp others' work |

Reputation is portable across multiple wastelands. The `spider.go`
fraud-detection module looks for stamp-trading rings.

---

## 11. Plugin System

The plugin system (`docs/design/plugin-system.md`, `plugins/`) is the
extension mechanism. **Plugins are formulas executed by Dogs**, not
arbitrary Go code (though `dolt-snapshots` ships a Go binary alongside
its formula).

### 11.1 The plugin format

Each plugin lives in `plugins/<name>/` with a `plugin.md` (TOML
frontmatter + Markdown body) and usually a `run.sh`. Frontmatter
schema (`docs/design/plugin-system.md:170-196`):

```toml
name = "string"           # Unique plugin identifier
description = "string"    # Human-readable
version = 1               # Schema version

[gate]
type = "cooldown|cron|condition|event|manual"
duration = "1h"           # for cooldown
schedule = "0 9 * * *"    # for cron
check = "gt stale -q"     # for condition
on = "startup"            # for event

[tracking]
labels = ["plugin:rebuild-gt", "category:maintenance"]
digest = true

[execution]
timeout = "5m"
notify_on_failure = true
severity = "low"          # or medium/high/critical
```

### 11.2 The plugin contract

Plugins are dispatched by Deacon patrol. Gate evaluation queries
**wisps** on the ledger, not state files (`docs/design/plugin-system.md:97-131`):

```bash
# Cooldown check: any runs in last hour?
bd list --wisp-type patrol --label plugin:rebuild-gt --created-after 1h -n 1
```

Each plugin run creates a wisp bead with structured labels. Plugin
wisps accumulate and get squashed daily by `gt plugin digest`.

### 11.3 The 13 plugins shipped

`plugins/` directory (13 plugins):

| Plugin | Gate | Severity | Purpose |
| ------ | ---- | -------- | ------- |
| **compactor-dog** | cooldown 30m | medium | Monitor Dolt commit growth across DBs and escalate when compaction needed (AI agent uses judgment) |
| **dolt-archive** | cooldown 1h | critical | Offsite backup: JSONL snapshots to git, dolt push to GitHub/DoltHub |
| **dolt-backup** | cooldown 15m | high | Smart Dolt DB backup with change detection |
| **dolt-log-rotate** | cooldown 6h | medium | Rotate Dolt server log when over size threshold |
| **dolt-snapshots** | event `convoy.created` | low | Tag Dolt DBs at convoy boundaries for audit/diff/rollback (Go binary + SQL) |
| **git-hygiene** | cooldown 12h | low | Clean stale branches, stashes, loose objects across all rig repos |
| **github-sheriff** | cooldown 2h | low | Monitor GitHub CI checks on open PRs, create beads for failures |
| **gitignore-reconcile** | cooldown 6h | low | Auto-untrack files tracked but matching active .gitignore rule |
| **quality-review** | cooldown 6h | medium | Analyze quality-review-result wisps from Refinery, alert on trends |
| **rebuild-gt** | cooldown 1h | medium | Rebuild stale gt binary from gastown source |
| **stuck-agent-dog** | cooldown 5m | high | Context-aware stuck/crashed agent detection (polecats + Deacons), with explicit OUT-OF-SCOPE rules for crew |
| **submodule-commit** | cooldown 2h | low | Auto-commit changes inside git submodules |
| **tool-updater** | cooldown 168h | medium | Upgrade bd and dolt via Homebrew |

Two plugins of particular interest:

- **stuck-agent-dog** insists that "the daemon should NEVER kill
  workers; it detects and logs. This plugin (running as a Dog agent
  with AI judgment) makes the restart decision after inspecting tmux
  pane output for signs of life." Its scope block is explicit:
  `<rig>-polecat-<name>` and `hq-deacon` are in scope; **crew sessions
  are explicitly out of scope** ("crew lifecycle is managed by the
  overseer (human), not dogs"). This is a deliberate guardrail.
- **dolt-snapshots** is the only plugin that ships its own Go binary
  (`main.go`, `main_test.go`). It's triggered by `event = "convoy.created"`
  and tags Dolt databases at convoy lifecycle boundaries for audit,
  diff, and rollback — using both immutable tags and mutable branches.

### 11.4 Plugin locations

`docs/design/plugin-system.md:45-67` shows the discovery model:

```
~/gt/plugins/                # Town-level (universal)
~/gt/<rig>/plugins/<name>/   # Rig-level (project-specific)
```

The Deacon scans both locations during patrol.

---

## 12. Observability — OTEL and the Feed

### 12.1 OTEL data model

`docs/otel-data-model.md` and `docs/design/otel/` define the
OpenTelemetry data model. Every record carries `run.id` (UUID) so all
events from a single agent session can be correlated
(`docs/otel-data-model.md:1-9`).

The identity hierarchy is `instance` → `run` → individual events
(`docs/otel-data-model.md:11-37`):

| Attribute | Source | Example |
| --------- | ------ | ------- |
| `instance` | `hostname:basename(town_root)` | `laptop:gt` |
| `town_root` | absolute path | `/Users/pa/gt` |
| `run.id` | UUID v4 | propagated via `GT_RUN` |
| `agent_type` | adapter | `claudecode`, `opencode`, `copilot` |
| `role` | Gas Town role | `polecat`, `witness`, `mayor`, `refinery`, `crew`, `deacon`, `dog`, `boot` |
| `agent_name` | role + slot | `wyvern-Toast` |
| `session_id` | tmux pane name |  |
| `rig` | rig name |  |

Event types (`docs/otel-data-model.md:39-260+`):

| Event | Trigger |
| ----- | ------- |
| `agent.instantiate` | Once per agent spawn — anchors all subsequent events |
| `session.start` / `session.stop` | tmux session lifecycle |
| `prime` / `prime.context` | Each `gt prime` invocation |
| `prompt.send` | Each `gt sendkeys` dispatch |
| `agent.event` | One per content block in agent log (opt-in) |
| `agent.usage` | One per assistant turn (token counts) |
| `bd.call` | Each bd subprocess invocation w/ duration |
| `mail` | All mail operations (send/read/archive/...) |
| `agent.state_change` | idle→working etc. |
| `mol.cook` / `mol.wisp` / `mol.squash` / `mol.burn` | Molecule lifecycle |

Metrics named in the README (`README.md:617-619`):

- `gastown.session.starts.total`
- `gastown.bd.calls.total`
- `gastown.polecat.spawns.total`
- `gastown.done.total`
- `gastown.convoy.creates.total`

Default OTLP backend is VictoriaMetrics/VictoriaLogs:

```bash
export GT_OTEL_LOGS_URL="http://localhost:9428/insert/jsonline"
export GT_OTEL_METRICS_URL="http://localhost:8428/api/v1/write"
```

### 12.2 The feed TUI

`gt feed` (`internal/feed/curator.go`, 544 LOC) is a three-panel
real-time terminal dashboard (`README.md:471-503`):

- **Agent Tree** — hierarchical view of agents grouped by rig and role
- **Convoy Panel** — in-progress and recently-landed convoys
- **Event Stream** — chronological creates, completions, slings, nudges

Flags: `--problems` (start in problems view), `--plain`, `--window`,
`--since 1h`. Navigation: `j`/`k` scroll, `Tab` switch panels, `1`/`2`/`3`
jump, `?` help, `p` toggle problems view.

The **Problems View** is critical at scale (20-50+ agents). It groups
by health state (`README.md:493-501`):

| State | Condition |
|-------|-----------|
| **GUPP Violation** | Hooked work with no progress for an extended period |
| **Stalled** | Hooked work with reduced progress |
| **Zombie** | Dead tmux session |
| **Working** | Active, progressing normally |
| **Idle** | No hooked work |

Intervention keys: `n` nudge selected agent, `h` handoff (refresh context).

### 12.3 Web dashboard

`gt dashboard` runs a web UI (default port 8080) "auto-refreshes via
htmx and includes a command palette for running gt commands directly
from the browser" (`README.md:505-518`).

---

## 13. The Proxy Server / Proxy Client

`cmd/gt-proxy-server/`, `cmd/gt-proxy-client/`, `internal/proxy/`. The
full reference is `docs/proxy-server.md`.

### 13.1 What it is

The proxy server exists for **sandboxed polecat execution** — when a
polecat runs inside a container (e.g. Daytona) it still needs to talk
to Gas Town's control plane, but without direct access to the host
filesystem or GitHub credentials. Two binaries:

| Binary | Runs on | Purpose |
| ------ | ------- | ------- |
| `gt-proxy-server` | Host | Accepts mTLS connections; executes `gt`/`bd` and serves git smart-HTTP |
| `gt-proxy-client` | Container | Installed as `gt` and `bd`; forwards calls over mTLS |

The architecture:

```
 Container                          Host
  gt mail inbox            ──mTLS──► gt-proxy-server ──► exec gt mail inbox
  git push origin/proxy    ──mTLS──► gt-proxy-server ──► git-receive-pack ~/gt/MyRig/.repo.git
```

### 13.2 Endpoints

mTLS server (default `0.0.0.0:9876`):

| Method | Path | Description |
| ------ | ---- | ----------- |
| POST | `/v1/exec` | Execute a `gt` or `bd` command |
| GET  | `/v1/git/<rig>/info/refs?service=<svc>` | git smart-HTTP capability advertisement |
| POST | `/v1/git/<rig>/git-upload-pack` | git fetch/clone |
| POST | `/v1/git/<rig>/git-receive-pack` | git push (CN-scoped branch authorization) |

Local admin server (default `127.0.0.1:9877`, no TLS):

| Method | Path | Description |
| ------ | ---- | ----------- |
| POST | `/v1/admin/issue-cert` | Issue a new polecat client certificate |
| POST | `/v1/admin/deny-cert` | Add a certificate serial to the runtime deny list |

### 13.3 Security model

The CN format is `gt-<rig>-<name>` (e.g. `gt-GasTown-rust`).
**Identity is derived from the client certificate, not from the request
body** — agents can't lie about who they are.

Branch authorization: a polecat may only push to
`refs/heads/polecat/<name>-*`. The server parses the pkt-line ref list
**before** passing the body to `git-receive-pack` and rejects any ref
outside scope.

Subcommand allowlist (auto-discovered from `gt proxy-subcmds`):

- `gt`: prime, hook, done, mail, nudge, mol, status, handoff, version, convoy, sling
- `bd`: create, update, close, show, list, ready, dep, export, prime, stats, blocked, doctor

Rate limits (per CN): default 10 req/s sustained, burst 20, max 32
concurrent exec subprocesses. The server's exec env is intentionally
sparse: only `HOME` and `PATH` are passed to subprocesses — no
`GITHUB_TOKEN`, no `GT_TOKEN`.

### 13.4 Importance

The proxy is not for routing LLM API calls. It is a **filesystem and
credential isolation boundary** between a possibly-malicious polecat
container and the host. This is the security-side complement to the
sandboxed-polecat-execution design at `docs/design/sandboxed-polecat-execution.md`.

---

## 14. Hooks — Git-Worktree-Based Persistence

`docs/HOOKS.md` covers the hook system, which has two distinct meanings
in Gas Town:

1. **Lifecycle hooks** — Claude `settings.json`, OpenCode JS plugins,
   Copilot `.github/hooks/gastown.json`. These are the integration
   layer covered in §6.
2. **Work hooks** — the polecat's git worktree carrying persistent
   work state ("propulsion principle").

Lifecycle hooks are managed centrally via:

```
~/.gt/hooks-base.json              ← Shared base config (all agents)
~/.gt/hooks-overrides/
  ├── crew.json                    ← Override for all crew workers
  ├── witness.json                 ← Override for all witnesses
  ├── gastown__crew.json           ← Rig+role override (gastown crew specifically)
```

Merge strategy: `base → role → rig+role` (more specific wins).

Generated targets per rig (`docs/HOOKS.md:38-50`):

| Target | Path | Override key |
| ------ | ---- | ------------ |
| Crew (shared) | `<rig>/crew/.claude/settings.json` | `<rig>/crew` |
| Witness | `<rig>/witness/.claude/settings.json` | `<rig>/witness` |
| Refinery | `<rig>/refinery/.claude/settings.json` | `<rig>/refinery` |
| Polecats (shared) | `<rig>/polecats/.claude/settings.json` | `<rig>/polecats` |
| Mayor | `mayor/.claude/settings.json` (key `mayor`) |
| Deacon | `deacon/.claude/settings.json` (key `deacon`) |

The "propulsion principle" (`docs/concepts/propulsion-principle.md`):
"**If you find something on your hook, YOU RUN IT.**" The startup
algorithm for every agent (`propulsion-principle.md:81-87`):

1. Check hook (`gt hook`)
2. Work hooked → EXECUTE immediately
3. Hook empty → Check mail for attached work
4. Nothing anywhere → ERROR: escalate to Witness

---

## 15. The `gt-model-eval/` Directory

`gt-model-eval/` is a promptfoo-based test harness — outside the Go
binary — for comparing Claude Opus, Sonnet, and Haiku on patrol
decision tasks (`gt-model-eval/README.md`). The intent: collect
**evidence** for safely downgrading patrol roles (Deacon, Witness,
Dogs) to cheaper models.

Two test classes:

- **Class B (directive)** — explicit instructions in the prompt to
  validate instruction-following. 82 tests across 8 YAML files
  (`deacon-zombie.yaml`, `witness-stuck.yaml`, `refinery-triage.yaml`,
  `dog-orphan.yaml`, etc.).
- **Class A (reasoning)** — neutral role context, no answer hints.
  Tests whether the model can derive the correct action from raw shell
  evidence. 12 tests.

The economic motivation: "Gas Town multi-agent setups burn through
Opus budget on patrol agents that follow prescriptive formulas. These
agents parse shell output and make rule-based decisions — they may not
need Opus-level reasoning."

---

## 16. The `.claude/` and `.opencode/` Directories

These are how Gas Town configures the AI sessions that drive its own
development (i.e. dogfooding).

### 16.1 .claude/

Two subdirectories: `commands/` and `skills/`.

`commands/`:
- **patrol.md** — `/patrol [witness|deacon|refinery]` — runs one patrol
  cycle. Documents the full step list for each role (witness has 9
  steps; deacon has 14 steps including the scheduler step).
- **reaper.md** — `/reaper [--dry-run]` — runs the wisp reaper directly
  (same cycle as `mol-dog-reaper`).
- **backup.md** — backup command.

`skills/`:
- **crew-commit/** (SKILL.md) — canonical commit workflow for crew:
  pre-flight → branch → stage → commit → push → PR. Insists "NEVER
  commit directly to `main`."
- **pr-list/** (SKILL.md) — list GitHub PRs in formatted ASCII table.
- **ghi-list/** (SKILL.md) — list GitHub issues in formatted ASCII
  table.
- **pr-sheriff/** (skill.md, lowercase) — PR Sheriff workflow: triage
  PRs into easy-wins and crew assignments. Delegates to
  `mol-pr-sheriff-patrol` formula at
  `$GT_ROOT/.beads/formulas/mol-pr-sheriff-patrol.formula.toml`.
  Notable: "This rig (gastown/crew/max) is responsible for
  steveyegge/gastown only. The beads repo (steveyegge/beads) is
  handled by beads/crew/emma. Do NOT discover or triage PRs from repos
  outside your scope." — a per-crew-member scope rule.

### 16.2 .opencode/

- **commands/handoff.md** — `/handoff` slash command for OpenCode users.
- **plugins/gastown.js** — the OpenCode JS plugin. Reacts to
  `session.created` (loads prime context), `session.compacted`
  (reloads), `session.deleted` (records costs). Injects
  `gt prime --hook` output into the system prompt via
  `experimental.chat.system.transform`. Sample:

```js
export const GasTown = async ({ $, directory }) => {
  const role = (process.env.GT_ROLE || "").toLowerCase();
  // ...
  return {
    event: async ({ event }) => {
      if (event?.type === "session.created") {
        if (didInit) return;
        didInit = true;
        primePromise = loadPrime("startup", eventSessionID(event));
      }
      if (event?.type === "session.compacted") {
        primePromise = loadPrime("compact", eventSessionID(event));
      }
      if (event?.type === "session.deleted") {
        const sessionID = event.properties?.info?.id;
        if (sessionID) {
          await captureRun(`${shellQuote(gtBin)} costs record --session ${shellQuote(sessionID)}`);
        }
      }
    },
    // ...
  };
};
```

---

## 17. The Contrib Harnesses

`docs/contrib-harnesses/polecat-pr-flow/` is a worked example of an
end-to-end rig customization. It demonstrates the **two-level
customization model** that operators have:

1. **Role directives** — per-role markdown injected at prime time
   (`~/gt/<rig>/directives/polecat.md`). Sets a behavioral boundary.
2. **Formula overlays** — per-formula TOML files that modify steps
   (`~/gt/<rig>/formula-overlays/mol-polecat-work.toml`). Surgical step
   replacement.

The polecat-pr-flow harness changes a rig's behavior from "Refinery
merges directly" to "Polecat opens a GitHub PR for review, doesn't
merge." Three override modes for overlays
(`docs/design/architecture.md:357-365`):

| Mode | Effect |
| ---- | ------ |
| `replace` | Swap step description entirely |
| `append` | Add text after existing step description |
| `skip` | Remove step (dependents inherit its needs) |

Validation via `gt doctor` and `gt formula overlay show <formula> --rig
<rig>`.

---

## 18. Notable Design Quotes

### From `docs/why-these-features.md:253-262`

> These features aren't bolted on. They're foundational:
>
> 1. Attribution is not optional. Every action has an actor.
> 2. Work is data. Not just tickets — structured, queryable data.
> 3. History matters. Track records determine trust.
> 4. Scale is assumed. Multi-repo, multi-agent, multi-org from day one.
> 5. Verification over trust. Quality gates are first-class primitives.

### From `docs/concepts/propulsion-principle.md:3-7`

> Gas Town is a steam engine. Agents are pistons. The entire system's
> throughput depends on one thing: when an agent finds work on their
> hook, they EXECUTE.

### From `docs/glossary.md:10-14`

> **GUPP (Gas Town Universal Propulsion Principle)**: "If there is work
> on your Hook, YOU MUST RUN IT." This principle ensures agents
> autonomously proceed with available work without waiting for external
> input. GUPP is the heartbeat of autonomous operation.
>
> **NDI (Nondeterministic Idempotence)**: The overarching goal ensuring
> useful outcomes through orchestration of potentially unreliable
> processes. Persistent Beads and oversight agents (Witness, Deacon)
> guarantee eventual workflow completion even when individual operations
> may fail or produce varying results.

### From `docs/design/witness-at-team-lead.md:983`

> *"The transport changes. The ledger endures."*

### From `docs/design/dog-execution-model.md:46-51`

> **Principle**: If the dog's failure would cause a Clown Show, it must
> be imperative Go.

### From `docs/design/polecat-lifecycle-patrol.md:313-322`

The "Deacon murder spree" lesson: "Mechanical detection of 'stuck' is
fragile because distinguishing 'thinking deeply' from 'hung' requires
intelligence. This is why Boot exists (intelligent triage) and why the
daemon's thresholds are conservative. Only the witness (an AI agent)
should make judgment calls about whether a polecat is truly stuck."

### From the MEOW acronym (`docs/glossary.md:7-9`)

> **MEOW (Molecular Expression of Work)**: Breaking large goals into
> detailed instructions for agents. Supported by Beads, Epics, Formulas,
> and Molecules.

And from `README.md:647-656`, "MEOW (Mayor-Enhanced Orchestration
Workflow)" — note the same acronym is used twice with different
expansions. The README version (Mayor-Enhanced) is the workflow
pattern; the glossary version (Molecular Expression of Work) is the
decomposition philosophy.

---

## 19. CHANGELOG Architectural Milestones

The 92K changelog covers 5 months of evolution from 0.1.0 (2026-01-02)
to 1.1.0 (2026-05-06). Major architectural shifts:

| Version | Date | Key architectural changes |
|---------|------|--------------------------|
| **0.1.0** | 2026-01-02 | Initial release. Mayor, Deacon, Witness, Refinery, Crew, Polecat all present. Convoy, sling, mail, escalate, handoff. Daemon mode. npm + GoReleaser distribution. |
| **0.2.x** | Jan 2026 | Iteration on lifecycle / safety. |
| **0.7.0** | 2026-02-15 | **Convoy ownership + merge strategies** (`--owned`, `--merge=direct|mr|local`). `gt convoy land`. Agent factory replaces switch statements. **Gemini CLI** and **Copilot CLI** runtime adapters. Auto-dismiss stalled polecat permission prompts. Dead crew detection. |
| **0.8.0** | 2026-02-23 | **Work queue + dispatch engine** (`gt queue`, config-driven capacity scheduler with sling context beads). **Full OpenTelemetry instrumentation** (logs + metrics via OTLP, VictoriaMetrics/VictoriaLogs integration). **Dog subsystem expansion** (handler patrol, session-hygiene dog, idle dog reaping, shutdown dance state machine). **Wasteland CLI (`gt wl`)** first lands. **Pi agent provider**. **Cost-tier presets**. **Promptfoo model comparison framework**. **gt mol step await-event**. Removed Dolt branch-per-polecat (huge simplification). |
| **0.9.0** | 2026-03-01 | **Batch-then-bisect merge queue** (Bors-style, GatesParallel). **Persistent polecats** (identity + sandbox survive `gt done` — biggest lifecycle change). **Compactor / Doctor / JSONL / Wisp Reaper dogs** all hardened to imperative Go. **Root-only wisps** (~6k rows/day → ~400). **Six-stage data lifecycle**. **`gt maintain`**, **`gt vitals`**, **`gt upgrade`**. **OperationalConfig** for ZFC-compliant thresholds. Nudge-first communication shift (~80% Dolt commit reduction for patrol traffic). |
| **0.10.0** | 2026-03-03 | (small) |
| **0.11.0** | 2026-03-05 | **Schema evolution** in wl sync. Reaper TTL tightened. |
| **0.12.0** | 2026-03-11 | **Refinery merge strategy** configurable direct vs PR. Compactor dog ships executable `run.sh`. MVGT integration guide. ZFC fix: removed ZFC-violating decision engine from boot triage. |
| **0.12.1** | 2026-03-15 | **Spider Protocol** — fraud detection for Wasteland stamps. |
| **0.13.0** | 2026-03-29 | **Wasteland stamps and pilot cohorts**, scorekeeper, stamp loop. **Post-squash gate phase** in Refinery. **Refinery auto_push** config. **Cost tiers for Boot and dogs**. |
| **1.0.0** | 2026-04-02 | **Windows platform support**. **Workflow formula type**. **Refinery PR merge strategy** (`gh pr merge`). `require_review=true`. `/crew-commit` skill. **Rate-limit watchdog plugin** auto-estop on 429. Default effort level config. `gt dolt pull`. Mayor approval for scope expansion. Polecat PreToolUse guard blocks sudo. |
| **1.0.1** | 2026-04-25 | `gt dog done` closes accumulated plugin mails (context bloat fix). |
| **1.1.0** | 2026-05-06 | Convoy completion + cross-rig dep notifications. Scheduler guards skip closed/tombstone beads. Resilience under Dolt memory pressure (subprocess timeout, parallel rig scan). bd 1.0+ compatibility. Daemon hardening (cross-rig mail delivery, pthread deadlock fix). Auto-burn orphan molecules. |

**Key takeaways from the CHANGELOG**:

- The **persistent-polecat refactor in 0.9.0** is the most architectural
  shift. Earlier (pre-0.9), polecats were destroyed on `gt done`. Now
  identity and sandbox survive, and only sessions are ephemeral.
- The **proxy server** arrives gradually, but the file `cmd/gt-proxy-server/`
  is in the tree and the docs reference Daytona integration as 2026-03-02
  (`sandboxed-polecat-execution.md`).
- **OTEL** instrumentation arrived in one big sweep at 0.8.0.
- **Wasteland** arrived in 0.8.0 (CLI suite) and matured in 0.12.1
  (fraud detection) and 0.13.0 (stamps and pilot cohorts).
- **Boot** and the watchdog chain are present from 0.1.0 but were
  refined repeatedly (notably 0.9.0 removed a ZFC-violating decision
  engine from degraded boot triage).

---

## 20. Open Questions and Known Limitations

Marked as **planned / not yet implemented** in the docs:

- **Capability-based routing** — `docs/why-these-features.md:79-83` says
  "Status: Planned — Skill tracking and automatic routing are not yet
  implemented. Work assignment is currently manual via `gt sling`."
- **Federation (Highway Operations Protocol / HOP)** —
  `docs/why-these-features.md:153-156`: "Status: Planned — Federation
  via HOP is designed but not yet implemented. Gas Town currently
  operates as a single-town system." Wasteland exists as a Phase 1
  alternative.
- **Witness AT integration** — `docs/design/witness-at-team-lead.md:3-8`:
  "Status: Future architecture — NOT YET IMPLEMENTED. The current
  system uses tmux-based session management. This document describes a
  planned architectural change to use Claude Code Agent Teams (AT) as
  the transport layer. No code for this exists yet."
- **Mol Mall (formula registry)** — `docs/design/mol-mall-design.md`:
  "Status: Vision document — Phase 1 (local formulas) exists. Phases
  2-5 (registry, publishing, federation) are not implemented."
- **Wasteland trust enforcement** — `docs/WASTELAND.md:18-21`: "Phase 1
  (wild-west mode) — All operations write directly to your local fork
  of the commons database. There is no trust-level enforcement yet."
- **Wasteland claim propagation** — same doc: "In Phase 1, claims write
  to your local wl_commons database only. Other rigs won't see your
  claim until the upstream commons is updated (e.g., via a DoltHub
  PR)."
- **Pool size enforcement** — `docs/design/polecat-lifecycle-patrol.md:653-657`:
  "Deferred — On-demand allocation works; fixed pool is optimization,
  not correctness."
- **Refinery mayor notification after merge** — same doc, "Pending":
  "PRs #2436/#2437 closed; branch cleanup shipped, mayor notify not
  yet."
- **`gt wl leave`** — `docs/WASTELAND.md:99-103`: not yet implemented.

Open questions in the plugin-system doc
(`docs/design/plugin-system.md:262-269`):

1. Plugin discovery in multiple clones: which clone's `plugins/` dir is
   canonical?
2. Should specific plugins prefer specific dogs?
3. Can plugins depend on other plugins? ("Probably not in v1.")
4. How to temporarily disable a plugin without deleting it?

---

## 21. Summary — Why This Architecture Matters

Gas Town is best understood as a **persistent multi-agent town** in
which:

- **Every action has an actor** (BD_ACTOR plumbing); attribution is
  structural, not behavioural.
- **Work is structured data on a Dolt-backed ledger**, queryable across
  rigs and federations.
- **Sessions are pistons** that fire on hooks; identities and sandboxes
  persist across firings.
- **Supervision is layered** (Daemon → Boot → Deacon → Witness →
  Polecats), with deliberate redundancy so that any single layer
  failing degrades to lower-level mechanical recovery.
- **Communication has discipline** — nudge is the default,
  mail/escalation is for things that must survive session death,
  seance is the channel of last resort for cross-session memory.
- **Customization is layered** — town > rig > role > formula
  directives, with three precedence-ordered overlays
  (replace/append/skip).
- **Extension is plugin-shaped** — TOML+Markdown frontmatter, gates
  evaluated against the wisp ledger, dispatched by the Deacon to Dogs.
- **Verification is first-class** — Refinery's batch-then-bisect merge
  queue, configurable quality gates, quality-review plugin computing
  per-worker trends.
- **Federation is designed-in** — Wasteland as a Dolt-backed federated
  wanted board with portable multi-dimensional reputation.
- **Telemetry is end-to-end** — OTEL with a `run.id` correlating all
  events across an agent session.
- **Security is meaningful** — the proxy server enforces a strong
  trust boundary between containerised polecats and the host
  (filesystem/credential isolation, branch-scoped pushes, mTLS, rate
  limits).

The system's load-bearing assumption is that, with the right
infrastructure, **20–30 agents can be productive simultaneously**
because work persists, lifecycles are managed, escalation routes
deterministically, and dispatch back-pressures intelligently. Gas Town
is a serious attempt at building the workspace-OS substrate for an
agent-saturated software-engineering organization.
