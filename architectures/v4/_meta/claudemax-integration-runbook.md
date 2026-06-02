# Claude Max Integration Runbook — Software Factory v4

**Purpose.** Numbered, operator-facing recipe for bringing up Claude Code under a Claude Max
subscription as the C28 worker that Gas City drives. This is the second operator task after
the [Gas City integration runbook](./gascity-integration-runbook.md) is complete. Sections
mirror that runbook's structure for consistency; do not duplicate content held there.

**Primary source.** Everything in this runbook is derived from
[C28 — Claude Code agent loop](../spec/C28-claude-code-agent-loop.md) §3.3 (env contract),
[C29 — Model floor & stylesheet routing](../spec/C29-model-floor-stylesheet.md) §3.3 (stylesheet
grammar), and [C04 — Session & provider runtime](../spec/C04-session-provider.md) §8 (config
surface), cross-checked against the D-23 prototype harvest (F7, F12) and the verified
`entrypoint.sh` (`/tmp/gascity-prototype/entrypoint.sh`).

**Verification callout convention.** Every item that is not yet verified against a live
pinned-`gc` run carries:

> **[needs-G11]** — exact field name unverified; correct at the conceptual level but
> the on-disk key spelling requires a pinned-`gc` run (G11) to freeze.

---

## 1. Prerequisites

### 1.1 Claude CLI under a Max subscription

| Item | What to do |
|---|---|
| Install the `claude` CLI | Pre-stage `claude-code` (npm package or pre-built binary) in the Docker image; the sandbox's TLS-inspection proxy blocks in-container downloads. See the [Gas City runbook §1](./gascity-integration-runbook.md#1-prerequisites). |
| Max subscription active | Log in at `claude.ai` under the Max plan. No API key is issued or needed; Max auth is OAuth-only. |
| Run `claude /login` once on the host | This populates `~/.claude/remote/.oauth_token` (sandbox path) or `~/.claude/` (laptop path). The token is the auth artifact C28 consumes. |

**Auth artifact.** The only credential needed is the OAuth token obtained by `claude /login`:

```
# Sandbox path (verified against the prototype):
/home/claude/.claude/remote/.oauth_token

# Laptop / standard path:
~/.claude/  (token managed internally by the claude CLI; no explicit file path needed)
```

On the sandbox, export it as an environment variable before bringing up the container:

```bash
export CLAUDE_CODE_OAUTH_TOKEN=$(cat /home/claude/.claude/remote/.oauth_token)
```

> **Verification status — CLAUDE_CODE_OAUTH_TOKEN: prototype-verified.**
> The prototype `docker-compose.sandbox.yml` passes `CLAUDE_CODE_OAUTH_TOKEN` to the container
> and `docs/PLAN.md` item 3 confirms Claude in tmux in the container authenticates via this
> env var (D-23, 2026-05-25). The env var name is confirmed. See also C28 I1: OAuth tokens
> MUST NOT be used outside the `claude` process; no other component reads this value.

### 1.2 Node.js runtime

The `claude` binary requires Node.js. Pre-stage it in the image (same proxy constraint as above):

```bash
# In Dockerfile
COPY --from=build-context /opt/node22 /opt/node22
ENV PATH="/opt/node22/bin:$PATH"
```

### 1.3 CA bundle (sandbox / proxy-mediated deployments only)

If running behind a TLS-inspection proxy (the Anthropic sandbox), bind-mount the host CA bundle
and set the three CA-trust env vars. Laptops and non-proxy deployments do not need this.

```bash
# docker-compose.sandbox.yml fragment (prototype-verified):
environment:
  - NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt
  - SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
  - REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
volumes:
  - /etc/ssl/certs/ca-certificates.crt:/etc/ssl/certs/ca-certificates.crt:ro
```

> **Verification status — CA bundle path: prototype-verified (D-23, docs/PLAN.md item 3).**
> The CA var name in C28's env table (`ANTHROPIC_CLAUDE_CODE_CA_BUNDLE`) maps to the same
> bundle but is a separate Claude-specific env var. See §2 for the full env table.

---

## 2. Auth & Session Environment

### 2.1 Copyable env block

The following env block is injected by C04 at every `Start`/`Resume` into the C28 agent
process (C04 §3.2 — env injection is total; I3: no turn runs without it). Place in the
`[[agent]] env = { … }` section of `city.toml`, or pass via container env for Phase-0.

```toml
# city.toml — [[agent]] env block for the C28 implementer worker
# Source: C28 §3.3 "Config / env contract — concrete Max bring-up table"
[[agent]]
name     = "worker"
provider = "claude"

# env = { … } exact key spelling is [needs-G11]; concepts are harvest-verified.
# Until G11 is run, wire via container environment (docker-compose env: section).
```

Container / `.env` form (use this at Phase-0):

```bash
# ── Auth (Max OAuth; no API key) ──────────────────────────────────────────────
CLAUDE_CODE_OAUTH_TOKEN=<token-from-claude-login>   # prototype-verified
ANTHROPIC_BASE_URL=<proxy-base-url>                 # sandbox only; omit on laptop

# ── Sandbox / root container bypass ───────────────────────────────────────────
IS_SANDBOX=1                                        # required when running as root (F12)

# ── OTLP telemetry ────────────────────────────────────────────────────────────
CLAUDE_CODE_ENABLE_TELEMETRY=1                      # enables OTLP emission from claude
OTEL_EXPORTER_OTLP_ENDPOINT=http://collector:4318  # [needs-G11] key spelling
OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf           # [needs-G11]
OTEL_METRICS_EXPORTER=otlp                          # 60s cadence
OTEL_LOGS_EXPORTER=otlp                             # 5s cadence
CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1               # optional; enables traces
OTEL_LOG_RAW_API_BODIES=1                           # per-API-call raw body dump → C24

# ── CA bundle (sandbox / proxy only) ──────────────────────────────────────────
NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt
SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
ANTHROPIC_CLAUDE_CODE_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt  # [needs-G11]
```

### 2.2 Env var purpose table

| Env var | Required | Purpose | Verification status |
|---|---|---|---|
| `CLAUDE_CODE_OAUTH_TOKEN` | Yes | Max OAuth token; the sole auth credential for C28 | Prototype-verified (D-23, docs/PLAN.md item 3, docker-compose.sandbox.yml) |
| `ANTHROPIC_BASE_URL` | Sandbox only | Base URL through the TLS-inspection proxy | Prototype-verified (docker-compose.sandbox.yml); omit on laptop |
| `IS_SANDBOX` = `"1"` | Yes (root container) | Allows `claude --dangerously-skip-permissions` to run as root without refusal | Harvest-verified F12; C28 E-C28-05 |
| `CLAUDE_CODE_ENABLE_TELEMETRY` = `"1"` | Yes | Activates native OTLP metrics/logs/traces emission from the `claude` process | C28 §3.3; AI-CONTEXT §4.3 |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | Yes | OTLP collector endpoint (C25 input) | C28 §3.3; **[needs-G11]** exact key |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | Yes | OTLP wire protocol | C28 §3.3; **[needs-G11]** exact key |
| `OTEL_METRICS_EXPORTER` = `"otlp"` | Yes | Routes Claude Code metrics to OTLP (60s cadence) | C28 §3.3; AI-CONTEXT §4.3 |
| `OTEL_LOGS_EXPORTER` = `"otlp"` | Yes | Routes Claude Code logs to OTLP (5s cadence) | C28 §3.3; AI-CONTEXT §4.3 |
| `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA` = `"1"` | Optional | Enables per-turn OTLP trace emission | C28 §3.3; AI-CONTEXT §4.3 |
| `OTEL_LOG_RAW_API_BODIES` = `"1"` | Yes | Dumps raw API request/response bodies to watched dir → C24 bridge → CXDB | C28 §3.3; AI-CONTEXT §13.2 |
| `NODE_EXTRA_CA_CERTS` | Sandbox only | Node.js CA trust (sandbox TLS proxy) | Prototype-verified docker-compose.sandbox.yml |
| `SSL_CERT_FILE` | Sandbox only | OpenSSL CA trust (sandbox TLS proxy) | Prototype-verified docker-compose.sandbox.yml |
| `ANTHROPIC_CLAUDE_CODE_CA_BUNDLE` | Sandbox/proxy only | Claude-specific CA bundle override | C28 §3.3 — **[needs-G11]** (inferred from prototype CA pattern; exact var name unverified) |

> **[needs-G11] callout — OTEL key spelling.** The OTEL variable *concepts* are
> harvest-verified (F7/F12) — endpoint, protocol, metrics/logs exporters, raw-API-bodies flag,
> IS_SANDBOX, CA bundle are all confirmed present. The *exact on-disk key names* (e.g.
> `OTEL_EXPORTER_OTLP_ENDPOINT` vs a different spelling) are marked `[needs-G11]` per C28 §3.3.
> Do not assume the keys above are frozen until a pinned-`gc` run verifies them.

### 2.3 Onboarding pre-acks (`~/.claude.json`)

Before `gc start --foreground`, the entrypoint must write `~/.claude.json`. Without these
entries, the interactive `claude` process hangs on dialogs and C04 returns E-C28-01.

```bash
# In entrypoint.sh — run before exec gc start --foreground
# Source: C28 §3.3 onboarding table; C04 §4.2; verified against prototype entrypoint.sh
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

> **Important:** this is `~/.claude.json`, NOT `~/.claude/settings.json` (F12, prototype-verified).
> Per-working-directory trust entries must cover every `workdir` an agent uses; the entrypoint
> writes them at container-start time because paths are only known then.

**Onboarding field reference:**

| Field | File | Value | Notes |
|---|---|---|---|
| `hasCompletedOnboarding` | `~/.claude.json` | `true` | Pre-acks theme picker dialog |
| `hasSeenWelcome` | `~/.claude.json` | `true` | Pre-acks welcome dialog |
| `theme` | `~/.claude.json` | `"dark"` | Any valid theme value |
| `bypassPermissionsModeAccepted` | `~/.claude.json` | `true` | Global bypass-permissions pre-ack |
| `projects[<workdir>].hasTrustDialogAccepted` | `~/.claude.json` | `true` | Per-workdir trust ack; written per rig path |
| `projects[<workdir>].bypassPermissionsModeAccepted` | `~/.claude.json` | `true` | Per-workdir bypass ack |
| `IS_SANDBOX` | container env | `"1"` | Root-container bypass (C28 E-C28-05) |

---

## 3. The `claude` Provider Preset

### 3.1 `city.toml` declaration

Gas City drives each C28 worker via the `[[agent]] provider = "claude"` preset (harvest-verified
from `city.toml.example`; C04 §8 config surface; C28 §3.3). The `[workspace] provider = "claude"`
sets the city-wide default.

```toml
# city.toml — Claude provider preset for the C28 implementer worker
# Source: C28 §3.3; C04 §8; harvest-verified against city.toml.example:9-11

[workspace]
name     = "software-factory"
provider = "claude"            # city-wide LLM-side preset (harvest-verified)

[[agent]]
name     = "worker"
provider = "claude"            # C28 implementer: Claude Code under Max OAuth
# env = { … }                 # OTEL + auth vars; see §2.1 — exact keys [needs-G11]

[[agent]]
name     = "judge"
provider = "claude"            # Phase-0 per D-1: same-provider judge (see §4)
```

> **Verification status — `provider = "claude"`: harvest-verified.**
> `city.toml.example` line 10 (`provider = "claude"` in `[workspace]`) and C04 §8 both confirm
> this is the correct LLM-side preset token that the `claude` CLI recognises.

### 3.2 How Gas City (C04) drives it

C04 launches C28 through the `gc start` controller (F6, harvest-verified). The tmux Provider is
the Phase-0 concrete (F7, harvest-verified):

1. `gc start --foreground` (the controller, C04) spawns each `[[agent]]` as a new tmux pane.
2. The pane runs: `claude --dangerously-skip-permissions [--resume <claude_session_id>]`
3. C04 injects the `[[agent]] env = { … }` block (OAuth + OTEL) at every `Start`/`Resume`.
4. C05/Sling dispatches a bead to the worker: `gc sling <bead-id>` → worker pool scales 0→1
   (F5, harvest-verified) — a new tmux pane with a fresh `claude` process.
5. The `claude` process (C28 loop) receives the bead context as its initial prompt and begins
   its inner loop: reason → PreToolUse hook gate → tool dispatch → PostToolUse observe → repeat.

```
gc start --foreground
  └─ tmux pane: worker
       └─ claude --dangerously-skip-permissions
            └─ C28 inner loop (reason → tool → observe → repeat)
```

> **Cross-reference.** The full session lifecycle (start → detach → crash-recover → stop) is
> in [C04 §9 state diagram](../spec/C04-session-provider.md#9-session-lifecycle--state-diagram).
> Do not duplicate here.

---

## 4. Model-Floor / Stylesheet Routing (C29)

### 4.1 Floor declaration

[C29](../spec/C29-model-floor-stylesheet.md) declares Claude Code under Max as the single
capability floor (F19/F31 in [F-MODE-COVERAGE](../spec/C29-model-floor-stylesheet.md#6-failure-modes--handling)):

```
floor = { id: "claude-code@max", family: "claude", cost_tier: "standard" }
```

C28 *is* the floor. C29 routes coder nodes to it and enforces the floor clamp (any rule that
would route a coder node to a weaker model is overridden).

### 4.2 `modeldb` entries (Phase-0)

Per [C29 §4.2](../spec/C29-model-floor-stylesheet.md#42-modeldb-schema-sweep-2-per-d-10)
(`modeldb` fields = `{id, family, cost_tier}`, binding decision D-10):

| id | family | cost_tier |
|---|---|---|
| `claude-code@max` | `claude` | `standard` |
| `claude-haiku-3` | `claude` | `economy` |

### 4.3 Worked stylesheet example

The following is a complete Phase-0 stylesheet (stored in C03 config as TOML, sourced from
[C29 §3.3](../spec/C29-model-floor-stylesheet.md#33-stylesheet-grammar-sweep-2-deliverable--resolves-c29oq-on-concrete-grammar)):

```toml
# model-stylesheet.toml  — Phase-0 stylesheet
# Source: C29 §3.3 (CSS-cascade, selector → declaration)

# ── Floor anchor (required; absent = E-C29-05 at stylesheet load) ─────────────
[model_floor]
id        = "claude-code@max"
family    = "claude"
cost_tier = "standard"

# ── Judge independence policy (Phase-0: same-provider per D-1/FE-1) ───────────
[judge_policy]
independence_level   = "L1"    # L1 = same-provider judge, rig/role/prompt-isolated
cross_family_enforce = false   # false at Phase-0; true = FE-1 (future)

# ── Routing rules (top-to-bottom, first-match-at-equal-specificity wins) ──────

[[model_rule]]
role      = "coder"            # selector: matches node.role exactly (specificity = 1)
model_id  = "claude-code@max"  # declaration: route coder nodes to the floor
cost_tier = "standard"

[[model_rule]]
role      = "judge"            # selector (specificity = 1)
model_id  = "claude-haiku-3"   # Phase-0: same-provider economy-tier judge (D-1)
cost_tier = "economy"

[[model_rule]]
role      = "tool"             # selector (specificity = 1)
model_id  = "claude-code@max"
cost_tier = "economy"

[[model_rule]]
# catch-all (specificity = 0; must be last)
model_id  = "claude-code@max"
cost_tier = "standard"
```

**Cascade resolution example — coder node:**

- Input: `{role: "coder", stage: "phase-0"}`
- Rule 1 matches (role=coder, specificity=1); catch-all matches (specificity=0)
- Winner: Rule 1 → `claude-code@max`
- Floor clamp: `claude-code@max` IS the floor → no change
- Result: `ModelIdentity{id:"claude-code@max", family:"claude", cost_tier:"standard"}`

**Judge-independence note (D-1 same-provider ruling):** At Phase-0, the judge node runs on
`claude-haiku-3` (same `claude` family). Independence is supplied by **rig partitioning +
role/prompt isolation** (C42), not by model-family diversity. The literal cross-provider
`family(judge) ≠ family(coder)` constraint is future enhancement FE-1. The `cross_family_enforce`
boolean in `[judge_policy]` is the clean seam FE-1 switches on later without re-architecture.

---

## 5. Bring-Up & Smoke Test

### 5.1 Full bring-up sequence

```bash
# 0. Pre-stage binaries in image (gc, bd, dolt, node, claude) — see §1

# 1. In entrypoint.sh: write ~/.claude.json pre-acks (§2.3)
cat > /root/.claude.json <<JEOF
{ ... }   # see §2.3 copyable block
JEOF

# 2. Write .gc/site.toml rig path bindings
mkdir -p "${CITY_DIR}/.gc"
cat > "${CITY_DIR}/.gc/site.toml" <<EOF
workspace_name = "software-factory"
[[rig]]
name = "worker"
path = "${RIGS_DIR}/worker"
EOF

# 3. Install pack imports (idempotent)
cd "${CITY_DIR}"
gc import install

# 4. Start the controller
#    IS_SANDBOX=1 required (F12, harvest-verified); tmux provider (F7, harvest-verified)
IS_SANDBOX=1 exec gc start --foreground
```

### 5.2 Dispatch one bead and observe a turn

```bash
# Create a task bead in the worker partition (prefix r1-)
bd create --type task --rig worker --body '{"task": "Write hello-world.py"}' r1-task-001

# Verify the bead
bd get r1-task-001

# Sling to the worker agent (pool scales 0→1; new tmux pane spawned — F5, harvest-verified)
gc sling r1-task-001

# Watch the worker pane
gc session list          # worker pane appears?
tmux attach -t <worker-pane>   # or: tmux ls to find the pane name
```

### 5.3 What success looks like

| Signal | What to look for |
|---|---|
| `gc session list` shows a `worker` pane | C04 Start succeeded; E-C28-05/E-C28-01 not triggered |
| Pane shows `claude` prompt and active reasoning | Claude Code agent loop running; Max OAuth auth accepted |
| `claude_session_id` appears in JSONL output | C04 sessionlog seam working; C24 parent-chain key present |
| OTLP metrics appear at collector endpoint (60s cadence) | `CLAUDE_CODE_ENABLE_TELEMETRY=1` + `OTEL_METRICS_EXPORTER=otlp` working |
| Raw API body files appear in watched dir | `OTEL_LOG_RAW_API_BODIES=1` working → C24 bridge input |
| Worker pane produces output (file edits / bead state change) | C28 inner loop completed ≥1 turn; work product emitted |
| No interactive dialog visible in pane | `~/.claude.json` pre-acks effective (E-C28-01 not triggered) |

**Acceptance criterion AC-C28-01 (from [C28 §8](../spec/C28-claude-code-agent-loop.md#8-acceptance-criteria-sweep-2-ac-code-table)):**
Given a bead dispatched to the `implementer` rig worker; when C04 starts the `claude` session
with the env block from C28 §3.3; then a Claude Code process starts, runs a multi-turn loop,
dispatches at least one tool, and a `session.id`-attributed work product appears in the bead store.

---

## 6. Known Gaps / Needs-G11

### 6.1 Max → API-key fallback (G12 — undesigned)

> **[DEFERRED — G12]** The Max → API-key fallback is **named but not designed** in v4.
> C28 §3.3 I1 states OAuth tokens are never used outside the `claude` process (ToS hard
> constraint); AI-CONTEXT §4.1 confirms "No separate API key issued" under Max. If Max
> revokes unattended subprocess automation, a provider/auth swap would land behind C04's
> `runtime.Provider` interface (specifically the `Start` method's process-spawn + env
> injection — C04 §5.5 auth-swap seam). The fallback auth path itself is undesigned.
> G12 is shared between C28:OQ-1 and C04:OQ-1. Do not design the fallback on the canonical
> track; flag it as a latent contingency.

### 6.2 Token budget / rate limit on one Max seat (G13 / G32 / G34 → C46)

> **[DEFERRED — G13/G32/G34]** A single Claude Max subscription ($200/month) has unquantified
> per-minute and per-day rate limits. v4 has no token-budget model for L5-volume implementer
> runs. The cost signal C28 emits via OTLP (§3.5) is the input; the cost model is routed to
> **C46** (per D-24). Mitigations present in v4 today:
> - C29 model-floor/stylesheet routes cheaper cost tiers for judge/tool nodes
> - C04 session suspend/detach avoids idle Max burn
> - Throughput ceiling (G34) is shared with C04/C05 (C04 §7: C05 owns pool sizing; C29 owns
>   model routing); no multi-seat horizontal scale is specified for Phase-0
>
> Do not quantify or design the token budget on the canonical track. The rate-limit backoff
> path (E-C28-04) is native to Claude Code (exponential backoff on 429) and is already in
> the E-code taxonomy.

### 6.3 Hook / MCP field shapes (needs-G11 per C02/D-34)

> **[needs-G11]** The `[[hook]]` block shape (`event`, `command`, `args` fields) and the MCP
> `[[service]]` block shape (`protocol = "mcp"`, `command` field) in `pack.toml` are inferred
> from [C02 §3.3](../spec/C02-pack-extension-abi.md) but have not been verified against a
> pinned `gc` install. The conceptual shapes are correct; exact field names await G11.
>
> Concrete example (inferred; annotated per C28 §3.4):
>
> ```toml
> # pack.toml — C28 implementer pack hook/MCP declarations [inferred — needs-G11]
>
> [[hook]]                          # [needs-G11] block name
> event   = "PreToolUse"
> command = "bin/override-gate"
> args    = ["--tool-name", "{tool_name}", "--session-id", "{session_id}"]
>
> [[hook]]
> event   = "PostToolUse"
> command = "bin/telemetry-observe"
> args    = ["--tool-name", "{tool_name}", "--exit-code", "{exit_code}"]
>
> [[hook]]
> event   = "SessionStart"
> command = "bin/session-init"
> args    = ["--session-id", "{session_id}", "--workdir", "{workdir}"]
>
> [[service]]                       # [needs-G11] block name
> name     = "cxdb-mcp"
> protocol = "mcp"
> command  = "bin/cxdb-mcp-server"
> ```
>
> **D-34 (ADOPTED, 2026-06-01):** "Tool-node command-key field name is a source contradiction, G11-gated. AI-CONTEXT §13.3's `[[tool]]` sketch uses `command`; the prototype `pack/pack.toml` uses `cmd`. Specs MUST carry the spelling note and MUST NOT claim either spelling as verified." The same D-34 uncertainty applies to `[[hook]] command` / `[[hook]] cmd` — neither form is confirmed canonical until a pinned-`gc` run (G11). All `command` key spellings in the TOML fragments above carry this caveat per D-34.
>
> If the field shapes C28 consumes differ from what C02 specifies, that is a **seam conflict**
> that must be surfaced — do not silently paper over it.

### 6.4 OTEL key spelling (needs-G11)

> **[needs-G11]** The exact `OTEL_*` env var names listed in §2.2 are sourced from AI-CONTEXT
> §13.2 L572–580. The variable *concepts* are harvest-verified (F7/F12); the on-disk key
> spellings need a pinned-`gc` run (G11) for final freeze.

---

## References

- [C28 — Claude Code agent loop spec](../spec/C28-claude-code-agent-loop.md) — primary source for env contract, agent-loop interface, hook/MCP registration
- [C29 — Model floor & stylesheet routing spec](../spec/C29-model-floor-stylesheet.md) — stylesheet grammar, `modeldb` schema, judge independence policy
- [C04 — Session & provider runtime spec](../spec/C04-session-provider.md) — tmux provider, `gc start`, session lifecycle, onboarding prerequisites
- [Gas City integration runbook](./gascity-integration-runbook.md) — the prior operator task; cross-reference for config files, conformance gate, error table
- [D-23 substrate harvest](./D-23-substrate-harvest.md) — empirical evidence map (F7 tmux, F12 IS_SANDBOX/onboarding, F5 pool min=0)
- Prototype `entrypoint.sh` at `lago-morph/gascity-prototype@b14c278` — verified sandbox path for `CLAUDE_CODE_OAUTH_TOKEN`, CA-bundle, IS_SANDBOX, and onboarding pre-acks (see [D-23 substrate harvest](./D-23-substrate-harvest.md) F12)
- [Ambiguities and gaps register](./ambiguities-and-gaps.md) — G11, G12, G13, G32, G34 gap definitions
