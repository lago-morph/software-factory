# Overstory — Substrate Audit

> Round-2 subagent 10 of `research/PLAN.md` §3.3.
> Source: `github.com/jayminwest/overstory` branch `main` at audit time (package
> version `0.11.0`, MIT, npm `@os-eco/overstory-cli`).
> Files consulted: `README.md`, `STEELMAN.md`, `CLAUDE.md`, `SECURITY.md`,
> `CHANGELOG.md`, `package.json`, `bunfig.toml`, `bun.lock`,
> `docs/runtime-abstraction.md`, `docs/runtime-adapters.md`,
> `docs/headless-hooks-design.md`, `docs/canopy-prompt-architecture.md`,
> `docs/direction-multi-swarm-and-containers.md`,
> `docs/direction-ui-and-ipc.md`, `docs/design/containerize-swarms.md`,
> `agents/{coordinator,lead,builder,scout,reviewer,merger,supervisor,
> orchestrator,monitor}.md`, `src/index.ts`, `src/types.ts`, `src/config.ts`,
> `src/runtimes/{types,registry,claude,aider,pi,gemini,sapling,codex}.ts`,
> `src/mail/{store,client,broadcast}.ts`,
> `src/worktree/{manager,tmux,process}.ts`,
> `src/merge/{queue,resolver,lock,predict}.ts`,
> `src/watchdog/{daemon,triage,health}.ts`,
> `src/commands/{coordinator,sling,merge,serve}.ts`,
> `src/agents/{manifest,overlay,turn-runner,lifecycle}.ts`,
> `.github/workflows/{ci,publish}.yml`.

## 1. What it is (one paragraph, independent of marketing)

Overstory is a Bun/TypeScript CLI (`ov`, ~36 Commander.js subcommands,
`src/index.ts:1-55`, version `0.11.0`) that turns either a human-driven
Claude Code session or a long-lived headless subprocess into the
**orchestrator** of a hierarchy of subordinate AI coding agents. Agents are
spawned by `ov sling <task-id>` (`src/commands/sling.ts`, 1,351 ln); each
gets its own `git worktree` on a branch
`overstory/{agentName}/{taskId}` (`src/worktree/manager.ts:64`), and runs
in tmux or as a headless `Bun.spawn` emitting NDJSON stream-json on stdout
(`src/agents/turn-runner.ts`). Inter-agent communication is a SQLite mail
bus in WAL mode (`src/mail/store.ts`) with 14 message types and
`@all`/`@builders`-style group addressing (`src/mail/broadcast.ts:23-40`).
A second SQLite database (`merge-queue.db`) holds a FIFO merge queue
(`src/merge/queue.ts:46-57`) whose resolver attempts up to four conflict-
resolution tiers — clean merge, keep-incoming, AI-rewrite, full re-imagine
(`src/merge/resolver.ts`). A "watchdog" Tier-0 mechanical daemon plus
optional Tier-1 LLM triage and Tier-2 monitor agent keep the fleet alive.
The substrate is runtime-agnostic: an `AgentRuntime` interface
(`src/runtimes/types.ts:158-266`) admits 11 adapter implementations
(Claude Code is the only `stable`; all others `experimental`). Overstory
is best described as **a single-machine, file-system-and-SQLite-backed
orchestration substrate for parallel git-worktree coding agents** — not a
server, not a SaaS, not a container fleet.

## 2. Architecture map

The hierarchy as documented in README.md lines 222-228 is
`Orchestrator (multi-repo) → Coordinator (one per project) → Supervisor /
Lead (depth 1) → Workers (depth 2, leaf)`, with a configurable depth limit
(default 2; CLAUDE.md line 43) "to prevent runaway spawning" — STEELMAN
risk 12 calls out exactly this failure mode. Components and citations:

**Operator surface.** Either a human at Claude Code with hooks in
`.claude/settings.local.json` (`SessionStart → ov prime`,
`UserPromptSubmit → ov mail check --inject`, plus PreToolUse path /
capability / dangerous-bash guards from `src/agents/hooks-deployer.ts`), or
a long-lived `ov coordinator start --headless` subprocess. CLAUDE.md
§"Orchestrator Model" lines 19-25; the headless/hook mapping table in
`docs/headless-hooks-design.md` Q1.

**Spawn path: `ov sling <task-id>`** (`src/commands/sling.ts`, 1,351 ln).
Validates the task via the tracker (`src/tracker/factory.ts`), creates a
worktree on a `overstory/{agentName}/{taskId}` branch
(`src/worktree/manager.ts:54-83`), loads the base agent definition
(`src/agents/manifest.ts`), generates the per-task overlay
(`src/agents/overlay.ts`), invokes `runtime.deployConfig(worktreePath,
overlay, hooks)` (`src/runtimes/claude.ts:118`, `aider.ts:100`, …), and
spawns either a tmux session (`src/worktree/tmux.ts`, 721 ln) or a
headless `Bun.spawn` driven by the per-turn engine
(`src/agents/turn-runner.ts`, 1,383 ln, stream-json on stdin/stdout).

**Workers.** Scouts (read-only, `agents/scout.md`), Builders (read-write
on a strict `FILE_SCOPE`, `agents/builder.md`), Reviewers (read-only,
`agents/reviewer.md`), Leads (depth-1 spawners, `agents/lead.md`, 435 ln),
and Mergers (read-write merge specialists, `agents/merger.md`, 164 ln,
triggered when the lead's `ov merge --dry-run --json` predicts a tier-3+
conflict — lead.md lines 335-360).

**Mail bus.** SQLite at `.overstory/mail.db`, WAL mode, busy_timeout 5 s.
Storage in `src/mail/store.ts` (425 ln); high-level client in
`src/mail/client.ts`. Schema below in §5.

**Merge pipeline.** Triggered by `merge_ready` mail. FIFO `merge-queue.db`
in `src/merge/queue.ts` (246 ln). Sentinel-file lock in `src/merge/lock.ts`
(140 ln). Dry-run predictor in `src/merge/predict.ts` (249 ln). Resolver in
`src/merge/resolver.ts` (932 ln), 4 tiers detailed in §6.

**Watchdog stack.** Tier 0 mechanical daemon polling tmux / pid / event-
store / mail (`src/watchdog/daemon.ts`, 1,257 ln, progressive escalation
0:warn → 1:nudge → 2:triage → 3:terminate at lines 5-15). Tier 1 AI
triage reads last 50 lines of session log and asks Claude
`retry|terminate|extend` (`src/watchdog/triage.ts`, 205 ln, 42-74). Tier 2
monitor agent for continuous fleet patrol (`agents/monitor.md`, 214 ln).

**UI / observability layer.** `ov serve` (`src/commands/serve.ts`, 565 ln)
runs HTTP + WebSocket on `127.0.0.1:7321` with routes `/healthz`,
`/api/runs`, `/api/agents`, `/api/events`, `/api/mail`, `/ws`, and an
`ui/dist` Vue SPA fallback (CLAUDE.md lines 622-627). This is the
documented "primary operator surface" for new (headless-default) projects;
tmux is the opt-in escape hatch.

## 3. The `AgentRuntime` interface

The single most reusable artifact in Overstory. Defined at
`src/runtimes/types.ts:158-266`, the interface has ~14 methods, of which 9
are required and 5 are optional. Methods, with one-line summaries:

| Method | Required | Purpose |
|---|---|---|
| `id: string` | yes | adapter identifier ("claude", "aider", "pi", …) |
| `stability: "stable"\|"beta"\|"experimental"` | yes | self-declared maturity |
| `instructionPath: string` | yes | relative path inside a worktree where the per-agent overlay file is written (e.g. `.claude/CLAUDE.md`, `AGENTS.md`, `CONVENTIONS.md`) |
| `buildSpawnCommand(opts: SpawnOpts) → string` | yes | shell string to launch the agent in a tmux pane |
| `buildPrintCommand(prompt, model?) → string[]` | yes | argv for a headless one-shot AI call (used by the merge resolver tiers 3-4 and the watchdog triage agent) |
| `deployConfig(wt, overlay, hooks) → Promise<void>` | yes | writes the overlay file and any runtime-specific guard config (Claude hooks JSON, Pi `.pi/extensions/`, Codex `AGENTS.md`, Aider `CONVENTIONS.md`) |
| `detectReady(paneContent) → ReadyState` | yes | parses tmux pane to detect loading/dialog/ready phase |
| `parseTranscript(path) → Promise<TranscriptSummary\|null>` | yes | returns `{inputTokens, outputTokens, model}` from runtime-native log files |
| `getTranscriptDir(projectRoot) → string\|null` | yes | where transcripts live on disk |
| `buildEnv(model: ResolvedModel) → Record<string,string>` | yes | env vars for provider routing (e.g. ANTHROPIC_BASE_URL/AUTH_TOKEN for gateway routing — see README §"Gateway Providers") |
| `requiresBeaconVerification?() → boolean` | optional | whether the orchestrator's "did the initial Enter actually get through?" loop should run |
| `connect?(process) → RuntimeConnection` | optional | direct JSON-RPC over stdin/stdout, replacing tmux for delivery; only Pi implements (per docstring at `types.ts:97-115`) |
| `headless?: boolean` | optional | declares runtime is non-tmux (Sapling = static `true`) |
| `buildDirectSpawn?(opts: DirectSpawnOpts) → string[]` | optional | argv for `Bun.spawn` headless; only some runtimes have it (Claude does; Codex, Pi, Cursor do not — README line 203) |
| `parseEvents?(stream) → AsyncIterable<AgentEvent>` | optional | NDJSON stdout decoder for headless agents |
| `prepareWorktree?(path) → Promise<void>` | optional | one-shot setup (Copilot folder-trust handshake) |

**How thin/thick.** The doc claim is "~200-400 line adapter file" (per
`docs/runtime-abstraction.md` line 14). Empirically:

| Runtime | Lines | Stability |
|---|---:|---|
| `runtimes/types.ts` (interface) | 266 | — |
| `runtimes/aider.ts` | 147 | experimental |
| `runtimes/gemini.ts` | 243 | experimental |
| `runtimes/codex.ts` | 273 | experimental |
| `runtimes/pi.ts` | 305 | experimental |
| `runtimes/claude.ts` | 579 | **stable** |
| `runtimes/sapling.ts` | 710 | stable (static headless) |

The thin adapters (Aider at 147 lines) confirm the contract is genuinely
modest. The mass concentrated in Claude and Sapling is mostly transcript
parsing, hook-deployer plumbing, and headless `parseEvents`. The interface
itself is the minimum surface area at which Overstory's existing
orchestration logic stops needing to know about Claude Code specifically.

**Portability implications.**

1. The orchestration engine (sling, coordinator, merge resolver, watchdog
   triage) calls **only** these methods plus `getRuntime()` from
   `src/runtimes/registry.ts`. It never shells out to `claude` directly.
2. Every runtime adapter is independently swappable per-agent (CLI
   `ov sling --runtime <name>`; `manifest.json` per-agent default).
3. The contract assumes a tmux fallback even for runtimes that prefer
   headless — `buildSpawnCommand` is mandatory. A truly tmux-free deployment
   requires `headless: true` AND `buildDirectSpawn`.
4. Guards are runtime-defined. Aider's adapter explicitly says "No
   OS-level sandbox or hook guards. Security relies on Aider's built-in
   file-scope limiting" (`aider.ts:30-32`). That is a portability hole, not a
   bug: Overstory's safety floor is **the weakest runtime in the swarm**.
5. The merge resolver tiers 3-4 hard-bind to whatever runtime is configured
   via `config.runtime.printCommand`/`config.runtime.default`
   (`resolver.ts:367`). Adopters can route conflict resolution to a
   completely different model from the one driving workers — useful for
   independence in any architecture that requires V&V model-family
   separation (Architecture 3 of `architectures/00-comparison.md`).

## 4. Worktree isolation

Implemented in `src/worktree/manager.ts:54-119`:

- `createWorktree({repoRoot, baseDir, agentName, baseBranch, taskId})` runs
  `git worktree add -b overstory/{agentName}/{taskId} {baseDir}/{agentName}
  {baseBranch}` (line 75). Naming is strict: branch always
  `overstory/{agentName}/{taskId}`; path always `{baseDir}/{agentName}`,
  where `baseDir` defaults to `.overstory/worktrees` (CLAUDE.md line 255).
- Pre-flight: before calling `git worktree add` it lists existing worktrees
  and rejects the operation if the same branch is already checked out
  somewhere else (lines 66-73). This explicitly defends against a known
  silent-overwrite failure mode (referenced bead `overstory-6878`).
- Post-flight: `validateWorktreeCreation` (lines 93-119) checks two things:
  (a) the new path appears in `git worktree list --porcelain`, and (b)
  `git ls-files` returns at least one tracked file. If either check fails,
  it calls `rollbackWorktree` which best-effort-removes the worktree and
  force-deletes the branch.
- `removeWorktree(repoRoot, path, {force?, forceBranch?})` at lines 258-290
  does `git worktree remove [--force] <path>` then `git branch -d` (or `-D`
  with `forceBranch`). Best-effort: if branch deletion fails (e.g. unmerged),
  the worktree is already gone and the error is swallowed.
- A specialized rescue path `preserveSeedsChanges(...)` (lines 304-405)
  extracts the `.seeds/` diff from a doomed lead branch and commits it onto
  canonical via `git diff ... | git apply --index | git commit`, so that
  issue-tracker state lives on even though lead branches are never merged
  through the normal pipeline.

**Garbage collection** is operator-driven, not automatic. The README documents
`ov worktree clean --completed | --all | --force` and the more aggressive
`ov clean --worktrees`. Both go through `removeWorktree`. There is no
periodic sweeper; the watchdog daemon does not GC worktrees.

**Disk-space model.** Each worker = one full checkout of the repo. STEELMAN
risk 7 explicitly names worktree corruption, orphan pruning, and disk space
as failure modes Overstory inherits.

## 5. SQLite mail

`src/mail/store.ts` is 425 lines and dependency-light: `import { Database }
from "bun:sqlite";`. The store opens its database with three pragmas
(line 200-202):

```
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
PRAGMA busy_timeout = 5000;
```

…and on close runs a passive WAL checkpoint (`close():` lines 414-422) so a
subsequent process sees the writes.

**Schema** (`store.ts:54-67`):

```sql
CREATE TABLE messages (
  id          TEXT PRIMARY KEY,
  from_agent  TEXT NOT NULL,
  to_agent    TEXT NOT NULL,
  subject     TEXT NOT NULL,
  body        TEXT NOT NULL,
  type        TEXT NOT NULL DEFAULT 'status'
                CHECK(type IN (<14 types>)),
  priority    TEXT NOT NULL DEFAULT 'normal'
                CHECK(priority IN ('low','normal','high','urgent')),
  thread_id   TEXT,
  payload     TEXT,                -- JSON blob
  read        INTEGER NOT NULL DEFAULT 0,
  created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX idx_inbox  ON messages(to_agent, read);
CREATE INDEX idx_thread ON messages(thread_id);
```

The CHECK constraint on `type` is regenerated at runtime from the
`MAIL_MESSAGE_TYPES` constant in `src/types.ts:293-308`, so the column
constraint always matches the TypeScript enum. A `migrateSchema` function
(lines 80-149) does in-place upgrades: missing `payload` column → ALTER ADD,
missing/outdated CHECK → table-rename-and-copy.

**Message types** (`src/types.ts:274-308`):

- Semantic (operator-facing): `status | question | result | error`.
- Protocol (machine-facing): `worker_done | worker_died | merge_ready |
  merged | merge_failed | escalation | health_check | dispatch | assign |
  decision_gate`.

Each protocol type has a documented payload shape (the `WorkerDonePayload`
interface and siblings start at `types.ts:327`). Protocol messages drive
state transitions in the watchdog and merge pipeline; semantic messages are
human-readable.

**Broadcast semantics** (`src/mail/broadcast.ts:23-92`). Recipient strings
starting with `@` resolve to groups:

- `@all` → all active sessions except the sender.
- `@builder|@builders` → all active builders except the sender.
  Same singular/plural pair for every capability in `CAPABILITY_GROUPS`
  (scout, reviewer, lead, merger, supervisor, coordinator, monitor).
- Resolution requires `activeSessions: AgentSession[]` as a pure input — no
  I/O — and throws if it resolves to zero recipients. The client
  (`src/mail/client.ts`) calls `resolveGroupAddress` then *inserts one row
  per resolved recipient*. There is no separate broadcast table.

**Throughput.** No benchmarks in repo; only a doc claim of "~1-5 ms per
query" (CLAUDE.md line 87). The bottleneck is SQLite's single-writer rule —
WAL allows concurrent readers but writes serialize through the
`busy_timeout=5000`. For a 10-20-agent swarm where each agent polls every
2 s (the dashboard interval), the load is on the order of 5-10 reads/sec
and a write per real event. SQLite WAL handles this without effort. The
real cost ceiling is the **mail-poll** pattern — every poll burns context
tokens in the agent reading the mail injection. STEELMAN risk 2 quantifies
the wider concern: 20 agents polling every 30 s = "24/7 background spend".

**Failure modes.**

- **Schema migration failure** is transactional (BEGIN/COMMIT, lines 116-148),
  so partial migration is impossible.
- **Insert/delete failure** wraps the error in a typed `MailError` (lines
  318-322, 366-371) so callers can recover.
- **Lock contention** is bounded by the 5 s busy_timeout; beyond that the
  raw bun:sqlite error surfaces.
- **No-recipient broadcast** throws explicitly (`broadcast.ts:62-66`) rather
  than silently swallowing.
- **Mail injection prompt-injection** — STEELMAN risk 10 explicitly names
  malicious mail as an attack surface; there is **no signature / no
  capability check** on the `from` field. Any process that can write to
  `.overstory/mail.db` can impersonate any agent.

## 6. The 4-tier conflict resolution

The four tiers, named exactly as the docstring (`src/merge/resolver.ts:1-12`),
implementation lines, and what they cost:

**Tier 1 — clean merge** (`tryCleanMerge`, lines 235-248).
`git merge --no-edit <branch>`. If exit code 0, done. Cost: one git
invocation. This is the only tier that does nothing risky.

**Tier 2 — auto-resolve / keep-incoming** (`tryAutoResolve`, lines 256-308,
guarded by `hasContentfulCanonical` at 192-204 and `checkMergeUnion` at
210-214). For each conflicted file: read content, check `merge=union`
gitattribute. If union, concatenate both sides (`resolveConflictsUnion`,
lines 173-186); otherwise call `resolveConflictsKeepIncoming` which strips
the `<<<<<<<` / `=======` / `>>>>>>>` block and keeps only the incoming
(branch) text — **unless** the canonical (HEAD) side has non-whitespace
content, in which case the file is escalated rather than silently losing
canonical changes (line 273-280). Cost: I/O + regex per file, no LLM call.

**Tier 3 — AI-resolve** (`tryAiResolve`, lines 340-409). For each remaining
conflicted file, the resolver builds a prompt that includes (a) explicit
"Output ONLY raw file content, NO markdown, NO preamble" rules, (b) optional
historical context from prior merges (mulch-search-derived, see below), and
(c) the raw conflicted-file content with markers intact. It then calls
`getRuntime(config?.runtime?.printCommand ?? config?.runtime?.default)`
and runs `runtime.buildPrintCommand(prompt)` — i.e. `claude --print -p
<prompt>` by default (`claude.ts:94-100`). Output is checked against
`looksLikeProse` (lines 314-333) which rejects anything starting "I ", "Here
", "To resolve", or wrapped in markdown fencing — a clever guardrail against
LLMs returning explanations instead of code. Cost: one LLM call per
conflicted file, full file in input and output.

**Tier 4 — re-imagine** (`tryReimagine`, lines 415-495). Aborts the merge,
then for each file in `entry.filesModified` it fetches both the canonical
version (`git show {canonical}:{file}`) and the branch version (`git show
{branch}:{file}`) and asks the AI to "reimplement the changes from the
branch version onto the canonical version" as a fresh file. Same prose-
guard rejection. Cost: one LLM call per file with *two* full file versions
in the prompt — roughly 3× the token cost of Tier 3.

**Conflict-history learning** (`queryConflictHistory`, lines 608-619, with
`buildConflictHistory` at 549-601). After each merge attempt, the resolver
records a textual pattern through `MulchClient.record('architecture', {type:
'pattern', tags: ['merge-conflict'], …})` (lines 626-650, fire-and-forget).
On a subsequent merge, it calls `mulchClient.search('merge-conflict')` and
parses the text back (`parseConflictPatterns`, regex at lines 501-535).
**Skip-tier logic**: a tier that has failed ≥ 2 times on any of the same
files **with zero successes** is skipped in future merges
(`buildConflictHistory:574-580`). The implementation is heuristic, not
formally typed — pattern recovery depends on the exact prose of the
recorded description.

**Operational guards** (in `resolver.ts:692-724`): before any tier runs, it
checks `git diff --name-only` and `--cached` for dirty tracked files; auto-
commits files that match os-eco state prefixes (`.seeds/`, `.overstory/`,
`.greenhouse/`, `.mulch/`, `.canopy/`, `.claude/`); stashes anything left;
unstashes in a `finally` block. Sentinel-file lock at
`.overstory/merge-{sanitized-target}.lock` (`src/merge/lock.ts`) prevents
two `ov merge` runs concurrent against the same target — uses `writeFileSync
(..., {flag:"wx"})` for atomic creation; if a lockfile exists, the holder
PID is checked for liveness and dead holders are evicted.

The whole pipeline is **opt-in per tier**: `createMergeResolver({
aiResolveEnabled, reimagineEnabled, ...})`. Tier 1 always runs, Tier 2
always runs, Tier 3 only if `aiResolveEnabled`, Tier 4 only if
`reimagineEnabled`. Cost-conscious operators can disable Tiers 3-4 and force
a human-in-loop merge instead. STEELMAN risk 6 is honest: even Tier 4
requires human review for semantic conflicts.

## 7. Headless / non-interactive operation

This is the question that decides whether Overstory is CI-friendly or not.
Mixed answer.

**What's available today.**

1. **Headless agent processes.** New projects ship with
   `runtime.claudeHeadlessByDefault: true` (CLAUDE.md lines 46-83). Workers
   spawn via `src/agents/turn-runner.ts` (1383 lines) as a `Bun.spawn`
   subprocess with `claude -p --output-format stream-json
   --input-format stream-json`. There is no tmux requirement. CI containers
   without tmux/DBus can run agents this way (CLAUDE.md line 55).
2. **Headless coordinator.** `ov coordinator start --headless` exists
   (`coordinator.ts:348-353, 513-…`) and the `headlessFlag` branch spawns a
   long-lived coordinator subprocess instead of a tmux session. Same for
   `ov orchestrator start` and `ov monitor start`.
3. **Exit triggers.** `ov coordinator check-complete`
   (`coordinator.ts:1467-1595`) evaluates three boolean triggers from
   `config.coordinator.exitTriggers`:
   - `allAgentsDone` — all non-coordinator sessions in the current run are
     in state `completed` **and** the merge queue has no `pending` rows.
     This is non-trivial — it explicitly waits for the merge tail
     (lines 1504-1523, bead `overstory-5c08`).
   - `taskTrackerEmpty` — shells out to `bd ready --json` / `sd ready
     --json` and reports complete when no work is unblocked.
   - `onShutdownSignal` — externally settable.
   `complete = true` only if all *enabled* triggers are met. No-enabled
   triggers => `complete: false` (safe default).
4. **JSON output mode** on essentially every command (the `--json` global
   flag in `src/index.ts` and per-command). A CI driver can poll status
   without parsing ANSI.
5. **`ov merge --all --json`** does the FIFO drain unattended; if conflicts
   exceed the enabled tier set, exit non-zero with structured error.
6. **CI workflows in the repo itself.** `.github/workflows/ci.yml` and
   `publish.yml` only run `bun install / lint / typecheck / test`. Overstory
   does not dogfood itself in its own CI.

**What's missing for "start coordinator, dispatch issue, wait for merge,
exit".**

1. **No `ov run` one-shot driver.** There is no `ov run --task <id> --until-
   merge` command. To approximate it, a CI script must:
   `ov coordinator start --headless --watchdog`
   `ov coordinator send "process task X"` (or write a dispatch mail)
   `until ov coordinator check-complete --json | jq -e .complete; do sleep N; done`
   `ov coordinator stop`
   The contract is *available*, but it is the operator's responsibility to
   wire it together. There is no exit-code-based fail-fast on global
   timeout, runaway-spawn detection, or aggregate cost ceiling.
2. **Cost ceilings.** No `--max-cost-usd` / `--max-tokens` flag anywhere.
   STEELMAN risk 12 calls this out as the canonical runaway risk and the
   only enforcement mechanism is the watchdog's `MAX_ESCALATION_LEVEL = 3`
   (terminate) for *stalled* agents — not *expensive* ones. `ov costs`
   reports after the fact.
3. **No container/sandbox.** `docs/design/containerize-swarms.md` is a
   design doc, not implementation. STEELMAN risk 7 catalogs tmux, git
   worktrees, SQLite WAL, and Claude Code hooks as infrastructure overhead;
   none of these are containerized.
4. **No structured failure → CI exit-code mapping.** When the merge queue
   leaves residual `failed` entries, a human is expected to triage. A
   reasonable CI wrapper would treat that as non-zero exit.

**Verdict on §3.3 question 7.** Overstory *can* run as a one-shot batch
suitable for CI — the primitives are there (`--headless`, `check-complete`,
`--json`, exit triggers, FIFO merge drain) — but the **contract has to be
assembled by the caller**. There is no single `ov run --until-done <task>`.
For a CI/CD pipeline this is a meaningful gap. It is also a small gap: a
~150-line wrapper script could close it.

## 8. Diff against `architectures/00-comparison.md` §4.1

Each row is one shared-infrastructure primitive. "Provides" = present and
usable as-is. "Partial" = the primitive exists but is incomplete in a way
that matters for the four architectures. "Absent" = not present.

| §4.1 primitive | Overstory verdict | Citation |
|---|---|---|
| **Worktree per unit of work** | **Provides.** | `src/worktree/manager.ts:54-119`; one worktree per agent, branch named `overstory/{agent}/{task}`. |
| **Sandboxed agent execution (capability scoping, network restrictions)** | **Partial.** Capability scoping is enforced **only on Claude Code** (PreToolUse hooks in `hooks-deployer.ts` + `guard-rules.ts`); the 9 other adapters explicitly opt out (`aider.ts:30-32` "no OS-level sandbox or hook guards"; `copilot --allow-all-tools`; `cursor --yolo`; README adapter table lines 205-217). No network restrictions anywhere. Codex relies on OS-level Seatbelt/Landlock. | Adapters in `src/runtimes/`; README adapter table; STEELMAN risk 10. |
| **Stable ID assignment (R/A/F/AE/U/S/K/etc.)** | **Absent.** Overstory uses agent names and task IDs from beads/seeds, but does not assign R&D-style stable identifiers to specs, features, units. Adopting any of the four architectures requires this layer on top. | No stable-ID generator in `src/`. |
| **Out-of-construction-tree scenarios** | **Absent.** Overstory's worktree pattern places construction trees side-by-side under `.overstory/worktrees/`. There is no "scenario / acceptance test tree" out-of-band of the construction tree. | — |
| **LLM-judge with model-family independence** | **Partial.** The merge resolver and watchdog triage can be routed to a different runtime via `config.runtime.printCommand` (`resolver.ts:367`, `triage.ts`), and gateway providers (z.ai, OpenRouter) are first-class (README §Gateway Providers, lines 337-374). But there is **no LLM-judge role** — review is a same-runtime reviewer agent (`agents/reviewer.md`, 140 ln). | `agents/reviewer.md`; runtime/print routing. |
| **Trajectory capture** | **Provides.** Headless runtimes emit NDJSON events that flow into `events.db` via `src/events/store.ts` + `src/events/tailer.ts`. Token usage parsed from runtime transcripts into `metrics.db` (`src/metrics/`). `ov replay`, `ov trace`, `ov feed`, `ov inspect`, `ov costs` consume them. | `src/events/`, `src/metrics/`; CLAUDE.md §"Project Structure". |
| **Manager loop / orchestrator** | **Provides.** `ov coordinator start` (long-lived process, exit triggers, mail-driven dispatch); operator-as-orchestrator (Claude Code session) is the alternative. `src/commands/coordinator.ts` is 1810 lines. | `src/commands/coordinator.ts`; CLAUDE.md §"Orchestrator Model". |
| **Decision log / audit trail** | **Partial.** SQLite databases (mail, sessions, events, runs, metrics, merge-queue) capture machine-readable history. There is no human-readable decision log per cycle. Mulch records function as a learning store but not an audit log. | `src/sessions/store.ts` + `RunStore`; `ov run show`. |
| **AGENTS.md / discoverability** | **Provides.** Per-runtime `instructionPath` (`.claude/CLAUDE.md`, `AGENTS.md`, `CONVENTIONS.md`) is deployed by `runtime.deployConfig`. Repo-baked `agents/{role}.md` (9 base definitions) plus dynamic per-task overlays (`src/agents/overlay.ts`). | `src/agents/overlay.ts`; `agents/*.md`. |

Net coverage: **5 of 9 provided outright, 3 partial, 1 absent.** The deepest
gap is "stable ID assignment", which is methodology-specific and lives
above the substrate. The most worrying partial is "sandboxed agent
execution": Overstory's safety floor is the weakest runtime adapter in the
swarm, and 10/11 adapters are explicitly experimental.

## 9. Risks Jaymin names

`STEELMAN.md` is 159 lines of deliberate self-criticism, organized as 12
named risks. The four clusters the brief asks about, with citations:

- **Merge conflicts (risk 6).** Quote: "Overstory's tiered merge
  resolution helps, but tier 4 (AI resolver) still requires human review
  for semantic conflicts. The merge queue becomes a bottleneck." Risk 1
  (compounding errors) is the deeper version: 3 parallel refactors × 5%
  individual error rate ≈ 14% aggregate.
- **Agent oversight (risks 4, 8).** Debugging swarm output is "forensic
  reconstruction" across multiple worktrees, mail threads, and
  interleaved timelines; the dashboard "shows activity, not output." Risk
  11 adds: scout-spec-build separates exploration from implementation,
  but the right design is usually discovered *during* implementation.
- **Cost ceiling (risks 2, 12).** Concrete number: 20 agents × 15 tasks ×
  6 h ≈ 8 M tokens ≈ $60; same tasks sequentially ≈ 1.2 M tokens ≈ $9 —
  "the 2-h speedup cost $51 in coordination." Risk 12 names runaway
  spawning, retry loops, and 24/7 mail-poll background spend as
  unbounded-resource failure modes; **"swarms require active monitoring
  and circuit breakers"** which Overstory does not provide.
- **Sandbox escape (risk 10).** Named attack vectors: mail injection
  (plaintext SQLite, no signing), hooks (eval user-provided bash guards),
  cross-worktree reads, predictably-named tmux sessions. A compromised
  agent can send malicious mail, modify `.overstory/config.yaml` to spawn
  more agents, or "inject into the merge queue to backdoor merged code."

Other risks named but not the brief's focus: 3 (architectural drift /
loss of coherent reasoning), 5 (premature decomposition), 7
(infrastructure complexity — tmux, git worktrees, SQLite WAL, watchdog
daemons, Claude Code hooks, dashboard TUI each a "failure mode you now
have to maintain and debug"), 9 (context fragmentation across agents).

`SECURITY.md` (59 lines) is far shorter. In-scope vulnerabilities: command
injection in `Bun.spawn`, path traversal, arbitrary file access, symlink
attacks, temp-file races, **agent escape** (an agent accessing files
outside its worktree or file scope), **mail injection**. Out of scope:
DoS via large input, cost overruns ("operational concern, not security"),
and any attack requiring local shell access. Existing hardening listed:
"Tool enforcement hooks that mechanically block file modifications for
non-implementation agents", "dangerous git operation blocking (force push,
reset --hard)", "file scope enforcement per agent", SQLite WAL with busy
timeouts. **These hardening measures all live only in the Claude Code
adapter.** Every other adapter explicitly opts out.

Jaymin's "when swarms might still be worth it" list (STEELMAN §"When Agent
Swarms Might Still Be Worth It"): truly independent tasks, embarrassingly
parallel work, large-scale exploration, learning/research,
deadline-sprints. Most day-to-day engineering is "deeply interconnected"
and better served by a single focused agent.

## 10. Recommendation

**Steal the design; do not adopt the implementation as-is.** Specifically:
re-implement the substrate in Python (Anyio + sqlite3 stdlib + libgit2 or
GitPython) and lift Overstory's interface designs verbatim. Three reasons:

**Reason 1: The interface designs are excellent, but the implementation is
Bun-locked and TypeScript-locked.** The `AgentRuntime` interface
(`src/runtimes/types.ts:158-266`), the mail schema (`store.ts:54-67`), the
4-tier conflict resolver (`resolver.ts:1-12`), and the FIFO queue
(`queue.ts:46-57`) are crisp, well-documented, and would survive
translation. But the implementation depends on `bun:sqlite`, `Bun.spawn`,
`Bun.file`, and Bun's stream/process APIs. Adopting as-is means accepting
Bun + TypeScript as a permanent constraint on the substrate. Given that
`research/PLAN.md` §10.4 anticipates OpenHands (Python) as a peer
substrate, and that Architecture 3's V&V discipline favors Python's broader
ML/eval ecosystem, a Bun-only substrate creates an unnecessary integration
boundary.

**Reason 2: Overstory's safety floor is the weakest runtime in the swarm,
and Jaymin says so on the record.** Of 11 adapters, only Claude Code is
`stable` (README adapter table lines 205-217). Aider, Copilot, Cursor, and
OpenCode adapters have zero guards (`aider.ts:30-32` is explicit). The
hook-based path-boundary / capability / dangerous-bash guards
(`hooks-deployer.ts`) only apply to Claude Code. Adopting Overstory as a
substrate means inheriting a security model whose strongest guarantees
disappear the moment you change runtime — which the substrate is *designed
to encourage you to do*. STEELMAN risks 10 and 12 both list this as a
fundamental risk, and `SECURITY.md` puts cost-runaway out of scope as
"operational, not security." That is honest. It is also a non-starter for
a system that wants to run unattended in CI. Re-implementing lets us
**unify the guard layer at the substrate**: capability/path/bash guards
become a substrate-level mediator that every runtime adapter must consult,
not a per-runtime opt-in.

**Reason 3: Headless CI is 80 % there but the last 20 % is structural.**
`ov coordinator start --headless`, `ov coordinator check-complete`,
`ov merge --all --json`, FIFO queue with exit triggers, JSON output on
every command — these primitives compose into a CI driver. But there is
no `ov run --task <id> --until-done --max-cost-usd N --timeout-s T` single
command, no cost ceiling, no runaway-spawn detector beyond a configurable
depth limit (default 2, CLAUDE.md line 43), no `.github/workflows/*.yml`
that runs Overstory itself, and no container story (the design doc at
`docs/design/containerize-swarms.md` is a design, not code). For a
software-factory that wants "we want to run as a CI/CD pipeline" (PLAN.md
§3.3 goal), these gaps need primary surgery, not bolt-ons. Re-implementing
lets us put the CI contract at the center: one command, one exit code,
budgeted compute, audit-trail file, deterministic cleanup.

**Keep verbatim** (design IP): the `AgentRuntime` interface
(`runtimes/types.ts:158-266`), mail schema and 14-type taxonomy
(`store.ts:54-67` + `types.ts:274-308`), group addressing
(`broadcast.ts:23-40`), the 4-tier resolver including the
`hasContentfulCanonical` data-loss guard (`resolver.ts:192-204`) and the
`looksLikeProse` LLM-output rejector (`resolver.ts:314-333`) — both
come from operational pain not paper design — the sentinel-file merge
lock with pid-liveness takeover (`lock.ts`), the FIFO queue with
`resolved_tier` recorded inline (`queue.ts:46-57`), the tiered watchdog
escalation, the two-layer base+overlay agent-definition pattern, mulch-
backed conflict-history learning with skip-after-2-failures
(`resolver.ts:574-580`), and the `check-complete` exit-trigger model
including the merge-tail check (`coordinator.ts:1467-1595`).

**Drop or redesign**: Bun + TypeScript → Python; tmux as first-class →
headless-only (the WebSocket UI is already the documented primary
surface); per-runtime guards → substrate-level capability mediator; the
11-adapter spread → three `stable` adapters (Claude Code, OpenHands SDK,
one open-weights option); operator-as-orchestrator (a human at Claude
Code) → headless CLI driver as the *only* orchestrator (a non-negotiable
for CI); plaintext mail → mail rows signed by writer identity (HMAC or
nonce) rejected at injection time if unsigned.

**Why not "adopt as-is" or "fork":** Both lock us into the Bun runtime and
inherit the 10 experimental adapters' safety footprint. Forking also
inherits Overstory's maintenance cadence ("PRs reviewed in roughly 2-week
batches; PRs inactive for 30+ days are closed" — README line 13), which
collides with the software-factory ambition.

**Why not "re-implement in Python from scratch":** Overstory has made
~50 specific design choices that were obviously informed by production
pain — `hasContentfulCanonical`, `looksLikeProse`, the sentinel-lock pid
takeover, the `.seeds/` preservation rescue, the os-eco state auto-commit
in the merge pre-check, the `validateWorktreeCreation` two-step post-flight
check. Re-discovering those costs months. Stealing them costs days.

**Why not "discard":** Of the substrate primitives in
`architectures/00-comparison.md` §4.1, Overstory provides 5 outright and 3
partially. The next-closest candidate (OpenHands SDK, audited in
report 11) attacks the *runtime* layer, not the orchestration layer. We
will need both. Discarding Overstory means re-deriving worktree GC, mail
schema, merge-tier discipline, watchdog escalation, and the runtime-
adapter contract from first principles. We won't do better than Jaymin
did. The right relationship to Overstory is **canonical reference
design** — like reading Plan 9 source before writing a kernel.

---

### Appendix A — Key file/line index

| Concern | File | Lines |
|---|---|---|
| CLI entry / version | `src/index.ts` | 1-55 |
| `AgentRuntime` interface | `src/runtimes/types.ts` | 158-266 |
| Mail schema (SQL) | `src/mail/store.ts` | 54-67 |
| Mail message types (TS) | `src/types.ts` | 274-308 |
| Group addressing | `src/mail/broadcast.ts` | 23-92 |
| Worktree create + validate | `src/worktree/manager.ts` | 54-119 |
| Merge queue schema | `src/merge/queue.ts` | 46-57 |
| Tier 1 — clean merge | `src/merge/resolver.ts` | 235-248 |
| Tier 2 — keep-incoming + guard | `src/merge/resolver.ts` | 192-204, 256-308 |
| Tier 3 — AI resolve | `src/merge/resolver.ts` | 340-409 |
| Tier 4 — re-imagine | `src/merge/resolver.ts` | 415-495 |
| Conflict-history learning | `src/merge/resolver.ts` | 549-619 |
| Merge sentinel lock | `src/merge/lock.ts` | 1-40 |
| Watchdog tiers | `src/watchdog/daemon.ts` | 5-15 |
| AI triage prompt | `src/watchdog/triage.ts` | 42-74 |
| `check-complete` exit triggers | `src/commands/coordinator.ts` | 1467-1595 |
| CI workflow | `.github/workflows/ci.yml` | full file (23 ln) |
| Publish workflow | `.github/workflows/publish.yml` | full file (101 ln) |
| Aider adapter (thinnest) | `src/runtimes/aider.ts` | 1-148 |
| Claude adapter (heaviest) | `src/runtimes/claude.ts` | 1-579 |

### Appendix B — Sources status

All files reachable at `raw.githubusercontent.com/jayminwest/overstory/main/<path>`
returned HTTP 200 and were fetched and read to the depth indicated above
(brief sections 1-10). Specifically read in full: `README.md`, `STEELMAN.md`,
`CLAUDE.md`, `SECURITY.md`, `package.json`, all 9 `agents/*.md` base
definitions, `src/runtimes/types.ts`, `src/runtimes/aider.ts`,
`src/mail/store.ts`, `src/mail/broadcast.ts`, `src/worktree/manager.ts`,
`src/merge/queue.ts`, and the entirety of the 4-tier resolver in
`src/merge/resolver.ts`. Read partially (head + targeted greps): the
other runtime adapters, `src/commands/coordinator.ts` (around `checkComplete`
at lines 1450-1595), `src/agents/turn-runner.ts`, watchdog daemon/triage,
`docs/runtime-abstraction.md`, `docs/headless-hooks-design.md`,
`docs/design/containerize-swarms.md`. **Blocked URLs:** the GitHub
Contents API (`api.github.com/repos/jayminwest/overstory/contents/...`) and
the GitHub MCP `mcp__github__get_file_contents` tool both refused the
session (rate limit for the unauthenticated sandbox IP; MCP scope limited
to `lago-morph/software-factory`). Directory enumeration was done instead
via the GitHub web HTML at `github.com/jayminwest/overstory/tree/main`,
which is fetchable but not officially supported. One in-tree path returned
HTTP 404: `.github/workflows/release.yml` — confirmed via GitHub HTML
listing that only `ci.yml` and `publish.yml` exist in `workflows/`. No
other 404s. The `ui/` directory was deliberately not read, per brief.
