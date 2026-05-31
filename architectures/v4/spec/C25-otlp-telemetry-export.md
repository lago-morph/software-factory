# C25 — OTLP telemetry export (`otlp-telemetry-export`)  (Spec, canonical track)

> Source: AI-CONTEXT §4.3 "Claude Code telemetry surface" (lines 156–180 — env-var config, three OTLP protocols, emitted signals, raw-bodies escape hatch, correlation attributes, export intervals); AI-CONTEXT §5.2 (line 210 — CXDB "no native OTLP receiver", positioned against OTel); AI-CONTEXT §5.4 (lines 222–232 — three bridge paths ranked by impedance, raw-API-bodies recommended); AI-CONTEXT §13.2 config block (lines 564–580 — `otel_collector` service + `[[agent]] env`); README §13.1 Phase 1 (lines 386, 411–413 — install OTel Collector to receive Claude Code OTLP; `CC -->|OTLP| OTel`, `CC -->|raw bodies| Bridge --> CX`); README §13.1 Phase-1 install checklist (lines 539–541); component-inventory line 37 (C25 row). Companion faithful specs: [`spec/C28-claude-code-agent-loop.md`](./C28-claude-code-agent-loop.md) (the agent that emits this telemetry), [`spec/C24-telemetry-cxdb-bridge.md`](./C24-telemetry-cxdb-bridge.md) (consumes the raw-bodies dir C25 produces), and the downstream [`spec/C26-otel-collector.md`](./C26-otel-collector.md) (the collector that receives this OTLP and owns the **anti-edge** Collector ✗→ CXDB, its INV-2) / [`spec/C27-langfuse-traces.md`](./C27-langfuse-traces.md) (the LangFuse trace sink), both authored this wave.
> Inventory ID: C25   Kind: interface   Status: sweep-1
> Maps from: A28b, A28c, A23. Depends on: C28 (Claude Code agent loop). Key gaps: G04. Related (downstream): C26 (collector), C27 (LangFuse), C24 (raw-bodies → CXDB bridge).

## 1. Purpose & responsibility

C25 is the **telemetry-export interface** of Software Factory v4: the seam by which **Claude Code's native OpenTelemetry surface** is configured and turned on so that the factory's agent activity leaves the agent process as structured, exportable signal. It is the **first stage of the observability pipeline** C25 → C26 (OTel Collector) → C27 (LangFuse), and it simultaneously feeds C24 (the raw-API-bodies → CXDB bridge) via the escape-hatch path (README:411–413, AI-CONTEXT §5.4). **The two sinks fork here — at the emitter (C25/C28) — not at any later stage** (README:411–413: the diagram diverges at `CC` into `OTLP| OTel` and `raw bodies| Bridge`); this is the load-bearing half of G04 (a reader who assumes the split happens "downstream" is exactly who wires OTLP→CXDB at the collector). C26's spec mirrors this ("the two sinks diverge at C25, not at C26").

C25 owns exactly **two export channels**, both native to Claude Code and both switched on purely by environment-variable configuration set in the Gas City session/agent config (AI-CONTEXT §13.2, lines 575–579):

1. **The OTLP channel** — Claude Code's native OpenTelemetry export of **metrics** and **events/logs** (and, behind a beta flag, **traces**) over OTLP to a configured endpoint (AI-CONTEXT:156–174). This is the structured-telemetry path consumed downstream by the OTel Collector (C26) → LangFuse (C27).
2. **The raw-API-bodies escape hatch** — `OTEL_LOG_RAW_API_BODIES=file:<dir>` dumps **untruncated request/response JSON** to a directory on disk; this output is "conversation-shaped, ideal for CXDB ingestion" (AI-CONTEXT:176) and is consumed by the C24 bridge.

C25's responsibility is the **configuration contract and the emission guarantees** of these two channels: *which env vars must be set, what signals/attributes/intervals result, what shape the raw-body files take, and where the two channels land.* It is the boundary that says "given Claude Code configured thus, this telemetry will appear at the OTLP endpoint and these files will appear in the raw-bodies dir." Everything downstream (receiving, fanning out, storing) belongs to C26/C27/C24.

> [FAITHFUL-FILL] v4 describes C25 entirely as **a surface Claude Code already provides plus the env vars that activate it** (AI-CONTEXT §4.3 is a description of Anthropic-supplied behaviour; inventory Kind = `interface`, not `component`). The minimal faithful framing is therefore that C25 is a **configuration-and-contract interface, not a piece of software we write**: it owns the env-var binding (in `city.toml`'s `[[agent]] env`, AI-CONTEXT:575–579) and the documented emission contract, and it asserts the channels' destinations. This is the smallest scope that makes "Claude Code native OTLP + raw-API-bodies escape hatch" a self-contained, referenceable component without absorbing the collector, LangFuse, or the bridge — each already its own inventory row (C26/C27/C24).

**What C25 is NOT:**

- It is **not** the OTel Collector. Receiving the OTLP stream, fanning it out, and forwarding to LangFuse is **C26** (inventory line 38: "Receives Claude Code OTLP, fans out to LangFuse"; README:411–412 `OTLP| OTel --> LF`). C25 *emits* to the collector's endpoint; it does not receive.
- It is **not** LangFuse / trace browsing. Session management and trace UI are **C27** (README:387). C25 is upstream of C27 by two hops.
- It is **not** the raw-bodies → CXDB bridge. Watching the `OTEL_LOG_RAW_API_BODIES` directory, posting to CXDB HTTP :9010, and defining delivery/ordering/back-pressure at that seam is **C24** (inventory line 39; README:389). C25 *produces* the directory of body files; C24 *consumes* it. The hard integration seam (G26/G27/G33) lives in C24, not C25.
- It is **not** CXDB. CXDB (C21) has **no native OTLP receiver** (AI-CONTEXT:210 / §5.2) and the OTLP→CXDB path is **considered and rejected** (AI-CONTEXT §11.1:466 + §11.3:497) — so the OTLP channel does *not* and must *not* terminate at CXDB; only the raw-bodies channel feeds CXDB, and only via the C24 bridge (this is the crux of G04 — see §6/§9).
- It is **not** the agent loop. The multi-turn reasoning that *generates* the telemetry is **C28** (which "emits telemetry", inventory relation). C25 is the export configuration around C28's process, not the agent itself.
- It is **not** an OTLP exporter implementation. The exporter is native to the Claude Code binary (Anthropic-supplied, AI-CONTEXT:158 "Native OpenTelemetry support"). C25 does not implement OTLP; it configures Claude Code's built-in exporter.

## 2. Context & dependencies

| Direction | Component | Relationship (v4 source) |
|---|---|---|
| Upstream (emits) | **C28** Claude Code agent loop | C28 is the process whose activity produces metrics/events/traces and raw API bodies; "emits telemetry" (inventory relation). C25's env vars configure C28's native exporter. Hard inventory dependency (`Depends on: C28`). |
| Upstream (carries config) | **C03** config / feature-flags + **C04** session/provider | The activating env vars live in `city.toml`'s `[[agent]] env` (AI-CONTEXT:575–579), set when the agent's session is stood up (C04). Section/var presence = capability on (C03's feature-flag convention). Soft — C25 is the *contract* over that config. |
| Downstream (OTLP) | **C26** OTel Collector | C25 exports OTLP to the collector's endpoint (`OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317`, AI-CONTEXT:578; README:411). First → second stage of the pipeline. |
| Downstream (OTLP, transitively) | **C27** LangFuse | C26 fans the OTLP stream out to LangFuse for trace browsing (README:412 `OTel --> LF`). C25 is two hops upstream. |
| Downstream (raw bodies) | **C24** telemetry → CXDB bridge | C25's `OTEL_LOG_RAW_API_BODIES` directory is exactly C24's input; C24 watches it and posts to CXDB HTTP (README:389, 413). Parallel sink to the OTLP path. |
| Lateral (sink it must NOT hit) | **C21** CXDB | CXDB has no OTLP receiver (AI-CONTEXT:210 / §5.2) and the OTLP→CXDB path is rejected (AI-CONTEXT §11.1:466 + §11.3:497); the OTLP channel must terminate at C26, never directly at CXDB (the anti-edge is enforced at C26 INV-2). The CXDB-bound data goes only via the raw-bodies → C24 path. |

C25 sits in the **Observability** subsystem and is **not foundational** (inventory: Foundational? = no). It is a **Batch-2** component (inventory: "observability ingest **C25, C26, C27, C24** … OTLP→collector→LangFuse, CXDB bridge"), depending on the Batch-2 agent loop (C28) and on the Batch-1 config/session substrate (C03/C04) that carries its env vars.

## 3. Interfaces / contracts

Sweep-1: interfaces **named + described**. Concrete env-var matrices, the OTLP signal schemas, and the raw-body file-naming contract are deferred to sweep 2; the names and shapes below are taken verbatim from AI-CONTEXT §4.3.

### 3.1 Inbound — activation config (C03/C04 `[[agent]] env` → C25)

The set of environment variables that turn the channels on (AI-CONTEXT:161–164, 575–579):

| Env var | Role (v4 source) |
|---|---|
| `CLAUDE_CODE_ENABLE_TELEMETRY=1` | Master switch for telemetry; works under Max with no API key (AI-CONTEXT:158, 161). |
| `OTEL_METRICS_EXPORTER=otlp` | Selects OTLP as the metrics export protocol (AI-CONTEXT:162). |
| `OTEL_LOGS_EXPORTER=otlp` | Selects OTLP as the events/logs export protocol (AI-CONTEXT:163). |
| `OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317` | The collector endpoint (C26); gRPC default :4317 (AI-CONTEXT:164, 167). |
| `OTEL_LOG_RAW_API_BODIES=file:<dir>` | Activates the escape hatch; dumps untruncated request/response JSON to `<dir>` (AI-CONTEXT:176; e.g. `file:/var/lib/cxdb-bridge/inbox`, AI-CONTEXT:579). |
| `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1` | (Optional) enables distributed traces across prompts → API calls → tool executions (AI-CONTEXT:174). |
| mTLS / per-signal vars | `OTEL_EXPORTER_OTLP_CLIENT_KEY`/`_CERTIFICATE` (gRPC), `CLAUDE_CODE_CLIENT_CERT`/`_KEY` (HTTP), headers, per-signal endpoints (AI-CONTEXT:169). |
| `OTEL_METRIC_EXPORT_INTERVAL` / `OTEL_LOGS_EXPORT_INTERVAL` | Export cadence; metrics 60s default, logs 5s default (AI-CONTEXT:180). |

> [FAITHFUL-FILL] v4 lists these vars across AI-CONTEXT:161–180 and the §13.2 config block but never gives a single normative "minimum activation set." The minimal faithful reading: the **required** set is the five vars in AI-CONTEXT:575–579 (`CLAUDE_CODE_ENABLE_TELEMETRY`, `OTEL_METRICS_EXPORTER`, `OTEL_LOGS_EXPORTER`, `OTEL_EXPORTER_OTLP_ENDPOINT`, `OTEL_LOG_RAW_API_BODIES`) — exactly the block v4 ships as the working config; the rest (`..._BETA`, mTLS, interval, per-signal) are **optional refinements** v4 names but does not require at Phase 1. A full normative matrix (defaults, allowed values per protocol) is a sweep-2 concern.

### 3.2 Outbound — the two channels

- **OTLP channel (C25 → C26).** Claude Code's native exporter pushes **metrics** and **events/logs** (and beta **traces**) over OTLP to `OTEL_EXPORTER_OTLP_ENDPOINT`. Three protocols are available (AI-CONTEXT:167): **gRPC** (default :4317), **HTTP/JSON** (:4318), **HTTP/protobuf** (:4318). The v4 working config uses gRPC :4317 (AI-CONTEXT:578). Postcondition: telemetry of the emitted-signal set (§3.3) appears at the collector endpoint on the configured cadence.
- **Raw-bodies channel (C25 → C24).** When `OTEL_LOG_RAW_API_BODIES=file:<dir>` is set, Claude Code writes **untruncated request/response JSON** to `<dir>` as files; the content is "conversation-shaped" (AI-CONTEXT:176). Postcondition: each API exchange yields body content on disk in `<dir>` that the C24 bridge can read and post to CXDB.

### 3.3 Emitted signals & correlation (the contract C26/C27/C24 read)

- **Metrics** (AI-CONTEXT:172): session count, lines of code, PRs, commits, costs, token usage, edit decisions, active time.
- **Events/logs** (AI-CONTEXT:173): user prompts, tool results, API requests/errors, tool decisions, permission changes, auth, MCP connections, plugins, skills.
- **Traces (beta)** (AI-CONTEXT:174): distributed tracing across user prompts → API calls → tool executions, gated by `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1`.
- **Correlation attributes** carried on the signals (AI-CONTEXT:178): `prompt.id`, `session.id`, `user.account_uuid`, `organization.id`, `terminal.type`. **`session.id` is the load-bearing correlation key** for the CXDB parent-chain (AI-CONTEXT §5.4 line 229 "parent-chain via `session.id`"). These are **Anthropic-native** attributes emitted by Claude Code's built-in exporter (AI-CONTEXT:178); C25 — a config-only interface that does *not* implement the exporter (INV-2) — therefore **relies on and asserts** this native property (it does not itself enforce it), and the Phase-1 fixture **verifies** `session.id` is present on the raw bodies (AC-5) so C24 can build CXDB turn lineage.

### 3.4 Invariants

- **INV-1 (two parallel sinks, never crossed).** The OTLP channel terminates at C26 (the collector); the raw-bodies channel terminates in the on-disk dir for C24. These are **two separate sinks** that **fork at the emitter (C25/C28), not at any later stage** (README:411 `OTLP| OTel`, line 413 `raw bodies| Bridge` — both edges leave `CC`). The OTLP channel is **never** wired to CXDB: CXDB has **no native OTLP receiver** (AI-CONTEXT:210 / §5.2) and the OTLP→CXDB path is **considered and rejected** (AI-CONTEXT §11.1:466 + §11.3:497). The downstream *enforcement* of that anti-edge — the rule that the collector must not export to CXDB — is **C26 INV-2**; the matching "no spans to CXDB" guarantee on the consume side is **C24 INV-6**. C25 owns the *split*; C26 owns the *anti-edge*. *(This invariant is the resolution of G04 — see §6/§9.)*
- **INV-2 (native exporter, config-only activation).** C25 introduces no new exporter code; the channels are activated solely by setting the §3.1 env vars on the Claude Code process (AI-CONTEXT:158 "Native OpenTelemetry support, configurable via env vars"). Turning telemetry off = unsetting `CLAUDE_CODE_ENABLE_TELEMETRY` / `OTEL_LOG_RAW_API_BODIES`.
- **INV-3 (`session.id` present on CXDB-bound data).** Every raw-body artifact the escape hatch writes carries enough identity — at minimum `session.id` (AI-CONTEXT:178, 229) — for C24 to derive the CXDB parent-chain. This is an **adopted native-exporter property** C25 **asserts and relies on** (the attributes are Anthropic-emitted, AI-CONTEXT:178; INV-2 — C25 configures, it does not implement the exporter), **verified by the Phase-1 fixture (AC-5)** rather than independently enforced by C25-the-spec; the *mapping rule* to CXDB's parent pointer is C24's (G26).
- **INV-4 (Max-compatible, no API key).** The telemetry surface "Works under Max with no API key" (AI-CONTEXT:158); C25's activation must not require an Anthropic API key, only the Max-authenticated Claude Code process.

> [FAITHFUL-FILL] INV-1…INV-4 are not stated verbatim as "invariants" in v4 but each is a direct restatement of an explicit v4 fact: two separate sinks (README:411–413 + AI-CONTEXT:210), native config-only activation (AI-CONTEXT:158), `session.id` as the parent-chain key (AI-CONTEXT:229), and Max-no-key operation (AI-CONTEXT:158). They are the minimal constraints that make the one-line responsibility ("native OTLP + raw-API-bodies escape hatch") well-defined without adding scope.

## 4. Data model / state

C25 is an **export interface**, not a data store. It owns no durable state; its "state" is (a) the activating env-var binding in config and (b) the transient on-disk raw-body files that exist until C24 consumes them.

| Aspect | Faithful spec (v4 source) |
|---|---|
| Owned artifact | None durable of its own. The OTLP stream is owned downstream by C26; the metrics/events schemas are Anthropic-defined (AI-CONTEXT:172–174). |
| Activation state | The §3.1 env vars in `city.toml` `[[agent]] env` (AI-CONTEXT:575–579) — version-controlled config owned by C03; C25 is the contract over it. |
| Raw-body files | Transient files in `OTEL_LOG_RAW_API_BODIES=file:<dir>` (e.g. `/var/lib/cxdb-bridge/inbox`, AI-CONTEXT:579). Written by Claude Code; lifetime = until C24 reads/removes them. **C25 produces; C24 owns the consume/retention lifecycle** (G26 territory). |
| Correlation keys | `prompt.id`, `session.id`, `user.account_uuid`, `organization.id`, `terminal.type` (AI-CONTEXT:178), rendered onto signals/bodies by the native exporter. |
| Persistence | None owned. OTLP is fire-and-export to C26 on a cadence; raw bodies persist on disk only until drained. |
| Consistency | Export cadence (metrics 60s, logs 5s defaults, AI-CONTEXT:180) is the temporal consistency point for the OTLP channel; the raw-bodies dir is eventually-consistent w.r.t. the agent's API calls (a body appears after each exchange). |

> [FAITHFUL-FILL] v4 gives the raw-body files no naming scheme, no completion/rename protocol, and no retention rule. Faithful reading at sweep 1: C25 simply asserts "files appear in `<dir>`"; the **partial-write / atomic-completion / retention** questions are explicitly C24's seam (G26 lists "partially-written body files" and back-pressure as C24-owned). C25 does not invent a file protocol here; it defers the consume-side lifecycle to C24 (§9 OQ-2).

## 5. Behavior

The flow is **configure → emit → two sinks**:

```mermaid
flowchart LR
    CFG[C03/C04 city.toml<br/>[[agent]] env vars] -->|activate| CC[C28 Claude Code<br/>native OTel exporter]
    CC -->|OTLP metrics/events/traces<br/>:4317 gRPC| OTEL[C26 OTel Collector]
    OTEL -->|fan-out| LF[C27 LangFuse]
    CC -->|raw API bodies JSON<br/>OTEL_LOG_RAW_API_BODIES dir| DIR[(raw-bodies dir<br/>/var/lib/cxdb-bridge/inbox)]
    DIR -->|watch + post :9010| BR[C24 bridge] --> CX[(C21 CXDB)]
    CC -. NOT wired .-x|no OTLP receiver| CX
```

Key flow notes:
- **Configure.** The §3.1 env vars are set on the agent process via `city.toml` `[[agent]] env` when C04 stands up the session (AI-CONTEXT:575–579). No code is deployed; activation is declarative.
- **Emit (OTLP).** Claude Code's native exporter pushes metrics (60s default) and events/logs (5s default) over OTLP gRPC to :4317 (C26), plus beta traces if the beta flag is set (AI-CONTEXT:172–180).
- **Emit (raw bodies).** In parallel, each API request/response is dumped untruncated to the configured dir (AI-CONTEXT:176), carrying the `session.id` correlation key (INV-3).
- **Two sinks diverge.** The OTLP stream goes collector → LangFuse (README:411–412). The raw bodies go dir → C24 bridge → CXDB (README:413). The two paths never cross; OTLP is never sent to CXDB (INV-1; AI-CONTEXT:210).
- **Verify.** Phase-1 acceptance is literally "Verify events flow" into the collector (README:539) and that the raw-bodies bridge is the "first non-trivial integration" (README:541) — C25's part is proving telemetry leaves the agent and lands at both sinks.

## 6. Failure modes & handling

| F-mode | Applies to C25 how | v4 handling (faithful) |
|---|---|---|
| **G04** (CXDB vs OTel framing tension) | A naive integrator wires the OTLP channel into CXDB — the explicitly-rejected path (CXDB has **no native OTLP receiver**, AI-CONTEXT:210 / §5.2; the OTLP→CXDB path is **considered and rejected**, AI-CONTEXT §11.1:466 + §11.3:497). | **Resolved by INV-1:** C25's contract states the OTLP sink is **C26 only**; CXDB is fed **only** by the raw-bodies → C24 path. The split forks at the **emitter (C25/C28)**, not at any later stage; the *anti-edge* enforcement (Collector ✗→ CXDB) is C26 **INV-2**. The spec names the two sinks explicitly (the thing G04 says v4 "never stated"). See §9 OQ-1. |
| **F42** Cognitive-Escrow Negligence | Operators stop watching the telemetry; the observability surface exists but is ignored. | Layer-3 observability + re-engagement surface design (F-MODE F42, **Partial — operator-side discipline still required**). C25 *provides* the signal; the re-engagement UI is C27/Layer-3, not C25-native. |
| **F22** Zombie agents (downstream enabler) | A stalled agent must be detectable; detection relies on liveness telemetry. | C25 is the *source*: "Anomaly detection on session liveness (PyOD on telemetry)" (F-MODE F22, **Addressed**) depends on C25 emitting session/active-time metrics (AI-CONTEXT:172). C25's contribution is faithful emission; the detection loop is downstream (Layer-4). |
| **F21** Context-window exhaustion (downstream enabler) | Detecting exhaustion needs token-usage telemetry. | "Runtime provides observability to detect exhaustion but doesn't prevent it" (F-MODE F21). C25 emits token-usage metrics (AI-CONTEXT:172); prevention is methodology, not C25. |
| **Collector-down** (interface-local) | The OTLP endpoint (C26 :4317) is unreachable; exports fail. | v4 says **nothing** about OTLP buffering/back-pressure when the collector is down (this is part of G33's "no story for partial/cascading failure of the OSS stack"). Faithful disposition: the exporter's behaviour on an unreachable endpoint is **Anthropic-native** (drop/retry per the SDK exporter) and **not specified by v4**; C25 cannot guarantee delivery beyond what Claude Code's exporter does. **Deferred** to C26/G33 (§9 OQ-3). |
| **Raw-bodies dir back-pressure** (interface-local) | The dir fills (disk pressure) or C24 stops draining. | The drain/back-pressure/partial-write handling is **C24's seam** (G26, G33). C25's faithful boundary: it produces files; what happens when CXDB/C24 is down (disk fills) is owned by C24's design, **deferred** here. |

> [FAITHFUL-FILL] "Collector-down" and "raw-bodies back-pressure" are interface-local conditions v4 does not address for C25 (they fall under G33, which the inventory assigns to C24, not C25). Faithful reading: C25's delivery semantics are **whatever Claude Code's native exporter and the OS filesystem provide** — v4 specifies no buffering layer at the emit side. The minimal consistent choice is to **state this explicitly and defer** the durability story to the receiving components (C26 for OTLP, C24 for raw bodies), since v4 places the only named integration-hardening budget there (README:541, G26/G33).

## 7. Cross-cutting (security / cost / scale / observability / ops)

- **Security.** The transport supports **mTLS** (gRPC: `OTEL_EXPORTER_OTLP_CLIENT_KEY`/`_CERTIFICATE`; HTTP: `CLAUDE_CODE_CLIENT_CERT`/`_KEY`) and custom headers (AI-CONTEXT:169) — faithful security posture for the OTLP channel. The **raw-API-bodies are untruncated request/response JSON** (AI-CONTEXT:176): they contain full prompt/response content and correlation identity (`user.account_uuid`, `organization.id`), so the dir (`/var/lib/cxdb-bridge/inbox`) is **sensitive at rest** — file-system permissions on that dir are the faithful control; data-at-rest handling beyond the dir is C24/CXDB's. C25 introduces no new secret beyond the optional mTLS material.
- **Cost.** Activation is config-only — no runtime cost beyond the native exporter's overhead. The escape hatch dumps **untruncated** bodies, so disk cost scales with conversation volume; retention/rotation is a C24/ops concern (G26). The telemetry surface works under **Max with no API key** (AI-CONTEXT:158, INV-4) — no incremental API cost.
- **Scale.** Export cadence (metrics 60s, logs 5s, AI-CONTEXT:180) bounds OTLP volume; intervals are tunable via `OTEL_METRIC_EXPORT_INTERVAL` / `OTEL_LOGS_EXPORT_INTERVAL`. Raw-body volume scales 1:1 with API exchanges — the load-bearing scale concern for the *bridge* (C24), not C25's emission.
- **Observability (of itself).** C25 *is* the observability source; its own health is "do events flow?" — the Phase-1 acceptance check (README:539). Whether the exporter is succeeding/failing to reach C26 is observable only via the collector side (C26) at this sweep.
- **Ops.** Turning telemetry on/off and pointing it at a different collector is a `city.toml` (C03) edit + commit (AI-CONTEXT:575–579) — declarative, no redeploy of C25 itself. The Phase-1 sequencing (README:539–541) is: stand up C26 → verify flow → install LangFuse/point collector at it → install CXDB + build the C24 bridge ("budget a week").

## 8. Acceptance criteria & test strategy

Sweep-1 acceptance (high-level):
1. **AC-1 (telemetry activates from config).** Setting the five §3.1 required env vars (AI-CONTEXT:575–579) on a Max-authenticated Claude Code process (no API key) causes telemetry to be emitted — "Verify events flow" (README:539; INV-2, INV-4).
2. **AC-2 (OTLP lands at the collector).** With `OTEL_EXPORTER_OTLP_ENDPOINT=:4317`, metrics and events/logs appear at the C26 collector endpoint over OTLP gRPC on the configured cadence (AI-CONTEXT:164,167,180).
3. **AC-3 (emitted-signal contract).** The metric set (session/LOC/PRs/commits/cost/tokens/edits/active-time) and event set (prompts/tool-results/API/decisions/auth/MCP/plugins/skills) per AI-CONTEXT:172–173 are present in the OTLP stream; beta traces appear iff `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1` (AI-CONTEXT:174).
4. **AC-4 (raw-bodies escape hatch).** With `OTEL_LOG_RAW_API_BODIES=file:<dir>`, untruncated request/response JSON appears as files in `<dir>` for each API exchange (AI-CONTEXT:176).
5. **AC-5 (`session.id` present).** Both channels carry the correlation attributes (AI-CONTEXT:178), and every raw-body artifact carries `session.id` so C24 can build the CXDB parent-chain (INV-3; AI-CONTEXT:229).
6. **AC-6 (two sinks, never crossed).** The OTLP stream is observed terminating at C26 (→ C27) and the raw bodies at the C24 dir; **no OTLP is sent to CXDB** (INV-1; CXDB has no OTLP receiver, AI-CONTEXT:210; OTLP→CXDB rejected, AI-CONTEXT §11.1:466 + §11.3:497). This is the G04 acceptance check; it mirrors C26 AC-3 (no CXDB exporter on the collector pipeline).
7. **AC-7 (config-only off).** Unsetting `CLAUDE_CODE_ENABLE_TELEMETRY` / `OTEL_LOG_RAW_API_BODIES` stops the respective channel with no code change (INV-2).

Test strategy (sweep-1): a Phase-1 fixture — one `[[agent]]` with the AI-CONTEXT:575–579 env block, a stub OTLP receiver standing in for C26 listening on :4317, and a scratch raw-bodies dir. Drive one short agent run; assert (a) metrics+events arrive at the stub receiver (AC-1/AC-2/AC-3), (b) untruncated body files appear in the dir carrying `session.id` (AC-4/AC-5), (c) nothing is posted to a CXDB endpoint by C25 itself (AC-6 — only C24 does that), and (d) unsetting the vars silences each channel (AC-7). Concrete env-var defaults matrix, OTLP signal schemas, and the raw-body file-naming/completion contract are deferred to sweep 2 (coordinated with C24).

## 9. Open questions

- **OQ-1 (→ [review-log](../_meta/review-log.md), top open question) — G04 two-sinks statement.** v4 is consistent but never says "two separate sinks" out loud, so a naive integrator may wire OTLP → CXDB (the rejected path: CXDB has no OTLP receiver, AI-CONTEXT:210 / §5.2; rejection at AI-CONTEXT §11.1:466 + §11.3:497). **Faithful resolution adopted:** INV-1 + AC-6 state explicitly that the OTLP channel terminates at C26 only and CXDB is fed *only* by raw-bodies → C24. **RESOLVED by D-12:** the two-sink rule stays as **cross-referenced per-spec notes** — the **fork** is stated **here at C25** (the source), the **Collector✗→CXDB anti-edge** at **C26** (INV-2), with **C24/C27** cross-referencing. **No new shared subsystem doc** (avoids scope creep). C25 is where the split originates, so it carries the fork statement; the others cross-reference it.
- **OQ-2 — raw-body file protocol seam (shared with C24, G26).** v4 gives the escape-hatch files no naming, atomic-completion, or retention contract. C25 faithfully *produces* files and defers the partial-write / completion-marker / drain-and-delete protocol to C24's consume side (G26). The shared question: is atomic-rename-on-complete an emit-side guarantee C25 should assert (if Claude Code provides it) or purely a C24 tolerance concern? Resolve jointly with the C24 author at sweep 2.
- **OQ-3 — emit-side durability when C26 is down (G33).** v4 specifies no buffering/back-pressure for the OTLP channel when the collector is unreachable; the exporter's behaviour is Anthropic-native and undocumented in v4. Deferred to C26/G33 — but flag whether any local OTLP buffer (file-based) is wanted before C26, or whether dropped telemetry during collector downtime is acceptable (faithful default: accept native exporter behaviour; do not add a buffer v4 doesn't name).
