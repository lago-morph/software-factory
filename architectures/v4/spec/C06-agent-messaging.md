# C06 — Messaging (Mail + Nudge)  (Spec, canonical track)

> Source: AI-CONTEXT §3.2 concept 6 "Messaging (Mail + Nudge)" (L90 — *"Mail = durable; Nudge = ephemeral"*, principles P9/P10); §3.4 / §13.1 smallest-install (L114–122, `[mail]` explicitly off in Phase 0); README §"Principle 9 — Attribution" (L225–232: `created_by` native, "Identity verification … signature on bead provenance" = **optional, deferred**), §Phase 0 (L364 "no daemon, no mail"); F-MODE-COVERAGE F32 (L34 "P9 attribution + optional HMAC signing layer", Addressed; L87 revisit "HMAC signing on mail bus"); component-inventory C06 row (Depends on C04; Maps from A22d/A28k/B71; Key gap G36).
> Inventory ID: C06   Kind: component   Status: sweep-1

## 1. Purpose & responsibility

C06 is the **inter-agent coordination** layer: the two native Gas City messaging primitives by which one
agent (or the operator, or a control loop) hands a message to another — **Mail** (durable, queued,
addressed) and **Nudge** (ephemeral, fire-and-forget signal). It is Gas City concept 6 —
*"Messaging (Mail + Nudge); Mail = durable; Nudge = ephemeral"* (AI-CONTEXT §3.2 L90) — **adopted
wholesale, not rebuilt**. Every message carries Gas City's native `created_by` actor (P9), so coordination
traffic is attributed by the same mechanism beads and events are.

It is responsible for:
- **Exposing the two delivery semantics** as the coordination contract between agents/roles:
  - **Mail** — a *durable, addressed* message that survives the recipient being offline/suspended and is
    delivered (and acknowledgeable) when the recipient next runs. The persistence + ordering substrate is
    Gas City's (`[mail]`), not C06-authored.
  - **Nudge** — an *ephemeral* signal with no durability guarantee: a poke ("a bead is ready", "wake and
    reconcile") that is lost if no one is listening. Best-effort by construction.
- **Carrying attribution on every message** — `created_by` flows automatically (P9, README L227 "Gas City
  beads, events native `created_by`" / L371 "every bead and event carries `created_by`"; AI-CONTEXT §3.2:
  messaging maps to P9/P10). C06 adds **no** identity machinery of its own; it inherits the substrate's actor
  stamp (for Mail directly; for the ephemeral Nudge the concept-6→P9 reading, qualified in I3).
- **Naming the addressing surface** — who a message is *to* (an agent/role/seat handle, keyed on the C04
  `session.id` and the C41/C42 actor identity) and *from* (the `created_by` actor). C06 binds these
  identities into the Mail envelope; it does not mint them.
- **Being feature-gated by config presence** — Mail exists only when the `[mail]` section is present
  (C03's "section presence = capability" model; AI-CONTEXT §3.2 concept 4). It is **explicitly off in
  Phase 0** (AI-CONTEXT L122 "Explicitly off: `[mail]`"; README L364 "no … mail") and switches on in a
  later phase when multi-agent coordination is needed.

**What it is explicitly NOT:**
- **NOT a custom message queue / broker / delivery engine.** Mail durability, queueing, and Nudge fan-out
  are Gas City-native primitives (AI-CONTEXT §3.2). C06 must **not** build a message bus, retry engine,
  durable-queue, or pub/sub layer — those are the substrate's. (The bar: Mail+Nudge are native coordination
  primitives; any custom delivery machinery is a flagged anti-build — see §7.)
- **NOT the dispatcher (C05 Sling).** Sling *routes work* (a bead/wisp → an agent/pool) and decides who
  acts next; C06 *carries messages* between already-addressed parties. Dispatch is a routing decision;
  messaging is a transport. (AI-CONTEXT §3.2 concept 8 vs concept 6.)
- **NOT the event bus (C23).** C23 is the append-only, monotonic-seq *record of every action* (an audit/
  observability log everyone can read); C06 is *addressed* point-to-point/role coordination. They share P9/
  P10 but differ in shape: broadcast-record vs directed-message.
- **NOT the work-graph (C19/C20 beads).** A bead is durable *work state*; Mail is a durable *message*.
  Coordination *about* a bead may be Mail, but the bead ledger is C19's, not C06's. (A message is not a
  work item.)
- **NOT the identity / attribution authority (C41).** C41 owns the actor model and `created_by` semantics;
  C06 is a *consumer* that stamps inherited identity onto messages. C06 does not verify identity.
- **NOT a signing / secrets layer.** The "optional HMAC signing" mentioned in v4 is **optional and
  deferred** (README L229; D-14); its key is a *secret* (gap **G37**, owned by C03). C06 must **not** build
  a signing subsystem or a secrets store (§6, G36/§7). *Reciprocal seam (C41):* C06 and C41 **share gap
  G36** (inventory). When the deferred FE-3 signing lands, the HMAC signature would attach at **C06's Mail
  envelope** and **bind to C41's provenance-verification seam** (C41 §2 lists C06 as "Downstream (consumes
  the seam) — Optional HMAC mail signing binds a message to a C41 actor"; C41 §4.3). C06 owns the *carrier*
  (the envelope the signature rides on); C41 owns the *identity* the signature binds — neither builds it on
  the canonical track.

## 2. Context & dependencies

| Direction | Piece | Relationship |
|---|---|---|
| Upstream (hosts C06) | **C01 Gas City substrate** | Mail + Nudge *are* native Gas City concepts; the `gc` binary owns the `[mail]` machinery and the Nudge primitive. C06 = the faithful spec of those adopted concepts. |
| Upstream (sole declared dep) | **C04 session/provider** | The recipient of a message is an agent running in (or resumable to) a **C04 session**; addressing keys on the stable `session.id` C04 emits (C04 §3 "session-id keyed on by C06"). A durable Mail to a suspended session is delivered on C04 resume. |
| Upstream (configures C06) | **C03 config** | `[mail]` section presence gates Mail (capability-by-presence); C03 also owns the secrets gap **G37** behind any future signing key (D-14). |
| Upstream (identity) | **C41 identity / C42 rig** | `created_by` actor (C41) is stamped on every message; C42 role partitions scope *who may message whom* (e.g. worker↔judge isolation is a partition concern, not a C06 transport concern). |
| Peer (distinct, not used-by) | **C23 event bus** | Sibling P9/P10 primitive; messaging is directed, the event bus is the broadcast record. Listed to disambiguate, not as a dependency. |
| Downstream (uses C06) | control loops & coordinator roles — **C18 reconciler, C05 dispatch, Mayor/coordinator agents** | A Nudge wakes a reconciler tick / signals "bead ready"; Mail carries durable hand-offs between coordinator and worker roles. |

C06's sole *declared* dependency is **C04** (component-inventory). It is **not foundational** — it is a
Phase-later capability that switches on when multi-agent coordination is required.

## 3. Interfaces / contracts (sweep-1: named + described)

C06 surfaces **two delivery primitives** behind the Gas City messaging concept. Named operation
*families* (concrete signatures/envelope schema are sweep-2):

1. **Mail — send (durable, addressed).** Hand a durable, attributed message to a named recipient
   (agent/role/seat). Persisted by the substrate; survives recipient offline/suspended. Carries
   `created_by` (from), recipient address (to), and payload.
2. **Mail — receive / acknowledge.** A recipient drains its durable inbox and (per the adopted substrate's
   semantics) acknowledges consumption. Delivery is *at-least-once on resume* — **the adopted Gas City
   `[mail]` semantics C06 relies on, not a guarantee v4 states or C06 implements** (v4 states only "Mail =
   durable", AI-CONTEXT §3.2 L90; the at-least-once/drain-on-run reading is the faithful entailment of
   "durable addressed message", confirmed against real `gc` at sweep-2): a session that was suspended when
   Mail arrived receives it when C04 brings it back.
3. **Nudge — signal (ephemeral).** Emit a best-effort poke to a recipient/topic ("wake", "bead ready").
   No durability, no ack, no retry: lost if no live listener. The lightweight wake/coordination signal.
4. **Addressing / identity binding.** Resolve a recipient handle (keyed on C04 `session.id` + C41/C42
   actor) and stamp the inherited `created_by` (from). C06 binds identities into the envelope; it does not
   mint or verify them.
5. **Config gate.** Mail is available iff `[mail]` is configured (C03 section-presence). Nudge is the
   lighter primitive available in the coordination-on configuration. (Whether Nudge is independently
   gated is unspecified — see OQ.)

> [FAITHFUL-FILL] v4 names the two primitives and their defining property (*Mail durable / Nudge
> ephemeral*, P9/P10 — AI-CONTEXT §3.2 L90) but does not enumerate the operations or the envelope schema.
> The five families above are the minimal faithful surface entailed by "a durable addressed message" (⇒
> send + receive/ack + an address) and "an ephemeral signal" (⇒ a single fire-and-forget op), plus the
> inherited-attribution requirement (⇒ identity binding) and the capability-by-presence model (⇒ config
> gate). No transport/queue/retry operation is invented — those are substrate-owned (§1 NOT-list). Exact
> signatures + envelope fields are deferred to sweep-2.

**Inbound contracts:**
- **Send-Mail / send-Nudge (from any agent or control loop)** — given a recipient address + payload,
  deliver per the chosen semantic. `created_by` is supplied by the substrate, not the caller.
- **Config surface (from C03)** — `[mail]` present ⇒ durable Mail enabled; absent ⇒ no Mail (Phase 0).
- **Partition policy (from C42)** — which roles may address which (read/write partition scoping); C06
  carries messages within the bounds C42 declares but does not author the policy.

**Outbound contracts:**
- **Delivered Mail to recipient inbox** — durable, attributed, drained-on-run (incl. drained on C04
  resume for a session that was offline at send time).
- **Delivered Nudge** — best-effort signal to a live recipient/topic; silently dropped if none.
- **Attribution surface** — every message carries `created_by`, so messaging traffic is attributable by
  the same P9 mechanism as beads/events (the input F14/F32 attribution claims rely on, §6).

**Invariants:**
- **I1 (Mail durability):** an accepted Mail is delivered at-least-once to its addressed recipient even
  across recipient suspend/restart — to the extent the adopted Gas City `[mail]` mechanism provides
  durable queueing. The durability is a *substrate property C06 adopts and relies on*, not one C06-the-spec
  independently implements. (AI-CONTEXT §3.2 L90 "Mail = durable".)
- **I2 (Nudge is best-effort):** a Nudge has **no** durability or delivery guarantee by construction; a
  lost Nudge is correct behavior, not a fault. Anything that *must* be delivered uses Mail. (L90 "Nudge =
  ephemeral".)
- **I3 (attribution totality):** every message carries a `created_by` actor; C06 adds no path that
  bypasses it. For **Mail** this is the substrate's native bead/event-class `created_by` stamp (P9, README
  L227/L371 "every bead and event carries `created_by`"), since a durable Mail is a recorded action. For
  the **ephemeral Nudge**, attribution rests on the concept-6 → P9/P10 mapping (AI-CONTEXT §3.2 L90: Messaging
  → P9, P10), a **[FAITHFUL-FILL] inference**: README's demonstrated `created_by` evidence is for beads and
  events, and a Nudge is neither a bead nor necessarily an event — whether the ephemeral signal flows through
  the *same* native stamp path is an adopted-substrate property to verify against real `gc` (→ OQ/sweep-2),
  not a guarantee C06-the-spec demonstrates. The canonical-track posture is *attributed coordination on both
  primitives*; the Nudge totality is the faithful reading, qualified here so it is not read as a proven
  substrate fact.
- **I4 (no self-asserted-identity hardening on the canonical track):** `created_by` is **self-asserted**
  (not cryptographically verified); message *authenticity* (sender truly is who it claims) is the
  optional/deferred HMAC-signing concern (G36/G37, D-14), **out of scope** here. C06 stamps identity; it
  does not prove it.
- **I5 (capability by presence):** Mail does not exist unless `[mail]` is configured (C03); C06 is dark in
  Phase 0 (AI-CONTEXT L122; README L364).

## 4. Data model / state

C06 owns **message-in-transit shape**, not durable storage. The durable Mail queue and the actor registry
live in the substrate.

| State | Owner | Notes |
|---|---|---|
| Mail envelope (from `created_by`, to recipient-address, payload, durability=durable) | C06 defines the shape; **Gas City `[mail]` persists it** | C06 does not own the queue/store; it adopts the substrate's durable Mail. Schema → sweep-2. |
| Nudge signal (from, to/topic, payload; no persistence) | C06 defines the shape; transient | Nothing durable to own — ephemeral by I2. |
| Recipient address ↔ live session | **C04** (`session.id`) + **C41/C42** (actor) | C06 *keys on* these; it does not own session liveness or the actor registry. |
| `created_by` actor | **C41** (identity/attribution) | Inherited, stamped, never minted by C06 (I3). |
| Durable Mail queue / inbox storage | **Gas City `[mail]`** (C01) | The persistence + ordering substrate; the explicit anti-build for C06 (§1, §7). |
| Signing key (if HMAC ever enabled) | **secret → C03/G37** (D-14) | Not stored or handled by C06; deferred. |

**Lifecycle (named; schema/diagram are sweep-2):**
- **Mail:** `composed → accepted(persisted) → {recipient offline: queued} → delivered-on-run → acked`.
  A recipient suspended at accept time receives on C04 resume (I1).
- **Nudge:** `emitted → {live listener: delivered | no listener: dropped}`. No queued state (I2).

## 5. Behavior

**Durable hand-off (Mail):**
1. An agent/coordinator composes a Mail to a named recipient (role/seat resolved via C04 `session.id` +
   C41/C42 actor). `created_by` is stamped by the substrate (I3).
2. The Gas City `[mail]` mechanism accepts and persists it (durable queue — substrate, not C06).
3. If the recipient is offline/suspended, it stays queued; when the recipient next runs — including after a
   **C04 resume** of a previously-suspended session — it drains and acks. At-least-once on run (I1).

**Ephemeral signal (Nudge):**
1. A producer emits a Nudge ("bead ready" / "wake and reconcile") to a recipient or topic.
2. A live listener receives it; if none is listening it is dropped — and that is correct (I2). Anything
   requiring guaranteed delivery is sent as Mail instead.

**Attribution (always-on):** both paths carry `created_by`; messaging traffic is queryable/attributable by
the same P9 mechanism that stamps beads and events (README L227/L371; the property F14/F32 lean on, §6 —
Mail via the native bead/event-class stamp, Nudge via the concept-6→P9 faithful reading, I3).

**Degraded / boundary behavior:**
- **Recipient never returns:** a durable Mail stays queued (substrate retention); C06 does not define a
  dead-letter / expiry policy — unspecified by v4 (→ OQ, deferred).
- **Mail disabled (`[mail]` absent / Phase 0):** durable coordination is simply unavailable; agents fall
  back to Nudge-only ephemeral signalling, or coordination routes through beads/dispatch. (Phase-0 posture
  per AI-CONTEXT L122 / README L364.)
- **Unauthenticated/forged message:** because `created_by` is self-asserted (I4), a forged-sender Mail is
  *not* detected on the canonical track — this is exactly G36, addressed-by-deferral in §6.

## 6. Failure modes & handling

| F-mode | Applies how | Handling per v4 |
|---|---|---|
| **F32** Mail-injection / unsigned coordination | C06 *is* the coordination/mail surface a forged or unsigned message would ride on | **Addressed** per F-MODE-COVERAGE L34 via **"P9 attribution + optional HMAC signing layer."** On the canonical track the *active* control is **P9 attribution** (`created_by` on every message, I3) — every message is *attributed*. The **HMAC signing** half is **optional and deferred** (README L229; revisit at Phase 3+, F-MODE-COVERAGE L87; D-14). C06 must **not** build the signing layer; it provides the attributed-message surface and records that authenticity-verification is deferred (G36/G37). This is the *partial-by-design* reality behind the "Addressed" label — see G36. |
| **F14** Attribution collapse | Coordination messages are actions that must carry an actor or attribution has a hole | **Addressed** (F-MODE-COVERAGE L32) by P9's native `created_by` — inherited, not C06-built (I3; for Mail the bead/event-class stamp, for Nudge the concept-6→P9 faithful reading, I3). C06's contribution is *not bypassing* the stamp; the guarantee is the substrate's. |
| **F17** Parallel agents on shared dirs lose data | Coordination *between* parallel agents flows over C06, but the data-loss failure is a **filesystem/partition** concern | **Addressed elsewhere** (F-MODE-COVERAGE L86) via Gas City **worktree isolation per run (C42)** + OPA / read-isolation enforcement on shared partitions (**C34**, with the lethal-trifecta blast-radius bound **C43**, per D-13) — **not C06-native**. C06 carries the messages; the isolation that prevents shared-dir clobber is C42/C34/C43's, not C06's. C06 must not build locking/coordination-of-writes machinery. |

**Gap-driven failure mode (assigned: G36):**

> [AMBIGUITY: G36] **Is attribution *integrity* (recipient can trust the claimed sender) provided, or only
> attribution *presence* (a sender is stamped)?**
> Reading A (presence): P9 stamps `created_by` natively on every bead/event/message; F-MODE-COVERAGE marks
> F32 **Addressed** ("P9 attribution + optional HMAC signing"). On this reading, *attributed* coordination
> is sufficient for the canonical track and the failure is handled.
> Reading B (integrity, the gap): G36 observes attribution is **self-asserted** — "Identity verification —
> verify claimed actor matches actual" is **"optional, deferred"** (README L229), and F32's signing half is
> **optional** ("an optional guard does not address a security failure"). On this reading, a *forged-sender*
> message is undetectable and F32 is only *partially* addressed despite the "Addressed" label.
> **Chosen (most consistent with v4 + binding decisions):** Reading A is the canonical-track *operating
> posture*, with Reading B recorded as the honest residual. Per **D-14**, the "optional HMAC signing" stays
> **optional/deferred** and its key is a **secret = G37 (owned by C03)** — distinct from the signing
> enhancement (FE-3) itself. C06 therefore **(a)** guarantees attribution *presence* (I3, the active P9
> control), **(b)** explicitly does **not** build a signing/secrets/verification layer (that would
> contradict D-14 and the bar), and **(c)** flags the integrity shortfall as a residual: message
> *authenticity* is deferred to the FE-3 signing enhancement, blocked on G37, revisited at FE-3's trigger.
> This is **address-by-deferral with reason**, escalated to review-log (OQ1), not a silent acceptance of
> the "Addressed" label.

## 7. Cross-cutting

- **Security:** attribution is present on every message (P9, I3) but **self-asserted** (I4) — no
  authenticity/integrity guarantee on the canonical track. The optional HMAC signing that would add
  integrity is **deferred** (D-14, G36); its key is a **secret = G37** (C03-owned). C06 must not store
  keys or sign — flagged, not owned. Sender↔recipient *authorization* (who may message whom) is the C42
  partition's, carried-not-authored by C06.
- **Cost:** Nudge is the cheap ephemeral signal; Mail incurs durable-write cost in the substrate. No cost
  model exists in v4 (G32, not C06's gap) — deferred.
- **Scale:** Mail throughput/queue scale is the adopted Gas City `[mail]` substrate's property, not
  specified by v4 for C06; not invented here (→ OQ, deferred).
- **Observability:** messages carry `created_by` and (for durable Mail) are inspectable via the substrate;
  coordination is attributable by the same P9 key as beads/events — the input the attribution-dependent
  F-modes (F14/F32) rely on.
- **Ops / the bar (anti-build flags):** **Mail (durable) and Nudge (ephemeral) are NATIVE Gas City
  coordination primitives** (AI-CONTEXT §3.2 concept 6). Any custom **message queue, broker, pub/sub,
  retry/back-off engine, durable-inbox store, or delivery-guarantee machinery** is a **flagged anti-build**
  — it duplicates the substrate and earns no principle-tied capability (HANDOFF §2 bar → DROP). C06 is a
  **config-and-contract** component (turn on `[mail]`; name the two semantics + envelope), not a build.
  The HMAC signing layer is likewise **dropped** here (optional/deferred, D-14). No Go fork (pack-only
  extension, AI-CONTEXT §3.5).

## 8. Acceptance criteria & test strategy (sweep-1, high level)

- **AC1 (durable Mail survives offline recipient):** a Mail sent to a suspended/offline recipient is
  delivered (at-least-once — the *adopted* substrate semantics, I1, verified against real `gc`) when that
  recipient next runs — including after a **C04 resume** — carrying its `created_by` (AI-CONTEXT §3.2 L90
  "Mail = durable" is the v4 anchor; the delivery-on-resume behavior is the faithful entailment, not a
  v4-stated contract).
- **AC2 (Nudge is ephemeral):** a Nudge with no live listener is dropped with no error and no queued state;
  delivery to a live listener is best-effort (I2).
- **AC3 (attribution totality):** every Mail carries the native `created_by` actor (bead/event-class stamp,
  README L227/L371) and C06 adds no path to emit an anonymous coordination message (I3). For the ephemeral
  **Nudge**, the test confirms `created_by` is present *to the extent the adopted substrate stamps the
  ephemeral primitive* — the concept-6→P9/P10 reading verified against real `gc` (I3 [FAITHFUL-FILL]; →
  sweep-2 if `gc` proves Nudge un-stamped, that is a faithful gap to record, not a C06-built fix).
- **AC4 (capability by presence):** with `[mail]` absent (Phase-0 config) durable Mail is unavailable and
  the system degrades to Nudge/bead coordination; adding `[mail]` enables it with no other change (I5;
  AI-CONTEXT L122).
- **AC5 (no custom delivery machinery — anti-build audit):** an import/usage audit shows C06 carries
  messages over the native Gas City Mail/Nudge primitives and introduces **no** queue/broker/retry/signing
  subsystem (§7 bar; F-MODE L34/L87 keep signing optional).
- **AC6 (G36 honesty):** the spec records that message *authenticity* is **not** verified on the canonical
  track (self-asserted `created_by`), that integrity is deferred to FE-3 signing blocked on G37 (D-14), and
  the residual is escalated to review-log — i.e. the "Addressed" F32 label is qualified, not relitigated.

## 9. Open questions (→ review-log)

- **OQ1 (G36, top):** F32 is labelled **Addressed** but its integrity half (HMAC signing) is **optional/
  deferred** and its key is a deferred secret (G37). When does authenticity verification become mandatory
  (FE-3 trigger), and until then is "attributed-but-unsigned" coordination an accepted residual risk for
  L4/L5 operation? *Recorded as address-by-deferral; needs an explicit FE-3 trigger ruling.*
- **OQ2 (Mail retention / dead-letter):** v4 says Mail is "durable" but never bounds retention or defines a
  dead-letter/expiry policy for a recipient that never returns. Inherited from the substrate? Needed before
  sweep-2 envelope/lifecycle detail.
- **OQ3 (Nudge gating):** Is Nudge independently feature-gated, or always-on once any coordination config is
  present? v4 gates `[mail]` explicitly but is silent on Nudge's gate (§3 family 5).
- **OQ4 (addressing granularity):** Are recipients addressed by individual `session.id`, by C42 role, by
  seat, or by topic (for Nudge)? v4 names the primitives but not the address space; inferred to key on C04
  `session.id` + C41/C42 actor, but the granularity is unstated (→ sweep-2 envelope schema).
