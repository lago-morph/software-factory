# C23 — Event Bus  (Spec, canonical track)

> Source: AI-CONTEXT §3.2 "nine concepts" (line 87 "Event Bus / Append-only JSONL with monotonic seq / P9, P10, P11"), §5.4 bridge-impedance table (line 228 "Gas City event bus JSONL → CXDB / **Lowest** / Events already attributed and trajectory-shaped"), §5.5 "what CXDB adds over plain JSONL" (lines 234–239); README §Part 4 (P9 attribution table line 228 "Audit trail / Queryable history / Gas City event bus + bead history / MIT / Native"; P11 event-substrate line 252 "Event substrate / Records every action / Gas City event bus (always), CXDB (for trajectories) / MIT / Apache 2.0 / Native + bridge"; P9 attribution narrative lines 222, 231 "Attribution flows automatically through beads and events without configuration"); spec/C01 §3 I7 (event bus seam, lines 87) + §4 (event-bus log state, line 111) + INV-3 (universal attribution); component-inventory C23 row (line 35 "Append-only JSONL with monotonic seq; records every action; lowest-impedance CXDB source", gaps A29/B46, depends C01, foundational yes), Batch-1 note (line 107); F-MODE-COVERAGE F10, F14, F11, F32, F43; ambiguities-and-gaps G27.
> Inventory ID: C23   Kind: data-store   Status: sweep-2
> Track: canonical (formerly Track A / faithful)
> Binding decisions obeyed: **D-5** (C41 owns the provenance hash-chain, computed over C23-provided
> ordered `event_id`s; C23 provides gap-free ordered `event_id`s ONLY, it does NOT provide the chain),
> **D-6** (canonical track, not "Track A").

## 1. Purpose & responsibility

C23 is the factory's **event bus**: the **append-only JSONL action log with a monotonic sequence number**
that is one of Gas City's five core primitives (AI-CONTEXT §3.2 concept 3). It is the substrate seam that
**records every action** taken in the factory — every dispatch, every gate, every bead transition, every
tool-node invocation — as an ordered, attributed, replayable stream (component-inventory C23; README line
252 "Records every action"). Together with the bead store (C19/C20) it forms the **Persistence & Memory**
audit foundation: beads are the *typed work-graph* (current state), the event bus is the *time-ordered log
of how that state was reached* (AI-CONTEXT §2; README line 228 "Audit trail … Gas City event bus + bead
history").

Like C01 and C21, C23 is **part of the adopted Gas City substrate** (MIT), not a factory-authored store
(README line 252 "MIT / Native"). C23's deliverable is therefore **the spec-of-record for the event-bus
seam C01 exposes (I7)**: the JSONL record shape, the monotonic-seq + append-only invariants, the universal-
attribution contract it inherits, and the contract handed to the two known consumers — the **CXDB bridge**
(C24, which treats the event bus as its *lowest-impedance* source) and the **identity/attribution model**
(C41, which "rides events"). It is **Batch-1 foundational** (component-inventory line 107): observability,
audit, self-healing, and the CXDB bridge all read from here.

**Responsibilities (what C23 is the spec-of-record for):**
- **Append-only event log** — every action appends exactly one JSONL record; records are never mutated or
  deleted in place (AI-CONTEXT §3.2 concept 3).
- **Monotonic sequence number** — each record carries a strictly-increasing `seq` that imposes a **total
  order** on events and lets consumers checkpoint and resume from a position (AI-CONTEXT §3.2 concept 3).
- **Universal attribution** — every event carries `created_by` automatically (inherited from the substrate
  invariant, spec/C01 INV-3; README line 231 "without configuration"). This is what makes the bus
  the corpus's strongest P9 match (F14).
- **"Records every action"** — the bus is the *complete* action ledger: dispatch, gate decisions, bead
  transitions, mail/nudge, tool-node runs, healer actions all emit events (README line 252; component-
  inventory C23).
- **Lowest-impedance CXDB source** — because events are *already attributed and trajectory-shaped*, the
  event-bus JSONL is the cheapest bridge path into CXDB (AI-CONTEXT §5.4 line 228). C23 owns *that this
  stream exists and is shaped to be bridgeable*; the bridge binary is C24.
- **Audit-trail / replay seam** — a queryable, ordered history supporting P9 (attribution), P10 (memory),
  P11 (self-healing observability) (AI-CONTEXT §3.2 concept 3 "P9, P10, P11").

**Explicitly NOT (boundaries):**
- **NOT factory-authored.** C23 is the Gas City event bus, adopted as part of the substrate (C01). The
  deliverable is the *seam spec + the record/ordering/attribution contract handed to C24/C41*, not a new
  Go event-bus implementation (README line 252 "Native"; mirrors spec/C01 §1 adoption boundary).
- **NOT the bead store.** Beads (C19/C20) are the *typed work-graph* — current, mutable, query-shaped
  state. C23 is the *append-only log of actions*. They are distinct Gas City concepts (AI-CONTEXT §3.2
  concepts 2 vs 3) and address different principles (beads P1/P5/P9/P10; bus P9/P10/P11). C23 does not own
  task state or dependencies.
- **NOT CXDB / the trajectory store.** C21 (CXDB) is a *separate Apache-2.0 content-addressed trajectory
  store* added in Phase 1 via a bridge. C23 is the *always-on MIT event bus* in the base substrate (README
  line 252 "Gas City event bus (always), CXDB (for trajectories)"). The event bus is plain JSONL; CXDB adds
  BLAKE3 dedup / O(1) branching / type projection *over* what plain JSONL gives (AI-CONTEXT §5.5).
- **NOT the bridge.** The event-bus-JSONL → CXDB **bridge** is **C24** (telemetry bridge). C23 defines the
  *source-side* stream shape and ordering; C24 owns delivery, batching, back-pressure, and ordering into
  CXDB (G26/G27 live at the bridge, not the bus).
- **NOT the identity/actor model.** C41 *defines* who/what can act and resolves `created_by`; C23 merely
  *carries* the `created_by` C41 stamps onto every event ("identity-attribution rides events", component-
  inventory C41 row, depends-on C23). C23 owns the attribution *field on the record*, not the actor schema.
- **NOT a message broker / pub-sub bus despite the name.** "Event bus" here is Gas City's *append-only JSONL
  log* primitive (AI-CONTEXT §3.2), not a Kafka/NATS-style network broker. Durable inter-agent messaging is
  the separate **Mail + Nudge** concept (C06; AI-CONTEXT §3.2 concept 6). No Kafka — consistent with the
  CXDB "no Postgres/Redis/Kafka" stance (AI-CONTEXT §5.3).
- **NOT OTLP / Claude Code telemetry.** Claude Code's OTLP metrics/logs and `OTEL_LOG_RAW_API_BODIES`
  (AI-CONTEXT §4.3) are a *different* observability stream consumed by C24's bridge; the event bus is Gas
  City's own internal action log. (The §5.4 impedance table contrasts the two as distinct bridge sources.)

## 2. Context & dependencies

| Direction | Component | Relationship |
|---|---|---|
| Upstream (depends on) | **C01** Gas City substrate | C23 *is* the event-bus seam C01 exposes as I7 (spec/C01 §3, line 87); its append-only-JSONL log is C01-owned state (spec/C01 §4, line 111). Inventory C23 "Depends on: C01". |
| External dependency | **Gas City** (MIT) | The adopted substrate providing the event-bus primitive (AI-CONTEXT §3.2 concept 3). C23 inherits Gas City's migration-tail risk (AI-CONTEXT §3.5) like C01. |
| Tightly-coupled peer | **C41** Identity / attribution | "identity-attribution rides events" — C41 resolves the `created_by` actor that C23 carries on every record (component-inventory C41 depends-on C23; README line 227). C23 supplies the carrier; C41 supplies the value + actor schema. |
| Downstream (consumer) | **C24** Telemetry → CXDB bridge | Treats the event-bus JSONL as its **lowest-impedance** source into CXDB (AI-CONTEXT §5.4 line 228). Reads the ordered, attributed stream; owns delivery/ordering into CXDB (G27). |
| Downstream (consumers) | **C40** Durable Orders; P11 self-healing components (anomaly/diagnosis) | Orders are *event-triggered* workflows that subscribe to events (e.g. crashes, gates) (component-inventory C40 depends-on C23; AI-CONTEXT §3.1 principle 11). Self-healing observes the action stream (AI-CONTEXT §3.2 concept 3 "P11"). |
| Downstream (consumers) | **Audit / query surfaces** (P9) | The bus is the queryable audit-trail history alongside bead history (README line 228). |

**Position in the system.** C23 is **Batch-1 foundational** (component-inventory line 107): "the load-
bearing schemas/interfaces everything else references". It sits *inside* the Gas City substrate (C01) but is
specced separately because C24 (bridge), C41 (identity), and C40 (Orders) each contract directly against the
event-record shape and ordering guarantees. It is **always-on** in every install — unlike CXDB it has no
feature-flag gate (README line 252 "always"); even the smallest Phase-0 install emits events (spec/
C01 §5 "Every action emits an event").

## 3. Interfaces / contracts

Sweep-1: interfaces **named and described**; concrete record schemas / append signatures / query API defer
to sweep 2 (and the actor-value contract to C41, the bridge delivery seam to C24).

| # | Interface | Direction | Description | Owning/detailing component |
|---|---|---|---|---|
| I1 | **Event append** | inbound (write) | Append exactly one JSONL record for an action; assigns the next monotonic `seq`; stamps `created_by`. The substrate-internal call every action path makes (spec/C01 §5 step 4). | C23 (this) |
| I2 | **Ordered read / tail / replay** | inbound (read) | Read events in `seq` order from a given position to the head; replay the action history; tail live. The audit/replay surface (AI-CONTEXT §3.2 "P9, P10, P11"). | C23 (this); C24/C40/self-healing consume |
| I3 | **Checkpoint / resume-from-seq** | inbound (read) | A consumer records its last-processed `seq` and resumes from there (the property that makes the bus a reliable bridge source). | C23 (this); C24 consumes (G27 ordering) |
| I4 | **`created_by` attribution field** | contract | Every record carries a resolvable actor id; C23 carries it, **C41 defines/resolves** the actor schema (README line 227; "rides events"). | **C41** (value+schema), C23 (carrier) |
| I5 | **CXDB-bridge source seam** | outbound (read) | The "events already attributed and trajectory-shaped" stream the C24 bridge consumes as the lowest-impedance CXDB path (AI-CONTEXT §5.4 line 228). C23 guarantees the stream *shape*; C24 owns delivery. C23 records are **plain JSONL with no `{bundle_id,type,version}` triple** — when bridged into CXDB they acquire a type triple *there* (C22/C24); the canonical bundle-id namespace is the **review-log XC-4** integrator ruling, not C23's concern. | C23 (source), **C24** (delivery) |
| I6 | **`[[service]]`/substrate lifecycle** | inbound (ops) | The bus is part of C01's lifecycle (always-on); operated alongside the substrate, no separate service block in the minimal install. | C01 (host), C23 (config of log location) |

**Invariants C23 must uphold (bus-level):**
- **INV-1 (append-only):** records are only ever *appended*; an existing record is never mutated, reordered,
  or deleted in place (AI-CONTEXT §3.2 concept 3 "Append-only JSONL"). This is what makes the log a trusted
  audit trail (F10).
- **INV-2 (monotonic seq / total order):** every record carries a strictly-increasing `seq`; `seq` imposes a
  total order on all events to checkpoint against (AI-CONTEXT §3.2 concept 3 "monotonic seq"). Whether
  `seq` is *gap-free* (single appender) or *monotonic-but-possibly-gapped* under concurrent producers is
  **not stated by v4** → OQ-4, to be confirmed against the pinned Gas City binary (checkpointing works
  either way: a consumer resumes from its last-seen `seq`).
- **INV-3 (universal attribution):** every event carries a resolvable `created_by` (inherited from
  spec/C01 INV-3; README line 231). No event is anonymous — this is the F14 guarantee.
- **INV-4 (records every action):** the bus is *complete* — every factory action that mutates state or makes
  a decision emits an event; there is no action path that bypasses the log (README line 252; component-
  inventory C23). This is an **adopted Gas City property** (C23 is not factory-authored), to be *verified*
  by the conformance pack (AC-7), not a guarantee C23-the-spec independently enforces over Gas City's
  internals — same G11-class "exercise the upstream claim" posture as C01/C21.
- **INV-5 (JSONL, one record per line):** the on-disk format is line-delimited JSON — one self-describing
  record per line — so it is grep-able, tailable, and bridgeable without a special reader (AI-CONTEXT §3.2;
  §5.5 frames CXDB as additions "over plain JSONL").
- **INV-6 (gap-free `event_id` stream — D-5 seam):** C23 provides a **gap-free, totally-ordered
  `event_id` stream** — the property D-5 names as C23's contribution to C41's tamper-evidence chain.
  Every appended record receives an `event_id` that is `(stream_name, seq)` with `seq` gap-free and
  strictly increasing. *No hash-chain is computed or maintained by C23.* The chain — if/when built — is
  **C41's** responsibility, computed over C23-provided `event_id`s. This is the D-5 boundary, stated
  verbatim from the review-log: **"C41 owns the provenance hash-chain, computed over C23-provided ordered
  `event_id`s. C23 provides gap-free ordered `event_id`s only; it does NOT provide the chain."**

### 3.1 `event_id` stream contract (D-5 seam — the C41-binding interface)

This subsection specifies the C23→C41 seam that D-5 froze. It is the contract C41 builds its
provenance hash-chain against, and the property the gap-free total-order acceptance test (AC-S2-O)
must verify.

**D-5 verbatim text** (review-log, adopted):
> "C41 owns the provenance hash-chain, computed over C23-provided ordered `event_id`s. C23 provides
> gap-free ordered `event_id`s only; it does NOT provide the chain. Update both specs."

**C23's obligation under D-5:**
- Every appended record is assigned an `event_id = {stream: <stream_name>, seq: <uint64>}` where `seq`
  is **gap-free and strictly increasing** within a named stream (no holes: if the last `seq` was N,
  the next MUST be N+1). This is the stronger-than-monotonic property D-5 depends on — a gap in the
  sequence is a detectable tamper signal for C41's chain.
- C23 exposes the `event_id` field on every record (field table §4.2).
- C23 does **not** compute, store, or verify any cryptographic hash over records. The chain,
  HMAC signing, and tamper-detection are C41's optional pack (README line 229; deferred per D-14/G37).
- C41 may call I2 (ordered read) to consume `event_id` values in `seq` order as inputs to its chain
  computation. C23 provides the ordered stream; C41 owns what it does with it.

**Why gap-free (not merely monotonic) is required:** A monotonic-but-gapped sequence would create
ambiguity for C41's hash-chain — a gap could be a dropped event (tamper) or a legitimately unused
sequence number. Gap-free removes the ambiguity: *any gap is a provenance failure*. (OQ-4 tracks
whether the pinned Gas City binary guarantees this in practice.)

> [FAITHFUL-FILL] **D-5 specifies "gap-free ordered `event_id`s" but v4 does not spell out
> whether the Gas City event bus is gap-free or merely monotonic.** AI-CONTEXT §3.2 says "monotonic
> seq"; it does not use "gap-free". The D-5 integrator ruling *adds* the gap-free requirement as the
> C41-binding property. C23 faithfully accepts this boundary: the gap-free invariant is C23's
> obligation to the D-5 seam, and OQ-4 is the verification spike against the pinned binary.

### 3.2 Publish / subscribe / delivery interface (sweep-2)

C23 is an **append-only log**, not a broker. There is no subscription registry inside C23. "Subscribe"
is implemented by a consumer tailing the log from a checkpointed `seq` (I2/I3). Delivery semantics:

| Property | Value | Reasoning |
|---|---|---|
| **Delivery guarantee** | At-least-once (on reader retry from last checkpoint) | The append-only log is durable; a consumer that crashes and resumes from its last saved `seq` will re-read and re-process events since that checkpoint. This gives at-least-once. Exactly-once requires idempotent consumers (their responsibility, not C23's). |
| **Order guarantee** | **Total order per stream** (gap-free `seq`; INV-2/INV-6) | All events on a stream are totally ordered by `seq`. Cross-stream ordering is wall-clock only (`ts` field). |
| **Durability** | Append persists before I1 returns | Append-only local file; the event is durable once appended. A crash before append completes means the event was never recorded (INV-4 failure). |
| **Delivery to C41** | Pull (I2 read, not push) | C41 reads the event_id stream via I2 to construct its chain; C23 does not push to C41. |
| **Delivery to C24** | Pull / tail | C24 tails I2 from its checkpoint; C23 does not push to C24. |
| **Back-pressure** | None in C23 | C23 appends unconditionally; producers are never blocked by consumer lag. Consumer lag is C24/C40's concern (G27). |

**I1 publish signature (sweep-2 concrete):**

```
append(event: EventRecord) → event_id: EventId
```

Where `EventRecord` is the record shape (§4.2) minus `seq` and `event_id` (assigned by C23 on append);
returns the assigned `event_id = {stream, seq}`. Fails loud if the backing store is unwritable (E5).

**I2 ordered read signature:**

```
read(from_seq: uint64, limit?: uint32) → []EventRecord
```

Returns records with `seq >= from_seq` in strictly ascending `seq` order, up to `limit` (or all if
omitted). Returns an empty list when `from_seq` is beyond the current head.

**I3 checkpoint / resume-from-seq:**

```
last_seq() → uint64   # head of the log; consumers save their own checkpoint
```

Consumers are responsible for persisting their last-processed `seq`. C23 provides `last_seq()` so
a new consumer can tail from the current head rather than replay the full history.

## 4. Data model / state

C23 *owns the event-log seam + record shape*; the **actor schema** behind `created_by` is owned by C41.
State C23 is the spec-of-record for:

| State | Description | Persistence | Detailed by |
|---|---|---|---|
| **Event log** (`events.jsonl`-style) | Append-only, line-delimited JSON; the ordered action ledger (AI-CONTEXT §3.2). | Append-only file (the Gas City event bus backing store). | C23 |
| **Monotonic `seq` counter** | The strictly-increasing, gap-free sequence assigned per append; the total-order + checkpoint key (INV-2/INV-6). | Derived from / persisted with the log. | C23 |
| **Per-record `created_by`** | Resolvable actor on every event (city/rig/agent) (README line 227). | Field on each JSONL record. | **C41** (actor schema), C23 (carrier field) |
| **Log location config** | Where the event log lives (path/rotation), part of C01's config. | Version-controlled `city.toml` (C03 model). | C03 (model), C01/C23 (binding) |

> [FAITHFUL-FILL] v4 specifies the event-bus *primitive* (append-only JSONL + monotonic seq + `created_by`)
> but not the concrete field-level event record. The minimal faithful elaboration of one record is:
> **`{event_id, seq, ts, created_by, action_type, target_ref?, payload}`** — where `event_id` is the
> D-5-seam identifier (stream + seq pair), `seq` is the monotonic gap-free order key (INV-2/INV-6), `ts`
> is the wall-clock timestamp, `created_by` is the inherited universal-attribution actor (spec/C01 INV-3;
> resolved by C41), `action_type` names the action that occurred (dispatch / gate / bead-transition / mail /
> tool-run / healer-action), `target_ref` optionally references the affected bead / session / molecule, and
> `payload` carries action-specific detail. This is the smallest set implied by "monotonic seq" + "records
> every action" + universal attribution + "events already attributed and trajectory-shaped" (AI-CONTEXT §5.4)
> + the D-5 gap-free `event_id` seam requirement. The actor-id shape inside `created_by` is **C41**.

**Consistency / lifecycle.** Append-only + gap-free monotonic seq give a **write-once, totally-ordered,
replayable** log: a reader can deterministically reconstruct the action history and checkpoint by `seq`. The
bus is **always-on from Phase 0** (additive to nothing — it is part of the base substrate; spec/C01 §4)
and unlike CXDB needs no feature flag (README line 252 "always"). The log is the *source-of-truth action
trail that survives independently of CXDB* — which is exactly why a CXDB outage is survivable (see §6, and
spec/C21 §6 G33 reading).

### 4.1 `EventId` — the D-5 seam type

| Field | Type | Req? | Semantics | Read-by | Write-by |
|---|---|---|---|---|---|
| `stream` | `string` | R | The named event stream (e.g. `"factory.main"`); scopes the `seq` namespace. One city may have multiple streams. | C41, C24, C40 read | C23 assigns on append |
| `seq` | `uint64` | R | Strictly-increasing, **gap-free** sequence number within the stream. If the prior appended `seq` was N, the next MUST be N+1 (INV-6). Any gap is a detectable ordering violation (E3). | C41 (hash-chain input), C24 (checkpoint), C40 (trigger match) | C23 assigns; never mutated |

`EventId` = `{stream, seq}`. This is the pair D-5 names: "C23 provides gap-free ordered `event_id`s" for
C41 to compute its hash-chain over. C23 does NOT hash, chain, or sign these values.

### 4.2 `EventRecord` — concrete wire schema (sweep-2)

Every JSONL line on the event bus is one `EventRecord`. Columns: **Field** / **Type** / **Req?**
(R = required, O = optional) / **Semantics** / **Read-by** / **Write-by**.

| Field | Type | Req? | Semantics | Read-by | Write-by |
|---|---|---|---|---|---|
| `event_id` | `EventId` | R | The D-5 seam identifier: `{stream, seq}`. The gap-free total-order key C41 builds its chain over (§3.1, INV-6). | C41 (chain), C24 (bridge), C40 (trigger) | C23 assigns |
| `seq` | `uint64` | R | Convenience copy of `event_id.seq`; the checkpoint key consumers persist (I3). Redundant with `event_id.seq` but present for grep/tail readability (INV-5). | All consumers | C23 assigns |
| `ts` | `timestamp` (ISO-8601 / RFC-3339) | R | Wall-clock time at append. Monotonic within seq order; not the ordering key (seq is). | Audit, C24 bridge | C23 stamps |
| `created_by` | `actor_id` | R | Resolvable actor (city/rig/agent) that triggered the action (INV-3; P9; spec/C01 INV-3). C23 **carries** the field; C41 **defines and resolves** the `actor_id` schema (I4). No anonymous events. | C41 (resolve), C24 (bridge attribution), audit | Action path writes; C23 stamps from substrate |
| `action_type` | `enum{…}` | R | Closed set of action kinds (§4.3). Each value names one class of factory event. | C40 (trigger predicates), C24 (bridge), audit | Action path writes |
| `target_ref` | `string` \| `bead_id` | O | Reference to the affected bead / session / molecule / formula. Free-form string or a C19 `bead_id`. Absent when no single target (e.g. a city-level event). | C40 (filter), audit | Action path writes |
| `payload` | `object` | O | Action-specific detail. Schema is per `action_type` (§4.3). Free-form map for forward compatibility; action-type-specific schemas frozen at T6 per the plan. | C24 (bridge into CXDB), consumers | Action path writes |

> [FAITHFUL-FILL] **The `seq` redundancy.** `event_id.seq` and the top-level `seq` field carry the same
> value. v4 (AI-CONTEXT §3.2) says "monotonic seq" as a first-class field; D-5 adds `event_id = {stream,
> seq}` as the seam type. The minimal consistent approach is to keep both: `seq` at the top level (faithful
> to v4's framing and grep-friendliness per INV-5), `event_id` as the D-5 seam object. They must match;
> a mismatch is E6 (see §6.1).

### 4.3 `action_type` enumeration (sweep-2)

The closed set of action kinds the bus records. Every factory action that mutates state or makes a
decision MUST appear here (INV-4). Enumeration frozen at T6 (plan §4).

| `action_type` value | Description | Primary emitter | Typical `target_ref` |
|---|---|---|---|
| `dispatch` | A bead/wisp was dispatched to an agent or pool (AI-CONTEXT §3.2 concept 8) | C05/C06 | bead_id |
| `gate_decision` | A formula gate evaluated and produced a pass/fail decision | C11/C12 | formula/bead ref |
| `bead_transition` | A bead changed `status` or `type` (C19/C20 write) | C19 via C20 | bead_id |
| `mail_sent` | A durable mail message was enqueued (C06) | C06 | session/rig ref |
| `nudge_sent` | An ephemeral nudge was sent (C06) | C06 | session ref |
| `tool_invocation` | A tool-node was invoked in a formula run (C17) | C17 | formula/molecule ref |
| `healer_action` | The self-healing loop took an action (C36/C37/C39) | C39/C36/C37 | bead_id (anomaly/fix_task) |
| `override_recorded` | An operator override was written as a bead (C35) | C35 | bead_id (override) |
| `order_triggered` | A durable Order was triggered by an event match (C40) | C40 | order ref |
| `session_lifecycle` | A session was started / stopped / crashed (C01) | C01 | session ref |

> [FAITHFUL-FILL] **The enumeration is inferred.** v4 says "records every action" (README line 252) and
> lists the action classes in the dependency graph (dispatch, gate, bead transitions, mail/nudge, tool runs,
> healer) but never enumerates `action_type` values. This table is the minimal faithful set covering every
> action path named in v4. It is **open-for-extension** (adding a value requires a schema version bump, not
> a breaking change) and must be verified against the pinned Gas City binary at T6 (plan).

## 5. Behavior

**Stand up (Phase 0).** The event bus comes up *with* the Gas City substrate — no separate install. The
minimal install (C01 §4) already emits events; there is no off switch (README line 252 "always").

**Emit an event (append path).**
1. Any factory action path (dispatch, gate, bead transition, mail/nudge, tool-node run, healer action)
   calls I1 with `{action_type, target_ref?, payload}`.
2. C23 stamps `created_by` (the substrate's universal-attribution actor; C41-resolved) (INV-3).
3. C23 assigns the **next monotonic `seq`** (INV-2) and a timestamp.
4. C23 **appends** exactly one JSONL record to the event log (INV-1, INV-5). The record is now durable and
   ordered.

**Read / replay / tail (consume path).** A consumer (C24 bridge, C40 Orders, self-healing, audit query)
reads via I2 from a checkpointed `seq` (I3) to the head, in order. Orders are *triggered* by matching events
(AI-CONTEXT §3.1 principle 11 "Orders subscribing to crashes/gates"). The CXDB bridge (C24) tails the log
and posts the *already-attributed, trajectory-shaped* records to CXDB (AI-CONTEXT §5.4 line 228) — see §7
G27 for which source v4 actually wires.

### 5.1 Publish → ordered delivery → C41 chain-input (sequence diagram)

The diagram shows the three roles interacting with C23: an **action path** that emits an event (publish),
a **general consumer** (e.g. C24 bridge or C40 Order) that reads the ordered stream, and **C41** consuming
the `event_id` stream as input to its provenance hash-chain. The diagram covers the D-5 boundary: C23
hands over gap-free `event_id`s; C41 owns what it computes over them.

```mermaid
sequenceDiagram
    participant A as Action Path (any emitter)
    participant C23 as C23 Event Bus
    participant Con as Consumer (C24/C40)
    participant C41 as C41 Identity / Attribution

    A->>C23: append({action_type, target_ref, payload, created_by})
    C23->>C23: assign event_id = {stream, seq=N+1} (gap-free, INV-6)
    C23-->>A: return event_id

    Con->>C23: read(from_seq=last_checkpoint)
    C23-->>Con: []EventRecord in seq order (INV-2, total order)
    Con->>Con: process records; persist last seq as checkpoint

    C41->>C23: read(from_seq=chain_head)
    C23-->>C41: []EventRecord with gap-free event_ids
    C41->>C41: extend hash-chain over event_ids (D-5: C41 owns chain, not C23)
```

**D-5 boundary visible in the diagram:** C23 returns `event_id` values to C41 via the same I2 read
interface all consumers use. C23 does nothing special for C41 — it provides the ordered, gap-free stream.
C41 is the sole actor that extends a hash-chain; C23 never does.

### 5.2 Gap detection (ordering violation — E3)

A consumer (typically C41) can detect a gap by comparing the received `seq` to its expected next value.
If `received_seq != expected_seq`, a gap has occurred — the bus's gap-free invariant (INV-6) was violated.
This is E3 in the error taxonomy (§6.1). The consumer must fail loud and not silently accept a gapped stream,
because from C41's perspective any gap is a potential tamper signal.

## 6. Failure modes & handling

C23 carries the audit/attribution F-modes the event bus is the corpus's strongest match for, plus the
gap thread it shares with the CXDB bridge (G27).

**F14 (Attribution collapse) — addressed.** Every event carries `created_by` automatically (INV-3); "P9 is
Gas City's strongest native match in the corpus … attribution flows automatically through beads and events
without configuration" (README line 231; F-MODE-COVERAGE F14 "Addressed … every bead, event, action carries
actor"). C23's append path makes an anonymous event impossible — the guarantee underwriting F14. *The actor
value's correctness is C41's; C23 guarantees the field is present and resolvable.*

**F10 (Findings disappear into chat) — addressed.** Because the bus is the **complete, append-only** record
of every action (INV-1, INV-4), decisions and findings are captured in a durable, queryable trail rather
than lost to ephemeral chat (F-MODE-COVERAGE F10 "Override log discipline … content-addressed trajectory
store"). The event bus is the always-on half of that pairing (CXDB is the bridged half).

**F11 (Renumbering breaks references) — partial at this layer.** v4's primary F11 mechanism is CXDB BLAKE3
content-addressing (F-MODE-COVERAGE F11). C23's contribution is the **monotonic `seq`**: an immutable,
never-reused ordering key gives stable references into the action history. C23 does *not* content-address
payloads (that is CXDB's add-over-plain-JSONL, AI-CONTEXT §5.5) — so C23 addresses F11 *for event identity/
ordering* and defers payload-level immutability to C21/CXDB.

**F32 (Mail-injection / unsigned coordination) & F43 (RSI board-visibility) — partial / deferred.** The
event bus + bead history is the *audit-trail* leg of these mitigations (F-MODE-COVERAGE F32 "P9 attribution
+ optional HMAC signing layer"; F43 "P9 attribution + audit trail + bead history"). C23 provides the
**attributed, append-only record** that makes coordination auditable; the **optional signed-provenance /
HMAC** layer is explicitly *optional and deferred* in v4 (README line 229 "Custom: signature on bead
provenance … optional, deferred"; owned by C41). C23 faithfully carries `created_by` and defers signing to
C41's optional layer.

**G27 (major) — event-bus ↔ CXDB impedance/path contradiction.**
> [AMBIGUITY: G27] AI-CONTEXT §5.4 ranks **"Gas City event bus JSONL → CXDB"** as **Lowest impedance / best**
> ("events already attributed and trajectory-shaped", line 228), but the very next line **recommends the
> raw-API-bodies path** (ranked #2 "Low") and §11.1/README build around that, with no stated reason for
> overriding the ranking. Two readings: **(a)** the event-bus path is the intended CXDB source (honor the
> ranking) — C23's stream is the canonical bridge input; **(b)** the raw-API-bodies path is intended (honor
> the recommendation) — the event bus is *one available* low-impedance source but C24 wires the raw-bodies
> path because raw API bodies are *conversation-shaped end-to-end* whereas Gas City events are action-shaped
> (a turn-DAG needs the model's actual request/response bodies, which the event bus does not contain).
> **Chosen: (b), with C23 remaining a first-class lowest-impedance *source* the bridge MAY also consume.**
> This is most consistent with the rest of v4: README §Part 4 and AI-CONTEXT §11/§13.2 concretely build the
> raw-API-bodies bridge (the standalone Go binary watching `OTEL_LOG_RAW_API_BODIES`, AI-CONTEXT §5.4 line
> 232), and CXDB's *turn* unit needs the conversation payloads that live in raw API bodies, not in Gas City's
> action events. *(That events are action-shaped and lack the full model request/response bodies is a
> **faithful inference** grounding choice (b): v4 calls events "trajectory-shaped"/"attributed" (§5.4) but
> never states whether the full bodies ride on them — so this is the basis for picking (b), not a v4 fact.)*
> The "Lowest" ranking is best read as *"events are the cheapest-to-bridge **because already
> attributed**"* — a property statement, not a build directive that overrides the explicit recommendation.
> **Faithful resolution for C23:** C23 guarantees its stream is *bridgeable* (attributed + ordered + shaped
> for replay, I5) so the event-bus path **remains available** and is the cheapest if/when needed; **which
> path C24 actually wires is C24's decision (G27 lives at the bridge seam).** C23 takes no position that
> contradicts v4 and surfaces the contradiction as an OQ → review-log.

**Degraded behaviour.** The event bus is the substrate's own durable log; if **CXDB** is down the event bus
**continues** unaffected and is the surviving source-of-truth action trail (this is what makes the C21 G33
fail-open reading hold — spec/C21 §6). If the **event log** write itself fails (disk full / I/O),
that is a substrate-level failure (C01) — faithful handling is fail-loud at the substrate (an action that
cannot be recorded must not be silently lost, given INV-4); the exact policy is a sweep-2 / C01 concern.
A partial/torn final line on crash is detectable (JSONL line-framing, INV-5) and is a known recovery case.

> F-mode applicability is owned by C57 (coverage map); C23 surfaces the bus-level failure classes
> (attribution loss F14, audit completeness F10, reference stability F11, unsigned coordination F32/F43,
> CXDB-path contradiction G27) and defers the canonical mapping there.

### 6.1 Error taxonomy (E-codes, sweep-2)

Enumerated failure modes across C23's three surfaces — **append** (I1), **read/checkpoint** (I2/I3),
and **ordering/gap** (INV-6). Each row: detection point, handling, and the AC-code that tests it.

| # | Failure | Surface | Detection | Handling | AC |
|---|---|---|---|---|---|
| **E1** | **Anonymous event** — `created_by` absent or empty on an appended record | append (I1) | Required-field check at append time (INV-3) | Reject the append; the action path MUST supply `created_by`. An event without attribution is a F14 failure and a chain-input violation for C41. | AC-S2-4 |
| **E2** | **Unknown `action_type`** — a value not in the §4.3 enumeration | append (I1) | Closed-set check (INV-4 contract) | Reject the append; unknown types bypass the completeness invariant. *G11-gated: if Gas City does not enforce natively, C02 pack enforces detect.* | AC-S2-3 |
| **E3** | **Ordering/gap violation** — `seq` is not N+1 from prior (INV-6 broken) | read (I2); detected by consumer | Consumer compares `seq` to `expected_next_seq` | Fail loud on the consumer side; C23 MUST NOT produce gaps (D-5 gap-free contract). If a gap is detected it is either a C23 bug or tamper — escalate; do NOT silently skip. C41 MUST treat a gap as a tamper signal. | AC-S2-O |
| **E4** | **Mutation of existing record** — a historical record was modified in place (INV-1 broken) | read/replay (I2) | Re-read of a historical record differs from its first-read value | Fail loud. The audit trail is corrupted; this invalidates C41's hash-chain and the entire F10 guarantee. Log the deviation; escalate to substrate-level ops. | AC-S2-2 |
| **E5** | **Append durability failure** — the backing store is unwritable (disk full / I/O error) | append (I1) | I1 returns an error | Fail loud (the action that cannot be recorded must not be silently lost, INV-4). The emitting action path MUST surface the failure; silent swallow is the F10 failure mode. Recovery is C01 substrate-level. | AC-S2-5 |
| **E6** | **`seq` / `event_id.seq` mismatch** — top-level `seq` field disagrees with `event_id.seq` | append (I1) or read (I2) | Field consistency check at append/read | Reject; one of the two fields was incorrectly set. A mismatch indicates a serialization bug in the emitter. | AC-S2-6 |
| **E7** | **`created_by` actor unresolvable** — the carried actor id fails C41 resolution | read (I2) / attribution layer | C41 resolution attempt fails | C23's failure surface is limited to *carrying* the field; C41 reports unresolvability. C23 supplies the field value; C41 owns the verdict (I4). Flagged as F14-partial. | (C41 AC) |
| **E8** | **Torn/partial final JSONL line** — log file ends mid-record (crash during append) | read (I2) / startup | JSONL line-framing — a line that does not parse as valid JSON is detected immediately | The partial line is discarded (the append was not completed before crash); the prior complete record is the new head. This is a known recovery case (§6 "Degraded behaviour"); the truncated record was never durably committed. | AC-S2-7 |

> **D-5 boundary note.** C23 owns E1–E8 (append/read/ordering failures). C23 does **not** own
> hash-chain verification or HMAC checking — those are C41's E-codes against its own provenance layer.
> E3 (gap violation) is the critical shared-surface: C23 guarantees no gaps (produces); C41 detects gaps
> (consumes); a gap triggers C41's tamper response, not a C23 recovery action.

## 7. Cross-cutting (security / cost / scale / observability / ops)

- **Security.** `created_by` on every event (INV-3) is the audit/attribution foundation (P9). The
  append-only + monotonic-seq shape gives a **tamper-evident-by-convention** trail (out-of-order or missing
  `seq` is detectable), but C23 does **not** cryptographically sign events — the optional HMAC/signed-
  provenance layer is C41's deferred optional pack (README line 229). Plaintext-TOML log-location config
  inherits the G37 exposure thread (flagged, deferred to config/secrets owner — out of C23 faithful scope).
  > [AMBIGUITY resolution — D-5] The integrator's ruling **D-5** fixes the tamper-evidence ownership split:
  > **C41 owns the provenance hash-chain**, computed over **C23-provided ordered gap-free `event_id`s**.
  > C23's faithful contribution is exactly that — the ordered, gap-free, append-only `seq`/`event_id` stream
  > (INV-1/INV-2) — and **not** any cryptographic chain over records. So C23 provides the ordered ids only;
  > the chain (if/when built) is C41's, keyed on C23's `event_id = (stream, seq)`.
- **Cost.** Append-only local file I/O; no managed-store fees (consistent with the CXDB "no Postgres/Redis/
  Kafka" stance, AI-CONTEXT §5.3). v4 gives no per-event cost model.
- **Scale.** "Records every action" (INV-4) means event volume scales with factory activity; v4 names no
  sharding/rotation story for the bus → log growth/rotation is a known limitation (OQ). The monotonic-seq +
  checkpoint design (I3) means consumers scale by resuming, not re-reading.
- **Observability.** C23 *is* a core observability substrate (the action stream feeding P11 self-healing and
  the audit query surface). Its own health (append latency, log growth, last-seq lag for the bridge) is what
  C24/ops monitor.
- **Ops.** Always-on with the substrate (no separate service). Log location + rotation are the key ops
  config (C03 model). Inherits Gas City's migration-tail risk (AI-CONTEXT §3.5): a JSONL-format or seq-
  semantics change upstream would ripple to C24/C41 — pin the Gas City version (mirrors spec/C01
  INV-1).

## 8. Acceptance criteria & test strategy

### 8.1 Sweep-1 high-level criteria (preserved)

1. **AC-1 (always-on append — INV-4/I1):** in the minimal Phase-0 install, performing a unit of work
   produces event records for each action with **no configuration** (README line 231; spec/C01 §5).
2. **AC-2 (append-only — INV-1):** existing records are never mutated/reordered/deleted; a re-read of the log
   yields byte-identical historical records.
3. **AC-3 (monotonic seq + total order — INV-2):** every record's `seq` is strictly greater than the prior
   record's; the order is total.
4. **AC-4 (universal attribution — INV-3, addresses F14):** every event carries a **resolvable** `created_by`;
   no anonymous events exist (README line 231). *Actor-value correctness is verified jointly with C41.*
5. **AC-5 (ordered read / replay / checkpoint — I2/I3):** a consumer can read from a checkpointed `seq` to
   head in order, and resume from its last-processed `seq` after restart.
6. **AC-6 (bridgeable source — I5, addresses G27):** the event stream is *attributed and trajectory-shaped*
   such that the C24 bridge can consume it as a CXDB source (AI-CONTEXT §5.4 line 228). *Which path C24 wires
   is C24's; this AC proves the event-bus path is viable.*
7. **AC-7 (audit completeness — INV-4, addresses F10):** every state-mutating/decision action emits an event;
   an audit query over the log reconstructs the action history with no silent gaps.
8. **AC-8 (CXDB-independence — supports C21 G33):** with CXDB down, the event bus keeps appending and remains
   the surviving source-of-truth action trail (spec/C21 §6 fail-open reading).

### 8.2 Concrete acceptance tests (sweep-2)

Each is an executable check against the **Gas-City-event-bus conformance pack** (boots the pinned Gas City
substrate). `assert reject(...)` = the call is refused / returns error. `assert seq_of(records)` = the
`seq` values of the returned list. `assert eq(a, b)` = values are identical. Notation:
`eb.append(r)` = call I1; `eb.read(n)` = call I2 from seq=n; `eb.last_seq()` = call I3.

**Append path (I1) and required fields**

- **AC-S2-1 (always-on, no-config)** — Boot the minimal Gas City substrate. Perform one dispatchable
  action. Assert `len(eb.read(0)) >= 1` with no event-bus configuration beyond the substrate default.
  Verifies INV-4/AC-1.

- **AC-S2-2 (append-only)** — Append records r1, r2. Read both back. Modify `r1.payload` in memory.
  Re-read the log. Assert the on-disk r1 equals the original (not the modified copy). Verifies INV-1/E4.

- **AC-S2-3 (closed `action_type`)** — `assert reject(eb.append({action_type: "not_an_action_type", …}))`.
  *G11-gated: passes natively iff Gas City enforces the enum; else C02 pack-level check.* Verifies E2/INV-4.

- **AC-S2-4 (no anonymous events)** — `assert reject(eb.append({created_by: null, action_type: "dispatch", …}))`.
  Verifies E1/INV-3/AC-4/F14.

- **AC-S2-5 (durability failure loud)** — Simulate an unwritable backing store (e.g. chmod the log file).
  Call `eb.append(…)`. Assert the call returns an error (does not silently succeed). The emitter must be
  able to detect and surface the failure (E5/INV-4).

- **AC-S2-6 (`seq`/`event_id.seq` consistency)** — Append a valid record. Call `eb.read(0)`. Assert
  `record.seq == record.event_id.seq` for every returned record. Verifies E6/§4.2.

**Ordering and gap-free `event_id` stream — the D-5 property**

- **AC-S2-O (gap-free total order — the C41-seam test)** — Append N=100 records in sequence. Read all.
  Assert `seq_of(records) == [1, 2, …, N]` — no gaps, no reordering. Then checkpoint at seq=50 and
  append 10 more. Read from seq=50. Assert `seq_of(result) == [50, 51, …, 60]`. Assert `event_id.seq`
  equals `seq` for every record. **This is the primary D-5 property test: the event_id stream C41
  depends on is gap-free and totally ordered.** Verifies INV-2/INV-6/D-5/AC-3.

**Ordered read / replay / checkpoint (I2/I3)**

- **AC-S2-R1 (read from checkpoint)** — Append 20 records. Checkpoint at seq=10. Append 10 more. Call
  `eb.read(10)`. Assert exactly 21 records returned (seq 10 through 30 inclusive). Verifies I2/I3/AC-5.

- **AC-S2-R2 (resume after crash)** — Append records, save checkpoint at seq=K. Simulate crash/restart
  (re-instantiate the bus from backing store). Call `eb.read(K)`. Assert records from K to head returned
  in seq order. Verifies I3/AC-5.

**Torn-line recovery (E8)**

- **AC-S2-7 (torn final line)** — Append a valid record (seq=N), then write a partial (non-terminated)
  JSON fragment directly to the log file. Re-open the bus. Assert: (a) `eb.last_seq() == N` (partial line
  discarded), (b) `eb.read(0)` returns records 1..N with no parse errors. Verifies E8.

**Audit completeness and CXDB-independence**

- **AC-S2-8 (audit completeness)** — Run a standard factory workflow (dispatch → gate → bead transition).
  Assert that `eb.read(0)` contains events with `action_type` in {`dispatch`, `gate_decision`,
  `bead_transition`} — no silent-gap action paths. Verifies INV-4/AC-7.

- **AC-S2-9 (CXDB-independence)** — Bring down CXDB. Perform an action. Assert `eb.append(…)` succeeds
  and the record is readable via `eb.read(…)`. Assert CXDB status has no effect on bus append or read.
  Verifies AC-8.

**Test strategy.** These tests form the **Gas-City-event-bus conformance pack** (mirroring the C01/C21
conformance shape). They boot the pinned Gas City substrate and assert AC-S2-1…AC-S2-9 against the
*real* event bus. **AC-S2-O (gap-free total order) is the gate test for the C41 seam** — it must pass
before C41 can build its hash-chain on C23's stream. **All tests must pass before C24 (bridge), C41
(identity), and C40 (Orders) build against C23**, since all three contract against the record shape and
ordering guarantees.

## 9. Open questions

- **OQ-1 (→ review-log, top): G27 event-bus-vs-raw-bodies CXDB path.** AI-CONTEXT §5.4 *ranks* the event-bus
  path lowest-impedance but *recommends* raw-API-bodies, with no stated override reason. §6 picks reading (b)
  (raw bodies wired; event bus remains an available source) as most consistent with the concrete build, but
  the contradiction is unresolved in v4 — freeze the bridge source at sweep 2 with C24, and confirm whether
  the event-bus path is ever wired or purely latent.
- **OQ-2 (→ review-log): exact event record schema + `action_type` enumeration.** The §4 [FAITHFUL-FILL]
  record (`{seq, ts, created_by, action_type, target_ref?, payload}`) and the closed set of action types
  must be frozen at sweep 2 before C24/C41/C40 contract against them.
- **OQ-3: `created_by` carrier-vs-resolver seam with C41.** Confirm C23 owns the *field* and C41 owns the
  *actor schema + resolution* ("rides events"), and exactly what actor-id shape lands in the record.
- **OQ-4: `seq` semantics under concurrency / crash.** Is `seq` strictly gap-free (single appender) or
  monotonic-but-possibly-gapped under concurrent producers? Torn-final-line recovery on crash and log
  rotation/growth bounds are unspecified in v4 → confirm against the pinned Gas City binary (mirrors the
  C21 "exercise the upstream claims" thread).
