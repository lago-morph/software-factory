# C21 — CXDB Trajectory Store  (Spec, Track A)

> Source: README §Part 4 (Persistence line 122 "CXDB for content-addressed trajectories … CXDB via bridge"; memory-layer table line 241 "Content-addressed trajectory store / Replay + branching + dedup / **CXDB** / Apache 2.0 / Bridge pack"; query interface line 242; event substrate line 252; P11 substrate line 261; P12 counterfactual line 274, line 278 "CXDB … the driver is your most significant invention"; license line 290; transfusion line 302; §Part 6 Phase 1 lines 388–397 install + bridge + "CXDB substrate ready for P11 anomaly clustering and P12 counterfactual replay"; §Part 7 line 500 "Foundational components (CXDB …) stay as upstream OSS"; line 541 "Install CXDB … first non-trivial integration; budget a week"), AI-CONTEXT §5 (CXDB — content-addressed trajectory store: §5.1 metadata lines 196–202, §5.2 ingestion API lines 204–210, §5.3 turn model lines 212–220, §5.4 bridges lines 222–232, §5.5 "what CXDB adds" lines 234–240), §10 license table (line 325 "Content-addressed substrate / CXDB / Apache 2.0 / Only player; mature for purpose"; line 359 counterfactual; line 375 layer mapping), §11 decisions (lines 463–466 CXDB integration Phase 1 + bridge path), §13.2 Phase-1 `[[service]]` block (lines 558, 579), §14 risk register (line 618 "CXDB stays small-team"), §15.2 repo (line 635); component-inventory C21 row (line 33) + critical-path notes (lines 107, 123); ambiguities-and-gaps G17, G33 (and G11 content-addressing thread).
> Inventory ID: C21   Kind: data-store   Status: sweep-1
> Track: A (faithful)

## 1. Purpose & responsibility

C21 is the factory's **content-addressed trajectory store**: an *adopted* (not authored) install of
**CXDB** (`github.com/strongdm/cxdb`, Apache 2.0 — *both the repo URL and the license are unverified
upstream assertions per G11; treat as provisional until the OQ-3/§6 conformance run confirms them*),
configured as the substrate that records agent
**trajectories** — the conversation-shaped, turn-by-turn history of every run — in a form that supports
**deduplication**, **O(1) branching**, and **replay**. It is the second persistence pillar alongside the
bead work-graph (C19): beads are the *typed work-ledger*, CXDB is the *content-addressed trajectory log*
(README line 122; AI-CONTEXT §2 line 52 "event store (CXDB) + work ledger (Beads)").

The store's organizing unit is the **turn** (not a span or an event): each turn carries a parent-turn
pointer forming a **DAG** (not a tree), payloads are content-addressed by **BLAKE3** of their
msgpack-serialized bytes ("Blob CAS"), and forking a trajectory from any point is **O(1)** — a new head
pointer, no history copy (AI-CONTEXT §5.3). This turn-DAG + CAS shape is what makes the two highest-value
loops buildable: **P11 self-healing** (anomaly→diagnosis over recorded trajectories) and **P12
self-optimization** (counterfactual replay = re-run a trajectory from a midpoint via O(1) branching)
(README lines 261, 274, 278; AI-CONTEXT §5.5).

**Responsibilities (what C21 is the spec-of-record for):**
- **Trajectory ingest** via CXDB's two native protocols: **binary msgpack on port 9009** (high-throughput
  writer, Go client library) and **HTTP/JSON REST on port 9010** (browsers, dashboards, ad-hoc queries)
  (AI-CONTEXT §5.2). C21 owns *that these endpoints exist and how the factory points at them*; the
  **bridge** that feeds them from Claude Code raw-API bodies is a *separate* component (C24).
- **Turn-DAG storage** — append a turn with a parent pointer; maintain the DAG of trajectories
  (AI-CONTEXT §5.3).
- **BLAKE3 content-addressing / Blob CAS** — store each payload once, keyed by BLAKE3 of its
  msgpack bytes; identical payloads dedup automatically; the hash is tamper-evidence (AI-CONTEXT §5.3,
  §5.5 line 236).
- **O(1) trajectory branching** — fork from any turn by creating a new head pointer with no history copy;
  the primitive C49 counterfactual-replay and self-healing investigations depend on (AI-CONTEXT §5.3 line
  216, §5.5 line 237).
- **Replay / retrieval** — reconstruct a trajectory by walking the parent chain; sub-ms retrieval over
  TB-scale (AI-CONTEXT §5.5 lines 239–240).
- **Hosting the dynamic type system** `{bundle_id, type, version}` per payload and the **type registry**
  (`registry/`) — CXDB *provides the mechanism*; the v4-specific **type bundle/schemas** registered into
  it are owned by **C22** (AI-CONTEXT §5.3 lines 218–219).
- **Query interface** — HTTP/JSON REST instead of grep over log files (AI-CONTEXT §5.5 line 240; README
  line 242).
- **File-backed storage layout** — `turns.log`, `blobs.pack`, `registry/`; **no Postgres/Redis/Kafka**
  (AI-CONTEXT §5.3 line 220).

**Explicitly NOT (boundaries):**
- **NOT authored by the factory.** Like C01, CXDB is *adopted verbatim* as upstream OSS (README line 500
  "Foundational components (CXDB …) stay as upstream OSS … The factory builds the orchestration glue, not
  the foundations"). Our deliverable is the **install + version-pin + `[[service]]` config + the type-bundle
  registration contract handed to C22 + the ingest/query seam handed to C24/consumers** — not CXDB's Rust
  source.
- **NOT the bridge.** The raw-API-bodies → CXDB **bridge** (a standalone Go tool-node binary in a pack
  that watches `OTEL_LOG_RAW_API_BODIES` and posts to :9010) is **C24** (README line 389; AI-CONTEXT §5.4
  line 232). C21 defines the *server-side ingest seam*; C24 owns delivery/ordering/back-pressure (G26).
- **NOT the v4 type schemas.** The concrete `{bundle_id, type, version}` bundle (e.g. the v4 turn/trajectory
  payload schemas) and viewpoint tagging are **C22** (inventory line 34). C21 hosts the registry mechanism;
  C22 fills it. This split is the faithful reading of inventory's "depends on: C21" for C22.
- **NOT the counterfactual-replay driver.** C21 provides the **O(1) branching primitive**; the *driver*
  that uses it to re-run trajectories from a midpoint for variant tests is **C49** — "your most significant
  invention … largely unsolved" (README line 278; AI-CONTEXT §10 line 359 "Primitive exists; driver yours").
- **NOT the bead store / event bus.** Beads (C19/C20) are the typed work-graph; the Gas City event bus
  (C23) is the append-only JSONL action log. CXDB is a *distinct* Apache-2.0 store added in Phase 1 via a
  bridge, not part of the Gas City substrate (README line 122; spec-faithful/C01 §1 boundary).
- **NOT an OTLP receiver.** CXDB has **no native OTLP receiver** and is explicitly positioned *against*
  OTel ("Spans model request trees, not conversations"); the OTLP→CXDB path is rejected (highest impedance)
  (AI-CONTEXT §5.2 line 210, §5.4 line 230; README line 466 "Skip OTLP → CXDB path"). C21 does not accept
  spans.

## 2. Context & dependencies

| Direction | Component | Relationship |
|---|---|---|
| Upstream (depends on) | **C01** Gas City substrate | C21 is registered as a Phase-1 `[[service]]` block in `city.toml` and its lifecycle is operated alongside the substrate (AI-CONTEXT §13.2 lines 558, 579). Inventory C21 "Depends on: C01". |
| External dependency | **CXDB** (`github.com/strongdm/cxdb`, Apache 2.0) | The adopted store itself: Rust server (~16k LOC) + Go client (~9.5k) + React/TS frontend (~6.7k) + type registry + k8s manifests (AI-CONTEXT §5.1). **G33** (partial-failure) and the §14 "CXDB stays small-team" risk live here (§6). |
| Downstream (consumer) | **C22** CXDB type registry & viewpoint tagging | Registers the v4 `{bundle_id, type, version}` bundle into C21's `registry/`; **critical-path dependent** (inventory line 123). |
| Downstream (consumer) | **C24** Telemetry → CXDB bridge | Posts trajectory turns to C21's :9010 HTTP ingest (or :9009 binary); defines the delivery seam (G26/G27). |
| Downstream (consumer) | **C49** Counterfactual replay driver | Re-runs trajectories from a midpoint via C21's O(1) branching; **critical-path dependent** "most significant invention" (inventory line 61). |
| Downstream (consumers) | **C36** Anomaly detection, **C37** Trajectory clustering, **C38** Diagnosis agent | The P11 self-healing loop reads/embeds/clusters/diagnoses over trajectories stored in C21 (inventory lines 48–50). |

**Position in the system.** C21 is **Batch-1 foundational** (inventory line 107) and the inventory names
it **the first thing to spec, carefully**: "C21 CXDB trajectory store (+ C22 type registry) — every
observability, clustering, replay, and loop-closure component reads/writes here. Resolves the most
foundational gaps (G17 schemas, G11 content-addressing). No exemplar for the v4-specific type bundle, so
spec this first and carefully" (inventory line 123). It is **on the critical path**: C49 (counterfactual
replay) and C22 (type registry) both depend directly on it. In the delivery plan it is **Phase 1** — the
"first non-trivial integration; budget a week" (README line 541).

## 3. Interfaces / contracts

Sweep-1: interfaces are **named and described**; concrete signatures/schemas defer to sweep 2 and to the
owning components (C22 for the type bundle, C24 for the bridge delivery seam).

| # | Interface | Direction | Description | Owning/detailing component |
|---|---|---|---|---|
| I1 | **Binary ingest (msgpack :9009)** | inbound (write) | High-throughput trajectory writer via the Go client library; append a turn + payload (AI-CONTEXT §5.2). The fast path for the bridge / Go writers. | C21 (this); C24 uses it |
| I2 | **HTTP/JSON ingest + query (REST :9010)** | inbound (write + read) | REST surface for browsers, dashboards, ad-hoc queries, and the recommended bridge post path (AI-CONTEXT §5.2, §5.4 line 232; README line 242 "CXDB HTTP API"). | C21 (this); C24 posts here |
| I3 | **Turn append (parent-pointered)** | inbound (write) | Append a turn carrying a parent-turn pointer, forming the DAG (AI-CONTEXT §5.3). Payload content-addressed on write. | C21 (this) |
| I4 | **Blob CAS (BLAKE3) put/get** | internal/inbound | Store/fetch a payload keyed by BLAKE3 of its msgpack bytes; identical payloads dedup (AI-CONTEXT §5.3, §5.5). | C21 (this) |
| I5 | **Branch / fork (O(1))** | inbound (write) | Create a new head pointer from any turn with no history copy (AI-CONTEXT §5.3 line 216). The primitive C49 builds on. | C21 (this); C49 consumes |
| I6 | **Replay / trajectory retrieval** | inbound (read) | Reconstruct a trajectory by walking the parent chain; sub-ms retrieval over TB-scale (AI-CONTEXT §5.5). | C21 (this); C36/C37/C38/C49 consume |
| I7 | **Type registry** (`{bundle_id, type, version}`, `registry/`) | inbound (config) + read | Register/resolve typed payload schemas (JSON bundles like `mycompany.agents.v1`). C21 hosts the mechanism; the **v4 bundle is C22**. C21-A deliberately does **not** name the v4 trajectory `bundle_id` — the tracks currently disagree (C21-B `softwarefactory.trajectory.v1`, C22-A `softwarefactory.v4`, C22-B `strongdm.factory.v4`, C20-B `v4.beads.v1`); see **review-log XC-4** and defer the canonical namespace to the integrator ruling. | **C22** (the bundle), C21 (host) |
| I8 | **`[[service]]` lifecycle** | inbound (ops) | Registered in `city.toml` as a Phase-1 service the substrate operates (AI-CONTEXT §13.2 lines 558, 579). | C01 (host), C21 (config) |

**Invariants C21 must uphold (store-level):**
- **INV-1 (content-addressing):** every payload is keyed by BLAKE3 of its msgpack-serialized bytes;
  storing the same bytes twice yields one stored blob (dedup) and the same key (AI-CONTEXT §5.3, §5.5).
  > [FAITHFUL-FILL] v4 states "BLAKE3 Blob CAS" and "`{bundle_id,type,version}` per payload" (AI-CONTEXT
  > §5.3) but does not spell out the *serialize-then-hash ordering*. "msgpack-serialize the payload, then
  > BLAKE3 the msgpack bytes" is the minimal faithful reading (msgpack is v4's named turn-payload
  > encoding); the *BLAKE3 CAS + dedup* property is v4-stated, the serialization-ordering detail is filled.
- **INV-2 (turn-DAG, not tree):** every turn except a root has exactly one parent pointer; multiple turns
  may share a parent (branching); the structure is a DAG (AI-CONTEXT §5.3 line 215).
- **INV-3 (O(1) branch):** forking from any turn allocates a new head pointer and copies **no** history
  (AI-CONTEXT §5.3 line 216, §5.5 line 237). Branch cost is independent of trajectory length.
- **INV-4 (tamper-evidence):** because keys are BLAKE3 of content, any payload mutation changes its key;
  the parent chain is therefore content-verifiable (AI-CONTEXT §5.5 line 236).
- **INV-5 (no external datastore):** storage is `turns.log` + `blobs.pack` + `registry/` only — no
  Postgres/Redis/Kafka (AI-CONTEXT §5.3 line 220).
- **INV-6 (no OTLP):** the store ingests turns, not OTel spans; OTLP is not an accepted protocol
  (AI-CONTEXT §5.2 line 210).

## 4. Data model / state

C21 *owns the install + config*; the **v4 payload schemas** are owned by C22 (deferred, faithful to
inventory). State C21 is the spec-of-record for at sweep 1:

| State | Description | Persistence | Detailed by |
|---|---|---|---|
| **Install + version pin** | The CXDB server binary, its pinned version/commit, k8s manifests if used (AI-CONTEXT §5.1). | Filesystem / container image + version control. | C21 |
| **`turns.log`** | Append log of turns, each with a parent-turn pointer; the DAG backbone (AI-CONTEXT §5.3). | Append-only file. | C21 |
| **`blobs.pack`** | BLAKE3-addressed Blob CAS of msgpack payloads; dedup store (AI-CONTEXT §5.3). | Packed file. | C21 |
| **`registry/`** | The dynamic type system: `{bundle_id, type, version}` JSON bundles (AI-CONTEXT §5.3). | Directory of JSON bundles. | **C22** (v4 bundle), C21 (host) |
| **`[[service]]` config** | The `city.toml` block pointing the factory at CXDB (Phase 1). | Version-controlled config. | C03 (model), C21 (this block) |

**The "turn" unit (faithful from AI-CONTEXT §5.3).** A *turn* is the unit of storage: it has (a) a
parent-turn pointer (root turns have none), and (b) one or more content-addressed payloads each tagged
with a `{bundle_id, type, version}` triple. A *trajectory* is a path through the turn-DAG (root → head). A
*branch* is a new head pointer rooted at an existing turn.

> [FAITHFUL-FILL] v4 specifies the turn *model* (parent pointer + content-addressed payloads + type triple)
> but not the concrete field-level turn record (e.g. turn id type, timestamp, actor, payload-key list). The
> minimal faithful elaboration is: **a turn record = {turn_id, parent_turn_id?, payload_refs: [blake3_key
> + type_triple], created_by}**, where `created_by` mirrors the substrate's universal-attribution invariant
> (spec-faithful/C01 INV-3; README line 231) so trajectories are attributable. This is the smallest set
> implied by "parent turn pointer" (AI-CONTEXT §5.3) + "Blob CAS" + "type per payload" + the corpus-wide
> attribution requirement; the exact wire fields are sweep-2 and the *typed payload* schemas are C22's.

**Consistency / lifecycle.** Append-only `turns.log` + immutable BLAKE3-keyed blobs give a
write-once-read-many, content-verifiable store. Branching never mutates existing turns (INV-3). The store
is added in **Phase 1** (additive to the Phase-0 substrate; spec-faithful/C01 §4) and is "ready for P11
anomaly clustering and P12 counterfactual replay" once standing (README line 397).

## 5. Behavior

**Stand up (Phase 1).** Operator installs the pinned CXDB server, exposes :9009 (binary) and :9010
(HTTP), and registers a `[[service]]` block in `city.toml` (AI-CONTEXT §13.2). The v4 type bundle (C22)
is registered into `registry/`. The bridge (C24) is then pointed at :9010. Result: a content-addressed
trajectory store standing alongside the Gas City substrate, ready for P10 full memory + P11/P12 (README
lines 393, 397).

**Ingest a turn.**
1. A writer (the C24 bridge over :9010, or a Go writer over :9009) submits a turn: payload bytes +
   `{bundle_id, type, version}` + parent-turn pointer.
2. C21 msgpack-serializes the payload, computes its **BLAKE3** key, and stores it in `blobs.pack` **iff
   not already present** (dedup; INV-1).
3. C21 appends a turn record to `turns.log` referencing the blob key(s) and the parent pointer (INV-2).
4. Performance contract: **p50 < 1ms append for 10KB payloads** (AI-CONTEXT §5.5 line 239).

**Branch (O(1)).** A consumer (C49 driver, or a self-healing investigation) requests a fork from turn T.
C21 creates a new head pointer rooted at T; **no history is copied** (INV-3). Subsequent appends extend
the new branch independently. This is the primitive that makes counterfactual replay tractable
(AI-CONTEXT §5.5 line 237; README line 274).

**Replay / retrieve.** A consumer requests a trajectory by head turn; C21 walks the parent chain to the
root, resolving each turn's content-addressed payloads from the Blob CAS; **sub-ms retrieval over
TB-scale** (AI-CONTEXT §5.5 line 240). Type-aware projection lets the UI render typed payloads structurally
rather than as raw JSON (AI-CONTEXT §5.5 line 238).

> Sequence/state diagrams (Mermaid), the exact ingest/branch/query wire contracts, and the BLAKE3+msgpack
> serialization algorithm are **sweep-2+**. The *typed-payload* projection schemas are owned by **C22**.

## 6. Failure modes & handling

C21 carries the foundation-level gaps assigned to it (G17, G33) plus the inherited dependency risk (G11
thread / §14 "CXDB stays small-team").

**G17 (blocker) — no schema for the core stores; the v4-specific type bundle is never specified.**
CXDB's turn model is described (AI-CONTEXT §5.3) but "the v4-specific type bundle (`{bundle_id, type,
version}`) that v4 must register is never specified" (G17). For C21 the faithful resolution is a **split**:
C21 specifies *that* CXDB provides the registry mechanism and the turn-record shape (INV-1…INV-6 + the
[FAITHFUL-FILL] turn record in §4); the **concrete v4 payload schemas/bundle are owned by C22** (inventory
line 34 "Dynamic `{bundle_id,type,version}` type system"). C21 thus *addresses* G17 for the store mechanism
and **defers the schema content to C22** — the inventory's own decomposition. C21's acceptance (§8) requires
that a v4 bundle *can* be registered and resolved, proving the mechanism even before C22 fills it.

**G33 (major) — no story for partial/cascading failure of the OSS stack; specifically "What happens when
CXDB is down mid-run?"**
> [AMBIGUITY: G33] Two readings of C21's obligation. **(a)** *CXDB is best-effort observability* — if the
> store is down, the run continues and trajectories for that window are simply lost (degraded, fail-open).
> **(b)** *CXDB is load-bearing for P11/P12* — a down store must not silently drop trajectories the
> self-healing/optimization loops depend on, so the **bridge** must buffer/back-pressure (the actual seam).
> **Chosen: (a) for C21, with the durability obligation placed on C24.** This is most consistent with v4:
> the trajectory store is an *additive Phase-1* capability layered on a substrate that already has its own
> durable beads + event bus (the run's source-of-truth survives in Gas City regardless), and v4 explicitly
> locates the delivery/back-pressure question at the **bridge seam** ("back-pressure when CXDB is down" is
> listed under the *bridge* gap G26, not the store). Faithful handling: C21 must **fail-open to the run**
> (a CXDB outage does not crash the factory; the run proceeds on beads+events), MUST be **idempotent on
> replayed writes** (BLAKE3 content-addressing makes re-posting the same turn a no-op — INV-1 — which is
> exactly what a buffering bridge needs), and **defers** the buffer/retry/circuit-breaker design to **C24**
> (G26/G33). v4 prescribes no in-store HA design; inventing replication/clustering would exceed faithful
> scope, so C21 records "single-node, file-backed, no built-in HA" as a known limitation → OQ.

**§14 dependency risk — "CXDB stays small-team" (Medium/Medium).** Mitigation per v4: "Apache 2.0 means a
fork is always available; design integration to minimize lock-in" (AI-CONTEXT §14 line 618). Faithful
handling: keep the integration behind the named seams (I1–I8) so a fork/replacement is a seam-swap, and
**pin a version** (mirrors spec-faithful/C01 INV-1) so behaviour is reproducible.

**G11 thread (content-addressing / unverified third-party).** Like Gas City, every claimed CXDB behaviour
(BLAKE3 dedup, O(1) branch, p50<1ms, sub-ms TB-scale retrieval) is an *unverified upstream assumption* until
exercised. C21's acceptance (§8) includes a **conformance check** against the *pinned* CXDB that proves
dedup, O(1) branch (cost independent of length), and the performance contract — the de-risking gate before
C22/C24/C49 build on it.

**Degraded behaviour.** CXDB down ⇒ run continues on beads+events (fail-open, reading (a) above); the
window's trajectories are recoverable iff the bridge (C24) buffered them. Corrupt/partial turn write ⇒
detectable via BLAKE3 mismatch (INV-4).

> F-mode applicability is owned by C57 (coverage map); C21 surfaces the store-level failure classes
> (store-unavailability G33, version drift, small-team abandonment §14) and defers the canonical F-mode
> mapping there.

## 7. Cross-cutting (security / cost / scale / observability / ops)

- **Security.** BLAKE3 content-addressing gives **tamper-evidence** (INV-4) — a payload cannot be silently
  altered without changing its key. The `created_by` carried on turns (§4 [FAITHFUL-FILL]) preserves the
  P9 attribution chain into trajectories. Secret/endpoint handling for the `[[service]]` block inherits the
  G37 plaintext-TOML exposure (flagged, deferred to config/secrets owner — out of C21 faithful scope).
- **Cost.** v4 gives no CXDB-specific cost model (G32); storage is file-backed local I/O (no managed DB
  fees). The *consumer* costs (embedding all trajectories for C37, replay token spend for C49) belong to
  those components, not the store.
- **Scale.** Performance contract: **p50 < 1ms append for 10KB payloads; sub-ms retrieval over TB-scale**
  (AI-CONTEXT §5.5). O(1) branching means trajectory-count, not depth, drives branch cost. v4 names no
  multi-node/HA story → single-node ceiling is a known limitation (OQ).
- **Observability.** C21 *is* the observability substrate for trajectories; the React/TS frontend
  (AI-CONTEXT §5.1) renders typed payloads. The store's own health (up/down, lag) is what G33/C24 must
  monitor.
- **Ops.** Install = pinned CXDB server + :9009/:9010 exposure + `[[service]]` registration; "first
  non-trivial integration; budget a week" (README line 541). Version pin + reproducible install are the
  key ops invariants (mirrors C01).

## 8. Acceptance criteria & test strategy

Sweep-1 = high-level criteria (concrete tests at sweep 2).

1. **AC-1 (store stands up):** the pinned CXDB exposes :9009 (binary) and :9010 (HTTP), registered as a
   Phase-1 `[[service]]` in `city.toml`, alongside the Gas City substrate (AI-CONTEXT §13.2; README line
   388).
2. **AC-2 (content-addressing + dedup — INV-1):** posting two turns with byte-identical payloads stores
   the blob **once** and both turns reference the same BLAKE3 key (AI-CONTEXT §5.5 line 236).
3. **AC-3 (turn-DAG + replay — INV-2/I6):** a multi-turn trajectory is reconstructable by walking parent
   pointers from head to root; the result equals what was ingested.
4. **AC-4 (O(1) branch — INV-3):** forking from a turn at depth N is **constant-time / no history copy**
   independent of N; the new branch extends independently of the parent (AI-CONTEXT §5.3 line 216). *This
   is the primitive C49 depends on — verify it explicitly.*
5. **AC-5 (registry mechanism — addresses G17):** a v4 `{bundle_id, type, version}` bundle can be
   registered into `registry/` and resolved on read; typed payloads project structurally (AI-CONTEXT §5.3,
   §5.5 line 238). *Proves the mechanism C22 fills.*
6. **AC-6 (performance contract — *measure, don't assume*):** **measure and record** p50 append for 10KB
   payloads and point-retrieval latency against the *pinned* binary, comparing them to v4's asserted
   "p50 < 1ms / sub-ms over TB-scale" (AI-CONTEXT §5.5 lines 239–240). These numbers are **unverified
   upstream claims** (G11), not guaranteed properties — the AC is the de-risking measurement, and a miss
   is a finding for the integrator, not a build-blocking contract C21 must hit.
7. **AC-7 (fail-open + idempotent ingest — addresses G33):** with CXDB down, a factory run continues on
   beads+events without crashing; re-posting a previously-accepted turn is a **no-op** (BLAKE3 idempotency,
   INV-1) — the property a buffering C24 bridge relies on. *Buffer/retry design itself is C24's.*
8. **AC-8 (no OTLP — INV-6):** the store rejects/does-not-accept OTel spans; only turns are ingested
   (AI-CONTEXT §5.2 line 210).

**Test strategy.** A **CXDB-conformance pack** (mirroring the C01 conformance shape) that boots the pinned
CXDB and asserts AC-1…AC-8 — in particular the BLAKE3 dedup, the O(1)-branch cost-independence, and the
p50/retrieval contract — against a *real* pinned binary. This suite is the de-risking gate for the
content-addressing/branching/performance assumptions and **must pass before C22, C24, C36–C38, and C49
build on C21**.

## 9. Open questions

- **OQ-1 (→ review-log, top):** **G17 split** — C21 owns the registry *mechanism*, C22 owns the v4 *bundle*.
  Is the inventory split (C21 store / C22 type-bundle) the intended decomposition, and exactly which
  turn-record fields are C21's (the §4 [FAITHFUL-FILL]) vs which payload schemas are C22's? Freeze this seam
  at sweep 2 before C22 builds.
- **OQ-2 (→ review-log):** **G33 / store availability** — confirm the fail-open reading (run survives a
  CXDB outage on beads+events) and that the durability obligation (buffer/back-pressure) is C24's, not the
  store's. v4 has no in-store HA design; is single-node file-backed acceptable for P11/P12 volume, or does
  the optimized track need replication?
- **OQ-3:** Which CXDB version/commit to pin, and has anyone exercised the BLAKE3-dedup / O(1)-branch /
  p50<1ms claims against a real binary (the G11 content-addressing thread)? Until a conformance run exists,
  every branching/perf claim is provisional.
- **OQ-4:** Binary (:9009) vs HTTP (:9010) ingest path for the bridge — v4 recommends the HTTP post path for
  the bridge (AI-CONTEXT §5.4 line 232) but the binary path is the high-throughput one; freeze which C24
  uses at sweep 2 (interacts with G26 back-pressure).
