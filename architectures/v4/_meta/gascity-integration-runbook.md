# Gas City Integration Runbook — Software Factory v4

**Purpose.** Concrete, step-by-step recipe an engineer follows to stand up Gas City for
Software Factory v4. This is the operator deliverable for the Gas City adoption track.
Follow each section in order; do not skip the conformance gate (§7).

**Config source of truth.** All config keys, file layout, and verification status come from
[gascity-config-anchor.md](./gascity-config-anchor.md). Where a key is marked
`[needs-pinned-gc-run (G11)]` below, confirm it against a live `gc` install before relying
on it in production.

**Rig model.** Per **D-31** (adopted 2026-06-01) a single Gas City city hosts **multiple
rigs simultaneously**. The worked example in §8 shows a worker rig and a judge rig co-residing
in the same city — this is the minimum Phase-2 shape and a required design constraint, not an
option.

---

## 1. Prerequisites

### Go toolchain

| Requirement | Value | Source |
|---|---|---|
| Go version | **1.26.3** — `go.mod` is authoritative; verify with `head -5 go.mod` | [config anchor §1](./gascity-config-anchor.md) |
| Minimum host tools | `git`, `make`, `curl`, `tar`, Docker + `docker compose` | [conformance-check preconditions](./gascity-conformance-check.md) |

Install Go 1.26.3 (adjust path as needed):

```bash
curl -sLO https://go.dev/dl/go1.26.3.linux-amd64.tar.gz
tar -C /usr/local -xzf go1.26.3.linux-amd64.tar.gz
export PATH="/usr/local/go/bin:$PATH"
go version     # must print: go version go1.26.3 linux/amd64
```

> **Verification status — Go version: harvest-verified.** The `go.mod` of
> `gastownhall/gascity` is the authoritative source. The prototype README states "Go 1.25"
> but that is stale — `go.mod` wins. Always run `head -5 go.mod` after cloning to confirm
> the required version.

### Binaries to pre-stage

Gas City's sandbox/container environment blocks in-container downloads via a TLS-inspection
proxy. Stage all binaries on the **host** before building the Docker image (F12 context,
PLAN items 1–2):

| Binary | Role |
|---|---|
| `gc` | Gas City controller — built from source (§2) |
| `bd` | Bead store CLI — companion to `gc` |
| `dolt` | Dolt SQL server for the bead store |
| `node` | Node.js runtime (required by `claude`) |
| `claude` | Claude Code CLI — the agent process |

### Environment variables

```bash
# Required — allows `claude --dangerously-skip-permissions` to run as root (F12)
export IS_SANDBOX=1

# Required — Dolt push/clone ref; default refs/dolt/data is rejected by
# TLS-inspection proxies (F9)
export DOLT_REF=refs/heads/dolt-data
```

> **Verification status — IS_SANDBOX: harvest-verified (F12).**
> **Verification status — DOLT_REF: harvest-verified (F9).**

---

## 2. Install and Pin

### Pin identity

All v4 work targets exactly these artifacts:

| Artifact | Value |
|---|---|
| Prototype repo | `lago-morph/gascity-prototype` |
| Prototype branch + commit | `claude/great-pascal-RUfkN` @ **`b14c278`** (PLAN dated 2026-05-25) |
| Upstream `gc` SDK | `gastownhall/gascity@183897e` (post-v1.0.0, PackV2) |

### Clone and build

```bash
# Clone the prototype at the pinned commit
git clone https://github.com/lago-morph/gascity-prototype.git /tmp/gascity
cd /tmp/gascity
git checkout claude/great-pascal-RUfkN

# Verify the commit before building
git rev-parse HEAD        # must print: b14c278...
head -5 go.mod            # confirms the required Go version

# Build and install the gc binary
make install              # produces /usr/local/bin/gc

# Verify
gc version                # should report a version line
bd --version              # companion bead-store CLI; must also be on PATH
```

> **E-C01-03:** If `git rev-parse HEAD` does not match `b14c278`, stop and re-check your
> checkout. Behavioural deviation from harvest facts surfaces as conformance failures.

### What "install" produces

The v4 production install does **not** use `gc init` (it is interactive and cannot run
unattended — F4). Instead, author `pack.toml` and `city.toml` directly from §3–§4 below,
then run `gc start --foreground` (§6).

---

## 3. `city.toml` — Workspace Configuration

`city.toml` is the workspace install config. Section presence is the feature flag: absent
section = capability off. It is **version-controlled** alongside packs.

> **D-31 rule:** The rig block is an **array** (`[[rig]]` / `[[rigs]]`). Author one entry
> per rig role. The Phase-2 minimum is two blocks: worker + judge.

> **D-32 rule:** The city.toml rig-block **spelling** (`[[rig]]` vs `[[rigs]]`) is
> **`[needs-pinned-gc-run (G11)]`** — F1 names `[[rig]]` canonical but the prototype
> `city.toml.example` uses `[[rigs]]`. The invariant that holds regardless of spelling:
> **a rig `path` field MUST NOT appear in city.toml** (it is a PackV2 error). Path bindings
> live exclusively in `.gc/site.toml` (§4).

```toml
# city.toml
# ─────────────────────────────────────────────────────────────────────────────
# WORKSPACE
# Verification: harvest-verified (city.toml.example:9-11)
# ─────────────────────────────────────────────────────────────────────────────
[workspace]
name     = "software-factory"          # city identity
provider = "claude"                    # city-default session provider preset
global_fragments = ["command-glossary", "operational-awareness"]
#   ^── city-wide prompt fragments; list may be empty at Phase 0

# ─────────────────────────────────────────────────────────────────────────────
# PER-RIG PACK IMPORTS (must live here, NOT in pack.toml — F3)
# Verification: harvest-verified (F3; city.toml.example:15-16)
# ─────────────────────────────────────────────────────────────────────────────
[defaults.rig.imports.gastown]
source = "github.com/gastownhall/gascity.git//examples/gastown/packs/gastown"
# Every registered rig automatically imports the gastown rig-scoped agents
# (witness, refinery, polecat). Do NOT re-import gastown in pack.toml if it
# is already imported there (duplicate → startup refusal — F3).

# ─────────────────────────────────────────────────────────────────────────────
# HEALTH-PATROL / CONTROLLER LOOP
# Verification: harvest-verified (field names present in prototype — city.toml.example:18-30)
# ─────────────────────────────────────────────────────────────────────────────
[daemon]
patrol_interval  = "30s"     # reconciler tick cadence
max_restarts     = 5         # crash-loop quarantine threshold
restart_window   = "1h"      # window for max_restarts count
shutdown_timeout = "10s"     # graceful-stop before SIGKILL
wisp_gc_interval = "5m"      # closed-wisp reaper cadence
wisp_ttl         = "30m"     # TTL for ephemeral molecules (wisps)
formula_v2       = true      # opt-in to graph.v2 formula execution

# ─────────────────────────────────────────────────────────────────────────────
# BEAD STORE
# Use "bd" (Dolt-backed, prototype default) or "file" for a simpler Phase-0.
# Verification: harvest-verified ("bd" in prototype — city.toml.example:32-36 / F9)
# ─────────────────────────────────────────────────────────────────────────────
[beads]
provider = "bd"
# "file" is also valid and simpler for Phase-0; "bd" requires a running dolt server.
# "exec:<script>" is also accepted [needs-pinned-gc-run (G11)]

# ─────────────────────────────────────────────────────────────────────────────
# ORDER SCHEDULING
# Verification: harvest-verified (max_timeout set in prototype — city.toml.example:38-40)
# ─────────────────────────────────────────────────────────────────────────────
[orders]
max_timeout = "10m"     # global order timeout
# skip = [...]          # order-skip filter list; omit to let all orders run

# ─────────────────────────────────────────────────────────────────────────────
# AGENT DECLARATIONS
# One [[agent]] block per named agent. Section presence = agent declared.
# Verification: harvest-verified
# ─────────────────────────────────────────────────────────────────────────────
[[agent]]
name     = "worker"
provider = "claude"
# env = { OTEL_EXPORTER_OTLP_ENDPOINT = "http://collector:4318" }
#    ^── per-agent env (Phase-1 addition; exact OTEL keys [needs-pinned-gc-run (G11)])

[[agent]]
name     = "judge"
provider = "claude"
# Per D-1: the judge runs on the same provider family as the worker.
# Separation is enforced by rig/role partition (C42), not by model family.

# ─────────────────────────────────────────────────────────────────────────────
# MESSAGING (Phase 1/2 addition — OMIT at Phase 0)
# Verification: [needs-pinned-gc-run (G11)] — not enabled in prototype city.toml
# ─────────────────────────────────────────────────────────────────────────────
# [mail]
# provider = "beadmail"   # default; "exec:<script>" also accepted

# ─────────────────────────────────────────────────────────────────────────────
# RIG PARTITION BLOCKS  (Phase-2 addition — D-31 requires ≥2 rigs)
#
# SPELLING NOTE [needs-pinned-gc-run (G11)]:
#   F1 (canonical ruling) = [[rig]] (singular)
#   prototype city.toml.example = [[rigs]] (plural)
#   Both spell it WITHOUT a `path` field — that is the invariant that holds.
#   The example below uses [[rigs]] to match the verified prototype; annotate
#   with the G11 flag so the operator knows to confirm spelling against a live gc.
#
# Verification: prefix mechanism harvest-verified (F10);
#               city.toml rig-block spelling [needs-pinned-gc-run (G11)]
# ─────────────────────────────────────────────────────────────────────────────

# WORKER RIG — implements code; read_partition MUST NOT include "scenarios" (holdout invariant)
[[rigs]]   # [needs-pinned-gc-run (G11)]: confirm whether [[rig]] or [[rigs]] is correct
name   = "worker"
prefix = "r1"
# REQUIRED: explicit prefix prevents auto-derived collision (F10).
# "rig1"/"rig2" both auto-derive "ri" and collide — always set prefix explicitly.
#
# read_partition  = "code"       # [needs-pinned-gc-run (G11)]: field exists per v4 spec (C42)
# write_partition = "code"       # [needs-pinned-gc-run (G11)]: field exists per v4 spec (C42)
# Holdout invariant: "scenarios" MUST NOT appear in read_partition of the worker rig.

# JUDGE RIG — evaluates completed work; read surface includes scenarios
[[rigs]]   # [needs-pinned-gc-run (G11)]: confirm spelling
name   = "judge"
prefix = "gp"
# read_partition  = "code,scenarios"   # [needs-pinned-gc-run (G11)]
# write_partition = "verdicts"          # [needs-pinned-gc-run (G11)]

# ─────────────────────────────────────────────────────────────────────────────
# FORMULAS (Phase 1 addition — OMIT at Phase 0)
# Section presence = C12 formula DAG composition ON.
# Verification: [needs-pinned-gc-run (G11)] — not enabled in prototype
# ─────────────────────────────────────────────────────────────────────────────
# [formulas]
# dir = "formulas"   # content is C12's domain; section presence is the flag

# ─────────────────────────────────────────────────────────────────────────────
# SERVICES (Phase 1 addition — OMIT at Phase 0)
# Section presence = external service wired in.
# Verification: [needs-pinned-gc-run (G11)]
# ─────────────────────────────────────────────────────────────────────────────
# [[service]]
# name = "langfuse"
# # endpoint / auth keys go here — treat as G37 risk (plaintext in TOML)

# DO NOT emit:
#   [autonomy]       — no such Gas City config block exists (see C56 for autonomy policy)
#   convergence.max_iterations  — not a real field (F2, harvest-verified non-existent)
```

---

## 4. `.gc/site.toml` — Machine-Local Rig Path Bindings

`.gc/site.toml` is written by the entrypoint at container-start time because only the
entrypoint knows runtime filesystem paths. It is **never committed** (add to `.gitignore`).

**D-32 invariant (holds regardless of `city.toml` spelling):** rig `path` belongs
**exclusively** here. `[[rigs]] path =` in `city.toml` is a PackV2 validation error (F1).

`.gc/site.toml` always uses **`[[rig]]` (singular)** with `name` + `path` — this is verified
verbatim in the prototype entrypoint.sh lines 70–76 (harvest-verified, F1).

```toml
# .gc/site.toml  — machine-local, entrypoint-written, NEVER committed
# Verification: harvest-verified (F1; entrypoint.sh:70-76)

workspace_name = "software-factory"

# WORKER RIG path binding
[[rig]]
name = "worker"
path = "/workspace/rigs/worker"

# JUDGE RIG path binding  (D-31: second rig required)
[[rig]]
name = "judge"
path = "/workspace/rigs/judge"
```

> **How the entrypoint writes this file** (based on prototype entrypoint.sh pattern):

```bash
# In entrypoint.sh (run at container-start):
mkdir -p "${CITY_DIR}/.gc"
cat > "${CITY_DIR}/.gc/site.toml" <<EOF
workspace_name = "software-factory"

[[rig]]
name = "worker"
path = "${RIGS_DIR}/worker"

[[rig]]
name = "judge"
path = "${RIGS_DIR}/judge"
EOF
```

---

## 5. `pack.toml` — Root Pack Manifest

`pack.toml` declares the pack identity and its imports. It is **version-controlled** and
must use `schema = 2` (PackV2). See [C02 — Pack ABI](../spec/C02-pack-extension-abi.md) for
the full tool-node ABI contract.

```toml
# pack.toml
# ─────────────────────────────────────────────────────────────────────────────
# PACK IDENTITY
# Verification: harvest-verified (pack/pack.toml in prototype)
# ─────────────────────────────────────────────────────────────────────────────
[pack]
name   = "software-factory"
schema = 2
# schema = 2 is REQUIRED (PackV2). gc REFUSES startup on wrong value.

# ─────────────────────────────────────────────────────────────────────────────
# PACK IMPORTS
# Source paths are resolved from gc's embedded FS at load time — no network.
# Verification: harvest-verified (F3; pack/pack.toml in prototype)
# ─────────────────────────────────────────────────────────────────────────────
[imports.gastown]
source = "github.com/gastownhall/gascity.git//examples/gastown/packs/gastown"
# gastown imports maintenance transitively. Do NOT also import maintenance here
# — it would duplicate the `dog` agent and refuse startup (F3).

# ─────────────────────────────────────────────────────────────────────────────
# TOOL-NODE DECLARATIONS (Phase-2 addition; one [[tool]] block per tool node)
# Verification: [needs-pinned-gc-run (G11)] — tool-node ABI; see C02
# ─────────────────────────────────────────────────────────────────────────────
# [[tool]]
# name = "inspect-eval"
# type = "subprocess"               # the only sanctioned kind (no Go fork)
# cmd  = "bin/inspect-eval"         # executable relative to pack root
# args = ["--bead-id", "{bead_id}"] # {placeholder} substituted from bead context
# work_partition = "code"           # [needs-pinned-gc-run (G11)]

# capability_id = "softwarefactory.v4.packs.inspect-eval"
# ^── C03 validates this against the CapabilityDescriptor registry (D-33 / XC-7 resolved)

# DO NOT put [defaults.rig.imports.*] here — PackV2 rejects it in a pack manifest.
# Those go in city.toml (F3, harvest-verified).
```

---

## 6. Provider / Session Bring-Up

### Pre-flight: pre-ack Claude onboarding dialogs

Claude presents three dialogs that hang an agent session if not pre-acknowledged (F12,
harvest-verified). The entrypoint must write `~/.claude.json` **before** `gc start`:

```bash
# In entrypoint.sh — write before exec gc start
cat > /root/.claude.json <<JEOF
{
  "firstStartTime": "2026-01-01T00:00:00.000Z",
  "hasCompletedOnboarding": true,
  "hasSeenWelcome": true,
  "theme": "dark",
  "bypassPermissionsModeAccepted": true,
  "projects": {
    "${CITY_DIR}":               {"hasTrustDialogAccepted": true, "bypassPermissionsModeAccepted": true},
    "${RIGS_DIR}/worker":        {"hasTrustDialogAccepted": true, "bypassPermissionsModeAccepted": true},
    "${RIGS_DIR}/judge":         {"hasTrustDialogAccepted": true, "bypassPermissionsModeAccepted": true}
  }
}
JEOF
```

> **Important:** this file is `~/.claude.json`, NOT `~/.claude/settings.json` (F12).
> Per-working-directory trust entries must cover every path an agent uses; the entrypoint
> writes them because paths are only known at runtime.

### Install pack imports

Pack imports must be materialized before the controller starts:

```bash
cd "${CITY_DIR}"
gc import install    # materializes .gc/imports/ and writes packs.lock
```

> `gc import install` is idempotent; skip if `packs.lock` already exists.

### Start the controller

```bash
# Phase-0 provider-kind = tmux (harvest-verified, F7)
# IS_SANDBOX=1 required for claude --dangerously-skip-permissions as root (F12)
IS_SANDBOX=1 gc start --foreground
```

`gc start --foreground` is the supervisor (PID 7 in-container; tini is PID 1 for zombie
reaping). It reconciles desired-vs-running agents, reaps dead sessions, and fires due orders
(harvest-verified, F6).

> **Verification status — tmux provider (F7 harvest-verified):** Phase-0 provider-kind is
> tmux. Each agent (`worker`, `judge`) runs as a separate interactive `claude` process in its
> own tmux pane within a single tmux server named after the city. The controller manages panes
> and restarts dead ones.
>
> **Verification status — `gc start` controller (F6 harvest-verified).**
>
> **Other provider kinds (`"subprocess"`, `"k8s"`, `"exec:<script>"`):**
> `[needs-pinned-gc-run (G11)]`

### Health check

```bash
gc status                  # controller running?
gc session list            # shows named agent panes (worker, judge)
```

---

## 7. Conformance Gate

Run the [Gas City conformance check](./gascity-conformance-check.md) **before** building
any downstream components. This is the gate that turns native claims into verified facts.

**Do not skip this gate.** Components that depend on Gas City native capabilities
(C19/C20 bead store, C04 sessions, C42 rig partitioning, C40 orders) are provisionally
unverified until their conformance test passes.

### Quick-start

```bash
# From inside the running container:
gc status                          # AC-C01-1: controller up
bd create --type test --rig worker test-bead    # smoke-signal bead round-trip
bd ls                               # bead appears?
gc sling <bead-id>                  # AC-C01-1: sling dispatches to worker pane
gc session list                     # worker pane spawned?
gc events --follow                  # event stream running?
```

### Test A — prevent-vs-detect (KEYSTONE)

Test A is the single most important test. Its outcome routes the D-30 binding gate:

```bash
# From worker rig context — attempt cross-rig bead access:
bd get gp-<some-judge-bead-id>     # Test A1 (bead-layer): exit code + data returned?
cat ../judge/some-file              # Test A2 (OS layer): exit code?
```

| Test A outcome | D-30 consequence |
|---|---|
| **PREVENT** — gc/bd/OS refuses out-of-prefix access | D-30 watcher not needed; D-20 fence is a real control; P2/P3b may proceed |
| **DETECT-ONLY / SILENT** — access permitted but logged, or no logging | D-30 watcher MUST be built before P2; `auto-001` binding gate triggered; unattended remains human-in-the-loop |

> **prevent-vs-detect-OPEN:** The enforcement strength of bead-prefix scoping is **not yet
> tested** (F10 marks this OPEN). The prototype never ran the end-to-end probe. The
> [D-23 spike protocol](./D-23-gas-city-spike-protocol.md) is the resolver. Until Test A
> runs, treat partition scoping as a convention (detect-only) — do NOT design P2 components
> that assume rig boundaries block access.

### Full battery

Run Tests A–G as described in the
[conformance check procedure](./gascity-conformance-check.md). All tests currently carry
status **OWED** (require Docker). Record results in the conformance check Results Record
before declaring the substrate READY.

---

## 8. Worked Minimal Example — 2-Rig City (Worker + Judge)

This section walks through bringing up a two-rig city, dispatching one bead, and observing
the result. It is the D-31 canonical example: worker-rig ≠ judge-rig, same city.

### File layout

```
/workspace/city/
├── city.toml           # versioned; from §3
├── pack.toml           # versioned; from §5
├── .gc/
│   └── site.toml       # machine-local; entrypoint-written; from §4
├── agents/
│   ├── worker/
│   │   └── prompt.template.md
│   └── judge/
│       └── prompt.template.md
└── packs.lock          # generated by gc import install
/workspace/rigs/
├── worker/             # worker rig working directory
└── judge/              # judge rig working directory
```

### Step 1 — Write config files

Produce the three files per §3, §4, §5.

```bash
mkdir -p /workspace/city /workspace/rigs/worker /workspace/rigs/judge
```

Write `city.toml` (from §3), `pack.toml` (from §5), and then run the entrypoint block to
write `.gc/site.toml` (from §4).

### Step 2 — Write minimal agent prompts

```bash
mkdir -p /workspace/city/agents/worker /workspace/city/agents/judge

cat > /workspace/city/agents/worker/prompt.template.md <<'EOF'
You are the Software Factory worker agent. Your bead id is {{ .BeadID }}.
Complete the task in the bead and mark it done.
EOF

cat > /workspace/city/agents/judge/prompt.template.md <<'EOF'
You are the Software Factory judge agent. Evaluate the worker's output.
EOF
```

### Step 3 — Pre-ack Claude dialogs and install imports

```bash
# Write ~/.claude.json (per §6)
IS_SANDBOX=1 \
CITY_DIR=/workspace/city \
RIGS_DIR=/workspace/rigs \
bash /path/to/entrypoint-pre-ack-snippet.sh

cd /workspace/city
gc import install
```

### Step 4 — Bring up the controller

```bash
cd /workspace/city
IS_SANDBOX=1 gc start --foreground &    # background for demo; use --foreground in production

# Wait for controller to settle:
sleep 5
gc status
```

Expected output: controller running; two rigs registered (`worker`, `judge`).

```bash
gc session list
# Expected: two panes — "worker" and "judge" — each running an interactive
# `claude` process in its own tmux pane.
```

> **Verification status — multi-rig session bring-up:** The `gc session list` output
> showing two panes from two `[[rig]]` blocks is `[needs-pinned-gc-run (G11)]` until the
> conformance check live-run confirms it (conformance test D).

### Step 5 — Dispatch a bead to the worker rig

```bash
# Create a bead in the worker partition
bd create --type task --rig worker --body '{"task": "Write hello-world.py"}' r1-task-001

# Verify the bead exists
bd get r1-task-001
# Expected: bead with `created_by` set (INV-3 attribution)

# Sling the bead to the worker agent
gc sling r1-task-001
# Expected: worker pane receives the bead; a new tmux pane or existing pane
# shows activity
```

> **Verification status — sling dispatch: harvest-verified (F5, F8).** `gc sling`
> dispatches a bead; worker pool `min=0` scales 0→1 on dispatch (spawns a new tmux pane).

### Step 6 — Observe the event stream

```bash
gc events --follow
# Expected: events flow showing bead creation, session start, attribution
```

> **Verification status — event stream: `[needs-pinned-gc-run (G11)]`.**
> The event stream was not exercised end-to-end in the prototype stand-up.
> Run conformance check Test G to verify.

### Step 7 — Cross-rig isolation check (preview of conformance Test A)

```bash
# From the worker rig's context — attempt to access the judge's bead namespace:
bd get gp-<any-judge-bead-id>
# Record: exit code, data returned (or refused), logged?
# This is Test A1 of the conformance check.
```

Record the outcome and route to D-30 per §7 above.

### D-31 confirmation

This example demonstrates ≥2 rigs (worker prefix `r1-`, judge prefix `gp-`) co-resident in
one city, with distinct path bindings in `.gc/site.toml` and distinct `[[rigs]]` blocks in
`city.toml`. The D-32 file-split is honoured: `path` appears only in `.gc/site.toml`.

---

## Config-Key Needs-G11 Summary

The following config keys require operator verification against a pinned `gc` install before
relying on them in production. Count: **12 keys / blocks marked needs-pinned-gc-run (G11)**.

| Key / Block | File | Reason |
|---|---|---|
| `city.toml` rig-block spelling (`[[rig]]` vs `[[rigs]]`) | city.toml | F1 vs prototype diverge |
| `[[rig]] read_partition` | city.toml | Named in v4 spec (C42); not in prototype example |
| `[[rig]] write_partition` | city.toml | Named in v4 spec (C42); not in prototype example |
| `[[agent]] env = { … }` (exact OTEL keys) | city.toml | Key names not verified end-to-end |
| `[agent_defaults]` (provider, wake_mode, etc.) | city.toml | Some fields parsed-but-not-applied |
| `[mail] provider = "beadmail"` | city.toml | Not enabled in prototype city.toml |
| `[events] provider` | city.toml | Not exercised end-to-end |
| `[formulas]` (section + content) | city.toml | Not enabled in prototype |
| `[[service]] name` + endpoint | city.toml | Schema unverified (D-23 spike Test B target) |
| `[[tool]] type = "subprocess"` + `cmd` / `args` / `work_partition` | pack.toml | Tool-node ABI; see [C02](../spec/C02-pack-extension-abi.md) |
| `[beads] provider = "exec:<script>"` | city.toml | Alternative provider; only `"bd"` verified |
| `[session] provider` non-tmux values (`"k8s"`, `"subprocess"`, `"exec:<script>"`) | city.toml | Phase-0 kind = tmux is verified; others not |

---

## Error Quick-Reference

| Symptom | Likely cause | Fix |
|---|---|---|
| `gc start` exits non-zero with config-validation error | Misplaced key (e.g. `path=` in city.toml rig block) | Move `path` to `.gc/site.toml`; see E-C01-06 |
| `claude` refuses to start; permissions error | `IS_SANDBOX=1` not set | Set in env; see E-C01-04 |
| Agent pane hangs at dialog | `~/.claude.json` not pre-acked | Write the pre-ack file per §6; see E-C01-05 |
| `gc start` refuses with duplicate-agent error | `gastown` imported directly in city.toml AND transitively via pack | Remove direct import; see E-C03-01 / F3 |
| `dolt push` fails | `DOLT_REF` not set to `refs/heads/dolt-data` | Set env var; see E-C01-10 |
| Build error: "requires go 1.26.3 or newer" | Wrong Go version on PATH | Install Go 1.26.3; see E-C01-02 |
| Bead prefix collision at startup | Auto-derived prefix from rig names clashes | Set explicit `prefix =` in every `[[rig]]`/`[[rigs]]` block; see F10 |

---

## References

- [Config anchor — single source of truth for keys](./gascity-config-anchor.md)
- [Conformance check procedure](./gascity-conformance-check.md)
- [D-23 substrate harvest (F1–F12)](./D-23-substrate-harvest.md)
- [D-23 spike protocol](./D-23-gas-city-spike-protocol.md)
- [C01 — Gas City runtime substrate spec](../spec/C01-gas-city-substrate.md)
- [C02 — Pack and tool-node ABI spec](../spec/C02-pack-extension-abi.md)
- [C03 — Layered config / feature-flag model](../spec/C03-config-feature-flags.md)
- [C04 — Session and provider runtime](../spec/C04-session-provider.md)
- [C42 — Rig / agent-role partitioning](../spec/C42-rig-partitioning.md)
