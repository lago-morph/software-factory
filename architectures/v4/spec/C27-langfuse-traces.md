# C27 — LangFuse trace store & browser (`langfuse-traces`)  (Spec, Track A)

> Source: README §13.1 Phase 1 (lines 387, 406, 412 — "Install LangFuse self-hosted for trace browsing + session management"; `OTel --> LF` in the Phase-1 diagram), README §13.1 install checklist (line 540 — "Install LangFuse self-hosted, point the OTel Collector at it. Verify trace browsing works"), README license table (lines 294–295, 333 — LangFuse self-host is "clean"; Phoenix Elastic License rejected, "Use LangFuse instead"); AI-CONTEXT §7 Layer-3 table (lines 313, 315, 316 — LLM event storage / trace browsing / session-conversation = LangFuse) and §8 multi-capability table (line 374 — "LangFuse: L3: storage + browsing + session + prompt versioning; weak L4 fallback"), AI-CONTEXT §13.2 config block (lines 552–555 — `[[service]] name="langfuse" type="external" endpoint="http://localhost:3000"`), AI-CONTEXT §15.1 (line 637 — repo `github.com/langfuse/langfuse`); component-inventory line 39 (C27 row: "Self-hosted LLM trace browsing + session/prompt versioning"; Depends on C26; Key gaps G37). Companion faithful specs: [`spec/C25-otlp-telemetry-export.md`](./C25-otlp-telemetry-export.md) (the export surface, and the off-the-shelf-config-not-daemon framing this spec mirrors), [`spec/C26-otel-collector.md`](./C26-otel-collector.md) (the upstream collector that exports OTLP into C27 — authored in parallel this wave), and the lateral [`spec/C24-telemetry-cxdb-bridge.md`](./C24-telemetry-cxdb-bridge.md) (the *other* sink — raw bodies → CXDB — which C27 is explicitly NOT).
> Inventory ID: C27   Kind: data-store   Status: sweep-1
> Maps from: A25, A24b, B48. Depends on: C26 (OTel Collector). Key gaps: G37. Related: C25 (export surface, two hops upstream), C24 (the lateral CXDB sink C27 is not).

## 1. Purpose & responsibility

C27 is the **trajectory-browsing sink** at the terminal end of Software Factory v4's OTLP observability pipeline: a **self-hosted deployment of LangFuse** (the off-the-shelf, Apache-2.0/MIT-licensed LLM observability platform) that **receives the OTLP stream forwarded by the OTel Collector (C26), stores it as browsable LLM traces, and gives a human operator a UI** to inspect what the agents did — sessions, prompts, model calls, costs, and timings — and to version prompts/sessions over time (README:387; AI-CONTEXT:374). It is the third and final stage of the pipeline **C25 (Claude Code native OTLP) → C26 (Collector) → C27 (LangFuse)** (README:411–412 `CC -->|OTLP| OTel --> LF`).

C27's responsibility is captured almost entirely by **"deploy and configure a piece of OSS"**, not "write software." Mirroring how C25 is specced as *config, not a daemon we author*, C27 is specced as:

1. **A deployment** — stand up self-hosted LangFuse (its standard docker-compose stack: the LangFuse server + its backing Postgres + ClickHouse/object-store as the LangFuse release requires) as an `external` service in the Gas City service registry (AI-CONTEXT:552–555).
2. **A configuration contract** — register it at its endpoint (`http://localhost:3000`, AI-CONTEXT:555), provision the credentials it needs (DB password, project/API keys), and **point C26's OTLP exporter at LangFuse's OTLP ingestion endpoint** so traces land (README:540).
3. **The capability it thereby gives us** — **trace/session browsing + prompt versioning** for the factory's agent activity: the human-facing "what happened, and why" surface that satisfies the **P12 (observability)** principle's *inspectability* requirement and underpins the operator re-engagement guard for F42 (README:387; AI-CONTEXT:374).

The custom-code budget for C27 is **near zero**: a service-registry entry, a docker-compose/env deployment, the C26→LangFuse endpoint wiring, and an acceptance check that "trace browsing works" (README:540). We do **not** author LangFuse, its storage, or its UI.

> [FAITHFUL-FILL] v4 never specifies *how* LangFuse ingests from the collector — README:540 says only "point the OTel Collector at it." LangFuse exposes a **native OTLP-trace ingestion endpoint** (`/api/public/otel`, signal path `/api/public/otel/v1/traces`), which is the mechanism by which a generic OTel Collector forwards traces to LangFuse; this is the minimal consistent reading of "point the collector at it" (it requires no custom receiver and matches LangFuse's documented OSS capability — AI-CONTEXT:374 "storage + browsing"). LangFuse's OTLP ingestion is **OTLP/HTTP only** (HTTP/JSON or HTTP/protobuf; **gRPC is not supported** at the LangFuse seam) and authenticates with **HTTP Basic auth** from the base64-encoded `public_key:secret_key` pair — so C26 targets it with its `otlphttp` exporter (consistent with C26 §3.2). LangFuse's OTLP receiver is **trace-oriented** (it ingests trace/observation spans, not metrics/logs — see §3.1 and OQ-1). The exact endpoint path / version header / OTLP exporter block is a sweep-2 concern, coordinated with the C26 author. See §3.1 and §9 OQ-1.

> [FAITHFUL-FILL] v4 lists LangFuse's license **inconsistently**: README:294 calls the self-host "MIT (most) / MIT core," while AI-CONTEXT:313–316/326/374 repeatedly rate it "Apache 2.0." Both readings agree on the only load-bearing fact — **the self-hosted core is a permissive, cleanly self-hostable OSS license** (explicitly contrasted with Phoenix's restrictive Elastic License, which v4 rejects "for hosted-service paths," README:295/333). C27 relies only on that fact; pinning the exact SPDX identifier of the chosen LangFuse release is a deployment-time check (§9 OQ-3), not an architecture decision.

**What C27 is NOT:**

- It is **not** the OTel Collector and does **not** receive Claude Code's OTLP directly. Receiving the agent's raw OTLP and fanning it out is **C26** (inventory line 38; README:411–412 `OTLP| OTel --> LF`). C27 is downstream of C26 and ingests **from** the collector, not from C25.
- It is **not** the export surface. The env-var-activated native OTLP emission is **C25** (AI-CONTEXT:158); C27 is two hops downstream of it.
- It is **not** the CXDB sink and is **not** on the path to CXDB. The factory has **two separate sinks** (the G04 two-sinks rule): the OTLP path ends here at LangFuse (trace browsing), and the **other** path — raw API bodies → **C24** bridge → **C21** CXDB — is entirely separate (README:411–413). C27 is a **terminal sink**: it consumes OTLP and is **not a source for CXDB, anomaly detection (C36), clustering (C37), or counterfactual replay (C49)** — those read CXDB, never LangFuse. (AI-CONTEXT:326/374 note LangFuse *could* be a "weak L4 fallback" event substrate; v4 does **not** choose that path — CXDB is the L4 substrate — so C27 stays a browsing sink only. See §9 OQ-2.)
- It is **not** a custom trace store or custom UI. The data model, storage engine, and browser are LangFuse's, off the shelf (AI-CONTEXT:374). We add no custom storage schema, no custom UI, and no hardening over what LangFuse provides natively.
- It is **not** a secrets manager. The credentials LangFuse requires live in `city.toml`/env as plaintext today (G37); C27 consumes them and does **not** introduce a secrets-management layer. The unbuilt secrets-store gap is tracked as the open gap **G37** (canonical resolution owned by **C03**, the config owner — §9 OQ-4); it is *not* a Future-Enhancements item (FE-3 is the signing/key model, itself *blocked on* G37). See §6/§7/§9 OQ-4.
- It is **not** the override-"why" capture loop. Operator-override detection and "why"-field logging are **C35** (AI-CONTEXT:317–319, "Small custom"/DIY hooks). C27 provides the *browsing* surface; the override-discipline loop is separate.

## 2. Context & dependencies

| Direction | Component | Relationship (v4 source) |
|---|---|---|
| Upstream (ingests from) | **C26** OTel Collector | C26 fans the Claude Code OTLP stream out and **exports it to LangFuse** (README:412 `OTel --> LF`; line 540 "point the OTel Collector at it"). This is C27's only inbound data path. Hard inventory dependency (`Depends on: C26`). |
| Upstream (transitively) | **C25** OTLP export | C25 is the native emission surface; C26 receives it; C27 is two hops down. C27 inherits the emitted-signal + correlation contract (incl. `session.id`) that C25 guarantees (C25 §3.3). |
| Upstream (deployment substrate) | **C01** Gas City + **C03** config | LangFuse is registered as an `[[service]] type="external"` in `city.toml` (AI-CONTEXT:552–555); C03's config layer carries the endpoint and the credential env. C27 is the *deployment + contract* over that registry entry. |
| Consumer (human) | **Operator** (Layer-3 / P12) | The human inspects sessions/traces/prompts via LangFuse's UI at `:3000` — the "why did the agent do that" surface (README:387; AI-CONTEXT:374). This is C27's only "downstream": a person, not another component. |
| Lateral (the sink C27 is NOT) | **C24 → C21** raw-bodies bridge → CXDB | The parallel, separate sink for conversation-shaped data (README:413). C27 and C24 never exchange data; the two-sinks rule (G04) keeps them disjoint. |

C27 sits in the **Observability** subsystem and is **not foundational** (inventory: Foundational? = no). It is a **Batch-2** component (inventory: "observability ingest **C25, C26, C27, C24** … OTLP→collector→LangFuse"), depending on C26 (built in parallel this wave) and on the Batch-1 substrate/config (C01/C03) that registers it.

## 3. Interfaces / contracts

Sweep-1: interfaces **named + described**. Concrete OTLP-ingestion endpoint paths, the LangFuse trace/session/prompt data-model fields, the docker-compose service set, and the env-var/credential matrix are deferred to sweep 2 (coordinated with C26). The names/shapes below are LangFuse-native (off the shelf) plus the v4 registry binding.

### 3.1 Inbound — OTLP trace ingestion (C26 → C27)

The single inbound data interface: **LangFuse's OTLP-trace ingestion endpoint**, to which the C26 collector exports the agent OTLP stream (README:540; mechanism per the §1 FAITHFUL-FILL). The contract C27 publishes to C26:

| Aspect | Sweep-1 contract (v4 source / LangFuse-native) |
|---|---|
| Endpoint | LangFuse OTLP ingestion (HTTP), reachable at the LangFuse service address (`http://localhost:3000`, AI-CONTEXT:555; concrete path → sweep 2 / OQ-1). |
| Payload | **OTLP traces only.** LangFuse's OTLP endpoint ingests OTLP **trace/observation spans**; it does **not** ingest OTLP metrics or logs (verified against LangFuse's OTel docs). Distributed traces are gated upstream by Claude Code's `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA` (C25 §3.3); C27 stores the **trace** spans C26 forwards. **Seam note (OQ-1):** C26 §3.3 currently pipelines metrics + logs/events **and** traces to this endpoint, but only traces are ingestible here — the metrics/logs disposition is a **C26-side** decision to resolve jointly (see OQ-1). |
| Auth | LangFuse **HTTP Basic auth** built from the base64-encoded **`public_key:secret_key`** pair (provisioned at deploy); C26's `otlphttp` exporter presents it as the `Authorization: Basic …` header (exact construction + `x-langfuse-ingestion-version` header → sweep 2 / OQ-1). This is the published auth shape C26 binds against, and is part of the G37 credential surface (§7). |
| Correlation | C27 relies on the **upstream correlation set C26 forwards unaltered** (C26 INV-4: `prompt.id`, `session.id`, `user.account_uuid`, `organization.id`, `terminal.type` — AI-CONTEXT:178), with **`session.id`** (C25 §3.3) as the **grouping key** so the UI can group spans into **sessions**. LangFuse's session/trace grouping is native; C27 does not compute it. |
| Postcondition | Forwarded spans become **browsable traces/sessions** in the LangFuse UI within LangFuse's ingestion latency. |

### 3.2 Inbound — operator browsing (human → C27)

LangFuse's **native web UI** at `:3000` (AI-CONTEXT:555): the human operator authenticates and browses **traces, sessions, model calls, token/cost metrics, and prompt versions** (AI-CONTEXT:374). This is an off-the-shelf interface; C27 owns only the deployment that exposes it and the operator credentials. **Operator authentication is LangFuse-native** (LangFuse ships its own login/RBAC); C27 authors **no** auth/SSO layer over it (same off-the-shelf posture as INV-3).

### 3.3 Inbound — deployment & registration config (C03/operator → C27)

| Interface | Role (v4 source) |
|---|---|
| `[[service]] name="langfuse" type="external" endpoint="http://localhost:3000"` | The Gas City service-registry binding that makes LangFuse addressable in the city (AI-CONTEXT:552–555). |
| docker-compose / deployment manifest | Stands up the LangFuse server + its backing stores (Postgres, and the ClickHouse/object-store the LangFuse release requires). Off-the-shelf LangFuse deployment; not authored. |
| Credential env (DB password, LangFuse API keys, initial admin) | The secrets LangFuse needs, supplied via env/`city.toml` (G37 — plaintext today; §7). |

### 3.4 Outbound

**None to other components.** C27 is a **terminal sink** (§1). It emits no data into the factory pipeline; its only "output" is the human-readable UI (§3.2). In particular it does **not** post to CXDB, beads, or the event bus — those are fed by other paths (INV-2).

### 3.5 Invariants

- **INV-1 (terminal sink — ingest-only, browse-only).** C27 ingests OTLP from C26 and serves a browsing UI; it produces **no** outbound data interface to any other v4 component (§3.4). Adding a C27→CXDB or C27→anomaly feed would violate this; those consumers read **CXDB**, not LangFuse.
- **INV-2 (two separate sinks — the G04 rule).** The OTLP path terminates **here** (LangFuse); the conversation/raw-bodies path terminates at **CXDB via C24**. The two never cross. C27 is the OTLP-sink half of the two-sinks invariant that C25/C26 also assert (README:411–413; AI-CONTEXT:210).
- **INV-3 (off-the-shelf, config-only — no custom code over LangFuse).** C27 deploys and configures stock LangFuse; it introduces **no** custom storage schema, UI, receiver, or hardening. "Turning it off" = removing the service + registry entry. (Mirrors C25 INV-2.)
- **INV-4 (sessions via upstream `session.id`).** Trace→session grouping in the UI depends on the **upstream correlation set C26 forwards unaltered** (C26 INV-4: `prompt.id`, `session.id`, `user.account_uuid`, `organization.id`, `terminal.type` — AI-CONTEXT:178), of which **`session.id`** (C25 §3.3) is the grouping key, being present on the spans. C27 does not synthesize identity; it relies on the contract C25 guarantees and C26 forwards.

> [FAITHFUL-FILL] INV-1…INV-4 are not stated verbatim as "invariants" in v4 but each restates an explicit v4 fact: terminal trace-browsing role (README:387; AI-CONTEXT:374), two separate sinks (README:411–413 + AI-CONTEXT:210), off-the-shelf self-host (README:387/540), and `session.id` as the correlation key (AI-CONTEXT:178). They are the minimal constraints that make "self-hosted LangFuse trace store & browser" well-defined without adding scope.

## 4. Data model / state

C27 **owns a data store** (inventory Kind = `data-store`) — but the schema, storage engine, and lifecycle are **LangFuse's, off the shelf**, not authored by v4.

| Aspect | Faithful spec (v4 source / LangFuse-native) |
|---|---|
| Owned data | The **LangFuse trace/observation/session/prompt store** — traces, spans/observations, sessions, model-call metadata, token/cost figures, and prompt versions (AI-CONTEXT:374). Schema is LangFuse-defined; v4 adds none. |
| Backing storage | LangFuse's standard backing stores (Postgres for metadata; the ClickHouse/object-store the LangFuse release uses for high-volume trace data). Operated as part of the self-host deployment; **C27 does not design these**. |
| Persistence & retention | LangFuse-native persistence; **retention/rotation is a LangFuse-config + ops concern**, not a v4 invention (mirrors C25's "retention is downstream"). v4 states no retention policy — deferred to ops (§9 OQ-5). |
| Sensitivity at rest | Traces contain **prompt/response content and correlation identity** (`user.account_uuid`, `organization.id` — AI-CONTEXT:178) and so are **sensitive at rest**; LangFuse's own access controls + the deployment's filesystem/DB permissions are the controls. C27 adds no new data-at-rest mechanism beyond what LangFuse provides. |
| Credentials (owned config, not data) | DB password + LangFuse API keys + initial admin, held in `city.toml`/env **as plaintext today** (G37; §7). Version-controlled config, not durable C27 state. |
| Consistency | Eventually-consistent w.r.t. the agent run: a span is browsable after LangFuse ingests the forwarded OTLP (LangFuse ingestion latency). C27 asserts no stronger guarantee. |

> [FAITHFUL-FILL] v4 names LangFuse's capability ("storage + browsing + session + prompt versioning," AI-CONTEXT:374) but specifies none of the backing-store topology, schema, or retention. Faithful reading at sweep 1: **C27 owns "a LangFuse store" as a black box** — the concrete service set (Postgres/ClickHouse), schema, and retention are LangFuse-deployment details settled at sweep 2/deploy time, not v4 architecture. C27 does not invent any of them.

## 5. Behavior

The flow is **deploy → register → C26 points at it → operator browses**:

```mermaid
flowchart LR
    CC[C25 Claude Code<br/>native OTLP] -->|OTLP| OTEL[C26 OTel Collector]
    OTEL -->|export OTLP traces<br/>+ LangFuse API key| LF[C27 LangFuse<br/>self-hosted :3000]
    LF --> STORE[(LangFuse store<br/>Postgres + ClickHouse)]
    OP((Operator)) -->|browse traces/<br/>sessions/prompts| LF
    OTEL -. NOT this path .-x|two-sinks rule| CX[(C21 CXDB)]
    CC -. raw bodies .-> BR[C24 bridge] --> CX
```

Key flow notes:
- **Deploy.** Stand up self-hosted LangFuse via its standard docker-compose stack (server + Postgres + ClickHouse/object-store), provision its credentials, and register it as `[[service]] type="external"` at `:3000` (AI-CONTEXT:552–555). No custom code.
- **Wire.** Point C26's OTLP exporter at LangFuse's ingestion endpoint with the LangFuse API key (README:540) — the C26→C27 ingestion seam (§3.1). This is the single integration step; it aligns with C26's export description (authored in parallel).
- **Ingest & store.** LangFuse ingests forwarded OTLP-trace spans and persists them as traces/observations/sessions, grouping by the upstream `session.id` (INV-4).
- **Browse.** The operator opens the LangFuse UI and inspects sessions/traces/prompts/costs — the P12 inspectability surface and the F42 re-engagement surface (README:387; AI-CONTEXT:374).
- **Verify.** Phase-1 acceptance is literally "**Verify trace browsing works**" (README:540) — C27's part is proving forwarded traces appear and are browsable, and that nothing on this path touches CXDB (INV-2).

## 6. Failure modes & handling

| F-mode | Applies to C27 how | v4 handling (faithful) |
|---|---|---|
| **G37** (secrets/credentials absent) | LangFuse's DB password + API keys live in `city.toml`/env as **plaintext** (AI-CONTEXT §13.2), alongside other secrets (OTel mTLS certs, Max OAuth tokens) that are **owned elsewhere** (C25/C41/C04), not by C27. | **Noted + deferred.** Minimal faithful expectation: credentials are referenced from `city.toml`/env per the existing convention (AI-CONTEXT:552–555, 569–579); C27 adds **no** secrets-management layer. The unbuilt secrets-store gap is tracked as the open gap **G37**, whose canonical resolution is owned by **C03** (the config owner — §9 OQ-4); it is *not* a Future-Enhancements item (FE-3 is the signing/key model and is itself *blocked on* G37). See §7, §9 OQ-4. |
| **G04** (two-sinks framing) | A naive integrator wires the OTLP/LangFuse path into CXDB, or treats LangFuse as the L4 substrate (AI-CONTEXT:326/374 "weak L4 fallback"). | **Resolved by INV-1/INV-2:** C27 is a terminal browsing sink; CXDB is fed only by C24. The "weak L4 fallback" option is named by v4 but **not chosen** (CXDB is the L4 substrate). See §9 OQ-2. |
| **F42** Cognitive-Escrow Negligence | The operator stops watching; the trace UI exists but is ignored. | **Partial — operator discipline still required** (F-MODE F42). C27 *provides* the inspection/re-engagement surface (README:387; AI-CONTEXT:374); the discipline to look at it is operator-side, not C27-native. C27's faithful contribution is making the surface exist and be browsable. |
| **F22 / F21 / others (downstream enablers)** | Liveness/exhaustion detection reads telemetry. | C27 is the **OTLP browsing** sink; the *numeric* detection loops (F22/F21 via PyOD) read **CXDB/metrics**, not LangFuse (the L4 substrate is CXDB — AI-CONTEXT:325). C27's contribution to these is the human-browsable view, not the automated detector. |
| **LangFuse-down / ingestion failure** (service-local) | LangFuse (or its Postgres/ClickHouse) is down; forwarded traces are dropped or buffered upstream. | v4 says **nothing** about LangFuse availability or buffering (part of G33, "no story for partial/cascading failure of the OSS stack," which the inventory assigns to **C24** — the integration-hardening budget — **not** C27). Faithful disposition: availability/retry is **whatever LangFuse + C26's exporter provide natively**; C27 adds no buffer. **Deferred** to the C26-exporter / G33 story (§9 OQ-6). LangFuse being down degrades *browsing only* — it never blocks the agent (telemetry is fire-and-forget upstream) and never affects the CXDB path (INV-2). |
| **Trace-store growth** (service-local) | Untruncated trace volume grows the LangFuse store. | Retention/rotation is **LangFuse-config + ops** (G33 territory), not a v4 invention; deferred (§9 OQ-5). C27 adds no custom retention. |

> [FAITHFUL-FILL] "LangFuse-down" and "trace-store growth" are service-local conditions v4 does not address for C27 (they fall under G33, which the inventory assigns to C24 — and C21 — not C26 or C27). Faithful reading: C27's availability/durability is **whatever stock LangFuse provides** — v4 specifies no buffering or HA layer at this sink. The minimal consistent choice is to **state this and defer**, since adding HA/buffering over LangFuse is exactly the kind of stack-hardening the bar drops (it gives no new principle-tied capability).

## 7. Cross-cutting (security / cost / scale / observability / ops)

- **Security (incl. G37).** LangFuse needs **credentials** — a DB password, project/public+secret API keys, and an initial admin — and these sit beside the OTel mTLS certs and Max OAuth tokens in `city.toml`/env **as plaintext** (AI-CONTEXT §13.2; G37). v4 has **no secrets-management story**, and inventing one here is **out of scope** (it is hardening and fails the capability-for-principle bar). The unbuilt secrets store is the open gap **G37** (canonical resolution owned by **C03**, the config owner — §9 OQ-4); it is *not* a Future-Enhancements item — FE-3 is the signing/key model and is itself *blocked on* G37, not the secrets store. The **faithful, minimal** posture: credentials are referenced from `city.toml`/env per the existing convention, the LangFuse deployment's filesystem/DB permissions protect them at rest, and the gap is **stated and deferred** (§9 OQ-4). Trace content itself is **sensitive at rest** (full prompts/responses + identity attributes, AI-CONTEXT:178) — LangFuse's native access controls + deployment permissions are the controls; C27 adds none beyond LangFuse.
- **Cost.** Deployment-only — the cost is the self-hosted LangFuse stack's compute/storage (Postgres + ClickHouse), scaling with trace volume; no incremental API cost (telemetry "works under Max with no API key" upstream, C25 INV-4). Retention/rotation (an ops lever) bounds storage cost (§9 OQ-5).
- **Scale.** Trace volume scales with agent activity and the upstream export cadence/beta-trace flag (C25 §3.3). Throughput/HA of the LangFuse store is a **LangFuse-deployment** concern (G33), not a v4 design — C27 runs the stock self-host; scaling it is ops, not custom code.
- **Observability (of itself).** C27 *is* an observability surface; its own health is "does trace browsing work?" — the Phase-1 acceptance check (README:540). Whether ingestion is succeeding is visible in the LangFuse UI itself (new traces appearing) and at the C26 exporter side.
- **Ops.** Stand-up/teardown and re-pointing are a docker-compose deployment + a `city.toml` (C03) service entry + the C26 exporter target (AI-CONTEXT:552–555; README:540) — declarative, no custom service. Phase-1 sequencing (README:539–541): stand up C26 → verify flow → **install LangFuse, point the collector at it, verify browsing** → install CXDB + build the C24 bridge. Upgrades = bumping the LangFuse image (carrying the schema/license check, OQ-3).

## 8. Acceptance criteria & test strategy

Sweep-1 acceptance (high-level):
1. **AC-1 (LangFuse stands up self-hosted).** The LangFuse docker-compose stack (server + backing stores) comes up healthy and is reachable at its endpoint (`:3000`, AI-CONTEXT:555), registered as `[[service]] type="external"` (AI-CONTEXT:552–555).
2. **AC-2 (C26→C27 ingestion works).** With C26's OTLP exporter pointed at LangFuse's ingestion endpoint (+ API key), spans forwarded by C26 are **ingested and stored** as LangFuse traces (README:540 — the C26→C27 seam).
3. **AC-3 (trace browsing works).** A human can open the LangFuse UI and **browse the forwarded traces** — the literal Phase-1 check "Verify trace browsing works" (README:540).
4. **AC-4 (sessions group by `session.id`).** Spans carrying the upstream `session.id` (C25 §3.3; AI-CONTEXT:178) are grouped into browsable **sessions** in the UI (INV-4) — LangFuse-native behavior, verified end-to-end.
5. **AC-5 (prompt/session versioning available).** LangFuse's prompt/session-versioning surface is present and usable (AI-CONTEXT:374) — confirmed available, not custom-built.
6. **AC-6 (terminal sink — two-sinks boundary).** The OTLP/LangFuse path is observed terminating **here**; **no data flows from C27 to CXDB / beads / event bus**, and the path does not touch CXDB (INV-1/INV-2; the C27 half of the G04 check).
7. **AC-7 (credentials referenced from config; gap noted).** LangFuse's required credentials are supplied via `city.toml`/env per convention (AI-CONTEXT:552–555); the **G37 plaintext-secrets gap is recorded and deferred** (no secrets store built; §9 OQ-4).

Test strategy (sweep-1): a Phase-1 fixture — bring up the LangFuse self-host stack, register it in a scratch `city.toml`, and point a stub C26 collector (or the real one, parallel wave) at LangFuse's OTLP ingestion endpoint with a provisioned API key. Drive one short agent run (or replay a captured OTLP-trace batch through C26) and assert: (a) the stack is healthy and reachable (AC-1); (b) forwarded spans are ingested and **browsable** in the UI (AC-2/AC-3); (c) spans with a shared `session.id` appear as one session (AC-4); (d) the prompt/session-versioning surface exists (AC-5); (e) nothing is posted from C27 to a CXDB endpoint (AC-6); (f) the deployment reads its credentials from `city.toml`/env and the G37 gap is documented (AC-7). The concrete OTLP-ingestion endpoint path, the LangFuse trace/session schema fields, the docker-compose service set, and the credential/env matrix are deferred to sweep 2 (coordinated with the C26 author).

## 9. Open questions

- **OQ-1 (→ [review-log](../_meta/review-log.md), top open question) — the C26→C27 ingestion endpoint (shared with C26).** v4 says only "point the OTel Collector at it" (README:540) and never names the ingestion mechanism. Faithful reading adopted: C26 exports OTLP traces to **LangFuse's native OTLP-trace ingestion endpoint** (no custom receiver). The shared question to settle with the C26 author at sweep 2: pin the exact endpoint path (`/api/public/otel`) + `otlphttp` exporter block + Basic-auth header (base64 `public:secret` + `x-langfuse-ingestion-version`). **Signal-set mismatch to resolve (the load-bearing half):** LangFuse's OTLP endpoint ingests **traces only** — it does **not** ingest OTLP metrics or logs (verified against LangFuse's OTel docs) — yet **C26 §3.3 currently pipelines metrics + logs/events *and* traces into this endpoint, and C26 AC-5 asserts metrics/events "appear in LangFuse."** Those non-trace signals will not land here. **Faithful default for the C27 side:** C27's ingestion/browse contract is **traces/observations/sessions only**; it does **not** assert metrics/events browsability in LangFuse at sweep 1. **DEFERRED — needs orchestrator decision:** the *direction* of the fix (C26 routes **only** traces to LangFuse and metrics/events terminate elsewhere/nowhere on the OTLP path, vs. proving the chosen release ingests them) edits **C26 §3.3/AC-5** and must be ruled jointly so C26's export description and C27's ingestion contract are one seam.
- **OQ-2 — LangFuse as "weak L4 fallback" event substrate (G04-adjacent).** AI-CONTEXT:326/374 names LangFuse as a "weak L4 fallback" generic event substrate, but v4 chooses **CXDB** as the L4 substrate (AI-CONTEXT:325; README:413). Faithful pick: **C27 is a browsing sink only**, NOT an L4 source — the self-healing loop (C36/C37/C38) reads CXDB. Reviewer item: confirm no downstream component is ever wired to read trajectories *from* LangFuse (which would break INV-1 and the two-sinks rule). (Reading A: LangFuse browsing-only, CXDB is L4 — adopted. Reading B: use LangFuse's L4 fallback — rejected, contradicts the CXDB-as-substrate choice.)
- **OQ-3 — LangFuse license/SPDX pin.** v4 states the license inconsistently (README:294 "MIT core" vs AI-CONTEXT "Apache 2.0"). Both agree the self-host core is permissive and cleanly self-hostable (vs Phoenix's rejected Elastic License, README:295/333). Open: at deploy time, pin the exact license of the chosen LangFuse release and confirm the self-host path stays clean (no Elastic-style hosted-service restriction creeps in via an enterprise edition). Low risk; a deployment-time check, not an architecture blocker.
- **OQ-4 — G37 secrets handling (cross-cutting, config owner is C03).** LangFuse credentials are plaintext in `city.toml`/env alongside OTel mTLS certs and Max OAuth tokens (AI-CONTEXT §13.2). Faithful disposition: **note + defer** — reference creds from config, build no secrets store (inventing one fails the bar; the unbuilt secrets store is the open gap **G37**, *not* a Future-Enhancements item — FE-3 is the signing/key model and is itself *blocked on* G37). Open item for the reviewer: **G37 is a key gap on C03, C27, and C43** (per the component inventory), and the plaintext-credential surface it names is also touched by the OTel/Max/judge paths — should the deferral live once in a shared Observability/config note rather than restated per component? (Faithful pick: state the minimal expectation here; the **canonical resolution belongs to C03**, the config owner.)
- **OQ-5 — trace retention/rotation.** v4 states no retention policy for the LangFuse store; untruncated trace volume grows it. Faithful: retention is a **LangFuse-config + ops** lever (G33), not a v4 invention — deferred. Open: set a default retention at deploy time (ops), since the store holds sensitive content (AI-CONTEXT:178) and unbounded growth is a cost/security drift.
- **OQ-6 — LangFuse-down durability (G33; owned at C24, exporter-side shared with C26).** v4 specifies no buffering/HA for the LangFuse sink when it is down; the exporter's behavior is C26/LangFuse-native and undocumented in v4. Deferred to the C26-exporter behaviour + the G33 story (owned at C24) — flag whether dropped traces during LangFuse downtime are acceptable (faithful default: accept; browsing degrades but the agent and the CXDB path are unaffected — do not add an HA/buffer layer v4 doesn't name).
