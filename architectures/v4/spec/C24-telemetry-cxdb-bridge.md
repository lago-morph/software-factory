# C24 — Telemetry → CXDB Ingestion Bridge  (Spec, Track A)

> Source: README §Part 6 Phase 1 (line 386 "Install OpenTelemetry Collector … `OTEL_LOG_RAW_API_BODIES=file:<dir>` for the raw-body path"; line 389 "Build the raw-API-bodies → CXDB bridge as a Gas City pack — a small standalone tool node binary that watches the `OTEL_LOG_RAW_API_BODIES` directory and posts to CXDB via HTTP/JSON :9010. Pattern transfusion from Kilroy's per-stage logging and Gas City's `internal/sessionlog` — but the bridge is a standalone binary called by Gas City as a tool node, not a Go import"; line 408 graph node "Bridge[raw-bodies → CXDB bridge pack]", line 413 "CC -->|raw bodies| Bridge --> CX"; line 541 "Install CXDB alongside, build the raw-API-bodies bridge. This is the first non-trivial integration; budget a week"); AI-CONTEXT §4.3 (line 176 "`OTEL_LOG_RAW_API_BODIES=file:<dir>` dumps untruncated request/response JSON to disk. Conversation-shaped, ideal for CXDB ingestion"; line 178 correlation attributes `prompt.id`, `session.id`, `user.account_uuid`, `organization.id`, `terminal.type`), §5.2 (lines 204–210 ingest protocols :9009/:9010), §5.4 (lines 222–232 bridge impedance table + "Recommended: raw API bodies path … standalone Go binary that watches `OTEL_LOG_RAW_API_BODIES` directory and posts to CXDB HTTP API … parent-chain via `session.id`"), §5.5 (BLAKE3 idempotency), §11.1 (lines 463–466 "Bridge path: raw API bodies → CXDB — Yes, recommended … standalone tool-node binary in a pack", "Skip OTLP → CXDB path — Yes"), §13.2 (lines 558, 579 `[[service]] cxdb` + `OTEL_LOG_RAW_API_BODIES = "file:/var/lib/cxdb-bridge/inbox"`); component-inventory C24 row (line 36 "Standalone tool-node watching raw-API-bodies dir, posting to CXDB HTTP; defines delivery/ordering/back-pressure at the seam", maps A29b/A29c/A28c/B45, depends C21+C28, gaps G26/G27/G33, foundational no) + Batch-2 note (line 109); spec/C21 §3 (I2 HTTP ingest), §6 (G33 fail-open + idempotency, AC-7); spec/C23 §6 (G27 reading (b)); ambiguities-and-gaps G26, G27, G33; review-log D-2 (bundle-id `softwarefactory.v4.trajectory`).
> Inventory ID: C24   Kind: interface   Status: sweep-1
> Track: A (faithful)

## 1. Purpose & responsibility

C24 is the factory's **telemetry → CXDB ingestion bridge**: a **standalone Go tool-node binary, shipped in a
Gas City pack**, that **watches the raw-API-bodies directory** Claude Code dumps (`OTEL_LOG_RAW_API_BODIES=
file:<dir>`, AI-CONTEXT §4.3 line 176) and **posts each conversation-shaped body to CXDB's HTTP/JSON ingest
(:9010)** as a parent-pointered turn (README line 389; AI-CONTEXT §5.4 line 232). It is the **seam that turns
agent trajectory telemetry into stored trajectories** — the load-bearing wire between the Agent Loop (C28)
and the trajectory store (C21) that makes P10 (full memory) and P11/P12 (self-healing / self-optimization)
buildable (README lines 388–397).

C24 is **the spec-of-record for the bridge seam itself**: which ingest path is wired (G27), the
delivery/ordering/at-least-once contract (G26), the `session.id` → CXDB parent-turn mapping (G26), and the
buffer/retry/back-pressure behavior when CXDB is down (G26/G33). v4 calls this "**the first non-trivial
integration; budget a week**" (README line 541) precisely because the hard parts live at *this* seam — C21
(store) and C23 (event bus) both explicitly **defer** delivery/back-pressure to C24.

**Responsibilities (what C24 is the spec-of-record for):**
- **Watch the raw-bodies inbox** — observe `OTEL_LOG_RAW_API_BODIES` dir (`/var/lib/cxdb-bridge/inbox`,
  AI-CONTEXT §13.2 line 579) for new/completed body files (README line 389).
- **Parse conversation-shaped bodies into CXDB turns** — read each untruncated request/response JSON body,
  shape it into a CXDB turn payload tagged with the v4 trajectory type triple (AI-CONTEXT §4.3 line 176
  "conversation-shaped"; §5.3 turn model).
- **Resolve the parent-turn pointer from `session.id`** — maintain the per-session head so successive bodies
  for one `session.id` chain into a trajectory ("parent-chain via `session.id`", AI-CONTEXT §5.4 line 229).
- **Post to CXDB :9010 (HTTP/JSON)** — the recommended ingest path (AI-CONTEXT §5.4 line 232; README line
  389; C21 I2).
- **Own the delivery contract at the seam (G26)** — ordering, at-least-once delivery, handling of
  partially-written body files, and the `session.id` → parent-turn mapping rule.
- **Own buffer / retry / back-pressure (G26/G33)** — when CXDB is down or slow, buffer un-posted bodies and
  retry; do not crash the run (C21 fail-open) and do not silently drop trajectories.
- **Be a pack-delivered tool node** — packaged + invoked per the pack/tool-node ABI (C02/C17); **not** a Go
  import of Gas City code (README line 389; AI-CONTEXT §11.1 line 465).
- **Transfuse the parse pattern** from Gas City `internal/sessionlog` + Kilroy per-stage logging (README
  line 389) — pattern transfusion, not code import (C51 discipline).

**Explicitly NOT (boundaries):**
- **NOT the trajectory store.** CXDB (C21) owns content-addressing, dedup, O(1) branch, turn-DAG storage.
  C24 only *posts* turns to C21's ingest seam (C21 I2); it does not store or address payloads (README line
  500 "factory builds the orchestration glue, not the foundations").
- **NOT the type bundle / schemas.** The `{bundle_id, type, version}` triple C24 stamps on each turn is owned
  by **C22** (the v4 CXDB trajectory bundle, `softwarefactory.v4.trajectory` per review-log D-2). C24
  *uses* the registered type; it does not define it (inventory C22; spec/C21 I7).
- **NOT the OTLP/metrics path.** Claude Code's OTLP metrics/events → OTel Collector → LangFuse is a
  **separate sink** (C25/C26/C27); C24 consumes only the **raw-API-bodies escape hatch**, not OTLP, and the
  **OTLP → CXDB path is explicitly rejected** (AI-CONTEXT §5.4 line 230, §11.1 line 466; C21 INV-6). C24
  never sends spans to CXDB.
- **NOT the event bus.** The Gas City event-bus JSONL → CXDB path (C23) is the *lowest-impedance source* but
  is **not the path v4 wires** (G27, resolved below); C23 remains an available source the bridge MAY also
  consume but the canonical C24 input is raw API bodies.
- **NOT the OTLP exporter.** Claude Code's emission of raw bodies to disk (the producer side) is **C25**
  (`otlp-telemetry-export` / raw-bodies escape hatch); C24 is the *consumer* that watches the dir C25
  configures. The `OTEL_LOG_RAW_API_BODIES` env binding lives in the agent session config (C04/C28; AI-
  CONTEXT §13.2). *(C24's inventory `depends on` lists C21+C28; the producer is C28's raw-body emission via
  the C25 escape-hatch config.)*
- **NOT the counterfactual-replay / self-healing readers.** C24 is write-side only (telemetry → store);
  C36/C37/C38/C49 read from C21, not from C24.
- **NOT a span/trace processor.** No OTLP span-tree → turn-DAG translation (the explicitly-rejected mapping,
  AI-CONTEXT §5.4 line 230).

## 2. Context & dependencies

| Direction | Component | Relationship |
|---|---|---|
| Upstream (producer) | **C28** Claude Code agent loop (+ **C25** raw-bodies escape hatch) | C28, run with `OTEL_LOG_RAW_API_BODIES=file:<dir>` (AI-CONTEXT §13.2 line 579), dumps untruncated request/response JSON to the inbox dir. C24 watches that dir. Inventory C24 "Depends on: C28". |
| Downstream (sink) | **C21** CXDB trajectory store | C24 posts turns to C21's HTTP/JSON ingest :9010 (C21 I2; AI-CONTEXT §5.4 line 232). C21 owns dedup/branch/storage; defers delivery/back-pressure to C24 (spec/C21 §6 G33). Inventory C24 "Depends on: C21". |
| Type provider | **C22** CXDB type registry & viewpoint tagging | Supplies the `{bundle_id,type,version}` triple (`softwarefactory.v4.trajectory`, review-log D-2) C24 stamps on each posted turn. |
| Alternative source (latent) | **C23** Event bus | The *lowest-impedance* CXDB source (AI-CONTEXT §5.4 line 228), but **not the wired path** (G27 reading (b)). C23 guarantees a bridgeable stream (C23 I5); C24 MAY also consume it, but the canonical input is raw bodies. |
| Packaging host | **C02** Pack/tool-node ABI, **C17** Tool-node abstraction | C24 is a standalone tool-node binary distributed in a pack, invoked via the tool-node protocol — not a Go import (README line 389; AI-CONTEXT §11.1 line 465). |
| Exemplar (pattern) | Gas City `internal/sessionlog`, Kilroy per-stage logging | Transfused *parse pattern* (Claude Code JSONL → turns); pattern transfusion, not code import (README line 389; C51). |

**Position in the system.** C24 is **Batch-2** (component-inventory line 109): it stands up in **Phase 1**
alongside the CXDB install (README lines 388–389) once C21 is up and C28/C25 emit raw bodies. It is **not
foundational** (inventory C24): nothing in Batch 1 contracts against it; it is a leaf that wires two existing
seams (C28 producer → C21 sink). It is, however, **on the de-risking critical path** for the whole
observability/self-healing tier — "the first non-trivial integration; budget a week" (README line 541) — and
is **feature-flag-gated** with CXDB (it only exists when the CXDB capability is enabled; README line 252
"CXDB (for trajectories)").

## 3. Interfaces / contracts

Sweep-1: interfaces **named and described**; concrete wire signatures / file-watch semantics / retry params
defer to sweep 2 (and the type triple to C22, the ingest wire to C21).

| # | Interface | Direction | Description | Owning/detailing component |
|---|---|---|---|---|
| I1 | **Raw-bodies inbox watch** | inbound (read) | Watch `OTEL_LOG_RAW_API_BODIES` dir for new/completed body files; detect a file is *complete* (not partially written) before ingesting (AI-CONTEXT §4.3, §13.2; G26 partial-file handling). | C24 (this) |
| I2 | **Body → turn parse/shape** | internal | Parse one untruncated request/response JSON body into a CXDB turn payload (conversation-shaped); attach the `{bundle_id,type,version}` triple from C22. Transfused parse pattern from `internal/sessionlog` (README line 389). | C24 (this); **C22** (triple) |
| I3 | **`session.id` → parent-turn mapping** | internal/state | Maintain per-`session.id` head pointer so successive bodies chain into one trajectory ("parent-chain via `session.id`", AI-CONTEXT §5.4 line 229); resolve the parent-turn pointer for each new turn. The G26 mapping rule lives here. | C24 (this) |
| I4 | **CXDB HTTP/JSON post (:9010)** | outbound (write) | POST the shaped turn to CXDB's HTTP ingest (C21 I2; AI-CONTEXT §5.4 line 232). Idempotent at the store (BLAKE3 content-addressing makes a re-post a no-op — C21 INV-1/AC-7). | C21 (sink), C24 (caller) |
| I5 | **Durable buffer + retry / back-pressure** | internal/state | Persist un-acked bodies; retry on CXDB unavailability with bounded back-pressure; advance a checkpoint of last-successfully-posted body so a restart resumes without re-scanning or dropping (G26/G33). | C24 (this) |
| I6 | **Tool-node lifecycle (pack)** | inbound (ops) | Packaged + invoked as a Gas City tool node (C02/C17 ABI); configured via the pack's TOML; operated alongside CXDB in Phase 1 (README line 389). | C02/C17 (ABI), C24 (config) |

**Invariants C24 must uphold (bridge-level):**
- **INV-1 (no silent drop — at-least-once):** every *complete* body file is delivered to CXDB at least once,
  or retained in the buffer until it can be; a body is removed from the buffer only after CXDB acks
  (addresses G26 delivery + G33 "trajectories the loops depend on must not silently drop").
  > [FAITHFUL-FILL] v4 names the bridge but does not state at-least-once vs exactly-once. **At-least-once** is
  > the minimal faithful choice because v4 *already* makes re-delivery safe: CXDB is BLAKE3 content-addressed,
  > so re-posting the same turn is a no-op (AI-CONTEXT §5.5; spec/C21 §6 AC-7). At-least-once +
  > store-side idempotency = effectively-once with the simplest bridge — exactly-once delivery would require
  > distributed coordination v4 never mentions. (Per-`session.id` ordering is the only ordering v4 implies via
  > the parent-chain.)
- **INV-2 (parent-chain integrity per session):** turns for one `session.id` are posted with parent pointers
  that reconstruct the conversation order; a later body's turn points at the prior body's turn for that
  session (AI-CONTEXT §5.4 line 229). Cross-session ordering is **not** constrained (independent trajectories).
- **INV-3 (fail-open to the run):** if CXDB is down/unreachable, C24 buffers and retries; it **never crashes
  or blocks the agent run** — the run proceeds on beads+events (spec/C21 §6 reading (a); G33). The
  bridge is best-effort to the *run* but durable for the *trajectory*.
- **INV-4 (complete-file only):** C24 ingests a body only once it is fully written; a partially-written body
  file is detected and deferred, never posted truncated (G26 "partially-written body files").
  > [FAITHFUL-FILL] v4 (G26) flags partial-file handling as undefined. The minimal faithful rule — *wait for a
  > completeness signal (e.g. rename/close/size-stable) before ingest* — is the smallest choice that prevents
  > posting a torn turn; the exact completeness mechanism (atomic rename vs fsnotify-close vs size-stability)
  > is sweep-2 and depends on how C25/Claude Code writes the files (OQ-2).
- **INV-5 (checkpoint / resumable):** C24 persists which bodies have been posted so a restart neither
  re-scans the whole inbox nor drops un-posted bodies (G26 restart safety; mirrors the C23 I3 checkpoint
  property).
- **INV-6 (no OTLP, no spans):** C24 posts only conversation-shaped turns from raw bodies; it never sends
  OTLP spans to CXDB (the rejected path, AI-CONTEXT §5.4 line 230; C21 INV-6).

## 4. Data model / state

C24 *owns the bridge runtime state*; the **turn payload schema/triple** is C22's, the **stored turn** is
C21's. State C24 is the spec-of-record for at sweep 1:

| State | Description | Persistence | Detailed by |
|---|---|---|---|
| **Inbox cursor / processed set** | Which body files have been successfully posted (checkpoint for restart, INV-5). | Durable local file (alongside the pack's working dir). | C24 |
| **Per-`session.id` head map** | The current CXDB head turn per active session, to resolve the parent pointer (INV-2). | Durable local state (must survive restart to keep chaining). | C24 |
| **Pending/retry buffer** | Complete-but-not-yet-acked bodies awaiting CXDB (INV-1/INV-3). | Durable local buffer (file or queue dir). | C24 |
| **Pack/tool-node config** | Inbox dir path, CXDB :9010 endpoint, type-bundle id, retry/back-pressure params. | Pack TOML (C02/C03 model). | C02/C03 (model), C24 (binding) |
| **Posted turn** | The CXDB turn (payload + triple + parent ptr) — *owned/stored by C21*, *typed by C22*. | CXDB (`turns.log`/`blobs.pack`). | **C21** (store), **C22** (triple) |

> [FAITHFUL-FILL] v4 specifies the bridge *behavior* (watch dir → post HTTP) but not its persisted runtime
> state. The minimal faithful set is **{inbox cursor, per-session head map, pending buffer}** — each is
> directly forced by a v4-named requirement: the cursor by restart-safety (G26), the head map by
> "parent-chain via `session.id`" (AI-CONTEXT §5.4), the buffer by "back-pressure when CXDB is down" (G26).
> Exact on-disk formats are sweep-2.

**Consistency / lifecycle.** C24 stands up in **Phase 1** with CXDB (additive to Phase 0; README line 388).
Its state is **derived/transient** — it can be rebuilt by re-scanning the inbox (CXDB idempotency makes
re-posts no-ops), so the cursor/head-map are an *optimization for correctness-under-restart*, not an
independent source of truth. The **source-of-truth trajectory survives in CXDB**; the **source-of-truth
action trail survives in beads+events** regardless of C24. C24 is therefore a *replayable, restartable
courier*, which is exactly what at-least-once + store idempotency (INV-1) buys.

## 5. Behavior

**Stand up (Phase 1).** The pack is installed; the tool node is configured with the inbox dir
(`/var/lib/cxdb-bridge/inbox`, AI-CONTEXT §13.2), the CXDB :9010 endpoint, and the
`softwarefactory.v4.trajectory` type bundle (C22/D-2). C28 worker sessions are configured with
`OTEL_LOG_RAW_API_BODIES=file:<that dir>` (AI-CONTEXT §13.2 line 579). The bridge begins watching.

**Ingest path (steady state).**
1. **Watch** (I1): a new body file appears in the inbox; C24 waits for the completeness signal (INV-4).
2. **Parse/shape** (I2): read the untruncated request/response JSON; shape into a CXDB turn payload; attach
   the `{bundle_id,type,version}` triple from C22 and the body's `session.id` (AI-CONTEXT §4.3 line 178).
3. **Resolve parent** (I3): look up the per-`session.id` head; set the new turn's parent pointer; this is the
   `session.id` → parent-turn mapping rule (G26).
4. **Post** (I4): POST the turn to CXDB :9010 (C21 I2). On ack, advance the session head + inbox cursor and
   drop the body from the buffer (INV-1/INV-5).
5. **On failure** (I5): CXDB down/slow/error → retain in the buffer, back off and retry; do **not** crash the
   run (INV-3). Re-posts are safe (CXDB BLAKE3 idempotency, INV-1).

**Restart.** On restart, C24 resumes from the persisted cursor + head map; un-acked buffered bodies are
re-posted (idempotent). No inbox re-scan-from-zero is required, and no complete body is lost (INV-5).

> Sequence/state diagrams (Mermaid), the file-completeness detection algorithm, the exact `session.id`→
> parent-turn rule, the retry/back-pressure schedule (back-off curve, buffer bound, circuit-breaker), and the
> body-JSON → turn-payload field mapping are **sweep-2+**. The type triple is **C22**; the ingest wire is **C21**.

## 6. Failure modes & handling

C24 owns the three gaps assigned at this seam (G26, G27, G33).

**G27 (major) — which ingest path: event-bus vs raw-API-bodies. RESOLVED HERE.**
> [AMBIGUITY: G27] AI-CONTEXT §5.4 *ranks* the **Gas City event-bus JSONL → CXDB** path **lowest impedance /
> best** ("events already attributed and trajectory-shaped", line 228) but *recommends* the **raw-API-bodies**
> path (ranked #2 "Low") and §11.1 + README concretely build that one, with no stated override reason. Two
> readings: **(a)** honor the *ranking* → wire the event-bus path; **(b)** honor the *recommendation + the
> concrete build* → wire the raw-API-bodies path. **Chosen: (b) — C24 wires the raw-API-bodies path; the
> event bus (C23) remains a first-class latent source the bridge MAY also consume.** This is unambiguously the
> reading most consistent with the rest of v4: the recommendation is explicit ("**Recommended**: raw API
> bodies path", AI-CONTEXT §5.4 line 232), the §11.1 decision row says "Bridge path: raw API bodies → CXDB —
> Yes, recommended" (line 465), README Part 6 builds *only* the raw-bodies bridge (lines 389, 408, 413, 541),
> and the §13.2 service config wires `OTEL_LOG_RAW_API_BODIES` (line 579) — there is no event-bus-→-CXDB
> wiring anywhere in the concrete plan. The "Lowest" ranking is best read as a **property statement** ("events
> are cheapest-to-bridge *because already attributed*"), not a build directive. The deciding *technical*
> reason (a faithful inference, not a v4 fact): CXDB's unit is the **turn = a model request/response
> conversation** (AI-CONTEXT §5.3), and raw API bodies *are* the untruncated request/response bodies
> ("conversation-shaped", §4.3 line 176), whereas Gas City events are **action-shaped** and do not carry the
> model's full request/response payloads — so the turn-DAG that P11/P12 need can be reconstructed from raw
> bodies but not from action events alone. C23 §6 already pre-concurs with reading (b) and defers the binding
> to C24; **C24 hereby binds the raw-API-bodies path.** OQ-1 records the residual contradiction for the
> integrator.

**G26 (major) — raw-bodies → CXDB bridge seam: delivery / ordering / partial files / `session.id` mapping /
back-pressure. ADDRESSED HERE.** v4 leaves all five seam questions undefined (G26). Faithful resolutions:
- **Delivery:** **at-least-once** + store-side BLAKE3 idempotency = effectively-once (INV-1; see [FAITHFUL-
  FILL]). No exactly-once machinery (v4 never asks for it).
- **Ordering:** **per-`session.id` parent-chain** ordering only (INV-2), grounded in "parent-chain via
  `session.id`" (AI-CONTEXT §5.4 line 229). Cross-session order is unconstrained.
- **Partial files:** **complete-file-only ingest** (INV-4) — wait for a completeness signal; never post a
  torn body.
- **`session.id` → parent-turn mapping:** maintain a **per-session head pointer** (I3); each new body's turn
  parents the prior session turn. The exact rule (first body of a session → root turn; subsequent →
  prior head) is the §5.4-line-229 chain made concrete; precise mechanism is sweep-2 (OQ-3).
- **Back-pressure:** **durable buffer + bounded retry** (I5), fail-open to the run (INV-3).

**G33 (major) — partial/cascading OSS-stack failure; "what happens when CXDB is down mid-run?" ADDRESSED
HERE (the seam v4 locates it at).** C21 §6 places the *durability obligation* on the bridge; C24 discharges
it: **CXDB down ⇒ C24 buffers + retries, the run continues on beads+events (fail-open, INV-3), and buffered
trajectories are delivered when CXDB returns (idempotent re-post, INV-1).** No trajectory the self-healing/
optimization loops depend on is silently dropped *as long as the buffer holds* — the **buffer bound** is the
one honest limit (a sufficiently long CXDB outage exceeding the buffer can still lose the oldest window; v4
prescribes no unbounded durable queue, so this is a **known limitation → OQ-4**, the faithful posture given
v4's "no Postgres/Redis/Kafka" stance, AI-CONTEXT §5.3).

**Other failure cases.**
- **Malformed / unparseable body** → quarantine (move aside) + emit an event; do not block the inbox
  (fail-open per body). *[FAITHFUL-FILL]: v4 silent on bad bodies; quarantine-and-continue is the minimal
  non-blocking choice.*
- **Inbox disk fills / body writer outpaces bridge** → back-pressure surfaces as inbox growth; this is the
  scale limit (OQ-4); v4 names no rate-limit on body emission.
- **Duplicate body delivery** (re-scan after restart) → harmless: CXDB BLAKE3 idempotency makes the re-post a
  no-op (INV-1; C21 AC-7).

> F-mode applicability is owned by C57 (coverage map); C24 surfaces the seam-level failure classes
> (trajectory loss on CXDB outage G33, torn/duplicate delivery G26, path-binding G27) and defers the
> canonical F-mode mapping there. The bridge underwrites F10 (findings persisted as trajectories, not lost to
> chat) and the P11 substrate, contingent on CXDB being the sink.

## 7. Cross-cutting (security / cost / scale / observability / ops)

- **Security.** Raw API bodies contain **untruncated request/response JSON** (AI-CONTEXT §4.3) — i.e. full
  prompts/outputs, the most sensitive payload in the system. C24 moves them from a local inbox to CXDB over
  HTTP/JSON :9010; the inbox dir + transport + CXDB endpoint inherit the **G37 secret/exposure thread**
  (plaintext local dir, unauthenticated localhost HTTP) — flagged, **deferred to the config/secrets owner**
  (out of C24 faithful scope; v4 gives no auth/TLS story for :9010). C24 carries `session.id`/attribution
  through to the turn but does not itself sign (C41's optional layer).
- **Cost.** Bridge is a local Go process tailing files + posting HTTP; no managed-store fees (consistent with
  the CXDB no-managed-DB stance, AI-CONTEXT §5.3). The *storage* cost is C21's; v4 gives no bridge cost model.
- **Scale.** Throughput must keep up with raw-body emission volume across all C28 sessions; the buffer bound
  + inbox growth are the scale limits (G33/OQ-4). The HTTP path (:9010) is the *recommended* (not the
  high-throughput :9009 binary) path — for very high volume the binary path is the latent alternative (C21
  I1; OQ-5, interacts with G26 back-pressure).
- **Observability.** C24's own health (inbox lag, buffer depth, last-acked cursor, CXDB up/down, post error
  rate) is the key operational signal — it is what tells ops whether trajectories are landing. Emitting these
  as events on C23 keeps the bridge auditable.
- **Ops.** Pack-delivered tool node operated alongside CXDB in Phase 1 (README line 389). "First non-trivial
  integration; budget a week" (README line 541) — the de-risking work *is* this seam. Pin the CXDB version
  (inherits C21's version-pin invariant) so the :9010 ingest contract is reproducible.

## 8. Acceptance criteria & test strategy

Sweep-1 = high-level criteria (concrete tests at sweep 2).

1. **AC-1 (watch → post happy path — I1/I4):** a complete raw-body file dropped in the inbox results in a
   corresponding turn posted to CXDB :9010 and resolvable on read (AI-CONTEXT §5.4; C21 I2).
2. **AC-2 (parent-chain per session — INV-2/I3, addresses G26):** two bodies with the same `session.id`
   produce two turns where the second's parent pointer is the first's turn; reconstructing the trajectory
   yields conversation order (AI-CONTEXT §5.4 line 229).
3. **AC-3 (cross-session independence — INV-2):** bodies from two different `session.id`s produce two
   independent (unrelated-parent) trajectories.
4. **AC-4 (complete-file-only — INV-4, addresses G26):** a partially-written body file is **not** posted
   until complete; no torn turn ever reaches CXDB.
5. **AC-5 (at-least-once + idempotent — INV-1, addresses G26):** every complete body lands in CXDB at least
   once; re-posting the same body (e.g. after restart) is a **no-op** at the store (BLAKE3, C21 AC-7) — no
   duplicate turn.
6. **AC-6 (fail-open + buffer/retry — INV-3/INV-5, addresses G33):** with CXDB **down**, the agent run
   continues (no crash/block); bodies accumulate in the durable buffer; when CXDB returns, all buffered
   bodies are delivered and the trajectories are complete (within the buffer bound).
7. **AC-7 (restart-resumable — INV-5, addresses G26):** killing and restarting the bridge mid-stream loses
   no complete body and produces no duplicate turn; it resumes from the persisted cursor + head map.
8. **AC-8 (no OTLP/spans — INV-6, honors G27 reading):** C24 ingests only raw-body turns; no OTLP span is
   ever posted to CXDB (the rejected path, AI-CONTEXT §5.4 line 230; C21 INV-6).
9. **AC-9 (path binding — addresses G27):** the wired source is the **raw-API-bodies** inbox, not the event
   bus; the event-bus path is verified *latent* (not wired) — confirming reading (b).

**Test strategy.** A **bridge integration pack** that boots the pinned CXDB (C21 conformance prerequisite),
points the bridge at a synthetic inbox, and drives AC-1…AC-9 — in particular the parent-chain mapping, the
complete-file gate, the at-least-once/idempotent delivery, and the **CXDB-down fail-open/buffer/recover**
cycle (the G33 de-risker). This suite **must pass before the P11 self-healing readers (C36/C37/C38) rely on
trajectories landing in CXDB**, since they assume C24 delivered them. It is the concrete realization of
README line 541's "first non-trivial integration; budget a week."

## 9. Open questions

- **OQ-1 (→ review-log, top): G27 residual contradiction.** §6 binds the **raw-API-bodies** path (reading
  (b)) as most consistent with the concrete v4 build, but AI-CONTEXT §5.4 still *ranks* the event-bus path
  best with no stated override. Confirm the event-bus path is purely latent (never wired) — or whether a
  future track promotes it for the action-event subset. (Mirrors C23 OQ-1; this is the binding side.)
- **OQ-2 (→ review-log): file-completeness detection (G26).** How does Claude Code / the C25 escape hatch
  signal a raw-body file is fully written (atomic rename? close? size-stability?)? The INV-4 mechanism
  depends on this and must be confirmed against the real emitter at sweep 2.
- **OQ-3 (→ review-log): exact `session.id` → parent-turn rule (G26).** First-body-of-session → root vs.
  attach to an existing session trajectory across bridge restarts; and whether one body maps to exactly one
  turn or splits request/response into separate turns. Freeze at sweep 2 with C21/C22.
- **OQ-4: buffer bound / durability ceiling (G33).** What is the maximum CXDB-outage window before the buffer
  overflows and the oldest trajectories are lost? v4 prescribes no durable unbounded queue (no Kafka, §5.3) —
  is a bounded local buffer acceptable for P11/P12, or does the optimized track need a spill-to-disk/WAL?
- **OQ-5: HTTP (:9010) vs binary (:9009) ingest under load.** v4 recommends HTTP for the bridge (AI-CONTEXT
  §5.4 line 232) but the binary path is the high-throughput one (C21 I1); freeze which C24 uses at sweep 2
  (interacts with G26 back-pressure and the §13.2 dual-endpoint config). (Mirrors C21 OQ-4.)
