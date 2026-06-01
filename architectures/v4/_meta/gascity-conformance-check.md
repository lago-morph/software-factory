# Gas City Conformance Check — Native-Claims Verification Procedure

**Purpose.** Verify, against a real running `gc`, every "Gas City does X natively" claim that v4
Sweep-2 components are about to be built on. This procedure is the gate between the D-23 spike
protocol (which defines the tests) and the actual construction of Sweep-2 components. Nothing in
Sweep-2 that depends on a Gas City native capability should be built until the relevant test here
has been run and its outcome recorded.

**Live-run status: OWED — requires a Docker-capable environment.**
The D-23 spike protocol was authored but not executed (per [HANDOFF.md §0.3.5](./HANDOFF.md)). This
procedure is a fully runnable operationalization of that protocol: exact commands, expected outputs,
and explicit PASS/FAIL criteria. Execute it the moment a Docker environment is available. Until then,
every test in this document has status OWED and every downstream component that depends on a native
claim must treat that claim as UNVERIFIED.

**What blocks if this procedure is skipped.** The keystone is Test A (prevent-vs-detect). Its
outcome determines whether the D-30 blocking watcher must be built — a decision that reshapes the
P2/P3b security architecture. Running Test A is not optional before any P2 component design is
finalized. Tests B and C discharge OQs that gate C44 twin design and C40 Orders durability
design respectively. Skipping this procedure leaves all three component tracks building on
unverified foundations.

**Source.** This procedure operationalizes
[D-23-gas-city-spike-protocol.md](./D-23-gas-city-spike-protocol.md) section by section.
Ground-truth build facts come from [D-23-substrate-harvest.md](./D-23-substrate-harvest.md) (F1–F12,
`lago-morph/gascity-prototype@b14c278`). Config keys cross-reference
[gascity-config-anchor.md](./gascity-config-anchor.md); where a key is named below it is marked
`[see config anchor]`.

---

## Preconditions

### Environment

| Requirement | Detail |
|---|---|
| Docker daemon | Running on the host; `docker compose` available. All tests run inside the container — not on the host directly. |
| Go toolchain | **Go 1.26.3** — this is the version the prototype was built against (F-context in [substrate harvest](./D-23-substrate-harvest.md) §build facts; `go.mod` is authoritative — run `head -5 /tmp/gascity/go.mod` to confirm before downloading a Go tarball). If `go.mod` says something different, use what `go.mod` says. |
| Host tools | `git`, `curl`, `make`, `tar`. No internet access needed inside the container (all binaries are pre-staged — see §Binary staging below). |
| Auth | Either `ANTHROPIC_API_KEY=sk-ant-…` (laptop) or `CLAUDE_CODE_OAUTH_TOKEN` from `/home/claude/.claude/remote/.oauth_token` (Anthropic sandbox). |
| OS audit | For Test A2, the host running the conformance check should NOT have additional seccomp or AppArmor profiles applied beyond Docker defaults, so the test measures `gc`'s own enforcement rather than ambient host policy. Note any non-default Docker security options in the run record. |

### Pinned commit

All tests must run against:

```
Prototype repo:  lago-morph/gascity-prototype   branch claude/great-pascal-RUfkN   commit b14c278
Upstream gc SDK: gastownhall/gascity             commit 183897e  (post-v1.0.0, PackV2)
```

Do not run against a different branch or commit without updating this document and re-recording all
results. Prototype sources and upstream `gc` must match (the prototype's `go.mod` pins the upstream
SDK version).

### Build procedure

Follow [D-23 spike protocol §1](./D-23-gas-city-spike-protocol.md#1-obtain-and-build-gc) exactly.
Abbreviated summary:

```bash
# 1. Clone
git clone https://github.com/lago-morph/gascity-prototype.git
cd gascity-prototype
git checkout claude/great-pascal-RUfkN

# 2. Stage binaries on the HOST (sandbox TLS-inspection proxy blocks in-container downloads — F12
#    context in substrate harvest; spike protocol §1 "Stage binaries")
mkdir -p build-context
# Stage dolt, bd, gc (built from source), node22, claude-code into build-context/
# See spike protocol §1 for the full curl/make commands.
# IMPORTANT: confirm Go version from go.mod before downloading the Go tarball.

# 3. Build the image
docker build -t gascity-prototype:latest -f build-context/Dockerfile build-context/

# 4. Configure auth (.env) and start
#    Laptop: cp .env.example .env && edit ANTHROPIC_API_KEY
#    Sandbox: use the sandbox .env form from spike protocol §1 with network_mode: host
docker compose up -d   # sandbox: docker compose -f docker-compose.yml -f docker-compose.sandbox.yml up -d
```

### Verify minimal stand-up before running tests

These checks are prerequisites; if any fails, diagnose before proceeding to the test battery.

```bash
# Controller is up and all named gastown agents are running
docker exec gascity-prototype gc status
# Expected: mayor (coordinator), deacon (health-patrol), boot (bootstrap), worker pool,
#           rig1 observer, control-dispatchers — all running or idle.

# Sessions visible
docker exec gascity-prototype gc session list

# Bead store accessible
docker exec gascity-prototype bash -lc 'cd /workspace/rigs/rig1 && bd ls'
# Expected: empty or minimal list, no error.

# Round-trip smoke signal (end-to-end prerequisite for all tests below)
docker exec gascity-prototype bash -lc \
  'cd /workspace/rigs/rig1 && bd create "conformance-smoke-signal: bead store working"'
# Note returned bead ID (will be r1-<hash>). Confirm:
docker exec gascity-prototype bash -lc 'cd /workspace/rigs/rig1 && bd ls'
```

If `gc status` shows all agents and `bd ls` returns without error, the minimal stand-up is
confirmed. Proceed to the test battery.

---

## Test Battery

---

### Test A — Prevent-vs-Detect (KEYSTONE)

**Purpose.** Determine whether `gc` (and/or the OS sandbox) **prevents** out-of-partition access at
tool-call or process boundary — refusing the call and returning a non-zero exit with no data — or
merely permits and logs the access after the fact. This is the test that decides whether the D-30
blocking watcher must be built.

> **D-30 operator-adopted prevent-gate (verbatim binding):**
> "unattended operation (P2) and self-modification (P3b) require the substrate to BLOCK (prevent at the tool-call/process boundary) — not merely detect — out-of-boundary access on the relevant blast-radius face."

The D-30 watcher's design is **deferred** until this test runs. Test A is the go/no-go gate for
that design decision. Do not design or build the watcher before running this test.

**Discharges:** C34:OQ-C34-1 and C43:OQ-C43-1 (these are the same enforce-or-audit question seen
from C34 and C43 respectively; the same test run closes both).

Test A has two sub-tests because the question spans two enforcement layers:
- **A1** — the bead/tool layer (what `gc`/`bd` enforces at tool-call time)
- **A2** — the OS/Bash layer (what a claude process can do with raw shell commands, potentially
  bypassing the bead trail entirely; per [D-23 spike protocol §3](./D-23-gas-city-spike-protocol.md#3-test-a--prevent-vs-detect-the-test), VERDICT.md §6 item 8)

---

#### Test A1 — Bead/tool-layer cross-partition access

**Setup.** Create bead targets in rig2 scope and city scope. Note the returned IDs — substitute the
actual values for `r2-TARGET` and `gp-TARGET` in the probe commands.

```bash
# Create an r2-scoped target bead (from rig2's directory):
docker exec gascity-prototype bash -lc \
  'cd /workspace/rigs/rig2 && bd create "conformance-target-r2: bead for cross-partition probe"'
# Record returned ID as r2-TARGET

# Create a city-level (gp-scoped) target bead:
docker exec gascity-prototype bash -lc \
  'cd /workspace/city && bd create "conformance-target-gp: city-level bead for probe"'
# Record returned ID as gp-TARGET
```

**Probe A1a — rig1-scoped read of an r2- bead (cross-rig read):**

```bash
docker exec gascity-prototype bash -lc \
  'cd /workspace/rigs/rig1 && bd get r2-TARGET'
# Capture: stdout verbatim, stderr verbatim, exit code ($?)
```

**Probe A1b — rig1-scoped read of a gp- bead (cross-tier read):**

```bash
docker exec gascity-prototype bash -lc \
  'cd /workspace/rigs/rig1 && bd get gp-TARGET'
# Capture: stdout verbatim, stderr verbatim, exit code
```

**Probe A1c — rig1-scoped attempt to CREATE an r2- prefixed bead (cross-partition write):**

```bash
# Try --prefix flag first; if unsupported, try the inline-prefix form:
docker exec gascity-prototype bash -lc \
  'cd /workspace/rigs/rig1 && bd create --prefix r2 "conformance-create-attempt: rig1 writing r2"'
# If --prefix is rejected as unknown flag, use:
docker exec gascity-prototype bash -lc \
  'cd /workspace/rigs/rig1 && bd create "r2-conformance-create-attempt: rig1 writing r2 prefix"'
# Capture: stdout, stderr, exit code
```

**Check event trail for all A1 probes:**

```bash
docker exec gascity-prototype bash -lc \
  'gc events --since=5m | grep -i "r2-TARGET\|denied\|refused\|audit\|scope\|prefix"'
# Capture: whether any event was emitted for the cross-partition accesses
```

**Command(s):** A1a + A1b + A1c probes above, plus the event-trail check.

**Expected output (PREVENT path):**
- `bd get r2-TARGET` exits non-zero; stderr contains "access denied", "out of scope", "prefix
  mismatch", or similar. No bead data on stdout.
- `bd create --prefix r2` (or inline-r2 form) exits non-zero with a scope/prefix error. No bead
  created with r2 prefix.

**Expected output (DETECT-ONLY path):**
- `bd get r2-TARGET` exits 0; bead data printed to stdout. Access may or may not appear in `gc events`.
- `bd create` with r2 prefix exits 0; bead is created. Access may appear in `gc events`.

**PASS criterion (PREVENT):** All cross-partition probes exit non-zero with no data returned to
the caller. The bead layer enforces partition at the call boundary.

**FAIL criterion (DETECT-ONLY):** Any cross-partition probe exits 0 and returns data or creates a
bead. The bead layer is advisory.

**FAIL criterion (SILENT):** Any cross-partition probe exits 0, returns data, AND produces no entry
in `gc events` or any audit trail. Worst case — neither prevention nor detection.

**What each outcome implies:**

| A1 Outcome | Implication |
|---|---|
| **PREVENT** | D-20's "fence pulled to P2 precondition" holds as a real control. C43's boundary-typing is an enforcement control, not a metadata declaration. C34's holdout boundary is enforced at dispatch time. D-30 watcher is not needed for the bead/tool layer. Architecture proceeds as specified. |
| **DETECT-ONLY** | C43's typing is advisory; bead-layer is an audit mechanism, not a hard gate. A compensating prevent layer at the bead/tool level (e.g., OPA policy wrapping `bd` calls) must be evaluated before P2. D-30 watcher **MUST be built** for the bead layer. |
| **SILENT** | `auto-001` binding gate triggered. Before P2: add a compensating prevent layer (OPA policy, Linux namespace, or seccomp restricting `bd` cross-prefix writes) **or** formally descope the unattended-autonomy claim. This is a go/no-go gate, not a noted caveat (spike protocol §6 "auto-001 binding gate"). |

**Discharges:** C34:OQ-C34-1 (bead layer), C43:OQ-C43-1 (same question from C43 angle).

---

#### Test A2 — OS/Bash-layer cross-partition filesystem access

**Purpose.** A worker whose `cwd` is `/workspace/rigs/rig1` may be able to read rig2's files and
city config using raw shell commands — which bypass the bead trail entirely. This probes whether
the OS provides a second enforcement layer, or whether the bead layer is the only gate (and is
therefore bypassable by any agent that can execute a shell command).

**Setup.** No additional setup beyond the minimal stand-up. The probes are read-only at the
filesystem level and do not create any artifacts.

**Probe A2a — cross-rig filesystem read:**

```bash
docker exec gascity-prototype bash -lc \
  'cd /workspace/rigs/rig1 && cat ../rig2/README.md'
# Capture: stdout (data printed Y/N), exit code
```

**Probe A2b — city-config read from rig1 context:**

```bash
# First confirm the city.toml path in the layout:
docker exec gascity-prototype bash -lc 'ls /workspace/city/'

# Then probe:
docker exec gascity-prototype bash -lc \
  'cd /workspace/rigs/rig1 && cat /workspace/city/city.toml'
# A worker reading the city config at OS level — should this be prevented?
# Capture: stdout (data printed Y/N), exit code
```

**Probe A2c — check whether A2a/A2b reads appeared in any audit trail:**

```bash
docker exec gascity-prototype bash -lc \
  'gc events --since=5m | grep -i "cat\|read\|rig2\|city.toml\|filesystem"'
# Capture: events returned Y/N
```

**Command(s):** A2a + A2b + A2c probes above.

**Expected output (PREVENT path):**
- `cat ../rig2/README.md` exits non-zero (permission denied, chroot restriction, namespace
  confinement). No data returned.
- `cat /workspace/city/city.toml` exits non-zero. No data returned.

**Expected output (DETECT path):**
- Reads succeed (data printed, exit 0) AND entries appear in `gc events` or OS audit log.

**Expected output (SILENT path):**
- Reads succeed, exit 0, no entries in any trail.

**PASS criterion (PREVENT):** Both filesystem probes exit non-zero. OS layer enforces partition
independently of the bead trail.

**FAIL criterion (DETECT):** Reads succeed but appear in `gc events`. OS layer detects but does
not prevent; C34's audit boundary covers OS reads.

**FAIL criterion (SILENT):** Reads succeed with no trail entry. VERDICT.md §6 item 8 confirmed —
C34 is not an OS audit boundary for raw Bash reads; agents could read cross-rig files and city
secrets without any detection. Compensating control (e.g., Linux user-namespace isolation per rig,
or a `claude` process wrapper that restricts `cwd`-relative parent traversal) required before P2.

**What each outcome implies:**

| A2 Outcome | Implication |
|---|---|
| **PREVENT at OS level** | Combined with A1 PREVENT: no compensating layer needed. D-30 watcher not required. |
| **DETECT at OS level** | OS layer is advisory. C34's audit boundary works for OS reads but is not a gate. D-30 watcher scope expands to cover OS-level reads if A1 is also DETECT-ONLY. |
| **SILENT** | Most severe outcome. C34 is not an OS audit boundary for raw reads. Any agent with shell access can read cross-rig files and the city config without leaving a trace. D-30 watcher **MUST be built** and must operate at the OS level (namespace/seccomp), not only at the bead/tool layer. P2 cannot proceed without this control. |

**Discharges:** C34:OQ-C34-1 (OS layer sub-question).

---

### Test B — `[[service]]` / Twin Semantics

**Purpose.** Verify that `gc` honors a `[[service]]` block at runtime and that the twin-substitution
assumption (each v4 twin maps to a `[[service]]` registration that controls record/replay/stateful
mode) is grounded in observable `gc` behavior, not speculation.

**Discharges:** C44:OQ-4 (per-twin `[[service]]` TOML + fixture/cassette schema), C44:OQ-2 partial
(three-mode precedence: replay → stateful → OpenAPI).

**Setup.** No new artifacts; the running city from the minimal stand-up is sufficient. If the city
`city.toml` already contains a `[[service]]` block [see config anchor for canonical key spelling],
observe its effect directly. If not, the probe commands will surface what `gc` knows about the
`[[service]]` schema.

**Commands:**

```bash
# 1. Inspect existing [[service]] declarations in the running config:
docker exec gascity-prototype bash -lc \
  'grep -A 20 "\[\[service\]\]" /workspace/city/city.toml 2>/dev/null || echo "NO [[service]] in city.toml"'
docker exec gascity-prototype bash -lc \
  'find /workspace -name "pack.toml" | xargs grep -l "service" 2>/dev/null'
docker exec gascity-prototype bash -lc 'cat /pack/pack.toml'

# 2. What does gc know about registered services?
docker exec gascity-prototype gc service list 2>&1 || echo "gc service list: not a command"
docker exec gascity-prototype gc help 2>&1 | grep -i "service\|twin\|replay\|stateful"
docker exec gascity-prototype gc help service 2>/dev/null || echo "no gc service subcommand"

# 3. Inspect the [[service]] schema via help or TOML parse errors:
docker exec gascity-prototype bash -lc \
  'cd /workspace/city && gc service register --help 2>&1 | head -30' || echo "no gc service register"
docker exec gascity-prototype bash -lc \
  'gc help session 2>&1; gc help sling 2>&1; gc help order 2>&1' | head -80

# 4. Check whether gastown pack defines any [[service]] blocks:
docker exec gascity-prototype bash -lc \
  'find /usr/local/lib /usr/local/share /root -name "*.toml" 2>/dev/null \
   | xargs grep -l "\[\[service\]\]" 2>/dev/null | head -5'
docker exec gascity-prototype bash -lc \
  'gc pack inspect gastown 2>/dev/null || gc pack list 2>/dev/null'

# 5. Is a [[service]] registration visible as a named pane?
docker exec gascity-prototype gc session list
docker exec gascity-prototype gc status
```

**Expected output (PASS).** `gc` has a recognized `[[service]]` block schema (visible in `gc help`
output, TOML parse error messages, or pack inspection). The schema includes fields such as `name`,
`mode` (or equivalent distinguishing replay / stateful / openapi modes), and a fixture/cassette path
reference. If a `[[service]]` is active, a corresponding entry appears in `gc session list` or
`gc status`. The twin mode is identifiable from the config.

**PASS criterion:** `gc` demonstrates that it reads, registers, and acts on a `[[service]]` block
at runtime. The TOML fields accepted are observable. At least one twin mode (`record`, `replay`,
`stateful`, or `openapi`) is confirmed to exist at the schema level.

**FAIL criterion:** `gc help` contains no mention of `service`, `twin`, `replay`, or `stateful`.
No `[[service]]` blocks are found in any pack or city config. `gc` behavior is inconsistent with
the assumption that twin substitution is a `gc` native capability.

**What each outcome implies:**

| B Outcome | Implication |
|---|---|
| **PASS — schema confirmed** | C44's per-twin packaging design can proceed. Authors must bind C44:OQ-4 fields to the observed schema (not to inferred field names). The three-mode precedence (C44:OQ-2) should be recorded from the observed `gc help` output. |
| **FAIL — `[[service]]` not in `gc` schema** | C44's twin design is speculative with respect to the actual `gc` schema. C44:OQ-4 must be re-authored against observed `gc` capabilities before any implementation. The per-twin packaging design is blocked. |

**Discharges:** C44:OQ-4, C44:OQ-2 (partial).

---

### Test C — Orders Durability (Crash / Resume)

**Purpose.** Verify that Gas City Orders survive (a) an in-process `gc` controller crash and
restart, and (b) a full container death and restart. This determines whether the bead/Orders
mechanism alone is sufficient for unattended P11 loops, or whether a Temporal-class external
durability layer is required.

**Discharges:** C40:OQ-1 (Orders-insufficiency → Temporal trigger; falsifiable condition),
C40:OQ-3 (crash-resume granularity, idempotency, default retry bound).

**Setup.** Create a durable bead that represents a long-running, multi-step order. Note the returned
ID as `r1-DUR`.

```bash
docker exec gascity-prototype bash -lc \
  'cd /workspace/rigs/rig1 && bd create "conformance-durability: multi-step durability probe"'
# Record returned ID as r1-DUR

# Confirm the bead is open and the coordinator has seen it:
docker exec gascity-prototype bash -lc 'cd /workspace/rigs/rig1 && bd get r1-DUR'
# Start event follow in background (separate terminal or capture after):
docker exec gascity-prototype gc events --follow &
```

---

#### Test C1 — In-process controller crash (C40:OQ-3a)

**Commands:**

```bash
# Identify the gc controller PID:
docker exec gascity-prototype bash -lc 'pgrep -a gc'

# Send SIGKILL to the controller (not to the container):
docker exec gascity-prototype bash -lc 'kill -9 $(pgrep -f "gc start")'

# Wait for tini/PID1 to restart gc (per F6, gc runs under tini as PID 7):
docker exec gascity-prototype bash -lc 'sleep 5 && gc status'

# Check bead state after restart:
docker exec gascity-prototype bash -lc 'cd /workspace/rigs/rig1 && bd get r1-DUR'

# Check for resume/restart events:
docker exec gascity-prototype bash -lc 'gc events --since=5m | grep -i "resume\|restart\|r1-DUR"'
```

**Expected output (PASS):** `gc status` shows agents running again within a few seconds of the
kill. `bd get r1-DUR` shows the bead in the same state it was in before the kill (or advanced to a
checkpoint boundary). `gc events` shows a resume or restart event referencing the order.

**PASS criterion:** Bead state is preserved through the controller crash. Resume picks up at or
after the last completed step boundary (not from zero). The event trail shows a controlled restart.

**FAIL criterion (re-start from zero):** Bead state is preserved but the order re-executes from the
beginning, not from the last step. Resume granularity is order-level, not step-level.

**FAIL criterion (bead lost):** `bd get r1-DUR` returns an error or shows no record after the
restart. The controller crash destroyed in-flight state.

---

#### Test C2 — Container death and full restart (C40:OQ-3b)

**Commands:**

```bash
# While r1-DUR is open:
docker compose down

# Restart the container:
docker compose up -d   # sandbox: add -f docker-compose.sandbox.yml

# Wait for entrypoint re-clone of rigs + beadstore (watch logs):
docker compose logs --tail=80 city

# Verify bead survived container death:
docker exec gascity-prototype bash -lc 'cd /workspace/rigs/rig1 && bd ls'
docker exec gascity-prototype bash -lc 'cd /workspace/rigs/rig1 && bd get r1-DUR'
```

**Expected output (PASS):** `bd get r1-DUR` returns the bead record with its last-known state.
The dolt beadstore was pushed before the kill and the entrypoint re-cloned it; bead state survived.

**PASS criterion:** Bead state (status, last-step marker) is present after container restart and
matches the pre-death state. The dolt push cadence (periodic, not on-demand) means some in-flight
progress may be lost, but the bead RECORD survives.

**FAIL criterion (ephemeral):** `bd get r1-DUR` fails or returns a blank/initial record. The bead
store was not persisted before container death. Orders are ephemeral to container restarts. This
triggers C40:OQ-1: "any container restart during a multi-step order results in lost progress" is the
confirmed falsifiable trigger for the Temporal integration requirement.

---

#### Test C3 — Default retry bound (C40:OQ-3c)

**Commands:**

```bash
# Create a deliberately unresolvable bead (will fail repeatedly):
docker exec gascity-prototype bash -lc \
  'cd /workspace/rigs/rig1 && bd create "conformance-retry: intentionally unresolvable XYZZY-NO-MATCH"'
# Record returned ID as r1-RETRY

# Watch retry events (let run for a few minutes):
docker exec gascity-prototype bash -lc \
  'gc events --follow | grep -i "retry\|fail\|error\|XYZZY\|r1-RETRY"'

# After the order stalls or errors out:
docker exec gascity-prototype bash -lc 'cd /workspace/rigs/rig1 && bd get r1-RETRY'
```

**Expected output (PASS):** `gc events` shows retry attempts followed by a terminal failure or
"max retries exceeded" state. The bead transitions to an error/failed state. The retry count is
observable from the events.

**PASS criterion:** A finite retry ceiling is observed (exact count recorded). C40:OQ-3 retry
bound = known.

**FAIL criterion (unbounded):** Events show repeated retries with no terminal state within a
reasonable observation window (10+ minutes). Retry bound is unknown or effectively infinite.
C40:OQ-1 partial: set the trigger condition to "observed stall without terminal state."

**What each C outcome implies:**

| C Sub-test | Outcome | Implication |
|---|---|---|
| C1 (controller kill) | Bead preserved, step-boundary resume | C40:OQ-3 granularity = step. No Temporal dependency from controller crash alone. |
| C1 (controller kill) | Bead preserved, re-execute from start | C40:OQ-3 granularity = order. Idempotency required for order definitions. |
| C1 (controller kill) | Bead lost | Dolt SQL state not flushed to disk on kill. High-durability mode needed even for in-process crashes. |
| C2 (container kill) | Bead preserved | dolt push cadence is sufficient for container-restart durability. C40:OQ-1 trigger NOT met. |
| C2 (container kill) | Bead lost (ephemeral) | Orders durability ceiling = dolt push cadence. C40:OQ-1 trigger: any container restart during multi-step order causes lost progress. Temporal integration warranted for P11 unattended loops longer than the push cadence. |
| C3 (retry) | Finite bound observed | C40:OQ-3 retry bound = N (record the count). |
| C3 (retry) | No bound observed | Add explicit retry ceiling to C40 spec. C40:OQ-1 partial trigger = "observed stall." |

**Discharges:** C40:OQ-1, C40:OQ-3.

---

### Test D — Rig Partitioning Honored by `gc status` / Worker Dispatch

**Purpose.** Verify that the bead-prefix scoping mechanism (F10 in substrate harvest) is correctly
applied at worker dispatch time: a worker dispatched to rig1 actually has its `cwd` set to
`/workspace/rigs/rig1/` and can only create beads with the `r1-` prefix. This closes the operational
question of whether partition assignment is honored by the controller, not just declared in config.

**Discharges:** C42 rig-partitioning operational claim; supports C34:OQ-C34-1 (bead-layer
partitioning is plumbed end-to-end).

**Setup.** Requires a worker dispatch. Use the smoke-signal bead from the minimal stand-up, or
create a new one.

```bash
# Create a bead to trigger dispatch:
docker exec gascity-prototype bash -lc \
  'cd /workspace/rigs/rig1 && bd create "conformance-dispatch: rig partition assignment probe"'
# Record ID as r1-DISPATCH

# Observe which worker pane picks it up and its cwd:
docker exec gascity-prototype gc events --follow | grep -i "r1-DISPATCH\|dispatch\|worker\|sling"

# After dispatch is visible, check the worker session's cwd:
docker exec gascity-prototype gc session list
docker exec gascity-prototype bash -lc \
  'gc session list --json 2>/dev/null | python3 -m json.tool | grep -A3 "worker\|cwd\|rig"'
```

**Expected output (PASS):** The event log shows the coordinator dispatching `r1-DISPATCH` to a
worker. `gc session list` shows the worker pane with `cwd = /workspace/rigs/rig1/` (or equivalent).
The bead created by the worker during processing has the `r1-` prefix.

**PASS criterion:** Worker's `cwd` is rig1-scoped and any beads it creates carry the `r1-` prefix.
The controller honored the rig partition in dispatch.

**FAIL criterion:** Worker `cwd` is not rig-scoped (e.g., `/workspace/` or `/`), OR a worker
dispatched for rig1 creates beads with a non-`r1-` prefix. Partition assignment is not enforced
at dispatch time.

**Discharges:** C42 rig-partitioning (operational dispatch path).

---

### Test E — `created_by` Attribution Stamped on Beads

**Purpose.** Verify that beads carry a `created_by` field (or equivalent identity attribution)
that identifies the agent role that created them. This is the C41 attribution claim: the bead store
is the audit trail for agent identity, and that claim is only meaningful if attribution is stamped at
write time.

**Discharges:** C41 identity attribution (bead-store attribution field present and populated).

**Setup.** Use beads already created during earlier tests; alternatively create a fresh one.

```bash
# Inspect an existing bead for attribution fields:
docker exec gascity-prototype bash -lc \
  'cd /workspace/rigs/rig1 && bd get r1-<any-existing-bead-id> --format json 2>/dev/null \
   || bd get r1-<any-existing-bead-id>'

# If bd supports JSON output, pipe through jq or python3 -m json.tool:
docker exec gascity-prototype bash -lc \
  'cd /workspace/rigs/rig1 && bd ls --format json 2>/dev/null | python3 -m json.tool | head -60'

# Inspect the dolt schema directly to see all columns:
docker exec gascity-prototype bash -lc \
  'cd /workspace/rigs/rig1 && bd schema 2>/dev/null || echo "bd schema: not a command"'

# Check via dolt SQL directly (dolt runs a local SQL server per F9):
docker exec gascity-prototype bash -lc \
  'dolt --help | grep -i "sql\|query" | head -5'
docker exec gascity-prototype bash -lc \
  'cd /workspace/city/.gc/beadstore 2>/dev/null && dolt sql -q "DESCRIBE beads" 2>/dev/null \
   || echo "direct dolt access path unclear — check gc status for beadstore port"'
```

**Expected output (PASS):** A bead record includes a `created_by`, `author`, `agent`, or equivalent
field that is populated with an agent identifier (role name or session ID). The field is non-null
for every bead inspected.

**PASS criterion:** Attribution field is present and populated in the bead schema. C41's audit-trail
claim is grounded.

**FAIL criterion:** No attribution field is present in the bead schema, or the field exists but is
always null. C41's attribution claim is unverified; the bead store is not a reliable audit trail for
agent identity.

**Discharges:** C41 identity attribution operational claim.

---

### Test F — Bead-Prefix Scoping and Explicit Prefix Config

**Purpose.** Verify that the explicit `prefix` config key in `city.toml` [see config anchor §3]
correctly avoids rig-name collision (F10 in substrate harvest: `rig1` and `rig2` both auto-derive
prefix `"ri"` and collide without explicit overrides) and that prefix assignment is visible in
`gc status` output.

**Discharges:** C42:OQ-4 (partial — prefix config operational), F10 collision-avoidance fact.

**Commands:**

```bash
# Inspect the city.toml for explicit prefix settings:
docker exec gascity-prototype bash -lc \
  'grep -A5 "prefix" /workspace/city/city.toml'

# Confirm the running prefixes match the config:
docker exec gascity-prototype bash -lc 'gc status --verbose 2>/dev/null || gc status'

# Verify that beads created from each rig carry the correct prefix:
docker exec gascity-prototype bash -lc 'cd /workspace/rigs/rig1 && bd ls | head -10'
docker exec gascity-prototype bash -lc 'cd /workspace/rigs/rig2 && bd ls | head -10'
# r1- prefix expected for rig1 beads; r2- prefix expected for rig2 beads
```

**Expected output (PASS):** `city.toml` contains `prefix = "r1"` and `prefix = "r2"` (or
equivalent explicit overrides) for rig1 and rig2 respectively. Beads listed under each rig
directory carry the matching prefix. No `ri-` prefixed beads appear (the collision form).

**PASS criterion:** Explicit prefix config is present and effective. No prefix collision is
observed in the running city.

**FAIL criterion:** No explicit prefix config is present and `bd ls` shows `ri-` prefixed beads
from both rigs (collision), OR only one rig's beads appear. Prefix collision is active; the
`city.toml` as deployed does not apply the F10 fix.

**Discharges:** C42 bead-prefix scoping (F10 operational confirmation).

---

### Test G — Reconciler Convergence (gc Desired-State Loop)

**Purpose.** Verify that the `gc` reconciler (F6: `gc start --foreground` reconciles desired-vs-
running, reaps dead sessions, fires due orders) converges correctly when an agent session is killed
externally. This confirms that C18's "per-tick desired-state convergence" claim is operational.

**Discharges:** C18 reconciler convergence (operational), C40 "fires due orders" sub-claim.

**Commands:**

```bash
# Identify a named agent session (e.g. the deacon / health-patrol):
docker exec gascity-prototype gc session list

# Kill the named session externally (kill the tmux pane, not the controller):
PANE_ID=$(docker exec gascity-prototype bash -lc \
  'tmux list-panes -a -F "#{pane_id} #{pane_title}" | grep -i "deacon\|health" | awk "{print \$1}"')
docker exec gascity-prototype bash -lc "tmux kill-pane -t $PANE_ID"

# Observe: does gc restart the pane within a few reconciler ticks?
docker exec gascity-prototype bash -lc 'sleep 10 && gc session list'
docker exec gascity-prototype bash -lc \
  'gc events --since=2m | grep -i "deacon\|restart\|reconcil\|reap"'
```

**Expected output (PASS):** Within a few seconds (or the reconciler tick interval), the killed
agent pane reappears in `gc session list`. `gc events` shows a "reap" or "restart" event for the
killed pane. The agent is back up without manual intervention.

**PASS criterion:** The reconciler detects the dead session and restarts it automatically. C18's
desired-state convergence claim is operationally confirmed.

**FAIL criterion:** The killed pane does not reappear. The reconciler does not detect or restart
dead sessions. C18's convergence claim is not supported by the running `gc`.

**Discharges:** C18 reconciler convergence operational claim.

---

## Claim-to-Test Matrix

All statuses are OWED until the live run is executed and results are recorded in this table.

| Native Claim / Component | Claim Summary | Test(s) | Current Status |
|---|---|---|---|
| C34:OQ-C34-1 | Holdout boundary is enforced at bead dispatch (prevent, not merely audit) | A1, A2 | **OWED** |
| C43:OQ-C43-1 | Isolation-boundary typing is a real control (prevent, not a declaration) | A1 | **OWED** |
| C34:OQ-C34-1 (OS layer) | OS-level Bash reads are in the audit trail (VERDICT.md §6 item 8) | A2 | **OWED** |
| C44:OQ-4 | Per-twin `[[service]]` TOML + fixture/cassette schema is supported by `gc` | B | **OWED** |
| C44:OQ-2 (partial) | Three-mode twin precedence (replay → stateful → OpenAPI) exists in `gc` | B | **OWED** |
| C40:OQ-1 | Orders-insufficiency → Temporal trigger; falsifiable condition | C2, C3 | **OWED** |
| C40:OQ-3 | Crash-resume granularity; idempotent re-launch; default retry bound | C1, C2, C3 | **OWED** |
| C42 rig partition dispatch | Workers are dispatched to rig-scoped `cwd`; prefix honored end-to-end | D | **OWED** |
| C41 identity attribution | Beads carry a `created_by` attribution field at write time | E | **OWED** |
| C42 bead-prefix scoping | Explicit `prefix=` config prevents rig-name collision (F10) | F | **OWED** |
| C18 reconciler convergence | `gc` reconciler restarts dead agent sessions automatically | G | **OWED** |

---

## Outcome Routing

This table maps each test result to the downstream architectural consequence. The "Spec annotation /
D-decision input" column names the spec(s) or decision record that must be updated once the result
is known.

| Test | PASS outcome | FAIL outcome | Spec annotation / D-decision input |
|---|---|---|---|
| **A1 PREVENT** | D-20 fence is a real control; C43/C34 are enforcement boundaries; D-30 watcher not needed for bead layer | D-30 watcher MUST be built; `auto-001` binding gate triggered if A2 also SILENT; C43/C34 downgraded to advisory | C34, C43, D-30 design decision, `auto-001` gate |
| **A2 PREVENT** | OS layer enforces rig partition; combined with A1 PREVENT: no compensating layer needed | OS layer does not enforce; if SILENT: VERDICT.md §6 item 8 confirmed; C34 is not OS audit boundary | C34, D-30 scope (may need OS-level compensating control) |
| **A2 SILENT** | (N/A — SILENT is always a FAIL) | C34 OS audit claim is void; undetected cross-rig reads possible; D-30 watcher scope must include OS reads; P2 blocked without OS-level control | C34 annotation, D-30 scope, P2 readiness gate |
| **B PASS** | C44 twin design can proceed; bind OQ-4 fields to observed schema | C44:OQ-4 must be re-authored before any C44 implementation; per-twin packaging design is blocked | C44 (OQ-4, OQ-2 partial) |
| **C1 PASS (step-boundary)** | C40:OQ-3 granularity = step; controller-crash durability confirmed | C40:OQ-3 granularity = order; idempotency requirement propagates to order definitions | C40:OQ-3 annotation |
| **C2 PASS (durable)** | dolt push cadence sufficient for container-restart durability; C40:OQ-1 trigger NOT met | C40:OQ-1 trigger confirmed: any container restart during multi-step order = lost progress; Temporal integration warranted for P11 | C40 (OQ-1, OQ-3); Temporal integration decision |
| **C3 PASS (bound known)** | C40:OQ-3 retry ceiling = N; record in C40 | Retry bound unknown; add explicit ceiling to C40 spec | C40:OQ-3 annotation |
| **D PASS** | Rig partition assignment honored at dispatch; C42 operational path confirmed | Partition dispatch broken; C42 rig-assignment design must be revisited | C42 annotation |
| **E PASS** | C41 attribution field confirmed; bead store is a reliable identity audit trail | C41 attribution claim unverified; bead store is not a reliable audit trail; C41 design must address missing attribution | C41 annotation |
| **F PASS** | F10 prefix-collision fix is in place and effective | F10 collision is active in the deployed config; `city.toml` must be corrected before any test that uses multi-rig beads | C42, `city.toml` authoring guidance |
| **G PASS** | C18 reconciler convergence confirmed; desired-state loop is operational | C18 convergence claim not supported; `gc` does not restart dead agents; C18 design must account for manual recovery | C18 annotation |

---

## Protocol Ambiguities and Unrunnable Items (for Orchestrator)

The following items in [D-23-gas-city-spike-protocol.md](./D-23-gas-city-spike-protocol.md) were
ambiguous or potentially unrunnable as written and are flagged for the orchestrator:

1. **`bd create --prefix r2` flag existence is unverified.** Probe A1c offers a fallback (inline
   prefix in the bead content string). The `--prefix` flag may not exist in the `bd` binary at the
   pinned commit. The fallback form (`bd create "r2-…"`) tests whether the bead-layer enforces
   against a content-embedded prefix, which is a slightly different enforcement scenario. Record
   which form was used.

2. **`gc events --since=5m` syntax.** The `--since` flag and its time-duration format are assumed
   but not confirmed against the pinned `gc` binary. If `--since` is not recognized, substitute
   `gc events --tail=100` or `gc events | tail -100` as appropriate.

3. **`gc session list --json` flag.** JSON output mode is assumed for Test D's cwd inspection;
   the flag may not exist. If not, parse text output or use `tmux list-panes -a` directly inside
   the container.

4. **Dolt SQL direct access path for Test E.** The beadstore Dolt server runs on a local port
   (per F9 and substrate harvest), but the exact socket path / port is not documented in the
   protocol. The `bd schema` command is a speculative alias. Direct `dolt sql` access requires
   knowing the server's bind address. If `bd` does not expose schema, the dolt server port must be
   identified from `gc status` output or container environment before Test E can run.

5. **tmux pane ID extraction in Test G.** The pane title format (`#{pane_title}` in tmux
   `list-panes`) may not match the agent role name in all `gc` configurations. Adjust the `grep`
   pattern to match actual pane titles observed in `gc session list` output during the run.

6. **Reconciler tick interval for Test G.** The observation window (`sleep 10`) assumes the
   reconciler fires within 10 seconds. If the tick interval is longer, the sleep must be extended.
   The tick interval is not documented in the protocol or harvest; note the actual recovery latency
   in the results record.

---

## Results Record (fill in during live run)

| Test | Date | Operator | Observation | Verdict | OQ(s) closed | Decision triggered |
|---|---|---|---|---|---|---|
| A1a | — | — | — | — | — | — |
| A1b | — | — | — | — | — | — |
| A1c | — | — | — | — | — | — |
| A2a | — | — | — | — | — | — |
| A2b | — | — | — | — | — | — |
| A2c | — | — | — | — | — | — |
| B | — | — | — | — | — | — |
| C1 | — | — | — | — | — | — |
| C2 | — | — | — | — | — | — |
| C3 | — | — | — | — | — | — |
| D | — | — | — | — | — | — |
| E | — | — | — | — | — | — |
| F | — | — | — | — | — | — |
| G | — | — | — | — | — | — |

---

*Procedure authored 2026-06-01. Operationalizes [D-23-gas-city-spike-protocol.md](./D-23-gas-city-spike-protocol.md). Ground-truth build facts from [D-23-substrate-harvest.md](./D-23-substrate-harvest.md) (F1–F12, `lago-morph/gascity-prototype@b14c278`). Config keys cross-reference [gascity-config-anchor.md](./gascity-config-anchor.md). Execute against prototype branch `claude/great-pascal-RUfkN`.*
