# D-23 Gas City Reality-Check Spike — Runnable Protocol

**Status:** PROTOCOL ONLY — spike not yet executed (operator decision: no live agents/token burn this session).
**Resolves:** C34:OQ-C34-1, C43:OQ-C43-1, C40:OQ-1, C40:OQ-3, C44:OQ-4 (partial), C44:OQ-2 (partial).
**Prerequisite decisions:** [D-23 (adopted)](review-log.md) — prevent-vs-detect reality-check, first Sweep-2 action; [D-20 (adopted)](review-log.md) — C43 fence pulled to P2 precondition (holds only if D-23 resolves "prevent").

---

## 0. Purpose and the binding question

**The one pivotal question this spike must answer:**

> Does `gc` (or the pack loader / OS sandbox) **PREVENT** an out-of-partition access at tool-call or config-load time — refusing the call, returning a non-zero exit, returning no data to the agent — or does it only **PERMIT-and-LOG** (detect after the fact)?

This is not a curiosity. Every "Gas City does X natively" claim in v4 rests on the answer, and the two outcomes trigger different architectural paths:

| Outcome | Consequence |
|---|---|
| **PREVENT** — `gc` refuses the call, non-zero exit, no data returned | D-20's "fence pulled to P2 precondition" holds as a real control. C43's boundary-typing is a *control*, not a declaration. C34's holdout boundary is enforced at dispatch time. Architecture proceeds as specified. |
| **DETECT-ONLY** — call succeeds, data returned, access appears in audit log only | Triggers the `auto-001` binding-gate decision: a compensating prevent layer (OPA policy, seccomp profile, or Linux namespace restriction) must be added before P2, **or** the unattended-autonomy scope must be descoped. D-20's fence closes a documented window, not a real one. C34 is an audit boundary, not an enforcement boundary. |

**What the prototype already established:** The [Gas City prototype](https://github.com/lago-morph/gascity-prototype) (built 2026-05-25, branch `claude/great-pascal-RUfkN`) proved the city *stands up* — all six gastown agents started, mayor and boot exchanged inter-agent commands within seconds, bead-store, dolt, tmux, and claude all verified working inside Docker. It did **not** run the end-to-end smoke test (`bd create` → mayor reconciles → worker completes), and it did **not** probe the bead-prefix enforcement boundary. The partition-enforcement question is therefore **unverified** and remains the highest-leverage unknown in the entire architecture.

**Scope note:** This spike also covers `[[service]]` twin semantics (Test B) and Orders durability (Test C), resolving C44:OQ-4, C40:OQ-3, and C40:OQ-1 in one run.

---

## 1. Obtain and build `gc`

### Prerequisites

- Docker daemon running (all tests are Dockerized; the prototype is not runnable without it).
- Git, curl, and `make` on the host.
- Either an Anthropic API key (laptop) or `CLAUDE_CODE_OAUTH_TOKEN` from `/home/claude/.claude/remote/.oauth_token` (Anthropic sandbox).

### Clone the prototype

```bash
git clone https://github.com/lago-morph/gascity-prototype.git
cd gascity-prototype
git checkout claude/great-pascal-RUfkN   # the branch that was verified working
```

### Stage binaries (required — TLS-inspection proxy blocks in-container downloads)

The sandbox's TLS-inspection proxy blocks `curl`/`go get` from inside containers. All binaries must be staged on the **host** and `COPY`'d into the image via the build context. Run these commands on the **host**, not inside a container:

```bash
mkdir -p build-context

# dolt
curl -fsSL -o build-context/dolt-linux-amd64.tar.gz \
  https://github.com/dolthub/dolt/releases/latest/download/dolt-linux-amd64.tar.gz

# bd (beads CLI)
curl -fsSL -o /tmp/bd.tgz \
  https://github.com/gastownhall/beads/releases/download/v1.0.4/beads_1.0.4_linux_amd64.tar.gz
tar -xzf /tmp/bd.tgz -C /tmp && cp /tmp/bd build-context/

# gc — build on the host first
# IMPORTANT: verify the Go version requirement in go.mod before downloading.
# At time of prototype build: go.mod required Go 1.26.3 (verify at run time with
# `head -5 /tmp/gascity/go.mod`). The prototype README showed "Go 1.25"; run-time
# go.mod is authoritative — download accordingly.
GC_GO_VERSION=1.26.3   # adjust to what go.mod says
curl -fsSL "https://go.dev/dl/go${GC_GO_VERSION}.linux-amd64.tar.gz" \
  | tar -xz -C /tmp/
export PATH=/tmp/go/bin:$PATH

git clone https://github.com/gastownhall/gascity.git /tmp/gascity
head -5 /tmp/gascity/go.mod   # CONFIRM version matches what you downloaded above
(cd /tmp/gascity && make install)
cp ~/go/bin/gc build-context/

# claude + node — copy from the existing install on the host
cp -r /opt/node22 build-context/
cp -r /opt/claude-code build-context/

# copy image support files
cp Dockerfile entrypoint.sh city.toml.example build-context/
cp -r pack build-context/
```

### Build the image

```bash
docker build -t gascity-prototype:latest -f build-context/Dockerfile build-context/
```

### Configure auth

**Laptop path:**

```bash
cp .env.example .env
# Edit .env: set ANTHROPIC_API_KEY=sk-ant-…
# RIG1_URL / RIG2_URL / BEADSTORE_URL default to lago-morph/* and are correct as-is.
docker compose up -d
```

**Anthropic sandbox path** (requires `--network=host`, CA-bundle mount, OAuth token):

```bash
# .env for sandbox (do not commit):
cat > .env <<'EOF'
ANTHROPIC_API_KEY=
ANTHROPIC_BASE_URL=$ANTHROPIC_BASE_URL
CLAUDE_CODE_OAUTH_TOKEN=$(cat /home/claude/.claude/remote/.oauth_token)
RIG1_URL=http://local_proxy@127.0.0.1:38985/git/lago-morph/gascity-proto-rig1
RIG2_URL=http://local_proxy@127.0.0.1:38985/git/lago-morph/gascity-proto-rig2
BEADSTORE_URL=http://local_proxy@127.0.0.1:38985/git/lago-morph/gascity-proto-beadstore.git
RIG1_BRANCH=main
RIG2_BRANCH=main
BEADSTORE_BRANCH=main
DOLT_REF=refs/heads/dolt-data
EOF

# Expand the oauth token var before writing the file — the heredoc above leaves it
# as a literal string; run:
sed -i "s|\$(cat /home/claude/.claude/remote/.oauth_token)|$(cat /home/claude/.claude/remote/.oauth_token)|" .env

docker compose -f docker-compose.yml -f docker-compose.sandbox.yml up -d
```

The `docker-compose.sandbox.yml` overlay adds: `network_mode: host`, `/etc/ssl/certs/ca-certificates.crt` bind-mount (the sandbox TLS-inspection CA that in-container claude must trust), and `NODE_EXTRA_CA_CERTS` / `SSL_CERT_FILE` env vars.

---

## 2. Minimal stand-up

The smallest city needed for the spike tests: one rig registered (rig1), dog pool enabled, beads active.

### Confirm the controller is up

```bash
docker compose logs --tail=40 city        # watch the entrypoint sequence
docker exec gascity-prototype gc status   # expect: all named gastown agents shown
```

Expected `gc status` output: coordinator (mayor), health-patrol (deacon), bootstrap (boot), worker pool, rig1 observer, control-dispatchers — all in a running or idle state.

### Confirm sessions and events

```bash
docker exec gascity-prototype gc session list        # list active tmux sessions / agent panes
docker exec gascity-prototype gc events --follow     # live event stream; Ctrl-C to stop
```

### Confirm bead store is accessible

```bash
docker exec gascity-prototype bash -lc \
  'cd /workspace/rigs/rig1 && bd ls'
```

Expected: empty or minimal list; no error. If `bd ls` errors, the dolt server has not started — check `gc status` for the bead provider process.

### Smoke-signal bead (end-to-end prerequisite)

Before running the enforcement tests, verify the round-trip works at all:

```bash
docker exec gascity-prototype bash -lc \
  'cd /workspace/rigs/rig1 && bd create "spike-smoke-signal: confirm bead store works"'
```

Note the returned bead ID (will be `r1-<hash>`). Confirm it appears:

```bash
docker exec gascity-prototype bash -lc 'cd /workspace/rigs/rig1 && bd ls'
```

---

## 3. Test A — Prevent-vs-detect (THE test)

This test has two sub-probes because the question spans two layers: the **bead/tool layer** (what `gc`/`bd` enforces at tool-call time) and the **OS/Bash layer** (what a claude process with cwd=rig1 can do at the filesystem level, which may bypass the bead trail entirely — VERDICT.md §6 item 8).

### A1 — Bead visibility: cross-partition bead access

**Setup:** Obtain a rig2-scoped bead ID and a holdout/scenarios bead ID to use as targets. If none exist, create them from the controller context (city-level scope):

```bash
# Create an r2-scoped bead from rig2's directory (city-level or rig2 worker context):
docker exec gascity-prototype bash -lc \
  'cd /workspace/rigs/rig2 && bd create "spike-target-r2: bead for cross-partition probe"'
# Note the returned ID, e.g. r2-abc123

# Create a gp-scoped (city-level) bead:
docker exec gascity-prototype bash -lc \
  'cd /workspace/city && bd create "spike-target-gp: city-level bead for probe"'
# Note the returned ID, e.g. gp-def456
```

**Probe A1a — rig1-scoped worker reads an r2- bead:**

```bash
docker exec gascity-prototype bash -lc \
  'cd /workspace/rigs/rig1 && bd get r2-abc123'
# Capture: stdout, stderr, exit code ($?)
```

**Probe A1b — rig1-scoped worker reads a gp- bead:**

```bash
docker exec gascity-prototype bash -lc \
  'cd /workspace/rigs/rig1 && bd get gp-def456'
```

**Probe A1c — rig1-scoped worker attempts to CREATE an r2- bead:**

```bash
docker exec gascity-prototype bash -lc \
  'cd /workspace/rigs/rig1 && bd create --prefix r2 "spike-create-attempt: rig1 writing r2 prefix"'
# Alternative if --prefix flag not supported:
docker exec gascity-prototype bash -lc \
  'cd /workspace/rigs/rig1 && bd create "r2-spike-create-attempt: rig1 writing r2 prefix"'
```

**Capture for all A1 probes:** stdout verbatim, stderr verbatim, exit code, and check the event log:

```bash
docker exec gascity-prototype gc events --follow &
# (run probes in another terminal or capture events after)
docker exec gascity-prototype bash -lc 'gc events --since=5m | grep -i "r2-abc123\|r2-def\|audit\|denied\|refused"'
```

**A1 verdict table:**

| Observation | Verdict | Interpretation |
|---|---|---|
| `bd get r2-abc123` exits non-zero, stderr says "access denied" / "out of scope" / "prefix mismatch", no bead data returned | **PREVENT** | Bead layer enforces partition at read |
| `bd get r2-abc123` exits 0, bead data printed to stdout | **DETECT-ONLY** (bead layer) | Check whether access appears in `gc events` or audit trail |
| `bd create --prefix r2` exits non-zero with scope/prefix error | **PREVENT** | Bead layer enforces partition at write |
| `bd create --prefix r2` exits 0, bead created with r2 prefix | **DETECT-ONLY** (bead layer) | Check audit trail |
| Access not in any event/audit trail | **SILENT** — worst case; neither prevent nor detect | Requires escalation |

### A2 — OS/Bash-level reads: filesystem access bypassing the bead trail

This probe checks whether a worker whose `cwd` is `/workspace/rigs/rig1` can read rig2's files and holdout/scenarios content using raw Bash commands — which may not appear in the bead/OTLP trail at all (VERDICT.md §6 item 8 and [panel/02-security.md](panel/02-security.md)).

**Probe A2a — cross-rig filesystem read:**

```bash
docker exec gascity-prototype bash -lc \
  'cd /workspace/rigs/rig1 && cat ../rig2/README.md'
# Capture: stdout, exit code
```

**Probe A2b — read a hypothetical holdout/scenarios path:**

```bash
# First confirm where scenarios/holdout files would live under the city layout:
docker exec gascity-prototype bash -lc 'find /workspace/city -name "*.toml" | head -10'
docker exec gascity-prototype bash -lc 'ls /workspace/city/'

# Then probe:
docker exec gascity-prototype bash -lc \
  'cd /workspace/rigs/rig1 && cat /workspace/city/city.toml'
# A worker reading the city config at OS level — should this be prevented?
```

**Probe A2c — check whether the OS read appeared in any audit trail:**

```bash
docker exec gascity-prototype bash -lc \
  'gc events --since=5m | grep -i "cat\|read\|rig2\|scenarios\|city.toml"'
# If the above returns nothing, the read was silent.
```

**A2 verdict table:**

| Observation | Verdict | Implication for C34 |
|---|---|---|
| `cat ../rig2/README.md` exits non-zero (permission denied, chroot, namespace restriction) | **PREVENT at OS level** | C34's audit boundary is real |
| `cat ../rig2/README.md` succeeds, data printed, AND appears in `gc events` / OTLP trail | **DETECT at OS level** | C34 audit works but is not prevention |
| `cat ../rig2/README.md` succeeds, data printed, NOT in any trail | **SILENT** — no detect, no prevent | C34 is not an audit boundary for OS reads; VERDICT.md §6 item 8 confirmed |
| `cat /workspace/city/city.toml` succeeds, not in trail | **SILENT city-config read** | Agent could read all orders/secrets without detection |

---

## 4. Test B — `[[service]]` / twin semantics

This test probes what a `[[service]]` block in `city.toml` or `pack.toml` actually registers and does at runtime, resolving C44:OQ-4 (per-twin packaging schema) and partially C44:OQ-2 (three-mode precedence).

### Inspect existing `[[service]]` declarations

```bash
docker exec gascity-prototype bash -lc 'cat /workspace/city/city.toml | grep -A 20 "\[\[service\]\]"'
docker exec gascity-prototype bash -lc 'find /workspace -name "pack.toml" -exec grep -l "service" {} \;'
docker exec gascity-prototype bash -lc 'cat /pack/pack.toml'
```

### What does `gc` know about registered services?

```bash
docker exec gascity-prototype gc service list    # if this command exists
docker exec gascity-prototype gc help            # enumerate available subcommands
docker exec gascity-prototype gc help service 2>/dev/null || echo "no service subcommand"
```

### Inspect what a `[[service]]` block registers

```bash
# Try to register a minimal test service and observe:
docker exec gascity-prototype bash -lc \
  'cd /workspace/city && gc service register --help 2>&1 | head -30'

# Read the gc source or help to understand the [[service]] schema:
docker exec gascity-prototype bash -lc \
  'gc help session 2>&1; gc help sling 2>&1; gc help order 2>&1' | head -60
```

### Probe the twin mode (replay vs stateful vs OpenAPI)

```bash
# Check if the gastown pack defines any [[service]] blocks:
docker exec gascity-prototype bash -lc \
  'find /usr/local/lib /usr/local/share /root -name "*.toml" 2>/dev/null | xargs grep -l "\[\[service\]\]" 2>/dev/null | head -5'

# Inspect the packed gastown configuration:
docker exec gascity-prototype bash -lc \
  'gc pack inspect gastown 2>/dev/null || gc pack list 2>/dev/null'
```

**Capture for Test B:** The TOML schema accepted by `[[service]]` blocks; whether registration is immediate or deferred to controller reconciliation; which twin modes (`record`, `replay`, `stateful`, `openapi`) are supported; what fields are mandatory; and whether session/pane isolation per twin is visible in `gc status`.

**B verdict table:**

| Question | Observation to capture | OQ resolved |
|---|---|---|
| Does `[[service]]` register a runtime process or a metadata record? | `gc status` before/after registration; process list | C44:OQ-4 |
| What TOML fields does `[[service]]` accept? | Schema from `gc help` or TOML parse error messages | C44:OQ-4 |
| Which twin mode is the default? | `gc help service` or pack.toml defaults | C44:OQ-2 |
| Are twin sessions visible as named panes in `gc session list`? | `gc session list` output | C44:OQ-1 (partial) |

---

## 5. Test C — Orders durability

This test resolves C40:OQ-1 (the Orders-insufficiency → Temporal trigger) and C40:OQ-3 (crash-resume granularity, idempotency, default retry bound) by killing the controller and the container mid-order and observing what survives.

### Setup: create a long-running order

```bash
# Create a bead that takes multiple steps (e.g. a multi-part task):
docker exec gascity-prototype bash -lc \
  'cd /workspace/rigs/rig1 && bd create "spike-durability: multi-step task step 1 of 3"'
# Note the bead ID: r1-DUR

# Confirm the bead is open and the coordinator has seen it:
docker exec gascity-prototype bash -lc 'cd /workspace/rigs/rig1 && bd get r1-DUR'
docker exec gascity-prototype gc events --follow &
```

### Kill the controller mid-step (C40:OQ-3a — in-process crash)

```bash
# Identify the gc controller PID inside the container:
docker exec gascity-prototype bash -lc 'pgrep -a gc'

# Send SIGKILL to the controller (not the container):
docker exec gascity-prototype bash -lc 'kill -9 $(pgrep -f "gc start")'

# Observe: does tini/PID1 restart gc automatically? How quickly?
docker exec gascity-prototype bash -lc 'sleep 5 && gc status'

# Check bead state after restart:
docker exec gascity-prototype bash -lc 'cd /workspace/rigs/rig1 && bd get r1-DUR'
```

**Capture:** Was the order resumed at the last checkpoint (step-boundary resume) or re-executed from the start? What is the resume granularity? Does `gc events` show a "resumed" or "restarted" event?

### Kill the container mid-step (C40:OQ-3b — container death)

```bash
# While r1-DUR is in progress:
docker compose down   # or docker rm -f gascity-prototype

# Bring it back up:
docker compose up -d   # sandbox: add -f docker-compose.sandbox.yml

# Wait for rehydration (entrypoint re-clones rigs + beadstore):
docker compose logs --tail=60 city

# Check bead state survived:
docker exec gascity-prototype bash -lc 'cd /workspace/rigs/rig1 && bd ls'
docker exec gascity-prototype bash -lc 'cd /workspace/rigs/rig1 && bd get r1-DUR'
```

**Capture:** Was the bead state (status, last-step marker) preserved in the dolt beadstore and recovered after re-clone? Was any in-flight step lost?

### Probe the default retry bound

```bash
# Create a bead that deliberately fails (e.g. invalid task):
docker exec gascity-prototype bash -lc \
  'cd /workspace/rigs/rig1 && bd create "spike-retry: intentionally unresolvable task XYZZY"'
# Watch how many times gc retries before giving up:
docker exec gascity-prototype gc events --follow | grep -i "retry\|fail\|XYZZY"
```

**C verdict table:**

| Observation | Verdict | OQ resolved |
|---|---|---|
| Bead state preserved after container restart | Orders are durable to container death | C40:OQ-3 (durability) |
| Bead state lost after container restart | Orders are ephemeral; Temporal dependency confirmed | C40:OQ-3, triggers Temporal threshold |
| Resume at step-boundary (last completed step) | Granularity = step | C40:OQ-3 (granularity) |
| Re-execute from start | Granularity = order (not step) | C40:OQ-3 |
| Retry count observable in events | Default retry bound known | C40:OQ-3 |
| No observable retry limit | Retry bound unknown; set C40:OQ-1 trigger as "observed stall" | C40:OQ-1 partial |

---

## 6. Results template and decision routing

### Fill-in table (one row per test; complete after execution)

| Test | Observation captured | Verdict | v4 OQ(s) resolved | Decision triggered |
|---|---|---|---|---|
| **A1a** — `bd get r2-<id>` from rig1 cwd | _[fill: exit code, stdout/stderr snippet]_ | PREVENT / DETECT-ONLY / SILENT | C34:OQ-C34-1, C43:OQ-C43-1 | If PREVENT: D-20 confirmed. If DETECT-ONLY or SILENT: `auto-001` binding gate triggered. |
| **A1b** — `bd get gp-<id>` from rig1 cwd | _[fill]_ | PREVENT / DETECT-ONLY / SILENT | C34:OQ-C34-1 | Same as A1a |
| **A1c** — `bd create --prefix r2` from rig1 cwd | _[fill]_ | PREVENT / DETECT-ONLY | C43:OQ-C43-1 | Same as A1a |
| **A2a** — `cat ../rig2/README.md` from rig1 cwd | _[fill: exit code, data returned Y/N, in trail Y/N]_ | PREVENT / DETECT / SILENT | C34:OQ-C34-1 (OS layer) | If SILENT: VERDICT.md §6 item 8 confirmed; C34 is not an OS audit boundary; compensating control required before P2. |
| **A2b** — `cat /workspace/city/city.toml` from rig1 cwd | _[fill]_ | PREVENT / DETECT / SILENT | C34:OQ-C34-1 (OS layer) | Same as A2a |
| **A2c** — OS reads in audit trail | _[fill: events returned Y/N]_ | DETECT / SILENT | C34:OQ-C34-1 | Confirms or refutes C34's audit boundary claim |
| **B** — `[[service]]` schema and runtime registration | _[fill: TOML fields observed, twin mode, process visible Y/N]_ | Schema confirmed / Not found | C44:OQ-4, C44:OQ-2 (partial) | If `[[service]]` absent or schema differs: C44 design must bind to observed schema before implementation. |
| **C (controller kill)** — bead state after `gc` restart | _[fill: bead status, resume granularity]_ | Step-boundary / Order-start / Bead lost | C40:OQ-3 | If bead lost: Orders durability insufficient; escalate to Temporal discussion. |
| **C (container kill)** — bead state after `docker compose down/up` | _[fill: bead status, steps preserved Y/N]_ | Durable / Ephemeral | C40:OQ-3 | If Ephemeral: C40:OQ-1 trigger condition = container restart; Temporal integration warranted. |
| **C (retry bound)** — max retries observed | _[fill: count or "unbounded"]_ | Bound known / Unknown | C40:OQ-3 | If unbounded: add explicit retry ceiling to C40 spec. |

### OQ closure map

This spike is designed to close or substantially narrow the following v4 open questions:

| OQ id | Component | Question | Closed by test |
|---|---|---|---|
| C34:OQ-C34-1 | C34 holdout-integrity | PREVENT vs DETECT at bead layer | A1 |
| C43:OQ-C43-1 | C43 isolation-boundary | PREVENT vs DETECT at bead layer (same question) | A1 |
| C34:OQ-C34-1 (OS) | C34 holdout-integrity | OS-level Bash reads in audit trail (VERDICT.md §6 item 8) | A2 |
| C40:OQ-1 | C40 orders | Orders-insufficiency → Temporal trigger (falsifiable condition) | C |
| C40:OQ-3 | C40 orders | Crash-resume granularity; idempotent re-launch; default retry bound | C |
| C44:OQ-4 | C44 twins | Per-twin `[[service]]` TOML + fixture/cassette schema | B |
| C44:OQ-2 (partial) | C44 twins | Three-mode precedence (replay→stateful→OpenAPI) | B |

OQs **not** closed by this spike (remain for Sweep-2 per-component freeze): C40:OQ-2 (order-definition syntax / trigger-predicate grammar), C40:OQ-4 (C40↔C39 launch seam), C44:OQ-1 (G22/G31 sibling cross-check), C44:OQ-3 (twin session-state reset granularity), C44:OQ-5 (per-twin engine choice), C43:OQ-C43-2 (P0→P3b exposure window interim bound).

### Decision routing after results

**If A1 = PREVENT and A2 = PREVENT:**
- D-20's fence is a real control. Architecture proceeds as specified. C34 and C43 OQs are jointly closed with verdict = "enforce." No compensating layer needed.

**If A1 = DETECT-ONLY (bead layer only) and A2 = PREVENT (OS layer):**
- The bead layer is advisory; the OS layer provides the actual enforcement. Document the distinction. C43's "typing" is a metadata declaration, not a hard refuse. Compensating prevent layer at the bead/tool level (OPA policy wrapping `bd` calls) should be evaluated before P2.

**If A1 = DETECT-ONLY and A2 = SILENT (worst case):**
- `auto-001` binding gate is triggered. Required action before P2: add a compensating prevent layer (Linux namespace / seccomp restricting cross-rig path access, OPA policy enforcing bead-prefix scope at the `bd` binary boundary) **or** formally descope the unattended autonomy claim (P2). This is not optional — VERDICT.md §6 item 1 makes this a go/no-go gate, not a noted caveat.

**If C = Ephemeral (container kill destroys bead state):**
- Orders durability ceiling is the dolt push cadence (currently manual). The falsifiable trigger for C40:OQ-1 is: "any container restart during a multi-step order results in lost progress." Temporal integration is warranted if P11 self-healing loops run unattended longer than the push cadence.

**If B = `[[service]]` not found in `gc help` or pack schema:**
- C44's design is speculative with respect to the actual `gc` schema. The per-twin packaging design (C44:OQ-4) must be re-authored against observed `gc` capabilities before implementation.

---

*Protocol authored: 2026-06-01. Execute against prototype branch `claude/great-pascal-RUfkN` or a rebuild from the same sources. For the prototype repo and bead store repos, see [lago-morph/gascity-prototype](https://github.com/lago-morph/gascity-prototype) and [gastownhall/gascity](https://github.com/gastownhall/gascity).*
